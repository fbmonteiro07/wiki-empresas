<!-- Per-company wiki page. Financials block (Consensus estimates, BBG, EUR) is auto-injected
     by build_wiki_html.py from _data/estimates.json — do NOT hand-write it. -->

# BESI — BE Semiconductor Industries N.V.

_Wiki · generated 2026-06-20 · **Dutch issuer — no SEC 10-K/10-Q/20-F**; sources: transcripts + Besi IR + BBG (EUR). Euronext Amsterdam: BESI (ADR: BESIY). Local sources: `E:\Wiki Felipe\BESI\transcripts` · `E:\briefings\2026\*-company-specific.md`. Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · EUR

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | €956m | €1.3bn |
| Gross profit | €619m | €824m |
| Gross margin | 64.8% | 65.7% |
| EBITDA | €431m | €566m |
| EPS | €4.12 | €5.97 |
| Capex | €14m | €17m |
| OCF (≈EBITDA) | €431m | €566m |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
BESI is the leading supplier of semiconductor **assembly / advanced-packaging equipment** — die attach (incl. **hybrid bonding** and **thermo-compression bonding, TCB**), packaging (molding, trim & form, singulation), and plating/cleaning. The structural story is **hybrid bonding**: BESI's lead tool for the 2.5D/3D stacking that AI silicon needs (HBM stacking, logic-on-logic, CoWoS-class 2.5D). AI-related orders were ~50% of total 2025 orders (Q4-25 call, 2026-02-19). Margins are best-in-WFE (GM 63–66%) and the model is highly geared to the HBM/CoWoS capex cycle. Hardware partner of Applied Materials on the highest-end HB roadmap.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Hybrid bonding / TCB die-attach systems · 2) Die-attach (epoxy/eutectic) · 3) Packaging (molding, trim & form, singulation) + plating/cleaning |
| **Main buyer(s)** | Foundries & OSATs building AI packages — TSMC, Intel, ASE/Amkor — for 2.5D/3D (HBM, CoWoS); HB adoption now 20 customers; end-demand AMD/Broadcom/Apple |
| **Key suppliers** | Precision components, optics & motion parts; Applied Materials (AMAT) HB hardware partner on highest-end roadmap |

## Position in the value chain
BESI sits in the **back-end / advanced-packaging** tier of semicap — between precision-component suppliers and the foundries/OSATs that build AI packages. Hybrid bonding is the AI-packaging optionality: the bonding step for 2.5D/3D structures (HBM stacks, chiplet/logic stacking) that scales with HBM and CoWoS-class capacity. Cross-links: [cowos-packaging](themes/cowos-packaging.md), [semicap-wfe](themes/semicap-wfe.md).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="BESI position in the value chain">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 z" fill="#444"/>
    </marker>
  </defs>
  <rect x="10" y="70" width="170" height="80" rx="8" fill="#eef3fb" stroke="#5b7fb5"/>
  <text x="95" y="100" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold">Suppliers</text>
  <text x="95" y="120" text-anchor="middle" font-family="sans-serif" font-size="11">precision components,</text>
  <text x="95" y="135" text-anchor="middle" font-family="sans-serif" font-size="11">optics, motion, parts</text>
  <rect x="270" y="55" width="190" height="110" rx="8" fill="#fdf2e3" stroke="#d59034"/>
  <text x="365" y="82" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold">BESI</text>
  <text x="365" y="102" text-anchor="middle" font-family="sans-serif" font-size="11">assembly / advanced-</text>
  <text x="365" y="117" text-anchor="middle" font-family="sans-serif" font-size="11">packaging equipment:</text>
  <text x="365" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold">hybrid bonding</text>
  <text x="365" y="149" text-anchor="middle" font-family="sans-serif" font-size="11">die-attach · TCB</text>
  <rect x="540" y="70" width="170" height="80" rx="8" fill="#eaf6ee" stroke="#3f9d63"/>
  <text x="625" y="96" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold">Customers</text>
  <text x="625" y="116" text-anchor="middle" font-family="sans-serif" font-size="11">TSMC · Intel · OSATs</text>
  <text x="625" y="131" text-anchor="middle" font-family="sans-serif" font-size="11">2.5D/3D AI packaging</text>
  <line x1="180" y1="110" x2="268" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="460" y1="110" x2="538" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="365" y="195" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="#a05a00">Hybrid bonding = the AI-packaging optionality (HBM stacking + CoWoS-class 2.5D/3D)</text>
