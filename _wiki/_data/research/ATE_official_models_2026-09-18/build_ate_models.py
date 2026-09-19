# -*- coding: utf-8 -*-
"""Build the two official ATE models in the 'Template DCF <TICKER>.xlsx' family (AMD/AVGO convention, Sep-2026):
   - Template DCF ADVANTEST.xlsx (JPY mm, calendar-year columns CY2023-CY2045, FY-Mar bridge block)
   - Template DCF TER.xlsx (US$ mm, calendar = fiscal)
Both share one top-down ATE-TAM block (WFE x test-intensity ratio, ex burn-in on Advantest's TAM basis) so the two
companies' shares are measured against the same pool. Sheets: 'Capa DCF - Base' + 'Premissas e fontes' (same names,
colours, fonts, number formats and freeze panes as Template DCF AMD/AVGO). openpyxl writes formulas only; Excel COM
recalculates (see recalc_verify.py). Rule: no TEXT cell may start with '='.
"""
import datetime as dt, os, json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2023, 2046))                 # 23 columns
COLS = [get_column_letter(4 + i) for i in range(len(YEARS))]   # D..Z
BASE = {2023, 2024, 2025}
P = "'Premissas e fontes'!"

# ---------------------------------------------------------------- styles (from Template DCF AMD.xlsx)
F_TITLE = Font(name="Arial", size=16, bold=True, color="FF203864")
F_TXT = Font(name="Arial", size=10, color="FF202020")
F_TXTB = Font(name="Arial", size=10, bold=True, color="FF202020")
F_NOTE = Font(name="Arial", size=9, color="FF666666")
F_INPUT = Font(name="Arial", size=10, color="FF0000FF")          # blue = hard input / assumption
F_LINK = Font(name="Arial", size=10, color="FF008000")           # green = internal source (link to Premissas)
F_RES = Font(name="Arial", size=12, bold=True, color="FFFFFFFF")
FILL_HDR = PatternFill("solid", fgColor="FFDCE6F1")
FILL_ASSUM = PatternFill("solid", fgColor="FFFFF2CC")
FILL_RES = PatternFill("solid", fgColor="FF203864")
NF_NUM = '#,##0;\\(#,##0\\);"-"'
NF_NUM1 = '#,##0.0;\\(#,##0.0\\);"-"'
NF_NUM2 = '0.00;\\(0.00\\);"-"'
NF_PCT = '0.0%;\\(0.0%\\);"-"'
NF_CHK = '0.00;\\(0.00\\);0.00'
NF_DATE = 'dd\\-mmm\\-yyyy'
NF_DATE_S = 'dd\\-mmm\\-yy'


def setc(ws, addr, value, font=F_TXT, nf=None, fill=None, align=None):
    c = ws[addr]
    if isinstance(value, str) and not value.startswith("=") and value[:1] == "=":
        raise ValueError("text starting with '=' " + value)
    c.value = value
    c.font = font
    if nf: c.number_format = nf
    if fill: c.fill = fill
    if align: c.alignment = Alignment(horizontal=align)
    return c


def label(ws, r, text, bold=False, fill=None, col="C"):
    setc(ws, f"{col}{r}", text, F_TXTB if bold else F_TXT, fill=fill)


def header_row(ws, r, text):
    setc(ws, f"C{r}", text, F_TXTB, fill=FILL_HDR)
    for c in COLS:
        ws[f"{c}{r}"].fill = FILL_HDR


def note(ws, r, text, col="C"):
    if text.startswith("="):
        raise ValueError("note starts with '='")
    setc(ws, f"{col}{r}", text, F_NOTE, align="left")


def year_header(ws, r, tags=None):
    for i, y in enumerate(YEARS):
        t = f"CY{str(y)[2:]}{'B' if y in BASE else 'E'}" if tags is None else tags[i]
        setc(ws, f"{COLS[i]}{r}", t, F_TXTB, fill=FILL_HDR, align="center")


def row_formula(ws, r, fn, nf=NF_NUM, font=F_TXT, start=0, end=None, fill=None, bold=False):
    """fn(i, col, prevcol) -> formula string or number or None"""
    end = len(COLS) if end is None else end
    for i in range(start, end):
        c = COLS[i]; pc = COLS[i - 1] if i > 0 else None
        v = fn(i, c, pc)
        if v is None: continue
        f = font
        if bold: f = Font(name="Arial", size=10, bold=True, color=font.color.rgb if font.color else "FF202020")
        setc(ws, f"{c}{r}", v, f, nf=nf, fill=fill, align="right")


def setup_sheet(ws, title, units, legend):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2.25
    ws.column_dimensions["B"].width = 2.25
    ws.column_dimensions["C"].width = 47
    for c in COLS: ws.column_dimensions[c].width = 12.5
    for r in (1, 2, 5, 7): ws.row_dimensions[r].height = 18
    setc(ws, "C2", title, F_TITLE, align="left")
    setc(ws, "C3", units, F_TXT, align="left")
    setc(ws, "C4", legend, F_NOTE, align="left")
    ws.freeze_panes = "D6"


# =====================================================================================================
# Premissas e fontes — generic writer
# =====================================================================================================
class Prem:
    """Registers rows on 'Premissas e fontes'. Two kinds: (a) reference table rows (years 2023..2028 in D..I, source in L),
    (b) per-year assumption rows (CY23B..CY45E in D..Z, note in AB)."""
    def __init__(self, ws, ticker, unit_line):
        self.ws = ws; self.rows = {}
        ws.sheet_view.showGridLines = False
        ws.column_dimensions["A"].width = 2.25; ws.column_dimensions["B"].width = 2.25
        ws.column_dimensions["C"].width = 47
        for c in COLS: ws.column_dimensions[c].width = 12.5
        ws.column_dimensions["AB"].width = 55; ws.column_dimensions["AC"].width = 12.5
        ws.freeze_panes = "D6"
        setc(ws, "C2", f"{ticker} | Premissas e fontes", F_TITLE, align="left")
        setc(ws, "C3", unit_line, F_TXT, align="left")
        for i, y in enumerate(range(2023, 2029)):
            setc(ws, f"{COLS[i]}5", y, F_TXTB, nf="0", fill=FILL_HDR, align="center")
        setc(ws, "L6", "Arquivo, aba e células de origem. CY = ano-calendário.", F_NOTE, align="left")
        self.r = 7

    def ref(self, key, text, vals, src, nf=NF_NUM, formula=False, font=F_INPUT):
        """vals: list up to 6 (2023..2028) — None skips."""
        r = self.r; self.rows[key] = r
        label(self.ws, r, text)
        for i, v in enumerate(vals):
            if v is None: continue
            setc(self.ws, f"{COLS[i]}{r}", v, F_TXT if (isinstance(v, str) and v.startswith("=")) and not formula else font, nf=nf, align="right")
        if src: setc(self.ws, f"L{r}", src, F_NOTE, align="left")
        self.r += 1
        return r

    def single(self, key, text, val, src, nf=NF_NUM, fill=FILL_ASSUM, font=F_INPUT):
        r = self.r; self.rows[key] = r
        label(self.ws, r, text)
        setc(self.ws, f"D{r}", val, font, nf=nf, fill=fill)
        if src: setc(self.ws, f"F{r}", src, F_NOTE, align="left")
        self.r += 1
        return r

    def section(self, text):
        self.r += 1
        setc(self.ws, f"C{self.r}", text, F_TXTB, fill=FILL_HDR)
        self.r += 1

    def year_hdr(self):
        year_header(self.ws, self.r); self.r += 1

    def series(self, key, text, values, note_txt, nf=NF_PCT, hard_font=F_INPUT, hard_fill=FILL_ASSUM):
        """values: dict year -> number | formula string | None."""
        r = self.r; self.rows[key] = r
        label(self.ws, r, text)
        for i, y in enumerate(YEARS):
            v = values.get(y)
            if v is None: continue
            if isinstance(v, str) and v.startswith("="):
                setc(self.ws, f"{COLS[i]}{r}", v, F_TXT, nf=nf, align="right")
            else:
                setc(self.ws, f"{COLS[i]}{r}", v, hard_font, nf=nf, fill=hard_fill, align="right")
        if note_txt: setc(self.ws, f"AB{r}", note_txt, F_NOTE, align="left")
        self.r += 1
        return r

    def text(self, t):
        note(self.ws, self.r, t); self.r += 1


def fill_years(d, start_year, value):
    for y in YEARS:
        if y >= start_year and y not in d: d[y] = value
    return d


def ramp(d, pts):
    """pts: list of (year, value); linear between points, flat after last."""
    pts = sorted(pts)
    for y in YEARS:
        if y in d: continue
        if y <= pts[0][0]: continue
        for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
            if y0 < y <= y1:
                d[y] = v0 + (v1 - v0) * (y - y0) / (y1 - y0); break
        else:
            if y > pts[-1][0]: d[y] = pts[-1][1]
    return d


# =====================================================================================================
# Shared market inputs (US$ bn) — canonical for BOTH models
# =====================================================================================================
WFE = {2023: 95.76, 2024: 100.34, 2025: 116.0, 2026: 158.0, 2027: 205.0, 2028: 240.0}
WFE_G = ramp({}, [(2028, 0.06), (2029, 0.06), (2031, 0.04), (2034, 0.03)])          # CY29+ growth inputs
TAM_REF = {2023: 4.9, 2024: 6.0, 2025: 9.0, 2026: 13.75}      # Advantest deck 07-29 (CY24-26 mid); CY23 = Capstone Industry Assumptions (old basis)
SOC_REF = {2024: 4.1, 2025: 6.9, 2026: 11.0}
RATIO_IN = ramp({2027: 0.080, 2028: 0.083}, [(2028, 0.083), (2030, 0.083), (2034, 0.080)])   # CY27 lag dip (TER mgmt), CY28 recovers toward the >=$20bn path
SOC_MIX = {2023: 0.75}; SOC_MIX = fill_years(ramp(SOC_MIX | {2027: 0.80, 2028: 0.79}, [(2028, 0.79), (2032, 0.78)]), 2029, 0.78)

FX = {2023: 141.43, 2024: 151.92, 2025: 149.96, 2026: 157.0}; fill_years(FX, 2027, 150.0)

# ADVANTEST quarterly history (BBG bdh, periodicity Q, pulled 2026-09-18) — JPY mm; calendar sums below
ADV_Q = {  # (sales, gp, oi, ni, eps, capex, da, dil_sh)
    "2023Q1": (147392, 78698, 38547, 30594, 41.575, 6223, 6134, 739.02), "2023Q2": (101251, 50951, 14269, 9202, 12.4875, 5685, 6023, 739.74),
    "2023Q3": (116260, 58058, 21000, 16736, 22.69, 4272, 6469, 739.88), "2023Q4": (133233, 67387, 26830, 21205, 28.74, 4122, 6640, 739.94),
    "2024Q1": (135763, 69634, 19529, 15147, 20.53, 5513, 6972, 740.42), "2024Q2": (138725, 76906, 31325, 23873, 32.35, 3778, 7102, 740.25),
    "2024Q3": (190481, 110091, 63534, 45470, 61.557, 3364, 7156, 740.86), "2024Q4": (218152, 118854, 69267, 51867, 70.30, 4849, 6721, 740.00),
    "2025Q1": (232349, 139234, 64035, 39967, 54.465, 5423, 6096, 736.05), "2025Q2": (263776, 171638, 123952, 90180, 123.14, 5649, 6112, 734.36),
    "2025Q3": (262957, 163641, 108483, 79633, 109.034, 12654, 6250, 732.56), "2025Q4": (273804, 169708, 113571, 78713, 108.376, 6431, 6435, 728.77),
    "2026Q1": (328073, 221120, 153114, 126827, 174.805, 8278, 6815, 728.16), "2026Q2": (367473, 255553, 189990, 174780, 241.27, 9852, 7151, 728.58),
}


def adv_cy(year):
    qs = [ADV_Q[f"{year}Q{q}"] for q in (1, 2, 3, 4)]
    s = [sum(q[k] for q in qs) for k in range(7)]
    s.append(sum(q[7] for q in qs) / 4)
    return dict(sales=s[0], gp=s[1], oi=s[2], ni=s[3], eps=s[4], capex=s[5], da=s[6], sh=s[7])


ADV_CY = {y: adv_cy(y) for y in (2023, 2024, 2025)}

