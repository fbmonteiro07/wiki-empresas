"""Cross-check the DC delay registry (projects.csv / model_output.json) against the Aterio census.

Reads   _wiki/_data/dc_projects/model_output.json       registry phases as the engine sees them (IT-eq, universe, buckets)
        _wiki/_data/dc_projects/projects.csv            lat/lon per phase
        _wiki/_data/dc_projects/aterio/registry_map.json hand-reviewed matches: "ST|campus" -> {"aterio": [campus keys], "note"}
        P:/Felipe Monteiro/Aterio/.../data_center_inventory_<date>.csv   (newest; --src overrides the folder)
Writes  _wiki/_data/dc_projects/aterio/xchk.json        matched groups + flags, registry-only, Aterio-only, state coverage
        _wiki/_data/dc_projects/aterio/xchk_review.md   the same as a reviewable list

Matching: a registry campus maps to one or more Aterio campuses (key = ATERIO_DATA_CENTER_CAMPUS_UID, else the building
UID). The map file wins; campuses not in it are auto-matched (same state, ≤30 km, name/developer score ≥ AUTO_MIN) and
listed as 'auto' so a reviewer can confirm them into the map. Registry and Aterio campuses that share a match form one
group (union-find), and every comparison is made per group.

Bases: registry MW are the engine's IT-eq (facility/grid/unknown ÷1.2, gen ÷1.5). Aterio MW are facility power ÷ the
census's own facility/IT median (1.15). Window = activation 2026-01..2030-12, the registry's scope. Aterio withdrawn and
cancelled buildings are reported separately and never counted as capacity.

Run:  py _wiki/_tools/aterio_registry_xchk.py [--src <Aterio folder>] [--suggest]
      build_dc_delay.py calls run() on every build and embeds the result as the page's Aterio tab.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DATA = os.path.join(WIKI, "_data", "dc_projects")
OUT_DIR = os.path.join(DATA, "aterio")
MAP_FILE = os.path.join(OUT_DIR, "registry_map.json")
sys.path.insert(0, HERE)
import aterio_core as core  # noqa: E402  (shared Aterio loader: source folder, inventory read, ratio, stage groups)

SRC_CANDIDATES = core.SRC_CANDIDATES
FAC_IT = None            # facility/IT ratio (house rule 1). Never hardcoded: run() measures it on the export through
                         # aterio_core (statistic named in _data/aterio/treatment.json); shown on the page
AUTO_MIN = 2.5           # auto-accept score
SUGGEST_MIN = 1.2        # below this nothing is suggested
WIN = ("2026-01", "2030-12")
DATE_FLAG_M = 9          # months between earliest dates before a date flag
SIZE_BAND = (0.5, 2.0)   # Aterio/registry IT-eq ratio outside this band -> size flag

GROUP = core.GROUP
STOP =set(("data center centre centers datacenter datacenters campus campuses llc inc the ai dc phase building bldg "
            "project of and at a park site facility facilities hyperscale digital technology technologies infrastructure "
            "group corp corporation co company dr rd road hwy st ave county city north south east west new self build "
            "expansion parkway pkwy blvd ii iii iv tech partners holdings properties development developer").split())
ALIAS = {"facebook": "meta", "amazon": "aws", "hut8": "hut", "powerhouse": "powerhouse", "clear": "cleanarc",
         "cleanarc": "cleanarc", "databank": "databank", "edgeconnex": "edgeconnex", "corescale": "corscale",
         "iren": "iren", "streamdatacenters": "stream", "xai": "xai", "spacex": "xai"}


def toks(*xs) -> set[str]:
    out = set()
    for x in xs:
        if not isinstance(x, str):
            continue
        s = x.lower().replace("power house", "powerhouse").replace("data bank", "databank").replace("hut 8", "hut8") \
            .replace("clean arc", "cleanarc").replace("clear arc", "cleanarc")
        for t in re.findall(r"[a-z0-9]+", s):
            if len(t) >= 3 and t not in STOP and not t.isdigit():
                out.add(ALIAS.get(t, t))
    return out


def hav(la1, lo1, la2, lo2) -> float:
    if None in (la1, lo1, la2, lo2) or any(isinstance(v, float) and math.isnan(v) for v in (la1, lo1, la2, lo2)):
        return 999.0
    p = math.pi / 180
    h = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def months(a: str, b: str) -> int | None:
    if not a or not b:
        return None
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:7]) - int(a[5:7])


find_inventory = core.find_inventory     # kept importable from here (older callers)


# ----------------------------------------------------------------------------- loaders
def aterio_campuses(inv_path: str) -> tuple[dict, dict, float]:
    """Aterio campuses + their buildings from the shared loader, and the facility/IT ratio measured on the export."""
    a = core.load(inv_path, cols=None)       # US rows, every field; key / act / grp / like come from the loader
    a["MW"] = a["mw"]
    camps, blds = {}, defaultdict(list)
    first = lambda s: next((str(v) for v in s if isinstance(v, str) and v.strip()), "")
    for k, d in a.groupby("key"):
        name = first(d["DATA_CENTER_CAMPUS_NAME"]) or first(d["DATA_CENTER_BUILDING_NAME"])
        camps[k] = {"key": k, "st": d["STATE_CODE"].iloc[0], "name": name, "prov": first(d["PROVIDER_NAME"]),
                    "users": "; ".join(sorted({u for v in d["END_USER_COMPANIES"].dropna() for u in re.split(r",\s*", v)})),
                    "county": first(d["COUNTY_NAME"]), "city": first(d["CITY_NAME"]),
                    "lat": float(d["LOCATION_LATITUDE"].mean()), "lon": float(d["LOCATION_LONGITUDE"].mean()),
                    "n": int(len(d)), "mw": round(float(d["MW"].sum()), 1),
                    "tok": toks(name, " ".join(d["DATA_CENTER_BUILDING_NAME"].head(3).astype(str)), first(d["PROVIDER_NAME"])),
                    "ptok": toks(first(d["PROVIDER_NAME"]), first(d["PROVIDER_BACKED_BY"]))}
        for r in d.itertuples():
            blds[k].append({"g": r.grp, "mw": float(r.MW), "act": r.act, "like": r.like,
                            "name": str(r.DATA_CENTER_BUILDING_NAME), "stage": r.DATA_CENTER_STAGE})
    return camps, blds, core.ratio(a)["k"]


def registry_campuses() -> dict:
    import csv
    m = json.load(open(os.path.join(DATA, "model_output.json"), encoding="utf-8"))
    ll = {}
    with open(os.path.join(DATA, "projects.csv"), encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                ll[r["project_id"]] = (float(r["lat"]), float(r["lon"]))
            except (TypeError, ValueError):
                pass
    camps = {}
    for p in m["phases"]:
        k = f"{p['st']}|{p['campus']}"
        c = camps.setdefault(k, {"key": k, "st": p["st"], "campus": p["campus"], "dev": p.get("dev", ""), "ten": p.get("ten", ""),
                                 "county": p.get("county", ""), "city": p.get("city", ""), "pts": [], "phases": []})
        if p["id"] in ll:
            c["pts"].append(ll[p["id"]])
        c["phases"].append({"id": p["id"], "it": float(p.get("it") or 0), "ps": p.get("ps", ""), "cod": (p.get("cod") or "")[:7],
                            "u": p.get("u", ""), "lk": p.get("lk", ""), "bear": (p.get("res", {}).get("bear") or {}).get("b", "")})
    for c in camps.values():
        c["lat"] = sum(x for x, _ in c["pts"]) / len(c["pts"]) if c["pts"] else None
        c["lon"] = sum(y for _, y in c["pts"]) / len(c["pts"]) if c["pts"] else None
        c["tok"] = toks(c["campus"], c["dev"])
        c["dtok"] = toks(c["dev"], c["ten"])
    return camps


# ----------------------------------------------------------------------------- matching
def candidates(rc: dict, acs: list[dict], top: int = 4) -> list[tuple]:
    out = []
    for x in acs:
        d = hav(rc["lat"], rc["lon"], x["lat"], x["lon"])
        if d > 60:
            continue
        j = len(rc["tok"] & x["tok"]) / max(1, len(rc["tok"] | x["tok"]))
        dev = 1.0 if rc["dtok"] & x["ptok"] else 0.0
        cty = 0.5 if rc["county"] and x["county"] and rc["county"].lower().split()[0] in x["county"].lower() else 0.0
        s = 2 * j + dev + cty + max(0.0, 1 - d / 25)
        out.append((round(s, 2), round(d, 1), x["key"]))
    out.sort(reverse=True)
    return out[:top]


def match(reg: dict, ac: dict, mp: dict) -> tuple[dict, list]:
    by_st = defaultdict(list)
    for x in ac.values():
        by_st[x["st"]].append(x)
    res, suggest = {}, []
    for k, rc in reg.items():
        e = mp.get(k)
        cands = candidates(rc, by_st[rc["st"]])
        if e is not None:
            keys = [a for a in e.get("aterio", []) if a in ac]
            res[k] = {"keys": keys, "how": "reviewed", "note": e.get("note", ""),
                      "stale": [a for a in e.get("aterio", []) if a not in ac]}
            continue
        if cands and cands[0][0] >= AUTO_MIN and cands[0][1] <= 30:
            res[k] = {"keys": [cands[0][2]], "how": "auto", "note": f"score {cands[0][0]}, {cands[0][1]} km"}
        else:
            res[k] = {"keys": [], "how": "unmatched", "note": ""}
            if cands and cands[0][0] >= SUGGEST_MIN:
                suggest.append((k, cands))
    return res, suggest


def groups(res: dict) -> list[tuple[set, set]]:
    parent = {}

    def f(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for k, r in res.items():
        f(("r", k))
        for a in r["keys"]:
            parent[f(("a", a))] = f(("r", k))
    comp = defaultdict(lambda: (set(), set()))
    for x in list(parent):
        root = f(x)
        (comp[root][0] if x[0] == "r" else comp[root][1]).add(x[1])
    return [v for v in comp.values() if v[1]]


# ----------------------------------------------------------------------------- comparison
def in_win(act: str) -> bool:
    return bool(act) and WIN[0] <= act <= WIN[1]


def aterio_side(keys: set, ac: dict, blds: dict) -> dict:
    b = [x for k in keys for x in blds[k]]
    cap = [x for x in b if x["g"] != "wd"]
    win = [x for x in cap if in_win(x["act"]) or (x["g"] in ("uc", "delayed", "ann") and not x["act"])]
    it = lambda xs: round(sum(x["mw"] for x in xs) / FAC_IT, 1)
    acts = sorted(x["act"] for x in win if x["g"] in ("uc", "delayed") and x["act"])
    acts_all = sorted(x["act"] for x in win if x["act"] and x["g"] != "active")
    cnt = {g: sum(1 for x in b if x["g"] == g) for g in ("active", "uc", "delayed", "ann", "wd")}
    return {"keys": sorted(keys), "names": sorted({ac[k]["name"] for k in keys}), "prov": sorted({ac[k]["prov"] for k in keys}),
            "cnt": cnt, "no_mw": sum(1 for x in b if x["mw"] <= 0),
            "users": "; ".join(sorted({ac[k]["users"] for k in keys if ac[k]["users"]})),
            "n": len(b), "fac_all": round(sum(x["mw"] for x in b), 1),
            "it_win": it(win), "it_uc": it([x for x in win if x["g"] == "uc"]), "it_delayed": it([x for x in win if x["g"] == "delayed"]),
            "it_ann": it([x for x in win if x["g"] == "ann"]), "it_active": it([x for x in win if x["g"] == "active"]),
            "it_ann_low": it([x for x in win if x["g"] == "ann" and x["like"] == "Low"]),
            "it_wd": it([x for x in b if x["g"] == "wd"]), "n_wd": sum(1 for x in b if x["g"] == "wd"),
            "it_late": it([x for x in cap if x["act"] > WIN[1]]),
            "uc_first": acts[0] if acts else "", "uc_last": acts[-1] if acts else "",
            "pipe_first": acts_all[0] if acts_all else ""}


def registry_side(keys: set, reg: dict) -> dict:
    ph = [p for k in keys for p in reg[k]["phases"]]
    it = lambda xs: round(sum(p["it"] for p in xs), 1)
    nonen = sorted(p["cod"] for p in ph if p["ps"] != "energized" and p["cod"])
    uc = sorted(p["cod"] for p in ph if p["ps"] == "under_construction" and p["cod"])
    return {"campuses": sorted(reg[k]["campus"] for k in keys), "dev": sorted({reg[k]["dev"] for k in keys}),
            "n": len(ph), "it": it(ph), "it_en": it([p for p in ph if p["ps"] == "energized"]),
            "it_uc": it([p for p in ph if p["ps"] == "under_construction"]), "it_ns": it([p for p in ph if p["ps"] == "not_started"]),
            "it_bear_delayed": it([p for p in ph if p["bear"] == "delayed"]),
            "u": sorted({p["u"] for p in ph if p["u"]}),
            "cod_first": nonen[0] if nonen else "", "cod_last": nonen[-1] if nonen else "",
            "uc_first": uc[0] if uc else "", "ids": sorted(p["id"] for p in ph)}


def flags(r: dict, a: dict) -> list[dict]:
    out = []
    if a["it_wd"] > 0 and (r["it_uc"] + r["it_ns"]) > 0:
        out.append({"k": "withdrawn", "sev": 3, "t": f"Aterio marks {a['n_wd']} building(s), {a['it_wd']:.0f} MW IT-eq, Not Approved/Withdrawn or Cancelled; the registry carries {r['it_uc'] + r['it_ns']:.0f} MW still to come."})
    if a["it_delayed"] > 0:
        out.append({"k": "delayed", "sev": 2, "t": f"Aterio marks {a['it_delayed']:.0f} MW IT-eq Delayed."})
    c = a["cnt"]
    if r["it_uc"] >= 50 and c["uc"] + c["active"] + c["delayed"] == 0:
        sz = f"{a['it_ann']:.0f} MW IT-eq" if a["it_ann"] > 0 else "no MW figure"
        out.append({"k": "reg_ahead", "sev": 3, "t": f"Registry has {r['it_uc']:.0f} MW under construction; Aterio lists {c['ann']} building(s), all only announced ({sz}){', plus ' + str(c['wd']) + ' withdrawn' if c['wd'] else ''}."})
    if (r["it_uc"] + r["it_ns"]) >= 50 and c["active"] > 0 and c["uc"] + c["delayed"] + c["ann"] == 0:
        out.append({"k": "aterio_done", "sev": 2, "t": f"Registry still has {r['it_uc'] + r['it_ns']:.0f} MW to come; Aterio shows every building active ({c['active']})."})
    if r["it_uc"] == 0 and r["it_ns"] > 0 and a["it_uc"] >= 50:
        out.append({"k": "aterio_ahead", "sev": 2, "t": f"Registry has nothing under construction ({r['it_ns']:.0f} MW not started); Aterio has {a['it_uc']:.0f} MW IT-eq under construction ({c['uc']} building(s))."})
    if r["cod_first"] and a["pipe_first"]:
        d = months(r["cod_first"], a["uc_first"] or a["pipe_first"])
        if d is not None and abs(d) >= DATE_FLAG_M:
            out.append({"k": "later" if d > 0 else "earlier", "sev": 2 if d > 0 else 1,
                        "t": f"First date: registry {r['cod_first']}, Aterio {a['uc_first'] or a['pipe_first']} ({'+' if d > 0 else ''}{d} months{' — Aterio later' if d > 0 else ' — Aterio earlier'})."})
    if r["it"] >= 50 and a["it_win"] >= 50:
        ratio = a["it_win"] / r["it"]
        if not SIZE_BAND[0] <= ratio <= SIZE_BAND[1]:
            out.append({"k": "size", "sev": 1, "t": f"Size 2026-30: registry {r['it']:.0f} MW vs Aterio {a['it_win']:.0f} MW IT-eq (×{ratio:.1f})."})
    return out


# ----------------------------------------------------------------------------- run
def run(src: str | None = None, suggest_out: list | None = None) -> dict:
    global FAC_IT
    inv_path, asof = find_inventory(src)
    ac, blds, FAC_IT = aterio_campuses(inv_path)
    reg = registry_campuses()
    mdoc = json.load(open(MAP_FILE, encoding="utf-8")) if os.path.exists(MAP_FILE) else {}
    mp, verdicts, holds = mdoc.get("map", {}), mdoc.get("verdicts", {}), mdoc.get("holds", {})
    res, suggest = match(reg, ac, mp)
    if suggest_out is not None:
        suggest_out.extend(suggest)
    G = groups(res)
    matched_r = set().union(*[g[0] for g in G]) if G else set()
    matched_a = set().union(*[g[1] for g in G]) if G else set()
    rows = []
    for rk, ak in G:
        r, a = registry_side(rk, reg), aterio_side(ak, ac, blds)
        fl = flags(r, a)
        how = sorted({res[k]["how"] for k in rk})
        vd = next((verdicts[k] for k in sorted(rk) if k in verdicts), None)
        rows.append({"st": reg[next(iter(rk))]["st"], "reg": r, "at": a, "flags": fl, "sev": max([f["sev"] for f in fl], default=0),
                     "how": how, "verdict": vd,
                     "notes": [res[k]["note"] for k in sorted(rk) if res[k]["note"] and res[k]["how"] == "reviewed"]})
    rows.sort(key=lambda x: (-x["sev"], -(x["reg"]["it"] + x["at"]["it_win"])))
    reg_only = []
    for k, rc in reg.items():
        if k in matched_r:
            continue
        r = registry_side({k}, reg)
        reg_only.append({"st": rc["st"], "campus": rc["campus"], "dev": rc["dev"], "it": r["it"], "it_uc": r["it_uc"],
                         "it_ns": r["it_ns"], "it_en": r["it_en"], "cod_first": r["cod_first"], "u": r["u"],
                         "how": res[k]["how"], "note": res[k]["note"]})
    reg_only.sort(key=lambda x: -x["it"])
    at_only = []
    for k, x in ac.items():
        if k in matched_a:
            continue
        a = aterio_side({k}, ac, blds)
        if a["it_uc"] + a["it_delayed"] <= 0:
            continue
        at_only.append({"st": x["st"], "key": k, "name": x["name"], "prov": x["prov"], "users": x["users"],
                        "city": x["city"], "county": x["county"], "it_uc": a["it_uc"], "it_delayed": a["it_delayed"],
                        "it_ann": a["it_ann"], "it_active": a["it_active"], "uc_first": a["uc_first"], "uc_last": a["uc_last"],
                        "hold": (holds.get(k) or {}).get("t", "")})
    at_only.sort(key=lambda x: -(x["it_uc"] + x["it_delayed"]))
    # state coverage: Aterio under construction (2026-30, IT-eq) vs how much of it sits in matched campuses; registry UC
    st = defaultdict(lambda: {"at_uc": 0.0, "at_uc_matched": 0.0, "reg_uc": 0.0, "reg_all": 0.0, "at_ann_hi": 0.0})
    for k, bl in blds.items():
        s = ac[k]["st"]
        for x in bl:
            if x["g"] in ("uc", "delayed") and (in_win(x["act"]) or not x["act"]):
                st[s]["at_uc"] += x["mw"] / FAC_IT
                if k in matched_a:
                    st[s]["at_uc_matched"] += x["mw"] / FAC_IT
            if x["g"] == "ann" and x["like"] == "High" and in_win(x["act"]):
                st[s]["at_ann_hi"] += x["mw"] / FAC_IT
    for rc in reg.values():
        for p in rc["phases"]:
            st[rc["st"]]["reg_all"] += p["it"]
            if p["ps"] == "under_construction":
                st[rc["st"]]["reg_uc"] += p["it"]
    states = sorted(({"st": s, **{k: round(v / 1000, 2) for k, v in d.items()}} for s, d in st.items()),
                    key=lambda x: -x["at_uc"])
    tot = lambda key, xs: round(sum(x[key] for x in xs), 2)
    nflag = defaultdict(int)
    for r in rows:
        for f in r["flags"]:
            nflag[f["k"]] += 1
    out = {"asof": asof, "inventory": os.path.basename(inv_path), "fac_it": FAC_IT, "window": list(WIN),
           "rules": {"auto_min": AUTO_MIN, "date_flag_m": DATE_FLAG_M, "size_band": list(SIZE_BAND)},
           "n_reg": len(reg), "n_reg_matched": len(matched_r), "n_reviewed": sum(1 for r in res.values() if r["how"] == "reviewed"),
           "n_auto": sum(1 for r in res.values() if r["how"] == "auto"),
           "n_groups": len(G), "flag_counts": dict(nflag),
           "verdict_counts": {s: sum(1 for v in verdicts.values() if v.get("status") == s) for s in ("fixed", "not_adopted", "explained", "open")},
           "map_reviewed": mdoc.get("reviewed", ""),
           "stale_map": [f"{k} -> {s}" for k, r in res.items() for s in r.get("stale", [])],
           "totals": {"at_uc": tot("at_uc", states), "at_uc_matched": tot("at_uc_matched", states), "reg_uc": tot("reg_uc", states),
                      "reg_all": tot("reg_all", states), "at_ann_hi": tot("at_ann_hi", states),
                      "reg_only_it": round(sum(x["it"] for x in reg_only) / 1000, 2),
                      "at_only_uc": round(sum(x["it_uc"] + x["it_delayed"] for x in at_only) / 1000, 2)},
           "states": states, "groups": rows, "reg_only": reg_only, "at_only": at_only[:150], "n_at_only": len(at_only),
           "n_held": sum(1 for x in at_only if x["hold"]), "it_held": round(sum(x["it_uc"] + x["it_delayed"] for x in at_only if x["hold"]) / 1000, 2),
           "suggest": [{"reg": k, "cands": [{"score": s, "km": d, "key": a, "name": ac[a]["name"], "prov": ac[a]["prov"]} for s, d, a in c]}
                       for k, c in suggest]}
    return out


def write(out: dict) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "xchk.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    t = out["totals"]
    L = [f"# Registry vs Aterio census — cross-check (Aterio {out['asof']})", "",
         f"Registry campuses {out['n_reg']}: matched {out['n_reg_matched']} ({out['n_reviewed']} hand-reviewed, {out['n_auto']} auto). "
         f"Aterio under construction 2026-30: {t['at_uc']:.1f} GW IT-eq, of which {t['at_uc_matched']:.1f} GW sits on campuses the registry has. "
         f"Registry under construction {t['reg_uc']:.1f} GW, all phases {t['reg_all']:.1f} GW.", "",
         "## Flags (most serious first)", ""]
    for g in out["groups"]:
        if not g["flags"]:
            continue
        L.append(f"- **{g['st']} · {' + '.join(g['reg']['campuses'])}** ↔ {' + '.join(g['at']['names'])} ({', '.join(g['at']['prov'])})")
        for f in g["flags"]:
            L.append(f"  - [{f['k']}] {f['t']}")
    L += ["", "## Registry-only (no Aterio match)", ""]
    L += [f"- {x['st']} · {x['campus']} — {x['it']:.0f} MW IT-eq ({x['how']}{': ' + x['note'] if x['note'] else ''})" for x in out["reg_only"]]
    L += ["", f"## Aterio-only, under construction (top 40 of {out['n_at_only']})", ""]
    L += [f"- {x['st']} · {x['name']} ({x['prov']}, {x['city']}) — UC {x['it_uc']:.0f} MW IT-eq, first {x['uc_first']}" for x in out["at_only"][:40]]
    with open(os.path.join(OUT_DIR, "xchk_review.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--suggest", action="store_true", help="print unmatched registry campuses with candidates")
    a = ap.parse_args()
    sug = []
    out = run(a.src, sug)
    write(out)
    t = out["totals"]
    print(f"Aterio {out['asof']} · registry {out['n_reg']} campuses, matched {out['n_reg_matched']} · groups {out['n_groups']} · flags {out['flag_counts']}")
    print(f"Aterio UC 2026-30 {t['at_uc']} GW IT-eq (matched {t['at_uc_matched']}) · registry UC {t['reg_uc']} · registry-only {t['reg_only_it']} · Aterio-only UC {t['at_only_uc']}")
    if out["stale_map"]:
        print("STALE map entries:", out["stale_map"])
    if a.suggest:
        for k, c in sug:
            print(k)
            for s, d, key in c:
                print(f"    {s:5.2f} {d:6.1f} km  {key}")


if __name__ == "__main__":
    main()
