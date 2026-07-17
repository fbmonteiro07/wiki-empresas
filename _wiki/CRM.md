<!-- per-company wiki page · synthesized from co-located disk sources only -->

# CRM — Salesforce, Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\CRM` (filings + transcripts) · `E:\briefings\2026` (morning + company-specific). Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $46.0bn | $50.4bn |
| Gross profit | $36.1bn | $38.4bn |
| Gross margin | 78.4% | 76.2% |
| EBITDA | $19.0bn | $20.8bn |
| EPS | $13.42 | $15.79 |
| Capex | $692m | $744m |
| OCF (≈EBITDA) | $19.0bn | $20.8bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

> **Fidelity flag:** the transcripts used (Q1 FY27, Q4 FY26) are third-party reconstructions (fool.com / investing.com via WebFetch) — close paraphrase, **not verbatim**, with quotation marks only where the source has them. Treat figures as directional. **Outlook:** attempted (`outlook.py --no-body --days 14`) — returned no output in this environment, so no email-sourced notes; sell-side stances below are from the on-disk briefings.

## Snapshot
Salesforce is the global leader in CRM software, repositioning from "Customer 360" toward the **agentic enterprise** — the Agentforce 360 Platform unifies Sales, Service, Marketing, Commerce, Slack, Tableau/Analytics, Data Cloud (Data 360) and the Agentforce agentic layer on one platform (10-K FY26, 2026-03-02). Model is ~100% subscription, sold direct + via partners/AppExchange. FY26 revenue $41.5bn, +10% y/y (+9% cc); the company guides FY27 ~$46bn (+10–11%) and a **FY30 target of $63bn** (~11% CAGR) (Q4 FY26, 2026-02-25). It sits in the **application-software** layer — the front-line of the AI-monetization / "SaaS-apocalypse" debate ([tokenmaxxing](themes/tokenmaxxing.md)): is agentic AI a new ARR pool stacked on the seat base, or does autonomous labor cannibalize the seats it sells today?

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Core CRM clouds (Sales / Service / Marketing) · 2) Agentforce (agentic-AI layer, ARR $1bn+) · 3) Data 360 / Data Cloud (+ Informatica) |
| **Main buyer(s)** | Enterprises (sales / service / marketing teams), sold direct + via partners/AppExchange; ~100% subscription |
| **Key suppliers** | Cloud infra (AWS / self-run Hyperforce DCs) + frontier LLMs (Anthropic ~$300M/yr) |

## Position in the value chain
Salesforce buys/operates cloud infrastructure (Hyperforce runs inside third-party data centers — primarily AWS — plus self-operated capacity; 10-K FY26) and frontier LLMs (Benioff: "~$300M of Anthropic this year at Salesforce", @theallinpod via briefing 2026-05-16), packages them into CRM clouds + Data 360 + Agentforce, and sells subscriptions to enterprises. **Agentforce is the swing factor**: the agentic-AI bull (digital labor = new consumption ARR on top of seats) vs the SaaS-seat-cannibalization bear (agents replace the human seats CRM monetizes). Structurally, CRM is one of the few players that can occupy *both* of the agentic-era roles Bain says most vendors must choose between — the **neutral agent platform** and the **proprietary-data supplier** that powers agents ("only a few giants (Salesforce, for example) can realistically do both"; Bain Technology Report 2025).

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12">
  <rect x="10" y="55" width="160" height="100" rx="6" fill="#eef2f7" stroke="#5b7799"/>
  <text x="90" y="78" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="90" y="98" text-anchor="middle">Cloud infra (AWS /</text>
  <text x="90" y="114" text-anchor="middle">Hyperforce own DCs)</text>
  <text x="90" y="134" text-anchor="middle">+ frontier LLMs</text>
  <text x="90" y="150" text-anchor="middle">(Anthropic ~$300M)</text>

  <rect x="250" y="35" width="220" height="140" rx="6" fill="#dbe7d5" stroke="#4a7a3a"/>
  <text x="360" y="58" text-anchor="middle" font-weight="bold">Salesforce</text>
  <text x="360" y="80" text-anchor="middle">CRM clouds: Sales /</text>
  <text x="360" y="96" text-anchor="middle">Service / Marketing</text>
  <text x="360" y="116" text-anchor="middle">+ Data Cloud (Data 360)</text>
  <text x="360" y="138" text-anchor="middle" font-weight="bold">+ Agentforce</text>
  <text x="360" y="158" text-anchor="middle" font-style="italic">(the swing factor)</text>

  <rect x="550" y="55" width="160" height="100" rx="6" fill="#f5ead9" stroke="#a8772f"/>
  <text x="630" y="92" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="630" y="114" text-anchor="middle">Enterprise</text>
  <text x="630" y="130" text-anchor="middle">(sales / service /</text>
  <text x="630" y="146" text-anchor="middle">marketing teams)</text>

  <line x1="170" y1="105" x2="248" y2="105" stroke="#333" stroke-width="2" marker-end="url(#ar)"/>
  <line x1="470" y1="105" x2="548" y2="105" stroke="#333" stroke-width="2" marker-end="url(#ar)"/>

  <text x="360" y="200" text-anchor="middle" font-style="italic" fill="#666">Bull: agentic AI = new consumption ARR on the seat base · Bear: agents cannibalize SaaS seats</text>

  <defs>
    <marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#333"/>
    </marker>
  </defs>
