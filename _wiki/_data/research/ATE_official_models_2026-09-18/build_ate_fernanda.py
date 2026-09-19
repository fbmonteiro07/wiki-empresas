# -*- coding: utf-8 -*-
"""ATE Consolidado Advantest + TER.xlsx — Fernanda-style calendar-year workbook for the two ATE names, plus revenue build-up,
mix, regions and customer tables. Data: Bloomberg pulls (ate_*.json, 2026-09-18), the two official models (Template DCF
ADVANTEST / TER, cached values), 10-K / tanshin / deck disclosures. Convention copied from
_wiki/models/cyber-software-financials-CY2019-2028.xlsx: black = actual, blue = estimate; CY = Bloomberg '<yr>BC' calendarisation;
GAAP/IFRS rows = reported fiscal quarters day-prorated into calendar years."""
import os, json, datetime as dt, calendar
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L

HERE = os.path.dirname(os.path.abspath(__file__))
ASOF = "2026-09-18"
cy = json.load(open(os.path.join(HERE, "ate_cy_bc.json"))); qa = json.load(open(os.path.join(HERE, "ate_q_actuals.json")))
qc = json.load(open(os.path.join(HERE, "ate_q_cons.json"))); segq = json.load(open(os.path.join(HERE, "ate_seg_q.json"))); sega = json.load(open(os.path.join(HERE, "ate_seg_a.json")))
LAY = json.load(open(os.path.join(HERE, "layout.json")))
ADV_X = os.path.join(HERE, "Template DCF ADVANTEST.xlsx"); TER_X = os.path.join(HERE, "Template DCF TER.xlsx")
OUT = os.path.join(HERE, "ATE Consolidado Advantest + TER.xlsx")
YEARS = list(range(2019, 2029)); HOUSE_YEARS = {2026, 2027, 2028}
CQ = [(2025, 1), (2025, 2), (2025, 3), (2025, 4), (2026, 1), (2026, 2), (2026, 3), (2026, 4)]
CO = {"6857": dict(name="Advantest (6857 JP)", fye=3, ccy="JPY", unit="JPY mm", eps_u="JPY"), "TER": dict(name="Teradyne (TER US)", fye=12, ccy="USD", unit="USD mm", eps_u="USD")}
TK = ["6857", "TER"]
FX_CY = {2018: 111.30, 2019: 109.00, 2020: 106.35, 2021: 110.43, 2022: 131.73, 2023: 141.43, 2024: 151.92, 2025: 149.96, 2026: 157.0, 2027: 150.0, 2028: 150.0}
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LOG = []

BLK = Font(name="Arial", size=10, color="FF000000"); BLU = Font(name="Arial", size=10, color="FF0000FF"); GRY = Font(name="Arial", size=9, color="FF666666")
BLD = Font(name="Arial", size=10, bold=True); TIT = Font(name="Arial", size=14, bold=True, color="FF203864"); WHT = Font(name="Arial", size=10, bold=True, color="FFFFFFFF")
FILL_H = PatternFill("solid", fgColor="FFDCE6F1"); FILL_S = PatternFill("solid", fgColor="FF203864"); FILL_B = PatternFill("solid", fgColor="FFF2F2F2")
NF_N = '#,##0;(#,##0);"-"'; NF_N1 = '#,##0.0;(#,##0.0);"-"'; NF_N2 = '0.00;(0.00);"-"'; NF_P = '0.0%;(0.0%);"-"'; NF_X = '0.0"x"'


def fnum(v):
    try:
        return None if v is None or v != v else float(v)
    except Exception:
        return None


def eom(y, m): return dt.date(y, m, calendar.monthrange(y, m)[1])


def infer_period_end(t, fy, q):
    fye = CO[t]["fye"]; m = ((fye + 3 * q - 1) % 12) + 1; y = fy if m <= fye else fy - 1
    return eom(y, m)


def snap(d):
    best = None
    for yy in (d.year - 1, d.year, d.year + 1):
        for q, mo in enumerate([3, 6, 9, 12], 1):
            dist = abs((d - eom(yy, mo)).days)
            if best is None or dist < best[0]: best = (dist, yy, q)
    return best[1], best[2]


def fq_label(t, d):
    fye = CO[t]["fye"]; fy = d.year if d.month <= fye else d.year + 1; q = ((d.month - fye - 1) % 12) // 3 + 1
    adv = f" = FQ{q} FY{str(fy-1)[2:]} na convenção Advantest" if t == "6857" else ""
    return f"FQ{q} FY{str(fy)[2:]} (ended {d.day:02d}-{MON[d.month-1]}-{str(d.year)[2:]}){adv}"


# ------------------------------------------------------------------ quarterly actuals → rows with dates
QROWS = {t: [] for t in TK}
for k, rows in qa.items():
    fy, q = int(k[:4]), int(k[5])
    for t in TK:
        r = rows.get(t)
        if not r or r.get("SALES_REV_TURN") is None: continue
        ped = r.get("PERIOD_END_DT")
        d = dt.date.fromisoformat(ped[:10]) if ped else infer_period_end(t, fy, q)
        if not ped: LOG.append(f"{t} {k}: PERIOD_END_DT ausente — inferido {d} do calendário fiscal")
        rr = dict(r); rr["_end"] = d; rr["_fy"] = fy; rr["_q"] = q; rr["_key"] = k
        QROWS[t].append(rr)
for t in TK:
    QROWS[t].sort(key=lambda r: r["_end"])
    for i, r in enumerate(QROWS[t]):
        r["_start"] = (QROWS[t][i - 1]["_end"] + dt.timedelta(days=1)) if i and (r["_end"] - QROWS[t][i - 1]["_end"]).days < 120 else r["_end"] - dt.timedelta(days=90)


def prorate(t, field, weighted=False, rows=None):
    acc = {}; days = {}
    for r in (rows if rows is not None else QROWS[t]):
        v = fnum(r.get(field))
        if v is None: continue
        s, e = r["_start"], r["_end"]; tot = (e - s).days + 1
        for y in sorted({s.year, e.year}):
            ys, ye = dt.date(y, 1, 1), dt.date(y, 12, 31); lo, hi = max(s, ys), min(e, ye)
            if lo > hi: continue
            n = (hi - lo).days + 1; w = n / tot
            acc[y] = acc.get(y, 0.0) + (v * n if weighted else v * w); days[y] = days.get(y, 0) + n
    out = {}
    for y, n in days.items():
        if n >= 0.99 * (366 if calendar.isleap(y) else 365): out[y] = acc[y] / n if weighted else acc[y]
    return out


PR = {}
for t in TK:
    PR[t] = {f: prorate(t, f) for f in ["SALES_REV_TURN", "GROSS_PROFIT", "IS_OPER_INC", "NET_INCOME", "IS_ADJUSTED_NET_INCOME", "CF_FREE_CASH_FLOW", "CF_CASH_FROM_OPER", "CAPITAL_EXPEND", "IS_DILUTED_EPS"]}
    PR[t]["SHARES"] = prorate(t, "IS_SH_FOR_DILUTED_EPS", weighted=True)


def bc(t, y, f): return fnum(cy.get(str(y), {}).get(t, {}).get(f))
def is_actual(t, y): return bc(t, y, "BEST_SALES") is not None and (bc(t, y, "BEST_SALES_NUMEST") or 0) == 0


# method check
worst = 0.0
for t in TK:
    for y in YEARS:
        if is_actual(t, y) and y in PR[t]["SALES_REV_TURN"] and bc(t, y, "BEST_SALES"):
            d = PR[t]["SALES_REV_TURN"][y] / bc(t, y, "BEST_SALES") - 1; worst = max(worst, abs(d))
            if abs(d) > 0.004: LOG.append(f"{t} CY{y}: receita reportada pró-rateada {PR[t]['SALES_REV_TURN'][y]:,.0f} vs BC Bloomberg {bc(t, y, 'BEST_SALES'):,.0f} ({d:+.2%})")
