# Reconciliation — 2026-07-27 (/run-inbox)

_Every NEW quantitative datapoint from this run, placed against three baselines. Split into **DIVERGES (the alpha)** and **CONFIRMS (no action)**._

**Sources reconciled (5):** Bernstein · Newman "Apple Deep Dive" (2026-03-03, backfill) · The Information "China Starts Mass-Producing Homegrown DUV" (2026-07-27) · Morgan Stanley · Woodring "HDDs F4Q26 Preview: Reigniting The Bull Case" (2026-07-27) · UBS · Lin/Abrams/Arcuri "Can Intel challenge TSMC's advanced packaging leadership?" (2026-07-27) · UBS · Keirstead "Microsoft — Update on Azure, Capex and M365" (2026-07-26).

## Baselines used
1. **Prior wiki comments** — on-disk, per page (intra-quarter tables, "where the sell-side stands", `## Changelog`).
2. **Capstone house models** — `_data/house.json`, asof 2026-07-27. Covers 5 of this run's names: **AAPL, AVGO, GOOG, NVDA, TSM**. No house model for STX, WDC, MSFT, INTC, ASML, SMIC, MEDIATEK, TOKYOELEC, ORCL, AMZN.
3. **BBG consensus** — ⚠ the live wrapper (`E:\bloomberg_api`, `bdp`) returned **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal."** However `_data/estimates.json` carries a **same-day snapshot, asof 2026-07-27, 97 tickers**, fetched earlier today at 18:35. That snapshot is used throughout. **No web data was substituted for consensus.** The only genuinely missing field is `BEST_TARGET_PRICE` (not in the snapshot schema) — consensus-PT comparisons below come from the broker notes' own cited means and are labelled as such.
   Private names (**ANTHROPIC, OPENAI**) have no BBG/house — reconciled vs prior wiki comments only.

Note on basis: BBG periods here are **calendar** (CY2026/CY2027); several brokers quote **fiscal** years (MSFT Jun, AVGO Oct, AAPL Sep, STX/WDC Jun). Where the two are mixed the row is tagged **BASIS** and screened out of the alpha column.

---

## Where the new data DIVERGES