</svg>

## Current state (Q1 FY27, call 2026-05-27)
Beat that "cleared the bar but didn't change the AI debate" — stock ~flat to -3% (briefing 2026-05-28).
- **Revenue $11.13bn, +13% y/y (+12% cc)** — above guide; corroborated by 10-Q (period ended 2026-04-30, total revenues $11,133m). **cRPO $33.6bn, +13% cc** — in-line, soft vs buyside hopes of 13–14% (Q1 FY27 call; briefing 2026-05-28: "cRPO at lower end of buyside").
- **Agentforce ARR surpassed $1bn** (from ~$800m at Q4 FY26 and ~$540m at Q3 FY26); **AI & Data ARR $3.4bn**, ~50% from existing customers expanding (Q1 FY27). **28.6tn tokens** processed (+152% q/q); **3.8bn Agentic Work Units** (+111% q/q) — the new agentic-consumption gauge.
- **Margins/cash:** non-GAAP op margin 34.8% (+250bps y/y); GAAP 21.1%. OCF $6.7bn. **$25bn ASR** cut diluted shares ~10% y/y (~103m shares retired) — capital return doing real work on EPS while top-line growth normalizes to low-teens (Q1 FY27).
- **Pricing:** hybrid — premium agentic SKUs (A1E / A4x bookings +~60% y/y), Agentic Enterprise License Agreements, plus consumption (tokens/work-units). Not pure seat, not pure consumption (Q1 FY27; Q3 FY26 call). Third-party color: CRM is among the vendors already shifting from seat-based toward outcome/usage pricing ("~$2 per conversation" charge-per-action model; JPM, Ogg, 2025-09-03; Bain Technology Report 2025).
- **Soft spots:** Marketing, Commerce and **Tableau** bookings/renewals still weak; offset by Agentforce/Data 360/Slack. Sales Cloud growth re-accel to ~10% from 8% (briefing 2026-05-28).
- **Informatica** (closed Q3 FY26, 3 months early): ~$1.1bn Data 360/Informatica Cloud ARR; on-prem contribution helped the headline (Q4 FY26, Q1 FY27).
- **Guidance:** FY27 revenue raised to ~$45.9–46.2bn; Q2 ~$11.3bn (~10% cc); non-GAAP op margin 34.3% reiterated; FY27 FCF >$16.5bn (Q4/Q1 FY27). FY30 target $63bn (Q4 FY26).

