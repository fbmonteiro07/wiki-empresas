# TER — Teradyne, Inc.

_Wiki · generated 2026-06-19 · sources: `E:\Wiki Felipe\TER` (filings + transcripts) · `_equity_calls` · `_briefings`. Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $4.4bn | $5.5bn |
| Gross profit | $2.6bn | $3.3bn |
| Gross margin | 58.6% | 59.6% |
| EBITDA | $1.4bn | $2.0bn |
| EPS | $6.88 | $9.93 |
| Capex | $262m | $277m |
| OCF (≈EBITDA) | $1.4bn | $2.0bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Teradyne is the #2 global automated-test-equipment (ATE) vendor — a back-end semiconductor name levered to **test intensity**, not wafer starts. Three reportable segments: **Semiconductor Test** (~87% of revenue: SoC + Memory + Integrated System Test/IST), **Robotics** (Universal Robots cobots + MiR autonomous mobile robots, ~7%), and **Product Test** (board test, wireless, PIC/silicon-photonics test, defense/aerospace, ~6%) (TER 10-Q, Q1 FY26, 2026-05-01). The structural story is the swing from a mobile-driven mix to an **AI-dominant** one: AI-related demand was **~70% of total revenue in Q1 FY26**, up from ~60% in Q4 FY25 and ~50% in Q3 FY25 (TER Q1 FY26 call, 2026-04-29). Duopoly in SoC/memory ATE vs **Advantest**; Robotics competes with FANUC/ABB/KUKA/Yaskawa (TER 10-K, 2026-02-19).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) SoC test systems (AI-compute, ~75% of SoC) · 2) Memory/HBM test (Magnum) · 3) Robotics (Universal Robots cobots + MiR) |
| **Main buyer(s)** | Foundries / OSATs / IDMs / memory makers / fabless + hyperscaler ASIC (VIP) programs; concentrated — top-5 = 44% of FY25 rev, ~2 customers drive most tester demand |
| **Key suppliers** | Test instruments, lasers/optics (SiPh), handlers, probers, robotics components |

## Position in the value chain
Back-end test. Teradyne buys instruments and handler/prober/robotics components, integrates them into ATE platforms, and sells to foundries, OSATs, IDMs, memory makers and fabless/HPC/mobile customers. Levered to the **rising test intensity of complex AI chips, HBM stacks, and co-packaged optics (CPO)** — more chiplets, more die-stacking and tighter latent-defect tolerance mean more test insertions per device (TER Q3 FY25 call, 2025-10-29).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="720" height="220" fill="#ffffff"/>
  <!-- Suppliers -->
  <rect x="10" y="55" width="170" height="110" rx="8" fill="#eef4fb" stroke="#3b6ea5"/>
  <text x="95" y="80" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">Suppliers</text>
  <text x="95" y="102" font-family="sans-serif" font-size="10" text-anchor="middle">Test instruments,</text>
  <text x="95" y="118" font-family="sans-serif" font-size="10" text-anchor="middle">lasers / optics (SiPh),</text>
  <text x="95" y="134" font-family="sans-serif" font-size="10" text-anchor="middle">handlers, probers,</text>
  <text x="95" y="150" font-family="sans-serif" font-size="10" text-anchor="middle">robotics components</text>
  <!-- TER -->
  <rect x="245" y="40" width="220" height="140" rx="8" fill="#fef6e7" stroke="#c9921f" stroke-width="2"/>
  <text x="355" y="66" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">TERADYNE (TER)</text>
  <text x="355" y="90" font-family="sans-serif" font-size="10" text-anchor="middle">ATE test systems:</text>
  <text x="355" y="106" font-family="sans-serif" font-size="10" text-anchor="middle">SoC + Memory/HBM (Magnum)</text>
  <text x="355" y="122" font-family="sans-serif" font-size="10" text-anchor="middle">IST / SLT · PIC/CPO (Photon 100)</text>
  <text x="355" y="144" font-family="sans-serif" font-size="10" text-anchor="middle">Universal Robots cobots</text>
  <text x="355" y="160" font-family="sans-serif" font-size="10" text-anchor="middle">+ MiR mobile robots</text>
  <!-- Customers -->
  <rect x="530" y="55" width="180" height="110" rx="8" fill="#edf7ee" stroke="#4a8b53"/>
  <text x="620" y="80" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">Customers</text>
  <text x="620" y="102" font-family="sans-serif" font-size="10" text-anchor="middle">Foundries, OSATs,</text>
  <text x="620" y="118" font-family="sans-serif" font-size="10" text-anchor="middle">IDMs, memory makers,</text>
  <text x="620" y="134" font-family="sans-serif" font-size="10" text-anchor="middle">fabless / mobile / HPC,</text>
  <text x="620" y="150" font-family="sans-serif" font-size="10" text-anchor="middle">hyperscaler ASIC (VIP)</text>
  <!-- Arrows -->
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#444"/>
    </marker>
  </defs>
  <line x1="180" y1="110" x2="243" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="465" y1="110" x2="528" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
  <text x="355" y="205" font-family="sans-serif" font-size="10" font-style="italic" text-anchor="middle">Back-end test · levered to rising test intensity of AI chips + HBM + CPO</text>
