"""Independent stdlib reconciliation of Meta's Aterio dashboard; no source edits."""
import collections
import csv
import hashlib
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SRC = Path(r"P:\Felipe Monteiro\Aterio\data-centers\inventory\data_center_inventory_20260831.csv")
rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig", newline="")))
us = [r for r in rows if r["COUNTRY_CODE"] == "US"]
num = lambda r, k: float(r.get(k) or 0)
mw = lambda r: num(r, "SELECTED_POWER_CAPACITY_MW")
ci = lambda r: num(r, "CRITICAL_IT_CAPACITY_MW")
year = lambda r: int(r["DATA_CENTER_ACTIVATION_DATE"][:4]) if r["DATA_CENTER_ACTIVATION_DATE"] else 0
key = lambda r: r["ATERIO_DATA_CENTER_CAMPUS_UID"] or r["ATERIO_DATA_CENTER_UID"]
ratio_rows = [r for r in us if mw(r) > 0 and ci(r) > 0]
k = round(statistics.median(mw(r) / ci(r) for r in ratio_rows), 2)
camp = collections.defaultdict(list)
for r in us:
    camp[key(r)].append(r)
excluded = {c for c, rs in camp.items() if any(r["PROJECT_EXECUTION_LIKELIHOOD"] == "Low" for r in rs)
            and not any(r["END_USER_COMPANIES"].strip() or r["PROVIDER_TICKER_NAME"] in ("AMZN", "GOOG", "GOOGL", "META", "MSFT") for r in rs)}
sel = [r for r in us if r["PROVIDER_TICKER_NAME"] == "META" or re.search(r"facebook|\bmeta\b", r["END_USER_COMPANIES"], re.I)]
def house(r):
    return (2026 <= year(r) <= 2030 and key(r) not in excluded and
            (r["DATA_CENTER_STAGE"] in ("Active", "Construction", "Delayed") or
             (r["DATA_CENTER_STAGE"] in ("Announcement", "Land Bank") and r["PROJECT_EXECUTION_LIKELIHOOD"] == "High")))
def medium(r):
    return (2026 <= year(r) <= 2030 and key(r) not in excluded and r["DATA_CENTER_STAGE"] in ("Announcement", "Land Bank")
            and r["PROJECT_EXECUTION_LIKELIHOOD"] == "Medium")
total = lambda rs: sum(mw(r) for r in rs)
live = [r for r in sel if r["DATA_CENTER_STAGE"] in ("Active", "Construction", "Delayed", "Announcement", "Land Bank")]
kept = [r for r in sel if house(r)]
active = [r for r in sel if r["DATA_CENTER_STAGE"] == "Active"]
base = [r for r in active if not house(r)]
construction = [r for r in sel if r["DATA_CENTER_STAGE"] == "Construction"]
uc_keys = {key(r) for r in construction}
campus_build = [r for r in live if r["DATA_CENTER_STAGE"] in ("Construction", "Delayed") or
                (r["DATA_CENTER_STAGE"] in ("Announcement", "Land Bank") and key(r) in uc_keys)]
vals = {
    "operating_facility_mw": total(active), "pre2026_operating_facility_mw": total(base),
    "construction_facility_mw": total(construction), "house_facility_mw": total(kept),
    "house_self_facility_mw": total(r for r in kept if r["PROVIDER_TICKER_NAME"] == "META"),
    "house_tenant_facility_mw": total(r for r in kept if r["PROVIDER_TICKER_NAME"] != "META"),
    "medium_facility_mw": total(r for r in sel if medium(r)),
    "after2030_facility_mw": total(r for r in live if r["DATA_CENTER_STAGE"] != "Active" and year(r) > 2030),
    "undated_facility_mw": total(r for r in live if r["DATA_CENTER_STAGE"] != "Active" and not year(r)),
    "campus_construction_sensitivity_facility_mw": total(campus_build),
}
vals.update({n.replace("facility_mw", "it_eq_gw"): v / k / 1000 for n, v in list(vals.items())})
vals["end2030_it_eq_gw"] = (total(base) + total(kept)) / k / 1000
vals["end2030_with_medium_it_eq_gw"] = vals["end2030_it_eq_gw"] + vals["medium_it_eq_gw"]
vals["house_native_it_else_proxy_sensitivity_gw"] = sum(ci(r) if ci(r) > 0 else mw(r) / k for r in kept) / 1000
vals["house_ratio_1_17_gw"] = total(kept) / 1.17 / 1000
vals["house_ratio_1_27_gw"] = total(kept) / 1.27 / 1000
vals["construction_numeric_gap_vs_bernstein_14_60_gw_basis_unreconciled"] = 14.60 - total(construction) / 1000
percamp = []
for c in {key(r) for r in sel}:
    rs = [r for r in sel if key(r) == c]
    percamp.append({"name": rs[0]["DATA_CENTER_CAMPUS_NAME"], "state": rs[0]["STATE_CODE"],
                    "live_facility_mw": total(r for r in rs if r in live),
                    "house_facility_mw": total(r for r in rs if house(r)),
                    "medium_facility_mw": total(r for r in rs if medium(r)),
                    "after2030_facility_mw": total(r for r in rs if r in live and year(r)>2030),
                    "missing_mw_buildings": sum(not r["SELECTED_POWER_CAPACITY_MW"] for r in rs)})