# =====================================================================================================
# ADVANTEST
# =====================================================================================================
def build_advantest(path, ter_us):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Capa DCF - Base"
    wp = wb.create_sheet("Premissas e fontes")
    pr = Prem(wp, "ADVANTEST", "Dados extraídos das fontes indicadas. ¥ milhões salvo indicação; TAM/WFE em US$ bilhões.")

    # ---- reference table (2023..2028 in D..I)
    pr.section("Histórico calendarizado (CY) a partir dos trimestres BBG + referência de consenso")
    cy = ADV_CY
    pr.ref("rev_ref", "Receita total CY (¥ mi) | histórico BBG / consenso BBG CY", [cy[2023]["sales"], cy[2024]["sales"], cy[2025]["sales"], 1525591, 2140572, 2639526],
           "CY23-25: bdh SALES_REV_TURN trimestral somado (6857 JP, 2026-09-18). CY26-28: bdp BEST_SALES 1CY/2CY/3CY (2026-09-18). ⚠ o 1CY BBG (1.525,6) é inferior à soma dos trimestres reportados + kFQ (~1.590).")
    pr.ref("gp_ref", "Lucro bruto CY (¥ mi)", [cy[2023]["gp"], cy[2024]["gp"], cy[2025]["gp"]], "bdh GROSS_PROFIT trimestral somado.")
    pr.ref("oi_ref", "Resultado operacional CY (¥ mi) | histórico / consenso EBIT", [cy[2023]["oi"], cy[2024]["oi"], cy[2025]["oi"], 730365, 1094998, 1379757], "bdh IS_OPER_INC; CY26-28 bdp BEST_EBIT 1CY/2CY/3CY.")
    pr.ref("ni_ref", "Lucro líquido CY (¥ mi)", [cy[2023]["ni"], cy[2024]["ni"], cy[2025]["ni"]], "bdh NET_INCOME trimestral somado. Consenso de NI/EPS BBG NÃO é calendarizado (1CY = 1FY) — não usar como CY.")
    pr.ref("eps_ref", "EPS básico CY (¥) | soma dos trimestres", [cy[2023]["eps"], cy[2024]["eps"], cy[2025]["eps"]], "bdh IS_EPS trimestral somado.", nf=NF_NUM2)
    pr.ref("da_ref", "Depreciação e amortização CY (¥ mi)", [cy[2023]["da"], cy[2024]["da"], cy[2025]["da"]], "bdh CF_DEPR_AMORT trimestral somado.")
    pr.ref("capex_ref", "Capex CY (¥ mi)", [cy[2023]["capex"], cy[2024]["capex"], cy[2025]["capex"]], "bdh CF_CAP_EXPEND_PRPTY_ADD trimestral somado (sinal invertido).")
    pr.ref("sh_ref", "Ações diluídas CY (mi, média)", [cy[2023]["sh"], cy[2024]["sh"], cy[2025]["sh"]], "bdh IS_SH_FOR_DILUTED_EPS média dos 4 trimestres.", nf=NF_NUM1)
    pr.ref("ts_mix", "Test Systems / receita (mix FY-Mar aplicado ao CY)", [0.876, 0.876, 0.896], "FY24 682,8/779,7 = 87,6%; FY25 1.019,4/1.128,6 = 90,3%; CY25 = 0,25×FY24 + 0,75×FY25; CY23 usa FY24 (mix FY23 não disponível na mesma segmentação). Base do cenário, não reportado.", nf=NF_PCT)
    pr.ref("soc_in_ts", "SoC / Test Systems (mix FY aplicado ao CY)", [0.645, 0.645, 0.726], "Deck 1Q FY26 (2026-07-29): FY24 SoC 440,4 / TS 682,8; FY25 767,4 / 1.019,4; CY25 blend 0,25/0,75.", nf=NF_PCT)
    pr.ref("mem_in_ts", "Memória / Test Systems (mix FY aplicado ao CY)", [0.231, 0.231, 0.184], "Deck 1Q FY26: FY24 157,7; FY25 171,5.", nf=NF_PCT)
    pr.ref("oth_in_ts", "Outros sistemas / Test Systems (mix FY aplicado ao CY)", [0.124, 0.124, 0.090], "Deck 1Q FY26: FY24 84,7; FY25 80,5.", nf=NF_PCT)
    pr.ref("ar", "Contas a receber (¥ mi) | 31-mar-25 / 31-mar-26 / 30-jun-26", [113031, 228731, 178497], "Tanshin FY2025 (2026-04-27) p.6 e 1Q FY2026 (2026-07-29) p.5 — trade and other receivables.")
    pr.ref("inv", "Estoques (¥ mi) | 31-mar-25 / 31-mar-26 / 30-jun-26", [209707, 231718, 273654], "Tanshin FY2025 / 1Q FY2026 — inventories.")
    pr.ref("ap", "Contas a pagar (¥ mi) | 31-mar-25 / 31-mar-26 / 30-jun-26", [107093, 142061, 154357], "Tanshin FY2025 / 1Q FY2026 — trade and other payables.")
    pr.ref("sbc_fy", "Stock-based compensation FY (¥ mi) | FY24 / FY25", [2893, 4450], "Tanshin FY2025 cash-flow statement p.10.")
    pr.ref("tax_fy", "Alíquota efetiva FY | FY24 / FY25", [0.283, 0.274], "Tanshin FY2025 p.8: impostos 63.597/224.774 e 141.367/516.720.", nf=NF_PCT)

    pr.section("Guidance FY2026 (abr-2026 → mar-2027) — revisão de 29-jul-2026 (deck + tanshin 1Q FY26)")
    G = [("g_sales", "Receita FY26e (¥ mi)", 1714000), ("g_oi", "Resultado operacional FY26e (¥ mi)", 846000), ("g_pbt", "LAIR FY26e (¥ mi)", 891000),
         ("g_ni", "Lucro líquido FY26e (¥ mi)", 660000), ("g_eps", "EPS básico FY26e (¥)", 911.64), ("g_soc", "SoC test systems FY26e (¥ mi)", 1243500),
         ("g_mem", "Memory test systems FY26e (¥ mi)", 227000), ("g_oth", "Outros sistemas FY26e (¥ mi)", 104500), ("g_so", "Services & Others FY26e (¥ mi)", 139000),
         ("g_rd", "P&D FY26e (¥ mi)", 110000), ("g_capex", "Capex FY26e (¥ mi)", 50000), ("g_da", "D&A FY26e (¥ mi)", 31000), ("g_fx", "FX assumido FY26e (¥/US$)", 152)]
    for k, t, v in G:
        pr.single(k, t, v, "Advantest, 1Q FY2026 results (2026-07-29): guidance revisado (abril: 1.420.000 / 627.500 / 641,61). 1H 802,0 + 2H 912,0.", nf=NF_NUM2 if k in ("g_eps",) else NF_NUM, fill=None)
    pr.single("q1cy26_sales", "Trimestre jan-mar 2026 (Q4 FY25) — receita (¥ mi)", 328073, "Tanshin 4Q FY2025; usado na ponte FY↔CY.", fill=None)
    pr.single("q1cy26_oi", "Trimestre jan-mar 2026 (Q4 FY25) — resultado operacional (¥ mi)", 153114, "Idem.", fill=None)
    pr.single("q1cy26_ni", "Trimestre jan-mar 2026 (Q4 FY25) — lucro líquido (¥ mi)", 126827, "Idem.", fill=None)

    pr.section("TAM de testers — referência Advantest (deck 1Q FY26, 29-jul-2026; ex burn-in) e consenso FY (BBG)")
    pr.ref("tam_ref", "TAM ATE total (US$ bi) | CY23 base Capstone / CY24-25 Advantest / CY26e ponto médio", [TAM_REF[2023], TAM_REF[2024], TAM_REF[2025], TAM_REF[2026]],
           "CY24 6,0 / CY25 9,0 / CY26e 13,0-14,5 (mid 13,75; abril 10,9-12,2) — deck Advantest 2026-07-29. CY23 4,9 = ASML_Peers_SemiCap_Felipe.xlsx | Industry Assumptions!K26 (base antiga, informativo).", nf=NF_NUM2)
    pr.ref("soc_ref", "TAM SoC (US$ bi) | referência Advantest", [None, SOC_REF[2024], SOC_REF[2025], SOC_REF[2026]], "Deck 2026-07-29: CY24 4,1 / CY25 6,9 / CY26e 10,5-11,5 (mid 11,0). Memória = 1,9 / 2,1 / 2,5-3,0.", nf=NF_NUM2)
    pr.ref("cons_fy_sales", "Consenso BBG FY-Mar (¥ mi) | FY26 (mar-27) / FY27 / FY28", [None, None, None, 1748675, 2229626, 2630998], "bdp BEST_SALES 1FY/2FY/3FY, 6857 JP, 2026-09-18 (colunas 2026-28 = FY26-28, ano de INÍCIO).")
    pr.ref("cons_fy_oi", "Consenso BBG FY-Mar — EBIT (¥ mi)", [None, None, None, 881712, 1151220, 1372140], "bdp BEST_EBIT 1FY/2FY/3FY.")
    pr.ref("cons_fy_ni", "Consenso BBG FY-Mar — lucro líquido (¥ mi)", [None, None, None, 673534, 862962, 1026083], "bdp BEST_NET_INCOME 1FY/2FY/3FY.")
    pr.ref("cons_fy_eps", "Consenso BBG FY-Mar — EPS (¥)", [None, None, None, 927.49, 1186.43, 1422.02], "bdp BEST_EPS 1FY/2FY/3FY. 26 analistas, rating 4,73, PT médio ¥43.178.", nf=NF_NUM2)
    pr.ref("ter_us", "Teradyne Semi Test ex-IST (US$ mi) | modelo oficial TER — para o check de soma de shares", ter_us,
           "Template DCF TER.xlsx | Capa DCF - Base linha 19 menos IST (CY25 129,2; CY26-28 230/245/290 da iniciação; CY23-24 sem IST na segmentação antiga). Valores colados — atualizar se o modelo TER mudar.", nf=NF_NUM)

    pr.section("Valuation e balanço")
    pr.single("val_date", "Data de valuation", dt.datetime(2026, 8, 27), "Template DCF NVDA.xlsx | Audit & Checks!D5. Mantida a data para comparabilidade com AMD/AVGO.", nf=NF_DATE)
    pr.single("wacc", "WACC", 0.10, "Hipótese: 10% do template aplicado como WACC no FCFF (em ¥ — conservador para um emissor japonês; não é estimativa de mercado).", nf=NF_PCT)
    pr.single("g", "Crescimento terminal", 0.02, "Template DCF NVDA.xlsx | Capa DCF - Base!D91.", nf=NF_PCT)
    pr.single("roic", "ROIC incremental terminal", 0.20, "Hipótese do template: reinvestimento terminal = g / ROIC.", nf=NF_PCT)
    pr.single("shares", "Ações diluídas | referência 2Q CY26 (mi)", 728.58, "bdh IS_SH_FOR_DILUTED_EPS 30-jun-2026 (728,58); em circulação 723,97 mi (732,0 emitidas − 8,03 tesouraria, tanshin 1Q FY26). CB ¥100 bi (zero cupom, 2031) não convertido no modelo.", nf=NF_NUM1, fill=None)
    pr.single("cash", "Caixa e equivalentes (¥ mi)", 413124, "Tanshin 1Q FY2026 p.5, 30-jun-2026.", fill=None)
    pr.single("invsec", "Aplicações e títulos (investment securities, ¥ mi)", 357737, "Tanshin 1Q FY2026 p.5 — inclui títulos de dívida comprados no 1Q (¥87,8 bi) e participações estratégicas a valor justo. Tratado como ativo não operacional; ajuste se preferir excluir as participações.", fill=None)
    pr.single("debt", "Dívida financeira bruta (¥ mi) | CB valor de face", 100000, "Zero Coupon Convertible Bonds due 2031, emitidos 20-abr-2026 (¥100 bi; passivo contábil ¥88,9 bi em 30-jun-26). Sem empréstimos bancários.", fill=None)
    pr.single("bs_date", "Data-base do balanço no modelo", dt.datetime(2026, 6, 30), "Anterior à data de valuation; atualização manual disponível.", nf=NF_DATE, fill=None)
    pr.single("px", "Preço de referência (¥, informativo)", 32050, "BBG PX_LAST 6857 JP, 2026-09-18. Não entra no valuation.", fill=None)
    pr.single("pt_cons", "PT médio consenso (¥, informativo)", 43178, "BBG BEST_TARGET_PRICE, 26 analistas (23 buy / 3 hold / 0 sell), 2026-09-18.", fill=None)

    # ---- per-year assumptions
    pr.section("Premissas de mercado e operação (CY)")
    pr.year_hdr()
    wfe_vals = {y: WFE[y] for y in WFE}
    pr.series("wfe", "WFE global (US$ bi)", wfe_vals, "CY23-24 SEMI/VLSI via ASML_Peers_SemiCap_Felipe.xlsx | Industry Assumptions!K10:L10; CY25 UBS actual 116 (Implied WFE sheet); CY26-28 158/205/240 = base da iniciação TER (2026-09-16; wiki canônico CY26 $140-160 bi, CY27 house $180-215, CY28 house até $260).", nf=NF_NUM1)
    pr.series("wfe_g", "Crescimento WFE (CY29+)", {y: v for y, v in WFE_G.items() if y >= 2029}, "Hipótese pós-CY28: +6% CY29-30, convergindo a +3% a partir de CY34. Editável.")
    ratio_vals = {y: f"={COLS[YEARS.index(y)]}{pr.rows['tam_ref']}/{COLS[YEARS.index(y)]}{pr.rows['wfe']}" for y in (2023, 2024, 2025, 2026)}
    ratio_vals.update({y: RATIO_IN[y] for y in YEARS if y >= 2027})
    pr.series("ratio", "ATE / WFE (intensidade de teste, base Advantest ex burn-in)", ratio_vals, "CY23-26 calibrado ao TAM de referência (fórmula). CY27 8,0% = queda do lag WFE→wafer (TER mgmt 07-29: 'could revert to 6-7%' na base própria); CY28 8,3% (TER mgmt: TAM ≥$20 bi com WFE ~$250 bi); fade a 8,0% até CY34. Base ≠ 'test ÷ receita de semis' (~1%, UBS).")
    soc_vals = {2023: SOC_MIX[2023], 2024: f"=E{pr.rows['soc_ref']}/E{pr.rows['tam_ref']}", 2025: f"=F{pr.rows['soc_ref']}/F{pr.rows['tam_ref']}", 2026: f"=G{pr.rows['soc_ref']}/G{pr.rows['tam_ref']}"}
    soc_vals.update({y: SOC_MIX[y] for y in YEARS if y >= 2027})
    pr.series("soc_mix", "SoC / TAM ATE", soc_vals, "CY24-26 = referência Advantest (fórmula); CY27+ hipótese 80% → 78% (memória cresce com novas fabs, mgmt 07-29).")
    adv_soc = fill_years(ramp({2026: 0.68, 2027: 0.70, 2028: 0.70}, [(2028, 0.70), (2031, 0.68)]), 2032, 0.68)
    pr.series("adv_soc", "Advantest | share em SoC test", {y: adv_soc[y] for y in YEARS if y >= 2026}, "Mgmt 07-29: 66% em CY25, 'path to >70%'; CY26 68%, CY27-28 70%, fade a 68% (TER qualificando socket a socket — Debate). CY23-25 implícito na capa.")
    adv_mem = fill_years({2026: 0.50, 2027: 0.48}, 2028, 0.48)
    pr.series("adv_mem", "Advantest | share em memory test", {y: adv_mem[y] for y in YEARS if y >= 2026}, "Mgmt 07-29: share de memória 'may decline this year' (NAND não incumbente); TER concorda. 50% → 48%. CY23-25 implícito na capa.")
    pr.series("fx", "FX ¥/US$ (média do ano)", FX, "CY23-25 média mensal BBG USDJPY (141,4/151,9/150,0); CY26 157 (YTD 158,1; guidance 2H ¥150); CY27+ 150 = premissa da companhia.", nf=NF_NUM1)
    oth = fill_years({2026: 0.075, 2027: 0.070}, 2028, 0.070)
    pr.series("oth_ratio", "Outros sistemas / (SoC + memória)", {y: oth[y] for y in YEARS if y >= 2026}, "FY24 14,2%; FY25 8,6%; FY26e 7,1% (deck 07-29). Handlers/probers crescem abaixo dos testers.")
    so = fill_years({2026: 0.090, 2027: 0.085}, 2028, 0.085)
    pr.series("so_ratio", "Services & Others / Test Systems", {y: so[y] for y in YEARS if y >= 2026}, "FY24 14,2%; FY25 10,7%; FY26e 8,8% (deck 07-29). Base instalada cresce com atraso.")
    gm_hist = {y: f"={COLS[YEARS.index(y)]}{pr.rows['gp_ref']}/{COLS[YEARS.index(y)]}{pr.rows['rev_ref']}" for y in (2023, 2024, 2025)}
    gm = fill_years(ramp({2026: 0.680, 2027: 0.665, 2028: 0.655}, [(2028, 0.655), (2031, 0.630)]), 2032, 0.630)
    pr.series("gm", "Margem bruta", gm_hist | {y: gm[y] for y in YEARS if y >= 2026}, "CY23-25 reportado (BBG). CY26 68% (1H CY26 68,5%; guidance implica 2H menor — custo de DRAM nos testers, Q&A Q9); fade a 63% até CY31 (BOM, mix de memória, pass-through parcial).")
    opex_hist = {y: f"=({COLS[YEARS.index(y)]}{pr.rows['gp_ref']}-{COLS[YEARS.index(y)]}{pr.rows['oi_ref']})/{COLS[YEARS.index(y)]}{pr.rows['rev_ref']}-{COLS[YEARS.index(y)]}{{SBC}}" for y in (2023, 2024, 2025)}
    opx = fill_years(ramp({2026: 0.183, 2027: 0.180, 2028: 0.175}, [(2028, 0.175), (2031, 0.185)]), 2032, 0.185)
    sbc = fill_years({}, 2023, 0.004)
    pr.series("sbc", "SBC / receita", sbc, "FY25 4.450/1.128.610 = 0,39%. Sem add-back.")
    opex_hist = {y: v.replace("{SBC}", str(pr.rows["sbc"])) for y, v in opex_hist.items()}
    pr.series("opex", "Opex ex-SBC / receita (SG&A + P&D + outros operacionais)", opex_hist | {y: opx[y] for y in YEARS if y >= 2026}, "CY23-25 = (lucro bruto − resultado operacional)/receita − SBC (CY24 inclui impairment ¥21,4 bi). CY26 18,3% (1Q FY26 17,9%; guidance OPM 49,4% ~ GM 68% − opex 18,6%); P&D FY26e ¥110 bi = 6,4%. Normaliza a 18,5% (CY31+).")
    tax = fill_years({2026: 0.26}, 2027, 0.27)
    pr.series("tax", "Alíquota de imposto", {2023: 0.283, 2024: 0.283, 2025: 0.274} | {y: tax[y] for y in YEARS if y >= 2026}, "FY24 28,3% / FY25 27,4% (tanshin). Guidance FY26 implica 25,9%; 27% no longo prazo.")
    da_hist = {y: f"={COLS[YEARS.index(y)]}{pr.rows['da_ref']}/{COLS[YEARS.index(y)]}{pr.rows['rev_ref']}" for y in (2023, 2024, 2025)}
    da = fill_years({2026: 0.020, 2027: 0.019}, 2028, 0.020)
    pr.series("da", "Depreciação operacional / receita", da_hist | {y: da[y] for y in YEARS if y >= 2026}, "CY23-25 BBG. FY26e D&A ¥31 bi / 1.714 = 1,8%. Intensidade 2,0% no longo prazo (modelo asset-light: contract manufacturer).")
    cx_hist = {y: f"={COLS[YEARS.index(y)]}{pr.rows['capex_ref']}/{COLS[YEARS.index(y)]}{pr.rows['rev_ref']}" for y in (2023, 2024, 2025)}
    cx = fill_years({2026: 0.030, 2027: 0.030, 2028: 0.030}, 2029, 0.025)
    pr.series("capex", "Capex / receita", cx_hist | {y: cx[y] for y in YEARS if y >= 2026}, "CY23-25 BBG. FY26e ¥50 bi / 1.714 = 2,9% (expansão de capacidade 5.000 → 10.000+ testers/ano); 2,5% após CY28.")
    nwc = fill_years({}, 2026, 0.26)
    pr.series("nwc", "NWC operacional / receita", {2025: "=(E{ar}+E{inv}-E{ap})/F{rev}".replace("{ar}", str(pr.rows["ar"])).replace("{inv}", str(pr.rows["inv"])).replace("{ap}", str(pr.rows["ap"])).replace("{rev}", str(pr.rows["rev_ref"]))} | {y: nwc[y] for y in YEARS if y >= 2026},
              "NWC = recebíveis + estoques − fornecedores. 31-mar-26: 318,4 bi / receita CY25 1.032,9 = 30,8%; 30-jun-26: 297,8 bi / LTM ~1.232 = 24%. 26% constante.")
    fin = fill_years({2026: 66000}, 2027, 4000)
    pr.series("fin", "Resultado financeiro (¥ mi)", {y: fin[y] for y in YEARS if y >= 2026}, "CY26: jan-mar 2026 +19,3 bi (inclui ¥17,3 bi de call options) + abr-jun 2026 +44,1 bi (ganho de valuation de instrumentos financeiros ¥41,1 bi) + ~2 bi juros no 2H. CY27+ juros ~¥4 bi sobre caixa/aplicações. Não recorrente por natureza — ver EPS.", nf=NF_NUM)
    shp = ramp({2026: 727.5, 2027: 720.0, 2028: 714.0}, [(2028, 714.0), (2035, 690.0)]); fill_years(shp, 2036, 690.0)
    pr.series("sh", "Ações para EPS (mi, média do ano)", {y: shp[y] for y in YEARS if y >= 2026}, "Recompras ¥114 bi em FY25 e ¥42 bi no 1Q FY26 (~0,8% do capital por trimestre a ¥32k); CB ¥100 bi (2031) compensaria parte — líquido −0,8%/ano até CY35. Editável.", nf=NF_NUM1)
    q1s = fill_years({2027: 0.235, 2028: 0.240}, 2029, 0.240)
    pr.series("q1share", "Trimestre jan-mar como % da receita do CY (ponte FY↔CY)", {y: q1s[y] for y in YEARS if y >= 2027}, "Jan-mar 2026 = 328,1 / CY26 modelo ≈ 20% num ano de +55%; em crescimento de 15-20% o 1º trimestre pesa ~23,5-24%. Usado só na ponte FY(Mar) = CY − Q(jan-mar) + Q(jan-mar do ano seguinte).")

    pr.text("")
    pr.text("Método: FCFF = EBIT após SBC × (1 − imposto) + depreciação operacional − capex − variação de NWC. Terminal: NOPAT × (1 + g) × (1 − g / ROIC).")
    pr.text("Desconto de fim de ano; CY26 proporcional aos dias posteriores à data de valuation. Colunas são anos-calendário; a Advantest reporta FY-Mar — ver ponte na capa (linhas 96-104).")
    pr.text("TAM em US$ na base da própria Advantest (SoC + memória, EX burn-in). A base da Teradyne (7-9% do WFE) e a razão 'teste ÷ receita de semis' (~1%, UBS) NÃO são intercambiáveis — nunca misturar.")
    pr.text("CY23-25B são bases do cenário: receita total CY é reportada (BBG), o split por segmento aplica o mix FY-Mar do deck — os shares históricos implícitos são aproximações.")
    pr.text("A variante de casa está na linha 'ATE / WFE' CY27 (8,0%): manter 8,7% (CY26) levaria o TAM CY27 a ~$17,8 bi e a receita FY27 para perto do consenso; o consenso BBG FY27 (¥2.229,6 bi) implica intensidade ~9,5% do WFE em CY27.")
    pr.text("Fontes primárias: tanshin FY2025 (2026-04-27) e 1Q FY2026 (2026-07-29), deck e Q&A de 29-jul-2026 (ADVANTEST/transcripts). Consenso e histórico trimestral: Bloomberg (bdp/bdh) 2026-09-18.")

    R = pr.rows
    # ================================================================= Capa
    setup_sheet(ws, "ADVANTEST | DCF top-down",
                "¥ milhões, salvo ações (milhões), WFE/TAM (US$ bilhões), receita em US$ (milhões), FX (¥/US$) e valor por ação (¥). Colunas = ano-calendário CY2023–2045; a companhia reporta FY-Mar (ponte nas linhas 96-104).",
                "Azul / amarelo: premissas (aba Premissas e fontes). Verde: fontes internas. CY23–25B: bases do cenário calendarizadas a partir dos trimestres BBG, não receitas reportadas por segmento.")
    year_header(ws, 5)
    Pc = lambda key, c: f"{P}{c}{R[key]}"

    # ---- Block A: ATE market
    header_row(ws, 7, "Mercado de teste (ATE) | top-down em US$ bilhões — base Advantest (SoC + memória, ex burn-in)")
    label(ws, 8, "WFE global (US$ bi)")
    row_formula(ws, 8, lambda i, c, pc: f"={Pc('wfe', c)}" if YEARS[i] <= 2028 else f"={pc}8*(1+{c}9)", nf=NF_NUM1, font=F_LINK, end=6)
    row_formula(ws, 8, lambda i, c, pc: f"={pc}8*(1+{c}9)", nf=NF_NUM1, start=6)
    label(ws, 9, "Crescimento WFE")
    row_formula(ws, 9, lambda i, c, pc: f"={c}8/{pc}8-1" if YEARS[i] <= 2028 else f"={Pc('wfe_g', c)}", nf=NF_PCT, start=1, font=F_TXT)
    for i in range(6, len(COLS)): ws[f"{COLS[i]}9"].font = F_LINK
    label(ws, 10, "ATE / WFE (intensidade de teste)")
    row_formula(ws, 10, lambda i, c, pc: f"={Pc('ratio', c)}", nf=NF_PCT, font=F_LINK)
    label(ws, 11, "TAM ATE total (US$ bi)", bold=True, fill=FILL_HDR)
    row_formula(ws, 11, lambda i, c, pc: f"={c}8*{c}10", nf=NF_NUM2, fill=FILL_HDR, bold=True)
    label(ws, 12, "Crescimento TAM ATE")
    row_formula(ws, 12, lambda i, c, pc: f"={c}11/{pc}11-1", nf=NF_PCT, start=1)
    label(ws, 13, "TAM ATE | referência Advantest (deck 29-jul-2026; CY23 base Capstone)")
    row_formula(ws, 13, lambda i, c, pc: f"={Pc('tam_ref', c)}", nf=NF_NUM2, font=F_LINK, end=4)
    label(ws, 14, "Modelo − referência (US$ bi)")
    row_formula(ws, 14, lambda i, c, pc: f"={c}11-{c}13", nf=NF_CHK, end=4)
    label(ws, 15, "SoC / TAM ATE")
    row_formula(ws, 15, lambda i, c, pc: f"={Pc('soc_mix', c)}", nf=NF_PCT, font=F_LINK)
    label(ws, 16, "TAM SoC test (US$ bi)")
    row_formula(ws, 16, lambda i, c, pc: f"={c}11*{c}15", nf=NF_NUM2)
    label(ws, 17, "TAM memory test (US$ bi)")
    row_formula(ws, 17, lambda i, c, pc: f"={c}11-{c}16", nf=NF_NUM2)
    label(ws, 18, "TAM SoC | referência Advantest (US$ bi)")
    row_formula(ws, 18, lambda i, c, pc: f"={Pc('soc_ref', c)}" if YEARS[i] >= 2024 else None, nf=NF_NUM2, font=F_LINK, end=4)

    # ---- Block B: Advantest share and revenue
    header_row(ws, 20, "Advantest | share e receita")
    label(ws, 21, "FX ¥/US$ (média do ano)")
    row_formula(ws, 21, lambda i, c, pc: f"={Pc('fx', c)}", nf=NF_NUM1, font=F_LINK)
    label(ws, 22, "Share Advantest em SoC test")
    row_formula(ws, 22, lambda i, c, pc: f"=IFERROR({c}24/1000/{c}16,NA())" if YEARS[i] in BASE else f"={Pc('adv_soc', c)}", nf=NF_PCT)
    label(ws, 23, "Share Advantest em memory test")
    row_formula(ws, 23, lambda i, c, pc: f"=IFERROR({c}25/1000/{c}17,NA())" if YEARS[i] in BASE else f"={Pc('adv_mem', c)}", nf=NF_PCT)
    for i in range(3, len(COLS)):
        ws[f"{COLS[i]}22"].font = F_LINK; ws[f"{COLS[i]}23"].font = F_LINK
    label(ws, 24, "Receita SoC test systems (US$ mi)")
    row_formula(ws, 24, lambda i, c, pc: f"={c}27/{c}21" if YEARS[i] in BASE else f"={c}16*{c}22*1000", nf=NF_NUM)
    label(ws, 25, "Receita memory test systems (US$ mi)")
    row_formula(ws, 25, lambda i, c, pc: f"={c}28/{c}21" if YEARS[i] in BASE else f"={c}17*{c}23*1000", nf=NF_NUM)
    label(ws, 26, "Advantest | Receita (¥ mi)", bold=True)
    label(ws, 27, "SoC test systems")
    row_formula(ws, 27, lambda i, c, pc: f"={Pc('rev_ref', c)}*{Pc('ts_mix', c)}*{Pc('soc_in_ts', c)}" if YEARS[i] in BASE else f"={c}24*{c}21", nf=NF_NUM)
    label(ws, 28, "Memory test systems")
    row_formula(ws, 28, lambda i, c, pc: f"={Pc('rev_ref', c)}*{Pc('ts_mix', c)}*{Pc('mem_in_ts', c)}" if YEARS[i] in BASE else f"={c}25*{c}21", nf=NF_NUM)
    label(ws, 29, "Outros sistemas (handlers, probers, outros)")
    row_formula(ws, 29, lambda i, c, pc: f"={Pc('rev_ref', c)}*{Pc('ts_mix', c)}*{Pc('oth_in_ts', c)}" if YEARS[i] in BASE else f"=({c}27+{c}28)*{Pc('oth_ratio', c)}", nf=NF_NUM)
    label(ws, 30, "Test Systems total")
    row_formula(ws, 30, lambda i, c, pc: f"=SUM({c}27:{c}29)", nf=NF_NUM)
    label(ws, 31, "Services & Others")
    row_formula(ws, 31, lambda i, c, pc: f"={Pc('rev_ref', c)}*(1-{Pc('ts_mix', c)})" if YEARS[i] in BASE else f"={c}30*{Pc('so_ratio', c)}", nf=NF_NUM)
    for i in range(0, 3):
        for r in (27, 28, 29, 31): ws[f"{COLS[i]}{r}"].font = F_LINK
    label(ws, 32, "Receita total do cenário", bold=True, fill=FILL_HDR)
    row_formula(ws, 32, lambda i, c, pc: f"={c}30+{c}31", nf=NF_NUM, fill=FILL_HDR, bold=True)
    label(ws, 33, "Crescimento da receita")
    row_formula(ws, 33, lambda i, c, pc: f"={c}32/{pc}32-1", nf=NF_PCT, start=1)
    label(ws, 34, "Receita total | referência (CY23-25 reportado BBG; CY26-28 consenso BBG calendarizado)")
    row_formula(ws, 34, lambda i, c, pc: f"={Pc('rev_ref', c)}", nf=NF_NUM, font=F_LINK, end=6)
    label(ws, 35, "Cenário − referência")
    row_formula(ws, 35, lambda i, c, pc: f"={c}32-{c}34", nf=NF_NUM, end=6)

    r0 = 37
    pl = write_pl_block(ws, r0, R, rev_row=32, ticker="ADV")
    dsc = write_discount_block(ws, pl["fcff"], pl["end"] + 2)
    val = write_valuation_block(ws, dsc, pl, R, ccy="¥", extra_assets=[("Aplicações e títulos (investment securities)", "invsec")])
    n0 = val["end"] + 2
    note(ws, n0, "Top-down: TAM ATE = WFE × intensidade de teste, na base da própria Advantest (ex burn-in); receita = TAM SoC × share + TAM memória × share, em US$, convertida pelo FX médio; outros sistemas e serviços como razões.")
    note(ws, n0 + 1, "CY27 é a variante de casa: intensidade cai para 8,0% (lag WFE→wafer, TER mgmt) e o TAM cresce +19% contra WFE +30%; o consenso FY27 implica ~9,5%. Idêntico ao bridge da iniciação TER (2026-09-16) — os dois modelos oficiais usam o mesmo pool.")
    note(ws, n0 + 2, "CY23–25B: receita total CY reportada (soma dos trimestres BBG); split por segmento aplica o mix FY-Mar do deck — os shares históricos implícitos (linhas 22-23) são aproximações.")
    note(ws, n0 + 3, "O FCFF considera apenas a fração de CY26 após 27-ago-2026. Não há preço atual ou upside implícito na capa; preço e PT de consenso ficam em Premissas (informativo).")
    rc = n0 + 5
    header_row(ws, rc, "Reconciliações")
    checks = [
        ("TAM: SoC + memória = total", lambda c: f"={c}11-{c}16-{c}17", None),
        ("TAM modelo vs referência Advantest (CY23-26)", lambda c: f"={c}14", 4),
        ("Receita: soma dos segmentos", lambda c: f"={c}32-SUM({c}27:{c}29)-{c}31", None),
        ("Shares: TER (modelo TER, ex-IST) + Advantest ≤ 100% do TAM", lambda c: f"=MAX(0,({c}24+{c}25+{P}{c}{R['ter_us']})/1000/{c}11-1)", 6),
        ("Memo: residual do TAM para outros vendors (1 − Advantest − TER)", lambda c: f"=1-({c}24+{c}25+{P}{c}{R['ter_us']})/1000/{c}11", 6),
        ("Equity: EV − dívida líquida", None, None),
        ("Sensibilidade: centro = DCF base", None, None),
        ("Mercados: residual negativo", lambda c: f"=MIN(0,{c}17,{c}29,{c}31)", None),
    ]
    rr = rc + 1
    for text, fn, end in checks:
        label(ws, rr, text)
        if fn is not None:
            row_formula(ws, rr, lambda i, c, pc, fn=fn: fn(c), nf=(NF_PCT if text.startswith("Memo") else NF_CHK), end=end)
        elif text.startswith("Equity"):
            setc(ws, f"D{rr}", f"=D{val['equity']}-(D{val['ev']}-D{val['netdebt']})", F_TXT, nf=NF_CHK)
        elif text.startswith("Sensib"):
            setc(ws, f"D{rr}", f"=I{val['grid_center_row']}-D{val['ps']}", F_TXT, nf=NF_CHK)
        rr += 1
    # ---- FY bridge
    rb = rr + 1
    header_row(ws, rb, "Ponte FY-Mar ↔ CY (FY(t) = CY(t) − jan-mar(t) + jan-mar(t+1)) e consenso FY")
    label(ws, rb + 1, "Receita jan-mar do ano (¥ mi) | 2026 reportado; 2027+ = % do CY (premissa)")
    row_formula(ws, rb + 1, lambda i, c, pc: (f"={Pc('q1cy26_sales', 'D')}" if YEARS[i] == 2026 else f"={c}32*{Pc('q1share', c)}") if YEARS[i] >= 2026 else None, nf=NF_NUM, start=3, end=8)
    label(ws, rb + 2, "Receita FY-Mar modelo (¥ mi) | FY26 = abr-26→mar-27 na coluna CY26")
    nx = lambda c: COLS[COLS.index(c) + 1]
    row_formula(ws, rb + 2, lambda i, c, pc: f"={c}32-{c}{rb+1}+{nx(c)}{rb+1}" if 2026 <= YEARS[i] <= 2028 else None, nf=NF_NUM, start=3, end=6)
    label(ws, rb + 3, "Receita FY-Mar | guidance FY26 (jul-26) / consenso BBG FY27-28")
    row_formula(ws, rb + 3, lambda i, c, pc: (f"={Pc('g_sales', 'D')}" if YEARS[i] == 2026 else f"={Pc('cons_fy_sales', c)}") if 2026 <= YEARS[i] <= 2028 else None, nf=NF_NUM, font=F_LINK, start=3, end=6)
    label(ws, rb + 4, "Modelo − referência FY (%)")
    row_formula(ws, rb + 4, lambda i, c, pc: f"={c}{rb+2}/{c}{rb+3}-1" if 2026 <= YEARS[i] <= 2028 else None, nf=NF_PCT, start=3, end=6)
    label(ws, rb + 5, "Resultado operacional jan-mar (¥ mi) | 2026 reportado; 2027+ = margem EBIT do CY × receita jan-mar")
    row_formula(ws, rb + 5, lambda i, c, pc: (f"={Pc('q1cy26_oi', 'D')}" if YEARS[i] == 2026 else f"={c}{rb+1}*{c}{pl['ebitm']}") if YEARS[i] >= 2026 else None, nf=NF_NUM, start=3, end=8)
    label(ws, rb + 6, "Resultado operacional FY-Mar modelo (¥ mi)")
    row_formula(ws, rb + 6, lambda i, c, pc: f"={c}{pl['ebit']}-{c}{rb+5}+{nx(c)}{rb+5}" if 2026 <= YEARS[i] <= 2028 else None, nf=NF_NUM, start=3, end=6)
    label(ws, rb + 7, "Resultado operacional FY-Mar | guidance FY26 / consenso BBG FY27-28")
    row_formula(ws, rb + 7, lambda i, c, pc: (f"={Pc('g_oi', 'D')}" if YEARS[i] == 2026 else f"={Pc('cons_fy_oi', c)}") if 2026 <= YEARS[i] <= 2028 else None, nf=NF_NUM, font=F_LINK, start=3, end=6)
    label(ws, rb + 8, "Modelo − referência FY (%)")
    row_formula(ws, rb + 8, lambda i, c, pc: f"={c}{rb+6}/{c}{rb+7}-1" if 2026 <= YEARS[i] <= 2028 else None, nf=NF_PCT, start=3, end=6)
    label(ws, rb + 9, "Intensidade ATE/WFE CY27 implícita no consenso FY27 (receita ∝ TAM)")
    setc(ws, f"H{rb+9}", f"=H10*H{rb+3}/H{rb+2}", F_TXT, nf=NF_PCT, align="right")
    # ---- wiki summary
    rw = rb + 11
    write_wiki_block(ws, rw, R, pl, rev_row=32, ticker="ADV", val=val)
    wb.save(path)
    return dict(R=R, pl=pl, val=val, bridge=rb, wiki=rw)


