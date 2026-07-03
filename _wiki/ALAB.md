# ALAB — Astera Labs, Inc.

_Wiki · generated 2026-06-19 · sources: `E:\Wiki Felipe\ALAB` (filings + transcripts) · `E:\briefings\2026\*` · Master index: [00_INDEX.md](00_INDEX.md). Themes: [custom-asic-tpu](themes/custom-asic-tpu.md) · [optical-cpo](themes/optical-cpo.md). Note: IPO'd Mar-2024 — short filing history (~9 filings)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $1.5bn | $2.3bn |
| Gross profit | $1.1bn | $1.6bn |
| Gross margin | 72.3% | 71.1% |
| EBITDA | $534m | $839m |
| EPS | $2.91 | $4.39 |
| Capex | $52m | $74m |
| OCF (≈EBITDA) | $534m | $839m |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Fabless "Intelligent Connectivity Platform" supplier for AI/cloud infrastructure — purpose-built semiconductors that solve data, memory and networking bottlenecks inside the rack (FY25 10-K, 2026-02-20). Four product families on PCIe/Ethernet/CXL standards plus a COSMOS software suite: **Aries** PCIe/CXL Smart DSP retimers + smart cable modules (signal conditioning), **Scorpio** Smart Fabric Switches (P-Series scale-out, X-Series scale-up), **Taurus** Ethernet smart cable modules, and **Leo** CXL memory controllers. FY2025 revenue **$852.5M, +115% y/y**, non-GAAP GM **75.7%**, net income **$219.1M** vs. an $83.4M FY24 loss (10-K, 2026-02-20). The story is a pure AI-infrastructure connectivity play levered to hyperscaler capex, with **content per accelerator now >$1,000 and rising** and a stated SAM expanding ">10x over five years to $25B" (Mohan, Q4-2025 call, 2026-02-10). Extreme customer concentration: top-5 customers each 11–29% of revenue, manufacturing partners buying on behalf of end-hyperscalers (10-Q, 2026-05-06).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Aries PCIe/CXL retimers & smart cable modules · 2) Scorpio Smart Fabric switches (scale-up X / scale-out P) · 3) Taurus Ethernet AEC modules (+ Leo CXL) |
| **Main buyer(s)** | Hyperscalers (AWS, Microsoft, Google) buying via manufacturing partners; extreme concentration — top customer 29%, top-5 ~90% of revenue (10-Q, 2026-05-06) |
| **Key suppliers** | TSMC (sole foundry, all ICs); ASE / Amkor (assembly + test); substrate / module partners |

