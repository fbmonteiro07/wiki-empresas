#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch 5-year weekly blended-forward P/E (1BF and 2BF) for the AI complex.

Basis matches the Capstone comp-dashboard forward-P/E charts: BEST_PE_RATIO with
BEST_FPERIOD_OVERRIDE=1BF (1-yr blended forward) and 2BF (2-yr blended forward).
Output: _wiki/_data/ai_pe_5y.json
Run: py _wiki/_tools/build_ai_pe5y.py
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BBG_DIR = Path(r"E:\bloomberg_api")
if str(BBG_DIR) not in sys.path:
    sys.path.insert(0, str(BBG_DIR))

from bloomberg import bdh, bdp  # noqa: E402

OUT = ROOT / "_wiki" / "_data" / "ai_pe_5y.json"
ASOF = dt.date.today()
START = "20210801"

NAMES = {
    "MSFT": "MSFT US Equity", "GOOG": "GOOG US Equity", "META": "META US Equity",
    "AMZN": "AMZN US Equity", "NVDA": "NVDA US Equity", "AVGO": "AVGO US Equity",
    "TSM": "TSM US Equity", "ASML": "ASML US Equity",
}
BBG_TO_TK = {v: k for k, v in NAMES.items()}


def bbg_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        msg = str(exc).lower()
        if "500" not in msg and "503" not in msg and "connect" not in msg:
            raise
        os.environ["BBG_LOCAL_ONLY"] = "1"
        return fn(*args, **kwargs)


def series(df):
    out = defaultdict(dict)
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        tk = BBG_TO_TK.get(str(row.get("ticker")))
        try:
            v = float(row.get("value"))
        except (TypeError, ValueError):
            continue
        if tk and math.isfinite(v):
            out[tk][str(row.get("date"))[:10]] = round(v, 3)
    return out


def main():
    all_bbg = list(NAMES.values())
    data = {}
    for ov in ("1BF", "2BF"):
        hist = bbg_call(bdh, all_bbg, ["BEST_PE_RATIO"], START, ASOF.strftime("%Y%m%d"),
                        periodicitySelection="WEEKLY", BEST_FPERIOD_OVERRIDE=ov)
        data[ov] = series(hist)
        snap = bbg_call(bdp, all_bbg, ["BEST_PE_RATIO"], BEST_FPERIOD_OVERRIDE=ov)
        for _, row in snap.iterrows():
            tk = BBG_TO_TK.get(str(row.get("ticker")))
            try:
                v = float(row.get("value"))
            except (TypeError, ValueError):
                continue
            if tk and math.isfinite(v):
                data[ov].setdefault(tk, {})[ASOF.isoformat()] = round(v, 3)
        n = sum(len(v) for v in data[ov].values())
        print(f"{ov}: {n} points across {len(data[ov])} tickers")

    dates = sorted({d for ov in data.values() for tk in ov.values() for d in tk})
    payload = {
        "meta": {
            "asof": ASOF.isoformat(),
            "source": "Bloomberg BEST_PE_RATIO via Capstone wrapper; BEST_FPERIOD_OVERRIDE=1BF/2BF (blended forward), weekly",
            "start": "2021-08-01",
        },
        "dates": dates,
        "pe": {tk: {
            "p1": [data["1BF"].get(tk, {}).get(d) for d in dates],
            "p2": [data["2BF"].get(tk, {}).get(d) for d in dates],
        } for tk in NAMES},
    }
    OUT.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT} — {len(dates)} weeks, asof {ASOF}")


if __name__ == "__main__":
    main()
