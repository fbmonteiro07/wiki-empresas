#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fetch_funding.py — market series for the AI credit & funding monitor.

Pulls ~2 years of daily history from the LOCAL Bloomberg terminal (bdh via
E:\bloomberg_api, localhost:8194 — raises loudly if the Terminal is closed)
into _wiki/_data/funding_market.json. On any failure the previous JSON is
left untouched and the script exits 1.

Weekly routine authorized 2026-09-29; also supports a standalone refresh:
    py "E:/Wiki Felipe empresas/_wiki/_tools/fetch_funding.py"
    py "E:/Wiki Felipe empresas/_wiki/_tools/build_funding_monitor.py"

Instrument config lives in _data/funding_deals.json:
  - market_series[]: {ticker, label, unit, decimals} — fetched as PX_LAST.
  - bonds[]: EMPTY SLOT — paste Bloomberg tickers or "/isin/XX… Corp" rows as
    {ticker, label, unit, field?} (field defaults to PX_LAST; use YLD_YTM_MID
    or Z_SPRD_MID for bonds) and re-run. They are appended to the same file
    and the dashboard picks them up automatically.
"""
import json
import sys
import datetime as dt
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
DEALS = DATA / "funding_deals.json"
OUT = DATA / "funding_market.json"

sys.path.insert(0, r"E:\bloomberg_api")


def main():
    cfg = json.loads(DEALS.read_text(encoding="utf-8"))
    instruments = []
    for row in cfg.get("market_series", []):
        instruments.append({**row, "field": row.get("field", "PX_LAST")})
    for row in cfg.get("bonds", []):
        instruments.append({**row, "field": row.get("field", "PX_LAST")})
    if not instruments:
        print("no instruments configured — nothing to fetch")
        return 1

    from bloomberg import bdh  # local-terminal-only wrapper; raises if down

    # A Friday morning brief must compare completed sessions, not intraday marks.
    end = dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=730)
    s, e = start.strftime("%Y%m%d"), end.strftime("%Y%m%d")

    # group by field so each bdh call is one (tickers, [field]) batch
    by_field = {}
    for ins in instruments:
        by_field.setdefault(ins["field"], []).append(ins)

    series_out, errors = [], []
    for field, group in by_field.items():
        tickers = [g["ticker"] for g in group]
        try:
            df = bdh(tickers, [field], s, e)
        except Exception as exc:  # terminal down / entitlement — fail loud
            errors.append(f"bdh({tickers}, {field}): {type(exc).__name__}: {exc}")
            continue
        cols = {c.lower(): c for c in df.columns}
        c_date, c_tk, c_val = cols.get("date"), cols.get("ticker"), cols.get("value")
        if not all([c_date, c_tk, c_val]):
            errors.append(f"unexpected bdh columns {list(df.columns)} for {field}")
            continue
        for g in group:
            sub = df[df[c_tk] == g["ticker"]].sort_values(c_date)
            pts = [[str(r[c_date])[:10], round(float(r[c_val]), 4)]
                   for _, r in sub.iterrows() if math.isfinite(float(r[c_val])) and str(r[c_date])[:10] <= str(end)]
            pts = sorted(dict(pts).items())
            if not pts:
                errors.append(f"{g['ticker']}: no data returned")
                continue
            series_out.append({
                "ticker": g["ticker"], "label": g.get("label", g["ticker"]),
                "unit": g.get("unit", ""), "field": field,
                "decimals": g.get("decimals", 2), "points": pts,
                "last": pts[-1][1], "last_date": pts[-1][0],
            })
            print(f"  {g['ticker']:<18} {len(pts):>4} pts  last {pts[-1][1]} ({pts[-1][0]})")

    if errors or len(series_out) != len(instruments):
        sys.stderr.write("FETCH FAILED — keeping previous funding_market.json\n" +
                         "\n".join(errors) + "\n")
        return 1

    history = DATA / 'credit-monitor' / 'market-history'
    history.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        previous = json.loads(OUT.read_text(encoding='utf-8'))
        stamp = previous.get('fetched_at', 'unknown').replace(':', '-')
        archive = history / (stamp + '.json')
        if not archive.exists():
            archive.write_text(json.dumps(previous, indent=1), encoding='utf-8')
    temporary = OUT.with_suffix('.tmp')
    temporary.write_text(json.dumps({
        "fetched_at": dt.datetime.now().isoformat(timespec="seconds"),
        "start": str(start), "end": str(end),
        "series": series_out, "errors": errors,
    }, indent=1), encoding="utf-8")
    temporary.replace(OUT)
    print(f"-> {OUT}  ({len(series_out)} series{', ' + str(len(errors)) + ' errors' if errors else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
