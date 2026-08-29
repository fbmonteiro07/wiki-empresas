# Reconciliation — 2026-08-28 (/run-inbox, scheduled/unattended)

_Every NEW quantitative datapoint from tonight's ingest, placed against **(1)** prior wiki comments, **(2)** Capstone house models, **(3)** BBG consensus. Bloomberg was **LIVE** for this run (wrapper `E:\bloomberg_api`, `BEST_FPERIOD_OVERRIDE` passed as a kwarg — note the wrapper rejects an `overrides={...}` dict with `BAD_ARGS / Invalid override field`). Sources ingested: Barclays AI-lab unit economics (08-28), AlphaSense ex-AWS Bedrock expert call (08-27), Goldman/Kioxia IR (08-25), Bristlemoon/Sandisk (08-28), Jefferies water (08-24), Digitimes/YMTC (08-28), UBS CXMT model file (08-06), plus four flagged historical backfills._

⚠️ **Period-basis warning applied throughout:** Barclays' ladder is **calendar** years; Kioxia is **FY ending March**; Sandisk is **FY ending ~June**; MSFT is **FY ending June**. Every comparison below states the basis it uses. (This is the check the 08-28 memory note demands after the MU/SNDK "implausible scaling" error, which was a full-FY-vs-one-quarter basis mismatch.)

---

## 🔴 DIVERGES (the alpha)

### 1. ★★ [[SNDK]] — THREE INDEPENDENT SOURCES NOW REJECT MANAGEMENT'S FY28-30 GROWTH FRAME, AND CONSENSUS IS ONE OF THEM

This is the highest-value finding of the run. The wiki has carried "SNDK FY29 vs the mid-to-high-teens guide" as its largest open divergence. Tonight it gets a **third independent leg and a mechanism.**

| Source | FY29 revenue | FY29 EPS | vs mgmt guide (mid-to-high-teens growth **every year** FY28-30) |
|---|---|---|---|
| **Management (Investor Day)** | mid-to-high-teens growth | — | — |
| **BBG consensus** (BEST_SALES/BEST_EPS 3FY, 2026-08-28) | **$52.67bn vs $58.59bn in 2FY = −10.1%** | **$211.10 vs $259.46 in 2FY = −18.6%** | ❌ **rejects it — consensus models an outright DOWN year** |
| **Bernstein** (already on page, Street-high $3,000 PT) | **$50.1bn = −11.9%** | — | ❌ rejects it |
| **Bristlemoon** (NEW, 08-28) scenario 1 — NBM floor holds | — | **$218** | ❌ rejects it |
| **Bristlemoon** scenario 2 — NBMs breached | — | **$154** | ❌ rejects it, harder |

