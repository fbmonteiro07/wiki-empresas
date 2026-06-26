# ARM — Arm Holdings plc

_Wiki · generated 2026-06-19 · **20-F filer (UK foreign private issuer)** — files annual 20-F, no 10-K/10-Q · sources: `E:\Wiki Felipe\ARM` (20-Fs FY24–FY26 + transcripts) · `_briefings\2026` roll-up · theme [custom-asic-tpu](themes/custom-asic-tpu.md). Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof 2026-06-22 · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $5.6bn | $7.3bn |
| Gross profit | $5.5bn | $6.9bn |
| Gross margin | 98.1% | 94.2% |
| EBITDA | $2.6bn | $3.6bn |
| EPS | $1.99 | $2.79 |
| Capex | $391m | $421m |
| OCF (≈EBITDA) | $2.6bn | $3.6bn |

<svg xmlns="http://www.w3.org/2000/svg" width="326" height="88" viewBox="0 0 326 88" font-family="-apple-system,Segoe UI,Roboto,sans-serif"><text x="0" y="10" font-size="11" font-weight="600" fill="#33405c">FY1 EPS revision</text><rect x="0" y="14.0" width="20" height="44.0" rx="2" fill="#1c5fd6"/><text x="10" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="28" y="16.1" width="20" height="41.9" rx="2" fill="#1c5fd6"/><text x="38" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="56" y="15.2" width="20" height="42.8" rx="2" fill="#1c5fd6"/><text x="66" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="84" y="15.1" width="20" height="42.9" rx="2" fill="#1c7d3f"/><text x="94" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="0" y="84" font-size="10" fill="#1c7d3f">+2.2% 3m · -2.6% 6m</text><text x="176" y="10" font-size="11" font-weight="600" fill="#33405c">FY2 EPS revision</text><rect x="176" y="16.4" width="20" height="41.6" rx="2" fill="#1c5fd6"/><text x="186" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="204" y="17.2" width="20" height="40.8" rx="2" fill="#1c5fd6"/><text x="214" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="232" y="14.2" width="20" height="43.8" rx="2" fill="#1c5fd6"/><text x="242" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="260" y="14.0" width="20" height="44.0" rx="2" fill="#1c7d3f"/><text x="270" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="176" y="84" font-size="10" fill="#1c7d3f">+7.9% 3m · +5.7% 6m</text></svg>

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Arm is the upstream IP-licensing layer of the compute industry: it designs CPU/GPU/NPU architectures and processor IP and collects (i) up-front license fees and (ii) a per-unit royalty on substantially every chip shipped using its designs — typically a % of chip ASP or a fixed fee per unit, rising as more Arm IP is included (FY26 20-F, Item 4). FY26 revenue $4.92B, +23% YoY, split License & other $2.31B (47%) / Royalty $2.61B (53%); operating margin ~18% GAAP, ~49% non-GAAP in Q4 (FY26 20-F; Q4 FY26 call, 2026-05-06). The franchise is in two transitions that define the thesis: (1) royalty mix-up from ARMv9 + Compute Subsystems (CSS) lifting per-chip rates, and (2) a move *downstream* into its own silicon — the **Arm AGI CPU** launched at Q4 FY26 with Meta as lead partner. ~57% of revenue comes from top-5 customers (incl. Arm China and SoftBank); SoftBank controls Arm (~controlled-company / FPI status). Mobile app processors are ~43% of royalty (FY26 20-F).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Processor IP licenses + per-unit royalties (CPU/GPU/NPU) · 2) Compute Subsystems (CSS) + ARMv9 royalty stack · 3) Arm AGI CPU own silicon (Meta lead) |
| **Main buyer(s)** | Chip/SoC designers (Apple, Qualcomm, Nvidia, MediaTek, Samsung) + hyperscaler custom CPUs (AWS Graviton, Google Axion, MSFT Cobalt, NVDA Vera); top-5 ~57% of rev, Arm China ~16% |
| **Key suppliers** | Mostly own R&D/IP; for AGI silicon depends on TSMC foundry + ASIC design partners (Socionext, Broadcom) |

