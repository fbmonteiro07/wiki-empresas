<!-- Per-company wiki page (page-id TOKYOELEC = Tokyo Electron, the Japanese WFE maker).
     NOTE: ticker "TEL" in the US wiki = TE Connectivity — this is a DIFFERENT company.
     NO SEC filings — Japanese issuer (TSE: 8035). Sources: transcripts/IR + repo + BBG (JPY).
     Financials block (BBG, JPY) auto-injected — do NOT hand-write. -->

# TOKYOELEC — Tokyo Electron Limited (TSE: 8035; TEL Japan)

_Wiki · generated 2026-06-20 · **No SEC filings — Japanese issuer (TSE Prime: 8035); transcripts + IR + BBG (JPY).** Sources: `E:\Wiki Felipe\TOKYOELEC\transcripts` (IR results decks/scripts) + `E:\briefings\2026` roll-up + equity-call read-throughs (`E:\equity_calls_transcripts\Semis`) + BBG (JPY). Master index: [../INDEX.md](../INDEX.md). (Disambiguation: the US-wiki page [TEL](TEL.md) is **TE Connectivity** — unrelated.)_

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · JPY

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | ¥3075.3bn | ¥3745.9bn |
| Gross profit | ¥1420.8bn | ¥1857.9bn |
| Gross margin | 46.2% | 49.6% |
| EBITDA | ¥933.8bn | ¥1189.7bn |
| EPS | ¥1527.73 | ¥1779.04 |
| Capex | ¥209.0bn | — |
| OCF (≈EBITDA) | ¥933.8bn | ¥1189.7bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Tokyo Electron is one of the world's top-3 wafer-fab-equipment (WFE) makers and the broadest-line Japanese semicap player, alongside Applied Materials and Lam in the front-end. Its franchise is built on near-monopoly positions in a handful of process steps: **coater/developer (photoresist "track") at 91% world share**, plus strong shares in dielectric **etch (>50%)**, **deposition (CVD ~38%, ALD, oxidation/diffusion)**, **cleaning**, **wafer prober (~38%)** and HBM/3D-integration **bonders** (shares CY2025, Gartner/TechInsights via FY26 deck, 2026-04-30). Revenue = **SPE new equipment (~¥1,775bn FY26)** + recurring **Field Solutions (¥626bn, +16% FY26)**. End-mix is non-memory/logic-foundry ~59%, DRAM 31%, NAND 10%. It is the cleanest Japanese-listed proxy for the leading-edge WFE up-cycle (litho-adjacent track, GAA etch, HBM packaging). Reports in English; fiscal year ends March. See cross-theme: [semicap-wfe](themes/semicap-wfe.md).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Etch (~36% of SPE) · 2) Coater/developer track (~28%, 91% world share) · 3) Deposition CVD/ALD (~20%) |
| **Main buyer(s)** | Leading-edge foundries & memory makers (TSMC, Samsung, SK Hynix, Micron); end-mix non-memory/logic 59% / DRAM 31% / NAND 10%; China 34% of FY26 sales |
| **Key suppliers** | Upstream precision components, sub-systems and raw materials (parts/materials inflation a margin driver; Strait-of-Hormuz flagged as supply-chain risk) |

## Position in the value chain
TEL sits in the middle of the WFE chain: it buys precision components and sub-systems from upstream suppliers, builds front-end process tools (coat/develop, etch, deposition, cleaning) plus prober/bonder, and sells them to the leading foundries and memory makers (TSMC, Samsung, SK Hynix, Micron). Its leverage is to **leading-edge node transitions and memory/HBM capex** — coater/developer rides every EUV layer, etch rides DRAM-capacitor/GAA/HBM, bonders ride advanced packaging.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="#444"/>
    </marker>
  </defs>
  <rect x="8" y="65" width="170" height="90" rx="6" fill="#eef3fb" stroke="#3b6db3"/>
  <text x="93" y="92" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="93" y="112" text-anchor="middle">Precision components,</text>
  <text x="93" y="128" text-anchor="middle">sub-systems, materials</text>

  <rect x="238" y="45" width="244" height="130" rx="6" fill="#fdf1e3" stroke="#c87f2a"/>
  <text x="360" y="70" text-anchor="middle" font-weight="bold">Tokyo Electron (WFE)</text>
  <text x="360" y="90" text-anchor="middle">Coat / develop (track, 91% share)</text>
  <text x="360" y="108" text-anchor="middle">Etch · deposition · cleaning</text>
  <text x="360" y="126" text-anchor="middle">Prober · HBM / 3D bonders</text>
  <text x="360" y="148" text-anchor="middle" font-style="italic">Top-3 global WFE maker</text>

  <rect x="542" y="55" width="170" height="110" rx="6" fill="#eaf6ed" stroke="#3a8f51"/>
  <text x="627" y="80" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="627" y="102" text-anchor="middle">Foundries: TSMC</text>
  <text x="627" y="120" text-anchor="middle">Memory: Samsung,</text>
  <text x="627" y="136" text-anchor="middle">SK Hynix, Micron</text>

  <line x1="178" y1="110" x2="236" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="482" y1="110" x2="540" y2="110" stroke="#444" stroke-width="2" marker-end="url(#arr)"/>
