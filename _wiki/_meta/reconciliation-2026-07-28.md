# Reconciliation — run-inbox 2026-07-28

_Every NEW quantitative datapoint from this run, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`, asof 2026-07-28), (3) BBG consensus._

**Sources reconciled**
- **S1** Fubon Research · Sherman Shang / Daniel Yang — "Our advanced packaging, CoWoS forecast adjustments; other updates", 2026-07-28
- **S2** Morgan Stanley · Brian Nowak CFA — "The Paths to 25-50% GenAI ROIC", 2026-07-27
- **S3** Micron IR call · "Satish", 2026-07-27
- **S4** Morgan Stanley TMT webcast · Joe Moore / Meta Marshall / Lee Simpson / Erik Woodring / host Sean, 2026-07-28

## ⚠ On the BBG column

`bdp` raised **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal"** at reconciliation time, so **no live re-query was possible.** However `_data/estimates.json` carries a **stored pull dated 2026-07-28 (today)**, so the consensus column below is real BBG consensus from today's pull, *not* a live quote and *not* substituted web data. Prices in that pull are the 07-28 marks (MSFT $393.35, MU $820.53, NVDA $197.01, AAPL $340.08 …).
**Action:** log into the Terminal / reconnect the Capstone VPN and re-run `wiki-consensus` if you need an intraday mark. Nothing below is blocked on it.
Consensus figures are **CY-basis** (calendar-year sums, uniform non-GAAP) — several sell-side marks here are **fiscal**-year. Period mismatches are called out inline rather than netted.

---

# DIVERGES — the alpha

### 1. MU — the $100bn RPO is a **floor-price** number, and back-solving the floor is the trade
**New (S3):** Satish states the ~**$100bn RPO** on the 14 priced SCAs is computed as **contract volumes × the FLOOR price**, and that actual SCA revenue "will be well above the RPO levels" because pricing currently sits **at the ceiling** (≈ the June-CQ market price).
**Prior wiki:** the page carried "16 SCAs; 14 = $100B min floor" — the number was already logged but **not the basis**. This is the material addition.
**Back-solve.** SCAs = ~25% of revenue as of earnings; the F4Q26 guide is ~$50bn/qtr ⇒ ~**$50bn/yr of SCA revenue at current pricing**. Against a $100bn RPO:

| Remaining SCA horizon | Revenue at current price | Implied floor as % of current |
|---|---|---|
| 3 years | ~$150bn | ~67% |
| 4 years | ~$200bn | ~**50%** |
| 5 years | ~$250bn | ~40% |

**Cross-check, and it holds.** At ~50% of current pricing with COGS unchanged and today's 86% GM, the floor GM computes to **~72%** — which is exactly "**well above**" the fiscal-2018 low-60s cyclical peak Satish names as the benchmark, without being near 86%. The two disclosures are internally consistent and jointly pin the floor at roughly **40-67% of current pricing**.
**Why it is alpha:** anyone anchoring a downside case on the RPO is anchoring on the **bear bound**, and anyone treating "GM well above the prior peak" as protection is accepting a **~35-45% price haircut** in that scenario. BBG has CY2027 GM at **86.0%** — i.e. consensus carries the *ceiling* GM as the full-year 2027 number.
**Action:** the gap between the 86% ceiling and the ~72% implied floor is the range the SCA structure actually guarantees. Logged to `MU.md`; feeds the edge tracker.

### 2. CDNS — consensus has essentially nothing in for agentic EDA
**New (S4, Lee Simpson):** record backlog, ~5-6th consecutive beat-and-raise, and agentic EDA called "**a demand accelerator**" with the full design flow now offered, **20+ ChipStack engagements with a number already paying**, NVIDIA named as a user — and explicitly "**a small amount second half 26, but really a 2027 story**."
**BBG consensus:** CY2026 revenue $6,275mn → CY2027 **$7,127mn = +13.6%**; EPS $7.99 → $9.46.
**House:** no Capstone CDNS model.
**Divergence:** consensus models 2027 revenue growth of **+13.6%**, essentially CDNS's structural rate, with **no visible contribution from the thing the analyst calls a demand accelerator in exactly that year**. Either the agentic monetisation is immaterial or 2027 numbers are too low. Cleanest upside asymmetry in the batch.
**Watch:** 2H26 monetisation disclosure and the FY27 guide.

### 3. META — MS's own model contains the ROIC bear it is arguing against
**New (S2):** Overweight, **Top Pick, PT $775** (DCF ~8% WACC / ~3% terminal ⇒ ~23x '27 P/E). GAAP operating income **92,216 (26e) → 101,748 (27e) → 104,841 (28e)**.
**BBG consensus:** CY2026 EBIT **87,298**, CY2027 **106,120**; CY2026 EPS **34.87**, CY2027 **35.62**.
**House:** 2026E EPS **32.72**, 2027E **38.24**; revenue 257 / 313.
**Divergence, three layers:**
- MS's **2028 operating income grows +3.0%** (101,748 → 104,841) against ~20% constant-currency revenue growth on MS's own capex path. The Top Pick rests on call options MS says are outside the base numbers.
- MS's **2027 GAAP operating income (101,748) is ~4% BELOW BBG CY2027 EBIT (106,120)** — the most bullish seat on the name is below consensus on '27 profit.
- **House (32.72) and MS (32.49) agree with each other and both sit ~7% BELOW BBG CY2026 EPS (34.87).** That is a coherent, corroborated house-vs-Street short on 2026 earnings — the house view just got a second vote.
**Action:** the house's below-consensus 2026 META EPS is **confirmed by MS**; the divergence to press is consensus CY2026 EPS, not the PT.

### 4. AAPL — the house model's above-consensus EPS runs straight into the memory-BoM margin call
**New (S4, Erik Woodring):** September-quarter **gross margin ~60bp BELOW consensus** and **services growth 0.5-1.0pt below consensus**, driven by **memory-cost BoM inflation** landing in a quarter with two months of no iPhone price increases. Also: **80-90% of the rally is factor/positioning/thematic, not fundamental**.
**House:** 2026 revenue **480**, EPS **10.12**; 2027 revenue 539, EPS **11.11** (fiscal basis).
**BBG consensus:** CY2026 revenue **488,056**, EPS **8.90**; CY2027 revenue 535,043, EPS **10.12**; GM 47.7% both years.
**Divergence:** the house is **slightly BELOW consensus on revenue** but **+13.7% ABOVE on 2026 EPS** (10.12 vs 8.90) and **+9.8% above on 2027** — i.e. the house edge on AAPL is **entirely a margin call**. Woodring is pushing the opposite way on exactly that line, for a structural reason (memory) the house model has to absorb.
**Basis caveat:** house years are fiscal (Sept), BBG is calendar — directional, not like-for-like.
**Action:** stress the house AAPL margin assumption against a doubling HBM/DRAM cost curve (see item 5). This is the highest-priority house-model review item from this run.

### 5. NVDA — Fubon's unit math sits above consensus revenue growth, and supports the house
**New (S1):** chip output **12.4mn in 2027 vs 8.2mn in 2026 (+51%)**; **Rubin ASP US$78-80K** at a held **75-80% chip GM**; **HBM4 at US$31-32/GB vs US$17-18/GB for HBM3e** (and US$35-36/GB for everyone else).
**BBG consensus:** CY2026 revenue 391,860 → CY2027 **567,073 = +44.7%**; GM 74.9% → 74.3%.
**House:** 2026E revenue **407** → 2027E **661 = +62%**; GM 75% → 74%.
**Divergence:** Fubon has **units +51%** *with ASP inflating* — those two multiply. Consensus revenue growth of **+44.7% is below the unit growth alone**, which implies consensus is carrying flat-to-down blended ASPs into a year Fubon has Rubin repricing sharply higher. The **house at +62% is the number consistent with Fubon's build**; the house sits **+16.6% above BBG CY2027 revenue** ($661bn vs $567bn) and this run's supply-side data supports it.
**The matched pair to watch:** house GM of 74% in 2027 and consensus 74.3% **both depend on the $78-80K Rubin ASP actually landing**, because HBM4 content cost roughly doubles. ASP and GM are one assumption, not two — if the ASP slips, the GM goes with it.
**Offsetting near-term negative, already logged:** Rubin 2026 volume cut to ~1mn on the thermal redesign/push-out (offset by 3Q26 Blackwell, so 2026 output roughly unchanged), with **KYEC cutting its FY26 guide to high-30s% from 40%** as the first company-level confirmation that the delay bites the supply chain.

### 6. ARM — the FY28 CPU number the market now demands is ~27% of consensus revenue
**New (S4, Lee Simpson):** Equal-weight, "**about 200 is the right level**"; it is "**well expected they'll raise the FY28 [CPU] number to $2bn, so that for me is a minimum**."
**Prior wiki:** the same analyst on **07-22** did *not* expect a formal CPU-TAM update, with management merely "pointing to upside vs the ~**$1bn** FY28 sales guide". **The guide is now assumed to double, and the doubling is the floor** — a materially higher bar set by the same seat in six days.
**BBG consensus:** CY2026 revenue $5,611mn → CY2027 **$7,432mn**; EPS 1.99 → 2.79. ARM FY28 (ending Mar-2028) ≈ CY2027.
**Divergence:** a **$2bn** own-silicon CPU line would be ~**27% of consensus CY2027 revenue** — far too large to be sitting inside a $7.4bn consensus alongside unchanged royalty/licensing assumptions. Either consensus revenue is materially too low or the $2bn is a TAM/bookings number rather than recognised revenue. **Resolve the basis before treating it as an estimate.**
**Valuation tension:** fair value ~$200 against a **$244.74** BBG price = **~18% downside** from the analyst who is also setting the highest CPU bar. Rating and number are pulling opposite ways.
**Catalyst:** Q1 print, Wednesday.

### 7. SKHYNIX — the print landed at the bottom of the range and below the consensus run-rate
**New (S4, Sean, pre-print):** buyside bogey **KRW 60-65tn**, MS at **65tn** with drift toward a 60 handle; "the reaction matters more than the number."
**Prior wiki:** actual **OP KRW 60.54tn** (revenue KRW 79.3tn vs KRW 83.9tn) — the bottom of the range, and **~7% below MS's own 65tn**.
**BBG consensus:** CY2026 EBIT **KRW 273.1tn** ⇒ ~**KRW 68tn/quarter** implied run-rate.
**Divergence:** the Q2 actual of **60.54tn is ~11% below the quarterly run-rate embedded in the CY2026 consensus**, which means the back half has to carry more than the print implies. Consensus CY2027 EBIT of 439.5tn (+61%) is the number under pressure, not CY2026.
**⚠ Date tension, unresolved:** S4 is filed 2026-07-28 but is internally **pre-print** ("Hynix tomorrow… Samsung on Thursday"), while the wiki dates the SKHYNIX Q2 print 2026-07-28. All S4 Hynix commentary is labelled pre-print on the page rather than reconciled away.

### 8. AMZN — MS is far above consensus on EBIT but not on EPS
**New (S2):** OW **PT $330**; FY Dec-26e revenue **826,010**, GAAP EBIT **114,379 (26e) → 162,602 (27e)**; **AWS growth 34.9% (26e) → 40.2% (27e) → 36.2% (28e)**.
**BBG consensus:** CY2026 revenue **821,209**, EBIT **100,788**, EPS 9.33; CY2027 revenue 935,048, EBIT **131,403**, EPS **11.98**.
**Divergence:** revenue is **in line (+0.6%)** but MS EBIT is **+13.5% above consensus in 2026 and +23.7% above in 2027** — while MS's implied '27 EPS (~$11.4, back-solved from ~29x '27 on the $13 average) is **at or slightly below** the 11.98 consensus. Above-consensus operating profit that does not reach EPS points to depreciation, tax or share count below the line. **Basis caveat: MS EBIT is GAAP, BBG EBIT is adjusted** — part of the gap is definitional, but not 24 points of it.
**Also:** MS's **40.2% AWS growth in 2027 is the page-high mark**, above GS ~35%, JPM +32.4% and the 35-36% buy-side bogey.

### 9. MEDIATEK — an ~8x CoWoS allocation step against +69% consensus revenue
**New (S1):** TSMC CoWoS allocation **1.5% / 17,400 wafers (2026) → 7.3% / 137,700 (2027)** — a **~7.9x** step that makes MTK TSMC's #4 CoWoS customer; Fubon's **top pick for TPU** and expects MTK to "further raise its custom-ASIC market share in 2027."
**BBG consensus:** CY2026 revenue TWD 651,500mn → CY2027 **1,099,772mn = +68.8%**; EPS 65.47 → **135.25 (+107%)**.
**Divergence (bullish, with a caveat):** consensus already embeds a large ASIC ramp, but a ~7.9x allocation increase is a bigger vector than +69% total revenue implies. **Caveat: CoWoS ASIC is a small base inside a company still dominated by smartphone SoC**, so the two growth rates are not on the same denominator — this is an upside vector to size, not a clean edge.
**Note:** MEDIATEK has **no `## Intra-quarter` section and no timeline JSON** — `build_intraquarter.py` does not cover it. Content was folded into Debate + the existing CoWoS-allocation section.

