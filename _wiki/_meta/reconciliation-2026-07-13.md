# Reconciliation — 2026-07-13

_Variance pass on the NEW quantitative datapoints from the 2026-07-13 run-inbox (5 unique sell-side notes: Mizuho DC-Capex 07-11, MS/Nowak Internet-Capex 07-12, JPM Server-CPU 07-12, MS/Marshall Scale-Up 07-13, BofA/Arya Core-Wars 07-13) against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

> **BBG consensus = PENDING.** Bloomberg wrapper returned HTTP 503 (Terminal not logged in / VPN down) at run time. On-disk baselines done below; re-run `/wiki-consensus` once the Terminal is back to fill the BBG column. Web data was NOT substituted for consensus.

---

## DIVERGES — the alpha

| Name | New sell-side mark | Prior wiki | House model | BBG | Read / action |
|---|---|---|---|---|---|
| **INTC** | **BofA (Arya) flips to Buy, PO $160** (2026-07-13); Mizuho Neutral $135 (07-11) | BofA was **Underperform $96** (now → Changelog) | (no INTC house model) | PENDING | **Biggest thesis shift of the run.** A two-notch BofA reversal on stronger PC/server pricing + Products OpM +~600bps + 18A-P/14A foundry traction — even while BofA models INTC server share *falling* 41%→24% by CY30. Rating-vs-fundamentals tension worth pressing: the Buy is a pricing/margin/foundry-option call, not a share call. Mizuho ($135 Neutral) is the more cautious anchor. **Verify the Buy against the underlying PDF** (inferred from disclosure code C-1-9; QCOM's B-3-7=U/P cross-checks the mapping). |
| **COHR** | MS (Marshall/Moore) 2028E revenue ~**$12.86bn** (07-13) | prior MS-based build on page | House **CY28E rev $19.6bn**, PF EPS $23.60 (`Modelo COHR`, 2026-05-26) | PENDING | **House is ~50% above MS on COHR '28 revenue** ($19.6bn vs $12.86bn). Either the house 800G/1.6T ramp is too steep or MS is under-modeling the scale-up optical pull it just turned more constructive on. Material — reconcile the house COHR model's CY28 ramp vs MS's rebuilt CPO-adoption model. |
| **ARM** | BofA Neutral, **PT $245 → $460** (07-13); Mizuho OP $500 (07-11) | BofA $245 (now → Changelog) | (no ARM house model) | PENDING | **~2x PT hike while holding Neutral** = classic rating-vs-PT tension (BofA sees ~50% CPU value-share by CY30 / AGI demand >$2bn FY27-28 vs ~$1bn supply, but valuation caps the rating). Mizuho Outperform $500 is the more directional call. JPM's ~90% AI-head-node / ~43%-blended-by-'28 share frame underwrites the bull. |
| **MU** | Mizuho OP **$1,375** (07-11) | Mizuho **$1,150** (2026-05-27, → Changelog) | (no MU house model) | PENDING | +$225 (+20%) PT hike on "memory prices remain elevated" as an AI-capex input. Consistent with the LTA-tightening thesis already on the page (SK Hynix roadshow / Bernstein LTA notes, 07-06/07-09). Confirms direction; magnitude is a new Street data point. |
| **SNDK** | Mizuho OP **$2,200** (07-11) | Mizuho **$1,825** (2026-05-27, → Changelog) | (no SNDK house model) | PENDING | +$375 (+21%) on the same elevated-NAND thesis. New Street-high context; track vs the NAND up-cycle already logged. |
| **CRDO** | Mizuho OP **$290 — new Street high** (07-11) | prior marks below $290 | (no house model) | PENDING | New Street high on the copper-durability + optics-second-engine story (>80% FY27 growth, >$600M optical). Momentum name; flag if fundamentals lag the multiple. |
| **META (capex)** | MS capex '27/'28 **$225bn/$250bn** (07-12); Mizuho: +7GW/14GW 2027 ⇒ ~$200-300B (07-11) | prior MS $175/$205bn (already drifted by daily ingest) | House capex **$170bn (2027E)** (`Modelo Meta`, 2026-06-11) | PENDING | **House META capex ($170bn '27) sits well below the new Street ('27 $225bn, '28 $250bn).** If the Street ramp is right, house under-models META spend (and the downstream AVGO/NVDA/memory pull). House base PT $688 also below MS $775 (but inside house bull $840). Bridge the house capex line to the announced 14GW-by-2027. |

## CONFIRMS — no action (logged for the record)

| Name | New sell-side mark | House / prior | BBG | Note |
|---|---|---|---|---|
| **NVDA** | Mizuho OP $300 (07-11); BofA Buy $350 reit (07-13); MS Top Pick (07-13) | House rev '27 $661bn, EPS '27 $15.44; GW sold ~24.8 '27 | PENDING | Sell-side PTs ($300-350) and house fundamentals both firmly bullish; content/GW $40→$100bn (Feynman) is directionally consistent with house rev/GW ~$25bn (different metric — chip vs full-system GW). No tension. |
| **AMD** | BofA Buy $620 (from $550); Mizuho OP $615 (07-11) | prior BofA $500 → Changelog | PENDING | Two brokers converge ~$615-620 on MI455X Helios ramp + EPYC share gains. Aligned; no divergence. |
| **AVGO** | Mizuho OP $530 (07-11); MS positive 2027-28 ASIC ramps (07-13) | House AI-semis $132bn '27/$251bn '28, GW 9.9→19.6, EPS PF $21→$36 | PENDING | Sell-side constructive on the exact ASIC/networking ramp the house model already carries aggressively. Confirms. |
| **GOOG** | MS OW $415 (07-12); Mizuho: GOOGL capex +83%/101% (07-11) | House EPS '27 $16.20 (>cons ~$14.5); capex '27 $310bn | PENDING | House already models a steep GOOG capex/TPU ramp; Street capex revisions corroborate rather than contradict. Confirms the house TPU-external-sales thesis (+ve AVGO). |
| **AMZN** | MS OW $330 (07-12); capex $308bn/$318bn '27/'28 | prior MS $330 (reiteration) | PENDING | PT reiterated; capex marks corroborate the hyperscaler-capex theme. |
| **MSFT** | MS OW $650; bull/base/bear $860/$650/$310 (07-12) | prior MS/Weiss $650 (reiteration) | PENDING | Base PT unchanged; only scenario granularity is new. |
| **QCOM** | BofA reiterate Underperform $220 (07-13) | prior BofA U/P (06-25) | PENDING | No change. The bear holdout on DC-CPU optionality ($5bn FY27E DC vs $1.7Tn 2030 TAM hype). |
| **ORCL** | Mizuho OP $320 — new mark (07-11) | first Mizuho mark on page | PENDING | New broker view; neocloud/OCI capex driver ($398B '27/$485B '28 neocloud). No prior Mizuho mark to drift. |
| **CRWV** | Mizuho Neutral $110 — new mark (07-11) | first Mizuho mark | PENDING | New broker view; Neutral despite bullish neocloud-capex backdrop. |
| **TSM** | JPM foundry/OSAT beneficiary (07-12, qualitative) | House EPS NT$143.5 '27, GM ~66% | PENDING | Qualitative read-through (AMD x86 share + AI-accel/ARM CPU). No new number to reconcile. |

---

## Macro read-through (capex convergence)

Two independent shops (MS/Nowak bottom-up, Mizuho/Rakesh consensus-tracking) now land on the **same ~$1.2T/$1.4T hyperscaler capex for '27/'28** and a path to **~120GW by '28** (from ~30 in '25), with cost/GW *rising* ~20% on memory + powered-shell inflation. The house models carry GOOG ($310bn '27) aggressively but **META ($170bn '27) below the Street '28 trajectory** — the single most actionable gap this run for the AI-capex complex. Downstream, this supports the elevated-memory (MU/SNDK/SK Hynix/Samsung) and custom-ASIC (AVGO/GOOG-TPU) legs already in the wiki, and the JPM server-CPU super-cycle (26mn→68mn units '25-'28; ARM ~43% blended by '28) as the newest incremental vector.

_Next: re-run `/wiki-consensus` when the Bloomberg Terminal is back to resolve every PENDING cell (place each PT/EPS vs the consensus median and flag the true Street highs/lows)._
