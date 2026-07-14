<!-- Per-company wiki page. Financials block ("Consensus estimates (BBG)") is auto-injected by
     build_wiki_html.py from _data/estimates.json — do NOT hand-write it. -->

# DELL — Dell Technologies Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\DELL` (filings + transcripts) · `_equity_calls` · `E:\briefings\2026`. Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $162.4bn | $194.9bn |
| Gross profit | $28.6bn | $34.1bn |
| Gross margin | 17.6% | 17.5% |
| EBITDA | $16.7bn | $20.7bn |
| EPS | $16.60 | $21.98 |
| Capex | $3.6bn | $4.0bn |
| OCF (≈EBITDA) | $16.7bn | $20.7bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Dell is the world's largest server/storage OEM and #1/#2 commercial PC vendor, now re-architected around AI infrastructure. Two reporting segments: **ISG** (Infrastructure Solutions Group — AI-optimized servers, traditional servers & networking, storage) and **CSG** (Client Solutions Group — commercial + consumer PCs). FY26 (ended 2026-01-30) revenue **$113.5B, +19%** (FY26 10-K), split ISG $60.8B / CSG $51.0B. The story is the AI-server ramp: AI-optimized servers went **$1.9B → $9.3B → $24.7B** (FY24→FY25→FY26) and management guides **~$60B for FY27** (Q1 FY27 print). At its 2025 Securities Analyst Meeting Dell **raised its long-term framework** to **7–9% revenue / 15%+ EPS growth** (from 3–4% / 6–8% in 2021/2023), targeting EPS to roughly double over five years (Dell SAM deck, 2025-10-07). Dell sits in the middle of the AI value chain — buying GPUs/components (chiefly NVIDIA + memory) and integrating, deploying and servicing rack-scale systems for neoclouds, sovereigns and enterprises. Capital-light model (no material buys until customer PO), shareholder-friendly (dividend +20%, buyback), ≥15% LT EPS framework.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) AI-optimized servers (ISG, $24.7B FY26) · 2) Commercial & consumer PCs (CSG, $51.0B) · 3) Traditional servers, networking & storage (ISG) |
| **Main buyer(s)** | Neoclouds (majority of AI-server rev) + enterprise + sovereign/hyperscaler for ISG; commercial & consumer for CSG; 5,000+ AI-factory customers, $53.1B AI backlog |
| **Key suppliers** | NVIDIA GPUs (GB200/GB300/Rubin); memory — DRAM/HBM/NAND (#1 2H constraint); components/optics; L7–L10 assembly outsourced to Wistron/Inventec |

## Position in the value chain
Dell is the systems integrator between silicon and the AI buyer: it takes NVIDIA GPUs + memory/components and ships engineered, deployed, serviced rack-scale AI factories plus storage; CSG is the PC leg. It is the **largest server OEM at ~9% share** (BofA DC primer; ODM-direct ~46% of the market, so OEMs split the rest). The bull case is AI-server **momentum + supply-chain execution moat**; the bear case is that AI-optimized servers carry **thin margins** that dilute ISG (segment margin 11.7% FY26 vs 12.8% FY25, FY26 10-K) — volume up, mix down. Bernstein pegs **AI-server operating margin at ~5% or less vs low-teens for traditional servers**, but argues the absolute-dollar opportunity is large and that AI-server margins should expand as enterprise/on-prem adoption mixes up (Bernstein initiation, 2025-09-15). A structural watch-item: NVIDIA's move to ship finished L10 compute trays (Rubin/VR200) could migrate value and margin upstream to NVIDIA — flagged **negative for Dell/SMCI** — though the impact on Dell is muted since it already outsources L7–L10 to Wistron/Inventec (Q425 Techknowledge takeaways). Relevant cross-link: [ai-datacenter-power](themes/ai-datacenter-power.md) (rack-scale power/cooling readiness is a gating factor management repeatedly cites).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12">
  <rect x="10" y="40" width="170" height="140" rx="6" fill="#eef3fb" stroke="#2c5d9b"/>
  <text x="95" y="62" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="95" y="84" text-anchor="middle">NVIDIA GPUs</text>
  <text x="95" y="104" text-anchor="middle">(GB200/GB300/Rubin)</text>
  <text x="95" y="126" text-anchor="middle">DRAM / HBM / NAND</text>
  <text x="95" y="148" text-anchor="middle">components, optics</text>
  <rect x="275" y="25" width="180" height="170" rx="6" fill="#e9f7ee" stroke="#1f8a4c"/>
  <text x="365" y="48" text-anchor="middle" font-weight="bold">DELL</text>
  <text x="365" y="72" text-anchor="middle">ISG: AI servers</text>
  <text x="365" y="90" text-anchor="middle">+ traditional servers</text>
  <text x="365" y="108" text-anchor="middle">+ storage</text>
  <text x="365" y="132" text-anchor="middle">CSG: PCs</text>
  <text x="365" y="158" text-anchor="middle" font-style="italic">integrate · deploy</text>
  <text x="365" y="176" text-anchor="middle" font-style="italic">service · finance</text>
  <rect x="550" y="40" width="160" height="140" rx="6" fill="#fdf2e9" stroke="#c2660c"/>
  <text x="630" y="62" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="630" y="86" text-anchor="middle">Neoclouds</text>
  <text x="630" y="108" text-anchor="middle">(majority of rev)</text>
  <text x="630" y="130" text-anchor="middle">Enterprise</text>
  <text x="630" y="152" text-anchor="middle">Sovereign / hyperscaler</text>
  <line x1="180" y1="110" x2="273" y2="110" stroke="#444" stroke-width="2" marker-end="url(#a)"/>
  <line x1="455" y1="110" x2="548" y2="110" stroke="#444" stroke-width="2" marker-end="url(#a)"/>
  <defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#444"/></marker></defs>
  <text x="365" y="214" text-anchor="middle" fill="#1f8a4c" font-weight="bold">AI-server momentum (+757% YoY) — but thin AI-server margins dilute ISG mix</text>
</svg>

## Current state (latest quarter)
**Q1 FY27 (reported 2026-05-28; qtr ended 2026-05-01)** — the widest beat in Dell's public history:
- **Revenue $43.8B, +88% YoY**; GAAP op income $3.66B vs $1.17B; op margin +330bp; **EPS ~$4.86** vs ~$3.00 Street / ~$3.50 buy-side whisper (briefing 2026-05-29).
- **AI-optimized servers $16.1B vs $1.9B PY** (+757%); **traditional servers & networking $8.5B, +92%** (the surprise — agentic-inference CPU demand); storage $4.3B, +8% (Q1 FY27 10-Q).
- **AI-server orders $24.4B; backlog $53.1B; >$100B cumulative orders; 5,000+ AI-factory customers** (CFO David Kennedy / ISG pres. Arthur Lewis, JPM call 2026-05-29). For context, the SAM deck (2025-10-07) had cited **3,000+ unique AI-server customers to date** and **6,700+ in the five-quarter opportunity pipeline** — so the customer base has scaled materially.
- **Guidance raised:** FY27 revenue +~$27B at midpoint (~$140B→$168B); FY27 AI-server guide **$50B→$60B**; FY27 EPS guide **$12.9→$17.9** (Bernstein, 2026-05-29). 2H AI-server step-down framed as **supply, not demand**; **memory = #1 constraint** for 2H.
- CSG: commercial $13.0B / consumer $1.6B; Dell expects to beat a ~-18% 2H PC market and take share (JPM call, 2026-05-29).
- **Barron's "Top CEOs of 2026" profile of Michael Dell** frames the same Q1 FY27 inflection for a generalist audience: AI-optimized servers **"generated revenue of $16.1 billion in the first quarter, a 757% increase from the prior year"**; total revenue **$43.8 billion, a record and an increase of 88%**; shares **up more than 250% in the past 12 months** (Barron's/Andrew Bary, 2026-06-22).
- **Barron's Tech Trader (Adam Levine)** on the same print: server business **"sales up 181% from last year"** (broader server line, vs the +757%/+92% AI-server/traditional-server split disclosed elsewhere), plus a **"strong showing from the PC segment"** on raised PC prices and premium-segment share gains; flags a **"pull-forward of demand"** in PCs, comparable to HP's (Barron's, 2026-06-01).

## Long-term financial framework (SAM deck, 2025-10-07)
Dell's 2025 Securities Analyst Meeting (Michael Dell / Jeff Clarke / Arthur Lewis / interim CFO David Kennedy) materially **raised the multi-year framework** vs prior SAMs:
- **Total Dell:** revenue **7–9%** (vs 3–4% in 2021 & 2023), diluted EPS **15%+** (vs 6%+ in 2021, 8%+ in 2023), NI-to-adj.-FCF conversion **100%+**, return **80%+** of adj. FCF to shareholders, **dividend +10%/yr through FY30**.
- **Segment splits:** ISG **11–14%** revenue growth (AI-driven + share gain + Dell-IP storage); CSG **2–3%** (PC refresh of an aging ~1.5B install base).
- **EPS bridge** (four levers): durable revenue growth, gross-profit growth (storage Dell-IP mix + enterprise-AI rate), opex scaling, programmatic + opportunistic buybacks. Management expects **EPS to roughly double over five years** (non-GAAP diluted EPS path FY21 $4.88 → FY26E $9.55, a ~14% CAGR).
- **ISG history (SAM):** AI-server shipments drove ISG revenue to **$55.3B FY26E** with op income **$6.2B** at a **~9.9% rate** (op-inc rate progression 9.9% FY18 → 12.8% FY25); ISG targets gross-margin-accretion via storage growth, enterprise-AI attach and denser latest-gen traditional servers. **>70% of the traditional-server installed base is on 14G or older** — 16G/17G boxes replace 3–7 legacy units, with 17G ASPs up ~40% over three years on higher content.
- **Capital return:** $14.5B returned since FY23; dividend $1.32→$1.48→$1.78→$2.10 (FY23→FY26, +12%/+20%/+18%); committed to investment-grade rating and 1.5x core leverage with disciplined tuck-in M&A.

## Debate / thesis
- **Bull:** AI demand is durable, broad and re-accelerating into agentic; Dell is taking share as Supermicro/Lenovo stumble; supply-chain + deployment moat ("rack-to-production <6.5 hrs, 99% uptime," first-to-ship GB200/GB300/Rubin) is hard to replicate; capital-light, FCF-focused; raising prices to defend GM amid memory inflation and *winning* on supply (Wamsi/BofA, 2026-06-08; Michael Dell, 2026-04-07). **Bernstein initiated Outperform on 2025-09-15 at PT $175** ("Best In Class Operator and Clear Winner in the intelligence revolution"), calling Dell a structural share-gainer "very inexpensive relative to its growth profile," valuing it at **14x FY28/CY27 EPS of $12.59** (FY25A/FY26E/FY27E EPS $8.10/$9.57/$10.88) and ~17x FY27 FCF of $8.1B; PT was subsequently raised to **$500 post-Q1** (briefing 2026-05-29). **JPM (Samik Chatterjee) carries Dell Overweight** — "portfolio positioned for growth long-term through priority on infrastructure investments and leverage to AI compute" — but flags it is "working to navigate memory cost headwinds across its portfolio" (JPM Hardware & Networking, 2025-12-15). BofA (Wamsi Mohan) Buy **PT $500**, FY27E EPS ~$19 (briefing 2026-05-29). Brad Gerstner: "building the backbone of American AI" ($DELL +757% AI, $51B+ backlog).
  - **Pre-print BofA setup (Wamsi Mohan on the Fenske expert call, 2026-05-08):** ahead of the print, Mohan walked the AI-server guide higher in steps — Dell guided **$25B→$50B**, BofA raised to **$60B** post-Asia-trip channel checks (builds for Dell AI servers "super strong"), and flagged the SMCI legal overhang could push it to **$70–75B** as **~$10B of AI revenue floats from Super Micro to Dell**. His core rebuttal of the bear: **$25B of incremental AI revenue at ~5% EBIT margins "discredits the memory narrative"** as something Dell can't offset; layered on top of PC pull-forward + agentic industry-standard-server strength, fighting Dell into the print was "a losing battle." He also framed *why* Dell rallied: shorts who were long memory/optical "picked Dell" as the offsetting short ("at the losing end of the memory trade") and got caught offside (BofA/Wamsi Mohan via Fenske call, 2026-05-08).
  - **Agentic X86 refresh "just getting started" (650 Group networking call, 2026-06-04):** the 650 Group analyst tied the traditional-server surprise to an "OpenClaw moment" at GTC — agents hit the database 24/7 vs a human every ~5 min, so the previously-declining non-AI X86 market is now *growing*, in both cloud and enterprise. His read on Dell/HPE: **"this is just getting started — we barely have orders here,"** the enterprise demand inflected in **March** and takes time to convert to orders; this is **structural X86 refresh + incremental agentic demand**, not purely a cyclical pull-forward (650 Group, 2026-06-04).
  - **SIG (Mehdi Hosseini) — Positive, PT $700 (2026-07-08):** raising estimates on a higher mix of NeoCloud/Enterprise spend — new **FY28/FY29 EPS $24.23/$28.08** vs consensus $22.13/$25.70 (PT = **25x FY29 EPS**). ISG revenue CAGR **37% FY26–29**; DC segment rising to **>60% of ISG by FY29** (from ~40% in FY27) as Dell gains NeoCloud share; Enterprise troughs FY27 (-12% y/y) then returns to double-digit growth as inferencing broadens; **Vera (Arm) CPU an FY28 opportunity.** Supply-chain checks: Inventec/Foxconn guiding ~20% server-shipment growth CY26; industry shifting toward PCIe/MGX form factors vs rack-scale (SIG/Mehdi Hosseini, 2026-07-08).
- **Bear:** AI-optimized servers are **low-margin** — Bernstein estimates AI-server op margin **~5% or less vs low-teens for traditional** (Bernstein, 2025-09-15); ISG margin -110bp YoY (FY26 10-K); the +88% top line masks GM compression (corporate GM 20.0% FY26 vs 22.2% FY25). Morgan Stanley's Erik Woodring (2026-06-16) concedes "numbers for Dell are too low this year" but flags the **duration risk**: how much is pull-forward + pricing vs sustainable units — if order-unit growth flips neutral/negative, the market re-rates on peak-earnings fear even as EPS rises. He's playing the on-prem-compute theme via distributors/VARs rather than chasing the OEM. Bernstein's own sector caveat: enterprise-inferencing TAM ~$370B today is "potentially insufficient to sustain current levels of spend without a near-term digestion cycle," with historical precedent (Sun Microsystems dot-com) for violent OEM swings (Bernstein, 2025-09-15).
- **Where the Street stands:** Post-Q1 print, near-universal positive: Bernstein OP $500, BofA Buy $500, JPM (Samik Chatterjee) Overweight (hosted the 5/29 call), Barclays moved positioning from -2 (crowded short) to 0 on massive short-cover (briefing 2026-05-29). FinTwit euphoric (@patrickmoorhead, @altcap). MS the notable cautious/duration holdout.

## Catalysts / what to watch
- **Q2 FY27 print** (~late Aug 2026): guide implied Q2 ≈ Q1 AI-server level; watch order book + backlog build and any 2H supply unlock.
- **Veera Rubin ramp:** Dell expects to be first OEM to ship; backlog is shifting Blackwell→Rubin; next-5-quarter pipeline "almost exclusively" Rubin-weighted. Watch the NVIDIA L10-tray model shift (Rubin/VR200) — value/margin migration risk to NVIDIA, though Dell already outsources L7–L10 (Q425 Techknowledge).
- **Memory pricing** (DRAM/HBM/NAND): the binding 2H constraint and the key GM swing factor; cross-read SNDK/MU/SKHYNIX. JPM flags memory cost as the headwind to navigate (2025-12-15).
- **Traditional-server durability:** is the +92% agentic-inference demand structural or pull-forward (the MS duration question)? 650 Group's read is that it is structural ("OpenClaw" agentic X86 refresh, "just getting started," enterprise inflected March 2026) — a bull data point on the duration debate (650 Group, 2026-06-04).
- **SMCI share migration:** Super Micro's legal overhang could shift **~$10B of AI revenue to Dell**, a swing factor BofA cited in walking its FY27 AI-server number toward $70–75B (BofA/Wamsi Mohan via Fenske call, 2026-05-08) — watch how much actually lands.
- **18G server launch** and 14G installed-base refresh (~11–13:1 consolidation; >70% of base still on 14G or older per SAM deck).
- **AI-server market growth:** industry outlook ~30% CAGR 2025–2030 (650 Group, via JPM Hardware & Networking 2025-12-15) — the volume backdrop for Dell's ISG framework.
- **Server segment as the primary growth engine:** Barron's frames the whole print around the server line — AI-optimized servers +757% y/y to $16.1B is the headline, but Tech Trader's broader "server business" +181% y/y read (which nets in traditional servers) is the number generalist/retail flow is trading off (Barron's/Bary + Levine, 2026-06-22 / 2026-06-01).
- **PC-segment pricing / pull-forward dynamic:** Dell raised PC prices and gained premium-segment share in Q1 FY27, but Levine flags a demand **pull-forward** dynamic comparable to HP's — watch whether CSG unit growth normalizes or reverses once the pulled-forward demand is exhausted (Barron's/Levine, 2026-06-01).
- Capital returns cadence (dividend +20% Feb 2026; ongoing buyback; +10%/yr commitment through FY30 per SAM deck).

## Risks
- AI-server mix dilutes ISG/corporate gross margin (FY26 10-K); AI-server op margin ~5% or less (Bernstein, 2025-09-15).
- Memory + advanced-silicon scarcity; single-/limited-source suppliers (FY26 10-K Item 1A).
- AI-server revenue **non-linearity** — shipment timing vs orders drives quarterly variability (Q1 FY27 10-Q).
- Demand concentration / duration: heavy neocloud revenue mix; pull-forward + pricing risk (MS, 2026-06-16); sector digestion-cycle risk if inferencing TAM proves insufficient (Bernstein, 2025-09-15).
- Value-chain migration: NVIDIA finished-L10-tray model could shift margin upstream (Q425 Techknowledge).
- Key-person dependence on Michael Dell / Jeff Clarke (FY26 10-K).
- Tariff / export-control / sanctions exposure; China (FY26 10-K).
- Dividend/buyback discretionary; meaningful cash flow to debt service (FY26 10-K).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **UBS (Dave Vogt) Dell callback post-print (UBS "Dell callback", 2026-05-29):** UBS's read on the widest beat in Dell's history. Total revenue **$43.8B, ~$8.5B / 24% above UBS estimate**. AI server $16.1B (vs $13B est., ~24% upside) seen as **least controversial / sandbagged — not the stock driver**. The surprise was **core/traditional server +92% y/y with absolute UNIT growth, not just price** (mgmt "let slip" on the public call) — traditional servers taking on AI workloads at advanced enterprise/large-tech customers. On the AI order book: **a large/increasing share of orders is now Vera Rubin** (migrating up the NVIDIA roadmap), with **tremendous demand for the GB/Grace variants** (neoclouds taking Grace-GPU products). Backlog **$51B** exiting the quarter (from $43B), $24.4B orders booked; pipeline "multiple times backlog" (>$100B) but mgmt pushed back on building a linear order→rev-rec waterfall (lumpy). FY27 AI-server guide **$50B→$60B** (buy-side was higher); 2H step-down framed as **supply not demand; memory = #1 constraint**. CSG: 17% rev growth + **8% op margin (280 bps above UBS's 5.2%) is NOT sustainable** — normalizes to 5–6% (~$0.50 of the EPS beat was PC margin). UBS stays **Neutral on valuation** — Dell now trades near a market multiple / premium to NVDA/Broadcom on a declining-gross-margin business; flags a tough fiscal-28 first-half PC comp (UBS "Dell callback", 2026-05-29). Read-across: HPE may not follow Dell's traditional-server demand/margin strength; TD Synnex's high (general-purpose compute/networking) business a positive read.
- **MS (Erik Woodring) servers note** _(2026-06-15/16)_ + **Dell CFO/ISG @ JPM post-print** _(2026-05-29)_: bull = $53B AI backlog / $60B FY27 guide; **MS bear** = thin AI-server margins (ISG 11.7% vs 12.8%) + traditional-server pull-forward.
- **Mizuho (Vijay Rakesh) — memory/agentic-AI note** _(header dated 2026-05-27; manifest 2026-06-03)_: reiterates **Outperform, raises PT to $350 (from $300)**, ~23x F28E EPS — sees Dell benefiting from Agentic AI server ramps, **Vera-only CPU racks potentially made by Dell**, an expanding AI-server backlog and continued storage ramps. Nudges ests: F27E rev/EPS $143.9B/$13.19 (cons. $142.3B/$13.10), F28E $159.1B/$15.35 (cons. $157.9B/$15.18). Frames Dell as a key enabler of the "AgenticAI revolution" alongside memory names (Mizuho "HBM4e Ramping/Agentic AI", 2026-05-27).
- **Mizuho (Vijay Rakesh) — DC-capex industry note** _(2026-07-11)_: in "DC Capex Ramping to >$1.4T in 2028E; FCF Outlook Improving," Mizuho names **DELL (with SMCI) as a system-integrator (SI) beneficiary** of accelerating AI data-center capex ($1.2T 2027E / >$1.4T 2028E; ~$50B/GW × 106GW 2026-30E ≈ >$5.3T). A demand read-through only; no change to Mizuho's DELL rating/PT (Outperform, $350, from the 05-27 note). [../relat%C3%B3rios%20bons/DC_Capex_Ramping_to__14T_in_2028E_FCF_Outlook_Improving.html](../relat%C3%B3rios%20bons/DC_Capex_Ramping_to__14T_in_2028E_FCF_Outlook_Improving.html)
- **Nomura (Asia AI Semi & Server, 2026-06-30)** — **IREN is now a sizeable Dell AI-server customer:** IREN bought **$5.8bn** of GPUs + ancillary equipment from Dell alongside its Nov-25 Microsoft deal, added **$3.5bn** more (Mar-26), then **$1.6bn** additional (May-26) to service its $3.4bn NVIDIA cloud contract — real neocloud hardware orders flowing through Dell (Nomura, 2026-06-30).

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY27 · May 28 → Jun 22, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1 FY27) | Intra-quarter flow | Signal |
|---|---|---|---|
| **AI-server demand** | $16.1B (+757% y/y); orders $24.4B, backlog $53.1B, >$100B cumulative, FY27 guide $50B→$60B | UBS: AI-server $16.1B "least controversial / sandbagged" · JPM OW corroborates backlog $53.1B / 5,000+ AI-factory customers | **✓ confirms** (and still sandbagged) |
| **Traditional server** | $8.5B (+92%); FY27 guide >60% | UBS: the real surprise — +92% y/y with UNIT growth, not just price, on agentic workloads | **✓ confirms** (units, not just price) |
| **Margin / mix** | Op margin +330bp; AI mix still dilutive | UBS: CSG 8% op margin "NOT sustainable" (normalizes 5-6%) · MS: thin AI-server margin (ISG 11.7% vs 12.8%) | **⚠ nuance** (margin is the soft spot) |
| **Memory / supply** | Memory = constraint #1 in 2H; the step-down is supply, not demand | BofA: Dell raising prices to defend GM on memory inflation and *winning* on supply | **✓ confirms** (supply is the bottleneck) |
| **Guidance / durability** | FY27 guide rev ~$168B, EPS $17.9 | MS: "numbers too low this year" but flags duration risk — if units turn flat/negative, re-rate on peak-earnings | **⚠ nuance** (peak-earnings debated) |
| **PC / CSG durability** | CSG commercial $13.0B / consumer $1.6B; Dell expects to beat a ~-18% 2H PC market and take share | Barron's/Levine: PC prices up + premium-share gains, but flags a demand "pull-forward" comparable to HP's | **⚠ nuance** (echoes the MS duration concern, now on CSG) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-29 | UBS · Dave Vogt (callback) | demand | mixed | UBS (post-print callback): total revenue $43.8B, ~$8.5B / 24% above UBS's estimate. AI server $16.1B seen as "least controversial / sandbagged". The surprise was core/traditional server +92% y/y with UNIT growth, not just price. A large/growing share of orders is now Vera Rubin; backlog $51B exiting the quarter. CSG at 8% op margin "NOT sustainable" (normalizes to 5-6%). UBS stays Neutral on valuation — Dell trades near a market multiple / premium to NVDA/Broadcom on a business with declining gross margin. |
| 05-29 | Bernstein | valuation | bull | Bernstein: PT raised to $500 post-Q1 (from $175 at the Outperform initiation on 2025-09-15). |
| 05-29 | BofA · Wamsi Mohan | valuation | bull | BofA (Wamsi Mohan): Buy, PT $500, FY27E EPS ~$19. |
| 05-29 | JPM · Samik Chatterjee | demand | bull | JPM hosted a call with CFO David Kennedy + ISG pres. Arthur Lewis post-earnings: AI-server orders $24.4B, backlog $53.1B, >$100B in cumulative orders, 5,000+ AI-factory customers. Dell expects to beat a 2H PC market of ~-18% and gain share. JPM Overweight. |
| 06-01 | Barron's · Adam Levine (Tech Trader) | demand | mixed | Q1 FY27 read for a generalist audience: server business "sales up 181% from last year" (broader server line); "strong showing from the PC segment" on raised PC prices and premium-segment share gains; flags a PC-demand "pull-forward," comparable to HP's. |
| 06-08 | BofA · Wamsi Mohan | margin | bull | BofA conference wrap: Dell raising prices to defend GM amid memory inflation and *winning* on supply. |
| 06-04 | 650 Group (networking call) | demand | bull | 650 Group ties Dell/HPE's traditional-server strength to an "OpenClaw moment" at GTC — agents hammer the database 24/7 vs a human every ~5 min, so the formerly-declining non-AI X86 market is now growing in cloud AND enterprise. On Dell/HPE: "this is just getting started — we barely have orders here," enterprise demand inflected in March; structural X86 refresh + incremental agentic demand, not just pull-forward. |
| 06-15 | Morgan Stanley · Erik Woodring | valuation | mixed | MS (Woodring) servers note: bull = $53B AI backlog / $60B FY27 guide; MS bear = thin AI-server margins (ISG 11.7% vs 12.8%) + traditional-server pull-forward. Concedes "numbers for Dell are too low this year" but flags duration risk — if order unit growth turns neutral/negative, the market re-rates on peak-earnings fear. Prefers to play the on-prem-compute theme via distributors/VARs. |
| 06-22 | Barron's · Andrew Bary ("Top CEOs of 2026") | demand | bull | Michael Dell profile: AI-optimized servers "generated revenue of $16.1 billion in the first quarter, a 757% increase from the prior year"; total revenue "$43.8 billion, a record and an increase of 88%"; shares "up more than 250% in the past 12 months" — the AI-server inflection now crossing into generalist/retail coverage. |
| 07-08 | SIG · Mehdi Hosseini | demand | bull | SIG Positive, PT $700 (25x FY29 EPS): raising estimates on a higher mix of NeoCloud/Enterprise spend. New FY28/FY29 EPS $24.23/$28.08 vs consensus $22.13/$25.70. ISG revenue CAGR 37% FY26-29; DC segment rising to >60% of ISG by FY29 (from ~40% FY27) on NeoCloud share gains; Enterprise troughs FY27 (-12% y/y) then returns to double-digit growth as inferencing broadens; Vera (Arm) CPU an FY28 opportunity. Checks: Inventec/Foxconn guiding ~20% server-shipment growth CY26; industry shift toward PCIe/MGX form factors vs rack-scale. |
| 07-11 | Mizuho · Vijay Rakesh (DC Capex Ramping to >$1.4T in 2028E) | demand | bull | Names **DELL (with SMCI) as a system-integrator (SI) beneficiary** of accelerating AI DC capex ($1.2T 2027E / >$1.4T 2028E; ~$50B/GW × 106GW 2026-30E ≈ >$5.3T). Read-through only; no change to Mizuho's DELL Outperform / $350 PT (05-27). (Mizuho · Vijay Rakesh, 2026-07-11) |

