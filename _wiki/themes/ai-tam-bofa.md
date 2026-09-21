<!-- Cross-company THEME page — BofA "AI 2030" TAM framework. Scaffold built to plug Capstone accelerator estimates into BofA's structural ratios. Buy-side voice. -->

# Theme — AI Data-Center TAM (BofA "AI 2030" framework)

_Wiki · generated 2026-06-30 · cross-company theme · scaffold for cross-checking the BofA top-down TAM against Capstone bottoms-up estimates. Source exhibit: BofA (Vivek Arya) "AI 2030: Stronger for Longer", 2026-05-13 ([HTML](../../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html)). Company pages: [../00_INDEX.md](../00_INDEX.md) · themes index: [00_THEMES.md](00_THEMES.md)._

## What it is / why it matters
BofA's "AI 2030" note sizes the **AI data-center systems TAM at ~$1.7Tn by CY30** (from $23bn in 2022, ~45% CAGR), broken into servers (accelerators / HBM / CPUs), networking (switching / SmartNIC / optical / copper) and storage. This page exists for one purpose: **to make that top-down TAM a fill-in engine for Capstone's own bottoms-up work.** The key structural fact is that every line in BofA's exhibit moves in a near-fixed ratio to **AI Accelerators** — so once we plug in *our* accelerator estimate (GPU + custom ASIC), the rest of the TAM (HBM, networking, optical, storage…) drops out of BofA's ratios, and any line where our view diverges from BofA's becomes the explicit debate. The buy-side value: it turns a static sell-side exhibit into a cross-check — where is BofA too high/low vs our names, and is the dollar TAM even *supply-feasible* given the InP/HBM/cleanroom constraints our expert calls flag.

> **Status: scaffold.** The Capstone accelerator estimates are pending (Felipe finalizing). The fill-in section below is wired with BofA's multipliers and ready to receive them. **TODO:** drop our accelerator $ per year → auto-populate the implied TAM → flag divergences.

## 🆕🔴🔴🔴 2026-09-17 (Notion meeting-notes ingest, 09-21) — **§7 ITEM 6 GETS SAID OUT LOUD BY AN OUTSIDE VOICE, AND IT IS ATTACHED TO A NUMBER: HYPERSCALERS NEED *"$800 BILLION FLOWING TO THE INFRASTRUCTURE LEVEL"* A YEAR BY 2029 TO COVER DEPRECIATION, OPEX AND A 15% ROIC — AND *"IF YOU THINK THE TOTAL ADDRESSABLE MARKET OF AI BY 2029 IS JUST SOFTWARE, THEN IT'S VERY DIFFICULT TO GET TO $800 BILLION."* PLUS A DEDUPLICATED EX-CHINA GEN-AI REVENUE SERIES THAT PUTS **THREE DIFFERENT BASES IN ONE PARAGRAPH**.**

**Source: Azeem Azhar (Exponential View) @ BofA-hosted expert call, 2026-09-17 — Capstone notes (Notion transcript).** Archive: [`../../_equity_calls/Overall/2026-09-17_BofA_AI-industry-expert-call-Azeem-Azhar.md`](../../_equity_calls/Overall/2026-09-17_BofA_AI-industry-expert-call-Azeem-Azhar.md). ⚠️⚠️ **EXPERT VOICE HOSTED BY BofA GLOBAL THEMATIC RESEARCH — *NOT* BofA RESEARCH. No rating, no price target, no BofA estimate. Nothing in this block may be aggregated with the Vivek Arya / Didier Scemama marks on this page, and it does not move any consensus number.** ⚠️ Machine transcription of an unlabelled multi-speaker room; the arithmetic flagged below is this page's, not his.

