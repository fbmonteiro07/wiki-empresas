# Edge tracker — house vs Street

_Generated 2026-10-06 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| GOOG | Revenue $bn | 2026 | 505.00 | 427.40 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 545.10 | +18% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-10-02.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 1 | **KIOXIA** | Same near-term numbers as the Street, but the out-year collapses: Bernstein's CY28 "normalization" plus the YMTC threat. **The bear is entirely an FY3/29 call.** |
| 2 | **SK hynix** | Above the Street on CY27, well below on CY28. The TP cut is HBM pricing (smaller CY27 HBM hike for SKH, share shifting to Samsung), not the cycle. |
| 3 | **Samsung** | Same shape as SKH: the CY28 normalization is a −30-40% EPS gap to consensus across all three DRAM names. That is Bernstein's single biggest disagreement with the Street. |
| 4 | **MU** | ⚠ Stale on arrival: written before the 09-30 print, and its 4QFY26E / 1QFY27E sit below the actual print and the guide (see MU page). The FY28 gap is the normalization call, not stale data. |
| 5 | **SNDK** | Bernstein is near the Street high on NAND while modelling NAND GM normalizing to mid-60s% exiting CY28. That sits awkwardly with its KIOXIA Underperform. **The rating split is about YMTC exposure and valuation, not NAND pricing.** |
| 6 | **META** capex | The house is now ~14% below cash consensus and ~28% below Bernstein's lease-inclusive path on 2027. This widens the open house-vs-Street META capex divergence from 09-28. **Bridge needed: lease/ROU share of META 2027 capex.** |
| 7 | **GOOG** | Below the Street on PT and EPS, above it on capex: the classic "capex up, EPS down" Market-Perform. 2027 capex sits between house ($310bn) and JPM ($378bn). |
| 8 | **ORCL** | Near the Street high on PT. Exhibit 13's ORCL capex path does not reconcile on any single basis: 2026E $107bn vs FY26 cash actual $56bn, while 2027E $92bn sits on the FY27 cash guide. Treat it as a capacity-model input, not an Oracle forecast. |
| 9 | **MSFT** | Basis is ambiguous (xlsx says "through CY2027", Bernstein's MSFT base year is fiscal). If lease-inclusive, $200bn is BELOW cash consensus, an internal oddity in a capacity model, not a call on MSFT. |
| 10 | **STX** | MS is far above calendarized consensus EPS. Stock **−10% on 10-02** ($945.57 → $848.99) on the Toshiba ¥60bn capacity headline, which MS argues is <25% of supply growth and ~5% of industry EB. |
| 11 | **WDC** | Same as STX. Stock **−10%** ($462.56 → $415.29). |
| 12 | **CEG / VST** (roster) | Outperform-rated but ~15% below consensus PT on both IPPs. A low-end bull, worth knowing when citing "Bernstein constructive". |
| 13 | **CRWV** (roster) | Street low, still the only Underperform on the page. |

## Consensus PT vs spot — live pull in `reconciliation-2026-10-02.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| WDC | 414 | 655 | +58% | street high 900 · low 466 ABOVE spot · 21/7/0 of 28 |
| BESI | 193 | 281 | +46% | street high 400 · low 173 below spot · 16/8/0 of 24 |
| STX | 819 | 1,127 | +38% | street high 1,400 · low 860 ABOVE spot · 23/4/0 of 27 |
| IFX | 64 | 88 | +37% | street high 124 · low 50 below spot · 27/4/0 of 31 |
| ASML | 1,849 | 2,460 | +33% | street high 2,915 · low 2,100 ABOVE spot · 21/0/0 of 21 |
| VRT | 255 | 333 | +31% | street high 400 · low 188 below spot · 30/6/1 of 37 |
| AMZN | 255 | 333 | +30% | street high 405 · low 230 below spot · 77/4/0 of 81 |
| SNOW | 340 | 438 | +29% | street high 525 · low 280 below spot · 51/5/1 of 57 |
| MDB | 363 | 459 | +27% | street high 565 · low 372 ABOVE spot · 37/8/0 of 45 |
| DISCO | 65,500 | 81,867 | +25% | street high 105,000 · low 63,000 below spot · 18/6/0 of 24 |
| NVT | 175 | 211 | +21% | street high 260 · low 182 ABOVE spot · 19/1/0 of 20 |
| APH | 90 | 108 | +20% | street high 198 · low 90 ABOVE spot · 17/3/0 of 20 |
| TEL | 222 | 248 | +12% | street high 300 · low 215 below spot · 16/6/0 of 22 |
| BE | 296 | 292 | -1% | street high 450 · low 105 below spot · 23/13/1 of 37 |