### 10. AMD — the ASE half of the allocation is not visible in the TSMC-only line
**New (S1):** **total** CoWoS allocation rises to **300k wafers in 2027**, majority of the increase at **ASE**; TSMC-only runs 7.2% → 7.0% = **84,300 → 132,300**, implying **~170k of the 300k sits at ASE**. Driver named as "agentic AI and strong server CPU demand" — the **Venice/CPU leg, not MI-series**.
**BBG consensus:** CY2026 revenue 49,334 → CY2027 **78,248 = +58.6%** — strikingly close to the **+57%** TSMC-only wafer growth.
**Divergence (bullish):** if consensus is calibrated to the TSMC-only ramp, the **ASE tranche is incremental** and 2027 revenue growth has upside to +58.6%. Requires confirming that the 300k is accelerator-only and not double-counting.

---

# CONFIRMS — no action

| # | Name | New datapoint | Baselines | Read |
|---|---|---|---|---|
| 11 | **AVGO** | S1: 2027 CoWoS **22.3% / 421,800 wafers**, +60% off 263,100 | BBG CY2027 rev **190,031 = +54.0%**; **house 2027 rev 190.0 — an exact match to consensus**; house EPS 21.07 vs BBG 21.17 | Wafer growth and revenue growth line up. House = consensus for 2027; the entire house edge sits in **2028 (rev 315 / EPS 35.96)**, untested here. Fubon's cut from its own 06-05 24-25%/~459.6k is a **share** trim on a pool going 1,170k → 1,890k — absolute wafers still rise ~60%. Denominator effect, not a cut. |
| 12 | **INTC** | S1: EMIB **10-12k/mo end-2026 → 24-25k/mo end-2027**; CFO earmarks a large share of the capex increase for advanced packaging / EMIB-T | BBG capex CY2026 **19,227 → CY2027 24,503 (+27%)** | Consensus already carries a **+$5.3bn capex step into 2027**. Fubon supplies the *reason* rather than a new number. Revenue consensus +19.5%, EPS 1.00 → 2.01. |
| 13 | **SNDK** | S4 (Joe Moore): enterprise NAND **>70 cents on multiple transactions, +60-70% vs Q2**; LTA pushback reversed | BBG CY2026 GM **81.3% → CY2027 84.5%**; revenue 37,703 → **57,614 (+52.8%)** | Consensus already models extreme NAND margins. The spot datapoint confirms the pricing path rather than extending it. Weakness confined to consumer/PC/smartphone. |
| 14 | **STX / WDC** | S4 (Woodring): pricing-driven beat-and-raise; **non-LTA hikes of 30/40/50%**; **~50% GM, 70-80% incremental, "nowhere close to peak"** | STX BBG GM **50.5% (CY26) → 57.4% (CY27)**; WDC **52.4% → 58.6%**. STX CY27 EPS 35.01 (+67%); MS PT STX $1,035 vs px 747.30 (+38.5%), WDC $650 vs px 463.51 (+40.2%) | Direction confirmed and consensus **already embeds ~+7pts of GM expansion** — a high bar, but Woodring's "nowhere close to peak" is the more aggressive claim. ⚠ His pre-print bar was **sequential** (~3-4% q/q company-implied vs bulls at 8-14%) while the print disclosed **y/y** — the bulls were not straightforwardly vindicated. Same analyst as the 07-26/27 PT moves, so **nothing re-logged**. |
| 15 | **SAMSUNG** | S4 (Sean): prelim OP vs ~KRW 85tn consensus, near KRW 100tn ex-provision, stock still **-7%** | BBG CY2026 EBIT **KRW 364.2tn ⇒ ~KRW 91tn/qtr**; prelim actual on the page **KRW 89.4tn** | Print is on the CY2026 consensus run-rate. ⚠ **Provision size unreconciled**: Sean's "close to 100tn ex-provision" implies ~KRW 11tn vs the page's JPM/BofA **~KRW 15tn+ / KRW 110-120tn underlying**. Buyback mechanics (3-yr 50%-of-FCF policy expiring, Q4-results window, ~KRW 40tn stock bonus, book-value trigger) are net-new colour with no consensus equivalent. |
| 16 | **TSM** | S1: CoWoS **180kwpm end-2027 held / 220kwpm end-2028 with upside**; wafer series 129k → 1,890k (+61.5% in 2027); **SoIC cut 90k → 70k in 4Q28** | BBG CY2027 revenue **+35.3%** | CoWoS is a subset of TSMC revenue, so +61.5% vs +35.3% is not a like-for-like edge — recorded as context. ⚠ **BBG TSM EPS (CY2026 519.02 / CY2027 709.63 NT$) is an order of magnitude above the house's NT$102.5 / NT$143.5 and above reported history — an ADR-ratio / scaling artifact in the stored pull. EPS excluded from this reconciliation; revenue used.** |
| 17 | **MSFT** | S2: OW **PT $600**, FY28e EPS **$23.86**; Azure **40.0 → 42.3 → 43.0%** FY26-28e; IaaS framework ~67% incremental margin / ~31% ROIC | BBG CY2026 EPS **17.73**, CY2027 **20.88**; px **$393.35** | MS FY Jun basis vs BBG CY basis — **not like-for-like**, directional only. The check that matters is **Azure accelerating in every one of the next three fiscal years**, which is the aggressive part of the thesis, not the PT. **Correction carried: MSFT spot is $381.70 in the note (back-solved from all three scenario returns); the $561.57 figure is the mean consensus PT, not the price.** MS's own caveat that *reported* incremental margins run below the 60-70% band resolves the apparent conflict with Redburn's ~12-13% — not a real disagreement. |
| 18 | **GLW** | S4 (Marshall): Enterprise **+65% y/y**, Telco flat, guide light vs a ~**$200mn** revenue / few-cents EPS bar | BBG CY2026 revenue 19,086 → CY2027 **22,880 (+19.9%)**; EPS 3.23 → 4.30 | Consensus carries +20% revenue and +33% EPS into 2027; a light guide against a modest upside bar does not break it. ⚠ **"Essentially flat" Telco vs the print's Carrier -9% q/q is probably a q/q-vs-y/y basis gap**, but Marshall also offers a different *cause* (supply reallocation into Enterprise) vs Barclays' pull-in/LTA-lumpiness read. Her CPO-scale downshift is a **2028** issue, outside this consensus window. |
| 19 | **ANET** | S4 (Marshall): interest in Arista, business "expected to accelerate next year" | BBG CY2026 revenue 11,531 → CY2027 **14,296 = +24.0%** | ⚠ **Consensus does not currently show acceleration into 2027** on the CY basis available. Whether Marshall's claim diverges depends on the CY2026 growth rate, which the stored pull does not carry — **re-check when BBG is back**. One line of positioning colour, deliberately not inflated. |
| 20 | **MU (guide)** | S3: **F4Q26 gross margin guide 86%**, up from ~85% | BBG CY2026 GM **83.2%**, CY2027 **86.0%** | Consensus carries the **ceiling GM as the full-year 2027 number** — i.e. the Street assumes the guide holds for five-plus quarters. Confirms the cycle; see item 1 for what the floor implies if it does not. Joe Moore's "positive at 800, not at 1200" is live: BBG px **$820.53**. |