LOG.insert(0, f"MÉTODO: máx |receita pró-rateada − Bloomberg BC| nos anos completos = {worst:.2%}")

# ------------------------------------------------------------------ segments (PG_REVENUE)
def seg_map(rows, lvl=None):
    """rows: list of {name, lvl, vals{'Period k Value'}} → {name: value of Period 1}."""
    out = {}
    if not isinstance(rows, list): return out
    for r in rows:
        if lvl is not None and r.get("lvl") != lvl: continue
        v = fnum(r.get("vals", {}).get("Period 1 Value")); nm = str(r["name"]).replace(" ", " ").strip()
        if v is not None and nm not in out: out[nm] = v
    return out


SEG_Q = {t: {} for t in TK}   # end-date -> {segment: value}
def seg_total(t, m):
    if t == "6857": a, b = m.get("Test System Business"), m.get("Services & Others"); return None if (a is None or b is None) else a + b
    a, b, c = m.get("Semiconductor Test"), (m.get("Product Test") if m.get("Product Test") is not None else m.get("All Other")), m.get("Robotics")
    if a is None: return None
    if b is None: b = (m.get("System Test") or 0) + (m.get("Wireless Test") or 0)
    return a + b + (c or 0)
def maps_from(rows, keys=("Period 1 Value",)):
    out = []
    for pk in keys:
        mm = {}
        for r in rows:
            v = fnum(r.get("vals", {}).get(pk)); nm = str(r["name"]).replace("\xa0", " ").strip()
            if v is not None and nm not in mm: mm[nm] = v
        out.append(mm)
    return out
for t in TK:
    # (2) latest-5 window by order
    recent = sorted(QROWS[t], key=lambda r: r["_end"])[-5:][::-1]
    for rr, m in zip(recent, maps_from(segq[t].get("latest5", []), ("Period 1 Value", "Period 2 Value", "Period 3 Value", "Period 4 Value", "Period 5 Value"))):
        tot = seg_total(t, m); rev = fnum(rr.get("SALES_REV_TURN"))
        if tot and rev and abs(tot / rev - 1) < 0.01: SEG_Q[t][rr["_end"]] = m
        else: LOG.append(f"{t} latest5 {rr['_end']}: total de segmentos {tot} vs receita {rev} — descartado")
    # (1) key-based with consistency check
    for k, rows in segq[t].items():
        if k == "latest5" or not isinstance(rows, list): continue
        m = maps_from(rows)[0]; tot = seg_total(t, m)
        rr = next((r for r in QROWS[t] if r["_key"] == k), None)
        if rr is None or not tot: continue
        rev = fnum(rr.get("SALES_REV_TURN"))
        if rev and abs(tot / rev - 1) < 0.01:
            SEG_Q[t].setdefault(rr["_end"], m)
        else:
            LOG.append(f"{t} {k} ({rr['_end']}): total de segmentos {tot:,.0f} ≠ receita reportada {rev:,.0f} — BBG devolveu outro período; descartado")
    LOG.append(f"{t}: {len(SEG_Q[t])} trimestres com segmentos: {', '.join(d.isoformat() for d in sorted(SEG_Q[t]))}")
SEG_A = {t: {} for t in TK}   # BBG fiscal year (end-year label) -> {segment: value}
for t in TK:
    for y, rows in sega[t].items():
        m = seg_map(rows)
        if m: SEG_A[t][int(y)] = m

ADV_SEGNAMES = {"soc": ["SoC Test Systems", "SoC"], "mem": ["Memory Test Systems", "Memory"], "oth": ["Other Systems", "Mechatronics Systems"], "so": ["Services & Others", "Services, Support & Others"]}
TER_SEGNAMES = {"semi": ["Semiconductor Test"], "soc": ["SOC"], "mem": ["Memory"], "ist": ["IST"], "pt": ["Product Test", "All Other"], "rob": ["Robotics"], "st": ["System Test"], "wt": ["Wireless Test"]}


SUBSTR = {"SoC Test Systems": ["soc"], "Memory Test Systems": ["memory"], "Other Systems": ["other systems", "mechatronics"], "Services & Others": ["services"],
          "Semiconductor Test": ["semiconductor test"], "SOC": ["soc"], "Memory": ["memory"], "IST": ["ist"], "Product Test": ["product test", "all other"], "Robotics": ["robotics"]}
def pick(m, names):
    for n in names:
        if n in m: return m[n]
    for n in names:
        for sub in SUBSTR.get(n, []):
            for k, v in m.items():
                kl = k.lower()
                if sub in kl and not (sub == "soc" and "test system business" in kl) and not (sub == "memory" and "non" in kl): return v
    return None


def adv_cy_segments():
    """Calendar-year Advantest segments (¥mm). CY = Jan-Mar (FQ4 of prior FY) + Apr-Dec (FQ1-3) from quarterly PG_REVENUE when the
    four quarters exist; else prorate 0.25×FY(t-1) + 0.75×FY(t) from annual PG_REVENUE (BBG FY label = end year)."""
    out = {}
    for y in YEARS:
        if y in HOUSE_YEARS: continue
        qs = [d for d in SEG_Q["6857"] if d.year == y]
        if len(qs) == 4:
            out[y] = {k: sum(pick(SEG_Q["6857"][d], nm) or 0 for d in qs) for k, nm in ADV_SEGNAMES.items()}; out[y]["_basis"] = "trimestres"
        else:
            a0, a1 = SEG_A["6857"].get(y), SEG_A["6857"].get(y + 1)     # FY ending Mar-y (Apr y-1..Mar y) and FY ending Mar-(y+1)
            if a0 and a1:
                out[y] = {k: 0.25 * (pick(a0, nm) or 0) + 0.75 * (pick(a1, nm) or 0) for k, nm in ADV_SEGNAMES.items()}; out[y]["_basis"] = "FY pró-rateado 25/75"
    return out


def ter_cy_segments():
    out = {}
    for y in YEARS:
        if y in HOUSE_YEARS: continue
        a = SEG_A["TER"].get(y)
        if not a: continue
        d = {k: pick(a, nm) for k, nm in TER_SEGNAMES.items()}
        if d["pt"] is None and (d["st"] or d["wt"]): d["pt"] = (d["st"] or 0) + (d["wt"] or 0); d["_pt_note"] = "System Test + Wireless Test (segmentação antiga, inclui storage)"
        if d["rob"] is None and y == 2019: d["rob"] = 296.761; LOG.append("TER CY2019: Robotics ausente no PG_REVENUE anual de 2019 — usado 296,8 (BBG PG_REVENUE, bloco 2023 período 5 = FY2019)")
        out[y] = d
    return out


ADV_SEG_CY = adv_cy_segments(); TER_SEG_CY = ter_cy_segments()
for t in TK:
    for d, m in sorted(SEG_Q[t].items()):
        if pick(m, ADV_SEGNAMES["soc"] if t == "6857" else ["SOC"]) is None: LOG.append(f"{t} {d}: sem linha SoC nos segmentos — chaves: {list(m)[:8]}")
# sanity: Advantest quarterly SoC summed over FY-Mar vs annual PG_REVENUE
for fy_end in (2025, 2026):
    qs = [d for d in SEG_Q["6857"] if dt.date(fy_end - 1, 4, 1) <= d <= dt.date(fy_end, 3, 31)]
    if len(qs) == 4:
        s_ = sum(pick(SEG_Q["6857"][d], ADV_SEGNAMES["soc"]) or 0 for d in qs); a_ = pick(SEG_A["6857"].get(fy_end, {}), ADV_SEGNAMES["soc"])
        LOG.append(f"6857 FY ending Mar-{fy_end}: SoC soma dos 4 trimestres {s_:,.0f} vs anual PG_REVENUE {a_ if a_ is None else f'{a_:,.0f}'}")
