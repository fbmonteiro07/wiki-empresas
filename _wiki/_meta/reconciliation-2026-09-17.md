# Reconciliation — 2026-09-17 (/run-inbox, scheduled/unattended)

**Sources reconciled (quantitative only):** Ciena Investor Forum 2026 (management primary, 2026-09-16) · Goldman Sachs on META (2026-09-13) · Citi on META (2026-09-16) · Morgan Stanley assuming coverage of Online Travel (2026-09-16). The JPM Fal.Con note (2026-09-03) carried **no new estimate and no PT change**, and the JPM security initiation is dated **2023-01-24** — both are excluded from the variance pass by design; the Databricks marketing book carries no numbers at all.

**Baselines used:**
1. **Prior wiki marks** — read off each page before editing.
2. **Capstone house models** — `_data/house.json`, asof 2026-09-17. ⚠️ Covers **9 names: AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TER, TSM**. **There is NO house model for CIEN and none for BKNG** — the two names carrying the largest new datapoints tonight are reconciled against prior wiki marks and BBG only.
3. **BBG consensus — ✅ LIVE THIS RUN.** `bdp()` answered; `PX_LAST` and `BEST_TARGET_PRICE` for CIEN/META/BKNG came back **identical to the on-disk `_data/estimates.json` snapshot (asof 2026-09-16)**, so the snapshot is current and was used for the fuller field set. **No PENDING column this run.**
   - ⚠️ **Annual `1FY/2FY/3FY` lines used throughout, never the `CY` blocks.** This is load-bearing for CIEN — see the basis note under ①.

---

## Where the new data DIVERGES

### ① ★ CIEN: the "$8.3–8.4B FY27 floor" is arithmetically EMPTY, and consensus had already cleared it before it was published

The headline read on the Investor Forum is that management hardened FY27 from a growth rate into a dollar range. It did not add information.

| | |
|---|--:|
| FY26 guide, top of range (09-03) | **$6.40bn** |
| × 1.30 | **$8.32bn** |
| × 1.3125 | **$8.40bn** |
| Deck's stated FY27 "current floor" | **$8.3–8.4bn** |

🔴 **The range IS the 09-03 "at least +30%" restated in dollars off the FY26 guide top. It is not a raise, and it carries no new demand information** — which is what the catalyst post-mortem concluded from the transcript alone, now confirmed from the deck itself.

And the Street was already past it:

| FY27 (BBG 2FY, FYE Oct-2027) | Consensus | Company floor | Read |
|---|--:|--:|---|
| Revenue | **$8,429m** | $8,300–8,400m | 🔴 consensus **+0.35% above the TOP** of the floor |
| Gross margin | **45.52%** | 45–46% | ✓ dead centre |
| Implied EBIT margin | **25.50%** ($2,149.5m) | 25–27% | ⚠️ consensus sits at the **BOTTOM** of the company range |

➤ **Where the asymmetry actually is: MARGIN, not revenue.** Consensus has taken the revenue floor and then modelled the *bottom* of the company's own operating-margin range. If the 25–27% band is a floor in the same sense the revenue number is, there is ~1.5pt of operating margin — roughly **$125m of EBIT, ~6% of the FY27 consensus EBIT line** — that the Street is not carrying.

⚠️ **BASIS TRAP, RECORDED SO IT IS NOT RE-DERIVED: CIEN's fiscal year ends in October.** The `CY2027` block in `estimates.json` prints **$9,048m** against the 2FY annual line of **$8,429m** — 7.3% apart. Scoring the company's FY27 floor against the CY block would have manufactured a fake *"company guiding 8% below consensus"* story. **Use the annual line for CIEN, always.**

### ② ★★ META: Goldman publishes a BUY on top of a model 13% below consensus on 2027 EBIT and 18% below on EPS — while sitting 1.7% ABOVE on revenue

All three houses are within ~1.7% of each other on 2027 revenue. They are 20 percentage points apart on what that revenue earns.

