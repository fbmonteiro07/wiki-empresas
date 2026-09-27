# Edge tracker — house vs Street

_Generated 2026-09-26 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.30 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.10 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-09-24-night.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| D1 | **DB rating history: Hold since 2024-11-12; Hold $105 on 2026-05-29; Hold $150 set 2026-08-27** (DB p.5 table) | 🔴 **The wiki was wrong, not the Street.** Corrected on the page with the old value in `## Changelog`. Any past "unanimous-ish Buy" reading of the OKTA ladder that counted DB as a Buy overstated bullishness by one house. |
| D2 | **DB PT $150** (reaffirmed) | Lowest target on the wiki's ladder, but NOT the Street low — at least one un-ingested house sits at $127. **Recover who owns the $127.** |
| D3 | **Agent-product price ≈ 75% uplift on core** (one Energy CISO: $1.5m/yr vs $2m core; beta since Dec) | ⚠️ Single account, beta pricing, a quote. Above mgmt's range — but DB uses it to argue pricing is **fragile** (competition coming), not conservative. Directional only; not written to any estimate. |
| D4 | **Renewal pull-forward: Jan-2027 renewal pulled into Aug-2026** (VAR #3) | Qualitative but directly bears on the F3Q27 cRPO print (~2026-12-02): cRPO beat without sub-revenue acceleration = DB/Bernstein bear case. Adds a second, independent mechanism to the same-direction risk. |

## Consensus PT vs spot — live pull in `reconciliation-2026-09-24-night.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
