#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fetch_credit_watch.py — daily history for the AI credit alert watch list (local Bloomberg Desktop API).

Reads  _data/credit_watch_config.json   hand-edit: instruments with Bloomberg ticker CANDIDATES + alert rules
       _data/technicals/prices.json     equity closes the 18:15 chain already pulls (no second Bloomberg pull)
Writes _data/credit_watch.json          {fetched_at, bbg_status, series:[{id, label, group, company, unit, field,
                                         ticker, status, points:[[date, value]...], last, last_date, error}]}

Fail-soft PER INSTRUMENT — the opposite of fetch_funding.py (which refuses to replace anything unless every
configured instrument succeeds): an instrument whose candidates all fail KEEPS its previous points (status
'stale') and records the error; the first LIMIT / WORKFLOW_REVIEW_NEEDED response marks bbg_status 'blocked'
and the remaining Bloomberg pulls are skipped (previous points kept). The first candidate that returns history
is pinned as the instrument's ticker and tried first next time.

Usage
  py fetch_credit_watch.py                 refresh every instrument
  py fetch_credit_watch.py --ids CRWV_CDS5Y ORCL_CDS5Y
  py fetch_credit_watch.py --probe         try every candidate over a 15-day window, print what resolves, write nothing
stdlib only (pandas arrives through the Bloomberg wrapper's own environment).
"""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_wiki" / "_data"
CONFIG = DATA / "credit_watch_config.json"
OUT = DATA / "credit_watch.json"
TECHNICALS = DATA / "technicals" / "prices.json"

sys.path.insert(0, r"E:\bloomberg_api")


def is_block(exc):
    text = f"{type(exc).__name__}: {exc}"
    return any(k in text for k in ("WORKFLOW_REVIEW", "LIMIT /", "Workflow review"))


def frame_points(df, ticker, end_iso):
    cols = {c.lower(): c for c in df.columns}
    c_date, c_tk, c_val = cols.get("date"), cols.get("ticker"), cols.get("value")
    if not all([c_date, c_tk, c_val]):
        raise ValueError(f"unexpected bdh columns {list(df.columns)}")
    sub = df[df[c_tk] == ticker].sort_values(c_date)
    pts = {}
    for _, r in sub.iterrows():
        try:
            v = float(r[c_val])
        except (TypeError, ValueError):
            continue
        d = str(r[c_date])[:10]
        if math.isfinite(v) and d <= end_iso:
            pts[d] = round(v, 4)
    return sorted(pts.items())


def technicals_points(ticker_us, history_days):
    """Closes from the 18:15 chain's prices.json — keyed by wiki ticker (CRWV), bbg 'CRWV US Equity'."""
    if not TECHNICALS.exists():
        return None, None
    tech = json.loads(TECHNICALS.read_text(encoding="utf-8"))
    for name, row in tech.get("names", {}).items():
        if row.get("bbg") == ticker_us:
            cutoff = (dt.date.today() - dt.timedelta(days=history_days)).isoformat()
            pts = [[d, float(c)] for d, c in zip(row.get("d", []), row.get("c", []))
                   if c is not None and d >= cutoff and math.isfinite(float(c))]
            return pts, tech.get("asof")
    return None, None


# ---------------------------------------------------------------- issuer yield board (config["board"])
def _cpn_forms(cpn):
    """9.75 -> ['9.75', '9 3/4']; 9 -> ['9']; 5.2 -> ['5.2']."""
    from fractions import Fraction
    forms = []
    txt = f"{cpn:g}"
    forms.append(txt)
    frac = Fraction(str(cpn)).limit_denominator(16)
    whole, rem = divmod(frac.numerator, frac.denominator)
    if rem and frac.denominator in (2, 4, 8, 16):
        forms.append(f"{whole} {rem}/{frac.denominator}" if whole else f"{rem}/{frac.denominator}")
    return forms


def bond_candidates(ticker, b):
    """Bloomberg ticker strings for one bond, most likely first.  b = {cpn, mty 'YYYY-MM-DD', suffix?}."""
    y, m, d = b["mty"].split("-")
    dates = [f"{m}/{d}/{y[2:]}", f"{m}/{d}/{y}"]
    suffixes = [b.get("suffix", "")] + ([""] if b.get("suffix") else [])
    out = []
    for cp in _cpn_forms(float(b["cpn"])):
        for dt_ in dates:
            for sfx in suffixes:
                out.append(" ".join(x for x in (ticker, cp, dt_, sfx, "Corp") if x))
    seen, uniq = set(), []
    for c in out:
        if c not in seen:
            seen.add(c); uniq.append(c)
    return uniq


def board_instruments(cfg):
    """Rows for every board bond (YLD_YTM_MID history) and issuer CDS (PX_LAST), same shape as config['instruments']."""
    board = cfg.get("board") or {}
    rows = []
    for iss in board.get("issuers", []):
        comp, name = iss["company"], iss.get("name", iss["company"])
        if iss.get("cds"):
            rows.append({"id": f"{comp}_CDS5Y", "group": "cds", "company": comp, "label": f"{name} 5Y CDS", "unit": "bp",
                         "field": "PX_LAST", "candidates": [iss["cds"]], "status": iss.get("cds_status", "verified-ticker"),
                         "rules": dict(board.get("cds_rules", {}), **iss.get("cds_rules", {})),
                         "board": {"issuer": comp, "name": name, "tier": iss.get("tier", ""), "kind": "cds"}})
        for b in iss.get("bonds", []):
            mty = b["mty"]
            mon = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}[mty[5:7]]
            kind = b.get("type", "senior")
            ccy = b.get("ccy", "USD")
            label = f"{name} {b['cpn']:g}% {mon}-{mty[:4]}" + (f" {ccy}" if ccy != "USD" else "") + (" (convertible)" if kind.startswith("conv") else "")
            rows.append({"id": f"{comp}_{b['cpn']:g}_{mty[:4]}" + (f"_{ccy}" if ccy != "USD" else ""), "group": "bond", "company": comp,
                         "label": label, "unit": "%", "field": b.get("field", "YLD_YTM_MID"),
                         "candidates": bond_candidates(iss.get("ticker", comp), b), "status": b.get("status", "verified-ticker"),
                         "rules": dict(board.get("bond_rules", {}), **b.get("rules", {})),
                         "board": {"issuer": comp, "name": name, "tier": iss.get("tier", ""), "kind": kind, "ccy": ccy, "cpn": b["cpn"],
                                   "mty": mty, "suffix": b.get("suffix", ""), "headline": bool(b.get("headline")), "note": b.get("note", "")}})
    return rows


