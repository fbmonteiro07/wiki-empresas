"""build_sentiment_monitor.py — the daily SENTIMENT MONITOR: one page that aggregates
the three sentiment surfaces (hot/cold × bull/bear panel, the Sentiment Radar /
attention family, the CNN Fear & Greed study) into a visual daily read.

Sections
  01 Market mood      CNN Fear & Greed gauge + 7 components + 12-month strip, what SPY/QQQ did
                      in the following 5 sessions from the current band (2021→ study),
                      universe breadth (EPS revisions, rating drift, tweet tone, sell-side actions).
  02 Movers           who is getting hotter / colder on the daily tweet corpus (7-day attention
                      vs the prior 4 weeks, z-scored across the universe, Δ vs a week earlier),
                      with tone, the stock's move over the same window and a 35-day sparkline.
  03 Windows          what usually happens next: quadrant forward returns (hot/cold × bull/bear,
                      Bloomberg track 2024→) and the "turned hot / turned cold" event stats.
  04 Map              HOT × BULL scatter of the latest weekly panel, quadrant-coloured.
  05 Daily note       generated narrative (numbers from the sections) + an optional hand/LLM
                      note from _data/sentiment/daily_note.md.
  06 Sources          freshness of every feed (tweets, sell-side mail, Bloomberg, CNN, panel) with
                      hand-written status notes from _data/sentiment/status_notes.json.

Inputs  (all under _wiki/_data/sentiment/, written by build_sentiment.py / the 17:40 sweep):
  panel_weekly.json, panel_long.json, tweet_daily.json, sellside_daily.json, bbg_history.json
  + CNN Fear & Greed pulled live (production.dataviz.cnn.io, browser headers, unverified TLS
  because of the corporate proxy; fail-soft to the cache cnn_fg.json). The 2021→2026 forward-
  return study is seeded once from the embedded payload of attention-sentiment/cnn-next-week.html.
Outputs _dashboards/sentiment-monitor.html · _data/sentiment/cnn_fg.json (cache)
        _data/sentiment/monitor.json (numbers) · _data/sentiment/monitor_note.md (the daily note,
        for the Twitter wrap e-mail).
stdlib only. Read-only on pages. Runs in refresh_features.py right after build_sentiment.py.
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

e = html.escape


def J(name):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def pct(x, d=1):
    return "–" if x is None else f"{x * 100:+.{d}f}%"


def fnum(x, d=2):
    return "–" if x is None else f"{x:+.{d}f}"


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


def seed_cnn_study(cache: dict) -> None:
    """One-off: lift the 2021→2026 daily F&G series + the 5-session forward-return study out of the
    embedded payload of the retained Fear & Greed page, so the monitor does not depend on that page."""
    if cache.get("study") or not CNN_SEED_PAGE.exists():
        return
    try:
        t = CNN_SEED_PAGE.read_text(encoding="utf-8", errors="replace")
        big = max(re.findall(r"<script[^>]*>(.*?)</script>", t, re.S), key=len)
        m = re.search(r'atob\("([A-Za-z0-9+/=]+)"\)', big)
        j = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode("utf-8"))
        obs = j["observations"]
        study = {"asof": j["meta"].get("end"), "horizon_sessions": j["meta"].get("horizon_sessions", 5), "source": j["meta"].get("cnn_url", "CNN"),
                 "spy": [[o["date"], round(o["fg"], 2), round(o["return_pct"], 3)] for o in obs["SPY"]["close"]],
                 "qqq": [[o["date"], round(o["fg"], 2), round(o["return_pct"], 3)] for o in obs["QQQ"]["close"]]}
        cache["study"] = study
        hist = cache.setdefault("history", {})
        for d, fg, _ in study["spy"]:
            hist.setdefault(d, fg)
        cache["seeded_from"] = str(CNN_SEED_PAGE.name) + " (" + str(j["meta"].get("generated_utc", ""))[:10] + ")"
        print(f"  cnn: seeded {len(study['spy'])} study rows + history from {CNN_SEED_PAGE.name}")
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
        return cache, "live"
    except Exception as ex:  # noqa: BLE001
        return cache, f"cache ({type(ex).__name__}: {str(ex)[:60]})"


def band_stats(rows, lo, hi):
    r = [x[2] for x in rows if lo <= x[1] < hi]
    if len(r) < 10:
        return None
    return {"n": len(r), "mean": mean(r), "median": median(r), "hit": sum(1 for v in r if v > 0) / len(r),
            "p10": pctile(r, 0.10), "p90": pctile(r, 0.90)}


# ----------------------------------------------------------------------------- SVG helpers
def svg_gauge(v, w=260):
    """Semicircular 0-100 gauge, needle at v."""
    cx, cy, R = w / 2, w / 2 - 10, w / 2 - 22
    segs = [(0, 25, "var(--crit)"), (25, 45, "color-mix(in srgb,var(--crit) 55%,var(--s4))"), (45, 55, "var(--base)"),
            (55, 75, "color-mix(in srgb,var(--good) 55%,var(--s4))"), (75, 100, "var(--good)")]
    def pt(val, rad):
        a = math.pi * (1 - val / 100)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)
    s = [f"<svg viewBox='0 0 {w} {w/2+18}' width='{w}' height='{w/2+18}' role='img' aria-label='Fear and Greed gauge'>"]
    for lo, hi, col in segs:
        x0, y0 = pt(lo, R); x1, y1 = pt(hi, R)
        s.append(f"<path d='M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}' fill='none' stroke='{col}' stroke-width='16' stroke-linecap='butt' opacity='.85'/>")
    if v is not None:
        x, y = pt(v, R - 4)
        s.append(f"<line x1='{cx}' y1='{cy}' x2='{x:.1f}' y2='{y:.1f}' stroke='var(--ink)' stroke-width='3' stroke-linecap='round'/>")
        s.append(f"<circle cx='{cx}' cy='{cy}' r='5' fill='var(--ink)'/>")
    for val, lab in ((0, "0"), (25, "25"), (50, "50"), (75, "75"), (100, "100")):
        x, y = pt(val, R + 18)
        s.append(f"<text x='{x:.1f}' y='{y + 4:.1f}' font-size='10' text-anchor='middle' fill='var(--muted)'>{lab}</text>")
    s.append(f"<text x='{cx}' y='{cy - 14}' font-size='30' font-weight='650' text-anchor='middle' fill='var(--ink)'>{'–' if v is None else f'{v:.0f}'}</text>")
    s.append(f"<text x='{cx}' y='{cy + 4}' font-size='11' text-anchor='middle' fill='var(--muted)' style='text-transform:uppercase;letter-spacing:.8px'>{e(cnn_rating(v))}</text>")
    s.append("</svg>")
    return "".join(s)


def svg_strip(series: list[tuple[str, float]], w=640, h=120, bands=((0, 25), (75, 100))):
    """Line strip 0-100 with fear/greed bands shaded."""
    if not series:
        return ""
    ml, mr, mt, mb = 28, 8, 8, 20
    W, H = w - ml - mr, h - mt - mb
    n = len(series)
    X = lambda i: ml + (i / max(1, n - 1)) * W
    Y = lambda v: mt + (1 - v / 100) * H
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' preserveAspectRatio='none' class='strip'>"]
    s.append(f"<rect x='{ml}' y='{Y(100)}' width='{W}' height='{Y(75)-Y(100)}' fill='var(--good)' opacity='.08'/>")
    s.append(f"<rect x='{ml}' y='{Y(25)}' width='{W}' height='{Y(0)-Y(25)}' fill='var(--crit)' opacity='.08'/>")
    for lv in (25, 50, 75):
        s.append(f"<line x1='{ml}' x2='{ml+W}' y1='{Y(lv)}' y2='{Y(lv)}' stroke='var(--grid)' stroke-dasharray='3 4'/>")
        s.append(f"<text x='{ml-4}' y='{Y(lv)+3}' font-size='9' text-anchor='end' fill='var(--muted)'>{lv}</text>")
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(series))
    s.append(f"<polyline points='{pts}' fill='none' stroke='var(--s1)' stroke-width='1.8' vector-effect='non-scaling-stroke'/>")
    xl, vl = X(n - 1), series[-1][1]
    s.append(f"<circle cx='{xl:.1f}' cy='{Y(vl):.1f}' r='3.5' fill='var(--s1)'/>")
    step = max(1, n // 6)
    for i in range(0, n, step):
        s.append(f"<text x='{X(i):.1f}' y='{h-6}' font-size='9' text-anchor='middle' fill='var(--muted)'>{series[i][0][:7]}</text>")
    s.append("</svg>")
    return "".join(s)


def svg_spark(vals: list[float], w=120, h=28, color="var(--s1)"):
    if not vals or max(vals) <= 0:
        return f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}'></svg>"
    mx = max(vals); n = len(vals)
    pts = " ".join(f"{(i/(max(1,n-1)))*w:.1f},{h - (v/mx)*(h-3) - 1:.1f}" for i, v in enumerate(vals))
    last_x = w; last_y = h - (vals[-1] / mx) * (h - 3) - 1
    return (f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}' class='spark'><polyline points='{pts}' fill='none' stroke='{color}' stroke-width='1.5'/>"
            f"<circle cx='{last_x:.1f}' cy='{last_y:.1f}' r='2.2' fill='{color}'/></svg>")


def svg_band_bars(stats_by_band: list[tuple[str, dict | None]], current: str | None, w=640, h=170):
    """Mean next-5-session return per F&G band (bars) + hit rate (text)."""
    ml, mr, mt, mb = 40, 8, 14, 34
    W, H = w - ml - mr, h - mt - mb
    vals = [b["mean"] for _, b in stats_by_band if b]
    if not vals:
        return ""
    vmax = max(abs(v) for v in vals) or 1
    n = len(stats_by_band); bw = W / n
    Y0 = mt + H / 2
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' class='bands'>"]
    s.append(f"<line x1='{ml}' x2='{ml+W}' y1='{Y0}' y2='{Y0}' stroke='var(--grid)'/>")
    for i, (lab, b) in enumerate(stats_by_band):
        x = ml + i * bw
        if b:
            hgt = (b["mean"] / vmax) * (H / 2 - 6)
            col = "var(--s1)" if b["mean"] >= 0 else "var(--crit)"
            op = "1" if lab == current else ".45"
            y = Y0 - hgt if hgt > 0 else Y0
            s.append(f"<rect x='{x+6:.1f}' y='{y:.1f}' width='{bw-12:.1f}' height='{abs(hgt):.1f}' fill='{col}' opacity='{op}' rx='2'/>")
            s.append(f"<text x='{x+bw/2:.1f}' y='{(y-4) if hgt>0 else (y+abs(hgt)+11):.1f}' font-size='9.5' text-anchor='middle' fill='var(--ink2)'>{b['mean']:+.1f}% · {b['hit']*100:.0f}%</text>")
        if lab == current:
            s.append(f"<rect x='{x+1:.1f}' y='{mt}' width='{bw-2:.1f}' height='{H}' fill='none' stroke='var(--accent)' stroke-dasharray='3 3'/>")
        s.append(f"<text x='{x+bw/2:.1f}' y='{h-18}' font-size='10' text-anchor='middle' fill='var(--muted)'>{e(lab)}</text>")
    s.append(f"<text x='{ml}' y='{h-4}' font-size='9.5' fill='var(--muted)'>bars: mean SPY return over the next 5 sessions · label: mean · % positive · dashed box: today's band</text>")
    s.append("</svg>")
    return "".join(s)


def svg_scatter(points: list[dict], w=760, h=440):
    """HOT (x) × BULL (y) scatter, quadrant-coloured, labelled extremes."""
    ml, mr, mt, mb = 40, 16, 16, 34
    W, H = w - ml - mr, h - mt - mb
    xs = [p["x"] for p in points]; ys = [p["y"] for p in points]
    lo, hi = min(-3.2, min(xs)), max(3.2, max(xs)); lo2, hi2 = min(-3.2, min(ys)), max(3.2, max(ys))
    X = lambda v: ml + (v - lo) / (hi - lo) * W
    Y = lambda v: mt + (1 - (v - lo2) / (hi2 - lo2)) * H
    mx, my = median(xs) or 0, median(ys) or 0
    s = [f"<svg viewBox='0 0 {w} {h}' width='100%' height='{h}' class='scatter'>"]
    s.append(f"<rect x='{X(mx):.1f}' y='{mt}' width='{ml+W-X(mx):.1f}' height='{Y(my)-mt:.1f}' fill='var(--s4)' opacity='.07'/>")
    s.append(f"<rect x='{ml}' y='{Y(my):.1f}' width='{X(mx)-ml:.1f}' height='{mt+H-Y(my):.1f}' fill='var(--s1)' opacity='.07'/>")
    s.append(f"<line x1='{X(mx):.1f}' x2='{X(mx):.1f}' y1='{mt}' y2='{mt+H}' stroke='var(--base)' stroke-dasharray='4 4'/>")
    s.append(f"<line x1='{ml}' x2='{ml+W}' y1='{Y(my):.1f}' y2='{Y(my):.1f}' stroke='var(--base)' stroke-dasharray='4 4'/>")
    s.append(f"<text x='{ml+W-4}' y='{mt+12}' font-size='10' text-anchor='end' fill='var(--s4)' font-weight='700'>HOT · BULL</text>")
    s.append(f"<text x='{ml+4}' y='{mt+H-6}' font-size='10' fill='var(--s1)' font-weight='700'>COLD · BEAR</text>")
    s.append(f"<text x='{ml+W-4}' y='{mt+H-6}' font-size='10' text-anchor='end' fill='var(--muted)' font-weight='700'>HOT · BEAR</text>")
    s.append(f"<text x='{ml+4}' y='{mt+12}' font-size='10' fill='var(--muted)' font-weight='700'>COLD · BULL</text>")
    for p in points:
        col = {"hot-bull": "var(--s4)", "cold-bear": "var(--s1)"}.get(p["q"], "var(--muted)")
        s.append(f"<circle cx='{X(p['x']):.1f}' cy='{Y(p['y']):.1f}' r='{4.5 if p.get('label') else 3}' fill='{col}' opacity='.85'><title>{e(p['t'])} · HOT {p['x']:+.2f} · BULL {p['y']:+.2f}{e(p.get('tip',''))}</title></circle>")
        if p.get("label"):
            s.append(f"<text x='{X(p['x'])+6:.1f}' y='{Y(p['y'])+3.5:.1f}' font-size='10' fill='var(--ink)'>{e(p['t'])}</text>")
    s.append(f"<text x='{ml+W/2}' y='{h-8}' font-size='10' text-anchor='middle' fill='var(--muted)'>HOT composite (attention + news vs trailing 4w, z) →</text>")
    s.append(f"<text transform='translate(12,{mt+H/2}) rotate(-90)' font-size='10' text-anchor='middle' fill='var(--muted)'>BULL composite (tone, EPS revisions, rating drift, sell-side) →</text>")
    s.append("</svg>")
    return "".join(s)


def hbar(v, vmax, color):
    wpct = 0 if vmax == 0 else min(100, abs(v) / vmax * 100)
    return f"<span class='hb'><i style='width:{wpct:.0f}%;background:{color}'></i></span>"


# ----------------------------------------------------------------------------- main
def main() -> int:
    pw = J("panel_weekly.json"); pl = J("panel_long.json"); td = J("tweet_daily.json"); sd = J("sellside_daily.json"); bh = J("bbg_history.json")
    if not pw:
        print("[WARN] panel_weekly.json missing — nothing to build"); return 1
    names = pw.get("names", {})
    notes = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}

    # ---- CNN ----
    cache = json.loads(CNN_CACHE.read_text(encoding="utf-8")) if CNN_CACHE.exists() else {}
    seed_cnn_study(cache)
    cache, cnn_status = fetch_cnn(cache)
    CNN_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    now = cache.get("now", {}); fg = now.get("score")
    hist = sorted(cache.get("history", {}).items())
    strip = [(d, v) for d, v in hist if d >= (TODAY - dt.timedelta(days=365)).isoformat()]
    cnn_through = hist[-1][0] if hist else None
    study = cache.get("study")
    bands = [(f"{lo}–{lo+10}", band_stats(study["spy"], lo, lo + 10) if study else None) for lo in range(0, 100, 10)]
    cur_band = None if fg is None else f"{int(fg//10)*10}–{int(fg//10)*10+10}"
    cur_stats = next((b for lab, b in bands if lab == cur_band), None)
    cur_stats_q = band_stats(study["qqq"], int(fg // 10) * 10, int(fg // 10) * 10 + 10) if (study and fg is not None) else None
    fear_entries = band_stats(study["spy"], 0, 25) if study else None
    greed_entries = band_stats(study["spy"], 75, 101) if study else None

    # ---- universe breadth (latest weekly panel) ----
    wk = pw["weeks"][-1]; row = pw["panel"][wk]
    n_names = len(row)
    def share(cond):
        xs = [cond(r) for r in row.values()]
        xs = [x for x in xs if x is not None]
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
    px_through = None
    if bh:
        px_through = max((max(s["PX_LAST"]) for s in bh["series"].values() if s.get("PX_LAST")), default=None)
    tw_age, ss_age, px_age, cnn_age = age_days(tw_through), age_days(ss_through), age_days(px_through), age_days(cnn_through)
    tweets_fresh = tw_age is not None and tw_age <= 4

    # ---- movers: daily attention momentum on the tweet corpus ----
    movers_rows = []
    if td and tw_through:
        D = d_iso(tw_through)
        def window_sum(days: dict, a: dt.date, b: dt.date, key="m_cur"):
            tot, cnt = 0.0, 0
            for dstr, r in days.items():
                dd = d_iso(dstr)
                if a <= dd <= b:
                    tot += r.get(key, 0) or 0; cnt += 1
            return tot
        def mom(days, end):
            a7 = window_sum(days, end - dt.timedelta(days=6), end) / 7
            b28 = window_sum(days, end - dt.timedelta(days=34), end - dt.timedelta(days=7)) / 28
            return (a7, b28, math.log((a7 + 0.2) / (b28 + 0.2)))
        cur, prev, meta = {}, {}, {}
        for t, days in td["tickers"].items():
            a7, b28, m1 = mom(days, D)
            if a7 + b28 <= 0:
                continue
            cur[t] = m1
            prev[t] = mom(days, D - dt.timedelta(days=7))[2]
            bull = window_sum(days, D - dt.timedelta(days=6), D, "bull"); bear = window_sum(days, D - dt.timedelta(days=6), D, "bear")
            spark = [window_sum(days, D - dt.timedelta(days=k), D - dt.timedelta(days=k)) for k in range(34, -1, -1)]
            meta[t] = {"a7": a7, "b28": b28, "bull": bull, "bear": bear, "spark": spark}
        zc, zp = zscores(cur), zscores(prev)
        px = (bh or {}).get("series", {})
        def ret(t, end, k):
            s = px.get(t, {}).get("PX_LAST", {})
            if not s:
                return None
            ds = sorted(s)
            def last_on(dd):
                c = [x for x in ds if x <= dd.isoformat()]
                return s[c[-1]] if c else None
            p1, p0 = last_on(end), last_on(end - dt.timedelta(days=k))
            return None if not (p1 and p0) else p1 / p0 - 1
        for t in cur:
            z1, z0 = zc.get(t), zp.get(t)
            if z1 is None or z0 is None:
                continue
            m = meta[t]
            movers_rows.append({"t": t, "name": names.get(t, t), "z": z1, "dz": z1 - z0, "a7": m["a7"], "b28": m["b28"],
                                "bull": m["bull"], "bear": m["bear"], "tone": (m["bull"] / (m["bull"] + m["bear"])) if (m["bull"] + m["bear"]) >= 3 else None,
                                "r7": ret(t, D, 7), "r28": ret(t, D, 28), "spark": m["spark"]})
    MIN_VOL = 1.5   # mentions/day in either window — below this the log-ratio is noise
    eligible = [r for r in movers_rows if max(r["a7"], r["b28"]) >= MIN_VOL]
    rising = sorted([r for r in eligible if r["dz"] > 0], key=lambda r: -r["dz"])[:8]
    falling = sorted([r for r in eligible if r["dz"] < 0], key=lambda r: r["dz"])[:8]
    hottest = sorted(eligible, key=lambda r: -r["z"])[:8]

    # ---- windows: quadrant forward returns + turned hot / cold (Bloomberg track, long panel) ----
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
                if a < m0 and b >= p80:
                    for h in hot_ev:
                        v = r.get(f"rel_ret_{h}")
                        if v is not None: hot_ev[h].append(v)
                if a >= m0 and b <= p20:
                    for h in cold_ev:
                        v = r.get(f"rel_ret_{h}")
                        if v is not None: cold_ev[h].append(v)
        st = lambda xs: None if len(xs) < 8 else {"n": len(xs), "mean": mean(xs), "median": median(xs), "hit": sum(1 for v in xs if v > 0) / len(xs), "p25": pctile(xs, .25), "p75": pctile(xs, .75)}
        return {h: st(v) for h, v in hot_ev.items()}, {h: st(v) for h, v in cold_ev.items()}
    turned_hot, turned_cold = transitions(src["panel"], src["weeks"])

    # ---- map: latest own-panel week ----
    pts = []
    hs = [r["HOT"] for r in row.values() if r.get("HOT") is not None]; bs = [r["BULL"] for r in row.values() if r.get("BULL") is not None]
    hm, bm = median(hs) or 0, median(bs) or 0
    ranked = sorted((t for t in row if row[t].get("HOT") is not None and row[t].get("BULL") is not None), key=lambda t: -(abs(row[t]["HOT"] - hm) + abs(row[t]["BULL"] - bm)))
    label_set = set(ranked[:18])
    for t in ranked:
        r = row[t]
        q = ("hot" if r["HOT"] >= hm else "cold") + "-" + ("bull" if r["BULL"] >= bm else "bear")
        tip = f" · mentions/wk {r.get('m_cur', 0):.0f} · EPS rev 4w {pct(r.get('eps_rev'))} · SI {r.get('si') if r.get('si') is None else round(r['si'],1)}%"
        pts.append({"t": t, "x": r["HOT"], "y": r["BULL"], "q": q, "label": t in label_set, "tip": tip})
    q_counts = {}
    for p in pts:
        q_counts[p["q"]] = q_counts.get(p["q"], 0) + 1

    # ---- daily note (generated) ----
    note = []
    if fg is not None:
        d1w, d1m = now.get("prev_1w"), now.get("prev_1m")
        move = ""
        if d1w is not None and d1m is not None:
            move = f" — {('up' if fg >= d1w else 'down')} from {d1w:.0f} a week ago and {d1m:.0f} a month ago ({cnn_rating(d1m)})"
        note.append(f"**Market mood.** CNN Fear & Greed is at **{fg:.0f} ({cnn_rating(fg)})**{move}.")
        if cur_stats:
            note.append(f"Since 2021, when the index sat in the {cur_band} band, SPY's next five sessions averaged **{cur_stats['mean']:+.1f}%** "
                        f"(positive {cur_stats['hit']*100:.0f}% of the time, n={cur_stats['n']}; QQQ {cur_stats_q['mean']:+.1f}% / {cur_stats_q['hit']*100:.0f}%)" + ".")
        comps = cache.get("components", {})
        if comps:
            fearful = [lab for k, lab in CNN_COMPONENTS if k in comps and (comps[k].get("rating") or "").find("fear") >= 0]
            greedy = [lab for k, lab in CNN_COMPONENTS if k in comps and (comps[k].get("rating") or "").find("greed") >= 0]
            if fearful or greedy:
                note.append("Components: " + (f"fear in {', '.join(fearful)}" if fearful else "no component in fear") + ("; " if fearful and greedy else "") + (f"greed in {', '.join(greedy)}" if greedy else "") + ".")
    note.append(f"**Universe breadth (week ending {wk}, {n_names} names).** EPS revisions up for {eps_up*100:.0f}% and down for {eps_dn*100:.0f}% of the universe; "
                f"analyst rating drift positive for {rat_up*100:.0f}%; {px_up4*100:.0f}% of names up over the past 4 weeks. "
                f"Sell-side actions this week: {ss_up} names with net upgrades vs {ss_dn} with net downgrades, PT raises in {ss_pt_up} vs cuts in {ss_pt_dn}"
                + (f" (sell-side mail through {ss_through}, {ss_age} days old — treat as stale)." if ss_age and ss_age > 7 else "."))
    if movers_rows:
        fresh_txt = "" if tweets_fresh else f" ⚠ The X corpus stops on {tw_through} ({tw_age} days ago), so these are the last valid movers, not today's."
        def mv(r):
            bits = [f"**{r['t']}** ({r['dz']:+.1f}σ, {r['a7']:.1f} mentions/day vs {r['b28']:.1f})"]
            if r["tone"] is not None: bits.append(f"tone {r['tone']*100:.0f}% bull")
            if r["r7"] is not None: bits.append(f"stock {pct(r['r7'])} over the window")
            return " · ".join(bits)
        note.append(f"**Getting hotter (7-day attention vs the prior 4 weeks, through {tw_through}).** " + "; ".join(mv(r) for r in rising[:5]) + "." + fresh_txt)
        note.append("**Cooling off.** " + "; ".join(mv(r) for r in falling[:5]) + ".")
    th15, tc15 = turned_hot.get("15d"), turned_cold.get("15d")
    if th15 and tc15:
        note.append(f"**What history says about these windows (Bloomberg track, {span[0]} → {span[1]}).** Names that *turned hot* (from below the median to the top quintile in one week) "
                    f"went on to a mean **{th15['mean']*100:+.1f}%** universe-relative return over the next 15 days (positive {th15['hit']*100:.0f}%, n={th15['n']}); names that *turned cold* "
                    f"returned {tc15['mean']*100:+.1f}% (positive {tc15['hit']*100:.0f}%, n={tc15['n']}).")
    q15 = {q: quad.get(q + "|rel_ret_15d") for q in ("hot-bull", "hot-bear", "cold-bull", "cold-bear")}
    q15 = {q: s for q, s in q15.items() if s}
    if len(q15) == 4:
        best = max(q15, key=lambda q: q15[q]["mean"]); worst = min(q15, key=lambda q: q15[q]["mean"])
        note.append(f"By quadrant on 15 days, {best} has been the best state ({q15[best]['mean']*100:+.1f}%, positive {q15[best]['hit']*100:.0f}%, n={q15[best]['n']}) and {worst} the worst ({q15[worst]['mean']*100:+.1f}%, positive {q15[worst]['hit']*100:.0f}%). The spreads are a few tenths of a percent: attention tells you where the crowd is, not where the stock goes next.")
    note_md = "\n\n".join(note)
    extra_note = DAILY_NOTE.read_text(encoding="utf-8").strip() if DAILY_NOTE.exists() else ""
    extra_age = age_days(dt.datetime.fromtimestamp(DAILY_NOTE.stat().st_mtime).date().isoformat()) if DAILY_NOTE.exists() else None

    # ---- outputs: numbers + note ----
    (DATA / "monitor_note.md").write_text(f"== SENTIMENT MONITOR · {TODAY.isoformat()} ==\n\n{note_md}\n", encoding="utf-8")
    (DATA / "monitor.json").write_text(json.dumps({
        "asof": TODAY.isoformat(), "cnn": {"now": now, "components": cache.get("components", {}), "status": cnn_status, "through": cnn_through, "band": cur_band, "band_stats_spy": cur_stats, "band_stats_qqq": cur_stats_q},
        "breadth": {"week": wk, "n": n_names, "eps_up": eps_up, "eps_dn": eps_dn, "rating_up": rat_up, "tone_bull": tone_bull, "tone_n": tone_n, "ss_up": ss_up, "ss_dn": ss_dn, "ss_pt_up": ss_pt_up, "ss_pt_dn": ss_pt_dn, "px_up4w": px_up4},
        "movers": {"through": tw_through, "fresh": tweets_fresh, "rising": [{k: v for k, v in r.items() if k != "spark"} for r in rising], "falling": [{k: v for k, v in r.items() if k != "spark"} for r in falling], "hottest": [{k: v for k, v in r.items() if k != "spark"} for r in hottest]},
        "windows": {"span": span, "quadrants": quad, "turned_hot": turned_hot, "turned_cold": turned_cold},
        "freshness": {"tweets": tw_through, "sellside": ss_through, "prices": px_through, "cnn": cnn_through, "panel": pw.get("asof")},
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    # ----------------------------------------------------------------------------- HTML
    def md_inline(s):
        s = e(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
        return s
    def fresh_cls(a, warn=3, bad=7):
        return "ok" if a is not None and a <= warn else ("warn" if a is not None and a <= bad else "bad")

    comp_tiles = "".join(
        f"<div class='ctile'><div class='l'>{e(lab)}</div><div class='v {e((cache.get('components', {}).get(k, {}).get('rating') or '').replace(' ', '-'))}'>{e(cache.get('components', {}).get(k, {}).get('rating') or '–')}</div></div>"
        for k, lab in CNN_COMPONENTS)
    def stat_tile(label, st, sub=""):
        if not st:
            return f"<div class='oc-tile'><div class='l'>{e(label)}</div><div class='v'>–</div><div class='s'>{e(sub)}</div></div>"
        return (f"<div class='oc-tile'><div class='l'>{e(label)}</div><div class='v {'pos' if st['mean']>=0 else 'neg'}'>{st['mean']:+.1f}%</div>"
                f"<div class='s'>positive {st['hit']*100:.0f}% · median {st['median']:+.1f}% · p10 {st['p10']:+.1f}% / p90 {st['p90']:+.1f}% · n={st['n']}{(' · ' + sub) if sub else ''}</div></div>")

    mood = (
        "<section class='oc mon' id='mood'><p class='oc-kicker'>01 · market mood · CNN Fear & Greed + universe breadth</p>"
        f"<h2 class='oc-headline'>{'Fear & Greed at ' + f'{fg:.0f}' + ' — ' + cnn_rating(fg) if fg is not None else 'Fear & Greed unavailable'}"
        + (f", from {now['prev_1m']:.0f} a month ago" if now.get('prev_1m') is not None else "") + "</h2>"
        "<div class='mood-grid'>"
        f"<div class='card gauge'>{svg_gauge(fg)}<div class='gsub'>prev close {now.get('prev_close') if now.get('prev_close') is None else round(now['prev_close'])} · 1w ago {now.get('prev_1w') if now.get('prev_1w') is None else round(now['prev_1w'])} · 1m ago {now.get('prev_1m') if now.get('prev_1m') is None else round(now['prev_1m'])} · 1y ago {now.get('prev_1y') if now.get('prev_1y') is None else round(now['prev_1y'])}<br><span class='mut'>source CNN · {e(cnn_status)} · through {e(cnn_through or '–')}</span></div></div>"
        f"<div class='card'><h3>Twelve months</h3>{svg_strip(strip)}<div class='ctiles'>{comp_tiles}</div></div>"
        "</div>"
        "<h3>What SPY did in the following five sessions, by Fear & Greed band (2021 → " + e(study['asof'] if study else '–') + ")</h3>"
        f"<div class='card'>{svg_band_bars(bands, cur_band)}</div>"
        f"<div class='oc-tiles four'>{stat_tile(f'Today band {cur_band} · SPY next 5 sessions', cur_stats)}{stat_tile(f'Today band {cur_band} · QQQ next 5 sessions', cur_stats_q)}{stat_tile('Extreme fear (<25) · SPY next 5 sessions', fear_entries)}{stat_tile('Extreme greed (≥75) · SPY next 5 sessions', greed_entries)}</div>"
        f"<h3>Universe breadth — week ending {e(wk)}, {n_names} names</h3>"
        "<div class='oc-tiles four'>"
        f"<div class='oc-tile'><div class='l'>EPS revisions (4w)</div><div class='v'>{eps_up*100:.0f}% <small>up</small></div><div class='s'>{eps_dn*100:.0f}% down · Bloomberg BEst 1BF</div></div>"
        f"<div class='oc-tile'><div class='l'>Rating drift (4w)</div><div class='v'>{rat_up*100:.0f}% <small>improving</small></div><div class='s'>share of names with a better average rating</div></div>"
        f"<div class='oc-tile'><div class='l'>Sell-side actions (week)</div><div class='v'>{ss_up} <small>↑</small> / {ss_dn} <small>↓</small></div><div class='s'>net upgrades vs downgrades · PT raises {ss_pt_up} / cuts {ss_pt_dn}" + (f" · <b class='bad'>mail through {ss_through}</b>" if ss_age and ss_age > 7 else "") + "</div></div>"
        f"<div class='oc-tile'><div class='l'>Price breadth (4w)</div><div class='v'>{px_up4*100:.0f}% <small>up</small></div><div class='s'>names with a positive 4-week return · tweet tone bullish in {('–' if tone_bull is None else f'{tone_bull*100:.0f}%')} of {tone_n} names with tone</div></div>"
        "</div></section>")

    def mover_rows(rows, color):
        vmax = max((abs(r["dz"]) for r in rows), default=1) or 1
        out = []
        for r in rows:
            tone = "–" if r["tone"] is None else f"{r['tone']*100:.0f}% bull"
            out.append(f"<tr><td class='tk'>{e(r['t'])}<small>{e(r['name'][:28])}</small></td>"
                       f"<td class='bar'>{hbar(r['dz'], vmax, color)}<b>{r['dz']:+.1f}σ</b></td>"
                       f"<td class='r'>{r['z']:+.1f}</td><td class='r'>{r['a7']:.1f} <small>vs {r['b28']:.1f}</small></td><td class='r'>{tone}</td>"
                       f"<td class='r {'pos' if (r['r7'] or 0) >= 0 else 'neg'}'>{pct(r['r7'])}</td><td class='r {'pos' if (r['r28'] or 0) >= 0 else 'neg'}'>{pct(r['r28'])}</td><td>{svg_spark(r['spark'], color=color)}</td></tr>")
        return "".join(out)
    thead = "<thead><tr><th>Name</th><th>Δ attention (z, vs a week earlier)</th><th class='r'>HOT z</th><th class='r'>mentions/day · 7d vs 4w</th><th class='r'>tone 7d</th><th class='r'>stock 7d</th><th class='r'>stock 4w</th><th>35 days</th></tr></thead>"
    movers = (
        "<section class='oc mon' id='movers'><p class='oc-kicker'>02 · movers · who is getting hotter or colder</p>"
        f"<h2 class='oc-headline'>Attention movers through {e(tw_through or '–')}" + ("" if tweets_fresh else f" <span class='stale-tag'>⚠ X corpus {tw_age} days old</span>") + "</h2>"
        "<p class='oc-sub'>Curated X mentions per day over the last 7 days against the prior 4 weeks, log-ratio z-scored across the universe (HOT z). Δ is the change in that z versus the same measure a week earlier: the names whose attention is accelerating, and the ones going quiet. "
        "Tone = share of bullish-lexicon tweets. Stock = price change over the same 7 days / 4 weeks (Bloomberg, through " + e(px_through or '–') + ").</p>"
        "<div class='grid2'>"
        f"<div class='card'><h3>Getting hotter</h3><table class='mv'>{thead}<tbody>{mover_rows(rising, 'var(--s4)')}</tbody></table></div>"
        f"<div class='card'><h3>Cooling off</h3><table class='mv'>{thead}<tbody>{mover_rows(falling, 'var(--s1)')}</tbody></table></div>"
        "</div>"
        f"<h3>Hottest right now (HOT z level)</h3><div class='card'><table class='mv'>{thead}<tbody>{mover_rows(hottest, 'var(--accent)')}</tbody></table></div>"
        "</section>")

    def quad_cell(k):
        s = quad.get(k)
        if not s:
            return "<td>–</td>"
        cls = "pos" if s["mean"] >= 0 else "neg"
        return f"<td class='{cls}'><b>{s['mean']*100:+.1f}%</b><small>hit {s['hit']*100:.0f}% · n={s['n']}</small></td>"
    def ev_cell(st):
        if not st:
            return "<td>–</td>"
        cls = "pos" if st["mean"] >= 0 else "neg"
        return f"<td class='{cls}'><b>{st['mean']*100:+.1f}%</b><small>median {st['median']*100:+.1f}% · hit {st['hit']*100:.0f}% · p25/p75 {st['p25']*100:+.1f}/{st['p75']*100:+.1f} · n={st['n']}</small></td>"
    windows = (
        "<section class='oc mon' id='windows'><p class='oc-kicker'>03 · windows · what usually happens next</p>"
        f"<h2 class='oc-headline'>Forward universe-relative returns after a sentiment state — Bloomberg track, {e(span[0])} → {e(span[1])}</h2>"
        "<p class='oc-sub'>Weekly panel, returns relative to the universe mean so the market's own move cancels out. Quadrants are cut at each week's medians of HOT and BULL. 'Turned hot' = below the median one week, top quintile the next; 'turned cold' = the mirror image.</p>"
        "<div class='grid2'>"
        "<div class='card'><h3>Quadrant this week → next 1w / 15d / 4w</h3><table class='qd'><thead><tr><th></th><th>1 week</th><th>15 days</th><th>4 weeks</th></tr></thead><tbody>"
        + "".join(f"<tr><th>{lab}</th>{quad_cell(q+'|rel_ret_1w')}{quad_cell(q+'|rel_ret_15d')}{quad_cell(q+'|rel_ret_4w')}</tr>" for q, lab in (("hot-bull", "Hot · bull"), ("hot-bear", "Hot · bear"), ("cold-bull", "Cold · bull"), ("cold-bear", "Cold · bear")))
        + "</tbody></table></div>"
        "<div class='card'><h3>Turned hot / turned cold this week → next 1w / 15d / 4w</h3><table class='qd'><thead><tr><th></th><th>1 week</th><th>15 days</th><th>4 weeks</th></tr></thead><tbody>"
        f"<tr><th>Turned hot</th>{ev_cell(turned_hot.get('1w'))}{ev_cell(turned_hot.get('15d'))}{ev_cell(turned_hot.get('4w'))}</tr>"
        f"<tr><th>Turned cold</th>{ev_cell(turned_cold.get('1w'))}{ev_cell(turned_cold.get('15d'))}{ev_cell(turned_cold.get('4w'))}</tr>"
        "</tbody></table><p class='note'>Small-sample caution: both tables describe averages across many names and weeks; dispersion (p25/p75) is wide and the signal has not been a reliable timing tool — see the backtest page for the IC history.</p></div>"
        "</div></section>")

    map_sec = (
        "<section class='oc mon' id='map'><p class='oc-kicker'>04 · map · where every name sits this week</p>"
        f"<h2 class='oc-headline'>HOT × BULL, week ending {e(wk)} — " + " · ".join(f"{q_counts.get(q,0)} {q}" for q in ("hot-bull", "hot-bear", "cold-bull", "cold-bear")) + "</h2>"
        + ("" if tweets_fresh else f"<p class='oc-sub stale-tag'>⚠ The HOT axis rides on the X corpus, which stops on {e(tw_through or '–')}: names with zero recent mentions read as extremely cold this week. Read the BULL axis (EPS revisions, rating drift, sell-side) and wait for the feed to resume before trusting the hot side.</p>")
        + f"<div class='card'>{svg_scatter(pts)}</div></section>")

    note_sec = (
        "<section class='oc mon' id='note'><p class='oc-kicker'>05 · daily note · generated from the numbers above</p>"
        f"<h2 class='oc-headline'>The read for {TODAY.isoformat()}</h2>"
        "<div class='card note-card'>" + "".join(f"<p>{md_inline(p)}</p>" for p in note) + "</div>"
        + (f"<h3>Analyst note <small class='mut'>(_data/sentiment/daily_note.md, {extra_age} days old)</small></h3><div class='card note-card extra'>" + "".join(f"<p>{md_inline(p)}</p>" for p in extra_note.split('\n\n')) + "</div>" if extra_note else
           "<p class='note'>Drop a markdown paragraph in <code>_data/sentiment/daily_note.md</code> (by hand or from the 09:00 Twitter-briefing task) and it renders here under the generated note.</p>")
        + "</section>")

    def src_row(label, through, age, note_key, desc):
        cls = fresh_cls(age)
        n = notes.get(note_key, "")
        return (f"<tr><td><span class='dot {cls}'></span>{e(label)}</td><td class='r'>{e(through or '–')}</td><td class='r'>{'–' if age is None else f'{age} d'}</td><td>{e(desc)}" + (f"<br><b class='{cls}'>{e(n)}</b>" if n else "") + "</td></tr>")
    sources = (
        "<section class='oc mon' id='sources'><p class='oc-kicker'>06 · sources · how fresh is each feed</p><h2 class='oc-headline'>Feeds behind this page</h2>"
        "<div class='card'><table class='src'><thead><tr><th>Feed</th><th class='r'>through</th><th class='r'>age</th><th>what it drives · status</th></tr></thead><tbody>"
        + src_row("X corpus (tweets.sqlite, twitterapi.io)", tw_through, tw_age, "tweets", "attention movers, HOT axis, tweet tone · fetched by the 09:00 twitter-briefing task")
        + src_row("Sell-side e-mail (Outlook DASL sweep)", ss_through, ss_age, "sellside", "sell-side actions, note flow, subject tone · 17:40 sweep (refresh_sentiment.bat)")
        + src_row("Bloomberg (prices, BEst EPS, ratings, SI)", px_through, px_age, "bbg", "stock moves in the windows, EPS/rating breadth · 17:40 sweep when the terminal is logged in")
        + src_row("CNN Fear & Greed", cnn_through, cnn_age, "cnn", f"market mood gauge, components, 12-month strip · pulled live at build ({e(cnn_status)})")
        + src_row("Weekly panel (build_sentiment.py)", pw.get("asof"), age_days(pw.get("asof")), "panel", "quadrants, breadth, map · 18:15 chain (own track May-2026 →; Bloomberg track 2024 → for the window stats)")
        + "</tbody></table></div>"
        "<p class='note'>Deep dives: <a href='sentiment.html'>hot/cold × bull/bear backtest</a> · <a href='attention-sentiment/index.html'>Sentiment Radar (attention, specialist sales, narratives)</a> · <a href='attention-sentiment/cnn-next-week.html'>Fear & Greed study</a> · <a href='attention-sentiment/specialist-sales.html'>specialist sales</a>.</p>"
        "</section>")

    nav = ("<div class='or-nav-group'><p>Sentiment monitor</p>"
           "<a href='#mood'><span class='or-nav-number' aria-hidden='true'>01</span>Market mood</a>"
           "<a href='#movers'><span class='or-nav-number' aria-hidden='true'>02</span>Movers</a>"
           "<a href='#windows'><span class='or-nav-number' aria-hidden='true'>03</span>Windows</a>"
           "<a href='#map'><span class='or-nav-number' aria-hidden='true'>04</span>Map</a>"
           "<a href='#note'><span class='or-nav-number' aria-hidden='true'>05</span>Daily note</a>"
           "<a href='#sources'><span class='or-nav-number' aria-hidden='true'>06</span>Sources</a></div>")
    worst = min((a for a in (tw_age, ss_age, px_age) if a is not None), default=None)
    stale_n = sum(1 for a in (tw_age, ss_age, px_age, cnn_age) if a is not None and a > 7)
    shell = (
        "<div class='or-dashboard'><a class='or-skip' href='#dashboard-main'>Skip to content</a>"
        "<aside class='or-sidebar'><a class='or-brand' href='index.html' aria-label='Wiki dashboards'>"
        "<span class='or-brand-mark' aria-hidden='true'>C</span><span>CAPSTONE<small>RESEARCH INTELLIGENCE</small></span></a>"
        f"<nav class='or-navigation' aria-label='Sections'>{nav}</nav>"
        f"<div class='or-sidebar-footer'><span class='or-status-dot'></span>Sentiment monitor<small>Generated {TODAY.isoformat()} · {stale_n} stale feed{'s' if stale_n != 1 else ''}</small>"
        "<a href='index.html'>All dashboards <span aria-hidden='true'>↗</span></a><a href='../index.html'>Back to research wiki <span aria-hidden='true'>↗</span></a></div></aside>"
        "<div class='or-workspace'><header class='or-topbar'><div><p class='or-breadcrumb'>RESEARCH / SENTIMENT</p><h1>Sentiment monitor</h1></div>"
        f"<div class='or-topbar-actions'><span class='or-asof'>Fear & Greed <b>{'–' if fg is None else f'{fg:.0f} · ' + cnn_rating(fg)}</b></span>"
        f"<span class='or-asof'>X corpus through <b>{e(tw_through or '–')}</b></span>"
        "<button type='button' class='or-theme' aria-label='Switch to dark theme' aria-pressed='false'><svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.6' aria-hidden='true'><path d='M20.5 13A8.5 8.5 0 0 1 11 3.5 8.5 8.5 0 1 0 20.5 13Z'/></svg></button>"
        "</div></header><main id='dashboard-main' class='or-main' tabindex='-1'>")

    css = r"""
