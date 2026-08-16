# Reconciliation — 2026-08-15 (/run-inbox, scheduled)

_Variance pass on every NEW quantitative datapoint from tonight's 10 sources, against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

**Sources reconciled:** SanDisk Investor Day deck (company primary, 98pp) · Citi SNDK 08-14 · Bernstein SNDK 08-14 · Susquehanna SNDK 08-13 · JPM SNDK 08-14 · Barclays SNDK 08-14 · Jefferies SNDK 08-13 · MU/Sadana KeyBanc fireside 08-10 (Bloomberg FINAL TRANSCRIPT) · UBS Arcuri AMAT callback 08-14 · SNDK Q4 FY26 transcript 08-05.

## Baseline status

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Done (on disk). |
| **2. Capstone house models** | ✅ Done — but coverage is thin for tonight's names. `_data/house.json` holds **AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM**. Of tonight's six names **only NVDA has a house model**. SNDK / MU / AMAT / LRCX / KLAC have **no house model** — reconciled vs wiki + BBG only. |
| **3. BBG consensus — LIVE** | 🔴 **PENDING.** `bdp` raised `ConnectionError: blpapi: could not start session (Terminal not running / logged out?)` — repeated `Failed to connect to 127.0.0.1:8194` at 23:34-23:35. **Terminal not logged in / Capstone VPN down.** No web data substituted. |
| **3b. BBG consensus — ON-DISK SNAPSHOT** | ✅ Used as the stand-in: `_wiki/_data/estimates.json`, **asof 2026-08-14** (from the 08-14 `/wiki-consensus` run, 98/98 clean). One day stale, which for tonight's purpose is acceptable — **but note it PRE-DATES none of tonight's notes; the 08-14 broker set may not yet be in it.** ⚠️ Per the standing caveat, **CY2026 sums embed pre-print consensus for already-reported quarters — CY2027 is the clean column and is what is used below.** |

**Action required:** log in to the Bloomberg Terminal / reconnect the VPN and re-run `/wiki-consensus` to resolve the LIVE column, especially the **SNDK CY27 EPS** and **MU CY27 GM** rows below.

---

## DIVERGES (the alpha)

### 1. 🔴🔴 MU — consensus models an 86% CY27 gross margin, but management has just disclosed that most contracted volume is CEILINGED at CQ2-2026 pricing

| Mark | Value | Source |
|---|--:|---|
| BBG consensus CY2027 gross margin | **86.0%** | estimates.json, asof 08-14 |
| BBG consensus CY2027 EPS / revenue | **$163.61 / $262.5bn** | estimates.json |
| MU **floor** GM under the SCAs | *"considerably higher than prior peak… prior peak was in the low 60s. So it's probably going to be **70, 75 at least**"* | UBS · Arcuri, 08-14 (analyst estimate) |
| MU **ceiling** on the 16 announced SCAs | **"our CQ2 pricing"** | **Sadana (EVP & CBO), 08-10 — management, verbatim** |

**The divergence.** Consensus carries an **86% CY27 gross margin**. Management has now disclosed that the SCAs are a **price BAND**, and that on the **16 SCAs announced at the time of earnings the ceiling is CQ2-2026 pricing**. If those 16 represent the bulk of contracted volume, then an 86% CY27 GM requires one of three things to be true, and they are not equally likely:
1. **CQ2-2026 pricing already implies ~86% GM** — possible, since MU printed 85-86% GM around that period, in which case the ceiling is not binding at the consensus level and the estimate is safe;
2. the **uncapped/floating volume** carries the blended margin higher — but Sadana says *"most of the volume… is going to have a price band"*, which limits how much work the floating tranche can do;
3. consensus is **carrying CQ2-level margins into CY27 without recognising that they are now a CAP rather than a spot outcome** — which would make 86% a ceiling being modelled as a base case.

