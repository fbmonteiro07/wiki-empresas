<!-- Per-company wiki page. Financials/consensus block auto-injected by build_wiki_html.py from _data/estimates.json — do NOT hand-write it. -->

# QCOM — QUALCOMM Incorporated

_Wiki · generated 2026-06-19 · sources: `E:\Wiki Felipe\QCOM` (10-K FY25, 10-Q Q2 FY26, transcripts) · `_briefings` roll-up. Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $41.1bn | $45.4bn |
| Gross profit | $22.7bn | $25.0bn |
| Gross margin | 55.2% | 55.0% |
| EBITDA | $13.6bn | $15.0bn |
| EPS | $9.86 | $11.47 |
| Capex | $1.6bn | $1.8bn |
| OCF (≈EBITDA) | $13.6bn | $15.0bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Qualcomm is the leading merchant supplier of premium mobile SoCs and cellular modem/RF, plus the dominant 3G/4G/5G patent licensor. Two reporting engines: **QCT** (chips — Handsets, Automotive, IoT) and **QTL** (licensing). FY25 revenue $44.3B, +14% YoY (10-K, 2025-11-05). QCT $38.4B (Handsets $27.8B / Auto $4.0B / IoT $6.6B); QTL ~flat YoY but ~70%+ EBT margin and the bulk of pre-tax profit. The structural debate: Handsets (≈72% of QCT) is a mature, China-heavy, Apple-eroding base, so the equity story rests on **diversification** (auto Snapdragon Digital Chassis, IoT/edge-AI, Snapdragon X PCs) and a nascent **data-center CPU / AI-inference** push offsetting Apple's modem in-sourcing.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Handset Snapdragon SoCs + modem/RF ($27.8B) · 2) QTL cellular-IP licensing (bulk of pre-tax profit) · 3) Automotive Snapdragon Digital Chassis |
| **Main buyer(s)** | Smartphone OEMs — Samsung (>70% Snapdragon), Xiaomi/China OEMs, Apple (declining); Apple, Samsung & Xiaomi each ≥10% of FY25 revenue |
| **Key suppliers** | TSMC / Samsung foundry (fabless); ASE / Amkor assembly & test |

## Position in the value chain
QCOM is fabless: it designs Snapdragon SoCs, modem/RF and auto/IoT silicon (built at TSMC/Samsung foundries) and sells to smartphone, auto and PC OEMs, while QTL monetizes its cellular IP across the industry regardless of who makes the chip. Key tension: **Apple is in-sourcing its baseband modem** ("we expect that Apple will increasingly use its own modem products… which will have a significant negative impact on our QCT revenues" — 10-K FY25), pushing QCOM to diversify non-handset revenue (auto exiting FY26 at a >$6B run-rate; data-center shipments to a hyperscaler starting Dec-2026). On the DC side, QCOM is now positioned as an **ARM-based merchant data-center vendor**: it launched the **AI200/AI250 inference-optimized accelerator cards and rack solutions on 2026-10-27** (PCIe for scale-up; AI200 commercial 2026, AI250 in 2027) (TD Cowen, 2025-10-27), and is one of two named CPU-side partners (with Fujitsu) on NVIDIA's **NVLink Fusion**, which extends NVLink to third-party CPUs/accelerators (MS Scale-up primer). First DC design win surfaced: **HUMAIN targeting 200MW from 2026 using QCOM AI200/AI250 rack solutions** (JPM, 2025-11/Oct-25).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Arial, sans-serif" font-size="11">
  <defs>
    <marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Suppliers -->
  <rect x="10" y="70" width="150" height="80" rx="6" fill="#eef3fb" stroke="#3b6db5"/>
  <text x="85" y="92" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="110" text-anchor="middle">TSMC / Samsung</text>
  <text x="85" y="125" text-anchor="middle">foundry (fabless)</text>
  <text x="85" y="140" text-anchor="middle">ASE/Amkor assy</text>
  <!-- Qualcomm -->
  <rect x="240" y="40" width="220" height="140" rx="6" fill="#fff3e0" stroke="#d98324"/>
  <text x="350" y="62" text-anchor="middle" font-weight="bold">QUALCOMM (QCOM)</text>
  <text x="350" y="82" text-anchor="middle">QCT: Snapdragon SoC +</text>
  <text x="350" y="97" text-anchor="middle">modem/RF</text>
  <text x="350" y="115" text-anchor="middle">Auto (Digital Chassis)</text>
  <text x="350" y="130" text-anchor="middle">IoT / edge-AI / PC X2</text>
  <text x="350" y="150" text-anchor="middle" font-style="italic">QTL: cellular IP licensing</text>
  <text x="350" y="168" text-anchor="middle">Data-center CPU (2027+)</text>
  <!-- Customers -->
  <rect x="540" y="40" width="170" height="140" rx="6" fill="#eafaf0" stroke="#2e8b57"/>
  <text x="625" y="62" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="625" y="82" text-anchor="middle">Samsung (&gt;70% SD)</text>
  <text x="625" y="98" text-anchor="middle">Xiaomi, China OEMs</text>
  <text x="625" y="116" text-anchor="middle">Apple (declining —</text>
  <text x="625" y="130" text-anchor="middle">modem in-sourcing)</text>
  <text x="625" y="150" text-anchor="middle">Auto OEMs (VW/Audi)</text>
  <text x="625" y="166" text-anchor="middle">PC OEMs (Snapdragon)</text>
  <!-- arrows -->
  <line x1="160" y1="110" x2="238" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="460" y1="110" x2="538" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arr)"/>
  <text x="200" y="103" text-anchor="middle" font-size="10">wafers</text>
  <text x="500" y="103" text-anchor="middle" font-size="10">chips + IP</text>
  <text x="350" y="205" text-anchor="middle" font-size="10" fill="#b00">Headwind: Apple modem in-sourcing · Offset: auto + IoT/edge-AI + data-center diversification</text>
