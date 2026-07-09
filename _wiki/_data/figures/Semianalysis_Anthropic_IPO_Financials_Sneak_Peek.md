# Semianalysis_Anthropic_IPO_Financials_Sneak_Peek.pdf — figure transcription

Source: SemiAnalysis — "Anthropic 3Q26 Profit Over $1B: The Anthropic IPO Financials Sneak Peak" (Joey Brookhart, Crystal Huang, Dylan Patel), 2026-07-08 (PAID). Forwarded via Daniel Grozdea, 2026-07-08.
Covers the 18 chart/table exhibits (of 25 pages). Machine/vision transcription of figure pages for text search; not an interpretation. All $ figures as printed. **Note on constructs:** "Total Gross Revenue" rows are **quarterly GAAP recognized revenue** ($M); "ARR" figures are **exit run-rate** — do not conflate.

## p.3 — "We Were Right About Anthropic" (stacked column, $B; Source: WSJ + SemiAnalysis Tokenomics Model)
Validation of the Tokenomics model vs WSJ-reported actuals. Four columns: **Q1'26 Actual, Q1'26 (SemiAnalysis), Q2'26 Actual, Q2'26 (SemiAnalysis).** Blue = Revenue (up); green = Compute & infrastructure costs (down); yellow = Other operating costs (down); white line = **Total adjusted operating income** (adjusted ≈ ex-SBC).
- Q1'26 Actual: revenue ≈ $4.7B; adj. operating income ≈ −$0.7B.
- Q1'26 SemiAnalysis: revenue ≈ $4.8B; adj. op inc ≈ −$1.2B.
- Q2'26 Actual: revenue ≈ $11B; adj. op inc ≈ **+$1.0B** (crosses into profit).
- Q2'26 SemiAnalysis: revenue ≈ $11B; adj. op inc ≈ $0.
Takeaway: model tracks WSJ actuals closely; adjusted (ex-SBC) operating income turns positive around Q2'26.

## p.4 — "Anthropic Funding History" (table; Source: SemiAnalysis)
| Round | Date | Amount Raised | Post-money |
|---|---|---|---|
| Series A | May 2021 | $124M | – |
| Series B | Apr 2022 | $580M | – |
| Google | Feb 2023 | $300M | – |
| Series C | Mar 2023 | $300M | $4.1B |
| Amazon | Sep 2023 | up to $4B (initial $1.25B) | – |
| Google | Oct 2023 | up to $2B (initial $500M) | – |
| Series E | Mar 2025 | $3.5B | $61.5B |
| Series F | Sep 2025 | $13B | $183B |
| Series G | Feb 2026 | $30B | $380B |
| Series H | May 2026 | $65B | $965B |
(No Series D row printed.)

## p.7a — "Claude Code Commits as % of All GitHub Commits" (7-day MA; Source: SemiAnalysis Research)
Rises from ~0% (Jan 2025) to a peak ≈ **8.4%** (~Jun 2026); latest labeled **7.297%**. Confirms Claude Code >7% of all GitHub daily commits.

## p.7b — "Anthropic's ARR Trajectory" (line, $B; Jan-24→Jun-26; Source: Tokenomics Model)
Hockey stick from ~$0 to **$60B**. Near-flat ~$0–1B through 2024; ~$9B by end-2025; near-vertical through 1H26 to **$60B by Jun-26**. Dotted markers at each model release (Opus 3 / Haiku 3 → Sonnet 3.5 → Sonnet 3.7 → Opus 4/Sonnet 4 → Opus 4.1 → Sonnet 4.5/Haiku 4.5 → Opus 4.5 → Opus 4.6 → **Fable 5**); the vertical ramp begins around Opus 4.6 (~Dec-25).

