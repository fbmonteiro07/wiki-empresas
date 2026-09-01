# Reconciliation — 2026-08-31 (/run-inbox, scheduled 23h)

_Every NEW quantitative datapoint from this run, placed against three baselines: **(1)** prior wiki marks on the page, **(2)** the Capstone house model where one exists, **(3)** BBG consensus (live — Terminal was up; `bdp` via `E:\bloomberg_api`, pulled 2026-08-31)._

**BBG status: ✅ LIVE.** No PENDING columns this run. Consensus PTs are `BEST_TARGET_PRICE`; consensus EPS are `BEST_EPS` with `BEST_FPERIOD_OVERRIDE` in 1FY/2FY/3FY. ⚠️ Note the wrapper rejects an `overrides={...}` dict — overrides must be passed as **kwargs** (`bdp(tk, flds, BEST_FPERIOD_OVERRIDE='2FY')`). Recorded because the dict form failed with `BAD_ARGS / Invalid override field` on the first attempt.

---

## Where the new data DIVERGES

### 1. 🔴🔴 THE HEADLINE FINDING: Deutsche Bank's "bullish" hardware initiation is BELOW consensus on 5 of its 6 wiki-covered PTs — and its EPS sit ON consensus. It is a MULTIPLE call, not an estimate call.

| Name | DB rating | **DB PT** | **BBG cons. TP** | DB vs cons. | Spot | DB's stated valuation basis | DB implied EPS | **BBG cons. EPS (same yr)** | EPS gap |
|---|---|--:|--:|--:|--:|---|--:|--:|--:|
| [[LITE]] | Buy | **$1,200** | $1,133.81 | 🟢 **+5.8%** | $914.76 | ~27x CY28E P/E | ~$44.4 | 3FY (FY29) $46.91 | ~−5% |
| [[COHR]] | Buy | **$400** | $418.62 | 🔴 **−4.4%** | $277.83 | ~24x CY28 P/E | ~$16.7 | 2FY $14.38 / 3FY $18.66 | ~in line |
| [[ANET]] | Buy | **$220** | $245.00 | 🔴 **−10.2%** | $195.69 | 50/50 FY28E P/E ~35x & EV/uFCF ~34x | ~$6.29 | 3FY **$6.30** | 🎯 **−0.2%** |
| [[CSCO]] | Buy | **$135** | $140.00 | 🔴 **−3.6%** | $110.49 | 50/50 FY27E P/E ~25x & EV/uFCF ~27x | ~$5.40 | 1FY $5.10 | +5.9% |
| [[HPE]] | Buy | **$62** | $68.70 | 🔴 **−9.8%** | $52.24 | 50/50 CY27E P/E ~15x & EV/EBITDA ~10x | ~$4.13 | 2FY **$4.12** | 🎯 **+0.2%** |
| [[DELL]] | Hold | **$480** | $526.94 | 🔴 **−8.9%** | $456.01 | 50/50 CY27 P/E ~22x & EV/EBITDA ~14x | ~$21.8 | 1FY $19.10 / 2FY $23.04 | ~in line |

🔴 **THE CONCLUSION, AND IT IS NOT VISIBLE FROM THE HEADLINES: DB initiates with 5 Buys and language as bullish as anything on these pages (*"silicon cannot lase"*, *"highest conviction"*, *"the champion of the volume AI build out"*) — and then publishes price targets BELOW the Street on every covered name except Lumentum. The reason is arithmetic, not caution about the story: DB's EARNINGS ESTIMATES ARE THE STREET'S (ANET within 0.2%, HPE within 0.2%, DELL and COHR in line, CSCO +5.9%), so the entire PT gap is DB paying a LOWER MULTIPLE than consensus does.** DB says this in its own words for HPE — *"our numbers that are roughly in line with consensus"* — and BBG confirms it name by name.

⚠️ **How to use it: DB is NOT a source of estimate upside on this sector. It is a source of (a) the architecture argument, (b) the channel checks, and (c) a disciplined multiple framework. Anyone reading the initiation as "a new bull on the tape" is misreading it — on price, DB is the most conservative published house on ANET, HPE and DELL of those the wiki tracks.**