</svg>

## Current state (latest quarter)
**2026 Investor Day — June 24, 2026 (New York) — the datacenter pivot quantified.** QCOM raised **FY29E non-handset revenue to $40B** (from $22B prior) — DC $15B+ / Auto $10B / IoT $14B+ — anchored by a new **$15B+ DC revenue target** with **$5B guided for FY27** (vs ~$300M F26), backed by **two global hyperscaler custom-silicon deals (each >$1B)**. Proof points: **MSFT deploying QCOM HBC (High Bandwidth Compute) XPU solutions inside Azure** (Satya Nadella confirmed live on stage); **META signed an MOU for the Dragonfly C1000 CPU** to power its next-gen server fleet (production 2H2028); AI-accelerator/connectivity ramp from 2H FY27. Non-handset reaches **~50% of revenue FY27 / ~65%+ FY29** (from ~30%); **FY29E non-GAAP EPS target >$18** (vs consensus $14-15); longer-term DC ambition ~$50B at 5%+ share within 5-7 years in a $1T+ 2029 DC TAM. Auto design-win pipeline raised **$45B→$65B**. QCOM also acquired **Modular (~$4B)** for its open software stack (Mojo language / MAX inference engine) to compete with CUDA. Stock +~10% on the event. (Sources: JPM / Joseph Cardoso; MS / Joseph Moore; Citi / Atif Malik; Barclays / Tom O'Malley; BofA / Vivek Arya, 2026-06-25; @PatrickMoorhead live tweets, 2026-06-24.)

**Q2 FY26 (reported 2026-04-29, quarter ended 2026-03-29)** — Revenue $10.6B, **-3% YoY**; non-GAAP EPS $2.65 (high end of guide). QCT $9.1B (10-Q QCT total $9.08B; **Handsets $6.02B, -13% YoY**; Auto $1.33B, +38%; IoT $1.73B, +9%). QCT EBT margin compressed to **27%** (from 30%). QTL $1.4B at 72% EBT margin (+5% YoY on better mix). GAAP net income $7.4B was flattered by a **$5.7B income-tax benefit** releasing the DTA valuation allowance that had been charged in Q4 FY25 — not operating strength (10-Q, 2026-04-29).
- **Guidance Q3 FY26:** revenue $9.2–$10.0B, non-GAAP EPS $2.10–$2.30; QCT $7.9–$8.5B. CFO: China handset revenue "will reach a bottom in the third quarter" (Q2 FY26 call).
- **Demand read-through (light):** amid the broad CPU/compute shortage, Conor's Asia checks see **no signs of Qualcomm cutting orders** — "any compute is good" — with Qualcomm also marketing its own ARM-based servers (Redburn "Conor O'Mara Asia Trip Takeaways", 2026-06-23).
- **Diversification proof points:** Automotive crossed >$5B annualized for the first time, exiting FY26 at a >$6B run-rate; data-center initial shipments to a leading hyperscaler expected **December**, framed margin-accretive (Q2 FY26 call). VW Group (Audi/Porsche) LOI signed (Q1 FY26 call). Snapdragon X2 → 150 PC designs targeted for 2026.

## Debate / thesis
- **Bull:** Diversification is real and accelerating — Auto +38% YoY, FY29 Auto+IoT target $22B; data-center CPU/inference optionality (Alphawave Semi + Ventana acquisitions, first hyperscaler shipments Dec-26) opens a new TAM; QTL remains a high-margin cash engine; capital return ~$3.7B/quarter. Server-CPU thesis circulated buy-side (CPU:GPU ratio toward 1:1 in agentic AI; lead times stretching) (@fundaai, briefing 2026-05-15). **JPM (Samik, OW, 2025-12-15)** frames the bull case as a re-rating from a mid-teens to a **low-20x multiple** driven by the revenue-mix shift away from smartphones, with the DC opportunity (starting FY27) reaching a multi-billion-dollar level by ~FY28 — putting QCOM "into the elite club of data center silicon providers"; auto ADAS/AD is ~1/3 of the $45B design-win pipeline. Server-CPU TAM ~$27B CY25 → ~$60B CY30E with ARM taking 20%+ server share by CY30E (BofA, 2026-02-23). At JPM's TMC conference QCOM struck a "very bullish tone" on the data-center compute TAM, outlining **four sockets it is pursuing**: (1) **custom ASIC** (the announced hyperscaler win, ramping end-2026 into 2027 — explicitly framed "like MediaTek on Google TPU"), (2) **CPUs** (using ARM IP, claiming it can exceed ARM's own vertically-integrated CPU performance), (3) **accelerators**, and (4) **connectivity chips from Alpha Wave**; the custom ASIC ramps first with CPU/accelerator layering in over time, the wins span **both US and Chinese hyperscalers** (ByteDance speculated in press), a single customer is expected to adopt multiple sockets over time (an amplifier effect), and QCOM quantified this as **multi-billion dollars in 2027** (JPM "Conf feedback," 2026-05-22). Citi reads the first custom-silicon win as **likely an LPU inference chip, "most likely with someone like Google,"** consistent with Marvell also having an LPU program — i.e. hyperscalers engaging ASIC providers beyond Broadcom/MediaTek (Citi "MSFT C1Q26 recap," 2026-04-30). Channel color corroborates a real **automotive design moat**: a German auto Tier-1 expert described QCOM as **having "a monopoly… in certain product lines,"** so OEMs are "forced to work with a company like Qualcomm," and named QCOM (with Infineon) as one of the only chipset suppliers compatible with **ASIL-D zonal controllers** — NXP/STM "don't stand a chance at the moment to work on these product lines." Qualcomm runs a **standardized-part, higher-margin model** (vs NXP/TI customizing to the OEM), and sits at the top of the price stack — the expert pegged a **15–20% price delta vs NXP / Chinese suppliers** (Expert call, 2026-06-08). Fresh custom-silicon read: **ByteDance is reportedly finalizing its next-gen in-house CPU by early 2027 (MP targeted 2H27) and may tap Qualcomm to help make it** (TrendForce, 2026-06-30) — a potential incremental datapoint on the "US + Chinese hyperscaler" custom-ASIC wins QCOM referenced.
- **Bear:** Handsets still ~70% of QCT and shrinking — Apple modem in-sourcing is an explicit, management-acknowledged "significant negative" (10-K FY25). **JPM sizes the Apple in-sourcing drag at a $6-7B revenue headwind over the next few years**, "likely to overwhelm most of the growth in other parts of the business," so share-price outcomes hinge on DC roadmap updates (JPM, 2025-12-15); JPM also flags QTL litigation risk and the challenge of managing the cost base to a lower revenue run-rate while ramping DC investment. **UBS (Arcuri, Neutral) is the skeptic:** smartphones stay **>50% of OP even in CY27/28**; QCOM "can be a player in data center" but it is "at best several years away from moving the needle," and the adjacencies "are still not needle moving and Street estimates already seem to assume this outcome," so UBS sees no path to a sustained estimate-revision cycle (UBS, prices 12/19/25). UBS sizes the internal-competition risk: **Apple modem ~$5B, QTL license cessation ~$1.5B, Samsung ~$1B**. China handset units soft on the DRAM/memory shortage (Q1/Q2 FY26 calls). **Memory-supply allocation is now an explicit bear axis: Citi ranks QCOM at the BOTTOM of its AI-compute-semis stack despite the HBC announcement** — because QCOM's High Bandwidth Compute uses a stack of **LPDDR** memory and Citi sees QCOM with **limited memory allocation until 2029** in a DRAM-shortage-constrained world (Citi / Atif Malik, "Compute Semis: DRAM Supply Is the New Ranking Metric," 2026-06-29). The rally was called the "problem child" of the chip complex — Tae Kim newsletter flagged +80% off lows as overdone given DC ambition; **QCOM -11% on 2026-05-13** (briefing 2026-05-13). AMD overtook QCOM in semi revenue in 1QC26 with the gap "widening from here" (@SKundojjala, briefing 2026-05-06). Citi's read on the QCOM print is a clean statement of the bull/bear split: **estimates are coming down** (70% of sales still smartphone-exposed; QCOM missed the Sept quarter on smartphone weakness), yet the **stock re-rated up on multiple expansion** (off ~12x) purely on the custom-silicon teaser — with **short interest at a high** and China Android guided to bottom in the June quarter; the data-center detail is gated until QCOM's **June 24 investor day** (Citi "MSFT C1Q26 recap," 2026-04-30). On the PC side, FinTwit skepticism persists that a strong local-PC LLM showdown (3-4 yrs out) will be between NVIDIA's RTX Spark and Apple — "Qualcomm? Nope" (@firstadopter, 2026-06-29).
- **Where the Street stands:** Bifurcated, no longer a blank — **JPM OW** (Samik Chatterjee, QCOM ~$178 12/2025) on the diversification re-rate thesis, vs **UBS Neutral, PT $185** (raised from prior $175), ~6% implied upside, "hard to get excited" on the transition overhang (Arcuri, 12/19/25). The disagreement is precisely on whether DC/diversification can outrun the Apple drag and force estimate upgrades (JPM yes / UBS no). Briefing color stays mixed-to-cautious: JPM ran a QCOM bogey survey into the print (briefing 2026-05-12); semis broadly flagged extended (R&Co: "63% above 200d, largest since Dot-Com," briefing 2026-05-12). Longer-term modem-displacement read-through repeatedly cited vs Intel 14A smartphone wins (briefing 2026-05-14).
- **Where the Street stands — post-Investor Day (2026-06-25):** the DC pivot is now more credible, but the FY29 ramp stays a "show-me" story for most.
  - **MS (Joseph Moore):** **upgraded UW→EW; PT $146→$231.** "We have been wrong to be skeptical"; "$5bn of guidance for AI in FY27 from a proven management team clearly pushes them into the AI beneficiaries category," $15B FY29 "aspirational" — but remains mindful of smartphone headwinds (MS / Joseph Moore, 2026-06-25).
  - **Citi (Atif Malik):** Neutral; PT **$160→$198**. "Lifts L/T Model and Target EPS >$18 by F29"; 20x F28 EPS (above 3yr avg) for DC traction; maintains Neutral on handset softness from memory costs (Citi / Atif Malik, 2026-06-25). Reaffirmed cautious on 2026-06-29: ranks QCOM **at the bottom** of the AI-compute-semis order (DRAM-allocation-driven), HBC on LPDDR with limited allocation until 2029.
  - **BofA (Vivek Arya):** Underperform (maintained); PO **$195→$220**. "Investor Day impresses, but AI execution still unproven"; FY29E non-handset $40B; SOTP 16x blended CY28E PE; China/Apple-QTL/DC-execution risks remain (BofA / Vivek Arya, 2026-06-25).
  - **JPM (Joseph Cardoso):** Neutral; PT $265 (unch.). QCOM provided evidence it can be "a genuine data center winner" ($5B FY27→$15B+ FY29, HBC, hyperscaler engagements, Modular), share ambitions to 5%+ (~$50B in 5-7yr) — tempered by "candid acknowledgement of near-term" execution challenges (JPM / Joseph Cardoso, 2026-06-25).
  - **Barclays (Tom O'Malley):** Underweight (maintained); PT $150. "All Eyes on DC"; MSFT HBC + META C1000 + two unnamed hyperscalers confirmed; "two named customers seem like enough for the stock to work" but remains a "show-me story in a highly competitive market" (Barclays / Tom O'Malley, 2026-06-25).
  - **GS (James Schneider):** Neutral; PT **$180 (raised, from $145)** — 15x P/E (up from 12x on higher datacenter revenue) on normalized EPS **$12.00 (up from $11.00)**; FY26 EPS est **$10.73 (from $10.70)**. GS **raised estimates ~10% on average** post the QCOM Investor Day (modeling $5bn/$8.2bn DC revenue FY27/28), **raised auto estimates and cut handset**. Names QCOM among its tactical *downside* ideas into 2Q (with KLAC, ARM) — DC re-rate ahead of the proof, 70% of sales still handset (Goldman Sachs "2Q Preview: Expect broad upside...", 2026-07-05).

