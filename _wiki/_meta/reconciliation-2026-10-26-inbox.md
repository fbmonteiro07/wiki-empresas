# Reconciliation — /run-inbox 2026-10-26 (interactive, daytime)

Sources reconciled (quantitative only):
- **UBS · Timothy Arcuri / Seth Cho — "$210B Server CPU TAM By C2030; Gated By Memory Supply"**, 2026-10-26. On-page ingest was split: the "Relação DRAM e CPU" session wrote the first pass (MU/AMD/INTC/ARM/NVDA + hbm-memory/cxl-memory-fabric) and this run added the second pass (PT history, Fig 39, $210B basis, BBG deltas).
- **Anthropic, PBC — Form S-1**, filed 2026-10-26 (EDGAR acc. 0001628280-26-067168, verified). Counterparty read-throughs on AMZN/GOOG/MSFT/NVDA/AVGO/AMD are from this run. The ANTHROPIC page itself is c6d7e2bc (Codex numerical review + the "S-1 highlights" session).
- **SpaceX 8-K** Item 8.01, filed 2026-10-26 (event 10-24, acc. 0001104659-26-118614).

**BBG: LIVE** (`bdp`, pulled 2026-10-26 ~11:30 BRT). ARM 1FY/2FY are March fiscal years; UBS's ARM model is calendar (C2026E), so ARM is compared against the calendarized `estimates.json` row.
**House:** `house.json` has no AMD/INTC/ARM/MU/SPCX model. AMZN is not in it either, while GOOG/NVDA/AVGO are but the S-1 adds no EPS/revenue datapoint to reconcile against them. The house baseline is therefore n/a this run.

## DIVERGES (the alpha)

| Ticker / theme | Metric | New datapoint | Baseline (prior wiki · BBG live) | Gap | Note |
|---|---|---|---|---|---|
| INTC | UBS PT | **Neutral, $100** (from $103, 10-19) | BBG mean PT **$120.78**, px $87.11 | UBS **−17%** vs consensus PT | Second cut in a week. At the median foundry comp ($92/k-wsm vs the $160 average UBS applies) the SOTP is ~$95 (our arithmetic). The page's old "$122" was INTC's **share price** in the 07-07 note's disclosure table, not a PT. Corrected by the DRAM session (drift line). |
| INTC | UBS EPS C2028E | **$2.94** | BBG 3FY **$3.168** | **−7%** | UBS sits below the Street on the out-year while C2026-27E are +1% / +4% ($1.57 / $2.20 vs $1.555 / $2.119). UBS has FCF negative in C2027-28E (−$1.0B / −$4.2B, Fig 33). |
| AMD | UBS EPS CY27E | **$17.58** | BBG 2FY **$15.85** | **+11%** | CY26E $7.91 vs $7.579 (+4%). UBS's "$3-4K per CPU" headline (p.1) sits well above UBS's own AMD server ASP of ~$1.6-2.4K (Fig 32). Flagged on the page. |
| AMD | UBS PT | **Buy, $730** (unchanged since 07-24) | BBG mean PT **$651.65**, px $516.26. Page Debate still listed UBS at **$700** (07-15 step) | UBS **+12%** vs consensus | The page's $700 was a stale mark (tagged, not rewritten). |
| server-cpu-tam (AMD/ARM/INTC) | C2030E TAM | **UBS $208B printed / ~$210B headline**: traditional $48B + AI $160B (≈$99B head-node + ≈$61B standalone) | UBS's own prior **~$175B** (05-18/21). BofA **$210bn+** CY30E (08-12): ~$30bn traditional + ~$180bn AI | Same headline, **different composition** | UBS holds AI attach at 0.83:1 and sizes the base to a 77EB DRAM line (an identity, not evidence that memory set the count). BofA moves toward ~1:1. Never merge the two $210Bs. Unit share C2030E AMD 34 / ARM 38 / INTC 28 (from 29 / 42 / 29). |
| ANTHROPIC × MSFT | Azure commitment | **≥$44.9bn** Nov-2026→May-2033, minimum, per-tranche exit for undelivered tranches | Relay **$31.4B** (09-29) / **$30bn** announced (Nov-2025) | **+43%** vs relay | Amended Feb and Oct 2026. Smallest of the three CSP floors. Starts Nov-2026. |
| ANTHROPIC × SPCX / NVDA | SpaceXAI compute | **Up to $120.5bn** into 2029; **~$3.1bn/month** at full delivery (Dec-2026) | NVDA page: **$1.25bn/month** (JPM desk 06-30). Deal seed **$45bn**, relay **$84.5bn** | ~2.5× the monthly run-rate | "Up to", cancelable on 90 days' notice after the Jan/Mar-2027 initial periods. The flexible (GPU) dollars vs the non-cancelable (TPU/CSP) dollars are the S-1's real message for NVDA share. |
| ANTHROPIC × GOOG | TPU beyond the floor | **$125-150bn** estimated 2028-31 payments to "TPU providers, including Google" | Not on the wiki | New | An estimate outside the commitments table, across providers. Don't add it to the ≥~$114.5bn floor or allocate it to Broadcom. |
| ANTHROPIC × AMZN / GOOG | Ownership caps | **Amazon 12%** conversion cap; **Google 14.99%** cap | BofA: Amazon **15-21%** stake estimate (09-04); Google **14%** | AMZN cap below BofA's range | The S-1 discloses caps, not % held (the principal-holders table is voting stock only). |
| ANTHROPIC × NVDA | NVIDIA equity | **None disclosed**: only Amazon, Google, Microsoft are named equity investors (p.74) | BofA **$10bn** NVIDIA investment (08-07) | Not confirmed | The Lambda "10% NVIDIA revenue share" (Patel, 10-25) is also not in the filing. |
| ANTHROPIC × AMD | AMD supply | **>$20.0bn** expected spend over the term if the CY2027 tranche is fully procured; **no MW**; AMD **up to $5.0bn** equity, conditional | Page: up to **2GW / 2,000MW from 1H27**, "$5B equity", desk math **~$15-20B/yr** | Different basis | The >$20bn is Anthropic spend over the term, not an annual rate or AMD revenue. Calendar 2027, not 1H27. |
| AMZN / channel | CSP marketplace take-rate test | H1'26 marketplace sales **~$7.8bn** (48% × $16.286bn, derived); channel-partner fees **+$2.7bn y/y** (p.150) | Relay **~16%** FY25 fee rate ($351M, not in the public S-1) | Up to ~35% if all fees went to CSPs | 🔭 **A test, not a take-rate**: "channel partners" is not CSP-only. |

