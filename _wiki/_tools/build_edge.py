r"""
FEATURE 1 — Divergence / Edge tracker.

"Divergences are the alpha; agreement is noise." This promotes the per-ingest
Step-7 reconciliation work into one STANDING, ranked page that answers: across
every name, where does the HOUSE view diverge most from the STREET — and where
have the curated reconciliation runs already flagged an edge?

Three inputs, all already on disk:
  - _data/house.json      (house model, from extract_house.py)
  - _data/estimates.json  (BBG consensus)
  - _meta/reconciliation-*.md  (curated DIVERGES + live PT/spot pulls)

Writes _meta/edge.md + _dashboards/edge.html. Read-only on pages.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_edge.py"
"""
import sys, json, re, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import (WIKI, META, DATA, DASH, read, load_estimates,
                   parse_md_table, num, html_head, TODAY)
sys.stdout.reconfigure(encoding="utf-8")

FLAG = 15.0  # |Δ%| threshold to call something an edge


def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def programmatic_edges():
    """House vs consensus, USD names only (avoid FX/basis traps). Returns list of dicts."""
    house = json.loads((DATA / "house.json").read_text(encoding="utf-8")).get("companies", {})
    est = load_estimates().get("companies", {})
    rows = []
    YMAP = {"2026": "CY2026", "2027": "CY2027"}
    for tk, h in house.items():
        c = est.get(tk) or {}
        if c.get("ccy", "USD") != "USD" or "error" in c:
            continue
        per = c.get("periods") or {}
        for y, cyk in YMAP.items():
            hy = h["years"].get(y)
            cp = per.get(cyk) or {}
            if not hy:
                continue
            # EPS (cleanest, no basis risk)
            if hy.get("eps") is not None and cp.get("eps") is not None:
                d = pct(hy["eps"], cp["eps"])
                if d is not None and abs(d) >= FLAG:
                    rows.append({"tk": tk, "metric": "EPS", "year": y,
                                 "house": hy["eps"], "cons": cp["eps"], "d": d, "unit": ""})
            # Revenue (house $bn vs consensus $mn -> /1000); flag basis on big gaps
            if hy.get("rev") is not None and cp.get("rev") is not None:
                cons_bn = cp["rev"] / 1000.0
                d = pct(hy["rev"], cons_bn)
                if d is not None and abs(d) >= FLAG:
                    rows.append({"tk": tk, "metric": "Revenue $bn", "year": y,
                                 "house": hy["rev"], "cons": round(cons_bn, 1), "d": d, "unit": "bn"})
    rows.sort(key=lambda r: -abs(r["d"]))
    return rows


