"""Financials theme dashboard: Exchange volumes (CME, ICE, CBOE, NDAQ).

Question it tests (themes/financials.md, 2026-11-02): is 2026's exchange volume structural hedging
demand or a volatility spike, and are the listed-options exchanges keeping share?

Reads  _data/financials/exchange_volumes.json   (fetch_exchange_volumes.py: OCC, Cboe xlsx, CME and
                                                 ICE monthly releases, Cboe VIX/OVX history)
       _data/estimates.json                      (BBG BEst consensus, local terminal)
Writes _dashboards/fin-exchanges.html            (feature-script compliant: no wiki page is touched)
"""
from __future__ import annotations

import datetime as dt
import json
import math
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fin_dash_common import fmt_num, fmt_pct, heat_style, legend, page, shell, table  # noqa: E402

WIKI = Path(__file__).resolve().parents[1]
DATA = WIKI / "_data" / "financials" / "exchange_volumes.json"
EST = WIKI / "_data" / "estimates.json"
OUT = WIKI / "_dashboards" / "fin-exchanges.html"

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# NYSE full-day closures (US listed options follow the same calendar); checked against Cboe's own
# trading-day counts wherever the Cboe file covers the month
NYSE_HOLIDAYS = {
    "2023": ["01-02", "01-16", "02-20", "04-07", "05-29", "06-19", "07-04", "09-04", "11-23", "12-25"],
    "2024": ["01-01", "01-15", "02-19", "03-29", "05-27", "06-19", "07-04", "09-02", "11-28", "12-25"],
    "2025": ["01-01", "01-09", "01-20", "02-17", "04-18", "05-26", "06-19", "07-04", "09-01", "11-27", "12-25"],
    "2026": ["01-01", "01-19", "02-16", "04-03", "05-25", "06-19", "07-03", "09-07", "11-26", "12-25"],
}
TICKERS = [("CME", "CME Group", "--fs1"), ("ICE", "Intercontinental Exchange", "--fs2"),
           ("CBOE", "Cboe Global Markets", "--fs3"), ("NDAQ", "Nasdaq", "--fs4")]


def lab(key: str) -> str:
    return f"{MON[int(key[5:]) - 1]}-{key[2:4]}"


def prior(key: str) -> str:
    return f"{int(key[:4]) - 1}{key[4:]}"


def trading_days(key: str, cboe_days: float | None) -> int | None:
    y, m = int(key[:4]), int(key[5:])
    if cboe_days:
        return int(cboe_days)
    hol = NYSE_HOLIDAYS.get(str(y))
    if hol is None:
        return None
    d, n = dt.date(y, m, 1), 0
    while d.month == m:
        if d.weekday() < 5 and d.strftime("%m-%d") not in hol:
            n += 1
        d += dt.timedelta(days=1)
    return n


def yoy(cur, prev):
    if cur is None or not prev:
        return None
    return round(100 * (cur / prev - 1), 1)


