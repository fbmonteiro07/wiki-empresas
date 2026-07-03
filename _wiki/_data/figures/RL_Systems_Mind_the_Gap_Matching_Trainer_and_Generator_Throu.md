# RL Systems Mind the Gap: Matching Trainer and Generator Throughput — figure transcriptions

- Report file: `RL Systems Mind the Gap_ Matching Trainer and Generator Throughput.pdf` (SemiAnalysis)
- Pages covered: 13, 15, 28, 29
- Note: machine transcription of figure/table pages for text-search purposes. Numbers read off charts are approximate where not printed.

## p.13 — Generation-Bound: Generator Output Trails Trainer Demand / LLM Inference Dominates Generation Time

**Chart 1: "Generation-Bound: Generator Output Trails Trainer Demand"** (line chart)
- X-axis: Training Step (0–9). Y-axis: Samples / s.
- Series: Trainer Consumption (orange), Generator Production (blue).
- Trainer Consumption (approx): 2.46, 3.02, 3.03, 3.05, 2.44, 2.34, 3.06, 3.03, 2.34, 2.41 — dotted line "avg 2.75/s".
- Generator Production (approx): 0.55, 1.65, 2.07, 1.94, 1.91, 1.79, 2.13, 2.02, 2.02, 2.21 — dotted line "avg 1.98/s".
- Annotation: "Trainer idle ~30% of wall-clock, 10.5% MFU".
- Printed source: "Source: SemiAnalysis, Company Reports" (in-chart); "Source: SemiAnalysis" (caption).

**Chart 2: "LLM Inference Dominates Generation Time"** (stacked bar chart)
- X-axis: Training Step (0–9). Y-axis: Generation Time per Sample (s).
- Series: LLM Inference (orange, % share labeled), Sandbox (blue, remainder).
- Total heights (approx) and LLM Inference share: step 0 ~405s (88%), 1 ~500s (93%), 2 ~545s (94%), 3 ~555s (96%), 4 ~585s (97%), 5 ~660s (97%), 6 ~630s (98%), 7 ~610s (98%), 8 ~690s (98%), 9 ~660s (98%).
- Printed source: "Source: SemiAnalysis, Company Reports" (in-chart); "Source: SemiAnalysis" (caption).

Page text: section heading "Frequent Tool Use and Easy Task" / "Setup".

## p.15 — LLM Inference Dominates Generation Time and Keeps Growing / Behavior Drift: Longer Responses and More Tool Calls

**Chart 1: "LLM Inference Dominates Generation Time and Keeps Growing"** (stacked bar chart)
- X-axis: Training Step (0–24). Y-axis: Generation Time per Sample (s), 0–2000.
- Series: LLM Inference (orange), Sandbox (blue, thin slice on top).
- Annotation: "LLM inference grows 352s to 1941s (99% of generation)".
- Bar totals (approx, steps 0–24): 370, 525, 505, 750, 820, 1020, 1200, 1310, 1160, 1260, 1020, 1150, 1160, 1160, 1090, 1155, 1210, 1015, 1570, 1335, 1215, 1300, 1300, 1575, 1950.
- Printed source: "Source: SemiAnalysis, Company Reports" (in-chart); "Source: SemiAnalysis" (caption).

**Chart 2: "Behavior Drift: Longer Responses and More Tool Calls"** (bars + line, dual axis)
- X-axis: Training Step (0–24). Left Y-axis: Avg Sequence Length (k tokens), 0–~28. Right Y-axis: Tool Calls per Rollout, 15–50.
- Avg Sequence Length bars (approx k tokens, steps 0–24): 7.3, 10.6, 10.3, 13.7, 16.4, 19.0, 20.7, 21.1, 19.6, 20.2, 16.0, 17.0, 16.8, 18.5, 17.1, 19.1, 20.7, 24.1, 20.5, 18.2, 23.2, 22.7, 22.1, 28.0 (approx; some bars [illegible] precisely).
- Tool Calls per Rollout line (approx): rises from ~15 at step 0 to ~40 by step 6, dips to ~30 at step 10, ~35–38 mid-range, spike to ~49 at step 18, ~35 at step 19, climbs to ~52 by step 24.
- Printed source: "Source: SemiAnalysis, Company Reports" (in-chart); "Source: SemiAnalysis" (caption).

Page text (below charts): "On the capability side, the curriculum is too easy for the model. On average, 55% of problems have a 100% solve rate, i.e., every rollout in the group passes. A rollout group where every rollout has the same reward produces zero advantage and contributes no…"

## p.28 — RL Process (slime) table

Page text (above table): "Looking at our experiment on Qwen3 235B A22B slime, we land ~4.86x higher than Tinker's published $4.86/Mtok target at $16.23/Mtok."

**Table: "RL Process (slime)"**