## Position in the value chain
Astera is a fabless designer sitting between the foundry/packaging supply base and the hyperscalers/AI-platform builders. It owns no fabs — **TSMC fabricates all ICs**, with ASE and Amkor for assembly/test (FY25 10-K, 2026-02-20) — and sells retimers, fabric switches, AECs and CXL controllers that attach to GPUs/XPUs (Nvidia, AMD, hyperscaler custom silicon) inside AI racks. The historical base is PCIe signal conditioning (Aries) for scale-out; the growth leg is **Scorpio scale-up fabric switching** (X-Series), guided to become the largest product line by Q4-2026 (Q1-2026 call, 2026-05-05), plus the 2027 UALink/optical/NVLink-Fusion roadmap. Astera, AVGO and MRVL all carry PCIe products (mostly scale-out today); Astera is best known for its retimers, while AVGO has held the majority of the PCIe switch market — Astera's Scorpio entry is the merchant challenge to that (MS Scale-up primer, J. Moore/Brett). Astera is also a named ASIC-side partner on Nvidia's NVLink Fusion alongside MediaTek/Marvell/Alchip/Synopsys/Cadence (MS Scale-up primer).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <rect x="0" y="0" width="720" height="220" fill="#ffffff"/>
  <!-- Suppliers -->
  <rect x="10" y="45" width="170" height="130" rx="8" fill="#eef3fb" stroke="#3b5ba9" stroke-width="1.5"/>
  <text x="95" y="68" text-anchor="middle" font-weight="bold" fill="#1f3a6e">Suppliers</text>
  <text x="95" y="94" text-anchor="middle">TSMC (sole foundry)</text>
  <text x="95" y="116" text-anchor="middle">ASE / Amkor</text>
  <text x="95" y="132" text-anchor="middle">(assembly + test)</text>
  <text x="95" y="156" text-anchor="middle">substrates / modules</text>
  <!-- ALAB -->
  <rect x="255" y="30" width="210" height="160" rx="8" fill="#fdeee6" stroke="#c0622a" stroke-width="2"/>
  <text x="360" y="52" text-anchor="middle" font-weight="bold" fill="#9c3d12">Astera Labs (fabless)</text>
  <text x="360" y="76" text-anchor="middle">Connectivity platform</text>
  <text x="360" y="98" text-anchor="middle">Aries PCIe/CXL retimers</text>
  <text x="360" y="118" text-anchor="middle" font-weight="bold" fill="#9c3d12">Scorpio scale-up fabric</text>
  <text x="360" y="138" text-anchor="middle">switches (growth leg)</text>
  <text x="360" y="160" text-anchor="middle">Leo CXL · Taurus AEC</text>
  <text x="360" y="180" text-anchor="middle">COSMOS software</text>
  <!-- Customers -->
  <rect x="540" y="45" width="170" height="130" rx="8" fill="#eaf6ee" stroke="#2f8f4e" stroke-width="1.5"/>
  <text x="625" y="68" text-anchor="middle" font-weight="bold" fill="#1d6b38">Customers</text>
  <text x="625" y="94" text-anchor="middle">Hyperscalers</text>
  <text x="625" y="112" text-anchor="middle">(AWS, Microsoft,</text>
  <text x="625" y="128" text-anchor="middle">Google + others)</text>
  <text x="625" y="152" text-anchor="middle">AI accelerators:</text>
  <text x="625" y="170" text-anchor="middle">Nvidia / AMD / custom</text>
  <!-- Arrows -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#555"/>
    </marker>
  </defs>
  <line x1="182" y1="110" x2="251" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="467" y1="110" x2="536" y2="110" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="360" y="210" text-anchor="middle" font-style="italic" fill="#444">>$1,000 content/accelerator; scale-up fabric (Scorpio X) the growth leg into UALink/optical 2027+</text>
</svg>

## Current state (latest quarter)
**Q1 2026 (calendar; reported 2026-05-05, qtr ended Mar 31, 2026):**
- Revenue **$308.4M**, +14% q/q, **+93% y/y**; above the $286–297M guide. GAAP op income $61.8M on $308.4M rev, GAAP GM 76.3% (10-Q, 2026-05-06). Non-GAAP EPS **$0.61**, non-GAAP GM **76.4%** (+70 bps q/q), non-GAAP op margin **36.2%** (transcript, 2026-05-05).
- Revenue +93% y/y driven by higher unit shipments of **Scorpio, Aries and Taurus** plus richer mix of hardware modules and Scorpio (10-Q, 2026-05-06).
- **PCIe Gen 6** now >1/3 of total revenue; "millions of Gen 6 ports shipped" (Mohan). **Scorpio X-Series (scale-up)** shipping initial production volumes; mgmt guides Scorpio to be the **largest product line by Q4-2026** (transcript, 2026-05-05).
- **Leo CXL** deploying on Microsoft Azure M-series; second CXL design win + a KV-cache custom controller win (ships 2027). Content per accelerator **>$1,000 and rising** (transcript, 2026-05-05).
- **Guidance:** Q2-2026 revenue **$355–365M (+15–18% q/q)**; non-GAAP GM ~73% (incl. ~200 bps drag from the Amazon warrant/customer agreement); non-GAAP EPS $0.68–0.70 (transcript, 2026-05-05).
- Customer concentration (Q1-2026, % of revenue): A 29% / B 21% / C 16% / D 12% / E 12% — several are manufacturing partners buying for end-hyperscalers (10-Q, 2026-05-06).

