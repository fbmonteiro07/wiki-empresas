"""Financials theme dashboard: AI infrastructure financing (BX, KKR, APO, BLK, OWL).

Question it tests (themes/financials.md, 2026-11-02): is the asset managers' AI-infrastructure financing
becoming recurring fee-paying capital, or a run of episodic, concentrated deals, and how does the market
price the paper they put out?

Reads  _data/financials/ai_financing_registry.json  deal register keyed to the compute-deal timeline IDs
                                                     (hand-curated; reviewed_through = last timeline date read)
       themes/ai-compute-deals.md                    read-only drift check: new dated sections that mention a
                                                     manager after reviewed_through, and IDs no longer present
       _data/credit_workbook.json                    OFFICIAL AI-credit base (Daniel Grozdea's AI_Credit_Live)
       _data/estimates.json                          BBG BEst consensus
Writes _dashboards/fin-ai-financing.html             (feature-script compliant: no wiki page is touched)
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fin_dash_common import fmt_num, fmt_pct, page, shell, table  # noqa: E402

WIKI = Path(__file__).resolve().parents[1]
REG = WIKI / "_data" / "financials" / "ai_financing_registry.json"
TIMELINE = WIKI / "themes" / "ai-compute-deals.md"
CREDIT = WIKI / "_data" / "credit_workbook.json"
EST = WIKI / "_data" / "estimates.json"
OUT = WIKI / "_dashboards" / "fin-ai-financing.html"

MANAGERS = [("BX", "Blackstone"), ("KKR", "KKR"), ("APO", "Apollo"), ("BLK", "BlackRock"), ("OWL", "Blue Owl")]
STAGES = [("proposed", "--st1"), ("announced", "--st2"), ("binding", "--st3"), ("closed", "--st4"),
          ("funded", "--st4"), ("delivered", "--st5")]
STAGE_ORDER = {s: i for i, (s, _) in enumerate(STAGES)}
STAGE_COLOR = dict(STAGES)
MANAGER_RX = re.compile(r"Blackstone|\bBX\b|\bKKR\b|Helix|Apollo|\bAPO\b|Big Sky|BlackRock|\bBLK\b|\bAIP\b|"
                        r"Blue Owl|\bOWL\b|Hyperion|Beignet|Sopa(?:i)?pilla|\bQTS\b|Aligned")
KIND_LABEL = {"footprint": "Footprint", "cost-per-GW": "Cost per GW", "exposure share": "Exposure share",
              "pipeline": "Pipeline", "funding/redemptions": "Funding side / redemptions"}


def clip(text: str, n: int) -> str:
    """Shorten at a word boundary; the full text sits in the row's details."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(",;:(") + " …"


def ref_link(ref: str) -> str:
    if ref.startswith("http"):
        host = re.sub(r"^https?://(www\.)?", "", ref).split("/")[0]
        return f'<a href="{escape(ref)}">{escape(host)}</a>'
    return f"<code>{escape(ref)}</code>"


def drift_check(reg: dict) -> tuple[list[str], list[str]]:
    """Timeline sections dated after the registry review that mention a manager; IDs gone from the timeline."""
    text = TIMELINE.read_text(encoding="utf-8")
    since = reg["reviewed_through"]
    newer = []
    heads = list(re.finditer(r"(?m)^#{2,3} .*$", text))
    for i, h in enumerate(heads):
        md = re.search(r"(20\d\d)[- ](\d\d)[- ](\d\d)", h.group(0))
        if not md:
            continue
        date = "-".join(md.groups())
        if date <= since:
            continue
        body = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        if MANAGER_RX.search(h.group(0) + body):
            newer.append(f"{date}: {h.group(0).lstrip('#').strip()[:140]}")
    missing = sorted({d["deal_id"] for d in reg["deals"] if not d.get("no_timeline_id")
                      and d["deal_id"].split("/")[0] not in text})
    return newer, missing


