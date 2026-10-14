# -*- coding: utf-8 -*-
"""Recalculate Template DCF CRWV.xlsx in MY OWN Excel COM instance (DispatchEx — never the user's Excel), create the
revenue/GW x EBITDA-margin Data Table, scan error cells, save (caches values), then compare Excel values with an
independent Python replica of the model chain at named checkpoints."""
import os, sys, json
import win32com.client as win32, pythoncom
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_crwv_model as B

FN = "Template DCF CRWV.xlsx"
PATH = os.path.join(HERE, FN)
lay = json.load(open(os.path.join(HERE, "layout.json")))
R, pl, val, mm, dsc = lay["R"], lay["pl"], lay["val"], lay["mm"], lay["dsc"]
assert not os.path.exists(os.path.join(HERE, "~$" + FN)), "lock file present"

xl = win32.DispatchEx("Excel.Application"); xl.Visible = False; xl.DisplayAlerts = False
try:
    wb = xl.Workbooks.Open(PATH, UpdateLinks=0)
    ws = wb.Worksheets(B.SH_COVER)
    g2 = int(val["grid2"])
    rng = ws.Range(f"F{g2+1}:L{g2+5}")
    rng.Table(RowInput=ws.Range("D6"), ColumnInput=ws.Range("E6"))
    g3 = int(val["grid3"])
    ws.Range(f"F{g3+1}:K{g3+5}").Table(RowInput=ws.Range("F6"), ColumnInput=ws.Range("G6"))
    xl.CalculateFullRebuild()
    errs = []
    for sh in wb.Worksheets:
        ur = sh.UsedRange; vals = ur.Value; r0, c0 = ur.Row, ur.Column
        for i, rowv in enumerate(vals):
            for j, v in enumerate(rowv):
                if isinstance(v, int) and v < -2146000000:
                    errs.append((sh.Name, sh.Cells(r0 + i, c0 + j).Address(False, False), v))
    print(f"error cells: {len(errs)}" + (f" -> {errs[:15]}" if errs else ""))
    grid2 = ws.Range(f"F{g2+1}:L{g2+5}").Value
    grid3 = ws.Range(f"F{g3+1}:K{g3+5}").Value
    wb.Save(); wb.Close(SaveChanges=False)
finally:
    xl.Quit(); del xl

# ---------------------------------------------------------------- python replica
import openpyxl
wbv = openpyxl.load_workbook(PATH, data_only=True)
C = wbv[B.SH_COVER]; Pm = wbv[B.SH_PREM]
Y = B.YEARS; COLS = B.COLS
def row(r): return {y: C[f"{COLS[i]}{r}"].value for i, y in enumerate(Y)}
def prow(key): return {y: Pm[f"{COLS[i]}{R[key]}"].value for i, y in enumerate(Y)}
def ps(key): return Pm[f"D{R[key]}"].value

adds = {2023: 70, 2024: 290, 2025: 490}; adds.update(B.ADDS_IN)
ye = {2023: 70, 2024: 360, 2025: 850}
for y in Y:
    if y >= 2036: adds[y] = ye[y - 1] * ps("g_fleet")
    if y >= 2026: ye[y] = ye[y - 1] + adds[y]
lag = ps("lag"); prebuild = ps("prebuild"); life = int(C["F6"].value); repl = C["G6"].value
mult = C["D6"].value; adj = C["E6"].value
rev = dict(B.REV); rev[2026] = (ps("g_rev_lo") + ps("g_rev_hi")) / 2
bill = {y: (ps("bill_2026") if y == 2026 else ye[y - 1] + (0.5 - lag) * adds[y]) for y in Y if y >= 2024}
revgw = {}
for y in Y:
    if y >= 2027:
        revgw[y] = B.REVGW[y] * mult; rev[y] = bill[y] * revgw[y]
