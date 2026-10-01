#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_funding_monitor.py — render the AI credit & funding monitor.

Reads  _data/funding_deals.json   (hand-edit ledger + config, attributed)
       _data/funding_market.json  (BBG series written by fetch_funding.py)
Writes _dashboards/credit-monitor.html  (self-contained, EN, light+dark)

Weekly refresh: refresh_credit_monitor.py (Fridays 09:00 America/Sao_Paulo).
    py "E:/Wiki Felipe empresas/_wiki/_tools/fetch_funding.py"      # market data
    py "E:/Wiki Felipe empresas/_wiki/_tools/build_funding_monitor.py"
"""
import json
import html as H
import datetime as dt
from pathlib import Path
from funding_common import observations, change, change_text
from funding_dashboard_ui import enhance

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
DASH = ROOT / "_wiki" / "_dashboards"
OUT = DASH / "credit-monitor.html"

deals = json.loads((DATA / "funding_deals.json").read_text(encoding="utf-8"))
try:
    market = json.loads((DATA / "funding_market.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    market = {"fetched_at": "never", "series": [], "errors": ["funding_market.json missing — run fetch_funding.py"]}

E = H.escape
for series in market.get('series', []):
    series['points'] = observations(series)
    if series['points']:
        series['last_date'], series['last'] = series['points'][-1]
market['series'] = [s for s in market.get('series', []) if s['points']]

# ---------------------------------------------------------------- helpers
def sdate(iso):  # "2026-08-24" -> ordinal days
    return dt.date.fromisoformat(iso).toordinal()

def fmt(v, dec=2):
    return f"{v:,.{dec}f}"

def month_ends(points):
    """last observation of each month -> [(date, val)]"""
    out, cur = [], None
    for d, v in points:
        m = d[:7]
        if cur and cur[0][:7] != m:
            out.append(cur)
        cur = (d, v)
    if cur:
        out.append(cur)
    return out

# ---------------------------------------------------------------- line panel
def line_panel(s, idx):
    pts = s["points"]
    W, HH, ml, mr, mt, mb = 520, 168, 46, 14, 14, 26
    iw, ih = W - ml - mr, HH - mt - mb
    xs = [sdate(p[0]) for p in pts]
    ys = [p[1] for p in pts]
    x0, x1 = min(xs), max(xs)
    lo, hi = min(ys), max(ys)
    pad = (hi - lo) * 0.12 or 0.1
    lo, hi = lo - pad, hi + pad
    def X(x): return ml + (x - x0) / max(1, x1 - x0) * iw
    def Y(y): return mt + (hi - y) / (hi - lo) * ih
    poly = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in zip(xs, ys))
    # y gridlines: 3
    gl = []
    for i in range(3):
        gy = lo + (hi - lo) * (i + 0.5) / 3
        gl.append(f'<line class="grid" x1="{ml}" x2="{W-mr}" y1="{Y(gy):.1f}" y2="{Y(gy):.1f}"/>' \
                  f'<text class="ax" x="{ml-6}" y="{Y(gy)+3:.1f}" text-anchor="end">{fmt(gy, s.get("decimals",2))}</text>')
    # x ticks: ~5 (quarter-ish)
    xt = []
    for i in range(5):
        tx = x0 + (x1 - x0) * i / 4
        d = dt.date.fromordinal(int(tx))
        xt.append(f'<text class="ax" x="{X(tx):.1f}" y="{HH-8}" text-anchor="middle">{d.strftime("%b %y")}</text>')
    last_d, last_v = pts[-1]
    dec = s.get("decimals", 2)
    payload = E(json.dumps({"dates": [p[0] for p in pts], "vals": ys, "unit": s.get("unit",""), "dec": dec,
                            "x0": x0, "x1": x1, "lo": lo, "hi": hi, "ml": ml, "mr": mr, "mt": mt, "mb": mb, "w": W, "h": HH}), quote=True)
    return f"""
