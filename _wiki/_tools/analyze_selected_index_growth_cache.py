#!/usr/bin/env python3
"""Analyze coverage, period mapping, growth and EBIT margins in the extraction."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


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
    text = str(value).split()[0]
    try:
        year = int(text.split("/")[-1])
        return 2000 + year if year < 100 else year
    except (TypeError, ValueError):
        return None


def aggregate(rows, revenue_key, ebit_key, exclude_financials=False):
    relevant = [r for r in rows if not exclude_financials or r["sector"] != "Financials"]
    revenue_values = [num(r[revenue_key]) for r in relevant]
    ebit_pairs = [(num(r[revenue_key]), num(r[ebit_key])) for r in relevant]
    total_revenue = sum(value for value in revenue_values if value is not None)
    covered_pairs = [(revenue, ebit) for revenue, ebit in ebit_pairs if revenue is not None and ebit is not None]
    covered_revenue = sum(revenue for revenue, _ in covered_pairs)
    total_ebit = sum(ebit for _, ebit in covered_pairs)
    return {
        "company_count": len(relevant),
        "revenue_company_count": sum(value is not None for value in revenue_values),
        "revenue_usd_bn": total_revenue / 1000,
        "ebit_company_count": len(covered_pairs),
        "ebit_covered_revenue_usd_bn": covered_revenue / 1000,
        "ebit_revenue_coverage": covered_revenue / total_revenue if total_revenue else None,
        "ebit_usd_bn": total_ebit / 1000,
        "weighted_ebit_margin": total_ebit / covered_revenue if covered_revenue else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    companies = data["companies"]
    rows = []
    for company in companies:
        security = company["security"]
        row = dict(company)
        for year in (2024, 2025, 2026):
            actual = data[f"actual_{year}"].get(security, {})
            row[f"revenue_{year}_actual"] = actual.get("SALES_REV_TURN")
            row[f"ebit_{year}_actual"] = actual.get("EBIT")
        current_period = data["estimates"]["1FY"].get(security, {}).get("BEST_CUR_FISCAL_YEAR_PERIOD")
        current_year = period_year(current_period)
        row["current_estimate_period"] = current_period
        row["current_estimate_year"] = current_year
        for step, period in enumerate(("1FY", "2FY", "3FY")):
            estimate = data["estimates"][period].get(security, {})
            estimate_year = current_year + step if current_year else None
            row[f"estimate_year_{period}"] = estimate_year
            row[f"revenue_{period}"] = estimate.get("BEST_SALES")
            row[f"ebit_{period}"] = estimate.get("BEST_EBIT")
        rows.append(row)

    period_counts = Counter(row["current_estimate_year"] for row in rows)
    raw = {}
    raw_ex_fin = {}
    for year in (2024, 2025, 2026):
        raw[str(year)] = aggregate(rows, f"revenue_{year}_actual", f"ebit_{year}_actual")
        raw_ex_fin[str(year)] = aggregate(rows, f"revenue_{year}_actual", f"ebit_{year}_actual", True)
    for period in ("1FY", "2FY", "3FY"):
        raw[period] = aggregate(rows, f"revenue_{period}", f"ebit_{period}")
        raw_ex_fin[period] = aggregate(rows, f"revenue_{period}", f"ebit_{period}", True)

    matched_24_25 = [r for r in rows if num(r["revenue_2024_actual"]) is not None and num(r["revenue_2025_actual"]) is not None]
    rev24 = sum(num(r["revenue_2024_actual"]) for r in matched_24_25)
    rev25 = sum(num(r["revenue_2025_actual"]) for r in matched_24_25)
    fy1_2026 = [r for r in rows if r["current_estimate_year"] == 2026 and num(r["revenue_2025_actual"]) is not None and num(r["revenue_1FY"]) is not None]
    rev25_fy1 = sum(num(r["revenue_2025_actual"]) for r in fy1_2026)
    rev26_fy1 = sum(num(r["revenue_1FY"]) for r in fy1_2026)
    report = {
        "generated_at": data["generated_at"],
        "company_count": len(rows),
        "current_estimate_year_counts": {str(k): v for k, v in sorted(period_counts.items(), key=lambda x: (x[0] is None, x[0] or 9999))},
        "raw_aggregate": raw,
        "raw_aggregate_ex_financials": raw_ex_fin,
        "matched_growth": {
            "2024_to_2025_company_count": len(matched_24_25),
            "2024_revenue_usd_bn": rev24 / 1000,
            "2025_revenue_usd_bn": rev25 / 1000,
            "growth": rev25 / rev24 - 1 if rev24 else None,
            "2025_to_2026e_company_count": len(fy1_2026),
            "2025_revenue_usd_bn_for_2026e_cohort": rev25_fy1 / 1000,
            "2026e_revenue_usd_bn": rev26_fy1 / 1000,
            "growth_2026e": rev26_fy1 / rev25_fy1 - 1 if rev25_fy1 else None,
        },
        "workbook_latest_revenue_usd_bn": sum(num(row["workbook_fy_revenue_usd_m"]) or 0 for row in rows) / 1000,
        "rows": rows,
    }
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "rows"}, indent=2))


if __name__ == "__main__":
    main()