# =====================================================================================================
# TER
# =====================================================================================================
def build_ter(path, adv_us):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Capa DCF - Base"
    wp = wb.create_sheet("Premissas e fontes")
    pr = Prem(wp, "TER", "Dados extraídos das fontes indicadas. US$ milhões salvo indicação; TAM/WFE em US$ bilhões. Ano fiscal = ano-calendário (dez).")

    pr.section("Histórico reportado (10-K) e referência de consenso / iniciação")
    pr.ref("rev_ref", "Receita total (US$ mi) | 10-K / consenso BBG CY26-28", [2676.3, 2819.9, 3190.0, 5065.9, 6237.3, 7543.4],
           "10-K FY23-FY25 (TER/TER_10-K_2026-02-19: 3.190.024; 2.819.880; 2.676.298). CY26-28: bdp BEST_SALES 1FY/2FY/3FY (2026-09-18).")
    pr.ref("init_rev", "Receita total | iniciação Capstone 2026-09-16 (base)", [None, None, None, 5126.5, 6219.8, 7693.6], "_wiki/_data/research/TER_Initiation_2026-09-16_model_out.json → cases.base.periods (ter_model.py). Substituído por este workbook.")
    pr.ref("semi", "Semiconductor Test (US$ mi) | segmento", [1866, 2016, 2523.7], "CY23-24 ASML_Peers_SemiCap_Felipe.xlsx | TER IS!K8:L8 (segmentação antiga); CY25 10-K FY25 (inclui IST 129,2 — ressegmentação 2025).")
    pr.ref("pt", "Product Test (US$ mi) | System Test + Wireless", [390, 404, 358.0], "CY23-24 ASML_Peers 'TER IS'!K9:L10 somados; CY25 10-K FY25.")
    pr.ref("rob", "Robotics (US$ mi)", [420, 400, 308.3], "CY23-24 ASML_Peers 'TER IS'!K11:L11; CY25 10-K FY25.")
    pr.ref("gm_ref", "Margem bruta (non-GAAP)", [0.574, 0.585, 0.582], "10-K FY24/FY25 (gross profit 57,4% / 58,5% / 58,2%).", nf=NF_PCT)
    pr.ref("oim_ref", "Margem operacional non-GAAP", [0.200, 0.210, 0.220], "Wiki TER.md tabela de casa (~21% / ~22%); FY23 ~20% (aprox., base do cenário).", nf=NF_PCT)
    pr.ref("sbc_ref", "Stock-based compensation (US$ mi)", [57.7, 60.1, 64.0], "10-K cash-flow: 57.682 / 60.122 / 63.999.", nf=NF_NUM1)
    pr.ref("dep_ref", "Depreciação (US$ mi)", [92.1, 101.0, 111.4], "10-K cash-flow: 92.118 / 100.977 / 111.445.", nf=NF_NUM1)
    pr.ref("capex_ref", "Capex (US$ mi) | 10-K / consenso BBG CY26-28", [159.6, 198.1, 224.0, 281.9, 352.6, 429.4], "10-K purchases of PP&E: 159.642 / 198.095 / 224.009; CY26-28 bdp BEST_CAPEX.", nf=NF_NUM1)
    pr.ref("ar", "Contas a receber (US$ mi) | dez-23 / dez-24 / dez-25 / jun-26", [422.1, 471.4, 786.9, 1109.7], "10-K FY24/FY25; 10-Q 2Q FY26 (2026-06-28).", nf=NF_NUM1)
    pr.ref("inv", "Estoques (US$ mi)", [310.0, 298.5, 379.6, 403.3], "10-K FY24/FY25; 10-Q 2Q FY26.", nf=NF_NUM1)
    pr.ref("ap", "Contas a pagar (US$ mi)", [180.1, 134.8, 269.2, 383.4], "10-K FY24/FY25; 10-Q 2Q FY26.", nf=NF_NUM1)
    pr.ref("eps_ref", "EPS non-GAAP (US$) | reportado / consenso BBG CY26-28", [2.93, 3.22, 3.97, 8.838, 11.453, 14.769], "FY23-25 releases (wiki TER.md); CY26-28 bdp BEST_EPS 1FY/2FY/3FY (2026-09-18).", nf=NF_NUM2)
    pr.ref("init_eps", "EPS non-GAAP | iniciação Capstone 2026-09-16 (base)", [None, None, None, 9.03, 11.92, 15.99], "model_out.json cases.base.periods.eps: 9,026 / 11,921 / 15,992.", nf=NF_NUM2)
    pr.ref("cons_ebit", "Consenso BBG — EBIT (US$ mi)", [None, None, None, 1655.7, 2143.5, 2724.3], "bdp BEST_EBIT 1FY/2FY/3FY. 19 analistas (13 buy / 6 hold), rating 4,32, PT médio $450,87.")
    pr.ref("cons_gm", "Consenso BBG — margem bruta", [None, None, None, 0.5936, 0.5951, 0.5971], "bdp BEST_GROSS_MARGIN.", nf=NF_PCT)
    pr.ref("adv_us", "Advantest test systems SoC + memória (US$ mi) | modelo oficial ADVANTEST — check de shares", adv_us, "Template DCF ADVANTEST.xlsx | Capa DCF - Base linhas 24+25 (CY23-25 implícito; CY26-28 cenário base). Valores colados — atualizar se o modelo Advantest mudar.")
    pr.ref("ist", "IST (storage test) dentro de Semi Test (US$ mi) | excluído do check de shares", [None, None, 129.2, 230, 245, 290], "CY25 10-K FY25 (IST 129,2); CY26-28 sub-segmentação da iniciação (model_out.json subseg). IST não está no TAM SoC+memória da Advantest.")
    pr.ref("tam_ref", "TAM ATE (US$ bi) | referência Advantest (deck 29-jul-2026; CY23 base Capstone)", [TAM_REF[2023], TAM_REF[2024], TAM_REF[2025], TAM_REF[2026]],
           "CY24 6,0 / CY25 9,0 / CY26e 13,75 (mid 13,0-14,5) — deck Advantest; validado pelo CEO da TER ('right zip code', call 2026-07-29). Base ex burn-in. CY23 4,9 = Industry Assumptions!K26.", nf=NF_NUM2)

    pr.section("Guidance 3Q FY26 (28-jul-2026) e âncoras da iniciação")
    pr.single("g_q3_rev", "3Q FY26 receita guidance (US$ mi, ponto médio $1.250)", 1250, "Press release 2026-07-28: $1,15-1,25 bi… revisado: $1.250 mi ±; H1 = 50-52% da receita do ano → FY26 $5,02-5,22 bi.", fill=None)
    pr.single("h1_rev", "1H FY26 receita reportada (US$ mi)", 2611.5, "1Q 1.282,5 + 2Q 1.329,0 (releases 2026-04-29 / 2026-07-28).", nf=NF_NUM1, fill=None)
    pr.single("h1_eps", "1H FY26 EPS non-GAAP reportado (US$)", 5.02, "Idem (2,56 + 2,47; companhia: $5,02).", nf=NF_NUM2, fill=None)

    pr.section("Valuation e balanço")
    pr.single("val_date", "Data de valuation", dt.datetime(2026, 8, 27), "Template DCF NVDA.xlsx | Audit & Checks!D5. Mantida a data para comparabilidade com AMD/AVGO.", nf=NF_DATE)
    pr.single("wacc", "WACC", 0.10, "Hipótese: 10% do template aplicado como WACC no FCFF (iniciação usou Ke 10% / g 3% com fade de margem a 30% → $212 rolado).", nf=NF_PCT)
    pr.single("g", "Crescimento terminal", 0.02, "Template DCF NVDA.xlsx | Capa DCF - Base!D91.", nf=NF_PCT)
    pr.single("roic", "ROIC incremental terminal", 0.20, "Hipótese do template: reinvestimento terminal = g / ROIC.", nf=NF_PCT)
    pr.single("shares", "Ações diluídas | referência 2Q FY26 (mi)", 157.7, "10-Q 2Q FY26: weighted diluted 157.693 mil; em circulação 156,34 mi (27-jul-2026).", nf=NF_NUM1, fill=None)
    pr.single("cash", "Caixa + títulos (US$ mi)", 517.1, "10-Q 2Q FY26 (28-jun-2026): caixa 349,5 + títulos CP 5,3 + títulos LP 162,3.", nf=NF_NUM1, fill=None)
    pr.single("technoprobe", "Participação Technoprobe (equity method, US$ mi)", 515.0, "10-Q 2Q FY26: equity method investment 514.957 (10% da Technoprobe). Ativo não operacional somado ao equity.", nf=NF_NUM1, fill=None)
    pr.single("debt", "Dívida financeira bruta (US$ mi)", 0.0, "Sem dívida em 28-jun-2026 (revolver $750 mi disponível; $200 mi de dez-25 quitados no 1H).", nf=NF_NUM1, fill=None)
    pr.single("bs_date", "Data-base do balanço no modelo", dt.datetime(2026, 6, 28), "Anterior à data de valuation; atualização manual disponível.", nf=NF_DATE, fill=None)
    pr.single("px", "Preço de referência (US$, informativo)", 363.05, "BBG PX_LAST TER US, 2026-09-18. Não entra no valuation.", nf=NF_NUM2, fill=None)
    pr.single("pt_cons", "PT médio consenso (US$, informativo)", 450.87, "BBG BEST_TARGET_PRICE, 19 analistas, 2026-09-18. Iniciação Capstone: NEUTRAL, PT $400 (25x CY28E).", nf=NF_NUM2, fill=None)

    pr.section("Premissas de mercado e operação (CY)")
    pr.year_hdr()
    pr.series("wfe", "WFE global (US$ bi)", {y: WFE[y] for y in WFE}, "CY23-24 SEMI/VLSI via ASML_Peers_SemiCap_Felipe.xlsx | Industry Assumptions!K10:L10; CY25 UBS actual 116; CY26-28 158/205/240 = base da iniciação TER (2026-09-16). Idêntico ao Template DCF ADVANTEST.", nf=NF_NUM1)
    pr.series("wfe_g", "Crescimento WFE (CY29+)", {y: v for y, v in WFE_G.items() if y >= 2029}, "Hipótese pós-CY28: +6% CY29-30, convergindo a +3% a partir de CY34. Editável.")
    ratio_vals = {y: f"={COLS[YEARS.index(y)]}{pr.rows['tam_ref']}/{COLS[YEARS.index(y)]}{pr.rows['wfe']}" for y in (2023, 2024, 2025, 2026)}
    ratio_vals.update({y: RATIO_IN[y] for y in YEARS if y >= 2027})
    pr.series("ratio", "ATE / WFE (intensidade de teste, base Advantest ex burn-in)", ratio_vals, "CY23-26 calibrado ao TAM de referência (fórmula). CY27 8,0% = lag WFE→wafer (mgmt 07-29: 'could revert to 6-7%' na base TER); CY28 8,3%; fade a 8,0%. Na base da iniciação (8,0/7,3/7,5% × WFE) o TAM era 12,6/15,0/18,0 — mesmo crescimento, base menor.")
    share = fill_years(ramp({2026: 0.314, 2027: 0.323, 2028: 0.333}, [(2028, 0.333), (2030, 0.335)]), 2031, 0.335)
    pr.series("share", "Teradyne | share do TAM ATE (Semi Test ÷ TAM)", {y: share[y] for y in YEARS if y >= 2026}, "Calibrado para reproduzir a receita Semi Test da iniciação ($4,32 / 5,30 / 6,64 bi): +90bp/+100bp por ano — dentro do bogey de IR ('couple hundred bps', 2026-08-03; 300-400bp em 2026 na base TER). Flat 33,5% após CY30. CY23-25 implícito na capa.")
    ptg = fill_years(ramp({2026: 410 / 358.0 - 1, 2027: 465 / 410 - 1, 2028: 525 / 465 - 1}, [(2028, 525 / 465 - 1), (2032, 0.03)]), 2033, 0.03)
    pr.series("pt_g", "Crescimento Product Test", {y: ptg[y] for y in YEARS if y >= 2026}, "CY26-28 = níveis da iniciação ($410 / 465 / 525 mi: Omnix, MLTP, CPO ~$200 mi em 2027); converge a +3%.")
    robg = fill_years(ramp({2026: 396 / 308.3 - 1, 2027: 460 / 396 - 1, 2028: 530 / 460 - 1}, [(2028, 530 / 460 - 1), (2033, 0.03)]), 2034, 0.03)
    pr.series("rob_g", "Crescimento Robotics", {y: robg[y] for y in YEARS if y >= 2026}, "CY26-28 = níveis da iniciação ($396 / 460 / 530 mi; 1H26 +33% y/y, 'grow in proportion with the company'); converge a +3%.")
    gm = fill_years({2026: 0.5946, 2027: 0.5951, 2028: 0.6020}, 2029, 0.600)
    pr.series("gm", "Margem bruta (non-GAAP)", {2023: f"=D{pr.rows['gm_ref']}", 2024: f"=E{pr.rows['gm_ref']}", 2025: f"=F{pr.rows['gm_ref']}"} | {y: gm[y] for y in YEARS if y >= 2026},
              "CY23-25 reportado. CY26 59,5% (FY 'right around 59%'), CY27 59,5%, CY28 60,2% ('60% or higher over the mid-term', IR 08-03); 60% no longo prazo.")
    sbc = fill_years({}, 2026, 0.014)
    pr.series("sbc", "SBC / receita", {2023: f"=D{pr.rows['sbc_ref']}/D{pr.rows['rev_ref']}", 2024: f"=E{pr.rows['sbc_ref']}/E{pr.rows['rev_ref']}", 2025: f"=F{pr.rows['sbc_ref']}/F{pr.rows['rev_ref']}"} | {y: sbc[y] for y in YEARS if y >= 2026},
              "10-K. Non-GAAP da TER NÃO exclui SBC — opex ex-SBC + SBC = opex non-GAAP. 1,4% (iniciação).")
    opx = ramp({2026: 0.2728 - 0.014, 2027: 0.2473 - 0.014, 2028: 0.2219 - 0.014}, [(2028, 0.2219 - 0.014), (2033, 0.2600 - 0.014)]); fill_years(opx, 2034, 0.2600 - 0.014)
    pr.series("opex", "Opex ex-SBC / receita (non-GAAP)", {2023: f"=D{pr.rows['gm_ref']}-D{pr.rows['oim_ref']}-D{{S}}", 2024: f"=E{pr.rows['gm_ref']}-E{pr.rows['oim_ref']}-E{{S}}", 2025: f"=F{pr.rows['gm_ref']}-F{pr.rows['oim_ref']}-F{{S}}"} | {y: opx[y] for y in YEARS if y >= 2026},
              "CY26-28 = opex da iniciação ($1.398 / 1.538 / 1.707 mi = 27,3% / 24,7% / 22,2% da receita, 'opex cresce menos da metade da receita', CEO 09-09) menos SBC. Normaliza para 26% (margem EBIT ~34%) até CY33 — fade mais suave que a iniciação (30%).")
    for y in (2023, 2024, 2025):
        c = COLS[YEARS.index(y)]
        wp[f"{c}{pr.rows['opex']}"].value = wp[f"{c}{pr.rows['opex']}"].value.replace("{S}", str(pr.rows["sbc"]))
    tax = fill_years({2026: 0.15, 2027: 0.15, 2028: 0.155}, 2029, 0.16)
    pr.series("tax", "Alíquota de imposto (non-GAAP)", {2023: 0.146, 2024: 0.098, 2025: 0.121} | {y: tax[y] for y in YEARS if y >= 2026}, "GAAP 10-K: 14,6% / 9,8% / 12,1%. Non-GAAP 15% / 15% / 15,5% (iniciação; 2Q FY26 15,1%); 16% no longo prazo.")
    da = fill_years({}, 2026, 0.024)
    pr.series("da", "Depreciação operacional / receita", {2023: f"=D{pr.rows['dep_ref']}/D{pr.rows['rev_ref']}", 2024: f"=E{pr.rows['dep_ref']}/E{pr.rows['rev_ref']}", 2025: f"=F{pr.rows['dep_ref']}/F{pr.rows['rev_ref']}"} | {y: da[y] for y in YEARS if y >= 2026},
              "10-K depreciação (sem amortização de intangíveis, já excluída do EBIT non-GAAP). 2,4% (iniciação).")
    cx = fill_years({2026: 0.069, 2027: 0.061, 2028: 0.056}, 2029, 0.050)
    pr.series("capex", "Capex / receita", {2023: f"=D{pr.rows['capex_ref']}/D{pr.rows['rev_ref']}", 2024: f"=E{pr.rows['capex_ref']}/E{pr.rows['rev_ref']}", 2025: f"=F{pr.rows['capex_ref']}/F{pr.rows['rev_ref']}"} | {y: cx[y] for y in YEARS if y >= 2026},
              "Iniciação: $355 / 380 / 430 mi (BEst $282 / 353 / 429); 5% no longo prazo (média FY19-25 5,8%).")
    nwc = fill_years({}, 2026, 0.25)
    pr.series("nwc", "NWC operacional / receita", {2023: f"=(D{pr.rows['ar']}+D{pr.rows['inv']}-D{pr.rows['ap']})/D{pr.rows['rev_ref']}", 2024: f"=(E{pr.rows['ar']}+E{pr.rows['inv']}-E{pr.rows['ap']})/E{pr.rows['rev_ref']}", 2025: f"=(F{pr.rows['ar']}+F{pr.rows['inv']}-F{pr.rows['ap']})/F{pr.rows['rev_ref']}"} | {y: nwc[y] for y in YEARS if y >= 2026},
              "NWC = recebíveis + estoques − fornecedores. Dez-25 28,1%; jun-26 $1.130 mi / LTM ~$4.460 mi = 25,3%. 25% constante.")
    fin = fill_years({}, 2026, 20.0)
    pr.series("fin", "Outras receitas (juros) (US$ mi)", {y: fin[y] for y in YEARS if y >= 2026}, "~+$5 mi/trimestre (2Q FY26 +$5,8 mi; caixa ~$0,5 bi, sem dívida).", nf=NF_NUM1)
    aff = fill_years({}, 2026, 22.0)
    pr.series("affil", "Equity method Technoprobe, base non-GAAP (US$ mi)", {y: aff[y] for y in YEARS if y >= 2026}, "~+$5,5 mi/trimestre (GAAP −$1,9 mi + $7,6 mi de amortização add-back no 2Q FY26). Fora do FCFF.", nf=NF_NUM1)
    shp = ramp({2026: 157.8, 2027: 157.5, 2028: 157.0}, [(2028, 157.0), (2035, 153.5)]); fill_years(shp, 2036, 153.5)
    pr.series("sh", "Ações diluídas para EPS (mi, média do ano)", {y: shp[y] for y in YEARS if y >= 2026}, "Iniciação: 2H26 $150 mi de recompra, $400-450 mi/ano depois (~−0,3%/ano líquido de SBC).", nf=NF_NUM1)

    pr.text("")
    pr.text("Método: FCFF = EBIT non-GAAP (após SBC) × (1 − imposto) + depreciação operacional − capex − variação de NWC. Terminal: NOPAT × (1 + g) × (1 − g / ROIC).")
    pr.text("Desconto de fim de ano; CY26 proporcional aos dias posteriores à data de valuation. Ano fiscal da Teradyne = ano-calendário.")
    pr.text("TAM em US$ na base da Advantest (SoC + memória, EX burn-in) — a MESMA do Template DCF ADVANTEST — para que os shares das duas somem contra o mesmo pool. Na base TER (7-9% do WFE) o share da TER lê ~34-37%.")
    pr.text("CY26-28 reproduz a iniciação de 2026-09-16 (receita $5,13 / 6,22 / 7,69 bi; EPS $9,03 / 11,92 / 15,99) dentro de ~1% — as diferenças vêm da anualização (a iniciação é trimestral).")
    pr.text("Fontes primárias: 10-K FY23-FY25, 10-Q 2Q FY26, releases 2026-04-29 / 2026-07-28, call 2026-07-29 (TER/transcripts), UBS fireside com IR 2026-08-03. Consenso: Bloomberg (bdp) 2026-09-18.")

    R = pr.rows
    setup_sheet(ws, "TER | DCF top-down",
                "US$ milhões, salvo ações (milhões) e WFE/TAM (US$ bilhões). Horizonte CY2023–2045; ano fiscal = ano-calendário.",
                "Azul / amarelo: premissas (aba Premissas e fontes). Verde: fontes internas. CY23–25B: bases do cenário (segmentação de 2025 difere da anterior).")
    year_header(ws, 5)
    Pc = lambda key, c: f"{P}{c}{R[key]}"
    header_row(ws, 7, "Mercado de teste (ATE) | top-down em US$ bilhões — base Advantest (SoC + memória, ex burn-in), idêntico ao Template DCF ADVANTEST")
    label(ws, 8, "WFE global (US$ bi)")
    row_formula(ws, 8, lambda i, c, pc: f"={Pc('wfe', c)}", nf=NF_NUM1, font=F_LINK, end=6)
    row_formula(ws, 8, lambda i, c, pc: f"={pc}8*(1+{c}9)", nf=NF_NUM1, start=6)
    label(ws, 9, "Crescimento WFE")
    row_formula(ws, 9, lambda i, c, pc: f"={c}8/{pc}8-1" if YEARS[i] <= 2028 else f"={Pc('wfe_g', c)}", nf=NF_PCT, start=1)
    for i in range(6, len(COLS)): ws[f"{COLS[i]}9"].font = F_LINK
    label(ws, 10, "ATE / WFE (intensidade de teste)")
    row_formula(ws, 10, lambda i, c, pc: f"={Pc('ratio', c)}", nf=NF_PCT, font=F_LINK)
    label(ws, 11, "TAM ATE total (US$ bi)", bold=True, fill=FILL_HDR)
    row_formula(ws, 11, lambda i, c, pc: f"={c}8*{c}10", nf=NF_NUM2, fill=FILL_HDR, bold=True)
    label(ws, 12, "Crescimento TAM ATE")
    row_formula(ws, 12, lambda i, c, pc: f"={c}11/{pc}11-1", nf=NF_PCT, start=1)
    label(ws, 13, "TAM ATE | referência Advantest (deck 29-jul-2026; CY23 base Capstone)")
    row_formula(ws, 13, lambda i, c, pc: f"={Pc('tam_ref', c)}", nf=NF_NUM2, font=F_LINK, end=4)
    label(ws, 14, "Modelo − referência (US$ bi)")
    row_formula(ws, 14, lambda i, c, pc: f"={c}11-{c}13", nf=NF_CHK, end=4)
    label(ws, 15, "TAM ATE na base da iniciação TER (memo: 8,0% / 7,3% / 7,5% × WFE)")
    row_formula(ws, 15, lambda i, c, pc: {2026: "=G8*0.08", 2027: "=H8*0.073", 2028: "=I8*0.075"}.get(YEARS[i]), nf=NF_NUM2, start=3, end=6)

    header_row(ws, 17, "Teradyne | share e receita (US$ milhões)")
    label(ws, 18, "Share Teradyne no TAM ATE (Semi Test ÷ TAM)")
    row_formula(ws, 18, lambda i, c, pc: f"=IFERROR({c}19/1000/{c}11,NA())" if YEARS[i] in BASE else f"={Pc('share', c)}", nf=NF_PCT)
    for i in range(3, len(COLS)): ws[f"{COLS[i]}18"].font = F_LINK
    label(ws, 19, "Semiconductor Test")
    row_formula(ws, 19, lambda i, c, pc: f"={Pc('semi', c)}" if YEARS[i] in BASE else f"={c}11*{c}18*1000", nf=NF_NUM)
    label(ws, 20, "Product Test")
    row_formula(ws, 20, lambda i, c, pc: f"={Pc('pt', c)}" if YEARS[i] in BASE else f"={pc}20*(1+{Pc('pt_g', c)})", nf=NF_NUM)
    label(ws, 21, "Robotics")
    row_formula(ws, 21, lambda i, c, pc: f"={Pc('rob', c)}" if YEARS[i] in BASE else f"={pc}21*(1+{Pc('rob_g', c)})", nf=NF_NUM)
    for i in range(0, 3):
        for r in (19, 20, 21): ws[f"{COLS[i]}{r}"].font = F_LINK
    label(ws, 22, "Receita total do cenário", bold=True, fill=FILL_HDR)
    row_formula(ws, 22, lambda i, c, pc: f"=SUM({c}19:{c}21)", nf=NF_NUM, fill=FILL_HDR, bold=True)
    label(ws, 23, "Crescimento da receita")
    row_formula(ws, 23, lambda i, c, pc: f"={c}22/{pc}22-1", nf=NF_PCT, start=1)
    label(ws, 24, "Receita total | referência (CY23-25 10-K; CY26-28 consenso BBG)")
    row_formula(ws, 24, lambda i, c, pc: f"={Pc('rev_ref', c)}", nf=NF_NUM, font=F_LINK, end=6)
    label(ws, 25, "Cenário − referência")
    row_formula(ws, 25, lambda i, c, pc: f"={c}22-{c}24", nf=NF_NUM, end=6)
    label(ws, 26, "Receita total | iniciação Capstone 2026-09-16")
    row_formula(ws, 26, lambda i, c, pc: f"={Pc('init_rev', c)}", nf=NF_NUM, font=F_LINK, start=3, end=6)
    label(ws, 27, "Cenário − iniciação (%)")
    row_formula(ws, 27, lambda i, c, pc: f"={c}22/{c}26-1", nf=NF_PCT, start=3, end=6)

    pl = write_pl_block(ws, 29, R, rev_row=22, ticker="TER")
    dsc = write_discount_block(ws, pl["fcff"], pl["end"] + 2)
    val = write_valuation_block(ws, dsc, pl, R, ccy="US$", extra_assets=[("Participação Technoprobe (equity method)", "technoprobe")])
    n0 = val["end"] + 2
    note(ws, n0, "Top-down: TAM ATE = WFE × intensidade de teste (base Advantest, ex burn-in — a mesma do modelo oficial da Advantest); Semi Test = TAM × share; Product Test e Robotics por crescimento.")
    note(ws, n0 + 1, "CY26-28 reproduz a iniciação de 2026-09-16 (NEUTRAL, PT $400 = 25x CY28E): mesma WFE, mesmo crescimento de TAM (+19%/+20%), mesma receita por segmento, GM, opex, imposto e recompras; margem EBIT normaliza para ~34% até CY33 (a iniciação usava fade a 30% no DCF).")
    note(ws, n0 + 2, "CY23–25B: bases do cenário (segmentação de 2025 move IST para Semi Test; CY23-24 usam a segmentação antiga do peer model).")
    note(ws, n0 + 3, "O FCFF considera apenas a fração de CY26 após 27-ago-2026. Não há preço atual ou upside implícito na capa; preço e PT ficam em Premissas (informativo).")
    rc = n0 + 5
    header_row(ws, rc, "Reconciliações")
    checks = [
        ("TAM modelo vs referência Advantest (CY23-26)", lambda c: f"={c}14", 4),
        ("Receita: soma dos segmentos", lambda c: f"={c}22-SUM({c}19:{c}21)", None),
        ("Shares: TER (ex-IST) + Advantest (modelo Advantest) ≤ 100% do TAM", lambda c: f"=MAX(0,({c}19-{P}{c}{R['ist']}+{P}{c}{R['adv_us']})/1000/{c}11-1)", 6),
        ("Memo: residual do TAM para outros vendors (1 − TER ex-IST − Advantest)", lambda c: f"=1-({c}19-{P}{c}{R['ist']}+{P}{c}{R['adv_us']})/1000/{c}11", 6),
        ("Iniciação: receita CY26-28 dentro de ±1,5%", lambda c: f"=IF(ABS({c}27)>0.015,{c}27,0)", 6),
        ("Equity: EV − dívida líquida", None, None),
        ("Sensibilidade: centro = DCF base", None, None),
    ]
    rr = rc + 1
    for text, fn, end in checks:
        label(ws, rr, text)
        if fn is not None:
            row_formula(ws, rr, lambda i, c, pc, fn=fn: fn(c), nf=(NF_PCT if text.startswith("Memo") else NF_CHK), end=end, start=3 if "Iniciação" in text else (2 if "IST" in text else 0))
        elif text.startswith("Equity"):
            setc(ws, f"D{rr}", f"=D{val['equity']}-(D{val['ev']}-D{val['netdebt']})", F_TXT, nf=NF_CHK)
        elif text.startswith("Sensib"):
            setc(ws, f"D{rr}", f"=I{val['grid_center_row']}-D{val['ps']}", F_TXT, nf=NF_CHK)
        rr += 1
    rw = rr + 1
    write_wiki_block(ws, rw, R, pl, rev_row=22, ticker="TER", val=val)
    wb.save(path)
    return dict(R=R, pl=pl, val=val, wiki=rw)


