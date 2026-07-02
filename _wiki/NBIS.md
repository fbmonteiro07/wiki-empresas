<!-- per-company wiki page · synthesized from co-located disk sources only -->

# NBIS — Nebius Group N.V.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\NBIS` (20-F filings + transcripts) · `E:\briefings\2026`. Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $3.3bn | $12.5bn |
| Gross profit | $2.3bn | $8.9bn |
| Gross margin | 69.7% | 71.1% |
| EBITDA | $1.3bn | $6.9bn |
| EPS | $-3.07 | $-3.01 |
| Capex | $24.3bn | $31.1bn |
| OCF (≈EBITDA) | $1.3bn | $6.9bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

> **Provenance / fidelity flag:** NBIS is the **restructured ex-Yandex entity** — Dutch holdco (Nebius Group N.V., Schiphol/Amsterdam), Nasdaq:NBIS. In **July 2024 it divested all Russia + related international businesses (>95% of consolidated revenue, assets and employees** at the time); trading resumed **2024-10-21** (20-F FY2025, 2026-04-30). Short public history as an AI company → financials are **immature and reorganized** (Toloka deconsolidated Q2 2025 and recast into discontinued ops). On-disk **filings are SEC 20-F** (foreign private issuer; no 10-Q/10-K). The two transcripts read (Q1 2026 2026-05-13, Q4 2025 2026-02-12) are **third-party reconstructions** (fool.com / investing.com via WebFetch) — close paraphrase, not verbatim. **Outlook: attempted (`outlook.py --no-body --days 7`), returned no output in this session — treat as unavailable;** sell-side flow below is from on-disk `E:\briefings\2026`.

## Snapshot
Nebius is a **global, multi-tenant AI neocloud** — a full-stack GPU cloud (compute clusters, storage, networking + in-house software/managed services) "purpose built for AI," spanning training and inference at scale (20-F FY2025, 2026-04-30). **Three reportable segments:** the core **Nebius** AI cloud (FY2025 $480.3m, +603% y/y, ~91% of segment revenue), **TripleTen** edtech (re-skilling; $54.1m, +88%), and **Avride** autonomous-vehicle/delivery robotics ($1.3m). Group revenue **$529.8m FY2025 vs $91.5m FY24 vs $9.8m FY23** — a >450% step-up. It also holds significant equity stakes in **ClickHouse** (~25%, ~$15bn round) and **Toloka** (equity-method since May 2025), both spun out, plus 2026 bolt-ons **Tavily / Eigen AI / Clarifai** (20-F FY2025; Q1 2026 call). In the value chain it sits in the **AI-infrastructure / neocloud layer** — buying NVIDIA GPUs, power and capital upstream, selling reserved + on-demand GPU capacity to AI labs and enterprises downstream. SemiAnalysis maps it across the **IaaS layer** (multitenant SLURM/K8s clusters) and **PaaS layer** (selling fractions of GPU clusters to startups), and rates it a **Gold-tier neocloud — behind CoreWeave** but ahead of Azure on managed-cluster UX (SemiAnalysis ClusterMAX, Patel et al., 2025-11-12). The whole thesis is an **ARR ramp racing ahead of a multi-billion funding/capex burn** toward profitability.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Nebius AI GPU cloud — reserved + on-demand compute (~91% of segment rev) · 2) Token Factory inference · 3) TripleTen edtech |
| **Main buyer(s)** | Hyperscaler anchors Microsoft + Meta, plus AI labs / startups / enterprises; highly concentrated — 83% of FY2025 receivables from a single customer |
| **Key suppliers** | NVIDIA GPUs (GB300 / Vera Rubin; $2bn NVDA stake, "Exemplar Cloud"); datacenter land/power (3.5+ GW); capital ($6bn+ raised) |

