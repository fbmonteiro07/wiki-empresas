# Reconciliation — 2026-08-10 (/run-inbox, scheduled)

_Every NEW quantitative datapoint from the 2026-08-10 ingest, checked against (1) prior wiki comments, (2) Capstone house models (`_data/house.json`, asof 2026-08-10), (3) BBG consensus (`_data/estimates.json`, **asof 2026-08-07**). Split DIVERGES (alpha) vs CONFIRMS._

**BBG column status: AVAILABLE (on-disk snapshot, asof 2026-08-07 — three days stale, 98 companies).** ⚠️ **No fresh Terminal pull was run inside this task, deliberately: refreshing 98 tickers mid-run carries the known partial-drop failure mode (the fetch prints "n/n ok" and exits 0 even when the Terminal dies mid-run, stamping carry-overs with today's asof). The 08-07 snapshot is the wiki's canonical consensus file and is fit for a three-day-old comparison; a refresh is `/wiki-consensus`'s job.** ⚠️ **Standing basis caveat applies to every CY2026 figure below: the CY sums embed PRE-PRINT consensus for already-reported quarters, so CY2026 understates beats. CY2027 is clean (all quarters forecast) and is the column to lean on.**

**House-model coverage is 8 names (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM).** Of the 25 pages patched today, only 4 have a house model — so the house column is marked **n/a** rather than silently skipped on the other 21.

---

## 🔴 DIVERGES — the alpha

### 1. SKHYNIX — TWO CONSENSUS VENDORS DISAGREE BY 26% ON 2027, AND UBS'S "12% ABOVE CONSENSUS" CLAIM INVERTS ON OUR OWN DATA

| | FY/CY2026 EPS (KRW) | FY/CY2027 EPS (KRW) |
|---|---|---|
| **UBS (new, 2026-08-07)** | **390,164** (was 396,943, −1.7%) | **547,875** (was 576,936, −5.0%) |
| **Consensus UBS cites** (Visible Alpha, per the note) | 347,486 | **462,067** |
| **BBG consensus (wiki, asof 08-07)** | 318,472 | **580,750** |
| House model | n/a | n/a |

🔴 **THE FINDING: UBS says it is "12% ABOVE '27E CONSENSUS, WHICH WE BELIEVE HAS NOW FACTORED IN LTA ADJUSTMENTS." Against the BBG consensus this wiki actually carries, UBS is 5.7% BELOW.** The two "consensus" figures for the same year differ by **26%** (462,067 Visible Alpha vs 580,750 BBG).
- ⚠️ **This is a data-integrity flag before it is a stock call, and it matters because the wiki's per-page consensus snapshots are BBG.** Anyone reading `SKHYNIX.md` sees a BBG CY2027 EPS materially above UBS's "above-consensus" number. **Do not restate UBS's "+12%" on this page without naming the vendor.**
- ⚠️ **Bases checked before flagging: CY2027 is the clean column (all four quarters forecast, no pre-print contamination), and SK Hynix is a December FYE so FY≈CY. So the gap is NOT a fiscal-calendar artifact.** The likely driver is LTA treatment — UBS explicitly says Visible Alpha "has now factored in LTA adjustments" while BBG's contributor set may not have, which would make the BBG number the STALER of the two despite being higher.
- **Actionable:** the direction of the next consensus revision is the trade. If UBS is right that LTAs cap ASPs, BBG's 580,750 has ~20% of downside to Visible Alpha's level — on a stock already **−49% from its 22 June peak** at 1.80x NTM P/BV. **A "cheap on BBG numbers" screen on this name is reading the wrong consensus.**
- **Prior wiki:** consistent with the page's existing "extraordinary 3x spread" observation on targets (KIS KRW 4.7m vs BNK KRW 1.48m). The estimate dispersion now matches the target dispersion.

### 2. AAOI — WOLFE'S "WE ARE FAR BELOW THE STREET" WAS ALREADY STALE WHEN IT PUBLISHED, AND CONSENSUS SITS BELOW THE COMPANY'S OWN GUIDE

| | Q3-26 rev | CY2026 EPS | CY2027 EPS |
|---|---|---|---|
| Company guide (08-05/06) | **$273M** (midpoint) | — (FY26 rev "$1.1B unchanged") | — |
| **Wolfe (new, 08-06)** | — | **$0.62** | **$3.60** |
| Consensus Wolfe cites (pre-print) | $278M | $1.03 | $5.00 |
| **BBG consensus (wiki, asof 08-07)** | **$266.5M** | **$0.69** | **$4.70** |
| House model | n/a | n/a | n/a |

🔴 **TWO DIVERGENCES, AND THEY POINT OPPOSITE WAYS:**
- **(a) Wolfe's differentiation has mostly evaporated.** The note frames itself as far below the Street ($0.62 vs $1.03 on 2026; $3.60 vs $5.00 on 2027). Against BBG one day later the gaps are **$0.62 vs $0.69** and **$3.60 vs $4.70** — consensus already collapsed toward Wolfe post-print. ⚠️ **Wolfe's cited consensus is PRE-PRINT. The wiki should carry the note's ANALYSIS (the 26.9% ex-one-off gross margin, the physical de-risking of the Q3 ramp) and NOT its "vs consensus" framing.**
- **(b) 🔴 THE MORE INTERESTING ONE: BBG's Q3 consensus of $266.5M is BELOW the company's own $273M guide midpoint, and CY2026 revenue consensus of $1,046M is ~5% BELOW the reaffirmed "$1.1B" target.** The Street is explicitly not underwriting management's own numbers. **That is the setup: a company reaffirming $1.1B while consensus sits at $1.046M and Wolfe's own conclusion is "they are effectively underwriting a >$500M quarter" in Q4.** The Q3 print is the referee, and the bar is now BELOW the guide — which cuts bullish on the reaction function even if the bear is right on execution.
- **Prior wiki CONFIRMED:** the page's 20-40% unfilled-demand datapoint and the "capacity-gated, not demand-gated" framing are untouched — Wolfe independently says "demand is NOT a problem." The disagreement is entirely about conversion.

### 3. LITE — AT THE HOUSE'S OWN EPS AND JEFFERIES' OWN MULTIPLE, THE STOCK IS ~48% ABOVE FAIR

| | 2027 EPS | Implied at 20x (Jefferies' stated analog for the name) |
|---|---|---|
| **Capstone house model** (`Modelo consolidado incl. LITE`, 2026-06-16) | **$30.02** | **~$600** |
| BBG consensus CY2027 (asof 08-07) | $23.96 | ~$479 |
| The number Jefferies says the market "threw out" | ~$50 | ~$1,000 |
| **Spot (BBG file, 08-07)** | | **$886.35** |

🔴 **THE FINDING, and it uses only numbers we already own: Jefferies' framing is that "$50 OF EARNINGS, 20 TIMES, THAT'S A THOUSAND — stock got to a thousand, IT HAD NO PLACE TO GO. AT 600, YOU COULD BE LIKE, ALL RIGHT, NOW THERE'S A LOT OF UPSIDE." Our own house model is $30.02, which at his 20x is ~$600 — precisely the level he calls attractive. The stock is at $886.**
- ⚠️ **Basis caution, stated because it bounds the conclusion: Jefferies does not date his "$50 of earnings" (LITE has a June FYE, so a CY2027 house figure and an unstated FY basis are not strictly comparable), and 20x is his descriptive multiple for the peak narrative, not a published target — no PT is given on the call.** So treat this as a triangulation, not a valuation.
- **Actionable read:** the house model is 25% ABOVE BBG CY2027 consensus and still implies the stock is expensive on the analyst's own multiple. **The bull case at these prices requires the ~$50 number, which is 2.1x BBG consensus and 1.7x our own model.** That is the specific thing to underwrite or reject into the print — and Jefferies' new MPO/laser-content risk (management says content is unchanged, he doubts it) attacks exactly the revenue line that gets you from $30 to $50.

### 4. COHR — OUR HOUSE MODEL IS 92% ABOVE CONSENSUS AND IS BUILT ON THE ANALYST WHO NOW PREFERS THE OTHER NAME

| | 2027 EPS | 2028 EPS |
|---|---|---|
| **Capstone house model** (`Modelo COHR.xlsx`, 2026-05-26 — source line: **"Built on Jefferies/Blayne Curtis"**) | **$19.21** | **$23.60** |
| BBG consensus CY2027 (asof 08-07) | **$10.00** | n/a in file |
| Spot (08-07) | $377.48 | |

🔴 **THE FINDING IS A PROVENANCE PROBLEM, NOT A NUMBER PROBLEM: the house COHR model is explicitly built on Blayne Curtis's work, and the note ingested today has Curtis (a) preferring [[LITE]] over COHR, (b) reducing the entire COHR-outperformance case to ONE condition ("if they show outperformance versus Lumentum, IT'S ON 6-INCH SUPPLY"), and (c) noting that relative trade "has been tried THREE TIMES AND IT HASN'T WORKED."**
- ⚠️ **Our model sits 92% above BBG CY2027 consensus while its source analyst is not the marginal bull on the name.** That does not make the model wrong — it means **the model's key sensitivity is now identified and dated: 6-inch InP supply, testable at next week's print.**
- **Action:** re-run the COHR model's 6-inch assumption explicitly, and if it is the load-bearing input, mark it as such in the model. Also note COHR carries the group's largest China-manufacturing exposure per the same call ("most of the non-Chinese companies still build in China, PARTICULARLY COHERENT") against a transceiver-ban headline Curtis calls an overreaction — a second unmodelled tail.

### 5. MCHP — THE BEAR USES THE HIGHER EPS AND THE BULL USES THE LOWER ONE. THE ENTIRE DISAGREEMENT IS THE MULTIPLE

| | EPS basis | Multiple | Target |
|---|---|---|---|
| **Jefferies (new, 08-07) — BEAR** | **$5.00** ("next year's number") | **20x** (a DISCOUNT to the 20-25x analog band, "Microchip's been undergrowing") | **$100** |
| GS · Schneider (08-06) — BULL | $4.50 (normalized) | 26x (a PREMIUM) | $115 |
| **BBG consensus CY2027 EPS (asof 08-07)** | **$4.42** | — | — |
| Spot (08-07) | $84.04 | | |

🔴 **THE FINDING: the bear's earnings number is 13% ABOVE BBG consensus and 11% above the bull's; the bull's is in line with consensus. Neither side is arguing about earnings — the $15 of target separation is 100% multiple.** ⚠️ **That makes the MCHP debate un-resolvable by the next print's EPS and resolvable only by whether the market grants a recovered-but-undergrowing analog franchise a premium or a discount. Log it as a re-rating question, and stop treating MCHP beats as thesis-relevant.**
- **Prior wiki:** this now sits directly against the margin-driven bull rows of 08-06, and Jefferies' challenge to the print itself ("gross margins had a lot of like ONE-TIMERS in there") is the falsifiable part — check FQ2 gross margin ex-items.

### 6. SPCX — THE LEASE RATES ARE 2-8x BELOW WHAT THE SAME GPU EARNS SERVING TOKENS, AND NEITHER SIDE IS IN ANY MODEL WE HOLD

| Same hardware, different use | Earnings per GPU-hour | Source basis |
|---|---|---|
| SPCX lease to ANTHROPIC | **$7.80** | **CONTRACTED** — cited to the SpaceX S-1 |
| SPCX lease to GOOG | **$11.50** | **CONTRACTED** — cited to the Google agreement |
| Serving Kimi K3 — agentic | $23 | MODELLED gross revenue at published API pricing, unstated utilisation |
| Serving Kimi K3 — chatbot | $60 | same |

🔴 **DIVERGES against this wiki's own SPCX bull case, which rests on a PREMIUM ("value-based pricing," "$30-50M/MW/year," "industry-high pricing," "payback in less than a year"). On these marks the landlord leg with the two largest disclosed counterparties clears at the LOW end.** Two readings, both live: an unexploited margin pool no model on the page includes, **or** evidence the merchant economics do not survive at scale.
- ⚠️ **NO-NETTING RULE ENFORCED: $/GPU-hour and $/MW/year are different bases and were NOT converted (the `assumptions.md` per-chip-vs-per-watt rule). SemiAnalysis's $30-50M/MW/year (08-07) stands unchanged.**
- ✅ **CONFIRMS New Street (Ferragu, 07-30):** the "spot-vs-planned compute arb" told per-chip — the Anthropic relationship is the LOW end of realised pricing.
- 🔴 **NET-NEW: the GOOGLE agreement prices ~47% ABOVE the Anthropic lease — and it is the same contract carrying the 9/30 delivery deadline the page tracks as the nearest hard test.** Testable against the next compute-segment revenue-per-GW disclosure.

### 7. NVDA — A SOFTWARE RESULT DEFENDS THE LATENCY FLANK AND CANNIBALISES NVIDIA'S OWN LPU LINE. NO CONSENSUS NUMBER MOVES

| | 2027 |
|---|---|
| **Capstone house model** | rev **$661bn**, EPS **$15.44**, GM 74%, OPM 94% |
| BBG consensus | CY2027 not directly comparable in file (FY basis) — no change implied |

⚠️ **DIVERGES as an unpriced structural item, not as an estimate revision: TileRT puts an 8×B200 node at 340 tok/s/user for $13.56/M output tokens (1% above the best conventional FP4 cost at 1.9x the interactivity). It attacks the ultra-low-latency TAM that NVIDIA NOW SELLS INTO ITSELF — the note references "NVIDIA Groq LPUs" and quarter-by-quarter "NVIDIA LPU30, LPU40" shipment estimates. Nobody in the note names the conflict.**
- **Neither the house model nor consensus breaks out an LPU line, so there is nothing to reconcile numerically — which is exactly the point: a product line material enough for SemiAnalysis to model quarterly is invisible in every number we hold.** Action: ask whether LPU is inside the house model's Data Center line at all.
- ✅ **CONFIRMS the house's high-GM structure indirectly:** the result is GPU-positive (fungibility, "rebalance in software"), so the flank defence is a support for the merchant-GPU thesis, not a threat to it.

### 8. LRCX / SNDK — THE SAME $40BN IS BOTH THE BEAT AND THE NEXT DOWNCYCLE, AND CONSENSUS DOES NOT CARRY THE BULL EPS IT IS BEING ARGUED AGAINST

| SNDK | CY2026 EPS | CY2027 EPS |
|---|---|---|
| **BBG consensus (asof 08-07)** | **$149.38** | **$237.45** |
| The "$300-500 of earnings" Jefferies says will "never" get credit | — | **$300-500** |

⚠️ **CALIBRATION, and it defuses part of the argument: the $300-500 EPS bull case Jefferies is attacking is NOT in BBG consensus, which sits at $237 for CY2027. He is arguing against a buy-side narrative, not against published numbers.** The PT cut is real; the earnings ceiling he is puncturing was never in the Street's model.
- 🔴 **THE GENUINE DIVERGENCE IS ON SUPPLY, AND IT IS CROSS-NAME: "[[LRCX]] TALKED ABOUT $40 BILLION AND THEN THEY SAID IT'S ALL HAPPENING… A YEAR OR TWO EARLIER… I'M ASSUMING THAT'S THE KOREANS."** The same NAND spend that produced Lam's "billion dollar beat and raise" is the mechanism of the next oversupply — **a supply-response signal read off the EQUIPMENT layer rather than off memory-maker guidance.** BBG carries LRCX CY2027 EPS at $10.61 with no visible haircut for a pulled-forward NAND cycle.
- ⚠️ **Prior wiki tension retained, not resolved: SKHYNIX's ~$38-39bn Korean commitment is long-dated (first cleanroom June 2029, WFE 2031) and is NOT supply relief inside 2026-28, while the equipment layer says capacity is arriving NOW. Both stand.**

### 9. AAOI / SNDK / MCHP / TXN / ON / KLAC — no house model exists

⚠️ **Six of today's most-patched names have no Capstone model (`house.json` covers 8 names, none of them these). The house column above is honestly blank rather than proxied.** ✅ **Worth flagging as a coverage gap: AAOI now has an institutional rating and a testable Q3 ramp, and SNDK has a live PT action — both are model-able and neither is modelled.**

---

## ✅ CONFIRMS

1. **AVGO — the house already underwrites the story Jefferies says is the catalyst.** He says "it's really about '28 for Broadcom, which will be MORE OF A FALL OR LATE FALL STORY." **House model 2028 EPS $35.96** vs 2027 $21.07 — i.e. the house is carrying a +71% 2028 step. BBG CY2027 EPS $21.21 is in line with house $21.07 (0.7% apart), so the divergence is entirely in the out-year the analyst says the market has not engaged with yet. **Nothing to reconcile; the positioning and the model agree.**
2. **SKHYNIX capital return — the company confirmed the timing the desk was waiting for.** BofA's "50% of FCF, W40tn+ buyback vs W20tn+ dividend" (08-06/07) and UBS's "Won12tn 2H26 buyback, path to 50% of FCF" (08-07) now sit behind a company disclosure that an announcement comes **within 3Q26**. **Two houses, one company statement, same direction.**
3. **HBM de-spec — three independent routes, one conclusion.** UBS's unit math (de-spec + MORE units = supply-rationed BOM), SK Hynix management ("if it was to occur it would reflect SUPPLY SHORTAGE, not a change in demand"), and the page's prior GFHK/@jukan05 8-Hi report all agree. **The 12-Hi question is closed.**
4. **AAOI Q3 800G ramp — two source classes, one number.** Wolfe (+5x q/q, ~$64M, "lines installed and producing units today… quals ARE DONE") and Crux Capital's buy-side write-up ("should grow nearly 5x," implying ~$60-65M) independently agree. **The strongest 2H26 evidence the page holds.**
5. **AMAT into the print — a clean, dated bogey now exists.** Jefferies: "their print next week should be CLOSER TO LAM." **BBG consensus for the quarter: rev $9,013M, EPS $3.42.** A Lam-quality result means a beat against that. **Scoreable on the day, against the MS Equal-Weight row on the page.**
6. **Token-price elasticity vs the wiki's standing price-cut argument.** Exponential View's "every 10% reduction in token price drives a 12-18% increase in token consumption" (elasticity 1.2-1.8, ELASTIC) is directionally consistent with everything on `tokenmaxxing`. ⚠️ **Basis unstated — explicitly NOT promoted to `assumptions.md` until a second independent source corroborates it.**
7. **SPCX memory-as-binding-constraint.** The page's 08-05 machine-translated Musk quote ("memory output +20%/yr against demand +200%") is corroborated in an English sell-side note by Jefferies (08-07). **Same claim, independent route.**

---

## Open items carried forward

1. 🔴 **Resolve the SKHYNIX consensus-vendor gap (BBG CY2027 580,750 vs Visible Alpha 462,067).** Until then, do not quote UBS's "+12% vs consensus" on the page without naming the vendor. Candidate for `/wiki-consensus`.
2. 🔴 **SNDK's Jefferies PT is KNOWN-STALE** — "cut pretty heavily," no number given on the call; the page still shows the desk's BUY / TP $3,000 (08-05), flagged in place. Resolve against the published note.
3. **COHR house model: mark the 6-inch InP assumption as the load-bearing input** and re-test it after next week's print.
4. **Ask whether the house NVDA model contains any LPU line at all** — SemiAnalysis models LPU30/LPU40 shipments quarterly; we carry no such line.
5. **Model coverage gap:** AAOI, SNDK, MCHP, TXN, ON, KLAC all patched today with no house model.
6. ⚠️ **`CEREBRAS.md`'s intra-quarter window header still reads "May 06 → Jul 09, 2026" and is stale** — left for `/wiki-lint`.
7. **BBG snapshot is 3 days old (asof 2026-08-07).** Next `/wiki-consensus` should refresh and re-run items 1 and 2 above.
