"""US data-center delay model — bottom-up by project phase.

Reads   _wiki/_data/dc_projects/raw/*.csv        regional registry files (see SCHEMA.md)
        _wiki/_data/dc_projects/overrides.csv    optional hand corrections (same header; replaces rows by project_id)
        _wiki/_data/dc_projects/state_rules.json state instruments, governors, scenarios, lead times, basis factors
        _wiki/_data/dc_projects/local_moratoria.json
        _wiki/_data/dc_projects/us_states_albers_10m.json  (us-atlas@3.0.1, pre-projected Albers USA)
Writes  _wiki/_data/dc_projects/projects.csv      merged + validated registry
        _wiki/_data/dc_projects/model_output.json per-phase results, aggregates, guardrails
        _wiki/_data/dc_projects/validation.txt    schema problems found while merging
        _wiki/_dashboards/dc-delay-risk.html      the dashboard

Bucket logic (per phase, per scenario) — mirrors the Capstone internal deck's waterfall:
  1 energized   phase_status == energized, or cod_base before the as-of month
  2 no_pause    no state instrument active in the scenario and no local moratorium covers the site
  3 protected   a pause exists but does not reach the phase: it needs no approval the pause blocks,
                or it already holds that approval (issued before the pause started)
  4 ends_first  the pause binds, but ends before the approval is needed
                (need date = cod_base - lead time of the blocked approval)
  5 delayed     pause end > need date -> new cod = pause end + lead time (max across binding pauses)
Unknown approval status: if the need date falls before the pause started, the schedule implies the
approval is in hand (protected); otherwise the scenario's `unknown_exposed` list decides, by phase_status,
whether an unknown counts as not-yet-obtained. These defaults are shown on the page.

stdlib only. Run:  py "E:\\Wiki Felipe empresas\\_wiki\\_tools\\build_dc_delay.py"
"""
from __future__ import annotations

import csv
import glob
import html
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # _wiki
DATA = os.environ.get("DC_DATA") or os.path.join(ROOT, "_data", "dc_projects")          # env overrides: tests only
DASH = os.environ.get("DC_DASH") or os.path.join(ROOT, "_dashboards", "dc-delay-risk.html")

COLS = ("project_id,campus,phase,developer,tenant,city,county,state,lat,lon,mw,mw_basis,campus_status,"
        "phase_status,likelihood,cod_base,cod_source,power_path,grid,utility,air_permit,air_permit_date,"
        "interconnection,local_approval,local_approval_date,local_moratorium,source,source_date,notes").split(",")
ENUMS = {
    "mw_basis": {"IT", "facility", "grid", "gen", "unknown"},
    "campus_status": {"operating_expanding", "under_construction", "announced"},
    "phase_status": {"energized", "under_construction", "not_started"},
    "likelihood": {"high", "medium", "low", ""},
    "cod_source": {"company", "filing", "press", "analyst", "year_only", "estimate", ""},
    "power_path": {"grid", "btm_gas", "hybrid", "nuclear", "other", ""},
    "air_permit": {"n/a", "issued", "pending", "not_filed", "unknown", ""},
    "interconnection": {"energized", "agreement", "study", "unknown", ""},
    "local_approval": {"approved", "pending", "denied", "unknown", ""},
}
BUCKETS = ["energized", "no_pause", "protected", "ends_first", "delayed"]
YEARS = [2026, 2027, 2028, 2029, 2030]
STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "PR": "Puerto Rico",
}
NAME_TO_ST = {v: k for k, v in STATE_NAMES.items()}


# ----------------------------------------------------------------------------- months
def m_parse(s: str | None) -> int | None:
    """'YYYY-MM' (or 'YYYY') -> month index; None if blank/invalid."""
    if not s:
        return None
    s = s.strip()
    try:
        if len(s) == 4:
            return int(s) * 12 + 5
        y, m = s[:7].split("-")
        y, m = int(y), int(m)
        if not 1 <= m <= 12:
            return None
        return y * 12 + (m - 1)
    except ValueError:
        return None


def m_fmt(i: int | None) -> str:
    return "" if i is None else f"{i // 12:04d}-{i % 12 + 1:02d}"


def m_year(i: int) -> int:
    return i // 12


