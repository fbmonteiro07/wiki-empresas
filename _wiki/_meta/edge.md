# Edge tracker — house vs Street

_Generated 2026-07-14 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 9.79 | +96% |
| COHR | Revenue $bn | 2027 | 16.60 | 11.10 | +50% |
| LITE | EPS | 2027 | 30.02 | 23.69 | +27% |
| GOOG | Revenue $bn | 2027 | 641.00 | 512.40 | +25% |
| COHR | EPS | 2026 | 8.27 | 6.80 | +22% |
| GOOG | Revenue $bn | 2026 | 505.00 | 421.00 | +20% |
| NVDA | EPS | 2027 | 15.44 | 12.88 | +20% |
| NVDA | Revenue $bn | 2027 | 661.00 | 561.40 | +18% |

## Curated divergences — latest reconciliation (`reconciliation-2026-07-13.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| INTC | **BofA (Arya) flips to Buy, PO $160** (2026-07-13); Mizuho Neutral $135 (07-11) | **Biggest thesis shift of the run.** A two-notch BofA reversal on stronger PC/server pricing + Products OpM +~600bps + 18A-P/14A foundry traction — even while BofA models INTC server share *falling* 41%→24% by CY30. Rating-vs-fundamentals tension worth pressing: the Buy is a pricing/margin/foundry-option call, not a share call. Mizuho ($135 Neutral) is the more cautious anchor. **Verify the Buy against the underlying PDF** (inferred from disclosure code C-1-9; QCOM's B-3-7=U/P cross-checks the mapping). |
| COHR | MS (Marshall/Moore) 2028E revenue ~**$12.86bn** (07-13) | **House is ~50% above MS on COHR '28 revenue** ($19.6bn vs $12.86bn). Either the house 800G/1.6T ramp is too steep or MS is under-modeling the scale-up optical pull it just turned more constructive on. Material — reconcile the house COHR model's CY28 ramp vs MS's rebuilt CPO-adoption model. |
| ARM | BofA Neutral, **PT $245 → $460** (07-13); Mizuho OP $500 (07-11) | **~2x PT hike while holding Neutral** = classic rating-vs-PT tension (BofA sees ~50% CPU value-share by CY30 / AGI demand >$2bn FY27-28 vs ~$1bn supply, but valuation caps the rating). Mizuho Outperform $500 is the more directional call. JPM's ~90% AI-head-node / ~43%-blended-by-'28 share frame underwrites the bull. |
| MU | Mizuho OP **$1,375** (07-11) | +$225 (+20%) PT hike on "memory prices remain elevated" as an AI-capex input. Consistent with the LTA-tightening thesis already on the page (SK Hynix roadshow / Bernstein LTA notes, 07-06/07-09). Confirms direction; magnitude is a new Street data point. |
| SNDK | Mizuho OP **$2,200** (07-11) | +$375 (+21%) on the same elevated-NAND thesis. New Street-high context; track vs the NAND up-cycle already logged. |
| CRDO | Mizuho OP **$290 — new Street high** (07-11) | New Street high on the copper-durability + optics-second-engine story (>80% FY27 growth, >$600M optical). Momentum name; flag if fundamentals lag the multiple. |
| META(capex) | MS capex '27/'28 **$225bn/$250bn** (07-12); Mizuho: +7GW/14GW 2027 ⇒ ~$200-300B (07-11) | **House META capex ($170bn '27) sits well below the new Street ('27 $225bn, '28 $250bn).** If the Street ramp is right, house under-models META spend (and the downstream AVGO/NVDA/memory pull). House base PT $688 also below MS $775 (but inside house bull $840). Bridge the house capex line to the announced 14GW-by-2027. |

## Consensus PT vs spot — live pull in `reconciliation-2026-07-13.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| _no live pull_ | | | | |
