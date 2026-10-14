# -*- coding: utf-8 -*-
"""Template DCF CRWV.xlsx — official CoreWeave model in the 'Template DCF <TICKER>.xlsx' family (AMD/AVGO/ADV/TER structure),
labels in ENGLISH (Felipe, 2026-10-14: "Keep all in english").
Driver: active IT-load power (MW) -> billable power (1-quarter lag) x realised revenue per GW-year -> adj. EBITDA -> D&A per GW
-> EBIT -> NOPAT; capex = growth (build cost per GW, with a pre-build share of next year's adds) + replacement (everything installed
in t-life, adds and prior replacements, at a replacement share of the current build cost); FCFF -> DCF (WACC x g grid) + two Excel
Data Tables (revenue/GW x EBITDA margin; replacement life x replacement cost) created by COM in recalc_verify.py.
Sheets: DCF Cover - Base, Assumptions & sources, History, Debt. openpyxl writes formulas only; Excel COM recalculates.
Rule: no TEXT cell may start with '='.
"""
import datetime as dt, os, json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2023, 2046))
COLS = [get_column_letter(4 + i) for i in range(len(YEARS))]   # D..Z
BASE = {2023, 2024, 2025}
SH_COVER = "DCF Cover - Base"
SH_PREM = "Assumptions & sources"
SH_HIST = "History"
SH_DEBT = "Debt"
P = f"'{SH_PREM}'!"
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
        setc(ws, f"{COLS[i]}{r}", f"CY{str(y)[2:]}{'A' if y in BASE else 'E'}", F_TXTB, fill=FILL_HDR, align="center")


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
        setc(ws, "C2", f"{ticker} | Assumptions & sources", F_TITLE, align="left")
        setc(ws, "C3", unit_line, F_TXT, align="left")
        setc(ws, "C4", "Blue = HARD input (filing / consensus); yellow = PARTIAL assumption (sourced range, point is ours); salmon = ESTIMATE (no source). Source in column L (tables) or AB (series).", F_NOTE, align="left")
        for i, y in enumerate(range(2023, 2029)):
            setc(ws, f"{COLS[i]}5", y, F_TXTB, nf="0", fill=FILL_HDR, align="center")
        setc(ws, "L6", "File, sheet and source cells. CY = calendar year (= CoreWeave's fiscal year).", F_NOTE, align="left")
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


# ===================================================================================================== inputs (US$ mm)
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
SH = fill_years({}, 2026, 603.4)


