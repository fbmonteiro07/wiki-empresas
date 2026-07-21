r"""
build_openrouter_dash.py — render _wiki/_data/openrouter/dashboard.json into a
self-contained, theme-aware HTML dashboard at _wiki/_dashboards/openrouter.html
(also publishable as an Artifact — no external assets).

Framing hard-won from the estimate double-check:
  * implied $ = tokens x LIST price with caching OFF  =>  a CEILING, ~3x realized.
  * lead with RELATIVE RANK + PAID-token share (free tokens are excluded from the
    $-comparison base), and show a cache-sensitivity ladder that reconciles the
    ceiling toward OpenRouter's reported actual spend.

Run (after or_fetch.py + or_build.py):
  py "E:\Wiki Felipe empresas\_wiki\_tools\build_openrouter_dash.py"
"""
import json
import math
from pathlib import Path

DATA = Path("E:/Wiki Felipe empresas/_wiki/_data")
DASH = Path("E:/Wiki Felipe empresas/_wiki/_dashboards")
OR = DATA / "openrouter"

D = json.loads((OR / "dashboard.json").read_text(encoding="utf-8"))
CAP_LABEL = {"first-party": "First-party API", "open+own": "Open-weight + own API", "open-weight": "Open-weight (hosted)"}
CAP_COLOR = {"first-party": "var(--s1)", "open+own": "var(--s2)", "open-weight": "var(--s3)"}


def tok(x):
    if x >= 1e12:
        return "%.1fT" % (x / 1e12)
    if x >= 1e9:
        return "%.0fB" % (x / 1e9)
    return "%.0fM" % (x / 1e6)


def dol(x):
    if abs(x) >= 1e9:
        return "$%.2fB" % (x / 1e9)
    if abs(x) >= 1e6:
        return "$%.0fM" % (x / 1e6)
    return "$%.0fk" % (x / 1e3)


def pct(x, dp=1):
    return ("%." + str(dp) + "f%%") % (x * 100)


def esc(s):
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


import math as _m
from datetime import date as _date

_GRAD_N = [0]


def _dnum(d):
    p = (d + "-01-01")[:10].split("-")
    return _date(int(p[0]), int(p[1]), int(p[2])).toordinal()


def _smooth(P):
    """Monotone-ish cubic path through points [(x,y),...]."""
    if len(P) < 2:
        return ""
    d = ["M%.1f %.1f" % P[0]]
    for i in range(len(P) - 1):
        x0, y0 = P[i]; x1, y1 = P[i + 1]
        dx = (x1 - x0) * 0.42
        d.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (x0 + dx, y0, x1 - dx, y1, x1, y1))
    return " ".join(d)


def linechart(pts, vk, color, ylab, pts2=None, color2=None, W=1010, H=280, log=False, area=True, flags=None):
    """Polished time-series chart: real time axis, smooth curve, gradient area,
    monthly ticks, optional log scale, flagged basis-break points (hollow)."""
    pts = sorted([p for p in pts if p.get(vk)], key=lambda p: p["date"])
    pts2 = sorted([q for q in (pts2 or []) if q.get(vk) is not None], key=lambda p: p["date"])
    if not pts:
        return ""
    flags = flags or {}
    PL, PB, PT, PR = 58, 30, 16, 24
    PW, PH = W - PL - PR, H - PT - PB
    alld = [p["date"] for p in pts] + [q["date"] for q in pts2]
    x0, x1 = _dnum(min(alld)), _dnum(max(alld))
    span = max(x1 - x0, 1)
    x0 -= span * 0.03; x1 += span * 0.03
    vals = [p[vk] for p in pts] + [q[vk] for q in pts2]
    if log:
        lo = min(vals) / 1.6; hi = max(vals) * 1.6
        L0, L1 = _m.log10(lo), _m.log10(hi)
        Y = lambda v: PT + PH - (_m.log10(max(v, 1e-9)) - L0) / (L1 - L0) * PH
    else:
        hi = max(vals) * 1.18
        Y = lambda v: PT + PH - (v / hi) * PH
    X = lambda d: PL + (_dnum(d) - x0) / (x1 - x0) * PW
    _GRAD_N[0] += 1
    gid = "g%d" % _GRAD_N[0]
    s = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" font-family="system-ui,-apple-system,Segoe UI,sans-serif">' % (W, H)]
    s.append('<defs><linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity=".28"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs>' % (gid, color, color))
    # y grid
    if log:
        v = 10 ** _m.floor(_m.log10(min(vals) / 1.6))
        gv = []
        while v <= hi:
            gv.append(v); v *= 10
    else:
        gv = [hi * k / 4 for k in range(5)]
    for v in gv:
        y = Y(v) if v > 0 or log else PT + PH
        if PT - 2 <= y <= PT + PH + 2:
            s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (PL, y, PL + PW, y))
            s.append('<text x="%d" y="%.1f" fill="var(--muted)" font-size="10.5" text-anchor="end">%s</text>' % (PL - 7, y + 3, esc(ylab(v))))
    # monthly x ticks
    yy, mm = int(min(alld)[:4]), int(min(alld)[5:7])
    while (yy, mm) <= (int(max(alld)[:4]), int(max(alld)[5:7])):
        d = "%04d-%02d" % (yy, mm)
        xx = X(d)
        if PL - 2 <= xx <= PL + PW + 2:
            s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--grid)" stroke-width="1" opacity=".6"/>' % (xx, PT, xx, PT + PH))
            s.append('<text x="%.1f" y="%d" fill="var(--muted)" font-size="10.5" text-anchor="middle">%s/%02d</text>' % (xx, H - 9, ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")[mm-1], yy % 100))
        mm += 1
        if mm > 12:
            mm = 1; yy += 1
    P = [(X(p["date"]), Y(p[vk])) for p in pts]
    if area and len(P) > 1:
        s.append('<path d="%s L%.1f %.1f L%.1f %.1f Z" fill="url(#%s)" stroke="none"/>' % (_smooth(P), P[-1][0], PT + PH, P[0][0], PT + PH, gid))
    if len(P) > 1:
        s.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % (_smooth(P), color))
    for p, (xx, yv) in zip(pts, P):
        fl = flags.get(p["date"])
        if fl:
            s.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="var(--surf)" stroke="%s" stroke-width="2" stroke-dasharray="2 2"><title>%s — %s\n⚠ %s</title></circle>' % (xx, yv, color, esc(p["date"]), esc(ylab(p[vk])), esc(fl)))
        else:
            s.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="var(--surf)" stroke-width="1.5"><title>%s — %s</title></circle>' % (xx, yv, color, esc(p["date"]), esc(ylab(p[vk]))))
        s.append('<text x="%.1f" y="%.1f" fill="var(--ink)" font-size="10.5" font-weight="600" text-anchor="middle">%s</text>' % (xx, yv - 10, esc(ylab(p[vk]))))
    if pts2:
        P2 = [(X(q["date"]), Y(q[vk])) for q in pts2]
        if len(P2) > 1:
            s.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 4"/>' % (_smooth(P2), color2))
        for q, (xx, yv) in zip(pts2, P2):
            s.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"><title>%s — %s (realized)</title></circle>' % (xx, yv, color2, esc(q["date"]), esc(ylab(q[vk]))))
    s.append('</svg>')
    return "".join(s)


plat = D["platform"]
token_mom = plat.get("token_momentum_weekly")
if token_mom is None:
    token_mom_label = "n/a"
else:
    token_mom_label = (chr(9650) if token_mom >= 0 else chr(9660)) + (" %+.0f%%" % (token_mom * 100))
labs = D["labs"]
models = D["models"]
apps = D["apps"]
guards = D["guardrails"]
orr = D["anchors"]
by = {l["author"]: l for l in labs}

# ---------- history (one record per date, written deduped by or_build) ----------
HIST = []
_hp = OR / "history.jsonl"
if _hp.is_file():
    for _ln in _hp.read_text(encoding="utf-8").splitlines():
        _ln = _ln.strip()
        if _ln:
            try:
                HIST.append(json.loads(_ln))
            except ValueError:
                pass
HIST.sort(key=lambda r: r.get("date", ""))

# WoW deltas: latest vs previous snapshot ($-share and token-share, in points)
WOW = {}
if len(HIST) >= 2:
    cur_rec, prev_rec = HIST[-1], HIST[-2]
    for a, v in cur_rec.get("labs", {}).items():
        pv = prev_rec.get("labs", {}).get(a)
        if not pv or not prev_rec.get("revenue_annualized") or not cur_rec.get("revenue_annualized"):
            continue
        cur_s = v["rev_ann"] / cur_rec["revenue_annualized"]
        prev_s = pv["rev_ann"] / prev_rec["revenue_annualized"]
        cur_t = v["tok_wk"] / cur_rec["tokens_week"] if cur_rec.get("tokens_week") else 0
        prev_t = pv["tok_wk"] / prev_rec["tokens_week"] if prev_rec.get("tokens_week") else 0
        WOW[a] = {"d_rev_pp": (cur_s - prev_s) * 100, "d_tok_pp": (cur_t - prev_t) * 100}


def L(name):
    return next((l for l in labs if l["display"].startswith(name)), None)


ant, oai, ggl, dsk, xmi = L("Anthropic"), L("OpenAI"), L("Google"), L("DeepSeek"), L("Xiaomi")

# ---------- HERO TILES ----------
top_lab = labs[0]
top_app = next((a for a in apps if a.get("title")), {})
tiles = [
    ("Tokens / day", tok(plat["daily_tokens"]), "via OpenRouter · ~%s/mo · %s free" % (tok(plat["tokens_month_run_rate"]), pct(plat["free_token_pct"], 0))),
    ("Implied $ / yr", dol(plat["revenue_annualized"]), "at LIST price, caching OFF — a ceiling (~3× realized)"),
    ("Input intensity", "%.1f:1" % plat["input_ratio"], "prompt : completion · ~97% of tokens are input"),
    ("#1 by implied $", esc(top_lab["display"]), "%s/yr · %s of $ vs %s of paid tokens" % (dol(top_lab["revenue_annualized"]), pct(top_lab["rev_share"], 0), pct(top_lab["paid_token_share"], 0))),
    ("7d vs 30d token momentum", token_mom_label, "all observed text models · overlapping windows"),
    ("#1 app", esc(top_app.get("title", "-")), "%s tokens/wk · coding agents lead" % tok(top_app.get("tokens_week", 0))),
]
tiles_html = "".join('<div class="tile"><div class="tlabel">%s</div><div class="tval">%s</div><div class="tsub">%s</div></div>' % (esc(a), esc(b), esc(c)) for a, b, c in tiles)

# ---------- EXECUTIVE READ ----------
# A compact decision layer for the first viewport. Every number below already
# exists in dashboard.json; this is presentation only, not a second model.
volume_lab = max(labs, key=lambda l: l.get("paid_token_share", 0))
reported_monthly = (orr.get("reported_monthly_spend_musd") or 0) * 1e6
insights = [
    ("Value leader", top_lab["display"],
     "%s of implied dollars on %s of paid tokens" %
     (pct(top_lab["rev_share"], 0), pct(top_lab["paid_token_share"], 0)), "accent-blue"),
    ("Volume / value gap", volume_lab["display"],
     "%s of paid tokens, but %s of implied dollars" %
     (pct(volume_lab["paid_token_share"], 0), pct(volume_lab["rev_share"], 0)), "accent-pink"),
    ("Reality check", dol(reported_monthly) + "/mo realized",
     "vs %s/mo at list price with caching off" % dol(plat["revenue_month_run_rate"]), "accent-amber"),
]
insights_html = "".join(
    '<article class="insight %s"><div class="insight-kicker">%s</div>'
    '<div class="insight-value">%s</div><p>%s</p>'
    '<div class="insight-source">OpenRouter public data &middot; %s &middot; trailing 7d</div></article>' %
    (cls, esc(kicker), esc(value), esc(body), esc(D["asof"]))
    for kicker, value, body, cls in insights)

# ---------- CACHE-SENSITIVITY LADDER ----------
ladder = [
    ("Implied at list, cache-OFF", plat["revenue_month_run_rate"], "var(--warn)", "ceiling"),
    ("If 50% of input cached", plat["revenue_month_cache50"], "var(--s1)", ""),
    ("If 70% of input cached", plat["revenue_month_cache70"], "var(--s1)", ""),
    ("OpenRouter reported actual", (orr.get("reported_monthly_spend_musd") or 0) * 1e6, "var(--good)", "Jun-26"),
]
lmax = max(v for _, v, _, _ in ladder) or 1
ladder_html = "".join(
    '<div class="barrow2"><div class="barname">%s %s</div>'
    '<div class="bartrack"><div class="barfill" style="width:%.1f%%;background:%s"></div></div>'
    '<div class="barval">%s/mo</div></div>' % (
        esc(n), ('<span class="tag">%s</span>' % t) if t else "", v / lmax * 100, c, dol(v))
    for n, v, c, t in ladder)

# ---------- SCATTER: PAID token share vs $ share (log-log) ----------
sc = [l for l in labs if l["paid_token_share"] > 0 and l["rev_share"] > 0][:16]
LO, HI = 0.1, 100.0
W, H, PAD_L, PAD_B, PAD_T, PAD_R = 720, 460, 56, 46, 20, 20
PW, PH = W - PAD_L - PAD_R, H - PAD_T - PAD_B


def sx(v):
    v = max(min(v, HI), LO)
    return PAD_L + (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * PW


def sy(v):
    v = max(min(v, HI), LO)
    return PAD_T + PH - (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * PH


maxrev = max(l["revenue_annualized"] for l in sc) or 1
LBL = {"Anthropic", "OpenAI", "Google (Gemini)", "DeepSeek", "Xiaomi", "Moonshot (Kimi)", "Z.ai (Zhipu)", "xAI (Grok)", "MiniMax", "NVIDIA (Nemotron)"}
s = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Paid token share versus implied dollar share by lab" font-family="system-ui,-apple-system,Segoe UI,sans-serif">' % (W, H)]
for gv in (0.1, 1, 10, 100):
    x, y = sx(gv), sy(gv)
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (x, PAD_T, x, PAD_T + PH))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (PAD_L, y, PAD_L + PW, y))
    s.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="11" text-anchor="middle">%g%%</text>' % (x, PAD_T + PH + 16, gv))
    s.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="11" text-anchor="end">%g%%</text>' % (PAD_L - 6, y + 3, gv))
s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="5 4"/>' % (sx(LO), sy(LO), sx(HI), sy(HI)))
s.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="10.5" text-anchor="middle" transform="rotate(-30 %.1f %.1f)">$ = tokens</text>' % (sx(40), sy(60), sx(40), sy(60)))
s.append('<text x="%.1f" y="%.1f" fill="var(--ink2)" font-size="12" text-anchor="middle">Share of PAID tokens (log)</text>' % (PAD_L + PW / 2, H - 6))
s.append('<text transform="rotate(-90 14 %.1f)" x="14" y="%.1f" fill="var(--ink2)" font-size="12" text-anchor="middle">Share of implied $ (log)</text>' % (PAD_T + PH / 2, PAD_T + PH / 2))
s.append('<text x="%.1f" y="%.1f" fill="var(--good)" font-size="11" opacity=".9">premium ▲ ($ &gt; tokens)</text>' % (PAD_L + 8, PAD_T + 16))
s.append('<text x="%.1f" y="%.1f" fill="var(--crit)" font-size="11" text-anchor="end" opacity=".9">commodity ▼ (tokens &gt; $)</text>' % (PAD_L + PW - 6, PAD_T + PH - 8))
for l in sc:
    x, y = sx(l["paid_token_share"] * 100), sy(l["rev_share"] * 100)
    r = 5 + 20 * math.sqrt(l["revenue_annualized"] / maxrev)
    col = CAP_COLOR[l["capture"]]
    s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity=".5" stroke="%s" stroke-width="1.5"><title>%s\npaid tokens %s · $ %s · requests %s\n%s/yr (ceiling) · $%.2f/Mtok · %s:1 in:out</title></circle>' % (
        x, y, r, col, col, esc(l["display"]), pct(l["paid_token_share"]), pct(l["rev_share"]), pct(l["req_share"]),
        dol(l["revenue_annualized"]), l["blended_price_per_mtok"], ("%.0f" % l["input_ratio"]) if l["input_ratio"] else "n/a"))
    if l["display"] in LBL:
        dy = -r - 4 if y > PAD_T + 30 else r + 12
        s.append('<text x="%.1f" y="%.1f" fill="var(--ink)" font-size="11" font-weight="600" text-anchor="middle">%s</text>' % (x, y + dy, esc(l["display"].split(" (")[0])))
