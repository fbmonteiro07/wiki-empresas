# PANW — Palo Alto Networks, Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\PANW` (10-K FY25, 10-Q FQ3 FY26, transcripts) · `_equity_calls` · `E:\briefings\2026\*.md`. Master index: [../INDEX.md](../INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $12.9bn | $14.6bn |
| Gross profit | $9.8bn | $11.2bn |
| Gross margin | 76.3% | 76.5% |
| EBITDA | $4.2bn | $5.2bn |
| EPS | $3.73 | $4.43 |
| Capex | $237m | $289m |
| OCF (≈EBITDA) | $4.2bn | $5.2bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
The largest pure-play enterprise cybersecurity vendor, pivoting from a product (firewall) company to a multi-platform recurring-revenue franchise. Three platforms: **Strata** (network security — ML-powered NGFWs + Prisma Access/SD-WAN SASE), **Prisma Cloud / Cortex Cloud** (cloud-native protection, CNAPP), and **Cortex** (AI-driven security operations — XSIAM, XDR, XSOAR, Xpanse) — now extended into **identity** (CyberArk) and **observability** (Chronosphere). FY25 revenue $9,221.5M, +14.9% YoY; subscription & support is the growth engine, with recurring revenue now ~46% of product revenue vs 22% three years ago (10-K FY25, 2025-08-29; Q3 FY26 call, 2026-06-02). The strategic spine is **"platformization"** — consolidating point products onto PANW platforms — and, increasingly, securing customers' AI/agentic deployments. NGS ARR is the headline KPI: $5.6B exiting FY25, guided to $8.9–8.95B for FY26 (inflated by M&A).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Strata — network security (ML-powered NGFWs + Prisma Access/SD-WAN SASE) · 2) Prisma Cloud / Cortex Cloud (cloud-native protection, CNAPP) · 3) Cortex — AI-driven SecOps (XSIAM/XDR/XSOAR) |
| **Main buyer(s)** | Enterprises & government IT/security teams; ~2,280 platformized customers, 120% net retention (Q3 FY26) |
| **Key suppliers** | Cloud infra (AWS/Azure/GCP) for SaaS delivery; memory/storage components for firewall hardware (cost inflation drove ~10% April price hike); threat intel via Unit 42 |

## Position in the value chain
PANW sits between upstream infrastructure/threat-intelligence inputs and downstream enterprise/government buyers, packaging detection + prevention + AI-driven response into platforms rather than point tools. The differentiated angle is **platformization** (land-and-consolidate across network, cloud, SecOps, identity, observability) plus an emerging **agentic-SecOps** posture — using AI to defend against AI-accelerated attacks (XSIAM, AgentiX, Prisma AIRS) while monetizing the expanding AI threat surface.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="11">
  <rect x="10" y="55" width="150" height="110" rx="6" fill="#eef2f7" stroke="#5b7da6"/>
  <text x="85" y="78" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="98" text-anchor="middle">Cloud infra (AWS/</text>
  <text x="85" y="112" text-anchor="middle">Azure/GCP)</text>
  <text x="85" y="130" text-anchor="middle">Threat intel /</text>
  <text x="85" y="144" text-anchor="middle">Unit 42, data</text>
  <rect x="225" y="30" width="270" height="160" rx="6" fill="#dde9f5" stroke="#2f5e91" stroke-width="2"/>
  <text x="360" y="52" text-anchor="middle" font-weight="bold">Palo Alto Networks</text>
  <text x="360" y="68" text-anchor="middle" font-style="italic">cybersecurity platforms</text>
  <rect x="240" y="80" width="240" height="26" rx="4" fill="#fff" stroke="#2f5e91"/>
  <text x="360" y="97" text-anchor="middle">Strata — network security / SASE</text>
  <rect x="240" y="112" width="240" height="26" rx="4" fill="#fff" stroke="#2f5e91"/>
  <text x="360" y="129" text-anchor="middle">Prisma — cloud / SASE</text>
  <rect x="240" y="144" width="240" height="26" rx="4" fill="#fff" stroke="#2f5e91"/>
  <text x="360" y="161" text-anchor="middle">Cortex — AI SecOps (+ identity)</text>
  <rect x="560" y="55" width="150" height="110" rx="6" fill="#eef2f7" stroke="#5b7da6"/>
  <text x="635" y="78" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="635" y="100" text-anchor="middle">Enterprise</text>
  <text x="635" y="118" text-anchor="middle">Government</text>
  <text x="635" y="136" text-anchor="middle">~2,280 platformized</text>
  <line x1="160" y1="110" x2="223" y2="110" stroke="#2f5e91" stroke-width="2" marker-end="url(#a)"/>
  <line x1="495" y1="110" x2="558" y2="110" stroke="#2f5e91" stroke-width="2" marker-end="url(#a)"/>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#2f5e91"/></marker></defs>
  <text x="360" y="208" text-anchor="middle" fill="#555">platformization (consolidate point tools) + agentic-SecOps (defend AI with AI)</text>
