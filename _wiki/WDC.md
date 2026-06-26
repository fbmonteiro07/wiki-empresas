<!-- Per-company wiki page. Synthesis of co-located disk sources only. -->

# WDC — Western Digital

_Wiki · generated 2026-06-19 · sources: `E:\Wiki Felipe\WDC` (filings + transcripts) · `_equity_calls` · `_briefings`. Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof 2026-06-22 · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $15.1bn | $20.6bn |
| Gross profit | $7.9bn | $11.9bn |
| Gross margin | 52.2% | 58.0% |
| EBITDA | $6.8bn | $11.0bn |
| EPS | $13.52 | $21.57 |
| Capex | $632m | $849m |
| OCF (≈EBITDA) | $6.8bn | $11.0bn |

<svg xmlns="http://www.w3.org/2000/svg" width="326" height="88" viewBox="0 0 326 88" font-family="-apple-system,Segoe UI,Roboto,sans-serif"><text x="0" y="10" font-size="11" font-weight="600" fill="#33405c">FY1 EPS revision</text><rect x="0" y="23.8" width="20" height="34.2" rx="2" fill="#1c5fd6"/><text x="10" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="28" y="18.3" width="20" height="39.7" rx="2" fill="#1c5fd6"/><text x="38" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="56" y="14.0" width="20" height="44.0" rx="2" fill="#1c5fd6"/><text x="66" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="84" y="14.0" width="20" height="44.0" rx="2" fill="#1c7d3f"/><text x="94" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="0" y="84" font-size="10" fill="#1c7d3f">+10.7% 3m · +28.8% 6m</text><text x="176" y="10" font-size="11" font-weight="600" fill="#33405c">FY2 EPS revision</text><rect x="176" y="34.4" width="20" height="23.6" rx="2" fill="#1c5fd6"/><text x="186" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="204" y="24.5" width="20" height="33.5" rx="2" fill="#1c5fd6"/><text x="214" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="232" y="15.2" width="20" height="42.8" rx="2" fill="#1c5fd6"/><text x="242" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="260" y="14.0" width="20" height="44.0" rx="2" fill="#1c7d3f"/><text x="270" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="176" y="84" font-size="10" fill="#1c7d3f">+31.2% 3m · +86.5% 6m</text></svg>

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Western Digital is now a **pure-play hard disk drive (HDD) company** after spinning off its Flash/NAND unit as SanDisk on **February 21, 2025** (FY25 10-K, 2025-08-14). It develops and manufactures substantially all of its own recording heads and magnetic media, selling capacity-enterprise (nearline) drives into three end markets — **Cloud, Client, Consumer** — but the business is now overwhelmingly a hyperscaler mass-storage story: **Cloud was 89% of revenue** in fiscal Q3 FY26 (10-Q for period ended 2026-04-03; Q3 FY26 call, 2026-04-30). It is one of three scaled HDD makers alongside Seagate and Toshiba (FY25 10-K). The thesis: HDDs remain the lowest-TCO medium for the petabyte-to-exabyte "cold/warm" tier that the AI data buildout is inflating — management frames long-term storage demand at **>25% CAGR** with exabyte shipments +34% y/y last quarter (Q3 FY26, 2026-04-30). Differentiation runs on areal-density transitions: ePMR/OptiNAND/UltraSMR today, **HAMR** (heat-assisted magnetic recording) for the 44TB+ → 100TB+ roadmap.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Nearline/capacity-enterprise HDDs (Cloud, 89% of rev) · 2) Client HDDs · 3) Consumer storage |
| **Main buyer(s)** | Hyperscalers / cloud (89% of revenue); concentrated — top 10 customers = 71% of revenue |
| **Key suppliers** | Recording heads/media in-house; upstream glass substrates (Hoya), magnetic suspensions/heads (TDK), motors/actuators/controllers |

## Position in the value chain
WDC is the manufacturing integrator in the HDD chain: it builds its own heads and media in-house (vertical integration) and assembles drives, then sells nearline/capacity-enterprise HDDs to hyperscalers and enterprise. Post-SanDisk spin it is **pure HDD** — no NAND/Flash — so it is the cost-of-bits alternative to (not a participant in) the NAND complex. Customers are concentrated: top 10 = 71% of revenue (10-Q, 2026-04-03). It sits in a 3-player oligopoly; on Bernstein's count, revenue share is **WDC 45% / Seagate 41% / Toshiba 14%** (Bernstein HDD, 2025-10-23).

