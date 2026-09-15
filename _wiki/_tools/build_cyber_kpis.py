r"""
FEATURE — Cyber KPI ledger ("the numbers Bloomberg doesn't carry").

Cyber names trade on non-GAAP operating KPIs — net new ARR, NGS ARR, cRPO, NRR,
Flex ARR, module attach, platformized customers — none of which are in BBG
consensus. They live scattered in prose across PANW/CRWD/OKTA pages, so every
preview re-derives them. This renders the hand-curated ledger
_data/cyber_kpis.json (one record per fiscal quarter, every value sourced and
flagged when derived) into one page with:
  - next-print cards: company guide + BBG consensus (live from estimates.json)
    + the buy-side bar + the pre-registered test it feeds
  - cross-company small multiples on a CALENDAR quarter-end axis (fiscal years
    differ: PANW Jul-31, CRWD/OKTA Jan-31; quarter-ends align on Jan/Apr/Jul/Oct)
  - per-company engine chart + full KPI table (hover = source)

Writes _meta/cyber-kpis.md + _dashboards/cyber-kpis.html. Read-only on pages.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_cyber_kpis.py"
"""
import sys, json, html, re, datetime as dt
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import META, DATA, DASH, TODAY, html_head
sys.stdout.reconfigure(encoding="utf-8")

# Categorical slots 1-3 of the wiki dataviz palette (light surface). Validated
# 2026-09-14 with validate_palette.py: adjacent CVD ΔE 9.2, normal ΔE 27.6, all
# checks pass; aqua is <3:1 on the surface → relief rule: direct labels + tables.
PALETTE = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a", 4: "#eda100"}
GRID, AXIS, INK, MUTED = "#e3e7ee", "#9aa3b2", "#1a1f29", "#6b7280"
FLAG_MARK = {"derived": "°", "approx": "≈", "floor": "≥"}


def load():
    led = json.load(open(DATA / "cyber_kpis.json", encoding="utf-8"))
    est = {}
    p = DATA / "estimates.json"
    if p.is_file():
        est = json.load(open(p, encoding="utf-8")).get("companies", {})
    return led, est


def fmt(v, unit):
    if v is None:
        return "—"
    if unit == "$m":
        return f"${v:,.0f}m" if abs(v) >= 100 else f"${v:,.1f}m"
    if unit == "%":
        return f"{v:.1f}%" if abs(v - round(v)) > 0.05 else f"{v:.0f}%"
    if unit == "#":
        return f"{v:,.0f}"
    return str(v)


def tick_fmt(v, unit):
    """Axis ticks: short forms so they never clip the left gutter ($6,000m -> $6bn)."""
    if unit == "$m" and abs(v) >= 1000:
        return f"${v / 1000:g}bn"
    return fmt(v, unit)


def label_ix(n, step):
    """X labels to draw: always the LAST point, then every `step` back — so the final two never collide."""
    return set(range(n - 1, -1, -step))


def flag_mark(flag):
    if not flag:
        return ""
    f = flag.lower()
    for k, m in FLAG_MARK.items():
        if f.startswith(k):
            return m
    return "°"


def cal_label(end):
    d = dt.date.fromisoformat(end)
    return d.strftime("%b-%y")


# ----------------------------------------------------------------- SVG charts
def _yscale(vals, h_top, h_bot, pad_frac=0.12, zero=False):
    vs = [v for v in vals if v is not None]
    if not vs:
        vs = [0, 1]
    lo, hi = min(vs), max(vs)
    if zero:
        lo = min(lo, 0)
    span = (hi - lo) or 1
    lo -= span * pad_frac
    hi += span * pad_frac
    if zero and lo > 0:
        lo = 0

    def y(v):
        return h_bot - (v - lo) / (hi - lo) * (h_bot - h_top)
    return y, lo, hi


def _ticks(lo, hi, n=4):
    span = hi - lo
    raw = span / n
    mag = 10 ** int(f"{raw:e}".split("e")[1])
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 1:
            break
    t0 = (int(lo / step) + (1 if lo > 0 else 0)) * step if lo % step else lo
    t = t0
    out = []
    while t <= hi + 1e-9:
        if t >= lo - 1e-9:
            out.append(round(t, 6))
        t += step
    return out


