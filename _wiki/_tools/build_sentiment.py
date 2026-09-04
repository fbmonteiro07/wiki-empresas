"""
build_sentiment.py — Bull/bear × hot/cold sentiment indicator for the wiki universe.

Pipeline (each step caches into _wiki/_data/sentiment/ so later steps can run offline):
  tweets : read the twitter-briefing corpus (E:\\.claude\\data\\twitter-briefing\\tweets.sqlite, read-only),
           map every tweet to wiki tickers (cashtag + company-name aliases), score tone with a
           transparent finance lexicon, aggregate per ticker-day.
  bbg    : Bloomberg history (bdh, local terminal): PX_LAST, BEST_EPS (1BF), BEST_ANALYST_RATING,
           SI_PERCENT_EQUITY_FLOAT for every company in estimates.json.
  panel  : weekly (Friday) cross-sectional panel — attention, tone, news volume, EPS revision,
           rating drift, short interest — plus forward 1w/4w returns, raw and universe-relative.
  backtest: weekly rank IC per component and composite, quintile spreads, 2-D quadrant returns.
  dash   : _wiki/_dashboards/sentiment.html (self-contained, theme-aware).

Usage: py build_sentiment.py [--step tweets|bbg|bbglong|mail_merge|sellside|panel|long|leadlag|picks|events_pull|events|dash|all] [--no-bbg]

Nightly: `refresh_sentiment.bat` (17:40 weekdays) runs the two Outlook PowerShell sweeps + the BBG pulls,
then the 18:15 `refresh_features.py` chain reruns this script with --no-bbg (caches) to rebuild the panels,
the event study and the dashboard. See INFRA.md §3.
Read-only on pages; writes only to _wiki/_data/sentiment and _wiki/_dashboards.
"""
import sys, os, re, json, math, socket, sqlite3, argparse, datetime as dt
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]           # _wiki
DATA = ROOT / "_data" / "sentiment"; DATA.mkdir(parents=True, exist_ok=True)
DASH = ROOT / "_dashboards"
TWEET_DB = Path(r"E:\.claude\data\twitter-briefing\tweets.sqlite")
START = "2026-05-01"                                  # dense tweet coverage starts May 2026
TODAY = dt.date.today()

def bbg_up(host="127.0.0.1", port=8194, timeout=2.0):
    """Is this machine's Bloomberg Terminal serving the local API? (bdp/bdh/bds are LOCAL-ONLY since 2026-08-12.)
    Probed with a 2s TCP connect because blpapi itself retries a dead port for ~60s per call."""
    try:
        with socket.create_connection((host, port), timeout=timeout): return True
    except OSError: return False

# ----------------------------------------------------------------------------- universe / aliases
def load_universe():
    est = json.load(open(ROOT / "_data" / "estimates.json", encoding="utf-8"))["companies"]
    return {t: {"bbg": v["bbg"], "name": v.get("name", t), "ccy": v.get("ccy")} for t, v in est.items()}

# Company-name aliases. Case-insensitive unless listed in CASE_SENSITIVE (ambiguous common words).
ALIASES = {
 "AAOI": ["Applied Optoelectronics", "Applied Opto"], "AAPL": ["Apple"], "ADI": ["Analog Devices"],
 "ADVANTEST": ["Advantest"], "AEIS": ["Advanced Energy"], "AGX": ["Argan"], "AIXA": ["Aixtron"],
 "AKAM": ["Akamai"], "ALAB": ["Astera Labs", "Astera"], "AMAT": ["Applied Materials"], "AMD": ["AMD"],
 "AMZN": ["Amazon", "AWS"], "ANET": ["Arista"], "AOSL": ["Alpha and Omega Semi", "Alpha & Omega"],
 "APH": ["Amphenol"], "APP": ["AppLovin"], "ARM": ["Arm Holdings"], "ASML": ["ASML"], "AVGO": ["Broadcom"],
 "AXTI": ["AXT Inc"], "BE": ["Bloom Energy"], "BESI": ["BE Semiconductor", "Besi"], "BKNG": ["Booking Holdings", "Booking.com"],
 "CDNS": ["Cadence"], "CEG": ["Constellation Energy"], "CIEN": ["Ciena"], "COHR": ["Coherent Corp", "Coherent"],
 "CRDO": ["Credo"], "CRM": ["Salesforce"], "CRWD": ["CrowdStrike"], "CRWV": ["CoreWeave"], "CSCO": ["Cisco"],
 "DELL": ["Dell"], "DISCO": ["Disco Corp"], "ETN": ["Eaton"], "FLEX": ["Flex Ltd"], "FSLY": ["Fastly"],
 "GEV": ["GE Vernova", "Vernova"], "GLW": ["Corning"], "GOOG": ["Google", "Alphabet", "Gemini"], "HPE": ["Hewlett Packard Enterprise", "HPE"],
 "IFX": ["Infineon"], "INTC": ["Intel"], "KIOXIA": ["Kioxia"], "KLAC": ["KLA Corp", "KLA"], "LITE": ["Lumentum"],
 "LRCX": ["Lam Research"], "MCHP": ["Microchip Technology"], "MEDIATEK": ["MediaTek"], "META": ["Meta"],
 "MP": ["MP Materials"], "MRVL": ["Marvell"], "MSFT": ["Microsoft", "Azure"], "MU": ["Micron"], "NBIS": ["Nebius"],
 "NET": ["Cloudflare"], "NFLX": ["Netflix"], "NOW": ["ServiceNow"], "NVDA": ["Nvidia", "NVIDIA"], "NVT": ["nVent"],
 "NVTS": ["Navitas"], "NXPI": ["NXP"], "ON": ["onsemi", "ON Semiconductor"], "ORCL": ["Oracle"], "PANW": ["Palo Alto Networks"],
 "PLTR": ["Palantir"], "POET": ["POET Technologies"], "POWI": ["Power Integrations"], "PWR": ["Quanta Services"],
 "QCOM": ["Qualcomm"], "RDDT": ["Reddit"], "SAMSUNG": ["Samsung Electronics", "Samsung"], "SANM": ["Sanmina"],
 "SHOP": ["Shopify"], "SKHYNIX": ["SK Hynix", "SK hynix", "Hynix"], "SMCI": ["Supermicro", "Super Micro"], "SMIC": ["SMIC"],
 "SMTC": ["Semtech"], "SNDK": ["Sandisk", "SanDisk"], "SNPS": ["Synopsys"], "SPOT": ["Spotify"], "STX": ["Seagate"],
 "TEL": ["TE Connectivity"], "TER": ["Teradyne"], "TLN": ["Talen Energy", "Talen"], "TM": ["Toyota"],
 "TOKYOELEC": ["Tokyo Electron"], "TSEM": ["Tower Semiconductor"], "TSLA": ["Tesla"], "TSM": ["TSMC", "Taiwan Semi"],
 "TXN": ["Texas Instruments"], "UBER": ["Uber"], "VECO": ["Veeco"], "VEEV": ["Veeva"], "VRT": ["Vertiv"],
 "VST": ["Vistra"], "WDC": ["Western Digital"], "WMB": ["Williams Companies"], "WOLF": ["Wolfspeed"],
 # data-infra / observability pages (added 2026-09-04)
 "SNOW": ["Snowflake"], "MDB": ["MongoDB"], "DDOG": ["Datadog"], "DT": ["Dynatrace"], "ESTC": ["Elasticsearch", "Elastic N.V"],
}
CASE_SENSITIVE = {"Apple", "Meta", "Oracle", "Uber", "Intel", "Dell", "Eaton", "Corning", "Coherent", "Booking.com", "Reddit",
                  "Argan", "Samsung", "Micron", "Cadence", "Arista", "Credo", "Toyota", "Talen", "Flex Ltd", "KLA", "AMD",
                  "ASML", "SMIC", "HPE", "AWS", "Azure", "Gemini", "Tesla", "Google", "Amazon", "Microsoft", "Netflix", "Spotify", "Snowflake"}
# Cashtags that collide with English words are still fine because the '$' prefix disambiguates.
PRIVATE = {"ANTHROPIC", "OPENAI", "CEREBRAS"}

ALIAS_NEG = {"Samsung": r"(?! Electro| SDI| Bio| Life| Fire| Securities| C&T| Heavy| Display| SDS| Card)", "Toyota": r"(?! Industries| Tsusho| Boshoku| Gosei)",
             "Meta": r"(?! Platforms Inc\.? \(FB\)| description| analysis)", "Google": r"(?! Cloud Next| Play Store)"}
def build_matchers(universe):
    cash = re.compile(r"\$([A-Za-z]{1,6})\b")
    pats = []
    for t, names in ALIASES.items():
        if t not in universe: continue
        for n in names:
            flags = 0 if n in CASE_SENSITIVE else re.IGNORECASE
            pats.append((t, re.compile(r"(?<![A-Za-z])" + re.escape(n) + ALIAS_NEG.get(n, "") + r"(?![a-z])", flags)))
    return cash, pats

# ----------------------------------------------------------------------------- tone lexicon
BULL = ["beat", "beats", "raise", "raised", "raises", "upgrade", "upgraded", "upgrades", "strong", "stronger", "strength",
        "accelerat", "record", "upside", "bullish", "outperform", "blowout", "surge", "surges", "surging", "rally", "rallies",
        "breakout", "above consensus", "ahead of", "sold out", "tight", "shortage", "pricing power", "guide up", "guided up",
        "all-time high", "ath", "momentum", "buy", "buying", "long", "top pick", "expand", "expands", "expansion", "win", "wins",
        "winner", "demand", "robust", "exceed", "exceeds", "impressive", "inflect", "inflection", "reaccelerat", "oversubscribed",
        "capacity add", "ramp", "ramping", "new high", "positive", "bull case", "undervalued", "cheap"]
BEAR = ["miss", "misses", "missed", "cut", "cuts", "downgrade", "downgraded", "downgrades", "weak", "weaker", "weakness",
        "decelerat", "slow", "slowing", "slowdown", "downside", "bearish", "underperform", "plunge", "plunges", "crash", "crashes",
        "selloff", "sell-off", "below consensus", "inventory", "glut", "oversupply", "overcapacity", "pushout", "push-out", "delay",
        "delayed", "delays", "cancel", "cancelled", "canceled", "warn", "warns", "warning", "guide down", "guided down", "lower guidance",
        "bubble", "overvalued", "expensive", "short", "shorting", "fraud", "lawsuit", "probe", "investigation", "subpoena", "tariff",
        "tariffs", "ban", "banned", "restriction", "restrictions", "layoff", "layoffs", "disappoint", "disappointing", "concern",
        "concerns", "risk", "risks", "headwind", "headwinds", "competition", "erosion", "loses", "lost share", "bear case", "drop",
        "drops", "falls", "fell", "tumble", "tumbles", "sink", "sinks", "negative", "peak", "peaked", "top is in"]
NEG = re.compile(r"\b(not|no|never|isn't|isnt|aren't|don't|dont|doesn't|won't|without|hardly)\b", re.IGNORECASE)
def _lex(words):
    return re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)) + r")(?![a-z])", re.IGNORECASE)
BULL_RE, BEAR_RE = _lex(BULL), _lex(BEAR)

def tone(text):
    """(score in [-1,1], n_hits). Negation inside the preceding 3 words flips a hit."""
    b = n = 0
    for rx, sign in ((BULL_RE, 1), (BEAR_RE, -1)):
        for m in rx.finditer(text):
            pre = text[max(0, m.start() - 30):m.start()]
            s = -sign if NEG.search(" ".join(pre.split()[-3:])) else sign
            if s > 0: b += 1
            else: n += 1
    tot = b + n
    return ((b - n) / tot if tot else 0.0), tot