def main() -> None:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    credit = json.loads(CREDIT.read_text(encoding="utf-8"))
    est = json.loads(EST.read_text(encoding="utf-8"))
    deals = reg["deals"]
    newer, missing = drift_check(reg)
    mounts: list = []

    # ---------------- tiles ----------------
    by_mgr = {t: [d for d in deals if t in d["managers"]] for t, _ in MANAGERS}
    done = [d for d in deals if d["execution"] in ("closed", "funded", "delivered")]
    largest = max((d for d in deals if d.get("amount_usd_bn") and d["amount_basis"] != "target (non-binding MoU)"),
                  key=lambda d: d["amount_usd_bn"])
    bonds = {b["ticker"]: b for b in credit["bonds"] if b.get("section") in ("IG", "HY")}
    linked = {}
    for d in deals:
        for t in d.get("linked_bonds") or []:
            if t in bonds:
                linked[t] = (d, bonds[t])
    face = sum(b["amt_mn"] for _, b in linked.values()) / 1000
    ylds = [b["yld"] for _, b in linked.values() if b.get("yld") is not None]
    tiles = [
        ("Deals on file", f"{len(deals)}", " · ".join(f"{t} {len(v)}" for t, v in by_mgr.items()) +
         " (shared deals count in each)"),
        ("Closed or delivered", f"{len(done)}", f"{sum(d['execution'] == 'binding' for d in deals)} binding, not closed · "
         f"{sum(d['execution'] in ('announced', 'proposed') for d in deals)} announced or proposed"),
        ("Largest single disclosed amount", f"${largest['amount_usd_bn']:,.0f}bn",
         f"{escape(largest['title'][:60])} ({escape(largest['amount_basis'])}); amounts are not summed: bases differ"),
        ("Manager-linked project bonds", f"${face:,.1f}bn",
         f"{len(linked)} bonds issued (Capstone sum of issue sizes) · YTM {min(ylds):.2f}–{max(ylds):.2f}% · workbook {escape(credit.get('values_asof', ''))}"),
    ]
    tile_html = '<div class="fd-tiles">' + "".join(
        f'<div class="fd-tile"><div class="l">{a}</div><div class="v">{b}</div><div class="s">{c}</div></div>'
        for a, b, c in tiles) + "</div>"

    # ---------------- swimlane (server-rendered SVG) ----------------
    def ddate(d):
        return d.get("first_event_date") or d.get("latest_update_date")

    dates = [ddate(d) for d in deals if ddate(d)]
    lo = dt.date.fromisoformat(min(dates)[:7] + "-01")
    hi = dt.date.today().replace(day=1) + dt.timedelta(days=45)
    W, lane_h, left, top = 1100, 54, 96, 24
    H = top + lane_h * len(MANAGERS) + 30

    def xpos(s: str) -> float:
        s = s if len(s) >= 10 else s[:7] + "-15"
        f = (dt.date.fromisoformat(s[:10]) - lo).days / (hi - lo).days
        return left + f * (W - left - 20)

    svg = [f'<svg class="fd-lane" viewBox="0 0 {W} {H}" role="img" aria-label="AI financing deals by manager and date">']
    m = lo
    while m <= hi:
        x = xpos(m.isoformat())
        svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top - 6}" y2="{H - 26}" style="stroke:var(--grid)"/>')
        if m.month in (1, 4, 7, 10):
            svg.append(f'<text x="{x:.1f}" y="{H - 10}" text-anchor="middle">{m.strftime("%b-%y")}</text>')
        m = (m + dt.timedelta(days=32)).replace(day=1)
    for i, (t, name) in enumerate(MANAGERS):
        y = top + i * lane_h + lane_h / 2
        svg.append(f'<line x1="{left}" x2="{W - 20}" y1="{y}" y2="{y}" style="stroke:var(--base)"/>')
        svg.append(f'<text class="ln" x="8" y="{y + 4}">{escape(name)}</text>')
        used: list[float] = []
        for d in sorted(by_mgr[t], key=lambda d: ddate(d) or ""):
            if not ddate(d):
                continue
            x = xpos(ddate(d))
            dy = 0
            while any(abs(x - u[0]) < 12 and u[1] == dy for u in used):
                dy = -dy + (14 if dy <= 0 else 0)
            used.append((x, dy))
            col = STAGE_COLOR.get(d["execution"], "--base")
            hollow = not d.get("first_event_date")
            tip = (f"<b>{escape(d['title'])}</b><div>{escape(d['deal_id'])}</div>"
                   f"<div class='r'><span>Amount</span><span>{escape(d['amount_text'][:160])}</span></div>"
                   f"<div class='r'><span>Basis</span><span>{escape(d['amount_basis'])}</span></div>"
                   f"<div class='r'><span>Stage</span><span>{escape(d['execution'])} · {escape(d['evidence'])}</span></div>"
                   f"<div class='r'><span>Date</span><span>{escape(ddate(d))}{' (latest update; first date not archived)' if hollow else ''}</span></div>")
            style = (f"fill:var(--surf);stroke:var({col});stroke-width:2.5" if hollow
                     else f"fill:var({col});stroke:var(--surf);stroke-width:2")
            svg.append(f'<circle cx="{x:.1f}" cy="{y + dy:.1f}" r="7" style="{style}" data-tip="{escape(tip)}"/>')
    svg.append("</svg>")
    lane_svg = "".join(svg)
    stage_legend = '<div class="fd-legend">' + "".join(
        f'<span><i class="dot" style="background:var({c})"></i>{s}</span>' for s, c in STAGES if s != "funded") + \
        '<span><i class="dot" style="background:var(--base)"></i>unknown</span>' \
        '<span><i class="dot" style="background:var(--surf);border:2px solid var(--st3)"></i>first date not archived</span></div>'

    # ---------------- register table ----------------
    rows = []
    for d in sorted(deals, key=lambda d: (-(STAGE_ORDER.get(d["execution"], -1)), ddate(d) or ""), reverse=False):
        hist = "".join(f"<li>{escape(h['date'])}: {escape(h['event'])} <small>({escape(h['source'])})</small></li>"
                       for h in d.get("history", []))
        srcs = " · ".join(f"{escape(s['label'])} {ref_link(s['ref'])}" for s in d.get("sources", [])[:5])
        col = STAGE_COLOR.get(d["execution"], "--base")
        tags = " ".join(d["managers"])
        rows.append(
            f'<tr data-tags="{tags}">'
            f'<td class="txt"><b>{escape(d["title"])}</b><br><small>{escape(d["deal_id"])}'
            f'{" · not a timeline ID" if d.get("no_timeline_id") else ""}</small></td>'
            f'<td class="txt">{", ".join(d["managers"])}<br><small>{escape(clip(d["role"], 120))}</small></td>'
            f'<td class="txt">{escape(clip(d["amount_text"], 200))}<br><small>Basis: {escape(d["amount_basis"])}</small></td>'
            f'<td class="txt">{escape(clip(d["capacity_text"], 110))}<br><small>Basis: {escape(d["capacity_basis"])}</small></td>'
            f'<td class="txt"><span class="fd-stage" style="background:var({col})"></span>{escape(d["execution"])}<br>'
            f'<small>{escape(d["evidence"])}<br>{escape(d.get("first_event_date") or "n.d.")} → {escape(d.get("latest_update_date") or "")}</small></td>'
            f'<td class="txt wide">{escape(d["status_note"])}'
            f'<details><summary>Counterparty, history ({len(d.get("history", []))}) and sources</summary>'
            f'<p><b>Counterparty:</b> {escape(d["counterparty"])}<br><b>Tenant / offtaker:</b> {escape(d["tenant_or_offtaker"])}<br>'
            f'<b>Role:</b> {escape(d["role"])}<br><b>Amount:</b> {escape(d["amount_text"])}<br><b>Capacity:</b> {escape(d["capacity_text"])}</p>'
            f'<ul>{hist}</ul><p>{srcs}</p></details></td></tr>')
    chips = '<div class="fd-chips"><button data-filter="all" data-target="t-register" aria-pressed="true">All</button>' + "".join(
        f'<button data-filter="{t}" data-target="t-register" aria-pressed="false">{n} ({len(by_mgr[t])})</button>' for t, n in MANAGERS) + "</div>"
    register = ('<div class="fd-scroll"><table class="fd-t fd-reg" id="t-register"><thead><tr><th>Deal</th><th>Manager · role</th>'
                '<th>Amount (as stated)</th><th>Capacity</th><th>Stage</th><th>Where it stands</th>'
                '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")

    # ---------------- market marks (official credit workbook) ----------------
    ig_hy = sorted([b for b in bonds.values() if b.get("yld") is not None], key=lambda b: b["yld"])
    bars = []
    bw, rowh = 1100, 22
    maxy = max(b["yld"] for b in ig_hy)
    for i, b in enumerate(ig_hy):
        y = 6 + i * rowh
        hit = b["ticker"] in linked
        col = "--fs1" if hit else "--base"
        wpx = (b["yld"] / (maxy * 1.08)) * (bw - 360)
        mgr = ", ".join(linked[b["ticker"]][0]["managers"]) if hit else ""
        tip = (f"<b>{escape(b['name'])}</b><div class='r'><span>YTM</span><span>{b['yld']:.2f}%</span></div>"
               f"<div class='r'><span>Price</span><span>{b['px']:.2f}</span></div>"
               f"<div class='r'><span>Tenant</span><span>{escape(b.get('tenant') or '')}</span></div>"
               f"<div class='r'><span>Section</span><span>{escape(b['section'])}</span></div>")
        bars.append(f'<g data-tip="{escape(tip)}"><rect x="0" y="{y}" width="{bw}" height="{rowh}" fill="transparent"/>'
                    f'<text x="0" y="{y + 15}" style="fill:var({"--ink" if hit else "--muted"});font-weight:{650 if hit else 400}">'
                    f'{escape(b["ticker"])}{" · " + mgr if mgr else ""}</text>'
                    f'<text x="120" y="{y + 15}">{escape((b.get("tenant") or "")[:24])}</text>'
                    f'<rect x="300" y="{y + 5}" width="{wpx:.1f}" height="12" rx="4" style="fill:var({col})"/>'
                    f'<text x="{306 + wpx:.1f}" y="{y + 15}" style="fill:var(--ink2)">{b["yld"]:.2f}% · {escape(b["section"])}</text></g>')
    bar_svg = (f'<svg class="fd-lane" viewBox="0 0 {bw} {8 + rowh * len(ig_hy)}" role="img" '
               f'aria-label="Project bond yields">' + "".join(bars) + "</svg>")
    mrows = []
    for t, (d, b) in sorted(linked.items(), key=lambda kv: -kv[1][1]["amt_mn"]):
        mrows.append([f"<b>{t}</b>", f'<td class="txt">{escape(b["name"])}<br><small>{escape(d["registry_key"])} · '
                      f'{", ".join(d["managers"])}</small></td>', escape(b.get("tenant") or ""), escape(b.get("rating") or ""),
                      f"${b['amt_mn'] / 1000:,.1f}bn", f"{b['px']:.2f}", f"{b['yld']:.2f}%",
                      fmt_num(b.get("oas_bp"), 0), f'{fmt_num(b.get("pickup_bp"), 0)}<br><small>vs {escape(b.get("comp_name") or "")}</small>',
                      fmt_num(b.get("dyld_since_sep_bp"), 0), escape(b.get("barclays_rec") or "–"),
                      fmt_num(b.get("mw"), 0)])
    marks_table = table(["Ticker", "Bond", "Tenant", "Rating", "Issue size", "Price", "YTM", "OAS (bp)",
                         "Pickup vs tenant bond (bp)", "Δ yield since 15-Sep (bp)", "Barclays", "MW*"], mrows)

    # ---------------- manager context ----------------
    ctx_rows = []
    for kind, label in KIND_LABEL.items():
        items = [c for c in reg["manager_context"] if c["kind"] == kind]
        if not items:
            continue
        ctx_rows.append(f'<tr class="grp"><td colspan="4">{escape(label)}</td></tr>')
        for c in sorted(items, key=lambda c: (c["manager"], c["date"])):
            ctx_rows.append(f'<tr data-tags="{c["manager"]}"><td>{escape(c["manager"])}</td><td>{escape(c["date"])}</td>'
                            f'<td class="txt">{escape(c["statement"])}</td><td class="txt"><small>{escape(c["source"])}</small></td></tr>')
    ctx_chips = '<div class="fd-chips"><button data-filter="all" data-target="t-ctx" aria-pressed="true">All</button>' + "".join(
        f'<button data-filter="{t}" data-target="t-ctx" aria-pressed="false">{n}</button>' for t, n in MANAGERS) + "</div>"
    ctx_table = ('<div class="fd-scroll"><table class="fd-t" id="t-ctx"><thead><tr><th>Manager</th><th>Date</th><th>Statement</th>'
                 '<th>Source</th></tr></thead><tbody>' + "".join(ctx_rows) + "</tbody></table></div>")

    # ---------------- consensus ----------------
    crows = []
    for t, name in MANAGERS:
        c = est["companies"].get(t)
        if not c:
            continue
        p, pt = c["periods"], c["pt"]
        up = 100 * (pt["cons"] / c["px"] - 1) if pt.get("cons") and c.get("px") else None
        crows.append([f'<a href="../index.html#{t}">{t}</a>', escape(name), f"${c['px']:,.2f}", f"${pt['cons']:,.1f}", fmt_pct(up, 1),
                      f"{int(pt.get('buy', 0))} / {int(pt.get('hold', 0))} / {int(pt.get('sell', 0))}",
                      f"{escape(p['1FQ']['label'])}: ${p['1FQ']['eps']:.2f}", f"${p['1FY']['eps']:.2f}", f"${p['2FY']['eps']:.2f}",
                      fmt_num(c["px"] / p["1FY"]["eps"], 1, "x"), fmt_num(c["px"] / p["2FY"]["eps"], 1, "x")])
    cons_table = table(["Ticker", "Manager", "Price", "Mean PT", "Upside", "Buy / Hold / Sell", "Next quarter EPS",
                        "FY1 EPS", "FY2 EPS", "P/E FY1", "P/E FY2"], crows)

    # ---------------- method ----------------
    oq = "".join(f"<li>{escape(q)}</li>" for q in reg["open_questions"])
    rej = "".join(f"<li><code>{escape(r['deal_id'])}</code>: {escape(r['reason'])}</li>" for r in reg["rejected_ids"])
    drift = ""
    if newer or missing:
        drift = ('<div class="fd-callout warn"><b>Registry needs a review</b><br>'
                 + "".join(f"Timeline entry after {escape(reg['reviewed_through'])} mentioning a manager: {escape(n)}<br>" for n in newer)
                 + "".join(f"Deal ID no longer found in the timeline: <code>{escape(i)}</code><br>" for i in missing) + "</div>")
    else:
        drift = (f'<div class="fd-callout">Registry is current with the compute-deal timeline: no dated entry after '
                 f'{escape(reg["reviewed_through"])} mentions a manager, and every timeline ID is still present.</div>')

    groups_nav = [("Financing", [("overview", "Overview"), ("map", "Deal map"), ("register", "Deal register")]),
                  ("Market", [("marks", "Bond marks"), ("voices", "What managers say"), ("consensus", "Consensus")]),
                  ("Research", [("method", "Open questions & method")])]
    body = shell("AI infrastructure financing", "RESEARCH / FINANCIALS / ASSET MANAGERS", "Registry reviewed through",
                 f"{reg['reviewed_through']} · bonds {credit.get('values_asof', '')}", groups_nav,
                 ("Financials · asset managers", "BX · KKR · APO · BLK · OWL"))
    body += f"""
{drift if newer or missing else ''}
<section id="overview"><p class="oc-kicker">Financials theme · asset managers</p>
<h2>AI infrastructure financing: platforms, project bonds and chip leases</h2>
<p class="fd-main-q">Blackstone, KKR, Apollo, BlackRock and Blue Owl now sit on both sides of the AI build-out: they own data-center platforms, lead chip and GPU financings, and sponsor the joint ventures behind Meta's campuses. The debate on the <a href="../index.html#TH-financials">Financials theme</a> is whether this becomes recurring, fee-paying capital or a run of episodic, concentrated deals. This page keeps each deal on its stated basis, keyed to the <a href="../index.html#TH-ai-compute-deals">compute-deal timeline</a> IDs, next to how the market prices the managers' project bonds in the official AI-credit workbook.</p>
{tile_html}
</section>
<section id="map"><h2>Deal map</h2>
<p class="sub">One dot per deal and manager, at its first archived event date, coloured by execution stage (proposed → delivered). Shared deals appear in each manager's lane. Hover for the amount on its stated basis. Dot size is uniform on purpose: EV, facility size, development cost and commitment ceilings are not comparable quantities.</p>
<div class="fd-card">{stage_legend}<div class="fd-scroll">{lane_svg}</div></div></section>
<section id="register"><h2>Deal register</h2>
<p class="sub">Amounts and capacity are quoted as the source states them, with their basis. Evidence (press-reported, company-announced, filed) is kept apart from execution (binding, closed, delivered). Rows without a timeline ID are manager-linked financings the timeline does not carry as compute deals, such as the Meta joint-venture bonds.</p>
<div class="fd-card">{chips}{register}</div></section>
<section id="marks"><h2>Bond marks</h2>
<p class="sub">Live marks from the official AI-credit workbook (Daniel Grozdea's AI_Credit_Live, Bloomberg values as of {escape(credit.get('values_asof', ''))}). Bases follow the workbook: price in points, yield = YTM %, OAS in bp, pickup = bond OAS minus the tenant's comparable bond OAS. Change since 15-Sep compares live YTM with Barclays' 15-Sep YTW, so it is approximate.</p>
<div class="fd-card"><h3>Yield to maturity, all IG and HY data-center project bonds in the workbook</h3><p class="fd-sub">Manager-linked bonds in blue; the rest of the workbook universe in grey for context.</p><div class="fd-scroll">{bar_svg}</div></div>
<div class="fd-card"><h3>The managers' bonds</h3>{marks_table}<p class="fd-src">*MW is the workbook's seed critical-IT figure, unverified and not comparable with Meta's "1 GW" or Blue Owl's GW statements.</p></div>
</section>
<section id="voices"><h2>What the managers say</h2>
<p class="sub">Footprint, cost per GW, exposure, pipeline and the funding side, as stated on calls and in filings. GW statements carry no stated basis (facility vs IT load) and are never added up.</p>
<div class="fd-card">{ctx_chips}{ctx_table}</div></section>
<section id="consensus"><h2>Consensus</h2>
<p class="sub">Bloomberg BEst as of {escape(est['asof'])} (local terminal). Bloomberg's EPS for the alternative managers follows its own adjusted basis, not the companies' FRE / DE / ANI definitions. KKR and Apollo had not reported Q3 at the cut-off (Apollo November 3, KKR November 9), so their next quarter is Q3-26E. Attributed broker views are on the company pages.</p>
<div class="fd-card">{cons_table}</div></section>
<section id="method"><h2>Open questions &amp; method</h2>
{drift}
<div class="fd-card"><h3>Open questions and conflicts ({len(reg['open_questions'])})</h3><ol class="fd-sub">{oq}</ol></div>
<div class="fd-card"><h3>Timeline IDs reviewed and left out ({len(reg['rejected_ids'])})</h3><ul class="fd-sub">{rej}</ul></div>
<div class="fd-card"><p class="fd-sub">{escape(reg.get('note', ''))}</p>
<p class="fd-sub"><b>Refresh</b>: the register is hand-curated in <code>_data/financials/ai_financing_registry.json</code> (fold new timeline entries in and move <code>reviewed_through</code>); <code>build_fin_ai_financing.py</code> runs in the 18:15 chain, re-reads the credit workbook and flags timeline entries the register has not absorbed.</p></div>
</section>"""
    html = page("AI infrastructure financing", "Asset managers' AI-infrastructure deals on their stated bases, "
                "with project-bond marks from the official AI-credit workbook", body, mounts)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(WIKI)} ({len(html) / 1024:.0f} KB) · {len(deals)} deals · {len(linked)} linked bonds")
    print("drift:", newer or "none", "| missing IDs:", missing or "none")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
