<!-- per-company wiki page · synthesized from co-located disk sources only -->

# CRWD — CrowdStrike Holdings, Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\CRWD` (filings + transcripts) · `E:\briefings\2026`. Master index: [../00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $5.9bn | $7.2bn |
| Gross profit | $4.7bn | $5.7bn |
| Gross margin | 78.7% | 79.1% |
| EBITDA | $1.8bn | $2.2bn |
| EPS | $4.83 | $6.19 |
| Capex | $403m | $445m |
| OCF (≈EBITDA) | $1.8bn | $2.2bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

> **Fidelity flag:** the two transcripts read (Q1 FY27 2026-06-03, Q4 FY26 2026-03-03) are third-party reconstructions (fool.com via WebFetch) — close paraphrase, **not verbatim**; quotation marks retained only where the source carried them. The WebFetch summary mislabeled Q1 FY27 as "ended Jan 31 2027" — it ended **April 30 2026** (confirmed by the 10-Q filed 2026-06-04). Q3/Q2 FY26 saved from WebSearch headline summaries (metrics only). No CRWD-specific sell-side PT exists in the on-disk briefings — only read-throughs and expert-call invites (see Debate); a standing MS rating is now confirmed via disclosure tables (see Debate).

## Snapshot
CrowdStrike is the cloud-native cybersecurity platform built around **Falcon** — a single lightweight sensor that ingests endpoint, cloud-workload, identity and third-party telemetry once and reuses it across detection, investigation and response. The 10-K (FY26, 2026-03-05) positions Falcon as "the definitive platform for cybersecurity **consolidation**," displacing legacy point products. The model is ~95% subscription. Mix has broadened well beyond the EDR/XDR core: **Cloud security** (>$800m ARR), **Next-Gen SIEM** (>$600m), **Identity** (>$520m) plus the **Charlotte AI** agentic layer and the new **AIDR** (AI Detection & Response) line. It sits in the security-software layer of the AI stack — buying cloud infra/telemetry upstream, selling consolidation + agentic SecOps to enterprises downstream. Two structural angles: **platform consolidation** (Falcon Flex multi-module commitments) and **agentic-AI SecOps** (Charlotte AI as the reasoning engine; CRWD reframing itself as "critical AI infrastructure," Kurtz Q1 FY27).

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Falcon Endpoint/EDR-XDR (core sensor) · 2) Cloud security (>$800m ARR) · 3) Next-Gen SIEM (>$600m); + Identity, Charlotte AI, AIDR |
| **Main buyer(s)** | Enterprises buying platform consolidation (~95% subscription); no explicit customer concentration disclosed on the page |
| **Key suppliers** | Cloud infra / compute + third-party telemetry & data feeds (page does not name specific hyperscaler vendors) |

