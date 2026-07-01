r"""
FEATURE 9 — Book exposure map: positions × unresolved debates × catalysts.

The wiki knows theses; the comp-sheet knows positions. This joins them: for
every name in _data/book.json (hand-maintained — seed from the Core Positions
sheet) it pulls the page's one-line thesis, the house-vs-consensus divergence
(house.json vs estimates.json), the next dated catalyst, any past-due catalyst
without a post-mortem, and staleness flags. Answers the question none of the
other dashboards do: "where is the book most exposed to a debate we haven't
resolved?" Also lists big divergences on names NOT in the book (candidates).

Writes _meta/book.md + _dashboards/book.html. Read-only on pages.
Run AFTER build_catalysts.py and extract_house.py (refresh_features.py orders this).

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_book.py"
"""
import sys, json, re, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import (WIKI, META, DATA, DASH, read, load_estimates,
                   parse_md_table, html_head, TODAY, changelog_entries)
sys.stdout.reconfigure(encoding="utf-8")

FLAG = 10.0   # |Δ%| house-vs-cons to surface on the book page (looser than edge.md's 15)


def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def index_theses():
    """ticker -> one-line thesis from 00_INDEX.md tables."""
    out = {}
    md = read(WIKI / "00_INDEX.md")
    for m in re.finditer(r"^\|\s*(\w[\w.]*)\s*\|\s*\[[^\]]+\]\([^)]+\)\s*\|\s*(.+?)\s*\|\s*$",
                         md, re.M):
        out[m.group(1).upper()] = m.group(2)
    return out


def catalysts_by_ticker():
    """From _meta/catalysts.md: ticker -> (next_upcoming, past_due_count)."""
    upcoming, pastdue = {}, {}
    md = read(META / "catalysts.md")
    m = re.search(r"##\s*📅 Upcoming.*?(?=\n##\s)", md, re.S)
    if m:
        _, rows = parse_md_table(m.group(0))
        for cells in rows:
            if len(cells) >= 3 and cells[1] not in upcoming:   # table is date-sorted
                upcoming[cells[1]] = (cells[0], re.sub(r"\*\*", "", cells[2])[:120])
    m = re.search(r"##\s*⏰ Passed.*?(?=\n##\s)", md, re.S)
    if m:
        _, rows = parse_md_table(m.group(0))
        for cells in rows:
            if len(cells) >= 3:
                pastdue[cells[1]] = pastdue.get(cells[1], 0) + 1
    return upcoming, pastdue


def staleness_flags():
    """ticker -> set of flags from _meta/staleness.md."""
    flags = {}
    p = META / "staleness.md"
    if not p.is_file():
        return flags
    md = read(p)
    for label, key in [("BBG estimates missing", "no-BBG"), ("No transcripts", "no-transcripts")]:
        m = re.search(rf"##[^\n]*{label}[^\n]*\n+([^\n#]+)", md, re.I)
        if m:
            for tk in re.split(r"[,\s]+", m.group(1).strip()):
                if tk:
                    flags.setdefault(tk.upper(), set()).add(key)
    return flags


def divergences():
    """(ticker, year) -> {'eps': Δ%, 'rev': Δ%} house vs consensus (USD names)."""
    try:
        house = json.loads((DATA / "house.json").read_text(encoding="utf-8")).get("companies", {})
    except Exception:
        house = {}
    est = load_estimates().get("companies", {})
    out = {}
    for tk, h in house.items():
        c = est.get(tk) or {}
        if c.get("ccy", "USD") != "USD" or "error" in c:
            continue
        per = c.get("periods") or {}
        for y, cyk in (("2026", "CY2026"), ("2027", "CY2027")):
            hy = (h.get("years") or {}).get(y)
            cp = per.get(cyk) or {}
            if not hy:
                continue
            d = {}
            de = pct(hy.get("eps"), cp.get("eps"))
            if de is not None:
                d["eps"] = de
            dr = pct(hy.get("rev"), (cp.get("rev") / 1000.0) if cp.get("rev") else None)
            if dr is not None:
                d["rev"] = dr
            if d:
                out[(tk, y)] = d
    return out


