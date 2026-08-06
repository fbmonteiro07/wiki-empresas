# Reconciliation — 2026-08-05 (/run-inbox)

_Every NEW quantitative datapoint from this run, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus. Qualitative/thematic content is out of scope._

**Sources reconciled:** SpaceX Q2 2026 earnings call (Bloomberg FINAL TRANSCRIPT, 2026-08-04) + 6 AlphaSense expert calls (interviews Feb–Jul 2026). One expert call (NVDA, Apr-2025 interview) and one (ProsperOps/FinOps) were dropped at routing and contribute nothing here.

## Baseline availability — read this before the tables

| Baseline | Status |
|---|---|
| **(1) Prior wiki comments** | ✅ Available (on disk). |
| **(2) Capstone house models** | ⚠️ **N/A for SPCX and CRWV — neither is in `_data/house.json`** (house covers AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM only). No house bridge can be built for the two names this run actually moves. |
| **(3) BBG consensus** | ⚠️ **LIVE FETCH FAILED — `HTTP 503: Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal`.** ✅ **BUT the on-disk snapshot `_data/estimates.json` is `asof 2026-08-05` with `lrq 2026-06-30` — i.e. it was captured TODAY and is POST-PRINT, so it is a valid consensus baseline and is used below.** No web data was substituted. **Action: log in to the Terminal / reconnect the Capstone VPN if a live re-pull is wanted; the conclusions below do not depend on it.** |

⚠️ **DATA-QUALITY WARNING FOUND IN THIS RUN — `estimates.json` CY-sum capex for SPCX is broken.** The `CY2026.capex` field reads **$35.35bn**, but its own quarterly components sum to **$55.3bn** (Q1 $10.0 actual + Q2 $18.4 actual + Q3E $11.47 + Q4E $15.40). **A ~$20bn internal inconsistency. Use SUM-OF-QUARTERS for SPCX capex, never the CY field.** This is the same class of defect already recorded for CY-sum revenue elsewhere in the wiki. ⚠️ **`CY2027.capex` reads $135.59bn against CY2027 revenue of $91.52bn — capex at 148% of revenue, with no quarterly components available to check it. Treat as UNVERIFIED and do not cite.**

---

## 🔴 DIVERGES — the alpha

### 1. SPCX capex: consensus is ~27% below the guide management just gave, and the gap is concentrated in Q3

