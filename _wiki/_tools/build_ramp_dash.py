r"""build_ramp_dash.py -- Ramp AI Index dashboard.

Renders the two Ramp series held under _data/ramp-ai-index/ into one self-contained,
theme-aware page at _wiki/_dashboards/ramp-ai-index.html (also publishable as an
Artifact -- no external assets, no CDN, no fonts).

  model_share.json  (Jan-25 ->)  who gets used: provider mix, Anthropic's capability
                                 ladder, vintage turnover, launch curves.
  series.json       (Aug-23 ->)  how much gets spent: median monthly AI spend per
                                 employee, three cohorts.

The page's argument, in order: Anthropic has never lost the lead on this panel; the
mix moved UP the capability ladder in Dec-25; enterprise AI spend has essentially no
installed base (models <=3 months old hold most of it); and -- the load-bearing
caveat -- the spend series and the ladder shift are the SAME event seen twice, so the
spend acceleration is not clean evidence of volume diffusion.

Colour: dataviz skill. Categorical slots 1-3 (#2a78d6/#eb6834/#1baf7a light,
#3987e5/#d95926/#199e70 dark) validated --pairs all in both modes; the ordinal blue
ramps validated --ordinal in both modes. Light-mode aqua carries a contrast WARN, so
the relief rule applies: every chart ships a table view.

Run after build_ramp_index.py:
    py "E:\Wiki Felipe empresas\_wiki\_tools\build_ramp_dash.py"

Read-only on pages; writes only _wiki/_dashboards/ramp-ai-index.html. stdlib only.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DATA = os.path.join(WIKI, "_data", "ramp-ai-index")
OUT = os.path.join(WIKI, "_dashboards", "ramp-ai-index.html")
# --artifact: same page, wrapper-free, for publishing via the Artifact tool
ART = os.environ.get("RAMP_ARTIFACT_OUT",
                     os.path.join(WIKI, "_dashboards", "ramp-ai-index.artifact.html"))

MS = json.load(io.open(os.path.join(DATA, "model_share.json"), encoding="utf-8"))
SP = json.load(io.open(os.path.join(DATA, "series.json"), encoding="utf-8"))

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
D = MS["dates"]
N = len(D)


def lab(ym):
    y, m = ym.split("-")[:2]
    return "%s-%s" % (MON[int(m) - 1], y[2:])


def esc(s):
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f1(v):
    return "%.1f" % v


# --------------------------------------------------------------------------- derived
PROV = MS["providers"]
OTHER = [round(PROV["xAI"][i] + PROV["Cursor"][i], 4) for i in range(N)]
LAD = MS["anthropic_ladder_pct_all"]
LADR = MS["anthropic_ladder_pct_anthropic"]
VINT = MS["vintage_pct"]
CONC = MS["concentration"]
MODELS = MS["models"]

# frontier = Opus + Fable, as % of Anthropic's own mix (the ladder-shift line)
FRONT = [round((LADR["Opus"][i] or 0) + (LADR["Fable"][i] or 0), 2) for i in range(N)]

# spend series, restricted to the model-share window so the two panels share an x axis
SPD = SP["dates"]
SP0 = SPD.index(D[0])
SPMED = SP["cohorts"]["median"]["level"]
SPMOM = SP["cohorts"]["median"]["compound_3m_pct"]
SP_WIN = [SPMED[SP0 + i] for i in range(N)]
SPMOM_WIN = [SPMOM[SP0 + i] for i in range(N)]

LATEST = lab(D[-1])
PREV = lab(D[-2])

# ------------------------------------------------------------------- chart primitives
W, H = 1040, 344
# PAD_T leaves a clear band ABOVE the plot for the dated annotation labels: printed
# inside the plot they land on a filled band and fight the top gridline.
PAD_L, PAD_R, PAD_T, PAD_B = 46, 132, 32, 34
PW = W - PAD_L - PAD_R
PH = H - PAD_T - PAD_B


def xs(i):
    return PAD_L + (PW * i / float(N - 1))


def ys(v, vmax=100.0):
    return PAD_T + PH * (1 - v / vmax)


def xticks(step=2):
    o = []
    for i in range(0, N, step):
        o.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (xs(i), H - 12, lab(D[i])))
    if (N - 1) % step:
        o.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (xs(N - 1), H - 12, lab(D[-1])))
    return "".join(o)


def yaxis(vmax=100.0, step=25, suffix="%"):
    o = []
    v = 0
    while v <= vmax + 1e-9:
        y = ys(v, vmax)
        o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (PAD_L, y, PAD_L + PW, y))
        o.append('<text x="%d" y="%.1f" class="ax end">%g%s</text>' % (PAD_L - 8, y + 4, v, suffix))
        v += step
    return "".join(o)


def stack(series, colors, labels, vmax=100.0, gap=True):
    """Stacked area, bottom-up. 2px surface gap between bands (dataviz mark spec)."""
    base = [0.0] * N
    out = []
    for si, s in enumerate(series):
        top = [base[i] + s[i] for i in range(N)]
        pts_t = " ".join("%.1f,%.2f" % (xs(i), ys(top[i], vmax)) for i in range(N))
        pts_b = " ".join("%.1f,%.2f" % (xs(i), ys(base[i], vmax)) for i in range(N - 1, -1, -1))
        out.append('<polygon points="%s %s" fill="%s" fill-opacity=".92"/>' % (pts_t, pts_b, colors[si]))
        if gap and si < len(series) - 1:
            out.append('<polyline points="%s" fill="none" stroke="var(--surf)" stroke-width="2"/>' % pts_t)
        base = top
    # direct labels at the right edge, at each band's final mid-height
    base = [0.0] * N
    for si, s in enumerate(series):
        mid = base[N - 1] + s[N - 1] / 2.0
        if s[N - 1] >= vmax * 0.045:
            out.append('<text x="%.1f" y="%.1f" class="dlab">%s <tspan class="dnum">%s%%</tspan></text>'
                       % (PAD_L + PW + 9, ys(mid, vmax) + 4, esc(labels[si]), f1(s[N - 1])))
        base = [base[i] + s[i] for i in range(N)]
    return "".join(out)


def legend(colors, labels, notes=None):
    o = ['<div class="lg">']
    for i, l in enumerate(labels):
        n = ('<span class="lgn">%s</span>' % esc(notes[i])) if notes and notes[i] else ""
        o.append('<span><i style="background:%s"></i>%s%s</span>' % (colors[i], esc(l), n))
    o.append("</div>")
    return "".join(o)


def hoverlayer(cid):
    """Per-month hit columns + crosshair. Tooltip content is built in JS from CHARTS[cid]."""
    o = ['<g class="cross" id="cx_%s" style="display:none"><line y1="%d" y2="%d" class="cxl"/></g>' % (cid, PAD_T, PAD_T + PH)]
    half = PW / float(N - 1) / 2.0
    for i in range(N):
        x0 = max(PAD_L, xs(i) - half)
        x1 = min(PAD_L + PW, xs(i) + half)
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="transparent" '
                 'class="hit" data-c="%s" data-i="%d"/>' % (x0, PAD_T, x1 - x0, PH, cid, i))
    return "".join(o)


def svg(cid, body, aria):
    return ('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s" class="chart">%s%s</svg>'
            % (W, H, esc(aria), body, hoverlayer(cid)))


def annot(i, text, dy=0, align="middle"):
    """Dated vertical annotation rule, label in the clear band above the plot."""
    x = xs(i)
    return ('<g class="ann"><line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>'
            '<text x="%.1f" y="%d" text-anchor="%s" class="annt">%s</text></g>'
            % (x, PAD_T, x, PAD_T + PH, x, PAD_T - 8 + dy, align, esc(text)))


def table(headers, rows, cls="", cap=""):
    o = ['<details class="tv"><summary>Table view%s</summary><div class="tw"><table class="%s">' % (cap, cls)]
    o.append("<thead><tr>" + "".join("<th>%s</th>" % esc(h) for h in headers) + "</tr></thead><tbody>")
    for r in rows:
        o.append("<tr>" + "".join(
            ('<td class="%s">%s</td>' % (c[1], c[0])) if isinstance(c, tuple) else ("<td>%s</td>" % c)
            for c in r) + "</tr>")
    o.append("</tbody></table></div></details>")
    return "".join(o)


# ============================================================== chart 1: provider mix
C1 = ["var(--s1)", "var(--s2)", "var(--s3)"]
L1 = ["Anthropic", "OpenAI", "Other"]
S1 = [PROV["Anthropic"], PROV["OpenAI"], OTHER]
ch1 = (yaxis() + stack(S1, C1, L1)
       + annot(D.index("2025-07"), "Jul-25 low 50.4%")
       + annot(D.index("2026-03"), "Mar-26 high 77.8%")
       + xticks())

t1 = table(["Month", "Anthropic %", "OpenAI %", "xAI %", "Cursor %", "Models on panel", "Top model", "Top model %"],
           [[lab(D[i]), (f1(PROV["Anthropic"][i]), "r"), (f1(PROV["OpenAI"][i]), "r"),
             ("%.2f" % PROV["xAI"][i], "r"), ("%.2f" % PROV["Cursor"][i], "r"),
             (str(CONC[i]["n_models"]), "r"), CONC[i]["top1"], (f1(CONC[i]["top1_share"]), "r")]
            for i in range(N)], "num")

# ==================================================== chart 2: Anthropic ladder (ordinal)
LADC = ["var(--o1)", "var(--o2)", "var(--o3)", "var(--o4)"]
LADL = ["Haiku", "Sonnet", "Opus", "Fable"]
S2 = [LAD[f] for f in LADL]
ch2 = (yaxis() + stack(S2, LADC, LADL)
       + annot(D.index("2025-12"), "Dec-25 \u2014 Opus takes the mix")
       + xticks())

t2 = table(["Month", "Haiku", "Sonnet", "Opus", "Fable", "Anthropic total", "Opus+Fable, % of Anthropic"],
           [[lab(D[i])] + [(f1(LAD[f][i]), "r") for f in LADL]
            + [(f1(PROV["Anthropic"][i]), "r"), (f1(FRONT[i]), "r hl")] for i in range(N)], "num",
           cap=" \u2014 ladder as % of all named models")

# ============================================================== chart 3: vintage turnover
VC = ["var(--o2)", "var(--o3)", "var(--o4)"]
VL = ["\u22643 months old", "4\u201312 months", ">12 months"]
S3 = [VINT["le3"], VINT["m4_12"], VINT["gt12"]]
cens = D.index(MS["vintage_censored_through"])
# the wash marks the censored window; its caption goes in the clear band above the
# plot -- muted ink printed on the saturated fill was unreadable
ch3 = (yaxis() + stack(S3, VC, VL)
       + ('<rect x="%d" y="%d" width="%.1f" height="%d" class="cens"/>'
          '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>'
          '<text x="%.1f" y="%d" class="censt">\u2190 left-censored: model age understated</text>'
          % (PAD_L, PAD_T, xs(cens) - PAD_L, PH, xs(cens), PAD_T, xs(cens), PAD_T + PH,
             (PAD_L + xs(cens)) / 2, PAD_T - 8))
       + xticks())

t3 = table(["Month", "\u22643m old %", "4\u201312m %", ">12m %", "Models on panel", "HHI (0\u2013100)", "Top-3 %"],
           [[lab(D[i]), (f1(VINT["le3"][i]), "r"), (f1(VINT["m4_12"][i]), "r"),
             (f1(VINT["gt12"][i]) + ("*" if i <= cens else ""), "r"),
             (str(CONC[i]["n_models"]), "r"), ("%.1f" % CONC[i]["hhi"], "r"),
             (f1(CONC[i]["top3_share"]), "r")] for i in range(N)], "num",
           cap=" \u2014 * = censored, model age understated")

# ================================================================= chart 4: launch curves
LAUNCH = [m for m in MODELS if not m["censored"] and m["peak"] >= 4.0]
LAUNCH.sort(key=lambda m: m["first_i"])
MAXAGE = max(len(m["series"]) - m["first_i"] for m in LAUNCH)
SW, SH = 214, 132
SPL, SPR, SPT, SPB = 30, 8, 14, 22
SPW, SPPH = SW - SPL - SPR, SH - SPT - SPB
# one shared y-scale so panel heights are comparable; must clear the tallest peak
# (Sonnet 3.7 at 63.7%) or the leading model's curve is silently clipped
SMAX = float(int(max(m["peak"] for m in LAUNCH) / 10.0) * 10 + 10)
SGRID = [g for g in range(0, int(SMAX) + 1, 20)]


def sparkpanel(m):
    ser = m["series"][m["first_i"]:]
    ages = len(ser)
    px = lambda a: SPL + SPW * a / float(MAXAGE - 1)
    py = lambda v: SPT + SPPH * (1 - v / SMAX)
    pts = " ".join("%.1f,%.1f" % (px(a), py(ser[a])) for a in range(ages))
    area = ('<polygon points="%s %.1f,%.1f %.1f,%.1f" fill="%s" fill-opacity=".16"/>'
            % (pts, px(ages - 1), py(0), px(0), py(0),
               "var(--s2)" if m["provider"] == "OpenAI" else "var(--s1)"))
    col = "var(--s2)" if m["provider"] == "OpenAI" else "var(--s1)"
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s share by months since debut" class="sm">' % (SW, SH, esc(m["model"]))]
    for gv in SGRID:
        o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (SPL, py(gv), SPL + SPW, py(gv)))
        o.append('<text x="%d" y="%.1f" class="ax end sm-ax">%d</text>' % (SPL - 5, py(gv) + 3, gv))
    o.append(area)
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts, col))
    pk = m["months_to_peak"]
    o.append('<circle cx="%.1f" cy="%.1f" r="4.2" fill="var(--surf)" stroke="%s" stroke-width="2"/>'
             % (px(pk), py(m["peak"]), col))
    o.append('<text x="%.1f" y="%.1f" class="smpk" text-anchor="%s">%s%%</text>'
             % (px(pk) + (6 if pk < MAXAGE * .6 else -6), py(m["peak"]) - 6,
                "start" if pk < MAXAGE * .6 else "end", f1(m["peak"])))
    for a in (0, 6, 12, 18):
        if a <= MAXAGE - 1:
            o.append('<text x="%.1f" y="%d" class="ax mid sm-ax">%d</text>' % (px(a), SH - 7, a))
    o.append("</svg>")
    return ('<figure class="smf"><figcaption><b>%s</b><span>%s \u00b7 debut %s</span></figcaption>%s</figure>'
            % (esc(m["model"]), esc(m["provider"]), lab(m["first"]), "".join(o)))


t4 = table(["Model", "Provider", "Debut", "Debut share %", "Peak %", "Peak month", "Months to peak", "%s %%" % LATEST],
           [[esc(m["model"]), esc(m["provider"]), lab(m["first"]), (f1(m["debut_share"]), "r"),
             (f1(m["peak"]), "r hl"), lab(m["peak_month"]), (str(m["months_to_peak"]), "r"),
             (f1(m["latest"]), "r")]
            for m in sorted(MODELS, key=lambda x: -x["peak"]) if m["peak"] >= 0.5], "num",
           cap=" \u2014 every model peaking \u22650.5%")

# ==================================================== chart 5+6: the cross-read (two panels)
CH, CPT, CPB = 196, 22, 26
CPH = CH - CPT - CPB


def crosspanel(vals, vmax, color, ylabel, cid, step, fmt="%g%%", fill=True, tag=None):
    def cy(v):
        return CPT + CPH * (1 - v / float(vmax))
    o = []
    v = 0
    while v <= vmax + 1e-9:
        o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (PAD_L, cy(v), PAD_L + PW, cy(v)))
        o.append('<text x="%d" y="%.1f" class="ax end">%s</text>' % (PAD_L - 8, cy(v) + 4, fmt % v))
        v += step
    pts = " ".join("%.1f,%.2f" % (xs(i), cy(vals[i] or 0)) for i in range(N))
    if fill:
        o.append('<polygon points="%s %.1f,%.1f %.1f,%.1f" fill="%s" fill-opacity=".14"/>'
                 % (pts, PAD_L + PW, cy(0), PAD_L, cy(0), color))
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts, color))
    o.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="var(--surf)" stroke="%s" stroke-width="2.5"/>'
             % (xs(N - 1), cy(vals[-1] or 0), color))
    x = xs(D.index("2025-12"))
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>' % (x, CPT, x, CPT + CPH))
    if tag:
        o.append('<text x="%.1f" y="%d" text-anchor="middle" class="annt">%s</text>' % (x, CPT - 5, esc(tag)))
    o.append('<text x="%.1f" y="%d" class="dlab">%s</text>' % (PAD_L + PW + 9, cy(vals[-1] or 0) + 4, esc(ylabel)))
    for i in range(0, N, 2):
        o.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (xs(i), CH - 8, lab(D[i])))
    half = PW / float(N - 1) / 2.0
    for i in range(N):
        x0, x1 = max(PAD_L, xs(i) - half), min(PAD_L + PW, xs(i) + half)
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="transparent" class="hit" data-c="%s" data-i="%d"/>'
                 % (x0, CPT, x1 - x0, CPH, cid, i))
    return ('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s" class="chart">'
            '<g class="cross" id="cx_%s" style="display:none"><line y1="%d" y2="%d" class="cxl"/></g>%s</svg>'
            % (W, CH, esc(ylabel), cid, CPT, CPT + CPH, "".join(o)))


ch5 = crosspanel(FRONT, 100, "var(--s1)", "Opus+Fable", "front", 25,
                 tag="Dec-25 — the ladder flip")
ch6 = crosspanel(SP_WIN, 12, "var(--s2)", "$/employee", "spend", 3, fmt="$%g", fill=True)

t5 = table(["Month", "Opus+Fable, % of Anthropic", "Median AI spend / employee", "3-mo compound, %/mo"],
           [[lab(D[i]), (f1(FRONT[i]), "r"), ("$%.2f" % SP_WIN[i], "r"),
             ("%+.2f" % SPMOM_WIN[i] if SPMOM_WIN[i] is not None else "\u2014", "r")] for i in range(N)], "num")

# ============================================================ chart 7: spend, 3 cohorts
COH = [("median", "All companies", "var(--s1)"), ("top10", "Top 10%", "var(--s2)"), ("top1", "Top 1%", "var(--s3)")]
FULLD = SPD
FN = len(FULLD)
IH = 330
IPT, IPB = 18, 34
IPH = IH - IPT - IPB


def ix(i):
    return PAD_L + (PW * i / float(FN - 1))


# headroom for the tallest cohort index rather than clipping it flat against the top
IMAX = float(int(max(max(SP["cohorts"][k]["level"][i] / SP["cohorts"][k]["level"][0] * 100
                         for i in range(FN)) for k, _, _ in COH) / 100) * 100 + 100)


def iy(v):
    return IPT + IPH * (1 - v / IMAX)


idx_body = []
for gv in range(0, int(IMAX) + 1, 200):
    idx_body.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (PAD_L, iy(gv), PAD_L + PW, iy(gv)))
    idx_body.append('<text x="%d" y="%.1f" class="ax end">%d</text>' % (PAD_L - 8, iy(gv) + 4, gv))
for key, name, col in COH:
    lv = SP["cohorts"][key]["level"]
    b = lv[0]
    pts = " ".join("%.1f,%.2f" % (ix(i), iy(lv[i] / b * 100)) for i in range(FN))
    idx_body.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts, col))
    idx_body.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="var(--surf)" stroke="%s" stroke-width="2.5"/>'
                    % (ix(FN - 1), iy(lv[-1] / b * 100), col))
    idx_body.append('<text x="%.1f" y="%.1f" class="dlab">%s <tspan class="dnum">%d</tspan></text>'
                    % (PAD_L + PW + 9, iy(lv[-1] / b * 100) + 4, esc(name), round(lv[-1] / b * 100)))
xi = FULLD.index(D[0])
idx_body.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>' % (ix(xi), IPT, ix(xi), IPT + IPH))
idx_body.append('<text x="%.1f" y="%d" class="annt" text-anchor="middle">model-mix panel starts</text>' % (ix(xi), IPT + 12))
for i in range(0, FN, 3):
    idx_body.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (ix(i), IH - 12, lab(FULLD[i])))
half = PW / float(FN - 1) / 2.0
for i in range(FN):
    x0, x1 = max(PAD_L, ix(i) - half), min(PAD_L + PW, ix(i) + half)
    idx_body.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="transparent" class="hit" data-c="idx" data-i="%d"/>'
                    % (x0, IPT, x1 - x0, IPH, i))
ch7 = ('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Ramp AI spend per employee, three cohorts, indexed" class="chart">'
       '<g class="cross" id="cx_idx" style="display:none"><line y1="%d" y2="%d" class="cxl"/></g>%s</svg>'
       % (W, IH, IPT, IPT + IPH, "".join(idx_body)))

t7 = table(["Month", "All companies $", "Top 10% $", "Top 1% $", "All, index", "Top 10%, index", "Top 1%, index"],
           [[lab(FULLD[i])]
            + [("$%s" % format(SP["cohorts"][k]["level"][i], ",.2f"), "r") for k, _, _ in COH]
            + [(str(int(round(SP["cohorts"][k]["level"][i] / SP["cohorts"][k]["level"][0] * 100))), "r")
               for k, _, _ in COH] for i in range(FN)], "num",
           cap=" \u2014 Aug-23 = 100")

# ====================================================================== tooltip payload
CHARTS = {
    "prov": {"dates": [lab(d) for d in D], "unit": "%",
             "rows": [{"n": "Anthropic", "c": "var(--s1)", "v": PROV["Anthropic"]},
                      {"n": "OpenAI", "c": "var(--s2)", "v": PROV["OpenAI"]},
                      {"n": "Other (xAI, Cursor)", "c": "var(--s3)", "v": OTHER}],
             "foot": [CONC[i]["top1"] + " leads at " + f1(CONC[i]["top1_share"]) + "%" for i in range(N)]},
    "lad": {"dates": [lab(d) for d in D], "unit": "%",
            "rows": [{"n": f, "c": LADC[k], "v": LAD[f]} for k, f in enumerate(LADL)],
            "foot": ["Opus+Fable = " + f1(FRONT[i]) + "% of Anthropic's own mix" for i in range(N)]},
    "vint": {"dates": [lab(d) for d in D], "unit": "%",
             "rows": [{"n": VL[k], "c": VC[k], "v": S3[k]} for k in range(3)],
             "foot": [("%d models on panel \u00b7 HHI %.1f" % (CONC[i]["n_models"], CONC[i]["hhi"]))
                      + ("  \u2014 age censored" if i <= cens else "") for i in range(N)]},
    "front": {"dates": [lab(d) for d in D], "unit": "%",
              "rows": [{"n": "Opus+Fable, % of Anthropic", "c": "var(--s1)", "v": FRONT}], "foot": None},
    "spend": {"dates": [lab(d) for d in D], "unit": "$", "pre": True,
              "rows": [{"n": "Median AI spend / employee", "c": "var(--s2)", "v": SP_WIN}], "foot": None},
    "idx": {"dates": [lab(d) for d in FULLD], "unit": "$", "pre": True,
            "rows": [{"n": n, "c": c, "v": SP["cohorts"][k]["level"]} for k, n, c in COH], "foot": None},
}

# ============================================================================ stat tiles
def tile(v, l, s, tone=""):
    return ('<div class="tile %s"><div class="tv2">%s</div><div class="tl">%s</div><div class="ts">%s</div></div>'
            % (tone, v, esc(l), esc(s)))


anth_lo = min(PROV["Anthropic"])
anth_hi = max(PROV["Anthropic"])
oa_prev_hi = max(PROV["OpenAI"][D.index("2025-10"):-1])
sol = [m for m in MODELS if m["model"] == "GPT-5.6 Sol"]
sol_deb = sol[0]["debut_share"] if sol else 0
big_deb = max((m for m in MODELS if not m["censored"]), key=lambda m: m["debut_share"])
oa_debs = sorted((m for m in MODELS if m["provider"] == "OpenAI" and not m["censored"]),
                 key=lambda m: -m["debut_share"])[:2]

TILES = "".join([
    tile(f1(PROV["Anthropic"][-1]) + "%", "Anthropic, share of named-model usage",
         "%s \u00b7 %+.1fpp vs %s \u00b7 range %s\u2013%s%% since Jan-25"
         % (LATEST, PROV["Anthropic"][-1] - PROV["Anthropic"][-2], PREV, f1(anth_lo), f1(anth_hi))),
    tile(f1(PROV["OpenAI"][-1]) + "%", "OpenAI, same basis",
         "%s \u00b7 %+.1fpp vs %s \u00b7 best month since Sep-25" % (LATEST, PROV["OpenAI"][-1] - PROV["OpenAI"][-2], PREV)),
    tile(f1(FRONT[-1]) + "%", "Anthropic mix that is Opus or Fable",
         "was %s%% in Nov-25, the month before the flip" % f1(FRONT[D.index("2025-11")])),
    tile(f1(VINT["le3"][-1]) + "%", "usage on models \u22643 months old",
         ">12-month models hold just %s%% \u2014 no installed base" % f1(VINT["gt12"][-1])),
    tile("$" + format(SP_WIN[-1], ",.2f"), "median monthly AI spend / employee",
         "%s \u00b7 %+.0f%% y/y \u00b7 top 1%% at $%s"
         % (LATEST, SP["cohorts"]["median"]["yoy_pct"][-1], format(SP["cohorts"]["top1"]["level"][-1], ",.0f"))),
])

# ============================================================================== the page
CSS = """
:root{color-scheme:light;--plane:#f9f9f7;--surf:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
 --grid:#e1e0d9;--base:#c3c2b7;--border:rgba(11,11,11,.10);
 --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;
 --o1:#86b6ef;--o2:#3987e5;--o3:#1c5cab;--o4:#0d366b;
 --good:#0ca30c;--warn:#fab219;--crit:#d03b3b;--flag:#ec835a;
 --headbg:#0f1729;--headsub:#8492ad;--link:#7fb0ff;--wash:rgba(42,120,214,.06)}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){color-scheme:dark;
 --plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--base:#383835;
 --border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;--s3:#199e70;
 --o1:#cde2fb;--o2:#86b6ef;--o3:#3987e5;--o4:#184f95;--headbg:#000;--wash:rgba(57,135,229,.10)}}
:root[data-theme="dark"]{color-scheme:dark;--plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;
 --muted:#898781;--grid:#2c2c2a;--base:#383835;--border:rgba(255,255,255,.10);
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--o1:#cde2fb;--o2:#86b6ef;--o3:#3987e5;--o4:#184f95;
 --headbg:#000;--wash:rgba(57,135,229,.10)}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
 font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--headbg);color:#fff;padding:26px 30px 22px}
header h1{margin:0 0 6px;font-size:23px;letter-spacing:-.2px}
header p{margin:0;color:var(--headsub);max-width:104ch;font-size:13.5px}
header a{color:var(--link)}
main{padding:22px 30px 60px;max-width:1180px;margin:0 auto}
section{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin:0 0 18px}
h2{margin:0 0 3px;font-size:16.5px;letter-spacing:-.1px}
h2 .k{color:var(--muted);font-weight:400;font-size:12.5px;margin-left:8px;letter-spacing:0}
.sub{margin:0 0 14px;color:var(--ink2);font-size:13px;max-width:108ch}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(196px,1fr));gap:12px;margin:0 0 18px}
.tile{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.tv2{font-size:27px;font-weight:650;letter-spacing:-.6px;line-height:1.1}
.tl{font-size:12.5px;color:var(--ink2);margin-top:3px}
.ts{font-size:11.5px;color:var(--muted);margin-top:5px;line-height:1.42}
.chart,.sm{display:block;overflow:visible}
.grid{stroke:var(--grid);stroke-width:1}
.ax{fill:var(--muted);font-size:11px}
.sm-ax{font-size:9.5px}
.mid{text-anchor:middle}.end{text-anchor:end}
.dlab{fill:var(--ink2);font-size:12px;font-weight:500}
.dnum{fill:var(--ink);font-weight:650}
.annl{stroke:var(--ink);stroke-width:1;stroke-dasharray:3 3;opacity:.45}
.annt{fill:var(--ink2);font-size:10.5px}
.ann text{paint-order:stroke;stroke:var(--surf);stroke-width:3px}
.cens{fill:var(--muted);opacity:.10}
.censt{fill:var(--muted);font-size:10px;text-anchor:middle}
.cxl{stroke:var(--ink);stroke-width:1;opacity:.32}
.smpk{fill:var(--ink);font-size:10.5px;font-weight:650;paint-order:stroke;stroke:var(--surf);stroke-width:3px}
.lg{display:flex;flex-wrap:wrap;gap:6px 20px;margin:12px 0 2px;font-size:12.5px;color:var(--ink2)}
.lg span{display:inline-flex;align-items:center;gap:7px}
.lg i{width:11px;height:11px;border-radius:3px;display:inline-block;flex:0 0 auto}
.lgn{color:var(--muted);font-size:11.5px}
.smgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(214px,1fr));gap:14px 16px;margin-top:6px}
.smf{margin:0}
.smf figcaption{font-size:12px;color:var(--ink2);margin:0 0 2px;display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.smf figcaption b{color:var(--ink);font-weight:620}
.smf figcaption span{color:var(--muted);font-size:10.5px;text-align:right}
.tv{margin-top:14px;border-top:1px solid var(--border);padding-top:10px}
.tv summary{cursor:pointer;color:var(--ink2);font-size:12.5px}
.tv summary:hover{color:var(--ink)}
.tw{max-height:430px;overflow:auto;margin-top:10px;border:1px solid var(--border);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:12px}
th,td{padding:5px 10px;border-bottom:1px solid var(--border);text-align:left;white-space:nowrap}
th{position:sticky;top:0;background:var(--surf);color:var(--ink2);font-weight:600;z-index:1}
td.r,th.r{text-align:right;font-variant-numeric:tabular-nums}
td.hl{font-weight:650}
tbody tr:hover{background:var(--wash)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.note{border-left:3px solid var(--flag);background:var(--wash);border-radius:0 8px 8px 0;padding:11px 14px;margin:14px 0 0;font-size:12.8px;color:var(--ink2)}
.note b{color:var(--ink)}
.note.warnn{border-left-color:var(--crit)}
ul.cav{margin:10px 0 0;padding-left:19px;font-size:12.8px;color:var(--ink2)}
ul.cav li{margin-bottom:7px}
ul.cav b{color:var(--ink)}
#tt{position:fixed;pointer-events:none;z-index:60;background:var(--surf);border:1px solid var(--border);
 border-radius:9px;padding:9px 11px;font-size:12px;box-shadow:0 8px 26px rgba(0,0,0,.20);display:none;min-width:186px}
#tt .h{font-weight:650;margin-bottom:6px;color:var(--ink)}
#tt .rw{display:flex;align-items:center;gap:8px;justify-content:space-between;margin:2px 0;color:var(--ink2)}
#tt .rw i{width:9px;height:9px;border-radius:2px;display:inline-block;flex:0 0 auto}
#tt .rw b{color:var(--ink);font-variant-numeric:tabular-nums}
#tt .ft{margin-top:6px;padding-top:5px;border-top:1px solid var(--border);color:var(--muted);font-size:11px}
footer{color:var(--muted);font-size:11.5px;padding:0 30px 40px;max-width:1180px;margin:0 auto;line-height:1.6}
@media(max-width:900px){.cols{grid-template-columns:1fr}main,header,footer{padding-left:16px;padding-right:16px}}
"""

JS = """
var CHARTS=%s;
var tt=document.getElementById('tt');
function grp(s){var p=s.split('.');p[0]=p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');return p.join('.');}
function fmt(v,u,pre){if(v==null)return'\\u2014';return pre?(u+grp(v.toFixed(2))):(v.toFixed(v<10?2:1)+u);}
document.addEventListener('mousemove',function(e){
 var t=e.target;
 if(!t.classList||!t.classList.contains('hit')){hide();return;}
 var cid=t.getAttribute('data-c'),i=+t.getAttribute('data-i'),C=CHARTS[cid];if(!C)return;
 var g=document.getElementById('cx_'+cid);
 if(g){var ln=g.querySelector('line');var x=t.getAttribute('x')*1+t.getAttribute('width')/2;
  ln.setAttribute('x1',x);ln.setAttribute('x2',x);g.style.display='';}
 var h='<div class="h">'+C.dates[i]+'</div>';
 for(var k=0;k<C.rows.length;k++){var r=C.rows[k];
  h+='<div class="rw"><span style="display:inline-flex;align-items:center;gap:7px"><i style="background:'+r.c+'"></i>'+r.n+'</span><b>'+fmt(r.v[i],C.unit,C.pre)+'</b></div>';}
 if(C.foot&&C.foot[i])h+='<div class="ft">'+C.foot[i]+'</div>';
 tt.innerHTML=h;tt.style.display='block';
 var w=tt.offsetWidth,hh=tt.offsetHeight;
 var L=e.clientX+16,T=e.clientY-hh/2;
 if(L+w>innerWidth-10)L=e.clientX-w-16;
 if(T<8)T=8; if(T+hh>innerHeight-8)T=innerHeight-hh-8;
 tt.style.left=L+'px';tt.style.top=T+'px';
});
function hide(){tt.style.display='none';
 var c=document.querySelectorAll('.cross');for(var i=0;i<c.length;i++)c[i].style.display='none';}
document.addEventListener('mouseleave',hide);
"""


def build(artifact=False):
    """artifact=True emits the Artifact variant: no doctype/html/head/body wrapper
    (the Artifact host supplies its own skeleton), title + style at the top."""
    p = []
    if artifact:
        p.append("<title>Ramp AI Index</title><style>%s</style>" % CSS)
    else:
        p.append("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             "<meta name='viewport' content='width=device-width,initial-scale=1'>"
             "<title>Ramp AI Index \u2014 model mix &amp; enterprise AI spend</title>"
             "<style>%s</style></head><body>" % CSS)


    p.append("<header><h1>Ramp AI Index \u2014 who gets used, and what gets spent</h1>"
             "<p>Two monthly series off the same Ramp panel (US corporate-card / bill-pay customers): "
             "<b>model mix</b>, %s\u2013%s, %d months and %d named models; and <b>AI spend per employee</b>, "
             "%s\u2013%s, %d months. Shares sum to 100%% each month across the models Ramp names. "
             "<b>Read the coverage caveat before quoting any number as market share</b> \u2014 "
             "Google/Gemini, Meta, Mistral and DeepSeek appear in no month of this panel. "
             "Primary data on disk at <code>_wiki/_data/ramp-ai-index/</code>; rebuild with "
             "<code>build_ramp_index.py</code> \u2192 <code>build_ramp_dash.py</code>.</p></header>"
             % (lab(D[0]), LATEST, N, len(MODELS), lab(SPD[0]), lab(SPD[-1]), len(SPD)))

    p.append("<main>")
    p.append('<div class="tiles">%s</div>' % TILES)

    # 1 ---------------------------------------------------------------- provider mix
    p.append('<section><h2>1 \u00b7 Anthropic has never lost this panel<span class="k">provider share of named-model usage, %%</span></h2>'
             '<p class="sub">Nineteen months, and Anthropic leads in every one of them. The narrowest month was '
             'Jul-25 (%s%% vs %s%%); the widest Mar-26 (%s%%). %s is Anthropic\u2019s weakest month since Jan-26 '
             'and OpenAI\u2019s strongest since Sep-25 \u2014 driven almost entirely by one launch, GPT-5.6 Sol, which '
             'took %s%% in its debut month.</p>%s%s%s</section>'
             % (f1(PROV["Anthropic"][D.index("2025-07")]), f1(PROV["OpenAI"][D.index("2025-07")]),
                f1(anth_hi), LATEST, f1(sol_deb),
                svg("prov", ch1, "Provider share of Ramp named-model usage by month"),
                legend(C1, ["Anthropic", "OpenAI", "Other \u2014 xAI + Cursor"],
                       [None, None, "%s%% combined in %s" % ("%.2f" % OTHER[-1], LATEST)]), t1))

    # 2 ---------------------------------------------------------------- the ladder
    p.append('<section><h2>2 \u00b7 The mix moved up the ladder in one month<span class="k">Anthropic model families, %% of all named models</span></h2>'
             '<p class="sub">Between Nov-25 and Dec-25 Opus went from %s%% to %s%% of Anthropic\u2019s own mix \u2014 '
             'a single-month step from a premium niche to the majority of usage, and it has stayed there since '
             '(%s%% in %s including Fable). Sonnet, which held two thirds of the whole panel in early 2025, is now '
             '%s%%. <b>This is a price/mix event as much as a usage event</b>: flagship tiers list at a multiple of '
             'mid-tier per token, so a shift of this size lifts spend even with flat token volume. Section 5 is where '
             'that matters.</p>%s%s%s</section>'
             % (f1(FRONT[D.index("2025-11")]), f1(LADR["Opus"][D.index("2025-12")]), f1(FRONT[-1]), LATEST,
                f1(LAD["Sonnet"][-1]),
                svg("lad", ch2, "Anthropic model families as a share of all named-model usage"),
                legend(LADC, ["Haiku", "Sonnet", "Opus", "Fable"],
                       ["cheapest", None, None, "top tier, per ANTHROPIC.md"]), t2))

    # 3 ---------------------------------------------------------------- vintage
    p.append('<section><h2>3 \u00b7 Enterprise AI has no installed base<span class="k">usage by model age, %%</span></h2>'
             '<p class="sub">Models first seen within the last three months hold <b>%s\u2013%s%%</b> of all usage in '
             'every month of 2026. Models older than a year hold <b>%s%%</b>. Nothing sediments: each release '
             're-races the whole panel, and %d models are live in %s against 7 at the start. <b>The shaded region is '
             'left-censored</b> \u2014 age is measured from first appearance in the panel (Jan-25), not from true '
             'release, so the &gt;12-month band cannot fill until %s.</p>%s%s%s</section>'
             % (f1(min(VINT["le3"][D.index("2026-01"):])), f1(max(VINT["le3"][D.index("2026-01"):])),
                f1(VINT["gt12"][-1]), CONC[-1]["n_models"], LATEST, lab(D[cens + 1]),
                svg("vint", ch3, "Share of usage by model age bucket"),
                legend(VC, VL, ["the re-race", None, "the residue"]), t3))

    # 4 ---------------------------------------------------------------- launch curves
    p.append('<section><h2>4 \u00b7 Launch curves<span class="k">share by months since debut \u00b7 every model peaking \u22654%%</span></h2>'
             '<p class="sub">Each panel starts at a model\u2019s first month on the panel; the ring marks its peak. '
             'The shape is consistent: a fast climb to a peak inside <b>%d\u2013%d months</b>, then a decay as the next '
             'release lands. The largest debut in the file is <b>%s at %s%%</b> (%s). OpenAI\u2019s largest is '
             '<b>%s at %s%%</b>, just ahead of %s\u2019s %s%%. Panels share one axis (0\u2013%d%%), so heights are '
             'comparable across models; blue is Anthropic, orange OpenAI.</p><div class="smgrid">%s</div>%s</section>'
             % (min(m["months_to_peak"] for m in LAUNCH), max(m["months_to_peak"] for m in LAUNCH),
                esc(big_deb["model"]), f1(big_deb["debut_share"]), lab(big_deb["first"]),
                esc(oa_debs[0]["model"]), f1(oa_debs[0]["debut_share"]),
                esc(oa_debs[1]["model"]), f1(oa_debs[1]["debut_share"]), int(SMAX),
                "".join(sparkpanel(m) for m in LAUNCH), t4))

    # 5 ---------------------------------------------------------------- cross-read
    p.append('<section><h2>5 \u00b7 The cross-read \u2014 and the caution it carries<span class="k">ladder shift vs spend per employee, same axis</span></h2>'
             '<p class="sub">Two separate panels, one shared time axis, dashed rule at Dec-25. Anthropic\u2019s mix '
             'flips to Opus in the same month the spend series changes regime: median spend per employee compounded '
             '<b>+3.96%%/mo</b> over the twelve months to Dec-25, then <b>+12.44%%/mo</b> over the seven months since '
             '($5.26 \u2192 $%s, +127%%).</p>%s%s'
             '<div class="note warnn"><b>The wiki currently reads the spend series as evidence of demand diffusion '
             '(<code>themes/macro-cycle.md</code>: \u201cspend diffusion IS accelerating sharply\u201d). This chart '
             'says that read is not clean.</b> The same panel shows a simultaneous mix shift up the price ladder, and '
             'a flagship token costs a multiple of a mid-tier one. Some unknown part of the +12.44%%/mo is therefore '
             '<i>price and mix</i>, not more AI being used. The two series cannot separate them: Ramp gives spend and '
             'model identity, not tokens. <b>Neither the volume read nor the price read is provable from this file</b> '
             '\u2014 what is provable is that whoever quotes the spend acceleration as diffusion owes a mix '
             'adjustment. Resolving it needs per-model token volume or list-price weights, neither of which is in the '
             'panel. Co-timing is not causation in either direction; both could follow a third driver (agentic coding '
             'adoption is the obvious candidate).</div>%s</section>'
             % (format(SP_WIN[-1], ",.2f"), ch5, ch6, t5))

    # 6 ---------------------------------------------------------------- spend series
    p.append('<section><h2>6 \u00b7 The spend series in full<span class="k">three cohorts, indexed, %s = 100</span></h2>'
             '<p class="sub">Levels differ by ~600x across cohorts ($%s vs $%s vs $%s in %s), so the chart indexes '
             'each to its own Aug-23 base \u2014 never two y-axes. Cohorts are <b>re-cut every month</b>, so part of '
             'each step is re-ranking rather than same-company growth, which is why the top-1%% cohort is the noisiest '
             'line here and the least safe to quote month-to-month.</p>%s%s%s</section>'
             % (lab(SPD[0]), format(SPMED[-1], ",.2f"), format(SP["cohorts"]["top10"]["level"][-1], ",.2f"),
                format(SP["cohorts"]["top1"]["level"][-1], ",.0f"), lab(SPD[-1]),
                ch7, legend([c for _, _, c in COH], [n for _, n, _ in COH],
                            ["$%s" % format(SPMED[-1], ",.2f"),
                             "$%s" % format(SP["cohorts"]["top10"]["level"][-1], ",.2f"),
                             "$%s" % format(SP["cohorts"]["top1"]["level"][-1], ",.0f")]), t7))

    # 7 ---------------------------------------------------------------- reconciliation
    p.append('<section><h2>7 \u00b7 Reconciliation and basis traps<span class="k">read this before quoting anything above</span></h2>'
             '<div class="note"><b>The %s%%-vs-%s%% trap.</b> <code>_wiki/ANTHROPIC.md</code> carries a different '
             'Ramp cut: as of Jun-2026 Anthropic is the most-used AI vendor among US businesses at <b>~41%% of firms '
             'vs OpenAI ~39.5%%</b> (Big Technology podcast w/ Ramp\u2019s Ara Kharazian, 2026-06-18). This page has '
             'Anthropic at <b>%s%%</b> and OpenAI at <b>%s%%</b> for the same month. <b>Both can be right \u2014 they '
             'are different denominators.</b> The vendor-adoption cut counts <i>firms</i> and lets a firm be counted '
             'for both vendors (it need not sum to 100); this cut is a share of named-model usage and does sum to 100. '
             'Read together they say Anthropic and OpenAI are close to <b>tied on enterprise penetration</b> while '
             'Anthropic takes roughly <b>2.5x the model-level share</b> \u2014 i.e. Anthropic\u2019s lead here is '
             'intensity per customer, not customer count. That is a claim worth carrying; \u201cAnthropic has 71%% of '
             'the enterprise LLM market\u201d is not.</div>'
             '<ul class="cav">%s</ul>'
             '<div class="note"><b>What would change the picture.</b> A second consecutive month of OpenAI share '
             'gains (%s\u2019s %+.1fpp was one launch); any appearance of Google/Gemini rows, which would restate '
             'every share on this page; a Ramp methodology note fixing the weighting basis; or the vintage &le;3m band '
             'falling below ~50%%, which would be the first sign that model releases have stopped resetting the '
             'panel.</div></section>'
             % (f1(PROV["Anthropic"][D.index("2026-06")]), f1(PROV["OpenAI"][D.index("2026-06")]),
                f1(PROV["Anthropic"][D.index("2026-06")]), f1(PROV["OpenAI"][D.index("2026-06")]),
                "".join("<li>%s</li>" % esc(c).replace("COVERAGE:", "<b>COVERAGE:</b>")
                        .replace("BASIS:", "<b>BASIS:</b>")
                        .replace("VINTAGE IS LEFT-CENSORED:", "<b>VINTAGE IS LEFT-CENSORED:</b>")
                        for c in MS["caveats"]),
                LATEST, PROV["OpenAI"][-1] - PROV["OpenAI"][-2]))

    p.append("</main>")
    p.append('<div id="tt"></div>')
    p.append("<footer>Source: <b>Ramp AI Index</b> \u2014 model mix CSV supplied by Felipe 2026-09-02 "
             "(<code>ramp-ai-index-model-share.csv</code>), spend-per-employee CSV 2026-08-20. "
             "Raw + derived on disk at <code>_wiki/_data/ramp-ai-index/</code>. Ramp\u2019s own methodology note is "
             "<b>not verified</b>: cohort definitions are read off column headers and the model-share weighting basis "
             "is not stated in the export. Panel is Ramp\u2019s US corporate-card / bill-pay customer base \u2014 not "
             "total enterprise AI spend, and not a revenue proxy for any listed name. "
             "Anthropic tier ordering (Haiku&lt;Sonnet&lt;Opus&lt;Fable) is the wiki\u2019s read per "
             "<code>_wiki/ANTHROPIC.md</code>, not a Ramp field. "
             "Built by <code>_wiki/_tools/build_ramp_dash.py</code>.</footer>")
    p.append("<script>%s</script>" % (JS % json.dumps(CHARTS)))
    if not artifact:
        p.append("</body></html>")

    html = "".join(p)
    dest = ART if artifact else OUT
    with io.open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  (%.1f KB)" % (dest, len(html.encode("utf-8")) / 1024.0))


if __name__ == "__main__":
    import sys
    build(artifact="--artifact" in sys.argv)