</svg>

## Current state (latest quarter)
**Q4 FY2026 (quarter ended Mar-2026; reported Apr-30-2026) — strong rebound off a timing-driven Q3 trough.** Net sales **¥711.8bn (+28.9% QoQ, +8.6% YoY)**; gross margin **46.8% (+4.1pts QoQ)**; operating income **¥205.6bn (+77.1% QoQ)**, OPM **28.9%**; net income ¥214.2bn (lifted by a ¥115.4bn full-year gain on sale of strategic shareholdings) (FY26 IR deck, 2026-04-30). Q3 FY26 had dipped to ¥552.0bn / OPM 21.0% purely on **shipment timing**, not demand (Q3 deck, 2026-02-06).

**Full-year FY2026:** net sales **¥2,443.5bn (+0.5% YoY, record)**; gross profit ¥1,107.8bn, **GM 45.3% (−1.8pts YoY)**; operating income **¥624.9bn (−10.4% YoY)**, OPM **25.6% (−3.1pts)**; net income **¥574.4bn (+5.6%, all-time high)**; ROE 29.6%; record FCF ¥433.2bn. **Margin compression** came from parts/materials inflation, product mix, more ex-Japan field engineers, and +11% R&D — TEL is spending into the cycle, not harvesting it (FY26 deck, 2026-04-30). SPE end-mix FY26: **non-memory 59% / DRAM 31% / NAND 10%**; by product Etch 36% / Coater-developer 28% / Deposition 20% / Cleaning 9% / Prober 5%. China fell to **34.1% of FY26 sales** (from 41.7% FY25) as leading-edge (Korea/Taiwan) outgrew mature-node (China-heavy).

**Guidance — new H1-only disclosure (FY27 H1):** net sales **¥1,570bn**, GM 45.5%, operating income **¥431bn (OPM 27.5%)** — all half-year records, driven by AI-server demand; **H2 guided stronger than H1** on later-CY26 DRAM + advanced-logic shipments. SPE new equipment H1 FY27 **+41% YoY to ¥1,200bn**. FY27 product drivers: **coater/developer +50%+** (DRAM EUV + logic EUV multi-patterning), **etch ~+25–30%** (DRAM capacitor PORs at all leaders, HBM interconnect, GAA gate/isotropic at 2nm), **advanced packaging +60%+** (prober >¥100bn; HBM bonders, logic 3D-integration). FY27 capex ¥190bn, R&D ¥330bn (FY26 deck, 2026-04-30). WFE-market outlook: **CY26–27 $150–170bn/yr, +20%+ vs ~$120bn CY25; leading-edge +30%+.**

