# Reconciliation — 2026-08-03

_Run: `/run-inbox` (scheduled, unattended). Four sources reconciled:_
1. **UBS fireside with Teradyne IR (Amy McAndrews), 2026-08-03** — post-2Q26 callback debrief (machine transcript).
2. **Fubon supply-chain update — Sherman Shang (Taiwan semis) + Arthur (downstream/ODM), hosted by Jefferies, 2026-08-03** (machine transcript).
3. **Morgan Stanley · Erik Woodring, "What's New in the 10-Q, Including 2 Post-Earnings Thoughts" (Apple), 2026-08-03.**
4. **SemiAnalysis · Kimbo Chen / Shubham Choudhari / Bryan Shan / Dylan Patel, "Kimi K3, The Manos, The Mythos, The Legendos", 2026-08-03.**

_Two further files in the inbox — the `(12) …` SemiAnalysis PDFs on **Amazon's AI Resurgence (2025-09-03)** and **Microsoft's AI Strategy Deconstructed (2025-11-12)** — were **dropped as duplicate re-drops**, not reconciled. Both were already ingested substantively (AMZN.md:87, MRVL.md:105, MSFT.md:128-129, ORCL.md:51). Nothing was double-counted._

---

## Baseline availability

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Available — used throughout; every superseded value was moved to the relevant page's `## Changelog` during patching. |
| **2. Capstone house models** | ⚠️ **Partial — 8 of 16 affected names have no house model.** `_data/house.json` (asof 2026-08-03, scraped from the pages; underlying Excel models dated **2026-06-05 → 2026-06-17**) covers **AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM**. **No house model for TER, MEDIATEK, INTC, AMD, AMZN, MU, SKHYNIX, SAMSUNG, ADVANTEST, STX, WDC, ARM.** TER carries only an EPS-only block from the ASML-peers semicap model — **already flagged broken on 2026-08-01 (house 2026E EPS $5.46 vs consensus $8.08, -32%); still un-remarked, so no TER house comparison is attempted below.** |
| **3. BBG consensus (live re-pull)** | 🔴 **PENDING — `HTTP 503: Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal`.** Tested at ingest against `TER US Equity` / `AAPL US Equity`. **No web data was substituted at any point.** Consequence: **no `BEST_TARGET_PRICE` for this run** — every PT placement below is vs prior wiki PTs and spot only, never vs a consensus median. |
| **3b. BBG consensus (on-disk snapshot)** | ✅ **Used as the consensus baseline throughout.** `_data/estimates.json` **asof 2026-08-03** — same calendar date as every source in this run — 97 names, full quarterly (1FQ/2FQ) + CY2026/CY2027 lines. This is genuine recorded BBG consensus, but it is a **snapshot, not a live pull**: it carries no target prices and cannot reflect any revision made during 08-03 itself. |

### Action required
**Log in to the Bloomberg Terminal / reconnect the Capstone VPN, then re-run `/wiki-consensus`** to (a) refresh `estimates.json` live and (b) pull `BEST_TARGET_PRICE` so the Apple PT in ① (currently placed only against the Refinitiv mean of **$319.82** carried inside the MS note itself) and the TER/ADVANTEST PTs can be marked against the BBG consensus median.

---

## Method flags (read before using any number below)

