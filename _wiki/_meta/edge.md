# Edge tracker — house vs Street

_Generated 2026-07-14 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.79 | +96% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.10 | +50% |
| LITE | EPS | 2027 | 30.02 | 23.69 | +27% |
| GOOG | Revenue $bn | 2027 | 641.00 | 512.10 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.80 | +22% |
| GOOG | Revenue $bn | 2026 | 505.00 | 420.90 | +20% |
| NVDA | EPS | 2027 | 15.44 | 12.88 | +20% |
| NVDA | Revenue $bn | 2027 | 661.00 | 562.90 | +17% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-13.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| INTC | **BofA (Arya) flips to Buy, PO $160** (2026-07-13); Mizuho Neutral $135 (07-11) | **Biggest thesis shift of the run — and BofA's Buy sits ~50% above the consensus target.** A two-notch reversal on stronger PC/server pricing + Products OpM +~600bps + 18A-P/14A foundry traction — even while BofA models INTC server share *falling* 41%→24% by CY30. The Street median hasn't repriced (spot ≈ cons $106): the Buy is a pricing/margin/foundry-option call, not a share call. Mizuho ($135 Neutral) the cautious anchor. **Verify the Buy against the underlying PDF** (disclosure code C-1-9; QCOM's B-3-7=U/P cross-checks the mapping). |
| COHR | MS (Marshall/Moore) 2028E revenue ~**$12.86bn** (07-13) | **House CY28 $19.6bn is +77% above the cons CY27 median and +52% above the CY27 street-high.** MS's 2028 $12.86bn ≈ the current CY27 street-high — i.e. MS's out-year sits roughly where the Street's high is a full year earlier. No BBG CY28 median to place MS directly, but the house 800G/1.6T ramp runs far above any live BBG line. Reconcile the house COHR CY28 ramp vs MS's rebuilt CPO-adoption model. |
| ARM | BofA Neutral, **PT $245 → $460** (07-13); Mizuho OP $500 (07-11) | **~2x BofA PT hike blows ~50% past the consensus target** while holding Neutral = classic rating-vs-PT tension (BofA: ~50% CPU value-share by CY30 / AGI demand >$2bn FY27-28 vs ~$1bn supply, valuation caps the rating). Mizuho OP $500 the more directional call, also well above cons. JPM's ~90% AI-head-node / ~43%-blended-by-'28 share frame underwrites the bull. |
| META(capex) | MS capex '27/'28 **$225bn/$250bn** (07-12); Mizuho: +7GW/14GW 2027 ⇒ ~$200-300B (07-11) | **House META capex ($170bn '27) sits ~8% BELOW even the consensus median ($185bn)** — and far below MS ($225bn) and the $358bn street-high. If the Street ramp is right, house under-models META spend (and the downstream AVGO/NVDA/memory pull). House base PT $688 also below cons PT $816. Bridge the house capex line to the announced 14GW-by-2027. |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-13.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| ORCL | 130 | 257 | +99% | Mizuho OP $320 above even cons; deepest cons-vs-spot gap on the list (neocloud/OCI capex). |
| CRWV | 82 | 141 | +73% | Cons implies large upside though Mizuho itself is Neutral $110 (below cons). |
| MU | 984 | 1,567 | +59% | Mizuho $1,375 sits ~12% BELOW cons — Street already more bullish; elevated-memory thesis. |
| MSFT | 386 | 560 | +45% | MS OW $650 well above cons median. |
| NVDA | 209 | 302 | +45% | Mizuho $300 ≈ cons; BofA $350 +16%. House fundamentals above cons (edge intact). |
| AVGO | 396 | 523 | +32% | Mizuho $530 ≈ cons; house CY27 EPS ≈ cons $21.14. |
| AMZN | 246 | 315 | +28% | MS $330 +5% above cons; capex above the street-high. |
| SNDK | 1,768 | 2,222 | +26% | Mizuho $2,200 ≈ cons median — elevated-NAND thesis, not above Street. |
| QCOM | 182 | 229 | +25% | BofA Underperform $220 just below cons — the bear holdout. |
| COHR | 316 | 392 | +24% | House CY28 rev far above any live BBG line (no CY28 median). |
| META | 660 | 816 | +24% | House capex $170bn '27 below the cons median $185bn — under-modeled spend. |
| GOOG | 356 | 433 | +22% | MS $415 ~cons; house EPS $16.20 only +3% above fresh cons $15.78. |
| CRDO | 245 | 281 | +15% | Mizuho $290 only +3% above cons — "new Street high" barely above median. |
| ARM | 286 | 306 | +7% | BofA $460 / Mizuho $500 both ~50%+ above cons — Street median lags the hikes. |
| AMD | 566 | 527 | -7% | Spot has run through the cons target; BofA $620 / Mizuho $615 ~+18% above cons. |
| INTC | 106 | 106 | -0% | Spot ≈ cons; BofA Buy $160 (+51%) not yet in the median. |