## Debate / thesis
- **Bull:** TEL is the highest-share, broadest-line beneficiary of the leading-edge WFE up-cycle the Street keeps raising — UBS/Arcuri models WFE TAM ~$200B CY27 / ~$250B CY28 and says the buy side is "not there" ([semicap-wfe](themes/semicap-wfe.md); Arcuri/UBS, 2026-05-15). TEL's **91% coater/developer share** makes it a toll on every incremental EUV layer (DRAM EUV adoption + logic EUV multi-patterning), and it has won DRAM-capacitor and **HBM-interconnect etch PORs at all leading memory customers** — direct leverage to the HBM build-out ([hbm-memory](themes/hbm-memory.md); FY26 deck, 2026-04-30). Memory is the dollar engine: JPM/Tokyo desk hears CY26 WFE +25–30% / CY27 +20–25% (Shikanai/JPM memory call, 2026-05-28). FY27 H1 already guided +41% SPE and record half-year profit. CEO Kawai: confident in Japan toolmakers' edge vs China; 3D-integration business ¥30bn last yr → potential ¥300bn+ by 2030 (President Kawai, FinTwit @illyquid, briefing 2026-06-18).
- **Bear:** (1) **Margins went the wrong way** — FY26 GM −1.8pts / OPM −3.1pts on parts/materials inflation, mix and ex-Japan field-engineer build; the cycle is lifting revenue but not yet margins, and TEL has barely flexed pricing (vs the WFE-pricing-upside thesis). (2) **China ~34% of revenue and falling** — still a third of the book and exposed to US/Japan export-control escalation and ICAP mature-node overcapacity (China weighting down from 42%→34%, declining as AI capex shifts elsewhere; @illyquid, briefing 2026-06-18). (3) **Lumpy, timing-driven prints** — Q3 FY26 air-pocket (OPM 21%) shows how a few large customers swing the quarter; TEL even *stopped* giving full-year guidance because customer investment is "extremely big in size" and unpredictable. (4) **NAND only 10%, and the NAND-WFE recovery looks capped** — MS names TEL among the Japanese SPE makers with relatively high NAND sales exposure (with Kokusai, Disco, Micronics Japan), but models NAND WFE at only ~$10.2bn in 2025 (+102% y/y) → ~$11bn 2026 (+8%) and NAND WFE intensity recovering from 8% (2024) to ~18% (2025) then *flat-lining through 2027* — not back to pre-2022 30%+ — because (a) bit-demand growth has moderated to mid-teens (~9% modeled 2025), (b) SK Hynix/Micron/Samsung are steering capex to DRAM/HBM (DRAM WFE intensity up, overall memory WFE intensity broadly flat) with no greenfield NAND yet started, and (c) makers are getting bit-density from lateral shrink, CBA wafer-bonding and QLC rather than pure layer-count etch/dep — capping the etch/deposition pull TEL is most levered to ("MS AI NAND overview", 2025-09-10). Net: NAND is a thin, migration-only near-term lever; MS itself stays "relatively cautious on WFE" and prefers Advantest/Disco (test/grinder) over the WFE names. (5) Buy-side bars across WFE are high — even strong prints have sold off (AMAT precedent; Sur/JPM, 2026-05-15).
  - _Nuance — CBA/wafer-bonding offsets part of the NAND-etch bear:_ MS flags CMOS-bonded-array (wafer bonding) as a primary NAND density lever displacing layer-count, which plays *to* TEL's HBM/3D-integration bonder franchise even as it caps NAND etch/dep intensity ("MS AI NAND overview", 2025-09-10).
- **Where the Street stands:** No US sell-side PT in the inbox (Japanese issuer; Outlook not reachable this session). Read-through from the WFE complex is constructive — KLA the only large-cap to commit CY27 WFE > CY26; AMAT/LRCX preferred US pair; ASML the litho choke point (briefings/semicap-wfe theme). MS sits relatively cautious on WFE into 2026 on China headwinds + conservative NAND capex, preferring Advantest/Disco within Japan semicap ("MS AI NAND overview", 2025-09-10). Tape: Tokyo Electron **+4.7%** in the memory-led Japan rally on Tim Cook's memory price-hike read-through (briefing, 2026-06-18).

## Catalysts / what to watch
- **Q1 FY2027 print — late-Jul/early-Aug 2026** (next reporting date). First test of the +41% SPE H1 ramp and whether GM/OPM inflect back toward the >50% GM / >35% OPM 2-year target management flagged.
- **H2 FY27 acceleration** — guided stronger than H1 on later-CY26 DRAM + advanced-logic; watch order cadence.
- **Coater/developer & etch order flow** — DRAM EUV adoption and 2nm GAA gate-etch ramps; advanced-packaging prober crossing ¥100bn.
- **HBM/3D-integration** — bonder/debonder, permanent wafer bonding; Kawai's ¥300bn+ by 2030 ambition for 3D integration. The CBA/wafer-bonding NAND density lever MS calls out is an incremental pull on the same franchise ("MS AI NAND overview", 2025-09-10).
- **NAND greenfield watch** — MS notes no greenfield NAND expansion has started; an early-CY26 greenfield announcement would be the swing factor for NAND-WFE (and TEL etch/dep) re-rating, vs the modeled flat-line through 2027 ("MS AI NAND overview", 2025-09-10).
- **China export-control / ICAP** — any US/Japan tightening hits the ~34% China book and CXMT-linked mature-node demand.
- **WFE TAM revisions** — UBS $200B/$250B CY27/28 vs Street; the memory-capex re-rate is the swing factor (semicap-wfe theme).
- **Geopolitics** — TEL flagged a protracted Strait-of-Hormuz blockade as a parts/materials supply-chain risk (FY26 deck, 2026-04-30).

