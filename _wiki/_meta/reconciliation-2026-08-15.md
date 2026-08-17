# Reconciliation — 2026-08-15 (/run-inbox, scheduled)

_Variance pass on every NEW quantitative datapoint from tonight's 10 sources, against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

**Sources reconciled:** SanDisk Investor Day deck (company primary, 98pp) · Citi SNDK 08-14 · Bernstein SNDK 08-14 · Susquehanna SNDK 08-13 · JPM SNDK 08-14 · Barclays SNDK 08-14 · Jefferies SNDK 08-13 · MU/Sadana KeyBanc fireside 08-10 (Bloomberg FINAL TRANSCRIPT) · UBS Arcuri AMAT callback 08-14 · SNDK Q4 FY26 transcript 08-05.

## Baseline status

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Done (on disk). |
| **2. Capstone house models** | ✅ Done — but coverage is thin for tonight's names. `_data/house.json` holds **AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM**. Of tonight's six names **only NVDA has a house model**. SNDK / MU / AMAT / LRCX / KLAC have **no house model** — reconciled vs wiki + BBG only. |
| **3. BBG consensus — LIVE** | ✅ **RESOLVED 2026-08-17 via `/wiki-consensus`** (was 🔴 PENDING on `ConnectionError: blpapi: could not start session` at 23:34-23:35 on 08-15). Live pull `estimates.json` **asof 2026-08-17**, **98/98 names, 0 FAIL lines, 0 null prices, and 0 entries byte-identical to the 08-14 vintage** (i.e. no silent carry-overs), plus three ad-hoc live pulls the same date: consensus target price / rating, the reported-quarter adjusted GM ladder for MU+SNDK, and an H1-CY2028 probe. **No web data was substituted at any point.** |
| **3b. BBG consensus — ON-DISK SNAPSHOT** | ✅ Used as the stand-in: `_wiki/_data/estimates.json`, **asof 2026-08-14** (from the 08-14 `/wiki-consensus` run, 98/98 clean). One day stale, which for tonight's purpose is acceptable — **but note it PRE-DATES none of tonight's notes; the 08-14 broker set may not yet be in it.** ⚠️ Per the standing caveat, **CY2026 sums embed pre-print consensus for already-reported quarters — CY2027 is the clean column and is what is used below.** |

~~**Action required:** log in to the Bloomberg Terminal / reconnect the VPN and re-run `/wiki-consensus` to resolve the LIVE column, especially the **SNDK CY27 EPS** and **MU CY27 GM** rows below.~~ ✅ **Done 2026-08-17.** Both priority rows resolved below — and **both resolved AGAINST consensus, not for it.**

---

## BBG consensus pull — live 2026-08-17 (the PT column this run never had)

_Ad-hoc `bdp` against `E:\bloomberg_api`, 2026-08-17. Spot and PT pulled in the same call, so the upside is internally consistent. Rating = `BEST_ANALYST_RATING` on the 1-5 scale (5 = all buys); **n** = `TOT_ANALYST_REC`._

| Ticker | Spot | Cons PT | Upside | Rating (n) | Read |
|---|--:|--:|--:|--:|---|
| **MU** | 1034.04 | 1586.42 | **+53.4%** | 4.83/5 (59) | 🔴 **Largest upside in the run, on the deepest sample of the six — and it sits directly on top of item ①.** The Street pays a **53% premium to spot while carrying an 86.0% CY27 gross margin that is 415bp ABOVE the margin MU actually realised in the ceiling quarter** (see ①). The PT is not evidence the estimate is safe; it is the same estimate expressed as a target. **Divergence stands and is the highest-conviction row in the report.** |
| **NVDA** | 227.68 | 303.71 | **+33.4%** | 4.88/5 (81) | ✅ **Highest-rated name in the run on the deepest sample anywhere (81 recs).** Consistent with ⑧/⑨: no estimate dispute near-term, the call is the calendar roll. **CONFIRMS.** |
| **AMAT** | 537.59 | 654.20 | **+21.7%** | 4.74/5 (43) | ⚠️ Reads with ⑤ — the Street is constructive on the name but its **CY27→H1-28 revenue trajectory cannot accommodate Arcuri's systems number** (see ⑤). Upside is priced off the consensus trajectory, not off the capacity-doubling one. |
| **SNDK** | 1812.00 | 2196.10 | **+21.2%** | 4.71/5 (31) | 🔴 Reads with ③: **Bernstein's Street-high $3,000 is +36.6% above the consensus PT of $2,196**, and +65.6% above spot vs the Street's +21.2%. The gap between the Street-high and the Street is **larger than the Street's entire upside case**. |
| **KLAC** | 206.04 | 234.54 | **+13.8%** | 4.29/5 (31) | **Weakest conviction of the six** (4.29/5, the only sub-4.5 rating). KLAC contributes no quantitative row to this run — its TSMC-capex remark stays in the unquantifiable table. |
| **LRCX** | 342.28 | 376.81 | **+10.1%** | 4.65/5 (37) | **Lowest upside of the six.** LRCX's only datapoint this run is the industry NAND-WFE figure, which is a **TAM line and not an LRCX revenue line** — see the basis-mismatch table. No estimate content. |