s.append('</svg>')
scatter_svg = "".join(s)

# ---------- $/yr BARS ----------
bl = labs[:12]
mx = max(l["revenue_annualized"] for l in bl) or 1
bars = []
for l in bl:
    mom = l["momentum"]
    chip = '<span class="mut">n/a</span>' if mom is None else '<span class="mom %s">%s %+.0f%%</span>' % ("up" if mom >= 0 else "dn", "▲" if mom >= 0 else "▼", mom * 100)
    bars.append(
        '<div class="barrow"><div class="barname" style="border-left:3px solid %s">%s <span class="cap">%s</span></div>'
        '<div class="bartrack"><div class="barfill" style="width:%.1f%%;background:%s"></div></div>'
        '<div class="barval">%s</div><div class="barmom">%s</div></div>' % (
            CAP_COLOR[l["capture"]], esc(l["display"]), esc(l["capture"].replace("-", " ")),
            l["revenue_annualized"] / mx * 100, CAP_COLOR[l["capture"]], dol(l["revenue_annualized"]), chip))
bars_html = "".join(bars)

# ---------- TREND (accumulates one point per weekly snapshot) ----------
# fixed colour per lab (entity-stable across rebuilds, independent of rank)
TREND_SLOT = {"anthropic": "--s1", "openai": "--s2", "google": "--s3", "deepseek": "--s4", "z-ai": "--s5",
              "moonshotai": "--s4", "x-ai": "--s5", "xiaomi": "--s3", "minimax": "--s2"}
top_trend = [l["author"] for l in labs[:5]]
TW, TH, TPL, TPB, TPT, TPR = 720, 300, 46, 34, 14, 120
TPW, TPH = TW - TPL - TPR, TH - TPT - TPB
trend_html = ""
if HIST:
    maxs = 0.0
    series = {}
    for a in top_trend:
        pts = []
        for i, rec in enumerate(HIST):
            v = rec.get("labs", {}).get(a)
            if v and rec.get("revenue_annualized"):
                s = v["rev_ann"] / rec["revenue_annualized"] * 100
                pts.append((i, s, rec["date"], v["rev_ann"]))
                maxs = max(maxs, s)
        if pts:
            series[a] = pts
    maxs = max(maxs * 1.15, 10)
    nx = max(len(HIST) - 1, 1)

    def tx(i):
        return TPL + (i / nx) * TPW if nx else TPL + TPW / 2

    def ty(s):
        return TPT + TPH - (s / maxs) * TPH

    tsvg = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Implied dollar share by lab over time" font-family="system-ui,-apple-system,Segoe UI,sans-serif">' % (TW, TH)]
    step = 10 if maxs <= 45 else 20
    g = 0
    while g <= maxs:
        y = ty(g)
        tsvg.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (TPL, y, TPL + TPW, y))
        tsvg.append('<text x="%d" y="%.1f" fill="var(--muted)" font-size="11" text-anchor="end">%d%%</text>' % (TPL - 6, y + 3, g))
        g += step
    for i, rec in enumerate(HIST):
        tsvg.append('<text x="%.1f" y="%d" fill="var(--muted)" font-size="10.5" text-anchor="middle">%s</text>' % (tx(i), TH - 8, esc(rec["date"][5:])))
    for a, pts in series.items():
        col = "var(%s)" % TREND_SLOT.get(a, "--s1")
        disp, _, _ = (by[a]["display"], 0, 0) if a in by else (a, 0, 0)
        if len(pts) > 1:
            path = " ".join("%s%.1f %.1f" % ("M" if k == 0 else "L", tx(p[0]), ty(p[1])) for k, p in enumerate(pts))
            tsvg.append('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (path, col))
        for p in pts:
            tsvg.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"><title>%s — %s\n%.1f%% of implied $ (%s/yr)</title></circle>' % (
                tx(p[0]), ty(p[1]), col, esc(disp), esc(p[2]), p[1], dol(p[3])))
        lp = pts[-1]
        tsvg.append('<text x="%.1f" y="%.1f" fill="%s" font-size="11" font-weight="600">%s %.0f%%</text>' % (
            tx(lp[0]) + 8, ty(lp[1]) + 4, col, esc(disp.split(" (")[0]), lp[1]))
    tsvg.append('</svg>')
    note = ('<p class="note">One point per weekly snapshot — the line builds as the Monday auto-refresh accumulates history (started %s).</p>'
            % esc(HIST[0]["date"])) if len(HIST) < 3 else ""
    trend_html = ('<h2>Share of implied $ over time</h2>'
                  '<p class="sub">Top-5 labs by implied spend, share of platform dollars per weekly snapshot — the "watch the migration" chart.</p>'
                  '<div class="card">' + "".join(tsvg) + note + '</div>')