| | Q3-26 | Q4-26 | 2H-26 |
|---|---|---|---|
| **Management guide** (CFO: *"the next two quarters are very similar to the current quarter from a CapEx level perspective"*, i.e. ≈ Q2's $18.4bn) | **~$18.4bn** | **~$18.4bn** | **~$36.8bn** |
| **BBG consensus** (`estimates.json`, asof 08-05, post-print) | **$11.47bn** | **$15.40bn** | **$26.87bn** |
| **Variance** | **cons 38% below** | **cons 16% below** | **cons $9.9bn / 27% below** |

**Why it is still open despite the print being a day old:** the snapshot is dated 08-05, so this is *post-print* consensus that has **not** absorbed the capex guide. MS caught it — *"the company is guiding to a SIMILAR LEVEL OF CAPEX PER QUARTER FOR THE REMAINDER OF THE YEAR, implying approximately incremental ~$18BN OF 2H CAPEX ON TOP OF OUR PRIOR FORECAST"* (Adam Jonas, 2026-08-05) — and the current consensus mark sits roughly halfway between MS's old and new numbers, i.e. the Street is mid-revision.
**Trade-relevant read:** this is a **negative** revision still to come on the cash line, into a name whose bear case just migrated from segment losses to cash burn. It is the mechanism behind "higher estimates offset by higher capex" and behind a +67% EBITDA beat producing a −5% to −7% stock. **Watch: whether Q3 consensus capex converges to ~$18bn over the next two weeks. If it does not, the Q3 print is a capex miss waiting to happen.**
⚠️ Caveat: "very similar to the current quarter" is management's phrasing, not a formal guide, and Q2's $18.4bn excludes the separate $856M EchoStar spectrum-credit payment.

### 2. SPCX: the $100bn December ARR claim and consensus Q4 revenue are NOT mutually consistent

Management defined it precisely (CFO Johnsen): **$100bn of ARR "based on our expected revenue in the MONTH OF DECEMBER"** → **December revenue must be ~$8.33bn.** Musk: *"not a question mark… that's what we would achieve if we basically did nothing… it probably will be higher than that."*

| | Value |
|---|---|
| Implied December-2026 monthly revenue | **$8.33bn** |
| BBG consensus Q4-26E revenue | **$17.78bn** |
| ⟹ implied Oct + Nov combined | **$9.45bn** (avg **$4.72bn**/mo) |
| Consensus Q3-26E monthly average | **$4.13bn**/mo |
| ⟹ **implied Nov → Dec step** | **+76% in a single month** |

**Either consensus Q4 revenue is materially too low, or the $100bn ARR figure is not achievable on a smooth ramp.** Both cannot hold. **If instead December is reached by a smooth ramp (~$6.5 / $7.4 / $8.33bn), Q4 revenue is ~$22.2bn and consensus is ~20% too low.**
**Which way to lean:** the ramp mechanics management disclosed are *back-loaded and dated* — the [[GOOG]]/[[ANTHROPIC]] deals *"start to ramp either later this quarter or in October"*, and a further **$6.7bn of cloud revenue contracted in the first weeks of Q3 "begins ramping starting in October."** A genuinely December-weighted quarter is therefore not absurd. ⚠️ **But note the definitional soft spot: annualizing a single month makes ARR maximally flattering to exactly this shape of ramp. This is the single most checkable claim on the page and it resolves at the Q3 print (early Nov) and definitively at Q4.**

### 3. SPCX management's compute, power and $/W numbers are 2-3x every Street baseline on the page

| Metric | Management (08-04) | Street / prior wiki | Gap |
|---|---|---|---|
| Nameplate compute, exit-2027 | **~10 GW** ("closer to 10 than 5") | **MS 4.15 GW** | **2.4x** |
| **Power & cooling, exit-2027** (⚠️ **DIFFERENT BASIS — see below**) | **15-20 GW** ("tentative target 20… probably close to 15") | **no Street baseline exists** | **net-new** |
| Monetization per watt (Rubin) | **$30-50/W** = $30-50bn/GW | **MS base case $16.5/W**; New Street: ~$50bn/GW *"premium may not last"* vs [[CRWV]] ~$12bn/GW; Gavin Baker ~$50bn/GW | **1.8-3.0x MS** |
| $1T revenue year | **2030** (from 2031; *"non-zero chance of 2029"*) | **MS 2030 revenue $319bn** | **~3.1x MS** |
| Starship cadence, ~Aug-2027 | **"at least one flight a day"** | **New Street: model needs ~1/week, runs ~1yr behind Elon** | **~7x** |

⚠️⚠️ **THE GW-BASIS RULE APPLIES AND IS THE MOST IMPORTANT LINE IN THIS REPORT: ~10 GW is IT LOAD / nameplate compute; 15-20 GW is POWER-PLANT / power-and-cooling level. Per `_meta/assumptions.md` these must never be netted, averaged or compared. The overbuild is deliberate — *"our goal is to have far more power cooling and electrical equipment than we have GPUs… given the relative expense of GPUs versus balance of system"* — implying a target ratio of ~1.5-2x power capacity to IT load.**
**Where the alpha is:** the 15-20 GW power figure has **no Street or house baseline at all**, and if the overbuild behaviour generalises to other allocation-constrained buyers, every GW-based sizing in [themes/ai-datacenter-power](../themes/ai-datacenter-power.md) built off *IT load* understates the turbine / transformer / switchgear / genset / cooling order book by 50-100%.
⚠️ **Counterweight retained: FUNDA's six independent channel sources converged on 3.5-5 GW against the ~8-10 GW ambition (P(8 GW) ≈ 12-17%), and Musk pre-discounted his own 20 GW to ~15 GW in the same sentence. Treat all of these as PROCUREMENT INTENT, not delivery forecasts.**

### 4. GPU price direction: the AWS practitioner and the buy side flatly contradict each other

| Source | Claim |
|---|---|
| **AlphaSense expert, ex-AWS BD** (interview 2026-02-23) | *"Price degradation for high-end GPUs typically follows the release of new generations, with a **20-25% DROP OVER 18 MONTHS**; neo-clouds experience similar percentage declines but from a lower base."* |
| **AlphaSense expert, ex-MSFT/ex-CoreWeave** (interview 2026-04-23) | Expects supply growth to **reduce the scarcity premium**, with mix shifting from spot to committed long-term contracts at **greater discounts**. |
| **Gavin Baker / Atreides** (~2026-08-04, on [[NVDA]]) | **B200 rental prices UP 50-60% in six-to-seven months.** |
| **[[SPCX]] CFO** (2026-08-04) | *"increasingly favorable economics with each agreement we sign"*; **sub-1-year payback** on new compute capital. |

**Not reconcilable as stated, and the split is chronological: both expert views are Feb/Apr-2026 FORECASTS of compression; both 08-04 datapoints are August OBSERVATIONS of the opposite.** The honest reading is that the experts described the *normal* post-generation decay curve and the 2026 shortage has suspended it. **The open question — and it is the central one for [[CRWV]], [[NBIS]] and the neocloud complex — is whether the 20-25%/18-month decay reasserts when supply catches up.** ⚠️ **Do NOT average these. Track which regime holds at the next contract-renewal datapoint.**

---

## ✅ CONFIRMS — no action

| New datapoint | Baseline | Read |
|---|---|---|
| **SPCX Q2 rev $7.81bn / adj EBITDA $3.5bn** | Wiki already scored vs Visible Alpha ($6.9bn / $2.1bn) | Already logged; transcript confirms the release recap. No change. |
| **SPCX AI segment adj. EBITDA +$1.1bn (from $(609)M in Q1-26)** | Wiki bear case cited the loss trail | ⚠️ **Supersedes the segment-loss bear leg — handled as thesis drift in `SPCX.md ## Changelog`.** Not a consensus variance; consensus has no segment split on disk. |
| **SPCX CY2026 consensus revenue $41.67bn** | Sum-of-quarters = $42.67bn (Q1 $4.69 + Q2 $7.81 actual + Q3E $12.39 + Q4E $17.78) | Internally consistent within ~$1bn. ✅ **The revenue CY-sum is sound — only the CAPEX field is broken.** |
| **SPCX CY2026 consensus EBITDA $18.99bn** | Sum-of-quarters implies Q1 ≈ $(1.0)bn | Consistent with a negative Q1. ✅ Sound. |
| **SPCX balance sheet: $100bn cash, $47.5bn backlog, $25bn IG notes @ 5.855% WAC / 11.7yr** | Wiki carried MS's *"~$84bn/yr external capital '27-34"* requirement and The Information's *"doesn't have the same deep pockets"* | ✅ **Confirms the funding question is DEFERRED, not solved:** $100bn covers ~5-6 quarters at the guided ~$18.4bn/qtr burn. 2027+ financing need stands. |
| **AWS actual utilization "closer to 90%" vs 70-80% base case** (ex-AWS BD, interview 2026-03-12) | **MS's GenAI ROIC framework on [[AMZN]] assumes 75% utilization** | ✅ **Confirms MS is CONSERVATIVE on its single most sensitive input.** At ~90%, MS's ~31% IaaS ROIC is understated. Directionally supports the AWS bull case vs the Redburn $230 margin short. |
| **AMZN FY26 capex** | Wiki: guided ~$200bn → ~$220bn; **BBG CY2026 $213.9bn** | ✅ Consensus sits mid-range. No variance. |
| **Neocloud payback discipline: "2-3 years max acceptable, risk >3.5-4 years"** (ex-CoreWeave expert) | **[[CRWV]] BBG consensus: CY26 capex $32.39bn; CY27 EBITDA $15.70bn** | ✅ **On a 1-year deployment lag, consensus implies ~2.1 years — INSIDE the expert's acceptable band.** (Unlagged CY26/CY26 gives 4.4yr and CY27/CY27 gives 2.5yr; the lagged figure is the right one given the expert names "deployment lag" as a tracked KPI.) **Consensus is underwriting a payback the practitioner would sign off on.** |
| **Hyperscaler 3-5yr vs neocloud 2-3yr payback asymmetry** | Wiki [[CRWV]] bear case (leverage, customer concentration, GPU residual) | ✅ Practitioner corroboration of a structural point the page already makes. Mechanism, not new numbers. |
| **Musk: memory supply +20%/yr vs demand +200%/yr** | Wiki carried the machine-translated version | ✅ **Substance confirmed verbatim.** Not a new number — an upgrade of source quality. ⚠️ The transcript adds a *counterweight* the relay stripped (intelligence-per-watt deflation), logged on [themes/hbm-memory](../themes/hbm-memory.md). |
| **Starlink Q2 net adds +1.7M (vs 1.4M Q1), ARPU flat $66** | Visible Alpha: 12.1mn subs / $65.5 ARPU; actual 12M / $66 | ✅ Subs a hair light on total, but **net adds ACCELERATED** — a better print than "in line." No consensus net-add mark on disk to score against. |
| **"Jensen says fast inference is 30% of the market"** (ex-Cerebras expert) | Wiki [[CEREBRAS]] page: *"Jensen calls fast-inference ~20%"*; BofA/Arya ~10-20% | ⚠️ **DISCREPANCY LOGGED, NOT RESOLVED** — 20% and 30% both attributed to Jensen by different sources, and the expert prefixed his with *"if I even believe Jensen."* **The 30% figure was NOT adopted.** Flagged inline on the CEREBRAS page. |

---

## Provenance flags carried into the pages

- ⚠️ **Three of the six ingested expert calls are the SAME person** — a Former Principal BD Manager (WW GenAI) at AWS who left Feb-2024 and subsequently ran GenAI strategy/BD at [[CEREBRAS]] until Jul-2025. **He disclosed on the record that he STILL OWNS CEREBRAS STOCK** (*"my answer will be biased, but I still own the stocks of Cerebras"*). Every Cerebras claim is weighted accordingly on that page.
- ⚠️ **All expert-call interviews predate the AMZN Q2 FY26 print (2026-07-30)** — dates run Feb-23, Mar-12, Apr-01, Apr-23, Jul-16. They were filed as **structural** evidence, not intra-quarter flow.
- ⚠️ **The "2 million chips / 27 data centers / 1 GW" walkthrough on [[AMZN]] was EXPLICITLY labelled by the expert as *"a hypothetical number"* and MUST NOT be cited as a forecast.** Logged only because the shape of the calculation is how capacity is actually sized.
- ⚠️ **The AWS↔Cerebras "disaggregated inference" architecture (Trainium leg + CS-3 leg) is one former employee's account and is UNCORROBORATED by either company in this wiki.**

## Open items for the next run

1. **Re-pull BBG live** once the Terminal is logged in — specifically to see whether SPCX Q3 capex consensus has converged toward the ~$18.4bn guide (DIVERGES #1) and whether Q4 revenue has moved toward the ARR-implied ~$22bn (DIVERGES #2).
2. **Fix or flag `estimates.json` SPCX capex** — the CY2026 field ($35.35bn) contradicts its own quarterly sum ($55.3bn) by ~$20bn, and CY2027 ($135.59bn = 148% of revenue) is unverifiable. Downstream consumers of the CY capex field are wrong for this ticker.
3. **No house model exists for SPCX or CRWV** — the two names this run actually moves cannot be bridged to Capstone numbers. Worth deciding whether SPCX warrants one now that it is public, reporting, and carrying the largest single-account compute read-through in the wiki.