## Catalysts / what to watch
- **DC ramp execution (post-Investor Day, 2026-06-24)** — the $5B FY27 → $15B+ FY29 DC trajectory is the new central watch item: AI accelerator/connectivity ramp begins **2H FY27**; **META Dragonfly C1000 CPU production 2H2028**; MSFT Azure HBC deployment; the two unnamed hyperscaler custom-silicon wins (each >$1B). Progress toward non-handset ~50% FY27 / ~65%+ FY29 and FY29E EPS >$18 (broker post-event notes, 2026-06-25).
- **Memory/DRAM allocation for HBC** — Citi's new "DRAM supply is the ranking metric" frame makes QCOM's LPDDR allocation (limited until 2029) a gating variable for the AI200/AI250/HBC ramp (Citi, 2026-06-29).
- **ByteDance custom-CPU engagement** — reportedly finalizing next-gen in-house CPU by early 2027, MP 2H27, possibly tapping QCOM (TrendForce, 2026-06-30) — watch for confirmation as a possible Chinese-hyperscaler custom-silicon win.
- **Modular (~$4B) acquisition close** — open software stack (Mojo/MAX) to compete with CUDA; integration alongside Ventana (RISC-V) (JPM / Joseph Cardoso, 2026-06-25).
- **Q3 FY26 print** (late Jul-2026) — does China handset trough confirm; QCT margin trajectory.
- **Data-center first shipments** to lead hyperscaler — December 2026; any DC revenue disclosure (FY27 ramp guided on Q1 FY26 call). AI200 commercial in 2026, AI250 in 2027 (TD Cowen, 2025-10-27); HUMAIN 200MW ramp from 2026 (JPM).
- **DC roadmap updates** — JPM argues share-price outcomes are "dictated by updates on the datacenter silicon roadmap and revenue opportunities" (JPM, 2025-12-15).
- **Apple modem share** — QCOM held "20% share assumption for fall Apple phones" (Q2 FY26 call); watch the glidepath as Apple's in-house modem scales toward the $6-7B (JPM) / ~$5B+$1.5B QTL (UBS) at-risk base.
- **Auto run-rate** — exit FY26 >$6B; FY29 Auto+IoT $22B target progress; ADAS/AD ~1/3 of the $45B design-win pipeline (JPM).
- **Memory/DRAM availability** — gating China handset units near-term.
- **6G** — coalition launched; silicon 2028, launches 2029 (long-dated).

