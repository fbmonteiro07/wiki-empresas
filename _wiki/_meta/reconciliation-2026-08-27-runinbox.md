# Reconciliation — /run-inbox 2026-08-27 (23h scheduled run)

_Every NEW quantitative datapoint from tonight's 13 ingested sources, placed against **three baselines**: (1) prior wiki comments already on the page, (2) the Capstone house model, (3) BBG consensus._

**BBG status: ✅ LIVE.** Pulled 2026-08-27 via the Capstone wrapper (`E:\bloomberg_api`, `bdp`, `BEST_FPERIOD_OVERRIDE` passed as a **kwarg**, not in an `overrides=` dict — the dict form raises `BAD_ARGS / Invalid override field`). Fields: `BEST_EPS`, `BEST_SALES`, `BEST_EBIT`, `BEST_CAPEX` at `1FY/2FY/3FY`. **Periods are each company's own FISCAL years**, which avoids the CY-sum wedge documented in `_meta/assumptions.md`.

✅ **RESOLVED 2026-08-28 via `/wiki-consensus` — BOTH ROWS ARE CORRECT AND ARE NOW ADMITTED AS BASELINES. The two figures reproduce EXACTLY on a fresh live pull, and the reason they looked wrong is a QUARTER-vs-FISCAL-YEAR BASIS ERROR in the original flag, not a currency or scaling fault.** Live `bdp` re-pull 2026-08-28 (`BEST_FPERIOD_OVERRIDE` = `1FY`/`2FY`/`3FY`, kwarg form): **`MU` 1FY sales $129,311.2m, EBIT margin 76.2%, EPS $72.78**; **`SNDK` 1FY sales $48,825.5m, EBIT margin 79.5%, EPS $211.74, and 3FY EPS $211.10 BELOW 2FY $259.46** — i.e. every flagged number is transcribed correctly. ⚠️ **The `MU` flag's *"on a ~$45bn base"* is the defect: it places a full FISCAL YEAR against roughly ONE QUARTER of revenue.** MU printed **$41.5bn in F3Q26 alone** and guided F4Q26 to **~$50bn**; its last full fiscal year (FY25) was **$37.4bn**. 🔴 **The decisive corroboration is external and independent: BMO's own FY26E model — built bottom-up from three ALREADY-REPORTED quarters ($13,643 + $23,860 + $41,456 = $78,959m) plus the guided quarter ($50,140m) — totals $129,099m and $73.00 EPS, versus BBG's $129,311.2m and $72.78. That is +0.16% on revenue and −0.30% on EPS.** Three quarters of MU's "1FY" is therefore reported FACT, not forecast. The 2FY line ($151.683) also reproduces the $151.678 logged on 08-21/08-22 to three decimals — stable across seven sessions. **`SNDK` is corroborated the same way and lands CONSERVATIVE:** its 1FY (FY-Jun-2027) $48,825.5m sits **BELOW** both Susquehanna's FY27e $51.4bn and Bernstein's FY27 $50.0bn, and the 79.5% EBIT margin follows directly from a **PRINTED 84.6% non-GAAP gross margin in Q4 FY26** and an 83-85% guide. ➤ **Per the standing rule on this wiki, neither row is rejected on plausibility — and on inspection neither deserved to be. Both are restored as usable baselines.** See the new item **10** below, which is what the `SNDK` 3FY line actually means.

---

## Where the new data DIVERGES

### 1. [[LITE]] — management's FY28 earnings power is ~20% above consensus and ~a full year ahead of the consensus trajectory
**New datapoint:** Lumentum management, Deutsche Bank Technology Conference (2026-08-27), *"substantially take up where we think our earnings power will be in… our fiscal 2028"* — the ingested digest renders the destination as **$40 of FY28 earnings power**, attributed to OCS volume × OCS margin.

| Baseline | FY28 (fiscal, ending ~Jul-2028) | vs the $40 claim |
|---|--:|---|
| **BBG consensus** (2FY) | **$33.30** | **+20.1%** |
| BBG consensus (3FY = FY29) | $46.29 | the $40 sits **between** FY28 and FY29 consensus |
| **Capstone house model** (CY2027E, `Modelo consolidado incl. LITE`, 2026-06-16) | **$30.02** | **+33%** ⚠️ *period mismatch — house is calendar-2027, management's FY28 ends ~Jul-2028, so ~2 quarters later; the like-for-like gap is smaller than 33%* |
| Prior wiki comment | page carried OCS on a revenue/mix basis only — **no EPS figure had ever been attached to the OCS ramp** | net-new framing |

