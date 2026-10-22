# Reconciliation — /run-inbox 2026-10-21 (scheduled 23h, unattended)

Sources:
- **Meta Q3 2026 print:** press release + 8-K, 2026-10-21. No call transcript was on disk.
- **Bernstein** · Shmulik et al., "Meta: From Facebook to Meta to Muse", 2026-10-20.
- **BofA** · Post / Bansal, "3Q Preview: Back on offense with AI", 2026-10-16. The PDF is now on disk.
- **Micron** · Scott DeBoer, "Technology and Product Leadership" webinar, 2026-10-21 (Bloomberg live transcript).
- **Cantor** · Knoblauch, "Backstop 101: What Does a Backstop Mean?", 2026-10-21.
- **Wells Fargo** SpaceX model, 2026-10-21 (Gawrelski), post-Q3.

**BBG baseline:** the live wrapper failed (no Terminal session on localhost:8194). I used the on-disk snapshot `_data/estimates.json`, **asof 2026-10-21** (the 12h wiki-consensus refresh). Per standing practice a same-day snapshot is a valid baseline, so no column is PENDING.
- **Caveat:** the snapshot has already rolled META to `lrq 2026-09-30`, so 1FQ = Q4-26E. Q3 is compared against the Street bars logged on the page (BofA / Bernstein panels).
- **Basis:** FY fields use 1FY/2FY/3FY. CY sums are not used, because they embed pre-print consensus.

**House baselines:**
- META: `Modelo Meta pós 2Q26.xlsm` (saved 2026-10-12), via `_data/house.json`.
- No house model exists for MU or SPCX.

## DIVERGES (alpha candidates)

| Ticker | Metric | New datapoint | Baseline (prior wiki / house / BBG) | Gap | Note |
|---|---|---|---|--:|---|
| META | FY26 capex | Guide $135-145bn, narrowed from $130-145bn (Meta PR, 10-21) | **House $150.7bn**; BBG 1FY $139.9bn | House **+$5.7bn above the TOP** of the guide | The house is the outlier. The model needs a capex bridge before the FY27 work. |
| META | FY26 total expenses | Guide $175-179bn, including the $9.89bn AG charge (PR) | **House $162.0bn** | House −$13-17bn; **−$3-7bn ex-charge** | The charge explains ~$10bn. The rest is a house opex gap. |
| META | Q3 capex (incl. finance-lease principal) | $34.91bn (PR) | Street $41.6bn, BofA $42.7bn, Bernstein $42.0bn (page) | **−16% vs Street** | Timing or basis? Not explained in the PR; it is the call question. The implied Q4 is $49.2-59.2bn vs BBG 1FQ $49.8bn, so consensus sits at the low end of the implied range. |
| META | Q4-26 revenue guide | $73-76bn, midpoint $74.5bn | BBG 1FQ $73.57bn; BofA expected guide $71.5-74.5bn; desk ~$74.5-75bn | Midpoint **+1.3% vs BBG**; the guide's low end sits at BofA's expected midpoint | Above the sell-side bar, in line with the desk bar. |
| META | FY27 capex (Bernstein) | $230.5bn (Bernstein, 10-20) | BBG 2FY $201.9bn; house $200.0bn; BofA $205bn (from $192bn) | **+14% vs BBG / house** | A new Street-high-side mark. The company gave no FY27 number, so it is unresolved. |
| META | FY27 EPS (Bernstein) | $33.21, from $36.68 | BBG 2FY $37.87; house $35.63 | **−12% vs BBG**, −7% vs house | Outperform kept, PT $800 vs BBG consensus $816 (below consensus despite the positive rating). |
| SPCX | WF 2027E revenue | $230.4bn, from $123.3bn (WF model 10-21) | BBG 2FY $154.2bn | **+49%** | Driven by AI/compute: the Anthropic line was repriced from $20m to $40m/MW, and other compute went $26.2bn → $101.3bn. |
| SPCX | WF 2027E capex | $466.4bn, from $301.0bn | BBG 2FY $231.7bn | **+101%** | It was already +61% before this revision (10-20 recon). |
| SPCX | WF 2027E EPS | $8.83, from $3.27 | BBG 2FY $2.58 | **3.4x** | The largest EPS gap on the page. |
| SPCX | WF YE27 compute | 10.75GW, from 7.28GW | Musk ~13GW (Q3 call); MS 4.9GW / JPM 6.4GW (page) | below management, above the Street | WF moved toward the guide. |
| MU | DRAM supply balance | *"we actually don't see a time when it comes into balance"* (DeBoer, answering Bajarin) | The page's "peak is settled, trough is the fight" debate (GS/DB); the 2028 down-year in BofA's TAM | qualitative | Management widens "tight through CY27-28" to no balance at all. This is management talking its book, not a forecast, but it is the most aggressive duration claim on the page. |

## CONFIRMS (no action)

| Ticker | Metric | New datapoint | Baseline | Note |
|---|---|---|---|---|
| META | Q3 revenue | $64.60bn +26% | Guide $61-64bn; Street $63.3bn (BofA panel) / Bernstein consensus $63.31bn; BofA $63.8bn; Bernstein $64.06bn; desk ~$64bn | Beat: +0.9% vs the guide's high end, in line with the desk bar. 9 of the last 9 quarters came in above the guide midpoint. |
| META | Q3 GAAP EPS | $3.83 ($7.40 ex-charge) | BofA $3.79 incl. the accrual | In line once the charge is matched. |
| META | FY26 capex vs BBG | Guide midpoint $140bn | BBG 1FY $139.9bn | In line. Only the house model diverges (above). |
| META | 2027 framework | Qualitative only: "sustain strong overall revenue growth throughout 2027"; RL losses ~$15bn | BofA: "no formal 2027 capex guide… qualitative framework" | BofA called it. The desk's FY27 opex $210-225bn / capex $225-250bn frame is neither confirmed nor refuted. |
| META | Capital raise | New non-voting Class C stock, effective 2027-01-19, explicitly "for capital raising" | UBS Dwyer: "bracing for some sort of capital raise" (10-16) | The desk read on the early print date confirmed in structure. No issuance was announced. |
| MU | 1-delta node timing | Volume ramp 2H CY27 (Boise) | Existing page marks 2H27 | Confirmed. Density gain is mid-20s %. |
| MU | 4F² DRAM | Rejected; "3D DRAM coming in instead of 4F²" | Satya Kumar 10-16 "a tool in the toolkit"; ASML-call participant (10-21) said Micron skips it | Hardened. The old framing went to the Changelog. |
| GOOG | Data-center lease guarantee book | $43.8bn at 6/30/26 (Cantor, from filings) | ~$44bn on the page | Ties. The construction-loan vs lease-backstop conflict with Bernstein's 10-20 lawyer is logged as OPEN on GOOG/ai-compute-deals. |

_No BBG-dependent row is PENDING._
