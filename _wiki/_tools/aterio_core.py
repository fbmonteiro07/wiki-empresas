"""Shared loader for the Aterio data-center census. One place that finds the export, reads the inventory, measures the
facility/IT ratio and applies the Capstone house rules, so no builder carries its own copy.

Imported by   aterio_capstone_view.py       house view (US total, states, campuses, sensitivity, vintages)
              build_aterio_hyperscalers.py  Amazon / Google / Meta / Microsoft dashboard + company lookup
              build_aterio_company.py       per-company page sections
              aterio_registry_xchk.py       registry vs census cross-check
              build_aterio_dashboard.py     explorer (keeps its own wide read: it needs Canada and all 77 fields;
                                            source folder, stage groups and the ratio come from here)

House rules live in _wiki/_data/aterio/treatment.json (decided by Felipe 2026-11-09) and are read through rules():
  rule 1  headline basis IT-eq = facility MW ÷ Aterio's own facility/IT median, measured on the export being read
  rule 2  universe = switched on inside the window + Construction + Delayed + Announcement / Land Bank rated High
  rule 3  dates = DATA_CENTER_ACTIVATION_DATE as Aterio publishes it
  rule 4  drop campuses rated Low likelihood whose buildings name no end user, in every stage
No ratio is hardcoded anywhere: fac_it() measures it and reads the statistic to use from treatment.json.

Bases: MW = SELECTED_POWER_CAPACITY_MW = facility power per building. IT-eq = facility ÷ fac_it()["k"]. Rows are
buildings; campus key = campus UID, else the building UID. US only unless country=None.
"""
from __future__ import annotations

import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # _wiki
RULES = os.path.join(ROOT, "_data", "aterio", "treatment.json")
SRC_CANDIDATES = [r"P:\Felipe Monteiro\Aterio", r"\\10.10.10.2\Dados\PesquisaBolsa\Felipe Monteiro\Aterio"]
INV_GLOB = ("data-centers", "inventory", "data_center_inventory_*.csv")
BTM_GLOB = ("power-generation", "behind-the-meter-inventory", "behind_the_meter_power_generation_inventory_*.csv")

# the columns the house view needs (monthly snapshots carry a subset; load() fills the missing ones with None)
COLS = ["COUNTRY_CODE", "SELECTED_POWER_CAPACITY_MW", "CRITICAL_IT_CAPACITY_MW", "DATA_CENTER_ACTIVATION_DATE",
        "DATA_CENTER_STAGE", "PROJECT_EXECUTION_LIKELIHOOD", "END_USER_COMPANIES", "ATERIO_DATA_CENTER_CAMPUS_UID",
        "ATERIO_DATA_CENTER_UID", "DATA_CENTER_CAMPUS_NAME", "DATA_CENTER_BUILDING_NAME", "STATE_CODE", "PROVIDER_NAME",
        "CITY_NAME", "COUNTY_NAME"]
RANK = {"Low": 1, "Medium": 2, "High": 3}
UNRANK = {v: k for k, v in RANK.items()}
LIVE = ["Active", "Construction", "Delayed", "Announcement", "Land Bank"]
GROUP = {"Active": "active", "Construction": "uc", "Delayed": "delayed", "Announcement": "ann",
         "Land Bank": "ann", "Not Approved/Withdrawn": "wd", "Cancelled": "wd"}
# company views only: a hyperscaler self-build names its own tenant for rule 4 (Aterio leaves END_USER_COMPANIES
# empty on owner-operated buildings). The US headline in aterio_capstone_view does not use it (+0.07 GW IT-eq).
SELF_TENANT_TICKERS = ("AMZN", "GOOG", "GOOGL", "META", "MSFT")


# ----------------------------------------------------------------------------- where the export is
def _asof(path: str) -> str:
    d = re.search(r"(\d{8})", os.path.basename(path)).group(1)
    return f"{d[:4]}-{d[4:6]}-{d[6:]}"


def find_src(arg: str | None = None) -> str:
    """The Aterio folder: --src if given, else the P: drive, else the UNC path."""
    for c in ([arg] if arg else []) + SRC_CANDIDATES:
        if c and os.path.isdir(os.path.join(c, "data-centers")):
            return c
    raise FileNotFoundError(f"Aterio folder not found (tried {[arg] + SRC_CANDIDATES})")