# ----------------------------------------------------------------------------- registry
def load_registry(problems: list[str]) -> list[dict]:
    rows: dict[str, dict] = {}
    files = sorted(glob.glob(os.path.join(DATA, "raw", "*.csv")))
    ov = os.path.join(DATA, "overrides.csv")
    for path in files + ([ov] if os.path.exists(ov) else []):
        tag = os.path.basename(path)
        with open(path, newline="", encoding="utf-8-sig") as fh:
            rd = csv.DictReader(fh)
            missing = [c for c in COLS if c not in (rd.fieldnames or [])]
            if missing:
                problems.append(f"{tag}: missing columns {missing}")
            for n, r in enumerate(rd, start=2):
                r = {c: (r.get(c) or "").strip() for c in COLS}
                r["_file"] = tag
                pid = r["project_id"]
                if not pid:
                    problems.append(f"{tag}:{n}: blank project_id — skipped")
                    continue
                if tag == "overrides.csv" and r["phase"] == "DROP":      # hand fix: remove a raw row (e.g. split into tranches)
                    rows.pop(pid, None)
                    continue
                for c, ok in ENUMS.items():
                    if r[c] not in ok:
                        problems.append(f"{tag}:{n} {pid}: {c}={r[c]!r} not in schema")
                if r["state"] not in STATE_NAMES:
                    problems.append(f"{tag}:{n} {pid}: state={r['state']!r}")
                try:
                    r["_mw"] = float(r["mw"])
                except ValueError:
                    problems.append(f"{tag}:{n} {pid}: mw={r['mw']!r} not numeric — skipped")
                    continue
                if m_parse(r["cod_base"]) is None and r["phase_status"] != "energized":
                    problems.append(f"{tag}:{n} {pid}: cod_base={r['cod_base']!r} unparseable")
                if not r["source"]:
                    problems.append(f"{tag}:{n} {pid}: no source")
                if pid in rows and tag != "overrides.csv":
                    old = rows[pid]
                    problems.append(f"{tag}:{n} {pid}: duplicate of {old['_file']} — kept the newer source_date")
                    if (r["source_date"] or "") < (old["source_date"] or ""):
                        continue
                rows[pid] = r
    return list(rows.values())


def apply_adjustments(rows: list[dict], problems: list[str]) -> list[dict]:
    """adjustments.json (HAND-EDIT): date_shift = [{prefix, months, why}] moves cod_base of every row whose id starts
    with prefix (one date basis: energization); set_fields = [{prefix, fields, why}] overwrites fields."""
    path = os.path.join(DATA, "adjustments.json")
    if not os.path.exists(path):
        return rows
    adj = json.load(open(path, encoding="utf-8"))
    for a in adj.get("date_shift", []):
        hit = 0
        for r in rows:
            c = m_parse(r["cod_base"])
            if r["project_id"].startswith(a["prefix"]) and c is not None:
                r["cod_base"] = m_fmt(c + a["months"])
                r["notes"] = f"DATE SHIFT {a['months']:+d}m ({a['why']}) | " + r["notes"]
                hit += 1
        if not hit:
            problems.append(f"adjustments.json date_shift: no row starts with {a['prefix']}")
    for a in adj.get("set_fields", []):
        hit = 0
        for r in rows:
            if r["project_id"].startswith(a["prefix"]):
                for k, v in a["fields"].items():
                    r[k] = v
                r["notes"] = f"SET {a['fields']} ({a['why']}) | " + r["notes"]
                hit += 1
        if not hit:
            problems.append(f"adjustments.json set_fields: no row starts with {a['prefix']}")
    return rows


def apply_ramps(rows: list[dict], problems: list[str]) -> list[dict]:
    """ramps.json: {project_id: {"dates": [YYYY-MM, ...], "why": text, "status_after_first": optional,
    "shares": optional list summing to 1}} — a campus row dated whole at its first phase is split into tranches on
    those dates: equal unless a sourced `shares` list is given (Capstone ESTIMATE either way)."""
    path = os.path.join(DATA, "ramps.json")
    if not os.path.exists(path):
        return rows
    ramps = {k: v for k, v in json.load(open(path, encoding="utf-8")).items() if not k.startswith("_")}
    out = []
    for r in rows:
        spec = ramps.get(r["project_id"])
        if not spec:
            out.append(r)
            continue
        n = len(spec["dates"])
        sh = spec.get("shares") or [1.0 / n] * n
        if len(sh) != n or abs(sum(sh) - 1) > 1e-6:
            problems.append(f"ramps.json: {r['project_id']} shares must have {n} entries summing to 1 - equal split used")
            sh = [1.0 / n] * n
        for k, d in enumerate(spec["dates"], start=1):
            t = dict(r)
            t["project_id"] = f"{r['project_id']}-T{k}"
            t["phase"] = f"{r['phase']} · tranche {k}/{n}"
            t["_mw"] = r["_mw"] * sh[k - 1]
            t["mw"] = f"{t['_mw']:.1f}"
            t["cod_base"] = d
            t["cod_source"] = "estimate" if k > 1 or d != r["cod_base"][:7] else r["cod_source"]
            if k > 1 and spec.get("status_after_first"):
                t["phase_status"] = spec["status_after_first"]
            t["notes"] = f"RAMP SPLIT (Capstone estimate): {r['mw']} MW in {n} {'sourced-share' if spec.get('shares') else 'equal'} tranches {spec['dates'][0]}→{spec['dates'][-1]} — {spec['why']} | {r['notes']}"
            out.append(t)
        ramps.pop(r["project_id"])
    for k in ramps:
        problems.append(f"ramps.json: {k} not found in the registry")
    return out