# ---------- NEW MODELS THIS WEEK ----------
new_models = D.get("new_models") or []
newm_html = ""
if new_models:
    chips = "".join('<span class="chip"><b>%s</b> <span class="mut">%s · %s/wk</span></span>' % (
        esc(m["name"]), esc(m["lab"]), tok(m["tokens_week"])) for m in new_models)
    newm_html = ('<div class="callout" style="border-color:var(--s2)"><b>New on OpenRouter since %s:</b> %s</div>'
                 % (esc(new_models[0].get("since", "last snapshot")), chips))


# ---------- LAB TABLE ----------
def momcell(m):
    if m is None:
        return '<td class="r mut" data-v="-999">n/a</td>'
    return '<td class="r %s" data-v="%.4f">%+.0f%%</td>' % ("pos" if m >= 0 else "neg", m, m * 100)


def wowcell(author):
    w = WOW.get(author)
    if not w:
        return '<td class="r mut" data-v="-999">—</td>'
    d = w["d_rev_pp"]
    return '<td class="r %s" data-v="%.3f">%+.1f pp</td>' % ("pos" if d >= 0 else "neg", d, d)


rows = []
for l in labs:
    arr_b = l.get("arr_busd")
    arr_txt = ("$%.1fB" % arr_b) if arr_b else '<span class="mut">n/a</span>'
    orp = l.get("or_pct_of_arr")
    orp_txt = ("%.1f%%" % orp) if orp is not None else '<span class="mut">—</span>'
    ir = l["input_ratio"]
    rows.append(
        '<tr><td>%s</td><td><span class="capdot" style="background:%s"></span>%s</td>'
        '<td class="r" data-v="%.5f">%s</td><td class="r" data-v="%.5f">%s</td><td class="r" data-v="%.5f">%s</td>'
        '<td class="r" data-v="%.4f"><b>%s</b></td><td class="r" data-v="%.4f">$%.2f</td><td class="r" data-v="%.1f">%s</td>%s%s'
        '<td class="r" data-v="%s">%s</td><td class="r" data-v="%s">%s</td></tr>' % (
            esc(l["display"]), CAP_COLOR[l["capture"]], esc(CAP_LABEL.get(l["capture"], l["capture"])),
            l["paid_token_share"], pct(l["paid_token_share"]), l["req_share"], pct(l["req_share"]),
            l["rev_share"], pct(l["rev_share"]),
            l["revenue_annualized"], dol(l["revenue_annualized"]),
            l["blended_price_per_mtok"], l["blended_price_per_mtok"],
            (ir or 0), (("%.0f:1" % ir) if ir else "n/a"), momcell(l["momentum"]), wowcell(l["author"]),
            (arr_b or -1), arr_txt, (orp if orp is not None else -1), orp_txt))
lab_table = "".join(rows)

# ---------- ARR BRIDGE ----------
bridge = sorted([l for l in labs if l.get("arr_busd")], key=lambda l: -l["arr_busd"])
bmx = max(l["arr_busd"] for l in bridge) or 1
brows = []
for l in bridge:
    aw = l["arr_busd"] / bmx * 100
    orw = min(l["revenue_annualized"] / 1e9 / bmx * 100, aw)
    note = "" if l["capture"] == "first-party" else " *"
    brows.append(
        '<div class="barrow2"><div class="barname">%s%s</div>'
        '<div class="bartrack"><div class="barfill" style="width:%.2f%%;background:var(--arrbar)"></div>'
        '<div class="barfill" style="width:%.2f%%;background:var(--s1)" title="OpenRouter list-$ (ceiling)"></div></div>'
        '<div class="barval">$%.1fB <span class="mut">ARR · OR≈%s</span></div></div>' % (
            esc(l["display"]), note, aw, max(orw, 0.6), l["arr_busd"],
            ("%.1f%%" % l["or_pct_of_arr"]) if l.get("or_pct_of_arr") is not None else "—"))
bridge_html = "".join(brows)

# ---------- MODELS ----------
mrows = []
for m in models[:20]:
    ir = m.get("input_ratio")
    pin, pout = m.get("price_in_mtok", 0), m.get("price_out_mtok", 0)
    mrows.append('<tr><td>%s</td><td>%s</td><td class="r" data-v="%.1f">%s</td><td class="r" data-v="%.3f">$%.2f</td><td class="r" data-v="%.3f">$%.2f</td><td class="r" data-v="%.1f"><b>%s/yr</b></td><td class="r" data-v="%.4f">$%.2f</td><td class="r" data-v="%.1f">%s</td></tr>' % (
        esc(m["name"]), esc(m["lab"]), m["daily_tokens"], tok(m["daily_tokens"]),
        pin, pin, pout, pout,
        m["revenue_annualized"], dol(m["revenue_annualized"]), m["blended_price_per_mtok"], m["blended_price_per_mtok"],
        (ir or 0), (("%.0f:1" % ir) if ir else "n/a")))
models_table = "".join(mrows)

# ---------- CROSS-CLOUD PRICING ----------
CLOUDS = json.loads((OR / "cloud_prices.json").read_text(encoding="utf-8"))
CONF_BADGE = {
    "official": ('<span class="conf off">official</span>', ""),
    "observed": ('<span class="conf off">observed</span>', "seen live in OpenRouter's routing feed"),
    "list": ('<span class="conf lst">=list</span>', "resold at the model-maker's list price (mechanism)"),
    "native": ('<span class="conf off">native</span>', ""),
    "reported": ('<span class="conf rep">reported</span>', ""),
    "pending": ("", ""),
    "na": ("", ""),
}


def cloud_cell(cell, base_in, base_out):
    if not cell or cell.get("conf") == "na":
        return '<td class="r mut" data-v="-2">—</td>'
    if cell.get("conf") == "pending" or "in" not in cell:
        return '<td class="r mut" data-v="-1">offered · $?</td>'
    i, o = cell["in"], cell["out"]
    badge = CONF_BADGE.get(cell.get("conf", ""), ("", ""))[0]
    tip = (' title="%s"' % esc(cell["note"])) if cell.get("note") else ""
    # premium vs cheapest list route (input basis)
    prem = ""
    if base_in and abs(i - base_in) / base_in > 0.02:
        mult = i / base_in
        prem = ' <span class="%s">%.1fx</span>' % ("neg" if mult > 1 else "pos", mult)
    return '<td class="r" data-v="%.4f"%s>$%.2f / $%.2f %s%s</td>' % (i, tip, i, o, badge, prem)


crows = []
for cm in CLOUDS["models"]:
    li, lo = cm["list"]["in"], cm["list"]["out"]
    klass_pill = '<span class="pillk %s">%s</span>' % ("fp" if cm["klass"] == "first-party" else "ow", "1st-party" if cm["klass"] == "first-party" else "open-weight")
    crows.append('<tr><td>%s <span class="mut">· %s</span> %s</td>'
                 '<td class="r" data-v="%.4f"><b>$%.2f / $%.2f</b></td>%s%s%s</tr>' % (
                     esc(cm["name"]), esc(cm["lab"]), klass_pill,
                     li, li, lo,
                     cloud_cell(cm.get("bedrock"), li, lo),
                     cloud_cell(cm.get("vertex"), li, lo),
                     cloud_cell(cm.get("azure"), li, lo)))
cloud_table = "".join(crows)

mech_table = "".join(
    '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        esc(r["venue"]), esc(r["batch"]), esc(r["cache_read"]), esc(r["long_context"]), esc(r["regional"]))
    for r in CLOUDS.get("mechanics", {}).get("rows", []))

# ---------- NEOCLOUD MARKET (per-provider prices from the endpoints watchlist) ----------
NEO = D.get("neoclouds") or []
neo_open = [n for n in NEO if n["klass"] == "open"]
neo_fp = [n for n in NEO if n["klass"] == "first-party"]


def neo_cell(entry, maker):
    if not entry:
        return '<td class="r mut" data-v="-1">—</td>'
    mult = ""
    if maker and maker.get("in"):
        m = entry["in"] / maker["in"]
        if abs(m - 1) > 0.02:
            mult = ' <span class="%s">%.1fx</span>' % ("neg" if m > 1 else "pos", m)
        else:
            mult = ' <span class="mut">=maker</span>'
    return '<td class="r" data-v="%.4f" title="%s · ctx %s">$%.2f / $%.2f%s</td>' % (
        entry["in"], esc(entry.get("quant") or ""), entry.get("ctx"), entry["in"], entry["out"], mult)


