#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch Bloomberg data for the AI re-rating / revenue-acceleration exhibit.

Coverage: MSFT, GOOG, META, AMZN, NVDA, AVGO, TSM, ASML (US listings).
  - Blended-forward P/E (BEST_PE_RATIO), weekly since 2025-07-01
  - PX_LAST weekly since 2025-07-01
  - BEST_SALES for CY2026/2027/2028 (1CY/2CY/3CY overrides), weekly since 2025-12-01
    MSFT is June-fiscal: calendar years are built from four quarterly BEst estimates
    (same roll convention as build_hyperscaler_revisions.py).
  - Basis checks: bdp nCY vs nFY per name so fiscal-offset names are labeled honestly.

Output (feature-script compliant): _wiki/_data/ai_rerating_2026.json
Run: py _wiki/_tools/build_ai_rerating.py
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BBG_DIR = Path(r"E:\bloomberg_api")
if str(BBG_DIR) not in sys.path:
    sys.path.insert(0, str(BBG_DIR))

from bloomberg import bdh, bdp  # noqa: E402

OUT = ROOT / "_wiki" / "_data" / "ai_rerating_2026.json"

ASOF_DATE = dt.date.today()
ASOF = ASOF_DATE.strftime("%Y%m%d")
PE_START = dt.date(2025, 7, 1)
SALES_START = dt.date(2025, 12, 1)

NAMES = {
    "MSFT": "MSFT US Equity",
    "GOOG": "GOOG US Equity",
    "META": "META US Equity",
    "AMZN": "AMZN US Equity",
    "NVDA": "NVDA US Equity",
    "AVGO": "AVGO US Equity",
    "TSM": "TSM US Equity",
    "ASML": "ASML US Equity",
}
BBG_TO_TK = {v: k for k, v in NAMES.items()}
SALES_DIRECT = [t for t in NAMES if t != "MSFT"]
CY_OVERRIDES = {2026: "1CY", 2027: "2CY", 2028: "3CY"}

# Same convention as build_hyperscaler_revisions.py (cutover day after report).
MSFT_ROLLS = [
    {"effective": dt.date(2026, 1, 29), "cy26_start_fq": 1, "cy27_start_fq": 5, "cy28_start_fq": 9},
    {"effective": dt.date(2026, 4, 30), "cy26_start_fq": 0, "cy27_start_fq": 4, "cy28_start_fq": 8},
    {"effective": dt.date(2026, 7, 30), "cy26_start_fq": -1, "cy27_start_fq": 3, "cy28_start_fq": 7},
]


def finite(v: Any) -> float | None:
    try:
        out = float(v)
        return out if math.isfinite(out) else None
    except (TypeError, ValueError):
        return None


def bbg_call(fn: Callable[..., pd.DataFrame], *args: Any, **kwargs: Any) -> pd.DataFrame:
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        msg = str(exc).lower()
        if "500" not in msg and "503" not in msg and "connection test failed" not in msg and "connect" not in msg:
            raise
        os.environ["BBG_LOCAL_ONLY"] = "1"
        return fn(*args, **kwargs)


def rows_by_key(df: pd.DataFrame, field: str) -> dict[str, list[tuple[str, float]]]:
    out: dict[str, list[tuple[str, float]]] = defaultdict(list)
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        if str(row.get("field")) != field:
            continue
        tk = BBG_TO_TK.get(str(row.get("ticker")))
        val = finite(row.get("value"))
        if not tk or val is None:
            continue
        out[tk].append((str(row.get("date"))[:10], val))
    for k in out:
        out[k] = sorted(out[k])
    return out


def snap_map(df: pd.DataFrame, field: str) -> dict[str, float]:
    out: dict[str, float] = {}
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        if str(row.get("field")) != field:
            continue
        tk = BBG_TO_TK.get(str(row.get("ticker")))
        val = finite(row.get("value"))
        if tk and val is not None:
            out[tk] = val
    return out


def series_value(rows: list[tuple[str, float]], target: dt.date, max_stale_days: int = 42) -> float | None:
    prior = [(d, v) for d, v in rows if dt.date.fromisoformat(d) <= target]
    if not prior:
        return None
    d, v = prior[-1]
    if (target - dt.date.fromisoformat(d)).days > max_stale_days:
        return None
    return v


def msft_start_fq(year: int, date: dt.date) -> int:
    start = {2026: 2, 2027: 6, 2028: 10}[year]
    for roll in MSFT_ROLLS:
        if date >= roll["effective"]:
            start = roll[f"cy{year - 2000}_start_fq"]
    return start


def weekly_dates(start: dt.date) -> list[dt.date]:
    dates = [d.date() for d in pd.date_range(start, ASOF_DATE, freq="W-FRI")]
    if ASOF_DATE not in dates:
        dates.append(ASOF_DATE)
    return sorted(set(dates))