<figure class="lpanel">
 <figcaption><b>{E(s['label'])}</b><span class="chart-value num">{fmt(last_v,dec)}<small>{E(s.get('unit',''))}</small></span><span class="chart-source">Bloomberg · {E(s['ticker'])} · {E(last_d)}</span></figcaption>
 <svg viewBox="0 0 {W} {HH}" data-pts="{payload}" role="img" aria-label="{E(s['label'])} daily series, two years">
  {''.join(gl)}
  <line class="axis" x1="{ml}" x2="{W-mr}" y1="{HH-mb}" y2="{HH-mb}"/>
  {''.join(xt)}
  <polyline class="ser1" points="{poly}"/>
  <circle class="ser1d" cx="{X(xs[-1]):.1f}" cy="{Y(ys[-1]):.1f}" r="4"/>
  <line class="cross" x1="0" x2="0" y1="{mt}" y2="{HH-mb}" style="display:none"/>
  <circle class="crossdot" r="4.5" style="display:none"/>
 </svg>
</figure>"""

# ---------------------------------------------------------------- hbar (spread change)
def hbar_chart(block):
    rows = block["rows"]
    W, rh, ml, mr = 560, 34, 236, 64
    HH = rh * len(rows) + 30
    low = min(0, min((r['bp'] for r in rows), default=0)) * 1.15
    high = max(0, max((r['bp'] for r in rows), default=0)) * 1.15
    iw = W - ml - mr
    def X(value): return ml + (value - low) / (high - low or 1) * iw
    bars = []
    for i, r in enumerate(rows):
        y = 10 + i * rh
        bw = max(1, abs(X(r['bp']) - X(0)))
        left = min(X(0), X(r['bp']))
        bars.append(
            f'<text class="lbl" x="{ml-8}" y="{y+17}" text-anchor="end">{E(r["bucket"])}</text>'
            f'<rect class="barfill" x="{left:.1f}" y="{y+4}" width="{bw:.1f}" height="20" rx="4"/>'
            f'<text class="val num" x="{X(max(0,r["bp"]))+7:.1f}" y="{y+18}">{r["bp"]:+g}bp</text>'
            f'<title>{E(r["bucket"])}: {r["bp"]:+g}bp YTD</title>')
        # wrap each row's marks in a group for hover
        bars[-1] = f'<g class="hrow"><rect class="hit" x="0" y="{y}" width="{W}" height="{rh}" fill="transparent"/>{bars[-1]}</g>'
    base = f'<line class="axis" x1="{X(0):.1f}" x2="{X(0):.1f}" y1="6" y2="{HH-16}"/>'
    return f'<svg viewBox="0 0 {W} {HH}" role="img" aria-label="YTD spread change by bucket">{base}{"".join(bars)}</svg>'

# ---------------------------------------------------------------- dot plot (project bonds)
def dot_plot(block):
    rows = block["rows"]
    W, rh, ml, mr = 620, 36, 250, 22
    HH = rh * len(rows) + 44
    xmax = max(15.5, max((r['yield_pct'] for r in rows), default=0) * 1.14)
    iw = W - ml - mr
    def X(v): return ml + v / xmax * iw
    grid, marks = [], []
    for gv in (5, 10, 15):
        grid.append(f'<line class="grid" x1="{X(gv):.1f}" x2="{X(gv):.1f}" y1="8" y2="{HH-30}"/>' \
                    f'<text class="ax" x="{X(gv):.1f}" y="{HH-14}" text-anchor="middle">{gv}%</text>')
    for i, r in enumerate(rows):
        y = 20 + i * rh
        crwv = r["offtaker"].startswith("CRWV")
        cls = "dot-crwv" if crwv else "dot-amzn"
        marks.append(
            f'<g class="hrow"><rect class="hit" x="0" y="{y-14}" width="{W}" height="{rh}" fill="transparent"/>'
            f'<text class="lbl" x="{ml-10}" y="{y+4}" text-anchor="end">{E(r["bond"])} <tspan class="mut2">· {E(r["site"])}</tspan></text>'
            f'<line class="stem" x1="{ml}" x2="{X(r["yield_pct"]):.1f}" y1="{y}" y2="{y}"/>'
            f'<circle class="{cls}" cx="{X(r["yield_pct"]):.1f}" cy="{y}" r="6"/>'
            f'<text class="val num" x="{X(r["yield_pct"])+11:.1f}" y="{y+4}">{r["yield_pct"]}%</text>'
            f'<title>{E(r["bond"])} — {E(r["site"])} — offtaker {E(r["offtaker"])} — yield {r["yield_pct"]}%</title></g>')
    return f'<svg viewBox="0 0 {W} {HH}" role="img" aria-label="Project bond yields by offtaker">{"".join(grid)}{"".join(marks)}</svg>'

# ---------------------------------------------------------------- repricing path
def path_chart(block):
    rows = block["rows"]
    W, HH, ml, mr, mt, mb = 620, 210, 52, 118, 16, 30
    iw, ih = W - ml - mr, HH - mt - mb
    def mx(d): return sdate(d + '-01' if len(d) == 7 else d)
    xmin = min((mx(r['date']) for r in rows), default=dt.date.today().toordinal())
    xmax = max((mx(r['date']) for r in rows), default=xmin)
    ymax = max(620, max((r['spread_bp'] for r in rows), default=0) * 1.18)
    def X(m): return ml + (m - xmin) / max(1, xmax - xmin) * iw
    def Y(v): return mt + (ymax - v) / ymax * ih
    grid = []
    for gv in (ymax / 3, ymax * 2 / 3, ymax):
        grid.append(f'<line class="grid" x1="{ml}" x2="{W-mr}" y1="{Y(gv):.1f}" y2="{Y(gv):.1f}"/>' \
                    f'<text class="ax" x="{ml-6}" y="{Y(gv)+3:.1f}" text-anchor="end">S+{gv:.0f}</text>')
    first, last = dt.date.fromordinal(xmin), dt.date.fromordinal(xmax)
    first_month, last_month = first.year * 12 + first.month - 1, last.year * 12 + last.month - 1
    tick_months = list(range(first_month, last_month + 1, max(1, (last_month - first_month + 5) // 6)))
    if tick_months[-1] != last_month:
        tick_months.append(last_month)
    for month in tick_months:
        tick = dt.date(month // 12, month % 12 + 1, 1)
        m = max(xmin, tick.toordinal())
        label = tick.strftime('%b %y')
        grid.append(f'<text class="ax" x="{X(m):.1f}" y="{HH-8}" text-anchor="middle">{label}</text>')
    crwv = sorted([r for r in rows if r["issuer"] == "CRWV"], key=lambda r: mx(r['date']))
    others = [r for r in rows if r["issuer"] != "CRWV"]
    line = " ".join(f"{X(mx(r['date'])):.1f},{Y(r['spread_bp']):.1f}" for r in crwv)
    marks = [f'<polyline class="ser2" points="{line}"/>']
    for r in crwv:
        x, y = X(mx(r["date"])), Y(r["spread_bp"])
        marks.append(f'<g class="hrow"><circle class="dot-crwv ring" cx="{x:.1f}" cy="{y:.1f}" r="6"/>'
                     f'<text class="val num" x="{x:.1f}" y="{y-11:.1f}" text-anchor="middle">S+{r["spread_bp"]}</text>'
                     f'<title>CRWV {E(r["instrument"])} — S+{r["spread_bp"]} ({E(r["date"])}). {E(r["note"])} [{E(r["source"])}]</title></g>')
    oc = {"IREN": "dot-amzn", "NBIS": "dot-aqua"}
    # dodge right-margin labels vertically: alternate below/above by spread order
    for k, r in enumerate(sorted(others, key=lambda r: r["spread_bp"])):
        x, y = X(mx(r["date"])), Y(r["spread_bp"])
        dy = 16 if k % 2 == 0 else -9
        marks.append(f'<g class="hrow"><circle class="{oc.get(r["issuer"], "dot-aqua")} ring" cx="{x:.1f}" cy="{y:.1f}" r="6"/>'
                     f'<text class="val num" x="{x+10:.1f}" y="{y+dy:.1f}">{E(r["issuer"])} S+{r["spread_bp"]}</text>'
                     f'<title>{E(r["issuer"])} {E(r["instrument"])} — S+{r["spread_bp"]} ({E(r["date"])}). {E(r["note"])} [{E(r["source"])}]</title></g>')
    return f'<svg viewBox="0 0 {W} {HH}" role="img" aria-label="Neocloud loan spreads through 2026">{"".join(grid)}<line class="axis" x1="{ml}" x2="{W-mr}" y1="{HH-mb}" y2="{HH-mb}"/>{"".join(marks)}</svg>'

# ---------------------------------------------------------------- issuance bars
def issuance_chart(iss):
    W, HH, ml, mb = 480, 210, 56, 40
    ih = HH - 24 - mb
    vmax = max(iss["fy26e_high_bn"], iss['ai_related_ytd_bn'], iss['fy25_total_bn'], 1) * 1.12
    def Y(v): return 24 + (1 - v / vmax) * ih
    bars = [("FY2025", iss["fy25_total_bn"], "b250", f"${iss['fy25_total_bn']}bn"),
            ("2026 YTD", iss["ai_related_ytd_bn"], "b450", f"${iss['ai_related_ytd_bn']}bn"),
            ("FY2026E", iss["fy26e_low_bn"], "b200d", f"${iss['fy26e_low_bn']}–{iss['fy26e_high_bn']}bn E")]
    bw, gap = 96, 42
    out = []
    for i, (lbl, v, cls, vl) in enumerate(bars):
        x = ml + i * (bw + gap)
        out.append(f'<g class="hrow"><rect class="{cls}" x="{x}" y="{Y(v):.1f}" width="{bw}" height="{HH-mb-Y(v):.1f}" rx="4"/>')
        if lbl == "FY2026E":
            out.append(f'<rect class="b200r" x="{x}" y="{Y(iss["fy26e_high_bn"]):.1f}" width="{bw}" height="{Y(v)-Y(iss["fy26e_high_bn"]):.1f}" rx="4"/>')
        out.append(f'<text class="val num" x="{x+bw/2}" y="{Y(max(v, iss["fy26e_high_bn"] if lbl=="FY2026E" else v))-7:.1f}" text-anchor="middle">{vl}</text>'
                   f'<text class="lbl" x="{x+bw/2}" y="{HH-18}" text-anchor="middle">{lbl}</text>'
                   f'<title>{lbl}: {vl} AI-related issuance across credit channels (MS tracker 2026-08-20)</title></g>')
    return f'<svg viewBox="0 0 {W} {HH}" role="img" aria-label="AI-related debt issuance">{"".join(out)}<line class="axis" x1="{ml-8}" x2="{W-10}" y1="{HH-mb}" y2="{HH-mb}"/></svg>'

# ---------------------------------------------------------------- assemble pieces
by_ticker = {s["ticker"]: s for s in market.get("series", [])}

def delta_bp(s, days):
    result = change(s, days)
    return result['value'] if result else None

tiles = []
for s in market.get("series", []):
    weekly = change(s, 7)
    monthly = change(s, 30)
    dtxt = ' · '.join(f'{label}: {x["value"]:+.1f} {x["unit"]}' if x else f'{label}: unavailable' for label, x in [('1w', weekly), ('1m', monthly)])
    tiles.append(f'<div class="tile"><div class="tl">{E(s["label"])}</div>'
                 f'<div class="tv num">{fmt(s["last"], s.get("decimals",2))}<span class="tu">{E(s.get("unit",""))}</span></div>'
                 f'<div class="td num" title="1w: {E(change_text(s, 7))}; 1m: {E(change_text(s, 30))}">{dtxt}</div><div class="tile-source">Bloomberg · {E(s["last_date"])}</div></div>')
iss = deals["issuance"]
tiles.append(f'<div class="tile"><div class="tl">AI-related issuance YTD</div>'
             f'<div class="tv num">${iss["ai_related_ytd_bn"]}<span class="tu">bn</span></div>'
             f'<div class="td">vs ${iss["fy25_total_bn"]}bn all of 2025</div><div class="tile-source">MS · 2026-08-20 · historical snapshot</div></div>')

panels = "".join(line_panel(s, i) for i, s in enumerate(market.get("series", [])))

gauge_tbl_rows = ""
if market.get("series"):
    me = {s["ticker"]: dict(month_ends(s["points"])[-13:]) for s in market["series"]}
    all_months = sorted({d for m in me.values() for d in m})[-13:]
    hdr = "".join(f"<th>{E(s['label'])}</th>" for s in market["series"])
    gauge_tbl_rows = "".join(
        "<tr><td class='num'>" + E(d) + "</td>" +
        "".join(f"<td class='num'>{fmt(me[s['ticker']].get(d), s.get('decimals',2)) if me[s['ticker']].get(d) is not None else '—'}</td>"
                for s in market["series"]) + "</tr>"
        for d in all_months)
    gauge_tbl = f"<table><thead><tr><th>Month-end</th>{hdr}</tr></thead><tbody>{gauge_tbl_rows}</tbody></table>"
else:
    gauge_tbl = "<p class='mut'>No market data yet — run fetch_funding.py.</p>"

cat_order = list(dict.fromkeys(["Hyperscaler IG", "Neocloud", "Lab / SPV", "Vendor guarantee"] + [d['category'] for d in deals['deals']]))
ledger_rows = []
for cat in cat_order:
    rows = [d for d in deals["deals"] if d["category"] == cat]
    if not rows:
        continue
    ledger_rows.append(f'<tr class="cat"><td colspan="7">{E(cat)}</td></tr>')
    for d in rows:
        ledger_rows.append(
            f'<tr data-category="{E(cat)}"><td class="num">{E(d["date"])}</td><td><b>{E(d["issuer"])}</b></td>'
            f'<td>{E(d["instrument"])}</td><td class="num">{E(d["size"])}</td>'
            f'<td class="num">{E(d["pricing"])}</td><td>{E(d["counterparty"])}</td>'
            f'<td>{E(d["note"])} <span class="src">[{E(d["source"])}]</span></td></tr>')

STATUS = {"good": ("✓", "OK"), "warning": ("⚠", "Watch"), "serious": ("▲", "Stress"), "critical": ("✖", "Critical"), "gap": ("◌", "Gap")}
score_rows = []
for r in deals["scoreboard"]:
    icon, word = STATUS.get(r["status"], ("•", r["status"]))
    score_rows.append(f'<div class="srow"><span class="chip chip-{E(r["status"])}"><span class="ci">{icon}</span>{word}</span>'
                      f'<div><b>{E(r["signpost"])}.</b> {E(r["read"])} <span class="src">[{E(r["source"])}]</span></div></div>')

watch_rows = "".join(f'<li><b class="num">{E(w["date"])}</b> — {E(w["event"])}</li>' for w in deals["watch"])

rp = deals["repricing_path"]
pb = deals["project_bonds_snapshot"]
sc = deals["spread_change_ytd_bp"]

sc_tbl = "<table><thead><tr><th>Bucket</th><th>YTD Δ (bp)</th></tr></thead><tbody>" + "".join(
    f"<tr><td>{E(r['bucket'])}</td><td class='num'>{r['bp']:+g}</td></tr>" for r in sc["rows"]) + "</tbody></table>"

bonds_note = ("<b>Live bond series slot:</b> `bonds[]` in <code>_data/funding_deals.json</code> is empty by design — "
              "paste Bloomberg tickers or <code>/isin/… Corp</code> rows from SRCH (wishlist inside the file: the six "
              "project bonds, CRWV TL/unsecured, ORCL Feb-26 jumbo, Anthropic SPV A2) and re-run the fetch; "
              "they render here automatically.")

CSS = """
:root{
 --paper:#f9f9f7; --card:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --mut:#898781;
 --grid:#e1e0d9; --axis:#c3c2b7; --line:#e1e0d9; --ring:rgba(11,11,11,.10);
 --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a;
 --b200:#9ec5f4; --b250:#86b6ef; --b450:#2a78d6;
 --good:#0ca30c; --warn:#fab219; --serious:#ec835a; --crit:#d03b3b;
 --shadow:0 1px 2px rgba(11,11,11,.05), 0 8px 24px -18px rgba(11,11,11,.25);
}
@media (prefers-color-scheme: dark){
 :root:not([data-theme="light"]){
  --paper:#0d0d0d; --card:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --mut:#898781;
  --grid:#2c2c2a; --axis:#383835; --line:#2c2c2a; --ring:rgba(255,255,255,.10);
  --s1:#3987e5; --s2:#d95926; --s3:#199e70;
  --b200:#184f95; --b250:#1c5cab; --b450:#3987e5;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -18px rgba(0,0,0,.6);
 }
}
:root[data-theme="dark"]{
 --paper:#0d0d0d; --card:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --mut:#898781;
 --grid:#2c2c2a; --axis:#383835; --line:#2c2c2a; --ring:rgba(255,255,255,.10);
 --s1:#3987e5; --s2:#d95926; --s3:#199e70;
 --b200:#184f95; --b250:#1c5cab; --b450:#3987e5;
 --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -18px rgba(0,0,0,.6);
}
*{box-sizing:border-box;margin:0}
body{background:var(--paper);color:var(--ink);font:14.5px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;padding:0 20px 70px}
.wrap{max-width:1180px;margin:0 auto}
.num{font-variant-numeric:tabular-nums}
a{color:var(--s1)}
header{padding:36px 0 20px;border-bottom:3px solid var(--ink)}
.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);font-weight:600}
h1{font-size:clamp(26px,4vw,38px);line-height:1.1;margin:8px 0 10px}
.dek{max-width:78ch;color:var(--ink2);font-size:15.5px}
.meta{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:12px;font-size:12px;color:var(--mut)}
.meta b{color:var(--ink2)}
section{margin-top:34px}
h2{font-size:19px;margin-bottom:4px}
.sub{color:var(--ink2);font-size:13.5px;margin-bottom:14px;max-width:88ch}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;box-shadow:var(--shadow)}
.tl{font-size:12px;color:var(--ink2);font-weight:600}
.tv{font-size:27px;font-weight:700;margin-top:2px}
.tu{font-size:14px;color:var(--mut);margin-left:2px}
.td{font-size:12px;color:var(--ink2);margin-top:2px}
.mut{color:var(--mut)} .mut2{fill:var(--mut);color:var(--mut)}
.gpanels{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px}
figure.lpanel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px 6px;box-shadow:var(--shadow)}
figure.lpanel figcaption{font-size:12.5px;margin-bottom:2px}
svg{width:100%;height:auto;display:block}
.grid{stroke:var(--grid);stroke-width:1}
.axis{stroke:var(--axis);stroke-width:1}
.ax{fill:var(--mut);font-size:10.5px}
.lbl{fill:var(--ink2);font-size:11.5px}
.val{fill:var(--ink);font-size:11.5px;font-weight:600}
.ser1{fill:none;stroke:var(--s1);stroke-width:2;stroke-linejoin:round}
.ser2{fill:none;stroke:var(--s2);stroke-width:2;stroke-linejoin:round}
.ser1d{fill:var(--s1)}
.stem{stroke:var(--grid);stroke-width:1.5}
.dot-crwv{fill:var(--s2)} .dot-amzn{fill:var(--s1)} .dot-aqua{fill:var(--s3)}
.ring{stroke:var(--card);stroke-width:2}
.barfill{fill:var(--s1)}
.b200{fill:var(--b200)} .b250{fill:var(--b250)} .b450{fill:var(--b450)}
.b200d{fill:var(--b200);stroke:var(--s1);stroke-dasharray:4 3;stroke-width:1.2}
.b200r{fill:var(--b200);opacity:.45}
.hrow .hit{cursor:default}
.hrow:hover circle, .hrow:hover rect.barfill{filter:brightness(1.12)}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2);margin:8px 2px 0}
.legend .sw{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.cross{stroke:var(--mut);stroke-width:1;stroke-dasharray:3 3}
.crossdot{fill:var(--card);stroke:var(--s1);stroke-width:2.5}
#tip{position:fixed;pointer-events:none;background:var(--card);border:1px solid var(--line);border-radius:8px;
 padding:6px 10px;font-size:12px;color:var(--ink);box-shadow:var(--shadow);display:none;z-index:10}