neo_rows = []
for n in sorted(neo_open, key=lambda x: -(x["n_providers"])):
    maker = n.get("maker")
    maker_txt = ('<td class="r" data-v="%.4f"><b>$%.2f / $%.2f</b></td>' % (maker["in"], maker["in"], maker["out"])) if maker else '<td class="r mut" data-v="-1">—</td>'
    ch = n["cheapest"]
    ch_txt = '<td class="r" data-v="%.4f">%s <b>$%.2f / $%.2f</b>%s</td>' % (
        ch["in"], esc(ch["provider"]), ch["in"], ch["out"],
        (' <span class="pos">%.1fx</span>' % (ch["in"] / maker["in"]) if maker and maker.get("in") and ch["in"] / maker["in"] < 0.98 else ""))
    neo_rows.append('<tr><td>%s <span class="mut">· %s</span></td>%s%s%s%s%s%s<td class="r" data-v="%d">%d</td><td class="r" data-v="%.2f">%.1fx</td></tr>' % (
        esc(n["name"]), esc(n["lab"]), maker_txt, ch_txt,
        neo_cell(n.get("together"), maker), neo_cell(n.get("fireworks"), maker),
        neo_cell(n.get("deepinfra"), maker), neo_cell(n.get("google"), maker),
        n["n_providers"], n["n_providers"], n.get("spread_in") or 0, n.get("spread_in") or 0))
neo_table = "".join(neo_rows)

fp_proof = ""
if neo_fp:
    bits = []
    for n in neo_fp:
        venues = []
        for k, label in (("maker", n["lab"].split(" (")[0]), ("bedrock", "Bedrock"), ("google", "Vertex"), ("azure", "Azure")):
            e = n.get(k)
            if e:
                venues.append("%s $%.0f/$%.0f" % (label, e["in"], e["out"]))
        if len(venues) >= 2:
            bits.append("<b>%s</b>: %s" % (esc(n["name"]), esc(" = ".join(venues))))
    if bits:
        fp_proof = ('<div class="callout"><b>Observed, not inferred:</b> the routing feed shows the same first-party model at the SAME price on every venue — %s. '
                    'The lab sets one list price; clouds are distribution. (Second entries at +10%% are regional tiers.)</div>' % " · ".join(bits))

# ---------- APPS ----------
amx = max(a["tokens_week"] for a in apps) or 1
arows = []
for a in apps[:15]:
    if not a.get("title"):
        continue
    arows.append(
        '<div class="barrow2"><div class="barname apn">%s <span class="cap">%s</span></div>'
        '<div class="bartrack"><div class="barfill" style="width:%.1f%%;background:var(--s1)"></div></div>'
        '<div class="barval">%s/wk</div></div>' % (esc(a["title"]), esc(", ".join(a.get("categories", [])[:2])), a["tokens_week"] / amx * 100, tok(a["tokens_week"])))
apps_html = "".join(arows)

# ---------- TOTAL SYSTEM GROWTH ----------
sysg = D.get("system_growth", {})
ts = sysg.get("token_series", [])
spend_pts = sysg.get("spend_points", [])
mult_may = None
may = next((p["tokens_mo_T"] for p in ts if p["date"] == "2026-05"), None)
now_t = ts[-1]["tokens_mo_T"] if ts else plat["tokens_month_run_rate"] / 1e12
if may:
    mult_may = now_t / may
cost_pts = sysg.get("cost_series", [])
realized_pts = [{"date": p["date"], "cost_mo_musd": p["spend_mo_musd"]} for p in spend_pts]
blend_tok = sysg.get("blend_per_mtok", 0)
cost_now = (cost_pts[-1]["cost_mo_musd"] if cost_pts else 0)
gtiles = [
    ("Token run-rate", "%.0fT/mo" % now_t, "~%.1f quadrillion tokens/yr" % sysg.get("run_rate_quad_yr", 0)),
    ("Token growth", ("%.1f×" % mult_may) if mult_may else "n/a", "since May 2026"),
    ("7d vs 30d token momentum", token_mom_label, "all observed text models · not strict WoW"),
    ("Cost @ today's blend", "$%.0fM/mo" % cost_now, "$%.1fB/yr at $%.2f/Mtok blended" % (cost_now * 12 / 1e3, blend_tok)),
    ("Realized spend", "$%.0fM/mo" % (spend_pts[-1]["spend_mo_musd"] if spend_pts else 0), "reported (~$0.9B/yr) — ~flat since Mar"),
    ("Price / token", "collapsing", "vol ~%.1f×, $ ~flat ⇒ $/tok ↓" % (mult_may or 0)),
]
gtiles_html = "".join('<div class="tile"><div class="tlabel">%s</div><div class="tval">%s</div><div class="tsub">%s</div></div>' % (esc(a), esc(b), esc(c)) for a, b, c in gtiles)
tok_flags = {p["date"]: p["flag"] for p in sysg.get("token_points_meta", []) if p.get("flag")}
gsvg = linechart(ts, "tokens_mo_T", "var(--s1)", lambda v: ("%.0fT" % v) if v >= 10 else ("%.1fT" % v), log=True, flags=tok_flags)
csvg = linechart(cost_pts, "cost_mo_musd", "var(--s4)", lambda v: "$%.0fM" % v, pts2=realized_pts, color2="var(--good)")

# ---------- SHARE BY PRODUCT ----------
pm = D.get("product_mix", {})
io_in, io_out = pm.get("input_pct", 0), pm.get("output_pct", 0)
io_bar = ('<div style="display:flex;height:26px;border-radius:5px;overflow:hidden;font-size:11.5px;font-weight:700;color:#fff">'
          '<div style="width:%.1f%%;background:var(--s1);display:flex;align-items:center;justify-content:center">input %.0f%%</div>'
          '<div style="width:%.1f%%;background:var(--s4);display:flex;align-items:center;justify-content:center">out %.0f%%</div></div>' % (
              io_in * 100, io_in * 100, io_out * 100, io_out * 100))
wl = pm.get("workload", [])
wlmax = max((w["pct"] for w in wl), default=1) or 1
wl_html = "".join(
    '<div class="barrow2"><div class="barname">%s</div><div class="bartrack"><div class="barfill" style="width:%.1f%%;background:var(--s2)"></div></div><div class="barval">%s</div></div>' % (
        esc(w["name"]), w["pct"] / wlmax * 100, pct(w["pct"], 0)) for w in wl)
mod_txt = " · ".join("%s %s" % (esc(m["name"]), pct(m["pct"], 2 if m["pct"] < 0.01 else 1)) for m in pm.get("modality", []))

# assemble growth + product-mix + io-math (pre-formatted vars; no % in the BODY concat)
GROWTH = (
    '<h2 id="growth">System growth — total tokens &amp; cost</h2>'
    + ('<p class="sub">OpenRouter\'s whole pie over time. <b>Left:</b> total tokens/mo (one point per weekly snapshot; May-2026 is a reported anchor ~8M users; Mar ~8.4T excluded as off-basis). <b>Right:</b> total cost/mo = those tokens priced at today\'s model blend ($%.2f/Mtok); the dashed green line is OpenRouter\'s reported <i>realized</i> spend.</p>' % blend_tok)
    + '<div class="tiles growth-tiles">' + gtiles_html + '</div>'
    + '<div class="card"><div class="tlabel" style="margin-bottom:6px">Total token growth <span class="mut">(log scale · hollow dashed point = basis break, hover it)</span></div>' + gsvg + '</div>'
    + '<div class="card"><div class="tlabel" style="margin-bottom:6px">Total cost growth <span class="mut">(volume × today\'s blend)</span></div>' + csvg
    + '<div class="legend"><span><span class="dot" style="background:var(--s4)"></span>implied $ at today\'s blend</span><span><span class="dot" style="background:var(--good)"></span>reported realized spend</span></div></div>'
    + ('<p class="note"><b>The tell:</b> at today\'s blend the cost curve tracks volume (~%.1f× since May), but reported spend is ~flat ($83M Mar → $76M Jun) — so the <b>blended price per token is collapsing</b> as free tiers and cheap open models eat the marginal token. The "cost @ blend" line is a <i>ceiling</i> scenario (list price, no caching); realized sits ~⅓ of it.</p>' % (mult_may or 0)))

PRODUCT = (
    '<h2 id="product">What the system runs — share by product</h2>'
    '<p class="sub">Three cuts of the same token volume: by phase (input vs output), by workload, and by modality.</p>'
    '<div class="grid2"><div class="card"><div class="tlabel" style="margin-bottom:6px">By phase — input vs output tokens</div>' + io_bar
    + ('<p class="note" style="margin-top:8px">The system is <b>%.0f%% input tokens (%.1f:1)</b> — the fingerprint of coding/agentic traffic (huge context in, small answer out), and the single biggest driver of serving margin (see note below).</p></div>' % (io_in * 100, pm.get("ratio", 0)))
    + ('<div class="card"><div class="tlabel" style="margin-bottom:6px">By workload <span class="mut">(top-20 apps = %.0f%% of system tokens)</span></div>' % (pm.get("workload_coverage_pct", 0) * 100)) + wl_html
    + ('<p class="note" style="margin-top:8px">Modality: %s. Coding/agentic dominates the app-attributable volume; the rest is unlabeled long-tail.</p></div></div>' % mod_txt)
    + ('<div class="callout"><b>How the input/output math is decided.</b> The mix is <b>observed, not assumed</b>: every model row in OpenRouter\'s feed reports <code>total_prompt_tokens</code> and <code>total_completion_tokens</code>; the ratio is their quotient (platform %.1f:1; Anthropic 65:1, DeepSeek 20:1, Xiaomi 113:1). It drives margin through two asymmetries — <b>cost:</b> serving input (prefill: parallel, compute-bound) runs ~5× cheaper per token than output (decode: sequential, HBM-bandwidth-bound), per DeepSeek\'s own disclosure (73.7k vs 14.8k tok/s/node); <b>price:</b> providers list input at ~20-35%% of the output price. Input-heavy traffic therefore stacks cheap-to-serve tokens priced above cost → structurally fat blended margin. The serving-margin model blends at <b>each lab\'s own observed mix</b> — using a chat-like 3:1 where the traffic is really 20-65:1 understates margin by ~15-25 points.</div>' % pm.get("ratio", 0)))

GROWTH_PRODUCT = GROWTH + PRODUCT