for y in (2024, 2025):
    qs = [d for d in SEG_Q["TER"] if d.year == y]
    if len(qs) == 4:
        s_ = sum(pick(SEG_Q["TER"][d], ["Semiconductor Test"]) or 0 for d in qs); a_ = pick(SEG_A["TER"].get(y, {}), ["Semiconductor Test"])
        LOG.append(f"TER CY{y}: Semi Test soma dos 4 trimestres {s_:,.1f} vs anual PG_REVENUE {a_}")

# ------------------------------------------------------------------ official models (cached values)
def model_vals():
    a = openpyxl.load_workbook(ADV_X, data_only=True)["Capa DCF - Base"]; t = openpyxl.load_workbook(TER_X, data_only=True)["Capa DCF - Base"]
    A = LAY["adv"]; T = LAY["ter"]; aw = int(A["wiki"]); tw = int(T["wiki"]); apl = {k: int(v) for k, v in A["pl"].items()}; tpl = {k: int(v) for k, v in T["pl"].items()}
    col = {2023: "D", 2024: "E", 2025: "F", 2026: "G", 2027: "H", 2028: "I"}
    out = {"adv": {}, "ter": {}, "pool": {}}
    for y, c in col.items():
        g = lambda ws, r: fnum(ws[f"{c}{r}"].value)
        out["pool"][y] = dict(wfe=g(a, 8), ratio=g(a, 10), tam=g(a, 11), tam_soc=g(a, 16), tam_mem=g(a, 17))
        out["adv"][y] = dict(fx=g(a, 21), sh_soc=g(a, 22), sh_mem=g(a, 23), soc_us=g(a, 24), mem_us=g(a, 25), soc=g(a, 27), mem=g(a, 28), oth=g(a, 29), so=g(a, 31), rev=g(a, 32),
                             gm=g(a, apl["gm"]), gp=g(a, apl["gp"]), ebit=g(a, apl["ebit"]), fin=g(a, aw + 4), ni=g(a, aw + 5), sh=g(a, aw + 6), eps=g(a, aw + 7), eps_ex=g(a, aw + 8), fcfe=g(a, aw + 9))
        out["ter"][y] = dict(share=g(t, 18), semi=g(t, 19), pt=g(t, 20), rob=g(t, 21), rev=g(t, 22), gm=g(t, tpl["gm"]), gp=g(t, tpl["gp"]), ebit=g(t, tpl["ebit"]), ni=g(t, tw + 5), sh=g(t, tw + 6), eps=g(t, tw + 7), fcfe=g(t, tw + 9))
    return out


M = model_vals()
TER_SUB = {2026: (3205, 885, 230), 2027: (3900, 1150, 245), 2028: (4950, 1400, 290)}   # initiation SOC / Memory / IST mix

# ------------------------------------------------------------------ helpers
def put(ws, r, c, v, font=BLK, nf=None, fill=None, al=None, wrap=False):
    cell = ws.cell(row=r, column=c, value=v); cell.font = font
    if nf: cell.number_format = nf
    if fill: cell.fill = fill
    if al or wrap: cell.alignment = Alignment(horizontal=al, wrap_text=wrap, vertical="top" if wrap else None)
    return cell


def header(ws, r, labels, first="", first_w=None):
    put(ws, r, 1, first, BLD, fill=FILL_H)
    for i, t in enumerate(labels): put(ws, r, 2 + i, t, BLD, fill=FILL_H, al="center")


def band(ws, r, text, ncols):
    put(ws, r, 1, text, WHT, fill=FILL_S)
    for c in range(2, ncols + 2): ws.cell(row=r, column=c).fill = FILL_S


def vals_row(ws, r, label, vals, nf=NF_N, est_from=None, fonts=None, indent=False, note=None, ncols=None):
    put(ws, r, 1, ("  " if indent else "") + label, BLK)
    for i, v in enumerate(vals):
        if v is None: put(ws, r, 2 + i, "-", GRY, al="right"); continue
        f = fonts[i] if fonts else (BLU if (est_from is not None and i >= est_from) else BLK)
        put(ws, r, 2 + i, v, f, nf=nf, al="right")
    if note: put(ws, r, 2 + (ncols or len(vals)) + 1, note, GRY)


def ratio(a, b): return None if (a is None or not b) else a / b
def growth(cur, prev): return None if (cur is None or prev in (None, 0)) else cur / prev - 1
def usd(t, y, v): return None if v is None else (v / FX_CY[y] if t == "6857" else v)


# ------------------------------------------------------------------ annual series per company (CY2019-2028)
def annual(t):
    A = {}
    house = M["adv"] if t == "6857" else M["ter"]
    for y in YEARS:
        ok = bc(t, y, "BEST_SALES") is not None
        d = dict(actual=is_actual(t, y))
        if y in HOUSE_YEARS:
            h = house[y]
            d.update(rev=h["rev"], gm_adj=h["gm"], oi_adj=h["ebit"], ni_adj=h["ni"], eps_adj=h["eps"], shares=h["sh"], fcf=h["fcfe"], gm_gaap=None, oi_gaap=None, ni_gaap=None, eps_gaap=None,
                     nest=bc(t, y, "BEST_SALES_NUMEST"), cons_rev=bc(t, y, "BEST_SALES"), cons_ebit=bc(t, y, "BEST_OPP") or bc(t, y, "BEST_EBIT"), cons_eps=bc(t, y, "BEST_EPS"), cons_ni=bc(t, y, "BEST_NET_INCOME"), src="house")
            if t == "6857": d.update(gm_gaap=h["gm"], oi_gaap=h["ebit"], ni_gaap=h["ni"], eps_gaap=h["eps"])
        else:
            rev = bc(t, y, "BEST_SALES") if ok else PR[t]["SALES_REV_TURN"].get(y)
            gp = PR[t]["GROSS_PROFIT"].get(y); oi = PR[t]["IS_OPER_INC"].get(y); ni = PR[t]["NET_INCOME"].get(y); nia = PR[t]["IS_ADJUSTED_NET_INCOME"].get(y)
            sh = PR[t]["SHARES"].get(y)
            d.update(rev=rev, gm_gaap=ratio(gp, rev), gm_adj=(bc(t, y, "BEST_GROSS_MARGIN") / 100 if bc(t, y, "BEST_GROSS_MARGIN") else None),
                     oi_gaap=oi, oi_adj=bc(t, y, "BEST_OPP") or bc(t, y, "BEST_EBIT"), ni_gaap=ni, ni_adj=bc(t, y, "BEST_NET_INCOME") or nia,
                     eps_gaap=bc(t, y, "BEST_EPS_GAAP") or (ratio(ni, sh) if sh else None), eps_adj=bc(t, y, "BEST_EPS"), shares=sh,
                     fcf=PR[t]["CF_FREE_CASH_FLOW"].get(y) or bc(t, y, "BEST_ESTIMATE_FCF"), nest=bc(t, y, "BEST_SALES_NUMEST"), cons_rev=None, cons_ebit=None, cons_eps=None, cons_ni=None, src="bbg")
            if t == "6857":   # IFRS: non-GAAP == reported; BBG BEst 'actuals' can differ slightly → keep reported where available
                if oi is not None: d["oi_adj"] = oi
                if ni is not None: d["ni_adj"] = ni
                if gp is not None and rev: d["gm_adj"] = gp / rev
                eq = PR[t]["IS_DILUTED_EPS"].get(y)
                if eq is not None:
                    if d["eps_adj"] is not None and abs(eq / d["eps_adj"] - 1) > 0.02: LOG.append(f"6857 CY{y}: EPS BEst-actual BBG {d['eps_adj']:.1f} ≠ soma dos trimestres reportados {eq:.1f} — usado o reportado (BBG não calendariza EPS de FYE março)")
                    d["eps_adj"] = eq; d["eps_gaap"] = eq
                elif d["eps_adj"] is None and ni and sh: d["eps_adj"] = ni / sh
        A[y] = d
    return A