- 🔴🔴🔴 **THE PAYBACK REQUIREMENT, AND IT IS THE FIRST TIME AN OUTSIDE SOURCE PUTS A DATED INFRASTRUCTURE-LEVEL REVENUE TARGET ON THE BUILD-OUT.** *"In our base case model, by 2029, in order to cover their depreciation expense, their OPEX, and a 15% ROIC… hyperscalers need [$800] billion a year of revenue. So that's **not $800 billion in the full Gen AI stack. That's $800 billion flowing to the infrastructure level that has put all these data centers together.**"* ⚠️ The transcript garbles the figure once as *"a billion dollars a year"*; the very next sentence names $800bn twice, so $800bn is the figure. ➤➤ **WHY IT BELONGS HERE AND NOT ONLY ON [hyperscaler-capex](hyperscaler-capex.md): this page's entire plausibility test is a DENOMINATOR argument (§1's `AI % of Overall IT Spend` row, 19.5% of $8,726bn by 2030; §7 item 6's software-budget-vs-wage-bill switch). Azhar states the same test as a forward revenue requirement and answers it the same way FUNDA does — *"If you think the total addressable market of AI by 2029 is just software, then it's very difficult to get to $800 billion. If you think it is software plus a new category, you could get to that $800 billion. If you think it is attached to a productivity boom that will really expand the markets, that $800 billion sits comfortably within the envelope."*** ✅ **Independent corroboration of the §7-item-6 FRAMING from a source with no model, no coverage and nothing to sell. It changes nothing in §1-§5.**
- 🔴🔴🔴 **THE REVENUE SERIES — AND THE WHOLE VALUE OF IT IS THAT THE BASES ARE SEPARATED. HE GIVES FOUR NUMBERS IN ONE PARAGRAPH AND THEY ARE FOUR DIFFERENT QUANTITIES.** Methodology as he states it: *"revenues flowing through the generative AI economy, both from a top-down way and a bottom-up way, for a thousand companies… a unique data set of **deduplicated** revenue flowing through Gen AI. **That is, if a dollar is spent with OpenAI and they spend 40 cents of it with Microsoft, we'll just count that as a dollar.**"*

| Figure | Basis — **state it every time** | As of |
|---|---|---|
| **~$140bn** | **Trailing twelve months**, deduplicated, **ex-China** | Aug 2026 |
| **~$115bn** | same TTM basis | Jun 2026 (*"about $115 billion"*) |
| **~3.2x** | y/y growth of the TTM series, vs his own end-2025 forecast of a **deceleration to 2.5x / 2.25x** | 2026 |
| **~$229bn** | **ANNUALISED AUGUST RUN-RATE** (August revenue × 12) — *not* a TTM, *not* a calendar year | Aug 2026 |
| **~$205-210bn** | **CALENDAR-YEAR 2026E**, against **~$63bn for calendar 2025** | CY26E |

  ⚠️⚠️ **THE TTM / RUN-RATE / CALENDAR-YEAR TRIPLE IS THE TRAP. In a 3.2x year the TTM sits at roughly 60% of the exit run-rate — $140bn and $229bn are the same series two definitions apart, and anyone quoting "$140bn of AI revenue" against a forward capex number is off by ~1.6x before the argument starts. EX-CHINA throughout.**