# ---------- GUARDRAILS ----------
gmap = {"PASS": "good", "WARN": "warn", "INFO": "info", "FAIL": "crit"}
guard_html = "".join('<tr><td><span class="gstat %s">%s</span></td><td>%s</td><td>%s</td></tr>' % (
    gmap.get(st, "info"), st, esc(k.replace("_", " ")), esc(msg)) for k, (st, msg) in guards.items())

asof, gen = D["asof"], D["generated"]

CSS = r"""
:root{color-scheme:light;--plane:#f9f9f7;--surf:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
--grid:#e1e0d9;--base:#c3c2b7;--border:rgba(11,11,11,.10);--s1:#2a78d6;--s2:#008300;--s3:#e87ba4;--s4:#eda100;--s5:#1baf7a;
--good:#0ca30c;--crit:#d03b3b;--warn:#c98500;--arrbar:#b7d3f6;--headbg:#0f1729;--headsub:#8492ad;--link:#7fb0ff;}
@media(prefers-color-scheme:dark){:root:where(:not([data-theme=light])){color-scheme:dark;--plane:#0d0d0d;--surf:#1a1a19;
--ink:#fff;--ink2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--base:#383835;--border:rgba(255,255,255,.10);
--s1:#3987e5;--s2:#008300;--s3:#d55181;--s4:#c98500;--s5:#199e70;--good:#0ca30c;--crit:#d03b3b;--warn:#eda100;--arrbar:#184f95;--headbg:#000;--headsub:#8492ad;--link:#7fb0ff;}}
:root[data-theme=dark]{color-scheme:dark;--plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;
--grid:#2c2c2a;--base:#383835;--border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#008300;--s3:#d55181;--s4:#c98500;--s5:#199e70;
--good:#0ca30c;--crit:#d03b3b;--warn:#eda100;--arrbar:#184f95;--headbg:#000;--headsub:#8492ad;--link:#7fb0ff;}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{background:var(--headbg);color:#fff;padding:20px 28px}
header h1{margin:0;font-size:21px} header p{margin:5px 0 0;color:var(--headsub);font-size:13px} header a{color:var(--link);text-decoration:none}
nav.tabs{position:sticky;top:0;z-index:30;background:var(--headbg);display:flex;gap:2px;flex-wrap:wrap;padding:8px 20px;border-bottom:1px solid rgba(255,255,255,.08)}
nav.tabs a{color:var(--headsub);font-size:12px;font-weight:600;padding:6px 10px;border-radius:7px;text-decoration:none;white-space:nowrap}
nav.tabs a:hover{color:#fff;background:rgba(255,255,255,.10)}
h2{scroll-margin-top:52px}
main{max-width:1080px;margin:0 auto;padding:22px 26px 90px}
h2{font-size:17px;margin:34px 0 4px;border-bottom:1px solid var(--grid);padding-bottom:6px}
.sub{color:var(--ink2);font-size:13px;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(184px,1fr));gap:12px;margin:18px 0 6px}
.tile{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.tlabel{color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em}
.tval{font-size:24px;font-weight:700;margin:3px 0 2px;line-height:1.15}
.tsub{color:var(--ink2);font-size:12px}
.card{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:12px 0}
.callout{border-left:4px solid var(--s1);background:var(--surf);padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0;font-size:14px}
.callout.warn{border-color:var(--warn)} .callout b{color:var(--ink)}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2);margin:8px 0 2px}
.legend span{display:inline-flex;align-items:center;gap:6px}.dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.barrow{display:grid;grid-template-columns:206px 1fr 92px 82px;align-items:center;gap:10px;margin:5px 0;font-size:13px}
.barrow2{display:grid;grid-template-columns:220px 1fr 150px;align-items:center;gap:10px;margin:5px 0;font-size:13px}
.barname{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:7px}
.barname .cap,.apn .cap{color:var(--muted);font-size:11px;display:block;line-height:1.1}
.bartrack{background:var(--grid);border-radius:4px;height:16px;display:flex;gap:2px}
.barfill{height:16px;border-radius:4px;min-width:2px}
.barval{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.barmom{text-align:right;font-size:12px;color:var(--ink2);font-variant-numeric:tabular-nums}
.mom{font-weight:600}.mom.up{color:var(--good)}.mom.dn{color:var(--crit)}
.tag{background:var(--grid);color:var(--ink2);font-size:10.5px;padding:0 5px;border-radius:8px;font-weight:600}
.chip{display:inline-block;background:var(--grid);border-radius:9px;padding:2px 9px;margin:2px 4px 2px 0;font-size:12.5px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12.6px}
th,td{border-bottom:1px solid var(--grid);padding:6px 9px;text-align:left}
th{color:var(--ink2);font-weight:700;cursor:pointer;white-space:nowrap;user-select:none}
th.r,td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:hover td{background:rgba(127,127,127,.06)}
.pos{color:var(--good)}.neg{color:var(--crit)}.mut{color:var(--muted)}
.capdot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:6px}
.scroll{overflow-x:auto}
.gstat{font-weight:700;font-size:11px;padding:1px 7px;border-radius:9px}
.gstat.good{background:rgba(12,163,12,.15);color:var(--good)}.gstat.warn{background:rgba(201,133,0,.16);color:var(--warn)}
.gstat.info{background:rgba(127,127,127,.14);color:var(--ink2)}.gstat.crit{background:rgba(208,59,59,.15);color:var(--crit)}
.note{color:var(--ink2);font-size:12.5px}.note code{background:var(--grid);padding:1px 5px;border-radius:4px}
.conf{font-size:9.5px;font-weight:700;padding:0 4px;border-radius:6px;vertical-align:1px}
.conf.off{background:rgba(12,163,12,.15);color:var(--good)}.conf.lst{background:rgba(42,120,214,.14);color:var(--s1)}
.conf.rep{background:rgba(201,133,0,.16);color:var(--warn)}
.pillk{font-size:10px;font-weight:700;padding:0 6px;border-radius:8px}
.pillk.fp{background:rgba(42,120,214,.14);color:var(--s1)}.pillk.ow{background:rgba(0,131,0,.13);color:var(--s2)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:820px){.grid2{grid-template-columns:1fr}.barrow{grid-template-columns:140px 1fr 74px}.barmom{display:none}.barrow2{grid-template-columns:150px 1fr 120px}}

/* Research cockpit refresh */
:root{--plane:#f3f5f8;--surf:#fff;--surf2:#f8fafc;--ink:#101828;--ink2:#475467;--muted:#667085;
--grid:#e4e7ec;--base:#d0d5dd;--border:rgba(16,24,40,.10);--s1:#6157e5;--s2:#039855;--s3:#e14d72;
--s4:#dc6803;--s5:#079455;--good:#039855;--crit:#d92d20;--warn:#dc6803;--headbg:#0b1220;
--headsub:#a7b2c5;--link:#c7d7fe;--shadow:0 1px 2px rgba(16,24,40,.04),0 8px 24px rgba(16,24,40,.05)}
@media(prefers-color-scheme:dark){:root:where(:not([data-theme=light])){--plane:#080d17;--surf:#111827;--surf2:#0d1524;
--ink:#f5f7fa;--ink2:#cbd5e1;--muted:#94a3b8;--grid:#263244;--base:#344054;--border:rgba(255,255,255,.10);
--s1:#8b83ff;--s2:#32d583;--s3:#f970a0;--s4:#fdb022;--s5:#32d583;--good:#32d583;--crit:#f97066;
--warn:#fdb022;--headbg:#050914;--headsub:#94a3b8;--link:#c7d7fe;--shadow:0 12px 32px rgba(0,0,0,.18)}}
:root[data-theme=dark]{--plane:#080d17;--surf:#111827;--surf2:#0d1524;--ink:#f5f7fa;--ink2:#cbd5e1;
--muted:#94a3b8;--grid:#263244;--base:#344054;--border:rgba(255,255,255,.10);--s1:#8b83ff;--s2:#32d583;
--s3:#f970a0;--s4:#fdb022;--s5:#32d583;--good:#32d583;--crit:#f97066;--warn:#fdb022;--headbg:#050914;
--headsub:#94a3b8;--link:#c7d7fe;--shadow:0 12px 32px rgba(0,0,0,.18)}
html{scroll-behavior:smooth}
body{font:14px/1.55 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
.skip{position:fixed;left:16px;top:-60px;z-index:100;background:var(--surf);color:var(--ink);padding:9px 13px;
border-radius:8px;box-shadow:var(--shadow);text-decoration:none}.skip:focus{top:12px}
.progress{position:fixed;left:0;top:0;z-index:90;width:100%;height:3px;background:transparent}
.progress>span{display:block;width:0;height:100%;background:linear-gradient(90deg,var(--s1),var(--s3));transition:width .1s linear}
header.hero{position:relative;overflow:hidden;background:radial-gradient(circle at 78% 15%,rgba(97,87,229,.28),transparent 30%),
radial-gradient(circle at 95% 100%,rgba(7,148,85,.17),transparent 32%),var(--headbg);padding:34px 30px 38px}
header.hero:after{content:"";position:absolute;inset:auto -8% -110px 48%;height:170px;border:1px solid rgba(255,255,255,.08);
border-radius:50%;transform:rotate(-8deg);pointer-events:none}
.hero-inner{max-width:1440px;margin:auto;position:relative;z-index:1}.eyebrow{display:flex;align-items:center;gap:8px;color:#cbd5e1;
font-size:11px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;margin-bottom:12px}.status-dot{width:7px;height:7px;
background:#32d583;border-radius:50%;box-shadow:0 0 0 5px rgba(50,213,131,.12)}
.hero-grid{display:flex;align-items:end;justify-content:space-between;gap:32px}.hero h1{font-size:clamp(30px,4vw,50px);
letter-spacing:-.045em;line-height:1.02;max-width:800px}.hero h1 span{color:#b9b4ff}.hero p{max-width:760px;
font-size:15px;line-height:1.6;margin-top:12px;color:#aab6ca}.hero-actions{display:flex;gap:9px;flex-shrink:0}
.action{display:inline-flex;align-items:center;justify-content:center;height:38px;padding:0 13px;border:1px solid rgba(255,255,255,.15);
border-radius:9px;background:rgba(255,255,255,.07);color:#fff!important;font:600 12px/1 inherit;cursor:pointer;text-decoration:none}
.action:hover{background:rgba(255,255,255,.13)}
.page-shell{max-width:1480px;margin:0 auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:34px;padding:0 30px}
.rail{position:sticky;top:18px;align-self:start;padding:26px 0;max-height:calc(100vh - 36px);overflow:auto}.rail-label{color:var(--muted);
font-size:10px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;padding:0 10px 8px}
nav.tabs{position:static;display:flex;flex-direction:column;gap:2px;background:transparent;border:0;padding:0;flex-wrap:nowrap}
nav.tabs a{position:relative;color:var(--ink2);font-size:12px;padding:8px 10px;border-radius:8px;font-weight:600}
nav.tabs a:hover{background:var(--surf);color:var(--ink)}nav.tabs a.active{background:var(--surf);color:var(--ink);box-shadow:var(--shadow)}
nav.tabs a.active:before{content:"";position:absolute;left:0;top:8px;bottom:8px;width:3px;border-radius:2px;background:var(--s1)}
.rail-note{margin:18px 10px 0;padding-top:14px;border-top:1px solid var(--grid);color:var(--muted);font-size:10.5px;line-height:1.55}
main{max-width:none;min-width:0;margin:0;padding:28px 0 100px}.overview{background:var(--surf);border:1px solid var(--border);border-radius:18px;
padding:22px 22px 20px;box-shadow:var(--shadow)}.section-kicker{font-size:10px;color:var(--s1);font-weight:800;letter-spacing:.13em;text-transform:uppercase}
.overview-title{font-size:22px;margin:3px 0 0;letter-spacing:-.02em}.overview-title:before{display:none}.overview>.tiles,.growth-tiles{grid-template-columns:repeat(3,minmax(0,1fr))}.callout{border-left-width:3px;border-radius:0 10px 10px 0}
.overview .callout{margin:15px 0}.tiles{grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.tile{position:relative;background:var(--surf2);
border-radius:12px;padding:14px;overflow:hidden}.tile:before{content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--s1);opacity:.55}
.tval{font-size:22px;letter-spacing:-.025em}.insight-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:14px}
.insight{position:relative;border:1px solid var(--border);background:var(--surf2);border-radius:12px;padding:15px;overflow:hidden}
.insight:after{content:"";position:absolute;right:-22px;top:-24px;width:74px;height:74px;border-radius:50%;background:var(--s1);opacity:.08}
.insight.accent-pink:after{background:var(--s3)}.insight.accent-amber:after{background:var(--s4)}.insight-kicker{font-size:10px;
font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}.insight-value{font-size:18px;font-weight:750;letter-spacing:-.02em;margin-top:5px}
.insight p{color:var(--ink2);font-size:12px;margin:3px 0 12px}.insight-source{color:var(--muted);font-size:9.5px}
h2{font-size:24px;letter-spacing:-.025em;margin:44px 0 5px;border:0;padding:0;scroll-margin-top:28px}
h2:before{content:"";display:block;width:32px;height:3px;background:var(--s1);border-radius:4px;margin-bottom:10px}.sub{font-size:13px;max-width:880px}
.card{border-radius:14px;padding:18px 20px;box-shadow:var(--shadow)}.grid2{gap:16px}.legend{gap:10px}
.bartrack{height:10px;border-radius:999px}.barfill{height:10px;border-radius:999px}
.table-tools{position:sticky;left:0;display:flex;align-items:end;justify-content:space-between;gap:12px;margin:0 0 10px}
.table-search{min-width:260px;height:36px;border:1px solid var(--grid);border-radius:9px;background:var(--surf2);color:var(--ink);
padding:0 11px;font:inherit;outline:none}.table-search:focus{border-color:var(--s1);box-shadow:0 0 0 3px rgba(97,87,229,.12)}
.row-count{color:var(--muted);font-size:11px}table{font-size:12px}th{position:relative;background:var(--surf);padding-top:9px;padding-bottom:9px}
th[role=button]:after{content:"  \2195";opacity:.35}th[aria-sort=ascending]:after{content:"  \2191";opacity:1;color:var(--s1)}
th[aria-sort=descending]:after{content:"  \2193";opacity:1;color:var(--s1)}th:focus-visible{outline:2px solid var(--s1);outline-offset:-2px}
td{padding-top:8px;padding-bottom:8px}tbody tr:nth-child(even) td{background:rgba(127,127,127,.025)}
.scroll{scrollbar-width:thin;scrollbar-color:var(--base) transparent}.scroll table th:first-child,.scroll table td:first-child{position:sticky;left:0;
z-index:2;background:var(--surf);box-shadow:1px 0 0 var(--grid)}.scroll table th:first-child{z-index:3}
.back-top{position:fixed;right:22px;bottom:22px;z-index:50;width:40px;height:40px;border:1px solid var(--border);border-radius:12px;
background:var(--surf);color:var(--ink);box-shadow:var(--shadow);cursor:pointer;opacity:0;transform:translateY(8px);pointer-events:none;transition:.2s}
.back-top.show{opacity:1;transform:none;pointer-events:auto}a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--s1);outline-offset:3px}
@media(max-width:1100px){.tiles{grid-template-columns:repeat(3,minmax(0,1fr))}.page-shell{grid-template-columns:190px minmax(0,1fr);gap:22px}}
@media(max-width:820px){header.hero{padding:26px 18px 28px}.hero-grid{display:block}.hero-actions{margin-top:20px}.page-shell{display:block;padding:0 14px}
.rail{position:sticky;top:0;z-index:40;max-height:none;margin:0 -14px;padding:7px 14px;background:var(--plane);border-bottom:1px solid var(--grid);overflow-x:auto}
.rail-label,.rail-note{display:none}nav.tabs{flex-direction:row;width:max-content}nav.tabs a{padding:7px 10px}
nav.tabs a.active:before{left:9px;right:9px;top:auto;bottom:2px;width:auto;height:2px}.overview{border-radius:14px;padding:17px}
.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}.insight-grid{grid-template-columns:1fr}h2{font-size:21px;scroll-margin-top:60px}
.barrow2{grid-template-columns:minmax(120px,1fr) 1fr 90px}.table-tools{align-items:stretch;flex-direction:column}.table-search{min-width:0;width:100%}}
@media(max-width:520px){.hero h1{font-size:32px}.tiles{grid-template-columns:1fr 1fr}.tval{font-size:19px}.tile{padding:12px}
.barrow{grid-template-columns:110px 1fr 64px}.barrow2{grid-template-columns:110px 1fr 78px}.barname{padding-left:0}.card{padding:15px}
.grid2{gap:0}.hero-actions{width:100%}.action{flex:1}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.progress>span,.back-top{transition:none}}
"""

