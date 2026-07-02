r"""
build_index.py — regenerate 00_INDEX.md from _data/index_meta.json.

00_INDEX.md is a DERIVED artifact: sector membership and the one-line theses
live in _data/index_meta.json (hand-edit that file, never the index itself).
This is the one feature script allowed to write a file in _wiki/ root, and it
writes exactly one: 00_INDEX.md. Guards against drift:

  - every company page on disk must appear in index_meta.json; strays are
    emitted under an "Unclassified" section (never silently dropped);
  - meta entries whose page no longer exists are skipped with a WARN;
  - the header page-count is computed, not typed.

    py "E:/Wiki Felipe empresas/_wiki/_tools/build_index.py"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _wlib import WIKI, DATA, TODAY, company_pages

sys.stdout.reconfigure(encoding="utf-8")

LABS_SECTION = "AI labs (private)"

PREAMBLE = """# Research Wiki — by company

> 🌐 **Navigable version (offline):** open [`index.html`](index.html) — sidebar by theme + full-text search across all pages. Rebuild: `py E:/.claude/scripts/build_wiki_html.py`.
>
> 📊 **Dashboards** (hub: [`_dashboards/index.html`](_dashboards/index.html)): [edge tracker](_dashboards/edge.html) · [read-through map](_dashboards/readthrough.html) · [catalyst loop](_dashboards/catalysts.html) · [catalyst timeline (Gantt)](_dashboards/gantt.html) · [what changed](_dashboards/diff.html) · [canonical assumptions](_dashboards/assumptions.html) · [book exposure](_dashboards/book.html). Rebuild all: `py "_wiki/_tools/refresh_features.py"`.
>
> 🔎 **Full-corpus search** (reports + calls + briefings + transcripts + Stratechery, not just wiki pages): `py "_wiki/_tools/search.py" <query>` (index: `py "_wiki/_tools/build_search_index.py"`).
"""

DESCRIPTION = """Each page follows the [_TEMPLATE](_TEMPLATE.md): Snapshot · Current state (latest quarter) · Debate (bull/bear + where the sell-side stands, attributed + dated) · Catalysts · Risks · Consensus estimates (BBG) · Sources (links). Archive master index: [../INDEX.md](../INDEX.md). Thematic pages: [themes/00_THEMES.md](themes/00_THEMES.md).

> Attribution is the point: every datapoint carries its source (broker/analyst/call + date). Where on-disk coverage is thin (small-caps, power, Toyota), the page says so explicitly."""


def main():
    meta = json.loads((DATA / "index_meta.json").read_text(encoding="utf-8"))
    on_disk = {t for t, _ in company_pages()}

    listed, out_sections = set(), []
    n_labs = 0
    for sec in meta["sections"]:
        rows = []
        for e in sec["entries"]:
            t = e["ticker"]
            if t not in on_disk:
                print(f"[WARN] index_meta.json lists {t} ({sec['title']}) but _wiki/{t}.md does not exist — skipped")
                continue
            listed.add(t)
            thesis = e["thesis"].replace("|", "\\|")
            rows.append(f"| {t} | [{e['display']}]({t}.md) | {thesis} |")
        if not rows:
            continue
        if sec["title"] == LABS_SECTION:
            n_labs = len(rows)
        out_sections.append(
            f"## {sec['title']}\n| Ticker | Page | One-line thesis |\n|---|---|---|\n" + "\n".join(rows)
        )

    stray = sorted(on_disk - listed)
    if stray:
        print(f"[WARN] {len(stray)} page(s) not in index_meta.json — emitted under 'Unclassified': {', '.join(stray)}")
        rows = [f"| {t} | [{t}]({t}.md) | ⚠ not yet classified — add to `_data/index_meta.json` |" for t in stray]
        out_sections.append(
            "## Unclassified (auto-flagged)\n| Ticker | Page | One-line thesis |\n|---|---|---|\n" + "\n".join(rows)
        )

    n_pages = len(listed) + len(stray)
    n_cos = n_pages - n_labs
    header = (
        f"_Generated {TODAY.isoformat()} by `_tools/build_index.py` from [`_data/index_meta.json`](_data/index_meta.json) "
        f"(hand-edit the json, not this file) · **{n_cos} companies + {n_labs} private AI labs ({n_pages} pages)** · "
        "one page per ticker synthesizing all co-located sources in `E:\\Wiki Felipe`: filings (10-K/10-Q/20-F) + "
        "earnings transcripts + investor-day decks + thematic equity calls (`_equity_calls`) + per-ticker roll-up of "
        "the email briefings (`_briefings/by-ticker`) + BBG consensus & street-high estimates (`_data/estimates.json`)._"
    )

    body = "\n\n".join([PREAMBLE.rstrip(), header, DESCRIPTION, *out_sections]) + "\n"
    (WIKI / "00_INDEX.md").write_text(body, encoding="utf-8")
    print(f"00_INDEX.md -> {n_pages} pages · {len(out_sections)} sections · {n_labs} labs")


if __name__ == "__main__":
    main()
