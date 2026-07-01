# SHOP — Shopify Inc.

_Wiki · generated 2026-06-20 · sources: `E:\Wiki Felipe\SHOP` (10-K/10-Q + transcripts) · `_briefings` (May–Jun 2026 roll-up). Master index: [00_INDEX.md](00_INDEX.md)._

<!-- SNAPSHOT:START (auto: _tools/build_snapshot.py — do not hand-edit) -->
### 📊 Consensus snapshot — BBG · asof  · USD

| Metric | CY2026E | CY2027E |
|---|--:|--:|
| Revenue | $14.7bn | $18.1bn |
| Gross profit | $7.0bn | $8.5bn |
| Gross margin | 47.2% | 46.9% |
| EBITDA | $2.7bn | $3.4bn |
| EPS | $1.87 | $2.43 |
| Capex | $30m | $37m |
| OCF (≈EBITDA) | $2.7bn | $3.4bn |

_Gross profit = Revenue × GM%. OCF: no forward BBG consensus — EBITDA shown as proxy._
<!-- SNAPSHOT:END -->

## Snapshot
Global commerce operating system: a multi-tenant cloud platform that lets merchants — SMB to enterprise — start, run and scale a business across online, offline (POS), B2B and social/marketplace channels. Two revenue legs: **Subscription Solutions** (~24% of rev; recurring plan fees, Plus/enterprise, apps, themes, domains) and **Merchant Solutions** (~76% of rev; payments, capital/lending, shipping, ads/Shop Campaigns) — the latter is GMV-correlated and the growth engine, but lower-margin (Shopify Payments drags blended GM) (10-Q Q1 FY26, 2026-05-05). FY25: **GMV $378B (+29%), revenue $11.6B (+30%), FCF $2.0B / 17% margin** (Q4 FY25 call, 2026-02-11). >21,000 apps in the App Store; ~7,600 employees; >14% of U.S. e-commerce; ~half of merchants now outside North America (10-K FY25, 2026-02-11). In the AI value chain SHOP is a **commerce-platform/payments layer** — consumes cloud (Google Cloud) + payment rails, sells software + take-rate to merchants — and is positioning to be the **transaction back-end for agentic commerce** via UCP and Agentic Storefronts. Founder/CEO Tobi Lütke holds a Founder Share (concentrated voting). Files as a U.S. domestic-style registrant despite foreign-private-issuer status.

## At a glance — product · buyer · supplier
| | |
|---|---|
| **Sells (top 3)** | 1) Merchant Solutions / Shopify Payments + Shop Pay (~76% of rev, GMV take-rate) · 2) Subscription Solutions / Plus plan fees (~24% of rev, recurring) · 3) Merchant add-ons — Capital/lending, shipping/fulfillment, ads (Shop Campaigns) + App Store |
| **Main buyer(s)** | Merchants SMB→enterprise (pay subscription + take-rate, ~half now outside North America) and consumers who check out via Shop Pay |
| **Key suppliers** | Google Cloud (hosting/compute); card networks/acquirers + Shopify Payments processing partners (payment rails) |