JS = r"""
function sortT(t,c,num){var tb=t.tBodies[0],rs=[].slice.call(tb.rows);
var asc=t.getAttribute('data-c')==c?!(t.getAttribute('data-a')=='1'):true;t.setAttribute('data-c',c);t.setAttribute('data-a',asc?'1':'0');
rs.sort(function(a,b){var x=a.cells[c],y=b.cells[c];var av=num?parseFloat(x.getAttribute('data-v')||x.textContent):x.textContent.trim().toLowerCase();
var bv=num?parseFloat(y.getAttribute('data-v')||y.textContent):y.textContent.trim().toLowerCase();
if(num){av=isNaN(av)?-1e18:av;bv=isNaN(bv)?-1e18:bv;}return asc?(av>bv?1:av<bv?-1:0):(av<bv?1:av>bv?-1:0);});rs.forEach(function(r){tb.appendChild(r);});}
document.querySelectorAll('table.sortable').forEach(function(t){[].forEach.call(t.tHead.rows[0].cells,function(th,i){th.onclick=function(){sortT(t,i,th.classList.contains('r'));};});});

(function(){
  var root=document.documentElement,themeBtn=document.getElementById('themeToggle');
  function applyTheme(t){root.setAttribute('data-theme',t);if(themeBtn){themeBtn.textContent=t==='dark'?'Light mode':'Dark mode';themeBtn.setAttribute('aria-pressed',t==='dark'?'true':'false');}}
  var saved='';try{saved=localStorage.getItem('or-theme')||'';}catch(e){}
  if(saved){applyTheme(saved);}else{applyTheme(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');}
  if(themeBtn){themeBtn.addEventListener('click',function(){var next=root.getAttribute('data-theme')==='dark'?'light':'dark';applyTheme(next);try{localStorage.setItem('or-theme',next);}catch(e){}});}
  var progress=document.querySelector('.progress span'),topBtn=document.querySelector('.back-top');
  function onScroll(){var max=document.documentElement.scrollHeight-innerHeight;var p=max>0?scrollY/max*100:0;if(progress)progress.style.width=p+'%';if(topBtn)topBtn.classList.toggle('show',scrollY>700);}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(topBtn){topBtn.addEventListener('click',function(){scrollTo({top:0,behavior:'smooth'});});}
  document.querySelectorAll('.table-search').forEach(function(input){
    var table=document.getElementById(input.getAttribute('data-table')),counter=document.querySelector('[data-for="'+input.getAttribute('data-table')+'"]');
    if(!table)return;var rows=[].slice.call(table.tBodies[0].rows);
    function filter(){var q=input.value.trim().toLowerCase(),shown=0;rows.forEach(function(row){var yes=!q||row.textContent.toLowerCase().indexOf(q)>-1;row.hidden=!yes;if(yes)shown++;});if(counter)counter.textContent=shown+' of '+rows.length+' rows';}
    input.addEventListener('input',filter);filter();
  });
  document.querySelectorAll('table.sortable th').forEach(function(th){
    th.setAttribute('role','button');th.setAttribute('tabindex','0');th.setAttribute('aria-sort','none');
    th.addEventListener('click',function(){var table=th.closest('table');table.querySelectorAll('th').forEach(function(x){x.setAttribute('aria-sort','none');});
      th.setAttribute('aria-sort',table.getAttribute('data-a')==='1'?'ascending':'descending');});
    th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();th.click();}});
  });
  var links=[].slice.call(document.querySelectorAll('nav.tabs a[href^="#"]'));
  var targets=links.map(function(a){return document.querySelector(a.getAttribute('href'));}).filter(Boolean);
  if('IntersectionObserver' in window){var observer=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){links.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+entry.target.id);});}});},{rootMargin:'-15% 0px -74% 0px',threshold:0});targets.forEach(function(t){observer.observe(t);});}
})();
"""

