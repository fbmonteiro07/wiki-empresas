"""sentiment_studies.py — the studies behind the merged Sentiment page.

Ported 2026-10-13 from the retired Codex "Sentiment Radar" project
(Documents/Codex/2026-09-20/a-gente-tem-um-tracker-de) so every piece rebuilds daily inside the wiki chain
off the wiki's own caches instead of a second collection pipeline:

  cnn_extremes  CNN Fear & Greed → SPY / QQQ / QQQ÷SPY over the next 5 sessions: every reading by centred band
                (30 = 25 ≤ F&G < 35), first entries into a band, and directed threshold crossings (down to ≤20/≤30,
                up to ≥70/≥80/≥90) with per-threshold non-overlap; close→t+5 and delayed t+1→t+6; circular
                20-session block bootstrap (1,000 draws). Same rules as Codex study_weekly_levels.py v2.1.
  score_bands   HOT and BULL (Bloomberg track, 0–100 = 50 + clipped z × 50/3) → the stock over the next 5 / 10
                sessions after a next-close entry; per-company non-overlap (next signal ≥ 11 sessions later);
                pooled USD names + each company's own analogs; 20-session calendar-block bootstrap (800 draws).
                Codex study_score_returns.py v1.0 rules, re-pointed at HOT/BULL (Felipe 2026-10-13: one score).
  ss_ledger     mechanical sell-side ledger: dated rating / PT / estimate actions per ticker from the parsed
                broker mail (sellside_mail_raw.json × sellside_parsed_cache.json), 30-day aggregates per name.
  daily         per-ticker daily series for the stock chart (price, Bloomberg Twitter + news count/sentiment,
                curated X mentions) and the Bloomberg-Twitter movers (7-day vs prior 4 weeks), which keep the
                'who is getting hotter' read alive when the own X corpus is stale.
  desk          the desk-review ledger: the 21-Sep Codex specialist-sales review (155 observations, retained as
                the seed) + every daily review written by the 10:00 sentiment-radar task (desk_review/*.json).

Inputs  _data/sentiment/{cnn_fg,etf_history,panel_long,bbg_long,tweet_daily,sellside_mail_raw,
        sellside_parsed_cache}.json, _dashboards/attention-sentiment/specialist-sales.json (seed, once)
Outputs _data/sentiment/{cnn_extremes,score_bands,ss_ledger,daily_series,desk_ledger}.json
stdlib only. Read-only on pages. Called by build_sentiment_monitor.py; runnable alone (py sentiment_studies.py).
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TOOLS = Path(__file__).resolve().parent
WIKI = TOOLS.parent
DATA = WIKI / "_data" / "sentiment"
DESK_DIR = DATA / "desk_review"
SEED = WIKI / "_dashboards" / "attention-sentiment" / "specialist-sales.json"
TODAY = dt.date.today()


def J(name):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False), encoding="utf-8")


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def quantile(values, p):
    if not values:
        return None
    a = sorted(values)
    k = (len(a) - 1) * p
    lo = int(k)
    hi = min(len(a) - 1, lo + 1)
    return a[lo] + (a[hi] - a[lo]) * (k - lo)


def rnd(v, d=4):
    return None if v is None else round(v, d)


def sig(*parts) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(json.dumps(p, sort_keys=True, default=str).encode("utf-8"))
    return h.hexdigest()[:16]


def universe():
    est = json.loads((WIKI / "_data" / "estimates.json").read_text(encoding="utf-8"))["companies"]
    return {t: {"name": v.get("name", t), "ccy": v.get("ccy")} for t, v in est.items()}


def last_on_or_before(series: dict, d: str, keys: list, maxdays=4):
    """Value on d or the closest earlier date within maxdays (non-US names on US sessions)."""
    import bisect
    i = bisect.bisect_right(keys, d) - 1
    if i < 0:
        return None
    if (dt.date.fromisoformat(d) - dt.date.fromisoformat(keys[i])).days > maxdays:
        return None
    return series[keys[i]]


# ============================================================================= CNN extremes
CNN_CENTERS = tuple(range(0, 101, 10))
CNN_THRESHOLDS = (20, 30, 70, 80, 90)
CNN_VERSION = "weekly-levels-v2.1-wiki"
CNN_ITER, CNN_BLOCK = 1000, 20
CNN_MODES = ("close", "delayed")


def cnn_band(fg):
    return min(100, max(0, int((fg + 5) // 10) * 10))


def _describe(rows):
    vals = [r["ret"] for r in rows]
    return {"n": len(vals), "mean": mean(vals), "median": statistics.median(vals) if vals else None,
            "pos": 100 * sum(v > 0 for v in vals) / len(vals) if vals else None,
            "p10": quantile(vals, .1), "p90": quantile(vals, .9),
            "first": rows[0]["date"] if rows else None, "last": rows[-1]["date"] if rows else None}


def _membership(rows, mode):
    last_band_exit, last_cross_exit, members = {}, {}, {}
    for i, r in enumerate(rows):
        labels = []
        if r["fg"] is not None and r["ret"][mode] is not None:
            c = cnn_band(r["fg"])
            labels.append(f"all_{c}")
            prev = rows[i - 1] if i else None
            if prev and prev["fg"] is not None:          # an unknown prior reading cannot establish a fresh entry
                if cnn_band(prev["fg"]) != c and r["entry"][mode] >= last_band_exit.get(c, -1):
                    labels.append(f"episode_{c}"); last_band_exit[c] = r["exit"][mode]
                for th in CNN_THRESHOLDS:
                    crossed = (prev["fg"] > th >= r["fg"]) if th <= 30 else (prev["fg"] < th <= r["fg"])
                    if crossed and r["entry"][mode] >= last_cross_exit.get(th, -1):
                        labels.append(f"cross_{th}"); last_cross_exit[th] = r["exit"][mode]
        members[i] = labels
    return members


def _bootstrap(rows, members, mode, seed):
    n = len(rows)
    rng = random.Random(seed)
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for _ in range(CNN_ITER):
        idx = []
        while len(idx) < n:
            s = rng.randrange(n)
            idx.extend((s + j) % n for j in range(CNN_BLOCK))
        vals = collections.defaultdict(list); base = []
        for i in idx[:n]:
            v = rows[i]["ret"][mode]
            if v is None or rows[i]["fg"] is None:
                continue
            base.append(v)
            for k in members[i]:
                vals[k].append(v)
        avg = mean(base)
        for k, vs in vals.items():
            if len(vs) < 3:
                continue
            m = sum(vs) / len(vs)
            out[k]["mean"].append(m); out[k]["excess"].append(m - avg)
    return out


def cnn_extremes(force=False):
    cnn = J("cnn_fg.json") or {}
    etf = J("etf_history.json")
    hist = cnn.get("history", {})
    if not hist or not etf:
        print("  cnn_extremes: missing cnn_fg.json or etf_history.json — skipped")
        return J("cnn_extremes.json")
    tri = {k: etf["series"][k]["TRI"] for k in ("SPY", "QQQ")}
    start = min(hist)
    days = sorted(d for d in tri["SPY"].keys() & tri["QQQ"].keys() if d >= start)
    key = sig(CNN_VERSION, [(d, hist.get(d)) for d in days], [tri["SPY"][d] for d in days], [tri["QQQ"][d] for d in days], max(hist), hist[max(hist)])
    prev = J("cnn_extremes.json")
    if prev and prev.get("meta", {}).get("sig") == key and not force:
        return prev
    results, recent = {}, {}
    for tk in ("SPY", "QQQ", "QQQ/SPY"):
        tr = [tri[tk][d] if tk != "QQQ/SPY" else tri["QQQ"][d] / tri["SPY"][d] for d in days]
        rows = []
        for i, d in enumerate(days):
            r = {"date": d, "fg": hist.get(d), "ret": {}, "entry": {}, "exit": {}, "exit_date": {}}
            for mode in CNN_MODES:
                ent = i + (mode == "delayed"); end = ent + 5
                r["ret"][mode] = (tr[end] / tr[ent] - 1) * 100 if end < len(days) else None
                r["entry"][mode], r["exit"][mode] = ent, end
                r["exit_date"][mode] = days[end] if end < len(days) else None
            rows.append(r)
        results[tk] = {}
        for mode in CNN_MODES:
            members = _membership(rows, mode)
            boot = _bootstrap(rows, members, mode, 20260921 + (mode == "delayed"))
            elig = [{"date": r["date"], "fg": r["fg"], "ret": r["ret"][mode], "exit_date": r["exit_date"][mode], "groups": members[i]}
                    for i, r in enumerate(rows) if r["fg"] is not None and r["ret"][mode] is not None]
            base = _describe(elig)
            groups = {}
            for fam, cs in (("all", CNN_CENTERS), ("episode", CNN_CENTERS), ("cross", CNN_THRESHOLDS)):
                for c in cs:
                    k = f"{fam}_{c}"
                    sub = [r for r in elig if k in r["groups"]]
                    st = _describe(sub)
                    st["excess"] = (st["mean"] - base["mean"]) if sub else None
                    b = boot.get(k, {})
                    for metric in ("mean", "excess"):
                        vs = b.get(metric, [])
                        st[f"{metric}_ci"] = [quantile(vs, .025), quantile(vs, .975)] if len(sub) >= 10 and len(vs) >= CNN_ITER * .8 else None
                    st["years"] = {y: _describe([r for r in sub if r["date"][:4] == y and (r["exit_date"] or "")[:4] == y])["mean"]
                                   for y in sorted({r["date"][:4] for r in rows})}
                    st["status"] = "no observations" if not sub else ("small sample" if len(sub) < 20 else "descriptive")
                    if fam == "cross":
                        st["events"] = [[r["date"], round(r["fg"], 1), round(r["ret"], 2)] for r in sub]
                    groups[k] = {kk: (rnd(v, 3) if isinstance(v, float) else v) for kk, v in st.items()}
            results[tk][mode] = {"baseline": {k: (rnd(v, 3) if isinstance(v, float) else v) for k, v in base.items()}, "groups": groups}
        # every crossing in the last ~6 months, matured or pending (display list; no non-overlap filter)
        rc = []
        for i in range(1, len(rows)):
            p, r = rows[i - 1], rows[i]
            if p["fg"] is None or r["fg"] is None or r["date"] < (TODAY - dt.timedelta(days=190)).isoformat():
                continue
            for th in CNN_THRESHOLDS:
                crossed = (p["fg"] > th >= r["fg"]) if th <= 30 else (p["fg"] < th <= r["fg"])
                if crossed:
                    rc.append({"date": r["date"], "th": th, "dir": "down" if th <= 30 else "up", "fg": round(r["fg"], 1),
                               "ret": rnd(r["ret"]["close"], 2), "matures": days[i + 5] if i + 5 < len(days) else None})
        recent[tk] = rc
    hk = sorted(hist)
    cur = hist[hk[-1]]
    zone = ("≤20" if cur <= 20 else "≤30" if cur <= 30 else "≥90" if cur >= 90 else "≥80" if cur >= 80 else "≥70" if cur >= 70 else None)
    out = {"meta": {"version": CNN_VERSION, "sig": key, "built": dt.datetime.now().isoformat(timespec="minutes"),
                    "start": days[0], "price_end": days[-1], "cnn_through": hk[-1], "obs_min": min(hist.values()), "obs_max": max(hist.values()),
                    "horizon_sessions": 5, "thresholds": list(CNN_THRESHOLDS), "centers": list(CNN_CENTERS),
                    "bootstrap": {"iterations": CNN_ITER, "block_sessions": CNN_BLOCK},
                    "timing": {"close": "close on the reading date → close 5 ETF sessions later (descriptive; CNN vintages are not immutable)",
                               "delayed": "enter at the next close, exit 5 sessions after entry (conservative sensitivity)"},
                    "samples": {"all": "every eligible reading in [c−5, c+5); outcomes overlap",
                                "episode": "first entry into a band from outside, with a known prior reading; no entry before the previous selected exit for that band",
                                "cross": "first crossing down to ≤20/≤30 or up to ≥70/≥80/≥90; days inside a zone are not new events; deeper thresholds in the same phase are related, not independent"},
                    "limitations": ["Retrospective, potentially revised CNN history (no publication-time vintages).",
                                    "Five trading sessions, not a calendar week.",
                                    "A positive conditional mean is not skill: compare with the unconditional mean and hit rate.",
                                    "No CI below 10 observations; under 20 is flagged as a small sample. No correction for many comparisons."]},
           "current": {"date": hk[-1], "fg": cur, "band": cnn_band(cur), "zone": zone},
           "results": results, "recent": recent}
    save("cnn_extremes.json", out)
    print(f"  cnn_extremes: {days[0]} → {days[-1]} · F&G {cur:.0f} (band {cnn_band(cur)}) · "
          f"SPY cross≤30 n={results['SPY']['close']['groups']['cross_30']['n']} · cross≥70 n={results['SPY']['close']['groups']['cross_70']['n']}")
    return out


# ============================================================================= HOT / BULL score bands
SB_VERSION = "score-bands-v1.0-hotbull"
SB_BANDS = ["0–<20", "20–<40", "40–<60", "60–<80", "80–100"]
SB_PERIODS = {"all": ("2024-01-01", "9999-12-31"), "pre2026": ("2024-01-01", "2025-12-31"), "2026": ("2026-01-01", "9999-12-31")}
SB_BLOCK, SB_ITER = 20, 800
SB_HORIZONS = (5, 10)


def to_score(z):
    return None if z is None else 50 + max(-3.0, min(3.0, z)) * 50 / 3


def sb_band(s):
    return None if s is None else min(4, int(s // 20))


def _sb_plan(dates, start, end):
    idx = [i for i, d in enumerate(dates) if start <= d <= end]
    blocks = sorted({i // SB_BLOCK for i in idx})
    rng = random.Random(230926)
    return [collections.Counter(rng.choices(blocks, k=len(blocks))) for _ in range(SB_ITER)] if blocks else []


def _sb_summary(events, h, start, end, plan):
    pairs = [(e, e["o"][h]) for e in events if start <= e["date"] <= end and h in e["o"] and e["o"][h]["exit"] <= end]
    vals = [o["ret"] for _, o in pairs]
    out = {"n": len(vals), "stocks": len({e["t"] for e, _ in pairs}), "mean": rnd(mean(vals), 3), "median": rnd(statistics.median(vals), 3) if vals else None,
           "up": rnd(100 * sum(v > 0 for v in vals) / len(vals), 1) if vals else None, "p10": rnd(quantile(vals, .1), 3), "p90": rnd(quantile(vals, .9), 3), "ci": None}
    ex = [o["xs"] for _, o in pairs if o.get("xs") is not None]
    out["xs_qqq"] = rnd(mean(ex), 3); out["xs_n"] = len(ex)
    if len(vals) >= 10:
        groups = collections.defaultdict(lambda: [0.0, 0])
        for e, o in pairs:
            g = groups[e["i"] // SB_BLOCK]; g[0] += o["ret"]; g[1] += 1
        if len(groups) >= 5:
            sims = []
            for w in plan:
                den = sum(n * w.get(k, 0) for k, (_, n) in groups.items())
                if den:
                    sims.append(sum(s * w.get(k, 0) for k, (s, _) in groups.items()) / den)
            if len(sims) >= SB_ITER * .95:
                out["ci"] = [rnd(quantile(sims, .025), 3), rnd(quantile(sims, .975), 3)]
    return out


def _sb_scope(events, dates, plans):
    res = {}
    for per, (a, b) in SB_PERIODS.items():
        res[per] = {}
        for h in SB_HORIZONS:
            base = _sb_summary(events, h, a, b, plans[per])
            bands = [_sb_summary([e for e in events if e["band"] == k], h, a, b, plans[per]) for k in range(5)]
            for x in bands:
                x["vs_base"] = rnd(x["mean"] - base["mean"], 3) if x["n"] and base["mean"] is not None else None
            res[per][str(h)] = {"base": base, "bands": bands}
    return res


def score_bands(force=False):
    pl = J("panel_long.json"); bl = J("bbg_long.json"); etf = J("etf_history.json")
    if not (pl and bl and etf):
        print("  score_bands: missing panel_long / bbg_long / etf_history — skipped")
        return J("score_bands.json")
    uni = universe()
    qqq = etf["series"]["QQQ"]["PX_LAST"]
    dates = sorted(d for d in etf["series"]["SPY"]["PX_LAST"] if d >= "2023-12-01")      # US session calendar
    weeks = pl["weeks"]
    key = sig(SB_VERSION, weeks[-1], pl.get("asof"), bl.get("asof"), dates[-1], len(dates))
    prev = J("score_bands.json")
    if prev and prev.get("meta", {}).get("sig") == key and not force:
        return prev
    import bisect
    widx = {w: bisect.bisect_right(dates, w) - 1 for w in weeks}
    px = {t: s.get("PX_LAST", {}) for t, s in bl["series"].items()}
    pkeys = {t: sorted(s) for t, s in px.items()}
    plans = {per: _sb_plan(dates, a, b) for per, (a, b) in SB_PERIODS.items()}
    out = {"meta": {}, "pooled": {}, "companies": {}}
    for fam in ("HOT", "BULL"):
        ledger = collections.defaultdict(list)
        for t in sorted({t for w in weeks for t in pl["panel"][w]}):
            usd = (uni.get(t, {}).get("ccy") == "USD")
            nxt = 0
            for w in weeks:
                r = pl["panel"][w].get(t)
                s = to_score(r.get(fam)) if r else None
                i = widx[w]
                if s is None or i < nxt or i < 0:
                    continue
                nxt = i + 11                                  # the slot is taken even if the outcome is immature
                ev = {"t": t, "date": dates[i], "w": w, "i": i, "score": round(s, 1), "band": sb_band(s), "usd": usd, "o": {}}
                for h in SB_HORIZONS:
                    ent, end = i + 1, i + 1 + h
                    if end >= len(dates):
                        continue
                    d0, d1 = dates[ent], dates[end]
                    if usd:
                        a, b = px.get(t, {}).get(d0), px.get(t, {}).get(d1)
                    else:
                        a = last_on_or_before(px.get(t, {}), d0, pkeys.get(t, [])); b = last_on_or_before(px.get(t, {}), d1, pkeys.get(t, []))
                    if not a or not b or a <= 0 or b <= 0:
                        continue
                    ret = 100 * (b / a - 1)
                    q0, q1 = qqq.get(d0), qqq.get(d1)
                    xs = (ret - 100 * (q1 / q0 - 1)) if (usd and q0 and q1) else None
                    ev["o"][h] = {"ret": ret, "xs": xs, "exit": d1}
                ledger[t].append(ev)
        pooled = [e for t, evs in ledger.items() for e in evs if e["usd"]]
        out["pooled"][fam] = _sb_scope(pooled, dates, plans)
        lw = weeks[-1]
        for t, evs in ledger.items():
            r = pl["panel"][lw].get(t) or {}
            s = to_score(r.get(fam))
            c = out["companies"].setdefault(t, {"name": (pl.get("names") or {}).get(t, uni.get(t, {}).get("name", t)), "usd": uni.get(t, {}).get("ccy") == "USD"})
            own = []
            b = sb_band(s)
            for h in SB_HORIZONS:
                same = [e for e in evs if e["band"] == b and h in e["o"]] if b is not None else []
                vals = [e["o"][h]["ret"] for e in same]
                own.append({"h": h, "n": len(vals), "mean": rnd(mean(vals), 3), "median": rnd(statistics.median(vals), 3) if vals else None,
                            "up": rnd(100 * sum(v > 0 for v in vals) / len(vals), 1) if vals else None,
                            "p10": rnd(quantile(vals, .1), 3), "p90": rnd(quantile(vals, .9), 3)})
            c[fam] = {"score": rnd(s, 1), "band": b, "own": own, "n_signals": len(evs)}
        print(f"  score_bands {fam}: {sum(len(v) for v in ledger.values())} sampled signals · pooled USD {len(pooled)}")
    out["meta"] = {"version": SB_VERSION, "sig": key, "built": dt.datetime.now().isoformat(timespec="minutes"), "track": "Bloomberg track (panel_long)",
                   "week": weeks[-1], "first_week": weeks[0], "price_asof": bl.get("asof"), "qqq_asof": max(qqq), "bands": SB_BANDS, "horizons": list(SB_HORIZONS),
                   "score": "0–100 = 50 + clip(z, ±3) × 50/3, z = the weekly HOT / BULL composite (50 = that week's average name)",
                   "sampling": "per company: first valid weekly score, then the first one at least 11 US sessions later; same sample for both horizons; no selection on outcomes",
                   "timing": "score at the Friday close (t); entry next session close (t+1); exits t+6 / t+11 (5 / 10-session holds); exact-date prices for USD names, last price within 4 days for non-US names",
                   "uncertainty": f"95% interval for the mean: {SB_ITER} resamples of fixed {SB_BLOCK}-session calendar blocks carrying all stocks together; ≥10 outcomes and ≥5 occupied blocks",
                   "baseline": "all bands in the same scope/period/horizon; pooled = USD names, event-weighted; QQQ excess = same-date PX_LAST, USD names only",
                   "periods": "2024–25 purged at 31-Dec-2025; 2026 is a stability check, not a holdout",
                   "limitations": ["Weekly composite, so successive samples are ~3 weeks apart per name; names and market phases are not independent.",
                                   "HOT/BULL are coincident-to-lagging on the weekly CCF (see the lead/lag study): read the bands as context, not a forecast.",
                                   "Fewer than 10 own-stock outcomes → no headline estimate; under 20 is thin."]}
    save("score_bands.json", out)
    return out


# ============================================================================= sell-side ledger (mechanical)
import re  # noqa: E402
_RATING = (r"(?:Buy|Overweight|OW|Outperform|OP|Neutral|Equal[- ]?Weight|EW|Hold|Sell|Underweight|UW|Underperform|Market[- ]Perform|"
           r"Sector[- ]Perform|Peer[- ]Perform|Accumulate|Reduce|Add)")
# a rating CHANGE in the subject: "Upgrade to OW", "Upgrading to Overweight", "upgraded to Overweight from Equal-weight",
# "Buy from Neutral", "U/G to Buy" — a bare "upgrade" (iPhone upgrade cycle, CCL upgrade roadmap) does not count
RX_RATING_SUBJ = re.compile(r"\b(?:upgrad\w*|downgrad\w*|U/G|D/G)\b\s+(?:\w+\s+){0,3}?to\s+" + _RATING + r"\b|\b" + _RATING + r"\s+from\s+" + _RATING + r"\b", re.I)
RX_PT_SUBJ = re.compile(r"\b(?:PT|TP|PO|price target|target price|price objective)\b", re.I)
# multi-topic digests: the parser maps whichever universe name they mention to actions about other companies
RX_DIGEST = re.compile(r"morning|must read|on my radar|radar|recap|today|one[- ]liners|AM (?:Note|View)|\bAM\b \d|sketch|best of|takeaways|daily|wrap|"
                       r"week ahead|weekly|digest|highlights|chips for breakfast|silk road|ideas|thoughts|minute|notes from|first read", re.I)


RX_PAREN_TK = re.compile(r"\(([A-Z0-9]{2,6})(?:\.[A-Z]{1,2})?\)")


def _foreign_ticker(t, subj):
    """A parenthesised ticker in the subject that is not this one ('Gemini Space Station Inc. (GEMI)') = another company."""
    return any(m.group(1) != t for m in RX_PAREN_TK.finditer(subj))


def _rating_names(t, subj, aliases):
    """For a rating change: the segment right before the last ':' ahead of the rating phrase must name the company
    ('JPM | META: Upgrade to OW' yes; 'GUC: Stronger Google CPU ramp …; Upgrade to OW' no — that is GUC's upgrade)."""
    m = RX_RATING_SUBJ.search(subj)
    if not m:
        return False
    head = subj[:m.start()]
    if ":" not in head:
        return True
    segs = head.split(":")
    return _subject_names(t, segs[-2], aliases)


RX_BROKER_LEAD = re.compile(r"^\s*(?:JPM|UBS|GS|MS|BofA|Bernstein|Jefferies|JEF|Barclays|Citi|Citigroup|DB|Deutsche Bank|Redburn|Rothschild|"
                            r"Evercore|Wolfe|Mizuho|Nomura|Macquarie|HSBC|BNP|Cantor|KeyBanc|Needham|Stifel|Piper|Raymond James|TD Cowen|Cowen|"
                            r"Wells Fargo|WFS|IDEA|First Read|Flash|Update)\b[^:]*$", re.I)
TICKER_STOP = {"JPM", "UBS", "GS", "MS", "DB", "JEF", "AI", "US", "USA", "PT", "TP", "PO", "OW", "UW", "EW", "OP", "EPS", "CEO", "CFO", "GPU", "CPU",
               "ASIC", "HBM", "DRAM", "NAND", "AWS", "TMT", "IT", "FY", "YOY", "YTD", "NEW", "BUY", "SELL", "HOLD", "ADD", "ETF", "EU", "UK", "APAC",
               "EM", "ASIA", "LLM", "SAAS", "ARR", "NRR", "CPO", "NPO", "OCS", "ASP", "TAM", "ROI", "FCF", "GM", "OM", "EV", "ADAS", "IPO", "CY",
               "PC", "PCB", "CCL", "DC", "AR", "VR", "OEM", "ODM", "RMB", "NT", "HK", "TT", "JP", "KS", "GR", "NA", "LN", "FQ", "RE", "VS", "UPS"}


def _lead_names(t, subj, aliases):
    """The entity a 'Name: …' subject is about must be this company; broker prefixes ('UBS:', 'JPM | Software |') are skipped
    ('Alchip Technologies: … Trn3 ramp …' is Alchip's note even when it mentions Google)."""
    segs = subj.split(":")
    for seg in segs[:-1]:
        if _subject_names(t, seg, aliases):
            return True
        if not RX_BROKER_LEAD.search(seg):
            return False
    return True


def _multi_name(t, subj):
    """Two or more other ticker-like tokens ('Earnings feedback (AFRM, IREN, S, WDAY)', 'MDB/SNOW previews') = a multi-name note."""
    toks = set(re.findall(r"(?<![A-Za-z0-9])([A-Z]{2,5})(?![A-Za-z0-9])", subj)) - TICKER_STOP - {t}
    return len(toks) >= 2

def _subject_names(t, subj, aliases):
    """The ticker itself (word, $T, (T), 'T US') or one of its company aliases as a whole word — so 'MetaX' is not META."""
    if re.search(r"(?<![A-Za-z0-9])\$?" + re.escape(t) + r"(?![A-Za-z0-9])", subj):
        return True
    return any(re.search(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", subj, re.I) for a in aliases.get(t, []))


def ss_ledger(force=False):
    raw = J("sellside_mail_raw.json"); cache = J("sellside_parsed_cache.json")
    if not raw or not cache:
        print("  ss_ledger: missing raw mail or parse cache — skipped")
        return J("ss_ledger.json")
    key = sig("ss-ledger-v6", len(raw), raw[-1].get("id") if raw else None, cache.get("_v"), len(cache))
    prev = J("ss_ledger.json")
    if prev and prev.get("meta", {}).get("sig") == key and not force:
        return prev
    through = max((r.get("d") for r in raw if r.get("d")), default=None)
    if not through:
        return prev
    cut90 = (dt.date.fromisoformat(through) - dt.timedelta(days=90)).isoformat()
    try:
        from build_sentiment import ALIASES as aliases
    except Exception:  # noqa: BLE001
        aliases = {}
    seen, events = set(), []
    flow = collections.defaultdict(lambda: collections.defaultdict(float))     # t -> date -> weighted notes
    firms_by = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in raw:
        d = r.get("d"); rec = cache.get(r.get("id") or "")
        if not d or not isinstance(rec, dict) or not rec.get("per"):
            continue
        S = set(rec.get("S") or [])
        for t, (w, sc, nh, up, dn, pt, est) in rec["per"].items():
            flow[t][d] += w
            firms_by[t][d].add(rec.get("firm"))
            if d < cut90:
                continue
            # The parser's action flags are read from the e-mail body and fire on recaps, product "upgrades" and other
            # names' initiations (checked 2026-10-13: 16 "NVDA upgrades" in a month, none real). A dated action on this
            # ledger therefore needs the ticker in the SUBJECT and, for a rating change, rating language in the subject.
            subj = r.get("subject") or ""
            if (t not in S or len(S) > 2 or RX_DIGEST.search(subj) or _foreign_ticker(t, subj) or _multi_name(t, subj)
                    or not _subject_names(t, subj, aliases) or not _lead_names(t, subj, aliases)):
                continue
            single = len(S) == 1
            kinds = []
            if single and (up or dn) and _rating_names(t, subj, aliases):
                kinds.append("upgrade" if up else "downgrade")
            if pt is not None and (abs(abs(pt) - 0.05) > 1e-9 or RX_PT_SUBJ.search(subj)):
                kinds.append("PT raise" if pt > 0 else "PT cut" if pt < 0 else "PT maintained")
            if est and single:
                kinds.append("estimates up" if est > 0 else "estimates down")
            if not kinds:
                continue
            is_pt = any(k.startswith("PT") for k in kinds)
            events.append({"d": d, "tm": r.get("t"), "t": t, "firm": rec.get("firm"), "kinds": kinds, "pt": rnd(pt, 4) if is_pt else None,
                           "pt_nominal": is_pt and abs(abs(pt) - 0.05) < 1e-9,       # direction only ("raising PT"), size unknown
                           "tone": rnd(sc, 2) if nh else None, "s": (r.get("subject") or "")[:150]})
    events.sort(key=lambda e: (e["d"], e.get("tm") or ""), reverse=True)
    # the same firm repeating the same action on a name within 3 days (analyst note + desk relay, forwards) counts once
    kept, last = [], {}
    for ev in events:
        for k in ev["kinds"]:
            key2 = (ev["t"], ev["firm"], k)
            if key2 in last and (dt.date.fromisoformat(last[key2]) - dt.date.fromisoformat(ev["d"])).days <= 3:
                ev["kinds"] = [x for x in ev["kinds"] if x != k]
            else:
                last[key2] = ev["d"]
        if ev["kinds"]:
            kept.append(ev)
    events = kept
    D = dt.date.fromisoformat(through)
    def wsum(t, a, b):
        return sum(v for dd, v in flow[t].items() if a <= dd <= b)
    a30, a90 = (D - dt.timedelta(days=29)).isoformat(), (D - dt.timedelta(days=119)).isoformat()
    b30 = (D - dt.timedelta(days=30)).isoformat()
    names = {}
    for t in flow:
        ev = [e for e in events if e["t"] == t and e["d"] >= a30]
        n30 = wsum(t, a30, through); prior = wsum(t, a90, b30) / 3
        firms30 = set().union(*[s for dd, s in firms_by[t].items() if dd >= a30]) if any(dd >= a30 for dd in firms_by[t]) else set()
        pts = [e["pt"] for e in ev if e["pt"] is not None and e["pt"] != 0 and not e.get("pt_nominal")]
        names[t] = {"notes30": round(n30, 1), "notes_prior30": round(prior, 1), "flow": rnd(math.log((n30 + 1) / (prior + 1)), 3),
                    "firms30": len(firms30 - {None}), "up": sum("upgrade" in e["kinds"] for e in ev), "down": sum("downgrade" in e["kinds"] for e in ev),
                    "pt_up": sum("PT raise" in e["kinds"] for e in ev), "pt_down": sum("PT cut" in e["kinds"] for e in ev),
                    "pt_avg": rnd(mean(pts), 4), "est_up": sum("estimates up" in e["kinds"] for e in ev), "est_down": sum("estimates down" in e["kinds"] for e in ev),
                    "last": max((e["d"] for e in events if e["t"] == t), default=None)}
    out = {"meta": {"sig": key, "built": dt.datetime.now().isoformat(timespec="minutes"), "through": through, "window_days": 30, "events_days": 90,
                    "emails": len(raw), "rule": "an action counts only from a subject about the company itself (ticker or company name as a whole word, the company — not another one — leading any 'Name:' prefix, no other tickers, no multi-topic digests); a rating change also needs rating-change grammar in the subject ('Upgrade to OW', 'Buy from Neutral'); a PT change needs an explicit from/to move or a PT mention; "
                    "the same firm + ticker + action on the same day counts once. Notes flow = weighted e-mails mentioning the name, last 30 days vs the prior 90-day monthly average (log ratio)."},
           "names": names, "events": events[:1500]}
    save("ss_ledger.json", out)
    print(f"  ss_ledger: mail through {through} · {len(events)} dated actions in 90 days · {len(names)} names")
    return out


# ============================================================================= daily series + Bloomberg-Twitter movers
DAILY_DAYS = 400


def daily_series(force=False):
    bl = J("bbg_long.json"); td = J("tweet_daily.json"); etf = J("etf_history.json")
    if not bl:
        return J("daily_series.json")
    key = sig("daily-v1", bl.get("asof"), (td or {}).get("asof"), (etf or {}).get("asof"), TODAY.isoformat())
    prev = J("daily_series.json")
    if prev and prev.get("meta", {}).get("sig") == key and not force:
        return prev
    uni = universe()
    start = (TODAY - dt.timedelta(days=DAILY_DAYS)).isoformat()
    cal = sorted({d for s in bl["series"].values() for f in ("PX_LAST", "TWITTER_PUBLICATION_COUNT") for d in s.get(f, {}) if d >= start})
    qqq = (etf or {}).get("series", {}).get("QQQ", {}).get("PX_LAST", {})
    F = {"px": "PX_LAST", "tw": "TWITTER_PUBLICATION_COUNT", "ts": "TWITTER_SENTIMENT_DAILY_AVG", "nw": "NEWS_PUBLICATION_COUNT", "ns": "NEWS_SENTIMENT_DAILY_AVG"}
    tick = {}
    for t, s in bl["series"].items():
        row = {}
        for k, f in F.items():
            ser = s.get(f, {})
            if k == "px":
                row[k] = [None if ser.get(d) is None else float(f"{ser[d]:.5g}") for d in cal]
            elif k in ("tw", "nw"):
                row[k] = [None if ser.get(d) is None else int(round(ser[d])) for d in cal]
            else:
                row[k] = [None if ser.get(d) is None else round(ser[d], 3) for d in cal]
        own = (td or {}).get("tickers", {}).get(t, {})
        row["x"] = [None if d not in own else round(own[d].get("m_cur", 0) or 0, 1) for d in cal]
        tick[t] = row
    q = [None if qqq.get(d) is None else round(qqq[d], 3) for d in cal]
    # ---- Bloomberg-Twitter movers: 7-day average count vs the prior 28 days, log ratio z across names; Δ vs a week earlier
    def mom(series: dict, end: dt.date):
        def avg(a, b):
            vals = [v for d, v in series.items() if a <= d <= b]
            return sum(vals) / len(vals) if vals else 0.0
        a7 = avg((end - dt.timedelta(days=6)).isoformat(), end.isoformat())
        b28 = avg((end - dt.timedelta(days=34)).isoformat(), (end - dt.timedelta(days=7)).isoformat())
        return a7, b28, math.log((a7 + 1) / (b28 + 1))
    end = max((d for s in bl["series"].values() for d in s.get("TWITTER_PUBLICATION_COUNT", {})), default=None)
    movers = []
    if end:
        E = dt.date.fromisoformat(end)
        cur, prv, meta = {}, {}, {}
        for t, s in bl["series"].items():
            tw = s.get("TWITTER_PUBLICATION_COUNT", {})
            if not tw:
                continue
            a7, b28, m1 = mom(tw, E)
            if max(a7, b28) < 20:                               # under ~20 posts/day the ratio is noise
                continue
            cur[t] = m1; prv[t] = mom(tw, E - dt.timedelta(days=7))[2]
            ts = [v for d, v in s.get("TWITTER_SENTIMENT_DAILY_AVG", {}).items() if (E - dt.timedelta(days=6)).isoformat() <= d <= end]
            ts0 = [v for d, v in s.get("TWITTER_SENTIMENT_DAILY_AVG", {}).items() if (E - dt.timedelta(days=34)).isoformat() <= d <= (E - dt.timedelta(days=7)).isoformat()]
            pxs = s.get("PX_LAST", {}); pk = sorted(pxs)
            def ret(k):
                a = last_on_or_before(pxs, (E - dt.timedelta(days=k)).isoformat(), pk, 6); b = last_on_or_before(pxs, end, pk, 6)
                return None if not (a and b) else b / a - 1
            meta[t] = {"a7": a7, "b28": b28, "tone": mean(ts), "dtone": (mean(ts) - mean(ts0)) if ts and ts0 else None, "r7": ret(7), "r28": ret(28)}
        def z(d):
            v = list(d.values())
            if len(v) < 5:
                return {}
            m = sum(v) / len(v); sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** .5 or 1
            return {k: max(-3, min(3, (x - m) / sd)) for k, x in d.items()}
        zc, zp = z(cur), z(prv)
        for t in cur:
            if t in zc and t in zp:
                m = meta[t]
                movers.append({"t": t, "name": uni.get(t, {}).get("name", t), "z": rnd(zc[t], 3), "dz": rnd(zc[t] - zp[t], 3), "a7": round(m["a7"], 1), "b28": round(m["b28"], 1),
                               "tone": rnd(m["tone"], 3), "dtone": rnd(m["dtone"], 3), "r7": rnd(m["r7"], 4), "r28": rnd(m["r28"], 4)})
    out = {"meta": {"sig": key, "built": dt.datetime.now().isoformat(timespec="minutes"), "start": cal[0] if cal else None, "end": cal[-1] if cal else None,
                    "bbg_asof": bl.get("asof"), "x_through": max((max(v) for v in (td or {}).get("tickers", {}).values() if v), default=None),
                    "fields": {"px": "PX_LAST (local ccy)", "tw": "Bloomberg TWITTER_PUBLICATION_COUNT (all of X)", "ts": "TWITTER_SENTIMENT_DAILY_AVG (−1..+1)",
                               "nw": "NEWS_PUBLICATION_COUNT", "ns": "NEWS_SENTIMENT_DAILY_AVG", "x": "curated-handle mentions (own corpus, tweets.sqlite)"},
                    "movers_through": end, "movers_rule": "Bloomberg Twitter count: 7-day daily average vs the prior 28 days, log((a7+1)/(b28+1)) z-scored across names; Δ = change in that z vs a week earlier; names under ~20 posts/day in both windows dropped"},
           "dates": cal, "qqq": q, "tickers": tick, "names": {t: uni.get(t, {}).get("name", t) for t in tick}, "movers": movers}
    save("daily_series.json", out)
    print(f"  daily_series: {len(cal)} days × {len(tick)} names · BBG-Twitter movers through {end}: {len(movers)} names")
    return out


# ============================================================================= desk-review ledger
def _seed_from_codex():
    """Convert the retained 21-Sep Codex specialist-sales review into ledger observations (once; cached)."""
    p = DATA / "desk_seed_codex_2026-09-21.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    if not SEED.exists():
        return {"observations": [], "companies": {}, "meta": {}}
    j = json.loads(SEED.read_text(encoding="utf-8"))
    src = j.get("sources", {})
    obs = []
    for t, c in j.get("companies", {}).items():
        for o in c.get("observations", []):
            s = src.get(o.get("source"), {})
            obs.append({"id": "codex-" + o.get("id", ""), "date": o.get("date"), "ticker": t, "firm": s.get("firm"), "author": s.get("author"),
                        "role": s.get("role"), "kind": o.get("kind"), "tone": o.get("tone"), "position": o.get("position"),
                        "summary": o.get("summary"), "excerpt": o.get("excerpt"), "subject": s.get("subject"), "source_id": s.get("original_id") or o.get("source"),
                        "review": "Codex contextual review of 07–21 Sep 2026 (retained seed)", "review_date": "2026-09-21"})
    comp = {t: {k: c.get(k) for k in ("coverage", "tone", "position", "summary", "latest", "houses")} for t, c in j.get("companies", {}).items()}
    seed = {"meta": {**j.get("meta", {}), "converted": TODAY.isoformat(), "from": str(SEED)}, "observations": obs, "companies": comp,
            "macro": j.get("macro", []), "highlights": j.get("highlights", {})}
    p.write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  desk: seeded {len(obs)} observations from the Codex 21-Sep review")
    return seed


def desk_ledger(force=False):
    seed = _seed_from_codex()
    reviews = sorted(DESK_DIR.glob("20??-??-??.json")) if DESK_DIR.exists() else []
    obs = {o["id"]: o for o in seed.get("observations", [])}
    rv = []
    for p in reviews:
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa: BLE001
            print(f"  desk: {p.name} unreadable ({ex})"); continue
        for o in r.get("observations", []):
            if o.get("id") and o.get("ticker"):
                o.setdefault("review", "Claude daily desk review"); o.setdefault("review_date", r.get("date"))
                obs[o["id"]] = o
        rv.append({"date": r.get("date"), "file": p.name, "headline": r.get("headline"), "n_obs": len(r.get("observations", [])),
                   "mail_window": r.get("mail_window"), "status": r.get("status")})
    allobs = sorted(obs.values(), key=lambda o: o.get("date") or "", reverse=True)
    comp = {}
    for o in allobs:
        c = comp.setdefault(o["ticker"], {"n": 0, "houses": set(), "latest": None, "tone": None, "position": None, "summary": None, "n30": 0})
        c["n"] += 1
        if o.get("firm"): c["houses"].add(o["firm"])
        if c["latest"] is None:
            c.update(latest=o.get("date"), tone=o.get("tone"), position=o.get("position"), summary=o.get("summary"), latest_firm=o.get("firm"))
        if (o.get("date") or "") >= (TODAY - dt.timedelta(days=30)).isoformat():
            c["n30"] += 1
    for c in comp.values():
        c["houses"] = sorted(c["houses"])
    out = {"meta": {"built": dt.datetime.now().isoformat(timespec="minutes"), "n_obs": len(allobs), "reviews": len(rv),
                    "latest_review": rv[-1]["date"] if rv else None, "seed": seed.get("meta", {}).get("window_start", "") + " → " + seed.get("meta", {}).get("window_end", "")},
           "reviews": rv[-60:], "companies": comp, "observations": allobs[:800], "seed_macro": seed.get("macro", [])}
    save("desk_ledger.json", out)
    print(f"  desk_ledger: {len(allobs)} observations ({len(rv)} daily reviews + seed) · {len(comp)} names")
    return out


def breadth():
    """Live index-breadth panel (share of Nasdaq Composite / S&P 500 / Russell 2000 members ≥10/20/30/50% below their
    all-time high), built by build_market_breadth.py --rolling from the 09-29 snapshot + daily increments."""
    p = WIKI / "_data" / "market_breadth" / "latest" / "summary.json"
    incs = list((WIKI / "_data" / "market_breadth" / "increments").glob("*.json"))
    if incs and (not p.exists() or max(x.stat().st_mtime for x in incs) > p.stat().st_mtime):
        try:                                   # a newer increment than the panel → rebuild it here (~2 s, no Bloomberg call)
            import build_market_breadth
            build_market_breadth.build_rolling()
        except Exception as ex:  # noqa: BLE001
            print(f"  breadth: rolling rebuild failed ({type(ex).__name__}: {str(ex)[:100]}) — keeping the last panel")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def latest_review():
    reviews = sorted(DESK_DIR.glob("20??-??-??.json")) if DESK_DIR.exists() else []
    return json.loads(reviews[-1].read_text(encoding="utf-8")) if reviews else None


def run(force=False):
    t0 = dt.datetime.now()
    out = {"cnn": cnn_extremes(force), "bands": score_bands(force), "ss": ss_ledger(force), "daily": daily_series(force), "desk": desk_ledger(force), "review": latest_review(), "breadth": breadth()}
    print(f"  studies done in {(dt.datetime.now() - t0).total_seconds():.0f}s")
    return out


if __name__ == "__main__":
    run(force="--force" in sys.argv)
