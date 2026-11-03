"""Monthly exchange-volume feed for the Financials exchanges dashboard (fin-exchanges.html).

Public sources, stdlib urllib through the TLS proxy (unverified SSL context, as the other fetchers):
  OCC   marketdata.theocc.com/exchange-volume (market view, monthly, options): US listed-options
        contracts cleared and share by exchange, grouped into Cboe / Nasdaq / ICE (NYSE) / MIAX / other
  Cboe  cdn.cboe.com .../<Month>-<YYYY>-Monthly-Volume-Statistics-Xlsx-.xlsx: ADV by segment, market
        share, rolling three-month revenue per contract (one-month lag), SPX / VIX / XSP ADV
  CME   PR Newswire monthly volume releases: total and asset-class ADV with y/y, BrokerTec / EBS
        notional, customer collateral balances (prose, parsed)
  ICE   s2.q4cdn.com monthly statistics PDFs: y/y % by asset class and open interest. ICE publishes
        levels only in an IR spreadsheet behind bot protection. Needs PyMuPDF (fitz); skipped without it.
  VIX   cdn.cboe.com VIX_History.csv / OVX_History.csv: monthly average of daily closes
Nasdaq's monthly data sheet and CME's IR volume pages refuse scripted requests (HTTP 403), so Nasdaq
is covered through its OCC options share and its quarterly results.

Writes _wiki/_data/financials/exchange_volumes.json   parsed series; every month carries its source URL
       _wiki/_data/financials/exchange_volumes_raw/    download cache (gitignored)
Usage  py fetch_exchange_volumes.py [--since 2023-01] [--refresh]
       Cached months are reused; the latest two months and the current-year OCC / Cboe files are
       always re-downloaded. --refresh re-downloads everything.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import io
import json
import re
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
OUT = WIKI / "_data" / "financials" / "exchange_volumes.json"
RAW = WIKI / "_data" / "financials" / "exchange_volumes_raw"

CTX = ssl._create_unverified_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/130 Safari/537.36"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
QUARTER_WORD = {3: "First", 6: "Second", 9: "Third", 12: "Fourth"}

# OCC exchange codes -> listed-options exchange groups
OCC_GROUPS = {
    "Cboe": ["CBOE", "C2", "BATS", "EDGX"],
    "Nasdaq": ["PHLX", "ISE", "GEM", "MCRY", "NSDQ", "NOBO"],
    "ICE (NYSE)": ["AMEX", "ARCA"],
    "MIAX": ["MIAX", "EMLD", "MPRL", "SPHR"],
    "MEMX": ["MEMX"],
    "BOX": ["BOX"],
}

WARN: list[str] = []


def fetch(url: str, refresh: bool, binary: bool = False):
    RAW.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("//", 1)[-1])[-90:]
    path = RAW / (hashlib.sha1(url.encode()).hexdigest()[:10] + "_" + name)
    if path.exists() and not refresh:
        data = path.read_bytes()
    else:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, context=CTX, timeout=45).read()
        path.write_bytes(data)
    return data if binary else data.decode("utf-8", "replace")


def exists(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        return urllib.request.urlopen(req, context=CTX, timeout=25).status == 200
    except Exception:
        return False


def html_text(h: str) -> str:
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?i)</(p|li|tr|h\d|div|table)>", "\n", h)
    h = re.sub(r"(?i)<(td|th)[^>]*>", " | ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("\xa0", " ")
    h = re.sub(r"[ \t]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n", h)


def month_iter(since: str, until: str):
    y, m = map(int, since.split("-"))
    uy, um = map(int, until.split("-"))
    while (y, m) <= (uy, um):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def is_recent(y: int, m: int, today: dt.date, n: int = 2) -> bool:
    return (today.year * 12 + today.month) - (y * 12 + m) <= n


# ---------------------------------------------------------------- OCC
def occ(since: str, today: dt.date, refresh: bool) -> dict:
    out = {"months": {}, "urls": {}, "groups": OCC_GROUPS}
    for year in range(int(since[:4]), today.year + 1):
        date = f"{year}1231" if year < today.year else today.strftime("%Y%m%d")
        url = ("https://marketdata.theocc.com/exchange-volume?reportView=market&reportType=M"
               f"&reportDate={date}&instrumentType=options&format=txt")
        try:
            txt = fetch(url, refresh or year == today.year)
        except Exception as e:
            WARN.append(f"OCC {year}: {e}")
            continue
        out["urls"][str(year)] = url
        lines = txt.splitlines()
        head = next((l for l in lines if l.startswith("Date")), "")
        codes = head.split()[1:]
        codes = [c for c in codes if c not in ("OCC", "Total")] + ["OCC Total"]
        for line in lines:
            mm = re.match(r"(\d\d)/(\d{4})\s", line)
            if not mm:
                continue
            nums = re.findall(r"([\d,]+)\s+([\d.]+)%", line)
            if len(nums) != len(codes):
                WARN.append(f"OCC {mm.group(2)}-{mm.group(1)}: {len(nums)} values for {len(codes)} columns")
                continue
            by = {c: [int(v.replace(",", "")), float(p)] for c, (v, p) in zip(codes, nums)}
            total = by.pop("OCC Total")[0]
            groups = {g: sum(by.get(c, [0])[0] for c in cs) for g, cs in OCC_GROUPS.items()}
            groups["Other"] = sum(v for c, (v, _) in by.items()
                                  if not any(c in cs for cs in OCC_GROUPS.values()))
            key = f"{mm.group(2)}-{mm.group(1)}"
            if key < since:
                continue
            out["months"][key] = {
                "total": total,
                "groups": {g: {"contracts": v, "share": round(100 * v / total, 2) if total else None}
                           for g, v in groups.items()},
                "by_exchange": by,
                "url": url,
            }
    return out


# ---------------------------------------------------------------- Cboe xlsx
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def xlsx_rows(data: bytes) -> dict[str, dict[int, dict[str, str]]]:
    z = zipfile.ZipFile(io.BytesIO(data))
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    sheets = {}
    for s in wb.find("m:sheets", NS):
        tgt = rels[s.get("{%s}id" % NS["r"])].lstrip("/")
        tgt = tgt if tgt.startswith("xl/") else "xl/" + tgt
        rows: dict[int, dict[str, str]] = {}
        for c in ET.fromstring(z.read(tgt)).iter("{%s}c" % NS["m"]):
            v = c.find("m:v", NS)
            if v is None:
                continue
            val = ss[int(v.text)] if c.get("t") == "s" else v.text
            col, row = re.match(r"([A-Z]+)(\d+)", c.get("r")).groups()
            rows.setdefault(int(row), {})[col] = val
        sheets[s.get("name")] = rows
    return sheets


# section header (lower-case prefix) -> section key
CBOE_SECTIONS = [("trading days", "days"), ("adv/adnv by business", "adv"),
                 ("market share by business", "share"), ("rolling three-month", "rpc"),
                 ("adv for select index", "index"), ("fx rates", None)]
# (section, label prefix) -> metric key
CBOE_METRICS = {
    ("days", "options, futures & u.s. equi"): "days_us",
    ("adv", "multiply-listed options"): "adv_multilist_k",
    ("adv", "index options"): "adv_index_k",
    ("adv", "total options"): "adv_options_k",
    ("adv", "futures - adv"): "adv_futures_k",
    ("adv", "u.s. equities - exchange"): "adv_us_eq_on_bn_sh",
    ("adv", "u.s. equities - off-exchange"): "adv_us_eq_off_mn_sh",
    ("adv", "european equities"): "adnv_eu_eq_bn_eur",
    ("adv", "global fx"): "adnv_fx_bn_usd",
    ("share", "multiply-listed options"): "share_multilist",
    ("share", "index options"): "share_index",
    ("share", "total options"): "share_options",
    ("share", "u.s. equities - exchange"): "share_us_eq_on",
    ("share", "european equities"): "share_eu_eq",
    ("rpc", "multiply-listed options"): "rpc_multilist",
    ("rpc", "index options"): "rpc_index",
    ("rpc", "total options"): "rpc_options",
    ("rpc", "futures - per contract"): "rpc_futures",
    ("rpc", "u.s. equities - exchange"): "capture_us_eq_on_per100",
    ("rpc", "global fx"): "capture_fx_per_mn",
    ("index", "spx options"): "adv_spx_k",
    ("index", "vix options"): "adv_vix_opt_k",
    ("index", "xsp options"): "adv_xsp_k",
    ("index", "vix futures"): "adv_vix_fut_k",
}


def parse_cboe_sheet(rows: dict[int, dict[str, str]]) -> dict[str, dict[str, float]]:
    # 2025+ files carry labels in column A; the 2024 file shifts the table to column D
    head, lab_col = None, "A"
    for r in sorted(rows):
        hit = next((c for c, v in rows[r].items() if (v or "").strip().lower() == "period"), None)
        if hit:
            head, lab_col = rows[r], hit
            break
    if not head:
        return {}
    cols = {}
    for col, lab in head.items():
        mm = re.match(r"([A-Za-z]{3})-(\d\d)$", (lab or "").strip())
        if mm:
            mo = [m[:3] for m in MONTHS].index(mm.group(1).title()) + 1
            cols[col] = f"20{mm.group(2)}-{mo:02d}"
    out: dict[str, dict[str, float]] = {}
    section = None
    for r in sorted(rows):
        lab = (rows[r].get(lab_col) or "").strip().lower()
        if not lab:
            continue
        hit = next((key for pre, key in CBOE_SECTIONS if lab.startswith(pre)), "keep")
        if hit != "keep":
            section = hit
            continue
        if lab.startswith("options - adv") or lab.startswith("options - per") or lab == "options":
            continue
        for (sec, pre), metric in CBOE_METRICS.items():
            if sec == section and lab.startswith(pre):
                for col, month in cols.items():
                    v = rows[r].get(col)
                    try:
                        out.setdefault(month, {})[metric] = float(v)
                    except (TypeError, ValueError):
                        pass
                break
    return out


def cboe(since: str, today: dt.date, refresh: bool) -> dict:
    out = {"months": {}, "files": {}}
    base = "https://cdn.cboe.com/resources/investor_relations/revenue_per_contract/"
    for year in range(int(since[:4]), today.year + 1):
        if year < today.year:
            cands = [(year, 12)]
        else:
            cands = [(year, m) for m in range(today.month, 0, -1)]
        for y, m in cands:
            url = f"{base}{MONTHS[m - 1]}-{y}-Monthly-Volume-Statistics-Xlsx-.xlsx"
            if y == today.year and not (RAW / "x").parent.exists():
                pass
            try:
                data = fetch(url, refresh or y == today.year, binary=True)
            except Exception:
                continue
            for name, rows in xlsx_rows(data).items():
                if not re.fullmatch(r"\d{4}", name.strip()):
                    continue
                for month, vals in parse_cboe_sheet(rows).items():
                    if month >= since and vals.get("adv_options_k"):
                        vals["url"] = url
                        out["months"][month] = vals
            out["files"][str(year)] = url
            break
        else:
            WARN.append(f"Cboe {year}: no monthly xlsx found")
    return out


# ---------------------------------------------------------------- CME (PR Newswire)
CME_ASSETS = ["Interest Rate", "Equity Index", "Energy", "Agricultural", "Foreign Exchange",
              "Metals", "Cryptocurrency", "International"]
NEG = ("decreased", "fell", "declined", "was down", "down", "dropped")


def to_m(num: str, unit: str | None) -> float:
    v = float(num.replace(",", ""))
    if unit and unit.lower() == "million":
        return v
    if unit and unit.lower() == "thousand":
        return v / 1000
    return v / 1e6 if v >= 1000 else v


def cme_sections(t: str) -> dict[str, str]:
    heads = list(re.finditer(r"([^\n]{0,80}?)(?:highlights|ADV)(?: across asset classes)?"
                             r"(?: compared to [^\n]{0,40}?)? includes?:?", t, re.I))
    sec: dict[str, str] = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(t)
        lead = h.group(1).lower()
        kind = ("quarterly" if "quarter" in lead or re.search(r"\bq\d\b", lead) else
                "monthly" if "month" in lead or any(m.lower() in lead for m in MONTHS) else
                "annual" if "annual" in lead or "year" in lead else "other")
        sec[kind] = sec.get(kind, "") + "\n" + t[h.end():end]
    return sec


def parse_cme(t: str) -> dict:
    # the lead sentence ("... today reported ...") carries the monthly headline; the bullets above
    # it lead with asset-class records, so they are skipped
    i = t.find("today report")
    lead = t[i:i + 420] if i >= 0 else t[:1500]
    rec: dict = {}
    mm = re.search(r"([\d.]+) million contracts", lead)
    if mm:
        rec["adv_m"] = float(mm.group(1))
        mp = re.search(r"\b(up|down|an increase of|a decrease of|increased|decreased|rose|fell)\s+(\d+(?:\.\d+)?)%", lead)
        if mp and mp.start() < mm.end() + 120:
            rec["yoy"] = float(mp.group(2)) * (-1 if mp.group(1) in NEG + ("a decrease of",) else 1)
    sec = cme_sections(t)
    body = sec.get("monthly") or ""
    assets = {}
    names = "|".join(CME_ASSETS)
    # releases print "Interest Rate ADV of …", "Record Metals ADV of …" or the name on its own line
    pat = (r"(?:^|\n)\s*(?:Record (?:(?:MONTHS|monthly|all-time) )?)?(ASSETS)\s+ADV (?:(increased|decreased|rose|fell|grew|declined|was up|was down) "
           r"(\d+(?:\.\d+)?)% (?:year-over-year )?to |(?:reached |hit |of )?)(?:an? )?(?:new )?(?:all-time )?"
           r"(?:record )?(?:of )?([\d.,]+) ?(million|thousand)? contracts")
    for m in re.finditer(pat.replace("ASSETS", names).replace("MONTHS", "|".join(MONTHS)), body, re.I):
        name, verb, pct, num, unit = m.groups()
        name = next(a for a in CME_ASSETS if a.lower() == name.lower())
        if name in assets:
            continue
        a = {"adv_m": round(to_m(num, unit), 4)}
        if pct:
            a["yoy"] = float(pct) * (-1 if verb.lower() in NEG else 1)
        assets[name] = a
    # "Additional … product highlights" lines give the asset-class growth without a level
    for m in re.finditer(r"(?:^|\n)\s*(ASSETS) ADV (increased|decreased|rose|fell) (\d+(?:\.\d+)?)%(?! (?:year-over-year )?to)"
                         .replace("ASSETS", names), body, re.I):
        name = next(a for a in CME_ASSETS if a.lower() == m.group(1).lower())
        if name in assets and assets[name].get("yoy") is None:
            assets[name]["yoy"] = float(m.group(3)) * (-1 if m.group(2).lower() in NEG else 1)
    rec["assets"] = assets
    m = re.search(r"BrokerTec overall average daily notional value \(ADNV\) (increased|decreased|rose|fell) "
                  r"(\d+)% to \$([\d.]+) (trillion|billion)", body)
    if m:
        rec["brokertec_adnv_bn"] = float(m.group(3)) * (1000 if m.group(4) == "trillion" else 1)
        rec["brokertec_yoy"] = float(m.group(2)) * (-1 if m.group(1) in NEG else 1)
    m = re.search(r"EBS Spot FX ADNV (increased|decreased|rose|fell) (\d+)% to \$([\d.]+) billion", body)
    if m:
        rec["ebs_adnv_bn"] = float(m.group(3))
        rec["ebs_yoy"] = float(m.group(2)) * (-1 if m.group(1) in NEG else 1)
    m = re.search(r"collateral balances[^\n]*?rolling 3-months ending (\w+ \d{4}) were \$([\d.]+) billion for cash "
                  r"collateral and \$([\d.]+) billion for non-cash", t)
    if m:
        rec["collateral"] = {"period_end": m.group(1), "cash_bn": float(m.group(2)),
                             "noncash_bn": float(m.group(3))}
    q = sec.get("quarterly")
    if q is not None:
        mq = re.search(r"(Q[1-4]) (?:ADV|with|of)[^.]{0,60}?([\d.]+) million contracts,?\s*(up|down)?\s*(\d+)?%?", lead)
        if mq:
            rec["quarter"] = {"label": mq.group(1), "adv_m": float(mq.group(2))}
            if mq.group(4):
                rec["quarter"]["yoy"] = float(mq.group(4)) * (-1 if mq.group(3) == "down" else 1)
    return rec


def cme(since: str, today: dt.date, refresh: bool) -> dict:
    out = {"months": {}, "listing": "https://www.prnewswire.com/news/cme-group/"}
    cards = []
    for page in range(1, 5):
        url = f"https://www.prnewswire.com/news/cme-group/?page={page}&pagesize=100"
        try:
            h = fetch(url, True)
        except Exception as e:
            WARN.append(f"CME listing page {page}: {e}")
            break
        for m in re.finditer(r'<a[^>]+href="(/news-releases/[^"]+-\d{9}\.html)"[^>]*>(.*?)</a>', h, re.S):
            txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
            md = re.match(r"(\w{3}) (\d{2}), (\d{4})", txt)
            if md:
                cards.append((dt.datetime.strptime(md.group(0), "%b %d, %Y").date(), txt, m.group(1)))
        if cards and min(c[0] for c in cards).isoformat()[:7] < since:
            break
    vol = re.compile(r"\bADV\b|Average Daily Volume|Monthly Volume|Volume (?:Hits|Sets)|Market Statistics", re.I)
    skip = re.compile(r"International|Daily Volume Record|Open Interest|Single Day|Single-Day|Spot\+|Complex|"
                      r"Futures Set|Futures Reach|Credit Futures", re.I)
    picked: dict[str, tuple] = {}
    for d, title, href in sorted(set(cards)):
        if d.day > 8 or not vol.search(title) or skip.search(title):
            continue
        y, m = (d.year, d.month - 1) if d.month > 1 else (d.year - 1, 12)
        key = f"{y}-{m:02d}"
        if key >= since and key not in picked:
            picked[key] = (d, title, "https://www.prnewswire.com" + href)
    for key, (d, title, url) in sorted(picked.items()):
        y, m = map(int, key.split("-"))
        try:
            h = fetch(url, refresh or is_recent(y, m, today))
        except Exception as e:
            WARN.append(f"CME {key}: {e}")
            continue
        body = re.search(r'(?is)<section[^>]*class="[^"]*release-body[^"]*"[^>]*>(.*?)</section>', h)
        t = html_text(body.group(1) if body else h)
        t = re.sub(r"\.release-content[^\n]*\n", "", t)
        # PR Newswire sometimes splits digits with spaces ("4 2 % to 20. 8 million")
        t = re.sub(r"(\d) (\d) ?%", r"\1\2%", t)
        t = re.sub(r"(\d)\. (\d)", r"\1.\2", t)
        rec = parse_cme(t)
        rec.update({"title": title.split(" ET ", 1)[-1][:160], "date": d.isoformat(), "url": url})
        tm = re.search(r"([\d.]+) Million Contracts", title, re.I)
        if tm and rec.get("adv_m") and abs(float(tm.group(1)) - rec["adv_m"]) > 0.05 and "Q" not in title[:0]:
            WARN.append(f"CME {key}: lead ADV {rec['adv_m']} vs title {tm.group(1)} — check")
        if MONTHS[m - 1] not in t[:2500] and "monthly" not in t[:2500].lower():
            WARN.append(f"CME {key}: release text does not name {MONTHS[m - 1]} — month assignment unverified")
        if not rec.get("adv_m"):
            WARN.append(f"CME {key}: headline ADV not parsed")
        out["months"][key] = rec
    # CME states y/y only when volume grew; otherwise compute it from the prior-year release
    # (Capstone arithmetic, flagged yoy_calc so the dashboard can mark it)
    ms = out["months"]
    for key, rec in ms.items():
        prev = ms.get(f"{int(key[:4]) - 1}{key[4:]}")
        if not prev:
            continue
        if rec.get("yoy") is None and rec.get("adv_m") and prev.get("adv_m"):
            rec["yoy"] = round(100 * (rec["adv_m"] / prev["adv_m"] - 1), 1)
            rec["yoy_calc"] = True
        for name, a in rec.get("assets", {}).items():
            pa = prev.get("assets", {}).get(name)
            if a.get("yoy") is None and pa and pa.get("adv_m"):
                a["yoy"] = round(100 * (a["adv_m"] / pa["adv_m"] - 1), 1)
                a["yoy_calc"] = True
    return out


# ---------------------------------------------------------------- ICE (q4cdn PDFs)
ICE_CANON = [
    (r"^energy$", "Energy"), (r"^oil$", "Oil"), (r"^brent$", "Brent"), (r"^wti\*?$", "WTI"),
    (r"^gasoil$", "Gasoil"), (r"^natural gas$", "Natural Gas"),
    (r"^north american (natural )?gas$", "North American Gas"),
    (r"^other crude (&|and) refined products$", "Other Crude & Refined"),
    (r"^ttf( gas)?$", "TTF Gas"), (r"^asia gas$", "Asia Gas"), (r"^agriculture & metals$", "Agriculture & Metals"),
    (r"^ags & metals$", "Agriculture & Metals"), (r"^sugar$", "Sugar"), (r"^cocoa$", "Cocoa"),
    (r"^coffee$", "Coffee"), (r"^cotton$", "Cotton"), (r"^financials?$", "Financials"),
    (r"^interest rates?$", "Interest Rates"), (r"^euribor$", "Euribor"), (r"^sonia$", "SONIA"),
    (r"^gilts?$", "Gilts"), (r"^equity indic(es|ies)$", "Equity Indices"), (r"^msci$", "MSCI"),
    (r"^nyse equity options$", "NYSE Equity Options"),
]


def ice_canon(name: str) -> str:
    n = re.sub(r"(?i)^(record\s+)?(total\s+)?", "", name.strip()).strip(" *").lower()
    n = re.sub(r"\s+20\d\d$", "", n)
    for pat, canon in ICE_CANON:
        if re.match(pat, n):
            return canon
    return name.strip()
def ice_candidates(y: int, m: int) -> list[str]:
    mn = MONTHS[m - 1]
    post = y + 1 if m == 12 else y
    c = [f"Intercontinental-Exchange-Reports-{mn}-{y}-Statistics-{post}.pdf",
         f"Intercontinental-Exchange-Reports-{mn}-Statistics-{post}.pdf"]
    if m in QUARTER_WORD:
        q = QUARTER_WORD[m]
        c += [f"Intercontinental-Exchange-Reports-{mn}-and-{q}-Quarter-{y}-Statistics-{post}.pdf",
              f"Intercontinental-Exchange-Reports-{mn}-and-{q}-Quarter-Statistics-{post}.pdf",
              f"Intercontinental-Exchange-Reports-{mn}-{q}-Quarter-and-Full-Year-{y}-Statistics-{post}.pdf",
              f"Intercontinental-Exchange-Reports-{mn}-and-Full-Year-{y}-Statistics-{post}.pdf"]
    return ["https://s2.q4cdn.com/154085107/files/doc_news/" + x for x in c]


def _signed(word: str | None, num: str | None) -> float | None:
    if not word:
        return None
    return 0.0 if word == "flat" else (-1 if word == "down" else 1) * float(num or 0)


def parse_ice(t: str) -> dict:
    # PDF ligatures come through as stray glyphs ("Reíned", "Coìee")
    t = re.sub(r"(?<=[a-z])í(?=[a-z])", "fi", t)
    t = re.sub(r"(?<=[a-z])ì(?=[a-z])", "ff", t).replace("�", "fi")
    start = re.search(r"(?i)\b(?:\w+ )?highlights include:?", t)
    body = t[start.end():] if start else t
    stop = re.search(r"(?i)(quarter|full year|full-year|annual|year) highlights include|About Intercontinental", body)
    body = body[:stop.start()] if stop else body
    lines, record = {}, []
    item = (r"(?m)^\s*(Record )?([A-Z][\w&.,*/ -]{1,60}?) (ADV|OI) (up|down|flat)\s*(\d+(?:\.\d+)?)?%?(?: y/y)?"
            r"(?:[;,]\s*(?:including [^;\n]*?;\s*)?OI (up|down|flat)\s*(\d+(?:\.\d+)?)?%?)?")
    for m in re.finditer(item, body):
        rec_flag, name, kind, w1, n1, w2, n2 = m.groups()
        name = re.sub(r"(?i)^(Total )?average daily volume \(ADV\)$", "Total", name.strip())
        name = re.sub(r"(?i)^(Total )?open interest \(OI\)$", "Total", name)
        if name != "Total":
            rec_flag = rec_flag or re.match(r"(?i)record\b", name)
            name = ice_canon(name)
        rec = lines.setdefault(name, {})
        if kind == "ADV":
            rec.setdefault("adv_yoy", _signed(w1, n1))
            if w2:
                rec.setdefault("oi_yoy", _signed(w2, n2))
        else:
            rec.setdefault("oi_yoy", _signed(w1, n1))
        if rec_flag:
            record.append(name)
    total = {}
    m = re.search(r"(?i)(record )?total average daily volume \(ADV\) (up|down|flat)\s*(\d+(?:\.\d+)?)?%", body)
    if m:
        total["adv_yoy"] = _signed(m.group(2).lower(), m.group(3))
        total["record"] = bool(m.group(1))
    m = re.search(r"(?i)open interest \(OI\) (up|down|flat)\s*(\d+(?:\.\d+)?)?%", body)
    if m:
        total["oi_yoy"] = _signed(m.group(1).lower(), m.group(2))
    lines.pop("Total", None)
    return {"total": total or None, "lines": lines, "records": record,
            "total_adv_disclosed": "adv_yoy" in total}


def ice(since: str, today: dt.date, refresh: bool) -> dict:
    out = {"months": {}}
    try:
        import fitz  # PyMuPDF, already used by the inbox ingest
    except ImportError:
        WARN.append("ICE skipped: PyMuPDF (fitz) not importable")
        return out
    last = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    for y, m in month_iter(since, f"{last[0]}-{last[1]:02d}"):
        key = f"{y}-{m:02d}"
        url = next((u for u in ice_candidates(y, m)
                    if (RAW / (hashlib.sha1(u.encode()).hexdigest()[:10] + "_" +
                               re.sub(r"[^A-Za-z0-9._-]+", "_", u.split("//", 1)[-1])[-90:])).exists()
                    or exists(u)), None)
        if not url:
            if not is_recent(y, m, today, 1):
                WARN.append(f"ICE {key}: no statistics PDF found")
            continue
        try:
            data = fetch(url, refresh, binary=True)
            doc = fitz.open(stream=data, filetype="pdf")
            t = "\n".join(p.get_text() for p in doc)
        except Exception as e:
            WARN.append(f"ICE {key}: {e}")
            continue
        rec = parse_ice(t)
        md = re.search(r"\b(20\d\d-\d\d-\d\d)\b", t[:600])
        rec.update({"url": url, "date": md.group(1) if md else None})
        if not rec.get("total"):
            WARN.append(f"ICE {key}: neither total ADV nor total OI parsed")
        elif not rec["total_adv_disclosed"]:
            WARN.append(f"ICE {key}: release gives total OI but no total ADV y/y (left blank, not inferred)")
        out["months"][key] = rec
    return out


# ---------------------------------------------------------------- VIX / OVX
def vol_index(since: str, refresh: bool) -> dict:
    out = {"months": {}, "urls": {}}
    for sym in ("VIX", "OVX"):
        url = f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{sym}_History.csv"
        try:
            txt = fetch(url, True)
        except Exception as e:
            WARN.append(f"{sym}: {e}")
            continue
        out["urls"][sym] = url
        acc: dict[str, list[float]] = {}
        for row in csv.DictReader(io.StringIO(txt)):
            d = row.get("DATE") or row.get("Date")
            c = row.get("CLOSE") or row.get(sym) or row.get("Close")
            if not d or not c:
                continue
            mo, dd, yy = d.split("/") if "/" in d else (d[5:7], d[8:10], d[:4])
            key = f"{yy}-{int(mo):02d}"
            if key >= since:
                acc.setdefault(key, []).append(float(c))
        for key, vals in acc.items():
            out["months"].setdefault(key, {})[sym.lower() + "_avg"] = round(sum(vals) / len(vals), 2)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2023-01")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    today = dt.date.today()
    data = {
        "built": dt.datetime.now().isoformat(timespec="seconds"),
        "since": a.since,
        "note": ("Monthly exchange statistics from public company releases and OCC. OCC counts cleared US "
                 "listed-options contracts (equity + index), so exchange-group shares are of OCC volume. "
                 "Cboe RPC is the company's rolling three-month average, reported with a one-month lag. "
                 "ICE monthly releases give y/y % only. Industry ADV = OCC monthly total / Cboe US trading "
                 "days (Capstone arithmetic)."),
        "occ": occ(a.since, today, a.refresh),
        "cboe": cboe(a.since, today, a.refresh),
        "cme": cme(a.since, today, a.refresh),
        "ice": ice(a.since, today, a.refresh),
        "vol": vol_index(a.since, a.refresh),
    }
    # a network failure must not wipe history: keep the previous block for any source that came back short
    if OUT.exists():
        prev = json.loads(OUT.read_text(encoding="utf-8"))
        for k in ("occ", "cboe", "cme", "ice", "vol"):
            old, new = len(prev.get(k, {}).get("months", {})), len(data[k]["months"])
            if old and new < old:
                data[k] = prev[k]
                WARN.append(f"{k}: fetch returned {new} months vs {old} on file; kept the previous data")
    data["warnings"] = WARN
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    for k in ("occ", "cboe", "cme", "ice", "vol"):
        ms = sorted(data[k]["months"])
        print(f"{k:5} {len(ms):3} months  {ms[0] if ms else '-'} .. {ms[-1] if ms else '-'}")
    for w in WARN:
        print("WARN", w)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
