# Edge tracker — house vs Street

_Generated 2026-08-18 · the standing view of where our model and the curated reconciliation runs disagree with consensus. Divergence = candidate alpha; agreement is noise. Rebuild: `py _wiki/_tools/build_edge.py`._

> ⚠️ Programmatic rows are auto-computed (house.json vs estimates.json, USD names only) — **verify the basis before trading** (revenue gross/net/TAC differences can masquerade as edge). Curated rows below are analyst-vetted.

## Programmatic — house vs consensus (|Δ| ≥ 15%)

| Ticker | Metric | Yr | House | Consensus | Δ |
|---|---|---|--:|--:|--:|
| COHR | EPS | 2027 | 19.21 | 11.66 | +65% |
| COHR | Revenue $bn | 2027 | 16.60 | 12.60 | +31% |
| NVDA | EPS | 2027 | 15.44 | 12.95 | +19% |
| GOOG | Revenue $bn | 2026 | 505.00 | 426.90 | +18% |
| GOOG | Revenue $bn | 2027 | 641.00 | 544.40 | +18% |
| NVDA | Revenue $bn | 2027 | 661.00 | 571.00 | +16% |
| AAPL | EPS | 2026 | 10.12 | 8.76 | +16% |

## Curated divergences — latest reconciliation (`reconciliation-2026-08-17-night.md`)

| Name | New datapoint | Read (the edge) |
|---|---|---|
| 🔴🔴 DELL | Morgan Stanley is +26.0% above consensus on EPS and its price target is 14.7% BELOW the consensus target. Both houses raised the numbers and neither will pay for them — and neither does the Street. | Morgan Stanley is +26.0% above consensus on EPS and its price target is 14.7% BELOW the consensus target. Both houses raised the numbers and neither will pay for them — and neither does the Street. |
| 🔴 LITE | the first FILED full-year OCS number, and the ramp is already guided, not merely relayed. Skepticism moves off the relays and onto the $400m. | the first FILED full-year OCS number, and the ramp is already guided, not merely relayed. Skepticism moves off the relays and onto the $400m. |
| 🔴 SPCX | DB is +11.1% above consensus on 2027 revenue, but the EPS gap is a basis question, not an edge, and capex now has three incompatible bases. | DB is +11.1% above consensus on 2027 revenue, but the EPS gap is a basis question, not an edge, and capex now has three incompatible bases. |
| 🔴 HPE | an upgrade with a price-target cut, and MS is +11.7% above consensus on the fiscal year it is valuing. | an upgrade with a price-target cut, and MS is +11.7% above consensus on the fiscal year it is valuing. |
| 🔴 AVGO | Epoch reconciles to the dollar with what the page already held, but it adds a timing and seniority shape that no estimate carries. | Epoch reconciles to the dollar with what the page already held, but it adds a timing and seniority shape that no estimate carries. |
| 🔴 INTC | the ">97% EMIB-T yield" claim has no stated process step, and every other mark on the wiki that does name one is 50–92%. | the ">97% EMIB-T yield" claim has no stated process step, and every other mark on the wiki that does name one is 50–92%. |
| 🔴 CoWoS 2027 growth | ~2.5x apart between houses, and internally inconsistent inside Mizuho's own numbers. | ~2.5x apart between houses, and internally inconsistent inside Mizuho's own numbers. |
| 🔴 The relay arrived first and inverted the sign | on two pages at once. | on two pages at once. |
| 🔴 TrendForce contradicts TrendForce on 2027 DRAM | same house, 12 days, opposite sign — while staying consistent on NAND. | same house, 12 days, opposite sign — while staying consistent on NAND. |
| 🔴 CIEN | the scale-across anchor adopted 24 hours earlier measures a different thing. | the scale-across anchor adopted 24 hours earlier measures a different thing. |
| 🔴 — | Two unexplained Mizuho PT moves, same pattern as a prior instance. | Two unexplained Mizuho PT moves, same pattern as a prior instance. |
| 🔴 Fabrinet | a relay of the SAME print already on the wiki is measured on a taxonomy the company retired in that very report. | a relay of the SAME print already on the wiki is measured on a taxonomy the company retired in that very report. |
| 🔴 Two independent merchant CW-laser entrants land in the same quarter | the moat holds through CY27 and breaks on price, not volume, in 2028. | the moat holds through CY27 and breaks on price, not volume, in 2028. |
| 🔴 — | The EML→SiPho pivot partially nets the InP-scarcity thesis against the SiPho-share thesis. Three agents reached this independently. | The EML→SiPho pivot partially nets the InP-scarcity thesis against the SiPho-share thesis. Three agents reached this independently. |
| 🔴 Anthropic's datacenter debt per MW is bimodal | the blended average is not a usable build anchor. | the blended average is not a usable build anchor. |
| 🔴 Cursor's token routing is a quantified threat to frontier-lab API revenue | and it now sits inside a competitor. | and it now sits inside a competitor. |
| — | Mizuho's CSP capex was raised AND re-labelled in five weeks, and its RPO growth rate is internally inconsistent. | Mizuho's CSP capex was raised AND re-labelled in five weeks, and its RPO growth rate is internally inconsistent. |
| — | Un-scored and newly-contested marks worth tracking | Un-scored and newly-contested marks worth tracking |

