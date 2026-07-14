# FLEX — Flex Ltd.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\FLEX` (filings + transcripts) · `_briefings`. Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $30.8bn | $40.4bn |
| Gross profit | $3.0bn | $4.2bn |
| Gross margin | 9.8% | 10.3% |
| EBITDA | $2.6bn | $3.7bn |
| EPS | $3.97 | $6.17 |
| Capex | $1.2bn | $1.1bn |
| OCF (≈EBITDA) | $2.6bn | $3.7bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Flex is the world's #2 contract electronics manufacturer / EMS-ODM (~$27.9B FY26 revenue, FYE Mar-31), pivoting from low-margin assembly toward an "end-to-end manufacturing partner" with proprietary **datacenter power and cooling** content. As of FY26 it reorganized into three reportable segments (10-K, 2026-05-20): **ITS** — Integrated Technology Solutions (Communications, Lifestyle; $11.1B, 40% of sales, -2% y/y); **RMS** — Regulated Manufacturing Solutions (Industrial, Automotive, Healthcare; $10.2B, 36%, +5%); and **CPI** — Cloud and Power Infrastructure (Cloud & Cooling, Power; $6.6B, 24%, +38% y/y). The CPI segment is the AI-datacenter story: **Anord Mardix** critical power (switchgear, busway, modular power pods, turnkey datacenter electrical), **Crown** medium-voltage switchgear/grid, **JetCool** direct-to-chip liquid cooling, plus embedded power (power shelves, BBUs, DC/DC) riding the **800V DC** and 1MW+ rack transition (10-K FY25, 2025-05-21; Q3 FY26, 2026-02-04). On May 5, 2026 Flex announced it will **spin off CPI into a separate public company** (target Q1 CY2027), splitting the AI-power pure-play from the legacy EMS base. No customer >10% of sales; top-10 = 45% (10-K FY26).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) ITS — Integrated Technology Solutions / EMS (comms, lifestyle), $11.1B · 2) RMS — Regulated Manufacturing (industrial, auto, healthcare), $10.2B · 3) CPI — Cloud & Power Infrastructure (Anord Mardix critical power, JetCool liquid cooling), $6.6B +38% |
| **Main buyer(s)** | Hyperscalers / neoclouds / utilities for CPI (Google contract, new AWS) + auto/health/industrial OEMs; no customer >10%, top-10 = 45% |
| **Key suppliers** | Upstream electronic components — semis, passives, connectors, enclosures, switchgear/power components and raw materials sourced for build-and-integrate |

## Position in the value chain
Flex sits in the middle of the AI-datacenter and broader-electronics chain: it buys components from suppliers, then designs/builds/integrates at scale — and increasingly sells its **own** power and cooling IP (Anord Mardix critical power, JetCool liquid cooling) into hyperscaler/neocloud/utility buildouts. The differentiated content is **800V DC power delivery + direct-to-chip liquid cooling** for high-density AI racks, where Flex claims a "very small group of competitors" (Q3 FY26, 2026-02-04). BofA's datacenter primer corroborates the dual content: **Flex Power** is listed by NVIDIA as a **power-system-component partner** for the 800V DC architecture, and **Flex/JetCool** is one of the **ten CDU manufacturers named NVIDIA partners at Computex 2025** (BofA, 2025-09-15). On cooling, BofA places Flex/JetCool *outside* its Tier-1 CDU vendor set (Delta, nVent, Schneider/Motivair, Vertiv, DCX) in a nascent ~$1.2B-2024 CDU market — i.e., a credible NVIDIA-partner entrant but not yet a scale leader in coolant distribution units. See [800v-dc-power](themes/800v-dc-power.md) and [ai-datacenter-power](themes/ai-datacenter-power.md).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <defs>
    <marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L7,3 L0,6 Z" fill="#444"/>
    </marker>
  </defs>
  <!-- Suppliers -->
  <rect x="10" y="70" width="150" height="80" rx="8" fill="#eef2f7" stroke="#5b6b7f"/>
  <text x="85" y="95" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="114" text-anchor="middle">components,</text>
  <text x="85" y="130" text-anchor="middle">semis, passives,</text>
  <text x="85" y="146" text-anchor="middle">enclosures</text>
  <!-- Flex -->
  <rect x="230" y="35" width="250" height="150" rx="8" fill="#e3eefc" stroke="#1f5fa6" stroke-width="2"/>
  <text x="355" y="58" text-anchor="middle" font-weight="bold" fill="#1f5fa6">Flex (FLEX)</text>
  <text x="355" y="78" text-anchor="middle">EMS / ODM manufacturing</text>
  <text x="355" y="96" text-anchor="middle">+ design &amp; supply chain</text>
  <text x="355" y="118" text-anchor="middle" font-weight="bold">Datacenter power (Anord Mardix):</text>
  <text x="355" y="134" text-anchor="middle">switchgear · busway · power pods · 800V</text>
  <text x="355" y="156" text-anchor="middle" font-weight="bold">JetCool liquid cooling:</text>
  <text x="355" y="172" text-anchor="middle">direct-to-chip / CDU</text>
  <!-- Customers -->
  <rect x="550" y="55" width="160" height="110" rx="8" fill="#eef7ee" stroke="#3a7d3a"/>
  <text x="630" y="78" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="630" y="98" text-anchor="middle">cloud / AI datacenter</text>
  <text x="630" y="116" text-anchor="middle">(hyperscaler, neocloud,</text>
  <text x="630" y="132" text-anchor="middle">utility)</text>
  <text x="630" y="152" text-anchor="middle">auto · health · industrial</text>
  <!-- arrows -->
  <line x1="160" y1="110" x2="228" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="480" y1="110" x2="548" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
  <text x="355" y="206" text-anchor="middle" fill="#1f5fa6" font-style="italic">800V power stack + liquid cooling = AI-datacenter content; CPI to be spun off Q1 CY2027</text>
