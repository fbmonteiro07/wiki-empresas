# Reconciliation — /run-inbox 2026-10-23 (scheduled 23h, unattended)

Sources with NEW quantitative datapoints (31 files processed; qualitative podcasts are skipped here unless they carry a number):
- **UBS** · Karl Keirstead, "CoreWeave Inc — Credit Risks and Playing AI Defense", 2026-10-23 (Buy, PT $120 → $105).
- **Morgan Stanley** · Adam Wood / Ryan Lountzis / Kate Konetzke, "CoreWeave: Where Do We Go From Here?", 2026-10-23 (EW, PT $99 → $70).
- **Goldman Sachs** · Gabriela Borges, "Oracle: Data center model refresh ahead of investor day", 2026-10-22 (Buy, PT $240 → $206).
- **J.P. Morgan** · Samik Chatterjee, "Oracle: Investor Day Preview…", 2026-10-20 (OW; no PT in the note).
- **Morgan Stanley** · Meta Marshall et al., "CQ3 Reseller Survey – Acceleration Continues As Threat Environment Grows", 2026-10-22.
- **Citi** · Fatima Boolani et al., "CIO Survey: Cyber Budget Trends Showing Acceleration", 2026-10-15.
- **FUNDA (FundaAI)**, "Preview|MSFT FY1Q27…Azure Expected to Beat Guidance", 2026-10-23 (independent substack).
- **J.P. Morgan Korea desk** China-NAND expert call (expert "Mr. Tian"; call date ~2026-10-22, UNCONFIRMED).
- **SemiAnalysis**, "Amazon's Trainium Takes a Strike at the Training King", 2026-10-23; SemiAnalysis Weekly Ep. 040 (2026-10-23).
- **Management on podcasts:** Jensen Huang (BG2, 2026-10-15), Andy Jassy (a16z, 2026-10-23), Nikesh Arora (All-In, 2026-10-21). OpenAI security post (2026-10-23).

**BBG baseline: LIVE tonight.** The wrapper answered at ~23:30 (`bdp`, `BEST_FPERIOD_OVERRIDE` 1FY/2FY/3FY; PX_LAST and BEST_TARGET_PRICE = consensus mean). Fiscal bases: ORCL FY May (1FY = FY27), PANW FY Jul (1FY = FY27), CRWD/OKTA/NET/NVDA FY Jan (1FY = FY27 ≈ CY26), MSFT FY Jun, CRWV/AMZN CY. The on-disk `_data/estimates.json` (asof 2026-10-23) was not refreshed by this run.
⚠ **AMZN BBG EPS is contaminated below the line** (1FY $14.43 > 2FY $12.49 with EBITDA rising): it embeds equity-stake marks. Reconcile AMZN at EBITDA/sales, not EPS.

**House baselines:** CRWV — Capstone credit/equity model figures as logged on the CRWV page; NVDA — `house.json` (2027E revenue $661.0bn, EPS $15.44). No house model for ORCL, PANW, CRWD, OKTA, NET, MSFT, AMZN, or the memory names on these metrics.

## DIVERGES (alpha candidates)