| 2027E | BBG consensus (2FY) | **GS** (09-13, Buy $725) | **Citi** (09-16, Buy $800) | Capstone house (06-11) |
|---|--:|--:|--:|--:|
| Revenue | $305,419m | $310,507m (**+1.7%**) | $310,127m (**+1.5%**) | $313,000m (+2.5%) |
| EBIT / operating income | $103,525m | **$89,950m (−13.1%)** | **$111,061m (+7.3%)** | ~35% margin ⇒ ~$110,000m |
| EPS | $38.09 | **$31.39 (−17.6%)** | $36.92 GAAP (−3.1%) | $38.24 (+0.4%) |
| FCF | — | **−$26,071m** | — | **−$23,000m** |

🔴🔴 **GS and Citi are 0.12% apart on 2027 revenue and 23.5% apart on 2027 operating income.** The $75 price-target spread between them is therefore **an earnings disagreement, not a multiple disagreement** — the exact inverse of the 09-10 JPM upgrade, which was all multiple on identical EPS.

🔴 **Inside the GS model, 2027 is a down year that its own text never discusses:** EPS falls y/y (**$31.65 → $31.39**), FCF yield turns **negative (−1.6%)**, and EBIT grows **+3.5% on +21.6% revenue** — every incremental revenue dollar is consumed. The mechanism is depreciation: D&A **$37bn → $67bn** against capex $138bn → $214bn.

✅ **THE HOUSE MODEL SPLITS THE DIFFERENCE IN AN INFORMATIVE WAY.** Capstone's 2027 EPS of **$38.24** is within 0.4% of consensus and **22% above Goldman** — but Capstone's FCF of **−$23bn** is close to Goldman's **−$26bn**. ➤ **So the house already agrees with GS that the cash line goes deeply negative, and disagrees only about whether that shows up in EPS.** That localises the entire dispute to the **depreciation schedule** — useful life and in-service timing — rather than to demand, revenue or capex. **That is a model-bridge question the house can answer from its own file, and it is the most actionable item in this report.**

⚠️ **Basis caveats before anyone trades this:** (a) Citi's 2026 GAAP operating income embeds **$13,580m of one-time items**, so only 2027/2028 is like-for-like between the two houses; (b) Citi's headline EPS box is **pro-forma ex-SBC** ($39.45 / $48.80 / $59.77) compared against a GAAP consensus column — the comparable GAAP diluted line is **$28.11 / $36.92 / $46.17**, and the $800 target is struck on ~22x the $36.92; (c) `BEST_EBIT` is a normalised consensus line, so the GAAP-vs-adjusted seam is real even in the clean years.

### ③ CIEN 2029: the revenue target is already in the curve; the entire surprise is margin — but the comparison is a year offset and must be labelled as such

| | Company 2029 target | BBG 3FY (= FY28) | Read |
|---|--:|--:|---|
| Revenue | ~$14.0bn | $10,857m × 1.30 = **$14,114m** | ✓ **already in the curve** |
| Gross margin | ~50% | **46.01%** | 🔴 +4.0pt gap |
| Operating margin | 32–35% | **28.06%** ($3,046.6m) | 🔴 +3.9 to +6.9pt gap |

⚠️ **The consensus column is FY28 and the company column is 2029 — one year apart.** The gaps above are an **upper bound** on the disagreement, not a measurement of it; a year of consensus margin expansion closes part of it mechanically. Both sides are adjusted/non-GAAP. **Do not compare either to a GAAP line.**

### ④ CIEN: management's own "~5x cash generated from operations" does not close against the published FY25 base

The deck claims operating cash flow quintuples 2026 → 2029. Against the 2029 target set (~20% FCF margin on ~$14bn, plus capex), OCF lands around **$3.1–3.2bn** — implying a base of roughly **$0.6bn**. **FY25 actual OCF was $806m.** ➤ **Either the base year is not FY25, or the multiple is rounded generously.** No base year is disclosed on the slide (the axis reads 2026 → 2029). **Logged as UNVERIFIED, not adopted.** Worth one question at ECOC on 09-21/22.

---

## CONFIRMS — no action

