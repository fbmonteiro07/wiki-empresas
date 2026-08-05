# Reconciliation — 2026-08-04

_Run: `/run-inbox` (scheduled, unattended). Four sources reconciled:_
1. **AMD Q2 2026 earnings call — Bloomberg LIVE TRANSCRIPT, 2026-08-04** (the PRIMARY source for a print that had already been ingested earlier the same day from desk notes).
2. **Barclays · Saket Kalia / Ethan Sneckenberger, "Cloudflare, Inc. — Traffic Continues to Inflect, We Wonder if 'The Check Is in the Mail' Given Volume and Rev. Lags; Latest 2025 Mkt Share Data", 2026-08-04** (earnings preview; completed 03-Aug 16:44 GMT, released 04-Aug 04:10 GMT).
3. **Bernstein QUICK TAKE · Gautam Chhugani / Mahika Sapra / Sanskar Chindalia / Harsh Misra, "AI Infra/miners: Texas data center audit to drive more MW scarcity", 2026-08-04.**
4. **Capstone internal research synthesis · Daniel Grozdea, "SPCX 2Q26 Earnings Preview — reports tonight 8/4 AMC (lockup, not the quarter)", 2026-08-04 13:08** — a PRE-print synthesis of ~3 weeks / 73 SPCX-tagged emails across MS, Bernstein, DB, Cantor, SIG, UBS, Citi, 22V, GS and FundaAI. **Not a Bernstein note** (the router mis-detected the broker).

_Source 4 arrived **before** the print it previews, and the print itself was already on `SPCX.md`. Handled under the relay rule — **the primary wins**; the relay was folded only as a **scored pre-print bar** plus two new covering houses. Nothing in the maiden-print block was altered._

---

## Baseline availability

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Available — used throughout. Every superseded value was moved to the relevant page's `## Changelog` during patching. Only **one** supersession occurred this run (see below); the other three sources were purely additive. |
| **2. Capstone house models** | 🔴 **Effectively unavailable — 10 of the 11 affected names have no house model.** `_data/house.json` covers **NVDA only** among today's names. **No house model for AMD, NET, MSFT, AMZN, CRWV, SPCX, DELL, SMCI, AKAM, FSLY.** ⚠️ AMD is the notable gap: it is the largest print in this run and one of the most-discussed names on the wiki, and there is no house number to place the guide against. |
| **3. BBG consensus (live re-pull)** | 🔴 **PENDING — `HTTP 503: Bloomberg connection test failed – please ensure you are logged in to Bloomberg Terminal`.** Tested at ingest time via `E:\bloomberg_api` (`from bloomberg import bdp`, `AMD US Equity` / `NET US Equity`, `PX_LAST` + `BEST_TARGET_PRICE`). **No web data was substituted at any point.** |
| **3b. BBG consensus (on-disk snapshot)** | ✅ **Used as the consensus baseline.** `_data/estimates.json` **asof 2026-08-04** — i.e. a BBG pull dated the same day as every source, 97 names, quarterly (1FQ/2FQ) + CY2026/CY2027. This is genuine BBG consensus, not a substitute. |

### 🔴 Action required — re-run when the Terminal is back
1. **No `BEST_TARGET_PRICE` this run.** `estimates.json` carries `px` but no consensus target, so **Barclays' NET PT $300 could not be placed against the consensus PT** — the single most useful missing placement (see DIVERGES ①). Re-run `/wiki-consensus` or an ad-hoc `bdp` pull for `NET US Equity`, `AMD US Equity`.
2. **SPCX has NO record in `estimates.json`** (97 names; SPCX is not among them). Newly public — **add it to the fetch list.** Until then the only consensus mark for SPCX is the **Visible Alpha** set carried inside source 4, which is not BBG-verifiable.

