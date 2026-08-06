# Reconciliation — 2026-08-05 (/run-inbox)

_Every NEW quantitative datapoint from this run, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus. Qualitative/thematic content is out of scope._

**Sources reconciled:** SpaceX Q2 2026 earnings call (Bloomberg FINAL TRANSCRIPT, 2026-08-04) + 6 AlphaSense expert calls (interviews Feb–Jul 2026). One expert call (NVDA, Apr-2025 interview) and one (ProsperOps/FinOps) were dropped at routing and contribute nothing here.

## Baseline availability — read this before the tables

| Baseline | Status |
|---|---|
| **(1) Prior wiki comments** | ✅ Available (on disk). |
| **(2) Capstone house models** | ⚠️ **N/A for SPCX and CRWV — neither is in `_data/house.json`** (house covers AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM only). No house bridge can be built for the two names this run actually moves. |
| **(3) BBG consensus** | ✅ **RESOLVED 2026-08-06 via `/wiki-consensus`** (was ⚠️ **LIVE FETCH FAILED — `HTTP 503: Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal`** at ingest; the on-disk snapshot `asof 2026-08-05`, `lrq 2026-06-30`, post-print, was used as a valid baseline). Live pull `estimates.json` **asof 2026-08-06**, **98/98 names, 0 records byte-identical to the 08-05 vintage and 0 records missing a live `px` — i.e. no silent carry-overs**, plus an ad-hoc live `PX_LAST` / `BEST_TARGET_PRICE` / `EQY_REC_CONS` pull the same date for the four names carrying findings here. **No web data was substituted at any point.** **The re-pull answered open item #1 and it went AGAINST the direction the report expected — see the resolution block below.** |

⚠️ **DATA-QUALITY WARNING FOUND IN THIS RUN — `estimates.json` CY-sum capex for SPCX is broken.** The `CY2026.capex` field reads **$35.35bn**, but its own quarterly components sum to **$55.3bn** (Q1 $10.0 actual + Q2 $18.4 actual + Q3E $11.47 + Q4E $15.40). **A ~$20bn internal inconsistency. Use SUM-OF-QUARTERS for SPCX capex, never the CY field.** This is the same class of defect already recorded for CY-sum revenue elsewhere in the wiki. ⚠️ **`CY2027.capex` reads $135.59bn against CY2027 revenue of $91.52bn — capex at 148% of revenue, with no quarterly components available to check it. Treat as UNVERIFIED and do not cite.**

---

## ✅ BBG live resolution — 2026-08-06

### Did the live re-pull change the consensus this report was built on? — **Yes, on SPCX, and the Q3 capex leg moved the WRONG WAY.**

The pull is clean (98/98 names, no carry-overs). Of the two names carrying findings, **CRWV consensus is unchanged to the decimal** and **SPCX moved on every line inside 24 hours of the print.** The report set an explicit watch condition on SPCX Q3 capex — *"watch whether Q3 converges to ~$18bn within two weeks; if not, Q3 is a capex miss waiting to happen"* — and **it did not converge: it fell.**

| SPCX consensus line | 08-05 (in this report) | **08-06 (live)** | Δ | vs management guide | What it does to the finding |
|---|--:|--:|--:|--:|---|
| **Q3-26E capex** | $11.47bn | **$10.83bn** | **−5.6%** | **−41.1%** vs ~$18.4bn | 🔴 **① STRENGTHENS materially.** The Street moved *away* from the guide. Even the **street HIGH ($14.51bn) is 21% below** it — **not one analyst is at management's Q3 number.** |
| **Q4-26E capex** | $15.40bn | **$18.19bn** | **+18.2%** | **−1.1%** vs ~$18.4bn | ① **Q4 fully converged.** Street high $34.18bn. |
| 2H-26E capex | $26.87bn | **$29.02bn** | +8.0% | **−21.1%** (gap **$7.8bn**) | ① Gap narrowed from $9.9bn/27% to $7.8bn/21% — **but entirely via Q4.** |
| Q3-26E revenue | $12.39bn | **$12.72bn** | +2.7% | — | ② Street high $16.02bn. |
| **Q4-26E revenue** | $17.78bn | **$18.71bn** | **+5.2%** | — | ② **NARROWS, direction supports the finding.** Implied Nov→Dec step falls **+76% → +61%**; consensus now **15.7% below** the smooth-ramp $22.2bn (was ~20%). Street high **$29.44bn** sits *above* the smooth ramp. |
| CY2027 revenue | $91.52bn | **$97.98bn** | **+7.1%** | — | ③ Base rose 7% in a day; management's $1T-in-2030 is still ~3x MS's $319bn. |

