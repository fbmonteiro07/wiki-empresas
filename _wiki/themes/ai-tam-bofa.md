<!-- Cross-company THEME page — BofA "AI 2030" TAM framework. Scaffold built to plug Capstone accelerator estimates into BofA's structural ratios. Buy-side voice. -->

# Theme — AI Data-Center TAM (BofA "AI 2030" framework)

_Wiki · generated 2026-06-30 · cross-company theme · scaffold for cross-checking the BofA top-down TAM against Capstone bottoms-up estimates. Source exhibit: BofA (Vivek Arya) "AI 2030: Stronger for Longer", 2026-05-13 ([HTML](../../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html)). Company pages: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md)._

## What it is / why it matters
BofA's "AI 2030" note sizes the **AI data-center systems TAM at ~$1.7Tn by CY30** (from $23bn in 2022, ~45% CAGR), broken into servers (accelerators / HBM / CPUs), networking (switching / SmartNIC / optical / copper) and storage. This page exists for one purpose: **to make that top-down TAM a fill-in engine for Capstone's own bottoms-up work.** The key structural fact is that every line in BofA's exhibit moves in a near-fixed ratio to **AI Accelerators** — so once we plug in *our* accelerator estimate (GPU + custom ASIC), the rest of the TAM (HBM, networking, optical, storage…) drops out of BofA's ratios, and any line where our view diverges from BofA's becomes the explicit debate. The buy-side value: it turns a static sell-side exhibit into a cross-check — where is BofA too high/low vs our names, and is the dollar TAM even *supply-feasible* given the InP/HBM/cleanroom constraints our expert calls flag.

> **Status: scaffold.** The Capstone accelerator estimates are pending (Felipe finalizing). The fill-in section below is wired with BofA's multipliers and ready to receive them. **TODO:** drop our accelerator $ per year → auto-populate the implied TAM → flag divergences.

## 1) Source exhibit — BofA absolute TAM ($bn)

| TAM ($bn) | 2022 | 2023 | 2024 | 2025 | 2026E | 2027E | 2028E | 2029E | 2030E | CAGR '25-'30 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Overall IT Spend | 4,594 | 4,693 | 5,039 | 5,564 | 6,316 | 6,985 | 7,468 | 8,086 | 8,726 | 9% |
| Data Center Systems TAM | 227 | 238 | 334 | 506 | 772 | 1,126 | 1,490 | 1,796 | 2,041 | 32% |
| **AI Data Center Systems TAM** | **23** | **63** | **160** | **264** | **548** | **866** | **1,192** | **1,482** | **1,706** | **45%** |
| &nbsp;&nbsp;_AI % of Overall IT Spend_ | 0.5% | 1.3% | 3.2% | 4.7% | 8.7% | 12.4% | 16.0% | 18.3% | 19.5% | |
| &nbsp;&nbsp;_AI % of DC Systems TAM_ | 10.1% | 26.6% | 48.0% | 52.2% | 70.9% | 76.9% | 80.0% | 82.5% | 83.6% | |
| **AI Servers** | 16.3 | 49.5 | 130.4 | 216.0 | 425.1 | 673.6 | 927.9 | 1,144.8 | 1,308.5 | 43% |
| &nbsp;&nbsp;AI CPUs | 1.2 | 2.1 | 4.0 | 9.3 | 24.5 | 40.8 | 58.6 | 72.5 | 87.6 | 57% |
| &nbsp;&nbsp;**AI Accelerators** | 14.3 | 45.0 | 120.2 | 196.5 | 381.1 | 603.2 | 830.1 | 1,026.1 | 1,170.6 | 43% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ HBM | 1.6 | 4.2 | 17.4 | 34.5 | 76.8 | 105.5 | 120.5 | 139.9 | 168.3 | 37% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Other (DDR/SSD/mb/power) | 0.8 | 2.4 | 6.2 | 10.3 | 19.5 | 29.6 | 39.1 | 46.1 | 50.3 | 37% |
| **AI Networking** | 5.6 | 10.4 | 21.6 | 34.6 | 95.3 | 150.8 | 207.5 | 266.8 | 316.1 | 56% |
| &nbsp;&nbsp;AI Switching | 2.2 | 4.6 | 8.8 | 12.5 | 30.9 | 52.6 | 71.2 | 103.9 | 128.7 | 59% |
| &nbsp;&nbsp;AI SmartNIC | 0.9 | 2.0 | 3.3 | 4.8 | 23.5 | 39.7 | 59.0 | 68.7 | 77.6 | 75% |
| &nbsp;&nbsp;**AI Connectivity/Other** | 2.5 | 3.8 | 9.5 | 17.4 | 40.9 | 58.5 | 77.4 | 94.2 | 109.8 | 45% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Optical | 1.9 | 3.4 | 8.6 | 15.3 | 35.8 | 49.5 | 62.3 | 76.0 | 87.7 | 42% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Electrical/Copper | 0.6 | 0.4 | 0.9 | 2.1 | 5.1 | 9.0 | 15.1 | 18.2 | 22.1 | 61% |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;· DAC | 0.5 | 0.4 | 0.5 | 0.8 | 1.3 | 1.8 | 2.1 | 2.4 | 2.6 | 26% |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;· ACC | 0.0 | 0.0 | 0.0 | 0.0 | 0.4 | 1.2 | 2.1 | 3.1 | 6.0 | 180% |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;· AEC | 0.1 | 0.1 | 0.2 | 1.2 | 3.4 | 6.0 | 10.9 | 12.8 | 13.6 | 62% |
| **AI Storage** | 1.1 | 3.2 | 8.2 | 13.5 | 27.3 | 41.2 | 56.8 | 70.6 | 81.2 | 43% |
| Non-AI Data Center TAM | 204.1 | 174.4 | 173.3 | 241.5 | 224.8 | 260.7 | 298.1 | 314.1 | 335.7 | 7% |