## CONFIRMS (no action)

| Ticker / theme | Metric | New datapoint | Baseline | Verdict |
|---|---|---|---|---|
| ARM | UBS PT / EPS | Buy **$320** (07-30); C2026E / C2027E EPS **$2.10 / $2.85** | BBG PT **$294.77** (UBS +9%), px $214.35. Calendarized BBG EPS **$2.01 / $2.83** | ✓ In line on EPS (+4% / +1%). Date fix: UBS dates the $360 step **07-20** (page had 07-25, the relay date). Logged in ARM Changelog. |
| MU | UBS PT | Buy **$1,625** (05-26), unchanged | BBG PT **$1,628.94**, px $886.34 | ✓ At consensus. The MU-specific new content is qualitative ("best way to play server CPU demand"). |
| AMZN | AWS commitment | **≥$110.0bn** May-2026→Apr-2036, minimum with true-up | Relay $110B; announced >$100B / 5GW | ✓ Confirms ANTH-AWS-20260420 (no MW in the filing). |
| AMZN / GOOG | 2026 placements | Amazon $25bn package ($10bn funded: G-2 $5bn + Series H $5bn; $15bn conditional). Google $40bn ($20bn funded; $20bn conditional) | JPM "could total ~$33bn" AMZN (06-16); JPM $40bn GOOG | ✓ Both confirm. The AMZN $33bn is lifetime: ~$8.0bn legacy notes (2023/24) + $10.0bn in 2026 = ~$18.0bn funded, plus $15.0bn conditional (AMZN page, line ~315). Verified: G-2 57.9m sh in Q2 = Google 38.6m + Amazon 19.3m at $259.1364 = $15.0bn. |
| AVGO | Broadcom leases | **~$161.2bn** rent ex-interest, five-year master equipment leases, **Broadcom named lessor**; 2026 lease ~$125.2bn; up to **$42.0bn** convertible (9% PIK / 90% VWAP; 13% / 85%) | Relay $161.2bn "Broadcom-related"; AVGO 10-Q "up to $42bn" | ✓ Confirms, and upgrades "related" to named. Still no GW, so the GW-ladder reconciliation stays open. |
| NVDA | Nscale | Up to **~$44.6bn** into 2033 | Page $45bn / 6 years; Nscale's own S-1 $44.6bn | ✓ |
| SPCX | Chip financing | 8-K: binding commitment letter, Apollo-managed lessor, **~$40bn** principal GPU finance lease; close before YE26; schedules 1H27 | Press ~$40bn talks (FT/WSJ/Reuters 10-06/07). BBG PT $247.67, px $147.41 | ✓ Size confirmed. Structure changed (lease vs loans/bonds). Status upgraded (commitment, not closed). No estimate change. |
| ANTHROPIC | Concentration | Top five ~**25%** of 9M'26 revenue; no customer >10% | Codex review: ~21% (Q3-only, derived) | ✓ Different periods, consistent. |

## Follow-ups
- **INTC** is the one name where the new note moves away from the Street (PT −17% vs consensus, C2028E EPS −7%). The INTC 3Q print is the 2026-11-03 catalyst on the page.
- **Pull the S-1 exhibits that matter** (ex-4.3 Amazon NPA, ex-10.11 Broadcom 2026 lease) into a deal-level read if the GW reconciliation is needed. The CSP cloud contracts themselves are not filed.
- **SPCX:** log the Apollo lease close/pricing under SPCX-NVDA-FIN-20261006 when filed. The Q3 10-Q (acc. 0001628280-26-066880, filed 10-22) is on EDGAR but not archived in `SPCX/`.