## Position in the value chain
Cloud infra + telemetry feed the Falcon cloud-native platform, which fans out across endpoint/XDR, identity, cloud security, Next-Gen SIEM and Charlotte AI, sold as a consolidation play into the enterprise. The edge vs. point-product rivals is **single-sensor data reuse + agentic automation**: Charlotte AI usage +6x y/y with ARR "more than tripled" (Q4 FY26), and AIDR "adoption happen[ing] this fast" — Kurtz frames the AIDR TAM as "structurally larger" than EDR (7 attack surfaces vs 1) as enterprises rush to secure their own AI deployments (Q1 FY27, 2026-06-03).

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 220" font-family="sans-serif" font-size="12">
  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#444"/>
    </marker>
  </defs>
  <!-- Suppliers -->
  <rect x="10" y="70" width="150" height="80" rx="6" fill="#eef3f8" stroke="#5b7c99" stroke-width="1.5"/>
  <text x="85" y="98" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="118" text-anchor="middle">Cloud infra</text>
  <text x="85" y="134" text-anchor="middle">Telemetry / data</text>
  <!-- CRWD platform -->
  <rect x="225" y="30" width="270" height="160" rx="8" fill="#fdf1e3" stroke="#d08a3e" stroke-width="2"/>
  <text x="360" y="52" text-anchor="middle" font-weight="bold">CrowdStrike — Falcon</text>
  <text x="360" y="68" text-anchor="middle" font-size="11">cloud-native, single sensor</text>
  <rect x="240" y="80" width="115" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="297" y="97" text-anchor="middle" font-size="10">Endpoint / XDR</text>
  <rect x="365" y="80" width="115" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="422" y="97" text-anchor="middle" font-size="10">Identity</text>
  <rect x="240" y="112" width="115" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="297" y="129" text-anchor="middle" font-size="10">Cloud security</text>
  <rect x="365" y="112" width="115" height="26" rx="4" fill="#fff" stroke="#d08a3e"/>
  <text x="422" y="129" text-anchor="middle" font-size="10">Next-Gen SIEM</text>
  <rect x="240" y="144" width="240" height="30" rx="4" fill="#f6e0c0" stroke="#d08a3e"/>
  <text x="360" y="163" text-anchor="middle" font-size="10" font-weight="bold">Charlotte AI — agentic SecOps</text>
  <!-- Customers -->
  <rect x="560" y="70" width="150" height="80" rx="6" fill="#eef8ef" stroke="#5a9367" stroke-width="1.5"/>
  <text x="635" y="98" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="635" y="118" text-anchor="middle">Enterprise</text>
  <text x="635" y="134" text-anchor="middle">(consolidation)</text>
  <!-- arrows -->
  <line x1="160" y1="110" x2="222" y2="110" stroke="#444" stroke-width="2" marker-end="url(#ar)"/>
  <line x1="498" y1="110" x2="557" y2="110" stroke="#444" stroke-width="2" marker-end="url(#ar)"/>
</svg>