➤ **Read it as a ONE-YEAR PULL-FORWARD rather than a raise: $40 in FY28 is roughly where the Street already has FY29 (minus ~14%). Management is saying the trajectory arrives a year early, and it named the cause (OCS margin mix).** ⚠️⚠️ **DO NOT MODEL THE $40.** The source is an internally-circulated AI-generated digest, **not** a company or Bloomberg transcript; the "$40" is the digest's phrasing of the destination and does not appear inside the verbatim quote block; and no basis (GAAP/non-GAAP), share count or timing is given. **This is the single highest-priority verification item from tonight's run.** At the current $956.14 (BBG PX_LAST 08-27), $40 is **23.9x FY28** vs **28.7x** on consensus.

### 2. [[LITE]] — the OCS ramp clears the wiki's own pre-registered test, but sits INSIDE the analyst ceiling, not above it
**New datapoint:** OCS shipments *"doubling sequentially"*, revenue expected to **cross $100m next quarter**.

| Baseline | Mark | Verdict |
|---|---|---|
| **Prior wiki comment (08-19)** | pre-registered test: **"F1Q27 OCS ≥ $100m"**, against a **back-solved ~$52m June quarter** and an audited FY26 total of **>$90.0m** | ✅ **PASSES** — ~$52m → ~$100m+ is exactly the doubling |
| **Prior wiki comment (08-14, JPM · Cardoso)** | September OCS is *"low triple digits, or… **below $150m** a quarter"* | ⚠️ **the guide lands INSIDE the band, not above it** |
| **Prior wiki comment (08-13, mgmt via BTG)** | **$400m across 2H CY26**, ~**$250m/qtr run-rate CY27+** | 🔴 **STILL THE HARDER TEST AND IT IS UNCHANGED: ~$100m in September leaves ≥$250-300m for the December quarter alone — a ~5x step off the filed ~$52m June base in two quarters.** |

➤ **A pre-registered wiki test resolving in the bulls' favour is worth recording as a process win. But the September number being merely "in the band" means the $400m 2H-CY26 ladder is now MORE back-loaded, not less.**

### 3. [[META]] — the house model is the LOW mark on 2027 capex, ~14% below consensus and ~15-25% below the buy-side floor
**New datapoint:** BofA · Justin Post (2026-08-27): Reuters reports up to **7GW added next year**; *"if you assume $40bn a gigawatt, that could put you in the **mid-2s**"*, against **~$145bn this year**; the buy-side survey floor is *"**$200bn, which is kind of the MINIMUM**."*

| Baseline | 2027 capex | vs the $200bn floor |
|---|--:|---|
| **Capstone house model** (`Modelo Meta pós 2Q26`, 2026-06-11) | **$170bn** | **−15%** 🔴 |
| **BBG consensus** (2FY `BEST_CAPEX`) | **$197bn** | −1.5% (essentially AT the floor) |
| BofA buy-side survey floor | $200bn | — |
| Reuters-derived ceiling (7GW × $40bn) | **mid-$200bns** | **+25% or more** |
| BBG consensus 2026 (1FY) | $139bn | *vs BofA's "$145 this year" — a ~4% gap, basis unreconciled* |

🔴 **THE HOUSE IS EXPOSED HERE AND THE MECHANISM IS FCF, NOT CAPEX.** The house model already carries **2027E FCF of −$23bn on $170bn of capex**. Holding everything else constant, consensus capex of $197bn takes house FCF to roughly **−$50bn**, and the Reuters-derived case to roughly **−$100bn**. **That is precisely the financing problem BofA named** — *"we'd think they would probably need to RAISE SOME CAPITAL to fund it, or… keep doing pretty large deals with BlackRock and others"*, with the "no near-term equity raise" message given an explicit **three-month half-life**. ➤ **Action: the house capex line is the single most out-of-consensus number in tonight's batch and it is on the wrong side. Re-run the Meta capex/FCF bridge before the next print.**

⚠️⚠️ **UNIT TRAP, AND IT IS LIVE THIS WEEK:** the *"$40bn a gigawatt"* above is a **TOTAL BUILD COST** assumption used to gross up capex. [[NVDA]] separately put Vera Rubin at **~$40bn of NVDA REVENUE per GW**, and its CFO commentary implies **~$35-47bn of NVDA revenue per GW** at PORTS-Pike. **The two $40bn figures measure different things and their coincidence is an accident.** Jensen's own total-build figure is ~$60bn/GW. Never net or chain them.

