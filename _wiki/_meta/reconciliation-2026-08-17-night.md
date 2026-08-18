# Reconciliation — 2026-08-17 (night, /run-inbox scheduled)

_Variance pass on every NEW quantitative datapoint from tonight's 12 sources, against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus. Written after the patches landed (37 files: 29 company pages + 8 theme dossiers)._

**Sources reconciled:** LITE FY2026 Form 10-K (company primary, filed 08-17) · Fabrinet Q4 FY26 earnings call (company primary, 08-17, Bloomberg INITIAL DRAFT) · Mizuho / Vijay Rakesh AI Server Call 08-16 · Morgan Stanley / Erik Woodring Global IT Hardware 08-10 · Irrational Analysis on COHR 08-13 · Irrational Analysis transceiver-ban memo 08-04 · FUNDA Deep|Optics 08-12 · FUNDA FMS-2026 08-11 · Deutsche Bank / Edison Yu SpaceX 08-17 · Epoch AI / Campbell Hutcheson 08-12 · Hugging Face State of Open Models 08-14 · Goldman Sachs US Weekly Kickstart 08-14.

## Baseline status

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Done (on disk). Every patch agent ran an explicit before-insert read; the collisions are itemised below. |
| **2. Capstone house models** | ✅ Done — coverage is thin for tonight's names. `_data/house.json` (asof 2026-08-17) holds **AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM**. Of tonight's newly-marked names only **LITE, AVGO, NVDA, META, GOOG** have a house model. **DELL, HPE, STX, SPCX, SNDK, MU, AMD, INTC, CRDO, MEDIATEK, KIOXIA, MRVL, ALAB, MCHP, AAOI, AXTI, TSEM, CIEN, ANET, CSCO have no house model** — reconciled vs wiki + BBG only. |
| **3. BBG consensus — LIVE** | 🔴 **PENDING.** Live `bdp` against `E:\bloomberg_api` raised `ConnectionError: blpapi: could not start session` at **23:40** (three failed connects to 127.0.0.1:8194, `PlatformController` gave up) — Terminal not running / logged out at that hour. **No web data was substituted at any point.** The one column this costs us is **consensus target price / rating**, which is not in the on-disk snapshot. |
| **3b. BBG consensus — ON-DISK SNAPSHOT** | ✅ **Used, and it is NOT stale: `_wiki/_data/estimates.json` is `asof 2026-08-17`, written at 18:29 tonight** by today's `/wiki-consensus` run (98/98 names). So the EPS / revenue / capex consensus columns below are same-day, not a carry-over. ✅ **Integrity spot-check passed: the snapshot's `LITE.actual.rev` = 3014.0 matches the FY26 10-K's $3,014.0m to the decimal**, which independently validates the actuals side of the snapshot against a filing that landed after it was written. ⚠️ Standing caveat applies: **CY2026 sums embed pre-print consensus for already-reported quarters — CY2027 is the clean column and is what is used below.** ⚠️ **CY2028 is absent for every name**, so DB's SPCX 2028E and Mizuho's 2028E marks have no consensus counterpart. |

**Action required:** log in to the Bloomberg Terminal / reconnect the Capstone VPN and re-run `/wiki-consensus` to resolve the **consensus PT + rating** column, priority rows **DELL** (item ①) and **SPCX** (item ③).

---

## New price targets vs spot and vs consensus CY2027 EPS

_Spot and consensus EPS both from the 18:29 on-disk snapshot, so the implied multiples are internally consistent. Consensus PT column PENDING (see above)._

| Ticker | Spot | New PT | Upside | Cons CY27 EPS | PT on CY27 | Action | Note |
|---|--:|--:|--:|--:|--:|---|---|
| **SPCX** | 146.23 | **235** (DB) | **+60.7%** | 1.66 | 141.6x | reiterated | ③ — EPS basis unresolved; multiple is meaningless until it is |
| **MU** | 1011.75 | **1375** (Mizuho) | **+35.9%** | 163.61 | 8.4x | **reiteration** of 07-11 | ✅ no drift |
| **AVGO** | 392.43 | **530** (Mizuho) | **+35.1%** | 21.28 | 24.9x | reiterated | ⑤ |
| **NVDA** | 225.01 | **300** (Mizuho) | **+33.3%** | 12.93 | 23.2x | **reiteration** of 07-11 | ✅ CONFIRMS — sits on the consensus PT of **$303.71** from the live 08-17 pull recorded in `reconciliation-2026-08-15.md` |
| **HPE** | 57.61 | **69** (MS) | **+19.8%** | 4.10 | 16.8x | **UPGRADE EW→OW, PT $71→$69** | ④ — PT falls on an upgrade |
| **LITE** | 968.90 | **1140** (Mizuho) | **+17.7%** | 27.95 | 40.8x | reiterated | ② |
| **AMD** | 506.00 | **580** (Mizuho) | **+14.6%** | 15.30 | 37.9x | **CUT from $615, UNEXPLAINED** | ⑦ |
| **SNDK** | 1786.85 | **1900** (Mizuho) | **+6.3%** | 238.25 | 8.0x | **CUT from $2,200** | ⑧ |
| **INTC** | 103.49 | **109** (Mizuho) | **+5.3%** | 2.02 | 54.0x | **reiteration** | ⑥ — retroactively firms the un-rationalised 08-09 cut from $135 |
| **DELL** | 479.81 | **500** (Mizuho) | **+4.2%** | 22.48 | 22.2x | reiterated (was $350) | ① |
| **STX** | 994.79 | *no new PT* | (+4.0% on standing $1,035) | 45.50 | 22.7x | **Top Pick reiterated, PT not restated** | ✅ absence of a PT correctly not read as a change |
| **CRDO** | 282.82 | **290** (Mizuho) | **+2.5%** | 8.77 | 33.1x | **reiteration** | ⑨ — one source, not two |
| **DELL** | 479.81 | **430** (MS) | **−10.4%** | 22.48 | 19.1x | EW held, **PT $477→$430** | ① — **the target is BELOW spot** |