def write_merged(rows: list[dict]) -> None:
    with open(os.path.join(DATA, "projects.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS + ["source_file"])
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["state"], r["campus"], r["cod_base"], r["project_id"])):
            w.writerow({**{c: r[c] for c in COLS}, "source_file": r["_file"]})


# ----------------------------------------------------------------------------- rules
def norm_place(s: str) -> str:
    s = (s or "").lower()
    for w in (" county", " parish", " township", " city of", "city of ", " city", " borough", " village", " town"):
        s = s.replace(w, "")
    return s.strip()


def local_matches(row: dict, locals_: list[dict]) -> list[dict]:
    out = []
    lm = (row["local_moratorium"] or "").lower()
    for L in locals_:
        if L.get("state") != row["state"]:
            continue
        j = norm_place(L.get("jurisdiction", ""))
        c = norm_place(L.get("county", ""))
        hit = False
        if L.get("match") == "explicit":           # narrow instruments: only rows that name them
            if lm and j and j in lm:
                out.append(L)
            continue
        if L.get("level") == "county" and c and c == norm_place(row["county"]):
            hit = True
        elif j and (j == norm_place(row["city"]) or (L.get("level") == "county" and j == norm_place(row["county"]))):
            hit = True
        elif lm and j and j in lm:
            hit = True
        if hit:
            out.append(L)
    return out


def instrument_hits(row: dict, kind: str) -> bool:
    """Does an instrument that blocks `kind` apply to this phase at all?"""
    if kind == "air_permit":
        return row["power_path"] in ("btm_gas", "hybrid") or row["air_permit"] in ("pending", "not_filed")
    if kind == "interconnection":
        return row["power_path"] in ("grid", "hybrid", "nuclear", "") and row["interconnection"] != "energized"
    if kind == "new_license":
        return row["phase_status"] == "not_started"
    return False


def approval_state(row: dict, kind: str, sc: dict) -> tuple[str, int | None]:
    """(status, date) of the approval an instrument of `kind` blocks. status: have | need | unknown."""
    if kind == "air_permit":
        st = row["air_permit"]
        if st == "issued":
            return "have", m_parse(row["air_permit_date"])
        if st in ("pending", "not_filed"):
            return "need", m_parse(row["air_permit_date"])
        return "unknown", None
    if kind == "interconnection":
        st = row["interconnection"]
        if st == "energized":
            return "have", None
        if st == "agreement":                      # scenario switch: ERCOT says even Base Load still needs verification
            return ("have", None) if sc.get("agreement_protects", True) else ("need", None)
        if st == "study":
            return "need", None
        return "unknown", None
    if kind == "new_license":
        st = row["local_approval"]
        if st == "approved":
            return "have", m_parse(row["local_approval_date"])
        if st in ("pending", "denied"):
            return "need", m_parse(row["local_approval_date"])
        return "unknown", None
    return "unknown", None