**The single most important read: the Street absorbed the capex guide into Q4 ALONE and took Q3 down.** Consensus is modelling a back-half-loaded capex curve that management explicitly denied (*"the next two quarters are very similar to the current quarter from a CapEx level perspective"*). **The Q3 capex-miss risk flagged in ① is now MORE likely than when this report was written, not less** — and it is un-hedged by the street high.

### BBG consensus pull — live PT / spot / rating, 2026-08-06

_This report carried no PT rows at ingest, and `estimates.json` still has no `BEST_TARGET_PRICE` field (4th consecutive run needing an ad-hoc `bdp` pull)._

| Ticker | Spot | Cons PT | Upside | Rating | Read |
|---|--:|--:|--:|--:|---|
| **SPCX** | 111.78 | 222.43 | +99.0% | 4.41/5 | 🔴 **The Street carries +99% upside on a name whose own Q3 capex consensus sits 41% BELOW the guide management just gave.** PT unmoved on the print ($222.60 on 08-05) even though consensus revenue and capex both moved — the PT is not yet reflecting the cash line. |
| **CRWV** | 88.94 | 138.59 | +55.8% | 4.19/5 | Consensus estimates unmoved to the decimal this run; the GPU-pricing-regime debate (④) is unexpressed in both estimates and PT. |
| **NBIS** | 211.14 | 265.40 | +25.7% | 4.29/5 | Neocloud comp read-across for ④; no new datapoint this run. |
| **AMZN** | 274.29 | 326.47 | +19.0% | 4.85/5 | 📌long. Highest-rated name in the run; CY2026 capex $214.16bn confirms mid-guide. Lowest upside of the four — the least contested. |

⚠️ **SPCX's PT is unmoved on the print** ($222.43 vs the $222.60 logged 08-05) even though consensus revenue and capex both moved. **The Street is carrying +99% upside on a name whose own capex consensus sits 41% below the guide management just gave for next quarter** — the PT is not yet reflecting the cash line. That tension is the cleanest expression of ① and ②.

### Other rows re-placed against the fresh pull
- **CRWV — consensus UNCHANGED to the decimal** (CY26 rev $12.55bn / EBITDA $7.32bn / capex $32.39bn; CY27 rev $25.05bn / EBITDA $15.70bn). **④ stays open and unexpressed:** the GPU-pricing-regime question is not in estimates yet. The CONFIRMS payback row also holds exactly — lagged CY26 capex ÷ CY27 EBITDA = **2.06 years**, still inside the practitioner's 2-3yr band.
- **AMZN CY2026 capex $213.88bn → $214.16bn.** CONFIRMS holds — still mid-range vs the guided ~$200→220bn.

### ⚠️ Both `estimates.json` SPCX capex defects PERSIST in the fresh pull — this is a script-level CY-sum bug, not a one-day blip
| Field | 08-06 value | Cross-check | Verdict |
|---|--:|--:|---|
| `SPCX.CY2026.capex` | **$37.50bn** | sum-of-quarters = **$57.42bn** (Q1 $10.0a + Q2 $18.4a + Q3E $10.83 + Q4E $18.19) | 🔴 **~$19.9bn internal gap — still broken.** Use sum-of-quarters. |
| `SPCX.CY2027.capex` | **$151.11bn** | = **154% of** CY2027 revenue ($97.98bn); no quarterly components | 🔴 **Still UNVERIFIED — do not cite.** |

**Open item #2 stays open and is now confirmed reproducible across two independent pulls.** Any downstream consumer of the CY capex field is wrong for this ticker.

---

## Where the new data DIVERGES

_BBG column below carries BOTH vintages: the 08-05 on-disk snapshot this report was written against, and the **08-06 live re-pull** that resolved it._

