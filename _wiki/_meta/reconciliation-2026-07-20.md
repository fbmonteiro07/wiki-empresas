# Reconciliation — 2026-07-20 run

_New quantitative datapoints from the 18-source inbox batch, checked vs three baselines:_
_(1) prior wiki comments (on disk) · (2) Capstone house models (`house.json`, asof 2026-07-20) · (3) BBG consensus._
**BBG column = PENDING** — Bloomberg Terminal offline at run time (ConnectTimeout / Capstone VPN down). Re-run `py E:/.claude/scripts/fetch_estimates.py <tickers>` then `_wiki/_tools/build_snapshot.py` once the Terminal is back. No web data substituted for consensus.

Basis flags matter below: GAAP vs non-GAAP EPS, calendar vs fiscal year, and post-split per-share bases are noted where they drive the gap.

---

## DIVERGES (the alpha)

| Name | New datapoint (source, date) | vs prior wiki | vs house model | vs BBG | Read |
|---|---|---|---|---|---|
| **ASML** | Bernstein OP €2,500 / ADR $2,859 (40x on €62.6 Q5-8 EPS) — *(Bernstein "WFE/AI-GW", 2026-07-20)* | Morgan Stanley OP €1,930 (35x on €56.42 FY28e) SAME DAY *(MS NDR, 2026-07-20)* → **~30% same-day PT gap**, both OW/Top-Pick | no house (ASML not modeled) | PENDING | **Sell-side internally split ~30%** on ASML — the gap is target multiple (40x vs 35x) × out-year EPS base. Watch which base the Street median sits on when BBG returns. |
| **GOOG** | DB FY27 Cloud **~$190-195bn vs Street ~$142bn** (+35% above Street); FY27 capex $325bn (from ~$250bn) *(DB "Aiming for the Clouds", 2026-07-20)* | page already carried GOOG cloud > Street (prior recon 07-16 flagged "house 2027 > BofA clean-basis") | house 2027 rev $641bn / capex $310bn — **house corroborates DB (both above Street)**; house capex $310bn slightly below DB $325bn | PENDING | **House + DB both materially above Street on Cloud** — the standing GOOG edge. DB EPS $14.24 (GAAP) sits below house $16.20 (basis/segment mix — verify vs BBG). |
| **NVDA** | Bernstein 27E EPS $12.52 (OP $315) *(2026-06-17)*; MS ~22x CY27 EPS $13.08 *(MS Memory, 2026-07-20)* | in-line with the Street cluster on page | **house 2027 EPS $15.44 GAAP / $15.49 non-GAAP — ~18-23% ABOVE the Street $12.52-13.08** | PENDING | **House is well above consensus on NVDA out-year EPS** — genuine positive edge; size it against the BBG median when back. |
| **AVGO** | MS values at 28x CY27e ModelWare $17.92 / ~26x non-GAAP $19.59 *(MS Memory, 2026-07-20)* | consistent with page | **house 2027 EPS $21.07 — ~10-18% ABOVE the MS $17.92-19.59 base** | PENDING | House above Street on AVGO out-year EPS too (AI-semi ramp $132bn'27). Positive edge; confirm basis vs BBG. |
| **TSM** | JPM: 2026 rev guide **"40%+ and could end higher"**, capex $62bn midpoint *(JPM post-2Q, 2026-07-16)* | prior recon 07-16: "TSM house trails print" | house 2026 rev $165bn on 2025 $122bn = **+35%** — **house rev growth BELOW the guided 40%+** | PENDING | **House 2026 rev likely too conservative vs the 40%+ guide** — carry-over gap, now larger. House GM ~66% ≈ cons 2027 67.6% (fine). |
| **META** | JPM 2027 capex **+42% to ~$200bn** *(JPM joint call, 2026-07-20)*; Citrini ~14GW/3yr | page capex was lower | **house 2027 capex $170bn — ~$30bn / ~15% BELOW the raised JPM ~$200bn** | PENDING | **House capex trails the new sell-side** — update risk to house FCF ($-23bn'27 would deepen). BofA PO $835 (24x) vs house EPS $38.24. |
| **AMZN** | Redburn Neutral **$230** (AWS gross margin -520bp, Gen-AI book ~12%) *(R&Co Redburn, 2026-07-20)* | **cluster-low** vs BofA $310 / JPM $330 / GS $335 / Barclays $330 | no house | PENDING | **First hard margin-compression short on the page** — directly contests the AWS-margin-inflection narrative (SemiAnalysis +213bp). The live debate. |
| **MSFT** | Redburn Neutral $400, Gen-AI book ~13% (IC GM -680bp); JPM credit **DOWNGRADE to UW** (debt issuance imminent) *(both 2026-07-20)* | page constructive on Azure re-accel | no house | PENDING | Margin-compression + funding-supply bear case vs the Azure-reaccel bull — two-sided into the 07-29 print. |
| **ORCL** | Redburn **SELL, PT $155→$110** (database bet won't ramp; cloud-DB +29% vs 50%+ implied) *(2026-07-20)*; JPM credit **UPGRADE to OW** | first bear-rated note on the page (prior $155 moved to Changelog) | no house | PENDING | **Equity SELL / credit OW split** — Street-low equity PT while credit turns constructive on rel-val. Sharpest divergence in the hyperscaler set. |
| **ARM** | Bernstein OP **$500 (from $300)**, $223bn 2030 TAM *(2026-06-17)* | vs Octahedron **SHORT** ("fake bottleneck") + GS $150 / Redburn $130 | no house | PENDING | **Widest PT dispersion in coverage** ($130-500) — Bernstein's TAM-expansion bull vs the fund short. Pure alpha/opinion split. |
| **INTC** | Octahedron (fund) FY-next EPS **$5-6.50**, path to $150 *(2026-07-15)* | vs Bernstein MP $100, EPS 27E only **$1.50** *(2026-06-17)* | no house | PENDING | **~3-4x EPS gap** between the fund's non-consensus earnings-power call and sell-side — the fund is underwriting a mis-modeled turnaround. Track against the print. |
| **SNDK** | Bernstein OP **$3,000** vs MS OW **$1,750** SAME DAY *(2026-07-20)* | both new to page | no house | PENDING | ~$1,250 PT dispersion = the NAND 2028-durability / cycle-normalization debate (Bernstein sees LTAs de-risking the cycle → higher through-cycle EPS). |
| **QCOM** | Citrini FY29 non-handset guide **$22bn→$40bn** (HBC/AI200-300) *(2026-07-20)* | vs JPM "staying on the sideline," margin-dilutive DC ramp *(2026-07-16)* | no house | PENDING | Newsletter DC-pivot bull vs sell-side skepticism — the datacenter-optionality debate on a mislabeled mobile name. |

---

## CONFIRMS (no action)

| Name(s) | New datapoint | Confirms |
|---|---|---|
| **Hyperscaler capex '27** | AMZN ~$300bn (JPM/BofA), GOOG ~$300-325bn (DB/JPM), META ~$200bn (JPM) | Broad capex-up '27 already on hyperscaler-capex theme (Mizuho $846B/$912B, MS $1.2/1.4t, Citi) — new notes cluster in the same band. Capex-up consensus intact; FCF-vanishing thread reinforced. |
| **ASML capacity** | Low-NA EUV 85 (FY27) / 110 (FY28), High-NA 4-5 rev-rec FY26 | Triple-sourced same window (didier 07-15 + MS 07-20 + Bernstein 07-20) — no divergence on the capacity gate. |
| **Memory pricing** | DC memory +25%+ q/q (MS); SIA DRAM +70% 1q / +40% 2q; DRAM +60%/3mo (BofA) | Confirms the DRAM-shortage / memory-supercycle thesis on hbm-memory + MU/SNDK. MU MS OW $1,200 **reaffirmed** (already on page — no drift). |
| **TSM packaging** | CoWoS numbers "revised up ~3-4x this year"; adv-packaging 10%→low-teens % rev | Confirms CoWoS tightness on cowos-packaging (demand>supply 2-3yrs). |
| **AMD** | Bernstein OP $600 (already logged); server-CPU TAM $120→$200bn; BofA TAM $1tn→$1.5tn | PT already on page — CONFIRM; only the EPS series + TAM-doubling are net-new color. |
| **NVDA rating** | Bernstein OP $315 (already logged from prior ingest) | CONFIRM — not re-drifted; source link added. |
| **AAPL** | BofA higher ASPs (Pro Max +$200), foldable ~15M, Siri catalyst | Confirms the house ASP-up thesis (house ASP $874→$946→$1,021; units 240→267→280→286). |

---

## Follow-ups
- **Re-run BBG** once Terminal/VPN is back: `fetch_estimates.py NVDA GOOG AVGO TSM META AAPL ASML AMD ARM MU ORCL MSFT AMZN INTC SNDK` → `build_snapshot.py` → resolve the PENDING columns above (the house-above-Street reads on NVDA/AVGO/GOOG and the house-below reads on TSM/META capex are the priority placements).
- **House-model update candidates**: TSM 2026 rev (trails 40%+ guide), META 2027 capex (trails ~$200bn).
- **AMZN ExpertCall (2026-03-12)** figures are Q1'26 vintage — excluded from the post-print intra-quarter tables; not reconciled as current.
