# Edge tracker — house vs Street

_Generated 2026-09-03 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 426.70 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 548.30 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.71 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-02.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| D1 · AVGO | consensus is AT the FY27 guide but ~18% BELOW the FY28 guide. The whole debate is FY27-vs-FY28 phasing, and it is a VOLUME gap, not a margin gap. | consensus is AT the FY27 guide but ~18% BELOW the FY28 guide. The whole debate is FY27-vs-FY28 phasing, and it is a VOLUME gap, not a margin gap. |
| D2 · AVGO | the Capstone house model's GW ladder MATCHES management almost exactly, but the house books ~20% more AI revenue over FY27-28. The gap is entirely DEPLOYMENT TIMING, and the house should make it explicit. | MODEL BRIDGE TO RUN: the house is modelling ~29.5GW of demand as though ~29.5GW ships, at ~$14bn/GW. The same $413bn can be reached from ~15GW shipped at ~$27bn/GW. These are NOT the same model — they have opposite sensitivities. |
| D3 · GOOG | the house's stated EPS edge has CLOSED. Consensus caught up; the page still claims the old gap. | the house's stated EPS edge has CLOSED. Consensus caught up; the page still claims the old gap. |
| D4 · AXTI | management's "revenue opportunity exiting 2026" runs ~15-25% ABOVE the consensus-implied Q4. Flagged, deliberately not scored. | management's "revenue opportunity exiting 2026" runs ~15-25% ABOVE the consensus-implied Q4. Flagged, deliberately not scored. |
| D5 · TSEM | the Street takes the company's FY28 MARGIN but not its FY28 VOLUME. And Stifel initiates Buy at the very bottom of the target range. | the Street takes the company's FY28 MARGIN but not its FY28 VOLUME. And Stifel initiates Buy at the very bottom of the target range. |
| D6 · AXTI | management's FIRST-EVER capex path runs 40-90% ABOVE consensus. This is the cleanest hard divergence of the run. | Internally coherent with everything else AXT said: |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-02.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| SKHYNIX | 1,580,000 | 3,198,064 | +102% | street high 5,300,000 · low 680,000 below spot · 46/1/0 of 47 |
| SAMSUNG | 248,000 | 491,782 | +98% | street high 725,000 · low 300,000 ABOVE spot · 43/0/0 of 43 |
| CRDO | 164 | 283 | +73% | street high 350 · low 227 ABOVE spot · 22/1/0 of 23 |
| AXTI | 56 | 95 | +69% | street high 125 · low 55 below spot · 5/1/0 of 6 |
| MU | 958 | 1,578 | +65% | street high 2,200 · low 900 below spot · 56/4/0 of 60 |
| COHR | 264 | 418 | +58% | street high 500 · low 280 ABOVE spot · 22/6/0 of 28 |
| TSEM | 206 | 312 | +51% | street high 367 · low 260 ABOVE spot · 8/1/1 of 10 |
| AVGO | 357 | 532 | +49% | street high 675 · low 350 below spot · 58/4/0 of 62 |
| ON | 74 | 108 | +47% | street high 150 · low 85 ABOVE spot · 11/19/0 of 30 |
| LITE | 847 | 1,136 | +34% | street high 1,400 · low 820 below spot · 29/4/0 of 33 |
| TSM | 417 | 551 | +32% | street high 700 · low 440 ABOVE spot · 29/1/0 of 30 |
| GOOG | 339 | 428 | +26% | street high 475 · low 379 ABOVE spot · 17/1/0 of 18 |