| Name | New datapoint (this run) | vs prior wiki | vs house model | vs BBG consensus | Read |
|---|---|---|---|---|---|
| **STX** | ⭐ **MS · Woodring: PT $1,035** (20.0x CY27 EPS **$51.67**); bull $1,446 / bear $490; OW, Top Pick (2026-07-27) | Last published MS mark was **$582** (bull $796), 2026-04-06 → a **+78% PT revision** in <4 months. Moved to Changelog | **No STX house model** — a gap on a name printing 7/28 | CY27 cons EPS **34.62**, Street high **44.33** → MS is **+49% vs cons and +17% ABOVE the highest estimate on the Street**. Yet PT $1,035 is only **+6%** vs the note's cited cons PT mean $979.05. Spot $816.99 | **The Street's PTs already discount earnings its own estimates don't carry.** Either estimates rise toward the PTs or the PTs are unsupported; the checks (300-400EB/yr shortfall through CY28, 2032 CSP visibility, $25-30/TB) point at the estimate side. **Largest gap in the batch. Build the house model before the print.** |
| **WDC** | ⭐ **MS · Woodring: PT $650** (20.0x CY27 EPS **$32.29**); bull $920 / bear $322; OW (2026-07-27) | Last published MS mark **$380** (bull $519), 2026-04-06 → **+71%**. Moved to Changelog | **No WDC house model** | CY27 cons EPS **23.19**, high **38.33** → **+39% vs cons**, inside the high. PT vs cited cons mean $615.15 = **+6%**. Spot $497.92 | Same structural setup as STX but less extreme — MS stays inside the Street high here. **STX carries the asymmetry; WDC confirms the direction.** New company-sourced leg: WDC mgmt sees "an opportunity" for $/TB growth to reach **teens % Y/Y** vs +9% in March |
| **INTC** | UBS Neutral, **PT $121**, implied **CY26 EPS $1.42** / CY27 $1.96 (back-solved from stated 70.4x / 51.1x at $100) | Page carried UBS Neutral/$121 already (07-26 Outlook preview); the implied EPS is net-new | No INTC house model | CY26 cons **$1.00**, high **$1.30** → UBS **+42% vs cons, +9% ABOVE the Street high**. CY27 $1.96 vs cons $2.01 = in line. PT vs spot $91.67 = **+32%** | **Rating-vs-numbers tension:** a Neutral rating carrying a +32% target and an above-high near-year estimate. ⚠ **PARTIAL** — EPS is derived from a P/E, not printed. Press the analyst on why this is Neutral |
| **MEDIATEK** | ⭐ UBS Buy, **PT NT$6,500**, implied **CY27 EPS 181.2** (from 20.7x at NT$3,750) | Page carried Buy/NT$6,500; the implied EPS and the v9-prototype yield evidence are net-new | **No MEDIATEK house model** | CY27 cons **132.54**, high **183.96** → **+37% vs cons, effectively AT the Street high**. CY26 63.9 vs cons 65.33 = in line | **The whole divergence is the Google TPU v9 ramp, and it is past design-intent** — UBS's ~90% EMIB-T packaging yield is measured on **trial production runs of MediaTek's v9 prototype**. Two dependencies outside MediaTek's control: Ibiden's ¥220bn Gama plant only reaches MP late-2027 (and Google TPU demand alone "could largely absorb" it), and EMIB-T *substrate* yields are ~50% vs >80% for HPC ABF. **Consensus CY27 may be 37% too low, untested by any house view** |
| **MSFT** | ⭐ **Microsoft's own capex guide decomposed:** memory hardware inflation adds **$5bn in 4Q/Jun and $20bn across 2H CY26 → $25bn of the CY26 $190bn guide from memory price alone** | New. `hyperscaler-capex.md` carried an open Jefferies question on what drove the GOOGL raise — this answers it | No MSFT house model | Not decomposed in any consensus line; BBG carries only a single capex number | **≈13% of the guide buys no incremental compute** (derived ratio). The wiki's canonical **"$1.4trn 2028 hyperscaler capex"** frame (MS · Nowak, 2026-07-12) does **not** split price from capacity, so every capex→GW inference on the wiki silently assumes capex ≈ capacity. A material slice lands on **[[MU]] / [[SKHYNIX]] / [[SAMSUNG]]** revenue instead. **Most re-usable number in the batch. Not additive to the $1.4trn frame** |
| **MSFT** | UBS **cuts PT $510 → $480**, holds Buy; FY06/27E EPS 19.49 → **19.26**, FY06/28E 22.68 → **22.12**; FY27 capex $234b → **$261b** | PT/capex marks already on page from the 07-26 preview — enriched, not re-entered. **Azure Signal-vs-gestão moved ✓ confirma → ⚠ nuança** | No MSFT house model | UBS-cited cons FY27 **19.40** / FY28 **22.78** → UBS is **below consensus on both out-years**. PT vs BBG spot $389.10 = +23% | **Only PT cut in a batch of four raises, and the rating is held anyway.** The substance is the balance sheet: equity FCF yield **2.4% → 0.1%** in FY06/27E; net cash 51,414 → 49,906 → **1,299** → **net debt (13,408)** by FY28E. First source on the page to date Microsoft going net-debt. ⚠ **BASIS:** the $261bn is **all-in = $209.0bn cash P&E + $51.6bn capital leases**, so it is *not* like-for-like with the $230-235bn sell-side consensus or BofA's $243.5bn bogey |
| **SMIC** | Named 2026 recipient of domestic immersion-DUV tools; CEO Zhao Haijun (May call): overseas customers want China capacity "because capacity was tight elsewhere" | Page had the Match Act and the multiple-patterning history; the tool-delivery + demand-offset legs are net-new | No SMIC house model | Consensus capex **CY2026 $7.96bn → CY2027 $6.70bn = −16%** | **A 16% capex step-down is inconsistent with a fab adding tools, qualifying a new domestic supplier and fielding overflow demand.** Flag the SMIC CY27 capex line as the number in this batch most likely to be wrong-footed |
| **ASML** | MATCH Act would widen restrictions to immersion DUV **and curb servicing** at some Chinese fabs; China domestic output ~5 tools 2026 / ~20 in 2027 | Story already on page via a same-day **Jefferies · Beavington** relay. Net-new: the **131-unit base rate**, the four qualification gates, domestic EUV "years away", the **servicing** leg, ~10% China price rises. ⚠ Jefferies named Yuliansheng as the *manufacturer*; the primary source leaves it unnamed | No ASML house model | CY26 rev €42.6bn / CY27 €55.99bn (+31%) — **5 tools vs 131 shipped is immaterial inside the estimate window** | **Size the tool story down, and move the attention to the annuity.** The servicing curb attacks the installed-base service/upgrade line — carried in no CY26/27 consensus number, and un-backfillable by 5-20 domestic units/yr. Relevant against ING's standing ~1%-of-revenue service-licence estimate. **Watch the service line, not the China tool line** |
| **AAPL** | Bernstein (2026-03-03, backfill): iPhone BOM **+~25%**; 12GB DRAM line **$28.93 → $114.00 (+294%)**, memory ~5% → ~16-17% of BOM; FY27 scenario grid **$11.43 / $10.28 / $9.54 / $8.81** | Bernstein mark moves **$290 (2025-09-15) → $340 (2026-03-03)**, flagged in-page as a **stale mark, not current**. PT $340 vs BBG spot **$336.91** → ~1% from fully realised in <5 months | **House 2026E EPS 10.12 / rev $480bn** | CY26 cons EPS **8.89** / rev $488.1bn; Bernstein F26E (FYE Sep) 8.72 / $471.1bn | ⚠ **BASIS** (fiscal-Sep vs calendar). Even after the shift, **house EPS is ~14% above consensus** — pre-existing, not created by this run — and sits between Bernstein's S1 and S2, i.e. the house implicitly underwrites a **benign memory-cost outcome**. Bernstein's BOM work is the sharpest available bear input. **Action: run the house model against the S3/S4 legs** |