def main() -> None:
    all_bbg = list(NAMES.values())

    # ---- P/E and price, weekly ----
    pe_hist = bbg_call(bdh, all_bbg, ["BEST_PE_RATIO", "PX_LAST"], PE_START.strftime("%Y%m%d"), ASOF,
                       periodicitySelection="WEEKLY")
    pe_rows = rows_by_key(pe_hist, "BEST_PE_RATIO")
    px_rows = rows_by_key(pe_hist, "PX_LAST")
    pe_snap_df = bbg_call(bdp, all_bbg, ["BEST_PE_RATIO", "PX_LAST"])
    pe_now = snap_map(pe_snap_df, "BEST_PE_RATIO")
    px_now = snap_map(pe_snap_df, "PX_LAST")

    # ---- BEST_SALES: direct CY names, weekly per override year ----
    direct_bbg = [NAMES[t] for t in SALES_DIRECT]
    sales_hist: dict[int, dict[str, list[tuple[str, float]]]] = {}
    sales_now: dict[int, dict[str, float]] = {}
    fy_now: dict[int, dict[str, float]] = {}
    for year, ov in CY_OVERRIDES.items():
        hist = bbg_call(bdh, direct_bbg, ["BEST_SALES"], SALES_START.strftime("%Y%m%d"), ASOF,
                        periodicitySelection="WEEKLY", BEST_FPERIOD_OVERRIDE=ov)
        sales_hist[year] = rows_by_key(hist, "BEST_SALES")
        snap = bbg_call(bdp, direct_bbg, ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=ov)
        sales_now[year] = snap_map(snap, "BEST_SALES")
        fy = bbg_call(bdp, direct_bbg, ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=f"{year - 2025}FY")
        fy_now[year] = snap_map(fy, "BEST_SALES")

    # ---- MSFT quarterly sales for calendarization ----
    msft_bbg = [NAMES["MSFT"]]
    msft_q_hist: dict[int, list[tuple[str, float]]] = {}
    msft_q_now: dict[int, float | None] = {}
    for fq in range(1, 14):
        hist = bbg_call(bdh, msft_bbg, ["BEST_SALES"], SALES_START.strftime("%Y%m%d"), ASOF,
                        periodicitySelection="WEEKLY", BEST_FPERIOD_OVERRIDE=f"{fq}FQ")
        msft_q_hist[fq] = rows_by_key(hist, "BEST_SALES").get("MSFT", [])
        snap = bbg_call(bdp, msft_bbg, ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=f"{fq}FQ")
        msft_q_now[fq] = snap_map(snap, "BEST_SALES").get("MSFT")

    # MSFT CY25 actual-ish base: sum of FQ that are now reported is not available via
    # BEst history once reported; use bdp on -2FQ..? Keep it simple: CY26 estimate from
    # quarters (Q3FY26+Q4FY26 actuals fold into BEst history until replaced). For growth
    # rates we only need CY26E/27E/28E consistently built the same way.
    def msft_cy(year: int, date: dt.date | None) -> float | None:
        start = msft_start_fq(year, date or ASOF_DATE)
        if start < 1:
            return None
        vals = []
        for fq in range(start, start + 4):
            v = msft_q_now.get(fq) if date is None else series_value(msft_q_hist.get(fq, []), date)
            vals.append(v)
        return sum(vals) if all(v is not None for v in vals) else None

    # ---- assemble weekly history ----
    dates = weekly_dates(SALES_START)
    sales_records: list[dict[str, Any]] = []
    for date in dates:
        for year in CY_OVERRIDES:
            for tk in NAMES:
                if tk == "MSFT":
                    val = msft_cy(year, date)
                    basis = "calendarized from BEst fiscal quarters"
                else:
                    val = series_value(sales_hist[year].get(tk, []), date)
                    basis = CY_OVERRIDES[year]
                if date == ASOF_DATE:
                    if tk == "MSFT":
                        val = msft_cy(year, None) or val
                    else:
                        val = sales_now[year].get(tk, val)
                sales_records.append({
                    "date": date.isoformat(), "ticker": tk, "year": year,
                    "sales_mm": round(val, 1) if val is not None else None, "basis": basis,
                })

    pe_records: list[dict[str, Any]] = []
    for tk in NAMES:
        for d, v in pe_rows.get(tk, []):
            pe_records.append({"date": d, "ticker": tk, "best_pe": round(v, 3)})
    px_records: list[dict[str, Any]] = []
    for tk in NAMES:
        for d, v in px_rows.get(tk, []):
            px_records.append({"date": d, "ticker": tk, "px": round(v, 3)})

    # ---- CY vs FY alignment check (fiscal-offset names flagged, not fixed) ----
    checks = []
    for year in CY_OVERRIDES:
        for tk in SALES_DIRECT:
            cy = sales_now[year].get(tk)
            fy = fy_now[year].get(tk)
            diff = abs(cy / fy - 1.0) if cy is not None and fy not in (None, 0) else None
            checks.append({
                "ticker": tk, "year": year,
                "cy_snapshot_mm": cy, "fy_snapshot_mm": fy,
                "cy_vs_fy_diff": round(diff, 4) if diff is not None else None,
                "note": "large diff expected for NVDA (Jan FY) and AVGO (Oct FY): nCY is true calendar-year consensus",
            })

    payload = {
        "meta": {
            "asof": ASOF_DATE.isoformat(),
            "built_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "source": "Bloomberg BEst consensus via Capstone wrapper / local Desktop API fallback",
            "pe_field": "BEST_PE_RATIO (blended forward)",
            "sales_field": "BEST_SALES with 1CY/2CY/3CY calendar overrides; MSFT calendarized from fiscal quarters",
            "pe_history_start": PE_START.isoformat(),
            "sales_history_start": SALES_START.isoformat(),
            "sales_units": "millions, listing currency (growth rates currency-invariant)",
        },
        "pe": pe_records,
        "px": px_records,
        "pe_now": {tk: round(v, 3) for tk, v in pe_now.items()},
        "px_now": {tk: round(v, 3) for tk, v in px_now.items()},
        "sales": sales_records,
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    n_pe = len(pe_records)
    n_sales = sum(1 for r in sales_records if r["sales_mm"] is not None)
    print(f"wrote {OUT} — {n_pe} P/E rows, {n_sales} populated sales rows, asof {ASOF_DATE}")


if __name__ == "__main__":
    main()