</svg>

## Current state (latest quarter)
**Q1-26 (reported 2026-04-23):** Revenue €184.9m, +11.1% q/q / +28.3% y/y (high-end mobile + 2.5D AI compute), slightly below the ~€187.6m guide midpoint. **Orders €269.7m, +7.7% q/q / +104.5% y/y** — the standout, driven by hybrid bonding. GM 63.5%; operating margin 34.6%; net income €51.6m (net margin 27.9%); net cash €103.3m. Mgmt: "unit orders for hybrid bonding systems more than doubled versus Q4 and exceeded prior quarterly peak from Q2 2024"; HB adoption now **20 customers**. **Q2-26 guide: revenue +30–40% q/q, GM 64–66%**, opex flat to +10%; H1-26 tracking ~+49% y/y (Q1-26 call). On 2.5D/3D, mgmt cited "accelerated and broader adoption" across AMD, Broadcom, Apple M5; CoWoS expansion and photonics/CPO driving robust orders. Prior call (Q4-25, 2026-02-19): AI = ~50% of 2025 orders; >150 cumulative HB systems; AMAT partnership supports highest-end customers.

## Debate / thesis
- **Bull:** HB/CPO secular ramp. **MS (Nigel van Putten et al.), OW PT €300** raised LT revenue model to **€1.7–2.2bn** (from €1.5–1.9bn, +15% mid) and OP margin band to 45–55% (from 40–55%) at the June 18 investor day; CPO "clearest area of upside," moving R&D→production faster than expected; tech lead of 2–4 generations; 20 customers ordered, 10 in production (MS, 2026-06-18/19). **Redburn Rothschild, Buy PT €350** (from €270) on FY26-30E revenue +9–20% (EBIT +13-27%, 3-14% above consensus), two AI-logic HB opportunities (Redburn "Two opportunities, Two risks", 2026-06-15). The two new logic legs: (1) **China / Huawei LogicFolding** — Huawei's logic-on-logic 3D stacking (to chase transistor density without sub-7nm EUV access) needs BESI's industry-leading alignment accuracy; Redburn forecasts a **cumulative 73 bonders to China by 2030** (vs ~60 at TSMC's AP6). (2) **Co-Packaged Optics** — reliability improvements tip CPO toward scale-up networking adoption in **2028/29**; the PIC-EIC bond in TSMC's COUPE requires D2W HB, for a **cumulative 50 CPO bonders by 2030** (accelerating from 2H28). Redburn models BESI revenue €972m(FY26E)/€1,414m('27)/€1,820m('28) — HB €242m→€1,085m (60% 5yr CAGR) — and a **46% EBIT CAGR to 2030**; mainstream is also firming as OSAT (ASE/Amkor) FY26 capex expectations rose ~122% YTD and ASE utilization hit ~80% in Q1-26 (Redburn, 2026-06-15). Adoption already broadening in logic: AMD V-Cache (memory-on-logic) → ASICs, and Intel's **Clearwater Forest** is its first commercial hybrid-bonded chip on Foveros Direct (Redburn, 2026-06-15). CEO at investor day: "everything up and to the right…order momentum improved significantly since Q2-25" (per BofA EU, 2026-06-18).
- **Bear:** Near-term HB ramp is more measured than the 2030 headline implies — MS cut FY26/27 estimates -4%/-3% (FY28 +2%) even while raising LT model (MS, 2026-06-19). HBM-for-HB adoption is not locked: HBM4E is first adoption point, broader adoption in HBM5; all three memory makers still *evaluating* (Q1-26 call). Redburn models only a **cumulative 247 HBM bonders** through 2030 — a lower BESI share in memory than logic (Korean makers lean on local supply: SEMES, Hanwha Semitech) and a **probability-adjusted haircut to the D2W bonder market** for two structural risks: (1) **Wafer-to-Wafer (W2W) bonding** — imec/EV Group demoed 200nm W2W at ITF World 2026; W2W's batch throughput is ~8x D2W and could be used to bond DRAM *pairs* before D2W stacking, **halving** the D2W bond count for HBM; (2) **optically-networked commodity DRAM** — pooling DRAM off the accelerator via optical links could shrink the HBM market altogether, though a ~300ns light↔electrical conversion latency makes near-term displacement unlikely. Redburn concludes evolutionary D2W still wins but lowered its valuation multiple 29x→28x EV/EBIT to reflect the memory uncertainty (Redburn, 2026-06-15). Supply-chain checks reinforce the timing risk: SK Hynix says HB is "not for HBM4E" (it's for faster/higher-layer products beyond ~20 layers, requiring a full equipment changeover and "a lot more investment"); Samsung is doing technical HBM4 alignment work but "won't be commercial on current plans" and still leans on thermal/fluxless bonding; Inspectrum pegs the HB crossover at 16-20 Hi layers. NAND is leading actual HB adoption (YMTC, Kioxia in mass production; Samsung/Hynix/Micron not yet, "strategically" timing) (Jefferies Techknowledge, 2025-12-17). High multiple, EUR-reported, cyclical order book, China/CoWoS concentration.
- **Bull (sole TSMC-qualified HB + SOIC sizing; Redburn "Conor O'Mara Asia Trip Takeaways", 2026-06-23):** Conor reiterates **Besi remains the sole TSMC-qualified hybrid bonder — Shibaura (Shibarra) is not yet qualified** (TSMC keeps raising the specs). He sizes the SOIC leg directly: **TSMC's aggressive SOIC capacity expansion in 2027-28 needs 15-20 hybrid bonders per 10,000-unit SOIC line**, with new SOIC use cases being **silicon-photonics chips and Broadcom's next-gen TPU**. Conor flipped bullish on Besi on these SOIC/HB numbers (after being bearish for a while) but cautions that **buy-side expectations have risen a lot — a lot is already priced in** (Redburn "Conor O'Mara Asia Trip Takeaways", 2026-06-23). One offsetting tell: Samsung disclosed for the first time it has its own hybrid-bonding project and would offer it at a premium (higher HBM4E stacks) — incremental TAM but also a longer-run second source (Redburn, 2026-06-23).
- **Competitive watch (NEW):** Supply-chain checks flag would-be entrants chipping at BESI's HB lead. **Shibaura's TFC-6800** logic die-to-wafer hybrid bonder is "under evaluation at TSMC" with a "pretty good" early read; BESI was first-mover and Shibaura is trying to catch up (10x accuracy hurdle at 0.1 micron) while pushing higher UPH via double-head config — progress expected "some time in 2026." **TEL** may enter the die-to-wafer HB market (currently wafer-to-wafer only, Y500bn 5-yr bonding target from Y30bn), and **AMAT** — BESI's HB hardware partner — is also running its own die-to-wafer R&D leveraging cleaning/probing IP. **TOWA** frames "ASMPT and BESI as still very early stage" in HBM-stack molding (no mould production yet). DISCO notes it doesn't compete with BESI in dicing/grinding (Jefferies Techknowledge, 2025-12-17). Supports the bear's competitive-intensity point against the 2–4-generation-lead claim.
- **Where sell-side stands:** **MS OW €300; Redburn Rothschild Buy €350.** BofA EU constructive on the ASML/ASMI/**BESI** Intel-foundry optionality basket (base ~15 BESI HB tools / bull ~182 if iPhone on Intel; BofA EU, 2026-05-11). On Redburn 12m relative-highs screen (2026-06-15). **Bernstein/Rasgon (WFE / AI GW note, 2026-07-20): Outperform, PT €280** (px €225.50; EPS €1.66/3.34/5.84 25A/26E/27E) — table-level, the first Bernstein PT on the page (no dedicated thesis in the note).
- **M&A / consolidation chatter (NEW, AlphaSense Deep Research, 2026-06-22):** the AlphaSense primers surface a building takeover narrative around BESI. Kepler Cheuvreux reports "takeover interest has built around Besi, with **Lam named as an active suitor**" — acquiring BESI would complete Lam's adv-packaging value chain into hybrid die-bonding (Kepler "Besi", 2026-03-13, via AlphaSense). The ASML primer frames **ASML as a "prominent logical consolidator"** of BESI (die-to-wafer hybrid-bonding leader, >90% share) — a Dutch-on-Dutch deal would bypass the Vifo-Act screening US buyers (Lam/AMAT) face, and BESI's ~€14B market cap is only ~3-4% of ASML's value; ASML mgmt calls a BESI acquisition a compelling "build-or-buy" alternative while exploring internal hybrid-bonding with Prodrive/VDL-ETG. **AMAT holds a ~9% stake in BESI** (a commercial advantage / defensive motive). Bernstein cautions mass-market HB adoption for HBM/DRAM likely pushes to ~2028 as the industry runs lower-cost thermal-compression bonding through 2026-27 (AlphaSense "DR ASML/LRCX primers", 2026-06-22).

## Catalysts / what to watch
- **Q2-26 print (~late July 2026)** — test of the +30–40% q/q revenue guide and the HB order trajectory.
- **HBM-for-HB qualification milestones** — memory-maker sample quals through mid-2026; mainstream production 2027 (HBM4E→HBM5).
- **CPO / co-packaged optics** moving R&D→production — flagged by mgmt and MS as the clearest upside.
- **CoWoS / 2.5D capacity adds** at TSMC + OSATs; China 2.5D buildout sustainability.
- **Shibaura TFC-6800 TSMC evaluation outcome** — competitive read-through on BESI's logic die-to-wafer share, with progress flagged for "some time in 2026" (Jefferies Techknowledge, 2025-12-17).
- Execution on the raised €1.7–2.2bn LT model laid out at the June 18 investor day.
- **CoWoS / flip-chip read-through (Jefferies & BofA, Apr-2026):** BESI benefits from TSMC's aggressive CoWoS capacity adds via its flip-chip business; **AI is now ~50% of BESI revenue**, set to benefit from added SoC capacity (AMD now, NVDA/Broadcom later, plus Ethernet-switch CPO and Apple/Broadcom) (Jefferies "Asia tech", 2026-04-07; BofA "TSMC review" raised numbers on ASM + BESI, 2026-04-16). Watch: **Shibaura is *not* qualified for logic-logic hybrid bonding** (incremental positive for BESI), per Jefferies expert (2026-04-07).
- **Advanced-packaging call-option framing (Citrini "26 Trades for 2026", 2025-12-17):** frames BESI as an advanced-packaging die-attach leader tied to TSMC + Applied Materials (their **"Kinex"** JV — AMAT supplying Xtera epi + PROVision e-beam into GAA / backside-power / wafer-level hybrid-bonding flows), where **mainstream + photonics do the near-term work** and the **real 2026+ call-option is logic-side hybrid bonding / advanced die-attach** as designs move to true 3D stacks (Foveros Direct, SoIC). Key nuance: if **Intel pushes its most-advanced 3D roadmap right to conserve cash, BESI's orders slip right too**, whereas **KLIC (EMIB) and Amkor (packaging) are needed for immediate production** — i.e. BESI is the later-cycle, higher-optionality name (Citrini "26 Trades for 2026", 2025-12-17).

## Risks
- HBM hybrid-bonding adoption slips or HBM5-weighted (back-end-loaded), not HBM4E — the central swing; SK Hynix/Samsung checks point to HB landing beyond ~20 layers and post-HBM4E, with NAND (YMTC/Kioxia) leading actual adoption (Jefferies Techknowledge, 2025-12-17).
- Near-term estimates already trimmed (MS FY26/27 -4%/-3%) despite LT raise — set-up risk vs lofty multiple.
- Order-book cyclicality; lumpy HB system orders quarter-to-quarter.
- China / 2.5D-CoWoS demand concentration and export-control exposure.
- EUR reporting; FX translation vs USD-centric peer comps.
- Competitive intensity in advanced packaging (ASMPT, Shibaura on logic die-to-wafer, TEL/AMAT entry risk in die-to-wafer) despite the 2–4 generation lead claim (Jefferies Techknowledge, 2025-12-17).

<!-- Consensus estimates (BBG, EUR) block auto-injected here by the HTML builder -->

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1-26 · Apr 23 → Jul 14, 2026 · sell-side / expert calls / reports between earnings._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1-26 · 2026-04-23) | Intra-quarter flow | Signal |
|---|---|---|---|
| **HB / AI-packaging demand** | HB units >2x vs Q4, adoption to 20 customers; "everything up and to the right" | MS (OW €300) raised LT model to €1.7–2.2bn; Redburn (Buy €350) two AI-logic HB legs, visibility to 2030; Conor: sole TSMC-qualified HB, SOIC needs 15-20 bonders/10K line | **✓ confirms** (broad-based order momentum) |
| **CPO / photonics** | CPO moving R&D→production faster than expected | Redburn: CPO reliability tips scale-up adoption 2028/29 (EIC-PIC Cu-Cu HB via COUPE); ~50 CPO bonders by 2030 | **✓ confirms** (CPO an emerging equipment leg) |
| **AI-capex monetisation / valuation** | AI ~50% of 2025 orders; capital-light, high-return model | Rothschild/Redburn strategy screen names BESI a European top Buy (clears FCF/RoCE/leverage gates); but Conor: "a lot is already priced in," buy-side bar high | **⚠ nuance** (thesis intact, expectations elevated) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 06-15 | Rothschild/Redburn · Aziz/Schulze-Melander | produto | bull | "Two opportunities, Two risks": **Buy, PT €270→€350**; two AI-logic HB legs (Huawei LogicFolding — 73 bonders to China by 2030; CPO — 50 CPO bonders by 2030 from 2H28); BESI rev €972m/€1,414m/€1,820m FY26-28E; HB €242m→€1,085m (60% 5yr CAGR); 46% EBIT CAGR to 2030. |
| 06-18 | Morgan Stanley · van Putten (investor day) | guidance | bull | **OW, PT €300**; LT revenue model raised to €1.7–2.2bn (from €1.5–1.9bn) + OP-margin band 45–55%; CPO "clearest area of upside," 2–4 generation tech lead, 20 customers ordered / 10 in production. |
| 06-22 | AlphaSense Deep Research (ASML/LRCX primers) | capital | mixed | Building takeover narrative: Kepler names **Lam an active suitor** for BESI (completes adv-packaging chain); ASML framed as the "prominent logical consolidator" (Dutch-on-Dutch, ~€14B mcap, AMAT ~9% stake); Bernstein cautions mass-market HB for HBM/DRAM ~2028. |
| 06-23 | Rothschild/Redburn · Conor O'Mara (Asia trip) | competicao | bull | BESI **sole TSMC-qualified hybrid bonder** (Shibaura not yet); TSMC's SOIC expansion 2027-28 needs **15-20 HB per 10,000-unit SOIC line**; new SOIC use cases = silicon-photonics chips + Broadcom's next-gen TPU. Bullish, but "buy-side expectations have risen a lot — a lot is already priced in"; Samsung disclosed its own HB project (longer-run second source). |
| 07-14 | Rothschild/Redburn · Karamanos (strategy) | valuation | bull | **"AI Monetisation & the Impact on Sector Rotation" strategy note names BE Semiconductor a European top Buy** — "BESI's hybrid-bonding franchise is a direct AI-logic advanced-packaging play, with the AI upcycle strengthening and visibility extended toward 2030. Core AI infrastructure with high-return, capital-light growth." BESI clears Redburn's FCF/RoCE/leverage screen (6-mo Δ: sales-growth **+5.7%**, FCF **+28.1%**, RoCE **+1.3%**, EBITDA-margin **+0.2%**, net-debt/EBITDA **−0.2x**, capital-employed growth **+5.0%**). Rating **Buy** (Redburn Buy = ≥15% upside over 1yr); strategy-level top-Buy screen citing the earlier "BE Semiconductor: Two Opportunities, Two Risks" (15 Jun 2026) — no new PT (Redburn PT €350 unchanged). (Rothschild/Redburn · Karamanos "AI Monetisation & Sector Rotation", 2026-07-14) |
| 07-20 | Bernstein · Stacy Rasgon ("WFE / AI GW note") | valuation | bull | **TABLE-ONLY (no dedicated thesis in this note): Outperform, PT €280** (px €225.50); EPS €1.66/3.34/5.84 (25A/26E/27E). BESI carried at coverage-table level as the hybrid-bonding / advanced-packaging AI read-through; first Bernstein PT on the page. (Bernstein / Stacy Rasgon, 2026-07-20) |

**Quarter synthesis:** the intra-quarter flow is uniformly constructive on the HB/CPO secular story — MS (OW €300) and Redburn (Buy €350) both raised, Conor confirms BESI as the sole TSMC-qualified hybrid bonder into a 2027-28 SOIC expansion, and takeover chatter (Lam/ASML) adds optionality. **07-14:** Rothschild/Redburn's AI-monetisation strategy screen adds a top-Buy endorsement (advanced-packaging AI-logic play clearing the FCF/RoCE/leverage gates) — a strategy-level confirmation of the thesis rather than a new estimate; the standing caution (Conor: "a lot is already priced in," MS FY26/27 estimate trims despite the LT raise) is the offset. **07-20:** Bernstein/Rasgon's "WFE / AI GW note" carries BESI at table level — **Outperform, PT €280** (px €225.50; EPS €1.66/3.34/5.84 25A/26E/27E) — a hybrid-bonding/advanced-packaging AI read-through and the first Bernstein PT on the page (no dedicated thesis in the note).

## Management commentary — evolution (last 4 quarters)

| Theme | Q2-25 (2025-07-24) | Q3-25 (2025-10-23) | Q4-25 (2026-02-19) | Q1-26 (2026-04-23) |
|---|---|---|---|---|
| Orders / bookings | −3% q/q; H2 to rise significantly | +36.5% q/q to ~€174.7m, early recovery | €250.4m, +43.3% q/q | €269.7m, +7.7% q/q, +104.5% y/y |
| Hybrid bonding adoption | One 5-system HB order (>€20m); broadening | Building toward 18-customer level | 18 customers; >150 cumulative systems | 20 customers; HB units >2x vs Q4 |
| HBM-for-HB timeline | HBM4 qual on track; prod late-26 into 27 | — | 2026 key year; quals by mid-26 | Pilot/qual 2026; mainstream 2027 onwards |
| Gross margin | Q3 guide 60–62% | — | 63.3%; Q1-26 guide 63–65% | 63.5%; Q2-26 guide 64–66% |
| AI mix / 2.5D-CoWoS | Adv packaging key to AI differentiation | — | AI ~50% of 2025 orders; 2.5D share "very high" | Broader adoption: AMD, Broadcom, Apple M5 |
| CPO / photonics | — | — | Co-packaged optics in early development | Moving to production faster than expected |

_Source: BESI earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** none — Dutch issuer, no SEC 10-K/10-Q/20-F. Primary disclosure via Besi IR press releases ([besi.com/investor-relations](https://www.besi.com/investor-relations/)).
- **Research reports (relatórios bons):**
  - [Q425 Techknowledge tech takeaways (Jefferies)](../relat%C3%B3rios%20bons/Q425_Techknowledge_tech_takeaways.html)
  - [Redburn (Rothschild & Co) — "Two opportunities, Two risks" (2026-06-15; Buy, PT €350) — Huawei LogicFolding, CPO, W2W/optical-DRAM risks](../relat%C3%B3rios%20bons/Redburn_Research.html)
  - [AlphaSense Deep Research — ASML primer (2026-06-22)](../relat%C3%B3rios%20bons/DR-Report-by-Alphasense-06-22-2026-20-18.html) — BESI as ASML/Lam consolidation target (Kepler "Lam active suitor"; Dutch-on-Dutch ASML logic; AMAT 9% stake; ~€14B mcap); HB mass-market for DRAM ~2028 (Bernstein).
  - [AlphaSense Deep Research — LRCX primer (2026-06-22)](../relat%C3%B3rios%20bons/DR-Report-by-Alphasense-06-22-2026-20-13.html) — Kepler: Lam named active suitor for BESI to complete adv-packaging value chain.
  - [Jefferies — Asia tech (2026-04-07)](../relat%C3%B3rios%20bons/2026_04_07_jef_asia_7_apr_2026.html) — AI ~50% of BESI revenue; flip-chip benefits from CoWoS adds; Shibaura not qualified for logic-logic HB.
  - [Redburn (Conor O'Mara) — Asia Trip Takeaways (2026-06-23)](../relat%C3%B3rios%20bons/77420a6c-61c1-4757-8047-3a24cced258c_Key_Takeaways_from_Conor_OMaras_recent_Management_Meetings_across_ASIA_1.html) — Besi sole TSMC-qualified HB (Shibaura not); SOIC expansion 2027-28 needs 15-20 bonders/10K line; new SOIC = silicon photonics + Broadcom next TPU; bullish but much priced in; Samsung discloses own HB project.
  - [BofA — TSMC/ASML review (2026-04-16)](../relat%C3%B3rios%20bons/2026_04_16_tsm_baml_16_apr_2026.html) — raised numbers on ASM + BESI on TSMC CoWoS/SoC capacity adds.
  - [Rothschild/Redburn (Karamanos) — "AI Monetisation & the Impact on Sector Rotation" (2026-07-14)](../relat%C3%B3rios%20bons/Redburn_Research_3.html) — BESI a European top Buy (hybrid-bonding AI-logic advanced-packaging play, visibility to 2030, capital-light high-return; clears the FCF/RoCE/leverage screen: sales-growth Δ +5.7%, FCF +28.1%, RoCE Δ +1.3%); strategy-level top-Buy screen citing the earlier 15-Jun BESI note, no fresh PT.
  - [Bernstein (Stacy Rasgon) — "WFE / AI GW note" (2026-07-20)](../relat%C3%B3rios%20bons/Bernstein_on_WFE.html) — table-only: Outperform, PT €280 (px €225.50); EPS €1.66/3.34/5.84 (25A/26E/27E); BESI the hybrid-bonding/advanced-packaging AI read-through (no dedicated thesis in the note).
  - [Nutty "The AI Power Crisis — Part 4" (nuttycld.substack.com, 2026-04-25)](../relat%C3%B3rios%20bons/The_AI_Power_Crisis_Part_4_-_Nutty.html) — BESI named "the more interesting name" in the BSPDN/hybrid-bonding convergence thesis: the same process logic (attach more tightly, connect more closely) drives both BSPDN (backside power delivery) and HBM stacking, and BESI + AMAT lead the D2W (die-to-wafer) side of that convergence. SK Hynix ordering a hybrid bonding inline system jointly developed by AMAT and BESI for its HBM line — "not just an HBM headline" but validation that BESI's HB technology is at the center of both the HBM and BSPDN structural waves. EVG/Tokyo Electron lead the W2W (wafer-to-wafer) carrier-bonding side of BSPDN; BESI/AMAT lead D2W. Intel's Q1'26 call signaling advanced packaging demand "at the billions of dollars per year level" (not hundreds of millions as initially expected) directionally supports BESI's TAM.
- **Transcripts:** [`Q1-26 (2026-04-23)`](../BESI/transcripts/BESI_Q1-2026-earnings_2026-04-23.md) · [`Q4-25 (2026-02-19)`](../BESI/transcripts/BESI_Q4-2025-earnings_2026-02-19.md) · [`Q3-25`](../BESI/transcripts/BESI_Q3-2025-earnings_2025-10-23.md) · [`Q2-25 (2025-07-24)`](../BESI/transcripts/BESI_Q2-2025-earnings_2025-07-24.md). Read in depth: Q1-26 + Q4-25.
- **Briefings:** `E:\briefings\2026\2026-06-19-company-specific.md` (MS OW €300, LT model raise), `2026-06-18-company-specific.md` (investor day guide raise), `2026-05-26-company-specific.md` (Redburn Buy €350; Barclays CMD preview), `2026-05-11-company-specific.md` (BofA EU Intel-foundry basket), `2026-06-15-company-specific.md` (12m relative highs).
- **Outlook:** attempted via `outlook.py` — Python not available on PATH in this shell (`py`/`python` both failed); no live inbox pull. Sell-side attribution above is sourced from the archived company-specific briefings.
- **BBG:** consensus estimates (EUR) auto-injected by HTML builder.
- **Themes:** [cowos-packaging](themes/cowos-packaging.md), [semicap-wfe](themes/semicap-wfe.md).

## Changelog
| Date | Change |
|---|---|
| 2026-07-20 | Added **Bernstein/Stacy Rasgon "WFE / AI GW note" (2026-07-20)** — first Bernstein PT on the page: **table-only Outperform, PT €280** (px €225.50; EPS €1.66/3.34/5.84 25A/26E/27E), BESI carried as the hybrid-bonding/advanced-packaging AI read-through (no dedicated thesis in the note — not invented). Added 1 intra-quarter Full-log row (07-20, valuation/bull) + synthesis line, a "Where sell-side stands" note, and a Sources link. Additive — no PT/rating superseded (MS €300 / Redburn €350 unchanged). |
| 2026-07-16 | Added a Citrini "26 Trades for 2026" (2025-12-17) call-option datapoint to Current-state read-throughs: AMAT–BESI **"Kinex"** JV (Xtera epi + PROVision e-beam into GAA/backside-power/HB flows); BESI = the 2026+ logic-side hybrid-bonding call-option vs KLIC (EMIB)/Amkor for immediate production, with Intel-3D-roadmap timing the swing. Additive; no estimate/PT superseded. |
| 2026-07-14 | Added **Rothschild/Redburn (Karamanos) "AI Monetisation & the Impact on Sector Rotation" (2026-07-14)** — BESI a named **European top Buy** (hybrid-bonding AI-logic advanced-packaging play, visibility to 2030, capital-light high-return; clears the note's FCF/RoCE/leverage screen, 6-mo Δ sales-growth +5.7% / FCF +28.1% / RoCE +1.3%). A strategy-level top-Buy screen citing the earlier 15-Jun "Two Opportunities, Two Risks" note — **no fresh PT** (Redburn PT €350 / MS €300 unchanged). Scaffolded the **`## Intra-quarter — calls, commentary & reports`** section by hand (page previously lacked one): Signal-vs-management table + full log (populated with the post-Q1-26 flow already documented in Debate: 06-15 Redburn, 06-18 MS, 06-22 AlphaSense M&A, 06-23 Conor O'Mara + the new 07-14 row) + synthesis. Added a Sources link. No PT/rating superseded — additive. |