table{border-collapse:collapse;width:100%;font-size:12.8px}
th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);text-align:left;padding:7px 10px;border-bottom:2px solid var(--line)}
td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tr.cat td{font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink2);background:color-mix(in srgb,var(--card) 60%,var(--paper));border-bottom:2px solid var(--line)}
.tscroll{overflow-x:auto}
.src{color:var(--mut);font-size:11.5px}
details{margin-top:10px}
summary{cursor:pointer;color:var(--ink2);font-size:12.5px}
.srow{display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.srow:last-child{border-bottom:0}
.chip{flex:0 0 auto;display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:700;border-radius:99px;padding:2px 10px;border:1px solid var(--ring);color:var(--ink)}
.chip .ci{font-size:12px}
.chip-good .ci{color:var(--good)} .chip-warning .ci{color:var(--warn)} .chip-serious .ci{color:var(--serious)}
.chip-critical .ci{color:var(--crit)} .chip-gap .ci{color:var(--mut)}
ul.watch{list-style:none;padding:0}
ul.watch li{padding:7px 0;border-bottom:1px solid var(--line);font-size:13.5px}
ul.watch li:last-child{border-bottom:0}
footer{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);color:var(--mut);font-size:12.5px}
code{background:color-mix(in srgb,var(--card) 55%,var(--paper));border:1px solid var(--line);border-radius:4px;padding:0 5px;font-size:12px}
.note{font-size:12.5px;color:var(--ink2);margin-top:10px}
"""

JS = """
const tip = document.createElement('div'); tip.id = 'tip'; document.body.appendChild(tip);
function showTip(html, x, y){ tip.innerHTML = html; tip.style.display='block';
  const r = tip.getBoundingClientRect();
  tip.style.left = Math.min(x+14, innerWidth - r.width - 12) + 'px';
  tip.style.top  = Math.max(8, y - r.height - 12) + 'px'; }
