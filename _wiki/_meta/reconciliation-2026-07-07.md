# Reconciliation — 2026-07-07 run-inbox

New quantitative datapoints from the 4 files ingested 2026-07-07, checked against **(1)** prior wiki marks, **(2)** Capstone house models (`_data/house.json`, asof 2026-07-07), and **(3)** BBG consensus (live — Terminal up, no PENDING this run). FY1/FY2/FY3 = 2026/2027/2028 for all names below (Dec year-ends). BBG capex shown as absolute (wrapper returns negative cash-outflow). BBG pulled 2026-07-07: `PX_LAST, BEST_TARGET_PRICE, BEST_EPS, BEST_SALES, BEST_CAPEX`.

Sources: MS "The Catalyst Path Ahead" (ASML, Lee Simpson) · BofA "Raising Internet capex ests" (Justin Post) · UBS "SpaceX's Terafab" (Tim Arcuri) · NVIDIA NDR deck (company IR).

---

## DIVERGES — the alpha

| Name | Metric | New datapoint (source) | BBG consensus | House | Read |
|---|---|---|---|---|---|
| **GOOG** | Capex 2027 | **$290bn** (BofA, from $257bn prior) | **$243.9bn** | **$310bn** | Both house AND BofA well above Street on '27 Google capex. BofA +$46bn (+19%) vs cons; **house $310bn is Street-highest, +$66bn (+27%) vs cons**. Consensus has not caught up to the post-June-3-capital-raise capex step-up. Edge: long Google capex-beneficiary read (TPU/semicap/power); the capex line itself is a headwind to near-term GOOG FCF (house 2027 FCF **−$55bn**). |
| **GOOG** | Capex 2026 | **$195bn** (BofA, from $187bn) | $186.5bn | $183bn | BofA modestly above cons; house slightly below cons. Minor — the '27 gap is the story. |
| **META** | Capex 2027 | **$185bn** (BofA, from $157bn) | **$162.0bn** | $170bn | BofA +$23bn (+14%) vs cons and +$15bn vs house. House sits between cons and BofA. Street still catching up to Meta's AI-capacity build. |
| **META** | Capex 2026 | **$145bn** (BofA, from $130bn) | $134.7bn | $131bn | BofA +$10bn above both cons and house. House ≈ cons; BofA the high mark. |
| **META** | EPS 2027 | (BofA note is capex-focused; house EPS for context) | **$44.36** | **$38.24** | Not from the BofA note, but flagged: **house 2027 EPS $38.24 is ~14% BELOW consensus $44.36** — the heavier house capex/depreciation drag. The capex-up datapoints reinforce the house-below-Street-EPS setup (more D&A). Watch on any 2Q print. |
| **INTC** | Price target | **$122 Neutral** (UBS, from $40) | **$102.26** (median) | n/a | UBS PT **+19% above the consensus median** and above spot ($110.39), yet rating stays **Neutral** — a rating-vs-PT tension (consensus median $102 sits *below* spot, i.e. Street sees downside; UBS sees upside but won't rate it Buy). The move is a **huge upward revision from UBS's own $40** (Dec-2025), driven by the Terafab optionality (INTC as Terafab "knowledge owner"/tool-slot broker), not core fundamentals. Optionality re-rating, not an earnings call. |
| **ASML** | EPS 2027 | **€47.38** (MS) | **€43.00** | see note | MS FY27 EPS **+10% above consensus €43.00**, driven by lifting EUV unit ests to **92** (from 90) — SK Hynix now 6 tools/qtr vs 3. Below the Street-high EPS bulls (Bernstein €56.7 25-28E, JPM +35% vs cons) already on the ASML/semicap pages but a clean above-cons mark. FY26 (€32.00 vs cons €31.80) and FY28 (€52.19 vs cons €52.07) are in line. |
| **ANTHROPIC** | $/GW capacity | **>$40bn/GW, up to ~$50bn/GW** for specialized AI capacity (BofA, SpaceX deal) | n/a (private) | n/a | vs prior wiki marks: Patel ~$25bn/GW; BG2 ~$22–23bn/GW/yr; Trainium <$10bn/GW. BofA's $40–50bn/GW is a **high-end mark** — reflects specialized/leased AI capacity economics, not build cost. Directionally supports the "capacity-deal revenue/GW >> build cost/GW" thesis on the hyperscaler pages (AWS rev/GW $10.6bn, Google Cloud $15.7bn — the deals imply large upside). Reconciled vs prior wiki only (no BBG/house). |

## CONFIRMS — no action

| Name | Metric | New datapoint | Baseline | Read |
|---|---|---|---|---|
| **ASML** | PT €1,830 (MS, from €1,660), OW/Top Pick | BBG PT median €1,701.67 | Above the consensus median (+8%) but **below** the Street-high bulls already logged (Bernstein €2,300, JPM/Redburn €1,900). MS is a mid-to-upper mark, not new Street-high. No page thesis change. |
| **ASML** | Sales FY26 €39.4bn (MS, from €37.7bn) | BBG €39.17bn | In line with consensus. Confirms. |
| **ASML** | EPS FY26 €32.00 / FY28 €52.19 (MS) | BBG €31.80 / €52.07 | Both in line. Confirms. |
| **AMZN** | AWS capex $159bn'26 / $230bn'27 (BofA, Buy reiterated) | BBG **total-company** capex $199.6bn'26 / $230.1bn'27 | **Basis mismatch** — BofA figure is AWS ex-retail; BBG is whole-company. Not directly comparable, so filed as CONFIRMS-with-caveat rather than a clean divergence. Signal: BofA's **AWS-alone $230bn'27 ≈ the Street's whole-company $230bn'27** → BofA implicitly sees AWS capex at the level Street models for all of Amazon, i.e. above-Street on AWS. AMZN has no house model in `house.json` (not tracked). |
| **NVDA** | GPU cloud-pricing durability: H100 +13%/+21% (3m/6m), A100 +7%/+5% (deck, SemiAnalysis) | House NVDA rev $407bn'26 / $661bn'27; GM ~75%/~74% | Qualitative/roadmap deck, no PT. Pricing-durability + Rubin/Feynman cadence + GB300 cost/token leadership are **supportive of** the house DC-rev and GM lines (no number to reconcile). Rubin 2026 / Feynman 2028 public cadence is company framing to hold against the sell-side Rubin-ramp / Kyber-slip debate, not a supersession. |

---

**Net edge from this run:** the cleanest new alpha is the **hyperscaler-capex-above-consensus** cluster — GOOG '27 (both house $310bn and BofA $290bn >> cons $244bn) and META '27 (BofA $185bn / house $170bn > cons $162bn). Consensus capex is lagging the mid-2026 step-up (Alphabet June-3 raise, Meta AI-capacity build), which reads long the capex-beneficiary chain (semicap/WFE — see the corroborating UBS-Terafab + MS-ASML EUV items this same run — TPU/ASIC, and DC power) and cautious on near-term hyperscaler FCF. Second, **ASML FY27 EPS €47.38 (+10% vs cons)** adds one more above-Street EUV mark. Third, **INTC's UBS $40→$122** is an optionality re-rating on Terafab, not fundamentals — a Neutral-rated PT above both consensus and spot, worth watching but not a conviction signal.