**Quarter synthesis:** after Dell's largest beat ever, the sell-side stopped debating demand (consensus: AI-server sandbagged, traditional server +92% in units) and moved to the *quality and durability* of the margin — CSG unsustainable (UBS), thin AI margin (MS) and the fear of peak-earnings if unit growth turns; valuation (near a market multiple) is what holds back the Neutrals. Barron's generalist coverage (06-01, 06-22) corroborates both halves of the debate from the outside: the AI-server headline number is being repeated almost verbatim in mainstream press (bull, sandbagged-demand thesis broadening its audience), while Levine's PC-segment "pull-forward" language independently echoes the MS/Woodring duration concern — this time applied to CSG rather than ISG.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2 FY26 (2025-08-01) | Q3 FY26 (2025-10-31) | Q4/FY26 (FY end 2026-01-30) | Q1 FY27 (2026-05-01) |
|---|---|---|---|---|
| Total revenue | $29.8B, +19% YoY | $27.0B, +11% YoY | FY26 $113.5B, +19% | $43.8B, +88% YoY (widest beat ever) |
| AI-optimized servers | Not split (S&N $12.9B, +69%) | Not split (S&N $10.1B, +37%) | FY26 $24.7B, +166% | $16.1B, +757% YoY |
| Traditional servers & networking | Not split (in S&N line) | Not split (in S&N line) | FY26 $19.5B, +9% | $8.5B, +92%; FY27 guide >60% |
| Storage | $3.9B, -3% | $4.0B, ~flat | FY26 $16.6B, +1% | $4.3B, +8%; FY27 guide ~mid-single-digit |
| Margin / AI-mix dilution | — | — | GM 20.0% (-220bp); ISG margin 11.7% vs 12.8% | Op margin +330bp; AI mix still dilutive |
| Memory / supply & pricing | — | — | Raising prices vs 30-100% component inflation | Memory = #1 2H constraint; step-down is supply not demand |

