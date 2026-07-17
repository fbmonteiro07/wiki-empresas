# CRDO — Credo Technology Group Holding Ltd

_Wiki · generated 2026-06-19 · sources: `E:\Wiki Felipe\CRDO` (filings + transcripts) · `_briefings\2026\*` (heavily covered, ~42 hits). Master index: [00_INDEX.md](00_INDEX.md). Themes: [optical-cpo](themes/optical-cpo.md) · [custom-asic-tpu](themes/custom-asic-tpu.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $2.1bn | $3.5bn |
| Gross profit | $1.4bn | $2.3bn |
| Gross margin | 67.0% | 66.6% |
| EBITDA | $1.1bn | $1.9bn |
| EPS | $5.03 | $8.64 |
| Capex | $333m | $148m |
| OCF (≈EBITDA) | $1.1bn | $1.9bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Fabless connectivity-IC supplier built to "transform connectivity at scale through fast, reliable and energy-efficient system solutions" for AI data centers (FY26 10-K, 2026-06-15). Sells high-speed copper and optical interconnect up to 1.6T: **ZeroFlap (ZF) Active Electrical Cables (AECs)**, ZF optical transceivers, **optical and PCIe retimers/DSPs**, **SerDes chiplets**, OmniConnect memory solutions, and SerDes-IP licensing — all on its own SerDes/DSP technology with an "n-1" (legacy-node) cost advantage. Optimized for Ethernet/PCIe and emerging **UALink, ESUN, SUE** scale-up fabrics across Front-End, Scale-Out, Scale-Up and Scale-In networks. **FY26 (ended ~Apr 2026) revenue $1.3B, +206% y/y** (vs $436.8M FY25), non-GAAP GM 68.1%, non-GAAP NI $662M (FY26 10-K; Q4 call 2026-06-01). The story is a **copper-to-optical-plus-AEC AI connectivity ramp** with extreme customer concentration: top-10 = ~90% of FY26 revenue, two customers >10% (Customer A 49%, Customer B 32% per 10-K) — Amazon is a confirmed customer (holds a Credo warrant) and Microsoft is named in the filing.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) ZeroFlap Active Electrical Cables (active copper) · 2) SerDes/DSP retimers (Ethernet/PCIe) · 3) Optical DSPs + ZeroFlap optics |
| **Main buyer(s)** | Hyperscalers — Amazon (Cust. A ~49%) & Microsoft (Cust. B ~32%) + 5th hyperscaler & Neocloud/Tier-2 tail; top-10 = ~90% of FY26 rev |
| **Key suppliers** | TSMC foundry (n-1 node); OSAT Amkor/ASE (package), KYEC/Sigurd (test); BizLink (AEC manufacturing); IP/EDA (Comira, Dust Photonics) |

## Position in the value chain
Credo is a fabless designer between the foundry/IP supply base and the hyperscalers. It owns no fabs — TSMC produces the wafers, third parties package/assemble/test — and it sells AEC active-copper cables, SerDes/DSP retimers, optical DSPs and chiplet connectivity to the large hyperscalers (Amazon, Microsoft) plus a fifth hyperscaler and a growing Neocloud/Tier-2 tail. Its differentiated position is **active copper (AECs) for short-reach scale-up plus optical for longer reach** — straddling the copper-vs-optical debate rather than betting purely on one (themes [optical-cpo](themes/optical-cpo.md), [custom-asic-tpu](themes/custom-asic-tpu.md)).