ANN = {t: annual(t) for t in TK}
for t in TK:
    for y in YEARS:
        if ANN[t][y]["rev"] is None: LOG.append(f"{t} CY{y}: sem receita (BC e pró-rateio indisponíveis)")

wb = openpyxl.Workbook(); wb.remove(wb.active)
NC = len(YEARS)
# =====================================================================================================
# Sheet 1 — CY Summary
# =====================================================================================================
ws = wb.create_sheet("CY Summary")
ws.column_dimensions["A"].width = 46
for i in range(NC): ws.column_dimensions[L(2 + i)].width = 11.5
ws.column_dimensions[L(NC + 3)].width = 70
put(ws, 1, 1, "ATE — Advantest + Teradyne | resumo em ano-calendário (US$ milhões salvo indicação)", TIT)
put(ws, 2, 1, f"Bloomberg BEst calendarizado ('<yr>BC', pulled {ASOF}) para CY2019-CY2025 (anos completos = actuals); CY2026-CY2028 = modelos oficiais Capstone (Template DCF ADVANTEST / TER, 2026-09-18). Advantest convertida ao FX médio do CY (BBG USDJPY; 157 / 150 / 150 nas projeções).", GRY)
put(ws, 3, 1, "Preto = actual  |  Azul = estimativa (casa)  |  Cinza = consenso BBG (memo). Advantest reporta FY-Mar em IFRS; Teradyne non-GAAP (SBC não excluído).", GRY)
r = 5
ylab = [f"CY{y}{'A' if y <= 2025 else 'E'}" for y in YEARS]


def matrix(title, rows, nf):
    global r
    put(ws, r, 1, title, BLD); r += 1; header(ws, r, ylab, "Empresa"); r += 1
    for label, vals, est_from, font_override in rows:
        vals_row(ws, r, label, vals, nf=nf, est_from=est_from, fonts=([font_override] * NC if font_override else None)); r += 1
    r += 1


def A(t, k): return [ANN[t][y].get(k) for y in YEARS]
adv_rev_us = [usd("6857", y, ANN["6857"][y]["rev"]) for y in YEARS]; ter_rev = A("TER", "rev")
comb_rev = [None if (a is None or b is None) else a + b for a, b in zip(adv_rev_us, ter_rev)]
matrix("Receita (US$ mi)", [("Advantest (US$, ao FX médio do CY)", adv_rev_us, 7, None), ("Teradyne", ter_rev, 7, None), ("Combinado", comb_rev, 7, None), ("Advantest — ¥ bilhões (memo)", [None if v is None else v / 1000 for v in A("6857", "rev")], 7, None)], NF_N)
def gser(v): return [None] + [growth(v[i], v[i - 1]) for i in range(1, NC)]
matrix("Crescimento da receita (US$)", [("Advantest (US$)", gser(adv_rev_us), 7, None), ("Advantest (¥, moeda local)", gser(A("6857", "rev")), 7, None), ("Teradyne", gser(ter_rev), 7, None), ("Combinado", gser(comb_rev), 7, None)], NF_P)
matrix("Margem bruta (Advantest IFRS; Teradyne non-GAAP)", [("Advantest", A("6857", "gm_adj"), 7, None), ("Teradyne", A("TER", "gm_adj"), 7, None)], NF_P)
adv_oi_us = [usd("6857", y, ANN["6857"][y]["oi_adj"]) for y in YEARS]; ter_oi = A("TER", "oi_adj")
matrix("Resultado operacional (US$ mi; Advantest IFRS, Teradyne non-GAAP)", [("Advantest (US$)", adv_oi_us, 7, None), ("Teradyne", ter_oi, 7, None), ("Combinado", [None if (a is None or b is None) else a + b for a, b in zip(adv_oi_us, ter_oi)], 7, None)], NF_N)
matrix("Margem operacional", [("Advantest", [ratio(o, v) for o, v in zip(A("6857", "oi_adj"), A("6857", "rev"))], 7, None), ("Teradyne", [ratio(o, v) for o, v in zip(ter_oi, ter_rev)], 7, None),
                               ("Combinado", [ratio(a, b) for a, b in zip([None if (x is None or y is None) else x + y for x, y in zip(adv_oi_us, ter_oi)], comb_rev)], 7, None)], NF_P)
adv_ni_us = [usd("6857", y, ANN["6857"][y]["ni_adj"]) for y in YEARS]; ter_ni = A("TER", "ni_adj")
matrix("Lucro líquido (US$ mi; Advantest IFRS, Teradyne non-GAAP)", [("Advantest (US$)", adv_ni_us, 7, None), ("Teradyne", ter_ni, 7, None), ("Combinado", [None if (a is None or b is None) else a + b for a, b in zip(adv_ni_us, ter_ni)], 7, None)], NF_N)
matrix("EPS diluído (moeda local; Advantest ¥ IFRS, Teradyne US$ non-GAAP)", [("Advantest (¥)", A("6857", "eps_adj"), 7, None), ("Teradyne (US$)", A("TER", "eps_adj"), 7, None)], NF_N2)
matrix("Ações diluídas (milhões)", [("Advantest", A("6857", "shares"), 7, None), ("Teradyne", A("TER", "shares"), 7, None)], NF_N1)
adv_fcf_us = [usd("6857", y, ANN["6857"][y]["fcf"]) for y in YEARS]
matrix("Free cash flow (US$ mi; CFO − capex; CY26-28 = FCF equity dos modelos)", [("Advantest (US$)", adv_fcf_us, 7, None), ("Teradyne", A("TER", "fcf"), 7, None)], NF_N)
matrix("Mix Advantest / (Advantest + Teradyne)", [("Receita", [ratio(a, c) for a, c in zip(adv_rev_us, comb_rev)], 7, None), ("Resultado operacional", [ratio(a, c) for a, c in zip(adv_oi_us, [None if (x is None or y is None) else x + y for x, y in zip(adv_oi_us, ter_oi)])], 7, None)], NF_P)
# consensus memo CY26-28
put(ws, r, 1, "Consenso BBG calendarizado ('<yr>BC') — memo para CY2026-CY2028 (casa ÷ consenso − 1 na linha seguinte)", BLD); r += 1; header(ws, r, ylab, "Empresa"); r += 1
for t, lab in (("6857", "Advantest receita (¥ mi) — consenso"), ("TER", "Teradyne receita (US$ mi) — consenso")):
    cons = [ANN[t][y]["cons_rev"] if y in HOUSE_YEARS else None for y in YEARS]
    vals_row(ws, r, lab, cons, NF_N, fonts=[GRY] * NC); r += 1
    vals_row(ws, r, "  casa ÷ consenso − 1", [ratio(ANN[t][y]["rev"], ANN[t][y]["cons_rev"]) - 1 if (y in HOUSE_YEARS and ANN[t][y]["cons_rev"]) else None for y in YEARS], NF_P, fonts=[BLU] * NC); r += 1
for t, lab in (("6857", "Advantest EPS (¥) — consenso BBG FY-Mar (NÃO calendarizado: 1CY = 1FY)"), ("TER", "Teradyne EPS (US$) — consenso")):
    cons = [ANN[t][y]["cons_eps"] if y in HOUSE_YEARS else None for y in YEARS]
    vals_row(ws, r, lab, cons, NF_N2, fonts=[GRY] * NC); r += 1
