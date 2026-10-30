#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
credit_workbook.py — the OFFICIAL AI-credit base: Daniel Grozdea's AI_Credit_Live.xlsx as a data layer.

Felipe, 2026-10-16: "use o arquivo do Daniel como nossa base de crédito pra frente; todos os reports podem sair
dele, mantenha ele atualizado, e sobe ele como o oficial para o dashboard de crédito."

The workbook (layout = Barclays IG/HY Data Center Comp Sheets, 16-Sep-2026) holds live =BDP() formulas:
  Monitor            27 data-center project bonds (7 IG + 18 HY) + 2 tenant/parent comps (CRWV 9.75% 2031, ORCL 4.95% 2031)
  Other Instruments  NVDA / AVGO / AMD / SpaceX senior notes, neocloud & miner converts and HY, loans, tenant comparator bonds
  CDS                CDS_FLAT_SPREAD of AVGO / AMD / SPCX / NVDA / ORCL / META / GOOGL / MSFT / AMZN and the CRWV 1-10Y curve
  Equities           issuer + tenant equities with relative volume
  Terms & Lease / Financials / Since Barclays   static Barclays figures (15-Sep) per bond
  Deal Index + one dossier tab per bond          sourced term sheets (SEC filings, indentures, releases) with open gaps

What this module does
  --import <xlsx>   parse the workbook (openpyxl, cached values) -> _data/credit_workbook.json (canonical), copy the file to
                    _data/credit-monitor/workbook/AI_Credit_Live.xlsx (the official copy), write the dossiers as a dated
                    Capstone briefing in _briefings/<year>/ so the corpus can search them, append the day's values to history.
  --refresh         re-pull the SAME Bloomberg fields the workbook uses (PX_LAST, YLD_YTM_MID, OAS_SPREAD_MID, CHG_PCT_1D,
                    CDS_FLAT_SPREAD, VOLUME ...) through the local Desktop API for every ticker in the JSON, recompute the
                    derived columns exactly as the sheet does (principal vs par, change since 15-Sep, pickup vs tenant comp),
                    append to history. Fail-soft: a blocked / absent terminal keeps the previous values and says so.
                    The xlsx itself is never written (its formulas are live when opened in Excel with the add-in).
  --print           the brief block (what the weekly e-mail and the alerts e-mail embed)

Bases (never mixed): bond price in points of par, yield = YLD_YTM_MID in %, spread = OAS_SPREAD_MID in bp, CDS = CDS_FLAT_SPREAD
in bp (NOT the PX_LAST series of the issuer board — different basis), equities in % and x relative volume. Barclays yields are
YTW, live yields YTM: changes since 15-Sep are approximate (workbook caveat kept).

stdlib + openpyxl (import only) + the local Bloomberg wrapper (refresh only).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
JSON_PATH = DATA / "credit_workbook.json"
WB_DIR = DATA / "credit-monitor" / "workbook"
OFFICIAL = WB_DIR / "AI_Credit_Live.xlsx"
HISTORY = WB_DIR / "history.jsonl"
SNAPSHOTS = WB_DIR / "snapshots"
BRIEFINGS = ROOT / "_briefings"

SOURCE_LABEL = ("AI_Credit_Live.xlsx — Daniel Grozdea (Capstone), live Bloomberg workbook; layout per Barclays IG/HY Data Center "
                "Comp Sheets (16-Sep-2026); CDS comparison dates follow the imported column headings")

BOND_FIELDS = ["PX_LAST", "CHG_PCT_1D", "YLD_YTM_MID", "OAS_SPREAD_MID", "PX_CLOSE_1D", "TRACE_LAST_TRADE_SIZE", "PRICE_LAST_TIME"]
CDS_FIELDS = ["CDS_FLAT_SPREAD"]
EQ_FIELDS = ["PX_LAST", "CHG_PCT_1D", "VOLUME", "VOLUME_AVG_30D", "LAST_TRADE_TIME"]

# workbook thresholds (Monitor notes row): amber yield >= 10 %, pink = yield up >= 25bp since 15-Sep, relative volume amber >= 1.5x
YIELD_LINE = 10.0
PINK_BP = 25.0
RELVOL_LINE = 1.5


# ----------------------------------------------------------------------------- small helpers
def _num(v):
    """Cell value -> float or None (Bloomberg error strings, blanks, text -> None)."""
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) if math.isfinite(float(v)) else None
    if isinstance(v, str):
        s = v.strip().replace(",", "")
        if not s or s.startswith("#"):
            return None
        try:
            return float(s)
        except ValueError:
            return None
    return None


def _txt(v):
    if v is None:
        return None
    if isinstance(v, dt.datetime):
        return v.date().isoformat()
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, float) and math.isfinite(v) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _date(v):
    if isinstance(v, dt.datetime):
        return v.date().isoformat()
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}", v):
        return v[:10]
    return None


def _r(v, n=3):
    return None if v is None else round(v, n)


def is_block(exc):
    text = f"{type(exc).__name__}: {exc}"
    return any(k in text for k in ("WORKFLOW_REVIEW", "LIMIT /", "Workflow review"))


def load():
    try:
        return json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# ----------------------------------------------------------------------------- parse (import)
def _rows(ws, first=5):
    for i, r in enumerate(ws.iter_rows(min_row=first, max_row=ws.max_row, values_only=True), first):
        yield i, list(r) + [None] * (26 - len(r))


def _section_name(a):
    a = (a or "").strip()
    if a.startswith("Investment Grade"):
        return "IG"
    if a.startswith("High Yield"):
        return "HY"
    if a.startswith("Tenant / parent"):
        return "Parent"
    return a


