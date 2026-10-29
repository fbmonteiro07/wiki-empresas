# Reconciliation — /run-inbox 2026-10-28

_Scheduled 23:00 run. 47 inbox files: 34 podcast summaries (19 backfill) + 13 PDFs swept from the P: drop folder. Baselines: (1) prior wiki values on the page, (2) Capstone house models (`_data/house.json`, asof 2026-10-28), (3) BBG consensus from the on-disk snapshot `_data/estimates.json` **asof 2026-10-28** (wiki-consensus refresh 12:27). The live Terminal was not re-queried; the same-day snapshot is the baseline. Per the CY-sum trap, CY2026 sums embed pre-print consensus for reported quarters, so EBIT and out-year figures are preferred where EPS bases differ (GAAP vs adjusted, AMZN's investment marks)._

Podcast numbers are commentary, not estimates. Only those that collide with a filed or modelled number are reconciled below.

## DIVERGES (the alpha)

| Ticker | New datapoint (source, date) | vs prior wiki | vs house | vs BBG consensus (snapshot 10-28) | Read |
|---|---|---|---|---|---|
| **AMZN** | **2027E capex $355bn** (MS · Nowak, 10-18); $312bn (UBS · Ju, 10-26); $302bn (BofA · Post, 10-25); $302.5bn (Bernstein · Devnani, 10-27) | MS was $325bn (07-31) | no house model | CY27 capex **$290.7bn** → MS **+22%**, UBS +7%, BofA/Bernstein +4% | Every broker printing this week is above consensus. MS is the outlier, and its PT still went up ($335 → $350, Top Pick). UBS's framing is that the stock already discounts $300bn+. |
| **AMZN** | **AWS 2027E operating margin 46%** (UBS, 10-26) | — | — | UBS says consensus ~38% | Widest stated gap vs the Street in tonight's flow. MS has 42% ('27) / 44% ('28). |
| **AMZN** | **FY27E EBIT $167.2bn** (MS 10-18); OI $148.9bn (JPM · Anmuth, 10-15) | MS $166.1bn prior | — | CY27 EBIT **$142.1bn** → MS **+18%**, JPM +5% | MS's Top Pick case rests on AWS 47% growth / 42% margin. |
| **AMZN** | 3Q26 EBIT **$28.0bn** (Bernstein 10-27); JPM desk ~$28bn; BofA $26.35bn; BofA desk $25.2bn | — | — | Q3 EBIT **$26.06bn** → Bernstein +7.4% | The bar is above consensus going into tomorrow's (10-29) print. BofA's revenue of $202.0bn ≈ cons $202.26bn. |
| **GOOG** | **JPMe 3Q26 capex $56.3B** (JPM 10-15, Fig. 1 p.4, page image) | **The print block scored the $51.4B print against "$44.9B" (the Q2 actual). Corrected tonight; see the GOOG Changelog** | — | JPM-cited consensus $44.2B | The print was ~$4.9B **below** JPM's model, not above it. |
| **GOOG** | JPMe FY27 capex $378.3B; FCF 2027E **−$96.1B**; $80B of new debt assumed for 2027 | FCF −$96.1B was already on the page | house FCF 2027 **−$55bn** | CY27 capex $322.6bn → JPM **+17%** | JPM's model is far more capex-heavy than both the house model and consensus. Bernstein's FCF 2027E is −$59.8B, close to the house. |
| **GOOG** | JPMe Cloud 2027E **$230.8B** (from $181.7B; growth 70% → 107%) | 2027 +107% only | — | not in the snapshot | TPU-sales driven, and a large step-up. |
| **META** | JPM 2027E capex **$242.7B**, FCF **−$72.8B** (10-15) | same values already logged (48pp deck) | house FCF 2027 **−$56.4bn** | CY27 capex $226.9bn → +7% | JPM's FCF is $16bn worse than the house. Revenue agrees (JPM $307.9bn, house $308.1bn, cons $313.0bn). |
| **META** | JPM 2026E GAAP EPS **$27.99** (from $31.27) on a **$10bn 3Q legal accrual** (52-state AG settlement, outside the expense guide) | $27.99 already on page | house 2026 EPS **$31.96** | CY26 EPS $33.5 | This is a basis gap (GAAP with a one-off), not an operating divergence. Check whether the house model carries the accrual. |
| **META** | "$1.4 trillion" of compute/DC commitments (Patel on the CASPA panel, 10-24, podcast) | 10-Q sums to ~$825bn | — | — | No stated basis, so not adopted. Flagged on the page. |
| **UBER** | Restructuring savings **~$600M+/yr**, ~3,300 people (JPM 10-15) | ~$800M (BofA 09-04); ~3,400 (The Information 09-03) | — | 2027 adj. EPS $4.47 = JPM $4.47 | The savings estimate varies by source. JPM models none of it, so there is EBITDA upside vs JPM if it lands. |
| **RDDT** | Bernstein (first rating) MP **$180**; FY26E rev **$3,464M**, FY27E $4,606M (10-27) | JPM 3Q rev $924M | — | PT cons **$213** (Bernstein −16%); CY26 rev $3,256M (+6.4%); CY27 $4,460M (+3.3%) | Bernstein's own consensus is $3,390M vs BBG $3,256M, so the panels differ ~4%. Bernstein is above on revenue but below on PT. |
| **SHOP** | Bernstein Outperform **$160** (px $168.18), FY26E/27E EPS **$1.69 / $2.19** (10-27) | no PT on page | — | PT cons $177.3; CY26 EPS $1.86 (**−9%**); CY27 $2.59 (**−15%**) | An Outperform with the PT below the price and EPS well below consensus. That is a rating-vs-PT tension. |
| **ANTHROPIC** | SemiAnalysis Ep. 041 (10-27): Google NPA "$40bn / $20bn delivered"; "$70bn NPA"; Amazon stake "~$18bn" (a16z host); "two quarters profitable" | **S-1 on page:** Google up to $30bn / $10bn used / $20bn remaining; Amazon notes $6.2bn + NPA up to $20bn ($5bn used); 1Q26 adj. loss ~$0.6bn implied | private | — | **The podcasts are wrong vs the filing.** Logged, not adopted. ARR "~$80bn" (host) vs $65B+ (08-21); NRR "500%" for 1Q is not in the S-1 (page: Sep ~900%). |
| **NVDA** | AI-native venture funding **~$600bn in 1H26** (Huang, Yahoo Finance at GTC Berlin, 10-21) | $400bn over six months (Huang, 09-14/15) | — | — | The CEO's own figure is up 50% in five weeks. Treat it as a soft number with a moving window. |
| **NVDA / CRWV** | GPU useful life "eight to maybe more" years (Huang, 10-21) | consensus 7–8 yr; CoreWeave 10+ yr (UBS 10-02); Cantor ~10 yr | — | — | First CEO number on this. It supports long depreciation lives at the neoclouds. |
| **CRWV** | GW build cost ~$40bn (2024) → "north of $60bn"; cost of debt with lab offtake 13–15% (Patel, CASPA, 10-24) | Huang ~$50bn/GW build (10-21); `rev-per-gw` (c) ~$50bn/GW | — | — | Same basis (build cost), but Patel is ~20% above Huang. Never net either against NVDA content/GW (BG2 "40+"/"50"). |
| **PANW** | Employees **~21,921** at 2026-07-31 (DEF 14A); NGS ARR ex-CyberArk $7.69bn → implied CyberArk ~$1.4bn | Arora "25,000" (U-M, 10-22); CyberArk + Chronosphere ~$1.6bn (FQ3) | — | — | The CEO rounds headcount up ~14% vs the proxy. Implied CyberArk ARR is below the FQ3 mark, though that mark included Chronosphere. |
| **CRWD** | Breakout time average **29 min** (Kurtz, No Priors, 10-22) | 27 min (GS BBG LIVE, 09-10) | — | — | Likely a vintage difference (new threat report vs old); minor. |
| **TSM** | GM path "45% → now 60" (Patel, CASPA, 10-24) | 3Q26 actual 66.0% | house 2026 GM 66% | — | The podcast figure is stale; the house model and the print agree. |
| **ASML** | WFE 2026 ~$120bn at the start of the year → **~$155bn exit** (Rasgon, CASPA, 10-24) | LRCX "mid-$150bn"; MS $163bn (08-25) | — | — | Within the existing range (on a CY-exit framing). |
| **MU / SAMSUNG / SKHYNIX / SNDK** | Memory fwd P/E "two, three, four times" (Rasgon, CASPA) | BofA comp table 10-28: MU 12x/5x/5x, Samsung 5x/4x/4x | — | — | Rhetorical. Rasgon's range sits below the BofA comp table. |

## CONFIRMS (no action)

| Ticker | Datapoint | Baseline it matches |
|---|---|---|
| AMZN | PTs: MS $350, UBS $348, JPM $365, BofA $320, Bernstein $320 | BBG PT cons **$333.5** (hi $405 / lo $230). All within the band; median broker ≈ cons |
| AMZN | 3Q revenue BofA $202.0bn; UBS 3Q EPS $2.42 | cons Q3 rev $202.26bn / EPS $2.35 |
| AMZN | Project Mercury numbers (BofA · Post primary, 09-16) | the relay already on the page (09-16), every number matches |
| META | JPM post-revision values (2027E rev $307.9bn, GAAP EPS $31.08, capex $242.7bn) | the 48pp deck already logged; house rev 2027 $308.1bn |
| UBER | JPM 3Q GBs $59.9bn, adj. EBITDA $2,936M; 2027E adj. EPS $4.47 | page (48pp deck); BBG CY27 EPS $4.47 |
| GOOG | Bernstein MP $385 unchanged; Waymo >500k paid rides/wk (Pichai 10-21) | page |
| MSFT | F1Q27 slides + F2Q27 outlook slides | every number in the print block (only two source-label corrections) |
| AVGO / ANTHROPIC | Broadcom NPA $42bn (SemiAnalysis Ep. 041) | S-1 $42.0bn (but it funds lease rent, not new TPUs) |
| ANTHROPIC | Compute commitments $500–600bn (Ep. 041); revenue/MW ~$16M → $60M+ | page $265.6bn + $321.4bn = $587.0bn (June); SemiAnalysis 07-08 |
| NSCALE / SPCX | ~$100bn/GW Nscale commitment; ~$15bn/GW SpaceX on 90-day terms | page arithmetic $44.6bn / 460 MW ≈ $97bn/GW; $50M/MW/yr terminable |
| OPENAI | 1.2bn weekly users (90% free); health ~1/3 of weekly users; Stargate $300bn / 4.5GW | page |
| NET | non-human traffic 60/40; hyperscaler GPU utilisation 5–8% | ">50% non-human" (Q2 call); "single digits" (Q1 call) |
| CXMT (no page) | BofA initiation re-download | identical to the 10-27 ingest except a page-1 recipient watermark |

## Not reconciled / pending
- **AMZN prints 2026-10-29 AMC.** All AMZN bars above are pre-print, so score them at the print.
- MS FY26 EPS $13.24 (10-18) vs $13.43 (MS 10-07) comes from different tables and is not reconciled.
- OpenAI: 100,000 advertisers / 89 countries (Friar, 10-21) is net-new with no baseline (UBS 10-07 said "test phase").
