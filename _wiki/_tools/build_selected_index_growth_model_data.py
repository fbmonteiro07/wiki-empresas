#!/usr/bin/env python3
"""Build calibrated 2024-2030 revenue/EBIT/AI model data from Bloomberg pulls."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


YEARS = list(range(2024, 2031))
FORECAST_YEARS = [2026, 2027, 2028]


def num(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def period_year(value):
    if not value:
        return None
    try:
        year = int(str(value).split()[0].split("/")[-1])
        return year + 2000 if year < 100 else year
    except (TypeError, ValueError):
        return None


def direct_forecast(data, security, target_year):
    actual = data.get(f"actual_{target_year}", {}).get(security, {})
    actual_revenue = num(actual.get("SALES_REV_TURN"))
    actual_ebit = num(actual.get("EBIT"))
    if actual_revenue is not None:
        return actual_revenue, actual_ebit, "HARD", f"Bloomberg FY{target_year} actual"
    current = data["estimates"]["1FY"].get(security, {})
    current_year = period_year(current.get("BEST_CUR_FISCAL_YEAR_PERIOD"))
    if current_year is None:
        return None, None, "MISSING", "No fiscal-period mapping"
    for step, period in enumerate(("1FY", "2FY", "3FY")):
        if current_year + step == target_year:
            estimate = data["estimates"][period].get(security, {})
            return (
                num(estimate.get("BEST_SALES")),
                num(estimate.get("BEST_EBIT")),
                "PARTIAL",
                f"Bloomberg consensus {period} mapped to FY{target_year}",
            )
    return None, None, "MISSING", f"No Bloomberg consensus mapped to FY{target_year}"


def weighted_growth(pairs):
    pairs = [(prior, target) for prior, target in pairs if prior is not None and target is not None and prior > 0]
    prior_sum = sum(prior for prior, _ in pairs)
    target_sum = sum(target for _, target in pairs)
    return target_sum / prior_sum - 1 if prior_sum else None


def weighted_margin(pairs):
    pairs = [(revenue, ebit) for revenue, ebit in pairs if revenue is not None and ebit is not None and revenue > 0]
    revenue_sum = sum(revenue for revenue, _ in pairs)
    return sum(ebit for _, ebit in pairs) / revenue_sum if revenue_sum else None


def summarize(rows, year, revenue_field="revenue", ebit_field="ebit", exclude_financials=False):
    filtered = [row for row in rows if not exclude_financials or row["sector"] != "Financials"]
    revenue_values = [num(row.get(f"{revenue_field}_{year}")) for row in filtered]
    total_revenue = sum(value for value in revenue_values if value is not None)
    pairs = [
        (num(row.get(f"{revenue_field}_{year}")), num(row.get(f"{ebit_field}_{year}")))
        for row in filtered
    ]
    covered = [(revenue, ebit) for revenue, ebit in pairs if revenue is not None and ebit is not None]
    covered_revenue = sum(revenue for revenue, _ in covered)
    total_ebit = sum(ebit for _, ebit in covered)
    return {
        "company_count": len(filtered),
        "revenue_company_count": sum(value is not None for value in revenue_values),
        "revenue_usd_bn": total_revenue / 1000,
        "ebit_company_count": len(covered),
        "ebit_usd_bn": total_ebit / 1000,
        "ebit_covered_revenue_usd_bn": covered_revenue / 1000,
        "ebit_revenue_coverage": covered_revenue / total_revenue if total_revenue else None,
        "weighted_ebit_margin": total_ebit / covered_revenue if covered_revenue else None,
        "ai_low_usd_bn": total_revenue * 0.02 / 1000,
        "ai_high_usd_bn": total_revenue * 0.03 / 1000,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    rows = []
    for company in data["companies"]:
        security = company["security"]
        row = dict(company)
        for year in (2024, 2025):
            actual = data[f"actual_{year}"].get(security, {})
            row[f"revenue_{year}"] = num(actual.get("SALES_REV_TURN"))
            row[f"ebit_{year}"] = num(actual.get("EBIT"))
            row[f"revenue_tag_{year}"] = "HARD" if row[f"revenue_{year}"] is not None else "MISSING"
            row[f"ebit_tag_{year}"] = "HARD" if row[f"ebit_{year}"] is not None else "MISSING"
            row[f"source_{year}"] = f"Bloomberg FY{year} actual; 2026-08-10 snapshot"
        for year in FORECAST_YEARS:
            revenue, ebit, tag, source = direct_forecast(data, security, year)
            row[f"direct_revenue_{year}"] = revenue
            row[f"direct_ebit_{year}"] = ebit
            row[f"direct_tag_{year}"] = tag
            row[f"direct_source_{year}"] = source
        rows.append(row)

    sectors = sorted({row.get("sector") or "Unclassified" for row in rows})
    for row in rows:
        if not row.get("sector"):
            row["sector"] = "Unclassified"

    growth_anchors = {}
    margin_anchors = {}
    prior_direct_field = {2026: "revenue_2025", 2027: "direct_revenue_2026", 2028: "direct_revenue_2027"}
    for year in FORECAST_YEARS:
        growth_anchors[str(year)] = {}
        margin_anchors[str(year)] = {}
        all_growth_pairs = []
        all_margin_pairs = []
        for sector in sectors:
            sector_rows = [row for row in rows if row["sector"] == sector]
            growth_pairs = [
                (num(row.get(prior_direct_field[year])), num(row.get(f"direct_revenue_{year}")))
                for row in sector_rows
            ]
            margin_pairs = [
                (num(row.get(f"direct_revenue_{year}")), num(row.get(f"direct_ebit_{year}")))
                for row in sector_rows
            ]
            growth_anchors[str(year)][sector] = weighted_growth(growth_pairs)
            margin_anchors[str(year)][sector] = weighted_margin(margin_pairs)
            all_growth_pairs.extend(growth_pairs)
            all_margin_pairs.extend(margin_pairs)
        growth_anchors[str(year)]["__GLOBAL__"] = weighted_growth(all_growth_pairs)
        margin_anchors[str(year)]["__GLOBAL__"] = weighted_margin(all_margin_pairs)

    for year in FORECAST_YEARS:
        for row in rows:
            direct_revenue = num(row[f"direct_revenue_{year}"])
            prior_revenue = num(row.get(f"revenue_{year - 1}"))
            if direct_revenue is not None:
                row[f"revenue_{year}"] = direct_revenue
                row[f"revenue_tag_{year}"] = row[f"direct_tag_{year}"]
                row[f"source_{year}"] = row[f"direct_source_{year}"]
            elif prior_revenue is not None:
                growth = growth_anchors[str(year)].get(row["sector"])
                if growth is None:
                    growth = growth_anchors[str(year)]["__GLOBAL__"]
                row[f"revenue_{year}"] = prior_revenue * (1 + growth) if growth is not None else None
                row[f"revenue_tag_{year}"] = "ESTIMATE" if row[f"revenue_{year}"] is not None else "MISSING"
                row[f"source_{year}"] = f"Sector consensus growth anchor applied to prior year ({growth:.2%})" if growth is not None else "Missing"
            else:
                row[f"revenue_{year}"] = None
                row[f"revenue_tag_{year}"] = "MISSING"
                row[f"source_{year}"] = "Missing prior revenue and direct consensus"

            direct_ebit = num(row[f"direct_ebit_{year}"])
            if direct_ebit is not None:
                row[f"ebit_{year}"] = direct_ebit
                row[f"ebit_tag_{year}"] = row[f"direct_tag_{year}"]
            else:
                margin = margin_anchors[str(year)].get(row["sector"])
                if margin is None:
                    margin = margin_anchors[str(year)]["__GLOBAL__"]
                revenue = num(row[f"revenue_{year}"])
                row[f"ebit_{year}"] = revenue * margin if revenue is not None and margin is not None else None
                row[f"ebit_tag_{year}"] = "ESTIMATE" if row[f"ebit_{year}"] is not None else "MISSING"

    terminal_growth = {}
    terminal_margin = {}
    for sector in sectors:
        available_growth = [
            growth_anchors[str(year)].get(sector)
            for year in (2027, 2028)
            if growth_anchors[str(year)].get(sector) is not None
        ]
        if not available_growth:
            available_growth = [growth_anchors["2028"]["__GLOBAL__"]]
        terminal_growth[sector] = {
            "low": min(available_growth),
            "base": sum(available_growth) / len(available_growth),
            "high": max(available_growth),
        }
        margin = margin_anchors["2028"].get(sector)
        terminal_margin[sector] = margin if margin is not None else margin_anchors["2028"]["__GLOBAL__"]

    for row in rows:
        sector = row["sector"]
        for case in ("low", "base", "high"):
            prior = num(row["revenue_2028"])
            for year in (2029, 2030):
                value = prior * (1 + terminal_growth[sector][case]) if prior is not None else None
                row[f"revenue_{year}_{case}"] = value
                prior = value
        for year in (2029, 2030):
            row[f"revenue_{year}"] = row[f"revenue_{year}_base"]
            row[f"revenue_tag_{year}"] = "ESTIMATE" if row[f"revenue_{year}"] is not None else "MISSING"
            row[f"source_{year}"] = (
                f"2027E/2028E sector consensus growth average ({terminal_growth[sector]['base']:.2%})"
            )
            revenue = num(row[f"revenue_{year}"])
            row[f"ebit_{year}"] = revenue * terminal_margin[sector] if revenue is not None else None
            row[f"ebit_tag_{year}"] = "ESTIMATE" if row[f"ebit_{year}"] is not None else "MISSING"

    summary = {}
    summary_ex_fin = {}
    for year in YEARS:
        summary[str(year)] = summarize(rows, year)
        summary_ex_fin[str(year)] = summarize(rows, year, exclude_financials=True)
        if year in (2029, 2030):
            for case in ("low", "high"):
                case_summary = summarize(rows, year, revenue_field=f"revenue_{year}_{case}".rsplit(f"_{year}", 1)[0])
                summary[str(year)][f"revenue_{case}_usd_bn"] = case_summary["revenue_usd_bn"]

    # Correct low/high totals directly; summarize expects the conventional field naming.
    for year in (2029, 2030):
        for case in ("low", "high"):
            total = sum(num(row.get(f"revenue_{year}_{case}")) or 0 for row in rows) / 1000
            summary[str(year)][f"revenue_{case}_usd_bn"] = total
            summary[str(year)][f"ai_2pct_{case}_usd_bn"] = total * 0.02
            summary[str(year)][f"ai_3pct_{case}_usd_bn"] = total * 0.03

    # Historical like-for-like growth guardrail.
    matched_24_25 = [row for row in rows if num(row["revenue_2024"]) is not None and num(row["revenue_2025"]) is not None]
    matched_24 = sum(num(row["revenue_2024"]) for row in matched_24_25)
    matched_25 = sum(num(row["revenue_2025"]) for row in matched_24_25)

    output = {
        "generated_at": data["generated_at"],
        "methodology": {
            "2024_2025": "Bloomberg annual actual SALES_REV_TURN and EBIT, USD override",
            "2026_2028": "Bloomberg actual if available, otherwise BEST consensus mapped by fiscal-year label; missing revenue/EBIT uses sector-level consensus anchors",
            "2029_2030_revenue": "Sector terminal growth = average of 2027E and 2028E sector consensus growth; low/high use min/max of those two sourced rates",
            "2029_2030_ebit": "2028E sector consensus EBIT margin held constant; mix shifts remain in aggregate",
            "ai_revenue": "2% and 3% of selected-index company revenue in each year; user scenario held constant",
        },
        "growth_anchors": growth_anchors,
        "margin_anchors": margin_anchors,
        "terminal_growth": terminal_growth,
        "terminal_margin": terminal_margin,
        "summary": summary,
        "summary_ex_financials": summary_ex_fin,
        "matched_2024_2025": {
            "company_count": len(matched_24_25),
            "revenue_2024_usd_bn": matched_24 / 1000,
            "revenue_2025_usd_bn": matched_25 / 1000,
            "growth": matched_25 / matched_24 - 1 if matched_24 else None,
        },
        "rows": rows,
    }
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items() if key not in {"rows", "growth_anchors", "margin_anchors", "terminal_growth", "terminal_margin"}}, indent=2))


if __name__ == "__main__":
    main()
