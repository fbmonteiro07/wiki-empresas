# ev-state-of-ai-economy-2026.pdf — figure transcriptions (part 2)

Report: "ev-state-of-ai-economy-2026.pdf" (Exponential View, "State of the AI Economy 2026").
Pages covered in this file: 42, 52, 54, 57, 58, 59, 60, 61, 63, 65, 66.
Note: machine transcription of figure/chart pages so the data is text-searchable. Values read from chart images; approximate where unlabeled.

## p.42 — The transition from chat to agents is multiplying token use

Section header: "4 | Tokens: The unit of value for the AI economy?"

**Left chart — Agent coordination density** (% tool use per prompt, OpenRouter; line chart, Jan 26–Jun 26):
- Jan 26: ~5%; rises to ~6.5% then dips
- Feb 26: ~7–10% (peak ~10% end-Feb)
- Mar 26: ~9–13.5% (peak ~13.5%), dip to ~10.5%
- Apr 26: ~12.5–13.5%, dip to ~10.5–11%
- May 26: ~11.5–13%
- Jun 26: rises to ~15% at end of series

**Right chart — Token consumption per task** (average tokens consumed per task, log scale; horizontal stacked bars, Output tokens vs Input tokens; x-axis: Tokens per task, log scale 100 → 10m):

| Task | Total | Output tokens | Input tokens |
|---|---|---|---|
| Code Reasoning (single-turn) | 1.19k | 1.03k output | 0.16k input |
| Code Chat (multi-turn) | 3.39k | 1.45k output | 1.94k input |
| Agentic Coding (OpenHands agent) | 4.17m | 26.93k output | 4.14m input |

Annotation on Agentic Coding bar: "≈1,200× the tokens of a chat task".

Source line: "Sources: Exponential View analysis; OpenRouter; Bai, Huang, Wang, Sun, Mihalcea, Brynjolfsson and Pentland 2026."

## p.52 — Section divider: 5 | Stack: Where the value is captured

(no chart data — section divider) Text: "Revenue is concentrated, but apps and models are gaining share. Labs retain pricing only while they hold the frontier; the economic value of yesterday's frontier diminishes quickly into open weights. Where margin accrues across the stack will depend on technical advancements, which cut across competitive dynamics."

## p.54 — Revenue is concentrated today, but the mix is shifting

Two horizontal bar charts: Annualized GenAI revenue, $million, Q1 2024 (left) vs Q1 2026 (right). Categories (legend): Apps (yellow), Foundation Models (teal), Hosting (purple), Chips (green). Axis $0–$300,000 ($m). Approximate values read from bars:

| Company | Category | Q1 2024 ($m annualized, approx) | Q1 2026 ($m annualized, approx) |
|---|---|---|---|
| Cursor | Apps | ~0 | ~2,000 |
| Anthropic | Foundation Models | ~1,000 | ~20,000 |
| OpenAI | Foundation Models | ~3,000 | ~27,000 |
| Google | Hosting | ~1,000 | ~30,000 |
| Microsoft | Hosting | ~5,000 | ~23,000 |
| AWS | Hosting | ~2,000 | ~10,000 |
| Nebius | Hosting | ~0 | ~4,000 |
| CoreWeave | Hosting | ~500 | ~9,000 |
| Oracle | Hosting | ~8,000 | ~25,000 |
| NVIDIA | Chips | ~90,000 | ~300,000 |
| TSMC | Chips | ~35,000 | ~88,000 |
| AMD | Chips | ~9,000 | ~23,000 |
| Broadcom | Chips | ~9,000 | ~33,000 |

Source line: "Sources: Exponential View analysis; company filings. Note: Revenues not subject to deduplication adjustment."

## p.57 — Frontier labs can defend premium pricing, for now

**Left chart — Epoch Capabilities Index** (score at release, OpenAI/Anthropic/open-weight; scatter with trend lines, Jul 23–Jan 26, y-axis 80–160):
- Three upward trend lines: OpenAI (dark purple) and Anthropic (teal) nearly overlapping, from ~112 (mid-2023) to ~155 (early 2026); Open-weight (yellow) lower and parallel, from ~95 to ~152 — open-weight tracks the frontier with a lag. Individual model scores not labeled.

**Right chart — Output price** ($/million output tokens, log scale $0.1–$100+, Jan 23–Jan 26; series: Anthropic (teal), OpenAI (purple), Others (grey)). Labeled points (approx):
- GPT-3 davinci: ~$2 (early 2023)
- GPT-4: ~$60 (early 2023)
- Claude 1: ~$25 (2023)
- GPT-4 Turbo: ~$30 (late 2023)
- Claude 2.1: ~$24 (late 2023)
- Opus 3: ~$75 (early 2024)
- GPT-4o: ~$10 (mid 2024)
- GPT-4.5: ~$150 (early 2025)
- Opus 4.1: ~$75 (2025)
- GPT-5: ~$10; GPT-5.1: ~$10 (2025)
- Opus 4.6: ~$25 (late 2025/26); GPT-5.2: ~$18; GPT-5.4: ~$12; GPT-5.5: ~$30; Opus 4.8: ~$22 (2026)
- Others (grey lines): mostly $0.3–$10 range