# =====================================================================================================
# Shared blocks
# =====================================================================================================
def write_pl_block(ws, r0, R, rev_row, ticker):
    Pc = lambda key, c: f"{P}{c}{R[key]}"
    rev = rev_row
    header_row(ws, r0, "Resultado operacional e caixa")
    r = r0 + 1; rows = {}
    label(ws, r, "Margem bruta"); row_formula(ws, r, lambda i, c, pc: f"={Pc('gm', c)}", nf=NF_PCT, font=F_LINK); rows["gm"] = r; r += 1
    label(ws, r, "Lucro bruto"); row_formula(ws, r, lambda i, c, pc: f"={c}{rev}*{c}{rows['gm']}"); rows["gp"] = r; r += 1
    label(ws, r, "Opex ajustado, ex-SBC"); rows["opex"] = r
    row_formula(ws, r, lambda i, c, pc: f"=-{c}{rev}*{c}{r+1}"); r += 1
    label(ws, r, "Opex ex-SBC / receita"); row_formula(ws, r, lambda i, c, pc: f"={Pc('opex', c)}", nf=NF_PCT, font=F_LINK); rows["opexr"] = r; r += 1
    label(ws, r, "Stock-based compensation"); row_formula(ws, r, lambda i, c, pc: f"=-{c}{rev}*{Pc('sbc', c)}"); rows["sbc"] = r; r += 1
    label(ws, r, "EBIT após SBC" + (" (= resultado operacional IFRS)" if ticker == "ADV" else " (= resultado operacional non-GAAP)"), bold=True)
    row_formula(ws, r, lambda i, c, pc: f"=SUM({c}{rows['gp']}:{c}{rows['opex']},{c}{rows['sbc']})", bold=True); rows["ebit"] = r; r += 1
    label(ws, r, "Margem EBIT após SBC"); row_formula(ws, r, lambda i, c, pc: f"={c}{rows['ebit']}/{c}{rev}", nf=NF_PCT); rows["ebitm"] = r; r += 1
    label(ws, r, "Alíquota de imposto"); row_formula(ws, r, lambda i, c, pc: f"={Pc('tax', c)}", nf=NF_PCT, font=F_LINK); rows["tax"] = r; r += 1
    label(ws, r, "NOPAT"); row_formula(ws, r, lambda i, c, pc: f"={c}{rows['ebit']}*(1-{c}{rows['tax']})"); rows["nopat"] = r; r += 1
    label(ws, r, "Depreciação operacional"); row_formula(ws, r, lambda i, c, pc: f"={c}{rev}*{Pc('da', c)}"); rows["da"] = r; r += 1
    label(ws, r, "Capex"); row_formula(ws, r, lambda i, c, pc: f"=-{c}{rev}*{Pc('capex', c)}"); rows["capex"] = r; r += 1
    label(ws, r, "Capital de giro operacional (NWC)"); row_formula(ws, r, lambda i, c, pc: f"={c}{rev}*{Pc('nwc', c)}" if YEARS[i] >= 2025 else None); rows["nwc"] = r; r += 1
    label(ws, r, "Variação de NWC | efeito caixa"); row_formula(ws, r, lambda i, c, pc: f"=-({c}{rows['nwc']}-{pc}{rows['nwc']})", start=3); rows["dnwc"] = r; r += 1
    label(ws, r, "Fluxo de caixa livre (FCFF)", bold=True)
    row_formula(ws, r, lambda i, c, pc: f"=SUM({c}{rows['nopat']}:{c}{rows['capex']},{c}{rows['dnwc']})", start=3, bold=True); rows["fcff"] = r; r += 1
    label(ws, r, "FCFF / receita"); row_formula(ws, r, lambda i, c, pc: f"={c}{rows['fcff']}/{c}{rev}", nf=NF_PCT, start=3); rows["fcffr"] = r
    rows["end"] = r; rows["rev"] = rev
    return rows