.mon{margin-bottom:46px}.mon h3{margin:26px 0 10px;font-size:15px}
.mood-grid{display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:stretch}@media(max-width:900px){.mood-grid{grid-template-columns:1fr}}
.gauge{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.gsub{font-size:11px;color:var(--ink2);margin-top:6px;line-height:1.7}
.ctiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px;margin-top:12px}
.ctile{border:1px solid var(--border);border-radius:8px;padding:8px 10px;background:var(--plane)}.ctile .l{font-size:9px;letter-spacing:.5px;text-transform:uppercase;color:var(--muted)}
.ctile .v{font-size:12px;font-weight:700;margin-top:3px;text-transform:capitalize}.ctile .v.fear,.ctile .v.extreme-fear{color:var(--crit)}.ctile .v.greed,.ctile .v.extreme-greed{color:var(--good)}.ctile .v.neutral{color:var(--ink2)}
.oc-tiles.four{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:14px 0 6px}@media(max-width:1100px){.oc-tiles.four{grid-template-columns:repeat(2,minmax(0,1fr))}}
.oc-tile .v small{font-size:12px;font-weight:500;color:var(--muted);letter-spacing:0}.oc-tile .v.pos{color:var(--s1)}.oc-tile .v.neg{color:var(--crit)}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}@media(max-width:1100px){.grid2{grid-template-columns:1fr}}
.card{min-width:0;overflow:hidden}.card h3{margin-top:0}
table.mv,table.qd,table.src{width:100%;border-collapse:collapse;font-size:12px}table.mv th,table.qd th,table.src th{font-size:9.5px;letter-spacing:.4px;text-transform:uppercase;color:var(--muted);text-align:left;padding:6px 6px;border-bottom:1px solid var(--grid)}
table.mv td,table.qd td,table.src td{padding:7px 6px;border-bottom:1px solid var(--grid);vertical-align:middle}td.r,th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.tk{font-weight:700;white-space:nowrap}td.tk small{display:block;font-weight:400;color:var(--muted);font-size:10px}
td.bar{min-width:150px}.hb{display:inline-block;width:90px;height:8px;background:var(--grid);border-radius:4px;vertical-align:middle;margin-right:8px;overflow:hidden}.hb i{display:block;height:100%}
td.pos,.pos{color:var(--s1)}td.neg,.neg{color:var(--crit)}td small{display:block;color:var(--muted);font-size:10px;font-weight:400}
table.qd th{text-align:left}table.qd td{font-size:13px}
.stale-tag{color:var(--crit);font-size:12px;font-weight:600;background:color-mix(in srgb,var(--crit) 12%,var(--surf));padding:2px 8px;border-radius:8px;vertical-align:middle}
.note-card p{margin:0 0 12px;font-size:13.5px;line-height:1.8;color:var(--ink)}.note-card p:last-child{margin:0}.note-card.extra{border-left:3px solid var(--accent)}
.note{font-size:11px;color:var(--muted);line-height:1.8;margin:10px 0 0}.mut{color:var(--muted)}b.bad{color:var(--crit)}b.warn{color:var(--warn)}b.ok{color:var(--good)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;vertical-align:1px}.dot.ok{background:var(--good)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--crit)}
.or-main .oc .oc-headline{font-size:24px}.or-topbar-actions .or-asof+.or-asof{margin-left:-6px}
"""
    theme_js = r"""