- 🔴🔴 **SCOPE — AND IT IS THE ANSWER TO THIS WIKI'S API-vs-ALL-IN TRAP: THIS IS *ALL-IN*, NOT MODEL-LAYER.** He names the four sources of the pool explicitly: *"the foundation model labs, but increasingly directly American enterprises and companies around the world **running AI services on the hyperscalers themselves**. And increasingly you're starting to see **SaaS companies like Adobe and others demonstrating AI uplift to their revenue**. And finally, there's a large number of **privately held companies in vertical space who are now exceeding a billion dollars of revenue**."* ➤ **So the pool = model layer + hyperscaler AI revenue + SaaS AI uplift + private vertical-AI apps, counted once at the end-customer dollar. It is NOT an API line and must never be set against one (the house's own API-vs-all-in gap is ~4.2x).**
- ⛔⚠️ **ONE BASIS DOES *NOT* RESOLVE ON THE RECORDING — LOGGED UNRESOLVED RATHER THAN GUESSED.** Immediately after the $800bn requirement he says the gap is *"quite a distance away from where we'll end this year. [break] part of the stack, which will probably be in the **$140, $150 billion range**."* The sentence breaks mid-clause. **TWO READINGS, BOTH LIVE: (a) $140-150bn is the INFRASTRUCTURE-LEVEL slice of CY26 — which is how the Notion auto-summary read it, and which implies infrastructure captures ~68-71% of his own $205-210bn CY26 total; or (b) it is a loose restatement of the TTM ex-China TOTAL ($140bn), in which case he is comparing a 2029 infrastructure-level target against a 2026 all-in TTM — apples to oranges, and the "$800bn vs $140-150bn" gap that the summary headlines is not a like-for-like gap at all.** ⚠️ **Under reading (a) the 2029 arithmetic is $800bn of infra ÷ ~0.70 ⇒ a ~$1.1tn all-in ex-China Gen-AI economy by 2029; under reading (b) no such implication exists. DO NOT USE EITHER UNTIL THE PUBLISHED "STATE OF THE AI ECONOMY" UPDATE PINS IT.** ➤ **TODO: the August update of Exponential View's "The State of the AI Economy" is the document that settles this — the June vintage is already on disk ([ev-state-of-ai-economy-2026.html](../../relat%C3%B3rios%20bons/ev-state-of-ai-economy-2026.html)).**
- ✅ **WHERE IT LANDS AGAINST THE HOUSE, PUT ON THE SAME BASIS FIRST.** The house **AI Labs Revenue MAP** is a **MODEL-LAYER** pool on a **MID-YEAR ARR run-rate** basis and **INCLUDES CHINA**, anchored at **~$140bn mid-26**; the **LLM Market MAP** carries CY26 system revenue of **$141.6bn all-in for the model/token layer**. Azhar's $140bn is a **TTM, ex-China, ALL-IN including applications and hyperscaler AI**. ⚠️ **SAME DIGITS, THREE DIFFERENT QUANTITIES — a digit collision of exactly the class this page already carries between $1.7tn-AI-DC-systems and $1.7tn-industry-sales.** ➤ **On a CY26 basis his $205-210bn ex-China all-in sits ABOVE the house's $141.6bn model-layer system revenue, but the gap is SCOPE (apps + hyperscaler AI, which the house pool excludes) NET OF GEOGRAPHY (China, which the house pool includes) — it is not evidence the house is too low. The only clean like-for-like on this page is against the wiki's own EV entry: the June TTM the wiki carries as $110bn is restated by its author to "about $115bn" (see [tokenmaxxing](tokenmaxxing.md) for the full reconciliation of the EV series).**
- 🔭 **THE DEMAND-SIDE EVIDENCE HE ATTACHES TO IT, AND IT IS THE STRONGEST DATAPOINT IN THE CALL FOR THE "SOFTWARE-PLUS" TAM.** A show-of-hands poll of *"a couple of hundred CIOs… more likely Russell 2000 companies than the very, very big companies"* at a Las Vegas conference ~10 days before the call: *"last year when I asked them, how many of you are having concrete, tangible results from AI? **About a quarter of the hands went up. And 10 days ago when I asked the question, 95% of the room put their hand up.** And that was quite a surprise to me."* With the behavioural corollary: *"I haven't really found many… mature companies outside of advanced technology companies who've said, we're going to slow down our spending. **They're actually increasing their ambitions.**"* ⚠️⚠️ **A SHOW OF HANDS, NOT A SURVEY: self-selected attendees, not the same cohort year to year, no definition of "concrete tangible results", no spend attached, and an unnamed venue. It is a directional inflection, NOT a 95% adoption statistic — do not put it in a model.** ➤ **And he supplies his own governor in the same breath: *"the capability of the AI models that currently exist has FAR EXCEEDED the ability of normal businesses to adopt, absorb and deploy them"*, with the $140bn representing *"many, many companies, most companies EXPERIMENTING and a small handful actually getting up the diffusion curve."* One named datapoint at the top of that curve: a construction/engineering company of 10,000-25,000 employees spending *"about $30 million this year across AI"* and expecting to raise it.**
- ⚠️ **THE EX-CHINA BASIS IS NOT A ROUNDING CHOICE — HE SIZES WHAT IS EXCLUDED.** Data-centre capex ratio US:China **3.4:1 in 2024 → ~6.1:1 in 2026**; China's share of global AI compute *"has actually fallen since… 2023. And it's roughly about 18 percent of global compute."* ➤ Full China leg belongs on [china-export](china-export.md) — carried here only because every figure in this block is ex-China and the exclusion is material.

## 🆕🔴🔴 2026-09-15 — **THE FRANCHISE NOTE BEHIND THIS PAGE WAS RE-CUT: CY30 INDUSTRY TAM +19% TO $3.2tn, THE CAGR FROM 14% TO 18%, AND WFE RAISED AT EVERY NODE OF THE CURVE. ⚠️ IT IS A DIFFERENT AGGREGATE FROM THE $1.7tn EXHIBIT BELOW — AND THE TWO NUMBERS COLLIDE ON THE SAME DIGITS.**