</svg>

## Current state (latest quarter)
**Q3 FY26 (qtr ended Apr 30, 2026; reported 2026-06-02).** A broad beat clearing all bogeys after a ~60% one-month run into the print.
- **NGS ARR $8.13B, +60% YoY** (incl. ~$1.6B from CyberArk + Chronosphere); **RPO $18.4B** (10-Q, 2026-06-03), +36% YoY; **revenue $3.00B, +31% YoY** (10-Q: $3,002M vs $2,289M PY).
- **Organic** NNARR $370M vs $350M guide; organic RPO bookings +25% YoY (Barclays/Kalia, 2026-06-03).
- **GAAP net loss $(177)M / $(0.22)** for the quarter, driven by CyberArk/Chronosphere acquisition accounting; 9-mo GAAP net income $589M (10-Q, 2026-06-03). Non-GAAP adjusted FCF $910M, +57% YoY (Q3 FY26 call).
- **Segment color:** NGFW bookings ~+40% ("strongest hardware quarter in a decade"); SASE ARR $1.6B +40% with ~50 displacement wins ~$200M; **XSIAM ARR >$600M, +100% YoY** (740+ customers); Prisma AIRS customers >300 (tripled QoQ). Platformized customers ~2,280 (+110 net new), 120% net retention (Q3 FY26 call).
- **Guide raised:** FY26 NGS ARR $8.9–8.95B (+59–60%), RPO $20.9–21.0B, revenue $11.415–11.425B (+24%), op margin 28.9–29.2%, adj FCF margin 37.5%; FQ4 EPS ~$0.97 vs Street ~$0.94 (briefing 2026-06-03; Q3 call). Stock fell ~1% post-print — "healthy breather," not a verdict (Jefferies/Favuzza, 2026-06-03).