(function(){var root=document.documentElement,KEY='wiki-dash-theme';var b=document.querySelector('.or-theme');if(!b)return;var d=root.dataset.theme==='dark';b.setAttribute('aria-pressed',String(d));b.setAttribute('aria-label',d?'Switch to light theme':'Switch to dark theme');b.addEventListener('click',function(){try{localStorage.setItem(KEY,root.dataset.theme||'light');}catch(e){}});})();
"""
    font = ""
    if FONT.exists():
        font = ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'
                + base64.b64encode(FONT.read_bytes()).decode() + ') format("woff2")}')
    page = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Sentiment monitor</title>"
            "<script>try{var t=localStorage.getItem('wiki-dash-theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t;}catch(e){}</script>"
            f"<style>{font}{OR_CSS}{css}</style></head><body>{shell}{mood}{movers}{windows}{map_sec}{note_sec}{sources}"
            "<p class='hub-credit note'>Built by <code>_tools/build_sentiment_monitor.py</code> from the sentiment caches in <code>_data/sentiment/</code>; CNN pulled live with a cache fallback. Numbers also in <code>monitor.json</code>; the daily note in <code>monitor_note.md</code> for the Twitter wrap.</p>"
            f"</main></div></div><script>{OR_JS}</script><script>{theme_js}</script></body></html>")
    OUT.write_text(page, encoding="utf-8")
    print(f"  -> {OUT}")
    print(f"  cnn {cnn_status}: {fg} ({cnn_rating(fg)}) through {cnn_through} · tweets through {tw_through} ({tw_age} d) · sell-side through {ss_through} ({ss_age} d) · prices through {px_through} ({px_age} d)")
    print(f"  movers: {len(rising)} rising / {len(falling)} falling · turned-hot n(15d) = {(turned_hot.get('15d') or {}).get('n')} · map {q_counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