---

# Excluded — basis artifacts, not edges

Screened out so they do not reach the edge tracker as false divergences:

1. **GOOG revenue — gross vs net.** MS FY26e revenue **500,611** and the house's **505** both sit ~18% above BBG CY2026 **424,583**. The house and MS agree with each other; the BBG series is the outlier and is almost certainly on a different (ex-TAC / net) revenue definition. **Not an edge.**
2. **GOOG EPS / net income — the MS table is internally impossible.** MS shows FY26e **net income 255,100 against EBITDA 241,667**, and two different operating-income series in the same exhibit. EPS 20.62 against BBG 12.87 and house 11.80 cannot be reconciled while net income exceeds EBITDA. **Treated as an OCR/one-off data-quality failure and excluded.** The clean comparison that survives: **house 2026E EPS 11.80 vs BBG CY2026 12.87 (house -8.3%)**, and house 2027E 16.20 vs BBG 16.23 (in line).
3. **TSM EPS scaling.** See item 16 — BBG CY EPS in the stored pull is inconsistent with reported history and with the house model; an ADR-ratio artifact.
4. **CXMT capacity.** S4's "**about 30,000 wafers**" is an order of magnitude below the **~290-350k wspm** carried from Wells Fargo (07-14) and BofA (07-12). Recorded as reported and flagged on SKHYNIX / china-export / outros-asia; **the existing page marks were left standing and the 30k was not adopted.**
5. **AVGO share-vs-wafers framing.** Fubon's 2027 share trim to 22.3% is a **wafer/unit** claim on a growing pool and does **not** contradict MS's ~80%-of-TPU-**revenue** defence. Different denominators.
6. **NVDA — no rating in S2.** The MS ROIC note carries no NVDA rating or PT. Its GB300 economics are logged as a **demand-durability read-through only**; nobody should back-solve a target from it.