1. **⚠️ CY2026 understates beats — systematic, ours not Bloomberg's.** Our CY aggregate re-pulls already-reported quarters via `BEST_FPERIOD_OVERRIDE`, which returns the **pre-print consensus mean rather than the comparable actual**. Root-caused on 2026-08-01 (TER: CY26 line $8.08 vs sum-of-quarters $8.96, **-9.8%**). It affects **all 97 names** — every one has ≥1 reported 2026 quarter embedded in its CY2026 line. **CY2027 is clean** (`n_actual=0` for all 97). **Where a CY2026 comparison below is load-bearing it is flagged; prefer the CY2027 column.**
2. **⚠️ TSM mixes unit bases in one record.** `estimates.json` keys TSM to the **ADR** (`TSM US Equity`): `px`/`mktcap` are **USD**, `rev`/`capex` are **TWD millions** (parent basis), and `eps` is **TWD per ADR**. The Capstone house model quotes **NT$ per ordinary share**. **Comparing them requires ×5 on the house EPS** — done explicitly in the **CONFIRMS** table. A naive comparison shows a spurious ~5× gap.
3. **FX is calibrated, not assumed.** TWD/USD is **backed out of the data against an observable anchor** rather than guessed: TSMC's own 2026 capex guide is **$60-64bn** (USD-denominated, disclosed) and the BBG CY2026 capex line is **TWD 1,957,725m** → implied **31.58 TWD/USD**. Every TWD→USD conversion below uses 31.58. Guardrail: the same rate returns TSM CY2026 revenue of **$172bn** against a house model of **$165bn** (-4%) — i.e. the rate does not distort the revenue line either, so it is not fitted to a single series.
4. **⚠️ Both transcripts are machine (ASR) transcripts** with garbled proper nouns (Fubon←"Foobon", Blackwell←"Black Wheel", CoWoS←"CoOS", Kyber←"Kyper", Titan←"Tycan", Broadcom←"Borcom", Venice←"V-ness", Vera←"V-core", KYEC←"KYC", Ibiden←"Epident", SerDes←"services"). Two names were **not resolvable and deliberately not guessed** — `"Seasam"` (a Taiwanese advanced-packaging supplier spanning CoWoS/EMIB/fan-out/next-gen CoWoS) and `"Weichuang"` (a Taiwanese ODM). Numbers quoted from speech are inherently softer than numbers read off a published note; the Morgan Stanley figures in ① are the only ones in this run taken from a written source.
5. **One derived-price estimate is Fubon's, not ours.** The $78-80k Rubin ASP in ⑧ is **Fubon's own back-solve off an assumed 75-80% Nvidia chip gross margin**, not a disclosed price. It is carried as his estimate with the assumption attached, and is **not** used to drive any conclusion below on its own.
6. **No consensus PT anywhere in this run** (see baseline 3). Any statement about a PT is vs prior wiki PTs and spot.

---

## Consensus + house reference table (BBG on-disk snapshot, asof 2026-08-03)

_Native reporting currency; revenue/capex in millions unless marked. House = Capstone official model (June-2026 vintage)._