put(ws, r + 1, 1, "Nota: para a Advantest o EPS de consenso BBG em '2026BC' é o EPS do FY-Mar-2027 (¥927), não um EPS calendarizado — comparar EPS em FY ou por trimestre; receita e EBIT BC são calendarizados.", GRY)
ws.freeze_panes = "B6"

# =====================================================================================================
# Sheet 2 — CY Detail by company (Fernanda rows + revenue build-up)
# =====================================================================================================
wd = wb.create_sheet("CY Detail by company")
wd.column_dimensions["A"].width = 52
for i in range(NC): wd.column_dimensions[L(2 + i)].width = 11.5
wd.column_dimensions[L(NC + 3)].width = 80
put(wd, 1, 1, "Detalhe por empresa em ano-calendário — P&L (GAAP/IFRS e non-GAAP) + revenue build-up por segmento e drivers", TIT)
put(wd, 2, 1, f"Bloomberg (pulled {ASOF}): linhas non-GAAP = BEst calendarizado '<yr>BC' (anos completos = actuals); linhas GAAP/IFRS = trimestres reportados pró-rateados por dias no ano-calendário; segmentos = PG_REVENUE (produto). CY2026-28 = modelos oficiais Capstone.", GRY)
r = 4
ydet = [f"CY{y}{'A' if y <= 2025 else 'E'}" for y in YEARS]