## Debate / thesis
- **Bull:**
  - **Scale-up inflection:** Scorpio X scale-up fabric switches now in production; UALink switches (higher ASP than PCIe) deploy 2027 alongside Amazon + AMD ASIC/GPU launches — the "key inflection point" narrative (Gajendra, 2026-05-05). MS (J. Moore) raised PT **$210 → $240, OW**, framed as "buy & ramp before the product cycle kicks in" (briefing 2026-05-06).
  - **Scale-up TAM is the new greenfield:** MS frames scale-up as a "greenfield opportunity virtually overnight" and models the scale-up market at a **34% CAGR 2024–2030 to ~$17bn**, with ALAB/AVGO/MRVL the merchant beneficiaries as non-Nvidia XPUs ramp; ALAB itself guides an incremental **$5bn scale-up TAM by 2030** (MS Scale-up primer, J. Moore/Brett). TD Cowen is bigger on the components layer: a scale-up components TAM (redrivers/retimers/switches) **>$67bn by 2030**, inside a >$155bn systems market — "underappreciated in its magnitude" (TD Cowen, 2026-03-11). Astera's own AI PCIe interconnect TAM is framed at **$1.6bn by 2027** (per JPM, 2025-10-17).
  - **Scorpio-X = Amazon Trainium attach, sized:** MS base case has Scorpio revenue **>doubling to $186mn in 2026 (~18% of total rev)**, of which **~70% (~$130mn) is Scorpio-X**, built on **650k Trainium units scaled-up with Scorpio, 25% attach, $800 ASP**; bull case puts scale-up at **$400mn / total rev $1.5bn** (MS Scale-up primer). The SemiAnalysis AWS Trainium3 teardown corroborates the socket: Trainium3 NL72x2 uses **184 scale-up switches per rack** across three switch generations (160-lane → 320-lane Scorpio-X PCIe Gen6 → 72+ port UALink end-state), plus **6 PCIe Gen6 x16 retimers per compute tray** and PCIe AECs cross-rack — Scorpio-X described as an "anchor socket" pulling in retimers/gearboxes (SemiAnalysis, 2025-12; MS). Barron's roundtable bull: Astera "essentially enables rack-scale computing for everyone else… the only real merchant alternative" for non-Nvidia ASICs, growing ~100% this year (Barron's Tech Roundtable).
  - **Content compounding:** >$1,000/accelerator and rising as optical (NPO 2027, CPO 2028) and custom (NVLink Fusion, KV-cache controllers) layer on; SAM ">10x to $25B over five years" (Mohan, 2026-02-10). BofA (Arya) PO change on "AI fabric ramp strengthening" (briefing 2026-05-06).
  - **Hyperscaler anchoring:** $6.5B cumulative Amazon warrant-linked purchase agreement (3.3M warrant shares) across switches/signal conditioning/optical engines (Tate, 2026-02-10); two new US-hyperscaler Scorpio design wins (2026-02-10); Scorpio P to two more hyperscalers late-2026. The Amazon structure is an equity-based rebate: warrants vest as AWS hits purchase milestones at a **$20.34 strike**, an effective ~23% discount on components by Sep-25 — "the more Amazon buys, the more they save" (SemiAnalysis, 2025-12). ALAB +16% the week into JPM TMC (top semis leader), presented Tue 10:05am (briefing 2026-05-19/05-20).
  - **"The way to play the Trainium trade" (Citi/Jefferies "Blaine," Asia recal, 2026-05-22):** with Trainium server production ~flat in Q2 (Trn2→Trn3 transition) and Blaine cautious that MRVL "doesn't get paid on all the units," he flags **Astera as the cleaner Trainium expression** — "there's a big trend on scale-up overall content-per-accelerator that is underestimated," and ALAB is "the way to play" it (while noting the stock has "gone crazy").
  - **JPM small-cap top pick + memory-tightness tailwind (JPM Sur, Semis Spring Series, 2026-05-29; JPM TMC feedback, 2026-05-22):** Sur keeps **ALAB an overweight top pick in mid-cap/small-cap semis**; at JPM's TMC conference Astera flagged **continued strong demand for fabric switching (within-rack) and copper AEC (scale-out)**, plus a *new* driver — **memory tightness + higher memory/storage intensity on inferencing workloads is creating fresh opportunities for ALAB's CXL- and PCIe-based switching** (memory-tiering/pooling) — a read-through that the DRAM shortage is pulling Leo/CXL content forward.