def svg_lines(series, labels, title, unit, w=390, h=250, note=""):
    """series: [{'name','color','vals':[v|None per label]}]; labels: shared x categories."""
    L, R, T, B = 44, 70, 34, 34
    n = len(labels)
    xs = [L + (w - L - R) * (i / max(n - 1, 1)) for i in range(n)]
    allv = [v for s in series for v in s["vals"]]
    y, lo, hi = _yscale(allv, T, h - B)
    o = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}" '
         f'style="font:11px -apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:100%">']
    o.append(f'<text x="{L}" y="14" fill="{INK}" font-weight="700" font-size="12.5">{html.escape(title)}</text>')
    # legend (always present for >=2 series)
    lx = L
    for s in series:
        o.append(f'<rect x="{lx}" y="21" width="9" height="9" rx="2" fill="{s["color"]}"/>'
                 f'<text x="{lx + 13}" y="29" fill="{MUTED}">{html.escape(s["name"])}</text>')
        lx += 13 + 7 * len(s["name"]) + 14
    for tv in _ticks(lo, hi):
        yy = y(tv)
        o.append(f'<line x1="{L}" x2="{w - R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>'
                 f'<text x="{L - 6}" y="{yy + 4:.1f}" fill="{MUTED}" text-anchor="end">{tick_fmt(tv, unit)}</text>')
    show = label_ix(n, 1 if n <= 8 else 2)
    for i, lab in enumerate(labels):
        if i in show:
            o.append(f'<text x="{xs[i]:.1f}" y="{h - 12}" fill="{MUTED}" text-anchor="middle">{html.escape(lab)}</text>')
    for s in series:
        pts = [(xs[i], y(v), labels[i], v) for i, v in enumerate(s["vals"]) if v is not None]
        # break the line where a value is missing
        seg, segs = [], []
        for i, v in enumerate(s["vals"]):
            if v is None:
                if seg:
                    segs.append(seg); seg = []
            else:
                seg.append((xs[i], y(v)))
        if seg:
            segs.append(seg)
        for sg in segs:
            if len(sg) > 1:
                d = " ".join(f"{x:.1f},{yy:.1f}" for x, yy in sg)
                o.append(f'<polyline points="{d}" fill="none" stroke="{s["color"]}" stroke-width="2" stroke-linejoin="round"/>')
        for x, yy, lab, v in pts:
            o.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4" fill="{s["color"]}" stroke="#fff" stroke-width="2">'
                     f'<title>{html.escape(s["name"])} · {html.escape(lab)}: {fmt(v, unit)}</title></circle>')
        if pts:
            x, yy, lab, v = pts[-1]
            o.append(f'<text x="{x + 7:.1f}" y="{yy + 4:.1f}" fill="{INK}" font-weight="600">{fmt(v, unit)}</text>')
    if note:
        o.append(f'<text x="{L}" y="{h - 1}" fill="{MUTED}" font-size="9.5">{html.escape(note)}</text>')
    o.append("</svg>")
    return "".join(o)