</svg>

## Current state (latest quarter)
**Q1 FY26 (reported 2026-04-29, quarter ended Mar 29 2026)** — a record. Total revenue **$1,282.5M, +87% y/y / +18% q/q** ($200M above the prior 2021 peak); GAAP diluted EPS **$2.53** (vs $0.61 Q1 FY25), non-GAAP EPS **$2.56**; non-GAAP gross margin **60.9%** (+370bps q/q); non-GAAP operating margin a record **37.5%** (TER Q1 FY26 call; 10-Q 2026-05-01). GAAP gross profit $780.9M (61%), GAAP operating income $473.0M, net income $398.9M (10-Q). Segment split: **Semi Test $1,110.8M (+104.8% y/y)** — SoC $882M (~75% AI-compute), Memory $203M (near-record on HBM/DRAM), IST $27M; **Robotics $91.3M (+32% y/y, 4th straight q/q growth)**; **Product Test $80.4M (+8% y/y, defense/aerospace led)**. Geography heavily Asia: Taiwan 41%, Korea 19%, China 11% of revenue (10-Q). **Guidance Q2 FY26: revenue $1.15–$1.25B, non-GAAP EPS $1.86–$2.15, GM 58–59%**; H1-weighted (~55–60% of FY26 in H1). FY26 evergreen target reiterated: **~$6B revenue / $9.50–$11 non-GAAP EPS** (TER Q4 FY25 call, 2026-02-03). Capital return modest: $5.5M buyback + $20.4M dividends ($0.13/qtr) in Q1 (10-Q).

## Capstone estimates (house model)
_Source: Capstone peer model (`ASML_Peers_SemiCap_v16.xlsx` — Peer Comp, 2026-06-15). EPS-only (full P&L not modeled by name here)._

| Diluted EPS ($) | 2024 | 2025 | 2026E | 2027E | 2028E | vs cons NTM |
|---|--:|--:|--:|--:|--:|--:|
| TER | 3.38 | 3.47 | 5.46 | 6.90 | — | ~8.25 |

**House read:** EPS 2026E $5.46 / 2027E $6.90 — **below** consensus (more cautious on ATE) (NTM ~8.25). (Capstone peer model, 2026-06-15)