## Position in the value chain
SHOP sits between infrastructure suppliers (cloud compute, card networks/acquirers) and the demand side (merchants who pay subscription + take-rate; consumers who check out, increasingly via Shop Pay). It captures economics on *both* GMV (payments/merchant solutions) and seats (subscriptions). The live structural debate is **agentic commerce**: bull case = AI agents are a new top-of-funnel that *expands* transactions SHOP clears (UCP keeps the checkout on Shopify — "LLMs do not bypass Shopify's checkout," Finkelstein, Q4 FY25); bear case = LLM storefronts (ChatGPT/Gemini/Copilot) become the buying surface and *disintermediate* the merchant-consumer relationship and the take-rate.

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12">
  <rect x="10" y="60" width="150" height="100" rx="6" fill="#eef2f7" stroke="#4a5568"/>
  <text x="85" y="82" text-anchor="middle" font-weight="bold">Suppliers</text>
  <text x="85" y="104" text-anchor="middle">Cloud (Google</text>
  <text x="85" y="120" text-anchor="middle">Cloud), compute</text>
  <text x="85" y="138" text-anchor="middle">Payment rails /</text>
  <text x="85" y="154" text-anchor="middle">card networks</text>

  <rect x="255" y="50" width="200" height="120" rx="6" fill="#dbeafe" stroke="#1e40af" stroke-width="2"/>
  <text x="355" y="74" text-anchor="middle" font-weight="bold">Shopify</text>
  <text x="355" y="96" text-anchor="middle">Commerce platform</text>
  <text x="355" y="114" text-anchor="middle">Merchant software +</text>
  <text x="355" y="132" text-anchor="middle">Payments (Shop Pay) +</text>
  <text x="355" y="150" text-anchor="middle">Fulfillment / Capital</text>

  <rect x="550" y="60" width="160" height="100" rx="6" fill="#eef2f7" stroke="#4a5568"/>
  <text x="630" y="82" text-anchor="middle" font-weight="bold">Customers</text>
  <text x="630" y="104" text-anchor="middle">Merchants:</text>
  <text x="630" y="120" text-anchor="middle">SMB → enterprise</text>
  <text x="630" y="142" text-anchor="middle">Consumers via</text>
  <text x="630" y="158" text-anchor="middle">Shop Pay</text>

  <line x1="160" y1="110" x2="253" y2="110" stroke="#4a5568" stroke-width="2" marker-end="url(#a)"/>
  <line x1="455" y1="110" x2="548" y2="110" stroke="#4a5568" stroke-width="2" marker-end="url(#a)"/>

  <text x="355" y="200" text-anchor="middle" font-style="italic" fill="#b45309">Agentic-commerce debate: bull = AI agents expand transactions (UCP keeps checkout on SHOP); bear = LLM storefronts disintermediate.</text>
  <defs>
    <marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#4a5568"/>
    </marker>
  </defs>
</svg>

## Current state (latest quarter)
**Q1 FY26 (call 2026-05-05).** Above-trend print, then sold off ~19% by mid-quarter on margin/comp worries (JPM Smilek, briefing 2026-05-28).
- **GMV $101B, +35% y/y (+30% cc)** — 2nd straight quarter >$100B. **Revenue $3.17B, +34%** (subscription $750M +21%; merchant solutions $2,420M +39%) (10-Q Q1 FY26).
- **Take-rate / attach climbing:** Merchant Solutions now **76% of revenue** (vs 74% y/y). **Shopify Payments $67B GMV, +41%, = 67% of total GMV** (+3pp). **Shop Pay $35B GMV, +59%** (intl +70%+). MRR $212M +16%; Plus = 35% of MRR.
- **FCF $476M, 15% margin** — 4 straight quarters of 30%+ growth at mid-to-high-teens FCF margin. OpEx 37% of rev (-4pp y/y), headcount flat. GAAP net loss $(581)M is driven by a $(1,082)M mark on equity investments — non-operating; income from operations was +$382M (10-Q).
- **Agentic commerce signal:** AI-driven traffic **+8x y/y**, orders from AI search **~+13x**, converting ~2x organic; **UCP** open protocol with Amazon/Meta/Microsoft/Salesforce/Stripe; Sidekick weekly-active shops +385%. AI writes >50% of SHOP's code.
- **Intl/enterprise:** intl GMV +45% (Europe +48%), NA strongest in 4+ yrs; $100M+ GMV merchants nearly doubled in 2yrs (LVMH, Victoria's Secret, Mulberry, Orvis, Lands' End onboarded); B2B GMV +80%; offline +33%; Shop app GMV +70%.
- **Q2 FY26 guide:** revenue growth **high-20s%**, GP growth mid-20s%, OpEx 35-36%, FCF margin mid-teens; only ~0.5pt FX tailwind vs >2pt in Q1 (i.e. tougher optical comp into 2H — Rothschild: H2 comps ~400bps harder, briefing 2026-05-28).