- **Bear:**
  - **Extreme customer concentration** — top customer 29%, top-5 ~90% of revenue, much of it through manufacturing partners that can shift volumes (10-Q, 2026-05-06). Binary on design wins.
  - **Scale-up switching is getting crowded:** TD Cowen rates **ALAB Hold (target $116.48 area; rating history $200→$225→$170)**, flagging that Scorpio X "in direct competition with Broadcom's historically very strong Ethernet switching and Marvell's increasingly competitive merchant UALink switch offerings"; Marvell's Celestial AI + XConn acquisitions and Upscale AI launches make merchant UALink switching "increasingly competitive" — a headwind for ALAB while a growth option for MRVL (TD Cowen, 2026-03-11). Within Trainium3, AWS explicitly dual-tracks: Broadcom PEX90144 (144-lane, 72-port) is provisioned as a backup if the 160-lane Scorpio-X is unavailable (SemiAnalysis, 2025-12).
  - **Competitive encroachment in signal conditioning / AEC:** JPM (Harlan Sur) frames Astera as a "qualified second-source" at Amazon that has gained AEC share into the **low/mid-teens (~14%)** but Credo still holds **~80%** of AEC share; CRDO's single-vendor (module + cable) accountability vs. Astera's silicon/paddle-card model is a structural edge (JPM Credo, 2025-10-17). Hyperscaler-captive and merchant switch competition (AVGO Tomahawk scale-out; GCP using OCS for scale-up) caps parts of the opportunity (briefing 2026-05-20).
  - **Optical positioning skepticism:** R&Co Redburn (Harrison) "Tripping the Light Fantastic" rated **ALAB Neutral** alongside CIEN, vs Buys on LITE/COHR/CLS/CRDO (briefing 2026-05-18/05-19) — i.e. less optical conviction than pure-plays. ALAB's NPO/CPO is a 2027/2028 story.
  - **Trainium time-to-market retimers may de-spec:** AWS's cableless compute-tray design uses "a few inexpensive retimers… designed in to de-risk" the initial ramp; after a successful first deployment AWS "can potentially remove some of the retimers" — i.e. early content is partly transient (SemiAnalysis, 2025-12). Trainium itself remains "significantly lower performance than merchant GPUs," so the scale-up upside is levered to AWS architectural choices and Trainium volumes (MS Scale-up primer).
  - **Valuation/momentum:** AI-semis at ~5σ momentum, 62% above 200dma; buyside reframing the supply chain as a "quarter-by-quarter revision trade, not a multi-year hold" (briefing 2026-05-17). ALAB screens at a premium — ~32.5x EV/S NTM vs ~20x ex-Credo peer average (JPM Credo comps, 2025-10-17). GM headwind from richer hardware-module mix + warrant accounting.
- **Where the sell-side stands (from notes/briefings):** **MS (J. Moore) OW, PT $240** (raised from $210, 2026-05-06; the earlier scale-up primer carried OW PT $200). **BofA (Arya)** positive PO change on AI fabric ramp (2026-05-06). **JPM (Sur)** held rating, "strong R/G driven by AI demand" (2026-05-06); JPM's Credo work casts ALAB as the share-taker chasing Credo's AEC lead (2025-10-17). **TD Cowen Hold** on scale-up-switching competition, but flags NVLink-Fusion attach on Trainium 4 as material upside ~2028/2029 (2026-03-11). **R&Co Redburn (Harrison) Neutral** on optical framing (2026-05-18).