### 4. [[NVDA]] — consensus FY28 revenue is ~5% BELOW management's own supply-set floor, and the house is between the two
**New datapoint (company primary, CFO Commentary 08-26):** FY28 guided **+~70%**, explicitly *"a supply constrained outlook"* against demand supporting ~100%.

| Baseline | FY28 revenue | vs the +70% guide (~$689bn off consensus FY27 of $405bn) |
|---|--:|---|
| **BBG consensus** (2FY `BEST_SALES`) | **$652.8bn** (+61.2% on 1FY) | **−5.2%** 🔴 |
| **Capstone house model** (2027E, FY≈CY) | **$661bn** (+62%) | **−4.0%** |
| Prior wiki comments — the covering analysts | JPM ~$695bn · MS $690.2bn · SIG ~$700bn · Redburn ~20% FY28 EPS upgrade | **all ABOVE consensus** |

➤ **The aggregate has not caught up to the guide, and the lead analysts are all above the aggregate. If management's +70% is a FLOOR (its own framing), consensus carries ~$36bn of catch-up. The house sits with consensus, not with the covering analysts.**

### 5. [[NVDA]] — the house gross margin is 100-200bp ABOVE management's own FY28 guide
**New datapoint:** FQ3 **74.0% ±50bp** → **FQ4 trough 71-72%** → **FY28 settle 72-73%**.

| Baseline | GM | vs the 72-73% FY28 guide |
|---|--:|---|
| **Capstone house model** 2027E | **~74%** | **+100-200bp** 🔴 |
| Page snapshot (BBG-derived) CY2027E | 74.0% | +100-200bp |
| Prior wiki comment — the sell-side going in | JPM 73.5% · MS 74.6% · Barclays 74.7% · GS/BBG 74.8% (for FQ3) | the reset is **~250-300bp vs where the Street actually sat** |

➤ **Action: the house GM line needs to come down to management's guide. On the house's own ~$661bn 2027E revenue, 150bp of gross margin is roughly $10bn of gross profit.** ⚠️⚠️ **AND THE QUALITY OF THE GUIDE IS NOW IN QUESTION IN THE OTHER DIRECTION: MS's Joe Moore says the rack **LPDDR5 content was halved and moved to CONSIGNMENT**, so it *"doesn't have to pass through NVIDIA, which helps gross margin PERCENTAGE."* Part of the guided GM% is memory cost routed AROUND the P&L. **Gross-profit DOLLARS are the honest series this quarter; anyone bridging FQ3 GM must know whether LPDDR5 is in or out of the base.**

### 6. [[NVDA]] — consensus has EBIT margin RISING into FY28 while gross margin is guided DOWN
| | 1FY (FY27) | 2FY (FY28) |
|---|--:|--:|
| BBG `BEST_EBIT` / `BEST_SALES` | $266.7bn / $405.1bn = **65.9%** | $435.2bn / $652.8bn = **66.7%** |

➤ **Consensus implies ~80bp of EBIT-margin EXPANSION in FY28 against a gross margin guided 200-300bp LOWER. That requires very large opex leverage to be true.** ⚠️ **Not necessarily wrong — revenue is growing ~60% and opex is not — but it is an unexamined assumption sitting inside the consensus EPS line, and it is the arithmetic that has to hold for the $14.92 FY28 consensus EPS to survive the margin reset. Flagged as the cleanest place to look for consensus EPS downgrades.**

### 7. [[VEEV]] — the "bearish" UBS growth number is actually ABOVE consensus
**New datapoint:** UBS · Keirstead (08-27) models *"more like **14% total revenue growth next year**"*, framed on the call as below the buy-side's *"comfy 15 to 20% zip code."*

| Baseline | FY28 revenue growth | vs UBS's 14% |
|---|--:|---|
| **BBG consensus** (1FY $3,686m → 2FY $4,136m) | **+12.2%** | **UBS is +1.8pts ABOVE consensus** |
| Prior wiki comment | page framed 14% as the bear case against a 15-20% buy-side assumption | ⚠️ **the framing is wrong relative to the sell-side aggregate** |

➤ **Useful correction: the wiki has been treating ~14% as a bearish mark. Against published consensus it is a mildly BULLISH one — it is only bearish against buy-side expectations. Both statements are true and the page should say which baseline it means.** ✅ Separately, consensus FY27 revenue of **$3,686m sits ~1.3% ABOVE the raised guide midpoint of $3.635-3.645bn** — consistent with a beat-and-raise already partly in numbers.