def parse_monitor(wb):
    ws, wsf = wb["Monitor"], wb.formulas["Monitor"]
    bonds, totals, section = [], {}, None
    for i, r in _rows(ws):
        a = r[0]
        if a is None:
            continue
        if r[1] is None and r[6] is None:
            if str(a).startswith("Notes:"):
                continue
            section = _section_name(a)
            continue
        if str(a).endswith(" total"):
            totals[str(a).split()[0]] = {"face_mn": _num(r[6]), "wavg_price": _num(r[7]), "par_mn": _num(r[12]),
                                        "par_pct": _num(r[13]), "since_sep_mn": _num(r[15])}
            continue
        comp_ticker = None
        f = wsf.cell(row=i, column=22).value  # V: =_xll.BDP("NVDA 4.95 06/15/36 Corp","OAS_SPREAD_MID")
        if isinstance(f, str):
            m = re.search(r'BDP\("([^"]+)"', f)
            comp_ticker = m.group(1) if m else None
        bonds.append({
            "ticker": _txt(r[1]), "name": _txt(a), "section": section, "tenant": _txt(r[2]), "location": _txt(r[3]),
            "mw": _num(r[4]), "rating": _txt(r[5]), "amt_mn": _num(r[6]),
            "px": _num(r[7]), "chg_pct_1d": _num(r[8]), "yld": _num(r[9]), "trace_size": _txt(r[10]), "px_time": _txt(r[11]),
            "par_mn": _num(r[12]), "par_pct": _num(r[13]), "chg_value_mn": _num(r[14]), "since_sep_mn": _num(r[15]),
            "dyld_since_sep_bp": _num(r[16]), "barclays_rec": _txt(r[17]), "first_issued": _date(r[18]),
            "oas_bp": _num(r[19]), "comp_name": _txt(r[20]), "comp_oas_bp": _num(r[21]), "pickup_bp": _num(r[22]),
            "pickup_sep_bp": _num(r[23]), "pickup_chg_bp": _num(r[24]), "bbg": _txt(r[25]), "comp_bbg": comp_ticker,
        })
    return bonds, totals


def parse_keyed(wb, name, cols):
    """Static Barclays sheets keyed by ticker (column B)."""
    out = {}
    for i, r in _rows(wb[name]):
        tk = _txt(r[1])
        if not tk or r[0] is None or str(r[0]).endswith(" total"):
            continue
        out[tk] = {k: (f(r[c]) if f else _txt(r[c])) for k, (c, f) in cols.items()}
    return out


def parse_other(wb):
    ws = wb["Other Instruments"]
    snap_ref = None
    m = re.search(r"Snapshot reference:\s*([\w-]+)", str(ws["A2"].value or ""))
    if m:
        snap_ref = m.group(1)
    rows, group = [], None
    for i, r in _rows(ws):
        if r[0] is None:
            continue
        if r[1] is None and r[15] is None:
            group = _txt(r[0])
            continue
        rows.append({"name": _txt(r[0]), "group": _txt(r[1]) or group, "amt_mn": _num(r[2]), "px": _num(r[3]), "chg_pct_1d": _num(r[4]),
                     "yld": _num(r[5]), "trace_size": _txt(r[6]), "px_time": _txt(r[7]), "par_mn": _num(r[8]), "par_pct": _num(r[9]),
                     "chg_value_mn": _num(r[10]), "yld_snapshot": _num(r[11]), "dyld_vs_snapshot_bp": _num(r[12]),
                     "rating_sp": _txt(r[13]), "isin": _txt(r[14]), "bbg": _txt(r[15]),
                     "kind": ("loan" if str(r[15] or "").startswith("BL") else "convertible" if "(cv" in str(r[0]) else "bond")})
    return rows, snap_ref


def parse_cds(wb):
    ws = wb["CDS"]
    headers = next(ws.iter_rows(min_row=4, max_row=4, values_only=True))
    dates = next(ws.iter_rows(min_row=3, max_row=3, values_only=True))
    return parse_cds_table(headers, (r for _, r in _rows(ws)), dates)


def parse_cds_table(headers, data_rows, dates=()):
    """Read labeled columns; daily closes must never become old desk marks."""
    heads = [str(h or "").strip().lower() for h in headers]
    def col(*labels):
        return next((i for i, h in enumerate(heads) if h in labels), None)
    name, ticker = col("name"), col("bloomberg ticker")
    current = col("last", "live (bp)", "live flat spread (bp)", "flat spread (bp)")
    previous = col("prev close (bp)")
    snapshot = next((i for i, h in enumerate(heads) if "snapshot" in h and not h.startswith(("δ", "Δ", "chg", "change"))), None)
    desk = next((i for i, h in enumerate(heads) if "ms" in h and "24" in h and not h.startswith(("δ", "Δ", "chg", "change"))), None)
    if name is None or ticker is None or current is None or (previous is None and snapshot is None and desk is None):
        raise ValueError("Unrecognized CDS column headings; refusing a positional import")
    def value(row, index):
        return row[index] if index is not None and index < len(row) else None
    def cached_date(index):
        v = value(dates, index)
        if isinstance(v, (int, float)):
            return (dt.date(1899, 12, 30) + dt.timedelta(days=int(v))).isoformat()
        return _date(v)
    rows = []
    for r in data_rows:
        if not value(r, ticker):
            continue
        row = {"name": _txt(value(r, name)), "bbg": _txt(value(r, ticker)),
               "spread_bp": _num(value(r, current)),
               "spread_snapshot_bp": _num(value(r, snapshot)),
               "ms_desk_0824_bp": _num(value(r, desk)),
               "cds_layout": "daily-closes-v2" if previous is not None else "dated-baselines-v1"}
        if previous is not None:
            basis = _txt(value(r, col("column c source")))
            row["cached_quote"] = {"value_bp": row["spread_bp"], "basis": basis,
                "last_update": _txt(value(r, col("last update (time, else curve date)"))),
                "previous_close_bp": _num(value(r, previous)), "previous_close_date": cached_date(previous),
                "daily_change_bp": _num(value(r, col("chg day / day")))}
            # Column C can be CBIN PX_MID, which is not CDS_FLAT_SPREAD.
            if basis != "Flat spread (EOD close)":
                row["spread_bp"] = None
        derive_cds(row)
        rows.append(row)
    return rows


