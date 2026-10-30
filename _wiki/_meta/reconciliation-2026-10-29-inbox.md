# Reconciliation — /run-inbox 2026-10-29

_Scheduled 23:00 run. 10 inbox files: 8 podcast summaries (4 backfill) + 2 PDFs (Amazon Q3 2026 earnings release, 2026-10-29; UBS · Keirstead "Microsoft Corp. — Azure/OpenAI Drives the Upside", 2026-10-29). Baselines: (1) prior wiki values on the page, (2) Capstone house models (`_data/house.json`, asof 2026-10-29 — **no house model for AMZN, MSFT, CSCO**), (3) BBG consensus from the on-disk snapshot `_data/estimates.json` (**asof 2026-10-29**). The live `bdp` pull failed (Terminal not logged in: `localhost:8194` refused), so the snapshot is the baseline. It is a same-day pull and taken BEFORE the AMZN print, so it is the pre-print consensus. No web data was substituted._

Podcast numbers are commentary, not estimates. Only those that collide with a filed or modelled number are reconciled below.

## Where the new data DIVERGES

| Ticker | New datapoint (source, date) | vs prior wiki | vs house | vs BBG consensus (snapshot 10-29) | Read |
|---|---|---|---|---|---|
| **AMZN** | **3Q26 OI $28.1bn, 13.9% margin** (Amazon release, 10-29) | guide $22.5–26.5bn; Street $26.0bn; Bernstein $28.0bn; buy-side bar $27.5bn+ | no house model | Q3 EBIT cons **$26.06bn** (10-28 snapshot) → **+7.8%** | Above the top of the guide, and above the buy-side bar too. The beat is in OI, not revenue. |
| **AMZN** | **3Q26 AWS +39.3%, $45.98bn; AWS OI $17.8bn (38.7% margin)** | cons ~37.4%; buy-side bar **42%**; AWS margin 39.4% in Q2 | — | — | It beats consensus but misses the buy-side whisper by about 3pt, and the margin slips about 70bp q/q. That tension is the print. |
| **AMZN** | **3Q26 PP&E purchases $77.3bn gross** | pre-print $57.9bn (Visible Alpha via Jefferies) / $60bn (BofA) | — | — | **+29–33% vs the pre-print marks.** FY26 "~$220bn" is reiterated; if that maps to the 9M gross line ($175.7bn), Q4 is only about $44–48bn (house arithmetic; the basis is undefined in the release, so check it on the call). |
| **AMZN** | **4Q26 guide: revenue $240–247bn, OI $28.5–33.5bn** | — | — | 1FQ cons rev **$244.5bn** (midpoint −0.4%); EBIT **$33.0bn** (midpoint $31.0bn, **−6%**; the top of the range is only 1.5% above cons). **Post-print BBG (asof 2026-10-30):** rev **$244.9bn** (midpoint $243.5bn, −0.6%; street-high $255.9bn); EBIT **$32.78bn** (midpoint **−5.4%**, top of range +2.2%; street-high $37.8bn) | Revenue is in line and the OI guide sits below the Street. A day after the print, consensus EBIT has eased only ~$0.2bn, so the gap holds: the Street sits at the upper third of the OI range, not at the midpoint. |
| **AMZN** | **3Q26 GAAP EPS $1.89** | page Street mark $1.97 | — | BBG Q3 EPS cons **$2.35** (10-28 snapshot) | **The two consensus EPS bases differ by $0.38.** The BBG EPS line is contaminated below the line (investment gains; see the GOOG precedent), so **reconcile at EBIT, not EPS.** Q3'25 EPS had $9.5bn of Anthropic gains; Q3'26 names none. |
| **AMZN** | **TTM FCF −$42.4bn** (vs −$7.6bn last logged) | −$7.6bn (Q2) | — | — | The capex step-up moves straight into FCF. Q3 standalone FCF is about −$33.5bn (house arithmetic: OCF $42.4bn − net PP&E $75.9bn). |
| **MSFT** | **UBS · Keirstead PT $700** (from $675, which was set 10-14 and never logged on the page; the last logged UBS mark is $525, 07-30), 23x CY28 non-GAAP | UBS $525 (07-30) → $700 | no house model | PT cons **$632.3** (hi $870) → **+10.7%** | It joins the upper half of the Street range. UBS cut the multiple 25x → 23x but raised the numbers. |
| **MSFT** | **UBS FY27E all-in capex $217.6bn; FY28E $273.4bn; FY29E $324.4bn**; CY26 $170bn | UBS 07-26 FY27 $261bn all-in ($209.0bn cash + $51.6bn leases) | — | 1FY capex cons **$191.0bn**, 2FY **$221.2bn** | **Basis gap:** UBS is all-in (P&E $195.7bn + leases $21.9bn); BBG `BEST_CAPEX` is most likely cash. On P&E alone UBS is +2.5% vs cons for FY27, so not a real divergence. Most of the cut from UBS's 07-26 number is in the lease leg ($51.6bn → $21.9bn). |
| **MSFT** | **OpenAI ≈30% of Azure revenue ($10bn of F1Q27)** (UBS) | 10-Q: OpenAI revenue $10.0bn in the quarter (~11% of total revenue), on the page 10-28 | — | — | Same $10bn as the 10-Q, now expressed on an Azure denominator. **Concentration is the new debate** (Signal: Demand cover ✗). |
| **CSCO** | **FY25 hyperscaler AI orders $2.3bn vs $1bn target; FY26 $9.3bn vs $5bn** (Jeetu Patel, exec, A Bit Personal, 10-29 — podcast) | page ">$2B" FY25; $9.3bn FY26 | — | — | It refines the base: the FY26 multiple is **~4.0x, not the 4.5x on the page** (house arithmetic). These are orders, not revenue. |
| **OPENAI** | **~$20bn/GW target, 5-yr TCO** vs host Collison's ~$70bn (Altman, Cheeky Pint, 10-29 — podcast) | Hock Tan $20–30bn/GW "sustained" chip content; Huang ~$50bn/GW build; Patel "north of $60bn" | — | — | **A new basis: a 5-yr TCO target, GW type unstated.** Never net it against the build-cost or chip-content series (see the `$/watt` unit hazard). |

