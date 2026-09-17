# Edge tracker — house vs Street

_Generated 2026-09-17 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.20 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.10 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.77 | +15% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-17.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| ★ — | CIEN: the "$8.3–8.4B FY27 floor" is arithmetically EMPTY, and consensus had already cleared it before it was published | Where the asymmetry actually is: MARGIN, not revenue. |
| ★★ — | META: Goldman publishes a BUY on top of a model 13% below consensus on 2027 EBIT and 18% below on EPS — while sitting 1.7% ABOVE on revenue | So the house already agrees with GS that the cash line goes deeply negative, and disagrees only about whether that shows up in EPS. |
| — | CIEN 2029: the revenue target is already in the curve; the entire surprise is margin — but the comparison is a year offset and must be labelled as such | CIEN 2029: the revenue target is already in the curve; the entire surprise is margin — but the comparison is a year offset and must be labelled as such |
| — | CIEN: management's own "~5x cash generated from operations" does not close against the published FY25 base | Either the base year is not FY25, or the multiple is rounded generously. |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-17.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| CIEN | 355 | 502 | +41% | street high 660 · low 324 below spot · 15/5/1 of 21 |
| BKNG | 169 | 239 | +41% | street high 301 · low 188 ABOVE spot · 33/9/0 of 42 |
| META | 673 | 752 | +12% | street high 1,000 · low 580 below spot · 72/7/0 of 79 |
| PANW | 378 | 403 | +7% | street high 475 · low 190 below spot · 46/13/1 of 60 |
| CRWD | 245 | 239 | -3% | street high 425 · low 132 below spot · 41/14/1 of 56 |
