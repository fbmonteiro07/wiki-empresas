# -*- coding: utf-8 -*-
"""Template DCF CRWV.xlsx — official CoreWeave model in the 'Template DCF <TICKER>.xlsx' family (AMD/AVGO/ADV/TER convention).
Driver: active IT-load power (MW) -> billable power (1-quarter lag) x realised revenue per GW-year -> adj. EBITDA -> D&A per GW
-> EBIT -> NOPAT; capex = growth (build cost per GW, with a pre-build share of next year's adds) + replacement (adds of t-life
at a replacement share of the current build cost); FCFF -> DCF (WACC x g grid) + a second grid revenue/GW x EBITDA margin
(Excel Data Table created by COM in recalc_verify.py). Sheets: Capa DCF - Base, Premissas e fontes, Historico, Divida.
openpyxl writes formulas only; Excel COM recalculates. Rule: no TEXT cell may start with '='.
"""
import datetime as dt, os, json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2023, 2046))
COLS = [get_column_letter(4 + i) for i in range(len(YEARS))]   # D..Z
BASE = {2023, 2024, 2025}
P = "'Premissas e fontes'!"
NY = len(YEARS)

F_TITLE = Font(name="Arial", size=16, bold=True, color="FF203864")
F_TXT = Font(name="Arial", size=10, color="FF202020")
F_TXTB = Font(name="Arial", size=10, bold=True, color="FF202020")
F_NOTE = Font(name="Arial", size=9, color="FF666666")
F_INPUT = Font(name="Arial", size=10, color="FF0000FF")
F_LINK = Font(name="Arial", size=10, color="FF008000")
F_RES = Font(name="Arial", size=12, bold=True, color="FFFFFFFF")
FILL_HDR = PatternFill("solid", fgColor="FFDCE6F1")
FILL_ASSUM = PatternFill("solid", fgColor="FFFFF2CC")
FILL_RES = PatternFill("solid", fgColor="FF203864")
FILL_EST = PatternFill("solid", fgColor="FFFCE4D6")      # salmon = ESTIMATE (no source)
NF_NUM = '#,##0;\\(#,##0\\);"-"'
NF_NUM1 = '#,##0.0;\\(#,##0.0\\);"-"'
NF_NUM2 = '0.00;\\(0.00\\);"-"'
NF_PCT = '0.0%;\\(0.0%\\);"-"'
NF_CHK = '0.00;\\(0.00\\);0.00'
NF_DATE = 'dd\\-mmm\\-yyyy'
NF_DATE_S = 'dd\\-mmm\\-yy'
NF_X = '0.0"x";\\(0.0"x"\\);"n/m"'


def setc(ws, addr, value, font=F_TXT, nf=None, fill=None, align=None):
    c = ws[addr]
    c.value = value
    c.font = font
    if nf: c.number_format = nf
    if fill: c.fill = fill
    if align: c.alignment = Alignment(horizontal=align)
    return c


def label(ws, r, text, bold=False, fill=None, col="C"):
    assert not text.startswith("="), text
    setc(ws, f"{col}{r}", text, F_TXTB if bold else F_TXT, fill=fill)


def header_row(ws, r, text, cols=None):
    setc(ws, f"C{r}", text, F_TXTB, fill=FILL_HDR)
    for c in (cols or COLS):
        ws[f"{c}{r}"].fill = FILL_HDR


def note(ws, r, text, col="C"):
    assert not text.startswith("="), text
    setc(ws, f"{col}{r}", text, F_NOTE, align="left")


def year_header(ws, r):
    for i, y in enumerate(YEARS):
        setc(ws, f"{COLS[i]}{r}", f"CY{str(y)[2:]}{'B' if y in BASE else 'E'}", F_TXTB, fill=FILL_HDR, align="center")


def row_formula(ws, r, fn, nf=NF_NUM, font=F_TXT, start=0, end=None, fill=None, bold=False):
    end = NY if end is None else end
    for i in range(start, end):
        c = COLS[i]; pc = COLS[i - 1] if i > 0 else None
        v = fn(i, c, pc)
        if v is None: continue
        f = Font(name="Arial", size=10, bold=True, color=font.color.rgb if font.color else "FF202020") if bold else font
        setc(ws, f"{c}{r}", v, f, nf=nf, fill=fill, align="right")


def setup_sheet(ws, title, units, legend):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2.25; ws.column_dimensions["B"].width = 2.25
    ws.column_dimensions["C"].width = 56
    for c in COLS: ws.column_dimensions[c].width = 12.5
    for r in (1, 2, 5, 7): ws.row_dimensions[r].height = 18
    setc(ws, "C2", title, F_TITLE, align="left")
    setc(ws, "C3", units, F_TXT, align="left")
    setc(ws, "C4", legend, F_NOTE, align="left")
    ws.freeze_panes = "D6"


class Prem:
    def __init__(self, ws, ticker, unit_line):
        self.ws = ws; self.rows = {}
        ws.sheet_view.showGridLines = False
        ws.column_dimensions["A"].width = 2.25; ws.column_dimensions["B"].width = 2.25
        ws.column_dimensions["C"].width = 60
        for c in COLS: ws.column_dimensions[c].width = 12.5
        ws.column_dimensions["AB"].width = 70; ws.column_dimensions["AC"].width = 12.5
        ws.freeze_panes = "D6"
        setc(ws, "C2", f"{ticker} | Premissas e fontes", F_TITLE, align="left")
        setc(ws, "C3", unit_line, F_TXT, align="left")
        setc(ws, "C4", "Azul = dado HARD (filing / consenso); amarelo = premissa PARTIAL (faixa com fonte, ponto é nosso); salmão = ESTIMATE (sem fonte). Fonte na coluna L (tabelas) ou AB (séries).", F_NOTE, align="left")
        for i, y in enumerate(range(2023, 2029)):
            setc(ws, f"{COLS[i]}5", y, F_TXTB, nf="0", fill=FILL_HDR, align="center")
        setc(ws, "L6", "Arquivo, aba e células de origem. CY = ano-calendário (= ano fiscal da CoreWeave).", F_NOTE, align="left")
        self.r = 7

    def ref(self, key, text, vals, src, nf=NF_NUM, font=F_INPUT, fill=None):
        r = self.r; self.rows[key] = r
        label(self.ws, r, text)
        for i, v in enumerate(vals):
            if v is None: continue
            if isinstance(v, str) and v.startswith("="):
                setc(self.ws, f"{COLS[i]}{r}", v, F_TXT, nf=nf, align="right")
            else:
                setc(self.ws, f"{COLS[i]}{r}", v, font, nf=nf, fill=fill, align="right")
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


# ===================================================================================================== inputs (US$ mm)
# --- reported (10-K FY25 2026-03-02; 10-Q 2Q26 2026-08-12) ---
REV = {2023: 229, 2024: 1915, 2025: 5131}
CONS = {"rev": {2026: 12770.37, 2027: 26439.52, 2028: 42212.08}, "ebitda": {2026: 7482.66, 2027: 16630.37, 2028: 27896.76},
        "ebit": {2026: 1004.25, 2027: 4113.10, 2028: 7363.56}, "ni": {2026: -2197.83, 2027: -1132.69, 2028: 974.96},
        "eps": {2026: -3.92, 2027: -2.09, 2028: 1.431}, "capex": {2026: 35670.67, 2027: 47897.41, 2028: 50387.97}}
PX, PT_CONS, MKTCAP = 77.81, 139.77, 43485.6
ADDS_IN = {2026: 1050, 2027: 1300, 2028: 1500, 2029: 1600, 2030: 1700, 2031: 1400, 2032: 1200, 2033: 1000, 2034: 900, 2035: 800}
REVGW = fill_years({2027: 12.0, 2028: 12.5, 2029: 12.8, 2030: 13.0, 2031: 13.3, 2032: 13.7}, 2033, 14.0)
EBITDA_M = fill_years({2026: 0.575, 2027: 0.62, 2028: 0.64, 2029: 0.64, 2030: 0.63}, 2031, 0.62)
DA_GW = fill_years({2026: 4.6, 2027: 4.8}, 2028, 5.0)
SBC = fill_years({2026: 0.05, 2027: 0.03, 2028: 0.025}, 2029, 0.02)
TAX = fill_years({2026: 0.05, 2027: 0.05, 2028: 0.05, 2029: 0.10, 2030: 0.15}, 2031, 0.21)
BUILD = fill_years({2026: 33.0, 2027: 38.0}, 2028, 40.0)
NWC = fill_years({2026: -0.70, 2027: -0.55, 2028: -0.45, 2029: -0.40}, 2030, -0.35)
KD = fill_years({2026: 0.095}, 2027, 0.09)
SH = fill_years({}, 2026, 580.0)