| Step | Avg Response Length | Avg Sequence Length | Rollout Time (s) |
|---|---|---|---|
| 0 | 11,128 | 19,702 | 593.4 |
| 1 | 13,227 | 21,473 | 479.2 |
| 2 | 10,946 | 19,777 | 518.9 |
| 3 | 12,691 | 20,357 | 479.2 |
| 4 | 13,644 | 20,628 | 426.4 |
| 5 | 12,185 | 21,004 | 522.1 |
| 6 | 12,766 | 20,257 | 555.3 |
| 7 | 12,718 | 21,383 | 523.7 |
| 8 | 11,203 | 19,127 | 374.4 |
| 9 | 10,451 | 17,228 | 527.1 |
| 10 | 12,896 | 19,333 | 455.4 |
| 11 | 11,696 | 19,603 | 457.8 |
| 12 | 10,273 | 19,183 | 433.1 |
| 13 | 13,168 | 20,730 | 513.4 |
| 14 | 12,864 | 21,939 | 481.5 |
| 15 | 12,852 | 20,193 | 423.5 |
| 16 | 11,590 | 18,860 | 620.7 |
| 17 | 13,847 | 21,686 | 508.9 |
| 18 | 11,630 | 19,900 | 496.1 |
| 19 | 12,856 | 20,922 | 454.4 |
| **Steady Average** | **12,232** | **20,164** | **492.2** |

Printed source: "Source: SemiAnalysis".

## p.29 — Tinker TCO table / RL Process (Prime RL) table

**Table 1: "Tinker TCO"**

| Step | Prefill cost | Decode cost | Train cost | Total cost | Total cost per Mtok |
|---|---|---|---|---|---|
| 0 | $0.37 | $1.21 | $2.57 | $4.16 | $3.30 |
| 1 | $0.36 | $1.44 | $2.80 | $4.60 | $3.35 |
| 2 | $0.38 | $1.19 | $2.58 | $4.16 | $3.28 |
| 3 | $0.33 | $1.38 | $2.66 | $4.37 | $3.36 |
| 4 | $0.30 | $1.48 | $2.69 | $4.48 | $3.39 |
| 5 | $0.38 | $1.33 | $2.74 | $4.45 | $3.31 |
| 6 | $0.33 | $1.39 | $2.64 | $4.36 | $3.36 |
| 7 | $0.38 | $1.38 | $2.79 | $4.55 | $3.33 |
| 8 | $0.34 | $1.22 | $2.50 | $4.06 | $3.32 |
| 9 | $0.29 | $1.14 | $2.25 | $3.68 | $3.34 |
| 10 | $0.28 | $1.40 | $2.52 | $4.21 | $3.40 |
| 11 | $0.34 | $1.27 | $2.56 | $4.18 | $3.33 |
| 12 | $0.39 | $1.12 | $2.50 | $4.01 | $3.27 |
| 13 | $0.33 | $1.43 | $2.71 | $4.47 | $3.37 |
| 14 | $0.39 | $1.40 | $2.86 | $4.66 | $3.32 |
| 15 | $0.32 | $1.40 | $2.64 | $4.35 | $3.37 |
| 16 | $0.32 | $1.26 | $2.46 | $4.04 | $3.35 |
| 17 | $0.34 | $1.51 | $2.83 | $4.68 | $3.37 |
| 18 | $0.36 | $1.27 | $2.60 | $4.22 | $3.32 |
| 19 | $0.35 | $1.40 | $2.73 | $4.48 | $3.35 |
| **Steady Average** | **$0.35** | **$1.33** | **$2.63** | **$4.31** | **$3.34** |

Printed source: "Source: SemiAnalysis".

Page text (between tables): "For our experiment on Qwen3 235B A22B Prime RL, we landed at ~2.01x higher than Tinker's published $3.43/Mtok target at $6.90/Mtok."

**Table 2: "RL Process (Prime RL)"**

| Step | Avg Prompt Length | Avg Response Length | Avg Sequence Length | Rollout Time (s) |
|---|---|---|---|---|
| 0 | 3,629 | 10,203 | 13,833 | 371 |
| 1 | 5,141 | 11,898 | 17,039 | 479 |
| 2 | 5,689 | 12,317 | 18,006 | 529 |
| 3 | 5,118 | 13,042 | 18,160 | 544 |
| 4 | 5,394 | 13,360 | 18,755 | 587 |
| 5 | 6,904 | 12,851 | 19,755 | 656 |
| 6 | 5,897 | 13,116 | 19,013 | 632 |
| 7 | 5,272 | 13,418 | 18,691 | 608 |
| 8 | 6,892 | 13,569 | 20,461 | 688 |
| 9 | 5,971 | 13,262 | 19,233 | 663 |
| **Steady Average** | **5,591** | **12,704** | **18,294** | **576** |

Printed source: "Source: SemiAnalysis".