</svg>

## Current state (latest quarter)
**Q4 / FY26 (reported 2026-05-06)** — beat-and-raise, with the CPI spin-off as the headline.
- **Q4 revenue $7.5B, +17% y/y**; adj. gross margin 9.9% (record, +50 bps); adj. operating margin 6.7% (+50 bps); adj. EPS $0.93, +27% (Q4 FY26 call, 2026-05-06).
- **FY26: revenue $27.9B, +8%**; adj. EPS $3.30, +25%; adj. operating margin 6.3% (+70 bps); FCF ~$1.1B; CapEx $625M (2.2% of sales) (10-K 2026-05-20; Q4 call).
- **Segment FY26 (10-K MD&A):** ITS $11.1B (-2%, 5.4% income margin); RMS $10.2B (+5%, 6.0%); **CPI $6.6B (+38%, 9.2% margin, -100 bps on cloud-ramp investment)**. CPI sub-mix: **Cloud & Cooling +29%, Power +61%** y/y. CPI was $3.2B in FY24 → $4.8B FY25 → $6.6B FY26.
- **Spin-off:** CPI to become a standalone public co (power + thermal + compute integration for AI datacenters / utilities), target **Q1 CY2027**, intended tax-free. CEO **Revathi Advaithi → CPI CEO**; **Michael Hartung → Flex (RemainCo) CEO** (Q4 FY26 call).
- **FY27 guide (combined, pre-spin):** revenue $32.3–33.8B (+18% midpoint); adj. op margin 7.0–7.1%; adj. EPS $4.21–4.51 (+32% midpoint); CapEx $1.4–1.6B (steps up for compute/power capacity); **CPI +65–75%** growth (multi-year contracts incl. Google), ramping 80%+ in FY28.
- Closed **EP2 (Electrical Power Products)** acquisition the week of the print — utility-grade power / grid modernization.

