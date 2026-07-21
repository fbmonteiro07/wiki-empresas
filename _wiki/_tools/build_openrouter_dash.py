r"""
build_openrouter_dash.py — render _wiki/_data/openrouter/dashboard.json into a
self-contained, theme-aware HTML dashboard at _wiki/_dashboards/openrouter.html
(also suitable to publish as an Artifact — no external assets).

Colors follow the dataviz reference palette; categorical capture-classes carry
direct labels (secondary encoding) so identity is never colour-alone.

Run (after or_fetch.py + or_build.py):
  py "E:\Wiki Felipe empresas\_wiki\_tools\build_openrouter_dash.py"
"""
import json
import math
import datetime as dt
from pathlib import Path

DATA = Path("E:/Wiki Felipe empresas/_wiki/_data")
DASH = Path("E:/Wiki Felipe empresas/_wiki/_dashboards")
OR = DATA / "openrouter"

D = json.loads((OR / "dashboard.json").read_text(encoding="utf-8"))
ARR = json.loads((OR / "arr.json").read_text(encoding="utf-8"))

CAP_LABEL = {"first-party": "First-party API", "open+own": "Open-weight + own API", "open-weight": "Open-weight (hosted)"}
CAP_COLOR = {"first-party": "var(--s1)", "open+own": "var(--s2)", "open-weight": "var(--s3)"}


def tok(x):
    if x >= 1e12:
        return "%.1fT" % (x / 1e12)
    if x >= 1e9:
        return "%.0fB" % (x / 1e9)
    return "%.0fM" % (x / 1e6)


def dol(x):  # x in USD -> $B/$M/$k
    if abs(x) >= 1e9:
        return "$%.2fB" % (x / 1e9)
    if abs(x) >= 1e6:
        return "$%.0fM" % (x / 1e6)
    return "$%.0fk" % (x / 1e3)


def pct(x, dp=1):
    return ("%." + str(dp) + "f%%") % (x * 100)


def esc(s):
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


plat = D["platform"]
labs = D["labs"]
models = D["models"]
apps = D["apps"]
guards = D["guardrails"]
orr = D["anchors"]

# ---------- HERO TILES ----------
top_lab = labs[0]
top_app = next((a for a in apps if a.get("title")), {})
tiles = [
    ("Tokens / day", tok(plat["daily_tokens"]), "routed via OpenRouter (~%s / mo)" % tok(plat["tokens_month_run_rate"])),
    ("Implied spend / yr", dol(plat["revenue_annualized"]), "at OpenRouter list price · upper bound"),
    ("Blended price", "$%.2f" % plat["blended_price_per_mtok"], "per 1M tokens (weighted)"),
    ("#1 by implied $", top_lab["display"], "%s/yr · %s of $, %s of tokens" % (dol(top_lab["revenue_annualized"]), pct(top_lab["rev_share"], 0), pct(top_lab["token_share"], 0))),
    ("#1 app", esc(top_app.get("title", "-")), "%s tokens/wk · coding agents lead" % tok(top_app.get("tokens_week", 0))),
]

# ---------- SCATTER: token share vs revenue share (log-log) ----------
sc_labs = [l for l in labs if l["token_share"] > 0 and l["rev_share"] > 0][:16]
LO, HI = 0.1, 100.0  # % axis bounds
W, H, PAD_L, PAD_B, PAD_T, PAD_R = 720, 460, 54, 46, 20, 20
PW, PH = W - PAD_L - PAD_R, H - PAD_T - PAD_B


def sx(share_pct):
    v = max(min(share_pct, HI), LO)
    return PAD_L + (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * PW


def sy(share_pct):
    v = max(min(share_pct, HI), LO)
    return PAD_T + PH - (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO)) * PH