| Name | New datapoint | Prior wiki / house | BBG consensus (08-05 snapshot → **08-06 live**) | Read (the edge) |
|---|---|---|---|---|
| **SPCX** | CFO: Q3 and Q4 capex *"very similar to the current quarter"* → **~$18.4bn/qtr, ~$36.8bn for 2H26** | Page carried MS's *"~$18bn of 2H capex ON TOP OF OUR PRIOR FORECAST"* (08-05); no house model exists for SPCX | 08-05: Q3E $11.47bn · Q4E $15.40bn · 2H $26.87bn → **08-06 LIVE: Q3E $10.83bn (−5.6%) · Q4E $18.19bn (+18.2%) · 2H $29.02bn**; Q3 street-**high** only $14.51bn | 🔴 **STAYS — and the Q3 leg STRENGTHENED.** _Original 08-05 read:_ consensus $9.9bn / 27% below the guide, 38% below on Q3 alone; snapshot post-print so the Street was mid-revision, not un-informed; a negative cash-line revision still to come into a name whose bear case just migrated from segment losses to burn; **watch whether Q3 converges to ~$18bn within two weeks.** → ✅ **RESOLVED 08-06: it did NOT converge — it FELL to $10.83bn (−41.1% vs guide).** The Street absorbed the guide into **Q4 alone** (now −1.1% vs guide). **Not one analyst is at the Q3 guide — the street high is still 21% below it.** 2H gap narrows to $7.8bn / 21%, but only via Q4. **Consensus is modelling a back-half-loaded capex curve management explicitly denied — so the Q3 capex miss is MORE likely now, not less.** |
| **SPCX** | *"$100 billion of ARR… based on our expected revenue in the MONTH OF DECEMBER"* → **Dec-26 revenue must be ~$8.33bn** | Page had flagged the figure "IMPLAUSIBLE AS TRANSCRIBED" and suggested $10bn — **that flag is now withdrawn**; the scope, not the magnitude, was wrong | 08-05: Q4-26E revenue $17.78bn → **08-06 LIVE: $18.71bn (+5.2%)**; Q3E $12.72bn (+2.7%); Q4 street-**high $29.44bn** | **The two are not mutually consistent.** _Original 08-05:_ if Dec = $8.33bn, Oct+Nov = $9.45bn (avg $4.72bn/mo) vs a Q3 average of $4.13bn/mo — **an implied +76% single-month Nov→Dec step**; on a smooth ramp Q4 is ~$22.2bn and consensus ~20% too low. → ✅ **08-06: NARROWS, and the direction of revision SUPPORTS the finding.** Oct+Nov now $10.38bn (avg $5.19/mo) vs Q3 avg $4.24/mo ⟹ implied Nov→Dec step **+76% → +61%**; consensus now **15.7% below** the smooth-ramp $22.2bn. **The street high ($29.44bn) sits ABOVE the smooth ramp — the bull tail is already underwriting the December-weighted quarter.** Still not reconciled; **resolves at the Q3 print (early Nov).** |
| **SPCX** | Exit-2027: **~10 GW nameplate compute** AND **15-20 GW power-and-cooling**; **$30-50/W** Rubin monetization; **$1T revenue in 2030**; **"one flight a day"** by ~Aug-27 | MS: **4.15 GW**, **$16.5/W**, **$319bn 2030 revenue**; New Street bear needs **~1 Starship launch/week** and runs a year behind Elon | **No GW, $/W or cadence fields exist on the wrapper — this row stays "no BBG basis" for its core metrics.** CY2027 revenue: 08-05 $91.52bn → **08-06 LIVE $97.98bn (+7.1%)**; CY27 street-high $157.53bn | **Management is 2-3x every Street baseline on the page, and the 15-20 GW power figure has NO Street or house baseline at all.** ⚠️ **Different GW bases — ~10 GW is IT load, 15-20 GW is power-plant level; never net them.** The overbuild is deliberate (*"far more power cooling and electrical equipment than we have GPUs"*), implying **~1.5-2x power capacity to IT load** — if that behaviour generalises, every GW sizing in `themes/ai-datacenter-power` built off IT load **understates the electrical/cooling order book by 50-100%.** ⚠️ FUNDA's six channel sources say 3.5-5 GW (P(8GW) ≈ 12-17%); treat as procurement INTENT. |
| **CRWV** | Two AlphaSense practitioners: high-end GPU prices decay **20-25% over 18 months** post-generation, and the **scarcity premium compresses** as supply matures | Gavin Baker (08-04): **B200 rentals UP 50-60% in 6-7 months**; SPCX CFO (08-04): *"increasingly favorable economics with each agreement we sign"*, sub-1-yr payback | CRWV CY26 rev $12.55bn / EBITDA $7.32bn; CY27 rev $25.05bn / EBITDA $15.70bn — ✅ **08-06 LIVE: UNCHANGED TO THE DECIMAL** (capex CY26 $32.39bn also identical) | **Flatly contradictory — and the split is chronological: both expert views are Feb/Apr-2026 FORECASTS of compression; both August datapoints are OBSERVATIONS of the opposite.** Honest reading: the experts described the normal post-generation decay curve and the 2026 shortage has suspended it. **The open question for the whole neocloud complex is whether 20-25%/18mo reasserts when supply catches up.** ⚠️ Do NOT average. Track at the next contract-renewal datapoint. ✅ **08-06: consensus did not move a decimal, so the pricing-regime question is entirely UNEXPRESSED in estimates — this stays open with no consensus anchor either way.** |