**Why it is alpha regardless of which holds:** the market's working model of memory LTAs — "floor protected, upside retained" — is **wrong for Micron's first 16 SCAs**. The disclosure converts a distribution with a right tail into one that is **truncated on the right** for most volume. Even if 86% is achievable, the *variance* around it has collapsed on the upside while the downside (the floor, ~70-75% on Arcuri's estimate) remains open. **Consensus EPS may be roughly right while the option value embedded in the multiple is not.**

**➜ Falsifiable test:** MU's realised GM in any quarter where spot DRAM prices rise materially above CQ2-2026 levels. If GM does not expand with spot, the ceiling is binding and the "LTAs preserve upside" narrative fails for MU specifically. **This is checkable at the next print.**

**➜ Action:** re-run the BBG pull when the Terminal is back and check whether CY27 GM has moved since 08-14; and put the question to management. Arcuri had MU on the road in Singapore on **Monday 08-17** — his 70-75% floor estimate was explicitly pre-verification, so that meeting is the near-term resolution point.

---

### 2. 🔴 MU vs SNDK — the two largest LTA books are priced the OPPOSITE way round, and the wiki had been treating them as one trade

| | **MU (SCAs)** | **SNDK (NBMs)** |
|---|---|---|
| Structure | **Price BAND — floor AND ceiling** | **FLOOR only** |
| Ceiling | **CQ2-2026 pricing** on the 16 announced SCAs | **None** — uncommitted capacity *"floats with prevailing market prices"* |
| Floor GM | **~70-75%** (Arcuri est., not company-guided) | **~80%** (company-stated, corroborated by SIG/BofA/JPM) |
| Coverage | 16 SCAs; $22bn cash-like, $18bn cash | 8 NBMs; **50% FY27 supply → ~67% FY28** (company deck) |
| Upside participation | **Capped on most volume** | **Retained on the uncontracted third** |

**Nothing on either page contradicts this — it simply had never been put side by side.** The implication is directional and tradeable: **on a further NAND/DRAM melt-up SanDisk participates and Micron largely does not**, on already-signed volume. It also introduces **contract vintage** as an earnings-power variable for MU that no model on this wiki currently carries: SCAs struck at the CQ2-2026 ceiling are capped lower than SCAs signed later at higher prevailing prices.

**➜ Action:** the two names should **not** be expressed as a single "memory LTA de-risking" position. Check `_data/book.json` for any paired exposure.

---

### 3. 🔴 SNDK — Bernstein's Street-high $3,000 is built on a model that REJECTS the growth guide it endorses

| Mark | FY27 | FY28 | FY29 | FY30 |
|---|--:|--:|--:|--:|
| **Bernstein revenue ($bn)** | 50.0 | 56.8 | **50.1 (−11.9%)** | 53.0 |
| Company guide (FY28-30 revenue growth) | — | **mid-to-high teens %** | **mid-to-high teens %** | **mid-to-high teens %** |
| BBG consensus CY2027 revenue | **$54.5bn** | — | — | — |

**Bernstein reiterates Outperform / TP $3,000 (Street high) under a headline that says the Investor Day made it *"more bullish"* — while modelling a −11.9% revenue decline in FY29 and an FY30 still below FY28.** The $3,000 is therefore underwritten by **buyback accretion** (−47% share count: 148.09m → ~78.1m by FY30 on $104.9bn of cumulative FCF at a constant $1,500 repurchase price), **not** by management's growth framework.

**Why this is alpha rather than pedantry:** it means the Street-high target does **not** require the acyclicality thesis to be true — arguably making it the most robust bull case on the page — but anyone citing *"Bernstein is at $3,000"* as sell-side endorsement of the FY28-30 model **is misreading the note**. The two are different bets that happen to share a number.

**⚠️ Basis caveat:** SNDK's fiscal year ends June, so FY28 (Jul-27→Jun-28) straddles CY27H2/CY28H1. Bernstein's FY28 $56.8bn and SIG's FY28 $56.6bn are **not** directly comparable to BBG's CY2027 $54.5bn — do not net them.

---

### 4. 🔴 SNDK — consensus CY27 gross margin (84.3%) sits ABOVE the company's own FY28-30 target (~80%)

| Mark | Value |
|---|--:|
| BBG consensus CY2027 GM | **84.3%** |
| Company FY28-30 target GM | **~80% average** |
| Company FY28-30 target OM / FCF margin | 75% / ~50% |

**Consensus is not modelling the guide — it is modelling above it.** This is *consistent* with the page's central reading (the ~80% is the **NBM floor restated as a target**, not a forecast — MS: management *"threaded the needle"* by guiding to a margin level *"corresponding to what we already knew was the NBM margin floor"*). But it makes the asymmetry explicit and worth stating plainly:

- If ~80% is the **floor**, consensus at 84.3% is reasonable and the guide is conservative → the stock re-rates on proof.
- If ~80% is the **forecast**, consensus is **~430bp too high** on CY27 GM and the estimate cuts come later.

**➜ This is the single cleanest binary on the SNDK page, and it is testable quarterly.** The page already frames it correctly; what is new is that consensus has now been measured against it.

---

### 5. ⚠️ AMAT — Arcuri's capacity-derived 2028 systems number is far above anything in the consensus trajectory

| Mark | Value | Basis |
|---|--:|---|
| AMAT systems, most recent quarter | **~$7bn** | Arcuri, 08-14 |
| Arcuri systems **exiting 2028** | **~$14bn / quarter** | his model, from the capacity-doubling disclosure |
| BBG consensus **CY2027** total revenue | **$48.1bn** (~$12bn/qtr, all-in) | estimates.json |
| BBG consensus CY2027 EPS | **$19.74** | estimates.json |

**⚠️ BASIS GUARD — these are not like-for-like and must not be netted:** Arcuri's figure is **quarterly SYSTEMS (SSG)** revenue exiting **CY2028**; the consensus figure is **annual TOTAL company** revenue (SSG + AGS + Display) for **CY2027**. Different segment, different period, different frequency.

Even so the direction is stark: **~$14bn/quarter of systems alone implies a total-company run-rate roughly 40-50% above the CY2027 consensus annualised**, one year later. And the underlying disclosure is unusually hard — a **doubling of manufacturing capacity through 2028 with further expansions beyond**, i.e. capital already committed, which management declined to call revenue guidance and Arcuri says *"obviously it is."*

**➜ Action:** this cannot be resolved without **CY2028 consensus**, which is **not in the on-disk snapshot** (estimates.json carries only 1FQ / 2FQ / CY2026 / CY2027 for AMAT). **Add CY2028 to the next BBG pull** — until then this row is directionally flagged, not sized.

**⚠️ Counterweight on the same call, and it argues the opposite way on margin:** *"about **80% of Applied's costs are actually component costs**… the fixed cost component here is actually not that high."* If ~80% of COGS is variable, **the revenue doubling drops through at ~60%, not at classic capital-equipment leverage** — so a systems doubling is worth materially less to EPS than the revenue line suggests. **Consensus CY27 GM of 50.8% is consistent with a low-fixed-cost structure, so consensus appears to be modelling this correctly; the risk is in models that assume fat operating leverage.**

---

### 6. ⚠️ SNDK — the post-Investor-Day house cluster sits ABOVE the on-disk consensus, which has not yet caught up

| House | CY27 EPS | vs BBG CY2027 cons **$238.25** |
|---|--:|--:|
| Citi (derived from its own fiscal quarters) | ~$244 | **+2.4%** |
| JPM | $250 | **+4.9%** |
| BofA | $255 | **+7.0%** |
| FUNDA (independent, not a broker) | $292 | **+22.6%** |
| _SIG — different basis:_ FY28 EPS | _$249.43_ | _not comparable (FY Jun-28, and the PT is 11x this)_ |

**Read this as a mechanical lag, not as alpha in itself:** the on-disk snapshot is **asof 08-14** and most of these notes published **on** 08-14, so consensus has likely not absorbed them. **The genuine content is that every post-day house is ABOVE consensus and none is below** — there is no two-sided dispersion on CY27 EPS among the houses that attended.

**➜ Action:** re-pull BBG when the Terminal is up; if CY2027 consensus has NOT moved toward ~$245-250 within a week, the gap is real rather than a lag.

---

### 7. ⚠️ SNDK — Citi is 33% ABOVE consensus in the out-year while 6% BELOW it in the near year

| Period (Citi fiscal, June YE) | Citi | First Call cons (per Citi) | Gap |
|---|--:|--:|--:|
| FY2027E | $205.36 | $218.73 | **−6.1%** |
| FY2028E | $268.28 | $254.15 | **+5.6%** |
| FY2029E | **$265.18** | **$199.12** | **+33.2%** |

**The shape matters more than the level.** The Street's disagreement with the SanDisk story is **concentrated entirely in the out-years** — consensus has FY29 EPS falling ~22% from FY28 while Citi has it roughly flat. **This is the same finding Jefferies reached from the revenue side** (*"implies big upward revisions to current consensus forecasts (+16% / −4% / −30% y/y for FY28E/29E/30E)"* — i.e. consensus models FY30 revenue **30% below** the company framework, already logged on the page).

**➜ Two independent houses, two different line items, same conclusion: the out-year consensus is modelling a cycle-down that management says will not happen. That is where the SNDK debate actually is — not in the next twelve months.**

---

## CONFIRMS (no action)

### 8. ✅🔴 NVDA — the Capstone house model and UBS Arcuri land in the same place, ~19% above consensus

| Mark | CY2027 EPS | CY2027 revenue |
|---|--:|--:|
| **BBG consensus** (asof 08-14) | **$12.93** | **$569.1bn** |
| **Capstone house model** (`house.json`) | **$15.44** | **$661bn** |
| **UBS · Arcuri** (08-14) | *"more than **$15** next year"* | — |
| Gap: house vs consensus | **+19.4%** | **+16.1%** |

**This is the most useful confirmation of the run.** The house has carried an out-of-consensus NVDA CY27 EPS of **$15.44** against a Street at **$12.93**. Arcuri independently expects the buy-side to converge on *"more than $15 next year and then a path to 20 bucks in 28"* — **effectively the house number** — and states *"there is **no other major bank anywhere close to me** in terms of numbers… but **the buy side's kind of roughly where I already am**."*

**The consensus gap corroborates his claim of being alone on the sell-side, and it puts a named major-bank analyst alongside the Capstone model.** ➜ **No change to the house model is warranted; its principal external risk — being the only holder of the number — is now measurably lower.**

**Note the shape of the resulting call:** if the buy-side already shares the number (as Arcuri asserts and the house independently reached), then NVDA is **not an estimate call** — it is a **calendar-roll / multiple call**. At **$220 the stock is ~11x his CY28 EPS of ~$20**. *"I just don't think the stock stays at 220 when you're talking about being inside of early 27."*

---

### 9. ✅ NVDA — the guide ladder is internally consistent and sits just above consensus

| Step | Value | vs BBG consensus |
|---|--:|--:|
| BBG cons, quarter about to report (1FQ) | **$91.8bn** (hi $94.2bn) | — |
| Arcuri expected **print** | $94-95bn | **+2.4% to +3.5%** |
| BBG cons, quarter being **guided** (2FQ) | **$103.8bn** | — |
| Arcuri expected **guide** | **$107-108bn** | **+3.1% to +4.0%** |
| Arcuri expected eventual **report** of that quarter | $110-111bn | +6.0% to +6.9% |
| **What the supply chain implies** | **$117-119bn** | **+12.7% to +14.6%** |
| Buy-side whisper Arcuri rejects | ~$120bn | +15.6% |

✅ **Consensus and Arcuri agree closely on the print and the guide.** The whole setup risk is in the last two rows: **the supply chain is running ~13-15% above the consensus guide because the CFO holds an $8-10bn buffer.** ➜ **The named hazard is a framing failure, not a demand failure — the buy-side pricing the supply-chain number ($117-119bn) and reading a managed $107-108bn guide as a miss.** Logged as a pre-print watch item, not a divergence.

### 10. ✅ MU — management confirms the SCA collateral figure the page had only from a broker

**$22bn of cash and cash-like commitments on the 16 SCAs, of which $18bn is cash on the balance sheet** (Sadana, 08-10) matches exactly what the page carried from **Bernstein** ($18bn cash deposits + $4bn letters of credit, 2026-07-09). **Broker-sourced figure now confirmed by management. No change.**

### 11. ✅ SNDK — the company primary confirms the NBM coverage path the page already carried, and settles a broker discrepancy

**Deck: *"50% FY27 Supply under NBMs… growing to approximately 67% in FY28"*** — confirms BofA / SIG / JPM / Bernstein and the page's standing figures. **Citi's "50% in FY26, ~66% in FY27" is a one-year shift and is not adopted.** No estimate impact.

### 12. ✅ SNDK — two of the page's own flags were wrong and are withdrawn (no estimate impact)

- **"SIG vs BofA arithmetic tension" on bit-per-wafer productivity** — the deck carries **both** *"27% CAGR Yearly Average Productivity"* and *"54% average gen-to-gen bit/wafer growth"* **on the same slide**. Both houses quoted the company correctly. The do-not-net instruction stands.
- **"BofA's growth rates look transposed"** — the deck shows Consumer/Edge **30%+ CAGR** is the **historical** era and AI/DC **high-teens** the **forward** era. BofA reported it correctly.

### 13. ✅ SNDK — Citrini's 2030 decomposition is CONFIRMED as a faithful reading of the deck, but is NOT an independent source

Citrini's **480EB staging / 420EB KV cache / 300EB fast data lakes** is exactly the deck's **40% / 35% / 25% × 1.2ZB**. ⚠️ **Do not treat Citrini and the deck as two corroborating sources.** Provenance now visible: the **1.2ZB TAM is TechInsights** (third party); the **workload splits are Sandisk-internal**. The existing unit guard (annual demand ≠ the ~1ZB installed base) is unaffected.

---

## Not reconcilable / basis mismatches — logged so nobody nets them later

| Datapoint | Why it cannot be compared |
|---|---|
| **LRCX: NAND WFE ~$20bn/yr run rate** (Arcuri, from Lam's Sept guide) | **Industry WFE spend**, not LRCX revenue. BBG CY2027 LRCX revenue is **$37.7bn** (total company, all device types). Never net an industry-TAM figure against a company revenue line. |
| **MU HBM/DDR trade ratio 3:1 → ~4:1** | A **substitution ratio**, not a supply forecast. Do not chain it into any bit-growth or wafer-start series on the memory pages. |
| **MU "$250 billion" investment** | A long-horizon aggregate stated on stage, unreconciled to any capex line. BBG CY2026 MU capex consensus is **$34.9bn**. **Not adopted.** |
| **SNDK wafer capacity ~1,830 kwpm peak / ~560 kwpm retired** | Physical capacity, no consensus equivalent. Note the substantive point: the *"~30% below prior peak"* figure is **retirement, not idling** — retired capacity does not return on a price signal. |
| **KLAC "very, very big numbers" on TSMC 2027 capex** | Unquantified and second-hand. Directional only. |
| **SNDK/Kioxia JV = 33% of world NAND wafers** (TechInsights) | Industry share, no consensus line. Reads onto KIOXIA. |
| **Bernstein: HBF needs 3-4x wafer capacity per exabyte** | An estimate about a **pre-revenue** product that every house explicitly excludes from numbers. Not modellable; logged as a supply-side mechanism. |

---

## Open items for the next run

1. 🔴 **Re-run the BBG pull** (`/wiki-consensus`) once the Terminal is logged in / VPN is up — the LIVE column is PENDING for all six names. **Priority rows: MU CY27 GM (86.0%) and SNDK CY27 EPS ($238.25).**
2. **Add CY2028 to the BBG fetch.** The AMAT capacity-doubling claim (item 5) and the SNDK FY29/FY30 dispute (items 3 and 7) both live in a year the on-disk snapshot does not carry. **This is currently the binding constraint on reconciling the most interesting claims on the wiki.**
3. **No house model exists for SNDK, MU, AMAT, LRCX or KLAC.** Five of tonight's six names could only be reconciled against two of the three baselines. Given that memory and semicap are where the wiki's most active debates sit, this is a real gap.
4. **Watch for the MU Singapore NDR (Monday 2026-08-17)** — Arcuri's 70-75% floor-margin estimate was explicitly pre-verification, and the ceiling question (item 1) is exactly what should be put to management.