## Debate / thesis
- **Bull:** Agentforce is a genuine new ARR pool — $0→$1bn+ in ~18 months, work-units and tokens compounding triple-digits q/q; Data 360 + Informatica give the proprietary-context moat that makes agents useful ("the last mile is hard… companies need the context", Milano, Q3 FY26). SaaStr's Lemkin: Agentforce "could be worth 3-4x the software business long-term" (Q4 FY26). 34%+ margins + $50bn buyback authorization + $25bn ASR = a self-help EPS/FCF story even at ~10% growth. R&Co Redburn Buy: "Q1 clears the bar, H2 acceleration on track" (briefing 2026-05-28). MS (Weiss) **OW PT $287** (2026-05-28).
  - **The "incumbents-win" framework (third-party):** JPM's agentic-disruption matrix concludes that "software companies that offer entrenched, multi-product, multi-layer solutions to an enterprise customer base are best insulated" — point-solution, single-layer, SMB-skewed vendors face the real disruption risk; CRM (enterprise, multi-product, multi-layer, owns the system of record) sits on the protected side (JPM, Ogg, 2025-09-03). Bain frames it as a fork — agentic players must "either become the neutral agent platform or supply the unique data that powers it," and "only a few giants (Salesforce, for example) can realistically do both" (Bain Technology Report 2025). UBS's enterprise-IT checks are the cleanest pushback on the bear: "we're really not hearing seat-displacement anecdotes and none talked about AI applications displacing incumbent SaaS… the Street could now be over-indexing too cautious" — and notes OpenAI itself runs on third-party Salesforce (UBS, 2025-09). Bernstein's 247-page Gen-AI Handbook adds a measured incumbent read on CRM specifically: AI is **"both a small headwind and a mostly offsetting small tailwind (Agentforce)"** for Salesforce — i.e. roughly net-neutral, not the existential disruption the bears price — while SAP and Oracle screen as "best positioned" among SaaS incumbents (Bernstein "Scaling Intelligence", 2026-06-22). Bernstein also flags CRM's **credit-based GenAI pricing** (base fee + consumption credits, like Workday/Adobe) as a **margin-defensive** structure vs Microsoft's flat-fee Copilot — additional token consumption is covered by the credit mechanism rather than eroding margin (Bernstein "Scaling Intelligence", 2026-06-22).
