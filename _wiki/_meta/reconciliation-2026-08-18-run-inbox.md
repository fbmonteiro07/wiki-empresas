# Reconciliation — 2026-08-18 (/run-inbox night run, 8 sources)

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus. Purely qualitative/technical material (the Irrational Analysis optics note) is out of scope by design and is not tabled below._

⚠️ **BBG BASIS — READ THIS BEFORE USING THE THIRD COLUMN.** A **live** `bdp` pull failed at 23:5x with `ConnectionError: blpapi: could not start session (Terminal not running / logged out?)` — the Terminal is logged out at this hour, as expected for a night run. **Rather than mark the column PENDING, this report uses the on-disk BBG consensus in `_wiki/_data/estimates.json`, `asof 2026-08-18`** — i.e. genuine Bloomberg data pulled by *today's* earlier `/wiki-consensus` refresh (commit `fa64193c`), not a web substitute. **No live re-pull is required for this report to stand.** Two standing caveats apply and are honoured throughout:
- **`CY2026` sums embed PRE-PRINT consensus for quarters already reported** — CY2026 comparisons are directional only; **CY2027 is the clean column** and carries the weight below.
- **Fiscal-vs-calendar mismatches are flagged explicitly, never netted.** [[MU]] (Aug FY), [[AVGO]] (Oct FY) and [[SNDK]] (Jun FY) are all off-calendar; BBG's CY columns are calendar. Where a broker's FY and BBG's CY are compared, the row says so and the gap is treated as indicative, not as a disagreement.
- **BBG prices in `estimates.json` are the refresh snapshot** (AVGO $380.00, MU $940.76, SNDK $1,625.78, Samsung KRW263,500, SK hynix KRW1,621,000, Kioxia ¥57,150) and differ from the prices printed in the notes (AVGO $392.43 on 08/17, MU $1,011.75 on 08/17, Samsung KRW230,500 on 08/06). **Implied upside percentages below use the BBG snapshot price so that all names are on one basis.**

---

## Where the new data DIVERGES

### ① 🔴🔴 AVGO — our house FY28 AI number ($251bn) is **+22.3% above the Street-HIGH sell-side note** and **+49% above the Street**. The entire house edge in this name lives in FY28, not FY27
| Baseline | FY28 AI semi revenue | FY28 EPS |
|---|--:|--:|
| Capstone house | **$251bn** | **$35.96** |
| Wells Fargo (Rakers, 08-18) — Street-high | $205.3bn | $29.00 |
| Bloomberg (via JPM buyside survey, 08-11) | $229bn | $25.69 |
| Street / VisibleAlpha (per the note) | $168.2bn | $26.18 |
| **House vs Wells** | **+22.3%** | **+24.0%** |

The revenue and EPS gaps are the same size and the same direction, so this is **one bet expressed twice, not two findings**. What sharpens it is the FY27 comparison directly below in CONFIRMS: house $21.07, Wells $21.70 and BBG CY2027 $21.28 sit inside a ±2% band. **We are AT consensus for FY27 and alone in the world for FY28.**
➜ **Action: bridge the FY28 house numbers against Wells' published ladder (11.4GW × $13.2bn blended) BEFORE the 2026-09-02 print, and state explicitly whether the house edge is GW or $/GW. Wells' own note concedes the independent Epoch-implied rate is ~$11bn/GW; if the house is at Wells' GW and a higher rate, that assumption is the whole position and should be defended in writing rather than carried implicitly.**

### ② 🔴🔴 GOOG — Wells' TPU fleet (8.2GW in 2028) is **smaller than Barclays' EXTERNAL-only TPU-aaS capacity (11.5GW)** already on the page. Both cannot be right
| Baseline | 2026 | 2027 | 2028 |
|---|--:|--:|--:|
| Wells / Gawrelski (08-18) — **whole Google TPU fleet, EoP GW** | 4.8 | 6.3 | 8.2 |
| Barclays / Sandler (07-24) — **EXTERNAL, off-GCP TPU-aaS only** | 1.4 | 3.7 | **11.5** |