_The copper sub-rows (DAC/ACC/AEC) are transcribed from a lower-resolution part of the exhibit — treat as approximate; they sum to ~the Electrical/Copper line. Confirm against the PDF before quoting._

## 2) Composition — each line as % of AI Data Center Systems TAM

| Subtopic | 2022 | 2023 | 2024 | 2025 | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **AI Servers** | 70.9% | 78.3% | 81.4% | 81.8% | 77.6% | 77.8% | 77.8% | 77.2% | 76.7% |
| &nbsp;&nbsp;AI CPUs | 5.2% | 3.3% | 2.5% | 3.5% | 4.5% | 4.7% | 4.9% | 4.9% | 5.1% |
| &nbsp;&nbsp;**AI Accelerators** | 62.2% | 71.2% | 75.0% | 74.4% | 69.6% | 69.7% | 69.6% | 69.2% | 68.6% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ HBM | 7.0% | 6.6% | 10.9% | 13.1% | 14.0% | 12.2% | 10.1% | 9.4% | 9.9% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Other (DDR/SSD/power) | 3.5% | 3.8% | 3.9% | 3.9% | 3.6% | 3.4% | 3.3% | 3.1% | 2.9% |
| **AI Networking** | 24.3% | 16.5% | 13.5% | 13.1% | 17.4% | 17.4% | 17.4% | 18.0% | 18.5% |
| &nbsp;&nbsp;AI Switching | 9.6% | 7.3% | 5.5% | 4.7% | 5.6% | 6.1% | 6.0% | 7.0% | 7.5% |
| &nbsp;&nbsp;AI SmartNIC | 3.9% | 3.2% | 2.1% | 1.8% | 4.3% | 4.6% | 4.9% | 4.6% | 4.5% |
| &nbsp;&nbsp;**AI Connectivity/Other** | 10.9% | 6.0% | 5.9% | 6.6% | 7.5% | 6.8% | 6.5% | 6.4% | 6.4% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Optical | 8.3% | 5.4% | 5.4% | 5.8% | 6.5% | 5.7% | 5.2% | 5.1% | 5.1% |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ Electrical/Copper | 2.6% | 0.6% | 0.6% | 0.8% | 0.9% | 1.0% | 1.3% | 1.2% | 1.3% |
| **AI Storage** | 4.8% | 5.1% | 5.1% | 5.1% | 5.0% | 4.8% | 4.8% | 4.8% | 4.8% |

_Sanity check: HBM ÷ Accelerators reproduces BofA's own "HBM % of Accelerators" row (11/9/14/18/20/17/15/14/14%), so the shares tie out to the source._

## 3) The fill-in engine — every line as a multiple of AI Accelerators

This is the workhorse. In the forward years the ratios are remarkably stable, so **Capstone's accelerator estimate × the multiplier ≈ each TAM line** (BofA's implied structure). Override any multiplier where our view differs.