maxrev = max(l["revenue_annualized"] for l in sc_labs) or 1
LABEL_THESE = {"Anthropic", "OpenAI", "Google (Gemini)", "DeepSeek", "Xiaomi", "Moonshot (Kimi)", "Z.ai (Zhipu)", "xAI (Grok)", "MiniMax", "NVIDIA (Nemotron)"}
svg = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Token share versus revenue share by lab" font-family="system-ui,-apple-system,Segoe UI,sans-serif">' % (W, H)]
# gridlines + ticks at 0.1,1,10,100
for gv in (0.1, 1, 10, 100):
    x = sx(gv); y = sy(gv)
    svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (x, PAD_T, x, PAD_T + PH))
    svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)" stroke-width="1"/>' % (PAD_L, y, PAD_L + PW, y))
    lbl = ("%g%%" % gv)
    svg.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="11" text-anchor="middle">%s</text>' % (x, PAD_T + PH + 16, lbl))
    svg.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="11" text-anchor="end">%s</text>' % (PAD_L - 6, y + 3, lbl))
# 45-degree tokens==dollars reference line
svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="5 4"/>' % (sx(LO), sy(LO), sx(HI), sy(HI)))
svg.append('<text x="%.1f" y="%.1f" fill="var(--muted)" font-size="10.5" text-anchor="end" transform="rotate(-30 %.1f %.1f)">tokens = dollars</text>' % (sx(45), sy(70), sx(45), sy(70)))
# axis titles
svg.append('<text x="%.1f" y="%.1f" fill="var(--ink2)" font-size="12" text-anchor="middle">Share of tokens (log)</text>' % (PAD_L + PW / 2, H - 6))
svg.append('<text transform="rotate(-90 14 %.1f)" x="14" y="%.1f" fill="var(--ink2)" font-size="12" text-anchor="middle">Share of implied $ (log)</text>' % (PAD_T + PH / 2, PAD_T + PH / 2))
# regions annotation
svg.append('<text x="%.1f" y="%.1f" fill="var(--good)" font-size="11" text-anchor="start" opacity="0.9">premium ▲ ($ &gt; tokens)</text>' % (PAD_L + 8, PAD_T + 16))
svg.append('<text x="%.1f" y="%.1f" fill="var(--crit)" font-size="11" text-anchor="end" opacity="0.9">commodity ▼ (tokens &gt; $)</text>' % (PAD_L + PW - 6, PAD_T + PH - 8))
for l in sc_labs:
    x = sx(l["token_share"] * 100); y = sy(l["rev_share"] * 100)
    r = 5 + 20 * math.sqrt(l["revenue_annualized"] / maxrev)
    col = CAP_COLOR[l["capture"]]
    svg.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="0.5" stroke="%s" stroke-width="1.5"><title>%s\ntokens %s · $ %s\nimplied %s/yr · $%.2f/Mtok</title></circle>' % (
        x, y, r, col, col, esc(l["display"]), pct(l["token_share"]), pct(l["rev_share"]), dol(l["revenue_annualized"]), l["blended_price_per_mtok"]))
    if l["display"] in LABEL_THESE:
        dy = -r - 4 if y > PAD_T + 30 else r + 12
        svg.append('<text x="%.1f" y="%.1f" fill="var(--ink)" font-size="11" font-weight="600" text-anchor="middle">%s</text>' % (x, y + dy, esc(l["display"].split(" (")[0])))
svg.append('</svg>')
scatter_svg = "".join(svg)

# ---------- $/yr BAR (top labs) ----------
bar_labs = labs[:12]
mx = max(l["revenue_annualized"] for l in bar_labs) or 1
bars = []
for l in bar_labs:
    w = l["revenue_annualized"] / mx * 100
    mom = l["momentum"]
    if mom is None:
        chip = '<span class="mut">n/a</span>'
    else:
        cls = "up" if mom >= 0 else "dn"
        arw = "▲" if mom >= 0 else "▼"
        chip = '<span class="mom %s">%s %+.0f%%</span>' % (cls, arw, mom * 100)
    bars.append(
        '<div class="barrow"><div class="barname" style="border-left:3px solid %s">%s <span class="cap">%s</span></div>'
        '<div class="bartrack"><div class="barfill" style="width:%.1f%%;background:%s"></div></div>'
        '<div class="barval">%s/yr</div><div class="barmom">%s</div></div>' % (
            CAP_COLOR[l["capture"]], esc(l["display"]), esc(l["capture"].replace("-", " ")), w, CAP_COLOR[l["capture"]],
            dol(l["revenue_annualized"]), chip))