## Current state (Q1 FY27, call 2026-06-03)
Record Q1, beat-and-raise. Total revenue $1.39bn (+26% y/y); subscription $1.32bn (+26%). **Ending ARR $5.51bn (+24% y/y, accelerating);** **net new ARR $256m (+32% y/y)** — record Q1, above guide. Non-GAAP op income $326m (24% margin, +62% y/y); non-GAAP EPS $1.10 (pre-split); **FCF $468.5m (34% margin, all-time high)**; non-GAAP gross margin 79% (sub 81%); Rule of 40 = 59 (Q1 FY27, 2026-06-03).
- **FY27 guide raised:** net new ARR to $1.279–1.303bn (+27–29% midpoint), up >520bps / >$50m vs the initial Q4 guide of $1.21–1.26bn; revenue $5.915–5.959bn (+23–24%); FCF margin ≥30% (Q1 FY27 vs Q4 FY26, 2026-03-03).
- **Falcon Flex (consolidation engine):** ending ARR **$1.9bn (+99% y/y)**, 300+ new accounts; ReFlex base 480 (25% of Flex), avg +26% ARR uplift; 130+ multi-reflexers avg +51% over initial contract (Q1 FY27). At Q4 FY26: Flex $1.69bn (+120%), 1,600+ adopters, avg ARR >$1m.
- **Emerging modules:** Cloud + SIEM + Identity combined ARR **>$2bn**; Next-Gen SIEM **>$600m**; **AIDR +250%+ sequentially** with Q2 pipeline >$50m; FalconShield ARR nearly quadrupled y/y; Signal + Seraphic acquisitions added $7.8m NN ARR (Q1 FY27).
- **Capital/structure:** 4-for-1 forward split effective 2026-07-02; cash $4.55bn; ex-NVIDIA Bartley Richardson hired as Chief AI & Autonomous System Officer (Q1 FY27).
- **CEO framing of the July 2024 outage, in hindsight (Barron's "Top CEOs of 2026," George Kurtz profile, 2026-06-22):** "The biggest lesson learned is you gotta get in front of this stuff; you have to take accountability for it... The biggest thing that came out of this was earning even more trust from our customers because we didn't shy away from it." The outage "took down more than eight million Windows computers"; the stock recovered within 4 months, and "if you bought it the day before the disaster, your money has doubled" (Barron's, 2026-06-22).

## Debate / thesis
- **AI-software read-through — agent cybersecurity as a new category (Vercel CEO Guillermo Rauch, Stanford MS&E435, 2026-06-29):** agents with their own computers/sandboxes create new attack surface (data exfil, prompt-injection, abused tool/API access) needing isolation, exfil-prevention, governance and guardrails — a PC-era "viruses & phishing" analogue. Tailwind read-through for CRWD's agentic-SecOps / Charlotte AI and AI-runtime-security ambitions. See [tokenmaxxing theme](themes/tokenmaxxing.md).
- **Bull:** Net-new-ARR re-acceleration with margin leverage — NN ARR +32% y/y on a $5.5bn base, FCF margin 34%, op margin +62% y/y (Q1 FY27). Consolidation is compounding: Flex ARR +99–120% y/y, module attach deepening (Q4 FY26: 50% of customers on 6+ modules, 34% on 7+, 24% on 8+). Durable retention at scale — gross retention 97%, net retention 115% (Q4 FY26). AI-security is the new growth vector: Charlotte AI usage +6x / ARR >3x y/y, AIDR "adoption happen[ing] this fast," CRWD reframed as "critical AI infrastructure" (Kurtz, Q1 FY27). Persistent 52-week-high / momentum-leader callouts through May 2026 (StockMKTNewz lists, briefings 2026-05-15→05-22). FTNT print read-through "positive for PANW/S/CRWD" (Bernstein/Seidman, briefing 2026-05-14).
- **Bear:** (1) The **July 19, 2024 outage** is still the *lead* risk factor in both the FY26 10-K (2026-03-05) and the Q1 FY27 10-Q (2026-06-04) — "expected to continue to have an adverse effect," with open lawsuits/claims and ongoing "customer commitment packages" and a "Strategic Plan." (2) Valuation/crowding — name repeatedly on 52-week-high lists; ZS flagged as "most crowded short in security" by peers, a tape-risk proxy for the group (briefing 2026-05-19). (3) Intense competition + reliance on customers renewing *and adding modules* — the consolidation thesis cuts both ways if attach stalls (10-K risk factors). (4) As a cyber vendor, CRWD is itself a perennial attack target; a perceived failure-to-detect would hit brand/retention (10-K).
- **Read-through color (third-party, attributed):**
  - WFC software-conf recap (2026-04-13): the CrowdStrike meeting was "very upbeat" on Project Glasswing/Mythos; cyber was "the one bright spot where people talk more about the AI opportunity than the AI risk" — every vendor views Mythos/Glasswing as a **net positive for cyber budgets** (lower hacker skill floor → expanded attack surface → CISO urgency). On the Glasswing logo list, only CrowdStrike and Palo were named among the dozen-plus vendors, making it "difficult to figure out who else to own" (WFC "software" call, 2026-04-13). [../relat%C3%B3rios%20bons/2026_04_13_software_wfc_13_apr_26.html](../relat%C3%B3rios%20bons/2026_04_13_software_wfc_13_apr_26.html)
  - Jefferies (Brent Thill / "Cyber Joe", 2026-06-01): Jefferies' CIO at their conference named **CrowdStrike his "go-to in a deserted island with one raft"** (endpoint + cloud + ITDR, most-used, most willing to expand) while wanting to cut 80 cyber tools to ~5; key structural point — even if Anthropic/OpenAI "took over the enterprise world, you would still need a third-party security auditor," so frontier-lab dominance doesn't displace CRWD (Jefferies "Brent/Jeff AI" call, 2026-06-01). [../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html)
  - UBS (Roger Boyd, 2026-06-18): a dozen-plus CISO checks show cyber budgets "in a better place than a few months ago" (board-level Mythos urgency), but security teams remain resource-constrained and 6–12 month sales cycles don't compress to weeks (ZS CEO: Mythos "a bigger demand driver than COVID" but slower-burn; Nikesh @ PANW: "chaos"). Net: UBS turns **slightly more positive on the more-cautious non-CRWD/PANW vendors and slightly more cautious on CrowdStrike and Palo** on the view that incremental dollars may spread (cyber is "consistently a fill-in-the-gaps procurement motion"; identity + data get the most airtime) (UBS "Karl software call", 2026-06-18). [../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html](../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html)
- **Where the sell-side/buy-side stands:** No dedicated CRWD note on disk, but a **standing Morgan Stanley rating is now confirmed: Overweight since 2024-01-09**, last reference price $434.74 — surfaced only in the MS coverage/disclosure tables of an unrelated MSFT–OpenAI note (MS GVAT/US Enterprise Software, Baer/Castagno, 2025-04-30); that note carries no CRWD thesis, PT or commentary. Otherwise on-disk coverage is read-through and expert-channel only: Barclays/Kalia ran a Westcon Europe cyber-distributor April-Q channel call (PANW/CRWD/ZS/OKTA, briefings 2026-05-07→05-11); JPM/Essex security-software webinar incl. CRWD (2026-05-15); JPM "State of Security" cross-ref (PANW/NET/CRWD). All-In Pod (David Sacks) cited PANW/CRWD in the "FDA for AI" / Mythos framing — frontier labs gaining cyber capability in 3–6 months drives systems-hardening demand (briefing ~mid-May 2026). Octahedron's Databricks deep-dive plots CRWD only as a dot in its data-infra-software EV/Revenue and EV/Rev/Growth (CY25E) comp scatters — no CRWD thesis; included as a high-multiple SaaS reference point.
  - **First dedicated CRWD rating on disk — Sell (Rothschild & Co Redburn, US Morning desk, 2026-07-01):** flags the 4-for-1 forward stock split executing after market close on 2026-07-01 (stock ~$760/share pre-split → implies ~$190–200/share post-split); values CRWD at **33x EV/sales NTM — ~3x the cyber-peer average — and a 1% FCF yield**, the explicit basis for the Sell. This is the first EV/sales or FCF-yield multiple logged for CRWD on this page (prior valuation references were the MS Overweight rating/ref-price only, with no explicit multiple) — Redburn's framing stands opposite the MS Overweight and the bull consolidation/AI-tailwind case above (Rothschild & Co Redburn, US Morning desk, 2026-07-01).
  - **Momentum/technical context (Rothschild & Co TMT Daily, Rowan Adley, 2026-07-01):** CRWD hit a 12-month relative high alongside AMD/AMAT/LRCX/KLAC/PANW/APH as the SOX rallied +3.9% on the DRAM-capacity-addition trade — a sector-momentum tailwind that sits in tension with Redburn's same-day Sell call on valuation.

## Catalysts / what to watch
- **Q2 FY27 print** — by cadence ~late Aug/Sep 2026 (Q2 FY26 was 2025-08-27). Guide: net new ARR $284–286m (+28–29%), revenue $1.436–1.442bn, FCF margin ~24.5% (seasonally low) (Q1 FY27 guide).
- **4-for-1 stock split** effective 2026-07-02 — executes after market close 2026-07-01; stock ~$760/share pre-split implies ~$190-200/share post-split (Rothschild & Co Redburn, 2026-07-01).
- **AIDR ramp** — first full quarters of the new AI-detection line; watch the >$50m Q2 pipeline convert; whether Charlotte AI agentic monetization scales beyond the >3x ARR base (Q1 FY27).
- **Flex/ReFlex durability** — reflex uplift cadence (+26% avg, +51% multi-reflex) is the leading indicator for the consolidation flywheel.
- **Outage tail** — resolution of July-19-related litigation and run-off of customer commitment packages (10-Q, 2026-06-04).

## Risks
- July 19 Incident: ongoing adverse effect, litigation/claims, customer commitment package run-off, "Strategic Plan" execution (10-K FY26 + 10-Q Q1 FY27).
- History of GAAP losses; profitability not assured in all periods (10-K).
- Dependence on customers renewing subscriptions *and* adding modules; failure to land new logos.
- Intense competition / potential market-share loss; long, unpredictable sales cycles.
- Product failure (real or perceived) to detect/prevent incidents → brand/retention damage.
- CRWD itself is a high-value cyberattack target; compromise of its systems would damage reputation and results (10-K).
- **Operational-resilience track record (bull-side counterpoint, Barron's "Top CEOs of 2026," 2026-06-22):** Kurtz frames the July 2024 outage (8m+ Windows machines down) as a trust-building moment in hindsight — "earning even more trust from our customers because we didn't shy away from it" — and the stock recovered within 4 months of the disaster. Tension with the 10-K/10-Q framing above (still the *lead* risk factor, "expected to continue to have an adverse effect," open litigation) — same event, opposite framing depending on audience (Barron's, 2026-06-22 vs. 10-K FY26/10-Q Q1 FY27).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

> **AI-monetization angle:** CRWD is a securing-AI / agentic-SecOps play rather than a token-consumption story — Charlotte AI ARR >3x y/y and AIDR are sold as protection for enterprise AI buildouts. See cross-theme: [tokenmaxxing](themes/tokenmaxxing.md) (CRWD not in the exposure table; relevance is the demand pull from frontier-lab AI adoption, "Mythos Moment," Q1 FY27).

## In the inbox (Outlook — recent sell-side flow)
- **Morgan Stanley TMT** _(2026-06-05)_: 'CRWD bullish on AI demand.'
- **BTG Mythos expert call** _(2026-06-18)_: AI-driven-attack escalation = secular tailwind for AI-native cyber (Falcon / Charlotte AI / AIDR).

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY27 · Apr 13 → Jun 18, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1 FY27) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Growth / ARR** | Rev $1.39bn, +26% (accelerating); ending ARR $5.51bn (+24%); net new ARR $256M (+32%, record Q1) | Jefferies (Cyber Joe): CRWD "go-to in a deserted island", wants to cut 80 tools to ~5 · Bernstein: the FTNT print is positive for CRWD | **✓ confirms** (consolidation preference) |
| **AI as tailwind** | AIDR +250%+ q/q; Kurtz repositions CRWD as "critical AI infra" | WFC: cyber is the "bright spot" where there's more talk of opportunity than AI risk · BTG: AI attacks = secular tailwind · JPM (Essex, 06-30): Chinese-model-driven vuln acceleration keeps CRWD an essential defensive layer, not a disruption target | **✓ confirms** (AI is an opportunity) |
| **Budgets / demand** | FY27 guide raised: net new ARR $1.279-1.303bn | UBS (Boyd): budgets "better than a few months ago" but teams resource-constrained, 6-12m cycles don't compress; incremental dollars may spread | **⚠ nuance** (incremental spreads out) |
| **Consolidation / Flex** | Falcon Flex ARR $1.9bn (+99%); 480 ReFlex | Jefferies: CISOs want to cut the stack to ~5 vendors (CRWD/PANW cited) | **✓ confirms** (Flex captures consolidation) |
| **Operational resilience** | 10-K/10-Q: July-19 outage still the lead risk factor, litigation ongoing | Barron's "Top CEOs of 2026" (Kurtz): outage reframed as a trust-building moment; stock recovered within 4 months | **⚠ nuance** (mainstream press bullish on the recovery story vs. filings' cautious legal framing) |
| **Valuation** | FY27 guide raised; FCF margin ≥30%; Rule of 40 = 59 (Q1 FY27) — no explicit multiple given by management | Rothschild & Co Redburn (2026-07-01): Sell — 33x EV/sales NTM (~3x cyber-peer avg), 1% FCF yield, flagged into the 4-for-1 split | **✗ contests** (first dedicated Sell/multiple call on disk; opposes MS Overweight and the bull consolidation case) |
| **Competition / AI tailwind** | AIDR +250%+ q/q; Kurtz: "critical AI infra" | JPM (Manicardi, 07-01): adds TENB to Focus List, upgrades QLYS on Chinese-AI-driven vuln-discovery urgency — consistent with JPM/Essex (06-30) keeping CRWD/PANW as essential defensive layer | **✓ confirms** (AI-driven vuln acceleration = cyber-spend tailwind, not a share-loss risk to CRWD) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 04-13 | WFC · software conf recap | demand | bull | WFC reported that its meeting with CrowdStrike at the conference was "very upbeat" on Project Glasswing/Mythos; cyber was "the one bright spot where people talk more about the AI opportunity than the AI risk" — Mythos seen as a net positive for cyber budgets. On the Glasswing logo list, only CrowdStrike and Palo were cited, making it "difficult to figure out who else to own". |
| 05-05 | Morgan Stanley · TMT | demand | bull | Morgan Stanley TMT (Outlook): 'CRWD bullish on AI demand.' |
| 05-14 | Bernstein · Seidman | competition | bull | Bernstein/Seidman: the FTNT print is a "positive for PANW/S/CRWD" read. |
| 06-01 | Jefferies · Brent Thill / "Cyber Joe" | demand | bull | Jefferies' CIO at the conference named CrowdStrike as his "go-to in a deserted island with one raft" (endpoint + cloud + ITDR), wanting to cut 80 cyber tools down to ~5. Structural point: even if Anthropic/OpenAI dominated the enterprise, "you would still need a third-party security auditor" — frontier-lab dominance does not displace CRWD. |
| 06-18 | UBS · Roger Boyd | valuation | bear | UBS (over a dozen checks with CISOs): cyber budgets "in a better place than a few months ago" on board-level Mythos urgency, but teams remain resource-constrained and 6-12 month cycles are not compressing. Net: UBS turns slightly more positive on the non-CRWD/PANW vendors and slightly more cautious on CrowdStrike and Palo, on the view that the incremental dollars may spread out. |
| 06-18 | BTG · Mythos expert call | demand | bull | BTG Mythos expert call (Outlook): escalation of AI-driven attacks = secular tailwind for AI-native cyber (Falcon / Charlotte AI / AIDR). |
| 06-30 | JPM · Brian Essex | demand | bull | "Chinese AI Models Catching Up, Vulnerabilities Accelerating" — open-weight Chinese models closing the vuln-discovery gap vs frontier models; CVEs already accelerating, enterprises bracing for a "tsunami of vulnerabilities." JPM keeps **CRWD (and PANW) best positioned as essential defensive layers rather than disruption targets** as mean-time-to-exploit collapses; adds TENB to the Analyst Focus List, upgrades QLYS to Neutral. Corroborates the AI-as-tailwind (not AI-as-risk) thesis. (JPM / Brian Essex, 2026-06-30) |
| 06-22 | Barron's · "Top CEOs of 2026" (George Kurtz profile) | risk | mixed | Kurtz on the July 2024 outage (8m+ Windows computers down): "The biggest lesson learned is you gotta get in front of this stuff; you have to take accountability for it... The biggest thing that came out of this was earning even more trust from our customers because we didn't shy away from it." Stock recovered within 4 months; "if you bought it the day before the disaster, your money has doubled." (Barron's, 2026-06-22) |
| 07-01 | Rothschild & Co Redburn · US Morning desk | valuation | bear | Initiated/flagged Sell on CRWD. 4-for-1 forward stock split executes after market close today (2026-07-01); stock ~$760/share pre-split implies ~$190-200/share post-split. Values CRWD at 33x EV/sales NTM — ~3x the cyber-peer average — and a 1% FCF yield; explicit basis for the Sell call. |
| 07-01 | Rothschild & Co · TMT Daily (Rowan Adley) | demand | bull | CRWD hit a 12-month relative high alongside AMD/AMAT/LRCX/KLAC/PANW/APH as the SOX rallied +3.9% on the DRAM-capacity-addition trade — sector-momentum tailwind, same day as Redburn's Sell-on-valuation call. |
| 07-01 | JPMorgan · Intl Market Intelligence (Federico Manicardi) | competicao | bull | JPM added TENB to its Analyst Focus List and upgraded QLYS, citing rising urgency for cybersecurity spend as Chinese AI models close the gap in vulnerability-discovery capabilities — sector read-through/competitive context consistent with JPM/Essex's 06-30 note keeping CRWD (and PANW) positioned as the essential defensive layer rather than a disruption target. |

