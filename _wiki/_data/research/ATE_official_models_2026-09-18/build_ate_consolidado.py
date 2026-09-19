# -*- coding: utf-8 -*-
"""ATE Consolidado Advantest + TER.xlsx — the two official models side by side in US$ (Advantest at CY-average FX), combined
P&L, mix between the two (share of the pool, SoC vs memory, segments, regions, end-markets) and a sourced customer table.
Model numbers are READ from the two Template DCF workbooks (cached values after COM recalc) — nothing retyped."""
import os, json, datetime as dt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

HERE = os.path.dirname(os.path.abspath(__file__))
ADV_X = os.path.join(HERE, "Template DCF ADVANTEST.xlsx"); TER_X = os.path.join(HERE, "Template DCF TER.xlsx")
LAY = json.load(open(os.path.join(HERE, "layout.json")))
OUT = os.path.join(HERE, "ATE Consolidado Advantest + TER.xlsx")

F_TITLE = Font(name="Arial", size=16, bold=True, color="FF203864"); F_TXT = Font(name="Arial", size=10, color="FF202020")
F_TXTB = Font(name="Arial", size=10, bold=True, color="FF202020"); F_NOTE = Font(name="Arial", size=9, color="FF666666")
F_IN = Font(name="Arial", size=10, color="FF0000FF"); F_LINK = Font(name="Arial", size=10, color="FF008000")
F_WHITE = Font(name="Arial", size=11, bold=True, color="FFFFFFFF")
FILL_H = PatternFill("solid", fgColor="FFDCE6F1"); FILL_S = PatternFill("solid", fgColor="FF203864"); FILL_Y = PatternFill("solid", fgColor="FFFFF2CC")
NF_N = '#,##0;\\(#,##0\\);"-"'; NF_N1 = '#,##0.0;\\(#,##0.0\\);"-"'; NF_N2 = '0.00;\\(0.00\\);"-"'; NF_P = '0.0%;\\(0.0%\\);"-"'; NF_X = '0.0"x"'
YRS = [2023, 2024, 2025, 2026, 2027, 2028]; YC = ["D", "E", "F", "G", "H", "I"]     # Consolidado columns
MODEL_COL = {2023: "D", 2024: "E", 2025: "F", 2026: "G", 2027: "H", 2028: "I"}    # same in the models


def setc(ws, a, v, font=F_TXT, nf=None, fill=None, al=None, wrap=False):
    if isinstance(v, str) and v.startswith("=") and not v.startswith("=") is False:
        pass
    c = ws[a]; c.value = v; c.font = font
    if nf: c.number_format = nf
    if fill: c.fill = fill
    if al or wrap: c.alignment = Alignment(horizontal=al, wrap_text=wrap, vertical="top" if wrap else None)
    return c


def hdr(ws, r, text, c0="C", c1="K"):
    setc(ws, f"{c0}{r}", text, F_TXTB, fill=FILL_H)
    for ci in range(openpyxl.utils.column_index_from_string(c0) + 1, openpyxl.utils.column_index_from_string(c1) + 1):
        ws[f"{L(ci)}{r}"].fill = FILL_H


def yhdr(ws, r, labels, c0=4):
    for i, t in enumerate(labels):
        setc(ws, f"{L(c0 + i)}{r}", t, F_TXTB, fill=FILL_H, al="center")


def row(ws, r, label, vals, nf=NF_N, font=F_TXT, c0=4, note=None, bold=False, src_font=None):
    setc(ws, f"C{r}", label, F_TXTB if bold else F_TXT)
    for i, v in enumerate(vals):
        if v is None: continue
        f = font if not (isinstance(v, str) and v.startswith("=")) else (F_TXT if font is F_IN else font)
        if bold: f = Font(name="Arial", size=10, bold=True, color=f.color.rgb if f.color else "FF202020")
        setc(ws, f"{L(c0 + i)}{r}", v, f, nf=nf, al="right")
    if note: setc(ws, f"{L(c0 + len(vals) + 1)}{r}", note, F_NOTE, al="left")


def sheet(wb, name, title, sub, widths):
    ws = wb.create_sheet(name); ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2.25; ws.column_dimensions["B"].width = 2.25
    for k, w in widths.items(): ws.column_dimensions[k].width = w
    setc(ws, "C2", title, F_TITLE); setc(ws, "C3", sub, F_TXT); return ws


# ------------------------------------------------------------------ read the two models (cached values)
def model_vals():
    a = openpyxl.load_workbook(ADV_X, data_only=True)["Capa DCF - Base"]; t = openpyxl.load_workbook(TER_X, data_only=True)["Capa DCF - Base"]
    A = LAY["adv"]; T = LAY["ter"]; aw = int(A["wiki"]); tw = int(T["wiki"])
    apl = {k: int(v) for k, v in A["pl"].items()}; tpl = {k: int(v) for k, v in T["pl"].items()}
    out = {"adv": {}, "ter": {}, "pool": {}}
    for y, c in MODEL_COL.items():
        g = lambda ws, r: ws[f"{c}{r}"].value
        out["pool"][y] = dict(wfe=g(a, 8), ratio=g(a, 10), tam=g(a, 11), tam_soc=g(a, 16), tam_mem=g(a, 17))
        out["adv"][y] = dict(fx=g(a, 21), soc_us=g(a, 24), mem_us=g(a, 25), soc=g(a, 27), mem=g(a, 28), oth=g(a, 29), ts=g(a, 30), so=g(a, 31), rev=g(a, 32),
                             gm=g(a, apl["gm"]), gp=g(a, apl["gp"]), ebit=g(a, apl["ebit"]), ebitm=g(a, apl["ebitm"]), fcff=g(a, apl["fcff"]),
                             fin=g(a, aw + 4), ni=g(a, aw + 5), sh=g(a, aw + 6), eps=g(a, aw + 7), eps_ex=g(a, aw + 8), fcfe=g(a, aw + 9), cons_rev=g(a, aw + 10))
        out["ter"][y] = dict(share=g(t, 18), semi=g(t, 19), pt=g(t, 20), rob=g(t, 21), rev=g(t, 22), gm=g(t, tpl["gm"]), gp=g(t, tpl["gp"]), ebit=g(t, tpl["ebit"]),
                             ebitm=g(t, tpl["ebitm"]), fcff=g(t, tpl["fcff"]), other=g(t, tw + 4), ni=g(t, tw + 5), sh=g(t, tw + 6), eps=g(t, tw + 7), fcfe=g(t, tw + 9), cons_rev=g(t, tw + 10))
    return out


M = model_vals()
# Advantest CY history (BBG quarterly sums; ¥mm) for NI/EPS where the model rows are blank in base years
ADV_HIST = {2023: dict(ni=77737, eps=105.49, sh=739.65, gp=255094), 2024: dict(ni=136357, eps=184.74, sh=740.38, gp=375485), 2025: dict(ni=288493, eps=395.02, sh=732.94, gp=644221)}
TER_HIST = {2023: dict(ni=None, eps=2.93, sh=164.3), 2024: dict(ni=None, eps=3.22, sh=163.3), 2025: dict(ni=None, eps=3.97, sh=159.7)}
BBG = dict(date="2026-09-18", adv_px=32050, adv_sh=732.0, adv_mcap=23460600, adv_ev=23155642, adv_pe=36.05, adv_pt=43178, adv_rating=4.73, adv_n=26,
           ter_px=359.90, ter_sh=156.34, ter_mcap=56267.0, ter_ev=55886.2, ter_pe=38.35, ter_pt=450.87, ter_rating=4.32, ter_n=19, usdjpy=156.69)
ADV_CONS = {2026: (1525591, 730365), 2027: (2140572, 1094998), 2028: (2639526, 1379757)}   # BBG 1CY-3CY sales / EBIT (¥mm)
TER_CONS = {2026: (5065.9, 1655.7), 2027: (6237.3, 2143.5), 2028: (7543.4, 2724.3)}
TER_SUB = {2025: (1889.7, 504.9, 129.2), 2026: (3205, 885, 230), 2027: (3900, 1150, 245), 2028: (4950, 1400, 290)}   # SOC / Memory / IST (initiation mix for 26-28)