### ⚠️ Method flags applied
- **`estimates.json` CY2026 systematically understates beats** (known defect, root-caused 2026-08-01, still unfixed: CY sums embed pre-print consensus for already-reported quarters; **CY2027 is clean**). **No conclusion in this report rests on a CY2026 figure** — quarterly (1FQ/2FQ) and CY2027 only.
- **The 08-04 snapshot pre-dates the two prints in this run.** AMD's `lrq` is **2026-06-27** (Q2 actuals not yet folded into the consensus record) and SPCX is absent. For AMD this is exactly the right vintage for scoring a guide against the bar it was set to clear — but every AMD line below will move on the next pull.
- **`house.json` NVDA `opm` field reads 89% / 92% / 94% (2025/26/27).** Implausible as an operating margin; treated as a **parse artifact and not used**. Only the house `rev` and `eps` lines were relied on.
- **No bridge was built.** `estimates.json` carries no segment split, so AMD's consensus Instinct/Data-Center line cannot be isolated from total revenue. Rather than free-hand a bottoms-up 2027 bridge, the comparison below is stated on figures that exist. (Wiki rule: no un-disciplined models.)

---

## 🔴 DIVERGES — the alpha

### ① ★ NET — the Overweight has already been overtaken by the tape, two days before the print
| Mark | Value | Source |
|---|--:|---|
| Barclays PT | **$300.00** | Barclays · Kalia, 2026-08-04 |
| Barclays reference price | $278.98 (31-Jul-26) | same |
| Barclays stated upside | **+7.5%** | same |
| **BBG `px` asof 2026-08-04** | **$301.33** | `estimates.json` |
| **Implied upside at the current mark** | **−0.4%** | derived from the two figures above |

**The note was released 04-Aug 04:10 GMT off a 31-Jul reference price, and the stock closed above the target price on the day of release.** The Overweight now carries no implied upside. This is the rating-vs-PT tension the reconciliation step exists to catch, and it is **live into an 08-06 print**. Two readings, and the history favours the first: Barclays' own PT path is **$235 (OW initiation, 02-Dec-2025) → $250 (10-Feb-2026) → $300 (13-Jul-2026)** — three raises in eight months — so **a fourth raise into or immediately after the print is the base case**, and the note's own logic ("could see upside as the lag starts to catch up") is written as a setup for exactly that. The alternative is that the rating is stale. ⚠️ **Cannot be placed against the consensus PT this run — BBG live is down.** That placement is the first thing to run when it returns.

### ② NET — Barclays sits ~110bps BELOW consensus on gross margin while sitting ABOVE it on EBIT
| Metric (Q2 FY26E) | Barclays | BBG consensus | Variance |
|---|--:|--:|--:|
| Revenue | ~$665m | **$666.4m** | −0.2% (in line) |
| Gross margin | **~72.0%** | **73.12%** | **−112bps** |
| EBIT margin | **~14.0%** | 13.60% (= $90.6m / $666.4m) | **+40bps** |

**Both cannot be comfortably true unless Barclays models materially lighter opex than the Street.** The two-sidedness is the point: if Barclays is right on gross margin and the Street is right on opex, **consensus EBIT is too high**; if Barclays' opex assumption is the right one, its own Rule-of-50 path is safer than the GM line suggests. Barclays' framing pre-empts the bear read — the path to the 70-77% long-term range **"will not be linear"** because **Act 3 carries below-corporate-average gross margins and is growing as a mix**, and a GM downtick **should arrive with an uptick in growth or operating margin**. **That is a falsifiable claim: if 08-06 prints GM at/below ~72% WITHOUT a faster growth or better EBIT print, the mix argument fails on its first test.** Watch the 08-06 GM against **72.0% (Barclays) / 73.1% (consensus)**.