Barclays' external-only 2028 figure exceeds Wells' entire fleet by ~40%. The likeliest resolution is definitional — capacity Google **OWNS** versus capacity Google **SELLS** (SPV-owned racks it does not operate) — but **neither note states which it is measuring**, and the distinction is exactly the axis the TPU-aaS margin debate turns on.
➜ **Action: until this is pinned down, treat every GW-based sizing of Google's TPU economics on this wiki as unsafe, including the TPU-aaS unit economics. It is cheap to resolve at the next disclosure and it is the highest-value open question of the run.**

### ③ 🔴 GOOG — Wells' $811bn purchase-commitment figure **fails its own arithmetic**; the wiki's primary-sourced $707.0bn stands
| Baseline | 1Q26 | 2Q26 |
|---|--:|--:|
| **Capstone 10-Q diff (07-23) — PRIMARY, retained** | $232.7bn | **$707.0bn** |
| Wells Fargo (08-18) — headline | $332.4bn | $811bn |
| Wells Fargo — its own stated components (LT $610.3bn + ST $63bn) | — | **$673.3bn** |

The note's sentence contradicts itself twice: the components sum to $673.3bn rather than $811bn, and short-term is described as "growing" to $63bn **from $138bn**, which is a fall. Our filing-derived figure sits **between** the note's component sum and its headline.
➜ **Action: none on the number — the wiki figure stands. Carry the lesson instead: this line is now large enough that a ~$100bn discrepancy passes unnoticed through a published note, so purchase commitments must be taken from the filing every quarter and never from a broker restatement.**

### ④ 🔴🔴 CROSS-THEME — memory alone at **$1.61tn of 2027 revenue** does not fit inside **$5.8tn of six-year hyperscaler capex**
| Source | Figure | Period |
|---|--:|---|
| UBS / Gaudois (08-07) — memory industry revenue | **~US$1.61 TRILLION** | 2027E, **one year** |
| Goldman Sachs Credit Strategy / Lynam (07-09) — five-hyperscaler AI capex | **US$5.8 TRILLION** | FY2025–FY2030, **six years** |

A single component category running $1.6tn in one year cannot be accommodated by any capex-composition model currently on this wiki.
➜ **Action: size where that memory revenue is actually SOLD. Three resolutions with opposite trade implications — (a) memory forecasts are too high (bearish MU/SAMSUNG/SKHYNIX/SNDK); (b) hyperscaler capex is too low (bullish the complex); (c) memory sells far beyond the five hyperscalers into sovereign, neocloud, enterprise and on-device demand, which would make memory structurally LESS hyperscaler-dependent than the wiki assumes. Not resolvable from either note; logged on both theme pages.**

### ⑤ ✅ RESOLVED 2026-08-19 → CONFIRMS — SAMSUNG — both new houses are **BELOW BBG on 2027 EPS** while both claim to be **ABOVE consensus on operating profit**
| Baseline | 2026E EPS (KRW) | 2027E EPS (KRW) |
|---|--:|--:|
| BBG consensus (`estimates.json`, asof 08-18) | 46,404 | **75,198** |
| UBS / Gaudois (08-07) | 43,532 (**−6.2%**) | 73,903 (**−1.7%**) |
| KB Securities / Jeff Kim (08-10) | 46,237 (−0.4%) | 69,200 (**−8.0%**) |
| UBS's OWN printed "Cons." for 12/27E | — | **69,649** |

UBS states it is "16% above '27E consensus OP" and KB "+4.8%" above consensus OP — yet both sit below BBG on EPS. **The reconciliation is a consensus-SOURCE gap: UBS's own consensus compile (69,649) is ~8% below BBG's (75,198) for the same year.** A second possible contributor is the OP-versus-EPS basis (non-operating items, tax, the preferred-share structure).
➜ **Action: "X% above consensus" claims on Samsung are NOT comparable across houses this quarter, nor to our BBG snapshot. Any Korean-memory screen must state which consensus it uses or it is measuring vendor methodology. Re-run this row against a LIVE `BEST_EPS` 12/27E pull once the Terminal is up to separate a vendor artefact from a stale on-disk figure.**

✅ **08-19 resolution (live BBG pull) — the row's stated divergence is FALSIFIED, and the cause is a defect in OUR consensus baseline, not vendor methodology. Moved to CONFIRMS.**

Pulled live 2026-08-19 on `005930 KS Equity`, `BEST_EPS` with `BEST_FPERIOD_OVERRIDE=2FY` (= 12/27E, Samsung is a Dec year-end), i.e. **Bloomberg's own annual consensus line** rather than our calendar-year sum-of-quarters:

| Mark for 12/27E EPS (KRW) | Value | vs BBG **annual line** 70,400 |
|---|--:|--:|
| **BBG annual line — live 08-19 (`BEST_EPS` 2FY)** | **70,400** | — |
| UBS's own printed "Cons." | 69,649 | **-1.1%** |
| UBS / Gaudois (08-07) | 73,903 | **+5.0% ABOVE** |
| KB Securities / Jeff Kim (08-10) | 69,200 | -1.7% |
| _our `estimates.json` CY2027 sum-of-quarters_ | _75,198_ | _**+6.8%** - the outlier is OURS_ |

**The ~8% "UBS-vs-BBG" spread was never a vendor-compile gap.** UBS's compile (69,649) sits **within 1.1%** of Bloomberg's own annual line. The gap was between UBS and **our aggregate**, which runs +6.8% hot on this name. Two consequences, and the second is bigger than the original row:

1. **The row's claim inverts.** UBS is **+5.0% ABOVE** consensus on 12/27E EPS, not -1.7% below — so UBS's "16% above '27E consensus OP" is *consistent* with its EPS after all, and the paradox the row was built on disappears. KB remains marginally below (-1.7%), which is noise. ➜ **Moved to CONFIRMS: the houses and Bloomberg agree on Samsung 2027 EPS once compared on the same basis.**
2. 🔴 **A new baseline defect, logged as method flag 8 below** — and it lands on the column the wiki treats as clean.

➜ **Action retired.** Any Samsung EPS comparison must use `BEST_EPS` 2FY, not the page's CY2027 cell.

### ⑥ 🔴 AVGO — the Street-high forecast and a BELOW-consensus forecast differ by **one unobservable assumption on identical volumes**
| $/GW assumption | Source | Implied FY27 AI revenue on Wells' 7.581GW ladder |
|---|---|--:|
| $13.5bn blended | **Wells Fargo's choice** | **$141.5bn** (Street-high) |
| ~$11bn implied | **Epoch AI data, cited inside the same note** | **~$110bn** (BELOW the $118.8bn Street) |
| $10–20bn band | Broadcom management's own stated range | — |

The note contains its own refutation: it reports the independent implied rate and then models ~23% above it.
➜ **Action: $/GW is now the dominant variable in every custom-ASIC forecast on this wiki and the range in active use spans ~2×. REJECT any GW-based ASIC number quoted without its $/GW rate. Standing unit rule re-applied: these are CONTENT-per-GW figures and must never be netted against project-DEBT-per-GW ($34.5bn ÷ >1GW) or build-cost-per-GW anchors.**

### ⑦ 🔴 SKHYNIX — two houses now hand the 2027 HBM bit-share lead to Samsung, but the mechanism weakens the claim
| Baseline | Samsung | SK hynix | Micron |
|---|--:|--:|--:|
| UBS (08-07) — 2027 HBM **bit** supply share | **40%** | 38% | 22% |
| KB Securities (08-10) — 2027 **HBM4** share | **44% ("largest")** | — | — |
| Prior wiki position | SK hynix leadership carried as structural | | |

Two independent houses, two different share metrics, same reversal — that is a consensus forming rather than one house's view. **But UBS reaches Samsung 40% while simultaneously CUTTING Samsung's own 2027 HBM bits from 24bn to 22bn Gb**, so the share gain is partly a denominator effect: it implies UBS cut the rest of the industry harder than Samsung.
➜ **Action: the falsifiable claim is "SK Hynix ships LESS than currently modelled in 2027" — NOT "Samsung ships more." That is checkable against SK Hynix's own capacity disclosures and is the cleanest test this theme can run in the next two quarters.**

### ⑧ ✅ RESOLVED 2026-08-19 → CONFIRMS — MU — management's mid-$40bn FY27 capex is ~14% below BBG's CY2027, but the periods do not line up
| Baseline | Capex | Period |
|---|--:|---|
| Management via UBS (08-17) — reiterated | **mid-$40bn** | **FY27, ending Aug-2027** |
| BBG consensus (`estimates.json`) | $52.2bn | **CY2027** |