## Position in the value chain
Nebius converts three scarce upstream inputs — **NVIDIA GPUs, datacenter land/power, and capital** — into contracted AI compute sold to AI labs and enterprises. The differentiation is owned, in-house full-stack infra (>75% owned capacity, 3.5+ GW contracted) plus an NVIDIA "Exemplar Cloud" relationship and a $2bn NVDA equity stake. The structural tension to underwrite: **ARR ramped to ~$1.9bn (Q1 2026) against a $20–25bn 2026 capex plan and $6bn+ raised** — i.e., a self-funding flywheel that still depends on continuous capital access and on two anchor hyperscaler customers (Microsoft, Meta). A structural tailwind flagged by SemiAnalysis: Microsoft underestimated XPU-cloud demand, is "firmly back to the market" but out of near-term capacity, and is now **forced to rent GPUs from neoclouds (Nebius named) and resell at materially lower margin via Foundry** — demand pull for NBIS, margin pain for Azure (Patel et al., 2025-11-12). Cross-theme: [ai-datacenter-power](themes/ai-datacenter-power.md) — power/land + the NVDA chip ramp are the binding constraints.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 220" font-family="sans-serif" font-size="12">
  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#444"/>
    </marker>
  </defs>
  <!-- Suppliers -->
  <rect x="8" y="40" width="160" height="140" rx="6" fill="#eef3f8" stroke="#5b7c99" stroke-width="1.5"/>
  <text x="88" y="60" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="88" y="82" text-anchor="middle" font-size="11">NVIDIA GPUs</text>
  <text x="88" y="100" text-anchor="middle" font-size="11">(GB300 / Vera Rubin)</text>
  <text x="88" y="122" text-anchor="middle" font-size="11">Datacenter / power</text>
  <text x="88" y="140" text-anchor="middle" font-size="11">(land, 3.5+ GW)</text>
  <text x="88" y="162" text-anchor="middle" font-size="11">Capital ($6bn+ raised)</text>
  <!-- Nebius -->
  <rect x="230" y="25" width="260" height="170" rx="8" fill="#fdf1e3" stroke="#d08a3e" stroke-width="2"/>
  <text x="360" y="47" text-anchor="middle" font-weight="bold">Nebius — AI neocloud</text>
  <text x="360" y="63" text-anchor="middle" font-size="10">full-stack GPU cloud, &gt;75% owned</text>
  <rect x="245" y="76" width="230" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="360" y="93" text-anchor="middle" font-size="10">Train + inference (Token Factory)</text>
  <rect x="245" y="108" width="110" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="300" y="125" text-anchor="middle" font-size="9">ClickHouse 25%</text>
  <rect x="365" y="108" width="110" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="420" y="125" text-anchor="middle" font-size="9">Toloka (eq. mthd)</text>
  <rect x="245" y="140" width="110" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="300" y="157" text-anchor="middle" font-size="9">Avride (AV/robots)</text>
  <rect x="365" y="140" width="110" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="420" y="157" text-anchor="middle" font-size="9">TripleTen (edtech)</text>
  <text x="360" y="186" text-anchor="middle" font-size="9" font-style="italic">ex-Yandex; Russia divested Jul-2024</text>
  <!-- Customers -->
  <rect x="552" y="40" width="160" height="140" rx="6" fill="#eef8ef" stroke="#5a9367" stroke-width="1.5"/>
  <text x="632" y="60" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="632" y="84" text-anchor="middle" font-size="11">Hyperscalers</text>
  <text x="632" y="100" text-anchor="middle" font-size="11">(Microsoft, Meta)</text>
  <text x="632" y="124" text-anchor="middle" font-size="11">AI labs / startups</text>
  <text x="632" y="142" text-anchor="middle" font-size="11">Enterprise</text>
  <text x="632" y="160" text-anchor="middle" font-size="10">ARR ~$1.9bn → $7–9bn</text>
  <!-- arrows -->
  <line x1="168" y1="110" x2="227" y2="110" stroke="#444" stroke-width="2" marker-end="url(#ar)"/>
  <line x1="490" y1="110" x2="549" y2="110" stroke="#444" stroke-width="2" marker-end="url(#ar)"/>
</svg>

## Current state (Q1 2026, call 2026-05-13)
Beat-and-raise, with the EBITDA inflection now the story. **Group revenue $399m (+684% y/y, +75% q/q); Nebius core $390m (~98% of group, +841% y/y).** **ARR ~$1.9bn exit** (up from ~$1.25bn q/q). **Group adj. EBITDA $130m (32% margin)** vs $15m in Q4'25; **Nebius AI adj. EBITDA margin 45%** (from 24%). Net income $621m flattered by a non-cash ClickHouse revaluation gain (598.9m gain at FY level — not operating). Operating cash flow **$2.3bn** on record customer prepayments; **cash $9.3bn** (Q1 2026, 2026-05-13).
- **2026 guide:** group revenue **$3.0–3.4bn**, **ARR $7–9bn** exit, adj. EBITDA margin **~40%**, **capex raised to $20–25bn** (from $16–20bn at Q4) — "in response to pre-committed customer demand for 2027 capacity." CFO flags "nonlinear quarterly adjusted EBITDA margin progression" (back-end-weighted deploys).
- **Capacity:** 3.5+ GW contracted, targeting 4+ GW YE2026; >75% owned; new **Pennsylvania** owned site (250–300 MW by end-2027, 1.2 GW by 2030); Alabama/Missouri early-2027. DCs in Finland (owned) + France, Iceland, UK, Israel, US (incl. New Jersey).
- **Anchor contracts:** **Meta $27bn / 5yr** ($12bn dedicated compute from early-2027 + $15bn discretionary capacity option); **Microsoft** ramping H2 2026. Both structured to unlock asset-backed financing (Q1 2026; MS+2 Meta contracts "unlock significant ABF at attractive terms," NBIS CFO via briefing 2026-05-13).
- **Microsoft contract — terms (Hedgeye/Felix Wang, 2025-12-10):** announced Sep-2025, **$17.4bn contract value (upsize to $19.4bn possible)**, 5-yr, supplying AI infra from the **Vineland, NJ** DC from late-2025 through 2031. Several tranches across 2025–26 (~1-yr trial period); **must deliver capacity on specified timelines — failure can trigger termination after a 60-day cure period**; **no minimum purchase obligations**; financing via cash / "cash flows under deal" / debt. NBIS runs a sales team solely dedicated to MSFT, framing demand as Copilot + own-model + Azure-resale compute (Boroditsky, CRO).
- **Meta contract — terms (Hedgeye/Felix Wang, 2025-12-10):** **$2.9bn contract value, 5-yr (to 2030), two tranches (Dec-2025, Feb-2026)** — note this is materially below the **$27bn** headline NBIS guides to; reconcile as a signed/dedicated tranche vs. the larger discretionary option. Treat the gap as a watch item.
- **Vineland, NJ power (Barclays, 2026-01-21):** the MSFT site is a **400 MW fully-islanded** AI DC (MSFT signed the head lease); power via **Langley Holdings / BERGEN Engines — 36 × 11.2 MW medium-speed gas engines** ("first medium-speed reciprocating engine power plant in the US"). Bear flag: behind-the-meter gas + diesel backup drew local emissions/community pushback (Vineland city council, Nov-2025; DataOne flagged a deployment delay outside its control).
- **NVIDIA:** $2bn equity stake; GB300 "Exemplar Cloud" status; Vera Rubin/Vera CPU access; ~5 GW commitment through 2030.
- **GPU spot-price hike eff. 2026-06-01 (FundaAI "Deep|LLM 26H1 Part 2", 2026-06-24):** FundaAI reproduces NBIS's own customer email raising PAYG spot pricing **~30% across the board: H100 $2.95→$3.85/hr, H200 $3.50→$4.50, B200 $5.50→$7.15, B300 $6.10→$7.85**, with Chinese clouds raising in tandem. FundaAI cites it as direct supply-side evidence of the compute bottleneck (H100 one-year lease rates also +40% since 2025-10). This is a concrete, NBIS-specific **datapoint that cuts against the Hedgeye "neocloud pricing rollover" bear** (which flagged the first like-for-like decline back in Dec-2025) — spot pricing is now inflecting up into the sold-out backdrop (FundaAI, 2026-06-24). [Source](../relat%C3%B3rios%20bons/LLM_Part_2_funda.html)