🎯 **The one genuine outlier is [[LITE]], the only name where DB is above the Street on BOTH price and multiple.** Prior wiki marks for context: **R&Co Redburn Buy $1,270 (08-17) · DB Buy $1,200 (NEW, #2 on the page) · BofA Neutral $1,100 · MS EW $1,000 (08-24, raised from $900 on 08-03).** DB's $1,200 becomes the second-highest PT on the page and the highest from a house initiating fresh.

### 2. 🔴🔴 [[COHR]] — the HOUSE is +42.9% above consensus AND **+17.0% above the STREET HIGH** on CY28 EPS (re-measured live 2026-09-01). No analyst on the Street is at the house's number. Largest open house-vs-Street gap on the wiki; it needs a bridge.

| CY28E EPS | Value | vs house |
|---|--:|--:|
| **Capstone house model** (`Modelo COHR.xlsx`, 2026-05-26, Jefferies-based) | **$23.60** | — |
| DB implied (PT $400 ÷ 24x) | ~$16.67 | 🔴 **−29%** |
| BBG consensus (interpolating 2FY $14.38 / 3FY $18.66 across a June FY) | ~$16.5 | 🔴 **−30%** |

🔴 **The house is carrying a CY28 Coherent number roughly 40-43% above where both the newest initiating house and the Street sit. That is a big enough gap to be either the position or the error, and it should not sit unexamined.** Note the house model is dated **2026-05-26 and is explicitly "built on Jefferies/Blayne Curtis"** — and Jefferies has since (08-07) turned notably more two-sided on the LITE/COHR pair and flagged the MPO risk to laser content. **Action: re-derive the house CY28 COHR bridge (revenue $19.6bn at ~41% GM) against DB's own build, which reaches only ~$19 of EPS by FY29E on a business it calls capacity-constrained-turning-cash-generative. The disagreement is most likely in the gross-margin path or the CPO/OCS attach, not the transceiver ramp.** ⚠️ **Per the standing rule, do NOT discard either number on plausibility — reconcile first. The house was right and the "implausible" broker model was right on Korea in August; the failure mode runs both ways.**

✅🔴 **RESOLVED 2026-09-01 (`/wiki-consensus`, live ad-hoc `1FY/2FY/3FY` pull) — THE CONSENSUS SIDE OF THIS BRIDGE IS CONFIRMED TO THE CENT, AND THE GAP IS WORSE THAN "~40% vs THE MEDIAN": THE HOUSE IS 17% ABOVE THE STREET **HIGH**.** Coherent's last reported quarter is 2026-06-30, so `1FY` = FY2027 (ending Jun-27), `2FY` = FY2028, `3FY` = FY2029. The 08-31 interpolation is exact:

| CY2028E EPS | Value | vs house $23.60 |
|---|--:|--:|
| **Capstone house** (`Modelo COHR.xlsx`, 2026-05-26, Jefferies-based) | **$23.60** | — |
| **BBG consensus MEDIAN**, ½`2FY` $14.385 + ½`3FY` $18.656 | **$16.52** | 🔴 **house +42.9%** |
| **BBG STREET HIGH**, ½`2FY_HI` $20.40 + ½`3FY_HI` $19.96 | **$20.18** | 🔴🔴 **house +17.0%** |
| DB implied (PT $400 ÷ 24x) | ~$16.67 | +0.9% vs the median — **DB IS the consensus number** |

🔴🔴 **THE SHARPENED FINDING: the house is not merely above the Street's average on Coherent CY28 — it is 17% above the single most bullish mark BBG carries. There is no analyst on the Street at the house's number. That moves this from "a big gap worth bridging" to "the house is outside the entire published range," which is a materially higher bar and confirms this as the largest open reconciliation item on the wiki.**

➤ **Two things the fresh pull adds to the bridge brief: (1) the GM path is the likely culprit — BBG has COHR gross margin at 40.96% (`1FY`) → 41.96% (`2FY`) → 42.91% (`3FY`), i.e. the Street models ~2pp of expansion over three years against the house's ~41% on $19.6bn of revenue, so the disagreement is more likely in the REVENUE/mix line than in margin. (2) The consensus TP is **$418.62** against a **$271.37** spot (+54% implied) with DB at $400 — so the Street is bullish on the STOCK while sitting far below the house on the EARNINGS. If the house's CY28 number is right, the Street's targets are far too low; if the targets are right, the house's EPS is not what is driving them.**

⚠️ **Still not resolved (and not a BBG question): WHY the house is there. The bridge against DB's own build remains the open task — `/wiki-consensus` can only establish where the Street is, which it now has, precisely.**

### 3. 🔴🔴 [[TXN]] — Goldman's SELL is 31.5% below consensus. The single widest single-name PT divergence this run.

| | Value |
|---|--:|
| **GS rating / PT (2026-08-30)** | **Sell, $225** |
| Spot (28-Aug close per GS) | $258.64 |
| Spot (BBG, 08-31) | $260.91 |
| **BBG consensus TP** | **$328.68** |
| GS vs consensus | 🔴 **−31.5%** |
| GS implied multiple on BBG 2FY EPS ($10.28) | ~21.9x |
| Consensus TP implied multiple on same EPS | ~32.0x |

🔴 **GS is publishing a bullish humanoid/physical-AI TAM (raised to ~890k units by 2030 and $138bn by 2035) with [[TXN]] named in three separate BOM lines — and rating the stock a SELL with the lowest PT on the tape. The gap is ~10 turns of multiple, not an earnings dispute.** ⚠️ **This is a clean, dateable disagreement and belongs in the edge tracker: the Street is paying 32x for TI's analog franchise into an AI/robotics content story; GS says 22x. Nothing in this run resolves it.**

### 4. 🔴🔴 [[NOW]] — Wells Fargo's $175 is 23% above a consensus PT that sits BELOW the spot price.

| | Value |
|---|--:|
| **WF rating / PT (2026-08-12)** | **OW, $175** (raised from $160) |
| WF reference price (08/11/26) | $127.54 |
| Spot (BBG, 08-31) | **$147.99** |
| **BBG consensus TP** | **$142.78** |
| Consensus implied return from spot | 🔴 **−3.5%** |
| WF vs consensus TP | 🟢 **+22.6%** |
| WF FY27E EPS $5.04 vs BBG 2FY | **$5.04** — 🎯 exact |
| WF FY28E EPS $5.98 vs BBG 3FY $6.08 | −1.6% |

🔴 **Two things worth separating. First, the Street's average price target on ServiceNow is now BELOW the share price — the consensus is, mechanically, mildly negative at spot after a ~16% rally since WF's note. Second, WF's estimates are consensus to the cent, so its 23% PT premium is entirely a terminal-value/multiple argument (25x EV/FCF on forward NTM), which it states: *"increasing terminal value of incumbent platforms improving multiples."*** ⚠️ **A five-name PT sweep (MSFT, NOW, SAP, CRM, WDAY) with every FY27/FY28 EPS marked "NC" is a re-rating call dressed as an upgrade cycle. Flagged on all three affected pages so it is not read as estimate momentum.**

### 5. 🔴 [[MSFT]] — WF $700 is 22.9% above consensus, on consensus earnings.

| | Value |
|---|--:|
| **WF rating / PT (2026-08-12)** | **OW, $700** (raised from $650) |
| WF reference price / spot now | $503.81 → **$507.29** (barely moved) |
| **BBG consensus TP** | **$569.60** |
| WF vs consensus | 🟢 **+22.9%** |
| WF FY27E EPS $19.58 vs BBG 1FY $19.78 | −1.0% |
| WF FY28E EPS $23.53 vs BBG 2FY $23.50 | 🎯 **+0.1%** |

**Same structure as NOW: identical earnings, a much higher multiple (30x P/E on forward NTM vs the ~24x implied by consensus TP). WF names MSFT and NOW as the two *"most (+)"* beneficiaries of open-weight model diffusion. The whole thesis lives in the terminal multiple.**

### 6. [[CRM]] — ✅ **RESOLVED 2026-09-01 → CONFIRMS** (struck as a basis artifact): the "16% below consensus" EPS gap FLIPS SIGN between BBG's own annual and quarterly panels; what survives is only that Wells Fargo's PT is STALE, not bearish

| | Value |
|---|--:|
| **WF rating / PT (2026-08-12)** | **EW, $205** (raised from $200) |
| WF reference price (08/11/26) | $197.47 |
| **Spot (BBG, 08-31)** | **$257.54** — 🔴 **+30% since the note** |
| **BBG consensus TP** | **$270.62** |
| WF PT vs SPOT | 🔴 **−20.4%** |
| WF "FY2027E" EPS $14.09 vs BBG 1FY | $16.73 → 🔴 **−15.8%** |

⚠️ **DO NOT LOG THIS AS A HOUSE-VS-STREET DIVERGENCE UNTIL THE PERIOD IS CONFIRMED. Salesforce's fiscal year ends in January, so a note labelled "FY 2027E" may mean the year ending Jan-2027 (BBG's 1FY) or may be a calendar-2027 label. A ~16% gap is exactly the size a one-year offset produces here (BBG 1FY $16.73 → 2FY $16.07 → 3FY $18.35). This is the same failure mode that produced the 08-28 false "implausible scaling" rejection: CHECK THE PERIOD BASE BEFORE CALLING A DISAGREEMENT.** What IS unambiguous and actionable: **the stock has run 30% since 12-Aug and WF's $205 target is now 20% below spot — the PT is stale, not bearish, and the page should not carry it as a live view without that caveat.**