**What changed (BofA · Vivek Arya, "US Semiconductors — State of the Union: raising estimates, industry TAM doubling to $3.2tn CY30", 2026-09-15; relayed via the BofA TMT desk · Brian Fenske, sales commentary):**

| Line | Prior | New (2026-09-15) | Δ |
|---|---|---|---|
| Total semiconductor industry TAM, CY30 | **$2.7tn** | **$3.2tn** | **+19%** |
| Implied industry CAGR CY26-30 | **14%** | **18%** | +4pp |
| WFE CY26 | $144bn | **$156bn** (+33% YoY) | +8% |
| WFE CY27 | $190bn | **$210bn** | +11% |
| WFE CY28 | n/a on this page | **$270bn+** | new |
| WFE CY30 | n/a on this page | **$360bn** | new |
| NAND WFE CY26 | n/a on this page | **$15bn (+38% YoY)** | new |
| Automotive semis CY26 | n/a on this page | **$60bn (+12% YoY)** | new |

Drivers named: *"led mostly by growth in memory/data center, and also incrementally higher recovery in auto/industrial"*; the WFE upside *"comes largely from higher expectations for Memory WFE (especially DRAM)"*. The framing line: *"Effectively, the industry took 50 years to reach the $1T sales milestone, and is already set to double TAM in 4 years from $1.7T today."*

⚠️⚠️ **BASIS COLLISION — READ THIS BEFORE QUOTING EITHER NUMBER.** This page's source exhibit is the **AI Data-Center Systems TAM of $1,706bn in CY30** (§1 below, from the 2026-05-13 "AI 2030: Stronger for Longer" cut). Today's note is the **TOTAL semiconductor industry TAM**, a much larger aggregate, and its *"$1.7T today"* refers to **industry sales in 2026**, not to the CY30 AI-DC line. **Same digits, different universes.** The AI-DC sub-line was **NOT restated** in today's email, so **§1-§5 of this page STAND unchanged** and the fill-in engine's multipliers are untouched; whether the AI-DC slice was re-cut inside the new note can only be settled by reading the PDF. **TODO: pull the 2026-09-15 PDF and, if the AI-DC systems line moved, restate §1 with the old exhibit preserved in `## Changelog` first.**

**The European read-across, same house, same day (BofA · Didier Scemama, Head of European IT Hardware Research, 2026-09-15, emailed direct):** **EUV WFE grows faster than ex-EUV (+28% CAGR vs +25%)** as EUV spreads across sub-5nm logic and advanced DRAM; **WFE intensity reaches 11.2% in 2030E**; [[ASML]] carries an **EPS CAGR of 35% 25-30E → €110 EPS power in 2030E**, ASMI **€70 EPS power** on a 40% CAGR. Preferred expressions: semicaps (ASML, ASMI, VAT, COTN) plus IFX/STM.

