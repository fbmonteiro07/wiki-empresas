# Reconciliation — /run-inbox 2026-10-16

_Generated 2026-10-16 (scheduled 23h /run-inbox). Baselines: (1) prior wiki comments, (2) Capstone house models (`## Capstone estimates` blocks / `_data/house.json`), (3) BBG consensus — **LIVE** `bdp` pull at run time (Terminal up; on-disk `estimates.json` asof 2026-10-16 agrees)._

Sources this run: Jefferies "OCP Takeaways - Optical Innovation Accelerating" (Curtis et al., 2026-10-16) · SemiAnalysis "ASML Is Building a Hybrid Bonding Tool!" (Zhang/Wong/Lee/Patel, 2026-10-15) · Jefferies FI trading desk "A Survival Guide to Datacenter Credit" (Haber, 2026-09-14) · Capstone "Checks de cloud" compilation (2026-10-15, derived) · MS + Nomura TSMC post-3Q26 notes (2026-10-15; estimates logged on TSM.md by the 10-16 interactive session, first reconciled here).

Qualitative-only sources (no PT/EPS): SemiAnalysis (no ratings/PTs by construction), Jefferies OCP (no PTs printed; roster dollar figures are closing prices, not PTs — see `jefferies-roster-price-not-pt`).

## DIVERGES (the alpha)

| Ticker | New datapoint (source, date) | Baseline | Gap | Read |
|---|---|---|---|---|
| TSM | 2026E EPS: MS NT$112.10, Nomura NT$111.06 (2026-10-15) | **House NT$102.5** (Capstone model 2026-06-10); BBG 1FY NT$109.79 | House −8% vs both notes, −7% vs BBG | House model predates the 2Q and 3Q26 beats — stale, not a view. Roll the model (2026 is now 3/4 reported). |
| TSM | 2027E EPS: MS NT$148.64, Nomura NT$149.77 | House NT$143.5; BBG 2FY NT$144.96 | House −3.5/−4.2% vs the notes; notes +2.5/+3.3% above BBG | Street-high direction post-print; house sits at/below consensus. |
| TSM | PT: MS NT$3,088 (OW, unch., 20x 2027E); Nomura NT$3,615 → **3,745** (Buy, 25x 2027F) | BBG target NT$3,393.2; px NT$2,420 | MS −9% / Nomura +10% vs consensus target | Same EPS (~149), the whole spread is the multiple (20x vs 25x). MS's OW PT below the consensus target = rating/PT tension worth noting. |
| CRWV | Jefferies desk prints CoreWeave's own debt yield at ~11.2% (p.13) and 12.2% (p.14) in the same note (2026-09-14) | Workbook (`credit_workbook.json`, live 10-16) | ~100bp internal inconsistency | Don't cite a single Jefferies CRWV yield; use the official workbook. Every CRWV-leased project bond (APLD/ELNFOR/CORZ/ELKGVP/EDGCOM/GALAXY, 7.6–10.3% YTW) yields LESS than CoreWeave itself — the market prices the SPV/Meta-reassignment structure, not the tenant. |
| CRWV | Capstone compilation says UBS's "Customer 3" (global bank) moved TO CoreWeave | UBS primary (2026-09-22, pp.41-42): the bank did move to CoreWeave in mid-2025, then LEFT for its own data centers | Compilation omits the exit | Omission, not an inversion (verifier re-read the primary) — the churn-to-on-prem is the datapoint; primary quoted on the CRWV row. |
| DC project bonds | Jefferies 9/14 YTW/STW comp table (24 bonds) | Workbook live YTM/OAS 10/16 (Barclays 15-Sep YTW) | Every bond yields more on 10/16 than at Jefferies' 9/14 mark (YTW≠YTM — approximate) | One-month widening across the comp set; bases not netted (see ai-compute-deals.md). |

## CONFIRMS (no action)

| Ticker | New datapoint | Baseline | Read |
|---|---|---|---|
| TSM | 2028E EPS MS 189.81 / Nomura 189.61 | BBG 3FY NT$183.39; prior wiki median ~NT$190.6 (6 houses) | +3.4% vs BBG, in line with the post-print median already on the page. |
| LITE | Jefferies holds **80M 1.6T units C27** "despite concerns of tightness at 3nm" (2026-10-16) | Jefferies 09-24 model "80M+ 1.6T" (LITE.md) | Restatement, not a raise. BBG PT US$1,170.6 vs px US$824 — no broker PT to place. |
| NVDA | MaxLPS "up to 40% more Rubin GPU capacity" (company claim relayed by Jefferies) | Already on NVDA.md as a company claim, not adopted | Jefferies adds only the "meaningful potential offset" framing. |
| BESI / ASML | SemiAnalysis: ASML D2W hybrid bonder, volume ≥2030; BESI 2026-29 logic order book impact "muted"; HBM HB ≤20% of BESI 2028 consensus revenue (SA estimate) | BESI.md debate (Redburn 09-23 ~90% logic share); BBG BESI target €266 vs px €155.6 | No near-term estimate change; a 2030+ terminal-share bear. SA estimate not netted vs Redburn's bonder count (different bases). |
| CRDO / ALAB / NVTS | OCP product datapoints (ALC 1.6T 50m C27; Aries 7 optical drivers; NVTS 24kW 800V board) | BBG targets CRDO $280 (px $170), ALAB $424 (px $286), NVTS $14.6 (px $8.3) | Qualitative; nothing to reconcile numerically. |
| MSFT/AMZN/GOOG/ORCL/CRWV/NBIS/ANTHROPIC/OPENAI | Cloud-checks compilation marks (Archera 10-08 call, UBS Evidence Lab, MS AlphaWise, FundaAI) | Most already on pages from their primaries | Derived artifact — only missing items added, attributed to the original source; expert/survey marks have no house/BBG baseline. |

## Follow-ups
- Roll the TSM house model (2026E NT$102.5 is pre-2Q/3Q beat).
- Barclays TSMC note (OW, PT US$665) still queued in `_inbox/PENDING_FULL_REPORTS.md` — needs Barclays Live login.
- Three P: files stranded (locked) this run: Barclays IG/HY DC credit digest Sep-2026, Barclays HY CoreWeave "In the Eye of the AI Storm", Redburn Research.pdf — next run.