h = json.loads((ROOT / "_data/aterio/hyperscalers.json").read_text(encoding="utf-8"))
m = next(c for c in h["companies"] if c["id"] == "meta")
checks = {"house_matches_dashboard": abs(vals["house_it_eq_gw"] - m["house"]) < .00051,
          "medium_matches_dashboard": abs(vals["medium_it_eq_gw"] - m["med"]) < .00051,
          "no_duplicate_building_ids": len(sel) == len({r["ATERIO_DATA_CENTER_UID"] for r in sel}),
          "self_tenant_roles_partition_house": abs(vals["house_self_facility_mw"] + vals["house_tenant_facility_mw"] - vals["house_facility_mw"]) < 1e-6}
assert all(checks.values()), checks
result = {"recorded_date": "2026-11-10", "source": str(SRC), "source_asof": "2026-08-31",
          "source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(), "matched_us_buildings": len(sel),
          "live_buildings": len(live), "ratio": {"median_rounded": k, "rows_with_both":len(ratio_rows),
          "rows_equal_to_one":sum(abs(mw(r)/ci(r)-1)<1e-6 for r in ratio_rows)},
          "inputs": {"building_mw_dates_status": "HARD as vendor fields, not independently verified engineering facts",
          "median_1_15": "HARD measured cross-sectional median; ESTIMATE when applied to each Meta building",
          "bernstein_14_60": "Broker chart reading from November 6, 2026; PARTIAL, chart precision and scope unresolved",
          "native_it_sensitivity": "Uses vendor CRITICAL_IT_CAPACITY_MW where positive; field quality not independently validated, not adopted"},
          "values": vals, "checks": checks, "external_checks": {
          "stock": "PARTIAL: independent company total installed stock unavailable; only census bookkeeping validated",
          "flow": "PARTIAL: Bernstein reports a stock under construction, not annual delivery; do not splice into annual adds",
          "construction_benchmark": "UNRECONCILED: later Bernstein/Aterio chart versus August building export; campus classification can also explain part of gap",
          "physical_constant": "1.15 >= 1; plausible facility/IT proxy but 1.000 vendor rows expose basis ambiguity"},
          "notes_only_attribution": [{k:r[k] for k in ("ATERIO_DATA_CENTER_UID", "DATA_CENTER_BUILDING_NAME", "DATA_CENTER_CAMPUS_NAME", "PROVIDER_NAME", "END_USER_COMPANIES", "DATA_CENTER_STAGE", "DATA_CENTER_ACTIVATION_DATE", "SELECTED_POWER_CAPACITY_MW", "NOTES")}
                                     for r in us if r["ATERIO_DATA_CENTER_UID"] == "8c5eb1c4-35bd-452c-9ad7-338657086592"],
          "campuses": sorted(percamp,key=lambda c:-c["live_facility_mw"])}
(OUT / "audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
with (OUT / "meta_buildings.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=sel[0].keys());w.writeheader();w.writerows(sel)
print(json.dumps({k:v for k,v in result.items() if k not in ("campuses","inputs","notes_only_attribution")},indent=2))