---

## Where the new data DIVERGES

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

✅ **08-17 resolution (was PENDING) — hypothesis ① is FALSIFIED, and this is the most consequential thing to come out of the run.**

**The ceiling quarter is not a forecast — MU has already reported it.** MU's last reported quarter ended **2026-05-28**, which snaps to **CQ2-2026**: the exact quarter Sadana named as the ceiling. So "our CQ2 pricing" is an **observable, printed number**, and the three-way branch above collapses to one testable comparison. Pulled on the same adjusted/consensus basis the CY sums use (`BEST_FPERIOD_OVERRIDE` 0FQ = last reported), live 08-17:

| Quarter | Override | Consensus-basis GM | Revenue ($m) |
|---|:--:|--:|--:|
| CQ3-2025 | −3FQ | 44.29% | 11,154 |
| CQ4-2025 | −2FQ | 52.10% | 12,954 |
| CQ1-2026 | −1FQ | 69.13% | 19,857 |
| **CQ2-2026 — THE CEILING QUARTER (reported)** | **0FQ** | **81.86%** | **35,688** |
| CQ3-2026E | 1FQ | 86.00% | 50,992 |
| CQ4-2026E | 2FQ | 86.40% | 57,162 |
| CQ1-2027E | 3FQ | 86.46% | 60,518 |
| CQ2-2027E | 4FQ | 86.21% | 64,324 |
| **CY2027E (blended)** | — | **86.0%** | **262,475** |

**Branch ① said an 86% CY27 GM would be safe if "CQ2-2026 pricing already implies ~86% GM." It does not — CQ2-2026 printed 81.86%.** Consensus therefore carries **CY2027 gross margin ~415bp ABOVE the margin realised in the very quarter that caps the price on most contracted volume**, and it starts doing so **immediately**: the next unreported quarter is already modelled at 86.00%, +414bp above the ceiling quarter.

**What this does and does not prove — stated precisely, because the distinction is the whole finding:**
- ✅ It **kills the benign reading.** Nobody can now argue the ceiling is non-binding because it already sits at consensus margin. It sits 415bp below it.
- ⚠️ It does **not** prove consensus is wrong. **A price ceiling caps price, not gross margin.** With price capped on the SCA volume, ~all of the 415bp expansion must come from **cost-per-bit reduction and mix** (HBM/node migration), not from price. That is a materially harder requirement than "prices keep rising," and it is the requirement consensus is implicitly underwriting.
- ➜ **The call sharpens from "86% may be a ceiling modelled as a base case" to: consensus needs ~415bp of pure cost-and-mix expansion off an already-record 81.9% base, on volume whose price is contractually capped.**

**Consensus has not moved since the disclosure.** CY2027 GM **86.0%**, EPS **$163.61**, revenue **$262,475m** are **unchanged to the decimal** from the 08-14 vintage — despite Sadana's 08-10 disclosure and the 08-14 broker set. (This is a true no-move, not a stale record: MU's entry did change on the pull — spot $971.66 → $1,034.83 — so the file refreshed and the estimates simply did not.) **Seven days on from the disclosure, the Street has not touched the number.**

