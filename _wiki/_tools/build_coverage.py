r"""
FEATURE 8 — Source-coverage audit ("is everything being read?").

lint_wiki/remediate flag *missing* inputs (no BBG, no transcript on disk). This
flags the opposite failure: inputs that EXIST on disk but the synthesized page
never read. It measures, per ticker, available source material vs. what the page
actually cites/links, and ranks the most under-read names.

Robust signals (not fooled by a page that deliberately links a representative
subset — e.g. "39 calls, see INDEX" + 4 links):
  - FRESHNESS OF READING: the newest transcript / 10-Q on disk doesn't appear in
    the page at all  -> the latest primary source went unread.
  - TYPE IGNORED: decks / equity-calls / reports exist on disk but the page links
    zero of that type.
  - SYNTHESIS DENSITY: lots of material (filings+transcripts+calls+briefings) but
    few dated citations / low word count -> thin synthesis.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_coverage.py"

Writes _meta/coverage.md + _dashboards/coverage.html. Read-only on pages.
"""
import sys, re, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _wlib import WIKI, META, DASH, TODAY, company_pages, read, DATE_RE, html_head
sys.stdout.reconfigure(encoding="utf-8")

SEC = WIKI.parent   # E:\Wiki Felipe empresas


def index_counts():
    """Parse INDEX.md summary table -> {tk: {sec, tx, decks, calls, briefings}}."""
    out = {}
    p = SEC / "INDEX.md"
    if not p.is_file():
        return out
    for ln in read(p).split("\n"):
        m = re.match(r"^\|\s*([A-Z]{1,10})\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", ln)
        if m:
            out[m.group(1)] = dict(sec=int(m[2]), tx=int(m[3]), decks=int(m[4]),
                                   calls=int(m[5]), briefings=int(m[6]))
    return out


def disk_transcripts(tk):
    d = SEC / tk / "transcripts"
    dates = []
    if d.is_dir():
        for f in d.glob("*.md"):
            m = DATE_RE.search(f.name)
            if m:
                dates.append(m.group(1))
    return sorted(dates)


def disk_filings(tk):
    """[(type, date)] for top-level filing html (10-K/10-Q/20-F)."""
    out = []
    for f in (SEC / tk).glob(f"{tk}_*.html") if (SEC / tk).is_dir() else []:
        m = re.match(rf"{tk}_(10-K|10-Q|20-F|8-K)_(20\d\d-\d\d-\d\d)", f.name)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def disk_decks(tk):
    """(total_pdf_count, latest_deck_date) — date parsed from filename."""
    d = SEC / tk / "apresentações"
    if not d.is_dir():
        return 0, None
    pdfs = list(d.rglob("*.pdf"))
    dates = [DATE_RE.search(f.name).group(1) for f in pdfs if DATE_RE.search(f.name)]
    return len(pdfs), (max(dates) if dates else None)


def page_links(md):
    """All relative link targets (../X) in the page, '../' stripped, %20 decoded."""
    raw = re.findall(r"\]\(\.\./([^)\s]+)\)", md)
    return [l.replace("%20", " ").replace("%C3%A3", "ã").replace("%C3%B3", "ó") for l in raw]


def audit():
    idx = index_counts()
    rows = []
    for tk, pf in company_pages():
        md = read(pf)
        if "no public financials" in md.lower() or "private company" in md.lower():
            continue   # private labs — different source model
        words = len(re.findall(r"\w+", md))
        page_dates = set(DATE_RE.findall(md))
        n_cit = len(page_dates)
        links = page_links(md)
        low = [l.lower() for l in links]

        tx_disk = disk_transcripts(tk)
        latest_tx = tx_disk[-1] if tx_disk else None
        latest_tx_read = bool(latest_tx and latest_tx in page_dates)

        fil = disk_filings(tk)
        def latest(kind):
            ds = sorted(d for t, d in fil if t == kind)
            return ds[-1] if ds else None
        lq, lk = latest("10-Q"), latest("10-K")
        latest_10q_read = (lq is None) or (lq in page_dates)
        latest_10k_read = (lk is None) or (lk in page_dates)
        # the 10-Q is usually redundant when the same-quarter transcript was read —
        # only treat an unread 10-Q as a real miss if the quarter isn't otherwise covered.
        def _near(a, b, days=75):
            from datetime import date
            try:
                return abs((date.fromisoformat(a) - date.fromisoformat(b)).days) <= days
            except Exception:
                return False
        q_covered = bool(latest_tx_read and latest_tx and lq and _near(latest_tx, lq))
        q10_miss = (lq is not None) and (not latest_10q_read) and (not q_covered)

        ix = idx.get(tk, {})
        calls_avail = ix.get("calls", 0)
        briefings = ix.get("briefings", 0)
        decks_disk, latest_deck = disk_decks(tk)
        # only a RECENT deck (≤ ~2y) that's uncited counts as a real miss — a 2021
        # investor day legitimately doesn't need citing in a 2026 page.
        deck_recent = bool(latest_deck and (TODAY - __import__("datetime").date.fromisoformat(latest_deck)).days <= 760)
        deck_read = any(latest_deck and latest_deck in l for l in links) if latest_deck else True

        calls_used = sum(1 for l in low if l.startswith("_equity_calls/"))
        decks_used = sum(1 for l in low if "apresenta" in l)
        reports_used = sum(1 for l in low if l.startswith("relat"))

        # --- flags ---
        flags = []
        if latest_tx and not latest_tx_read:
            flags.append(f"latest transcript {latest_tx} unread")
        if q10_miss:
            flags.append(f"latest 10-Q {lq} unread (no same-qtr transcript either)")
        if calls_avail >= 3 and calls_used == 0:
            flags.append(f"{calls_avail} equity calls on file, 0 linked")
        if deck_recent and not deck_read and decks_used == 0:
            flags.append(f"recent deck {latest_deck} uncited ({decks_disk} on disk)")
        if briefings >= 15 and n_cit < 12:
            flags.append(f"{briefings} briefings but only {n_cit} dated citations")

        material = ix.get("sec", 0) + ix.get("tx", 0) + calls_avail + briefings + decks_disk
        engagement = words + 25 * n_cit
        density = round(engagement / material, 1) if material else None  # synthesis per unit of source

        # severity: freshness misses dominate, then ignored types, then thinness
        sev = (3 * (latest_tx is not None and not latest_tx_read)
               + 2 * q10_miss
               + 1.5 * (calls_avail >= 3 and calls_used == 0)
               + 1.0 * (deck_recent and not deck_read and decks_used == 0)
               + 1.0 * (briefings >= 15 and n_cit < 12)
               + (1.0 if (material >= 25 and (density or 1e9) < 90) else 0))

        rows.append(dict(tk=tk, words=words, cit=n_cit, material=material, density=density,
                         tx=f"{len(tx_disk)}", latest_tx=latest_tx or "—", tx_ok=latest_tx_read,
                         calls=f"{calls_used}/{calls_avail}", decks=f"{decks_used}/{decks_disk}",
                         reports=reports_used, briefings=briefings, sev=round(sev, 1),
                         flags=flags))
    rows.sort(key=lambda r: (-r["sev"], r["density"] if r["density"] is not None else 1e9))
    return rows


