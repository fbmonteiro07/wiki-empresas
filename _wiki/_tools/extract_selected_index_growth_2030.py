#!/usr/bin/env python3
"""Extract 2024/2025 actual and FY1/FY2/FY3 consensus revenue/EBIT."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from pathlib import Path

from openpyxl import load_workbook

from probe_revenue_ebit_history import Client


def chunks(items, size=150):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def workbook_companies(path):
    wb = load_workbook(path, read_only=True, data_only=False)
    ws = wb["Companies"]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=4, max_row=4))]
    h = {value: i for i, value in enumerate(headers)}
    rows = []
    for values in ws.iter_rows(min_row=5, values_only=True):
        rows.append(
            {
                "company_key": values[h["Company_Key"]],
                "company_name": values[h["Company_Name"]],
                "security": values[h["Primary_Security"]],
                "sector": values[h["GICS_Sector"]],
                "country": values[h["Country"]],
                "indices": values[h["Index_Memberships"]],
                "workbook_fy_revenue_usd_m": values[h["FY_Revenue_USD_m"]],
                "workbook_fy_period": values[h["FY_Revenue_Period"]],
            }
        )
    wb.close()
    return rows


def merge_batches(client, securities, fields, overrides, batch_size):
    result = {}
    total = math.ceil(len(securities) / batch_size)
    for batch_no, batch in enumerate(chunks(securities, batch_size), 1):
        print(f"{overrides} batch {batch_no}/{total}", flush=True)
        result.update(client.ref(batch, fields, overrides))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=150)
    args = parser.parse_args()
    companies = workbook_companies(args.workbook)
    securities = list(dict.fromkeys(row["security"] for row in companies))
    actual_fields = ["NAME", "EQY_FUND_CRNCY", "SALES_REV_TURN", "EBIT", "OPER_MARGIN"]
    estimate_fields = ["NAME", "BEST_CUR_FISCAL_YEAR_PERIOD", "BEST_SALES", "BEST_EBIT"]
    client = Client()
    try:
        actual_2024 = merge_batches(
            client,
            securities,
            actual_fields,
            {"EQY_FUND_YEAR": "2024", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            args.batch_size,
        )
        actual_2025 = merge_batches(
            client,
            securities,
            actual_fields,
            {"EQY_FUND_YEAR": "2025", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            args.batch_size,
        )
        actual_2026 = merge_batches(
            client,
            securities,
            actual_fields,
            {"EQY_FUND_YEAR": "2026", "FUND_PER": "Y", "EQY_FUND_CRNCY": "USD"},
            args.batch_size,
        )
        estimates = {}
        for period in ("1FY", "2FY", "3FY"):
            estimates[period] = merge_batches(
                client,
                securities,
                estimate_fields,
                {"BEST_FPERIOD_OVERRIDE": period, "EQY_FUND_CRNCY": "USD"},
                args.batch_size,
            )
    finally:
        client.close()
    payload = {
        "generated_at": dt.datetime.now().astimezone().isoformat(),
        "source": "Bloomberg Desktop API //blp/refdata",
        "input_workbook": str(args.workbook.resolve()),
        "company_count": len(companies),
        "security_count": len(securities),
        "companies": companies,
        "actual_2024": actual_2024,
        "actual_2025": actual_2025,
        "actual_2026": actual_2026,
        "estimates": estimates,
        "field_definitions": {
            "actual_revenue": "SALES_REV_TURN; FUND_PER=Y; EQY_FUND_YEAR; EQY_FUND_CRNCY=USD",
            "actual_ebit": "EBIT with same annual/year/currency overrides",
            "estimate_revenue": "BEST_SALES; BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY; EQY_FUND_CRNCY=USD",
            "estimate_ebit": "BEST_EBIT with same fiscal-period/currency overrides",
        },
    }
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in payload.items() if key not in {"companies", "actual_2024", "actual_2025", "actual_2026", "estimates"}}, indent=2))


if __name__ == "__main__":
    main()