bars_html = "".join(bars)

# ---------- LAB TABLE ----------
def momcell(m):
    if m is None:
        return '<td class="r mut" data-v="-999">n/a</td>'
    cls = "pos" if m >= 0 else "neg"
    return '<td class="r %s" data-v="%.4f">%+.0f%%</td>' % (cls, m, m * 100)


rows = []
for l in labs:
    arr_b = l.get("arr_busd")
    arr_txt = ("$%.1fB" % arr_b) if arr_b else '<span class="mut">n/a</span>'
    orpct = l.get("or_pct_of_arr")
    orpct_txt = ("%.1f%%" % orpct) if orpct is not None else '<span class="mut">—</span>'
    rows.append(
        '<tr><td>%s</td><td><span class="capdot" style="background:%s"></span>%s</td>'
        '<td class="r" data-v="%.5f">%s</td><td class="r" data-v="%.5f">%s</td>'
        '<td class="r" data-v="%.4f"><b>%s</b></td><td class="r" data-v="%.4f">$%.2f</td>%s'
        '<td class="r" data-v="%s">%s</td><td class="r" data-v="%s">%s</td></tr>' % (
            esc(l["display"]), CAP_COLOR[l["capture"]], esc(CAP_LABEL.get(l["capture"], l["capture"])),
            l["token_share"], pct(l["token_share"]), l["rev_share"], pct(l["rev_share"]),
            l["revenue_annualized"], dol(l["revenue_annualized"]),
            l["blended_price_per_mtok"], l["blended_price_per_mtok"],
            momcell(l["momentum"]),
            (arr_b or -1), arr_txt, (orpct if orpct is not None else -1), orpct_txt))
lab_table = "".join(rows)

# ---------- ARR BRIDGE ----------
bridge = [l for l in labs if l.get("arr_busd")]
bridge.sort(key=lambda l: -l["arr_busd"])
bmx = max(l["arr_busd"] for l in bridge) or 1
brows = []
for l in bridge:
    aw = l["arr_busd"] / bmx * 100
    orw = min(l["revenue_annualized"] / 1e9 / bmx * 100, aw)
    fp = l["capture"] == "first-party"
    note = "" if fp else " *"
    brows.append(
        '<div class="barrow"><div class="barname">%s%s</div>'
        '<div class="bartrack"><div class="barfill" style="width:%.2f%%;background:var(--arrbar)"></div>'
        '<div class="barfill orslice" style="width:%.2f%%;background:var(--s1)" title="OpenRouter list-$ ≈ %s/yr"></div></div>'
        '<div class="barval">$%.1fB <span class="mut">ARR</span></div>'
        '<div class="barmom">OR ≈ %s</div></div>' % (
            esc(l["display"]), note, aw, max(orw, 0.6), dol(l["revenue_annualized"]), l["arr_busd"],
            ("%.1f%%" % l["or_pct_of_arr"]) if l.get("or_pct_of_arr") is not None else "—"))
bridge_html = "".join(brows)

# ---------- MODELS TABLE ----------
mrows = []
for m in models[:20]:
    mrows.append('<tr><td>%s</td><td>%s</td><td class="r" data-v="%.1f">%s</td><td class="r" data-v="%.1f"><b>%s/yr</b></td><td class="r" data-v="%.4f">$%.2f</td></tr>' % (
        esc(m["name"]), esc(m["lab"]), m["daily_tokens"], tok(m["daily_tokens"]),
        m["revenue_annualized"], dol(m["revenue_annualized"]), m["blended_price_per_mtok"], m["blended_price_per_mtok"]))
models_table = "".join(mrows)

# ---------- APPS ----------
amx = max(a["tokens_week"] for a in apps) or 1
arows = []
for a in apps[:15]:
    if not a.get("title"):
        continue
    w = a["tokens_week"] / amx * 100
    cats = ", ".join(a.get("categories", [])[:2])
    arows.append(
        '<div class="barrow"><div class="barname apn">%s <span class="cap">%s</span></div>'
        '<div class="bartrack"><div class="barfill" style="width:%.1f%%;background:var(--s1)"></div></div>'
        '<div class="barval">%s/wk</div></div>' % (esc(a["title"]), esc(cats), w, tok(a["tokens_week"])))