### 8. [[COHR]] vs [[LITE]] — a 2x disagreement on the 2030 OCS market, published the same day
| Source (both 2026-08-27) | 2030 OCS market |
|---|---|
| **[[COHR]]** (via Jefferies) | *"OCS outlook **DOUBLED to $4bn by 2030** (some third parties say $8bn)"* — i.e. $8bn is the **outside** case |
| **[[LITE]]** (DB conference) | the **$8bn** TAM given at OFC last year is *"**significantly UNDERCALLED**"*, new number due **at OFC next March** — i.e. $8bn is the **floor** |

➤ **No consensus or house number exists for the OCS market, so this cannot be scored against a third baseline. The SPREAD is the datapoint: the only two credible merchant suppliers are 2x apart on the same market on the same day, and it resolves at OFC in March 2027 — now a dated wiki catalyst.** ⚠️ **Separately flag an ambiguity in the Jefferies wording: COHR's *"~$3bn datacom run-rate exiting F27"* is almost certainly TOTAL datacom (vs consensus FY27 sales of $10.77bn), not OCS. Do not read it as a $3bn OCS run-rate.**

### 9. [[MCHP]] — consensus has ~280bp of FY28 margin expansion against management's guide of underabsorption through JunQ
| | 1FY | 2FY |
|---|--:|--:|
| BBG `BEST_EBIT` / `BEST_SALES` | $2,418m / $6,395m = **37.8%** | $3,010m / $7,421m = **40.6%** |

**New datapoint:** *"Underutilization should decline by $8m in SepQ but **PERSIST THROUGH JunQ NEXT YEAR**"*, against **customer-specific price increases effective August through October** and *"**no channel restocking is visible**."*
➤ **Consensus is underwriting ~280bp of expansion in a year management has pre-announced as still carrying under-absorption. The price increases are the only offset named, and they are unquantified. ⚠ Mild divergence — flagged rather than actioned, since the two are not strictly incompatible (price can beat absorption drag).**

---

### 10. [[SNDK]] — consensus models an FY29 REVENUE DECLINE against management's own mid-to-high-teens growth framework, and this is the largest house-vs-Street gap on the wiki, now sized
**Source of the finding:** the `3FY EPS BELOW 2FY` line originally flagged as an implausible-scaling artefact (see header note) is **not an artefact — it is consensus deliberately modelling a cycle-down**, and placing it is the whole value of the row.

| SNDK consensus (BBG live, 2026-08-28, `BEST_FPERIOD_OVERRIDE`) | 1FY (FY-Jun-27) | 2FY (FY28) | 3FY (FY29) |
|---|--:|--:|--:|
| Revenue ($m) | 48,825.5 | 58,588.7 | **52,670.9** |
| y/y | — | +20.0% | **−10.1%** |
| EBIT margin | 79.5% | 78.5% | **71.4%** |
| EPS (median) | 211.74 | 259.46 | **211.10** (−18.6% y/y) |
| EPS street-high | 238.36 | 361.20 | **330.00** |
| Street-high premium to median | +12.6% | +39.2% | **+56.3%** |

➤ **The divergence, stated as a number: management guided mid-to-high-teens revenue growth EVERY year FY28-30 (Investor Day, 2026-08-13). At +16%, FY29 revenue would be ~$67,963m. Consensus carries $52,671m — roughly 22.5% BELOW the company's own framework, and pointing the opposite way in sign (−10.1% versus ~+16%).** The Street is not merely conservative on the out-year; it is modelling a cyclical downturn that management says will not happen.

✅ **This CORROBORATES two marks already on [[SNDK]] and converts both from prose into a placed figure.** (a) Jefferies: *"implies big upward revisions to current consensus forecasts (+16% / −4% / −30% y-y for FY28E/29E/30E)"* — the −4% FY29E and the sign flip are now confirmed directly off the wrapper. (b) Bernstein's own model does the same thing while carrying the Street-HIGH target: FY27 $50.0bn → FY28 $56.8bn → **FY29 $50.1bn (−11.9%)** → FY30 $53.0bn. **Bernstein's $3,000 and consensus agree that FY29 declines; they disagree only on the multiple.**