## Catalysts / what to watch
- **Q2-2026 print: ~early Aug 2026** — watch the $355–365M guide (+15–18% q/q), Scorpio X scale-up ramp, and confirmation Scorpio becomes #1 product line by Q4.
- **Conferences:** Jefferies Chicago Semis Conf (Aug 24–25, 2026) — ALAB confirmed presenter (briefing 2026-05-15).
- **2026:** Scorpio P to "two additional major hyperscalers" late-2026; Leo CXL Azure M-series production volumes. Scorpio-X ramp tied to Trainium3 NL32x2/NL72x2 (160-lane Gen6 switch first, then 320-lane) (SemiAnalysis, 2025-12).
- **2027 roadmap:** UALink-based switch deployments (higher ASP, lower latency than PCIe); Amazon + AMD ASIC/GPU launches; NVLink Fusion hybrid-rack revenue; PCIe Gen 7; 1.6T Taurus Ethernet; NPO volume. **2028:** CPO deployment. **2028/2029:** TD Cowen sees NVLink-Fusion attach on Amazon Trainium 4 as a re-acceleration driver (2026-03-11).
- Amazon $6.5B warrant agreement tranche progress (non-cash GM drag begins Q2-2026; $20.34 warrant strike).

## Risks
- **Customer concentration** — limited number of end customers drive revenue (top customer 29%; 10-Q 2026-05-06); orders flow through manufacturing partners that can reallocate volumes. Loss/slip at one hyperscaler is material.
- **Design-win dependence** — revenue swings on timing/number of multi-year, binary design wins (FY25 10-K).
- **Sole-foundry / supply** — TSMC fabricates **all** ICs; ASE/Amkor assembly/test; small set of module/substrate partners (FY25 10-K). No second source.
- **Standards risk** — products built on PCIe/CXL/Ethernet/UALink; UALink in early adoption (ratified 2025, no products shipping yet per MS primer) — if competing standards win or peers diverge, demand suffers (FY25 10-K).
- **Competition** — Credo (~80% AEC share vs ALAB ~14%; JPM 2025-10-17), Broadcom (scale-out switching + PEX90144 Trainium backup), Marvell (merchant UALink + Celestial AI/XConn), captive hyperscaler/COT silicon; ASP erosion + possible Trainium retimer de-spec over product life (FY25 10-K; SemiAnalysis 2025-12; TD Cowen 2026-03-11).
- **Margin mix / accounting** — richer hardware-module + Scorpio mix dilutes GM (75.7% FY25, -70 bps y/y); Amazon warrant non-cash charge hits GM from Q2-2026.
- **Macro / AI-capex cyclicality & valuation** — pure-play on hyperscaler AI capex at stretched momentum and premium multiple (~32.5x EV/S NTM); "revision trade" risk (briefing 2026-05-17; JPM comps 2025-10-17).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **Morgan Stanley (J. Moore)** _(2026-05-06)_: **Overweight, PT $240** — scale-up connectivity (Scorpio) the growth leg.
- **TMTB 'JPM TMT Conf Key Quotes (INTC, ALAB, ANET, DDOG)'** _(2026-05-19)_ + **Rothschild TMT Daily (Adley)** _(2026-05-20)_: ALAB/CRDO in focus; **Redburn Neutral** ('Tripping the Light Fantastic') the cautious counter.