def write_discount_block(ws, fcff_row, r0):
    rows = {}
    label(ws, r0, "Data do fluxo de caixa"); row_formula(ws, r0, lambda i, c, pc: f"=DATE({YEARS[i]},12,31)", nf=NF_DATE_S); rows["date"] = r0
    vd = "$D$" + str(r0 + 7)   # valuation date cell (row r0+7 = 'Data de valuation' in valuation block)
    label(ws, r0 + 1, "Prazo de desconto (anos)"); row_formula(ws, r0 + 1, lambda i, c, pc: f"=MAX(0,({c}{r0}-{vd})/365)", nf=NF_NUM2); rows["t"] = r0 + 1
    label(ws, r0 + 2, "Parcela pós-valuation do ano"); row_formula(ws, r0 + 2, lambda i, c, pc: f"=MAX(0,MIN(1,({c}{r0}-{vd})/({c}{r0}-DATE({YEARS[i]},1,1)+1)))", nf=NF_PCT); rows["frac"] = r0 + 2
    label(ws, r0 + 3, "FCFF considerado no valuation"); row_formula(ws, r0 + 3, lambda i, c, pc: "=0" if i < 3 else f"={c}{fcff_row}*{c}{r0+2}"); rows["fcffv"] = r0 + 3
    wacc = "$D$" + str(r0 + 8)
    label(ws, r0 + 4, "Valor presente do FCFF"); row_formula(ws, r0 + 4, lambda i, c, pc: f"={c}{r0+3}/(1+{wacc})^{c}{r0+1}"); rows["pv"] = r0 + 4
    rows["end"] = r0 + 4; rows["vstart"] = r0 + 6
    return rows