apps_html = "".join(arows)

# ---------- GUARDRAILS ----------
gmap = {"PASS": "good", "WARN": "warn", "INFO": "info", "FAIL": "crit"}
grows = []
for k, (st, msg) in guards.items():
    grows.append('<tr><td><span class="gstat %s">%s</span></td><td>%s</td><td>%s</td></tr>' % (
        gmap.get(st, "info"), st, esc(k.replace("_", " ")), esc(msg)))
guard_html = "".join(grows)

tiles_html = "".join(
    '<div class="tile"><div class="tlabel">%s</div><div class="tval">%s</div><div class="tsub">%s</div></div>' % (esc(t[0]), esc(t[1]), esc(t[2]))
    for t in tiles)

asof = D["asof"]
gen = D["generated"]

CSS = r"""
:root{color-scheme:light;--plane:#f9f9f7;--surf:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
--grid:#e1e0d9;--base:#c3c2b7;--border:rgba(11,11,11,.10);
--s1:#2a78d6;--s2:#008300;--s3:#e87ba4;--good:#0ca30c;--crit:#d03b3b;--warn:#c98500;
--arrbar:#b7d3f6;--headbg:#0f1729;--headink:#fff;--headsub:#8492ad;--link:#7fb0ff;}
@media(prefers-color-scheme:dark){:root:where(:not([data-theme=light])){color-scheme:dark;
--plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--base:#383835;
--border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#008300;--s3:#d55181;--good:#0ca30c;--crit:#d03b3b;--warn:#eda100;
--arrbar:#184f95;--headbg:#000;--headink:#fff;--headsub:#8492ad;--link:#7fb0ff;}}
:root[data-theme=dark]{color-scheme:dark;--plane:#0d0d0d;--surf:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;
--grid:#2c2c2a;--base:#383835;--border:rgba(255,255,255,.10);--s1:#3987e5;--s2:#008300;--s3:#d55181;
--good:#0ca30c;--crit:#d03b3b;--warn:#eda100;--arrbar:#184f95;--headbg:#000;--headink:#fff;--headsub:#8492ad;--link:#7fb0ff;}
*{box-sizing:border-box}
body{margin:0;background:var(--plane);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{background:var(--headbg);color:var(--headink);padding:20px 28px}
header h1{margin:0;font-size:21px} header p{margin:5px 0 0;color:var(--headsub);font-size:13px}
header a{color:var(--link);text-decoration:none}
main{max-width:1080px;margin:0 auto;padding:22px 26px 90px}
h2{font-size:17px;margin:34px 0 4px;border-bottom:1px solid var(--grid);padding-bottom:6px}
.sub{color:var(--ink2);font-size:13px;margin:0 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:18px 0 6px}
.tile{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.tlabel{color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em}
.tval{font-size:25px;font-weight:700;margin:3px 0 2px;line-height:1.15}
.tsub{color:var(--ink2);font-size:12px}
.card{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:16px 18px;margin:12px 0}
.callout{border-left:4px solid var(--s1);background:var(--surf);padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0;font-size:14px}
.callout b{color:var(--ink)}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2);margin:6px 0 2px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.dot{width:11px;height:11px;border-radius:50%;display:inline-block}
.barrow{display:grid;grid-template-columns:210px 1fr 96px 84px;align-items:center;gap:10px;margin:5px 0;font-size:13px}
.barname{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:7px}
.barname .cap,.apn .cap{color:var(--muted);font-size:11px;display:block;line-height:1.1}
.bartrack{background:var(--grid);border-radius:4px;height:16px;position:relative;display:flex;gap:2px}
.barfill{height:16px;border-radius:4px;min-width:2px}
.orslice{border-radius:4px;opacity:.95}
.barval{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.barmom{text-align:right;font-size:12px;color:var(--ink2);font-variant-numeric:tabular-nums}
.mom{font-weight:600}.mom.up{color:var(--good)}.mom.dn{color:var(--crit)}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12.7px}
th,td{border-bottom:1px solid var(--grid);padding:6px 9px;text-align:left}
th{color:var(--ink2);font-weight:700;cursor:pointer;white-space:nowrap;user-select:none}
th.r,td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:hover td{background:rgba(127,127,127,.06)}
.pos{color:var(--good)}.neg{color:var(--crit)}.mut{color:var(--muted)}
.capdot,.capdot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:6px}
.scroll{overflow-x:auto}
.gstat{font-weight:700;font-size:11px;padding:1px 7px;border-radius:9px}
.gstat.good{background:rgba(12,163,12,.15);color:var(--good)} .gstat.warn{background:rgba(201,133,0,.16);color:var(--warn)}
.gstat.info{background:rgba(127,127,127,.14);color:var(--ink2)} .gstat.crit{background:rgba(208,59,59,.15);color:var(--crit)}
.note{color:var(--ink2);font-size:12.5px} .note code{background:var(--grid);padding:1px 5px;border-radius:4px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:820px){.grid2{grid-template-columns:1fr}.barrow{grid-template-columns:150px 1fr 78px}.barmom{display:none}}
"""