## Risks
- **Apple modem in-sourcing** — explicit material headwind to QCT (10-K FY25); JPM $6-7B revenue over next few years; UBS ~$5B modem + ~$1.5B QTL license cessation.
- **Customer concentration** — Apple, Samsung and Xiaomi each ≥10% of consolidated revenue in FY25 (10-K).
- **China exposure** — large share of handset demand; Huawei export license revoked, no further product revenue expected; share shifts to Huawei-supplied OEMs a risk (10-K).
- **QTL durability** — licensing renewals / per-unit royalty caps / regulatory scrutiny / customer litigation; QTL carries the profit mix (JPM, UBS).
- **Customer in-house silicon** — competition "from products internally developed by our customers, including some of our largest customers" (10-K).
- **Premium-tier cyclicality + memory pricing** — DRAM shortage constraining handset units (Q1/Q2 FY26 calls).
- **Data-center execution** — unproven entry into an entirely new market vs entrenched x86/ARM incumbents; ecosystem/software support still ~80-90% x86 in CY26E (BofA); revenue not until FY27. Memory allocation (LPDDR for HBC) limited until 2029 is a supply-side gate (Citi, 2026-06-29).
- **PC push** — faces AMD/INTC competition and lacks an edge-AI "killer app"; tariff-related demand destruction a risk to adjacent markets (UBS).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **Citi (Atif Malik) — "US Semiconductors: Compute Semis: DRAM Supply Is the New Ranking Metric; NVDA & AMD on Top; QCOM at the Bottom"** _(2026-06-29)_: post-1Q ranking update; AI compute undersupplied (AWS EC2 GPU +20% price hike); DRAM shortage the biggest supply constraint. Ranks by memory-allocation weight — mega-caps: NVDA #1 (HBM partnerships), then AVGO (TPUs ~85% memory fulfillment); large caps: AMD #1 (Samsung/Micron), CBRS #2 (SRAM). **QCOM ranked at the bottom** despite the HBC announcement — HBC uses an LPDDR stack and Citi sees limited memory allocation to QCOM until 2029.
- **JPM (Samik Chatterjee) — Hardware & Networking, 2025-12-15** _(OW)_: long-term re-rating from diversification (PC/IoT/auto/DC); Apple modem in-sourcing a $6-7B headwind; share-price outcomes "dictated by" DC roadmap updates; multi-billion DC revenue by ~FY28.
- **UBS (Tim Arcuri) — 2026 US Semis overview** _(Neutral, PT $185, prices 12/19/25)_: smartphones >50% of OP through CY27/28; DC "several years away from moving the needle," offers an inferencing chip but adjacencies "not needle moving"; no sustained estimate-revision cycle.
- **UBS (Tim Arcuri) — 'Qualcomm: Animal Spirits Evident, But Still A Company In Transition'** _(2026-04-30)_: data-center entry could stir animal spirits, but 'hard to get excited' — handset/Apple-modem transition overhang.
- **Samik (JPM) QCOM/MediaTek call** (repo): handset/China + diversification (auto/PC/edge-AI) debate.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q2 FY26 print + intra-quarter · Apr 29 → Jun 30, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q2 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Data center / diversification** | Initial hyperscaler shipments in December; margin-accretive | JPM/Samik: "very bullish" tone, 4 sockets (custom ASIC "like MediaTek on TPU", ARM CPU, accelerators, Alphawave connectivity), multi-billions in '27, US+China · Citi/Malik: 1st win likely an LPU "like Google" · TrendForce: ByteDance may tap QCOM for its next-gen CPU | **✓ confirms** (optimistic on the roadmap) |
| **DC memory / HBC supply** | HBC on LPDDR; DC margin-accretive | Citi/Malik (06-29): QCOM ranked bottom of AI-compute stack — HBC LPDDR, limited memory allocation until 2029 | **⚠ nuance** (supply-gated ramp) |
| **Handsets / China** | Handset ~$6.0B; China bottoms in Q3 | Citi/Malik: 70% of sales still smartphone, estimates coming down, missed the Sept quarter · Redburn/O'Mara: no signs of QCOM cutting orders in Asia | **⚠ nuance** (bottom still "show-me") |
| **Automotive** | Auto $1.3B (+38%); >$5B annualized, exits FY26 >$6B | German Tier-1 expert call: QCOM a "monopoly in certain lines", OEMs "forced to work with Qualcomm"; only one (with Infineon) in ASIL-D, 15-20% premium vs NXP/Chinese players | **✓ confirms** (pricing moat) |
| **Equity re-rating** | Diversification (DC/auto/IoT) justifies a higher multiple | Citi/Malik: re-rate (from ~12x) purely on the custom-silicon "teaser" · Tae Kim: "problem child", +80% off the lows overdone, -11% on May-13 · @SKundojjala: AMD overtakes QCOM in semi revenue | **✗ contests** (multiple ahead of the proof) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 04-30 | Citi · Malik | competition | mixed | Citi reads the first custom-silicon win as likely an LPU inference chip "very likely with someone like Google," consistent with Marvell also having an LPU program — hyperscalers engaging ASIC providers beyond Broadcom/MediaTek ("MSFT C1Q26 recap"). |
| 04-30 | Citi · Malik | valuation | bear | Citi: estimates are coming down (70% of sales still smartphone; QCOM missed the September quarter on smartphone weakness), but the stock re-rated up on multiple expansion (from ~12x) purely on the custom-silicon teaser — with short interest rising and data-center detail held back until the Jun-24 investor day ("MSFT C1Q26 recap"). |
| 05-06 | @SKundojjala | competition | bear | AMD overtook QCOM in semi revenue in 1QC26 with the gap "widening from here" (briefing). |
| 05-13 | Tae Kim newsletter | valuation | bear | The rally was called the "problem child" of the chip complex — +80% off the lows seen as overdone given the DC ambition; QCOM -11% on May-13 (briefing). |
| 05-15 | @fundaai | demand | bull | A server-CPU thesis circulated on the buy-side (CPU:GPU ratio heading toward 1:1 in agentic AI; lead times stretching) as optionality for QCOM (briefing). |
| 05-22 | JPM · Samik Chatterjee | product | bull | At JPM's TMC conference, QCOM struck a "very bullish tone" on the DC compute TAM, outlining four sockets: (1) custom ASIC (the announced hyperscaler win, ramping late-2026 into 2027, "like MediaTek on Google TPU"), (2) CPUs (ARM IP), (3) accelerators, (4) Alphawave connectivity; wins at US and China hyperscalers, multi-billions in 2027 ("Conf feedback"). |
| 06-08 | Expert call · auto Tier-1 | competition | bull | German Tier-1 expert described QCOM as having "a monopoly in certain product lines," with OEMs "forced to work with Qualcomm"; named QCOM (with Infineon) as one of the only ones compatible with ASIL-D zonal controllers (NXP/STM "have no chance"). Standardized higher-margin model, 15-20% price premium vs NXP/Chinese players. |
| 06-23 | Redburn · Conor O'Mara | demand | bull | Amid the broad CPU/compute shortage, checks in Asia see no signs of QCOM cutting orders — "any compute is good" — with QCOM also marketing its own ARM servers ("Conor O'Mara Asia Trip Takeaways"). |
| 06-25 | Bernstein AM Note | valuation | bull | Bernstein AM Note (Chris Brady, 2026-06-25): QCOM flagged as positive on the day — context is the post-Investor Day reaction, with the $5B FY27 DC guide and MSFT/META design wins the catalysts (Bernstein AM, 2026-06-25). |
| 06-26 | @dnystedt (FinTwit) | produto | bull | **TSMC expected to manufacture QCOM's Dragonfly C100 data-center CPUs and AI300 AI accelerators on TSMC 3nm/2nm, using CoWoS or SoIC advanced packaging** — per media reports. Confirms TSMC as the foundry for the DC business that is central to the QCOM re-rating thesis; CoWoS/SoIC packaging aligns with the high-compute architecture of the Dragonfly/AI300 stack. (@dnystedt, 2026-06-26) |
| 06-24 | QCOM Investor Day / press | demand | bull | **META multi-generation custom CPU deal confirmed at QCOM Investor Day** — Meta confirmed as the first big-tech customer for QCOM's data-center CPUs (Dragonfly C1000), with a multi-generation commitment. Satya Nadella (MSFT) appeared personally to endorse the QCOM HBC XPU for Azure deployments. Combined: Meta (CPU) + MSFT (HBC XPU) = two of the five hyperscalers now publicly committed to QCOM silicon in the DC — ahead of the prior investor-day expectation of a single customer win. FY29E revenue target: $40B non-handset ($15B DC / $10B Auto / $14B IoT); $5B FY27 DC guide. (QCOM Investor Day / compiled briefing, 2026-06-24 event / 2026-06-27 compiled) |
| 06-27 | Compiled briefing / sell-side | product | bull | **Modular AI software acquisition confirmed ($4B)** — QCOM's acquisition of Modular (AI software/compiler company) confirmed, strategic rationale: (1) Modular's Max Engine compiler optimizes inference for heterogeneous hardware (Snapdragon, Dragonfly, ARM) — solving the QCOM software-stack gap that has historically held back adoption vs NVDA CUDA; (2) ~$4B price signals QCOM's commitment to owning the full stack (hardware + software + compilers) for the DC and edge; (3) reduces customer friction in porting AI workloads to QCOM silicon. Bull: removes the primary bear objection (lack of a mature software ecosystem). Bear: $4B at a pre-revenue AI software company is a large outright bet before the hardware itself ramps. (Compiled briefing, 2026-06-27; QCOM announcement 2026-06-24) |
| 06-29 | Citi · Atif Malik | supply | bear | **"DRAM Supply Is the New Ranking Metric" — QCOM ranked at the bottom** of the AI-compute-semis stack. AI compute undersupplied; DRAM shortage the biggest supply constraint. Citi weights the ranking on memory allocation: NVDA/AVGO top of mega-caps, AMD top of large-caps. QCOM last **despite the HBC announcement** — HBC uses an LPDDR memory stack and QCOM has **limited memory allocation until 2029**. A clean supply-side bear counterpoint to the post-Investor-Day DC bull case. (Citi / Atif Malik, 2026-06-29) |
| 06-30 | @trendforce (FinTwit) | product | bull | **ByteDance reportedly finalizing its next-gen in-house CPU by early 2027 (MP targeted 2H27) and may tap Qualcomm to help make it.** Read-through: a potential Chinese-hyperscaler custom-silicon win consistent with QCOM's "US + Chinese hyperscaler" custom-ASIC framing at the TMC conference / Investor Day; still a media report, not confirmed. (@trendforce, 2026-06-30) |
| 07-02 | DIGITIMES | competicao | mixed | **"Qualcomm's Dragonfly raises the stakes, but MediaTek's TPU and ASIC ties keep it in the race."** DIGITIMES frames the freshly launched Dragonfly platform as a deeper QCOM push into cloud AI, intensifying competition — but reads [MediaTek](MEDIATEK.md)'s entrenched Google-TPU / custom-ASIC relationships as a durable moat vs QCOM's still-nascent DC entry. Confirms the DC push is real and escalating, but tempers the share-capture expectation near-term. (DIGITIMES, 2026-07-02) |
| 07-05 | GS · James Schneider (Semis 2Q Preview) | valuation | bear | GS **Neutral, PT raised to $180 (from $145)** — 15x P/E (up from 12x) on normalized EPS **$12.00 (from $11.00)**; FY26 EPS est **$10.73 (from $10.70)**; **raised estimates ~10% on avg** post Investor Day ($5bn/$8.2bn DC rev FY27/28), **raised auto, cut handset**. Names QCOM among its tactical *downside* ideas into 2Q (with KLAC, ARM) vs upside AMAT/AMD/ON — DC re-rate ahead of the proof, 70% of sales still handset; SOX +88% vs SPX +14% "raised the bar." (Goldman Sachs "2Q Preview: Expect broad upside...", 2026-07-05) |
| 07-08 | JPM · Gokul Hariharan (TSMC 2Q26 preview) | product | mixed | **TSMC-preview read-through for QCOM (two light datapoints).** (1) **Mid-range 4nm mobile demand cut** — Android brands (memory-cost + price-sensitive tiers) have already given up mid-range 4nm volume; TSMC reallocated that capacity to CPU/accelerator — a demand negative for QCOM's mid-range mobile-SoC base. (2) **Google's next-gen TPU packaging "Qualcomm or MediaTek"** — Gokul names **Qualcomm as a possible partner** for the next Google TPU (which stays on CoWoS, not SOIC), consistent with QCOM's "US + Chinese hyperscaler" custom-silicon framing. (JPM · Gokul "TSMC 2Q26 preview", 2026-07-08) [Source](../relat%C3%B3rios%20bons/2026_07_08_gokul_preview_tsmc_2q26.html) |