⚠️ **Counterweight found in the same pull, and it is the honest qualifier: consensus DOES model a fade — just not in 2027.** The H1-CY2028 probe puts MU GM at **83.6%**, i.e. **−240bp off the CY27 level**, versus SNDK at −90bp (84.3% → 83.4%). **Consensus already carries a steeper margin roll-over for MU than for SanDisk**, which is directionally what the ceiling asymmetry in ② predicts. So the Street is not blind to the mechanism — **it has pushed it one year to the right of where the disclosure puts it.** The divergence is about **timing**, not existence.

**➜ Stays DIVERGES — strengthened, and now the run's highest-conviction row.** ➜ **Open modelling item (do NOT free-hand it):** size the cost-per-bit decline implied by 81.9% → 86.0% at capped price, and test it against MU's historical cost-down. That is a `/quant-estimate` job, not a reconciliation line.

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

✅ **08-17 resolution (was PENDING) — consensus prices the asymmetry, but only from 2028:**

| | **MU** | **SNDK** |
|---|--:|--:|
| Ceiling quarter GM, reported (0FQ) | **81.86%** | **81.47%** |
| Consensus CY2027 GM | **86.0%** | **84.3%** |
| Consensus H1-CY2028 GM | **83.6%** | **83.4%** |
| CY27 → H1-28 change | **−240bp** | **−90bp** |
| Consensus PT upside (live 08-17) | **+53.4%** | **+21.2%** |

**The structural read survives contact with the numbers, with one correction to make.** The two names came off almost identical ceiling-quarter margins (81.9% vs 81.5%), and consensus then fans them apart in CY27 (**MU 86.0% vs SNDK 84.3% — MU 170bp HIGHER**) before collapsing them back together in H1-28 (83.6% vs 83.4%, a 20bp gap). **So consensus models MU as the one with more margin upside in 2027 and more margin downside in 2028 — the precise opposite of the contract structure**, which caps MU's upside and leaves SanDisk's open.

**➜ This is the cleanest expression of ② available: on consensus numbers you are paid MORE for MU's CY27 margin (and +53.4% of PT upside) on the book that is capped, and LESS for SanDisk's on the book that is not.** Stays DIVERGES, and the pairing warning is reinforced rather than softened.

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

✅ **08-17 resolution (was PENDING) — the $3,000 is further outside the Street than the Street's own bull case:**

| Mark | Value | vs |
|---|--:|---|
| Spot (live 08-17) | **$1,812.00** | — |
| **BBG consensus PT** | **$2,196.10** | **+21.2%** vs spot |
| **Bernstein TP (Street high)** | **$3,000** | **+65.6%** vs spot · **+36.6% above the consensus PT** |
| BBG consensus rating | 4.71/5 (31 recs) | — |

**The gap between Bernstein and the Street ($804) is larger than the Street's entire upside case ($384).** That is the quantification the row was missing: this is not a Street-high that sits a notch above the pack, it is a target **two-thirds again as far from consensus as consensus is from spot**.

**And it sharpens the original point rather than blunting it.** Since the $3,000 is underwritten by **buyback accretion on a −47% share count**, not by the FY28-30 growth guide, the single most bullish target on the name is **the one least dependent on the acyclicality thesis** — while the consensus PT, at less than a third of the distance, is the one carrying the growth framework. **Anyone citing "the Street high is $3,000" as evidence the Street believes the guide has the argument exactly backwards.** Stays DIVERGES.

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

✅ **08-17 resolution (was PENDING) — consensus holds above the target across BOTH forecast years, and the ceiling quarter sets the floor for the whole argument:**

| Mark | Value | vs company ~80% target |
|---|--:|--:|
| SNDK ceiling quarter GM, reported (0FQ, CQ2-26) | **81.47%** | **+147bp** |
| BBG consensus CY2027 GM | **84.3%** (unchanged from 08-14) | **+430bp** |
| BBG consensus **H1-CY2028** GM | **83.4%** | **+340bp** |

