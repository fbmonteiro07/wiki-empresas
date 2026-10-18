# Reconciliation — /run-inbox 2026-10-17

_Generated 2026-10-17 (scheduled 23h /run-inbox, unattended). Baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus — **live `bdp` FAILED (blpapi: Terminal not running / logged out)**, so the BBG column uses the **on-disk snapshot `_data/estimates.json`, asof 2026-10-16** (one day old — a valid baseline; no web data substituted). Live-only fields (bond yields, CDS) are marked PENDING._

Sources this run: Barclays US HY Credit "CoreWeave (CRWV) In the Eye of the AI Storm – Maintain OW" (Harlib/Mulherin, 2026-10-15) · Rothschild & Co Redburn "Digital Infrastructure: Can't Buy the Frontier" (Haissl/Han, 2026-10-15) · Barclays FICC/Credit "Data Center Credit Digest – September 2026" (Harlib/Keches/Mulherin/Neuhaus, 2026-09-16, Sept vintage) · Goldman Sachs Credit Strategy "Global Credit Trader: AI, Credit, and a Higher Cost of Capital" (Lynam/Grut/Ali, 2026-10-15).

## DIVERGES (the alpha)

| Ticker | New datapoint (source, date) | Baseline | Gap | Read |
|---|---|---|---|---|
| CRWV | Barclays HY base case 2027E revenue **$28.27bn**, adj. EBITDA **$18.22bn** (2026-10-15) | House CY27 rev $26.70bn / EBITDA $16.55bn; BBG CY2027 rev $26.47bn / EBITDA $16.66bn | Rev +5.9% vs house, +6.8% vs BBG; EBITDA +10% vs house, +9.4% vs BBG | A CREDIT desk sits above both house and Street on 2027 — the bond OW is built on numbers the equity consensus doesn't carry. Watch whether the 3Q print (and the ~$40mn/MW + SpaceX $50-53mn/MW short-dated tiers) pulls 2027 up. |
| CRWV | Barclays HY 2030E revenue **$77.09bn**, active power ~**6.97GW**, capex $51.2bn | House CY30 rev $87.42bn, 8.0GW YE power, capex $74.9bn | Rev −12% vs house; −1GW of power | The inverse of the 2027 gap: Barclays models less out-year build than the house (and the company's >8GW). Out-year house revenue is the more aggressive mark. |
| CRWV | Barclays: 5y CDS **1,100/1,160 (1,130bp mid)**, 49.9% implied 5y PD (2026-10-15) | Bloomberg CRWV CDS USD SR 5Y D14 **482bp** (10-15, page) | ~650bp | Still two different contracts/quotes — unreconciled since 10-14. BBG live re-check **PENDING** (Terminal down). Do not cite one as "the" CDS. |
| CRWV | Barclays EUR 8.5% 2032 **€70.88 / 16.53% YTW** (mid-day 10-15) | Bloomberg via credit monitor 14.46% (10-14) | ~200bp | Largest single-tranche gap; partly timing/measure (YTW vs YTM). Live check **PENDING**. |
| CRWV / NBIS / ORCL | Redburn Sell PTs **$54 / $84 / $110** reiterated (2026-10-15) | BBG cons PT $137.35 / $287.95 / $240.01; px (10-16) $61.39 / $165.47 / $128.23 | PT −61% / −71% / −54% vs consensus; vs price −12% / −49% / −14% | Unchanged targets, but CRWV is now only ~12% above Redburn's $54 after the sell-off — the bear target is close to being reached on the credit tape alone. |
| Hyperscaler debt | GS: **$420bn** of direct hyperscaler issuance forecast for 2027 (2026-10-15) | BofA path on hyperscaler-capex: $215bn for 2027 | ~2x | Perimeter differs (GS five names incl. ORCL) but ORCL can't explain ~$200bn. The debt-funded share of 2027 capex is a live disagreement between houses. |
| WULF (no page) | Barclays Digest: CB-5 pushed to **1Q27 from 4Q26** (2026-09-16) | MS "on schedule" read on ai-datacenter-power | Schedule conflict | Both kept. Sept vintage; check TeraWulf's 3Q update. Relevant to GOOG (Fluidstack backstop) only at the margin. |
| Reflection / SpaceX | Redburn: c72MW at an ASSUMED $25m/MW/yr | SPCX page: JPM/podcast ~$50m/MW | 72MW vs ~36MW | Assumption-driven; the MW in the new REFL-SPCX-2026 row is labelled as Redburn's estimate. |

## CONFIRMS (no action)

| Ticker | New datapoint | Baseline | Read |
|---|---|---|---|
| CRWV | Barclays HY 3Q26E revenue **$3,581m** | BBG 1FQ $3,553m; guide $3.45-3.60bn | +0.8% vs consensus, top of guide. |
| CRWV | Barclays HY 2026E revenue $13.05bn / EBITDA $7.80bn / capex $37.99bn | House $12.80 / 7.36 / 37.0bn; BBG CY26 $12.77 / 7.48 / 35.67bn | +2% rev; within the FY guide ($12.4-13.2bn); capex +6.5% vs BBG but within the $35-39bn guide. |
| CRWV | Barclays 2Q26 liquidity $16.9bn | DB/house map $15.55bn | Basis only — Barclays includes ~$1.4bn restricted cash. |
| CRWV | Barclays backlog ~$129bn ($104.2bn + ~$25bn early 3Q) | Jefferies 3Q RPO bogey >$130B (page, 10-14) | Same arithmetic. |
| CRWV | Barclays "$10.3bn of converts in four quarters" | 8-K: September convert closed at **$4.2bn** (page, 10-16) | Barclays uses the $3.7bn pre-option vintage; the 8-K figure stands. |
| NVDA | Redburn Buy **TP $325** unchanged | BBG cons PT $325.66 | In line with consensus. |
| NVDA | Barclays Digest: Beacon Point ~$19.6bn base-term value ≈ the ~$20bn lease-assignment disclosure | NVDA.md ~$20bn + "credit substitution" framing | Corroborates; adds the bond-covenant angle. |
| Project finance | GS **$300bn** 2027 global project-finance forecast | GS 08-03 podcast $300bn (hyperscaler-capex) | Reiterated; now "firmly skewed to the upside". |
| IG supply | GS FY26 USD IG gross supply **$2,300bn** ($1,904bn YTD) | GS July $2.1tn (ai-datacenter-power) | Superseded by the same house — supersession marker added on the page. |
| DC bonds | GS avg HY DC bond price $101.5 (Jun 30) → $94.7 (Oct 14) | Jefferies 9/14 comp table + workbook live 10/16 widening (10-16 reconciliation) | Same direction, third source. |

## Follow-ups
- **0-byte drop:** `10.16.2026_CoreWeave (Buy) Credit markets under pressure, but fundamentals remain supportive.pdf` arrived empty on P: — ask for a re-drop.
- BBG Terminal down: re-run `/wiki-consensus` to resolve the PENDING CDS / EUR-2032 yield checks.
- NBIS.md 07-20 FinTwit row says the $1.1bn Reflection deal was with META — Redburn and the page's own history say Nebius. Flagged in-line, not rewritten.
- CRWV.md Risks still cites "$25.1B principal debt" (Q1 vintage); Barclays/house use $35.55bn at 2Q26 — stale line.
- Barclays TSMC note (OW, PT US$665) still queued in `_inbox/PENDING_FULL_REPORTS.md`.
