# Reconciliation — /run-inbox 2026-10-25 (scheduled 23h, unattended)

Two sources were processed. Both are podcast/panel commentary, not broker research, so neither carries a rating, a PT or a published estimate:
- **CASPA 2026 CEO Summit, "Semiconductor Industry Outlook Panel"**, 2026-10-24. Stacy Rasgon (Bernstein, speaking as an analyst; this is not a published Bernstein note) and Dylan Patel (SemiAnalysis, who sells research to the same buyers). Moderator: Austin Lyons (Chipstrat). YouTube machine transcript without speaker labels.
- **The a16z Show, "The New Startup Playbook | Box CEO Aaron Levie"**, 2026-10-25. Qualitative; the only sizing in it is loose private-market "market cap".

**BBG: RESOLVED 2026-10-26** against the fresh `estimates.json` (asof 2026-10-26); the BBG cells below now cite that snapshot. Original ingest note: **BBG: PENDING (live).** `bdp` could not connect (localhost:8194 refused, so the Terminal is not running or not logged in). Per the standing rule, no web data was substituted. The on-disk snapshot `estimates.json` (asof **2026-10-23**, two days old) is used as the consensus baseline below. **House:** NVDA `house.json` gives EPS 2026 $9.26 and 2027 $15.44. No house model exists for LRCX or AVGO, and the private names have none.

## Where the new data DIVERGES

| Ticker / theme | Metric | New datapoint | Baseline (prior wiki / house / BBG) | Gap | Note |
|---|---|---|---|---|---|
| NVDA | Next-year earnings growth | **Patel: earnings "still… doubling year-on-year… next year… or more"** [00:35:13] | BBG 10-26 (resolved): 2FY EPS median $15.89 vs 1FY $9.37, i.e. **+70%**; 2FY street-high `eps_hi` **$18.75 = +100%**. House: 2027 $15.44 vs 2026 $9.26, i.e. **+67%** | "Doubling" is ~30pp above the median and the house, and sits exactly AT the BBG street high | A loose verbal claim; "earnings" is undefined. If he means EPS, he is at the top of the Street range, well above the median and the house. Worth asking SemiAnalysis what its own NVDA model carries. |
| NVDA | Neocloud backstop price | **Patel: guaranteed "$3.50"** (unit and chip not stated), 50% revenue share above it for Firmus / Sharon AI [00:09:04] | NVDA page AICP block: **~$2.35/hr/GPU** GB300 six-year average (vs $4.50-4.60 for 5-year market contracts) | +$1.15 if both are $/GPU-hr | Basis is unknown (chip generation, tenor). Do not net. The **50%** share is the first number on this page; Jensen on BG2 (10-15) named revshare without a %. |
| ANTHROPIC / `rev-per-gw` (lab basis) | Lab monetisation per GW | **Patel: "on the order of 70 to 80 billion a gigawatt off of their inference capacity"**, citing unnamed "recent disclosures" [00:23:33] | Lab-basis marks in assumptions: Hock Tan **~$30bn/GW** (09-02); Baker/a16z ~$60-100bn (08-28); ~$10bn "today" (low mark) | **>2x** the supplier's own mark | NOT adopted. The disclosure is unnamed, and inference-only vs total GW and ARR vs run-rate are not stated. Never chain with rental or build bases. |
| ai-datacenter-power / `rev-per-gw` (build basis) | All-in build cost per GW | **Patel: ~$40bn (2024) → "north of 60" now**; ex chip-designer margin "like $20 billion" [00:22:29, 00:30:23] | Wiki build basis **~$50bn/GW** NVDA-GPU infra; NVDA's own reference (relayed by Rasgon) $25bn Blackwell / **$40bn Rubin** (chip content) | +$10bn+ vs the wiki's all-in basis | Consistent with the memory/substrate inflation he describes. The $40bn Rubin figure is a chip-content basis, a different thing. |
| ai-compute-deals / META | Hyperscaler commitments | **Patel: "Meta has $1.4 trillion dollars of commitments"** [00:09:46] | Meta 3Q26 10-Q aggregates on the page: non-cancelable **$454.5bn** + uncommenced leases **$355.7bn** ≈ **$810bn** | ~$590bn unexplained | Not adopted. Patel may be including off-filing or announced-not-signed items. Treat as his number. |
| ai-compute-deals / ANTH-LAMBDA-20260831 | Deal term | **Patel: Lambda gave NVIDIA a "10% revenue share"** to build the Anthropic cluster [00:09:04] | ID carries $35B, a Hut 8 site, NVIDIA holding the lease and Lambda operating; **unconfirmed by Lambda** | New term | A single verbal claim. It confirms neither the deal nor the term. |