## p.8 — Claude API price list (table; Source: Anthropic) — $ per MTok (Base Input / 5m Cache Write / 1h Cache Write / Cache Hits & Refresh / Output)
- **Fable 5:** $10 / $12.50 / $20 / $1 / $50
- **Mythos 5** (limited availability): $10 / $12.50 / $20 / $1 / $50
- **Opus 4.8 / 4.7 / 4.6 / 4.5:** $5 / $6.25 / $10 / $0.50 / $25
- Opus 4.1 (deprecated) / Opus 4 (retired ex-Google Cloud): $15 / $18.75 / $30 / $1.50 / $75
- **Sonnet 5 (through Aug 31, 2026):** $2 / $2.50 / $4 / $0.20 / $10
- **Sonnet 5 (starting Sep 1, 2026):** $3 / $3.75 / $6 / $0.30 / $15  ← price **increase** on the newest mid-tier
- Sonnet 4.6 / 4.5 / 4 (retired ex-Bedrock+GCP): $3 / $3.75 / $6 / $0.30 / $15
- Haiku 4.5: $1 / $1.25 / $2 / $0.10 / $5
- Haiku 3.5 (retired ex-Bedrock+GCP): $0.80 / $1 / $1.60 / $0.08 / $4
Note the Sonnet 5 step-up ($2/$10 → $3/$15 on 9/1/26) — the note cites this as evidence even lower-tier closed models can command higher pricing than prior gens.

## p.9a — "Less Consumer, Better Business: Consumer Subscription Mix, Anthropic vs OpenAI" (line, % of revenue; 1Q24→4Q26)
- **Anthropic:** ~11% (1Q24) declining to ~4% (4Q26) — structurally low-consumer.
- **OpenAI:** ~59% (1Q24) rising to peak ~66% (1Q25 & 3Q25), then falling sharply to ~21% (4Q26).

## p.9b — "OpenAI ARR by Segment" (stacked/grouped bars, $M; 1Q24→4Q26) [OpenAI comparator]
Segments: Consumer, Business, Enterprise, API, Ads. **API** explodes to ~$59B (4Q26); Consumer ~$18B; Enterprise ~$6–7B; Ads ~$1.5B. Shows OpenAI's late pivot to API/B2B.

## p.10 — "Demand Is The Story, Not Pricing Power" (dual-axis line; 1Q24→4Q26)
- **Token Volume** (red, left axis, Tn tokens/yr): near-flat 2024–2025, then exponential from 1Q26, steepest into 4Q26.
- **Blended Token Price** (green, right axis, $): high in 1H24, collapses through 3Q24–4Q24, then roughly flat (small bump ~3Q25) and slightly declining.
Takeaway: revenue growth is driven by the volume/consumption curve, not price.

## p.11 — API build by model family (table; Tokenomics Model, Anthropic Tab; quarterly 1Q24→4Q26 + "2030 input")
Rows per family: API revenue %, avg input/output mix, cache-hit rate, cache-write rate, **blended price per MTok**, API tokens produced (T tokens, annualized run-rate), API revenue ($M).
- **Opus 4.6 Fast Mode:** blended $/MTok 6.44 → 5.65 → 5.22 → 4.84 (1Q26→4Q26); API rev $2,036 → 4,316 → 6,996 → 10,196M.
- **Opus 4.6/4.5:** blended $/MTok 1.30 → 1.07 → 0.93 → 0.87; API rev $17,815 → 38,305 → 62,964 → 94,313M; tokens 16,593 → 41,022 → 72,691 → 117,355 (T, annualized).
- **Opus 4.1/4/3:** blended $/MTok falls 13.97 (1Q25) → ~3.16 (4Q26); small/declining API rev.
- **Sonnet 4.6/4.5/4/3.7/3.5/3:** blended $/MTok 2.79 (1Q25) → ~0.53 (2H26); API rev $4,581 → 9,711 → 15,741 → 21,667M (1Q26→4Q26); tokens 7,111 → 41,099 T.
Pattern: blended $/MTok falls sharply within each family while token volume and $ revenue rise — volume more than offsets price.