- **Bear:** **AI-driven structural reset of a mature platform.** BofA reinstated **Underperform, PO $160** — FY27 rev growth ~11%, FY28 ~9.6%, only 9x EV/FCF, "mature platform facing AI-driven structural reset" (briefing 2026-05-19). UBS (Keirstead) **Neutral**: "simply won't re-rate off 6-8% revs growth" (2026-05-28). cRPO came at the low end of buyside; JPM (Schilsky) tagged the print "**CRM = meh** — nothing changes the AI debate" (2026-05-28). The seat-cannibalization fear is the same one that hammered app-SW peers — see HubSpot-style "AI-driven customer behavior change" read-throughs and the [tokenmaxxing](themes/tokenmaxxing.md) SaaS-apocalypse thread. Benioff routing ~$300M to Anthropic ([tokenmaxxing](themes/tokenmaxxing.md), briefing 2026-05-16) cuts both ways: validates agentic spend but flags rising COGS / dependence on frontier-model suppliers.
  - **The seat-base is already eroding, pre-AI (third-party):** JPM documents CRM's cRPO yoy cc decelerating from ~23-28% in 2018-19 to ~10-12% now, driven partly by *customers cutting headcount* — Washington (Q1'26, per JPM): "CRPO will continue to be materially impacted by the cumulative effect of the measured sales performance… and our slower exploration base"; the read is that seat-based renewals were already softening on customer headcount cuts before agents arrive, and agentic automation could accelerate it (JPM, Ogg, 2025-09-03). Bain's "AI cannibalizes SaaS" quadrant flags high-automation / high-AI-penetration workflows as battlegrounds where incumbents keep the edge *only if* they proactively replace SaaS activity with AI, else risk "disruption, obsolescence" (Bain Technology Report 2025). UBS's monetization map cuts against the agentic-ARR bull near-term: 2-3 years post-ChatGPT, direct AI revenue from CRM/NOW/Adobe *combined* is <$1bn vs OpenAI alone likely out-earning the entire app-software ecosystem — most AI monetization is still "below the apps layer" (UBS, 2025-09).
  - **Competitive threat — Sierra (third-party):** JPM flags Sierra (founded by ex-CRM co-CEO Bret Taylor; ~$4.5bn val, ~$20m ARR Oct-24) as a CX/contact-center agent that "could look to address budget from legacy CRM softwares," with voice ("Sierra Speaks") diverting IVR/contact-center spend; per JPM, CRM has already had to defend large accounts to keep them on Agentforce over Sierra (JPM, Ogg, 2025-09-03).
  - **Token-optimization read-through — mixed (third-party):** UBS names CRM (with ServiceNow and Workday) as a "larger and well-penetrated seat-based SaaS firm" that is NOT helped as enterprises cut headcount growth / optimize seats / trim app-software budget growth to fund rising AI token costs — and warns their seat-plus-usage pricing transition "may now be met with even greater resistance"; the offsetting positive is that model-neutral software firms (don't own 1P models) could gain by playing an independent "token optimizer" role like Palantir's Evolve (UBS "The Ramp in Token Optimization" / Keirstead, 2026-06-23). [tokenmaxxing](themes/tokenmaxxing.md).
  - **Apps-spend pressure intensifying (third-party):** UBS's team (Keirstead/McGinnis) reports a "stronger barbell" in IT budgets — enterprises funding AI/data/hyperscaler/cyber by tempering headcount growth, throttling IT services, and on apps "pushing back on budget increases, minimizing seat growth, minimizing module expansion, negotiating much tougher on pricing" and compressing contract durations; "becoming a tougher apps software spend environment… probably going to get a little worse before it gets a little bit better." Caveat for CRM's moat: Karpathy flagged that **Claude is "getting very good at absorbing workflow knowledge"** — a long-term chip at Salesforce's "20 years of understanding the sales rep" edge — though UBS still credits real incumbency/complexity moats (UBS "Karl software call", 2026-06-18). [tokenmaxxing](themes/tokenmaxxing.md). Salesforce's recent **down-market move (Intercom/"Fin"/Intercom acquisition)** flagged alongside ServiceNow pushing down-market as a potential opening for HubSpot (UBS, 2026-06-18).
  - **The "agentic layer on top" framing (Poio expert, third-party):** ex-Google Cloud / Poio CEO Matt Slotnick argues the growth market for incumbents like CRM is **"a layer above their existing system"** — the automation/agent layer — and that owning the data/customer relationships is "a huge advantage" but does NOT guarantee winning that layer ("the fact that you have a bunch of data… magically means you're going to win that AI layer… that is not true yet"). The "last mile" (driving the actual outcome) is where value accrues and where big SW companies have historically been weakest; frontier models stay "super valuable" for the hardest tasks even as cheaper models (e.g. Kimi 2.6) approximate Claude for known workloads (WFC agentic-software expert call, 2026-05-29). [tokenmaxxing](themes/tokenmaxxing.md). [../relat%C3%B3rios%20bons/2026_05_29_wfc_sw_agentic_29_may_2026.html](../relat%C3%B3rios%20bons/2026_05_29_wfc_sw_agentic_29_may_2026.html)
  - **Conference tone (third-party):** Jefferies (Brent Thill) — Salesforce off its print sounded "stable, steady… not super exciting"; the team flags the broader "software is not dead, these AI companies are not going to eat them" takeaway, but also a striking **magnitude of sales-org turnover in Silicon Valley** (Jefferies "Brent/Jeff AI" call, 2026-06-01). [../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html)
- **Where the sell-side stands (on-disk, attributed):** **MS (Weiss) OW $287** (2026-05-28); **Barclays (Lenschow) OW, PT cut $252→$236**, "solid but not thesis-changing" (2026-05-28); **UBS (Keirstead) Neutral** (2026-05-28); **R&Co Redburn Buy** (2026-05-28); **BofA Underperform $160** (2026-05-19); **JPM (Murphy)** suspended rating/PT for policy reasons into the print (2026-05-27). Net: bifurcated — growth-discount bears vs self-help/agentic bulls; the swing variable is H2 FY27 cRPO acceleration + Agentforce ARR slope.

## Catalysts / what to watch
- **Q2 FY27 print** (~early Sep 2026, by cadence — Q2 FY26 was 2025-09-03). Watch: H2 cRPO acceleration (the whole bull/bear hinge), Agentforce ARR slope past $1bn, token/work-unit growth, and whether non-seat/consumption mix is disclosed.
- **BofA SF Global Tech Conference 2026-06-02–04** — CRM on the roster (briefing 2026-05-28); watch for agentic-monetization framing.
- Tableau/Marketing/Commerce stabilization — the drag offsetting Agentforce.
- Informatica integration revenue contribution; further M&A.
- Pricing model evolution: proof that agentic consumption stacks on seats rather than replacing them — and whether outcome/usage pricing (the "charge per work done" shift Bain/JPM describe) expands or merely re-prices the seat base.

## Risks
- **Seat cannibalization / AI behavior change** — the central thesis risk; autonomous agents could compress the human-seat base CRM monetizes (the bear case; [tokenmaxxing](themes/tokenmaxxing.md)). Note the seat base was already decelerating on customer headcount cuts pre-AI (cRPO cc from ~23-28% in 2018-19 to ~10-12%; JPM, Ogg, 2025-09-03) — agentic automation is an accelerant of an existing trend, not a new one.
- Growth maturity — low-teens cc revenue, sub growth ~11%, limited re-rating room at ~9x EV/FCF (BofA, 2026-05-19; UBS, 2026-05-28).
- LLM-cost / supplier dependence — frontier models "a critical part of our infrastructure" (Benioff, Q4 FY26); ~$300M Anthropic spend = rising COGS and reliance on external model providers.
- Competition — intense from Microsoft Dynamics/Copilot, ServiceNow ([NOW](NOW.md)), and AI-native challengers; specifically AI-native CX entrants like **Sierra** (Bret Taylor) targeting contact-center/IVR budgets and open-source agent frameworks (LangChain, AutoGen) for cost-sensitive workloads, though JPM views open-source as complementary not displacing for mission-critical use (JPM, Ogg, 2025-09-03). "models will change over time."
- Integration/M&A execution (Informatica, prior Slack/Tableau) and dilution; restructuring drag on GAAP margin.
- FX exposure (EUR, GBP, JPY, others) and data-residency/regulatory obligations on Hyperforce (10-K FY26, 2026-03-02).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **UBS Tech** _(2026-06-16)_: CRM featured in the 'software pain-trade' / positioning note (with PLTR).
- **Barclays & BofA desks** _(2026-06-16)_: CRM acquired **Fin** (AI); **BofA Underperform PT $160** (mature-platform / AI-reset bear); Benioff cites a $300M Anthropic deal.
- **Guillermo Rauch (Vercel CEO), Stanford MS&E435 lecture** _(2026-06-29)_: Primary-source operator confirming enterprise vibe-coding of Salesforce replacements — Vercel rebuilt its entire internal CRM (all sales-rep tooling) with 2 engineers using Salesforce solely as a backend API; predicts broad off-the-shelf SaaS replacement at the UI/workflow layer. Bear data point for the SaaS disruption thesis. ([transcript](../relat%C3%B3rios%20bons/401_Stanford_MSE435_Economics_of_-_vercel_ceo.html))

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY27 · May 19 → Jul 16, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1 FY27) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Growth / cRPO** | Rev $11.13bn, +13% (+12% cc), above guide; cRPO $33.6bn (+13% cc), at the low end | JPM (Schilsky): "CRM = meh", cRPO at the low end of buyside · UBS (Keirstead): "won't re-rate off 6-8% rev" | **⚠ nuance** (cRPO disappoints) |
| **Agentforce / AI monetization** | Agentforce ARR >$1bn; AI & Data ARR $3.4bn; 28.6tn tokens (+152% q/q) | Benioff: ~$300M of Anthropic this year → validates spend but raises COGS/frontier-vendor dependence | **⚠ nuance** (frontier-model cost) |
| **Moat / competition** | A1E/A4x bookings +~60% y/y; FY30 target $63bn | WFC (Slotnick/Poio): the growth market is "the layer above" (agentic), owning the data doesn't guarantee winning · UBS: Karpathy warns Claude "absorbs workflow knowledge" · Vercel CEO (Jun 29): Vercel rebuilt all of Salesforce internally with 2 engineers via vibe coding, still using Salesforce as backend API — the UI/workflow layer is at risk | **✗ contests** (threat to the agentic layer) |
| **Demand / apps** | FY27 guide raised to ~$45.9-46.2bn | UBS: "stronger barbell" in IT budgets — enterprises minimize seats/modules and negotiate harder on price | **✗ contests** (tougher apps environment) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-16 | @theallinpod (briefing) · Benioff | margin | bear | Benioff (via @theallinpod): "~$300M of Anthropic this year at Salesforce" — validates agentic spend but signals rising COGS / dependence on frontier-model vendors. |
| 05-19 | BofA · reinstate | valuation | bear | BofA reinstated Underperform, PO $160 — FY27 revenue growth ~11%, FY28 ~9.6%, only 9x EV/FCF, "mature platform facing AI-driven structural reset". |
| 05-27 | JPM · Murphy | valuation | neutral | JPM (Murphy) suspended rating/PT for policy reasons going into the print. |
| 05-28 | JPM · Schilsky | guidance | bear | JPM (Schilsky) tagged the print as "CRM = meh" — nothing changes the AI debate; cRPO came in at the low end of buyside. |
| 05-28 | Morgan Stanley · Weiss | valuation | bull | MS (Weiss): Overweight, PT $287. |
| 05-28 | Barclays · Lenschow | valuation | mixed | Barclays (Lenschow): Overweight, PT cut from $252 to $236, "solid but not thesis-changing". |
| 05-28 | UBS · Keirstead | valuation | bear | UBS (Keirstead): Neutral — "simply won't re-rate off 6-8% revs growth". |
| 05-28 | Redburn Atlantic · R&Co | valuation | bull | R&Co Redburn: Buy — "Q1 clears the bar, H2 acceleration on track". |
| 05-29 | WFC · Matt Slotnick (Poio) expert call | competition | bear | Ex-Google Cloud / Poio CEO argues the growth market for incumbents like CRM is "a layer above their existing system" (the agentic layer); owning the data/relationships is an advantage but does not guarantee winning that layer. The "last mile" is where value accrues and where large SW vendors have historically been weak. |
| 06-01 | Jefferies · Brent Thill | valuation | mixed | Jefferies (Brent Thill): Salesforce post-print sounded "stable, steady… not super exciting"; broader takeaway that "software is not dead", but notable magnitude of turnover in Silicon Valley sales orgs. |
| 06-16 | UBS · Tech desk | valuation | mixed | UBS Tech (Outlook): CRM featured in the 'software pain-trade' / positioning note (alongside PLTR). |
| 06-16 | Barclays & BofA · desks | capital | mixed | Barclays & BofA desks (Outlook): CRM acquired Fin (AI); BofA Underperform PT $160 (mature-platform/AI-reset bear); Benioff cites $300M deal with Anthropic. |
| 06-18 | UBS · Keirstead/McGinnis | demand | bear | UBS reports a "stronger barbell" in IT budgets — enterprises pressuring apps: "minimizing seat growth, minimizing module expansion, negotiating much tougher on pricing"; the apps-spend environment is getting harder. Karpathy warned that Claude is "getting very good at absorbing workflow knowledge", a long-term threat to Salesforce's 20-year moat; down-market move (Intercom/Fin) cited. |
| 06-23 | UBS · Keirstead | demand | mixed | UBS names CRM (with NOW/WDAY) as a well-penetrated seat-based SaaS firm NOT helped as enterprises cut headcount/optimize seats/trim app-budget growth to offset AI token costs; seat-plus-usage pricing "may now be met with even greater resistance." Offset: model-neutral software could gain by playing an independent "token optimizer" role like Palantir's Evolve. |
| 07-16 | Morgan Stanley · Josh Baer (2Q26 CIO Survey) | competition | mixed | In MS's 2Q26 CIO survey (n=100), CRM retains meaningful AI relevance — MS's vendor-consolidation framework flags **Salesforce (with Snowflake) as keeping AI relevance in Customer Service**, and CRM's **incremental-GenAI-spend share ticked up to 8% in 2026 (from 7%)** with Agentforce a **top agentic-automation option (3%→5%)**. But the nuance is the bear's: CRM screens among the vendors with **decelerating forward-year growth expectations** (vs MSFT/NOW the only two accelerating), reinforcing the seat-based-SaaS-under-pressure read (UBS 06-23). Net mixed — some AI-relevance validation, but not enough to break the "won't re-rate off single-digit growth" bear. (MS · Josh Baer, 2026-07-16) |
| 06-29 | Guillermo Rauch (Vercel CEO) — Stanford MS&E435 lecture | competition | bear | Primary-source confirmation of the SaaS-disruption bear: "we kind of reinvented all of Salesforce, all of it... it took a team of two people to create a new version of Salesforce, which is kind of crazy to think about." Vercel built an internal CRM that replaces the Salesforce UI layer for all its sales reps, using Salesforce purely as a backend API (system of record) while a vibe-coded v0 application handles the presentation layer. Rauch predicts enterprises are "underestimating just how many off-the-shelf applications will be thrown away and replaced" — but the system-of-record layer (ACL, workflows, databases Salesforce set up) survives; the risk is concentrated in the UI/workflow layer, which Salesforce is now competing with via Agentforce. Companies that "expose themselves with the right agentic interfaces (MCP, CLIs, APIs)" will be protected; those that don't will be "thrown away." (Guillermo Rauch, Stanford MS&E435, 2026-06-29; transcript: [401_Stanford_MSE435_Economics_of_-_vercel_ceo.html](../relat%C3%B3rios%20bons/401_Stanford_MSE435_Economics_of_-_vercel_ceo.html)) |