The competitive structure has "fundamentally changed from a shrinking industry to a growing one": the HDD sub-segments ripe for NAND cannibalization (2.5" PC-grade, mission-critical) are already mostly cannibalized, and the NAND-vs-HDD price gap has **stabilized at ~6-7x** for business-critical/nearline — which Bernstein reads as peak NAND data-center penetration (~24%) now behind us, reinforcing HDD as the lowest-cost "cool" data tier and projecting **business-critical HDD revenue to grow at ~17% CAGR 2024-30** (Bernstein HDD, 2025-10-23). Supply-chain checks corroborate the cost gap at **6-8x** and note inference servers "don't need HDD anyway" so eSSD is not a near-term cannibalization threat — the relevant battleground is AI data-storage (Jefferies/Q425 Techknowledge, 2025-12-17).

**Capacity is supply-disciplined and bottlenecked upstream.** Both WDC and STX meet exabyte demand by raising areal density rather than building new HDD factories; growth is gated by components — glass substrates (Hoya: ~3.5" utilization still <80%, "no intent to increase capacity") and especially **magnetic suspensions/heads**, flagged as the "main bottleneck" (TDK expanding suspension capacity +15% q/q). WDC is moving **from 10 to 12 platters** per drive to push capacity-per-unit; supply-chain order visibility had CY2026 and CY2027 already "sold out" and a 3-4 year upcycle on undersupply (Jefferies/Q425 Techknowledge, 2025-12-17).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif" font-size="12">
  <rect x="10" y="40" width="170" height="120" rx="6" fill="#eef3fb" stroke="#3b6ea5"/>
  <text x="95" y="62" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="95" y="84" text-anchor="middle">Recording heads / media</text>
  <text x="95" y="102" text-anchor="middle">(mostly in-house)</text>
  <text x="95" y="124" text-anchor="middle">Components: motors,</text>
  <text x="95" y="140" text-anchor="middle">actuators, controllers</text>
  <rect x="265" y="30" width="190" height="140" rx="6" fill="#dcece0" stroke="#2e7d4f"/>
  <text x="360" y="54" text-anchor="middle" font-weight="bold">WDC (pure HDD)</text>
  <text x="360" y="78" text-anchor="middle">Nearline / datacenter</text>
  <text x="360" y="94" text-anchor="middle">mass storage</text>
  <text x="360" y="116" text-anchor="middle">ePMR · UltraSMR · HAMR</text>
  <text x="360" y="138" text-anchor="middle" font-style="italic">post-SanDisk spin</text>
  <text x="360" y="154" text-anchor="middle" font-style="italic">(Flash divested 2025)</text>
  <rect x="540" y="40" width="170" height="120" rx="6" fill="#fbeee9" stroke="#a5613b"/>
  <text x="625" y="62" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="625" y="84" text-anchor="middle">Hyperscalers / cloud</text>
  <text x="625" y="100" text-anchor="middle">(nearline, ~89% rev)</text>
  <text x="625" y="124" text-anchor="middle">Enterprise storage,</text>
  <text x="625" y="140" text-anchor="middle">smart video, client</text>
  <line x1="180" y1="100" x2="262" y2="100" stroke="#555" stroke-width="2" marker-end="url(#ah)"/>
  <line x1="455" y1="100" x2="537" y2="100" stroke="#555" stroke-width="2" marker-end="url(#ah)"/>
  <defs>
    <marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 z" fill="#555"/>
    </marker>
  </defs>
</svg>

## Current state (latest quarter)
**Q3 FY26 (reported 2026-04-30) — a beat-and-raise.** Revenue **$3.3B, +45% y/y**, above the high end of guide; non-GAAP EPS **$2.72** (~2x y/y); non-GAAP gross margin **50.5%** (+1,040bps y/y, +440bps q/q); operating margin 38.6%; FCF $978M. Cloud $3.0B (89% of rev), +48% y/y. Volume **222 exabytes, +34% y/y**; pricing per TB **+9% y/y** on "better TCO value." The 10-Q (period ended 2026-04-03) attributes the +45% to a **34% rise in exabytes sold plus a 9% ASP/TB increase** "across all end markets." Net cash positive (~$450M) after SanDisk monetization cut $3.1B of debt. **No planned increase to unit capacity** — growth is areal-density + capacity-mix driven (Q3 FY26 call).

**Guidance — Q4 FY26:** revenue **$3.65B ±$100M** (~40% y/y at midpoint), gross margin **51–52%**, EPS **$3.25 ±$0.15** (Q3 FY26 call, 2026-04-30). Dividend raised 20% to $0.15/share; $752M buyback in the quarter.

**Technology:** HAMR now in qualification with **four customers** (44TB drives; roadmap >100TB); 40TB ePMR in qual with three customers, volume H2 2026; UltraSMR adopted by the three largest customers (Q3 FY26 call). LTAs now extend into **CY2028–2029**, structured as exabyte-volume commitments with pricing that may reset on new-capacity introductions — a notable lengthening vs Q2's "sold out for CY26 / agreements through CY27-28" framing (Q2 FY26 call, 2026-01-29).

## Debate / thesis
- **Bull:** A structurally elongated cycle, not a normal one. MS's **Erik Woodring** (equity call, 2026-06-16) raised numbers "materially again" on Asia checks: demand is broadening from core cloud to AI training/inference, humanoids and robots; supply is capped at ~30-35% annual exabyte growth, so the imbalance *elongates* the cycle rather than adding near-term volume. The punchline is **pricing**: HDD vendors are *targeting* ~$25/TB blended nearline in CY27 and ~$30 in CY28 vs ~$14.50/TB today — potential to roughly double pricing in two years via sequential escalators; non-LTA customers are already paying ~+30% q/q and distributor/NeoCloud "spot" is $30-35/TB. Woodring's WDC CY27/CY28 EPS would be "a little over $45 and a little over $70" if checks held — sub-10x on CY28. WDC has the **cleaner balance sheet and leading share** longer-term (Woodring, 2026-06-16). Corroborating: HDDs running ~90% sequential incremental gross margins and managing price up "on a steady basis," no longer giving back generation-change discounts in a supply-constrained market (JPM/Samik via [hbm-memory theme](themes/hbm-memory.md), 2026-06-12). JPM's TMC-conference read adds that **pricing is the biggest incremental upside** — neither WDC nor Seagate tried to temper price-increase expectations, and from WDC's current ~+9% q/q level "mid-teens pricing increases in 12 months' time… could be" — but WDC is more **price-driven** (cost declines limited to ~−10%/exabyte) vs Seagate's more cost-driven mix (faster cost declines on HAMR), so the revenue/cost-per-exabyte gap widens for both from different sources; both reiterated **no unit-capacity adds** (areal-density-only growth) (JPM "Networking", 2026-05-26). MS US-semis (Joe Moore, MS AI NAND overview, 2025-09-10) had earlier flagged the read-through: **OW on both WDC (Top Pick) and STX** as "a rising tide lifts all boats" so long as the **6-8x TCO differential** between HDDs and SSDs holds; 2026e EPS for the OW names ran ~26% above consensus.
- **Bear:** (1) **Tactical second-fiddle to Seagate** — Woodring keeps Seagate as top pick: STX reprices its Google HAMR "sweetheart" contract higher into Sept-26 and ramps 40TB HAMR in 2H CY26, whereas **WDC hasn't qualified HAMR yet** and ramps 44TB only in H1 CY27, so WDC lacks the same near-term pricing/GM juice (Woodring, 2026-06-16). Bernstein frames the same gap structurally: **WDC lags STX by ~2 years in HAMR** because it hedged on ePMR rather than going all-in, an "incorrect technology bet" that pressures both share and margin as it catches up; Bernstein models WDC 5yr EPS CAGR of only **17% vs STX 31%**, and GM expansion of just **39.6%→43.2% (FY25-30) vs STX 35.8%→51.9%** — hence Market-Perform, with the STX premium justified (Bernstein HDD, 2025-10-23). Supply-chain checks are blunter: **"WDC too optimistic on HAMR for 2027"** — Seagate took a long time to get HAMR right and high-volume HAMR "is not easy" (Jefferies/Q425 Techknowledge, 2025-12-17). **Counter-view (JPM, Semic Chatterjee, 2026-04-09):** the HAMR-lag worry is "probably a bit too much in focus" — customers don't care day-to-day whether a drive is HAMR or ePMR (they care about capacity/features), and WDC has a **well-cost-optimized ePMR platform extendable to ~60TB**, so the cost disadvantage of being behind on HAMR is smaller than imagined; near-term Seagate gets the GM benefit of ramping HAMR Gen-2, but **longer-term the two converge** (WDC's higher GM is offset by higher R&D/opex intensity from running multiple platforms + high-bandwidth-drive innovation) — "not much to pick between the two" on operating margin (JPM "HDD", 2026-04-09). (2) **Above-trendline shipments / shadow-order risk** — UBS (Arcuri) cautions HDD volume shipments are already above the long-term demand trendline, which could incentivize key customers to place "shadow" orders they don't ultimately need, plus accelerated eSSD replacement on power/energy efficiency (UBS 2026 overview, 2025-12-22). (3) **Valuation re-rating risk** — the gap to memory is the running buy-side argument *for* HDD, but FinTwit bears (@MF_Camillus, briefings 2026-06-16/19) flip it: "HDD TCO advantage overstated; the 40x+ vs HDD valuation gap is an aberration" that resolves toward DRAM/SSD. (4) **Peak-earnings optics** — if exabyte/order growth decelerates while EPS is still rising, the multiple de-rates regardless (Woodring, 2026-06-16). (5) Substitution from flash in lower-capacity/legacy form factors as NAND scales (FY25 10-K).
- **Where the sell-side/buy-side stands:** **MS (Woodring) Overweight on both HDDs, Seagate top pick, WDC 1B** — both at ~11-12x earnings on bull numbers (2026-06-16). **Bernstein (Newman) Market-Perform, PT $120** (16x CY27 EPS $7.53), raised from $96/13x at his 2025-09-15 sector initiation; prefers STX (Outperform, PT $275) over WDC on HAMR leadership (Bernstein HDD, 2025-10-23; Bernstein initiation, 2025-09-15). **UBS (Arcuri) Neutral, PT $145** — benign HDD market with disciplined capacity, but UBS out-year EPS sit ~7% (FY+1) to ~21% (FY+2) *below* consensus, reflecting its above-trendline/eSSD caution (UBS 2026 overview, 2025-12-22). WDC repeatedly on Rothschild's **12-month relative-high** screen (briefings 2026-06-17/18) alongside STX, AMAT, ASML. WDC is a standing name in **BofA/Fenske's "REAL bogey poll"** (true buy-side ests) for storage/memory (briefings 2026-05-11/15). No on-disk Outlook desk notes specific to WDC this window (see Sources).

## Catalysts / what to watch
- **Q4 FY26 print** (next earnings, ~late July 2026): guide $3.65B / 51-52% GM / $3.25 EPS — watch GM trajectory toward the next leg and any CY27/28 LTA pricing disclosures.
- **HAMR qualification** — conversion of the four customers in qual to volume; 44TB ramp timing (H1 CY27 per Woodring) is the gating item vs Seagate's 2H-CY26 40TB ramp. Note WDC pulled one HAMR customer qual forward to **1H26** and may bridge the gap with another ePMR generation (UBS 2026 overview, 2025-12-22); supply chain remains skeptical 2027 HAMR is achievable (Jefferies/Q425 Techknowledge, 2025-12-17).
- **Platter / areal-density transitions** — the 10→12 platter move (Jefferies/Q425 Techknowledge, 2025-12-17) is a near-term capacity-per-unit lever independent of HAMR.
- **LTA pricing resets** — CY27/CY28 contract pricing (escalators toward the $25/$30/TB targets) is the single biggest EPS swing factor (Woodring, 2026-06-16).
- **SanDisk stake monetization** — residual shares to be cleared (debt-for-equity swaps); de-levering progression.
- Exabyte demand breadth — confirmation that AI training/inference/physical-AI sustains the >25% storage CAGR. See storage-demand read-through in [hbm-memory](themes/hbm-memory.md) and [ai-datacenter-power](themes/ai-datacenter-power.md).

## Risks
- **Technology-transition execution** — failure to ramp HAMR cost-effectively (FY25 10-K explicitly flags the HAMR areal-density transition as a key risk); WDC is behind Seagate on HAMR qualification by ~2 years (Bernstein HDD, 2025-10-23; Woodring, 2026-06-16), and supply-chain checks doubt the 2027 timeline (Jefferies/Q425 Techknowledge, 2025-12-17).
- **Customer concentration** — top 10 = 71% of revenue (10-Q, 2026-04-03); hyperscaler capex/spending plans drive demand (FY25 10-K).
- **Above-trendline / shadow orders** — shipments already above the long-term demand trendline; risk that customers place orders they don't ultimately need, plus accelerated eSSD replacement on power/efficiency (UBS 2026 overview, 2025-12-22).
- **ASP / demand cyclicality** — "highly competitive industry subject to variations in ASPs and demand"; systems-demand volatility has an exaggerated effect on component demand (FY25 10-K). Peak-pricing optics if exabyte growth decelerates.
- **Flash substitution** — flash-based solutions compete in lower-capacity, smaller-form-factor and legacy markets as NAND scales (FY25 10-K); the relevant guardrail is the ~6-8x HDD-vs-eSSD cost gap holding (MS AI NAND overview, 2025-09-10; Jefferies/Q425 Techknowledge, 2025-12-17).
- **Macro / tariffs / China** — demand and pricing influenced by macro factors including tariffs and recession risk (FY25 10-K).
- **Separation overhang** — newly standalone HDD cost/capital structure; residual SanDisk-stake disposition (FY25 10-K).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **Morgan Stanley (Erik Woodring) — 'HDDs: The Next Leg Higher'** _(2026-06-15)_: HDD pricing-upside idea (Industry View Cautious, but the long thesis is nearline pricing).
- **Erik Woodring expert-call recap** _(2026-06-16)_: HDD pricing upside + server strength (WDC/STX, Dell/HPE, Apple cycles).

## Intra-quarter — calls, commentary & reports (since the last print)
_Q3 FY26 print + intra-quarter · Apr 30 → Jun 23, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q3 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Pricing (ASP/TB)** | +9% YoY on "better TCO"; no increase in unit capacity | JPM (TMC): pricing is the biggest incremental upside, "mid-teens in 12 months" from the current ~+9% level; neither WDC nor Seagate tempered it · MS Woodring: targets ~$25/TB CY27, ~$30 CY28 vs ~$14.50 today | **✓ confirms** (pricing is the thesis, with upside) |
| **Cloud / exabyte demand** | Cloud $3.0B (89%, +48% YoY); 222 EB (+34% YoY) | MS Woodring: demand broadening from cloud to AI training/inference, humanoids; supply capped at ~30-35% growth, elongating the cycle | **✓ confirms** (demand broadening) |
| **HAMR / roadmap** | HAMR in qual with 4 customers (44TB); ramp H1 CY27 | MS Woodring keeps Seagate as top pick (WDC 1B): WDC has not yet qualified HAMR, only ramps 44TB in H1 CY27 — behind Seagate | **⚠ nuance** (HAMR lag is the tactical gap) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-26 | JPM (Networking) | margin | bull | JPM (read from the TMC conference): pricing is the biggest incremental upside — neither WDC nor Seagate tried to temper price-increase expectations; from the current ~+9% QoQ level, 'mid-teens increases in 12 months could be.' WDC is more price-driven (cost declines limited to ~-10%/exabyte) vs Seagate more cost-driven; both reiterated no unit additions (growth only via density). |
| 06-15 | Morgan Stanley · Erik Woodring ('HDDs: The Next Leg Higher') | margin | bull | Pricing upside idea in nearline (Industry View Cautious, but the long thesis is pricing). HDD vendors targeting ~$25/TB blended in CY27 and ~$30 in CY28 vs ~$14.50/TB today; non-LTA customers already paying ~+30% QoQ and NeoCloud spot at $30-35/TB. |
| 06-16 | Morgan Stanley · Erik Woodring (equity call) | margin | mixed | Woodring raised numbers 'materially again' on Asia checks: demand broadening from cloud to AI training/inference, humanoids and robots; supply limited to ~30-35% annual exabyte growth, elongating the cycle. WDC CY27/CY28 EPS 'a little over $45 and a little over $70' if the checks hold — sub-10x in CY28. Keeps Seagate as top pick (WDC 1B) since WDC has not yet qualified HAMR and only ramps 44TB in H1 CY27. |

**Quarter synthesis:** the debate has shifted from "does demand hold?" to "how much can pricing double and how long does the cycle elongate" — the flow (JPM, MS Woodring) is unanimously bull on nearline pricing (targets $25/$30/TB) and on the elongation from capped supply, leaving the HAMR lag vs Seagate as the only tactical nuance (WDC 1B, not top pick).

## Management commentary — evolution (last 4 quarters)

| Theme | Q4 FY25 (2025-07-30) | Q1 FY26 (2025-10-30) | Q2 FY26 (2026-01-29) | Q3 FY26 (2026-04-30) |
| --- | --- | --- | --- | --- |
| Cloud / nearline demand | Cloud 90% of rev, $2.3B, +36% y/y | Cloud 89%, $2.5B, +31% y/y | Cloud 89%, $2.7B, +28% y/y | Cloud 89%, $3.0B, +48% y/y |
| Exabyte shipments | 190 EB, +32% y/y | 204 EB, +23% y/y | 215 EB, +22% y/y | 222 EB, +34% y/y |
| Pricing (ASP/TB) | Down low-single-digits, mix-driven | Modest low-single-digit increases | Flattish to slightly up; stable | +9% y/y on better TCO |
| Gross margin (non-GAAP) | 41.3%, +610bps y/y | 43.9%, +660bps y/y | 46.1%, +770bps y/y | 50.5%, +1,040bps y/y |
| HAMR qualification | Qual targeted H2 2027 | Pulled forward to H1 2026, ramp H1 2027 | In qual; progress with 2+ customers | In qual with four customers; 44TB |
| LTAs / customer coverage | Top-five firm POs through FY26 | Five firm through 2026, one to 2027 | "Sold out CY26"; deals to CY27-28 | LTAs extend into CY2028-2029 |

_Source: WDC earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY25 (2025-08-14)](../WDC/WDC_10-K_2025-08-14_0000106040-25-000038.html) · [10-Q Q3 FY26, period ended 2026-04-03 (2026-05-01)](../WDC/WDC_10-Q_2026-05-01_0001628280-26-029054.html).
- **Transcripts:** [Q3 FY26 (2026-04-30)](../WDC/transcripts/WDC_Q3-FY26-earnings_2026-04-30.md) · [Q2 FY26 (2026-01-29)](../WDC/transcripts/WDC_Q2-FY26-earnings_2026-01-29.md) · [Q1 FY26 (2025-10-30)](../WDC/transcripts/WDC_Q1-FY26-earnings_2025-10-30.md) · [Q4 FY25 (2025-07-30)](../WDC/transcripts/WDC_Q4-FY25-earnings_2025-07-30.md).
- **Equity calls:** [Erik Woodring (MS) — HDD/Dell/Apple (2026-06-16)](../_equity_calls/Overall/2026-06-16_ErikWoodring_HDD-Dell-Apple.md).
- **Research reports (relatórios bons):**
  - [Bernstein — Global HDD: It's HAMR time! (2025-10-23)](../relat%C3%B3rios%20bons/Bernstein_on_HDD.html)
  - [Bernstein — Initiation: AAPL/STX/DELL/SNDK (2025-09-15)](../relat%C3%B3rios%20bons/Bernstein_initiation_on_AAPL_STX_DELL_SNDK.html)
  - [UBS — US Semiconductors & Semi Equipment 2026 Overview (2025-12-22)](../relat%C3%B3rios%20bons/UBS_2026_overview.html)
  - [Morgan Stanley — AI NAND Overview (2025-09-10)](../relat%C3%B3rios%20bons/AI_Nand_overview_MS.html)
  - [Jefferies — Q425 Techknowledge tech takeaways (2025-12-17)](../relat%C3%B3rios%20bons/Q425_Techknowledge_tech_takeaways.html)
  - [JPM HDD (2026-04-09)](../relat%C3%B3rios%20bons/2026_04_09_hdd_jpm_9_apr_26.html) — HAMR-lag worry "too much in focus"; ePMR cost-optimized to ~60TB; LT margins converge
  - [JPM Networking (2026-05-26)](../relat%C3%B3rios%20bons/2026_05_26_nw_jpm_26_05.html) — pricing the biggest upside (mid-teens in 12mo possible); WDC price-driven, ~−10%/EB cost; no unit adds
- **Briefings:** company-specific 2026-06-16/17/18/19, 2026-06-03, 2026-05-11/15 (WDC on Rothschild relative-high screens; BofA REAL bogey poll; FinTwit HDD-vs-memory valuation debate). No `by-ticker/WDC.md` roll-up on disk.
- **Themes:** [hbm-memory](themes/hbm-memory.md) (HDD pulled into the memory-tightness tractor beam; ~90% incremental GM) · [ai-datacenter-power](themes/ai-datacenter-power.md).
- **Outlook:** attempted (`outlook.py --no-body --days 7`); returned no data in this environment — no live desk notes pulled.