**Quarter synthesis:** post-Investor Day (Jun-24), the debate is "is the $5B FY27 DC guide credible and at what multiple should QCOM trade?" — MS upgraded UW→EW ("We have been wrong to be skeptical"), Citi raised PT but stays Neutral, BofA/Barclays cautious, JPM Neutral at $265. Supply-chain (TSMC Dragonfly/AI300 foundry, 06-26), software (Modular $4B, 06-27) and customer proof (META/MSFT, 06-24) were more positive than expected. The two newest datapoints cut opposite ways: **06-29 Citi** adds a clean bear counterpoint — QCOM ranked *bottom* of the AI-compute stack on **memory allocation** (HBC on LPDDR, limited until 2029), a supply-side gate the DC bull case had not priced; **06-30 TrendForce** adds a bull optionality — **ByteDance may tap QCOM** for its next-gen CPU, a possible Chinese-hyperscaler win. Net remaining debate: execution timing + FY29E $40B credibility, now with memory allocation as an added constraint.

## Management commentary — evolution (last 4 quarters)

| Theme | Q3 FY25 (2025-07-30) | Q4 FY25 (2025-11-05) | Q1 FY26 (2026-02-04) | Q2 FY26 (2026-04-29) |
|---|---|---|---|---|
| Handsets / China demand | QCT chips $9.0B; handsets growing | Q4 QCT $9.8B (+9% QoQ), premium Android | Record handset $7.8B; China cutting inventory | Handset ~$6.0B; China to bottom in Q3 |
| Automotive | Auto +21% YoY; FY29 Auto+IoT $22B | Record auto qtr >$1B; FY25 auto +36% | Auto $1.1B (+15%); VW Group LOI signed | Auto $1.3B (+38%); >$5B annualized, exit >$6B |
| IoT / edge-AI / PC | IoT +24% YoY | FY25 IoT +22%; Wi-Fi 7, FWA, glasses | IoT $1.7B (+9%); Snapdragon X2, 150 PCs 2026 | IoT $1.7B (+9%); auto+IoT +20% YoY |
| Data center / diversification | Non-Apple QCT >15% growth framing | DC ambition central long-term story | Alphawave + Ventana closed; DC rev in 2027 | Hyperscaler shipments in December; margin accretive |
| Apple modem in-sourcing | — | Reiterates non-Apple QCT growth offset | — | No change to 20% share on fall Apple phones |
| Memory / DRAM constraint | — | — | DRAM shortage constrains handset units | DRAM still pressuring handset units |