def svg_bars(labels, vals, color, title, unit, w=390, h=250, note=""):
    L, R, T, B = 48, 16, 34, 34
    n = len(labels)
    y, lo, hi = _yscale(vals, T, h - B, zero=True)
    o = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}" '
         f'style="font:11px -apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:100%">']
    o.append(f'<text x="{L}" y="14" fill="{INK}" font-weight="700" font-size="12.5">{html.escape(title)}</text>')
    for tv in _ticks(lo, hi):
        yy = y(tv)
        o.append(f'<line x1="{L}" x2="{w - R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="{GRID}"/>'
                 f'<text x="{L - 6}" y="{yy + 4:.1f}" fill="{MUTED}" text-anchor="end">{tick_fmt(tv, unit)}</text>')
    y0 = y(0)
    o.append(f'<line x1="{L}" x2="{w - R}" y1="{y0:.1f}" y2="{y0:.1f}" stroke="{AXIS}"/>')
    slot = (w - L - R) / max(n, 1)
    bw = max(slot - 2, 4)  # 2px surface gap between adjacent bars
    present = [(i, v) for i, v in enumerate(vals) if v is not None]
    vmax_i = max(present, key=lambda t: t[1])[0] if present else -1
    last_i = present[-1][0] if present else -1
    show = label_ix(n, 1 if n <= 8 else 2)
    for i, (lab, v) in enumerate(zip(labels, vals)):
        x = L + i * slot + 1
        if i in show:
            o.append(f'<text x="{x + bw / 2:.1f}" y="{h - 12}" fill="{MUTED}" text-anchor="middle">{html.escape(lab)}</text>')
        if v is None:
            continue
        top, bot = (y(v), y0) if v >= 0 else (y0, y(v))
        hh = max(bot - top, 1)
        o.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{hh:.1f}" rx="4" fill="{color}">'
                 f'<title>{html.escape(lab)}: {fmt(v, unit)}</title></rect>')
        if v >= 0:  # square off the baseline end (rounded data-end only)
            o.append(f'<rect x="{x:.1f}" y="{max(top, bot - 4):.1f}" width="{bw:.1f}" height="{min(4, hh):.1f}" fill="{color}"/>')
        if i in (vmax_i, last_i):
            o.append(f'<text x="{x + bw / 2:.1f}" y="{top - 5:.1f}" fill="{INK}" text-anchor="middle" font-weight="600">{fmt(v, unit)}</text>')
    if note:
        o.append(f'<text x="{L}" y="{h - 1}" fill="{MUTED}" font-size="9.5">{html.escape(note)}</text>')
    o.append("</svg>")
    return "".join(o)