def derive_cds(row):
    for base, delta in (("spread_snapshot_bp", "d_snapshot_bp"), ("ms_desk_0824_bp", "d_vs_ms_bp")):
        a, b = row.get("spread_bp"), row.get(base)
        row[delta] = _r(a - b, 2) if a is not None and b is not None else None


def cds_tenor(row):
    match = re.search(r"\b(\d+)Y\b", row.get("bbg") or row.get("name") or "")
    return int(match.group(1)) if match else None


def parse_equities(wb):
    rows = []
    for i, r in _rows(wb["Equities"]):
        if not r[2]:
            continue
        rows.append({"name": _txt(r[0]), "why": _txt(r[1]), "bbg": _txt(r[2]), "px": _num(r[3]), "chg_pct_1d": _num(r[4]),
                     "volume": _num(r[5]), "vol_avg_30d": _num(r[6]), "relvol": _num(r[7]), "time": _txt(r[8])})
    return rows


def parse_deal_index(wb):
    rows = []
    for i, r in _rows(wb["Deal Index"]):
        if not r[0] or r[0] == "Ticker":
            continue
        rows.append({"ticker": _txt(r[0]), "bond": _txt(r[1]), "section": _txt(r[2]), "sources": _num(r[3]),
                     "official_sources": _num(r[4]), "open_gaps": _num(r[5]), "headline": _txt(r[6])})
    return rows


def parse_dossier(ws):
    """One dossier tab -> {title, asof, isin, metrics, sections:[{name, items:[{label,text,source,status}]}], timeline, sources, gaps}."""
    d = {"title": _txt(ws["A1"].value), "asof": None, "isin": None, "metrics": {}, "headline": None, "sections": [],
         "timeline": [], "sources": [], "gaps": []}
    m = re.search(r"as of (\d{4}-\d{2}-\d{2})", str(ws["A2"].value or ""))
    if m:
        d["asof"] = m.group(1)
    m = re.search(r"ISIN\s+(\S+)", str(ws["A2"].value or "") + " " + str(ws["B2"].value or ""))
    if m:
        d["isin"] = m.group(1)
    mode, cur = "metrics", None
    for i in range(3, ws.max_row + 1):
        a, b, c, e = (ws.cell(row=i, column=k).value for k in (1, 2, 3, 4))
        if a is None and b is None:
            continue
        at = _txt(a) or ""
        if at.startswith("Sources (") or at == "Sources":
            mode = "sources"; continue
        if at.startswith("Not found"):
            mode = "gaps"; continue
        if at == "Timeline":
            mode = "timeline"; continue
        if at == "Summary":
            mode = "summary"; continue
        if mode == "sources":
            # 'S1 | Indenture | 2026-06-10' in A, description in B, 'link' (hyperlink) in C
            ms = re.match(r"^(S\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*)$", at)
            if ms:
                link = ws.cell(row=i, column=3)
                d["sources"].append({"id": ms.group(1), "type": ms.group(2).strip(), "date": ms.group(3).strip(), "text": _txt(b),
                                     "url": (link.hyperlink.target if link.hyperlink else None)})
            continue
        if mode == "gaps":
            if b:
                d["gaps"].append(_txt(b))
            continue
        if mode == "timeline":
            if a is not None and b:
                d["timeline"].append({"date": _date(a) or at, "text": _txt(b), "source": _txt(c)})
            continue
        if mode == "summary":
            if at == "Headline":
                d["headline"] = _txt(b)
            elif b is None and c in (None, "Source"):
                mode = "sections"; cur = {"name": at, "items": []}; d["sections"].append(cur)
            continue
        if mode == "metrics":
            if b is not None:
                d["metrics"][at] = _txt(b) if not isinstance(b, (int, float)) else _num(b)
            continue
        # sections
        if b is None and (c in (None, "Source")):
            cur = {"name": at, "items": []}; d["sections"].append(cur)
        elif cur is not None and b is not None:
            cur["items"].append({"label": at, "text": _txt(b), "source": _txt(c), "status": _txt(e)})
    return d