| Line | = Accelerators × … | 2026E | 2027E | 2028E | 2029E | 2030E | Use |
|---|---|--:|--:|--:|--:|--:|---|
| **Total AI DC Systems TAM** | ×total | **1.44** | **1.44** | **1.44** | **1.44** | **1.46** | headline TAM ≈ 1.44 × accelerators |
| AI Servers | ×1.12 | 1.12 | 1.12 | 1.12 | 1.12 | 1.12 | servers incl. accelerators |
| AI CPUs | ×~0.07 | 0.064 | 0.068 | 0.071 | 0.071 | 0.075 | host CPU rack content |
| HBM | ×(% of acc.) | 0.20 | 0.17 | 0.15 | 0.14 | 0.14 | **BofA fades HBM share post-26** |
| Other server (DDR/SSD/power) | ×~0.045 | 0.051 | 0.049 | 0.047 | 0.045 | 0.043 | |
| AI Networking | ×~0.25 | 0.25 | 0.25 | 0.25 | 0.26 | 0.27 | rises into the outer years |
| &nbsp;&nbsp;AI Switching | ×~0.09 | 0.081 | 0.087 | 0.086 | 0.101 | 0.110 | |
| &nbsp;&nbsp;AI SmartNIC | ×~0.067 | 0.062 | 0.066 | 0.071 | 0.067 | 0.066 | |
| &nbsp;&nbsp;Optical | ×~0.075 | 0.094 | 0.082 | 0.075 | 0.074 | 0.075 | |
| &nbsp;&nbsp;Electrical/Copper | ×~0.017 | 0.013 | 0.015 | 0.018 | 0.018 | 0.019 | AEC the growth piece |
| AI Storage | ×~0.069 | 0.072 | 0.068 | 0.068 | 0.069 | 0.069 | most stable line |

**Worked example (using BofA's own 2030E accelerators = $1,170.6bn):** ×1.46 ⇒ ~$1,706bn total ✓; HBM ×0.14 ⇒ ~$168bn ✓; networking ×0.27 ⇒ ~$316bn ✓; optical ×0.075 ⇒ ~$88bn ✓. The engine reproduces the exhibit, so plugging *our* accelerator number is a one-step swap.

## 4) Capstone fill-in (PENDING — paste accelerator estimates here)

Drop our accelerator $ (GPU + custom ASIC, $bn) into the top row; the rest applies the §3 multipliers (edit any cell where we hold a different view). Compare the bottom line vs BofA's ~$1.7Tn and vs the hyperscaler-capex envelope.

| $bn | 2026E | 2027E | 2028E | 2029E | 2030E | vs BofA |
|---|--:|--:|--:|--:|--:|---|
| **AI Accelerators (Capstone)** | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ | BofA: 381 / 603 / 830 / 1,026 / 1,171 |
| → HBM | | | | | | BofA: 77 / 106 / 121 / 140 / 168 |
| → AI Networking | | | | | | BofA: 95 / 151 / 208 / 267 / 316 |
| → Optical | | | | | | BofA: 36 / 50 / 62 / 76 / 88 |
| → AI Storage | | | | | | BofA: 27 / 41 / 57 / 71 / 81 |
| → **Total AI DC TAM** | | | | | | BofA: 548 / 866 / 1,192 / 1,482 / 1,706 |

**Decision points when we fill this:** (1) do we agree HBM share of accelerators *fades* from 20%→14% (BofA), or stays elevated (our hbm-memory corpus leans tighter-for-longer)? (2) is our accelerator GPU/ASIC mix richer in ASIC than BofA's (AVGO 16% share by '30) — which would change networking attach? (3) does our optical number tie to the LITE/COHR/CIEN/GLW bottoms-up, given supply is the gate?

## 5) BofA's accelerator decomposition (sanity-check our total against this)

BofA raised the **accelerator TAM to ~$1.2Tn (from ~$1.0Tn)** on more hyperscaler custom ASIC. The internal split is the right yardstick for our own accelerator estimate:

| Vendor | CY25 | CY26E | CY27E | CY28E | CY30E | Implied share |
|---|--:|--:|--:|--:|--:|---|
| **NVDA** (merchant GPU) | ~$162bn | | | | ~$800bn | 83% → 68% |
| **AVGO** (custom ASIC + attach) | ~$16bn | ~$47bn | ~$90bn | ~$135bn | ~$182bn | 8% → 16% |
| **AMD** (merchant GPU #2) | ~$6.6bn | | | | ~$80bn | ~5–7% |

_Cross-check vs Capstone's own AVGO model ([custom-asic-tpu](custom-asic-tpu.md)): 2026 $115B / 2027 $190B / 2028 $315B total AI rev (incl. networking), GW deployed 4.1→9.9→19.6 (2026-28). Note Capstone's AVGO total is higher than BofA's accelerator-only line because it bundles networking attach._

## 6) BofA "AI 2030" scorecard — what they said per name

| Ticker | Rating | PO (in note) | Basis | Note |
|---|---|---|---|---|
| [NVDA](../NVDA.md) | Buy — **top sector pick** | $300→$320 | — | accel. share 68–77%; AI-DC TAM $1.4Tn→$1.7Tn |
| [AVGO](../AVGO.md) | Buy — **top pick** | $450 | 26x CY27 | ASIC $47/90/182bn CY26/27/30; share 12→16%; networking TAM →$316bn |
| [AMD](../AMD.md) | Buy — **top pick** | $450→$500 | 42x CY27 | GPU $6.6bn'25→$80bn'30E (~5–7% share) |
| [MU](../MU.md) | Buy — **top pick** | $500→$950 (SOTP) | $710 DRAM/NAND 3.1x P/B + $190 HBM 27x PE | _superseded → $1,550 post-F3Q26_; HBM TAM $35→$168bn |
| [MRVL](../MRVL.md) | **upgrade → Buy** | $125→$200 | 30x CY28 | Celestial CPO CY28E ~$901M; FY28/29E EPS $5.60/$7.80 |
| [COHR](../COHR.md) | Neutral | $365→$400 | 41x CY27 | 20–30% transceiver share; 6" InP edge; scale-out CPO lasers 1H27 |
| [LITE](../LITE.md) | Neutral | $1,100 | 48x CY27 | maintained |
| [ALAB](../ALAB.md) | Neutral | $200→$240 | 66x CY27 | risks: Amazon, MRVL/AVGO comp, UALink adoption |
| [CRDO](../CRDO.md) | Buy | $210 | 30x CY27 | _pre-Q4 print_; AEC adoption the swing |
| [ARM](../ARM.md) | Neutral | $140→$245 | 69x CY28 | DC content + AGI-CPU/chiplet optionality |
| [INTC](../INTC.md) | Underperform | $56→$96 | SOTP (IDM $74 37x + foundry $21–22 10x EV/S) | |

## 7) Cross-reference / reconciliation (where BofA meets our corpus)

The TAM is **price × volume and assumes demand is the constraint** — most of our expert calls say *supply* is the gate and part of the dollar growth is ASP melt-up. The high-value checks:

1. **Optical ($88bn '30E, +42% CAGR, ~5% of AI TAM) vs [optical-cpo](optical-cpo.md).** This exact note is the source of the page's "$316bn networking TAM" line. Stack BofA's $88bn top-down against the bottoms-up sub-slices we have (Rothschild CPO ~$15bn + scale-across ~$7bn + OCS ~$6bn by 2030 — leaving the rest as IMDD pluggables). **Feasibility test:** LITE/COHR "sold out into 2028," InP capacity only 2–4x over 3yr, pumps behind 50–60% — is $88bn even *makeable* on units, or is it an ASP story?
2. **HBM ($168bn '30E, +37%) vs [hbm-memory](hbm-memory.md).** Both pages already cite this note (MU SOTP). Back into **implied $/Gb** and compare to TrendForce's live ladder (HBM4 ~$2.05/Gb today → "must hit ~$5/Gb in '27"; NVDA $17–18/GB '26→$30–32 '27). BofA's *own* model fades HBM share of accelerators 20%→14% — i.e. more bearish on HBM duration than our June desks (UBS/MS/TrendForce: tight to mid-2028+). Clean place to take the other side.
3. **Copper/AEC ($22bn, +61%; AEC +62%) vs [CRDO](../CRDO.md) / [ALAB](../ALAB.md) / 650 Group.** Tiny (~1.3% of TAM) but fastest-growing networking slice. With "400G/lane stays copper" now settled (650 Group), BofA's copper line may be *understated* vs CRDO's print (AEC→optical >$600M FY27).
4. **Accelerators ($1.2Tn, ~69% of TAM) vs [custom-asic-tpu](custom-asic-tpu.md).** BofA's NVDA 68% / AVGO 16% split vs JPM's ASIC unit share (42%→53% of units '26→'27) and Capstone's AVGO GW model. Is our accelerator mix more ASIC-heavy than BofA's? That changes the networking attach in §3.
5. **Macro plausibility — AI = 19.5% of all IT spend by '30 vs [hyperscaler-capex](hyperscaler-capex.md).** Does $1.7Tn AI-DC TAM reconcile with the sum of hyperscaler + neocloud + sovereign capex we track?

## Sources
- **Primary:** [BofA (Vivek Arya) — "AI 2030: Stronger for Longer for compute, memory, networking" (2026-05-13)](../../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html). TAM exhibit transcribed above; per-name POs from company pages.
- **Theme cross-refs:** [hbm-memory](hbm-memory.md) (HBM TAM $35→$168bn, MU SOTP, price ladder), [optical-cpo](optical-cpo.md) ($316bn networking TAM, InP supply gate), [custom-asic-tpu](custom-asic-tpu.md) (accelerator $1.0→$1.2Tn, NVDA/AVGO/AMD split), [hyperscaler-capex](hyperscaler-capex.md) (demand envelope), [ai-datacenter-power](ai-datacenter-power.md) (power as the binding constraint).
- **Company pages:** [NVDA](../NVDA.md), [AVGO](../AVGO.md), [AMD](../AMD.md), [MU](../MU.md), [MRVL](../MRVL.md), [COHR](../COHR.md), [LITE](../LITE.md), [ALAB](../ALAB.md), [CRDO](../CRDO.md), [ARM](../ARM.md), [INTC](../INTC.md).
