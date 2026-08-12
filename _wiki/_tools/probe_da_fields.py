#!/usr/bin/env python3
"""Probe Bloomberg actual and consensus D&A-related fields on representative names."""

from __future__ import annotations

import json
from pathlib import Path

from probe_revenue_ebit_history import Client


def main():
    securities = ["AAPL US Equity", "005930 KS Equity", "2330 TT Equity", "SAP GY Equity"]
    actual_fields = [
        "NAME",
        "SALES_REV_TURN",
        "EBIT",
        "EBITDA",
        "CF_DEPR_AMORT",
        "IS_DEPRECIATION_AND_AMORTIZATION",
        "DEPR_AND_AMORT",
    ]
    estimate_fields = [
        "NAME",
        "BEST_CUR_FISCAL_YEAR_PERIOD",
        "BEST_SALES",
        "BEST_EBIT",
        "BEST_EBITDA",
        "BEST_DEPR_AMORT",
        "BEST_DEPR_EXP",
    ]
    client = Client()
    try:
        result = {
            "actual_2024": client.ref(
                securities,
                actual_fields,
                {"EQY_FUND_YEAR": "2024", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            ),
            "actual_2025": client.ref(
                securities,
                actual_fields,
                {"EQY_FUND_YEAR": "2025", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            ),
            "best_1fy": client.ref(
                securities,
                estimate_fields,
                {"BEST_FPERIOD_OVERRIDE": "1FY", "EQY_FUND_CRNCY": "USD"},
            ),
            "best_2fy": client.ref(
                securities,
                estimate_fields,
                {"BEST_FPERIOD_OVERRIDE": "2FY", "EQY_FUND_CRNCY": "USD"},
            ),
        }
    finally:
        client.close()
    output = Path("E:/Wiki Felipe empresas/da_field_probe.json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
