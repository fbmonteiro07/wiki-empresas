<!-- Per-company wiki page. Synthesis of co-located disk sources with attribution. Buy-side voice. -->

# NET — Cloudflare, Inc.

_Wiki · generated 2026-06-25 · sources: `E:\Wiki Felipe empresas\CDNs\_imported_from_E_root\` (NET filings + transcripts + decks). Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $2.8bn | $3.6bn |
| Gross profit | $2.1bn | $2.6bn |
| Gross margin | 73.6% | 73.3% |
| EBITDA | $647m | $769m |
| EPS | $1.18 | $1.59 |
| Capex | $425m | $503m |
| OCF (≈EBITDA) | $647m | $769m |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Cloudflare is the "connectivity cloud" — a single global network (present in 120+ countries / 350+ cities) that sits in front of a large share of Internet traffic and sells application performance/security, network security, and a developer/compute platform on top of it. Management frames the business as four "Acts": **Act 1** = application services + the legacy CDN/security/performance layer (the largest revenue base); **Act 2** = Zero Trust / SASE (Access, Gateway, DLP, CASB, email security, browser isolation) displacing legacy hardware (Palo Alto, Zscaler-type incumbents); **Act 3** = the **Workers developer platform** (Workers, Workers AI, Durable Objects, Dynamic Workers, AI Gateway) — edge compute/inference; **Act 4** = the emerging AI-content layer (AI Crawl Control / "pay per crawl") to control and eventually monetize AI bot traffic (NET Q4 2025 call, 2026-02-10). FY2025 revenue $2,167.9M, +29.8% YoY (NET Q4 2025 PR, 2026-02-10). The core debate is whether Cloudflare is the structural winner of the "agentic Internet" re-platforming — owning both the traffic agents pass through (Act 1) and the platform they run on (Workers/Act 3) — at a premium multiple, against gross-margin dilution from the fast-growing-but-lower-margin developer platform.

## Current state (latest quarter — Q1 FY26, call 2026-05-07)
Strong beat-and-build, paired with a surprise ~20% workforce reduction.
- **Revenue $639.8M, +34% YoY** (NET Q1 2026 call, 2026-05-07). Geographic mix: US 49% (+34%), EMEA 28% (+31%), APAC 15% (+34%).
- **Large customers:** 4,416 customers paying >$100k/yr, **+25% YoY**; these accounted for **72% of revenue** (up from 69% a year ago) and grew 38% YoY. Customers >$5M grew **50% YoY** with a record number of additions — NET added as many $5M+ customers in Q1 as in all of last year. Deals over $1M up **73% YoY** (fastest since 2024) (NET Q1 2026 call, 2026-05-07).
- **Dollar-based net retention 118%**, down 2pts QoQ, up 7pts YoY (NET Q1 2026 call, 2026-05-07).
- **Margins / cash:** non-GAAP gross margin **72.8%** (-210bps QoQ, -130bps YoY) — pressured by paid-vs-free traffic mix shift (network cost moving from S&M into COGS, "a wash" at the P&L level) and the lower-margin Workers/developer products; operating income $73.1M (op margin 11.4%); GAAP net income $94M / $0.25 diluted; **FCF $84.1M (13% of revenue)**; $4.2B cash & securities (NET Q1 2026 call, 2026-05-07).
- **RPO $2.543B, +36% YoY** (+2% QoQ); current RPO 64% of total, +34% YoY (NET Q1 2026 call, 2026-05-07).
- **Developer platform inflection:** developers reached **>5.5M, +1M in a single quarter** vs +1.5M in all of 2025; >3/4 of Workers growth from new customers (NET Q1 2026 call, 2026-05-07).
- **AI-at-the-edge angle:** management says it invests *behind* demand, not ahead — runs internal AI coding workloads on its own GPU fleet via Workers AI, getting GPU utilization "approaching" CPU's 70–80% vs hyperscalers' "single digits"; AI Gateway routes simple tasks to on-network models at near-zero marginal cost. Cloudflare's own AI usage +600% in three months; 97% of R&D uses AI coding tools, 100% of production code reviewed by AI agents. One large AI studio went from ~zero to >1M Dynamic Workers in 15 days (NET Q1 2026 call, 2026-05-07).
- **The restructuring:** announced a **~20% / >1,100-person headcount reduction** to move to an "agentic AI-first operating model"; restructuring charges $140–150M for FY26 (~$40M non-cash, mostly Q2). Notably **quota-carrying sales (AE) capacity was largely untouched** — cuts hit support ratios; management still expects net sales capacity growth to accelerate in 2026 and "more employees in 2027 than at any point in 2026." FY26 FCF expectation unchanged (NET Q1 2026 call, 2026-05-07).
- **Guidance (Q1 print):** Q2 FY26 revenue $664–665M (+30% YoY), op income $90–91M, EPS $0.27; FY26 revenue **$2.805–2.813B (+30% YoY)**, op income $418–421M, EPS $1.19–1.20 — a modest raise vs the FY26 frame given at Q4 ($2.785–2.795B, EPS $1.11–1.12) (NET Q1 2026 call, 2026-05-07; NET Q4 2025 PR, 2026-02-10). Management cited a path to **Rule of 40 >46% today and >50% next year** (NET Q1 2026 call, 2026-05-07).

**Prior quarter (Q4 FY25, 2026-02-10) for context:** revenue $614.5M, +33.6% YoY; FY25 $2,167.9M, +29.8%. Non-GAAP GM 74.9% (just below the 75–77% long-term target); non-GAAP op income $89.6M (14.6% margin); FCF $99.4M (16.2%). DBNR **120%** (+1pt QoQ, +9pt YoY); 4,298 customers >$100k (+23% YoY), 73% of revenue. Closed the largest ACV deal in company history (**$42.5M/yr**) after starting the year with the largest-ever TCV deal ($130M / 5yr); new ACV bookings +~50% YoY (fastest since 2021). RPO $2.496B; FY26 network capex guided to 12–15% of revenue (NET Q4 2025 PR, 2026-02-10; NET Q4 2025 call, 2026-02-10).

## Debate / thesis

- **AI-software read-through — Vercel validates *and contests* the "CDN for tokens" category (Vercel CEO Guillermo Rauch, Stanford MS&E435, 2026-06-29):** Rauch frames token/inference infrastructure (his "AI Gateway") as needing the exact CDN primitives — routing, failover, caching, observability, security, model load-balancing (route a cheap model for "say thanks," not a frontier GPU) — i.e. precisely Cloudflare's Act-3 Workers AI + AI Gateway bet. Independent validation of the TAM, but a reminder the category is contested (Vercel building the same gateway). Agentic-deploy demand inflecting hard (Vercel compute ~3x in months, deployments ~2x since Jan) corroborates NET's own AI-at-the-edge usage signals. See [tokenmaxxing theme](themes/tokenmaxxing.md).
- **Bull:** Cloudflare is a primary beneficiary of the agentic-Internet re-platforming on both sides of the model. CEO Prince: agents are the new users of the web and "Cloudflare is the platform they run on and the network they pass through," creating a flywheel — more agents → more code on Workers → more demand for performance/security/networking (NET Q4 2025 PR, 2026-02-10). "Not all traffic is created equal": NET deliberately avoided commodity bandwidth/video (the legacy CDN game) and sits in front of APIs/applications/agentic requests — "hundreds of billions of agentic requests per month, growing exponentially," vs pure-play CDNs whose traffic "agents aren't going to go watch reruns of the Super Bowl" (NET Q1 2026 call, 2026-05-07). The capital-light AI model (invest behind demand, high GPU utilization) is structurally different from hyperscalers who must invest ahead and "lease a server for 5x." Workers is inflecting (+1M developers/quarter). Go-to-market is firing: sales productivity up for a 9th straight quarter, record $5M+ adds, highest-ever renewal rate (NET Q1 2026 call, 2026-05-07).
- **Bear:** Gross margin is structurally drifting *down* — Q1 GM 72.8%, below the 75–77% long-term target and trending lower as the fast-growing Workers/developer mix (lower margin) and paid-traffic geography shift compound; management is explicitly steering investors toward operating margin / unit economics over gross margin (NET Q1 2026 call, 2026-05-07). The ~20% RIF, however framed, raises questions about whether AI-driven productivity is real leverage or a cost reset, and adds $140–150M of FY26 charges. Net retention has drifted (DBNR 120% Q4 → 118% Q1). Valuation is rich for a name decelerating toward ~30% growth, leaving little room for execution slips. The Act 4 / AI-monetization opportunity is real but largely pre-revenue — "uncharted territory," dependent on lighthouse deals and a micro-payment rail that "nobody can handle the volumes" of yet (NET Q1 2026 call, 2026-05-07).
- **Where the Street stands:** No broker price targets or ratings were present in the local source set (the BofA AKAM/NET-style sell-side notes referenced in the task were not in these files). Sell-side coverage on the calls spans Stifel, Citi, Goldman Sachs, Piper Sandler, RBC, Barclays, TD Cowen, Morgan Stanley, KeyBanc, William Blair, BTIG and Baird (NET Q4 2025 / Q1 2026 calls). _No "Consensus estimates (BBG)" block is hand-written here; the HTML builder injects estimates._
- **Fund read-through (Octahedron 2Q26 LP call — fund view, 2026-07-15):** "Cloudflare would be in this mix as well… especially CrowdStrike, Cloudflare are really hard to touch on valuation as they're so consensus" — a buy-side echo that NET screens as a high-quality but crowded/expensive agentic-Internet name (FUND estimates, not a sell-side rating). (Octahedron 2Q26 call — fund view, 2026-07-15)

## Catalysts / what to watch
- **Annual Investor Day — Tuesday, June 9, 2026** — flagged on the Q1 call; management said it will reframe disclosure toward operating margin / unit economics across the Acts (NET Q1 2026 call, 2026-05-07).
- **Q2 FY26 print** — guide $664–665M / +30% / EPS $0.27; first quarter to show the RIF flowing through opex and whether AE capacity growth actually re-accelerates as promised (NET Q1 2026 call, 2026-05-07).
- **Workers / Act 3 monetization** — developer count (+1M/qtr) vs gross-margin trajectory; whether the >$5.5M developer base converts to revenue without further margin dilution.
- **Act 4 — AI Crawl Control / "pay per crawl"** — one of NET's six stated 2026 priorities is first revenue from the long-tail content-monetization rail; watch lighthouse foundation-model deals and a viable micro-payment partner (NET Q1 2026 call, 2026-05-07).
- **Rule of 40 path** — management guided >46% now, >50% in 2027 — the margin-leverage proof point (NET Q1 2026 call, 2026-05-07).
- **AI-inference-at-the-edge wins** — Dynamic Workers / Workers AI ramps with AI labs (e.g., one studio 0→1M Dynamic Workers in 15 days); read-through to Act 1 traffic as agentic requests scale (NET Q1 2026 call, 2026-05-07).

## Risks
From the FY2025 10-K "Selected Risks" / Item 1A (NET 10-K FY2025):
- **History of net losses** — may not achieve/sustain profitability (still GAAP loss-making: FY25 GAAP net loss $102.3M).
- **Growth durability** — rapid past revenue growth "may not be indicative of future performance."
- **Customer retention / expansion dependence** — model relies on retaining and upselling paying customers and expanding usage; declines in renewals/upgrades/expansions would hit results (ties to the DBNR drift, 120%→118%).
- **Large-customer concentration / execution** — failure to attract, expand and retain large customers (now 72% of revenue) would hurt results.
- **Intense and increasing competition** — across application performance/security, network security and the developer/compute platform (hyperscalers AWS/Azure/GCP, Akamai/Fastly in CDN, Zscaler/Palo Alto in SASE/Zero Trust).
- **Network / co-location dependence** — damage, interference, or loss of co-location, ISP partnerships and interconnection relationships could degrade the network; security breaches or perceived insecurity of the network could erode trust.
- **Content / customer-activity liability** — the activities or content of paying/free customers (and Cloudflare's response) can create political, reputational and legal consequences.
- **Macro / geopolitical** — reduced enterprise security/performance spend, tariffs, conflicts and elections could pressure customers and demand.
- **Key-person / talent** — reliance on co-founders and key sales/technical/management personnel; the ~20% RIF adds execution and retention risk to this.
- **Indebtedness** — convertible senior notes (incl. 2030 Notes) and revolving credit facility — ability to repay when due.

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## Sources
- **Filings:** [NET 10-K FY2025](../CDNs/_imported_from_E_root/NET/NET_10-K_FY2025.htm); [NET 10-K/A FY2025 (amended)](../CDNs/_imported_from_E_root/NET/NET_10-K-A_FY2025_amended.htm); [NET 10-Q Q3 2025](../CDNs/_imported_from_E_root/NET/NET_10-Q_Q3-2025.htm).
- **Press release:** [NET Q4 2025 & FY2025 results (2026-02-10)](../CDNs/_imported_from_E_root/NET/NET_Q4-2025_Press-Release.htm).
- **Transcripts (earnings):** [NET Q1 2026 call (2026-05-07)](../CDNs/_imported_from_E_root/NET/20260507%20-%20ET-E%20-%20NET%20-%20Cloudflare%20Inc%20Q1%202026%20-%203%20pages.pdf); [NET Q4 2025 call (2026-02-10)](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20260210%20-%20ET-E%20-%20NET%20-%20Cloudflare%20Inc%20Q4%202025%20-%203%20pages.pdf); [NET Q3 2025 call (2025-10-30)](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20251030%20-%20ET-E%20-%20NET%20-%20Cloudflare%20Inc%20Q3%202025%20-%203%20pages.pdf); [NET Q2 2025 call (2025-07-31)](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20250731%20-%20ET-E%20-%20NET%20-%20Cloudflare%20Inc%20Q2%202025%20-%203%20pages.pdf).
- **Decks / conference presentations:** [NET Q4 2025 Investor Presentation](../CDNs/_imported_from_E_root/NET/NET_Q4-2025_Investor-Presentation.pdf); [NET Q3 2025 Investor Presentation](../CDNs/_imported_from_E_root/NET/NET_Q3-2025_Investor-Presentation.pdf); conference presentations [2026-03-03](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20260303%20-%20ET-CP%20-%20NET%20-%20Cloudflare%20Inc%20Presents%20at%20-%202%20pages.pdf), [2025-09-09](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20250909%20-%20ET-CP%20-%20NET%20-%20Cloudflare%20Inc%20Presents%20at%20-%202%20pages.pdf), [2025-08-12](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20250812%20-%20ET-CP%20-%20NET%20-%20Cloudflare%20Inc%20Presents%20at%20-%203%20pages.pdf), [2025-05-13](../CDNs/_imported_from_E_root/20260504%20-%20Felipe%20Monteiro%20-%207%20Documents%20-%208_43_01%20AM%20EST/20250513%20-%20ET-CP%20-%20NET%20-%20Cloudflare%20Inc%20Presents%20at%20-%202%20pages.pdf).
- **Cross-name context:** [CDN sector evolution Q2-25→Q1-26](../CDNs/_imported_from_E_root/CDN_Evolucao_Q2-25_Q1-26.docx).
- **Research reports (relatórios bons):** [Octahedron 2Q26 LP call (fund view) (2026-07-15)](../relat%C3%B3rios%20bons/2026_07_15_octahedron_2q_review.html) — read-through: NET grouped with CRWD as high-quality agentic-Internet names "really hard to touch on valuation as they're so consensus" (fund estimates, not a sell-side rating).

## Changelog
<!-- One dated line per material change. Move superseded numbers/ratings/PTs/theses here
     (with the old value + date) instead of deleting them. Newest first. -->
- 2026-07-20 — inbox ingest (read-through only): added one attributed Debate line + a Sources bullet for the Octahedron 2Q26 LP call (fund view, 2026-07-15) — NET grouped with CRWD as high-quality agentic-Internet names "really hard to touch on valuation as they're so consensus." Labeled a fund view (FUND estimates, not a sell-side rating). Additive — no number/rating/PT superseded.
- 2026-06-25 — page created from CDN archive (filings + transcripts + decks).