## Position in the value chain
Arm sits **upstream of nearly every SoC** in the world — virtually all smartphones, a majority of tablets/digital TVs, and a rising share of data-center CPUs run an Arm-architected core. It ships no volume silicon historically (AGI CPU is the first, production end-CY26); revenue is a **license + recurring per-unit royalty** model with a long tail (chips ship for years). The swing variable is the **server / data-center CPU TAM** — hyperscaler custom CPUs (AWS Graviton, Google Axion, Microsoft Cobalt, NVIDIA Vera/Grace) are Arm-architected, and agentic AI is lifting CPU:GPU ratios toward ~1:1.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <rect x="10" y="70" width="150" height="80" rx="6" fill="#eef3fb" stroke="#3b6cb7"/>
  <text x="85" y="100" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="120" text-anchor="middle">Own R&amp;D / IP</text>
  <text x="85" y="136" text-anchor="middle">(CPU/GPU/NPU,</text>
  <text x="85" y="150" text-anchor="middle">architecture)</text>
  <rect x="240" y="55" width="180" height="110" rx="6" fill="#dcebf7" stroke="#7b4fb7"/>
  <text x="330" y="85" text-anchor="middle" font-weight="bold">ARM</text>
  <text x="330" y="105" text-anchor="middle">CPU/GPU architecture</text>
  <text x="330" y="121" text-anchor="middle">+ IP licensing</text>
  <text x="330" y="137" text-anchor="middle">&amp; per-unit royalties</text>
  <text x="330" y="155" text-anchor="middle" font-style="italic">(now: AGI CPU silicon)</text>
  <rect x="500" y="35" width="210" height="150" rx="6" fill="#e7f6ec" stroke="#3a9d5d"/>
  <text x="605" y="60" text-anchor="middle" font-weight="bold">Customers (downstream)</text>
  <text x="605" y="82" text-anchor="middle">Apple · Qualcomm · Nvidia</text>
  <text x="605" y="98" text-anchor="middle">MediaTek · Samsung</text>
  <text x="605" y="120" text-anchor="middle" font-weight="bold">Hyperscaler custom CPUs:</text>
  <text x="605" y="136" text-anchor="middle">AWS Graviton · Google Axion</text>
  <text x="605" y="152" text-anchor="middle">Microsoft Cobalt · NVIDIA Vera</text>
  <text x="605" y="174" text-anchor="middle" font-style="italic">→ into final SoCs</text>
  <line x1="160" y1="110" x2="236" y2="110" stroke="#555" stroke-width="2" marker-end="url(#a)"/>
  <line x1="420" y1="110" x2="496" y2="110" stroke="#555" stroke-width="2" marker-end="url(#a)"/>
  <defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 Z" fill="#555"/></marker></defs>
  <text x="360" y="205" text-anchor="middle" fill="#777" font-style="italic">Upstream IP → royalty + license model · server-CPU TAM is the swing factor</text>
</svg>