def classify(row: dict, sc_id: str, sc: dict, rules: dict, locals_: list[dict], as_of: int) -> dict:
    cod = m_parse(row["cod_base"])
    if cod is None and row["phase_status"] != "energized":
        return {"b": "undated", "n": None, "d": 0, "r": "no energization date in the sources — outside the 2026-30 universe"}
    blocked_past = row["air_permit"] == "pending" or row["interconnection"] == "study"
    if row["phase_status"] == "energized" or (cod is not None and cod < as_of and not blocked_past):
        return {"b": "energized", "n": cod, "d": 0, "r": "energized before " + m_fmt(as_of)}
    lead = rules["lead_months"]
    pauses, notes, exempted = [], [], False
    for ins in rules["instruments"]:
        if ins["state"] != row["state"] or not ins["active"].get(sc_id):
            continue
        if ins.get("grid") and row["grid"] != ins["grid"]:
            continue
        if ins.get("min_mw") and row["_campus_mw"] < ins["min_mw"]:
            continue
        if any(row["project_id"].startswith(px) for px in ins.get("exempt", {}).get(sc_id, [])):
            notes.append(f"{ins['label']}: carved out in this scenario ({ins.get('exempt_why', '')})")
            exempted = True
            continue
        pauses.append({"id": ins["id"], "label": ins["label"], "blocks": ins["blocks"],
                       "start": m_parse(ins["start"][sc_id] if isinstance(ins["start"], dict) else ins["start"]),
                       "end": m_parse(ins["end"][sc_id])})
    for L in local_matches(row, locals_):
        if not L["active"].get(sc_id):
            continue
        pauses.append({"id": L["id"], "label": L["jurisdiction"] + (" local ban (ballot)" if L.get("ban") else " local moratorium"),
                       "blocks": L.get("blocks", "new_license"),
                       "start": m_parse(L["start"]), "end": m_parse(L["end"][sc_id])})
    if not pauses:
        if exempted:
            return {"b": "protected", "n": cod, "d": 0, "r": "; ".join(notes)}
        return {"b": "no_pause", "n": cod, "d": 0, "r": "no state or local pause in this scenario"}
    binding = []
    for p in pauses:
        kinds = p["blocks"] if isinstance(p["blocks"], list) else [p["blocks"]]
        for kind in kinds:
            if not instrument_hits(row, kind):
                notes.append(f"{p['label']}: does not reach ({kind} not needed)")
                continue
            need = cod - lead[kind]
            st, dt = approval_state(row, kind, sc)
            if st == "have":
                notes.append(f"{p['label']}: {kind} already in hand" + (f" ({m_fmt(dt)})" if dt else ""))
                continue
            if st == "unknown":
                if need < p["start"]:
                    notes.append(f"{p['label']}: {kind} needed by {m_fmt(need)}, before the pause → schedule implies in hand")
                    continue
                if row["phase_status"] not in sc["unknown_exposed"].get(kind, []):
                    notes.append(f"{p['label']}: {kind} status unknown → assumed in hand ({row['phase_status']})")
                    continue
            if p["end"] <= need:
                binding.append((p, kind, need, None))
                continue
            # attribution: without the pause the approval lands by max(need, start); the pause moves it to `end`
            binding.append((p, kind, need, cod + (p["end"] - max(need, p["start"]))))
    if not binding:
        return {"b": "protected", "n": cod, "d": 0, "r": "; ".join(notes)}
    delays = [(new, p, kind, need) for p, kind, need, new in binding if new is not None]
    if not delays:
        p, kind, need, _ = binding[0]
        return {"b": "ends_first", "n": cod, "d": 0,
                "r": f"{p['label']} ends {m_fmt(p['end'])}, {kind} needed by {m_fmt(need)}"}
    new, p, kind, need = max(delays, key=lambda t: t[0])
    new = max(new, cod)
    why = (f"{kind} needed by {m_fmt(need)} → +{lead[kind]}m after reopening" if need >= p["start"]
           else f"{kind} was due {m_fmt(need)}, before the pause began → slips by the pause length")
    return {"b": "delayed", "n": new, "d": new - cod, "r": f"{p['label']} to {m_fmt(p['end'])}: {why}"}


# ----------------------------------------------------------------------------- aggregation
def it_eq(row: dict, rules: dict) -> float:
    return row["_mw"] / rules["basis"]["to_it"].get(row["mw_basis"] or "unknown", rules["basis"]["to_it"]["unknown"])


def in_universe(row: dict, uni: str) -> bool:
    cod = m_parse(row["cod_base"])
    if cod is None or not (2026 * 12 <= cod <= 2030 * 12 + 11):
        return False
    if row["likelihood"] == "low":          # Aterio's low tier = announcement only (<40%): never counted as building
        return False                        # (2026-11-06 double-check: unleased spec / stale rows inflated the delay)
    if row["campus_status"] in ("under_construction", "operating_expanding"):
        return True
    return uni == "pipeline" and row["campus_status"] == "announced" and row["likelihood"] in ("high", "medium")


def _empty_state():
    return {"gw_2630": 0.0, "gw_2628": 0.0, "b2628": {b: 0.0 for b in BUCKETS}, "b2630": {b: 0.0 for b in BUCKETS},
            "yshift_2628": 0.0, "yshift_2630": 0.0, "to_2031": 0.0, "n": 0, "month_only": 0.0,
            "ab": {y: 0.0 for y in YEARS + [2031]}, "as": {y: 0.0 for y in YEARS + [2031]}}


def _add_cell(s: dict, cy: int, ny: int, bucket: str, g: float, delayed: bool) -> None:
    """Add g GW (base year cy, scenario year ny) to a state-shaped accumulator."""
    s["gw_2630"] += g
    s["b2630"][bucket] += g
    s["ab"][cy] += g
    s["as"][ny] += g
    if cy <= 2028:
        s["gw_2628"] += g
        s["b2628"][bucket] += g
    if delayed:
        if ny != cy:
            s["yshift_2630"] += g
            if cy <= 2028:
                s["yshift_2628"] += g
        else:
            s["month_only"] += g
        if ny >= 2031:
            s["to_2031"] += g


