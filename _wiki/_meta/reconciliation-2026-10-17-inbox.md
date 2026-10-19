# Reconciliation — /run-inbox 2026-10-17

_Generated 2026-10-17 (scheduled 23h /run-inbox, unattended). Baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus — **live `bdp` FAILED (blpapi: Terminal not running / logged out)**, so the BBG column uses the **on-disk snapshot `_data/estimates.json`, asof 2026-10-16** (one day old — a valid baseline; no web data substituted). Live-only fields (bond yields, CDS) are marked PENDING._

Sources this run: Barclays US HY Credit "CoreWeave (CRWV) In the Eye of the AI Storm – Maintain OW" (Harlib/Mulherin, 2026-10-15) · Rothschild & Co Redburn "Digital Infrastructure: Can't Buy the Frontier" (Haissl/Han, 2026-10-15) · Barclays FICC/Credit "Data Center Credit Digest – September 2026" (Harlib/Keches/Mulherin/Neuhaus, 2026-09-16, Sept vintage) · Goldman Sachs Credit Strategy "Global Credit Trader: AI, Credit, and a Higher Cost of Capital" (Lynam/Grut/Ali, 2026-10-15).

## Where the new data DIVERGES

| Ticker | New datapoint (source, date) | Baseline | Gap | Read |
|---|---|---|---|---|
| CRWV | Barclays HY base case 2027E revenue **$28.27bn**, adj. EBITDA **$18.22bn** (2026-10-15) | House CY27 rev $26.70bn / EBITDA $16.55bn; BBG CY2027 rev $26.47bn / EBITDA $16.66bn | Rev +5.9% vs house, +6.8% vs BBG; EBITDA +10% vs house, +9.4% vs BBG | A CREDIT desk sits above both house and Street on 2027 — the bond OW is built on numbers the equity consensus doesn't carry. Watch whether the 3Q print (and the ~$40mn/MW + SpaceX $50-53mn/MW short-dated tiers) pulls 2027 up. |
| CRWV | Barclays HY 2030E revenue **$77.09bn**, active power ~**6.97GW**, capex $51.2bn | House CY30 rev $87.42bn, 8.0GW YE power, capex $74.9bn | Rev −12% vs house; −1GW of power | The inverse of the 2027 gap: Barclays models less out-year build than the house (and the company's >8GW). Out-year house revenue is the more aggressive mark. |
| CRWV | Barclays EUR 8.5% 2032 **€70.88 / 16.53% YTW** (mid-day 10-15) | BBG `XS3333139288 Corp` YLD_YTM_MID: 10-14 **14.46%**, 10-15 close **14.07%**, 10-16 14.15%, live 2026-10-19 **14.02%** (YAS_BOND_YLD 14.51%, PX_MID **€78.68**) | **~250bp** vs the same-day 10-15 close; ~8 pts on price | **Resolved 2026-10-19 (live bdp; was PENDING) — the gap is real and holds on the same date.** Barclays' print is an intraday desk mark at the 10-15 trough; BBG's composite never closed above 14.46% (10-14) and has the bond ~8 points higher today. Carry 16.53% / €70.88 as the panic-low marker, not as the series; the BBG 14.0-14.5% composite is the mark to track, and the USD 9.625% 2032 sits at 14.59% / $81.07 live. |
| CRWV / NBIS / ORCL | Redburn Sell PTs **$54 / $84 / $110** reiterated (2026-10-15) | BBG cons PT $137.35 / $287.95 / $240.01; px (10-16) $61.39 / $165.47 / $128.23 | PT −61% / −71% / −54% vs consensus; vs price −12% / −49% / −14% | Unchanged targets, but CRWV is now only ~12% above Redburn's $54 after the sell-off — the bear target is close to being reached on the credit tape alone. |
| Hyperscaler debt | GS: **$420bn** of direct hyperscaler issuance forecast for 2027 (2026-10-15) | BofA path on hyperscaler-capex: $215bn for 2027 | ~2x | Perimeter differs (GS five names incl. ORCL) but ORCL can't explain ~$200bn. The debt-funded share of 2027 capex is a live disagreement between houses. |
| WULF (no page) | Barclays Digest: CB-5 pushed to **1Q27 from 4Q26** (2026-09-16) | MS "on schedule" read on ai-datacenter-power | Schedule conflict | Both kept. Sept vintage; check TeraWulf's 3Q update. Relevant to GOOG (Fluidstack backstop) only at the margin. |
| Reflection / SpaceX | Redburn: c72MW at an ASSUMED $25m/MW/yr | SPCX page: JPM/podcast ~$50m/MW | 72MW vs ~36MW | Assumption-driven; the MW in the new REFL-SPCX-2026 row is labelled as Redburn's estimate. |

## CONFIRMS (no action)

| Ticker | New datapoint | Baseline | Read |
|---|---|---|---|
| CRWV | Barclays HY 3Q26E revenue **$3,581m** | BBG 1FQ $3,553m; guide $3.45-3.60bn | +0.8% vs consensus, top of guide. |
| CRWV | Barclays: 5y CDS **1,100/1,160 (1,130bp mid)**, 49.9% implied 5y PD (2026-10-15) | BBG `CRWV CDS USD SR 5Y D14 Corp` **CDS_FLAT_SPREAD 1,120bp** (credit workbook snapshot 10-16 12:48) → **1,164bp** (live `bdp` 2026-10-19, LAST_UPDATE_DT 10-16) | **CONFIRMS — resolved 2026-10-19 (live bdp; was PENDING).** The "482bp" baseline was the SAME ticker's **PX_LAST** field (482.3 on 10-15, 468.5 on 10-16), not a different contract: PX_LAST and CDS_FLAT_SPREAD are two quote bases on one D14 contract, and the flat (conventional) spread is the one that matches the broker's 1,130bp mid (+10bp vs the 10-16 snapshot, −34bp vs the 10-16 close). ⚠️ The credit monitor's "CoreWeave 5Y CDS" series (`credit_watch.json`, field PX_LAST) publishes the ~470bp basis while the credit workbook's CDS tab uses CDS_FLAT_SPREAD — never net the two; cite the field with the number. |
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
- ~~BBG Terminal down: re-run `/wiki-consensus` to resolve the PENDING CDS / EUR-2032 yield checks.~~ Done 2026-10-19 (both rows above). Open: the credit monitor's 5Y CDS series is on PX_LAST (~470bp) while the workbook uses CDS_FLAT_SPREAD (~1,160bp) — pick one basis for the dashboard label.
- NBIS.md 07-20 FinTwit row says the $1.1bn Reflection deal was with META — Redburn and the page's own history say Nebius. Flagged in-line, not rewritten.
- CRWV.md Risks still cites "$25.1B principal debt" (Q1 vintage); Barclays/house use $35.55bn at 2Q26 — stale line.
- Barclays TSMC note (OW, PT US$665) still queued in `_inbox/PENDING_FULL_REPORTS.md`.

_BBG column resolved 2026-10-19 — estimates.json asof 2026-10-19 (107/107). Re-placed on the fresh vintage: CRWV CY2027 consensus rev $26.47bn / EBITDA $16.66bn (unchanged vs the 10-16 snapshot, so the Barclays +6.8% / +9.4% gaps stand); Redburn Sell PTs vs BBG median PT $136.52 / $287.95 / $240.01 (CRWV / NBIS / ORCL), px 10-19 $62.72 / $171.56 / $130.07 — CRWV is now ~16% above Redburn's $54. The CDS / EUR-2032 rows were resolved with a live `bdp` on the bond and CDS tickers (not in estimates.json)._