def scinsight():
    def s(l, k):
        return pct(l[k], 0) if l else "?"
    return (
        "<b>Anthropic</b> earns ~%s of implied dollars on ~%s of paid tokens and only <b>%s of requests</b> — few, huge, expensive Claude-Code calls (%s:1 input). "
        "<b>Google/Gemini</b> is the mirror image: <b>%s of requests</b> but ~%s of $ (many cheap Flash calls). "
        "<b>DeepSeek</b> and <b>Xiaomi</b> are ~%s / ~%s of paid tokens but ~%s / ~%s of $ — commodity volume."
    ) % (
        s(ant, "rev_share"), s(ant, "paid_token_share"), s(ant, "req_share"),
        ("%.0f" % ant["input_ratio"]) if ant and ant["input_ratio"] else "?",
        s(ggl, "req_share"), s(ggl, "rev_share"),
        s(dsk, "paid_token_share"), s(xmi, "paid_token_share"), s(dsk, "rev_share"), s(xmi, "rev_share"))


BODY = (
    '<header><h1>AI-Lab Traction Monitor <span style="font-weight:400;color:var(--headsub)">· built on OpenRouter public data</span></h1>'
    '<p>Developer/API demand → implied inference spend by lab · as of <b>' + asof + '</b> · trailing 7-day window · <a href="../index.html">← wiki</a></p></header>'
    '<nav class="tabs"><a href="#growth">System growth</a><a href="#value">Tokens ≠ $</a><a href="#labs">Lab leaderboard</a><a href="#cloud">Cross-cloud pricing</a><a href="#neo">Neocloud market</a><a href="#method">Method</a></nav><main>'
    '<div class="callout warn"><b>Read this first.</b> This reconstructs an "AI-lab ARR" view from OpenRouter\'s public usage feed. It captures <b>developer/API traction routed through OpenRouter</b> — a real, high-frequency leading indicator, but a <i>slice</i> that excludes first-party enterprise API and consumer subscriptions (ChatGPT/Claude/Gemini), the bulk of frontier-lab ARR. '
    'Dollars are <b>tokens × list price with caching OFF</b>, so they are a <b>ceiling ≈ 3× realized</b> spend. <b>Lead with relative rank and share, not the absolute $.</b></div>'
    '<div class="tiles">' + tiles_html + '</div>'
    + GROWTH_PRODUCT +
    '<h2>Is the $ real? — the ceiling vs reality</h2>'
    '<p class="sub">Implied spend priced at list with no cache credit, then with 50%/70% of input re-priced at each model\'s cache-read rate, vs OpenRouter\'s reported <i>actual</i> monthly spend. The ceiling reconciles toward reality once caching &amp; provider discounts are applied.</p>'
    '<div class="card">' + ladder_html + '<p class="note" style="margin-top:10px">OpenRouter spend was ~<b>flat</b> Mar→Jun 2026 (~$83M→$76M/mo) even as tokens ~2.7×\'d — the marginal token is cheap/free — so the gap is <b>list-vs-realized</b>, not platform growth. '
    '<span class="mut">(Mar ~$83M is <b>derived</b>: Sacra\'s ~$50M annualized OR-revenue ÷ ~5% take ÷ 12 — estimate-on-estimate; Jun $76M is a reported snapshot.)</span></p></div>'
    '<h2 id="value">Tokens ≠ dollars</h2>'
    '<p class="sub">Each lab by share of <b>paid</b> tokens (volume) vs share of implied dollars (value). Above the line = premium pricing; below = commodity volume. Bubble size = implied $/yr.</p>'
    '<div class="card">' + scatter_svg +
    '<div class="legend"><span><span class="dot" style="background:var(--s1)"></span>First-party API (OR $ ≈ lab)</span>'
    '<span><span class="dot" style="background:var(--s2)"></span>Open-weight + own API</span>'
    '<span><span class="dot" style="background:var(--s3)"></span>Open-weight (hosted — $ to 3rd-party, not lab)</span></div></div>'
    '<div class="callout">' + scinsight() + '</div>'
    '<h2>Implied annualized spend by lab <span class="mut" style="font-size:13px;font-weight:400">(ceiling — rank &gt; magnitude)</span></h2>'
    '<p class="sub">Tokens × list price, annualized from the trailing-7-day run-rate. Momentum = 7-day daily rate vs 30-day daily rate.</p>'
    '<div class="card">' + bars_html + '</div>'
    + trend_html +
    '<h2 id="labs">Lab leaderboard</h2><div class="card scroll"><table class="sortable"><thead><tr>'
    '<th>Lab</th><th>Capture</th><th class="r">Paid tok %</th><th class="r">Req %</th><th class="r">$ share</th><th class="r">Implied $/yr</th>'
    '<th class="r">$/Mtok</th><th class="r">in:out</th><th class="r">Momentum</th><th class="r">Δ$shr WoW</th><th class="r">Reported ARR</th><th class="r">OR % of ARR</th></tr></thead>'
    '<tbody>' + lab_table + '</tbody></table>'
    '<p class="note">Sortable. <b>Capture</b> = how OpenRouter dollars map to the lab. <b>First-party</b>: OR routes to the lab\'s own API, so implied $ ≈ a thin slice of the lab\'s revenue. '
    '<b>Open-weight (hosted)</b>: served by third-party inference providers — dollars accrue to the host, not the model\'s author, so "OR % of ARR" is not meaningful there.</p></div>'
    '<div class="grid2">'
    '<div><h2>Reported ARR bridge</h2><p class="sub">How thin the OpenRouter slice is vs each lab\'s <i>total</i> reported run-rate (blue tick = OR list-$ ceiling). <span class="mut">* open-weight: OR $ is host revenue, not the lab\'s.</span></p><div class="card">' + bridge_html + '</div></div>'
    '<div><h2>Top apps driving demand</h2><p class="sub">Trailing-7-day tokens by consuming app — coding agents dominate.</p><div class="card">' + apps_html + '</div></div>'
    '</div>'
    + newm_html +
    '<h2>Top models by implied spend</h2><div class="card scroll"><table class="sortable"><thead><tr>'
    '<th>Model</th><th>Lab</th><th class="r">Tokens/day</th><th class="r">$/Mtok in</th><th class="r">$/Mtok out</th><th class="r">Implied $/yr</th><th class="r">$/Mtok blended</th><th class="r">in:out</th></tr></thead>'
    '<tbody>' + models_table + '</tbody></table></div>'
    '<h2 id="cloud">Cross-cloud token pricing <span class="mut" style="font-size:13px;font-weight:400">(USD per 1M tokens, input / output, on-demand)</span></h2>'
    '<p class="sub">The same model priced across venues: first-party list (= OpenRouter route) vs AWS Bedrock vs Google Vertex vs Azure. As of ' + esc(CLOUDS.get("asof", "")) + '.</p>'
    '<div class="card scroll"><table class="sortable"><thead><tr><th>Model</th><th class="r">List / OpenRouter</th><th class="r">AWS Bedrock</th><th class="r">GCP Vertex</th><th class="r">Azure</th></tr></thead>'
    '<tbody>' + cloud_table + '</tbody></table>'
    '<div class="callout" style="margin-top:12px"><b>The pricing-power read.</b> Frontier <b>first-party</b> pricing is venue-independent — <b>observed</b>, not just asserted: the routing feed shows Claude Opus 4.8 at $5/$25 and Sonnet 5 at $2/$10 identically on Anthropic, Bedrock, Vertex and Azure (regional tiers +10%), and Sonnet 5\'s $2/$10 promo is printed on AWS\'s own page. '
    '(AWS\'s page also shows a $6/$30 Claude line — those rows are labeled <i>"Claude 3.5 Sonnet (extended access)"</i>, a legacy-model keep-alive fee; the page is JS-rendered and machine-reads badly, so treat any scrape of it with care.) '
    'Where hyperscalers DO mark up is <b>open-weight</b> hosting: DeepSeek V3.2 costs ~2.3× more per input token on Bedrock ($0.62) than its cheapest route ($0.27), Qwen3-Next ~1.5×; Mistral Large 3 is the exception at exactly list. '
    'So the cloud premium sits on open models (managed-hosting convenience), while frontier-lab pricing is venue-independent — <b>the lab, not the cloud, owns the token P&amp;L.</b></div>'
    '<h3 style="font-size:14.5px;margin:20px 0 4px">Beyond the sticker: discount &amp; surcharge mechanics <span class="mut" style="font-weight:400">(official pages, 2026-07-21)</span></h3>'
    '<p class="sub" style="margin-bottom:8px">Among the <b>first-party frontier labs</b> (Anthropic / OpenAI / Google), cache-read ≈ <b>10% of input</b> and batch ≈ <b>50% off</b> — commoditized. Open-weight makers run wider: DeepSeek prices cache-read at <b>20–52%</b> of input depending on model, xAI ~15%. The real differentiation is <b>long-context surcharges</b> (Gemini Pro doubles input above 200K ctx — the lever that monetizes big-context agents) and regional premia.</p>'
    '<div class="scroll"><table><thead><tr><th>Venue</th><th>Batch</th><th>Cache-read</th><th>Long-context</th><th>Regional / other</th></tr></thead>'
    '<tbody>' + mech_table + '</tbody></table></div>'
    '<p class="note">Cell flags: <span class="conf off">official</span> read from that venue\'s page · <span class="conf off">observed</span> seen in OpenRouter\'s live routing feed · <span class="conf lst">=list</span> venue resells at the model-maker\'s list (documented mechanism) · <span class="conf rep">reported</span> page-scraped, not hand-verified · "offered · $?" = on the venue, price not yet captured; hover a cell for cache/batch/long-context detail. Hand-edit <code>_data/openrouter/cloud_prices.json</code>.</p></div>'
    '<h2 id="neo">Same model, many sellers — the neocloud market</h2>'
    '<p class="sub">Per-provider prices from OpenRouter\'s endpoints feed (observed, auto-refreshed weekly): the model-maker\'s own API vs Together, Fireworks, DeepInfra and the cheapest route. Multiples are vs the maker\'s own price; hover for quantization &amp; context.</p>'
    + fp_proof +
    '<div class="card scroll"><table class="sortable"><thead><tr><th>Model</th><th class="r">Maker\'s own API</th><th class="r">Cheapest route</th>'
    '<th class="r">Together</th><th class="r">Fireworks</th><th class="r">DeepInfra</th><th class="r">Google (Model Garden)</th><th class="r"># sellers</th><th class="r">Spread (in)</th></tr></thead>'
    '<tbody>' + neo_table + '</tbody></table>'
    '<div class="callout" style="margin-top:12px"><b>Who subsidizes whom.</b> The neocloud-vs-maker relationship flips by lab: <b>DeepSeek\'s own API is the FLOOR</b> — Together/Fireworks charge up to ~4× DeepSeek\'s price for V4 Pro (its $0.44/$0.87 looks subsidized; no third party can serve it at that price). '
    '<b>Z.ai and Moonshot are the opposite</b> — neoclouds undercut the maker\'s API by ~40% (GLM-5.2: StreamLake $0.82 vs Z.AI $1.40). <b>Together prices AT maker list</b> (GLM $1.40/$4.40, MiniMax $0.30/$1.20 — matches its own pricing page) — it competes on reliability/quality, not price. '
    'And <b>Google shows up as a neocloud</b> (Model Garden) serving DeepSeek/Qwen/Llama at mid-pack prices. Wide spreads partly reflect quantization (fp4 vs fp8 vs int4) and context-length differences — hover the cells.</div></div>'
    '<h2 id="method">Methodology, guardrails &amp; scope</h2>'
    '<div class="card"><table><thead><tr><th>Check</th><th>Metric</th><th>Result</th></tr></thead><tbody>' + guard_html + '</tbody></table>'
    '<p class="note" style="margin-top:12px"><b>What OpenRouter\'s public feed does NOT expose:</b> tool-call counts, reasoning/cached tokens, and image/audio volume are all returned as 0; per-task ("Programming", "Roleplay") and "fastest-models" breakdowns are auth-gated. So those panels from openrouter.ai/rankings can\'t be reproduced from public data — omitted rather than faked.</p>'
    '<p class="note"><b>Method.</b> Implied $ = Σ (prompt×list-prompt + completion×list-completion) per model, caching off (the feed reports 0 cached), annualized from the trailing-7-day window; grouped by model author. Token counts &amp; prices are OpenRouter\'s own public JSON. Anchors: Menlo Ventures ("&gt;1 quadrillion tokens/yr"), Sacra (~$50M OR revenue @ ~5% take ⇒ ~$1B/yr spend), Jun-26 ~$76M/mo actual. ' + esc(orr.get("source", "")) + '</p>'
    '<p class="note"><b>Refresh.</b> Auto: Windows task <b>"OpenRouter Weekly Refresh" — Mondays 08:05</b> runs <code>refresh_openrouter.bat</code> (fetch → build → dashboard → git commit+push; log <code>E:\\.claude\\scripts\\refresh_openrouter.log</code>). Manual: <code>py _wiki/_tools/or_fetch.py</code> → <code>or_build.py</code> → <code>build_openrouter_dash.py</code>. The token API returns trailing 7/30-day totals only (no back-history); each snapshot appends one point to <code>history.jsonl</code> — the trend chart above builds itself weekly. ARR figures hand-edited &amp; attributed in <code>_data/openrouter/arr.json</code>.</p>'
    '<p class="note">Generated ' + gen + ' · data © OpenRouter (public). Implied-$ and ARR-bridge figures are estimates, not the labs\' reported revenue.</p></div>'
    '</main>'
)