**Two things are now established that the report could only assert.** First, **consensus does not revert to the guide even in 2028** — it fades only 90bp and stays ~340bp above the ~80% target, so this is not a one-year overshoot the Street plans to grow into. Second, and more useful, **SanDisk has already REPORTED 81.5% — above its own FY28-30 target.** The company is guiding to a margin level it is currently exceeding, which is direct evidence for the page's reading that **the ~80% is the NBM floor restated as a target, not a forecast** (MS: management *"threaded the needle"*).

**➜ The binary resolves toward the benign branch:** if ~80% were a genuine forecast, the company would be guiding to a **decline from a margin it just printed** — an implausible thing to put on an investor-day slide. **Consensus at 84.3% is defensible and the guide is conservative.** ⚠️ But note this cuts the other way for the bull case: **if ~80% is a floor the company is already above, then the "beat the guide" catalyst is largely spent** — the re-rating comes from proving durability, not from the next print. Stays DIVERGES (consensus still sits materially above the stated guide), with the balance of evidence now favouring consensus over the guide.

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

✅ **08-17 resolution (was PENDING) — the row is now SIZED. CY2028 is not fully on the wrapper, but H1-CY2028 is, and it is enough.**

The 8FQ consensus horizon reaches **Q1-28 and Q2-28** for AMAT (it does not reach a full CY2028 — see the corrected open item 2 below). Aggregating those two quarters the same way `fetch_estimates.py` calendarises, live 08-17:

| Mark | Value | Basis |
|---|--:|---|
| Consensus **CY2027** revenue | **$48,555m** (**$12,139m/qtr**) | 4 forecast quarters |
| Consensus **H1-CY2028** revenue | **$27,725m** (**$13,862m/qtr**) | 2 forecast quarters (Q1-28 + Q2-28) |
| Consensus H1-28 GM / EPS | 51.3% / $11.95 (2 qtrs) | — |
| **Arcuri systems, exiting CY2028** | **~$14,000m/qtr** | **SSG only** |
| Arcuri systems, most recent quarter | ~$7,000m/qtr | SSG only |

**The comparison that needs no assumption at all — and it is decisive.** Arcuri's **systems-only** exit-2028 figure (**~$14.0bn/qtr**) is **larger than the entire consensus TOTAL-COMPANY quarterly revenue in H1-2028 (~$13.9bn/qtr)**. Since SSG is by construction a *subset* of total revenue, consensus cannot accommodate Arcuri's number **by at least the whole of AGS + Display**, whatever those are worth. **No segment-share estimate is required to establish the gap — only the fact that a part cannot exceed the whole.**

**Sizing it, flagged as an extrapolation rather than a pull:** consensus grows AMAT **+14.2%** from the CY27 quarterly average to the H1-28 average; carrying that same consensus-implied trajectory to Q4-28 gives roughly **~$15.5bn/qtr total company**. Against that, Arcuri's ~$14bn of **systems alone** would require **SSG ≈ 90% of total revenue**, versus **~70% today** (his own ~$7bn systems on a ~$10bn quarter). **AMAT's segment mix does not move 20 points in two years.** ⚠️ *Tagged ESTIMATE: the Q4-28 figure is my extrapolation of consensus' own growth rate, not a BBG line — and H1-28 quarters are 6FQ/7FQ consensus, a thinner contributor set than the near quarters.*

**➜ Upgraded from ⚠️ flagged-not-sized to 🔴 DIVERGES.** Either Arcuri's capacity-derived systems number is far too high, or consensus is **~40%+ too low on 2028 revenue** — and the underlying disclosure (**a doubling of manufacturing capacity through 2028**, capital already committed, which management declined to call guidance and Arcuri says *"obviously it is"*) is unusually hard evidence for a claim this far from the Street. **This is the largest unresolved out-year gap in the run.** ⚠️ The margin counterweight above still binds: at ~80% variable cost, even a correct revenue call converts to much less EPS than the revenue gap implies — **so the trade expression is revenue/backlog, not margin leverage.**

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

✅ **08-17 resolution (was PENDING) — 3 of the 7 days elapsed, and consensus has not moved AT ALL:**