**Quarter synthesis:** a beat-and-raise print with accelerating ARR confirms the consolidation thesis (Jefferies/CISOs want ~5 vendors) and AI as a cyber tailwind; the only nuance came from UBS (Boyd), who sees better budgets but warns the incremental dollars may spread to non-CRWD/PANW vendors, turning slightly more cautious on the leading pair. **06-30: JPM (Essex) adds a fresh secular tailwind** — Chinese open-weight models are accelerating vulnerability discovery, keeping CRWD (and PANW) best positioned as the essential defensive layer, not a disruption target (adds TENB to focus list, upgrades QLYS to Neutral). Same day, **Barron's "Top CEOs of 2026"** profiles Kurtz reframing the July 2024 outage as a trust-building moment (recovered in 4 months) — mainstream-press validation of the resilience narrative that sits alongside, not in place of, the filings' more cautious ongoing-litigation framing. **07-01: first dedicated CRWD rating call lands, and it's a Sell** — Rothschild & Co Redburn values CRWD at 33x EV/sales NTM (~3x cyber-peer avg) / 1% FCF yield, flagged same-day as the 4-for-1 forward split executes after the close; this is the first explicit multiple/rating on the page distinct from the standing (but thesis-free) MS Overweight. Same-day tape context cuts the other way — Rothschild's own TMT Daily (Adley) has CRWD at a 12-month relative high with the SOX +3.9% on the DRAM-capacity trade, and JPM (Manicardi) reinforces the AI-driven-vuln-acceleration tailwind by adding TENB to its Focus List and upgrading QLYS — so the Sell is a valuation call layered on top of, not a reversal of, the demand/momentum picture.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2 FY26 (2025-08-27) | Q3 FY26 (2025-12-02) | Q4 FY26 (2026-03-03) | Q1 FY27 (2026-06-03) |
|---|---|---|---|---|
| Revenue growth | $1.17bn, +21% y/y | $1.23bn, +22% y/y | $1.31bn, +23% y/y | $1.39bn, +26% y/y (accelerating) |
| Net new ARR | $221m; 2H ≥40% guide | $265m, +73% y/y, record Q3 | $331m, +47% y/y, all-time record | $256m, +32% y/y, record Q1 |
| Ending ARR | >22% FY26 growth guide | $4.92bn, +23% y/y | $5.25bn, +24% — first cyber >$5bn | $5.51bn, +24%, accelerating |
| Falcon Flex (consolidation) | — | — | $1.69bn ARR, +120%; 1,600+ adopters | $1.9bn ARR, +99%; 480 ReFlex |
| AI (Charlotte / AIDR) | AI-driven demand cited | — | Charlotte usage >6x; ARR >3x; AIDR 5x | AIDR +250%+ q/q; "critical AI infra" |
| Profitability / FCF | — | CFO $398m, FCF $296m (records) | 25% op margin; FCF $1.24bn (26%) | FCF $468.5m (34%, record); Rule of 40=59 |