| Name | ccy | spot | CY2026 rev | CY2027 rev | rev Δ | CY2026 EPS | CY2027 EPS | CY2026 GM | CY2027 GM | House 2026 / 2027 |
|---|---|---|---|---|---|---|---|---|---|---|
| **TER** | USD | 363.65 | 4,899 | 6,253 | **+27.6%** | 8.08 | 11.34 | 58.5% | 59.2% | ⚠️ broken (EPS 5.46 / 6.90) |
| **ADVANTEST** | JPY | 31,430 | 1,457,644 | 1,839,863 | +26.2% | 733.78 | 959.18 | 66.5% | 67.2% | — |
| **AAPL** | USD | 304.82 | 486,223 | 535,735 | +10.2% | 8.77 | 9.95 | 47.5% | 47.5% | rev 480 / 539 ($bn); EPS **10.12 / 11.11** |
| **NVDA** | USD | 207.04 | 392,141 | 568,186 | **+44.9%** | 8.86 | 12.91 | 74.9% | 74.3% | rev **407 / 661** ($bn); EPS **9.26 / 15.44** |
| **TSM** | mixed | 402.08 (USD/ADR) | 5,435,272 TWD | 7,344,357 TWD | **+35.1%** | 519.71 /ADR | 710.39 /ADR | 66.1% | 66.4% | EPS NT$102.5 / 143.5 **per ordinary** (×5 → 512.5 / 717.5) |
| **MEDIATEK** | TWD | 3,910 | 659,139 | 1,140,248 | **+73.0%** | 66.62 | 136.37 | 45.7% | **44.3%** | — |
| **GOOG** | USD | 369.89 | 426,673 | 544,324 | +27.6% | 12.92 | 16.50 | 68.5% | 67.8% | rev 505 / 641; capex **183 / 310**; GW 4.6 / 7.75 |
| **INTC** | USD | 90.50 | 60,008 | 71,553 | +19.2% | 1.00 | 2.01 | 39.9% | 43.7% | — |
| **AMD** | USD | 483.03 | 49,396 | 78,537 | **+59.0%** | 7.40 | 13.96 | 55.8% | 55.9% | — |
| **AVGO** | USD | 387.22 | 123,422 | 190,191 | **+54.1%** | 13.60 | 21.21 | 74.2% | 72.4% | rev 115 / **190**; EPS 12.89 / **21.07**; 2028 rev 315, AI semis 251 |
| **AMZN** | USD | 284.71 | 820,312 | 945,704 | +15.3% | 9.61 | 12.57 | 51.3% | 53.1% | — |
| **MU** | USD | 814.20 | 163,761 | 262,692 | **+60.4%** | 96.50 | 163.98 | 83.2% | 86.0% | — |
| **SKHYNIX** | KRW | 1,521,000 | 350,971,987 | 545,346,672 | **+55.4%** | 328,968 | 623,862 | 84.6% | 84.9% | — |
| **SAMSUNG** | KRW | 233,500 | 706,327,968 | 982,216,094 | +39.1% | 46,811 | 75,167 | 69.4% | 75.2% | — |
| **STX** | USD | 811.61 | 14,961 | 21,802 | **+45.7%** | 24.03 | 44.51 | 53.7% | **63.4%** | — |
| **WDC** | USD | 520.77 | 15,319 | 21,274 | **+38.9%** | 13.92 | 23.39 | 52.4% | **58.6%** | — |
| **ARM** | USD | 236.06 | 5,641 | 7,561 | +34.0% | 2.01 | 2.82 | 98.0% | 93.3% | — |

_Book positions (`book.json`, asof 2026-07-01): **long NVDA, TSM, AVGO, MSFT, GOOG, META, AMZN, AAPL.** Four names carrying material findings in this run — AAPL ①, NVDA ②, GOOG ④, TSM ⑥ — are live longs; TER, MEDIATEK, INTC, MU/SKHYNIX, STX/WDC and ADVANTEST are not in the book._

---

## ⚠️ Read this first — the run's structural finding

**Three of the four live sources had already reached the wiki through a secondary route, and in two cases the primary source corrects the summary.** This is not a routing nuisance; it produced a live thesis inversion (③) and a misfiled note (②).

| Source | Secondary route already on the wiki | What the primary changed |
|---|---|---|
| UBS/Teradyne fireside | UBS **sector-sales notes** (Ruple) on TER/ADVANTEST/STX/WDC | 🔴 **"10-20 months" → "10-20 weeks"** — inverts the signal. Also un-collapsed a real analyst-vs-company disagreement. |
| Fubon supply-chain call | **Jefferies desk relays** on MEDIATEK/INTC/NVDA/AMD/AVGO/GOOG + cowos-packaging | Volume variance (Rubin Q3 300-400K → 200-300K), share mark (30-32% → 30-33%), KYEC guide basis, plus the entire downstream/ODM half of the call. |
| Morgan Stanley Apple note | A single full-log row **misfiled into the `### Archived — Q2 FY26` table** | Full note folded in properly; the archived row is cross-pointed, not deleted. A task chip was spawned to consolidate. |

**Implication for process:** desk relays and sales-note summaries are arriving *ahead of* the primaries and are being ingested as if authoritative. They compress ranges, drop the Q&A, and — at least once — corrupt a unit. **Where a relay and a primary disagree, the primary wins and the relay's figure moves to the Changelog.** Applied throughout below.

---

## Where the new data DIVERGES (the alpha)