## CONFIRMS (no action)

| Ticker | Datapoint | Baseline it matches |
|---|---|---|
| AMZN | 3Q26 revenue **$201.9bn** (+12%, +13% ex-FX; Prime Day ~400bp) | guide $197–202bn (top end); Street $202.0bn; BBG Q3 cons $202.26bn (10-28 snapshot): **in line** |
| AMZN | FY26 capex "~$220bn" reiterated | BBG CY2026 capex $216.2bn (+1.8%) |
| AMZN | AWS growth ">40% in 2027 and 2028" (Jassy, release) | Jassy a16z 10-23: "27 largely sold out"; MS AWS 47% case. Directionally confirmed; first numeric multi-year management guide |
| MSFT | UBS FY27E/FY28E EPS **$20.30 / $24.15** | BBG 1FY **$19.96** (+1.7%) / 2FY **$23.85** (+1.3%). UBS's FY29E $28.27 is **below** BBG 3FY $28.99 (−2.5%) |
| MSFT | UBS FY27E/FY28E/FY29E revenue $399.1 / $479.7 / $568.3bn | BBG $392.9 / $471.2 / $572.1bn (+1.6% / +1.8% / −0.7%) |
| MSFT | UBS CY26 capex $170bn | MSFT's own 10-28 guide ("~$170bn from ~$175bn") |
| MSFT | Suleyman: compute "1,000-fold" over 3 years, "100 to 1,000x" over the next 3 (The Builders, 10-29 — podcast) | qualitative industry scaling, no $ or GW basis; not reconciled |

## Not reconciled / pending

- **AMZN earnings call transcript is not on disk.** AWS backlog, AI/Trainium run-rates, 2027 capex and the capex basis all wait for it, and the Management-commentary evolution table has no Q3 column yet.
- ~~**AMZN 4Q guide vs BBG** uses the 10-29 snapshot's 1FQ (Q4-26E). The snapshot was pulled pre-print, so post-print revisions are not captured. Re-run `/wiki-consensus` once the Terminal is back.~~ Done 2026-10-30: re-placed on the post-print 1FQ (row stays in DIVERGES). Only one day of revisions is in, so re-check next week.
- OPENAI / ANTHROPIC podcast numbers (Navier-Stokes "~$10m-ish", "100s of millions" math programme, ">700 proofs"; Suleyman "thousands" of agents vs METR ~1,200) have no consensus baseline. Prior-wiki check only; METR's count stands.
- Altman's memory-maker "~$100bn FCF each" is a round number with no named company. Not adopted on hbm-memory.

_BBG column resolved 2026-10-30 — estimates.json asof 2026-10-30._