def latest(pattern: str) -> tuple[str, str]:
    """Newest file matching a dated pattern -> (path, 'YYYY-MM-DD')."""
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"no file matches {pattern}")
    return files[-1], _asof(files[-1])


def find_inventory(src: str | None = None) -> tuple[str, str]:
    """Newest building inventory -> (path, as-of date)."""
    for c in ([src] if src else []) + SRC_CANDIDATES:
        if not c:
            continue
        files = sorted(glob.glob(os.path.join(c, *INV_GLOB)))
        if files:
            return files[-1], _asof(files[-1])
    raise FileNotFoundError("Aterio inventory not found")


def src_of(inv_path: str) -> str:
    """The Aterio folder an inventory file sits in (so a --src override carries to the other files)."""
    return os.path.dirname(os.path.dirname(os.path.dirname(inv_path)))


def find_btm(src: str | None = None) -> tuple[str, str]:
    """Newest behind-the-meter generation inventory -> (path, as-of date)."""
    return latest(os.path.join(find_src(src), *BTM_GLOB))


def rules() -> dict:
    """The house rules (treatment.json)."""
    with open(RULES, encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------------- the inventory
def load(path: str, cols: list[str] | None = COLS, country: str | None = "US", self_tenant: bool = False):
    """One inventory file (current export or a monthly snapshot) as a building-level frame, index 0..n-1.

    cols = COLS reads only what the house view needs; cols = None reads every field. Derived columns:
      mw_raw  SELECTED_POWER_CAPACITY_MW as a number (NaN where Aterio has none)      mw    the same, NaN -> 0
      dt, yr  activation date and its year                                           act   'YYYY-MM' ('' if undated)
      key     campus UID, else building UID                                          campus  campus name, else building
      like    execution likelihood ('' if unrated)                                   grp   stage group (GROUP)
      user    True where the building names an end user; with self_tenant=True also where the provider is one of
              SELF_TENANT_TICKERS (company views)
    """
    import pandas as pd
    if cols is None:
        a = pd.read_csv(path, low_memory=False)
    else:
        need = list(cols) + (["PROVIDER_TICKER_NAME"] if self_tenant and "PROVIDER_TICKER_NAME" not in cols else [])
        head = set(pd.read_csv(path, nrows=0).columns)
        a = pd.read_csv(path, low_memory=False, usecols=[c for c in need if c in head])
    for c in COLS:
        if c not in a:
            a[c] = None
    if country and a["COUNTRY_CODE"].notna().any():
        a = a[a["COUNTRY_CODE"] == country]
    a = a.copy().reset_index(drop=True)
    a["mw_raw"] = pd.to_numeric(a["SELECTED_POWER_CAPACITY_MW"], errors="coerce")
    a["mw"] = a["mw_raw"].fillna(0.0)
    a["dt"] = pd.to_datetime(a["DATA_CENTER_ACTIVATION_DATE"], errors="coerce")
    a["yr"] = a["dt"].dt.year
    a["act"] = a["dt"].dt.strftime("%Y-%m").fillna("")
    a["key"] = a["ATERIO_DATA_CENTER_CAMPUS_UID"].fillna(a["ATERIO_DATA_CENTER_UID"])
    a["like"] = a["PROJECT_EXECUTION_LIKELIHOOD"].fillna("").astype(str)
    a["campus"] = a["DATA_CENTER_CAMPUS_NAME"].fillna(a["DATA_CENTER_BUILDING_NAME"])
    a["grp"] = a["DATA_CENTER_STAGE"].map(GROUP).fillna("ann")
    a["user"] = a["END_USER_COMPANIES"].fillna("").astype(str).str.strip().ne("")
    if self_tenant and "PROVIDER_TICKER_NAME" in a:
        a["user"] = a["user"] | a["PROVIDER_TICKER_NAME"].fillna("").astype(str).str.upper().isin(SELF_TENANT_TICKERS)
    return a


# ----------------------------------------------------------------------------- rule 1: facility -> IT-eq
def fac_it(mw, ci, rules_: dict | None = None) -> dict:
    """Facility/IT ratio measured on the rows that carry both fields. mw = facility MW, ci = CRITICAL_IT_CAPACITY_MW
    (numeric Series on the same index). 'k' is the ratio to divide by: the statistic named in treatment.json
    basis.fac_it ('median' -> the median rounded to 2 decimals, or a fixed number). The other statistics are returned
    for the sensitivity band only."""
    r = rules_ if rules_ is not None else rules()
    both = (ci > 0) & (mw > 0)
    if not both.any():
        raise ValueError("no building carries both facility and IT MW: the facility/IT ratio cannot be measured")
    ne1 =both & ((mw / ci) - 1).abs().gt(1e-6)
    med = float((mw[both] / ci[both]).median())
    spec = r["basis"].get("fac_it")
    return {"k": round(med, 2) if spec == "median" else float(spec), "median": med,
            "weighted": float(mw[both].sum() / ci[both].sum()),
            "weighted_excl_eq1": float(mw[ne1].sum() / ci[ne1].sum()) if ne1.any() else float("nan"),
            "n": int(both.sum()), "n_eq1": int(both.sum() - ne1.sum())}


def ratio(a, rules_: dict | None = None) -> dict:
    """fac_it() on a frame from load()."""
    import pandas as pd
    return fac_it(a["mw"], pd.to_numeric(a["CRITICAL_IT_CAPACITY_MW"], errors="coerce"), rules_)


def house_ratio(src: str | None = None) -> tuple[float, str]:
    """The rule-1 ratio for code that holds no inventory frame (the delay model converts facility-basis benchmarks
    with it): measured on the newest export; when the export cannot be read (P: offline, a half-copied or locked file,
    no building carrying both fields), the ratio the last house-view run saved in capstone_view.json. Returns
    (k, where it came from). Raises only if neither exists. The ratio follows the export being read (house rule 1)."""
    try:
        inv, asof = find_inventory(src)
        a = load(inv, cols=["COUNTRY_CODE", "SELECTED_POWER_CAPACITY_MW", "CRITICAL_IT_CAPACITY_MW"])
        return ratio(a)["k"], f"measured on the Aterio export of {asof}"
    except Exception as e:  # noqa: BLE001 - the delay page must build whatever state the export is in
        view = os.path.join(ROOT, "_data", "aterio", "capstone_view.json")
        if not os.path.exists(view):
            raise FileNotFoundError("Aterio facility/IT ratio unavailable: the export cannot be read and no saved house view "
                                    "exists (run aterio_capstone_view.py with the Aterio folder mounted)") from e
        with open(view, encoding="utf-8") as fh:
            v = json.load(fh)
        return float(v["fac_it"]), (f"saved by the house view on the Aterio export of {v['asof']} "
                                    f"(export not readable now: {type(e).__name__})")


# ----------------------------------------------------------------------------- rules 2-4: what counts
def masks(a, rules_: dict, like=None) -> dict:
    """Row masks under the house rules, on a frame from load(). like = optional per-row likelihood override
    (campus-level variants). 'keep' is the house view; 'raw' is everything Aterio dates to the window, no filter."""
    import pandas as pd
    lk = a["like"] if like is None else like
    y0, y1 = rules_["window"]
    inc = rules_["include"]
    st = a["DATA_CENTER_STAGE"]
    win = a["yr"].between(y0, y1)
    act = (st == "Active") & win & bool(inc.get("active_activated_in_window"))
    bld = st.isin(inc["building_stages"]) & win
    ann = st.isin(inc["announced_stages"]) & win
    ann_in = ann & lk.isin(inc["announced_likelihood"])
    if rules_["exclude"].get("low_likelihood_without_tenant"):
        low_nt = (lk == "Low").groupby(a["key"]).transform("any") & ~a["user"].groupby(a["key"]).transform("any")
    else:
        low_nt = pd.Series(False, index=a.index)
    return {"win": win, "act": act, "bld": bld, "ann": ann, "ann_in": ann_in, "low_nt": low_nt,
            "keep": (act | bld | ann_in) & ~low_nt, "raw": act | bld | ann}


def rules_line(r: dict, k: float) -> str:
    """One sentence stating the house rules, for page sections and dashboards (same wording everywhere)."""
    inc = r["include"]
    hi = " / ".join(inc["announced_likelihood"])
    return (f"facility MW ÷ {k:g} (Aterio's own facility/IT median); counts what switched on since Jan-{r['window'][0]}, "
            f"under construction, delayed and planned rated {hi}, dated {r['window'][0]}-{str(r['window'][1])[2:]} by Aterio; "
            f"drops campuses rated Low with no named end user (house rules of {r.get('decided', '')})")