_Source: CRWD earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY26 (2026-03-05)](../CRWD/CRWD_10-K_2026-03-05_0001535527-26-000010.html) — Falcon platform overview + risk factors · [10-Q Q1 FY27 (2026-06-04)](../CRWD/CRWD_10-Q_2026-06-04_0001535527-26-000025.html) — July 19 / Strategic Plan language.
- **Transcripts:** [Q1 FY27 (2026-06-03)](../CRWD/transcripts/CRWD_Q1-FY27-earnings_2026-06-03.md) · [Q4 FY26 (2026-03-03)](../CRWD/transcripts/CRWD_Q4-FY26-earnings_2026-03-03.md) — both read · [Q3 FY26 (2025-12-02)](../CRWD/transcripts/CRWD_Q3-FY26-earnings_2025-12-02.md) · [Q2 FY26 (2025-08-27)](../CRWD/transcripts/CRWD_Q2-FY26-earnings_2025-08-27.md) — saved, headline-only. _All third-party paraphrase — see fidelity flag._
- **Equity calls:** 0 attributed (no CRWD section in INDEX).
- **Briefings:** `E:\briefings\2026` — ~56 .md files mention CRWD, all read-through / expert-call / 52-week-high references (no dedicated PT). No `by-ticker/CRWD.md` roll-up on disk.
- **Research reports (relatórios bons):**
  - [Morgan Stanley — MSFT & OpenAI](../relat%C3%B3rios%20bons/MSFT_OAI.html) — CRWD only in MS disclosure/coverage tables: Overweight since 2024-01-09, ref price $434.74; no CRWD thesis.
  - [Octahedron — Databricks](../relat%C3%B3rios%20bons/Octahedron_on_DataBricks.html) — CRWD appears only as a comp dot in data-infra-software EV/Revenue & EV/Rev/Growth scatters; no CRWD thesis.
  - [WFC — software conf recap (2026-04-13)](../relat%C3%B3rios%20bons/2026_04_13_software_wfc_13_apr_26.html) — CRWD "very upbeat" on Glasswing/Mythos; cyber the bright spot; only CRWD + Palo on the Glasswing logo list.
  - [Jefferies (Brent Thill) — AI software/infra call (2026-06-01)](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html) — CIO's "deserted island" pick; third-party security audit still needed even if labs win enterprise.
  - [UBS (Roger Boyd) — software/AI team call (2026-06-18)](../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html) — cyber budgets improving on Mythos urgency but slow-burn; UBS slightly more cautious on CRWD/PANW as the incremental dollars may spread.
  - [Barron's, June 22 2026 issue](../relat%C3%B3rios%20bons/Barrons_22_June_2026.html) — "Top CEOs of 2026" profile of George Kurtz: July-2024-outage accountability quote, 4-month stock recovery, "money has doubled" framing.
- **Outlook (2026-07-01):** Rothschild & Co Redburn (US Morning desk) — CRWD Sell, 4-for-1 split note, 33x EV/sales NTM / 1% FCF yield · Rothschild & Co TMT Daily (Rowan Adley) — 12-month relative high alongside SOX peers · JPMorgan Intl Market Intelligence (Federico Manicardi) — TENB Focus List add / QLYS upgrade on Chinese-AI vuln-discovery read-through.

## Changelog
- **2026-06-30 (later)** — Added Barron's "Top CEOs of 2026" George Kurtz profile (2026-06-22 issue): outage-accountability quote, trust-building reframe, 4-month recovery. Patched into Current state and Risks (as a bull-side counterpoint to the filings' cautious litigation framing), Sinal-vs-gestão table, intra-quarter log, quarter synthesis, and Sources.
- **2026-07-01** — Added first dedicated CRWD rating/multiple on this page: Rothschild & Co Redburn (Sell) at 33x EV/sales NTM (~3x cyber-peer avg) / 1% FCF yield, tied to the 4-for-1 forward split executing after close 2026-07-01 (implies ~$190-200/share post-split vs. ~$760 pre-split). No prior EV/sales or FCF-yield figure existed on this page to supersede — the only pre-existing valuation reference was the thesis-free MS Overweight rating/ref-price ($434.74, since 2024-01-09), which stands alongside (not replaced by) the new Sell. Also added: Rothschild TMT Daily (Adley) 12-month-relative-high/SOX-momentum note, and JPMorgan (Manicardi) TENB Focus List add / QLYS upgrade on Chinese-AI vulnerability-discovery urgency. Patched into Debate/thesis, Catalysts (split-timing color), Sinal-vs-gestão table, intra-quarter full log, quarter synthesis, and Sources.