### ③ NET — the revenue line is not the test; the two metrics that matter are not in consensus
Barclays models **~30% growth to ~$665m** against consensus **$666.4m** — a 0.2% gap, i.e. **the revenue print is non-falsifying either way**. The thesis rests on **cRPO growth (+31% modelled)** and **DBNR (118% in 1Q26 → ~119% modelled)**, **neither of which `estimates.json` carries**. ⚠️ **So the wiki cannot currently score the actual test of this thesis against consensus** — the cap-model lag argument ("timing rather than underlying demand") is only checkable on cRPO and DBNR. Flagged as a coverage gap in the consensus data, not a disagreement.

### ④ ★ AMD — management put a floor above a NAMED 2027 number, and consensus is the low anchor
On the call, **C.J. Muse (Cantor) put ~$30bn of 2027 Instinct revenue** to management as implied by the data-center guide. **Lisa Su: *"what you're hearing from us is that your data center AI number is probably too low"*** — and separately, that "over 100%" should be read as **"well over 100%."**

| 2027 Data Center growth view | Mark | Source |
|---|--:|---|
| Sell-side consensus | **+88% y/y** | already on `AMD.md` (Jefferies, 2026-08-04) |
| Management language | **"well over" +100%** | Q2 call transcript, 2026-08-04 |
| Buy-side feedback | **~150%**, some **175-200%** | Jefferies desk, 2026-08-04 |

**Consensus is the LOW anchor of the three, and management spent the call nudging it upward without giving a number.** BBG CY2027 total revenue consensus is **$78.75bn** / EPS **$14.01**. ⚠️ **The Instinct line cannot be isolated — `estimates.json` has no segment split — so this is deliberately left as a range disagreement rather than a fabricated bridge.** The actionable form: **management has now explicitly rejected ~$30bn of 2027 Instinct as too low on the record**, which converts the buy-side's 150% from an aggressive assumption into the one closer to management's own framing. The reason the stock fell anyway is that the language was vague, not that the number was disappointing — and this exchange is the closest management came to a figure.

### ⑤ AMD — the Q3 guide beat consensus on revenue and EPS but MISSED it on gross margin
| Metric (Q3 FY26) | AMD guide | BBG 1FQ consensus | Variance |
|---|--:|--:|--:|
| Revenue (mid) | **$13.0bn** ±$300m | **$12.51bn** | **+3.9%** |
| Implied EPS | ~**$1.93** | **$1.873** | **+3.0%** |
| Gross margin | ~**56.0%** | **56.24%** | **−24bps** |
| Opex | **~$3.65bn** | not in consensus record | — |

**Gross margin is the only guided metric below consensus** — and it is guided **flat q/q on a +13% sequential revenue step**. That is now corroborated from three directions on the record: Jean Hu's **"data center AI… gross margin slightly below corporate average"**, Su's **Helios yield admission** ("expect overall yields to improve in the next few quarters — especially for a highly complex product"), and SemiAnalysis's 07-24 finding that AMD **cannot pass through the expected 2027 HBM price increase** because "most of AMD's volume goes to large buyers with real negotiating leverage." **The mix arithmetic that has capped this bull case all year is unchanged, and the fastest-growing line remains the least accretive.**

### ⑥ ⚠️ AMD — consensus Q4 embeds a very steep step that management never underwrote with a number
| Metric (Q4 FY26E) | BBG 2FQ consensus | Implied vs the Q3 guide |
|---|--:|--:|
| Revenue | **$15.71bn** | **+20.9% q/q** off $13.0bn |
| Gross margin | **55.71%** | **−53bps q/q** vs the ~56% Q3 guide |

**The Street is carrying a ~$2.7bn sequential revenue add with margin dilution, on the strength of adjectives.** Management said only that Q4 would be **"higher than"** Q3's strong double-digit growth, that **"the Helios ramp is just starting at the end of Q3 and it'll be much more substantial in Q4,"** and that Q1-27 would be **"a further step up."** No Q4 figure was given. ⚠️ **This is the least-supported number in the AMD consensus stack and the first place a Helios slip or a yield problem would surface.** Note the consensus GM step-down implicitly agrees with ⑤ — the Street is already modelling the ramp as margin-dilutive.