## CONFIRMS (no action)

| Ticker / theme | Metric | New datapoint | Baseline | Verdict |
|---|---|---|---|---|
| LRCX / semicap-wfe | CY26 / CY27 WFE | Rasgon: CY26 "120 maybe" at the start of the year → "probably end the year 155"; >$200bn 2027 is close to the ceiling ("we don't have the fabs") | Lam F1Q27 (10-21): CY26 "mid $150 billion", CY27 ">$200 billion"; Bernstein published $204bn (08-11) is the lowest broker mark on the page | ✓ Rasgon stays the low-end voice. No new number. |
| NVDA | Customer mix | Rasgon: hyperscale vs non-hyperscale "about 50/50"; labs "roughly 20% of the revenue" | Jensen on BG2 (10-15): labs "not quite one-third of our business… a quarter of our compute" | ✓ Roughly consistent (revenue vs compute bases). |
| NVDA | Growth guide | Rasgon relays "at least 70%" as a constrained guide | BBG 10-26 (resolved): 2FY revenue $702.7bn vs 1FY $411.1bn = **+71%** (unchanged vs the 10-23 snapshot) | ✓ |
| NVDA / AVGO | Multiples | Patel: "lowest multiples basically ever"; Rasgon: in his note ~9 months ago only 13 days in 10 years had NVDA cheaper vs the semis group, and "that's cheaper today" | BBG 10-26 (resolved): NVDA $217.33 / 2FY EPS $15.89 = **13.7x**; AVGO $330.64 / $19.27 = **17.2x** (10-23 snapshot read 13.3x / 16.7x) | ✓ Direction consistent (matches the BG2 host's "13 to 14 times"). The relative-to-SOX series is not on disk. |
| NVDA / cowos-packaging | CoWoS / HBM share | Patel: NVDA's unit share fell in 2026 and falls again in 2027 | JPM ASIC unit-share inflection (custom-asic-tpu) | ✓ Direction. 🔭 vs Jensen's "our market share is actually increasing" (management). |
| ai-datacenter-power | 2027 global DC GW | Patel: "nearly 50 GW" (~35 US, 7-8 China) | SemiAnalysis Ep. 039 (10-20) carried the same report; canonical `ai-dc-power-gw` is unchanged | ✓ A restatement of SemiAnalysis' own number, not a second source. Basis not stated. |
| hbm-memory | HBM trade ratio | Rasgon: "three or four times as many wafers" per GB vs DDR5 | Page canon | ✓ |
| hbm-memory / macro-cycle | Industry size | Rasgon: ~$1.5tn 2026, "up probably 100%", 70-80% of growth memory ASPs, units ~+10% | Not on the wiki in this form | 🆕 Logged as a spoken estimate. He says memory is a colleague's coverage. No baseline to reconcile against. |
| cowos-packaging / TSM | TSMC GM path | Patel: "45%… to now 60" over the decade | TSM page history | ✓ |
| AVGO | Anthropic chip lease | Patel: "rent to own… stretching out the payments over a few years" | FT 10-12 chip-lease entry | ✓ No new terms. |
| tokenmaxxing | Agent leverage / Jevons | Levie: 10-20% → 3-10x productivity; agent at $5-10/hr vs $1,000-2,000/hr legal review | Jassy (10-23) and Horowitz (10-24) Jevons framing | ✓ Qualitative. Levie's "couple hundred billion" of AI-coding market cap is private-valuation talk, not reconciled. |

## Follow-ups
- ~~Re-run the NVDA, AVGO and LRCX consensus once the Terminal is logged in (`/wiki-consensus`).~~ Done 2026-10-26: NVDA 1FY/2FY EPS $9.37/$15.89 and revenue $411.1bn/$702.7bn are unchanged over the weekend; AVGO 2FY EPS $19.27 unchanged; LRCX 1FY/2FY EPS $9.68/$12.14. No row changed section.
- The Patel "earnings doubling" claim is the one place tonight where an outside voice is materially above the Street median and the house (it matches the BBG 2FY street high, $18.75). Ask SemiAnalysis for its model basis before acting on it.

_BBG column resolved 2026-10-26 — estimates.json asof 2026-10-26._