def build(path):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = SH_COVER
    wp = wb.create_sheet(SH_PREM)
    wh = wb.create_sheet(SH_HIST)
    wd = wb.create_sheet(SH_DEBT)
    pr = Prem(wp, "CRWV", "Data taken from the sources named. US$ millions unless stated; power in MW (critical IT load, the company's basis); revenue per GW and build cost per GW in US$ billions per GW. Fiscal year = calendar year.")

    # ------------------------------------------------------------------ reference tables (2023..2028 in D..I)
    pr.section("Reported history (10-K FY25, 10-Q 2Q26) and BBG consensus (2026-10-13)")
    pr.ref("rev_ref", "Revenue (US$ m) | 10-K FY23-25 / BBG consensus CY26-28", [REV[2023], REV[2024], REV[2025], CONS["rev"][2026], CONS["rev"][2027], CONS["rev"][2028]],
           "10-K FY25 (CRWV/CRWV_10-K_2026-03-02): 229 / 1,915 / 5,131. CY26-28: _wiki/_data/estimates.json CRWV CY2026 / CY2027 / 3FY (BEst 2026-10-13; 47 analysts, 33 buy / 10 hold / 4 sell).")
    pr.ref("ebitda_ref", "Adjusted EBITDA (US$ m) | company / consensus", [None, 1226, 3098, CONS["ebitda"][2026], CONS["ebitda"][2027], CONS["ebitda"][2028]],
           "FY24: 64% margin (DB CRWV unit economics 2025-06-16) x 1,915 = 1,226 (PARTIAL). FY25 = sum of quarters: 1Q25 ~609 (1Q26 ~1,164 = 56% x 2,078, '+91% y/y', call 2026-05-07 — PARTIAL) + 2Q 753 + 3Q 838 + 4Q 898 (calls). CY26-28 BEst EBITDA.")
    pr.ref("aoi_ref", "Adjusted operating income (AOI, US$ m) | consensus EBIT CY26-28", [None, None, None, CONS["ebit"][2026], CONS["ebit"][2027], CONS["ebit"][2028]],
           "BEst EBIT (estimates.json). FY26 guide (call 2026-08-11): AOI $960-1,150m; 3Q26 $200-260m.")
    pr.ref("ni_ref", "GAAP net income (US$ m) | 10-K / consensus", [-594, -863, -1167, CONS["ni"][2026], CONS["ni"][2027], CONS["ni"][2028]], "10-K FY25 (net loss); BEst NI CY26-28.")
    pr.ref("eps_ref", "GAAP diluted EPS (US$) | 10-K / consensus", [-3.09, -4.30, -2.81, CONS["eps"][2026], CONS["eps"][2027], CONS["eps"][2028]],
           "10-K FY25 p.1508: net loss per share attributable to common stockholders, diluted: (3.09) / (4.30) / (2.81) (two-class method; post 20:1 split of Mar-25). CY26-28 BEst EPS (ex-SBC).", nf=NF_NUM2)
    pr.ref("da_ref", "Depreciation and amortization (US$ m)", [103, 863, 2454, 2540], "10-K cash flow FY23-25; 1H26 = 2,540 (10-Q 2Q26). 2026 column = 1H26 (memo).")
    pr.ref("sbc_ref", "Stock-based compensation (US$ m)", [15, 31, 630, 318], "10-K cash flow (FY25 includes $177m of RSUs vested at the IPO); 1H26 = 318 (memo).")
    pr.ref("capex_ref", "Cash capex (US$ m) | 10-K / BBG consensus CY26-28", [2943, 8702, 10309, CONS["capex"][2026], CONS["capex"][2027], CONS["capex"][2028]],
           "10-K 'Purchase of property and equipment' 2,943 / 8,702 / 10,309 (FY25 company basis ~$14bn incl. OEM financing: 3Q25 guide $12-14bn). CY26-28 BEst capex. FY26 guide (company basis): $35-39bn.")
    pr.ref("int_ref", "Net interest expense (US$ m)", [28, 361, 1229, 1176], "10-K FY23-25; 1H26 = 1,176 (10-Q 2Q26). 3Q26 guide: $860-940m.")
    pr.ref("power_ye", "Active power at year-end (MW, IT load)", [70, 360, 850, 1500], "10-K FY25 p.194: ~70 MW (Dec-23), ~360 MW (Dec-24), >850 MW (Dec-25). 2026 column = Jun-26: 1.5 GW (call 2026-08-11). YE26 guide: >1.85 GW.")
    pr.ref("contracted", "Contracted power (MW)", [None, None, 3100, 4200], "10-K FY25: ~3.1 GW (Dec-25). Call 2026-08-11: 3.7 GW at 2Q-end, 4.2 GW as of 11-Aug-26 (2026 column). Target: >=8 GW active by 2030.")
    pr.ref("rpo_ref", "Unsatisfied RPO (US$ m)", [None, None, 60700, 103700], "10-K FY25: $60.7bn (43% within 24 months). 10-Q 2Q26: $103.7bn, 41% in the 24 months to Jun-28, 39% months 25-48, balance months 49-78. Backlog (company metric): $66.8bn Dec-25 / $104bn Jun-26.")
    pr.ref("defrev", "Total deferred revenue (US$ m) | Dec-24 / Dec-25 / Jun-26", [None, 4064, 8185, 9692], "10-K FY25 balance sheet (769+3,295; 1,709+6,476); 10-Q 2Q26 (2,686+7,006). Customer prepayments = 15-25% of TCV (UBS 2026-09-22).")
    pr.ref("ar", "Accounts receivable (US$ m) | Dec-24 / Dec-25 / Jun-26", [None, 417, 3169, 2541], "10-K FY25; 10-Q 2Q26.")
    pr.ref("cash_ref", "Cash and equivalents (US$ m) | Dec-24 / Dec-25 / Jun-26", [None, 1361, 3127, 5524], "10-K FY25; 10-Q 2Q26. Additional restricted cash: 1,003 (Dec-25: 819 + 184) / 1,380 (Jun-26: 873 + 507) — debt-service coverage, excluded from net cash.")
    pr.ref("debt_ref", "Gross debt, principal (US$ m) | Dec-24 / Dec-25 / Jun-26", [None, 7926, 21615, 35551], "10-K FY25 note 10 (Dec-24 carrying value 7,926; Dec-25 carrying 21,373 + discount 242 = 21,615). 10-Q 2Q26 note 10: total principal 35,551 (recourse + non-recourse). See Debt sheet.")
    pr.ref("leases_ref", "Operating lease liabilities (US$ m) | Dec-24 / Dec-25 / Jun-26", [None, 2602, 8195, 16319], "10-K FY25; 10-Q 2Q26 (10% rate, 12-year term). Plus $35.5bn of leases not yet commenced (Jun-26). Rent sits in EBITDA — NOT added to net debt.")

    pr.section("FY26 guidance (2Q26 call, 2026-08-11) — company basis")
    pr.single("g_rev_lo", "FY26 revenue — low end (US$ m)", 12400, "Call 2026-08-11: $12.4-13.2bn (raised from $12.0-13.0bn in Feb-26).", fill=None)
    pr.single("g_rev_hi", "FY26 revenue — high end (US$ m)", 13200, "Same.", fill=None)
    pr.single("g_aoi_lo", "FY26 AOI — low end (US$ m)", 960, "Call 2026-08-11: $960-1,150m (from $900-1,100m).", fill=None)
    pr.single("g_aoi_hi", "FY26 AOI — high end (US$ m)", 1150, "Same.", fill=None)
    pr.single("g_capex_lo", "FY26 capex — low end (US$ m, company basis)", 35000, "Call 2026-08-11: $35-39bn (from $31-35bn). 1H26 reported: 6.8 + 9.4 = $16.2bn (cash: 14.1).", fill=None)
    pr.single("g_capex_hi", "FY26 capex — high end (US$ m)", 39000, "Same.", fill=None)
    pr.single("g_power_ye", "Active power YE26 — guide (MW)", 1850, "Call 2026-08-11: '>1.85 GW' (from >1.7 GW). UBS 09-22: 1,900 MW FY26E, 3,200 FY27E, 4,720 FY28E, 6,320 FY29E, 8,000 FY30E.", fill=None)
    pr.single("g_q3_rev", "3Q26 revenue — midpoint (US$ m)", 3525, "Call 2026-08-11: $3.45-3.60bn; 3Q AOI $200-260m; 3Q interest $860-940m; 3Q capex $11.5-13.5bn.", fill=None)
    pr.single("h1_rev", "1H26 reported revenue (US$ m)", 4653, "10-Q 2Q26: 2,078 + 2,575.", fill=None)
    pr.single("h1_aoi", "1H26 reported AOI (US$ m)", 149, "Calls: 1Q26 $21m + 2Q26 $128m.", fill=None)
    pr.single("bill_2026", "Average billable power 2026 (MW) — quarterly build", 1124, "Average over four quarters of the PRIOR quarter's average active power (UBS 09-22: 'it takes about a quarter for active power to generate revs'): 1Q (590+850)/2=720; 2Q (850+1,000)/2=925; 3Q (1,000+1,500)/2=1,250; 4Q (1,500+1,700)/2=1,600 (3Q26 YE estimated 1,700). Average 1,124. Overrides the annual formula in 2026 (adds were front-loaded in 1H).", fill=FILL_ASSUM)

    pr.section("Revenue-per-GW marks (US$ bn per IT-load GW per YEAR) — wiki ledger; NEVER net different bases")
    pr.single("m_ubs", "Realised on the installed book (UBS, 09-22)", 11.0, "UBS Keirstead 2026-09-22: 2Q26 $2.575bn x4 / 925 MW average active power in 1Q26 = ~$11bn/GW; 'closer to $15bn by end of 2027'. This model: 2026 implied by the guide = ~11.4.", nf=NF_NUM1, fill=None)
    pr.single("m_mgmt", "Floor for new long-dated contracts (4-6 years) — management", 15.5, "Nick Robbins (VP Corp Dev) @ BTG Pactual, 2026-09-21: mid-teens $/W/year is 'the absolute floor'; long-dated Vera Rubin 'clearing higher'. Seller of the capacity, not audited.", nf=NF_NUM1, fill=None)
    pr.single("m_nscale", "Nscale's filed book (S-1 2026-09-18) — blended / VR tranche", 13.2, "Nscale S-1: $103.4bn TCV / 5.7 years / 1.37 GW IT = ~$13.2bn/GW-year; Anthropic Vera Rubin tranche ~$16.2bn. Read by the wiki as the CEILING of a contracted book (open conflict with management).", nf=NF_NUM1, fill=None)
    pr.single("m_short", "Short-dated contracts (3-6 months) — annualised", 40.0, "Robbins 09-21: 'about $40 million a megawatt' on short-dated contracts for PRIOR generations (Blackwell / Grace Blackwell), term and time basis not stated; JPM 09-24 repeats the print without a basis; only UBS 09-22 gives the term (3-6 months) and the annualised basis ($40bn/GW). Small slice of the book. Arete 08-21: $20-25m/MW on 2-3-year contracts.", nf=NF_NUM1, fill=None)
    pr.single("m_ratio", "Revenue / capex on a 5-year contract (management)", 2.0, "Robbins 09-21: 'historically… two to one ratio for a five-year deal between revenue and capex', 'expanded' since early 2026. 2:1 over 5 years on $40bn/GW = $16bn/GW-year.", nf=NF_NUM1, fill=None)
    pr.single("m_hedgeye", "Bear memo: monetisation per connected MW did not improve in 2025 (Hedgeye, Dec-25)", 0, "HE Global Technology BB, Dec-2025 (short since Apr-25). This model's quarterly calibration: 2Q25 ~12.4 → 2Q26 ~11.1 US$bn/GW (History sheet) — revenue per installed GW FELL as the fleet scaled.", nf=NF_NUM1, fill=None, font=F_NOTE)

    pr.section("Build cost per GW (CoreWeave's capex; it leases the shell) — US$ bn per IT-load GW")
    pr.single("c_ubs_bw", "Blackwell — UBS", 35.0, "UBS 09-22: 'capex to CoreWeave might be closer to $35bn per Blackwell-based GW and $40bn per Vera Rubin-based GW' (Crusoe all-in $57bn/GW, $30bn of it GPUs).", nf=NF_NUM1, fill=None)
    pr.single("c_ubs_vr", "Vera Rubin — UBS", 40.0, "Same. Arete 08-21: VR NVL72 racks 70-80% more expensive than Blackwell, ~+20% GPU capex per MW.", nf=NF_NUM1, fill=None)
    pr.single("c_back", "Backward check: 2024-26 capex / 1.85 GW", 34.0, "UBS: $62bn of 2024-26 capex to stand up 1.85 GW by YE26 = $34bn/GW ('flattered' — part of 2026 capex buys 2027 capacity). Calibration basis for the pre-build share.", nf=NF_NUM1, fill=None)

    pr.section("Valuation and balance sheet")
    pr.single("val_date", "Valuation date", dt.datetime(2026, 6, 30), "Same as the balance-sheet date (30-Jun-26). DEVIATION from the family convention (27-Aug-26): with ~$26bn/year of cash burn, valuing in August against June net debt would leave ~$5.6bn of July-August burn out of the bridge (~−$9/share; double-check 2026-10-14). Update both together at the 10-Q 3Q26.", nf=NF_DATE)
    pr.single("wacc", "WACC", 0.10, "Family convention (10%), kept for comparability — but for CRWV it is a SUBSIDY: with no tax shield (NOLs; 5% cash tax to 2028) Kd 10% x 65% + Ke 14% x 35% = 11.4%; at market weights (net debt 30bn vs market cap 43bn) 12-13%. Arete 11%; Redburn Ke 20%. See the WACC x g grid: 11% and 12% are the honest reading.", nf=NF_PCT)
    pr.single("g", "Terminal growth", 0.02, "Template DCF NVDA.xlsx | Capa DCF - Base!D91.", nf=NF_PCT)
    pr.single("roic", "Terminal incremental ROIC", 0.08, "ESTIMATE. The template uses 20%; here 8% because a new GW costs ~$40bn and generates NOPAT of ~$2-3bn (5-7% gross). See the 'implied incremental ROIC' row on the cover. Sensitivity in the grid.", nf=NF_PCT, fill=FILL_EST)
    pr.single("shares", "Diluted shares (m) | 551 outstanding + 29 RSUs + 23.4 options (treasury)", 603.4, "10-Q 2Q26: 457m class A + 94m class B (30-Jun-26); 29m unvested RSUs/RSAs; 24m options at $1.84 (intrinsic value $2,341m) → treasury method at $77.81 = 23.4m. Out-of-the-money converts (2031: $107.80 / cap $215.60; 2032: $119.60 / cap $230) stay in debt. No ATM (management 09-21: 'not at these prices').", nf=NF_NUM1, fill=None)
    pr.single("cash", "Cash + securities, unrestricted (US$ m, 30-Jun-26)", 5539, "10-Q 2Q26: cash 5,524 + securities 15. Restricted cash 1,380 excluded (mandatory interest/principal coverage under the DDTLs).", nf=NF_NUM1, fill=None)
    pr.single("debt", "Gross financial debt, principal (US$ m, 30-Jun-26)", 35772, "10-Q 2Q26 note 10: principal 35,551 (DDTLs, senior notes, converts, OEM financing, Magnetar) + finance leases 221. Operating leases (16,319) NOT added: rent already sits in EBITDA.", nf=NF_NUM1, fill=None)
    pr.single("bs_date", "Balance-sheet date used in the model", dt.datetime(2026, 6, 30), "Update at the 10-Q 3Q26.", nf=NF_DATE, fill=None)
    pr.single("px", "Reference price (US$, informational)", PX, "BBG PX_LAST CRWV US, 2026-10-13 (estimates.json). Not used in the valuation.", nf=NF_NUM2, fill=None)
    pr.single("pt_cons", "Consensus average PT (US$, informational)", PT_CONS, "BBG BEST_TARGET_PRICE, 47 analysts (hi 278 / lo 39), 2026-10-13. UBS Buy $120; JPM OW $125; Bernstein UP $74; Redburn Sell $54; Arete Buy $317.", nf=NF_NUM2, fill=None)
    pr.single("mktcap", "Market cap (US$ m, informational)", MKTCAP, "BBG 2026-10-13.", nf=NF_NUM, fill=None)
    pr.single("nd_2025", "Net debt Dec-25 (US$ m) — anchor of the debt roll", 18488, "Principal 21,615 − cash 3,127 (10-K FY25). Used only in the debt/EPS memo block, not in the DCF.", nf=NF_NUM, fill=None)
    pr.single("eq_2026", "Equity raised in 2026 (US$ m, net of capped calls)", 2490, "10-Q 2Q26 cash flow: private placements 2,982 (NVDA $2bn at $87.20 in Jan-26 + Jane Street $1bn) − capped calls 492. No ATM assumed in 2H26.", nf=NF_NUM, fill=None)
    pr.single("lag", "Lag from active power to billing (years)", 0.25, "UBS 09-22: ~1 quarter (GPU install/test ~6 weeks after energising). Average billable power = prior YE + (0.5 − lag) x adds (uniform adds).", nf=NF_NUM2)
    pr.single("prebuild", "Share of the year's capex that buys NEXT year's capacity", 0.20, "Calibrated: FY26 guide $37bn (mid) vs formula 33 x (0.8 x 1.05 GW + 0.2 x 1.3 GW) = 36.3 (−1.9%; the current-year build cost also prices the pre-built share). UBS: backward check 'flattered' by 2026 capex buying 2027.", nf=NF_PCT)
    pr.single("life", "Useful life for replacement (years) — INPUT ON THE COVER, F6 (memo)", f"='{SH_COVER}'!F6", "CoreWeave GPU depreciation: 6 years (10-K; MS AI Factories). Replacement in t = everything installed in t−6 (adds and replacements). Re-contracting in years 5-6 at 50-75% of ASP (DB 2025-06-16) is the optimistic side — sensitise 8 years.", nf="0", fill=None, font=F_LINK)
    pr.single("repl", "Replacement cost (% of the year's build cost) — INPUT ON THE COVER, G6 (memo)", f"='{SH_COVER}'!G6", "ESTIMATE: the shell is leased; GPUs/servers/network (~80% of capex) are replaced, part of the MEP/fit-out is kept.", nf=NF_PCT, fill=None, font=F_LINK)
    pr.single("g_fleet", "Fleet growth after 2035 (% of prior YE)", 0.03, "ESTIMATE: adds = 3% of the prior year's active power from 2036.", nf=NF_PCT, fill=FILL_EST)

    pr.section("Assumptions by year (CY)")
    pr.year_hdr()
    adds = {y: ADDS_IN[y] for y in ADDS_IN}
    pr.series("adds", "Active power additions (MW, IT load)", adds, "2026: +1,050 → YE 1,900 (guide >1,850; UBS 1,900; 1.5 GW already in Jun-26). 2027-30: 1,300 / 1,500 / 1,600 / 1,700 → 3.2 / 4.7 / 6.3 / 8.0 GW = UBS 09-22 path to management's ≥8 GW-by-2030 target. Contracted 4.2 GW + 1.5 GW powered land = ~6 GW visible (call 08-11). 2031-35 ESTIMATE: decelerates to 800 MW/year; 2036+ formula (g_fleet).", nf=NF_NUM, hard_fill=FILL_ASSUM)
    for y in range(2031, 2036):
        wp[f"{COLS[YEARS.index(y)]}{pr.rows['adds']}"].fill = FILL_EST
    pr.series("revgw", "Revenue per billable GW (US$ bn / GW-year), base", REVGW, "2026 implied by the guide = 12,800 / 1,124 MW = ~11.4 (cover). 2027 12.0 → 2030 13.0: blend of the legacy book (~11) with new long-dated contracts at mid-teens (management 09-21; Nscale 13.2-16.2) and a short-dated slice at ~40. UBS: ~15 at the 2027 EXIT; UBS 2030 target $85bn / ~6.7 GW billable = 12.7. 2031-33 rises to 14.0 and stays flat nominal: the legacy book (2025-26, ~2 GW at ~11) is re-contracted and the fleet becomes mostly 2027+ vintages contracted at >=15; 14.0 is BELOW every forward mark (management floor 15-16, Nscale VR 16.2, UBS 15 exit-27). PARTIAL.", nf=NF_NUM1)
    pr.series("ebitda_m", "Adjusted EBITDA margin", EBITDA_M, "2026 57.5%: 1H 57.6% (2.71bn / 4.65) + implied 2H (AOI guide 1,055 − 149 + D&A ~3.6bn) ≈ 56%; consensus 58.6%. 2027-28 62/64% (consensus 62.9/66.1%). LT 62%: between the contract-level mid-70s (management) and the long-term 25-30% operating-margin target after D&A (4Q25 call). DC rent (leases) and overhead sit here.", nf=NF_PCT)
    pr.series("da_gw", "D&A per average active GW (US$ bn / GW-year)", DA_GW, "Calibrated: FY25 2,454 / 605 MW average = 4.1; 1H26 annualised 5,080 / ~1,090 MW = 4.7. VR at $40bn/GW with mixed 6-15-year lives → ~5.0-5.5. 5.0 flat (PARTIAL). Drives EBIT/EPS, not FCFF (only through tax).", nf=NF_NUM1)
    pr.series("sbc", "SBC / revenue (deducted in EBIT after SBC)", SBC, "FY25 12.3% (includes $177m from the IPO); 1H26 6.8%. 5% → 2% LT. The company's AOI EXCLUDES SBC; the FCFF here deducts it.", nf=NF_PCT)
    pr.series("tax", "Cash tax rate on EBIT", TAX, "NOLs >$3bn (DB 2025-06-16); GAAP provision positive despite losses (146m in 1H26 — state/foreign). 5% to 2028, 21% from 2031.", nf=NF_PCT)
    pr.series("build", "Build cost per GW added (US$ bn / GW)", BUILD, "2026 33 (Blackwell; UBS 35 / backward check 34), 2027 38, 2028+ 40 (Vera Rubin, UBS). Flat nominal after 2028: memory/rack inflation vs density gains. PARTIAL.", nf=NF_NUM1)
    pr.series("nwc", "Operating NWC / revenue = (receivables − deferred revenue) / revenue", NWC, "Dec-25: (3,169 − 8,185) / 5,131 = −98%; Jun-26: (2,541 − 9,692) / LTM 7,590 = −94%. Prepayments (15-25% of TCV) scale with bookings, not revenue: the ratio compresses to −35% by 2030 (ESTIMATE — the only anchor is the prepayment %). Cash inflow = 35-70% of the revenue increment; UBS implies much larger inflows (12/27E net debt $56.5bn vs ~$80bn here).", nf=NF_PCT, hard_fill=FILL_EST)
    pr.series("kd", "Average cost of debt (memo, debt/EPS block)", KD, "10-Q 2Q26: effective rates 9-11% (DDTLs 9-15%, notes 9-10%, DDTL 4.0 7%, converts 2%). 1H26 interest 1,176 / average debt ~29bn = 8.1% + capitalised. UBS: every 100bp = ~$30m/quarter.", nf=NF_PCT)
    pr.series("sh", "Diluted shares for EPS (m, year average)", SH, "603.4 flat: no ATM, net SBC dilution ~1%/year ignored. The 2032 convert only dilutes above ~$200 (capped call).", nf=NF_NUM1)

    pr.text("")
    pr.text("Method: revenue = average billable power (prior YE + (0.5 − lag) x adds; 2026 from the quarterly build) x revenue per GW. EBITDA = revenue x margin. D&A = average active power x D&A/GW. FCFF = (EBITDA − D&A − SBC) x (1 − tax) + D&A − capex − change in NWC.")
    pr.text("Capex = growth [build cost x ((1 − pre-build) x adds of the year + pre-build x adds of the next year)] + replacement [power installed in t−life (adds AND prior replacements) x build cost x replacement % — at steady state replacement ≈ fleet ÷ life]. 2023-25 = reported cash capex; 2026 = guide (midpoint).")
    pr.text("Terminal: NOPAT x (1 + g) x (1 − g / ROIC). End-of-year discounting; CY26 pro rata for the days after the valuation date. Net debt = principal + finance leases − unrestricted cash (30-Jun-26).")
    pr.text("GW bases: ALL CoreWeave power is critical IT load (UBS 09-22) — never compare with facility GW (10-25% larger; Galaxy Helios 526 MW IT = 800 MW gross). Revenue/GW, build cost/GW and D&A/GW are three different bases — never net them.")
    pr.text("Primary sources: 10-K FY25 (2026-03-02), 10-Qs 1Q25-2Q26, calls 2Q25-2Q26 (CRWV/transcripts), BTG Pactual websession with Nick Robbins 2026-09-21 (Capstone notes). Sell-side: UBS 09-22, JPM 09-24, Arete 08-21, Bernstein 07-01/09-24, DB 2025-06-16, Redburn 09-21. BBG consensus 2026-10-13.")

    R = pr.rows
    Pc = lambda key, c: f"{P}{c}{R[key]}"
    Ps = lambda key: f"{P}$D${R[key]}"

    # ================================================================================================= Cover
    setup_sheet(ws, "CRWV | Power-driven DCF (IT-load GW x revenue per GW)",
                "US$ millions, except power (MW), revenue/GW, build cost/GW and D&A/GW (US$ billions per GW) and shares (millions). Horizon CY2023–2045; fiscal year = calendar year.",
                "Blue / yellow: assumptions (Assumptions & sources sheet; salmon = no source). Green: internal sources. CY23–25A: reported bases (10-K). 2026: company guide.")
    year_header(ws, 5)
    label(ws, 6, "Grid inputs: D6 revenue/GW multiplier 2027+ (1.00 = base) | E6 EBITDA-margin adjustment 2027+ (pp) | F6 replacement life (years) | G6 replacement cost (% of build)")
    setc(ws, "D6", 1.0, F_INPUT, nf=NF_NUM2, fill=FILL_ASSUM, align="right"); setc(ws, "E6", 0.0, F_INPUT, nf='+0.0%;-0.0%;0.0%', fill=FILL_ASSUM, align="right")
    setc(ws, "F6", 6, F_INPUT, nf='0" yrs"', fill=FILL_ASSUM, align="right"); setc(ws, "G6", 0.80, F_INPUT, nf=NF_PCT, fill=FILL_EST, align="right")

    header_row(ws, 7, "Capacity | active power (critical IT load, MW) and billable power")
    label(ws, 8, "Active power at year-end (MW)")
    row_formula(ws, 8, lambda i, c, pc: f"={Pc('power_ye', c)}" if YEARS[i] in BASE else f"={pc}8+{c}9", nf=NF_NUM)
    for i in range(3): ws[f"{COLS[i]}8"].font = F_LINK
    label(ws, 9, "Active power added in the year (MW)")
    row_formula(ws, 9, lambda i, c, pc: (f"={c}8" if i == 0 else f"={c}8-{pc}8") if YEARS[i] in BASE else (f"={Pc('adds', c)}" if YEARS[i] <= 2035 else f"={pc}8*{Ps('g_fleet')}"), nf=NF_NUM)
    for i in range(3, NY): ws[f"{COLS[i]}9"].font = F_LINK
    label(ws, 10, "Average active power in the year (MW) — D&A basis")
    row_formula(ws, 10, lambda i, c, pc: f"=({pc}8+{c}8)/2", nf=NF_NUM, start=1)
    label(ws, 11, "Average billable power (MW) = prior YE + (0.5 − lag) x adds | 2026: quarterly build")
    row_formula(ws, 11, lambda i, c, pc: f"={Ps('bill_2026')}" if YEARS[i] == 2026 else f"={pc}8+(0.5-{Ps('lag')})*{c}9", nf=NF_NUM, start=1)
    ws["G11"].font = F_LINK
    label(ws, 12, "Revenue per billable GW (US$ bn / GW-year) | CY24-26 implied")
    row_formula(ws, 12, lambda i, c, pc: f"={c}15/{c}11" if YEARS[i] <= 2026 else f"={Pc('revgw', c)}*$D$6", nf=NF_NUM1, start=1)
    for i in range(4, NY): ws[f"{COLS[i]}12"].font = F_LINK
    label(ws, 13, "Memo: revenue per average ACTIVE GW (US$ bn / GW-year) — alternative, lower basis")
    row_formula(ws, 13, lambda i, c, pc: f"={c}15/{c}10", nf=NF_NUM1, start=1)

    header_row(ws, 14, "Revenue (US$ millions)")
    label(ws, 15, "Scenario revenue", bold=True, fill=FILL_HDR)
    row_formula(ws, 15, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] in BASE else (f"=({Ps('g_rev_lo')}+{Ps('g_rev_hi')})/2" if YEARS[i] == 2026 else f"={c}11*{c}12"), nf=NF_NUM, fill=FILL_HDR, bold=True)
    for i in range(4): ws[f"{COLS[i]}15"].font = Font(name="Arial", size=10, bold=True, color="FF008000")
    label(ws, 16, "Revenue growth")
    row_formula(ws, 16, lambda i, c, pc: f"={c}15/{pc}15-1", nf=NF_PCT, start=1)
    label(ws, 17, "Revenue | BBG consensus CY26-28 (memo)")
    row_formula(ws, 17, lambda i, c, pc: f"={Pc('rev_ref', c)}", nf=NF_NUM, font=F_LINK, start=3, end=6)
    label(ws, 18, "Scenario ÷ consensus − 1")
    row_formula(ws, 18, lambda i, c, pc: f"={c}15/{c}17-1", nf=NF_PCT, start=3, end=6)
    label(ws, 19, "Memo: 2030 revenue — UBS $84.8bn / Street ~$80bn (UBS 09-22) vs scenario")
    setc(ws, "K19", "=K15/84800-1", F_TXT, nf=NF_PCT, align="right")

    # ---- P&L / cash
    header_row(ws, 21, "Operating result and cash (company adjusted basis; SBC deducted below)")
    r = 22; pl = {}
    label(ws, r, "Adjusted EBITDA margin"); row_formula(ws, r, lambda i, c, pc: (f"={Pc('ebitda_ref', c)}/{c}15" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else (f"={Pc('ebitda_m', c)}" if YEARS[i] == 2026 else f"={Pc('ebitda_m', c)}+$E$6"), nf=NF_PCT, font=F_LINK); pl["ebitdam"] = r; r += 1
    label(ws, r, "Adjusted EBITDA", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}15*{c}{pl['ebitdam']}" if YEARS[i] >= 2024 else None, bold=True); pl["ebitda"] = r; r += 1
    label(ws, r, "EBITDA | BBG consensus (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('ebitda_ref', c)}", font=F_LINK, start=3, end=6); pl["ebitda_c"] = r; r += 1
    label(ws, r, "D&A per average active GW (US$ bn / GW-year) | CY24-25 implied"); row_formula(ws, r, lambda i, c, pc: (f"={c}{r+1}/{c}10" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else f"={Pc('da_gw', c)}", nf=NF_NUM1, font=F_LINK); pl["dagw"] = r; r += 1
    label(ws, r, "Depreciation and amortization"); row_formula(ws, r, lambda i, c, pc: f"={Pc('da_ref', c)}" if YEARS[i] in BASE else f"={c}10*{c}{pl['dagw']}", font=F_LINK); pl["da"] = r
    for i in range(3, NY): ws[f"{COLS[i]}{r}"].font = F_TXT
    r += 1
    label(ws, r, "Adjusted operating income (AOI = EBITDA − D&A)", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebitda']}-{c}{pl['da']}" if YEARS[i] >= 2024 else None, bold=True); pl["aoi"] = r; r += 1
    label(ws, r, "Adjusted operating margin"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['aoi']}/{c}15" if YEARS[i] >= 2024 else None, nf=NF_PCT); pl["aoim"] = r; r += 1
    label(ws, r, "AOI | BBG consensus EBIT (memo) / FY26 guide midpoint"); row_formula(ws, r, lambda i, c, pc: f"=({Ps('g_aoi_lo')}+{Ps('g_aoi_hi')})/2" if YEARS[i] == 2026 else f"={Pc('aoi_ref', c)}", font=F_LINK, start=3, end=6); pl["aoi_c"] = r; r += 1
    label(ws, r, "Stock-based compensation"); row_formula(ws, r, lambda i, c, pc: f"=-{Pc('sbc_ref', c)}" if YEARS[i] in BASE else f"=-{c}15*{Pc('sbc', c)}"); pl["sbc"] = r; r += 1
    label(ws, r, "EBIT after SBC", bold=True); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['aoi']}+{c}{pl['sbc']}" if YEARS[i] >= 2024 else None, bold=True); pl["ebit"] = r; r += 1
    label(ws, r, "EBIT margin after SBC"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebit']}/{c}15" if YEARS[i] >= 2024 else None, nf=NF_PCT); pl["ebitm"] = r; r += 1
    label(ws, r, "Cash tax rate"); row_formula(ws, r, lambda i, c, pc: f"={Pc('tax', c)}" if YEARS[i] >= 2026 else None, nf=NF_PCT, font=F_LINK); pl["tax"] = r; r += 1
    label(ws, r, "NOPAT"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['ebit']}*(1-{c}{pl['tax']})" if YEARS[i] >= 2026 else None); pl["nopat"] = r; r += 1
    label(ws, r, "Build cost per GW added (US$ bn / GW)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('build', c)}" if YEARS[i] >= 2026 else None, nf=NF_NUM1, font=F_LINK); pl["build"] = r; r += 1
    label(ws, r, "Growth capex = build x ((1 − pre-build) x adds t + pre-build x adds t+1)")
    def f_cg(i, c, pc):
        if YEARS[i] < 2026: return None
        nc = COLS[i + 1] if i + 1 < NY else c
        return f"=-{c}{pl['build']}*((1-{Ps('prebuild')})*{c}9+{Ps('prebuild')}*{nc}9)"
    row_formula(ws, r, f_cg); pl["capex_g"] = r; r += 1
    label(ws, r, "Power replaced in the year (MW) = power installed in (t − life), adds and replacements included")
    row_formula(ws, r, lambda i, c, pc: f"=IF(COLUMN({c}9)-COLUMN($D$9)+1-$F$6>=1,INDEX($D${r+1}:$Z${r+1},1,COLUMN({c}9)-COLUMN($D$9)+1-$F$6),0)", nf=NF_NUM); pl["replaced"] = r; r += 1
    label(ws, r, "Power installed in the year (MW) = adds + replacements")
    row_formula(ws, r, lambda i, c, pc: f"={c}9+{c}{pl['replaced']}", nf=NF_NUM); pl["installed"] = r; r += 1
    label(ws, r, "Replacement capex = power replaced x build x replacement %")
    row_formula(ws, r, lambda i, c, pc: f"=-{c}{pl['replaced']}*{c}{pl['build']}*$G$6" if YEARS[i] >= 2026 else None); pl["capex_r"] = r; r += 1
    label(ws, r, "Total capex | CY23-25 reported cash; 2026 guide (midpoint)", bold=True)
    row_formula(ws, r, lambda i, c, pc: f"=-{Pc('capex_ref', c)}" if YEARS[i] in BASE else (f"=-({Ps('g_capex_lo')}+{Ps('g_capex_hi')})/2" if YEARS[i] == 2026 else f"={c}{pl['capex_g']}+{c}{pl['capex_r']}"), bold=True); pl["capex"] = r; r += 1
    label(ws, r, "Capex | BBG consensus (memo)"); row_formula(ws, r, lambda i, c, pc: f"=-{Pc('capex_ref', c)}", font=F_LINK, start=3, end=6); pl["capex_c"] = r; r += 1
    label(ws, r, "Memo: 2026 capex by the formula (calibration check)"); setc(ws, f"G{r}", f"=G{pl['capex_g']}+G{pl['capex_r']}", F_TXT, nf=NF_NUM, align="right"); pl["capex26f"] = r; r += 1
    label(ws, r, "Memo: total capex per GW INSTALLED in the year (adds + replacements; US$ bn / GW) — flow basis, includes pre-build"); row_formula(ws, r, lambda i, c, pc: f"=-{c}{pl['capex']}/{c}{pl['installed']}" if YEARS[i] >= 2024 else None, nf=NF_NUM1); pl["capexgw"] = r; r += 1
    label(ws, r, "Operating NWC (receivables − deferred revenue)"); row_formula(ws, r, lambda i, c, pc: (f"={Pc('ar', c)}-{Pc('defrev', c)}" if YEARS[i] >= 2024 else None) if YEARS[i] in BASE else f"={c}15*{Pc('nwc', c)}"); pl["nwc"] = r; r += 1
    label(ws, r, "Change in NWC | cash effect (customer prepayments)"); row_formula(ws, r, lambda i, c, pc: f"=-({c}{pl['nwc']}-{pc}{pl['nwc']})", start=2); pl["dnwc"] = r; r += 1
    label(ws, r, "Free cash flow to the firm (FCFF)", bold=True)
    row_formula(ws, r, lambda i, c, pc: f"={c}{pl['nopat']}+{c}{pl['da']}+{c}{pl['capex']}+{c}{pl['dnwc']}", start=3, bold=True); pl["fcff"] = r; r += 1
    label(ws, r, "FCFF / revenue"); row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}/{c}15", nf=NF_PCT, start=3); pl["fcffr"] = r; r += 1
    label(ws, r, "Memo: implied incremental ROIC = ΔNOPAT ÷ prior year's (capex − D&A)"); row_formula(ws, r, lambda i, c, pc: f"=IFERROR(({c}{pl['nopat']}-{pc}{pl['nopat']})/(-{pc}{pl['capex']}-{pc}{pl['da']}),NA())" if YEARS[i] >= 2028 else None, nf=NF_PCT); pl["roic_i"] = r
    pl["end"] = r; pl["rev"] = 15

    # ---- discount block
    r0 = pl["end"] + 2
    dsc = {}
    label(ws, r0, "Cash-flow date"); row_formula(ws, r0, lambda i, c, pc: f"=DATE({YEARS[i]},12,31)", nf=NF_DATE_S); dsc["date"] = r0
    vd = "$D$" + str(r0 + 7)
    label(ws, r0 + 1, "Discount period (years)"); row_formula(ws, r0 + 1, lambda i, c, pc: f"=MAX(0,({c}{r0}-{vd})/365)", nf=NF_NUM2); dsc["t"] = r0 + 1
    label(ws, r0 + 2, "Post-valuation fraction of the year"); row_formula(ws, r0 + 2, lambda i, c, pc: f"=MAX(0,MIN(1,({c}{r0}-{vd})/({c}{r0}-DATE({YEARS[i]},1,1)+1)))", nf=NF_PCT); dsc["frac"] = r0 + 2
    label(ws, r0 + 3, "FCFF included in the valuation"); row_formula(ws, r0 + 3, lambda i, c, pc: "=0" if i < 3 else f"={c}{pl['fcff']}*{c}{r0+2}"); dsc["fcffv"] = r0 + 3
    wacc = "$D$" + str(r0 + 8)
    label(ws, r0 + 4, "Present value of FCFF"); row_formula(ws, r0 + 4, lambda i, c, pc: f"={c}{r0+3}/(1+{wacc})^{c}{r0+1}"); dsc["pv"] = r0 + 4
    dsc["end"] = r0 + 4; dsc["vstart"] = r0 + 6

    # ---- valuation block
    v0 = dsc["vstart"]; val = {}
    header_row(ws, v0, "Valuation | FCFF and bridge to equity")
    label(ws, v0 + 1, "Valuation date"); setc(ws, f"D{v0+1}", f"={P}D{R['val_date']}", F_LINK, nf=NF_DATE); val["vdate"] = v0 + 1
    label(ws, v0 + 2, "WACC"); setc(ws, f"D{v0+2}", f"={P}D{R['wacc']}", F_LINK, nf=NF_PCT); val["wacc"] = v0 + 2
    label(ws, v0 + 3, "Terminal growth (g)"); setc(ws, f"D{v0+3}", f"={P}D{R['g']}", F_LINK, nf=NF_PCT); val["g"] = v0 + 3
    label(ws, v0 + 4, "Terminal incremental ROIC"); setc(ws, f"D{v0+4}", f"={P}D{R['roic']}", F_LINK, nf=NF_PCT); val["roic"] = v0 + 4
    label(ws, v0 + 5, "Diluted shares (millions)"); setc(ws, f"D{v0+5}", f"={P}D{R['shares']}", F_LINK, nf=NF_NUM1); val["sh"] = v0 + 5
    label(ws, v0 + 6, "Cash + securities (unrestricted)"); setc(ws, f"D{v0+6}", f"={P}D{R['cash']}", F_LINK, nf=NF_NUM); val["cash"] = v0 + 6
    rr = v0 + 7
    label(ws, rr, "Gross financial debt (principal + finance leases)"); setc(ws, f"D{rr}", f"={P}D{R['debt']}", F_LINK, nf=NF_NUM); val["debt"] = rr; rr += 1
    label(ws, rr, "Net debt"); setc(ws, f"D{rr}", f"=D{val['debt']}-D{val['cash']}", F_TXT, nf=NF_NUM); val["netdebt"] = rr; rr += 2
    Z = COLS[-1]; G0 = COLS[3]
    label(ws, rr, "PV of explicit cash flows"); setc(ws, f"D{rr}", f"=SUM({G0}{dsc['pv']}:{Z}{dsc['pv']})", F_TXT, nf=NF_NUM); val["pvx"] = rr; rr += 1
    label(ws, rr, "Terminal NOPAT"); setc(ws, f"D{rr}", f"={Z}{pl['nopat']}*(1+D{val['g']})", F_TXT, nf=NF_NUM); val["nopat_t"] = rr; rr += 1
    label(ws, rr, "Terminal net reinvestment"); setc(ws, f"D{rr}", f"=D{val['nopat_t']}*D{val['g']}/D{val['roic']}", F_TXT, nf=NF_NUM); val["reinv"] = rr; rr += 1
    label(ws, rr, "Terminal FCFF"); setc(ws, f"D{rr}", f"=IF(AND(D{val['wacc']}>D{val['g']},D{val['roic']}>D{val['g']}),D{val['nopat_t']}-D{val['reinv']},NA())", F_TXT, nf=NF_NUM); val["fcff_t"] = rr; rr += 1
    label(ws, rr, "Undiscounted terminal value"); setc(ws, f"D{rr}", f"=D{val['fcff_t']}/(D{val['wacc']}-D{val['g']})", F_TXT, nf=NF_NUM); val["tv"] = rr; rr += 1
    label(ws, rr, "PV of terminal value"); setc(ws, f"D{rr}", f"=D{val['tv']}/(1+D{val['wacc']})^{Z}{dsc['t']}", F_TXT, nf=NF_NUM); val["pvtv"] = rr; rr += 1
    label(ws, rr, "Enterprise value"); setc(ws, f"D{rr}", f"=SUM(D{val['pvx']},D{val['pvtv']})", F_TXT, nf=NF_NUM); val["ev"] = rr; rr += 1
    label(ws, rr, "Equity value"); setc(ws, f"D{rr}", f"=D{val['ev']}-D{val['netdebt']}", F_TXT, nf=NF_NUM); val["equity"] = rr; rr += 1
    label(ws, rr, "Value per share (US$)", bold=True, fill=FILL_RES); ws[f"C{rr}"].font = F_RES
    setc(ws, f"D{rr}", f"=D{val['equity']}/D{val['sh']}", F_RES, nf='"$"0.00;\\("$"0.00\\)', fill=FILL_RES); val["ps"] = rr; rr += 1
    label(ws, rr, "Terminal value / enterprise value"); setc(ws, f"D{rr}", f"=D{val['pvtv']}/D{val['ev']}", F_TXT, nf=NF_PCT); val["tvshare"] = rr; rr += 1
    label(ws, rr, "Value per share | explicit cash flows only (no terminal)"); setc(ws, f"D{rr}", f"=(D{val['pvx']}-D{val['netdebt']})/D{val['sh']}", F_TXT, nf='"$"0.00;\\("$"0.00\\)'); val["ps_nt"] = rr; rr += 1
    label(ws, rr, "Memo: EV at the reference price (market cap + net debt)"); setc(ws, f"D{rr}", f"={Ps('mktcap')}+D{val['netdebt']}", F_TXT, nf=NF_NUM); val["ev_px"] = rr; rr += 1
    label(ws, rr, "Memo: EV/EBITDA CY27E and CY28E at the reference price"); setc(ws, f"D{rr}", f"=D{val['ev_px']}/H{pl['ebitda']}", F_TXT, nf=NF_X); setc(ws, f"E{rr}", f"=D{val['ev_px']}/I{pl['ebitda']}", F_TXT, nf=NF_X); val["evm"] = rr; rr += 1
    label(ws, rr, "Memo: EV/revenue CY28E at the price (UBS PT $120 = 3.8x CY28E; peers ~4.5x)"); setc(ws, f"D{rr}", f"=D{val['ev_px']}/I15", F_TXT, nf=NF_X); val["evs"] = rr
    # grid WACC x g
    setc(ws, f"F{v0+1}", "Sensitivity | WACC x g (US$ / share)", F_TXTB)
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
    # grid 2: revenue/GW x EBITDA margin (Data Table created by COM in recalc_verify.py)
    g2 = v0 + 10
    setc(ws, f"F{g2}", "Sensitivity | revenue per GW in 2030 (US$ bn/GW, columns) x LT EBITDA margin (rows) — US$ / share (data table, filled by Excel)", F_TXTB)
    setc(ws, f"F{g2+1}", f"=D{val['ps']}", F_TXT, nf=NF_NUM2, fill=FILL_HDR)
    mults = [11, 12, 13, 14, 15, 16]
    for k, m in enumerate(mults):
        setc(ws, f"{get_column_letter(7+k)}{g2+1}", round(m / 13.0, 6), F_TXTB, nf=NF_NUM2, fill=FILL_HDR)
        setc(ws, f"{get_column_letter(7+k)}{g2+8}", m, F_NOTE, nf='0" bn/GW"', align="center")
    adjs = [-0.05, 0, 0.05, 0.10]
    for k, a in enumerate(adjs):
        setc(ws, f"F{g2+2+k}", a, F_TXTB, nf='+0.0%;-0.0%;0.0%', fill=FILL_HDR)
        setc(ws, f"E{g2+2+k}", f"={P}$Z${R['ebitda_m']}+F{g2+2+k}", F_NOTE, nf=NF_PCT)
    note(ws, g2 + 7, "Rows: EBITDA-margin adjustment (pp) over the WHOLE 2027+ path (column E = resulting LT margin). Columns: revenue/GW multiplier over the WHOLE 2027+ path (top row) — the bottom row shows the equivalent 2030 level (LT = 14.0 x mult). Base 2030 = 13.0 sits BELOW management's floor for new contracts (15-16): 1.9 GW legacy at 11 + 6.1 GW new at 15.5 would blend to ~14.4.", col="F")
    val["grid2"] = g2
    g3 = g2 + 10
    setc(ws, f"F{g3}", "Sensitivity | replacement life (years, columns) x replacement cost (% of build, rows) — US$ / share (data table)", F_TXTB)
    setc(ws, f"F{g3+1}", f"=D{val['ps']}", F_TXT, nf=NF_NUM2, fill=FILL_HDR)
    for k, lf in enumerate([5, 6, 7, 8, 10]):
        setc(ws, f"{get_column_letter(7+k)}{g3+1}", lf, F_TXTB, nf='0" yrs"', fill=FILL_HDR)
    for k, rp in enumerate([1.0, 0.8, 0.6, 0.4]):
        setc(ws, f"F{g3+2+k}", rp, F_TXTB, nf=NF_PCT, fill=FILL_HDR)
    note(ws, g3 + 6, "Replacement is what the Street rarely charges explicitly: at 6 years / 80% a mature fleet consumes ~$5.3bn per GW-year (≈ D&A). Longer life = re-contracting old GPUs (A100/H100 still rented in year 9) without replacing them — but the 7-10-year columns keep full pricing on old GPUs (DB 2025-06-16: 50-75% of ASP in years 5-6), so they are the UPPER BOUND, not a case.", col="F")
    val["grid3"] = g3
    # unit economics per GW at steady state (column P = 2035)
    u0 = g3 + 8
    header_row(ws, u0, "Steady-state unit economics per GW (column CY35E) — the arithmetic behind the DCF", cols=COLS[:3])
    ue = {}
    u = u0 + 1
    label(ws, u, "Revenue per billable GW (US$ bn / GW-year)"); setc(ws, f"D{u}", "=P12", F_TXT, nf=NF_NUM2); ue["rev"] = u; u += 1
    label(ws, u, "EBITDA per GW (US$ bn)"); setc(ws, f"D{u}", f"=D{ue['rev']}*P{pl['ebitdam']}", F_TXT, nf=NF_NUM2); ue["ebitda"] = u; u += 1
    label(ws, u, "D&A per GW (US$ bn)"); setc(ws, f"D{u}", f"=P{pl['dagw']}", F_TXT, nf=NF_NUM2); ue["da"] = u; u += 1
    label(ws, u, "SBC per GW (US$ bn)"); setc(ws, f"D{u}", f"=D{ue['rev']}*{P}P{R['sbc']}", F_TXT, nf=NF_NUM2); ue["sbc"] = u; u += 1
    label(ws, u, "Tax per GW = (EBITDA − D&A − SBC) x tax rate (US$ bn)"); setc(ws, f"D{u}", f"=(D{ue['ebitda']}-D{ue['da']}-D{ue['sbc']})*P{pl['tax']}", F_TXT, nf=NF_NUM2); ue["tax"] = u; u += 1
    label(ws, u, "Operating cash per GW before capex = EBITDA − SBC − tax (US$ bn)"); setc(ws, f"D{u}", f"=D{ue['ebitda']}-D{ue['sbc']}-D{ue['tax']}", F_TXTB, nf=NF_NUM2); ue["cfo"] = u; u += 1
    label(ws, u, "Build cost per GW (US$ bn)"); setc(ws, f"D{u}", f"=P{pl['build']}", F_TXT, nf=NF_NUM2); ue["build"] = u; u += 1
    label(ws, u, "Replacement per GW-year, mature fleet = build x replacement % ÷ life (US$ bn) — memo, what the DCF charges at steady state"); setc(ws, f"D{u}", f"=D{ue['build']}*$G$6/$F$6", F_TXT, nf=NF_NUM2); ue["repl_lvl"] = u; u += 1
    label(ws, u, "Replacement of 1 NEW GW, annual equivalent (sinking fund: first swap in year 'life') = build x % x WACC ÷ ((1+WACC)^life − 1)"); setc(ws, f"D{u}", f"=D{ue['build']}*$G$6*D{val['wacc']}/((1+D{val['wacc']})^$F$6-1)", F_TXT, nf=NF_NUM2); ue["repl"] = u; u += 1
    label(ws, u, "FCF per GW-year of 1 new GW, no growth = operating cash − equivalent replacement (US$ bn)", bold=True); setc(ws, f"D{u}", f"=D{ue['cfo']}-D{ue['repl']}", F_TXTB, nf=NF_NUM2); ue["fcf"] = u; u += 1
    label(ws, u, "Cash yield on build cost (FCF ÷ build)"); setc(ws, f"D{u}", f"=D{ue['fcf']}/D{ue['build']}", F_TXT, nf=NF_PCT); ue["yield"] = u; u += 1
    label(ws, u, "Gross payback of the build = build ÷ operating cash (years)"); setc(ws, f"D{u}", f"=D{ue['build']}/D{ue['cfo']}", F_TXT, nf='0.0" yrs"'); ue["pb"] = u; u += 1
    label(ws, u, "Value of 1 GW in perpetuity at WACC = FCF ÷ WACC (US$ bn)"); setc(ws, f"D{u}", f"=D{ue['fcf']}/D{val['wacc']}", F_TXT, nf=NF_NUM2); ue["pv"] = u; u += 1
    label(ws, u, "NPV of 1 new GW = value − build (US$ bn) — negative = each GW destroys value at WACC", bold=True); setc(ws, f"D{u}", f"=D{ue['pv']}-D{ue['build']}", F_TXTB, nf=NF_NUM2); ue["npv"] = u; u += 1
    label(ws, u, "Break-even revenue/GW (NPV = 0) at the same margin, life and replacement (US$ bn / GW-year)")
    setc(ws, f"D{u}", f"=(D{ue['build']}*D{val['wacc']}+D{ue['repl']}-D{ue['da']}*P{pl['tax']})/((P{pl['ebitdam']}-{P}P{R['sbc']})*(1-P{pl['tax']}))", F_TXT, nf=NF_NUM2); ue["be"] = u; u += 1
    note(ws, u, "Break-even: (EBITDA − SBC) x (1 − t) + D&A x t − equivalent replacement = build x WACC. Compare with the marks: installed book ~11, management's floor for new contracts 15-16 (= the break-even), short-dated ~40. A MATURE fleet replaces ~fleet ÷ life per year (memo row) — that is what the DCF charges from 2032.")
    val["ue"] = ue
    val["end"] = max(rr, u + 1)

    # ---- memo: debt roll + EPS (outside DCF)
    m0 = val["end"] + 2
    header_row(ws, m0, "Memo outside the DCF | implied net debt, interest, net income and EPS (no equity raised after 2026)")
    mm = {}
    r = m0 + 1
    label(ws, r, "Net debt at year-end (US$ m)"); mm["nd"] = r
    row_formula(ws, r, lambda i, c, pc: f"={Ps('nd_2025')}" if YEARS[i] == 2025 else (f"={pc}{r}-{c}{pl['fcff']}+{c}{r+1}-{Ps('eq_2026')}" if YEARS[i] == 2026 else f"={pc}{r}-{c}{pl['fcff']}+{c}{r+1}"), start=2); r += 1
    label(ws, r, "Net interest = (prior net debt − 0.5 x FCFF of the year) x cost of debt"); mm["int"] = r
    row_formula(ws, r, lambda i, c, pc: f"=({pc}{mm['nd']}-0.5*{c}{pl['fcff']})*{Pc('kd', c)}", start=3); r += 1
    label(ws, r, "Interest | reported FY23-25 (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('int_ref', c)}", font=F_LINK, end=3); r += 1
    label(ws, r, "Net debt / EBITDA"); mm["lev"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{mm['nd']}/{c}{pl['ebitda']}", nf=NF_X, start=2); r += 1
    label(ws, r, "Adjusted net income (company basis, EX-SBC) = (AOI − interest) x (1 − tax if positive)"); mm["ni"] = r
    row_formula(ws, r, lambda i, c, pc: f"=IF({c}{pl['aoi']}-{c}{mm['int']}>0,({c}{pl['aoi']}-{c}{mm['int']})*(1-{c}{pl['tax']}),{c}{pl['aoi']}-{c}{mm['int']})", start=3); r += 1
    label(ws, r, "Memo: net income after SBC"); mm["ni_sbc"] = r
    row_formula(ws, r, lambda i, c, pc: f"=IF({c}{pl['ebit']}-{c}{mm['int']}>0,({c}{pl['ebit']}-{c}{mm['int']})*(1-{c}{pl['tax']}),{c}{pl['ebit']}-{c}{mm['int']})", start=3); r += 1
    label(ws, r, "Net income | GAAP reported / BBG consensus (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('ni_ref', c)}", font=F_LINK, end=6); r += 1
    label(ws, r, "Diluted shares (m)"); mm["sh"] = r; row_formula(ws, r, lambda i, c, pc: f"={Pc('sh', c)}", nf=NF_NUM1, font=F_LINK, start=3); r += 1
    label(ws, r, "Adjusted EPS (US$, company / consensus basis: ex-SBC)", bold=True); mm["eps"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{mm['ni']}/{c}{mm['sh']}", nf=NF_NUM2, start=3, bold=True); r += 1
    label(ws, r, "EPS | BBG consensus (memo)"); row_formula(ws, r, lambda i, c, pc: f"={Pc('eps_ref', c)}", nf=NF_NUM2, font=F_LINK, start=3, end=6); r += 1
    label(ws, r, "Free cash flow to equity = FCFF − interest"); mm["fcfe"] = r; row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}-{c}{mm['int']}", start=3); r += 1
    label(ws, r, "Cumulative FCFF since 2026 (financing need until it turns positive)"); mm["cum"] = r
    row_formula(ws, r, lambda i, c, pc: f"={c}{pl['fcff']}" if YEARS[i] == 2026 else f"={pc}{r}+{c}{pl['fcff']}", start=3); r += 1
    mm["end"] = r - 1

    # ---- reconciliations
    rc = mm["end"] + 2
    header_row(ws, rc, "Reconciliations and guardrails (0 / green expected)")
    rr = rc + 1
    label(ws, rr, "Revenue − billable power x revenue/GW (2027+)"); row_formula(ws, rr, lambda i, c, pc: f"={c}15-{c}11*{c}12", nf=NF_CHK, start=4); rr += 1
    label(ws, rr, "AOI − (EBITDA − D&A)"); row_formula(ws, rr, lambda i, c, pc: f"={c}{pl['aoi']}-({c}{pl['ebitda']}-{c}{pl['da']})", nf=NF_CHK, start=1); rr += 1
    label(ws, rr, "FY26 guide: model AOI inside $960-1,150m (0 = ok; otherwise the deviation)"); setc(ws, f"G{rr}", f"=IF(G{pl['aoi']}<{Ps('g_aoi_lo')},G{pl['aoi']}-{Ps('g_aoi_lo')},IF(G{pl['aoi']}>{Ps('g_aoi_hi')},G{pl['aoi']}-{Ps('g_aoi_hi')},0))", F_TXT, nf=NF_CHK, align="right"); rr += 1
    label(ws, rr, "2026 capex calibration: formula ÷ guide (midpoint) − 1 (|x| < 10%)"); setc(ws, f"G{rr}", f"=G{pl['capex26f']}/G{pl['capex']}-1", F_TXT, nf=NF_PCT, align="right"); rr += 1
    label(ws, rr, "Revenue per billable GW between 10 and 20 US$ bn/GW (0 = inside; otherwise the excess)"); row_formula(ws, rr, lambda i, c, pc: f"=IF({c}12<10,{c}12-10,IF({c}12>20,{c}12-20,0))", nf=NF_CHK, start=1); rr += 1
    label(ws, rr, "Total capex per GW installed between 25 and 60 US$ bn/GW (flow; 0 = inside)"); row_formula(ws, rr, lambda i, c, pc: f"=IF({c}{pl['capexgw']}<25,{c}{pl['capexgw']}-25,IF({c}{pl['capexgw']}>60,{c}{pl['capexgw']}-60,0))", nf=NF_CHK, start=3); rr += 1
    label(ws, rr, "RPO coverage: model revenue 2H26 + 2027 + 1H28 ÷ 41% of the Jun-26 RPO (US$ 42.5bn) — >1 = model above the contracted book"); setc(ws, f"G{rr}", f"=(G15-{Ps('h1_rev')}+H15+I15/2)/(0.41*{P}G{R['rpo_ref']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "RPO coverage: revenue months 25-48 (2H28 + 2029 + 1H30) ÷ 39% of RPO (US$ 40.4bn)"); setc(ws, f"G{rr}", f"=(I15/2+J15+K15/2)/(0.39*{P}G{R['rpo_ref']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "Maximum net debt / EBITDA 2026-30 (UBS: 5.7x 2026E, 4.2x 2027E)"); setc(ws, f"G{rr}", f"=MAX(G{mm['lev']}:K{mm['lev']})", F_TXT, nf=NF_X, align="right"); rr += 1
    label(ws, rr, "Adds 2026-30 − (8,000 − YE25): 0 = 8.0 GW fleet in 2030 (management target ≥8 GW)"); setc(ws, f"G{rr}", "=SUM(G9:K9)-(8000-F8)", F_TXT, nf=NF_CHK, align="right"); rr += 1
    label(ws, rr, "Equity: EV − net debt"); setc(ws, f"D{rr}", f"=D{val['equity']}-(D{val['ev']}-D{val['netdebt']})", F_TXT, nf=NF_CHK); rr += 1
    label(ws, rr, "Sensitivity: centre = base DCF"); setc(ws, f"D{rr}", f"=I{val['grid_center_row']}-D{val['ps']}", F_TXT, nf=NF_CHK); rr += 1
    label(ws, rr, "2030 adjusted operating margin vs management's 25-30% long-term target (4Q25 call) — shortfall to the floor"); setc(ws, f"K{rr}", f"=MIN(0,K{pl['aoim']}-0.25)", F_TXT, nf=NF_PCT, align="right"); rr += 1
    rec_end = rr

    # ---- wiki block
    rw = rec_end + 1
    header_row(ws, rw, "Summary for the wiki | house estimates (CY) — Capstone estimates (house model)")
    label(ws, rw + 1, "Revenue (US$ m)"); row_formula(ws, rw + 1, lambda i, c, pc: f"={c}15", start=1, end=8)
    label(ws, rw + 2, "Active power at year-end (MW)"); row_formula(ws, rw + 2, lambda i, c, pc: f"={c}8", start=1, end=8)
    label(ws, rw + 3, "Revenue per billable GW (US$ bn)"); row_formula(ws, rw + 3, lambda i, c, pc: f"={c}12", nf=NF_NUM1, start=1, end=8)
    label(ws, rw + 4, "Adjusted EBITDA margin"); row_formula(ws, rw + 4, lambda i, c, pc: f"={c}{pl['ebitdam']}", nf=NF_PCT, start=1, end=8)
    label(ws, rw + 5, "Adjusted EBITDA (US$ m)"); row_formula(ws, rw + 5, lambda i, c, pc: f"={c}{pl['ebitda']}", start=1, end=8)
    label(ws, rw + 6, "Adjusted operating margin (AOI)"); row_formula(ws, rw + 6, lambda i, c, pc: f"={c}{pl['aoim']}", nf=NF_PCT, start=1, end=8)
    label(ws, rw + 7, "Capex (US$ m)"); row_formula(ws, rw + 7, lambda i, c, pc: f"=-{c}{pl['capex']}", start=1, end=8)
    label(ws, rw + 8, "FCFF (US$ m)"); row_formula(ws, rw + 8, lambda i, c, pc: f"={c}{pl['fcff']}", start=3, end=8)
    label(ws, rw + 9, "Adjusted net income (US$ m) | CY24-25 GAAP reported"); row_formula(ws, rw + 9, lambda i, c, pc: f"={Pc('ni_ref', c)}" if YEARS[i] < 2026 else f"={c}{mm['ni']}", start=1, end=8)
    label(ws, rw + 10, "Adjusted EPS (US$) | CY24-25 GAAP reported", bold=True); row_formula(ws, rw + 10, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] < 2026 else f"={c}{mm['eps']}", nf=NF_NUM2, start=1, end=8, bold=True)
    label(ws, rw + 11, "BBG consensus — revenue (memo)"); row_formula(ws, rw + 11, lambda i, c, pc: f"={Pc('rev_ref', c)}" if YEARS[i] >= 2026 else None, start=3, end=6, font=F_LINK)
    label(ws, rw + 12, "BBG consensus — EPS (memo)"); row_formula(ws, rw + 12, lambda i, c, pc: f"={Pc('eps_ref', c)}" if YEARS[i] >= 2026 else None, nf=NF_NUM2, start=3, end=6, font=F_LINK)
    label(ws, rw + 13, "Revenue: house ÷ consensus − 1"); row_formula(ws, rw + 13, lambda i, c, pc: f"={c}{rw+1}/{c}{rw+11}-1" if YEARS[i] >= 2026 else None, nf=NF_PCT, start=3, end=6)
    label(ws, rw + 14, "EV/EBITDA at the reference price (informational)"); row_formula(ws, rw + 14, lambda i, c, pc: f"=$D${val['ev_px']}/{c}{pl['ebitda']}" if YEARS[i] >= 2025 else None, nf=NF_X, start=2, end=8)
    note(ws, rw + 16, "The 'Capstone estimates (house model)' table on the wiki page (_wiki/CRWV.md) is transcribed from this block (CY24A-CY30E). Thesis-drift rule: when a number changes, move the old one to the page's Changelog.")
    note(ws, rw + 17, "Reading the model: at the current price the DCF is a bet on revenue per GW and on replacement — a GW costs ~$40bn and generates ~$8-9bn of EBITDA a year; with replacement every 6 years the unlevered return sits near the WACC. The revenue/GW x margin grid is the answer.")

    build_history(wh, R)
    build_debt(wd)

    wb.save(path)
    lay = dict(R=R, pl=pl, dsc=dsc, val=val, mm=mm, rec=rc, wiki=rw)
    json.dump(lay, open(os.path.join(OUT, "layout.json"), "w"), indent=1, default=str)
    return lay


# ================================================================================================= History sheet
HQ = ["FY23", "FY24", "FY25", "1Q25", "2Q25", "3Q25", "4Q25", "1Q26", "2Q26"]
HCOLS = [get_column_letter(4 + i) for i in range(len(HQ))]
HIST = [
    ("Revenue", [229, 1915, 5131, 981.6, 1212.8, 1364.7, 1571.9, 2078, 2575], NF_NUM1, "10-K FY25; 10-Qs (1Q25-3Q25 in US$ thousands, converted); 4Q25 = FY − 9M."),
    ("Cost of revenue", [69, 493, 1453, 262.4, 312.7, 368.8, 509.1, 716, 879], NF_NUM1, "Same."),
    ("Technology and infrastructure", [131, 961, 2929, 561.4, 669.9, 747.5, 950.2, 1273, 1507], NF_NUM1, "Same (includes DC rent, power, D&A)."),
    ("Sales and marketing", [13, 18, 144, 10.5, 36.8, 44.6, 52.0, 69, 60], NF_NUM1, "Same."),
    ("General and administrative", [30, 119, 651, 174.8, 174.2, 151.9, 150.2, 164, 178], NF_NUM1, "Same."),
    ("GAAP operating income", [-14, 324, -46, -27.5, 19.2, 51.9, -89.6, -144, -49], NF_NUM1, "Same."),
    ("Net interest expense", [-28, -361, -1229, -263.8, -267.2, -311.0, -387.0, -536, -640], NF_NUM1, "Same; 3Q25 call ($311m)."),
    ("GAAP net income", [-594, -863, -1167, -314.6, -290.5, -110.1, -451.8, -740, -626], NF_NUM1, "Same."),
    ("Depreciation and amortization", [103, 863, 2454, 443.5, 559.5, 630.5, 820.5, 1147, 1393], NF_NUM1, "Cash-flow YTD figures differenced by quarter."),
    ("Stock-based compensation", [15, 31, 630, 184, 145, 144.4, 156.6, 153, 165], NF_NUM1, "Cash-flow YTD differenced (9M25 473.4): 3Q 144.4 / 4Q 156.6 (the statement of equity shows 156.9 in 3Q — different basis)."),
    ("Cash capex (purchase of PP&E)", [2943, 8702, 10309, 1407, 2453, 2389, 4060, 7695, 6422], NF_NUM1, "Cash-flow YTD differenced."),
    ("Capex, company basis (calls)", [None, None, None, None, None, None, None, 6800, 9400], NF_NUM1, "Calls 1Q26 (05-07) and 2Q26 (08-11). FY26 guide $35-39bn. Includes OEM financing; differs from cash."),
    ("Adjusted EBITDA (company)", [None, 1226, 3098, 609, 753, 838, 898, 1164, 1510], NF_NUM1, "Calls; FY24 = 64% (DB 2025-06-16) PARTIAL; 1Q26 = '$1.2bn, ~56%' x 2,078 = 1,164 PARTIAL; 1Q25 = 1,164/1.91 ('+91% y/y') PARTIAL."),
    ("Adjusted EBITDA margin", [None, "=E20/E8", "=F20/F8", "=G20/G8", "=H20/H8", "=I20/I8", "=J20/J8", "=K20/K8", "=L20/L8"], NF_PCT, "Calculated."),
    ("AOI (adjusted operating income, company)", [None, None, None, None, 200, 217, None, 21, 128], NF_NUM1, "Calls: 2Q25 $200m (cited on the 2Q26 call, 08-11), 3Q25 $217m, 1Q26 $21m, 2Q26 $128m. FY25 guide $690-720m (3Q25 call)."),
    ("Active power at period-end (MW)", [70, 360, 850, 420, 470, 590, 850, 1000, 1500], NF_NUM, "10-K FY25 (70 / 360 / >850); calls (3Q25 590 = +120 q/q → 2Q25 470; 1Q25 ~420 ESTIMATE; 1Q26 '>1 GW'; 2Q26 1.5 GW)."),
    ("Contracted power at period-end (MW)", [None, None, 3100, None, None, 2900, 3100, 3500, 3700], NF_NUM, "Calls; 4.2 GW as of 11-Aug-26."),
    ("Revenue backlog (company, US$ bn)", [None, 15.1, 66.8, None, 30.1, 55.6, 66.8, 99.4, 104.0], NF_NUM1, "Calls (2Q25 'doubled YTD' → Dec-24 ~15.1 PARTIAL). RPO 10-K/10-Q: 60.7 (Dec-25) / 103.7 (Jun-26)."),
    ("Total deferred revenue (US$ m)", [None, 4064, 8185, None, None, None, 8185, None, 9692], NF_NUM, "Balance sheets."),
    ("Unrestricted cash (US$ m)", [217, 1361, 3127, None, None, None, 3127, None, 5524], NF_NUM, "Balance sheets."),
    ("Gross debt, principal (US$ m)", [None, 7926, 21615, None, None, None, 21615, None, 35551], NF_NUM, "Debt notes (Dec-24 carrying value)."),
    ("Weighted diluted shares (m)", [192, 218, 436, None, 487, None, None, None, 551], NF_NUM, "10-K / 10-Q (post 20:1 split)."),
]


def build_history(wh, R):
    wh.sheet_view.showGridLines = False
    wh.column_dimensions["A"].width = 2.25; wh.column_dimensions["B"].width = 2.25; wh.column_dimensions["C"].width = 52
    for c in HCOLS: wh.column_dimensions[c].width = 11.5
    wh.column_dimensions["N"].width = 80
    setc(wh, "C2", "CRWV | Reported history (annual and quarterly)", F_TITLE)
    setc(wh, "C3", "US$ millions unless stated. Source: 10-K FY25, 10-Qs 1Q25-2Q26 (CRWV/), earnings calls (CRWV/transcripts). Blue = reported; derived/PARTIAL noted in the source column.", F_TXT)
    for i, q in enumerate(HQ):
        setc(wh, f"{HCOLS[i]}5", q, F_TXTB, fill=FILL_HDR, align="center")
    setc(wh, "N5", "Source", F_TXTB, fill=FILL_HDR)
    header_row(wh, 7, "Income statement and cash flow", cols=HCOLS)
    r = 8
    for text, vals, nf, src in HIST:
        if text.startswith("Active power"):
            header_row(wh, r, "Operating and balance sheet", cols=HCOLS); r += 1
        label(wh, r, text)
        for i, v in enumerate(vals):
            if v is None: continue
            if isinstance(v, str):
                setc(wh, f"{HCOLS[i]}{r}", v, F_TXT, nf=nf, align="right")
            else:
                setc(wh, f"{HCOLS[i]}{r}", v, F_INPUT, nf=nf, align="right")
        setc(wh, f"N{r}", src, F_NOTE)
        r += 1
    r += 1
    header_row(wh, r, "Calibration | annualised quarterly revenue ÷ average active power of the PRIOR quarter (US$ bn / GW-year)", cols=HCOLS); r += 1
    label(wh, r, "Average active power of the prior quarter (MW)")
    act_row = 8 + [t for t, *_ in HIST].index("Active power at period-end (MW)") + 1
    prev = {"2Q25": f"=(E{act_row}+G{act_row})/2", "3Q25": f"=(G{act_row}+H{act_row})/2", "4Q25": f"=(H{act_row}+I{act_row})/2", "1Q26": f"=(I{act_row}+J{act_row})/2", "2Q26": f"=(J{act_row}+K{act_row})/2"}
    for q, f in prev.items():
        setc(wh, f"{HCOLS[HQ.index(q)]}{r}", f, F_TXT, nf=NF_NUM, align="right")
    setc(wh, f"N{r}", "Prior quarter = average of the end of the quarter before last and the end of the prior quarter (2Q25 uses Dec-24 360 and 1Q25 ~420 ESTIMATE). 1Q25 omitted (3Q24 not reported). Basis UBS 09-22 ('about a quarter for active power to generate revs'); 2Q26 = 2,575 x 4 / 925 = 11.1 = UBS.", F_NOTE)
    r += 1
    label(wh, r, "Revenue per billable GW (US$ bn / GW-year)", bold=True)
    for q in prev:
        c = HCOLS[HQ.index(q)]
        setc(wh, f"{c}{r}", f"={c}8*4/{c}{r-1}", F_TXTB, nf=NF_NUM1, align="right")
    setc(wh, f"N{r}", "Falls from ~12.4 (2Q25) to ~11.1 (2Q26): the fleet scaled faster than the average price (legacy MSFT/OpenAI book). UBS: ~11 → ~15 at the 2027 exit. Anchor of the model (cover row 12).", F_NOTE)
    r += 1
    label(wh, r, "Annualised D&A ÷ average active power of the quarter (US$ bn / GW-year)")
    for q in ("2Q25", "3Q25", "4Q25", "1Q26", "2Q26"):
        c = HCOLS[HQ.index(q)]; pcq = HCOLS[HQ.index(q) - 1]
        setc(wh, f"{c}{r}", f"={c}16*4/(({pcq}{act_row}+{c}{act_row})/2)", F_TXT, nf=NF_NUM1, align="right")
    setc(wh, f"N{r}", "Anchor of D&A per GW (cover): ~4.5-5.0.", F_NOTE)
    r += 1
    label(wh, r, "Annualised interest ÷ period-end gross debt (memo)")
    for q in ("4Q25", "2Q26"):
        c = HCOLS[HQ.index(q)]
        setc(wh, f"{c}{r}", f"=-{c}14*4/{c}{act_row+5}", F_TXT, nf=NF_PCT, align="right")
    setc(wh, f"N{r}", "4Q25 ~7.2% and 2Q26 ~7.2% on END-of-period principal (debt grew during the period; capitalised interest excluded) — contractual effective rates 9-11%.", F_NOTE)


# ================================================================================================= Debt sheet
DEBT = [
    ("Recourse", "DDTL 1.0 Facility", "Mar-2028", 0.15, 1300, 1553),
    ("Recourse", "DDTL 2.0 Facility", "Aug-2030", 0.11, 3190, 5037),
    ("Recourse", "DDTL 2.1 Facility", "Mar-2031", 0.09, 3000, 2741),
    ("Recourse", "DDTL 3.0 Facility", "Aug-2030", 0.09, 2215, 340),
    ("Recourse", "DDTL 5.0 Facility (SOFR + 4.50%, May-26)", "Nov-2031", 0.09, 1101, 0),
    ("Recourse", "2030 Senior Notes (9.25%)", "Jun-2030", 0.10, 2000, 2000),
    ("Recourse", "2031 9.00% Senior Notes", "Feb-2031", 0.10, 1750, 1750),
    ("Recourse", "2031 9.75% Senior Notes (Apr-26)", "Oct-2031", 0.10, 2750, 0),
    ("Recourse", "2032 9.625% Senior Notes (Jun-26)", "Jul-2032", 0.10, 1250, 0),
    ("Recourse", "2032 EUR Senior Notes (8.50%, EUR 2.0bn, swapped to US$)", "Jul-2032", 0.09, 2279, 0),
    ("Recourse", "2031 Convertible Senior Notes (1.75%)", "Dec-2031", 0.02, 2588, 2588),
    ("Recourse", "2032 Convertible Senior Notes (1.75%; conv. $119.60; cap call $230)", "Oct-2032", 0.02, 4000, 0),
    ("Recourse", "Convertible Promissory Notes", "Apr-2026", 0.07, 0, 168),
    ("Recourse", "Revolving Credit Facility", "Nov-2029", 0.07, 0, 1000),
    ("Recourse", "OEM and Software License Financing Arrangements", "Dec-26 to Jul-30", 0.11, 4220, 3518),
    ("Recourse", "Magnetar Loan", "Jan-2029", 0.12, 189, 273),
    ("Non-recourse", "DDTL 4.0 Facility (SOFR + 2.25% / UST + 2.00%; Meta take-or-pay)", "Mar-2032", 0.07, 2837, 0),
    ("Non-recourse", "OEM and Software License Financing Arrangements", "Aug-26 to Aug-28", 0.09, 882, 647),
]
PRINCIPAL = [("Remainder of 2026", 4413), ("2027", 6184), ("2028", 4416), ("2029", 2421), ("2030", 3221), ("Thereafter", 14896)]


def build_debt(wd):
    wd.sheet_view.showGridLines = False
    wd.column_dimensions["A"].width = 2.25; wd.column_dimensions["B"].width = 2.25; wd.column_dimensions["C"].width = 14
    wd.column_dimensions["D"].width = 66; wd.column_dimensions["E"].width = 16; wd.column_dimensions["F"].width = 14; wd.column_dimensions["G"].width = 14; wd.column_dimensions["H"].width = 14
    setc(wd, "C2", "CRWV | Debt (10-Q 2Q26, note 10 — principal, US$ millions)", F_TITLE)
    setc(wd, "C3", "Source: CRWV/CRWV_10-Q_2026-08-12 note 10 (total debt obligations; future principal payments). Rates = 'effective interest rates' from the table.", F_TXT)
    for j, h in enumerate(["Type", "Instrument", "Maturity", "Effective rate", "30-Jun-2026", "31-Dec-2025"]):
        setc(wd, f"{get_column_letter(3+j)}5", h, F_TXTB, fill=FILL_HDR, align="center")
    r = 6
    for typ, name, mat, rate, v26, v25 in DEBT:
        setc(wd, f"C{r}", typ, F_TXT); setc(wd, f"D{r}", name, F_TXT); setc(wd, f"E{r}", mat, F_TXT, align="center")
        setc(wd, f"F{r}", rate, F_INPUT, nf="0%", align="right"); setc(wd, f"G{r}", v26, F_INPUT, nf=NF_NUM, align="right"); setc(wd, f"H{r}", v25, F_INPUT, nf=NF_NUM, align="right")
        r += 1
    setc(wd, f"D{r}", "Total principal (recourse + non-recourse)", F_TXTB); setc(wd, f"G{r}", f"=SUM(G6:G{r-1})", F_TXTB, nf=NF_NUM, align="right"); setc(wd, f"H{r}", f"=SUM(H6:H{r-1})", F_TXTB, nf=NF_NUM, align="right"); tot = r; r += 1
    setc(wd, f"D{r}", "Weighted-average effective rate (Jun-26)", F_TXT); setc(wd, f"G{r}", f"=SUMPRODUCT(F6:F{tot-1},G6:G{tot-1})/G{tot}", F_TXT, nf=NF_PCT, align="right"); r += 1
    setc(wd, f"D{r}", "Check: note total = 35,551 (Jun-26) / 21,615 (Dec-25)", F_NOTE); setc(wd, f"G{r}", f"=G{tot}-35551", F_TXT, nf=NF_CHK, align="right"); setc(wd, f"H{r}", f"=H{tot}-21615", F_TXT, nf=NF_CHK, align="right"); r += 1
    setc(wd, f"D{r}", "Less: unamortized discount and issuance costs (Jun-26: 427 + 56)", F_NOTE); setc(wd, f"G{r}", -483, F_INPUT, nf=NF_NUM, align="right"); r += 1
    setc(wd, f"D{r}", "Carrying value (recourse 31,405 + non-recourse 3,663 = 35,068)", F_NOTE); setc(wd, f"G{r}", f"=G{tot}+G{r-1}", F_TXT, nf=NF_NUM, align="right"); r += 2
    setc(wd, f"D{r}", "Principal amortization (Jun-26)", F_TXTB, fill=FILL_HDR); setc(wd, f"G{r}", "US$ m", F_TXTB, fill=FILL_HDR, align="center"); r += 1
    p0 = r
    for lab, v in PRINCIPAL:
        setc(wd, f"D{r}", lab, F_TXT); setc(wd, f"G{r}", v, F_INPUT, nf=NF_NUM, align="right"); r += 1
    setc(wd, f"D{r}", "Total", F_TXTB); setc(wd, f"G{r}", f"=SUM(G{p0}:G{r-1})", F_TXTB, nf=NF_NUM, align="right"); r += 2
    notes = [
        "2Q26 interest: contractual 592 + discount amortization 45 − capitalised 79 = 558 (note 10); 'interest expense, net' on the P&L = 640. 3Q26 guide: $860-940m. 1H26 cash paid 806.",
        "Operating leases (Jun-26): PV 16,319 (10% rate, 12 years); future payments 29,135; not yet commenced 35,500 (a single site = 14,700, 393 MW to be delivered). Rent sits in EBITDA — do not add to debt.",
        "DDTL spreads (Redburn 09-21, Fig 70): S+962 (Jul-23), +425 (Sep-24), +400 (OpenAI, Jul-25), +225 (Meta, Mar-26), +450 (non-IG, May-26), +550 (Aug-26, $2.6bn DDTL 5.5, Sep-31). Term loan S+550 yields 9.15% (MS Credit 08-20).",
        "Capital raised: >$32bn of debt + equity through 2Q26 (call 08-11); WACD −300bp in 12 months (~$1.1bn/year of interest). S&P B+ positive (Apr-26). ATM registered, 'not at these prices' (Robbins 09-21).",
        "2031 convert: 9.2764 shares per $1,000 (conv. $107.80; capped call strike 107.80 / cap 215.60 — 10-K FY25). 2032 convert: 8.3612 shares per $1,000 (conv. $119.60); capped calls cost 492m, strike 119.60 / cap 230. Management: effective strike ~$200. Both treated as debt in the model (out of the money at $77.81).",
        "Subsequent events (10-Q 2Q26 note 16): Aug-26 $2.6bn DDTL 5.5 (JPMorgan agent; SOFR+550, matures Sep-31) and a $1.2bn draw on the Revolving Credit Facility — NOT in the model's 30-Jun-26 net debt (the draw funds 2H26 capex already discounted in the FCFF).",
    ]
    for t in notes:
        setc(wd, f"D{r}", t, F_NOTE); r += 1


if __name__ == "__main__":
    path = os.path.join(OUT, "Template DCF CRWV.xlsx")
    lay = build(path)
    print("built", path)