_Source: QCOM earnings calls (dates above); management commentary, paraphrased._

## Changelog
- 2026-07-10 — Added 1 light intra-quarter row (**JPM · Gokul "TSMC 2Q26 preview", 2026-07-08**): (1) mid-range **4nm mobile demand cut** (Android brands, memory-cost/price sensitivity) — a demand negative for QCOM's mid-range mobile-SoC base; (2) **Google's next-gen TPU packaging "Qualcomm or MediaTek"** — QCOM named as a possible Google-TPU partner, consistent with the "US + Chinese hyperscaler" custom-silicon framing already on the page. Full-log row + Sources link. Additive; no figure superseded.
- 2026-07-05 — Added the full **GS "2Q Preview" (Schneider, 07-05)** datapoint: **GS Neutral, PT $180 (raised, from $145)** — 15x P/E (from 12x) on normalized EPS $12.00 (from $11.00); FY26 EPS est $10.73 (from $10.70); GS raised estimates ~10% on avg post Investor Day, raised auto / cut handset. Added a bullet to "Where the Street stands — post-Investor Day," enriched the 07-05 intra-quarter row, and added the Sources link. QCOM remains a GS tactical *downside* idea (with KLAC, ARM). First GS rating/PT on the page — no prior GS figure superseded.
- 2026-06-30 — Added 2 intra-quarter rows: **Citi (06-29) "DRAM Supply Is the New Ranking Metric" — QCOM ranked at the bottom** (HBC on LPDDR, limited memory allocation until 2029) added to Bear thesis, Citi stance, Catalysts, Risks, Signal-vs-management (new DC memory/HBC supply row) + full log; **TrendForce (06-30) ByteDance may tap QCOM for next-gen CPU** added to Bull thesis, Catalysts + full log. Also added @firstadopter PC-LLM skepticism to Bear. Updated quarter synthesis. No PT/rating superseded.
- 2026-06-27 — Added 2 intra-quarter rows (06-27 compiled briefing highlighting 06-24 Investor Day outputs): META multi-generation CPU deal + MSFT HBC endorsement (two hyperscalers publicly committed); Modular AI acquisition ($4B, software-stack completion). Updated quarter synthesis to reflect these as de-risking the $5B FY27 DC guide.
- 2026-06-25 — Folded in the 2026 Investor Day (held 2026-06-24) and post-event sell-side reactions from research-wiki source. Added the FY29E $40B non-handset target ($15B DC / $10B Auto / $14B IoT), $5B FY27 DC guide, MSFT HBC / META C1000 proof points, Modular (~$4B) acquisition, and post-event PT moves to Debate/thesis and Catalysts. **Superseded ratings/PTs (moved here):** the prior "Where the Street stands" snapshot of JPM OW ~$178 (12/2025) and UBS Neutral $185 (12/19/25) is now stale — current post-event coverage: MS upgraded UW→EW $146→$231; Citi Neutral $160→$198; BofA U/P $195→$220; JPM Neutral $265; Barclays UW $150.