def corr(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pts) < 6:
        return None, len(pts)
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    sxy = sum((x - mx) * (y - my) for x, y in pts)
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    syy = sum((y - my) ** 2 for _, y in pts)
    return (round(sxy / math.sqrt(sxx * syy), 2) if sxx and syy else None), len(pts)


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    est = json.loads(EST.read_text(encoding="utf-8"))
    occ, cboe, cme, ice, vol = (d[k]["months"] for k in ("occ", "cboe", "cme", "ice", "vol"))
    allm = sorted(set(occ) | set(cme) | set(ice) | set(cboe))
    span = [k for k in allm if k >= "2024-01"]
    xs = [lab(k) for k in span]

    # --- derived monthly series (Capstone arithmetic where flagged) ---
    days_check = []
    occ_adv = {}
    for k, r in occ.items():
        cd = cboe.get(k, {}).get("days_us")
        td = trading_days(k, cd)
        calc_td = trading_days(k, None)
        if cd and calc_td and int(cd) != calc_td:
            days_check.append(f"{k}: Cboe {int(cd)} vs calendar {calc_td}")
        if td:
            occ_adv[k] = r["total"] / td / 1e6
    occ_yoy = {k: yoy(v, occ_adv.get(prior(k))) for k, v in occ_adv.items()}
    cme_yoy = {k: r.get("yoy") for k, r in cme.items()}
    ice_yoy = {k: (r.get("total") or {}).get("adv_yoy") for k, r in ice.items()}
    cboe_idx_yoy = {k: yoy(r.get("adv_index_k"), cboe.get(prior(k), {}).get("adv_index_k")) for k, r in cboe.items()}
    vix = {k: v.get("vix_avg") for k, v in vol.items()}
    ovx = {k: v.get("ovx_avg") for k, v in vol.items()}
    vix_yoy = {k: yoy(v, vix.get(prior(k))) for k, v in vix.items()}
    ovx_yoy = {k: yoy(v, ovx.get(prior(k))) for k, v in ovx.items()}

    latest = {"CME": max(cme), "ICE": max(ice), "CBOE": max(cboe), "OCC": max(occ)}
    mounts = []

    # ---------------- overview ----------------
    lc, li, lb, lo = latest["CME"], latest["ICE"], latest["CBOE"], latest["OCC"]
    c_rec, i_rec, b_rec, o_rec = cme[lc], ice[li], cboe[lb], occ[lo]
    o_prev = occ.get(prior(lo))
    tiles = [
        ("CME total ADV · " + lab(lc), f"{c_rec['adv_m']:.1f}m",
         f"{fmt_pct(c_rec.get('yoy'), 0, c_rec.get('yoy_calc'))} y/y · CME release {c_rec['date']}"),
        ("ICE total ADV · " + lab(li), fmt_pct((i_rec.get("total") or {}).get("adv_yoy")) + " y/y",
         f"OI {fmt_pct((i_rec.get('total') or {}).get('oi_yoy'))} y/y · ICE release {i_rec.get('date') or ''} (y/y only)"),
        ("Cboe index options ADV · " + lab(lb), f"{b_rec['adv_index_k'] / 1000:.2f}m",
         f"{fmt_pct(cboe_idx_yoy.get(lb), 1)} y/y · SPX {b_rec.get('adv_spx_k', 0) / 1000:.2f}m · Cboe data sheet"),
        ("US listed options · " + lab(lo), f"{occ_adv[lo]:.1f}m/day",
         f"{fmt_pct(occ_yoy.get(lo), 1)} y/y · {o_rec['total'] / 1e6:,.0f}m contracts cleared (OCC)"),
    ]
    tile_html = '<div class="fd-tiles">' + "".join(
        f'<div class="fd-tile"><div class="l">{escape(a)}</div><div class="v">{b}</div><div class="s">{c}</div></div>'
        for a, b, c in tiles) + "</div>"

    series_g = [
        {"name": "CME total ADV", "short": "CME", "color": "--fs1", "vals": [cme_yoy.get(k) for k in span],
         "notes": ["(calc)" if cme.get(k, {}).get("yoy_calc") else "" for k in span]},
        {"name": "ICE total ADV", "short": "ICE", "color": "--fs2", "vals": [ice_yoy.get(k) for k in span],
         "notes": ["" if ice_yoy.get(k) is not None else "(not disclosed)" for k in span]},
        {"name": "Cboe index options ADV", "short": "Cboe idx", "color": "--fs3", "vals": [cboe_idx_yoy.get(k) for k in span]},
        {"name": "US listed options ADV (OCC)", "short": "OCC", "color": "--fs4", "vals": [occ_yoy.get(k) for k in span]},
    ]
    mounts.append(("ch-growth", "line", {"xs": xs, "series": series_g, "yf": "pct", "zero": True, "height": 300,
                                          "label": "Year-on-year volume growth by exchange"}))
    mounts.append(("ch-vix", "line", {"xs": xs, "height": 150, "series": [
        {"name": "VIX monthly average", "color": "--fs1", "vals": [vix.get(k) for k in span]},
        {"name": "OVX monthly average", "color": "--fs2", "vals": [ovx.get(k) for k in span]}],
        "label": "VIX and OVX monthly averages"}))

    # growth vs volatility scatters
    def scat(ser, volser, name):
        groups, xsv, ysv = [], [], []
        for yr, col in (("2024", "--fs1"), ("2025", "--fs2"), ("2026", "--fs3")):
            pts = []
            for k in span:
                if k[:4] == yr and ser.get(k) is not None and volser.get(k) is not None:
                    pts.append({"x": volser[k], "y": ser[k], "label": f"{name} · {lab(k)}"})
                    xsv.append(volser[k]); ysv.append(ser[k])
            if pts:
                groups.append({"name": yr, "color": col, "pts": pts})
        return groups, corr(xsv, ysv)

    sc_cme, r_cme = scat(cme_yoy, vix_yoy, "CME")
    sc_cboe, r_cboe = scat(cboe_idx_yoy, vix_yoy, "Cboe index options")
    sc_ice, r_ice = scat(ice_yoy, ovx_yoy, "ICE")
    for cid, groups, xname in (("sc-cme", sc_cme, "VIX avg y/y"), ("sc-cboe", sc_cboe, "VIX avg y/y"),
                               ("sc-ice", sc_ice, "OVX avg y/y")):
        mounts.append((cid, "scatter", {"groups": groups, "xf": "pct", "yf": "pct", "xname": xname,
                                         "yname": "ADV y/y", "xlabel": xname + " (x) vs ADV y/y (y)", "height": 250}))

    def rtext(r):
        return "n/a" if r[0] is None else f"r = {r[0]:+.2f} across {r[1]} months"

    # growth table view
    gt_rows = []
    for k in span[::-1][:18]:
        gt_rows.append([lab(k), fmt_pct(cme_yoy.get(k), 0, cme.get(k, {}).get("yoy_calc")), fmt_pct(ice_yoy.get(k)),
                        fmt_pct(cboe_idx_yoy.get(k), 1), fmt_pct(occ_yoy.get(k), 1), fmt_num(vix.get(k)), fmt_num(ovx.get(k))])
    growth_table = table(["Month", "CME ADV", "ICE ADV", "Cboe index opt.", "US options (OCC)", "VIX avg", "OVX avg"], gt_rows)

    # quarter-to-date tracker
    today = dt.date.today()
    q = (today.month - 1) // 3
    qm = [f"{today.year}-{3 * q + i:02d}" for i in (1, 2, 3)]
    if not any(k in occ for k in qm):
        q = q - 1 if q else 3
    qtd_rows = []
    qmonths = [f"{today.year if q < 4 else today.year - 1}-{3 * (q % 4) + i:02d}" for i in (1, 2, 3)]

    def qtd(series_months: dict, field, months):
        have = [m for m in months if m in series_months and field(series_months[m]) is not None]
        if not have:
            return None, []
        cur = sum(field(series_months[m]) for m in have) / len(have)
        prev = [field(series_months[prior(m)]) for m in have if prior(m) in series_months]
        return (yoy(cur, sum(prev) / len(prev)) if len(prev) == len(have) else None), have

    for name, sm, fld in (("CME total ADV", cme, lambda r: r.get("adv_m")),
                          ("Cboe index options ADV", cboe, lambda r: r.get("adv_index_k")),
                          ("US listed options ADV (OCC)", {k: {"v": v} for k, v in occ_adv.items()}, lambda r: r["v"])):
        g, have = qtd(sm, fld, qmonths)
        qtd_rows.append([name, ", ".join(lab(m) for m in have) or "no month published yet",
                         fmt_pct(g, 1) if have else "n.d.", "simple average of monthly ADV vs the same months a year earlier"])
    ice_q = [ice_yoy.get(m) for m in qmonths if m in ice]
    qtd_rows.append(["ICE total ADV", ", ".join(lab(m) for m in qmonths if m in ice) or "no month published yet",
                     ", ".join(fmt_pct(v) for v in ice_q) or "n.d.", "ICE gives monthly y/y only; not averaged"])
    qlabel = f"Q{(q % 4) + 1}-{qmonths[0][2:4]}"

    # ---------------- CME ----------------
    cme_span = [k for k in span if k in cme]
    mounts.append(("ch-cme-adv", "bars", {"xs": [lab(k) for k in cme_span], "vals": [cme[k].get("adv_m") for k in cme_span],
                                           "color": "--fs1", "name": "Total ADV (m contracts)", "height": 240,
                                           "notes": [f"y/y {fmt_pct(cme[k].get('yoy'), 0)}{' (Capstone calc)' if cme[k].get('yoy_calc') else ' (CME)'}"
                                                     if cme[k].get('yoy') is not None else "" for k in cme_span]}))
    assets = ["Interest Rate", "Equity Index", "Energy", "Agricultural", "Foreign Exchange", "Metals", "Cryptocurrency", "International"]
    last13 = cme_span[-13:]
    heat_rows = []
    for a in assets:
        row = [a]
        for k in last13:
            x = cme[k].get("assets", {}).get(a)
            if not x:
                row.append('<td class="nd">–</td>')
                continue
            v = x.get("yoy")
            cell = f"{x['adv_m']:.1f}m" if x["adv_m"] >= 1 else f"{x['adv_m'] * 1000:.0f}k"
            row.append(f'<td{heat_style(v)} title="ADV {cell}">{fmt_pct(v, 0, x.get("yoy_calc"))}<br><small>{cell}</small></td>')
        heat_rows.append(row)
    heat_rows.append(["<b>Total</b>"] + [f'<td{heat_style(cme[k].get("yoy"))}><b>{fmt_pct(cme[k].get("yoy"), 0, cme[k].get("yoy_calc"))}</b><br><small>{cme[k]["adv_m"]:.1f}m</small></td>' for k in last13])
    cme_heat = table(["Asset class"] + [lab(k) for k in last13], heat_rows)
    coll = [(k, cme[k]["collateral"]) for k in cme_span if cme[k].get("collateral")]
    mounts.append(("ch-cme-coll", "line", {"xs": [c["period_end"][:3] + "-" + c["period_end"][-2:] for _, c in coll], "height": 220, "series": [
        {"name": "Cash collateral ($bn)", "color": "--fs1", "vals": [c["cash_bn"] for _, c in coll]},
        {"name": "Non-cash collateral ($bn)", "color": "--fs2", "vals": [c["noncash_bn"] for _, c in coll]}],
        "label": "CME customer collateral balances"}))
    bt = [(k, cme[k]) for k in cme_span if cme[k].get("brokertec_adnv_bn")]
    mounts.append(("ch-cme-bt", "bars", {"xs": [lab(k) for k, _ in bt], "vals": [r["brokertec_adnv_bn"] for _, r in bt],
                                          "color": "--fs3", "name": "BrokerTec ADNV ($bn)", "height": 220,
                                          "notes": [f"y/y {fmt_pct(r.get('brokertec_yoy'))}" for _, r in bt]}))

    # ---------------- ICE ----------------
    ice_span = [k for k in span if k in ice]
    mounts.append(("ch-ice-tot", "bars", {"xs": [lab(k) for k in ice_span], "vals": [ice_yoy.get(k) for k in ice_span],
                                           "signed": True, "name": "Total ADV y/y", "yf": "pct", "height": 230,
                                           "notes": ["ICE release did not give a total-ADV line" if ice_yoy.get(k) is None else
                                                     f"OI {fmt_pct((ice[k].get('total') or {}).get('oi_yoy'))} y/y" for k in ice_span]}))
    ice_lines = ["Energy", "Oil", "Brent", "Natural Gas", "TTF Gas", "Agriculture & Metals", "Financials",
                 "Interest Rates", "Euribor", "SONIA", "Equity Indices", "NYSE Equity Options", "NYSE Cash Equities"]
    l13 = ice_span[-13:]
    ice_rows = [["<b>Total ADV</b>"] + [f'<td{heat_style(ice_yoy.get(k))}><b>{fmt_pct(ice_yoy.get(k))}</b></td>' if ice_yoy.get(k) is not None
                                         else '<td class="nd" title="not in the release">n.d.</td>' for k in l13],
                ["Total OI"] + [f'<td{heat_style((ice[k].get("total") or {}).get("oi_yoy"))}>{fmt_pct((ice[k].get("total") or {}).get("oi_yoy"))}</td>' for k in l13]]
    for ln in ice_lines:
        row = [ln]
        for k in l13:
            x = ice[k]["lines"].get(ln)
            v = x.get("adv_yoy") if x else None
            row.append(f'<td{heat_style(v)}>{fmt_pct(v)}</td>' if v is not None else '<td class="nd">–</td>')
        ice_rows.append(row)
    ice_heat = table(["ADV y/y"] + [lab(k) for k in l13], ice_rows)
    nd_months = [lab(k) for k in ice_span if ice_yoy.get(k) is None]

    # ---------------- Cboe ----------------
    cb_span = [k for k in span if k in cboe]
    cxs = [lab(k) for k in cb_span]
    g = lambda f: [cboe[k].get(f) for k in cb_span]  # noqa: E731
    mounts.append(("ch-cb-idx", "line", {"xs": cxs, "height": 240, "series": [
        {"name": "SPX options", "color": "--fs1", "vals": [v / 1000 if v else None for v in g("adv_spx_k")]},
        {"name": "VIX options", "color": "--fs2", "vals": [v / 1000 if v else None for v in g("adv_vix_opt_k")]},
        {"name": "XSP options", "color": "--fs3", "vals": [v / 1000 if v else None for v in g("adv_xsp_k")]}],
        "label": "Cboe index options ADV, millions of contracts"}))
    mounts.append(("ch-cb-share", "line", {"xs": cxs, "height": 240, "series": [
        {"name": "Multi-listed options share", "color": "--fs1", "vals": [round(v * 100, 2) if v else None for v in g("share_multilist")]},
        {"name": "U.S. equities on-exchange share", "color": "--fs2", "vals": [round(v * 100, 2) if v else None for v in g("share_us_eq_on")]}],
        "label": "Cboe market share, percent"}))
    mounts.append(("ch-cb-rpc-idx", "line", {"xs": cxs, "height": 220, "series": [
        {"name": "Index options RPC ($)", "color": "--fs1", "vals": [round(v, 3) if v else None for v in g("rpc_index")]}],
        "label": "Cboe index options revenue per contract"}))
    mounts.append(("ch-cb-rpc-ml", "line", {"xs": cxs, "height": 220, "series": [
        {"name": "Multi-listed options RPC ($)", "color": "--fs2", "vals": [round(v, 3) if v else None for v in g("rpc_multilist")]}],
        "label": "Cboe multi-listed options revenue per contract"}))

    # ---------------- OCC share ----------------
    oc_span = [k for k in span if k in occ]
    groups = [("Cboe", "--fs1"), ("Nasdaq", "--fs2"), ("ICE (NYSE)", "--fs3"), ("MIAX", "--fs4")]
    mounts.append(("ch-occ-share", "line", {"xs": [lab(k) for k in oc_span], "height": 260, "endLabels": True, "mr": 70,
                                             "series": [{"name": gname, "short": gname, "color": col,
                                                         "vals": [occ[k]["groups"][gname]["share"] for k in oc_span]} for gname, col in groups]}))
    mounts.append(("ch-occ-adv", "bars", {"xs": [lab(k) for k in oc_span], "vals": [round(occ_adv.get(k), 2) if occ_adv.get(k) else None for k in oc_span],
                                           "color": "--fs4", "name": "US listed options ADV (m contracts/day)", "height": 220,
                                           "notes": [f"y/y {fmt_pct(occ_yoy.get(k), 1)}" if occ_yoy.get(k) is not None else "" for k in oc_span]}))
    share_rows = []
    for k in oc_span[::-1][:13]:
        gp = occ[k]["groups"]
        share_rows.append([lab(k), f"{occ[k]['total'] / 1e6:,.0f}", fmt_num(occ_adv.get(k), 1)] +
                          [f"{gp[n]['share']:.1f}%" for n in ("Cboe", "Nasdaq", "ICE (NYSE)", "MIAX", "MEMX", "BOX", "Other")])
    share_table = table(["Month", "Contracts (m)", "ADV (m)", "Cboe", "Nasdaq", "ICE (NYSE)", "MIAX", "MEMX", "BOX", "Other"], share_rows)

    # ---------------- consensus ----------------
    cons_rows = []
    for t, name, _ in TICKERS:
        c = est["companies"].get(t)
        if not c:
            continue
        p, pt = c["periods"], c["pt"]
        up = 100 * (pt["cons"] / c["px"] - 1) if pt.get("cons") and c.get("px") else None
        pe1 = c["px"] / p["1FY"]["eps"] if p.get("1FY", {}).get("eps") else None
        pe2 = c["px"] / p["2FY"]["eps"] if p.get("2FY", {}).get("eps") else None
        cons_rows.append([f'<a href="../index.html#{t}">{t}</a>', f"${c['px']:,.2f}", f"${pt['cons']:,.0f}", fmt_pct(up, 1),
                          f"{int(pt.get('buy', 0))} / {int(pt.get('hold', 0))} / {int(pt.get('sell', 0))}",
                          f"${p['1FQ']['rev']:,.0f}m", f"${p['1FQ']['eps']:.2f}", f"${p['1FY']['eps']:.2f}", f"${p['2FY']['eps']:.2f}",
                          fmt_num(pe1, 1, "x"), fmt_num(pe2, 1, "x")])
    cons_table = table(["Ticker", "Price", "Mean PT", "Upside", "Buy / Hold / Sell", "Q4-26E revenue", "Q4-26E EPS",
                        "FY26E EPS", "FY27E EPS", "P/E FY26E", "P/E FY27E"], cons_rows)

    # ---------------- page ----------------
    groups_nav = [("Volume cycle", [("overview", "Overview"), ("spike", "Spike or structural?"), ("qtd", "Quarter to date")]),
                  ("Exchanges", [("cme", "CME"), ("ice", "ICE"), ("cboe", "Cboe"), ("occ", "US options share")]),
                  ("Valuation", [("consensus", "Consensus")]), ("Research", [("method", "Method & sources")])]
    asof = max(latest.values())
    body = shell("Exchange volumes", "RESEARCH / FINANCIALS / EXCHANGES", "Latest month",
                 f"{lab(asof)} · built {d['built'][:10]}", groups_nav, ("Financials · exchanges", "CME · ICE · Cboe · Nasdaq"))
    # the ICE total-ADV omissions are already explained in the ICE section
    warn = [w for w in d.get("warnings", []) if "left blank, not inferred" not in w]
    body += f"""
<section id="overview"><p class="oc-kicker">Financials theme · exchanges</p>
<h2>Exchange volumes: one cycle, four franchises</h2>
<p class="fd-main-q">Q3 activity was strong across all four exchanges (CME ADV +16%, ICE futures and options ADV +31%, Cboe index-options ADV +24%, Nasdaq Index revenue +39%, per the Q3 releases in the <a href="../index.html#TH-financials">Financials theme</a>). This page tracks whether that holds month by month and whether it follows volatility. Monthly releases are public. Each value below carries its source in the Method section.</p>
{tile_html}
</section>
<section id="spike"><h2>Spike or structural?</h2>
<p class="sub">Year-on-year ADV growth by exchange, with VIX and OVX monthly averages on a separate axis beneath. If growth only follows volatility, the scatters below slope upward and months with falling volatility show falling volume.</p>
<div class="fd-card"><h3>Year-on-year volume growth</h3>
{legend([(s['name'], s['color']) for s in series_g])}
<div class="fd-chart" id="ch-growth"></div>
<p class="fd-sub" style="margin-top:14px">Volatility context: monthly average of daily closes (Cboe VIX and OVX history files)</p>
{legend([("VIX", "--fs1"), ("OVX (crude oil volatility)", "--fs2")])}
<div class="fd-chart" id="ch-vix"></div>
<details class="fd-tv"><summary>Table view (last 18 months)</summary>{growth_table}</details>
<p class="fd-src">CME y/y is from the CME release; where CME does not state it, it is computed from the prior-year release (marked <span class="fd-calc">c</span>; CME tends to omit y/y when volume fell). ICE gives y/y only and drops the total-ADV line in some months (gaps). Cboe index options and OCC y/y are Capstone arithmetic from the published levels; OCC ADV = OCC monthly contracts / US trading days.</p></div>
<div class="fd-grid2">
<div class="fd-card"><h3>CME: ADV growth vs VIX change</h3><p class="fd-sub">{rtext(r_cme)} (Capstone arithmetic, Pearson)</p>{legend([(g_['name'], g_['color']) for g_ in sc_cme], True)}<div class="fd-chart" id="sc-cme"></div></div>
<div class="fd-card"><h3>Cboe index options: ADV growth vs VIX change</h3><p class="fd-sub">{rtext(r_cboe)} (Capstone arithmetic, Pearson)</p>{legend([(g_['name'], g_['color']) for g_ in sc_cboe], True)}<div class="fd-chart" id="sc-cboe"></div></div>
<div class="fd-card"><h3>ICE: ADV growth vs OVX change</h3><p class="fd-sub">{rtext(r_ice)} (Capstone arithmetic, Pearson; months without a total-ADV line excluded)</p>{legend([(g_['name'], g_['color']) for g_ in sc_ice], True)}<div class="fd-chart" id="sc-ice"></div></div>
<div class="fd-card"><h3>How to read it</h3><p class="fd-sub">A strong positive correlation means the year-on-year volume change mostly tracks the change in volatility, which supports the "volatility spike" case. Points in the upper-left quadrant (volume up while volatility fell year on year) support the structural case. A correlation on 21–33 monthly points is descriptive, not a forecast, and one market event can dominate it.</p></div>
</div></section>
<section id="qtd"><h2>{qlabel} to date</h2>
<p class="sub">The current quarter's published months against the same months a year earlier. Bloomberg consensus for the quarter is in the Consensus section. Releases for a month arrive in the first week of the next month.</p>
<div class="fd-card">{table(["Series", "Months in", "QTD y/y", "Basis"], qtd_rows)}</div></section>
<section id="cme"><h2>CME</h2>
<div class="fd-card"><h3>Total ADV, millions of contracts</h3><p class="fd-sub">Monthly volume release (PR Newswire). Hover for y/y and its basis.</p><div class="fd-chart" id="ch-cme-adv"></div></div>
<div class="fd-card"><h3>Asset classes: y/y and ADV, last 13 months</h3><p class="fd-sub">Releases list asset classes selectively; a dash means the release did not give that line for the month (omitted is not zero). <span class="fd-calc">c</span> = y/y computed from the prior-year release because CME did not state it.</p>{cme_heat}</div>
<div class="fd-grid2">
<div class="fd-card"><h3>Customer collateral balances ($bn)</h3><p class="fd-sub">Rolling three-month average as stated in each monthly release, labelled by the month the average ends. Cash collateral drives CME's net interest income on clearing balances.</p>{legend([("Cash", "--fs1"), ("Non-cash", "--fs2")])}<div class="fd-chart" id="ch-cme-coll"></div></div>
<div class="fd-card"><h3>BrokerTec average daily notional ($bn)</h3><p class="fd-sub">Overall BrokerTec ADNV (U.S. and European repo plus U.S. Treasury cash), stated from the April 2026 release; earlier releases give only the components. Hover for y/y.</p><div class="fd-chart" id="ch-cme-bt"></div></div>
</div></section>
<section id="ice"><h2>ICE</h2>
<div class="fd-card"><h3>Total ADV, y/y</h3><p class="fd-sub">ICE's monthly release gives growth rates only. It omitted the total-ADV line in {len(nd_months)} of {len(ice_span)} months since Jan-24 ({", ".join(nd_months)}); those bars are left empty rather than inferred.</p><div class="fd-chart" id="ch-ice-tot"></div></div>
<div class="fd-card"><h3>By product line, ADV y/y, last 13 months</h3><p class="fd-sub">Line names normalised across releases (e.g. "Total Energy" = "Energy"). A dash means the line was not in that month's release; omitted is not zero.</p>{ice_heat}</div>
</section>
<section id="cboe"><h2>Cboe</h2>
<div class="fd-grid2">
<div class="fd-card"><h3>Index options ADV (m contracts)</h3>{legend([("SPX", "--fs1"), ("VIX options", "--fs2"), ("XSP", "--fs3")])}<div class="fd-chart" id="ch-cb-idx"></div></div>
<div class="fd-card"><h3>Market share (%)</h3>{legend([("Multi-listed options", "--fs1"), ("U.S. equities on-exchange", "--fs2")])}<div class="fd-chart" id="ch-cb-share"></div></div>
<div class="fd-card"><h3>Index options revenue per contract ($)</h3><p class="fd-sub">Cboe's rolling three-month average, reported with a one-month lag, so the latest month and each December are missing from the monthly sheets. The S&amp;P royalty reset from 2027 acts on this line.</p><div class="fd-chart" id="ch-cb-rpc-idx"></div></div>
<div class="fd-card"><h3>Multi-listed options revenue per contract ($)</h3><p class="fd-sub">Rolling three-month average, one-month lag (latest month and Decembers not published in the monthly sheets).</p><div class="fd-chart" id="ch-cb-rpc-ml"></div></div>
</div></section>
<section id="occ"><h2>US listed options: share by exchange group</h2>
<p class="sub">OCC clears every US listed option, so its exchange report gives a common denominator for Cboe, Nasdaq and ICE (NYSE American and Arca). Shares are of OCC-cleared contracts, equity and index together; Cboe's share includes its proprietary SPX and VIX. Nasdaq's own monthly data sheet is not reachable by script, so this is the monthly read on Nasdaq's options business.</p>
<div class="fd-card"><h3>Share of OCC-cleared contracts (%)</h3>{legend([(n, c) for n, c in groups])}<div class="fd-chart" id="ch-occ-share"></div>
<details class="fd-tv"><summary>Table view (last 13 months, all groups)</summary>{share_table}</details>
<p class="fd-src">Groups: Cboe = CBOE, C2, BZX (BATS), EDGX · Nasdaq = PHLX, ISE, GEMX, MRX, NOM, BX · ICE (NYSE) = NYSE American, NYSE Arca · MIAX = MIAX, Emerald, Pearl, Sapphire. Mapping by Capstone.</p></div>
<div class="fd-card"><h3>Industry ADV (m contracts per day)</h3><p class="fd-sub">OCC monthly contracts divided by US trading days (Capstone arithmetic; hover for y/y).</p><div class="fd-chart" id="ch-occ-adv"></div></div>
</section>
<section id="consensus"><h2>Consensus</h2>
<p class="sub">Bloomberg BEst consensus as of {escape(est['asof'])} (local terminal). FY lines are used because the calendar-year line uses Bloomberg's back-period estimates for reported quarters. All four report on a calendar year. Company pages hold the attributed broker views.</p>
<div class="fd-card">{cons_table}</div></section>
<section id="method"><h2>Method &amp; sources</h2>
<div class="fd-card"><p class="fd-sub">{escape(d['note'])}</p>
<ul class="fd-sub">
<li><b>OCC</b>: <a href="{escape(d['occ']['urls'].get(str(today.year), ''))}">exchange-volume report, market view, monthly</a>. Refetched every run.</li>
<li><b>Cboe</b>: monthly volume &amp; RPC data sheet (<a href="{escape(d['cboe']['files'].get(str(today.year), ''))}">latest file</a>), also linked from <a href="https://cboe.com/us/options/market_statistics/monthly_volume_rpc_reports/">cboe.com</a>.</li>
<li><b>CME</b>: monthly volume releases on <a href="{escape(d['cme']['listing'])}">PR Newswire</a> (CME's own monthly-volume page refuses scripted requests). Latest: <a href="{escape(c_rec['url'])}">{escape(c_rec['title'])}</a>.</li>
<li><b>ICE</b>: monthly statistics releases (PDF). Latest: <a href="{escape(i_rec['url'])}">{escape(lab(li))}</a>. Levels sit in ICE's Monthly Statistics Tracking spreadsheet, which refuses scripted requests.</li>
<li><b>Nasdaq</b>: the monthly volume data sheet on ir.nasdaq.com refuses scripted requests; options share comes from OCC and the rest from the quarterly results on the <a href="../index.html#NDAQ">NDAQ page</a>.</li>
<li><b>Volatility</b>: Cboe <a href="{escape(d['vol']['urls'].get('VIX', ''))}">VIX</a> and <a href="{escape(d['vol']['urls'].get('OVX', ''))}">OVX</a> daily history. MOVE (rates volatility) needs Bloomberg and is not shown.</li>
<li><b>Trading days</b>: Cboe's published count where available; otherwise the NYSE holiday calendar. Disagreements: {escape('; '.join(days_check) or 'none')}.</li>
</ul>
<p class="fd-sub"><b>Refresh</b>: <code>fetch_exchange_volumes.py</code> (network, public sources) then <code>build_fin_exchanges.py</code>. The 18:15 chain rebuilds the page from the saved JSON.</p>
{('<div class="fd-callout warn"><b>Parser notes from the last fetch</b><br>' + '<br>'.join(escape(w) for w in warn) + '</div>') if warn else ''}
</div></section>"""
    html = page("Exchange volumes", "Monthly volumes, share and revenue capture for CME, ICE, Cboe and Nasdaq "
                "against volatility and consensus", body, mounts)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(WIKI)} ({len(html) / 1024:.0f} KB) · latest {latest}")
    print("trading-day disagreements:", days_check or "none")
    print("corr CME/VIX", r_cme, "Cboe/VIX", r_cboe, "ICE/OVX", r_ice)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