## Debate / thesis
- **AI-software read-through — agent cybersecurity as a new category (Vercel CEO Guillermo Rauch, Stanford MS&E435, 2026-06-29):** Rauch argues that as agents get their own computers/sandboxes they open a PC-era-scale wave of new attack surface (data exfiltration, prompt-injection/exploitation, abused tool/API access), requiring new products for sandbox isolation, data-exfil prevention, governance and guardrails. Tailwind read-through for PANW's secure-AI / AI-runtime-security push (Prisma AIRS). See [tokenmaxxing theme](themes/tokenmaxxing.md).
- **Bull:**
  - "Cleared all bogeys; customers clearly turning to PANW to secure AI adoption; single-digit cyber share = long runway." MS (Marshall/Weiss) raised PT to **$320** from $253, OW; FY26E rev +23.8%, FY27E +18.2% (2026-06-03).
  - "Broad platform strength; NetSec/Prisma SASE displacement is the key differentiator vs ZS; constructive on FY27 acceleration." DB (Zelnick) Buy, PT **$350** — "strongest Q3 in several years" in SASE (2026-06-03).
  - "Solid execution with AI tailwinds and M&A synergies ahead of plan" — XSIAM, Prisma AIRS, CyberArk all beating. JPM (Essex/Lee) OW (2026-06-03).
  - IR-meeting takeaways: 4Q26 organic NNARR guide up $20M+ at midpoint; FY27 could add $1.9B+ total NNARR; accelerating NetSec can support FCF margins. Barclays (Kalia) OW, PT **$315** (note 2026-06-08, in briefing 2026-06-17).
  - **Agentic-AI demand inflection.** PANW expert (ex-PANW, BTG Mythos call 2026-06-18): Nikesh "referenced 800 customer meetings since April" on Mythos/AI security; "this is now the Mythos moment" (also acknowledged on the CRWD call). Unit 42 Frontier AI Defense: 800+ meetings in six weeks (Q3 FY26 call).
  - **Buy-side AI-enablement framing.** Cybersecurity is "one of the key constraints and governors on the pace at which AI will be rolled out" — PANW held as a cyber way to play the AI buildout / agent rollout, alongside infra (SNOW) and app-layer (INTU, HUBS, TEAM) picks. Felise Agranoff (PM, J.P. Morgan Asset Mgmt) in Barron's Tech Roundtable (2025-03-28); referenced at PANW $184.96 then, vs the ~$300s reached post-Q3-FY26.
  - **Citrini "All Along the AI Watchtower" (2026-07-20, newsletter):** flags **Project Glasswing (Anthropic)** with PANW as a key cyber partner, plus the **platform-consolidation playbook (DSPM roll-ups)**; PANW has re-rated but is still favored in the group (Citrini Semis, 2026-07-20).
- **Bear:**
  - "Beat-and-raise, but the **organic business is underwhelming**" — qualitative caution on product-revenue sustainability. Redburn/Rothschild Neutral (2026-06-03).
  - Headline NGS ARR/RPO growth is heavily flattered by M&A (~$1.6B of NGS ARR from CyberArk + Chronosphere); organic subscription revenue decelerated (Barclays, 2026-06-03; partly explained by virtual-firewall rev-rec mechanics per IR, 2026-06-17).
  - Product-outlook conservatism flagged: pull-forward dynamics + supply constraints; ~10% hardware price increase taken in April amid rising memory/storage component costs (Q3 FY26 call; DB 2026-06-03).
  - Integration/dilution risk: CyberArk consumed $21.1B (112M shares + $2.3B cash); GAAP loss this quarter; large goodwill/intangibles (10-Q, 2026-06-03).
- **UBS Q3 FY26 review + callbacks (Nikesh/Depak + IR), 2026-06-03 — the bear's exhibit A on quality:** of the **30% product growth, 8 points came from CyberArk** (inorganic); hardware revenue grew "roughly half" the disclosed 40% hardware-bookings growth, implying **subscription + support declined again** even in "the best cyber demand environment ever." Backlog build (lead-time extension assumed) is the bridge to a guided organic 4Q reacceleration; UBS models ~**$610M organic net-new ARR** for 4Q (vs ~$570M prior). On Mythos, Nikesh framed the impact as **"chaos"** and pushed back on the idea that 3Q results / 4Q guide directly benefit from urgency — immediate CISO playbook is test code, get patches; "cutting checks immediately is not really a thing," strategic decisions still 6+ months out. New markets: **sovereign clouds + neoclouds** (traditional CSPs historically don't buy firewalls for cloud environments) could lift the near-term product growth rate above the prior low-single-digit. Chronosphere's large-LLM customer went **~$100M → $200M ARR in the quarter, with another ~$100M of 4Q runway** before normalizing. CyberArk: framed as "more of a human-resource problem" to hit Street numbers, new head of sales starting July 1. At ~35x CY28 FCF, UBS sees "not a whole lot of wiggle room" despite better margins from CyberArk (UBS PANW review, 2026-06-03). [../relat%C3%B3rios%20bons/2026_06_03_panw_ubs_review_3_jun_26.html](../relat%C3%B3rios%20bons/2026_06_03_panw_ubs_review_3_jun_26.html)
- **UBS (Roger Boyd) cyber checks (2026-06-18):** Nikesh framed the current environment as "chaos" with teams focused on assessing their own risk/patching; bigger strategic Mythos-driven opportunities "will still take six months plus." UBS turns **slightly more cautious on Palo (and CrowdStrike)** vs the more-cautious-rated peers, on the view incremental cyber dollars may spread beyond the two platforms (identity + data get the most airtime) (UBS "Karl software call", 2026-06-18). [../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html](../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html)
- **Where the sell-side stands (post-print, 2026-06-03):** MS $320 OW · Barclays $315 OW · DB $350 Buy · JPM OW · Susquehanna Pos · Redburn Neutral. Skew decisively positive; the debate is organic-vs-inorganic quality, not direction.