**AEC incumbency and market structure.** Credo invented the AEC category in 2018 and still holds **~80% AEC market share** despite later entry by Marvell, Broadcom and especially **Astera Labs**, which has gained notable recent traction (JPM Credo, 2025-10-17; JPM H&N, 2025-12-15). The moat is **vertical integration from silicon to finished, qualified cable** — peers ship only silicon or module — giving time-to-market, cost and reliability edges; JPM expects Credo to keep overall leadership with rivals as second/third sources. AEC reach ~7m at ~10W up to 1.6T, bridging passive DAC (1–2m) and optics (150m+, 15–20W). On SIG's price tracking (SIG Optical-SIGnals, 2025-10-09), at 800G AECs run ~40% cheaper than AOCs — "highly compelling for shorter distances (NIC-to-ToR) at higher bandwidth" — though at 400G AOCs undercut AECs (a modest negative on LPO share staying flat at ~6%). **TAM framing (JPM Credo, 2025-10-17):** AECs ~$4bn by 2028 (units +60% CAGR, <1mn in 2022 → 10mn+ in 2028, ASPs trending low- to mid-hundreds as form factors move from "straight" 100G to Y/X 800G); optical DSP ~$6bn; PCIe retimer ~$2bn — aggregate interconnect TAM **$12bn+ at +45% CAGR** (reframed to $10bn+ in JPM H&N, 2025-12-15). AEC attach rate is **~1.5:1 per XPU today** (front- plus back-end, ex scale-up); management argues scale-up alone could be **up to 10x the scale-out volume** (JPM Credo, 2025-10-17).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <rect x="0" y="0" width="720" height="220" fill="#ffffff"/>
  <!-- Suppliers -->
  <rect x="10" y="40" width="180" height="140" rx="8" fill="#eef3fb" stroke="#3b5bA9" stroke-width="1.5"/>
  <text x="100" y="62" text-anchor="middle" font-weight="bold" fill="#1f3a6e">Suppliers</text>
  <text x="100" y="90" text-anchor="middle">TSMC foundry (wafers,</text>
  <text x="100" y="106" text-anchor="middle">n-1 legacy node)</text>
  <text x="100" y="130" text-anchor="middle">OSAT package/assembly/</text>
  <text x="100" y="146" text-anchor="middle">test; IP / EDA</text>
  <text x="100" y="168" text-anchor="middle">(Comira, Dust Photonics)</text>
  <!-- Credo -->
  <rect x="262" y="28" width="206" height="164" rx="8" fill="#fdeee6" stroke="#c0622a" stroke-width="2"/>
  <text x="365" y="50" text-anchor="middle" font-weight="bold" fill="#9c3d12">CRDO (fabless)</text>
  <text x="365" y="76" text-anchor="middle">AEC active copper (ZeroFlap)</text>
  <text x="365" y="98" text-anchor="middle">SerDes / DSP retimers</text>
  <text x="365" y="116" text-anchor="middle">(Ethernet/PCIe, 32G-200G)</text>
  <text x="365" y="138" text-anchor="middle">Optical DSP + ZF optics</text>
  <text x="365" y="160" text-anchor="middle">SerDes chiplets,</text>
  <text x="365" y="176" text-anchor="middle">OmniConnect, IP licensing</text>
  <!-- Customers -->
  <rect x="540" y="40" width="170" height="140" rx="8" fill="#eaf6ee" stroke="#2f8f4e" stroke-width="1.5"/>
  <text x="625" y="62" text-anchor="middle" font-weight="bold" fill="#1d6b38">Customers</text>
  <text x="625" y="90" text-anchor="middle">Hyperscalers:</text>
  <text x="625" y="110" text-anchor="middle">Amazon (Cust. A ~49%)</text>
  <text x="625" y="128" text-anchor="middle">Microsoft (Cust. B ~32%)</text>
  <text x="625" y="148" text-anchor="middle">+ 5th hyperscaler;</text>
  <text x="625" y="168" text-anchor="middle">Neoclouds / Tier-2 tail</text>
  <!-- Arrows -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#555"/>
    </marker>
  </defs>
  <line x1="192" y1="110" x2="258" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="470" y1="110" x2="536" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="360" y="210" text-anchor="middle" font-style="italic" fill="#444">Copper (AEC) + optical scale-up interconnect — top-10 = ~90% of revenue; two customers >10%</text>
</svg>

## Current state (latest quarter)
**Q4 FY26 (reported 2026-06-01 AMC; quarter ended ~April 2026), capping FY26:**
- **Q4 revenue $437M**, +7% q/q, **+157% y/y** — only ~$5M above ~$432M Street (thin top-line beat). Non-GAAP GM **68.3%** vs ~64.9% cons (big margin beat); non-GAAP NI $226.7M; **operating margin 49.6%**; FCF $177.5M; cash $1.4B (Q4 call 2026-06-01; briefing 2026-06-02).
- **Non-GAAP EPS $1.16 vs ~$1.02 cons (+14%, entirely margin-driven)** — Vital Knowledge: "157% y/y growth, only ~$5M above Street... top-line upside isn't enough" near-term (2026-06-01).
- **FY26 full year: revenue $1.3B (+206% y/y), non-GAAP NI $662M (>5x), non-GAAP GM 68.1%, EPS $3.46 (+392%)** (Q4 call).
- **Customer concentration: four customers ≥10% of Q4 (34% / 27% / 16% / 10%)** — broadening from three; Neoclouds/Tier-2 guided to ~20% of revenue over coming years.
- **Guidance — Q1 FY27:** $465–$475M, GM 67–69%, opex $86–$90M. **FY27: revenue >80% y/y (raised from >50% at the Q3 call), GM ~flat, opex +~50%, net margin ~50%.**
- **Optical raised to >$600M FY27** (from >$500M): optical DSPs + SiPho PICs (Dust Photonics) + ZeroFlap optics, each >$100M and each +80%+ y/y; FY28 optical floor ~$1.2B. **Dust Photonics funded with ~$750M net cash in Q1.** Supply chain "significant tightness"; 200G/lane ramp light in FY27, inflection 2H.
- **Stock reaction: -11.5% to -15% on the print** despite the beat-and-raise (briefings 2026-06-01/02) — buyside bars missed on revenue; "frontier model operator slowing deployments" per JPM 3P checks.