🔴 **The read: the durability debate is unresolved in consensus itself, and the dispersion proves it — the street-high premium WIDENS from +12.6% (1FY) to +39.2% (2FY) to +56.3% (3FY). The bull and bear tails diverge fastest in exactly the year the NBM book is supposed to be protecting.** ➤ **The falsifiable test is the NBM coverage disclosure, not the price tape: management stated FY29 NBM coverage is *"consistent with the '28 number so far"* (~two-thirds of bits), withheld only because it is still being optimised. If that holds, a −10% FY29 revenue line requires ASPs to fall through a contracted floor on two-thirds of volume — which is the one thing the NBM structure is designed to prevent.**

⚠️ **Basis guard: these are FISCAL-year lines (SNDK FY ends ~Jun), pulled with the period override — NOT the CY sums in `estimates.json`, which straddle fiscal years and would manufacture a different gap. Do not mix the two.** ⚠️ **`estimates.json` carries no FY29/CY2028 column at all, so this row is only reproducible from the live wrapper.**


## ✅ CONFIRMS — no action

| # | Name | New datapoint | Baseline | Verdict |
|---|---|---|---|---|
| 1 | **[[CRM]]** | FY27 non-GAAP EPS guide **$16.67-16.71** | **BBG 1FY consensus $16.713** | ✅ **Consensus is AT the top of the guide (+0.0-0.3%). Fully absorbed.** |
| 2 | **[[CRM]]** | FY27 revenue guide raised $200m to **~$46bn** | BBG 1FY `BEST_SALES` **$46,244m** | ✅ In line |
| 3 | **[[CRM]]** | FY27 non-GAAP operating margin **34% reaffirmed** | BBG 1FY EBIT/Sales = $15,900m/$46,244m = **34.4%** | ✅ In line — and note the margin was **held, not raised**, with the Deputy CFO naming **token spend** as the reason |
| 4 | **[[CRM]]** | William Blair **FY28E EPS $16.07 BELOW FY27E $16.71** (the investment gain rolling off) | BBG **2FY $15.952 < 1FY $16.713** | ✅✅ **Consensus independently shows the SAME year-on-year DECLINE. The "$2.53 of strategic-investment gains inside non-GAAP EPS" mechanic this page flagged is visibly embedded in the consensus curve — it is not a William Blair quirk.** |
| 5 | **[[NVDA]]** | Commitments: **$279bn** supply-and-capacity row, **$366bn** five-row total, **$56bn** second table, **$108.5bn** guarantees | Prior wiki: four broker numbers ($279bn / $311bn / ~$350bn / $366bn) logged as "different bases, do not net" | ✅ **The company primary CONFIRMS the page's refusal to net them, and identifies which is which. JPM's "~$350bn" is the only one that maps to no primary line — a rounded restatement of the $366bn total.** |
| 6 | **[[NVDA]]** | China DC Hopper **<1% of DC revenue**; FQ3 guide assumes **zero** China DC compute | Prior wiki carried both from the call | ✅ Verbatim confirmation from the company primary |
| 7 | **[[NVDA]]** house EPS | House 2027E non-GAAP **$15.49** | BBG 2FY **$14.915** | ✅ House **+3.9%** — inside tolerance, and directionally consistent with the house's higher revenue |
| 8 | **[[LITE]]** | NPO pulled forward *"late 2028/early 2029"* → *"**late 2027/early 2028**"* | Prior wiki 08-25: "NPO pulled FORWARD CY29 → CY28"; Jefferies conference 08-27: CPO slips to 2H C28+, NPO fills the gap | ✅✅ **Three sources, same direction — and this one is the company itself, with the mechanism (*"the market has caught on to these same PHYSICS issues"*)** |
| 9 | **[[MU]]** | The `1FY` consensus row this report EXCLUDED as implausible ($129.3bn sales, 76% EBIT margin) | BBG live 2026-08-28 **$129,311.2m / 76.2% / EPS $72.78** vs **BMO's independently-built FY26E $129,099m / EPS $73.00** | ✅✅ **RESOLVED — consensus is RIGHT and the exclusion was the error. +0.16% on revenue and −0.30% on EPS against a bottom-up broker model, because three of the four quarters are ALREADY REPORTED ($13,643 + $23,860 + $41,456) plus a guided ~$50bn. The original flag compared a fiscal YEAR to one QUARTER's revenue. No house edge is asserted or removed — the row simply returns to service as a baseline.** |
| 9 | **HBM de-spec** | DAMNANG: **~1.63x** effective output, HBM revenue at **81.5-98% of plan** | Jefferies, independently and with a model: de-spec *"stretches a constrained die pool and INCREASES accelerator shipments… does not undermine structural bit growth"* | ✅✅ **Two independent sources, one with a model, same conclusion. Also consistent with this page's own supply evidence — SK Hynix "tight even over the long term", UBS Korea DRAM fulfilment ratio 60%.** |
| 10 | **[[ALAB]]/[[COHR]]/[[LITE]]** | CPO ~C29, NPO C27-C28 | Three separate suppliers in one conference week | ✅ Converged |
| 11 | **[[ARM]]** | AGI CPU demand **>$2bn FY27-28** against a **$1bn TSMC allocation** | BBG 1FY sales **$6,070m** → the new business is **16-33% of current revenue**; consensus 1FY→2FY revenue **+35%** | ✅ **Consistent in scale.** ⚠️ But note management guided **total royalty growth DOWN to high-teens from ~20% on smartphone weakness** — the DC doubling is offsetting mobile, not adding to a healthy base. Consensus +35% total revenue growth is carried by licensing + AGI CPU, not royalties. |
| 12 | **[[TXN]]** | DC run-rate *"well north of $2bn"*, power ~half | BBG 1FY sales **$21,751m** → DC ≈ **9%+ of revenue** | ✅ Plausible and additive; no conflict |
| 13 | **[[NXPI]]** | GM leverage **~100bp per $1bn**, approaching **60% at ~$16bn** revenue | BBG 3FY sales **$17,388m** | ✅ **Consensus revenue crosses the $16bn threshold by FY29 — management's own GM algorithm is reachable inside the consensus horizon.** |
| 14 | **[[AMD]]** | *"Building toward a **$100bn server business**"*; **6GW** OpenAI/Meta over 4 years | BBG **3FY total company sales $119bn** | ✅ **The $100bn server ambition sits BEYOND the consensus horizon (it would be ~84% of FY29 total company revenue). Correctly read as an ambition, not a forecast** — no conflict, but do not let it into a model. |