✅🔴🔴 **RESOLVED 2026-09-01 — AND THE ANSWER IS NOT THE ONE THE CAVEAT ANTICIPATED. THE PERIOD LABEL IS FINE; IT IS THE *BASIS* THAT DECIDES THE SIGN, AND THE SIGN FLIPS.**

**First, the period question is closed. Salesforce's last reported quarter ends 2026-07-31 — that is Q2 of FY2027 (FYE 31-Jan) — so BBG's `1FY` IS the year ending Jan-2027. WF's "FY2027E" and BBG `1FY` are the same period. No offset exists.**

🔴 **But placing WF's $14.09 against the two BBG figures that BOTH claim to cover that period gives OPPOSITE ANSWERS:**

| BBG figure for FY2027 (→Jan-27) | Value | WF $14.09 vs it |
|---|--:|--:|
| **Annual consensus line** (`BEST_EPS`, `1FY` override) | **$16.73** | 🔴 **−15.8%** |
| **Sum of the four quarterly consensus marks** (`estimates.json` "CY2026" block) | **$13.38** | ✅ **+5.3%** |

⚠️ **AND THE "CY2026" LABEL IS A RED HERRING THAT MAKES THIS EASY TO GET WRONG: because Salesforce's quarters end Apr/Jul/Oct/Jan, the four quarters the builder snaps into its `CY2026` bucket are those ending **Apr-26, Jul-26, Oct-26 and Jan-27** — i.e. that block IS fiscal 2027, not calendar 2026. So these two numbers describe the SAME twelve months and BBG's own panel disagrees with itself by **+25.1%** ($13.38 quarterly sum vs $16.73 annual line).**