## Debate / thesis
- **Capstone model (house view):** diluted EPS $5.5 / $6.9 (2026-27E) — **below** NTM consensus ~$8.2 (model more cautious on ATE); implied P/E ~79x→63x. (Capstone official model — ASML_Peers_SemiCap v16, 2026-06-15)
- **Bull (UBS / Arcuri — Buy, PT $200):** Formal stance is **Buy, $200 PT** (from $195 spot; AI rev-mix lifting ~21%/25%/28% CY26/27/28) (UBS 2026 overview, Arcuri, 2025-12-22). Thesis: TER holds a portfolio of FY26-ramping wins — UBS reads them as the **Amazon "Project Vulcan" ASIC win** and the **NVDA evaluation** (second-source amid rising test times) — plus (1) mobile-test recovery at AAPL, (2) **HBM share gains**, (3) new AI-ASIC wins; end of Moore's Law = secular test-intensity tailwind. The under-appreciated leg: **SoC-Test TAM + the NVDA opportunity could approach ~$1B+/yr by 2027** (UBS, 2025-12-22). Arcuri sizes the NVDA tester opportunity explicitly: NVDA bought **~$1.8B of testers in 2024**, and he sees that NVDA tester TAM growing to **~$3.5–4B by 2028**, with TER plausibly capturing **~half (~$2B) — i.e. from ~zero in 2024 to ~$2B by 2028** (UBS–Arcuri weekly, 2026-04-06; UBS–Arcuri analog preview, 2026-04-20). Bigger picture, his core argument is that **TER is a TAM story, not a share story**: test intensity (test TAM ÷ semiconductor industry revenue) has historically run **~1% vs ~15% for front-end WFE**, so even a move to ~1.5–2% — driven by more insertions on stacked die / bonded wafers / CPO — makes "the TAM explode," with TER gaining share into an expanding TAM (UBS–Arcuri analog preview, 2026-04-20). On positioning, TER is **already qualified in NVDA gaming and in qualification for Rubin**, and the Ruben-Ultra shift from a 4-die to a 2-die package (576→288 die) is "broadly a wash" for a per-unit tester company (UBS–Arcuri weekly, 2026-04-06). By spring Arcuri had it among his top picks at a higher ref — "Teradyne at 320… that's one I like a lot," a late-cycle laggard (UBS weekly preview, 2026-05-18). CPO option also real — four test insertions, $300–700M mid-term TAM, first-mover via Fi-Con Tech + Quantifi/Photon 100 (UBS–Teradyne CPO call, Shannon Poehlen, 2026-05-04).
- **Bull (JPM / Samik — but Neutral, PT $193.37):** Constructive thesis, Neutral rating. AI rev mix steps **20%→41% (FY25→FY26E)**; VIP-ASIC test TAM durability + NVDA dual-source optionality (Vera Rubin insertion vs incumbent Advantest) are the swing factors; several "on-the-cusp" high-volume sockets straddle the 2025/26 boundary (JPM Hardware & Networking, Chatterjee, 2025-12-15). By mid-2026: "sounding a bit better about memory demand" → H2 upside; **Google ASIC (VIP compute) qual finishing ~end-3Q**, modest 4Q revenue then 2027 ramp; Intel merchant-test shift an out-year option (JPM, 2026-06-12).
- **Bear:** (1) **Customer concentration** — top-5 direct customers = 44% of FY25 revenue; "vast majority of tester demand driven by ~2 customers"; hyperscalers pushing dual-sourcing (10-K; TER Q3 FY25 call). (2) **Visibility/lumpiness** — Smith: "we don't have meaningful commitment from customers around what they'll buy and when"; 12–18-wk lead times mean no clean H2 reset on the print (TER Q1 FY26 call; JPM 2026-06-12). (3) H1-weighted year (VIP compute split ~85/15 H1/H2) → optically softer H2 (JPM, 2026-06-12). (4) Mobile soft; memory pricing/availability pressuring non-iOS demand (TER Q1 FY26 call). (5) **GPU-test skepticism** — supply-chain view is Advantest stays the GPU/HPC incumbent (large dies), with TER "best for mobile" / Apple integration-fanout; near-term TER not winning AI testing, though InFO-on-substrate parts (e.g., Tesla AI chip) could open a mid-tier lane (StoneX / John Su, TSMC channel, 2025-08-20). (6) **Robotics sub-scale** — breakeven cut $440M→$365M post-4Q24 restructuring, yet at ~$75M/qtr annualized still below breakeven; Project Vulcan ramp may not restore profitability in 2026 (JPM, 2025-12-15). TER also screens as a bottom-10 YTD robotics/humanoid-basket name, MS-rated **Underweight** (Shane Brett) in the humanoids universe (MS Humanoids).
- **Where the Street stands:** Split, tilting bull. **GS (Schneider) Buy, PT raised to $465 (from $350)** — 37x normalized EPS **$12.50 (from $10.00 on better visibility)**; **CY26 non-GAAP EPS est ~2% above Street** (~2% revenue upside in the quarter, though a 3Q guide down low-double-digits q/q on lumpiness); GS is **bullish on TER's merchant-GPU test share gains** vs Advantest's incumbency at Nvidia, and flags memory-test / NAND-eSSD recovery + CPO test as focus items (Goldman Sachs "2Q Preview: Expect broad upside...", 2026-07-05). **UBS Buy $200** (Arcuri, 2025-12-22; pushed higher to a ~$320 ref by 2026-05-18) vs **JPM Neutral $193.37** (Chatterjee, 2025-12-15) — disagreement centers on whether the NVDA second-source win and SoC-Test TAM (~$1B+/yr by 2027 per UBS) actually land, against StoneX channel skepticism that GPU test stays Advantest's. **TD Cowen (Krish Sankar) Buy, PT $400** (price $351.57, 07/08 close) — the back-end read: unlike front-end semicaps (raising prices 10-20% by year-end as customers grant extended visibility), **TER is NOT raising prices**, but Cowen says **EPS expectations have been de-risked** (TD Cowen "Earnings Preview: Puts & Takes", 2026-07-09).