## Debate / thesis
- **Bull:** Hyper-growth at scale with a credible margin inflection — core EBITDA margin 24%→45% in two quarters, ARR ~$1.9bn on a path to $7–9bn, fully sold out ("4 or more customers competing for every GPU we bring online," Q1 call via briefing 2026-05-14). Hyperscaler validation (Meta $27bn, Microsoft) + NVDA's $2bn equity and "Exemplar Cloud" status de-risk supply and signal preferred-partner standing ("Nebius will take care of you," Jensen, via @paradislabs briefing 2026-06-01). Structural demand pull from Microsoft's capacity shortfall — MSFT now forced to rent neocloud GPUs (Nebius named) and resell at lower margin (SemiAnalysis, 2025-11-12). Owned capacity (>75%) + 3.5+ GW contracted is a scarce, contractable asset. Pricing power now visible in the spot book — NBIS **raised PAYG GPU pricing ~30% eff. 2026-06-01** (H100 $2.95→$3.85, B200 $5.50→$7.15, B300 $6.10→$7.85), a direct rebuttal to the Hedgeye pricing-rollover bear (FundaAI, 2026-06-24). **BofA Buy, PO $205** (briefing 2026-05-11); high-conviction retail/buy-side neocloud pick ("$NBIS a 7-bagger… largest position," @mvcinvesting, briefing 2026-05-06); repeatedly on 52-week-high lists through May–June 2026. Beat read positively vs CRWV's softer margins (briefing 2026-05-13).
- **Bear:** (0) **"Meta Compute" pivot (NEW, Citi Tech Research call summary — Alex Placeres/Ron Josey/Tyler Radke/Mike Rollins/Heath Terry, via Daniel Grozdea, 2026-07-01):** Nebius flagged among neoclouds with meaningful Meta exposure now facing headline risk from Meta's newly announced "Meta Compute" pivot — Meta launched an external cloud business the same day to sell surplus AI computing capacity, competing directly with AWS/Azure/GCP and, by extension, neoclouds like Nebius and CoreWeave. This complicates the long-standing bull framing of Meta purely as a captive/growing anchor customer (see Changelog 2026-07-01) — Meta is simultaneously a major buyer (Barclays/Ross Sandler: $20bn+ TCV deals with both CoreWeave and Nebius, referenced in the Meta Compute coverage, 2026-06-30) and a prospective competitor for external compute-capacity sales. (1) **Capital intensity & funding dependence** — 20-F headline risk: "core business is capital-intensive and currently not profitable… ability to continue to operate and to grow will depend in large part on our ability to raise additional equity or debt financing." $20–25bn 2026 capex dwarfs revenue; dilution + a "more complex capital structure" with secured/unsecured layers are explicit risks (20-F FY2025). Hedgeye models NBIS **flipping from net cash to ~$15–20bn net debt FY2026–27** (incl. lease liabilities), with operating lease liabilities surging and gross margins that "may not grow" on high electricity/memory/labor costs (Hedgeye, 2025-12-10). (2) **Customer concentration** — **83% of FY2025 receivables from a single "Customer D"** (20-F FY2025); the whole 2027 ramp leans on Microsoft + Meta delivery over 5-year contracts. (3) **MSFT execution / NJ delay risk (NEW, Hedgeye 2025-12-10):** Vineland NJ DC not yet online and "not in NBIS's control" (DataOne); ~2-month slip vs. promised 300 MW reveal; Hedgeye assigns a **~20% chance MSFT falls through** and notes the contract's must-deliver-or-terminate (60-day cure) structure — "the longer this gets delayed, the bigger the risk MSFT walks away." (4) **Neocloud pricing rollover (NEW, Hedgeye 2025-12-10):** first like-for-like neocloud GPU price decline in 3 months; NBIS B200 pricing now only cheaper than CRWV; implied revenue per connected MW flat 2024→2025 (~$1.00) on heavy contra-revenue subsidies/discounts — needs B200/B300/R200 lift to hit estimates. (5) **"CoreWeave 2.0"** — Hedgeye flipped NBIS from Long to **Tactical Short (Dec-4-2025 @ $99.1; ~25% downside on a 2027 SOTP** assuming 20% MSFT risk + 2–3% rental price erosion), having ridden the long from $53.6 (Aug-4) to $101 (Nov-11). (6) **Circular GPU-financing scrutiny** — Burry's "Fugazi… make tens of $billions of NVDA GPUs disappear from balance sheets" thesis and "$IREN/$NBIS got NVDA funds" chatter name NBIS directly (briefings 2026-05-12, 2026-06-01). (7) **Net income is non-cash-gain flattered** (ClickHouse revaluation), not operating profit. (8) Immature company, intensely competitive neocloud market, GPU/power/talent supply constraints (20-F).
- **Peer positioning — $/MW comparison (Bernstein · Madison/Gautam, 2026-07-01):** Bernstein groups Nebius (NBIS) with CoreWeave (CRWV) and IREN in a $/MW analysis comparing neoclouds vs. data-center REITs vs. emerging AI-infra providers across margin, revenue yield, financing, capex and risk profile. Within the emerging AI-infra cohort, CIFR and WULF stand out on leasing margins; IREN shows strong margins from vertically-integrated landlord economics but lags CRWV/peers on scale/enterprise build — useful cross-check for where NBIS sits on the margin/scale spectrum vs. its closest comps.
- **Where the sell-side/buy-side stands:** **BofA — Buy, PO $205** (PO ↑, reit.; 1Q26 preview, briefing 2026-05-11; thesis: DC site activation supporting 2H26 ramp, capex intensity). **Morgan Stanley (Baer) — Equal-Weight, PT $126→$144** post-Q1 (Q1 rev $399m, ARR $1.92B, capex $20–25B; briefing 2026-05-14). **Hedgeye (Felix Wang) — Tactical Short** (Dec-4-2025 @ $99.1, ~25% downside; "Neocloud Winter / CRWV 2.0" thesis on MSFT/NJ delay + pricing rollover + net-debt swing, 2025-12-10). Conference presence: BofA SF Global Tech (Jun 2–4) alongside the hyperscalers/CRWV. No dedicated `by-ticker/NBIS.md` roll-up on disk.