| Name | New datapoint | Prior wiki / house | BBG consensus (on-disk, 2026-08-03) | Read (the edge) |
|---|---|---|---|---|
| **AAPL** 📌long ① | MS: component/memory costs "expect these trends to intensify"; R&D **10.7% of revenue** (record June-Q); pricing hedged as an incomplete offset | House **FY26 EPS $10.12 / FY27 $11.11**; MS **$8.84 / $10.00** | CY26 **$8.77** · CY27 **$9.95** | 🔴 **Largest gap in the run, and it is all margin.** House is **+14.5% / +11.1%** vs MS on a clean fiscal-to-fiscal basis — but house revenue is **within 1.3% both years**. The house carries a materially richer Apple margin than the Street *into* a note documenting cost inflation on three fronts. **Bridge the margin assumption or re-mark.** |
| **AAPL** 📌long ② | ~**3.5pts** Sept-Q supply shortage; no A-series shortage in MS's TSMC checks → falls entirely on Mac = **$3.5B**, a 40-pt gap vs MS's own Mac forecast **$8,724mn (0% y/y)** → conservative bar, Ternus beat set up for late Oct | **@markgurman 08-02, already on the page:** real MacBook Air shortages, Sept delivery dates, buyers steered to base MacBook Pro | MS Sept-Q EPS **$1.96** vs BBG 1FQ **$1.996** (**-1.8%**) | 🟠 **The setup call is contested by our own page.** The Mac constraint appears to *exist* — what is in dispute is magnitude, not existence. Note MS models **below** consensus on the very quarter it argues has upside. Resolves on the late-Oct print. |
| **TER** ③ | Primary: lead times **"10 to 20 week"**, staying **under six months**; the **12-month** visibility figure is **Advantest's**, from its own IR call the prior evening | UBS sales notes had **"10-20 MONTHS"** on 4 pages; and a "300-500bps" band | — (management commentary) | 🔴 **A unit error had inverted the thesis.** Short lead times are TER's deliberate **share-taking weapon**, not a ballooning backlog. Corrected on TER.md + ADVANTEST.md; old value preserved in each Changelog. The band also hid a live disagreement: UBS models **~500bps** 2026 share gain (8-900 memory / 400 SOC), company says **300-400bps** — *"your numbers are a little bit heavier than what we see."* |
| **TER** ④ | IR: FY26 GM **~59.0%**; mid-term **"60% or higher"**; new financial model at the **February** call | House block **root-caused broken 2026-08-01** (2026E EPS $5.46 vs cons $8.08, **-32%**) and **still un-remarked** | CY26 GM **58.50%** · CY27 **59.20%** · rev **+27.6%** | 🟡 **Management guides above consensus at both horizons: +50bp FY26, +80bp mid-term.** Two things cut against it: part of the strong 1H is **undisclosed one-time Q1 benefits** withheld "for competitive reasons" (not a quality-of-earnings positive), and IR's *"memory and SOC at parity"* is hard to square with the 07-29 call's *"memory will continue to be a strain… into 2027."* ⚠️ CY26 cell inherits method flag 1; CY27 is clean. **No house comparison is meaningful until TER is re-marked.** |
| **TSM** 📌long ⑤ | Fubon hears **2027 capex $80-85bn**, *"I'm not sure that is enough to support all the customers' demand"* | Fubon **$80bn** (07-17), **$75bn** (07-08) → both to Changelog | CY27 capex TWD 2,471,808m ⇒ **$78.3bn** @31.58 | 🟠 **Fubon is +2.2% to +8.6% above consensus and still rising.** Read-through positive for semicap and for the ATE-TAM bridge in ④. ✅ **2026 confirms exactly** — BBG $62.0bn vs the guided $60-64bn (this is also the FX anchor, method flag 3). |
| **INTC** ⑥ | ~90% EMIB yield *"is just from the lab… the production rate is only around **75%**"* | Page carried UBS **~90%** (actually sourced to MediaTek v9 **trial** runs); a same-morning **DIGITIMES "yields hit target"** headline | CY27 rev **+19.2%**, GM 39.9→43.7%, capex **+25.9%** — **none of it an EMIB bet** | 🟠 **First lab-vs-production split on the wiki, on the number the entire TPU ramp rests on.** Levels logged with basis and deliberately **not averaged**: substrate 50-60% · packaging ~90% lab/trial vs **~75% production** · bar "high 90%" (UBS) / 95%+ (Google's gate). **Asymmetry:** EMIB *success* is not in the Street's Intel numbers, but EMIB *failure* is a direct hit to MEDIATEK and GOOG. Net-new: MediaTek's greater EMIB commitment answers Intel's **capacity** aggression, not its yield — a weaker foundation than the page assumed. |
| **MEDIATEK** ⑦ | 400G SerDes **ready 2H27** (mgmt, 07-31) — a year earlier than Fubon thought; 2027 TPU **3.5-4mn**; 2028 share **30-33%** | Fubon's own bear case: *"400G not ready 2 yrs → share peaks 2028 → V10 back to Broadcom"*; 2027 vol **2.5-3mn**; share **30-32%** | CY27 rev **+73.0%**, GM **45.7%→44.3%** | 🟠 **Fubon withdrew his own bear case.** MediaTek now in V10 (2029); hedge retained (still double-checking, 6-12mo monitoring). ⚠️ **But his 2028 demand math breaks his own range:** 4-5mn units × ~**$15k** V9 content ⇒ **~$60-75bn** of 2028 ASIC revenue vs the **$35-52bn** cross-broker range he himself quotes, and vs BBG CY2027 *total* revenue of **$36bn**. Either $15k is system/rack content not chip revenue, or the allocation is aspirational (he says it is demand, not production), or the Street is low. **Do not carry $60-75bn as an estimate.** Separately his *"V9 GM maybe 50%+"* would be **accretive** vs the -1.4pt mix dilution consensus embeds — breaking the GM-dilutive/OpM-accretive shape MS and JPM corroborated. Adjudicates at **tape-out, end-2026**. |
| **NVDA** 📌long ⑧ | Chip output **8.2mn → 12.4mn (+51.2%)**; HBM4 **$17-18 → $30-32/GB (+77%)** | House 2027 rev **$661bn** / EPS **$15.44** | CY27 rev **$568bn (+44.9%)** / EPS **$12.91**; GM 74.3% | 🟠 **Supports the house being 16.3% / 19.6% above consensus.** Unit growth **+51.2%** brackets consensus revenue growth **+44.9%** and sits nearer the house **+62.4%** — and with HBM content inflating **+77%/GB**, consensus revenue growing *below* unit growth implies flat-to-down blended ASP, which is hard to reconcile. ⚠️ **But the $78-80k Rubin ASP on the page is an output of an assumed 75-80% chip GM** — re-scoped, and **no longer citable as evidence of GM durability** (circular). Two unresolved: Rubin Q3 **300-400K (relay) vs 200-300K (primary)**; and the HBM4 step year is ambiguous **inside the primary itself** — "2026" in prepared remarks, "2027" in Q&A (a 2026 step pulls the GM test forward a full year). |
| **STX / WDC** ⑨ | TER: *"a tremendous amount of demand"* for HDD test driving most of ISPT y/y growth; density **or** units? — *"I think it's **both**."* | Drive makers' own framing: **no unit adds**, density-led margin | STX CY27 rev **+45.7%**, GM **53.7→63.4% (+9.7pt)**; WDC **+38.9%**, GM **52.4→58.6% (+6.2pt)** | 🟡 **Consensus is priced on the pricing story; the incremental information is volume.** Tester capex is a real asset commitment, not a duplicate PO — bears on the live UBS 2x-ordering bear on WDC (capacity *is* being provisioned). Second-hand from a supplier, **not** a drive-maker disclosure. |
| **MU / SKHYNIX / SAMSUNG** ⑩ | *"Only a small volume of Micron and Samsung HBM"* on Rubin; **Rubin with SK Hynix HBM4 ramps late Aug/Sept** — which paces the 200-300K→700-800K step | SKHYNIX Sinal ⚠ → **✓ upgraded**; SemiAnalysis ~0% MU / ~30% Samsung first-12-mo share **not superseded** (12-mo model vs Aug snapshot are compatible) | MU CY27 rev **+60.4%**, GM 83.2→**86.0%**; SKHYNIX **+55.4%**, GM +0.3pt; SAMSUNG **+39.1%**, GM +5.8pt | 🟡 **The Rubin HBM4 ramp is Hynix's; the Q2 "HBM4 delay" reads as timing, not a lost socket.** MU's **+60.4% / +2.8pt GM** is the most aggressive ramp in the group and now carries **qualification/share risk to size**. Net-new: an **HBM base-die issue** is the *second* cause of the ~2-month Rubin push-out (page had only the thermal redesign). |
| **AVGO** 📌long ⑪ | Broadcom *"less bullish in expanding capacity — the **testing** capacity"*; 2H26 addition **pushed out** | House 2027 rev **$190bn** / EPS **$21.07**; house **2028 rev $315bn, AI semis $251bn** | CY27 rev **$190.2bn** / EPS **$21.21**; **no CY2028 line** | 🟡 **First hard-asset negative on AVGO itself — and there is no house cushion:** house and consensus 2027 are **identical**. The house **2028 $315bn / $251bn AI semis** has nothing to check against, and Fubon **declines the AVGO-share-recapture bull case**, naming Intel production rather than vendor reallocation as the swing. Offset: **V10 is a monster** (8× 2nm dies — ASR-caveated, **6,000W TDP**, 400/448G SerDes) and AVGO's 400G is ready. **Two contradictions left open:** Samsung Foundry 2nm/3nm qualification (page, 07-28) vs *"not so sure… Broadcom will still use TSMC"*; and 400G-ready vs the page's "448G missed the v9 deadline" — **different speed grades, do not net them.** |
| **GOOG** 📌long ⑫ | **12-15mn TPUs in 2028**; V9 has 4 compute dies → 2028 consumption **more than doubles** → **30-35mn compute dies**; net-new gate: **L11 rack assembly** | House **GW 4.6 → 7.75**; capex **$183bn → $310bn**. **Neither house nor BBG has a 2028.** | CY26 capex **$200.8bn** → CY27 **$310.2bn** | 🟡 **The house 2027 capex is dead on consensus; house 2026 sits $18bn below — and the constraint binds in a year neither model covers.** Fubon's target implies the GW ladder **roughly doubles again** in 2028 with capex to match. **Third supply gate is new to the page:** L11 TPU rack assembly — Hon Hai learning-curve-limited, takes the V8 rack in 2027, Google needs more ODMs for 2028 (page previously had only wafer + packaging gates). The *"supply-constrained yet selling TPUs externally"* tension is **recorded as unanswered** — Fubon defers to TSMC management's overbooking line rather than answering from his own checks. |

---

## CONFIRMS (no action)

| Name | Datapoint | Baseline | Read |
|---|---|---|---|
| **TSM** | 2026 capex **$60-64bn** guided | BBG CY2026 **$62.0bn** | Dead centre — and the anchor that calibrated FX (method flag 3). |
| **TSM** | House vs consensus, **ADR basis corrected** | House 2026 **NT$512.5/ADR** vs BBG **NT$519.71** (**-1.4%**); 2027 **NT$717.5** vs **NT$710.39** (**+1.0%**) | In line both years. Revenue $165bn vs $172bn (-4%); GM 66% vs 66.1%. ⚠️ Naive (un-×5) comparison shows a spurious ~5× gap — see method flag 2. |
| **TSM** | CoWoS **180K wpm end-2027 / 220K wpm 2028** | Prior Fubon forecast | **Restated maintained** — no revision. Upside skew flagged (ASIC expansion slowed to prioritise CoWoS). |
| **AAPL** | Revenue | House $480bn/$539bn vs BBG $486bn/$536bn | Within **1.3%** both years — which is precisely why ① is a margin finding, not a revenue one. |
| **MEDIATEK** | CY27 revenue **+73.0%**, GM **-1.4pt** | BBG | The Street is **not** missing the TPU ramp or its dilutive mix — only, possibly, its margin (see ⑦). |
| **AMD** | 300K wafers 2027 allocation, majority from ASE | BBG CY27 rev **+59.0%** | Reconfirmed unrevised. Counterweight recorded: TSMC **N2/N3 "very, very tight" in 2027** and Venice is an N2 part — **packaging relief ≠ ramp relief.** |
| **AMZN** 📌long | Trainium **1.6-1.7mn → ~3mn** (total, chip-production basis) | Page's UBS **Trainium3 unit-demand** 1.8mn / 2.8mn | **Different scope, ~10% apart → independent corroboration**, both bases labelled. BBG capex **+31.5%**. |
| **NVDA** 📌long | "Intel a must by 2028"; 8.2→12.4mn output; 30-35mn compute dies; 12-15mn 2028 TPU target | Prior wiki | Reconfirmed **verbatim, unrevised**. |
| **Memory / servers** | ODM check: **no 2027 memory spec change at Nvidia, Google or AWS**; cutting the module *"would very seriously impact AI server performance"* | The live memory-content bear | **Direct rebuttal.** ODM purchasing teams have *raised* capex to fund GPU buy-and-sell. |
| **tokenmaxxing** | **$0.171/M** input self-served on B300 vs **$0.74/M** blended on Moonshot (**-76.89%**); OpenRouter floor **$3/$15** | Prior SemiAnalysis benchmarks | Providers pricing **an order of magnitude above cost**. ⚠️ Benchmark basis changed (8k1k/1k1k synthetic → **recorded Claude Code traces**, median 142k in / 444 out, 65 turns/session) — **older cost-per-token figures are not like-for-like.** |
| **ARM** | TER structurally stronger at Arm-based server CPUs than x86 | — | Qualitative only; **Sinal deliberately unchanged.** Arcuri's server-TAM figures in that exchange were ASR-garbled and **dropped, not used**. |

_No private names (ANTHROPIC / OPENAI) carried new quantitative datapoints this run._

---

## Open items carried forward

1. 🔴 **Re-mark the TER house block.** Root-caused broken on 2026-08-01, still un-remarked. Every "house vs consensus" edge shown for TER remains an artefact.
2. 🔴 **Bridge or re-mark the AAPL house margin** (①) — a live long, +14.5% above MS on FY26 EPS at matched revenue.
3. 🔴 **Log in to Bloomberg / reconnect VPN and re-run `/wiki-consensus`** — resolves the PENDING live pull and supplies the `BEST_TARGET_PRICE` line missing from this whole run.
4. 🟠 **Extend the GOOG house model to 2028** (⑫) — the constraint Fubon identifies binds in a year neither the house nor consensus covers.
5. 🟠 **Fix the ingest ordering problem** (structural finding) — desk relays are landing ahead of primaries and being treated as authoritative.
6. 🟡 **Resolve the MEDIATEK $15k content basis** (⑦) — chip revenue vs system/rack content decides whether 2028 is $35-52bn or $60-75bn.
7. 🟡 **Unresolved and deliberately left visible:** the HBM4 step year (2026 vs 2027, inside one source); Rubin Q3 200-300K vs 300-400K; AVGO at Samsung Foundry; TER's "memory/SOC at parity" vs "memory a strain into 2027"; Intel EMIB ~75% vs the DIGITIMES "yields hit target" headline.
8. ℹ️ **Two ASR names never resolved** and deliberately not guessed: `"Seasam"` (a Taiwanese adv-packaging supplier spanning CoWoS/EMIB/fan-out/next-gen CoWoS — a desk relay of the identical sentence renders it "C SUN", **plausible, not claimed**) and `"Weichuang"` (a Taiwanese ODM).