# ----------------------------------------------------------------------------- step: tweets
def step_tweets(universe):
    cash, pats = build_matchers(universe)
    con = sqlite3.connect(str(TWEET_DB), timeout=60)   # E: is a network share — file: URIs break; plain read connection
    cur = con.execute("""select handle, category, substr(created_at,1,10) d, text, like_count, retweet_count, reply_count, view_count, is_reply
                         from tweets where created_at >= ? and coalesce(is_retweet,0)=0 and text is not null""", (START,))
    daily = defaultdict(lambda: defaultdict(lambda: {"m_cur": 0.0, "m_wire": 0.0, "eng": 0.0, "tone_w": 0.0, "tone_n": 0, "w": 0.0,
                                                     "bull": 0, "bear": 0, "top": []}))
    handles = defaultdict(lambda: defaultdict(float))
    n_tw = n_hit = 0
    for handle, cat, d, text, lk, rt, rp, vw, isr in cur:
        n_tw += 1
        found = set()
        for m in cash.finditer(text):
            t = m.group(1).upper()
            if t in universe and t not in PRIVATE: found.add(t)
        for t, rx in pats:
            if t in found: continue
            if rx.search(text): found.add(t)
        if not found: continue
        n_hit += 1
        sc, nh = tone(text)
        eng = math.log1p((lk or 0) + 2 * (rt or 0) + 0.5 * (rp or 0))
        w = 1.0 / len(found) if len(found) <= 3 else 0.25 / len(found)   # ticker lists carry little per-name signal
        for t in found:
            r = daily[t][d]
            if cat == "news": r["m_wire"] += w
            else: r["m_cur"] += w
            r["eng"] += w * eng
            if nh:
                ww = w * (1 + eng)
                r["tone_w"] += ww * sc; r["w"] += ww; r["tone_n"] += 1
                if sc > 0: r["bull"] += 1
                elif sc < 0: r["bear"] += 1
            handles[t][handle] += w
            if len(r["top"]) < 3 and cat != "news" and eng > 3:
                r["top"].append({"h": handle, "t": text[:180].replace("\n", " "), "s": round(sc, 2), "e": round(eng, 1)})
    con.close()
    out = {"asof": TODAY.isoformat(), "start": START, "tweets_scanned": n_tw, "tweets_matched": n_hit,
           "tickers": {t: {d: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for d, r in sorted(days.items())}
                       for t, days in daily.items()},
           "top_handles": {t: sorted(h.items(), key=lambda x: -x[1])[:8] for t, h in handles.items()}}
    (DATA / "tweet_daily.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"tweets: scanned {n_tw:,} · matched {n_hit:,} · tickers with mentions {len(daily)}")
    return out

# ----------------------------------------------------------------------------- step: bbg
def step_bbg(universe):
    sys.path.insert(0, r"E:\bloomberg_api")
    from bloomberg import bdh
    start = "20260401"; end = TODAY.strftime("%Y%m%d")
    bbgs = [v["bbg"] for t, v in universe.items() if t not in PRIVATE]
    inv = {v["bbg"]: t for t, v in universe.items()}
    series = defaultdict(lambda: defaultdict(dict))   # ticker -> field -> date -> value
    def pull(flds, chunk, **ov):
        for i in range(0, len(chunk), 15):
            sub = chunk[i:i + 15]
            try:
                df = bdh(sub, flds, start, end, **ov)
            except Exception as e:
                print("  bdh fail", sub[:2], flds, str(e)[:80]); continue
            for _, r in df.iterrows():
                v = r["value"]
                if v is None or (isinstance(v, float) and math.isnan(v)): continue
                series[inv[r["ticker"]]][r["field"]][str(r["date"])[:10]] = float(v)
    print("bbg: prices/rating/SI ...");  pull(["PX_LAST", "BEST_ANALYST_RATING", "SI_PERCENT_EQUITY_FLOAT"], bbgs)
    print("bbg: BEST_EPS 1BF ...");      pull(["BEST_EPS"], bbgs, BEST_FPERIOD_OVERRIDE="1BF")
    # benchmark
    pull(["PX_LAST"], ["SOX Index"]) if "SOX Index" in inv else None
    try:
        df = bdh(["SOX Index", "NDX Index"], ["PX_LAST"], start, end)
        for _, r in df.iterrows():
            series["_" + r["ticker"].split()[0]]["PX_LAST"][str(r["date"])[:10]] = float(r["value"])
    except Exception as e: print("  bench fail", e)
    out = {"asof": TODAY.isoformat(), "series": series}
    (DATA / "bbg_history.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"bbg: {len(series)} tickers · PX rows {sum(len(s['PX_LAST']) for s in series.values() if 'PX_LAST' in s):,}")
    return out

# ----------------------------------------------------------------------------- step: bbglong (Bloomberg social/news history, 2024→)
LONG_START = "20231201"
SOCIAL_FLDS = ["TWITTER_SENTIMENT_DAILY_AVG", "TWITTER_PUBLICATION_COUNT", "TWITTER_POS_SENTIMENT_COUNT", "TWITTER_NEG_SENTIMENT_COUNT",
               "NEWS_SENTIMENT_DAILY_AVG", "NEWS_PUBLICATION_COUNT"]
def step_bbglong(universe):
    """Bloomberg's own per-ticker Twitter/news sentiment + counts, prices, ratings, SI and BEST_EPS 1BF since Dec-2023.
    This is the backward track: independent of the twitter-briefing handle list, available for every name."""
    sys.path.insert(0, r"E:\bloomberg_api")
    from bloomberg import bdh
    end = TODAY.strftime("%Y%m%d")
    bbgs = [v["bbg"] for t, v in universe.items() if t not in PRIVATE]
    inv = {v["bbg"]: t for t, v in universe.items()}
    series = defaultdict(lambda: defaultdict(dict))
    def pull(flds, chunk, **ov):
        for i in range(0, len(chunk), 8):
            sub = chunk[i:i + 8]
            try: df = bdh(sub, flds, LONG_START, end, **ov)
            except Exception as e: print("  bdh fail", sub[:2], flds[:2], str(e)[:80]); continue
            for _, r in df.iterrows():
                v = r["value"]
                if v is None or (isinstance(v, float) and math.isnan(v)): continue
                series[inv[r["ticker"]]][r["field"]][str(r["date"])[:10]] = float(v)
    print("bbglong: prices/rating/SI ..."); pull(["PX_LAST", "BEST_ANALYST_RATING", "SI_PERCENT_EQUITY_FLOAT"], bbgs)
    print("bbglong: social ...");          pull(SOCIAL_FLDS[:4], bbgs)
    print("bbglong: news ...");            pull(SOCIAL_FLDS[4:], bbgs)
    print("bbglong: BEST_EPS 1BF ...");    pull(["BEST_EPS"], bbgs, BEST_FPERIOD_OVERRIDE="1BF")
    out = {"asof": TODAY.isoformat(), "start": LONG_START, "series": series}
    (DATA / "bbg_long.json").write_text(json.dumps(out), encoding="utf-8")
    n = sum(len(s.get("TWITTER_PUBLICATION_COUNT", {})) for s in series.values())
    print(f"bbglong: {len(series)} tickers · twitter-count days {n:,}")
    return out

# ----------------------------------------------------------------------------- helpers
def fridays(start, end):
    d = dt.date.fromisoformat(start); d += dt.timedelta((4 - d.weekday()) % 7)
    while d <= end: yield d; d += dt.timedelta(7)

def last_on_or_before(series, d):
    """series: {iso: val} sorted keys; return value at latest date <= d (within 10 days)."""
    best = None
    for k in series:   # dicts small (≤110 keys); linear ok
        if k <= d and (best is None or k > best): best = k
    if best and (dt.date.fromisoformat(d) - dt.date.fromisoformat(best)).days <= 10: return series[best]
    return None

def zscore(vals):
    xs = [v for v in vals.values() if v is not None]
    if len(xs) < 5: return {k: None for k in vals}
    mu = sum(xs) / len(xs); sd = (sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5 or 1.0
    return {k: (None if v is None else max(-3.0, min(3.0, (v - mu) / sd))) for k, v in vals.items()}

def rank(vals):
    ks = [k for k, v in vals.items() if v is not None]; ks.sort(key=lambda k: vals[k])
    r = {}; i = 0
    while i < len(ks):
        j = i
        while j + 1 < len(ks) and vals[ks[j + 1]] == vals[ks[i]]: j += 1
        for k in ks[i:j + 1]: r[k] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(a, b):
    ks = [k for k in a if a.get(k) is not None and b.get(k) is not None]
    if len(ks) < 8: return None, len(ks)
    ra, rb = rank({k: a[k] for k in ks}), rank({k: b[k] for k in ks})
    ma = sum(ra.values()) / len(ks); mb = sum(rb.values()) / len(ks)
    cov = sum((ra[k] - ma) * (rb[k] - mb) for k in ks)
    va = sum((ra[k] - ma) ** 2 for k in ks); vb = sum((rb[k] - mb) ** 2 for k in ks)
    return (cov / (va * vb) ** 0.5 if va and vb else None), len(ks)

# ----------------------------------------------------------------------------- panel + backtest (generic)
HORIZONS = {"1w": 7, "15d": 15, "4w": 28}      # calendar days forward; 15d = Felipe's preferred horizon (2026-09-02)

COMPONENTS = {
    # key: (label, family)  — family: hot (attention) / bull (direction) / crowd
    "att":     ("Attention (curated mentions vs trailing 4w)", "hot"),
    "news":    ("News-wire volume vs trailing 4w",             "hot"),
    "tone":    ("Tweet tone (lexicon, engagement-weighted)",    "bull"),
    "tone_chg":("Tweet tone change vs trailing 4w",            "bull"),
    "eps_rev": ("EPS revision, BEST_EPS 1BF, 4w %",            "bull"),
    "rating":  ("Analyst rating drift, 4w",                    "bull"),
    "si":      ("Short interest % float (level)",              "crowd"),
    "ss_att":  ("Sell-side note flow vs trailing 4w (Outlook)", "crowd"),
    "ss_tone": ("Sell-side subject tone (lexicon)",            "bull"),
    "ss_act":  ("Sell-side net rating changes, week",          "bull"),
    "ss_pt":   ("Sell-side avg price-target change %, week",   "bull"),
    "ss_est":  ("Sell-side net estimate revisions, week",      "bull"),
}
LONG_COMPONENTS = {
    "att":      ("BBG Twitter publication count vs trailing 4w", "hot"),
    "news":     ("BBG news publication count vs trailing 4w",    "hot"),
    "tone":     ("BBG Twitter sentiment (daily avg, count-weighted)", "bull"),
    "tone_chg": ("BBG Twitter sentiment change vs trailing 4w",  "bull"),
    "news_tone":("BBG news sentiment (daily avg, count-weighted)", "bull"),
    "eps_rev":  ("EPS revision, BEST_EPS 1BF, 4w %",             "bull"),
    "rating":   ("Analyst rating drift, 4w",                     "bull"),
    "si":       ("Short interest % float (level)",               "crowd"),
}
HOT_KEYS = ["att", "news"]
BULL_KEYS = {"panel": ["tone", "tone_chg", "eps_rev", "rating", "ss_tone", "ss_pt"], "long": ["tone", "tone_chg", "news_tone", "eps_rev", "rating"]}

def shift(f, days): return (dt.date.fromisoformat(f) + dt.timedelta(days)).isoformat()

def bbg_components(s, f):
    """EPS revision (4w, roll-guarded), rating drift (4w), SI level — shared by both panels."""
    e0 = last_on_or_before(s.get("BEST_EPS", {}), f); em4 = last_on_or_before(s.get("BEST_EPS", {}), shift(f, -28))
    eps_rev = None
    if e0 is not None and em4 not in (None, 0) and abs(em4) > 0.05:
        eps_rev = (e0 - em4) / abs(em4)
        if abs(eps_rev) > 0.25: eps_rev = None      # fiscal-period roll or sign flip — not a revision
    r0 = last_on_or_before(s.get("BEST_ANALYST_RATING", {}), f); rm4 = last_on_or_before(s.get("BEST_ANALYST_RATING", {}), shift(f, -28))
    si = None
    for k in sorted(s.get("SI_PERCENT_EQUITY_FLOAT", {})):
        if k <= f: si = s["SI_PERCENT_EQUITY_FLOAT"][k]
    return {"eps_rev": eps_rev, "rating": (r0 - rm4) if (r0 is not None and rm4 is not None) else None, "si": si}

def add_returns(row, s, f, end):
    p0 = last_on_or_before(s["PX_LAST"], f); row["px"] = p0
    pm4 = last_on_or_before(s["PX_LAST"], shift(f, -28))
    row["ret_m4w"] = (p0 / pm4 - 1) if (p0 and pm4) else None
    for h, d in HORIZONS.items():
        ok = dt.date.fromisoformat(shift(f, d)) <= end - dt.timedelta(1)
        p1 = last_on_or_before(s["PX_LAST"], shift(f, d)) if ok else None
        row["ret_" + h] = (p1 / p0 - 1) if (p0 and p1) else None

def finish_week(row, tickers, comps, bull_keys):
    for k in comps:
        z = zscore({t: row[t].get(k) for t in tickers})
        for t in tickers: row[t]["z_" + k] = z[t]
    for h in HORIZONS:
        xs = [row[t]["ret_" + h] for t in tickers if row[t]["ret_" + h] is not None]
        mu = sum(xs) / len(xs) if xs else None
        for t in tickers: row[t]["rel_ret_" + h] = (row[t]["ret_" + h] - mu) if (row[t]["ret_" + h] is not None and mu is not None) else None
    for t in tickers:
        r = row[t]
        hot = [r["z_" + k] for k in HOT_KEYS if r.get("z_" + k) is not None]
        bull = [r["z_" + k] for k in bull_keys if r.get("z_" + k) is not None]
        r["HOT"] = sum(hot) / len(hot) if hot else None
        r["BULL"] = sum(bull) / len(bull) if bull else None

def backtest(panel, weeks, keys):
    """Rank IC per week for every component × horizon (universe-relative fwd return), overall and by calendar year."""
    bt = {}
    for k in keys:
        for h in HORIZONS:
            rk = "rel_ret_" + h; ics = []; spreads = []
            for f in weeks:
                row = panel[f]; sig = {t: row[t].get(k) for t in row}; fwd = {t: row[t].get(rk) for t in row}
                ic, n = spearman(sig, fwd)
                if ic is None: continue
                ics.append((f, ic, n))
                ks = sorted([t for t in sig if sig[t] is not None and fwd[t] is not None], key=lambda t: sig[t]); q = max(1, len(ks) // 5)
                spreads.append((f, sum(fwd[t] for t in ks[-q:]) / q - sum(fwd[t] for t in ks[:q]) / q))
            if not ics: continue
            def summ(ix):
                m = sum(x[1] for x in ix) / len(ix); sd = (sum((x[1] - m) ** 2 for x in ix) / max(1, len(ix) - 1)) ** 0.5
                return {"mean_ic": m, "t": (m / (sd / len(ix) ** 0.5)) if sd else None, "hit": sum(1 for x in ix if x[1] > 0) / len(ix), "weeks": len(ix), "avg_n": sum(x[2] for x in ix) / len(ix)}
            res = summ(ics); res["ics"] = ics; res["q5_q1"] = sum(s[1] for s in spreads) / len(spreads)
            res["by_year"] = {}
            for y in sorted({x[0][:4] for x in ics}):
                ix = [x for x in ics if x[0][:4] == y]; sp = [s[1] for s in spreads if s[0][:4] == y]
                if len(ix) >= 4: res["by_year"][y] = dict(summ(ix), q5_q1=sum(sp) / len(sp))
            bt[f"{k}|{rk}"] = res
    return bt

def quadrants(panel, weeks):
    quad = defaultdict(list)
    for f in weeks:
        row = panel[f]
        hs = sorted(r["HOT"] for r in row.values() if r["HOT"] is not None); bs = sorted(r["BULL"] for r in row.values() if r["BULL"] is not None)
        if len(hs) < 10 or len(bs) < 10: continue
        hm, bm = hs[len(hs) // 2], bs[len(bs) // 2]
        for t, r in row.items():
            if r["HOT"] is None or r["BULL"] is None: continue
            qn = ("hot" if r["HOT"] >= hm else "cold") + "-" + ("bull" if r["BULL"] >= bm else "bear")
            for h in HORIZONS:
                v = r.get("rel_ret_" + h)
                if v is not None: quad[f"{qn}|rel_ret_{h}"].append(v)
    return {k: {"mean": sum(v) / len(v), "n": len(v), "hit": sum(1 for x in v if x > 0) / len(v)} for k, v in quad.items()}

def print_bt(bt, keys):
    for k in keys:
        for h in HORIZONS:
            b = bt.get(f"{k}|rel_ret_{h}")
            if b: print(f"  {k:9s} {h:4s} IC {b['mean_ic']:+.3f} t {b['t'] if b['t'] is None else round(b['t'],2)} hit {b['hit']:.0%} q5-q1 {b['q5_q1']:+.2%} ({b['weeks']}w)"
                        + "".join(f"  {y}:{v['mean_ic']:+.3f}" for y, v in b.get("by_year", {}).items()))

# ----------------------------------------------------------------------------- step: panel (own tweet corpus, May-2026→)
def step_panel(universe):
    tw = json.load(open(DATA / "tweet_daily.json", encoding="utf-8"))
    bb = json.load(open(DATA / "bbg_history.json", encoding="utf-8"))["series"]
    ss = json.load(open(DATA / "sellside_daily.json", encoding="utf-8")) if (DATA / "sellside_daily.json").exists() else None
    tickers = [t for t in universe if t not in PRIVATE and t in bb and bb[t].get("PX_LAST")]
    end = TODAY; weeks = [f.isoformat() for f in fridays(START, end)]
    def wk_agg(t, f):
        days = tw["tickers"].get(t, {}); f0 = dt.date.fromisoformat(f)
        agg = {"m_cur": 0.0, "m_wire": 0.0, "tone_w": 0.0, "w": 0.0, "tone_n": 0, "bull": 0, "bear": 0}
        for i in range(7):
            r = days.get((f0 - dt.timedelta(i)).isoformat())
            if r:
                for k in agg: agg[k] += r.get(k, 0)
        return agg
    W = {t: {f: wk_agg(t, f) for f in weeks} for t in tickers}
    panel = {}
    for i, f in enumerate(weeks):
        row = {}
        for t in tickers:
            a = W[t][f]; prev = [W[t][weeks[j]] for j in range(max(0, i - 4), i)]
            def ratio(key):
                if len(prev) < 2: return None
                return math.log((a[key] + 0.5) / (sum(p[key] for p in prev) / len(prev) + 0.5))
            tone_now = (a["tone_w"] / a["w"]) * (a["tone_n"] / (a["tone_n"] + 5)) if a["w"] else 0.0
            tone_prev = None
            if len(prev) >= 2:
                pw = sum(p["w"] for p in prev); pn = sum(p["tone_n"] for p in prev)
                tone_prev = (sum(p["tone_w"] for p in prev) / pw) * (pn / (pn + 5)) if pw else 0.0
            r = {"att": ratio("m_cur"), "news": ratio("m_wire"), "tone": tone_now if (a["tone_n"] or len(prev) >= 2) else None,
                 "tone_chg": (tone_now - tone_prev) if tone_prev is not None else None,
                 "m_cur": round(a["m_cur"], 1), "m_wire": round(a["m_wire"], 1), "bull": a["bull"], "bear": a["bear"],
                 "ss_att": None, "ss_tone": None, "ss_act": None, "ss_n": None, "ss_pt": None, "ss_est": None}
            if ss and f >= (ss.get("since") or "9999"):
                w1 = ss_window(ss, t, shift(f, -6), f); w4 = ss_window(ss, t, shift(f, -34), shift(f, -7))
                r["ss_n"] = round(w1["n"], 1)
                r["ss_att"] = math.log((w1["n"] + 0.5) / (w4["n"] / 4 + 0.5)) if shift(f, -34) >= (ss.get("since") or "9999") else None
                r["ss_tone"] = (w1["tone_w"] / w1["tone_n"]) * (w1["tone_n"] / (w1["tone_n"] + 3)) if w1["tone_n"] else 0.0
                r["ss_act"] = w1["up"] - w1["down"]
                r["ss_pt"] = (w1["pt_sum"] / w1["pt_n"]) if w1["pt_n"] else 0.0
                r["ss_est"] = w1["est_up"] - w1["est_down"]
            r.update(bbg_components(bb[t], f)); add_returns(r, bb[t], f, end); row[t] = r
        finish_week(row, tickers, COMPONENTS, BULL_KEYS["panel"]); panel[f] = row
    keys = list(COMPONENTS) + ["HOT", "BULL"]
    bt = backtest(panel, weeks, keys); quad = quadrants(panel, weeks)
    out = {"asof": TODAY.isoformat(), "weeks": weeks, "tickers": tickers, "components": COMPONENTS, "horizons": HORIZONS, "panel": panel,
           "backtest": bt, "quadrants": quad, "names": {t: universe[t]["name"] for t in tickers},
           "top_handles": tw.get("top_handles", {}), "tweets_scanned": tw["tweets_scanned"], "tweets_matched": tw["tweets_matched"]}
    (DATA / "panel_weekly.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"panel: {len(weeks)} weeks × {len(tickers)} tickers"); print_bt(bt, keys)
    return out

# ----------------------------------------------------------------------------- long-track weekly panel (shared by step_long and step_leadlag)
def build_long_panel(universe):
    """Weekly (Friday) panel on Bloomberg social/news history, Jan-2024 → today. Returns (bb, tickers, weeks, panel)."""
    bb = json.load(open(DATA / "bbg_long.json", encoding="utf-8"))["series"]
    tickers = [t for t in universe if t not in PRIVATE and t in bb and bb[t].get("PX_LAST") and bb[t].get("TWITTER_PUBLICATION_COUNT")]
    end = TODAY; weeks = [f.isoformat() for f in fridays("2024-01-05", end)]
    def wk(t, f):
        s = bb[t]; f0 = dt.date.fromisoformat(f); agg = {"cnt": 0.0, "ncnt": 0.0, "sw": 0.0, "nsw": 0.0, "pos": 0.0, "neg": 0.0, "days": 0}
        for i in range(7):
            d = (f0 - dt.timedelta(i)).isoformat()
            c = s["TWITTER_PUBLICATION_COUNT"].get(d)
            if c is None: continue
            agg["days"] += 1; agg["cnt"] += c; agg["sw"] += c * s.get("TWITTER_SENTIMENT_DAILY_AVG", {}).get(d, 0.0)
            agg["pos"] += s.get("TWITTER_POS_SENTIMENT_COUNT", {}).get(d, 0.0); agg["neg"] += s.get("TWITTER_NEG_SENTIMENT_COUNT", {}).get(d, 0.0)
            nc = s.get("NEWS_PUBLICATION_COUNT", {}).get(d, 0.0); agg["ncnt"] += nc; agg["nsw"] += nc * s.get("NEWS_SENTIMENT_DAILY_AVG", {}).get(d, 0.0)
        return agg
    W = {t: {f: wk(t, f) for f in weeks} for t in tickers}
    panel = {}
    for i, f in enumerate(weeks):
        row = {}
        for t in tickers:
            a = W[t][f]; prev = [W[t][weeks[j]] for j in range(max(0, i - 4), i)]
            def ratio(key):
                if len(prev) < 2 or a["days"] == 0: return None
                return math.log((a[key] + 0.5) / (sum(p[key] for p in prev) / len(prev) + 0.5))
            tone = (a["sw"] / a["cnt"]) if a["cnt"] else None
            ntone = (a["nsw"] / a["ncnt"]) if a["ncnt"] else None
            pc = sum(p["cnt"] for p in prev); tone_prev = (sum(p["sw"] for p in prev) / pc) if (len(prev) >= 2 and pc) else None
            r = {"att": ratio("cnt"), "news": ratio("ncnt"), "tone": tone, "tone_chg": (tone - tone_prev) if (tone is not None and tone_prev is not None) else None,
                 "news_tone": ntone, "cnt": round(a["cnt"]), "ncnt": round(a["ncnt"]), "pos": round(a["pos"]), "neg": round(a["neg"])}
            r.update(bbg_components(bb[t], f)); add_returns(r, bb[t], f, end); row[t] = r
        finish_week(row, tickers, LONG_COMPONENTS, BULL_KEYS["long"]); panel[f] = row
    return bb, tickers, weeks, panel

# ----------------------------------------------------------------------------- step: leadlag (is sentiment leading, coincident or lagging?)
LAGS = list(range(-4, 5))

def partial_spearman(x, y, z):
    """Spearman corr(x, y) controlling for z, over the keys present in all three. Returns (r, n)."""
    ks = [k for k in x if x.get(k) is not None and y.get(k) is not None and z.get(k) is not None]
    if len(ks) < 10: return None, len(ks)
    sub = lambda d: {k: d[k] for k in ks}
    rxy, _ = spearman(sub(x), sub(y)); rxz, _ = spearman(sub(x), sub(z)); ryz, _ = spearman(sub(y), sub(z))
    if None in (rxy, rxz, ryz): return None, len(ks)
    den = ((1 - rxz ** 2) * (1 - ryz ** 2)) ** 0.5
    return ((rxy - rxz * ryz) / den if den > 1e-9 else None), len(ks)

def _ccf(panel, weeks, keys, lags, min_n=10):
    """Cross-correlation function. R[j] = universe-relative return DURING the week ending weeks[j]
    (= rel_ret_1w stamped on weeks[j-1]). IC_k = mean_i Spearman(S_i, R_{i+k}): k>0 leading, k=0 coincident, k<0 lagging.
    Weekly returns do not overlap, so the per-lag IC series is close to independent and the t-stat is honest."""
    R = {}
    for j in range(1, len(weeks)):
        R[j] = {t: r.get("rel_ret_1w") for t, r in panel[weeks[j - 1]].items()}
    out = {}
    for k in keys:
        out[k] = {}
        for lag in lags:
            ics = []
            for i in range(len(weeks)):
                j = i + lag
                if j < 1 or j >= len(weeks): continue
                sig = {t: r.get(k) for t, r in panel[weeks[i]].items()}
                ic, n = spearman(sig, R[j])
                if ic is not None and n >= min_n: ics.append(ic)
            if len(ics) >= 6:
                m = sum(ics) / len(ics); sd = (sum((x - m) ** 2 for x in ics) / (len(ics) - 1)) ** 0.5
                out[k][str(lag)] = {"ic": m, "t": (m / (sd / len(ics) ** 0.5)) if sd else None, "n": len(ics), "hit": sum(1 for x in ics if x > 0) / len(ics)}
    return out

def _partial_fwd(panel, weeks, keys, ctrl="ret_m4w", lags=(1, 2, 3, 4)):
    """Forward IC after controlling for the past-4-week return (momentum). If a signal only 'works' because it
    is a rewrap of recent price action, this goes to ~0."""
    R = {j: {t: r.get("rel_ret_1w") for t, r in panel[weeks[j - 1]].items()} for j in range(1, len(weeks))}
    out = {}
    for k in keys:
        out[k] = {}
        for lag in lags:
            raw, par = [], []
            for i in range(len(weeks)):
                j = i + lag
                if j < 1 or j >= len(weeks): continue
                row = panel[weeks[i]]; sig = {t: r.get(k) for t, r in row.items()}; z = {t: r.get(ctrl) for t, r in row.items()}
                ic, n = spearman(sig, R[j]); pic, pn = partial_spearman(sig, R[j], z)
                if ic is not None and pic is not None and pn >= 10: raw.append(ic); par.append(pic)
            if len(par) >= 6:
                mp = sum(par) / len(par); sd = (sum((x - mp) ** 2 for x in par) / (len(par) - 1)) ** 0.5
                out[k][str(lag)] = {"ic_raw": sum(raw) / len(raw), "ic_partial": mp, "t_partial": (mp / (sd / len(par) ** 0.5)) if sd else None, "n": len(par)}
    return out

def _double_sort(panel, weeks, key, ctrl="ret_m4w", fwd="rel_ret_15d"):
    """Tercile of past-4w return × tercile of the signal → mean forward 15d relative return. Reads whether the
    signal adds information INSIDE each momentum bucket (rows) rather than just proxying for it."""
    cells = defaultdict(list)
    for f in weeks:
        row = panel[f]
        ok = [t for t, r in row.items() if r.get(key) is not None and r.get(ctrl) is not None and r.get(fwd) is not None]
        if len(ok) < 15: continue
        cs = sorted(row[t][ctrl] for t in ok); ss = sorted(row[t][key] for t in ok)
        c1, c2 = cs[len(cs) // 3], cs[2 * len(cs) // 3]; s1, s2 = ss[len(ss) // 3], ss[2 * len(ss) // 3]
        for t in ok:
            ci = "mom_lo" if row[t][ctrl] < c1 else ("mom_hi" if row[t][ctrl] >= c2 else "mom_mid")
            si = "sig_lo" if row[t][key] < s1 else ("sig_hi" if row[t][key] >= s2 else "sig_mid")
            cells[f"{ci}|{si}"].append(row[t][fwd])
    return {k: {"mean": sum(v) / len(v), "n": len(v)} for k, v in cells.items()}

def _verdict(ccf_k, partial_k=None):
    """Label from the CCF shape (where does |IC| live?) plus the momentum-controlled forward test.
    A signal can be mostly lagging AND still carry a genuine leading residual (analyst revisions do) —
    that case is named explicitly instead of being flattened to 'lagging'."""
    g = lambda lag: (ccf_k.get(str(lag)) or {}).get("ic")
    lead = [g(l) for l in (1, 2) if g(l) is not None]; lagg = [g(l) for l in (-1, -2) if g(l) is not None]; coin = g(0)
    ml = sum(lead) / len(lead) if lead else 0.0; mg = sum(lagg) / len(lagg) if lagg else 0.0; mc = coin or 0.0
    tl = (ccf_k.get("1") or {}).get("t") or 0.0
    pp = ((partial_k or {}).get("1") or {}); pt = pp.get("t_partial") or 0.0; pi = pp.get("ic_partial") or 0.0
    residual = abs(pt) >= 2.0 and abs(pi) >= 0.02          # forward IC survives the past-return control
    if abs(ml) >= 0.02 and abs(tl) >= 2.0 and abs(ml) >= 0.6 * max(abs(mc), abs(mg)):
        return "leading" + (" (contrarian)" if ml < 0 else "") + ("" if residual else " — but not ex-momentum")
    if abs(mg) > abs(ml) and abs(mg) > 0.5 * abs(mc) and abs(mg) >= 0.03:
        return "lagging (follows price)" + (" + leading residual ex-momentum" if residual else "")
    if abs(mc) >= 0.03 and abs(mc) > 1.5 * abs(ml):
        return "coincident" + (" + leading residual ex-momentum" if residual else "")
    return "weak / no structure" + (" (level signal — see double sort)" if residual else "")

def step_leadlag(universe):
    bb, tickers, weeks, panel = build_long_panel(universe)
    own = json.load(open(DATA / "panel_weekly.json", encoding="utf-8"))
    L_KEYS = ["att", "news", "tone", "tone_chg", "news_tone", "eps_rev", "rating", "si", "HOT", "BULL"]
    O_KEYS = ["att", "news", "tone", "tone_chg", "eps_rev", "rating", "si", "ss_att", "ss_tone", "ss_act", "ss_pt", "HOT", "BULL"]
    long_ccf = _ccf(panel, weeks, L_KEYS, LAGS)
    long_par = _partial_fwd(panel, weeks, L_KEYS)
    own_ccf = _ccf(own["panel"], own["weeks"], O_KEYS, list(range(-3, 4)), min_n=10)
    own_par = _partial_fwd(own["panel"], own["weeks"], O_KEYS, lags=(1, 2))
    # by-year CCF for the two headline signals (regime check)
    by_year = {}
    for y in sorted({w[:4] for w in weeks}):
        wy = [w for w in weeks if w[:4] == y]
        if len(wy) < 20: continue
        sub = {w: panel[w] for w in wy}
        by_year[y] = _ccf(sub, wy, ["tone", "att", "eps_rev", "si", "BULL"], LAGS)
    ds = {k: _double_sort(panel, weeks, k) for k in ("tone", "att", "eps_rev", "si")}
    # reverse direction, explicit: does THIS week's return predict NEXT week's signal? (Spearman of R_i on S_{i+1})
    reverse = {}
    R = {j: {t: r.get("rel_ret_1w") for t, r in panel[weeks[j - 1]].items()} for j in range(1, len(weeks))}
    for k in ("tone", "att", "news", "eps_rev", "rating"):
        ics = []
        for j in range(1, len(weeks) - 1):
            ic, n = spearman(R[j], {t: r.get(k) for t, r in panel[weeks[j]].items()})   # return during week j vs signal stamped at end of week j → contemporaneous
            ic2, n2 = spearman(R[j], {t: r.get(k) for t, r in panel[weeks[j + 1]].items()})  # return during week j vs signal one week LATER
            if ic2 is not None: ics.append(ic2)
        if len(ics) >= 6:
            m = sum(ics) / len(ics); sd = (sum((x - m) ** 2 for x in ics) / (len(ics) - 1)) ** 0.5
            reverse[k] = {"ic": m, "t": (m / (sd / len(ics) ** 0.5)) if sd else None, "n": len(ics)}
    verdicts = {k: _verdict(long_ccf[k], long_par.get(k)) for k in L_KEYS}
    out = {"asof": TODAY.isoformat(), "lags": LAGS, "weeks": len(weeks), "span": [weeks[0], weeks[-1]],
           "labels": {**{k: v[0] for k, v in LONG_COMPONENTS.items()}, "HOT": "HOT composite", "BULL": "BULL composite"},
           "own_labels": {**{k: v[0] for k, v in COMPONENTS.items()}, "HOT": "HOT composite", "BULL": "BULL composite"},
           "long": {"ccf": long_ccf, "partial": long_par, "verdict": verdicts, "by_year": by_year, "double_sort": ds, "reverse": reverse},
           "own": {"ccf": own_ccf, "partial": own_par, "weeks": len(own["weeks"]), "span": [own["weeks"][0], own["weeks"][-1]]}}
    (DATA / "leadlag.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"leadlag: {len(weeks)} weeks × {len(tickers)} tickers ({weeks[0]} → {weeks[-1]})")
    print("  signal      " + "".join(f"{('k%+d' % l):>8s}" for l in LAGS) + "   partial+1  verdict")
    for k in L_KEYS:
        c = long_ccf[k]; p = (long_par[k].get("1") or {})
        print(f"  {k:10s}  " + "".join(f"{(c.get(str(l)) or {}).get('ic', float('nan')):+8.3f}" for l in LAGS)
              + f"   {p.get('ic_partial', float('nan')):+.3f} (t {p.get('t_partial') or 0:+.1f})  {verdicts[k]}")
    print("  reverse (this week's return → next week's signal):", {k: round(v["ic"], 3) for k, v in reverse.items()})
    return out

# ----------------------------------------------------------------------------- step: picks (what we would have seen each week, and what happened next)
PICK_N = 10   # stored per side; the page derives top-3 / top-5 / top-10 from these

def _picks(panel, weeks, keys, names, n=PICK_N):
    """For every week and signal: the n highest and n lowest names on the signal, with the stock's
    universe-relative return over the FOLLOWING week (and 15 days). Only weeks whose following week has
    already happened are kept. Returns {signal: [{w, top:[...], bot:[...]}]} — statistics are computed
    on the page so the reader can switch N."""
    out = {}
    for k in keys:
        rows = []
        for f in weeks:
            row = panel[f]
            cands = [(t, r[k]) for t, r in row.items() if r.get(k) is not None and r.get("rel_ret_1w") is not None]
            if len(cands) < 2 * n + 5: continue
            cands.sort(key=lambda x: -x[1])
            pack = lambda lst: [{"t": t, "v": round(v, 3), "r1": round(row[t]["rel_ret_1w"], 4),
                                 "r15": (round(row[t]["rel_ret_15d"], 4) if row[t].get("rel_ret_15d") is not None else None),
                                 "raw1": (round(row[t]["ret_1w"], 4) if row[t].get("ret_1w") is not None else None)} for t, v in lst]
            rows.append({"w": f, "top": pack(cands[:n]), "bot": pack(cands[-n:][::-1])})   # bot ordered most-extreme first
        if rows: out[k] = rows
    return out

def step_picks(universe):
    bb, tickers, weeks, panel = build_long_panel(universe)
    own = json.load(open(DATA / "panel_weekly.json", encoding="utf-8"))
    L_KEYS = ["att", "news", "tone", "tone_chg", "news_tone", "eps_rev", "rating", "si", "HOT", "BULL"]
    O_KEYS = ["att", "news", "tone", "tone_chg", "eps_rev", "rating", "si", "ss_att", "ss_tone", "ss_act", "ss_pt", "HOT", "BULL"]
    names = {t: universe[t]["name"] for t in universe}
    out = {"asof": TODAY.isoformat(), "n_stored": PICK_N,
           "long": {"span": [weeks[0], weeks[-1]], "picks": _picks(panel, weeks, L_KEYS, names),
                    "labels": {**{k: v[0] for k, v in LONG_COMPONENTS.items()}, "HOT": "HOT composite", "BULL": "BULL composite"}},
           "own": {"span": [own["weeks"][0], own["weeks"][-1]], "picks": _picks(own["panel"], own["weeks"], O_KEYS, names),
                   "labels": {**{k: v[0] for k, v in COMPONENTS.items()}, "HOT": "HOT composite", "BULL": "BULL composite"}},
           "names": names}
    (DATA / "picks.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    # console summary at N=5, next-week relative return
    def summ(pk, n=5):
        for k, rows in pk.items():
            mt = [sum(x["r1"] for x in r["top"][:n]) / n for r in rows]; mb = [sum(x["r1"] for x in r["bot"][:n]) / n for r in rows]
            sp = [a - b for a, b in zip(mt, mb)]
            print(f"  {k:9s} weeks {len(rows):3d} · top{n} next-wk {sum(mt)/len(mt)*100:+.2f}% · bottom{n} {sum(mb)/len(mb)*100:+.2f}% · spread {sum(sp)/len(sp)*100:+.2f}% · spread>0 in {sum(1 for s in sp if s>0)/len(sp):.0%} of weeks")
    print(f"picks: long track {len(out['long']['picks'])} signals × {len(weeks)} weeks; own {len(out['own']['picks'])} signals × {len(own['weeks'])} weeks")
    print(" Bloomberg track:"); summ(out["long"]["picks"])
    print(" Own corpus:"); summ(out["own"]["picks"])
    return out

# ----------------------------------------------------------------------------- step: long (Bloomberg social/news, Dec-2023→)
def step_long(universe):
    bb, tickers, weeks, panel = build_long_panel(universe)
    keys = list(LONG_COMPONENTS) + ["HOT", "BULL"]
    bt = backtest(panel, weeks, keys); quad = quadrants(panel, weeks)
    # keep the embedded payload small: latest week full, earlier weeks only the composite + returns
    slim = {f: {t: {k: r.get(k) for k in ("HOT", "BULL", "att", "tone", "cnt", "ret_1w", "ret_15d", "ret_4w", "rel_ret_15d", "px")} for t, r in row.items()} for f, row in panel.items()}
    slim[weeks[-1]] = panel[weeks[-1]]
    out = {"asof": TODAY.isoformat(), "weeks": weeks, "tickers": tickers, "components": LONG_COMPONENTS, "horizons": HORIZONS,
           "panel": slim, "backtest": bt, "quadrants": quad, "names": {t: universe[t]["name"] for t in tickers}}
    (DATA / "panel_long.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"long: {len(weeks)} weeks × {len(tickers)} tickers ({weeks[0]} → {weeks[-1]})"); print_bt(bt, keys)
    return out

# ----------------------------------------------------------------------------- step: sellside (Outlook broker e-mails, subject-level)
FIRMS = {"jefferies": "Jefferies", "morganstanley": "Morgan Stanley", "jpmorgan": "JPMorgan", "jpmresearchmail": "JPMorgan", "jpmchase": "JPMorgan",
         "ubs": "UBS", "bofa": "BofA", "bankofamerica": "BofA", "ml.com": "BofA", "barclays": "Barclays", "gs.com": "Goldman Sachs", "bernstein": "Bernstein",
         "citi": "Citi", "db.com": "Deutsche Bank", "sig.com": "SIG", "susquehanna": "SIG", "rothschildandco": "Redburn", "redburn": "Redburn", "wolferesearch": "Wolfe",
         "evercore": "Evercore", "needham": "Needham", "raymondjames": "Raymond James", "stifel": "Stifel", "mizuho": "Mizuho", "tdcowen": "TD Cowen", "cowen": "TD Cowen",
         "wellsfargo": "Wells Fargo", "bmo": "BMO", "rbccm": "RBC", "baird": "Baird", "piper": "Piper Sandler", "oppenheimer": "Oppenheimer", "kbw": "KBW", "loopcapital": "Loop",
         "rosenblatt": "Rosenblatt", "newstreetresearch": "New Street", "arete": "Arete", "melius": "Melius", "moffettnathanson": "MoffettNathanson", "btig": "BTIG",
         "craig-hallum": "Craig-Hallum", "benchmark": "Benchmark", "cantor": "Cantor", "hsbc": "HSBC", "bnpparibas": "BNP Paribas", "macquarie": "Macquarie", "nomura": "Nomura",
         "daiwa": "Daiwa", "clsa": "CLSA", "guggenheim": "Guggenheim", "truist": "Truist", "keybanc": "KeyBanc", "wedbush": "Wedbush", "northlandcapital": "Northland",
         "kepler": "Kepler", "berenberg": "Berenberg", "santander": "Santander", "itau": "Itaú", "btgpactual": "BTG", "xpi": "XP", "bradesco": "Bradesco"}
SS_NOISE = re.compile(r"webinar|invitation|invite|dial-in|conference call details|unsubscribe|out of office|calendar|corporate access|roadshow|marketing|save the date|registration|survey|holiday", re.I)
SS_UP = re.compile(r"\bupgrad|rais\w* (?:our |the )?(?:PT|price target|target|estimates|ests|EPS)|(?:PT|price target|target)\w* (?:raised|up|to \$?\d+ from)|\bto (?:Buy|Overweight|Outperform|OW)\b|top pick|adding to (?:conviction|focus) list|beat|above|positive", re.I)
SS_DOWN = re.compile(r"\bdowngrad|(?:cut|lower|reduc|trim)\w* (?:our |the )?(?:PT|price target|target|estimates|ests|EPS)|(?:PT|price target|target)\w* (?:cut|lowered|down)|\bto (?:Sell|Underweight|Underperform|UW|Reduce)\b|remov\w* from (?:conviction|focus) list|miss|below|negative|concern", re.I)
SHORT_TICKERS = {t for t in ALIASES if len(t) <= 3} | {"APP", "NOW", "NET", "ARM", "TEL", "MP", "BE", "TM", "ON"}

def ss_firm(addr):
    a = (addr or "").lower()
    for k, v in FIRMS.items():
        if k in a: return v
    return a.split("@")[-1] if "@" in a else a

def build_subject_matchers(universe):
    cash, pats = build_matchers(universe)
    tk = []
    for t in universe:
        if t in PRIVATE or t not in ALIASES: continue
        if t in SHORT_TICKERS or len(t) <= 3:
            tk.append((t, re.compile(r"(?:\(" + re.escape(t) + r"\)|\$" + re.escape(t) + r"\b|\b" + re.escape(t) + r"(?:\.[A-Z]{1,2}\b| US\b| Equity\b))")))
        else:
            tk.append((t, re.compile(r"\b" + re.escape(t) + r"\b")))
    return cash, pats, tk

def step_sellside(universe):
    raw_p = DATA / "sellside_mail_raw.json"
    if not raw_p.exists(): print("sellside: no raw sweep file — run _wiki/_tools/sellside_mail_sweep.ps1 first"); return None
    txt = raw_p.read_text(encoding="utf-8-sig"); rows = json.loads(txt) if txt.strip() else []
    if isinstance(rows, dict): rows = [rows]
    if (DATA / "sellside_mail_bodies.jsonl").exists(): return step_sellside_bodies(universe, rows)
    cash, pats, tk = build_subject_matchers(universe)
    daily = defaultdict(lambda: defaultdict(lambda: {"n": 0.0, "tone_w": 0.0, "tone_n": 0, "up": 0.0, "down": 0.0, "firms": set(), "subj": []}))
    n_all = n_noise = n_hit = 0; firm_ct = defaultdict(int)
    for r in rows:
        subj = r.get("subject") or ""; d = r.get("d"); n_all += 1
        if not d or SS_NOISE.search(subj): n_noise += 1; continue
        found = set()
        for m in cash.finditer(subj):
            t = m.group(1).upper()
            if t in universe and t not in PRIVATE: found.add(t)
        for t, rx in pats:
            if t not in found and rx.search(subj): found.add(t)
        for t, rx in tk:
            if t not in found and rx.search(subj): found.add(t)
        if not found: continue
        n_hit += 1; firm = ss_firm(r.get("from")); firm_ct[firm] += 1
        sc, nh = tone(subj); up = 1 if SS_UP.search(subj) else 0; dn = 1 if SS_DOWN.search(subj) else 0
        w = 1.0 / len(found) if len(found) <= 3 else 0.25 / len(found)
        for t in found:
            a = daily[t][d]; a["n"] += w; a["up"] += w * up; a["down"] += w * dn; a["firms"].add(firm)
            if nh: a["tone_w"] += w * sc; a["tone_n"] += 1
            if len(a["subj"]) < 3 and len(found) <= 2: a["subj"].append({"f": firm, "s": subj[:140]})
    out = {"asof": TODAY.isoformat(), "since": min((r.get("d") for r in rows if r.get("d")), default=None), "emails": n_all, "noise_dropped": n_noise, "matched": n_hit,
           "firms": sorted(firm_ct.items(), key=lambda x: -x[1])[:30],
           "tickers": {t: {d: {"n": round(a["n"], 3), "tone_w": round(a["tone_w"], 4), "tone_n": a["tone_n"], "up": round(a["up"], 3), "down": round(a["down"], 3),
                               "firms": len(a["firms"]), "subj": a["subj"]} for d, a in sorted(days.items())} for t, days in daily.items()}}
    (DATA / "sellside_daily.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"sellside: {n_all:,} broker e-mails since {out['since']} · noise dropped {n_noise:,} · {n_hit:,} mapped to {len(daily)} tickers · top firms {out['firms'][:6]}")
    return out

def ss_window(ss, t, d0, d1):
    """Aggregate sell-side daily rows for ticker t over [d0, d1] inclusive (ISO strings)."""
    days = ss.get("tickers", {}).get(t, {}) if ss else {}
    agg = {"n": 0.0, "tone_w": 0.0, "tone_n": 0, "up": 0.0, "down": 0.0, "pt_up": 0.0, "pt_down": 0.0, "pt_sum": 0.0, "pt_n": 0.0, "est_up": 0.0, "est_down": 0.0}
    for d, a in days.items():
        if d0 <= d <= d1:
            for k in agg: agg[k] += a.get(k, 0)
    return agg

# ----------------------------------------------------------------------------- sell-side BODY parsing (used when sellside_mail_bodies.jsonl exists)
URL_RE = re.compile(r"<?https?://\S+>?|<mailto:[^>]+>", re.I)
DISCLAIM_RE = re.compile(r"IMPORTANT DISCLOSURES?|Analyst Certification|Disclosure Appendix|Disclosures for any|This message is subject|This e-?mail (?:and any|is intended|may contain)|"
                         r"confidential(?:ity)? (?:notice|and may)|Mistransmission|unsubscribe|Please vote|Extel|Institutional Investor survey|This report (?:is|was) (?:prepared|issued)|"
                         r"Reg AC|Regulation Analyst|MiFID|The information (?:herein|contained)|Past performance|©|Copyright", re.I)
RATING_POS = r"(?:Positive|Buy|Overweight|Outperform|OW|Add|Conviction Buy|Strong Buy|Accumulate)"
RATING_NEU = r"(?:Neutral|Hold|Equal-?weight|EW|Market Perform|Sector Perform|In-?Line|Peer Perform|Perform)"
RATING_NEG = r"(?:Negative|Sell|Underweight|UW|Underperform|Reduce)"
RATING_ANY = f"(?:{RATING_POS}|{RATING_NEU}|{RATING_NEG})"
RX_RATING_FROMTO = re.compile(r"Rating:?\s*(?:From|from)\s+(" + RATING_ANY + r")\s+(?:to|→)\s+(" + RATING_ANY + r")", re.I)
RX_UPGRADE_TO = re.compile(r"\b(upgrad\w*|downgrad\w*)\s+(?:\w+\s+){0,4}?to\s+(" + RATING_ANY + r")\b", re.I)
RX_UPDOWN = re.compile(r"\b(upgrad\w*|downgrad\w*|U/G|D/G)\b", re.I)
RX_PT_FROMTO = re.compile(r"(?:Price target|Target price|PT|TP|price objective|PO)\s*:?\s*(?:From|from)\s*(?:US)?\$?\s*([\d,]+(?:\.\d+)?)\s*(?:to|→)\s*(?:US)?\$?\s*([\d,]+(?:\.\d+)?)", re.I)
RX_PT_TOFROM = re.compile(r"(?:PT|TP|price target|target price|price objective|PO)\s*(?:to|of|at|→)\s*(?:US)?\$?\s*([\d,]+(?:\.\d+)?)\s*(?:\(?from\s*(?:US)?\$?\s*([\d,]+(?:\.\d+)?)\)?)", re.I)
RX_PT_RAISE = re.compile(r"\b(rais\w*|lift\w*|increas\w*|hik\w*|boost\w*|cut\w*|lower\w*|reduc\w*|trim\w*|slash\w*)\s+(?:our\s+|the\s+)?(?:\w+\s+){0,2}?(?:PT|TP|price target|target price|price objective)\b", re.I)
RX_EST = re.compile(r"\b(rais\w*|increas\w*|lift\w*|cut\w*|lower\w*|reduc\w*|trim\w*)\s+(?:our\s+|the\s+)?(?:\w+\s+){0,3}?(?:estimates?|ests?|EPS|forecasts?|numbers)\b", re.I)
UPW = ("rais", "lift", "increas", "hik", "boost"); DNW = ("cut", "lower", "reduc", "trim", "slash")

def rating_rank(r):
    r = r.lower()
    if re.fullmatch(RATING_POS.lower().replace("(?:", "(").replace("-?", "-?"), r) or r in ("positive", "buy", "overweight", "outperform", "ow", "add", "conviction buy", "strong buy", "accumulate"): return 1
    if r in ("negative", "sell", "underweight", "uw", "underperform", "reduce"): return -1
    return 0

def clean_body(b):
    b = URL_RE.sub(" ", b or "")
    m = None
    for mm in DISCLAIM_RE.finditer(b):
        if mm.start() > 400: m = mm; break
    if m: b = b[:m.start()]
    b = re.sub(r"[ \t\u00a0\r]+", " ", b)
    b = re.sub(r"\s*\n\s*", "\n", b)
    return b.strip()

SEG_RE = re.compile(r"\n|\s\|\s|\s[•▪■►·]\s|(?<=[a-z\)])\.\s+(?=[A-Z])")
def mention_windows(text, rxs, maxw=6):
    """Text windows for a ticker: the segment (line / bullet / sentence) holding each mention, plus the next one when short.
    Falls back to ±250 chars when the text has no structure."""
    segs = []; pos = 0
    for m in SEG_RE.finditer(text):
        segs.append((pos, m.start())); pos = m.end()
    segs.append((pos, len(text)))
    out = []
    for rx in rxs:
        for m in rx.finditer(text):
            i = next((k for k, (a, b) in enumerate(segs) if a <= m.start() < b), None)
            if i is None or (segs[i][1] - segs[i][0]) > 1200:
                out.append(text[max(0, m.start() - 250):m.end() + 250])
            else:
                a, b = segs[i]
                if b - a < 80 and i + 1 < len(segs): b = segs[i + 1][1]
                out.append(text[a:b])
            if len(out) >= maxw: return out
    return out

def body_actions(text):
    """Rating / PT / estimate actions inside a text window. Returns dict up, down, pt_chg (fraction or None), est (+1/-1/0)."""
    up = dn = 0; pt_chg = None; est = 0
    for m in RX_RATING_FROMTO.finditer(text):
        a, b = rating_rank(m.group(1)), rating_rank(m.group(2))
        if b > a: up += 1
        elif b < a: dn += 1
    if up == 0 and dn == 0:
        for m in RX_UPGRADE_TO.finditer(text):
            if m.group(1).lower().startswith("up"): up += 1
            else: dn += 1
        if up == 0 and dn == 0:
            for m in RX_UPDOWN.finditer(text):
                w = m.group(1).lower()
                if w.startswith("up") or w == "u/g": up += 1
                else: dn += 1
    def f(x):
        try: return float(x.replace(",", ""))
        except Exception: return None
    for m in RX_PT_FROMTO.finditer(text):
        a, b = f(m.group(1)), f(m.group(2))
        if a and b and a > 0 and 0.2 < b / a < 5: pt_chg = b / a - 1; break
    if pt_chg is None:
        for m in RX_PT_TOFROM.finditer(text):
            b, a = f(m.group(1)), f(m.group(2))
            if a and b and a > 0 and 0.2 < b / a < 5: pt_chg = b / a - 1; break
    if pt_chg is None:
        m = RX_PT_RAISE.search(text)
        if m:
            w = m.group(1).lower(); pt_chg = 0.05 if w.startswith(UPW) else (-0.05 if w.startswith(DNW) else None)   # direction only, nominal 5%
    m = RX_EST.search(text)
    if m:
        w = m.group(1).lower(); est = 1 if w.startswith(UPW) else (-1 if w.startswith(DNW) else 0)
    return {"up": min(up, 1), "down": min(dn, 1), "pt_chg": pt_chg, "est": est}

def step_sellside_bodies(universe, rows):
    """Body-level sell-side parsing with a per-e-mail cache (sellside_parsed_cache.json) so nightly reruns only
    parse new mail. Bodies are loaded lazily for exactly the e-mails the cache has not parsed yet."""
    cash, pats, tk = build_subject_matchers(universe)
    body_tk = []
    for t in universe:
        if t in PRIVATE or t not in ALIASES: continue
        body_tk.append((t, re.compile(r"(?:\(" + re.escape(t) + r"(?:\.[A-Z]{1,2})?\)|\$" + re.escape(t) + r"\b|Symbol:\s*" + re.escape(t) + r"\b|\b" + re.escape(t) + r"(?:\.[A-Z]{1,2}\b| US\b| US Equity\b))")))
    key2t = defaultdict(set)
    for t, names in ALIASES.items():
        if t in universe and t not in PRIVATE:
            key2t[t.lower()].add(t)
            for n in names: key2t[n.lower()].add(t)
    PREF = re.compile("|".join(re.escape(k) for k in sorted(key2t, key=len, reverse=True)), re.I)
    pats_by_t = defaultdict(list)
    for t, rx in pats: pats_by_t[t].append(rx)
    for t, rx in body_tk: pats_by_t[t].append(rx)
    def candidates(txt):
        c = set()
        for m in PREF.finditer(txt): c |= key2t.get(m.group(0).lower(), set())
        return c
    cache_p = DATA / "sellside_parsed_cache.json"
    cache = json.load(open(cache_p, encoding="utf-8")) if cache_p.exists() else {}
    PARSER_VERSION = 4
    if cache.get("_v") != PARSER_VERSION: cache = {"_v": PARSER_VERSION}
    # which e-mails still need their body read? (unseen, or cached from the subject before the body arrived)
    need = set()
    for r in rows:
        rid = r.get("id")
        if not rid or not r.get("d"): continue
        rec = cache.get(rid)
        if rec is None or rec == 0 or not (isinstance(rec, dict) and rec.get("hb")): need.add(rid)
    bodies = load_bodies(need) or {}
    print(f"  bodies: {len(need):,} e-mails to (re)parse, {len(bodies):,} bodies on disk for them")

    def parse_email(r, body):
        """→ None (noise / no ticker) or {"S": [...], "per": {t: [w, sc, nh, up, down, pt_chg, est]}, "firm": str, "hb": bool}"""
        subj = r.get("subject") or ""
        text = clean_body(body) if body else ""
        head = text[:600]
        if SS_NOISE.search(subj) or (text and SS_NOISE.search(head) and not re.search(r"rating|price target|estimates|initiat", text[:3000], re.I)):
            return {"noise": True, "hb": bool(text)}
        S = set()
        for m in cash.finditer(subj):
            t = m.group(1).upper()
            if t in universe and t not in PRIVATE: S.add(t)
        for t, rx in pats:
            if t not in S and rx.search(subj): S.add(t)
        for t, rx in tk:
            if t not in S and rx.search(subj): S.add(t)
        B = set()
        if text:
            scan = text[:6000]
            for m in cash.finditer(scan):
                t = m.group(1).upper()
                if t in universe and t not in PRIVATE: B.add(t)
            explicit = {m.group(1).upper() for m in cash.finditer(scan)} | {t for t, rx in body_tk if rx.search(scan)}
            for t in candidates(scan):
                if t in B or t in S: continue
                n_ment = sum(1 for rx in pats_by_t[t] for _ in rx.finditer(scan))
                if t in explicit or n_ment >= 2: B.add(t)      # a single passing name-drop is not coverage
        found = S | B
        if not found: return None
        body_only = B - S
        if S:
            wS = 1.0 / len(S) if len(S) <= 3 else 0.25 / len(S); wB = (0.25 / len(body_only)) if body_only else 0.0
        else:
            wS = 0.0; wB = (0.5 / len(B)) if len(B) <= 3 else (0.25 / len(B))
        single = len(found) == 1
        doc_tone, doc_hits = (tone(text[:3000]) if text else tone(subj)) if single else (0.0, 0)
        doc_act = (body_actions(text[:4000]) if text else body_actions(subj)) if single else None
        per = {}
        for t in found:
            w = wS if t in S else wB
            win = "\n".join(mention_windows(text[:8000], pats_by_t[t])) if text else ""
            if single:
                sc, nh = (tone(win) if win else (doc_tone, doc_hits))
                if not nh and doc_hits: sc, nh = doc_tone, doc_hits
                act = doc_act
            else:
                sc, nh = tone(win) if win else (0.0, 0)
                act = body_actions(win) if win else {"up": 0, "down": 0, "pt_chg": None, "est": 0}
            per[t] = [round(w, 4), round(sc, 3), nh, act["up"], act["down"], act["pt_chg"], act["est"]]
        return {"S": sorted(S), "per": per, "firm": ss_firm(r.get("from")), "hb": bool(text)}

    daily = defaultdict(lambda: defaultdict(lambda: {"n": 0.0, "tone_w": 0.0, "tone_n": 0, "up": 0.0, "down": 0.0, "pt_up": 0.0, "pt_down": 0.0, "pt_sum": 0.0, "pt_n": 0.0,
                                                     "est_up": 0.0, "est_down": 0.0, "firms": set(), "subj": []}))
    n_all = n_noise = n_hit = n_body_only = n_bodies = n_new = 0; firm_ct = defaultdict(int)
    for r in rows:
        d = r.get("d"); rid = r.get("id"); n_all += 1
        if not d or not rid: continue
        body = bodies.get(rid)
        rec = cache.get(rid)
        if rec == 0: rec = {"none": True, "hb": False}          # legacy cache value
        if rec is None or (body and not rec.get("hb")):
            rec = parse_email(r, body); n_new += 1
            if rec is None: rec = {"none": True, "hb": bool(body)}
            cache[rid] = rec
        if rec.get("none"): continue
        if rec.get("noise"): n_noise += 1; continue
        if rec.get("hb"): n_bodies += 1
        n_hit += 1
        if not rec["S"]: n_body_only += 1
        firm = rec["firm"]; firm_ct[firm] += 1
        subj = r.get("subject") or ""
        for t, (w, sc, nh, up, dn, pt, est) in rec["per"].items():
            a = daily[t][d]
            a["n"] += w; a["firms"].add(firm)
            if nh: a["tone_w"] += w * sc; a["tone_n"] += 1
            a["up"] += w * up; a["down"] += w * dn
            if pt is not None:
                a["pt_sum"] += w * pt; a["pt_n"] += w
                if pt > 0: a["pt_up"] += w
                elif pt < 0: a["pt_down"] += w
            if est > 0: a["est_up"] += w
            elif est < 0: a["est_down"] += w
            if len(a["subj"]) < 3 and (t in rec["S"]) and len(rec["S"]) <= 2:
                tag = ("↑rating " if up else "") + ("↓rating " if dn else "") + (f"PT {pt*100:+.0f}% " if pt is not None else "") + (f"est {'+' if est>0 else '-'} " if est else "")
                a["subj"].append({"f": firm, "s": subj[:140], "a": tag.strip(), "tone": sc})
    cache_p.write_text(json.dumps(cache), encoding="utf-8")
    out = {"asof": TODAY.isoformat(), "mode": "body", "since": min((r.get("d") for r in rows if r.get("d")), default=None), "emails": n_all, "bodies": n_bodies,
           "noise_dropped": n_noise, "matched": n_hit, "body_only_matched": n_body_only, "parsed_new": n_new,
           "firms": sorted(firm_ct.items(), key=lambda x: -x[1])[:30],
           "tickers": {t: {d: {"n": round(a["n"], 3), "tone_w": round(a["tone_w"], 4), "tone_n": a["tone_n"], "up": round(a["up"], 3), "down": round(a["down"], 3),
                               "pt_up": round(a["pt_up"], 3), "pt_down": round(a["pt_down"], 3), "pt_sum": round(a["pt_sum"], 4), "pt_n": round(a["pt_n"], 3),
                               "est_up": round(a["est_up"], 3), "est_down": round(a["est_down"], 3), "firms": len(a["firms"]), "subj": a["subj"]}
                           for d, a in sorted(days.items())} for t, days in daily.items()}}
    (DATA / "sellside_daily.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"sellside(body): {n_all:,} e-mails · {n_bodies:,} matched with body · noise dropped {n_noise:,} · {n_hit:,} mapped to {len(daily)} tickers ({n_body_only:,} via body only) · parsed {n_new:,} new · top firms {out['firms'][:5]}")
    return out

def load_bodies(needed=None):
    """Bodies from the JSONL. `needed` = the id set still to parse; None loads everything (full re-parse).
    The ~400 MB file is streamed and ids are matched before json.loads, so a nightly run costs one
    sequential read instead of decoding 53k JSON objects."""
    p = DATA / "sellside_mail_bodies.jsonl"
    if not p.exists(): return None
    if needed is not None and not needed: return {}
    out = {}
    for line in open(p, encoding="utf-8"):
        if needed is not None:
            i = line.find('"id":"')
            if i < 0: continue
            j = line.find('"', i + 6)
            if j < 0 or line[i + 6:j] not in needed: continue
        try: o = json.loads(line)
        except Exception: continue
        if o.get("id"): out[o["id"]] = o.get("body") or ""
    return out

def step_mail_merge():
    """Fold sellside_mail_delta.json (the nightly -Days sweep) into sellside_mail_raw.json.
    Dedupe key = received minute + subject, matching the sweep's own within-run key, so the same note
    sitting in two folders counts once. Rows already present keep their original EntryID (and therefore
    their fetched body). Delta file is left in place; the next sweep overwrites it."""
    raw_p = DATA / "sellside_mail_raw.json"; delta_p = DATA / "sellside_mail_delta.json"
    if not delta_p.exists(): print("mail_merge: no delta file — nothing to merge"); return None
    def read(p):
        if not p.exists(): return []
        txt = p.read_text(encoding="utf-8-sig")
        if not txt.strip(): return []
        rows = json.loads(txt)
        return [rows] if isinstance(rows, dict) else rows
    raw = read(raw_p); delta = read(delta_p)
    key = lambda r: (r.get("d", ""), r.get("t", ""), r.get("subject", ""))
    have = {key(r) for r in raw}
    added = [r for r in delta if r.get("d") and r.get("subject") and key(r) not in have and not have.add(key(r))]
    if not added:
        print(f"mail_merge: {len(delta):,} in delta, 0 new (raw stays at {len(raw):,})"); return {"added": 0, "total": len(raw)}
    raw.extend(added)
    raw.sort(key=lambda r: (r.get("d", ""), r.get("t", "")))
    tmp = raw_p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(raw, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    tmp.replace(raw_p)   # atomic-ish: never leave a half-written raw file if this dies mid-write
    print(f"mail_merge: +{len(added):,} new e-mails ({min(r['d'] for r in added)} → {max(r['d'] for r in added)}), raw now {len(raw):,}")
    return {"added": len(added), "total": len(raw)}

# ----------------------------------------------------------------------------- step: events (earnings event windows)
def step_events_pull(universe, chunk=4, attempts=3):
    """Earnings announcement dates/times + EPS actual vs estimate (bds EARN_ANN_DT_TIME_HIST_WITH_EPS).

    MERGE, never overwrite: this field times out on chunks above ~8 tickers, so a run routinely returns a
    subset (a 10-ticker chunking on 2026-09-02 came back with 69 of 99 names). A ticker's history is
    replaced only when the pull actually returned rows for it; otherwise the cached list is kept. Small
    chunks + retries keep the miss list short, and the print says what was refreshed vs kept."""
    sys.path.insert(0, r"E:\bloomberg_api")
    from bloomberg import bds
    import time
    p = DATA / "earnings_dates.json"
    prev = json.load(open(p, encoding="utf-8")).get("events", {}) if p.exists() else {}
    bbgs = [v["bbg"] for t, v in universe.items() if t not in PRIVATE]; inv = {v["bbg"]: t for t, v in universe.items()}
    def num(x):
        try: return float(x)
        except Exception: return None
    fresh = defaultdict(list); missed = []
    for i in range(0, len(bbgs), chunk):
        sub = bbgs[i:i + chunk]; df = None
        for k in range(attempts):
            try: df = bds(sub, ["EARN_ANN_DT_TIME_HIST_WITH_EPS"]); break
            except Exception as e:
                if k == attempts - 1: print("  bds fail", [inv[b] for b in sub], str(e)[:60])
                else: time.sleep(3)
        if df is None: missed += [inv[b] for b in sub]; continue
        rows = defaultdict(dict)
        for _, r in df.iterrows(): rows[(r["ticker"], int(r["position"]))][r["name"]] = r["value"]
        got = set()
        for (bb, pos), rec in rows.items():
            d = str(rec.get("Announcement Date", ""))[:10]
            if not d or d < "2023-11-01": continue
            got.add(bb)
            fresh[inv[bb]].append({"date": d, "time": str(rec.get("Announcement Time", "") or ""), "period": rec.get("Year/Period"),
                                   "eps": num(rec.get("Earnings EPS")), "eps_cmp": num(rec.get("Comparable EPS")), "eps_est": num(rec.get("Estimate EPS"))})
        missed += [inv[b] for b in sub if b not in got]
    ev = dict(prev)                                  # keep every cached ticker...
    for t, rows_t in fresh.items(): ev[t] = sorted(rows_t, key=lambda x: x["date"])   # ...replace only what came back
    out = {"asof": TODAY.isoformat(), "events": ev, "refreshed": sorted(fresh), "kept_from_cache": sorted(set(ev) - set(fresh))}
    p.write_text(json.dumps(out), encoding="utf-8")
    print(f"events_pull: {sum(len(v) for v in ev.values())} announcements for {len(ev)} tickers "
          f"({len(fresh)} refreshed, {len(set(ev) - set(fresh))} kept from cache"
          + (f", no data for {len(set(missed) - set(fresh))}: {sorted(set(missed) - set(fresh))[:8]}" if set(missed) - set(fresh) else "") + ")")
    return out

def _first_on_or_after(series, d, maxdays=6):
    for i in range(maxdays + 1):
        k = (dt.date.fromisoformat(d) + dt.timedelta(i)).isoformat()
        if k in series: return k, series[k]
    return None, None

def step_events(universe):
    bb = json.load(open(DATA / "bbg_long.json", encoding="utf-8"))["series"]
    evs = json.load(open(DATA / "earnings_dates.json", encoding="utf-8"))["events"]
    tw = json.load(open(DATA / "tweet_daily.json", encoding="utf-8"))["tickers"]
    ss = json.load(open(DATA / "sellside_daily.json", encoding="utf-8")) if (DATA / "sellside_daily.json").exists() else None
    tickers = [t for t in universe if t not in PRIVATE and t in bb and bb[t].get("PX_LAST")]
    # equal-weight universe daily index for relative returns
    dates = sorted({d for t in tickers for d in bb[t]["PX_LAST"]})
    ew = {}; lvl = 1.0; prev = None
    for d in dates:
        if prev:
            rets = [bb[t]["PX_LAST"][d] / bb[t]["PX_LAST"][prev] - 1 for t in tickers if d in bb[t]["PX_LAST"] and prev in bb[t]["PX_LAST"]]
            if rets: lvl *= 1 + sum(rets) / len(rets)
        ew[d] = lvl; prev = d
    _xs_cache = {}
    def xs_mean(d0, d1):
        """Cross-sectional mean buy-and-hold return of the universe over [d0, d1] — the right benchmark for a
        cross-sectional study (a daily-rebalanced EW index carries a rebalancing premium that biased 15-day drifts)."""
        k = (d0, d1)
        if k not in _xs_cache:
            rs = [bb[x]["PX_LAST"][d1] / bb[x]["PX_LAST"][d0] - 1 for x in tickers if d0 in bb[x]["PX_LAST"] and d1 in bb[x]["PX_LAST"]]
            _xs_cache[k] = (sum(rs) / len(rs)) if len(rs) >= 20 else None
        return _xs_cache[k]
    def rel(t, d0, d1):
        p0, p1 = bb[t]["PX_LAST"].get(d0), bb[t]["PX_LAST"].get(d1)
        mu = xs_mean(d0, d1) if (p0 is not None and p1 is not None) else None
        if p0 is None or p1 is None or mu is None: return None, None
        raw = p1 / p0 - 1; return raw, raw - mu
    def win_mean(series, d0, d1, wts=None):
        num = den = 0.0
        for k, v in series.items():
            if d0 <= k <= d1:
                w = (wts.get(k, 0.0) if wts else 1.0) or 0.0
                if wts is None: num += v; den += 1
                else: num += w * v; den += w
        return (num / den) if den else None
    def win_sum(series, d0, d1): return sum(v for k, v in series.items() if d0 <= k <= d1)
    def own(t, d0, d1):
        days = tw.get(t, {}); m = tw_w = tw_n = 0.0
        for d, r in days.items():
            if d0 <= d <= d1: m += r["m_cur"]; tw_w += r["tone_w"]; tw_n += r["w"]
        return m, ((tw_w / tw_n) if tw_n else None)
    out = []
    cut = (TODAY - dt.timedelta(16)).isoformat()
    for t in tickers:
        s = bb[t]; px = s["PX_LAST"]
        for e in evs.get(t, []):
            d = e["date"]
            if d < "2024-01-15" or d > cut: continue
            tm = e.get("time") or ""; after = (not tm) or tm >= "15:30"
            base = d if after else (dt.date.fromisoformat(d) - dt.timedelta(1)).isoformat()
            bk = None
            for k in sorted(px):
                if k <= base: bk = k
            if not bk: continue
            rk, _ = _first_on_or_after(px, (dt.date.fromisoformat(bk) + dt.timedelta(1)).isoformat())
            if not rk: continue
            k15, _ = _first_on_or_after(px, (dt.date.fromisoformat(bk) + dt.timedelta(15)).isoformat())
            if not k15: continue
            react_raw, react = rel(t, bk, rk); tot_raw, tot15 = rel(t, bk, k15); _, drift = rel(t, rk, k15)
            pre0 = (dt.date.fromisoformat(bk) - dt.timedelta(10)).isoformat(); pre1 = (dt.date.fromisoformat(bk) - dt.timedelta(1)).isoformat()
            b0 = (dt.date.fromisoformat(bk) - dt.timedelta(40)).isoformat(); b1 = (dt.date.fromisoformat(bk) - dt.timedelta(11)).isoformat()
            post0 = d; post1 = (dt.date.fromisoformat(d) + dt.timedelta(3)).isoformat()
            cnt = s.get("TWITTER_PUBLICATION_COUNT", {}); sent = s.get("TWITTER_SENTIMENT_DAILY_AVG", {}); ncnt = s.get("NEWS_PUBLICATION_COUNT", {}); nsent = s.get("NEWS_SENTIMENT_DAILY_AVG", {})
            def ratio(ser, a0, a1, c0, c1):
                x = win_mean(ser, a0, a1); y = win_mean(ser, c0, c1)
                return math.log((x + 0.5) / (y + 0.5)) if (x is not None and y is not None) else None
            e0 = last_on_or_before(s.get("BEST_EPS", {}), pre1); em = last_on_or_before(s.get("BEST_EPS", {}), (dt.date.fromisoformat(bk) - dt.timedelta(29)).isoformat())
            eps_rev = None
            if e0 is not None and em not in (None, 0) and abs(em) > 0.05:
                eps_rev = (e0 - em) / abs(em)
                if abs(eps_rev) > 0.25: eps_rev = None
            si = None
            for k in sorted(s.get("SI_PERCENT_EQUITY_FLOAT", {})):
                if k <= bk: si = s["SI_PERCENT_EQUITY_FLOAT"][k]
            run0 = None
            for k in sorted(px):
                if k <= (dt.date.fromisoformat(bk) - dt.timedelta(20)).isoformat(): run0 = k
            _, runup = rel(t, run0, bk) if run0 else (None, None)
            est, act = e.get("eps_est"), (e.get("eps_cmp") if e.get("eps_cmp") is not None else e.get("eps"))
            surprise = ((act - est) / abs(est)) if (est not in (None, 0) and act is not None and abs(est) > 0.02) else None
            if surprise is not None and abs(surprise) > 1.0: surprise = None
            om, ot = own(t, pre0, pre1); om_base, _ = own(t, b0, b1); om_post, ot_post = own(t, post0, post1)
            own_ok = pre0 >= "2026-05-01"
            ssw = ss_window(ss, t, pre0, pre1); ssb = ss_window(ss, t, b0, b1); ssp = ss_window(ss, t, post0, post1)
            ss_ok = ss is not None and pre0 >= (ss.get("since") or "9999")
            pre_tone = win_mean(sent, pre0, pre1, cnt); post_tone = win_mean(sent, post0, post1, cnt)
            out.append({"t": t, "date": d, "period": e.get("period"), "after": after, "base": bk, "react_day": rk, "d15": k15,
                        "react": react, "react_raw": react_raw, "tot15": tot15, "tot15_raw": tot_raw, "drift": drift,
                        "surprise": surprise,
                        "bbg_att": ratio(cnt, pre0, pre1, b0, b1), "bbg_tone": pre_tone, "bbg_pos_neg": (win_sum(s.get("TWITTER_POS_SENTIMENT_COUNT", {}), pre0, pre1) - win_sum(s.get("TWITTER_NEG_SENTIMENT_COUNT", {}), pre0, pre1)) / (win_sum(cnt, pre0, pre1) or 1),
                        "news_att": ratio(ncnt, pre0, pre1, b0, b1), "news_tone": win_mean(nsent, pre0, pre1, ncnt),
                        "own_att": (math.log((om / 10 + 0.5) / (om_base / 30 + 0.5)) if own_ok else None), "own_tone": (ot if own_ok else None), "own_m": om if own_ok else None,
                        "ss_att": (math.log((ssw["n"] / 10 + 0.05) / (ssb["n"] / 30 + 0.05)) if ss_ok else None), "ss_n": ssw["n"] if ss_ok else None,
                        "ss_tone": ((ssw["tone_w"] / ssw["tone_n"]) if (ss_ok and ssw["tone_n"]) else None), "ss_net": ((ssw["up"] - ssw["down"]) if ss_ok else None),
                        "ss_pt": ((ssw["pt_sum"] / ssw["pt_n"]) if (ss_ok and ssw["pt_n"]) else None), "ss_est": ((ssw["est_up"] - ssw["est_down"]) if ss_ok else None),
                        "ss_post_pt": ((ssp["pt_sum"] / ssp["pt_n"]) if (ss_ok and ssp["pt_n"]) else None),
                        "ss_post_n": ssp["n"] if ss_ok else None, "ss_post_net": ((ssp["up"] - ssp["down"]) if ss_ok else None),
                        "eps_rev": eps_rev, "runup": runup, "si": si,
                        "post_tone_shift": ((post_tone - pre_tone) if (post_tone is not None and pre_tone is not None) else None),
                        "own_post_shift": ((ot_post - ot) if (own_ok and ot_post is not None and ot is not None) else None)})
    # ---------------- stats
    SIG = {"bbg_att": "BBG Twitter attention into print (10d vs prior 30d)", "bbg_tone": "BBG Twitter sentiment, 10d pre", "bbg_pos_neg": "BBG pos−neg share, 10d pre",
           "news_att": "BBG news attention into print", "news_tone": "BBG news sentiment, 10d pre",
           "own_att": "Own-corpus curated attention into print", "own_tone": "Own-corpus tone, 10d pre",
           "ss_att": "Sell-side note flow into print (10d vs prior 30d)", "ss_tone": "Sell-side note tone (body windows), 10d pre", "ss_net": "Sell-side net rating changes, 10d pre",
           "ss_pt": "Sell-side avg PT change %, 10d pre", "ss_est": "Sell-side net estimate revisions, 10d pre",
           "eps_rev": "EPS revision into print (4w)", "runup": "20d run-up (relative)", "si": "Short interest % float", "surprise": "EPS surprise (actual vs est)",
           "post_tone_shift": "BBG sentiment shift, days 0..+3 minus pre", "own_post_shift": "Own-corpus tone shift, days 0..+3 minus pre", "ss_post_net": "Sell-side net rating changes, days 0..+3", "ss_post_pt": "Sell-side avg PT change %, days 0..+3"}
    OUT = {"react": "reaction (base close → next close, relative)", "tot15": "15 days total (relative)", "drift": "drift, day +1 close → day +15 (relative)"}
    def ic(pairs):
        if len(pairs) < 15: return None
        a = {i: p[0] for i, p in enumerate(pairs)}; b = {i: p[1] for i, p in enumerate(pairs)}
        r, n = spearman(a, b); return r
    stats = {}
    for k in SIG:
        for o in OUT:
            pairs = [(e[k], e[o]) for e in out if e.get(k) is not None and e.get(o) is not None]
            if len(pairs) < 15: continue
            r = ic(pairs); years = {}
            for y in sorted({e["date"][:4] for e in out}):
                py = [(e[k], e[o]) for e in out if e["date"][:4] == y and e.get(k) is not None and e.get(o) is not None]
                if len(py) >= 15: years[y] = {"ic": ic(py), "n": len(py)}
            srt = sorted(pairs, key=lambda p: p[0]); q = max(1, len(srt) // 5)
            stats[f"{k}|{o}"] = {"ic": r, "n": len(pairs), "q5_q1": sum(p[1] for p in srt[-q:]) / q - sum(p[1] for p in srt[:q]) / q,
                                 "q5": sum(p[1] for p in srt[-q:]) / q, "q1": sum(p[1] for p in srt[:q]) / q, "by_year": years}
    # conditional: attention tercile × beat/miss
    cond = defaultdict(list)
    ev_ok = [e for e in out if e.get("bbg_att") is not None and e.get("surprise") is not None and e.get("tot15") is not None]
    if ev_ok:
        atts = sorted(e["bbg_att"] for e in ev_ok); lo, hi = atts[len(atts) // 3], atts[2 * len(atts) // 3]
        for e in ev_ok:
            a = "hot" if e["bbg_att"] >= hi else ("cold" if e["bbg_att"] < lo else "mid")
            b = "beat" if e["surprise"] > 0.02 else ("miss" if e["surprise"] < -0.02 else "inline")
            cond[f"{a}|{b}"].append((e["react"], e["tot15"], e["drift"]))
    cond_out = {k: {"n": len(v), "react": sum(x[0] for x in v if x[0] is not None) / max(1, sum(1 for x in v if x[0] is not None)),
                    "tot15": sum(x[1] for x in v) / len(v), "drift": sum(x[2] for x in v if x[2] is not None) / max(1, sum(1 for x in v if x[2] is not None))} for k, v in cond.items()}
    res = {"asof": TODAY.isoformat(), "n_events": len(out), "signals": SIG, "outcomes": OUT, "stats": stats, "conditional": cond_out,
           "events": out, "own_from": "2026-05-01", "ss_from": (ss or {}).get("since")}
    (DATA / "events.json").write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
    print(f"events: {len(out)} earnings events with 15d outcomes ({min(e['date'] for e in out)} → {max(e['date'] for e in out)})")
    for k in SIG:
        line = f"  {k:16s}"
        for o in OUT:
            st = stats.get(f"{k}|{o}")
            line += f" | {o[:5]} IC {st['ic']:+.3f} n={st['n']:4d} q5-q1 {st['q5_q1']:+.2%}" if st else f" | {o[:5]}   –"
        print(line)
    for k, v in sorted(cond_out.items()): print(f"  {k:12s} n={v['n']:3d} react {v['react']:+.2%} tot15 {v['tot15']:+.2%} drift {v['drift']:+.2%}")
    return res

# ----------------------------------------------------------------------------- step: dash
def step_dash():
    from _sentiment_dash import render
    panel = json.load(open(DATA / "panel_weekly.json", encoding="utf-8"))
    daily = json.load(open(DATA / "tweet_daily.json", encoding="utf-8"))
    bbg = json.load(open(DATA / "bbg_history.json", encoding="utf-8"))["series"]
    long = None
    if (DATA / "panel_long.json").exists():
        long = json.load(open(DATA / "panel_long.json", encoding="utf-8"))
        # cross-validation: does own-corpus attention/tone rank names like Bloomberg's all-of-X measures? (overlapping weeks)
        ics_a, ics_t = [], []
        for f in panel["weeks"]:
            if f not in long["panel"]: continue
            a, b = panel["panel"][f], long["panel"][f]
            ic, n = spearman({t: a[t].get("att") for t in a}, {t: b.get(t, {}).get("att") for t in a})
            if ic is not None: ics_a.append(ic)
            ic, n = spearman({t: a[t].get("tone") for t in a}, {t: b.get(t, {}).get("tone") for t in a})
            if ic is not None: ics_t.append(ic)
        if ics_a: long["xval"] = {"att": sum(ics_a) / len(ics_a), "tone": (sum(ics_t) / len(ics_t)) if ics_t else 0.0, "n": len(ics_a)}
        print("xval own-vs-BBG attention IC %+.2f, tone %+.2f over %d weeks" % (long["xval"]["att"], long["xval"]["tone"], long["xval"]["n"]) if ics_a else "xval: no overlap")
    events = json.load(open(DATA / "events.json", encoding="utf-8")) if (DATA / "events.json").exists() else None
    leadlag = json.load(open(DATA / "leadlag.json", encoding="utf-8")) if (DATA / "leadlag.json").exists() else None
    picks = json.load(open(DATA / "picks.json", encoding="utf-8")) if (DATA / "picks.json").exists() else None
    ss = json.load(open(DATA / "sellside_daily.json", encoding="utf-8")) if (DATA / "sellside_daily.json").exists() else None
    html = render(panel, daily, bbg, long, events, ss, leadlag, picks)
    (DASH / "sentiment.html").write_text(html, encoding="utf-8")
    print("wrote", DASH / "sentiment.html", f"({len(html)/1024:.0f} KB)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--step", default="all"); ap.add_argument("--no-bbg", action="store_true")
    a = ap.parse_args(); uni = load_universe()
    steps = ["tweets", "bbg", "bbglong", "mail_merge", "sellside", "panel", "long", "leadlag", "picks", "events_pull", "events", "dash"] if a.step == "all" else [a.step]
    for s in steps:
        if s == "tweets": step_tweets(uni)
        elif s == "bbg":
            if a.no_bbg and (DATA / "bbg_history.json").exists(): print("bbg: skipped (--no-bbg), using cache")
            elif not bbg_up() and (DATA / "bbg_history.json").exists(): print("bbg: Terminal not serving 127.0.0.1:8194 — keeping cache")
            else:
                try: step_bbg(uni)
                except Exception as e:
                    if (DATA / "bbg_history.json").exists(): print("bbg: terminal unavailable, using cache —", str(e)[:100])
                    else: raise
        elif s == "bbglong":
            if a.no_bbg and (DATA / "bbg_long.json").exists(): print("bbglong: skipped (--no-bbg), using cache")
            elif not bbg_up() and (DATA / "bbg_long.json").exists(): print("bbglong: Terminal not serving 127.0.0.1:8194 — keeping cache")
            else:
                try: step_bbglong(uni)
                except Exception as e:
                    if (DATA / "bbg_long.json").exists(): print("bbglong: terminal unavailable, using cache —", str(e)[:100])
                    else: raise
        elif s == "panel": step_panel(uni)
        elif s == "long": step_long(uni)
        elif s == "leadlag": step_leadlag(uni)
        elif s == "picks": step_picks(uni)
        elif s == "mail_merge": step_mail_merge()
        elif s == "sellside": step_sellside(uni)
        elif s == "events_pull":
            if a.no_bbg and (DATA / "earnings_dates.json").exists(): print("events_pull: skipped (--no-bbg), using cache"); continue
            if not bbg_up() and (DATA / "earnings_dates.json").exists(): print("events_pull: Terminal not serving 127.0.0.1:8194 — keeping cache"); continue
            try: step_events_pull(uni)
            except Exception as e:
                if (DATA / "earnings_dates.json").exists(): print("events_pull: terminal unavailable, using cache —", str(e)[:100])
                else: raise
        elif s == "events": step_events(uni)
        elif s == "dash": step_dash()