_Source: DELL earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** FY26 10-K [`../DELL/DELL_10-K_2026-03-16_0001571996-26-000008.html`](../DELL/DELL_10-K_2026-03-16_0001571996-26-000008.html); Q1 FY27 10-Q [`../DELL/DELL_10-Q_2026-06-09_0001571996-26-000030.html`](../DELL/DELL_10-Q_2026-06-09_0001571996-26-000030.html).
- **Transcripts:** [Q1 FY27](../DELL/transcripts/DELL_Q1-FY27-earnings_2026-05-28.md) · [Q4 FY26](../DELL/transcripts/DELL_Q4-FY26-earnings_2026-02-26.md) · [Q3 FY26](../DELL/transcripts/DELL_Q3-FY26-earnings_2025-11-25.md) · [Q2 FY26](../DELL/transcripts/DELL_Q2-FY26-earnings_2025-08-28.md).
- **Equity calls:** Michael Dell JPM fireside (2026-04-07); Dell CFO + ISG pres. @ JPM post-earnings (2026-05-29); BofA conference wrap — Wamsi Mohan on DELL/HPE (2026-06-08); Erik Woodring / MS on servers (2026-06-16). See `E:/equity_calls_transcripts/Overall/`.
  - [Fenske cyber-software call — Wamsi Mohan pre-print on DELL (2026-05-08)](../_equity_calls/Overall/2026-05-08_Fenske_cyber-software.md) — AI-server walk $25B→$50B→$60B→$70-75B w/ ~$10B SMCI migration; $25B incremental at ~5% EBIT "discredits memory narrative"; shorts caught offside.
  - [650 Group networking call (2026-06-04)](../_equity_calls/Semis/2026-06-04_650Group_networking.md) — "OpenClaw" agentic X86 refresh structural, "just getting started," Dell/HPE "barely have orders," enterprise inflected March 2026.
