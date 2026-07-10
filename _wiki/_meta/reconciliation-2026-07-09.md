# Reconciliation — run-inbox 2026-07-09

New quantitative datapoints from the 8 files ingested 2026-07-09, variance-checked vs **(1) prior wiki comments** (on disk), **(2) Capstone house models** (on-page `## Capstone estimates` blocks), and **(3) BBG consensus**.

> **⚠ BBG column = PENDING.** The Bloomberg wrapper (`E:\bloomberg_api`) raised **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal."** The Terminal is not logged in / VPN likely down. Per protocol, the two on-disk baselines are completed below and the consensus column is left PENDING — **no web data was substituted for consensus.** Re-run `py "E:\Wiki Felipe empresas\_wiki\_tools\refresh_features.py" --run-estimates` (or `py E:\.claude\scripts\fetch_estimates.py`) once the Terminal is back to close these out.

Qualitative/thematic notes (INTC EMIB-T mechanics, GOOG TPU packaging, most theme read-throughs) are excluded — only NEW numbers are reconciled.

---

## DIVERGES — the alpha

| Name | New datapoint (source) | vs Prior wiki | vs House model | vs BBG cons |
|---|---|---|---|---|
| **TSM** | Fubon FY26/FY27 EPS **NT$103.90 / NT$144.13**; PT **NT$3,500** (Buy) (Fubon, 2026-07-08) | **Street-high on both.** PT NT$3,500 > JPM NT$3,100 (07-06) > UBS NT$3,000 (05-21) > Bernstein NT$2,780/$430 (07-06). EPS explicitly flagged by Fubon as above cons NT$99.52/NT$127.84. | House model block on page (see `## Capstone estimates`) — Fubon FY27 EPS sits at the top of the range; check house FY27 vs NT$144. | **PENDING** |
| **AMZN** | GS **PT $325 → $335** (Buy); rev **$827.6 / $952.9 / $1,081.0bn** FY26/27/28 (GS "Q2'26 Preview", 2026-07-07) | **New Street-high PT** among names on page: GS $335 > Barclays $330 (06-01) > Bernstein $315 (06-22) > BofA $310 (07-07). Rev path broadly consistent with the capex/GW framing already logged. | No dedicated AMZN house model block on page. | **PENDING** |
| **CIEN** | MS reiterate **EW, PT $490**; MS **CY28 EPS ~$15** vs buyside ~$18-20 (MS "Face-off Nokia vs Ciena", 2026-07-09) | **MS is the Street-low anchor** vs JPM OW $635 (06-05) & Citi Buy $658 (06-23); MS's own CY28 EPS ~$15 sits below the buyside ~$18-20 it cites. The bull/bear gap remains ~pure multiple. Consensus EPS on page CY26 $7.00 / CY27 $10.81. | No CIEN house model. | **PENDING** |
| **SPCX** | JPM initiate **OW, Dec-27 PT $225**; rev $18.7B(FY25A)→**$160.4B (FY28E)**; Adj. EPS $(0.84)→$5.77 (JPM, 2026-07-07) | Net-new page block. JPM's estimates are **far above the BBG synthetic consensus already noted on-page** (BBG EPS $(0.99)/$(0.04)/$0.50 FY26/27/28 vs JPM $0.43/$1.19/$5.77) — a wide pre-IPO estimate dispersion. | Private / no house model. | **PENDING** (pre-IPO; consensus thin) |
| **ANTHROPIC** | ARR **$9B(end-'25)→$30B(1Q26)→>$60B(now)**; 3Q26 EBIT **~$1B**; **$6T** base-case valuation (SemiAnalysis, 2026-07-08) | **Large upward revision** — prior wiki run-rate (~$40-47B, moved to Changelog this run) is now superseded by >$60B; profitability (3Q26 EBIT ~$1B, non-GAAP) is a new inflection vs the prior "money-burning labs" framing. | Private / no house/BBG. | n/a (private) |
| **OPENAI** | 1Q26 **>65% subscription** / ~40% Consumer-sub ARR; IPO reportedly pushed to **2027** (SemiAnalysis, 2026-07-08) | Sharpens the Anthropic-vs-OpenAI contrast (Anthropic 15% subs / API-led vs OpenAI subs-heavy); IPO-timing slip is new. | Private. | n/a (private) |

## CONFIRMS — no action

| Name | New datapoint (source) | Reconciliation |
|---|---|---|
| **TSM** | FY27 capex **US$75bn**; CoWoS **180kwpm end-FY27** → 210-220kwpm end-2028; 2Q26 GM **~67.1%** (Fubon, 2026-07-08) | **In-line.** Capex ≈ JPM $78bn FY27 (07-06). CoWoS 180k matches Jefferies/Sherman 180k end-Q4'27 (06-29), above JPM's 175k. GM 67.1% ≈ latest VA cons 66.9% / between Sherman 66.2% and JPM 69.5%. |
| **GEV** | BofA **Buy, PO $1,310** (40x 2027E adj. EBITDA); gas-turbine capacity 15→24GW '25-'30, sold out through 2030 (BofA "Power gap", 2026-07-08) | **Corroborates** the on-page gas-scarcity/pricing thesis (Barclays sold-out-through-2028; $200B backlog pulled to '27; Jefferies Buy 2028E EPS $6.35). Independent semis-anchored read on the 100+GW US shortfall. |
| **AMZN** | AWS capex **$159bn'26 / $230bn'27**; ~15GW added '26-27 at ~$25bn/GW (BofA, 2026-07-07, folded alongside GS preview) | **Consistent** with JPM "AI Capex 2.0" (~$200bn→$300bn→$350bn FY26-28) and the Trainium >$225bn commitments already on page. |
| **SKHYNIX** | SKHY ADR offering **~US$28.2bn** / ~17.79M new shares (~2.5% TSO) (Morgan Stanley S&T, 2026-07-08) | **≈ confirms** Jefferies' ~US$29bn sizing (rounding, not a supersession). ADR premium 5-10% expected vs TSMC's ~18% — structural, not an estimate. |
| **Analog complex** (IFX/TXN/ADI/ON/MCHP/NVTS/WOLF) | BofA CY30 AI-analog **segment** revenue/share (IFX $4.6bn/17.3%, TXN $5.7bn, ADI $4.4bn, ON $2.3bn, etc.) (BofA "Watts to Tokens", 2026-05-25) | **Thematic — not directly comparable to total-company consensus.** These are 2030 AI-analog *segment* model outputs; logged on-page + in `themes/800v-dc-power.md`. Flag for a forward cross-check once BBG total-company revenue is available. |

---

## To close out
1. **Log in to the Bloomberg Terminal / reconnect Capstone VPN**, then run `py "E:\Wiki Felipe empresas\_wiki\_tools\refresh_features.py" --run-estimates` to populate the PENDING consensus column for TSM, AMZN, CIEN, GEV, and the analog names (place Fubon's TSM EPS, GS's AMZN PT, and MS's CIEN CY28 EPS vs the consensus median).
2. **Edge tracker** should pick up the new DIVERGES rows (TSM Street-high EPS/PT; AMZN new Street-high PT; CIEN MS Street-low; SPCX pre-IPO dispersion; ANTHROPIC ARR revision) after the feature rebuild.

---

# Reconciliation — run-inbox 2026-07-09 (Run 2 · second batch)

New quantitative datapoints from the **second 2026-07-09 ingest** (3 new files: TD Cowen semicap preview + Bernstein "New Memory LTAs part 2"; the SemiAnalysis MSL piece is qualitative/strategic — excluded from the number reconciliation; the MS Nokia/Ciena file was a duplicate re-drop, no new numbers). Variance-checked vs **(1) prior wiki comments**, **(2) Capstone house models** (semicap-wfe page carries the ASML_Peers_SemiCap house EPS/WFE), and **(3) BBG consensus**.

> **⚠ BBG column = PENDING (again).** The wrapper (`E:\bloomberg_api`) still raised **HTTP 503 — "please ensure you are logged in to Bloomberg Terminal"** on this second run. On-disk baselines completed below; consensus left PENDING. No web data substituted.

## DIVERGES — the alpha

| Name | New datapoint (source) | vs Prior wiki | vs House model | vs BBG cons |
|---|---|---|---|---|
| **AMAT** | TD Cowen **Buy, PT $525→$700** (top Long); CY28 EPS power ~**$25 @ $250B WFE** (≈1.9x CY26E $13.35) (TD Cowen "Puts & Takes", 2026-07-09) | **New Street-high PT** on the page: $700 > GS $645 (07-05) > Redburn $560 > Bernstein-implied. Cowen the most bullish semicap voice on AMAT. | Cowen CY28 EPS $25 sits **just above** house AMAT 2028E ~$23 — consistent, slightly ahead. | **PENDING** |
| **ASML** | TD Cowen **Buy, PT €1,600**; EUV shippable 88/'27, 110/'28 (TD Cowen, 2026-07-09) | **Street-LOW anchor** vs the €1,830-2,300 cluster (Bernstein €2,300 07-06, JPM €1,900 06-03, MS €1,830 07-07, Redburn €1,900). Cowen's EUV-unit path (88/110) is *below* Bernstein's 91/113 and MS's 92 — the cautious ASML mark on the page even while calling it a top Long. | House ASML 2028E EPS €69 — cross-check PT-implied multiple once cons is back. | **PENDING** |
| **TSM** | TD Cowen **Hold, PT $400 (TSM-US ADR) — below $436.98 spot**; capex $56-60/$80/$100B '26/'27/'28; 38 of 88 EUV tools '27 (TD Cowen, 2026-07-09) | **Lone cautious rating** on a bull-heavy page (Fubon PT NT$3,500 Street-high 07-08; JPM/UBS bullish). Note the tension: Cowen's **capex stack ($80B/'27, $100B/'28) is MORE aggressive** than UBS ($75B/$85B) — so it's a valuation/multiple call on an already-run ADR, not a demand call. | TSM house model exists (bullish) — Cowen Hold is the outlier vs house. | **PENDING** |
| **STX** | TD Cowen **Buy, PT $850 (below $860 spot)**; CY27 EPS bull **→$45 (20% ASP)** from prior $35+; buyside already **+$50 (30% ASP)** (TD Cowen, 2026-07-09) | **Sell-side now chasing buy-side** — "first time in two years our bull view is below buyside." Buy rating with PT ~at/below spot = the pricing leg is largely in the tape. Prior wiki bull was $35+. | No STX house model. | **PENDING** |
| **WDC** | TD Cowen **Buy, PT $500 (below $550 spot)**; CY27 EPS bull **→$25 (20% ASP)** from prior $20; buyside **+$30 (30% ASP)** (TD Cowen, 2026-07-09) | Same HDD dynamic as STX — Buy w/ PT below spot; EPS bull raised but buy-side has out-run it. | No WDC house model. | **PENDING** |
| **AEIS** | TD Cowen **Hold, PT $350** (TD Cowen, 2026-07-09) | **Relative bear** — the sole non-Buy vs BofA $430, Citi $410, Needham $400, Cantor $400, WF OW $465. Cowen is the skeptic on the AEIS re-rate the page otherwise tracks. | No AEIS house model. | **PENDING** |
| **LRCX** | TD Cowen **Buy, PT $340→$400** (top Long); EPS ~**$9-10 @ $250B WFE** (TD Cowen, 2026-07-09) | PT in-range (GS $380 07-05, MS $404, Redburn $420) — near consensus, not divergent. But Cowen's $9-10 @ $250B is **below house LRCX 2028E ~$12** — a modelling gap to flag. | **Cowen EPS below house $12** at a similar WFE — check the bridge (share/margin assumptions). | **PENDING** |

## CONFIRMS — no action

| Name | New datapoint (source) | Reconciliation |
|---|---|---|
| **SNDK** | Bernstein reiterate **Outperform, PT $3,000** (11x FY28 EPS); FY26E/27E EPS **$65.43 / $243.73**, P/E 7.1x; ~$69B RPO backed by >$11B guarantees (Bernstein "New Memory LTAs part 2", 2026-07-09) | **Confirms/reiterates** the 06-30 Bernstein note already on page (FY27E ~$243 +28% vs cons; PT $3,000; bull $350). No PT/estimate drift — this is the part-2 structural deep-dive. The ~$69B RPO is a distinct metric from the on-page $42B backlog (added, not overwritten). |
| **MU** | TD Cowen **Buy, PT $1,600** (px $948.80); Bernstein: $18B cash deposits + $4B LC backing LTAs, coverage → 75-100% of RPO outer years (2026-07-09) | **Confirms.** Cowen $1,600 ≈ UBS $1,625 already on page (rounding, not a supersession). Bernstein's deposit/coverage figures corroborate the existing LTA-structure framing (the $18B/$4B were already on-page from the 06-29 Jefferies/Fubon IR call). |
| **KLAC** | TD Cowen **Buy, PT $200→$260** (top Long; post 10:1 split, fwd ests updated) (TD Cowen, 2026-07-09) | **In-range with a split caveat.** $260 post-split brackets Redburn $260 / GS Neutral $230 / MS OW $274 — but confirm the split basis before comparing (KLAC did a 10:1 split; unsplit UBS mark was $1,260). No clean divergence. |
| **ARM / TER** | ARM **Buy PT $475** (FY31 rev/EPS ~$25B/$9+ in $100B+ server-CPU TAM); TER **Buy PT $400** (TD Cowen, 2026-07-09) | ARM: no strong prior PT tracked on page — logged as new house mark, not a divergence. TER: $400 is **below GS $465 (07-05)** but within a reasonable band; Cowen flags back-end not raising prices / EPS de-risked (qualitative). |
| **WFE TAM** | TD Cowen **$150/$200/$250/$300/$400B CY26-30** (TD Cowen, 2026-07-09) | **Broadly confirms the house/UBS bull curve** — Cowen $250B '28 ≈ Capstone house $260B '28 ≈ UBS $248B (all well above cons $202B). Cowen's $400B-by-2030 is the aggressive tail vs Redburn $272B/2030 — logged as the high-end scenario on `themes/semicap-wfe.md`. |

## To close out (Run 2)
- Same BBG dependency as Run 1 — once the Terminal is back, place the Cowen semicap PTs (AMAT $700 Street-high, ASML €1,600 Street-low, TSM $400 Hold below spot) and the STX/WDC HDD EPS bulls against the consensus median. Two on-disk gaps worth a model check: **LRCX Cowen EPS $9-10 @ $250B vs house ~$12**, and **TSM Cowen Hold vs the bullish house model**.
