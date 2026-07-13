<!-- Per-company wiki page. Financials/consensus block auto-injected by build_wiki_html.py — do NOT hand-write it. -->

# RDDT — Reddit, Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\RDDT` (10-K FY25 + 10-Q Q1-26 + transcripts) · `E:\briefings\2026` roll-up. Master index: [00_INDEX.md](00_INDEX.md). IPO Mar-2024 — short filing history (3 10-Ks back not available; coverage from FY24 onward)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $3.2bn | $4.2bn |
| Gross profit | $2.9bn | $3.9bn |
| Gross margin | 91.3% | 91.6% |
| EBITDA | $1.4bn | $2.0bn |
| EPS | $5.85 | $7.65 |
| Capex | $11m | $16m |
| OCF (≈EBITDA) | $1.4bn | $2.0bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Reddit is a community-driven social platform (~100K+ active subreddits) that monetizes the largest open corpus of human conversation on the internet through two engines: (1) **advertising** (~94% of revenue) and (2) **AI/content data-licensing** ("Other revenue," ~6%) to AI labs training LLMs. FY25 revenue $2,202.5M, +69% YoY; advertising $2,062.5M, licensing/other $140.0M; net income $530M vs a $484M net loss in FY24 — the inflection-to-profitability year (10-K, 2026-02-06). Q4-25 DAUq 121.4M global (+19% YoY), 68.9M international (+28%) (10-K). The platform increasingly runs its own on-site search (Reddit Answers) on top of its corpus, layering a third potential monetization vector. Structural tension: Reddit depends on Google organic referral traffic for user acquisition even as Google's AI Overviews / AI Mode answer queries in-place — the central bear overhang.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Advertising (~94% of rev) · 2) AI/content data-licensing (~6%, "Other revenue") · 3) On-site search / Reddit Answers (emerging commerce) |
| **Main buyer(s)** | Advertisers (large / mid-market / SMB) for ads; AI labs (Google, OpenAI) for data-licensing — US ~79% of revenue |
| **Key suppliers** | Cloud/compute on AWS + Google Cloud; user-generated content (free human-conversation corpus); Google for organic traffic acquisition |