def write_valuation_block(ws, dsc, pl, R, ccy, extra_assets):
    r0 = dsc["vstart"]; rows = {}
    header_row(ws, r0, "Valuation | FCFF e ponte para equity")
    label(ws, r0 + 1, "Data de valuation"); setc(ws, f"D{r0+1}", f"={P}D{R['val_date']}", F_LINK, nf=NF_DATE); rows["vdate"] = r0 + 1
    assert r0 + 1 == dsc["end"] + 3, "valuation date row must sit at discount r0+7"
    label(ws, r0 + 2, "WACC"); setc(ws, f"D{r0+2}", f"={P}D{R['wacc']}", F_LINK, nf=NF_PCT); rows["wacc"] = r0 + 2
    label(ws, r0 + 3, "Crescimento terminal (g)"); setc(ws, f"D{r0+3}", f"={P}D{R['g']}", F_LINK, nf=NF_PCT); rows["g"] = r0 + 3
    label(ws, r0 + 4, "ROIC incremental terminal"); setc(ws, f"D{r0+4}", f"={P}D{R['roic']}", F_LINK, nf=NF_PCT); rows["roic"] = r0 + 4
    label(ws, r0 + 5, "Ações diluídas (milhões)"); setc(ws, f"D{r0+5}", f"={P}D{R['shares']}", F_LINK, nf=NF_NUM1); rows["sh"] = r0 + 5
    label(ws, r0 + 6, "Caixa + aplicações"); setc(ws, f"D{r0+6}", f"={P}D{R['cash']}", F_LINK, nf=NF_NUM); rows["cash"] = r0 + 6
    r = r0 + 7; extra_rows = []
    for text, key in extra_assets:
        label(ws, r, text); setc(ws, f"D{r}", f"={P}D{R[key]}", F_LINK, nf=NF_NUM); extra_rows.append(r); r += 1
    label(ws, r, "Dívida financeira bruta"); setc(ws, f"D{r}", f"={P}D{R['debt']}", F_LINK, nf=NF_NUM); rows["debt"] = r; r += 1
    label(ws, r, "Dívida líquida (− ativos não operacionais)")
    setc(ws, f"D{r}", f"=D{rows['debt']}-D{rows['cash']}" + "".join(f"-D{x}" for x in extra_rows), F_TXT, nf=NF_NUM); rows["netdebt"] = r; r += 2
    Z = COLS[-1]; G0 = COLS[3]
    label(ws, r, "PV dos fluxos explícitos"); setc(ws, f"D{r}", f"=SUM({G0}{dsc['pv']}:{Z}{dsc['pv']})", F_TXT, nf=NF_NUM); rows["pvx"] = r; r += 1
    label(ws, r, "NOPAT terminal"); setc(ws, f"D{r}", f"={Z}{pl['nopat']}*(1+D{rows['g']})", F_TXT, nf=NF_NUM); rows["nopat_t"] = r; r += 1
    label(ws, r, "Reinvestimento líquido terminal"); setc(ws, f"D{r}", f"=D{rows['nopat_t']}*D{rows['g']}/D{rows['roic']}", F_TXT, nf=NF_NUM); rows["reinv"] = r; r += 1
    label(ws, r, "FCFF terminal"); setc(ws, f"D{r}", f"=IF(AND(D{rows['wacc']}>D{rows['g']},D{rows['roic']}>D{rows['g']}),D{rows['nopat_t']}-D{rows['reinv']},NA())", F_TXT, nf=NF_NUM); rows["fcff_t"] = r; r += 1
    label(ws, r, "Valor terminal não descontado"); setc(ws, f"D{r}", f"=D{rows['fcff_t']}/(D{rows['wacc']}-D{rows['g']})", F_TXT, nf=NF_NUM); rows["tv"] = r; r += 1
    label(ws, r, "PV do valor terminal"); setc(ws, f"D{r}", f"=D{rows['tv']}/(1+D{rows['wacc']})^{Z}{dsc['t']}", F_TXT, nf=NF_NUM); rows["pvtv"] = r; r += 1
    label(ws, r, "Enterprise value"); setc(ws, f"D{r}", f"=SUM(D{rows['pvx']},D{rows['pvtv']})", F_TXT, nf=NF_NUM); rows["ev"] = r; r += 1
    label(ws, r, "Equity value"); setc(ws, f"D{r}", f"=D{rows['ev']}-D{rows['netdebt']}", F_TXT, nf=NF_NUM); rows["equity"] = r; r += 1
    label(ws, r, f"Valor por ação ({ccy})", bold=True, fill=FILL_RES); ws[f"C{r}"].font = F_RES
    setc(ws, f"D{r}", f"=D{rows['equity']}/D{rows['sh']}", F_RES, nf=('"¥"#,##0' if ccy == "¥" else '"$"0.00'), fill=FILL_RES); rows["ps"] = r; r += 1
    label(ws, r, "Valor terminal / enterprise value"); setc(ws, f"D{r}", f"=D{rows['pvtv']}/D{rows['ev']}", F_TXT, nf=NF_PCT); rows["tvshare"] = r; r += 1
    label(ws, r, "Valor por ação | fluxos explícitos apenas (sem terminal)"); setc(ws, f"D{r}", f"=(D{rows['pvx']}-D{rows['netdebt']})/D{rows['sh']}", F_TXT, nf=('"¥"#,##0' if ccy == "¥" else '"$"0.00')); rows["ps_nt"] = r
    # ---- sensitivity grid WACC x g (F..K, rows r0+1 .. r0+6), centre = base
    setc(ws, f"F{r0+1}", f"Sensibilidade | WACC × g ({ccy} / ação)", F_TXTB)
    setc(ws, f"F{r0+3}", f"=D{rows['ps']}", F_TXT, nf=(NF_NUM if ccy == "¥" else NF_NUM2), fill=FILL_HDR)
    gcols = ["G", "H", "I", "J", "K"]; gd = [-0.01, -0.005, 0, 0.005, 0.01]
    for gc, d in zip(gcols, gd):
        setc(ws, f"{gc}{r0+3}", f"=$D${rows['g']}+{d}", F_TXTB, nf=NF_PCT, fill=FILL_HDR)
    wd = [-0.02, -0.01, 0, 0.01, 0.02]
    for k, d in enumerate(wd):
        rr = r0 + 4 + k
        setc(ws, f"F{rr}", f"=$D${rows['wacc']}+{d}", F_TXTB, nf=NF_PCT, fill=FILL_HDR)
        for gc in gcols:
            f = (f"=(SUMPRODUCT(${G0}${dsc['fcffv']}:${Z}${dsc['fcffv']},1/(1+$F{rr})^${G0}${dsc['t']}:${Z}${dsc['t']})"
                 f"+${Z}${pl['nopat']}*(1+{gc}${r0+3})*(1-{gc}${r0+3}/$D${rows['roic']})/($F{rr}-{gc}${r0+3})/(1+$F{rr})^${Z}${dsc['t']}-$D${rows['netdebt']})/$D${rows['sh']}")
            setc(ws, f"{gc}{rr}", f, F_TXT, nf=(NF_NUM if ccy == "¥" else NF_NUM2))
    rows["grid_center_row"] = r0 + 6
    rows["end"] = max(r, r0 + 8)
    return rows


