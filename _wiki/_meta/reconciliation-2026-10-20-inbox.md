# Reconciliation — /run-inbox 2026-10-20 (scheduled 23h, unattended)

Sources:
- Two earnings prints:
  - **SpaceX Q3 2026**: the release plus the Bloomberg INITIAL DRAFT call transcript, 2026-10-20.
  - **Netflix Q3 2026**: the shareholder letter, 2026-10-20.
- Four SPCX previews: Citi 10-09, Wells Fargo 10-08 (+ model), Morgan Stanley 10-18, Deutsche Bank 10-19.
- New Street on CXMT (10-20).
- Jefferies hotel trends (10-20).
- Needham on humanoid robotics (10-20).
- Aterio on a Goldman Sachs-hosted call (10-20).
- SemiAnalysis Weekly podcast, Ep. 039 (10-20).
- Sundar Pichai on the Big Technology Podcast (recording date unconfirmed).

**BBG baseline:** the on-disk snapshot `_data/estimates.json`, **asof 2026-10-20** (same day; it came from the 12:29 wiki-consensus refresh). Per standing practice that is a valid baseline, so no column is PENDING. FY fields use 1FY/2FY/3FY or quarterly fields; CY2026 sums are not used (known pre-print-consensus defect). **House models:** none of SPCX, NFLX, BKNG or MU has a house block. GOOG has one (capex '27E $310bn).

## DIVERGES (alpha candidates)

| Ticker | Metric | New datapoint | Baseline (prior wiki / house / BBG) | Gap | Note |
|---|---|---|---|--:|---|
| SPCX | YE27 compute | ~13GW (Musk, Q3 call) | Q2 call "closer to 10 than 5"; MS 4.9GW; JPM 6.4GW; VA ~6GW | **>2x Street** | Same nameplate basis. The largest gap on the page. |
| SPCX | Q4-26 capex guide | $35-40bn (Johnsen) | Q2 call "similar to current quarter" (~$18.4bn); BBG 2FQ $21.6bn | **+62-85%** | FY26 implied ~$83-88bn vs 1FY $67.3bn, DB $70.0bn, WFS $66.3bn |
| SPCX | Q1-27 revenue guide | $33-37bn | BBG CY27 $113.6bn ≈ $28.4bn/qtr; WFS model Q1 $26.47bn | **+16-30%** | The guide alone annualises to $132-148bn |
| SPCX | Compute exit-2026 | 2.5-3GW | >2GW (08-04); JPM 2.2GW; Needham ~2.5GW | up | Guide raised |
| SPCX | Q3 adj. EBITDA | $8.809bn | BBG $6.59bn; WFS $7.59bn | **+34%** | Beat |
| SPCX | Q3 revenue | $14.575bn | BBG 1FQ $12.87bn; WFS $13.27bn; UBS relay $13.8bn | **+13%** | Above every preview |
| SPCX | Q3 GAAP EPS | $0.35 | BBG $0.147 | n/m | Inflated by other income (~$1.0bn) and a tax benefit. **Reconcile at operating income:** $2.79bn vs BBG EBIT $2.24bn (+25%). |
| SPCX | Consumer subscribers | 13.6M | VA 14.29M | −5% | Miss, offset by ARPU of $69 vs $66.74 |
| SPCX | WFS model FY27 capex | $301.0bn | BBG CY27 $187.4bn | **+61%** | Ties to the WFS PDF |
| NFLX | Q4-26 EPS guide | $0.67 | BBG $0.733 | **−8.6%** | Op margin 26.0% includes ~120bps from the RIF; ~27.2% ex-RIF is still below the 27.5% bar |
| NFLX | Q4-26 EBIT guide | $3,500M | BBG $3,722M | −6% | |
| NFLX | Q3 op margin | 34.6% ($4,459M) | guide 33.2%; BBG EBIT $4,274M | +4.3% | Management says expense timing, not a run-rate |
| NFLX | FY26 ad revenue | ~$2.7B | ~$3B (stated Q4'25-Q2'26) | **−10%** | Guide cut; Sinal Advertising ✓→✗ |
| NFLX | FY26 FCF | ~$12.0B | ~$12.5B guide; cons $12,677M (JPM 10-15) | −4% | One-off Q4 real-estate deal |
| BKNG | Jefferies PT | $185 HOLD (PT history, 10/19) | $200 (09-27); BBG cons $233.89 (low $170) | **−21% vs cons** | Lowest named-house PT on the page; the same note's demand data is strong |
| CXMT | 2030 capacity | ~640k wspm (Counterpoint via New Street) | DB 775k (09-16) | −135k | |
| CXMT | G5 node label | 1b by pitch / 1a by process (New Street) | MS 1b-class; Bernstein ~1c | 3 labels | Same 11.95nm figure |
| theme | 2027 global DC build | ~50GW, raised from 43 (SemiAnalysis podcast) | canonical ~20GW facility | **>2x** | Basis unstated; they are talking their book |
| theme | US active capacity | 55GW (Aterio direct) | JPM 75GW NA 2Q26 (10-13) | −20GW | Widens an open JPM gap |
| theme | 2027 delivered | ~30GW (Aterio, stated timelines, no haircut) | Jefferies 23.1 gross; Bernstein 25.5 facility | up | No delay haircut |

## CONFIRMS (no action)

| Ticker | Metric | New datapoint | Baseline | Note |
|---|---|---|---|---|
| SPCX | Dec-26 ARR | $100bn "on track" | $100bn target (08-04) | Unchanged |
| SPCX | SI revenue Q3 | $7.560bn | UBS AI $7.6bn relay (09-29) | Matches the relay; +17% vs VA |
| SPCX | Nameplate 9/30 | 1.7GW | VA 1.70 | In line, below DB/Citi 1.8 and WFS 1.84 |
| SPCX | $/W | "slightly above the high end of $30-50" | Musk $30-50 (08-04); Citi/VA ~$15/W | **Different revenue-per-watt bases. Not netted.** |
| SPCX | Backlog | $63bn (~$42bn <12m) | $47.5bn (Q2) | +33% q/q |
| SPCX | DB / MS | DB PT $235 unchanged (2027E revenue $115.3bn→$125.25bn); MS PT $300 unchanged (AI SOTP $183→$173) | — | Drift logged in Changelog |
| SPCX | WFS PT | OW $214 (from $212) | cons PT $223.62 | Below consensus |
| NFLX | Q3 revenue | $12,874M | guide $12.86B; BBG $12,872M | In line |
| NFLX | FY26 revenue | $51.1B | $51.0-51.4B guide; BBG 1FY $51,226M | −0.25% |
| NFLX | FY26 OM / EPS | 31.5% held; ~$3.57 implied | BBG EBIT $16,132M; EPS $3.508 | +1.8% EPS vs BBG |
| CXMT | Capacity 2026/27/28 | 350k / 420k / 500k (SemiAnalysis via New Street) | WFS/DB 350k; TrendForce 420k; MS ~500k | Within the page range; +50-60k vs the 06-23 Jefferies desk mark |
| Industry | HBM share of DRAM wafers 25/26/27 | 18/22/30% | JPM 19/23/28% | Close |
| theme | Hyperscaler self-build share | ~30%, falling (Aterio) | Jefferies ~60% colo (10-09) | Confirms Jefferies; contradicts the 10-20 lawyer's "20% rising" |
| theme | Humanoid funding 2023 / 2026 YTD | $560MM / >$10.3bn (Needham/PitchBook) | MS $557.5M / $6.6B to 07-15 | Same vendor; trend confirmed |
| theme | Toyota robots / Hyundai Atlas | ~$6.4bn/yr, 400k / ~25k units | JPM 09-27 | Confirms |
| ORCL | New Mexico IT under construction | >1GW (SemiAnalysis) | 1.2GW committed (UBS 08-05) | Consistent |
| GOOG | Compute shortfall | "everyone wishes… 2x" (Pichai) | house capex '27E $310bn; BBG CY27 $319.5bn | Direction only; no number, so the JPM $378bn vs cons spread is untouched |
| GOOG | Argon tokens | ~25T in 72h, ~3x Gemini 3.0 | ~22B tokens/min APIs (Q2 call) | Bases differ, not netted |

## Open items
- SPCX: the Google 9/30 GPU-delivery condition was **not addressed** on the call. The grace period runs to ~10-31.
- SPCX: Q3 10-Q not yet on EDGAR. Once filed, check the payable roll-forward (see the 10-20 capex/AP block).
- NFLX: the bull/bear verdict is pending the tape and the interview transcript.
- SPCX Q2-call revision file (`…2026804 DN…`) is still on P:. The sweep reports CONTENT DIFFERS. Pull it manually and diff it against the 08-04 FINAL transcript.