## Debate / thesis
- **Bull:**
  - **Agentic commerce is a TAM expander, not a threat** — SHOP owns the structured catalog + checkout; UCP (co-built w/ Google) keeps the transaction on Shopify even when discovery moves to LLMs. "LLMs do not bypass Shopify's checkout… this is where Shopify shines" (Finkelstein, Q4 FY25, 2026-02-11). MS TMT Spec-Sales framing: agentic commerce = "big getting bigger," GOOGL on data/protocol, AMZN on logistics, **SHOP on inventory** (briefing 2026-05-20). JPM (Smilek) calls GOOGL's universal cart SHOP's "most compelling AI shopping breadth partner" (briefing 2026-05-28).
  - **Compounding GMV + rising attach** — **JPM (Smilek/Anmuth) OW, PT $150**: 3-yr GMV/GP CAGR 20%+, FCF ~30%, OpInc 30%+; Platinum-partner channel check positive — "low META disruption risk," enterprise bullish, Sidekick strong, demand solid (briefings 2026-06-09, 2026-06-12). Spring 2026 Editions: 150+ updates, AI Catalog ~2x conversions vs scraped data, Shop Pay expanding to non-SHOP brands (250M+ shoppers) (briefing 2026-06-12).
  - **AI beneficiary in survey work** — MS AlphaWise: POS adoption ~2x y/y, merchants now run ~4 Shopify services (was ~3); "XYZ/SHOP/Stripe momentum" (briefing 2026-05-29). DB (Bhavin Shah): "strong 1Q presents a buying opportunity" (briefing 2026-05-06). SHOP on MS TMT Sales favorite-software list (briefing 2026-06-01).
  - **Ads as an underappreciated attach lever — Shop Campaigns** — UBS deep dive (~20-page overview) frames Shop Campaigns (Shopify's ad/merchant-acquisition product inside Merchant Solutions) as an incremental monetization leg, laying out an illustrative framework to quantify the potential upside opportunity to take-rate/attach from advertising; no specific dollar/GM figures disclosed in the note (UBS/Chiodo — Shop Campaigns, 2026-06-22).
- **Bear:**
  - **AI/token-cost margin drag** — JPM TMT desk's recurring "AI Token Costs Eating Internet Profits Alive" (SHOP/SPOT/META/PINS): JPM models **~$9M hit to Q1 Subscription COGS (~120bps Sub GM / ~30bps total GM), ~160bps/~40bps Y/Y 2026 Sub/Total GM headwind** (briefings 2026-05-06, 2026-05-28). The mix shift to lower-margin payments is itself a structural GM drag (10-Q "change in revenue mix").
  - **Comp / attach sustainability + competition** — Rothschild (Raj Chaudhury, Buy but cautious): Q2 fine but Q3 guide "just enough," bears get intra-quarter ammo, H2 comps ~400bps tougher, Q2 guide implies ~29-30% cc vs Q1's 30%; short interest rising; competitive pressure from **Stripe + Meta + agentic ecommerce**; caution on medium-term attach-rate sustainability (briefing 2026-05-28).
  - **Disintermediation tail** — if LLM storefronts (ChatGPT/Gemini/Copilot, OpenAI's SMB-advertiser push) capture discovery *and* checkout, the merchant relationship and take-rate are at risk. MS PYPL bear note cites "Apple/Shopify/agentic" as the competitive-intensity vector across payments (briefing 2026-05-13) — i.e. the same agentic shift cuts both ways.
  - Positioning: post-Q1 cohort weakness flagged; "sold on print," crowded internet positioning (TMTB via briefing 2026-05-13).
- **Where the sell-side/buy-side stands:** Constructive into mid-2026. **JPM (Smilek/Anmuth) OW, PT $150** (reiterated 2026-06-09/06-12). **DB (Bhavin Shah)** buying-opportunity stance (2026-05-06). **Rothschild (Chaudhury) Buy** but flags H2 comp/attach risk (2026-05-28). UBS (Chiodo) ran two SHOP deep-dive expert calls into June (long-term growth-algorithm framing; checkout-button benchmarking PayPal/Shop Pay/Apple Pay) (briefings 2026-05-29, 2026-06-09). Heavy IR access (UBS NY NDR 6/1; JPM IR cocktails 5/12). Live edge = the agentic-commerce expander-vs-disintermediation split and whether attach/GM can hold through tougher 2H comps. _(No SHOP entry in `_data/estimates.json` yet — consensus block not auto-injected.)_

## Catalysts / what to watch
- **Q2 FY26 print** — ~early Aug 2026 (cadence: Q1 was 2026-05-05). Watch: GMV growth into tougher comps (guide high-20s rev, ~0.5pt FX tailwind only), attach-rate/Payments penetration, AI/token COGS trajectory vs JPM's ~160bps 2026 Sub-GM model.
- **Agentic-commerce proof points** — UCP adoption with Amazon/Meta/Microsoft/Salesforce/Stripe + Google universal cart; AI-search order conversion durability beyond the small base.
- **Spring/Fall 2026 Editions** — product cadence (AI Catalog, Sidekick, Shop Pay to non-SHOP brands / 250M+ shoppers).
- **Enterprise pipeline** — $100M+ GMV merchant adds, B2B (+80% y/y) ramp.
- **Capital return** — $2B buyback execution (authorized Q4 FY25).

## Risks
- **Merchant retention / SMB cyclicality** — low switching cost; SMB exposure to consumer spend, inflation, tariffs/trade measures (10-K FY25 risk factors).
- **GM compression** — mix shift to lower-margin Shopify Payments + AI/token COGS (10-Q; JPM token-cost thesis).
- **Competition** — ecommerce SW, payment processors, marketplaces, and large platforms restricting data access (Meta/Apple/Amazon); Stripe in payments; agentic disintermediation by LLM storefronts (10-K; Rothschild 2026-05-28).
- **Third-party dependence** — Google Cloud hosting + Shopify Payments processing partners; outage/DDoS/cyber-breach exposure given large attack surface (10-K).
- **Regulatory** — financial-services/lending (Shopify Payments, Shopify Capital), data privacy, sanctions/AML, online-liability for merchant content; AI-specific regulation (10-K).
- **Governance** — Founder Share concentrates voting with CEO; FX (EUR/GBP/CAD); large non-operating equity-investment marks swing GAAP results (10-Q).

<!-- Consensus estimates (BBG) block auto-injected here by the HTML builder -->

## In the inbox (Outlook — recent sell-side flow)
- **UBS (Chiodo) — 'Shopify: Shop Campaigns Overview & Analysis'** _(2026-06-22)_: video recap of a ~20-page deep dive on the Shop Campaigns ad product, with an illustrative framework to quantify the potential upside opportunity (monetization/attach read-through).
- **Rothschild TMT Daily** _(2026-06-19)_: SHOP in focus (with AMZN/META).
- **JPM 'Agentic World: AMZN/WMT Deep Dive'** _(2026-06-18)_: the agentic-commerce debate — AI agents as TAM-expander vs LLM-storefront disintermediation.

## Intra-quarter — calls, commentary & reports (since the last print)
_Q1 FY26 · May 5 → Jun 22, 2026 · sell-side / expert calls / reports between earnings. Timeline visual: [timeline.html](timeline.html)._

**Signal vs management** — what management said on the last call × what the intra-quarter flow is saying (✓ confirms · ⚠ nuances · ✗ contests):

| Theme | Management said (Q1 FY26) | Intra-quarter flow | Signal |
|---|---|---|---|
| **Demand / GMV** | GMV $101B (+35% y/y, +30% cc); 2nd quarter >$100B | JPM (Smilek/Anmuth): Platinum-partner channel bullish, demand solid; MS AlphaWise: POS ~2x y/y, ~4 services/merchant | **✓ confirms** (channels corroborate) |
| **Margin** | FCF $476M (15% margin) | JPM desk: AI token cost ~$9M/Q (~120bps Sub GM, FY26 headwind ~160bps); UBS Chiodo: Shop Campaigns as an incremental monetization leg | **⚠ nuance** (token cost vs ads upside) |
| **Agentic / AI** | AI traffic +8x, AI orders ~+13x; UCP scaling | MS Spec-Sales: "big getting bigger" (SHOP on inventory); JPM: TAM-expander vs disintermediation-by-LLM-storefronts debate | **⚠ nuance** (double edge of agentic) |
| **Product** | UCP with Amazon/Meta/MSFT/Salesforce/Stripe | JPM: Spring '26 Editions 150+ updates, AI Catalog ~2x conversions, Shop Pay for non-SHOP brands (250M+) | **✓ confirms** (roadmap delivering) |
| **Guidance / comp** | Q2 guide revenue high-20s%; only ~0.5pt FX | Rothschild (Chaudhury): Q3 guide "just enough", H2 comps ~400bps harder, short interest rising | **⚠ nuance** (H2 comp tightens) |

**Full log** (all intra-quarter flow, by date):

| Date | Source | Theme | Bias | What was said |
|---|---|---|---|---|
| 05-06 | JPM (desk) | margin | bear | JPM TMT desk recurring "AI Token Costs Eating Internet Profits Alive" (SHOP/SPOT/META/PINS): models ~$9M hit to Subscription COGS in Q1 (~120bps of Sub GM / ~30bps of total GM), with a 2026 y/y headwind of ~160bps/~40bps to Sub/Total GM. |
| 05-06 | DB · Bhavin Shah | valuation | bull | DB (Bhavin Shah): "strong 1Q presents a buying opportunity". |
| 05-13 | Morgan Stanley (PYPL note) | competition | mixed | MS PYPL bear note cites "Apple/Shopify/agentic" as a competitive-intensity vector in payments — the same agentic shift cuts both ways. |
| 05-20 | Morgan Stanley · TMT Spec-Sales | demand | bull | MS TMT Spec-Sales: agentic commerce = "big getting bigger" — GOOGL on data/protocol, AMZN on logistics, SHOP on inventory. |
| 05-28 | Rothschild · Raj Chaudhury | guidance | bear | Rothschild (Chaudhury, Buy but cautious): Q2 ok but Q3 guide "just enough"; bears gain ammunition intra-quarter; H2 comps ~400bps harder; Q2 guide implies ~29-30% cc vs 30% in Q1; short interest rising; competitive pressure from Stripe + Meta + agentic ecommerce. |
| 05-29 | Morgan Stanley · AlphaWise | demand | bull | MS AlphaWise: POS adoption ~2x y/y, merchants now run ~4 Shopify services (was ~3); "XYZ/SHOP/Stripe momentum". |
| 06-09 | JPM · Smilek/Anmuth | valuation | bull | JPM (Smilek/Anmuth): Overweight, PT $150 — 3-year GMV/GP CAGR 20%+, FCF ~30%, OpInc 30%+; positive Platinum-partner channel check — "low META disruption risk", enterprise bullish, Sidekick strong, demand solid. |
| 06-12 | JPM · Smilek/Anmuth | product | bull | JPM: Spring 2026 Editions — 150+ updates, AI Catalog ~2x conversions vs scraped data, Shop Pay expanding to non-SHOP brands (250M+ shoppers). OW PT $150 reiterated. |
| 06-18 | JPM · 'Agentic World: AMZN/WMT Deep Dive' | demand | mixed | JPM (Outlook): agentic-commerce debate — AI agents as TAM-expander vs disintermediation by LLM storefronts. |
| 06-19 | Rothschild · TMT Daily | valuation | neutral | Rothschild TMT Daily (Outlook): SHOP in focus (with AMZN/META). |
| 06-22 | UBS · Chiodo | margin | bull | UBS (Chiodo, Outlook): 'Shopify: Shop Campaigns Overview & Analysis' — ~20-page deep dive into the Shop Campaigns ads product as an incremental monetization leg, with an illustrative framework to quantify the potential take-rate/attach upside; no specific dollar/GM figures disclosed. |

**Quarter synthesis:** the debate has shifted from "GMV growth" (confirmed, channels bullish) to margin sustainability — AI inference cost vs new monetization legs (Shop Campaigns/Shop Pay) — and to the double-edged sword of agentic commerce (TAM-expander vs disintermediation by LLM storefronts), with H2 comps giving the bears ammunition.

## Management commentary — evolution (last 4 quarters)

| Theme | Q2 FY25 (2025-08-06) | Q3 FY25 (2025-11-04) | Q4 FY25 (2026-02-11) | Q1 FY26 (2026-05-05) |
|---|---|---|---|---|
| GMV / demand | $88B, +31% y/y (+29% cc) | +32% y/y, intl & enterprise strong | $124B, +31% y/y — first qtr >$100B | $101B, +35% y/y (+30% cc) |
| Revenue growth | $2.7B, +31% y/y, broad-based | +32% y/y | $3.01B; FY25 $11.6B, +30% | $3.17B, +34% y/y |
| Payments / Shop Pay penetration | — | mix shift to payments-led solutions | Payments 68% of GMV; Shop Pay $43B | Payments 67% of GMV; Shop Pay $35B, +59% |
| Agentic commerce / AI | — | AI driving merchant efficiency | AI orders +15x since Jan'25; UCP w/ Google | AI traffic +8x, AI orders ~+13x; UCP scaling |
| International / enterprise | Intl GMV +42%; Europe +49%; B2B +101% | — | Intl rev +36%; GM/Sonos/L'Oreal; B2B +96% FY | Intl GMV +45%; LVMH/VS onboarded; B2B +80% |
| FCF / margin | FCF $422M, 16% margin (11th straight) | FCF & profitability "remain robust" | FY25 FCF $2.0B, 17%; Q4 19%; $2B buyback | FCF $476M, 15% margin |

_Source: SHOP earnings calls (dates above); management commentary, paraphrased._

## Sources
- **Filings:** [10-K FY2025 (2026-02-11)](../SHOP/SHOP_10-K_2026-02-11_0001594805-26-000007.html); [10-Q Q1 FY2026 (2026-05-05)](../SHOP/SHOP_10-Q_2026-05-05_0001594805-26-000019.html).
- **Transcripts (saved):** [Q1 FY26 (2026-05-05)](../SHOP/transcripts/SHOP_Q1-2026-earnings_2026-05-05.md); [Q4 FY25 (2026-02-11)](../SHOP/transcripts/SHOP_Q4-2025-earnings_2026-02-11.md); [Q3 FY25 (2025-11-04)](../SHOP/transcripts/SHOP_Q3-2025-earnings_2025-11-04.md); [Q2 FY25 (2025-08-06)](../SHOP/transcripts/SHOP_Q2-2025-earnings_2025-08-06.md). _(Two latest read in full; Q3/Q2 saved as headline summaries.)_
- **Briefings:** May–Jun 2026 morning + company-specific roll-up (no `_briefings/by-ticker/SHOP.md` rollup file yet) — datapoints from 2026-05-06, 05-13, 05-20, 05-28, 05-29, 06-01, 06-09, 06-12.
- **Outlook:** attempted (`outlook.py --no-body --days 7`) — returned no output in this environment; treated as unavailable. Sell-side attribution above is sourced from the briefings corpus.
