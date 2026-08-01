#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Bloomberg consensus-revision data, workbook, and dashboard.

Coverage: MSFT, META, GOOG, AMZN; calendar years 2027 and 2028;
metrics: capex, EBITDA, and EPS.

The script uses the desk wrapper in E:\\bloomberg_api. It first tries the normal
HTTP wrapper and automatically retries through the local Bloomberg Desktop API
when the internal service returns HTTP 503.

Outputs (feature-script compliant; no wiki pages are modified):
  _wiki/_data/hyperscaler_revisions_2027_2028.json
  _wiki/_dashboards/hyperscaler-revisions-2027-2028.xlsx
  _wiki/_dashboards/hyperscaler-revisions-2027-2028.html

Run:
  py _wiki/_tools/build_hyperscaler_revisions.py
"""

from __future__ import annotations

import datetime as dt
import html
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import pandas as pd
import xlsxwriter

ROOT = Path(__file__).resolve().parents[2]
BBG_DIR = Path(r"E:\bloomberg_api")
if str(BBG_DIR) not in sys.path:
    sys.path.insert(0, str(BBG_DIR))

from bloomberg import bdh, bdp  # noqa: E402

DATA_OUT = ROOT / "_wiki" / "_data" / "hyperscaler_revisions_2027_2028.json"
DASH_OUT = ROOT / "_wiki" / "_dashboards" / "hyperscaler-revisions-2027-2028.html"
XLSX_OUT = ROOT / "_wiki" / "_dashboards" / "hyperscaler-revisions-2027-2028.xlsx"

ASOF_DATE = dt.date.today()
ASOF = ASOF_DATE.strftime("%Y%m%d")
HIST_START_DATE = dt.date(2025, 12, 1)
HIST_START = HIST_START_DATE.strftime("%Y%m%d")
DISPLAY_START = dt.date(2026, 1, 2)

COMPANIES = {
    "MSFT": {"name": "Microsoft", "bbg": "MSFT US Equity", "fy_end": 6},
    "META": {"name": "Meta", "bbg": "META US Equity", "fy_end": 12},
    "GOOG": {"name": "Alphabet", "bbg": "GOOG US Equity", "fy_end": 12},
    "AMZN": {"name": "Amazon", "bbg": "AMZN US Equity", "fy_end": 12},
}
TICKER_FROM_BBG = {v["bbg"]: k for k, v in COMPANIES.items()}

METRICS = {
    "capex": {
        "field": "BEST_CAPEX",
        "label": "Capex",
        "unit": "USD bn",
        "scale": 1000.0,
        "sign": -1.0,
        "format": "$#,##0.0",
    },
    "ebitda": {
        "field": "BEST_EBITDA",
        "label": "EBITDA",
        "unit": "USD bn",
        "scale": 1000.0,
        "sign": 1.0,
        "format": "$#,##0.0",
    },
    "cash_proxy": {
        "field": None,
        "label": "EBITDA ? Capex",
        "unit": "USD bn",
        "scale": 1000.0,
        "sign": 1.0,
        "format": "$#,##0.0",
    },
    "eps": {
        "field": "BEST_EPS",
        "label": "EPS",
        "unit": "USD/share",
        "scale": 1.0,
        "sign": 1.0,
        "format": "$0.00",
    },
}
SOURCE_METRICS = ("capex", "ebitda", "eps")
FIELD_TO_METRIC = {v["field"]: k for k, v in METRICS.items() if v["field"]}
YEARS = {2027: "2CY", 2028: "3CY"}

# MSFT reports on a June fiscal year. HistoricalDataRequest treats nCY as nFY
# for this security, and BEST_EPS also falls back to FY even in a reference
# request. Fixed calendar years are therefore built from four quarterly BEst
# estimates. Cutovers are the day after the sourced earnings release/call.
MSFT_ROLLS = [
    {
        "effective": dt.date(2026, 1, 29),
        "reported": dt.date(2026, 1, 28),
        "cy27_start_fq": 5,
        "cy28_start_fq": 9,
        "source": "MSFT Q2 FY26 earnings call / 10-Q, 2026-01-28",
        "path": "MSFT/transcripts/MSFT_Q2-FY26-earnings_2026-01-28.md",
    },
    {
        "effective": dt.date(2026, 4, 30),
        "reported": dt.date(2026, 4, 29),
        "cy27_start_fq": 4,
        "cy28_start_fq": 8,
        "source": "MSFT Q3 FY26 earnings call / 10-Q, 2026-04-29",
        "path": "MSFT/transcripts/MSFT_Q3-FY26-earnings_2026-04-29.md",
    },
    {
        "effective": dt.date(2026, 7, 30),
        "reported": dt.date(2026, 7, 29),
        "cy27_start_fq": 3,
        "cy28_start_fq": 7,
        "source": "MSFT Q4 FY26 earnings call / FY26 10-K, 2026-07-29",
        "path": "MSFT/transcripts/MSFT_Q4-FY26-earnings_2026-07-29.md",
    },
]


def finite(value: Any) -> float | None:
    try:
        out = float(value)
        return out if math.isfinite(out) else None
    except (TypeError, ValueError):
        return None


def bbg_call(fn: Callable[..., pd.DataFrame], *args: Any, **kwargs: Any) -> pd.DataFrame:
    """Call the desk wrapper and retry locally if its HTTP service is down."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        msg = str(exc).lower()
        if "500" not in msg and "503" not in msg and "connection test failed" not in msg and "connect" not in msg:
            raise
        os.environ["BBG_LOCAL_ONLY"] = "1"
        return fn(*args, **kwargs)


def weekly_dates() -> list[dt.date]:
    dates = [d.date() for d in pd.date_range(DISPLAY_START, ASOF_DATE, freq="W-FRI")]
    if ASOF_DATE >= DISPLAY_START and ASOF_DATE not in dates:
        dates.append(ASOF_DATE)
    return sorted(set(dates))


def metric_value(metric: str, raw: Any) -> float | None:
    value = finite(raw)
    return None if value is None else value * METRICS[metric]["sign"]


def display_value(metric: str, raw_value: float | None) -> float | None:
    if raw_value is None:
        return None
    return raw_value / METRICS[metric]["scale"]


def records_by_key(df: pd.DataFrame) -> dict[tuple[str, str], list[tuple[dt.date, float]]]:
    out: dict[tuple[str, str], list[tuple[dt.date, float]]] = defaultdict(list)
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        ticker = TICKER_FROM_BBG.get(str(row.get("ticker")))
        metric = FIELD_TO_METRIC.get(str(row.get("field")))
        value = metric_value(metric, row.get("value")) if metric else None
        if not ticker or not metric or value is None:
            continue
        try:
            date = dt.date.fromisoformat(str(row.get("date"))[:10])
        except ValueError:
            continue
        out[(ticker, metric)].append((date, value))
    for key in out:
        out[key] = sorted(out[key])
    return out


def series_value(
    rows: list[tuple[dt.date, float]], target: dt.date, max_stale_days: int = 42
) -> float | None:
    prior = [(date, value) for date, value in rows if date <= target]
    if not prior:
        return None
    date, value = prior[-1]
    if (target - date).days > max_stale_days:
        return None
    return value


def snapshot_map(df: pd.DataFrame) -> dict[tuple[str, str], float]:
    out: dict[tuple[str, str], float] = {}
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        ticker = TICKER_FROM_BBG.get(str(row.get("ticker")))
        metric = FIELD_TO_METRIC.get(str(row.get("field")))
        value = metric_value(metric, row.get("value")) if metric else None
        if ticker and metric and value is not None:
            out[(ticker, metric)] = value
    return out


def msft_start_fq(year: int, date: dt.date) -> int:
    start = 6 if year == 2027 else 10
    for roll in MSFT_ROLLS:
        if date >= roll["effective"]:
            start = roll["cy27_start_fq"] if year == 2027 else roll["cy28_start_fq"]
    return start


def pct_change(current: float | None, base: float | None) -> float | None:
    if current is None or base in (None, 0):
        return None
    return current / base - 1.0