def latest_recon():
    # NB: sort by the DATE IN THE FILENAME, then mtime — never lexically.
    # A same-day suffixed report ("reconciliation-2026-08-27-runinbox.md") sorts
    # BEFORE the plain one lexically ('-' 0x2D < '.' 0x2E), so a plain sorted()[-1]
    # silently returns the OLDER report whenever a date has two files.
    files = list(META.glob("reconciliation-*.md"))
    if not files:
        return None

    def key(p):
        m = re.match(r"reconciliation-(\d{4})-(\d{2})-(\d{2})", p.name)
        d = (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (0, 0, 0)
        return (d, p.stat().st_mtime)

    return max(files, key=key)


def curated_diverges(rf):
    """Parse the 'DIVERGES' findings from the latest reconciliation file.

    Two report shapes exist in _meta and both must work:
      (a) NARRATIVE (every report since ~2026-07): each finding is its own
          '### N. <flag> TICKER — headline' sub-section followed by a per-finding
          baseline table (3-4 cols) and a '➜ **Action:**' line. The rows of those
          tables are BASELINES ("Bernstein (07-27)", "BBG consensus", "Delta"),
          NOT tickers — feeding them to the flat-table parser below yields
          nonsense rows like "Delta | +23.0%" and silently drops every finding
          after the first table. Parsed here from the headings instead.
      (b) FLAT TABLE (older reports): one wide table whose first column IS the
          ticker. Kept as a fallback when no '###' sub-sections are present.
    """
    md = read(rf)
    # isolate the DIVERGES section — match any header variant ("Where the new data DIVERGES",
    # "DIVERGES (the alpha)", "DIVERGES (potential alpha)", …) up to the next '##' or EOF.
    # NB: finditer, not search. A multi-pass day (two /run-inbox runs on the same date)
    # can leave TWO "## DIVERGES" sections in one report; re.search harvested only the
    # first and the later findings were invisible to edge.md and _dashboards/edge.html
    # (documented in reconciliation-2026-09-09.md). Concatenate every DIVERGES section.
    secs = [mm.group(0) for mm in
            re.finditer(r"##\s*[^\n]*DIVERGES[^\n]*.*?(?=\n##\s|\Z)", md, re.S | re.I)]
    if not secs:
        return []
    section = "\n".join(secs)

    # --- (a) narrative sub-sections ------------------------------------------------
    parts = re.split(r"\n###\s+", section)[1:]     # drop the text before the first '###'
    out = []
    for part in parts:
        head, _, body = part.partition("\n")
        # A later /wiki-consensus run can RESOLVE a finding and move it to CONFIRMS while
        # leaving the sub-section in place, so the report keeps its history. Such a heading
        # is tagged "RESOLVED <date> -> CONFIRMS": it is no longer an open divergence and
        # must not be listed as one, nor have its retired '➜ Action' line quoted here.
        # NB: match the HEADING only. Findings that were resolved but STAYED in DIVERGES
        # carry a "✅ … resolution" block in the BODY and must be kept.
        if re.search(r"RESOLVED\b.*?(?:→|->)\s*CONFIRMS", head, re.I):
            continue
        # strip leading numbering ("1.", "①") and severity flags (🔴 🟡 🟢 ★ ⚠️ ✅)
        h = re.sub(r"^\s*(?:\d+\.|[①-⓿❶-❿])\s*", "", head.strip())
        flag = "".join(ch for ch in h if ch in "\U0001F534\U0001F7E1\U0001F7E2★")
        h = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿️\s]+", "", h)
        name, sep, tail = h.partition("—")          # em-dash separates name from headline
        if not sep:                                  # no em-dash: keep whole heading as the claim
            name, tail = "", h
        name = re.sub(r"\*\*", "", name).strip()
        # A heading whose first em-dash falls late ("THE HEADLINE: <one long sentence> — <clause>")
        # would otherwise put the whole headline in the Name column and leave the claim a fragment.
        if len(name) > 60:
            name, claim_override = "—", h
        else:
            claim_override = None
        name = name or "—"
        claim = re.sub(r"\*\*", "", claim_override if claim_override else tail).strip()
        # prefer the explicit '➜ Action:' line as the read; fall back to the headline
        a = re.search(r"[➜➤]\s*\*\*(.+?)\*\*", body, re.S)   # both arrowhead glyphs: reports use U+27A4, older ones U+279C
        read_txt = re.sub(r"\s+", " ", re.sub(r"\*\*", "", a.group(1))).strip() if a else claim
        if len(read_txt) > 400:
            read_txt = read_txt[:397] + "…"
        out.append({"name": (flag + " " + name).strip(), "new": claim, "read": read_txt})
    if out:
        return out

    # --- (b) legacy flat table -----------------------------------------------------
    header, rows = parse_md_table(section)
    for cells in rows:
        if len(cells) < 5:
            continue
        name = re.sub(r"\*\*|\s", "", cells[0])
        out.append({"name": name, "new": cells[1], "read": cells[-1]})
    return out