## Debate / thesis
- **Bull:** CPI is a scarce, vertically-integrated AI-power play — Flex claims it is the only provider doing end-to-end cloud IT integration *plus* a full power/cooling portfolio (rack-to-utility), with "very small group of competitors" in 800V DC / 1MW+ racks (Q3 FY26, 2026-02-04). JPM (Samik Chatterjee) "Watts Up! 800V AI DC power stack" names **APH, FLEX, TEL, WOLF** as best positioned for the 800V rewiring of the AI rack — new connectors/cabling/power distribution = multi-billion TAM (briefing 2026-06-09). JPM's H&N year-ahead lays out the FLEX bull tenets: datacenter ~$5B in FY25 (~20% of total) growing **well above the +35% y/y guide** toward ~25% of the business, led by both Compute/Cloud and Power; **OP margins to ~7% by end-FY28** as high-margin Power (mid-teens; ~6% of FY24 rev) and Services mix up against the 4–5% base EMS; and **underappreciated upside to Google TPU-server volumes** plus a **new AWS customer relationship** (incremental Cloud-capex leverage) (JPM, 2025-12-15). The spin (target Q1 CY2027) crystallizes a pure-play AI-power SpinCo at a higher multiple vs. the EMS base. FY27 guide of +18% revenue / +32% EPS is well above legacy EMS growth, with CPI +65–75% the engine. NVIDIA (modular DC systems), LG (gigawatt-scale thermal) and Equinix (liquid-cooling) partnerships + a Google multi-year contract underpin backlog. FLEX joins the **S&P 500 on June 22, 2026** alongside MRVL — passive-flow tailwind (briefings 2026-06-09).
- **Bear:** CPI margins compressed -100 bps in FY26 (9.2%) on cloud-ramp investment, and cloud margins sit *below* power margins inside CPI (Stifel Q&A, Q4 FY26) — growth is dilutive near-term and CapEx steps to $1.4–1.6B in FY27. EMS is structurally low-margin (consolidated FY26 op margin only 6.3%) and ITS revenue is *shrinking* (-2%, Lifestyle -9%). JPM flags two distinct bear tenets: **execution track record more limited than peers** — FLEX's record on sustainable top-line/margin delivery is shorter than Jabil's, even if recent management execution has matched/beaten peers; and **multiple has ~doubled vs. pre-AI** — FLEX at **~20x earnings vs. a ~8x LT historical average**, among the richest premiums in the coverage group (JPM, 2025-12-15). Hyperscaler in-housing risk (Amazon developing its own cooling; "warrant deal" immaterial to FY26) and customer concentration (top-10 = 45%). Spin execution / cost and dis-synergies between CPI and the manufacturing base; "no assurance" the spin completes on terms or timeline (10-K risk factors). Tariff exposure is "low-calorie revenue" — pass-through dilutes margin (JPM Q&A, Q1 FY26).
- **Where the sell-side stands:** **JPM (Chatterjee) OW, FLEX at $68.80 (JPM, 2025-12-15)** — but ranks the EMS group **CLS > JBL > FLEX**, with FLEX last primarily on upgrade potential: Celestica ranks highest, then Jabil (better positioned to beat its conservative Amazon outlook), then Flex, whose "datacenter revenue growth will continue to be driven by power while compute remains robust." JPM's one-line OW rationale: "Well positioned for secular growth in Industrial, Auto, Health and CEC; Power business to be the growth driver in Cloud." The new **AWS relationship is double-edged** — Cloud-capex leverage for FLEX, but JPM flags it as a *share-loss risk to Jabil* (AWS is Jabil's primary Cloud customer). The EMS group ranks *lower* for 2026 than the prior year on higher reliance on Compute over Networking. UBS bucketed FLEX in its earnings-callback / 800V-power complex (briefing 2026-05-08). FLEX repeatedly on 52-week-high lists through the AI-hardware run (briefings 2026-05-12/14). **Baird (Luke Junk) Outperform, PT $165** — ~17x EV/C2027E EBITDA (21x SpinCo EBITDA at ~60% earnings mix + 11x RemainCo at ~40%); calls the CPI/SpinCo a "pureplay power franchise" spanning embedded (on-rack) and critical (infrastructure) power at mid-teens product-level operating margins, with power **~33% of SpinCo revenue and ~50% of earnings** and embedded power the most compelling leg (NVDA 800V platform partnership); Baird models SpinCo power at ~$1B F2024 → $2.1B F2026 → **~$7B F2028E (~7x growth)**, embedded-power content growth exceeding the 2-4x white-space content lift it ascribes to peers like Littelfuse (Baird "Transition to 800V in Datacenters", 2026-05-15).

### Bogey table — JPM growth/margin profile, pre-AI vs AI-era (JPM, 2025-12-15)
| Metric | Pre-AI guide | AI-era guide | Delta |
|---|---|---|---|
| Revenue growth | LSD–MSD | HSD (>5%) | +5 ppts |
| Operating margin | 5.8–6.0%+ | Mid-teens (Power) blending to ~7% co. by FY28 | — |
| EPS growth | Low-teens | — | +3 ppts EPS |
| AI mix of revenue | 19% (2024) → 24% (2025) | 31% (2026E) → 37% (2027E) | rising |
| P/E (early-2024 → current) | 8.1x | 20.8x | **+158%** re-rate |

_JPM's AI-mix walk shows FLEX as one of the larger P/E re-rates in the group (+158%), consistent with its "richest premium" bear point; FY27 AI mix of 37% sits mid-pack vs. CLS 74% / JBL 41% (JPM, 2025-12-15)._

