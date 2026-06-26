# Edge tracker — house vs Street

_Generated 2026-06-26 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.66 | +99% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.00 | +51% |
| LITE | EPS | 2027 | 30.02 | 23.53 | +28% |
| GOOG | Revenue $bn | 2027 | 641.00 | 510.00 | +26% |
| COHR | EPS | 2026 | 8.27 | 6.75 | +23% |
| GOOG | Revenue $bn | 2026 | 505.00 | 417.10 | +21% |
| NVDA | EPS | 2027 | 15.44 | 12.80 | +21% |
| NVDA | Revenue $bn | 2027 | 661.00 | 558.70 | +18% |

## Curated divergences — latest reconciliation (`reconciliation-2026-06-25.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| COHR | BofA CY27/28 EPS **$9.77 / $12.17**, PO $400 NEUTRAL (05-13) | **BBG resolves this: the outlier is OURS, not BofA's.** Street consensus EPS (FY26/27/28) **$5.46 / $8.33 / $11.98**; BofA's $9.77/$12.17 is **in line with Street**; our house **$19.21 ≈ 2× consensus**. Cons PT $386 ≈ BofA $400. **Action: interrogate the house COHR model** (Jefferies 1.6T ramp far above Street). |
| MRVL | BofA PO **$200 BUY**, FY28/29 EPS $5.60/$7.80 (05-13) | **BBG flags the page is stale:** live cons PT **$256**, stock **$281** — the $120/$80 on the page are obsolete. BofA $200 is **below** live consensus PT, and its EPS (FY28 $5.60) is **below** Street ($6.92) — so $200 is multiple-light, not a bull outlier. **Action: refresh MRVL targets.** |
| TSLA | JPM EPS 26E **$1.90** / 27E **$2.15** / 28E **$3.15**, PO $475 Neutral (06-24) | JPM 26E ≈ cons ($1.87); **JPM out-years BELOW Street** (27E $2.15 vs cons $2.44, -12%; 28E $3.15 vs $3.34) — JPM more cautious on the robotaxi ramp. But **PO $475 > cons $422 > spot $375**. Rev 26E $104.2bn ≈ cons $102.6bn. |
| AVGO | BofA ~**$110bn FY27 AI sales** (consensus; flags upside), top pick (05-13) | House FY27 EPS $21.07 ≈ cons FY27 **$19.20**; but house FY28 **$35.96 vs cons $25.72 (+40%)** — house bullish on the out-year. Cons PT **$522 vs spot $379 (+38% upside)** — Street very constructive. |
| GOOG | FundaAI capex **$180–190bn 2026**; Barclays capex "up significantly" 2027 | New sell-side **matches house 2026 capex exactly ($183bn)**. EPS: house 27E $16.20 ≈ cons **$15.34** (page's "vs ~$14.5 consensus" was stale). ⚠️ **Revenue basis mismatch** — house 2026 rev $505bn vs BBG `BEST_SALES` $422bn; likely gross-vs-net/TAC basis, verify before trusting the gap. |
| INTC | BofA PO **$56 → $96** but **still UNDERPERFORM** (05-13) | PT **+71% yet rating unchanged** — BofA chasing price, not endorsing. Logged to Changelog. |
| LITE | BofA PO **$1,100 NEUTRAL** (05-13) | $1,100 = ~37× house 2027E EPS. House very bullish; BofA neutral at a price the house EPS easily supports. |

## Consensus PT vs spot — live pull in `reconciliation-2026-06-25.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| NVDA | 196 | 301 | +54% | +54% upside to cons PT; house EPS ≈ cons |
| AVGO | 379 | 522 | +38% | +38% upside to cons PT; house FY28 +40% vs Street |
| LITE | 862 | 1,126 | +31% | BofA ≈ cons PT; house $30 ≈ cons FY28 (1 yr early) |
| ALAB | 398 | 278 | -30% | **stock 43% > cons PT** — most stretched vs targets |
| GOOGL | 344 | 432 | +26% | house 27E ≈ cons; rev basis to verify |
| INTC | 133 | 100 | -25% | **stock > both PTs** — momentum ahead of fundamentals |
| ARM | 348 | 284 | -18% | stock > cons PT > BofA |
| TSLA | 375 | 422 | +13% | PO above Street; JPM EPS below Street out-years |
| MRVL | 281 | 256 | -9% | stock > cons PT > BofA; wiki $120/$80 stale |
| AMD | 533 | 498 | -7% | BofA ≈ cons; stock above both |
| COHR | 407 | 386 | -5% | BofA ≈ Street; **house $19.21 = 2× Street** |