## Intra-quarter — calls, commentary & reports

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Product / Scorpio scale-up** | X-Series in production; #1 revenue line by Q4'26 | BTG/LightCounting (Bob): Scorpio X "ramping now", which will "explode" in the near-term; the new product quickly becomes the largest contributor | **✓ confirms** (timing aligned) |
| **Demand / Amazon** | Content >$1,000/accelerator and rising; 2027 ramp (UALink, AMD/Amazon) | BTG: ALAB "extremely well positioned" in scale-up switched, led by Amazon | **✓ confirms** (Amazon the anchor) |
| **Competition / AEC** | — (Aries/Taurus AEC scale-out) | BTG: ALAB has already taken AEC share at Amazon (Credo dominant); "bright future" for AECs | **⚠ nuance** (Credo still ~dominant) |
| **Valuation** | (n/a — management does not comment on the multiple) | BofA/Arya: PO $200→$240 but **stays NEUTRAL** (66x CY27E P/E) | **⚠ nuance** (multiple caps upside) |

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-13 | BofA · Vivek Arya | valuation | neutral | **PO $200 → $240, stays NEUTRAL** (66x CY27E P/E), at the near-high of high-growth compute/optical peers (18x-66x) but in line with the 0.5x EV/S-to-sales-CAGR framework given ALAB's superior growth. Downside risks: delays/changes at Amazon, competition from MRVL/AVGO, slow UALink/AEC adoption. (BofA "AI 2030", 2026-05-13) — _consistent with the positive BofA PO change recorded on 05-06._ |
| 06-19 | Nutty "Optics Primer" (nuttycld.substack.com, 2026-06-19) | product | bull | Nutty's CPO/silicon-photonics primer mentions ALAB in the optical connectivity context (brief mention). Astera Labs is positioned as a connectivity fabric specialist at the scale-up layer; the primer's broader CPO thesis — that inside-the-rack optical fabric is the next step-up in AI cluster connectivity — is directionally consistent with ALAB's Scorpio scale-up switched-fabric roadmap. No ALAB-specific new data in the primer. (Nutty "Optics Primer", nuttycld.substack.com, 2026-06-19) |
| 06-25 | BTG · LightCounting call | product | bull | Expert (Bob): scale-up switching + scale-up CPO are what will "explode" in the near-term, starting with **Astera Labs Scorpio X ramping now**. ALAB "extremely well positioned" in the transition to scale-up switched architectures, led by the **Amazon** business; a "more dynamic" small-cap, with a new product that quickly becomes the largest revenue contributor. The alternative technology = scale-up Ethernet (where Broadcom leads) — two approaches competing. In AEC, ALAB has already taken a slice at Amazon (Credo still dominant); the expert sees a **bright future for AECs** (rack-to-rack, replacing passive DAC). (BTG "LightCounting", 2026-06-25) |

**Quarter synthesis:** the flow confirms management's scale-up thesis (Scorpio X ramping, Amazon the anchor) — the debate migrated from demand to the **share price**: BofA endorses the fundamentals but locks at NEUTRAL on the multiple (66x), and the only remaining operational nuance is the still-subordinate position in AEC vs Credo.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2'25 (2025-08-05) | Q3'25 (2025-11-04) | Q4'25 (2026-02-10) | Q1'26 (2026-05-05) |
|---|---|---|---|---|
| Revenue / growth | $191.9M, +20% q/q, +150% y/y | $230.6M, +104% y/y | $270.6M, +17% q/q; FY25 $852.5M +115% | $308.4M, +14% q/q, +93% y/y |
| Gross margin (non-GAAP) | ~75% (Q3 guide) | — | 75.7%, -70 bps q/q on hardware mix | 76.4%, +70 bps; Q2 ~73% on Amazon drag |
| Scorpio fabric (scale-up) | P-Series ramped to volume production | P-Series volume; X-Series early ramp | P-Series >15% of revenue; X-Series initial ship | X-Series in production; #1 line by Q4'26 |
| Aries / PCIe Gen 6 | Gen 6 retimers ramping | Gen 6 retimer ramp continues | Aries +~70% y/y; Gen 6 high volume | Millions of Gen 6 ports; Gen 6 >1/3 of rev |
| Leo CXL memory | — | — | Azure M-Series win; volumes 2026 | Azure M-series live; 2nd win + KV-cache win |
| Content / TAM | — | — | SAM >10x to $25B in 5yrs | Content >$1,000/accelerator and rising |

