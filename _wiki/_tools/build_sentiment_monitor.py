"""build_sentiment_monitor.py — the single SENTIMENT page (sentiment-monitor.html).

Since 2026-10-13 this one page replaces the six Sentimento cards (Felipe: "put all of this in one single
dashboard"): the old monitor, the hot/cold × bull/bear dashboard (sentiment.html, now a redirect) and the four
Codex "Sentiment Radar" pages (attention & sentiment, specialist sales, Fear & Greed extremes, narratives — the
Codex pipeline is retired; its studies were ported to sentiment_studies.py and run on the wiki caches).

Tabs
  Today            desk read (LLM daily review from the 10:00 sentiment-radar task), Bloomberg-Twitter movers
                   (daily, all of X) + own curated-corpus movers, the generated note, feed freshness.
  Names            daily stock chart (price vs QQQ, X posts, tone) with each name's HOT/BULL band, own analogs,
                   desk view and sell-side actions; weekly ranking; HOT × BULL map; own-corpus weekly explorer.
  Market mood      CNN Fear & Greed gauge + components + 12 months; SPY/QQQ next 5 sessions by band, after new
                   extreme entries (≤20/≤30, ≥70/≥80/≥90) and recent crossings; universe breadth.
  Sell-side & desks  desk-view ledger (LLM reviews + the 21-Sep Codex seed), mechanical sell-side actions ledger.
  Backtests        quadrant / turned-hot windows, HOT/BULL score bands → 5/10 sessions, own-corpus ICs, Bloomberg
                   track, weekly picks, lead/lag, earnings event windows, methodology.
  Archive          the frozen Codex pages, dated.

Inputs  _data/sentiment/* (build_sentiment.py, the 17:40 sweep, sentiment_studies.py, desk_review/*.json)
        + CNN Fear & Greed pulled live (browser headers, unverified TLS behind the proxy; fail-soft to cnn_fg.json).
Outputs _dashboards/sentiment-monitor.html · _data/sentiment/{cnn_fg,monitor}.json · monitor_note.md
stdlib only. Read-only on pages. Runs in refresh_features.py right after build_sentiment.py, and again from the
10:00 sentiment-radar task after it writes the day's desk review.
"""
from __future__ import annotations

import base64
import datetime as dt
import gzip
import html
import json
import math
import re
import ssl
import statistics
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TOOLS = Path(__file__).resolve().parent
WIKI = TOOLS.parent
DATA = WIKI / "_data" / "sentiment"
DASH = WIKI / "_dashboards"
OUT = DASH / "sentiment-monitor.html"
CNN_CACHE = DATA / "cnn_fg.json"
NOTES = DATA / "status_notes.json"
DAILY_NOTE = DATA / "daily_note.md"
FONT = WIKI / "_data" / "openrouter" / "assets" / "plus-jakarta-sans.woff2"
CNN_SEED_PAGE = DASH / "attention-sentiment" / "cnn-next-week.html"
TODAY = dt.date.today()

sys.path.insert(0, str(TOOLS))
from openrouter_presentation import CSS as OR_CSS, JS as OR_JS  # noqa: E402
import sentiment_studies  # noqa: E402

e = html.escape


def J(name):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def pct(x, d=1):
    return "–" if x is None else f"{x * 100:+.{d}f}%"


def pp(x, d=1):
    """x already in percent."""
    return "–" if x is None else f"{x:+.{d}f}%"


def d_iso(s):
    return dt.date.fromisoformat(s[:10])


def age_days(s):
    return None if not s else (TODAY - d_iso(s)).days


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def median(xs):
    xs = sorted(x for x in xs if x is not None)
    return statistics.median(xs) if xs else None


def pctile(xs, q):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return xs[f] if f == c else xs[f] + (xs[c] - xs[f]) * (k - f)


def zscores(d: dict) -> dict:
    vals = [v for v in d.values() if v is not None]
    if len(vals) < 5:
        return {k: None for k in d}
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5 or 1.0
    return {k: (None if v is None else max(-3.0, min(3.0, (v - m) / sd))) for k, v in d.items()}


def md_inline(s):
    s = e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    return s


# ----------------------------------------------------------------------------- CNN Fear & Greed
CNN_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
CNN_HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
           "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
           "Referer": "https://edition.cnn.com/markets/fear-and-greed", "Origin": "https://edition.cnn.com"}
CNN_COMPONENTS = [("market_momentum_sp500", "S&P momentum (125d)"), ("stock_price_strength", "Price strength (52w hi/lo)"),
                  ("stock_price_breadth", "Breadth (McClellan)"), ("put_call_options", "Put/call"),
                  ("market_volatility_vix", "VIX vs 50d"), ("junk_bond_demand", "Junk bond demand"),
                  ("safe_haven_demand", "Safe-haven demand")]


def cnn_rating(v):
    if v is None:
        return "–"
    return "extreme fear" if v < 25 else "fear" if v < 45 else "neutral" if v <= 55 else "greed" if v <= 75 else "extreme greed"


def seed_cnn_history(cache: dict) -> None:
    """One-off: lift the 2021→2026-09 daily F&G series out of the embedded payload of the retained Codex Fear & Greed
    page (the live endpoint only returns ~13 months). Kept as a fallback for a lost cache."""
    if cache.get("history") and min(cache["history"]) <= "2021-03-01":
        return
    if not CNN_SEED_PAGE.exists():
        return
    try:
        t = CNN_SEED_PAGE.read_text(encoding="utf-8", errors="replace")
        big = max(re.findall(r"<script[^>]*>(.*?)</script>", t, re.S), key=len)
        m = re.search(r'atob\("([A-Za-z0-9+/=]+)"\)', big)
        j = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode("utf-8"))
        hist = cache.setdefault("history", {})
        for o in j["observations"]["SPY"]["close"]:
            hist.setdefault(o["date"], round(o["fg"], 2))
        cache["seeded_from"] = CNN_SEED_PAGE.name
        print(f"  cnn: seeded history from {CNN_SEED_PAGE.name}")
    except Exception as ex:  # noqa: BLE001
        print(f"  cnn: seed skipped ({type(ex).__name__}: {str(ex)[:80]})")


def fetch_cnn(cache: dict) -> tuple[dict, str]:
    """Pull the live index + ~13 months of history; merge into the cache. Returns (cache, status)."""
    start = (TODAY - dt.timedelta(days=400)).isoformat()
    try:
        req = urllib.request.Request(CNN_URL + start, headers=CNN_HDR)
        with urllib.request.urlopen(req, timeout=20, context=ssl._create_unverified_context()) as r:
            j = json.loads(r.read().decode("utf-8"))
        fg = j["fear_and_greed"]
        hist = cache.setdefault("history", {})
        for p in j.get("fear_and_greed_historical", {}).get("data", []):
            d = dt.datetime.fromtimestamp(p["x"] / 1000, dt.timezone.utc).date().isoformat()
            hist[d] = round(float(p["y"]), 2)
        hist[TODAY.isoformat()] = round(float(fg["score"]), 2)
        cache["now"] = {"score": round(float(fg["score"]), 2), "rating": fg.get("rating"), "prev_close": fg.get("previous_close"),
                        "prev_1w": fg.get("previous_1_week"), "prev_1m": fg.get("previous_1_month"), "prev_1y": fg.get("previous_1_year"),
                        "timestamp": fg.get("timestamp")}
        cache["components"] = {k: {"score": j[k].get("score"), "rating": j[k].get("rating")} for k, _ in CNN_COMPONENTS if k in j}
        cache["fetched_at"] = dt.datetime.now().isoformat(timespec="minutes")
        cache["asof"] = TODAY.isoformat()
        cache.pop("study", None)                    # the 5-session study now lives in cnn_extremes.json (rebuilt daily)
        return cache, "live"
    except Exception as ex:  # noqa: BLE001
        return cache, f"cache ({type(ex).__name__}: {str(ex)[:60]})"


# ----------------------------------------------------------------------------- SVG helpers
def svg_gauge(v, w=260):
    cx, cy, R = w / 2, w / 2 - 10, w / 2 - 22
    segs = [(0, 25, "var(--crit)"), (25, 45, "color-mix(in srgb,var(--crit) 55%,var(--s4))"), (45, 55, "var(--base)"),
            (55, 75, "color-mix(in srgb,var(--good) 55%,var(--s4))"), (75, 100, "var(--good)")]
    def pt(val, rad):
        a = math.pi * (1 - val / 100)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)
    s = [f"<svg viewBox='0 0 {w} {w/2+18}' width='{w}' height='{w/2+18}' role='img' aria-label='Fear and Greed gauge'>"]
    for lo, hi, col in segs:
        x0, y0 = pt(lo, R); x1, y1 = pt(hi, R)
        s.append(f"<path d='M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}' fill='none' stroke='{col}' stroke-width='16' opacity='.85'/>")
    if v is not None:
        x, y = pt(v, R - 4)
        s.append(f"<line x1='{cx}' y1='{cy}' x2='{x:.1f}' y2='{y:.1f}' stroke='var(--ink)' stroke-width='3' stroke-linecap='round'/>")
        s.append(f"<circle cx='{cx}' cy='{cy}' r='5' fill='var(--ink)'/>")
    for val in (0, 25, 50, 75, 100):
        x, y = pt(val, R + 18)
        s.append(f"<text x='{x:.1f}' y='{y + 4:.1f}' font-size='10' text-anchor='middle' fill='var(--muted)'>{val}</text>")
    s.append(f"<text x='{cx}' y='{cy - 14}' font-size='30' font-weight='650' text-anchor='middle' fill='var(--ink)'>{'–' if v is None else f'{v:.0f}'}</text>")
    s.append(f"<text x='{cx}' y='{cy + 4}' font-size='11' text-anchor='middle' fill='var(--muted)' style='text-transform:uppercase;letter-spacing:.8px'>{e(cnn_rating(v))}</text>")
    s.append("</svg>")
    return "".join(s)


def svg_strip(series, w=640, h=120):
    if not series:
        return ""
    ml, mr, mt, mb = 28, 8, 8, 20
    W, H = w - ml - mr, h - mt - mb
    n = len(series)
    X = lambda i: ml + (i / max(1, n - 1)) * W
    Y = lambda v: mt + (1 - v / 100) * H
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' preserveAspectRatio='none' class='strip'>"]
    s.append(f"<rect x='{ml}' y='{Y(100)}' width='{W}' height='{Y(70)-Y(100)}' fill='var(--good)' opacity='.08'/>")
    s.append(f"<rect x='{ml}' y='{Y(30)}' width='{W}' height='{Y(0)-Y(30)}' fill='var(--crit)' opacity='.08'/>")
    for lv in (30, 50, 70):
        s.append(f"<line x1='{ml}' x2='{ml+W}' y1='{Y(lv)}' y2='{Y(lv)}' stroke='var(--grid)' stroke-dasharray='3 4'/>")
        s.append(f"<text x='{ml-4}' y='{Y(lv)+3}' font-size='9' text-anchor='end' fill='var(--muted)'>{lv}</text>")
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(series))
    s.append(f"<polyline points='{pts}' fill='none' stroke='var(--s1)' stroke-width='1.8' vector-effect='non-scaling-stroke'/>")
    s.append(f"<circle cx='{X(n-1):.1f}' cy='{Y(series[-1][1]):.1f}' r='3.5' fill='var(--s1)'/>")
    for i in range(0, n, max(1, n // 6)):
        s.append(f"<text x='{X(i):.1f}' y='{h-6}' font-size='9' text-anchor='middle' fill='var(--muted)'>{series[i][0][:7]}</text>")
    s.append("</svg>")
    return "".join(s)


def svg_spark(vals, w=120, h=28, color="var(--s1)"):
    vals = [v or 0 for v in vals]
    if not vals or max(vals) <= 0:
        return f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}'></svg>"
    mx = max(vals); n = len(vals)
    pts = " ".join(f"{(i/(max(1,n-1)))*w:.1f},{h - (v/mx)*(h-3) - 1:.1f}" for i, v in enumerate(vals))
    return (f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}' class='spark'><polyline points='{pts}' fill='none' stroke='{color}' stroke-width='1.5'/>"
            f"<circle cx='{w:.1f}' cy='{h - (vals[-1]/mx)*(h-3) - 1:.1f}' r='2.2' fill='{color}'/></svg>")


BREADTH_COLORS = ["color-mix(in srgb,var(--s1) 38%,var(--surf))", "color-mix(in srgb,var(--s1) 62%,var(--surf))",
                  "color-mix(in srgb,var(--s1) 82%,var(--surf))", "var(--s1)"]     # sequential: ≥10 → ≥50% below ATH