- **Research reports (relatórios bons):**
  - [Bernstein initiation on AAPL, STX, DELL, SNDK](../relat%C3%B3rios%20bons/Bernstein_initiation_on_AAPL_STX_DELL_SNDK.html)
  - [Dell 2025 Securities Analyst Meeting Presentation](../relat%C3%B3rios%20bons/2025_Securities_Analyst_Meeting_Presentation.html)
  - [JPM Hardware & Networking (2025-12-15)](../relat%C3%B3rios%20bons/JPM_Hardware___Networkin_2025-12-15_5155719.html)
  - [Primer DC overall — BofA](../relat%C3%B3rios%20bons/Primer_DC_overall_BofA.html)
  - [Q425 Techknowledge tech takeaways](../relat%C3%B3rios%20bons/Q425_Techknowledge_tech_takeaways.html)
  - [UBS — Dell callback post-print (2026-05-29)](../relat%C3%B3rios%20bons/2026_05_29_dell_ubs_call_back_29_may_26.html) — traditional server +92% w/ unit growth; Vera Rubin large share of orders; FY27 AI $50→$60B; CSG 8% margin unsustainable; Neutral on valuation.
  - [Barron's, June 1 2026 issue — Tech Trader (Adam Levine)](../relat%C3%B3rios%20bons/Barrons_0106.html) — server sales +181% y/y; PC-segment price/share gains; flags a PC demand "pull-forward" comparable to HP's.
  - [Barron's, June 22 2026 issue — "Top CEOs of 2026" (Andrew Bary)](../relat%C3%B3rios%20bons/Barrons_22_June_2026.html) — Michael Dell profile: AI-server revenue $16.1B (+757% y/y); total revenue $43.8B (+88%, record); shares +250%+ over 12 months.
- **Briefings:** `E:/briefings/2026/2026-05-29-company-specific.md`, `2026-05-30-company-specific.md` (Q1 FY27 print recaps + sell-side PTs).
- **Outlook:** not reachable in this environment (no MAPI session); email to be added separately.

## Changelog
- **2026-07-13:** Added **Mizuho (Vijay Rakesh) "DC Capex Ramping to >$1.4T in 2028E; FCF Outlook Improving" (2026-07-11)** — additive read-through only. The note lists **DELL (with SMCI) as a system-integrator (SI) beneficiary** of accelerating AI DC capex ($1.2T 2027E / >$1.4T 2028E; ~$50B/GW × 106GW 2026-30E); no change to Mizuho's DELL Outperform / $350 PT (05-27). Added a brief line under "In the inbox," an intra-quarter full-log row (07-11, demand/bull) and an inline Sources link. No figure superseded.
- **2026-06-30:** Added Barron's generalist coverage of the Q1 FY27 print — "Top CEOs of 2026" Michael Dell profile (2026-06-22, AI-server $16.1B/+757%, total rev $43.8B/+88%, shares +250%+) and Tech Trader (2026-06-01, server sales +181%, PC pricing/share gains + pull-forward flag vs HP). Added to Current state, Catalysts (server as primary growth engine; PC pricing/pull-forward), Intra-quarter full log (06-01, 06-22) and Signal-vs-management (new PC/CSG durability row), extended the intra-quarter window to Jun 22, and added both Sources links.
- **2026-06-26:** Read two previously-unlinked equity calls — Fenske cyber-software call (2026-05-08, Wamsi Mohan/BofA pre-print on DELL) and 650 Group networking call (2026-06-04). Added: BofA's pre-print AI-server walk ($25B→$50B→$60B→$70-75B) with **~$10B SMCI revenue migration** and the "$25B incremental at ~5% EBIT discredits the memory narrative" rebuttal + "shorts caught offside" rally explanation (bull para + Catalysts); 650 Group's "OpenClaw" structural-agentic-X86-refresh / "just getting started, barely have orders" framing as a duration-debate bull point (bull para + intra-quarter log + Catalysts). Linked both calls under Sources.
