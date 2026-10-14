# -*- coding: utf-8 -*-
"""Print the wiki 'Capstone estimates (house model)' table + key lines from the recalculated workbook (cached values)."""
import os, sys, json, openpyxl
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
lay = json.load(open(os.path.join(HERE, "layout.json")))
pl, val, mm = lay["pl"], lay["val"], lay["mm"]
wb = openpyxl.load_workbook(os.path.join(HERE, "Template DCF CRWV.xlsx"), data_only=True)
C = wb["DCF Cover - Base"]
cols = {2024: "E", 2025: "F", 2026: "G", 2027: "H", 2028: "I", 2029: "J", 2030: "K"}
def v(r, y): return C[f"{cols[y]}{r}"].value
rows = [
    ("Revenue ($bn)", lambda y: f"{v(15, y)/1000:.2f}"),
    ("Active power, year-end (GW IT load)", lambda y: f"{v(8, y)/1000:.2f}"),
    ("Revenue per billable GW ($bn/GW-yr)", lambda y: f"{v(12, y):.1f}"),
    ("Adj. EBITDA ($bn)", lambda y: f"{v(pl['ebitda'], y)/1000:.2f}"),
    ("Adj. EBITDA margin", lambda y: f"{v(pl['ebitdam'], y):.1%}"),
    ("Adj. operating income (AOI, $bn)", lambda y: f"{v(pl['aoi'], y)/1000:.2f}"),
    ("Capex ($bn)", lambda y: f"{-v(pl['capex'], y)/1000:.1f}"),
    ("FCFF ($bn)", lambda y: ("n/a" if y < 2026 else f"{v(pl['fcff'], y)/1000:.1f}")),
    ("Net debt, year-end ($bn, memo roll)", lambda y: ("n/a" if y < 2025 else f"{v(mm['nd'], y)/1000:.1f}")),
    ("EPS ($) — CY24-25 GAAP reported, CY26+ adjusted", lambda y: f"{v(lay['wiki']+10, y):.2f}"),
]
yrs = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
print("| | " + " | ".join(f"CY{str(y)[2:]}{'A' if y <= 2025 else 'E'}" for y in yrs) + " |")
print("|---|" + "--:|" * len(yrs))
for name, f in rows:
    cells = []
    for y in yrs:
        try: cells.append(f(y))
        except Exception: cells.append("n/a")
    print(f"| {name} | " + " | ".join(cells) + " |")
print()
ps = C[f"D{val['ps']}"].value; ev = C[f"D{val['ev']}"].value; nd = C[f"D{val['netdebt']}"].value; tvs = C[f"D{val['tvshare']}"].value
print(f"DCF per share ${ps:.2f} | EV {ev:,.0f} | net debt {nd:,.0f} | TV/EV {tvs:.0%} | PV explicit {C[f'D{val[chr(112)+chr(118)+chr(120)]}'].value:,.0f}")
ue = val["ue"]
print("unit econ 2035:", {k: round(C[f"D{r}"].value, 2) for k, r in ue.items()})
g2 = int(val["grid2"]); g3 = int(val["grid3"])
print("grid2:"); [print("  ", [round(x, 0) if isinstance(x, (int, float)) else x for x in [C.cell(row=rr, column=cc).value for cc in range(6, 13)]]) for rr in range(g2 + 1, g2 + 6)]
print("grid3:"); [print("  ", [round(x, 0) if isinstance(x, (int, float)) else x for x in [C.cell(row=rr, column=cc).value for cc in range(6, 12)]]) for rr in range(g3 + 1, g3 + 6)]
rec = int(lay["rec"])
print("reconciliations:")
for rr in range(rec + 1, rec + 14):
    lab = C[f"C{rr}"].value
    if not lab: continue
    vals = [C.cell(row=rr, column=cc).value for cc in range(4, 12)]
    print("  ", lab[:90], "|", [round(x, 3) if isinstance(x, (int, float)) else x for x in vals if x is not None][:8])