wb = openpyxl.Workbook(); wb.remove(wb.active)

# =====================================================================================================
# Sheet 1 — Consolidado
# =====================================================================================================
ws = sheet(wb, "Consolidado", "ATE | Advantest + Teradyne — consolidado (US$ milhões)",
           "Fonte: Template DCF ADVANTEST.xlsx e Template DCF TER.xlsx (modelos oficiais, 2026-09-18). Advantest convertida ao FX médio do ano-calendário do modelo (¥141,4 / 151,9 / 150,0 / 157 / 150 / 150). CY23-25 = reportado (Advantest calendarizada a partir dos trimestres BBG); CY26-28 = cenário base.",
           {"C": 58, "D": 12.5, "E": 12.5, "F": 12.5, "G": 12.5, "H": 12.5, "I": 12.5, "J": 3, "K": 70})
setc(ws, "C4", "Azul: valores colados dos modelos/fontes. Preto: fórmulas nesta planilha. Colunas CY26-28 = cenário base Capstone (sem rating para a Advantest; TER NEUTRAL, PT $400).", F_NOTE)
yhdr(ws, 6, [f"CY{str(y)[2:]}{'A' if y <= 2025 else 'E'}" for y in YRS]); setc(ws, "K6", "Fonte / nota", F_TXTB, fill=FILL_H)
r = 8; hdr(ws, r, "Advantest (6857 JP) — ¥ → US$ ao FX médio do CY"); r += 1
R = {}
def put(key, label, vals, nf=NF_N, font=F_IN, note=None, bold=False):
    global r
    row(ws, r, label, vals, nf=nf, font=font, note=note, bold=bold); R[key] = r; r += 1