_Source: ALAB earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY2025 (2026-02-20)](../ALAB/ALAB_10-K_2026-02-20_0001736297-26-000010.html); [10-Q Q1-2026 (2026-05-06)](../ALAB/ALAB_10-Q_2026-05-06_0001736297-26-000020.html).
- **Transcripts:** [Q1-2026 (2026-05-05)](../ALAB/transcripts/ALAB_Q1-2026-earnings_2026-05-05.md); [Q4-2025 (2026-02-10)](../ALAB/transcripts/ALAB_Q4-2025-earnings_2026-02-10.md); [Q3-2025 (2025-11-04)](../ALAB/transcripts/ALAB_Q3-2025-earnings_2025-11-04.md); [Q2-2025 (2025-08-05)](../ALAB/transcripts/ALAB_Q2-2025-earnings_2025-08-05.md). (Two latest read in full; Q3/Q2 saved as summary captures.)
- **Research reports (relatórios bons):**
  - [Morgan Stanley — Scale-up Networking Primer (ALAB/AVGO/MRVL)](../relat%C3%B3rios%20bons/Scale_up_primer_MS.html)
  - [TD Cowen — Optical / Scale-up Networking (ALAB Hold)](../relat%C3%B3rios%20bons/TDCOWEN.html)
  - [J.P. Morgan — Credo: Leverage to Rising Interconnect (2025-10-17)](../relat%C3%B3rios%20bons/JPM_Credo_Leverage_to_Ri_2025-10-17_5103388.html)
  - [Barron's — Tech Roundtable: 4 Experts on the Next Phase of AI + 22 Favorite Stocks](../relat%C3%B3rios%20bons/Barrons_Tech_Roundtable__Our_4_Experts_on_the_Next_Phase_of_AIand_22_Favorite_Stocks_-_Barrons.html)
  - [SemiAnalysis — AWS Trainium3 Deep Dive: A Potential Challenger Approaching](../relat%C3%B3rios%20bons/AWS_Trainium3_Deep_Dive___A_Potential_Challenger_Approaching.html)
  - [JPM (Harlan Sur) — Semis Spring Series / TMC feedback (2026-05-29 & 2026-05-22)](../relat%C3%B3rios%20bons/2026_05_29_jpm_semis_29_may_26.html) — ALAB OW small-cap top pick; fabric-switch + AEC demand; memory-tightness pulling CXL/PCIe-switch opportunities forward.
  - [Citi/Jefferies (Blaine) — Asia recal call (2026-05-22)](../relat%C3%B3rios%20bons/2026_05_22_jef_asia_recal_call_22_may_2026.html) — ALAB "the way to play the Trainium trade"; scale-up content-per-accelerator underestimated.
  - [BofA (Vivek Arya) — "AI 2030: Stronger for Longer" (2026-05-13)](../relat%C3%B3rios%20bons/Vivek_State_of_the_union.html) — ALAB PO $200→$240, mantém NEUTRAL (66x CY27E); riscos Amazon/competição MRVL-AVGO/UALink.
  - [BTG — LightCounting optics/CPO expert call (2026-06-25)](../relat%C3%B3rios%20bons/BTG_LightCounting_Optics_Expert_Call_2026-06-25.html) — Scorpio X ramping now; ALAB "extremely well positioned" in scale-up switching (Amazon); the new product becomes the largest revenue contributor; bright future for AECs.
- **Themes:** [custom-asic-tpu](themes/custom-asic-tpu.md) (custom/NVLink-Fusion attach to hyperscaler XPUs); [optical-cpo](themes/optical-cpo.md) (NPO 2027 / CPO 2028; ALAB rated Neutral vs optical pure-plays).
- **Briefings:** `E:\briefings\2026\` — 2026-05-06 (MS PT $240 OW; BofA/JPM), 2026-05-11/05-12 (CRDO/AEC competition), 2026-05-15 (Jefferies conf), 2026-05-17/05-18/05-19/05-20 (JPM TMC, R&Co optical Neutral, +16% wk).
- **Outlook / sell-side notes:** Outlook/MAPI not available in this environment — no live email flow pulled. Sell-side attribution above is from on-disk briefings + research reports only.
