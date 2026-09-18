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
| ★★ — | CRWD: the consensus price target has gone BELOW spot, and 41 of 56 analysts still say Buy | The average target is 2.79% BELOW the market price. |
| ★★ — | CRWD FY29: consensus underwrites only the FLOOR of the new operating-margin target — the cleanest quantified edge of the run | Consensus FY29 operating margin is 28.00% — the bottom of management's band, to two decimals. The Street has taken the revenue ramp and declined the margin ramp. |
| ★ — | CRWD FY28 free cash flow: the Street's published mark is the company's own guide applied to the analyst's own revenue | DB's FCF number is not an independent estimate; it is the guided margin identity applied to DB's own revenue line. |
| ★ — | The consolidation thesis has no independent survey support, and the one survey that exists is mildly against it | Against MS · Cerisola's 09-15 framing |
| ★ — | CrowdStrike marks its own current AI cyber-spend attach at 1%; the sell-side uses 6–7% | The two independent ladders AGREE at the ~8% ceiling and differ SIX-FOLD at the floor. |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-17.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ON | 68 | 105 | +54% | street high 150 · low 75 ABOVE spot · 11/19/0 of 30 |
| CIEN | 344 | 502 | +46% | street high 660 · low 324 below spot · 15/5/1 of 21 |
| BKNG | 171 | 239 | +40% | street high 301 · low 188 ABOVE spot · 33/9/0 of 42 |
| MSFT | 498 | 574 | +15% | street high 870 · low 400 below spot · 67/4/0 of 71 |
| META | 682 | 752 | +10% | street high 1,000 · low 580 below spot · 72/7/0 of 79 |
| PANW | 375 | 403 | +7% | street high 475 · low 190 below spot · 46/13/1 of 60 |
| CRWD | 246 | 239 | -3% | street high 425 · low 132 below spot · 41/14/1 of 56 |
