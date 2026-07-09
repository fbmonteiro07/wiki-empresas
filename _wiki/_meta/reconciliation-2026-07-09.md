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