## Debate / thesis
- **Bull:**
  - **Optical is the second leg and it's inflecting.** Jefferies (Blayne Curtis) Buy, **PT $225 → $270** (2026-06-01): "AEC far from over, but **Optics is the real driver**"; FY27 optical >$600M, ~doubles in F28; **upside case $13 EPS C28, PT $390.** Barclays (O'Malley) OW $260: optical DSPs the biggest upside surprise, **FY28 optical ~$1.6B** (2026-06-01).
  - **AEC is the durable first leg, not a fad.** JPM (Cardoso) modeled a **revenue CAGR of 50%+ FY25–28E and earnings CAGR of 70%+** at initiation (JPM Credo, 2025-10-17), driven by AEC unit/ASP growth plus optical DSP and PCIe optionality — ahead of the industry's +40% AEC-unit forecast on new use cases (rack-to-rack, intra-switch DDC, scale-up PCIe) and broadening adoption (Amazon, Microsoft, xAI ramping; Meta, possibly Oracle/Google engaging — four "material" adopters in 2026 vs one in 2023). JPM H&N (2025-12-15) reiterates OW: AEC NIC-to-ToR units +30%+ CAGR through the decade, revenue closer to +40% on pricing, "underestimates the opportunity" ex scale-up.
  - **GM structurally superior** — non-GAAP GM ~68% with operating margin ~50% and net margin guided ~50% FY27, rare for a connectivity-IC name; "GM outstripping expectations" (GS Schneider, Buy, 2026-06-01). (JPM had modeled GM tracking the high end of the 63–65% LT range at initiation; actuals have run above it.)
  - **Straddles copper and optical** — @crux_capital_ (2026-06-19) puts CRDO in the **"stronger" connectivity bucket (copper+optics)** alongside SMTC/ALAB/MTSI/MXL/MRVL, vs the "weaker" pure-play optics (LITE/AAOI/FN/CIEN) exposed to China oversupply. Customer diversification underway (3→4 >10% customers; Neoclouds to ~20%). CRDO at **12-month relative highs** per Rothschild (2026-06-19).
  - **CPO is greenfield, not a Credo killer.** TD Cowen (Buy, **CRDO a Top Pick**, ref $112.33, 2026-03-11): CRDO "de-rated over the past six months over fears of displacement due to co-packaged optics" — TD Cowen "strongly pushes back." It sees scale-up CPO as a >$9bn greenfield for Lumentum/Coherent, "in sharp contrast to the worst case contemplated by Credo bears," and notes optics in scale-up does **not** preclude copper (TPUs have used both since v4). The connectivity-IP foundation (low-power, high-perf SerDes) is "as relevant as ever"; with AECs, **Active LED Cables (ALCs)**, ZeroFlap optics and OmniConnect, Credo will soon address "effectively every connection in the datacenter."
  - **UBS hosts Credo on an Asia NDR (Randy Abrams, 2026-07-09, Not Rated):** Credo grew **>200% YoY to ~US$1.3bn in FY26** and guides **FY27 >80% YoY**; optics inflects in H2 FY27 to **>US$600mn in FY27** (optical DSPs for CSPs, silicon-photonics PICs, zero-flap transceivers — each >US$100mn). AECs have multi-year growth — **5 of 6 major customers now >$100mn, only 1 fully penetrated; NeoCloud now ~20% of sales**; copper reach 100G/7m, 200G/6m, 400G/3-5m. New **Omni Connect (OmniConnect)** inference solution connects up to **2TB LPDDR to a GPU** at ~US$2.5-3k content/GPU (>$1bn potential). UBS models hyperscaler capex **+81%/+21% YoY in 2026/27** (UBS/Randy Abrams Asia NDR, 2026-07-09).
- **Bear:**
  - **Revenue, not margin, drives the stock — and the top line is only OK.** JPM desk (Joshua Meyers, 2026-06-01): "-11.5%... rev and guide both **missed buyside bars**; frontier model operator slowing deployments; **show-me territory for a while**"; ~$200 = 22.2x F28E $9 (buyside range $8–10). BEP: "the market repriced the **quality** of the beat — who the revenue comes from, and when the next leg arrives."
  - **AEC share loss is the structural bear.** JPM H&N (2025-12-15) bear case: ~80% share is "unsustainable" as large hyperscalers dual/multi-source; pricing pressure plus new-product ramps could **moderate gross margins** off the recent above-range highs; premium valuation "sets a high bar." JPM initiation flagged the same risk — peers (Marvell/Broadcom/Astera) gaining as second sources (JPM Credo, 2025-10-17).
  - **Copper-vs-optical narrative risk.** @Midnight_Captl (repeated May 12–13): "Jensen is telegraphing photonics — Lumentum, Coherent, Corning. **Not Credo. Not copper.**" Jefferies' Jeff Pu flagged "**AEC headwinds**... long-term physical limits beyond 3.2T... likely valued at a discount" (2026-05-11) — _though Pu reversed to a **new Buy** on 2026-06-29 on the [SPCX](SPCX.md) neocloud demand read-through._ The CPO/optical rotation periodically prices AECs as the lower-growth leg.
  - **Warrant economics flatter the optics on customer "wins."** Per SemiAnalysis (AWS Trainium3 Deep Dive, ~2025-12-04), AWS's AEC deal carries a **Credo stock rebate structured like the Astera/AWS warrant deal but far larger** — after Credo's share run, the warrant value Amazon received exceeded the spend needed to vest it, i.e. "**Credo effectively paid Amazon to take AECs.**" On Trainium3, AECs are used as 400G Y-cables (with gearbox, 56G→112G SerDes) NIC-to-ToR. The takeaway: anchor-customer revenue is real but the effective economics/concentration risk are richer than headline reach.
  - **Extreme customer concentration** — top-10 ~90%, Customer A 49% / Customer B 32% of FY26 (10-K); JPM est. FY25 Amazon ~63%, Microsoft just under 10%. A single hyperscaler deployment slip (the "frontier model operator" comment) moves the whole print.
