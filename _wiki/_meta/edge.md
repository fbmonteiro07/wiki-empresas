# Edge tracker — house vs Street

_Generated 2026-08-28 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.89 | +62% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.70 | +31% |
| GOOG | Revenue $bn | 2026 | 505.00 | 427.10 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 548.30 | +17% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-27.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴🔴 NVDA GROSS MARGIN | CONSENSUS IS 106-206bp ABOVE MANAGEMENT'S OWN GUIDED TROUGH (was 141-241bp on the 09:12 pull; the Street cut FQ4 GM 35bp intraday). THIS IS THE SINGLE LARGEST GAP IN THIS REPORT AND IT IS AGAINST A COMPANY GUIDE, NOT AN OPINION. | The price hikes are real and confirmed by Kress, but they land in FQ1 FY28, AFTER the trough, and only recover to 72-73% — not 75%. |
| 🔴🔴 NVDA FY28 REVENUE | MANAGEMENT'S IMPLIED ~$694bn IS ~4.4% ABOVE BBG CY2027 OF $665bn (was ~8.4% vs $638bn on the 09:12 pull — the gap HALVED intraday and is now INSIDE this report's own FY≠CY calendarisation error) | Treat the direction as the signal and the magnitude as indicative — and on the 08-27 INTRADAY re-pull the magnitude is only ~4.4%, which the caveats above already account for, so this row can no longer carry the claim that the Street is meaningfully below management. |
| 🔴 NVDA REVENUE PER GIGAWATT | MANAGEMENT'S $40bn (VERA RUBIN) vs THE HOUSE'S ~$25bn | But it does bound the upside: the house's 2027E of ~$25bn/GW implies Vera Rubin is a small share of 2027 GW. Management says Vera Rubin will be ~20% of FQ3 DC revenue and *"the fastest product ramp in NVIDIA's history."* If the mix shifts faster, the house's revenue/GW — and therefore its $661bn — is low. |
| 🔴 NVDA | ~25% OF FY28 REVENUE IS ATTACHED TO CUSTOMERS NVDA IS FINANCING, AND NO BASELINE ON THIS WIKI HAD A NUMBER FOR IT | ~25% OF FY28 REVENUE IS ATTACHED TO CUSTOMERS NVDA IS FINANCING, AND NO BASELINE ON THIS WIKI HAD A NUMBER FOR IT |
| 🔴 META | THE ~$10bn 3Q26 LEGAL ACCRUAL IS ALMOST CERTAINLY NOT IN THE CONSENSUS EPS YET | BUT the direction of travel among the covering houses is the opposite: BOTH maintained targets (BofA BUY PO $810, on 24x 2027E GAAP EPS; Barclays OVERWEIGHT PT $780), i.e. they are treating it as a NON-RECURRING charge and looking through it. The reconciliation item is therefore a MECHANICAL one — watch whether BBG's CY2026 GAAP EPS drops ~$3 while CY2027 is untouched. If CY2027 moves, someone … |
| 🔴 GS INITIATES CXMT AT BUY (TP Rmb129) | THE MOST CONCRETE DRAM-SUPPLY BEAR CASE THIS WIKI HAS, AND IT IS NOT IN ANY MEMORY-PAGE NUMBER | OPEN ITEM for the next pass: does 665k wpm of Chinese conventional DRAM by 2030 change the conventional-DRAM scarcity rent that the HBM pricing debate implicitly assumes? Note the direction — it is the supply answer to the scarcity, and no memory page currently models it. |
| NVDA CAPITAL RETURN | UBS WAS RIGHT ON THE REASON, WRONG ON THE SIZE | "Net of strategic uses" is the operative phrase given the ~$50bn already invested in the labs. There is no BBG consensus line for buyback pace. |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-27.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
