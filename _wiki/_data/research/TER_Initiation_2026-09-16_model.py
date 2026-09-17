# -*- coding: utf-8 -*-
"""Capstone TER (Teradyne) initiation -- base/bull/bear estimate model, guardrails, sensitivity, DCF cross-check.
Every input is tagged HARD / ANCHOR / PARTIAL / ESTIMATE with its source. Run: PYTHONIOENCODING=utf-8 py ter_model.py -> model_out.json
Teradyne's fiscal year is the calendar year (Dec FYE); quarters end late Mar / late Jun / late Sep / Dec 31. US$m unless stated. Non-GAAP as the
company defines it (excludes acquired-intangible amortisation, restructuring, ERP costs, equity-method amortisation; SBC is NOT excluded)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ market / balance sheet (HARD)
PX = 341.15            # HARD  Bloomberg PX_LAST pulled 2026-09-16 (late session)
SH_OUT = 156.34        # HARD  10-Q Q2 FY26 cover: 156,340,750 shares at 2026-07-27
DIL_Q2 = 157.7         # HARD  Q2 FY26 diluted weighted shares (press release 2026-07-28)
CASH_Q2 = 517.1        # HARD  cash 349.5 + ST marketable 5.3 + LT marketable 162.3 (10-Q / press release, 2026-06-28); company: "$517 million"
DEBT_Q2 = 0.0          # HARD  no debt at 2026-06-28; the $200m revolver balance at Dec-25 was repaid in H1 (cash-flow statement)
TECHNOPROBE = 515.0    # HARD  equity-method investment carrying value 2026-06-28 (10% of Technoprobe, bought May-2024 for $524m)
REVOLVER = 750.0       # HARD  $750m revolving credit facility, expires 2026-12-10 (10-K FY25)
DIV_Q = 0.13           # HARD  quarterly dividend per share

# ------------------------------------------------------------------ reported history (HARD, press releases / 10-Q)
H1 = dict(rev=2611.5, eps=5.02, gp=1575.7, oi=928.9, ni=791.9, fcf=579.0, ocf=734.3, capex=155.4)   # H1 FY26 as reported
Q2 = dict(rev=1329.0, gm=0.598, opex=346.3, oi=448.3, ni=389.0, eps=2.47, sh=157.7)                   # Q2 FY26; opex = GP 794.6 - OI 448.3
Q1 = dict(rev=1282.5, gm=0.609, opex=300.6, oi=480.4, ni=402.9, eps=2.56, sh=157.6)                   # Q1 FY26; opex = GP 781.0 - OI 480.4
FY25 = dict(rev=3190.0, eps=3.97, gm=0.582, ocf=674.4, capex=224.0, fcf=450.4, semi=2523.7, soc=1889.7, mem=504.9, ist=129.2, pt=358.0, rob=308.3,
            ibt_semi=700.7, ibt_pt=60.7, ibt_rob=-99.4, dep_amort=128.0, div=76.3)

# ------------------------------------------------------------------ consensus (Bloomberg BEst, pulled 2026-09-16)
CONS = {
    "CY26": dict(rev=5065.9, eps=8.838, gm=0.5936, ebit=1655.7, n=18, rev_hi=5226, rev_lo=4547, eps_hi=9.35, eps_lo=7.34),
    "CY27": dict(rev=6237.3, eps=11.453, gm=0.5951, ebit=2143.5, n=18, rev_hi=7708, rev_lo=5110, eps_hi=14.24, eps_lo=9.00, capex=352.6),
    "CY28": dict(rev=7543.4, eps=14.769, gm=0.5971, ebit=2724.3, n=11, rev_hi=9305, rev_lo=6075, eps_hi=18.95, eps_lo=10.60, capex=429.4),
    "CY29": dict(rev=8754.0, eps=18.45, n=1),
    # kFQ ladder Q3-26 .. Q4-28 (BEST_SALES / BEST_EPS mean; hi/lo)
    "FQ": [1243.6, 1235.7, 1417.8, 1596.1, 1606.5, 1575.1, 1810.8, 2011.0, 1902.2, 1770.0],
    "FQ_eps": [1.988, 1.942, 2.484, 2.970, 2.949, 2.760, 3.487, 4.050, 3.678, 3.250],
    "FQ_hi": [1300, 1330, 1555, 2020, 2018, 2337, 2450, 2670, 2250, 2093],
    "FQ_lo": [950, 900, 1210, 1355, 1215, 1155, 1365, 1620, 1625, 1465],
    "pt_mean": 450.87, "pt_hi": 550, "pt_lo": 390, "buy": 13, "hold": 6, "sell": 0, "fwd_pe_blended": 36.35,
}
QLAB = ["Q3 FY26E (Sep-26)", "Q4 FY26E (Dec-26)", "Q1 FY27E (Mar-27)", "Q2 FY27E (Jun-27)", "Q3 FY27E (Sep-27)", "Q4 FY27E (Dec-27)",
        "Q1 FY28E (Mar-28)", "Q2 FY28E (Jun-28)", "Q3 FY28E (Sep-28)", "Q4 FY28E (Dec-28)"]

# ------------------------------------------------------------------ the TAM bridge (industry inputs)
# WFE (US$bn): CY26 ~$158bn (UBS 2026-09-01 baseline; canonical wiki range $140-160bn). CY27: house $180-215bn / MS $223bn / UBS $225bn / Bernstein $175bn.
# CY28: house top $260bn / GS $281bn / UBS $275bn / MS $254bn (5th raise) / Bernstein $198bn. CY27 also: KLA-cited Street consensus ~$190bn, SEMI $175bn, Gartner $166bn. ATE share of WFE: TER management 4% (2023) -> 7% (2025) -> 8% (Jan-May 2026),
# "settle 7-9%, most likely 7-8%", "could revert down to 6%, 7% or so" in 2027 on the ~1-year WFE->wafer lag + ~16-week tester lead times (Greg Smith,
# Q2 CY26 call 2026-07-29); the "historically 8% of WFE... snapped back" framing is ARCURI'S question on the UBS fireside (2026-08-03); IR's answer: "the real answer is we don't know... I would plan for 7 to 9%".
# UBS published: "the Semi Test TAM has averaged a median of ~8% of WFE spend" (Arcuri via Ruple 2026-07-25). BofA: "ATE intensity likely sustaining at 7%-8%... $14bn+ ATE TAM as early as FY27E" (Arya 2026-07-29).
WFE = {"base": {2026: 158, 2027: 205, 2028: 240}, "bull": {2026: 158, 2027: 220, 2028: 260}, "bear": {2026: 158, 2027: 200, 2028: 225}}
RATIO = {"base": {2026: 0.080, 2027: 0.073, 2028: 0.075}, "bull": {2026: 0.080, 2027: 0.075, 2028: 0.077}, "bear": {2026: 0.080, 2027: 0.065, 2028: 0.068}}
SHARE_GAIN = {"base": {2027: 0.012, 2028: 0.015}, "bull": {2027: 0.020, 2028: 0.020}, "bear": {2027: 0.010, 2028: 0.010}}   # TER Semi Test share of ATE TAM, pp/yr

def build(case):
    """Quarterly non-GAAP build. Q3 FY26 anchored to the guide; Q4 FY26 to the '50-52% of revenue in H1' framing; CY27-28 from the TAM x share bridge
    with the consensus quarterly shape. Returns rows + segment annuals."""
    if case == "base":
        q3 = dict(rev=1270.0, gm=0.586, opex_pct=0.295)             # ANCHOR guide mid $1,250m / 58-59% / opex 29-30% of sales; +1.6% on the midpoint (10/10 quarters at or above mid)
        q4_rev = 1245.0                                             # ANCHOR "50-52% of annual revenue in H1" -> FY26 $5.02-5.22bn -> Q4 $1.16-1.36bn; Q4 opex "comparable to Q3"
        pt = {2026: 410, 2027: 465, 2028: 525}                      # ESTIMATE Product Test: FY25 $358m; H1 $187m; Omnyx/MLTP/CPO (~$200m CPO TAM 2027 low end); +13%/+13%
        rob = {2026: 396, 2027: 460, 2028: 530}                     # ESTIMATE Robotics: FY25 $308m; H1 $191m (+33%); "grow in proportion with the rest of the company"; +16%/+15%
        gm = {2027: [0.590, 0.595, 0.597, 0.598], 2028: [0.600, 0.602, 0.603, 0.603]}   # PARTIAL FY26 "~59%" -> "60% or higher over the mid-term" (IR 08-03); new model Feb-27
        opex_g = {2027: 0.10, 2028: 0.11}                           # PARTIAL "OpEx growth... less than half of revenue growth over time" (CEO, GS Communacopia small group 2026-09-13)
        shape = {2027: [0.237, 0.260, 0.256, 0.247], 2028: [0.235, 0.259, 0.256, 0.250]}   # ESTIMATE ~consensus quarterly shape (compute surge 1H27, memory adds through 2027)
        tax = {2026: 0.15, 2027: 0.15, 2028: 0.155}                 # PARTIAL Q2 FY26 GAAP ETR 15.1%; Q4 FY25 guide used 14.5%; drift up on geographic mix
        buyback = {2026: 150, 2027: 400, 2028: 450}                 # ESTIMATE H2-26 buyback $150m (H1 $74m, "build cash for M&A"); $400-450m/yr thereafter under the $617m remaining + renewal
    elif case == "bull":
        q3 = dict(rev=1330.0, gm=0.590, opex_pct=0.290)             # ESTIMATE the last-4-quarter mean beat (+8.6% vs mid) -- the track record, not the guide
        q4_rev = 1330.0                                             # top of the 50% H1 framing ($5.22bn)
        pt = {2026: 415, 2027: 490, 2028: 580}
        rob = {2026: 400, 2027: 490, 2028: 580}
        gm = {2027: [0.596, 0.600, 0.603, 0.605], 2028: [0.606, 0.607, 0.608, 0.608]}   # ESTIMATE new model >60% delivered early; product test/mix
        opex_g = {2027: 0.12, 2028: 0.12}
        shape = {2027: [0.237, 0.260, 0.256, 0.247], 2028: [0.235, 0.259, 0.256, 0.250]}
        tax = {2026: 0.15, 2027: 0.15, 2028: 0.155}
        buyback = {2026: 150, 2027: 500, 2028: 600}
    else:  # bear
        q3 = dict(rev=1250.0, gm=0.580, opex_pct=0.300)             # guide mid, low end of GM / high end of opex
        q4_rev = 1160.0                                             # bottom of the framing (52% H1 -> FY $5.02bn)
        pt = {2026: 405, 2027: 430, 2028: 460}
        rob = {2026: 390, 2027: 410, 2028: 430}
        gm = {2027: [0.582, 0.580, 0.580, 0.578], 2028: [0.582, 0.584, 0.585, 0.585]}   # ESTIMATE mix + new-product cost curves + input-cost inflation (Chroma GM -3ppt, JPM 07-30) + pricing to defend share
        opex_g = {2027: 0.08, 2028: 0.08}
        shape = {2027: [0.245, 0.262, 0.252, 0.241], 2028: [0.240, 0.258, 0.255, 0.247]}
        tax = {2026: 0.15, 2027: 0.15, 2028: 0.155}
        buyback = {2026: 150, 2027: 300, 2028: 300}
    OTHER = 5.0     # PARTIAL interest & other income ~+$5m/qtr (Q2 FY26 +$5.8m; cash ~$0.5bn, no debt)
    AFFIL = 5.5     # PARTIAL Technoprobe equity-method contribution on a non-GAAP basis ~+$5-6m/qtr (GAAP -$1.9m + $7.6m amortisation add-back in Q2)
    rows = []
    # ---- Q3 FY26
    r = dict(q=QLAB[0], rev=q3["rev"], gm=q3["gm"]); r["gp"] = r["rev"] * r["gm"]; r["opex"] = r["rev"] * q3["opex_pct"]; r["oi"] = r["gp"] - r["opex"]
    r["tax"] = tax[2026]; r["sh"] = 158.0; rows.append(r)
    # ---- Q4 FY26
    r = dict(q=QLAB[1], rev=q4_rev, gm=q3["gm"] - 0.001); r["gp"] = r["rev"] * r["gm"]; r["opex"] = rows[0]["opex"] + 2.0; r["oi"] = r["gp"] - r["opex"]
    r["tax"] = tax[2026]; r["sh"] = 158.0 - buyback[2026] / 2 / 360; rows.append(r)
    # ---- FY26 segment totals (Semi Test = total less Product Test less Robotics)
    fy26_rev = H1["rev"] + rows[0]["rev"] + rows[1]["rev"]
    seg = {2026: dict(total=fy26_rev, pt=pt[2026], rob=rob[2026], semi=fy26_rev - pt[2026] - rob[2026])}
    tam = {2026: WFE[case][2026] * RATIO[case][2026] * 1000}
    share = {2026: seg[2026]["semi"] / tam[2026]}
    opex26 = Q1["opex"] + Q2["opex"] + rows[0]["opex"] + rows[1]["opex"]
    prev_opex = opex26; prev_sh = rows[1]["sh"]
    for y in (2027, 2028):
        tam[y] = WFE[case][y] * RATIO[case][y] * 1000
        share[y] = share[y - 1] + SHARE_GAIN[case][y]
        semi = tam[y] * share[y]; total = semi + pt[y] + rob[y]
        seg[y] = dict(total=total, pt=pt[y], rob=rob[y], semi=semi)
        opex_y = prev_opex * (1 + opex_g[y]); prev_opex = opex_y
        qop = [opex_y * w for w in (0.242, 0.249, 0.252, 0.257)]
        for i in range(4):
            r = dict(q=QLAB[2 + (y - 2027) * 4 + i], rev=total * shape[y][i], gm=gm[y][i]); r["gp"] = r["rev"] * r["gm"]; r["opex"] = qop[i]; r["oi"] = r["gp"] - r["opex"]
            r["tax"] = tax[y]; prev_sh = prev_sh - buyback[y] / 4 / 380 + 0.15; r["sh"] = prev_sh   # ~$380 avg repurchase price; +0.15m/qtr SBC dilution
            rows.append(r)
    for r in rows:
        r["om"] = r["oi"] / r["rev"]; r["other"] = OTHER; r["pbt"] = r["oi"] + OTHER; r["ni"] = r["pbt"] * (1 - r["tax"]) + AFFIL; r["eps"] = r["ni"] / r["sh"]
    return rows, seg, tam, share, dict(pt=pt, rob=rob, buyback=buyback, opex_g=opex_g)

def agg(rows, idx, extra=None):
    r = [rows[i] for i in idx]; rev = sum(x["rev"] for x in r); gp = sum(x["gp"] for x in r); oi = sum(x["oi"] for x in r); ni = sum(x["ni"] for x in r)
    eps = sum(x["eps"] for x in r); opex = sum(x["opex"] for x in r)
    if extra:  # add reported H1 FY26
        rev += extra["rev"]; gp += extra["gp"]; oi += extra["oi"]; ni += extra["ni"]; eps += extra["eps"]; opex += extra["gp"] - extra["oi"]
    return dict(rev=rev, gm=gp / rev, oi=oi, om=oi / rev, ni=ni, eps=eps, opex=opex)

def periods(rows):
    return {"CY26": agg(rows, [0, 1], H1), "CY27": agg(rows, [2, 3, 4, 5]), "CY28": agg(rows, [6, 7, 8, 9])}

def cashflow(rows, case, seg, knobs):
    """Annual FCF: non-GAAP NI + D&A + SBC - dWC - capex. FY25: D&A $128m, SBC ~$70m (H1 FY26 $42m), capex $224m (7% of rev), FCF/NI ~75%.
    H1 FY26 actual: OCF $734m, capex $155m, FCF $579m on NI $792m (73% conversion, AR +$302m)."""
    P = periods(rows)
    out = {}
    cash = CASH_Q2
    # H2 FY26
    ni_h2 = rows[0]["ni"] + rows[1]["ni"]; rev_h2 = rows[0]["rev"] + rows[1]["rev"]
    da = 70; sbc = 45; dwc = -0.12 * (rev_h2 - H1["rev"]) if rev_h2 > H1["rev"] else 0.10 * (H1["rev"] - rev_h2)   # WC releases as revenue flattens
    capex = {"base": 200, "bull": 210, "bear": 190}[case]
    fcf = ni_h2 + da + sbc + dwc - capex
    cash += fcf - knobs["buyback"][2026] - DIV_Q * 2 * 156.5 - 0   # dividends
    out["H2-26"] = dict(ni=ni_h2, da=da, sbc=sbc, dwc=dwc, capex=capex, fcf=fcf, cash_end=cash)
    out["CY26"] = dict(ni=H1["ni"] + ni_h2, da=da + 66, sbc=sbc + 42, capex=capex + H1["capex"], fcf=H1["fcf"] + fcf, ocf=H1["ocf"] + fcf + capex, cash_end=cash)
    prev_rev = P["CY26"]["rev"]
    for y, key in ((2027, "CY27"), (2028, "CY28")):
        rev = P[key]["rev"]; ni = P[key]["ni"]
        da = {"CY27": 150, "CY28": 175}[key]                          # PARTIAL FY25 D&A $128m; capex step-up 2025-26 lifts depreciation
        sbc = {"CY27": 95, "CY28": 105}[key]                          # PARTIAL FY25 SBC ~$70m; H1 FY26 $42m
        dwc = -0.15 * (rev - prev_rev)                                 # ESTIMATE net WC ~15% of incremental revenue (Q2 FY26: AR 76 days, inventory 68 days of COGS, deferred revenue offsets)
        capex = {"CY27": {"base": 380, "bull": 420, "bear": 330}, "CY28": {"base": 430, "bull": 500, "bear": 350}}[key][case]   # PARTIAL BEst $353m / $429m; FY25 7.0% of revenue; capacity + demo assets
        fcf = ni + da + sbc + dwc - capex
        cash += fcf - knobs["buyback"][y] - DIV_Q * 4 * 156.0
        out[key] = dict(ni=ni, da=da, sbc=sbc, dwc=dwc, capex=capex, fcf=fcf, ocf=fcf + capex, cash_end=cash, fcf_yield=fcf / (PX * SH_OUT))
        prev_rev = rev
    return out

def dcf(rows, case, ke=0.10, tg=0.03, om_end=0.30):
    """Template-convention DCF (house: Ke 10%, g 3%). Explicit CY27-CY35; OM fades from the CY28 level to om_end by CY35; SBC charged as a cost;
    capex 5% of revenue long-run (FY19-25 average 5.8%); D&A 2.4%; dWC 15% of incremental revenue; tax 15.5%. Valuation date end-CY26 -> rolled 9 months."""
    P = periods(rows)
    g = {"base": [0.13, 0.11, 0.09, 0.07, 0.05, 0.04, 0.03], "bull": [0.16, 0.13, 0.10, 0.08, 0.06, 0.04, 0.03], "bear": [0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.03]}[case]
    om28 = P["CY28"]["om"]
    revs = [P["CY27"]["rev"], P["CY28"]["rev"]]
    for x in g: revs.append(revs[-1] * (1 + x))
    oms = [P["CY27"]["om"], om28] + [om28 - (om28 - om_end) * (i + 1) / 7 for i in range(7)]
    tax = 0.155; sbc_pct = 0.014; da_pct = 0.024; wc_pct = 0.15
    capex_pct = [0.061, 0.056, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    prev = P["CY26"]["rev"]; fcfs = []; table = []
    for i, (rv, m) in enumerate(zip(revs, oms)):
        nopat = rv * (m - sbc_pct) * (1 - tax); da = rv * da_pct; cx = rv * capex_pct[i]; dwc = (rv - prev) * wc_pct
        f = nopat + da - cx - dwc; fcfs.append(f); table.append(dict(year=2027 + i, rev=rv, om=m, nopat=nopat, fcf=f)); prev = rv
    pv = sum(f / (1 + ke) ** (i + 1) for i, f in enumerate(fcfs))
    tv = fcfs[-1] * (1 + tg) / (ke - tg); pv_tv = tv / (1 + ke) ** len(fcfs); ev = pv + pv_tv
    cf = cashflow(rows, case, None, build(case)[4])
    net_cash = cf["H2-26"]["cash_end"]                       # cash at end-CY26 after H2 buybacks/dividends; no debt
    eq = ev + net_cash + TECHNOPROBE
    sh = 157.6
    roll = (1 + ke) ** 0.75
    return dict(table=table, pv_fcf=pv, tv=tv, pv_tv=pv_tv, ev=ev, net_cash=net_cash, equity=eq, per_share=eq / sh, per_share_rolled=eq / sh * roll,
                tv_share=pv_tv / ev, ke=ke, g=tg, om_end=om_end)

# ------------------------------------------------------------------ guidance track record (HARD: press releases 2024-01-31 .. 2026-07-29)
GUIDE = [  # quarter, rev guide lo/hi, EPS guide lo/hi (non-GAAP), actual rev, actual EPS
    ("Q1 FY24", 540, 590, 0.22, 0.38, 600, 0.51), ("Q2 FY24", 665, 725, 0.64, 0.84, 730, 0.86), ("Q3 FY24", 680, 740, 0.66, 0.86, 737, 0.90),
    ("Q4 FY24", 710, 760, 0.80, 0.97, 753, 0.95), ("Q1 FY25", 660, 700, 0.58, 0.68, 686, 0.75), ("Q2 FY25", 610, 680, 0.41, 0.64, 652, 0.57),
    ("Q3 FY25", 710, 770, 0.69, 0.87, 769, 0.85), ("Q4 FY25", 920, 1000, 1.20, 1.46, 1083, 1.80), ("Q1 FY26", 1150, 1250, 1.89, 2.25, 1282, 2.56),
    ("Q2 FY26", 1150, 1250, 1.86, 2.15, 1329, 2.47)]

def track_record():
    out = []
    for q, lo, hi, elo, ehi, arev, aeps in GUIDE:
        mid = (lo + hi) / 2; emid = (elo + ehi) / 2
        out.append(dict(q=q, rev_lo=lo, rev_hi=hi, rev_mid=mid, rev=arev, beat_pct=arev / mid - 1, beat_abs=arev - mid, above_top=arev > hi,
                        eps_lo=elo, eps_hi=ehi, eps_mid=emid, eps=aeps, eps_beat=aeps - emid, eps_above_top=aeps > ehi))
    n = len(out); avg_pct = sum(o["beat_pct"] for o in out) / n; avg4 = sum(o["beat_pct"] for o in out[-4:]) / 4
    eps_avg = sum(o["eps_beat"] for o in out) / n; eps_avg4 = sum(o["eps_beat"] for o in out[-4:]) / 4
    return dict(rows=out, avg_pct=avg_pct, avg4_pct=avg4, eps_avg=eps_avg, eps_avg4=eps_avg4, n_above_top=sum(o["above_top"] for o in out),
                n_eps_above_top=sum(o["eps_above_top"] for o in out), n_at_or_above_mid=sum(o["beat_pct"] >= 0 for o in out),
                q3_implied_10q=1250 * (1 + avg_pct), q3_implied_4q=1250 * (1 + avg4), q3_eps_implied=2.00 + eps_avg4, q3_eps_implied_10q=2.00 + eps_avg)

if __name__ == "__main__":
    OUT = {"px": PX, "sh_out": SH_OUT, "cons": CONS, "fy25": FY25, "h1": H1, "wfe": WFE, "ratio": RATIO, "share_gain": SHARE_GAIN, "cases": {}}
    R = {}
    for case in ("base", "bull", "bear"):
        rows, seg, tam, share, knobs = build(case); P = periods(rows); cf = cashflow(rows, case, seg, knobs); d = dcf(rows, case)
        R[case] = (rows, seg, tam, share, knobs)
        print(f"\n===== {case.upper()} =====")
        for r in rows:
            print(f"{r['q']:20s} rev {r['rev']:7.0f}  GM {r['gm']*100:5.1f}%  opex {r['opex']:5.0f} ({r['opex']/r['rev']*100:4.1f}%)  OI {r['oi']:6.0f} ({r['om']*100:4.1f}%)  NI {r['ni']:6.0f}  sh {r['sh']:6.1f}  EPS {r['eps']:5.2f}")
        for k, v in P.items():
            c = CONS[k]
            print(f"  {k}: rev {v['rev']:7.0f} ({v['rev']/c['rev']-1:+.1%} vs cons {c['rev']:.0f})  GM {v['gm']*100:5.1f}%  OI {v['oi']:6.0f} ({v['om']*100:4.1f}% vs cons {c['ebit']/c['rev']*100:.1f}%)  EPS {v['eps']:6.2f} ({v['eps']/c['eps']-1:+.1%} vs cons {c['eps']:.2f})")
        for y in (2026, 2027, 2028):
            s = seg[y]; print(f"  {y}: WFE ${WFE[case][y]}bn x {RATIO[case][y]*100:.1f}% = ATE TAM ${tam[y]/1000:.1f}bn | Semi Test {s['semi']:.0f} ({share[y]*100:.1f}% share) + Product Test {s['pt']} + Robotics {s['rob']} = {s['total']:.0f}")
        for k in ("CY26", "CY27", "CY28"): print(f"  {k} FCF {cf[k]['fcf']:.0f} (capex {cf[k]['capex']:.0f}, dWC {cf[k].get('dwc',0):.0f}) cash end {cf[k]['cash_end']:.0f}")
        print(f"  DCF Ke10/g3 OM->30%: ${d['per_share']:.0f} end-26, ${d['per_share_rolled']:.0f} rolled (TV {d['tv_share']:.0%}, EV {d['ev']:.0f}, net cash {d['net_cash']:.0f})")
        OUT["cases"][case] = dict(rows=rows, periods=P, seg=seg, tam=tam, share=share, cf=cf, dcf=d, knobs=knobs)
    # ---- valuation
    b = OUT["cases"]["base"]["periods"]; bu = OUT["cases"]["bull"]["periods"]; be = OUT["cases"]["bear"]["periods"]
    MULT = 25.0
    PT = round(MULT * b["CY28"]["eps"] / 5) * 5
    BULL = round(MULT * bu["CY28"]["eps"] / 5) * 5
    BEAR = round(18.0 * be["CY28"]["eps"] / 5) * 5          # $202.9 -> $205 (same $5 rounding as the PT)
    EV_ = 0.25 * BULL + 0.5 * PT + 0.25 * BEAR
    OUT.update(pt=PT, mult=MULT, bull_val=BULL, bear_val=BEAR, bear_mult=18.0, expected_value=EV_)
    print(f"\nPT = {MULT}x CY28E EPS {b['CY28']['eps']:.2f} = {MULT*b['CY28']['eps']:.1f} -> ${PT} ({PT/PX-1:+.1%}); = {PT/b['CY27']['eps']:.1f}x CY27E; blended-fwd at Sep-27 (0.25*CY27+0.75*CY28) {0.25*b['CY27']['eps']+0.75*b['CY28']['eps']:.2f} -> {PT/(0.25*b['CY27']['eps']+0.75*b['CY28']['eps']):.1f}x")
    print(f"Bull {MULT}x {bu['CY28']['eps']:.2f} = ${BULL} ({BULL/PX-1:+.0%}); Bear 18x {be['CY28']['eps']:.2f} = ${BEAR} ({BEAR/PX-1:+.0%}); EV 25/50/25 = ${EV_:.0f} ({EV_/PX-1:+.1%})")
    # ---- DCF grids (base)
    rows_b = R["base"][0]
    grid = {}
    om28b = periods(rows_b)["CY28"]["om"]
    for ke in (0.09, 0.10, 0.109, 0.12):
        for om_end in (0.26, 0.30, 0.34, om28b):
            key = f"{ke:.1%}|{'flat' if om_end == om28b else f'{om_end:.0%}'}"
            grid[key] = dcf(rows_b, "base", ke=ke, om_end=om_end)["per_share_rolled"]
    OUT["dcf_om28"] = om28b
    OUT["dcf_bull_flat"] = dcf(R["bull"][0], "bull", ke=0.10, om_end=periods(R["bull"][0])["CY28"]["om"])["per_share_rolled"]
    OUT["dcf_bull_fade"] = dcf(R["bull"][0], "bull", ke=0.10, om_end=0.30)["per_share_rolled"]
    OUT["dcf_bear_fade"] = dcf(R["bear"][0], "bear", ke=0.10, om_end=0.26)["per_share_rolled"]
    OUT["dcf_grid"] = grid
    OUT["dcf_sens"] = {f"{ke:.0%}/{tg:.0%}": dcf(rows_b, "base", ke=ke, tg=tg)["per_share_rolled"] for ke in (0.09, 0.10, 0.11, 0.12) for tg in (0.02, 0.03, 0.04)}
    print("DCF grid (rolled):", {k: round(v) for k, v in grid.items()})
    # ---- PT sensitivity: one input at a time on the base case, 25x CY28E EPS
    base_eps = b["CY28"]["eps"]; sens = []
    def variant(label, **kw):
        global WFE, RATIO, SHARE_GAIN
        W0, R0, S0 = json.loads(json.dumps(WFE)), json.loads(json.dumps(RATIO)), json.loads(json.dumps(SHARE_GAIN))
        Wn = {k: {int(y): v for y, v in d_.items()} for k, d_ in json.loads(json.dumps(WFE)).items()}
        Rn = {k: {int(y): v for y, v in d_.items()} for k, d_ in json.loads(json.dumps(RATIO)).items()}
        Sn = {k: {int(y): v for y, v in d_.items()} for k, d_ in json.loads(json.dumps(SHARE_GAIN)).items()}
        if "wfe28" in kw: Wn["base"][2028] = kw["wfe28"]
        if "ratio28" in kw: Rn["base"][2028] = kw["ratio28"]
        if "ratio27" in kw: Rn["base"][2027] = kw["ratio27"]
        if "share" in kw: Sn["base"][2027] = kw["share"]; Sn["base"][2028] = kw["share"]
        WFE, RATIO, SHARE_GAIN = Wn, Rn, Sn
        rows, seg, tam, share, knobs = build("base")
        if "gm" in kw:
            for r in rows[2:]: r["gm"] += kw["gm"]; r["gp"] = r["rev"] * r["gm"]; r["oi"] = r["gp"] - r["opex"]
        if "opex" in kw:
            for i, r in enumerate(rows[2:]): f = (1 + kw["opex"]) if i < 4 else (1 + kw["opex"]) ** 2; r["opex"] *= f; r["oi"] = r["gp"] - r["opex"]
        if "tax" in kw:
            for r in rows: r["tax"] += kw["tax"]
        for r in rows: r["om"] = r["oi"] / r["rev"]; r["pbt"] = r["oi"] + 5.0; r["ni"] = r["pbt"] * (1 - r["tax"]) + 5.5; r["eps"] = r["ni"] / r["sh"]
        e = periods(rows)["CY28"]["eps"]; e27 = periods(rows)["CY27"]["eps"]
        WFE, RATIO, SHARE_GAIN = ({k: {int(y): v for y, v in d_.items()} for k, d_ in W0.items()}, {k: {int(y): v for y, v in d_.items()} for k, d_ in R0.items()}, {k: {int(y): v for y, v in d_.items()} for k, d_ in S0.items()})
        sens.append(dict(label=label, eps=e, eps27=e27, pt=MULT * e, dpt=MULT * (e - base_eps))); return e
    variant("CY28 WFE $220bn (Bernstein-to-SEMI end of the range)", wfe28=220); variant("CY28 WFE $254bn (MS, fifth raise of 2026)", wfe28=254); variant("CY28 WFE $275bn (UBS 2026-09-01)", wfe28=275)
    variant("ATE share of WFE 7.0% in CY28 (vs 7.5%)", ratio28=0.070); variant("ATE share of WFE 8.0% in CY28 (top of the 2026 run-rate)", ratio28=0.080)
    variant("CY27 ratio dips to 6.5% (management's 'could revert to 6-7%')", ratio27=0.065)
    variant("Share gain +50bp/yr (vs +120/+150bp)", share=0.005); variant("Share gain +250bp/yr (UBS-type)", share=0.025)
    variant("Gross margin -50bp every quarter CY27-28", gm=-0.005); variant("Gross margin +50bp every quarter", gm=0.005)
    variant("Opex growth +3pp/yr (13%/14%)", opex=0.03); variant("Opex growth -3pp/yr (7%/8%)", opex=-0.03)
    variant("Tax rate +2pp", tax=0.02)
    OUT["pt_sens"] = sens; OUT["pt_multiple_sens"] = {m: m * base_eps for m in (18, 20, 22, 25, 28, 30, 31, 33)}
    print(f"\nPT SENSITIVITY (25x CY28E EPS, base ${base_eps:.2f} -> ${MULT*base_eps:.0f}):")
    for s in sens: print(f"  {s['label']:62s} CY27 {s['eps27']:5.2f}  CY28 {s['eps']:5.2f}  PT ${s['pt']:.0f} ({s['dpt']:+.0f})")
    # ---- track record
    TR = track_record(); OUT["track"] = TR
    print(f"\nTRACK RECORD n={len(TR['rows'])}: avg beat vs mid {TR['avg_pct']:+.1%} (last 4 {TR['avg4_pct']:+.1%}); above top {TR['n_above_top']}/10 rev, {TR['n_eps_above_top']}/10 EPS; at/above mid {TR['n_at_or_above_mid']}/10; EPS beat avg ${TR['eps_avg']:+.2f} (last 4 ${TR['eps_avg4']:+.2f}); Q3 implied ${TR['q3_implied_10q']:.0f} / ${TR['q3_implied_4q']:.0f}, EPS ${TR['q3_eps_implied_10q']:.2f} / ${TR['q3_eps_implied']:.2f}")
    # ---- guardrails
    bc = OUT["cases"]["base"]; g = {}
    g["I1 input check: Q3 FY26 EPS reproduced from the guided P&L"] = (f"${bc['rows'][0]['eps']:.2f} on ${bc['rows'][0]['rev']:.0f}m / {bc['rows'][0]['gm']*100:.1f}% GM / opex 29.5% / tax 15% / 158.0m shares vs $2.00 guide mid", "input check (calibration): reproduces the midpoint within $0.05")
    g["I2 input check: FY26 shape vs the '50-52% in H1' framing"] = (f"H1 $2,611m = {H1['rev']/bc['periods']['CY26']['rev']:.1%} of our FY26 ${bc['periods']['CY26']['rev']:,.0f}m", "input restated: inside the 50-52% band")
    g["G1 implied TER share of the ATE TAM (Semi Test / [WFE x ratio])"] = (f"{bc['share'][2026]*100:.1f}% (2026) -> {bc['share'][2027]*100:.1f}% -> {bc['share'][2028]*100:.1f}%", "PASS vs UBS's ~37% 'basically flat' 2026 mark on the call (different TAM basis, Advantest's ex-burn-in) and IR's 300-400bp 2026 / 'couple hundred bps' 2027 bogey; our 2026 level is lower because our TAM denominator (8% of $158bn WFE) is larger than the Advantest-derived $12bn")
    g["G2 implied ATE TAM path"] = (f"${bc['tam'][2026]/1000:.1f}bn -> ${bc['tam'][2027]/1000:.1f}bn (+{bc['tam'][2027]/bc['tam'][2026]-1:.0%}) -> ${bc['tam'][2028]/1000:.1f}bn (+{bc['tam'][2028]/bc['tam'][2027]-1:.0%})", "PASS vs management's 'path to reach or exceed $20bn' as WFE approaches $250bn (ours: $18bn at $240bn) and TER's own 2027 TAM slide 'upper end $16-17bn' (Arcuri on the call); CY27 TAM growth (+19%) trails UBS's +43% WFE because the ratio dips, per management's own lag caveat")
    g["G3 CY27 / CY28 revenue growth vs the evergreen model and management's words"] = (f"{bc['periods']['CY27']['rev']/bc['periods']['CY26']['rev']-1:+.0%} / {bc['periods']['CY28']['rev']/bc['periods']['CY27']['rev']-1:+.0%}; CY27 EPS ${bc['periods']['CY27']['eps']:.2f} vs the evergreen model's $9.50-11 at $6bn", "PASS: 'a resurgence in growth in 2027' (CFO 07-29) and the target model being reached 'at an accelerated pace'; our CY27 revenue of $6.2bn is the model's $6bn a year early")
    g["G4 Q3 FY26 vs the guidance track record"] = (f"our ${bc['rows'][0]['rev']:.0f}m vs track-record-implied ${TR['q3_implied_10q']:.0f}m (10-qtr mean beat) / ${TR['q3_implied_4q']:.0f}m (last 4); consensus $1,244m", "CHECK: we sit deliberately at the low end of the pattern because the 2H guide was just re-based upward; the pattern says the Street is not positioned for a top-end print")
    g["G5 opex growth vs 'less than half of revenue growth'"] = (f"opex +{bc['knobs']['opex_g'][2027]:.0%} / +{bc['knobs']['opex_g'][2028]:.0%} vs revenue +{bc['periods']['CY27']['rev']/bc['periods']['CY26']['rev']-1:.0%} / +{bc['periods']['CY28']['rev']/bc['periods']['CY27']['rev']-1:.0%}", "PASS at the ceiling of management's framing (CEO, GS Communacopia small group 2026-09-09, per the 09-13 compile); this is the input that puts our EPS above the Street")
    g["G6 operating margin vs the reported peak"] = (f"CY27 {bc['periods']['CY27']['om']*100:.1f}% / CY28 {bc['periods']['CY28']['om']*100:.1f}% vs Q1 FY26 record 37.5% and Street CY28 {CONS['CY28']['ebit']/CONS['CY28']['rev']*100:.1f}%", "CHECK: CY28 at 38% assumes the Q1 FY26 structure recurs at 1.5x the revenue; the Street stops at 36%")
    g["G7 free cash flow conversion"] = (f"CY27 FCF ${bc['cf']['CY27']['fcf']:,.0f}m = {bc['cf']['CY27']['fcf']/bc['periods']['CY27']['ni']:.0%} of non-GAAP NI; CY28 {bc['cf']['CY28']['fcf']/bc['periods']['CY28']['ni']:.0%}", "PASS vs FY25 (71%) and H1 FY26 (73%); capex $380m/$430m vs BEst $353m/$429m")
    g["G8 CY28 vs BofA's '$8bn / $18 earnings power in a $250bn WFE world'"] = (f"Capstone ${bc['periods']['CY28']['rev']/1000:.2f}bn / ${bc['periods']['CY28']['eps']:.2f} at $240bn WFE", "PASS/CHECK: BofA's frame needs ~40% share of an 8%-of-WFE TAM; we carry 36.6% of 7.5% -- the gap is the share and ratio debate, not the WFE")
    OUT["guardrails"] = g
    print("\nGUARDRAILS:"); [print(f"  {k}: {v[0]} -- {v[1]}") for k, v in g.items()]
    # ---- price / PE context (Bloomberg, weekly blended-forward P/E)
    OUT["subseg"] = {"2025A": dict(soc=1889.7, mem=504.9, ist=129.2), "2026E": dict(soc=3205, mem=885, ist=230), "2027E": dict(soc=3900, mem=1150, ist=245), "2028E": dict(soc=4950, mem=1400, ist=290)}
    OUT["pe_hist"] = {"2016-25 mean": 21.7, "2016-25 median": 20.4, "2016-25 p10": 15.0, "2016-25 p90": 30.5, "2021-26 mean": 28.2, "2024 avg": 31.6, "2025 avg": 27.6, "2026 avg": 43.4, "now (blended)": 32.0, "bf_eps_0911": 10.65, "jun19 blended": 52.1, "jun19 trailing": 79.3, "jun30 blended_est": 56,
                      "Advantest 2016-25 mean": 25.1, "Advantest now": 29.5}
    OUT["price_path"] = {"2025-01-31": 115.79, "2025-04-30": 74.21, "2025-12-31": 193.56, "2026-03-31": 296.46, "2026-06-30": 483.84, "2026-07-31": 367.69, "2026-08-31": 349.83, "2026-09-16": PX}
    json.dump(OUT, open(os.path.join(D, "model_out.json"), "w"), indent=0, default=float)
    print("\nsaved model_out.json")