JS = r"""
function sortT(t,c,num){var tb=t.tBodies[0],rs=[].slice.call(tb.rows);
var asc=t.getAttribute('data-c')==c?!(t.getAttribute('data-a')=='1'):true;
t.setAttribute('data-c',c);t.setAttribute('data-a',asc?'1':'0');
rs.sort(function(a,b){var x=a.cells[c],y=b.cells[c];
var av=num?parseFloat(x.getAttribute('data-v')||x.textContent):x.textContent.trim().toLowerCase();
var bv=num?parseFloat(y.getAttribute('data-v')||y.textContent):y.textContent.trim().toLowerCase();
if(num){av=isNaN(av)?-1e18:av;bv=isNaN(bv)?-1e18:bv;}return asc?(av>bv?1:av<bv?-1:0):(av<bv?1:av>bv?-1:0);});
rs.forEach(function(r){tb.appendChild(r);});}
document.querySelectorAll('table.sortable').forEach(function(t){[].forEach.call(t.tHead.rows[0].cells,function(th,i){
th.onclick=function(){sortT(t,i,th.classList.contains('r'));};});});
"""

HTML = (
    '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>AI-Lab Traction — OpenRouter</title><style>' + CSS + '</style></head><body>'
    '<header><h1>AI-Lab Traction Monitor <span style="font-weight:400;color:var(--headsub)">· built on OpenRouter public data</span></h1>'
    '<p>Token demand → implied inference spend by lab · as of <b>' + asof + '</b> · trailing-7-day window · '
    '<a href="../index.html">← wiki</a></p></header><main>'
    '<div class="callout"><b>What this is.</b> A reconstruction of an "AI-lab ARR" view using only OpenRouter\'s public usage feed. '
    'It measures <b>developer/API traction routed through OpenRouter</b> — a real, high-frequency leading indicator, but a <i>slice</i>: '
    'it excludes first-party enterprise API and consumer subscriptions (ChatGPT/Claude/Gemini), which are the bulk of frontier-lab ARR. '
    'Dollars are <b>tokens × OpenRouter list price</b> = spend at list (an upper bound), not realized revenue.</div>'
    '<div class="tiles">' + tiles_html + '</div>'
    '<h2>Tokens ≠ dollars</h2>'
    '<p class="sub">Each lab plotted by its share of tokens (volume) vs share of implied dollars (value). '
    'On the dashed line, a lab earns dollars in line with its volume. <b>Above</b> = premium pricing (Anthropic); <b>below</b> = commodity volume (DeepSeek, Xiaomi). Bubble size = implied $/yr.</p>'
    '<div class="card">' + scatter_svg +
    '<div class="legend"><span><span class="dot" style="background:var(--s1)"></span>First-party API (OR $ ≈ lab)</span>'
    '<span><span class="dot" style="background:var(--s2)"></span>Open-weight + own API</span>'
    '<span><span class="dot" style="background:var(--s3)"></span>Open-weight (hosted — $ to 3rd-party, not lab)</span></div></div>'
    '<h2>Implied annualized spend by lab</h2>'
    '<p class="sub">Tokens × list price, annualized from the trailing-7-day run-rate. Momentum = 7-day daily rate vs 30-day daily rate.</p>'
    '<div class="card">' + bars_html + '</div>'
    '<h2>Lab leaderboard</h2><div class="card scroll"><table class="sortable"><thead><tr>'
    '<th>Lab</th><th>Capture</th><th class="r">Token share</th><th class="r">$ share</th><th class="r">Implied $/yr</th>'
    '<th class="r">$/Mtok</th><th class="r">Momentum</th><th class="r">Reported ARR</th><th class="r">OR % of ARR</th></tr></thead>'
    '<tbody>' + lab_table + '</tbody></table>'
    '<p class="note">Capture = how OpenRouter dollars map to the lab. <b>First-party</b>: OR routes to the lab\'s own API, so implied $ ≈ a thin slice of the lab\'s revenue. '
    '<b>Open-weight (hosted)</b>: served by third-party inference providers — the dollars accrue to the host, not the model\'s author, so "OR % of ARR" is not meaningful there.</p></div>'
    '<div class="grid2">'
    '<div><h2>Reported ARR bridge</h2><p class="sub">How thin the OpenRouter slice is vs each lab\'s <i>total</i> reported run-rate. Blue tick = OR implied list-$. <span class="mut">* open-weight: OR $ is host revenue, not the lab\'s.</span></p>'
    '<div class="card">' + bridge_html + '</div></div>'
    '<div><h2>Top apps driving demand</h2><p class="sub">Trailing-7-day tokens by consuming app — coding agents dominate.</p>'
    '<div class="card">' + apps_html + '</div></div>'
    '</div>'
    '<h2>Top models by implied spend</h2><div class="card scroll"><table class="sortable"><thead><tr>'
    '<th>Model</th><th>Lab</th><th class="r">Tokens/day</th><th class="r">Implied $/yr</th><th class="r">$/Mtok</th></tr></thead>'
    '<tbody>' + models_table + '</tbody></table></div>'
    '<h2>Methodology &amp; guardrails</h2>'
    '<div class="card"><table><thead><tr><th>Check</th><th>Metric</th><th>Result</th></tr></thead><tbody>' + guard_html + '</tbody></table>'
    '<p class="note" style="margin-top:12px"><b>Anchor.</b> OpenRouter\'s reported actual spend was ~$' + str(orr.get("reported_monthly_spend_musd")) + 'M/mo ('
    + str(orr.get("spend_asof")) + '); this model\'s <i>list-price</i> spend runs higher (list &gt; realized; multi-provider discounting; plus platform growth since the anchor), '
    'so treat the absolute $ as an <b>upper bound</b> and lean on <b>relative shares & momentum</b>. Sources: Menlo Ventures ("&gt;1 quadrillion tokens/yr"), Sacra (~$50M OR revenue @ ~5% take). '
    'Token counts &amp; prices are OpenRouter\'s own public feed (' + esc(orr.get("source", "")) + ').</p>'
    '<p class="note"><b>Refresh.</b> <code>py _wiki/_tools/or_fetch.py</code> → <code>py _wiki/_tools/or_build.py</code> → <code>py _wiki/_tools/build_openrouter_dash.py</code>. '
    'The token API returns trailing 7/30-day totals only (no back-history); a daily snapshot is appended to <code>history.jsonl</code> to build a go-forward trend. '
    'ARR figures are hand-edited in <code>_data/openrouter/arr.json</code> (each attributed).</p>'
    '<p class="note">Generated ' + gen + ' · data © OpenRouter (public). Implied-revenue and ARR-bridge figures are estimates, not the labs\' reported revenue.</p></div>'
    '</main><script>' + JS + '</script></body></html>'
)

out = DASH / "openrouter.html"
out.write_text(HTML, encoding="utf-8")
print("wrote", out, "(%.0f KB)" % (len(HTML) / 1024))