# ----------------------------------------------------------------- build
def main():
    led, est = load()
    cos = led["companies"]
    order = sorted(cos, key=lambda t: cos[t].get("color_slot", 9))

    # calendar axis = union of quarter-end months across companies, last 10
    ends = sorted({q["end"] for t in order for q in cos[t]["quarters"]})[-10:]
    labels = [cal_label(e) for e in ends]

    def series_for(kpi_by_tk, unit):
        out = []
        for t in order:
            k = kpi_by_tk.get(t) if isinstance(kpi_by_tk, dict) else kpi_by_tk
            if not k:
                continue
            byend = {q["end"]: q["v"].get(k) for q in cos[t]["quarters"]}
            out.append({"name": t, "color": PALETTE[cos[t]["color_slot"]],
                        "vals": [byend.get(e) for e in ends]})
        return out

    cross = [
        ("Revenue growth y/y", "%", "rev_yoy", "Filed revenue where available; PANW Q4 FY26 derived from the FY26 10-K total."),
        ("Recurring-base growth y/y", "%", {"PANW": "ngs_arr_yoy", "CRWD": "arr_yoy", "OKTA": "crpo_yoy"},
         "PANW = NGS ARR incl. CyberArk/Chronosphere from Q3 FY26 (organic +28% in Q2 FY26); CRWD = ending ARR; OKTA = cRPO."),
        ("Net retention", "%", "nrr", "PANW: platformized base only. CRWD/OKTA: dollar-based NRR as filed."),
    ]

    head, foot = html_head("Cyber KPI ledger — PANW · CRWD · OKTA",
                           f"{TODAY.isoformat()} · ledger asof {led['asof']} · hand-curated, every cell sourced · "
                           f"<code>_data/cyber_kpis.json</code>")
    H = [head, """<style>
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px;margin:10px 0 6px}
.card{background:#fff;border:1px solid #dde2ea;border-radius:8px;padding:12px 14px}
.card h3{margin:0 0 6px;font-size:14px}.card .k{color:#6b7280;font-size:11.5px;text-transform:uppercase;letter-spacing:.03em;margin-top:8px}
.card p{margin:2px 0;font-size:13px}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,1fr));gap:12px;margin:8px 0}
.chart{background:#fff;border:1px solid #dde2ea;border-radius:8px;padding:8px 6px 4px;overflow-x:auto}
table.kpi td,table.kpi th{font-size:12px;padding:4px 7px}table.kpi td.r{font-variant-numeric:tabular-nums}
td[title]{cursor:help;border-bottom:1px dotted #9aa3b2}
.fl{color:#8a6d1b;font-weight:700}
.wrap{overflow-x:auto}
</style>"""]
    H.append("<p class='byline'>The KPIs cyber names trade on and Bloomberg consensus does not carry. Values are as filed (10-Q/10-K) "
             "or as stated on the call; <span class='fl'>°</span> = house-derived, <span class='fl'>≈</span> = approximate as stated, "
             "<span class='fl'>≥</span> = company floor (\"more than\"). Hover any cell for its source. Fiscal years: PANW Jul-31, CRWD/OKTA Jan-31; "
             "cross-company charts use the calendar quarter-end.</p>")

    # ---- next-print cards
    H.append("<h2>Next print — guide vs consensus vs the bar</h2><div class='cards'>")
    md_cards = []
    for t in order:
        c = cos[t]; npr = c.get("next_print", {}); e = est.get(t, {})
        per = e.get("periods", {}).get(npr.get("bbg_period_key", "1FQ"), {})
        cons = f"rev ${per.get('rev', 0):,.0f}m · EPS ${per.get('eps', 0):.2f} ({per.get('label', '?')})" if per else "n/a"
        px = f"px ${e.get('px', 0):,.2f} · PT cons ${e.get('pt', {}).get('cons', 0):,.0f}" if e else ""
        guide = c.get("guide", {}).get("items", [""])[0]
        H.append(f"<div class='card'><h3><span style='color:{PALETTE[c['color_slot']]}'>■</span> {t} — {html.escape(npr.get('period', ''))}</h3>"
                 f"<p class='byline'>{html.escape(npr.get('expected', ''))} · {html.escape(px)}</p>"
                 f"<div class='k'>BBG consensus (live)</div><p>{html.escape(cons)}</p>"
                 f"<div class='k'>Company guide</div><p>{html.escape(guide)}</p>"
                 f"<div class='k'>The bar</div><p>{html.escape(npr.get('buyside_bar', ''))}</p>"
                 f"<div class='k'>Scored by</div><p><code>{html.escape(npr.get('pre_registered_test', ''))}</code></p></div>")
        md_cards.append(f"- **{t} — {npr.get('period', '')}** ({npr.get('expected', '')}) · BBG: {cons} · guide: {guide} · bar: {npr.get('buyside_bar', '')}")
    H.append("</div>")

    # ---- cross-company charts
    H.append("<h2>Cross-company — calendar quarter-end axis</h2><div class='charts'>")
    for title, unit, kpi, note in cross:
        H.append(f"<div class='chart'>{svg_lines(series_for(kpi, unit), labels, title, unit, note=note)}</div>")
    H.append("</div>")

    # ---- per company
    md = [f"# Cyber KPI ledger — {TODAY.isoformat()}\n",
          f"_Rendered from `_data/cyber_kpis.json` (asof {led['asof']}) by `_tools/build_cyber_kpis.py`. "
          "° derived · ≈ approximate · ≥ company floor. Sources per cell in the JSON._\n",
          "## Next print\n", *md_cards, ""]
    for t in order:
        c = cos[t]; qs = c["quarters"]; kp = c["kpis"]; col = PALETTE[c["color_slot"]]
        H.append(f"<h2><span style='color:{col}'>■</span> {t} — {html.escape(c['name'])}</h2>")
        eng = c.get("engine_kpi"); rec = c.get("recurring_kpi")
        H.append("<div class='charts'>")
        if eng and eng in kp:
            vals = [q["v"].get(eng) for q in qs]
            flagged = any((q.get("flags") or {}).get(eng) for q in qs)
            note = "° some quarters derived — see table" if flagged else ""
            H.append(f"<div class='chart'>{svg_bars([q['period'].replace(' FY', ' ') for q in qs], vals, col, kp[eng]['label'] + ' (' + kp[eng]['unit'] + ')', kp[eng]['unit'], note=note)}</div>")
        if rec and rec in kp and rec != eng:
            vals = [q["v"].get(rec) for q in qs]
            H.append(f"<div class='chart'>{svg_lines([{'name': c.get('recurring_label', rec), 'color': col, 'vals': vals}], [q['period'].replace(' FY', ' ') for q in qs], kp[rec]['label'] + ' (' + kp[rec]['unit'] + ')', kp[rec]['unit'])}</div>")
        H.append("</div>")
        # KPI table: rows = KPIs, cols = quarters
        used = [k for k in kp if any(q["v"].get(k) is not None for q in qs)]
        H.append("<div class='wrap'><table class='kpi'><thead><tr><th>KPI</th>" + "".join(
            f"<th class='r' title='quarter ended {q['end']} · reported {q['reported']}'>{html.escape(q['period'])}</th>" for q in qs) + "</tr></thead><tbody>")
        md.append(f"## {t} — {c['name']}\n")
        md.append("| KPI | " + " | ".join(q["period"] for q in qs) + " |")
        md.append("|---|" + "--:|" * len(qs))
        for k in used:
            cells, mcells = [], []
            for q in qs:
                v = q["v"].get(k); unit = kp[k]["unit"]
                fl = (q.get("flags") or {}).get(k, ""); mark = flag_mark(fl)
                src = (q.get("src") or {}).get(k, "")
                tip = html.escape((src + (" · " + fl if fl else "")).strip())
                cells.append(f"<td class='r' title=\"{tip}\">{fmt(v, unit)}{('<span class=fl>' + mark + '</span>') if v is not None and mark else ''}</td>")
                mcells.append((fmt(v, unit) + mark) if v is not None else "—")
            H.append(f"<tr><td>{html.escape(kp[k]['label'])} <span class='mut'>({kp[k]['unit']})</span></td>{''.join(cells)}</tr>")
            md.append(f"| {kp[k]['label']} ({kp[k]['unit']}) | " + " | ".join(mcells) + " |")
        H.append("</tbody></table></div>")
        g = c.get("guide", {})
        if g.get("items"):
            H.append(f"<p class='byline'><b>Guide</b> ({html.escape(g.get('as_of', ''))}):</p><ul>" +
                     "".join(f"<li>{html.escape(i)}</li>" for i in g["items"]) + "</ul>")
            md.append(f"\n**Guide** ({g.get('as_of', '')}):\n" + "\n".join(f"- {i}" for i in g["items"]))
        md.append("")

    H.append("<h2>Basis notes</h2><ul>"
             "<li><b>PANW NGS ARR</b> is not disclosed in the 10-Q/10-K text on disk — values are from the calls; Q4 FY26 is derived from the reported +63% y/y and the ~$970m desk NNARR (F4Q26 transcript not on disk). "
             "From Q3 FY26 NGS ARR includes ~$1.6bn of CyberArk + Chronosphere; organic growth was +28% in Q2 FY26 and is unresolved for Q4 FY26 pending the re-segmentation.</li>"
             "<li><b>PANW cRPO proxy</b> = the 10-Q/10-K line 'RPO we expect to recognize as revenue over the next 12 months'.</li>"
             "<li><b>CRWD</b> ending ARR and NNARR are exact from the 10-Q/10-K key-metrics table (thousands → $m); Q4 values derived as FY minus 9M; NRR is disclosed numerically only at fiscal year-end (plus Oct-24).</li>"
             "<li><b>OKTA</b> revenue/cRPO/RPO/NRR/>$100k customers are exact from the 10-Q/10-K; Q4 values derived as FY minus 9M; non-GAAP OM and FCF actuals live in Okta's supplemental commentary, which is not on disk — guides only.</li>"
             "<li>Cross-company 'recurring-base growth' compares three different constructs (NGS ARR / ending ARR / cRPO) — read direction and inflection, not level.</li>"
             "</ul>")
    H.append(foot)
    DASH.mkdir(parents=True, exist_ok=True); META.mkdir(parents=True, exist_ok=True)
    (DASH / "cyber-kpis.html").write_text("\n".join(H), encoding="utf-8")
    (META / "cyber-kpis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    nq = sum(len(cos[t]["quarters"]) for t in order)
    print(f"cyber-kpis: {len(order)} companies, {nq} company-quarters, axis {labels[0]}→{labels[-1]}")
    print(f"  -> {META / 'cyber-kpis.md'}\n  -> {DASH / 'cyber-kpis.html'}")


if __name__ == "__main__":
    main()