function hideTip(){ tip.style.display='none'; }
document.querySelectorAll('figure.lpanel svg').forEach(svg => {
  const cfg = JSON.parse(svg.dataset.pts);
  const cross = svg.querySelector('.cross'), dot = svg.querySelector('.crossdot');
  const n = cfg.dates.length;
  const dayOf = iso => Math.floor(new Date(iso + 'T00:00Z').getTime() / 864e5);
  const d0 = dayOf(cfg.dates[0]), d1 = dayOf(cfg.dates[n-1]);
  const iw = cfg.w - cfg.ml - cfg.mr, ih = cfg.h - cfg.mt - cfg.mb;
  svg.addEventListener('mousemove', ev => {
    const pt = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(svg.getScreenCTM().inverse());
    const frac = Math.min(1, Math.max(0, (pt.x - cfg.ml) / iw));
    const target = d0 + frac * (d1 - d0);
    let lo = 0, hi = n - 1;
    while (hi - lo > 1){ const m = (lo + hi) >> 1; (dayOf(cfg.dates[m]) < target) ? lo = m : hi = m; }
    const i = (target - dayOf(cfg.dates[lo])) < (dayOf(cfg.dates[hi]) - target) ? lo : hi;
    const x = cfg.ml + (dayOf(cfg.dates[i]) - d0) / Math.max(1, d1 - d0) * iw;
    const y = cfg.mt + (cfg.hi - cfg.vals[i]) / (cfg.hi - cfg.lo) * ih;
    cross.setAttribute('x1', x); cross.setAttribute('x2', x); cross.style.display = '';
    dot.setAttribute('cx', x); dot.setAttribute('cy', y); dot.style.display = '';
    showTip('<b>' + cfg.dates[i] + '</b> · ' + cfg.vals[i].toFixed(cfg.dec) + cfg.unit, ev.clientX, ev.clientY);
  });
  svg.addEventListener('mouseleave', () => { cross.style.display='none'; dot.style.display='none'; hideTip(); });
});
document.querySelectorAll('g.hrow').forEach(g => {
  const t = g.querySelector('title');
  if (!t) return;
  const txt = t.textContent; t.remove();
  g.addEventListener('mousemove', ev => showTip(txt, ev.clientX, ev.clientY));
  g.addEventListener('mouseleave', hideTip);
});
"""

hy_bp = fmt(by_ticker.get("LF98OAS Index", {}).get("last", 0) * 100, 0)
ig_bp = fmt(by_ticker.get("LUACOAS Index", {}).get("last", 0) * 100, 0)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Credit &amp; Funding Monitor</title><style>{CSS}</style></head><body>
<div class="wrap">
<header>
 <div class="eyebrow">Capstone · wiki feature dashboard · internal</div>
 <h1>AI Credit &amp; Funding Monitor</h1>
 <p class="dek">Track the cost and availability of capital behind the AI buildout. Compare broad credit conditions with issuer financing, counterparty quality and funding commitments.</p>
 <div class="meta"><span>market data <b>{E(market.get("fetched_at","never")[:16])}</b> (local BBG terminal)</span>
 <span>ledger asof <b>{E(deals["asof"])}</b> (hand-edit: <code>_data/funding_deals.json</code>)</span>
 <span>weekly refresh &amp; email: <b>Friday · 09:00 São Paulo</b></span>
 <span><a href="index.html">← dashboards hub</a></span></div>
</header>

<section>
 <div class="tiles">{''.join(tiles)}</div>
</section>

<section>
 <h2>Market gauges</h2>
 <p class="sub">Daily Bloomberg observations over two years. Weekly and monthly changes use calendar lookbacks with the actual comparison dates available on hover. Rates and OAS changes are in basis points.</p>
 <div class="gpanels">{panels}</div>
 <details class="card"><summary>Data table — last available observation in each month</summary><div class="tscroll">{gauge_tbl}</div></details>
</section>

<section>
 <h2>Where the stress lives — YTD spread change by bucket</h2>
 <p class="sub">{E(sc["takeaway"])} <span class="src">[{E(sc["source"])}]</span></p>
 <div class="card">{hbar_chart(sc)}<details><summary>Data table</summary>{sc_tbl}</details></div>
</section>

<section>
 <h2>Counterparty tiering — same asset, different offtaker</h2>
 <p class="sub">{E(pb["takeaway"])} <span class="src">[{E(pb["source"])}]</span></p>
 <div class="card">{dot_plot(pb)}
 <div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Amazon offtake</span>
 <span><span class="sw" style="background:var(--s2)"></span>CoreWeave offtake</span></div>
 <p class="note">{bonds_note}</p></div>
</section>

<section>
 <h2>Neocloud repricing path</h2>
 <p class="sub">The same borrower repriced S+225 → S+550 in four months while IG-offtaker deals (IREN vs MSFT, and META-offtake CRWV paper) held the tight end. ⚠ The 9.15% secured TL and the ~10% 5yr unsecured (SemiAnalysis 07-06) are different instruments — never chain them.</p>
 <div class="card">{path_chart(rp)}
 <div class="legend"><span><span class="sw" style="background:var(--s2)"></span>CRWV</span>
 <span><span class="sw" style="background:var(--s1)"></span>IREN (MSFT offtake)</span>
 <span><span class="sw" style="background:var(--s3)"></span>NBIS</span></div></div>
</section>

<section>
 <h2>Issuance &amp; absorption</h2>
 <p class="sub">{E(iss["fy26e_note"])}. IG share of supply: 1% (2024) → 7% (2025) → ~18% (2026 YTD) <span class="src">[{E(iss["ig_share_source"])}]</span>. Recent pace: ${iss["monthly_recent"][0]["bn"]}bn {E(iss["monthly_recent"][0]["label"])} + ${iss["monthly_recent"][1]["bn"]}bn {E(iss["monthly_recent"][1]["label"])}. {E(iss["ig_monthly_record"])}.</p>
 <div class="card">{issuance_chart(iss)}
 <p class="note">{E(iss["ai_related_ytd_note"])}</p></div>
</section>

<section>
 <h2>Deal ledger</h2>
 <p class="sub">Attributed financing records · evidence through {E(deals['asof'])}. Announced capacity, guarantees and committed or funded debt are distinct; amounts must not be added together.</p>
 <div class="card tscroll"><table>
 <thead><tr><th>Date</th><th>Issuer</th><th>Instrument</th><th>Size</th><th>Pricing</th><th>Counterparty / offtake</th><th>Note · source</th></tr></thead>
 <tbody>{''.join(ledger_rows)}</tbody></table></div>
</section>

<section>
 <h2>Appetite scoreboard</h2>
 <p class="sub">Research assessment recorded {E(deals['asof'])}. These dated judgments require source review before being treated as current signals.</p>
 <div class="card">{''.join(score_rows)}</div>
</section>

<section>
 <h2>Watch</h2>
 <div class="card"><ul class="watch">{watch_rows}</ul></div>
</section>

<footer>
 Built {dt.date.today().isoformat()} · sources inline per datapoint (MS Global Credit tracker 08-20, MS US Credit 08-14, GS credit 08-03/09, Barclays 08-13/20, SemiAnalysis 07-06, Epoch AI 08-12, NVDA/CRWV filings, BBG local terminal) · origin: internal weekly 2026-08-24, action item #3 (owner: PM) — theme page <code>_wiki/themes/internal-weekly-meeting.md</code> · palette: dataviz reference instance (validated light+dark).
</footer>
</div>
<script>{JS}</script>
</body></html>"""

page = enhance(page, deals, market)
temporary = OUT.with_suffix('.tmp')
temporary.write_text(page, encoding="utf-8")
temporary.replace(OUT)
print(f"credit monitor -> {OUT}  ({len(page)//1024} KB, {len(market.get('series',[]))} live series, {len(deals['deals'])} ledger rows)")