| Mark | 08-14 | 08-17 (live) | Move |
|---|--:|--:|--:|
| BBG consensus CY2027 EPS | $238.25 | **$238.25** | **0.00** |
| BBG consensus CY2027 revenue ($m) | 54,475.03 | **54,475.03** | **0.00** |
| BBG consensus CY2027 **street-high** EPS | $290.80 | **$290.80** | **0.00** |
| _(control — the record did refresh)_ CY2026 revenue ($m) | 35,971.30 | **36,011.35** | **+40.05** |

**The control line matters: SNDK's near-year revenue DID tick up (+$40m on CY26, +0.4% on the next quarter), so the file genuinely refreshed for this name — the out-year simply did not move.** This is a true no-move, not a carry-over.

**Two new readings, and the second is the more interesting:**
1. **The lag hypothesis is weakening but not yet dead** — the report set a one-week test and only three days have run. **Recheck 2026-08-22.** What can be said now: the Street revised the near year within three days of the investor day and left the out-year untouched, which is not the behaviour of a Street that is simply slow to process.
2. 🔴 **FUNDA's $292 is not an outlier beyond the Street — it IS the Street high.** Consensus CY27 street-high EPS is **$290.80**, versus FUNDA at **$292**. The report treated FUNDA as an independent extreme sitting +22.6% above consensus; in fact **someone on the sell-side already carries essentially the same number.** ⚠️ **Basis guard:** per `estimates.json`'s own note, a CY street-high is the **sum of quarterly highs** — an envelope that need not belong to any single house — so this bounds the range, it does not name a house at $290.80.

**➜ Stays DIVERGES.** The house cluster ($244-255) still sits above consensus ($238.25) with **no house below it**, and the dispersion is one-sided exactly as logged. Re-test 08-22.

---

### 7. ⚠️ SNDK — Citi is 33% ABOVE consensus in the out-year while 6% BELOW it in the near year

| Period (Citi fiscal, June YE) | Citi | First Call cons (per Citi) | Gap |
|---|--:|--:|--:|
| FY2027E | $205.36 | $218.73 | **−6.1%** |
| FY2028E | $268.28 | $254.15 | **+5.6%** |
| FY2029E | **$265.18** | **$199.12** | **+33.2%** |

**The shape matters more than the level.** The Street's disagreement with the SanDisk story is **concentrated entirely in the out-years** — consensus has FY29 EPS falling ~22% from FY28 while Citi has it roughly flat. **This is the same finding Jefferies reached from the revenue side** (*"implies big upward revisions to current consensus forecasts (+16% / −4% / −30% y/y for FY28E/29E/30E)"* — i.e. consensus models FY30 revenue **30% below** the company framework, already logged on the page).

**➜ Two independent houses, two different line items, same conclusion: the out-year consensus is modelling a cycle-down that management says will not happen. That is where the SNDK debate actually is — not in the next twelve months.**

⚠️ **08-17 resolution (was PENDING) — PARTIALLY resolvable only, and the unresolvable part is the part that matters. Stated plainly rather than papered over.**

**The disputed period is beyond the wrapper's horizon.** Citi's contested year is **FY2029 (Jul-28 → Jun-29)**. The BBG quarterly consensus horizon runs 8 fiscal quarters from SNDK's LRQ (2026-07-03), reaching **Q2-CY2028** — it stops right where the dispute begins. **No BBG line exists for the year in which Citi is +33% above First Call, and none can be manufactured from this pull. This row cannot be closed by `/wiki-consensus` and should stop being carried as if it could.**

What the horizon *does* reach, offered as the nearest available read:

| Mark | Value | Period |
|---|--:|---|
| BBG consensus **H1-CY2028** EPS | **$130.00** (2 qtrs) → **~$260 annualised** | Jan-28 → Jun-28 = back half of Citi's FY2028 |
| Citi **FY2028E** | $268.28 | Jul-27 → Jun-28 |
| First Call FY2028 cons (per Citi) | $254.15 | Jul-27 → Jun-28 |