put("a_fx", "FX ¥/US$ (média do ano; CY26+ premissa do modelo)", [M["adv"][y]["fx"] for y in YRS], NF_N1, note="Template DCF ADVANTEST | Capa linha 21 (BBG USDJPY médias mensais CY23-25; 157 / 150 premissa).")
put("a_rev_jpy", "Receita (¥ mi)", [M["adv"][y]["rev"] for y in YRS], note="Capa linha 32 (CY23-25 soma dos trimestres BBG; CY26-28 modelo).")
put("a_rev", "Receita (US$ mi)", [f"={c}{R['a_rev_jpy']}/{c}{R['a_fx']}" for c in YC], font=F_TXT, bold=True)
put("a_g", "Crescimento (US$)", [None] + [f"={YC[i]}{R['a_rev']}/{YC[i-1]}{R['a_rev']}-1" for i in range(1, 6)], NF_P, font=F_TXT)
put("a_gm", "Margem bruta", [M["adv"][y]["gm"] for y in YRS], NF_P)
put("a_gp", "Lucro bruto (US$ mi)", [f"={c}{R['a_rev']}*{c}{R['a_gm']}" for c in YC], font=F_TXT)
put("a_ebit_jpy", "Resultado operacional IFRS (¥ mi)", [M["adv"][y]["ebit"] for y in YRS], note="Capa linha 43 (= EBIT após SBC).")
put("a_ebit", "Resultado operacional (US$ mi)", [f"={c}{R['a_ebit_jpy']}/{c}{R['a_fx']}" for c in YC], font=F_TXT)
put("a_om", "Margem operacional", [f"={c}{R['a_ebit']}/{c}{R['a_rev']}" for c in YC], NF_P, font=F_TXT)
put("a_ni_jpy", "Lucro líquido (¥ mi)", [ADV_HIST[y]["ni"] if y <= 2025 else M["adv"][y]["ni"] for y in YRS], note="CY23-25 BBG trimestral somado; CY26-28 bloco wiki do modelo (CY26 inclui ¥66 bi de resultado financeiro não recorrente).")
put("a_ni", "Lucro líquido (US$ mi)", [f"={c}{R['a_ni_jpy']}/{c}{R['a_fx']}" for c in YC], font=F_TXT)
put("a_eps", "EPS (¥)", [ADV_HIST[y]["eps"] if y <= 2025 else M["adv"][y]["eps"] for y in YRS], NF_N2, note="CY26E ex não recorrente: ¥" + f"{M['adv'][2026]['eps_ex']:,.0f}" + ".")
put("a_epsg", "Crescimento EPS", [None] + [f"={YC[i]}{R['a_eps']}/{YC[i-1]}{R['a_eps']}-1" for i in range(1, 6)], NF_P, font=F_TXT)
put("a_fcf", "FCF equity (US$ mi) | CY26+ modelo; FY25 reportado ¥302 bi", [None, None, None] + [f"={M['adv'][y]['fcfe']}/{c}{R['a_fx']}" for y, c in zip(YRS[3:], YC[3:])], font=F_TXT)
put("a_cons", "Consenso BBG receita CY (¥ mi) — memo", [None, None, None] + [ADV_CONS[y][0] for y in YRS[3:]], note="bdp BEST_SALES 1CY/2CY/3CY 2026-09-18. ⚠ 1CY (1.525,6) < soma dos trimestres reportados + kFQ (~1.590).")
put("a_vs", "Casa ÷ consenso − 1 (receita)", [None, None, None] + [f"={c}{R['a_rev_jpy']}/{c}{R['a_cons']}-1" for c in YC[3:]], NF_P, font=F_TXT)
r += 1; hdr(ws, r, "Teradyne (TER US) — US$ milhões, ano fiscal = CY"); r += 1
put("t_rev", "Receita (US$ mi)", [M["ter"][y]["rev"] for y in YRS], bold=True, note="Template DCF TER | Capa linha 22 (CY23-25 10-K; CY26-28 modelo = iniciação 2026-09-16 ±0,1%).")
put("t_g", "Crescimento", [None] + [f"={YC[i]}{R['t_rev']}/{YC[i-1]}{R['t_rev']}-1" for i in range(1, 6)], NF_P, font=F_TXT)
put("t_gm", "Margem bruta (non-GAAP)", [M["ter"][y]["gm"] for y in YRS], NF_P)
put("t_gp", "Lucro bruto (US$ mi)", [f"={c}{R['t_rev']}*{c}{R['t_gm']}" for c in YC], font=F_TXT)
put("t_ebit", "Resultado operacional non-GAAP (US$ mi)", [M["ter"][y]["ebit"] for y in YRS], note="Capa (EBIT após SBC = OI non-GAAP; CY23-25 margens ~20/21/22% da tabela de casa).")
put("t_om", "Margem operacional", [f"={c}{R['t_ebit']}/{c}{R['t_rev']}" for c in YC], NF_P, font=F_TXT)
put("t_ni", "Lucro líquido non-GAAP (US$ mi)", [TER_HIST[y]["eps"] * TER_HIST[y]["sh"] if y <= 2025 else M["ter"][y]["ni"] for y in YRS], note="CY23-25 = EPS non-GAAP reportado × ações diluídas 10-K (aprox.); CY26-28 bloco wiki do modelo.")
put("t_eps", "EPS non-GAAP (US$)", [TER_HIST[y]["eps"] if y <= 2025 else M["ter"][y]["eps"] for y in YRS], NF_N2, note="Iniciação 2026-09-16: 9,03 / 11,92 / 15,99; PT $400 = 25x CY28E.")
put("t_epsg", "Crescimento EPS", [None] + [f"={YC[i]}{R['t_eps']}/{YC[i-1]}{R['t_eps']}-1" for i in range(1, 6)], NF_P, font=F_TXT)
put("t_fcf", "FCF equity (US$ mi) | CY23-25 reportado", [None, 470, 450] + [M["ter"][y]["fcfe"] for y in YRS[3:]], note="FY24/25 FCF reportado 0,47 / 0,45 bi (wiki TER.md); CY26+ modelo.")
put("t_cons", "Consenso BBG receita (US$ mi) — memo", [None, None, None] + [TER_CONS[y][0] for y in YRS[3:]], note="bdp BEST_SALES 1FY/2FY/3FY 2026-09-18.")
put("t_vs", "Casa ÷ consenso − 1 (receita)", [None, None, None] + [f"={c}{R['t_rev']}/{c}{R['t_cons']}-1" for c in YC[3:]], NF_P, font=F_TXT)
r += 1; hdr(ws, r, "Consolidado Advantest + Teradyne (US$ milhões)"); r += 1
put("c_rev", "Receita combinada", [f"={c}{R['a_rev']}+{c}{R['t_rev']}" for c in YC], font=F_TXT, bold=True)
put("c_g", "Crescimento", [None] + [f"={YC[i]}{R['c_rev']}/{YC[i-1]}{R['c_rev']}-1" for i in range(1, 6)], NF_P, font=F_TXT)
put("c_gp", "Lucro bruto combinado", [f"={c}{R['a_gp']}+{c}{R['t_gp']}" for c in YC], font=F_TXT)
put("c_gm", "Margem bruta combinada", [f"={c}{R['c_gp']}/{c}{R['c_rev']}" for c in YC], NF_P, font=F_TXT)
put("c_ebit", "Resultado operacional combinado", [f"={c}{R['a_ebit']}+{c}{R['t_ebit']}" for c in YC], font=F_TXT)
put("c_om", "Margem operacional combinada", [f"={c}{R['c_ebit']}/{c}{R['c_rev']}" for c in YC], NF_P, font=F_TXT)
put("c_ni", "Lucro líquido combinado", [f"={c}{R['a_ni']}+{c}{R['t_ni']}" for c in YC], font=F_TXT)
put("c_fcf", "FCF equity combinado (CY26+)", [None, None, None] + [f"={c}{R['a_fcf']}+{c}{R['t_fcf']}" for c in YC[3:]], font=F_TXT)
r += 1; hdr(ws, r, "Mix entre as duas"); r += 1
put("m_a", "Advantest / receita combinada", [f"={c}{R['a_rev']}/{c}{R['c_rev']}" for c in YC], NF_P, font=F_TXT, bold=True)
put("m_t", "Teradyne / receita combinada", [f"={c}{R['t_rev']}/{c}{R['c_rev']}" for c in YC], NF_P, font=F_TXT, bold=True)
put("m_a_ebit", "Advantest / resultado operacional combinado", [f"={c}{R['a_ebit']}/{c}{R['c_ebit']}" for c in YC], NF_P, font=F_TXT)
put("m_gap", "Diferencial de margem operacional (Advantest − Teradyne, pp)", [f"={c}{R['a_om']}-{c}{R['t_om']}" for c in YC], NF_P, font=F_TXT)
put("m_gdiff", "Diferencial de crescimento (Advantest − Teradyne, US$)", [None] + [f"={YC[i]}{R['a_g']}-{YC[i]}{R['t_g']}" for i in range(1, 6)], NF_P, font=F_TXT)
r += 1; hdr(ws, r, "Pool de teste (ATE) — base Advantest (SoC + memória, ex burn-in), idêntico nos dois modelos"); r += 1
put("p_wfe", "WFE global (US$ bi)", [M["pool"][y]["wfe"] for y in YRS], NF_N1, note="Capa linha 8 (ambos os modelos).")
put("p_ratio", "Intensidade de teste (ATE / WFE)", [M["pool"][y]["ratio"] for y in YRS], NF_P, note="CY23-26 calibrado ao TAM da Advantest; CY27 8,0% = variante de casa (lag WFE→wafer).")
put("p_tam", "TAM ATE total (US$ bi)", [M["pool"][y]["tam"] for y in YRS], NF_N2, bold=True, note="CY24 6,0 / CY25 9,0 / CY26e 13,75 = deck Advantest 2026-07-29 (mid); CY27-28 modelo.")
put("p_tam_soc", "TAM SoC (US$ bi)", [M["pool"][y]["tam_soc"] for y in YRS], NF_N2)
put("p_tam_mem", "TAM memória (US$ bi)", [M["pool"][y]["tam_mem"] for y in YRS], NF_N2)
put("p_adv_us", "Advantest test systems SoC + memória (US$ mi)", [M["adv"][y]["soc_us"] + M["adv"][y]["mem_us"] for y in YRS], note="Capa ADVANTEST linhas 24+25 (CY23-25 implícito do mix FY; CY26-28 = TAM × share).")
put("p_ter_us", "Teradyne Semi Test ex-IST (US$ mi)", [M["ter"][y]["semi"] - (TER_SUB.get(y, (0, 0, 0))[2] if y >= 2025 else {2023: 138.6, 2024: 85.0}[y]) for y in YRS], note="Capa TER linha 19 menos IST (BBG PG_REVENUE 2023-25: 138,6 / 85,0 / 129,2; 2026-28 iniciação 230 / 245 / 290).")
put("p_duo", "Duopólio / TAM", [f"=({c}{R['p_adv_us']}+{c}{R['p_ter_us']})/1000/{c}{R['p_tam']}" for c in YC], NF_P, font=F_TXT, bold=True)
put("p_adv_sh", "Advantest / TAM", [f"={c}{R['p_adv_us']}/1000/{c}{R['p_tam']}" for c in YC], NF_P, font=F_TXT)
put("p_ter_sh", "Teradyne (ex-IST) / TAM", [f"={c}{R['p_ter_us']}/1000/{c}{R['p_tam']}" for c in YC], NF_P, font=F_TXT)
put("p_oth", "Residual para outros vendors", [f"=1-{c}{R['p_duo']}" for c in YC], NF_P, font=F_TXT, note="Cai de 11% (CY25) para ~3% (CY28) — tensão aberta: ou o TAM mid-point da Advantest é conservador ou um dos dois shares está pesado.")
put("p_adv_in_duo", "Advantest / duopólio (ATE)", [f"={c}{R['p_adv_us']}/({c}{R['p_adv_us']}+{c}{R['p_ter_us']})" for c in YC], NF_P, font=F_TXT, bold=True)
r += 1; hdr(ws, r, "Pool SoC vs memória (US$ milhões)"); r += 1
put("s_adv_soc", "Advantest SoC test systems", [M["adv"][y]["soc_us"] for y in YRS])
put("s_ter_soc", "Teradyne SOC", [None, None] + [f"={M['ter'][y]['semi']}*{TER_SUB[y][0]}/{sum(TER_SUB[y])}" if y >= 2026 else TER_SUB[2025][0] for y in YRS[2:]], font=F_TXT, note="CY25 10-K/BBG 1.889,7; CY26-28 = Semi Test do modelo × mix da iniciação (74% / 74% / 75% SOC).")
put("s_soc_adv", "Advantest / (Advantest + Teradyne) em SoC", [None, None] + [f"={c}{R['s_adv_soc']}/({c}{R['s_adv_soc']}+{c}{R['s_ter_soc']})" for c in YC[2:]], NF_P, font=F_TXT, bold=True)
put("s_adv_soc_sh", "Advantest / TAM SoC", [f"={c}{R['s_adv_soc']}/1000/{c}{R['p_tam_soc']}" for c in YC], NF_P, font=F_TXT, note="Mgmt: 66% CY25, 'path to >70%'.")
put("s_ter_soc_sh", "Teradyne / TAM SoC", [None, None] + [f"={c}{R['s_ter_soc']}/1000/{c}{R['p_tam_soc']}" for c in YC[2:]], NF_P, font=F_TXT)
put("s_adv_mem", "Advantest memory test systems", [M["adv"][y]["mem_us"] for y in YRS])
put("s_ter_mem", "Teradyne Memory", [386.0, 501.8] + [f"={M['ter'][y]['semi']}*{TER_SUB[y][1]}/{sum(TER_SUB[y])}" if y >= 2026 else TER_SUB[2025][1] for y in YRS[2:]], font=F_TXT, note="BBG PG_REVENUE 2023-25 (386,0 / 501,8 / 504,9); CY26-28 mix da iniciação.")
put("s_mem_adv", "Advantest / (Advantest + Teradyne) em memória", [f"={c}{R['s_adv_mem']}/({c}{R['s_adv_mem']}+{c}{R['s_ter_mem']})" for c in YC], NF_P, font=F_TXT, bold=True)
put("s_adv_mem_sh", "Advantest / TAM memória", [f"={c}{R['s_adv_mem']}/1000/{c}{R['p_tam_mem']}" for c in YC], NF_P, font=F_TXT, note="Mgmt 07-29: share de memória 'may experience a decline this year' (NAND); TER concorda.")
put("s_ter_mem_sh", "Teradyne / TAM memória", [f"={c}{R['s_ter_mem']}/1000/{c}{R['p_tam_mem']}" for c in YC], NF_P, font=F_TXT)
r += 1; hdr(ws, r, f"Valuation (BBG {BBG['date']}) — informativo"); r += 1
yhdr(ws, r, ["Advantest", "Teradyne", "Combinado"]); r += 1
def vrow(label, a, t, comb=None, nf=NF_N, note=None):
    global r
    setc(ws, f"C{r}", label); setc(ws, f"D{r}", a, F_IN if not (isinstance(a, str) and a.startswith("=")) else F_TXT, nf=nf, al="right"); setc(ws, f"E{r}", t, F_IN if not (isinstance(t, str) and t.startswith("=")) else F_TXT, nf=nf, al="right")
    if comb is not None: setc(ws, f"F{r}", comb, F_TXT, nf=nf, al="right")
    if note: setc(ws, f"K{r}", note, F_NOTE)
    rr = r; r += 1; return rr