**Quarter synthesis:** the print "cleared the bar but didn't change the AI debate" — despite Agentforce >$1bn of ARR, the flow shifted to *structural risk*: pressure on seats/modules (UBS "barbell"), the agentic-layer/Claude threat to the 20-year moat, and the dependence on ~$300M of Anthropic that validates the spend but raises COGS; bulls (MS PT $287) remain isolated against a bear chorus (BofA Underperform $160, UBS, JPM). The Jun 29 Vercel CEO primary-source quote adds an operator-level datapoint to the bear case: enterprises are already vibe-coding Salesforce replacements (2 engineers rebuilt all of Salesforce internally), with the system-of-record layer surviving but the UI/workflow layer at risk from agentically-built alternatives.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2 FY26 (2025-09-03) | Q3 FY26 (2025-12-03) | Q4 FY26 (2026-02-25) | Q1 FY27 (2026-05-27) |
|---|---|---|---|---|
| Revenue growth | $10.25bn, +10% y/y (+9% cc) | $10.26bn, +9% y/y (+8% cc) | Q4 $11.2bn, +12%; FY26 +10% | $11.13bn, +13% (+12% cc), above guide |
| cRPO | $29.4bn, +11% y/y | $29.4bn, +11%; RPO ~$60bn | $35.1bn, +16% (+13% cc) | $33.6bn, +14% (+13% cc), low end |
| Agentforce standalone ARR | 6,000+ paid deals (no ARR yet) | ~$540m, +330% y/y | ~$800m, +169%; 29k deals/15mo | surpassed $1bn |
| AI & Data / consumption | AI & Data line +120% y/y | AI+Data ARR ~$1.4bn; 3.2tn tokens | ARR $2.9bn (+200%); 2.4bn work-units | AI & Data ARR $3.4bn; 28.6tn tokens (+152% q/q) |
| Margin / capital return | non-GAAP op mgn 34.3% | 35.5%; $4bn+ buyback; FCF $2.2bn | FY26 returned >$14bn; $50bn auth | 34.8% (+250bps); $25bn ASR, ~10% fewer shares |
| Pricing model | — | flexible: AELA + seat SKUs + consumption | A1E/A4x premium SKUs scaling | A1E/A4x bookings +~60% y/y; hybrid mix |