## Catalysts / what to watch
- **Q2 FY26 print** (late July 2026) — H1/H2 shape, memory-demand tone, whether H2 guide ticks up (JPM expects it to).
- **NVDA tester qualification / second-source** — call option for GPU test (Vera Rubin insertion); UBS sizes the SoC-Test + NVDA opportunity at ~$1B+/yr by 2027 (UBS, 2025-12-22; JPM, 2025-12-15). Pre-Q1 setup: TER had guided **H2 FY26 down ~20% h/h** and June (Q2) down, while building in only **~$50M of NVDA revenue in H2** — Arcuri thought TER was **sandbagging** on both, modeling June above the Street and an H2 that has "filled in" (driven by **Trainium, Mellanox and Broadcom networking** demand), and expected TER to ultimately take up the H2 guide (UBS–Arcuri analog preview, 2026-04-20).
- **Amazon "Project Vulcan" ASIC win** ramp through FY26 — also the swing factor for Robotics breakeven (UBS, 2025-12-22; JPM, 2025-12-15).
- **Google VIP-compute qualification** completing ~end-3Q FY26 → modest 4Q revenue, 2027 ramp (JPM, 2026-06-12).
- **CPO / silicon photonics** insertion mix evolution; ramp weighted to H2 (UBS CPO call, 2026-05-04). Watch SemiAnalysis CPO skepticism noted in the tape (briefing, 2026-06-17).
- **Intel** possible shift from in-house to merchant test — out-year, "not imminent" (JPM, 2026-06-12).
- Robotics "plan of record" customer ramp later 2026 + new US robotics facility (TER Q2 FY25 call, 2025-07-30).