v_px = vrow("Preço (moeda local)", BBG["adv_px"], BBG["ter_px"], nf=NF_N2, note="PX_LAST. USDJPY " + str(BBG["usdjpy"]) + ".")
v_fx = vrow("FX ¥/US$ spot", BBG["usdjpy"], 1.0, nf=NF_N2)
v_mc = vrow("Market cap (US$ mi)", f"={BBG['adv_mcap']}/D{v_fx}", BBG["ter_mcap"], f"=D{r}+E{r}", note="CUR_MKT_CAP (Advantest ¥23,46 tn / spot).")
v_ev = vrow("Enterprise value (US$ mi)", f"={BBG['adv_ev']}/D{v_fx}", BBG["ter_ev"], f"=D{r}+E{r}", note="CURR_ENTP_VAL (Advantest ¥23,16 tn).")
v_mix = vrow("Peso no market cap combinado", f"=D{v_mc}/F{v_mc}", f"=E{v_mc}/F{v_mc}", nf=NF_P)
v_evs26 = vrow("EV / receita CY26E (casa)", f"=D{v_ev}/G{R['a_rev']}", f"=E{v_ev}/G{R['t_rev']}", f"=F{v_ev}/G{R['c_rev']}", nf=NF_X)
v_evs27 = vrow("EV / receita CY27E (casa)", f"=D{v_ev}/H{R['a_rev']}", f"=E{v_ev}/H{R['t_rev']}", f"=F{v_ev}/H{R['c_rev']}", nf=NF_X)
v_pe26 = vrow("P/E CY26E (EPS casa)", f"=D{v_px}/G{R['a_eps']}", f"=E{v_px}/G{R['t_eps']}", nf=NF_X, note="Advantest CY26E inclui ganhos financeiros não recorrentes; ex: ¥" + f"{M['adv'][2026]['eps_ex']:,.0f} → " + f"{BBG['adv_px']/M['adv'][2026]['eps_ex']:.1f}x.")
v_pe27 = vrow("P/E CY27E (EPS casa)", f"=D{v_px}/H{R['a_eps']}", f"=E{v_px}/H{R['t_eps']}", nf=NF_X)
v_pe28 = vrow("P/E CY28E (EPS casa)", f"=D{v_px}/I{R['a_eps']}", f"=E{v_px}/I{R['t_eps']}", nf=NF_X)
vrow("P/E blended forward BBG (BEST_PE_RATIO)", BBG["adv_pe"], BBG["ter_pe"], nf=NF_X)
vrow("PT médio consenso (moeda local)", BBG["adv_pt"], BBG["ter_pt"], nf=NF_N2, note=f"{BBG['adv_n']} / {BBG['ter_n']} analistas; rating {BBG['adv_rating']} / {BBG['ter_rating']}. Casa: TER PT $400 (NEUTRAL); Advantest sem rating.")
vrow("Upside ao PT de consenso", f"=D{r-1}/D{v_px}-1", f"=E{r-1}/E{v_px}-1", nf=NF_P)
r += 1
for t in ["Bases: Advantest reporta FY-Mar em IFRS (¥); as colunas são anos-calendário somados a partir dos trimestres (histórico) e do modelo (projeção). Teradyne non-GAAP (exclui amortização de intangíveis e reestruturação; SBC NÃO excluído).",
          "TAM na base da própria Advantest (SoC + memória, EX burn-in). Teradyne Semi Test inclui IST (storage test) — excluído aqui para comparar com o mesmo pool. Não misturar com 'teste ÷ receita de semis' (~1%, UBS) nem com a base TER (7-9% do WFE incl. burn-in).",
          "Consenso BBG: EPS da Advantest NÃO é calendarizado (1CY = 1FY); comparar EPS em FY-Mar (¥927 / ¥1.186 / ¥1.422 FY26-28) ou por trimestre."]:
    setc(ws, f"C{r}", t, F_NOTE); r += 1
ws.freeze_panes = "D7"

# =====================================================================================================
# Sheet 2 — Mix e segmentos (history)
# =====================================================================================================
wm = sheet(wb, "Mix e segmentos", "ATE | Mix por segmento e produto — histórico e modelo",
           "Advantest em FY-Mar (¥ bi; FY18 = abr-2018→mar-2019) e Teradyne em ano-calendário (US$ mi). Fontes: BBG PG_REVENUE (FUND_PER=A, 2026-09-18), deck Advantest 1Q FY26, 10-K FY25 Teradyne, modelos oficiais.",
           {"C": 52, **{L(i): 11.5 for i in range(4, 16)}, "Q": 3, "R": 60})
r = 5
ADV_FY = list(range(2018, 2027))
ADV_SEG = {"SoC test systems": [148.6, 154.9, 141.5, 225.6, 325.4, 245.7, 440.4, 767.4, 1243.5],
           "Memory test systems": [63.1, 42.2, 65.8, 63.3, 78.8, 85.9, 157.7, 171.5, 227.0],
           "Outros sistemas (mechatronics → 'Other systems' a partir de FY24)": [39.2, 36.3, 40.0, 42.3, 59.9, 52.7, 84.7, 80.5, 104.5],
           "Services & Others (FY18-23: 'Services, Support & Others' incl. SLT)": [31.5, 42.5, 66.8, 85.8, 96.1, 102.3, 96.9, 109.2, 139.0]}
ADV_FX_FY = [111.07, 108.38, 106.20, 112.92, 135.67, 145.53, 152.55, 151.10, 152.0]
hdr(wm, r, "Advantest — receita por produto, FY-Mar (¥ bilhões)", c1="R"); r += 1
yhdr(wm, r, [f"FY{str(y)[2:]}{'e' if y == 2026 else ''}" for y in ADV_FY]); setc(wm, f"R{r}", "Fonte / nota", F_TXTB, fill=FILL_H); r += 1
seg_rows = []
for name, vals in ADV_SEG.items():
    row(wm, r, name, vals, NF_N1, F_IN); seg_rows.append(r); r += 1
setc(wm, f"R{seg_rows[0]}", "BBG PG_REVENUE (FY18-23 'SoC' dentro de Semiconductor & Component Test; FY24-25 deck 1Q FY26); FY26e = guidance jul-2026.", F_NOTE)
setc(wm, f"R{seg_rows[2]}", "FY24+ nova estrutura de 2 segmentos: SLT e interfaces migraram de Serviços para 'Other systems' — quebra de série entre FY23 e FY24.", F_NOTE)
tot = r; row(wm, r, "Receita total", [f"=SUM({L(4+i)}{seg_rows[0]}:{L(4+i)}{seg_rows[-1]})" for i in range(9)], NF_N1, F_TXT, bold=True); r += 1
row(wm, r, "Crescimento", [None] + [f"={L(4+i)}{tot}/{L(3+i)}{tot}-1" for i in range(1, 9)], NF_P, F_TXT); r += 1
for name, sr in zip(ADV_SEG, seg_rows):
    row(wm, r, "  % " + name.split(" (")[0], [f"={L(4+i)}{sr}/{L(4+i)}{tot}" for i in range(9)], NF_P, F_TXT); r += 1