def pt_vs_spot(rf):
    r"""Consensus PT vs spot for the names the latest reconciliation discusses.

    Sourced from `estimates.json`'s `pt` block, NOT from a transcribed markdown table.
    This used to scrape a "## BBG consensus pull" heading, which silently returned ZERO
    rows the moment a report titled that section differently ("## Consensus reference -
    BBG pull, 2026-09-02" on 09-02) - and even when it matched, it re-read numbers a
    human had retyped into the report rather than the pull itself. Since 2026-09-03
    `fetch_estimates.py` writes consensus PT / high / low / rating / rec-counts per name,
    so the panel is taken from the data and the report is used only for SCOPE (which
    names to show) and for the hand-written 'Read' commentary when it can be found.

    Upside is PT/spot - 1. Both legs come from the same BBG listing and are therefore in
    the SAME currency, so this panel is safe for the five names whose trading currency
    differs from their fundamentals currency (TSM/SMIC/ASML/SPOT/TM) - the hazard there
    is px/eps, never PT/px. Dual-listed names resolve to whichever listing the fetch
    uses (ASML = the US ADR panel: 21 analysts, zero sells, structurally more bullish
    than Amsterdam's 42 incl. 2 sells). Never net the two panels.
    """
    est = load_estimates()
    comps = (est.get("companies") or {}) if isinstance(est, dict) else {}
    if not comps:
        return []
    md = read(rf) if rf else ""

    # --- scope: tickers the report deliberately NAMES ---------------------------
    # Only places where a ticker is named on purpose - wiki links, '###' headings and
    # the first cell of a table row. Prose is excluded on purpose: several covered
    # tickers are ordinary English words (ON, BE, NET, APP, ARM, TM, MP), and matching
    # those in running text pulls in names the report never discussed.
    def _tk_in(tk, text):
        return re.search(r"(?<![A-Za-z0-9])" + re.escape(tk) + r"(?![A-Za-z0-9])", text)

    named = set()
    for tk in comps:
        if re.search(r"\[\[" + re.escape(tk) + r"\]\]", md):
            named.add(tk)
    for line in md.splitlines():
        ls = line.strip()
        if ls.startswith("###"):
            for tk in comps:
                if _tk_in(tk, ls):
                    named.add(tk)
        elif ls.startswith("|") and ls.count("|") >= 2:
            first = re.sub(r"\*\*|\s|\\", "", ls.split("|")[1])
            for tk in comps:
                if _tk_in(tk, first):
                    named.add(tk)

    # --- the hand-written 'Read' note, if the report still carries such a table ---
    reads = {}
    m = re.search(r"##[^\n]*(?:BBG consensus pull|Consensus reference)[^\n]*.*?(?=\n##\s|\Z)",
                  md, re.S | re.I)
    if m:
        _hdr, rows = parse_md_table(m.group(0))
        for cells in rows:
            if len(cells) < 2:
                continue
            tk = re.sub(r"\*\*|\s|\\", "", cells[0]).split("(")[0]
            if tk in comps and len(cells[-1].strip()) > 12:
                reads[tk] = cells[-1].strip()

    out = []
    for tk in sorted(named):
        c = comps.get(tk) or {}
        ptb = c.get("pt")
        if not isinstance(ptb, dict):
            continue
        spot, conspt = c.get("px"), ptb.get("cons")
        up = pct(conspt, spot)
        if up is None:
            continue
        hi, lo = ptb.get("hi"), ptb.get("lo")
        rd = reads.get(tk)
        if not rd:
            bits = []
            if hi:
                bits.append(f"street high {hi:,.0f}")
            if lo and spot:
                # whether the street's OWN bear case is already in the money is the
                # single most useful unprompted read on a PT panel
                bits.append(f"low {lo:,.0f} " + ("ABOVE spot" if lo > spot else "below spot"))
            n, b, h_, sl = ptb.get("n"), ptb.get("buy"), ptb.get("hold"), ptb.get("sell")
            if n:
                bits.append(f"{int(b or 0)}/{int(h_ or 0)}/{int(sl or 0)} of {int(n)}")
            rd = " · ".join(bits)
        out.append({"tk": tk, "spot": spot, "conspt": conspt, "up": up, "read": rd})
    out.sort(key=lambda r: -abs(r["up"]))
    return out


def fmt_d(d):
    s = f"{d:+.0f}%"
    return f'<span class="{"pos" if d>0 else "neg"}">{s}</span>'