## Risks
- Customer + geographic concentration (top-5 = 44% FY25; Taiwan/Korea/China = 71% of Q1 FY26 revenue) (10-K; 10-Q).
- Semiconductor cyclicality / over-supply swings inherent to ATE (10-K risk factors).
- China export-control / tariff exposure; competitors not always under the same restrictions (10-K).
- Reliance on a small set of AI/VIP programs whose timing drives lumpy orders; tester lead-times limit forward visibility (10-K; TER Q1 FY26 call).
- **GPU/HPC test may stay Advantest's** — TER position strongest in mobile/integration-fanout; NVDA/AI win is optionality, not base case (StoneX / John Su, 2025-08-20). UBS also flags EUV intensity potentially breaking the front-end-WFE→tester relationship, and difficulty securing wins on new ARM/ASIC/Apple designs (UBS, 2025-12-22).
- CPO/merchant-GPU TAM still early-stage; share split with Advantest/FormFactor unsettled across insertions (UBS CPO call, 2026-05-04).
- Robotics structurally sub-scale / below breakeven (JPM, 2025-12-15).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **UBS 2026 overview (Arcuri)** _(2025-12-22)_: **Buy, PT $200** — SoC-Test TAM "grossly under-appreciated," NVDA opp ~$1B+/yr by 2027; Amazon Vulcan + NVDA eval the FY26 ramps.
- **Samik Chatterjee (JPM) 2026 outlook** _(2025-12-15)_: **Neutral, PT $193.37** — VIP-ASIC TAM durability + NVDA share gains the 2026 watchpoint; robotics still sub-breakeven.
- **Samik Chatterjee (JPM) preview** _(2026-06-12)_: **Teradyne 2H improvement "nuanced positive"** — memory test demand stronger; 1H still leads 2H on VIP-compute split; Lumentum OCS-outsourcing read-through.
- **StoneX / John Su (TSMC channel)** _(2025-08-20)_: GPU test stays Advantest near-term; TER mobile/fanout-led; InFO-on-substrate a mid-tier opening.
- **Susquehanna corporate access** _(2026-06-18)_: TER in the test/semicap event calendar.
- **UBS (Arcuri) — semis** _(2026-06-15)_: "Paradine [Teradyne]… talking about being qualified for **Google TPU** — that's pretty good stuff" — incremental SoC-test design-win color for the ASIC ramp (UBS "Arcuri", 2026-06-15).
- **AlphaSense Deep Research — LRCX primer (Mizuho peer comp)** _(2026-06-22)_: TER at **CY27E P/E 38.2x / EV/FCF 49.8x / P/Sales 10.9x** (~$60bn mkt cap) — the richest EV/FCF in the Mizuho semicap comp table (AlphaSense "DR LRCX primer", 2026-06-22).

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY26 print → intra-quarter · Apr 29 → Jun 22, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **SoC / compute test** | SoC $882M (~75% compute-driven); structural mobile→AI shift | UBS (Arcuri): "qualified for Google TPU — pretty good stuff", design-win color for the ASIC ramp · GS (07-05): Buy $465, bullish on merchant-GPU test share gains vs Advantest's Nvidia incumbency | **✓ confirms** (ASIC + merchant-GPU share-gain optionality) |
| **Memory test** | $203M; strength in HBM + DRAM | JPM (Samik): stronger memory-test demand → 2H upside ("nuanced positive") | **✓ confirms** (memory pulls 2H) |
| **Guidance / 2H** | Q2 guide revenue $1.15-1.25B; "three AI waves" | JPM: 1H still leads 2H on the VIP-compute split (~85/15); Google ASIC qual finishing ~end-3Q, modest 4Q revenue, ramp in 2027 | **⚠ nuance** (ASIC upside slips to 2027) |
| **Product / optics** | — | UBS: CPO/silicon-photonics deep-dive, 4 test insertions, mid-term TAM $300-700M, ramp weighted to H2 | **✓ confirms** (real optionality in CPO) |
| **Valuation** | Record GM 60.9%; op margin 37.5% | UBS: top pick, late-cycle laggard — vs Mizuho comp: CY27E EV/FCF 49.8x, the richest in the semicap table; TD Cowen (07-09): Buy $400, EPS de-risked | **⚠ nuance** (laggard vs stretched multiple) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-04 | UBS · Arcuri / Shannon Poehlen / Gita Atalier | product | bull | UBS-Teradyne deep-dive on CPO/silicon photonics: real optionality — four test insertions, mid-term TAM of $300-700M, first-mover via Fi-Con Tech + Quantifi/Photon 100. Ramp weighted to H2. |
| 05-18 | UBS · Tim Arcuri | valuation | bull | In the weekly preview, TER among the top picks at a higher ref: "Teradyne at 320... that's one I like a lot," a late-cycle laggard. |
| 06-12 | JPM · Samik Chatterjee | guidance | mixed | Preview: 2H improvement "nuanced positive" — stronger memory test demand → H2 upside; 1H still leads 2H on the VIP-compute split (~85/15 H1/H2). Google ASIC (VIP compute) qual finishing ~end-3Q, modest 4Q revenue and ramp in 2027; Intel merchant test shift is an out-year option. Read-through from Lumentum OCS outsourcing. |
| 06-15 | UBS · Tim Arcuri | product | bull | "Teradyne... talking about being qualified for Google TPU — that's pretty good stuff" — incremental SoC-test design-win color for the ASIC ramp. |
| 06-18 | Susquehanna · corporate access | valuation | neutral | TER on the test/semicap events calendar (corporate access). |
| 06-22 | AlphaSense Deep Research · LRCX primer (Mizuho comp) | valuation | mixed | TER at CY27E P/E 38.2x / EV/FCF 49.8x / P/Sales 10.9x (~$60bn mkt cap) — the richest EV/FCF in Mizuho's semicap comp table. |
| 07-05 | GS · James Schneider (Semis 2Q Preview) | valuation | bull | GS **Buy, PT raised to $465 (from $350)** — 37x normalized EPS **$12.50 (from $10.00)**; **CY26 non-GAAP EPS est ~2% above Street** (~2% revenue upside in the quarter; 3Q guide down low-double-digits q/q on lumpiness). GS is **bullish on TER's merchant-GPU test share gains** vs Advantest's incumbency at Nvidia; also watches memory-test / NAND-eSSD recovery + CPO test. (Goldman Sachs "2Q Preview: Expect broad upside...", 2026-07-05) |
| 07-09 | TD Cowen · Krish Sankar | margem | bull | TD Cowen (Earnings Preview: Puts & Takes): **Buy, PT $400** (price $351.57, 07/08 close). Back-end read — **TER is NOT raising prices** (vs front-end semicaps lifting prices 10-20% by year-end on extended customer visibility), but **EPS expectations have been de-risked**. (TD Cowen "Earnings Preview: Puts & Takes", 2026-07-09) |