def write_wiki_block(ws, r0, R, pl, rev_row, ticker, val):
    """Resumo para a wiki — CY24A/CY25A/CY26E/CY27E/CY28E in columns E..I (same year columns), plus EPS and FCF (equity)."""
    Pc = lambda key, c: f"{P}{c}{R[key]}"
    unit = "¥ mi" if ticker == "ADV" else "US$ mi"
    header_row(ws, r0, "Resumo para a wiki | estimativas de casa (CY) — Capstone estimates (house model)")
    label(ws, r0 + 1, f"Receita ({unit})"); row_formula(ws, r0 + 1, lambda i, c, pc: f"={c}{rev_row}", start=1, end=6)
    label(ws, r0 + 2, "Margem bruta"); row_formula(ws, r0 + 2, lambda i, c, pc: f"={c}{pl['gm']}", nf=NF_PCT, start=1, end=6)
    label(ws, r0 + 3, "Margem operacional (EBIT após SBC)"); row_formula(ws, r0 + 3, lambda i, c, pc: f"={c}{pl['ebitm']}", nf=NF_PCT, start=1, end=6)
    if ticker == "ADV":
        label(ws, r0 + 4, "Resultado financeiro (¥ mi)"); row_formula(ws, r0 + 4, lambda i, c, pc: f"={Pc('fin', c)}" if YEARS[i] >= 2026 else f"={Pc('ni_ref', c)}/(1-{Pc('tax', c)})-{c}{pl['ebit']}", start=1, end=6, font=F_LINK)
        label(ws, r0 + 5, "Lucro líquido (¥ mi)"); row_formula(ws, r0 + 5, lambda i, c, pc: f"={Pc('ni_ref', c)}" if YEARS[i] < 2026 else f"=({c}{pl['ebit']}+{c}{r0+4})*(1-{c}{pl['tax']})", start=1, end=6)
        label(ws, r0 + 6, "Ações (mi, média)"); row_formula(ws, r0 + 6, lambda i, c, pc: f"={Pc('sh_ref', c)}" if YEARS[i] < 2026 else f"={Pc('sh', c)}", nf=NF_NUM1, start=1, end=6, font=F_LINK)
        label(ws, r0 + 7, "EPS (¥) | CY23-25 soma dos trimestres reportados", bold=True); row_formula(ws, r0 + 7, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] < 2026 else f"={c}{r0+5}/{c}{r0+6}", nf=NF_NUM2, start=1, end=6, bold=True)
        label(ws, r0 + 8, "EPS ex resultado financeiro não recorrente (¥)"); row_formula(ws, r0 + 8, lambda i, c, pc: f"=({c}{pl['ebit']}+4000)*(1-{c}{pl['tax']})/{c}{r0+6}" if YEARS[i] >= 2026 else None, nf=NF_NUM2, start=3, end=6)
        label(ws, r0 + 9, "FCF equity (¥ mi) = LL + D&A + SBC − ΔNWC − capex"); row_formula(ws, r0 + 9, lambda i, c, pc: f"={c}{r0+5}+{c}{pl['da']}-{c}{pl['sbc']}+{c}{pl['dnwc']}+{c}{pl['capex']}" if YEARS[i] >= 2026 else None, start=3, end=6)
        label(ws, r0 + 10, "Consenso BBG CY (receita / EPS não calendarizado) — memo"); row_formula(ws, r0 + 10, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] >= 2026 else None, start=3, end=6, font=F_LINK)
        label(ws, r0 + 11, "Receita: casa ÷ consenso BBG CY − 1"); row_formula(ws, r0 + 11, lambda i, c, pc: f"={c}{r0+1}/{c}{r0+10}-1" if YEARS[i] >= 2026 else None, nf=NF_PCT, start=3, end=6)
        label(ws, r0 + 12, "P/E implícito ao preço de referência (informativo)"); row_formula(ws, r0 + 12, lambda i, c, pc: f"={P}$D${R['px']}/{c}{r0+7}" if YEARS[i] >= 2025 else None, nf='0.0"x"', start=2, end=6)
    else:
        label(ws, r0 + 4, "Outras receitas + equity method (US$ mi)"); row_formula(ws, r0 + 4, lambda i, c, pc: f"={Pc('fin', c)}+{Pc('affil', c)}" if YEARS[i] >= 2026 else None, start=3, end=6, font=F_LINK)
        label(ws, r0 + 5, "Lucro líquido non-GAAP (US$ mi)"); row_formula(ws, r0 + 5, lambda i, c, pc: f"=({c}{pl['ebit']}+{Pc('fin', c)})*(1-{c}{pl['tax']})+{Pc('affil', c)}" if YEARS[i] >= 2026 else None, start=3, end=6)
        label(ws, r0 + 6, "Ações diluídas (mi, média) | CY24-25 10-K"); row_formula(ws, r0 + 6, lambda i, c, pc: f"={Pc('sh', c)}" if YEARS[i] >= 2026 else {2024: 163.3, 2025: 159.7}.get(YEARS[i]), nf=NF_NUM1, start=1, end=6, font=F_LINK)
        label(ws, r0 + 7, "EPS non-GAAP (US$) | CY23-25 reportado", bold=True); row_formula(ws, r0 + 7, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] < 2026 else f"={c}{r0+5}/{c}{r0+6}", nf=NF_NUM2, start=1, end=6, bold=True)
        label(ws, r0 + 8, "EPS | iniciação 2026-09-16 (memo)"); row_formula(ws, r0 + 8, lambda i, c, pc: f"={Pc('init_eps', c)}" if YEARS[i] >= 2026 else None, nf=NF_NUM2, start=3, end=6, font=F_LINK)
        label(ws, r0 + 9, "FCF equity (US$ mi) = LL + D&A + SBC − ΔNWC − capex"); row_formula(ws, r0 + 9, lambda i, c, pc: f"={c}{r0+5}+{c}{pl['da']}-{c}{pl['sbc']}+{c}{pl['dnwc']}+{c}{pl['capex']}" if YEARS[i] >= 2026 else None, start=3, end=6)
        label(ws, r0 + 10, "Consenso BBG (receita) — memo"); row_formula(ws, r0 + 10, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] >= 2026 else None, start=3, end=6, font=F_LINK)
        label(ws, r0 + 11, "EPS: casa ÷ consenso BBG − 1"); row_formula(ws, r0 + 11, lambda i, c, pc: f"={c}{r0+7}/{Pc('eps_ref', c)}-1" if YEARS[i] >= 2026 else None, nf=NF_PCT, start=3, end=6)
        label(ws, r0 + 12, "P/E implícito ao preço de referência (informativo)"); row_formula(ws, r0 + 12, lambda i, c, pc: f"={P}$D${R['px']}/{c}{r0+7}" if YEARS[i] >= 2025 else None, nf='0.0"x"', start=2, end=6)
    note(ws, r0 + 14, "A tabela 'Capstone estimates (house model)' da página wiki (_wiki/<TICKER>.md) é transcrita deste bloco (CY24A-CY28E). Thesis-drift: ao mudar um número, mover o antigo para o Changelog da página.")
    return r0