def fetch_data() -> dict[str, Any]:
    fields = [METRICS[metric]["field"] for metric in SOURCE_METRICS]
    direct_bbg = [COMPANIES[t]["bbg"] for t in ("META", "GOOG", "AMZN")]
    dates = weekly_dates()

    current: dict[tuple[str, int, str], float] = {}
    direct_snapshots: dict[int, dict[tuple[str, str], float]] = {}
    fy_snapshots: dict[int, dict[tuple[str, str], float]] = {}
    raw_direct_history: dict[int, dict[tuple[str, str], list[tuple[dt.date, float]]]] = {}

    for year, override in YEARS.items():
        snap = bbg_call(
            bdp,
            [c["bbg"] for c in COMPANIES.values()],
            fields,
            BEST_FPERIOD_OVERRIDE=override,
        )
        direct_snapshots[year] = snapshot_map(snap)

        fy = bbg_call(
            bdp,
            direct_bbg,
            fields,
            BEST_FPERIOD_OVERRIDE=f"{year - 2025}FY",
        )
        fy_snapshots[year] = snapshot_map(fy)

        hist = bbg_call(
            bdh,
            direct_bbg,
            fields,
            HIST_START,
            ASOF,
            periodicitySelection="WEEKLY",
            BEST_FPERIOD_OVERRIDE=override,
        )
        raw_direct_history[year] = records_by_key(hist)
        for ticker in ("META", "GOOG", "AMZN"):
            for metric in SOURCE_METRICS:
                value = direct_snapshots[year].get((ticker, metric))
                if value is not None:
                    current[(ticker, year, metric)] = value

    # Pull MSFT quarterly histories far enough to calendarize CY28 before and
    # after all three 2026 reporting rolls.
    msft_bbg = [COMPANIES["MSFT"]["bbg"]]
    msft_q_history: dict[int, dict[tuple[str, str], list[tuple[dt.date, float]]]] = {}
    msft_q_current: dict[int, dict[tuple[str, str], float]] = {}
    for fq in range(3, 14):
        hist = bbg_call(
            bdh,
            msft_bbg,
            fields,
            HIST_START,
            ASOF,
            periodicitySelection="WEEKLY",
            BEST_FPERIOD_OVERRIDE=f"{fq}FQ",
        )
        msft_q_history[fq] = records_by_key(hist)
        snap = bbg_call(
            bdp,
            msft_bbg,
            fields,
            BEST_FPERIOD_OVERRIDE=f"{fq}FQ",
        )
        msft_q_current[fq] = snapshot_map(snap)

    for year in YEARS:
        start_fq = msft_start_fq(year, ASOF_DATE)
        for metric in SOURCE_METRICS:
            values = [msft_q_current[fq].get(("MSFT", metric)) for fq in range(start_fq, start_fq + 4)]
            if all(value is not None for value in values):
                current[("MSFT", year, metric)] = sum(values)  # type: ignore[arg-type]

    history: list[dict[str, Any]] = []
    for date in dates:
        for ticker in COMPANIES:
            for year in YEARS:
                for metric in SOURCE_METRICS:
                    value: float | None
                    basis: str
                    if ticker == "MSFT":
                        start_fq = msft_start_fq(year, date)
                        quarters = []
                        for fq in range(start_fq, start_fq + 4):
                            rows = msft_q_history.get(fq, {}).get(("MSFT", metric), [])
                            quarters.append(series_value(rows, date))
                        value = sum(quarters) if all(v is not None for v in quarters) else None  # type: ignore[arg-type]
                        basis = f"calendarized from {start_fq}FQ-{start_fq + 3}FQ"
                    else:
                        rows = raw_direct_history[year].get((ticker, metric), [])
                        value = series_value(rows, date)
                        basis = YEARS[year]

                    if date == ASOF_DATE:
                        value = current.get((ticker, year, metric), value)
                    history.append(
                        {
                            "date": date.isoformat(),
                            "ticker": ticker,
                            "company": COMPANIES[ticker]["name"],
                            "year": year,
                            "metric": metric,
                            "metric_label": METRICS[metric]["label"],
                            "unit": METRICS[metric]["unit"],
                            "value_raw": round(value, 6) if value is not None else None,
                            "value": round(display_value(metric, value), 6) if value is not None else None,
                            "basis": basis,
                            "source": "Bloomberg BEst via Capstone wrapper",
                        }
                    )

    # MSFT CY2027 EBITDA needs a roll-adjusted history. The raw quarterly BEst
    # sums are correct at every date, but the contributor set changes sharply
    # when the nFQ window rolls after earnings (for example 6/6/6/3 estimates
    # before the January roll versus 7/7/7/7 after it). Backward chain-link the
    # contiguous nFQ regimes so the latest absolute BEst level remains untouched
    # while report-date contributor-set discontinuities do not reverse the
    # underlying within-regime revision trend. Preserve every raw value.
    msft_ebitda_roll_meta: dict[str, Any] = {}
    msft_ebitda_rows = sorted(
        [
            row
            for row in history
            if row["ticker"] == "MSFT" and row["year"] == 2027 and row["metric"] == "ebitda"
        ],
        key=lambda row: row["date"],
    )
    valid_msft_ebitda = [row for row in msft_ebitda_rows if row["value_raw"] is not None]
    segments: list[tuple[str, list[dict[str, Any]]]] = []
    for row in valid_msft_ebitda:
        if not segments or segments[-1][0] != row["basis"]:
            segments.append((row["basis"], []))
        segments[-1][1].append(row)
    if segments:
        offsets: dict[str, float] = {segments[-1][0]: 0.0}
        for idx in range(len(segments) - 2, -1, -1):
            basis, segment = segments[idx]
            next_basis, next_segment = segments[idx + 1]
            offsets[basis] = (
                next_segment[0]["value_raw"]
                + offsets[next_basis]
                - segment[-1]["value_raw"]
            )
        raw_first = valid_msft_ebitda[0]["value"]
        for row in msft_ebitda_rows:
            basis = row["basis"]
            if basis not in offsets:
                continue
            adjustment_raw = offsets[basis]
            row["raw_value_raw"] = row["value_raw"]
            row["raw_value"] = row["value"]
            row["roll_adjustment_raw"] = round(adjustment_raw, 6)
            row["roll_adjustment"] = round(display_value("ebitda", adjustment_raw), 6)
            if row["value_raw"] is not None:
                row["value_raw"] = round(row["value_raw"] + adjustment_raw, 6)
                row["value"] = round(display_value("ebitda", row["value_raw"]), 6)
            row["basis"] = basis + "; backward chain-linked at earnings rolls"
            row["source"] += "; roll-adjusted for nFQ contributor-set changes"
        adjusted_first = next(row["value"] for row in msft_ebitda_rows if row["value"] is not None)
        current_value = next(row["value"] for row in reversed(msft_ebitda_rows) if row["value"] is not None)
        msft_ebitda_roll_meta = {
            "method": "Backward additive chain-link across MSFT earnings-roll nFQ regimes; latest absolute BEst level anchored unchanged.",
            "raw_first": raw_first,
            "adjusted_first": adjusted_first,
            "current": current_value,
            "adjusted_change": round(current_value - adjusted_first, 6),
            "segment_adjustments": {basis: round(display_value("ebitda", offset), 6) for basis, offset in offsets.items()},
        }

    # Apply the same contributor-set normalization to MSFT CY2027 EPS. This
    # preserves the latest absolute quarterly-sum BEst consensus while making
    # the pre/post-earnings history comparable and retaining every raw value.
    msft_eps_roll_meta: dict[str, Any] = {}
    msft_eps_rows = sorted(
        [
            row
            for row in history
            if row["ticker"] == "MSFT" and row["year"] == 2027 and row["metric"] == "eps"
        ],
        key=lambda row: row["date"],
    )
    valid_msft_eps = [row for row in msft_eps_rows if row["value_raw"] is not None]
    eps_segments: list[tuple[str, list[dict[str, Any]]]] = []
    for row in valid_msft_eps:
        if not eps_segments or eps_segments[-1][0] != row["basis"]:
            eps_segments.append((row["basis"], []))
        eps_segments[-1][1].append(row)
    if eps_segments:
        eps_offsets: dict[str, float] = {eps_segments[-1][0]: 0.0}
        for idx in range(len(eps_segments) - 2, -1, -1):
            basis, segment = eps_segments[idx]
            next_basis, next_segment = eps_segments[idx + 1]
            eps_offsets[basis] = (
                next_segment[0]["value_raw"]
                + eps_offsets[next_basis]
                - segment[-1]["value_raw"]
            )
        raw_first = valid_msft_eps[0]["value"]
        for row in msft_eps_rows:
            basis = row["basis"]
            if basis not in eps_offsets:
                continue
            adjustment_raw = eps_offsets[basis]
            row["raw_value_raw"] = row["value_raw"]
            row["raw_value"] = row["value"]
            row["roll_adjustment_raw"] = round(adjustment_raw, 6)
            row["roll_adjustment"] = round(display_value("eps", adjustment_raw), 6)
            if row["value_raw"] is not None:
                row["value_raw"] = round(row["value_raw"] + adjustment_raw, 6)
                row["value"] = round(display_value("eps", row["value_raw"]), 6)
            row["basis"] = basis + "; backward chain-linked at earnings rolls"
            row["source"] += "; roll-adjusted for nFQ contributor-set changes"
        adjusted_first = next(row["value"] for row in msft_eps_rows if row["value"] is not None)
        current_value = next(row["value"] for row in reversed(msft_eps_rows) if row["value"] is not None)
        msft_eps_roll_meta = {
            "method": "Backward additive chain-link across MSFT earnings-roll nFQ regimes; latest absolute BEst level anchored unchanged.",
            "raw_first": raw_first,
            "adjusted_first": adjusted_first,
            "current": current_value,
            "adjusted_change": round(current_value - adjusted_first, 6),
            "segment_adjustments": {basis: round(display_value("eps", offset), 6) for basis, offset in eps_offsets.items()},
        }
    # EBITDA minus positive-spend capex: a deliberately simple, pre-interest,
    # pre-tax proxy. It is not company-reported FCF and excludes working capital,
    # cash taxes, interest, leases outside capex, and other cash items.
    source_history = {
        (row["date"], row["ticker"], row["year"], row["metric"]): row
        for row in history
    }
    for date in dates:
        for ticker in COMPANIES:
            for year in YEARS:
                ebitda = source_history.get((date.isoformat(), ticker, year, "ebitda"))
                capex = source_history.get((date.isoformat(), ticker, year, "capex"))
                raw_value = (
                    ebitda["value_raw"] - capex["value_raw"]
                    if ebitda and capex and ebitda["value_raw"] is not None and capex["value_raw"] is not None
                    else None
                )
                history.append(
                    {
                        "date": date.isoformat(),
                        "ticker": ticker,
                        "company": COMPANIES[ticker]["name"],
                        "year": year,
                        "metric": "cash_proxy",
                        "metric_label": METRICS["cash_proxy"]["label"],
                        "unit": METRICS["cash_proxy"]["unit"],
                        "value_raw": round(raw_value, 6) if raw_value is not None else None,
                        "value": round(display_value("cash_proxy", raw_value), 6) if raw_value is not None else None,
                        "basis": f"derived from {ebitda['basis']}" if ebitda else "derived",
                        "source": "Calculated: Bloomberg BEST_EBITDA minus positive-spend BEST_CAPEX",
                    }
                )
    # Rebase every series to its first available observation in 2026.
    groups: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in history:
        groups[(row["ticker"], row["year"], row["metric"])].append(row)
    for rows in groups.values():
        first = next((r for r in rows if r["value"] is not None), None)
        base = first["value"] if first else None
        for row in rows:
            row["change_from_first"] = (
                round(row["value"] - base, 6)
                if row["value"] is not None and base is not None
                else None
            )
            row["revision_from_first_pct"] = (
                round(pct_change(row["value"], base), 8)
                if row["value"] is not None and base not in (None, 0)
                else None
            )

    summary: list[dict[str, Any]] = []
    target_1m = ASOF_DATE - dt.timedelta(days=30)
    target_3m = ASOF_DATE - dt.timedelta(days=90)
    for key, rows in groups.items():
        ticker, year, metric = key
        valid = [r for r in rows if r["value"] is not None]
        if not valid:
            continue
        current_row = valid[-1]

        def base_before(target: dt.date) -> dict[str, Any] | None:
            eligible = [r for r in valid if dt.date.fromisoformat(r["date"]) <= target]
            return eligible[-1] if eligible else None

        base_1m = base_before(target_1m)
        base_3m = base_before(target_3m)
        base_ytd = valid[0]
        row: dict[str, Any] = {
            "ticker": ticker,
            "company": COMPANIES[ticker]["name"],
            "year": year,
            "metric": metric,
            "metric_label": METRICS[metric]["label"],
            "unit": METRICS[metric]["unit"],
            "current": current_row["value"],
            "current_date": current_row["date"],
            "basis": current_row["basis"],
            "source": current_row["source"],
        }
        for label, base_row in (("1m", base_1m), ("3m", base_3m), ("ytd", base_ytd)):
            row[f"{label}_base"] = base_row["value"] if base_row else None
            row[f"{label}_base_date"] = base_row["date"] if base_row else None
            row[f"{label}_change"] = (
                round(row["current"] - base_row["value"], 6) if base_row else None
            )
            row[f"{label}_pct"] = (
                round(pct_change(row["current"], base_row["value"]), 8) if base_row else None
            )
        summary.append(row)

    order_t = {ticker: i for i, ticker in enumerate(COMPANIES)}
    order_m = {metric: i for i, metric in enumerate(METRICS)}
    summary.sort(key=lambda r: (order_t[r["ticker"]], r["year"], order_m[r["metric"]]))

    checks: list[dict[str, Any]] = []
    tolerance = 0.005
    for ticker in ("META", "GOOG", "AMZN"):
        for year in YEARS:
            for metric in SOURCE_METRICS:
                cy = direct_snapshots[year].get((ticker, metric))
                fy = fy_snapshots[year].get((ticker, metric))
                diff = abs(cy / fy - 1.0) if cy is not None and fy not in (None, 0) else None
                checks.append(
                    {
                        "check": "CY/FY alignment for December year-end",
                        "ticker": ticker,
                        "year": year,
                        "metric": metric,
                        "status": "PASS" if diff is not None and diff <= tolerance else "FAIL",
                        "detail": f"{YEARS[year]} vs {year - 2025}FY; difference {diff:.3%}" if diff is not None else "missing value",
                    }
                )

    for year in YEARS:
        for metric in ("capex", "ebitda"):
            native = direct_snapshots[year].get(("MSFT", metric))
            qsum = current.get(("MSFT", year, metric))
            diff = abs(qsum / native - 1.0) if qsum is not None and native not in (None, 0) else None
            checks.append(
                {
                    "check": "MSFT quarterly calendarization vs native CY",
                    "ticker": "MSFT",
                    "year": year,
                    "metric": metric,
                    "status": "PASS" if diff is not None and diff <= tolerance else "FAIL",
                    "detail": f"sum of four calendar quarters vs {YEARS[year]}; difference {diff:.3%}" if diff is not None else "missing value",
                }
            )
        checks.append(
            {
                "check": "MSFT EPS calendar basis",
                "ticker": "MSFT",
                "year": year,
                "metric": "eps",
                "status": "PASS",
                "detail": "sum of four quarterly BEST_EPS estimates; native nCY BEST_EPS falls back to fiscal-year EPS and is intentionally not used",
            }
        )

    checks.append(
        {
            "check": "MSFT CY2027 EBITDA roll adjustment",
            "ticker": "MSFT",
            "year": 2027,
            "metric": "ebitda",
            "status": "PASS" if msft_ebitda_roll_meta else "FAIL",
            "detail": (
                f"latest BEst anchored at ${msft_ebitda_roll_meta['current']:.1f}bn; "
                f"roll-adjusted change ${msft_ebitda_roll_meta['adjusted_change']:+.1f}bn"
            ) if msft_ebitda_roll_meta else "adjustment metadata missing",
        }
    )

    checks.append(
        {
            "check": "MSFT CY2027 EPS roll adjustment",
            "ticker": "MSFT",
            "year": 2027,
            "metric": "eps",
            "status": "PASS" if msft_eps_roll_meta else "FAIL",
            "detail": (
                f"latest BEst anchored at ${msft_eps_roll_meta['current']:.3f}/share; "
                f"roll-adjusted change ${msft_eps_roll_meta['adjusted_change']:+.3f}/share"
            ) if msft_eps_roll_meta else "adjustment metadata missing",
        }
    )

    for key, rows in groups.items():
        coverage = sum(r["value"] is not None for r in rows) / len(rows) if rows else 0.0
        checks.append(
            {
                "check": "Weekly history coverage",
                "ticker": key[0],
                "year": key[1],
                "metric": key[2],
                "status": "PASS" if coverage >= 0.65 else "WARN",
                "detail": f"{coverage:.0%} of weekly dates populated; blanks retained when Bloomberg had no far-period consensus",
            }
        )

    payload = {
        "meta": {
            "asof": ASOF_DATE.isoformat(),
            "built_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "currency": "USD",
            "source": "Bloomberg BEst consensus via Capstone wrapper / local Bloomberg Desktop API fallback",
            "fields": {metric: METRICS[metric]["field"] for metric in SOURCE_METRICS},
            "derived": {"cash_proxy": "BEST_EBITDA ? positive-spend BEST_CAPEX"},
            "periods": {str(year): override for year, override in YEARS.items()},
            "history_start": DISPLAY_START.isoformat(),
            "methodology": (
                "META, GOOG and AMZN use Bloomberg calendar-year overrides directly. MSFT is June fiscal: "
                "fixed calendar years are the sum of four quarterly BEst estimates, with relative-quarter "
                "cutovers on the day after each company earnings release. MSFT CY2027 EBITDA and EPS histories are backward "
                "chain-linked across those nFQ regimes to neutralize contributor-set discontinuities while preserving "
                "the latest absolute BEst level; raw quarterly sums remain in the JSON and History sheet. Capex is sign-flipped to positive spend. "
                "EBITDA minus capex is a simple proxy, not reported FCF; it excludes working capital, cash taxes, "
                "interest, leases outside capex, and other cash items."
            ),
            "msft_ebitda_roll_adjustment": msft_ebitda_roll_meta,
            "msft_eps_roll_adjustment": msft_eps_roll_meta,
            "revision_windows": "1M=30 calendar days; 3M=90 calendar days; YTD=first available weekly observation on/after 2026-01-02.",
            "msft_rolls": [
                {**roll, "effective": roll["effective"].isoformat(), "reported": roll["reported"].isoformat()}
                for roll in MSFT_ROLLS
            ],
        },
        "summary": summary,
        "history": history,
        "checks": checks,
    }
    return payload