**Quarter synthesis:** the flow validates the growth levers (strong memory test, Google TPU design-win, CPO optionality) and GS (07-05) now sets a fresh bull PT ($465, up from $350) explicitly on merchant-GPU test share gains vs Advantest — but the debate stays on timing and price: Google's ASIC ramp slips to 2027 (JPM's 85/15 H1/H2 split), the durability of merchant-GPU test share vs Advantest's Nvidia incumbency is the swing, and the multiple is already the richest EV/FCF in Mizuho's semicap table.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2'25 | Q3'25 | Q4'25 | Q1'26 |
|---|---|---|---|---|
| **SoC/compute test (AI/HBM)** | SoC $397M; AI compute ~20% of SoC | SoC $440M (+11% q/q); test intensity rising w/ chiplets | SoC +47% q/q; AI >60% of revenue | SoC $882M (~75% compute-driven); structural mobile→AI shift |
| **Memory test** | $61M; timing-related dip, H2 recovery expected | $128M (+110% q/q); HBM3E/4 via Magnum 7H | Record $206M (+61% q/q) | $203M; HBM + DRAM strength |
| **Robotics** | $75M (+9% q/q); "plan of record" win for 2026 | $75M (flat q/q) | $89M; 3rd straight growth qtr | $91M (+32% y/y); 4th straight growth qtr |
| **China** | — | — | — | Memory pricing/availability hurting end-demand outside iOS |
| **AI demand** | Primary near-term growth driver | ~50% of revenue; ~60% guided Q4 | >60% of revenue; ~70% guided Q1 | ~70% of revenue; three AI waves framed |
| **Gross margin** | 57.3% non-GAAP | 58.5% non-GAAP (above guide) | within 57–58% guide | Record 60.9% (+370bps q/q) |

_Source: TER earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Capstone model:** `P:\Felipe Monteiro\US Equities\Modelos oficiais\ASML_Peers_SemiCap_v16.xlsx` (house peer EPS estimates).
- **Filings:** [10-K FY25 (filed 2026-02-19)](../TER/TER_10-K_2026-02-19_0001193125-26-059002.html) · [10-Q Q1 FY26 (filed 2026-05-01)](../TER/TER_10-Q_2026-05-01_0001193125-26-201058.html).
- **Transcripts:** [Q1 FY26](../TER/transcripts/TER_Q1-2026-earnings_2026-04-29.md) · [Q4 FY25](../TER/transcripts/TER_Q4-2025-earnings_2026-02-03.md) · [Q3 FY25](../TER/transcripts/TER_Q3-2025-earnings_2025-10-29.md) · [Q2 FY25](../TER/transcripts/TER_Q2-2025-earnings_2025-07-30.md).
- **Equity calls:** [UBS–Arcuri analog preview (2026-04-20)](../_equity_calls/Semis/2026-04-20_Arcuri_analog-preview.md) — NVDA tester TAM $3.5–4B by 2028, TER ~half; test-intensity 1% vs WFE 15%; H2 sandbag; [UBS–Arcuri weekly (2026-04-06)](../_equity_calls/Semis/2026-04-06_Arcuri_weekly.md) — NVDA bought $1.8B testers in 2024, TER gaming-qualified / in qual for Rubin, Ruben-Ultra die-count shift a "wash"; [UBS–Teradyne CPO deep-dive](../_equity_calls/Semis/2026-05-04_Arcuri-Teradyne_CPO.md) (Arcuri / Shannon Poehlen / Gita Atalier, 2026-05-04); UBS weekly preview (Arcuri, 2026-05-18 — TER a top pick); JPM memory/HDD preview (Samik Chatterjee, 2026-06-12). See the TER section in [INDEX](../INDEX.md).
- **Research reports (relatórios bons):**
  - [JPM Hardware & Networking (2025-12-15)](../relat%C3%B3rios%20bons/JPM_Hardware___Networkin_2025-12-15_5155719.html)
  - [UBS 2026 overview](../relat%C3%B3rios%20bons/UBS_2026_overview.html)
  - [StoneX / John Su — TSMC (2025-08-20)](../relat%C3%B3rios%20bons/StoneX_Market_Intelligence_-_John_Su_-_20250820_-_TSMC_11.html)
  - [Humanoids](../relat%C3%B3rios%20bons/Humanoids.html)
  - [UBS (Arcuri) — semis/memory (2026-06-15)](../relat%C3%B3rios%20bons/2026_06_15_ubs_arcuri_15_jun_26.html) — Teradyne qualified for Google TPU.
  - [AlphaSense Deep Research — LRCX primer (2026-06-22)](../relat%C3%B3rios%20bons/DR-Report-by-Alphasense-06-22-2026-20-13.html) — TER in Mizuho semicap comp (CY27E P/E 38.2x).
  - [GS 2Q Preview (2026-07-05)](../relat%C3%B3rios%20bons/2Q_Preview__Expect_broad_upside_but_run_in_stocks_raises_the_bar_tactical_ideas_for_earnings.html) — TER Buy, PT $465 (from $350), 37x normalized EPS $12.50 (from $10.00); CY26 non-GAAP EPS ~2% above Street; bullish on merchant-GPU test share gains vs Advantest's Nvidia incumbency.
  - [TD Cowen (Krish Sankar) — "Earnings Preview: Puts & Takes Heading Into SPE And Storage Earnings Season" (2026-07-09)](../relat%C3%B3rios%20bons/Cowen_Preview_Semicap_1.html) — Buy, PT $400; back-end (TER) NOT raising prices (vs front-end +10-20% by year-end); EPS expectations de-risked.