## Consensus PT vs spot — live pull in `reconciliation-2026-08-17-night.md` (upside ranked)

| Ticker | Spot | Cons PT | Upside | Read |
|---|--:|--:|--:|---|
| MU | 940 | 1,586 | +69% | 🔴 **Largest consensus upside in the entire run — and Mizuho's "no-drift" reiteration is 13.3% BELOW the Street's target.** The 07-11 reiteration was logged as ✅ CONFIRMS on the grounds that it had not moved; the PT layer shows what standing still cost. Consensus CY27 EPS **$163.61 unchanged to the decimal**, so this is not an estimate disagreement — the Street simply pays more for the same number. Reads into ⑧: the house carrying the **+70–100% HBM4e pricing** call also has the lowest target on the name that would capture it. |
| SPCX | 142 | 221 | +56% | 🔴 **This is the resolution that most changes item ③.** DB's $235 is barely above the Street's $221.09, and DB's 2027 revenue of **$115,308m sits 26.8% BELOW the street-high of $157,527m** — so DB is **between median and high, not an outlier**. The +11.1% revenue divergence is real but **mid-range**, and should not be traded as an aggressive call. Lowest rating conviction of the bullish cluster (4.46/5) on a 39-rec sample. ⚠️ The EPS sign conflict (DB +$1.06 vs consensus −$0.94 for CY2026) is **untouched by this pull** — still a basis question. |
| AVGO | 379 | 531 | +40% | ✅ **CONFIRMS — Mizuho's $530 is the consensus target to within 18 cents.** No PT edge either way. The finding in ⑤ was never a PT call: the **$29bn maximum contingent exposure = 15.2% of consensus CY2027 revenue ($190,743m, unchanged to the decimal)** and appears in neither the house nor the Street number. **A $531 consensus target that does not price a 15%-of-revenue second-loss exposure peaking mid-2027 is the finding**, and the fresh pull leaves it exactly as stated. |
| NVDA | 220 | 304 | +38% | ✅ **CONFIRMS row 1 holds on fresh data — the consensus PT is $303.71, IDENTICAL TO THE CENT to the 08-17 live pull**, while spot fell 2.4%. Highest-rated name in the run (4.88/5 on the deepest sample, 81 recs). Mizuho's $300 remains a reiteration sitting on consensus. **Nothing to re-place.** |
| SNDK | 1,634 | 2,196 | +34% | 🔴 **The largest below-Street gap in the run, and it quantifies ⑪.** Mizuho cut $2,200 → $1,900 with no model work; the Street's target is **$2,196.10 — i.e. essentially Mizuho's OLD number ($2,200, −0.2%).** So the un-rationalised cut moved Mizuho from *on consensus* to *13.5% below it*. Consensus CY27 EPS **$238.25 unchanged to the decimal** — the Street did not follow. **The new $1,750–$1,900 rungs are Mizuho's alone.** |
| AMD | 478 | 624 | +31% | 🔴 **Same pattern as SNDK, same house, same note — quantified.** The unexplained $615 → $580 cut lands **7.1% below** the Street's $624.40, and consensus CY27 EPS is **$15.30 unchanged to the decimal**. Mizuho's old $615 was itself only −1.5% vs today's consensus PT. **Two un-rationalised cuts in one note, both taking the house from consensus to below it.** |
| LITE | 876 | 1,130 | +29% | ✅ **PT is consensus (+0.9%) — so item ② is entirely an estimates-and-disclosure finding, not a price call.** ⚠️ **Worth flagging: spot fell 9.6% overnight** (968.90 → 875.88), the second-largest drop in the table, on the session *after* the FY26 10-K disclosed the >$90.0m OCS year and the **$757.8m of early convertible conversion requests**. Consensus CY27 EPS **$27.95 unchanged**, so the Street has not re-cut numbers — **the tape moved before the estimates did.** The **F1Q27 OCS ≥$100m** pass/fail stands. |
| HPE | 55 | 68 | +24% | ✅ **CONFIRMS on the PT leg, and it re-frames ④.** MS's upgrade target of $69 is **the consensus target (+0.7%)** — so the EW→OW upgrade is a **convergence to where the Street already was**, not a contrarian call. 🔴 **The EPS leg still DIVERGES but with a ceiling now attached:** MS's FY27 EPS of **$4.58 is +11.7% above the consensus $4.10 but −0.9% BELOW the street-high of $4.62** — MS is *at the top of the range, not beyond it*. |
| INTC | 96 | 119 | +24% | 🔴 **The only sub-4 rating in the run (3.61/5) — by far the weakest Street conviction**, and the third Mizuho mark landing below consensus. The $109 reiteration that "retroactively firms" the 08-09 cut from $135 sits **8.3% under** the Street's $118.90; the old $135 was **+13.5% above** today's consensus PT. Consensus CY27 EPS **$2.02 unchanged to the decimal** on a **54.0x** multiple. **Reads with ⑥: the house making the un-sourced ">97% EMIB-T yield" claim is also the most bearish on the target.** |
| STX | 908 | 1,113 | +23% | ✅ **The absence of a restated PT was correctly not read as a change — and the standing $1,035 is now 7.0% BELOW consensus.** Spot fell **8.7%** overnight, so the standing target's upside widened from +4.0% to **+14.0% on price alone**. Consensus CY27 EPS **$45.50 unchanged**. **"Top Pick reiterated" is, against the Street's own target, a below-consensus mark.** |
| CRDO | 248 | 296 | +20% | ✅ **PT effectively consensus (−2.1%), on the second-highest rating in the run (4.87/5).** ⚠️ **Biggest overnight price move in the table: −12.5%** (282.82 → 247.59), so the Mizuho reiteration's upside widened from +2.5% to **+17.1% on price alone**. Consensus CY27 EPS **$8.77 unchanged to the decimal**. The **unmodelled "ALC/microLED" leg** from ⑭ remains unsized and is a question for the print. |
| DELL | 461 | 504 | +9% | 🔴🔴 **THE RESOLUTION OF ITEM ①, and it lands on the stronger side. MS's $430 is 14.7% BELOW the consensus PT of $504.04 — genuinely below-Street, not merely below-spot.** And **DELL's +9.3% consensus upside is the LOWEST in the entire 12-name table** (next lowest is CRDO at +19.7%, i.e. DELL's is less than half), on the second-weakest rating (4.32/5). **So the Street as a whole is the least willing to pay up for DELL of any name in this run — which corroborates the "numbers up, multiple down" mechanism rather than softening it.** Mizuho's $500 is the consensus target (−0.8%). 🔴 **But the EPS leg cuts the other way — see item ① below.** |