## Catalysts / what to watch
- **FQ4 FY26 print — late August 2026** (FY-end Jul 31). Critical reads: **organic NNARR** (Barclays flags 4Q26 guide up $20M+; FY27 building toward $1.9B+ NNARR), seasonal Q4 strength, first clean view of CyberArk/Chronosphere in-period contribution.
- CyberArk + Chronosphere GTM cross-sell ramp (~1,000 cross-org engagements initiated as of Q3).
- AI-security monetization: Prisma AIRS, XSIAM/AgentiX, "Mythos/Fable" agentic-defense pipeline conversion.
- Long-term targets: NGS ARR **$20B by FY30**; 40%+ adjusted FCF margin by FY28 (Q1 FY26 call).
- Read-throughs: CRWD, FTNT, ZS, NET (platform/AI-security peers); PANW's print sets the cyber bar.

## Risks
- Organic growth deceleration masked by M&A; durability of product revenue vs pull-forward (Redburn; Barclays).
- Acquisition integration + dilution + GAAP losses; large goodwill/intangible base from CyberArk ($21.1B) and Chronosphere ($3.0B) (10-Q, 2026-06-03).
- Hardware cost inflation (memory/storage) pressuring product gross margin; price increases risk demand (Q3 FY26 call).
- Intense competition + scarce AI/ML engineering talent in the Bay Area; high attrition (10-K FY25 risk factors).
- Macro/geopolitical sensitivity of large enterprise + government deals; revenue-growth rate "may not be indicative of future performance" (10-K FY25 Item 1A).
- Concentration in NGS ARR as the market's primary lens — any organic ARR miss is outsized to the multiple.

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **BTG Mythos expert call** _(2026-06-18)_ + **Glasswing/Mythos cyber note** _(2026-06-04)_: AI-native cyber is reshaping the security value chain — PANW positioned as the platform consolidator.
- **Post-print sell-side reset** _(briefings, Jun-2026)_: PTs ~**$315–350** after a clean Q3; debate = organic vs M&A-flattered NGS ARR (CyberArk $21.1B + Chronosphere $3.0B).

