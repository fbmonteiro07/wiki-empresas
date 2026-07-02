# Wiki Felipe empresas — Capstone buyside research repo

One synthesized page per ticker (`_wiki/*.md`, ~101 names) + cross-company themes (`_wiki/themes/`), sitting on the raw archive (SEC filings, earnings transcripts, decks per ticker folder; equity calls, briefings, ingested reports, Stratechery at root). **Attribution is the point: every datapoint carries broker/analyst + date.**

## Answering research questions — do this FIRST

1. **Graph context**: `py "E:\Wiki Felipe empresas\_wiki\_tools\graph_query.py" --prompt "<the question>"` → context cards (thesis, supply chain, themes, canonical debate numbers, consensus, docs on disk) for every ticker/topic mentioned. A UserPromptSubmit hook injects this automatically — if a `[wiki knowledge-graph context …]` block is already in the prompt, don't re-run it, use it.
2. **Read the page**: open `_wiki/<TICKER>.md` (Debate + Changelog sections) before answering from model memory. Themes: `_wiki/themes/<slug>.md`.
3. **Primary sources**: `py "E:\Wiki Felipe empresas\_wiki\_tools\search.py" [-t TICKER] [-k call,transcript,report,briefing] <query>` — full-corpus FTS over reports/calls/briefings/transcripts/Stratechery, not just wiki pages.
4. **Cross-page numbers** (ASIC share, WFE TAM, hyperscaler capex, GW, HBM, AI TAM, DRAM pricing): use the canonical framing in `_wiki/_meta/assumptions.md` (`_data/assumptions.json`); cite variants by source+date. **Never mix GW bases** — facility GW ≠ IT-load GW ≠ 800V-subset GW.

## Rules

- Respond in English, even when the question is in Portuguese.
- Every datapoint attributed (broker/analyst/call + date). On pasted exhibits, confirm the source with the user — don't infer it.
- **Thesis-drift rule**: never silently overwrite a number/rating/PT/thesis on a page — move the old value into the page's `## Changelog` with the date, then update the body.
- When a catalyst resolves, add a line to `_wiki/_meta/outcomes.md` (`- TICKER YYYY-MM-DD — bull won|bear won|neutral — note`).
- Feature scripts are read-only on pages; they write only to `_wiki/_meta`, `_wiki/_data`, `_wiki/_dashboards`. Sole exception: `build_index.py` regenerates `_wiki/00_INDEX.md` (and nothing else) from `_data/index_meta.json`.
- Machine is behind a TLS proxy — stdlib Python only, no pip.

## Rebuild / refresh

- Everything (dashboards, meta, search index, graph): `py "E:\Wiki Felipe empresas\_wiki\_tools\refresh_features.py"`
- BBG estimates (needs terminal): `py E:/.claude/scripts/fetch_estimates.py [tickers]` → then `py _wiki/_tools/build_snapshot.py`
- Staleness report: `py E:/.claude/scripts/lint_wiki.py`
- Inbox ingest: drop PDFs in `_inbox/`, run `py E:/.claude/scripts/ingest_inbox.py` (trust the filename `YYYYMMDD` date prefix over PDF metadata).

## Map

- `_wiki/00_INDEX.md` — master index with one-line theses (**derived** — edit `_data/index_meta.json`, rebuild with `build_index.py`) · `_wiki/_TEMPLATE.md` — page structure
- `_wiki/_meta/` — assumptions.md, edge.md, catalysts.md + outcomes.md, book.md, staleness.md, diff-latest.md, worklist.md
- `_wiki/_data/` — estimates.json (BBG consensus), house.json (Capstone models), book.json (positions — hand-edit), assumptions.json (canonical numbers — hand-edit), graph.json (curated supply edges — hand-edit), index_meta.json (sector membership + one-line theses — hand-edit), graph_full.json (derived), search.db (derived)
- `_wiki/_dashboards/index.html` — hub (edge, read-through, catalysts, gantt, diff, coverage, assumptions, book, graph)
