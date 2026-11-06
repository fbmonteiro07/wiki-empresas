"""Weekly monitor for the US data-center registry behind dc-delay-risk.html (lane: dc-projects-monitor).

    py dc_monitor.py poll [--since YYYY-MM-DD] [--only tdlr_new,moratoria] [--no-save]
        Pull the free primary sources, diff them against the last run's snapshots and against the
        registry, and write leads to _data/dc_projects/monitor/runs/<today>/leads.{json,md}.
        Sources (each fail-soft; a failure is reported, its snapshot is left untouched):
          tdlr_new    Texas TDLR TABS registrations since the last run (cost-ranked; detail pages for the
                      large ones; data-center keywords / known owners)
          tdlr_watch  every TABS project the registry cites: completion / start / status / cost changes,
                      and registry dates that no longer match TDLR
          tceq        TCEQ gas-turbine air-permit list (issued / pending / voided): new permits, status moves
          moratoria   Moratorium Nation local inventory (CC-BY-4.0): new or changed data-center instruments
          epoch       Epoch AI Frontier Data Centers (data_centers.csv + data_center_timelines.csv)
          edgar       new 8-K / 10-Q / 10-K / S-1 / 6-K of listed developers (config edgar_tickers), MW snippets
          corpus      new wiki-corpus documents (search.db) that mention data-center MW/GW
        ERCOT (403 to scripts) and state-rule events are manual_watch items for the lane's research step.

    py dc_monitor.py apply --date YYYY-MM-DD [--write]
        Validate the lane's staged changes in runs/<date>/stage/ and (with --write) merge them:
          new.csv     new registry rows            -> raw/monitor.csv
          fixes.csv   replacement rows (same id)   -> overrides.csv   (notes must start 'MONITOR <date>:')
          drops.csv   project_id,why               -> overrides.csv DROP rows
          ramps.json  ramp specs                   -> ramps.json      (a replaced spec is kept in _history)
          shifts.json [{prefix, months, why}]      -> adjustments.json date_shift
        New rows whose notes start 'TDLR completion' get the +6m energization shift automatically.
        Old rows of every fixed/dropped id are saved to runs/<date>/applied.json.

    py dc_monitor.py rules --id <instrument> --set end.bear=2027-12 [--set ...] --source "..." --why "..." [--write]
    py dc_monitor.py rules --as-of YYYY-MM [--write]
    py dc_monitor.py rules --locals --id LOC-PA-000 --set end.bear=2027-03 --source "..." --why "..." [--write]
        Change state_rules.json (or, with --locals, local_moratoria.json) fields; the old value goes to the entry's
        `history` list; line endings and indent are kept.

    py dc_monitor.py add-local <moratorium_id> [--write]
        Build a local_moratoria.json entry from the tracker record (same conventions as the hand-built ones).

stdlib only (TLS proxy: unverified SSL context, as elsewhere in the wiki tools). Writes only under
_wiki/_data/dc_projects/.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import http.cookiejar
import io
import json
import os
import re
import sqlite3
import ssl
import sys
import time
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dc_delay as E  # noqa: E402

DATA = E.DATA
MON = os.path.join(DATA, "monitor")
SNAP = os.path.join(MON, "snapshots")
RUNS = os.path.join(MON, "runs")
SEARCH_DB = os.path.join(E.ROOT, "_data", "search.db")
CTX = ssl._create_unverified_context()
UA = "Mozilla/5.0 (Capstone research monitor)"
SEC_UA = "Capstone Research (felipe.monteiro@capstone.com.br)"   # same declared agent as E:\.claude\scripts\fetch_sec_filings.py
TODAY = dt.date.today()
SEV_ORDER = {"high": 0, "medium": 1, "low": 2}


# ----------------------------------------------------------------------------- io helpers
def jload(path: str, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def jsave(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def get(url: str, data: bytes | None = None, headers: dict | None = None, opener=None, timeout: int = 60) -> bytes:
    h = {"User-Agent": UA}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    if opener is not None:
        return opener.open(req, timeout=timeout).read()
    return urllib.request.urlopen(req, context=CTX, timeout=timeout).read()


def strip_html(t: str) -> str:
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>|</p>|</div>|</tr>|</li>", ". ", t, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).strip()


def mdy_to_iso(s: str) -> str:
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s or "")
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def lead(source: str, key: str, sev: str, title: str, detail: str = "", url: str = "", ids=(), data=None) -> dict:
    return {"source": source, "key": key, "sev": sev, "title": title, "detail": detail, "url": url,
            "registry_ids": sorted(set(ids)), "data": data or {}}


GENERIC = set(("data center centre campus the and of phase building bldg project hyperscale inc llc lp dc park tech "
               "technology technologies digital infrastructure holdings group partners energy power site ai county city "
               "texas north south east west new development developments one two llc. corp company co").split())


def toks(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(t) > 2 and t not in GENERIC}


def alias_hits(text: str, aliases: list[str]) -> list[str]:
    low = (text or "").lower()
    return [a for a in aliases if re.search(r"(?<![a-z0-9])" + re.escape(a.lower()) + r"(?![a-z0-9])", low)]


# ----------------------------------------------------------------------------- registry context
class Registry:
    def __init__(self) -> None:
        probs: list[str] = []
        self.rows = E.load_registry(probs)
        self.by_id = {r["project_id"]: r for r in self.rows}
        self.places: dict[tuple[str, str], list[str]] = {}
        self.states = {r["state"] for r in self.rows}
        for r in self.rows:
            for f in ("city", "county"):
                p = E.norm_place(r[f])
                if p:
                    self.places.setdefault((r["state"], p), []).append(r["project_id"])
        self.tabs: dict[str, list[str]] = {}
        for r in self.rows:
            for t in set(re.findall(r"TABS\d{10}", r["notes"] + " " + r["source"])):
                self.tabs.setdefault(t, []).append(r["project_id"])
        ramps = jload(os.path.join(DATA, "ramps.json"), {})
        self.ramp_why = {k: v.get("why", "") for k, v in ramps.items() if not k.startswith("_") and isinstance(v, dict)}
        for k, v in ramps.items():
            if k.startswith("_") or not isinstance(v, dict):
                continue
            for t in set(re.findall(r"TABS\d{10}", v.get("why", ""))):
                self.tabs.setdefault(t, []).append(k)
        self.campus_toks = []
        seen = set()
        for r in self.rows:
            ck = (r["state"], r["campus"])
            if ck in seen:
                continue
            seen.add(ck)
            ids = [x["project_id"] for x in self.rows if (x["state"], x["campus"]) == ck]
            self.campus_toks.append((r["state"], toks(r["campus"]), toks(r["campus"] + " " + r["developer"] + " " + r["tenant"] + " " + r["city"]), ids))

    def match_place(self, st: str, name: str) -> list[str]:
        return list(self.places.get((st, E.norm_place(name)), []))

    def match_name(self, name: str, st: str | None = None, extra: str = "") -> list[str]:
        """Fuzzy campus match: the distinctive tokens of `name` must sit in a registry campus's name tokens."""
        nt = toks(name)
        if not nt:
            return []
        best, out = 0.0, []
        for cst, ctoks, alltoks, ids in self.campus_toks:
            if st and cst != st:
                continue
            inter = nt & alltoks
            if not inter or not any(len(t) >= 4 for t in inter & ctoks):
                continue
            score = len(inter) / len(nt) + (0.2 if extra and toks(extra) & alltoks else 0)
            if score > best + 1e-9:
                best, out = score, list(ids)
            elif abs(score - best) < 1e-9:
                out += ids
        return out if best >= 0.6 else []