| Ticker | Metric | New datapoint | Baseline (prior wiki / house / BBG) | Gap | Note |
|---|---|---|---|--:|---|
| CRWV | 12m PT | **MS $70 (EW, from $99)**; **UBS $105 (Buy, from $120)** | BBG mean **$131.07**; px $54.24 | MS **−47%**, UBS −20% vs BBG | Two of the more constructive houses both cut on financing visibility, not fundamentals. The BBG mean is stale vs the tape (stock −37% in October per UBS); expect the mean to fall. MS sits at a new low on this page. |
| CRWV | CY28 EPS | **MS $2.37**; UBS $0.74 (from $1.66) | BBG 3FY **$1.16**; house **$0.54** | MS **+104%** vs BBG / +339% vs house; UBS −36% vs BBG | Widest spread on the name. MS's $2.37 is its own estimate on the "consensus methodology" basis (p.1 `**`); the `§` line on the same page is **Refinitiv consensus $0.80** — so MS sits ~3x its own quoted consensus and ~2x BBG's $1.16 (panel gap BBG vs Refinitiv +45%). UBS's cut is interest-driven (2028 interest $6.43bn → $8.30bn). |
| CRWV | CY28 capex | UBS **$58.4bn**; house **$60.8bn** | BBG 3FY **$50.8bn** | UBS +15%, house +20% vs BBG | BBG's 3FY capex looks under-built vs both the house and UBS; feeds the funding-gap debate. |
| CRWV | 2027 debt funding gap | UBS **$21-22bn base** (range ~$7-26bn); MS **$24-37bn** of new debt to reach ~3.3 GW by YE27 | Barclays HY ~$30bn (10-15); house NTM ~$19bn (10-14 financing map) | UBS +11-16% vs house; MS +26-95% vs house | The houses now bracket the house map from above. The house's NTM $19bn is the low end; MS's $37bn top would imply a materially larger 2027 raise. Re-check the `Debt` sheet against MS's DDTL ladder (DDTL 1.0 at 15.0% effective is that facility's own rate, not a "spike" — the All-In podcast line is wrong). |
| ORCL | 12m PT | **GS $206** (from $240) | BBG mean **$241.62**; px $126.16 | **−15%** vs BBG | Still +63% upside; the cut is EPS FY28/29 (−2.1% / −2.3%) and multiple, not revenue (unchanged). |
| ORCL | FY29 (May-29) capex | **JPM ~$133bn** (chart read); GS $95.4bn | BBG 3FY **$95.4bn** | JPM **+39%** vs BBG / GS | JPM's capex path ($92 → $120 → $133 → $140bn FY27-30) has no peak before FY30; GS and BBG peak in FY28. "Visibility to peak capex" is JPM's own stated debate for the 10-28 investor day. FY28: JPM $120bn vs GS $112.2bn vs BBG $103.8bn (+16% JPM vs BBG). |
| ORCL | FY29 revenue / EPS | GS $174.1bn / $15.23 | BBG 3FY $183.3bn / $15.74 | −5.0% / −3.2% | GS below consensus on the out-year; JPM's $187bn (+2.0%) is above. Houses straddle consensus by ~$13bn on FY29 revenue. |
| CRWD | 12m PT | **Citi $295** (Buy, from $260) | BBG mean **$252.51**; px $257.57 | **+16.8%** vs BBG | A Street-high-area mark on survey data alone; EPS unchanged vs consensus, so it is all multiple. MS holds $254 (≈ BBG). |
| OKTA | 12m PT | **MS $245** (OW, from $200 — the raise note itself is not ingested; seen in the reseller-survey table) | BBG mean **$214.57**; px $213.05; Citi $215 Neutral | **+14%** vs BBG | Same CY27e FCF ($1,037m), multiple 33x → 41x. The rating-vs-PT tension sits at Citi (Neutral, PT ≈ price). |
| PANW | Refinitiv PT high | MS in-note Refinitiv range tops at **$525** | Page's highest named PT: Wells Fargo $475 (09-20) | +$50 above any PT on the page | An un-ingested house has moved above $475; identify it. |
| YMTC (KIOXIA / SNDK / china-export) | 2027 capacity growth | JPM expert: Fab 3 adds **20-30k wpm by end-2027 ≈ +10-15%** on ~200k wpm (his "+12.5%" for 200k → 250k is arithmetically +25%) | JPM 08-31: *"+25% y-y next year"*; Jefferies 09-22: 250K after Phase 3 (+50K) | ~half the prior growth | Less aggressive China NAND supply than the investor bear case (bullish SNDK/KIOXIA). The expert's own arithmetic is inconsistent and he has been out of the industry a while — treat as a range, not a point. Bases differ (wpm vs JPM's "~2.5mn WSPM", which looks annual) — never net. |
| AMZN / custom ASIC | Trainium3 cost advantage | SemiAnalysis: **~14%** cheaper per marketed FP8 PFLOP-hour vs **GB200** ($0.32 vs $0.37); trails on cost per *effective* training FLOP until MFU ~43% (35% assumed) | AWS/JPM ~30% better TCO vs **GB300** (06-16); Jassy "30 to 40%" price-performance (10-23) | Different comparator | Not nettable (GB200 vs GB300; marketed vs effective FLOPs). It is the first independent TCO model on the page and is materially below the company claim on its own basis. |
| MSFT | Copilot seats (FUNDA model) | **~31M end-Jun-26**, ~37M end-Sep-26 | FUNDA 07-27: 37.0M for end-Jun (now cut); company ">30M" | −16% revision to FUNDA's own June | FUNDA re-based its own series down; Copilot Studio ARR ~$3.0bn is new. Azure call unchanged. |

## CONFIRMS (no action)