## Position in the value chain
Reddit is a two-sided internet platform sitting between content supply (its users + cloud infra on AWS/GCP) and two distinct demand pools: advertisers buying attention and AI labs buying its data corpus. The **dual engine** (ads + data-licensing) is the differentiator vs pure ad-net peers; the **Google-traffic dependency** is the supplier-side risk, since the same Google that licenses Reddit data also gates a large share of its inbound user traffic.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Reddit position in the value chain">
  <style>
    .box{fill:#fff;stroke:#333;stroke-width:1.5;rx:6;}
    .core{fill:#ffe8e0;stroke:#c0392b;stroke-width:2;}
    .lbl{font-family:Arial,Helvetica,sans-serif;font-size:11px;fill:#222;}
    .hdr{font-family:Arial,Helvetica,sans-serif;font-size:12px;font-weight:bold;fill:#111;}
    .risk{font-family:Arial,Helvetica,sans-serif;font-size:10px;fill:#c0392b;font-style:italic;}
    .arr{stroke:#555;stroke-width:1.5;fill:none;marker-end:url(#a);}
  </style>
  <defs>
    <marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Suppliers -->
  <rect class="box" x="10" y="55" width="170" height="100"/>
  <text class="hdr" x="20" y="75">Suppliers</text>
  <text class="lbl" x="20" y="95">Cloud: AWS + Google Cloud</text>
  <text class="lbl" x="20" y="112">Content = users (free,</text>
  <text class="lbl" x="20" y="126">human conversation corpus)</text>
  <text class="lbl" x="20" y="146">Traffic acquisition via Google</text>
  <!-- Reddit core -->
  <rect class="core" x="250" y="45" width="200" height="120"/>
  <text class="hdr" x="262" y="68">Reddit (RDDT)</text>
  <text class="lbl" x="262" y="88">Social platform</text>
  <text class="lbl" x="262" y="108">1) Advertising (~94%)</text>
  <text class="lbl" x="262" y="125">2) AI data-licensing (~6%)</text>
  <text class="lbl" x="262" y="142">3) Search / Reddit Answers</text>
  <text class="lbl" x="262" y="158" font-weight="bold">Dual engine: ads + data</text>
  <!-- Customers -->
  <rect class="box" x="520" y="45" width="190" height="120"/>
  <text class="hdr" x="530" y="68">Customers</text>
  <text class="lbl" x="530" y="90">Advertisers (large /</text>
  <text class="lbl" x="530" y="104">mid-market / SMB)</text>
  <text class="lbl" x="530" y="128">AI labs licensing data:</text>
  <text class="lbl" x="530" y="142">Google, OpenAI</text>
  <!-- Arrows -->
  <line class="arr" x1="180" y1="105" x2="248" y2="105"/>
  <line class="arr" x1="450" y1="105" x2="518" y2="105"/>
  <!-- Google dependency risk loop -->
  <path class="arr" d="M520,150 C460,200 200,200 110,158"/>
  <text class="risk" x="225" y="212">Risk: Google AI Overviews / AI Mode displace organic referral traffic in-place</text>
</svg>

## Current state (latest quarter)
Q1 FY26 (call 2026-04-30): revenue $663.4M, +69% YoY — 7th straight quarter >60% growth (transcript; 10-Q 2026-05-01). Advertising $624.7M (+74%); content licensing/other $38.7M (+15%). ARPU $5.23 (+44%). Net income $204.0M vs $26.2M PY. Adj. EBITDA margin 40% (+~1,100bps); FCF margin 47%, record FCF >$300M; gross margin 91.5%. Q1-26 DAUq 126.8M; **total DAUq YoY growth has decelerated to ~17%** from 51% a year earlier (10-Q) — the user-growth-deceleration debate is live. US revenue $525.6M, RoW $137.9M (10-Q). Mgmt's stated North Star: 100M US DAUq / 1B global DAUq (JPM access note, 2026-06-10). **Q2-26 guide:** revenue $715–725M (+43–45%); adj. EBITDA $285–295M (~40% margin) — decel guide reflects lapping a strong Q2-25.

## Debate / thesis
- **AI-software read-through — "static Q&A/content DBs" flagged as a short (Vercel CEO Guillermo Rauch, Stanford MS&E435, 2026-06-29):** in his long/short framing Rauch lists "static Q&A/content databases like Stack-Overflow-style models" among the categories most exposed as agents make answers cheap to generate. _Inferential for RDDT:_ Rauch named Stack Overflow, not Reddit, and RDDT's moat is live human community + a paid data-licensing model rather than a static reference DB — but it sharpens the standing bear case (LLM/AI-Overviews answer-substitution cannibalizing referral traffic, and the durability of content-licensing demand). See [tokenmaxxing theme](themes/tokenmaxxing.md).
- **Bull:** Unique, defensible human-data moat — "Reddit is the number one cited source in AI answers" (Huffman, Q4-25 call); dual monetization (ads + licensing). **Ad spend re-accelerating in expert checks** — UBS (Ben Legg) models RDDT ad growth Q2 73% / Q3 55% / Q4 51% (all nudged up from April war lows), calling Reddit "an amazing game of catch-up" cherry-picking the best features from Google/Meta (UBS Ben Legg, 2026-06-17). At the Jefferies conf RDDT outlined a durable-growth case: long runway to add advertisers + raise budgets at existing (the biggest recent growth driver), reiterating the goal to **double US DAU to 100M+** by converting 200M weekly users to daily (Jefferies/Brent Thill conf, 2026-06-01). BofA spec-sales pitched RDDT as one of the few remaining non-AI-adjacent growth stocks — **~50% growth at ~15x, down 40–50%, CPMs ~half of Pinterest's** at a less-mature platform, with data-deal-renewal headlines as binary upside (BofA/Fenske, 2026-04-16); BofA (Wigg) adds RDDT remains a top-1-or-2 cited AI source (with Wikipedia), so OpenAI/Google renewals + a potential Anthropic legal settlement can add high-margin dollars (BofA/Wigg, 2026-05-06). [Ben Legg](../relat%C3%B3rios%20bons/2026_06_17_ben_legg_ubs_17_jun_26.html) · [Jefferies conf](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html) · [Fenske](../relat%C3%B3rios%20bons/2026_04_16_fenske_16_apr_26.html) · [Wigg](../relat%C3%B3rios%20bons/2026_05_06_wigg_6_may_26.html) Ad business still early — ARPU +44% with ad-load headroom; active advertisers +75% YoY; SHOP integration unlocking SMB budgets (Bernstein/Seidman, briefing 2026-05-28). 40% adj. EBITDA margin / 47% FCF margin = high-quality compounding. JPM hosting mgmt access = OW posture (Schilsky/Anmuth, 2026-06-10/11). BofA advertiser survey flagged "Reddit strong 2Q trends" (2026-05-27). RDDT reportedly **gaining AI-search traffic** (JPM · Mark Schilsky, 2026-07-06) — a partial offset to the Google-organic-traffic-erosion bear if AI-search referral picks up what conventional organic search cedes. Buy-side roundtable view: Tony Kim (BlackRock) tagged RDDT a top pick on the selloff — "unduly punished… a unique position as the nonsocial social network… a bastion of human-curated content… going to do well as a result of AI search" (Barron's Tech Roundtable, 2025-03-28; flagged at $120.20).
- **Bear:** Google organic-traffic dependency. Huffman conceded "Traffic from Google… overall it was a headwind in Q2" (Q2-25 call); AI Overviews/AI Mode "affects everybody in the ecosystem." On 2026-05-06 RDDT -3% as Google AI Search Mode packaged Reddit content inside AI overviews; on 2026-05-21 RDDT -5% / JPM's #1 inbound on delayed reaction to Google I/O agentic-search risk ("organic search referral traffic to RDDT shrinks as AI Mode answers in-place"). DAUq growth decelerating (~17% vs 51% PY). Licensing revenue ($140M FY25) still modest and lumpy — the "AI data oil" narrative is not yet a needle-mover. CPG advertiser input-cost pressure flagged (JPM, 2026-06-10). **"Faustian bargain" framing** (Eric Seufert, Stratechery, 2025-04-24): the Google data-licensing deal is "a deal with the devil" — Reddit is structurally dependent on text-based search traffic it cannot diversify away from (legacy user base "won't allow" a TikTok-style format shift), while the same AI Overviews that source Reddit content also displace the click-through. The bull twist in the same piece: if Google breaks up its network business and abandons the open web, it has the incentive to "preference and prioritize" the publishers it holds licensing deals with — Reddit chief among them — feeding traffic back to monetize AI-overview ads.
- **The whole debate is DAUs (JPM internet preview, 2026-04-15):** JPM framed RDDT as "pretty split" — revenue beats are not the debate (everyone expects ~$650M+ Q1, nice beats), it's **US DAU** that sits "on the razor's edge" (buy-side bogey ~street + a few hundred K US adds); a beat and the stock works, a miss and it's down. Data-deal renewals with Google + OpenAI are a mid-to-back-half event to watch (JPM/Anmuth, 2026-04-15). [Source](../relat%C3%B3rios%20bons/2026_04_15_jpm_internet_preview_15_apr_26.html)
- **Where the Street stands:** JPM OW-leaning (active corporate access; Anmuth/Schilsky). Bernstein constructive on ROAS/SHOP (Seidman). BofA positive on 2Q ad trends. **Rothschild & Co Redburn is the bear — SELL** (Riser note, 2026-07-07): even the positive Gen-AI traffic data (Similarweb: Reddit Gen-AI referrals +2-3x May vs March, now above Wikipedia) is dismissed as immaterial — ~15m monthly Gen-AI visits vs ~500m WAU in 1Q26 means AI is "not yet going to matter for key DAU metrics"; R&Co argues AI's ability to resolve queries without click-through means it is "unlikely to ever be a meaningful traffic driver," and sees little incentive for LLM providers to sign data deals above the current ~$60m given stronger customer negotiating positions vs early-2024. Trades 31x FY27 Adj. EBITDA less SBC. The recent share move is read as the "AI winner" narrative returning (RDDT hit **3-month relative highs**, 2026-07-07) — R&Co's point is the premium multiple is riding a narrative the traffic data does not yet support. Redburn earlier flagged 3m relative lows (technical, 2026-05-26). GS desk: RDDT among "most-debated" internet singles, +25% on the week late-May, then "most out-of-favor" basket on traffic fears (2026-05-18/30). Tiger Global held $394M RDDT (13F, 2026-05-16).

## Catalysts / what to watch
- **Q2-26 print** (~late Jul/early Aug 2026) — guide $715–725M; lapping tough Q2-25 comp, so the decel optics matter.
- **MS 3Q digital ad-check calls** — Jun-30 (McLean) and Jul-13 (Legg), both covering META/GOOGL/RDDT/PINS (briefing 2026-06-13) — read-through on 3Q ad spend.
- **Google product cadence** — any further AI Mode / AI Overview changes to organic referral; the recurring share-price trigger.
- **Data-licensing renewals/new deals** — Google + OpenAI; "shifting to product partnership" framing (Q4-25). Watch for incremental labs (Anthropic, Meta) and any disclosed deal values.
- **Reddit v. Anthropic litigation** — Reddit's suit alleges Anthropic illegally scraped Reddit user data to train its models without consent, accessing Reddit content 100,000+ times in violation of TOS after refusing a licensing agreement; Reddit seeks restitution, punitive damages, and an injunction (JPM, citing Anmuth, 2025-09-18). Read-through: it both validates the licensing-revenue moat (data has paid-for value) and signals enforcement upside / a possible settlement template — watch for resolution.
- **US DAUq trajectory toward 100M** — the user-growth re-acceleration proof point.
- Potential S&P 500 inclusion candidate (Barron's flagged, 2026-06-09).

## Risks
- **Google traffic dependency** — relies on Google organic search to acquire users; algorithm/AI-Overview changes can cut referral traffic materially (10-K risk factors; Q2-25 call). Seufert frames this as inescapable: the legacy user base blocks a format pivot, so Reddit stays "dependent" on text-based search siphoned into its text content (Stratechery, 2025-04-24).
- **AI substitution of the platform itself** — Redditors may use LLMs (Google, OpenAI, Anthropic, Meta) to retrieve info instead of visiting Reddit (10-K).
- **DAUq volatility/deceleration** — absolute DAUq has declined in past periods; growth rate expected to slow as base scales; sensitive to community responses and content moderation (10-K).
- **Monetization concentration** — ~94% advertising; competes with Google/Meta/Snap/TikTok/Pinterest/X for ad budgets with less mature tooling (10-K). Licensing revenue lumpy/small.
- **Content-licensing misuse / IP** — limited control over partner reuse of licensed content; uncontrolled scraping by AI tools erodes licensing value (10-K). The Anthropic suit (100K+ unlicensed accesses alleged) is the live test case for whether Reddit can enforce its data property (JPM/Anmuth, 2025-09-18).
- **Cloud concentration** — sole reliance on AWS + GCP for infra (10-K) — note GCP supplier overlaps with Google the licensee/traffic gatekeeper.
- **Dual-class control** — founder/insider super-voting Class B; limited public-float governance influence (10-K).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **Rothschild & Co Redburn (US Riser)** _(2026-07-07)_: **SELL** — Similarweb Gen-AI traffic +2-3x (now > Wikipedia) but immaterial to DAU (~15m vs ~500m WAU); "AI winner" narrative driving the re-rating unsupported by the data; ~$60m data-deal pricing capped; 31x FY27 Adj. EBITDA-SBC. First explicit bear broker rating in the inbox.
- **MS TMT 7.07** _(2026-07-07)_: Huffman moat framing ("human, messy, pseudonymous conversation"; licensing a "bonus"); AI moderation caught 25K spammy posts/day in Q1 (-20% exposure).
- **BofA online-advertising sector call (Ben Legg)** _(2026-06-10)_: 'Reddit automated ad tools' a key topic, alongside Google AI-search read-through.
- **Stratechery (Eric Seufert)** _(2026-05-28)_ + Jefferies ad-expert checks: ad-monetization ramp vs Google AI-Overviews referral-traffic risk — the central debate.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY26 · Apr 30 → Jul 07, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1'26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Users / DAUq** | DAUq 126.8M, but growth decelerated to ~17% (from 51% YoY); North Star 100M US / 1B global | JPM: US DAU "on the razor's edge" is the whole debate · Jefferies: double US DAU to 100M+ by converting 200M weekly to daily | **⚠ nuance** (decel is the gap) |
| **Revenue / ads** | Rev $663M +69% (7th qtr >60%); ads $624.7M +74% | UBS/Legg models ads Q2 73%/Q3 55%/Q4 51% (revised up) · BofA survey "strong 2Q trends" · Bernstein: ad-load headroom, advertisers +75% | **✓ confirms** (ramp re-accelerates) |
| **Google / search traffic** | (no comment on the Q1 call; risk acknowledged in Q2-25) | JPM #1 inbound: AI Mode/Google I/O shrinks organic traffic (-5% on 05-21) · BofA/Wigg: AI Search Mode packages content (-3% on 05-06) | **✗ contests** (overhang live) |
| **Data-licensing** | Other rev $39M +15%; data "like oil"; shift to "product partnership" | JPM: Google+OpenAI renewals are a mid-to-back-half event · BofA/Wigg: top-1/2 cited source in AI, Anthropic settlement = upside · R&Co (07-07, Sell): little incentive for LLMs to sign deals above current ~$60m given stronger customer negotiating positions | **⚠ nuance** (lumpy, small; R&Co doubts pricing power) |
| **Valuation / rating** | — | BofA/Fenske: ~50% growth at ~15x, CPMs ~half of Pinterest, down 40-50% · Redburn: 3m relative lows (05-26) · Tiger $394M (13F) · **R&Co (07-07): SELL, 31x FY27 Adj. EBITDA-SBC** — Gen-AI traffic (+2-3x, > Wikipedia) still immaterial to DAU (~15m vs ~500m WAU); premium multiple rides an "AI winner" narrative unsupported by traffic data; stock at 3m relative HIGHS | **✗ contests** (first bear broker rating; the narrative-vs-fundamentals gap) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 04-15 | JPM · Anmuth | guidance | mixed | JPM (Internet 1Q preview): RDDT "pretty split" — revenue beats are not the debate (everyone expects ~$650M+ in Q1); what matters is US DAU, which is "on the razor's edge". Renewals of the data deals with Google + OpenAI are a mid-to-back-half event to watch. |
| 04-16 | BofA · Fenske (spec-sales) | valuation | bull | BofA spec-sales pitched RDDT as one of the few non-AI-adjacent growth stocks left — ~50% growth at ~15x, down 40-50%, CPMs ~half of Pinterest's on a less mature platform, with data-deal renewals as binary upside. |
| 05-06 | BofA · Wigg | demand | mixed | BofA (Wigg): RDDT remains a top-1-or-2 cited source in AI (with Wikipedia), so OpenAI/Google renewals + a potential legal settlement with Anthropic could add high-margin dollars. The same day, RDDT -3% as Google AI Search Mode packaged Reddit content inside AI overviews. |
| 05-16 | Tiger Global (13F) | valuation | neutral | Tiger Global held $394M of RDDT (13F). |
| 05-21 | JPM (desk) | demand | bear | RDDT -5% / JPM's #1 inbound on a delayed reaction to Google I/O agentic-search risk ("organic search referral traffic to RDDT shrinks as AI Mode answers in-place"). |
| 05-26 | Redburn Atlantic | valuation | neutral | Redburn flagged relative 3-month lows (technical). |
| 05-27 | BofA (advertiser survey) | demand | bull | BofA advertiser survey signaled "Reddit strong 2Q trends". |
| 05-28 | Bernstein · Seidman | demand | bull | Bernstein (Seidman): the ads business is still early — ARPU +44% with ad-load headroom; active advertisers +75% y/y; SHOP integration unlocking SMB budgets. |
| 06-01 | Jefferies · Brent Thill | demand | bull | At the Jefferies conference, RDDT laid out a durable growth case: a long runway to add advertisers + lift existing advertisers' budgets (the biggest recent driver), reiterating the goal to double US DAU to 100M+ by converting 200M weekly users to daily. |
| 06-10 | JPM · Schilsky/Anmuth | valuation | mixed | JPM hosting management access (OW stance); management's North Star: 100M US DAUq / 1B global DAUq. CPG advertisers' input-cost pressure also flagged. |
| 06-10 | BofA · Ben Legg | demand | mixed | BofA online-advertising sector call (Outlook): 'Reddit automated ad tools' a key theme, alongside Google AI-search read-through. |
| 06-17 | UBS · Ben Legg | demand | bull | UBS (Ben Legg) models RDDT ad growth Q2 73% / Q3 55% / Q4 51% (all nudged up vs April lows), calling Reddit "an amazing game of catch-up" as it cherry-picks the best features from Google/Meta. |
| 07-07 | Rothschild & Co Redburn (US Riser) | valuation | bear | **Initiates/reiterates SELL.** Similarweb data (public 07-06) shows Reddit Gen-AI referral traffic **+2-3x May vs March, now above Wikipedia** — but off a ~5m/mo base, so ~15m monthly visits vs ~500m WAU in 1Q26 makes clear **Gen-AI is "not yet going to matter for key DAU metrics."** R&Co: AI resolving queries without click-through means it is "unlikely to ever be a meaningful traffic driver"; little incentive for LLMs to sign data deals above the current ~$60m (stronger customer negotiating positions vs early-2024). The 1-month share move reflects the "AI winner" narrative returning; RDDT at **3m relative highs**. Trades **31x FY27 Adj. EBITDA less SBC**. (R&Co Redburn "US Riser", 2026-07-07) |
| 07-07 | Morgan Stanley (TMT 7.07) | demand | mixed | RDDT CEO Steve Huffman (MixedSignals pod) framed Reddit's core moat as **"human, messy, pseudonymous conversation" — increasingly valuable as the rest of the internet becomes AI-generated/influencer-driven/algorithmically flattened**; AI/data licensing is "meaningful but not the core business" (data/intelligence a "bonus"). Separately, RDDT says AI-powered moderation caught **25K spammy posts/comments per day in Q1, cutting user exposure ~20%** (Bloomberg). (MS TMT 7.07, 2026-07-07) |

**Quarter synthesis:** the debate has shifted from "do revenues beat?" (consensus that they do — ads re-accelerating in UBS/Bernstein expert checks) to the **US DAU × Google dependency** axis: the user count sits "on the razor's edge" while every AI Mode/AI Overviews move becomes a selloff trigger, leaving the positive ad signal hostage to the organic-traffic overhang. **Update (07-07):** the tape has flipped from 3m relative lows (late-May) to **3m relative highs** as the "AI winner" narrative returns — but Rothschild & Co (Redburn) put the first explicit broker **SELL** on the name, arguing the very Gen-AI traffic data driving the re-rating (+2-3x, now > Wikipedia) is still immaterial to DAU (~15m vs ~500m WAU) and that licensing pricing power is capped (~$60m deals). Bull (JPM: RDDT gaining AI-search traffic) vs bear (R&Co: narrative outruns the data) is now the sharpest axis into the Q2 print.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2'25 (2025-07-31) | Q3'25 (2025-10-30) | Q4'25 (2026-02-05) | Q1'26 (2026-04-30) |
|---|---|---|---|---|
| Revenue growth | Total rev ~$500M, +78% YoY | $585M, +68%; ads +74% | $726M, +70%; ads +75% | $663M, +69%; 7th qtr >60% |
| ARPU / monetization | ARPU $4.53, +47% YoY | ARPU $5.40, +41% (impressions) | ARPU $5.98, +42% | ARPU $5.23, +44% |
| Users / engagement | DAUq 110.4M, +21% YoY | DAUq 116M, ~+20% | DAUq 121.4M, +19% | DAUq 126.8M, ~+17% (decel) |
| Profitability / margin | Record profit quarter | Adj. EBITDA 40%; net inc $163M | FY25 adj. EBITDA ~38%; GM 91.2% | Adj. EBITDA 40%; FCF 47%, >$300M |
| AI data-licensing | Other rev $35M, +24% YoY | Partnerships "healthy, collaborative" | $36M; shift to "product partnership" | $39M, +15%; data "like oil" |
| Reddit Answers / search | — | Integrated into core search | Search WAUq 60M→80M; queries ~15M | Adding product catalog (commerce) |

_Source: RDDT earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [FY25 10-K (2026-02-06)](../RDDT/RDDT_10-K_2026-02-06_0001713445-26-000022.html); [Q1-26 10-Q (2026-05-01)](../RDDT/RDDT_10-Q_2026-05-01_0001713445-26-000069.html).
- **Transcripts:** [Q1-26 (2026-04-30)](../RDDT/transcripts/RDDT_Q1-2026-earnings_2026-04-30.md); [Q4-25 (2026-02-05)](../RDDT/transcripts/RDDT_Q4-2025-earnings_2026-02-05.md); [Q3-25 (2025-10-30)](../RDDT/transcripts/RDDT_Q3-2025-earnings_2025-10-30.md); [Q2-25 (2025-07-31)](../RDDT/transcripts/RDDT_Q2-2025-earnings_2025-07-31.md).
- **Research reports (relatórios bons):**
  - [JPM — Anthropic: Buckle Up (2025-09-18)](../relat%C3%B3rios%20bons/JPM_Anthropic_Buckle_Up__2025-09-18_5064281.html)
  - [Stratechery (Eric Seufert) — open web / ADS](../relat%C3%B3rios%20bons/Stratecherry_-_Eric_ADS.html)
  - [Barron's Tech Roundtable — 4 Experts, 22 Favorite Stocks](../relat%C3%B3rios%20bons/Barrons_Tech_Roundtable__Our_4_Experts_on_the_Next_Phase_of_AIand_22_Favorite_Stocks_-_Barrons.html)
  - [JPM — Internet 1Q preview (Anmuth, 2026-04-15)](../relat%C3%B3rios%20bons/2026_04_15_jpm_internet_preview_15_apr_26.html) — DAU debate; deal renewals.
  - [BofA (Fenske) spec-sales — RDDT long pitch (2026-04-16)](../relat%C3%B3rios%20bons/2026_04_16_fenske_16_apr_26.html) · [BofA (Wigg) — AI-source moat (2026-05-06)](../relat%C3%B3rios%20bons/2026_05_06_wigg_6_may_26.html)
  - [Jefferies software/internet conf (Brent Thill, 2026-06-01)](../relat%C3%B3rios%20bons/2026_06_01_brent_jeff_ai_1_jun_26.html)
  - [UBS (Ben Legg) — digital-ad expert: RDDT ad growth (2026-06-17)](../relat%C3%B3rios%20bons/2026_06_17_ben_legg_ubs_17_jun_26.html)
- **Briefings:** `E:\briefings\2026` roll-up — RDDT-specific desk notes: 2026-05-06 (Google AI Mode), 2026-05-21 (Google I/O -5%), 2026-05-26 (Redburn rel lows), 2026-05-27 (BofA ad survey), 2026-05-28 (Bernstein ROAS/SHOP), 2026-06-10/11 (JPM corp access), 2026-06-12/13 (MS ad checks), 2026-05-16 (Tiger 13F $394M). No dedicated `by-ticker/RDDT.md` roll-up exists yet.
- **Outlook:** attempted this run via `outlook.py` — returned no output (no usable Outlook/COM session in environment); sell-side stance above is sourced from the saved briefings, not a live inbox pull.