- **Briefings:** company-specific roll-up (2026-06-17) — TER "zero email coverage" that day; SemiAnalysis CPO skepticism noted in TMT tape.
- **Outlook:** Direct Outlook mailbox search was not available to this run (mailbox unreachable to subagents); sell-side stance above is sourced from the saved equity-call transcripts and the dated briefing roll-up instead.

## Changelog
- **2026-07-09** — Added **TD Cowen "Earnings Preview: Puts & Takes" (Krish Sankar, 2026-07-09)** — first TD Cowen PT on the page: **Buy, PT $400** (price $351.57, 07/08 close); the back-end read — **TER is NOT raising prices** (unlike front-end semicaps, +10-20% by year-end on extended customer visibility), but Cowen says **EPS expectations have been de-risked**. Added to "Where the Street stands," the Valuation signal-vs-management row, 1 intra-quarter full-log row (07-09, margem/bull) + quarter-synthesis line, and Sources. No prior TD Cowen figure superseded (first Cowen PT on the page). TER not among Cowen's top Longs (front-end + subsystems only).
- **2026-07-05** — Added **GS "2Q Preview" (Schneider, 2026-07-05)** — first GS PT on the page: **Buy, PT $465 (from $350)**, 37x normalized EPS $12.50 (from $10.00); **CY26 non-GAAP EPS ~2% above Street**; GS bullish on merchant-GPU test share gains vs Advantest's Nvidia incumbency. Added to "Where the Street stands," the SoC/compute-test signal-vs-management row, 1 intra-quarter full-log row + quarter synthesis, and Sources. No prior GS figure superseded.
- **2026-06-26** — Read the two previously-unlinked UBS–Arcuri equity calls (analog preview 2026-04-20; weekly 2026-04-06). Added net-new bull-case quant to Debate/thesis (NVDA bought ~$1.8B testers in 2024; NVDA tester TAM ~$3.5–4B by 2028 with TER ~half ≈ $2B; test-intensity ~1% vs WFE ~15% "TAM-not-share" framing; TER gaming-qualified / in qual for Rubin; Ruben-Ultra 576→288 die shift a "wash") and to Catalysts (pre-Q1 H2-down-20%-h/h guide + ~$50M NVDA-H2 sandbag, Arcuri sees H2 "filled in" on Trainium/Mellanox/Broadcom). Linked both calls in Sources. (The XP GPU-memory call, 2026-05-27, was reviewed but contained no substantive TER content — spurious auto-attribution — so was not used.)
