r"""build_ramp_dash.py -- Ramp AI Index dashboard.

Renders everything held under _data/ramp-ai-index/ into one self-contained, theme-aware
page at _wiki/_dashboards/ramp-ai-index.html (no external assets, no CDN, no fonts).

  panel.json        (Jul-23 ->)  adoption (Ramp vs Census, by vendor / size / sector),
                                 AI share of business spend, spend-per-employee extras and
                                 segment cuts, model share by segment, and the Token Spend
                                 Management sample (weekly volume / spend by maker, $/M).
  model_share.json  (Jan-25 ->)  who gets used: provider mix, Anthropic's capability
                                 ladder, vintage turnover, launch curves.
  series.json       (Oct-23 ->)  how much gets spent: median monthly AI spend per
                                 employee, three cohorts.
  restatement.json               what Ramp re-cut vs the archived vintages.

Every number in the prose is computed from the data at build time -- nothing is typed
in -- so the page re-reads itself when fetch_ramp_index.py pulls a new month.

Colour: dataviz skill. Categorical slots 1-3 (#2a78d6/#eb6834/#1baf7a light,
#3987e5/#d95926/#199e70 dark) validated --pairs in both modes; the ordinal blue ramps
validated --ordinal in both modes. Light-mode aqua carries a contrast WARN, so the
relief rule applies: every chart ships a table view.

Run after fetch_ramp_index.py -> build_ramp_index.py:
    py "E:\Wiki Felipe empresas\_wiki\_tools\build_ramp_dash.py"            [--artifact]

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


def _load(name, default=None):
    p = os.path.join(DATA, name)
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else default


MS = _load("model_share.json")
SP = _load("series.json")
PN = _load("panel.json")
RS = _load("restatement.json", {})
META = _load("fetch_meta.json", {})

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
D = MS["dates"]
N = len(D)


def lab(ym):
    y, m = ym.split("-")[:2]
    return "%s-%s" % (MON[int(m) - 1], y[2:])


def labw(ymd):
    """weekly label: '12 Oct 26'"""
    y, m, d = ymd.split("-")[:3]
    return "%d %s %s" % (int(d), MON[int(m) - 1], y[2:])


def esc(s):
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f1(v):
    return "\u2014" if v is None else "%.1f" % v


def f2(v):
    return "\u2014" if v is None else "%.2f" % v


def money(v, dec=2):
    return "\u2014" if v is None else "$" + format(v, ",.%df" % dec)


def pct_change(a, b):
    return None if (a in (None, 0) or b is None) else (b / a - 1) * 100


def compound(a, b, months):
    return None if (a in (None, 0) or b is None or months <= 0) else ((b / a) ** (1.0 / months) - 1) * 100


# --------------------------------------------------------------------------- derived
PROV = MS["providers"]
OTHER = [round(sum(PROV[p][i] for p in PROV if p not in ("Anthropic", "OpenAI")), 4) for i in range(N)]
LAD = MS["anthropic_ladder_pct_all"]
LADR = MS["anthropic_ladder_pct_anthropic"]
VINT = MS["vintage_pct"]
CONC = MS["concentration"]
MODELS = MS["models"]
LATEST = lab(D[-1])
PREV = lab(D[-2])

# frontier = Opus + Fable, as % of Anthropic's own mix (the ladder-shift line)
FRONT = [round((LADR["Opus"][i] or 0) + (LADR["Fable"][i] or 0), 2) for i in range(N)]
# the flip month = the largest single-month rise in the frontier share
FLIP = max(range(1, N), key=lambda i: FRONT[i] - FRONT[i - 1])
FLIP_M = D[FLIP]

# spend series on the model-share window so the two panels share an x axis
SPD = SP["dates"]
SP0 = SPD.index(D[0])
SPMED = SP["cohorts"]["median"]["level"]
SPMOM = SP["cohorts"]["median"]["compound_3m_pct"]
SP_WIN = [SPMED[SP0 + i] for i in range(N)]
SPMOM_WIN = [SPMOM[SP0 + i] for i in range(N)]
# regimes around the flip, on the spend series' own index
fs = SPD.index(FLIP_M)
REG_PRE = compound(SPMED[max(0, fs - 12)], SPMED[fs], min(12, fs))
REG_POST = compound(SPMED[fs], SPMED[-1], len(SPD) - 1 - fs)
POST_MONTHS = len(SPD) - 1 - fs

# adoption / panel
AD = PN["adoption"]["dates"]
AN = len(AD)
ADO = PN["adoption"]["overall"]
CEN = PN["adoption"]["census"]
VEN = PN["adoption"]["vendor"]
VEN_ORDER = sorted(VEN, key=lambda k: -(VEN[k][-1] or 0))
CROSS = PN["adoption"]["vendor_crossover_anthropic_gt_openai"]
SIZE = PN["adoption"]["size"]
SECT = PN["adoption"]["sector"]
SS = PN["spend_share"]
SX = PN["spend_extra"]
SC = PN["spend_curated"]
MSC = PN["model_share_curated"]
TK = PN["tokens"]
WK = TK["weeks"]
WN = len(WK)
MAKERS = TK["makers"]
LAT_A = lab(AD[-1])

# tokens: maker groups for the stacked share chart
TOP_MAKERS = ["anthropic", "openai", "google", "xai"]
MK_LABEL = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google", "xai": "xAI",
            "cursor": "Cursor", "moonshot": "Moonshot", "deepseek": "DeepSeek", "meta": "Meta",
            "alibaba": "Alibaba", "zhipu": "Zhipu", "minimax": "MiniMax", "nvidia": "NVIDIA",
            "thinking-machines-lab": "Thinking Machines", "typesafe": "Typesafe"}
VOL = TK["volume_by_maker"]
SPND = TK["spend_by_maker"]
WTOT = [sum(VOL[m][i] for m in VOL) for i in range(WN)]
WSTOT = [sum(SPND[m][i] for m in SPND) for i in range(WN)]
VSHARE = {}
for m in TOP_MAKERS:
    VSHARE[m] = [100.0 * VOL[m][i] / WTOT[i] if WTOT[i] else 0 for i in range(WN)]
VSHARE["other"] = [max(0.0, 100.0 - sum(VSHARE[m][i] for m in TOP_MAKERS)) for i in range(WN)]
# blended $/M by maker, weekly (spend / volume), the price-vs-volume key
BLEND = {}
for m in ("anthropic", "openai"):
    BLEND[m] = [1e6 * SPND[m][i] / VOL[m][i] if VOL[m][i] else None for i in range(WN)]
BLEND["all"] = [1e6 * WSTOT[i] / WTOT[i] if WTOT[i] else None for i in range(WN)]
# monthly roll-up (complete months) for the cross-read against spend per employee
MM = TK["months_complete"]
MV = TK["monthly_volume_by_maker"]
MSP = TK["monthly_spend_by_maker"]
MTOT_V = [sum(MV[m][i] for m in MV) for i in range(len(MM))]
MTOT_S = [sum(MSP[m][i] for m in MSP) for i in range(len(MM))]
MBLEND_ALL = [1e6 * MTOT_S[i] / MTOT_V[i] if MTOT_V[i] else None for i in range(len(MM))]
MBLEND_ANT = [1e6 * MSP["anthropic"][i] / MV["anthropic"][i] if MV["anthropic"][i] else None for i in range(len(MM))]
# the decomposition over the post-flip window, where the two series overlap
mf = MM.index(FLIP_M) if FLIP_M in MM else 0
ml = len(MM) - 1
DEC = {
    "months": ml - mf, "from": MM[mf], "to": MM[ml],
    "spend_x": MTOT_S[ml] / MTOT_S[mf] if MTOT_S[mf] else None,
    "vol_x": MTOT_V[ml] / MTOT_V[mf] if MTOT_V[mf] else None,
    "price_x": (MBLEND_ALL[ml] / MBLEND_ALL[mf]) if (MBLEND_ALL[mf] and MBLEND_ALL[ml]) else None,
    "ant_spend_x": MSP["anthropic"][ml] / MSP["anthropic"][mf] if MSP["anthropic"][mf] else None,
    "ant_vol_x": MV["anthropic"][ml] / MV["anthropic"][mf] if MV["anthropic"][mf] else None,
    "ant_price_x": (MBLEND_ANT[ml] / MBLEND_ANT[mf]) if (MBLEND_ANT[mf] and MBLEND_ANT[ml]) else None,
    "pepm_x": SPMED[-1] / SPMED[fs] if SPMED[fs] else None,
}

# ------------------------------------------------------------------- chart primitives
W, H = 1040, 344
PAD_L, PAD_R, PAD_T, PAD_B = 46, 132, 32, 34
PW = W - PAD_L - PAD_R
PH = H - PAD_T - PAD_B


class Ax(object):
    """One x axis over a date list; every chart on the page builds on this."""

    def __init__(self, dates, h=H, pt=PAD_T, pb=PAD_B, weekly=False):
        self.d, self.n, self.h, self.pt, self.pb = dates, len(dates), h, pt, pb
        self.ph = h - pt - pb
        self.weekly = weekly

    def x(self, i):
        return PAD_L + (PW * i / float(self.n - 1))

    def y(self, v, vmax, vmin=0.0):
        return self.pt + self.ph * (1 - (v - vmin) / float(vmax - vmin))

    def lab(self, i):
        return labw(self.d[i]) if self.weekly else lab(self.d[i])

    def ticks(self, step):
        o = []
        for i in range(0, self.n, step):
            o.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (self.x(i), self.h - 12, self.lab(i)))
        if (self.n - 1) % step and (self.n - 1) - ((self.n - 1) // step) * step >= step * 0.45:
            o.append('<text x="%.1f" y="%d" class="ax mid">%s</text>' % (self.x(self.n - 1), self.h - 12, self.lab(self.n - 1)))
        return "".join(o)

    def yaxis(self, vmax, step, fmt="%g%%", vmin=0.0):
        o = []
        v = vmin
        while v <= vmax + 1e-9:
            y = self.y(v, vmax, vmin)
            o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (PAD_L, y, PAD_L + PW, y))
            o.append('<text x="%d" y="%.1f" class="ax end">%s</text>' % (PAD_L - 8, y + 4, fmt % v))
            v += step
        return "".join(o)

    def hover(self, cid):
        o = ['<g class="cross" id="cx_%s" style="display:none"><line y1="%d" y2="%d" class="cxl"/></g>' % (cid, self.pt, self.pt + self.ph)]
        half = PW / float(self.n - 1) / 2.0
        for i in range(self.n):
            x0 = max(PAD_L, self.x(i) - half)
            x1 = min(PAD_L + PW, self.x(i) + half)
            o.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="transparent" class="hit" data-c="%s" data-i="%d"/>'
                     % (x0, self.pt, x1 - x0, self.ph, cid, i))
        return "".join(o)

    def svg(self, cid, body, aria):
        return ('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s" class="chart">%s%s</svg>'
                % (W, self.h, esc(aria), body, self.hover(cid)))

    def annot(self, i, text, dy=0, align="middle"):
        x = self.x(i)
        return ('<g class="ann"><line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>'
                '<text x="%.1f" y="%d" text-anchor="%s" class="annt">%s</text></g>'
                % (x, self.pt, x, self.pt + self.ph, x, self.pt - 8 + dy, align, esc(text)))

    def stack(self, series, colors, labels, vmax=100.0, gap=True, suffix="%"):
        base = [0.0] * self.n
        out = []
        for si, s in enumerate(series):
            top = [base[i] + (s[i] or 0) for i in range(self.n)]
            pts_t = " ".join("%.1f,%.2f" % (self.x(i), self.y(top[i], vmax)) for i in range(self.n))
            pts_b = " ".join("%.1f,%.2f" % (self.x(i), self.y(base[i], vmax)) for i in range(self.n - 1, -1, -1))
            out.append('<polygon points="%s %s" fill="%s" fill-opacity=".92"/>' % (pts_t, pts_b, colors[si]))
            if gap and si < len(series) - 1:
                out.append('<polyline points="%s" fill="none" stroke="var(--surf)" stroke-width="2"/>' % pts_t)
            base = top
        base = [0.0] * self.n
        for si, s in enumerate(series):
            v = s[self.n - 1] or 0
            mid = base[self.n - 1] + v / 2.0
            if v >= vmax * 0.045:
                out.append('<text x="%.1f" y="%.1f" class="dlab">%s <tspan class="dnum">%s%s</tspan></text>'
                           % (PAD_L + PW + 9, self.y(mid, vmax) + 4, esc(labels[si]), f1(v), suffix))
            base = [base[i] + (s[i] or 0) for i in range(self.n)]
        return "".join(out)

    def lines(self, series, colors, labels, vmax, vmin=0.0, fmt=None, fill_first=False, width=2):
        """Multi-line with gaps on None, end-ring and direct label on each line.
        Labels are nudged apart so they never overprint."""
        out = []
        ends = []
        for si, s in enumerate(series):
            segs, cur = [], []
            for i in range(self.n):
                if s[i] is None:
                    if cur:
                        segs.append(cur)
                    cur = []
                else:
                    cur.append("%.1f,%.2f" % (self.x(i), self.y(s[i], vmax, vmin)))
            if cur:
                segs.append(cur)
            if fill_first and si == 0 and segs:
                first = segs[0][0].split(",")[0]
                lastx = segs[-1][-1].split(",")[0]
                out.append('<polygon points="%s %s,%.1f %s,%.1f" fill="%s" fill-opacity=".12"/>'
                           % (" ".join(" ".join(g) for g in segs), lastx, self.y(vmin, vmax, vmin), first, self.y(vmin, vmax, vmin), colors[si]))
            for g in segs:
                out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (" ".join(g), colors[si], width))
            lastv = next((s[i] for i in range(self.n - 1, -1, -1) if s[i] is not None), None)
            lasti = next((i for i in range(self.n - 1, -1, -1) if s[i] is not None), None)
            if lastv is not None:
                out.append('<circle cx="%.1f" cy="%.1f" r="4.2" fill="var(--surf)" stroke="%s" stroke-width="2.4"/>'
                           % (self.x(lasti), self.y(lastv, vmax, vmin), colors[si]))
                ends.append([self.y(lastv, vmax, vmin), labels[si], (fmt or f1)(lastv), si])
        ends.sort()
        for k in range(1, len(ends)):
            if ends[k][0] - ends[k - 1][0] < 14:
                ends[k][0] = ends[k - 1][0] + 14
        # keep the stack inside the plot: push the whole run back up if it spilled below
        floor = self.pt + self.ph - 2
        if ends and ends[-1][0] > floor:
            shift = ends[-1][0] - floor
            for e in ends:
                e[0] -= shift
        for yv, l, v, si in ends:
            out.append('<text x="%.1f" y="%.1f" class="dlab">%s <tspan class="dnum">%s</tspan></text>'
                       % (PAD_L + PW + 9, yv + 4, esc(l), esc(v)))
        return "".join(out)


def legend(colors, labels, notes=None):
    o = ['<div class="lg">']
    for i, l in enumerate(labels):
        n = ('<span class="lgn">%s</span>' % esc(notes[i])) if notes and notes[i] else ""
        o.append('<span><i style="background:%s"></i>%s%s</span>' % (colors[i], esc(l), n))
    o.append("</div>")
    return "".join(o)


def table(headers, rows, cls="", cap=""):
    o = ['<details class="tv"><summary>Table view%s</summary><div class="tw"><table class="%s">' % (cap, cls)]
    o.append("<thead><tr>" + "".join("<th>%s</th>" % esc(h) for h in headers) + "</tr></thead><tbody>")
    for r in rows:
        o.append("<tr>" + "".join(
            ('<td class="%s">%s</td>' % (c[1], c[0])) if isinstance(c, tuple) else ("<td>%s</td>" % c)
            for c in r) + "</tr>")
    o.append("</tbody></table></div></details>")
    return "".join(o)


def nice_max(v, steps=(5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000, 10000)):
    for s in steps:
        if v <= s * 4:
            return s * 4, s
    return v, v / 4


CHARTS = {}
AX = Ax(D)                       # model-share months
AXA = Ax(AD)                     # adoption months
AXS = Ax(SPD)                    # spend months
AXW = Ax(WK, weekly=True)        # token weeks

# ============================================================== chart A: adoption vs Census
CA = ["var(--s1)", "var(--muted)"]
chA = (AXA.yaxis(60, 15) + AXA.lines([ADO, CEN], CA, ["Ramp overall", "Census estimate"], 60, fmt=lambda v: f1(v) + "%", fill_first=True)
       + AXA.annot(AD.index(PN["adoption"]["census_wording_change"]), "Nov-25 \u2014 Census re-words the question")
       + AXA.ticks(3))
CHARTS["adopt"] = {"dates": [lab(d) for d in AD], "unit": "%",
                   "rows": [{"n": "Ramp overall", "c": CA[0], "v": ADO}, {"n": "Census estimate", "c": CA[1], "v": CEN}],
                   "foot": [("%+.2fpp m/m" % PN["adoption"]["overall_mom_pp"][i]) + ((" \u00b7 %+.1fpp y/y" % PN["adoption"]["overall_yoy_pp"][i]) if PN["adoption"]["overall_yoy_pp"][i] is not None else "") for i in range(AN)]}
tA = table(["Month", "Ramp overall %", "m/m pp", "y/y pp", "Census %", "Census question"],
           [[lab(AD[i]), (f2(ADO[i]), "r"), (f2(PN["adoption"]["overall_mom_pp"][i]), "r"), (f2(PN["adoption"]["overall_yoy_pp"][i]), "r"),
             (f2(CEN[i]), "r"), esc((PN["adoption"]["census_question_version"][i] or "").replace("_", " "))] for i in range(AN)], "num")

# ============================================================== chart B: vendor adoption
CV = {"Anthropic": "var(--s1)", "OpenAI": "var(--s2)", "xAI": "var(--s3)", "DeepSeek": "var(--s4)", "Mistral AI": "var(--s5)"}
vmax_v = nice_max(max(max(v for v in VEN[k] if v is not None) for k in VEN))[0]
chB = (AXA.yaxis(vmax_v, vmax_v / 4) + AXA.lines([VEN[k] for k in VEN_ORDER], [CV.get(k, "var(--muted)") for k in VEN_ORDER], VEN_ORDER, vmax_v, fmt=lambda v: f1(v) + "%")
       + (AXA.annot(AD.index(CROSS), "%s \u2014 Anthropic passes OpenAI" % lab(CROSS)) if CROSS else "")
       + AXA.ticks(3))
CHARTS["vendor"] = {"dates": [lab(d) for d in AD], "unit": "%",
                    "rows": [{"n": k, "c": CV.get(k, "var(--muted)"), "v": VEN[k]} for k in VEN_ORDER], "foot": None}
tB = table(["Month"] + ["%s %%" % k for k in VEN_ORDER],
           [[lab(AD[i])] + [(f2(VEN[k][i]), "r") for k in VEN_ORDER] for i in range(AN)], "num",
           cap=" \u2014 share of US businesses with a payment to the vendor (firms can count for several)")


def yoy(series, i=-1):
    if len(series) < 13:
        return None
    a, b = series[i - 12], series[i]
    return None if (a is None or b is None) else b - a


# size + sector latest table (no chart: the ranking is the content)
seg_rows = []
for k in ["Small businesses", "Medium-sized businesses", "Large businesses"]:
    if k in SIZE:
        seg_rows.append([("Size", "k"), esc(k), (f1(SIZE[k][-1]) + "%", "r hl"), ("%+.1f" % yoy(SIZE[k]) if yoy(SIZE[k]) is not None else "\u2014", "r"),
                         (f1(SIZE[k][AD.index(D[0])]) + "%", "r")])
for k in sorted(SECT, key=lambda s: -(SECT[s][-1] or 0)):
    seg_rows.append([("Sector", "k"), esc(k), (f1(SECT[k][-1]) + "%", "r hl"), ("%+.1f" % yoy(SECT[k]) if yoy(SECT[k]) is not None else "\u2014", "r"),
                     (f1(SECT[k][AD.index(D[0])]) + "%", "r")])
tSeg = ('<div class="tw tw-open"><table class="num"><thead><tr><th>Cut</th><th>Segment</th><th class="r">%s</th><th class="r">y/y pp</th><th class="r">%s</th></tr></thead><tbody>%s</tbody></table></div>'
        % (LAT_A, lab(D[0]), "".join("<tr>" + "".join(('<td class="%s">%s</td>' % (c[1], c[0])) if isinstance(c, tuple) else "<td>%s</td>" % c for c in r) + "</tr>" for r in seg_rows)))
states = PN["adoption"]["state_latest"]
tState = table(["State", "Adoption %", "Firms on panel"], [[esc(s["state"]), (f1(s["pct"]), "r"), (format(s["n_firms"], ","), "r")] for s in states], "num",
               cap=" \u2014 by state, %s (small-state denominators are thin)" % LAT_A)

# ============================================================== chart C: AI share of business spend
SSD = SS["dates"]
AXSS = Ax(SSD)
sv = SS["overall_pct"]
vmax_s = nice_max(max(sv), steps=(0.5, 1, 2, 2.5, 5))[0]
chC = AXSS.yaxis(vmax_s, vmax_s / 4, fmt="%g%%") + AXSS.lines([sv], ["var(--s1)"], ["AI share of spend"], vmax_s, fmt=lambda v: f2(v) + "%", fill_first=True) + AXSS.ticks(3)
CHARTS["sshare"] = {"dates": [lab(d) for d in SSD], "unit": "%", "rows": [{"n": "AI share of total payment volume", "c": "var(--s1)", "v": sv}], "foot": None}
sec_latest = sorted(((k, v[-1], yoy(v)) for k, v in SS["sector_pct"].items() if v[-1] is not None and k != "Unknown"), key=lambda t: -t[1])
tC = table(["Sector", "AI share of spend %, " + lab(SSD[-1]), "y/y pp", lab(D[0]) + " %"],
           [[esc(k), (f2(v), "r hl"), ("%+.2f" % y if y is not None else "\u2014", "r"), (f2(SS["sector_pct"][k][SSD.index(D[0])]), "r")] for k, v, y in sec_latest], "num",
           cap=" \u2014 all %d NAICS sectors" % len(sec_latest))

# ============================================================== chart 1: provider mix
C1 = ["var(--s1)", "var(--s2)", "var(--s3)"]
L1 = ["Anthropic", "OpenAI", "Other"]
S1 = [PROV["Anthropic"], PROV["OpenAI"], OTHER]
a_lo_i = min(range(N), key=lambda i: PROV["Anthropic"][i])
a_hi_i = max(range(N), key=lambda i: PROV["Anthropic"][i])
ch1 = (AX.yaxis(100, 25) + AX.stack(S1, C1, L1)
       + AX.annot(a_lo_i, "%s low %s%%" % (lab(D[a_lo_i]), f1(PROV["Anthropic"][a_lo_i])))
       + AX.annot(a_hi_i, "%s high %s%%" % (lab(D[a_hi_i]), f1(PROV["Anthropic"][a_hi_i])))
       + AX.ticks(2))
t1 = table(["Month", "Anthropic %", "OpenAI %", "xAI %", "Cursor %", "Models on panel", "Top model", "Top model %"],
           [[lab(D[i]), (f1(PROV["Anthropic"][i]), "r"), (f1(PROV["OpenAI"][i]), "r"),
             ("%.2f" % PROV["xAI"][i], "r"), ("%.2f" % PROV["Cursor"][i], "r"),
             (str(CONC[i]["n_models"]), "r"), CONC[i]["top1"], (f1(CONC[i]["top1_share"]), "r")]
            for i in range(N)], "num")
CHARTS["prov"] = {"dates": [lab(d) for d in D], "unit": "%",
                  "rows": [{"n": "Anthropic", "c": "var(--s1)", "v": PROV["Anthropic"]},
                           {"n": "OpenAI", "c": "var(--s2)", "v": PROV["OpenAI"]},
                           {"n": "Other (xAI, Cursor)", "c": "var(--s3)", "v": OTHER}],
                  "foot": [CONC[i]["top1"] + " leads at " + f1(CONC[i]["top1_share"]) + "%" for i in range(N)]}
# the latest month's debuts and the biggest mover
debuts = sorted((m for m in MODELS if m["first_i"] == N - 1), key=lambda m: -m["latest"])
oa_run = 0
for i in range(N - 1, 0, -1):
    if PROV["OpenAI"][i] > PROV["OpenAI"][i - 1]:
        oa_run += 1
    else:
        break
anth_streak = sum(1 for i in range(N) if PROV["Anthropic"][i] > PROV["OpenAI"][i])

# ==================================================== chart 2: Anthropic ladder (ordinal)
LADC = ["var(--o1)", "var(--o2)", "var(--o3)", "var(--o4)"]
LADL = ["Haiku", "Sonnet", "Opus", "Fable"]
S2 = [LAD[f] for f in LADL]
ch2 = (AX.yaxis(100, 25) + AX.stack(S2, LADC, LADL)
       + AX.annot(FLIP, "%s \u2014 Opus takes the mix" % lab(FLIP_M))
       + AX.ticks(2))
t2 = table(["Month", "Haiku", "Sonnet", "Opus", "Fable", "Anthropic total", "Opus+Fable, % of Anthropic"],
           [[lab(D[i])] + [(f1(LAD[f][i]), "r") for f in LADL]
            + [(f1(PROV["Anthropic"][i]), "r"), (f1(FRONT[i]), "r hl")] for i in range(N)], "num",
           cap=" \u2014 ladder as % of all named models")
CHARTS["lad"] = {"dates": [lab(d) for d in D], "unit": "%",
                 "rows": [{"n": f, "c": LADC[k], "v": LAD[f]} for k, f in enumerate(LADL)],
                 "foot": ["Opus+Fable = " + f1(FRONT[i]) + "% of Anthropic's own mix" for i in range(N)]}

# ============================================================== chart 3: vintage turnover
VC = ["var(--o2)", "var(--o3)", "var(--o4)"]
VL = ["\u22643 months old", "4\u201312 months", ">12 months"]
S3 = [VINT["le3"], VINT["m4_12"], VINT["gt12"]]
cens = D.index(MS["vintage_censored_through"])
ch3 = (AX.yaxis(100, 25) + AX.stack(S3, VC, VL)
       + ('<rect x="%d" y="%d" width="%.1f" height="%d" class="cens"/>'
          '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>'
          '<text x="%.1f" y="%d" class="censt">\u2190 left-censored: model age understated</text>'
          % (PAD_L, PAD_T, AX.x(cens) - PAD_L, PH, AX.x(cens), PAD_T, AX.x(cens), PAD_T + PH,
             (PAD_L + AX.x(cens)) / 2, PAD_T - 8))
       + AX.ticks(2))
t3 = table(["Month", "\u22643m old %", "4\u201312m %", ">12m %", "Models on panel", "HHI (0\u2013100)", "Top-3 %"],
           [[lab(D[i]), (f1(VINT["le3"][i]), "r"), (f1(VINT["m4_12"][i]), "r"),
             (f1(VINT["gt12"][i]) + ("*" if i <= cens else ""), "r"),
             (str(CONC[i]["n_models"]), "r"), ("%.1f" % CONC[i]["hhi"], "r"),
             (f1(CONC[i]["top3_share"]), "r")] for i in range(N)], "num",
           cap=" \u2014 * = censored, model age understated")
CHARTS["vint"] = {"dates": [lab(d) for d in D], "unit": "%",
                  "rows": [{"n": VL[k], "c": VC[k], "v": S3[k]} for k in range(3)],
                  "foot": [("%d models on panel \u00b7 HHI %.1f" % (CONC[i]["n_models"], CONC[i]["hhi"]))
                           + ("  \u2014 age censored" if i <= cens else "") for i in range(N)]}
y26 = D.index("2026-01") if "2026-01" in D else max(0, N - 9)

# ================================================================= chart 4: launch curves
LAUNCH = [m for m in MODELS if not m["censored"] and m["peak"] >= 4.0]
LAUNCH.sort(key=lambda m: m["first_i"])
MAXAGE = max(len(m["series"]) - m["first_i"] for m in LAUNCH)
SW, SH = 214, 132
SPL, SPR, SPT, SPB = 30, 8, 14, 22
SPW, SPPH = SW - SPL - SPR, SH - SPT - SPB
SMAX = float(int(max(m["peak"] for m in LAUNCH) / 10.0) * 10 + 10)
SGRID = [g for g in range(0, int(SMAX) + 1, 20)]


def sparkpanel(m):
    ser = m["series"][m["first_i"]:]
    ages = len(ser)
    px = lambda a: SPL + SPW * a / float(max(1, MAXAGE - 1))
    py = lambda v: SPT + SPPH * (1 - v / SMAX)
    pts = " ".join("%.1f,%.1f" % (px(a), py(ser[a])) for a in range(ages))
    col = "var(--s2)" if m["provider"] == "OpenAI" else ("var(--s1)" if m["provider"] == "Anthropic" else "var(--s3)")
    area = ('<polygon points="%s %.1f,%.1f %.1f,%.1f" fill="%s" fill-opacity=".16"/>'
            % (pts, px(ages - 1), py(0), px(0), py(0), col))
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s share by months since debut" class="sm">' % (SW, SH, esc(m["model"]))]
    for gv in SGRID:
        o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="grid"/>' % (SPL, py(gv), SPL + SPW, py(gv)))
        o.append('<text x="%d" y="%.1f" class="ax end sm-ax">%d</text>' % (SPL - 5, py(gv) + 3, gv))
    o.append(area)
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts, col))
    pk = m["months_to_peak"]
    o.append('<circle cx="%.1f" cy="%.1f" r="4.2" fill="var(--surf)" stroke="%s" stroke-width="2"/>' % (px(pk), py(m["peak"]), col))
    o.append('<text x="%.1f" y="%.1f" class="smpk" text-anchor="%s">%s%%</text>'
             % (px(pk) + (6 if pk < MAXAGE * .6 else -6), py(m["peak"]) - 6, "start" if pk < MAXAGE * .6 else "end", f1(m["peak"])))
    for a in (0, 6, 12, 18):
        if a <= MAXAGE - 1:
            o.append('<text x="%.1f" y="%d" class="ax mid sm-ax">%d</text>' % (px(a), SH - 7, a))
    o.append("</svg>")
    return ('<figure class="smf"><figcaption><b>%s</b><span>%s \u00b7 debut %s</span></figcaption>%s</figure>'
            % (esc(m["model"]), esc(m["provider"]), lab(m["first"]), "".join(o)))


t4 = table(["Model", "Provider", "Debut", "Debut share %", "Peak %", "Peak month", "Months to peak", "%s %%" % LATEST],
           [[esc(m["model"]), esc(m["provider"]), lab(m["first"]), (f1(m["debut_share"]), "r"),
             (f1(m["peak"]), "r hl"), lab(m["peak_month"]), (str(m["months_to_peak"]), "r"), (f1(m["latest"]), "r")]
            for m in sorted(MODELS, key=lambda x: -x["peak"]) if m["peak"] >= 0.5], "num",
           cap=" \u2014 every model peaking \u22650.5%")
big_deb = max((m for m in MODELS if not m["censored"]), key=lambda m: m["debut_share"])
oa_debs = sorted((m for m in MODELS if m["provider"] == "OpenAI" and not m["censored"]), key=lambda m: -m["debut_share"])[:2]

# ==================================================== chart 5: the cross-read (three panels)
CH, CPT, CPB = 196, 22, 26
AXC = Ax(D, h=CH, pt=CPT, pb=CPB)


def crosspanel(vals, vmax, color, ylabel, cid, step, fmt="%g%%", fill=True, tag=None, vfmt=None):
    o = [AXC.yaxis(vmax, step, fmt=fmt)]
    o.append(AXC.lines([vals], [color], [ylabel], vmax, fmt=vfmt or (lambda v: f1(v)), fill_first=fill))
    o.append(AXC.annot(FLIP, tag) if tag else '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="annl"/>' % (AXC.x(FLIP), CPT, AXC.x(FLIP), CPT + CPH_))
    o.append(AXC.ticks(2))
    return AXC.svg(cid, "".join(o), ylabel)


CPH_ = CH - CPT - CPB
ch5 = crosspanel(FRONT, 100, "var(--s1)", "Opus+Fable, % of Anthropic", "front", 25, tag="%s \u2014 the ladder flip" % lab(FLIP_M), vfmt=lambda v: f1(v) + "%")
sp_max = nice_max(max(SP_WIN), steps=(2, 3, 4, 5, 10))[0]
ch6 = crosspanel(SP_WIN, sp_max, "var(--s2)", "median $/employee", "spend", sp_max / 4, fmt="$%g", vfmt=lambda v: money(v))
# tokens on the same month axis (complete months only; None before the TSM sample starts)
ANT_M = [None] * N
ANT_P = [None] * N
for i, m in enumerate(MM):
    if m in D:
        ANT_M[D.index(m)] = MV["anthropic"][i] / 1e12
        ANT_P[D.index(m)] = MBLEND_ANT[i]
tk_max = nice_max(max(v for v in ANT_M if v is not None), steps=(1, 2, 5, 10, 20, 50, 100, 200, 500))[0]
ch6b = crosspanel(ANT_M, tk_max, "var(--s3)", "Anthropic tokens, tn / month", "tok", tk_max / 4, fmt="%g", vfmt=lambda v: "%.1f tn" % v)
CHARTS["front"] = {"dates": [lab(d) for d in D], "unit": "%", "rows": [{"n": "Opus+Fable, % of Anthropic", "c": "var(--s1)", "v": FRONT}], "foot": None}
CHARTS["spend"] = {"dates": [lab(d) for d in D], "unit": "$", "pre": True, "rows": [{"n": "Median AI spend / employee", "c": "var(--s2)", "v": SP_WIN}], "foot": None}
CHARTS["tok"] = {"dates": [lab(d) for d in D], "unit": " tn", "rows": [{"n": "Anthropic tokens (TSM sample)", "c": "var(--s3)", "v": ANT_M}],
                 "foot": [("blended $%.2f / M tokens" % ANT_P[i]) if ANT_P[i] else "before the token sample" for i in range(N)]}
t5 = table(["Month", "Opus+Fable, % of Anthropic", "Median AI spend / employee", "3-mo compound, %/mo", "Anthropic tokens, tn (TSM)", "Anthropic blended $/M (TSM)"],
           [[lab(D[i]), (f1(FRONT[i]), "r"), (money(SP_WIN[i]), "r"),
             ("%+.2f" % SPMOM_WIN[i] if SPMOM_WIN[i] is not None else "\u2014", "r"),
             (f2(ANT_M[i]), "r"), (money(ANT_P[i]), "r")] for i in range(N)], "num")

# ============================================================ chart 7: spend, 3 cohorts
COH = [("median", "All companies", "var(--s1)"), ("top10", "Top 10%", "var(--s2)"), ("top1", "Top 1%", "var(--s3)")]
FN = len(SPD)
AXI = Ax(SPD, h=330, pt=18, pb=34)
IDX = dict((k, [SP["cohorts"][k]["level"][i] / SP["cohorts"][k]["level"][0] * 100 for i in range(FN)]) for k, _, _ in COH)
IMAX = float(int(max(max(IDX[k]) for k in IDX) / 100) * 100 + 100)
ch7 = (AXI.yaxis(IMAX, 200, fmt="%g")
       + AXI.lines([IDX[k] for k, _, _ in COH], [c for _, _, c in COH], [n for _, n, _ in COH], IMAX, fmt=lambda v: "%d" % round(v))
       + AXI.annot(SPD.index(D[0]), "model-mix panel starts", dy=20)
       + AXI.ticks(3))
ch7 = AXI.svg("idx", ch7, "Ramp AI spend per employee, three cohorts, indexed")
t7 = table(["Month", "All companies $", "Top 10% $", "Top 1% $", "p90 company $", "p99 company $", "Spend-weighted (winsorised) $", "All, index", "Top 10%, index", "Top 1%, index"],
           [[lab(SPD[i])]
            + [(money(SP["cohorts"][k]["level"][i]), "r") for k, _, _ in COH]
            + [(money(SX["p90"][i]), "r"), (money(SX["p99"][i]), "r"), (money(SX["winsorized_weighted"][i]), "r")]
            + [(str(int(round(IDX[k][i]))), "r") for k, _, _ in COH] for i in range(FN)], "num",
           cap=" \u2014 %s = 100" % lab(SPD[0]))
CHARTS["idx"] = {"dates": [lab(d) for d in SPD], "unit": "$", "pre": True,
                 "rows": [{"n": n, "c": c, "v": SP["cohorts"][k]["level"]} for k, n, c in COH], "foot": None}

# restatement table (latest common month, per cohort)
rs_sp = (RS.get("spend_per_employee") or [None])[-1]
rs_ms = (RS.get("model_share") or [None])[-1]
rs_rows = []
if rs_sp:
    for r in rs_sp["rows"]:
        rs_rows.append([lab(r["month"])] + sum(([(money(r[s]["old"]), "r"), (money(r[s]["new"]), "r"),
                                                 ("%+.1f%%" % r[s]["pct"] if r[s]["pct"] is not None else "dropped", "r hl")] for _, s, _ in [(0, "median", 0), (0, "top10", 0), (0, "top1", 0)]), []))
tRS = table(["Month", "Median, old", "Median, new", "rev.", "Top 10%, old", "new", "rev.", "Top 1%, old", "new", "rev."], rs_rows, "num",
            cap=" \u2014 %s vs the live series" % (rs_sp["vintage"] if rs_sp else "")) if rs_rows else ""

# ============================================================ chart 8: spend by segment
FTE = SC.get("fte_segment", {})
FIN = SC.get("company_financing_status", {})
SEG_C = ["var(--o2)", "var(--o3)", "var(--o4)"]
fte_labels = [l for l in FTE.get("labels", []) if l in FTE.get("median", {})]
seg_max = nice_max(max(max(v for v in FTE["median"][l] if v is not None) for l in fte_labels), steps=(5, 10, 20, 25, 50))[0] if fte_labels else 20
ch8 = (AXS.yaxis(seg_max, seg_max / 4, fmt="$%g")
       + AXS.lines([FTE["median"][l] for l in fte_labels], SEG_C[:len(fte_labels)], fte_labels, seg_max, fmt=lambda v: money(v))
       + AXS.ticks(3))
ch8 = AXS.svg("fte", ch8, "Median AI spend per employee by company size")
CHARTS["fte"] = {"dates": [lab(d) for d in SPD], "unit": "$", "pre": True,
                 "rows": [{"n": l, "c": SEG_C[k], "v": FTE["median"][l]} for k, l in enumerate(fte_labels)], "foot": None}
seg_tab = []
for dim, title in (("fte_segment", "Company size"), ("company_financing_status", "Financing"), ("naics_sector", "Sector"), ("business_office_state", "State")):
    if dim not in SC:
        continue
    for l in SC[dim]["labels"]:
        med = SC[dim]["median"].get(l)
        wt = SC[dim]["weighted"].get(l)
        if not med:
            continue
        seg_tab.append([(title, "k"), esc(l), (money(med[-1]), "r hl"), ("%+.0f%%" % pct_change(med[-13], med[-1]) if pct_change(med[-13], med[-1]) is not None else "\u2014", "r"),
                        (money(wt[-1]) if wt else "\u2014", "r"), (money(med[SPD.index(D[0])]), "r")])
t8 = table(["Cut", "Segment", "Median $/employee, " + lab(SPD[-1]), "y/y", "Spend-weighted $ (winsorised)", lab(D[0])], seg_tab, "num",
           cap=" \u2014 every curated segment Ramp publishes")

# ============================================================ chart 9: model share by segment
seg_share_rows = []
for dim, title in (("fte_segment", "Company size"), ("company_financing_status", "Financing"), ("naics_sector", "Sector")):
    if dim not in MSC["dims"]:
        continue
    dd = MSC["dims"][dim]
    for l in dd["labels"]:
        a = dd["provider_pct"].get("%s|Anthropic" % l)
        o = dd["provider_pct"].get("%s|OpenAI" % l)
        if not a:
            continue
        seg_share_rows.append([(title, "k"), esc(l), (f1(a[-1]), "r hl"), (f1(o[-1]) if o else "\u2014", "r"),
                               (f1(a[MSC["dates"].index(FLIP_M) - 1]) if FLIP_M in MSC["dates"] else "\u2014", "r"), (f1(a[0]), "r")])
t9 = ('<div class="tw tw-open"><table class="num"><thead><tr><th>Cut</th><th>Segment</th><th class="r">Anthropic %%, %s</th><th class="r">OpenAI %%</th><th class="r">Anthropic %%, %s</th><th class="r">Anthropic %%, %s</th></tr></thead><tbody>%s</tbody></table></div>'
      % (lab(MSC["dates"][-1]), lab(D[FLIP - 1]), lab(MSC["dates"][0]),
         "".join("<tr>" + "".join(('<td class="%s">%s</td>' % (c[1], c[0])) if isinstance(c, tuple) else "<td>%s</td>" % c for c in r) + "</tr>" for r in seg_share_rows)))

# ============================================================ chart 10: tokens
TKC = ["var(--s1)", "var(--s2)", "var(--s4)", "var(--s3)", "var(--base)"]
TKL = ["Anthropic", "OpenAI", "Google", "xAI", "Other"]
S10 = [VSHARE[m] for m in TOP_MAKERS] + [VSHARE["other"]]
ch10 = AXW.yaxis(100, 25) + AXW.stack(S10, TKC, TKL) + AXW.ticks(13)
ch10 = AXW.svg("tokshare", ch10, "Share of weekly token volume by model maker")
CHARTS["tokshare"] = {"dates": [labw(w) for w in WK], "unit": "%",
                      "rows": [{"n": TKL[k], "c": TKC[k], "v": [round(v, 2) for v in S10[k]]} for k in range(5)],
                      "foot": ["%.1f tn tokens \u00b7 $%s spend" % (WTOT[i] / 1e12, format(WSTOT[i], ",.0f")) for i in range(WN)]}
other_latest = sorted(((m, VOL[m][-1]) for m in VOL if m not in TOP_MAKERS), key=lambda t: -t[1])
t10 = table(["Week ending", "Total tokens, tn", "Total spend $", "Anthropic %", "OpenAI %", "Google %", "xAI %", "Other %", "Blended $/M, all", "Anthropic $/M", "OpenAI $/M"],
            [[labw(WK[i]), ("%.2f" % (WTOT[i] / 1e12), "r"), (format(WSTOT[i], ",.0f"), "r")]
             + [(f1(VSHARE[m][i]), "r") for m in TOP_MAKERS] + [(f1(VSHARE["other"][i]), "r"),
                (f2(BLEND["all"][i]), "r"), (f2(BLEND["anthropic"][i]), "r"), (f2(BLEND["openai"][i]), "r")] for i in range(WN)], "num",
            cap=" \u2014 weekly, Token Spend Management sample")

# weekly spend by maker (levels, $)
ws_max = nice_max(max(WSTOT) / 1e6, steps=(0.5, 1, 2, 5, 10, 20, 50, 100))[0]
S11 = [[SPND[m][i] / 1e6 for i in range(WN)] for m in TOP_MAKERS] + [[max(0.0, WSTOT[i] - sum(SPND[m][i] for m in TOP_MAKERS)) / 1e6 for i in range(WN)]]
ch11 = AXW.yaxis(ws_max, ws_max / 4, fmt="$%gM") + AXW.stack(S11, TKC, TKL, vmax=ws_max, suffix="M") + AXW.ticks(13)
ch11 = AXW.svg("tokspend", ch11, "Weekly token spend by model maker, $M")
CHARTS["tokspend"] = {"dates": [labw(w) for w in WK], "unit": "M", "pre": False,
                      "rows": [{"n": TKL[k], "c": TKC[k], "v": [round(v, 3) for v in S11[k]]} for k in range(5)],
                      "foot": ["$%s total" % format(WSTOT[i], ",.0f") for i in range(WN)]}

# prices: blended $/M from Ramp's own tokenPrices (all / output / uncached input), Anthropic vs OpenAI
PD = TK["price_dates"]
AXP = Ax(PD, weekly=True)
PR = TK["price_usd_per_m"]
pr_series = [("anthropic|all_tokens", "Anthropic, all tokens", "var(--s1)"), ("anthropic|output", "Anthropic, output", "var(--o3)"),
             ("anthropic|uncached_input", "Anthropic, uncached input", "var(--o1)"),
             ("openai|all_tokens", "OpenAI, all tokens", "var(--s2)"), ("openai|output", "OpenAI, output", "var(--flag)"),
             ("openai|uncached_input", "OpenAI, uncached input", "var(--s5)")]
pr_series = [t for t in pr_series if t[0] in PR]
pr_max = nice_max(max(max(v for v in PR[k] if v is not None) for k, _, _ in pr_series), steps=(1, 2, 5, 10, 20, 25, 50))[0]
ch12 = AXP.yaxis(pr_max, pr_max / 4, fmt="$%g") + AXP.lines([PR[k] for k, _, _ in pr_series], [c for _, _, c in pr_series], [l for _, l, _ in pr_series], pr_max, fmt=lambda v: money(v)) + AXP.ticks(13)
ch12 = AXP.svg("price", ch12, "Blended price per million tokens, Anthropic vs OpenAI, by token type")
CHARTS["price"] = {"dates": [labw(d) for d in PD], "unit": "$", "pre": True,
                   "rows": [{"n": l, "c": c, "v": PR[k]} for k, l, c in pr_series], "foot": None}
t12 = table(["Week ending"] + [l + " $/M" for _, l, _ in pr_series],
            [[labw(PD[i])] + [(f2(PR[k][i]), "r") for k, _, _ in pr_series] for i in range(len(PD))], "num",
            cap=" \u2014 trailing-7-day cost / tokens, sampled weekly")


def first_val(s):
    return next((v for v in s if v is not None), None)


def last_val(s):
    return next((v for v in reversed(s) if v is not None), None)


# ============================================================================ stat tiles
def tile(v, l, s, tone=""):
    return ('<div class="tile %s"><div class="tv2">%s</div><div class="tl">%s</div><div class="ts">%s</div></div>'
            % (tone, v, esc(l), esc(s)))


ven_a, ven_o = VEN["Anthropic"][-1], VEN["OpenAI"][-1]
TILES = "".join([
    tile(f1(ADO[-1]) + "%", "US businesses paying for AI",
         "%s \u00b7 %+.1fpp y/y \u00b7 Census survey says %s%%" % (LAT_A, PN["adoption"]["overall_yoy_pp"][-1], f1(CEN[-1]))),
    tile("%s%% vs %s%%" % (f1(ven_a), f1(ven_o)), "Anthropic vs OpenAI, share of businesses",
         "%s \u00b7 Anthropic ahead since %s \u00b7 firms can count for both" % (LAT_A, lab(CROSS) if CROSS else "n/a")),
    tile(f1(PROV["Anthropic"][-1]) + "%", "Anthropic, share of named-model usage",
         "%s \u00b7 %+.1fpp vs %s \u00b7 OpenAI %s%%" % (LATEST, PROV["Anthropic"][-1] - PROV["Anthropic"][-2], PREV, f1(PROV["OpenAI"][-1]))),
    tile(f1(FRONT[-1]) + "%", "Anthropic mix that is Opus or Fable",
         "was %s%% in %s, the month before the flip" % (f1(FRONT[FLIP - 1]), lab(D[FLIP - 1]))),
    tile(money(SPMED[-1]), "median monthly AI spend / employee",
         "%s \u00b7 %+.0f%% y/y \u00b7 top 1%% at %s \u00b7 RESTATED series" % (lab(SPD[-1]), SP["cohorts"]["median"]["yoy_pct"][-1], money(SP["cohorts"]["top1"]["level"][-1], 0))),
    tile(f1(VSHARE["anthropic"][-1]) + "%", "Anthropic share of tokens (TSM sample)",
         "week to %s \u00b7 OpenAI %s%% \u00b7 Google %s%%" % (labw(WK[-1]), f1(VSHARE["openai"][-1]), f1(VSHARE["google"][-1]))),
])

# ============================================================================== the page
CSS = """
:root{color-scheme:light;--plane:#f9f9f7;--surf:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
 --grid:#e1e0d9;--base:#c3c2b7;--border:rgba(11,11,11,.10);
 --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#8e5bd6;--s5:#b8860b;
 --o1:#86b6ef;--o2:#3987e5;--o3:#1c5cab;--o4:#0d366b;
 --good:#0ca30c;--warn:#fab219;--crit:#d03b3b;--flag:#ec835a;
 --headbg:#0f1729;--headsub:#8492ad;--link:#7fb0ff;--wash:rgba(42,120,214,.06)}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])){color-scheme:dark;
 --plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--base:#383835;
 --border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#a37ee3;--s5:#d4a52a;
 --o1:#cde2fb;--o2:#86b6ef;--o3:#3987e5;--o4:#184f95;--headbg:#000;--wash:rgba(57,135,229,.10)}}
:root[data-theme="dark"]{color-scheme:dark;--plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;
 --muted:#898781;--grid:#2c2c2a;--base:#383835;--border:rgba(255,255,255,.10);
 --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#a37ee3;--s5:#d4a52a;--o1:#cde2fb;--o2:#86b6ef;--o3:#3987e5;--o4:#184f95;
 --headbg:#000;--wash:rgba(57,135,229,.10)}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);
 font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--headbg);color:#fff;padding:26px 30px 22px}
header h1{margin:0 0 6px;font-size:23px;letter-spacing:-.2px}
header p{margin:0;color:var(--headsub);max-width:104ch;font-size:13.5px}
header a{color:var(--link)}
header code{color:#c9d4ea}
nav.toc{background:var(--surf);border-bottom:1px solid var(--border);padding:8px 30px;font-size:12.5px;display:flex;flex-wrap:wrap;gap:4px 18px}
nav.toc a{color:var(--ink2);text-decoration:none}
nav.toc a:hover{color:var(--ink)}
main{padding:22px 30px 60px;max-width:1180px;margin:0 auto}
section{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin:0 0 18px;scroll-margin-top:12px}
h2{margin:0 0 3px;font-size:16.5px;letter-spacing:-.1px}
h2 .k{color:var(--muted);font-weight:400;font-size:12.5px;margin-left:8px;letter-spacing:0}
h3{margin:18px 0 4px;font-size:14px}
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
.tw-open{max-height:none;margin-top:4px}
table{border-collapse:collapse;width:100%;font-size:12px}
th,td{padding:5px 10px;border-bottom:1px solid var(--border);text-align:left;white-space:nowrap}
th{position:sticky;top:0;background:var(--surf);color:var(--ink2);font-weight:600;z-index:1}
td.r,th.r{text-align:right;font-variant-numeric:tabular-nums}
td.hl{font-weight:650}
td.k{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.04em}
tbody tr:hover{background:var(--wash)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.note{border-left:3px solid var(--flag);background:var(--wash);border-radius:0 8px 8px 0;padding:11px 14px;margin:14px 0 0;font-size:12.8px;color:var(--ink2)}
.note b{color:var(--ink)}
.note.warnn{border-left-color:var(--crit)}
.note.goodn{border-left-color:var(--good)}
ul.cav{margin:10px 0 0;padding-left:19px;font-size:12.8px;color:var(--ink2)}
ul.cav li{margin-bottom:7px}
ul.cav b{color:var(--ink)}
.dec{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0 0}
.dec div{border:1px solid var(--border);border-radius:9px;padding:9px 12px}
.dec b{display:block;font-size:19px;letter-spacing:-.4px}
.dec span{font-size:11.5px;color:var(--muted)}
#tt{position:fixed;pointer-events:none;z-index:60;background:var(--surf);border:1px solid var(--border);
 border-radius:9px;padding:9px 11px;font-size:12px;box-shadow:0 8px 26px rgba(0,0,0,.20);display:none;min-width:186px}
#tt .h{font-weight:650;margin-bottom:6px;color:var(--ink)}
#tt .rw{display:flex;align-items:center;gap:8px;justify-content:space-between;margin:2px 0;color:var(--ink2)}
#tt .rw i{width:9px;height:9px;border-radius:2px;display:inline-block;flex:0 0 auto}
#tt .rw b{color:var(--ink);font-variant-numeric:tabular-nums}
#tt .ft{margin-top:6px;padding-top:5px;border-top:1px solid var(--border);color:var(--muted);font-size:11px}
footer{color:var(--muted);font-size:11.5px;padding:0 30px 40px;max-width:1180px;margin:0 auto;line-height:1.6}
@media(max-width:900px){.cols{grid-template-columns:1fr}main,header,footer,nav.toc{padding-left:16px;padding-right:16px}}
"""

JS = """
var CHARTS=%s;
var tt=document.getElementById('tt');
function grp(s){var p=s.split('.');p[0]=p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');return p.join('.');}
function fmt(v,u,pre){if(v==null)return'\\u2014';if(pre)return u+grp(v.toFixed(2));var d=Math.abs(v)<10?2:1;return grp(v.toFixed(d))+u;}
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


def xfmt(x):
    return "\u2014" if x is None else "%.2fx" % x


def build(artifact=False):
    p = []
    if artifact:
        p.append("<title>Ramp AI Index</title><style>%s</style>" % CSS)
    else:
        p.append("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
                 "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                 "<title>Ramp AI Index \u2014 adoption, model mix, spend &amp; tokens</title>"
                 "<style>%s</style></head><body>" % CSS)

    p.append("<header><h1>Ramp AI Index \u2014 who adopts, who gets used, what gets spent, and the tokens behind it</h1>"
             "<p>Every series Ramp publishes on <a href='https://ramp.com/data/ai-index'>ramp.com/data/ai-index</a>, pulled "
             "%s: <b>adoption</b> (%s\u2013%s, overall / vendor / size / sector / state, with the Census survey alongside), "
             "<b>model mix</b> (%s\u2013%s, %d named models), <b>AI spend per employee</b> (%s\u2013%s, restated by Ramp in this vintage), "
             "<b>AI share of business spend</b>, and the <b>Token Spend Management sample</b> (%d weeks of token volume and spend "
             "across %d model series from %d makers, to the week ending %s). "
             "<b>Read the basis notes before quoting any share as market share.</b> Primary data on disk at "
             "<code>_wiki/_data/ramp-ai-index/</code>; rebuild with <code>fetch_ramp_index.py</code> \u2192 "
             "<code>build_ramp_index.py</code> \u2192 <code>build_ramp_dash.py</code>.</p></header>"
             % (esc(META.get("fetched_at", "")), lab(AD[0]), LAT_A, lab(D[0]), LATEST, len(MODELS), lab(SPD[0]), lab(SPD[-1]),
                WN, TK["model_count"], len(MAKERS), labw(WK[-1])))
    p.append('<nav class="toc"><a href="#adoption">A \u00b7 Adoption</a><a href="#vendor">B \u00b7 Vendor penetration</a>'
             '<a href="#sshare">C \u00b7 Share of spend</a><a href="#prov">1 \u00b7 Model mix</a><a href="#ladder">2 \u00b7 Ladder</a>'
             '<a href="#vintage">3 \u00b7 Vintage</a><a href="#launch">4 \u00b7 Launch curves</a><a href="#cross">5 \u00b7 Price vs volume</a>'
             '<a href="#spend">6 \u00b7 Spend series</a><a href="#segments">7 \u00b7 Segments</a><a href="#tokens">8 \u00b7 Tokens</a>'
             '<a href="#basis">9 \u00b7 Basis traps</a></nav>')
    p.append("<main>")
    p.append('<div class="tiles">%s</div>' % TILES)

    # A ---------------------------------------------------------------- adoption
    a12 = ADO[-13] if AN >= 13 else None
    p.append('<section id="adoption"><h2>A \u00b7 Adoption: %s%% of US businesses now pay for AI<span class="k">share of firms with an AI payment in the month, %%</span></h2>'
             '<p class="sub">Ramp sees a paid AI transaction at <b>%s%%</b> of the %s businesses on its platform in %s, up from %s%% a year earlier and %s%% at the start of the series (%s). '
             'The Census Bureau\u2019s survey puts it at <b>%s%%</b> \u2014 the gap is the point of the index: surveys under-count, and the Census re-worded its question in %s '
             '(the step in the grey line is the wording change, not adoption). Momentum has <b>cooled</b>: the last six months added %s pp against %s pp in the prior six.</p>%s%s%s'
             '<h3>By company size and sector, %s</h3>%s%s</section>'
             % (f1(ADO[-1]), f1(ADO[-1]), "70,000+", LAT_A, f1(a12), f1(ADO[0]), lab(AD[0]), f1(CEN[-1]),
                lab(PN["adoption"]["census_wording_change"]), "%.1f" % (ADO[-1] - ADO[-7]), "%.1f" % (ADO[-7] - ADO[-13]),
                AXA.svg("adopt", chA, "Ramp AI adoption vs Census estimate"), legend(CA, ["Ramp overall", "Census Business Trends and Outlook Survey"], [None, "re-worded Nov-25"]), tA,
                LAT_A, tSeg, tState))

    # B ---------------------------------------------------------------- vendor adoption
    p.append('<section id="vendor"><h2>B \u00b7 Vendor penetration: Anthropic %s%% vs OpenAI %s%% of businesses<span class="k">share of firms paying each vendor, %% \u2014 firms count for every vendor they pay</span></h2>'
             '<p class="sub">This is the <b>penetration</b> cut the wiki previously carried only second-hand (ANTHROPIC.md: ~41%% vs ~39.5%% in Jun-26, from the Big Technology podcast). '
             'Primary now: Anthropic passed OpenAI in <b>%s</b> and leads by <b>%s pp</b> in %s. A firm paying both counts for both, so the lines do not sum to anything \u2014 '
             'compare with section 1, where the same two vendors are %s%% vs %s%% of <i>usage</i>. xAI is the only third vendor above 1%% (%s%%); DeepSeek and Mistral are rounding error (%s%% / %s%%).</p>%s%s%s</section>'
             % (f1(ven_a), f1(ven_o), lab(CROSS) if CROSS else "n/a", "%.1f" % (ven_a - ven_o), LAT_A, f1(PROV["Anthropic"][-1]), f1(PROV["OpenAI"][-1]),
                f1(VEN["xAI"][-1]), f2(VEN.get("DeepSeek", [None])[-1]), f2(VEN.get("Mistral AI", [None])[-1]),
                AXA.svg("vendor", chB, "Share of US businesses paying each AI vendor"), legend([CV.get(k, "var(--muted)") for k in VEN_ORDER], VEN_ORDER), tB))

    # C ---------------------------------------------------------------- share of spend
    p.append('<section id="sshare"><h2>C \u00b7 AI is %s%% of business spend on Ramp<span class="k">AI spend / total payment volume, %%</span></h2>'
             '<p class="sub">From %s%% in %s to <b>%s%%</b> in %s \u2014 a %sx rise in share of wallet. This is the one Ramp series that is <i>not</i> a ratio to headcount or a count of firms: '
             'it is AI dollars over all dollars, so it moves with both AI spend and everything else businesses pay for. The sector table is the dispersion: '
             '<b>%s</b> leads at %s%%, <b>%s</b> trails at %s%%.</p>%s%s</section>'
             % (f2(sv[-1]), f2(sv[0]), lab(SSD[0]), f2(sv[-1]), lab(SSD[-1]), "%.1f" % (sv[-1] / sv[0]),
                esc(sec_latest[0][0]), f2(sec_latest[0][1]), esc(sec_latest[-1][0]), f2(sec_latest[-1][1]),
                AXSS.svg("sshare", chC, "AI share of total payment volume"), tC))

    # 1 ---------------------------------------------------------------- provider mix
    deb_txt = (" The month\u2019s debuts: %s." % ", ".join("%s (%s%%)" % (esc(m["model"]), f1(m["latest"])) for m in debuts[:3])) if debuts else " No new model debuted this month."
    lo_txt = ("Anthropic\u2019s low was %s (%s%% vs OpenAI %s%%%s); its high %s (%s%%)."
              % (lab(D[a_lo_i]), f1(PROV["Anthropic"][a_lo_i]), f1(PROV["OpenAI"][a_lo_i]),
                 ", the one month it trailed" if PROV["Anthropic"][a_lo_i] < PROV["OpenAI"][a_lo_i] else "", lab(D[a_hi_i]), f1(PROV["Anthropic"][a_hi_i])))
    p.append('<section id="prov"><h2>1 \u00b7 Anthropic has led this panel in %d of %d months<span class="k">provider share of named-model usage, %%</span></h2>'
             '<p class="sub">%s In %s Anthropic holds <b>%s%%</b> (%+.1f pp m/m) and OpenAI <b>%s%%</b> '
             '(%+.1f pp m/m%s).%s %d models are live against %d at the start; the top model is <b>%s</b> at %s%%.</p>%s%s%s</section>'
             % (anth_streak, N, lo_txt,
                LATEST, f1(PROV["Anthropic"][-1]), PROV["Anthropic"][-1] - PROV["Anthropic"][-2], f1(PROV["OpenAI"][-1]), PROV["OpenAI"][-1] - PROV["OpenAI"][-2],
                (", %d consecutive monthly gains" % oa_run) if oa_run >= 2 else "", deb_txt, CONC[-1]["n_models"], CONC[0]["n_models"], esc(CONC[-1]["top1"]), f1(CONC[-1]["top1_share"]),
                AX.svg("prov", ch1, "Provider share of Ramp named-model usage by month"),
                legend(C1, ["Anthropic", "OpenAI", "Other \u2014 xAI + Cursor"], [None, None, "%s%% combined in %s" % ("%.2f" % OTHER[-1], LATEST)]), t1))

    # 2 ---------------------------------------------------------------- the ladder
    p.append('<section id="ladder"><h2>2 \u00b7 The mix moved up the ladder in one month<span class="k">Anthropic model families, %% of all named models</span></h2>'
             '<p class="sub">Between %s and %s the Opus-or-above share of Anthropic\u2019s own mix went from %s%% to %s%% \u2014 a single-month step from a premium niche to the majority of usage, '
             'and it has held since (<b>%s%%</b> in %s including Fable). Sonnet, which held two thirds of the whole panel in early 2025, is now %s%% of it. '
             '<b>This is a price/mix event as much as a usage event</b>: flagship tiers list at a multiple of mid-tier per token. Section 5 now tests that with the token sample.</p>%s%s%s</section>'
             % (lab(D[FLIP - 1]), lab(FLIP_M), f1(FRONT[FLIP - 1]), f1(FRONT[FLIP]), f1(FRONT[-1]), LATEST, f1(LAD["Sonnet"][-1]),
                AX.svg("lad", ch2, "Anthropic model families as a share of all named-model usage"),
                legend(LADC, ["Haiku", "Sonnet", "Opus", "Fable"], ["cheapest", None, None, "top tier, per ANTHROPIC.md"]), t2))

    # 3 ---------------------------------------------------------------- vintage
    p.append('<section id="vintage"><h2>3 \u00b7 Enterprise AI has no installed base<span class="k">usage by model age, %%</span></h2>'
             '<p class="sub">Models first seen within the last three months hold <b>%s\u2013%s%%</b> of all usage in every month since %s; in %s it is %s%%. '
             'Models older than a year hold <b>%s%%</b>. Nothing sediments: each release re-races the whole panel. <b>The shaded region is left-censored</b> \u2014 age is measured from '
             'first appearance in the panel (%s), not from true release, so the &gt;12-month band cannot fill until %s.</p>%s%s%s</section>'
             % (f1(min(VINT["le3"][y26:])), f1(max(VINT["le3"][y26:])), lab(D[y26]), LATEST, f1(VINT["le3"][-1]), f1(VINT["gt12"][-1]), lab(D[0]), lab(D[cens + 1]),
                AX.svg("vint", ch3, "Share of usage by model age bucket"), legend(VC, VL, ["the re-race", None, "the residue"]), t3))

    # 4 ---------------------------------------------------------------- launch curves
    p.append('<section id="launch"><h2>4 \u00b7 Launch curves<span class="k">share by months since debut \u00b7 every model peaking \u22654%%</span></h2>'
             '<p class="sub">Each panel starts at a model\u2019s first month on the panel; the ring marks its peak. The shape is consistent: a fast climb to a peak inside '
             '<b>%d\u2013%d months</b>, then a decay as the next release lands. The largest debut on file is <b>%s at %s%%</b> (%s). OpenAI\u2019s largest is <b>%s at %s%%</b>, '
             'then %s at %s%%. Panels share one axis (0\u2013%d%%); blue is Anthropic, orange OpenAI.</p><div class="smgrid">%s</div>%s</section>'
             % (min(m["months_to_peak"] for m in LAUNCH), max(m["months_to_peak"] for m in LAUNCH), esc(big_deb["model"]), f1(big_deb["debut_share"]), lab(big_deb["first"]),
                esc(oa_debs[0]["model"]), f1(oa_debs[0]["debut_share"]), esc(oa_debs[1]["model"]), f1(oa_debs[1]["debut_share"]), int(SMAX),
                "".join(sparkpanel(m) for m in LAUNCH), t4))

    # 5 ---------------------------------------------------------------- cross-read with tokens
    p.append('<section id="cross"><h2>5 \u00b7 Price vs volume \u2014 the token sample answers the question the spend series could not<span class="k">ladder shift, spend per employee and Anthropic token volume, one time axis</span></h2>'
             '<p class="sub">Three panels, dashed rule at %s. Anthropic\u2019s mix flips to Opus in the same month the spend series changes regime: median spend per employee compounded '
             '<b>%+.2f%%/mo</b> over the twelve months to %s, then <b>%+.2f%%/mo</b> over the %d months since (%s \u2192 %s, on the restated series). The earlier vintage of this page could not say '
             'how much of that was price/mix rather than volume. Ramp\u2019s Token Spend Management sample now carries both tokens and dollars per model, so the split is measurable \u2014 '
             'for that sample.</p>%s%s%s'
             '<div class="dec"><div><b>%s</b><span>token spend, all makers, %s \u2192 %s</span></div><div><b>%s</b><span>token volume, same window</span></div>'
             '<div><b>%s</b><span>implied blended $/M tokens (spend \u00f7 volume)</span></div><div><b>%s</b><span>Anthropic token spend</span></div><div><b>%s</b><span>Anthropic token volume</span></div>'
             '<div><b>%s</b><span>Anthropic blended $/M</span></div><div><b>%s</b><span>median spend / employee, same window</span></div></div>'
             '<div class="note goodn"><b>Verdict for the sample: volume, not price.</b> Since the ladder flip, token volume in the sample grew <b>%s</b> while blended price per token '
             '<b>fell</b> to %s of its %s level \u2014 so dollars grew less than tokens, and the spend acceleration <i>understates</i> volume growth rather than overstating it. '
             'The Sep-02 caution on this page (that the +%s%%/mo of the old vintage was partly price/mix) was right to be asked and is answered the other way for this sample: the mix moved up the ladder '
             'and the blended price still fell, because cached-input tokens and cheaper tiers dilute the average, and list prices themselves came down. '
             'The cleanest price read confirms the mix story on the way up: Anthropic’s <b>output</b> $/M in the sample went %s (%s) → %s (%s) → %s (%s) — up with the ladder, then easing — '
             'so the mix effect is real at the output-token level and is simply outweighed by cache share and volume in the blend. '
             '<b>Limits:</b> the token sample is the subset of Ramp customers using its TSM product (Ramp: \u201cnot representative of Ramp\u2019s total AI spend volume, though results are '
             'directionally similar\u201d); the spend-per-employee series is the whole panel; the two are not the same firms. Blended $/M mixes token types (cached input is a fraction of list), '
             'so a falling blend is partly cache share, not only price cuts \u2014 section 8 separates output and uncached input.</div>%s</section>'
             % (lab(FLIP_M), REG_PRE, lab(FLIP_M), REG_POST, POST_MONTHS, money(SPMED[fs]), money(SPMED[-1]),
                ch5, ch6, ch6b,
                xfmt(DEC["spend_x"]), lab(DEC["from"]), lab(DEC["to"]), xfmt(DEC["vol_x"]), xfmt(DEC["price_x"]), xfmt(DEC["ant_spend_x"]), xfmt(DEC["ant_vol_x"]), xfmt(DEC["ant_price_x"]), xfmt(DEC["pepm_x"]),
                xfmt(DEC["vol_x"]), xfmt(DEC["price_x"]), lab(DEC["from"]), "12.44",
                money(first_val(PR.get("anthropic|output", []))), labw(PD[0]),
                money(PR["anthropic|output"][PD.index([d for d in PD if d[:7] == FLIP_M][-1])]) if any(d[:7] == FLIP_M for d in PD) else "—", lab(FLIP_M),
                money(last_val(PR.get("anthropic|output", []))), labw(PD[-1]), t5))

    # 6 ---------------------------------------------------------------- spend series + restatement
    rs_txt = ""
    if rs_sp:
        lc = rs_sp["latest_common"]
        rs_txt = ('<div class="note warnn"><b>Ramp restated this series.</b> The vintage on this page until Oct-2026 (CSV supplied by Felipe 2026-08-20, through %s) differs from the live series in '
                  '<b>every month</b>: the median is revised between %+.1f%% and %+.1f%%, and the first two months (%s) were dropped. For the latest common month, %s, the median moved from '
                  '<b>%s to %s</b>, the top-10%% cohort from %s to %s and the top-1%% from %s to %s. <b>Quote the vintage with the number</b> \u2014 the wiki pages that carry the old marks '
                  '(tokenmaxxing, macro-cycle, SPCX) keep them in their changelogs. Ramp\u2019s published definition now reads: monthly observed AI spending \u00f7 employee count for businesses in the reported cohort.</div>%s'
                  % (lab(rs_sp["vintage"].split("through-")[1][:7]), rs_sp["median_revision_pct_range"][0], rs_sp["median_revision_pct_range"][1],
                     ", ".join(lab(m) for m in rs_sp["dropped_months"]) or "none", lab(lc["month"]), money(lc["median"]["old"]), money(lc["median"]["new"]),
                     money(lc["top10"]["old"]), money(lc["top10"]["new"]), money(lc["top1"]["old"], 0), money(lc["top1"]["new"], 0), tRS))
    p.append('<section id="spend"><h2>6 \u00b7 The spend series in full<span class="k">three cohorts, indexed, %s = 100</span></h2>'
             '<p class="sub">Levels differ by ~%dx across cohorts (%s vs %s vs %s in %s), so the chart indexes each to its own %s base \u2014 never two y-axes. '
             'Cohorts are <b>re-cut every month</b>, so part of each step is re-ranking rather than same-company growth, which is why the top-1%% cohort is the noisiest line and the least safe to '
             'quote month-to-month. The table also carries the p90 / p99 company and Ramp\u2019s spend-weighted (winsorised) mean, which is the series closest to \u201cdollars\u201d: %s per employee in %s.</p>%s%s%s%s</section>'
             % (lab(SPD[0]), int(round(SP["cohorts"]["top1"]["level"][-1] / SPMED[-1])), money(SPMED[-1]), money(SP["cohorts"]["top10"]["level"][-1]), money(SP["cohorts"]["top1"]["level"][-1], 0), lab(SPD[-1]), lab(SPD[0]),
                money(SX["winsorized_weighted"][-1]), lab(SPD[-1]),
                ch7, legend([c for _, _, c in COH], [n for _, n, _ in COH], [money(SPMED[-1]), money(SP["cohorts"]["top10"]["level"][-1]), money(SP["cohorts"]["top1"]["level"][-1], 0)]), t7, rs_txt))

    # 7 ---------------------------------------------------------------- segments
    big = [l for l in fte_labels if l == "Large"]
    small = [l for l in fte_labels if l == "Small"]
    seg_line = ""
    if big and small:
        seg_line = ("Per employee, <b>small</b> companies spend <b>%s</b> a month against <b>%s</b> at large ones (%s) \u2014 a %.1fx gap that was %.1fx in %s: "
                    "headcount is the denominator, and a 20-person firm with two Claude Code seats reads as heavy. "
                    % (money(FTE["median"]["Small"][-1]), money(FTE["median"]["Large"][-1]), lab(SPD[-1]),
                       FTE["median"]["Small"][-1] / FTE["median"]["Large"][-1], FTE["median"]["Small"][SPD.index(D[0])] / FTE["median"]["Large"][SPD.index(D[0])], lab(D[0])))
    vc = FIN.get("median", {}).get("VC-backed")
    pe = FIN.get("median", {}).get("PE-backed")
    fin_line = ("VC-backed firms spend <b>%s</b> per employee, PE-backed <b>%s</b>, everyone else <b>%s</b>. " % (money(vc[-1]), money(pe[-1]), money(FIN["median"]["Other"][-1]))) if (vc and pe and FIN["median"].get("Other")) else ""
    leads = [r for r in seg_share_rows if r[3][0] != "\u2014" and float(r[2][0]) > float(r[3][0])]
    trails = [r for r in seg_share_rows if r[3][0] != "\u2014" and float(r[2][0]) <= float(r[3][0])]
    share_line = ("Anthropic leads named-model usage in %d of %d published segments (%s) and trails OpenAI in %s. "
                  % (len(leads), len(seg_share_rows), ", ".join("%s %s%%" % (r[1], r[2][0]) for r in sorted(leads, key=lambda r: -float(r[2][0]))[:4]),
                     ", ".join("%s %s%%" % (r[1], r[2][0]) for r in sorted(trails, key=lambda r: float(r[2][0]))[:4]) or "none"))
    p.append('<section id="segments"><h2>7 \u00b7 Who spends, and who uses what<span class="k">spend per employee by segment \u00b7 model share by segment</span></h2>'
             '<p class="sub">%s%s%s<b>Segment cuts are thin</b>: Ramp publishes only the larger models per segment, so a 0.0 means no row for that vendor in that segment-month, not zero usage.</p>%s%s%s'
             '<h3>Anthropic vs OpenAI share of named-model usage, by segment</h3>%s</section>'
             % (seg_line, fin_line, share_line, ch8, legend(SEG_C[:len(fte_labels)], fte_labels), t8, t9))

    # 8 ---------------------------------------------------------------- tokens
    a_first = first_val(PR.get("anthropic|all_tokens", []))
    a_last = last_val(PR.get("anthropic|all_tokens", []))
    o_first = first_val(PR.get("openai|all_tokens", []))
    o_last = last_val(PR.get("openai|all_tokens", []))
    g_first_i = next((i for i in range(WN) if VOL["google"][i] > 0), None)
    p.append('<section id="tokens"><h2>8 \u00b7 The token sample: %s tn tokens and %s a week<span class="k">Token Spend Management sample \u00b7 weekly \u00b7 %d model series, %d makers</span></h2>'
             '<p class="sub">Ramp\u2019s TSM product imports usage and billing from connected providers, so this cut is the only one with <b>tokens</b> in it and the only one where Google, Meta, DeepSeek and the '
             'Chinese labs appear at all. In the week to %s Anthropic carried <b>%s%%</b> of tokens and <b>%s%%</b> of dollars; OpenAI %s%% / %s%%; Google %s%% of tokens%s; everything else %s%%. '
             'The sample\u2019s own blended price fell from %s to %s per million tokens for Anthropic and %s to %s for OpenAI between %s and %s.</p>%s%s%s'
             '<h3>Weekly token spend by maker, $M</h3>%s'
             '<h3>Blended price per million tokens, by token type</h3><p class="sub">Trailing-7-day cost \u00f7 tokens from Ramp\u2019s price series, Anthropic and OpenAI only. <b>Output</b> and <b>uncached input</b> are the '
             'cleanest price reads; \u201call tokens\u201d is diluted by cached input. The gap between the two makers is mostly mix (which tiers the sample buys), not list price per tier.</p>%s%s%s</section>'
             % ("%.1f" % (WTOT[-1] / 1e12), "$%.1fM" % (WSTOT[-1] / 1e6), TK["model_count"], len(MAKERS),
                labw(WK[-1]), f1(VSHARE["anthropic"][-1]), f1(100 * SPND["anthropic"][-1] / WSTOT[-1]), f1(VSHARE["openai"][-1]), f1(100 * SPND["openai"][-1] / WSTOT[-1]),
                f1(VSHARE["google"][-1]), (" (first seen %s)" % labw(WK[g_first_i])) if g_first_i is not None else "", f1(VSHARE["other"][-1]),
                money(a_first), money(a_last), money(o_first), money(o_last), labw(PD[0]), labw(PD[-1]),
                ch10, legend(TKC, TKL, [None, None, None, None, ", ".join(MK_LABEL.get(m, m) for m, _ in other_latest[:6])]), t10,
                ch11, ch12, legend([c for _, _, c in pr_series], [l for _, l, _ in pr_series]), t12))

    # 9 ---------------------------------------------------------------- reconciliation
    p.append('<section id="basis"><h2>9 \u00b7 Reconciliation and basis traps<span class="k">read this before quoting anything above</span></h2>'
             '<div class="note"><b>Four different denominators, one panel.</b> (i) <b>Adoption</b> counts firms with any AI payment (section A); (ii) <b>vendor penetration</b> counts firms paying a vendor, '
             'overlapping (B: Anthropic %s%% vs OpenAI %s%% in %s); (iii) <b>model share</b> is share of named-model usage and sums to 100 (1: %s%% vs %s%% in %s); (iv) <b>token share</b> is the TSM '
             'sub-sample\u2019s token volume (8: %s%% vs %s%%). Read together: Anthropic and OpenAI are close on <b>customer count</b> while Anthropic takes roughly <b>%.1fx the usage</b> \u2014 the lead is '
             'intensity per customer. \u201cAnthropic has %s%% of the enterprise LLM market\u201d is not a sentence any of these supports.</div>'
             '<ul class="cav">%s</ul>'
             '<div class="note"><b>What would change the picture.</b> OpenAI gaining usage share for a third consecutive month; Google rows appearing in the model-share panel (they exist only in the token sample, '
             'at %s%% of tokens); the adoption curve flattening further (%+.1f pp in the last six months); the &le;3-month vintage band falling below ~50%%; or Ramp restating again \u2014 this vintage already moved every month of the spend series.</div></section>'
             % (f1(ven_a), f1(ven_o), LAT_A, f1(PROV["Anthropic"][-1]), f1(PROV["OpenAI"][-1]), LATEST, f1(VSHARE["anthropic"][-1]), f1(VSHARE["openai"][-1]),
                PROV["Anthropic"][-1] / PROV["OpenAI"][-1], f1(PROV["Anthropic"][-1]),
                "".join("<li>%s</li>" % esc(c).replace("COVERAGE:", "<b>COVERAGE:</b>").replace("BASIS:", "<b>BASIS:</b>").replace("VINTAGE IS LEFT-CENSORED:", "<b>VINTAGE IS LEFT-CENSORED:</b>")
                        for c in MS["caveats"]) + "".join("<li>%s</li>" % esc(c).replace("RESTATED:", "<b>RESTATED:</b>") for c in SP["caveats"])
                + "<li><b>TOKEN SAMPLE:</b> %s</li>" % esc(TK["definition"]),
                f1(VSHARE["google"][-1]), ADO[-1] - ADO[-7]))

    p.append("</main>")
    p.append('<div id="tt"></div>')
    p.append("<footer>Source: <b>Ramp AI Index</b> (Ramp Economics Lab, Ara Kharazian), <a href='https://ramp.com/data/ai-index'>ramp.com/data/ai-index</a>, pulled %s by "
             "<code>fetch_ramp_index.py</code> from the page\u2019s inline data; earlier vintages (CSVs supplied by Felipe 2026-08-20 and 2026-09-02) archived under "
             "<code>_wiki/_data/ramp-ai-index/vintages/</code>. Panel = Ramp\u2019s US corporate-card / bill-pay customer base (70,000+ firms) \u2014 not total enterprise AI spend, and not a revenue "
             "proxy for any listed name. The token cut is the Token Spend Management sub-sample. Anthropic tier ordering (Haiku&lt;Sonnet&lt;Opus&lt;Fable) is the wiki\u2019s read per "
             "<code>_wiki/ANTHROPIC.md</code>, not a Ramp field. Built by <code>_wiki/_tools/build_ramp_dash.py</code>.</footer>" % esc(META.get("fetched_at", "")))
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