**So through the back half of Citi's FY28, calendar consensus is running at roughly $260 annualised — between First Call's FY28 and Citi's own, and NOT decelerating.** ⚠️ **Do not read this as evidence against the FY29 collapse:** annualising two quarters imposes no cycle shape, and the drop Citi and Jefferies both flag is timed for the year *after* this window. **The only honest conclusion is that consensus has not yet begun to roll over at the point the data runs out.**

**➜ Stays DIVERGES, re-tagged as NOT BBG-RESOLVABLE.** ➜ To close it properly the fetch needs **annual** consensus (`nBF` fiscal-year overrides), not deeper quarterly — see the corrected open item 2.

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

✅ **08-17 resolution (was PENDING) — CONFIRMS holds on an unchanged consensus, with one qualifier to Arcuri's "no other bank is close" claim:**

| Mark | 08-14 | 08-17 (live) | Move |
|---|--:|--:|--:|
| BBG consensus CY2027 EPS | $12.93 | **$12.93** | **0.00** |
| BBG consensus CY2027 revenue ($bn) | 569.1 | **569.1** | **0.00** |
| Capstone house CY2027 EPS / revenue | $15.44 / $661bn | unchanged | — |
| **House vs consensus** | +19.4% / +16.1% | **+19.4% / +16.1%** | — |
| Consensus PT vs spot (live) | — | **$303.71 vs $227.68 = +33.4%**, 4.88/5 (81 recs) | — |

**Consensus did not move to the decimal on either line, so the confirmation is intact and the edge tracker's programmatic NVDA rows (+19% EPS, +16% revenue) survive the refresh unchanged.**

⚠️ **New qualifier the fresh pull surfaces — it slightly softens one claim without touching the finding.** Consensus **CY2027 street-high EPS is $15.94**, i.e. **above** the house's $15.44. So the house number is **inside the Street's range, near the top — not beyond it.** Arcuri's *"no other major bank anywhere close to me"* is a statement about the **median-to-high gap**, and it survives; but "the house holds a number nobody on the Street holds" would be **wrong** and should not be said. ⚠️ **Basis guard:** a CY street-high here is the **sum of quarterly highs**, an envelope that need not belong to any single house — so this bounds the range without naming a bank at $15.94.

**➜ CONFIRMS, unchanged. No change to the house model is warranted.** The finding's substance — that a named major-bank analyst independently reached the house number — is untouched; what changes is that the house's *external* risk was already lower than "sole holder," since the Street's own high envelope clears it.

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

✅ **08-17 resolution (was PENDING) — the ladder is unchanged to the decimal two days before the print:**

| Step | 08-14 | 08-17 (live) |
|---|--:|--:|
| BBG cons, quarter about to report (1FQ) | $91,799m (hi $94,236m) | **$91,799m (hi $94,236m)** |
| BBG cons, quarter being guided (2FQ) | $103,829m | **$103,829m (hi $112,149m)** |

