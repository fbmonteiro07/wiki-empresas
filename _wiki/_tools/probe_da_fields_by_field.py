#!/usr/bin/env python3
"""Probe candidate Bloomberg D&A fields one request at a time."""

from __future__ import annotations

import json
from pathlib import Path

from probe_revenue_ebit_history import Client


def main():
    securities = ["AAPL US Equity", "005930 KS Equity", "2330 TT Equity", "SAP GY Equity"]
    actual_fields = ["NAME", "SALES_REV_TURN", "EBIT", "EBITDA", "CF_DEPR_AMORT", "IS_DEPRECIATION_AND_AMORTIZATION", "DEPR_AND_AMORT"]
    estimate_fields = ["NAME", "BEST_CUR_FISCAL_YEAR_PERIOD", "BEST_SALES", "BEST_EBIT", "BEST_EBITDA", "BEST_DEPR_AMORT", "BEST_DEPR_EXP"]
    client = Client()
    try:
        result = {"actual_fields": {}, "estimate_fields": {}}
        for field in actual_fields:
            result["actual_fields"][field] = client.ref(
                securities,
                [field],
                {"EQY_FUND_YEAR": "2024", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            )
        for field in estimate_fields:
            result["estimate_fields"][field] = client.ref(
                securities,
                [field],
                {"BEST_FPERIOD_OVERRIDE": "1FY", "EQY_FUND_CRNCY": "USD"},
            )
    finally:
        client.close()
    output = Path("E:/Wiki Felipe empresas/da_field_probe_by_field.json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