## Catalysts / what to watch
- **CPI spin-off (target Q1 CY2027)** — Form 10 / structure, RemainCo vs SpinCo financials, multiple re-rate; key swing factor.
- **Q1 FY27 print (~late July 2026):** guide $7.35–7.65B revenue / $0.86–0.92 EPS; **CPI +20–30%** (ramps 2H FY27) — watch the CPI growth cadence and cloud-ramp margin drag.
- **June 22, 2026:** S&P 500 inclusion effective (passive buy flow).
- **CapEx step-up to $1.4–1.6B in FY27** — compute capacity additions; FCF conversion guided ~60% (ex-spin costs) vs 80%+ historically.
- **AWS ramp** — JPM's bull leg on incremental Cloud-capex leverage; conversion is the proof point (and the Jabil share-loss watch) (JPM, 2025-12-15).
- Hyperscaler/neocloud contract conversions (Google named); NVIDIA / LG / Equinix program ramps; EP2 integration.

## Risks
- **Spin-off execution** — may not complete on terms/timeline; cost and dis-synergy risk (10-K FY26 risk factors).
- **CPI margin dilution** — investments in cloud/power capacity pressure CPI margins; demand outside Flex's control (10-K).
- **Customer concentration** — top-10 = 45% of sales; hyperscaler in-sourcing of cooling/power (Q1/Q3 FY26 calls).
- **Cyclicality / demand variability** — order cancellations, short product lifecycles; ITS/Lifestyle consumer weakness (10-K; Q3 FY26).
- **Tariffs / trade policy** — pass-through "low-calorie revenue," margin headwind; geopolitical exposure (10-K; Q1 FY26 call).
- **Capital intensity** — customer-specific equipment impairment/obsolescence; rising CapEx into FY27 (10-K).
- **Execution vs. peers** — JPM bear point: shorter sustainable growth/margin track record than Jabil (JPM, 2025-12-15).
- **Valuation** — ~20x vs. ~8x LT average; ~+158% P/E re-rate leaves little room for AI-narrative disappointment (JPM, 2025-12-15).
- Structurally low EMS margins (~6% consolidated) limit RemainCo re-rating.

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->
_Note: FLEX not yet present in `_data/estimates.json` (asof 2026-06-19) — consensus block will populate once estimates are fetched for the ticker._