**And the companion argument that matters for this framework's SHAPE, not its level:** *"Regulation may reduce the frequency of frontier training runs, but production AI agents will require monitoring, verification, containment and auditability across prompts, outputs and tool calls"* — which BofA expects to **redirect spend from concentrated frontier training toward distributed inference, control and connectivity infrastructure, producing a BROADER semiconductor cycle even if GPU growth moderates**, favouring **custom ASICs, CPUs, networking switches, optical interconnect and memory**, while *"Semicaps [are] largely agnostic to such shift in spending with a potential longer-term benefit if custom ASICs and connectivity silicon adopt the most leading-edge nodes"* (BofA · Didier Scemama, 2026-09-15). ➤ **If that mix shift is right, this page's fill-in engine is the thing that breaks first: every line here is pinned to a near-fixed ratio against AI ACCELERATORS, and a regulation-driven rotation into CPUs/networking/optics/memory changes the ratios rather than the total. Flagged as the first identified failure mode of the multiplier approach.**

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
6. **★★ THE BASIS SWITCH — SOFTWARE BUDGET vs WAGE BILL, and it is the single most consequential claim any source has made about this page's denominator (FUNDA "Deep|LLM: RSI Is the Most Important Variable, and Compute Is the Deepest Moat", 2026-08-05)** [Source](../../relat%C3%B3rios%20bons/Funda_on_RSI.html). **"If continual learning works, the valuation reference shifts FROM SOFTWARE BUDGET TO WAGE BILL: roughly $1 TRILLION GLOBALLY for the former, against MORE THAN $10 TRILLION IN U.S. WHITE-COLLAR WAGES ALONE for the latter."** The pricing path that follows: **from tens of dollars PER SEAT per month toward PER-TASK, PER-OUTCOME, and ultimately PER-UNIT-OF-LABOUR-REPLACED — "each step RAISES THE SHARE OF VALUE AI VENDORS CAPTURE."**
   - **⚠️ WHY THIS BELONGS ON A HARDWARE-TAM PAGE, STATED EXPLICITLY, BECAUSE IT IS NOT AN EXTRA NUMBER TO APPEND — IT REPLACES THE SANITY CHECK.** Everything above on this page is a **COST-SIDE** TAM: BofA sizes what buyers spend on silicon, networking and storage, and its own plausibility test is the row `AI % of Overall IT Spend` (§1: **19.5% of a $8,726bn IT budget by 2030**). That test is the standard bear discipline on the $1.7Tn — *AI cannot eat an implausible share of the IT budget.* **FUNDA's claim is that the IT budget is the wrong denominator entirely: if AI is sold as an employee rather than as a tool, the pool it is paid out of is the wage bill, and the IT-spend ceiling stops binding.** *Our arithmetic on FUNDA's two stated figures, not FUNDA's:* BofA's **$1.7Tn AI-DC systems TAM by 2030 EXCEEDS the entire ~$1Tn global software budget**, which on the old basis is prima facie absurd — the picks-and-shovels costing more than the product they serve — **but is ~17% of the >$10Tn US white-collar wage bill, which is not.** **Item 5 above asks whether $1.7Tn reconciles with the capex we track; item 6 asks the prior question of whether the revenue pool that has to service that capex is $1Tn or $10Tn+. Nothing on this page is decidable without answering it.**
   - **THE MIGRATION IS ALREADY MEASURABLE, which is the part that makes this more than a framing argument: [ANTHROPIC](../ANTHROPIC.md)'s API REVENUE SHARE OF 70-75%, WITH EIGHT-FIGURE ACCOUNTS DOUBLING IN SIX MONTHS — FUNDA's evidence that "the market is ALREADY SHIFTING FROM SEATS TOWARD USAGE AND OUTCOMES, and is one reason A SaaS FRAMEWORK IS THE WRONG BASIS FOR SETTING A VALUATION CEILING ON AI COMPANIES."** ⚠️ **A 70-75% API mix is the cleanest single observable for the per-seat→per-task migration, and it is a leading indicator for THIS page: usage-priced revenue converts into token volume converts into accelerator units, whereas seat-priced revenue does not.**
   - **⚠️ SCALE REFERENCE, CARRIED WITH AN EXPLICIT WARNING: "AI MAY EVENTUALLY ACCOUNT FOR 10-20% OF GLOBAL GDP, AND NO SINGLE COMPANY CAN CAPTURE EVEN 1% OF THAT VALUE." THIS IS AN UNCONFIRMED ACCOUNT of a closed-door discussion involving DeepSeek's founder that was circulating in the market in late July 2026 — FUNDA itself labels it unconfirmed by the company. DO NOT PRESENT IT AS SOURCED, do not put it in a model, and note that the second clause is a NEGATIVE claim about value capture that cuts against every single-name TAM on this page.**
   - **THE COUNTER-EVIDENCE FUNDA CONCEDES RATHER THAN OMITS, and it is the strongest datapoint against the whole basis switch: a widely cited MIT STUDY FOUND 95% OF ENTERPRISE GENAI PILOTS PRODUCED NO MEASURABLE ROI (methodology disputed).** ⚠️ **The wage-bill TAM is conditional on ONE capability — continual learning — and FUNDA says so; the 95% figure is what the world looks like before it arrives. Treat the basis switch as a SCENARIO on this page, not as a revision to §1: BofA's exhibit stands unchanged, and the switch tells you which denominator to test it against if and when enterprise adoption inflects.**

