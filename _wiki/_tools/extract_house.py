r"""
FEATURE 6 — Numbers as structured data (house model layer).

Scrapes the "## Capstone estimates (house model)" table out of each company page
into _data/house.json so the house view becomes machine-queryable (and feeds the
edge tracker). Consensus already lives structured in _data/estimates.json; this
adds the *house* side so the two can be diffed.

Read-only on pages. Writes only _data/house.json.

    py "E:/Wiki Felipe empresas/_wiki/_tools/extract_house.py"
"""
import sys, json, re
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import company_pages, read, section, parse_md_table, num, DATA, TODAY
sys.stdout.reconfigure(encoding="utf-8")

YEAR_RE = re.compile(r"(20\d\d)|(?:FY|CY)?\s?'?(\d\d)\b")


def to_year(tok):
    """'2026E' / 'CY27' / \"'27\" / 'FY26' -> 2026 (int) or None."""
    t = tok.strip().replace("&nbsp;", " ")
    m = re.search(r"20\d\d", t)
    if m:
        return int(m.group(0))
    m = re.search(r"'?(\d\d)E?\b", t)  # E? so 'CY26E' / 'CY27E' parse, not just 'CY24'
    if m:
        return 2000 + int(m.group(1))
    return None


def row_label(cells):
    return cells[0].replace("&nbsp;", " ").replace("*", "").strip(" —-–").lower()


def main():
    out = {}
    for tk, pf in company_pages():
        md = read(pf)
        # accept "Capstone estimates", "House model", "House estimates"
        body = section(md, r"(Capstone estimates|House (model|estimates))")
        if not body:
            continue
        header, rows = parse_md_table(body)
        if not header or not rows:
            continue
        # map data columns -> year
        cols = []  # (col_index, year)
        for i, h in enumerate(header):
            if i == 0:
                continue
            y = to_year(h)
            if y:
                cols.append((i, y))
        if not cols:
            continue
        years = {}
        for ci, y in cols:
            years.setdefault(str(y), {})
        # pull canonical metrics
        for cells in rows:
            if len(cells) < 2:
                continue
            lbl = row_label(cells)
            key = None
            if lbl.startswith("revenue") and "/" not in lbl:
                key = "rev"
            elif lbl.startswith("eps"):
                key = "eps"
            elif lbl.startswith("gross margin") or lbl == "gm":
                key = "gm"
            elif "op margin" in lbl or lbl.startswith("operating margin"):
                key = "opm"
            elif "free cash flow" in lbl or lbl.startswith("fcf"):
                key = "fcf"
            if not key:
                continue
            for ci, y in cols:
                if ci < len(cells):
                    v = num(cells[ci])
                    if v is not None:
                        years[str(y)][key] = v
        years = {y: d for y, d in years.items() if d}
        if not years:
            continue
        # source note (the italic byline under the heading, if any)
        src = ""
        m = re.search(r"_Source:\s*(.*?)_", body)
        if m:
            src = m.group(1).strip()
        out[tk] = {"years": years, "raw_header": header,
                   "raw_rows": [c for c in rows], "source": src}

    DATA.mkdir(parents=True, exist_ok=True)
    payload = {"asof": TODAY.isoformat(),
               "note": "House (Capstone) model figures scraped from each page's "
                       "'Capstone estimates (house model)' table. rev/fcf in the page's "
                       "stated unit (usually $bn); eps absolute; gm/opm in %.",
               "companies": out}
    (DATA / "house.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    ncov = sum(1 for c in out.values() if c["years"])
    print(f"house.json written: {len(out)} pages with a house table ({ncov} with parsed metrics) -> {DATA/'house.json'}")
    # quick visibility
    for tk in sorted(out):
        ys = out[tk]["years"]
        print(f"  {tk:6} " + " · ".join(f"{y}:" + ",".join(f"{k}={v}" for k, v in sorted(d.items())) for y, d in sorted(ys.items())))


if __name__ == "__main__":
    main()