### ⑤ BKNG: Morgan Stanley assumes coverage essentially AT consensus on the numbers, and slightly below on the target

| | MS (Cost, 09-16) | BBG consensus | Gap |
|---|--:|--:|--:|
| Revenue 2026 | $29,477m | $29,244m (1FY) | +0.8% |
| Revenue 2027 | $32,035m | $31,940m (2FY) | +0.3% |
| Revenue 2028 | $34,724m | $34,626m (3FY) | +0.3% |
| EBITDA 2026 | $10,954m | $10,833m | +1.1% |
| EBITDA 2027 | $12,301m | $12,238m | +0.5% |
| EBITDA 2028 | $13,524m | $13,525m | **−0.0%** |
| Price target | **$230** | $238.95 (consensus PT) | −3.7% |

➤ **A coverage assumption that changes the analyst and the derivation but not the numbers.** MS lands inside 1.1% of consensus on every revenue and EBITDA line out to 2028 — the 2028 EBITDA differs by $1m on $13.5bn. The Overweight therefore rests entirely on the **framework** call (*"horizontal AI looks more like a new acquisition channel than a disintermediation threat"*) and on a multiple — 18x versus the ~20x long-term ex-COVID average — not on an estimate edge.

⚠️ MS's EPS ladder is **GAAP**; `BEST_EPS` is adjusted. The comparable pair is net income: MS 2027 GAAP NI $8,886m vs consensus 2FY NI $9,051m (−1.8%). ⚠️ **BBG reports BKNG gross margin as 100.0%** — that is the net-revenue presentation, not a margin.

### ⑥ CIEN FY27 gross margin, and the FY26 scoreboard

Company FY27 GM floor **45–46%** vs consensus **45.52%** — dead centre, no edge either way. The 2024→2026 scoreboard management put on the record (revenue +$2.4bn at a 27% CAGR to the $6.4bn FY26 guide; adjusted operating margin +~1100bps; adjusted EPS up $5+ at a 98% CAGR) reconciles against the consensus 1FY line of **$6,421.9m** — the Street is $22m above the guide top and there is no dispute about FY26.

### ⑦ CRWD / PANW — nothing to reconcile, by design

The JPM Fal.Con note's rating history ends **`20-Aug-26 OW 201.63 235`**, identical to the OW / $235 (Dec-27) already on the page — **no PT change, no new estimate**. Its net-new content (the $260bn CY29 → $565bn CY34 TAM ladder, the $215bn AI-security split, the 3.5%-penetration benchmark) is **company framing, not a broker estimate**, and is logged as such. The 2023 initiation is filed archivally on both pages and **supersedes nothing**.

🔴 **One trap recorded: the two JPM documents sit on different price bases** — the 2026 note's rating history is split-adjusted, the 2023 initiation prints as-traded. Chaining them naively shows CRWD *falling* 61% in eight months. Split-proof comparison: CRWD market cap $25.5bn → $209.8bn (~8.2x); PANW $47.9bn → $282.1bn (~5.9x). The exercise also surfaced a **PANW 2:1 split (Dec-2024)** the page had never recorded.

---

## DATA DEFECTS FOUND WHILE RECONCILING

- 🔧 **`_data/house.json` drops the MINUS SIGN on negative FCF.** META's parsed block reads `"fcf": {2025: 22.0, 2026: 17.0, 2027: 23.0}` while its own `raw_rows` read `"22", "-17", "-23"`. **The house model has META FCF going NEGATIVE in 2026 and 2027; the parsed field says positive.** Anything reading `house.json["companies"]["META"]["years"]["2027"]["fcf"]` gets **+$23bn instead of −$23bn** — a $46bn sign error on the exact line finding ② turns on. ➤ **Fix the sign handling in the house-model loader and re-check every other name.** (This report used `raw_rows`, which is correct.)
- ⚠️ **`_meta/catalysts.md` carries the 2026-09-16 CIEN post-mortem row twice**, identical text on consecutive lines. The file is regenerated by `refresh_features.py`, so the duplication is upstream of the artifact.
- ⚠️ **A Citi META price-target cut from $850 to $800 is missing from the corpus.** The 09-16 note prints $800 with no "previous" marker, so the cut happened in a note never ingested, on an unknown date.
- ⚠️ **Ciena's $52bn 2029 TAM is a re-aggregation, not an independent vote** — its five cited sources (Cignal AI, Dell'Oro, LightCounting, Omdia, 650 Group) are all already on `themes/optical-cpo.md`. Only the Q4'26 CPO/NPO sample date, the Coherent-Lite ramp window, the accretive-margin claim and the segment boundaries are first-party.