- **Where the sell-side stands (post-Q4):** **Unanimous bulls** — **Mizuho Outperform $290** (new Street high; Vijay Rakesh, 2026-07-11) · GS Buy · **Jefferies Buy $270** · **Barclays OW $260** · **JPM (Cardoso) OW $250** · **TD Cowen Buy (Top Pick)** · SIG Positive (briefing 2026-06-02). JPM initiated OW on 2025-10-17 at a **Dec-26 PT of $165** (~48x CY27 EPS; superseded by the $250 in the post-Q4 table). Consensus: FY27 optical is real, AEC durable, margins superior; near-term **"show-me" mode** until revenue re-accelerates in 2H FY27.
  - **Mizuho reiterates Outperform, PT $290 — CRDO a "critical supplier" to the DC-capex ramp (Mizuho "DC Capex Ramping to >$1.4T in 2028E; FCF Outlook Improving", Vijay Rakesh, 2026-07-11):** Mizuho names CRDO among the "critical suppliers" (with LITE) to accelerating AI DC capex ($1.2T 2027E / >$1.4T 2028E, ~$50B/GW, 106GW 2026-30E). PT **$290 (~19x F28E P/S)** on CRDO's SerDes-IP-led lower-TCO edge (AEC + Optical DSP + ALC + ZeroFlap optics + OmniConnect), with the LT TAM framed at **~$10B (up >3x vs the mid-2024 ~$3B)**; GM ~65% (at-to-above the LT 63-65% range). Engaged with all seven major hyperscalers. (Mizuho / Vijay Rakesh, 2026-07-11; price ref $257.79)
  - **MS (NC) — AEC leadership today, optics the second growth engine (MS "Bringing More Light to Scale-Up Networks — Updated Scale-Up Primer", Meta Marshall / Joseph Moore, 2026-07-13):** in MS's updated scale-up primer (scale-up TAM 4x'd to **~$70bn by 2030**), CRDO (Not Covered) is "one of the cleanest exposures to **copper durability** through its **ZeroFlap AEC franchise**"; the current base is primarily scale-out, but **Blue Heron gives direct scale-up optionality across UALink, ESUN and Ethernet**, and the optical expansion (**DustPhotonics acq, ZeroFlap optical transceivers, new optical-DSP portfolio**) broadens exposure across **800G / 1.6T / 3.2T** and hedges the eventual copper-to-optics transition. MS cites mgmt's **>80% FY2027 revenue growth** and **>$600M from optical products** — optics "a meaningful second growth engine rather than simply a defensive hedge"; the watch item is **execution across several new product categories** while sustaining the core AEC business. (MS "Updated Scale-Up Primer", 2026-07-13)

## Catalysts / what to watch
- **Q1 FY27 print: ~early September 2026** — first read on the $465–475M guide, optical >$600M trajectory, and whether the "frontier model operator" deployment slowdown reverses.
- **Optical ramp pace:** ZeroFlap optics (TensorWave shipping; three more in qual), optical DSP to 1.6T, Dust Photonics SiPho PIC integration — the three >$100M legs.
- **AEC roadmap:** PCIe Gen 6 AECs to mass production 1H FY27; 200G/lane (light FY27, inflect 2H); fifth hyperscaler + Neocloud/Tier-2 mix toward ~20%.
- **FY28 step-ups:** ALCs (Active LED Cables) and Weaver/OmniConnect gearbox ramping FY28; FY28 optical floor ~$1.2B (mgmt) to ~$1.6B (Barclays). TD Cowen (2026-03-11): ALCs — validated by the **Hyperlume (microLED) acquisition** — sample F2027, production ramp F2028, positioned as a lower-risk/lower-power path to near-packaged optics (NPO) vs laser-based CPO.
- **OmniConnect adoption:** VSR SerDes (~10in) + protocol-agnostic gearbox could shift accelerator I/O off CoWoS/HBM toward a modular design (UALink/SUE-T scale-up, microLED NPO). TD Cowen (2026-03-11): "briefs well" but adoption "far from a foregone conclusion" — VSR SerDes must be designed into the ASIC itself; early engagements only, hard to size.
- **Scale-up standards:** UALink / ESUN / SUE adoption (Blue Heron 200G retimer) vs NVLink/Ethernet — determines copper-vs-optical content mix.

