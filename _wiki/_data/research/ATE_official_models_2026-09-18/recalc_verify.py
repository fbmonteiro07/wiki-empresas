# -*- coding: utf-8 -*-
"""Recalculate the two built workbooks in MY OWN Excel COM instance (DispatchEx; never touches the user's Excel), scan for
error cells, save (caches values), then compare Excel values with the Python replica at named checkpoints."""
import os, sys, json, time
import win32com.client as win32, pythoncom
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ate_replica import compare

FILES = [("ADV", "Template DCF ADVANTEST.xlsx"), ("TER", "Template DCF TER.xlsx")]
xl = win32.DispatchEx("Excel.Application"); xl.Visible = False; xl.DisplayAlerts = False
try:
    for tk, fn in FILES:
        p = os.path.join(HERE, fn)
        assert not os.path.exists(os.path.join(HERE, "~$" + fn)), "lock file present"
        wb = xl.Workbooks.Open(p, UpdateLinks=0)
        xl.CalculateFullRebuild()
        errs = []
        for ws in wb.Worksheets:
            ur = ws.UsedRange
            vals = ur.Value
            r0, c0 = ur.Row, ur.Column
            for i, rowv in enumerate(vals):
                for j, v in enumerate(rowv):
                    if isinstance(v, int) and v < -2146000000:   # COM error values arrive as ints (#VALUE! = -2146826273)
                        errs.append((ws.Name, ws.Cells(r0 + i, c0 + j).Address(False, False), v))
        print(f"{tk}: {len(errs)} error cells" + (f" -> {errs[:12]}" if errs else ""))
        wb.Save(); wb.Close(SaveChanges=False)
finally:
    xl.Quit(); del xl

lay = json.load(open(os.path.join(HERE, "layout.json")))
allok = True
for tk, fn in FILES:
    L = lay["adv" if tk == "ADV" else "ter"]
    L["R"] = {k: int(v) for k, v in L["R"].items()}
    for k in ("pl", "val"):
        L[k] = {kk: (int(vv) if isinstance(vv, (int, str)) and str(vv).isdigit() else vv) for kk, vv in L[k].items()}
    L["wiki"] = int(L["wiki"])
    res, out, v = compare(os.path.join(HERE, fn), tk, L)
    bad = [r for r in res if not r[4]]
    allok &= not bad
    print(f"== {tk}: {len(res)} checkpoints, {len(bad)} mismatches; per share (replica) = {v['ps']:,.2f}; TV/EV {v['tvshare']:.1%}")
    for r in res:
        if not r[4] or r[0] in ("per share", "ev", "rev 2026", "rev 2027", "rev 2028", "eps 2026", "eps 2027", "eps 2028"):
            print(f"  {'OK ' if r[4] else 'BAD'} {r[0]:14s} {r[1]:6s} excel={r[2]!s:>18} replica={r[3]:,.4f}")
print("ALL OK" if allok else "MISMATCHES")