def svg_breadth(points, lo, hi, w=420, h=190):
    """Change in the share of members ≥10/20/30/50% below their all-time high since the baseline (pp), one line per
    threshold, shared y-range across the three indices (levels sit 17–92% apart, so a level chart is flat)."""
    ml, mr, mt, mb = 38, 66, 10, 22
    W, H = w - ml - mr, h - mt - mb
    n = len(points)
    X = lambda i: ml + (i / max(1, n - 1)) * W
    Y = lambda v: mt + (hi - v) / ((hi - lo) or 1) * H
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' role='img' aria-label='Change in the share of members below their all-time high'>"]
    step = 1 if hi - lo <= 8 else 2 if hi - lo <= 16 else 5
    for v in range(int(math.ceil(lo / step) * step), int(math.floor(hi)) + 1, step):
        s.append(f"<line x1='{ml}' x2='{ml+W}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='{'var(--base)' if v == 0 else 'var(--grid)'}'/>"
                 f"<text x='{ml-5}' y='{Y(v)+3:.1f}' font-size='9.5' text-anchor='end' fill='var(--muted)'>{v:+d}</text>")
    base = points[0]["pct"]
    labels = []
    for k in range(4):
        pts = " ".join(f"{X(i):.1f},{Y(p['pct'][k] - base[k]):.1f}" for i, p in enumerate(points))
        s.append(f"<polyline points='{pts}' fill='none' stroke='{BREADTH_COLORS[k]}' stroke-width='{1.6 + 0.3 * k:.1f}'/>")
        last = points[-1]["pct"][k] - base[k]
        labels.append([Y(last) + 3.5, f"≥{(10, 20, 30, 50)[k]} {last:+.1f}", k])
    labels.sort()                                   # end labels: keep ≥10 px apart so close lines stay readable
    for a in range(1, len(labels)):
        labels[a][0] = max(labels[a][0], labels[a - 1][0] + 10)
    over = labels[-1][0] - (mt + H + 3)
    if over > 0:
        for lab in labels: lab[0] -= over
    for y, txt, k in labels:
        s.append(f"<text x='{ml+W+4}' y='{y:.1f}' font-size='9.5' fill='var(--ink2)'><tspan fill='{BREADTH_COLORS[k]}'>■</tspan> {txt}</text>")
    for i in sorted({0, n // 2, n - 1}):
        s.append(f"<text x='{X(i):.1f}' y='{h-6}' font-size='9.5' text-anchor='{'start' if i == 0 else 'end' if i == n - 1 else 'middle'}' fill='var(--muted)'>{points[i]['date'][5:]}</text>")
    for i, p in enumerate(points):
        tip = " · ".join(f"≥{t}% {p['pct'][k]:.1f}% ({p['counts'][k]:,}, {p['pct'][k] - base[k]:+.1f} pp)" for k, t in enumerate((10, 20, 30, 50)))
        s.append(f"<rect x='{X(i) - W / max(1, n - 1) / 2:.1f}' y='{mt}' width='{W / max(1, n - 1):.1f}' height='{H}' fill='transparent'><title>{p['date']} · {tip}{' · ' + str(p['carried']) + ' carried prices' if p['carried'] else ''}</title></rect>")
    s.append("</svg>")
    return "".join(s)


def svg_band_bars(rows, current, w=640, h=170, label="SPY"):
    """rows = [(centre, stats)] from cnn_extremes all_<c>; bars = mean next-5-session return, label = mean · % up."""
    ml, mr, mt, mb = 40, 8, 14, 34
    W, H = w - ml - mr, h - mt - mb
    vals = [b["mean"] for _, b in rows if b and b.get("n", 0) >= 10]
    if not vals:
        return ""
    vmax = max(abs(v) for v in vals) or 1
    n = len(rows); bw = W / n; Y0 = mt + H / 2
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' class='bands'>",
         f"<line x1='{ml}' x2='{ml+W}' y1='{Y0}' y2='{Y0}' stroke='var(--grid)'/>"]
    for i, (c, b) in enumerate(rows):
        x = ml + i * bw
        if b and b.get("n", 0) >= 10:
            hgt = (b["mean"] / vmax) * (H / 2 - 6)
            col = "var(--s1)" if b["mean"] >= 0 else "var(--crit)"
            y = Y0 - hgt if hgt > 0 else Y0
            s.append(f"<rect x='{x+6:.1f}' y='{y:.1f}' width='{bw-12:.1f}' height='{abs(hgt):.1f}' fill='{col}' opacity='{'1' if c == current else '.45'}' rx='2'><title>F&amp;G {c} (±5) · n={b['n']} · mean {b['mean']:+.2f}% · up {b['pos']:.0f}%</title></rect>")
            s.append(f"<text x='{x+bw/2:.1f}' y='{(y-4) if hgt>0 else (y+abs(hgt)+11):.1f}' font-size='9.5' text-anchor='middle' fill='var(--ink2)'>{b['mean']:+.1f}% · {b['pos']:.0f}%</text>")
        elif b and b.get("n"):
            s.append(f"<text x='{x+bw/2:.1f}' y='{Y0-4:.1f}' font-size='9' text-anchor='middle' fill='var(--muted)'>n={b['n']}</text>")
        if c == current:
            s.append(f"<rect x='{x+1:.1f}' y='{mt}' width='{bw-2:.1f}' height='{H}' fill='none' stroke='var(--accent)' stroke-dasharray='3 3'/>")
        s.append(f"<text x='{x+bw/2:.1f}' y='{h-18}' font-size='10' text-anchor='middle' fill='var(--muted)'>{c}</text>")
    s.append(f"<text x='{ml}' y='{h-4}' font-size='9.5' fill='var(--muted)'>bars: mean {label} return over the next 5 sessions, every reading in the band (overlapping) · label: mean · % up · dashed: today's band · bands under 10 readings not drawn</text></svg>")
    return "".join(s)


def hbar(v, vmax, color):
    wpct = 0 if vmax == 0 else min(100, abs(v) / vmax * 100)
    return f"<span class='hb'><i style='width:{wpct:.0f}%;background:{color}'></i></span>"


def tk_link(t):
    return f"<a class='tkl' href='#names' data-tk='{e(t)}'>{e(t)}</a>"


# ----------------------------------------------------------------------------- main
def main() -> int:
    pw = J("panel_weekly.json"); pl = J("panel_long.json"); td = J("tweet_daily.json"); sd = J("sellside_daily.json"); bh = J("bbg_history.json")
    if not pw:
        print("[WARN] panel_weekly.json missing — nothing to build"); return 1
    names = pw.get("names", {})
    notes = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}

    # ---- CNN (live, cached) then the studies (CNN extremes need today's reading) ----
    cache = json.loads(CNN_CACHE.read_text(encoding="utf-8")) if CNN_CACHE.exists() else {}
    seed_cnn_history(cache)
    cache, cnn_status = fetch_cnn(cache)
    CNN_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    now = cache.get("now", {}); fg = now.get("score")
    hist = sorted(cache.get("history", {}).items())
    strip = [(d, v) for d, v in hist if d >= (TODAY - dt.timedelta(days=365)).isoformat()]
    cnn_through = hist[-1][0] if hist else None
    S = sentiment_studies.run()
    cx, sb, ssl_, ds, desk, review = S["cnn"], S["bands"], S["ss"], S["daily"], S["desk"], S["review"]

    def cnn_g(tk, mode, key):
        return (((cx or {}).get("results", {}).get(tk, {}).get(mode, {}) or {}).get("groups", {}) or {}).get(key)
    cur_band = sentiment_studies.cnn_band(fg) if fg is not None else None
    cur_stats = cnn_g("SPY", "close", f"all_{cur_band}") if cur_band is not None else None
    cur_stats_q = cnn_g("QQQ", "close", f"all_{cur_band}") if cur_band is not None else None
    fear_x, greed_x = cnn_g("SPY", "close", "cross_30"), cnn_g("SPY", "close", "cross_70")
    recent_x = (cx or {}).get("recent", {}).get("SPY", [])
    recent_xq = {r["date"] + str(r["th"]): r for r in (cx or {}).get("recent", {}).get("QQQ", [])}

    # ---- universe breadth (latest weekly panel) ----
    wk = pw["weeks"][-1]; row = pw["panel"][wk]
    n_names = len(row)
    def share(cond):
        xs = [x for x in (cond(r) for r in row.values()) if x is not None]
        return (sum(xs) / len(xs), len(xs)) if xs else (None, 0)
    eps_up, _ = share(lambda r: None if r.get("eps_rev") is None else (1 if r["eps_rev"] > 0.002 else 0))
    eps_dn, _ = share(lambda r: None if r.get("eps_rev") is None else (1 if r["eps_rev"] < -0.002 else 0))
    rat_up, _ = share(lambda r: None if r.get("rating") is None else (1 if r["rating"] > 0 else 0))
    tone_bull, tone_n = share(lambda r: None if not (r.get("bull", 0) + r.get("bear", 0)) else (1 if r["bull"] > r["bear"] else 0))
    ss_up = sum(1 for r in row.values() if (r.get("ss_act") or 0) > 0); ss_dn = sum(1 for r in row.values() if (r.get("ss_act") or 0) < 0)
    ss_pt_up = sum(1 for r in row.values() if (r.get("ss_pt") or 0) > 0); ss_pt_dn = sum(1 for r in row.values() if (r.get("ss_pt") or 0) < 0)
    px_up4 = share(lambda r: None if r.get("ret_m4w") is None else (1 if r["ret_m4w"] > 0 else 0))[0]

    # ---- freshness ----
    tw_through = max((max(v) for v in td["tickers"].values() if v), default=None) if td else None
    ss_through = max((max(v) for v in sd["tickers"].values() if v), default=None) if sd else None
    px_through = max((max(s["PX_LAST"]) for s in bh["series"].values() if s.get("PX_LAST")), default=None) if bh else None
    bx_through = (ds or {}).get("meta", {}).get("movers_through")
    rv_date = (review or {}).get("date")
    tw_age, ss_age, px_age, cnn_age, bx_age, rv_age = (age_days(x) for x in (tw_through, ss_through, px_through, cnn_through, bx_through, rv_date))
    tweets_fresh = tw_age is not None and tw_age <= 4

    # ---- own-corpus movers (curated handles, tweets.sqlite) ----
    movers_rows = []
    if td and tw_through:
        D = d_iso(tw_through)
        def window_sum(days, a, b, key="m_cur"):
            return sum((r.get(key, 0) or 0) for dstr, r in days.items() if a <= d_iso(dstr) <= b)
        def mom(days, end):
            a7 = window_sum(days, end - dt.timedelta(days=6), end) / 7
            b28 = window_sum(days, end - dt.timedelta(days=34), end - dt.timedelta(days=7)) / 28
            return (a7, b28, math.log((a7 + 0.2) / (b28 + 0.2)))
        cur, prev, meta = {}, {}, {}
        for t, days in td["tickers"].items():
            a7, b28, m1 = mom(days, D)
            if a7 + b28 <= 0:
                continue
            cur[t] = m1; prev[t] = mom(days, D - dt.timedelta(days=7))[2]
            bull = window_sum(days, D - dt.timedelta(days=6), D, "bull"); bear = window_sum(days, D - dt.timedelta(days=6), D, "bear")
            spark = [window_sum(days, D - dt.timedelta(days=k), D - dt.timedelta(days=k)) for k in range(34, -1, -1)]
            meta[t] = {"a7": a7, "b28": b28, "bull": bull, "bear": bear, "spark": spark}
        zc, zp = zscores(cur), zscores(prev)
        px = (bh or {}).get("series", {})
        def ret(t, end, k):
            s = px.get(t, {}).get("PX_LAST", {})
            ds_ = sorted(s)
            def last_on(dd):
                c = [x for x in ds_ if x <= dd.isoformat()]
                return s[c[-1]] if c else None
            p1, p0 = last_on(end), last_on(end - dt.timedelta(days=k))
            return None if not (p1 and p0) else p1 / p0 - 1
        for t in cur:
            if zc.get(t) is None or zp.get(t) is None:
                continue
            m = meta[t]
            movers_rows.append({"t": t, "name": names.get(t, t), "z": zc[t], "dz": zc[t] - zp[t], "a7": m["a7"], "b28": m["b28"],
                                "tone": (m["bull"] / (m["bull"] + m["bear"])) if (m["bull"] + m["bear"]) >= 3 else None,
                                "r7": ret(t, D, 7), "r28": ret(t, D, 28), "spark": m["spark"]})
    eligible = [r for r in movers_rows if max(r["a7"], r["b28"]) >= 1.5]
    rising = sorted([r for r in eligible if r["dz"] > 0], key=lambda r: -r["dz"])[:8]
    falling = sorted([r for r in eligible if r["dz"] < 0], key=lambda r: r["dz"])[:8]

    # ---- Bloomberg-Twitter movers (all of X, daily; fresh while the Terminal is up) ----
    bm = (ds or {}).get("movers", [])
    b_rise = sorted([r for r in bm if (r["dz"] or 0) > 0], key=lambda r: -r["dz"])[:8]
    b_fall = sorted([r for r in bm if (r["dz"] or 0) < 0], key=lambda r: r["dz"])[:8]
    b_tup = sorted([r for r in bm if r.get("dtone") is not None and r["dtone"] > 0], key=lambda r: -r["dtone"])[:5]
    b_tdn = sorted([r for r in bm if r.get("dtone") is not None and r["dtone"] < 0], key=lambda r: r["dtone"])[:5]
    dtk = (ds or {}).get("tickers", {}); ddates = (ds or {}).get("dates", [])
    def bspark(t, n=35):
        return [v for v in (dtk.get(t, {}).get("tw") or [])[-n:]]

    # ---- windows: quadrant forward returns + turned hot / cold (Bloomberg track) ----
    src = pl if pl else pw
    quad = src.get("quadrants", {})
    span = (src["weeks"][0], src["weeks"][-1]) if src.get("weeks") else ("", "")
    def transitions(panel, weeks):
        hot_ev, cold_ev = {"1w": [], "15d": [], "4w": []}, {"1w": [], "15d": [], "4w": []}
        for w0, w1 in zip(weeks[:-1], weeks[1:]):
            r0, r1 = panel.get(w0, {}), panel.get(w1, {})
            h0 = [r["HOT"] for r in r0.values() if r.get("HOT") is not None]; h1 = [r["HOT"] for r in r1.values() if r.get("HOT") is not None]
            if len(h0) < 20 or len(h1) < 20:
                continue
            m0, p80, p20 = median(h0), pctile(h1, 0.8), pctile(h1, 0.2)
            for t, r in r1.items():
                a, b = r0.get(t, {}).get("HOT"), r.get("HOT")
                if a is None or b is None:
                    continue
                for cond, ev in ((a < m0 and b >= p80, hot_ev), (a >= m0 and b <= p20, cold_ev)):
                    if cond:
                        for h in ev:
                            v = r.get(f"rel_ret_{h}")
                            if v is not None: ev[h].append(v)
        st = lambda xs: None if len(xs) < 8 else {"n": len(xs), "mean": mean(xs), "median": median(xs), "hit": sum(1 for v in xs if v > 0) / len(xs), "p25": pctile(xs, .25), "p75": pctile(xs, .75)}
        return {h: st(v) for h, v in hot_ev.items()}, {h: st(v) for h, v in cold_ev.items()}
    turned_hot, turned_cold = transitions(src["panel"], src["weeks"])

    # ---- score bands for the names on today's lists ----
    comp_b = (sb or {}).get("companies", {})
    def analog(t, fam="HOT", h=5):
        c = comp_b.get(t, {}).get(fam) or {}
        o = next((x for x in c.get("own", []) if x["h"] == h), None)
        return c.get("score"), c.get("band"), o
    BANDL = (sb or {}).get("meta", {}).get("bands", ["0–<20", "20–<40", "40–<60", "60–<80", "80–100"])

    # ---- daily note (generated) ----
    note = []
    if fg is not None:
        d1w, d1m = now.get("prev_1w"), now.get("prev_1m")
        move = f" — {('up' if fg >= d1w else 'down')} from {d1w:.0f} a week ago and {d1m:.0f} a month ago ({cnn_rating(d1m)})" if d1w is not None and d1m is not None else ""
        note.append(f"**Market mood.** CNN Fear & Greed is at **{fg:.0f} ({cnn_rating(fg)})**{move}.")
        if cur_stats and cur_stats_q and cur_stats.get("n"):
            note.append(f"Since 2021, readings in the {cur_band} band (±5) were followed by SPY **{cur_stats['mean']:+.2f}%** over five sessions (up {cur_stats['pos']:.0f}% of the time, "
                        f"n={cur_stats['n']} overlapping readings; QQQ {cur_stats_q['mean']:+.2f}% / {cur_stats_q['pos']:.0f}%).")
        last_x = recent_x[-1] if recent_x else None
        if last_x:
            note.append(f"Last extreme crossing: {'down to' if last_x['dir'] == 'down' else 'up to'} {'≤' if last_x['dir'] == 'down' else '≥'}{last_x['th']} on {last_x['date']} (F&G {last_x['fg']:.0f}); "
                        + (f"SPY {last_x['ret']:+.2f}% over the next five sessions." if last_x.get("ret") is not None else f"its five-session window matures {last_x.get('matures') or 'after the next sessions'}."))
    if b_rise:
        def bmv(r):
            bits = [f"**{r['t']}** ({r['dz']:+.1f}σ, {r['a7']:.0f} posts/day vs {r['b28']:.0f})"]
            if r.get("r7") is not None: bits.append(f"stock {pct(r['r7'])} over the week")
            return " · ".join(bits)
        note.append(f"**Getting hotter on X (Bloomberg all-of-X count, 7 days vs the prior 4 weeks, through {bx_through}).** " + "; ".join(bmv(r) for r in b_rise[:5]) + ".")
        note.append("**Cooling off.** " + "; ".join(bmv(r) for r in b_fall[:5]) + ".")
    if not tweets_fresh and tw_through:
        note.append(f"The curated-handle X corpus stops on {tw_through} ({tw_age} days ago); the own-corpus HOT axis and movers are frozen until it resumes.")
    note.append(f"**Universe breadth (week ending {wk}, {n_names} names).** EPS revisions up for {eps_up*100:.0f}% and down for {eps_dn*100:.0f}%; "
                f"rating drift positive for {rat_up*100:.0f}%; {px_up4*100:.0f}% of names up over 4 weeks. Sell-side: {ss_up} names with net upgrades vs {ss_dn} with net downgrades, "
                f"PT raises in {ss_pt_up} vs cuts in {ss_pt_dn}" + (f" (mail through {ss_through}, {ss_age} days old — stale)." if ss_age and ss_age > 7 else "."))
    th15, tc15 = turned_hot.get("15d"), turned_cold.get("15d")
    if th15 and tc15:
        note.append(f"**What history says (Bloomberg track, {span[0]} → {span[1]}).** Names that *turned hot* returned **{th15['mean']*100:+.1f}%** universe-relative over 15 days "
                    f"(positive {th15['hit']*100:.0f}%, n={th15['n']}); *turned cold* {tc15['mean']*100:+.1f}% (positive {tc15['hit']*100:.0f}%, n={tc15['n']}). "
                    "Attention says where the crowd is, not where the stock goes next.")
    note_md = "\n\n".join(note)
    extra_note = DAILY_NOTE.read_text(encoding="utf-8").strip() if DAILY_NOTE.exists() else ""
    extra_age = age_days(dt.datetime.fromtimestamp(DAILY_NOTE.stat().st_mtime).date().isoformat()) if DAILY_NOTE.exists() else None

    # ---- outputs: numbers + note (monitor.json also feeds the Sentiment Radar e-mail) ----
    def slim(rs):
        return [{k: v for k, v in r.items() if k != "spark"} for r in rs]
    watch = []
    for r in (review or {}).get("up", []) + (review or {}).get("down", []):
        if r.get("ticker"): watch.append(r["ticker"])
    for r in b_rise[:5] + b_fall[:5]:
        if r["t"] not in watch: watch.append(r["t"])
    analogs = {}
    for t in watch:
        a = {}
        for fam in ("HOT", "BULL"):
            sc, bd, o5 = analog(t, fam, 5); _, _, o10 = analog(t, fam, 10)
            a[fam] = {"score": sc, "band": None if bd is None else BANDL[bd], "h5": o5, "h10": o10}
        analogs[t] = a
    (DATA / "monitor_note.md").write_text(f"== SENTIMENT MONITOR · {TODAY.isoformat()} ==\n\n{note_md}\n", encoding="utf-8")
    (DATA / "monitor.json").write_text(json.dumps({
        "asof": TODAY.isoformat(), "built": dt.datetime.now().isoformat(timespec="minutes"),
        "cnn": {"now": now, "components": cache.get("components", {}), "status": cnn_status, "through": cnn_through, "band": cur_band, "band_stats_spy": cur_stats,
                "band_stats_qqq": cur_stats_q, "cross_30_spy": {k: v for k, v in (fear_x or {}).items() if k != "events"}, "cross_70_spy": {k: v for k, v in (greed_x or {}).items() if k != "events"},
                "recent_crossings": recent_x[-6:], "zone": (cx or {}).get("current", {}).get("zone")},
        "breadth": {"week": wk, "n": n_names, "eps_up": eps_up, "eps_dn": eps_dn, "rating_up": rat_up, "tone_bull": tone_bull, "tone_n": tone_n, "ss_up": ss_up, "ss_dn": ss_dn, "ss_pt_up": ss_pt_up, "ss_pt_dn": ss_pt_dn, "px_up4w": px_up4},
        "movers": {"through": tw_through, "fresh": tweets_fresh, "rising": slim(rising), "falling": slim(falling)},
        "bbg_movers": {"through": bx_through, "rising": b_rise, "falling": b_fall, "tone_up": b_tup, "tone_down": b_tdn},
        "analogs": analogs, "analog_meta": {"track": (sb or {}).get("meta", {}).get("track"), "week": (sb or {}).get("meta", {}).get("week")},
        "windows": {"span": span, "quadrants": quad, "turned_hot": turned_hot, "turned_cold": turned_cold},
        "ss_ledger": {"through": (ssl_ or {}).get("meta", {}).get("through")},
        "desk": {"latest_review": rv_date, "n_obs": (desk or {}).get("meta", {}).get("n_obs")},
        "breadth": {"asof": (S.get("breadth") or {}).get("asof"), "baseline": (S.get("breadth") or {}).get("baseline"),
                    "indices": [{"label": x["label"], "pct": x["points"][-1]["pct"], "lookback": x.get("lookback"), "covered": x["covered"], "universe": x["universe"]} for x in (S.get("breadth") or {}).get("indices", [])]},
        "freshness": {"tweets": tw_through, "sellside": ss_through, "prices": px_through, "cnn": cnn_through, "panel": pw.get("asof"), "bbg_twitter": bx_through, "desk_review": rv_date, "breadth": (S.get("breadth") or {}).get("asof")},
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- the hot/cold × bull/bear sections (ranking, map, backtests …) ----
    import build_sentiment
    from _sentiment_dash import render_parts, JS as SX_JS, RANKING_CSS
    parts = render_parts(*build_sentiment.dash_inputs())

    # =========================================================================== HTML
    def fresh_cls(a, warn=3, bad=7):
        return "ok" if a is not None and a <= warn else ("warn" if a is not None and a <= bad else "bad")
    def stale(a, what, limit=4):
        return f" <span class='stale-tag'>⚠ {e(what)} {a} days old</span>" if a is not None and a > limit else ""
    def head(kicker, title, sub=""):
        return f"<p class='oc-kicker'>{kicker}</p><h2 class='oc-headline'>{title}</h2>" + (f"<p class='oc-sub'>{sub}</p>" if sub else "")

    # ---------------- TODAY
    def card_item(r, side):
        t = r.get("ticker", "")
        ev = ", ".join(e(x) for x in (r.get("evidence") or [])[:4])
        return (f"<div class='dcard {side}'><div class='dh'>{tk_link(t)}<span class='sig'>{e(r.get('signal') or '')}</span>"
                f"<span class='conv'>{e(r.get('conviction') or '')}</span></div><p>{md_inline(r.get('why') or '')}</p>"
                + (f"<p class='cw'><b>Confirms:</b> {md_inline(r['confirm'])}</p>" if r.get("confirm") else "")
                + (f"<p class='cw'><b>Weakens:</b> {md_inline(r['weaken'])}</p>" if r.get("weaken") else "")
                + (f"<p class='evid'>evidence {ev}</p>" if ev else "") + "</div>")
    if review:
        mw = review.get("mail_window") or {}
        desk_read = (
            "<section class='oc mon' id='desk-read'>"
            + head("01 · desk read · Claude daily review of specialist sales, priority authors and the numbers below",
                   md_inline(review.get("headline") or f"Desk review {rv_date}") + stale(rv_age, "review", 1),
                   f"Review of {e(rv_date or '–')} · status {e(review.get('status') or '–')} · mail {e(mw.get('channel') or '–')} "
                   f"{e((mw.get('from_utc') or '')[:16])} → {e((mw.get('to_utc') or '')[:16])} UTC · {mw.get('screened', '–')} screened · {mw.get('read', '–')} read · "
                   f"newest received {e((mw.get('newest_received_utc') or '–')[:16])}")
            + (f"<div class='card note-card'><p>{md_inline(review.get('market_read') or '')}</p></div>" if review.get("market_read") else "")
            + "<div class='grid2'>"
            + f"<div><h3>Rising attention / crowding</h3>{''.join(card_item(r, 'up') for r in review.get('up', [])) or '<p class=note>None with enough support today.</p>'}</div>"
            + f"<div><h3>Easing crowding / weakening sentiment</h3>{''.join(card_item(r, 'down') for r in review.get('down', [])) or '<p class=note>None with enough support today.</p>'}</div>"
            + "</div>"
            + ("<h3>Themes and quality-source notes</h3><div class='card note-card'>" + "".join(f"<p><b>{e(th.get('title') or '')}.</b> {md_inline(th.get('text') or '')}</p>" for th in review.get("themes", [])) + "</div>" if review.get("themes") else "")
            + ("<p class='note'><b>Coverage gaps:</b> " + " · ".join(e(x) for x in review.get("coverage_gaps", [])) + "</p>" if review.get("coverage_gaps") else "")
            + ("<p class='note'><b>Sources:</b> " + " · ".join(e(x) for x in review.get("source_notes", [])) + "</p>" if review.get("source_notes") else "")
            + "</section>")
    else:
        desk_read = ("<section class='oc mon' id='desk-read'>" + head("01 · desk read", "No desk review yet",
                     "The 10:00 <code>sentiment-radar</code> task writes <code>_data/sentiment/desk_review/YYYY-MM-DD.json</code> (specialist sales, SemiAnalysis, DAMNANG) and this card renders it. "
                     "Until then the desk ledger in Sell-side &amp; desks carries the retained 07–21 Sep review.") + "</section>")

    def bm_rows(rows, color):
        vmax = max((abs(r["dz"] or 0) for r in rows), default=1) or 1
        out = []
        for r in rows:
            out.append(f"<tr><td class='tk'>{tk_link(r['t'])}<small>{e((r.get('name') or '')[:28])}</small></td><td class='bar'>{hbar(r['dz'] or 0, vmax, color)}<b>{(r['dz'] or 0):+.1f}σ</b></td>"
                       f"<td class='r'>{(r['z'] or 0):+.1f}</td><td class='r'>{r['a7']:,.0f} <small>vs {r['b28']:,.0f}</small></td>"
                       f"<td class='r'>{'–' if r.get('tone') is None else f'{r[chr(116)+chr(111)+chr(110)+chr(101)]:+.2f}'}<small>{'' if r.get('dtone') is None else f'Δ {r[chr(100)+chr(116)+chr(111)+chr(110)+chr(101)]:+.2f}'}</small></td>"
                       f"<td class='r {'pos' if (r.get('r7') or 0) >= 0 else 'neg'}'>{pct(r.get('r7'))}</td><td class='r {'pos' if (r.get('r28') or 0) >= 0 else 'neg'}'>{pct(r.get('r28'))}</td>"
                       f"<td>{svg_spark(bspark(r['t']), color=color)}</td></tr>")
        return "".join(out)
    bthead = "<thead><tr><th>Name</th><th>Δ attention (z vs a week earlier)</th><th class='r'>level z</th><th class='r'>posts/day 7d vs 4w</th><th class='r'>BBG tone 7d</th><th class='r'>stock 7d</th><th class='r'>stock 4w</th><th>35 days</th></tr></thead>"
    def mover_rows(rows, color):
        vmax = max((abs(r["dz"]) for r in rows), default=1) or 1
        return "".join(
            f"<tr><td class='tk'>{tk_link(r['t'])}<small>{e(r['name'][:28])}</small></td><td class='bar'>{hbar(r['dz'], vmax, color)}<b>{r['dz']:+.1f}σ</b></td>"
            f"<td class='r'>{r['z']:+.1f}</td><td class='r'>{r['a7']:.1f} <small>vs {r['b28']:.1f}</small></td><td class='r'>{'–' if r['tone'] is None else f'{r[chr(116)+chr(111)+chr(110)+chr(101)]*100:.0f}% bull'}</td>"
            f"<td class='r {'pos' if (r['r7'] or 0) >= 0 else 'neg'}'>{pct(r['r7'])}</td><td class='r {'pos' if (r['r28'] or 0) >= 0 else 'neg'}'>{pct(r['r28'])}</td><td>{svg_spark(r['spark'], color=color)}</td></tr>"
            for r in rows)
    othead = "<thead><tr><th>Name</th><th>Δ attention (z vs a week earlier)</th><th class='r'>HOT z</th><th class='r'>mentions/day 7d vs 4w</th><th class='r'>tone 7d</th><th class='r'>stock 7d</th><th class='r'>stock 4w</th><th>35 days</th></tr></thead>"
    own_block = (f"<div class='grid2'><div class='card'><h3>Getting hotter</h3><table class='mv'>{othead}<tbody>{mover_rows(rising, 'var(--s4)')}</tbody></table></div>"
                 f"<div class='card'><h3>Cooling off</h3><table class='mv'>{othead}<tbody>{mover_rows(falling, 'var(--s1)')}</tbody></table></div></div>")
    def tone_list(rows):
        return "".join(f"<li>{tk_link(r['t'])} <b>{r['dtone']:+.2f}</b> <span class='mut'>to {r['tone']:+.2f} · {r['a7']:,.0f} posts/day · stock 7d {pct(r.get('r7'))}</span></li>" for r in rows)
    movers = (
        "<section class='oc mon' id='movers'>"
        + head("02 · movers · who is getting hotter or colder on X", f"Bloomberg all-of-X attention through {e(bx_through or '–')}" + stale(bx_age, "Bloomberg Twitter", 4),
               "Bloomberg's daily Twitter publication count per name: 7-day average against the prior 4 weeks (log ratio, z-scored across the universe). Δ is the change in that z versus a week earlier — "
               "the names whose discussion is accelerating and the ones going quiet. Tone = Bloomberg's Twitter sentiment, 7-day mean (−1..+1), Δ vs the prior 4 weeks. Stock = price change (Bloomberg). "
               "A falling count is not negative sentiment; read it with the tone column.")
        + f"<div class='grid2'><div class='card'><h3>Getting hotter</h3><table class='mv'>{bthead}<tbody>{bm_rows(b_rise, 'var(--s4)')}</tbody></table></div>"
        f"<div class='card'><h3>Cooling off</h3><table class='mv'>{bthead}<tbody>{bm_rows(b_fall, 'var(--s1)')}</tbody></table></div></div>"
        + f"<div class='grid2'><div class='card'><h3>Tone improving (7d vs prior 4w)</h3><ul class='tl'>{tone_list(b_tup)}</ul></div><div class='card'><h3>Tone deteriorating</h3><ul class='tl'>{tone_list(b_tdn)}</ul></div></div>"
        + (f"<h3>Curated-handle corpus (tweets.sqlite) — through {e(tw_through or '–')}</h3>{own_block}" if tweets_fresh else
           f"<details class='card'><summary>Curated-handle corpus movers (tweets.sqlite) — frozen on {e(tw_through or '–')}, {tw_age} days old</summary>{own_block}</details>")
        + "</section>")

    note_sec = (
        "<section class='oc mon' id='note'>" + head("03 · the read · generated from the numbers on this page", f"The read for {TODAY.isoformat()}")
        + "<div class='card note-card'>" + "".join(f"<p>{md_inline(p)}</p>" for p in note) + "</div>"
        + (f"<h3>Analyst note <small class='mut'>(_data/sentiment/daily_note.md, {extra_age} days old)</small></h3><div class='card note-card extra'>" + "".join(f"<p>{md_inline(p)}</p>" for p in extra_note.split('\n\n')) + "</div>" if extra_note else "")
        + "</section>")

    def src_row(label, through, age, note_key, desc, warn=3, bad=7):
        cls = fresh_cls(age, warn, bad)
        n = notes.get(note_key, "")
        return (f"<tr><td><span class='dot {cls}'></span>{e(label)}</td><td class='r'>{e(through or '–')}</td><td class='r'>{'–' if age is None else f'{age} d'}</td><td>{e(desc)}" + (f"<br><b class='{cls}'>{e(n)}</b>" if n else "") + "</td></tr>")
    sources = (
        "<section class='oc mon' id='sources'>" + head("04 · sources · how fresh is each feed", "Feeds behind this page")
        + "<div class='card'><table class='src'><thead><tr><th>Feed</th><th class='r'>through</th><th class='r'>age</th><th>what it drives · status</th></tr></thead><tbody>"
        + src_row("Bloomberg Twitter / news (bdh social fields)", bx_through, bx_age, "bbg", "Today's movers, stock-chart X/tone panels, Bloomberg-track HOT/BULL, score bands · 17:40 sweep when the Terminal is logged in")
        + src_row("Bloomberg prices, BEst EPS, ratings, SI, SPY/QQQ", px_through, px_age, "bbg", "stock moves, EPS/rating breadth, Fear & Greed and score-band returns · 17:40 sweep")
        + src_row("Index breadth (Bloomberg constituents, daily increment)", (S.get("breadth") or {}).get("asof"), age_days((S.get("breadth") or {}).get("asof")), "breadth", "Market mood → index breadth · market_breadth_bbg.py --update in the 17:40 sweep and the 10:01 task (completed sessions only)")
        + src_row("CNN Fear & Greed", cnn_through, cnn_age, "cnn", f"gauge, components, extreme-entry study · pulled live at every build ({cnn_status})")
        + src_row("Desk review (Claude, 10:00 sentiment-radar task)", rv_date, rv_age, "desk", "desk read, desk-view ledger · reads specialist-sales, SemiAnalysis and DAMNANG mail since the last cutoff", 1, 3)
        + src_row("Sell-side e-mail (Outlook DASL sweep)", ss_through, ss_age, "sellside", "sell-side actions ledger, note flow, BULL sell-side legs · 17:40 sweep (refresh_sentiment.bat)")
        + src_row("Curated X corpus (tweets.sqlite, twitterapi.io)", tw_through, tw_age, "tweets", "own-corpus movers, weekly ranking HOT axis, tweet examples · 09:00 twitter-briefing task")
        + src_row("Weekly panels (build_sentiment.py)", pw.get("asof"), age_days(pw.get("asof")), "panel", "ranking, map, quadrants, backtests · 18:15 chain")
        + "</tbody></table></div></section>")
    tab_today = desk_read + movers + note_sec + sources

    # ---------------- NAMES
    tab_names = (
        "<section class='oc mon' id='stock'>" + head("01 · one name, daily", "Stock chart — price, X discussion and tone",
            "Price rebased to 100 at the start of the window against QQQ; Bloomberg's daily all-of-X post count (bars, 7-day average line) with the curated-handle mentions (orange, own axis); "
            "Bloomberg Twitter and news sentiment as 7-day means. The strip above the chart is everything else the page knows about the name: HOT/BULL band and the name's own history in that band, "
            "the latest desk view and the sell-side actions of the last 30 days of mail.")
        + "<div class='card'><div class='dc-bar'><select id='dc_tk' aria-label='Ticker'></select><span id='dc_ranges' class='seg'>"
        + "".join(f"<button type='button' data-r='{r}'{' class=on' if r == 90 else ''}>{lab}</button>" for r, lab in ((30, '1M'), (90, '3M'), (180, '6M'), (365, '1Y')))
        + "</span></div><div id='dc_info' class='dc-info'></div><div id='dc_chart' class='dc-chart'></div><div id='dc_read' class='dc-read'></div></div>"
        + "</section>"
        + "<div class='sx'>" + parts["ranking"] + parts["map"]
        + parts["ticker"].replace("<section><h2>Ticker explorer — <select id=\"tk\"></select></h2>",
                                  "<section><h2>Curated-handle corpus, weekly — <select id=\"tk\" aria-label='Ticker (weekly)'></select></h2><div class='note'>Own tweet corpus (≈440 handles): weekly mentions, lexicon tone and the highest-engagement tweets. Follows the stock chart's ticker.</div>")
        + "</div>")

    # ---------------- MARKET MOOD
    comp_tiles = "".join(
        f"<div class='ctile'><div class='l'>{e(lab)}</div><div class='v {e((cache.get('components', {}).get(k, {}).get('rating') or '').replace(' ', '-'))}'>{e(cache.get('components', {}).get(k, {}).get('rating') or '–')}</div></div>"
        for k, lab in CNN_COMPONENTS)
    def stat_tile(label, st, sub=""):
        if not st or not st.get("n"):
            return f"<div class='oc-tile'><div class='l'>{e(label)}</div><div class='v'>–</div><div class='s'>{e(sub)}</div></div>"
        ci = st.get("mean_ci")
        return (f"<div class='oc-tile'><div class='l'>{e(label)}</div><div class='v {'pos' if st['mean']>=0 else 'neg'}'>{st['mean']:+.2f}%</div>"
                f"<div class='s'>up {st['pos']:.0f}% · median {st['median']:+.2f}% · n={st['n']}" + (f" · 95% CI {ci[0]:+.2f} / {ci[1]:+.2f}" if ci else " · no CI (n&lt;10)")
                + (f" · {e(sub)}" if sub else "") + "</div></div>")
    def xs_table(tk, mode):
        res = (cx or {}).get("results", {}).get(tk, {}).get(mode)
        if not res:
            return "<p class='note'>Study unavailable.</p>"
        base = res["baseline"]
        years = sorted({y for g in res["groups"].values() for y in (g.get("years") or {})})
        rows = []
        for th in (20, 30, 70, 80, 90):
            g = res["groups"].get(f"cross_{th}") or {}
            lab = f"New entry {'≤' if th <= 30 else '≥'}{th} ({'fear' if th <= 30 else 'greed'})"
            if not g.get("n"):
                rows.append(f"<tr><th>{lab}</th><td colspan='{7+len(years)}' class='mut'>no crossing in the sample (max F&amp;G {(cx or {}).get('meta', {}).get('obs_max', 0):.0f})</td></tr>"); continue
            ci = g.get("mean_ci"); xci = g.get("excess_ci")
            rows.append(f"<tr><th>{lab}</th><td class='r'>{g['n']}<small>{e(g['status'])}</small></td><td class='r {'pos' if g['mean']>=0 else 'neg'}'><b>{g['mean']:+.2f}%</b></td><td class='r'>{g['median']:+.2f}%</td>"
                        f"<td class='r'>{g['pos']:.0f}%</td><td class='r'>{g['p10']:+.1f} / {g['p90']:+.1f}</td><td class='r'>{'–' if not ci else f'{ci[0]:+.2f} / {ci[1]:+.2f}'}</td>"
                        f"<td class='r'>{'–' if g.get('excess') is None else f'{g[chr(101)+chr(120)+chr(99)+chr(101)+chr(115)+chr(115)]:+.2f}'}<small>{'' if not xci else f'CI {xci[0]:+.2f}/{xci[1]:+.2f}'}</small></td>"
                        + "".join(f"<td class='r'>{'–' if (g.get('years') or {}).get(y) is None else f'{g[chr(121)+chr(101)+chr(97)+chr(114)+chr(115)][y]:+.1f}'}</td>" for y in years) + "</tr>")
        rows.append(f"<tr class='base'><th>All readings (baseline)</th><td class='r'>{base['n']}</td><td class='r'>{base['mean']:+.2f}%</td><td class='r'>{base['median']:+.2f}%</td><td class='r'>{base['pos']:.0f}%</td>"
                    f"<td class='r'>{base['p10']:+.1f} / {base['p90']:+.1f}</td><td></td><td></td>" + "".join("<td></td>" for _ in years) + "</tr>")
        return ("<table class='qd xs'><thead><tr><th></th><th class='r'>n</th><th class='r'>mean</th><th class='r'>median</th><th class='r'>% up</th><th class='r'>p10 / p90</th><th class='r'>95% CI mean</th><th class='r'>vs all (pp)</th>"
                + "".join(f"<th class='r'>{y}</th>" for y in years) + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>")
    xs_panels = "".join(f"<div data-key='{tk}|{mode}'{'' if (tk, mode) == ('SPY', 'close') else ' hidden'}>{xs_table(tk, mode)}</div>"
                        for tk in ("SPY", "QQQ", "QQQ/SPY") for mode in ("close", "delayed"))
    def ep_table(tk):
        res = (cx or {}).get("results", {}).get(tk, {}).get("close")
        if not res:
            return ""
        out = []
        for c in range(0, 101, 10):
            a, ep = res["groups"].get(f"all_{c}") or {}, res["groups"].get(f"episode_{c}") or {}
            if not a.get("n"):
                continue
            out.append(f"<tr{' class=cur' if c == cur_band else ''}><th>{c} <small>[{max(0,c-5)}, {min(100,c+5)})</small></th><td class='r'>{a['n']}</td><td class='r {'pos' if a['mean']>=0 else 'neg'}'>{a['mean']:+.2f}%</td><td class='r'>{a['pos']:.0f}%</td>"
                       f"<td class='r'>{ep.get('n', 0)}</td><td class='r'>{'–' if not ep.get('n') else f'{ep[chr(109)+chr(101)+chr(97)+chr(110)]:+.2f}%'}</td><td class='r'>{'–' if not ep.get('n') else f'{ep[chr(112)+chr(111)+chr(115)]:.0f}%'}</td></tr>")
        return ("<table class='qd'><thead><tr><th>F&amp;G band</th><th class='r'>readings</th><th class='r'>mean 5s</th><th class='r'>% up</th><th class='r'>first entries</th><th class='r'>mean 5s</th><th class='r'>% up</th></tr></thead><tbody>"
                + "".join(out) + "</tbody></table>")
    rc_rows = "".join(
        f"<tr><td>{e(r['date'])}</td><td>{'↓ to ≤' if r['dir'] == 'down' else '↑ to ≥'}{r['th']}</td><td class='r'>{r['fg']:.0f}</td>"
        f"<td class='r {'pos' if (r.get('ret') or 0) >= 0 else 'neg'}'>{'pending · matures ' + e(r['matures'] or 'later') if r.get('ret') is None else pp(r['ret'], 2)}</td>"
        f"<td class='r'>{'' if (recent_xq.get(r['date'] + str(r['th'])) or {}).get('ret') is None else pp(recent_xq[r['date'] + str(r['th'])]['ret'], 2)}</td></tr>"
        for r in reversed(recent_x))
    # ---- index breadth: share of constituents ≥10/20/30/50% below their all-time high (live panel, daily increments)
    br = S.get("breadth")
    if br and br.get("indices"):
        b_age = age_days(br.get("asof"))
        allv = [p["pct"][k] - x["points"][0]["pct"][k] for x in br["indices"] for p in x["points"] for k in range(4)]
        blo, bhi = math.floor(min(allv + [0]) - 0.5), math.ceil(max(allv + [0]) + 0.5)
        def br_card(x):
            lb = x.get("lookback") or {}
            last = x["points"][-1]
            rows = "".join(
                f"<tr><th><span class='bsw' style='background:{BREADTH_COLORS[k]}'></span>≥{t}%</th><td class='r'>{last['counts'][k]:,}</td><td class='r'><b>{last['pct'][k]:.1f}%</b></td>"
                f"<td class='r {'neg' if (lb.get('delta_pp') or [0]*4)[k] > 0 else 'pos'}'>{(lb.get('delta_pp') or [0]*4)[k]:+.1f}<small>{(lb.get('delta_counts') or [0]*4)[k]:+,}</small></td>"
                f"<td class='r {'neg' if x['delta_pp'][k] > 0 else 'pos'}'>{x['delta_pp'][k]:+.1f}<small>{x['delta_counts'][k]:+,}</small></td></tr>" for k, t in enumerate(br["thresholds"]))
            ir = lb.get("index_return_pct")
            return (f"<div class='card'><h3>{e(x['label'])}</h3>"
                    f"<p class='note' style='margin:0 0 6px'>{x['covered']:,} of {x['universe']:,} members covered · {last['carried']} on a carried price · index {('–' if ir is None else f'{ir:+.1f}%')} over {lb.get('sessions', '–')} sessions, {x['index_return_pct']:+.1f}% since {e(br['baseline'])}</p>"
                    + svg_breadth(x["points"], blo, bhi)
                    + "<table class='qd bt'><thead><tr><th>below ATH</th><th class='r'>names</th><th class='r'>share</th>"
                    f"<th class='r'>Δ {lb.get('sessions', '–')}s, pp</th><th class='r'>Δ since {e(br['baseline'][5:])}</th></tr></thead><tbody>{rows}</tbody></table></div>")
        spx = next((x for x in br["indices"] if x["ticker"] == "SPX Index"), br["indices"][0])
        lbs = spx.get("lookback") or {}
        breadth_sec = (
            "<section class='oc mon' id='idxbreadth'>"
            + head("03 · index breadth · how far members sit below their all-time highs",
                   f"S&amp;P 500: {spx['points'][-1]['pct'][1]:.0f}% of members are ≥20% below their all-time high "
                   f"({(lbs.get('delta_pp') or [0, 0])[1]:+.1f} pp over {lbs.get('sessions', '–')} sessions), through {e(br['asof'])}" + stale(b_age, "breadth", 4),
                   "Every constituent's close against its running all-time intraday high (Bloomberg INTERVAL_HIGH through the 09-08 baseline, then extended by each session's PX_HIGH). "
                   "Chart = change since the 09-08 baseline in percentage points, one line per threshold (the four overlap — a name 50% down is in all four — so never add them); the table carries the levels. Old peaks and structural losers keep the LEVELS high (the Nasdaq Composite includes many small "
                   "caps and SPACs); read the CHANGE: a rising share = participation narrowing, a falling share = more names recovering toward their highs. Δ red = more names below the line. "
                   + e(br.get("membership") or "") + ". Hover a chart for each session's counts.")
            + "<div class='grid3'>" + "".join(br_card(x) for x in br["indices"]) + "</div>"
            + f"<p class='note'>Source: Bloomberg Desktop API (PX_LAST / PX_HIGH, split-adjusted, cash dividends unadjusted). {e(br.get('missing_observations') or '')} "
              f"Daily increment: <code>market_breadth_bbg.py --update</code> (17:40 sweep and the 10:01 task, completed sessions only) → <code>build_market_breadth.py --rolling</code>. "
              f"Files: <code>_data/market_breadth/latest/</code> (summary.json, breadth_daily.csv, constituents_latest.csv). The original audited study (validation vs Bloomberg's ALL_TIME_HIGH_PERCENT) is the "
              f"<a href='market-breadth.html'>09-29 snapshot</a>.</p></section>")
    else:
        b_age = None
        breadth_sec = ("<section class='oc mon' id='idxbreadth'>" + head("03 · index breadth", "Index breadth unavailable",
                       "<code>_data/market_breadth/latest/summary.json</code> is missing — run <code>market_breadth_bbg.py --update</code> and <code>build_market_breadth.py --rolling</code>.") + "</section>")
    band_rows = [(c, cnn_g("SPY", "close", f"all_{c}")) for c in range(0, 101, 10)]
    cm = (cx or {}).get("meta", {})
    tab_mood = (
        "<section class='oc mon' id='gauge'>"
        + head("01 · market mood · CNN Fear & Greed", ("Fear & Greed at " + f"{fg:.0f} — {cnn_rating(fg)}" if fg is not None else "Fear & Greed unavailable")
               + (f", from {now['prev_1m']:.0f} a month ago" if now.get('prev_1m') is not None else "") + stale(cnn_age, "CNN", 3))
        + "<div class='mood-grid'>"
        + f"<div class='card gauge'>{svg_gauge(fg)}<div class='gsub'>prev close {'–' if now.get('prev_close') is None else round(now['prev_close'])} · 1w ago {'–' if now.get('prev_1w') is None else round(now['prev_1w'])} · 1m ago {'–' if now.get('prev_1m') is None else round(now['prev_1m'])} · 1y ago {'–' if now.get('prev_1y') is None else round(now['prev_1y'])}<br><span class='mut'>source CNN · {e(cnn_status)} · through {e(cnn_through or '–')}</span></div></div>"
        + f"<div class='card'><h3>Twelve months <small class='mut'>(shaded: ≤30 fear watch zone, ≥70 greed watch zone)</small></h3>{svg_strip(strip)}<div class='ctiles'>{comp_tiles}</div></div>"
        + "</div>"
        + f"<div class='oc-tiles four'>{stat_tile(f'Today band {cur_band} · SPY next 5 sessions', cur_stats, 'all readings, overlapping')}{stat_tile(f'Today band {cur_band} · QQQ next 5 sessions', cur_stats_q, 'all readings, overlapping')}"
        f"{stat_tile('New entry ≤30 (fear) · SPY next 5', fear_x, 'non-overlapping crossings')}{stat_tile('New entry ≥70 (greed) · SPY next 5', greed_x, 'non-overlapping crossings')}</div>"
        + "</section>"
        + "<section class='oc mon' id='extremes'>"
        + head("02 · extreme entries · what SPY and QQQ did next", f"New crossings into fear or greed → the next five sessions, {e(cm.get('start') or '–')} → {e(cm.get('price_end') or '–')}",
               "A crossing is the first reading down to ≤20 / ≤30 or up to ≥70 / ≥80 / ≥90 from the other side; staying inside a zone is not a new event, and windows for the same threshold never overlap. "
               "Deeper thresholds in the same sell-off are stages of one phase, not independent episodes. 95% intervals come from 1,000 circular 20-session block resamples; none below 10 events. "
               "Thresholds are watch levels fixed before computing, not CNN's own category cuts.")
        + "<div class='card'><div class='dc-bar'><b>ETF</b> <select data-switch='xs' data-part='0' aria-label='ETF'><option>SPY</option><option>QQQ</option><option value='QQQ/SPY'>QQQ ÷ SPY</option></select> "
        "<b>Timing</b> <select data-switch='xs' data-part='1' aria-label='Timing'><option value='close'>reading close → +5 sessions</option><option value='delayed'>next close → +5 (conservative)</option></select></div>"
        f"<div id='xs'>{xs_panels}</div><p class='note'>vs all = mean minus the mean of every reading in the sample (pp); by-year columns = mean return of that year's events. {e(' · '.join(cm.get('limitations', [])))}</p></div>"
        + "<div class='grid2'>"
        + f"<div class='card'><h3>Crossings in the last six months</h3><table class='qd'><thead><tr><th>date</th><th>crossing</th><th class='r'>F&amp;G</th><th class='r'>SPY next 5</th><th class='r'>QQQ next 5</th></tr></thead><tbody>{rc_rows or '<tr><td colspan=5 class=mut>none</td></tr>'}</tbody></table><p class='note'>Every crossing, before the non-overlap filter; pending = the five-session window has not closed.</p></div>"
        + f"<div class='card'><h3>Every band, SPY next 5 sessions</h3>{svg_band_bars(band_rows, cur_band)}<details><summary>Band table — all readings vs first entries</summary>{ep_table('SPY')}</details></div>"
        + "</div></section>"
        + breadth_sec
        + "<section class='oc mon' id='breadth'>" + head("04 · coverage-universe breadth · the 106 wiki names", f"Week ending {e(wk)}, {n_names} names")
        + "<div class='oc-tiles four'>"
        + f"<div class='oc-tile'><div class='l'>EPS revisions (4w)</div><div class='v'>{eps_up*100:.0f}% <small>up</small></div><div class='s'>{eps_dn*100:.0f}% down · Bloomberg BEst 1BF</div></div>"
        + f"<div class='oc-tile'><div class='l'>Rating drift (4w)</div><div class='v'>{rat_up*100:.0f}% <small>improving</small></div><div class='s'>share of names with a better average rating</div></div>"
        + f"<div class='oc-tile'><div class='l'>Sell-side actions (week)</div><div class='v'>{ss_up} <small>↑</small> / {ss_dn} <small>↓</small></div><div class='s'>net upgrades vs downgrades · PT raises {ss_pt_up} / cuts {ss_pt_dn}" + (f" · <b class='bad'>mail through {ss_through}</b>" if ss_age and ss_age > 7 else "") + "</div></div>"
        + f"<div class='oc-tile'><div class='l'>Price breadth (4w)</div><div class='v'>{px_up4*100:.0f}% <small>up</small></div><div class='s'>names with a positive 4-week return</div></div>"
        + "</div></section>")

    # ---------------- SELL-SIDE & DESKS
    dcomp = (desk or {}).get("companies", {})
    def tone_cls(t):
        t = (t or "").lower()
        return "pos" if t.startswith(("pos", "constr", "bull")) else "neg" if t.startswith(("neg", "bear", "caut", "skep")) else ""
    drows = "".join(
        f"<tr data-tk='{e(t)}'><td class='tk'>{tk_link(t)}</td><td class='{tone_cls(c.get('tone'))}'>{e(c.get('tone') or '–')}</td><td>{e(c.get('position') or '–')}</td>"
        f"<td>{e(c.get('latest_firm') or '–')}<small>{e((c.get('latest') or '')[:10])}</small></td><td class='r'>{c['n']}<small>{c['n30']} in 30d</small></td><td class='wrapcell'>{e(c.get('summary') or '')}<small>{e(', '.join(c.get('houses', [])[:6]))}</small></td></tr>"
        for t, c in sorted(dcomp.items(), key=lambda kv: kv[1].get("latest") or "", reverse=True))
    orows = "".join(
        f"<tr data-tk='{e(o.get('ticker') or '')}'><td>{e((o.get('date') or '')[:10])}</td><td class='tk'>{tk_link(o.get('ticker') or '')}</td><td>{e(o.get('firm') or '–')}<small>{e(o.get('author') or '')}{' · ' + e(o['role']) if o.get('role') else ''}</small></td>"
        f"<td>{e(o.get('kind') or '')}</td><td class='{tone_cls(o.get('tone'))}'>{e(o.get('tone') or '')}</td><td>{e(o.get('position') or '')}</td>"
        f"<td class='wrapcell'>{e(o.get('summary') or '')}" + (f"<details><summary>excerpt</summary><q>{e((o.get('excerpt') or '')[:420])}</q><small>{e(o.get('subject') or '')} · {e(o.get('review') or '')}</small></details>" if o.get("excerpt") else "") + "</td></tr>"
        for o in (desk or {}).get("observations", [])[:250])
    sm = (ssl_ or {}).get("meta", {}); snames = (ssl_ or {}).get("names", {})
    s_age = age_days(sm.get("through"))
    srank = sorted(snames.items(), key=lambda kv: -(abs(kv[1]["up"] - kv[1]["down"]) * 2 + abs(kv[1]["pt_up"] - kv[1]["pt_down"]) + kv[1]["notes30"] / 50))[:60]
    srows = "".join(
        f"<tr data-tk='{e(t)}'><td class='tk'>{tk_link(t)}</td><td class='r'>{v['notes30']:.0f}<small>prior {v['notes_prior30']:.0f}/mo</small></td><td class='r {'pos' if (v['flow'] or 0) > 0 else 'neg' if (v['flow'] or 0) < 0 else ''}'>{'–' if v['flow'] is None else f'{v[chr(102)+chr(108)+chr(111)+chr(119)]:+.2f}'}</td>"
        f"<td class='r'>{v['firms30']}</td><td class='r pos'>{v['up'] or ''}</td><td class='r neg'>{v['down'] or ''}</td><td class='r pos'>{v['pt_up'] or ''}</td><td class='r neg'>{v['pt_down'] or ''}</td>"
        f"<td class='r'>{pct(v['pt_avg'])}</td><td class='r'>{v['est_up'] or ''}{'/' if v['est_up'] or v['est_down'] else ''}{v['est_down'] or ''}</td><td class='r'>{e(v.get('last') or '–')}</td></tr>"
        for t, v in srank)
    erows = "".join(
        f"<tr data-tk='{e(ev['t'])}'><td>{e(ev['d'])}</td><td class='tk'>{tk_link(ev['t'])}</td><td>{e(ev.get('firm') or '–')}</td>"
        f"<td>{' · '.join(f'<span class={chr(39)}{chr(112)+chr(111)+chr(115) if k in (chr(117)+chr(112)+chr(103)+chr(114)+chr(97)+chr(100)+chr(101), chr(80)+chr(84)+chr(32)+chr(114)+chr(97)+chr(105)+chr(115)+chr(101), chr(101)+chr(115)+chr(116)+chr(105)+chr(109)+chr(97)+chr(116)+chr(101)+chr(115)+chr(32)+chr(117)+chr(112)) else chr(110)+chr(101)+chr(103)}{chr(39)}>{e(k)}</span>' for k in ev['kinds'])}</td>"
        f"<td class='r'>{'size n/a' if ev.get('pt_nominal') else pct(ev.get('pt'))}</td><td class='wrapcell'>{e(ev.get('s') or '')}</td></tr>"
        for ev in (ssl_ or {}).get("events", [])[:300])
    dm = (desk or {}).get("meta", {})
    tab_desks = (
        "<section class='oc mon' id='deskviews'>"
        + head("01 · desk views · specialist sales, desks and priority authors", f"Desk-view ledger — {dm.get('n_obs', 0)} attributed observations, latest review {e(dm.get('latest_review') or 'none yet')}",
               "Each row is one attributed observation read in context: who said it (firm, author, role), what kind of claim it is (investor feedback, desk opinion, positioning, management claim, technical), "
               "tone, the positioning it describes and a one-line summary with the original excerpt. Desk and specialist-sales voices carry no ratings or price targets and never aggregate with rated research. "
               "Seeded with the retained Codex review of 07–21 Sep 2026; every daily review since then appends. A forward or repeated quote is one claim, not several.")
        + "<div class='card'><div class='dc-bar'><input type='search' class='tkfilter' data-target='dtab' placeholder='Filter by ticker…' aria-label='Filter desk views by ticker'></div>"
        f"<div class='scroll'><table class='qd lt' id='dtab'><thead><tr><th>Name</th><th>latest tone</th><th>positioning</th><th>latest source</th><th class='r'>obs</th><th>latest view · houses</th></tr></thead><tbody>{drows or '<tr><td colspan=6 class=mut>no observations</td></tr>'}</tbody></table></div></div>"
        + "<h3>Observation log</h3><div class='card'><div class='dc-bar'><input type='search' class='tkfilter' data-target='otab' placeholder='Filter by ticker…' aria-label='Filter observations by ticker'></div>"
        f"<div class='scroll'><table class='qd lt' id='otab'><thead><tr><th>date</th><th>name</th><th>source</th><th>kind</th><th>tone</th><th>positioning</th><th>summary</th></tr></thead><tbody>{orows}</tbody></table></div></div>"
        + "</section>"
        + "<section class='oc mon' id='sellside'>"
        + head("02 · sell-side actions · mechanical, from the broker-mail parse", f"Rating, price-target and estimate actions — mail through {e(sm.get('through') or '–')}" + stale(s_age, "broker mail", 3),
               e(sm.get("rule") or "") + " Window: the last 30 days of mail ending on the newest e-mail, so a stale mailbox shows its last valid month, not today.")
        + "<div class='card'><div class='dc-bar'><input type='search' class='tkfilter' data-target='stab' placeholder='Filter by ticker…' aria-label='Filter sell-side names'></div>"
        f"<div class='scroll'><table class='qd lt' id='stab'><thead><tr><th>Name</th><th class='r'>notes 30d</th><th class='r'>flow Δ</th><th class='r'>firms</th><th class='r'>upgr.</th><th class='r'>downgr.</th><th class='r'>PT ↑</th><th class='r'>PT ↓</th><th class='r'>avg PT Δ</th><th class='r'>est ↑/↓</th><th class='r'>last action</th></tr></thead><tbody>{srows}</tbody></table></div></div>"
        + "<h3>Recent actions</h3><div class='card'><div class='dc-bar'><input type='search' class='tkfilter' data-target='etab' placeholder='Filter by ticker…' aria-label='Filter sell-side actions'></div>"
        f"<div class='scroll'><table class='qd lt' id='etab'><thead><tr><th>date</th><th>name</th><th>firm</th><th>action</th><th class='r'>PT Δ</th><th>subject</th></tr></thead><tbody>{erows}</tbody></table></div></div>"
        + "</section>")

    # ---------------- BACKTESTS
    def quad_cell(k):
        s = quad.get(k)
        if not s:
            return "<td>–</td>"
        return f"<td class='{'pos' if s['mean'] >= 0 else 'neg'}'><b>{s['mean']*100:+.1f}%</b><small>hit {s['hit']*100:.0f}% · n={s['n']}</small></td>"
    def ev_cell(st):
        if not st:
            return "<td>–</td>"
        return f"<td class='{'pos' if st['mean'] >= 0 else 'neg'}'><b>{st['mean']*100:+.1f}%</b><small>median {st['median']*100:+.1f}% · hit {st['hit']*100:.0f}% · p25/p75 {st['p25']*100:+.1f}/{st['p75']*100:+.1f} · n={st['n']}</small></td>"
    windows = (
        "<section class='oc mon' id='windows'>"
        + head("01 · windows · what usually happens next", f"Forward universe-relative returns after a sentiment state — Bloomberg track, {e(span[0])} → {e(span[1])}",
               "Weekly panel, returns relative to the universe mean. Quadrants cut at each week's medians of HOT and BULL. 'Turned hot' = below the median one week, top quintile the next; 'turned cold' the mirror image.")
        + "<div class='grid2'><div class='card'><h3>Quadrant this week → next 1w / 15d / 4w</h3><table class='qd'><thead><tr><th></th><th>1 week</th><th>15 days</th><th>4 weeks</th></tr></thead><tbody>"
        + "".join(f"<tr><th>{lab}</th>{quad_cell(q+'|rel_ret_1w')}{quad_cell(q+'|rel_ret_15d')}{quad_cell(q+'|rel_ret_4w')}</tr>" for q, lab in (("hot-bull", "Hot · bull"), ("hot-bear", "Hot · bear"), ("cold-bull", "Cold · bull"), ("cold-bear", "Cold · bear")))
        + "</tbody></table></div><div class='card'><h3>Turned hot / turned cold → next 1w / 15d / 4w</h3><table class='qd'><thead><tr><th></th><th>1 week</th><th>15 days</th><th>4 weeks</th></tr></thead><tbody>"
        + f"<tr><th>Turned hot</th>{ev_cell(turned_hot.get('1w'))}{ev_cell(turned_hot.get('15d'))}{ev_cell(turned_hot.get('4w'))}</tr>"
        + f"<tr><th>Turned cold</th>{ev_cell(turned_cold.get('1w'))}{ev_cell(turned_cold.get('15d'))}{ev_cell(turned_cold.get('4w'))}</tr>"
        + "</tbody></table><p class='note'>Averages across many names and weeks; dispersion is wide and the signal has not been a reliable timing tool (lead/lag below).</p></div></div></section>")
    sbm = (sb or {}).get("meta", {})
    def sb_table(fam, per, h):
        blk = (sb or {}).get("pooled", {}).get(fam, {}).get(per, {}).get(str(h))
        if not blk:
            return "<p class='note'>Study unavailable.</p>"
        def tr(lab, x, cls=""):
            if not x.get("n"):
                return f"<tr class='{cls}'><th>{lab}</th><td colspan='8' class='mut'>no outcomes</td></tr>"
            ci = x.get("ci")
            return (f"<tr class='{cls}'><th>{lab}</th><td class='r'>{x['n']}<small>{x['stocks']} names</small></td><td class='r {'pos' if (x['mean'] or 0) >= 0 else 'neg'}'><b>{x['mean']:+.2f}%</b></td><td class='r'>{x['median']:+.2f}%</td><td class='r'>{x['up']:.0f}%</td>"
                    f"<td class='r'>{x['p10']:+.1f} / {x['p90']:+.1f}</td><td class='r'>{'–' if not ci else f'{ci[0]:+.2f} / {ci[1]:+.2f}'}</td><td class='r'>{'' if x.get('vs_base') is None else f'{x[chr(118)+chr(115)+chr(95)+chr(98)+chr(97)+chr(115)+chr(101)]:+.2f}'}</td>"
                    f"<td class='r'>{'–' if x.get('xs_qqq') is None else f'{x[chr(120)+chr(115)+chr(95)+chr(113)+chr(113)+chr(113)]:+.2f}'}</td></tr>")
        return ("<table class='qd xs'><thead><tr><th>score band</th><th class='r'>n</th><th class='r'>mean</th><th class='r'>median</th><th class='r'>% up</th><th class='r'>p10 / p90</th><th class='r'>95% CI mean</th><th class='r'>vs all (pp)</th><th class='r'>vs QQQ (pp)</th></tr></thead><tbody>"
                + "".join(tr(BANDL[i], x) for i, x in enumerate(blk["bands"])) + tr("All bands (baseline)", blk["base"], "base") + "</tbody></table>")
    sb_panels = "".join(f"<div data-key='{fam}|{per}|{h}'{'' if (fam, per, h) == ('HOT', 'all', 10) else ' hidden'}>{sb_table(fam, per, h)}</div>"
                        for fam in ("HOT", "BULL") for per in ("all", "pre2026", "2026") for h in (5, 10))
    bands_sec = (
        "<section class='oc mon' id='bands'>"
        + head("02 · score bands · HOT / BULL → the next 5 and 10 sessions", f"Score and subsequent returns — {e(sbm.get('track') or '')}, weeks {e(sbm.get('first_week') or '–')} → {e(sbm.get('week') or '–')}",
               e(sbm.get("score") or "") + ". " + e(sbm.get("timing") or "") + ". " + e(sbm.get("sampling") or "") + ". " + e(sbm.get("uncertainty") or "") + ".")
        + "<div class='card'><div class='dc-bar'><b>Score</b> <select data-switch='sb' data-part='0' aria-label='Score'><option>HOT</option><option>BULL</option></select> "
        "<b>Period</b> <select data-switch='sb' data-part='1' aria-label='Period'><option value='all'>2024 → today</option><option value='pre2026'>2024–25</option><option value='2026'>2026</option></select> "
        "<b>Hold</b> <select data-switch='sb' data-part='2' aria-label='Holding period'><option value='5'>5 sessions</option><option value='10' selected>10 sessions</option></select></div>"
        f"<div id='sb'>{sb_panels}</div><p class='note'>{e(sbm.get('baseline') or '')}. {e(sbm.get('periods') or '')}. {e(' '.join(sbm.get('limitations', [])))} Each name's own analogs in its current band are on the stock chart (Names).</p></div>"
        + "</section>")
    tab_back = windows + bands_sec + "<div class='sx'>" + parts["warn"] + parts["own_bt"] + parts["long"] + parts["picks"] + parts["leadlag"] + parts["events"] + parts["method"] + "</div>"

    # ---------------- ARCHIVE
    arch = [("market-breadth.html", "Market breadth — the audited 09-29 study", "2026-09-29", "Constituent drawdown study (Sep 8 → Sep 29) with the validation against Bloomberg ALL_TIME_HIGH_PERCENT. Its membership and pre-window highs are the base of Market mood → index breadth, which extends it every session."),
            ("attention-sentiment/crowding-tracker.html", "Attention & sentiment — stock radar (Codex)", "2026-09-30", "106-name radar on the Codex 'Attention & sentiment score' (early_pressure). Replaced by Today → movers (Bloomberg Twitter) and Names → stock chart."),
            ("attention-sentiment/specialist-sales.html", "Specialist sales — 07–21 Sep review (Codex)", "2026-09-21", "The LLM-reviewed desk ledger; its 155 observations are the seed of Sell-side & desks → desk views."),
            ("attention-sentiment/cnn-next-week.html", "Fear & Greed — extreme entries (Codex)", "2026-09-23", "Same rules as Market mood → extreme entries, which now rebuilds daily."),
            ("attention-sentiment/cnn-spy-qqq-study.html", "Fear & Greed — full correlation study (Codex)", "2026-09-18", "Same-day correlation, rolling correlation and lead tests; one-off research, not refreshed."),
            ("attention-sentiment/score-returns.html", "Score → 1/2-week returns (Codex)", "2026-09-29", "The early_pressure composite; replaced by Backtests → score bands on HOT/BULL."),
            ("attention-sentiment/narrative-diffusion.html", "Narratives — META/Muse case study (Codex)", "2026-09-21", "Alias / author-diffusion case study (META, GOOGL, NBIS, ORCL, NVDA); retrospective by design."),
            ("attention-sentiment/daily-brief.html", "Sentiment Radar daily brief — last Codex edition", "2026-09-30", "The Codex daily e-mail; the 10:00 sentiment-radar task (Claude) writes it now."),
            ("attention-sentiment/crowding-tracker-previous.html", "Stock radar — previous design (Codex)", "2026-09-21", "Superseded layout, kept for reference.")]
    tab_arch = ("<section class='oc mon' id='arch'>" + head("archive · frozen pages", "Frozen snapshots behind this page, kept with their data dates",
                "The Codex pipeline lost access to the wiki caches, CNN and Outlook from 2026-09-30 and kept mailing 09-29 data; it was retired on 2026-10-13 and its studies were ported "
                "into this page so they rebuild in the wiki chain. These files are never rebuilt.")
                + "<div class='card'><table class='qd lt'><thead><tr><th>page</th><th>data as of</th><th>what it was · where it lives now</th></tr></thead><tbody>"
                + "".join(f"<tr><td><a href='{e(h)}'>{e(t)}</a></td><td>{e(d)}</td><td class='wrapcell'>{e(x)}</td></tr>" for h, t, d, x in arch if (DASH / h).exists())
                + "</tbody></table></div></section>")

    # ---------------- shell
    TABS = [("today", "Today", tab_today), ("names", "Names", tab_names), ("mood", "Market mood", tab_mood),
            ("desks", "Sell-side & desks", tab_desks), ("backtests", "Backtests", tab_back), ("archive", "Archive", tab_arch)]
    nav = "<div class='or-nav-group'><p>Sentiment</p>" + "".join(
        f"<a href='#{k}' data-tab='{k}'><span class='or-nav-number' aria-hidden='true'>{i:02d}</span>{e(lab)}</a>" for i, (k, lab, _) in enumerate(TABS, 1)) + "</div>"
    tabbar = "<div class='tabbar' role='tablist'>" + "".join(f"<a href='#{k}' role='tab' data-tab='{k}'>{e(lab)}</a>" for k, lab, _ in TABS) + "</div>"
    body = "".join(f"<div class='tab' id='tab-{k}' data-tab='{k}' role='tabpanel'>{html_}</div>" for k, _, html_ in TABS)
    stale_n = sum(1 for a in (tw_age, ss_age, px_age, cnn_age, bx_age) if a is not None and a > 7)
    shell = (
        "<div class='or-dashboard'><a class='or-skip' href='#dashboard-main'>Skip to content</a>"
        "<aside class='or-sidebar'><a class='or-brand' href='index.html' aria-label='Wiki dashboards'>"
        "<span class='or-brand-mark' aria-hidden='true'>C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>"
        f"<nav class='or-navigation' aria-label='Tabs'>{nav}</nav>"
        f"<div class='or-sidebar-footer'><span class='or-status-dot'></span>Sentiment<small>Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · {stale_n} feed{'s' if stale_n != 1 else ''} &gt;7 days old</small>"
        "<a href='index.html'>All dashboards <span aria-hidden='true'>↗</span></a><a href='../index.html'>Back to research wiki <span aria-hidden='true'>↗</span></a></div></aside>"
        "<div class='or-workspace'><header class='or-topbar'><div><p class='or-breadcrumb'>RESEARCH / SENTIMENT</p><h1>Sentiment</h1></div>"
        f"<div class='or-topbar-actions'><span class='or-asof'>Fear & Greed <b>{'–' if fg is None else f'{fg:.0f} · ' + cnn_rating(fg)}</b></span>"
        f"<span class='or-asof'>Bloomberg X <b>{e(bx_through or '–')}</b></span><span class='or-asof'>desk review <b>{e(rv_date or '–')}</b></span>"
        "<button type='button' class='or-theme' aria-label='Switch to dark theme' aria-pressed='false'><svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.6' aria-hidden='true'><path d='M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z'/></svg></button>"
        f"</div></header><main id='dashboard-main' class='or-main' tabindex='-1'>{tabbar}<div class='sx'><div id='tip' class='tip'></div></div>")

    # ---- page data for the stock chart and per-name strip
    mon = {"daily": {"dates": ddates, "qqq": (ds or {}).get("qqq"), "tickers": dtk, "names": (ds or {}).get("names", {})},
           "bands": {"labels": BANDL, "week": sbm.get("week"), "c": {t: {f: {"s": (c.get(f) or {}).get("score"), "b": (c.get(f) or {}).get("band"), "own": (c.get(f) or {}).get("own")} for f in ("HOT", "BULL")} for t, c in comp_b.items()}},
           "desk": {t: {k: c.get(k) for k in ("tone", "position", "summary", "latest", "latest_firm", "n", "n30")} for t, c in dcomp.items()},
           "ss": {t: v for t, v in snames.items()}, "ss_through": sm.get("through"), "review": {r.get("ticker"): r for r in (review or {}).get("up", []) + (review or {}).get("down", []) if r.get("ticker")}}
    mon_json = json.dumps(mon, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    font = ""
    if FONT.exists():
        font = ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'
                + base64.b64encode(FONT.read_bytes()).decode() + ') format("woff2")}')
    page = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Sentiment</title>"
            "<script>try{var t=localStorage.getItem('wiki-dash-theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t;}catch(e){}</script>"
            f"<style>{font}{OR_CSS}{PAGE_CSS}{RANKING_CSS}</style></head><body>{shell}{body}"
            "<p class='hub-credit note'>Built by <code>_tools/build_sentiment_monitor.py</code> (+ <code>sentiment_studies.py</code>, <code>_sentiment_dash.py</code>) from <code>_data/sentiment/</code>; "
            "CNN pulled live with a cache fallback; the desk read comes from the 10:00 sentiment-radar task. Numbers in <code>monitor.json</code>.</p>"
            f"</main></div></div><script>window.__SENT__ = {parts['payload']};window.__MON__ = {mon_json};</script>"
            f"<script>{SX_JS}</script><script>{OR_JS}</script><script>{PAGE_JS}</script></body></html>")
    OUT.write_text(page, encoding="utf-8")
    print(f"  -> {OUT} ({len(page)/1e6:.1f} MB)")
    print(f"  cnn {cnn_status}: {fg} ({cnn_rating(fg)}) · BBG X through {bx_through} · own X through {tw_through} ({tw_age} d) · mail {ss_through} ({ss_age} d) · prices {px_through} · desk review {rv_date}")
    print(f"  movers: BBG {len(b_rise)}↑/{len(b_fall)}↓ · own {len(rising)}↑/{len(falling)}↓")
    return 0


PAGE_CSS = r"""
.mon{margin-bottom:46px}.mon h3{margin:26px 0 10px;font-size:15px}
.tab{display:none}.tab.on{display:block}
.tabbar{display:flex;gap:4px;flex-wrap:wrap;margin:0 0 22px;border-bottom:1px solid var(--border)}
.tabbar a{padding:9px 14px;font-size:13px;font-weight:600;color:var(--ink2);text-decoration:none;border-bottom:2px solid transparent;margin-bottom:-1px}
.tabbar a[aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent)}.tabbar a:hover{color:var(--ink)}
.mood-grid{display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:stretch}@media(max-width:900px){.mood-grid{grid-template-columns:1fr}}
.gauge{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.gsub{font-size:11px;color:var(--ink2);margin-top:6px;line-height:1.7}
.ctiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px;margin-top:12px}
.ctile{border:1px solid var(--border);border-radius:8px;padding:8px 10px;background:var(--plane)}.ctile .l{font-size:9px;letter-spacing:.5px;text-transform:uppercase;color:var(--muted)}
.ctile .v{font-size:12px;font-weight:700;margin-top:3px;text-transform:capitalize}.ctile .v.fear,.ctile .v.extreme-fear{color:var(--crit)}.ctile .v.greed,.ctile .v.extreme-greed{color:var(--good)}.ctile .v.neutral{color:var(--ink2)}
.oc-tiles.four{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:14px 0 6px}@media(max-width:1100px){.oc-tiles.four{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.oc-tiles.four{grid-template-columns:1fr}}
.oc-tile .v small{font-size:12px;font-weight:500;color:var(--muted);letter-spacing:0}.oc-tile .v.pos{color:var(--s1)}.oc-tile .v.neg{color:var(--crit)}.or-main .oc-tile .v{font-size:26px}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:14px}@media(max-width:1100px){.grid2{grid-template-columns:1fr}}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:14px}@media(max-width:1250px){.grid3{grid-template-columns:1fr}}
.bsw{display:inline-block;width:14px;height:3px;border-radius:2px;margin-right:7px;vertical-align:3px}table.qd.bt th,table.qd.bt td{white-space:nowrap;padding:6px 4px}
.card{min-width:0;overflow:hidden}.card h3{margin-top:0}
table.mv,table.qd,table.src{width:100%;border-collapse:collapse;font-size:12px}table.mv th,table.qd th,table.src th{font-size:9.5px;letter-spacing:.4px;text-transform:uppercase;color:var(--muted);text-align:left;padding:6px 6px;border-bottom:1px solid var(--grid)}
table.mv td,table.qd td,table.src td{padding:7px 6px;border-bottom:1px solid var(--grid);vertical-align:middle}td.r,th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.qd tbody th{font-size:12px;text-transform:none;letter-spacing:0;color:var(--ink);font-weight:600}table.qd tr.base td,table.qd tr.base th{border-top:2px solid var(--grid);color:var(--ink2)}table.qd tr.cur th{color:var(--accent)}
table.lt td{vertical-align:top}td.wrapcell{white-space:normal;min-width:260px;line-height:1.55}td.wrapcell q{display:block;margin:6px 0;color:var(--ink2);font-style:italic}
td.tk{font-weight:700;white-space:nowrap}td.tk small{display:block;font-weight:400;color:var(--muted);font-size:10px}
td.bar{min-width:150px}.hb{display:inline-block;width:90px;height:8px;background:var(--grid);border-radius:4px;vertical-align:middle;margin-right:8px;overflow:hidden}.hb i{display:block;height:100%}
td.pos,.pos{color:var(--s1)}td.neg,.neg{color:var(--crit)}td small{display:block;color:var(--muted);font-size:10px;font-weight:400}
.stale-tag{color:var(--crit);font-size:12px;font-weight:600;background:color-mix(in srgb,var(--crit) 12%,var(--surf));padding:2px 8px;border-radius:8px;vertical-align:middle;letter-spacing:0}
.note-card p{margin:0 0 12px;font-size:13.5px;line-height:1.8;color:var(--ink)}.note-card p:last-child{margin:0}.note-card.extra{border-left:3px solid var(--accent)}
.note{font-size:11px;color:var(--muted);line-height:1.8;margin:10px 0 0}.mut{color:var(--muted)}b.bad{color:var(--crit)}b.warn{color:var(--warn)}b.ok{color:var(--good)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;vertical-align:1px}.dot.ok{background:var(--good)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--crit)}
.or-main .oc .oc-headline{font-size:22px}.or-topbar-actions .or-asof+.or-asof{margin-left:-6px}
a.tkl{color:inherit;text-decoration:none;border-bottom:1px dotted var(--muted)}a.tkl:hover{color:var(--accent)}
ul.tl{margin:0;padding-left:18px;font-size:12.5px;line-height:1.9}
details.card summary,details summary{cursor:pointer;font-weight:600;font-size:13px}
.dcard{border:1px solid var(--border);border-radius:10px;padding:12px 14px;margin:0 0 10px;background:var(--surf)}.dcard.up{border-left:3px solid var(--s4)}.dcard.down{border-left:3px solid var(--s1)}
.dcard .dh{display:flex;gap:10px;align-items:baseline;font-weight:700;font-size:14px}.dcard .sig{font-size:10px;font-weight:650;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}.dcard .conv{margin-left:auto;font-size:10px;color:var(--muted)}
.dcard p{margin:6px 0 0;font-size:12.5px;line-height:1.65}.dcard p.cw{color:var(--ink2)}.dcard p.evid{font-size:10.5px;color:var(--muted)}
.dc-bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 12px;font-size:12px}.dc-bar b{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}
.dc-bar select,.dc-bar input{font:inherit;font-size:12.5px;padding:5px 9px;border:1px solid var(--border);border-radius:7px;background:var(--surf);color:var(--ink)}.dc-bar input{min-width:220px}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:7px;overflow:hidden}.seg button{font:inherit;font-size:12px;padding:5px 11px;border:0;background:var(--surf);color:var(--ink2);cursor:pointer}.seg button.on{background:var(--accent);color:var(--surf)}
.dc-info{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin:0 0 10px}.dc-info .it{border:1px solid var(--border);border-radius:8px;padding:9px 11px;background:var(--plane);font-size:12px;line-height:1.55}
.dc-info .it .l{font-size:9px;letter-spacing:.5px;text-transform:uppercase;color:var(--muted);font-weight:650}.dc-info .it .v{font-weight:700;font-size:14px;margin:2px 0}
.dc-chart{position:relative}.dc-chart svg{display:block;width:100%}.dc-hover{position:absolute;pointer-events:none;background:var(--surf);border:1px solid var(--border);border-radius:7px;padding:7px 9px;font-size:11.5px;line-height:1.55;box-shadow:0 2px 10px #0002;display:none;z-index:3;white-space:nowrap}
.dc-read{font-size:12px;color:var(--ink2);line-height:1.7;margin-top:8px}
.sx{--line:var(--border);--ink3:var(--muted);--blue:var(--s1);--orange:var(--s4);--red:var(--crit);--aqua:var(--s2);--chip:var(--plane);--bg:var(--plane);--mid:var(--grid);
 --blue-soft:color-mix(in srgb,var(--s1) 22%,var(--surf));--red-soft:color-mix(in srgb,var(--crit) 22%,var(--surf));--orange-soft:color-mix(in srgb,var(--s4) 24%,var(--surf))}
.sx h2{font-size:16px;margin:0 0 10px;letter-spacing:-.2px}.sx h3{font-size:13.5px;margin:14px 0 6px;color:var(--ink2)}.sx .sub{color:var(--ink2);font-size:13px}
.sx .kpis{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0 6px}.sx .kpi{background:var(--surf);border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:150px;flex:1 1 180px}
.sx .kpi b{display:block;font-size:20px;font-weight:600}.sx .kpi span{color:var(--ink2);font-size:12px}
.sx section{background:var(--surf);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:16px 0}
.sx .row{display:flex;gap:16px;flex-wrap:wrap}.sx .col{flex:1 1 420px;min-width:0}
.sx table{border-collapse:collapse;width:100%;font-size:12.5px}.sx th,.sx td{padding:5px 8px;border-bottom:1px solid var(--grid);text-align:right;white-space:nowrap}
.sx th{color:var(--ink2);font-weight:600;cursor:pointer;user-select:none;position:sticky;top:0;background:var(--surf)}.sx th:first-child,.sx td:first-child,.sx th.l,.sx td.l{text-align:left}
.sx tr:hover td{background:var(--chip)}.sx .tk{font-weight:600}.sx .nm{color:var(--ink3);font-size:11px;font-weight:400;margin-left:6px}
.sx .barwrap{display:inline-block;width:96px;height:12px;position:relative;vertical-align:middle}.sx .barwrap i{position:absolute;left:50%;top:0;width:1px;height:12px;background:var(--ink3);opacity:.5}
.sx .barwrap b{position:absolute;top:1px;height:10px;border-radius:3px}
.sx .tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:600;background:var(--chip);color:var(--ink2)}.sx .tag.hb{background:var(--orange-soft)}.sx .tag.cb{background:var(--blue-soft)}.sx .tag.hr{background:var(--red-soft)}
.sx .scroll,.scroll{overflow:auto;max-height:640px;border:1px solid var(--grid);border-radius:6px}.sx .scroll[style*="max-height:none"] th{position:static}
.sx svg{display:block;max-width:100%}.sx .tip{position:fixed;pointer-events:none;background:var(--surf);border:1px solid var(--line);border-radius:6px;padding:6px 9px;font-size:12px;box-shadow:0 2px 8px rgba(0,0,0,.12);display:none;z-index:9;max-width:340px}
.sx .legend{display:flex;gap:14px;font-size:12px;color:var(--ink2);margin:4px 0 8px;flex-wrap:wrap}.sx .legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.sx select,.sx input{font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--surf);color:var(--ink)}
.sx .note{color:var(--ink2);font-size:12.5px;line-height:1.6}.sx .warn{border-left:3px solid var(--orange);padding:6px 10px;background:var(--chip);border-radius:4px;font-size:12.5px;margin:8px 0}
.sx .tw{font-size:12px;border-left:2px solid var(--line);padding:4px 8px;margin:4px 0;color:var(--ink2)}.sx .tw b{color:var(--ink)}
.sx details summary{cursor:pointer;font-weight:600}.sx dl{display:grid;grid-template-columns:200px 1fr;gap:4px 14px;font-size:12.5px}.sx dt{color:var(--ink2)}.sx dd{margin:0}
.sx .pos{color:var(--s1)}.sx .neg{color:var(--crit)}.sx .hzbar{display:flex;gap:10px;align-items:center;margin:0 0 10px;font-size:13px;flex-wrap:wrap}
@media(max-width:640px){.sx dl{grid-template-columns:1fr}.mood-grid{grid-template-columns:1fr}.or-main .oc .oc-headline{font-size:19px}}
"""

PAGE_JS = r"""
(function(){
 // ---------------- tabs (hash-driven; tab containers are #tab-<key> so the shell's scroll-spy ignores them)
 const keys=[...document.querySelectorAll('.tab')].map(t=>t.dataset.tab);
 function show(k,scroll){
  if(!keys.includes(k)) k='today';
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.tab===k));
  document.querySelectorAll('[data-tab]').forEach(a=>{ if(a.tagName!=='A') return; const on=a.dataset.tab===k;
    a.setAttribute('aria-selected',String(on)); if(on) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
  try{localStorage.setItem('sent-tab',k);}catch(e){}
  if(scroll) window.scrollTo(0,0);
  // charts first drawn inside a hidden tab took the 900px fallback and then read that width back; let them refit
  const tab=document.getElementById('tab-'+k);
  ['sc','tkc','icbar','qbar','icts','licbar','lqbar','licts','pk_curve'].forEach(id=>{const el=document.getElementById(id); if(el&&tab&&tab.contains(el)){el.removeAttribute('width'); el.style.width='100%';}});
  setTimeout(()=>window.dispatchEvent(new Event('resize')),20);
 }
 window.__showTab=show;
 window.addEventListener('hashchange',()=>show(location.hash.slice(1),true));
 let start=location.hash.slice(1); if(!keys.includes(start)){ try{start=localStorage.getItem('sent-tab')||'today';}catch(e){start='today';} }
 show(start,false);
 // ---------------- generic selects that switch pre-rendered panels: <select data-switch=ID data-part=i> → #ID > [data-key="a|b|…"]
 document.querySelectorAll('select[data-switch]').forEach(s=>s.addEventListener('change',()=>{
  const id=s.dataset.switch; const sels=[...document.querySelectorAll(`select[data-switch="${id}"]`)].sort((a,b)=>a.dataset.part-b.dataset.part);
  const key=sels.map(x=>x.value).join('|'); document.querySelectorAll(`#${CSS.escape(id)} > [data-key]`).forEach(p=>p.hidden=p.dataset.key!==key);
 }));
 // ---------------- ticker filters on the ledger tables
 document.querySelectorAll('input.tkfilter').forEach(inp=>inp.addEventListener('input',()=>{
  const q=inp.value.trim().toUpperCase(); document.querySelectorAll(`#${inp.dataset.target} tbody tr`).forEach(tr=>{tr.hidden=!!q && !(tr.dataset.tk||'').toUpperCase().includes(q);});
 }));
 // ---------------- stock chart
 const M=window.__MON__||{}; const S=M.daily||{}; const sel=document.getElementById('dc_tk'); if(!sel||!S.tickers) return;
 const box=document.getElementById('dc_chart'), info=document.getElementById('dc_info'), read=document.getElementById('dc_read');
 const tks=Object.keys(S.tickers).sort(); const NM=S.names||{};
 tks.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t+' — '+(NM[t]||'').slice(0,30);sel.appendChild(o);});
 let range=90; sel.value=tks.includes('NVDA')?'NVDA':tks[0];
 const f1=(x,d=1)=>x==null?'–':(x>0?'+':'')+(+x).toFixed(d), fp=(x,d=1)=>x==null?'–':(x>0?'+':'')+(x*100).toFixed(d)+'%';
 const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 function ma(a,k){const o=[];for(let i=0;i<a.length;i++){let s=0,n=0;for(let j=Math.max(0,i-k+1);j<=i;j++){if(a[j]!=null){s+=a[j];n++;}}o.push(n?s/n:null);}return o;}
 function strip(t){
  const B=(M.bands||{}), c=(B.c||{})[t]||{}, L=B.labels||[]; const D=(M.desk||{})[t], SS=(M.ss||{})[t], R=(M.review||{})[t];
  const sc=f=>{const x=c[f]||{}; if(x.s==null) return '<div class="v">–</div>';
    const own=(x.own||[]); const o5=own.find(o=>o.h===5)||{}, o10=own.find(o=>o.h===10)||{};
    const an=o10.n>=10?`own history in this band: next 10 sessions ${f1(o10.mean,1)}% (median ${f1(o10.median,1)}%, up ${o10.up==null?'–':o10.up.toFixed(0)}%, n=${o10.n}${o10.n<20?', thin':''}) · 5 sessions ${f1(o5.mean,1)}%`
      :`only ${o10.n||0} own outcomes in this band — no headline estimate`;
    return `<div class="v">${x.s.toFixed(0)} <small class="mut">${esc(L[x.b]||'')}</small></div>${an}`;};
  let h=`<div class="it"><div class="l">HOT (Bloomberg track, week ${esc(B.week||'')})</div>${sc('HOT')}</div><div class="it"><div class="l">BULL</div>${sc('BULL')}</div>`;
  h+=D?`<div class="it"><div class="l">Desk view · ${esc((D.latest||'').slice(0,10))} · ${esc(D.latest_firm||'')}</div><div class="v">${esc(D.tone||'–')} <small class="mut">${esc(D.position||'')}</small></div>${esc(D.summary||'')} <span class="mut">(${D.n} obs, ${D.n30} in 30d)</span></div>`
       :`<div class="it"><div class="l">Desk view</div><div class="v">–</div><span class="mut">no attributed desk observation</span></div>`;
  h+=SS?`<div class="it"><div class="l">Sell-side, 30 days of mail to ${esc(M.ss_through||'')}</div><div class="v">${SS.up}↑ ${SS.down}↓ <small class="mut">ratings</small> · ${SS.pt_up}↑ ${SS.pt_down}↓ <small class="mut">PTs</small></div>avg PT change ${fp(SS.pt_avg)} · ${SS.notes30} notes (prior ${SS.notes_prior30}/mo) · ${SS.firms30} firms</div>`
        :`<div class="it"><div class="l">Sell-side</div><div class="v">–</div><span class="mut">no parsed broker notes</span></div>`;
  info.innerHTML=h;
  read.innerHTML=R?`<b>Today's desk read:</b> ${esc(R.signal||'')} — ${esc(R.why||'')}`:'';
 }
 function draw(){
  const t=sel.value, T=S.tickers[t]; if(!T) return; strip(t);
  const N=S.dates.length, last=S.dates[N-1]; const cut=new Date(new Date(last).getTime()-range*864e5).toISOString().slice(0,10);
  let i0=S.dates.findIndex(d=>d>=cut); if(i0<0) i0=0; const idx=[]; for(let i=i0;i<N;i++) idx.push(i);
  const W=Math.max(320,box.clientWidth||900), ml=48, mr=74, ph=[170,120,110], gap=30, top=12; const H=top+ph[0]+ph[1]+ph[2]+gap*3;
  const X=k=>ml+k/(Math.max(1,idx.length-1))*(W-ml-mr);
  const px=idx.map(i=>T.px[i]), q=idx.map(i=>S.qqq?S.qqq[i]:null);
  const first=a=>a.find(v=>v!=null); const p0=first(px), q0=first(q);
  const rp=px.map(v=>v==null||!p0?null:v/p0*100), rq=q.map(v=>v==null||!q0?null:v/q0*100);
  const tw=idx.map(i=>T.tw[i]), tw7=ma(tw,7), xo=idx.map(i=>T.x[i]), ts7=ma(idx.map(i=>T.ts[i]),7), ns7=ma(idx.map(i=>T.ns[i]),7);
  let s=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(t)} daily price, X posts and tone">`;
  const path=(a,Y)=>{let d='',pen=false;a.forEach((v,k)=>{if(v==null){return;}d+=(pen?'L':'M')+X(k).toFixed(1)+','+Y(v).toFixed(1);pen=true;});return d;};
  // panel 1: price vs QQQ
  let y0=top, vals=rp.concat(rq).filter(v=>v!=null), lo=Math.min(...vals), hi=Math.max(...vals); if(!vals.length){lo=90;hi=110;} const pad=(hi-lo)*.08||2; lo-=pad; hi+=pad;
  const Y1=v=>y0+18+(hi-v)/(hi-lo)*(ph[0]-18);
  s+=`<text x="${ml}" y="${y0+10}" font-size="11.5" fill="var(--ink2)">Price, rebased to 100 on ${esc(S.dates[idx[0]])} (local ccy) — <tspan fill="var(--ink)">${esc(t)}</tspan> vs <tspan fill="var(--muted)">QQQ (dashed)</tspan></text>`;
  [lo+pad,100,hi-pad].forEach(v=>{s+=`<line x1="${ml}" x2="${W-mr}" y1="${Y1(v)}" y2="${Y1(v)}" stroke="var(--grid)" ${v===100?'':'stroke-dasharray="3 4"'}/><text x="${ml-6}" y="${Y1(v)+3}" font-size="10" fill="var(--muted)" text-anchor="end">${v.toFixed(0)}</text>`;});
  s+=`<path d="${path(rq,Y1)}" fill="none" stroke="var(--muted)" stroke-width="1.4" stroke-dasharray="4 3"/><path d="${path(rp,Y1)}" fill="none" stroke="var(--ink)" stroke-width="2"/>`;
  const lp=[...rp].reverse().find(v=>v!=null), lq=[...rq].reverse().find(v=>v!=null);
  if(lp!=null) s+=`<text x="${W-mr+4}" y="${Y1(lp)+4}" font-size="10.5" font-weight="700" fill="var(--ink)">${f1(lp-100,1)}%</text>`;
  if(lq!=null) s+=`<text x="${W-mr+4}" y="${Y1(lq)+14}" font-size="10" fill="var(--muted)">QQQ ${f1(lq-100,1)}%</text>`;
  // panel 2: X posts
  y0=top+ph[0]+gap; const twm=Math.max(1,...tw.filter(v=>v!=null)); const Y2=v=>y0+ph[1]-(v/twm)*(ph[1]-18); const bw=Math.max(1,(W-ml-mr)/idx.length*.7);
  const xom=Math.max(1,...xo.filter(v=>v!=null)); const Y2b=v=>y0+ph[1]-(v/xom)*(ph[1]-18);
  s+=`<text x="${ml}" y="${y0+10}" font-size="11.5" fill="var(--ink2)">X posts per day — <tspan fill="var(--s1)">Bloomberg, all of X (bars, 7-day line)</tspan> · <tspan fill="var(--s4)">curated handles (right axis)</tspan></text>`;
  tw.forEach((v,k)=>{if(v!=null) s+=`<rect x="${(X(k)-bw/2).toFixed(1)}" y="${Y2(v).toFixed(1)}" width="${bw.toFixed(1)}" height="${(y0+ph[1]-Y2(v)).toFixed(1)}" fill="var(--s1)" opacity=".28"/>`;});
  s+=`<path d="${path(tw7,Y2)}" fill="none" stroke="var(--s1)" stroke-width="1.8"/>`;
  if(xo.some(v=>v)) s+=`<path d="${path(xo,Y2b)}" fill="none" stroke="var(--s4)" stroke-width="1.5"/><text x="${W-mr+4}" y="${Y2b(xom)+8}" font-size="10" fill="var(--s4)">${xom.toFixed(0)}</text>`;
  s+=`<text x="${ml-6}" y="${y0+ph[1]}" font-size="10" fill="var(--muted)" text-anchor="end">0</text><text x="${ml-6}" y="${Y2(twm)+8}" font-size="10" fill="var(--muted)" text-anchor="end">${twm>=1000?(twm/1000).toFixed(1)+'k':twm.toFixed(0)}</text>`;
  // panel 3: tone
  y0=top+ph[0]+ph[1]+gap*2; const tv=ts7.concat(ns7).filter(v=>v!=null); const tm=Math.max(.05,...tv.map(Math.abs)); const Y3=v=>y0+18+(1-v/tm)/2*(ph[2]-18);
  s+=`<text x="${ml}" y="${y0+10}" font-size="11.5" fill="var(--ink2)">Sentiment, 7-day mean — <tspan fill="var(--s1)">Bloomberg Twitter</tspan> · <tspan fill="var(--s2)">Bloomberg news</tspan></text>`;
  s+=`<line x1="${ml}" x2="${W-mr}" y1="${Y3(0)}" y2="${Y3(0)}" stroke="var(--base)"/><text x="${ml-6}" y="${Y3(tm)+4}" font-size="10" fill="var(--muted)" text-anchor="end">+${tm.toFixed(2)}</text><text x="${ml-6}" y="${Y3(-tm)+4}" font-size="10" fill="var(--muted)" text-anchor="end">−${tm.toFixed(2)}</text>`;
  s+=`<path d="${path(ns7,Y3)}" fill="none" stroke="var(--s2)" stroke-width="1.5"/><path d="${path(ts7,Y3)}" fill="none" stroke="var(--s1)" stroke-width="2"/>`;
  // x axis: month ticks
  let lastM=''; idx.forEach((i,k)=>{const m=S.dates[i].slice(0,7); if(m!==lastM){lastM=m; if(k>0||idx.length<40) s+=`<line x1="${X(k)}" x2="${X(k)}" y1="${top}" y2="${H-14}" stroke="var(--grid)" stroke-dasharray="2 5"/><text x="${X(k)+3}" y="${H-3}" font-size="10" fill="var(--muted)">${range<=60?S.dates[i].slice(5):m}</text>`;}});
  s+=`<line id="dc_x" x1="0" x2="0" y1="${top}" y2="${H-14}" stroke="var(--accent)" stroke-width="1" visibility="hidden"/><rect x="${ml}" y="${top}" width="${W-ml-mr}" height="${H-top-14}" fill="transparent" id="dc_hit"/></svg>`;
  box.innerHTML=s+'<div class="dc-hover" id="dc_hv"></div>';
  const hit=document.getElementById('dc_hit'), xl=document.getElementById('dc_x'), hv=document.getElementById('dc_hv');
  hit.addEventListener('mousemove',ev=>{const r=hit.getBoundingClientRect(); const k=Math.max(0,Math.min(idx.length-1,Math.round((ev.clientX-r.left)/r.width*(idx.length-1)))); const i=idx[k];
   xl.setAttribute('x1',X(k)); xl.setAttribute('x2',X(k)); xl.setAttribute('visibility','visible');
   hv.innerHTML=`<b>${esc(S.dates[i])}</b><br>price ${T.px[i]==null?'–':T.px[i]} ${rp[k]==null?'':'('+f1(rp[k]-100,1)+'%)'} · QQQ ${rq[k]==null?'–':f1(rq[k]-100,1)+'%'}<br>X posts ${T.tw[i]==null?'–':T.tw[i].toLocaleString()} · 7d ${tw7[k]==null?'–':Math.round(tw7[k]).toLocaleString()} · curated ${T.x[i]==null?'–':T.x[i]}<br>tone ${f1(T.ts[i],2)} (7d ${f1(ts7[k],2)}) · news ${T.nw[i]==null?'–':T.nw[i]} items, tone ${f1(T.ns[i],2)}`;
   hv.style.display='block'; const bx=box.getBoundingClientRect(); let lx=ev.clientX-bx.left+14; if(lx>bx.width-260) lx=ev.clientX-bx.left-270; hv.style.left=lx+'px'; hv.style.top=(ev.clientY-bx.top+10)+'px';});
  hit.addEventListener('mouseleave',()=>{xl.setAttribute('visibility','hidden');hv.style.display='none';});
 }
 function syncWeekly(t){const w=document.getElementById('tk'); if(w && [...w.options].some(o=>o.value===t)){w.value=t; if(typeof renderTicker==='function') renderTicker();}}
 sel.addEventListener('change',()=>{draw();syncWeekly(sel.value);});
 document.querySelectorAll('#dc_ranges button').forEach(b=>b.addEventListener('click',()=>{range=+b.dataset.r; document.querySelectorAll('#dc_ranges button').forEach(x=>x.classList.toggle('on',x===b)); draw();}));
 window.addEventListener('resize',()=>{ if(document.getElementById('tab-names').classList.contains('on')) draw(); });
 document.addEventListener('click',ev=>{const a=ev.target.closest('a.tkl'); if(!a) return; const t=a.dataset.tk; if(!S.tickers[t]) return; ev.preventDefault(); sel.value=t; syncWeekly(t); location.hash='names'; show('names',false); draw(); document.getElementById('stock').scrollIntoView({block:'start'});});
 draw(); syncWeekly(sel.value);
 // theme persistence (same key as the other wiki dashboards)
 const tb=document.querySelector('.or-theme'); if(tb){const root=document.documentElement; tb.setAttribute('aria-pressed',String(root.dataset.theme==='dark')); tb.addEventListener('click',()=>{try{localStorage.setItem('wiki-dash-theme',root.dataset.theme||'light');}catch(e){}});}
})();
"""


if __name__ == "__main__":
    sys.exit(main())