Source line: "Sources: Exponential View analysis; Epoch AI."

## p.58 — Labs must outrun open-weight commoditization to hold margin

(conceptual diagram, no numeric data) Schematic: x-axis "Difficulty of capability", y-axis "Value". Model cost curve rises exponentially. Zones left to right: "Lightweight open-weight — Summarize an article"; "Leading open-weight — Draft working code"; "Closed-weight frontier — Multi-day agentic work"; "Beyond the frontier — Tasks beyond current model capabilities" (right of curve, arrow "More capability"); below curve: "Not worth the cost — Value too low to justify current token costs" (arrow "More efficient").

## p.59 — Last year's frontier is commoditizing fast

**Price per capability frontier** — blended price $, grouped by performance at GPQA Diamond (PhD-level science). Y-axis: "Cheapest price to reach the level (3:1 blended, $ / 1M tokens)", log scale $0.10–$100; x-axis 2023–2026. Step-down lines per capability tier, labeled points (approx):
- GPT-4 tier: starts ~$40 (early 2023), steps down; Claude 3 Haiku ~$0.5 (2024); Qwen Turbo ~$0.09 (late 2024)
- Claude 3 Opus tier: starts ~$30 (early 2024); steps down via Claude 3.5 Sonnet (~$6→$2); Phi-4 ~$0.12 (late 2024)
- o1 tier: starts ~$26 (late 2024); DeepSeek-R1 ~$1 (early 2025); GPT-5 nano ~$0.15 (2025)
- o3 tier (dashed): starts ~$17 (2025); ~$3.5 mid-2025; DeepSeek V3.2 ~$0.3 (late 2025)

Annotation: "Labs earn a time-limited premium on the current frontier."

Source line: "Sources: Exponential View analysis; Epoch AI."

## p.60 — Among self-selecting OpenRouter users, token share is moving to open-weight

**Weekly OpenRouter token share** (% per model author; stacked area, Jul 25–Jun 26). Series (bottom to top): google, anthropic, openai, deepseek, tencent, xiaomi, minimax, others.
- Callout: Google + OpenAI + Anthropic combined share falls from 72% (dashed line, ~Jul 25) to 33% (Jun 26).
- Approximate reads: google ~25–30% mid-2025 declining to ~12% by Jun 26; anthropic ~15–20% declining to ~13%; openai ~10–15% declining to ~8%; deepseek/tencent/xiaomi/minimax/others growing to fill remainder.

Source line: "Sources: Exponential View analysis; OpenRouter. Note: While OpenRouter is not a cross-section of the market, its data shows the behavior of self-selecting 'model-routing' users."

## p.61 — Under pricing pressure, labs push into apps and infrastructure

(infographic/screenshot collage, limited numeric data)
- Left: "Today" stack diagram — Consumer surplus (dashed) / Apps / Foundation models / Hosting, with arrows showing labs pushing from Foundation models into Apps and Hosting.
- Box "Building vertical apps: Law": Legora, Clio, Harvey (H logo), Codex for Legal (OpenAI), Claude for Legal (Anthropic).
- Screenshot excerpts: "Anthropic and OpenAI are both launching joint ventures for enterprise AI services" — Anthropic announcement quote: "An engagement might begin with the company's engineering team sitting down with clinicians and IT staff to build tools that fit into the workflows that staff already use… Engagements like this will run across mid-sized companies across industries, each shaped by the people closest to the work."
- OpenAI "Announcing The Stargate Project": intends to invest **$500 billion over the next four years** building new AI infrastructure for OpenAI in the United States; "We will begin deploying **$100 billion immediately**."
- "Anthropic invests **$50 billion** in American AI infrastructure" — building data centers with Fluidstack in Texas and New York, with more sites to come.

Source line: "Sources: Exponential View analysis; TechCrunch; OpenAI; Anthropic."

## p.63 — Text-only quote slide

(no data content — full-page pull quote: "AI demand is more revenue-validated than any prior platform shift. The investment case comes down to whether falling prices can move enough token volume to earn a return on CapEx.")

## p.65 — Authors

(no data content — authors page: Azeem Azhar, Founder; William Gildea, Product Manager; Hannah Petrovic, PhD, Senior Researcher; Nathan Warren, Senior Researcher; Marija Gavrilov, Managing Director. Contacts: aieconomy@exponentialview.co; helen@exponentialview.co)

## p.66 — Follow our analysis on Exponential View

(no data content — promotional page for www.exponentialview.co; screenshots of newsletter "Why AI isn't showing up on your bottom line" and "AI: Boom or Bubble?" dashboard showing gauges as of 22 June 2026: Economic Strain (Capex/GDP) 1.1% caution and worsening; Industry Strain (Investment/Revenue) 7.4 warning but improving; Revenue Momentum (doubling time in years) 0.7 safe and improving; Valuation Heat (Nasdaq 100 P/E) 33.0 caution and worsening; Funding Quality 1.5 caution and worsening; overall gauge "Boom")