## Intra-quarter — calls, commentary & reports (since the last print)
_Q3 FY26 · Jun 2 → Jul 20, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q3 FY26 · Jun'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **NGS ARR / quality** | NGS ARR $8.13B, +60% (incl. M&A) | UBS: 8 of the 30pts of product growth come from CyberArk, subs+support fell again · Redburn: "organic underwhelming" · IR: headline inflated by ~$1.6B of M&A | **✗ contests** (organic is the gap) |
| **Network security (SASE/NGFW)** | NGFW bkgs +40%; SASE $1.6B +40% | DB/Zelnick: "strongest Q3 in several years" in SASE, displacement vs ZS | **✓ confirms** (NetSec is the highlight) |
| **M&A / Mythos (agentic-AI)** | CyberArk/Chrono closed; "Mythos moment" | BTG: Nikesh cites 800 meetings since April · UBS: Nikesh calls it "chaos," strategic decisions 6+ months out · JPM (Essex, 06-30): Chinese-model-driven vuln acceleration keeps PANW the essential defensive layer, not a disruption target · Citrini (07-20): Project Glasswing (Anthropic) names PANW a key cyber partner; DSPM roll-up playbook | **⚠ nuance** (real demand, slow conversion) |
| **Operating margin** | guide 28.9–29.2% (M&A dilutive) | Barclays/Kalia: accelerating NetSec sustains FCF margins; FY27 +$1.9B NNARR | **⚠ nuance** (M&A dilution vs defensible FCF) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 06-03 | Morgan Stanley · Marshall/Weiss | valuation | bull | "Cleared all bogeys; customers clearly turning to PANW to secure AI adoption; single-digit cyber share = long runway". MS raised PT to US$320 (from US$253), OW; FY26E revenue +23.8%, FY27E +18.2%. |
| 06-03 | Deutsche Bank · Zelnick | competition | bull | "Broad platform strength; NetSec/Prisma SASE displacement is the key differentiator vs ZS; constructive on the FY27 acceleration". DB Buy, PT US$350 — "strongest Q3 in several years" in SASE. |
| 06-03 | JPM · Essex/Lee | guidance | bull | "Solid execution with AI tailwinds and M&A synergies ahead of plan" — XSIAM, Prisma AIRS, CyberArk all beating. JPM OW. |
| 06-03 | UBS · PANW Q3 FY26 review + callbacks (Nikesh/Depak + IR) | guidance | bear | Bear's Exhibit A on quality: of the 30% product growth, 8 points came from CyberArk (inorganic); hardware revenue grew "roughly half" of the 40% bookings, implying subscription + support fell again even in the "best cyber demand environment ever". UBS models ~US$610M of organic net-new ARR in 4Q. Mythos framed as "chaos"; "cutting checks immediately is not really a thing", strategic decisions still 6+ months out. New markets: sovereign + neoclouds. At ~35x CY28 FCF, UBS sees "not a whole lot of wiggle room". |
| 06-03 | Redburn/Rothschild | guidance | bear | "Beat-and-raise, but the organic business is underwhelming" — qualitative caution on the sustainability of product revenue. Neutral. |
| 06-04 | Glasswing/Mythos cyber note | demand | bull | AI-native cyber reshaping the security value chain — PANW positioned as the platform consolidator. |
| 06-08 | Barclays · Kalia | guidance | bull | IR-meeting takeaways: 4Q26 organic NNARR guide raised US$20M+ at the midpoint; FY27 could add US$1.9B+ of total NNARR; accelerating NetSec can sustain FCF margins. Barclays OW, PT US$315. |
| 06-17 | IR meeting (briefing 2026-06-17) | guidance | mixed | IR takeaways: organic subscription revenue deceleration partly explained by virtual-firewall rev-rec mechanics; NGS ARR/RPO headline flattered by M&A (~US$1.6B from CyberArk + Chronosphere). |
| 06-18 | BTG · Mythos expert call | demand | bull | Expert (ex-PANW): Nikesh "referenced 800 customer meetings since April" on Mythos/AI security; "this is now the Mythos moment" (also acknowledged on the CRWD call). Unit 42 Frontier AI Defense: 800+ meetings in six weeks. |
| 06-18 | UBS · Roger Boyd (cyber checks / Karl software call) | valuation | bear | Nikesh frames the environment as "chaos", teams focused on assessing their own risk/patching; larger strategic Mythos opportunities "will still take six months plus". UBS turns slightly more cautious on Palo (and CrowdStrike) vs peers, seeing incremental cyber dollars spreading beyond the two platforms (identity + data gaining more attention). |
| 06-30 | JPM · Brian Essex | demand | bull | "Chinese AI Models Catching Up, Vulnerabilities Accelerating" — open-weight Chinese models are closing the gap with frontier models in vulnerability discovery, and CVEs are already accelerating; enterprises face a coming "tsunami of vulnerabilities." JPM keeps **PANW (OW) and CRWD best positioned as essential defensive layers rather than disruption targets** as mean-time-to-exploit collapses. Adds TENB to the Analyst Focus List and upgrades QLYS Underweight→Neutral. (JPM / Brian Essex, 2026-06-30) |
| 07-06 | @TheTranscript_ (PANW CEO quote) | capital | neutral | Macro/AI-financing read (not PANW-specific): CEO Nikesh Arora says **hyperscalers have the balance-sheet capacity to finance their AI-infrastructure spending for the next 1-3 years, but new Frontier labs "will need to go public"** — he is "not sure there's more private-market capital available to support their capex needs." A capex-financing datapoint reflected to [hyperscaler-capex theme](themes/hyperscaler-capex.md). (@TheTranscript_, 2026-07-06) |
| 07-15 | Octahedron · 2Q26 LP call | demand | bull | READ-THROUGH: cyber names "quite well positioned" for the agent era. (Octahedron 2Q26 LP call, 2026-07-15) [Source](../relat%C3%B3rios%20bons/2026_07_15_octahedron_2q_review.html) |
| 07-20 | Citrini Semis ("All Along the AI Watchtower") | demanda | bull | Project Glasswing (Anthropic) names PANW a key cyber partner; the platform-consolidation playbook (DSPM roll-ups) continues; PANW has re-rated but is still favored. (Citrini Semis, 2026-07-20) [Source](../relat%C3%B3rios%20bons/Citrini_jul_20.html) |