## Current state (latest quarter)
**Q4 FY26 (call 2026-05-06):** revenue $1.49B (+20%); License & other $819M (+29%); Royalty $671M (+11%); non-GAAP EPS $0.60 (record); FY26 $4.92B (+23%), non-GAAP EPS $1.77. Vs Street (Capstone briefing, 2026-05-06): license beat ($780M), royalty slightly light ($691M); stock +13% in session. **Q1 FY27 guide:** rev $1.26B ±$50M (~+20%), non-GAAP EPS $0.40 ±$0.04.
- **Data center royalty more than doubled YoY** again; Arm targets a **>$100B data-center CPU TAM by 2030** as agentic AI needs >4x today's CPU capacity (Q4 FY26 call). Haas: "by the end of the decade, the largest market share by CPU type will be Arm."
- **Own silicon — Arm AGI CPU:** launched with **Meta as lead partner**; **~$2B of customer demand across FY27+FY28** (>2x the analyst-day figure), 50+ ecosystem partners (AWS, Broadcom, GCP, MSFT, NVDA, Oracle, Samsung, TSMC). FY27 AGI revenue held at ~$1B on supply constraints; first-gen GM ~30%+ (dilutive to the ~49% non-GAAP IP model). FY31 framing: ~$15B AGI + ~$10B IP, combined EPS >$9. Meta's Arm-based server CPU is **under development with Socionext** as ASIC design partner (JPM ASIC Design Services teach-in).
- **CSS the royalty engine:** CFO Child (Q3 FY26 call) — CSS could be "upwards of 50% of royalties within a couple of years"; CSS royalty rates now >10% of ASP (Q1 FY26). Royalty stacking confirmed from the SoftBank side: **v9 royalty ≈ 2x v8, and CSS ≈ 2x v9** (Jefferies Techknowledge / SoftBank takeaways, 2025-12-17). Same note flags a live monetization dispute — SoftBank says Arm is charging MediaTek the **full CSS license even where MediaTek uses only part of the IP** (CSS billed as a packaged solution); MediaTek denies using CSS.
- **Royalty/licensing guidance + cloud-share milestone (expert callback):** post-Q4 FY26, ARM is guiding **both royalty and licensing +20% YoY in fiscal Q1 (June qtr) and across FY27** (Q4 royalty was +11% on a tough MediaTek-9400 comp + low-end smartphone weakness); **cloud/AI royalty up ~2x YoY**, and Arm says its **cloud (data-center) share has reached ~50%** the way it measures it, up from near-zero at end-2020 (Grace/Vera at NVDA the big driver). Q4 licensing +29% on a major Indonesian sovereign-wealth-fund deal + two new CSS deals (one smartphone "sounds like MediaTek," one data-center networking); **ACV +22% YoY**. FY27 licensing guide includes **~$100M for the AGI chip**; AGI backlog "basically doubled in six weeks" since launch but is **memory-constrained** (N3 chip, customers can't place a TSMC PO without HBM allocation Arm can't help secure), so "AGI revenue will be more about supply than demand for the foreseeable future." Arm sees a hyperscaler roadmap to a **700-core chip** (~4x today's 284-core), with per-core ASP "not really that different" from x86 but Arm's core counts growing faster — and Arm internally pegs the **server-CPU TAM at $200-300B by 2030** on a demand basis (vs the ">$100B" it says publicly) (Expert "SiTime/ARM call," 2026-05-07).
- **Companion-CPU lever + Google Arm mix (Citi Asia checks):** the Arm storyline is most levered to **companion CPUs** (the fixed CPU:GPU ratio inside AI servers, ~99% Arm in GB-class racks). Citi's Asia checks found the **CPU mix at Google up to ~60% Arm** (Axion, higher than expected) and **Graviton ~60% of AWS's general-purpose mix** — i.e. x86 volumes structurally lower. NVIDIA's ~$20B standalone-Arm-CPU figure (Vera, ramping Q4) is "chips not memory" and likely bundles NVLink/head-node CPUs given the ASP is far above peers; the agentic-AI/RAG portion of the TAM stays more x86-native near-term (Citi "Asia recap," 2026-05-22).
- **Server-CPU TAM doubling (sell-side framing):** BofA (Arya, 2026-02-23) lifted server CPU TAM to **~$60B by CY30E from ~$27B in CY25** (+17% CAGR; AI servers ~70%/~$41B at +27% CAGR), with Arm value share to **~20-25%+ by CY30E from ~5% in CY24** (raised from prior 15-20% outlook); AMD ~40%, INTC down to ~40% from 63% CY24. SoftBank framing is more aggressive: Arm hyperscaler CPU share **~20% today, targeting ~50% by year-end** as AWS/Google/Microsoft/Alibaba shift off Intel/AMD to own chips (Jefferies Techknowledge, 2025-12-17). UBS's server-CPU-TAM note quantifies the unit-share path: **ARM server-CPU unit share rising from 16% (2025) to 42% (2030)** as agentic AI lifts CPU-bound orchestration work (planning/tool-use/retrieval), with the total server-CPU market reaching **~$170bn by 2030** (units 23m→63m, 30% CAGR) — AMD 24%→29%, Intel 60%→29% over the same span (UBS "Quantifying the server CPU opportunity", 2026-05-21).

## Debate / thesis
- **Bull (Bernstein, Rasgon):** PT raised **$300 → $500, Outperform** (2026-06-17) on a **server CPU TAM raise to $223B**; Arm targeting **$22B revenue by 2030**, FY31E EPS lifted $9.83 → $11.79. The init thesis (David Dai, 2026-05-18, $300): agentic AI = ~120M CPU cores/GW, ~4x a traditional data center; Arm holds ~50% CPU share among top hyperscalers (Graviton/Axion/Cobalt/Vera all Arm-architected — Moorhead, 2026-05-07). CPU:GPU ratio moving from ~8:1 (training) to ~1:1 (agentic/inference). Axion is actively displacing x86 host CPUs in Google TPU 8t/8i — "50% less power, 80% improvement over x86" (Arm CEO at GCP Next, 2026-05-11). PC optionality: NVDA RTX Spark / N1X Arm PC with Microsoft (briefings, 2026-06-01; ARM +12% pre-mkt).
- **AGI CPU silicon optionality (BofA, Arya, 2026-02-23):** with a full CPU **chiplet**, Arm's per-server economics expand **~30x** — from royalty of ~$50-100/chip @ ~98% GM to full silicon of ~$1.5k-2.0k/chip @ 50-60% GM. At a modest **~3% server CPU share by CY28E** (~$1.2B incremental sales) Arm captures ~$0.30/~10% EPS accretion; ~5% share by CY30E (~$3B) = ~$0.70/15-20% accretion — not yet in models. Caveat: the ~$200M/qtr (~$800M/yr) SoftBank licensing/outsourced-R&D line **may go away** once the chiplet matures (one-time, embedded in CPU ASP) — Arm needs ≥3% share just to offset it. 'Arm Everywhere' event held SF, Mar 24 2026 (expected merchant-CPU unveil).
- **Bear:** royalty came in *light* vs Street in Q4 FY26 even as license beat — the highest-multiple part of the story (per-unit royalty compounding) is lumpy. The AGI CPU pivot trades Arm's pristine IP margins for ~30% hardware GM and puts Arm into **direct competition with its own licensees** (explicit new risk factor, FY26 20-F). Customer concentration is acute: top-5 = ~57% of revenue, Arm China alone ~16%; **PRC ~18% of revenue** with US/UK–China trade & national-security overhang, and Arm does **not control Arm China** (FY26 20-F risk factors). Mobile is ~43% of royalty into a soft smartphone unit backdrop (memory-driven; Q3 FY26 flagged 1–2% total royalty risk). Competition from x86 and free **RISC-V** (some customers are RISC-V backers). UBS's Arcuri is pointedly skeptical on the bull-case royalty math: investors model **50c-$1 per core**, but Arcuri argues the big CPU winners pay far less — **NVIDIA pays "substantially below 50 cents per core, way below,"** as do the large hyperscaler Arm-CPU customers — so the back-of-envelope core-count × royalty math is "too high"; he also discounts Arm's own AGI-CPU demand because the bulk of customers (he believes Meta + OpenAI) "don't do what they say they're going to do," warranting a bigger discount factor (UBS "Arcuri call," 2026-06-15).
- **Where the sell-side stands:** Bernstein OP $500 (Rasgon, 2026-06-17). UBS **Buy, PT $195** (Arcuri, 2025-12-22; spot ~$121, bear-case $114) — thesis: data center the most fertile end-market as cloud pushes for power-optimized CPU architectures, plus custom-ASIC attach; UBS above Street with FY26E rev $4,859M / non-GAAP EPS $1.72 and FY27E $6,056M / $2.42 (CY27 $6,991M / $3.01), running ~+2-3% on revenue and ~+5-12% on EPS vs consensus. BofA **Neutral, PT $245** (Arya, "AI 2030", 2026-05-13, raised from $140 on 2026-02-23; 69x CY28E non-GAAP EPS, mid of the 35x-92x historical range) — likes the data-center content + silicon/chiplet (AGI CPU) optionality, offset by high SoftBank dependence and opex ramp; still Neutral on valuation. _(Prior $140 PO retained in Changelog.)_ **Redburn Neutral, PT $130** (2026-06-17) — the bear-leaning house: it nudged ARM revenue up only on a healthier-than-feared smartphone market, but bakes in just **$1bn AGI CPU revenue over the coming 18 months** and pointedly **does NOT include the guided $15bn 2030 AGI CPU revenue** absent confirmed purchase contracts; it sits **9-19% below consensus on FY29-31 revenue**, trims near-term contribution margin (Meta shares the NRE burden, pressuring ASPs / margin-dilutive CPU mix), and notes ARM trades at ~48x two-year-forward EV/sales, a steep premium to premium-rated peers (Redburn, 2026-06-17). SoftBank read-through bundled: Bernstein lifted SoftBank to OP ¥11,200 (from ¥8,200) on the same ARM CPU-TAM revision (2026-06-17); SoftBank "is not interested in selling one share" of Arm (Haas, Q3 FY26 call) and pegs Arm's standalone valuation ~$500B starting point (Jefferies Techknowledge, 2025-12-17). Arm is on the Jefferies Chicago Semis Conf roster (Aug 24) and ran an IR fireside 2026-06-15.

## Catalysts / what to watch
- **Q1 FY27 print** (~late July 2026): first read on royalty re-acceleration vs the light Q4 royalty; AGI CPU order-book updates.
- **Arm AGI CPU production** — expected by end of CY2026 (FY26 20-F); first revenue ~$90–100M in Q4 FY27; watch GM trajectory and whether the $2B FY27+28 demand converts.
- **Server/data-center share milestones** — Graviton5 / Axion / Cobalt 200 / Vera ramps; whether Arm crosses ~50% hyperscaler CPU share (Q3/Q4 FY26 framing; SoftBank "~50% by year-end" target, Jefferies 2025-12-17). BofA sees ~20-25%+ *value* share by CY30E.
- **CSS royalty mix** crossing into the "teens" then toward ~50% of royalties; watch v9/CSS stacking (v9 ≈ 2x v8, CSS ≈ 2x v9) and the MediaTek CSS-billing dispute.
- **China / Arm China** commercial-relationship and export-control headlines; **SoftBank** capital actions (read-through both ways).
- Cross-theme: agentic-AI CPU:GPU ratio and custom-silicon mix — see [custom-asic-tpu](themes/custom-asic-tpu.md) (Vera, Axion, Graviton all carry embedded Arm cores).

## Risks
- **Own-silicon pivot (AGI CPU):** new competitive/brand/operational/financial risk; channel conflict with licensees; ~30% GM dilutive to IP model (FY26 20-F). Note the SoftBank licensing line (~$800M/yr) may not survive the chiplet transition (BofA, 2026-02-23).
- **Customer concentration:** top-5 ~57%, Arm China ~16–21%, mobile app processors ~43% of royalty (FY26 20-F).
- **China:** PRC ~18% of revenue; no control over Arm China; US/UK–PRC trade & national-security exposure (FY26 20-F).
- **Architecture license substitution:** customers can take an architecture license and build their own cores, or shift to **RISC-V** / x86 (FY26 20-F). x86 still ~70-80% of server CPU value today; RISC-V winning low-end industrial (UBS, 2025-12-22).
- **Cyclicality / smartphone units:** royalty tied to end-market chip shipments; memory-driven handset unit softness (Q3 FY26 call); mobile ~50% of revenue exposed to tariff-related demand destruction (UBS, 2025-12-22).
- **Governance:** SoftBank-controlled company + FPI exemptions limit minority influence (FY26 20-F).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## Changelog
- 2026-06-25 — BofA (Vivek Arya) PO raised **$140 → $245** (Neutral maintained) in the "AI 2030" note dated 2026-05-13 — basis moved to 69x CY28E non-GAAP EPS on data-center content + AGI-CPU/chiplet optionality. Prior BofA PO of $135→$140 (2026-02-23) superseded.

## In the inbox (Outlook — recent sell-side flow)
- **BofA — 'The CPU Debate with Vivek Arya'** _(2026-06-11)_: evolving CPU market / AI infra — ARM-architected server CPUs (Graviton/Axion/Cobalt) the TAM driver; agentic AI pushing CPU:GPU toward 1:1.
- **Bernstein** (per Morning Briefing): server-CPU TAM raised to **$223B**, ARM Outperform **PT $500**.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q4 FY26 print + intra-quarter · May 06 → Jun 23, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q4 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Data center / server CPU** | DC royalty >2x YoY; hyperscaler share ~50%; CPU TAM >$100B in 2030 | Bernstein: TAM $223B, ARM $22B rev in 2030 · UBS: share 16%→42% by 2030 · Citi: ~99% ARM in GB-class racks | **✓ confirms** (bulls raise TAM) |
| **Own silicon (AGI CPU)** | AGI CPU launched w/ Meta; ~$2B demand FY27+28 | Arcuri: customers "don't do what they say"; Redburn models only $1B over 18m and excludes the $15B of 2030 absent a contract | **⚠ nuance** (AGI demand discounted) |
| **Royalty / monetization** | Royalty $671M, +11% (light vs Street $691M) | Arcuri: NVDA pays "well below 50c/core", core×royalty math "too high" | **✗ contests** (royalty/core is the hole) |
| **Competition (x86)** | Strong demand across the 3 AI segments | CEO @ GCP: Axion displaces x86 "50% less power"; Citi: Google ~60% ARM, Graviton ~60% of AWS | **✓ confirms** (x86 displacement) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-07 | Expert call · SiTime/ARM | guidance | bull | Post-Q4, ARM guides royalty and licensing both +20% YoY in fiscal Q1 (Jun) and across FY27; cloud/AI royalty ~2x YoY; cloud (data-center) share reached ~50% on ARM's metric (from ~zero in late-2020), with NVDA's Grace/Vera the big driver. AGI backlog "basically doubled in six weeks" but is memory-constrained; hyperscaler roadmap for a 700-core chip; server-CPU TAM internally pegged at $200-300bn by 2030. |
| 05-07 | Patrick Moorhead | demand | bull | ARM holds ~50% CPU share among top hyperscalers (Graviton/Axion/Cobalt/Vera all ARM); Meta as AGI lead (briefing). |
| 05-11 | Arm CEO @ GCP Next | competition | bull | Axion actively displacing x86 host CPUs on Google TPU 8t/8i — "50% less power, 80% improvement over x86" (briefing). |
| 05-18 | Bernstein · David Dai | demand | bull | Bernstein initiates at Outperform PT $300: agentic AI = ~120M CPU cores/GW (~4x a traditional data center); ARM at ~50% CPU share among top hyperscalers; CPU:GPU ratio from ~8:1 (training) to ~1:1 (agentic/inference). |
| 05-21 | UBS · Sunny Lin | demand | bull | UBS "Quantifying the server CPU opportunity": ARM's server-CPU unit share rises from 16% (2025) to 42% (2030) as agentic AI lifts CPU-bound orchestration work; total server-CPU market reaches ~$170bn by 2030 (units 23m→63m, 30% CAGR); AMD 24%→29%, Intel 60%→29%. |
| 05-22 | Citi · Blayne Curtis | competition | bull | Asia checks: ARM's storyline is more levered to companion CPUs (fixed CPU:GPU ratio in AI servers, ~99% ARM in GB-class racks). CPU mix at Google up to ~60% ARM (Axion, above expected) and Graviton ~60% of AWS's general-purpose mix; NVDA's ~$20bn standalone Arm-CPU figure (Vera) is "chips, not memory" ("Asia recap"). |
| 06-01 | Capstone briefing | product | bull | PC optionality: NVDA RTX Spark / N1X Arm PC with Microsoft; ARM +12% pre-market (briefing). |
| 06-15 | UBS · Arcuri | valuation | bear | Arcuri skeptical on the bull case's royalty math: investors model 50c-$1 per core, but the big winners pay far less — NVIDIA pays "substantially below 50 cents per core, well below," as do the large hyperscalers; the core-count × royalty math is "too high." Also discounts AGI-CPU demand because most customers (Meta + OpenAI) "don't do what they say they're going to do" ("Arcuri call"). |
| 06-17 | Bernstein · Rasgon | valuation | bull | PT raised $300→$500, Outperform: server-CPU TAM revised to $223bn; ARM targeting $22bn of revenue by 2030, FY31E EPS raised from $9.83 to $11.79. Bernstein also raised SoftBank to OP ¥11,200 (from ¥8,200) on the same revision (briefing). |
| 06-17 | Redburn | valuation | bear | Redburn Neutral PT $130, the most bearish house: raises revenue only on better-than-feared smartphone, but bakes in just $1bn of AGI CPU over the next 18 months and explicitly does NOT include the guided $15bn of 2030 AGI without confirmed contracts; sits 9-19% below consensus on FY29-31 revenue; ARM trades at ~48x EV/sales two years out, a steep premium vs peers (briefing). |

**Quarter synthesis:** with DC share and x86 displacement broadly confirmed by the bulls (Bernstein PT $300→$500, UBS), the debate shifted to *how much ARM monetizes per core* — Arcuri and Redburn attack the royalty×core-count arithmetic and discount the $15B of 2030 AGI-CPU absent a contract, opening the widest PT spread in the sector ($130 vs $500).

## Management commentary — evolution (last 4 quarters)

| Theme | Q1 FY26 (2025-07-30) | Q2 FY26 (2025-11-05) | Q3 FY26 (2026-02-04) | Q4 FY26 (2026-05-06) |
|---|---|---|---|---|
| Total revenue | $1.05B, best Q1 ever (2nd $1B+ qtr) | $1.14B, +34% (3rd $1B+ qtr) | $1.24B, +26% (4th $1B+ qtr) | $1.49B, +20%; FY26 $4.92B, +23% |
| Royalty (v9 mix) | $585M record, +25% on v9/CSS/DC | $620M record, +21% | $737M, +27% (incl. DC strength) | $671M, +11% (light vs Street $691M) |
| CSS licensing/adoption | 16 licenses/10 cos; CSS >10% of ASP | 19 licenses/11 cos; top-4 Android ship CSS | 21 licenses/12 cos; could be ~50% of royalties | Demand strong across all 3 AI segments |
| Data center / server CPU | 70k enterprises on Neoverse, 14x since 2021 | DC royalty doubled YoY; 1B+ Neoverse CPUs | Hyperscaler share to reach ~50% | DC royalty >2x YoY; >$100B CPU TAM by 2030 |
| Own silicon (AGI CPU) | Not launched; Neoverse/CSS direction only | Dream Big Semi M&A; integration signal | Segment reorg (Edge/Physical/Cloud AI) | AGI CPU launched w/ Meta; ~$2B FY27+28 demand |
| Margin / EPS | — | Non-GAAP EPS $0.39, beat by $0.06 | 41% op margin; EPS $0.43, high-end | ~49% op margin; EPS $0.60 record |

_Source: ARM earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings (20-F, UK FPI):** [FY26 20-F (FY ended 2026-03-31)](../ARM/ARM_20-F_2026-05-26_0001973239-26-000097.html) · [FY25 20-F](../ARM/ARM_20-F_2025-05-28_0001973239-25-000016.html) · [FY24 20-F](../ARM/ARM_20-F_2024-05-29_0001973239-24-000012.html).
- **Transcripts:** [Q4 FY26 (2026-05-06)](../ARM/transcripts/ARM_Q4-FY26-earnings_2026-05-06.md) · [Q3 FY26 (2026-02-04)](../ARM/transcripts/ARM_Q3-FY26-earnings_2026-02-04.md) · [Q2 FY26 (2025-11-05)](../ARM/transcripts/ARM_Q2-FY26-earnings_2025-11-05.md) · [Q1 FY26 (2025-07-30)](../ARM/transcripts/ARM_Q1-FY26-earnings_2025-07-30.md).
- **Research reports (relatórios bons):**
  - [BofA — CPU in AI: key inference beneficiary, TAM could >2x by CY30 (Arya, 2026-02-23)](../relat%C3%B3rios%20bons/CPU.html)
  - [UBS — 2026 Semiconductors Overview (ARM Buy, Arcuri, PT $195, 2025-12-22)](../relat%C3%B3rios%20bons/UBS_2026_overview.html)
  - [Jefferies — Q4'25 Techknowledge tech takeaways (SoftBank: CSS/MediaTek royalties, 50% server share, 2025-12-17)](../relat%C3%B3rios%20bons/Q425_Techknowledge_tech_takeaways.html)
  - [JPM — ASIC Design Services Teach-in (Meta Arm server CPU w/ Socionext)](../relat%C3%B3rios%20bons/JPM_ASIC_Design_Services_Teach-in.html)
  - [UBS — Quantifying the server CPU opportunity (Sunny Lin, 2026-05-21) — ARM server-CPU unit share 16%→42% by 2030, $170bn TAM](../relat%C3%B3rios%20bons/CPU_TAM_-_UBS.html)
  - [Expert "SiTime/ARM call" (2026-05-07) — royalty/licensing +20% Q1 & FY27; cloud share ~50%; ACV +22%; AGI backlog 2x in 6 weeks (memory-constrained); 700-core roadmap; $200-300B server-CPU TAM](../relat%C3%B3rios%20bons/2026_05_07_sitm_arm_7_apr_2026.html)
  - [UBS "Arcuri call" (2026-06-15) — royalty-rate skepticism (NVDA pays <<50c/core); discounts Meta/OpenAI AGI demand](../relat%C3%B3rios%20bons/2026_06_15_ubs_arcuri_15_jun_26.html)
  - [Citi "Asia recap" (Blayne Curtis, 2026-05-22) — companion CPUs; Google ~60% Arm (Axion), Graviton ~60% of mix; NVDA $20B standalone-Arm figure](../relat%C3%B3rios%20bons/2026_05_22_jef_asia_recal_call_22_may_2026.html)
  - [BofA (Vivek Arya) — "AI 2030: Stronger for Longer / State of the Union" (2026-05-13)](../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html) — ARM Neutral, **PO $140→$245** (69x CY28E EPS) on data-center content + AGI-CPU/chiplet optionality.
- **Briefings:** `E:\briefings\2026` — 2026-06-17 (Bernstein ARM PT $300→$500, server-CPU TAM $223B; SoftBank ¥11,200) · 2026-05-18 (Bernstein init OP $300) · 2026-05-06 (Q4 FY26 print recap) · 2026-05-07 (Moorhead — ~50% hyperscaler CPU share; Meta AGI lead) · 2026-05-11 (Axion x86 displacement, GCP Next) · 2026-06-01 (NVDA RTX Spark / Arm PC).
- **Theme:** [custom-asic-tpu](themes/custom-asic-tpu.md).
- **Outlook:** attempted (`outlook.py --no-body --days 7`) — **unavailable in this environment** (no MAPI/Outlook session; empty return). No inbox notes incorporated.