## In the inbox (Outlook — recent sell-side flow)
- **JPM (Samik) — H&N Year-Ahead / EMS ranking** _(2025-12-15)_: **OW, FLEX $68.80**; ranks EMS **CLS > JBL > FLEX**; bull = Google/TPU + new AWS + Power growth, ~7% OP margin by FY28; bear = limited execution track record vs. peers + ~20x vs. ~8x historical (richest premium).
- **JPM (Samik) — 'Watts Up! Shift to 800V'** _(2026-06-09)_: **FLEX among best-positioned** (Anord Mardix critical power + 800V/1MW rack); JPM notes 'long crowding in Flex has picked up substantially.' New specifics: FLEX is most relevant to the **power distribution solutions TAM, which JPM/Omdia sizes growing 20%+ CAGR from ~$50bn (2025) to ~$90bn (2028)**; the power-management subset (~$1mn/MW content) grows ~30% CAGR to **$45bn by 2028** (from $20bn). JPM estimates **Flex's power business is ~32% of CPI/SpinCo revenue today, on track to exceed 40% by 2027**, with the 800V portfolio spanning power shelves, PSUs, capacitor bank units (CBU), BBUs, liquid-cooled busbars, switchgear, packaged substations and fully-integrated power racks; named a key NVIDIA power partner (JPM "800V", 2026-06-09).
- **BofA — Datacenter primer** _(2025-09-15)_: Flex Power = NVIDIA 800V power-system-component partner; Flex/JetCool = NVIDIA Computex-2025 CDU partner, but outside BofA's Tier-1 CDU vendor set.
- **JPM networking conf recap (JPM "Networking recap", 2026-05-26):** at JPM's conference Flex sounded **confident about power-segment margins rising with scale**, and explicitly framed the **~15% power margin as NOT the long-term target — room to go higher as scale improves** (incremental to the bull's CPI-margin debate; pre-CPI-spin commentary). The same recap's cloud-capex model is the demand backdrop: JPM raised its data-center capex outlook to **~+80% y/y in 2026** (>$250B step-up) and **~+50% in 2027** (>$285B step-up, ~$860B aggregate top-4 hyperscaler spend), after North American installed DC power capacity jumped **8 GW in 1Q26 (highest-ever quarterly add)** and the planned pipeline grew to **>175 GW** — and DC capex now consumes **>90% of hyperscaler operating cash flow** by JPM's 2027 forecast (JPM "Networking recap", 2026-05-26).
- **Baird (Luke Junk) — "Transition to 800V in Datacenters"** _(2026-05-15)_: Outperform, PT $165; FLEX a "pureplay power franchise," SpinCo power ~33% of rev / ~50% of earnings, ~$7B power by F2028E (~7x F2024); embedded power (NVDA 800V partner) the most compelling leg. CEO Revathi Advaithi flagged as highly credible (ex-Eaton).
- **SemiAnalysis — "Inside the 800VDC Revolution, Part 1"** _(2026-05-26)_: names Flex (a major NVIDIA manufacturing partner) as having **publicly advocated for in-depth hazard identification and 800VDC safety training** at DC facilities — a positioning signal on FLEX's deep involvement in the 800V power-delivery build. Sizes the sidecar/power-rack TAM peaking ~$11B (2028) and SST TAM ~$13B by 2030, with power-rack ASP ~$400-500k (~10x a standard AC power rack) — the content-uplift backdrop for FLEX's CPI power franchise (SemiAnalysis, 2026-05-26).
- **S&P 500 inclusion** _(June 22, alongside MRVL)_ — passive demand tailwind.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q4 FY26 · May 6 → Jun 22, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q4 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **DC / CPI demand** | CPI FY26 $6.6B (+38%); FY27 guide CPI +65-75% | JPM: DC capex ~+80% y/y in 2026 (>$250B step-up), +50% in 2027; +8 GW of power in NA in 1Q (largest quarterly add) | **✓ confirms** (DC macro supports it) |
| **Power margin** | Power margins > cloud; toward "full architecture" | JPM: ~15% power margin is NOT the LT target, "room to go higher as scale improves" | **✓ confirms** (with upside) |
| **Product / 800V** | 800V DC suite, 1MW+ racks; NVIDIA partner | JPM: FLEX among the best-positioned (Anord Mardix + 800V/1MW); power ~32% of CPI today → >40% in 2027; "long crowding picked up a lot" | **✓ confirms** (leading positioning) |
| **Structure / spin** | CPI spin-off announced, target Q1 CY2027 | S&P: S&P 500 inclusion on Jun 22, 2026 — passive-flow tailwind | **✓ confirms** (re-rating underway) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-26 | JPM · Samik (Networking conf recap) | margin | bull | At JPM's conference, Flex sounded confident about power margins rising with scale and framed ~15% power margin as NOT the LT target — "room to go higher as scale improves". Demand backdrop: JPM raised its DC capex outlook to ~+80% y/y in 2026 (>US$250B step-up) and ~+50% in 2027; North American DC power capacity +8 GW in 1Q26 (largest quarterly add ever); pipeline >175 GW. |
| 06-09 | JPM · Samik (Watts Up! Shift to 800V) | product | bull | FLEX among the best-positioned (Anord Mardix critical power + 800V/1MW rack); JPM notes that "long crowding in Flex has picked up substantially". Power-distribution TAM (Omdia) +20% CAGR from ~US$50bn (2025) to ~US$90bn (2028); power-management subset (~US$1mn/MW) +30% CAGR to US$45bn in 2028. JPM estimates Flex's power business is ~32% of CPI/SpinCo revenue today, on track to >40% in 2027; the 800V portfolio spans power shelves, PSUs, CBU, BBUs, liquid-cooled busbars, switchgear, substations and integrated power racks. NVIDIA power partner. |
| 06-22 | S&P / briefings (2026-06-09) | valuation | bull | FLEX inclusion in the S&P 500 effective Jun 22, 2026 (alongside MRVL) — passive-flow tailwind. |

**Quarter synthesis:** the intra-quarter flow was almost one-sidedly confirmatory — JPM amplified everything management said (DC capex +80%, power margins with upside, FLEX best-positioned in 800V) and "long crowding" picked up a lot; the debate shifted from "whether the demand exists" to "what the power SpinCo is worth," with S&P 500 inclusion providing the flow push.