**Quarter synthesis:** the debate has shifted from "direction" (positive skew, PTs $315–350) to **growth quality** — headline NGS ARR/RPO flattered by M&A, with UBS/Redburn pointing out that organic subs+support fell even in the "best cyber demand environment ever"; the upside now depends on the organic 4Q reacceleration (NNARR ~$610M UBS) and conversion of the Mythos pipeline, which management itself admits is 6+ months out. **06-30: JPM (Essex) reinforces the secular demand tailwind** — Chinese open-weight models are accelerating vulnerability discovery, and JPM keeps PANW (and CRWD) best positioned as the essential defensive layer (not a disruption target) as the vulnerability tsunami builds; it adds TENB to its focus list and upgrades QLYS to Neutral. **07-20:** Citrini flags PANW as Anthropic's Project Glasswing cyber partner + the DSPM platform-consolidation playbook (re-rated but still favored); the 07-15 Octahedron LP call adds a read-through that cyber names are "quite well positioned" for the agent era.

## Management commentary — evolution (last 4 quarters)

| Theme | Q4 FY25 (Aug'25) | Q1 FY26 (Nov'25) | Q2 FY26 (Feb'26) | Q3 FY26 (Jun'26) |
|---|---|---|---|---|
| NGS ARR (core KPI) | $5.6B exiting FY25 | $5.85B, +29% YoY | $6.33B, +33% (+28% organic) | $8.13B, +60% (incl. M&A) |
| Operating margin | >30% first time, +340bps | 30.2%, +140bps YoY | 30.3%, 3rd qtr >30% | guide 28.9–29.2% (M&A dilutive) |
| Platformization | bookings highest in 2.5 yrs | 16 net new; XSIAM doubled YoY | ~110 net new; ~1,550 total | 110 net new; ~2,280 total |
| Network security (Strata/SASE) | — | SASE ARR $1.3B, +34% | SASE $1.5B +40%; hw rev +10% | NGFW bkgs +40%; SASE $1.6B +40% |
| Cortex / AI SecOps (XSIAM) | — | ~470 cust, avg ARR >$1M | XSIAM ARR >$0.5B; 600+ cust | XSIAM ARR >$600M, +100% YoY |
| M&A / agentic-AI security | CyberArk/Chronosphere announced | Chronosphere+CyberArk pending | CyberArk closing; "control" shift | CyberArk/Chrono closed; "Mythos moment" |