def parse_workbook(path: Path):
    import openpyxl  # noqa: WPS433 — import-time only; the refresh path is stdlib + the Bloomberg wrapper
    wb = openpyxl.load_workbook(path, data_only=True)
    wb.formulas = openpyxl.load_workbook(path, data_only=False)
    bonds, totals = parse_monitor(wb)
    terms = parse_keyed(wb, "Terms & Lease", {
        "next_call": (4, None), "call_px": (5, _num), "px_to_call_pts": (6, _num), "amort_start": (7, None),
        "amort_before_mty_pct": (8, _num), "comp_bond": (9, None), "comp_spread_bp": (10, _num), "lease_type": (11, None),
        "lease_tenor": (12, None), "construction_start": (13, None), "lease_commencement": (14, None), "barclays_spread_sep_bp": (15, _num)})
    fin = parse_keyed(wb, "Financials", {
        "facility_cost_mn": (6, _num), "cost_per_mw_mn": (7, _num), "base_rent_per_mw_mn": (8, _num), "escalator": (9, None),
        "pct_debt_financed": (10, _num), "gross_lev_issuance_x": (11, _num), "gross_lev_maturity_x": (12, _num),
        "rent_yield_on_cost": (13, _num), "debt_per_mw_mn": (14, _num), "mw": (15, _num)})
    since = parse_keyed(wb, "Since Barclays", {
        "px_0803": (3, _num), "ytw_0803": (4, _num), "spread_0803_bp": (5, _num), "px_0915": (6, _num), "ytw_0915": (7, _num),
        "spread_0915_bp": (8, _num)})
    for b in bonds:
        b["terms"] = terms.get(b["ticker"], {})
        b["financials"] = fin.get(b["ticker"], {})
        b["barclays"] = since.get(b["ticker"], {})
    other, snap_ref = parse_other(wb)
    cds = parse_cds(wb)
    eq = parse_equities(wb)
    deal_index = parse_deal_index(wb)
    dossiers = {}
    for row in deal_index:
        if row["ticker"] in wb.sheetnames:
            dossiers[row["ticker"]] = parse_dossier(wb[row["ticker"]])
    asof = max((d.get("asof") or "" for d in dossiers.values()), default=None) or None
    readme = [str(c.value) for (c,) in wb["README"].iter_rows(min_col=1, max_col=1) if c.value]
    return {"bonds": bonds, "totals": totals, "other": other, "snapshot_ref": snap_ref, "cds": cds, "equities": eq,
            "deal_index": deal_index, "dossiers": dossiers, "asof": asof, "readme": readme,
            "notes": {"monitor": _txt(wb["Monitor"]["A38"].value), "other": _txt(wb["Other Instruments"]["A2"].value),
                      "cds": _txt(wb["CDS"]["A2"].value), "equities": _txt(wb["Equities"]["A2"].value)}}


# ----------------------------------------------------------------------------- derived columns (exactly the sheet's arithmetic)
def _derive_bond(b):
    px, amt = b.get("px"), b.get("amt_mn")
    if px is not None and amt is not None:
        b["par_mn"] = _r((px - 100) / 100 * amt)
        b["par_pct"] = _r((px - 100) / 100, 5)
        if b.get("px_close_1d") is not None:
            b["chg_value_mn"] = _r((px - b["px_close_1d"]) / 100 * amt)
        p15 = (b.get("barclays") or {}).get("px_0915")
        if p15 is not None:
            b["since_sep_mn"] = _r((px - p15) / 100 * amt)
    y15 = (b.get("barclays") or {}).get("ytw_0915")
    if b.get("yld") is not None and y15 is not None:
        b["dyld_since_sep_bp"] = _r((b["yld"] - y15) * 100, 2)
    if b.get("oas_bp") is not None and b.get("comp_oas_bp") is not None:
        b["pickup_bp"] = _r(b["oas_bp"] - b["comp_oas_bp"], 2)
        if b.get("pickup_sep_bp") is not None:
            b["pickup_chg_bp"] = _r(b["pickup_bp"] - b["pickup_sep_bp"], 2)


def _derive_other(o):
    px, amt = o.get("px"), o.get("amt_mn")
    if px is not None and amt is not None:
        o["par_mn"] = _r((px - 100) / 100 * amt)
        o["par_pct"] = _r((px - 100) / 100, 5)
        if o.get("px_close_1d") is not None:
            o["chg_value_mn"] = _r((px - o["px_close_1d"]) / 100 * amt)
    if o.get("yld") is not None and o.get("yld_snapshot") is not None:
        o["dyld_vs_snapshot_bp"] = _r((o["yld"] - o["yld_snapshot"]) * 100, 2)


def _totals(bonds):
    out = {}
    for sec in ("IG", "HY"):
        rows = [b for b in bonds if b["section"] == sec and b.get("amt_mn")]
        face = sum(b["amt_mn"] for b in rows)
        priced = [b for b in rows if b.get("px") is not None]
        wavg = sum(b["px"] * b["amt_mn"] for b in priced) / sum(b["amt_mn"] for b in priced) if priced else None
        par = sum(b["par_mn"] for b in rows if b.get("par_mn") is not None)
        out[sec] = {"n": len(rows), "face_mn": _r(face, 1), "wavg_price": _r(wavg), "par_mn": _r(par, 1),
                    "par_pct": _r(par / face, 5) if face else None,
                    "since_sep_mn": _r(sum(b["since_sep_mn"] for b in rows if b.get("since_sep_mn") is not None), 1)}
    return out


# ----------------------------------------------------------------------------- history
def history_rows(wb, when):
    date, time = when[:10], when[11:16]
    src = wb.get("values_source_key", "xlsx")
    for b in wb["bonds"]:
        yield {"date": date, "time": time, "src": src, "kind": "bond", "id": b["bbg"], "tk": b["ticker"], "px": b.get("px"),
               "yld": b.get("yld"), "oas": b.get("oas_bp"), "chg1d": b.get("chg_pct_1d")}
    for o in wb["other"]:
        yield {"date": date, "time": time, "src": src, "kind": "other", "id": o["bbg"], "tk": o["name"], "px": o.get("px"),
               "yld": o.get("yld"), "chg1d": o.get("chg_pct_1d")}
    for c in wb["cds"]:
        yield {"date": date, "time": time, "src": src, "kind": "cds", "id": c["bbg"], "tk": c["name"], "spread": c.get("spread_bp")}
    for e in wb["equities"]:
        yield {"date": date, "time": time, "src": src, "kind": "equity", "id": e["bbg"], "tk": e["name"], "px": e.get("px"),
               "chg1d": e.get("chg_pct_1d"), "relvol": e.get("relvol")}