if __name__ == "__main__":
    import sys; sys.path.insert(0, OUT)
    from ate_replica import replica
    adv_path = os.path.join(OUT, "Template DCF ADVANTEST.xlsx")
    ter_path = os.path.join(OUT, "Template DCF TER.xlsx")
    # pass 1: placeholders for the cross-model rows, replica each side, then pass 2 with the real numbers
    meta_a = build_advantest(adv_path, [None] * 6)
    out_a, _ = replica(adv_path, "ADV", meta_a["R"])
    adv_us = [round(out_a[y]["soc_us"] + out_a[y]["mem_us"], 1) for y in range(2023, 2029)]
    meta_t = build_ter(ter_path, adv_us)
    out_t, _ = replica(ter_path, "TER", meta_t["R"])
    ist = {2023: 0, 2024: 0, 2025: 129.2, 2026: 230, 2027: 245, 2028: 290}
    ter_us = [round(out_t[y]["semi"] - ist[y], 1) for y in range(2023, 2029)]
    meta_a = build_advantest(adv_path, ter_us)
    json.dump({"adv": meta_a, "ter": meta_t, "adv_us": adv_us, "ter_us": ter_us}, open(os.path.join(OUT, "layout.json"), "w"), indent=1, default=str)
    print("built", adv_path, ter_path)
    print("adv_us", adv_us); print("ter_us", ter_us)
    for tk, o in (("ADV", out_a), ("TER", out_t)):
        for y in (2025, 2026, 2027, 2028):
            print(tk, y, {k: round(o[y][k], 1) for k in ("tam", "rev", "ebit") if k in o[y]}, "eps", round(o[y].get("eps", 0), 2))