## Risks
- **Margin pressure** — parts/materials inflation, product mix and ex-Japan headcount drove FY26 GM/OPM down; the 2-yr >50% GM / >35% OPM target is unproven.
- **China concentration / export controls** — ~34% of revenue; falling but still large, exposed to mature-node overcapacity and US/Japan restrictions.
- **Customer concentration & timing lumpiness** — a few large foundry/memory customers swing quarters (Q3 FY26 trough); company withdrew full-year guidance for this reason.
- **Cyclicality** — WFE is capex-driven; an AI-capex air-pocket or memory price reversal would hit new-equipment orders (Field Solutions partly cushions).
- **NAND under-exposure / structurally-capped NAND-WFE** — only ~10% of SPE; MS models NAND WFE intensity flat-lining ~18% through 2027 (not back to pre-2022 30%+) as memory capex tilts to DRAM/HBM and density shifts from layer-count etch/dep to lateral-shrink/CBA/QLC, capping the etch/dep dollars TEL is most levered to ("MS AI NAND overview", 2025-09-10).
- **FX / Japan-issuer factors** — yen-denominated sales limit translation risk but ADR-less listing and thinner US sell-side coverage vs AMAT/LRCX/KLAC.

<!-- Consensus estimates (BBG, JPY) block auto-injected here by the HTML builder from _data/estimates.json — do NOT hand-write. Currency: JPY. -->

## In the inbox (Outlook — recent sell-side flow)
- _Outlook not reachable this session (Python alias not on PATH); no direct desk notes pulled. Coverage of TEL in the priority US inbox is thin (Japanese issuer) — exposure is via WFE-complex read-through (AMAT/LRCX/KLAC/ASML notes) captured in the [semicap-wfe](themes/semicap-wfe.md) theme and the 2026-06 briefings._
- _From the repo (relatórios bons):_ MS AI NAND overview (2025-09-10) names TEL among NAND-exposed Japanese SPE makers but stays relatively cautious on WFE (China + conservative NAND capex), preferring Advantest/Disco — sourced below.
- **SIG / Mehdi Hosseini — 2Q26 Asia tour (TEL call)** _(2026-06-18)_: TEL raised its WFE outlook — **~$150B for 2026, base-case ~$170B for 2027**; path to **$200B** would need faster NAND, faster advanced logic and/or extra memory-capacity additions (DRAM already looks robust, so upside skews to NAND + logic). DRAM the strongest conviction area: **tech migration yields only ~10% bit-growth vs mid-teens-to-~20% demand**, so capacity adds are required (underpins DRAM capex through 2027). NAND more conservative — a node migration alone generates **~30% bit-growth**, so TEL assumes NAND capex roughly flat in 2027; but importantly **now seeing actual NAND capacity additions** (at least two customers adding real capacity, vs four months ago expecting none) — not yet viewed as a sustained multiyear cycle. 3D-NAND layer count moving from **high-200s toward ~300 in 2027, some early ~400-layer**. **Cryo-Etch**: modest 2026 revenue, ≥1 customer to HVM in 2027 (~400-layer NAND); LT addressable market **~$1.5–2.0B, targeting ~50% share ($0.8–1.0B)**, working with all major non-China NAND makers. **GAA**: one major process-of-record (POR) position in a critical conductor-etch application, aiming to expand into more etch apps across future nodes. Visibility from **5–6 month equipment lead time** + customers signing **2–3 year agreements** into 2028 (9–12 months post-delivery to qualify/realize output). **China WFE ~low-$50B in 2026** (up from mid-$40B previously); not the principal 2027 driver, and Chinese-memory post-IPO investment is *not* in the $170B forecast (upside). Advanced logic (incl. TSMC next-gen nodes) the most likely source of upside beyond forecast. Pricing kept **yen-based** (annual resets, inflation/labor surcharges), not USD-linked (SIG "Susq Asia tour", 2026-06-18).
- **BofA (Hirokawa) — Japan SPE preview** _(2026-04-16)_: BofA is **cautious on the front-end (Tokyo Electron) near-term** — its house view is that the March-2026 quarter is the memory-pricing peak (NAND ASP +~70% q/q in Mar-Q, decelerating to ~30% in Jun-Q), and historically TEL's share price peaks within ~3 quarters of the memory-price-momentum peak. (BofA prefers back-end/DISCO over front-end as a result.) The bull counter is TrendForce's call for another +70-75% q/q NAND-pricing quarter in Jun-Q, which would extend TEL's strength (BofA "Japan SPE preview", 2026-04-16).
- **Jefferies (Wong) — Asia tech** _(2026-04-07)_: Tokyo Electron itself admits it is **conservative on WFE this year at +15%; "more like 20"**, and sees upside to China (had expected flat, now +10%, potentially more on CXMT/YMTC IPOs); ALD a tailwind as 16A/14A logic needs more single-layer ALD (Jefferies "Asia tech", 2026-04-07).