---

## BBG re-placement layer — 2026-09-17 12:31 (`/wiki-consensus`)

_This report was written on the **09-16** vintage, i.e. the evening of Ciena's Investor Forum. `estimates.json` has since refreshed to **asof 2026-09-17** (107/107 live, 0 FAIL lines, 0 null prices, 0 carry-over stamps, **0 records byte-identical to the 09-16 vintage**). This is therefore the **first post-Investor-Forum consensus print**, and it lands on finding ②._

⚠️ **Basis honoured exactly as §38 demands: every figure below is the BBG *annual* line (`1FY`/`2FY`/`3FY`), never the `CY` block.** On the CY2027 block CIEN's consensus operating margin reads **26.73%** — near the TOP of the company's 25–27% band — which would have **falsified finding ② outright**. The annual line reads **25.58%**. The basis trap this report recorded is not hypothetical; it inverts the conclusion.

| CIEN annual consensus | 09-16 | 09-17 | Δ |
|---|--:|--:|--:|
| FY2026 (`1FY`) revenue | $6,421.9m | $6,421.9m | **0.00%** |
| FY2026 operating margin | 20.37% | 20.37% | **0bp** |
| FY2027 (`2FY`) revenue | $8,429.5m | **$8,447.7m** | +0.22% |
| FY2027 EBIT | $2,149.5m | **$2,161.3m** | +0.55% |
| FY2027 operating margin | 25.50% | **25.58%** | **+8bp** |
| FY2028 (`3FY`) revenue | $10,857.3m | $10,890.2m | +0.30% |
| FY2028 EBIT | $3,046.6m | **$3,109.6m** | **+2.07%** |
| FY2028 operating margin | 28.06% | **28.55%** | **+49bp** |

