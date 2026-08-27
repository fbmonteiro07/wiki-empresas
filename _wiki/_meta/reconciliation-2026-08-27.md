# Reconciliation — 2026-08-27 (`/run-inbox`, post-NVDA-print)

_Every NEW quantitative datapoint from this run, placed against three baselines: **(1)** prior wiki comments, **(2)** the Capstone house model, **(3)** BBG consensus (`_wiki/_data/estimates.json`, **asof 2026-08-27**, refreshed by `wiki-consensus` at 09:12 — BBG has already rolled `lrq` to 2026-07-26, i.e. it recognises NVDA's just-reported quarter). Purely qualitative/thematic sources are skipped._

⚠️⚠️ **THREE BASIS WARNINGS THAT GOVERN EVERY NVDA ROW BELOW, STATED ONCE.**
1. **FY ≠ CY.** NVIDIA's FY28 runs ~Feb-2027 → Jan-2028. It is compared against BBG **CY2027** here because that is the closest available frame — there is **no CY2028 in the file at all**. The one-month offset is not adjusted for and is a real source of error in a business growing ~70%.
2. **The CY sums embed PRE-PRINT consensus for reported quarters.** The file's own note says calendar-year figures use kFQ consensus for forecast quarters and reported figures for closed ones. NVDA's CY2026 carries `n_actual: 2`, so half of it is actual and half is forecast.
3. **The 08-27 pull is ~18 hours after an AMC print.** Some contributors will have updated and some will not. Where a gap below is small, it may simply be an un-refreshed contributor rather than a real disagreement. **Gaps under ~1% are not treated as signal.**

---

## 🔴 DIVERGES — the alpha

### 1. 🔴🔴🔴 NVDA GROSS MARGIN — CONSENSUS IS 141-241bp ABOVE MANAGEMENT'S OWN GUIDED TROUGH. THIS IS THE SINGLE LARGEST GAP IN THIS REPORT AND IT IS AGAINST A COMPANY GUIDE, NOT AN OPINION.

| Period | **Management guide (2026-08-26)** | BBG consensus (08-27) | Capstone house | Gap vs BBG |
|---|---|---|---|---|
| FQ3 FY27 (Q3-26E) | **74.0% ±50bp** | **74.49%** | — | **+49bp** — consensus sits at the very top of the guided band |
| FQ4 FY27 (Q4-26E) | **71-72% (the trough)** | **73.41%** | — | 🔴🔴 **+141bp to +241bp** |
| FY28 settle ≈ CY2027 | **72-73%** | **73.30%** | **~74%** | **+30bp to +130bp (BBG); +100bp to +200bp (house)** |
| CY2026 | — | **74.40%** | **~75%** | house **+60bp** vs BBG, and above the FQ3/FQ4 guided path |

**Why this is the alpha and not just a stale-model artefact:** the FQ4 number is the one that matters. Management did not hint at margin pressure — it **reset** guidance, using the words *"we are resetting expectations today,"* and gave a specific trough. **A consensus sitting 141-241bp above a freshly-guided trough is not a rounding difference; it is unrevised.** The cause is named and forward-looking: *"we are experiencing EXTREME PRICING CONDITIONS IN MEMORY. The magnitude of the price increase has EXCEEDED OUR PRIOR EXPECTATIONS and are headed even higher into next year."*

**Against baseline (1), prior wiki comments — this is a clean reversal of the page's own positioning read:**
- JPM Market Intelligence (Josh Meyers, 08-24): *"nobody seems at all concerned the team can't maintain 75% GMs (something underlined by recent checks suggesting price hikes are coming)."* ➜ **The price hikes are real and confirmed by Kress, but they land in FQ1 FY28, AFTER the trough, and only recover to 72-73% — not 75%.**
- JPM buy-side survey (08-25): FQ3 **GPM bogey 74.8%** ➜ **guide 74.0%, an 80bp miss on the one line the buy-side had a number for.**
- UBS/Arcuri (08-14): *"GM ~75% through C2027"* ➜ **dead by company guidance.** His C2027 build (revenue ~$681bn, FCF ~$360bn) rests on it.
- **MS's deliberately conservative 73% CY27 model (MS NDR recap, 07-14) was the closest published mark on the page — and is still ~100bp optimistic against the guided FQ4 trough.**

**Against baseline (2), the house model: `Modelo Felipe NVDA.xlsx` carries ~75% for 2026E and ~74% for 2027E.** Both are now above the company's own path. ➜ **NAMED MODEL BRIDGE: the house GM line needs to come down ~100-200bp in 2027E and the 2026E exit needs to reflect a 71-72% Q4. On the house's own 2027E revenue of $661bn, a 150bp GM cut is ~$9.9bn of gross profit — roughly $0.35-0.40 of EPS before opex and tax effects.** Not applied here; flagged for the model owner.

**⚠️ The honest counter, recorded so this is not read as one-sided:** management frames the memory cost as *"a SYMPTOM OF THE SAME DEMAND SURGE that's driving our own growth,"* and it is raising prices to recover. If the FQ1 FY28 price increases stick, 72-73% is a floor with an upward bias rather than a new normal. **The falsifiable checkpoint is the FQ3 print on 2026-11-17: does 74.0% ±50bp hold, and is the 71-72% FQ4 trough reaffirmed?**

### 2. 🔴🔴 NVDA FY28 REVENUE — MANAGEMENT'S IMPLIED ~$692bn IS ~8% ABOVE BBG CY2027 OF $638bn

| | Figure | Source |
|---|--:|---|
| H1 FY27 actual | **$177,837mn** | Company (press release) |
| FQ3 FY27 guide | **$108,000mn ±2%** | Company |
| FQ4 FY27 (no company guide) | $121,491mn | BBG 2FQ consensus |
| **⇒ Implied FY27** | **~$407,328mn** | derived |
| **⇒ FY28 at the guided +~70%** | **~$692bn** | derived |
| BBG **CY2027** revenue | **$638,464mn** | BBG, asof 08-27 |
| **Gap** | **≈ +8.4%** | |
| Capstone house 2027E revenue | **$661,000mn** | `Modelo Felipe NVDA.xlsx` (2026-06-17) |
| **Gap vs house** | **≈ +4.7%** | |

⚠️⚠️ **CAVEATS, AND THEY ARE LOAD-BEARING: (a) the FY27 base uses a BBG estimate for FQ4, so the derived FY28 inherits that error; (b) FY28 ≠ CY2027 — one month of offset in a ~70%-growth year is worth roughly 4-6% on its own, which could account for MOST of the 8.4% gap; (c) "approximately 70%" is a rounded number.** ➜ **Treat the direction as the signal and the magnitude as indicative: consensus and the house are both BELOW management's own first-ever full-year guide, and the house is closer than the Street.** **The house's 2027E of $661bn sits between BBG's $638bn and management's implied ~$692bn — the house is already leaning the right way.**

🔴 **The genuinely new and un-modelled fact underneath it: the +70% is a SUPPLY number.** *"This is a supply constrained outlook"* against *"customers' forecasts point to our growth DOUBLING next year"* and *"at this moment we have supply for 70%."* ➜ **Any upward revision from here is, by management's own framing, a supply event — so the thing to track is CoWoS/HBM/shell additions, not order commentary. Conversely the downside case is no longer a demand miss; it is a supply miss.**

### 3. 🔴 NVDA REVENUE PER GIGAWATT — MANAGEMENT'S $40bn (VERA RUBIN) vs THE HOUSE'S ~$25bn

| | Revenue per GW | Source |
|---|--:|---|
| Hopper | **~$18bn** | Jensen Huang, 2026-08-26 |
| Grace Blackwell | **~$25bn** | Jensen Huang, 2026-08-26 |
| **Vera Rubin** | **~$40bn** | Jensen Huang, 2026-08-26 |
| Capstone house 2025 / 2026E / 2027E | **~$21 / ~$24 / ~$25bn** | `Modelo Felipe NVDA.xlsx` |
| JPM cross-check (already on page) | $25-35bn | JPM "AI Capex 2.0" |

**This is NOT a straight contradiction and must not be logged as one: the house number is a BLENDED, installed-base-weighted average across generations in a given year, while $40bn is the per-GW content of ONE generation at full configuration.** A 2027 in which Vera Rubin is a minority of shipped GW is entirely consistent with a ~$25bn blended average. ➜ **But it does bound the upside: the house's 2027E of ~$25bn/GW implies Vera Rubin is a small share of 2027 GW. Management says Vera Rubin will be ~20% of FQ3 DC revenue and *"the fastest product ramp in NVIDIA's history."* If the mix shifts faster, the house's revenue/GW — and therefore its $661bn — is low.** **NAMED MODEL BRIDGE: re-cut the house's 2027E GW mix with Vera Rubin at $40bn/GW and Grace Blackwell at $25bn/GW, and see what blended rate falls out.** **Deliberately NOT written into `## Capstone estimates` this run.**

⚠️⚠️ **UNIT DISCIPLINE, per the standing `$/watt` rule: the $40bn is NVDA REVENUE per GW. In the same call Jensen also gave ~$60bn as TOTAL DATACENTRE BUILD COST per GW (from ~$30bn five years ago), and a closing hearsay remark of *"$50 billion data centers."* Three numbers, three bases, and the $50bn contradicts his own $60bn minutes earlier. The $50bn is barred from every series.**

### 4. 🔴 NVDA — ~25% OF FY28 REVENUE IS ATTACHED TO CUSTOMERS NVDA IS FINANCING, AND NO BASELINE ON THIS WIKI HAD A NUMBER FOR IT

*"We expect demand from the AI labs **for which we expect to leverage our balance sheet** to contribute toward **roughly a quarter of our business next year**"* (Kress, 08-26). On the derived FY28 of ~$692bn that is **~$173bn of revenue**.

- **Baseline (1):** the page carried the circularity debate qualitatively for two months with no company-sourced sizing. **Now sized, by the company.**
- **Corroborated on the balance sheet, which is the part that makes it credible:** non-marketable securities **$22,251mn → $51,157mn** in six months (+$28.9bn); marketable equity securities **$12,886mn → $42,783mn**; long-term debt **$7,469mn → $32,366mn**. Management: *"we've invested nearly $50 billion in the frontier AI labs."*
- **Against MS TMT Credit (Lindsay Tyler, 08-24), which is the only house with a framework:** she forecasts **~$200bn of all-in credit exposure by CY28-end** including **~$170bn of adjustments and contingent obligations**, and says *"current spreads arguably price the credit more like a BBB than an AA"* while her own stress case (growth plateaus) still lands at **~0.7x leverage**. ✅ **The two are consistent — ~$173bn of revenue exposure against ~$200bn of credit exposure — which is a rare case of a credit model and a company disclosure agreeing on scale.**
- 🔴 **THE ONE PLACE THE BUY-SIDE WAS TOO BULLISH: JPM's desk (08-24) reported a narrative that the backstopping becomes *"TENS OF BILLIONS of dollars in new revenue."* Management sized the revenue-share stream at *"the potential to drive BILLIONS in revenue over the medium to long term."* Mechanism confirmed; magnitude one order of magnitude lower.**
- **No BBG line exists for this.** It is not a consensus-modelled item.

### 5. 🔴 META — THE ~$10bn 3Q26 LEGAL ACCRUAL IS ALMOST CERTAINLY NOT IN THE CONSENSUS EPS YET

| | Figure |
|---|--:|
| BBG CY2026 EPS (asof 08-27) | **$33.31** |
| BBG CY2026 revenue | $252,502mn |
| Settlement accrual guided into 3Q'26 | **~$10bn pre-tax** (BofA) |
| Shares out | 2,567.0mn (BofA stock data) |
| **⇒ Pre-tax EPS impact** | **~$3.90/share** |
| **⇒ After-tax at ~15-20%** | **~$3.1-3.3/share, ≈9-10% of CY2026 EPS** |

⚠️ **The settlement was announced 2026-08-26 and this pull is 2026-08-27 — a ~$3+/share item cannot plausibly have been absorbed by the full contributor set overnight. Expect a GAAP CY2026 EPS cut of roughly that size.** ➜ **BUT the direction of travel among the covering houses is the opposite: BOTH maintained targets (BofA BUY PO $810, on 24x 2027E GAAP EPS; Barclays OVERWEIGHT PT $780), i.e. they are treating it as a NON-RECURRING charge and looking through it. The reconciliation item is therefore a MECHANICAL one — watch whether BBG's CY2026 GAAP EPS drops ~$3 while CY2027 is untouched. If CY2027 moves, someone is treating the remedies as an ongoing revenue drag, which neither house does.**

✅ **AND A SCORE AGAINST A NUMBER THIS WIKI ALREADY CARRIED: the Oguz Erkan deep dive (08-23, independent Substack) triangulated plausible damages of $24-40bn from the Anthropic authors' settlement and New Mexico v. Meta as yardsticks. Actual: ~$18bn headline, of which only ~$12.7bn unconditional, over ten years. The outcome came in 25% to 70% BELOW his range** — his METHOD (analogising from settled comparables) was sound, his LEVEL was too high, and BofA independently calls it *"less than feared."* **Erkan's estimate is left on the page with this outcome recorded against it.**

⚠️ **UNRESOLVED AND NOT SMOOTHED: BofA says ~$18bn ($12.7bn + $5.3bn contingent); Barclays says *"a maximum ~$17.1b."* The primary settlement document was not obtained. Any EPS bridge built off this page must pick a house and say which.**

### 6. 🔴 GS INITIATES CXMT AT BUY (TP Rmb129) — THE MOST CONCRETE DRAM-SUPPLY BEAR CASE THIS WIKI HAS, AND IT IS NOT IN ANY MEMORY-PAGE NUMBER

GS (Allen Chang +17, *"CHIPS IV"*, 08-24): CXMT capacity **more than doubles by 2030E vs 2026E to 665k wpm**; conventional DRAM supply reaches **41% / 50% of Samsung / SK hynix by 2028E, from 28% / 35% in 2025**; **50% of China DRAM demand captured by 2028E**. Also: China WFE **+13% / +20% / +15% y/y in 2026-28E**; China semis capex to **US$82bn in 2030E, raised 79%**; **domestic HBM3/3E targeted 4Q26**.

| Baseline | Status |
|---|---|
| (1) Prior wiki | CXMT tracked on `themes/china-export` as a policy object and a headline risk. **No capacity model, no rating, no target existed anywhere on this wiki.** |
| (2) House models | **No CXMT coverage. No China-DRAM supply line in any house memory model.** |
| (3) BBG | **CXMT is not in `estimates.json`. No consensus.** |

⚠️⚠️ **DELIBERATELY NOT FOLDED INTO MU / SAMSUNG / SKHYNIX THIS RUN, and the reason is a basis distinction the wiki keeps having to make: 41%/50% is CONVENTIONAL-DRAM SUPPLY share — not HBM, and not revenue or profit share. Dropping it into the 2027 pricing debate (UBS +90% blended Samsung HBM ASP vs JPM +42% industry, both open since 08-24) without that qualifier would manufacture a false contradiction of exactly the kind logged in the Korean-CY-sum and gross-vs-net episodes.** ➜ **OPEN ITEM for the next pass: does 665k wpm of Chinese conventional DRAM by 2030 change the conventional-DRAM scarcity rent that the HBM pricing debate implicitly assumes? Note the direction — it is the supply answer to the scarcity, and no memory page currently models it.** **The 4Q26 domestic HBM3/3E date is checkable THIS QUARTER.**

### 7. ⚠️ NVDA CAPITAL RETURN — UBS WAS RIGHT ON THE REASON, WRONG ON THE SIZE

| | Expected (UBS/Arcuri, 08-14) | Actual (Q2 FY27) |
|---|---|---|
| Buyback run-rate | step from "$20-22bn/qtr" to **"$40-45bn/qtr"** | **$20bn** |
| Dividend | — | $6bn ($0.25/sh) |
| Total returned | — | **$26bn (a record)** |
| Authorisation remaining | — | ~$99bn |
| FCF payout | ≥50% plan | **60% YTD**, *"net of strategic uses"* |

**Arcuri's stated reason for a hold-back (cash reserved for the SpaceX/financing deals) and his call that no new capital-return number would be announced were both right; only his magnitude was wrong.** ➜ **"Net of strategic uses" is the operative phrase given the ~$50bn already invested in the labs. There is no BBG consensus line for buyback pace.**

---

## ✅ CONFIRMS — no action

### 8. ✅ NVDA FQ3 REVENUE GUIDE IS ESSENTIALLY IN LINE WITH THE REFRESHED CONSENSUS
**Guide $108.0bn ±2% vs BBG 1FQ (Q3-26E) $107,193mn = +0.75%.** Inside the noise band. ⚠️ **Note the page's PRE-print Street mark was ~$104.5bn; BBG now reads $107.2bn, so consensus had already moved up ~2.6% before or immediately after the print. The "+3.3% vs Street" scoring on the NVDA page is against the pre-print vintage and both are correct on their own dates.** **`rev_hi` for the quarter is $138,694mn — the high estimate is 29% above the guide midpoint, so the dispersion is enormous and the median is doing a lot of work.**

### 9. ✅ MS TMT CREDIT HAD NVIDIA'S FINANCING ARCHITECTURE RIGHT TWO DAYS BEFORE THE COMPANY DESCRIBED IT
Lindsay Tyler's 08-24 initiation named the **~4.25GW PORTS-Pike shell RVG**, the **revenue-sharing / credit-support model** and the **>$500bn partnership** — all three confirmed on the 08-26 call, and her *">$500bn still in MOUs"* caveat confirmed verbatim by NVIDIA's own *"subject to definitive agreements."* ➜ **This raises the weight the page should give her ~$200bn all-in CY28 exposure forecast, which is currently the only quantified framework for it.** ⚠️ **NOT confirmed: her "up to 25%" residual-value-support percentage. NVIDIA gave no RVS number.**

### 10. ✅ ANET — MANAGEMENT'S AFFIRMED FY26 GUIDE SITS ~2% ABOVE CONSENSUS, AND THE SCALE-ACROSS SPLIT MATCHES THE PAGE
| | Figure |
|---|--:|
| Company FY26 revenue guide (affirmed 08-26) | **$12.6bn** |
| BBG CY2026 revenue | **$12,338.6mn** |
| **Gap** | **+2.1% in the company's favour** |
| Company GM guide | 62-64% · BBG CY2026 GM **62.8%** — in line |
| AI-fabric minimum, affirmed | **≥$3.5bn** |
| Scale-across at "a third of our AI business" | ⇒ **~$1.17bn** vs the ~$1.2bn already on the page from Susquehanna and MS/Accton ✅ |

**Management independently confirmed the ~⅓ figure, settling the FUNDA newsletter's $1.1bn/$3.6bn relay (08-12) in favour of the company framing.** **Also newly bounded: the 10%-customer count is *"one, maybe two more — it's NOT three more,"* with *"over a hundred AI customers"* behind it.**

### 11. ✅ THE 08-25 THE-INFORMATION REPORTING WAS CONFIRMED BY THE COMPANY
Groq 3 LPX in full production with **[[NBIS]] Nebius first**, and **[[SPCX]] SpaceXAI deploying Vera CPUs** — both reported 08-25 by The Information and both confirmed in NVIDIA's own release and call. The Artificial Analysis benchmark relay (~4x tokens/sec vs next best) is repeated by management.

### 12. ✅ SMTC — THE FINAL TRANSCRIPT RE-VERIFIED EVERY FOUNDING FIGURE, AND THE PAGE'S DECISION TO LEAVE A NUMBER BLANK WAS VINDICATED
All Q2 FY27 actuals reconciled against a clean text layer ($342m / $0.71 / 54.5% / segments summing exactly to $342m). **The founding pass had flagged an illegible figure as *"almost certainly a garbled 40%"*; the final transcript reads "well over 50%." The guess would have been wrong and the number was correctly left off the page.**
⚠️ **NO CONSENSUS BASELINE EXISTS: SMTC is ABSENT from `_wiki/_data/estimates.json`.** The Q3 FY27 guide (**$410m ±$5m, GM 58.3% ±100bp, EPS $1.05 ±$0.03 on ~99mn shares, adj EBITDA $134m ±$4m**) therefore **cannot be placed against the Street from this wiki.** ➤ **NAMED GAP — add SMTC to the BBG fetch list.**

### 13. ✅ WILLIAM BLAIR HOT CHIPS — RATINGS RECORDED, NO ESTIMATE CHANGES TO RECONCILE
**ARM Outperform (px $241.56) · AVGO Outperform ($356.74) · NVDA Outperform ($213.05) · GOOG Outperform ($343.34) · ALAB Outperform ($282.65) · AMD MARKET PERFORM ($479.18).** **No price targets and no estimate revisions are stated in the body**, so there is nothing to place against BBG. Context only: BBG CY2027 revenue — ARM $7,576mn, AMD $86,696mn, AVGO $190,561mn, GOOG $544,339mn.

---

## 🗄️ STALE MARKS QUARANTINED (older numbers that must not supersede newer ones)

| Note | Date | Marks | Why quarantined |
|---|---|---|---|
| Mizuho · Vijay Rakesh, *"The DC Storage Evolution"* | **2026-04-09** | MU **$545** (from $530), SNDK **$1,000** (from $710), STX **$565** (from $475), WDC **$400** (from $340); LRCX $295, MKSI $320 | 🔴 **The SAME analyst's MU target on this wiki is $1,375 as of 2026-08-09 — the April mark is 2.5x out of date.** Filed on SNDK.md as a dated backfill with an explicit non-supersede banner. Its **NAND contract pricing forecast of +81%/+20% q/q for 2Q-3Q26E** is a forecast for quarters now largely past — **left as an unperformed scorecard check, flagged as an open item.** |
| MS TMT Credit · Lindsay Tyler, AVGO/TPU leasing | **2026-05-29** | *"recent AVGO spread weakness presents a potential entry point"* | A spread view on a name that has reported twice since. Recorded as its own date's stance, **not carried forward as live.** |

---

## Open items carried forward

1. 🔴 **The NVDA house model needs a GM cut** (~100-200bp on 2027E) and a Vera-Rubin-weighted revenue/GW re-cut. **Neither was applied this run.**
2. 🔴 **The NVDA snapshot block is stale.** It carries CY2026E GM 75.0% (house) and CY2027E 74.0% (BBG) against BBG's now-74.4%/73.3% and management's 72-73% FY28. It is auto-generated by `_tools/build_snapshot.py` and will re-cut on the next refresh.
3. 🔴 **Every NVDA price target on the page is now PRE-PRINT** (MS OW $288 · BMO $340 · UBS $280 · BofA $350 · DB Hold $255 · Arete $283). A second pass is needed within days.
4. 🔴 **CXMT vs the memory pages' 2027 pricing debate** — see item 6. Not folded, deliberately.
5. ⚠️ **Add SMTC to the BBG fetch list** — no consensus exists for a name with a live page and a fresh guide.
6. ⚠️ **META headline-number discrepancy** ($18bn BofA vs $17.1bn Barclays) — resolve by obtaining the settlement document.
7. ⚠️ **Score Mizuho's April NAND contract-pricing forecast (+81%/+20% q/q for 2Q-3Q26E) against realised pricing** — a free, on-disk credibility test that was not run.