### ⑦ ★ NVDA — paying up ~50% per megawatt versus Microsoft, at the same counterparty
Bernstein Exhibit 2, IREN revenue yield:

| Contract | Per **IT MW** | Per **gross MW** |
|---|--:|--:|
| Microsoft | **~$10mn** | ~$11mn |
| **NVIDIA** | **~$15mn** | ~$14mn |
| Enterprises | — | ~$11mn |
| **NVDA vs MSFT (IT MW basis)** | **+50%** | +27% |

⚠️ **Bases must not be mixed** — the per-IT-MW and per-gross-MW series are different denominators and are carried separately. Recent **enterprise cloud deals price GPU-hour rates 20-25% above prior guidance**, and Bernstein's logic is explicit: **"If MWs are scarce, it makes sense to earn more per MW."**

Placed against the only house model available this run:

| NVDA | House (`house.json`) | BBG CY2027 | House vs consensus |
|---|--:|--:|--:|
| 2027 revenue | **$661bn** | **$568.2bn** | **+16.3%** |
| 2027 EPS | **$15.44** | **$12.91** | **+19.6%** |

**The house is already the aggressive mark, and this is a cost datapoint on the leased-capacity leg of that thesis** — not a revenue variance but a **returns** variance. It does not change the model; it raises the cost of the megawatts the model's compute-leasing strategy consumes, at a moment when the supply of approved megawatts is being throttled (see ⑧). **Logged as a watch item, not an estimate change.**

### ⑧ ⚠️ The scarcity mechanism behind ⑦ — a third political vector on power in one week
Texas Governor Abbott has directed the **PUCT and ERCOT to audit every data-center project in the interconnection process**; **ERCOT has PAUSED the "Batch Zero" review that was due to publish classification results on 2026-08-07.** The queue stands at **474 GW of interconnection REQUESTS with data centers ~90% of new requests** (⚠️ **requested-capacity basis — NOT comparable to energized, IT-load or facility GW**; cross-checks consistently against the **>2,000 GW FERC queue / 4-5 year wait** already on the power dossier, a different queue on the same basis). Bernstein: the audit **"throttles speculative data center pipeline and makes genuine sites with development history more valuable."**

**This is the third distinct political/regulatory vector logged on `themes/ai-datacenter-power.md` inside a week** — the NY moratorium (via Baker, 08-04), the Texas tax-abatement repeals (The Information, 08-02) and now the ERCOT audit (08-04). **Time-to-power is lengthening for new builds while already-approved MW re-rate** — which is the same fact pattern driving ⑦ and the CONFIRM in ⑨.

---

## ✅ CONFIRMS — no action

### ⑨ MSFT — the mirror image of ⑦, and a genuine confirm of timing
Microsoft's earlier IREN contract at **~$10mn per IT MW** now sits **~33% below the current clearing price (~$15mn under the NVDA contract)**. Against MSFT capex consensus of **$44.65bn (Q3-26E)** and **$46.6bn (Q4-26E)** — annualising above $180bn — **locking hosted capacity one vintage early is worth real money, and the wiki should credit it as such rather than treating the contract as a neutral fact.** No estimate change.

### ⑩ SPCX — the pre-print bar, scored against the actuals already on the page
| Metric (Q2 26) | Visible Alpha consensus | MSe | **Actual** | Score |
|---|--:|--:|--:|---|
| Revenue | $6.9bn | $6.75bn | **$7.81bn** | **+13.2% vs consensus** |
| Adj. EBITDA | $2.1bn | $2.0bn | **$3.5bn** | **+66.7%** |
| Consumer Starlink subs | 12.1mn | 12.0mn | **12M** | −0.8% (in line) |
| Consumer monthly ARPU | $65.5 | $65.5 | **$66** | +0.8% (in line) |
| End-of-period compute | 1.4 GW | 1.4 GW | **1.4 GW** | on the nose |
| EBIT | −$1.6bn | −$1.7bn | _no actual on page_ | open |
| Adj. diluted EPS | −$0.32 | −$0.35 | _no actual on page_ | open |