def write_workbook(payload: dict[str, Any]) -> None:
    XLSX_OUT.parent.mkdir(parents=True, exist_ok=True)
    wb = xlsxwriter.Workbook(XLSX_OUT)
    wb.set_properties(
        {
            "title": "Hyperscaler consensus revisions — CY2027/CY2028",
            "subject": "Bloomberg BEst capex, EBITDA, and EPS revisions",
            "author": "Capstone / Codex",
            "company": "Capstone",
            "comments": payload["meta"]["source"],
        }
    )

    navy = "#12263A"
    blue = "#2F75B5"
    light_blue = "#DDEBF7"
    light_orange = "#FCE4D6"
    pale = "#F4F7FA"
    border = "#D5DCE5"
    gray = "#5B6573"
    white = "#FFFFFF"
    green = "#E2F0D9"
    red = "#F4CCCC"

    title_fmt = wb.add_format({"bold": True, "font_size": 20, "font_color": white, "bg_color": navy, "align": "left", "valign": "vcenter"})
    subtitle_fmt = wb.add_format({"font_size": 10, "font_color": gray, "italic": True})
    section_fmt = wb.add_format({"bold": True, "font_size": 12, "font_color": navy, "bottom": 2, "bottom_color": blue})
    header_fmt = wb.add_format({"bold": True, "font_color": white, "bg_color": navy, "border": 1, "border_color": navy, "align": "center", "valign": "vcenter", "text_wrap": True})
    text_fmt = wb.add_format({"border": 1, "border_color": border, "valign": "vcenter"})
    text_wrap_fmt = wb.add_format({"border": 1, "border_color": border, "valign": "top", "text_wrap": True})
    date_fmt = wb.add_format({"border": 1, "border_color": border, "num_format": "yyyy-mm-dd", "align": "center"})
    pct_fmt = wb.add_format({"border": 1, "border_color": border, "num_format": "+0.0%;-0.0%;-", "align": "right"})
    pct_plain_fmt = wb.add_format({"border": 1, "border_color": border, "num_format": "0.0%", "align": "right"})
    bn_fmt = wb.add_format({"border": 1, "border_color": border, "num_format": "$#,##0.0", "align": "right"})
    eps_fmt = wb.add_format({"border": 1, "border_color": border, "num_format": "$0.00", "align": "right"})
    pass_fmt = wb.add_format({"border": 1, "border_color": border, "bg_color": green, "font_color": "#375623", "align": "center"})
    warn_fmt = wb.add_format({"border": 1, "border_color": border, "bg_color": light_orange, "font_color": "#9C5700", "align": "center"})
    fail_fmt = wb.add_format({"border": 1, "border_color": border, "bg_color": red, "font_color": "#9C0006", "align": "center"})
    note_fmt = wb.add_format({"font_color": gray, "font_size": 9, "text_wrap": True, "valign": "top"})
    link_fmt = wb.add_format({"font_color": blue, "underline": True})

    ws = wb.add_worksheet("Dashboard")
    ws.hide_gridlines(2)
    ws.set_tab_color(blue)
    ws.set_column("A:A", 12)
    ws.set_column("B:B", 9)
    ws.set_column("C:C", 11)
    ws.set_column("D:D", 13)
    ws.set_column("E:E", 12)
    ws.set_column("F:F", 11)
    ws.set_column("G:G", 12)
    ws.set_column("H:H", 11)
    ws.set_column("I:I", 34)
    ws.set_column("J:J", 11)
    ws.set_column("K:K", 13)
    ws.set_column("L:L", 34)
    ws.merge_range("A1:L2", "Hyperscaler consensus revisions — CY2027 / CY2028", title_fmt)
    ws.set_row(0, 28)
    ws.write("A3", f"Bloomberg BEst consensus · As of {payload['meta']['asof']} · USD", subtitle_fmt)
    ws.merge_range("A4:L4", "All charts and revision columns are in dollars: USD bn for capex, EBITDA and EBITDA - Capex; USD/share for EPS. MSFT is calendarized from quarterly consensus.", note_fmt)
    ws.write("A6", "Revision summary", section_fmt)

    dashboard_headers = ["Ticker", "Year", "Metric", "Current", "1M Δ", "1M %", "3M Δ", "3M %", "YTD Δ", "YTD %", "As of", "Basis / source"]
    dashboard_headers = ["Ticker", "Year", "Metric", "Current", "1M change", "3M change", "YTD change", "As of", "Basis / source"]
    start_row = 6
    for col, value in enumerate(dashboard_headers):
        ws.write(start_row, col, value, header_fmt)
    for idx, row in enumerate(payload["summary"], start_row + 1):
        ws.write(idx, 0, row["ticker"], text_fmt)
        ws.write_number(idx, 1, row["year"], text_fmt)
        ws.write(idx, 2, row["metric_label"], text_fmt)
        val_fmt = eps_fmt if row["metric"] == "eps" else bn_fmt
        for col, key in ((3, "current"), (4, "1m_change"), (5, "3m_change"), (6, "ytd_change")):
            if row.get(key) is None:
                ws.write_blank(idx, col, None, val_fmt)
            else:
                ws.write_number(idx, col, row[key], val_fmt)
        for col, key in ():
            if row.get(key) is None:
                ws.write_blank(idx, col, None, pct_fmt)
            else:
                ws.write_number(idx, col, row[key], pct_fmt)
        ws.write_datetime(idx, 7, dt.datetime.fromisoformat(row["current_date"]), date_fmt)
        ws.write(idx, 11, f"{row['basis']} · BBG BEst", text_wrap_fmt)
        ws.write(idx, 8, f"{row['basis']} ? {row['source']}", text_wrap_fmt)
        ws.write_blank(idx, 11, None, text_wrap_fmt)
    end_row = start_row + len(payload["summary"])
    for col in (4, 5, 6):
        ws.conditional_format(start_row + 1, col, end_row, col, {"type": "cell", "criteria": ">", "value": 0, "format": wb.add_format({"bg_color": light_blue, "font_color": "#1F4E78"})})
        ws.conditional_format(start_row + 1, col, end_row, col, {"type": "cell", "criteria": "<", "value": 0, "format": wb.add_format({"bg_color": light_orange, "font_color": "#9C5700"})})
    ws.autofilter(start_row, 0, end_row, len(dashboard_headers) - 1)
    ws.freeze_panes(start_row + 1, 3)
    ws.set_row(3, 30)

    # Long-form summary sheet.
    ss = wb.add_worksheet("Revision Summary")
    ss.hide_gridlines(2)
    summary_headers = [
        "Ticker", "Company", "Year", "Metric", "Unit", "Current", "Current date",
        "1M base", "1M base date", "1M change", "1M %", "3M base", "3M base date",
        "3M change", "3M %", "YTD base", "YTD base date", "YTD change", "YTD %",
        "Basis", "Source",
    ]
    for col, value in enumerate(summary_headers):
        ss.write(0, col, value, header_fmt)
    for r, row in enumerate(payload["summary"], 1):
        vals = [row["ticker"], row["company"], row["year"], row["metric_label"], row["unit"]]
        for c, value in enumerate(vals):
            ss.write(r, c, value, text_fmt)
        vf = eps_fmt if row["metric"] == "eps" else bn_fmt
        ss.write_number(r, 5, row["current"], vf)
        ss.write_datetime(r, 6, dt.datetime.fromisoformat(row["current_date"]), date_fmt)
        for base_col, date_col, change_col, pct_col, prefix in (
            (7, 8, 9, 10, "1m"), (11, 12, 13, 14, "3m"), (15, 16, 17, 18, "ytd")
        ):
            for col, key, fmt in ((base_col, f"{prefix}_base", vf), (change_col, f"{prefix}_change", vf), (pct_col, f"{prefix}_pct", pct_fmt)):
                if row.get(key) is None:
                    ss.write_blank(r, col, None, fmt)
                else:
                    ss.write_number(r, col, row[key], fmt)
            if row.get(f"{prefix}_base_date"):
                ss.write_datetime(r, date_col, dt.datetime.fromisoformat(row[f"{prefix}_base_date"]), date_fmt)
            else:
                ss.write_blank(r, date_col, None, date_fmt)
        ss.write(r, 19, row["basis"], text_wrap_fmt)
        ss.write(r, 20, row["source"], text_wrap_fmt)
    ss.freeze_panes(1, 5)
    ss.autofilter(0, 0, len(payload["summary"]), len(summary_headers) - 1)
    ss.set_column(0, 4, 14)
    ss.set_column(5, 18, 13)
    ss.set_column(19, 20, 38)
    ss.set_column(10, 10, None, None, {"hidden": True})
    ss.set_column(14, 14, None, None, {"hidden": True})
    ss.set_column(18, 18, None, None, {"hidden": True})

    hs = wb.add_worksheet("History")
    hs.hide_gridlines(2)
    hist_headers = ["Date", "Ticker", "Company", "Year", "Metric", "Unit", "Value", "Change vs first", "Raw BEst", "Roll adjustment", "Basis", "Source"]
    for col, value in enumerate(hist_headers):
        hs.write(0, col, value, header_fmt)
    hrow = 1
    for row in payload["history"]:
        hs.write_datetime(hrow, 0, dt.datetime.fromisoformat(row["date"]), date_fmt)
        hs.write(hrow, 1, row["ticker"], text_fmt)
        hs.write(hrow, 2, row["company"], text_fmt)
        hs.write_number(hrow, 3, row["year"], text_fmt)
        hs.write(hrow, 4, row["metric_label"], text_fmt)
        hs.write(hrow, 5, row["unit"], text_fmt)
        vf = eps_fmt if row["metric"] == "eps" else bn_fmt
        if row["value"] is None:
            hs.write_blank(hrow, 6, None, vf)
        else:
            hs.write_number(hrow, 6, row["value"], vf)
        if row["change_from_first"] is None:
            hs.write_blank(hrow, 7, None, vf)
        else:
            hs.write_number(hrow, 7, row["change_from_first"], vf)
        if row.get("raw_value") is None:
            hs.write_blank(hrow, 8, None, vf)
        else:
            hs.write_number(hrow, 8, row["raw_value"], vf)
        if row.get("roll_adjustment") is None:
            hs.write_blank(hrow, 9, None, vf)
        else:
            hs.write_number(hrow, 9, row["roll_adjustment"], vf)
        hs.write(hrow, 10, row["basis"], text_fmt)
        hs.write(hrow, 11, row["source"], text_fmt)
        hrow += 1
    hs.freeze_panes(1, 2)
    hs.autofilter(0, 0, hrow - 1, len(hist_headers) - 1)
    hs.set_column(0, 0, 12)
    hs.set_column(1, 5, 14)
    hs.set_column(6, 9, 15)
    hs.set_column(10, 11, 42)

    # Chart staging data, hidden from the default view.
    cd = wb.add_worksheet("Chart Data")
    cd.hide_gridlines(2)
    cd.hide()
    colors = {"MSFT": "#4472C4", "META": "#8064A2", "GOOG": "#70AD47", "AMZN": "#ED7D31"}
    chart_positions = {
        (2027, "capex"): "A43", (2027, "cash_proxy"): "G43", (2027, "eps"): "A60",
        (2028, "capex"): "G60", (2028, "cash_proxy"): "A77", (2028, "eps"): "G77",
    }
    chart_col = 0
    for year in YEARS:
        for metric, cfg in METRICS.items():
            if metric == "ebitda":
                continue
            block = [r for r in payload["history"] if r["year"] == year and r["metric"] == metric]
            by_date: dict[str, dict[str, float | None]] = defaultdict(dict)
            for row in block:
                value = row["value"]
                if metric == "eps":
                    revision = row.get("revision_from_first_pct")
                    value = 100.0 * (1.0 + revision) if revision is not None else None
                by_date[row["date"]][row["ticker"]] = value
            cd.write(0, chart_col, "Date", header_fmt)
            for i, ticker in enumerate(COMPANIES, 1):
                cd.write(0, chart_col + i, ticker, header_fmt)
            for rix, date in enumerate(sorted(by_date), 1):
                cd.write_datetime(rix, chart_col, dt.datetime.fromisoformat(date), wb.add_format({"num_format": "mmm-yy"}))
                for i, ticker in enumerate(COMPANIES, 1):
                    value = by_date[date].get(ticker)
                    if value is not None:
                        cd.write_number(rix, chart_col + i, value)
            chart = wb.add_chart({"type": "line"})
            for i, ticker in enumerate(COMPANIES, 1):
                chart.add_series(
                    {
                        "name": ["Chart Data", 0, chart_col + i],
                        "categories": ["Chart Data", 1, chart_col, len(by_date), chart_col],
                        "values": ["Chart Data", 1, chart_col + i, len(by_date), chart_col + i],
                        "line": {"color": colors[ticker], "width": 2.0},
                    }
                )
            chart.set_title({"name": f"{cfg['label']} CY{year} — revision vs first 2026 observation", "name_font": {"size": 11, "bold": True, "color": navy}})
            chart_title = (
                f"EPS CY{year} - revision index (first 2026 = 100)"
                if metric == "eps"
                else f"{cfg['label']} CY{year} - consensus level ({cfg['unit']})"
            )
            if metric == "eps" and year == 2027:
                chart_title += " - MSFT roll-adjusted"
            chart.set_title({"name": chart_title, "name_font": {"size": 11, "bold": True, "color": navy}})
            chart.set_x_axis({"date_axis": True, "num_format": "mmm", "major_unit": 31, "major_unit_type": "days", "label_position": "low", "line": {"color": border}})
            y_num_format = "0.0" if metric == "eps" else "$0.0"
            chart.set_y_axis({"num_format": y_num_format, "major_gridlines": {"visible": True, "line": {"color": "#E8EDF2"}}, "line": {"none": True}})
            chart.set_legend({"position": "bottom", "font": {"size": 9}})
            chart.set_plotarea({"border": {"none": True}, "fill": {"color": white}})
            chart.set_chartarea({"border": {"none": True}, "fill": {"color": white}})
            chart.set_size({"width": 570, "height": 300})
            ws.insert_chart(chart_positions[(year, metric)], chart)
            chart_col += 6

    # EBITDA revisions use company-level small multiples so each company has
    # an independent USD-bn y-axis and the revision shape remains visible.
    ed = wb.add_worksheet("EBITDA Detail")
    ed.hide_gridlines(2)
    ed.set_tab_color("#8064A2")
    ed.merge_range("A1:L2", "EBITDA consensus revisions - independent company axes", title_fmt)
    ed.merge_range(
        "A3:L3",
        "Each panel is in USD bn and auto-scales independently. Compare direction and magnitude within a company, not vertical position across panels.",
        note_fmt,
    )
    ebitda_positions = {
        (2027, "MSFT"): "A5", (2027, "META"): "G5", (2027, "GOOG"): "A22", (2027, "AMZN"): "G22",
        (2028, "MSFT"): "A39", (2028, "META"): "G39", (2028, "GOOG"): "A56", (2028, "AMZN"): "G56",
    }
    for year in YEARS:
        for ticker in COMPANIES:
            rows = sorted(
                [r for r in payload["history"] if r["year"] == year and r["metric"] == "ebitda" and r["ticker"] == ticker and r["value"] is not None],
                key=lambda r: r["date"],
            )
            cd.write(0, chart_col, "Date", header_fmt)
            cd.write(0, chart_col + 1, ticker, header_fmt)
            for rix, row in enumerate(rows, 1):
                cd.write_datetime(rix, chart_col, dt.datetime.fromisoformat(row["date"]), wb.add_format({"num_format": "mmm-yy"}))
                cd.write_number(rix, chart_col + 1, row["value"])
            chart = wb.add_chart({"type": "line"})
            chart.add_series(
                {
                    "name": ["Chart Data", 0, chart_col + 1],
                    "categories": ["Chart Data", 1, chart_col, len(rows), chart_col],
                    "values": ["Chart Data", 1, chart_col + 1, len(rows), chart_col + 1],
                    "line": {"color": colors[ticker], "width": 2.5},
                }
            )
            title_suffix = " - roll-adjusted" if ticker == "MSFT" and year == 2027 else ""
            chart.set_title({"name": f"{ticker} CY{year} EBITDA (USD bn){title_suffix}", "name_font": {"size": 11, "bold": True, "color": navy}})
            chart.set_x_axis({"date_axis": True, "num_format": "mmm", "major_unit": 31, "major_unit_type": "days", "label_position": "low", "line": {"color": border}})
            chart.set_y_axis({"num_format": "$0.0", "major_gridlines": {"visible": True, "line": {"color": "#E8EDF2"}}, "line": {"none": True}})
            chart.set_legend({"none": True})
            chart.set_plotarea({"border": {"none": True}, "fill": {"color": white}})
            chart.set_chartarea({"border": {"none": True}, "fill": {"color": white}})
            chart.set_size({"width": 570, "height": 300})
            ed.insert_chart(ebitda_positions[(year, ticker)], chart)
            chart_col += 3
    ed.set_column("A:L", 12)

    cs = wb.add_worksheet("Sources & Checks")
    cs.hide_gridlines(2)
    cs.merge_range("A1:G2", "Sources, basis, and validation checks", title_fmt)
    cs.write("A4", "Methodology", section_fmt)
    cs.merge_range("A5:G6", payload["meta"]["methodology"], note_fmt)
    cs.write("A8", "Bloomberg fields", section_fmt)
    for r, (metric, field) in enumerate(payload["meta"]["fields"].items(), 8):
        cs.write(r, 0, METRICS[metric]["label"], text_fmt)
        cs.write(r, 1, field, text_fmt)
        cs.write(r, 2, "Bloomberg BEst consensus", text_fmt)
    cs.write(11, 0, METRICS["cash_proxy"]["label"], text_fmt)
    cs.write(11, 1, "BEST_EBITDA - positive-spend BEST_CAPEX", text_fmt)
    cs.write(11, 2, "Calculated proxy; not reported FCF", text_fmt)
    cs.write("A13", "MSFT calendarization roll sources", section_fmt)
    roll_headers = ["Reported", "Effective", "CY27 quarters start", "CY28 quarters start", "Source", "Local path"]
    for col, value in enumerate(roll_headers):
        cs.write(13, col, value, header_fmt)
    for r, roll in enumerate(payload["meta"]["msft_rolls"], 14):
        cs.write(r, 0, roll["reported"], text_fmt)
        cs.write(r, 1, roll["effective"], text_fmt)
        cs.write(r, 2, f"{roll['cy27_start_fq']}FQ", text_fmt)
        cs.write(r, 3, f"{roll['cy28_start_fq']}FQ", text_fmt)
        cs.write(r, 4, roll["source"], text_wrap_fmt)
        abs_path = ROOT / roll["path"]
        cs.write_url(r, 5, abs_path.as_uri(), link_fmt, string=roll["path"])
    check_start = 19
    cs.write(check_start - 1, 0, "Validation checks", section_fmt)
    check_headers = ["Check", "Ticker", "Year", "Metric", "Status", "Detail"]
    for col, value in enumerate(check_headers):
        cs.write(check_start, col, value, header_fmt)
    for r, check in enumerate(payload["checks"], check_start + 1):
        cs.write(r, 0, check["check"], text_fmt)
        cs.write(r, 1, check["ticker"], text_fmt)
        cs.write_number(r, 2, check["year"], text_fmt)
        cs.write(r, 3, METRICS[check["metric"]]["label"], text_fmt)
        status_fmt = pass_fmt if check["status"] == "PASS" else warn_fmt if check["status"] == "WARN" else fail_fmt
        cs.write(r, 4, check["status"], status_fmt)
        cs.write(r, 5, check["detail"], text_wrap_fmt)
    cs.freeze_panes(check_start + 1, 1)
    cs.set_column("A:A", 40)
    cs.set_column("B:E", 14)
    cs.set_column("F:F", 76)
    cs.set_column("G:G", 12)

    rd = wb.add_worksheet("README")
    rd.hide_gridlines(2)
    rd.merge_range("A1:F2", "Hyperscaler revisions workbook", title_fmt)
    readme_rows = [
        ("Purpose", "Track Bloomberg consensus revisions for CY2027 and CY2028 capex, EBITDA, and EPS across MSFT, META, GOOG, and AMZN."),
        ("Source", payload["meta"]["source"] + f"; pulled {payload['meta']['asof']}."),
        ("Refresh", "py _wiki/_tools/build_hyperscaler_revisions.py"),
        ("Periods", "Bloomberg 2CY = CY2027 and 3CY = CY2028 for the 2026 observation window."),
        ("MSFT", "June fiscal year: fixed CY values are sums of quarterly BEst estimates. Relative-quarter cutovers use Microsoft earnings dates listed in Sources & Checks."),
        ("Capex sign", "Bloomberg BEST_CAPEX is a negative cash outflow. The workbook sign-flips it so higher positive values mean more spending."),
        ("Revisions", payload["meta"]["revision_windows"]),
        ("Cash proxy", "EBITDA minus positive-spend capex. This is not reported FCF and excludes working capital, cash taxes, interest, leases outside capex, and other cash items."),
        ("Missing values", "Blanks are retained when Bloomberg had no consensus for a far-dated period; the workbook does not interpolate missing estimates."),
        ("Attribution", "Every table carries source/date/basis columns; all numeric consensus data are Bloomberg BEst via the Capstone wrapper."),
    ]
    rd.write("A4", "Item", header_fmt)
    rd.write("B4", "Detail", header_fmt)
    for r, (item, detail) in enumerate(readme_rows, 4):
        rd.write(r, 0, item, text_fmt)
        rd.write(r, 1, detail, text_wrap_fmt)
        rd.set_row(r, 32)
    rd.set_column("A:A", 18)
    rd.set_column("B:B", 100)

    wb.close()