- **🔴 THE NEW AND GENUINELY SURPRISING RESULT: Bristlemoon's *bear* scenario 1 IS the consensus. $218 vs BBG 3FY $211.10 = only +3.3%.** The market has already priced the world in which blended ASP falls to the NBM floor and non-NBM ASP halves. **Only the NBM-BREACH case ($154, −27.0% vs consensus) is genuinely un-priced.**
- **The mechanism Bristlemoon adds, which neither Bernstein nor consensus supplied:** management's model is **internally inconsistent**. Mid-high-teens bit growth + flat ASP cannot coexist with a ~80% average gross margin, because *"the ~80% average gross margin is only plausible if ASP falls by over 30% from today's levels."* The sole reconciliation is that GM **enters** FY28 at 80%, i.e. blended ASP is already at the NBM floor — making the "sustainable model" a bet the NBMs hold in an oversupplied market. Verdict: *"a piece of investor marketing material that should be de-emphasized."*
- **Corroboration of the floor itself is now two-sided and tight:** Bristlemoon derives an NBM floor **26-28% below realised 4Q26 ASP** and a **78-79% GM floor** (vs 4Q26's 84.6%); CFO **Luis Visoso** independently confirmed *"around 80%"* at the Investor Day. **The two agree to within ~1-2 points.**
- ➤ **ACTION: the wiki should stop carrying management's FY28-30 model as a live forecast and carry the SCENARIO BAND instead. The trade is not "is the guide right" — consensus already says no. The trade is whether the NBMs HOLD, which is worth ~$57 of FY29 EPS ($211 → $154) and is a counterparty question, not a supply/demand question.**
- ⚠️ **Counterweight kept: Bristlemoon is NET LONG the cycle** — it judges oversupply *"unlikely… within the next 2-3 years"*, and at 8x even the breach case gives a **$1,200-$1,700 mid-2028 "trough" price vs $1,485 today.** A bear case that is roughly flat on the stock is a weak bear case.
- **No Capstone house model exists for SNDK** (no `## Capstone estimates` block on the page) — baseline (2) unavailable. Flagged as a gap worth closing given this is the wiki's largest standing divergence.

### 2. 🔴 [[NOW]] — THE EXPERT'S DISRUPTION CASE IS NOT IN CONSENSUS AT ALL

| | 1FY | 2FY | 3FY |
|---|--:|--:|--:|
| **BBG BEST_EPS** | $4.083 | $5.035 | $6.080 |
| implied growth | — | **+23.3%** | **+20.8%** |

- Consensus models **steady low-20s% EPS compounding with no inflection** — i.e. **zero probability weight on the agentic-erosion case.**
- The ex-Bedrock PM: *"a lot of the things that ServiceNow provides can be solved [by agents]… what ServiceNow does can be done with Claude Code or, in the future, Claude for Work and the future of agents picking small pieces of ServiceNow."* He concedes the **system-of-record moat** and the enterprise sales motion.
- ➤ **This is a qualitative-vs-quantitative divergence, which is the kind that persists longest. The erosion thesis attacks NET EXPANSION and GROSS MARGIN before revenue — neither of which shows up in an EPS line until it already has. The observable to track is NRR and gross-margin trajectory, not revenue growth.**
- ⚠️ **Weight it appropriately: the expert volunteered he is only *"starting to study"* the name at the analyst's prompt. This is an informed outsider on the technology, not a specialist on the business.**

### 3. 🔴 BARCLAYS vs THE EX-BEDROCK OPERATOR — A DIRECT CONFLICT ON HYPERSCALER INDIRECT-API ECONOMICS

| Source | Claim |
|---|---|
| **Barclays** (08-28) | Models **"Indirect Hyperscaler Fees" at 20% of customer spend** — the cloud takes a fee on top of the lab's token revenue |
| **Ex-AWS Bedrock PM** (08-27) | *"AWS doesn't charge any premium. They get discounts from Anthropic, and that's how they're trying to make money… **it's actually cheaper to go to Bedrock than to run an API through Anthropic** for enterprises"* (because committed-spend cloud discounts apply on Bedrock and not on the lab's own API) |

- **Reconcilable if Barclays' 20% is a WHOLESALE SPREAD (buy-side-of-the-trade margin) rather than a markup on list price — the customer can then pay less at Bedrock while AWS still books ~20 points.** But the two are **not obviously the same number**, and one is a model while the other is an operator's account of actual pricing.
- ➤ **LEFT UNRESOLVED ON PURPOSE. The distinction matters for [[AMZN]]/[[MSFT]]/[[GOOG]] gross-margin modelling and for whether frontier-lab API pricing power is being taxed by distribution or subsidised by it. Recorded in both the company pages and [themes/tokenmaxxing.md](../themes/tokenmaxxing.md).**

### 4. 🔴 [[KIOXIA]] — GOLDMAN RUNS ABOVE CONSENSUS, AND THE GAP WIDENS WITH HORIZON (the cycle-duration bet, quantified)

Basis: Kioxia FY ends **March**; GS "3/27E" = BBG **1FY**. Units ¥bn.

| | GS (08-25) | BBG consensus | GS vs cons |
|---|--:|--:|--:|
| **Revenue FY3/27E** | ¥10,405.2 | ¥9,996.2 | **+4.1%** |
| **Revenue FY3/28E** | ¥13,874.3 | ¥13,025.6 | **+6.5%** |
| **Revenue FY3/29E** | ¥16,364.1 | ¥14,549.3 | **+12.5%** |
| **EPS FY3/27E** | ¥10,827.8 | ¥10,264.1 | **+5.5%** |
| **EPS FY3/28E** | ¥14,918.7 | ¥14,053.4 | **+6.2%** |
| **EPS FY3/29E** | ¥17,669.1 | ¥16,144.5 | **+9.4%** |

- **GS is a modest bull in FY1 and a real bull in FY3 — the divergence is monotonically increasing, which is the signature of a DURATION disagreement rather than a level disagreement.** That maps exactly onto GS's stated thesis (*"tightness will last through CY27"*, *"a higher level of profits is sustainable compared to past NAND cycles"*).
- ⚠️ **Note the sign contrast with [[SNDK]] directly above: consensus has Sandisk FY29 revenue −10.1% while it has Kioxia FY3/29 GROWING. Two NAND makers, opposite consensus shapes one year apart on a fiscal-year offset. Worth a dedicated check — either the fiscal-calendar offset explains it (Sandisk FY29 ≈ Kioxia FY3/29-to-3/30) or consensus is carrying an inconsistency across the NAND complex.** Flagged as the top follow-up from this run.
- **No Capstone house model for KIOXIA** — baseline (2) unavailable.

### 5. ⚠️ [[CRWV]] / [[NBIS]] — CONSENSUS PUTS FIRST PROFIT IN EXACTLY THE YEAR TWO INDEPENDENT SOURCES SAY THE COMPETITIVE WINDOW OPENS

| BEST_EPS | 1FY | 2FY | 3FY |
|---|--:|--:|--:|
| **CRWV** | −$3.896 | −$1.775 | **+$1.376** |
| **NBIS** | −$2.022 | −$1.737 | **+$0.284** |

- Both cross into profit at **3FY ≈ 2028** — the same year **Barclays** says *"hyperscalers likely start to lose market share of AI lab training and inference… when backstopped AI infrastructure projects come online"*, and within the *"three years down the line"* the ex-Bedrock PM gives for CoreWeave/Nebius becoming genuine competitors.
- ➤ **Two unrelated sources and the consensus EPS curve all point at 2028. That is unusually tight cross-corroboration for a forward risk, and it argues the neocloud re-rating is a 2027 event (anticipation) rather than a 2028 one.**
- ⚠️ **The bear half is equally sourced and belongs beside it: today the workload is RENTED INFERENCE, not resident application or data — *"my application doesn't run on CoreWeave, my data doesn't stay with CoreWeave."* Moving up the stack is the stated precondition, and it is not yet evidenced.**

### 6. ⚠️ [[SAMSUNG]] / [[SKHYNIX]] — BofA's PUBLISHED CONSENSUS COLUMN IS ~3-4x BELOW ITS OWN ESTIMATES (recorded, NOT adjudicated)

Both BofA Korea notes were **skipped as already-ingested**, but their estimate tables carry a divergence large enough to log:

| | BofA 2026E | Consensus (Visible Alpha, per BofA's own table) | BofA vs cons |
|---|--:|--:|--:|
| **Samsung EPS** | ₩45,212 | ₩33,551 | **+34.8%** |
| **SK Hynix EPS** | ₩363,321 | ₩86,813 | **+319%** |

- ⚠️ **RECORDED AS PRINTED, NOT ADJUDICATED, per the standing rule against rejecting broker models on plausibility (this wiki has now been wrong in BOTH directions on Korean memory numbers — the JPM 77%/52% margin rejection, and the 08-28 MU/SNDK consensus-line deletion).**
- ⚠️ **SAMSUNG MUST BE RECONCILED AT NET INCOME, NEVER EPS** — the common-vs-preferred share-count trap means broker headline EPS (common only) is not comparable to BBG (preferred-inclusive). BofA net income 2026E **₩301,579bn** / 2027E **₩403,418bn** is the comparable line. The SK Hynix gap is too large to be a share-count artifact and is more likely a **stale Visible Alpha panel** in a cycle where estimates are moving faster than the panel refreshes.
- ➤ **No action taken. Logged so the next `/wiki-consensus` run can test the SK Hynix line against a fresh BBG pull rather than against BofA's embedded VA column.**

---

## ✅ CONFIRMS (no action)

### 7. [[AMZN]] / [[GOOG]] — Barclays' cloud AI-revenue lines are small enough vs consensus totals to be non-contradictory

Basis: Barclays is **calendar '26E**; BBG 1FY is the company fiscal year (≈CY for both).

| | Barclays AI revenue '26E | BBG 1FY total revenue | AI as % of total |
|---|--:|--:|--:|
| **AWS** | $37bn | $828.6bn (AMZN consolidated) | **~4.5%** |
| **GCP** | $37bn | $432.9bn (GOOG consolidated) | **~8.5%** |

- These are **AI-only subsets of a segment**, not comparable to consolidated consensus, and nothing in them contradicts the existing wiki marks. **Recorded for scale, not as a variance.**
- ⚠️ **Barclays' AWS = GCP parity at a flat 30% share each is ASSERTED, not derived. Do not adopt it as a share call** — it sits against this wiki's own evidence of Google Cloud outgrowing peers (GCP 2Q26 +82%, already on [themes/tokenmaxxing.md](../themes/tokenmaxxing.md)).
- **Azure is not broken out at all** (inside Barclays' "Other Cloud" 40% bucket, $49/$116/$201bn '26E-'28E) — so no MSFT comparison is possible from this note. MSFT's June fiscal year would require a re-basis in any case.

### 8. [[GOOG]] — the house model is untouched by tonight's sources

Capstone official model (`Google Modelo oficial.xlsx`, 2026-06-05): revenue **$403 / $505 / $641bn** (25/26/27E), EPS **$8.41 / $11.80 / $16.20**, capex **$91 / $183 / $310bn**. House EPS '27E **$16.20 vs BBG 2FY $16.484** — **the house is now −1.7% BELOW consensus**, having been flagged on-page as *"above consensus (~$14.5)"* when written in June. ➤ **Consensus has caught up to and slightly passed the house. Not caused by tonight's ingest, but it means the page's "house above consensus" framing is now STALE and should be re-marked at the next `/wiki-consensus`.** Barclays' GCP AI line ($37bn '26E) is a subset of the house's cloud revenue and does not challenge it.

### 9. [[META]] — the Mizuho backfill is immaterial against both consensus and the house

| | Value | vs BBG 1FY revenue $254.0bn | vs house 2026E revenue $257bn |
|---|--:|--:|--:|
| Mizuho subscription, medium-term | **~$8bn** | ~3.1% | ~3.1% |
| Mizuho subscription, longer-term | **$10bn+** | ~3.9% | ~3.9% |
| Mizuho incremental OI (50-70% margin) | **$4.0-5.6bn** | — | vs house EBIT margin ~37% '26E |

- Mizuho's PT **$835** (05-28 and 06-03, unchanged across both notes) sits **above the Capstone base PT $688** and just below the house **bull $840**. ➤ **The house bull case and Mizuho's base case are the same number — a useful calibration, and it means Mizuho's subscription optionality is roughly what the house already needs for its bull scenario.**
- ⚠️ **Both notes are ~3 months stale and are tagged as backfill in-page; neither supersedes any current META mark.**

### 10. [[INTC]] — the $550m Veolia UPW contract is real but immaterial to the P&L

- **$550M over 16 years ≈ ~$34m/yr** against BBG 1FY revenue **$63.0bn** = **~0.05%.** ✅ **No estimate impact.**
- ➤ **The value is NOT the dollars — it is (a) the first hard price for ultrapure-water scope per leading-edge fab, a line this wiki's fab-capex work has carried as unsized, and (b) the siting constraint: Intel Chandler and TSMC Arizona share one water system under DC-driven pressure, in a state that has just imposed a three-year DC tax-incentive moratorium.**

### 11. [[SHOP]] — the Morgan Stanley backfill marks are stale and correctly quarantined

- MS 07-19: **OW, price $126, PT $192 (+53%)**, ~10.5x/8.6x EV/revenue, ~73.3x/56.5x P/E. Against BBG today: **BEST_EPS 1FY $1.898 / 2FY $2.474 / 3FY $3.301.**
- ✅ **Tagged 📚 BACKFILL in-page with an explicit "NOT the current PT ladder" warning. No drift introduced.**

---

## Baseline coverage for this run

| Baseline | Status |
|---|---|
| **(1) Prior wiki comments** | ✅ Done — and it produced the run's best finding (SNDK: Bernstein's −11.9% already on-page + consensus −10.1% + Bristlemoon's mechanism = three legs). |
| **(2) Capstone house models** | ⚠️ **Partial.** Only [[GOOG]] and [[META]] carry a `## Capstone estimates` block among tonight's affected names. **Missing for AMZN, MSFT, SNDK, KIOXIA, INTC, NOW, ORCL, CRWV, NBIS, SHOP.** The SNDK gap is the costly one — it is the wiki's largest standing divergence and has no house number to test against. |
| **(3) BBG consensus** | ✅ **LIVE.** Wrapper healthy; `BEST_FPERIOD_OVERRIDE` must be passed as a **kwarg**, not in an `overrides={}` dict (the dict form raises `BAD_ARGS / Invalid override field`). |

## Follow-ups ranked

1. **🔴 Resolve the NAND consensus-shape inconsistency:** consensus has [[SNDK]] FY29 revenue **−10.1%** but [[KIOXIA]] FY3/29 **growing**. Establish whether the fiscal-year offset accounts for it before either mark is used in a pitch.
2. **🔴 Build (or locate) a Capstone house model for [[SNDK]]** — the largest open divergence on the wiki currently has no house baseline.
3. **Re-mark the [[GOOG]] page's "house above consensus" line** — house '27E EPS $16.20 is now −1.7% *below* BBG 2FY $16.484.
4. **Test the BofA [[SKHYNIX]] consensus column** (₩86,813 vs BofA ₩363,321) against a fresh BBG Korea pull at the next `/wiki-consensus`; suspected stale Visible Alpha panel, not a real 3x view gap.
5. **Track the Barclays-vs-operator indirect-API conflict** (20% fee vs "no premium") — first company disclosure of AI-lab GAAP financials should settle it.