## Sources
- **Primary:** [BofA (Vivek Arya) — "AI 2030: Stronger for Longer for compute, memory, networking" (2026-05-13)](../../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html). TAM exhibit transcribed above; per-name POs from company pages.
- **Theme cross-refs:** [hbm-memory](hbm-memory.md) (HBM TAM $35→$168bn, MU SOTP, price ladder), [optical-cpo](optical-cpo.md) ($316bn networking TAM, InP supply gate), [custom-asic-tpu](custom-asic-tpu.md) (accelerator $1.0→$1.2Tn, NVDA/AVGO/AMD split), [hyperscaler-capex](hyperscaler-capex.md) (demand envelope), [ai-datacenter-power](ai-datacenter-power.md) (power as the binding constraint).
- **Company pages:** [NVDA](../NVDA.md), [AVGO](../AVGO.md), [AMD](../AMD.md), [MU](../MU.md), [MRVL](../MRVL.md), [COHR](../COHR.md), [LITE](../LITE.md), [ALAB](../ALAB.md), [CRDO](../CRDO.md), [ARM](../ARM.md), [INTC](../INTC.md).
- **[Ingest run — 2026-08-06]** [FUNDA — "Deep|LLM: RSI Is the Most Important Variable, and Compute Is the Deepest Moat" (fundaai.substack.com, 2026-08-05)](../../relat%C3%B3rios%20bons/Funda_on_RSI.html) — **the TAM-BASIS SWITCH, folded into §7 item 6.** **"If continual learning works, the valuation reference shifts FROM SOFTWARE BUDGET TO WAGE BILL: roughly $1 TRILLION globally for the former, against MORE THAN $10 TRILLION IN U.S. WHITE-COLLAR WAGES ALONE."** Pricing path **per-seat → per-task → per-outcome → per-unit-of-labour-replaced**, each step raising vendor value capture; migration evidence **[ANTHROPIC](../ANTHROPIC.md) API revenue share 70-75% with EIGHT-FIGURE ACCOUNTS DOUBLING IN SIX MONTHS**, and the argument that **a SaaS framework is the wrong basis for a valuation ceiling**. ⚠️ **Also carried with warnings: the "AI may account for 10-20% OF GLOBAL GDP, and no single company can capture even 1%" scale reference is an UNCONFIRMED account of a closed-door discussion (DeepSeek founder) — not sourced; and FUNDA concedes the MIT study finding 95% OF ENTERPRISE GENAI PILOTS PRODUCED NO MEASURABLE ROI (methodology disputed).** Capex/scenario leg on [hyperscaler-capex](hyperscaler-capex.md); July drawdown leg on [macro-cycle](macro-cycle.md).