## p.12 — "Consumer Subscription Build" (table; Tokenomics Model, Anthropic Tab; quarterly)
- **Consumer MAU, end of period (M):** …12.40 (4Q25) → **39.44 (1Q26)** → 61.27 → 77.62 → **93.97 (4Q26)** — the 4Q25→1Q26 jump reflects the "Department of War" consumer bump.
- Paying-subscriber attach rate of MAU: ~9–11% → held ~9%.
- **Blended Consumer Subscription ARPU, monthly ($):** 20 → 20 → 25 → 30 → 35 → 38 → **40 (1Q26) → 45 (2Q26)** → 51 → 56 (4Q26). (Text: "avg paying US consumer ≈ $45/month" = 2Q26.)
- SKU pricing: Pro $20/mo ($17 billed annually); Max 5x $100/mo; Max 20x $200/mo.
- Paid SKU mix shifting toward Max tiers over time (Max 20x 5%→18% of paid by 4Q26).
- **Consumer Subscription ARR, end of period ($M):** 400 (4Q25) → **1,550 (1Q26)** → 2,759 → 3,911 → 5,237 (4Q26).

## p.13 — "Anthropic's Monthly Net New ARR" (line, $B; Jan-24→Jun-26)
Flat ~$0 through 2025; ramps vertically from Dec-25; spikes to ~**$11B (Mar-26)**, dips to ~$10B, then ~**$12B (Jun-26)**. Confirms NNARR now ~$10–12B/month.