## Risks
- **Customer concentration** — top-10 ~90% of FY26; two customers >10% (Customer A 49%, B 32%); JPM est. FY25 Amazon ~63%. Any hyperscaler design-loss or deployment slip is material (FY26 10-K; JPM "frontier model operator slowing deployments," 2026-06-01). Warrant-rebate economics with AWS mean anchor-customer revenue carries embedded give-back (SemiAnalysis, AWS Trainium3, 2025-12).
- **AEC share erosion** — ~80% share unlikely to hold as hyperscalers multi-source to Astera/Marvell/Broadcom; pricing/competition could moderate the above-range gross margins (JPM H&N, 2025-12-15).
- **Copper displacement / optical rotation** — AEC growth questioned at >3.2T physical limits; CPO/photonics narrative periodically prices copper as the loser ("Not Credo. Not copper."). TD Cowen counters CPO is scale-up greenfield and does not preclude copper (2026-03-11).
- **Foundry/supply dependence** — fabless; relies on **TSMC** for wafers (n-1 node), **Amkor/ASE** for packaging, **KYEC/Sigurd** for test, **BizLink** for AEC manufacturing; flexibility to shift capacity China↔Malaysia plus a third region (~$1.5M capex per ~1mn AEC units), but "significant tightness in the supply chain" (Q4 call; JPM Credo, 2025-10-17).
- **Valuation / "show-me"** — premium multiple (~22x F28E EPS) on a name where the market is repricing the quality, not size, of beats; revenue must re-accelerate to justify the re-rate.
- **Geopolitics / China** — tariffs, customs, trade sanctions and cross-border restrictions; reported revenue is heavily Asia/Hong Kong by ship-to (Hong Kong ~56%, Mainland China ~18%, US ~15% per JPM), though true end-customer China exposure is low-single-digit % (JPM Credo, 2025-10-17; FY26 10-K).
- **Integration risk** — Comira (closed), Dust Photonics (~$750M, Q1 FY27) and Hyperlume (microLED/ALC) acquisitions must deliver the optical/IP roadmap.

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **JPM (J. Meyers) — 'Chips for Breakfast: MRVL Rally, … CRDO, HPE, Computex'** _(2026-06-02)_: CRDO featured in the AI-connectivity flow.
- **Sell-side PT table** _(company-specific, 2026-06-02)_: Jefferies $270 · JPM (Cardoso) $250 · Barclays $260 · GS Buy · SIG Positive — uniformly long; stock sold ~15% post-print on high buyside bars.
- **Citi (Blaine Curtis) — Asia checks / AI silicon call** _(2026-05-22)_: makes **CRDO a top pick** — "controversial," which he likes. The bear data point that knocked the stock was **BizLink (Credo's AEC cable partner) guiding a tempered first half with XA (a large customer) down**; but two offsets — (1) Credo is **ramping a second AEC source** (small/trailing-edge, even BizLink doesn't see it), and (2) **package-and-test DSP volumes up ~50–60% in Q1/Q2**, still implying a Credo beat-and-raise. AEC builds are lumpy and Credo already cycled one XA down-cycle (guided XA down, other customers up — and those customers wanted product Credo couldn't supply). On memory tiering, CRDO has a longer-term CXL-expander play alongside Marvell/Astera (Citi/Blaine, 2026-05-22).
- **650 Group — networking research** _(2026-05-26)_: constructive on the **AEC market** — "a lot of robust growth ahead." Only ~half-dozen customers are on 800G/100G-per-lane today; the rest of the industry is still on 400G or 56/28G-per-lane, and as the whole X86/GPU server complex moves to 100G-per-lane (where you can't do passive copper) AECs become the attractive solution. **CPO concern is "both overblown and much further into the future"** — multi-rack scale-up is incremental and doesn't touch existing back-/front-end topologies, so **copper lasts far longer than people anticipate**; **400G-per-lane can still be copper** (no longer up for debate). Credo's **ZeroFlap optics has neat features beyond being another 1.6T DSP**, and **ALCs (Active LED / micro-LED) open a new market**; new DSP entrants (Nvidia, Cisco/Acacia, Credo ZeroLink) make the bigger 1.6T market attractive even at lower share (650 Group, 2026-05-26).

## Intra-quarter — calls, commentary & reports

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q4 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Optical (2nd leg)** | Raised to >$600M FY27 (3 legs >$100M, +80%); floor ~$1.2B FY28 | BTG/LightCounting (Bob): Credo ("Kretos") **leader among the new optical-DSP entrants** + vertical ZeroFlap integration (with Oracle) | **✓ confirms** (optical taking off) |
| **AEC (core copper)** | Growth engine; hyperscaler + Neocloud; PCIe Gen6 MP 1H FY27 | BTG: AECs have a "bright future" (displacing passive DAC); Credo grew by adding customers despite competition | **✓ confirms** (AEC durable) |
| **Competition / agility** | (AEC leader ~80% share) | BTG: the smaller players (Credo, Astera) "more agile and faster" in AI; MRVL was slow to ramp AECs via partners | **✓ confirms** (incumbent slow) |
| **Valuation** | (n/a — management doesn't comment on the multiple) | BofA/Arya (pre-print): Buy PO $210 (30x CY27), but risks from MRVL/AVGO competition + slow AEC adoption | **⚠ nuance** ("show-me" post-print) |

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-13 | BofA · Vivek Arya | valuation | bull | CRDO among the high-growth compute/optical names; **rating BUY (C-1-9), PO $210** (30x CY27 PE, within the peer range of 22x-60x). Downside risks: MRVL/AVGO competition at scale, slow AEC adoption, a hyperscaler downturn, inability to scale. (BofA "AI 2030", 2026-05-13) — _pre-print Q4; superseded by the post-Q4 table (Jefferies $270 / Barclays $260 / JPM $250) in the sell-side section._ |
| 06-29 | Jefferies · Jeff Pu (@sssjeffpu) | demand | bull | **New Buy on CRDO** — a reversal from Pu's prior cautious "AEC headwinds... likely valued at a discount" stance (2026-05-11). The trigger is an AI-connectivity demand read-through from a projected **SpaceX neocloud buildout** (1GW→4.5GW→9.5GW 2026-28; ~2.2M/2.5M Blackwell-equiv GPUs 2027/28) — incremental GPU count drives AEC/optical content. See [SPCX](SPCX.md). |
| 06-19 | Nutty "Optics Primer" (nuttycld.substack.com, 2026-06-19) | product | bull | Nutty's CPO/silicon-photonics primer mentions Credo in the optical-DSP context. Key finding: CRDO's ZeroFlap optical transceiver and DSP stack are positioned at the early-mover edge of the new optical-DSP entrant group; the primer's discussion of CPO and high-speed optical connectivity within AI clusters reinforces Credo's thesis that AEC (copper) is a bridge to an optical future rather than a permanent endpoint. No new CRDO-specific financial data in the primer. (Nutty "Optics Primer", nuttycld.substack.com, 2026-06-19) |
| 07-09 | UBS · Randy Abrams (Asia NDR) | demand | bull | UBS (Not Rated) hosted Credo on an Asia non-deal roadshow: FY26 rev >200% YoY to ~US$1.3bn, FY27 guide >80% YoY; optics inflecting H2 FY27 to >US$600mn FY27 (optical DSPs/CSPs, SiPho PICs, zero-flap transceivers each >US$100mn). AECs multi-year — 5 of 6 major customers >$100mn, only 1 fully penetrated; NeoCloud ~20% of sales; copper reach 100G/7m, 200G/6m, 400G/3-5m. New Omni Connect inference solution connects up to 2TB LPDDR to a GPU at ~US$2.5-3k content/GPU (>$1bn potential). UBS models hyperscaler capex +81%/+21% YoY 2026/27. |
| 07-10 | Jefferies · Blayne Curtis ("Blayne's Bytes") | demand | bull | **CRDO a standout beneficiary of the META/SPCX frontier-model releases** — both scaled on NVDA GPUs, so successful frontier competition is a positive read-through for NVDA and CRDO; underscores that frontier competition supports the durability of hyperscaler capex (and AEC/optical connectivity content). (Jefferies · Blayne Curtis, 2026-07-10) |
| 07-12 | R&Co Redburn · Mike Harrison (via Rowan/Julian/Maddy) | demand | bull | **Redburn 5 weekly — Credo a "Buy," one of the most compelling ideas in the hottest space (optical networking).** Two-pronged bull case: (1) **copper has a longer runway than the market realizes** — hyperscalers keep copper relevant (cheaper, lower latency); NVDA designing GPUs with **two physical ports** to stay flexible on copper vs optical amid launch-cycle delays — CRDO's core copper products a hedge on the optical-transition risk; (2) **ZF Optics** differentiated launch — intelligent transceivers with a **software overlay predicting failures before they occur** (reduces AI-cluster downtime) vs a commoditized backdrop; **recently won an Oracle contract**, with scope to expand existing xAI/Meta/AWS/Microsoft relationships into front-end networks. **Springboard read on the shape of growth:** mgmt has talked to **~$600mn FY27 optical rev**, but growth is heavily back-ended — Redburn estimates a **Q4 exit rate ~$335mn → >$1.3bn annualized**, so at 30% growth **FY28 optical could be >$1.7bn**, well above consensus (which most model as a linear $150mn×4). $51bn market cap. (R&Co Redburn / Mike Harrison, 2026-07-12) |
| 06-25 | BTG · LightCounting call | competition | bull | Expert (Bob) on **Credo (referred to as "Kretos")**: it is the **leader among the new optical-DSP entrants**, focused on China/low-cost, but also doing something unusual — **vertical integration with ZeroFlap transceivers** (same playbook as the AECs, a complete product; developed with Oracle OCI). Ranks the near-term entrants **Kretos > MaxLinear > Qualcomm**. On AECs he sees a **bright future** (displacing passive DAC within/between racks) — "did a tremendous job adding customers and growing despite competition from larger incumbents"; pivoting to optical. The smaller companies (Credo, Astera) are "more agile and faster" in AI vs incumbents (e.g., MRVL was slow to ramp AECs via cable partners). (BTG "LightCounting", 2026-06-25) |
| 07-11 | Mizuho · Vijay Rakesh | valuation | bull | **"DC Capex Ramping to >$1.4T in 2028E" — reiterate Outperform, PT $290** (~19x F28E P/S; new Street high; price $257.79). CRDO named a **"critical supplier"** (with LITE) to the AI DC-capex ramp (cons **$1.2T 2027E / >$1.4T 2028E**; ~$50B/GW; 106GW 2026-30E ≈ $5.3T). Thesis: SerDes-IP-led lower-TCO edge across **AEC + Optical DSP + ALC + ZeroFlap optics + OmniConnect**; LT TAM **~$10B (>3x the mid-2024 ~$3B)**; engaged with all 7 major hyperscalers; GM ~65% (at-to-above LT 63-65%). (Mizuho / Vijay Rakesh, 2026-07-11) |
| 07-13 | Morgan Stanley · Marshall/Moore | product | bull | **"Bringing More Light to Scale-Up Networks: An Updated Scale-Up Primer"** (scale-up TAM 4x'd to ~$70bn by 2030). CRDO (**Not Covered**): "one of the cleanest exposures to **copper durability**" via the **ZeroFlap AEC franchise**; base primarily scale-out, but **Blue Heron gives direct scale-up optionality across UALink/ESUN/Ethernet**, and the optical expansion (**DustPhotonics, ZeroFlap optical transceivers, new optical-DSP portfolio**) broadens exposure across **800G/1.6T/3.2T** and hedges the copper→optics transition. MS cites mgmt's **>80% FY2027 revenue growth** and **>$600M from optical products** — optics a "meaningful second growth engine, not just a defensive hedge"; watch item = **execution across several new product categories**. (MS / Meta Marshall / Joseph Moore, 2026-07-13) |

**Quarter synthesis:** the expert flow (BTG) is confirmatory on both legs — optical taking off (Credo the leader among the new DSPs + the ZeroFlap vertical) and AEC durable with agility vs slow incumbents — but the market debate shifted from the thesis to the **quality of the beat**: after the print, the stock fell ~15% and entered "show-me" mode on when revenue re-accelerates, despite the raise. **07-11/07-13 add two constructive marks:** Mizuho reiterates Outperform at a **new Street-high $290**, tagging CRDO a "critical supplier" to the >$1.4T-2028E DC-capex ramp (LT TAM ~$10B, >3x mid-2024); and MS's Updated Scale-Up Primer (NC) frames CRDO as a clean copper-durability play with a real second optical leg (Blue Heron scale-up optionality + DustPhotonics; >80% FY27 rev growth, >$600M optical) — both reinforce the two-legged (copper + optics) bull, with execution across the new optical categories the residual watch item.

## Management commentary — evolution (last 4 quarters)

| Theme | Q1 FY26 (2025-09-03) | Q2 FY26 (2025-12-01) | Q3 FY26 (2026-03-02) | Q4 FY26 (2026-06-01) |
| --- | --- | --- | --- | --- |
| Revenue / top-line | $223.1M, +31% q/q, +274% y/y (record) | $268M, +20% q/q, +272% y/y (record) | $407M, +52% q/q, +200%+ y/y | $437M, +7% q/q, +157% y/y; FY26 $1.3B +206% |
| AEC (core copper) | Record; double-digit seq; broadening to rack-to-rack, 200G/lane | Strong ramp; hyperscaler demand the driver | Extended to fifth hyperscaler; PCIe Gen6 sampling, MP 1H FY27 | Core growth engine; hyperscaler + Neocloud adoption |
| Optical | On track to double FY26; full DSP to 1.6T | On track to double FY26 | ZeroFlap shipping to TensorWave; ramp pulled into Q1 FY27 | Raised to >$600M FY27 (3 legs each >$100M, +80%); FY28 floor ~$1.2B |
| Non-GAAP gross margin | 67.6% | 67.7% | 68.6% (+92 bps q/q) | 68.3%; FY26 68.1% (+310 bps y/y) |
| Customer concentration | Three >10% (35/33/20%); 4th hyperscaler emerging | Three >10% | Three >10% (39/32/17%); guides 3-4 in coming qtrs | Four ≥10% (34/27/16/10%); Neocloud/Tier-2 to ~20% |
| Forward outlook | FY26 ~+120% y/y; net margin ~40% | FY26 framed to ~triple FY25 (~$1.3B) | FY27 >50% y/y (MSD seq growth) | FY27 raised to >80% y/y; GM ~flat; net margin ~50% |

_Source: CRDO earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY2026 (2026-06-15)](../CRDO/CRDO_10-K_2026-06-15_0001628280-26-043303.html); [10-Q Q3 FY26 (2026-03-03, qtr ended 2026-01-31)](../CRDO/CRDO_10-Q_2026-03-03_0001628280-26-014017.html).
- **Transcripts:** [Q4 FY26 (2026-06-01)](../CRDO/transcripts/CRDO_Q4-FY26-earnings_2026-06-01.md); [Q3 FY26 (2026-03-02)](../CRDO/transcripts/CRDO_Q3-FY26-earnings_2026-03-02.md); [Q2 FY26 (2025-12-01)](../CRDO/transcripts/CRDO_Q2-FY26-earnings_2025-12-01.md); [Q1 FY26 (2025-09-03)](../CRDO/transcripts/CRDO_Q1-FY26-earnings_2025-09-03.md).
- **Research reports (relatórios bons):**
  - [JPM Credo — Leverage to Rising AI Interconnect; Initiate OW (2025-10-17)](../relat%C3%B3rios%20bons/JPM_Credo_Leverage_to_Ri_2025-10-17_5103388.html)
  - [JPM Hardware & Networking — 2026 Outlook (2025-12-15)](../relat%C3%B3rios%20bons/JPM_Hardware___Networkin_2025-12-15_5155719.html)
  - [TD Cowen — Connectivity / Scale-Up & Photonics; CRDO Top Pick (2026-03-11)](../relat%C3%B3rios%20bons/TDCOWEN.html)
  - [SIG — 3Q25 Optical-SIGnals (2025-10-09)](../relat%C3%B3rios%20bons/3Q25_Optical-SIGnals_10-09-25_1.html)
  - [SemiAnalysis — AWS Trainium3 Deep Dive](../relat%C3%B3rios%20bons/AWS_Trainium3_Deep_Dive___A_Potential_Challenger_Approaching.html)
  - [Citi (Blaine Curtis) — Asia checks / AI silicon (2026-05-22)](../relat%C3%B3rios%20bons/2026_05_22_jef_asia_recal_call_22_may_2026.html) — CRDO top pick; BizLink/XA bear point + 2nd-source and DSP P&T-volume offsets.
  - [650 Group — networking research (2026-05-26)](../relat%C3%B3rios%20bons/2026_05_26_650_group_26_05.html) — AEC robust growth, CPO concern overblown/far out, copper at 400G/lane, ZeroFlap/ALC optionality.
  - [BofA (Vivek Arya) — "AI 2030: Stronger for Longer" (2026-05-13)](../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html) — CRDO Buy, PO $210 (30x CY27); riscos competição MRVL/AVGO + adoção AEC (pré-print Q4).
  - [BTG — LightCounting optics/CPO expert call (2026-06-25)](../relat%C3%B3rios%20bons/BTG_LightCounting_Optics_Expert_Call_2026-06-25.html) — Credo ("Kretos") leader among the new entrants in optical DSP + vertical integration (ZeroFlap, with Oracle); bright future for AECs; smaller players (Credo/Astera) more agile than incumbents.
  - [Mizuho (Vijay Rakesh) — "DC Capex Ramping to >$1.4T in 2028E; FCF Outlook Improving" (2026-07-11)](../relat%C3%B3rios%20bons/DC_Capex_Ramping_to__14T_in_2028E_FCF_Outlook_Improving.html) — CRDO Outperform PT $290 (new Street high); "critical supplier" to the DC-capex ramp; SerDes-IP TCO edge; LT TAM ~$10B (>3x mid-2024 ~$3B); GM ~65%; engaged w/ all 7 major hyperscalers.
  - [Morgan Stanley (Marshall/Moore) — "Bringing More Light to Scale-Up Networks: An Updated Scale-Up Primer" (2026-07-13)](../relat%C3%B3rios%20bons/TELECOM_20260713_0418.html) — CRDO (NC): cleanest copper-durability play (ZeroFlap AEC), Blue Heron scale-up optionality (UALink/ESUN/Ethernet), optics the 2nd growth engine (DustPhotonics; >80% FY27 rev growth, >$600M optical); execution the watch item.
- **Briefings:** ~42 hits across `E:\briefings\2026\*` — Q4 print recap + sell-side PT table (2026-06-01/02), copper-vs-optical FinTwit debate (2026-05-12/13/14), connectivity bucketing + 12m relative highs (2026-06-19). JPM "Chips for Breakfast" thread context.
- **Themes:** [optical-cpo](themes/optical-cpo.md) (CRDO in stronger copper+optics bucket vs pure-play optics); [custom-asic-tpu](themes/custom-asic-tpu.md) (AI back-end/scale-up interconnect read-through).
- **Outlook / sell-side emails:** no Outlook tool available in this environment — none pulled directly. Sell-side stances above are quoted from the on-disk briefing roll-ups (JPM, Jefferies, Barclays, GS, SIG, Vital Knowledge) and the research reports listed above, attributed by bank + date.

## Changelog
| Date | Change |
|---|---|
| 2026-07-13 | Added two notes. **Mizuho (Vijay Rakesh) "DC Capex Ramping to >$1.4T in 2028E" (2026-07-11)** — reiterate Outperform, **PT $290 (new Street high, ~19x F28E P/S)**; CRDO a "critical supplier" to the DC-capex ramp; SerDes-IP TCO edge, LT TAM ~$10B (>3x mid-2024 ~$3B), GM ~65%. **MS (Marshall/Moore) "Updated Scale-Up Primer" (2026-07-13, NC)** — CRDO cleanest copper-durability play (ZeroFlap AEC), Blue Heron scale-up optionality (UALink/ESUN/Ethernet), optics the 2nd growth engine (DustPhotonics; mgmt >80% FY27 rev growth + >$600M optical); execution the watch item; scale-up TAM 4x'd to ~$70bn by 2030. Added the Mizuho PT + an MS bullet to "Where the sell-side stands," 2 intra-quarter rows (07-11, 07-13), 2 Sources links, and a synthesis update. No PT superseded — Mizuho a new-broker addition (highest PT); MS is Not Covered (no PT). Additive. |