## Management commentary — evolution (last 4 quarters)
| Theme | Q1 FY26 (Jul-24-25) | Q2 FY26 (Oct-29-25) | Q3 FY26 (Feb-04-26) | Q4 FY26 (May-06-26) |
|---|---|---|---|---|
| Revenue / EPS | Rev $6.6B +4%; EPS $0.72 (rec.) | Rev ~$6.8B +4%; EPS $0.79 (rec.) +23% | Rev $7.1B +8%; EPS $0.87 (rec.) +13% | Q4 rev $7.5B +17%; EPS $0.93 +27% |
| Data center / cloud | FY26 DC target $6.5B, ~35% growth, ~25% of co. | Cloud-and-power the driver of the raise | Reaffirmed 35% DC growth; double-digit to continue | CPI FY26 $6.6B +38%; FY27 CPI +65–75% |
| Power vs cooling/compute cycle | Power to outpace cloud; full suite (IT/cool/power) | Cloud + power momentum cited | 800V DC, 1MW+ racks; AI infra platform; NVIDIA/LG | Power margins > cloud; toward "full architecture" |
| Margins | Op margin 6.0% +120 bps; GM 9.1% | Adj. op margin ~6.0% | Op margin 6.5% (record) +40 bps; GM 9.8% | Q4 op margin 6.7% +50 bps; GM 9.9% (rec.) |
| CapEx / capacity | CapEx $131M ~2%; Poland doubles EU power cap. | — | Net CapEx $145M ~2%; power capacity heaviest | FY26 CapEx $625M; FY27 guide $1.4–1.6B |
| Portfolio / structure | Old segments (Reliability/Agility) | — | New segments coming; Investor Day May 13 | CPI spin-off announced, target Q1 CY2027; Google deal |

_Source: FLEX earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY26 (2026-05-20)](../FLEX/FLEX_10-K_2026-05-20_0000866374-26-000012.html) · [10-K FY25 (2025-05-21)](../FLEX/FLEX_10-K_2025-05-21_0000866374-25-000027.html) (Anord Mardix / Crown / JetCool / power-pod detail) · [10-Q Q3 FY26 (2026-02-06)](../FLEX/FLEX_10-Q_2026-02-06_0000866374-26-000005.html).
- **Transcripts:** [Q4 FY26 (2026-05-06)](../FLEX/transcripts/FLEX_Q4-FY26-earnings_2026-05-06.md) · [Q3 FY26 (2026-02-04)](../FLEX/transcripts/FLEX_Q3-FY26-earnings_2026-02-04.md) · [Q2 FY26 (2025-10-29)](../FLEX/transcripts/FLEX_Q2-FY26-earnings_2025-10-29.md) · [Q1 FY26 (2025-07-24)](../FLEX/transcripts/FLEX_Q1-FY26-earnings_2025-07-24.md).
- **Research reports (relatórios bons):**
  - [JPM Hardware & Networking (2025-12-15)](../relat%C3%B3rios%20bons/JPM_Hardware___Networkin_2025-12-15_5155719.html)
  - [JPM "Watts Up! Shift to 800V" (2026-06-09)](../relat%C3%B3rios%20bons/JPM_on_800v.html) — FLEX best-positioned on power distribution; power ~32% of CPI → 40%+ by 2027; power-distribution TAM $50bn→$90bn (2028).
  - [Primer DC overall BofA](../relat%C3%B3rios%20bons/Primer_DC_overall_BofA.html)
  - [JPM — Networking conf recap (2026-05-26)](../relat%C3%B3rios%20bons/2026_05_26_nw_jpm_26_05.html) — Flex power margin: 15% not the LT target, room to rise with scale; cloud-capex +80% (2026) / +50% (2027), 8 GW 1Q26 add.
  - Baird — "Transition to 800V in Datacenters" (Dobre/Kallo/Junk/Gerra, 2026-05-15) — FLEX Outperform PT $165; SpinCo power ~33% rev / ~50% earnings, ~$7B by F2028E; embedded power (NVDA 800V partner) the key leg.
  - SemiAnalysis — "Inside the 800VDC Revolution, Part 1" (2026-05-26) — Flex advocates 800VDC hazard/safety training; sidecar TAM ~$11B (2028), SST TAM ~$13B (2030), power-rack ASP ~$400-500k (~10x AC).
- **Briefings:** JPM "Watts Up! 800V" (2026-06-09); H&N pre-quiet-period catch-up (2026-06-12); UBS callback bucket (2026-05-08); 52-week-high tape-tells (2026-05-12/14); S&P 500 inclusion (2026-06-09).
- **Themes:** [800v-dc-power](themes/800v-dc-power.md) · [ai-datacenter-power](themes/ai-datacenter-power.md).
- **Outlook:** queried (`outlook.py --no-body --days 14`) — no FLEX-specific sell-side emails returned in this environment.