**Both rungs are identical to the prior vintage, so every percentage in the ladder above still holds as printed** (Arcuri's $94-95bn print = +2.4% to +3.5% over consensus; his $107-108bn guide = +3.1% to +4.0%).

🔴 **One number the fresh pull adds, and it is the most useful thing here: the 2FQ street-high is $112,149m.** The report's key hazard was the buy-side anchoring on the supply-chain-implied **$117-119bn** and reading a managed **$107-108bn** guide as a miss. **The Street's own published high is $112.1bn — well above Arcuri's expected guide, and still ~5-6% BELOW the supply-chain number.** So the whisper is outside the entire published sell-side range, high end included. ➜ **The framing hazard is confirmed and now bounded: even the most aggressive published analyst is not at the number the buy-side is said to be pricing.** Stays CONFIRMS (no estimate dispute), sharpened as a pre-print watch item.

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

1. ~~🔴 **Re-run the BBG pull** (`/wiki-consensus`) once the Terminal is logged in / VPN is up — the LIVE column is PENDING for all six names. **Priority rows: MU CY27 GM (86.0%) and SNDK CY27 EPS ($238.25).**~~ ✅ **DONE 2026-08-17.** Both priority rows resolved, and **both against consensus**: MU's ceiling quarter printed **81.86%** vs consensus CY27 **86.0%** (branch ① falsified), and SNDK CY27 EPS **did not move at all** ($238.25 → $238.25) while the near year did. **No row crossed DIVERGES ↔ CONFIRMS.**
2. 🔴 **CORRECTED — "add CY2028 to the BBG fetch" is not achievable the way it was written, and the reason should be recorded.** The 08-17 probe replicated `fetch_estimates.py`'s calendarisation out to the full **8FQ** horizon: it reaches **only Q1-28 + Q2-28** for AMAT / SNDK / MU / LRCX / KLAC (**nq=2**) and **Q1-28 alone** for NVDA (**nq=1**). **A full CY2028 cannot be aggregated from quarterly consensus for any name in this run** — the horizon ends mid-year. Consequences:
   - **H1-CY2028 was enough to size AMAT (item 5)** — now upgraded to 🔴 DIVERGES on a part-cannot-exceed-the-whole argument that needs no segment assumption.
   - **It is NOT enough for SNDK FY29/FY30 (items 3 and 7)**, which sit entirely beyond the horizon. **Item 7 is re-tagged NOT BBG-RESOLVABLE.**
   - ➜ **The correct fix is annual, not deeper quarterly:** pull fiscal-year consensus via `BEST_FPERIOD_OVERRIDE` **`1BF`/`2BF`/`3BF`** and carry it as a separate FY block, clearly basis-separated from the calendarised CY sums (SNDK's June year-end means FY ≠ CY and the two must never be netted). ⚠️ Note the standing wrapper quirk on `BF` overrides for capex fields before wiring this in.
3. ⚠️ **NEW — size the MU cost-down implied by the ceiling (item 1).** Consensus needs **~415bp** of GM expansion (81.86% → 86.0%) on volume whose **price is contractually capped**, so it must come from cost-per-bit and mix alone. **Do not free-hand this** — it is a `/quant-estimate` job: calibrate against MU's historical cost-per-bit decline and test whether the required rate is inside precedent. **This is the highest-value open modelling item on the wiki.**
4. **No house model exists for SNDK, MU, AMAT, LRCX or KLAC.** Five of tonight's six names could only be reconciled against two of the three baselines. Given that memory and semicap are where the wiki's most active debates sit, this is a real gap. ⚠️ **The 08-17 refresh raises the cost of this gap:** items ①, ④ and ⑤ are now all sized against consensus alone, with no house number to anchor them.
5. 🔴 **The MU Singapore NDR is TODAY (Monday 2026-08-17)** — Arcuri's 70-75% floor-margin estimate was explicitly pre-verification, and the ceiling question (item 1) is exactly what should be put to management. **The 08-17 pull gives that meeting a much sharper question than the report could pose on 08-15:** not *"what is the floor?"* but ***"consensus carries CY27 gross margin 415bp above the 81.9% you printed in the CQ2-2026 quarter that caps most of your SCA volume — where does that expansion come from if not price?"***
6. ⚠️ **Re-test SNDK CY27 EPS on 2026-08-22** — the report's own one-week test on item ⑥. Three days in, consensus has not moved at all ($238.25) while the near year did revise, which already leans against the lag explanation.

---

_BBG column resolved 2026-08-17 — `estimates.json` asof **2026-08-17** (98/98 live, 0 FAIL, 0 null prices, 0 records byte-identical to the 08-14 vintage, so no silent carry-overs), plus three ad-hoc live pulls the same date: consensus PT/rating for the six names, the reported-quarter adjusted-basis GM ladder for MU + SNDK (`0FQ`/`-1FQ`… overrides), and an H1-CY2028 probe across the full 8FQ horizon. **All nine PENDING quantitative rows placed — ①-⑦ in DIVERGES and ⑧-⑨ in CONFIRMS. No row crossed DIVERGES ↔ CONFIRMS** — items ①②③④⑥ stay DIVERGES (①②③④ strengthened), ⑤ upgraded ⚠️→🔴 and sized, ⑦ re-tagged NOT BBG-RESOLVABLE, ⑧⑨ stay CONFIRMS on consensus that did not move to the decimal. Canonical header `## Where the new data DIVERGES` applied (was `## DIVERGES (the alpha)`). **No web data substituted at any point.**_