def block_pl(t):
    global r
    c = CO[t]; A_ = ANN[t]
    band(wd, r, f"{c['name']}   |   {c['unit']}, EPS em {c['eps_u']}   |   FYE {'mar' if t == '6857' else 'dez'}", NC + 1); r += 1
    header(wd, r, ydet, c["unit"]); r += 1
    rows = [("Receita", "rev", NF_N, None), ("  YoY", None, NF_P, "g")]
    vals_row(wd, r, "Receita", [A_[y]["rev"] for y in YEARS], NF_N, est_from=7); r += 1
    vals_row(wd, r, "YoY", gser([A_[y]["rev"] for y in YEARS]), NF_P, est_from=7, indent=True); r += 1
    if t == "TER":
        vals_row(wd, r, "Margem bruta — GAAP", [A_[y]["gm_gaap"] for y in YEARS], NF_P, est_from=7); r += 1
        vals_row(wd, r, "Margem bruta — non-GAAP", [A_[y]["gm_adj"] for y in YEARS], NF_P, est_from=7); r += 1
        vals_row(wd, r, "Resultado operacional (EBIT) — GAAP", [A_[y]["oi_gaap"] for y in YEARS], NF_N, est_from=7); r += 1
        vals_row(wd, r, "Margem EBIT — GAAP", [ratio(A_[y]["oi_gaap"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
        vals_row(wd, r, "Resultado operacional (EBIT) — non-GAAP", [A_[y]["oi_adj"] for y in YEARS], NF_N, est_from=7); r += 1
        vals_row(wd, r, "Margem EBIT — non-GAAP", [ratio(A_[y]["oi_adj"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
        vals_row(wd, r, "Lucro líquido — GAAP", [A_[y]["ni_gaap"] for y in YEARS], NF_N, est_from=7); r += 1
        vals_row(wd, r, "Lucro líquido — non-GAAP", [A_[y]["ni_adj"] for y in YEARS], NF_N, est_from=7); r += 1
        vals_row(wd, r, "Margem líquida — non-GAAP", [ratio(A_[y]["ni_adj"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
        vals_row(wd, r, "EPS diluído — GAAP", [A_[y]["eps_gaap"] for y in YEARS], NF_N2, est_from=7); r += 1
        vals_row(wd, r, "EPS diluído — non-GAAP", [A_[y]["eps_adj"] for y in YEARS], NF_N2, est_from=7); r += 1
    else:
        vals_row(wd, r, "Margem bruta — IFRS", [A_[y]["gm_adj"] for y in YEARS], NF_P, est_from=7); r += 1
        vals_row(wd, r, "Resultado operacional — IFRS", [A_[y]["oi_adj"] for y in YEARS], NF_N, est_from=7); r += 1
        vals_row(wd, r, "Margem operacional", [ratio(A_[y]["oi_adj"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
        vals_row(wd, r, "Lucro líquido — IFRS", [A_[y]["ni_adj"] for y in YEARS], NF_N, est_from=7, note="CY26E inclui ¥66 bi de resultado financeiro não recorrente (ganhos de valuation de investimentos estratégicos); EPS ex = ¥" + f"{M['adv'][2026]['eps_ex']:,.0f}.", ncols=NC); r += 1
        vals_row(wd, r, "Margem líquida", [ratio(A_[y]["ni_adj"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
        vals_row(wd, r, "EPS básico/diluído (¥)", [A_[y]["eps_adj"] for y in YEARS], NF_N2, est_from=7); r += 1
    vals_row(wd, r, "Ações diluídas (milhões, média ponderada)", [A_[y]["shares"] for y in YEARS], NF_N1, est_from=7); r += 1
    vals_row(wd, r, "Free cash flow (CFO − capex; CY26+ FCF equity do modelo)", [A_[y]["fcf"] for y in YEARS], NF_N, est_from=7); r += 1
    vals_row(wd, r, "Margem FCF", [ratio(A_[y]["fcf"], A_[y]["rev"]) for y in YEARS], NF_P, est_from=7, indent=True); r += 1
    vals_row(wd, r, "Nº de estimativas de receita (BBG)", [A_[y]["nest"] for y in YEARS], NF_N, fonts=[GRY] * NC); r += 1
    vals_row(wd, r, "Consenso BBG receita ('<yr>BC') — memo", [A_[y]["cons_rev"] if y in HOUSE_YEARS else None for y in YEARS], NF_N, fonts=[GRY] * NC); r += 1
    vals_row(wd, r, "Consenso BBG EBIT ('<yr>BC') — memo", [A_[y]["cons_ebit"] if y in HOUSE_YEARS else None for y in YEARS], NF_N, fonts=[GRY] * NC); r += 1


def block_buildup_adv():
    global r
    put(wd, r, 1, "Revenue build-up — Advantest (¥ milhões; CY = jan-mar do FQ4 anterior + abr-dez)", BLD, fill=FILL_B)
    for cc in range(2, NC + 2): wd.cell(row=r, column=cc).fill = FILL_B
    r += 1
    S = ADV_SEG_CY; H = M["adv"]
    def ser(k):
        out = []
        for y in YEARS:
            if y in HOUSE_YEARS: out.append(H[y][{"soc": "soc", "mem": "mem", "oth": "oth", "so": "so"}[k]])
            else: out.append(S.get(y, {}).get(k))
        return out
    soc, mem, oth, so = ser("soc"), ser("mem"), ser("oth"), ser("so")
    vals_row(wd, r, "SoC test systems", soc, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Memory test systems", mem, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Outros sistemas (handlers, probers, interfaces; 'Mechatronics' até FY23)", oth, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Services & Others", so, NF_N, est_from=7); r += 1
    tot = [None if any(v is None for v in (a, b, c_, d)) else a + b + c_ + d for a, b, c_, d in zip(soc, mem, oth, so)]
    vals_row(wd, r, "Soma dos segmentos", tot, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Receita reportada / modelo (linha 'Receita' acima)", [ANN["6857"][y]["rev"] for y in YEARS], NF_N, est_from=7, indent=True); r += 1
    vals_row(wd, r, "Diferença (segmentos − receita)", [None if (a is None or b is None) else a - b for a, b in zip(tot, [ANN["6857"][y]["rev"] for y in YEARS])], NF_N, fonts=[GRY] * NC, indent=True,
             note="Histórico: segmentos BBG PG_REVENUE trimestrais (2024-25) ou FY pró-rateado 25/75 (≤2023) — diferença = calendarização/arredondamento. Basis por ano na linha abaixo.", ncols=NC); r += 1
    vals_row(wd, r, "Base do build-up histórico", [S.get(y, {}).get("_basis") if y not in HOUSE_YEARS else "modelo" for y in YEARS], None, fonts=[GRY] * NC, indent=True); r += 1
    vals_row(wd, r, "  % SoC", [ratio(a, b) for a, b in zip(soc, tot)], NF_P, est_from=7, indent=True); r += 1
    vals_row(wd, r, "  % Memória", [ratio(a, b) for a, b in zip(mem, tot)], NF_P, est_from=7, indent=True); r += 1
    vals_row(wd, r, "  % Outros sistemas + Services", [ratio(None if (a is None or b is None) else a + b, c_) for a, b, c_ in zip(oth, so, tot)], NF_P, est_from=7, indent=True); r += 1
    put(wd, r, 1, "Drivers do modelo (CY2023-CY2028; Template DCF ADVANTEST)", BLD); r += 1
    P = M["pool"]
    def mser(src, k, yrs=range(2023, 2029)): return [(src[y][k] if y in src else None) for y in YEARS]
    vals_row(wd, r, "WFE global (US$ bi)", mser(P, "wfe"), NF_N1, est_from=7); r += 1
    vals_row(wd, r, "Intensidade de teste (TAM ATE / WFE)", mser(P, "ratio"), NF_P, est_from=7); r += 1
    vals_row(wd, r, "TAM ATE total (US$ bi) — base Advantest ex burn-in", mser(P, "tam"), NF_N2, est_from=7); r += 1
    vals_row(wd, r, "TAM SoC (US$ bi)", mser(P, "tam_soc"), NF_N2, est_from=7); r += 1
    vals_row(wd, r, "Share Advantest em SoC", mser(H, "sh_soc"), NF_P, est_from=7, note="CY23-25 implícito (receita SoC ÷ TAM SoC); mgmt: 66% em CY25, 'path to >70%'.", ncols=NC); r += 1
    vals_row(wd, r, "Receita SoC (US$ mi) = TAM × share", mser(H, "soc_us"), NF_N, est_from=7); r += 1
    vals_row(wd, r, "TAM memória (US$ bi)", mser(P, "tam_mem"), NF_N2, est_from=7); r += 1
    vals_row(wd, r, "Share Advantest em memória", mser(H, "sh_mem"), NF_P, est_from=7); r += 1
    vals_row(wd, r, "Receita memória (US$ mi) = TAM × share", mser(H, "mem_us"), NF_N, est_from=7); r += 1
    vals_row(wd, r, "FX ¥/US$ (média do ano)", [FX_CY[y] for y in YEARS], NF_N1, est_from=7); r += 1
    vals_row(wd, r, "Outros sistemas / (SoC + memória)", [ratio(H[y]["oth"], H[y]["soc"] + H[y]["mem"]) if y in H else None for y in YEARS], NF_P, est_from=7); r += 1
    vals_row(wd, r, "Services & Others / Test Systems", [ratio(H[y]["so"], H[y]["soc"] + H[y]["mem"] + H[y]["oth"]) if y in H else None for y in YEARS], NF_P, est_from=7); r += 1


def block_buildup_ter():
    global r
    put(wd, r, 1, "Revenue build-up — Teradyne (US$ milhões; segmentação de 2025: Semi Test inclui IST; Product Test = System + Wireless ex-IST)", BLD, fill=FILL_B)
    for cc in range(2, NC + 2): wd.cell(row=r, column=cc).fill = FILL_B
    r += 1
    S = TER_SEG_CY; H = M["ter"]
    def hist(k): return [S.get(y, {}).get(k) if y not in HOUSE_YEARS else None for y in YEARS]
    semi = [H[y]["semi"] if y in HOUSE_YEARS else S.get(y, {}).get("semi") for y in YEARS]
    soc = [H[y]["semi"] * TER_SUB[y][0] / sum(TER_SUB[y]) if y in HOUSE_YEARS else S.get(y, {}).get("soc") for y in YEARS]
    mem = [H[y]["semi"] * TER_SUB[y][1] / sum(TER_SUB[y]) if y in HOUSE_YEARS else S.get(y, {}).get("mem") for y in YEARS]
    ist = [H[y]["semi"] * TER_SUB[y][2] / sum(TER_SUB[y]) if y in HOUSE_YEARS else S.get(y, {}).get("ist") for y in YEARS]
    pt = [H[y]["pt"] if y in HOUSE_YEARS else S.get(y, {}).get("pt") for y in YEARS]
    rob = [H[y]["rob"] if y in HOUSE_YEARS else S.get(y, {}).get("rob") for y in YEARS]
    vals_row(wd, r, "Semiconductor Test", semi, NF_N, est_from=7); r += 1
    vals_row(wd, r, "SOC", soc, NF_N, est_from=7, indent=True, note="CY26-28: Semi Test do modelo × mix da iniciação (SOC 74% / 74% / 75%; memória 20% / 22% / 21%; IST 5% / 5% / 4%).", ncols=NC); r += 1
    vals_row(wd, r, "Memory", mem, NF_N, est_from=7, indent=True); r += 1
    vals_row(wd, r, "IST (storage test; dentro de Semi Test desde 2023)", ist, NF_N, est_from=7, indent=True); r += 1
    vals_row(wd, r, "Product Test (2019-22: System Test + Wireless Test, incl. storage)", pt, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Robotics", rob, NF_N, est_from=7); r += 1
    tot = [None if any(v is None for v in (a, b, c_)) else a + b + c_ for a, b, c_ in zip(semi, pt, rob)]
    vals_row(wd, r, "Soma dos segmentos", tot, NF_N, est_from=7); r += 1
    vals_row(wd, r, "Receita reportada / modelo", [ANN["TER"][y]["rev"] for y in YEARS], NF_N, est_from=7, indent=True); r += 1
    vals_row(wd, r, "Diferença (segmentos − receita)", [None if (a is None or b is None) else a - b for a, b in zip(tot, [ANN["TER"][y]["rev"] for y in YEARS])], NF_N, fonts=[GRY] * NC, indent=True); r += 1
    vals_row(wd, r, "  % Semi Test", [ratio(a, b) for a, b in zip(semi, tot)], NF_P, est_from=7, indent=True); r += 1
    vals_row(wd, r, "  % SOC / Semi Test", [ratio(a, b) for a, b in zip(soc, semi)], NF_P, est_from=7, indent=True); r += 1
    vals_row(wd, r, "  % Memory / Semi Test", [ratio(a, b) for a, b in zip(mem, semi)], NF_P, est_from=7, indent=True); r += 1
    put(wd, r, 1, "Drivers do modelo (CY2023-CY2028; Template DCF TER)", BLD); r += 1
    P = M["pool"]
    def mser(src, k): return [(src[y][k] if y in src else None) for y in YEARS]
    vals_row(wd, r, "WFE global (US$ bi)", mser(P, "wfe"), NF_N1, est_from=7); r += 1
    vals_row(wd, r, "Intensidade de teste (TAM ATE / WFE)", mser(P, "ratio"), NF_P, est_from=7); r += 1
    vals_row(wd, r, "TAM ATE total (US$ bi) — base Advantest ex burn-in", mser(P, "tam"), NF_N2, est_from=7); r += 1
    vals_row(wd, r, "Share Teradyne no TAM (Semi Test incl. IST ÷ TAM)", mser(H, "share"), NF_P, est_from=7, note="Calibrado à iniciação (2026-09-16): +90bp / +100bp por ano; na base WFE da iniciação = 34,2% / 35,4% / 36,9%.", ncols=NC); r += 1
    vals_row(wd, r, "Semi Test (US$ mi) = TAM × share", mser(H, "semi"), NF_N, est_from=7); r += 1
    vals_row(wd, r, "Product Test — crescimento", [growth(H[y]["pt"], H[y - 1]["pt"]) if (y in H and (y - 1) in H) else None for y in YEARS], NF_P, est_from=7); r += 1
    vals_row(wd, r, "Robotics — crescimento", [growth(H[y]["rob"], H[y - 1]["rob"]) if (y in H and (y - 1) in H) else None for y in YEARS], NF_P, est_from=7); r += 1


block_pl("6857"); r += 1; block_buildup_adv(); r += 2
block_pl("TER"); r += 1; block_buildup_ter(); r += 2
wd.freeze_panes = "B4"

# =====================================================================================================
# Sheet 3 — Quarterly CY2025-CY2026
# =====================================================================================================
wq = wb.create_sheet("Quarterly CY2025-CY2026")
wq.column_dimensions["A"].width = 52
for i in range(8): wq.column_dimensions[L(2 + i)].width = 13.5
wq.column_dimensions["K"].width = 70
put(wq, 1, 1, "Visão trimestral — trimestre fiscal alocado ao trimestre-calendário mais próximo (1Q25 … 4Q26)", TIT)
put(wq, 2, 1, f"Bloomberg, pulled {ASOF}. A = reportado (FUND_PER=Qn); E = consenso BEst (1FQ/2FQ). Advantest: FQ1 FY26 (convenção da empresa) = abr-jun 2026 = 2Q26. Segmentos trimestrais = PG_REVENUE por trimestre fiscal.", GRY)
r = 4
QL = [f"{q}Q{str(y)[2:]}" for y, q in CQ]


def qblock(t):
    global r
    c = CO[t]
    band(wq, r, f"{c['name']}   |   {c['unit']}, EPS em {c['eps_u']}", 9); r += 1
    header(wq, r, QL, c["unit"]); r += 1
    QV = {}
    for rr in QROWS[t]:
        yq = snap(rr["_end"])
        if yq in CQ:
            QV[yq] = dict(kind="A", label=fq_label(t, rr["_end"]), rev=fnum(rr.get("SALES_REV_TURN")), gp=fnum(rr.get("GROSS_PROFIT")), oi=fnum(rr.get("IS_OPER_INC")), ni=fnum(rr.get("NET_INCOME")),
                          nia=fnum(rr.get("IS_ADJUSTED_NET_INCOME")), eps=fnum(rr.get("IS_DILUTED_EPS")), epsa=fnum(rr.get("IS_COMP_EPS_ADJUSTED")), sh=fnum(rr.get("IS_SH_FOR_DILUTED_EPS")),
                          fcf=fnum(rr.get("CF_FREE_CASH_FLOW")), gm_c=None, oi_c=None, end=rr["_end"], seg=SEG_Q[t].get(rr["_end"]))
    for k in range(1, 9):
        rr = qc[str(k)].get(t, {}); ped = rr.get("BEST_PERIOD_END_DATE")
        if not ped or rr.get("BEST_SALES") is None: continue
        d = dt.date.fromisoformat(ped[:10]); yq = snap(d)
        if yq in CQ and yq not in QV:
            ni, e = fnum(rr.get("BEST_NET_INCOME")), fnum(rr.get("BEST_EPS"))
            QV[yq] = dict(kind="E", label=fq_label(t, d), rev=fnum(rr.get("BEST_SALES")), gp=None, oi=None, ni=None, nia=ni, eps=fnum(rr.get("BEST_EPS_GAAP")), epsa=e, sh=(ni / e if (ni and e) else None),
                          fcf=fnum(rr.get("BEST_ESTIMATE_FCF")), gm_c=(fnum(rr.get("BEST_GROSS_MARGIN")) / 100 if rr.get("BEST_GROSS_MARGIN") else None), oi_c=fnum(rr.get("BEST_OPP")) or fnum(rr.get("BEST_EBIT")), end=d, seg=None, nest=fnum(rr.get("BEST_SALES_NUMEST")))
    def g(k, key): v = QV.get(k); return None if v is None else v.get(key)
    def fonts_kind(): return [BLU if g(k, "kind") == "E" else BLK for k in CQ]
    vals_row(wq, r, "Trimestre fiscal (fim do período)", [g(k, "label") for k in CQ], None, fonts=[GRY] * 8); r += 1
    vals_row(wq, r, "Base", [{"A": "A - reportado", "E": "E - consenso"}.get(g(k, "kind")) for k in CQ], None, fonts=[GRY] * 8); r += 1
    rev = [g(k, "rev") for k in CQ]
    vals_row(wq, r, "Receita", rev, NF_N, fonts=fonts_kind()); r += 1
    # yoy vs same calendar quarter a year earlier (needs 2024 quarters)
    prev = {}
    for rr in QROWS[t]:
        yq = snap(rr["_end"]); prev[yq] = fnum(rr.get("SALES_REV_TURN"))
    vals_row(wq, r, "YoY (vs mesmo trimestre-calendário)", [growth(g(k, "rev"), prev.get((k[0] - 1, k[1]))) for k in CQ], NF_P, fonts=fonts_kind(), indent=True); r += 1
    if t == "TER":
        vals_row(wq, r, "Margem bruta — GAAP (reportado)", [ratio(g(k, "gp"), g(k, "rev")) for k in CQ], NF_P, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "Margem bruta — non-GAAP (consenso)", [g(k, "gm_c") for k in CQ], NF_P, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "EBIT — GAAP (reportado)", [g(k, "oi") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "EBIT — non-GAAP (consenso)", [g(k, "oi_c") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "Lucro líquido — GAAP (reportado)", [g(k, "ni") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "Lucro líquido — non-GAAP", [g(k, "nia") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "EPS diluído — GAAP", [g(k, "eps") for k in CQ], NF_N2, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "EPS diluído — non-GAAP", [g(k, "epsa") for k in CQ], NF_N2, fonts=fonts_kind()); r += 1
    else:
        vals_row(wq, r, "Margem bruta — IFRS (reportado) / consenso", [ratio(g(k, "gp"), g(k, "rev")) if g(k, "kind") == "A" else g(k, "gm_c") for k in CQ], NF_P, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "Resultado operacional — IFRS / consenso", [g(k, "oi") if g(k, "kind") == "A" else g(k, "oi_c") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "Margem operacional", [ratio(g(k, "oi") if g(k, "kind") == "A" else g(k, "oi_c"), g(k, "rev")) for k in CQ], NF_P, fonts=fonts_kind(), indent=True); r += 1
        vals_row(wq, r, "Lucro líquido — IFRS / consenso", [g(k, "ni") if g(k, "kind") == "A" else g(k, "nia") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
        vals_row(wq, r, "EPS (¥)", [g(k, "eps") if g(k, "kind") == "A" else g(k, "epsa") for k in CQ], NF_N2, fonts=fonts_kind()); r += 1
    vals_row(wq, r, "Ações diluídas (milhões)", [g(k, "sh") for k in CQ], NF_N1, fonts=fonts_kind()); r += 1
    vals_row(wq, r, "Free cash flow (CFO − capex)", [g(k, "fcf") for k in CQ], NF_N, fonts=fonts_kind()); r += 1
    vals_row(wq, r, "Nº de estimativas de receita", [g(k, "nest") for k in CQ], NF_N, fonts=[GRY] * 8); r += 1
    # segment build-up
    put(wq, r, 1, "Revenue build-up por segmento (reportado; PG_REVENUE trimestral)", BLD, fill=FILL_B)
    for cc in range(2, 10): wq.cell(row=r, column=cc).fill = FILL_B
    r += 1
    names = ADV_SEGNAMES if t == "6857" else {"semi": ["Semiconductor Test"], "soc": ["SOC"], "mem": ["Memory"], "ist": ["IST"], "pt": ["Product Test"], "rob": ["Robotics"]}
    labels = {"soc": "SoC test systems" if t == "6857" else "  SOC", "mem": "Memory test systems" if t == "6857" else "  Memory", "oth": "Outros sistemas", "so": "Services & Others", "semi": "Semiconductor Test", "ist": "  IST", "pt": "Product Test", "rob": "Robotics"}
    for key_, nm in names.items():
        vals_row(wq, r, labels[key_], [pick(g(k, "seg") or {}, nm) if g(k, "seg") else None for k in CQ], NF_N, fonts=[BLK] * 8); r += 1
    if t == "6857":
        vals_row(wq, r, "  % SoC / receita", [ratio(pick(g(k, "seg") or {}, ADV_SEGNAMES["soc"]) if g(k, "seg") else None, g(k, "rev")) for k in CQ], NF_P, fonts=[BLK] * 8); r += 1
    else:
        vals_row(wq, r, "  % SOC / Semi Test", [ratio(pick(g(k, "seg") or {}, ["SOC"]) if g(k, "seg") else None, pick(g(k, "seg") or {}, ["Semiconductor Test"]) if g(k, "seg") else None) for k in CQ], NF_P, fonts=[BLK] * 8); r += 1
    r += 1
    return QV


QVS = {t: qblock(t) for t in TK}
wq.freeze_panes = "B4"

# =====================================================================================================
# Sheets 4-6 — Mix e segmentos / Regiões / Clientes (from the first version, fixed)
# =====================================================================================================
exec(open(os.path.join(HERE, "ate_extra_sheets.py"), encoding="utf-8").read())

# =====================================================================================================
# Sheet 7 — Notes
# =====================================================================================================
wn = wb.create_sheet("Notes"); wn.column_dimensions["A"].width = 34; wn.column_dimensions["B"].width = 150
put(wn, 1, 1, "Notas de método, fontes e qualidade de dados", TIT); r = 3
NOTES = [
 ("Método ano-calendário", "Linhas non-GAAP anuais: Bloomberg BEst calendarizado (BEST_FPERIOD_OVERRIDE = '<year>BC'): cada trimestre fiscal é pró-rateado nos anos-calendário pelos dias que tem em cada um. Para a Advantest (FYE março) CY2025 = 1/4 do FQ4 (jan-mar 2025)... na prática BBG usa os trimestres reportados: CY2025 = jan-mar 25 + abr-jun 25 + jul-set 25 + out-dez 25 quando os quatro estão reportados. Anos completos voltam como actuals (zero estimativas). Teradyne: CY = FY."),
 ("Linhas GAAP/IFRS", "Bloomberg não tem consenso GAAP para lucro bruto, EBIT ou lucro líquido; as linhas GAAP/IFRS são construídas aqui pró-rateando por dias os trimestres reportados (GROSS_PROFIT, IS_OPER_INC, NET_INCOME) — só anos completos. Checagem: o mesmo procedimento aplicado à receita reproduz a receita calendarizada BBG dentro de " + f"{worst:.2%}" + "."),
 ("CY2026-CY2028", "NÃO são consenso: são os modelos oficiais Capstone (Template DCF ADVANTEST.xlsx e Template DCF TER.xlsx, 2026-09-18). O consenso BBG '<yr>BC' aparece em linhas 'memo' (cinza). TER: NEUTRAL, PT $400 (iniciação 2026-09-16); Advantest: sem rating."),
 ("Revenue build-up", "Segmentos = Bloomberg PG_REVENUE (hierarquia de produto). Advantest: SoC / Memory / Other systems / Services & Others — CY a partir dos trimestres fiscais quando os quatro existem (2024-25), senão FY-Mar pró-rateado 25/75 (≤2023; a estrutura de 2 segmentos começa em FY24: SLT e interfaces migraram de Serviços para 'Other systems', quebra de série). Teradyne: Semiconductor Test (SOC / Memory / IST) / Product Test / Robotics na segmentação de 2025; 2019-22 Product Test = System Test + Wireless Test (inclui storage, depois movido para IST dentro de Semi Test). CY26-28: TAM × share (drivers listados), sub-split SOC/Memory/IST pela mix da iniciação."),
 ("Pool de teste (TAM)", "Base da própria Advantest (SoC + memória, EX burn-in): CY24 $6,0 bi / CY25 $9,0 bi / CY26e $13,75 bi (deck 29-jul-2026, ponto médio); CY27-28 = WFE × intensidade (8,0% / 8,3%) nos dois modelos. Teradyne Semi Test ex-IST para comparar com o mesmo pool. Não misturar com a base Teradyne (7-9% do WFE, inclui burn-in) nem com 'teste ÷ receita de semis' (~1%, UBS)."),
 ("Advantest — bases", "IFRS, ¥; FY termina em março (FY2026 = abr-2026→mar-2027 na convenção da empresa; Bloomberg rotula pelo ano de término = FY2027). EPS de consenso BBG NÃO é calendarizado (1CY = 1FY). CY26E do modelo inclui ¥66 bi de resultado financeiro não recorrente. Conversão a US$ ao FX médio do CY (BBG USDJPY): 109,0 / 106,4 / 110,4 / 131,7 / 141,4 / 151,9 / 150,0 (2019-25); 157 / 150 / 150 nas projeções (premissa do modelo)."),
 ("Teradyne — bases", "Non-GAAP da companhia (exclui amortização de intangíveis, reestruturação e itens; SBC NÃO excluído) = base do consenso BEst. Ressegmentação em 2025 (IST para Semi Test). Clientes: 10-K FY23/FY24/FY25 ('Sales and Distribution' e 'Revenues by country')."),
 ("Regiões", "Teradyne: localização do site do cliente (10-K / 10-Q). Advantest: ship-to por região (slide 7 do deck 1Q FY26) — as séries do PDF foram atribuídas às regiões por magnitude (Taiwan = maior ship-to; China ≈19% no Q1 FY26 confirmam duas das sete); localização do cliente (tanshin: Japão / Américas / Europa / Ásia)."),
 ("Reprodução no Excel", 'BDP("6857 JP Equity","BEST_SALES","BEST_FPERIOD_OVERRIDE","2027BC"); trimestres reportados: BDP("TER US Equity","SALES_REV_TURN","FUND_PER","Q2","EQY_FUND_YEAR","2026"); consenso trimestral: BEST_FPERIOD_OVERRIDE = "1FQ".."8FQ"; segmentos: BDS("TER US Equity","PG_REVENUE","FUND_PER","Q2","EQY_FUND_YEAR","2026").'),
 ("Arquivos", "Modelos oficiais em P:\\Felipe Monteiro\\US Equities\\Modelos oficiais; scripts (pull_ate_bbg.py, build_ate_fernanda.py, ate_extra_sheets.py) em _wiki/_data/research/ATE_official_models_2026-09-18/."),
]
for k, v in NOTES:
    put(wn, r, 1, k, BLD, wrap=True); put(wn, r, 2, v, BLK, wrap=True); wn.row_dimensions[r].height = 60; r += 1
r += 1; put(wn, r, 1, "Log de qualidade de dados", BLD); r += 1
for line in LOG:
    put(wn, r, 2, line, GRY, wrap=True); r += 1

wb.save(OUT); print("saved", OUT); print("\n".join(LOG[:25]))