➜ **Action: DO NOT score this as a disagreement without adjusting the period — MU's FY27 contains only ~2/3 of CY2027 and capex is ramping, so the fiscal figure is mechanically lower. The real question the gap raises is whether consensus is front-running a capacity ramp management describes as C2028-weighted (ID1 + Tongluo brownfield mid-C2027; Tongluo greenfield, ID2 and Hiroshima F15 in C2028). If the ramp is genuinely C2028-weighted, CY2027 consensus capex is EARLY rather than wrong. Re-check against a fiscal-basis consensus before acting.**

✅ **08-19 resolution (live BBG pull) — the gap was ENTIRELY the period mismatch, exactly as the row hypothesised. Moved to CONFIRMS — and the residual risk flips to the opposite year.**

Pulled live 2026-08-19 on `MU US Equity` with `BEST_FPERIOD_OVERRIDE` on a **fiscal** basis (MU is an Aug year-end, so 2FY = FY2027 ending Aug-2027 — the exact period management guided):

| Period | BBG consensus capex | y/y | Management |
|---|--:|--:|---|
| FY2026 (1FY, ends Aug-26) | $28.0bn | — | — |
| **FY2027 (2FY, ends Aug-27)** | **$45.0bn** | **+60.8%** | **"mid-$40bn"** ✅ |
| FY2028 (3FY, ends Aug-28) | $48.5bn | **+7.6%** | — |
| _(for reference) CY2027 — our page's cell_ | _$52.2bn_ | — | _not the guided period_ |

**Management's mid-$40bn and consensus FY27 of $45.0bn are the same number.** The ~14% "shortfall" was the Aug-FY vs calendar-year mismatch and nothing else — do not carry it as a disagreement. ➜ **Moved to CONFIRMS.**