def main():
    rows = audit()
    # "flagged" = a concrete unread source (not the soft low-density signal alone)
    flagged = [r for r in rows if r["flags"]]

    # ---- markdown ----
    md = [f"# Source-coverage audit\n",
          f"_Generated {TODAY.isoformat()} · {len(rows)} public-company pages · "
          f"flags inputs that exist on disk but the page never read. "
          f"Rebuild: `py _wiki/_tools/build_coverage.py`._\n",
          f"**{len(flagged)} pages flagged** (severity > 0), worst first.\n",
          "| Sev | Ticker | Words | Cites | Density | Latest tx | tx read? | Calls used | Decks | What's unread |",
          "|--:|---|--:|--:|--:|---|:--:|---|---|---|"]
    for r in flagged:
        md.append(f"| {r['sev']} | {r['tk']} | {r['words']} | {r['cit']} | "
                  f"{r['density'] if r['density'] is not None else '—'} | {r['latest_tx']} | "
                  f"{'✓' if r['tx_ok'] else '✗'} | {r['calls']} | {r['decks']} | "
                  f"{'; '.join(r['flags'])} |")
    md.append("\n_Density = (words + 25·citations) / (filings+transcripts+calls+briefings+decks). "
              "Low density + high material = thin synthesis. 'Calls used' = `_equity_calls` links / "
              "available (a low ratio is fine if the page links a representative subset)._")
    META.mkdir(parents=True, exist_ok=True)
    (META / "coverage.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---- html ----
    head, foot = html_head("🔎 Source-coverage audit",
                           f"{TODAY.isoformat()} · {len(flagged)}/{len(rows)} pages flagged · inputs on disk the page never read")
    h = [head, "<p class='byline'>Ranks pages by how much available source material looks <b>unread</b>. "
               "Severity weights freshness misses (latest transcript / 10-Q absent from the page) highest, "
               "then ignored source types, then thin synthesis. A low 'calls used' ratio alone is fine — "
               "pages link a representative subset.</p>"]
    h.append("<table class='sortable'><thead><tr>"
             "<th class='r'>Sev</th><th>Ticker</th><th class='r'>Words</th><th class='r'>Cites</th>"
             "<th class='r'>Density</th><th>Latest tx</th><th>Read?</th><th>Calls used</th>"
             "<th>Decks</th><th>What's unread</th></tr></thead><tbody>")
    for r in rows:
        cls = "neg" if r["sev"] >= 3 else ("" if r["sev"] == 0 else "")
        readmark = "<span class='pos'>✓</span>" if r["tx_ok"] else "<span class='neg'>✗</span>"
        h.append(f"<tr><td class='r' data-v='{r['sev']}'><b class='{cls}'>{r['sev']}</b></td>"
                 f"<td class='tk'><a href='../{r['tk']}.html'>{r['tk']}</a></td>"
                 f"<td class='r'>{r['words']}</td><td class='r'>{r['cit']}</td>"
                 f"<td class='r'>{r['density'] if r['density'] is not None else '—'}</td>"
                 f"<td>{r['latest_tx']}</td><td>{readmark}</td><td>{r['calls']}</td>"
                 f"<td>{r['decks']}</td><td style='font-size:12px'>{html.escape('; '.join(r['flags']))}</td></tr>")
    h.append("</tbody></table>")
    h.append(foot)
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "coverage.html").write_text("\n".join(h), encoding="utf-8")

    print(f"coverage: {len(flagged)}/{len(rows)} pages flagged")
    print(f"  -> {META/'coverage.md'}\n  -> {DASH/'coverage.html'}")
    print("\nTop 12 under-read:")
    for r in rows[:12]:
        print(f"  {r['sev']:>4}  {r['tk']:<10} dens={r['density']}  "
              f"tx={r['tx']}(latest {r['latest_tx']} {'read' if r['tx_ok'] else 'UNREAD'})  "
              f"calls={r['calls']} decks={r['decks']}  | {'; '.join(r['flags'])}")


if __name__ == "__main__":
    main()
