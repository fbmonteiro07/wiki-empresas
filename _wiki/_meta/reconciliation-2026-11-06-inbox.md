# Reconciliation — /run-inbox 2026-11-06

_This report checks each new quantitative datapoint from tonight's sources against three baselines: (1) prior wiki marks; (2) Capstone house models; (3) BBG consensus._

- **BBG is LIVE tonight.** Pulled 2026-11-06 ~23:50 BRT via `E:\bloomberg_api` (`bdp`, `BEST_FPERIOD_OVERRIDE` 1FY/2FY/3FY, plus 1FQ for ABNB). For SPGI, MCO and MSCI (December FY), 1FY/2FY/3FY = 2026/27/28. The on-disk `estimates.json` is also asof 2026-11-06.
- **House models:** none of tonight's quantitative names has a Capstone house model (SPGI, MCO, MSCI, SK hynix, Samsung, ABNB, IREN, Riot, ORCL credit). GOOG/AMZN/META have house models, but the JPM call carried credit views only, with no equity estimates (the recording ends at the first Q&A).
- **Private names** (OPENAI, ANTHROPIC) were checked against prior wiki marks only.
- **Sources tonight:**
  - Barclays SPGI/MCO/MSCI, "2027e another healthy issuance year" (2026-11-02).
  - J.P. Morgan Hyperscalers Joint Equity & Credit call, Chatterjee/Spear (2026-11-04).
  - NH Investment & Securities 2027 Korea strategy call via BTG, Cho/Kim (2026-11-04).
  - CyberEdge expert call via BTG, Meshel (2026-11-05).
  - Airbnb Q3 2026 call (2026-11-05).
  - IREN Q1 FY27 call, Bloomberg copy (2026-11-05).
  - Jefferies Washington Strategy (2026-11-04).
  - Arizton Global Hyperscale DC market report.
  - Capstone Brazil AI-DC note (2026-11-06).
  - Five podcasts: Altman, Riot CEO Les, Hinojosa/Abbott, Suleyman (re-upload), Hassabis.

## DIVERGES (the alpha)

| Name | New datapoint (source) | vs prior wiki | vs house | vs BBG (live 11-06) | Read |
|---|---|---|---|---|---|
| **SKHYNIX** | NH (Cho/Kim, 11-04): P/E **4.3x 2026 / 2.9x 2027**, P/B 2.7x; 2027 earnings growth "only 17%" | Page had no NH mark | none | Px ₩1,132,000; 1FY EPS **₩359,816**, 2FY **₩535,836** → **3.1x / 2.1x**. NH's multiples imply EPS about **27-28% below consensus** in both years (≈₩263k / ₩390k), unless NH used a different price date. BBG 2FY/1FY growth is **+49%**, against NH's "17%". NH's own 4.3x → 2.9x implies about +48%, so the "17%" is internally inconsistent | **NH sits well below the Street on hynix earnings, or its 17% is a different line (KOSPI-level).** Use this as a prompt to verify, not a verdict (memo: memory-complex consensus has been wrongly called inflated before). BBG PT ₩3.17m (+180%) is a screen flag; recheck the panel. |
| **SAMSUNG** | NH (11-04): P/E **5.1x**, P/B 2.1x; shareholder returns ~₩40tn; new rule cancelling treasury shares within 1.5 years | Page: "~₩40tn bonus stock should not be canceled" (now ⚠ vs the new rule) | none | Px ₩188,700; 1FY EPS **₩46,845** → **4.0x**. NH implies EPS about **22% below consensus** | Same pattern as hynix: the Korea strategist is materially below the sell-side single-name consensus on memory earnings. |
| **Arizton (theme ai-datacenter-power)** | US hyperscale MW added: **10,010 (2026) / 10,741 (2027)**; global 17,066 / 19,475. Investment $440bn (2025) → $903bn (2031), 12.7% CAGR. US build cost $9-14M/MW | Bernstein **+19 IT-GW** US 2027; Jefferies **18.0 IT-GW** | none | n/a | **Arizton is about 40% below the broker range** for US 2027 additions. Basis differs (hyperscale operators only, ≥15 MW per facility, no colo/neocloud), so it is the conservative bound, not a contradiction. Do not net it into the broker series. |
| **ORCL** | JPM (Chatterjee, 11-04): the 6 GW plan needs **~$220bn** of capital. **~50%** comes from other parties' sources (vendor financing, customer hardware, prepayments); **~$90bn** is internally generated | Investor Day release: "no size is given" | no ORCL house model | n/a (credit/funding, not a consensus field) | First sell-side sizing of the non-balance-sheet funding share. JPM credit stays **Overweight**; S&P/Moody's action is the watch item. |
| **META** | JPM (Spear, 11-04): **$356bn** uncommenced leases; S&P negative outlook 10-30 with a 1x net-leverage downgrade trigger | WSJ **$347bn** (08-17) | house model has no lease line | n/a | Leases are still growing (+$9bn since August); the 1x trigger is now a live constraint. Credit Neutral is unchanged. |
| **AVGO** | JPM (11-04): S&P counts a peak of **$43bn** of contingent liabilities (customer-financing guarantees) as debt in FY28 and removed its positive outlook | 🆕 nothing on the page | AVGO house model has no guarantee line | n/a | New balance-sheet lens on the XPU financing structures; feeds the NVDA/AVGO financing debate. |
| **Riot / ANTHROPIC (ai-compute-deals)** | Les (11-04, sponsored interview): Corsicana **910 MW / ~$28bn / 15 years / $130/kW-month NNN**, $6M/MW Riot capex. Data-centre NOI **$227M 2H27 → $701M 1H28 → ~$2.3bn 2029** | ~1 GW Corsicana **LOI** (Bernstein 08-11). Rockdale $9.1bn / 20 years | none (RIOT uncovered) | RIOT 3FY (FY28) EPS still **−$0.30**, px $16.71, cons PT $30.9 | The LOI is now a signed lease, slightly smaller (910 MW vs ~1 GW). Management's FY28 NOI path versus a still-negative FY28 consensus EPS suggests the Street is not crediting it. They can't be netted (D&A, interest, mining), so treat this as a prompt only. |

