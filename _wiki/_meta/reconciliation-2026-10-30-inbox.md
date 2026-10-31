# Reconciliation — /run-inbox 2026-10-30

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG live is OFFLINE**: `bdp` gets "Failed to connect to 127.0.0.1:8194", meaning the Terminal is not logged in. The BBG column therefore uses the **on-disk snapshot `_wiki/_data/estimates.json`, asof 2026-10-30** (same-day, from the 10-30 /wiki-consensus run). It does not need re-running, but the Q3 quarter columns are pre-print.
- **No house model exists for BKNG, SNOW, MSFT, META or ANTHROPIC.** GOOG/NVDA/AMZN house models carry nothing comparable to tonight's datapoints.
- **Private names** (ANTHROPIC, OPENAI, SPCX pre-IPO marks) are checked against prior wiki marks only.

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (snapshot 10-30) | Read |
|---|---|---|---|---|---|
| **BKNG** | BofA 4Q bookings / rev / EPS **$45.0bn / $6.7bn / $2.25**; 4Q nights 297m (+5%); expected 4Q guide nights +3-5% vs Street +6% (BofA · Post, 2026-10-25) | Same direction as JPM 10-15 (FY guide implies 4Q GB ~+2%) | none | 4Q cons rev **$6,791m**, EPS **$2.301** → BofA **−1.3% rev, −2.2% EPS** | Two houses now pre-position a 4Q cut. The 11-03 print is a **4Q-guide event**: a guide at Street (+6% nights) would be the surprise. |
| **BKNG** | Bernstein **Market-Perform, PT $188** unchanged; 2027E EPS $12.05 → **$11.97** (Bernstein · Clarke, 2026-10-19) | PT unchanged; EPS trimmed | none | cons PT **$233.6** (hi $301 / lo $170, n=41) → Bernstein **−19.5%** vs median; px $148.13 → PT **+27%** upside even at MP | The only non-Buy mark on the board. It still implies upside from a 52-week-low price, so the stock trades below even the bear-ish house. |
| **BKNG** | Bernstein's app-engagement signal: web traffic +6.9% but app MAU **+1.1%** (Sep −2%, Oct −4%); Priceline weakest (Bernstein, 2026-10-19) | 🆕 first app-vs-web split on the page | — | — | Direct/app share is the agentic-disintermediation falsifier (MS 10-12 framework); a falling app MAU cuts against the "~2/3 direct" defence. |
| **BKNG** | Booking invests **$100m in its own agent, Vayo**; has not partnered with Muse, while Expedia has (Bernstein, 2026-10-19) | 🆕 not on the page before | — | — | A strategic fork vs EXPE. BofA flags 2027 agentic investment as an earnings-expectations risk. The $100m is unsourced beyond Bernstein's summary. |
| **AMZN** | Capstone house: FY26 ads **≈$81.8bn (+19%)**; underlying rate ~22% → ~18%; 2027 should converge to ~15-17% (Capstone internal ads study, 2026-10-30) | vs pre-print JPM **$84.5bn** / Bernstein **$84.8bn** (as cited by the study) | house ≈ **−$3bn** vs Street on FY26 ads | BBG has no ads line (n/a) | House below the Street on ads. Watch for Street FY26/27 ad-line cuts. The −5pp of 2027 ad growth ≈ −$0.27 EPS sensitivity is the house's. |
| **ANTHROPIC** | Chamath: IPO **$80-120bn raise at $1.3-1.7tn** (midpoint 1.5), "priced fairly… no deal" (All-In #295, 2026-10-30 — podcast) | His own 09-26 X post: ~$200bn at ~$1T. Page marks: $2T (The Information/WSJ); $965B Series H post | — | — | The panel's valuation is now **below** the $2T press marks. The cash base resets the raise size: S-1 cash+STI **$131.651bn**. |
| **ANTHROPIC** | "$80bn debt facility / $300bn dry powder" (UNCONFIRMED speaker); "$100bn ARR by year-end"; "$40tn TAM" (All-In #295) | S-1 (on page): **$15.0bn revolver**; run-rate field blank; $40tn = value of knowledge work | — | — | All three are **host errors vs the S-1**: logged as 🔭 corrections, not adopted. |
| **GOOG** | Host tape "10-15% down, ~$500bn" (Calacanis, All-In #295) | page had no post-print tape | — | Snapshots: $320.46 (10-28 pre-print) → $283.07 (10-29) → **$278.22 (10-30)** = **−13.2% / ≈−$510bn** (snapshot times, not closes) | Host figure **ties** to the BBG snapshots. The new bear vector (Max Anderson auction allegation) is unverified. |
| **META** | Net cash "−2" ($80bn cash+ST vs $82bn debt; UNCONFIRMED speaker) (All-In #295) | page CASH line implied ≈+$1.5bn (cash vs non-current debt only) | — | — | 3Q26 10-Q: cash+marketable **$82.449bn** vs total debt **$83.669bn** → **≈−$1.22bn** (Chamath's first "−1.2" ties; the "−2" correction does not). Page now carries both bases. |
| **hyperscaler-capex** | "AI complex owes $340-400bn"; funding need through end-27 ≈ **30%** of Treasury issuance (later "30-40%") (Chamath, All-In #295) | GS five-name 800 / 35% / 420; JPM $4.1T AI debt through 2030 | — | — | **Basis unknown and drifts within the episode.** Kept separate and not netted against GS/JPM. |

## CONFIRMS (no action)

| Name | Datapoint | Baseline | Result |
|---|---|---|---|
| BKNG | BofA Buy, **PO $234 → $232** (19x 2027E EPS $12.23) | cons PT $233.6 | at consensus; −$2 is a 2027E EPS trim, not a view change (old PO → Changelog) |
| BKNG | 3Q: BofA nights 342.5m / GB $52.98bn / rev $9.613bn / EBITDA $4.528bn / EPS $4.52; Bernstein rev $9.634bn / EBITDA $4.555bn | BBG Q3 cons rev **$9,544m**, EBITDA **$4,490m**, EPS **$4.493** | both houses +0.7-1% on revenue, +0.6-1.5% on EBITDA: the "usual small beat" |
| BKNG | BofA 2026E EPS **$10.39** | BBG CY26 EPS **$10.29** | +1%: in line (CY sum, pre-print caveat) |
| SNOW | CEO: "this year, roughly, we will make 6 billion dollars", ~9,000 people (Ramaswamy, Unicorn Bakery, 2026-10-29 — podcast) | FY27 product-rev guide $6.07B (Q2 FY27); BBG CY26 total rev **$6,193m** | ties to the product guide; not a new guide |
| GOOG | Cloud $30.7B, Cloud OI $3.6B → $11.1B, Search +12% to $63.35B, Services OI ~$39B (All-In hosts) | Q3 FY26 release on the page | all tie |
| MSFT | Revenue $198bn → $332bn with ~+2,000 staff (UNCONFIRMED speaker) | 10-Ks: FY22 $198.27bn → FY26 $331.84bn; employees ~221k → ~223k | ties on an FY22→FY26 basis |
| MSFT | "halved its debt" (Chamath) | total debt $49.78bn (FY22) → $40.29bn (FY26), −19% | direction right, magnitude overstated |
| NVDA | $1 COGS → $4 revenue, 75% GM (Friedberg) | page Q2 FY27 GM 75.0% | ties; the "$18 of Anthropic revenue" chain is illustrative (last step made up by the host) |
| SPCX | Colossus-1 **$1.25bn/month**; June IPO "$85bn" (Friedberg/Calacanis) | 424B4; page $85.7bn incl. over-allotment | ties. Friedberg's $10bn build cost / ~83% margin is his own assumption (~87% on his inputs) |
| ANTHROPIC | H1 $16.286bn (14.0x), Q2 $11.555bn (30.7x), Class F 50.1%, GM 85.4%, $72.388bn + $8.720bn non-cash loss, tiers >11,900 / >1,900 / ~250, RSI 26% | S-1 snapshot on the page | all tie. Friedberg's "85% incremental" is the H1 average; incremental ≈91% (our arithmetic) |
| ANTHROPIC | Q3 "moderated to ~50%" whisper (Chamath) | PARTIAL Q3 $16.8bn (Breakingviews) vs Q2 $11.555bn = +45% q/q | consistent |
| macro-cycle | GDPNow 3.7% Q3 / 2.5% H1; AI capex ~3% of GDP (Sacks) | 10-23: Chamath's unquantified "basically all of" GDP growth | direction confirms; first numbers on the claim (GDPNow not pulled from the Atlanta Fed) |
| ai-compute-deals | Kazakhstan DC Valley "1 gigawatt planned" (Jensen, Astana re-upload) | page: no Kazakhstan–NVIDIA deal ID; June Bloomberg "up to $10B" accords | planned figure, basis unstated: **no new ID** |

## PENDING
- **BBG live**: the Terminal is not logged in. The 10-30 snapshot covers every name above. Post-print (11-03) BKNG consensus will need a refresh.