➤ **① and the revenue leg — UNCHANGED, and marginally reinforced.** FY26 did not move by a single dollar (the report's "no dispute about FY26" is now literally verified against a fresh pull). FY27 revenue rose $18.2m to **$8,447.7m**, i.e. **+0.57% above the top of the $8,300–8,400m "floor"** (was +0.35%). **The headline is still empty. Stays DIVERGES.**

➤➤ 🔴 **② STAYS DIVERGES — but the fresh data RE-FRAMES the mechanism, and this is the material thing to come out of the refresh.** The gap to the top of the company's own range is now **$119.6m of FY27 EBIT, 5.5% of the consensus EBIT line** (the report estimated ~$125m / ~6% — it holds, marginally narrowed). What is new is **where the Street put its post-Forum revision: it raised FY2028 operating margin +49bp and FY2027 only +8bp — six times more in the year beyond the guide than in the guided year.** And **FY2028 consensus OM now stands at 28.55%, ABOVE the top of the company's own 25–27% band.**

➤ **CONSEQUENCE: the Street is not refusing the margin range — it is deferring it by a year.** Consensus already underwrites >27% operating margin, just in FY2028 rather than FY2027. That converts ② from a *disbelief* call into a **timing** call, which is both weaker and far more testable: it resolves at the FY27 quarterly guides, not at a 2029 model. ⚠️ **Stated as an interpretation of a one-day revision, not an established view** — one print after an investor day is thin evidence, and the FY28 line carries no guide to test it against.

➤ **Isolation check, which is what gives the CIEN move its weight: across all 107 names, only FOUR carried ANY estimate field moving ≥0.5% overnight** (CIEN CY27 EPS +1.29% / EBIT +1.21%; NFLX CY27 capex −1.70%; CRWV CY27 EPS −0.96%; ESTC capex −0.6/−0.7%). **CIEN's revision is a genuine post-event re-mark, not tape noise** — this was otherwise a session in which prices moved and estimates did not (SMCI +9.7%, INTC +8.6%, HPE +8.2%, MDB +6.9%, ARM +6.5%, AMD +6.3%, MU +5.9%, SNDK +5.6% on the day, against a consensus tape that barely twitched).

➤ **Price/PT context:** CIEN spot **$340.50 → $355.02 (+4.26%)**, consensus PT **$495.05 → $502.10**, street high **$660** unchanged, street low **$324.34** unchanged and still below spot. Upside to the consensus target compresses to **+41%** (from +45%).

➤ **Findings ③–⑥ and the CONFIRMS block are UNAFFECTED** — none of their names (META, BKNG) carried an estimate revision ≥0.5% on this vintage; META's 2027 EBIT/EPS consensus and BKNG's lines are unchanged, so the Goldman-vs-Citi depreciation dispute and the house's +22% EPS gap stand exactly as written.

_BBG column resolved 2026-09-17 — estimates.json asof 2026-09-17. No cell in this report was ever marked PENDING (BBG was live at ingest); this layer re-places the report's quantitative rows against the first post-Forum vintage instead._


---

# SECOND PASS — 2026-09-17 (c), /run-inbox 23h (scheduled, unattended)

_Appended to this same report rather than opened as `reconciliation-2026-09-18.md`: a new file on the same day evicts this one from the edge tracker's newest-report-only harvest. **§⑦ above ("CRWD / PANW — nothing to reconcile, by design") described the 10h pass and is NOT superseded — it was true of the JPM notes. Tonight's sources are three COMPANY PRIMARIES and there is a great deal to reconcile.**_

**Baseline used.** `estimates.json` **asof 2026-09-17** (same-day vintage, 107 names) — **no BBG PENDING on this pass**. ⚠️ **Every figure below is the BBG ANNUAL line (`1FY`/`2FY`/`3FY`), never the `CY` block — see ③ under CONFIRMS for what the CY block would have done to PANW.**

⚠️ **TWO LEGS OF THE THREE-LEG RECONCILIATION ARE STRUCTURALLY UNAVAILABLE TONIGHT, AND THAT IS A FINDING, NOT AN OMISSION.**
- **No Capstone house model exists for [[CRWD]], [[PANW]] or SentinelOne.** `_data/house.json` (asof 2026-09-17) carries **nine** names: AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TER, TSM. **Leg (2) is absent, not skipped.**
- **BBG carries no ARR, no net-new ARR and no segment ARR.** So CrowdStrike's **$695M / $585M** segment disclosures and its **≥$1,626M FY28 net-new-ARR guide**, and Palo Alto's **NGS ARR** guide, **cannot be scored against consensus at all** — only against the companies' own prior disclosures and the desks' bogeys. **This is a standing blind spot for every ARR-reporting name in this wiki, and tonight it covers the three headline numbers of the run.**
- **SentinelOne is not in `estimates.json`** (107 names, S absent) and has no wiki page. Its Q2 FY27 primary has **no consensus baseline of any kind**.

## Where the new data DIVERGES — second pass

### ⑧ ★★ CRWD: the consensus price target has gone BELOW spot, and 41 of 56 analysts still say Buy

BBG asof **2026-09-17**: **px $245.70**, **consensus PT $238.84** (n=**56**; **41 buy / 14 hold / 1 sell**; street high $425, low $132). ➤ **The average target is 2.79% BELOW the market price.**

🔴 **This page recorded the opposite three sessions ago.** The 09-15 block carries *"consensus PT $238.58 (n=56) — consensus PT sits essentially at spot ($237.83), which is itself a positioning signal."* **Since then the stock has added 3.3% and the consensus target has added 0.11%.** The ratings distribution has not moved.

➤ **The ratings and the targets are now saying different things about the same stock, and the gap is measurable rather than rhetorical.** That is the positioning constraint the 09-15 call named in words (*"people are positioned long those two… and it's worked, unfortunately"*) expressed as a number. ⚠️ **Not a valuation call: the targets are stale relative to the tape, which is the ordinary state of affairs after a fast move. The signal is the ABSENCE of target revisions after Fal.Con, not the level.**

### ⑨ ★★ CRWD FY29: consensus underwrites only the FLOOR of the new operating-margin target — the cleanest quantified edge of the run

The investor-briefing deck put a **FY29 target model** on the record for the first time: **non-GAAP operating margin 28–32%**, FCF margin 34–38%, against 1H27 actuals of 24% and 30%.

| CRWD FY29 (BBG `3FY`) | Consensus | Company target | Implied EBIT | vs consensus |
|---|--:|--:|--:|--:|
| Revenue | **$8,979.5m** | — | — | — |
| Operating income | **$2,514.2m** | — | — | — |
| **Operating margin** | **28.00%** | **28–32%** | — | **at the FLOOR** |
| … at the 30% midpoint | — | 30% | **$2,693.9m** | **+7.1%** |
| … at the 32% top | — | 32% | **$2,873.5m** | **+14.3%** |

➤ **Consensus FY29 operating margin is 28.00% — the bottom of management's band, to two decimals. The Street has taken the revenue ramp and declined the margin ramp.** If management delivers the midpoint, FY29 EBIT is 7.1% above where the Street sits; the top of the band is +14.3%. **That is a real, dated, falsifiable edge and it does not require believing any TAM number.**

⚠️ **BASIS WARNING, because this is where the comparison breaks: do NOT score the company's 82–85% gross-margin target against BBG's `gm`.** The company's target is **SUBSCRIPTION** gross margin (1H27 actual 81%); BBG's `3FY` gm of **79.94%** is a company-level figure that includes professional services. **Different denominators. The margin comparison above is deliberately made at EBIT, which is like-for-like.**

### ⑩ ★ CRWD FY28 free cash flow: the Street's published mark is the company's own guide applied to the analyst's own revenue

Deutsche Bank's FY28 re-model (already on the CRWD page, 2026-09-03) reads **revenue $7,415m, FCF $2,410m**. **$2,410m ÷ $7,415m = 32.50%** — **exactly** the FY28 free-cash-flow-margin floor the company guided at the investor briefing (*"FY28 32.5%+"*).

➤ **DB's FCF number is not an independent estimate; it is the guided margin identity applied to DB's own revenue line.** Applying the same **32.5% floor to BBG's `2FY` consensus revenue of $7,368.4m** gives **≥$2,394.7m** of FY28 FCF — a derived consensus-equivalent the wiki did not have. **Until a house publishes an FY28 FCF margin that is NOT 32.5%, treat the Street's FY28 FCF as a restatement of guidance and not as a view.** ✅ Separately, **DB's $7,415m revenue is +0.63% vs the $7,368.4m consensus** — in line, no edge.

### ⑪ ★ The consolidation thesis has no independent survey support, and the one survey that exists is mildly against it

UBS Evidence Lab, **n=100 enterprise security leaders, fielded November 2025** (from the 2026-01-13 outlook; the consolidation section was dropped when that note was first ingested on 09-15 off a mangled PDF): **35% expect to consolidate vendors · 43% no change · 20% expect to EXPAND**. UBS's own conclusion: *"2026 will see **less active consolidation**."* Preferred + 2nd-choice consolidation winners: **[[CRWD]] 52% · [[MSFT]] 45% · ZS 21% · [[PANW]] 15%.**

➤ **Against MS · Cerisola's 09-15 framing** — budget-driven consolidation as *the* share-gain engine, PANW and CRWD as the winners, ZS on the short leg — **the only surveyed evidence in this corpus has the consolidating cohort at a MINORITY, ranks ZS ABOVE PANW, and puts PANW LAST of the four.**

⚠️ **Dated, and the caveat is material: November 2025, ten months before the call and before the CyberArk close (2026-02-11).** PANW's own F4Q26 deck reports **~220 net new platformizations (+44% y/y)** and **NRR >120% among platformized customers** — the behaviour is visible in the book even though the intent survey did not anticipate it. **Logged as a counterweight and as a gap in the evidence base, NOT as a refutation, and no number was written to the assumptions ledger.**

### ⑫ ★ CrowdStrike marks its own current AI cyber-spend attach at 1%; the sell-side uses 6–7%

The deck's 2027 AI-security band runs **$36bn at a 1% cyber-spend attach to $291bn at 8%**, both computed on Gartner's **$3.64T "AI spend surge"** case (×1% = $36.4bn, ×8% = $291.2bn — the **$2.67T baseline shown beside it is never used**, so the low end is a low-ATTACH case, not a low-spend case). Cerisola's construction starts from *"security runs at roughly 6–7% of IT budget; assume a similar attach to the AI budget"*, rising to *"8, 9, 10%."*

➤ **The two independent ladders AGREE at the ~8% ceiling and differ SIX-FOLD at the floor.** Since every AI-cyber TAM on `themes/ai-cybersecurity.md` — $120bn, $220bn, $215bn, $36–291bn — is an attach-rate assumption wearing a dollar sign, **the attach rate is the single highest-leverage number on that page and neither side has defined its numerator.** Logged as a corpus gap, not as a divergence to trade.

## CONFIRMS — second pass

### ⑬ PANW: the tightest guide-vs-consensus fit in this wiki — four marks, all inside the range

| PANW mark | Company guide (2026-09-01) | BBG consensus (annual line, asof 09-17) | Δ vs guide midpoint |
|---|---|--:|--:|
| FY'27 revenue (`1FY`) | $14,100–14,200m | **$14,164.1m** | **+0.10%** |
| FY'27 non-GAAP diluted EPS (`1FY`) | $4.16–4.19 | **$4.18** | **+0.12%** |
| Q1'27 revenue (`1FQ`) | $3,300–3,310m | **$3,308.0m** | **+0.09%** |
| Q1'27 non-GAAP diluted EPS (`1FQ`) | $0.96–0.98 | **$0.972** | **+0.21%** |

➤ **All four sit inside the guided range and none is more than 21bp from the midpoint. There is no estimate edge anywhere in PANW's guided P&L.** Any PANW edge has to come from **NGS ARR, net new NGS ARR, platformizations or the Idira ramp — none of which BBG carries.** ✅ Also confirmed: BBG's FY26 actual revenue of **$11,480.0m** matches the deck's reported figure exactly.

### ⑭ 🔴 BASIS TRAP CONFIRMED ON A FOURTH NAME — PANW's CY block is NOT its fiscal year, and the wedge is 8%

| PANW | CY block | Annual line | Wedge |
|---|--:|--:|--:|
| 2026 | CY2026 **$13,021.7m** | `1FY` **$14,164.1m** | **−8.1%** |
| 2027 | CY2027 **$15,094.3m** | `2FY` **$16,181.8m** | **−6.7%** |

🔴 **Scoring the company's own $14,100–14,200m FY27 guide against the CY2026 block would have printed "consensus sits 8% BELOW management's guidance" — a fabricated story, on a July-31 fiscal year end.** Same class as the DELL and CRM traps already recorded; this is the fourth name it has been confirmed on.

✅ **And the contrast that stops the rule being over-generalised: CRWD's January-31 FYE makes the wedge immaterial** — CY2026 $5,951.0m vs `1FY` $6,006.5m = **−0.92%**; CY2027 $7,362.2m vs `2FY` $7,368.4m = **−0.09%**. **The rule is FYE-specific, not universal: check the wedge before deciding whether it matters.**

### ⑮ CrowdStrike's deck arithmetic closes on six independent checks

| Claim | Check | Result |
|---|---|--:|
| ~3.5% of $565bn reaches $20bn ARR | 565 × 3.5% | **$19.78bn** ✅ |
| Agentic SOC $695m → $1.8bn at 13% CAGR to CY34 | 695 × 1.13⁸ | **$1,848m** ✅ |
| Agentic Identity $585m → $1.7bn at 14% CAGR | 585 × 1.14⁸ | **$1,669m** ✅ |
| AI-security slice of the CY34 TAM = $215bn | 115 + 52 + 48 | **$215bn** ✅ |
| CY29 TAM category split sums to the $260bn total | 6+11+13+26+27+30+32+33+40+42 | **$260bn** ✅ |
| 2027 AI-security band off the surge case | 3,640 × 1% / × 8% | **$36.4bn / $291.2bn** ✅ |

➤ **The deck's internal arithmetic is clean. Every argument therefore lives in the ASSUMPTIONS — the 3.5% capture rate, the 17% TAM CAGR and the attach rate — not in the sums.** ✅ One more: **FY28 net new ARR ≥$1,626m ÷ FY27 $1,355m = 1.2000 exactly**, confirming *"20%+"* is a floor at precisely +20.0% and not a rounded range.

### ⑯ The $10bn-within-FY30 pull-forward is arithmetically CONSERVATIVE against the rate just delivered

From the disclosed **2Q27 ending ARR of $5.8bn**, reaching **$10bn by the end of FY30** (31-Jan-2030, 3.5 years) requires a **~16.8% CAGR**. The company has just delivered **~21.9% over two years** ($3.9bn at 2Q25 → $5.8bn at 2Q27; the deck rounds it to 23%). **The pulled-forward target therefore requires deceleration of roughly five points, not acceleration.**

⚠️ **And the "15% CAGR" label is being applied to the WRONG leg by anyone who reads it off the headline: it runs from $10bn to $20bn** (10 × 1.15⁵ = **$20.11bn** ✅), i.e. FY30→FY35 — **not from today's $5.8bn base.** Two different rates on one slide.

### ⑰ PANW gross margin: the Street has already taken the mix-driven erosion the deck under-plays

BBG `1FY` gross margin **75.36%**, sitting between the FY26 actual non-GAAP **75.8%** and the Q4'26 exit rate of **74.8%** (FY25 was 76.4%). ➤ **No edge — but it retires the question. The acquisition-mix gross-margin decline is absent from the company's highlights slide and present in consensus.**

## DATA DEFECTS FOUND WHILE RECONCILING — second pass

- 🔴 **The CrowdStrike deck's TAM slide returns its ten category values in REVERSE order against their labels in the PDF text layer.** A naive extraction prints **Secure Browser $42bn and Cloud Security $6bn**; the truth is exactly inverted. **The check that catches it is additivity — the correct pairing sums to exactly $260bn.** Read from the rendered image. Same class as the Jefferies chart-deck mispairing already in this wiki's memory.
- 🔴 **Two further chart mispairings in the same batch.** The CRWD Flex slide's text layer emits a 4×2 table column-major (`>2,900 / >40% / $2.29B / >630`), and UBS's consolidation-winners prose lists the vendors *"Microsoft, CrowdStrike, Palo Alto Networks, and Zscaler"* — **which is not the rank order of its own chart**. **Three mispairing traps in one night across two houses and one company: for any number that lives inside a chart, read the pixels.**
- ⚠️ **`themes/ai-cybersecurity.md` §2c is headed "SEVEN BACKFILL NOTES" and the Bernstein arc is now EIGHT** (a 2025-07-16 note arrived tonight). An addendum was inserted beside the list rather than rewriting the header; **the header should be re-cut on the next pass that touches §2c.**
- ⚠️ **`PENDING_FULL_REPORTS.md` was absent from `_inbox` at the start of this run.** It was swallowed by `--archive` at 10h and, unlike `_expert_calls_seen.json`, appears not to have been restored. **The 10h record says both were restored and md5-verified, so either the restore did not land or something removed it afterwards.**
- ✅ **`_expert_calls_seen.json` survived tonight's `--archive` intact** — md5 `bd9cf582…` identical before and after, verified rather than assumed.