🔴 **But the row's own open question now resolves against the other year.** It asked whether CY2027 consensus was front-running a ramp management describes as C2028-weighted (ID1 + Tongluo brownfield mid-C2027; Tongluo greenfield, ID2 and Hiroshima F15 in C2028). On a fiscal basis consensus puts **the entire step-up in FY27 (+60.8%) and then goes nearly flat in FY28 (+7.6%)**. If management's ramp really is C2028-weighted, the exposure is **consensus FY2028 capex being too LOW, not FY2027 being too high** — the inverse of the concern as written. On MU's own disclosed schedule, three of the five named nodes land in C2028 against a +7.6% consensus capex step.
➜ **Action: test FY28, not FY27. Watch for an FY28 capex guide above ~$48.5bn at the Sept print — that is the falsifiable version of this row.** _(MU's CY2027 GM and EPS did not move at all 08-18 → 08-19: 86.0% / $163.61.)_

### ⑨ ⚠️ MEDIATEK — a named house now contests the part-level attribution the DC-ASIC sizing rests on
| Baseline | TPU v8t | TPU v8i |
|---|---|---|
| Wiki working map (Barclays; Jeff Pu; @jukan05) | MediaTek (~$10bn CY27) | **AVGO** ("volume node", >$60bn CY27) |
| Wells Fargo (08-18) | **AVGO** | **AVGO** — "we believe both are Broadcom, vs reports that TPU v8i is MediaTek" |

Wells asserts a belief with no check, writing from the incumbent's side, and does **not** dispute MediaTek's second-source role in general — the same note calls it "a primary focus" and flags reports of AMD involvement in TPU v10.
➜ **Action: part attribution is now an ASSUMPTION rather than a given. Anyone sizing MediaTek's 2027 DC-ASIC revenue off a specific part number must say so explicitly. Resolvable at the next TPU disclosure; kept as an open contest on the MEDIATEK page, not a correction.**

## ✅ CONFIRMS — no action

| # | Datapoint (source) | Baseline agreement | Note |
|---|---|---|---|
| **1** | **[[AVGO]] FY27 EPS $21.70** (Wells Fargo, 08-18) | House **$21.07** · BBG CY2027 **$21.28** · Wells vs BBG **+2.0%**, house vs BBG **−1.0%** | ✅ **Three independent marks inside a ±2% band on FY27 EPS. Our model is effectively AT consensus for FY27 — which sharpens Diverges #1/#2: this name's entire house edge is FY28, not FY27.** |
| **2** | **[[AVGO]] FY27 AI semi revenue — house $132bn vs Street $118.8bn** | Wells' $141.5bn now sits **+7.2% above the house**, and the house is **+11.1% above the Street** | ✅🔴 **A SECOND HOUSE HAS ARRIVED ON THE SAME SIDE OF OUR FY27 AI CALL, AND ABOVE IT. The house view (AI FY27 materially above Street) gains an independent, published, above-consensus corroborator for the first time. The house is no longer the outlier on FY27 — it is now the MIDDLE of a three-point distribution.** |
| **3** | **[[SNDK]] NBM coverage 50% FY27 → ~66% FY28** (Citi corrected reissue, 08-18) | Wiki DISPUTE #3 (08-14) refused Citi's FY26/FY27 framing against the Investor Day deck; **BofA, SIG, JPM and Bernstein all said FY27/FY28** | ✅🔴 **THE DISPUTE IS CLOSED IN THE WIKI'S FAVOUR. Citi silently reissued the note with the fiscal years corrected to the page's figures — a full-text diff finds exactly two changes, this one and a capitalisation fix. No estimate, rating or PT moved. The refuse-and-log discipline is validated; nothing to change on the page beyond recording the resolution.** |
| **4** | **[[MU]] SCA split ~40% priced-framework / ~10% take-or-pay / ~50% market** (UBS · Arcuri, 08-17) | **Micron IR (Satish) gave the page the same three tranches on 07-27** | ✅ **Second-source confirmation of a management disclosure. The genuinely NET-NEW increment is smaller and was recorded as such: the ~40-point priced tranche is itself split between FIXED-price and ceiling+floor BANDED contracts, unsized by either source — now the largest unquantified input in the SCA structure, ahead of the floor GM level.** |
| **5** | **[[MU]] fulfilling <50% of DC customers' requested volumes** (UBS, 08-17) | KeyBanc fireside 08-10 (*"not able to meet any more than half of the demand"*); Kioxia's own 40–50% fill rate (08-17); KB Securities' *"only 60% of big techs' memory demand is being met"* (08-10) | ✅ **Fourth independent restatement, now from three different suppliers. The fill-rate constraint is the best-corroborated fact in memory right now and needs no further verification.** |
| **6** | **HBM 2027 repricing is a CATCH-UP to conventional DRAM, not an independent AI-demand event** (Bernstein 07-20 predicted it; Micron management confirmed the mechanism to UBS on 08-17) | Bernstein: HBM +2.0–2.5× vs conventional already +4× and possibly +5× · UBS: 2027 HBM ASP **+90% y/y (raised from +68%)** — inside Bernstein's band at the low end | ✅ **An outside-in prediction and an inside-out confirmation matching a month apart, with a third house's ASP revision landing inside the predicted range. Best-supported pricing claim on the memory theme.** ➤ **The implication is a CEILING, not upside: if HBM is catching up to what conventional already achieved, conventional's realised increase bounds how bullish HBM ASPs can get.** |
| **7** | **[[NVDA]] Rubin Ultra de-spec, with HBM PROCUREMENT still going up** (UBS, 08-07: *"could be de-specing Rubin Ultra. Yet, on higher GPU SiP estimates, we slightly INCREASE Nvidia HBM procurement estimates for '27"*) | Third venue for the de-spec; **confirms the DIRECTION of the correction the 08-17 run made on [[MU]]/[[NVDA]]** after a relay had inverted the sign | ✅🔴 **Important because it validates a prior correction rather than a prior claim: content per GPU steps DOWN while total procurement steps UP on higher SiP count. Anyone reading the de-spec as an NVDA demand signal has the sign backwards.** |
| **8** | **[[SAMSUNG]] shareholder return step to ~KRW100–215tn** (KB 08-10: expects an announced KRW100–200tn, up >10× from KRW9.8tn · UBS 08-07: 50%-of-FCF-ex-M&A policy on FCF of KRW248tn/450tn ⇒ ~KRW108tn 2026E / ~KRW215tn 2027E) | Two houses, two independent METHODS — one an expected announcement, one a formula | ✅ **UBS's formula-derived figure lands at the midpoint of KB's expectation range. Strongest form the Samsung return thesis has taken on the page.** |
| **9** | **[[SAMSUNG]] KB 3Q26E OP KRW112tn, DRAM OPM 83%, NAND OPM 71%, 60% fill rate, 3y→5y LTAs, 44% HBM4 share** (KB primary, 08-10) | The 08-11 Jefferies-desk RELAY of this note, already on the page | ✅ **Every quantitative claim in the relay held verbatim against the primary — notable because the standing wiki finding is that relays distort (units inverted, ranges compressed, Q&A dropped). The only correction was the HOUSE: produced by KB Securities, merely distributed by Jefferies.** |
| **10** | **PT marks — implied upside on the BBG snapshot price** | [[AVGO]] Wells $545 = **+43.4%** (px $380.00) · [[MU]] UBS $1,625 = **+72.7%** (px $940.76) · [[SNDK]] Citi $2,100 = **+29.2%**, Bernstein $3,000 = **+84.5%** (px $1,625.78) · [[SAMSUNG]] UBS KRW535k = **+103.0%**, KB KRW600k = **+127.7%**, Bernstein KRW440k = **+67.0%** (px KRW263,500) · [[SKHYNIX]] Bernstein KRW3.3m = **+103.6%** · [[KIOXIA]] Bernstein ¥40,000 = **−30.0%** (px ¥57,150) | ✅ **No PT in this run is a new Street high or low on any page, and only ONE rating/PT action occurred: UBS's Samsung cut (550k → 535k), retired to that page's Changelog.** ⚠️ **The Bernstein marks (07-20) were each checked against the pages and NONE is a change — all match marks already logged, so they are historical corroboration, not rating actions.** ⚠️ **Note the shape of the memory book: implied upside of +67% to +128% on the Korean names and −30% on Kioxia, from the SAME house on the SAME day. Bernstein's US and Asia teams are explicitly split on NAND — the US team long [[SNDK]] at $3,000, the Asia team short [[KIOXIA]] at ¥40,000 — on a stated view about whether AI demand accrues to DRAM or NAND. That is a thesis gap, not a valuation gap, and it is the cleanest expression of the NAND debate available.** |
| **11** | **[[GOOG]] RPO $514bn exiting 2Q26** (Wells Fargo, 08-18) | Page already carries **$514B backlog** from the print | ✅ **Exact match. Worth noting given that the same note's purchase-commitment figure (Diverges #3) does not tie — the RPO line is clean, so the failure there is specific rather than systemic.** |
| **12** | **[[GOOG]] house 2027 revenue $641bn vs BBG CY2027 $544.4bn (+17.8%)** | Pre-existing house position, not new tonight | ⚠️ **Not a finding from this run — surfaced only because tonight's GOOG patch touched the page. Recorded so the standing gap stays visible: the house is +17.8% above consensus on 2027 revenue while at $16.20 vs $16.50 on EPS, i.e. materially above on the top line and slightly BELOW on the bottom line. That combination implies a much heavier cost/depreciation assumption than consensus and is worth an explicit note the next time the GOOG model is revisited.** |

---

## Follow-ups this report generates

1. **Bridge the [[AVGO]] FY28 house numbers** ($251bn AI / $35.96 EPS) against Wells' 11.4GW × $13.2bn ladder — state whether the house edge is GW or $/GW, before the 09-02 print. *(Diverges #1, #2, #8.)*
2. **Resolve the Google TPU GW definition** — owned vs sold capacity — which reconciles Wells' 8.2GW fleet with Barclays' 11.5GW external-only. *(Diverges #4.)*
3. **Size where the $1.61tn of 2027 memory revenue is actually sold** — inside or outside the five hyperscalers. *(Diverges #5.)*
4. ~~**Re-run this reconciliation's [[SAMSUNG]] rows against a LIVE BBG pull**, specifically `BEST_EPS` 12/27E.~~ ✅ **DONE 2026-08-19 — it is NEITHER a vendor artefact nor a stale figure: it is our own CY sum-of-quarters running +6.8% hot. Row ⑤ moved to CONFIRMS; the defect is now method flag 8.**
5. ~~**Check MU's fiscal-2027 capex against a fiscal-basis consensus.**~~ ✅ **DONE 2026-08-19 — fiscal FY27 consensus $45.0bn vs management mid-$40bn: they agree. Row ⑧ moved to CONFIRMS, and the open risk moved to FY2028 (+7.6% consensus step against three of five named nodes).**

---

## Method flag added by the 2026-08-19 consensus refresh

8. 🔴 **The "CY2027 is the clean column" rule has a carve-out: EPS on the Korean names.** Method flag 7 (from 2026-08-01) established that every `estimates.json` **CY2026** line understates a beat, because our CY aggregate re-pulls already-reported quarters via `BEST_FPERIOD_OVERRIDE` and `BEST_*` on a past fiscal period returns pre-print consensus. **CY2027 was exempted on the grounds that `n_actual=0` for all names** — no reported quarters, nothing to misprice. That exemption is **not sufficient for EPS**. Tested live 2026-08-19, our CY2027 sum-of-quarters against Bloomberg's own annual line (`BEST_EPS`/`BEST_SALES` 2FY) on calendar-year-end names:

| Ticker (Dec FY-end) | our CY2027 EPS | BBG annual line | EPS gap | rev gap |
|---|--:|--:|--:|--:|
| GOOG | $16.50 | $16.52 | **-0.1%** | +0.5% |
| NVDA | $12.95 | $12.96 | **-0.1%** | +0.8% |
| TER | $11.16 | $11.45 | -2.6% | -0.7% |
| **SAMSUNG** | KRW 75,198 | KRW 70,400 | 🔴 **+6.8%** | +1.6% |
| **SKHYNIX** | KRW 566,381 | KRW 471,650 | 🔴 **+20.1%** | +1.0% |

**Revenue ties everywhere (≤1.6%); EPS breaks only on the two Korean names.** That rules out a period mismatch and points at contributor depth: many houses publish quarterly *revenue* for Samsung / SK hynix, far fewer publish quarterly *EPS*, so the four-quarter EPS sum is built from a thin and evidently more bullish contributor set than Bloomberg's annual compile. The mechanism is inferred, not confirmed — **the measured effect is what matters, and on SKHYNIX it is +20%.**

➜ **Rule: for SAMSUNG and SKHYNIX, take EPS from a live `BEST_EPS` 2FY/3FY pull, never from the page's CY cell. Off-calendar names (MU Aug, AVGO Oct, SNDK/KLAC Jun) were already excluded from CY-vs-FY comparison and are unaffected by this flag** — their gaps in the same test (+8.0%, +10.2%, -7.7%, -7.5%) are the expected fiscal offset, not this defect.

_BBG column resolved 2026-08-19 — `estimates.json` asof **2026-08-19** (98/98 live, 0 FAIL lines, 0 null prices, 0 `error` keys, 0 carry-over `revisions` stamps, no stale top-level provenance keys). **One record byte-identical to the 08-18 vintage — VST** — investigated and cleared: `140.52` is exactly VST's **08-18 official close**, the fetch log shows a normal live read at 31/98 (not an exception carry-over), and a re-probe during this run returned `140.06` / `139.99`, so the name is trading today. ⚠️ **VST's `px` in this vintage is therefore yesterday's close — any VST upside calculation off this file is ~0.4% stale.** Plus two ad-hoc live pulls: `BEST_EPS` 1FY/2FY on Samsung, and fiscal `BEST_CAPEX` / `BEST_EPS` / `BEST_GROSS_MARGIN` 1FY-3FY on MU. **Two rows moved DIVERGES → CONFIRMS (⑤ SAMSUNG, ⑧ MU)**; no row moved the other way. Canonical header `## Where the new data DIVERGES` applied (was `## Where the new data DIVERGES (the alpha)`). **No web data was substituted at any point.**_

⚠️ **Prices in this report's CONFIRMS #10 upside table are now stale** — spot fell again 08-18 → 08-19 on every memory name: [[KIOXIA]] ¥57,150 → **¥49,950 (-12.6%)**, [[AVGO]] $380.00 → **$360.85 (-5.0%)**, [[SAMSUNG]] KRW263,500 → **KRW257,500 (-2.3%)**, [[SNDK]] $1,625.78 → **$1,594.23 (-1.9%)**, [[MU]] $940.76 → **$932.44 (-0.9%)**; [[SKHYNIX]] was the one gainer, KRW1,621,000 → KRW1,624,000. **Every implied-upside figure in that table is now understated, and Bernstein's ¥40,000 Kioxia short has gone from -30.0% to -19.9% implied downside in one session.** Estimates did not move on any of these names — this is price, not revision.