avg = {y: (ye[y - 1] + ye[y]) / 2 for y in Y if y >= 2024}
ebitda_ref = {2024: 1226, 2025: 3098}
ebitda = {y: ebitda_ref[y] for y in (2024, 2025)}
for y in Y:
    if y >= 2026: ebitda[y] = rev[y] * (B.EBITDA_M[y] + (adj if y >= 2027 else 0))
da = {2023: 103, 2024: 863, 2025: 2454}
for y in Y:
    if y >= 2026: da[y] = avg[y] * B.DA_GW[y]
sbc = {2023: 15, 2024: 31, 2025: 630}
for y in Y:
    if y >= 2026: sbc[y] = rev[y] * B.SBC[y]
ebit = {y: ebitda[y] - da[y] - sbc[y] for y in Y if y >= 2024}
nopat = {y: ebit[y] * (1 - B.TAX[y]) for y in Y if y >= 2026}
capex = {2023: 2943, 2024: 8702, 2025: 10309, 2026: (ps("g_capex_lo") + ps("g_capex_hi")) / 2}
cg, cr = {}, {}; replaced = {}; installed = {}
for i, y in enumerate(Y):
    k = i + 1 - life
    replaced[y] = installed[Y[k - 1]] if k >= 1 else 0
    installed[y] = adds[y] + replaced[y]
    if y >= 2026:
        nxt = adds[Y[i + 1]] if i + 1 < len(Y) else adds[y]
        cg[y] = B.BUILD[y] * ((1 - prebuild) * adds[y] + prebuild * nxt)
        cr[y] = replaced[y] * B.BUILD[y] * repl
        if y >= 2027: capex[y] = cg[y] + cr[y]
nwc = {2024: 417 - 4064, 2025: 3169 - 8185}
for y in Y:
    if y >= 2026: nwc[y] = rev[y] * B.NWC[y]
dnwc = {y: -(nwc[y] - nwc[y - 1]) for y in Y if y >= 2025}
fcff = {y: nopat[y] + da[y] - capex[y] + dnwc[y] for y in Y if y >= 2026}
import datetime as dt
vd = ps("val_date"); wacc = ps("wacc"); g = ps("g"); roic = ps("roic")
pv = 0.0; t = {}
for y in Y:
    d = dt.datetime(y, 12, 31); t[y] = max(0, (d - vd).days / 365)
    frac = max(0, min(1, (d - vd).days / ((d - dt.datetime(y, 1, 1)).days + 1)))
    if y >= 2026: pv += fcff[y] * frac / (1 + wacc) ** t[y]
nop_t = nopat[2045] * (1 + g); fcff_t = nop_t * (1 - g / roic); tv = fcff_t / (wacc - g); pvtv = tv / (1 + wacc) ** t[2045]
ev = pv + pvtv; nd = ps("debt") - ps("cash"); eq = ev - nd; psh = eq / ps("shares")
# debt roll / eps
ndr = {2025: ps("nd_2025")}; intr = {}; ni = {}; eps = {}
for y in Y:
    if y >= 2026:
        intr[y] = (ndr[y - 1] - 0.5 * fcff[y]) * B.KD[y]
        ndr[y] = ndr[y - 1] - fcff[y] + intr[y] - (ps("eq_2026") if y == 2026 else 0)
        x = (ebitda[y] - da[y]) - intr[y]; ni[y] = x * (1 - B.TAX[y]) if x > 0 else x; eps[y] = ni[y] / B.SH[y]

