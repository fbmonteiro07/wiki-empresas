# Reconciliation — /run-inbox 2026-08-27 (23h scheduled run)

_Every NEW quantitative datapoint from tonight's 13 ingested sources, placed against **three baselines**: (1) prior wiki comments already on the page, (2) the Capstone house model, (3) BBG consensus._

**BBG status: ✅ LIVE.** Pulled 2026-08-27 via the Capstone wrapper (`E:\bloomberg_api`, `bdp`, `BEST_FPERIOD_OVERRIDE` passed as a **kwarg**, not in an `overrides=` dict — the dict form raises `BAD_ARGS / Invalid override field`). Fields: `BEST_EPS`, `BEST_SALES`, `BEST_EBIT`, `BEST_CAPEX` at `1FY/2FY/3FY`. **Periods are each company's own FISCAL years**, which avoids the CY-sum wedge documented in `_meta/assumptions.md`.

⚠️ **Two consensus rows were EXCLUDED from this report as implausible-and-unverified rather than used: `MU` (1FY sales $129.3bn on a ~$45bn base, 76% EBIT margin) and `SNDK` (1FY sales $48.8bn, 79% EBIT margin, and 3FY EPS BELOW 2FY).** Per the standing rule on this wiki, these are **not** being rejected on plausibility — they are simply not being used as a baseline until the basis is verified, because neither name carries a new quantitative datapoint tonight (both were qualitative de-spec read-throughs). **Flagged for `/wiki-consensus` to check the currency/scaling on those two tickers.**

---

## 🔴 DIVERGES — the alpha

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
4. ⚠️ **`MU` and `SNDK` BBG consensus rows** — implausible scaling (see header note). Route to `/wiki-consensus`.
5. ⚠️ **[[VEEV]]** — correct the page's framing of "14% growth" as bearish; it is above the sell-side aggregate (+12.2%) and below the buy-side assumption only.
