<!-- per-company wiki page. "Consensus estimates (BBG)" block auto-injected by build_wiki_html.py from _data/estimates.json (USD) — do NOT hand-write it. NVTS not yet in estimates.json as of 2026-06-20, so the block may be absent. -->

# NVTS — Navitas Semiconductor

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\NVTS` (10-K/10-Q filings + transcripts) · briefings `E:\briefings\2026`. Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof 2026-06-22 · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $42m | $74m |
| Gross profit | $16m | $31m |
| Gross margin | 39.2% | 41.3% |
| EBITDA | $-43m | $-33m |
| EPS | $-0.18 | $-0.15 |
| Capex | $2m | $2m |
| OCF (≈EBITDA) | $-43m | $-33m |

<svg xmlns="http://www.w3.org/2000/svg" width="326" height="88" viewBox="0 0 326 88" font-family="-apple-system,Segoe UI,Roboto,sans-serif"><text x="0" y="10" font-size="11" font-weight="600" fill="#33405c">FY1 EPS revision</text><text x="10" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="28" y="6.2" width="20" height="51.8" rx="2" fill="#1c5fd6"/><text x="38" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="56" y="13.7" width="20" height="44.3" rx="2" fill="#1c5fd6"/><text x="66" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="84" y="14.0" width="20" height="44.0" rx="2" fill="#1c7d3f"/><text x="94" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="0" y="84" font-size="10" fill="#1c7d3f">-15.0% 3m</text><text x="176" y="10" font-size="11" font-weight="600" fill="#33405c">FY2 EPS revision</text><text x="186" y="69" font-size="9" text-anchor="middle" fill="#8492ad">6m</text><rect x="204" y="7.5" width="20" height="50.5" rx="2" fill="#1c5fd6"/><text x="214" y="69" font-size="9" text-anchor="middle" fill="#8492ad">3m</text><rect x="232" y="13.1" width="20" height="44.9" rx="2" fill="#1c5fd6"/><text x="242" y="69" font-size="9" text-anchor="middle" fill="#8492ad">1m</text><rect x="260" y="14.0" width="20" height="44.0" rx="2" fill="#1c7d3f"/><text x="270" y="69" font-size="9" text-anchor="middle" fill="#8492ad">now</text><text x="176" y="84" font-size="10" fill="#1c7d3f">-12.8% 3m</text></svg>

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Navitas is a **fabless, small-cap (~$45.9m FY25 revenue) wide-bandgap power-semiconductor pure-play** — **GaN** power ICs ("GaNFast") plus **SiC** MOSFETs/diodes ("GeneSiC", acquired Aug-2022) — that has executed a hard strategic pivot ("Navitas 2.0") away from its legacy China mobile/consumer fast-charger business toward **high-power markets: AI data centers, energy/grid infrastructure, performance computing, industrial electrification** (10-K FY2025, 2026-02-27). FY2025 revenue fell **45% to $45.9m** (from $83.3m) as China mobile/consumer rolled off; net loss **$117.0m** (10-K, 2026-02-27). The entire equity story now hangs on one swing factor: the **May-2025 selection by NVIDIA to co-develop the next-gen 800V HVDC datacenter power architecture** for Kyber/Rubin-Ultra rack-scale systems ([Navitas IR, 2025-05-21](https://ir.navitassemi.com/news-releases/news-release-details/nvidia-selects-navitas-collaborate-next-generation-800-v-hvdc)). This is a high-beta, binary-feel name — material AI-DC P&L contribution is not guided until **2027**, against a cash-burning P&L and a forced GaN-foundry migration off TSMC.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) GaN power ICs (GaNFast) · 2) SiC MOSFETs/diodes (GeneSiC) · 3) 800V HVDC grid-to-GPU power platforms (e.g. 10kW all-GaN DC-DC) |
| **Main buyer(s)** | AI-datacenter / NVIDIA 800V HVDC (the swing, P&L from 2027); legacy mobile chargers (exiting); sold via distribution — Distributor A = 59% of Q1'26 revenue |
| **Key suppliers** | Fabless foundries: TSMC (GaN, exits Jul-2027), GlobalFoundries + Powerchip (GaN), X-Fab (SiC) |

## Position in the value chain
Navitas sits in the middle of the AI-power stack: it does **no fabrication itself** (fabless), sourcing GaN wafers from **TSMC** (sole historical GaN foundry, ceasing GaN production July-2027) plus **GlobalFoundries** (new US 8-inch GaN partnership, production 2027) and **Powerchip**, and SiC from **X-Fab** on Navitas-developed process (10-K, 2026-02-27). It designs and sells GaN + high-voltage SiC power ICs that span "the entire power path from the utility grid to the GPU." The **NVIDIA 800V HVDC design win is the swing**: GaN content is framed at **~$10–15k per MW** and SiC AC-DC PSU content at **~$5–8k per MW**, with PSU scaling (10kW→18.5kW) driving non-linear SiC content (Q1 2026 call, 2026-05-05). UBS independently sizes the content economics in a similar range, framing Navitas at **~$45/kW of 800V-rack power content by 2030** — split **$10 UHV SiC + $10–15 SiC/HV GaN + $25–30 low-voltage GaN** — and a **power-only SAM growing from ~$750m (2025) to ~$2.6bn (2030)** (UBS / T. Arcuri, 2025-12-22); note low-voltage GaN (the GPU-proximate VR/conversion stage) is the largest content bucket, where Navitas is less established than incumbents (TXN, MPWR, IFX). The offsetting reality is **small-cap / cash-burn risk** — $45.9m FY25 revenue, ~$12m/qtr operating loss, breakeven needing revenue "in the high 30s [millions/qtr]" vs $8.6m actual (Q1 2026 call). See [800v-dc-power](themes/800v-dc-power.md) · [ai-datacenter-power](themes/ai-datacenter-power.md).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="11">
  <rect x="8" y="48" width="176" height="124" rx="6" fill="#eef3fb" stroke="#3b5b92"/>
  <text x="96" y="70" text-anchor="middle" font-weight="bold">Suppliers (foundry)</text>
  <text x="96" y="90" text-anchor="middle" font-weight="bold">TSMC — GaN</text>
  <text x="96" y="107" text-anchor="middle">(exits GaN Jul-2027)</text>
  <text x="96" y="125" text-anchor="middle">GlobalFoundries (US, '27)</text>
  <text x="96" y="142" text-anchor="middle">Powerchip · X-Fab (SiC)</text>
  <text x="96" y="160" text-anchor="middle">fabless model</text>

  <rect x="262" y="35" width="196" height="150" rx="6" fill="#dceede" stroke="#2f7d46"/>
  <text x="360" y="58" text-anchor="middle" font-weight="bold">Navitas (NVTS)</text>
  <text x="360" y="78" text-anchor="middle">GaN power ICs (GaNFast)</text>
  <text x="360" y="96" text-anchor="middle">+ SiC MOSFET/diode</text>
  <text x="360" y="114" text-anchor="middle">(GeneSiC)</text>
  <text x="360" y="134" text-anchor="middle">grid-to-GPU power path</text>
  <text x="360" y="156" text-anchor="middle" font-weight="bold">FY25 rev $45.9m · loss-making</text>

  <rect x="536" y="30" width="176" height="160" rx="6" fill="#fbf0e6" stroke="#b3691f"/>
  <text x="624" y="50" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="624" y="69" text-anchor="middle" font-weight="bold">AI datacenter 800V</text>
  <text x="624" y="85" text-anchor="middle" font-weight="bold">(NVIDIA) — the swing</text>
  <text x="624" y="103" text-anchor="middle">mobile chargers (exiting)</text>
  <text x="624" y="121" text-anchor="middle">EV / industrial</text>
  <text x="624" y="139" text-anchor="middle">solar / energy storage</text>
  <text x="624" y="160" text-anchor="middle">hyperscalers · Tier-1 OEM/ODM</text>

  <line x1="184" y1="110" x2="258" y2="110" stroke="#444" stroke-width="2" marker-end="url(#a)"/>
  <line x1="458" y1="110" x2="532" y2="110" stroke="#444" stroke-width="2" marker-end="url(#a)"/>
  <defs>
    <marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#444"/>
    </marker>
  </defs>
  <text x="360" y="208" text-anchor="middle" fill="#666">NVIDIA 800V design win = the swing (~$10–15k GaN + $5–8k SiC per MW; AI-DC P&amp;L from 2027) · small-cap cash-burn = the risk</text>
</svg>

## Current state (latest quarter)
**Q1 2026 (quarter ended 2026-03-31; call 2026-05-05):** Revenue **$8.6m**, +18% sequentially (Q4'25 $7.3m), above the high end of guidance; **high-power markets +35% YoY** and now the majority of revenue, "AI infrastructure" (data center + grid) **+50% QoQ** (Q1 2026 call). Non-GAAP gross margin **39.0%** (+30bps); non-GAAP operating loss **$11.7m**; non-GAAP net loss **-$0.04**. GAAP net loss **$33.8m / -$0.15** (incl. ~$10.3m stock comp, $4.7m intangible amortization, earnout fair-value swings) (10-Q, 2026-05-05). Cash **$221m, zero debt** (down from $237m at YE25 on working-capital build; inventory $14.9m); ~230m diluted shares. **Customer concentration is extreme — Distributor A was 59% of Q1 revenue** (10-Q, 2026-05-05). Q2 2026 guide: revenue **$10.0m ± $0.5m** (16%+ sequential), non-GAAP GM **39.25% ± 75bps**, opex **$14.5–15.5m** (Q1 2026 call). Mobile/low-end consumer is "rapidly diminishing… insignificant by year-end." Management TAM: **$3.5bn by 2030 at 60%+ CAGR**.

## Debate / thesis
- **Bull:** The **NVIDIA 800V HVDC selection (May-2025)** legitimizes Navitas as one of very few suppliers with *both* GaN and SiC across the grid-to-GPU path — "Having both makes a huge difference" (Q1 2026 call). High-power is now the majority of revenue and growing (+35% YoY, AI-DC+grid +50% QoQ); gross margin is climbing through the pivot (38.5%→39.0%) and the legacy China-mobile drag is almost fully shed. Reference designs are real: a **10kW all-GaN 800V-to-50V DC-DC platform at 98.5% peak efficiency**, co-developed with a customer (Q4 2025 call, 2026-02-24), and — per JPM's June primer — a newer **20kW 800V-to-6V DC-DC platform on latest-gen GaN at 97.5% peak efficiency** (addressing NVIDIA's 800V→6V-direct target) plus an 800V-to-50V AI power brick, both drawing "strong customer interest"; **Gen5/Gen6 1.2kV SiC is sampling** with feedback of up to **50% higher power density and >98% system efficiency** (JPM "First Principles," 2026-06-25). JPM frames Navitas's ambition as becoming **#2 to Infineon in AI power** via performance leadership across the whole grid-to-core chain, with a **2030 SAM of ~$3.5bn at a ~60% CAGR (roughly 50/50 GaN/SiC)** and a signed **cross-license with Infineon**; it also notes AC-DC SiC content **scales non-linearly** (from ~$2 in a 5kW PSU today to ~$200/kW in the 30kW PSUs due in 6–9 months) (JPM "First Principles," 2026-06-25). Even bearish UBS validates a long-run **~$2.6bn power-only SAM by 2030 at ~$45/kW** of 800V-rack content (UBS / T. Arcuri, 2025-12-22). Morgan Stanley's J. Moore nudged the PT to **$13.70 (from $12.50)** — "tracking but proofpoints pending… Stepping up the Voltage" (briefing 2026-05-06). $221m cash, zero debt = runway to fund the ramp.
- **Bear:** It is **pre-revenue on the actual story** — material AI-DC P&L contribution isn't until **2027** (Q3/Q1 calls), while the company burns ~$12m/qtr operating loss on $8.6m of revenue and needs "high-30s [millions/qtr]" to break even (Q1 2026 call) — a >4x revenue gap. The Street's marginal-buyer rating is *negative*: **Morgan Stanley is Underweight** (since 2025-04-06, ref $6.04) and **Jefferies is HOLD** (ref $6.43, 2025-09-26) — both well below where the bull-case PTs sit, i.e. the sell-side broadly does not underwrite the 800V optionality at current prices. On the content math, UBS's $45/kW splits the largest bucket ($25–30/kW) into **low-voltage GaN**, the GPU-proximate stage where incumbents (TXN, MPWR, IFX) are entrenched — not a given that Navitas wins it (UBS / T. Arcuri, 2025-12-22). FinTwit is openly skeptical of the narrative: **@insane_analyst** flagged "dumb ppl falling for **Navitas CEO TAM bullshit. SiC is garbage. Only GaN portfolio of value**" (briefings 2026-06-15/06-16). The **TSMC GaN exit (July 2027)** forces an unproven migration to GlobalFoundries/Powerchip with re-qualification risk (10-K, 2026-02-27). **59% single-distributor concentration** (10-Q) and a small, volatile float make this a momentum trade on NVDA headlines, not fundamentals.
- **Where the sell-side/buy-side stands:** Coverage skews **cautious to negative** at the franchise level even as the theme is hot. **Morgan Stanley (Joseph Moore)** carries an **Underweight** rating (initiated 2025-04-06, ref $6.04) yet a **$13.70 PT**, "tracking but proofpoints pending" (briefing 2026-05-06; rating per MS Scale-up primer). **Jefferies HOLD** (ref $6.43, Asia takeaways, 2025-09-26; Jefferies is an NVTS underwriter — note conflict). **UBS (Timothy Arcuri)** frames the bull-case TAM math but does not endorse the equity (2025-12-22). Deutsche Bank's Ross Seymore "Stepping up the Voltage" (briefing 2026-05-06). Coverage is thin and intermittent — across May–June 2026 NVTS repeatedly shows **0 sell-side emails** in the briefing universe (e.g. 2026-05-12/05-22/05-28/05-31/06-18), with flow appearing only as FinTwit/52-week-high-list name-drops. Net: a small-cap where the Street is in wait-and-see mode pending 2027 proof points.

## Catalysts / what to watch
- **Q2 2026 print (~early Aug 2026)** — guide $10.0m ± $0.5m / 39.25% GM; watch high-power mix, AI-DC+grid sequential pace, and whether mobile is fully shed.
- **In-rack GaN proof points (Q1–Q2 2027 per mgmt)** — board/system-level testing now; the gate to NVIDIA 800V production revenue.
- **NVIDIA Kyber/Rubin-Ultra 800V HVDC ramp (2H26 standard arrival; deployment ~2027)** — the single biggest swing; tied to the broader 800V timeline (see [800v-dc-power](themes/800v-dc-power.md)).
- **Low-voltage GaN traction** — the largest content bucket per UBS ($25–30/kW of the $45/kW); evidence Navitas can take share from incumbents (TXN/MPWR/IFX) at the GPU-proximate stage (UBS / T. Arcuri, 2025-12-22).
- **GlobalFoundries US 8-inch GaN qualification → production 2027** — execution proof that the TSMC-exit migration is de-risked.
- **Path to breakeven** — revenue "high-30s/qtr" vs $8.6m today; watch the sequential ramp slope and opex discipline ($14.5–15.5m).
- **Capital adequacy** — $221m cash vs ~$12m/qtr operating burn; any ATM/raise (small ATM costs already in the filings).

## Risks
- **Cash burn / going-concern-adjacent runway:** persistent net losses ($117.0m FY25), ~$12m/qtr operating loss, breakeven >4x current revenue; "may require additional capital… might not be available on acceptable terms, if at all" (10-K risk factors, 2026-02-27).
- **Binary AI-DC dependence:** the thesis rests on NVIDIA 800V adoption and timing — no material P&L until 2027; if the 800V transition slips or content is contested, there is little else.
- **Content-capture risk at the GPU-proximate stage:** UBS's largest 2030 content bucket is low-voltage GaN ($25–30/kW), dominated today by TXN/MPWR/IFX; Navitas winning it is not assured (UBS / T. Arcuri, 2025-12-22).
- **Customer/distributor concentration:** Distributor A = **59% of Q1 2026 revenue** (10-Q, 2026-05-05).
- **Foundry transition risk:** TSMC ceasing GaN production July-2027; migration to GlobalFoundries/Powerchip requires re-qualification, risks delays/scrap/cost (10-K, 2026-02-27).
- **SiC credibility / competition:** FinTwit questions the SiC franchise value ("SiC is garbage," @insane_analyst, briefing 2026-06-16); competes against far larger IDMs (Infineon, onsemi, TI, STM) and a potential China GaN/SiC supply flood. Note also TSMC commentary that trailing-edge **power demand, particularly SiC, remains weak** into C26 (Jefferies Asia takeaways, 2025-09-26) — a soft cyclical backdrop for the SiC base.
- **Small-cap volatility:** thin float, momentum-driven, high beta to NVDA/800V headlines; legacy China mobile/consumer + tariff exposure during wind-down (10-K, 2026-02-27).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder (figures in USD). NVTS not in estimates.json as of 2026-06-20 — block may be absent. -->

## In the inbox (Outlook — recent sell-side flow)
- **Nutty "Part 2 — NVIDIA Kyber Rack & 800V Ecosystem" (nuttycld.substack.com, 2026-04-17):** Pre-print piece covering the NVIDIA Kyber rack (1MW, 800V HVDC) and the 800V power-semiconductor ecosystem. NVTS is named alongside IFX as a key supplier in the 800V architecture, framing Navitas's GaN/SiC portfolio as well-positioned for the rack-scale power inflection — consistent with the NVIDIA 800V HVDC design win announced May-2025. (Nutty "Part 2", nuttycld.substack.com, 2026-04-17)
- **Nutty "Part 3 — 800V Ecosystem Follow-up" (nuttycld.substack.com, ~2026-04-21):** Brief follow-up naming NVTS alongside IFX and ADI in the 800V power-semiconductor stack (3 mentions, brief). No new company-specific data beyond reinforcing NVTS's place in the 800V ecosystem. (Nutty "Part 3", nuttycld.substack.com, ~2026-04-21)
- A two-pass Outlook pull was attempted (`outlook.py --no-body --days 14`) but **returned no usable output in this environment** (empty result). Sell-side/FinTwit stance below is therefore sourced from the **briefing archive** and the **research-report set**, not a live inbox.
- **Morgan Stanley (Joseph Moore)** — **Underweight** (since 2025-04-06, ref $6.04 per Scale-up primer); PT **$13.70** (from $12.50), "tracking but proofpoints pending" _(briefing 2026-05-06)_.
- **Jefferies** — **HOLD**, ref $6.43 _(Asia takeaways, 2025-09-26; NVTS is a Jefferies underwriting client — conflict noted)_.
- **UBS (Timothy Arcuri)** — power-only SAM ~$750m→$2.6bn by 2030 at ~$45/kW 800V-rack content _(2025-12-22)_; framing only, no equity endorsement read in-report.
- **JPM "Watts Up! Shift to 800V" (2026-06-09)** — Navitas is the **source of JPM's WBG market sizing**: the wide-bandgap power-device market (AI DC + energy/grid) grows **30%+ CAGR from ~$1bn (2025) to $5bn+ by 2030**, with long-term content **$25K–$35K/MW split ~evenly SiC/GaN** (GaN primarily inside the DC — the segment most relevant to NVTS). Driven by the 800V rack pivot, non-linear PSU scaling (2x power → ~5x SiC content; PSU 5–10kW→18.5–30kW) and grid SST/BESS modernization for the 219–298 GW of projected 2030 AI-DC demand. Corroborates NVTS's own $3.5bn-by-2030 / 60%+ CAGR TAM framing. Navitas also listed among NVIDIA-highlighted silicon providers.
- **Citi "800V DC power" (2026-06-15)** — Citi's GaN/SiC split is **constructive on GaN-at-the-rack** (where NVTS plays): **GaN preferred for sub-650V conversion** at server/rack level, **SiC for >1,000V infrastructure** (rectifiers, power shelves, SSTs). Earliest broad deployment is **±400V HVDC bipolar (each rail ≤400V → ≤650V device stress)**, leveraging the mature/cost-competitive 650V GaN ecosystem from EVs — favorable adoption timing for rack-level GaN from 2027–2028. Note Citi's named GaN winners are TXN/ON (high-voltage + vertical GaN), not NVTS — i.e. the theme is GaN-positive but the share question for NVTS is open (Citi "800V", 2026-06-15).
- **FinTwit** _(briefings 2026-06-15/06-16)_: **@insane_analyst** bearish on the SiC narrative ("only GaN portfolio of value"); **@bubbleboi** mentions NVTS as a potential AI-DC-power-stack re-entry (no fundamental conviction). Recurring pattern: NVTS shows **0 sell-side emails** on most days (2026-05-12 / 05-22 / 05-28 / 05-31 / 06-18) — coverage is thin and headline-driven.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 2026 · May 5 → Jun 16, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Demand / TAM** | $3.5bn by 2030 at 60%+ CAGR; AI-infra +50% QoQ | JPM: WBG $1bn→$5bn+ at 30%+ CAGR (sizing supplied by NVTS itself), listed among NVIDIA's suppliers | **✓ confirms** (corroborates the TAM) |
| **Product / 800V roadmap** | 3-phase architecture; in-rack GaN proof Q1–Q2'27 | Citi: favorable timing for rack GaN 2027–2028 via ±400V bipolar/mature 650V | **✓ confirms** (timing aligned) |
| **Competition / GaN share** | Has GaN + SiC across the grid-to-GPU path ("having both makes a difference") | Citi: GaN winners are TXN/ON, not NVTS · @insane_analyst: "SiC is garbage, only GaN has value" | **✗ contests** (share open, SiC questioned) |
| **Valuation / conviction** | — | MS Underweight (ref $6.04) but PT $13.70; DB "Stepping up the Voltage" | **⚠ nuance** (PT rises, rating doesn't) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-06 | Morgan Stanley · Joseph Moore (briefing 2026-05-06) | valuation | mixed | MS maintains Underweight (since 2025-04-06, ref US$6.04) but raised PT to US$13.70 (from US$12.50), "tracking but proofpoints pending… Stepping up the Voltage". Deutsche Bank (Ross Seymore) also "Stepping up the Voltage". |
| 06-09 | JPM · Samik Chatterjee (Watts Up! Shift to 800V) | demand | bull | Navitas is the source of JPM's WBG sizing: WBG power-device market (AI DC + energy/grid) grows 30%+ CAGR from ~US$1bn (2025) to US$5bn+ by 2030; LT content US$25K–35K/MW split ~evenly SiC/GaN (GaN mainly inside the DC — the segment most relevant to NVTS). Driven by the 800V pivot, non-linear PSU scaling (2x power → ~5x SiC content) and grid SST/BESS modernization. Corroborates NVTS's own US$3.5bn-by-2030 / 60%+ CAGR TAM; Navitas listed among the silicon suppliers highlighted by NVIDIA. |
| 06-25 | JPM · Deshpande (First Principles — AI Power) | product | bull | JPM primer: Navitas repositioned as an AI-DC-power + grid pure-play aiming to be **#2 to Infineon**; new **20kW 800V-to-6V GaN platform (97.5% peak eff.)** + 800V-to-50V brick; **Gen5/6 1.2kV SiC sampling (up to 50% higher density, >98% eff.)**; **2030 SAM ~$3.5bn at ~60% CAGR (~50/50 GaN/SiC)**; signed **cross-license with Infineon**; AC-DC SiC content scales non-linearly (~$2 in a 5kW PSU → ~$200/kW in a 30kW PSU); TSMC ships through ~2029, GF 8-inch US production 2027. (Sector primer, not an equity rating.) |
| 06-15 | Citi · 800V DC power (briefing 2026-06-15) | competition | mixed | Citi's GaN/SiC split is constructive on GaN-in-rack (where NVTS plays): GaN preferred for sub-650V conversion at the server/rack level, SiC for >1,000V infra. Earlier deployment is ±400V bipolar HVDC (each rail ≤400V → ≤650V stress) leveraging the mature 650V GaN ecosystem from EVs — favorable timing for rack GaN 2027–2028. Note: Citi's named GaN winners are TXN/ON (not NVTS) — GaN-positive theme but the share question for NVTS is open. |
| 06-16 | FinTwit · @insane_analyst (briefing 2026-06-16) | competition | bear | @insane_analyst bearish on the SiC narrative — "dumb ppl falling for Navitas CEO TAM bullshit. SiC is garbage. Only GaN portfolio of value". @bubbleboi mentions NVTS as a possible re-entry into the AI-DC-power-stack (without fundamental conviction). |

**Quarter synthesis:** the debate has shifted from the "if" of the TAM (now corroborated by JPM, with NVTS itself the source of the sizing) to the "who captures it" — competition in rack GaN (Citi points to TXN/ON, not NVTS) and SiC credibility (FinTwit skeptical) have become the sticking point, while the sell-side raises PTs without changing ratings, leaving the 2027 optionality still not underwritten.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2'25 (2025-08-04) | Q3'25 (2025-11-03) | Q4'25 (2026-02-24) | Q1'26 (2026-05-05) |
| --- | --- | --- | --- | --- |
| Revenue | $14.5m, midpoint; "classic downturn" | $10.1m, at midpoint | $7.3m; framed Q4 as the bottom | $8.6m, +18% QoQ, above guide |
| High-power vs mobile | Pivot announced; deprioritize China mobile | "Navitas 2.0"; mobile <50% in Q4 | High-power majority for first time; mobile <25% | High-power +35% YoY, AI-infra +50% QoQ |
| Gross margin | 38.5%; flat until revenue inflects | 38.7%, +20bps on mix | 38.7% non-GAAP | 39.0%, +30bps; guide 39.25% |
| NVIDIA 800V / AI-DC | Selected; $2.6bn TAM, ramp late-2026/2027 | Power-selected partner; 2027 material P&L | 10kW all-GaN 800V-to-50V, 98.5% eff. | 3-phase arch; in-rack GaN proof Q1–Q2'27 |
| GaN foundry / TSMC | Powerchip 8-inch added; TSMC supply to mid-'27 | TSMC primary; exploring more partners | GlobalFoundries US GaN, prod. late-26/'27 | GF US 8-inch GaN 2027; TSMC exits Jul-'27 |
| Cash / runway | $161m, no debt; ~$10–11m/qtr burn | $151m, no debt | ~$237m, no debt | $221m, no debt; breakeven "high-30s/qtr" |

_Source: NVTS earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY2025 (2026-02-27)](../NVTS/NVTS_10-K_2026-02-27_0001821769-26-000007.html) · [10-Q Q1 2026 (2026-05-05)](../NVTS/NVTS_10-Q_2026-05-05_0001628280-26-030524.html).
- **Transcripts:** [Q1 2026 (2026-05-05)](../NVTS/transcripts/NVTS_Q1-2026-earnings_2026-05-05.md) · [Q4 2025 (2026-02-24)](../NVTS/transcripts/NVTS_Q4-2025-earnings_2026-02-24.md) · [Q3 2025 (2025-11-03)](../NVTS/transcripts/NVTS_Q3-2025-earnings_2025-11-03.md) · [Q2 2025 (2025-08-04)](../NVTS/transcripts/NVTS_Q2-2025-earnings_2025-08-04.md). _Two latest read in full; Q2'25 is the full Refinitiv edited transcript, Q3'25/Q4'25/Q1'26 are sourced from public transcript coverage (Motley Fool / Yahoo / Seeking Alpha) and cross-checked to the 10-Q/10-K._
- **Press:** [NVIDIA selects Navitas — 800V HVDC (Navitas IR, 2025-05-21)](https://ir.navitassemi.com/news-releases/news-release-details/nvidia-selects-navitas-collaborate-next-generation-800-v-hvdc).
- **Research reports (relatórios bons):**
  - [UBS — The State of The State: 2026 Preview (US Semis, T. Arcuri, 2025-12-22)](../relat%C3%B3rios%20bons/UBS_2026_overview.html) — power-only SAM $750m→$2.6bn by 2030; $45/kW 800V content split ($10 UHV SiC / $10–15 SiC+HV GaN / $25–30 LV GaN).
  - [JPM "Watts Up! Shift to 800V" (2026-06-09)](../relat%C3%B3rios%20bons/JPM_on_800v.html) — WBG market $1bn→$5bn+ (2030, Navitas-sourced); $25–35K/MW split ~evenly SiC/GaN; GaN primarily inside the DC.
  - JPM "First Principles — AI Power Infrastructure" (Deshpande, 2026-06-25) — NVTS aims to be #2 to Infineon; 20kW 800V-to-6V GaN (97.5% eff.), Gen5/6 1.2kV SiC sampling (50% higher density); 2030 SAM ~$3.5bn/~60% CAGR (~50/50 GaN/SiC); Infineon cross-license; non-linear AC-DC SiC content scaling
  - [Citi "800V DC power" (2026-06-15)](../relat%C3%B3rios%20bons/800v_Citi.html) — GaN preferred sub-650V at rack, SiC >1,000V infra; ±400V bipolar leverages mature 650V GaN; Citi GaN winners TXN/ON.
  - [Jefferies — Asia Takeaways: WFE/Memory Better, NVDA/AVGO Strong C26 (2025-09-26)](../relat%C3%B3rios%20bons/Asia_Takeaways_WFE_Memory_Better_NVDA_AVGO_Strong_C26_An.html) — NVTS rated HOLD (ref $6.43); SiC/power trailing-edge demand weak into C26 (no thesis-level NVTS content beyond rating).
  - [Morgan Stanley — Scale-up Primer](../relat%C3%B3rios%20bons/Scale_up_primer_MS.html) — NVTS rated Underweight (since 2025-04-06, ref $6.04); no NVTS body/thesis content beyond rating.
- **Themes:** [800v-dc-power](themes/800v-dc-power.md) · [ai-datacenter-power](themes/ai-datacenter-power.md).
- **Briefings:** `E:\briefings\2026` — 2026-05-06 (MS PT $13.70; DB "Stepping up the Voltage"), 2026-06-15/06-16 (FinTwit SiC skepticism / AI-DC-power read-through), plus thin/zero-coverage days (05-12 / 05-22 / 05-28 / 05-31 / 06-18).
- **Consensus:** BBG estimates auto-injected from `_data/estimates.json` (NVTS US Equity, USD) — not present as of 2026-06-20.