---

## DIVERGES — the alpha

### ① 🔴🔴 DELL — Morgan Stanley is **+27.5% above consensus on EPS** and its price target is **10.4% BELOW spot**. Both houses raised the numbers and neither will pay for them.

| Mark | Value | vs consensus CY2027 EPS $22.48 |
|---|--:|--:|
| MS **new** FY28 EPS (08-10) | **$28.66** | **+27.5%** |
| MS **old** FY28 EPS | $23.83 | +6.0% |
| SIG FY28 EPS (on page) | $24.23 | +7.8% |
| BofA FY27E EPS (on page) | ~$19 | −15.5% |

MS raised FY28 EPS **+20%** ($23.83 → $28.66) and simultaneously cut the target multiple **20x → 15x**, netting a **−9.9% PT ($477 → $430)** — a target that now sits **10.4% below the $479.81 spot**. Mizuho's $500, struck six days later, is **+4.2%**. **So the two houses that just told us Dell's earnings revisions go higher are jointly marking the stock at −10% to +4%.** Woodring says it outright: Dell "will see significant positive earnings revisions in the months ahead… but at 16x our new FY28 EPS, we believe valuation largely reflects this strength."

**The edge:** this is a pure multiple call dressed as a rating. If MS's own $28.66 is right and the multiple merely holds at the 19.1x that spot implies, the stock is worth ~$547; at MS's old 20x it is ~$573. **Consensus EPS has ~27% of catch-up to do to reach a number MS has already published**, and DELL has no house model to arbitrate. ⚠️ Note the opposing supply-chain check already on the page: Fubon (08-11) has SPCX/CRWV going **direct to ODMs at VR200**, i.e. a bigger rack pie but possibly a smaller Dell slice of the marginal rack.
**PENDING:** the consensus PT would settle whether $430 is genuinely below-Street or merely below-spot.

### ② 🔴 LITE — the first FILED full-year OCS number, and the ramp is **already guided**, not merely relayed. Skepticism moves off the relays and onto the $400m.

The FY26 10-K discloses **OCS revenue of more than $90.0m for fiscal 2026** — the first filed full-year figure, superseding the standing framing that the 10-Q's ">$25.0m Mar-26 quarter ≈ $100m annualized" was the only filed anchor.

🔴 **The 10-Q carries a second figure that makes the shape exact rather than bounded: ">$38.0m for the nine months".** Therefore:

| Period | Derivation | Value |
|---|---|--:|
| Q1+Q2 FY26 | 9M >$38.0m − Q3 >$25.0m | **≈$13m combined** |
| Q3 FY26 (Mar-26) | filed | **>$25.0m** |
| Q4 FY26 (Jun-26) | FY >$90.0m − 9M >$38.0m | **≈$52m** |
| FY26 total | filed | **>$90.0m** (13+25+52 = 90 ✓) |

**≈58% of the year's OCS revenue landed in the final quarter, so the EXIT run-rate is ≈$208m annualized, not $90m.** That is the honest denominator for a forward run-rate claim, and it collapses the apparent heroism of the relays:

| Mark | Status | vs FY26 >$90.0m | vs ≈$208m exit run-rate | vs guided 1H-FY27 (≈$800m ann.) |
|---|---|--:|--:|--:|
| **$400m in 1H FY27 (=2H CY26)** | **PRIMARY (guided)** | 4.4x the whole prior FY, in two quarters | **≈3.8x** | base |
| first triple-digit OCS quarter (FQ1'27 guide) | **PRIMARY (guided)** | one quarter > all of FY26 | ≈2x q/q | — |
| ">$1bn 2027 run-rate" | ⚠️ RELAY (not on the call) | ~11.1x | **≈4.8x** | **≈1.25x** |
| "$1.25bn/yr capacity" | ⚠️ RELAY | ~13.9x | ≈6.0x | **≈1.56x** |
| "~$10bn OCS TAM" | ⚠️ RELAY | ~111x | ~48x | ~12.5x |

**The edge:** the load-bearing number is the **$400m the company has already guided**, not the ">$1bn" that follows it — and the audit's earlier "~10-12x ramp" framing, while arithmetically right on the full-year base, materially overstates the step being asked for. **Only the ~$10bn TAM remains genuinely unbridged** (vs Redburn's $2.0bn '27 / $6.2bn '30 pool and COHR's >$4bn). **F1Q27 OCS ≥$100m is now a hard pass/fail.**
- **vs house model:** the relayed ">$1bn 2027" would be **12.3% of the house's 2027E revenue of $8.1bn** (12.7% of consensus CY27 $7,884m) from a line that was **2.99% of FY26 revenue**. House 2027E EPS $30.02 vs consensus $27.95 = **+7.4%** (below the 15% edge threshold; LITE is not on the programmatic edge list).
- ⚠️ **Unresolved against a prior wiki mark:** the filings imply a **≈$52m** June quarter against the page's **≈$70m** working mark (JPM "Networking" recap, 2026-05-08) — **~26% below**. Neither the Q4FY26 release nor the call disclosed an OCS figure, so **that broker mark was never scored.** Both left standing.
- **Also filed, and it is the "own the light source" thesis in company numbers:** laser chip + assembly = 78% of Components growth ≈ **$693.7m = 50.7% of LITE's entire incremental FY26 revenue**, with **ASPs UP** on the 200G lane shift — against **cloud transceivers +>173% on volume with ASPs DOWN**. FY26 GAAP GM decomposition: **54% factory utilization / 29% mix / 17% intangibles.**
- **New capital-structure risk, not in any estimate:** all Notes are convertible at holder option in Q1 FY27 and are reclassified to **current liabilities**; **$757.8m of early conversion requests as of 08-14**, principal settled in CASH.

### ③ 🔴 SPCX — DB is **+11.1% above consensus on 2027 revenue**, but the EPS gap is a **basis question, not an edge**, and capex now has three incompatible bases.

| Metric | DB revised | Consensus CY2027 | Δ |
|---|--:|--:|--:|
| Revenue | $115,308m | $103,785m | **+11.1%** |
| Capex | $185,034m | $181,353m | +2.0% |
| Non-GAAP EPS | $3.44 | $1.66 | *(basis — see below)* |

DB took 2027E revenue **$97,105m → $115,308m** and 2028E **$148,081m → $198,056m**, EBITDA 2027E **$63,330m → $78,369m**, EPS 2027E **$2.35 → $3.44** and 2028E **$3.30 → $5.62**, while **cutting gross margin in all three years** (2026E 61.5%→59.0%, 2027E 68.1%→63.3%, 2028E 68.9%→66.6%) — the signature of a lower-margin application layer (Cursor) bolted onto a higher-margin base, plus separately raised neocloud estimates.

⚠️ **Do NOT report the EPS gap as a 2.07x divergence.** Consensus has SPCX at **−$0.94** for CY2026 where DB has **+$1.06** — a sign difference, not a magnitude difference, which points to a non-GAAP treatment mismatch rather than a disagreement about the business. **Resolve at the next print before trading it.**
🔴 **Capex has three live bases and they must not be blended:** DB 2026E **$66,950m** vs the page's mandated sum-of-quarters **~$57.4bn** vs the CY-sum snapshot **$47.4bn** — the standing `estimates.json` CY-sum defect (CY columns embed pre-print consensus for reported quarters) showing up again. **CY2028 has no consensus at all**, so DB's 2028E numbers are unarbitrated.
- **vs prior wiki:** DB's "1.4 GW exiting 2Q26 → >2 GW by year-end" is the **same ladder as the Q2 print, not independent corroboration**, and DB does **not** underwrite the ~10 GW exit-2027 figure carried elsewhere on the page. DB's PT ($235, +60.7% on spot) was already on the page from 08-10 — **no PT drift this run.**

### ④ 🔴 HPE — an **upgrade with a price-target cut**, and MS is **+11.7% above consensus** on the fiscal year it is valuing.

MS moved HPE **Equal-weight → Overweight while cutting the PT $71 → $69**, because the methodology changed from **17x FY27 EPS of $4.17** to **15x FY27 EPS of $4.58**: the estimate rose ~10%, the multiple compressed ~12%. **MS's $4.58 is +11.7% above the consensus CY2027 EPS of $4.10.** The PT still implies +19.8% on spot. **The edge is the same shape as DELL's — numbers up, multiple down — but here the rating followed the numbers instead of the multiple.** ⚠️ MS now argues the pull-forward is structural, which cuts against the same analyst's own June "ASP, not units" bear line still standing on the page.

### ⑤ 🔴 AVGO — Epoch reconciles **to the dollar** with what the page already held, but it adds a **timing and seniority** shape that no estimate carries.

✅ **Not a new exposure — corroboration.** $6bn (A1) + $24bn (A2) + $4.5bn (B) = **$34.5bn of debt**, and adding the **$800m Apollo/Atlas SP equity already on the page** reproduces the "**$35bn first tranche**" from JPM (06-16) and AVGO's own 10-Q. **Logged as one fact so it is never double-counted as a second exposure.** The **$29bn reported maximum exposure** was already on the page.
**Genuinely net-new, and it changes the risk shape:**
- **The draw schedule: ~16 stages over a little more than a year, with ~$24bn out by summer 2027 ⇒ Broadcom's exposure PEAKS MID-2027. Today's drawn balance is not the peak.**
- **The waterfall: AVGO is SECOND-loss, behind used-rack residual value** — precisely what Bernstein's 08-11 residual-value flag was pointing at.
- **The 2.75pp A2-vs-B spread (5.75% vs 8.5%) is an UPPER BOUND on what the backstop is worth to lenders**, since it also embeds seniority.
**Scale check:** $29bn of maximum contingent exposure = **15.2% of consensus CY2027 revenue ($190,743m)**. House 2027E revenue ($190bn) and consensus are **in line**; house 2027E EPS $21.07 vs consensus $21.28 is **−1%**. **So the contingent exposure is material relative to the P&L and appears in neither number.**
⚠️ **Never chain $34.5bn to a per-GW mark:** it sits against an open-ended ">1 GW" (a *ceiling* on debt-per-GW) and buys complete rack systems at Google's grossed-up resale price — not comparable to Hock's $10–20bn/GW content or Jefferies' $11bn/GW.

### ⑥ 🔴 INTC — the ">97% EMIB-T yield" claim **has no stated process step**, and every other mark on the wiki that does name one is 50–92%.

| Source | Date | Mark | Level named? |
|---|---|---|---|
| **Mizuho** | 08-16 | **">97%"** | 🔴 **NO** |
| Fubon | 07-08 | Google requires **95%+**, "very challenging" by mid-2027, falls back to TSMC CoWoS 2028 | yes (gate) |
| DIGITIMES | 08-03 | package **>90%**, but "**a 50% SUBSTRATE YIELD REMAINS THE BOTTLENECK**" | yes |
| JPM | 08-16 | **~60% substrate / ~90% chip-on-substrate** | yes |
| UBS | 07-26 | **~90–92% packaging validation, substrate ~50%** | yes |
| rival IR (relay) | 07-28 | EMIB "doesn't work" | — |

**Decision: ">97%" was NOT used to declare Google's 95% gate cleared, and all five marks are kept side by side.** The spread between the highest and lowest level-specified mark is **~1.6x**, so a headline yield without a named step cannot be placed. **This is the run's clearest example of a number that looks like a resolution and is actually a missing basis.** Net-new and usable: the reticle ladder denominated as **output** for the first time — "**5–10x increase in ASIC outs**".

### ⑦ 🔴 CoWoS 2027 growth — ~2.5x apart between houses, and **internally inconsistent inside Mizuho's own numbers**.

| Source | 2027 CoWoS growth |
|---|--:|
| **Mizuho 08-16** | **+>75% y/y** |
| JPM (Gokul) 05-27, on page | **+30%** |
| **Mizuho's OWN capacity ladder on the page** (140kwpm end-26 → >200kwpm end-27) | **≈+43% exit-to-exit** |

A reconciliation **hypothesis** was logged with a stated falsifier (">75%" may be a CoWoS-**equivalent pool** figure including the non-TSMC additions the note itself flags as upside — ASX and AMKR growing CoWoS 2x — versus a TSMC-only ladder). **Mizuho does not say so, so it is not adopted.** ✅ The **5.5x CoWoS-L reticle base is identical** across Mizuho's 08-09 and 08-16 notes and remains the reliable anchor; the same author's reticle *ladder*, however, moved from 10–12x (EMIB/EMIB-T) + 14x-by-2029E (CoPoS) to an aggregated **8–12x for 2028E** in seven days.

### ⑧ 🔴 The relay arrived first **and inverted the sign — on two pages at once**.

The Mizuho 08-16 note had already been folded onto NVDA, MU and CRDO that morning as an 08-17 "**via TMTB**" relay row. **Relay:** HBM content flat GB300→VR200 "**before stepping up materially with VR-Ultra**." **Primary:** flat at **288GB (HBM4)** through VR200 and **VR-Ultra DOWN to 256GB HBM4e** — what rises is **price (+70–100%)** and **rack-level content (+3.5x on NVL576 / Oberon x4 / Taycan, which carries 8x the GPUs)**. **Both NVDA and MU had adopted the inverted direction.** Characterisations retired to Changelog, relay rows retained as dated records.
**And the per-GPU number cannot currently be placed at all — four non-agreeing marks:**

| Source | VR-Ultra HBM per GPU |
|---|--:|
| Mizuho 08-16 | **256GB** (HBM4e) |
| FundaAI | **192GB** (HBM4 8-Hi, "Lite" NVL576) |
| Fubon | **~384GB** (two-die survivor) |
| UBS / JPM | **384 → 192GB** |

Diagnosed as **SKU ambiguity, not noise**. **Rule recorded: no per-GPU HBM number is usable without naming the SKU and the rack.**
🔴 **And the price leg collides with MU's own contract structure:** Mizuho's **+70–100% HBM4e pricing** against management's disclosure that the first **16 SCAs are ceilinged at CQ2-2026 pricing**. MU's Sinal now scores price **direction ✓** and price **CAPTURE ⚠** separately. Mizuho also **conflates "LTAs/SCAs/NBMs" as one instrument** — the standing finding is that **MU is a ceiling and SNDK is a floor**.

### ⑨ 🔴 TrendForce contradicts **TrendForce** on 2027 DRAM — same house, 12 days, opposite sign — while staying consistent on NAND.

| Vintage | DRAM 2027 | DRAM 2028 | NAND |
|---|---|---|---|
| 07-30 (on the theme page) | gap **"widening in 2027"** | — | "turns positive, loosens 2H27" |
| **08-11 at FMS (this run)** | gap **"bottoms out and begins to narrow in 2027"** | **+4.0% sufficiency** | **+0.4% 2027 / 2% oversupply 2028** |

✅ **The asymmetry is what makes it diagnosable: the NAND leg did NOT flip.** TrendForce is *consistent on NAND and self-contradictory on DRAM*, and the newer version is a third-party relay of a conference slide **with no stated basis**. 🔴 It also collides with **UBS's "undersupplied until at least 2Q28"** (2027 sufficiency −13.6% raw / −1.2% inventory-adjusted). Basis guard recorded: TrendForce quotes no basis; the page carries three. **FUNDA takes the opposite side** — ASP flattening is "structural normalization", prices hold at elevated levels through 2027 on higher LTA share and a DC mix shift — so the theme now carries an explicit dated bear pole and bull pole, unresolved.

### ⑩ 🔴 CIEN — the scale-across anchor adopted **24 hours earlier** measures a different thing.

| Source | Figure | What it denotes |
|---|--:|---|
| Redburn (adopted 08-17 as *the* anchor) | **>$20bn by 2030** | **scale-across itself** |
| **CIEN management via FUNDA 08-12** | **$8–10bn by 2029** | **a SLICE of a >$20bn long-haul + metro transport market** |
| ANET via FUNDA 08-12 | $15bn (switching/routing) → ~$20bn incl. optics, 2030 | **a third slice** |

**Written on-page as non-interchangeable, neither adopted.** ANET's and CIEN's figures are closer to **additive** than conflicting (different layers under Nokia/Hotard's scale-across-vs-DCI boundary, adopted as the page's working cut). ✅ The three constructions do cluster in the **low-$20bn band**, which strengthens the standing instruction that the 650 Group's "$100bn+" is the outlier — but the *identity* of the >$20bn matters and was being conflated.

### ⑪ 🔴 Two unexplained Mizuho PT moves, same pattern as a prior instance.

- **AMD Outperform $615 (07-11) → $580 (08-16)** with **no revised multiple or EPS** — the mark simply sits in an industry note's PT table. $580 on consensus CY27 EPS $15.30 = **37.9x**.
- The same house did this to **INTC ($135 → $109 inside the 08-09 AVGO note)**; tonight's $109 reiteration retroactively firms that cut.
- **SNDK $2,200 (07-11) → $1,900 (08-16)**, Outperform held, in an industry note with **no SNDK model work**, on a ~14% lower price. First house to re-mark post-Investor-Day (retiring one of three "stale" flags). **The new ladder is $2,745 → $2,500 → $2,250 → $2,200 → $2,100 → $1,900 → $1,750, so the page's repeated "nobody between $1,750 and $2,200" no longer holds.**
**Read:** PT marks embedded in industry notes are being changed without rationale. They are logged as published and flagged as un-rationalised rather than treated as analytical revisions.

### ⑫ 🔴 Fabrinet — a relay of the SAME print already on the wiki is measured on a **taxonomy the company retired in that very report**.

**Relay (already on the page):** "Datacom was DOWN on the quarter, $258mn vs $271mn consensus", FN −6.5%. **Company:** **data center $669m, +68% y/y, 51% of revenue** under the new three-way cut (data centers / comms infrastructure / auto-industrial-other) adopted *because* "hyperscalers and other data center service providers are the ultimate customers of many of the products we manufacture, including some of those that have been characterized as telecom products in the past."
**The relay's q/q ties to the new segments (+8.1% vs +7.6% relayed) but its y/y does NOT (new segments imply ~+56%, relay says +39%).** **Basis artifact until re-run against the restated 12-quarter history** — do not treat the "datacom miss" as a demand datapoint.
Other FN marks worth carrying: **NVIDIA down 20%+ for the year at FN while the rest of the business grew ~57–60%**; the **revenue-capacity ladder to $12.5–14bn vs ~$11.5bn framed one quarter earlier** (+8.7% to +21.7% in a quarter, ≈2.7–3.0x FY26 revenue, on ~$1,500–1,750/sq ft); and a **three-rung cross-stack GM ladder from one week of prints — LITE 50.4% > COHR 40.2% > Fabrinet 12.2%** (FN on 1.3% opex / 10.9% operating margin, a three-year high).

### ⑬ 🔴 Two independent merchant CW-laser entrants land in the **same quarter** — the moat holds through CY27 and breaks on price, not volume, in 2028.

**MACOM: CW laser in production "late CY2027 at the earliest" despite intense customer pull** (and a flagged **general supply shortage of InP DFB lasers**) alongside **WIN Semiconductors' CW project with "a major US optical chip IDM", mass production YE27** (JPM, 07-26, already on the page). ✅ **The two-supplier moat is corroborated INTACT through CY27** — a second entrant cannot arrive sooner even with intense pull. 🔴 **But 2028 now has a converging cohort**, which feeds Jefferies' (08-05) C28 capacity-overshoot risk where "the pricing gains that drove margin expansion would be the first casualty". ⚠️ **Open, not adopted: WIN's unnamed IDM may BE MACOM**, which would collapse the cohort back to one program.

### ⑭ 🔴 The EML→SiPho pivot **partially nets** the InP-scarcity thesis against the SiPho-share thesis. Three agents reached this independently.

A SiPho transceiver carries **~50% LESS InP content** than an EML-based one but **significantly more active-alignment content**, and "it is trivial to pivot manufacturing from EML based to SiPho based — the issue is active alignment capacity/throughput, not the design itself." Against the wiki's own SiPho-share marks (**Jefferies 07-14: SiPho >60% of 1.6T; GS: SiPh 56% of dollars by 2027**), a share shift is **InP-demand-dilutive per unit** — the opposite sign to the InP-shortage narrative running on MACOM's DFB shortage, the InP capacity adds and the 5-year optical LTAs. **Forced a per-bin restatement: EML InP demand is exposed to the pivot; CW / high-power InP is not.** ⚠️ Denominator trap flagged (1.6T vs total). LITE management's OFC-2026 lane-share rebuttal (InP 91%→79% of AI lanes) **does not answer the per-module content point.**

### ⑮ 🔴 Anthropic's datacenter debt per MW is **bimodal — the blended average is not a usable build anchor**.

| Project | Sponsor | Critical IT | Project debt | $m per MW |
|---|---|--:|--:|--:|
| Abernathy | Fluidstack JV | 168 MW | $1.300bn | **$7.74** |
| Barber Lake | Cipher | 207 MW | $1.733bn | **$8.37** |
| Lake Mariner | TeraWulf | 378 MW | $3.200bn | **$8.47** |
| Meridian Arc | Next Frontier / Fluidstack JV | 430 MW | $5.700bn | **$13.26** |
| River Bend | Hut 8 | 245 MW | $3.250bn | **$13.27** |
| **Total** | | **1,428 MW** | **$15.183bn** | **$10.63 blended** |

**Two clean clusters ~57% apart ($7.7–8.5m/MW vs $13.3m/MW), so the blended $10.63m/MW (≈$10.6bn/GW) averages across what are evidently different scopes** (shell-only vs powered-and-equipped, or different power-cost regions). ⚠️ **UNIT DISCIPLINE: this is project DEBT per MW of CRITICAL IT LOAD — not facility GW, not total build cost, and NOT revenue per watt.** It must not be netted against the $30–50/W Rubin, ~$29/W Colossus, IREN $/MW or $36–60bn/GW build anchors already on the wiki.
🔴 **Also a base collision, flagged not netted:** Bernstein (07-07) has the "**Anthropic contract at $19Bn**" at TeraWulf/Lake Mariner against Epoch's **$3.200bn** for the same site — **lease/contract value vs project debt raised**, two different quantities.

### ⑯ 🔴 Cursor's token routing is a quantified threat to frontier-lab API revenue — and it now sits inside a competitor.

DB estimates **Cursor's internal Composer model costs 10–20% of Claude/GPT**, and models the ladder at ~$120/month of usage: **uncapped Pro → Cursor pays Anthropic or OpenAI $120 on $20 of revenue (−500% GM); Team seat + meter → 25% GM; Cursor Router sending two-thirds of agent turns to Composer 2.5 → COGS $48 on $80, 40% GM.** **Cursor reached $1bn ARR on ~300 people.** ⚠️ **Magnitude deliberately left unquantified on ANTHROPIC and OPENAI — DB publishes no dollar spend and no Anthropic-vs-OpenAI split**, so the 10–20% ratio and the two-thirds routing share are labelled DB estimates, not disclosures. Anthropic is simultaneously Cursor's supplier and its rival (**Claude Code and OpenAI Codex named as Cursor's most direct competitors**).

### ⑰ ⚠️ Mizuho's CSP capex was **raised AND re-labelled in five weeks**, and its RPO growth rate is internally inconsistent.

- **Capex:** 08-16 "**CSP** capex +111%/+50% to ~$1T/~$1.5T 2026E/27E, 2028E +12% to >$1.6T" vs the 07-11 note the wiki cites, "**AI DC** capex to $1.2T '27 / >$1.4T '28". **2027E moved $1.2T → ~$1.5T and 2028E >$1.4T → >$1.6T while the base label changed.** Either a raise or a redefinition; the note does not say. **Not adopted — canonical framing stays on `hyperscaler-capex.md` / `_meta/assumptions.md`.**
- **RPO:** the summary says "**up 3.5x y/y**", the body says "**up >250% y/y**", and the stated endpoints (**~$735bn in 1Q25 → ~$2.3T now**) work out to **~3.1x / +213% over ~5–6 quarters, not a year**. **Endpoints logged; none of the four rates adopted.** Four separate agents independently reached this handling.
- ⚠️ **"Neoclouds & Tier-II CSPs to >30% share 2027E"** is compatible with the wiki's "frontier labs ≈80% of demand" (capex share vs end-demand share), **but for ASIC share the direction is negative** — Neoclouds are the buyer class least able to fund custom silicon.

### ⑱ ⚠️ Un-scored and newly-contested marks worth tracking

- **COHR yield: management's "6-inch is cost structure, NOT a yield gap" (08-12) vs the inferred "the only explanation is bad CPO-laser yield" (08-13) sit at EVIDENTIARY PARITY, because COHR publishes no yield data** — an MS analyst asked on the call and got nothing. **This is a disclosure gap, not a factual contradiction.** 🔴 And there is now a **mundane competing explanation from LITE's own 10-K**: 54% of LITE's FY26 GM-dollar gain came from **factory utilization**, only 29% from mix — utilization being precisely the lever a capacity-constrained issuer mid-6-inch-transition has least of.
- **The InP-ramp RANKING is contradicted across houses:** FUNDA/Nokia-call has **COHR "already doing pretty well" and LITE "a bit behind"** (second instance after Aurelion's 4-inch-vs-6-inch bear, 07-29) against **JPM 08-14: LITE gets the MORE significant FY27 GM expansion on EARLIER program ramps.** Both stand.
- **CIEN is NOT among Fabrinet's ≥10% customers** (Cisco 20 / NVDA 16 / Nokia 11 / AMZN 11) — a disclosure-threshold fact only (**CIEN <10% of FN's $4.6bn ≈ <$460m**), filed as outsourcing mix, with the **Nokia-on / CIEN-off** pairing as the watch item.
- **CRDO: "ALC/microLED" appears in neither management's guided FY27 optical breakdown nor any sell-side preview on the page** — an unmodelled leg, unsized (Mizuho gives no number), and a question for the print.
- **MEDIATEK's "FIRST high-volume EMIB-T customer" is an ORDERING claim with no stated basis**, upgrading MTK from one-of-several to anchor tenant while AVGO and META are also EMIB-T evaluators (DIGITIMES 08-03).
- **MRVL pJ/bit: 13.2 optical vs ~50 copper (new) against ~2.5 E-O-E + 0.7 laser vs ~10 copper (SemiAnalysis CPO Book).** Similar ratio, ~4–5x different absolute levels on **both** sides ⇒ different scopes (network path vs point-to-point link). **Rule: never chain them.**
- **FUNDA vs FUNDA on HBF bandwidth:** 08-11 "bandwidth *and* capacity above HBM" → 08-14 "read bandwidth *on par* with HBM". **Post-event version governs.**
- **Elasticity ranking contested:** MS (07-27) models a larger % shortfall in PCs than smartphones; FUNDA argues PC OEMs are the *more* tolerant buyer.
- **STX:** the MS note's own exhibit price of **$812.76** sits below prices already on the page from the same window (SIG $856.13 on 08-01, MS spot $851.69 on 07-27) — carried as the exhibit's own figure, **no inference drawn**.

---

## CONFIRMS — no action

| # | Datapoint | Baseline agreement |
|---|---|---|
| 1 | **Mizuho NVDA PT $300** | Sits on the **consensus PT of $303.71** (live 08-17 pull, recorded in `reconciliation-2026-08-15.md`) and is a reiteration of the 07-11 mark. |
| 2 | **`estimates.json` actuals validated by a filing written after it** | The snapshot's `LITE.actual.rev` = **3014.0** matches the FY26 10-K's **$3,014.0m** to the decimal. |
| 3 | **Mizuho MU $1,375 / CRDO $290 / INTC $109** | Reiterations of 07-11 (and 08-09 for INTC) — no drift to log. |
| 4 | **AVGO's Anthropic exposure reconciles to the dollar** | $6bn + $24bn + $4.5bn = $34.5bn debt, + $800m Apollo/Atlas SP equity = the "$35bn first tranche" already on the page from JPM 06-16 + AVGO's 10-Q. Corroboration, **not** a second exposure. |
| 5 | **Kyber/Feynman midplane delay** | Mizuho's cause matches **SemiAnalysis 07-06** — second independent house, upgraded from single-source. |
| 6 | **CoWoS-L 5.5x reticle base** | Identical across Mizuho's 08-09 and 08-16 notes. |
| 7 | **MEDIATEK 2028 EMIB-T HVM** | Matches management ("HVM early 2028"), Nomura and MS; the TPUv9/EMIB-T link matches UBS 07-24 and management's on-record "we are more committed to EMIB-T" (07-31). Third-house corroboration; **no packaging assumption superseded.** |
| 8 | **Ramp AI Index** | GS's $12 median / $650 top-decile (July) is consistent with the wiki's 06-18 marks ($11 median / $611 top-10%) and SPCX's "~$11 in June" — one series still climbing, **not three conflicting readings.** |
| 9 | **MU's two KeyBanc lines** | FUNDA relayed them; both **verified verbatim in the Bloomberg FINAL TRANSCRIPT already on disk** (`MU\transcripts\MU_KeyBanc-Tech-Leadership-Forum_2026-08-10.md`) — *"the number one constraint they have is DRAM"* and *"we are not able to meet any more than half of the demand our customers have."* ⚠️ **The 08-15 fold of that transcript MISSED both** — the relay indexed our own primary better than we did. |
| 10 | **KIOXIA 40–50% fulfilment** | Consistent with Micron's "cannot meet more than half of data center demand" — two independent suppliers on the same shortfall. |
| 11 | **HBF 1.5–2TB per package** | = 3–4 stacks × ~500GB, consistent with Arete's 512GB-16-die / 1.5TB-gen-3 and JPM's 512GB-two-stack (different bases). |
| 12 | **CXL 1H27 expansion / 2H27 pooling** | FUNDA independently corroborates the BNP timeline already on the theme. |
| 13 | **Scale-across clusters in the low-$20bn band** | Three constructions (Redburn, ANET, CIEN) — reinforces that 650 Group's "$100bn+" is the outlier. ⚠️ Subject to item ⑩'s base caveat. |
| 14 | **FN's "NPO before CPO"** | Independent supply-chain-side corroboration of the NPO-additivity thesis built from LITE's call and the LightCounting revision — from the layer that physically builds the packages. FN gave **no** revenue or margin ("too early to talk about revenues and margins"). |
| 15 | **Nothing on the programmatic edge list moved** | House-vs-consensus |Δ|≥15% rows (COHR EPS +65% / rev +31%, NVDA EPS +19% / rev +16%, GOOG rev +18%, AAPL EPS +16%) are untouched by tonight's sources. LITE house-vs-consensus is **+7.4%** on 2027 EPS — below threshold. |

---

## Not independent corroboration — double-count guards set this run

1. **FUNDA Deep|Optics restates THREE sets of figures already on the wiki under other bylines:** the LightCounting datacom set (JPM · Cardoso, 08-06), the ANET $15bn/$20bn/$3–4bn set (MS · Derrick Yang, 08-05) and Nokia's EUR 2.8bn order intake (JPM · Scott Silver, 07-26). **Three of five headline sizings.**
2. **Mizuho 08-16 reached NVDA, MU and CRDO twice** — once as an 08-17 "via TMTB" relay, once as tonight's primary. **One source, not two** (and the relay had the sign wrong — item ⑧).
3. **DB's SPCX compute ladder (1.4 GW → >2 GW)** is the same ladder as the Q2 print.
4. **Epoch's AVGO tranching** is the same transaction as JPM's 06-16 "$35B XPV/SPV" at higher resolution.
5. **Bernstein's HBF wafer-absorption argument, called "NET-NEW" in the 08-15 changelog, was stated unquantified by FUNDA three days earlier.** Bernstein owns the number; FUNDA owns the priority.

## Baselines that could not be run

- **Consensus target price and rating for every name above** — Terminal offline (item 3 in the baseline table). Priority rows: **DELL** and **SPCX**.
- **CY2028 consensus for any name** — absent from the snapshot, so DB's SPCX 2028E ($198.1bn revenue / $5.62 EPS) and Mizuho's 2028E packaging and unit marks are unarbitrated.
- **House models for 20 of tonight's marked names** (see baseline table) — DELL and SPCX, the two largest estimate divergences in the run, both lack one.
- **Private names (ANTHROPIC, OPENAI)** have no BBG or house baseline by construction — reconciled vs prior wiki comments only.