_Source: PANW earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY25 (2025-08-29)](../PANW/PANW_10-K_2025-08-29_0001327567-25-000027.html); [10-Q FQ3 FY26 (2026-06-03)](../PANW/PANW_10-Q_2026-06-03_0001327567-26-000015.html).
- **Transcripts:** [Q3 FY26 (2026-06-02)](../PANW/transcripts/PANW_Q3-FY26-earnings_2026-06-02.md); [Q2 FY26 (2026-02-17)](../PANW/transcripts/PANW_Q2-FY26-earnings_2026-02-17.md); [Q1 FY26 (2025-11-19)](../PANW/transcripts/PANW_Q1-FY26-earnings_2025-11-19.md); [Q4 FY25 (2025-08-18)](../PANW/transcripts/PANW_Q4-FY25-earnings_2025-08-18.md).
- **Equity calls:** BTG Mythos expert call (2026-06-18) — agentic-AI security demand, "Mythos moment," 800 PANW customer meetings since April. · [Octahedron 2Q26 LP call (2026-07-15)](../relat%C3%B3rios%20bons/2026_07_15_octahedron_2q_review.html) — read-through: cyber names "quite well positioned" for the agent era.
- **Research reports (relatórios bons):**
  - [Barron's Tech Roundtable: Our 4 Experts on the Next Phase of AI and 22 Favorite Stocks](../relat%C3%B3rios%20bons/Barrons_Tech_Roundtable__Our_4_Experts_on_the_Next_Phase_of_AIand_22_Favorite_Stocks_-_Barrons.html)
  - [UBS — PANW Q3 FY26 review + callbacks (2026-06-03)](../relat%C3%B3rios%20bons/2026_06_03_panw_ubs_review_3_jun_26.html) — organic quality: CyberArk 8pts of 30% product growth, subs/support declined; Mythos = "chaos"; sovereign/neocloud new market; Chronosphere LLM customer $100M→$200M ARR.
  - [UBS (Roger Boyd) — software/AI team call (2026-06-18)](../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html) — Nikesh "chaos," 6mo+ strategic timeline; UBS slightly more cautious on PANW/CRWD as incremental dollars spread.
  - [Citrini Semis — "All Along the AI Watchtower" (2026-07-20)](../relat%C3%B3rios%20bons/Citrini_jul_20.html) — PANW as Anthropic's Project Glasswing cyber partner; platform-consolidation (DSPM roll-ups) playbook; re-rated but still favored.
- **Briefings:** 2026-06-03 (post-print sell-side roll-up, 12 emails), 2026-06-17 (IR-meeting takeaways), 2026-05-11 (FQ3 preview). No `_briefings/by-ticker/PANW.md` roll-up exists yet.
- **Outlook:** attempted (`outlook.py --no-body --days 14`); no usable output / session unavailable — email color to be added separately.

## Changelog
- **2026-07-20** — /run-inbox. Added **Citrini Semis "All Along the AI Watchtower" (2026-07-20, newsletter)** — bull: PANW as Anthropic's **Project Glasswing** key cyber partner + the platform-consolidation (DSPM roll-up) playbook, re-rated but still favored → new Debate Bull sub-bullet, M&A/Mythos Signal-row annotation, 1 intra-quarter full-log row (07-20, demanda/bull), synthesis line, Sources link. Also added **Octahedron 2Q26 LP call (2026-07-15)** as a read-through (cyber names "quite well positioned" for the agent era) — 1 full-log row (07-15) + Equity-calls Source link. Extended the intra-quarter window header → Jul 20. Additive; no PT/rating superseded. (First Changelog entry on this page.)