fxr = r; row(wm, r, "FX ¥/US$ (média FY-Mar)", ADV_FX_FY, NF_N1, F_IN, note="BBG USDJPY médias mensais abr→mar; FY26e = premissa da companhia (¥152; YTD 159).", ); r += 1
row(wm, r, "Receita total (US$ mi)", [f"={L(4+i)}{tot}*1000/{L(4+i)}{fxr}" for i in range(9)], NF_N, F_TXT); a_us = r; r += 1
row(wm, r, "SoC (US$ mi)", [f"={L(4+i)}{seg_rows[0]}*1000/{L(4+i)}{fxr}" for i in range(9)], NF_N, F_TXT); a_soc_us = r; r += 1
row(wm, r, "Memória (US$ mi)", [f"={L(4+i)}{seg_rows[1]}*1000/{L(4+i)}{fxr}" for i in range(9)], NF_N, F_TXT); a_mem_us = r; r += 1
r += 1; hdr(wm, r, "Advantest — mix de aplicação e trimestres recentes", c1="R"); r += 1
yhdr(wm, r, ["FY24", "FY25", "FY26e"]); r += 1
row(wm, r, "SoC: Computing / Communications (% do SoC)", [0.90, None, 0.95], NF_P, F_IN, note="Deck 1Q FY26: FY24 90/10, FY26e 95/5 (Auto / Industrial / Consumer / DDIC = resto)."); r += 1
row(wm, r, "Memória: DRAM (% da memória)", [0.95, 0.90, 0.85], NF_P, F_IN, note="Deck 1Q FY26: DRAM 95 / 90 / 85%; não volátil 5 / 10 / 15% (triplica em dois anos)."); r += 1
row(wm, r, "SoC: ~80% HPC / AI (comentário)", [None, 0.80, None], NF_P, F_IN, note="Call 3Q FY25 (2026-01-28): ~80% do negócio SoC é HPC/AI."); r += 1
r += 1; yhdr(wm, r, ["Q4 FY25", "Q1 FY26"]); setc(wm, f"C{r}", "Trimestres (¥ bi) — jan-mar 2026 / abr-jun 2026", F_TXTB); r += 1
for name, v in [("SoC test systems", [237.2, 259.6]), ("Memory test systems", [36.8, 48.0]), ("Other systems", [22.3, 26.0]), ("Support services", [13.1, 13.6]), ("Others", [18.6, 20.3]), ("Total", [328.1, 367.5])]:
    row(wm, r, name, v, NF_N1, F_IN, bold=(name == "Total")); r += 1
setc(wm, f"R{r-6}", "Deck 1Q FY26 (2026-07-29).", F_NOTE)
r += 1; hdr(wm, r, "Teradyne — receita por segmento e sub-segmento, CY (US$ milhões)", c1="R"); r += 1
TY = list(range(2019, 2026)); yhdr(wm, r, [str(y) for y in TY]); setc(wm, f"R{r}", "Fonte / nota", F_TXTB, fill=FILL_H); r += 1
TER_SEG = [("Semiconductor Test", [1552.6, 2259.6, 2642.3, 2080.6, 1957.2, 2123.9, 2523.7], "BBG PG_REVENUE / 10-K; 2023-25 na segmentação de 2025 (inclui IST)."),
           ("  SOC", [1286.4, 1877.4, 2246.7, 1706.9, 1432.6, 1537.1, 1889.7], "BBG PG_REVENUE nível 2."),
           ("  Memory", [266.1, 382.2, 395.6, 373.7, 386.0, 501.8, 504.9], "BBG PG_REVENUE nível 2."),
           ("  IST (storage/system test dentro de Semi Test desde 2023)", [None, None, None, None, 138.6, 85.0, 129.2], "BBG PG_REVENUE; antes de 2023 dentro de System Test."),
           ("Product Test (2019-22: System Test + Wireless Test)", [444.8, 582.7, 684.6, 671.0, 343.9, 331.1, 358.0], "2019-22 soma de System + Wireless (segmentação antiga, incl. storage); 2023-25 restated ex-IST."),
           ("Robotics", [296.8, 279.7, 375.9, 403.1, 375.2, 364.8, 308.3], "BBG PG_REVENUE / 10-K.")]
trow = {}
for name, vals, src in TER_SEG:
    row(wm, r, name, vals, NF_N1, F_IN, note=src); trow[name] = r; r += 1
ttot = r; row(wm, r, "Receita total", [f"={L(4+i)}{trow['Semiconductor Test']}+{L(4+i)}{trow['Product Test (2019-22: System Test + Wireless Test)']}+{L(4+i)}{trow['Robotics']}" for i in range(7)], NF_N1, F_TXT, bold=True, note="10-K: 2.295,0 / 3.121,5 / 3.702,9 / 3.155,0 / 2.676,3 / 2.819,9 / 3.190,0 (diferenças de arredondamento/corporate)."); r += 1
for name in ["Semiconductor Test", "  SOC", "  Memory", "Product Test (2019-22: System Test + Wireless Test)", "Robotics"]:
    row(wm, r, "  % " + name.strip(), [f"={L(4+i)}{trow[name]}/{L(4+i)}{ttot}" for i in range(7)], NF_P, F_TXT); r += 1
row(wm, r, "  SOC / Semi Test", [f"={L(4+i)}{trow['  SOC']}/{L(4+i)}{trow['Semiconductor Test']}" for i in range(7)], NF_P, F_TXT); r += 1
r += 1; yhdr(wm, r, ["Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 CY26"]); setc(wm, f"C{r}", "Teradyne — end-market e trimestre", F_TXTB); r += 1
row(wm, r, "AI-related como % da receita", [0.50, 0.60, 0.70, None], NF_P, F_IN, note="Calls 1Q FY26 (2026-04-29): ~50% → ~60% → ~70%."); r += 1
row(wm, r, "Compute como % da receita de produto SOC", [None, None, None, 0.70], NF_P, F_IN, note="Call 2Q CY26 (2026-07-29): compute 70% do SOC product revenue, +~600% y/y."); r += 1
row(wm, r, "SOC / Memory / IST no trimestre (US$ mi)", [None, None, None, "843 / 212 / 67"], None, F_IN, note="Call 2Q CY26: Semi Test $1.122 mi = SOC 843 + memória 212 (recorde) + IST 67."); r += 1
r += 1; hdr(wm, r, "Duopólio SoC e memória — histórico em US$ (Advantest FY-Mar ao FX médio FY vs Teradyne CY)", c1="R"); r += 1
yhdr(wm, r, [str(y) for y in TY]); setc(wm, f"R{r}", "⚠ Basis: FY-Mar da Advantest (FY19 = abr-19→mar-20) contra CY da Teradyne — desalinhamento de um trimestre.", F_NOTE); r += 1
# Advantest FY columns for 2019..2025 map to ADV_FY index 1..7
adv_soc_us_cells = [f"={L(4+j)}{a_soc_us}" for j in range(1, 8)]; adv_mem_us_cells = [f"={L(4+j)}{a_mem_us}" for j in range(1, 8)]
row(wm, r, "Advantest SoC (US$ mi, FY-Mar)", adv_soc_us_cells, NF_N, F_TXT); d1 = r; r += 1
row(wm, r, "Teradyne SOC (US$ mi, CY)", [f"={L(4+i)}{trow['  SOC']}" for i in range(7)], NF_N, F_TXT); d2 = r; r += 1
row(wm, r, "Advantest / (Advantest + Teradyne) em SoC", [f"={L(4+i)}{d1}/({L(4+i)}{d1}+{L(4+i)}{d2})" for i in range(7)], NF_P, F_TXT, bold=True); r += 1
row(wm, r, "Advantest memória (US$ mi, FY-Mar)", adv_mem_us_cells, NF_N, F_TXT); d3 = r; r += 1
row(wm, r, "Teradyne Memory (US$ mi, CY)", [f"={L(4+i)}{trow['  Memory']}" for i in range(7)], NF_N, F_TXT); d4 = r; r += 1
row(wm, r, "Advantest / (Advantest + Teradyne) em memória", [f"={L(4+i)}{d3}/({L(4+i)}{d3}+{L(4+i)}{d4})" for i in range(7)], NF_P, F_TXT, bold=True); r += 1
row(wm, r, "Duopólio SoC + memória (US$ mi)", [f"={L(4+i)}{d1}+{L(4+i)}{d2}+{L(4+i)}{d3}+{L(4+i)}{d4}" for i in range(7)], NF_N, F_TXT); d5 = r; r += 1
row(wm, r, "  Advantest / duopólio", [f"=({L(4+i)}{d1}+{L(4+i)}{d3})/{L(4+i)}{d5}" for i in range(7)], NF_P, F_TXT, bold=True); r += 1
row(wm, r, "TAM ATE referência (US$ bi) — Advantest deck (CY24-25) / Capstone Industry Assumptions (2019-23, base antiga)", [None, None, 7.5, 6.2, 4.9, 6.0, 9.0], NF_N2, F_IN, note="2021-23 = ASML_Peers_SemiCap_Felipe.xlsx Industry Assumptions (base antiga, ~40% abaixo da série Advantest em 2025); 2024-25 deck Advantest 2026-07-29."); d6 = r; r += 1
row(wm, r, "  Duopólio / TAM referência", [None, None] + [f"={L(4+i)}{d5}/1000/{L(4+i)}{d6}" for i in range(2, 7)], NF_P, F_TXT, note="2021-23 >100% confirma que a base antiga do peer model subestima o TAM."); r += 1
wm.freeze_panes = "D5"