def build(path):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Capa DCF - Base"
    wp = wb.create_sheet("Premissas e fontes")
    wh = wb.create_sheet("Histórico")
    wd = wb.create_sheet("Dívida")
    pr = Prem(wp, "CRWV", "Dados extraídos das fontes indicadas. US$ milhões salvo indicação; potência em MW (carga crítica de TI, base da companhia); receita/GW e custo de build em US$ bilhões por GW. Ano fiscal = ano-calendário.")

    # ------------------------------------------------------------------ reference tables (2023..2028 in D..I)
    pr.section("Histórico reportado (10-K FY25, 10-Q 2Q26) e consenso BBG (2026-10-13)")
    pr.ref("rev_ref", "Receita (US$ mi) | 10-K FY23-25 / consenso BBG CY26-28", [REV[2023], REV[2024], REV[2025], CONS["rev"][2026], CONS["rev"][2027], CONS["rev"][2028]],
           "10-K FY25 (CRWV/CRWV_10-K_2026-03-02): 229 / 1.915 / 5.131. CY26-28: _wiki/_data/estimates.json CRWV CY2026 / CY2027 / 3FY (BEst 2026-10-13; 47 analistas, 33 buy / 10 hold / 4 sell).")
    pr.ref("ebitda_ref", "EBITDA ajustado (US$ mi) | companhia / consenso", [None, 1226, 3098, CONS["ebitda"][2026], CONS["ebitda"][2027], CONS["ebitda"][2028]],
           "FY24: 64% de margem (DB CRWV unit economics 2025-06-16) x 1.915 = 1.226 (PARTIAL). FY25 = soma dos trimestres: 1Q25 ~609 (1Q26 ~1.164 = 56% x 2.078, '+91% y/y', call 2026-05-07 — PARTIAL) + 2Q 753 + 3Q 838 + 4Q 898 (calls). CY26-28 BEst EBITDA.")
    pr.ref("aoi_ref", "Lucro operacional ajustado (AOI, US$ mi) | consenso EBIT CY26-28", [None, None, None, CONS["ebit"][2026], CONS["ebit"][2027], CONS["ebit"][2028]],
           "BEst EBIT (estimates.json). Guia FY26 (call 2026-08-11): AOI $960-1.150 mi; 3Q26 $200-260 mi.")
    pr.ref("ni_ref", "Lucro líquido GAAP (US$ mi) | 10-K / consenso", [-594, -863, -1167, CONS["ni"][2026], CONS["ni"][2027], CONS["ni"][2028]], "10-K FY25 (net loss); BEst NI CY26-28.")
    pr.ref("eps_ref", "EPS GAAP diluído (US$) | 10-K / consenso", [-3.09, -4.30, -2.81, CONS["eps"][2026], CONS["eps"][2027], CONS["eps"][2028]],
           "10-K FY25 p.1508: net loss per share atribuível aos acionistas, diluído: (3,09) / (4,30) / (2,81) (método two-class; pós split 20:1 de mar-25). CY26-28 BEst EPS (ex-SBC).", nf=NF_NUM2)
    pr.ref("da_ref", "Depreciação e amortização (US$ mi)", [103, 863, 2454, 2540], "10-K cash-flow FY23-25; 1H26 = 2.540 (10-Q 2Q26). Coluna 2026 = 1H26 (memo).")
    pr.ref("sbc_ref", "Stock-based compensation (US$ mi)", [15, 31, 630, 318], "10-K cash-flow (FY25 inclui $177 mi de RSUs vestidas no IPO); 1H26 = 318 (memo).")
    pr.ref("capex_ref", "Capex caixa (US$ mi) | 10-K / consenso BBG CY26-28", [2943, 8702, 10309, CONS["capex"][2026], CONS["capex"][2027], CONS["capex"][2028]],
           "10-K 'Purchase of property and equipment' 2.943 / 8.702 / 10.309 (FY25 base da companhia ~$14 bi incl. OEM financing: guia 3Q25 $12-14 bi). CY26-28 BEst capex. Guia FY26 (base companhia): $35-39 bi.")
    pr.ref("int_ref", "Despesa financeira líquida (US$ mi)", [28, 361, 1229, 1176], "10-K FY23-25; 1H26 = 1.176 (10-Q 2Q26). Guia 3Q26: $860-940 mi.")
    pr.ref("power_ye", "Potência ativa no fim do ano (MW, carga de TI)", [70, 360, 850, 1500], "10-K FY25 p.194: ~70 MW (dez-23), ~360 MW (dez-24), >850 MW (dez-25). Coluna 2026 = jun-26: 1,5 GW (call 2026-08-11). Guia YE26: >1,85 GW.")
    pr.ref("contracted", "Potência contratada (MW)", [None, None, 3100, 4200], "10-K FY25: ~3,1 GW (dez-25). Call 2026-08-11: 3,7 GW no 2Q, 4,2 GW em 11-ago-26 (coluna 2026). Alvo: >=8 GW ativos em 2030.")
    pr.ref("rpo_ref", "RPO não satisfeita (US$ mi)", [None, None, 60700, 103700], "10-K FY25: $60,7 bi (43% em 24 meses). 10-Q 2Q26: $103,7 bi, 41% nos 24 meses até jun-28, 39% meses 25-48, saldo meses 49-78. Backlog (métrica da companhia): $66,8 bi dez-25 / $104 bi jun-26.")
    pr.ref("defrev", "Receita diferida total (US$ mi) | dez-24 / dez-25 / jun-26", [None, 4064, 8185, 9692], "10-K FY25 balanço (769+3.295; 1.709+6.476); 10-Q 2Q26 (2.686+7.006). Pré-pagamentos de clientes = 15-25% do TCV (UBS 2026-09-22).")
    pr.ref("ar", "Contas a receber (US$ mi) | dez-24 / dez-25 / jun-26", [None, 417, 3169, 2541], "10-K FY25; 10-Q 2Q26.")
    pr.ref("cash_ref", "Caixa e equivalentes (US$ mi) | dez-24 / dez-25 / jun-26", [None, 1361, 3127, 5524], "10-K FY25; 10-Q 2Q26. Caixa restrito adicional: 1.003 (dez-25: 819 + 184) / 1.380 (jun-26: 873 + 507) — cobertura de serviço da dívida, excluído do caixa líquido.")
    pr.ref("debt_ref", "Dívida bruta, principal (US$ mi) | dez-24 / dez-25 / jun-26", [None, 7926, 21615, 35551], "10-K FY25 nota 10 (dez-24 valor contábil 7.926; dez-25 contábil 21.373 + desconto 242 = 21.615). 10-Q 2Q26 nota 10: principal total 35.551 (recourse + non-recourse). Ver aba Dívida.")
    pr.ref("leases_ref", "Passivo de arrendamento operacional (US$ mi) | dez-24 / dez-25 / jun-26", [None, 2602, 8195, 16319], "10-K FY25; 10-Q 2Q26 (taxa 10%, prazo 12 anos). Mais $35,5 bi de arrendamentos não iniciados (jun-26). Aluguel está no EBITDA — NÃO entra na dívida líquida.")

    pr.section("Guidance FY26 (call 2Q26, 2026-08-11) — base da companhia")
    pr.single("g_rev_lo", "Receita FY26 — piso (US$ mi)", 12400, "Call 2026-08-11: $12,4-13,2 bi (elevado de $12,0-13,0 bi em fev-26).", fill=None)
    pr.single("g_rev_hi", "Receita FY26 — teto (US$ mi)", 13200, "Idem.", fill=None)
    pr.single("g_aoi_lo", "AOI FY26 — piso (US$ mi)", 960, "Call 2026-08-11: $960-1.150 mi (de $900-1.100 mi).", fill=None)
    pr.single("g_aoi_hi", "AOI FY26 — teto (US$ mi)", 1150, "Idem.", fill=None)
    pr.single("g_capex_lo", "Capex FY26 — piso (US$ mi, base companhia)", 35000, "Call 2026-08-11: $35-39 bi (de $31-35 bi). 1H26 reportado: 6,8 + 9,4 = $16,2 bi (caixa: 14,1).", fill=None)
    pr.single("g_capex_hi", "Capex FY26 — teto (US$ mi)", 39000, "Idem.", fill=None)
    pr.single("g_power_ye", "Potência ativa YE26 — guia (MW)", 1850, "Call 2026-08-11: '>1,85 GW' (de >1,7 GW). UBS 09-22: 1.900 MW FY26E, 3.200 FY27E, 4.720 FY28E, 6.320 FY29E, 8.000 FY30E.", fill=None)
    pr.single("g_q3_rev", "Receita 3Q26 — ponto médio (US$ mi)", 3525, "Call 2026-08-11: $3,45-3,60 bi; AOI 3Q $200-260 mi; juros 3Q $860-940 mi; capex 3Q $11,5-13,5 bi.", fill=None)
    pr.single("h1_rev", "Receita 1H26 reportada (US$ mi)", 4653, "10-Q 2Q26: 2.078 + 2.575.", fill=None)
    pr.single("h1_aoi", "AOI 1H26 reportado (US$ mi)", 149, "Calls: 1Q26 $21 mi + 2Q26 $128 mi.", fill=None)
    pr.single("bill_2026", "Potência faturável média 2026 (MW) — cálculo trimestral", 1124, "Média de 4 trimestres da potência ativa média do trimestre ANTERIOR (UBS 09-22: 'it takes about a quarter for active power to generate revs'): 1Q (590+850)/2=720; 2Q (850+1.000)/2=925; 3Q (1.000+1.500)/2=1.250; 4Q (1.500+1.700)/2=1.600 (3Q26 YE estimado 1.700). Média 1.124. Substitui a fórmula anual em 2026 (adições concentradas no 1H).", fill=FILL_ASSUM)

    pr.section("Marcas de receita por GW (US$ bi por GW de TI por ANO) — ledger da wiki, NÃO somar bases diferentes")
    pr.single("m_ubs", "Realizada no livro instalado (UBS, 09-22)", 11.0, "UBS Keirstead 2026-09-22: 2Q26 $2,575 bi x4 / 925 MW médios do 1Q26 = ~$11 bi/GW; 'closer to $15 bn by end of 2027'. Este modelo: 2026 implícito pelo guia = ~11,4.", nf=NF_NUM1, fill=None)
    pr.single("m_mgmt", "Piso para novos contratos longos (4-6 anos) — gestão", 15.5, "Nick Robbins (VP Corp Dev) @ BTG Pactual, 2026-09-21: mid-teens $/W/ano é 'the absolute floor'; Vera Rubin longo 'clearing higher'. Fonte vendedora, não auditada.", nf=NF_NUM1, fill=None)
    pr.single("m_nscale", "Livro filado da Nscale (S-1 2026-09-18) — blended / tranche VR", 13.2, "Nscale S-1: $103,4 bi TCV / 5,7 anos / 1,37 GW TI = ~$13,2 bi/GW-ano; tranche Anthropic Vera Rubin ~$16,2 bi. Lido pela wiki como TETO do livro contratado (conflito aberto com a gestão).", nf=NF_NUM1, fill=None)
    pr.single("m_short", "Contratos curtos (3-6 meses) — anualizado", 40.0, "Robbins 09-21: 'about $40 million a megawatt' em contratos curtos de gerações ANTERIORES (Blackwell / Grace Blackwell), sem prazo nem base temporal ditos; JPM 09-24 repete o print sem base; só a UBS 09-22 dá o prazo (3-6 meses) e a base anualizada ($40 bi/GW). Fatia pequena do livro. Arete 08-21: $20-25 mi/MW em contratos de 2-3 anos.", nf=NF_NUM1, fill=None)
    pr.single("m_ratio", "Receita / capex em contrato de 5 anos (gestão)", 2.0, "Robbins 09-21: 'historically… two to one ratio for a five-year deal between revenue and capex', 'expanded' desde o início de 2026. 2:1 em 5 anos sobre $40 bi/GW = $16 bi/GW-ano.", nf=NF_NUM1, fill=None)
    pr.single("m_hedgeye", "Memo bear: monetização por MW conectado não melhorou em 2025 (Hedgeye, dez-25)", 0, "HE Global Technology BB, dez-2025 (short desde abr-25). Calibração trimestral deste modelo: 2Q25 ~12,4 → 2Q26 ~11,1 US$ bi/GW (aba Histórico) — a receita por GW instalado CAIU enquanto a frota escalou.", nf=NF_NUM1, fill=None, font=F_NOTE)

    pr.section("Custo de construção por GW (capex da CoreWeave, que arrenda o shell) — US$ bi / GW de TI")
    pr.single("c_ubs_bw", "Blackwell — UBS", 35.0, "UBS 09-22: 'capex to CoreWeave might be closer to $35 bn per Blackwell-based GW and $40 bn per Vera Rubin-based GW' (Crusoe all-in $57 bi/GW, $30 bi em GPUs).", nf=NF_NUM1, fill=None)
    pr.single("c_ubs_vr", "Vera Rubin — UBS", 40.0, "Idem. Arete 08-21: racks VR NVL72 70-80% mais caros que Blackwell, ~+20% capex de GPU por MW.", nf=NF_NUM1, fill=None)
    pr.single("c_back", "Check retrospectivo: capex 2024-26 / 1,85 GW", 34.0, "UBS: $62 bi de capex 2024-26 para 1,85 GW em YE26 = $34 bi/GW ('flattered' — parte do capex de 2026 compra capacidade de 2027). Base de calibração da parcela pré-construída.", nf=NF_NUM1, fill=None)

    pr.section("Valuation e balanço")
    pr.single("val_date", "Data de valuation", dt.datetime(2026, 6, 30), "Igual à data-base do balanço (30-jun-26). DESVIO da convenção da família (27-ago-26): com queima de ~$26 bi/ano, valorar em ago com dívida líquida de jun deixaria ~$5,6 bi de caixa queimado em jul-ago fora da ponte (~−$9/ação; double-check 2026-10-14). Atualizar os dois juntos no 10-Q 3Q26.", nf=NF_DATE)
    pr.single("wacc", "WACC", 0.10, "Convenção da família (10%), mantida para comparabilidade — mas para a CRWV é um SUBSÍDIO: sem escudo fiscal (NOLs; imposto caixa 5% até 2028) Kd 10% x 65% + Ke 14% x 35% = 11,4%; a pesos de mercado (dívida líquida 30 bi vs market cap 43 bi) 12-13%. Arete 11%; Redburn Ke 20%. Ver grade WACC x g: 11% e 12% são a leitura honesta.", nf=NF_PCT)
    pr.single("g", "Crescimento terminal", 0.02, "Template DCF NVDA.xlsx | Capa DCF - Base!D91.", nf=NF_PCT)
    pr.single("roic", "ROIC incremental terminal", 0.08, "ESTIMATE. Template usa 20%; aqui 8% porque 1 GW novo custa ~$40 bi e gera NOPAT ~$2-3 bi (5-7% bruto). Ver linha 'ROIC incremental implícito' na capa. Sensibilidade na grade.", nf=NF_PCT, fill=FILL_EST)
    pr.single("shares", "Ações diluídas (mi) | 551 em circulação + 29 RSUs + 23,4 opções (treasury)", 603.4, "10-Q 2Q26: 457 mi classe A + 94 mi classe B (30-jun-26); 29 mi RSUs/RSAs não vestidas; 24 mi opções a $1,84 (valor intrínseco $2.341 mi) → treasury a $77,81 = 23,4 mi. Conversíveis fora do dinheiro (2031: $107,80 / cap $215,60; 2032: $119,60 / cap $230) ficam na dívida. Sem ATM (gestão 09-21: 'not at these prices').", nf=NF_NUM1, fill=None)
    pr.single("cash", "Caixa + títulos, não restrito (US$ mi, 30-jun-26)", 5539, "10-Q 2Q26: caixa 5.524 + títulos 15. Caixa restrito 1.380 excluído (cobertura obrigatória de juros/principal das DDTLs).", nf=NF_NUM1, fill=None)
    pr.single("debt", "Dívida financeira bruta, principal (US$ mi, 30-jun-26)", 35772, "10-Q 2Q26 nota 10: principal 35.551 (DDTLs, senior notes, conversíveis, OEM financing, Magnetar) + arrendamentos financeiros 221. Arrendamentos operacionais (16.319) NÃO somados: aluguel já está no EBITDA.", nf=NF_NUM1, fill=None)
    pr.single("bs_date", "Data-base do balanço no modelo", dt.datetime(2026, 6, 30), "Anterior à data de valuation; atualizar no 10-Q 3Q26.", nf=NF_DATE, fill=None)
    pr.single("px", "Preço de referência (US$, informativo)", PX, "BBG PX_LAST CRWV US, 2026-10-13 (estimates.json). Não entra no valuation.", nf=NF_NUM2, fill=None)
    pr.single("pt_cons", "PT médio consenso (US$, informativo)", PT_CONS, "BBG BEST_TARGET_PRICE, 47 analistas (hi 278 / lo 39), 2026-10-13. UBS Buy $120; JPM OW $125; Bernstein UP $74; Redburn Sell $54; Arete Buy $317.", nf=NF_NUM2, fill=None)
    pr.single("mktcap", "Market cap (US$ mi, informativo)", MKTCAP, "BBG 2026-10-13.", nf=NF_NUM, fill=None)
    pr.single("nd_2025", "Dívida líquida dez-25 (US$ mi) — âncora do roll de dívida", 18488, "Principal 21.615 − caixa 3.127 (10-K FY25). Usada só no bloco memo de dívida/EPS, não no DCF.", nf=NF_NUM, fill=None)
    pr.single("eq_2026", "Equity captado em 2026 (US$ mi, líquido de cap calls)", 2490, "10-Q 2Q26 cash-flow: private placements 2.982 (NVDA $2 bi a $87,20 em jan-26 + Jane Street $1 bi) − cap calls 492. Sem ATM assumido no 2H26.", nf=NF_NUM, fill=None)
    pr.single("lag", "Defasagem potência ativa → faturamento (anos)", 0.25, "UBS 09-22: ~1 trimestre (instalação/teste de GPUs ~6 semanas após energizar). Faturável média do ano = YE anterior + (0,5 − lag) x adições (adições uniformes).", nf=NF_NUM2)
    pr.single("prebuild", "Parcela do capex do ano que compra capacidade do ano SEGUINTE", 0.20, "Calibrado: guia FY26 $37 bi (mid) vs fórmula 33 x (0,8 x 1,05 GW + 0,2 x 1,3 GW) = 36,3 (−1,9%; o build do ano corrente precifica também a parcela pré-construída). UBS: check retrospectivo 'flattered' pelo capex de 2026 que compra 2027.", nf=NF_PCT)
    pr.single("life", "Vida útil para reposição (anos) — ENTRADA NA CAPA F6 (memo)", "='Capa DCF - Base'!F6", "Depreciação de GPUs da CoreWeave: 6 anos (10-K; MS AI Factories). Reposição em t = adições de t−6. Re-contratação em anos 5-6 a 50-75% do ASP (DB 2025-06-16) é o lado otimista — sensibilizar 8 anos.", nf="0", fill=None, font=F_LINK)
    pr.single("repl", "Custo de reposição (% do custo de build do ano) — ENTRADA NA CAPA G6 (memo)", "='Capa DCF - Base'!G6", "ESTIMATE: o shell é arrendado; troca-se GPU/servidor/rede (~80% do capex), mantém-se parte da MEP/fit-out.", nf=NF_PCT, fill=None, font=F_LINK)
    pr.single("g_fleet", "Crescimento da frota após 2035 (% do YE anterior)", 0.03, "ESTIMATE: adições = 3% da potência ativa do ano anterior a partir de 2036.", nf=NF_PCT, fill=FILL_EST)

    pr.section("Premissas por ano (CY)")
    pr.year_hdr()
    adds = {y: ADDS_IN[y] for y in ADDS_IN}
    pr.series("adds", "Adições de potência ativa (MW, carga de TI)", adds, "2026: +1.050 → YE 1.900 (guia >1.850; UBS 1.900; 1,5 GW já em jun-26). 2027-30: 1.300 / 1.500 / 1.600 / 1.700 → 3,2 / 4,7 / 6,3 / 8,0 GW = caminho UBS 09-22 ao alvo de ≥8 GW em 2030 (gestão). Contratada 4,2 GW + 1,5 GW powered land = ~6 GW visíveis (call 08-11). 2031-35 ESTIMATE: desacelera para 800 MW/ano; 2036+ fórmula (g_fleet).", nf=NF_NUM, hard_fill=FILL_ASSUM)
    for y in range(2031, 2036):
        wp[f"{COLS[YEARS.index(y)]}{pr.rows['adds']}"].fill = FILL_EST
    pr.series("revgw", "Receita por GW faturável (US$ bi / GW-ano), base", REVGW, "2026 implícito pelo guia = 12.800 / 1.124 MW = ~11,4 (capa). 2027 12,0 → 2030 13,0: blend do livro legado (~11) com novos contratos longos a mid-teens (gestão 09-21; Nscale 13,2-16,2) e fatia curta a ~40. UBS: ~15 no EXIT de 2027; alvo UBS 2030 $85 bi / ~6,7 GW faturáveis = 12,7. 2031-33 sobe a 14,0 e fica flat nominal: o livro legado (2025-26, ~2 GW a ~11) é re-contratado e a frota passa a ser majoritariamente vintages 2027+ contratados a >=15; 14,0 fica ABAIXO de todas as marcas forward (piso gestão 15-16, Nscale VR 16,2, UBS 15 no exit-27). PARTIAL.", nf=NF_NUM1)
    pr.series("ebitda_m", "Margem EBITDA ajustada", EBITDA_M, "2026 57,5%: 1H 57,6% (2,71 bi / 4,65) + 2H implícito (AOI guia 1.055 − 149 + D&A ~3,6 bi) ≈ 56%; consenso 58,6%. 2027-28 62/64% (consenso 62,9/66,1%). LT 62%: entre o nível contratual mid-70s (gestão) e o alvo de longo prazo de 25-30% de margem operacional (call 4Q25) após D&A. Aluguel de DC (arrendamento) e overhead estão aqui.", nf=NF_PCT)
    pr.series("da_gw", "D&A por GW ativo médio (US$ bi / GW-ano)", DA_GW, "Calibrado: FY25 2.454 / 605 MW médios = 4,1; 1H26 anualizado 5.080 / ~1.090 MW = 4,7. VR a $40 bi/GW com vida mista 6-15 anos → ~5,0-5,5. 5,0 flat (PARTIAL). Afeta EBIT/EPS, não o FCFF (só via imposto).", nf=NF_NUM1)
    pr.series("sbc", "SBC / receita (deduzido do EBIT após SBC)", SBC, "FY25 12,3% (inclui $177 mi do IPO); 1H26 6,8%. 5% → 2% LT. AOI da companhia EXCLUI SBC; o FCFF aqui deduz.", nf=NF_PCT)
    pr.series("tax", "Alíquota de imposto caixa sobre EBIT", TAX, "NOLs >$3 bi (DB 2025-06-16); provisão GAAP positiva em prejuízo (146 mi no 1H26 — estados/exterior). 5% até 2028, 21% a partir de 2031.", nf=NF_PCT)
    pr.series("build", "Custo de build por GW adicionado (US$ bi / GW)", BUILD, "2026 33 (Blackwell; UBS 35 / check retrospectivo 34), 2027 38, 2028+ 40 (Vera Rubin, UBS). Flat nominal após 2028: inflação de memória/rack vs ganhos de densidade. PARTIAL.", nf=NF_NUM1)
    pr.series("nwc", "NWC operacional / receita = (recebíveis − receita diferida) / receita", NWC, "Dez-25: (3.169 − 8.185) / 5.131 = −98%; jun-26: (2.541 − 9.692) / LTM 7.590 = −94%. Pré-pagamentos (15-25% do TCV) escalam com bookings, não com receita: a razão comprime para −35% até 2030 (ESTIMATE — única âncora é o % de pré-pagamento). Entrada de caixa = 35-70% do incremento de receita; UBS implica entradas bem maiores (dívida líquida 12/27E $56,5 bi vs ~$80 bi aqui).", nf=NF_PCT, hard_fill=FILL_EST)
    pr.series("kd", "Custo médio da dívida (memo, bloco de dívida/EPS)", KD, "10-Q 2Q26: taxas efetivas 9-11% (DDTLs 9-15%, notes 9-10%, DDTL 4.0 7%, conversíveis 2%). 1H26 juros 1.176 / dívida média ~29 bi = 8,1% + capitalizado. UBS: cada 100 bp = ~$30 mi/trimestre.", nf=NF_PCT)
    pr.series("sh", "Ações diluídas para EPS (mi, média do ano)", SH, "580 flat: sem ATM, SBC líquida ~1%/ano ignorada. Conversível 2032 só dilui acima de ~$200 (cap call).", nf=NF_NUM1)

    pr.text("")
    pr.text("Método: receita = potência faturável média (YE anterior + (0,5 − lag) x adições; 2026 pelo cálculo trimestral) x receita por GW. EBITDA = receita x margem. D&A = potência ativa média x D&A/GW. FCFF = (EBITDA − D&A − SBC) x (1 − imposto) + D&A − capex − variação de NWC.")
    pr.text("Capex = crescimento [custo de build x ((1 − pré-construção) x adições do ano + pré-construção x adições do ano seguinte)] + reposição [potência instalada em t−vida (adições E reposições anteriores) x custo de build x % reposição — em regime, reposição ≈ frota ÷ vida]. 2023-25 = capex caixa reportado; 2026 = guia (ponto médio).")
    pr.text("Terminal: NOPAT x (1 + g) x (1 − g / ROIC). Desconto de fim de ano; CY26 proporcional aos dias após a data de valuation. Dívida líquida = principal + arrendamentos financeiros − caixa não restrito (30-jun-26).")
    pr.text("Bases de GW: TODA potência da CoreWeave é carga crítica de TI (UBS 09-22) — não comparar com GW de instalação (10-25% maior; Galaxy Helios 526 MW TI = 800 MW brutos). Receita/GW, custo de build/GW e D&A/GW são três bases distintas — nunca netar.")
    pr.text("Fontes primárias: 10-K FY25 (2026-03-02), 10-Qs 1Q25-2Q26, calls 2Q25-2Q26 (CRWV/transcripts), BTG Pactual websession com Nick Robbins 2026-09-21 (Capstone notes). Sell-side: UBS 09-22, JPM 09-24, Arete 08-21, Bernstein 07-01/09-24, DB 2025-06-16, Redburn 09-21. Consenso BBG 2026-10-13.")

    R = pr.rows
    Pc = lambda key, c: f"{P}{c}{R[key]}"
    Ps = lambda key: f"{P}$D${R[key]}"

    # ================================================================================================= Capa
    setup_sheet(ws, "CRWV | DCF por potência (GW de TI x receita por GW)",
                "US$ milhões, salvo potência (MW), receita/GW, custo de build/GW e D&A/GW (US$ bilhões por GW) e ações (milhões). Horizonte CY2023–2045; ano fiscal = ano-calendário.",
                "Azul / amarelo: premissas (aba Premissas e fontes; salmão = sem fonte). Verde: fontes internas. CY23–25B: bases reportadas (10-K). 2026: guia da companhia.")
    year_header(ws, 5)
    label(ws, 6, "Entradas das grades: D6 multiplicador receita/GW 2027+ (1,00 = base) | E6 ajuste margem EBITDA 2027+ (p.p.) | F6 vida útil p/ reposição (anos) | G6 custo de reposição (% do build)")
    setc(ws, "D6", 1.0, F_INPUT, nf=NF_NUM2, fill=FILL_ASSUM, align="right"); setc(ws, "E6", 0.0, F_INPUT, nf='+0.0%;-0.0%;0.0%', fill=FILL_ASSUM, align="right")
    setc(ws, "F6", 6, F_INPUT, nf='0" anos"', fill=FILL_ASSUM, align="right"); setc(ws, "G6", 0.80, F_INPUT, nf=NF_PCT, fill=FILL_EST, align="right")

    header_row(ws, 7, "Capacidade | potência ativa (carga crítica de TI, MW) e potência faturável")
    label(ws, 8, "Potência ativa no fim do ano (MW)")
    row_formula(ws, 8, lambda i, c, pc: f"={Pc('power_ye', c)}" if YEARS[i] in BASE else f"={pc}8+{c}9", nf=NF_NUM)
    for i in range(3): ws[f"{COLS[i]}8"].font = F_LINK
    label(ws, 9, "Adições de potência ativa no ano (MW)")
    row_formula(ws, 9, lambda i, c, pc: (f"={c}8" if i == 0 else f"={c}8-{pc}8") if YEARS[i] in BASE else (f"={Pc('adds', c)}" if YEARS[i] <= 2035 else f"={pc}8*{Ps('g_fleet')}"), nf=NF_NUM)
    for i in range(3, NY): ws[f"{COLS[i]}9"].font = F_LINK
    label(ws, 10, "Potência ativa média do ano (MW) — base do D&A")
    row_formula(ws, 10, lambda i, c, pc: f"=({pc}8+{c}8)/2", nf=NF_NUM, start=1)
    label(ws, 11, "Potência faturável média (MW) = YE anterior + (0,5 − lag) x adições | 2026: cálculo trimestral")
    row_formula(ws, 11, lambda i, c, pc: f"={Ps('bill_2026')}" if YEARS[i] == 2026 else f"={pc}8+(0.5-{Ps('lag')})*{c}9", nf=NF_NUM, start=1)
    ws["G11"].font = F_LINK
    label(ws, 12, "Receita por GW faturável (US$ bi / GW-ano) | CY24-26 implícita")
    row_formula(ws, 12, lambda i, c, pc: f"={c}15/{c}11" if YEARS[i] <= 2026 else f"={Pc('revgw', c)}*$D$6", nf=NF_NUM1, start=1)
    for i in range(4, NY): ws[f"{COLS[i]}12"].font = F_LINK
    label(ws, 13, "Memo: receita por GW ATIVO médio (US$ bi / GW-ano) — base alternativa, menor")
    row_formula(ws, 13, lambda i, c, pc: f"={c}15/{c}10", nf=NF_NUM1, start=1)

    header_row(ws, 14, "Receita (US$ milhões)")
    label(ws, 15, "Receita do cenário", bold=True, fill=FILL_HDR)
    row_formula(ws, 15, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] in BASE else (f"=({Ps('g_rev_lo')}+{Ps('g_rev_hi')})/2" if YEARS[i] == 2026 else f"={c}11*{c}12"), nf=NF_NUM, fill=FILL_HDR, bold=True)
    for i in range(4): ws[f"{COLS[i]}15"].font = Font(name="Arial", size=10, bold=True, color="FF008000")
    label(ws, 16, "Crescimento da receita")
    row_formula(ws, 16, lambda i, c, pc: f"={c}15/{pc}15-1", nf=NF_PCT, start=1)
    label(ws, 17, "Receita | consenso BBG CY26-28 (memo)")
    row_formula(ws, 17, lambda i, c, pc: f"={Pc('rev_ref', c)}", nf=NF_NUM, font=F_LINK, start=3, end=6)
    label(ws, 18, "Cenário ÷ consenso − 1")
    row_formula(ws, 18, lambda i, c, pc: f"={c}15/{c}17-1", nf=NF_PCT, start=3, end=6)
    label(ws, 19, "Memo: receita 2030 — UBS $84,8 bi / Street ~$80 bi (UBS 09-22) vs cenário")
    setc(ws, "K19", "=K15/84800-1", F_TXT, nf=NF_PCT, align="right")

    # ---- P&L / cash
    header_row(ws, 21, "Resultado operacional e caixa (base ajustada da companhia; SBC deduzida abaixo)")
    r = 22; pl = {}
    label(ws, r, "Margem EBITDA ajustada"); row_formula(ws, r, lambda i, c, pc: (f"={Pc('ebitda_ref', c)}/{c}15" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else (f"={Pc('ebitda_m', c)}" if YEARS[i] == 2026 else f"={Pc('ebitda_m', c)}+$E$6"), nf=NF_PCT, font=F_LINK); pl["ebitdam"] = r; r += 1
    label(ws, r, "EBITDA ajustado", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}15*{c}{pl['ebitdam']}" if YEARS[i] >= 2024 else None, bold=True); pl["ebitda"] = r; r += 1
    label(ws, r, "EBITDA | consenso BBG (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('ebitda_ref', c)}", font=F_LINK, start=3, end=6); pl["ebitda_c"] = r; r += 1
    label(ws, r, "D&A por GW ativo médio (US$ bi / GW-ano) | CY24-25 implícito"); row_formula(ws, r, lambda i, c, pc: (f"={c}{r+1}/{c}10" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else f"={Pc('da_gw', c)}", nf=NF_NUM1, font=F_LINK); pl["dagw"] = r; r += 1
    label(ws, r, "Depreciação e amortização"); row_formula(ws, r, lambda i, c, pc: f"={Pc('da_ref', c)}" if YEARS[i] in BASE else f"={c}10*{c}{pl['dagw']}", font=F_LINK); pl["da"] = r
    for i in range(3, NY): ws[f"{COLS[i]}{r}"].font = F_TXT
    r += 1
    label(ws, r, "Lucro operacional ajustado (AOI = EBITDA − D&A)", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebitda']}-{c}{pl['da']}" if YEARS[i] >= 2024 else None, bold=True); pl["aoi"] = r; r += 1
    label(ws, r, "Margem operacional ajustada"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['aoi']}/{c}15" if YEARS[i] >= 2024 else None, nf=NF_PCT); pl["aoim"] = r; r += 1
    label(ws, r, "AOI | consenso BBG EBIT (memo) / guia FY26 ponto médio"); row_formula(ws, r, lambda i, c, pc: f"=({Ps('g_aoi_lo')}+{Ps('g_aoi_hi')})/2" if YEARS[i] == 2026 else f"={Pc('aoi_ref', c)}", font=F_LINK, start=3, end=6); pl["aoi_c"] = r; r += 1
    label(ws, r, "Stock-based compensation"); row_formula(ws, r, lambda i, c, pc: f"=-{Pc('sbc_ref', c)}" if YEARS[i] in BASE else f"=-{c}15*{Pc('sbc', c)}"); pl["sbc"] = r; r += 1
    label(ws, r, "EBIT após SBC", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['aoi']}+{c}{pl['sbc']}" if YEARS[i] >= 2024 else None, bold=True); pl["ebit"] = r; r += 1
    label(ws, r, "Margem EBIT após SBC"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebit']}/{c}15" if YEARS[i] >= 2024 else None, nf=NF_PCT); pl["ebitm"] = r; r += 1
    label(ws, r, "Alíquota de imposto caixa"); row_formula(ws, r, lambda i, c, pc: f"={Pc('tax', c)}" if YEARS[i] >= 2026 else None, nf=NF_PCT, font=F_LINK); pl["tax"] = r; r += 1
    label(ws, r, "NOPAT"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebit']}*(1-{c}{pl['tax']})" if YEARS[i] >= 2026 else None); pl["nopat"] = r; r += 1
    label(ws, r, "Custo de build por GW adicionado (US$ bi / GW)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('build', c)}" if YEARS[i] >= 2026 else None, nf=NF_NUM1, font=F_LINK); pl["build"] = r; r += 1
    label(ws, r, "Capex de crescimento = build x ((1 − pré) x adições t + pré x adições t+1)")
    def f_cg(i, c, pc):
        if YEARS[i] < 2026: return None
        nc = COLS[i + 1] if i + 1 < NY else c
        return f"=-{c}{pl['build']}*((1-{Ps('prebuild')})*{c}9+{Ps('prebuild')}*{nc}9)"
    row_formula(ws, r, f_cg); pl["capex_g"] = r; r += 1
    label(ws, r, "Potência reposta no ano (MW) = potência instalada em (t − vida), adições e reposições incluídas")
    row_formula(ws, r, lambda i, c, pc: f"=IF(COLUMN({c}9)-COLUMN($D$9)+1-$F$6>=1,INDEX($D${r+1}:$Z${r+1},1,COLUMN({c}9)-COLUMN($D$9)+1-$F$6),0)", nf=NF_NUM); pl["replaced"] = r; r += 1
    label(ws, r, "Potência instalada no ano (MW) = adições + reposições")
    row_formula(ws, r, lambda i, c, pc: f"={c}9+{c}{pl['replaced']}", nf=NF_NUM); pl["installed"] = r; r += 1
    label(ws, r, "Capex de reposição = potência reposta x build x % reposição")
    row_formula(ws, r, lambda i, c, pc: f"=-{c}{pl['replaced']}*{c}{pl['build']}*$G$6" if YEARS[i] >= 2026 else None); pl["capex_r"] = r; r += 1
    label(ws, r, "Capex total | CY23-25 caixa reportado; 2026 guia (ponto médio)", bold=True)
    row_formula(ws, r, lambda i, c, pc: f"=-{Pc('capex_ref', c)}" if YEARS[i] in BASE else (f"=-({Ps('g_capex_lo')}+{Ps('g_capex_hi')})/2" if YEARS[i] == 2026 else f"={c}{pl['capex_g']}+{c}{pl['capex_r']}"), bold=True); pl["capex"] = r; r += 1
    label(ws, r, "Capex | consenso BBG (memo)"); row_formula(ws, r, lambda i, c, pc: f"=-{Pc('capex_ref', c)}", font=F_LINK, start=3, end=6); pl["capex_c"] = r; r += 1
    label(ws, r, "Memo: capex de 2026 pela fórmula (check da calibração)"); setc(ws, f"G{r}", f"=G{pl['capex_g']}+G{pl['capex_r']}", F_TXT, nf=NF_NUM, align="right"); pl["capex26f"] = r; r += 1
    label(ws, r, "Memo: capex total por GW INSTALADO no ano (adições + reposições; US$ bi / GW) — base de fluxo, inclui pré-construção"); row_formula(ws, r, lambda i, c, pc: f"=-{c}{pl['capex']}/{c}{pl['installed']}" if YEARS[i] >= 2024 else None, nf=NF_NUM1); pl["capexgw"] = r; r += 1
    label(ws, r, "NWC operacional (recebíveis − receita diferida)"); row_formula(ws, r, lambda i, c, pc: (f"={Pc('ar', c)}-{Pc('defrev', c)}" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else f"={c}15*{Pc('nwc', c)}"); pl["nwc"] = r; r += 1
    label(ws, r, "Variação de NWC | efeito caixa (pré-pagamentos de clientes)"); row_formula(ws, r, lambda i, c, pc: f"=-({c}{pl['nwc']}-{pc}{pl['nwc']})", start=2); pl["dnwc"] = r; r += 1
    label(ws, r, "Fluxo de caixa livre (FCFF)", bold=True)
    row_formula(ws, r, lambda i, c, pc: f"={c}{pl['nopat']}+{c}{pl['da']}+{c}{pl['capex']}+{c}{pl['dnwc']}", start=3, bold=True); pl["fcff"] = r; r += 1
    label(ws, r, "FCFF / receita"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}/{c}15", nf=NF_PCT, start=3); pl["fcffr"] = r; r += 1
    label(ws, r, "Memo: ROIC incremental implícito = ΔNOPAT ÷ (capex − D&A) do ano anterior"); row_formula(ws, r, lambda i, c, pc: f"=IFERROR(({c}{pl['nopat']}-{pc}{pl['nopat']})/(-{pc}{pl['capex']}-{pc}{pl['da']}),NA())" if YEARS[i] >= 2028 else None, nf=NF_PCT); pl["roic_i"] = r
    pl["end"] = r; pl["rev"] = 15

    # ---- discount block
    r0 = pl["end"] + 2
    dsc = {}
    label(ws, r0, "Data do fluxo de caixa"); row_formula(ws, r0, lambda i, c, pc: f"=DATE({YEARS[i]},12,31)", nf=NF_DATE_S); dsc["date"] = r0
    vd = "$D$" + str(r0 + 7)
    label(ws, r0 + 1, "Prazo de desconto (anos)"); row_formula(ws, r0 + 1, lambda i, c, pc: f"=MAX(0,({c}{r0}-{vd})/365)", nf=NF_NUM2); dsc["t"] = r0 + 1
    label(ws, r0 + 2, "Parcela pós-valuation do ano"); row_formula(ws, r0 + 2, lambda i, c, pc: f"=MAX(0,MIN(1,({c}{r0}-{vd})/({c}{r0}-DATE({YEARS[i]},1,1)+1)))", nf=NF_PCT); dsc["frac"] = r0 + 2
    label(ws, r0 + 3, "FCFF considerado no valuation"); row_formula(ws, r0 + 3, lambda i, c, pc: "=0" if i < 3 else f"={c}{pl['fcff']}*{c}{r0+2}"); dsc["fcffv"] = r0 + 3
    wacc = "$D$" + str(r0 + 8)
    label(ws, r0 + 4, "Valor presente do FCFF"); row_formula(ws, r0 + 4, lambda i, c, pc: f"={c}{r0+3}/(1+{wacc})^{c}{r0+1}"); dsc["pv"] = r0 + 4
    dsc["end"] = r0 + 4; dsc["vstart"] = r0 + 6

    # ---- valuation block
    v0 = dsc["vstart"]; val = {}
    header_row(ws, v0, "Valuation | FCFF e ponte para equity")
    label(ws, v0 + 1, "Data de valuation"); setc(ws, f"D{v0+1}", f"={P}D{R['val_date']}", F_LINK, nf=NF_DATE); val["vdate"] = v0 + 1
    label(ws, v0 + 2, "WACC"); setc(ws, f"D{v0+2}", f"={P}D{R['wacc']}", F_LINK, nf=NF_PCT); val["wacc"] = v0 + 2
    label(ws, v0 + 3, "Crescimento terminal (g)"); setc(ws, f"D{v0+3}", f"={P}D{R['g']}", F_LINK, nf=NF_PCT); val["g"] = v0 + 3
    label(ws, v0 + 4, "ROIC incremental terminal"); setc(ws, f"D{v0+4}", f"={P}D{R['roic']}", F_LINK, nf=NF_PCT); val["roic"] = v0 + 4
    label(ws, v0 + 5, "Ações diluídas (milhões)"); setc(ws, f"D{v0+5}", f"={P}D{R['shares']}", F_LINK, nf=NF_NUM1); val["sh"] = v0 + 5
    label(ws, v0 + 6, "Caixa + aplicações (não restrito)"); setc(ws, f"D{v0+6}", f"={P}D{R['cash']}", F_LINK, nf=NF_NUM); val["cash"] = v0 + 6
    rr = v0 + 7
    label(ws, rr, "Dívida financeira bruta (principal + arrendamento financeiro)"); setc(ws, f"D{rr}", f"={P}D{R['debt']}", F_LINK, nf=NF_NUM); val["debt"] = rr; rr += 1
    label(ws, rr, "Dívida líquida"); setc(ws, f"D{rr}", f"=D{val['debt']}-D{val['cash']}", F_TXT, nf=NF_NUM); val["netdebt"] = rr; rr += 2
    Z = COLS[-1]; G0 = COLS[3]
    label(ws, rr, "PV dos fluxos explícitos"); setc(ws, f"D{rr}", f"=SUM({G0}{dsc['pv']}:{Z}{dsc['pv']})", F_TXT, nf=NF_NUM); val["pvx"] = rr; rr += 1
    label(ws, rr, "NOPAT terminal"); setc(ws, f"D{rr}", f"={Z}{pl['nopat']}*(1+D{val['g']})", F_TXT, nf=NF_NUM); val["nopat_t"] = rr; rr += 1
    label(ws, rr, "Reinvestimento líquido terminal"); setc(ws, f"D{rr}", f"=D{val['nopat_t']}*D{val['g']}/D{val['roic']}", F_TXT, nf=NF_NUM); val["reinv"] = rr; rr += 1
    label(ws, rr, "FCFF terminal"); setc(ws, f"D{rr}", f"=IF(AND(D{val['wacc']}>D{val['g']},D{val['roic']}>D{val['g']}),D{val['nopat_t']}-D{val['reinv']},NA())", F_TXT, nf=NF_NUM); val["fcff_t"] = rr; rr += 1
    label(ws, rr, "Valor terminal não descontado"); setc(ws, f"D{rr}", f"=D{val['fcff_t']}/(D{val['wacc']}-D{val['g']})", F_TXT, nf=NF_NUM); val["tv"] = rr; rr += 1
    label(ws, rr, "PV do valor terminal"); setc(ws, f"D{rr}", f"=D{val['tv']}/(1+D{val['wacc']})^{Z}{dsc['t']}", F_TXT, nf=NF_NUM); val["pvtv"] = rr; rr += 1
    label(ws, rr, "Enterprise value"); setc(ws, f"D{rr}", f"=SUM(D{val['pvx']},D{val['pvtv']})", F_TXT, nf=NF_NUM); val["ev"] = rr; rr += 1
    label(ws, rr, "Equity value"); setc(ws, f"D{rr}", f"=D{val['ev']}-D{val['netdebt']}", F_TXT, nf=NF_NUM); val["equity"] = rr; rr += 1
    label(ws, rr, "Valor por ação (US$)", bold=True, fill=FILL_RES); ws[f"C{rr}"].font = F_RES
    setc(ws, f"D{rr}", f"=D{val['equity']}/D{val['sh']}", F_RES, nf='"$"0.00;\\("$"0.00\\)', fill=FILL_RES); val["ps"] = rr; rr += 1
    label(ws, rr, "Valor terminal / enterprise value"); setc(ws, f"D{rr}", f"=D{val['pvtv']}/D{val['ev']}", F_TXT, nf=NF_PCT); val["tvshare"] = rr; rr += 1
    label(ws, rr, "Valor por ação | fluxos explícitos apenas (sem terminal)"); setc(ws, f"D{rr}", f"=(D{val['pvx']}-D{val['netdebt']})/D{val['sh']}", F_TXT, nf='"$"0.00;\\("$"0.00\\)'); val["ps_nt"] = rr; rr += 1
    label(ws, rr, "Memo: EV ao preço de referência (market cap + dívida líquida)"); setc(ws, f"D{rr}", f"={Ps('mktcap')}+D{val['netdebt']}", F_TXT, nf=NF_NUM); val["ev_px"] = rr; rr += 1
    label(ws, rr, "Memo: EV/EBITDA CY27E e CY28E ao preço de referência"); setc(ws, f"D{rr}", f"=D{val['ev_px']}/H{pl['ebitda']}", F_TXT, nf=NF_X); setc(ws, f"E{rr}", f"=D{val['ev_px']}/I{pl['ebitda']}", F_TXT, nf=NF_X); val["evm"] = rr; rr += 1
    label(ws, rr, "Memo: EV/receita CY28E ao preço (UBS PT $120 = 3,8x CY28E; pares ~4,5x)"); setc(ws, f"D{rr}", f"=D{val['ev_px']}/I15", F_TXT, nf=NF_X); val["evs"] = rr
    # grid WACC x g
    setc(ws, f"F{v0+1}", "Sensibilidade | WACC x g (US$ / ação)", F_TXTB)
    setc(ws, f"F{v0+3}", f"=D{val['ps']}", F_TXT, nf=NF_NUM2, fill=FILL_HDR)
    gcols = ["G", "H", "I", "J", "K"]; gd = [-0.01, -0.005, 0, 0.005, 0.01]
    for gc, d in zip(gcols, gd):
        setc(ws, f"{gc}{v0+3}", f"=$D${val['g']}+{d}", F_TXTB, nf=NF_PCT, fill=FILL_HDR)
    wdl = [-0.02, -0.01, 0, 0.01, 0.02]
    for k, d in enumerate(wdl):
        rg = v0 + 4 + k
        setc(ws, f"F{rg}", f"=$D${val['wacc']}+{d}", F_TXTB, nf=NF_PCT, fill=FILL_HDR)
        for gc in gcols:
            f = (f"=(SUMPRODUCT(${G0}${dsc['fcffv']}:${Z}${dsc['fcffv']},1/(1+$F{rg})^${G0}${dsc['t']}:${Z}${dsc['t']})"
                 f"+${Z}${pl['nopat']}*(1+{gc}${v0+3})*(1-{gc}${v0+3}/$D${val['roic']})/($F{rg}-{gc}${v0+3})/(1+$F{rg})^${Z}${dsc['t']}-$D${val['netdebt']})/$D${val['sh']}")
            setc(ws, f"{gc}{rg}", f, F_TXT, nf=NF_NUM2)
    val["grid_center_row"] = v0 + 6
    # grid 2 placeholder: receita/GW x margem EBITDA (Data Table created by COM in recalc_verify.py)
    g2 = v0 + 10
    setc(ws, f"F{g2}", "Sensibilidade | receita por GW em 2030 (US$ bi/GW, colunas) x margem EBITDA LT (linhas) — US$ / ação (tabela de dados, preenchida pelo Excel)", F_TXTB)
    setc(ws, f"F{g2+1}", f"=D{val['ps']}", F_TXT, nf=NF_NUM2, fill=FILL_HDR)
    mults = [11, 12, 13, 14, 15, 16]
    for k, m in enumerate(mults):
        setc(ws, f"{get_column_letter(7+k)}{g2+1}", round(m / 13.0, 6), F_TXTB, nf=NF_NUM2, fill=FILL_HDR)
        setc(ws, f"{get_column_letter(7+k)}{g2+8}", m, F_NOTE, nf='0" bi/GW"', align="center")
    adjs = [-0.05, 0, 0.05, 0.10]
    for k, a in enumerate(adjs):
        setc(ws, f"F{g2+2+k}", a, F_TXTB, nf='+0.0%;-0.0%;0.0%', fill=FILL_HDR)
    for k, a in enumerate(adjs):
        setc(ws, f"E{g2+2+k}", f"={P}$Z${R['ebitda_m']}+F{g2+2+k}", F_NOTE, nf=NF_PCT)
    note(ws, g2 + 7, "Linhas: ajuste de margem EBITDA (p.p.) sobre TODO o caminho 2027+ (coluna E = margem LT resultante). Colunas: multiplicador da receita/GW sobre TODO o caminho 2027+ (linha de cima) — a linha de baixo mostra o nível de 2030 equivalente (LT = 14,0 x mult). Base 2030 = 13,0 fica ABAIXO do piso da gestão para contratos novos (15-16): 1,9 GW legado a 11 + 6,1 GW novos a 15,5 daria ~14,4.", col="F")
    val["grid2"] = g2
    g3 = g2 + 10
    setc(ws, f"F{g3}", "Sensibilidade | vida útil para reposição (anos, colunas) x custo de reposição (% do build, linhas) — US$ / ação (tabela de dados)", F_TXTB)
    setc(ws, f"F{g3+1}", f"=D{val['ps']}", F_TXT, nf=NF_NUM2, fill=FILL_HDR)
    for k, lf in enumerate([5, 6, 7, 8, 10]):
        setc(ws, f"{get_column_letter(7+k)}{g3+1}", lf, F_TXTB, nf='0" anos"', fill=FILL_HDR)
    for k, rp in enumerate([1.0, 0.8, 0.6, 0.4]):
        setc(ws, f"F{g3+2+k}", rp, F_TXTB, nf=NF_PCT, fill=FILL_HDR)
    note(ws, g3 + 6, "A reposição é o que o Street raramente cobra explicitamente: a 6 anos / 80% a frota madura consome ~$5,3 bi por GW-ano (≈ D&A). Vida mais longa = re-contratação de GPUs antigas (A100/H100 ainda alugadas no ano 9) sem troca — mas as colunas 7-10 anos mantêm o preço cheio em GPUs velhas (DB 2025-06-16: 50-75% do ASP em anos 5-6), logo são o LIMITE SUPERIOR, não um cenário.", col="F")
    val["grid3"] = g3
    u0 = g3 + 8
    header_row(ws, u0, "Economia unitária por GW em regime (coluna CY35E) — a conta por trás do DCF", cols=COLS[:3])
    ue = {}
    u = u0 + 1
    label(ws, u, "Receita por GW faturável (US$ bi / GW-ano)"); setc(ws, f"D{u}", "=P12", F_TXT, nf=NF_NUM2); ue["rev"] = u; u += 1
    label(ws, u, "EBITDA por GW (US$ bi)"); setc(ws, f"D{u}", f"=D{ue['rev']}*P{pl['ebitdam']}", F_TXT, nf=NF_NUM2); ue["ebitda"] = u; u += 1
    label(ws, u, "D&A por GW (US$ bi)"); setc(ws, f"D{u}", f"=P{pl['dagw']}", F_TXT, nf=NF_NUM2); ue["da"] = u; u += 1
    label(ws, u, "SBC por GW (US$ bi)"); setc(ws, f"D{u}", f"=D{ue['rev']}*{P}P{R['sbc']}", F_TXT, nf=NF_NUM2); ue["sbc"] = u; u += 1
    label(ws, u, "Imposto por GW = (EBITDA − D&A − SBC) x alíquota (US$ bi)"); setc(ws, f"D{u}", f"=(D{ue['ebitda']}-D{ue['da']}-D{ue['sbc']})*P{pl['tax']}", F_TXT, nf=NF_NUM2); ue["tax"] = u; u += 1
    label(ws, u, "Caixa operacional por GW antes de capex = EBITDA − SBC − imposto (US$ bi)"); setc(ws, f"D{u}", f"=D{ue['ebitda']}-D{ue['sbc']}-D{ue['tax']}", F_TXTB, nf=NF_NUM2); ue["cfo"] = u; u += 1
    label(ws, u, "Custo de build por GW (US$ bi)"); setc(ws, f"D{u}", f"=P{pl['build']}", F_TXT, nf=NF_NUM2); ue["build"] = u; u += 1
    label(ws, u, "Reposição por GW-ano, frota madura = build x % reposição ÷ vida (US$ bi) — memo, base do DCF em regime"); setc(ws, f"D{u}", f"=D{ue['build']}*$G$6/$F$6", F_TXT, nf=NF_NUM2); ue["repl_lvl"] = u; u += 1
    label(ws, u, "Reposição de 1 GW NOVO, equivalente anual (sinking fund: primeira troca no ano 'vida') = build x % x WACC ÷ ((1+WACC)^vida − 1)"); setc(ws, f"D{u}", f"=D{ue['build']}*$G$6*D{val['wacc']}/((1+D{val['wacc']})^$F$6-1)", F_TXT, nf=NF_NUM2); ue["repl"] = u; u += 1
    label(ws, u, "FCF por GW-ano de 1 GW novo, sem crescimento = caixa operacional − reposição equivalente (US$ bi)", bold=True); setc(ws, f"D{u}", f"=D{ue['cfo']}-D{ue['repl']}", F_TXTB, nf=NF_NUM2); ue["fcf"] = u; u += 1
    label(ws, u, "Rendimento de caixa sobre o custo de build (FCF ÷ build)"); setc(ws, f"D{u}", f"=D{ue['fcf']}/D{ue['build']}", F_TXT, nf=NF_PCT); ue["yield"] = u; u += 1
    label(ws, u, "Payback bruto do build = build ÷ caixa operacional (anos)"); setc(ws, f"D{u}", f"=D{ue['build']}/D{ue['cfo']}", F_TXT, nf='0.0" anos"'); ue["pb"] = u; u += 1
    label(ws, u, "Valor de 1 GW em perpetuidade ao WACC = FCF ÷ WACC (US$ bi)"); setc(ws, f"D{u}", f"=D{ue['fcf']}/D{val['wacc']}", F_TXT, nf=NF_NUM2); ue["pv"] = u; u += 1
    label(ws, u, "NPV de 1 GW novo = valor − build (US$ bi) — negativo = cada GW destrói valor ao WACC", bold=True); setc(ws, f"D{u}", f"=D{ue['pv']}-D{ue['build']}", F_TXTB, nf=NF_NUM2); ue["npv"] = u; u += 1
    label(ws, u, "Receita/GW de equilíbrio (NPV = 0) com a mesma margem, vida e reposição (US$ bi / GW-ano)")
    setc(ws, f"D{u}", f"=(D{ue['build']}*D{val['wacc']}+D{ue['repl']}-D{ue['da']}*P{pl['tax']})/((P{pl['ebitdam']}-{P}P{R['sbc']})*(1-P{pl['tax']}))", F_TXT, nf=NF_NUM2); ue["be"] = u; u += 1
    note(ws, u, "Equilíbrio: (EBITDA − SBC) x (1 − t) + D&A x t − reposição equivalente = build x WACC. Comparar com as marcas: livro instalado ~11, piso da gestão para novos contratos 15-16 (= o equilíbrio), curto prazo ~40. A frota MADURA repõe ~frota ÷ vida por ano (linha memo) — é o que o DCF cobra a partir de 2032.")
    val["ue"] = ue
    val["end"] = max(rr, u + 1)

    # ---- memo: debt roll + EPS (outside DCF)
    m0 = val["end"] + 2
    header_row(ws, m0, "Memo fora do DCF | dívida líquida implícita, juros, lucro líquido e EPS (sem captação de equity após 2026)")
    mm = {}
    r = m0 + 1
    label(ws, r, "Dívida líquida no fim do ano (US$ mi)"); mm["nd"] = r
    row_formula(ws, r, lambda i, c, pc: f"={Ps('nd_2025')}" if YEARS[i] == 2025 else (f"={pc}{r}-{c}{pl['fcff']}+{c}{r+1}-{Ps('eq_2026')}" if YEARS[i] == 2026 else f"={pc}{r}-{c}{pl['fcff']}+{c}{r+1}"), start=2); r += 1
    label(ws, r, "Juros líquidos = (dívida líquida anterior − 0,5 x FCFF do ano) x custo da dívida"); mm["int"] = r
    row_formula(ws, r, lambda i, c, pc: f"=({pc}{mm['nd']}-0.5*{c}{pl['fcff']})*{Pc('kd', c)}", start=3); r += 1
    label(ws, r, "Juros | reportado FY23-25 e consenso implícito (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('int_ref', c)}", font=F_LINK, end=3); r += 1
    label(ws, r, "Dívida líquida / EBITDA"); mm["lev"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{mm['nd']}/{c}{pl['ebitda']}", nf=NF_X, start=2); r += 1
    label(ws, r, "Lucro líquido ajustado (base da companhia, EX-SBC) = (AOI − juros) x (1 − imposto se positivo)"); mm["ni"] = r
    row_formula(ws, r, lambda i, c, pc: f"=IF({c}{pl['aoi']}-{c}{mm['int']}>0,({c}{pl['aoi']}-{c}{mm['int']})*(1-{c}{pl['tax']}),{c}{pl['aoi']}-{c}{mm['int']})", start=3); r += 1
    label(ws, r, "Memo: lucro líquido após SBC"); mm["ni_sbc"] = r
    row_formula(ws, r, lambda i, c, pc: f"=IF({c}{pl['ebit']}-{c}{mm['int']}>0,({c}{pl['ebit']}-{c}{mm['int']})*(1-{c}{pl['tax']}),{c}{pl['ebit']}-{c}{mm['int']})", start=3); r += 1
    label(ws, r, "Lucro líquido | GAAP reportado / consenso BBG (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('ni_ref', c)}", font=F_LINK, end=6); r += 1
    label(ws, r, "Ações diluídas (mi)"); mm["sh"] = r; row_formula(ws, r, lambda i, c, pc: f"={Pc('sh', c)}", nf=NF_NUM1, font=F_LINK, start=3); r += 1
    label(ws, r, "EPS ajustado (US$, base da companhia / consenso: ex-SBC)", bold=True); mm["eps"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{mm['ni']}/{c}{mm['sh']}", nf=NF_NUM2, start=3, bold=True); r += 1
    label(ws, r, "EPS | consenso BBG (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('eps_ref', c)}", nf=NF_NUM2, font=F_LINK, start=3, end=6); r += 1
    label(ws, r, "FCF para o acionista = FCFF − juros"); mm["fcfe"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}-{c}{mm['int']}", start=3); r += 1
    label(ws, r, "FCFF acumulado desde 2026 (necessidade de financiamento até virar positivo)"); mm["cum"] = r
    row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}" if YEARS[i] == 2026 else f"={pc}{r}+{c}{pl['fcff']}", start=3); r += 1
    mm["end"] = r - 1

    # ---- reconciliations
    rc = mm["end"] + 2
    header_row(ws, rc, "Reconciliações e guardrails (0 / 🟢 esperado)")
    rr = rc + 1
    label(ws, rr, "Receita − potência faturável x receita/GW (2027+)"); row_formula(ws, rr, lambda i, c, pc: f"={c}15-{c}11*{c}12", nf=NF_CHK, start=4); rr += 1
    label(ws, rr, "AOI − (EBITDA − D&A)"); row_formula(ws, rr, lambda i, c, pc: f"={c}{pl['aoi']}-({c}{pl['ebitda']}-{c}{pl['da']})", nf=NF_CHK, start=1); rr += 1
    label(ws, rr, "Guia FY26: AOI do modelo dentro de $960-1.150 mi (0 = ok; senão desvio)"); setc(ws, f"G{rr}", f"=IF(G{pl['aoi']}<{Ps('g_aoi_lo')},G{pl['aoi']}-{Ps('g_aoi_lo')},IF(G{pl['aoi']}>{Ps('g_aoi_hi')},G{pl['aoi']}-{Ps('g_aoi_hi')},0))", F_TXT, nf=NF_CHK, align="right"); rr += 1
    label(ws, rr, "Calibração do capex 2026: fórmula ÷ guia (ponto médio) − 1 (|x| < 10%)"); setc(ws, f"G{rr}", f"=G{pl['capex26f']}/G{pl['capex']}-1", F_TXT, nf=NF_PCT, align="right"); rr += 1
    label(ws, rr, "Receita/GW faturável entre 10 e 20 US$ bi/GW (0 = dentro; senão excesso)"); row_formula(ws, rr, lambda i, c, pc: f"=IF({c}12<10,{c}12-10,IF({c}12>20,{c}12-20,0))", nf=NF_CHK, start=1); rr += 1
    label(ws, rr, "Capex total por GW instalado entre 25 e 60 US$ bi/GW (fluxo; 0 = dentro)"); row_formula(ws, rr, lambda i, c, pc: f"=IF({c}{pl['capexgw']}<25,{c}{pl['capexgw']}-25,IF({c}{pl['capexgw']}>60,{c}{pl['capexgw']}-60,0))", nf=NF_CHK, start=3); rr += 1
    label(ws, rr, "Cobertura da RPO: receita 2H26 + 2027 + 1H28 do modelo ÷ 41% da RPO de jun-26 (US$ 42,5 bi) — >1 = modelo acima do contratado"); setc(ws, f"G{rr}", f"=(G15-{Ps('h1_rev')}+H15+I15/2)/(0.41*{P}G{R['rpo_ref']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "Cobertura da RPO: receita meses 25-48 (2H28 + 2029 + 1H30) ÷ 39% da RPO (US$ 40,4 bi)"); setc(ws, f"G{rr}", f"=(I15/2+J15+K15/2)/(0.39*{P}G{R['rpo_ref']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "Dívida líquida / EBITDA máxima 2026-30 (UBS: 5,7x 2026E, 4,2x 2027E)"); setc(ws, f"G{rr}", f"=MAX(G{mm['lev']}:K{mm['lev']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "Adições 2026-30 − (8.000 − YE25): 0 = frota de 8,0 GW em 2030 (alvo da gestão ≥8 GW)"); setc(ws, f"G{rr}", "=SUM(G9:K9)-(8000-F8)", F_TXT, nf=NF_CHK, align="right"); rr += 1
    label(ws, rr, "Equity: EV − dívida líquida"); setc(ws, f"D{rr}", f"=D{val['equity']}-(D{val['ev']}-D{val['netdebt']})", F_TXT, nf=NF_CHK); rr += 1
    label(ws, rr, "Sensibilidade: centro = DCF base"); setc(ws, f"D{rr}", f"=I{val['grid_center_row']}-D{val['ps']}", F_TXT, nf=NF_CHK); rr += 1
    label(ws, rr, "Margem operacional ajustada 2030 vs alvo de longo prazo da gestão 25-30% (call 4Q25) — desvio ao piso"); setc(ws, f"K{rr}", f"=MIN(0,K{pl['aoim']}-0.25)", F_TXT, nf=NF_PCT, align="right"); rr += 1
    rec_end = rr

    # ---- wiki block
    rw = rec_end + 1
    header_row(ws, rw, "Resumo para a wiki | estimativas de casa (CY) — Capstone estimates (house model)")
    label(ws, rw + 1, "Receita (US$ mi)"); row_formula(ws, rw + 1, lambda i, c, pc: f"={c}15", start=1, end=8)
    label(ws, rw + 2, "Potência ativa no fim do ano (MW)"); row_formula(ws, rw + 2, lambda i, c, pc: f"={c}8", start=1, end=8)
    label(ws, rw + 3, "Receita por GW faturável (US$ bi)"); row_formula(ws, rw + 3, lambda i, c, pc: f"={c}12", nf=NF_NUM1, start=1, end=8)
    label(ws, rw + 4, "Margem EBITDA ajustada"); row_formula(ws, rw + 4, lambda i, c, pc: f"={c}{pl['ebitdam']}", nf=NF_PCT, start=1, end=8)
    label(ws, rw + 5, "EBITDA ajustado (US$ mi)"); row_formula(ws, rw + 5, lambda i, c, pc: f"={c}{pl['ebitda']}", start=1, end=8)
    label(ws, rw + 6, "Margem operacional ajustada (AOI)"); row_formula(ws, rw + 6, lambda i, c, pc: f"={c}{pl['aoim']}", nf=NF_PCT, start=1, end=8)
    label(ws, rw + 7, "Capex (US$ mi)"); row_formula(ws, rw + 7, lambda i, c, pc: f"=-{c}{pl['capex']}", start=1, end=8)
    label(ws, rw + 8, "FCFF (US$ mi)"); row_formula(ws, rw + 8, lambda i, c, pc: f"={c}{pl['fcff']}", start=3, end=8)
    label(ws, rw + 9, "Lucro líquido ajustado (US$ mi) | CY24-25 GAAP reportado"); row_formula(ws, rw + 9, lambda i, c, pc: f"={Pc('ni_ref', c)}" if YEARS[i] < 2026 else f"={c}{mm['ni']}", start=1, end=8)
    label(ws, rw + 10, "EPS ajustado (US$) | CY24-25 GAAP reportado", bold=True); row_formula(ws, rw + 10, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] < 2026 else f"={c}{mm['eps']}", nf=NF_NUM2, start=1, end=8, bold=True)
    label(ws, rw + 11, "Consenso BBG — receita / EPS (memo)"); row_formula(ws, rw + 11, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] >= 2026 else None, start=3, end=6, font=F_LINK)
    label(ws, rw + 12, "Consenso BBG — EPS (memo)"); row_formula(ws, rw + 12, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] >= 2026 else None, nf=NF_NUM2, start=3, end=6, font=F_LINK)
    label(ws, rw + 13, "Receita: casa ÷ consenso − 1"); row_formula(ws, rw + 13, lambda i, c, pc: f"={c}{rw+1}/{c}{rw+11}-1" if YEARS[i] >= 2026 else None, nf=NF_PCT, start=3, end=6)
    label(ws, rw + 14, "EV/EBITDA ao preço de referência (informativo)"); row_formula(ws, rw + 14, lambda i, c, pc: f"=$D${val['ev_px']}/{c}{pl['ebitda']}" if YEARS[i] >= 2025 else None, nf=NF_X, start=2, end=8)
    note(ws, rw + 16, "A tabela 'Capstone estimates (house model)' da página wiki (_wiki/CRWV.md) é transcrita deste bloco (CY24A-CY28E). Thesis-drift: ao mudar um número, mover o antigo para o Changelog da página.")
    note(ws, rw + 17, "Leitura do modelo: ao preço corrente o DCF é uma aposta na receita/GW e na reposição — 1 GW custa ~$40 bi e gera ~$7-8 bi de EBITDA/ano; com reposição a cada 6 anos o retorno unlevered fica perto do WACC. A grade receita/GW x margem é a resposta.")

    # ================================================================================================= Histórico
    build_historico(wh, R)
    build_divida(wd)

    wb.save(path)
    lay = dict(R=R, pl=pl, dsc=dsc, val=val, mm=mm, rec=rc, wiki=rw)
    json.dump(lay, open(os.path.join(OUT, "layout.json"), "w"), indent=1, default=str)
    return lay


# ================================================================================================= Histórico sheet
HQ = ["FY23", "FY24", "FY25", "1Q25", "2Q25", "3Q25", "4Q25", "1Q26", "2Q26"]
HCOLS = [get_column_letter(4 + i) for i in range(len(HQ))]
HIST = [
    ("Receita", [229, 1915, 5131, 981.6, 1212.8, 1364.7, 1571.9, 2078, 2575], NF_NUM1, "10-K FY25; 10-Qs (1Q25-3Q25 em US$ mil, convertidos); 4Q25 = FY − 9M."),
    ("Custo de receita", [69, 493, 1453, 262.4, 312.7, 368.8, 509.1, 716, 879], NF_NUM1, "Idem."),
    ("Tecnologia e infraestrutura", [131, 961, 2929, 561.4, 669.9, 747.5, 950.2, 1273, 1507], NF_NUM1, "Idem (inclui aluguel de DC, energia, D&A)."),
    ("Vendas e marketing", [13, 18, 144, 10.5, 36.8, 44.6, 52.0, 69, 60], NF_NUM1, "Idem."),
    ("Geral e administrativo", [30, 119, 651, 174.8, 174.2, 151.9, 150.2, 164, 178], NF_NUM1, "Idem."),
    ("Resultado operacional GAAP", [-14, 324, -46, -27.5, 19.2, 51.9, -89.6, -144, -49], NF_NUM1, "Idem."),
    ("Despesa financeira líquida", [-28, -361, -1229, -263.8, -267.2, -311.0, -387.0, -536, -640], NF_NUM1, "Idem; 3Q25 call ($311 mi)."),
    ("Lucro líquido GAAP", [-594, -863, -1167, -314.6, -290.5, -110.1, -451.8, -740, -626], NF_NUM1, "Idem."),
    ("Depreciação e amortização", [103, 863, 2454, 443.5, 559.5, 630.5, 820.5, 1147, 1393], NF_NUM1, "Cash-flow acumulado (YTD) diferenciado por trimestre."),
    ("Stock-based compensation", [15, 31, 630, 184, 145, 144.4, 156.6, 153, 165], NF_NUM1, "Cash-flow YTD diferenciado (9M25 473,4): 3Q 144,4 / 4Q 156,6 (o statement of equity mostra 156,9 no 3Q — base diferente)."),
    ("Capex caixa (compra de PP&E)", [2943, 8702, 10309, 1407, 2453, 2389, 4060, 7695, 6422], NF_NUM1, "Cash-flow YTD diferenciado."),
    ("Capex base da companhia (calls)", [None, None, None, None, None, None, None, 6800, 9400], NF_NUM1, "Calls 1Q26 (05-07) e 2Q26 (08-11). FY26 guia $35-39 bi. Inclui OEM financing; difere do caixa."),
    ("EBITDA ajustado (companhia)", [None, 1226, 3098, 609, 753, 838, 898, 1164, 1510], NF_NUM1, "Calls; FY24 = 64% (DB 2025-06-16) PARTIAL; 1Q26 = '$1,2 bi, ~56%' x 2.078 = 1.164 PARTIAL; 1Q25 = 1.164/1,91 ('+91% y/y') PARTIAL."),
    ("Margem EBITDA ajustada", [None, "=E20/E8", "=F20/F8", "=G20/G8", "=H20/H8", "=I20/I8", "=J20/J8", "=K20/K8", "=L20/L8"], NF_PCT, "Calculado."),
    ("AOI (lucro operacional ajustado, companhia)", [None, None, None, None, 200, 217, None, 21, 128], NF_NUM1, "Calls: 2Q25 $200 mi (citado na call 2Q26, 08-11), 3Q25 $217 mi, 1Q26 $21 mi, 2Q26 $128 mi. FY25 guia $690-720 mi (call 3Q25)."),
    ("Potência ativa no fim do período (MW)", [70, 360, 850, 420, 470, 590, 850, 1000, 1500], NF_NUM, "10-K FY25 (70 / 360 / >850); calls (3Q25 590 = +120 q/q → 2Q25 470; 1Q25 ~420 ESTIMATE; 1Q26 '>1 GW'; 2Q26 1,5 GW)."),
    ("Potência contratada no fim do período (MW)", [None, None, 3100, None, None, 2900, 3100, 3500, 3700], NF_NUM, "Calls; 4,2 GW em 11-ago-26."),
    ("Backlog de receita (companhia, US$ bi)", [None, 15.1, 66.8, None, 30.1, 55.6, 66.8, 99.4, 104.0], NF_NUM1, "Calls (2Q25 'doubled YTD' → dez-24 ~15,1 PARTIAL). RPO 10-K/10-Q: 60,7 (dez-25) / 103,7 (jun-26)."),
    ("Receita diferida total (US$ mi)", [None, 4064, 8185, None, None, None, 8185, None, 9692], NF_NUM, "Balanços."),
    ("Caixa não restrito (US$ mi)", [217, 1361, 3127, None, None, None, 3127, None, 5524], NF_NUM, "Balanços."),
    ("Dívida bruta, principal (US$ mi)", [None, 7926, 21615, None, None, None, 21615, None, 35551], NF_NUM, "Notas de dívida (dez-24 valor contábil)."),
    ("Ações médias diluídas (mi)", [192, 218, 436, None, 487, None, None, None, 551], NF_NUM, "10-K / 10-Q (pós split 20:1)."),
]


def build_historico(wh, R):
    wh.sheet_view.showGridLines = False
    wh.column_dimensions["A"].width = 2.25; wh.column_dimensions["B"].width = 2.25; wh.column_dimensions["C"].width = 52
    for c in HCOLS: wh.column_dimensions[c].width = 11.5
    wh.column_dimensions["N"].width = 80
    setc(wh, "C2", "CRWV | Histórico reportado (anual e trimestral)", F_TITLE)
    setc(wh, "C3", "US$ milhões salvo indicação. Fonte: 10-K FY25, 10-Qs 1Q25-2Q26 (CRWV/), calls de resultados (CRWV/transcripts). Azul = reportado; cinza = derivado/PARTIAL.", F_TXT)
    for i, q in enumerate(HQ):
        setc(wh, f"{HCOLS[i]}5", q, F_TXTB, fill=FILL_HDR, align="center")
    setc(wh, "N5", "Fonte", F_TXTB, fill=FILL_HDR)
    header_row(wh, 7, "Demonstração de resultado e caixa", cols=HCOLS)
    r = 8
    for text, vals, nf, src in HIST:
        if text.startswith("Potência ativa"):
            header_row(wh, r, "Operacional e balanço", cols=HCOLS); r += 1
        label(wh, r, text)
        for i, v in enumerate(vals):
            if v is None: continue
            if isinstance(v, str):
                setc(wh, f"{HCOLS[i]}{r}", v, F_TXT, nf=nf, align="right")
            else:
                setc(wh, f"{HCOLS[i]}{r}", v, F_INPUT, nf=nf, align="right")
        setc(wh, f"N{r}", src, F_NOTE)
        r += 1
    # calibration block: revenue per GW lagged
    r += 1
    header_row(wh, r, "Calibração | receita anualizada do trimestre ÷ potência ativa média do trimestre ANTERIOR (US$ bi / GW-ano)", cols=HCOLS); r += 1
    label(wh, r, "Potência ativa média do trimestre anterior (MW)")
    # row 23 = active power row (compute index)
    act_row = 8 + [t for t, *_ in HIST].index("Potência ativa no fim do período (MW)") + 1
    prev = {"2Q25": f"=(E{act_row}+G{act_row})/2", "3Q25": f"=(G{act_row}+H{act_row})/2", "4Q25": f"=(H{act_row}+I{act_row})/2", "1Q26": f"=(I{act_row}+J{act_row})/2", "2Q26": f"=(J{act_row}+K{act_row})/2"}
    for q, f in prev.items():
        setc(wh, f"{HCOLS[HQ.index(q)]}{r}", f, F_TXT, nf=NF_NUM, align="right")
    setc(wh, f"N{r}", "Trimestre anterior = média entre o fim do penúltimo e o fim do anterior (2Q25 usa dez-24 360 e 1Q25 ~420 ESTIMATE). 1Q25 omitido (3Q24 não reportado). Base UBS 09-22 ('about a quarter for active power to generate revs'); 2Q26 = 2.575 x 4 / 925 = 11,1 = UBS.", F_NOTE)
    r += 1
    label(wh, r, "Receita por GW faturável (US$ bi / GW-ano)", bold=True)
    for q in prev:
        c = HCOLS[HQ.index(q)]
        setc(wh, f"{c}{r}", f"={c}8*4/{c}{r-1}", F_TXTB, nf=NF_NUM1, align="right")
    setc(wh, f"N{r}", "Cai de ~12,4 (2Q25) para ~11,1 (2Q26): a frota escalou mais rápido que o preço médio (livro legado MSFT/OpenAI). UBS: ~11 → ~15 no exit de 2027. Âncora do modelo (capa linha 12).", F_NOTE)
    r += 1
    label(wh, r, "D&A anualizado ÷ potência ativa média do trimestre (US$ bi / GW-ano)")
    for q in ("2Q25", "3Q25", "4Q25", "1Q26", "2Q26"):
        c = HCOLS[HQ.index(q)]; pcq = HCOLS[HQ.index(q) - 1]
        setc(wh, f"{c}{r}", f"={c}16*4/(({pcq}{act_row}+{c}{act_row})/2)", F_TXT, nf=NF_NUM1, align="right")
    setc(wh, f"N{r}", "Âncora da D&A por GW (capa): ~4,1-4,7.", F_NOTE)
    r += 1
    label(wh, r, "Juros anualizados ÷ dívida bruta de fim de período (memo)")
    for q in ("4Q25", "2Q26"):
        c = HCOLS[HQ.index(q)]
        setc(wh, f"{c}{r}", f"=-{c}14*4/{c}{act_row+5}", F_TXT, nf=NF_PCT, align="right")
    setc(wh, f"N{r}", "4Q25 ~7,2% e 2Q26 ~7,2% sobre o principal de FIM de período (dívida cresceu no período; juros capitalizados excluídos) — taxas efetivas contratuais 9-11%.", F_NOTE)


# ================================================================================================= Dívida sheet
DEBT = [
    ("Recourse", "DDTL 1.0 Facility", "mar-2028", 0.15, 1300, 1553),
    ("Recourse", "DDTL 2.0 Facility", "ago-2030", 0.11, 3190, 5037),
    ("Recourse", "DDTL 2.1 Facility", "mar-2031", 0.09, 3000, 2741),
    ("Recourse", "DDTL 3.0 Facility", "ago-2030", 0.09, 2215, 340),
    ("Recourse", "DDTL 5.0 Facility (SOFR + 4,50%, mai-26)", "nov-2031", 0.09, 1101, 0),
    ("Recourse", "2030 Senior Notes (9,25%)", "jun-2030", 0.10, 2000, 2000),
    ("Recourse", "2031 9,00% Senior Notes", "fev-2031", 0.10, 1750, 1750),
    ("Recourse", "2031 9,75% Senior Notes (abr-26)", "out-2031", 0.10, 2750, 0),
    ("Recourse", "2032 9,625% Senior Notes (jun-26)", "jul-2032", 0.10, 1250, 0),
    ("Recourse", "2032 EUR Senior Notes (8,50%, €2,0 bi, swap p/ US$)", "jul-2032", 0.09, 2279, 0),
    ("Recourse", "2031 Convertible Senior Notes (1,75%)", "dez-2031", 0.02, 2588, 2588),
    ("Recourse", "2032 Convertible Senior Notes (1,75%; conv. $119,60; cap call $230)", "out-2032", 0.02, 4000, 0),
    ("Recourse", "Convertible Promissory Notes", "abr-2026", 0.07, 0, 168),
    ("Recourse", "Revolving Credit Facility", "nov-2029", 0.07, 0, 1000),
    ("Recourse", "OEM and Software License Financing Arrangements", "dez-26 a jul-30", 0.11, 4220, 3518),
    ("Recourse", "Magnetar Loan", "jan-2029", 0.12, 189, 273),
    ("Non-recourse", "DDTL 4.0 Facility (SOFR + 2,25% / UST + 2,00%; Meta take-or-pay)", "mar-2032", 0.07, 2837, 0),
    ("Non-recourse", "OEM and Software License Financing Arrangements", "ago-26 a ago-28", 0.09, 882, 647),
]
PRINCIPAL = [("Restante de 2026", 4413), ("2027", 6184), ("2028", 4416), ("2029", 2421), ("2030", 3221), ("Depois", 14896)]


def build_divida(wd):
    wd.sheet_view.showGridLines = False
    wd.column_dimensions["A"].width = 2.25; wd.column_dimensions["B"].width = 2.25; wd.column_dimensions["C"].width = 14
    wd.column_dimensions["D"].width = 66; wd.column_dimensions["E"].width = 16; wd.column_dimensions["F"].width = 14; wd.column_dimensions["G"].width = 14; wd.column_dimensions["H"].width = 14
    setc(wd, "C2", "CRWV | Dívida (10-Q 2Q26, nota 10 — principal, US$ milhões)", F_TITLE)
    setc(wd, "C3", "Fonte: CRWV/CRWV_10-Q_2026-08-12 nota 10 (total debt obligations; future principal payments). Taxas = 'effective interest rates' da tabela.", F_TXT)
    for j, h in enumerate(["Tipo", "Instrumento", "Vencimento", "Taxa efetiva", "30-jun-2026", "31-dez-2025"]):
        setc(wd, f"{get_column_letter(3+j)}5", h, F_TXTB, fill=FILL_HDR, align="center")
    r = 6
    for typ, name, mat, rate, v26, v25 in DEBT:
        setc(wd, f"C{r}", typ, F_TXT); setc(wd, f"D{r}", name, F_TXT); setc(wd, f"E{r}", mat, F_TXT, align="center")
        setc(wd, f"F{r}", rate, F_INPUT, nf="0%", align="right"); setc(wd, f"G{r}", v26, F_INPUT, nf=NF_NUM, align="right"); setc(wd, f"H{r}", v25, F_INPUT, nf=NF_NUM, align="right")
        r += 1
    setc(wd, f"D{r}", "Total principal (recourse + non-recourse)", F_TXTB); setc(wd, f"G{r}", f"=SUM(G6:G{r-1})", F_TXTB, nf=NF_NUM, align="right"); setc(wd, f"H{r}", f"=SUM(H6:H{r-1})", F_TXTB, nf=NF_NUM, align="right"); tot = r; r += 1
    setc(wd, f"D{r}", "Taxa efetiva média ponderada (jun-26)", F_TXT); setc(wd, f"G{r}", f"=SUMPRODUCT(F6:F{tot-1},G6:G{tot-1})/G{tot}", F_TXT, nf=NF_PCT, align="right"); r += 1
    setc(wd, f"D{r}", "Check: total da nota = 35.551 (jun-26) / 21.615 (dez-25)", F_NOTE); setc(wd, f"G{r}", f"=G{tot}-35551", F_TXT, nf=NF_CHK, align="right"); setc(wd, f"H{r}", f"=H{tot}-21615", F_TXT, nf=NF_CHK, align="right"); r += 1
    setc(wd, f"D{r}", "Menos: desconto e custos não amortizados (jun-26: 427 + 56)", F_NOTE); setc(wd, f"G{r}", -483, F_INPUT, nf=NF_NUM, align="right"); r += 1
    setc(wd, f"D{r}", "Valor contábil (recourse 31.405 + non-recourse 3.663 = 35.068)", F_NOTE); setc(wd, f"G{r}", f"=G{tot}+G{r-1}", F_TXT, nf=NF_NUM, align="right"); r += 2
    setc(wd, f"D{r}", "Amortização de principal (jun-26)", F_TXTB, fill=FILL_HDR); setc(wd, f"G{r}", "US$ mi", F_TXTB, fill=FILL_HDR, align="center"); r += 1
    p0 = r
    for lab, v in PRINCIPAL:
        setc(wd, f"D{r}", lab, F_TXT); setc(wd, f"G{r}", v, F_INPUT, nf=NF_NUM, align="right"); r += 1
    setc(wd, f"D{r}", "Total", F_TXTB); setc(wd, f"G{r}", f"=SUM(G{p0}:G{r-1})", F_TXTB, nf=NF_NUM, align="right"); r += 2
    notes = [
        "Juros 2Q26: contratuais 592 + amortização de desconto 45 − capitalizados 79 = 558 (nota 10); 'interest expense, net' na DRE = 640. Guia 3Q26: $860-940 mi. 1H26 caixa pago 806.",
        "Arrendamentos operacionais (jun-26): PV 16.319 (taxa 10%, 12 anos); pagamentos futuros 29.135; não iniciados 35.500 (um único site = 14.700, 393 MW a entregar). Aluguel está no EBITDA — não somar à dívida.",
        "Spreads das DDTLs (Redburn 09-21, Fig 70): S+962 (jul-23), +425 (set-24), +400 (OpenAI, jul-25), +225 (Meta, mar-26), +450 (não-IG, mai-26), +550 (ago-26, $2,6 bi DDTL 5.5, set-31). Term loan S+550 rende 9,15% (MS Credit 08-20).",
        "Capital levantado: >$32 bi dívida + equity até 2Q26 (call 08-11); WACD −300 bp em 12 meses (~$1,1 bi/ano de juros). Rating S&P B+ positivo (abr-26). ATM registrado, 'not at these prices' (Robbins 09-21).",
        "Conversível 2031: 9,2764 ações por $1.000 (conv. $107,80; cap call strike 107,80 / cap 215,60 — 10-K FY25). Conversível 2032: 8,3612 ações por $1.000 (conv. $119,60); cap calls custo 492 mi, strike 119,60 / cap 230. Gestão: strike efetivo ~$200. Ambos tratados como dívida no modelo (fora do dinheiro a $77,81).",
        "Eventos subsequentes (10-Q 2Q26 nota 16): ago-26 DDTL 5.5 de $2,6 bi (JPMorgan agente; SOFR+550, vence set-31) e saque de $1,2 bi no Revolving Credit Facility — NÃO estão na dívida líquida de 30-jun-26 do modelo (o saque financia o capex do 2H26 já descontado no FCFF).",
    ]
    for t in notes:
        setc(wd, f"D{r}", t, F_NOTE); r += 1


if __name__ == "__main__":
    path = os.path.join(OUT, "Template DCF CRWV.xlsx")
    lay = build(path)
    print("built", path)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk in ('ps', 'ev', 'fcff', 'ebitda', 'nd', 'eps', 'end')}) for k, v in lay.items() if k != 'R'}, indent=0))
