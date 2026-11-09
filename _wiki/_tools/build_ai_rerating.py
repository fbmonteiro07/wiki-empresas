#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch Bloomberg data for the AI re-rating / revenue-acceleration exhibit.

Coverage: MSFT, GOOG, META, AMZN, NVDA, AVGO, TSM, ASML (US listings).
  - Blended-forward P/E (BEST_PE_RATIO), weekly since 2025-07-01
  - PX_LAST weekly since 2025-07-01
  - BEST_SALES for CY2026/2027/2028 with ABSOLUTE calendar overrides 2026BC/2027BC/
    2028BC for all 8 names, weekly since 2025-12-01. The latest point is the bdp
    snapshot (folds in reported actuals); history is bdh.
  - Basis checks per name/year: <yr>BC vs relative nCY vs anchored nFY, and the
    snapshot-vs-last-history gap.

Why absolute overrides (verified 2026-11-09): relative nCY/nFQ in a historical
request resolve against TODAY's period for every past date, and for non-Dec FYE
names bdh nCY falls back to the fiscal year (MSFT bdh 1CY = 1FY $395bn vs bdp 1CY
$356bn; AVGO bdh 1CY = 1FY $105.9bn vs bdp 1CY $123.7bn). The pre-2026-11-09
builder therefore stitched fiscal-year history to a calendarized last point for
AVGO, and its MSFT nFQ roll table shifted pre-roll history (and lost CY2026 after
the July roll). <yr>BC == 1CY/2CY/3CY to the cent for the Dec-FYE names, equals
the sum of the four fixed MSFT fiscal quarters at every weekly point, and is a
true day-prorated calendarization for NVDA (Jan FY) and AVGO (Oct FY).

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
CY_OVERRIDES = {2026: "2026BC", 2027: "2027BC", 2028: "2028BC"}


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

    # ---- BEST_SALES: absolute calendar years for every name ----
    sales_hist: dict[int, dict[str, list[tuple[str, float]]]] = {}
    sales_now: dict[int, dict[str, float]] = {}
    ncy_now: dict[int, dict[str, float]] = {}
    for year, ov in CY_OVERRIDES.items():
        hist = bbg_call(bdh, all_bbg, ["BEST_SALES"], SALES_START.strftime("%Y%m%d"), ASOF,
                        periodicitySelection="WEEKLY", BEST_FPERIOD_OVERRIDE=ov)
        sales_hist[year] = rows_by_key(hist, "BEST_SALES")
        snap = bbg_call(bdp, all_bbg, ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=ov)
        sales_now[year] = snap_map(snap, "BEST_SALES")
        n_cy = year - ASOF_DATE.year + 1
        if n_cy >= 1:
            rel = bbg_call(bdp, all_bbg, ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=f"{n_cy}CY")
            ncy_now[year] = snap_map(rel, "BEST_SALES")
        else:
            ncy_now[year] = {}

    # Fiscal-year cross-check, anchored on the period 1FY points at today. A fiscal
    # year is mapped to the calendar year holding most of its months.
    fy1_end: dict[str, dt.date] = {}
    anchor = bbg_call(bdp, all_bbg, ["BEST_PERIOD_END_DATE"], BEST_FPERIOD_OVERRIDE="1FY")
    for _, row in anchor.iterrows():
        tk = BBG_TO_TK.get(str(row.get("ticker")))
        try:
            fy1_end[tk] = dt.date.fromisoformat(str(row.get("value"))[:10])
        except ValueError:
            continue
    fy_now: dict[tuple[str, int], tuple[str, float | None]] = {}
    for tk, end in fy1_end.items():
        fy1_cy = end.year if end.month >= 7 else end.year - 1
        for year in CY_OVERRIDES:
            n_fy = year - fy1_cy + 1
            if n_fy < 1:
                continue
            fy = bbg_call(bdp, [NAMES[tk]], ["BEST_SALES"], BEST_FPERIOD_OVERRIDE=f"{n_fy}FY")
            fy_now[(tk, year)] = (f"{n_fy}FY", snap_map(fy, "BEST_SALES").get(tk))

    # ---- assemble weekly history ----
    dates = weekly_dates(SALES_START)
    sales_records: list[dict[str, Any]] = []
    last_hist: dict[tuple[str, int], float | None] = {}
    for date in dates:
        for year, ov in CY_OVERRIDES.items():
            for tk in NAMES:
                val = series_value(sales_hist[year].get(tk, []), date)
                basis = ov
                if date == ASOF_DATE:
                    last_hist[(tk, year)] = val
                    if tk in sales_now[year]:
                        val = sales_now[year][tk]
                        basis = f"{ov} snapshot (reported actuals folded in)"
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

    # ---- basis checks ----
    checks = []
    for year in CY_OVERRIDES:
        for tk in NAMES:
            bc = sales_now[year].get(tk)
            ncy = ncy_now[year].get(tk)
            fy_label, fy = fy_now.get((tk, year), (None, None))
            hist_last = last_hist.get((tk, year))
            ratio = lambda a, c: round(a / c - 1.0, 4) if a is not None and c not in (None, 0) else None
            checks.append({
                "ticker": tk, "year": year,
                "bc_snapshot_mm": bc, "ncy_snapshot_mm": ncy,
                "fy_label": fy_label, "fy_snapshot_mm": fy,
                "bc_vs_ncy_diff": ratio(bc, ncy), "bc_vs_fy_diff": ratio(bc, fy),
                "last_history_mm": hist_last, "snapshot_vs_history_diff": ratio(bc, hist_last),
                "note": ("Dec-FYE names: BC == nCY == FY. NVDA nCY = fiscal year (ends Jan, ~1-month offset); "
                         "AVGO/MSFT nCY differ from BC (and fall back to FY in bdh history). "
                         "snapshot_vs_history_diff: bdp folds reported actuals into a part-reported year, "
                         "bdh history keeps the pre-print consensus for reported quarters."),
            })

    payload = {
        "meta": {
            "asof": ASOF_DATE.isoformat(),
            "built_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "source": "Bloomberg BEst consensus via Capstone wrapper / local Desktop API fallback",
            "pe_field": "BEST_PE_RATIO (blended forward)",
            "sales_field": "BEST_SALES with absolute calendar overrides 2026BC/2027BC/2028BC for all names (Bloomberg day-prorated quarter calendarization); history = bdh weekly, latest point = bdp snapshot",
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
