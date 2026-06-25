r"""
FEATURE 4 — "What changed" diff digest.

The nightly ingest writes a dated bullet into each page's '## Changelog' and a
run line into _meta/changelog.md. This rolls those up into a single recent-changes
digest (rating/PT moves highlighted) — the wiki's own delta, distinct from the
inbox briefing.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_diff.py"        # last 7 days
    py "E:/Wiki Felipe empresas/_wiki/_tools/build_diff.py 30"     # last 30 days

Writes _meta/diff-latest.md + _dashboards/diff.html. Read-only on pages.
"""
import sys, re, html, datetime as dt
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from _wlib import WIKI, META, DASH, company_pages, read, changelog_entries, html_head, TODAY
sys.stdout.reconfigure(encoding="utf-8")

WINDOW = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
CUTOFF = TODAY - dt.timedelta(days=WINDOW)

RATING = re.compile(r"\b(upgrade|downgrade|initiat|rais|cut|lower|PT|price target|"
                    r"\$\d|Buy|Sell|Hold|Overweight|Underweight|Neutral|Outperform)\b", re.I)


def recent(md):
    out = []
    for d, txt in changelog_entries(md):
        try:
            if dt.date.fromisoformat(d) >= CUTOFF:
                out.append((d, txt))
        except ValueError:
            pass
    return out


def ingest_runs():
    p = META / "changelog.md"
    if not p.is_file():
        return []
    out = []
    for ln in read(p).split("\n"):
        m = re.match(r"^\s*[-*]\s+(20\d\d-\d\d-\d\d)\s*[·;]\s*(.*)$", ln)
        if m:
            try:
                if dt.date.fromisoformat(m.group(1)) >= CUTOFF:
                    out.append((m.group(1), m.group(2).strip()))
            except ValueError:
                pass
    return out


def main():
    rows = []   # (date, ticker, text, is_rating)
    for tk, pf in company_pages():
        for d, txt in recent(read(pf)):
            rows.append((d, tk, txt, bool(RATING.search(txt))))
    rows.sort(key=lambda r: (r[0], r[1]), reverse=True)
    runs = ingest_runs()
    n_rating = sum(1 for r in rows if r[3])

    # ---------- markdown ----------
    md = [f"# What changed — last {WINDOW} days\n",
          f"_Generated {TODAY.isoformat()} (since {CUTOFF.isoformat()}) · rolls up every page's "
          f"`## Changelog` + the ingest run log. ⭐ = rating/PT move. "
          f"Rebuild: `py _wiki/_tools/build_diff.py [days]`._\n"]
    if rows:
        md.append("| Date | Ticker | Change |")
        md.append("|---|---|---|")
        for d, tk, txt, rat in rows:
            md.append(f"| {d} | {'⭐ ' if rat else ''}{tk} | {txt} |")
    else:
        md.append("_No page-level changelog entries in window. (Changelogs fill in as the "
                  "nightly ingest folds new datapoints — this digest grows with them.)_\n")
    md.append(f"\n## Ingest runs in window ({len(runs)})\n")
    if runs:
        for d, txt in runs:
            md.append(f"- **{d}** — {txt}")
    else:
        md.append("_none_")
    META.mkdir(parents=True, exist_ok=True)
    (META / "diff-latest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- html ----------
    head, foot = html_head(f"What changed — last {WINDOW} days",
                           f"{TODAY.isoformat()} · {len(rows)} page changes ({n_rating} rating/PT) · {len(runs)} ingest runs")
    h = [head, "<p class='byline'>⭐ = rating / price-target move. Rolls up page changelogs + ingest log.</p>"]
    if rows:
        h.append("<table class='sortable'><thead><tr><th>Date</th><th>Ticker</th><th>Change</th></tr></thead><tbody>")
        for d, tk, txt, rat in rows:
            star = "⭐ " if rat else ""
            h.append(f"<tr><td>{d}</td><td class='tk'>{star}{tk}</td><td>{html.escape(txt)}</td></tr>")
        h.append("</tbody></table>")
    else:
        h.append("<p>No page-level changelog entries in window. This digest grows as the nightly "
                 "ingest folds new datapoints into page changelogs.</p>")
    h.append(f"<h2>Ingest runs in window ({len(runs)})</h2><ul>")
    for d, txt in runs:
        h.append(f"<li><b>{d}</b> — {html.escape(txt)}</li>")
    h.append("</ul>")
    h.append(foot)
    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "diff.html").write_text("\n".join(h), encoding="utf-8")

    print(f"diff ({WINDOW}d): {len(rows)} page changes ({n_rating} rating/PT), {len(runs)} ingest runs")
    print(f"  -> {META/'diff-latest.md'}\n  -> {DASH/'diff.html'}")


if __name__ == "__main__":
    main()