# ----------------------------------------------------------------------------- TDLR TABS
TABS = "https://www.tdlr.texas.gov/TABS"
TABS_COLS = ["ProjectId", "ProjectNumber", "ProjectName", "ProjectCreatedOn", "ProjectStatus", "FacilityName", "City",
             "County", "TypeOfWork", "EstimatedCost", "DataVersionId"]
DETAIL_KEYS = ["Registration Date", "Project Name", "Facility Name", "Location Address", "Location County", "Start Date",
               "Completion Date", "Estimated Cost", "Type of Work", "Scope of Work", "Square Footage",
               "Are the private funds provided by the tenant?", "Current Status", "Owner Name", "Owner Address",
               "TENANT", "Tenant Name", "DESIGN FIRM"]
DETAIL_STOP = ["Type of Funds", "PERSON FILING FORM", "Owner Phone", "Contact Name", "Design Firm Name",
               "Registered accessibility", "RAS Name", "Project Number"]


def tabs_opener():
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=CTX), urllib.request.HTTPCookieProcessor(cj))
    get(TABS + "/Search", opener=op)
    return op


def tabs_search(op, start: int, length: int, **filt) -> dict:
    d = {"draw": "1", "start": str(start), "length": str(length), "order[0][column]": "9", "order[0][dir]": "desc",
         "search[value]": "", "search[regex]": "false"}
    for i, c in enumerate(TABS_COLS):
        d.update({f"columns[{i}][data]": c, f"columns[{i}][name]": "", f"columns[{i}][searchable]": "true",
                  f"columns[{i}][orderable]": "true", f"columns[{i}][search][value]": "", f"columns[{i}][search][regex]": "false"})
    d.update(filt)
    raw = get(TABS + "/Search/SearchProjects", data=urllib.parse.urlencode(d).encode(), opener=op,
              headers={"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    return json.loads(raw.decode("utf-8", "ignore"))


def tabs_detail(pid: str) -> dict:
    s = strip_html(get(f"{TABS}/Search/Project/{pid}", timeout=45).decode("utf-8", "ignore"))
    parts = re.split("(" + "|".join(re.escape(k) for k in DETAIL_KEYS + DETAIL_STOP) + "):?", s)
    d = {"id": pid}
    for i in range(1, len(parts) - 1, 2):
        k, v = parts[i], parts[i + 1].strip(" .")
        if k not in d:
            d[k] = v[:500]
    return d


def detail_fields(d: dict) -> dict:
    return {"completion": mdy_to_iso(d.get("Completion Date", "")), "start": mdy_to_iso(d.get("Start Date", "")),
            "status": (d.get("Current Status") or "")[:60], "cost": (d.get("Estimated Cost") or "")[:30],
            "owner": (d.get("Owner Name") or "")[:120], "name": (d.get("Project Name") or "")[:120]}


def src_tdlr_new(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    c = cfg["tdlr"]
    counties = {v: k.replace("_", " ") for k, v in jload(os.path.join(MON, "tdlr_counties.json"), {}).items()}
    op = tabs_opener()
    rows, start, total = [], 0, None
    while start < c["max_scan_rows"]:
        res = tabs_search(op, start, 100, RegistrationDateBegin=since.strftime("%m/%d/%Y"))
        data = res.get("data") or []
        total = res.get("recordsFiltered")
        rows += data
        if len(data) < 100 or (data[-1].get("EstimatedCost") or 0) < c["min_cost_keyword"]:
            break
        start += 100
    kw, aliases = cfg["dc_keywords"], cfg["owner_aliases"]
    cands = []
    for x in rows:
        cost = x.get("EstimatedCost") or 0
        txt = f"{x.get('ProjectName')} {x.get('FacilityName')}"
        hit = alias_hits(txt, kw) or alias_hits(txt, aliases)
        if cost >= c["min_cost_detail"] or (hit and cost >= c["min_cost_keyword"]):
            cands.append(x)
    out, fetched = [], 0
    for x in cands[: c["max_detail_fetches"]]:
        pid = x.get("ProjectNumber")
        try:
            d = tabs_detail(pid)
            fetched += 1
        except Exception as e:  # noqa: BLE001
            d = {"error": str(e)}
        time.sleep(c["sleep_s"])
        txt = " ".join(str(v) for v in (x.get("ProjectName"), x.get("FacilityName"), d.get("Owner Name"),
                                         d.get("Scope of Work"), d.get("TENANT"), d.get("Tenant Name")))
        k_hits = alias_hits(txt, kw)
        a_hits = [a for a in alias_hits(txt, aliases) if a != "data center"]
        if not k_hits and not a_hits:
            continue
        cost = x.get("EstimatedCost") or 0
        county = counties.get(str(x.get("County")), str(x.get("County")))
        known = reg.tabs.get(pid, [])
        same_county = reg.match_place("TX", county)
        sev = "low" if known else ("high" if cost >= 100e6 else "medium")
        f = detail_fields(d)
        title = (f"TDLR new registration {pid}: {x.get('ProjectName')} / {x.get('FacilityName')} ({county} Co.), "
                 f"${cost / 1e6:,.0f}m, completion {f['completion'] or (x.get('EstimatedEndDate') or '')[:10]}")
        det = (f"owner {f['owner'] or '?'}; scope: {(d.get('Scope of Work') or '')[:220]}; matched: {', '.join(k_hits + a_hits)}"
               + (f"; ALREADY IN REGISTRY ({', '.join(known)})" if known else "")
               + (f"; registry rows in {county} Co.: {len(same_county)}" if same_county else ""))
        out.append(lead("tdlr_new", pid, sev, title, det, f"{TABS}/Search/Project/{pid}", known or [],
                        {"county": county, "cost": cost, **f, "address": d.get("Location Address", "")[:160],
                         "registered": (x.get("ProjectCreatedOn") or "")[:10], "same_county_ids": same_county[:12]}))
    return out, f"{len(rows)} of {total} registrations since {since} scanned, {fetched} detail pages, {len(out)} data-center leads"


def registry_tdlr_dates(txt: str, pid: str) -> list[str]:
    """Completion dates the registry text attributes to TABS id `pid`. Only two explicit forms count:
    'YYYY-MM-DD ( ... TABSid ... )' (the id inside the parenthesis right after the date) and 'TABSid completion YYYY-MM-DD'.
    Anything else is ambiguous and is not compared."""
    out = []
    for m in re.finditer(r"(20\d\d-\d\d-\d\d)\s*\(", txt):
        depth, j = 1, m.end()
        while j < len(txt) and depth:
            depth += {"(": 1, ")": -1}.get(txt[j], 0)
            j += 1
        if pid in txt[m.end(): j]:
            out.append(m.group(1))
    out += re.findall(re.escape(pid) + r"\s+completion\s+(20\d\d-\d\d-\d\d)", txt)
    return out


def src_tdlr_watch(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    c = cfg["tdlr"]
    path = os.path.join(SNAP, "tdlr_watch.json")
    snap = jload(path, {})
    out, n, errs = [], 0, 0
    for pid in sorted(reg.tabs)[: c["max_watch_fetches"]]:
        ids = reg.tabs[pid]
        try:
            f = detail_fields(tabs_detail(pid))
            n += 1
        except Exception:  # noqa: BLE001
            errs += 1
            continue
        time.sleep(c["sleep_s"])
        old = snap.get(pid)
        if old:
            ch = {k: (old.get(k), f[k]) for k in ("completion", "start", "status", "cost") if (old.get(k) or "") != (f[k] or "")}
            if ch:
                sev = "high" if "completion" in ch or "status" in ch else "medium"
                out.append(lead("tdlr_watch", pid, sev, f"TDLR {pid} changed: " + "; ".join(f"{k} {a or '-'} → {b or '-'}" for k, (a, b) in ch.items()),
                                f"{f['name']} · owner {f['owner']}", f"{TABS}/Search/Project/{pid}", ids, {"changes": ch}))
        for pidrow in ids:
            row = reg.by_id.get(pidrow)
            if not row or not f["completion"]:
                continue
            rec = registry_tdlr_dates(row["notes"] + " " + reg.ramp_why.get(pidrow, ""), pid)
            if rec and f["completion"][:7] not in {d[:7] for d in rec}:
                out.append(lead("tdlr_watch", f"{pid}|{pidrow}", "high",
                                f"Registry date vs TDLR: {pidrow} records completion {', '.join(sorted(set(rec)))} for {pid}; TDLR now shows {f['completion']}",
                                f"{f['name']} · status {f['status']} · the registry's cod_base is completion +6m (Epoch convention)",
                                f"{TABS}/Search/Project/{pid}", [pidrow], {"registry": rec, "tdlr": f["completion"]}))
        snap[pid] = {**f, "checked": TODAY.isoformat()}
    if save:
        jsave(path, snap)
    base = "baseline" if not any(v.get("checked", "") < TODAY.isoformat() for v in snap.values()) else "diffed"
    return out, f"{n} cited TABS projects re-read ({errs} errors, {base}); {len(out)} changes or registry mismatches"


# ----------------------------------------------------------------------------- TCEQ turbines
def xlsx_sheets(b: bytes) -> dict[str, list[list[str]]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    z = zipfile.ZipFile(io.BytesIO(b))
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        ss = ["".join(t.itertext()) for t in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns)]
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", ns):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        p = "xl/" + target[rid].lstrip("/").replace("xl/", "")
        rows = []
        for r in ET.fromstring(z.read(p)).iter("{%s}row" % ns["m"]):
            vals: dict[int, str] = {}
            for cell in r.findall("m:c", ns):
                col = 0
                for ch in re.match(r"[A-Z]+", cell.get("r")).group(0):
                    col = col * 26 + ord(ch) - 64
                v = cell.find("m:v", ns)
                x = "" if v is None else (v.text or "")
                if cell.get("t") == "s" and x:
                    x = ss[int(x)]
                elif cell.get("t") == "inlineStr":
                    x = "".join(cell.itertext())
                vals[col - 1] = x.strip()
            rows.append([vals.get(i, "") for i in range(max(vals) + 1)] if vals else [])
        out[sh.get("name")] = rows
    return out


def xl_date(s: str) -> str:
    try:
        f = float(s)
        if 20000 < f < 80000:
            return (dt.date(1899, 12, 30) + dt.timedelta(days=int(f))).isoformat()
    except ValueError:
        pass
    return s


def src_tceq(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    path = os.path.join(SNAP, "tceq_turbines.json")
    snap = jload(path, {})
    sheets = xlsx_sheets(get(cfg["tceq_turbines_url"], timeout=90))
    version, cur = "", {}
    for name, rows in sheets.items():
        status = "issued" if "Issued" in name else ("pending" if "Pending" in name else "voided")
        hdr_i = next((i for i, r in enumerate(rows) if r and r[0].startswith("Permit No")), None)
        for r in rows[:6]:
            if r and r[0].startswith("Version"):
                version = r[0].replace("Version", "").strip()
        if hdr_i is None:
            continue
        hdr = rows[hdr_i]
        for r in rows[hdr_i + 1:]:
            if not r or not r[0]:
                continue
            d = dict(zip(hdr, r + [""] * (len(hdr) - len(r))))
            key = f"{d.get('Permit No.', '')}|{d.get('Turbine Model', '')}"
            cur[key] = {"status": status, "company": d.get("Company Name", ""), "city": d.get("City", ""),
                        "county": d.get("County", ""), "model": d.get("Turbine Model", ""), "n": d.get("Number of CTs", ""),
                        "mw": d.get("Project MW ", d.get("Project MW", "")), "received": xl_date(d.get("Received", "")),
                        "issued": xl_date(d.get("Issue Date", ""))}
    old = snap.get("permits", {})
    out = []
    if snap.get("version") == version and old:
        note = f"version {version} unchanged since {snap.get('checked')}"
    else:
        for k, v in cur.items():
            o = old.get(k)
            if o and o["status"] == v["status"] and o["mw"] == v["mw"]:
                continue
            if not old:
                continue     # first run: baseline only
            ids = reg.match_place("TX", v["county"]) + reg.match_place("TX", v["city"])
            ah = alias_hits(v["company"], cfg["owner_aliases"])
            try:
                mw = float(v["mw"] or 0)
            except ValueError:
                mw = 0.0
            sev = "high" if (ah or ids) else ("medium" if mw >= 100 else "low")
            what = f"new {v['status']}" if not o else f"{o['status']} → {v['status']}" + (f", MW {o['mw']} → {v['mw']}" if o["mw"] != v["mw"] else "")
            out.append(lead("tceq", k, sev, f"TCEQ turbine permit {k.split('|')[0]} ({v['company']}, {v['city']}/{v['county']} Co.): {what}, {v['mw']} MW",
                            f"{v['n']} × {v['model']}; received {v['received']}, issued {v['issued'] or '-'}"
                            + (f"; owner alias {', '.join(ah)}" if ah else "") + (f"; registry rows in that county/city: {len(ids)}" if ids else ""),
                            cfg["tceq_turbines_url"], ids[:20], v))
        note = f"version {version} ({len(cur)} turbine rows; {'baseline' if not old else str(len(out)) + ' changes vs ' + str(snap.get('version'))})"
    # standing check: TX rows marked air_permit=pending (with a filing month) whose county now lists a turbine
    # permit ISSUED in or after that month — candidate for pending -> issued
    for r in reg.rows:
        if r["state"] != "TX" or r["air_permit"] != "pending" or not r["air_permit_date"]:
            continue
        c = E.norm_place(r["county"])
        hits = [k for k, v in cur.items() if v["status"] == "issued" and E.norm_place(v["county"]) == c
                and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v["issued"] or "") and v["issued"][:7] >= r["air_permit_date"][:7]]
        if hits:
            out.append(lead("tceq", f"pending|{r['project_id']}", "medium",
                            f"{r['project_id']} is air_permit=pending, and TCEQ lists issued turbine permit(s) in {r['county']} Co. dated on/after its filing",
                            "; ".join(f"{h.split('|')[0]} {cur[h]['company']} {cur[h]['mw']} MW issued {cur[h]['issued']}" for h in hits[:4]) + " — check whether one is this site",
                            cfg["tceq_turbines_url"], [r["project_id"]]))
    if save:
        jsave(path, {"version": version, "checked": TODAY.isoformat(), "permits": cur})
    return out, note


# ----------------------------------------------------------------------------- Moratorium Nation
def src_moratoria(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    path = os.path.join(SNAP, "moratoria.json")
    snap = jload(path, {})
    raw = get(cfg["moratoria_url"], timeout=90).decode("utf-8", "ignore")
    rows = [r for r in csv.DictReader(io.StringIO(raw)) if "data_center" in r.get("sectors", "")]
    in_model = set(re.findall(r"record ([a-z0-9-]+)", json.dumps(jload(os.path.join(DATA, "local_moratoria.json"), {}))))
    cur = {}
    for r in rows:
        cur[r["moratorium_id"]] = {"st": r["state_abbrev"], "jur": r["jurisdiction"], "type": r["jurisdiction_type"],
                                   "status": r["enacted_status"], "enacted": r["date_enacted_iso"],
                                   "end": r["current_end_date_iso"], "days": r["duration_days"],
                                   "lat": r["latitude"], "lon": r["longitude"]}
    old = snap.get("records", {})
    out = []
    for k, v in cur.items():
        o = old.get(k)
        if not old:
            break                # first run: baseline only
        if o and all(o.get(f) == v[f] for f in ("status", "enacted", "end", "days")):
            continue
        ids = reg.match_place(v["st"], v["jur"])
        active = v["status"] in ("active", "extended", "pending")
        sev = "high" if ids and active else ("medium" if v["st"] in reg.states and active else "low")
        what = "new record" if not o else "; ".join(f"{f} {o.get(f) or '-'} → {v[f] or '-'}" for f in ("status", "enacted", "end", "days") if o.get(f) != v[f])
        out.append(lead("moratoria", k, sev, f"Local moratorium {v['jur']} ({v['type']}, {v['st']}): {what}",
                        f"status {v['status']}, enacted {v['enacted'] or '?'}, ends {v['end'] or 'open'}"
                        + ("; IN MODEL (local_moratoria.json)" if k in in_model else "; not in local_moratoria.json — `dc_monitor.py add-local " + k + "`")
                        + (f"; covers {len(ids)} registry rows" if ids else ""),
                        cfg["moratoria_url"], ids[:30], v))
    gone = [k for k in old if k not in cur]
    for k in gone[:20]:
        out.append(lead("moratoria", k, "low", f"Local moratorium record {k} no longer in the tracker", "", cfg["moratoria_url"]))
    if save:
        jsave(path, {"checked": TODAY.isoformat(), "records": cur})
    return out, f"{len(cur)} data-center records ({'baseline' if not old else str(len(out)) + ' new/changed'}; {len(in_model & set(cur))} in the model)"


# ----------------------------------------------------------------------------- Epoch AI
def src_epoch(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    path = os.path.join(SNAP, "epoch.json")
    snap = jload(path, {})
    dcs_raw = list(csv.DictReader(io.StringIO(get(cfg["epoch_urls"]["data_centers"], timeout=90).decode("utf-8", "ignore"))))
    tl_raw = list(csv.DictReader(io.StringIO(get(cfg["epoch_urls"]["timelines"], timeout=90).decode("utf-8", "ignore"))))
    us = {r["Name"] for r in dcs_raw if "united states" in (r.get("Country") or "").lower() or (r.get("Country") or "").strip() in ("USA", "US")}
    dcs = {r["Name"]: {"mw": r.get("Current power (MW)", ""), "owner": (r.get("Owner") or "")[:120], "users": (r.get("Users") or "")[:160],
                       "project": (r.get("Project") or "")[:80], "address": (r.get("Address") or "")[:160]} for r in dcs_raw if r["Name"] in us}
    tl = {}
    for r in tl_raw:
        if r["Data center"] in us:
            tl[f"{r['Data center']}|{r['Date']}"] = {"it": r.get("IT power (MW)", ""), "mw": r.get("Power (MW)", ""),
                                                     "bldg": r.get("Buildings operational", ""), "status": (r.get("Construction status") or "")[:240]}
    old_d, old_t = snap.get("dcs", {}), snap.get("tl", {})
    out = []

    def ids_for(name: str) -> list[str]:
        a = dcs.get(name, {})
        st = None
        m = re.search(r",\s*([A-Z]{2})\b", a.get("address", ""))
        if m and m.group(1) in E.STATE_NAMES:
            st = m.group(1)
        for full, ab in E.NAME_TO_ST.items():
            if not st and full in a.get("address", ""):
                st = ab
        return reg.match_name(name + " " + a.get("project", ""), st, a.get("owner", "") + " " + a.get("users", ""))

    if old_d:
        for n, a in dcs.items():
            if n not in old_d:
                ids = ids_for(n)
                out.append(lead("epoch", n, "low" if ids else "medium", f"Epoch adds US data center '{n}' ({a['mw'] or '?'} MW now)",
                                f"owner {a['owner']}; users {a['users']}; {a['address']}" + ("" if ids else "; NOT matched to the registry"),
                                "https://epoch.ai/data/ai-data-centers", ids))
        today = TODAY.isoformat()
        for k, v in tl.items():
            o = old_t.get(k)
            if o == v:
                continue
            name, date = k.split("|", 1)
            if date < (TODAY - dt.timedelta(days=45)).isoformat() and o is None:
                continue                      # back-filled history, not a schedule change
            ids = ids_for(name)
            fut = date >= today
            sev = "high" if (ids and fut) else ("medium" if fut else "low")
            what = "new dated point" if o is None else "; ".join(f"{f} {o.get(f) or '-'} → {v[f] or '-'}" for f in ("it", "mw", "bldg") if o.get(f) != v[f]) or "status text revised"
            out.append(lead("epoch", k, sev, f"Epoch timeline {name} @ {date}: {what} (IT {v['it'] or '?'} MW, power {v['mw'] or '?'} MW)",
                            v["status"], "https://epoch.ai/data/ai-data-centers", ids, {"new": v, "old": o}))
        for k in old_t:
            if k not in tl and k.split("|", 1)[1] >= today:
                name = k.split("|", 1)[0]
                out.append(lead("epoch", k, "high" if ids_for(name) else "medium", f"Epoch removed future timeline point {k}",
                                json.dumps(old_t[k], ensure_ascii=False)[:240], "https://epoch.ai/data/ai-data-centers", ids_for(name)))
        note = f"{len(dcs)} US data centers, {len(tl)} timeline points; {len(out)} changes"
    else:
        unmatched = [n for n in dcs if not ids_for(n)]
        for n in unmatched[:40]:
            a = dcs[n]
            out.append(lead("epoch", f"coverage|{n}", "medium", f"Coverage: Epoch US data center '{n}' has no registry match ({a['mw'] or '?'} MW now)",
                            f"owner {a['owner']}; users {a['users']}; {a['address']}", "https://epoch.ai/data/ai-data-centers"))
        note = f"baseline: {len(dcs)} US data centers, {len(tl)} timeline points; {len(unmatched)} not matched to the registry"
    if save:
        jsave(path, {"checked": TODAY.isoformat(), "dcs": dcs, "tl": tl})
    return out, note


# ----------------------------------------------------------------------------- EDGAR
MW_RX = re.compile(r"\b\d[\d,.]*\s*(?:MW|megawatts?|GW|gigawatts?)\b", re.I)
CTX_RX = re.compile(r"data cent|campus|energiz|HPC|AI factory|site|facility|lease|tenant|interconnect", re.I)


def sec_get(url: str) -> bytes:
    b = get(url, headers={"User-Agent": SEC_UA, "Accept-Encoding": "identity"}, timeout=90)
    time.sleep(0.15)
    return b


def src_edgar(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    tpath = os.path.join(SNAP, "sec_tickers.json")
    tick = jload(tpath, {})
    if not tick.get("map") or tick.get("checked", "") < (TODAY - dt.timedelta(days=30)).isoformat():
        j = json.loads(sec_get("https://www.sec.gov/files/company_tickers.json"))
        tick = {"checked": TODAY.isoformat(), "map": {v["ticker"].upper(): int(v["cik_str"]) for v in j.values()}}
        if save:
            jsave(tpath, tick)
    spath = os.path.join(SNAP, "edgar_seen.json")
    seen = jload(spath, {})
    forms = set(cfg["edgar_forms"])
    new, missing = [], []
    for t, mtoks in cfg["edgar_tickers"].items():
        cik = tick["map"].get(t.upper())
        if not cik:
            missing.append(t)
            continue
        try:
            sub = json.loads(sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
        except Exception:  # noqa: BLE001
            missing.append(t + "(err)")
            continue
        rec = sub.get("filings", {}).get("recent", {})
        for form, fdate, acc, prim in zip(rec.get("form", []), rec.get("filingDate", []), rec.get("accessionNumber", []), rec.get("primaryDocument", [])):
            if fdate < since.isoformat():
                break
            if form in forms and acc not in seen:
                new.append((t, mtoks, cik, form, fdate, acc, prim))
    out = []
    for t, mtoks, cik, form, fdate, acc, prim in new[: cfg["edgar_max_docs"]]:
        base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}"
        docs = [prim]
        try:
            idx = json.loads(sec_get(base + "/index.json"))
            docs += [i["name"] for i in idx.get("directory", {}).get("item", [])
                     if re.search(r"ex-?99|dex99|ex99", i["name"], re.I) and i["name"].lower().endswith((".htm", ".html", ".txt"))]
        except Exception:  # noqa: BLE001
            pass
        text = ""
        for d in dict.fromkeys(docs):
            try:
                text += " " + strip_html(sec_get(f"{base}/{d}")[:6_000_000].decode("utf-8", "ignore"))
            except Exception:  # noqa: BLE001
                continue
        sents = re.split(r"(?<=[.;])\s+(?=[A-Z(•])", text)
        snips = []
        for s in sents:
            if MW_RX.search(s) and CTX_RX.search(s) and 30 < len(s) < 700:
                s = s.strip()[:420]
                if s not in snips:
                    snips.append(s)
            if len(snips) >= 8:
                break
        dev_rows = [r for r in reg.rows if any(m.lower() in (r["developer"] + " " + r["tenant"] + " " + r["campus"]).lower() for m in mtoks)]
        ids = [r["project_id"] for r in dev_rows if (r["city"] and len(r["city"]) > 3 and r["city"] in text) or
               (r["campus"] and len(r["campus"].split("(")[0].strip()) > 5 and r["campus"].split("(")[0].strip() in text)]
        sev = "high" if (snips and ids) else ("medium" if snips else "low")
        out.append(lead("edgar", acc, sev, f"{t} {form} filed {fdate}" + (f" — {len(snips)} MW/GW passages" if snips else " — no MW/GW passage"),
                        " ‖ ".join(snips[:5]), f"{base}/{prim}", ids[:30], {"ticker": t, "form": form, "filed": fdate, "snippets": snips}))
        seen[acc] = fdate
    if save:
        jsave(spath, {k: v for k, v in seen.items() if v >= (TODAY - dt.timedelta(days=400)).isoformat()})
    return out, f"{len(cfg['edgar_tickers'])} tickers, {len(new)} new filings since {since} ({len(out)} read)" + (f"; not resolved: {', '.join(missing)}" if missing else "")


# ----------------------------------------------------------------------------- corpus
def src_corpus(reg: Registry, cfg: dict, since: dt.date, save: bool) -> tuple[list[dict], str]:
    con = sqlite3.connect(SEARCH_DB)
    q = ("SELECT path, kind, ticker, date, title, snippet(docs, 5, '[', ']', ' … ', 28), body FROM docs "
         "WHERE docs MATCH ? AND date >= ? AND date <= ? ORDER BY bm25(docs) LIMIT 250")
    rows = con.execute(q, (cfg["corpus_query"], since.isoformat(), TODAY.isoformat())).fetchall()
    amb = set(cfg.get("ambiguous_places", []))
    places = sorted({r["city"] for r in reg.rows if r["city"] and len(r["city"]) > 4 and r["city"] not in amb}, key=len, reverse=True)
    campuses = sorted({r["campus"].split("(")[0].strip() for r in reg.rows if len(r["campus"].split("(")[0].strip()) > 6}, key=len, reverse=True)
    out = []
    for path, kind, ticker, date, title, snip, body in rows:
        if kind in cfg["corpus_kinds_skip"]:
            continue
        b = body or ""
        hit_c = [c for c in campuses if c in b][:6]
        hit_p = [p for p in places if re.search(r"\b" + re.escape(p) + r"\b", b)][:6]
        n_mw = len(MW_RX.findall(b))
        sev = "medium" if (hit_c or hit_p) and n_mw else "low"
        ids = [r["project_id"] for r in reg.rows if r["campus"].split("(")[0].strip() in hit_c][:20]
        out.append(lead("corpus", path, sev, f"[{kind} {date}] {title or os.path.basename(path)}",
                        f"{snip}" + (f" · campuses: {', '.join(hit_c)}" if hit_c else "") + (f" · places: {', '.join(hit_p)}" if hit_p else ""),
                        path, ids, {"mw_mentions": n_mw}))
    out.sort(key=lambda x: (SEV_ORDER[x["sev"]], -x["data"]["mw_mentions"]))
    return out[: cfg["corpus_max"]], f"{len(rows)} corpus documents dated {since}..{TODAY} match; {min(len(out), cfg['corpus_max'])} listed"


SOURCES = {"tdlr_new": src_tdlr_new, "tdlr_watch": src_tdlr_watch, "tceq": src_tceq, "moratoria": src_moratoria,
           "epoch": src_epoch, "edgar": src_edgar, "corpus": src_corpus}


# ----------------------------------------------------------------------------- poll
def write_md(path: str, doc: dict, cfg: dict) -> None:
    L = [f"# DC registry monitor — leads {doc['date']}", "",
         f"Window: registrations / filings / corpus since **{doc['since']}**. Registry: {doc['registry_rows']} raw rows. "
         "Leads are candidates, not facts: every registry change still needs its primary source (lane step 3).", "",
         "| source | status | note |", "|---|---|---|"]
    for s, v in doc["sources"].items():
        L.append(f"| {s} | {'ok' if v['ok'] else 'FAILED'} | {(v.get('note') or v.get('error') or '').replace('|', '/')} |")
    for sev in ("high", "medium", "low"):
        ls = [x for x in doc["leads"] if x["sev"] == sev]
        L += ["", f"## {sev.capitalize()} ({len(ls)})", ""]
        for x in ls[: (400 if sev != "low" else 80)]:
            ids = f" · registry: {', '.join(x['registry_ids'][:8])}{' …' if len(x['registry_ids']) > 8 else ''}" if x["registry_ids"] else ""
            L.append(f"- **[{x['source']}]** {x['title']}{ids}")
            if x["detail"]:
                L.append(f"  - {x['detail'][:600]}")
            if x["url"]:
                L.append(f"  - {x['url']}")
    L += ["", "## Manual watch (research step)", ""] + [f"- {m['what']} → `{m.get('instrument', '')}`" + (f" — {m['why']}" if m.get("why") else "") for m in cfg["manual_watch"]]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def cmd_poll(a) -> int:
    cfg = jload(os.path.join(MON, "config.json"), None)
    state = jload(os.path.join(MON, "state.json"), {})
    if a.since:
        since = dt.date.fromisoformat(a.since)
    elif state.get("last_poll"):
        since = dt.date.fromisoformat(state["last_poll"]) - dt.timedelta(days=1)      # 1-day overlap
    else:
        since = TODAY - dt.timedelta(days=cfg["lookback_days_first_run"])
    reg = Registry()
    only = set(a.only.split(",")) if a.only else set(SOURCES)
    doc = {"date": TODAY.isoformat(), "since": since.isoformat(), "registry_rows": len(reg.rows), "sources": {}, "leads": []}
    for name, fn in SOURCES.items():
        if name not in only:
            continue
        t0 = time.time()
        try:
            leads, note = fn(reg, cfg, since, not a.no_save)
            doc["sources"][name] = {"ok": True, "note": note, "n": len(leads), "secs": round(time.time() - t0, 1)}
            doc["leads"] += leads
        except Exception as e:  # noqa: BLE001
            doc["sources"][name] = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300], "secs": round(time.time() - t0, 1)}
        print(f"  {name:10s} {'ok ' if doc['sources'][name]['ok'] else 'ERR'} {doc['sources'][name].get('note') or doc['sources'][name].get('error')}")
    doc["leads"].sort(key=lambda x: (SEV_ORDER[x["sev"]], x["source"], x["key"]))
    run = os.path.join(RUNS, TODAY.isoformat())
    os.makedirs(run, exist_ok=True)
    jsave(os.path.join(run, "leads.json"), doc)
    write_md(os.path.join(run, "leads.md"), doc, cfg)
    if not a.no_save and not a.only:
        state.update({"last_poll": TODAY.isoformat(), "last_since": since.isoformat(),
                      "last_counts": {s: sum(1 for x in doc["leads"] if x["sev"] == s) for s in SEV_ORDER},
                      "last_failed": [s for s, v in doc["sources"].items() if not v["ok"]]})
        jsave(os.path.join(MON, "state.json"), state)
    c = {s: sum(1 for x in doc["leads"] if x["sev"] == s) for s in SEV_ORDER}
    print(f"leads: high {c['high']} · medium {c['medium']} · low {c['low']} → {os.path.join(run, 'leads.md')}")
    return 0


# ----------------------------------------------------------------------------- apply
def check_row(r: dict) -> list[str]:
    p = []
    for c in E.COLS:
        r.setdefault(c, "")
    for c, ok in E.ENUMS.items():
        if r[c] not in ok:
            p.append(f"{c}={r[c]!r}")
    if r["state"] not in E.STATE_NAMES:
        p.append(f"state={r['state']!r}")
    try:
        float(r["mw"])
    except ValueError:
        p.append(f"mw={r['mw']!r}")
    cod = E.m_parse(r["cod_base"])
    if cod is None and r["phase_status"] != "energized":
        p.append(f"cod_base={r['cod_base']!r}")
    elif cod is not None and not (E.m_parse("2026-01") <= cod <= E.m_parse("2030-12")):
        p.append(f"cod_base {r['cod_base']} outside 2026-01..2030-12")
    if not r["source"]:
        p.append("no source")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["source_date"] or ""):
        p.append(f"source_date={r['source_date']!r}")
    if not re.fullmatch(r"[A-Z]{2}-[A-Z0-9-]+", r["project_id"] or ""):
        p.append(f"project_id={r['project_id']!r} (ST-CITYSLUG-CAMPUSSLUG-PHASE)")
    return p


def write_csv(path: str, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=E.COLS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def cmd_apply(a) -> int:
    run = os.path.join(RUNS, a.date)
    st = os.path.join(run, "stage")
    if not os.path.isdir(st):
        print("no stage folder:", st)
        return 1
    probs: list[str] = []
    existing = {r["project_id"]: r for r in E.load_registry(probs)}
    new = [dict(r) for r in csv.DictReader(open(os.path.join(st, "new.csv"), newline="", encoding="utf-8-sig"))] if os.path.exists(os.path.join(st, "new.csv")) else []
    fixes = [dict(r) for r in csv.DictReader(open(os.path.join(st, "fixes.csv"), newline="", encoding="utf-8-sig"))] if os.path.exists(os.path.join(st, "fixes.csv")) else []
    drops = [dict(r) for r in csv.DictReader(open(os.path.join(st, "drops.csv"), newline="", encoding="utf-8-sig"))] if os.path.exists(os.path.join(st, "drops.csv")) else []
    ramps_new = jload(os.path.join(st, "ramps.json"), {})
    shifts = jload(os.path.join(st, "shifts.json"), [])
    errors, plan = [], []
    seen = set()
    for r in new:
        r = {c: (r.get(c) or "").strip() for c in E.COLS}
        p = check_row(r)
        if r["project_id"] in existing:
            p.append("id already in the registry (use fixes.csv)")
        if r["project_id"] in seen:
            p.append("duplicate id in new.csv")
        seen.add(r["project_id"])
        tk = toks(r["campus"]) | toks(r["developer"])
        for q in existing.values():
            if q["state"] == r["state"] and (E.norm_place(q["city"]) == E.norm_place(r["city"]) or (q["county"] and E.norm_place(q["county"]) == E.norm_place(r["county"]))):
                qt = toks(q["campus"]) | toks(q["developer"])
                if tk and qt and len(tk & qt) / min(len(tk), len(qt)) >= 0.5:
                    plan.append(f"  ⚠ {r['project_id']}: possible duplicate of {q['project_id']} ({q['phase']}, {q['cod_base']}, {q['mw']} {q['mw_basis']}) — confirm in notes")
                    break
        (errors if p else plan).append(f"  {'✗' if p else '+'} NEW {r['project_id']} {r['mw']} {r['mw_basis']} cod {r['cod_base']} {r['phase_status']}" + (f" !! {'; '.join(p)}" if p else ""))
    for r in fixes:
        r = {c: (r.get(c) or "").strip() for c in E.COLS}
        p = check_row(r)
        o = existing.get(r["project_id"])
        if not o:
            p.append("not an existing id")
        if not r["notes"].startswith(f"MONITOR {a.date}:"):
            p.append(f"notes must start 'MONITOR {a.date}: <what changed, old → new, source>'")
        diff = [f"{c} {o.get(c)!r}→{r[c]!r}" for c in E.COLS if o and c not in ("notes", "source", "source_date") and (o.get(c) or "") != r[c]] if o else []
        (errors if p else plan).append(f"  {'✗' if p else '~'} FIX {r['project_id']}: {'; '.join(diff) or 'no key-field change'}" + (f" !! {'; '.join(p)}" if p else ""))
    for d in drops:
        if d.get("project_id") not in existing:
            errors.append(f"  ✗ DROP {d.get('project_id')}: not an existing id")
        elif not d.get("why"):
            errors.append(f"  ✗ DROP {d.get('project_id')}: needs a why")
        else:
            plan.append(f"  - DROP {d['project_id']}: {d['why']}")
    rj = jload(os.path.join(DATA, "ramps.json"), {})
    ids_after = (set(existing) | {r["project_id"] for r in new}) - {d.get("project_id") for d in drops}
    for k, v in ramps_new.items():
        if k.startswith("_"):
            continue
        p = []
        if k not in ids_after:
            p.append("ramp id not in the registry")
        if not v.get("dates") or any(E.m_parse(x) is None for x in v["dates"]):
            p.append("bad dates")
        if not v.get("why"):
            p.append("needs a why")
        if v.get("shares") and (len(v["shares"]) != len(v["dates"]) or abs(sum(v["shares"]) - 1) > 1e-6):
            p.append("shares must match dates and sum to 1")
        (errors if p else plan).append(f"  {'✗' if p else '≈'} RAMP {k}: {v.get('dates')}" + (" (replaces the current spec)" if k in rj else "") + (f" !! {'; '.join(p)}" if p else ""))
    adj = jload(os.path.join(DATA, "adjustments.json"), {"date_shift": [], "set_fields": []})
    have = {x["prefix"] for x in adj.get("date_shift", [])}
    auto = [{"prefix": r["project_id"], "months": 6, "why": f"TDLR construction-completion date -> energization (+6m, Epoch AI convention); monitor {a.date}"}
            for r in new if (r.get("notes") or "").startswith("TDLR completion") and r["project_id"] not in ramps_new
            and r.get("phase_status") != "energized" and not any(r["project_id"].startswith(h) for h in have)]
    covered = have | {s.get("prefix", "") for s in shifts + auto}
    for r in fixes:
        pid = r.get("project_id", "")
        if "TDLR" in (r.get("notes") or "").split("|")[0] and pid not in ramps_new and pid not in rj \
                and not any(pid.startswith(h) for h in covered if h):
            plan.append(f"  ⚠ {pid}: re-dated from TDLR but no +6m date_shift covers it — add it to shifts.json, or the date stays at construction completion")
    for s in shifts + auto:
        if not s.get("prefix") or not isinstance(s.get("months"), int) or not s.get("why"):
            errors.append(f"  ✗ SHIFT {s}: needs prefix, integer months, why")
        else:
            plan.append(f"  » SHIFT {s['prefix']} {s['months']:+d}m — {s['why'][:90]}")
    print(f"apply {a.date}: {len(new)} new · {len(fixes)} fixes · {len(drops)} drops · {len([k for k in ramps_new if not k.startswith('_')])} ramps · {len(shifts) + len(auto)} shifts")
    print("\n".join(plan + errors) or "  (nothing staged)")
    if errors:
        print(f"{len(errors)} problem(s) — nothing written")
        return 2
    if not a.write:
        print("dry run — re-run with --write to merge")
        return 0
    applied = {"date": a.date, "fixed_old": {}, "dropped_old": {}, "ramps_old": {}}
    if new:
        mp = os.path.join(DATA, "raw", "monitor.csv")
        cur = [dict(r) for r in csv.DictReader(open(mp, newline="", encoding="utf-8-sig"))] if os.path.exists(mp) else []
        write_csv(mp, cur + [{c: (r.get(c) or "").strip() for c in E.COLS} for r in new])
    ovp = os.path.join(DATA, "overrides.csv")
    ov = [dict(r) for r in csv.DictReader(open(ovp, newline="", encoding="utf-8-sig"))] if os.path.exists(ovp) else []
    fix_ids = {r["project_id"] for r in fixes}
    drop_ids = {d["project_id"] for d in drops}
    for pid in fix_ids | drop_ids:
        o = existing[pid]
        (applied["fixed_old"] if pid in fix_ids else applied["dropped_old"])[pid] = {c: o.get(c, "") for c in E.COLS} | {"_file": o.get("_file")}
    keep = [r for r in ov if not (r["project_id"] in fix_ids and r.get("phase") != "DROP") and not (r["project_id"] in drop_ids and r.get("phase") != "DROP")]
    drop_rows = [dict({c: existing[d["project_id"]].get(c, "") for c in E.COLS}, phase="DROP", notes=f"DROP MONITOR {a.date}: {d['why']}") for d in drops]
    write_csv(ovp, keep + [{c: (r.get(c) or "").strip() for c in E.COLS} for r in fixes] + drop_rows)
    if ramps_new:
        hist = rj.setdefault("_history", {})
        for k, v in ramps_new.items():
            if k.startswith("_"):
                continue
            if k in rj:
                applied["ramps_old"][k] = rj[k]
                hist.setdefault(k, []).append({"replaced": a.date, "old": rj[k]})
            rj[k] = v
        jsave(os.path.join(DATA, "ramps.json"), rj)
    if shifts or auto:
        adj.setdefault("date_shift", []).extend(shifts + auto)
        jsave(os.path.join(DATA, "adjustments.json"), adj)
    jsave(os.path.join(run, "applied.json"), applied)
    print("merged. Next: py build_dc_delay.py (then --checkpoint at the end of the run)")
    return 0


# ----------------------------------------------------------------------------- rules / locals
def parse_val(s: str):
    if s in ("true", "false"):
        return s == "true"
    if s == "null":
        return None
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return float(s) if "." in s else int(s)
    return s


def rules_write(obj: dict, raw: str, path: str) -> None:
    out = json.dumps(obj, indent=1, ensure_ascii=False)
    if "\r\n" in raw:
        out = out.replace("\n", "\r\n") + ("\r\n" if raw.endswith("\r\n") else "")
    elif raw.endswith("\n"):
        out += "\n"
    with open(path, "wb") as fh:
        fh.write(out.encode("utf-8"))


def cmd_rules(a) -> int:
    path = os.path.join(DATA, "local_moratoria.json" if a.locals else "state_rules.json")
    raw = open(path, "rb").read().decode("utf-8")
    r = json.loads(raw)
    items = r["moratoria"] if a.locals else r["instruments"]
    if a.as_of and not a.locals:
        print(f"as_of {r.get('as_of')} → {a.as_of}")
        r["as_of"] = a.as_of
    if a.id:
        ins = next((x for x in items if x["id"] == a.id), None)
        if not ins:
            print("no entry", a.id, "— ids:", [x["id"] for x in items][:120])
            return 1
        if not a.source or not a.why:
            print("--source and --why are required for an instrument change")
            return 1
        for kv in a.set or []:
            k, v = kv.split("=", 1)
            node, keys = ins, k.split(".")
            for kk in keys[:-1]:
                node = node.setdefault(kk, {})
            old, new = node.get(keys[-1]), parse_val(v)
            node[keys[-1]] = new
            ins.setdefault("history", []).append({"date": TODAY.isoformat(), "field": k, "old": old, "new": new, "source": a.source, "why": a.why})
            print(f"{a.id}.{k}: {old!r} → {new!r}")
        ins["source"] = (ins.get("source", "") + f" ; {a.source} ({TODAY.isoformat()})").strip(" ;")
    if a.write:
        rules_write(r, raw, path)
        print("written", path)
    else:
        print("dry run — add --write")
    return 0


def cmd_add_local(a) -> int:
    snap = jload(os.path.join(SNAP, "moratoria.json"), {}).get("records", {})
    v = snap.get(a.moratorium_id)
    if not v:
        print("not in the moratoria snapshot — run `poll --only moratoria` first, or check the id")
        return 1
    path = os.path.join(DATA, "local_moratoria.json")
    doc = jload(path, None)
    if any(f"record {a.moratorium_id}" in (m.get("source") or "") for m in doc["moratoria"]):
        print("already in local_moratoria.json")
        return 1
    st = v["st"]
    start = (v["enacted"] or "")[:7]
    if not start:
        print("record has no enactment date — add it by hand")
        return 1
    if v["end"]:
        end = v["end"][:7]
        tag = "end HARD (tracker end date)"
    else:
        months = float(v["days"]) / 30.44 if v.get("days") else doc["avg_local_duration_months"].get(st, 9.0)
        end = E.m_fmt(E.m_parse(start) + round(months))
        tag = "end PARTIAL (duration or state average)"
    dur = E.m_parse(end) - E.m_parse(start)
    n = 1 + max([int(m["id"].split("-")[-1]) for m in doc["moratoria"] if m["id"].startswith(f"LOC-{st}-") and m["id"].split("-")[-1].isdigit()] or [-1])
    active = v["status"] in ("active", "extended")
    entry = {"id": f"LOC-{st}-{n:03d}", "jurisdiction": v["jur"], "county": v["jur"] if v["type"] in ("County", "Parish") else "",
             "state": st, "level": "county" if v["type"] in ("County", "Parish") else "city",
             "type": f"moratorium ({v['type'].lower()})", "scope": "Added by the weekly monitor from the Moratorium Nation record; scope per the tracker.",
             "blocks": "new_license", "ban": False, "start": start,
             "end": {"base": end, "bear": end, "stress": E.m_fmt(E.m_parse(end) + max(dur, 1))},
             "duration_months": round(dur, 1), "status": "in_force" if active else v["status"],
             "active": {"base": active, "bear": active, "stress": active},
             "lat": float(v["lat"]) if v.get("lat") else None, "lon": float(v["lon"]) if v.get("lon") else None, "tag": tag,
             "source": f"Moratorium Nation local inventory (Michael J. Bommarito, CC-BY-4.0), https://mjbommar.github.io/moratorium-data-2026/data/moratorium_inventory.csv, monitor {TODAY.isoformat()}; record {a.moratorium_id}",
             "source_date": TODAY.isoformat()}
    print(json.dumps(entry, ensure_ascii=False, indent=1))
    if a.write:
        doc["moratoria"].append(entry)
        raw = open(path, "rb").read().decode("utf-8")
        rules_write(doc, raw, path)
        print("appended to", path)
    else:
        print("dry run — add --write")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("poll")
    p.add_argument("--since")
    p.add_argument("--only")
    p.add_argument("--no-save", action="store_true")
    p = sp.add_parser("apply")
    p.add_argument("--date", default=TODAY.isoformat())
    p.add_argument("--write", action="store_true")
    p = sp.add_parser("rules")
    p.add_argument("--id")
    p.add_argument("--set", action="append")
    p.add_argument("--source")
    p.add_argument("--why")
    p.add_argument("--as-of", dest="as_of")
    p.add_argument("--locals", action="store_true", help="edit a local_moratoria.json entry (LOC-..) instead of a state instrument")
    p.add_argument("--write", action="store_true")
    p = sp.add_parser("add-local")
    p.add_argument("moratorium_id")
    p.add_argument("--write", action="store_true")
    a = ap.parse_args()
    return {"poll": cmd_poll, "apply": cmd_apply, "rules": cmd_rules, "add-local": cmd_add_local}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
