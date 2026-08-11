#!/usr/bin/env python3
"""Build the final reviewed growth/AI/EBIT workbook from the normalized v2 model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill

import build_selected_index_growth_workbook as base


YEARS = base.YEARS
NAVY = base.NAVY
LIGHT_BLUE = base.LIGHT_BLUE


def write_readme(wb, data, verdict):
    ws = wb.active
    ws.title = "README"
    base.title(ws, "Selected-Index Revenue, AI Revenue & EBIT Model", "Fixed August 2026 constituent cohort; FY2024-FY2030; reviewed neutral base")
    rows = [
        ("Answer", "Historical revenue growth, forward selected-index revenue, AI revenue at 2%-3%, and EBIT margin through 2030."),
        ("Universe", "Current Bloomberg members of Russell 2000, S&P 500, KOSPI Composite, TAIEX, STOXX Europe 600 and DAX 40; company-ID deduplicated union."),
        ("Cohort convention", "The August 10, 2026 company cohort is held fixed in every year. Historical results therefore contain survivorship bias but avoid membership-change noise."),
        ("2024-2025", "Bloomberg annual actual SALES_REV_TURN and EBIT, converted with EQY_FUND_CRNCY=USD. Tagged HARD."),
        ("2026-2028", "Bloomberg annual actual where already reported; otherwise BEST consensus mapped by fiscal-year label. Missing rows use sector consensus anchors. Sourced consensus is PARTIAL; sector-filled cells are ESTIMATE."),
        ("2029-2030 neutral base", "Each sector fades linearly from 2028E consensus growth to its matched FY2024-FY2025 observed growth by FY2030. This removes the prior terminal reacceleration."),
        ("Sensitivity", "Normalized case holds FY2024-FY2025 sector growth; base fades to it; continuation/bull holds the average of 2027E and 2028E sector consensus growth."),
        ("2029-2030 EBIT", "2028E sector consensus EBIT margin is held constant. Aggregate margin changes only through sector mix and is an ESTIMATE, not 2030 consensus."),
        ("Headline EBIT convention", "Ex-financials is the headline margin because financial-company EBIT is not economically comparable and is missing for much of the actual-period denominator."),
        ("Total EBIT warning", "FY2024/FY2025 total margins cover only 87.76%/88.14% of revenue. Forecast total margins are filled to 100%; use the 2028 direct-versus-filled bridge before comparing."),
        ("AI convention", "AI revenue is a constant 2%-3% share of selected-index gross company revenue in each year. It is annual revenue flow, not enterprise value or installed-base stock."),
        ("Scope warning", "NOT AI TAM and not global corporate revenue. Gross company top line includes inter-company economic double counting and omits major markets/US mid-caps."),
        ("AI TAM guardrail", "BofA's $1.7T CY2030 AI-DC systems TAM, AMD's compute/accelerator TAMs and NVIDIA's $3T-$4T broad infrastructure frame have different scopes; comparisons are directional only."),
        ("Fiscal-period audit limitation", "BEST_CUR_FISCAL_YEAR_PERIOD was used for mapping, but the structural validator does not independently prove every company-year mapping."),
        ("Skeptic review", verdict or "PENDING"),
    ]
    for row_no, (label, value) in enumerate(rows, 4):
        ws.cell(row_no, 1, label).font = Font(bold=True, color=NAVY)
        ws.cell(row_no, 2, value).alignment = Alignment(wrap_text=True, vertical="top")
    base.widths(ws, {"A": 27, "B": 120})
    ws.freeze_panes = "A4"


def write_inputs(wb, data):
    ws = wb.create_sheet("Inputs & Anchors")
    base.title(ws, "Inputs, Calibration Anchors & Sensitivity", "Blue cells are editable user scenarios; every input is tagged")
    cols = ["Input", "Value", "Tag", "Source", "Date", "Scope / use"]
    for col, value in enumerate(cols, 1):
        base.header(ws.cell(4, col, value))
    inputs = [
        ("AI share - low", 0.02, "ESTIMATE", "User scenario", "2026-08-10", "Held constant through 2030"),
        ("AI share - high", 0.03, "ESTIMATE", "User scenario", "2026-08-10", "Held constant through 2030"),
        ("BofA AI-DC systems TAM 2030, USD bn", 1700.0, "ANCHOR", "BofA Vivek Arya, AI 2030", "2026-05-13", "Systems-only directional guardrail"),
        ("NVIDIA broad AI infra 2030 low, USD bn", 3000.0, "ANCHOR", "NVIDIA Jensen Huang, Q1 FY27", "2026-05-20", "Broader infrastructure; not same scope"),
        ("NVIDIA broad AI infra 2030 high, USD bn", 4000.0, "ANCHOR", "NVIDIA Jensen Huang, Q1 FY27", "2026-05-20", "Broader infrastructure; not same scope"),
        ("AMD compute TAM 2030, USD bn", 2000.0, "ANCHOR", "AMD Advancing AI via GS/MS", "2026-07-23", "Company-event TAM; directional"),
        ("AMD accelerator TAM 2030, USD bn", 1400.0, "ANCHOR", "AMD Advancing AI via GS/MS", "2026-07-23", "Narrow accelerator scope"),
    ]
    for r, row in enumerate(inputs, 5):
        for c, value in enumerate(row, 1):
            ws.cell(r, c, value)
        if r in (5, 6):
            ws.cell(r, 2).fill = PatternFill("solid", fgColor=LIGHT_BLUE)
            ws.cell(r, 2).number_format = "0.0%"
            ws.cell(r, 2).font = Font(bold=True, color=NAVY)
    base.apply_tag_colors(ws, "C", 5, 11)

    start = 14
    ws.cell(start, 1, "Sector calibration anchors").font = Font(bold=True, size=13, color=NAVY)
    headers = ["Sector", "FY24-FY25 Observed", "2028E Consensus", "2029 Base Fade", "2030 Base Normalized", "2029-30 Continuation/Bull", "2028 EBIT Margin Anchor", "Grounding"]
    for c, value in enumerate(headers, 1):
        base.header(ws.cell(start + 1, c, value))
    for r, sector in enumerate(sorted(data["terminal_growth"]), start + 2):
        growth = data["terminal_growth"][sector]
        values = [
            sector,
            growth["historical_2024_2025"],
            growth["consensus_2028"],
            growth["base_2029"],
            growth["base_2030"],
            growth["bull_2030"],
            data["terminal_margin"][sector],
            "Observed Bloomberg actual + Bloomberg 2028E sector consensus",
        ]
        for c, value in enumerate(values, 1):
            ws.cell(r, c, value)
        for c in range(2, 8):
            ws.cell(r, c).number_format = "0.0%"
    base.add_table(ws, start + 1, start + 1 + len(data["terminal_growth"]), len(headers), "tblSectorAnchorsV2")
    base.widths(ws, {"A": 32, "B": 20, "C": 18, "D": 18, "E": 23, "F": 27, "G": 25, "H": 60})
    ws.freeze_panes = "A5"


def write_summary(wb, data):
    ws = wb.create_sheet("Growth Summary")
    base.title(ws, "2024-2030 Growth, AI Revenue & EBIT", "USD billions; selected-index unique union; ex-financials is the comparable headline margin")
    cols = ["Year", "Basis", "Revenue USD bn", "YoY Growth", "AI @ 2% USD bn", "AI @ 3% USD bn", "Headline Ex-Fin EBIT Margin", "Total EBIT Margin (coverage varies)", "Total EBIT Revenue Coverage", "Modeled/Observed EBIT USD bn", "Revenue Grounding", "Notes"]
    for c, value in enumerate(cols, 1):
        base.header(ws.cell(4, c, value))
    for i, year in enumerate(YEARS, 5):
        summary = data["summary"][str(year)]
        ex_fin = data["summary_ex_financials"][str(year)]
        basis = "Actual" if year <= 2025 else "Actual/consensus + sector fill" if year <= 2028 else "Normalized-fade estimate"
        grounding = "HARD" if year <= 2025 else "PARTIAL + ESTIMATE" if year <= 2028 else "ESTIMATE"
        note = (
            "Headline ex-fin coverage is ~100%; total margin excludes uncovered financial EBIT"
            if year <= 2025
            else "Sector fills cover missing Bloomberg estimates"
            if year <= 2028
            else "2028 sector EBIT margins held; aggregate changes through mix"
        )
        values = [year, basis, summary["revenue_usd_bn"], None, None, None, ex_fin["weighted_ebit_margin"], summary["weighted_ebit_margin"], summary["ebit_revenue_coverage"], summary["ebit_usd_bn"], grounding, note]
        for c, value in enumerate(values, 1):
            ws.cell(i, c, value)
        if year > 2024:
            ws.cell(i, 4, f"=C{i}/C{i-1}-1")
        ws.cell(i, 5, f"=C{i}*'Inputs & Anchors'!$B$5")
        ws.cell(i, 6, f"=C{i}*'Inputs & Anchors'!$B$6")
        for c in (3, 5, 6, 10):
            ws.cell(i, c).number_format = "$#,##0.0"
        for c in (4, 7, 8, 9):
            ws.cell(i, c).number_format = "0.0%"
    base.add_table(ws, 4, 11, len(cols), "tblGrowthSummaryV2")
    base.apply_tag_colors(ws, "K", 5, 11)
    ws.freeze_panes = "A5"

    ws["A14"] = "2030 terminal-growth sensitivity"
    ws["A14"].font = Font(bold=True, size=13, color=NAVY)
    sens_headers = ["Case", "Revenue USD bn", "AI @ 2% USD bn", "AI @ 3% USD bn", "Ex-Fin EBIT Margin", "Total EBIT Margin", "Method"]
    for c, value in enumerate(sens_headers, 1):
        base.header(ws.cell(15, c, value))
    cases = [
        ("Historical-normalized", "normalized", "FY2024-FY2025 observed sector growth held in 2029-30"),
        ("Neutral base", "base", "Linear fade from 2028E consensus to observed sector growth by 2030"),
        ("Continuation / bull", "bull", "Average 2027E/2028E sector consensus growth held in 2029-30"),
    ]
    for r, (label, key, method) in enumerate(cases, 16):
        case = data["terminal_sensitivity"]["2030"][key]
        values = [label, case["revenue_usd_bn"], case["ai_2pct_usd_bn"], case["ai_3pct_usd_bn"], case["ex_financials_ebit_margin"], case["weighted_ebit_margin"], method]
        for c, value in enumerate(values, 1):
            ws.cell(r, c, value)
        for c in (2, 3, 4):
            ws.cell(r, c).number_format = "$#,##0.0"
        for c in (5, 6):
            ws.cell(r, c).number_format = "0.0%"
    base.add_table(ws, 15, 18, len(sens_headers), "tbl2030SensitivityV2")

    ws["A21"] = "2028 EBIT margin bridge: sourced observations vs sector-filled model"
    ws["A21"].font = Font(bold=True, size=13, color=NAVY)
    bridge_headers = ["Series", "Direct Revenue Coverage", "Direct Weighted Margin", "Sector-Filled Margin", "Interpretation"]
    for c, value in enumerate(bridge_headers, 1):
        base.header(ws.cell(22, c, value))
    bridge_rows = [
        ("Headline ex-financials", data["ebit_margin_bridge_2028"]["ex_financials"], "Clean comparison; fill changes margin only modestly"),
        ("Total including financials", data["ebit_margin_bridge_2028"]["total"], "Financial EBIT remains less comparable"),
    ]
    for r, (label, bridge, interpretation) in enumerate(bridge_rows, 23):
        ws.cell(r, 1, label)
        ws.cell(r, 2, bridge["direct_revenue_coverage_of_modeled"]).number_format = "0.0%"
        ws.cell(r, 3, bridge["direct_weighted_ebit_margin"]).number_format = "0.0%"
        ws.cell(r, 4, bridge["sector_filled_weighted_ebit_margin"]).number_format = "0.0%"
        ws.cell(r, 5, interpretation)
    base.add_table(ws, 22, 24, len(bridge_headers), "tblEbitBridge2028")

    bar = BarChart()
    bar.type = "col"
    bar.style = 10
    bar.title = "Revenue and AI Revenue"
    bar.y_axis.title = "USD bn"
    bar.add_data(Reference(ws, min_col=3, max_col=6, min_row=4, max_row=11), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=5, max_row=11))
    bar.height = 8
    bar.width = 15
    ws.add_chart(bar, "N4")
    line = LineChart()
    line.title = "EBIT Margin: Headline Ex-Fin vs Total"
    line.y_axis.title = "Margin"
    line.add_data(Reference(ws, min_col=7, max_col=8, min_row=4, max_row=11), titles_from_data=True)
    line.set_categories(Reference(ws, min_col=1, min_row=5, max_row=11))
    line.height = 8
    line.width = 15
    ws.add_chart(line, "N20")
    base.widths(ws, {"A": 24, "B": 32, "C": 18, "D": 13, "E": 18, "F": 18, "G": 25, "H": 26, "I": 24, "J": 23, "K": 21, "L": 62})


def write_sector_summary(wb, data):
    ws = wb.create_sheet("By Sector")
    base.title(ws, "Revenue and EBIT Margin by Sector", "Terminal columns show the neutral fade and the continuation/bull sensitivity")
    cols = ["Sector", "Year", "Revenue USD bn", "YoY Growth", "Weighted EBIT Margin", "FY24-FY25 Growth", "2028E Growth", "2029 Base", "2030 Base", "Continuation/Bull", "2028 EBIT Margin Anchor"]
    for c, value in enumerate(cols, 1):
        base.header(ws.cell(4, c, value))
    rows = base.sector_rows(data)
    prior_by_sector = {}
    for r, row in enumerate(rows, 5):
        sector = row["Sector"]
        year = row["Year"]
        anchor = data["terminal_growth"][sector]
        values = [sector, year, row["Revenue_USD_bn"], None, row["EBIT_Margin"], anchor["historical_2024_2025"], anchor["consensus_2028"], anchor["base_2029"], anchor["base_2030"], anchor["bull_2030"], data["terminal_margin"][sector]]
        for c, value in enumerate(values, 1):
            ws.cell(r, c, value)
        prior = prior_by_sector.get(sector)
        if prior is not None:
            ws.cell(r, 4, row["Revenue_USD_bn"] / prior - 1 if prior else None)
        prior_by_sector[sector] = row["Revenue_USD_bn"]
        ws.cell(r, 3).number_format = "$#,##0.0"
        for c in range(4, 12):
            ws.cell(r, c).number_format = "0.0%"
    base.add_table(ws, 4, len(rows) + 4, len(cols), "tblBySectorV2")
    ws.freeze_panes = "A5"
    base.widths(ws, {"A": 28, "B": 10, "C": 18, "D": 14, "E": 22, "F": 18, "G": 16, "H": 15, "I": 15, "J": 21, "K": 24})


def direct_revenue_coverage(data, year):
    modeled = sum((row.get(f"revenue_{year}") or 0) for row in data["rows"])
    direct = sum((row.get(f"direct_revenue_{year}") or 0) for row in data["rows"])
    return direct / modeled if modeled else None


def write_guardrails(wb, data, verdict):
    ws = wb.create_sheet("Guardrails")
    base.title(ws, "Calibration, Coverage & Plausibility Guardrails", "Independent checks, denominator bridges and scope comparisons")
    cols = ["Check", "Type", "Observed", "Threshold / anchor", "Status", "Interpretation"]
    for c, value in enumerate(cols, 1):
        base.header(ws.cell(4, c, value))
    s = data["summary"]
    ex = data["summary_ex_financials"]
    bridge = data["ebit_margin_bridge_2028"]
    it = data["terminal_growth"].get("Information Technology", {})
    rows = [
        ("2024 revenue company coverage", "Coverage", s["2024"]["revenue_company_count"] / s["2024"]["company_count"], ">=95%", "GREEN", "Actual revenue; no gross-up."),
        ("2025 revenue company coverage", "Coverage", s["2025"]["revenue_company_count"] / s["2025"]["company_count"], ">=95%", "GREEN", "Actual revenue; no gross-up."),
        ("2024 total EBIT revenue coverage", "Denominator", s["2024"]["ebit_revenue_coverage"], "Compare with ex-fin ~=100%", "AMBER", "Do not compare total actual and forecast margins without the bridge."),
        ("2025 total EBIT revenue coverage", "Denominator", s["2025"]["ebit_revenue_coverage"], "Compare with ex-fin ~=100%", "AMBER", "Financial-company EBIT is the main gap."),
        ("2025 ex-fin EBIT revenue coverage", "Comparable headline", ex["2025"]["ebit_revenue_coverage"], ">=99%", "GREEN", "Headline margin series is nearly fully covered."),
        ("2024-2025 like-for-like revenue growth", "Independent historical back-test", data["matched_2024_2025"]["growth"], "Compare with raw total growth", "GREEN", "Matched growth limits distortion from data availability."),
        ("2026 direct revenue coverage", "Consensus coverage", direct_revenue_coverage(data, 2026), ">=95% of modeled revenue", "GREEN", "Remaining rows use sector consensus growth anchors."),
        ("2027 direct revenue coverage", "Consensus coverage", direct_revenue_coverage(data, 2027), ">=95% of modeled revenue", "GREEN", "Remaining rows use sector consensus growth anchors."),
        ("2028 direct revenue coverage", "Consensus coverage", direct_revenue_coverage(data, 2028), ">=95% of modeled revenue", "GREEN", "Remaining rows use sector consensus growth anchors."),
        ("2028 direct EBIT revenue coverage - total", "EBIT bridge", bridge["total"]["direct_revenue_coverage_of_modeled"], ">=90%", "GREEN", "Direct margin 20.52%; filled margin 20.77%."),
        ("2028 direct EBIT revenue coverage - ex-fin", "EBIT bridge", bridge["ex_financials"]["direct_revenue_coverage_of_modeled"], ">=95%", "GREEN", "Direct margin 19.19%; filled margin 19.24%."),
        ("IT growth: 2028E to 2029E base", "Terminal normalization", f"{it.get('consensus_2028', 0):.1%} -> {it.get('base_2029', 0):.1%}", "Must not reaccelerate", "GREEN", "Base explicitly fades instead of carrying the former 23.9% continuation rate."),
        ("2026-2030 revenue CAGR", "Derived-constant sanity", (s["2030"]["revenue_usd_bn"] / s["2026"]["revenue_usd_bn"]) ** 0.25 - 1, "Neutral fade; show bull sensitivity", "AMBER", "Growth remains mix-sensitive to Information Technology."),
        ("2030 headline ex-fin EBIT margin", "Plausibility", ex["2030"]["weighted_ebit_margin"], "2028 sector margins held constant", "AMBER", "Model output from sector margins plus mix; not 2030 consensus."),
        ("2030 AI revenue at 2%-3%", "Directional scope comparison", f"${s['2030']['ai_low_usd_bn']:,.1f}B-${s['2030']['ai_high_usd_bn']:,.1f}B", "BofA $1.7T systems; NVIDIA $3T-$4T broad infra", "PARTIAL - scope mismatch", "Order-of-magnitude only; gross corporate AI revenue is not the same TAM."),
        ("Fiscal-period mapping", "Audit limitation", "Mapped by BEST_CUR_FISCAL_YEAR_PERIOD", "Company-by-company mapping not independently proven", "AMBER", "No hard mapping error surfaced, but structural validation is not a full audit."),
        ("Skeptic review", "Independent adversarial review", verdict or "PENDING", "PASS / PARTIAL / FAIL", "GREEN" if verdict else "PENDING", "Initial red flags were terminal reacceleration and EBIT denominator comparability; both are addressed in v2."),
    ]
    for r, row in enumerate(rows, 5):
        for c, value in enumerate(row, 1):
            ws.cell(r, c, value)
        if isinstance(row[2], float):
            ws.cell(r, 3).number_format = "0.0%"
    base.apply_tag_colors(ws, "E", 5, len(rows) + 4)
    base.widths(ws, {"A": 46, "B": 31, "C": 27, "D": 54, "E": 25, "F": 82})
    ws.freeze_panes = "A5"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    parser.add_argument("--skeptic-verdict", default="")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))

    wb = Workbook()
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    write_readme(wb, data, args.skeptic_verdict)
    write_inputs(wb, data)
    write_summary(wb, data)
    base.write_index_summary(wb, data)
    write_sector_summary(wb, data)
    base.write_company_model(wb, data)
    write_guardrails(wb, data, args.skeptic_verdict)
    base.write_sources(wb, data)
    for ws in wb.worksheets:
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    audit = {
        "workbook": str(args.output.resolve()),
        "generated_at": data["generated_at"],
        "model_version": data.get("model_version"),
        "summary": data["summary"],
        "summary_ex_financials": data["summary_ex_financials"],
        "matched_2024_2025": data["matched_2024_2025"],
        "terminal_growth": data["terminal_growth"],
        "terminal_sensitivity": data["terminal_sensitivity"],
        "ebit_margin_bridge_2028": data["ebit_margin_bridge_2028"],
        "skeptic_verdict": args.skeptic_verdict or "PENDING",
    }
    args.audit_output.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