## Changelog
- 2026-09-21 — notion-ingest: Azeem Azhar (Exponential View) @ BofA-hosted expert call 2026-09-17 — 1 dated block added, **NOTHING SUPERSEDED** (§1-§5 exhibit, multipliers, per-name scorecard and the ~$1.7tn CY30 AI-DC-systems TAM all stand; no ledger entry written). **Net-new: (1) a dated INFRASTRUCTURE-LEVEL revenue requirement — ~$800bn/yr by 2029 to cover depreciation + opex + 15% ROIC, explicitly "not $800 billion in the full Gen AI stack"; (2) his answer to it is §7 item 6 stated by an outside voice — software-only TAM makes $800bn "very difficult", software-plus-a-new-category reaches it, a productivity boom makes it "comfortable"; (3) a deduplicated EX-CHINA Gen-AI revenue series with the bases separated — TTM $140bn (Aug-26) vs $115bn (Jun-26), 3.2x y/y against his own forecast of a decline to 2.5x/2.25x, ANNUALISED August run-rate $229bn, CALENDAR 2026E $205-210bn vs $63bn in 2025; (4) the scope is ALL-IN (labs + hyperscaler AI + SaaS AI uplift + private vertical AI, counted once at the end-customer dollar) — NOT an API/model-layer line; (5) the CIO show-of-hands 95% vs ~25% a year earlier, with the capability-overhang governor in the same answer; (6) US:China DC-capex ratio 3.4:1 (2024) → 6.1:1 (2026), China ~18% of global AI compute.** ⛔ **ONE BASIS LEFT UNRESOLVED ON PURPOSE: whether the "$140, $150 billion range" he names against the $800bn target is the INFRASTRUCTURE slice of CY26 (the Notion summary's reading, implying infra ≈ 68-71% of his own $205-210bn total) or a loose restatement of the ex-China TTM TOTAL — the sentence breaks mid-clause on the recording. Both readings logged, neither adopted; the published August "State of the AI Economy" update settles it.** ⚠️⚠️ **EXPERT VOICE HOSTED BY BofA, NOT BofA RESEARCH — no rating, no PT, no BofA estimate; never aggregated with the Arya/Scemama marks on this page.** 🔭 Variant perception in the block: his $140bn (TTM, ex-China, all-in) collides on digits with the house AI Labs Revenue MAP's ~$140bn mid-26 anchor (model-layer, mid-year ARR, INCLUDES China) and the LLM Market MAP's $141.6bn CY26 — three different quantities.
- **2026-09-15 (/wiki-ingest, 21:00) — logged the BofA franchise-note re-cut WITHOUT touching §1-§5.** The CY30 TOTAL industry TAM went $2.7tn → $3.2tn (+19%) and the CY26-30 CAGR 14% → 18%, with WFE raised to $156bn/$210bn CY26/27 (from $144bn/$190bn) and new CY28 $270bn+/CY30 $360bn marks, NAND WFE $15bn (+38%) and auto $60bn (+12%) in CY26E (BofA · Vivek Arya, 2026-09-15; European read-across BofA · Didier Scemama same day: EUV WFE +28% CAGR vs ex-EUV +25%, WFE intensity 11.2% in 2030E, ASML €110 EPS power 2030E on a 35% CAGR). ✅ **NOTHING ON THIS PAGE WAS SUPERSEDED**: the exhibit in §1 is the AI DATA-CENTRE SYSTEMS TAM ($1,706bn CY30), a different and smaller aggregate than today's total-industry figure, and it was not restated in the email — the note's own "$1.7T today" refers to 2026 industry SALES, a digit collision with §1's CY30 AI-DC line. TODO left open: read the 2026-09-15 PDF and restate §1 only if the AI-DC line itself moved. Also logged the first identified failure mode of the fill-in engine: BofA's own AI-regulation note argues for a mix shift toward CPUs/networking/optics/memory, which moves the accelerator-ratio multipliers this page is built on.

<!-- One dated line per material change to the thesis/state-of-play. Move superseded numbers
     here (old value + date) instead of deleting. Newest first. -->
- **2026-08-06 (theme patch) — FUNDA's TAM-basis switch added as §7 item 6 + a Sources entry. NOTHING SUPERSEDED: BofA's §1-§5 exhibit, multipliers and per-name scorecard are unchanged, and the ~$1.7Tn CY30 AI-DC systems TAM remains this page's headline number.** **What changed is the SANITY CHECK, not the TAM: this page's plausibility test has been BofA's own `AI % of Overall IT Spend` row (19.5% of $8,726bn by 2030) — a COST-SIDE denominator. FUNDA argues that if continual learning works the reference pool is the WAGE BILL, not the software budget (~$1TN global software spend vs >$10TN of US white-collar wages alone), at which point the IT-budget ceiling stops binding.** *Our arithmetic on FUNDA's two figures, flagged as ours:* **BofA's $1.7Tn hardware TAM exceeds the entire ~$1Tn global software budget (absurd on the old basis) but is ~17% of the >$10Tn wage bill (not absurd).** Supporting datapoints added: **[ANTHROPIC](../ANTHROPIC.md) API revenue share 70-75%, eight-figure accounts doubling in six months**; pricing migration **per-seat → per-task → per-outcome → per-unit-of-labour-replaced**. ⚠️ **Two items carried with explicit warnings rather than adopted: the 10-20%-of-global-GDP scale reference is an UNCONFIRMED closed-door account (DeepSeek founder) and must never be presented as sourced; and the MIT 95%-of-pilots-no-ROI finding (methodology disputed) is the counter-evidence FUNDA itself concedes. The basis switch is recorded as a CONDITIONAL SCENARIO gated on continual learning, not as a revision to §1.** Cross-filed [hyperscaler-capex](hyperscaler-capex.md), [macro-cycle](macro-cycle.md), [ANTHROPIC](../ANTHROPIC.md).
- **2026-06-30** — page created (BofA "AI 2030" exhibit transcribed; fill-in engine built; §4 Capstone accelerator estimates still PENDING).