## Management commentary — evolution (last 2 quarters)

| Theme | Q3 FY26 (2026-02-06) | Q4 / FY26 (2026-04-30) |
|---|---|---|
| Quarterly sales / cadence | ¥552.0bn, −12.4% QoQ — timing-driven trough | ¥711.8bn, +28.9% QoQ rebound; FY26 record ¥2,443.5bn |
| Margins (GM / OPM) | GM 42.7% / OPM 21.0% — FY26 low point | GM 46.8% / OPM 28.9%; FY26 GM 45.3% (−1.8pts) |
| WFE / demand outlook | AI-server DRAM/HBM + advanced logic; WFE $150–170bn CY26–27 | Same $150–170bn; leading-edge +30%+; H1 FY27 SPE +41% YoY |
| SPE mix (non-mem/DRAM/NAND) | 56% / 36% / 8% | FY26 59% / 31% / 10% |
| NAND recovery | Early 3D-NAND recovery on fab utilization (8%) | NAND up to 10% (from 7%) — recovering |
| China / regional | China 31.8% — down on leading-edge skew | China 26.8% (Q4); FY26 34.1%, down from 41.7% |

_Source: TOKYOELEC earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** none — Japanese issuer (TSE Prime: 8035); no SEC filings exist.
- **Transcripts / IR:** [Q4 / full-year FY26 (2026-04-30)](../TOKYOELEC/transcripts/TOKYOELEC_Q4-FY26-earnings_2026-04-30.md) · [Q3 FY26 (2026-02-06)](../TOKYOELEC/transcripts/TOKYOELEC_Q3-FY26-earnings_2026-02-06.md). Compiled from Tokyo Electron IR English results deck + presenter script (tel.com IR) and the investing.com earnings-call summary; primary webcast not redistributable, figures attributed. Includes Gartner/TechInsights CY2025 market-share data (dated 2 April 2026, via TEL deck).
- **Research reports (relatórios bons):**
  - [Morgan Stanley — AI NAND overview](../relat%C3%B3rios%20bons/AI_Nand_overview_MS.html) (2025-09-10) — NAND-WFE intensity thesis (~18% flat-line through 2027), TEL among NAND-exposed Japanese SPE makers, CBA/wafer-bonding density lever, MS cautious on WFE vs Advantest/Disco.
  - [BofA — Japan SPE preview (Hirokawa, 2026-04-16)](../relat%C3%B3rios%20bons/2026_04_16_japan_spe_baml_16_apr_2026.html) — cautious on front-end/TEL near-term (Mar-Q memory peak → TEL share-price peak within ~3 quarters); prefers back-end/DISCO.
  - [Jefferies — Asia tech (2026-04-07)](../relat%C3%B3rios%20bons/2026_04_07_jef_asia_7_apr_2026.html) — TEL conservative on WFE +15% ("more like 20"); China flat → +10%; ALD tailwind at 16A/14A.
- **Equity calls:** WFE read-throughs — `../../../equity_calls_transcripts/Semis/2026-05-15_Harlan_semicap-AMAT.md`, `2026-05-28` JPM memory-China call (TEL prober/FormFactor reference in `_consolidado/TODOS_Semis.md`).
- **Briefings:** `E:\briefings\2026` — TEL datapoints in 2026-06-18 (memory rally +4.7%; President Kawai 3D-integration ¥300bn-by-2030, China ~30% and falling).
- **Outlook:** not pulled — Python alias unavailable this session.
- **Cross-theme:** [semicap-wfe](themes/semicap-wfe.md) · [hbm-memory](themes/hbm-memory.md).
