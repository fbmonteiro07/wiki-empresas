"""Capstone treatment of the Aterio data-center census -> _wiki/_data/aterio/capstone_view.json

Rules live in _wiki/_data/aterio/treatment.json (decided by Felipe 2026-11-09):
  headline basis   IT-eq = facility MW ÷ Aterio's own facility/IT median (buildings carrying both fields)
  universe         buildings activated in the window that are already Active (went live since Jan of the window start),
                   + Construction + Delayed, + Announcement / Land Bank rated High likelihood
  exclusion        campuses rated Low likelihood with no named end user, in every stage
  dates            DATA_CENTER_ACTIVATION_DATE as Aterio publishes it (no extra haircut)
Everything is US, building level, summed per activation year; campus key = campus UID, else building UID. Likelihood
is read per building as Aterio records it (a campus field, but 36 US campuses carry mixed values; the variants are in
'sens'). Rows with no MW count as zero (count and a fill estimate are in 'sens').

The output also carries: what Aterio dates to the window with no filter ("raw", includes buildings already live), what
each rule removed, the largest campuses removed, a by-state table, sensitivity of the total to the load-bearing choices
(facility/IT statistic, mixed-likelihood campuses, rows with no MW, tenant requirement), and how firm the dates are:
the same rules applied to earlier monthly exports ('vintages', cached in capstone_vintages.json — snapshots never
change) and delivery of earlier cohorts ('cohorts'). Guardrails are reported, never fitted to. Findings of the
2026-11-09 double-check (PARTIAL) are folded in here.

usage: py aterio_capstone_view.py [--src <Aterio folder>]   (build_dc_delay.py calls run() on every build)
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # _wiki
sys.path.insert(0, HERE)
import aterio_core as core  # noqa: E402

OUT = os.path.join(ROOT, "_data", "aterio", "capstone_view.json")
VINT = os.path.join(ROOT, "_data", "aterio", "capstone_vintages.json")
# The loader, the rule masks and the constants live in aterio_core.py, shared by every Aterio builder. The names stay
# importable from here (build_dc_delay and older callers use V.load / V.masks / V.RULES / V.RANK).
RULES, COLS, RANK, UNRANK, LIVE = core.RULES, core.COLS, core.RANK, core.UNRANK, core.LIVE
load, masks = core.load, core.masks


def vintages(rules: dict, k: float, inv: str, cur, asof: str) -> tuple[list, dict, dict]:
    """Same rules on earlier monthly exports (every other month-end over the last 12 months) + delivery of earlier
    cohorts, joined to the current export by building UID. Snapshot results are cached (snapshots never change);
    cohorts are cached per current export date."""
    import pandas as pd
    hist = os.path.join(os.path.dirname(inv), "monthly-history")
    files = sorted(glob.glob(os.path.join(hist, "*", "data_center_inventory_*.csv")))
    tag = lambda f: re.search(r"(\d{8})", os.path.basename(f)).group(1)
    cur_tag = asof.replace("-", "")
    rkey = hashlib.sha1(json.dumps({"i": rules["include"], "x": rules["exclude"], "w": rules["window"], "k": k},
                                   sort_keys=True).encode()).hexdigest()[:10]
    cache = json.load(open(VINT, encoding="utf-8")) if os.path.exists(VINT) else {}
    if cache.get("rules_key") != rkey:
        cache = {"rules_key": rkey, "snaps": {}, "cohorts": {}}
    y0, y1 = rules["window"]
    lo = f"{int(cur_tag[:4]) - 1}{cur_tag[4:]}"
    pick = [f for f in files if lo <= tag(f) < cur_tag and int(tag(f)[4:6]) % 2 == int(cur_tag[4:6]) % 2]
    loaded = {}

    def snap(f):
        t = tag(f)
        if t not in loaded:
            loaded[t] = load(f)
        return loaded[t]

    for f in pick:
        t = tag(f)
        if t in cache["snaps"]:
            continue
        d = snap(f)
        if not d["like"].ne("").any():
            cache["snaps"][t] = {"n_a": "no likelihood field"}
            continue
        m = masks(d, rules)
        kd, rd, act = d[m["keep"]], d[m["raw"]], d[d["DATA_CENTER_STAGE"] == "Active"]
        cache["snaps"][t] = {"by_year": {str(y): round(float(kd.loc[kd["yr"] == y, "mw"].sum()) / 1000 / k, 2) for y in range(y0, y1 + 1)},
                             "it": round(float(kd["mw"].sum()) / 1000 / k, 2), "raw_it": round(float(rd["mw"].sum()) / 1000 / k, 2),
                             "act_seen": {str(y): round(float(act.loc[act["yr"] == y, "mw"].sum()) / 1000 / k, 2) for y in range(y0 - 2, y0)}}
    rows = [{"asof": f"{t[:4]}-{t[4:6]}-{t[6:]}", **v} for t, v in sorted(cache["snaps"].items()) if t in {tag(f) for f in pick} and "by_year" in v]

    # cohorts: (1) construction dated last full year at the Dec before it; (2) construction dated Jan..asof of this year at last Dec;
    # (3) announced High dated next year at last Dec
    coh = cache["cohorts"].get(cur_tag)
    if coh is None:
        coh = {}
        yc = int(cur_tag[:4])
        cur_i = cur.set_index("ATERIO_DATA_CENTER_UID")[["DATA_CENTER_STAGE", "yr", "dt"]]
        f_prev2 = next((f for f in files if tag(f) == f"{yc - 2}1231"), None)
        f_prev1 = next((f for f in files if tag(f) == f"{yc - 1}1231"), None)

        def join(d):
            return d.join(cur_i, on="ATERIO_DATA_CENTER_UID", rsuffix="_now")

        if f_prev2:
            d = snap(f_prev2)
            c = join(d[(d["DATA_CENTER_STAGE"] == "Construction") & (d["yr"] == yc - 1)])
            ok = c["DATA_CENTER_STAGE_now"].eq("Active") & (c["yr_now"] <= yc - 1)
            coh["uc_last_year"] = {"snap": f"{yc - 2}-12-31", "year": yc - 1, "gw_it": round(float(c["mw"].sum()) / 1000 / k, 2),
                                   "live_it": round(float(c.loc[ok, "mw"].sum()) / 1000 / k, 2)}
        if f_prev1:
            d = snap(f_prev1)
            c = join(d[(d["DATA_CENTER_STAGE"] == "Construction") & (d["dt"] >= f"{yc}-01-01") & (d["dt"] <= asof)])
            ok = c["DATA_CENTER_STAGE_now"].eq("Active") & (c["dt_now"] <= asof)
            moved = c["DATA_CENTER_STAGE_now"].isin(LIVE) & (c["yr_now"] > yc)
            coh["uc_this_year"] = {"snap": f"{yc - 1}-12-31", "to": asof, "gw_it": round(float(c["mw"].sum()) / 1000 / k, 2),
                                   "live_it": round(float(c.loc[ok, "mw"].sum()) / 1000 / k, 2),
                                   "moved_next_year_it": round(float(c.loc[moved, "mw"].sum()) / 1000 / k, 2)}
            c = join(d[d["DATA_CENTER_STAGE"].isin(["Announcement", "Land Bank"]) & (d["like"] == "High") & (d["yr"] == yc + 1)])
            same = c["DATA_CENTER_STAGE_now"].isin(LIVE) & (c["yr_now"] == yc + 1)
            gone = c["DATA_CENTER_STAGE_now"].isna()
            coh["ann_high_next_year"] = {"snap": f"{yc - 1}-12-31", "year": yc + 1, "gw_it": round(float(c["mw"].sum()) / 1000 / k, 2),
                                         "still_dated_it": round(float(c.loc[same, "mw"].sum()) / 1000 / k, 2),
                                         "left_census_it": round(float(c.loc[gone, "mw"].sum()) / 1000 / k, 2)}
        cache["cohorts"] = {cur_tag: coh}
    with open(VINT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=1)
    return rows, coh, cache


def run(src: str | None = None) -> dict:
    rules = core.rules()
    inv, asof = core.find_inventory(src)
    a = load(inv)
    fi = core.ratio(a, rules)                      # rule 1: measured on this export, statistic named in treatment.json
    k, k_med, k_w, k_w_ne1 = fi["k"], fi["median"], fi["weighted"], fi["weighted_excl_eq1"]
    y0, y1 = rules["window"]
    inc = rules["include"]
    stage = a["DATA_CENTER_STAGE"]
    m = masks(a, rules)
    a["bucket"] = ""
    a.loc[m["act"], "bucket"] = "online"
    a.loc[m["bld"] & (stage == "Construction"), "bucket"] = "building"
    a.loc[m["bld"] & (stage == "Delayed"), "bucket"] = "delayed"
    a.loc[m["ann"], "bucket"] = "announced"
    raw, kept = a[m["raw"]], a[m["keep"]]
    g = lambda s: round(float(s.sum()) / 1000.0, 2)
    it = lambda s: round(float(s.sum()) / 1000.0 / k, 2)
    years = list(range(y0, y1 + 1))

    def by_year(df):
        out = {}
        for y in years:
            d = df[df["yr"] == y]
            out[str(y)] = {b: it(d.loc[d["bucket"] == b, "mw"]) for b in ("online", "building", "delayed", "announced")}
            out[str(y)]["total"] = it(d["mw"])
        return out

    # what each rule removed (in the window)
    rm_ann = raw[(raw["bucket"] == "announced") & ~raw["like"].isin(inc["announced_likelihood"])]
    rm_ann_by = {lk or "unrated": it(rm_ann.loc[rm_ann["like"] == lk, "mw"]) for lk in sorted(rm_ann["like"].unique())}
    low_nt = m["low_nt"]
    rm_low = raw[low_nt.loc[raw.index] & raw["bucket"].isin(["online", "building", "delayed"])]
    rm_low_ann_hi = raw[low_nt.loc[raw.index] & (raw["bucket"] == "announced") & raw["like"].isin(inc["announced_likelihood"])]
    undated = a[stage.isin(inc["building_stages"] + inc["announced_stages"]) & a["yr"].isna()]
    after = a[stage.isin(inc["building_stages"] + inc["announced_stages"]) & (a["yr"] > y1)]
    rem = raw[~m["keep"].loc[raw.index]].copy()
    rem["why"] = [("Low likelihood, no tenant" if low_nt.loc[i] else f"Announced, {lk or 'unrated'} likelihood") for i, lk in zip(rem.index, rem["like"])]
    removed_top = []
    for key, d in rem.groupby("key"):
        removed_top.append({"campus": str(d["campus"].iloc[0]), "st": str(d["STATE_CODE"].iloc[0]),
                            "prov": str(d["PROVIDER_NAME"].dropna().iloc[0]) if d["PROVIDER_NAME"].notna().any() else "",
                            "stages": ", ".join(sorted(set(d["DATA_CENTER_STAGE"]))),
                            "like": " / ".join(sorted({x or "unrated" for x in d["like"]}, key=lambda x: -RANK.get(x, 0))),
                            "it": it(d["mw"]), "why": "; ".join(sorted(set(d["why"])))})
    removed_top = sorted(removed_top, key=lambda r: -r["it"])[:25]

    # sensitivity of the total to the load-bearing choices (facility -> IT-eq at k unless stated)
    kept_fac = float(kept["mw"].sum()) / 1000
    rank = a["like"].map(RANK)
    lk_hi = rank.groupby(a["key"]).transform("max").map(UNRANK).fillna("")
    lk_lo = rank.groupby(a["key"]).transform("min").map(UNRANK).fillna("")
    mixed_keys = raw.groupby("key")["like"].agg(lambda s: len({x for x in s if x}) > 1)
    mixed_keys = set(mixed_keys[mixed_keys].index)
    tot = lambda mk: round(float(a.loc[mk, "mw"].sum()) / 1000 / k, 2)
    miss = m["keep"] & a["mw_raw"].isna()
    nz = a[m["keep"] & (a["mw"] > 0)]
    fill = a.loc[miss, "key"].map(nz.groupby("key")["mw"].median()).fillna(a.loc[miss, "bucket"].map(nz.groupby("bucket")["mw"].median()))
    camp_user = a["user"].groupby(a["key"]).transform("any")
    ann_hi = kept[kept["bucket"] == "announced"]
    sens = {
        "fac_it": {"median": round(k_med, 3), "weighted": round(k_w, 3), "weighted_excl_eq1": round(k_w_ne1, 3), "n": fi["n"],
                   "n_eq1": fi["n_eq1"],
                   "total_weighted": round(kept_fac / k_w, 2), "total_weighted_excl_eq1": round(kept_fac / k_w_ne1, 2)},
        "mixed_likelihood": {"campuses": len(mixed_keys), "raw_it": it(raw.loc[raw["key"].isin(mixed_keys), "mw"]),
                             "total_campus_highest": tot(masks(a, rules, lk_hi)["keep"]), "total_campus_lowest": tot(masks(a, rules, lk_lo)["keep"])},
        "missing_mw": {"rows": int(miss.sum()), "by_bucket": {b: int(n) for b, n in a.loc[miss, "bucket"].value_counts().items()},
                       "fill_it": round(float(fill.sum()) / 1000 / k, 2)},
        "tenant": {"kept_no_tenant_on_campus_it": it(kept.loc[~camp_user.loc[kept.index], "mw"]),
                   "building_no_tenant_on_campus_it": it(kept.loc[kept["bucket"].isin(["building", "delayed"]) & ~camp_user.loc[kept.index], "mw"]),
                   "ann_high_it": it(ann_hi["mw"]), "ann_high_no_user_it": it(ann_hi.loc[~ann_hi["user"], "mw"]),
                   "total_if_ann_high_needs_tenant": round((float(kept["mw"].sum()) - float(ann_hi.loc[~ann_hi["user"], "mw"].sum())) / 1000 / k, 2)},
        "low_no_tenant_by_stage": {s: it(d["mw"]) for s, d in raw[low_nt.loc[raw.index]].groupby("DATA_CENTER_STAGE")},
    }
    # dates sitting on Dec-30/31 (slip a calendar year if one day late)
    dec = kept[(kept["dt"].dt.month == 12) & (kept["dt"].dt.day >= 30)]
    sens["dec_end_dated_it"] = {str(y): it(dec.loc[dec["yr"] == y, "mw"]) for y in years}

    # states
    st_rows = []
    for st, d in kept.groupby("STATE_CODE"):
        r = raw[raw["STATE_CODE"] == st]
        st_rows.append({"st": st, "it": it(d["mw"]), "fac": g(d["mw"]), "raw_it": it(r["mw"]),
                        "building": it(d.loc[d["bucket"].isin(["building", "delayed"]), "mw"]),
                        "online": it(d.loc[d["bucket"] == "online", "mw"]),
                        "announced": it(d.loc[d["bucket"] == "announced", "mw"]),
                        "by_year": {str(y): it(d.loc[d["yr"] == y, "mw"]) for y in years}})
    st_rows.sort(key=lambda r: -r["it"])

    # campuses kept under the house rules, MW IT-eq by activation year x bucket (feeds the dc-delay-risk "GW added by
    # state" waterfall on the Aterio base and its state drilldown; the page aggregates states from these rows)
    first = lambda s: str(s.dropna().iloc[0]).strip() if s.notna().any() else ""
    camps = []
    for key, d in kept.groupby("key"):
        y = {}
        for (yr, b), mw in d.groupby(["yr", "bucket"])["mw"].sum().items():
            if mw > 0:
                y.setdefault(str(int(yr)), {})[b] = round(float(mw) / k, 1)
        if not y:
            continue
        users = sorted({u.strip() for x in d["END_USER_COMPANIES"].dropna() for u in str(x).split(",") if u.strip()})
        dts = d["dt"].dropna()
        camps.append({"k": str(key), "st": first(d["STATE_CODE"]), "n": first(d["campus"]), "p": first(d["PROVIDER_NAME"]),
                      "u": ", ".join(users)[:90], "c": first(d["CITY_NAME"]), "co": first(d["COUNTY_NAME"]),
                      "lk": " / ".join(sorted({x for x in d["like"] if x}, key=lambda x: -RANK.get(x, 0))),
                      "d": [dts.min().strftime("%Y-%m"), dts.max().strftime("%Y-%m")] if len(dts) else ["", ""],
                      "nb": int(len(d)), "y": y})
    camps.sort(key=lambda c: -sum(sum(v.values()) for v in c["y"].values()))

    # guardrails: Aterio's own record of buildings that went live (revised up later as Aterio backfills)
    act = a[stage == "Active"]
    pace = {str(int(y)): it(act.loc[act["yr"] == y, "mw"]) for y in range(2022, y0 + 1)}
    m_asof = int(asof[5:7])
    yb = by_year(kept)
    guard = {
        "pace_online_it": pace,
        "pace_note": f"IT-eq GW of buildings Aterio shows as Active, by activation year; {y0} covers Jan-{asof[5:7]} only ({m_asof} months).",
        "y0_run_rate_it": round(pace.get(str(y0), 0) * 12 / m_asof, 2) if m_asof else None,
        "next_year_vs_last_full_year": round(yb[str(y0 + 1)]["total"] / pace[str(y0 - 1)], 2) if pace.get(str(y0 - 1)) else None,
        "peak_year": max(years, key=lambda y: yb[str(y)]["total"]),
        "peak_vs_last_full_year": round(max(yb[str(y)]["total"] for y in years) / pace[str(y0 - 1)], 2) if pace.get(str(y0 - 1)) else None,
    }
    vint, coh = [], {}
    try:
        vint, coh, _ = vintages(rules, k, inv, a, asof)
    except Exception as e:  # noqa: BLE001 - history folder optional
        guard["vintage_error"] = f"{type(e).__name__}: {e}"[:200]
    vint = vint + [{"asof": asof, "by_year": {y: v["total"] for y, v in yb.items()}, "it": it(kept["mw"]), "raw_it": it(raw["mw"]),
                    "act_seen": {str(y): pace.get(str(y)) for y in range(y0 - 2, y0)}}]
    return {
        "asof": asof, "inventory": os.path.basename(inv), "built_by": "aterio_capstone_view.py", "rules": rules,
        "fac_it": k, "fac_it_n": fi["n"], "fac_it_measured": round(k_med, 3),
        "window": [y0, y1],
        "us": {"it": it(kept["mw"]), "fac": g(kept["mw"]), "by_year": yb,
               "buckets": {b: it(kept.loc[kept["bucket"] == b, "mw"]) for b in ("online", "building", "delayed", "announced")}},
        "raw": {"it": it(raw["mw"]), "fac": g(raw["mw"]), "online_it": it(raw.loc[raw["bucket"] == "online", "mw"]), "by_year": by_year(raw)},
        "removed": {"announced_by_likelihood": rm_ann_by, "low_no_tenant_built": it(rm_low["mw"]), "low_no_tenant_announced_high": it(rm_low_ann_hi["mw"]),
                    "undated_pipeline": it(undated["mw"]), "after_window": it(after["mw"]), "top": removed_top},
        "sens": sens, "vintages": vint, "cohorts": coh,
        "states": st_rows, "campuses": camps, "guard": guard,
        "n_buildings": int(len(kept)), "n_campuses": int(kept["key"].nunique()),
    }


def write(out: dict) -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    o = run(ap.parse_args().src)
    write(o)
    u, r = o["us"], o["raw"]
    print(f"Aterio {o['asof']} · Capstone view {u['it']:.1f} GW IT-eq ({u['fac']:.1f} facility) vs raw {r['it']:.1f} IT-eq ({r['fac']:.1f} facility, incl. {r['online_it']:.1f} live) · fac/IT {o['fac_it']} (n={o['fac_it_n']})")
    for y, v in u["by_year"].items():
        print(f"  {y}: {v['total']:6.1f}  (online {v['online']:.1f} · building {v['building']:.1f} · delayed {v['delayed']:.1f} · announced High {v['announced']:.1f})  raw {r['by_year'][y]['total']:.1f}")
    print("  removed:", json.dumps({k: v for k, v in o["removed"].items() if k != "top"}))
    print("  sens:", json.dumps(o["sens"]))
    print("  guard:", json.dumps(o["guard"]))
    print("  vintages:", json.dumps(o["vintages"]))
    print("  cohorts:", json.dumps(o["cohorts"]))
    print("  top removed:", [(x["campus"], x["st"], x["it"], x["why"]) for x in o["removed"]["top"][:6]])