## p.14a — "Inference Build" (table; Tokenomics Model, Anthropic Tab; quarterly)
- Implied Training Spend per MW ($M): ~2.0–2.8 across periods.
- **Gross Margin, Paid Inference:** (94%)×4 in 2024 → **41%** across 2025 → **63% / 64% / 66% / 67%** (1Q26→4Q26).
- **Total Gross Margin (incl. free-user inference):** (94%) 2024 → **38%** 2025 → **60% / 62% / 64% / 65%** (2026).
- **Total Inference Compute (MW):** 133 (1Q25) → 450 (4Q25) → **1,154 (1Q26) → 2,292 → 3,528 → 4,745 (4Q26)**.
- Average ARR-in-period per Inference MW ($M): ~$16.7M (4Q25) → ~$16.9M (1Q26) → ~$20M → ~$23M → ~$25M (4Q26). [In-period average; distinct from the note's "$60M ARR/MW later this year," which is a point-in-time run-rate ÷ current inference MW. The "$16M nine months ago" claim ties to the ~4Q25 value here.]

## p.14b — "Gross Margin Over Time: Anthropic vs OpenAI" (line, %; 1Q24→1Q26)
- **Anthropic:** ~−94% (all 2024) → jumps to ~+38% (1Q25), flat ~38–40% through 4Q25 → rises to ~**60% (1Q26)**.
- **OpenAI:** steady ~38–42% throughout, dips to ~31% (4Q25), ~38% (1Q26).
Anthropic crosses above OpenAI on gross margin in 1Q26.

## p.15 — "Inference Margin Build" (table; Tokenomics Model, OpenAI Tab; quarterly 4Q23→4Q26) [OpenAI comparator]
- Total Revenue ($M): 521 (4Q23) → 4,800 (4Q25) → 5,877 → 8,778 → 13,721 → **19,132 (4Q26)**.
- Gross Margin, Paid Inference: ~40–50% 2024 → ~62–68% 2026 (lower blended than Anthropic due to free-user drag).
- **Microsoft Revenue Share** (Actual, $38B cap, $M): 77 → … → 550 (4Q25) → 647 → 966 → 1,509 → 2,066 (4Q26); ~11% of total revenue; implied MSFT inference-compute routing ~54–57%.

## p.16 — "Consolidated Income Statement" (table; Tokenomics Model, Anthropic Tab; $M, quarterly 1Q24→4Q26) — **core P&L**
| Line ($M) | 4Q25 | 1Q26 | 2Q26 | 3Q26 | 4Q26 |
|---|---|---|---|---|---|
| Consumer Subscription Rev | 91 | 259 | 565 | 875 | 1,195 |
| Business Subscription Rev | 38 | 98 | 198 | 300 | 411 |
| Enterprise Subscription Rev | 134 | 385 | 825 | 1,275 | 1,725 |
| API Revenue | 1,613 | 4,149 | 9,925 | 17,675 | 26,863 |
| **Total Gross Revenue** | **1,876** | **4,890** | **11,513** | **20,125** | **30,194** |
| COGS, Inference | 1,163 | 1,956 | 4,375 | 7,245 | 10,558 |
| Gross Profit | 713 | 2,934 | 7,138 | 12,880 | 19,626 |
| Training Costs | 1,400 | 2,054 | 4,605 | 7,647 | 10,870 |
| Other OpEx | 900 | 2,000 | 3,000 | 4,000 | 6,000 |
| Other OpEx % of Rev | 48% | 41% | 26% | 20% | 20% |
| **GAAP Operating Income** | (1,587) | (1,120) | (467) | **1,232** | **2,756** |
| **EBTIT** (excl. Training) | (187) | 934 | 4,138 | 8,880 | 13,626 |
(Full history 1Q24→3Q25 also printed; all quarters through 4Q25 negative on both GAAP OI and EBTIT except EBTIT which is small-negative into 4Q25.)
Reconciliation: GAAP OI = Gross Profit − Training − Other OpEx; EBTIT = GAAP OI + Training. **GAAP OI turns positive in 3Q26 at $1.23B (6.1% margin)** — the note's "$1B profit / 6% margin" headline. **EBTIT turns positive in 1Q26**; 2Q26 EBTIT margin = 4,138/11,513 = **36%**. FY26: GAAP OI ≈ +$2.4B; EBTIT ≈ **+$27.6B**. Also printed: implied per-MW metrics, topline growth %, cost %, and implied token metrics (API Revenue per M tokens falls 5.60 → 0.65 $/M).

## p.17 — "Coding Market Vertical, ARR by Company" (line, $M; 1Q24→4Q26)
- **Anthropic 1P coding spend** (teal): explodes to ~**$92–93B** (4Q26, annualized run-rate).
- **OpenAI 1P coding spend** (purple): rises to ~**$41B**.
- Anthropic/OpenAI 3P application-company coding spend + Replit, Cursor, Windsurf, Cognition, Lovable, GitHub Copilot: all small (few $B each; the note pegs coding startups at +$6B ARR as of 2Q26).

## p.18/19 — "Total TaaS Market ARR" (line, $M; 1Q24→4Q26)
- Amazon Bedrock (blue): → ~**$29B** (4Q26).
- Google Enterprise Agent Platform / Vertex (yellow): → ~**$24B**.
- Microsoft Foundry (green): → ~**$5B**.
- Others (Together, Fireworks, Baseten, OpenRouter) (red): → ~**$10.5B**.
Total TaaS ARR ≈ $68B annualized by 4Q26 (note: ~$28B as of 2Q26); big-3 clouds ≈ 85% share.

## p.23 — "Anthropic vs OpenAI: Annual EBIT, FY24–28E" (line, $B)
- **Anthropic** (blue): ~$0 (2024) → ~−$2 (2025) → ~**+$27 (2026)** → ~+$110 (2027) → ~**+$227 (2028)**.
- **OpenAI** (orange): ~−$2 (2024) → ~−$8 (2025) → ~−$15 (2026) → ~+$13 (2027) → ~+$73 (2028).
Titled "EBIT," but the magnitudes match the note's **EBTIT** series (2026 ≈ $27B = the EBTIT sum on p.16, not GAAP OI ≈ $2.4B) — i.e. this is the pre-training-reinvestment profit metric. Cumulative Anthropic-over-OpenAI advantage ≈ **$250B through 2028** (note's stated figure).

## Not transcribed (no data figures)
p.1–2 (email header / title), p.5–6 (text), p.20 (small logo), p.21–22 & p.24 (text), p.25 (Substack footer: "© 2026 Dylan Patel, 548 Market Street PMB 72296, San Francisco, CA 94104").