**The shape is unambiguous: the two P&L lines blew out while every operating KPI landed exactly on the bar.** That **CONFIRMS** the page's standing conclusion — reached independently by MS ("largely at the mercy of technical forces") and DB ("neither of the two things that move the stock is the print") — that the quarter was never the driver, and it explains a **−5 to −7%** reaction to a large beat. Two new covering houses added this run: **Cantor OW $246** (whose EBITDA-beat call scored right) and **SIG Neutral, no PT**. ⚠️ **Not BBG-verifiable — SPCX has no `estimates.json` record.**

### ⑪ AKAM — the share loss is real and the consensus revenue line already reflects the right mechanism
**Akamai 21.9% of global CDN revenue in 2025, −160bps y/y** (after −230bps in 2024; series 25.7% → 24.6% → 25.8% → 23.5% → 21.9%), in a market that **grew +5.9% to $17.96bn** — so this is **share loss, not TAM loss**. Against BBG consensus **CY2026 $4.51bn → CY2027 $4.99bn (+10.7%)**: consensus still models growth, which is only coherent because the growth is coming from **security/compute, not delivery** — exactly the framing already on the page. **CONFIRMS; no estimate action.**

### ⑫ FSLY — a real but immaterial share gain
**Fastly 3.2% in 2025, +25bps y/y** (series 2.4% → 2.7% → 2.9% → 2.9% → 3.2%; the 2023→2024 delta was **+0bps**, so 2025 is a modest inflection rather than a trend). BBG consensus **CY2026 $719.5m → CY2027 $798.4m (+11.0%)**. ⚠️ **+25bps on a $17.96bn market ≈ $45mn of relative positioning — immaterial against a ~$720mn revenue base, and this figure is OUR arithmetic on two source numbers, not Bernstein's or Barclays'** (it was deliberately kept off the page for that reason). **CONFIRMS; no estimate action.**

### ⑬ CRWV — contracted capacity insulated; the cost side is the watch item
**Core Scientific has already delivered 437 MW to CoreWeave and remains on track to 590 MW by early 2027, so CORZ execution timelines are NOT impacted by the Texas audit** — even though CORZ's 300 MW gross Pecos expansion is exposed. Against BBG **CY2027 revenue $25.05bn** and **Q2-26E capex $7.94bn**: no estimate change. ⚠️ The offsetting read is the same one as ⑦ — **CoreWeave leases all of its datacenters, so a rising $/MW clearing price is a rising cost of sourcing**, compounding the yield-on-cost pressure already on the page. Bernstein carries no CRWV rating in this note; its standing **Underperform / PT $67** (Rezaei) is untouched.

### ⑭ DELL / SMCI — a denied rumour, correctly logged as a watch item only
The reported **$52bn / 13,000-rack GB300 order placed directly with Foxconn was called "fake news" by Musk**. Wells Fargo's Aaron Rakers' conditional read — **IF a buyer of that scale ordered racks direct from the ODM, that bypasses the OEM channel and is negative for DELL and SMCI** — survives the denial as a **structural channel-disintermediation question**, because the denial kills the specific order, not the mechanism. BBG consensus untested and unchanged: **DELL CY2027 $196.2bn / EPS $22.12**; **SMCI CY2027 $60.3bn / EPS $3.75**. **No estimate action.** It lands harder on SMCI, which does L7-L10 in-house.

### ⑮ AMD — segment profitability and cash flow: no consensus comparator, one new watch item
`estimates.json` carries no segment operating income and no FCF line, so the transcript's new disclosures **cannot be reconciled against BBG at all**. Against the **page**, however, one comparison is available and it is worth flagging:

| AMD cash flow | Q1 FY26 | Q2 FY26 | Direction |
|---|--:|--:|---|
| Operating cash flow | — | $2.4bn | — |
| **Free cash flow** | **$2.6bn (a record)** | **$1.6bn** | **−38% q/q** |
| Inventory | — | **~$8.5bn** (up q/q) | building |
| Cash + STI | $12.3bn | $13.1bn | +$0.8bn |

**FCF fell ~38% q/q on a +13% q/q revenue step, with inventory building** — management's only explanation was "to support strong data center demand," which is a demand-positive framing of a working-capital drag. New Q2 segment operating income, also with no consensus comparator: **Data Center $2.1bn / 31%**, **Client & Gaming $582mn / 15% (vs $767mn / 21% a year ago — down in both dollars and margin)**, **Embedded $386mn / 40% (vs $275mn / 33%)**. **Logged as a watch item ahead of the Q3 print, not as a divergence.**

---

## Internal inconsistencies caught and logged rather than resolved
1. **AMD "same rack power" vs SemiAnalysis's rack model.** Management claims Helios delivers **"up to 15% more throughput at the SAME RACK POWER and up to 30% more tokens per dollar than the competition."** SemiAnalysis's 07-24 bottoms-up build has **MI455X at ~240kW server / ~257kW all-in vs GB300 NVL72 at ~142kW / ~159kW**, i.e. "MI455X lands even beyond VR NVL72 in power draw." **These cannot both be right.** The page already carried a BofA-vs-SemiAnalysis power disagreement; management's claim is now a **third, on-the-record** input to it. **Resolvable against real Helios deployment data in 2H26 — not adjudicated here.**
2. **RIOT capacity, inside a single Bernstein note:** "~1 GW energized operating capacity in Texas available for AI deployments (700 MW Rockdale + 400 MW Corsicana)" — which itself sums to 1.1 GW — against "**ready operational 1.7 GW capacity in Texas**" in the co-location-lease discussion, while Exhibit 1 shows 1,700 MW as *Texas concentration of the planned pipeline*. Both carried, flagged, neither chosen.
3. **SPCX Starship Flight 13 date:** the page dates it **2026-07-24**; source 4 says **July 26-27**. Logged for a primary check.
4. **`MSFT.md` has TWO `## Changelog` sections** (~line 231 and ~line 425) — a pre-existing structural defect, out of scope for this run. This run's entry went into the first. **Referred to `/wiki-lint`.**

## Method note on the one supersession this run
Only one thesis-drift move occurred across eleven files: **`AMD.md` stated in two places that the earnings transcript was "not on file"** (the `## Current state` lead and the Jefferies 08-04 intra-quarter row, which described itself as "the most complete call reconstruction available (transcript not on file)"). Both statements became false when source 1 landed and were corrected in place, with the prior wording preserved in the Changelog. ⚠️ **Materially: the transcript CONFIRMED the desk-note reconstruction line by line — not one figure was revised.** That is a quality datapoint about the desk notes this wiki relies on when transcripts are late.

## Top of the run
1. **★ NET (①) — an Overweight whose stock closed above its price target on the day the note was released, two days before the print.** The most actionable single finding, and the PT-vs-consensus placement is still blocked on Bloomberg.
2. **★ AMD (④) — Su told an analyst on the record that ~$30bn of 2027 Instinct is "probably too low,"** which makes the +88% sell-side consensus the low anchor against a buy-side already at ~150%.
3. **★ NVDA (⑦) — paying ~50% more per IT MW than Microsoft did at the same counterparty**, against a house model already 16-20% above consensus, into a tightening approved-megawatt market (⑧).
4. **AMD (⑥) — consensus Q4 revenue implies +20.9% q/q on adjectives alone**, the weakest link in the AMD stack.
5. **AMD (⑤) — gross margin was the only guided metric below consensus**, now corroborated on the record from three independent directions.
6. **SPCX (⑩) — a +13% revenue and +67% EBITDA beat with every KPI exactly in line, and the stock fell**, confirming the technicals-over-fundamentals framing both covering houses set in advance.
