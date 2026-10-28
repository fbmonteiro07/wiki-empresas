# Reconciliation — /run-inbox 2026-10-27 (scheduled 23:00)

_Sources: GS · Giuni Lee / Daiki Takayama "TrendForce memory expert session…" (2026-10-27); BofA · Dai Shen / Simon Woo / Matt Shin "CXMT (A): China memory/AI key play… initiate Buy" (2026-10-28); Bernstein · Mark C. Newman et al. "HBF Deep Dive" (2026-10-27); FUNDA "Research|ANT: S-1 Review and First-Cut EPS Model" (2026-10-26); Cliff Sosin on Invest Like the Best EP.497 (2026-10-27, podcast)._

**Baselines.** (1) Prior wiki marks: the pages themselves. (2) House models: none exist for the memory/storage names or ANTHROPIC. META has one, but the Sosin podcast carries no numbers, so it isn't used. (3) BBG: the live `bdp` call got ConnectTimeout on 127.0.0.1:8194 (Terminal logged out), so the column uses the **on-disk snapshot `_data/estimates.json` asof 2026-10-27**, not live data. BBG FY mapping: SNDK/WDC/STX 1FY = FY Jun-27; MU 1FY = FY Aug-27; SKHYNIX/SAMSUNG 1FY = CY26 and 2FY = CY27; KIOXIA 1FY = FY Mar-27.

## Where the new data DIVERGES

| Name | New datapoint | vs prior wiki | vs house model | vs BBG consensus | Read |
|---|---|---|---|---|---|
| ANTHROPIC | FUNDA first-cut model: adj. OM FY26E 3.4%, **FY27E −12.9%**, FY28E −3.6%, FY29E 14.1%; compute **$98.6bn FY27E**, $152.3bn FY28E; cash trough $150.1bn end-2028 after an assumed ~$60bn IPO | WFS EBIT ex-SBC **+23.3% 2027E / +35.5% 2028E**; WFS compute $63.2bn 2027E; Barclays $74B (06-01). Revenue matches WFS (FY27E $118.3bn vs $117.6bn) | n/a (private) | n/a (private) | **Same top line, opposite margin sign.** FUNDA expenses the ~$800bn of commitments faster (68% by 2030). The debate is cost timing, not demand. Test: compute line in the S-1/A. |
| SKHYNIX | Bernstein O, TP **KRW 2,700,000**; EPS CY27E **554,848**. GS Buy TP ₩3,500,000 (unchanged) | Both unchanged (Bernstein 09-29, GS 10-12) | n/a | Cons PT ₩3,219,709: Bernstein **−16%**, GS +9%. Bernstein CY27 EPS **+16%** vs cons 2FY 477,698 | Bernstein sits below consensus on target while above it on EPS, i.e. it applies a ~4.9x multiple. A multiple call, not an earnings call. |
| SAMSUNG | Bernstein O, TP KRW 440,000; EPS CY27E 74,602. GS TP ₩500,000 common / **₩380,000 pref (from ₩360,000)** | Bernstein unchanged; GS pref drift logged in Changelog | n/a | Cons PT ₩493,547: Bernstein **−11%**, GS +1%. Bernstein CY27 EPS +4.6% vs cons 71,321 | Same pattern as Hynix: Bernstein's EPS is above consensus and its PT below. |
| MU | Bernstein O, TP **$1,300**; EPS FY27E 173.33 | Unchanged | n/a | Cons PT $1,628.94 → Bernstein **−20%**, near the Street low ($1,150). EPS +1.4% vs cons 1FY 170.99 | EPS is in line and the target is a low outlier: a multiple discount, now ~29% below cons PT/spot math. |
| SNDK | Bernstein O, TP **$3,000**; EPS FY27E 238.36 / FY28E 272.09 (labelled "2026E/2027E", base year 2026) | Unchanged; HBF trade-ratio mark moves 3–4x (08-14, unverified, no text layer) → **6.5x** | n/a | Cons PT $2,284 → **+31%** (Street high $3,900). EPS **+11.5%** / +3.6% vs cons 1FY 213.69 / 2FY 262.63 | Above consensus on both target and FY27 EPS. HBF is explicitly excluded from guidance, so it is upside optionality outside the numbers. |
| STX | Bernstein O, TP $1,350; EPS 40.61 / 64.40 | Unchanged | n/a | Cons PT $1,109.5 → **+22%**. EPS +9.5% / +12.3% vs cons 37.08 / 57.36 (basis assumed FY27/FY28) | Above consensus. WDC's cut widens Bernstein's STX-over-WDC preference. |
| WDC | Bernstein O, TP **$600 (from $770)** while EPS rises to 27.30 / 45.26 (from 23.39 / 36.58) | **Thesis drift: PT −22% while EPS is up 17% / 24%**; the note has no WDC text explaining it, so it may be a ticker-table error | n/a | Cons PT $609.5 → −1.6% (was well above). EPS +8% / +10% vs cons 25.28 / 40.99 | Unexplained. Verify against Bernstein's next WDC-specific note before using. |
| HBM industry | TrendForce via GS: 2027 blended HBM ASP **+122% to US$3.7/Gb**; industry revenue **>$200bn (+>230%)**; HBM4 ~60% of 2027 revenue; China <2% | TrendForce +121% (09-29) is self-consistent. Sell-side: JPM $3.0/Gb (+54%) and $160.1bn (09-22); UBS +76%; RBC +80-100%; GS own +100-160% | n/a | n/a (industry metric) | **The expert channel is ~$40bn+ above the highest sell-side HBM revenue mark on file.** Upside to Hynix/Samsung/MU HBM lines if TrendForce is right. |
| CXMT (688825 CH) | BofA initiation Buy, PO **CNY65**; EPS 2.85 / 3.85 / 4.30 (2026-28E) | Lowest bullish target on file: UBS Rmb70 (08-07), Bernstein CNY70 (09-21), MS Rmb88 (09-20), Nomura CNY116, GS Rmb129 (08-24). EPS vs UBS 2.20 / 4.98 / 6.40: **−23% 2027E / −33% 2028E** | n/a | no BBG (688825 CH not on wrapper; absent from estimates.json asof 2026-10-28) | BofA models a 2028 soft landing (ASP −10-20% pa after +9% in 2027). That makes it the most cautious CXMT model on file, and the only one to forecast an ASP down-cycle. |
| KIOXIA | Bernstein U, TP ¥49,000; EPS ¥10,485 / ¥14,140 against a post-split close of ¥12,605 | Matches the 09-29 marks (also pre-split) | n/a | Cons EPS 1FY ¥3,497 ≈ Bernstein ÷ 3 (¥3,495), which confirms a **3:1 split mismatch**. ⚠️ BBG's PT panel is also suspect: cons ¥38,331, Street **low ¥15,550 above the price**, 2 Sells | **Data-quality flag, not alpha.** Bernstein's TP split-adjusted is ~¥16,333, still above the price on Underperform. Don't use the KIOXIA consensus PT until the panel is split-adjusted. |