🔴🔴 **THE READ, AND IT IS A DO-NOT-TRADE VERDICT RATHER THAN A VIEW: Wells Fargo is 15.8% BELOW the annual consensus line and 5.3% ABOVE the sum of the quarterly consensus marks for the identical period. A "divergence" whose SIGN depends on which of two BBG series you pick is not a divergence — it is an artifact. The −15.8% must NOT be logged as a Wells Fargo call against the Street.** ➤ **This is the third distinct basis trap this backlog has hit in a month (the 08-28 "implausible scaling" false rejection, the [[STX]]/[[WDC]] FY28-labelled-as-2027 error resolved in `reconciliation-2026-08-29.md` §6, and now this) — and the first where the artifact is inside BBG itself rather than in our handling of it.**

⚠️ **CARRIED FORWARD AS A DATA-QUALITY ITEM, NOT AN ALPHA ITEM: [[CRM]]'s BBG consensus panel needs a basis audit before ANY CRM estimate comparison is trusted. Two corroborating symptoms from the same pull: the annual series DECLINES from `1FY` $16.73 to `2FY` $16.07 before rising to `3FY` $18.35 (an implausible shape for Salesforce), and the annual-vs-quarterly wedge here is +25.1% against ~+4% for a clean name like [[META]]. Most likely a GAAP / non-GAAP contributor mix differing between the annual and quarterly panels.**

✅ **What survives from §6 unchanged, because it needs no estimate basis at all: the stock is +30% since the 12-Aug note and WF's $205 target is now 20.4% below a $257.80 spot (consensus TP $270.62). The PT is STALE, not bearish, and the page should carry it with that caveat.**

### 7. 🔴 [[SAMSUNG]] — Citi cuts INTO an already-far-below-Street position. Consensus implies +90% upside; Citi implies +65%.