checks = [
    ("rev 2026", C[f"G15"].value, rev[2026]), ("rev 2027", C["H15"].value, rev[2027]), ("rev 2028", C["I15"].value, rev[2028]), ("rev 2030", C["K15"].value, rev[2030]),
    ("bill 2027", C["H11"].value, bill[2027]), ("revgw 2026", C["G12"].value, rev[2026] / bill[2026]),
    ("ebitda 2027", C[f"H{pl['ebitda']}"].value, ebitda[2027]), ("da 2028", C[f"I{pl['da']}"].value, da[2028]),
    ("aoi 2026", C[f"G{pl['aoi']}"].value, ebitda[2026] - da[2026]), ("ebit 2028", C[f"I{pl['ebit']}"].value, ebit[2028]),
    ("capex 2027", C[f"H{pl['capex']}"].value, -capex[2027]), ("capex 2030", C[f"K{pl['capex']}"].value, -capex[2030]), ("capex_r 2031", C[f"L{pl['capex_r']}"].value, -cr[2031]),
    ("fcff 2026", C[f"G{pl['fcff']}"].value, fcff[2026]), ("fcff 2028", C[f"I{pl['fcff']}"].value, fcff[2028]), ("fcff 2035", C[f"P{pl['fcff']}"].value, fcff[2035]), ("fcff 2045", C[f"Z{pl['fcff']}"].value, fcff[2045]),
    ("pvx", C[f"D{val['pvx']}"].value, pv), ("pvtv", C[f"D{val['pvtv']}"].value, pvtv), ("ev", C[f"D{val['ev']}"].value, ev), ("per share", C[f"D{val['ps']}"].value, psh),
    ("nd 2027", C[f"H{mm['nd']}"].value, ndr[2027]), ("int 2027", C[f"H{mm['int']}"].value, intr[2027]), ("eps 2027", C[f"H{mm['eps']}"].value, eps[2027]), ("eps 2028", C[f"I{mm['eps']}"].value, eps[2028]),
    ("grid center", C[f"I{val['grid_center_row']}"].value, psh),
]
bad = 0
for name, xv, rv in checks:
    ok = xv is not None and abs(xv - rv) <= 1e-6 * max(1, abs(rv))
    bad += not ok
    print(f"  {'OK ' if ok else 'BAD'} {name:14s} excel={xv!s:>18} replica={rv:,.4f}")
print("ALL OK" if not bad else f"MISMATCHES: {bad}")
print("\n--- key outputs ---")
for y in (2025, 2026, 2027, 2028, 2029, 2030, 2032, 2035, 2040, 2045):
    print(f"{y}: YE {ye[y]:,.0f} MW | repl {replaced[y]:,.0f} | rev {rev[y]:,.0f} | rev/GW {rev[y]/bill[y] if y>=2024 else 0:,.1f} | EBITDA {ebitda.get(y,0):,.0f} ({ebitda.get(y,0)/rev[y]:.0%}) | D&A {da.get(y,0):,.0f} | AOI {ebitda.get(y,0)-da.get(y,0):,.0f} | capex {capex.get(y,0):,.0f} | FCFF {fcff.get(y,0):,.0f} | ND {ndr.get(y,0):,.0f} | EPS {eps.get(y,0):,.2f}")
print(f"PV explicit {pv:,.0f} | PV TV {pvtv:,.0f} ({pvtv/ev:.0%} of EV) | EV {ev:,.0f} | net debt {nd:,.0f} | equity {eq:,.0f} | per share {psh:,.2f}")
print("grid2 (rows = EBITDA adj; cols = rev/GW mult):")
for rowv in grid2: print("   ", ["%.2f" % v if isinstance(v, (int, float)) else v for v in rowv])
print("grid3 (rows = repl share; cols = life):")
for rowv in grid3: print("   ", ["%.2f" % v if isinstance(v, (int, float)) else v for v in rowv])
ue = val["ue"]
print("unit economics 2035/GW:", {k: round(C[f"D{v}"].value, 3) for k, v in ue.items()})
json.dump({"per_share": psh, "ev": ev, "nd": nd, "rev": rev, "ebitda": ebitda, "fcff": fcff, "eps": eps, "nd_roll": ndr, "grid2": grid2, "grid3": grid3, "ue": {k: C[f"D{v}"].value for k, v in val["ue"].items()}}, open(os.path.join(HERE, "model_out.json"), "w"), indent=1, default=str)