# =====================================================================================================
# Sheet 3 — Regiões
# =====================================================================================================
wr = sheet(wb, "Regiões", "ATE | Mix geográfico", "Teradyne: receita por país (localização do cliente, 10-K / 10-Q). Advantest: ship-to por região (deck trimestral) e localização do cliente (tanshin).",
           {"C": 40, **{L(i): 11.5 for i in range(4, 16)}, "Q": 3, "R": 70})
r = 5; hdr(wr, r, "Teradyne — receita por país (US$ mi; localização do site do cliente)", c1="R"); r += 1
TREG_Y = [2021, 2022, 2023, 2024, 2025]; yhdr(wr, r, [str(y) for y in TREG_Y] + ["1H26 %", "2Q26 %"]); r += 1
TREG = [("Taiwan", [1117.9, 626.4, 384.8, 602.0, 1155.2], 0.41, 0.40), ("China", [632.0, 491.8, 314.9, 375.2, 451.3], 0.11, 0.12), ("Coreia", [502.2, 544.8, 394.7, 695.7, 446.3], 0.20, 0.20),
        ("Estados Unidos", [392.6, 469.9, 433.7, 374.3, 360.9], 0.07, 0.07), ("Europa", [260.0, 268.4, 273.8, 251.3, 215.4], 0.06, 0.04), ("Japão", [166.2, 162.9, 281.7, 159.8, None], 0.01, 0.01),
        ("Filipinas", [166.8, 124.1, 189.4, 53.6, 92.5], 0.02, 0.02), ("Singapura", [121.6, 99.5, 117.0, 90.1, 95.2], 0.04, 0.05), ("Tailândia", [138.8, 137.4, 91.8, 49.3, 67.6], 0.02, 0.03),
        ("Malásia", [136.8, 142.2, 89.2, 62.4, 107.4], 0.04, 0.03)]
TREG_TOT = [3702.9, 3155.0, 2676.3, 2819.9, 3190.0]
reg_rows = []
for name, vals, h1, q2 in TREG:
    row(wr, r, name, vals + [h1, q2], NF_N1, F_IN);
    for c in ("I", "J"): wr[f"{c}{r}"].number_format = NF_P
    reg_rows.append(r); r += 1
row(wr, r, "Japão + resto do mundo (residual)", [f"={TREG_TOT[i]}-SUM({L(4+i)}{reg_rows[0]}:{L(4+i)}{reg_rows[-1]})" for i in range(5)] + [0.03, 0.04], NF_N1, F_TXT, note="2025: Japão ~2% + RoW ~4% (10-K %); o valor de Japão 2025 não foi extraído em US$.");
for c in ("I", "J"): wr[f"{c}{r}"].number_format = NF_P
r += 1
row(wr, r, "Total", TREG_TOT + [1.0, 1.0], NF_N1, F_IN, bold=True, note="10-K FY23 / FY24 / FY25 'revenues by country'; 10-Q 2Q FY26 (six months / three months ended 28-jun-2026)."); ttr = r
for c in ("I", "J"): wr[f"{c}{r}"].number_format = NF_P
r += 1
for name, rr in zip([t[0] for t in TREG], reg_rows):
    row(wr, r, "  % " + name, [f"={L(4+i)}{rr}/{L(4+i)}{ttr}" for i in range(5)], NF_P, F_TXT); r += 1
setc(wr, f"R{reg_rows[0]}", "Taiwan 36% em 2025 (21% em 2024) e 41% no 1H26: o swing para compute AI/OSATs taiwaneses. Coreia 25% em 2024 (memória/Samsung 12,5%) → 14% em 2025 → 20% no 1H26 (HBM).", F_NOTE)
setc(wr, f"R{reg_rows[1]}", "China 14% (2025) / 11% (1H26): abaixo dos ~19-20% da Advantest.", F_NOTE)
r += 1; hdr(wr, r, "Advantest — ship-to por região, trimestral (¥ bilhões) — Q1 FY24 (abr-jun 2024) → Q1 FY26 (abr-jun 2026)", c1="R"); r += 1
AQ = ["Q1 FY24", "Q2 FY24", "Q3 FY24", "Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26"]
yhdr(wr, r, AQ); setc(wr, f"R{r}", "⚠ Séries mapeadas às regiões por magnitude (Taiwan = maior ship-to; China ≈19% no Q1 FY26 por Q&A). Conferir com o gráfico do slide 7.", F_NOTE); r += 1
AREG = [("Taiwan", [41.5, 73.1, 78.8, 133.1, 162.1, 115.4, 103.2, 188.8, 178.6]), ("China", [36.0, 42.7, 51.8, 44.6, 39.0, 52.1, 65.4, 56.8, 69.4]), ("Coreia do Sul", [33.4, 45.0, 54.9, 23.7, 32.7, 56.1, 57.0, 34.5, 67.4]),
        ("Japão", [9.5, 7.3, 11.7, 9.7, 12.2, 16.7, 21.8, 22.1, 29.5]), ("Américas", [9.1, 12.4, 12.6, 13.0, 9.6, 11.3, 12.0, 11.6, 13.2]), ("Europa", [3.9, 5.4, 5.0, 5.7, 4.4, 6.1, 5.9, 6.7, 6.1]), ("Outros", [5.3, 4.6, 3.4, 2.5, 3.8, 5.2, 8.5, 7.6, 3.3])]
areg_rows = []
for name, vals in AREG:
    row(wr, r, name, vals, NF_N1, F_IN); areg_rows.append(r); r += 1
atot = r; row(wr, r, "Total (confere com a receita trimestral reportada)", [f"=SUM({L(4+i)}{areg_rows[0]}:{L(4+i)}{areg_rows[-1]})" for i in range(9)], NF_N1, F_TXT, bold=True, note="Reportado: 138,7 / 190,5 / 218,2 / 232,3 / 263,8 / 262,9 / 273,8 / 328,1 / 367,5."); r += 1
for name, rr in zip([a[0] for a in AREG], areg_rows):
    row(wr, r, "  % " + name, [f"={L(4+i)}{rr}/{L(4+i)}{atot}" for i in range(9)], NF_P, F_TXT); r += 1