def _finish(states: dict, n: int) -> dict:
    out = {"wf": {b: 0.0 for b in BUCKETS}, "total": 0.0, "delayed_month_only": 0.0, "delayed_year_shift": 0.0,
           "to_2031": 0.0, "annual_base": {y: 0.0 for y in YEARS + [2031]},
           "annual_scen": {y: 0.0 for y in YEARS + [2031]}, "states": states, "n": n}
    for v in states.values():
        out["total"] += v["gw_2630"]
        for b in BUCKETS:
            out["wf"][b] += v["b2630"][b]
        out["delayed_month_only"] += v["month_only"]
        out["delayed_year_shift"] += v["yshift_2630"]
        out["to_2031"] += v["to_2031"]
        for y in YEARS + [2031]:
            out["annual_base"][y] += v["ab"][y]
            out["annual_scen"][y] += v["as"][y]
    out["pct"] = {y: (out["annual_scen"][y] / out["annual_base"][y] - 1) if out["annual_base"][y] else None
                  for y in YEARS}
    return out


def aggregate(rows: list[dict], res: list[dict], uni: str, rules: dict) -> dict:
    """Registry aggregates. Also keeps the per-state x base-year cells (`_cells`) the rake needs."""
    st, cells, n = defaultdict(_empty_state), defaultdict(list), 0
    for r, x in zip(rows, res):
        if not in_universe(r, uni):
            continue
        g = it_eq(r, rules) / 1000.0
        cy = m_year(m_parse(r["cod_base"]))
        ny = min(m_year(x["n"]), 2031)
        n += 1
        st[r["state"]]["n"] += 1
        _add_cell(st[r["state"]], cy, ny, x["b"], g, x["b"] == "delayed")
        cells[r["state"]].append((cy, ny, x["b"], g))
    out = _finish(dict(st), n)
    out["_cells"] = dict(cells)
    return out


def rake(agg: dict, rules: dict, iters: int = 500) -> dict:
    """Extrapolate the registry to the reference deck's Aterio totals by iterative proportional fitting on a
    state-group x base-year table: rows = the deck's top-10 states (+ one group for every other state), columns =
    the deck's base-case adds 2026-30. Every registry cell keeps its own bucket mix and slip pattern, so the result
    reads 'if the GW the registry misses looked like the GW it covers, in the same state and the same year'."""
    deck = rules["benchmarks"]["capstone_deck"]
    reg = agg["states"]
    grp = {s: (s if s in deck["states"] and reg[s]["gw_2630"] > 0.05 else "_rest") for s in reg}
    tg = {g: deck["states"][g] for g in set(grp.values()) if g != "_rest"}
    tg["_rest"] = deck["total"] - sum(tg.values())
    ty = {y: float(deck["annual_base"][str(y)]) for y in YEARS}
    # the deck's own 2026-28 state cards are a third margin (added after the 2026-11-06 double-check: without them the
    # rake missed the deck's TX/VA/PA/IN 2026-28 levels and let thin 2029-30 cells carry the headline)
    tc = {s: float(v["gw"]) for s, v in deck.get("state_cards_2628", {}).items() if s in tg}
    base = defaultdict(float)
    for s, cl in agg["_cells"].items():
        for cy, ny, b, g in cl:
            base[(grp[s], cy)] += g
    moved = {}
    for s, t in tc.items():                 # a carded state with no registry GW after 2028 cannot hold total - card in
        if not any(v > 0 for (g2, y), v in base.items() if g2 == s and y > 2028):   # 2029-30: send that remainder to
            moved[s] = round(tg[s] - t, 2)                                           # the rest-of-US group instead
            tg["_rest"] += tg[s] - t
            tg[s] = t
    m = dict(base)
    margins = ([(lambda k, g=g: k[0] == g, t) for g, t in tg.items()]
               + [(lambda k, y=y: k[1] == y, t) for y, t in ty.items()]
               + [(lambda k, s=s: k[0] == s and k[1] <= 2028, t) for s, t in tc.items()])
    for _ in range(iters):
        for sel, t in margins:
            ks = [k for k in m if sel(k)]
            tot = sum(m[k] for k in ks)
            if tot > 0:
                for k in ks:
                    m[k] *= t / tot
    w = {k: (m[k] / base[k] if base[k] else 0.0) for k in base}
    states = defaultdict(_empty_state)
    for s, cl in agg["_cells"].items():
        for cy, ny, b, g in cl:
            states[s]["n"] += 1
            _add_cell(states[s], cy, ny, b, g * w[(grp[s], cy)], b == "delayed")
    for s, v in states.items():
        v["factor"] = round(v["gw_2630"] / reg[s]["gw_2630"], 2) if reg[s]["gw_2630"] else None
    out = _finish(dict(states), agg["n"])
    out["rake"] = {"state_targets": tg, "year_targets": ty, "card_targets_2628": tc, "moved_to_rest_2930": moved,
                   "fit_card_2628": {s: round(sum(v for (g2, y), v in m.items() if g2 == s and y <= 2028), 2) for s in tc},
                   "fit_state": {g: round(sum(v for (g2, _), v in m.items() if g2 == g), 2) for g in tg},
                   "fit_year": {y: round(sum(v for (_, y2), v in m.items() if y2 == y), 2) for y in ty},
                   "weights": {f"{g}|{y}": round(v, 2) for (g, y), v in w.items()}}
    return out