| Ticker | Metric | New datapoint | Baseline | Note |
|---|---|---|---|---|
| CRWV | Revenue CY26/27/28 | UBS $13.05 / $28.40 / $45.58bn (unchanged); MS CY27 $25.88bn | BBG $12.86 / $26.81 / $43.12bn; house $12.80 / $26.70 / $44.69bn | UBS +1.5% / +5.9% / +5.7% vs BBG; MS −3.5%. Revenue is not the debate. |
| CRWV | Adj. EBITDA CY26/27/28 | UBS $7.56 / $16.65 / $26.41bn | BBG $7.54 / $16.74 / $27.94bn; house $7.36 / $16.55 / $28.60bn | Within ±1% on CY26/27; CY28 −5.5% vs BBG. |
| CRWV | EPS CY26/27 | UBS −$3.67 / −$1.46; MS −$2.97 / −$0.46 | BBG −$4.01 / −$1.97; house −$3.27 / −$1.83 | Both houses less negative than BBG; same sign. |
| ORCL | FY27/28 revenue & EPS | GS $89.1bn / $8.07, $128.9bn / $10.05; JPM $91bn / $132bn | BBG 1FY $90.4bn / $8.14; 2FY $131.3bn / $11.03 | Revenue within ±2%; GS FY28 EPS −8.9% (D&A/interest), flagged in the DIVERGES capex row. |
| ORCL | FY27 capex | GS $95.1bn; JPM ~$92bn | BBG 1FY $92.1bn | Ties. |
| PANW | 12m PT / EPS | Citi $440 (from $410), MS $410 (Top Pick, unch.); Citi EPS FY27/28 $4.19 / $4.86 | BBG mean $405.98; EPS $4.18 / $4.85 | Citi +8.4% vs BBG; EPS ties. MS reseller "in line/above" 93% vs 79% in Q2. |
| CRWD | EPS FY27/28 | Citi $1.26 / $1.64 | BBG $1.26 / $1.61 | Ties. |
| OKTA | EPS FY27/28 | Citi $3.94 / $4.27 | BBG $3.94 / $4.37 | FY28 −2.3%. |
| NVDA | 2027 consensus growth / multiple (Gerstner on BG2, host framing) | +74%; "13-14x" | BBG CY27 vs CY26 ~+74% (on-disk snapshot); 2FY/1FY sales $702.7bn / $411.1bn; px $210.96 / 2FY EPS $15.89 = 13.3x | Host figure ties to consensus. House 2027E revenue $661.0bn is −6% vs BBG 2FY (standing gap, not new). |
| NVDA | Capital return | Jensen: "60 some odd" % of FCF last quarter vs 50% commitment | Page: Q2 FY27 $26.0bn = 60% of FCF YTD | Ties. |
| NVDA | Content per GW | Jensen "40 plus" (ladder $18bn → "20-something" → 40+); a second "50" for Vera Rubin (basis undefined, speaker UNCONFIRMED) | MS $18 / $25 / $40bn per GW (09-10); GS three bases (09-10) | Consistent with MS's ladder; the "50" is logged without a winner. Content/capex per GW ≠ revenue per GW — never chained. |
| MSFT | F1Q27 Azure / M365 commercial cloud | FUNDA +47% / +18% | Guide 44-45% cc / ~17% cc; Jefferies & MS ~47% (page) | Above the guide but already the Street's whisper; FUNDA's own model said +47.1%. |
| AMZN | FY26 capex | Jassy ~$220bn restated; "could spend a lot more" (direction only) | Q2 call ~$220bn; BBG 1FY capex $221.9bn; 2FY $285.4bn | Ties; no CY27 number given. |
| OPENAI | Annualised revenue end-Sep-26 | UBS $50bn (basis unstated) | FT ~$70bn gross / ~$50bn net (10-12) | Matches the NET basis. WSJ 2Q26 revenue $6.7bn (+18% q/q) is new to the page (private — no BBG/house). |
| ANTHROPIC | 3Q26 revenue (secondhand) | $16.8bn said on All-In citing Bloomberg 10-14 — **UNVERIFIED, primary not pulled** | $65B+ ARR (08-21) | ~$67bn annualised is consistent with the ARR line; NRR 900% / GM 85% / OM 11% stay unadopted until the Bloomberg story is pulled. |
| MU / SKHYNIX / SAMSUNG | Memory shortage duration | Jassy: shortage does not end in 2027; AWS trades HBM vs core DRAM | Page: DRAM shortage to at least 2H28 (AlphaSense Amazon engineer, 07) | Customer CEO confirms. |
| HBM | Hybrid-bonding adoption | SemiAnalysis Ep. 040: "2029 or beyond"; ~+50% GB/stack best case | SA article 10-15: "before 2029, if at all" | Same view, restated by the authors. |
| ASML | 12-inch mask timing | "2030 time frame" (spoken) | Page: pilot 2031 / production ~2033 | Loose spoken variant; not adopted. |
| SKHYNIX | Dalian eSSD output | JPM expert: tool install end-Sep 2026 → output ~Sep 2027 | Page: equipment from 3Q26, etch tools from September | Consistent. |

## PENDING / follow-ups
- **ANTHROPIC** Q3 set — pull the Bloomberg 2026-10-14 story as the primary before any of it reaches the body.
- **PANW** — identify the house above $475 (Refinitiv high $525).
- **OKTA** — the MS $200 → $245 raise note is not ingested; pull it.
- **CRWV** — MS CY28 EPS $2.37 vs its quoted Refinitiv consensus $0.80 vs BBG $1.16: confirm whether MS is the 2028 Street high (the two consensus panels differ by ~45%).
- **ORCL** investor day **10-28** (GS cover's "10/29" is a typo per its own body) resolves the capex-peak fork (JPM vs GS/BBG).