def biggest_div(tk, divs):
    """Largest |Δ| across years/metrics for a ticker -> (label, Δ) or (None, None)."""
    best = (None, None)
    for (t, y), d in divs.items():
        if t != tk:
            continue
        for metric, v in d.items():
            if best[1] is None or abs(v) > abs(best[1]):
                best = (f"{metric.upper()} {y}", v)
    return best


def fmt_d(d):
    if d is None:
        return ""
    return f'<span class="{"pos" if d > 0 else "neg"}">{d:+.0f}%</span>'


def main():
    book = json.loads((DATA / "book.json").read_text(encoding="utf-8"))
    positions = book.get("positions", [])
    theses = index_theses()
    upcoming, pastdue = catalysts_by_ticker()
    stale = staleness_flags()
    divs = divergences()
    seed = book.get("seed")

    rows = []
    for p in positions:
        tk = p["tk"].upper()
        page = WIKI / f"{tk}.md"
        last_chg = ""
        if page.is_file():
            dates = [d for d, _ in changelog_entries(read(page))]
            last_chg = max(dates) if dates else ""
        dlabel, dval = biggest_div(tk, divs)
        nxt = upcoming.get(tk)
        rows.append({
            "tk": tk, "side": p.get("side", "long"), "weight": p.get("weight"),
            "note": p.get("note", ""), "thesis": theses.get(tk, "_no page_"),
            "div_label": dlabel, "div": dval,
            "next_cat": nxt[0] if nxt else "", "next_cat_txt": nxt[1] if nxt else "",
            "pastdue": pastdue.get(tk, 0), "flags": sorted(stale.get(tk, [])),
            "last_chg": last_chg, "has_house": dlabel is not None or
                        (tk in json.loads((DATA / "house.json").read_text(encoding="utf-8")).get("companies", {})),
        })
    # sort: biggest unresolved divergence first, then nearest catalyst
    rows.sort(key=lambda r: (-(abs(r["div"]) if r["div"] is not None else 0),
                             r["next_cat"] or "9999"))

    in_book = {r["tk"] for r in rows}
    candidates = []
    for (tk, y), d in sorted(divs.items(), key=lambda kv: -max(abs(v) for v in kv[1].values())):
        if tk in in_book:
            continue
        for metric, v in d.items():
            if abs(v) >= FLAG:
                candidates.append({"tk": tk, "label": f"{metric.upper()} {y}", "d": v})
    # dedupe to biggest per ticker
    seen, cand = set(), []
    for c in candidates:
        if c["tk"] not in seen:
            seen.add(c["tk"]); cand.append(c)

    # ---------- markdown ----------
    md = [f"# Book — positions × unresolved debates × catalysts\n",
          f"_Generated {TODAY.isoformat()} from `_data/book.json` (asof {book.get('asof','?')}). "
          f"Rebuild: `py _wiki/_tools/build_book.py`._\n"]
    if seed:
        md.append("> ⚠️ **SEED book** — initialized from the 8 house-model names, weights unknown. "
                  "Edit `_data/book.json` to match the real Core Positions (weights, adds/drops), "
                  "then remove the `\"seed\": true` flag.\n")
    md.append("| Ticker | Side | Wt % | House vs cons | Next catalyst | ⏰ due | Flags | Last chg | Thesis |")
    md.append("|---|---|--:|---|---|--:|---|---|---|")
    for r in rows:
        w = f"{r['weight']:.1f}" if r["weight"] is not None else "?"
        dv = f"{r['div_label']} {r['div']:+.0f}%" if r["div"] is not None else ("—" if r["has_house"] else "no house model")
        nc = f"{r['next_cat']} — {r['next_cat_txt']}" if r["next_cat"] else "_none dated_"
        fl = " ".join(r["flags"]) or ""
        md.append(f"| {r['tk']} | {r['side']} | {w} | {dv} | {nc} | {r['pastdue'] or ''} | {fl} | {r['last_chg']} | {r['thesis'][:110]} |")
    md.append(f"\n## Not in book — house-vs-consensus divergence ≥ {FLAG:.0f}% (candidates)\n")
    md.append("| Ticker | Metric | Δ | Thesis |")
    md.append("|---|---|--:|---|")
    for c in cand:
        md.append(f"| {c['tk']} | {c['label']} | {c['d']:+.0f}% | {theses.get(c['tk'], '')[:110]} |")
    if not cand:
        md.append("| _none_ | | | |")
    META.mkdir(parents=True, exist_ok=True)
    (META / "book.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- html ----------
    head, foot = html_head("Book — positions × debates × catalysts",
                           f"{TODAY.isoformat()} · where is the book most exposed to a debate we haven't resolved?")
    h = [head]
    if seed:
        h.append("<p style='background:#fff3cd;padding:10px 14px;border-radius:6px'>⚠️ <b>SEED book</b> — "
                 "8 house-model names, weights unknown. Edit <code>_data/book.json</code> to match the real "
                 "Core Positions, then drop the <code>seed</code> flag.</p>")
    h.append("<h2>Positions</h2>")
    h.append("<table class='sortable'><thead><tr><th>Ticker</th><th>Side</th><th class='r'>Wt %</th>"
             "<th>House vs cons</th><th>Next catalyst</th><th class='r'>⏰ due</th><th>Flags</th>"
             "<th>Last chg</th><th>Thesis</th></tr></thead><tbody>")
    for r in rows:
        w = f"{r['weight']:.1f}" if r["weight"] is not None else "?"
        dv = (f"{r['div_label']} {fmt_d(r['div'])}" if r["div"] is not None
              else ("—" if r["has_house"] else "<span class='mut'>no house model</span>"))
        nc = (f"<b>{r['next_cat']}</b> {html.escape(r['next_cat_txt'])}" if r["next_cat"]
              else "<span class='mut'>none dated</span>")
        due = f"<span class='pill due'>{r['pastdue']}</span>" if r["pastdue"] else ""
        fl = " ".join(f"<span class='pill dn'>{f}</span>" for f in r["flags"])
        h.append(f"<tr><td class='tk'>{r['tk']}</td><td>{r['side']}</td>"
                 f"<td class='r' data-v='{r['weight'] if r['weight'] is not None else -999}'>{w}</td>"
                 f"<td data-v='{abs(r['div']) if r['div'] is not None else -1:.2f}'>{dv}</td>"
                 f"<td>{nc}</td><td class='r' data-v='{r['pastdue']}'>{due}</td><td>{fl}</td>"
                 f"<td>{r['last_chg']}</td><td>{html.escape(r['thesis'][:140])}</td></tr>")
    h.append("</tbody></table>")
    h.append(f"<h2>Not in book — divergence ≥ {FLAG:.0f}% (candidates)</h2>")
    h.append("<table class='sortable'><thead><tr><th>Ticker</th><th>Metric</th><th class='r'>Δ</th>"
             "<th>Thesis</th></tr></thead><tbody>")
    for c in cand:
        h.append(f"<tr><td class='tk'>{c['tk']}</td><td>{c['label']}</td>"
                 f"<td class='r' data-v='{c['d']:.2f}'>{fmt_d(c['d'])}</td>"
                 f"<td>{html.escape(theses.get(c['tk'], '')[:140])}</td></tr>")
    h.append("</tbody></table>")
    h.append(foot)
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "book.html").write_text("\n".join(h), encoding="utf-8")

    print(f"book: {len(rows)} positions ({'SEED — fill weights!' if seed else 'live'}), "
          f"{len(cand)} off-book candidates ≥{FLAG:.0f}%")
    print(f"  -> {META/'book.md'}")
    print(f"  -> {DASH/'book.html'}")


if __name__ == "__main__":
    main()