_Source: CRM earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY26 (2026-03-02)](../CRM/CRM_10-K_2026-03-02_0001108524-26-000060.html) — business + risk factors · [10-Q Q1 FY27 (2026-05-28, period ended 2026-04-30)](../CRM/CRM_10-Q_2026-05-28_0001108524-26-000127.html).
- **Transcripts:** [Q1 FY27 (2026-05-27)](../CRM/transcripts/CRM_Q1-FY27-earnings_2026-05-27.md) · [Q4 FY26 (2026-02-25)](../CRM/transcripts/CRM_Q4-FY26-earnings_2026-02-25.md) · [Q3 FY26 (2025-12-03)](../CRM/transcripts/CRM_Q3-FY26-earnings_2025-12-03.md) · [Q2 FY26 (2025-09-03)](../CRM/transcripts/CRM_Q2-FY26-earnings_2025-09-03.md). _Read in full: Q1 FY27, Q4 FY26. Third-party paraphrase — see fidelity flag._
- **Briefings:** `E:\briefings\2026` — 2026-05-19-morning (BofA reinstate Underperform $160), 2026-05-21-morning (Barclays Q1 preview), 2026-05-27-morning (print setup, JPM suspends), 2026-05-28-morning (Q1 FY27 print recap + PT moves), 2026-05-16/-17/-18/-19-company-specific (Benioff $300M Anthropic).
- **Research reports (relatórios bons):**
  - [JPM First Principles — Agentic software (2025-09-03)](../relat%C3%B3rios%20bons/JPM_First_Principles___A_2025-09-03_5070498.html) — agentic-disruption matrix (entrenched multi-layer enterprise SW best insulated), seat-base/headcount decel, ~$2/conversation pricing, Sierra/Bret Taylor competitive threat.
  - [UBS OpenAI deep-dive](../relat%C3%B3rios%20bons/oAI_UBS.html) — enterprise-IT checks find no seat displacement / no SaaS app displacement (Street "over-indexing too cautious"); AI monetization still "below the apps layer", CRM/NOW/Adobe combined direct AI rev <$1bn.
  - [Bain Technology Report 2025](../relat%C3%B3rios%20bons/bain_report_technology_report_2025.html) — Salesforce one of few giants that can be both neutral agent platform and unique-data supplier; "AI cannibalizes SaaS" battleground quadrant; outcome/usage pricing shift.
  - [Bernstein — Scaling Intelligence: The Generative AI Handbook (2026-06-22)](../relat%C3%B3rios%20bons/Bernstein_on_Gen_AI_Software.html) — incumbents-survive framework; AI a "small headwind + mostly offsetting small tailwind (Agentforce)" for CRM; credit-based GenAI pricing as margin-defensive; SAP/Oracle "best positioned."
  - [UBS (Keirstead) — software/AI team call (2026-06-18)](../relat%C3%B3rios%20bons/2026_06_18_karl_ubs_18_jun_26.html) — tougher apps-spend environment, seat/module/pricing pushback; Claude absorbing workflow knowledge; CRM/NOW down-market moves.
  - [UBS "The Ramp in Token Optimization" (2026-06-23)](../relat%C3%B3rios%20bons/ued46392.html) — seat-based SaaS (CRM/NOW/WDAY) not helped by token-cost offsets, seat-plus-usage pricing meets greater resistance; offset = model-neutral "token optimizer" role (Palantir Evolve).
  - [WFC — agentic-software expert call (Matt Slotnick/Poio, 2026-05-29)](../relat%C3%B3rios%20bons/2026_05_29_wfc_sw_agentic_29_may_2026.html) — "agentic layer above the system" is the growth market; data/relationships an advantage not a guarantee; last-mile = where value accrues.
  - [Stanford MS&E435 — Guillermo Rauch (Vercel CEO): "we reinvented all of Salesforce with 2 engineers" via vibe coding; UI/workflow layer at risk, system-of-record layer survives (2026-06-29)](../relat%C3%B3rios%20bons/401_Stanford_MSE435_Economics_of_-_vercel_ceo.html)
  - [Jefferies (Brent Thill) — AI software/infra call (2026-06-01)](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html) — Salesforce "stable, steady, not super exciting"; SV sales-org turnover.
- **Theme:** [tokenmaxxing](themes/tokenmaxxing.md) — AI-monetization / SaaS-apocalypse debate.
- **Equity calls:** 0 CRM-specific attributed (Internet/Overall conference wraps on disk did not single out CRM). **Outlook:** unavailable this run.