# ---------- PRESENTATION SHELL ----------
# Keep the analytical sections above simple to generate; add the navigation,
# executive layer and interaction hooks here so the weekly refresh stays safe.
BODY = BODY.replace(
    '<header>',
    '<a class="skip" href="#content">Skip to analysis</a><div class="progress" aria-hidden="true"><span></span></div>'
    '<header class="hero"><div class="hero-inner"><div class="eyebrow"><span class="status-dot"></span>'
    'Weekly market signal</div><div class="hero-grid"><div class="hero-copy">', 1)
BODY = BODY.replace(
    '</header>',
    '</div><div class="hero-actions"><a class="action" href="../index.html">Wiki home</a>'
    '<button class="action" id="themeToggle" type="button" aria-pressed="false">Dark mode</button>'
    '</div></div></div></header>', 1)

_nav_start = BODY.index('<nav class="tabs">')
_nav_end = BODY.index('</nav>', _nav_start) + len('</nav>')
_nav = (
    '<div class="page-shell"><aside class="rail"><div class="rail-label">Explore</div>'
    '<nav class="tabs" aria-label="Dashboard sections">'
    '<a class="active" href="#overview">Executive read</a><a href="#growth">System growth</a>'
    '<a href="#product">Workload mix</a><a href="#reality">Ceiling vs reality</a>'
    '<a href="#value">Tokens &ne; dollars</a><a href="#spend">Spend ranking</a>'
    '<a href="#labs">Lab leaderboard</a><a href="#models">Top models</a>'
    '<a href="#cloud">Cross-cloud pricing</a><a href="#neo">Neocloud market</a>'
    '<a href="#method">Methodology</a></nav>'
    '<div class="rail-note">OpenRouter public feed<br>Trailing 7-day window<br>Refreshes every Monday</div></aside>'
)
BODY = BODY[:_nav_start] + _nav + BODY[_nav_end:]
BODY = BODY.replace('<main>', '<main id="content" tabindex="-1">', 1)
BODY = BODY.replace(
    '<div class="callout warn">',
    '<section class="overview" id="overview"><div class="section-kicker">Executive read</div>'
    '<h2 class="overview-title">What matters in this snapshot</h2><div class="callout warn">', 1)
BODY = BODY.replace(
    '<div class="tiles">' + tiles_html + '</div>',
    '<div class="tiles">' + tiles_html + '</div><div class="insight-grid">' + insights_html + '</div></section>', 1)
BODY = BODY.replace('<h2>Is the $ real?', '<h2 id="reality">Is the $ real?', 1)
BODY = BODY.replace('<h2>Implied annualized spend by lab', '<h2 id="spend">Implied annualized spend by lab', 1)
BODY = BODY.replace('<h2>Share of implied $ over time', '<h2 id="trend">Share of implied $ over time', 1)
BODY = BODY.replace('<h2>Top models by implied spend</h2>', '<h2 id="models">Top models by implied spend</h2>', 1)
BODY = BODY.replace(
    '<h2 id="labs">Lab leaderboard</h2><div class="card scroll"><table class="sortable">',
    '<h2 id="labs">Lab leaderboard</h2><div class="card scroll"><div class="table-tools">'
    '<input class="table-search" data-table="lab-table" aria-label="Filter lab leaderboard" placeholder="Filter labs, capture type, or metric...">'
    '<span class="row-count" data-for="lab-table"></span></div><table class="sortable" id="lab-table">', 1)
BODY = BODY.replace(
    '<h2 id="models">Top models by implied spend</h2><div class="card scroll"><table class="sortable">',
    '<h2 id="models">Top models by implied spend</h2><div class="card scroll"><div class="table-tools">'
    '<input class="table-search" data-table="model-table" aria-label="Filter top models" placeholder="Filter models or labs...">'
    '<span class="row-count" data-for="model-table"></span></div><table class="sortable" id="model-table">', 1)
BODY = BODY.replace(
    '<div class="card scroll"><table class="sortable"><thead><tr><th>Model</th><th class="r">List / OpenRouter</th>',
    '<div class="card scroll"><div class="table-tools"><input class="table-search" data-table="cloud-table" '
    'aria-label="Filter cross-cloud pricing" placeholder="Filter models or venues..."><span class="row-count" '
    'data-for="cloud-table"></span></div><table class="sortable" id="cloud-table"><thead><tr><th>Model</th>'
    '<th class="r">List / OpenRouter</th>', 1)
BODY = BODY.replace(
    '<div class="card scroll"><table class="sortable"><thead><tr><th>Model</th><th class="r">Maker',
    '<div class="card scroll"><div class="table-tools"><input class="table-search" data-table="neo-table" '
    'aria-label="Filter neocloud pricing" placeholder="Filter models or providers..."><span class="row-count" '
    'data-for="neo-table"></span></div><table class="sortable" id="neo-table"><thead><tr><th>Model</th>'
    '<th class="r">Maker', 1)
BODY = BODY.replace(
    '</main>',
    '<button class="back-top" type="button" aria-label="Back to top">&uarr;</button></main></div>', 1)

# Full standalone page (local dashboard, links back to the wiki).
FULL = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>AI-Lab Traction — OpenRouter</title><style>' + CSS + '</style></head><body>' + BODY + '<script>' + JS + '</script></body></html>')
# Artifact fragment: no doctype/html/head/body (the Artifact host injects those); drop the wiki back-link.
FRAG = '<style>' + CSS + '</style>' + BODY.replace(' · <a href="../index.html">← wiki</a>', '') + '<script>' + JS + '</script>'

(DASH / "openrouter.html").write_text(FULL, encoding="utf-8", newline="\n")
(OR / "openrouter.artifact.html").write_text(FRAG, encoding="utf-8", newline="\n")
print("wrote", DASH / "openrouter.html", "(full %.0f KB) + artifact fragment (%.0f KB)" % (len(FULL) / 1024, len(FRAG) / 1024))