SNAPSHOT_FIELDS = ["PX_LAST", "YLD_YTM_MID", "Z_SPRD_MID", "AMT_OUTSTANDING", "RTG_SP", "RTG_MOODY", "MATURITY", "CPN", "CRNCY", "SECURITY_DES"]


def bond_snapshot(bdp, tickers):
    """One bdp batch for the resolved board bonds: price, yield, Z-spread, size, ratings. Fail-soft -> {} ."""
    if not tickers:
        return {}
    try:
        df = bdp(tickers, SNAPSHOT_FIELDS)
    except Exception as exc:
        print(f"  snapshot bdp failed: {type(exc).__name__}: {str(exc)[:160]}")
        return {}
    cols = {c.lower(): c for c in df.columns}
    out = {}
    for _, r in df.iterrows():
        tk, fld, val = r[cols["ticker"]], r[cols["field"]], r[cols["value"]]
        try:
            if val is None or (isinstance(val, float) and not math.isfinite(val)):
                continue
        except TypeError:
            pass
        out.setdefault(tk, {})[fld] = val if isinstance(val, (int, float, str)) else str(val)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*", help="only these instrument ids")
    ap.add_argument("--probe", action="store_true", help="probe every candidate over 15 days, write nothing")
    ap.add_argument("--no-bbg", action="store_true", help="skip Bloomberg (technicals-backed equities only)")
    a = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"series": []}
    prev_by_id = {s["id"]: s for s in previous.get("series", [])}
    history_days = int(cfg.get("history_days", 400))
    today = dt.date.today()
    end_iso = today.isoformat()
    start = (today - dt.timedelta(days=15 if a.probe else history_days)).strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")

    bdh = None
    bbg_status = {"state": "skipped" if a.no_bbg else "ok", "detail": "", "checked_at": dt.datetime.now().isoformat(timespec="seconds")}
    if not a.no_bbg:
        try:
            from bloomberg import bdh  # noqa: F401  (local-terminal-only wrapper; raises if the Terminal is down)
        except Exception as exc:  # wrapper import failure = no Bloomberg this run
            bbg_status = {"state": "unavailable", "detail": f"{type(exc).__name__}: {exc}"[:300], "checked_at": bbg_status["checked_at"]}

    series_out, errors = [], []
    refreshed_ids = set()
    probe_resolved = set()
    all_instruments = list(cfg["instruments"]) + board_instruments(cfg)
    unknown = set(a.ids or []) - {ins["id"] for ins in all_instruments}
    if unknown:
        print("Unknown instrument ids: " + ", ".join(sorted(unknown)))
        return 2
    selected = [ins for ins in all_instruments if not a.ids or ins["id"] in a.ids]
    for ins in all_instruments:
        if a.ids and ins["id"] not in a.ids:
            if ins["id"] in prev_by_id:
                series_out.append(prev_by_id[ins["id"]])
            continue
        prev = prev_by_id.get(ins["id"], {})
        base = {"id": ins["id"], "label": ins["label"], "group": ins["group"], "company": ins.get("company"),
                "unit": ins.get("unit", ""), "field": ins.get("field", "PX_LAST"), "rules": ins.get("rules", {}),
                "config_status": ins.get("status", "unverified"), "context": ins.get("context", ""), "board": ins.get("board")}
        pts, used, err = None, None, None

        # 1) equities already in the technicals store: no Bloomberg call
        if ins.get("price_source") == "technicals" and not a.probe:
            for cand in ins["candidates"]:
                tp, asof = technicals_points(cand, history_days)
                if tp:
                    pts, used = tp, cand
                    base["source"] = f"technicals/prices.json (asof {asof})"
                    break

        # 2) Bloomberg candidates, previously resolved ticker first
        if pts is None and bdh is not None and bbg_status["state"] == "ok":
            cands = list(ins["candidates"])
            if prev.get("ticker") in cands:
                cands.remove(prev["ticker"]); cands.insert(0, prev["ticker"])
            for cand in cands:
                try:
                    df = bdh([cand], [base["field"]], start, end)
                    got = frame_points(df, cand, end_iso)
                    if a.probe:
                        print(f"  {ins['id']:<16} {cand:<36} -> {len(got)} pts" + (f"  last {got[-1][1]} ({got[-1][0]})" if got else ""))
                    if got:
                        probe_resolved.add(ins["id"])
                        pts, used = got, cand
                        base["source"] = f"Bloomberg {cand} {base['field']}"
                        break
                    err = f"{cand}: no data"
                except Exception as exc:
                    err = f"{cand}: {type(exc).__name__}: {exc}"[:300]
                    if is_block(exc):
                        bbg_status = {"state": "blocked", "detail": err, "checked_at": bbg_status["checked_at"]}
                        print(f"  Bloomberg Desktop API blocked — {err}")
                        break
                    if a.probe:
                        print(f"  {ins['id']:<16} {cand:<36} -> ERR {err[:120]}")
            if bbg_status["state"] == "blocked":
                err = "Bloomberg Desktop API blocked (LIMIT / WORKFLOW_REVIEW_NEEDED) — previous points kept"
        elif pts is None and not a.probe:
            err = {"skipped": "Bloomberg skipped (--no-bbg)", "unavailable": bbg_status["detail"],
                   "blocked": "Bloomberg Desktop API blocked — previous points kept"}.get(bbg_status["state"], "no source")

        if a.probe:
            continue
        if pts:
            refreshed_ids.add(ins["id"])
            series_out.append({**base, "ticker": used, "status": "ok", "points": pts,
                               "last": pts[-1][1], "last_date": pts[-1][0], "error": None,
                               "fetched_at": dt.datetime.now().isoformat(timespec="seconds")})
            print(f"  {ins['id']:<16} {used:<36} {len(pts):>4} pts  last {pts[-1][1]} ({pts[-1][0]})")
        elif prev.get("points"):
            series_out.append({**base, "ticker": prev.get("ticker"), "status": "stale", "points": prev["points"],
                               "last": prev["points"][-1][1], "last_date": prev["points"][-1][0], "error": err,
                               "fetched_at": prev.get("fetched_at")})
            errors.append(f"{ins['id']}: kept previous points through {prev['points'][-1][0]} — {err}")
            print(f"  {ins['id']:<16} STALE (kept {len(prev['points'])} pts to {prev['points'][-1][0]}) — {err}")
        else:
            series_out.append({**base, "ticker": None, "status": "none", "points": [], "last": None, "last_date": None,
                               "error": err, "fetched_at": None})
            errors.append(f"{ins['id']}: no history yet — {err}")
            print(f"  {ins['id']:<16} NONE — {err}")

    if a.probe:
        print(f"probe done · bbg_status {bbg_status['state']} {bbg_status['detail'][:160]}")
        return 0 if bbg_status["state"] == "ok" and selected and len(probe_resolved) == len(selected) else 1

    # snapshot (price / yield / Z-spread / size / ratings) for the resolved board bonds — one batch, fail-soft
    snap = {}
    if bdh is not None and bbg_status["state"] == "ok":
        from bloomberg import bdp
        snap = bond_snapshot(bdp, [x["ticker"] for x in series_out if x["id"] in refreshed_ids and x.get("board") and x["group"] == "bond" and x.get("ticker") and x["status"] == "ok"])
    for x in series_out:
        if x.get("board") and x["group"] == "bond":
            if x.get("ticker") in snap:
                x["snapshot"] = dict(snap[x["ticker"]], asof=dt.datetime.now().isoformat(timespec="seconds"))
            elif prev_by_id.get(x["id"], {}).get("snapshot"):
                x["snapshot"] = prev_by_id[x["id"]]["snapshot"]

    payload = {"fetched_at": dt.datetime.now().isoformat(timespec="seconds"), "history_days": history_days,
               "bbg_status": bbg_status, "series": series_out, "errors": errors}
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(OUT)
    ok = sum(1 for s in series_out if s["status"] == "ok")
    print(f"-> {OUT}  ({ok} fresh / {len(series_out)} series · bbg {bbg_status['state']}" + (f" · {len(errors)} kept/missing" if errors else "") + ")")
    return 0 if ok == len(series_out) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