## CONFIRMS (no action)

| Name | New datapoint (source) | vs prior wiki | vs BBG (live 11-06) | Read |
|---|---|---|---|---|
| **SPGI** | Barclays (11-02): OW, PT **$553 → $572**. EPS 26E/27E/28E **$17.74 / $20.40 / $22.95** (27E/28E were $20.85 / $23.39). 2027 Ratings growth cut to 7.6% (from 11.9%) | No prior Barclays mark | EPS 1FY/2FY/3FY **$17.98 / $20.18 / $22.82**, i.e. −1.3% / +1.1% / +0.6%. Cons PT **$529** (Barclays +8%); px $467.80 (+22% to the Barclays PT) | Even after cutting 2027 issuance, Barclays sits on the consensus line. The PT premium is multiple (~25x FY28E), not earnings. |
| **MCO** | Barclays: OW, PT **$575** unchanged. EPS 26E/27E/28E **$16.63 / $18.96 / $20.91** (27E/28E were $19.77 / $21.72). MIS 2027 growth 7.4% (from 12.1%) | No prior Barclays mark | **$16.77 / $18.65 / $20.70** (−0.8% / +1.7% / +1.0%). Cons PT **$556** (+3%); px $505.67 | In line. |
| **MSCI** | Barclays: OW, PT **$735 → $760**. EPS **$19.79 / $22.34 / $25.22** unchanged | No prior Barclays mark | **$19.67 / $22.50 / $25.66** (+0.6% / −0.7% / −1.7%). Cons PT **$690**; the Barclays PT is **+10% above** consensus and +19% above px $641 | EPS in line; the PT is a Street-high-type premium on multiple (~30x FY28E). |
| **ABNB (on BKNG)** | Airbnb Q3 (11-05): revenue $4.9bn (+19%), GBV $27.7bn (+21%), adj. EBITDA $2.5bn (52%). Q4 revenue guide **$3.22-3.28bn**; FY26 adj. EBITDA margin ~36%; new $12bn buyback | The 11-05 shareholder-letter row is already on BKNG.md | 1FQ revenue **$3,247m** = guide midpoint (post-print consensus); 1FY EPS $5.57 | Guide and consensus have converged after the print. The read-through to BKNG is the hotels push (an ex-Booking.com executive is now CBO) and agent bookings still non-material. |
| **AMZN** | JPM (11-04): ~$18bn term loan fully drawn; $62bn USD + $36bn non-USD issued in 2026 | 10-Q **$17.5bn** term loan | n/a | Ties to the 10-Q. JPM credit Overweight unchanged. |
| **Hyperscaler credit (5 names)** | JPM credit calls AMZN/GOOG/ORCL **OW**, META **Neutral**, MSFT **UW**; USD issuance $232bn YTD (AMZN 62 / GOOG 45 / ORCL 35 / META 40 / MSFT 25); 2027 spend for 6 names incl. SpaceX "likely above $1.5T" | July JPM call: identical ratings. Pershing ~$1.5tn | n/a | **No rating changes since July.** The issuance mix is new detail. The $232bn is USD-only, so it is not comparable with Barclays' ~$285bn all-currency year-end figure. |
| **IREN** | Q1 FY27 call (Bloomberg copy): Horizon 1 built in 14 months (vs JLL 18); $19bn raised in 12 months incl. $6.5bn GPU financing at 6-9.5%; ~$25bn of DC + GPU assets by June 2027 | Page (built today from the Quartr copy of the same call) had $10bn of DC assets only | 1FY EPS **−$2.05**; cons PT $60.6 vs px $21.64 (screen flag: recheck the panel) | Same call, so additional datapoints, not new information. |
| **OPENAI** | Altman (11-03): India "biggest market" (metric garbled, so not a user count); compute bet dated ~Aug-2022 | 1.2bn WAU (DevDay 09-29) stands | n/a | Qualitative; nothing superseded. |
| **GOOG** | Hassabis (11-05): 6-8 frontier offerings, 3-6 month leads, open source 6-12 months behind; coding agents 3-5x engineer productivity | Consistent with the page's "model is not the moat, GCP/TPU is" | n/a | Exec colour, not a number to model. |
| **Texas policy (ai-datacenter-power)** | Hinojosa (10-31, candidate): moratorium = "pause on approvals" / "new permits"; DC sales-tax exemption costs ≥$1bn/yr; electricity-rate freeze. Jefferies: Democrats won every governor race in its DC states (NV, GA, OH, IA, TX) | Theme: 21 GW (16 credible) under construction and grandfathered; WBK "more nuanced" | n/a | Confirms grandfathering of construction already under way. Gavin Baker's "allowed to finish… 2027-2028, union labor" is **not in the primary** (his paraphrase). |

## Not reconciled (qualitative / unverified)
- CyberEdge expert claims (2,700 critical vulnerabilities, +34%, $2.2bn crypto theft) are unsourced and were kept off the incident ledger.
- Capstone Brazil note: internal synthesis of third-party sources (ONS / Scala / JLL / FGV). No consensus baseline.
- Suleyman 92NY: a re-upload of the 10-12 taping, so no new datapoint.