## Catalysts / what to watch
- **Q2 2026 print** — by cadence ~early Aug 2026 (Q2'25 was 2025-08-07). Watch ARR trajectory toward the $7–9bn exit and the EBITDA margin path to ~40%.
- **Vineland, NJ / Microsoft delivery (key bear gate)** — whether the 300 MW / 400 MW-islanded site comes online on the contracted timeline; any slip raises the must-deliver-or-terminate (60-day cure) risk Hedgeye flags. H2 2026 MSFT ramp; potential $17.4bn→$19.4bn upsize.
- **Capacity activations** — Q3 & Q4 2026 deploys; first PA megawatts (end-2027); Alabama/Missouri (early-2027); progress to 4+ GW contracted.
- **Funding milestones** — first asset-backed financings on the MSFT/Meta contracts; whether the ATM (25M Class A shares) gets tapped; any new debt layers; net cash → net debt crossover (Hedgeye FY2026 est.).
- **Neocloud pricing** — like-for-like GPU rental pricing trend (Hedgeye flagged the first 3-month decline); B200/B300/R200 mix lift needed to hold revenue-per-MW.
- **Meta contract reconciliation** — the $2.9bn signed value (Hedgeye) vs. $27bn headline; tranche timing (Dec-2025, Feb-2026) and which facility houses the chips.
- **EU AI gigafactories** — NBIS may bid in the EU's formal AI-gigafactory process (launch Jan/Feb 2026, bidding ends summer 2026; majority-EU consortia required) (Hedgeye/WSJ, 2025-12-10).
- **Stakes** — ClickHouse / Toloka monetization or further markups; TripleTen/Avride strategic-partner outcomes; mgmt sees equity stakes as a multi-billion non-dilutive funding source (NBIS IR, Dec-2025).
- **"Meta Compute" ramp (NEW, Citi Tech Research call summary, 2026-07-01)** — watch whether Meta's newly launched external-cloud/surplus-compute business (competing with AWS/Azure/GCP and neoclouds) changes Meta's demand behavior as a Nebius anchor customer, or emerges as a direct competitive alternative for compute buyers Nebius targets.

## Risks
- Not profitable on an operating basis; extremely capital-intensive; growth depends on continuous access to equity/debt/ABF on acceptable terms — dilution and complex secured/unsecured capital structure (20-F FY2025). Hedgeye models a net-cash-to-net-debt swing and stagnant gross margins (2025-12-10).
- Severe customer concentration (83% of FY2025 receivables from one customer); dependence on two hyperscaler anchors over multi-year contracts (20-F FY2025).
- Microsoft contract execution: capacity must be delivered on specified timelines or face termination after a 60-day cure period; the Vineland, NJ site has experienced delays outside NBIS's direct control (Hedgeye 2025-12-10; Barclays 2026-01-21).
- Neocloud price erosion: like-for-like GPU rental pricing has begun to fall; heavy contra-revenue subsidies keep revenue per connected MW flat (Hedgeye 2025-12-10).
- Dependent on a limited number of suppliers for sophisticated hardware (NVIDIA GPUs); supply-chain, power, land and talent constraints (20-F FY2025).
- Immature, rapidly changing, intensely competitive AI-cloud market; any material reduction in AI spending hits results (20-F FY2025).
- Ex-Yandex provenance / short operating history; restated/recast comparatives (Toloka discontinued ops); export-control and cross-border regulatory exposure (20-F FY2025).
- Reported net income flattered by non-cash equity-revaluation gains (ClickHouse), not operating profit (20-F FY2025; Q1 2026 call).
- **Meta "Meta Compute" pivot (NEW, Citi Tech Research call summary, 2026-07-01):** Meta launched an external cloud business the same day to monetize surplus AI compute capacity, competing directly with AWS/Azure/GCP and, by extension, with neoclouds including Nebius and CoreWeave. Nebius is named among neoclouds with meaningful Meta exposure — Meta has signed $20bn+ TCV deals with both CoreWeave and Nebius (Barclays/Ross Sandler, referenced in the Meta Compute coverage, 2026-06-30), so a Meta compute-supply pullback or Meta's own external-cloud ramp both represent a headline risk to the anchor-contract bull case.
- **Compute-deal pricing / cash-ROIC backdrop (Citi Tech Research call summary, 2026-07-01):** recent large AI compute deals struck at $40-60bn annually per GW, a 30-60%+ premium to spot; hyperscaler cash ROIC on AI investment ~29%; data-center leasing focus has shifted to the 2028-2030 timeframe with power/NIMBYism as binding constraints — relevant backdrop for underwriting Nebius's own capacity-build economics and contract pricing.

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

> **AI-monetization angle:** NBIS is a pure **AI-infrastructure / token-supply** play — it monetizes GPU compute (training + the Token Factory inference product) rather than selling software. Demand pull is the AI capex cycle and NVDA chip ramp; the gate is power, land and capital. See [ai-datacenter-power](themes/ai-datacenter-power.md).

## In the inbox (Outlook — recent sell-side flow)
- **Cantor neocloud call — Nebius read-through (Cantor "CoreWeave call", 2026-06-18):** Cantor covers NBIS within the neocloud cohort (CoreWeave, Nebius, Iren, Crusoe, +Hive) and uses it as the bull comp for CRWV — **"Nebius and CoreWeave printed the same exact quarter in 1Q," both reiterated 2026 sold-out, both raised capex — yet Nebius is up ~80% since and has flipped CoreWeave in market cap** despite being "a bit the size in terms of deployed IT capacity." Cantor's read: the re-rating reflects the perception NBIS has **a lot of unsold capacity into rising GPU prices**; flags that NBIS aspires to be a more vertically-integrated full-stack AI cloud (vs. long-term capacity-reserve contracts) but **most NBIS revenue still comes from long-term capacity-reserve contracts** today (Cantor "CoreWeave call", 2026-06-18).
- **Fluidstack / neocloud financing read-through (Wells Fargo "Fluidstack call", 2026-06-08):** sector read-through to NBIS economics — **financing cost is the swing variable** (6% "ship it" vs high-teens "less excited"), the **Anthropic Q1 inflection drove the sector supply-demand imbalance**, and inference economics approaching human dollar-per-hour output underpin demand durability. Supports the NBIS sold-out / contracted-ramp thesis but reinforces the capital-access dependence already in the bear case (Wells Fargo "Fluidstack call", 2026-06-08).
- **BofA Buy PT $205** · **MS (Baer) EW $126→$144** · **NVIDIA $2B equity stake** _(briefings, 2026)_: ARR $7–9B / 45% EBITDA / Meta $27bn anchor.
- **Hedgeye Tactical Short** (Dec-4 @ $99.1, ~25% downside): "Neocloud Winter / CRWV 2.0" — MSFT NJ delay, pricing rollover, net-debt swing.
- **Burry 'circular GPU-financing' bear** + 83% single-customer receivable concentration — the funding/quality-of-earnings counter.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 2026 · May 11 → Jul 1, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Demand / sold-out** | Fully sold out — "4+ customers competing for every GPU we turn on" | Cantor (bull comp for CRWV): the re-rating reflects a perception of a lot of still-unsold capacity amid rising GPU prices | **⚠ nuance** (how much is already contracted?) |
| **ARR / guidance** | ARR ~$1.9bn exit (+50% q/q); '26 guide ARR $7-9bn, rev $3.0-3.4bn | MS Baer: EW, PT $126→$144 (acknowledges the numbers but the multiple already reflects them) | **✓ confirms** (numbers check out) |
| **Capex / funding** | Capex raised to $20-25bn "in response to pre-committed demand for '27" | WF Fluidstack: financing cost is the key variable (6% "ship it" vs high-teens "less excited") | **⚠ nuance** (depends on capital) |
| **NVDA validation / supply** | — | @paradislabs: NVDA $2bn stake + "Exemplar Cloud" GB300 + Vera Rubin access; Jensen: "Nebius will take care of you" | **✓ confirms** (NVDA seal of approval) |
| **Anchor contracts** | Meta $27bn/5yr; MSFT ramp H2'26 (structured to unlock ABF) | Cantor: most of the revenue still comes from LT capacity-reserve contracts | **✓ confirms** (contracted backlog) |
| **Meta relationship** | Meta framed purely as anchor customer ($27bn/5yr) | Citi (07-01): Meta's new "Meta Compute" external-cloud pivot creates headline risk — Meta is now also a prospective competitor for compute-capacity sales, not just a captive buyer; Barclays (06-30) confirms Meta is a named, material counterparty ($20bn+ TCV with NBIS) | **⚠ nuance** (customer-turned-competitor risk, newly flagged) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-11 | BofA | valuation | bull | BofA Buy, PO US$205 (PO raised, reit.; 1Q26 preview) — thesis: DC site activations supporting the 2H26 ramp, capex intensity (briefing 2026-05-11). |
| 05-13 | NBIS (earnings) · CFO (via briefing) | guidance | bull | 2026 guide: group revenue US$3.0-3.4bn, ARR US$7-9bn exit, adj. EBITDA margin ~40%, capex raised to US$20-25bn (from US$16-20bn in Q4) 'in response to pre-committed customer demand for 2027 capacity'. The Meta US$27bn/5yr and Microsoft (ramp H2 2026) contracts are structured to unlock ABF (briefing 2026-05-13). |
| 05-14 | Morgan Stanley · Baer | valuation | mixed | Morgan Stanley (Baer) Equal-Weight, PT US$126→US$144 post-Q1 (rev US$399m, ARR US$1.92B, capex US$20-25B; briefing 2026-05-14). |
| 05-14 | NBIS (earnings, via briefing) | demand | bull | Fully sold out — '4 or more customers competing for every GPU we bring online' (Q1 call via briefing 2026-05-14). |
| 06-01 | FinTwit · @paradislabs (via briefing) | supply | bull | NVIDIA validation: 'Nebius will take care of you' (Jensen, via @paradislabs briefing 2026-06-01). NVDA US$2bn stake + 'Exemplar Cloud' GB300 status + Vera Rubin/Vera CPU access. |
| 06-08 | Wells Fargo · Fluidstack call | capital | mixed | Sector read-through for NBIS: financing cost is the swing variable (6% 'ship it' vs high-teens 'less excited'), the Anthropic inflection in Q1 drove the supply-demand imbalance, and inference economics approaching dollar-per-hour human output sustain demand durability. Supports the sold-out/contracted-ramp thesis but reinforces the dependence on capital access (Wells Fargo 'Fluidstack call', 2026-06-08). |
| 06-18 | Cantor · 'CoreWeave call' | valuation | bull | Cantor uses NBIS as a bull comp for CRWV — 'Nebius and CoreWeave printed the same exact quarter in 1Q', both reaffirmed 2026 sold-out and raised capex, yet NBIS is up ~80% since and overtook CoreWeave in market cap despite less deployed IT capacity. The re-rating reflects the perception that NBIS has a lot of unsold capacity amid rising GPU prices; signals that most of NBIS's revenue still comes from long-term capacity-reservation contracts (Cantor 'CoreWeave call', 2026-06-18). |
| 06-28 | FundaAI Weekly | valuation | bull | **NBIS re-rating thesis: "from scarce GPU capacity to full-stack AI cloud."** FundaAI argues the market is beginning to reprice NBIS as a full-stack AI cloud rather than a raw GPU provider, driven by: (1) **Token Factory** — NBIS's inference product targets volume token generation at high utilization rates; rising utilization rate is the primary re-rating lever; (2) **stronger open-source models as a tailwind** — cheaper frontier-adjacent models (Llama, Mistral, etc.) drive Token Factory demand by making per-token inference more cost-effective vs proprietary APIs; (3) **Meta signed neocloud agreements (NBIS, March 2026)** — context: Google reportedly limited Meta's access to Gemini, prompting Meta to diversify inference infra to neoclouds including NBIS; confirms NBIS is entering the hyperscaler-adjacent tier of customers, not just startups. Re-rating from GPU-capacity multiples (~7x EV/revenue) toward cloud-platform multiples (~15-20x EV/revenue) requires demonstrated Token Factory scale. (FundaAI Weekly, 2026-06-28) |
| 06-30 | Barclays · Ross Sandler (referenced in Meta Compute coverage) | demand | mixed | Meta has signed $20bn+ TCV deals with neoclouds CoreWeave AND Nebius, plus multi-year deals with Oracle, Google Cloud and AWS — confirms Nebius as a named, material Meta compute-supply counterparty, which is precisely what makes it directly exposed to any Meta pullback or Meta's own compute-monetization pivot (Barclays · Ross Sandler, 2026-06-30). |
| 07-01 | Citi Tech Research call summary · Alex Placeres/Ron Josey/Tyler Radke/Mike Rollins/Heath Terry (via Daniel Grozdea) | risk | bear | **"Meta Compute" headline risk:** Nebius counted among neoclouds with meaningful Meta exposure; Meta launched an external cloud business the same day to sell surplus AI computing capacity, competing directly with AWS/Azure/GCP and, by extension, neoclouds like Nebius and CoreWeave. Separately: recent large AI compute deals struck at $40-60bn annually per GW (30-60%+ premium to spot); hyperscaler cash ROIC on AI investment ~29%; data-center leasing focus now on 2028-2030 with power/NIMBYism as binding constraints (Citi Tech Research call summary, 2026-07-01). |
| 07-01 | Bernstein · Madison/Gautam | valuation | neutral | $/MW analysis groups Nebius (NBIS) with CoreWeave (CRWV) and IREN comparing neoclouds vs. data-center REITs vs. emerging AI-infra providers on margin, revenue yield, financing, capex and risk profile. Within emerging AI-infra, CIFR and WULF stand out on leasing margins; IREN shows strong vertically-integrated landlord margins but lags CRWV/peers on scale/enterprise build (Bernstein · Madison/Gautam, 2026-07-01). |

**Quarter synthesis:** the flow validates the numbers, the sold-out status and the NVDA seal of approval, but the debate has shifted to two quality nuances — how much of the capacity is already contracted vs speculative amid rising GPU prices (Cantor), and the dependence on financing cost as the swing variable (WF). Thesis intact; the question has become "at what cost of capital does the '27 ramp hold up." **06-28: FundaAI adds a re-rating framework** — the bull case is no longer just "sold-out GPU cloud" but a full-stack AI cloud trajectory via Token Factory; the key milestones are utilization rate rising and Meta-class enterprise customers confirming the hyperscaler-adjacent tier. If NBIS demonstrates Token Factory at scale in 2H26, the multiple narrative shifts from capacity leasing to cloud SaaS, which is a meaningful re-rating lever. **07-01: new risk vector emerges** — Citi flags Meta's freshly launched "Meta Compute" external-cloud business as a headline risk: Meta is a confirmed, material Nebius compute-supply counterparty (Barclays, $20bn+ TCV, 06-30), but is now also entering the market as a seller of surplus AI compute, competing with the very neoclouds (Nebius, CoreWeave) it funds as a customer. This complicates the previously one-directional "Meta = anchor customer" bull framing without yet contradicting the underlying contract economics; watch whether Meta's own compute-monetization ramp changes its demand behavior toward Nebius. Bernstein's same-day $/MW cross-comp (NBIS vs. CRWV vs. IREN vs. data-center REITs/emerging AI-infra) is a useful positioning check but does not change the thesis.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2'25 (2025-08-07) | Q3'25 (2025-11-11) | Q4'25 (2026-02-12) | Q1'26 (2026-05-13) |
|---|---|---|---|---|
| Revenue / core growth | $105m rev, +625% y/y | $146m rev, +355% y/y | $228m rev, +547% y/y; core +830% | $399m rev, +684% y/y; core +841% |
| ARR / target | end-2025 ARR raised $900m–$1.1bn | ARR maintained; first $7–9bn-by-2026 target | ~$1.2bn exit, above guide | ~$1.9bn exit, +50% q/q |
| Profitability (adj. EBITDA) | core positive, ahead of plan | core AI margin ~19% | core margin 24%; group inflected positive | group 32%; core 45% |
| Capex / funding | — | 2025 capex raised ~$2bn→~$5bn | 2026 capex $16–20bn | capex raised $20–25bn; $6bn+ raised |
| Capacity / power | NJ first tranche on time | supply tight into 2026 | 2+ GW contracted, 3+ GW YE26 target | 3.5+ GW, >75% owned; PA site added |
| Anchor contracts | Microsoft first tranche on time | Meta + Microsoft long-term deals signed | Meta fully deployed; MSFT through 2026 | Meta $27bn/5yr; MSFT ramps H2'26 |

_Source: NBIS earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [20-F FY2025 (2026-04-30)](../NBIS/NBIS_20-F_2026-04-30_0001104659-26-052948.html) — business overview, segments, MD&A, risk factors · [20-F/A Amdt. No.1 (2026-05-22)](../NBIS/NBIS_20-F-A_2026-05-22_0001104659-26-065681.html) — FY2025 amendment · prior 20-Fs [FY2024 (2025-04-30)](../NBIS/NBIS_20-F_2025-04-30_0001558370-25-005991.html), [FY2023 (2024-04-26)](../NBIS/NBIS_20-F_2024-04-26_0001558370-24-005891.html), [FY2022 (2023-04-20)](../NBIS/NBIS_20-F_2023-04-20_0001558370-23-006319.html). _No 10-K/10-Q — foreign private issuer._
- **Transcripts:** [Q1 2026 (2026-05-13)](../NBIS/transcripts/NBIS_Q1-2026-earnings_2026-05-13.md) · [Q4 2025 (2026-02-12)](../NBIS/transcripts/NBIS_Q4-2025-earnings_2026-02-12.md) — both read · [Q3 2025 (2025-11-11)](../NBIS/transcripts/NBIS_Q3-2025-earnings_2025-11-11.md) · [Q2 2025 (2025-08-07)](../NBIS/transcripts/NBIS_Q2-2025-earnings_2025-08-07.md) — saved, headline-only. _Latest two are third-party paraphrase — see fidelity flag._
- **Research reports (relatórios bons):**
  - [HE Global Technology BB — Neocloud Winter / Tactical Short NBIS (Felix Wang, 2025-12-10)](../relat%C3%B3rios%20bons/HE_Global_Technology_BB_DEC2025_1.html)
  - [SemiAnalysis — Microsoft's AI Strategy Deconstructed: From Energy to Tokens (Patel et al., 2025-11-12)](../relat%C3%B3rios%20bons/Microsofts_AI_Strategy_Deconstructed_-_from_Energy_to_Tokens.html)
  - [Barclays — Powering AI: Gas Turbines Could Make or Break AI Ambitions (2026-01-21)](../relat%C3%B3rios%20bons/Barclays_Powering_AI_Gas_Turbines_Could_Make_or_Break_AI_Ambitions.html)
  - [Cantor — CoreWeave call (2026-06-18)](../relat%C3%B3rios%20bons/2026_06_18_call_coreweave_cantor.html) — Nebius/CoreWeave same 1Q, NBIS +80% / flipped CRWV market cap; unsold capacity into rising GPU prices; mostly capacity-reserve revenue.
  - [Wells Fargo — Fluidstack / neocloud financing call (2026-06-08)](../relat%C3%B3rios%20bons/2026_06_08_fluidstack_welss_fargo_8_un_26.html) — financing cost the swing variable; Anthropic Q1 inflection; inference dollar-per-hour durability.
  - [FundaAI — "Deep|LLM 26H1 Update Part 2: Frontier Labs & the Compute Bottleneck" (2026-06-24)](../relat%C3%B3rios%20bons/LLM_Part_2_funda.html) — reproduces NBIS's customer email: PAYG GPU spot prices +~30% eff. 2026-06-01 (H100 $2.95→$3.85, B200 $5.50→$7.15) — supply-bottleneck / pricing-power datapoint vs the Hedgeye rollover bear.
  - Citi Tech Research call summary (Alex Placeres/Ron Josey/Tyler Radke/Mike Rollins/Heath Terry, via Daniel Grozdea, 2026-07-01) — "Meta Compute" headline risk for neoclouds incl. NBIS; compute-deal pricing ($40-60bn/GW annually, 30-60%+ premium to spot), hyperscaler cash ROIC ~29%, 2028-2030 leasing focus.
  - Bernstein · Madison/Gautam (2026-07-01) — $/MW analysis: NBIS vs. CRWV vs. IREN vs. data-center REITs/emerging AI-infra (CIFR, WULF) on margin, revenue yield, financing, capex, risk.
  - Barclays · Ross Sandler (referenced in Meta Compute coverage, 2026-06-30) — Meta $20bn+ TCV deals with both CoreWeave and Nebius, plus Oracle/Google Cloud/AWS multi-year deals.
- **Equity calls:** 0 attributed (no NBIS section in INDEX).
- **Briefings:** `E:\briefings\2026` — ~88 .md/.html files mention NBIS (BofA Buy $205; MS EW $126→$144; NVDA $2B stake; $7–9B ARR / 40% EBITDA / 4GW / Meta $27bn flow; Burry circular-financing bear). No `by-ticker/NBIS.md` roll-up on disk.
- **Outlook:** attempted `outlook.py --no-body --days 7` — no output returned this session; unavailable.

## Changelog
| Date | Change |
|---|---|
| 2026-07-01 | Prior bull framing (through 06-28) treated Meta purely as a growing/captive anchor customer ($27bn/5yr contract, hyperscaler validation) with no competitive dimension flagged. Superseded/complicated — not contradicted — by Citi's 2026-07-01 "Meta Compute" flag: Meta launched an external cloud business the same day, selling surplus AI compute and competing directly with AWS/Azure/GCP and, by extension, neoclouds incl. Nebius/CoreWeave. Added as new Debate/Risks/Catalysts bullets + 2 intra-quarter rows (06-30 Barclays Meta TCV confirmation, 07-01 Citi Meta Compute + compute-deal pricing backdrop, 07-01 Bernstein $/MW cross-comp). Updated Signal-vs-management table and quarter synthesis. |
| 2026-06-28 | Added 1 intra-quarter row (06-28): FundaAI re-rating thesis — "from scarce GPU capacity to full-stack AI cloud" (Token Factory, utilization as re-rating lever, Meta neocloud agreements March 2026). Updated quarter synthesis. |