| | Value |
|---|--:|
| **Citi rating / TP (2026-08-31)** | **Buy, W430,000** (cut from W450,000) |
| Spot (BBG) | **W258,500** |
| **BBG consensus TP** | **W492,370.69** |
| Citi vs consensus | 🔴 **−12.7%** |
| Consensus implied upside from spot | **+90.5%** |
| Citi implied upside from spot | +66.3% (Citi prints 65.4% off its own W260,000 reference) |
| **Citi 3Q26E OP** | **W104.1tr** |
| Citi's own stated market consensus 3Q26E OP | W114.4tr → 🔴 **−9.0%** |
| Citi FY26E OP cut | −7.1% |

🔴 **Two separable divergences. (a) On the QUARTER, Citi is 9% below the Street on 3Q26E OP for reasons that are entirely below the operating line — ~W5tr FX plus ~W5tr of bonus provisions recognised through COGS as 2Q-capitalised inventory sells. That is a timing/accounting delta, not a demand call, and it should NOT be read into the memory cycle. (b) On the STOCK, Citi's target sits 12.7% below a consensus that is itself pricing +90% upside — so the marginal information is that even a constructive house is more conservative than the Street on where this re-rates to.**
🔴 **The structural mark worth carrying forward regardless of the PT: Citi models the semiconductor division at 101% of consolidated OP in 3Q26E versus 58% in 3Q25 — every non-memory division is now a net drag, and Citi attributes part of that to Samsung's OWN memory price hikes raising Mobile/CE input costs. A reflexive cost the sum-of-the-parts on this page does not currently net out.**
⚠️ **SHARE-COUNT TRAP APPLIED (standing house rule): Citi's EPS (W41,963 FY26E on 6,607m weighted-average ordinary shares) is COMMON-ONLY; BBG consensus EPS for 005930 is PREFERRED-INCLUSIVE. The two are not comparable and any gap is an artifact. Samsung is reconciled here at NET INCOME (Citi FY26E W277,249bn) and at EBIT (W366,736bn), never at EPS.**

### 8. 🔴 [[NVDA]] — Goldman's $300 is 7% BELOW consensus. And the house model's revenue-per-GW is a hard cross-check on the neocloud pricing story.

| | Value |
|---|--:|
| GS rating / PT (2026-08-30, physical-AI theme report) | Buy, **$300** |
| **BBG consensus TP** | **$322.98** |
| GS vs consensus | 🔴 **−7.1%** |
| Spot | $220.78 |
| **Capstone house 2026E non-GAAP EPS $9.30** vs BBG 1FY | **$9.28** → 🎯 **+0.2%** |
| **Capstone house 2027E non-GAAP EPS $15.49** vs BBG 2FY | **$15.39** → 🎯 **+0.6%** |

**The house NVDA model is a CONSENSUS model on earnings — within 0.6% at both marks. The differentiation in that model is not the EPS, it is the GW framing, and this run put a live market price on that framing:**

🔴 **THE REV-PER-GW TRIANGULATION, and it must be read with the units held straight:**
| Series | Value | Basis |
|---|--:|---|
| **Capstone house — NVDA revenue per GW sold** | **~$21bn (2025) → ~$24bn (2026E) → ~$25bn (2027E)** | NVDA silicon/systems revenue per GW of DC capacity sold |
| [[ORCL]] anchor (autumn 2025, via UBS) | $10bn/GW | cloud contract revenue per GW |
| SpaceX / [[NBIS]] new deals (UBS, 08-31) | **$30–50bn/GW** | ⚠️ **SHORT-TERM ~6-month deals priced near SPOT, on Vera Rubin clusters** |
| JPM APAC build cost (08-31) | **US$6.4–13.2mn/MW = ~$6.4–13.2bn/GW** | ⚠️ **CONSTRUCTION COST per GW — a different quantity entirely** |