### Notes on the above
- Prices in Bernstein's 26-Oct ticker table (SNDK $1,255.58, STX $644.21, MU $903.70, Hynix ₩1,341,000) are far below the last page marks (SNDK $1,712.89 on 09-28; STX $887.09 on 10-06). That matches the snapshot spot (SNDK $1,304.84, MU $928.76). Memory names have de-rated sharply in October, which is why consensus upside reads +60-140%.
- Bernstein's KIOXIA mismatch and the BBG panel both suggest any KIOXIA "upside to consensus PT" screen is currently meaningless.

## Where the new data CONFIRMS (no action)

| Name | New datapoint | Baseline | Read |
|---|---|---|---|
| ANTHROPIC | FUNDA FY26E revenue $52.80bn; 3Q26 back-solve ~$16.9bn (86x 4Q24) | WFS $52.631bn; house S-1 middle sensitivity $53.25bn (10-26); investor-day $16.8bn (10-15, PARTIAL) | Top line is consistent across all three. |
| ANTHROPIC | Distillation revenue ≈ $1.7–2.3bn (5–7% of ~$33bn 9M26) | S-1 5–7% share already on the page | First dollar estimate; FUNDA arithmetic on an S-1 fact. |
| SKHYNIX / SAMSUNG | GS Buy, ₩3,500,000 / ₩500,000 | Unchanged vs 10-12 / prior | No change. |
| DRAM pricing | TrendForce: DRAM up through 2027 into 1H28; LTA coverage 60-70% moderates 2027 increases; meaningful capacity not before 2028 (80-100K WPM per Korean supplier) | Consistent with the hbm-memory/SKHYNIX supply narrative and the 3Q26 print commentary | Confirms the "tight through 2027" consensus. |
| META | Sosin: "250 billion of revenue and they spend $250 billion a year" | FY26 revenue implied $254.7-257.7bn; capex $135-145bn + expenses $175-179bn (Meta 10-21) | Order of magnitude only; rhetorical capex+opex mix. |
| hyperscaler-capex | Sosin "3% of GDP" | GS 1.8% US GDP 2026 / 2.5% 2027 (08-02) | Off-the-cuff guest number; not used as a datapoint. |

## BBG consensus pull

Source: on-disk snapshot `_data/estimates.json` asof 2026-10-27 (Terminal offline at 23:27).

| Ticker | Spot | Cons PT | Upside | Read |
|---|---|---|---|---|
| SNDK | $1,304.84 | $2,284.26 | +75% | Bernstein $3,000 is above |
| WDC | $380.88 | $609.48 | +60% | Bernstein $600 is in line (after the cut) |
| STX | $667.85 | $1,109.55 | +66% | Bernstein $1,350 is above |
| MU | $928.76 | $1,628.94 | +75% | Bernstein $1,300 is below |
| SKHYNIX | ₩1,341,000 | ₩3,219,709 | +140% | Bernstein below, GS above |
| SAMSUNG | ₩222,000 | ₩493,547 | +122% | Bernstein below, GS ≈ |
| KIOXIA | ¥12,605 | ¥38,331 | (+204%, suspect: pre-split panel) | do not use |

**Edge-tracker note:** `edge.md` has been frozen since 2026-10-12 (retired tracker, per the repo CLAUDE.md), so this report is read directly. It is named for the run date, which sorts before the concurrent `reconciliation-2026-10-28-skhynix.md`, and was left that way rather than renamed to sort after it.

_BBG column resolved 2026-10-28 — estimates.json asof 2026-10-28._
