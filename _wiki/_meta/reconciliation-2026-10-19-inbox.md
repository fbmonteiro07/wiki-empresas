# Reconciliation — /run-inbox 2026-10-19 (interactive)

Sources: **J.P. Morgan · Doug Anmuth et al., "US Internet: 3Q 2026 Preview"** (2026-10-15, 48pp) and **Morgan Stanley · Adam Wood, "Microsoft 1Q27 Preview – Sustaining Momentum Against a Higher Bar"** (2026-10-19, 23pp). BBG consensus from `_data/estimates.json` (asof 2026-10-19). House models: no Capstone model numbers changed by these sources. "JPM cons" = the consensus column printed in the JPM deck (may differ from BBG).

## DIVERGES (alpha candidates)

| Ticker | Metric | Broker | BBG consensus | Gap | Note |
|---|---|---|--:|--:|---|
| AMZN | 2027E capex | JPM $366.4bn (JPM cons $281.5bn) | CY27 $290.3bn | **+26%** | JPM far above both consensus series |
| MSFT | FY27e capex (Jun-YE) | MS $220.1bn | 1FY $187.0bn | **+18%** | basis: MS fiscal year; BBG 1FY = FY27 |
| MSFT | 2027E capex (calendar) | JPM $241.9bn | CY27 $206.2bn | **+17%** | JPM calendarized (Chatterjee coverage, per deck) |
| MSFT | FY29e EPS | MS $30.12 | 3FY $28.70 | +4.9% | MS above the out-year |
| MSFT | FY28e EPS | MS $24.08 | 2FY $23.48 | +2.6% | |
| RDDT | 3Q26 revenue | JPM $924M | Q3-26E $870M | **+6.3%** | JPM bar $940M+; 4Q $1,129M vs $1,045M (+8%) |
| RDDT | 3Q26 adj. EBITDA | JPM $430M | (EBITDA $398M) | +8% | |
| AMZN | 3Q/4Q AWS growth | JPM +41% / +43% | JPM cons 37.4% / 38.1% | +3.6 / +4.9pp | BBG has no AWS segment field here |
| SPOT | PT | JPM €650 (OW) | cons €593 | +10% | ccy EUR |
| AMZN | PT | JPM $365 (OW) | cons $333 | +10% | |

## CONFIRMS

| Ticker | Metric | Broker | BBG consensus | Note |
|---|---|---|--:|---|
| MSFT | FY27e EPS | MS $19.70 (prior $19.66) | 1FY $19.77 | in line; MS PT $600 vs cons $593 |
| MSFT | F1Q27 EPS | MS ~$4.76-4.77 (cover vs Exh. 11) | Q3-26E $4.73 | in line |
| GOOG | PT | JPM $425 (from $420) | cons $427 | in line; BBG GOOG FY fields look mis-indexed — EPS not compared |
| UBER | 3Q26 adj. EPS | JPM $0.87 (NR) | Q3-26E $0.87 | in line; 2027E $4.47 vs CY27 $4.43 |
| RDDT | FY27E revenue | JPM $4,565M | CY27 $4,456M | +2.4%, close |
| BKNG | PT | JPM $248 (from $236) | cons $234 | +6% |
| NFLX | PT | JPM $85 (OW) | cons $92 | JPM below the consensus PT |

## Not reconciled / PENDING

- **GW capacity:** MS capacity tracker ~3.25 GW (FY26) / ~4.25 GW (FY27E) for MSFT. Basis undefined by MS (facility vs IT-load), so it was logged as a variant on `themes/ai-datacenter-power.md` and **not** netted against `ai-dc-power-gw`.
- **META:** the deck's estimate levels were added to the page; there is no single headline metric to set against BBG here.
- **Capital Carousel (3).pdf:** the same document as the 2026-09-21 Redburn "Capital Carousel" (only the watermark differs), so there is no new datapoint.