def append_history(wb, when):
    WB_DIR.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as fh:
        for row in history_rows(wb, when):
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_history():
    """{id: {date: row}} — last row per (id, date) wins."""
    out = {}
    if not HISTORY.exists():
        return out
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        out.setdefault(row["id"], {})[row["date"]] = row
    return out


def previous_obs(hist, iid, before_date):
    days = hist.get(iid, {})
    prior = sorted(d for d in days if d < before_date)
    return days[prior[-1]] if prior else None


# ----------------------------------------------------------------------------- import
def do_import(path: Path, when=None):
    when = when or dt.datetime.now().isoformat(timespec="minutes")
    parsed = parse_workbook(path)
    wb = {"source": SOURCE_LABEL, "source_file": path.name, "imported_at": when, "imported_from": str(path),
          "official_copy": str(OFFICIAL.relative_to(ROOT)).replace("\\", "/"),
          "values_source": "workbook cached values (last Excel recalculation with the Bloomberg add-in)",
          "values_source_key": "xlsx", "values_asof": parsed["asof"], "refreshed_at": None, "refresh": {"status": "not-run"},
          **parsed}
    wb["totals"] = {**_totals(wb["bonds"]), "sheet": parsed["totals"]}
    WB_DIR.mkdir(parents=True, exist_ok=True)
    if path.resolve() != OFFICIAL.resolve():
        shutil.copy2(path, OFFICIAL)
    JSON_PATH.write_text(json.dumps(wb, ensure_ascii=False, indent=1), encoding="utf-8")
    append_history(wb, when)
    write_snapshot(wb, when[:10])
    md = write_dossiers_md(wb)
    print(f"imported {path.name}: {len(wb['bonds'])} monitor bonds, {len(wb['other'])} other instruments, {len(wb['cds'])} CDS, "
          f"{len(wb['equities'])} equities, {len(wb['dossiers'])} dossiers; values asof {wb['values_asof']} (xlsx cache)")
    print(f"  official copy -> {OFFICIAL}\n  canonical json -> {JSON_PATH}\n  dossiers briefing -> {md}")
    return wb


def write_snapshot(wb, date):
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    slim = {k: wb[k] for k in ("values_source", "values_asof", "refreshed_at", "refresh", "totals", "bonds", "other", "cds", "equities")}
    (SNAPSHOTS / f"{date}.json").write_text(json.dumps(slim, ensure_ascii=False, indent=1), encoding="utf-8")


def write_dossiers_md(wb):
    asof = wb.get("values_asof") or dt.date.today().isoformat()
    out = BRIEFINGS / asof[:4] / f"{asof}-ai-credit-live-workbook-dossiers.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    L = [f"# AI data-center credit — deal dossiers from AI_Credit_Live.xlsx (Daniel Grozdea) — as of {asof}", "",
         f"_Source: **{SOURCE_LABEL}** · dossiers as of {asof} · official copy `{wb['official_copy']}` · canonical data "
         f"`_wiki/_data/credit_workbook.json` · search kind `briefing`._", "",
         "**Attribution for datapoints taken from this file:** \"Daniel Grozdea (Capstone) AI_Credit_Live.xlsx dossier <TICKER>, "
         f"as of {asof} — <source id> (<document type>, <date>)\". Each dossier line carries its own source id and a status "
         "(verified (official doc) / company statement / third party / seed, unverified / estimate). **'Seed, unverified' lines are "
         "Barclays comp-sheet leads, not verified facts.** Market levels in this file are the day's live composite quotes — use the "
         "dashboard / `credit_workbook.json` for current levels, never this file.", "",
         "## Deal index", "", "| Ticker | Bond | Section | Sources (official) | Open gaps | Headline |", "|---|---|---|---|---|---|"]
    for r in wb["deal_index"]:
        L.append(f"| {r['ticker']} | {r['bond']} | {r['section']} | {int(r['sources'] or 0)} ({int(r['official_sources'] or 0)}) | "
                 f"{int(r['open_gaps'] or 0)} | {r['headline']} |")
    for tk, d in wb["dossiers"].items():
        L += ["", f"## {tk} — {d['title']}", ""]
        if d.get("headline"):
            L.append(f"**Headline:** {d['headline']}")
        if d.get("isin"):
            L.append(f"ISIN {d['isin']}")
        for sec in d["sections"]:
            L += ["", f"### {sec['name']}", ""]
            for it in sec["items"]:
                L.append(f"- **{it['label']}** — {it['text']} _[{it['source'] or '—'} · {it['status'] or '—'}]_")
        if d["timeline"]:
            L += ["", "### Timeline", ""]
            for t in d["timeline"]:
                L.append(f"- {t['date']} — {t['text']} _[{t['source'] or '—'}]_")
        if d["sources"]:
            L += ["", "### Sources", ""]
            for s in d["sources"]:
                L.append(f"- {s['id']} · {s['type']} · {s['date']} — {s['text']}" + (f" — {s['url']}" if s.get("url") else ""))
        if d["gaps"]:
            L += ["", "### Not found / could not verify", ""]
            for g in d["gaps"]:
                L.append(f"- {g}")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


# ----------------------------------------------------------------------------- refresh (local Bloomberg API)
def _bdp_map(bdp, tickers, fields):
    """{ticker: {field: value}} for one batch; raises on a blocked terminal."""
    df = bdp(tickers, fields)
    cols = {c.lower(): c for c in df.columns}
    out = {}
    for _, r in df.iterrows():
        val = r[cols["value"]]
        if val is None or (isinstance(val, float) and not math.isfinite(val)):
            continue
        out.setdefault(r[cols["ticker"]], {})[r[cols["field"]]] = val
    return out


