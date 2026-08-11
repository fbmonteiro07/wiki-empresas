#!/usr/bin/env python3
"""Normalize 2029-30 growth and add comparable EBIT-margin bridges.

This is a second-pass calibration applied to the first Bloomberg-backed model.
The neutral base fades each sector's 2028E consensus growth to its matched
FY2024-FY2025 observed growth by FY2030.  The former continuation case is kept
as an explicitly labelled bull sensitivity.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


YEARS = range(2024, 2031)


def num(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def weighted_growth(rows, prior_field, target_field):
    pairs = [
        (num(row.get(prior_field)), num(row.get(target_field)))
        for row in rows
    ]
    pairs = [(prior, target) for prior, target in pairs if prior is not None and target is not None and prior > 0]
    prior_total = sum(prior for prior, _ in pairs)
    target_total = sum(target for _, target in pairs)
    return target_total / prior_total - 1 if prior_total else None


def summarize(rows, year, revenue_field=None, ebit_field=None, exclude_financials=False):
    revenue_field = revenue_field or f"revenue_{year}"
    ebit_field = ebit_field or f"ebit_{year}"
    selected = [row for row in rows if not exclude_financials or row["sector"] != "Financials"]
    revenues = [num(row.get(revenue_field)) for row in selected]
    total_revenue = sum(value for value in revenues if value is not None)
    pairs = [
        (num(row.get(revenue_field)), num(row.get(ebit_field)))
        for row in selected
    ]
    covered = [(revenue, ebit) for revenue, ebit in pairs if revenue is not None and ebit is not None]
    covered_revenue = sum(revenue for revenue, _ in covered)
    total_ebit = sum(ebit for _, ebit in covered)
    return {
        "company_count": len(selected),
        "revenue_company_count": sum(value is not None for value in revenues),
        "revenue_usd_bn": total_revenue / 1000,
        "ebit_company_count": len(covered),
        "ebit_usd_bn": total_ebit / 1000,
        "ebit_covered_revenue_usd_bn": covered_revenue / 1000,
        "ebit_revenue_coverage": covered_revenue / total_revenue if total_revenue else None,
        "weighted_ebit_margin": total_ebit / covered_revenue if covered_revenue else None,
        "ai_low_usd_bn": total_revenue * 0.02 / 1000,
        "ai_high_usd_bn": total_revenue * 0.03 / 1000,
    }


def direct_margin_bridge(rows, year, exclude_financials=False):
    selected = [row for row in rows if not exclude_financials or row["sector"] != "Financials"]
    modeled_revenue = sum(num(row.get(f"revenue_{year}")) or 0 for row in selected)
    direct_pairs = [
        (num(row.get(f"direct_revenue_{year}")), num(row.get(f"direct_ebit_{year}")))
        for row in selected
    ]
    direct_pairs = [(revenue, ebit) for revenue, ebit in direct_pairs if revenue is not None and ebit is not None]
    direct_revenue = sum(revenue for revenue, _ in direct_pairs)
    direct_ebit = sum(ebit for _, ebit in direct_pairs)
    full = summarize(selected, year)
    return {
        "direct_company_count": len(direct_pairs),
        "direct_revenue_usd_bn": direct_revenue / 1000,
        "direct_ebit_usd_bn": direct_ebit / 1000,
        "direct_revenue_coverage_of_modeled": direct_revenue / modeled_revenue if modeled_revenue else None,
        "direct_weighted_ebit_margin": direct_ebit / direct_revenue if direct_revenue else None,
        "sector_filled_weighted_ebit_margin": full["weighted_ebit_margin"],
        "sector_filled_revenue_coverage": full["ebit_revenue_coverage"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    rows = data["rows"]
    sectors = sorted({row["sector"] for row in rows})

    global_hist = weighted_growth(rows, "revenue_2024", "revenue_2025")
    terminal_growth = {}
    for sector in sectors:
        sector_rows = [row for row in rows if row["sector"] == sector]
        historical = weighted_growth(sector_rows, "revenue_2024", "revenue_2025")
        if historical is None:
            historical = global_hist
        growth_2027 = num(data["growth_anchors"]["2027"].get(sector))
        growth_2028 = num(data["growth_anchors"]["2028"].get(sector))
        if growth_2028 is None:
            growth_2028 = num(data["growth_anchors"]["2028"].get("__GLOBAL__"))
        available = [value for value in (growth_2027, growth_2028) if value is not None]
        continuation = sum(available) / len(available) if available else historical
        terminal_growth[sector] = {
            "historical_2024_2025": historical,
            "consensus_2028": growth_2028,
            "base_2029": (growth_2028 + historical) / 2,
            "base_2030": historical,
            "normalized_2029": historical,
            "normalized_2030": historical,
            "bull_2029": continuation,
            "bull_2030": continuation,
        }

    for row in rows:
        sector = row["sector"]
        anchor = terminal_growth[sector]
        margin = num(data["terminal_margin"].get(sector))
        for case in ("normalized", "base", "bull"):
            prior = num(row.get("revenue_2028"))
            for year in (2029, 2030):
                growth = anchor[f"{case}_{year}"]
                revenue = prior * (1 + growth) if prior is not None else None
                row[f"revenue_{year}_{case}"] = revenue
                row[f"ebit_{year}_{case}"] = revenue * margin if revenue is not None and margin is not None else None
                prior = revenue
        for year in (2029, 2030):
            row[f"revenue_{year}"] = row[f"revenue_{year}_base"]
            row[f"ebit_{year}"] = row[f"ebit_{year}_base"]
            row[f"revenue_tag_{year}"] = "ESTIMATE" if row[f"revenue_{year}"] is not None else "MISSING"
            row[f"ebit_tag_{year}"] = "ESTIMATE" if row[f"ebit_{year}"] is not None else "MISSING"
            row[f"source_{year}"] = (
                "Sector growth fades from 2028E consensus toward matched FY2024-FY2025 observed growth; "
                f"FY{year}={anchor[f'base_{year}']:.2%}"
            )

    summary = {str(year): summarize(rows, year) for year in YEARS}
    summary_ex_fin = {str(year): summarize(rows, year, exclude_financials=True) for year in YEARS}
    sensitivity = {}
    for year in (2029, 2030):
        sensitivity[str(year)] = {}
        for case in ("normalized", "base", "bull"):
            total = summarize(rows, year, f"revenue_{year}_{case}", f"ebit_{year}_{case}")
            ex_fin = summarize(rows, year, f"revenue_{year}_{case}", f"ebit_{year}_{case}", True)
            sensitivity[str(year)][case] = {
                "revenue_usd_bn": total["revenue_usd_bn"],
                "ai_2pct_usd_bn": total["revenue_usd_bn"] * 0.02,
                "ai_3pct_usd_bn": total["revenue_usd_bn"] * 0.03,
                "weighted_ebit_margin": total["weighted_ebit_margin"],
                "ex_financials_ebit_margin": ex_fin["weighted_ebit_margin"],
            }
        summary[str(year)]["revenue_low_usd_bn"] = sensitivity[str(year)]["normalized"]["revenue_usd_bn"]
        summary[str(year)]["revenue_high_usd_bn"] = sensitivity[str(year)]["bull"]["revenue_usd_bn"]

    matched = [row for row in rows if num(row.get("revenue_2024")) is not None and num(row.get("revenue_2025")) is not None]
    matched_24 = sum(num(row["revenue_2024"]) for row in matched)
    matched_25 = sum(num(row["revenue_2025"]) for row in matched)

    data["model_version"] = "v2-normalized-terminal-growth"
    data["methodology"]["2029_2030_revenue"] = (
        "Neutral base: linear sector fade from 2028E Bloomberg consensus growth to matched FY2024-FY2025 observed growth by FY2030. "
        "Normalized sensitivity holds historical growth; bull continues the average of 2027E/2028E consensus growth."
    )
    data["methodology"]["2029_2030_ebit"] = (
        "2028E sector consensus EBIT margins held constant; aggregate margin changes only through sector mix. "
        "Post-2028 margin is ESTIMATE, not 2030 consensus."
    )
    data["terminal_growth"] = terminal_growth
    data["summary"] = summary
    data["summary_ex_financials"] = summary_ex_fin
    data["terminal_sensitivity"] = sensitivity
    data["ebit_margin_bridge_2028"] = {
        "total": direct_margin_bridge(rows, 2028),
        "ex_financials": direct_margin_bridge(rows, 2028, True),
    }
    data["matched_2024_2025"] = {
        "company_count": len(matched),
        "revenue_2024_usd_bn": matched_24 / 1000,
        "revenue_2025_usd_bn": matched_25 / 1000,
        "growth": matched_25 / matched_24 - 1 if matched_24 else None,
    }
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "model_version": data["model_version"],
        "summary": summary,
        "summary_ex_financials": summary_ex_fin,
        "terminal_sensitivity": sensitivity,
        "ebit_margin_bridge_2028": data["ebit_margin_bridge_2028"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
