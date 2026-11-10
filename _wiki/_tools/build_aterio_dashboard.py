"""Aterio US data-center census -> explorer dashboard (_dashboards/aterio-dc.html).

Reads the Aterio export folder (P:\\Felipe Monteiro\\Aterio, or --src):
  data-centers/inventory/data_center_inventory_<YYYYMMDD>.csv   building-level census (latest file wins)
  data-centers/inventory/data_center_events_<YYYYMMDD>.csv      stage/progress events per building
  data-centers/inventory/monthly-history/<date>/*.csv           point-in-time snapshots (same schema)
  data-centers/inventory/Data Centers Data Dictionary.xlsx      field guide (level = building/campus)
  data-centers/reports/Aterio US Data Centers Weekly Report.xlsx Aterio's own pivots (30d deltas, activation
                                                                 forecast, reconstructed monthly momentum, ISO demand)
  power-generation/behind-the-meter-inventory/*.csv              behind-the-meter (BTM) generation phases + the DCs
                                                                 they link to
Writes  _wiki/_data/aterio/summary.json   every aggregate the page shows (no row-level data)
        _wiki/_dashboards/aterio-dc.html  the page (template _tools/aterio_ui/template.html + payload incl. rows)

Bases (shown on the page): SELECTED_POWER_CAPACITY_MW is total FACILITY power per building (published value,
else Aterio's estimate). IT-equivalent = facility / the median facility/IT ratio of the rows that report both.
TOT_PROJECT_COST is CAMPUS-level and repeated on every building of the campus, so cost is deduplicated per campus.
US only unless stated (the export also carries Canadian rows).

Run:  py _wiki/_tools/build_aterio_dashboard.py [--src <folder>]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
OUT_HTML = os.path.join(WIKI, "_dashboards", "aterio-dc.html")
OUT_JSON = os.path.join(WIKI, "_data", "aterio", "summary.json")
TEMPLATE = os.path.join(HERE, "aterio_ui", "template.html")

sys.path.insert(0, HERE)
import aterio_core as core  # noqa: E402  (shared Aterio loader: source folder, stage groups, facility/IT ratio)
import build_dc_delay as bdd  # noqa: E402  (map geometry + state names only)

SRC_CANDIDATES = core.SRC_CANDIDATES
STAGES = ["Active", "Construction", "Delayed", "Announcement", "Land Bank", "Not Approved/Withdrawn", "Cancelled"]
GROUP = core.GROUP
GROUPS =["active", "uc", "delayed", "ann", "wd"]
GROUP_LABEL = {"active": "Active", "uc": "Under construction", "delayed": "Delayed",
               "ann": "Announced (incl. land bank)", "wd": "Withdrawn / cancelled"}
HYPERSCALER_TICKERS = {"AMZN", "GOOG", "META", "MSFT", "ORCL", "AAPL"}
TICKER_ALIAS = {"GOOGL": "GOOG", "FB": "META"}


# ----------------------------------------------------------------------------- helpers
def gw(x) -> float:
    x = float(x or 0)
    return round(x / 1000.0, 2)


def ym(s):
    if s is None or (isinstance(s, float) and math.isnan(s)) or s is pd.NaT:
        return ""
    try:
        return pd.Timestamp(s).strftime("%Y-%m")
    except Exception:
        return ""


def clean(v):
    if v is None:
        return ""
    if isinstance(v, float) and math.isnan(v):
        return ""
    return str(v).strip()


def split_list(v) -> list[str]:
    v = clean(v)
    if not v:
        return []
    return [p.strip() for p in re.split(r",\s*", v) if p.strip()]


find_src, latest = core.find_src, core.latest     # kept importable from here (older callers)


def to_dt(s):
    return pd.to_datetime(s, errors="coerce")


def stage_gw(df: pd.DataFrame, by: str | None = None) -> dict:
    """GW per stage group (and optional extra key)."""
    out = {}
    for g in GROUPS:
        out[g] = gw(df.loc[df["grp"] == g, "MW"].sum())
    return out


# ----------------------------------------------------------------------------- loaders
INV_COLS_SNAP = ["ATERIO_DATA_CENTER_UID", "DATA_CENTER_STAGE", "SELECTED_POWER_CAPACITY_MW", "COUNTRY_CODE",
                 "DATA_CENTER_ACTIVATION_DATE", "DATA_CENTER_ANNOUNCED_DATE", "RECORD_CREATED_DATE", "STATE_CODE"]


def load_snapshot(path: str) -> pd.DataFrame:
    d = pd.read_csv(path, low_memory=False, usecols=lambda c: c in INV_COLS_SNAP)
    if "COUNTRY_CODE" in d.columns:
        d = d[d["COUNTRY_CODE"].fillna("US") == "US"]
    d = d.copy()
    d["MW"] = pd.to_numeric(d["SELECTED_POWER_CAPACITY_MW"], errors="coerce").fillna(0.0)
    d["act"] = to_dt(d.get("DATA_CENTER_ACTIVATION_DATE"))
    d["grp"] = d["DATA_CENTER_STAGE"].map(GROUP).fillna("ann")
    return d.set_index("ATERIO_DATA_CENTER_UID")


def wiki_tickers() -> set[str]:
    out = set()
    for f in glob.glob(os.path.join(WIKI, "*.md")):
        stem = os.path.splitext(os.path.basename(f))[0]
        if re.fullmatch(r"[A-Z0-9.]{1,8}", stem):
            out.add(stem)
    return out


def read_dictionary(path: str) -> dict:
    import openpyxl
    out = {}
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return out
    for ws in wb.worksheets:
        hdr = None
        for r in ws.iter_rows(values_only=True):
            if r and r[0] == "Field Name":
                hdr = r
                continue
            if hdr and r and r[1]:
                field = str(r[1]).replace("(PK)", "").replace("(FK)", "").strip()
                out.setdefault(field, {"label": clean(r[0]), "type": clean(r[2]), "level": clean(r[3]),
                                       "desc": clean(r[4]), "example": clean(r[5])[:80], "sheet": ws.title.strip()})
    return out


def read_weekly(path: str) -> dict:
    import openpyxl
    out: dict = {}
    if not os.path.exists(path):
        return out
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)

    def rows(name):
        if name not in wb.sheetnames:
            return [], []
        it = wb[name].iter_rows(values_only=True)
        h = next(it)
        return list(h), [r for r in it if any(v is not None for v in r)]

    out["sheets"] = [{"name": ws.title, "rows": ws.max_row, "cols": ws.max_column} for ws in wb.worksheets]
    h, r = rows("US 30d Comparison")
    out["d30"] = [dict(zip(h, x)) for x in r]
    for x in out["d30"]:
        for k, v in list(x.items()):
            if isinstance(v, dt.datetime):
                x[k] = v.strftime("%Y-%m-%d")
    # Aterio's activation forecast, cumulative MW by activation year (sum of the state sheet)
    h, r = rows("US Additional Info - Evo State")
    fc: dict = {}
    for x in r:
        y = x[1]
        if y is None:
            continue
        a = fc.setdefault(int(y), [0.0, 0.0, 0.0])
        for i in range(3):
            a[i] += float(x[2 + i] or 0)
    out["forecast"] = [{"year": y, "opt": gw(v[0]), "base": gw(v[1]), "cons": gw(v[2])} for y, v in sorted(fc.items())]
    out["forecast_asof"] = clean(r[0][5])[:10] if r else ""
    # reconstructed monthly stock (today's knowledge, dated back)
    h, r = rows("US Const Announced Momentum")
    mom: dict = {}
    for x in r:
        k = x[2]
        if not isinstance(k, dt.datetime):
            continue
        a = mom.setdefault(k.strftime("%Y-%m"), [0.0] * 6)
        for i, j in enumerate([3, 4, 6, 7, 9, 10]):
            a[i] += float(x[j] or 0)
    out["momentum"] = [{"m": k, "uc_n": int(v[0]), "uc": gw(v[1]), "ann_n": int(v[2]), "ann": gw(v[3]),
                        "act_n": int(v[4]), "act": gw(v[5])} for k, v in sorted(mom.items())]
    # ISO demand vs DC capacity
    h, r = rows("Data - ISO vs Data Centers")
    iso = []
    for x in r:
        if x[1] and isinstance(x[2], (int, float)):
            iso.append({"ba": x[1], "name": clean(x[0]), "demand_gw": gw(x[2]), "dc_gw": gw(x[3]),
                        "share": round(float(x[4] or 0), 4)})
    out["iso"] = sorted(iso, key=lambda d: -d["demand_gw"])
    return out


# ----------------------------------------------------------------------------- build
def build(src: str) -> dict:
    inv_path, asof = latest(os.path.join(src, "data-centers", "inventory", "data_center_inventory_*.csv"))
    ev_path, ev_asof = latest(os.path.join(src, "data-centers", "inventory", "data_center_events_*.csv"))
    asof_ts = pd.Timestamp(asof)
    raw = pd.read_csv(inv_path, low_memory=False)
    raw["MW"] = pd.to_numeric(raw["SELECTED_POWER_CAPACITY_MW"], errors="coerce")
    raw["MWf"] = raw["MW"].fillna(0.0)
    raw["grp"] = raw["DATA_CENTER_STAGE"].map(GROUP).fillna("ann")
    ca = raw[raw["COUNTRY_CODE"] == "CA"]
    us = raw[raw["COUNTRY_CODE"] == "US"].copy()
    us["MW"] = us["MWf"]
    us["IT"] = pd.to_numeric(us["CRITICAL_IT_CAPACITY_MW"], errors="coerce")
    us["act"] = to_dt(us["DATA_CENTER_ACTIVATION_DATE"])
    us["ann_d"] = to_dt(us["DATA_CENTER_ANNOUNCED_DATE"])
    us["cs_d"] = to_dt(us["DATA_CENTER_CONSTRUCTION_START_DATE"])
    us["created"] = to_dt(us["RECORD_CREATED_DATE"])
    us["y"] = us["act"].dt.year
    us["like"] = us["PROJECT_EXECUTION_LIKELIHOOD"].fillna("Unrated")
    us["ai"] = us["FLG_AI_FACILITY"].eq("Y")
    us["btm"] = us["FLG_BTM_ONSITE_POWER_GENERATION"].eq("Y")
    us["tick"] = us["PROVIDER_TICKER_NAME"].map(lambda t: TICKER_ALIAS.get(clean(t), clean(t)))
    wt = wiki_tickers()

    # facility/IT ratio from rows reporting both: the house ratio (rule 1, aterio_core.fac_it) + the MW-weighted variant
    fi = core.fac_it(us["MW"], us["IT"])
    it_ratio, it_ratio_wtd = fi["k"], round(fi["weighted"], 3)

    P: dict = {"asof": asof, "events_asof": ev_asof, "built": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
               "src": src, "it_ratio": it_ratio, "it_ratio_wtd": it_ratio_wtd, "it_ratio_n": fi["n"],
               "it_ratio_measured": round(fi["median"], 3),
               "group_label": GROUP_LABEL}

    # ---------------- stage table
    st = []
    for s in STAGES:
        d = us[us["DATA_CENTER_STAGE"] == s]
        if not len(d):
            continue
        st.append({"stage": s, "grp": GROUP[s], "n": int(len(d)), "gw": gw(d["MW"].sum()),
                   "n_mw": int(d["SELECTED_POWER_CAPACITY_MW"].notna().sum()),
                   "gw_pub": gw(pd.to_numeric(d["PROV_PUB_TOT_POWER_CAPACITY_MW"], errors="coerce").sum()),
                   "gw_it_rep": gw(d["IT"].sum()), "n_it": int(d["IT"].notna().sum()),
                   "gw_ai": gw(d.loc[d["ai"], "MW"].sum()), "n_ai": int(d["ai"].sum()),
                   "gw_btm": gw(d.loc[d["btm"], "MW"].sum()),
                   "like": {k: gw(d.loc[d["like"] == k, "MW"].sum()) for k in ["High", "Medium", "Low", "Unrated"]}})
    P["stages"] = st
    P["totals"] = {"n": int(len(us)), "gw": gw(us["MW"].sum()), "n_all": int(len(raw)), "n_ca": int(len(ca)),
                   "gw_ca": gw(ca["MWf"].sum()), "ca_stage": {s: int(v) for s, v in ca["DATA_CENTER_STAGE"].value_counts().items()},
                   "providers": int(us["ATERIO_PROVIDER_UID"].nunique()),
                   "campuses": int(us["ATERIO_DATA_CENTER_CAMPUS_UID"].nunique()),
                   "no_campus": int(us["ATERIO_DATA_CENTER_CAMPUS_UID"].isna().sum()),
                   "states": int(us["STATE_CODE"].nunique()), "counties": int(us["COUNTY_FIPS_CODE"].nunique())}

    # ---------------- timeline by activation year
    yrs = list(range(2016, 2036))
    tl = {"years": [str(y) for y in yrs] + ["2036+"], "series": {}}
    def by_year(mask):
        d = us[mask]
        vals = [gw(d.loc[d["y"] == y, "MW"].sum()) for y in yrs]
        vals.append(gw(d.loc[d["y"] >= 2036, "MW"].sum()))
        return vals
    tl["series"]["active"] = by_year(us["grp"] == "active")
    tl["series"]["uc"] = by_year(us["grp"] == "uc")
    tl["series"]["delayed"] = by_year(us["grp"] == "delayed")
    tl["series"]["ann"] = by_year(us["grp"] == "ann")
    for k in ["High", "Medium", "Low", "Unrated"]:
        tl["series"]["ann_" + k] = by_year((us["grp"] == "ann") & (us["like"] == k))
    tl["undated"] = {g: gw(us.loc[(us["grp"] == g) & us["y"].isna(), "MW"].sum()) for g in GROUPS}
    tl["uc_by_year"] = {str(int(y)): gw(v) for y, v in us[us["grp"] == "uc"].groupby("y")["MW"].sum().items()}
    P["timeline"] = tl

    # ---------------- weekly report
    W = read_weekly(os.path.join(src, "data-centers", "reports", "Aterio US Data Centers Weekly Report.xlsx"))
    P["weekly"] = W

    # ---------------- snapshots (point in time)
    snaps = []
    hist_dirs = sorted(glob.glob(os.path.join(src, "data-centers", "inventory", "monthly-history", "*")))
    snap_frames: dict[str, pd.DataFrame] = {}
    for d in hist_dirs:
        f = glob.glob(os.path.join(d, "data_center_inventory_*.csv"))
        if not f:
            continue
        date = os.path.basename(d)
        df = load_snapshot(f[0])
        snap_frames[date] = df
    cur = load_snapshot(inv_path)
    snap_frames[asof] = cur
    for date in sorted(snap_frames):
        df = snap_frames[date]
        snaps.append({"date": date, "n": int(len(df)), **{g: gw(df.loc[df["grp"] == g, "MW"].sum()) for g in GROUPS},
                      "n_uc": int((df["grp"] == "uc").sum())})
    P["snapshots"] = snaps

    # ---------------- comparisons vs earlier snapshots (transitions, slippage, growth)
    dates = sorted(snap_frames)
    def months_before(n):
        target = (asof_ts - pd.DateOffset(months=n)).strftime("%Y-%m")
        c = [d for d in dates if d.startswith(target)]
        return c[0] if c else None
    bases = []
    for n in (6, 12):
        b = months_before(n)
        if b and b not in bases:
            bases.append(b)
    if dates[0] not in bases and dates[0] != asof:
        bases.append(dates[0])
    comps = {}
    for b in bases:
        old = snap_frames[b]
        j = old.join(cur, lsuffix="_o", rsuffix="_n", how="inner")
        # transitions (GW at the OLD size so rows sum to the old stock; counts too)
        mat, matn = {}, {}
        for go in GROUPS:
            mat[go], matn[go] = {}, {}
            oo = old[old["grp"] == go]
            for gn in GROUPS:
                sel = j[(j["grp_o"] == go) & (j["grp_n"] == gn)]
                mat[go][gn] = gw(sel["MW_o"].sum())
                matn[go][gn] = int(len(sel))
            dropped = oo[~oo.index.isin(cur.index)]
            mat[go]["dropped"] = gw(dropped["MW"].sum())
            matn[go]["dropped"] = int(len(dropped))
            mat[go]["_total"] = gw(oo["MW"].sum())
        new = cur[~cur.index.isin(old.index)].copy()
        an = to_dt(new.get("DATA_CENTER_ANNOUNCED_DATE"))
        bts = pd.Timestamp(b)
        newsplit = {
            "after": {"n": int((an > bts).sum()), "gw": gw(new.loc[an > bts, "MW"].sum())},
            "before": {"n": int((an <= bts).sum()), "gw": gw(new.loc[an <= bts, "MW"].sum())},
            "undated": {"n": int(an.isna().sum()), "gw": gw(new.loc[an.isna(), "MW"].sum())},
            "by_grp": {g: gw(new.loc[new["grp"] == g, "MW"].sum()) for g in GROUPS},
            "by_grp_before": {g: gw(new.loc[(new["grp"] == g) & (an <= bts), "MW"].sum()) for g in GROUPS},
        }
        # slippage of activation dates for rows that were not yet active and dated after the base
        f = j[(j["act_o"] > bts) & j["act_n"].notna()].copy()
        f["slip"] = ((f["act_n"] - f["act_o"]).dt.days / 30.44).round()
        bins = [(-9999, -1, "Pulled in"), (0, 0, "Unchanged"), (1, 3, "1-3 mo"), (4, 6, "4-6 mo"),
                (7, 12, "7-12 mo"), (13, 24, "13-24 mo"), (25, 9999, ">24 mo")]
        slip = {}
        for g in ["uc", "ann"]:
            x = f[f["grp_o"] == g]
            w = x["MW_o"]
            tot = float(w.sum()) or 1.0
            slip[g] = {"n": int(len(x)), "gw": gw(w.sum()),
                       "bins": [{"label": lab, "n": int(((x["slip"] >= lo) & (x["slip"] <= hi)).sum()),
                                 "gw": gw(w[(x["slip"] >= lo) & (x["slip"] <= hi)].sum())} for lo, hi, lab in bins],
                       "share_later": round(float(w[x["slip"] > 0].sum()) / tot, 3),
                       "share_earlier": round(float(w[x["slip"] < 0].sum()) / tot, 3),
                       "wmean": round(float((x["slip"] * w).sum()) / tot, 1) if len(x) else None,
                       "median": float(x["slip"].median()) if len(x) else None}
        due = j[(j["grp_o"] == "uc") & (j["act_o"] > bts) & (j["act_o"] <= asof_ts)]
        due_out = {"gw": gw(due["MW_o"].sum()), "n": int(len(due)),
                   "now": {g: gw(due.loc[due["grp_n"] == g, "MW_o"].sum()) for g in GROUPS}}
        comps[b] = {"base": b, "old_n": int(len(old)), "old_gw": gw(old["MW"].sum()), "matched": int(len(j)),
                    "mat": mat, "matn": matn, "new": {"n": int(len(new)), "gw": gw(new["MW"].sum()), **newsplit},
                    "dropped": {"n": int((~old.index.isin(cur.index)).sum()),
                                "gw": gw(old.loc[~old.index.isin(cur.index), "MW"].sum())},
                    "slip": slip, "due": due_out}
    P["comparisons"] = comps
    P["default_base"] = months_before(12) or bases[0]

    # ---------------- flows from the events log (GW at the building's current size)
    ev = pd.read_csv(ev_path, low_memory=False)
    ev = ev[ev["ATERIO_DATA_CENTER_UID"].isin(us["ATERIO_DATA_CENTER_UID"])].copy()
    ev["d"] = to_dt(ev["EVENT_DATE"])
    mwmap = us.set_index("ATERIO_DATA_CENTER_UID")["MW"]
    ev["MW"] = ev["ATERIO_DATA_CENTER_UID"].map(mwmap).fillna(0.0)
    EVK = {"Announced": "ann", "Construction Started": "start", "Active": "active",
           "Not Approved/Withdrawn": "wd", "Delayed": "delayed", "Cancelled": "cancel",
           "Land Bank Purchase": "land", "Construction Finished": "finished"}
    ev["k"] = ev["EVENT_TYPE"].map(EVK)
    ev.loc[ev["EVENT_TYPE"].str.startswith("Under Construction", na=False), "k"] = "progress"
    evp = ev[(ev["d"] <= asof_ts) & (ev["d"] >= "2021-01-01")].copy()
    evp["q"] = evp["d"].dt.to_period("Q").astype(str)
    qs = sorted(evp["q"].unique())
    flows = {"q": qs}
    for k in ["ann", "start", "active", "wd", "delayed", "cancel"]:
        sub = evp[evp["k"] == k]
        flows[k] = [gw(sub.loc[sub["q"] == q, "MW"].sum()) for q in qs]
        flows[k + "_n"] = [int((sub["q"] == q).sum()) for q in qs]
    P["flows"] = flows
    P["events"] = {"rows": int(len(pd.read_csv(ev_path, usecols=[0]))), "us_rows": int(len(ev)),
                   "types": [{"type": t, "n": int(n)} for t, n in ev["EVENT_TYPE"].value_counts().items()],
                   "future_active": int(((ev["k"] == "active") & (ev["d"] > asof_ts)).sum())}

    # ---------------- states, counties
    states = {}
    for s, d in us.groupby("STATE_CODE"):
        states[s] = {"name": clean(d["STATE_NAME"].iloc[0]), "n": int(len(d)),
                     **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS},
                     **{"n_" + g: int((d["grp"] == g).sum()) for g in GROUPS},
                     "ai": gw(d.loc[d["ai"] & d["grp"].isin(["uc", "ann", "delayed"]), "MW"].sum()),
                     "btm": int(d["btm"].sum()),
                     "ann_hi": gw(d.loc[(d["grp"] == "ann") & (d["like"] == "High"), "MW"].sum())}
    P["states"] = states
    P["map"] = bdd.state_paths()
    cty = us.groupby(["COUNTY_NAME", "STATE_CODE"]).apply(
        lambda d: pd.Series({g: d.loc[d["grp"] == g, "MW"].sum() for g in GROUPS} | {"n": len(d)}),
        include_groups=False).reset_index()
    cty["pipe"] = cty["uc"] + cty["delayed"] + cty["ann"]
    top_c = cty.sort_values("uc", ascending=False).head(25)
    P["counties"] = [{"county": r.COUNTY_NAME, "st": r.STATE_CODE, "n": int(r.n),
                      **{g: gw(getattr(r, g)) for g in GROUPS}} for r in top_c.itertuples()]

    # ---------------- providers
    prov = []
    for (pid), d in us.groupby("ATERIO_PROVIDER_UID"):
        tot = d["MW"].sum()
        if tot < 150:
            continue
        t = clean(d["tick"].iloc[0])
        prov.append({"name": clean(d["PROVIDER_NAME"].iloc[0]), "pub": clean(d["PROVIDER_PUBLIC_PRIVATE"].iloc[0]),
                     "tick": t, "wiki": t in wt, "hs": t in HYPERSCALER_TICKERS,
                     "backed": clean(d["PROVIDER_BACKED_BY"].dropna().iloc[0]) if d["PROVIDER_BACKED_BY"].notna().any() else "",
                     "n": int(len(d)), "states": int(d["STATE_CODE"].nunique()),
                     **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS},
                     "ai": gw(d.loc[d["ai"], "MW"].sum()),
                     "ann_hi": gw(d.loc[(d["grp"] == "ann") & (d["like"] == "High"), "MW"].sum())})
    P["providers"] = sorted(prov, key=lambda p: -(p["uc"] + p["ann"] + p["active"] + p["delayed"]))
    uc_tot = us.loc[us["grp"] == "uc", "MW"].sum() or 1.0
    P["hs_share_uc"] = round(float(us.loc[(us["grp"] == "uc") & us["tick"].isin(HYPERSCALER_TICKERS), "MW"].sum()) / uc_tot, 3)
    P["pub_share_uc"] = round(float(us.loc[(us["grp"] == "uc") & us["PROVIDER_PUBLIC_PRIVATE"].eq("Public"), "MW"].sum()) / uc_tot, 3)
    P["cnd"] = {g: gw(us.loc[(us["grp"] == g) & us["PROVIDER_NAME"].eq("Company Not Disclosed"), "MW"].sum()) for g in GROUPS}

    # parsed list fields (a building's MW counts in full for every company named on it)
    def parsed(col: str, top: int = 25) -> dict:
        rows = []
        filled = us[col].notna()
        for idx, v in us.loc[filled, col].items():
            for name in split_list(v):
                rows.append((name, us.at[idx, "grp"], us.at[idx, "MW"]))
        if not rows:
            return {"fill": 0, "rows": []}
        x = pd.DataFrame(rows, columns=["name", "grp", "MW"])
        agg = []
        for name, d in x.groupby("name"):
            agg.append({"name": name, "n": int(len(d)), **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS}})
        agg.sort(key=lambda a: -(a["uc"] + a["ann"] + a["delayed"] + a["active"]))
        return {"fill": round(float(filled.mean()), 3), "n_bld": int(filled.sum()),
                "gw_bld": gw(us.loc[filled, "MW"].sum()), "rows": agg[:top]}
    P["lists"] = {"end_users": parsed("END_USER_COMPANIES"), "backed_by": parsed("PROVIDER_BACKED_BY"),
                  "financing": parsed("PROJECT_FINANCING_COMPANIES"),
                  "builders": parsed("CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES")}

    # ---------------- utilities, balancing authorities, generators
    pipe_mask = us["grp"].isin(["uc", "ann", "delayed"])
    util = []
    for name, d in us[us["UTILITY_NAME"].notna()].groupby("UTILITY_NAME"):
        if d["MW"].sum() < 300:
            continue
        util.append({"name": name, "tick": clean(d["UTILITY_TICKER_NAME"].dropna().iloc[0]) if d["UTILITY_TICKER_NAME"].notna().any() else "",
                     "pub": clean(d["UTILITY_PUBLIC_PRIVATE"].dropna().iloc[0]) if d["UTILITY_PUBLIC_PRIVATE"].notna().any() else "",
                     "n": int(len(d)), **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS}})
    util.sort(key=lambda u: -(u["uc"] + u["ann"] + u["delayed"]))
    P["utilities"] = {"rows": util[:30], "unknown_pipe_gw": gw(us.loc[pipe_mask & us["UTILITY_NAME"].isna(), "MW"].sum()),
                      "pipe_gw": gw(us.loc[pipe_mask, "MW"].sum()),
                      "unknown_uc_gw": gw(us.loc[(us["grp"] == "uc") & us["UTILITY_NAME"].isna(), "MW"].sum())}
    ba = []
    for ab, d in us[us["BAL_AUTH_ABBR"].notna()].groupby("BAL_AUTH_ABBR"):
        ba.append({"ba": ab, "name": clean(d["BAL_AUTH_NAME"].iloc[0]), "n": int(len(d)),
                   **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS}})
    ba.sort(key=lambda b: -(b["uc"] + b["ann"] + b["delayed"] + b["active"]))
    P["ba"] = {"rows": ba[:16], "unknown_pipe_gw": gw(us.loc[pipe_mask & us["BAL_AUTH_ABBR"].isna(), "MW"].sum())}
    gens = pd.to_numeric(us["TOT_NUM_GENERATORS"], errors="coerce")
    P["generators"] = {"fill": round(float(gens.notna().mean()), 3),
                       "by_grp": {g: int(gens[us["grp"] == g].sum()) for g in GROUPS},
                       "mw_per_gen": round(float(us.loc[gens > 0, "MW"].sum() / gens[gens > 0].sum()), 2) if (gens > 0).any() else None}

    # ---------------- behind-the-meter generation
    btm_dir = os.path.join(src, "power-generation", "behind-the-meter-inventory")
    bp, b_asof = latest(os.path.join(btm_dir, "behind_the_meter_power_generation_inventory_*.csv"))
    b = pd.read_csv(bp, low_memory=False)
    b["MW"] = pd.to_numeric(b["TOT_PHASE_NAMEPLATE_POWER_MW"], errors="coerce").fillna(0.0)
    b["tech"] = b["ATERIO_PLANT_TECHNOLOGY_TYPE"].replace({"Fuell Cell": "Fuel Cell"}).fillna("Other")
    BGRP = {"Active": "active", "Construction": "uc", "Site Preparation": "uc", "Delayed": "delayed",
            "Announcement": "ann", "Not Approved/Withdrawn": "wd", "Cancelled": "wd"}
    b["grp"] = b["PHASE_STAGE"].map(BGRP).fillna("ann")
    techs = []
    for t, d in b.groupby("tech"):
        techs.append({"tech": t, "n": int(len(d)), **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS},
                      "src": clean(d.groupby("ATERIO_PLANT_ENERGY_SOURCE")["MW"].sum().idxmax()) if d["ATERIO_PLANT_ENERGY_SOURCE"].notna().any() else ""})
    techs.sort(key=lambda r: -sum(r[g] for g in GROUPS))
    srcs = [{"src": s, "n": int(len(d)), "gw": gw(d["MW"].sum())} for s, d in b.groupby("ATERIO_PLANT_ENERGY_SOURCE")]
    srcs.sort(key=lambda r: -r["gw"])
    bst = [{"st": s, "n": int(len(d)), **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS}} for s, d in b.groupby("STATE_CODE")]
    bst.sort(key=lambda r: -sum(r[g] for g in GROUPS))

    def bparsed(col, top=15):
        rows = []
        for idx, v in b[col].items():
            for name in split_list(v):
                if name.lower() in ("company not disclosed",):
                    continue
                rows.append((name, b.at[idx, "grp"], b.at[idx, "MW"]))
        x = pd.DataFrame(rows, columns=["name", "grp", "MW"])
        agg = [{"name": n, "n": int(len(d)), **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS}} for n, d in x.groupby("name")]
        agg.sort(key=lambda r: (-r["n"], -sum(r[g] for g in GROUPS)))
        return agg[:top]
    dcb = pd.read_csv(latest(os.path.join(btm_dir, "data_center_with_behind_the_meter_*.csv"))[0], low_memory=False)
    dcb["MW"] = pd.to_numeric(dcb["SELECTED_POWER_CAPACITY_MW"], errors="coerce").fillna(0.0)
    dcb["grp"] = dcb["DATA_CENTER_STAGE"].map(GROUP).fillna("ann")
    phases = []
    for r in b.sort_values("MW", ascending=False).itertuples():
        phases.append([clean(r.PROJECT_NAME), clean(r.PLANT_NAME), clean(r.PHASE_NAME), clean(r.DEVELOPER_COMPANIES),
                       clean(r.CUSTOMER_COMPANIES), r.tech, clean(r.ATERIO_PLANT_ENERGY_SOURCE), clean(r.PHASE_STAGE),
                       round(float(r.MW), 1), clean(r.STATE_CODE), clean(r.COUNTY_NAME),
                       ym(r.PHASE_SELECTED_ACTIVATION_DATE), clean(r.CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES),
                       clean(r.FLG_BTM_PROJECT)])
    P["btm"] = {"asof": b_asof, "phases_n": int(len(b)), "projects_n": int(b["ATERIO_POWER_GENERATION_PROJECT_UID"].nunique()),
                "plants_n": int(b["ATERIO_POWER_GENERATION_PLANT_UID"].nunique()),
                "gw": gw(b["MW"].sum()), "by_grp": {g: gw(b.loc[b["grp"] == g, "MW"].sum()) for g in GROUPS},
                "flag_n": {k: int(v) for k, v in b["FLG_BTM_PROJECT"].value_counts().items()},
                "techs": techs, "sources": srcs, "states": bst[:15],
                "developers": bparsed("DEVELOPER_COMPANIES"), "equipment": bparsed("CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES", 20),
                "customers": bparsed("CUSTOMER_COMPANIES"),
                "dc": {"n": int(len(dcb)), "gw": gw(dcb["MW"].sum()), "by_grp": {g: gw(dcb.loc[dcb["grp"] == g, "MW"].sum()) for g in GROUPS},
                       "n_by_grp": {g: int((dcb["grp"] == g).sum()) for g in GROUPS}},
                "phases": phases,
                "phase_cols": ["project", "plant", "phase", "developer", "customer", "tech", "source", "stage", "mw", "st",
                               "county", "act", "equipment", "btm"]}

    # ---------------- AI facilities
    P["ai"] = {"by_grp": {g: gw(us.loc[us["ai"] & (us["grp"] == g), "MW"].sum()) for g in GROUPS},
               "n_by_grp": {g: int((us["ai"] & (us["grp"] == g)).sum()) for g in GROUPS},
               "n_flag_n": int(us["FLG_AI_FACILITY"].eq("N").sum()), "fill": round(float(us["FLG_AI_FACILITY"].notna().mean()), 3)}

    # ---------------- cost (campus-level, deduplicated)
    c = us[us["TOT_PROJECT_COST"].notna()].copy()
    c["cost"] = pd.to_numeric(c["TOT_PROJECT_COST"], errors="coerce")
    c["key"] = c["ATERIO_DATA_CENTER_CAMPUS_UID"].fillna(c["ATERIO_DATA_CENTER_UID"])
    camp_mw = us.assign(key=us["ATERIO_DATA_CENTER_CAMPUS_UID"].fillna(us["ATERIO_DATA_CENTER_UID"])).groupby("key")["MW"].sum()
    cc = c.groupby("key").agg(cost=("cost", "max"), costs=("cost", "nunique"), n=("cost", "size"),
                              name=("DATA_CENTER_CAMPUS_NAME", "first"), bname=("DATA_CENTER_BUILDING_NAME", "first"),
                              prov=("PROVIDER_NAME", "first"), st=("STATE_CODE", "first"),
                              stage=("DATA_CENTER_STAGE", lambda s: s.mode().iloc[0]),
                              grp=("grp", lambda s: s.mode().iloc[0]), ann=("ann_d", "min")).reset_index()
    cc["mw"] = cc["key"].map(camp_mw).fillna(0.0)
    cc = cc[(cc["cost"] > 0) & (cc["mw"] > 0)].copy()
    cc["mpm"] = cc["cost"] / cc["mw"] / 1e6
    naive = float(c["cost"].sum())
    bins = [(0, 2, "<$2M"), (2, 5, "$2-5M"), (5, 10, "$5-10M"), (10, 15, "$10-15M"), (15, 25, "$15-25M"),
            (25, 50, "$25-50M"), (50, 1e9, ">$50M")]
    hist = []
    for lo, hi, lab in bins:
        m = (cc["mpm"] >= lo) & (cc["mpm"] < hi)
        hist.append({"label": lab, **{g: int((m & (cc["grp"] == g)).sum()) for g in GROUPS}})
    sane = cc[(cc["mpm"] >= 2) & (cc["mpm"] <= 50)]
    ann_y = cc["ann"].dt.year
    med_y = []
    for y in range(2020, asof_ts.year + 1):
        s = sane[sane["ann"].dt.year == y]
        if len(s) >= 5:
            med_y.append({"year": y, "n": int(len(s)), "median": round(float(s["mpm"].median()), 1),
                          "wavg": round(float(s["cost"].sum() / s["mw"].sum() / 1e6), 1)})
    top = cc.sort_values("cost", ascending=False).head(20)
    P["cost"] = {"bld_fill": round(float(us["TOT_PROJECT_COST"].notna().mean()), 3), "campuses": int(len(cc)),
                 "naive_tn": round(naive / 1e12, 2), "dedup_tn": round(float(cc["cost"].sum()) / 1e12, 2),
                 "multi_value_campuses": int((cc["costs"] > 1).sum()),
                 "median_mpm": round(float(cc["mpm"].median()), 1), "sane_median": round(float(sane["mpm"].median()), 1),
                 "sane_n": int(len(sane)),
                 "by_grp": {g: {"n": int((sane["grp"] == g).sum()),
                                "median": round(float(sane.loc[sane["grp"] == g, "mpm"].median()), 1) if (sane["grp"] == g).any() else None,
                                "bn": round(float(cc.loc[cc["grp"] == g, "cost"].sum()) / 1e9, 0)} for g in GROUPS},
                 "hist": hist, "by_year": med_y,
                 "top": [{"name": clean(r.name) or clean(r.bname), "prov": clean(r.prov), "st": clean(r.st), "stage": r.stage,
                          "mw": round(float(r.mw)), "bn": round(float(r.cost) / 1e9, 1), "mpm": round(float(r.mpm), 1),
                          "n": int(r.n)} for r in top.itertuples()]}

    # ---------------- execution: durations, conversion, progress
    a2s = us[us["ann_d"].notna() & us["cs_d"].notna() & (us["cs_d"] >= us["ann_d"])]
    dur_start = [{"year": int(y), "n": int(len(d)), "median_m": round(float(((d["cs_d"] - d["ann_d"]).dt.days / 30.44).median()), 1)}
                 for y, d in a2s.groupby(a2s["cs_d"].dt.year) if 2018 <= y <= asof_ts.year and len(d) >= 5]
    s2a = us[(us["grp"] == "active") & us["cs_d"].notna() & us["act"].notna() & (us["act"] > us["cs_d"])]
    dur_build = [{"year": int(y), "n": int(len(d)), "median_m": round(float(((d["act"] - d["cs_d"]).dt.days / 30.44).median()), 1)}
                 for y, d in s2a.groupby(s2a["act"].dt.year) if 2018 <= y <= asof_ts.year and len(d) >= 5]
    uc_plan = us[(us["grp"] == "uc") & us["cs_d"].notna() & us["act"].notna() & (us["act"] > us["cs_d"])]
    conv = []
    for y in range(2019, asof_ts.year + 1):
        d = us[us["ann_d"].dt.year == y]
        if not len(d):
            continue
        conv.append({"year": y, "n": int(len(d)), "gw": gw(d["MW"].sum()),
                     **{g: gw(d.loc[d["grp"] == g, "MW"].sum()) for g in GROUPS},
                     **{"n_" + g: int((d["grp"] == g).sum()) for g in GROUPS}})
    pct = pd.to_numeric(us["PCT_CONSTRUCTION_STATUS"], errors="coerce")
    ucm = us["grp"] == "uc"
    pb = [(None, None, "Not reported"), (0, 0, "0%"), (0.0001, 0.25, "1-25%"), (0.2501, 0.5, "26-50%"),
          (0.5001, 0.75, "51-75%"), (0.7501, 0.9999, "76-99%"), (1, 1, "100%")]
    prog = []
    for lo, hi, lab in pb:
        m = pct.isna() if lo is None else (pct >= lo) & (pct <= hi)
        prog.append({"label": lab, "n": int((m & ucm).sum()), "gw": gw(us.loc[m & ucm, "MW"].sum()),
                     "by_year": {str(int(y)): gw(v) for y, v in us[m & ucm].groupby("y")["MW"].sum().items()}})
    P["execution"] = {"dur_start": dur_start, "dur_build": dur_build,
                      "uc_plan_m": round(float(((uc_plan["act"] - uc_plan["cs_d"]).dt.days / 30.44).median()), 1) if len(uc_plan) else None,
                      "uc_plan_n": int(len(uc_plan)), "conv": conv, "progress": prog,
                      "like_by_grp": {g: {k: gw(us.loc[(us["grp"] == g) & (us["like"] == k), "MW"].sum())
                                          for k in ["High", "Medium", "Low", "Unrated"]} for g in GROUPS}}

    # ---------------- risk by state
    P["risk_states"] = sorted([{"st": s, "delayed": v["delayed"], "wd": v["wd"], "n_delayed": v["n_delayed"], "n_wd": v["n_wd"],
                                "ann": v["ann"], "uc": v["uc"]} for s, v in states.items()],
                              key=lambda r: -(r["delayed"] + r["wd"]))[:20]

    # ---------------- fields guide (fill rate, level, description)
    dic = read_dictionary(os.path.join(src, "data-centers", "inventory", "Data Centers Data Dictionary.xlsx"))
    inv_cols = [c for c in raw.columns if c not in ("MW", "MWf", "grp")]
    fields = []
    for c in inv_cols:
        dd = dic.get(c, {})
        fields.append({"f": c, "fill": round(float(us[c].notna().mean()), 3),
                       "fill_uc": round(float(us.loc[us["grp"] == "uc", c].notna().mean()), 3),
                       "level": dd.get("level", ""), "type": dd.get("type", ""), "desc": dd.get("desc", "")[:260],
                       "example": dd.get("example", "")})
    P["fields"] = fields

    # ---------------- files map
    def fsize(p):
        try:
            return os.path.getsize(p)
        except OSError:
            return 0
    files = []
    files.append({"path": os.path.relpath(inv_path, src), "kind": "inventory", "rows": int(len(raw)), "size": fsize(inv_path),
                  "asof": asof, "what": "Building-level census: one row per data-center building (US + Canada), 77 fields: stage, power (published, Aterio estimate, selected, critical IT), dates, provider, tenants, utility, balancing authority, cost, links, notes."})
    files.append({"path": os.path.relpath(ev_path, src), "kind": "events", "rows": P["events"]["rows"], "size": fsize(ev_path),
                  "asof": ev_asof, "what": "Event log: one row per building per milestone (announced, construction started, 5-95% progress reads from satellite, finished, active, delayed, withdrawn, cancelled). Joins to the inventory on ATERIO_DATA_CENTER_UID."})
    files.append({"path": "data-centers/inventory/monthly-history/<date>/", "kind": "history", "rows": len(hist_dirs), "size": sum(fsize(p) for d in hist_dirs for p in glob.glob(os.path.join(d, "*.csv"))),
                  "asof": f"{dates[0]} to {[d for d in dates if d != asof][-1]}" if len(dates) > 1 else "",
                  "what": "Month-end point-in-time copies of the inventory and events (same schema). They show what Aterio knew at each date, so comparing them reveals stage moves, date slips and coverage added."})
    files.append({"path": "data-centers/inventory/quarterly-history/<date>/", "kind": "history", "rows": len(glob.glob(os.path.join(src, "data-centers", "inventory", "quarterly-history", "*"))),
                  "size": sum(fsize(p) for p in glob.glob(os.path.join(src, "data-centers", "inventory", "quarterly-history", "*", "*.csv"))),
                  "asof": "", "what": "Quarter-end subset of the monthly history (byte-identical copies of the matching month-ends). Nothing new; kept for convenience."})
    files.append({"path": "data-centers/inventory/Data Centers Data Dictionary.xlsx", "kind": "dictionary", "rows": len(dic), "size": fsize(os.path.join(src, "data-centers", "inventory", "Data Centers Data Dictionary.xlsx")),
                  "asof": "", "what": "Field guide for the inventory and events files: type, building vs campus level, description, example."})
    wr = os.path.join(src, "data-centers", "reports", "Aterio US Data Centers Weekly Report.xlsx")
    files.append({"path": os.path.relpath(wr, src), "kind": "report", "rows": len(W.get("sheets", [])), "size": fsize(wr),
                  "asof": (W.get("d30") or [{}])[0].get("updated_at", ""),
                  "what": "Aterio's own Excel report: 30-day deltas by stage, a cumulative activation forecast (optimistic / baseline / conservative) by state, ISO, provider and utility, a monthly momentum series rebuilt with today's knowledge, ISO demand vs DC capacity, cancellations, conversion and days-to-start tables, generator demand."})
    files.append({"path": os.path.relpath(bp, src), "kind": "btm", "rows": int(len(b)), "size": fsize(bp), "asof": b_asof,
                  "what": "Behind-the-meter / dedicated generation for data centers: one row per plant phase (project > plant > phase), technology, fuel, nameplate MW, stage, developer, customer, equipment suppliers, dates."})
    dcb_path = latest(os.path.join(btm_dir, "data_center_with_behind_the_meter_*.csv"))[0]
    files.append({"path": os.path.relpath(dcb_path, src), "kind": "btm", "rows": int(len(dcb)), "size": fsize(dcb_path), "asof": b_asof,
                  "what": "The inventory rows (same 77 fields) of the data centers linked to a BTM generation project (join on ATERIO_POWER_GENERATION_PROJECT_UID)."})
    P["files"] = files

    # ---------------- reconciliation of the 'GW under construction' numbers
    campuses_uc = set(us.loc[us["grp"] == "uc", "ATERIO_DATA_CENTER_CAMPUS_UID"].dropna())
    cm = us["ATERIO_DATA_CENTER_CAMPUS_UID"].isin(campuses_uc) & us["y"].between(2026, 2030)
    uc_nocamp = us[(us["grp"] == "uc") & us["ATERIO_DATA_CENTER_CAMPUS_UID"].isna() & us["y"].between(2026, 2030)]
    P["recon"] = {"uc": gw(us.loc[us["grp"] == "uc", "MW"].sum()),
                  "uc_delayed": gw(us.loc[us["grp"].isin(["uc", "delayed"]), "MW"].sum()),
                  "campus_2630": gw(us.loc[cm, "MW"].sum()),
                  "campus_2630_by_grp": {g: gw(us.loc[cm & (us["grp"] == g), "MW"].sum()) for g in GROUPS},
                  "uc_nocampus_2630": gw(uc_nocamp["MW"].sum())}

    # ---------------- explorer rows
    rows = []
    xy = bdd.albers_lower48()
    for r in us.sort_values("MW", ascending=False).itertuples():
        lat, lon = r.LOCATION_LATITUDE, r.LOCATION_LONGITUDE
        px = py_ = None
        if r.STATE_CODE not in ("AK", "HI", "PR") and pd.notna(lat) and pd.notna(lon):
            px, py_ = xy(float(lon), float(lat))
            px, py_ = round(px, 1), round(py_, 1)
        note = ""
        if r.grp != "active":  # keep the latest two dated note lines for pipeline rows (size)
            lines = [ln.strip() for ln in clean(r.NOTES).splitlines() if ln.strip()]
            note = " | ".join(lines[-2:])
            note = note[:320] + ("…" if len(note) > 320 else "")
        rows.append([clean(r.DATA_CENTER_BUILDING_NAME), clean(r.DATA_CENTER_CAMPUS_NAME), clean(r.PROVIDER_NAME), clean(r.tick),
                     clean(r.STATE_CODE), clean(r.COUNTY_NAME), clean(r.CITY_NAME), r.DATA_CENTER_STAGE,
                     round(float(r.MW), 1), round(float(r.IT), 1) if pd.notna(r.IT) else None, ym(r.act),
                     {"High": "H", "Medium": "M", "Low": "L"}.get(r.like, ""), 1 if r.ai else 0, 1 if r.btm else 0,
                     clean(r.UTILITY_NAME), clean(r.BAL_AUTH_ABBR), clean(r.END_USER_COMPANIES), ym(r.ann_d), ym(r.cs_d),
                     None if pd.isna(r.PCT_CONSTRUCTION_STATUS) else round(float(r.PCT_CONSTRUCTION_STATUS) * 100),
                     px, py_, note, 1 if clean(r.PROV_PUB_TOT_POWER_CAPACITY_MW) != "" else 0])
    P["row_cols"] = ["name", "campus", "provider", "tick", "st", "county", "city", "stage", "mw", "it", "act", "like", "ai",
                     "btm", "utility", "ba", "users", "ann", "cs", "pct", "x", "y", "notes", "pub"]
    P["rows"] = rows
    P["wiki_tickers"] = sorted(t for t in wt if t in set(us["tick"]))
    return P


def takeaways(P: dict) -> list[str]:
    st = {s["grp"]: s for s in P["stages"]}
    def g(k):
        return sum(s["gw"] for s in P["stages"] if s["grp"] == k)
    uc, ann, act = g("uc"), g("ann"), g("active")
    ucy = P["timeline"]["uc_by_year"]
    asof_y = P["asof"][:4]
    c = P["comparisons"].get(P["default_base"])
    hi = sum(s["like"]["High"] for s in P["stages"] if s["grp"] == "ann")
    out = [
        f"<b>{uc:.1f} GW of facility power is under construction</b> across {sum(s['n'] for s in P['stages'] if s['grp']=='uc'):,} buildings (≈{uc / P['it_ratio']:.0f} GW IT-equivalent). Aterio dates {ucy.get(asof_y, 0):.1f} GW of it to {asof_y}, {ucy.get(str(int(asof_y)+1), 0):.1f} GW to {int(asof_y)+1} and {ucy.get(str(int(asof_y)+2), 0):.1f} GW to {int(asof_y)+2}.",
        f"<b>The announced pipeline ({ann:.0f} GW) is {ann / uc:.1f}× what is being built.</b> Aterio rates {hi / ann:.0%} of it high-likelihood. Its own forecast puts {next((f['base'] for f in P['weekly'].get('forecast', []) if f['year'] == int(asof_y) + 2), 0):.0f} GW cumulative online by end-{int(asof_y)+2} (baseline), against {act:.0f} GW active today.",
    ]
    if c:
        out.append(f"<b>Part of the growth is coverage, not new projects.</b> Since {c['base']} the census added {c['new']['n']:,} buildings / {c['new']['gw']:.0f} GW. {c['new']['before']['gw']:.0f} GW of that was announced before {c['base']}, so it was backfilled.")
        s = c["slip"]["uc"]
        out.append(f"<b>Dates slip.</b> Of the {s['gw']:.1f} GW that was under construction on {c['base']} and dated after it, {s['share_later']:.0%} (MW-weighted) now carries a later activation date. The median slip is {s['median']:.0f} months. Of the {c['due']['gw']:.1f} GW that was due to go live by {P['asof']}, {c['due']['now']['active']:.1f} GW is active.")
    top3 = sorted(P["states"].items(), key=lambda kv: -kv[1]["uc"])[:3]
    out.append(f"<b>Construction is concentrated.</b> {', '.join(k for k, _ in top3)} hold {sum(v['uc'] for _, v in top3) / uc:.0%} of construction GW. Hyperscaler self-builds (AMZN, GOOG, META, MSFT, ORCL, AAPL as provider) are {P['hs_share_uc']:.0%} of it.")
    bt = P["btm"]
    gas = next((s["gw"] for s in bt["sources"] if s["src"] == "Natural Gas"), 0)
    out.append(f"<b>Onsite power is a gas story.</b> {bt['gw']:.0f} GW of behind-the-meter generation phases are tracked, {gas / bt['gw']:.0%} natural gas, but only {bt['by_grp']['active'] + bt['by_grp']['uc']:.0f} GW is active or under construction. {bt['dc']['n']:,} data-center buildings link to one.")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    a = ap.parse_args()
    src = find_src(a.src)
    P = build(src)
    P["takeaways"] = takeaways(P)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    summ = {k: v for k, v in P.items() if k not in ("rows", "map", "btm")}
    summ["btm"] = {k: v for k, v in P["btm"].items() if k != "phases"}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(summ, f, ensure_ascii=False, indent=1, default=str)
    tpl = open(TEMPLATE, encoding="utf-8").read()
    payload = json.dumps(P, ensure_ascii=False, separators=(",", ":"), default=str).replace("</", "<\\/")
    html = tpl.replace("/*__DATA__*/null", payload)
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"as of {P['asof']} | US rows {P['totals']['n']:,} | wrote {OUT_HTML} ({len(html)/1e6:.2f} MB) + {OUT_JSON}")


if __name__ == "__main__":
    main()