---

## Verification queue (highest priority first)

1. 🔴🔴 **[[LITE]] "$40 FY28 earnings power"** — obtain the primary Deutsche Bank conference transcript (Bloomberg or company). The number is +20% vs consensus and +33% vs the house model, and it currently rests on an AI-generated digest. **Nothing should be modelled until this is verified.**
2. 🔴 **[[META]] house capex** — the house $170bn is ~14% below consensus $197bn and ~15-25% below the buy-side floor; the FCF consequence is the live issue.
3. 🔴 **[[NVDA]] house gross margin** — house ~74% vs management's guided 72-73% FY28. Also decide the LPDDR5 consignment treatment before bridging FQ3.
4. ~~⚠️ **`MU` and `SNDK` BBG consensus rows** — implausible scaling (see header note). Route to `/wiki-consensus`.~~ ✅ **DONE 2026-08-28 — and it resolved AGAINST the flag: both rows are correct.** `MU` reproduces to +0.16% of BMO's bottom-up FY26E; `SNDK`'s 1FY sits BELOW two broker models (SIG $51.4bn, Bernstein $50.0bn). **The `SNDK` 3FY line was the real find and is now item 10 in `DIVERGES`: consensus models FY29 revenue −10.1% against a mid-to-high-teens company guide, ~22.5% below the framework.** ⚠️ **New standing item: neither row is reproducible from `estimates.json` — the FY ladder needs the live wrapper with `BEST_FPERIOD_OVERRIDE`.**
5. ⚠️ **[[VEEV]]** — correct the page's framing of "14% growth" as bearish; it is above the sell-side aggregate (+12.2%) and below the buy-side assumption only.

---

_BBG column resolved 2026-08-28 — `estimates.json` asof **2026-08-28** (99/99 live, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 `carried_over` stamps, and **0 records byte-identical to the 08-27 vintage**, so no silent carry-overs), plus an ad-hoc live `BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY` pull of `BEST_SALES / BEST_EBIT / BEST_NET_INCOME / BEST_EPS / BEST_EPS_HI / BEST_CAPEX` for `MU` and `SNDK`. **No `PENDING` cell existed in this report, nor anywhere in the 43-file backlog** — independently re-verified this run by scanning for literal table-cell `PENDING` values rather than trusting the prior run's summary line. **The two EXCLUDED consensus rows are the work this run actually did: both were validated and readmitted — `MU` into `CONFIRMS` (row 9), and `SNDK` into `DIVERGES` (item 10), where its 3FY line turned out to carry the largest house-vs-Street gap on the wiki.** Canonical header `## Where the new data DIVERGES` applied (was `## 🔴 DIVERGES — the alpha`). **No web data was substituted at any point.**_
