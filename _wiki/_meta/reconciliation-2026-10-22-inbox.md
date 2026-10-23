# Reconciliation — /run-inbox 2026-10-22 (scheduled 23h, unattended)

Sources:
- **UBS** · Stephen Ju, META 3Q26 earnings group callback, 2026-10-22 (machine transcript; host UNCONFIRMED).
- **Wells Fargo Securities** · Gawrelski, `META_WFS_Distribution_102126.xlsx` — post-print model (3Q26 actual), 2026-10-21.
- **Jefferies** · Gallo / Thill et al., "Sneak Peek Into Cyber CY27 Top Line Estimates", 2026-10-22.
- **Blackstone** Q3 2026 earnings call, 2026-10-22 (Bloomberg final transcript).

**BBG baseline:** live wrapper not attempted at 23h (the Terminal session is routinely logged out at this hour); I used the on-disk snapshot `_data/estimates.json`, **asof 2026-10-21** (one day old, post-META print). FY fields use 1FY/2FY/3FY (CY sums embed pre-print consensus for reported quarters). META is rolled to `lrq 2026-09-30`, so 1FY = FY26, 2FY = FY27, 3FY = FY28. CRWD/OKTA (Jan FYE): 1FY = FY27, 2FY = FY28. PANW (Jul FYE): 1FY = FY27. NET (Dec FYE): 1FY = FY26, 2FY = FY27.

**House baselines:** META — `Modelo Meta pós 2Q26.xlsm` (saved 2026-10-12) via `_data/house.json` (raw_rows read; parsed FCF sign not used). No house model for CRWD / PANW / OKTA / NET.

**Basis caveat (META EPS):** WFC prints **GAAP diluted EPS** (FY26 includes the $9.89bn AG charge); BBG consensus is the adjusted/comparable basis. The FY26 EPS gap is mostly the charge; the FY27/28 gaps are not.

## DIVERGES (alpha candidates)

| Ticker | Metric | New datapoint | Baseline (prior wiki / house / BBG) | Gap | Note |
|---|---|---|---|--:|---|
| META | FY27 capex (incl. finance-lease principal) | **WFC $249.3bn** (from $246.2bn, model 10-21); UBS's perceived buy-side *"about $250 billion"* (10-22) | BBG 2FY **$201.9bn**; house **$200.0bn**; Bernstein $230.5bn, BofA $205bn (page) | **+23.5% vs BBG**, +24.7% vs house | The buy-side bar (~$250bn: WFC, UBS, JPM's $250-275bn) is now ~$50bn above both the sell-side consensus and the house. The 4Q call (late Jan) is the resolution. House capex line is the largest open gap on the page. |
| META | FY27 EPS | **WFC $32.62 GAAP** (from $31.18); UBS 2027 EPS raised ~4% (level not given) | BBG 2FY **$37.87**; house **$35.63** | **−13.9% vs BBG**, −8.4% vs house | Same direction as Bernstein ($33.21, 10-20) and the buy-side "$32, $33" (WFC call, 10-22): the Street EPS line still embeds ~$200bn capex / lower D&A. GAAP vs adjusted explains little in FY27 (no charge). |
| META | FY27 total expenses | WFC **$212.3bn**; UBS's perceived buy-side OpEx *"close to $220 billion"* | House **$202.5bn**; desk bar $210-225bn (page) | +4.8% (WFC) / ~+8.6% (buy-side) vs house | House opex sits below every buy-side mark; same gap as the FY26 opex gap flagged 10-21. |
| META | FY28 capex | UBS *"close to 300"* (10-22); WFC $198.8bn | House $270.3bn; BBG 3FY $218.2bn | UBS +37% vs BBG; **WFC −26% vs house** | Houses split wide on 2028: WFC models a capex DECLINE in 2028 (EoP power 18.6 GW; capacity adds 7.0 → 4.5 GW), UBS models a further rise. The house sits between. |
| META | Equity financing | UBS: ~$250bn over three years, **~$75bn in 1Q27** (in model); WFC call: $60-80bn over 12 months ($40-50bn equity) — but **WFC's model carries $0 equity issuance** | Page: Class C effective 2027-01-19, "no specific financing plans" (Li) | n/a | Two houses now put a 1Q27 raise in the $60-80bn range; one of them has not put it in its model, so its EPS ($32.62) is pre-dilution. |
| META | FY28 compute resale revenue | WFC **$10.0bn** (from $20.0bn) | Page: WFC had zeroed 2027 and kept $20bn in 2028 (10-05) | −50% | The only house with dollars on Meta Compute resale halves it again. |

## CONFIRMS (no action)

| Ticker | Metric | New datapoint | Baseline | Note |
|---|---|---|---|---|
| META | FY27 revenue | WFC $314.9bn (ad +21.8%, +22.5% cc) | BBG 2FY $306.4bn (+2.8%); house $308.1bn (+2.2%) | Within 3%. WFC's model matches its 10-22 call (22-23% base). |
| META | 4Q26 revenue | WFC $75.77bn | Guide $73-76bn; BBG 1FQ $73.57bn | Top of the guide; +3% vs BBG. UBS: guide "stronger than we had hoped". |
| META | FY26 capex | WFC $136.7bn | Guide $135-145bn; BBG 1FY $139.9bn | Low half of the guide (implies a 4Q of ~$53.7bn). The house ($150.7bn) remains the outlier (10-21 DIVERGES row stands). |
| META | FY28 EPS / revenue | WFC $39.83 / $382.8bn | House $39.34 / $369.7bn; BBG 3FY $46.65 / $365.0bn | WFC ≈ house on EPS (+1.2%); both ~15% below BBG. |
| META | $700bn in the 8-K / 14C | UBS: maximum raise before Zuckerberg's voting power is affected | WFC call (10-22): "control-dilution ceiling, not a spend or raise plan" (page) | Two houses read it the same way. |
| CRWD | FY28 revenue consensus | $7.381bn (Jefferies/FactSet) | BBG 2FY $7.384bn | Ties (0.0%). |
| PANW | FY27 revenue | Guide $14.1-14.2bn; consensus $14.169bn (Jefferies/FactSet) | BBG 1FY $14.155bn | Ties; FY28 cons $16.189bn vs BBG 2FY $16.182bn. |
| OKTA | FY28 revenue consensus | $3.544bn (Jefferies/FactSet) | BBG 2FY $3.548bn | Ties. |
| NET | FY27 revenue consensus | $3.684bn (Jefferies/FactSet) | BBG 2FY $3.707bn | −0.6%; same consensus within panel noise. |
| CRWV / neoclouds | GPU rental pricing | Blackstone (Gray): *"Compute prices are actually up 50% year-on-year"*; value in legacy H100s | CRWV page: +25% then a second +10% price rise (10-01); 22V B200/B300 rates still rising (ai-compute-deals 09-27) | Direction confirmed by a financier/landlord; basis of the +50% unstated, so not chained into a series. |
| ai-datacenter-power | DC leasing momentum | Blackstone ~6 GW leased in 2026, 3x 2025 (GW basis unstated) | Page: record 13 GW NA adds in 2Q26 (JPM/datacenterHawk), Aterio 83 GW under construction | Consistent with the supply-constrained read; Blackstone's own platform, not a market total. |

_No BBG-dependent row is PENDING (on-disk snapshot asof 2026-10-21 used)._