## Sources
- **Filings:** [10-K FY25](../QCOM/QCOM_10-K_2025-11-05_0000804328-25-000085.html) · [10-Q Q2 FY26](../QCOM/QCOM_10-Q_2026-04-29_0000804328-26-000061.html).
- **Transcripts:** [Q2 FY26](../QCOM/transcripts/QCOM_Q2-FY26-earnings_2026-04-29.md) · [Q1 FY26](../QCOM/transcripts/QCOM_Q1-FY26-earnings_2026-02-04.md) · [Q4 FY25](../QCOM/transcripts/QCOM_Q4-FY25-earnings_2025-11-05.md) · [Q3 FY25](../QCOM/transcripts/QCOM_Q3-FY25-earnings_2025-07-30.md).
- **Research reports (relatórios bons):**
  - [UBS 2026 US Semis overview](../relat%C3%B3rios%20bons/UBS_2026_overview.html)
  - [JPM Hardware & Networking (2025-12-15)](../relat%C3%B3rios%20bons/JPM_Hardware___Networkin_2025-12-15_5155719.html)
  - [MS Scale-up primer](../relat%C3%B3rios%20bons/Scale_up_primer_MS.html)
  - [BofA US Semiconductors — CPU / ARM server](../relat%C3%B3rios%20bons/CPU.html)
  - [TD Cowen — scale-up / AI200-AI250](../relat%C3%B3rios%20bons/TDCOWEN.html)
  - [Expert call — auto analog; QCOM ASIL-D moat & pricing premium (2026-06-08)](../relat%C3%B3rios%20bons/IFXDE_-_ExpertCall_document_dated_09-06-2026.html)
  - [JPM "Conf feedback" — QCOM four DC sockets (custom ASIC/CPU/accelerator/Alpha Wave connectivity), multi-billion 2027, US+China hyperscalers (2026-05-22)](../relat%C3%B3rios%20bons/2026_05_22_jpm_conf_feedback_22_may_26.html)
  - [Citi "MSFT C1Q26 recap" — QCOM custom-silicon win likely LPU/Google; estimates down but multiple re-rate; June 24 investor day (Malik, 2026-04-30)](../relat%C3%B3rios%20bons/2026_04_30_msft_wfc_c1q26_recap_30_apr_26.html)
  - [Redburn (Conor O'Mara) — Asia Trip Takeaways (2026-06-23)](../relat%C3%B3rios%20bons/77420a6c-61c1-4757-8047-3a24cced258c_Key_Takeaways_from_Conor_OMaras_recent_Management_Meetings_across_ASIA_1.html) — no signs of Qualcomm cutting orders amid CPU/compute shortage (light read-through).
  - [GS 2Q Preview (2026-07-05)](../relat%C3%B3rios%20bons/2Q_Preview__Expect_broad_upside_but_run_in_stocks_raises_the_bar_tactical_ideas_for_earnings.html) — QCOM Neutral, PT $180 (from $145); normalized EPS $12.00 (from $11.00), FY26 EPS est $10.73; raised est ~10% (raised auto, cut handset); GS tactical downside idea.
  - [JPM · Gokul — "TSMC 2Q26 preview" (2026-07-08)](../relat%C3%B3rios%20bons/2026_07_08_gokul_preview_tsmc_2q26.html) — light read-through: mid-range 4nm mobile demand cut (Android, memory-cost/price sensitivity); Google next-gen TPU packaging possibly "Qualcomm or MediaTek."
- **Twitter/X:** @trendforce (ByteDance next-gen CPU may tap QCOM, 2026-06-30); @firstadopter / Tae Kim (PC-LLM showdown skepticism, 2026-06-29).
- **Briefings:** roll-up across `E:\briefings\2026` — QCOM "problem child"/Tae Kim substack and -11% day (2026-05-12, 2026-05-13); JPM bogey survey (2026-05-12); AMD overtakes QCOM in semi rev (2026-05-06); server-CPU thesis (2026-05-15); Intel 14A modem-displacement read-through (2026-05-14); Trump China CEO list incl. QCOM (2026-05-12).
- **Outlook:** Citi "DRAM Supply Is the New Ranking Metric" (2026-06-29) pulled from inbox; earlier sessions returned no output (Outlook COM unavailable) — other Street ratings/PTs sourced from sell-side research notes per attribution.