setc(wr, f"R{areg_rows[0]}", "Taiwan 30% (Q1 FY24) → 49% (Q1 FY26): fabless norte-americanos via TSMC/OSATs — mesma migração vista na Teradyne (Taiwan 41% no 1H26).", F_NOTE)
setc(wr, f"R{areg_rows[2]}", "Coreia (memória: HBM/DRAM para Hynix/Samsung) volátil — 23,7 no Q4 FY24 vs 67,4 no Q1 FY26.", F_NOTE)
r += 1; hdr(wr, r, "Advantest — receita por localização do cliente, FY-Mar (¥ bilhões, tanshin)", c1="R"); r += 1
yhdr(wr, r, ["FY24", "FY25"]); r += 1
for name, vals in [("Japão", [15.8, 25.1]), ("Américas (EUA, Brasil etc.)", [47.1, 44.5]), ("Europa (Alemanha, Israel, Irlanda etc.)", [20.0, 23.1]), ("Ásia (Taiwan, China, Coreia, Malásia etc.)", [696.8, 1035.9]), ("Total", [779.7, 1128.6])]:
    row(wr, r, name, vals, NF_N1, F_IN, bold=(name == "Total")); r += 1
row(wr, r, "  % Ásia", [f"=D{r-2}/D{r-1}", f"=E{r-2}/E{r-1}"], NF_P, F_TXT, note="Tanshin FY2025 p.12: 97,8% das vendas a clientes no exterior (Japão 2,2%). Ship-to Japão 8% ≠ cliente japonês (fabs de clientes estrangeiros no Japão)."); r += 1
wr.freeze_panes = "D5"

# =====================================================================================================
# Sheet 4 — Clientes
# =====================================================================================================
wc = sheet(wb, "Clientes", "ATE | Maiores clientes e concentração — comentários com fonte", "Cada linha carrega a fonte e a data. 'Inferência' = identificação de mercado, não disclosure da companhia.",
           {"C": 12, "D": 30, "E": 34, "F": 16, "G": 12, "H": 52, "I": 70})
r = 5
for i, t in enumerate(["Empresa", "Cliente / conta", "Métrica", "Valor", "Período", "Fonte (documento, data)", "Leitura / comentário"]):
    setc(wc, f"{L(3+i)}{r}", t, F_TXTB, fill=FILL_H)
r += 1
CL = [
 ("Advantest", "NVIDIA International, Inc.", "% das vendas consolidadas", "20,2% (¥228,3 bi)", "FY25 (mar-26)", "Annual securities report FY2025 via @QQ_Timmy (2026-08-01) — 2ª mão; aritmética confere (228,3 / 1.128,6). Wiki ADVANTEST.md 'Current state'.", "Primeira vez que um cliente cruza o limiar de 10% (ano anterior '–'). A incumbência em teste de GPU é ~1/5 da receita — o entrante (TER, 2ª fonte qualificada, 1º pedido no 2T CY26) é risco de P&L, não só de narrativa."),
 ("Advantest", "Base de clientes", "Descrição", "Foundries, OSATs, IDMs, memory makers; ~98% no exterior", "FY25", "Tanshin FY2025 (2026-04-27); wiki ADVANTEST.md Snapshot.", "Ship-to concentrado em Taiwan (~49% no Q1 FY26) = fabless americanos via TSMC/OSATs; localização do cliente Ásia 92%."),
 ("Advantest", "Taiwan (TSMC / OSATs / fabless)", "Ship-to", "~49% da receita", "Q1 FY26 (abr-jun 26)", "Deck 1Q FY26 slide 7 (mapeamento por magnitude) + Q&A Q10 ('Taiwan remains the largest ship-to region').", "Predominantemente SoC; CoWoS device testing 'comes from Advantest' (StoneX/John Su 2025-08-20)."),
 ("Advantest", "China", "% das vendas", "≈19% (histórico ~20%); SoC 80-85% / memória ~15%", "Q1 FY26", "Q&A 1Q FY26 Q10 (2026-07-29); call 3Q FY25: 20-25%.", "Novas fabs chinesas = opção 2028-29; até lá ~20% ou menos. Risco regulatório/decoupling + concorrência doméstica (call 4Q FY25)."),
 ("Advantest", "Mercado SoC (GPU / ASIC / CPU)", "Share em SoC test", "66% em CY25; 'path to >70%'; share em HPC ainda maior", "CY25 → CY26", "Q&A 1Q FY26 Q4 (2026-07-29).", "TER contesta: 'SOC share… pretty flat, maybe a slight incremental gain for us' (call TER 2026-07-29). Uma das duas está errada — dado final de share ATE CY26 (~abr-27) decide."),
 ("Advantest", "Hyperscaler ASIC / TPU (AVGO / MediaTek), AMD GPU & CPU, ARM server CPU", "Posição competitiva", "'Dominant position in TPU testing'; 'dominant share of CPU testing outside of Intel'", "2026", "MS Asia sales desk (Amerian, 2026-08-14 / 07-27) — comentário de vendas, NÃO research; MS Research (Charlie Chan) CoWoS +82%/+64% 2026-27.", "Inferência de mercado, não disclosure. Advantest declinou separar GPU / ASIC / CPU no TAM (Q&A Q1). 'Agnostic winner' entre NVDA e ASICs é a tese do desk."),
 ("Advantest", "Amazon Trainium (via Alchip)", "Leitura de cadeia", "Ganho de share assumido com a troca MRVL → Alchip no design service (Trainium 4 a 2nm)", "2026-08", "MS Asia desk (2026-08-14) — comentário de vendas.", "Hipótese de cadeia; nada disclosed pela Advantest."),
 ("Advantest", "Memória (SK Hynix / Samsung / Micron — HBM e DRAM de alta performance)", "Share em memory test", "~54% CY25 implícito; 'may experience a decline this year' (NAND não incumbente)", "CY26", "Q&A 1Q FY26 Q4; TER concorda ('I agree with their commentary about memory', call 2026-07-29).", "Perda de share em memória é consensual entre as duas; 'Korean suppliers win HBM4 tester orders from SK Hynix' (DIGITIMES 2026-07-30). Mix memória FY26e: DRAM 85% / NVM 15%."),
 ("Advantest", "Novo cliente hyperscaler ASIC", "Novo programa", "Contribuição a partir de FY26", "FY26", "Jefferies / Techknowledge (2025-12-17), via wiki.", "Alavanca da franquia NVDA (interface tester-handler) para ganhar os ASICs."),
 ("Advantest", "Visibilidade de demanda", "Horizonte de forecast", "18 meses com clientes próximos (antes ~6 meses)", "2026-07", "Q&A 1Q FY26 Q8.", "Contraste com TER: lead times de 10-20 semanas 'usando a supply chain para ganhar share' (UBS fireside IR 2026-08-03)."),
 ("Teradyne", "5 maiores clientes diretos", "% da receita consolidada", "44% (2025) / 36% (2024) / 32% (2023) / 26% (2022) / 33% (2021)", "2021-2025", "10-K FY25 (2026-02-19), FY24, FY23 — 'Sales and Distribution'.", "Concentração subiu 18 pp em dois anos com o ramp de compute AI; 'vast majority of tester demand driven by ~2 customers' (call 3Q FY25)."),
 ("Teradyne", "Dois 'specifying customers' (Semi Test + Product Test) + um comprador direto (OSAT)", "% da receita", "12% e 10% (especificadores); 19% (comprador direto, incl. receita especificada pelos dois)", "2025", "10-K FY25.", "Padrão hyperscaler/fabless → OSAT: os especificadores decidem a plataforma, o OSAT compra. Nenhum nome divulgado em 2025."),
 ("Teradyne", "Samsung", "% da receita (direto + OSATs)", "12,5%", "2024", "10-K FY24 / FY25 (Semi Test + Wireless Test).", "Memória (DRAM/HBM) + mobile; explica Coreia 25% da receita em 2024."),
 ("Teradyne", "Um cliente (Semi Test + Wireless Test)", "% especificado", "~13%", "2024", "10-K FY25.", "Não nomeado; perfil mobile/SoC (Semi + Wireless)."),
 ("Teradyne", "Texas Instruments", "% da receita", "10%", "2023", "10-K FY24 / FY23.", "Analógico/industrial — o cliente âncora do ciclo pré-AI."),
 ("Teradyne", "Qualcomm", "% da receita (direto + indireto)", "~12,5%", "2022", "10-K FY23.", "Mobile SoC; outro cliente OEM (Semi + Wireless) ~11% em 2022."),
 ("Teradyne", "TSMC (direto) e um OEM (Semi + Wireless, incl. OSATs como TSMC)", "% da receita", "TSMC 12%; OEM 19%", "2021", "10-K FY23 (o OEM não é nomeado; o mercado entende como Apple — inferência).", "Pico do ciclo mobile/Apple: Taiwan 30% da receita em 2021."),
 ("Teradyne", "Hyperscaler #1 (custom silicon)", "Share de tester na conta", "~70% após ramp de dual-source; cada grande hyperscaler = 'hundreds of millions to ~$1bn' de TAM anual", "2026-09", "GS Communacopia — small group com o CEO (2026-09-09; compile 09-13). Fonte = management, sem rating.", "Os ~30% de 'fast follower' eram estação de passagem, não teto. Conta não nomeada (Google/TPU e Amazon são inferências de sell-side)."),
 ("Teradyne", "Hyperscaler #2", "Ramp", "TAM maior que #1; rampa em incrementos de 10/20/30 pontos; share de produção relevante em 2027", "2027", "UBS fireside IR (2026-08-03); GS Communacopia (2026-09-13).", "Slope mais plano, teto mais alto; SKU a SKU."),
 ("Teradyne", "Merchant compute (NVDA — inferência)", "Qualificação", "Qualificada como 2º vendor; 1º pedido embarcado no 2T CY26; caminho de 3-5 anos até ~30% da porção compute", "2026-27+", "Call 2Q CY26 (2026-07-29); GS Communacopia (2026-09-13). Cliente NÃO nomeado.", "É exatamente a incumbência que responde por ~20% da receita da Advantest (NVIDIA 20,2%). GS (07-05): 'durability of Advantest's GPU-test share' = debate central."),
 ("Teradyne", "Networking / VIP (dois grandes clientes)", "Share", "'Very, very high share' nos dois; sole-source em um; TAM ~$1 bi em 2026 (vs '$800m+ by 2028' anterior)", "2026", "UBS fireside IR (2026-08-03).", "Trocaria 'metade do share em networking por metade do share na outra parte da conta' — a qualificação recíproca em compute é o objetivo."),
 ("Teradyne", "Memória (DRAM/HBM + NAND)", "Receita / book-to-bill", "Recorde $212 mi no 2T CY26; book-to-bill 2,0; 3º trimestre seguido >$200 mi", "2Q CY26", "Call 2Q CY26; UBS fireside IR (2026-08-03).", "Ganho de share em memória é o que a Advantest concede; TAM de memória 2026 '>40% maior que 2025'."),
 ("Teradyne", "AI como % da receita", "Mix", "~50% (3Q FY25) → ~60% (4Q FY25) → ~70% (1Q FY26); compute = 70% do SOC product revenue no 2T CY26 (+~600% y/y)", "2025-26", "Calls 1Q FY26 (2026-04-29) e 2Q CY26 (2026-07-29).", "Swing de mobile para AI em seis trimestres; Semi Test 79% da receita em 2025."),
 ("Teradyne", "Intel (merchant test)", "Opção", "Volta ao ATE comercial em 2027 em pequena escala; relevante em 2028+", "2027-28", "GS Communacopia small group (2026-09-13); UBS fireside (08-03): 'at least a year out'.", "Tese da companhia, não pedido."),
 ("Teradyne", "Robotics — cliente 'marquee'", "Crescimento", "3x 2025→2026 e 3x esperado 2026→2027 (UMA conta, não o segmento)", "2026-27", "GS Communacopia small group (2026-09-13).", "Robotics ainda abaixo do breakeven (~$365 mi/ano)."),
 ("Ambas", "TSMC / CoWoS (canal)", "Posicionamento", "CoWoS device testing 'comes from Advantest'; TER 'best for mobile' / InFO (Apple); 2ª fonte TER para teste AI na TSMC 'very difficult'", "2025-08", "StoneX / John Su — TSMC channel (2025-08-20).", "Leitura de canal de 2025; a qualificação de TER em merchant GPU (1º pedido 2T CY26) moveu o debate para 2027."),
 ("Ambas", "TAM e share — visões cruzadas", "Comentário do concorrente", "TER sobre o TAM da Advantest: 'right zip code'; concorda em memória, contesta SoC. UBS: share total da TER ~37% em 2026, 'basically flat'", "2026-07-29", "Call TER 2Q CY26 (Bloomberg transcript).", "No pool comum (ex burn-in, ex-IST) os dois modelos oficiais somam 94% / 96% / 97% do TAM em CY26-28 — resíduo para outros ~3%: os dois shares não podem estar ambos certos com o TAM mid-point."),
 ("Ambas", "Lead times como arma de share", "Operacional", "Advantest: visibilidade 12-18 meses; TER: 10-20 semanas, 'using our supply chain to gain share'", "2026-08", "UBS fireside TER IR (2026-08-03); Advantest IR call (2026-08-02) via TER.", "Em escassez, disponibilidade — não roadmap — é o mecanismo de share."),
]
for rowv in CL:
    for i, v in enumerate(rowv):
        setc(wc, f"{L(3+i)}{r}", v, F_TXT, wrap=True)
    wc.row_dimensions[r].height = 62
    r += 1