def _batches(seq, n=40):
    seq = list(dict.fromkeys(t for t in seq if t))
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def do_refresh(when=None):
    wb = load()
    if not wb:
        raise SystemExit("credit_workbook.json missing — run --import <AI_Credit_Live.xlsx> first")
    when = when or dt.datetime.now().isoformat(timespec="minutes")
    sys.path.insert(0, r"E:\bloomberg_api")
    status = {"status": "ok", "detail": "", "at": when, "missing": []}
    try:
        from bloomberg import bdp
    except Exception as exc:  # wrapper import failure = no terminal this run
        status = {"status": "unavailable", "detail": f"{type(exc).__name__}: {exc}"[:300], "at": when, "missing": []}
        return _finish(wb, status, when, changed=False)
    bond_tk = [b["bbg"] for b in wb["bonds"]] + [b["comp_bbg"] for b in wb["bonds"]] + [o["bbg"] for o in wb["other"]]
    got = {}
    try:
        for batch in _batches(bond_tk):
            got.update(_bdp_map(bdp, batch, BOND_FIELDS))
        for batch in _batches([c["bbg"] for c in wb["cds"]]):
            got.update(_bdp_map(bdp, batch, CDS_FIELDS))
        for batch in _batches([e["bbg"] for e in wb["equities"]]):
            got.update(_bdp_map(bdp, batch, EQ_FIELDS))
    except Exception as exc:
        kind = "blocked" if is_block(exc) else "error"
        status = {"status": kind, "detail": f"{type(exc).__name__}: {exc}"[:300], "at": when, "missing": []}
        return _finish(wb, status, when, changed=False)

    def take(row, tk, mapping):
        vals = got.get(tk)
        if not vals:
            status["missing"].append(tk); row["stale"] = True; return
        row["stale"] = False
        for key, fld in mapping.items():
            if fld in vals:
                v = vals[fld]
                row[key] = _txt(v) if key in ("trace_size", "px_time", "time") else _num(v)

    bmap = {"px": "PX_LAST", "chg_pct_1d": "CHG_PCT_1D", "yld": "YLD_YTM_MID", "oas_bp": "OAS_SPREAD_MID",
            "px_close_1d": "PX_CLOSE_1D", "trace_size": "TRACE_LAST_TRADE_SIZE", "px_time": "PRICE_LAST_TIME"}
    for b in wb["bonds"]:
        take(b, b["bbg"], bmap)
        comp = got.get(b.get("comp_bbg") or "", {})
        if "OAS_SPREAD_MID" in comp:
            b["comp_oas_bp"] = _num(comp["OAS_SPREAD_MID"])
        _derive_bond(b)
    for o in wb["other"]:
        take(o, o["bbg"], {"px": "PX_LAST", "chg_pct_1d": "CHG_PCT_1D", "yld": "YLD_YTM_MID", "px_close_1d": "PX_CLOSE_1D",
                           "trace_size": "TRACE_LAST_TRADE_SIZE", "px_time": "PRICE_LAST_TIME"})
        _derive_other(o)
    for c in wb["cds"]:
        take(c, c["bbg"], {"spread_bp": "CDS_FLAT_SPREAD"})
        derive_cds(c)
    for e in wb["equities"]:
        take(e, e["bbg"], {"px": "PX_LAST", "chg_pct_1d": "CHG_PCT_1D", "volume": "VOLUME", "vol_avg_30d": "VOLUME_AVG_30D", "time": "LAST_TRADE_TIME"})
        if e.get("volume") and e.get("vol_avg_30d"):
            e["relvol"] = _r(e["volume"] / e["vol_avg_30d"])
    wb["totals"] = {**_totals(wb["bonds"]), "sheet": wb["totals"].get("sheet", {})}
    if status["missing"]:
        status["missing"] = list(dict.fromkeys(status["missing"]))
        status["status"] = "partial"
        status["detail"] = f"{len(status['missing'])} instrument(s) returned no values — previous values kept"
    return _finish(wb, status, when, changed=True)


