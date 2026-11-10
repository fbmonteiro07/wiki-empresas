"""Hyperscaler view of the Aterio data-center census (Amazon, Google, Meta, Microsoft)
-> _wiki/_dashboards/aterio-hyperscalers.html (+ _wiki/_data/aterio/hyperscalers.json)

Where each of the four builds (campus map, states), how much (GW IT-eq), at what stage and Aterio likelihood, and the
house view under the rules in _data/aterio/treatment.json (decided by Felipe 2026-11-09).

Attribution (per building, newest US export):
  self-built  PROVIDER_TICKER_NAME is the company's ticker (Aterio's provider = owner/operator)
  leased      END_USER_COMPANIES names the company and the provider is someone else (colo / developer / neocloud);
              a building with several named tenants counts in full for each of them ('shared' flag)
Basis: facility MW (SELECTED_POWER_CAPACITY_MW) ÷ Aterio's own facility/IT median (house rule 1). Stages: operating =
Active (any date), building = Construction, delayed = Delayed, announced = Announcement + Land Bank split by likelihood.
House view = rules 2-4 over the activation window; a hyperscaler self-build counts as having a named tenant (itself)
for rule 4. Bernstein's 2026-11-06 player table (Aterio data via Bernstein) is carried as the cross-check.

Company lookup (search bar at the top of the page): every company Aterio names in any role (operator, end user,
backer, financier, power/equipment partner, utility, behind-the-meter generation) -> _data/aterio/company_lookup.json.
The wiki companies use the same matching as the page sections (build_aterio_company.SPEC).

usage: py build_aterio_hyperscalers.py [--src <Aterio folder>]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                       # _wiki
DASH = os.path.join(ROOT, "_dashboards", "aterio-hyperscalers.html")
TPL = os.path.join(HERE, "aterio_mags_ui", "template.html")
OUTJ = os.path.join(ROOT, "_data", "aterio", "hyperscalers.json")
OUTL = os.path.join(ROOT, "_data", "aterio", "company_lookup.json")   # every named company, for the page's search
FONT = os.path.join(ROOT, "_data", "openrouter", "assets", "plus-jakarta-sans.woff2")  # the dashboards hub face
CO = [{"id": "amzn", "name": "Amazon", "tick": ["AMZN"], "rx": r"\bamazon\b|\baws\b", "bern": "Amazon AWS"},
      {"id": "goog", "name": "Google", "tick": ["GOOG", "GOOGL"], "rx": r"google|alphabet", "bern": "Google"},
      {"id": "meta", "name": "Meta", "tick": ["META"], "rx": r"facebook|\bmeta\b", "bern": "Facebook"},
      {"id": "msft", "name": "Microsoft", "tick": ["MSFT"], "rx": r"microsoft|azure", "bern": "Microsoft"}]
GRPS = ["op", "uc", "dl", "aH", "aM", "aL"]          # operating, building, delayed, announced High / Medium / Low


def build(src: str | None = None) -> dict:
    import numpy as np
    import pandas as pd
    sys.path.insert(0, HERE)
    import aterio_core as core
    import build_dc_delay as bdd
    rules = core.rules()
    inv, asof = core.find_inventory(src)
    # shared loader (aterio_core): every field, US, index 0..n-1; self_tenant = a hyperscaler self-build names its own
    # tenant for rule 4 (core.SELF_TENANT_TICKERS, the four companies of this page)
    a = core.load(inv, cols=None, self_tenant=True)
    tick = a["PROVIDER_TICKER_NAME"].fillna("").astype(str)
    users = a["END_USER_COMPANIES"].fillna("").astype(str).str.strip()
    k = core.ratio(a, rules)["k"]                             # rule 1, measured on this export
    m = core.masks(a, rules)
    y0, y1 = rules["window"]
    st = a["DATA_CENTER_STAGE"]
    ann = st.isin(["Announcement", "Land Bank"])
    a["g"] = np.select([st.eq("Active"), st.eq("Construction"), st.eq("Delayed"), ann & a["like"].eq("High"), ann & a["like"].eq("Medium"),
                        ann & a["like"].eq("Low"), ann], ["op", "uc", "dl", "aH", "aM", "aL", "aM"], "drop")
    a["house"] = m["keep"]
    a["win"] = m["raw"]
    a["n_ten"] = users.apply(lambda s: len([u for u in s.split(",") if u.strip()]))
    proj = bdd.albers_lower48()
    IT = lambda s: round(float(s.sum()) / 1000 / k, 3)
    out = {"asof": asof, "inventory": os.path.basename(inv), "fac_it": k, "window": [y0, y1], "rules_decided": rules.get("decided"),
           "built": __import__("datetime").date.today().isoformat(), "companies": [], "us": {}}
    out["us"] = {"house": IT(a.loc[a["house"], "mw"]), "op": IT(a.loc[st.eq("Active"), "mw"])}
    for c in CO:
        self_ = tick.isin(c["tick"])
        ten = users.str.contains(c["rx"], case=False, regex=True) & ~self_
        d = a[self_ | ten].copy()
        d["role"] = np.where(self_.loc[d.index], "self", "leased")
        tot = {r: {g: IT(d.loc[(d["role"] == r) & (d["g"] == g), "mw"]) for g in GRPS + ["drop"]} for r in ("self", "leased")}
        house_by = {str(y): {r: {g: IT(d.loc[d["house"] & (d["role"] == r) & (d["yr"] == y) & (d["g"] == g), "mw"]) for g in ("op", "uc", "dl", "aH")}
                             for r in ("self", "leased")} for y in range(y0, y1 + 1)}
        raw_by = {str(y): IT(d.loc[d["win"] & (d["yr"] == y), "mw"]) for y in range(y0, y1 + 1)}
        pipe = d["g"].isin(["uc", "dl", "aH", "aM", "aL"])
        states = []
        for s, x in d.groupby("STATE_CODE"):
            states.append({"st": s, **{g: IT(x.loc[x["g"] == g, "mw"]) for g in GRPS}, "house": IT(x.loc[x["house"], "mw"]),
                           "leased": IT(x.loc[(x["role"] == "leased") & (x["g"] != "drop"), "mw"])})
        states.sort(key=lambda r: -(r["op"] + r["uc"] + r["dl"] + r["aH"] + r["aM"] + r["aL"]))
        camps = []
        for (key, role), x in d[d["g"] != "drop"].groupby(["key", "role"]):
            lat, lon = x["LOCATION_LATITUDE"].mean(), x["LOCATION_LONGITUDE"].mean()
            px = py = None
            if x["STATE_CODE"].iloc[0] not in ("AK", "HI", "PR") and pd.notna(lat) and pd.notna(lon):
                px, py = proj(float(lon), float(lat))
            hy = x.loc[x["house"], "yr"].dropna()
            ay = x.loc[pipe.loc[x.index], "yr"].dropna()
            first = lambda col: next((str(v) for v in x[col] if isinstance(v, str) and v.strip()), "")
            camps.append({"name": str(x["campus"].iloc[0]), "st": str(x["STATE_CODE"].iloc[0]), "city": first("CITY_NAME"), "county": first("COUNTY_NAME"),
                          "role": role, "prov": first("PROVIDER_NAME"),
                          "users": ", ".join(sorted({u.strip() for s_ in x["END_USER_COMPANIES"].dropna() for u in str(s_).split(",") if u.strip()})),
                          "shared": bool((x["n_ten"] > 1).any()),
                          "x": None if px is None else round(px, 1), "y": None if py is None else round(py, 1),
                          **{g: IT(x.loc[x["g"] == g, "mw"]) for g in GRPS},
                          "house": IT(x.loc[x["house"], "mw"]), "win": IT(x.loc[x["win"], "mw"]),
                          "after": IT(x.loc[pipe.loc[x.index] & (x["yr"] > y1), "mw"]),
                          "hy": [int(hy.min()), int(hy.max())] if len(hy) else None, "py": [int(ay.min()), int(ay.max())] if len(ay) else None,
                          "like": "/".join(sorted({v for v in x["like"] if v}, key=lambda v: -core.RANK.get(v, 0))),
                          "ai": bool((x["FLG_AI_FACILITY"] == "Y").any()), "btm": bool((x["FLG_BTM_ONSITE_POWER_GENERATION"] == "Y").any()),
                          "n": int(len(x)), "nomw": int(x["mw_raw"].isna().sum())})
        camps.sort(key=lambda r: -(r["op"] + r["uc"] + r["dl"] + r["aH"] + r["aM"] + r["aL"]))
        out["companies"].append({
            "id": c["id"], "name": c["name"], "tick": c["tick"][0], "bern": c["bern"], "tot": tot,
            "house": IT(d.loc[d["house"], "mw"]), "house_self": IT(d.loc[d["house"] & (d["role"] == "self"), "mw"]),
            "house_leased": IT(d.loc[d["house"] & (d["role"] == "leased"), "mw"]),
            "win": IT(d.loc[d["win"], "mw"]), "after": IT(d.loc[pipe & (d["yr"] > y1), "mw"]), "undated": IT(d.loc[pipe & d["yr"].isna(), "mw"]),
            "fac": {"op": round(float(d.loc[d["g"] == "op", "mw"].sum()) / 1000, 2), "uc": round(float(d.loc[d["g"] == "uc", "mw"].sum()) / 1000, 2),
                    "dl": round(float(d.loc[d["g"] == "dl", "mw"].sum()) / 1000, 2),
                    "op_self": round(float(d.loc[(d["g"] == "op") & (d["role"] == "self"), "mw"].sum()) / 1000, 2),
                    "uc_self": round(float(d.loc[(d["g"] == "uc") & (d["role"] == "self"), "mw"].sum()) / 1000, 2),
                    # Bernstein cross-check variants (self + leased): construction + Delayed, then the whole campus — every
                    # announced building on a campus where at least one building is under construction counts as building
                    "uc_campus": round(float(d.loc[d["g"].isin(["uc", "dl"]) | (d["g"].isin(["aH", "aM", "aL"])
                                                   & d["key"].isin(set(d.loc[d["g"] == "uc", "key"]))), "mw"].sum()) / 1000, 2)},
            "house_by": house_by, "raw_by": raw_by, "states": states, "campuses": camps,
            "n_campuses": len({cc["name"] + cc["st"] for cc in camps}), "n_bld": int((d["g"] != "drop").sum()),
            "nomw": int((d["mw_raw"].isna() & (d["g"] != "drop")).sum()),
            "shared_it": IT(d.loc[(d["n_ten"] > 1) & (d["g"] != "drop"), "mw"]),
        })
    # Bernstein 2026-11-06 player table (Aterio data via Bernstein) as the cross-check
    bfs = sorted(glob.glob(os.path.join(ROOT, "_data", "dc_projects", "broker", "bernstein_*.json")))
    if bfs:
        b = json.load(open(bfs[-1], encoding="utf-8"))
        rows = {r["player"]: r for grp in b.get("national", {}).get("groups", []) for r in grp.get("rows", [])}
        out["bernstein"] = {"source": b.get("source", {}), "note": b.get("national", {}).get("_note", ""),
                            "rows": {c["id"]: rows.get(c["bern"]) for c in CO}}
    out["lookup"] = lookup(a, inv, proj)
    return out


# ----------------------------------------------------------------------------- company lookup
# Every company the census names, in any role, so the page can answer "show me everything on X".
# Raw names come straight from Aterio's fields; the wiki companies are composites that use the SAME matching as
# the wiki page sections (build_aterio_company.SPEC), so the lookup and the pages agree.
NAMES = {"AMZN": "Amazon", "MSFT": "Microsoft", "GOOG": "Alphabet (Google)", "META": "Meta (Facebook)", "ORCL": "Oracle",
         "AAPL": "Apple", "OPENAI": "OpenAI", "ANTHROPIC": "Anthropic", "SPCX": "SpaceX / xAI", "CRWV": "CoreWeave",
         "NBIS": "Nebius", "NSCALE": "Nscale", "IREN": "IREN", "CEREBRAS": "Cerebras", "TSLA": "Tesla", "NVDA": "NVIDIA",
         "AMD": "AMD", "JPM": "JPMorgan", "GS": "Goldman Sachs", "BX": "Blackstone", "KKR": "KKR",
         "BLK": "BlackRock (incl. GIP)", "OWL": "Blue Owl", "APO": "Apollo", "GEV": "GE Vernova", "BE": "Bloom Energy",
         "TLN": "Talen", "VST": "Vistra (Luminant)", "CEG": "Constellation", "WMB": "Williams", "ETN": "Eaton",
         "PWR": "Quanta", "VRT": "Vertiv"}
ALIAS = {"AMZN": "AWS Amazon Web Services", "GOOG": "Google GOOGL", "META": "Facebook", "SPCX": "xAI X.AI SpaceX",
         "BLK": "Global Infrastructure Partners GIP", "VST": "Luminant", "MSFT": "Azure"}
GROUP_NAMES = {"AEP": "American Electric Power", "D": "Dominion Energy", "DUK": "Duke Energy", "ES": "Eversource", "ETR": "Entergy",
               "EXC": "Exelon", "FE": "FirstEnergy", "FTS": "Fortis", "PPL": "PPL", "WEC": "WEC Energy", "XEL": "Xcel Energy",
               "SO": "Southern Company", "NEE": "NextEra Energy", "AEE": "Ameren", "CNP": "CenterPoint", "PCG": "PG&E",
               "EIX": "Edison International", "SRE": "Sempra", "CMS": "CMS Energy", "DTE": "DTE Energy", "EVRG": "Evergy",
               "LNT": "Alliant Energy", "PNW": "Pinnacle West", "OGE": "OGE Energy", "NI": "NiSource", "PEG": "PSEG"}
SUFFIX = re.compile(r"^(llc|l\.l\.c\.?|inc\.?|incorporated|corp\.?|corporation|co\.?|ltd\.?|limited|l\.?p\.?|plc|n\.a\.?|s\.a\.?|gmbh|ag|lllp|pllc)$", re.I)
LIST_F = {"ten": "END_USER_COMPANIES", "bk": "PROVIDER_BACKED_BY", "fin": "PROJECT_FINANCING_COMPANIES",
          "pt": "CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES"}
BTM_F = {"dev": "DEVELOPER_COMPANIES", "eq": "CONSTRUCTION_EQUIPMENT_PROVIDER_COMPANIES", "fin": "PROJECT_FINANCING_COMPANIES",
         "cust": "CUSTOMER_COMPANIES"}
GI = {"op": 0, "uc": 1, "dl": 2, "aH": 3, "aM": 4, "aL": 5, "drop": 6}
BTM_STAGES = ["Active", "Construction", "Site Preparation", "Delayed", "Announcement", "Not Approved/Withdrawn", "Cancelled"]


def _names(v) -> list[str]:
    """Aterio list field -> names; re-attaches split-off suffixes ('Foo, LLC')."""
    from build_aterio_dashboard import split_list
    out: list[str] = []
    for p in split_list(v):
        if out and SUFFIX.match(p):
            out[-1] = f"{out[-1]}, {p}"
        else:
            out.append(p)
    return out


def _nkey(s: str) -> str:
    k = re.sub(r"[\s,.]+", " ", str(s).lower()).strip()
    while True:
        k2 = re.sub(r"\s(llc|inc|incorporated|corp|corporation|co|ltd|limited|lp|l p|plc)$", "", k)
        if k2 == k:
            return k
        k = k2


def _ym(v) -> int:
    import pandas as pd
    d = pd.to_datetime(v, errors="coerce")
    return 0 if pd.isna(d) else d.year * 100 + d.month


def lookup(a, inv: str, proj) -> dict:
    import pandas as pd
    from collections import Counter, defaultdict
    import aterio_core as core
    from build_aterio_company import SPEC, any_match
    clean =lambda v: "" if v is None or (isinstance(v, float) and v != v) else str(v).strip()
    ents, eidx, forms = [], {}, defaultdict(Counter)

    def eid(name: str, tick: str = "") -> int | None:
        name = clean(name)
        k = _nkey(name)
        if not k:
            return None
        if k not in eidx:
            eidx[k] = len(ents)
            ents.append({"t": set()})
        i = eidx[k]
        forms[i][name] += 1
        if tick:
            ents[i]["t"].add(tick)
        return i

    # campuses (same key as the rest of the page) + the registry campus each one maps to
    reg_by = defaultdict(set)
    xp = os.path.join(ROOT, "_data", "dc_projects", "aterio", "xchk.json")
    if os.path.exists(xp):
        for g in json.load(open(xp, encoding="utf-8")).get("groups", []):
            for k_ in g["at"]["keys"]:
                reg_by[k_] |= set(g["reg"]["campuses"])
    cost = pd.to_numeric(a["TOT_PROJECT_COST"], errors="coerce")
    camps, cix = [], {}
    for key, x in a.groupby("key", sort=False):
        first = lambda col: next((clean(v) for v in x[col] if clean(v)), "")
        lat, lon, st = x["LOCATION_LATITUDE"].mean(), x["LOCATION_LONGITUDE"].mean(), first("STATE_CODE")
        px = py = None
        if st not in ("AK", "HI", "PR") and pd.notna(lat) and pd.notna(lon):
            px, py = proj(float(lon), float(lat))
        cv = cost.loc[x.index].max()
        cix[key] = len(camps)
        camps.append([clean(x["campus"].iloc[0]), st, first("CITY_NAME"), first("COUNTY_NAME"),
                      None if px is None else round(px, 1), None if py is None else round(py, 1),
                      "; ".join(sorted(reg_by.get(key, ()))), None if pd.isna(cv) else round(float(cv) / 1e9, 2)])
    LK = {"High": 1, "Medium": 2, "Low": 3}
    bld = []
    for r in a.to_dict("records"):
        fl = (1 if r["house"] else 0) | (2 if r["win"] else 0) | (4 if r.get("FLG_AI_FACILITY") == "Y" else 0) \
            | (8 if r.get("FLG_BTM_ONSITE_POWER_GENERATION") == "Y" else 0) | (16 if clean(r.get("ESTIMATED_ACTIVATION_DATE_PUBLIC_SOURCE")) else 0)
        lists = [[i for i in (eid(n) for n in _names(r[LIST_F[f]])) if i is not None] for f in ("ten", "bk", "fin", "pt")]
        bld.append([cix[r["key"]], GI[r["g"]], None if r["mw_raw"] != r["mw_raw"] else round(float(r["mw_raw"]), 1),
                    _ym(r["DATA_CENTER_ACTIVATION_DATE"]), LK.get(r["like"], 0), fl,
                    eid(r["PROVIDER_NAME"], clean(r["PROVIDER_TICKER_NAME"]).upper()), *lists,
                    eid(r["UTILITY_NAME"], clean(r["UTILITY_TICKER_NAME"]).upper())])
    # behind-the-meter generation (nameplate MW: a different basis, never added to data-center MW)
    bp, _ = core.find_btm(core.src_of(inv))                   # same Aterio folder as the inventory being read
    b = pd.read_csv(bp, low_memory=False)
    b = b[b["FLG_BTM_PROJECT"] == "Y"].reset_index(drop=True)
    btm = []
    for r in b.to_dict("records"):
        devs, dt = _names(r["DEVELOPER_COMPANIES"]), _names(r["DEVELOPER_COMPANIES_TICKER"])
        lat, lon = r["LOCATION_LATITUDE"], r["LOCATION_LONGITUDE"]
        px = py = None
        if clean(r["STATE_CODE"]) not in ("AK", "HI", "PR") and pd.notna(lat) and pd.notna(lon):
            try:
                px, py = proj(float(lon), float(lat))
            except Exception:
                px = py = None
        mw = pd.to_numeric(r["TOT_PHASE_NAMEPLATE_POWER_MW"], errors="coerce")
        btm.append([clean(r["PROJECT_NAME"]), clean(r["PHASE_NAME"]), clean(r["STATE_CODE"]), clean(r["CITY_NAME"]),
                    BTM_STAGES.index(r["PHASE_STAGE"]) if r["PHASE_STAGE"] in BTM_STAGES else 4,
                    None if pd.isna(mw) else round(float(mw), 1), clean(r["ATERIO_PLANT_TECHNOLOGY_TYPE"]),
                    clean(r["ATERIO_PLANT_ENERGY_SOURCE"]), _ym(r["PHASE_SELECTED_ACTIVATION_DATE"]),
                    [i for i in (eid(n, (dt[j].upper() if len(dt) == len(devs) else "")) for j, n in enumerate(devs)) if i is not None],
                    *[[i for i in (eid(n) for n in _names(r[BTM_F[f]])) if i is not None] for f in ("eq", "fin", "cust")]])
    wiki = {os.path.splitext(f)[0] for f in os.listdir(ROOT) if f.endswith(".md") and f[0] != "_" and f[0].isupper()}
    th = {}
    im = os.path.join(ROOT, "_data", "index_meta.json")
    if os.path.exists(im):
        for s in json.load(open(im, encoding="utf-8")).get("sections", []):
            for e in s.get("entries", []):
                th.setdefault(e.get("ticker"), e.get("thesis", ""))
    raw = []
    for i, e in enumerate(ents):
        t = sorted(x for x in e["t"] if x and x.lower() != "nan")
        w = next((x for x in [{"GOOGL": "GOOG"}.get(x, x) for x in t] if x in wiki), "")
        raw.append([forms[i].most_common(1)[0][0], "/".join(t), w])
    # composites: the wiki companies (SPEC, same as the page sections), then tickers carried under several names
    tick = a["PROVIDER_TICKER_NAME"].fillna("").astype(str).str.upper()
    utick = a["UTILITY_TICKER_NAME"].fillna("").astype(str).str.upper()
    pos = lambda m: [int(i) for i in m[m].index]
    cos = []
    for t, s in SPEC.items():
        op = pd.Series(False, index=a.index)
        if s.get("op_tick"):
            op |= tick.isin([s["op_tick"], {"GOOG": "GOOGL"}.get(s["op_tick"], s["op_tick"])])
        if s.get("op_name"):
            op |= a["PROVIDER_NAME"].fillna("").str.contains(s["op_name"], case=False, regex=True)
        r = {"op": pos(op)}
        if s.get("tenant"):
            r["ten"] = pos(a["END_USER_COMPANIES"].map(lambda v: any_match(v, s["tenant"])) & ~op)
        for k_, f in (("backer", "bk"), ("fin", "fin"), ("partner", "pt")):
            if s.get(k_):
                r[f] = pos(a[LIST_F[f]].map(lambda v, rx=s[k_]: any_match(v, rx)))
        if s.get("util_tick"):
            r["ut"] = pos(utick == s["util_tick"])
        bb = {}
        for k_, f in (("btm_dev", "dev"), ("btm_eq", "eq"), ("btm_cust", "cust")):
            if s.get(k_):
                bb[f] = pos(b[BTM_F[f]].map(lambda v, rx=s[k_]: any_match(v, rx)))
        r = {k_: v for k_, v in r.items() if v}
        bb = {k_: v for k_, v in bb.items() if v}
        if not r and not bb:
            continue
        # the raw names this composite stands for (left out of its own counterparties)
        own = set()
        for j in r.get("op", []):
            if bld[j][6] is not None:
                own.add(bld[j][6])
        for f, rx in (("ten", s.get("tenant")), ("bk", s.get("backer")), ("fin", s.get("fin")), ("pt", s.get("partner"))):
            if rx:
                own |= {i for i, rw in enumerate(raw) if re.search(rx, rw[0], re.I)}
        cos.append({"n": NAMES.get(t, t), "t": t, "w": t if t in wiki else "", "al": ALIAS.get(t, ""),
                    "r": r, "b": bb, "own": sorted(own)})
    spec_t = set(SPEC) | {"GOOGL"}
    for col, role, ser in (("PROVIDER_NAME", "op", tick), ("UTILITY_NAME", "ut", utick)):
        for t, x in a[ser.ne("") & ~ser.isin(spec_t) & ser.ne("NAN")].groupby(ser):
            nm = sorted({clean(v) for v in x[col] if clean(v)})
            if len(nm) < 2:
                continue
            own = sorted({eidx[_nkey(n)] for n in nm if _nkey(n) in eidx})
            cos.append({"n": f"{GROUP_NAMES.get(t, t)} ({t}) — all {len(nm)} {'utilities' if role == 'ut' else 'provider names'}", "t": t,
                        "w": t if t in wiki else "", "al": " ".join(nm), "r": {role: [int(i) for i in x.index]}, "b": {}, "own": own})
    return {"camps": camps, "bld": bld, "btm": btm, "ents": raw, "cos": cos, "btmStages": BTM_STAGES, "btmFile": os.path.basename(bp),
            "th": {t: th[t] for t in {c["w"] for c in cos} | {r_[2] for r_ in raw} if t and th.get(t)}}


def write(out: dict) -> None:
    sys.path.insert(0, HERE)
    import build_dc_delay as bdd
    os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
    with open(OUTJ, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in out.items() if k != "lookup"}, fh, ensure_ascii=False, indent=1)
    with open(OUTL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out.get("lookup"), fh, ensure_ascii=False, separators=(",", ":"))
    tpl = open(TPL, encoding="utf-8").read()
    payload = json.dumps({**out, "map": bdd.state_paths(), "stateNames": bdd.STATE_NAMES}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    with open(DASH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(tpl.replace("/*__FONT__*/", font_face()).replace("/*__DATA__*/null", payload))


def font_face() -> str:
    """The hub's Plus Jakarta Sans face, inlined so the page matches the dashboards hub shell."""
    if not os.path.exists(FONT):
        return ""
    import base64
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    return ('@font-face{font-family:"OR Jakarta";font-weight:200 800;font-style:normal;font-display:swap;'
            f'src:url(data:font/woff2;base64,{b64}) format("woff2")}}')


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--render-only", action="store_true", help="re-render the page from the JSON already on disk (template change, no Aterio recompute)")
    args = ap.parse_args()
    if args.render_only:
        o = json.load(open(OUTJ, encoding="utf-8"))
        o["lookup"] = json.load(open(OUTL, encoding="utf-8"))
        write(o)
        print("re-rendered", DASH, "from", os.path.basename(OUTJ), "+", os.path.basename(OUTL))
        sys.exit(0)
    o = build(args.src)
    write(o)
    print(f"Aterio {o['asof']} · fac/IT {o['fac_it']} · US house view {o['us']['house']:.1f} GW IT-eq, operating {o['us']['op']:.1f}")
    for c in o["companies"]:
        t = c["tot"]
        print(f"  {c['name']:9s} operating {t['self']['op'] + t['leased']['op']:5.1f} (self {t['self']['op']:.1f}) · building {t['self']['uc'] + t['leased']['uc']:5.1f} · delayed {t['self']['dl'] + t['leased']['dl']:4.1f}"
              f" · announced H/M/L {t['self']['aH'] + t['leased']['aH']:.1f}/{t['self']['aM'] + t['leased']['aM']:.1f}/{t['self']['aL'] + t['leased']['aL']:.1f}"
              f" · house {c['house']:.1f} (self {c['house_self']:.1f}, leased {c['house_leased']:.1f}) · campuses {c['n_campuses']} · states {len(c['states'])}")
    print("wrote", DASH)