wc.freeze_panes = "D6"

# =====================================================================================================
# Sheet 5 — Fontes e notas
# =====================================================================================================
wf = sheet(wb, "Fontes e notas", "Fontes e bases", "", {"C": 160})
r = 5
for t in [
 "Modelos oficiais: P:\\Felipe Monteiro\\US Equities\\Modelos oficiais\\Template DCF ADVANTEST.xlsx e Template DCF TER.xlsx (2026-09-18). Os valores desta planilha são colados (não linkados) — refazer a colagem se os modelos mudarem (script build_ate_consolidado.py em _wiki/_data/research/ATE_official_models_2026-09-18/).",
 "Advantest: tanshin FY2025 (2026-04-27) e 1Q FY2026 (2026-07-29); deck e Q&A de 29-jul-2026 (ADVANTEST/transcripts); BBG bdh trimestral (calendarização CY) e PG_REVENUE (segmentos FY18-FY25); annual securities report FY2025 via @QQ_Timmy (NVIDIA 20,2%).",
 "Teradyne: 10-K FY23 / FY24 / FY25, 10-Q 2Q FY26 (TER/); calls 1Q FY26 (2026-04-29) e 2Q CY26 (2026-07-29); UBS fireside com IR (2026-08-03); GS Communacopia compiles (2026-09-13/14); BBG PG_REVENUE (segmentos 2019-2025); iniciação Capstone 2026-09-16.",
 "Consenso e preços: Bloomberg bdp 2026-09-18 (PX_LAST, CUR_MKT_CAP, CURR_ENTP_VAL, BEST_*). Advantest 1CY/2CY/3CY BEST_SALES; EPS BBG não calendarizado.",
 "FX: USDJPY médias mensais BBG — CY 141,4 / 151,9 / 150,0 (2023-25); FY-Mar 111,1 / 108,4 / 106,2 / 112,9 / 135,7 / 145,5 / 152,6 / 151,1 (FY18-FY25). Projeções ao FX do modelo (157 em CY26, 150 depois).",
 "Bases que não se misturam: (1) TAM Advantest (SoC + memória, ex burn-in) vs base TER (7-9% do WFE, incl. burn-in) vs 'teste ÷ receita de semis' (~1%, UBS). (2) FY-Mar da Advantest vs CY da Teradyne (o quadro histórico do duopólio desalinha um trimestre). (3) Segmentações: Advantest mudou para 2 segmentos em FY24 (SLT/interfaces → 'Other systems'); Teradyne ressegmentou em 2025 (IST → Semi Test; Product Test = System + Wireless ex-IST).",
 "Regiões da Advantest (slide 7): as séries do PDF foram atribuídas às regiões por magnitude — Taiwan é a maior (Q&A) e China ≈19% (Q&A) confirmam duas das sete; conferir visualmente antes de citar Coreia/Japão.",
 "Nenhum rating para a Advantest nesta planilha; Teradyne = NEUTRAL, PT $400 (iniciação 2026-09-16, reproduzida pelo modelo oficial).",
]:
    setc(wf, f"C{r}", t, F_TXT, wrap=True); wf.row_dimensions[r].height = 45; r += 1

wb.save(OUT); print("saved", OUT)