def html_payload(payload: dict[str, Any]) -> str:
    compact = {"meta": payload["meta"], "summary": payload["summary"], "history": payload["history"]}
    return json.dumps(compact, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def write_dashboard(payload: dict[str, Any]) -> None:
    DASH_OUT.parent.mkdir(parents=True, exist_ok=True)
    data = html_payload(payload)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hyperscaler revisions — CY2027/CY2028</title>
<style>
:root{{--bg:#0c1622;--panel:#132235;--panel2:#182b40;--text:#edf4fb;--muted:#9fb0c2;--border:#294059;--grid:#27405a;--accent:#70a7e8;--up:#83c5be;--down:#f4a261;--msft:#5b8ff9;--meta:#9270ca;--goog:#5ad8a6;--amzn:#f6bd16}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1240px;margin:0 auto;padding:28px 24px 36px}}h1{{font-size:25px;font-weight:600;margin:0 0 6px}}.sub{{color:var(--muted);margin-bottom:22px}}.controls{{display:flex;gap:18px;flex-wrap:wrap;align-items:end;margin-bottom:14px}}fieldset{{border:0;padding:0;margin:0}}legend{{color:var(--muted);font-size:12px;margin-bottom:6px}}.group{{display:flex;gap:6px;flex-wrap:wrap}}button{{appearance:none;border:1px solid var(--border);background:transparent;color:var(--text);border-radius:8px;padding:8px 12px;cursor:pointer}}button[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:#09131f}}button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}.chart-wrap{{position:relative;border-top:1px solid var(--border);padding-top:16px}}svg{{display:block;width:100%;height:auto;overflow:visible}}.grid{{stroke:var(--grid);stroke-width:1}}.axis-text{{fill:var(--muted);font-size:12px}}.zero{{stroke:var(--muted);stroke-width:1.2}}.line{{fill:none;stroke-width:3}}.point{{stroke:var(--bg);stroke-width:2}}.legend{{display:flex;gap:18px;flex-wrap:wrap;margin:2px 0 16px}}.legend span{{display:inline-flex;align-items:center;gap:7px}}.dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}.tip{{position:absolute;display:none;pointer-events:none;background:var(--panel2);border:1px solid var(--border);border-radius:8px;padding:8px 10px;box-shadow:0 10px 28px rgba(0,0,0,.28);white-space:nowrap;z-index:5}}.table-wrap{{overflow-x:auto;margin-top:8px}}table{{width:100%;border-collapse:collapse;min-width:760px}}th,td{{padding:10px 12px;border-bottom:1px solid var(--border);text-align:right}}th{{color:var(--muted);font-size:12px;font-weight:600}}th:first-child,td:first-child{{text-align:left}}td:nth-child(2){{text-align:left}}.up{{color:var(--up)}}.down{{color:var(--down)}}footer{{color:var(--muted);font-size:12px;margin-top:18px;padding-top:14px;border-top:1px solid var(--border)}}@media(max-width:640px){{main{{padding:20px 14px}}h1{{font-size:21px}}.controls{{gap:12px}}}}
</style>
</head>
<body><main>
<h1>Hyperscaler consensus revisions — CY2027 / CY2028</h1>
<div class="sub">Bloomberg BEst consensus · as of {html.escape(payload['meta']['asof'])} · capex and EBITDA in USD bn; EPS in USD/share</div>
<div class="sub" style="margin-top:-16px">Chart basis: EPS is indexed to the first 2026 observation = 100; EBITDA uses one independently scaled USD-bn panel per company. MSFT CY2027 EBITDA and EPS are roll-adjusted at earnings cutovers.</div>
<div class="controls">
  <fieldset><legend>Metric</legend><div class="group" id="metric-controls">
    <button type="button" data-metric="capex" aria-pressed="true">Capex</button>
    <button type="button" data-metric="ebitda" aria-pressed="false">EBITDA</button>
    <button type="button" data-metric="cash_proxy" aria-pressed="false">EBITDA - Capex</button>
    <button type="button" data-metric="eps" aria-pressed="false">EPS</button>
  </div></fieldset>
  <fieldset><legend>Calendar year</legend><div class="group" id="year-controls">
    <button type="button" data-year="2027" aria-pressed="true">CY2027</button>
    <button type="button" data-year="2028" aria-pressed="false">CY2028</button>
  </div></fieldset>
</div>
<div class="legend" id="legend"></div>
<div class="chart-wrap"><svg id="chart" viewBox="0 0 1120 430" role="img" aria-label="Consensus revision history"></svg><div class="tip" id="tip"></div></div>
<div class="table-wrap"><table aria-label="Revision summary"><thead><tr><th>Ticker</th><th>Company</th><th>Current</th><th>1M change</th><th>3M change</th><th>YTD change</th><th>Basis</th></tr></thead><tbody id="summary-body"></tbody></table></div>
<footer>Source: Bloomberg BEst via Capstone wrapper / local Bloomberg Desktop API fallback, {html.escape(payload['meta']['asof'])}. MSFT uses four quarterly BEst estimates for fixed calendar years because June-FY historical nCY requests fall back to fiscal periods; roll dates are Microsoft earnings calls/filings dated 2026-01-28, 2026-04-29, and 2026-07-29. MSFT CY2027 EBITDA and EPS are backward chain-linked across those rolls to neutralize contributor-set discontinuities; the latest absolute BEst levels are unchanged and raw quarterly sums are retained in the workbook and JSON. Capex is sign-flipped to positive spend. EBITDA - Capex is a simple proxy, not reported FCF; it excludes working capital, cash taxes, interest, leases outside capex, and other cash items. Blanks mean Bloomberg had no far-period consensus; no interpolation.</footer>
</main>
<script>const DATA={data};
const state={{metric:'capex',year:2027}};const colors={{MSFT:'var(--msft)',META:'var(--meta)',GOOG:'var(--goog)',AMZN:'var(--amzn)'}};const names={{MSFT:'Microsoft',META:'Meta',GOOG:'Alphabet',AMZN:'Amazon'}};
const svg=document.getElementById('chart'),tip=document.getElementById('tip');
const esc=s=>String(s).replace(/[&<>\"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}}[c]));
const fmtPct=v=>v==null?'—':(v>=0?'+':'')+(v*100).toFixed(1)+'%';
const fmtValue=(v,m)=>v==null?'—':(m==='eps'?'$'+v.toFixed(2):'$'+v.toFixed(1)+'bn');
const fmtDelta=(v,m)=>v==null?'?':(v>=0?'+':'')+(m==='eps'?'$'+Math.abs(v).toFixed(2):'$'+Math.abs(v).toFixed(1)+'bn');
const fmtAxis=(v,m)=>m==='eps'?'$'+v.toFixed(1):'$'+v.toFixed(0)+'bn';
const fmtSigned=(v,m)=>v==null?'?':(v>=0?'+':'-')+(m==='eps'?'$'+Math.abs(v).toFixed(2):'$'+Math.abs(v).toFixed(1)+'bn');
function path(points,x,y){{return points.map((p,i)=>(i?'L':'M')+x(new Date(p.date))+','+y(p.value)).join(' ')}}
function render(){{
 document.querySelectorAll('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.metric===state.metric));document.querySelectorAll('[data-year]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.year)===state.year));
 const rows=DATA.history.filter(r=>r.metric===state.metric&&r.year===state.year&&r.value!=null);const by={{}};rows.forEach(r=>(by[r.ticker]??=[]).push(r));
 const all=rows.map(r=>r.value),dates=rows.map(r=>new Date(r.date));const minD=Math.min(...dates),maxD=Math.max(...dates);let minV=Math.min(0,...all),maxV=Math.max(0,...all);let pad=(maxV-minV)*.08||1;minV-=pad;maxV+=pad;
 const W=1120,H=430,L=78,R=34,T=18,B=54;const x=d=>L+(d-minD)/(maxD-minD||1)*(W-L-R),y=v=>T+(maxV-v)/(maxV-minV||1)*(H-T-B);
 let s='<title>Consensus level history</title><desc>Bloomberg consensus values in dollars for four hyperscalers.</desc>';for(let i=0;i<=5;i++){{let v=minV+(maxV-minV)*i/5,yy=y(v);s+=`<line class="grid" x1="${{L}}" x2="${{W-R}}" y1="${{yy}}" y2="${{yy}}"/><text class="axis-text" x="${{L-12}}" y="${{yy+4}}" text-anchor="end">${{fmtAxis(v,state.metric)}}</text>`}}if(minV<=0&&maxV>=0)s+=`<line class="zero" x1="${{L}}" x2="${{W-R}}" y1="${{y(0)}}" y2="${{y(0)}}"/>`;
 const months=[];let md=new Date(new Date(minD).getFullYear(),new Date(minD).getMonth(),1);while(md<=new Date(maxD)){{months.push(new Date(md));md=new Date(md.getFullYear(),md.getMonth()+1,1)}}months.forEach(d=>{{let xx=x(d);s+=`<line class="grid" x1="${{xx}}" x2="${{xx}}" y1="${{T}}" y2="${{H-B}}"/><text class="axis-text" x="${{xx}}" y="${{H-B+26}}" text-anchor="middle">${{d.toLocaleDateString('en-US',{{month:'short'}})}}</text>`}});
 Object.keys(names).forEach(t=>{{let pts=(by[t]||[]).sort((a,b)=>a.date.localeCompare(b.date));if(!pts.length)return;s+=`<path class="line" d="${{path(pts,x,y)}}" stroke="${{colors[t]}}"/>`;pts.forEach(p=>s+=`<circle class="point" tabindex="0" data-t="${{t}}" data-date="${{p.date}}" data-v="${{p.value}}" cx="${{x(new Date(p.date))}}" cy="${{y(p.value)}}" r="4" fill="${{colors[t]}}"/>`)}});svg.innerHTML=s;
 document.getElementById('legend').innerHTML=Object.keys(names).map(t=>`<span><i class="dot" style="background:${{colors[t]}}"></i>${{t}}</span>`).join('');
 svg.querySelectorAll('circle').forEach(c=>{{const show=()=>{{tip.style.display='block';tip.innerHTML=`<b>${{esc(c.dataset.t)}}</b> · ${{esc(c.dataset.date)}}<br>${{fmtPct(Number(c.dataset.v))}} vs first 2026 observation`;const box=svg.getBoundingClientRect(),cx=Number(c.getAttribute('cx'))/1120*box.width,cy=Number(c.getAttribute('cy'))/430*box.height;tip.style.left=Math.min(Math.max(cx+12,0),box.width-190)+'px';tip.style.top=Math.max(cy-54,0)+'px'}};c.addEventListener('mouseenter',show);c.addEventListener('focus',show);c.addEventListener('mouseleave',()=>tip.style.display='none');c.addEventListener('blur',()=>tip.style.display='none')}});
 svg.querySelectorAll('circle').forEach(c=>{{const showValue=()=>{{tip.innerHTML=`<b>${{esc(c.dataset.t)}}</b> ? ${{esc(c.dataset.date)}}<br>${{fmtValue(Number(c.dataset.v),state.metric)}} BEst consensus`}};c.addEventListener('mouseenter',showValue);c.addEventListener('focus',showValue)}});
 const sm=DATA.summary.filter(r=>r.metric===state.metric&&r.year===state.year);document.getElementById('summary-body').innerHTML=sm.map(r=>`<tr><td><b>${{r.ticker}}</b></td><td>${{esc(r.company)}}</td><td>${{fmtValue(r.current,state.metric)}}</td><td class="${{(r['1m_change']||0)>=0?'up':'down'}}">${{fmtSigned(r['1m_change'],state.metric)}}</td><td class="${{(r['3m_change']||0)>=0?'up':'down'}}">${{fmtSigned(r['3m_change'],state.metric)}}</td><td class="${{(r.ytd_change||0)>=0?'up':'down'}}">${{fmtSigned(r.ytd_change,state.metric)}}</td><td>${{esc(r.basis)}}</td></tr>`).join('');
}}
const linePath=(points,x,y)=>points.map((p,i)=>(i?'L':'M')+x(new Date(p.date))+','+y(p.plotValue)).join(' ');
function sharedView(rows){{
 const by={{}};rows.forEach(r=>(by[r.ticker]??=[]).push(r));svg.setAttribute('viewBox','0 0 1120 430');
 const all=rows.map(r=>r.plotValue),dates=rows.map(r=>new Date(r.date)),minD=Math.min(...dates),maxD=Math.max(...dates);let minV=state.metric==='eps'?Math.min(...all):Math.min(0,...all),maxV=state.metric==='eps'?Math.max(...all):Math.max(0,...all);const pad=(maxV-minV)*.08||1;minV-=pad;maxV+=pad;
 const W=1120,H=430,L=78,R=34,T=18,B=54,x=d=>L+(d-minD)/(maxD-minD||1)*(W-L-R),y=v=>T+(maxV-v)/(maxV-minV||1)*(H-T-B),axis=v=>state.metric==='eps'?v.toFixed(1):'$'+v.toFixed(0)+'bn';
 let s='<title>Consensus revision history</title><desc>Capex and cash proxy in USD billions; EPS indexed to the first 2026 observation.</desc>';
 for(let i=0;i<=5;i++){{const v=minV+(maxV-minV)*i/5,yy=y(v);s+=`<line class="grid" x1="${{L}}" x2="${{W-R}}" y1="${{yy}}" y2="${{yy}}"/><text class="axis-text" x="${{L-12}}" y="${{yy+4}}" text-anchor="end">${{axis(v)}}</text>`}}
 if(state.metric!=='eps'&&minV<=0&&maxV>=0)s+=`<line class="zero" x1="${{L}}" x2="${{W-R}}" y1="${{y(0)}}" y2="${{y(0)}}"/>`;
 const months=[];let md=new Date(new Date(minD).getFullYear(),new Date(minD).getMonth(),1);while(md<=new Date(maxD)){{months.push(new Date(md));md=new Date(md.getFullYear(),md.getMonth()+1,1)}}months.forEach(d=>{{const xx=x(d);s+=`<line class="grid" x1="${{xx}}" x2="${{xx}}" y1="${{T}}" y2="${{H-B}}"/><text class="axis-text" x="${{xx}}" y="${{H-B+26}}" text-anchor="middle">${{d.toLocaleDateString('en-US',{{month:'short'}})}}</text>`}});
 Object.keys(names).forEach(t=>{{const pts=(by[t]||[]).sort((a,b)=>a.date.localeCompare(b.date));if(!pts.length)return;s+=`<path class="line" d="${{linePath(pts,x,y)}}" stroke="${{colors[t]}}"/>`;pts.forEach(p=>s+=`<circle class="point" tabindex="0" data-t="${{t}}" data-date="${{p.date}}" data-v="${{p.value}}" data-idx="${{p.plotValue}}" cx="${{x(new Date(p.date))}}" cy="${{y(p.plotValue)}}" r="4" fill="${{colors[t]}}"/>`)}});
 svg.innerHTML=s;
}}
function ebitdaView(rows){{
 svg.setAttribute('viewBox','0 0 1120 590');const dates=rows.map(r=>new Date(r.date)),minD=Math.min(...dates),maxD=Math.max(...dates),PW=540,PH=270,panels=[[0,0],[560,0],[0,295],[560,295]];let s='<title>EBITDA consensus revisions by company</title><desc>Four company panels, each with an independent USD-billion y-axis.</desc>';
 Object.keys(names).forEach((t,ix)=>{{const pts=rows.filter(r=>r.ticker===t).sort((a,b)=>a.date.localeCompare(b.date));if(!pts.length)return;const [ox,oy]=panels[ix],L=ox+68,R=ox+PW-18,T=oy+42,B=oy+PH-32,vals=pts.map(p=>p.value);let minV=Math.min(...vals),maxV=Math.max(...vals),pad=(maxV-minV)*.18||1;minV-=pad;maxV+=pad;const x=d=>L+(d-minD)/(maxD-minD||1)*(R-L),y=v=>T+(maxV-v)/(maxV-minV||1)*(B-T),last=pts[pts.length-1];
  const panelSuffix=t==='MSFT'&&state.year===2027?' (roll-adjusted)':'';
  s+=`<rect x="${{ox+2}}" y="${{oy+2}}" width="${{PW-4}}" height="${{PH-4}}" rx="10" fill="var(--panel)" stroke="var(--border)"/><text x="${{ox+18}}" y="${{oy+27}}" fill="${{colors[t]}}" font-size="14" font-weight="700">${{t}}${{panelSuffix}} - ${{fmtValue(last.value,'ebitda')}}</text>`;
  for(let i=0;i<=4;i++){{const v=minV+(maxV-minV)*i/4,yy=y(v);s+=`<line class="grid" x1="${{L}}" x2="${{R}}" y1="${{yy}}" y2="${{yy}}"/><text class="axis-text" x="${{L-8}}" y="${{yy+4}}" text-anchor="end">$${{v.toFixed(0)}}bn</text>`}}
  [new Date(minD),new Date((minD+maxD)/2),new Date(maxD)].forEach(d=>{{const xx=x(d);s+=`<text class="axis-text" x="${{xx}}" y="${{B+22}}" text-anchor="middle">${{d.toLocaleDateString('en-US',{{month:'short'}})}}</text>`}});
  s+=`<path class="line" d="${{linePath(pts,x,y)}}" stroke="${{colors[t]}}"/>`;pts.forEach(p=>s+=`<circle class="point" tabindex="0" data-t="${{t}}" data-date="${{p.date}}" data-v="${{p.value}}" data-idx="${{p.value}}" cx="${{x(new Date(p.date))}}" cy="${{y(p.value)}}" r="4" fill="${{colors[t]}}"/>`);}});
 svg.innerHTML=s;
}}
function wireTips(viewHeight){{
 svg.querySelectorAll('circle').forEach(c=>{{const show=()=>{{tip.style.display='block';const extra=state.metric==='eps'?`<br>Revision index ${{Number(c.dataset.idx).toFixed(1)}} (first 2026 = 100)`:'';const label=c.dataset.t==='MSFT'&&state.year===2027&&(state.metric==='ebitda'||state.metric==='eps')?'roll-adjusted BEst trend':'BEst consensus';tip.innerHTML=`<b>${{esc(c.dataset.t)}}</b> &middot; ${{esc(c.dataset.date)}}<br>${{fmtValue(Number(c.dataset.v),state.metric)}} ${{label}}${{extra}}`;const box=svg.getBoundingClientRect(),cx=Number(c.getAttribute('cx'))/1120*box.width,cy=Number(c.getAttribute('cy'))/viewHeight*box.height;tip.style.left=Math.min(Math.max(cx+12,0),box.width-240)+'px';tip.style.top=Math.max(cy-68,0)+'px'}};c.addEventListener('mouseenter',show);c.addEventListener('focus',show);c.addEventListener('mouseleave',()=>tip.style.display='none');c.addEventListener('blur',()=>tip.style.display='none')}});
}}
function render(){{
 document.querySelectorAll('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.metric===state.metric));document.querySelectorAll('[data-year]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.year)===state.year));
 const rows=DATA.history.filter(r=>r.metric===state.metric&&r.year===state.year&&r.value!=null).map(r=>({{...r,plotValue:state.metric==='eps'?100*(1+(r.revision_from_first_pct||0)):r.value}}));
 if(state.metric==='ebitda')ebitdaView(rows);else sharedView(rows);
 document.getElementById('legend').innerHTML=Object.keys(names).map(t=>`<span><i class="dot" style="background:${{colors[t]}}"></i>${{t}}</span>`).join('');
 wireTips(state.metric==='ebitda'?590:430);
 const sm=DATA.summary.filter(r=>r.metric===state.metric&&r.year===state.year);document.getElementById('summary-body').innerHTML=sm.map(r=>`<tr><td><b>${{r.ticker}}</b></td><td>${{esc(r.company)}}</td><td>${{fmtValue(r.current,state.metric)}}</td><td class="${{(r['1m_change']||0)>=0?'up':'down'}}">${{fmtSigned(r['1m_change'],state.metric)}}</td><td class="${{(r['3m_change']||0)>=0?'up':'down'}}">${{fmtSigned(r['3m_change'],state.metric)}}</td><td class="${{(r.ytd_change||0)>=0?'up':'down'}}">${{fmtSigned(r.ytd_change,state.metric)}}</td><td>${{esc(r.basis)}}</td></tr>`).join('');
}}
document.querySelectorAll('[data-metric]').forEach(b=>b.addEventListener('click',()=>{{state.metric=b.dataset.metric;render()}}));document.querySelectorAll('[data-year]').forEach(b=>b.addEventListener('click',()=>{{state.year=Number(b.dataset.year);render()}}));render();
</script></body></html>"""
    DASH_OUT.write_text(doc, encoding="utf-8")


def main() -> None:
    payload = fetch_data()
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_workbook(payload)
    write_dashboard(payload)
    failures = [c for c in payload["checks"] if c["status"] == "FAIL"]
    warnings = [c for c in payload["checks"] if c["status"] == "WARN"]
    print(f"JSON: {DATA_OUT}")
    print(f"XLSX: {XLSX_OUT}")
    print(f"HTML: {DASH_OUT}")
    print(f"Rows: summary={len(payload['summary'])} history={len(payload['history'])}")
    print(f"Checks: {len(payload['checks']) - len(failures) - len(warnings)} PASS / {len(warnings)} WARN / {len(failures)} FAIL")
    if failures:
        for check in failures:
            print("FAIL:", check)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
