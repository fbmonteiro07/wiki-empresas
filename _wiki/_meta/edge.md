# Edge tracker — house vs Street

_Generated 2026-09-14 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.40 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 547.10 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.74 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-11.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| NVDA | two houses, one disclosure, opposite postures — but it is a BASIS difference, not a disagreement | They agree on the two things that matter structurally |
| AMD | management's headline EPS ambition is not above the Street, and the $100bn server goal sits past the Street's horizon | The Street already crosses $20 in FY2028 at $22.84. |
| AMD | the number that actually drifted is the CPU:GPU ratio, and the bases may not be like-for-like | the number that actually drifted is the CPU:GPU ratio, and the bases may not be like-for-like |
| MSFT | consensus capex decelerates hard while management says it must keep building ahead | The Street's FY28–FY29 capex line embeds a sharp deceleration to low-teens growth that management has not guided and whose stated logic points the other way. |
| CRWV | the same $6.3bn is characterised two opposite ways, and the two readings are not compatible | the same $6.3bn is characterised two opposite ways, and the two readings are not compatible |
| GOOG | SemiAnalysis's $75.5bn of "guarantees" is +$31.5bn above the disclosed line, with no stated scope | SemiAnalysis's $75.5bn of "guarantees" is +$31.5bn above the disclosed line, with no stated scope |
| MSFT | management restated an older stake figure than the page already carries | management restated an older stake figure than the page already carries |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-11.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| CRWV | 89 | 146 | +64% | street high 317 · low 39 below spot · 29/11/3 of 43 |
| NVDA | 218 | 325 | +49% | street high 515 · low 180 below spot · 79/2/1 of 82 |
| GOOG | 335 | 426 | +27% | street high 475 · low 379 ABOVE spot · 16/1/0 of 17 |
| AMD | 516 | 628 | +22% | street high 1,250 · low 465 below spot · 56/12/0 of 68 |
| MSFT | 496 | 574 | +16% | street high 870 · low 400 below spot · 67/4/0 of 71 |
