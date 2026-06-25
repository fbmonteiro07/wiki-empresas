# Wiki feature tools (`_wiki/_tools`)

Six **additive** features layered on the empresas wiki. They are all read-only on
the company pages — every script writes only to `_meta/`, `_data/`, or
`_dashboards/`. Nothing rewrites a page's content.

Rebuild everything in one shot (wire this into the nightly routine, after the ingest):

```
py "E:/Wiki Felipe empresas/_wiki/_tools/refresh_features.py"
py "E:/Wiki Felipe empresas/_wiki/_tools/refresh_features.py --run-estimates"   # also fetch missing BBG
```

## The six

| # | Script | Output | What it does |
|---|---|---|---|
| 1 | `build_edge.py` | `_meta/edge.md`, `_dashboards/edge.html` | House vs Street divergences (the alpha): programmatic (house.json vs estimates.json, USD, \|Δ\|≥15%) + curated (latest `reconciliation-*.md`) + live PT/spot. |
| 2 | `remediate.py` | `_meta/worklist.{md,json}` | Turns lint/staleness flags into an actionable worklist. `--run-estimates` calls the (merge-safe) `fetch_estimates.py`; transcript gaps become `transcript-fetcher` tasks. |
| 3 | `build_readthrough.py` | `_meta/readthrough.md`, `_dashboards/readthrough.html` | Curated supply-chain graph (`_data/graph.json`): per-name upstream suppliers / downstream customers / competitors. |
| 4 | `build_diff.py` | `_meta/diff-latest.md`, `_dashboards/diff.html` | "What changed" digest from page `## Changelog`s + ingest log (rating/PT moves starred). Arg = window in days (default 7). |
| 5 | `build_catalysts.py` | `_meta/catalysts.md`, `_meta/outcomes.md`, `_dashboards/catalysts.html` | Catalyst calendar; flags passed catalysts with no logged outcome for a post-mortem. Log verdicts in `outcomes.md` to build a hit-rate. |
| 6 | `extract_house.py` | `_data/house.json` | Scrapes each page's "Capstone estimates (house model)" table into structured numbers (feeds #1). |

`_wlib.py` = shared read-only helpers. `_data/graph.json` (feature 3) and
`_meta/outcomes.md` (feature 5) are **hand-editable** — extend them over time.

## Rollback

The whole `_wiki/` text layer is git-tracked (the heavy binary archive is not).

```
git -C "E:/Wiki Felipe empresas" log --oneline          # one commit per feature
git -C "E:/Wiki Felipe empresas" revert <feature-commit> # undo one feature
git -C "E:/Wiki Felipe empresas" reset --hard baseline-pre-features   # nuke ALL features
```

Because every feature is additive, you can also just stop running a script and
delete its artifact — nothing else depends on the page content being changed.