def main():
    prog = programmatic_edges()
    rf = latest_recon()
    diverges = curated_diverges(rf) if rf else []
    pts = pt_vs_spot(rf) if rf else []
    recon_name = rf.name if rf else "—"

    # ---------- markdown ----------
    md = [f"# Edge tracker — house vs Street\n",
          f"_Generated {TODAY.isoformat()} · the standing view of where our model and the "
          f"curated reconciliation runs disagree with consensus. Divergence = candidate alpha; "
          f"agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._\n",
          f"> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) "
          f"— **verify the basis before trading** (revenue gross/net/TAC differences can masquerade "
          f"as edge). Curated rows below are analyst-vetted.\n",
          f"## Programmatic — house vs consensus (|Δ| ≥ {FLAG:.0f}%)\n",
          "| Ticker | Metric | Yr | House | Consensus | Δ |",
          "|---|---|---|--:|--:|--:|"]
    for r in prog:
        md.append(f"| {r['tk']} | {r['metric']} | {r['year']} | {r['house']:,.2f} | "
                  f"{r['cons']:,.2f} | {r['d']:+.0f}% |")
    if not prog:
        md.append("| _none over threshold_ | | | | | |")

    md.append(f"\n## Curated divergences — latest reconciliation (`{recon_name}`)\n")
    md.append("| Name | New datapoint | Read (the edge) |")
    md.append("|---|---|---|")
    for d in diverges:
        md.append(f"| {d['name']} | {d['new']} | {d['read']} |")
    if not diverges:
        md.append("| _no reconciliation file_ | | |")

    md.append(f"\n## Consensus PT vs spot — live pull in `{recon_name}` (upside ranked)\n")
    md.append("| Ticker | Spot | Cons PT | Upside | Read |")
    md.append("|---|--:|--:|--:|---|")
    for r in pts:
        md.append(f"| {r['tk']} | {r['spot']:,.0f} | {r['conspt']:,.0f} | {r['up']:+.0f}% | {r['read']} |")
    if not pts:
        md.append("| _no live pull_ | | | | |")

    META.mkdir(parents=True, exist_ok=True)
    (META / "edge.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- html ----------
    head, foot = html_head("Edge tracker — house vs Street",
                           f"{TODAY.isoformat()} · divergence = candidate alpha")
    h = [head]
    h.append("<p class='byline'>⚠️ Programmatic rows auto-computed from "
             "<code>house.json</code> vs <code>estimates.json</code> (USD names only). "
             "Verify revenue basis before trading. Click headers to sort.</p>")
    h.append(f"<h2>Programmatic — house vs consensus (|Δ| ≥ {FLAG:.0f}%)</h2>")
    h.append("<table class='sortable'><thead><tr><th>Ticker</th><th>Metric</th><th>Yr</th>"
             "<th class='r'>House</th><th class='r'>Consensus</th><th class='r'>Δ</th></tr></thead><tbody>")
    for r in prog:
        h.append(f"<tr><td class='tk'><a href='../index.html'>{r['tk']}</a></td><td>{r['metric']}</td>"
                 f"<td>{r['year']}</td><td class='r'>{r['house']:,.2f}</td>"
                 f"<td class='r'>{r['cons']:,.2f}</td>"
                 f"<td class='r' data-v='{r['d']:.4f}'>{fmt_d(r['d'])}</td></tr>")
    h.append("</tbody></table>")

    h.append(f"<h2>Curated divergences — latest reconciliation (<code>{recon_name}</code>)</h2>")
    h.append("<table><thead><tr><th>Name</th><th>New datapoint</th><th>Read (the edge)</th></tr></thead><tbody>")
    for d in diverges:
        h.append(f"<tr><td class='tk'>{html.escape(d['name'])}</td>"
                 f"<td>{html.escape(d['new'])}</td><td>{html.escape(d['read'])}</td></tr>")
    h.append("</tbody></table>")

    h.append(f"<h2>Consensus PT vs spot — live pull (upside ranked)</h2>")
    h.append("<table class='sortable'><thead><tr><th>Ticker</th><th class='r'>Spot</th>"
             "<th class='r'>Cons PT</th><th class='r'>Upside</th><th>Read</th></tr></thead><tbody>")
    for r in pts:
        h.append(f"<tr><td class='tk'>{r['tk']}</td><td class='r'>{r['spot']:,.0f}</td>"
                 f"<td class='r'>{r['conspt']:,.0f}</td>"
                 f"<td class='r' data-v='{r['up']:.4f}'>{fmt_d(r['up'])}</td>"
                 f"<td>{html.escape(r['read'])}</td></tr>")
    h.append("</tbody></table>")
    h.append(foot)
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "edge.html").write_text("\n".join(h), encoding="utf-8")

    print(f"edge: {len(prog)} programmatic, {len(diverges)} curated diverges, "
          f"{len(pts)} PT/spot rows (recon={recon_name})")
    print(f"  -> {META/'edge.md'}")
    print(f"  -> {DASH/'edge.html'}")


if __name__ == "__main__":
    main()
