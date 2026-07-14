# Reconciliation — 2026-07-13

_Variance pass on the NEW quantitative datapoints from the 2026-07-13 run-inbox (5 unique sell-side notes: Mizuho DC-Capex 07-11, MS/Nowak Internet-Capex 07-12, JPM Server-CPU 07-12, MS/Marshall Scale-Up 07-13, BofA/Arya Core-Wars 07-13) against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

> **BBG consensus = PENDING → RESOLVED 2026-07-14.** Bloomberg wrapper returned HTTP 503 (Terminal not logged in / VPN down) at run time on 07-13. On-disk baselines were done then; the BBG column below has now been filled from a live pull (estimates.json asof 2026-07-14 + BEST_TARGET_PRICE via the wrapper). Web data was NOT substituted for consensus.

---

## Where the new data DIVERGES

| Name | New sell-side mark | Prior wiki | House model | BBG (resolved 07-14) | Read / action |
|---|---|---|---|---|---|
| **INTC** | **BofA (Arya) flips to Buy, PO $160** (2026-07-13); Mizuho Neutral $135 (07-11) | BofA was **Underperform $96** (now → Changelog) | (no INTC house model) | Cons PT **$105.99** (spot $106.32). BofA $160 = **+51% above cons**; Mizuho $135 = +27%. | **Biggest thesis shift of the run — and BofA's Buy sits ~50% above the consensus target.** A two-notch reversal on stronger PC/server pricing + Products OpM +~600bps + 18A-P/14A foundry traction — even while BofA models INTC server share *falling* 41%→24% by CY30. The Street median hasn't repriced (spot ≈ cons $106): the Buy is a pricing/margin/foundry-option call, not a share call. Mizuho ($135 Neutral) the cautious anchor. **Verify the Buy against the underlying PDF** (disclosure code C-1-9; QCOM's B-3-7=U/P cross-checks the mapping). |
| **COHR** | MS (Marshall/Moore) 2028E revenue ~**$12.86bn** (07-13) | prior MS-based build on page | House **CY28E rev $19.6bn**, PF EPS $23.60 (`Modelo COHR`, 2026-05-26) | No BBG CY28 line. Cons **CY27 rev $11.07bn med / $12.885bn hi**; cons PT $391.50 (spot $316.25). | **House CY28 $19.6bn is +77% above the cons CY27 median and +52% above the CY27 street-high.** MS's 2028 $12.86bn ≈ the current CY27 street-high — i.e. MS's out-year sits roughly where the Street's high is a full year earlier. No BBG CY28 median to place MS directly, but the house 800G/1.6T ramp runs far above any live BBG line. Reconcile the house COHR CY28 ramp vs MS's rebuilt CPO-adoption model. |
| **ARM** | BofA Neutral, **PT $245 → $460** (07-13); Mizuho OP $500 (07-11) | BofA $245 (now → Changelog) | (no ARM house model) | Cons PT **$305.92** (spot $285.77). BofA $460 = **+50% above cons**; Mizuho $500 = +63%. | **~2x BofA PT hike blows ~50% past the consensus target** while holding Neutral = classic rating-vs-PT tension (BofA: ~50% CPU value-share by CY30 / AGI demand >$2bn FY27-28 vs ~$1bn supply, valuation caps the rating). Mizuho OP $500 the more directional call, also well above cons. JPM's ~90% AI-head-node / ~43%-blended-by-'28 share frame underwrites the bull. |
| **META (capex)** | MS capex '27/'28 **$225bn/$250bn** (07-12); Mizuho: +7GW/14GW 2027 ⇒ ~$200-300B (07-11) | prior MS $175/$205bn (already drifted by daily ingest) | House capex **$170bn (2027E)** (`Modelo Meta`, 2026-06-11) | Cons **CY27 capex $185.2bn med / $358.4bn hi**; cons PT $815.77 (spot $659.95). | **House META capex ($170bn '27) sits ~8% BELOW even the consensus median ($185bn)** — and far below MS ($225bn) and the $358bn street-high. If the Street ramp is right, house under-models META spend (and the downstream AVGO/NVDA/memory pull). House base PT $688 also below cons PT $816. Bridge the house capex line to the announced 14GW-by-2027. |

## CONFIRMS — no action (logged for the record)

_(MU / SNDK / CRDO moved here from DIVERGES on the 07-14 resolution — their Mizuho marks land at/below/≈ the consensus target, so they confirm the Street rather than diverge from it.)_

| Name | New sell-side mark | House / prior | BBG (resolved 07-14) | Note |
|---|---|---|---|---|
| **NVDA** | Mizuho OP $300 (07-11); BofA Buy $350 reit (07-13); MS Top Pick (07-13) | House rev '27 $661bn, EPS '27 $15.44; GW sold ~24.8 '27 | Cons PT **$302.50** (Mizuho ≈ cons; BofA $350 +16%). Cons CY27 rev **$562.9bn** (hi 732), EPS **$12.88** (hi 16.59). | Sell-side PTs bracket cons ($300-350); house rev'27 +17% / EPS'27 +20% above cons, both below the street-high — the standing house-above-Street edge (see 07-10). No tension. |
| **AMD** | BofA Buy $620 (from $550); Mizuho OP $615 (07-11) | prior BofA $500 → Changelog | Cons PT **$526.55** (spot $565.72); both marks ~+17-18% above cons. | Two brokers converge ~$615-620 (~+18% above the cons median; spot already through cons) on MI455X Helios + EPYC share. Aligned; bullish, no cross-source divergence. |
| **AVGO** | Mizuho OP $530 (07-11); MS positive 2027-28 ASIC ramps (07-13) | House AI-semis $132bn '27/$251bn '28, GW 9.9→19.6, EPS PF $21→$36 | Cons PT **$522.77** (Mizuho ≈ cons, +1%). Cons EPS CY26 $13.59 / CY27 **$21.14** (hi 25.34). | House CY27 EPS (~$21) ≈ cons $21.14; sell-side PT ≈ cons. Confirms the ASIC/networking ramp the house model carries. |
| **GOOG** | MS OW $415 (07-12); Mizuho: GOOGL capex +83%/101% (07-11) | House EPS '27 $16.20; capex '27 $310bn | Cons PT **$432.74** (MS −4%). Cons CY27 EPS **$15.78** (hi 17.41); capex **$254bn** (hi 339). | **Fresh cons CY27 EPS is $15.78 — house $16.20 is only +3% above (the "~$14.5" on the page was stale).** House capex $310bn is +22% above the cons median (below the $339bn hi); Street capex revisions corroborate the house TPU ramp. Confirms (+ve AVGO). |
| **AMZN** | MS OW $330 (07-12); capex $308bn/$318bn '27/'28 | prior MS $330 (reiteration) | Cons PT **$315.16** (MS +5%). Cons CY27 capex **$233bn** (hi 278). | PT reiterated ~cons; MS capex ($308bn '27) runs above the cons median and above the $278bn street-high — corroborates (upper-end) the hyperscaler-capex theme. |
| **MSFT** | MS OW $650; bull/base/bear $860/$650/$310 (07-12) | prior MS/Weiss $650 (reiteration) | Cons PT **$559.56** (MS +16%). | Base PT unchanged, +16% above the cons median; only scenario granularity is new. |
| **QCOM** | BofA reiterate Underperform $220 (07-13) | prior BofA U/P (06-25) | Cons PT **$228.66** (BofA −4%). | Bear holdout, PT just below the cons median. No change (DC-CPU optionality skepticism: $5bn FY27E DC vs $1.7Tn 2030 TAM hype). |
| **ORCL** | Mizuho OP $320 — new mark (07-11) | first Mizuho mark on page | Cons PT **$257.17** (Mizuho +24%; spot $129.54). | New broker view, well above the cons median on the neocloud/OCI-capex driver ($398B '27/$485B '28 neocloud). No prior Mizuho mark to drift. |
| **CRWV** | Mizuho Neutral $110 — new mark (07-11) | first Mizuho mark | Cons PT **$141.49** (Mizuho −22%). | New broker view; Neutral and ~22% below the cons median despite the bullish neocloud-capex backdrop. |
| **MU** | Mizuho OP **$1,375** (07-11) | Mizuho **$1,150** (2026-05-27, → Changelog) | Cons PT **$1,567.25** (Mizuho **−12%, below cons**; spot $983.86). Cons EPS CY27 $165.4 (hi 234). | +$225 (+20%) hike on "memory prices remain elevated" — yet **still ~12% below the consensus target**: the Street is already more bullish. Confirms the elevated-memory/LTA thesis (SK Hynix roadshow / Bernstein, 07-06/07-09); a catch-up, not a new Street high. |
| **SNDK** | Mizuho OP **$2,200** (07-11) | Mizuho **$1,825** (2026-05-27, → Changelog) | Cons PT **$2,222.33** (Mizuho **≈ cons, −1%**; spot $1,768). | +$375 (+21%) hike lands right at the consensus median — confirms the elevated-NAND thesis; not above the Street. |
| **CRDO** | Mizuho OP **$290 — "new Street high"** (07-11) | prior marks below $290 | Cons PT **$281.37** (Mizuho **+3%**; spot $244.70). | The "new Street high" is only ~3% above the cons median — the Street is already there. Momentum name (copper-durability + optics 2nd engine, >80% FY27 growth, >$600M optical); flag if fundamentals lag the multiple. |
| **TSM** | JPM foundry/OSAT beneficiary (07-12, qualitative) | House EPS NT$143.5 '27, GM ~66% | No new number (qualitative read-through) | AMD x86 share + AI-accel/ARM CPU tailwind. No datapoint to place vs cons. |

---

## BBG consensus pull

_Live pull 2026-07-14 (BEST_TARGET_PRICE + PX_LAST via the Bloomberg wrapper), upside = cons PT vs spot._

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| **ORCL** | 129.54 | 257.17 | +99% | Mizuho OP $320 above even cons; deepest cons-vs-spot gap on the list (neocloud/OCI capex). |
| **CRWV** | 81.70 | 141.49 | +73% | Cons implies large upside though Mizuho itself is Neutral $110 (below cons). |
| **MU** | 983.86 | 1567.25 | +59% | Mizuho $1,375 sits ~12% BELOW cons — Street already more bullish; elevated-memory thesis. |
| **MSFT** | 386.05 | 559.56 | +45% | MS OW $650 well above cons median. |
| **NVDA** | 209.05 | 302.50 | +45% | Mizuho $300 ≈ cons; BofA $350 +16%. House fundamentals above cons (edge intact). |
| **AVGO** | 396.47 | 522.77 | +32% | Mizuho $530 ≈ cons; house CY27 EPS ≈ cons $21.14. |
| **AMZN** | 245.90 | 315.16 | +28% | MS $330 +5% above cons; capex above the street-high. |
| **SNDK** | 1768.22 | 2222.33 | +26% | Mizuho $2,200 ≈ cons median — elevated-NAND thesis, not above Street. |
| **QCOM** | 182.20 | 228.66 | +25% | BofA Underperform $220 just below cons — the bear holdout. |
| **COHR** | 316.25 | 391.50 | +24% | House CY28 rev far above any live BBG line (no CY28 median). |
| **META** | 659.95 | 815.77 | +24% | House capex $170bn '27 below the cons median $185bn — under-modeled spend. |
| **GOOG** | 355.83 | 432.74 | +22% | MS $415 ~cons; house EPS $16.20 only +3% above fresh cons $15.78. |
| **CRDO** | 244.70 | 281.37 | +15% | Mizuho $290 only +3% above cons — "new Street high" barely above median. |
| **ARM** | 285.77 | 305.92 | +7% | BofA $460 / Mizuho $500 both ~50%+ above cons — Street median lags the hikes. |
| **INTC** | 106.31 | 105.99 | -0% | Spot ≈ cons; BofA Buy $160 (+51%) not yet in the median. |
| **AMD** | 565.72 | 526.55 | -7% | Spot has run through the cons target; BofA $620 / Mizuho $615 ~+18% above cons. |

## Macro read-through (capex convergence)

Two independent shops (MS/Nowak bottom-up, Mizuho/Rakesh consensus-tracking) now land on the **same ~$1.2T/$1.4T hyperscaler capex for '27/'28** and a path to **~120GW by '28** (from ~30 in '25), with cost/GW *rising* ~20% on memory + powered-shell inflation. The house models carry GOOG ($310bn '27) aggressively but **META ($170bn '27) below the Street '28 trajectory** — the single most actionable gap this run for the AI-capex complex. Downstream, this supports the elevated-memory (MU/SNDK/SK Hynix/Samsung) and custom-ASIC (AVGO/GOOG-TPU) legs already in the wiki, and the JPM server-CPU super-cycle (26mn→68mn units '25-'28; ARM ~43% blended by '28) as the newest incremental vector.

_BBG column resolved 2026-07-14 — estimates.json asof 2026-07-14; consensus target prices pulled live via BEST_TARGET_PRICE (Bloomberg wrapper). Marks placed vs the consensus median PT + CY26/CY27 fundamentals (median & `_hi` street-high). Reclassifications: **MU / SNDK / CRDO moved DIVERGES→CONFIRMS** (Mizuho marks at/below/≈ cons target — Street already there); **INTC / ARM** stay DIVERGES (broker PTs ~50%+ above cons); **COHR / META** stay DIVERGES on house-vs-cons (no BBG CY28 line for COHR; house META capex below even the cons median). GOOG cons CY27 EPS updated $14.5→$15.78._