def rnd(o, nd=3):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, dict):
        return {k: rnd(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [rnd(v, nd) for v in o]
    return o


# ----------------------------------------------------------------------------- map geometry
def albers_lower48():
    """d3.geoAlbersUsa lower-48 leg at scale 1300, translate [487.5, 305] (the us-atlas albers files)."""
    R = math.radians
    phi0, phi1 = R(29.5), R(45.5)
    sy0 = math.sin(phi0)
    n = (sy0 + math.sin(phi1)) / 2
    c = 1 + sy0 * (2 * n - sy0)
    r0 = math.sqrt(c) / n

    def raw(lam, phi):
        r = math.sqrt(c - 2 * n * math.sin(phi)) / n
        lam *= n
        return r * math.sin(lam), r0 - r * math.cos(lam)

    k, tx, ty = 1300.0, 487.5, 305.0
    cx, cy = raw(R(-0.6), R(38.7))

    def proj(lon, lat):
        lam = R(lon + 96.0)
        if lam > math.pi:
            lam -= 2 * math.pi
        if lam < -math.pi:
            lam += 2 * math.pi
        X, Y = raw(lam, R(lat))
        return tx + k * (X - cx), ty - k * (Y - cy)

    return proj


def state_paths() -> dict:
    topo = json.load(open(os.path.join(DATA, "us_states_albers_10m.json"), encoding="utf-8"))
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        pts = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a[1:] if pts else a)
        return pts

    def area_centroid(pts):
        a = cx = cy = 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            f = x0 * y1 - x1 * y0
            a += f
            cx += (x0 + x1) * f
            cy += (y0 + y1) * f
        if abs(a) < 1e-9:
            return abs(a), pts[0]
        return abs(a) / 2, (cx / (3 * a), cy / (3 * a))

    out = {}
    for g in topo["objects"]["states"]["geometries"]:
        st = NAME_TO_ST.get(g["properties"]["name"])
        if not st:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        d, best = [], (0, (0, 0))
        for poly in polys:
            for k, rg in enumerate(poly):
                pts = ring(rg)
                d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
                if k == 0:
                    ar, ce = area_centroid(pts)
                    if ar > best[0]:
                        best = (ar, ce)
        out[st] = {"d": "".join(d), "cx": round(best[1][0], 1), "cy": round(best[1][1], 1)}
    return out


# ----------------------------------------------------------------------------- guardrails
def guardrails(rows, results, aggs, rules) -> list[dict]:
    """Checks against observables NOT used to build the registry or the rake. 🟢 within band, 🟡 edge, 🔴 outside.
    Run on the bear scenario. None of them reuses a fitted constant (the rake targets are levels, the checks are
    shares, timing and Texas-specific delay reads from other houses)."""
    out = []
    bm = rules["benchmarks"]

    def flag(ratio, lo_g, hi_g, lo_y, hi_y):
        if ratio is None:
            return "⚪"
        if lo_g <= ratio <= hi_g:
            return "🟢"
        if lo_y <= ratio <= hi_y:
            return "🟡"
        return "🔴"

    u = aggs["bear"]["construction"]
    uc = u["total"] - u["wf"]["energized"]
    ate = bm["aterio_census"]
    cov = uc / ate["value"]
    out.append({"id": "level-aterio", "kind": "stock · coverage",
                "check": "Registry GW still under construction (campuses under construction, dated 2026-30, excl. energized; IT-eq) vs Aterio's US under-construction census",
                "model": round(uc, 1), "anchor": ate["value"], "ratio": round(cov, 2),
                "flag": flag(cov, 0.75, 1.25, 0.5, 1.5), "source": ate["source"], "caveat": ate["caveat"] + " The census counts buildings under construction; the deck's 139.5 GW counts campuses (later phases included), so the two don't reconcile with each other either."})
    deck = bm["capstone_deck"]
    out.append({"id": "level-deck", "kind": "stock · coverage",
                "check": "Registry GW vs the reference deck's Aterio base (139.5 GW dated 2026-30)",
                "model": round(u["total"], 1), "anchor": deck["total"], "ratio": round(u["total"] / deck["total"], 2),
                "flag": flag(u["total"] / deck["total"], 0.75, 1.25, 0.5, 1.5), "source": deck["source"],
                "caveat": "Coverage, not validation. The scaled view is raked to these totals, so the scaled view cannot be checked against them."})
    # timing: share of the registry's 2026-30 GW landing in 2027, vs national 2027 forecasts scaled by coverage
    b27 = u["annual_base"][2027]
    for f in bm["flows_2027"]:
        exp = f["value"] * cov
        out.append({"id": "timing-2027-" + f["id"], "kind": "flow · timing",
                    "check": f"Registry 2027 adds vs {f['who']} × registry coverage ({cov:.2f}) — above 1 means the registry's dates are front-loaded",
                    "model": round(b27, 1), "anchor": round(exp, 1), "ratio": round(b27 / exp, 2),
                    "flag": flag(b27 / exp, 0.75, 1.25, 0.5, 1.5), "source": f["source"], "caveat": f["caveat"]})
    # Texas delay vs FundaAI (independent: nothing is fitted to it any more)
    fa = bm["fundaai_tx_2027"]
    mid = (fa["lo"] + fa["hi"]) / 2
    for view, lab in (("construction", "registry"), ("scaled", "raked")):
        t = aggs["bear"][view]["states"].get("TX")
        if not t:
            continue
        cut = t["ab"][2027] - t["as"][2027]
        out.append({"id": f"delay-tx-2027-{lab}", "kind": "flow · delay",
                    "check": f"Texas net GW out of 2027 in the bear case ({lab} view) vs FundaAI's 2-3 GW IT downside",
                    "model": round(cut, 2), "anchor": f"{fa['lo']}-{fa['hi']}", "ratio": round(cut / mid, 2),
                    "flag": flag(cut / mid, fa["lo"] / mid, fa["hi"] / mid, 0.5, 1.6), "source": fa["source"],
                    "caveat": fa["caveat"] + (" Registry view covers only part of Texas, so it should sit at or below the anchor." if lab == "registry" else " Raked view is in the deck's units (basis unstated); FundaAI is IT-GW.")})
    w = bm.get("wfs_tx_held")
    if w:
        held = sum(it_eq(r, rules) / 1000 for r, x in zip(rows, results["bear"])
                   if r["state"] == "TX" and in_universe(r, "pipeline") and r["power_path"] in ("btm_gas", "hybrid")
                   and x["b"] == "delayed" and "frontier" not in r["campus"].lower())
        anchor = w["value_gen"] / rules["basis"]["to_it"]["gen"]
        out.append({"id": "delay-tx-btm-wfs", "kind": "stock · delay",
                    "check": "Texas on-site-gas GW delayed (bear, IT-eq, excl. INNIO/VoltaGrid-powered Frontier) vs Wells Fargo's ~3 GW of CAT/CMI turbines and recips on held Texas projects (÷1.5)",
                    "model": round(held, 2), "anchor": round(anchor, 2), "ratio": round(held / anchor, 2),
                    "flag": flag(held / anchor, 0.75, 1.5, 0.5, 2.5), "source": w["source"],
                    "caveat": w["caveat"] + " Order of magnitude only: generation nameplate vs load."})
    loc_tot = loc_del = 0.0
    for r, x in zip(rows, results["bear"]):
        if not in_universe(r, "pipeline"):
            continue
        if any(L["active"].get("bear") for L in local_matches(r, rules["_locals"])):
            g = it_eq(r, rules) / 1000
            loc_tot += g
            if x["b"] == "delayed" and ("local moratorium" in x["r"] or "local ban" in x["r"]):
                loc_del += g
    sa = bm["semianalysis_local"]
    share = loc_del / loc_tot if loc_tot else None
    out.append({"id": "delay-local", "kind": "ratio · delay",
                "check": "Share of registry GW inside local moratoria that is delayed (bear) vs SemiAnalysis ~1.5 of ~20 GW (~7.5%)",
                "model": None if share is None else round(share, 3), "anchor": sa["share"],
                "ratio": None if share is None else round(share / sa["share"], 2),
                "flag": "⚪" if share is None else flag(share / sa["share"], 0.5, 2.0, 0.25, 4.0),
                "source": sa["source"], "caveat": f"Only {loc_tot:.1f} GW of registry phases sit inside a matched local moratorium, and they already hold local approval: the registry under-samples the small unapproved projects local moratoria catch. " + sa["caveat"]})
    return out


# ----------------------------------------------------------------------------- main
def main() -> int:
    problems: list[str] = []
    rules = json.load(open(os.path.join(DATA, "state_rules.json"), encoding="utf-8"))
    locals_doc = json.load(open(os.path.join(DATA, "local_moratoria.json"), encoding="utf-8"))
    locals_ = locals_doc["moratoria"]
    rules["_locals"] = locals_
    as_of = m_parse(rules["as_of"])
    rows = apply_ramps(apply_adjustments(load_registry(problems), problems), problems)
    campus_mw = defaultdict(float)
    for r in rows:
        campus_mw[(r["state"], r["campus"])] += r["_mw"]
    for r in rows:
        r["_campus_mw"] = campus_mw[(r["state"], r["campus"])]
    if not rows:
        print("no registry rows found under raw/*.csv")
        return 1
    write_merged(rows)

    proj = albers_lower48()
    for r in rows:
        try:
            x, y = proj(float(r["lon"]), float(r["lat"]))
            r["_xy"] = (round(x, 1), round(y, 1))
        except ValueError:
            r["_xy"] = None
            problems.append(f"{r['_file']} {r['project_id']}: lat/lon missing — not on the map")
    for L in locals_:
        try:
            x, y = proj(float(L["lon"]), float(L["lat"]))
            L["xy"] = (round(x, 1), round(y, 1))
        except (KeyError, TypeError, ValueError):
            L["xy"] = None

    scen_ids = list(rules["scenarios"])
    results = {s: [classify(r, s, rules["scenarios"][s], rules, locals_, as_of) for r in rows] for s in scen_ids}
    aggs = {s: {u: aggregate(rows, results[s], u, rules) for u in ("construction", "pipeline")} for s in scen_ids}
    for s_ in scen_ids:
        aggs[s_]["scaled"] = rake(aggs[s_]["construction"], rules)
    rules["_calib"] = {"method": "IPF rake of registry state x base-year cells to the reference deck's state and year totals",
                       **aggs[scen_ids[0]]["scaled"]["rake"]}
    for s_ in scen_ids:
        for u in list(aggs[s_]):
            aggs[s_][u].pop("_cells", None)
    checks = guardrails(rows, results, aggs, rules)

    with open(os.path.join(DATA, "validation.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"{len(rows)} rows merged from raw/*.csv\n" + "\n".join(problems) + "\n")

    phases = []
    for i, r in enumerate(rows):
        phases.append({
            "id": r["project_id"], "campus": r["campus"], "phase": r["phase"], "dev": r["developer"],
            "ten": r["tenant"], "city": r["city"], "county": r["county"], "st": r["state"],
            "xy": r["_xy"], "mw": r["_mw"], "basis": r["mw_basis"] or "unknown", "it": round(it_eq(r, rules), 1),
            "cs": r["campus_status"], "ps": r["phase_status"], "lk": r["likelihood"], "cod": r["cod_base"][:7],
            "codsrc": r["cod_source"], "pw": r["power_path"], "air": r["air_permit"], "ic": r["interconnection"],
            "loc": r["local_approval"], "src": r["source"], "sd": r["source_date"], "notes": r["notes"],
            "u": "construction" if in_universe(r, "construction") else ("pipeline" if in_universe(r, "pipeline") else ""),
            "res": {s: {"b": results[s][i]["b"], "n": m_fmt(results[s][i]["n"]), "d": results[s][i]["d"],
                        "r": results[s][i]["r"]} for s in scen_ids},
        })
    public_rules = {k: v for k, v in rules.items() if not k.startswith("_")}
    model = {"as_of": rules["as_of"], "built": rules.get("built", ""), "n_rows": len(rows),
             "n_campuses": len({(r["state"], r["campus"]) for r in rows}),
             "scenarios": {s: rules["scenarios"][s] for s in scen_ids},
             "aggs": rnd(aggs), "checks": checks, "rules": public_rules, "locals": locals_doc, "calib": rules["_calib"],
             "phases": phases, "problems": problems[:400]}
    with open(os.path.join(DATA, "model_output.json"), "w", encoding="utf-8") as fh:
        json.dump(model, fh, ensure_ascii=False, indent=1)

    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dc_delay_ui", "template.html"),
               encoding="utf-8").read()
    payload = json.dumps({**model, "map": state_paths(), "stateNames": STATE_NAMES}, ensure_ascii=False,
                         separators=(",", ":")).replace("</", "<\\/")
    page = tpl.replace("/*__DATA__*/null", payload)
    with open(DASH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)

    b = aggs.get("bear", aggs[scen_ids[0]])["construction"]
    print(f"rows {len(rows)} · problems {len(problems)} · universe(construction) {b['total']:.1f} GW IT-eq")
    for s in scen_ids:
        a = aggs[s]["construction"]
        wf = " · ".join(f"{k} {a['wf'][k]:.1f}" for k in BUCKETS)
        print(f"  {s:7s} {wf} · year-shift {a['delayed_year_shift']:.1f} · 2031+ {a['to_2031']:.1f}")
    for c in checks:
        print(f"  {c['flag']} {c['id']}: model {c['model']} vs {c['anchor']} (x{c['ratio']})")
    print("wrote", DASH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