---

# Open questions carried forward

1. **Fubon reverses itself on Google/Intel in 20 days** — 07-08 "Google falls back on TSMC's 2028 CoWoS (95%+ yield bar very challenging)" → 07-28 "**Intel's supply is a must by 2028**". Logged as **capacity arithmetic, not a yield capitulation**: Fubon does not withdraw the yield concern. The wiki's three-way TPU-v9 packaging split is now **2-vs-1 for EMIB-T**, with UBS's own Arcuri still dissenting. **Not resolved.**
2. **INTC EMIB capacity vs UBS's package count** — Fubon's 24-25k/month exit rate implies ~290-300k packages/yr entering 2028 against **UBS's 2.3mn Google-TPU packages in 2028E** (07-27). Different bases or a further large step assumed.
3. **SoIC direction** — Fubon says TSMC is **slowing** SoIC to feed CoWoS; Redburn (06-23) and Susquehanna (07-11) both have SoIC expanding aggressively through 2028. If Fubon is right the exposed name is **BESI**.
4. **NPO/CPO vs CPO scale** — Fubon has NVDA leaning into NPO/CPO for the two-rack "Taycan" design; Marshall the same week cuts 2028 CPO scale. Opposite signs for 2028 optical content.
5. **AAPL into the print** — GS/Ng (07-27) models a beat with Services holding up; Woodring (07-28) is below consensus on **both** Services and September GM. Same two lines, opposite sides, 24 hours apart.
6. **MU content growth** — Satish concedes customers are cutting the *rate* of memory content growth but calls it **rationing, not optimisation**. Agrees with SemiAnalysis on the fact, differs on whether it reverses when supply arrives. Now testable.
7. **ARM $2bn** — recognised revenue or TAM/bookings? Resolve before modelling (item 6).

---

## Priority actions
1. **Stress the house AAPL margin assumption** against the memory-BoM curve — the house's +13.7% EPS premium to consensus is a pure margin call and this run put a named structural headwind on it (item 4).
2. **CDNS 2027** — consensus has nothing in for agentic EDA (item 2). Cleanest upside asymmetry in the batch.
3. **Press the house's below-consensus META CY2026 EPS** — now corroborated by MS (item 3).
4. **MU** — carry the ~40-67%-of-current implied SCA floor as the real downside bound, not the RPO (item 1).
5. **Re-run `wiki-consensus` once the Terminal is back** to refresh prices and resolve the ANET acceleration check (item 19) and the TSM EPS scaling artifact (item 16).