def _finish(wb, status, when, changed):
    wb["refresh"] = status
    if changed:
        wb["values_source"] = "Bloomberg Desktop API bdp (local terminal): workbook bond/equity fields and CDS_FLAT_SPREAD (not CBIN PX_MID) — composite snapshot"
        wb["values_source_key"] = "bbg-api"
        wb["values_asof"] = when[:10]
        wb["refreshed_at"] = when
        append_history(wb, when)
        write_snapshot(wb, when[:10])
    JSON_PATH.write_text(json.dumps(wb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"workbook refresh {status['status']}" + (f" — {status['detail']}" if status.get("detail") else "")
          + (f" · values asof {wb['values_asof']} ({wb['values_source_key']})" if changed else " · previous values kept"))
    return wb


# ----------------------------------------------------------------------------- brief (shared by the weekly e-mail and the alerts e-mail)
def _f(v, n=2, suf=""):
    return "—" if v is None else f"{v:,.{n}f}{suf}"


def brief_lines(wb=None):
    wb = wb or load()
    if not wb:
        return ["- Official workbook (AI_Credit_Live.xlsx): not imported yet — run credit_workbook.py --import."]
    T = wb["totals"]
    L = [f"PROJECT-BOND UNIVERSE — official workbook AI_Credit_Live.xlsx (Daniel Grozdea; Barclays comp-sheet layout, 16-Sep-2026)",
         f"Values: {wb['values_source']} · asof {wb['values_asof']}" + (f" (refreshed {wb['refreshed_at']})" if wb.get("refreshed_at") else "")
         + (f" · refresh {wb['refresh']['status']}: {wb['refresh'].get('detail', '')}" if wb.get("refresh", {}).get("status") not in ("ok", None) else "")]
    for sec, lab in (("IG", "IG builders"), ("HY", "HY builders")):
        t = T.get(sec) or {}
        L.append(f"- {lab}: {t.get('n')} bonds, face ${_f((t.get('face_mn') or 0) / 1000, 1)}bn, w-avg price {_f(t.get('wavg_price'))}, "
                 f"principal vs par ${_f((t.get('par_mn') or 0) / 1000, 2)}bn ({_f((t.get('par_pct') or 0) * 100, 1, '%')}), "
                 f"since 15-Sep ${_f((t.get('since_sep_mn') or 0) / 1000, 2)}bn.")
    hot = sorted((b for b in wb["bonds"] if b["section"] in ("IG", "HY") and (b.get("yld") or 0) >= YIELD_LINE), key=lambda b: -b["yld"])
    if hot:
        L.append("- Yields at or above the 10% line (MS: HY data-center deals get pulled near ~10%): "
                 + "; ".join(f"{b['ticker']} {b['yld']:.2f}% ({b['tenant']})" for b in hot) + ".")
    wid = sorted((b for b in wb["bonds"] if b["section"] in ("IG", "HY") and b.get("dyld_since_sep_bp") is not None), key=lambda b: -b["dyld_since_sep_bp"])[:5]
    if wid:
        L.append("- Widest yield change since Barclays 15-Sep (YTW→YTM, approximate): "
                 + "; ".join(f"{b['ticker']} {b['dyld_since_sep_bp']:+.0f}bp to {b['yld']:.2f}%" for b in wid) + ".")
    neg = [b for b in wb["bonds"] if (b.get("pickup_bp") or 0) < 0 and b["section"] in ("IG", "HY")]
    if neg:
        L.append("- Project bonds trading TIGHTER than the tenant's own unsecured comp (negative OAS pickup): "
                 + "; ".join(f"{b['ticker']} {b['pickup_bp']:+.0f}bp vs {b['comp_name']}" for b in neg) + ".")
    comps = [b for b in wb["bonds"] if b["section"] == "Parent"]
    if comps:
        L.append("- Tenant / parent comps: " + "; ".join(f"{b['name'].split(' Sr')[0]} px {_f(b['px'])} / {_f(b['yld'])}% / OAS {_f(b['oas_bp'], 0)}bp" for b in comps) + ".")
    crwv = sorted((c for c in wb["cds"] if c["name"].startswith("CRWV")), key=lambda c: cds_tenor(c) or 999)
    if crwv:
        L.append("- CRWV CDS curve (CDS_FLAT_SPREAD, bp): " + " · ".join(f"{c['name'].split()[-1]} {_f(c['spread_bp'], 0)}" for c in crwv) + ".")
    hyp = [c for c in wb["cds"] if cds_tenor(c) == 5]
    if hyp:
        L.append("- 5Y CDS (CDS_FLAT_SPREAD, bp): " + "; ".join(f"{c['name']} {_f(c['spread_bp'], 0)}" for c in hyp) + ".")
        paired = [c for c in hyp if c.get("d_vs_ms_bp") is not None]
        if paired:
            L.append("- 5Y CDS change vs MS desk 24-Aug-2026 (bp): " + "; ".join(f"{c['name']} {c['d_vs_ms_bp']:+.0f}" for c in paired) + ".")
        else:
            L.append("- CDS comparison gap: the current workbook has daily-close columns, not the earlier snapshot / MS 24-Aug marks. Those comparisons are unavailable. Cached daily closes retain their original dates and are not current quotes.")
    cv = [o for o in wb["other"] if o["name"].startswith("CRWV") and o["kind"] == "bond"]
    if cv:
        L.append("- CoreWeave straight bonds: " + "; ".join(f"{o['name']} px {_f(o['px'])} / {_f(o['yld'])}%" for o in cv) + ".")
    mov = sorted((e for e in wb["equities"] if e.get("chg_pct_1d") is not None), key=lambda e: e["chg_pct_1d"])[:5]
    if mov:
        L.append("- Equity tape (worst 1d, relative volume): " + "; ".join(f"{e['name']} {e['chg_pct_1d']:+.1f}% ({_f(e.get('relvol'), 1, 'x')})" for e in mov) + ".")
    L.append("- Bases: price in points of par; yield = YLD_YTM_MID %; spread = OAS_SPREAD_MID bp; CDS = CDS_FLAT_SPREAD bp (not the "
             "issuer board's PX_LAST series); Barclays 15-Sep levels are YTW. Static terms, financials and dossiers per bond: "
             "credit_workbook.json / dashboard section 'Data-center project bonds'.")
    return L


# ----------------------------------------------------------------------------- alerts (workbook layer for credit_alerts.py)
def workbook_alerts(wb=None, today=None, hist=None):
    """Rules on the workbook universe. Returns (rows, alerts) in credit_alerts' market-layer shape (ids 'WB_<ticker>')."""
    wb = wb or load()
    if not wb:
        return [], []
    today = today or (wb.get("values_asof") or dt.date.today().isoformat())
    hist = hist if hist is not None else read_history()
    src = wb.get("values_source", "")
    stale = wb.get("values_source_key") != "bbg-api" or wb.get("values_asof") != today
    rows, alerts = [], []

    def mk(iid, label, group, company, ticker, unit, last, d1=None, d5=None):
        return {"id": iid, "label": label, "group": group, "company": company, "ticker": ticker, "unit": unit,
                "alert_unit": "%" if group == "equity" else "bp", "status": "stale" if stale else "ok", "config_status": "workbook",
                "source": f"AI_Credit_Live.xlsx · {ticker}", "error": None, "n": None, "last": last, "last_date": wb.get("values_asof"),
                "prev_date": None, "d1": d1, "d5": d5, "sigma": None, "z1": None, "z5": None, "high_60d": False, "high_1y": False,
                "line_cross": None, "level_line": None, "workbook": True}

    def fire(row, sev, reasons, headline):
        alerts.append({"kind": "workbook", "id": row["id"], "company": row["company"], "group": row["group"], "severity": sev,
                       "headline": headline, "reasons": reasons, "last": row["last"], "last_date": row["last_date"], "d1": row["d1"],
                       "d5": row["d5"], "z1": None, "sigma": None, "alert_unit": row["alert_unit"], "ticker": row["ticker"],
                       "source": row["source"], "data_status": row["status"]})

    for b in wb["bonds"] + [dict(o, ticker=o["name"], section="Other", tenant=o["group"]) for o in wb["other"] if o["kind"] == "bond"]:
        iid = f"WB_{b['ticker']}".replace(" ", "_").replace("/", "-")
        prev = previous_obs(hist, b["bbg"], today)
        d1_yld = (b["yld"] - prev["yld"]) * 100 if prev and prev.get("yld") is not None and b.get("yld") is not None else None
        row = mk(iid, f"{b['ticker']} · {b['name'][:60]}", "bond", b.get("tenant") or b["ticker"], b["bbg"], "%", b.get("yld"), d1_yld)
        row["level_line"] = YIELD_LINE
        row["px"], row["chg_pct_1d"], row["dyld_since_sep_bp"] = b.get("px"), b.get("chg_pct_1d"), b.get("dyld_since_sep_bp")
        rows.append(row)
        if stale or b.get("stale") or b.get("yld") is None:
            continue
        reasons, score = [], 0
        y = b["yld"]
        crossed = prev and prev.get("yld") is not None and prev["yld"] < YIELD_LINE <= y
        if crossed:
            score = 3; reasons.append(f"crossed the {YIELD_LINE:.0f}% yield line ({prev['yld']:.2f}% on {prev['date']} → {y:.2f}%)")
        if d1_yld is not None and d1_yld >= 75:
            score = max(score, 3); reasons.append(f"yield {d1_yld:+.0f}bp since {prev['date']}")
        elif d1_yld is not None and d1_yld >= 40:
            score = max(score, 2); reasons.append(f"yield {d1_yld:+.0f}bp since {prev['date']}")
        c1 = b.get("chg_pct_1d")
        if c1 is not None and c1 <= -5:
            score = max(score, 3); reasons.append(f"price {c1:+.1f}% on the day (composite)")
        elif c1 is not None and c1 <= -3:
            score = max(score, 2); reasons.append(f"price {c1:+.1f}% on the day (composite)")
        if score:
            sev = {1: "low", 2: "medium", 3: "high"}[score]
            fire(row, sev, reasons, f"{b['ticker']} ({b.get('tenant') or 'n/a'}) {y:.2f}% / px {_f(b.get('px'))} ({today})")

    for c in wb["cds"]:
        iid = f"WB_CDS_{c['name'].replace(' ', '_')}"
        prev = previous_obs(hist, c["bbg"], today)
        d1 = c["spread_bp"] - prev["spread"] if prev and prev.get("spread") is not None and c.get("spread_bp") is not None else None
        row = mk(iid, f"{c['name']} (flat spread)", "cds", c["name"].split()[0], c["bbg"], "bp", c.get("spread_bp"), d1)
        rows.append(row)
        if stale or c.get("stale") or d1 is None:
            continue
        big = c["name"].startswith("CRWV")
        hi, md = (150, 50) if big else (75, 25)
        if d1 >= hi:
            fire(row, "high", [f"{d1:+.0f}bp since {prev['date']}"], f"{c['name']} {c['spread_bp']:,.0f}bp ({today})")
        elif d1 >= md:
            fire(row, "medium", [f"{d1:+.0f}bp since {prev['date']}"], f"{c['name']} {c['spread_bp']:,.0f}bp ({today})")

    for e in wb["equities"]:
        iid = f"WB_EQ_{e['bbg'].split()[0]}"
        row = mk(iid, f"{e['name']} equity", "equity", e["name"], e["bbg"], "", e.get("px"), e.get("chg_pct_1d"))
        row["relvol"] = e.get("relvol")
        rows.append(row)
        if stale or e.get("stale") or e.get("chg_pct_1d") is None:
            continue
        c1, rv = e["chg_pct_1d"], e.get("relvol") or 0
        if c1 <= -15 or (c1 <= -10 and rv >= 2.0):
            fire(row, "high", [f"{c1:+.1f}% on {rv:.1f}x 30d volume"], f"{e['name']} {c1:+.1f}% ({today})")
        elif c1 <= -10 or (c1 <= -7 and rv >= RELVOL_LINE):
            fire(row, "medium", [f"{c1:+.1f}% on {rv:.1f}x 30d volume"], f"{e['name']} {c1:+.1f}% ({today})")
    return rows, alerts


# ----------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--import", dest="imp", metavar="XLSX", help="parse this workbook as the official base (copies it)")
    ap.add_argument("--refresh", action="store_true", help="re-pull the workbook's Bloomberg fields through the local API")
    ap.add_argument("--print", dest="prt", action="store_true", help="print the brief block")
    ap.add_argument("--alerts", action="store_true", help="evaluate the workbook alert rules and print them")
    a = ap.parse_args()
    if a.imp:
        do_import(Path(a.imp))
    if a.refresh:
        do_refresh()
    if a.prt or not (a.imp or a.refresh or a.alerts):
        print("\n".join(brief_lines()))
    if a.alerts:
        rows, alerts = workbook_alerts()
        print(json.dumps({"rows": len(rows), "alerts": alerts}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