⚠️ **UNIT DISCIPLINE, ENFORCED (this wiki has been burned here before): these four series are on FOUR DIFFERENT BASES — silicon revenue per GW, cloud contract revenue per GW, spot-priced short-duration contract revenue per GW, and civil/shell BUILD COST per GW. They must not be netted, chained, or differenced into a margin. In particular the $30-50bn/GW figure is a ~6-month spot mark on the newest GPU generation and is not an annualised run-rate.**
⚠️ **That said, ONE cross-check is legitimate and is worth carrying as an open question: the house has NVDA capturing ~$25bn of revenue per GW in 2027E. If a neocloud's own contracted revenue on comparable capacity is being marked anywhere near $30-50bn/GW even on short-dated spot deals, the silicon share of the value chain is very high and the buyer's margin over silicon alone is thin. Either the neocloud numbers are duration-inflated spot prints (UBS's own reading), or the house NVDA rev/GW is conservative. Flagged for the [[CRWV]]/[[NBIS]]/NVDA triangle, not resolved here.**

### 9. 🔴 [[AMZN]] — GS $375 is 13.8% ABOVE consensus, and the $72bn automation number is NOT in it

| | Value |
|---|--:|
| GS rating / PT | Buy, **$375** |
| **BBG consensus TP** | **$329.67** |
| GS vs consensus | 🟢 **+13.8%** |
| BBG cons. EPS | 1FY $14.57 · 2FY **$12.35** · 3FY $15.62 |

⚠️ **Two flags. (1) GS's headline automation figure — *"~5.6% of leverage in Amazon's total cost to serve via automation by 2030 → ~$72bn cost savings and a ~240bps EBIT margin tailwind"* — is explicitly labelled *"IN OUR UPSIDE ANALYSIS"* by GS itself. It is a scenario, it is NOT in the $375 base case, and it must never be netted against consensus EBIT. (2) Note the consensus EPS SHAPE: 2FY ($12.35) is BELOW 1FY ($14.57) before recovering in 3FY ($15.62) — the Street is already modelling a capex/depreciation trough. Any humanoid-automation margin story lands on the far side of that dip, not before it.**

### 10. ⚠️ [[LITE]] — DB says it is "materially above consensus" at FY29. BBG says +6.6%. Handle per the standing FY3 rule.

| | Value |
|---|--:|
| DB FY29E non-GAAP EPS | ~**$50** |
| **BBG consensus 3FY EPS** | **$46.91** |
| DB vs consensus | +6.6% |
| DB's own claim | *"we are still materially above consensus"* |
| Management guide (given at DB's own Tech conference) | **FY28E EPS $40** |
| BBG consensus 2FY (≈FY28) | **$33.56** → management guide is **+19% vs Street** |
| DB's stated position | **BELOW the $40 management guide, above the Street** |

⚠️ **This is the known FY3 pattern: a house's characterisation of "consensus" in the out-years routinely disagrees with the BBG composite, because far-year contributor counts thin out. +6.6% is a real gap but "materially above" is doing work. DO NOT mark DB against the consensus printed in its own note. What IS clean and useful: the ORDERING is unambiguous and fully corroborated — MANAGEMENT ($40 FY28E) > DB > STREET ($33.56 FY28). A company guiding 19% above the Street, with a fresh initiating house choosing to sit between the two, is the most informative single fact on the LITE page this week.**
**House cross-check: Capstone LITE CY27E EPS $30.02 sits between BBG FY27 ($21.45) and FY28 ($33.56), which is where a calendarised June-FY number should sit. No divergence to flag.**

---

## ✅ CONFIRMS — no action

| Datapoint | Source | Baseline it confirms |
|---|---|---|
| **[[ANET]] FY28E EPS ~$6.29** (DB implied) | DB initiation | 🎯 BBG 3FY **$6.30** — within 0.2%. DB's ANET call is 100% multiple. |
| **[[HPE]] CY27E EPS ~$4.13** (DB implied) | DB initiation | 🎯 BBG 2FY **$4.12** — within 0.2%. DB stated its numbers were "roughly in line with consensus"; confirmed. |
| **[[DELL]] CY27 EPS ~$21.8** (DB implied) | DB initiation | BBG 1FY $19.10 / 2FY $23.04 — interpolates in line. |
| **[[MSFT]] FY27E $19.58 / FY28E $23.53** | WF, 08-12 | BBG 1FY $19.78 / 2FY $23.50 — −1.0% / +0.1%. Explicitly marked "NC" by WF; confirmed unchanged. |
| **[[NOW]] FY27E $5.04** | WF, 08-12 | 🎯 BBG 2FY **$5.04** — exact. |
| **[[NVDA]] house 2026E/2027E non-GAAP EPS $9.30 / $15.49** | Capstone model | BBG 1FY $9.28 / 2FY $15.39 — +0.2% / +0.6%. The house NVDA model is a consensus model on earnings. |
| **[[COHR]] DB FY29E ~$19** | DB initiation | BBG 3FY $18.66 — in line. (The divergence is with the HOUSE, not the Street — see §2.) |
| **[[ADI]] GS PT $480** | GS physical AI | BBG consensus TP $477.00 — 🎯 within 0.6%. |
| **[[NXPI]] GS PT $325** | GS physical AI | BBG consensus TP $312.96 — +3.8%, in line. |
| **[[FLEX]] GS PT $154** | GS physical AI | BBG consensus TP $159.91 — −3.7%, in line. |
| **[[MRVL]] purchase commitments $8.519bn exiting F2Q27 (from $2.757bn)** | 10-Q via WF | **Company filing — not an estimate, nothing to reconcile.** Consistent in DIRECTION with the FY28 raise from the 08-27 print. BBG consensus TP $293.27 vs spot $211.66 (+38.6%). |
| **[[META]] settlement up to $18bn** ($16.7bn + $459m + $75m + up to $1bn TX) | Court filing via Bloomberg/Stratechery | **Disclosed fact.** Against the house model (capex 2026E $131bn / 2027E $170bn), an $18bn one-off spread over years — with $5.3bn contingent — is not material to the capex debate. No estimate change warranted. |
| **DRAM contract pricing: DDR5 $18.44/GB, DDR4 $21.16/GB (Aug-26)** | TrendForce via WF | Consistent with the memory-inflation thread already on [[MU]]/[[SKHYNIX]]/[[SAMSUNG]]. ⚠️ Logged with the observation that the q/q RATE is decelerating (DDR5 95.9%→38.2%→19.5%) even as the level stays extreme. |
| **[[ON]] GS Neutral $95** | GS physical AI | BBG consensus TP $108.73 — GS −12.6%, directionally consistent with the Neutral. |
| **[[TSLA]] GS Neutral $360** | GS physical AI | BBG consensus TP $391.83 — GS −8.1%, consistent with the Neutral and with GS assigning it the lowest implied return of 30+ names in its own beneficiary table. |

---

## Items carried forward (not reconcilable this run)

- ✅ **RESOLVED 2026-09-01 — [[CRM]] period basis** (§6). The labels are fine (`1FY` = FY2027 = WF's "FY2027E"), but the −15.8% **flips to +5.3%** against the quarterly-sum basis for the same twelve months, because BBG's own annual and quarterly panels disagree by 25.1%. **Struck as a divergence; re-filed as a CRM consensus data-quality item.**
- ⚠️ **STILL OPEN, AND BIGGER THAN LOGGED — [[COHR]] CY28 bridge** (§2). Consensus side now nailed live 2026-09-01: median **$16.52**, **street high $20.18**. The house's $23.60 is +42.9% over the median and **+17.0% over the street HIGH — outside the entire published range.** The bridge against DB's own build is still the open task; `/wiki-consensus` cannot close it.
- **UBS's MTIA 400 internal inconsistency** — 288GB HBM3E / 9.4TB/s in the note text vs 432GB HBM4 in its own Figure 1. Both printed; unsettled; flagged on [[META]] and [[AVGO]].
- **The DB-vs-Jefferies laser-content dispute** — qualitative, not reconcilable against consensus, but it is the load-bearing engineering question under every optical PT in §1. Tracked in `themes/optical-cpo.md`.
- **The open-model contradiction** — Wells Fargo's CIO survey says customers are shifting to "good-enough" open-source models; UBS's CFO dinner the same month found *"hesitation to use open models, whether Chinese or even US,"* with buyers preferring cheaper CLOSED models. Both are survey/channel evidence, neither is consensus data. Logged in `themes/tokenmaxxing.md`.
- **Private names** ([[ANTHROPIC]], [[OPENAI]], [[CEREBRAS]]) — no BBG, no house model; reconciled against prior wiki comments only. The Anthropic–Nscale **$45bn** figure came verbally on the UBS call with no terms, duration or structure; awaiting a primary before it is treated as a mark.

---

_BBG column resolved 2026-09-01 — `estimates.json` asof **2026-09-01** (99/99 live, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 `carried_over` stamps, 0 records byte-identical to the 08-28 vintage), plus an ad-hoc live `BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY` pull for **CRM** and **COHR**. This report carried **no `PENDING` cells** (its 08-31 column was already live); this layer closes two of its **carried-forward** items instead: **[[CRM]] §6 struck as a basis artifact whose sign flips between BBG's own annual and quarterly panels**, and **[[COHR]] §2 sharpened — the house is +17.0% above the STREET HIGH, not merely +43% above the median.** Canonical header `## Where the new data DIVERGES` applied (was `## 🔴 DIVERGES — the alpha`). **No web data was substituted at any point.**_