_(No `## BBG consensus pull` table this run: the live wrapper is down and the on-disk snapshot schema carries no `BEST_TARGET_PRICE`. Consensus-PT figures above are the broker notes' own cited means, labelled as such. Re-run when the Terminal is back rather than substituting another source.)_

---

# Detail — the alpha items in full

## 1. STX / WDC — Morgan Stanley's out-year EPS is above the Street, but its PT is not
| | MS base CY27 EPS | BBG CY27 cons | BBG CY27 high | MS vs cons | MS vs high |
|---|---|---|---|---|---|
| **STX** | **$51.67** (PT $1,035 = 20.0x) | 34.62 | 44.33 | **+49%** | **+17% ABOVE the Street high** |
| **WDC** | **$32.29** (PT $650 = 20.0x) | 23.19 | 38.33 | **+39%** | −16% (inside the high) |

PTs vs the note's own cited consensus means: STX $1,035 vs $979.05 (**+6%**); WDC $650 vs $615.15 (**+6%**). BBG spot 2026-07-27: STX $816.99, WDC $497.92.

**The finding.** Morgan Stanley's STX CY27 EPS is **higher than the highest estimate on the Street**, yet its price target is only 6% above the consensus PT mean. That is an internal contradiction in the Street's own positioning: PTs already discount earnings power the estimates do not carry. Either the estimates rise toward the PTs, or the PTs are unsupported. Given the checks all point one way (300-400EB/yr shortfall through CY28, CSP visibility to 2032, $25-30/TB CY27-28 discussions), **the estimate side is the likelier adjuster, and STX carries the larger gap.**

**Prior-wiki baseline:** the page's last published MS marks were **STX $582 / WDC $380 (2026-04-06)** — so this is a **+78% / +71% PT revision** in under four months. Both old values moved to `## Changelog`.

**Caveat (do not lose):** the note is internally inconsistent — STX's base-case box says 18.0x while the PT line says 20.0x (only 20.0x ties to $1,035); WDC's PT header quotes CY27 EPS $27.12 vs the base-case box's $32.29 (only $32.29 ties to $650). The table above uses the readings that tie to the printed PTs.

**No house model for either name.** Two names now carrying a Street-high-beating sell-side call, a 49%/39% consensus gap and no house view to test it. **Highest-priority model build coming out of this run.**

## 2. STX / WDC — the advertised margin edge is roughly half what the note claims
| Sept-26 qtr | MSe | BBG cons | MS-cited cons | MSe vs BBG |
|---|---|---|---|---|
| STX GM | 53.2% | **51.9%** | 49.9% | **+130bps** (note claims +330bps) |
| WDC GM | 55.3% | **53.7%** | 51.8% | **+160bps** (note claims +350bps) |
| STX EPS | $6.11 | 5.805 (hi 6.71) | 5.84 | +5.3%, **below** the Street high |
| WDC EPS | $3.96 | 3.804 (hi 4.66) | 3.78 | +4.1%, **below** the Street high |
| STX rev | $3,806M | 3,791.9 (hi 4,157) | 3,782 | +0.4% |
| WDC rev | $4,046M | 4,006.8 (hi 4,411) | 4,027 | +1.0% |

MS derives its "consensus" $/TB as consensus revenue ÷ **MSe** EB shipments, which drags its consensus GM ~200bps below the actual BBG median. **Against real consensus the near-term edge is +130/+160bps, and MSe EPS sits *below* the Street high in both names and both quarters.** The buy-side bar into the 7/28 print is higher than the note's framing implies — which is the risk to MS's own "pounding the table" stance, not support for it. The out-year call (item 1) is where the asymmetry actually lives.

## 3. INTC — UBS's implied CY26 EPS is above the Street high
UBS Figure 1: Neutral, **PT US$121**, price US$100 (23 Jul), 2026E P/E **70.4x**, 2027E **51.1x** → implied EPS **$1.42 (CY26E)** and **$1.96 (CY27E)**.

| | UBS implied | BBG cons | BBG high | vs cons | vs high |
|---|---|---|---|---|---|
| CY2026 EPS | **$1.42** | 1.00 | 1.30 | **+42%** | **+9% above** |
| CY2027 EPS | $1.96 | 2.01 | 3.52 | −2% | inside |

**DIVERGES on 2026 only** — and note UBS holds **Neutral** while carrying a well-above-consensus near-year number, with PT $121 vs BBG spot $91.67 (+32%). A Neutral rating with a +32% target and an above-high estimate is a rating-vs-numbers tension worth pressing. ⚠ Tag **PARTIAL**: the EPS is back-solved from a stated P/E at a stated price, not printed directly.

## 4. MEDIATEK — UBS's CY27 EPS is at the Street high, and the TPU call is why
UBS Figure 1: Buy, **PT NT$6,500**, price NT$3,750 (24 Jul), 2026E P/E 58.7x, 2027E **20.7x** → implied EPS **63.9 (CY26E)** / **181.2 (CY27E)**.

| | UBS implied | BBG cons | BBG high | vs cons |
|---|---|---|---|---|
| CY2026 EPS | 63.9 | 65.33 | 82.73 | −2% (in line) |
| CY2027 EPS | **181.2** | 132.54 | 183.96 | **+37%, at the Street high** |

The entire divergence sits in 2027 and is the **Google TPU v9 ramp**. What makes this more than a forecast: UBS's ~90% EMIB-T packaging yield is measured **on trial production runs of MediaTek's v9 prototype** — v9 silicon has already been through EMIB-T, so this is past design-intent. Against that, two dependencies MediaTek does not control: Ibiden's ¥220bn Gama plant reaches MP only late-2027, and UBS says Google TPU demand alone "could largely absorb the planned capacity"; and EMIB-T **substrate** yields are ~50% vs >80% for HPC ABF. **No house model for MEDIATEK** — a name whose consensus 2027 EPS could be 37% too low, untested.

## 5. MSFT — Microsoft's own capex guide is ~13% memory price, not capacity
The single most re-usable number in the batch. Microsoft signalled two drivers behind the CY26 **$190bn** capex guide: compute demand, and **memory hardware inflation — worth $5bn in 4Q/Jun and $20bn across 2H CY26, a full-year CY26 boost of $25bn from memory inflation alone.**

$25bn / $190bn ≈ **13% of the guide buying no incremental compute** (derived ratio, not a printed figure).

**Why it diverges:** the wiki's canonical frame — "$1.4trn 2028 hyperscaler capex" (MS · Nowak, 2026-07-12), in `_meta/assumptions.md` — does **not** decompose price from capacity. Every GW-per-capex and capex-implies-demand inference on the wiki silently assumes capex ≈ capacity. This says a material slice of the 2026 step-up lands on **[[MU]] / [[SKHYNIX]] / [[SAMSUNG]] revenue**, not on GW deployed. It also directly answers the open Jefferies question on `hyperscaler-capex.md` about what drove the GOOGL raise. **Action: carry the price/capacity split into the GW assumptions; do not add this to the $1.4trn frame (not additive).**

## 6. MSFT — below-consensus out-year EPS while holding Buy
| | Prior UBS | New UBS | UBS-cited cons | vs cons |
|---|---|---|---|---|
| FY06/26E EPS | 16.95 | 16.95 | 16.80 | +0.9% |
| FY06/27E EPS | 19.49 | **19.26** | 19.40 | **−0.7%** |
| FY06/28E EPS | 22.68 | **22.12** | 22.78 | **−2.9%** |
| PT | $510 | **$480** | — | vs BBG spot $389.10 = +23% |

Rating held at Buy while cutting the PT 6% and taking both out-years **below** consensus — the only PT cut in this batch, against four raises. The balance-sheet path is the substance: **equity FCF yield 2.4% → 0.1% in FY06/27E**, net cash 51,414 (FY25) → 49,906 (FY26E) → **1,299 (FY27E)** → **net debt (13,408) (FY28E)**. UBS is the first source on the page to put a *date* on Microsoft going net-debt.

## 7. SMIC — a CY27 capex step-down that sits against everything else in the file
BBG consensus capex: **CY2026 $7.96bn → CY2027 $6.70bn (−16%)**.

Against that: SMIC is a **named 2026 recipient** of domestic immersion-DUV tools; CEO Zhao Haijun said on the May call that **overseas customers want to fab in China because capacity is tight elsewhere**; and SMIC is running multiple patterning on immersion DUV to make advanced smartphone/AI parts without EUV. A 16% capex decline is inconsistent with a fab adding tools, qualifying a new domestic supplier, and fielding overflow demand. **Flag the SMIC CY27 capex line as the number in this batch most likely to be wrong-footed.** No house model.

## 8. ASML — the exposure is the service annuity, and it is not in any estimate
Sizing first, because the headline overstates it: **~5 domestic DUV tools in 2026 and ~20 in 2027 vs the 131 immersion DUV systems ASML shipped last year** = ~4% and ~15% of a single year's output, and only if every unit qualifies (the article says insertion "could take many months or longer"). Against BBG CY2026 revenue €42.6bn / CY2027 €55.99bn (+31%), the domestic tool is **immaterial inside the estimate window → CONFIRMS on numbers.**

The divergence is structural and out-of-model: the **MATCH Act** would widen restrictions to immersion DUV **and curb servicing of tools at some Chinese fabs**. That attacks the **installed-base service/upgrade annuity**, which no CY26/27 consensus line carries, and which ~5-20 domestic units a year cannot backfill. Relevant against ING's standing ~1%-of-revenue service-licence estimate already on the page. Offsets, both real: ASML has already taken **~10% price increases** from several Chinese customers on less-advanced DUV lines, and China capacity is tight. **Watch the service line, not the China tool line.**

## 9. AAPL — the house model is 16% above consensus, and this note is the best available stress test
| | Bernstein F26E (FYE Sep) | BBG CY2026 | House 2026E |
|---|---|---|---|
| EPS | 8.72 | 8.89 | **10.12** |
| Revenue | $471.1bn | $488.1bn | **$480bn** |

**BASIS**: fiscal-Sep vs calendar differ by a quarter. Even after that shift, **house EPS 10.12 is ~14% above consensus and ~16% above Bernstein's mark.** That gap is **pre-existing, not created by this run** — but Bernstein's BOM work is now the sharpest bear input available to test it: the 12GB DRAM line going **$28.93 → $114.00 (+294%)**, memory moving from ~5% to ~16-17% of BOM, a **~25% total iPhone BOM increase**, and a four-scenario FY27 grid spanning **$11.43 / $10.28 / $9.54 / $8.81** (+22.9% / +10.5% / +2.6% / −5.3% vs consensus). The house 2026E of 10.12 sits between Bernstein's S1 and S2 — i.e. the house is implicitly underwriting a **benign-to-good** memory-cost outcome. **Action: run the house model against Bernstein's S3/S4 legs.**

**Scored forecast (backfill payoff):** Bernstein set **PT $340 on 2026-03-03**; BBG spot today is **$336.91** — the target is ~1% from fully realised in under five months. The mechanism it called (memory shortage as a *relative share gain* for Apple because low-end Android OEMs cannot secure memory) was subsequently measured by Bernstein's own June tracker: global shipments −11% y/y in Q2'26, Apple share 17% → 20%, the only major OEM to grow. **~5 months of lead time.** Not logged to `outcomes.md` — no discrete catalyst resolved, and the PT was never a wiki-held call.

---

# CONFIRMS — no action

| Name | New datapoint | Baseline | Verdict |
|---|---|---|---|
| **TSM** | UBS implied CY26/27 EPS 108.8 / 148.7 per ordinary share | BBG cons 103.8 / 141.9 (ADR-basis 519.02 / 709.63 ÷ 5); house NT$102.5 / 143.5 | UBS **+4.8% / +4.8%** vs both. House ≈ consensus. In line — no divergence. |
| **TSM** | UBS Buy **PT NT$3,650** (from NT$3,400) | Fubon NT$3,500 (06-05), GS NT$3,000 (07-02) | Now the **Street-high PT on the page**. UBS's own path NT$3,000 → 3,400 → 3,650 = **+22% in nine weeks**. Drift logged; the *rate* of revision is the signal, not the level. |
| **TSM** | Adv-packaging 9% → **18% of sales by 2030E**; AP revenue $16.0bn → $81.4bn | BBG consensus stops at CY2027 | **No consensus counterpart** — thesis input, not a testable divergence. |
| **AVGO** | UBS implied CY26 EPS $11.95 vs BBG CY26 cons $13.59 (−12%) | House 2026E 12.89 / 2027E 21.07 | **BASIS ARTIFACT — screened out.** AVGO's FY ends late Oct; a one-quarter shift on a name compounding ~70% EPS growth explains the whole gap. CY27: UBS $21.66 vs cons $21.17 (+2%), house 21.07. All three agree. |
| **INTC** | EMIB-T revenue $5.4 / 9.6 / 15.8bn (2028-30E); Google TPU $5.0 / 8.4 / 13.2bn of it | BBG stops at CY2027 | Unfalsifiable inside the estimate window → thesis, not alpha. ⚠ These are **US$mn of revenue, not units**. |
| **GOOG** | Google Cloud 2Q26 **+82%** | Reported quarter (lrq 2026-06-30) | CONFIRMS the accelerating-cloud leg. Load-bearing use: it is **counter-evidence to the token-optimization drag**, carried with UBS's own caveat that optimized spend concentrates in coding "for which Gemini models are less dominant". |
| **GOOG** | Capex to be raised again | BBG CY26 $197.8bn / CY27 $295.4bn; house $183bn / **$310bn**, FCF −$3bn / **−$55bn** | House is below cons on 2026 and **above on 2027**. UBS's direction cuts **toward** the house 2027 number. CONFIRMS house. |
| **TOKYOELEC** | Named in 3 CoPoS tool steps (depo/RDL, debonding, CMP); square-panel needs "an entirely new toolset" | BBG CY26 ¥3,081bn → CY27 ¥3,997bn (**+30%**) | Incremental optionality already inside a +30% consensus. Kept honest both ways: TEL is **absent from the EMIB-T supply chain entirely** and is not the share-gain name in the CoPoS steps UBS singles out. |
| **AVGO** | UBS Buy PT $485 confirmed current | BBG spot $383.22 | Confirmed not a stale carry. The note models **no AVGO volumes, share or ASIC economics** — nothing extrapolated. |
| **STX/WDC** | 300-400EB/yr shortfall through CY28; 2032 CSP visibility; $25-30/TB CY27-28 | BBG CY2027 already at STX GM 57.2% / EPS 34.62; WDC GM 58.6% / EPS 23.19 | Consensus has **already underwritten** a version of the tight world MS argues toward. The checks confirm the direction; they are not new information to the CY27 line. |
| **hbm-memory** | eSSD $0.60-0.70/GB vs HDD ~$0.015/GB = **17-20x**, widening to **>20x exiting CY26**, vs a ~3x substitution threshold | Prior wiki NAND-substitution framing | CONFIRMS — eSSD substitution risk into nearline is receding, not advancing. ⚠ Correction: an earlier framing in this run said the gap had *narrowed from ~25x*; the source says it is **widening**. |
| **ORCL / AMZN** | UBS: "AI capex/revs are **not** landing at the abysmal margin levels the bears feared" | Redburn SELL on ORCL; Redburn $230 margin short on AMZN | Directly contests both. Attributed and carried; no number to reconcile. |
| **ANTHROPIC / OPENAI** | Claude Cowork native inside Copilot; OpenAI down-tiering ("OpenAI Mini for 90% of what I do") | Prior wiki comments only (private names) | No BBG/house by construction. The OpenAI reframe is material: near-term risk is **down-tiering inside OpenAI's own ladder**, not defection to open models. |

---

# Actions falling out of this run

1. **Build STX and WDC house models.** Two names with a fresh Street-high-beating call, a 49%/39% CY27 consensus gap, PTs revised +78%/+71%, and a print on **7/28** — with no house view. Most urgent item here.
2. **Stress the AAPL house model (EPS 10.12) against Bernstein's S3/S4 memory-cost legs** ($9.54 / $8.81). The house is ~14% above consensus and implicitly assumes a benign memory outcome.
3. **Split price from capacity in the hyperscaler-capex assumptions.** Microsoft's own guide says $25bn of a $190bn CY26 number is memory inflation. Every capex→GW inference on the wiki currently assumes capex ≈ capacity.
4. **Watch ASML's service line, not its China tool line.** The MATCH Act servicing curb is the exposure no estimate carries.
5. **Question the SMIC CY27 capex consensus (−16%).** Inconsistent with the tool-delivery and tight-capacity evidence.
6. **Build a MEDIATEK house model** — consensus CY27 EPS may be ~37% too low if the TPU v9 ramp lands.
7. **Re-run this reconciliation's BBG column live once the Terminal is back**, to pick up `BEST_TARGET_PRICE` (absent from the snapshot schema) and confirm the same-day figures.

_Standing coverage gaps carried forward from 2026-07-24: no house model for AMD, MU, SKHYNIX, SAMSUNG, CRWV, ORCL, MRVL, ANET, SNPS, CDNS, AMZN. The GOOG house-vs-consensus 2026 basis gap remains open and is unrelated to this run._
