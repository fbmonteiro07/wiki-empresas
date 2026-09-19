# -*- coding: utf-8 -*-
"""Bloomberg pull for the ATE consolidated workbook (Fernanda-style): calendarised BC annuals 2018-2028, quarterly actuals
(FUND_PER=Qn + EQY_FUND_YEAR), quarterly consensus 1FQ..8FQ, FY actuals, and product-line segments (PG_REVENUE) annual + quarterly."""
import sys, json, time, os
sys.path.insert(0, r"E:\bloomberg_api"); sys.stdout.reconfigure(encoding="utf-8")
from bloomberg import bdp, bds
HERE = os.path.dirname(os.path.abspath(__file__))
T = ["6857 JP Equity", "TER US Equity"]
def key(tk): return tk.split()[0]
def tidy(df):
    out = {}
    for _, r in df.iterrows():
        v = r["value"]
        try:
            if v != v: v = None
        except Exception: pass
        if hasattr(v, "isoformat"): v = v.isoformat()
        out.setdefault(key(r["ticker"]), {})[r["field"]] = v
    return out
def call(fn, *a, **kw):
    for i in range(3):
        try: return fn(*a, **kw)
        except Exception as e:
            print("  retry", i, type(e).__name__, str(e)[:120]); time.sleep(4)
    raise SystemExit("bbg failed: " + str(kw))
t0 = time.time()
CYF = ["BEST_SALES", "BEST_GROSS_MARGIN", "BEST_OPP", "BEST_EBIT", "BEST_NET_INCOME", "BEST_EPS", "BEST_EPS_GAAP", "BEST_ESTIMATE_FCF", "BEST_CAPEX", "BEST_SALES_NUMEST", "BEST_EPS_NUMEST"]
cy = {}
for y in range(2018, 2029):
    cy[y] = tidy(call(bdp, T, CYF, BEST_FPERIOD_OVERRIDE=f"{y}BC"))
print("BC done", f"{time.time()-t0:.0f}s")
json.dump(cy, open(os.path.join(HERE, "ate_cy_bc.json"), "w"), indent=1, default=str)
QF = ["PERIOD_END_DT", "SALES_REV_TURN", "GROSS_PROFIT", "IS_OPER_INC", "NET_INCOME", "IS_ADJUSTED_NET_INCOME", "IS_DILUTED_EPS", "IS_COMP_EPS_ADJUSTED", "IS_SH_FOR_DILUTED_EPS", "CF_FREE_CASH_FLOW", "CF_CASH_FROM_OPER", "CAPITAL_EXPEND"]
qa = {}
for y in range(2018, 2028):
    for q in (1, 2, 3, 4):
        qa[f"{y}Q{q}"] = tidy(call(bdp, T, QF, FUND_PER=f"Q{q}", EQY_FUND_YEAR=y))
print("Q actuals done", f"{time.time()-t0:.0f}s")
json.dump(qa, open(os.path.join(HERE, "ate_q_actuals.json"), "w"), indent=1, default=str)
QC = ["BEST_PERIOD_END_DATE", "BEST_SALES", "BEST_GROSS_MARGIN", "BEST_OPP", "BEST_EBIT", "BEST_NET_INCOME", "BEST_EPS", "BEST_EPS_GAAP", "BEST_ESTIMATE_FCF", "BEST_SALES_NUMEST"]
qc = {}
for k in range(1, 9):
    qc[k] = tidy(call(bdp, T, QC, BEST_FPERIOD_OVERRIDE=f"{k}FQ"))
print("Q cons done", f"{time.time()-t0:.0f}s")
json.dump(qc, open(os.path.join(HERE, "ate_q_cons.json"), "w"), indent=1, default=str)
YF = ["PERIOD_END_DT", "SALES_REV_TURN", "GROSS_MARGIN", "IS_OPER_INC", "NET_INCOME", "IS_ADJUSTED_NET_INCOME", "IS_DILUTED_EPS", "IS_COMP_EPS_ADJUSTED", "IS_SH_FOR_DILUTED_EPS", "CF_FREE_CASH_FLOW"]
fy = {}
for y in range(2018, 2027):
    fy[y] = tidy(call(bdp, T, YF, FUND_PER="Y", EQY_FUND_YEAR=y))
json.dump(fy, open(os.path.join(HERE, "ate_fy_actuals.json"), "w"), indent=1, default=str)
print("FY done", f"{time.time()-t0:.0f}s")
# segments: quarterly PG_REVENUE per fiscal quarter (test the override), plus the default latest-5 window
def seg(df):
    rows = []; cur = None
    for _, r in df.iterrows():
        nm, v = r["name"], r["value"]
        if nm == "Metric Name": cur = {"name": v, "vals": {}}; rows.append(cur)
        elif nm == "Product Geographic Hierarchy Level": cur["lvl"] = float(v)
        elif str(nm).startswith("Period"): cur["vals"][nm] = v
    return rows
segq = {}
for tk in T:
    segq[key(tk)] = {"latest5": seg(call(bds, [tk], ["PG_REVENUE"], FUND_PER="Q"))}
    for y in range(2023, 2028):
        for q in (1, 2, 3, 4):
            try:
                d = bds([tk], ["PG_REVENUE"], FUND_PER=f"Q{q}", EQY_FUND_YEAR=y)
                segq[key(tk)][f"{y}Q{q}"] = seg(d)
            except Exception as e:
                segq[key(tk)][f"{y}Q{q}"] = {"error": str(e)[:150]}
    print("segments", tk, f"{time.time()-t0:.0f}s")
json.dump(segq, open(os.path.join(HERE, "ate_seg_q.json"), "w"), indent=1, default=str)
sega = {}
for tk in T:
    sega[key(tk)] = {}
    for y in range(2019, 2027):
        try: sega[key(tk)][y] = seg(bds([tk], ["PG_REVENUE"], FUND_PER="A", EQY_FUND_YEAR=y))
        except Exception as e: sega[key(tk)][y] = {"error": str(e)[:150]}
json.dump(sega, open(os.path.join(HERE, "ate_seg_a.json"), "w"), indent=1, default=str)
print("ALL DONE", f"{time.time()-t0:.0f}s")
# quick peek: Advantest quarterly segment override test
s = segq["6857"].get("2025Q4"); print("6857 2025Q4 (Jan-Mar 2025 if end-year labelling):", [(r["name"], r["vals"].get("Period 1 Value")) for r in s][:6] if isinstance(s, list) else s)
s = segq["TER"].get("2025Q1"); print("TER 2025Q1:", [(r["name"], r["vals"].get("Period 1 Value")) for r in s][:6] if isinstance(s, list) else s)