### 1. SPCX capex: consensus is ~27% below the guide management just gave, and the gap is concentrated in Q3

| | Q3-26 | Q4-26 | 2H-26 |
|---|---|---|---|
| **Management guide** (CFO: *"the next two quarters are very similar to the current quarter from a CapEx level perspective"*, i.e. ≈ Q2's $18.4bn) | **~$18.4bn** | **~$18.4bn** | **~$36.8bn** |
| **BBG consensus** (`estimates.json`, asof 08-05, post-print) | **$11.47bn** | **$15.40bn** | **$26.87bn** |
| **Variance** | **cons 38% below** | **cons 16% below** | **cons $9.9bn / 27% below** |
| ✅ **BBG consensus — LIVE re-pull, asof 08-06** | 🔴 **$10.83bn** | **$18.19bn** | **$29.02bn** |
| ✅ **Variance on the live pull** | 🔴 **cons 41% below** | **cons 1% below** | **cons $7.8bn / 21% below** |
| _Street **HIGH** (08-06)_ | _$14.51bn — **still 21% below the guide**_ | _$34.18bn_ | _$48.69bn_ |

**Why it is still open despite the print being a day old:** the snapshot is dated 08-05, so this is *post-print* consensus that has **not** absorbed the capex guide. MS caught it — *"the company is guiding to a SIMILAR LEVEL OF CAPEX PER QUARTER FOR THE REMAINDER OF THE YEAR, implying approximately incremental ~$18BN OF 2H CAPEX ON TOP OF OUR PRIOR FORECAST"* (Adam Jonas, 2026-08-05) — and the current consensus mark sits roughly halfway between MS's old and new numbers, i.e. the Street is mid-revision.
**Trade-relevant read:** this is a **negative** revision still to come on the cash line, into a name whose bear case just migrated from segment losses to cash burn. It is the mechanism behind "higher estimates offset by higher capex" and behind a +67% EBITDA beat producing a −5% to −7% stock. **Watch: whether Q3 consensus capex converges to ~$18bn over the next two weeks. If it does not, the Q3 print is a capex miss waiting to happen.**
⚠️ Caveat: "very similar to the current quarter" is management's phrasing, not a formal guide, and Q2's $18.4bn excludes the separate $856M EchoStar spectrum-credit payment.

### 2. SPCX: the $100bn December ARR claim and consensus Q4 revenue are NOT mutually consistent

Management defined it precisely (CFO Johnsen): **$100bn of ARR "based on our expected revenue in the MONTH OF DECEMBER"** → **December revenue must be ~$8.33bn.** Musk: *"not a question mark… that's what we would achieve if we basically did nothing… it probably will be higher than that."*

| | Value |
|---|---|
| Implied December-2026 monthly revenue | **$8.33bn** |
| BBG consensus Q4-26E revenue (08-05 snapshot) | **$17.78bn** |
| ⟹ implied Oct + Nov combined | **$9.45bn** (avg **$4.72bn**/mo) |
| Consensus Q3-26E monthly average | **$4.13bn**/mo |
| ⟹ **implied Nov → Dec step** | **+76% in a single month** |
| ✅ **BBG consensus Q4-26E revenue — LIVE, asof 08-06** | **$18.71bn** (+5.2%) |
| ✅ ⟹ implied Oct + Nov combined | **$10.38bn** (avg **$5.19bn**/mo) |
| ✅ Consensus Q3-26E monthly average | **$4.24bn**/mo |
| ✅ ⟹ **implied Nov → Dec step** | **+61% in a single month** (narrowed from +76%) |
| ✅ Consensus vs the smooth-ramp $22.2bn Q4 | **15.7% too low** (was ~20%) |
| _Street **HIGH** Q4-26E revenue (08-06)_ | _**$29.44bn** — above the smooth ramp_ |

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
| **AMZN FY26 capex** | Wiki: guided ~$200bn → ~$220bn; **BBG CY2026 $213.9bn** → ✅ **08-06 LIVE $214.16bn (+$0.3bn)** | ✅ Consensus sits mid-range. No variance. **CONFIRMS holds on the live re-pull.** Live PT $326.47 vs spot $274.29 (**+19.0%**), rating 4.85/5 — the highest-rated name in this run. |
| **Neocloud payback discipline: "2-3 years max acceptable, risk >3.5-4 years"** (ex-CoreWeave expert) | **[[CRWV]] BBG consensus: CY26 capex $32.39bn; CY27 EBITDA $15.70bn** → ✅ **08-06 LIVE: both unchanged; lagged payback recomputes to 2.06 yr** | ✅ **On a 1-year deployment lag, consensus implies ~2.1 years — INSIDE the expert's acceptable band.** (Unlagged CY26/CY26 gives 4.4yr and CY27/CY27 gives 2.5yr; the lagged figure is the right one given the expert names "deployment lag" as a tracked KPI.) **Consensus is underwriting a payback the practitioner would sign off on.** |
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

1. ~~**Re-pull BBG live** once the Terminal is logged in — specifically to see whether SPCX Q3 capex consensus has converged toward the ~$18.4bn guide (DIVERGES #1) and whether Q4 revenue has moved toward the ARR-implied ~$22bn (DIVERGES #2).~~ ✅ **DONE 2026-08-06 via `/wiki-consensus`** (98/98 clean, no carry-overs). **Answer: Q3 capex did NOT converge — it fell to $10.83bn, −41.1% vs the guide, with the street high still 21% below it; the guide was absorbed into Q4 alone. Q4 revenue DID move up (+5.2% to $18.71bn), narrowing the ARR inconsistency from a +76% to a +61% implied Nov→Dec step.** ① strengthens, ② narrows but stays open.
2. 🔴 **STILL OPEN — and now confirmed reproducible. Fix or flag `estimates.json` SPCX capex.** Re-checked on the fresh 08-06 pull: `CY2026.capex` **$37.50bn** vs sum-of-quarters **$57.42bn** (~**$19.9bn** gap); `CY2027.capex` **$151.11bn = 154% of** CY2027 revenue, still with no quarterly components to verify. Two independent pulls now reproduce it, so this is a **script-level CY-sum bug for this ticker, not a data blip.** Downstream consumers of the CY capex field are wrong for SPCX.
3. **No house model exists for SPCX or CRWV** — the two names this run actually moves cannot be bridged to Capstone numbers. Worth deciding whether SPCX warrants one now that it is public, reporting, and carrying the largest single-account compute read-through in the wiki. ⚠️ **Raised in priority by the 08-06 pull:** the Street carries **+99% upside** on SPCX while its own Q3 capex consensus sits 41% below management's guide — there is no house number to arbitrate that.
4. 🔴 **NEW — `estimates.json` still carries no `BEST_TARGET_PRICE` field.** This is the **4th consecutive run** that has had to do an ad-hoc `bdp` PT pull to place broker targets. Worth adding `BEST_TARGET_PRICE` + `EQY_REC_CONS` to `fetch_estimates.py` so the PT column is native. ⚠️ Note `TOT_ANALYST_REC_BUY/HOLD/SELL` raise **HTTP 500** on the wrapper — do not add those.
5. **Track next:** whether SPCX Q3 capex consensus starts rising off $10.83bn into the Q3 print (early Nov). If it stays near $11bn, the Q3 capex line is a miss waiting to happen; if it jumps toward $18bn, the revision is simply late rather than absent.

---

_BBG column resolved 2026-08-06 — `estimates.json` asof 2026-08-06 (98/98 names, 0 byte-identical carry-overs, 0 records missing a live px); PT / spot / rating via an ad-hoc live `PX_LAST` + `BEST_TARGET_PRICE` + `EQY_REC_CONS` pull the same date. **① SPCX capex stays in DIVERGES and strengthened on the Q3 leg; ② SPCX revenue stays in DIVERGES but narrowed; ③ SPCX GW/$/W stays in DIVERGES with no BBG basis (CY27 revenue base +7.1%); ④ CRWV stays in DIVERGES with consensus unmoved. Both CONFIRMS rows that referenced consensus (AMZN capex, CRWV payback) held. No row changed section.** No web data was substituted at any point._
