# Bernstein on Gen AI Software.pdf — figure-page transcription

- Report: "Bernstein on Gen AI Software.pdf" (Bernstein | Societe Generale Group, "Scaling Intelligence: The Generative AI Handbook"; distribution stamp "For the exclusive use of FELIPE MONTEIRO at CAPSTONE PARTNERS GESTAO DE RECURSOS LTDA on 24-Jun-2026")
- Pages covered by this file: 2, 4, 6, 113, 114, 115, 116, 132, 146, 154, 194
- Note: machine transcription of rendered figure-page images so chart/table data is text-searchable. Several pages rendered blank in the image extraction (only header/footer visible).

## p.2 — (no data content)
(no data content — page renders blank; only the distribution stamp is visible.)

## p.4 — (no data content)
(no data content — page renders blank; only Bernstein | Societe Generale Group masthead and footer "2 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)

## p.6 — Bernstein Ticker Table

Prices as of 16 Jun 2026. TTM Rel. Perf. column.

| Ticker | Rating | Cur | Closing Price (16 Jun 2026) | Price Target | TTM Rel. Perf. | Cur | Adj EPS 2026A | Adj EPS 2027E | Adj EPS 2028E | Adj P/E 2026A | Adj P/E 2027E | Adj P/E 2028E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ADBE (Adobe) | O | USD | 207.32 | 379.00 | (72.9)% | USD | 20.95 | 24.99 | 29.15 | 9.9 | 8.3 | 7.1 |
| HUBS (HubSpot) | O | USD | 182.85 | 381.00 | (91.2)% | USD | 9.70 | 13.16 | 15.79 | 2.5 | 2.1 | 1.8 |
| MSFT (Microsoft) | O | USD | 393.83 | 646.00 | (42.3)% | USD | 13.64 | 16.85 | 19.16 | 28.9 | 23.4 | 20.6 |
| MDB (MongoDB) | O | USD | 348.81 | 449.00 | 47.8% | USD | 2,464 | 3,035 | 3,626 | 10.4 | 8.5 | 7.1 |
| ORCL (Oracle) | O | USD | 188.33 | 325.00 | (35.3)% | USD | 7.63 | 8.57 | 12.86 | 24.7 | 22.0 | 14.6 |
| CRM (Salesforce.com) | U | USD | 161.71 | 173.00 | (63.2)% | USD | 12.52 | 14.53 | 15.60 | 12.9 | 11.1 | 10.4 |
| SAP (SAP) | O | USD | 165.41 | 323.00 | (68.6)% | EUR | 6.10 | 7.54 | 9.02 | 23.3 | 18.9 | 15.8 |
| SNOW (Snowflake) | M | USD | 238.32 | 250.00 | (10.5)% | USD | 4,684 | 6,228 | 7,927 | 17.6 | 13.2 | 10.4 |
| WDAY (Workday) | O | USD | 126.77 | 216.00 | (72.9)% | USD | 9.23 | 11.15 | 13.95 | 13.7 | 11.4 | 9.1 |
| SPX | | | 7,511.35 | | | | | | | | | |

Footnotes: O - Outperform, M - Market-Perform, U - Underperform, NR - Not Rated, CS - Coverage Suspended. MDB, SNOW estimate is Revenues (M); HUBS, MDB, SNOW valuation is EV/Sales (x); ADBE, HUBS, MSFT, SAP base year is 2025.
Source: Bloomberg, Bernstein estimates and analysis.

## p.113 — Exhibit 17: Truncated example of Anthropic's skills file (for earnings update) (1/2)

Screenshot of a skill definition file. Table at top:

| name | description |
|---|---|
| earnings-analysis | Create professional equity research earnings update reports (8-12 pages, 3,000-5,000 words) analyzing quarterly results for companies already under coverage. Fast-turnaround format focusing on beat/miss analysis, key metrics, updated estimates, and revised thesis. Includes 1-3 summary tables and 8-12 charts. Use when user requests "earnings update", "quarterly update", "earnings analysis", "Q1/Q2/Q3/Q4 results", or post-earnings report. |

Body: "Equity Research Earnings Update" — create professional EARNINGS UPDATE REPORTS following institutional standards (JPMorgan, Goldman Sachs, Morgan Stanley format). Key characteristics: Length 8-12 pages; Word count 3,000-5,000 words; Tables 1-3 summary (NOT comprehensive); Figures 8-12 charts; Turnaround 1-2 days (within 24-48 hours of earnings); Audience: clients already familiar with the company; Focus: what's NEW — beat/miss, updated estimates, thesis impact; Font: Times New Roman throughout (unless user specifies otherwise). "When to Use": user requests "Create an earnings update for [Company] Q3 2024", "Analyze [Company]'s quarterly results", "Post-earnings report for [Company]", "Q1/Q2/Q3/Q4 update for [Company]". Do NOT use if: user requests "initiation report" → use different skill; user requests "flash note" or "quick take" → different format.
Source: GitHub, Anthropic

## p.114 — Exhibit 18: Truncated example of Anthropic's skills file (for earnings update) (2/2)

"High-Level Workflow" — the earnings update process follows 5 phases (three shown).
- Phase 1: Data Collection (30-60 minutes). "CRITICAL: TRAINING DATA IS OUTDATED". Before starting, 4 steps in order: 1. Check today's date; 2. Search for latest ("[Company] latest earnings results"); 3. Verify the earnings release is within last 3 months; 4. Check transcript date matches release date. Common mistake: using outdated earnings calls from training data instead of searching for the latest. Requirements checklist: search for latest earnings (do NOT rely on training data); write down today's date and the release date found; verify release date within 3 months of today; verify transcript date matches release date; if dates don't match or are old (>3 months), search again. See references/workflow.md.
- Phase 2: Analysis (2-3 hours): beat/miss analysis for each key metric; segment/geographic/product breakdown; margin and guidance analysis; update financial model and estimates.
- Phase 3: Chart Generation (1-2 hours): create 8-12 charts focusing on quarterly trends and what's new — quarterly revenue progression, quarterly EPS progression.
Source: GitHub, Anthropic

## p.115 — Exhibit 19: System prompts should stay high level, but relevant enough

Infographic "Calibrating the system prompt" (Anthropic graphic) — a spectrum from "Too specific" (left, red) through "Just right" (center, green) to "Too vague" (right, red), each with an example customer-support system prompt for "Claude's Bakery":
- Too specific: highly procedural prompt enumerating exact intents ("incident_resolution", "general_inquiry", "order_resubmission", "account_maintenance", "requires_escalation"), exhaustive case lists and step-by-step conditional procedures [partially illegible fine print].
- Just right: "You are a customer support agent for Claude's Bakery… Use the tools available to you to resolve the issue efficiently and professionally." Access to order management systems, product catalogs, store policies. Response framework: 1. Identify the core issue; 2. Gather necessary context (tools to verify order details, check inventory, review policies); 3. Provide clear resolution with concrete next steps and realistic timelines; 4. Confirm satisfaction. Guidelines: choose the simplest solution; check order status before suggesting next steps; when uncertain call the human_assistance tool; for legal/health/allergy emergencies or financial adjustments beyond standard policy, call the human_assistance tool; acknowledge frustration/urgency and respond with appropriate empathy.
- Too vague: "You are a bakery assistant; you should attempt to solve customers' issues in a manner consistent with the principles and essence of the company brand. Escalate to a human if needed."
Source: Anthropic

## p.116 — (no data content)
(no data content — page renders blank; only footer "114 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)

## p.132 — (no data content)
(no data content — page renders blank; only footer "130 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)

## p.146 — (no data content)
(no data content — page renders blank; only footer "144 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)

## p.154 — (no data content)
(no data content — page renders blank; only footer "152 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)

## p.194 — (no data content)
(no data content — page renders blank; only footer "192 — SCALING INTELLIGENCE: THE GENERATIVE AI HANDBOOK". Body content did not render in the image.)
