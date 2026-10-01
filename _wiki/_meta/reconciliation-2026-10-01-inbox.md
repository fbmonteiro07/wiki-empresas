# Reconciliation — run-inbox 2026-10-01 (unattended)

_8 sources across four work units: optics, taiwan, mu and internet. Each new quantitative datapoint is checked against three baselines: (1) what the wiki already carried; (2) the Capstone house models, from each page's `## Capstone estimates (house model)` block and `_data/house.json` asof 2026-10-01, read from `raw_rows`; (3) BBG consensus. **BBG leg: LIVE.** The Terminal was up, and `bdp` was pulled on 2026-10-01 for PX_LAST, BEST_TARGET_PRICE/HI/LO, BEST_EPS, BEST_SALES, BEST_EBIT, BEST_GROSS_MARGIN and BEST_CAPEX, with `BEST_FPERIOD_OVERRIDE` set to 1FQ/2FQ/1FY/2FY/3FY. Every consensus figure states its fiscal period, taken from BEST_PERIOD_END_DATE: MU = FY-Aug, LITE/COHR = FY-Jun, CIEN = FY-Oct, CSCO = FY-Jul, SNPS = FY-Oct, and the rest = FY-Dec. Calendar-year sums (CY2026/CY2027) come from the on-disk `_data/estimates.json` (asof 2026-10-01). Where they are used, they carry the known caveat that reported quarters inside a CY sum embed pre-print consensus. Each number below was re-read in the primary text in the scratchpad (bern.txt, telecom.txt, sherman.txt, jpmtsm.txt, mupr.txt, muprep.txt, barc.txt, snps.txt), not taken from the unit summaries. Web data was not used anywhere._

Sources: Bernstein Zhu "US Networking: Scaling the bandwidth wall. Initiating with a positive view" (09-29, 117pp) · Morgan Stanley Marshall et al. "Potential FCC Rules on Optical Transceivers More Likely to Come in at 3.2T" (10-01) · Fubon Research Shang/Yang "Taiwan upstream 2026 outlook" (Sept-2026 deck, 119pp) · J.P. Morgan Hariharan et al. "TSMC: Expect strong 3Q26 results … Raise PT to NT$3300" (09-30) · Micron F4Q26 press release + "Fiscal Q4 2026 Earnings Call Prepared Remarks" (09-30; prepared remarks only, no Q&A on disk) · Barclays Sandler et al. "U.S. Internet: The Battle for the Persistent Consumer AI Agent Begins" (09-30) · São Pedro Capital GTF team "GTF Letter 5 — AI Won't Kill EDA, It Has to Pass Through It" (09-29; BUY-SIDE fund letter, fund long SNPS).

---

## 🔴 THE HEADLINE — the house is the Street LOW on COHR, it carries ~⅓ fewer NVIDIA units for 2027 than Fubon, and the Street is still behind on TSMC 2027-28 capex and on MU FY27 after the print

| # | Name | New datapoint (source) | Prior wiki | Capstone house | BBG live (10-01) | Gap |
|---|---|---|---|---|---|---|
| 1 | **COHR** | Bernstein **OP, PT $350**; FY28 (Jun) EPS **$15.76** | Capstone initiation 09-01: Neutral $285 | **Neutral, PT $285** (25x CY27E $11.30); CY28E $14.34 | PT **$413.40** (hi $500 / lo $280, n=29); FY28 EPS **$14.41**; px $319.19 | **House PT is −31% vs consensus and $5 above the Street low.** Bernstein is +9% vs BBG on FY28 EPS and roughly +23% vs the house on a like-for-like FY28 basis (my calendarisation) |
| 2 | **TSM** | JPM capex **US$64 / 86 / 100bn** (2026/27/28); EPS NT$108.62 / 147.80 / 190.42 | JPM US$62 / 81 / 90bn (09-17) | 2026E rev US$165bn, EPS NT$102.5; 2027E NT$143.5 (06-10 model) | capex ≈ **US$63 / 75 / 86bn** (NT$ converted at JPM's implied FX); EPS NT$107.09 / 140.73 / 176.82 | **JPM is +14% / +16% above consensus capex for 2027/28** and +7.7% on 2028 EPS. The house's 2026 line is stale: about −4% on both revenue and EPS |
| 3 | **NVDA** | Fubon GPU shipments **8.47mn (2026E) → 11.56mn (2027E), +36%** | 09-28: GS 14/18 GW; house GW 16.0/24.8 | chips deployed **7.67mn → 7.57mn (flat)**; DC revenue $379bn → $629bn | FY28 (Jan) revenue $701.7bn | **Fubon has 53% more 2027 units than the house.** For Rubin alone it is 9.83mn vs 6.40mn (+54%). The house reaches a lower revenue than consensus on far fewer units |
| 4 | **MU** | F1Q27 guide $61.5bn / ~86.25% / $38.15; FY27 capex 1H ~$25bn, "higher in 2H" | pre-print Street FQ1 $56.0-57bn; FY27 capex $45.0-45.3bn; MS post-print FY27 EPS $182.52 | no house model | 1FQ $61.41bn / $38.31 / 86.42%; FY27 (Aug) **$269.5bn / $168.22**, capex **$49.8bn** | **FY27 consensus EPS is still 7.8% below MS's post-print number, and consensus capex sits below the >$50bn floor that management's guide implies.** FQ1 consensus is already at the guide |
| 5 | **LITE / COHR (optics TAM)** | Bernstein transceiver market **$99bn (2027E) / $158bn (2028E)** | GS panel 08-10: **$72.6bn / $69.1bn** (2028 down 5%) | house LITE CY27 $8.1bn | n/a | **Bernstein is +36% above GS for 2027 and 2.3x for 2028.** The "2028 pause" on the optical-cpo page is now contested by a primary |
| 6 | **META** | Barclays prices Muse hosting at **$4.07 per DAU per month**; "$40B+ in extra annual compute" to win the free tier | 09-28: house $301bn vs Street $333-337bn CY26-27 capex | capex **$131bn / $170bn** | capex **$139.3bn / $198.5bn** | **The house is −14% on CY27 capex**, a gap that widened from −10% on 09-28. The house P&L is in line (2027 EPS $38.24 vs $38.38) |

➤ **COHR is the actionable gap.** The house PT is now the Street's second-lowest mark. Bernstein's OP $350 sits *below* the $413 median, yet still $65 above the house. The disagreement is FY28 EPS, not FY27: the three numbers agree within ~1% for FY27 ($9.51 Bernstein vs $9.39 BBG; house CY27 $11.30 vs BBG CY2027 $11.91). It is the FY28 leg (Bernstein revenue $16.27bn vs BBG $14.74bn) that the house's 25x-CY27 framing does not price.
➤ **NVDA: the house needs a unit bridge.** Bernstein's VR NVL72 rack BOM (XPU $4,657K + HBM $697K over 72 packages ≈ $74k per package, my arithmetic) is consistent with the house's ~$83k all-in revenue per chip ($629bn / 7.57mn). Fubon's 11.56mn units at the house's revenue would imply ~$54k. Either Fubon's CoWoS-derived shipment count overstates what NVIDIA ships and recognises in 2027, or the house is under-modelling 2027 volume.
➤ **TSMC and MU share one pattern: management or a lead broker moved the capex line first, and consensus has not caught up.** TSMC capex for 2027-28 is +14-16% above consensus at JPM. For MU, management's 1H/2H shape puts FY27 capex above $50bn, against a $49.8bn consensus.

---

## Where the new data DIVERGES

### 1. 🔴 COHR — house Neutral $285 is the Street's second-lowest PT; Bernstein OP $350 sits below the consensus median
- **Bernstein Zhu (09-29): Outperform, PT $350**, which is ~22x "$16 in FY 2028 EPS" (p.68; model p.104).

| Item | Bernstein | BBG (live) | Bernstein vs BBG |
|---|--:|--:|--:|
| FY27 (Jun) revenue / EPS | $10.85bn / $9.51 | $10.70bn / $9.39 | +1.4% / +1.3% |
| FY28 revenue / EPS | $16.27bn / $15.76 | $14.74bn / $14.41 | +10.4% / +9.4% |

- **Price targets vs consensus:** the BBG median is **$413.40** (hi $500 / lo $280, n=29, rating 4.55) and px is **$319.19**. Bernstein's Outperform is therefore −15% vs the median, with only +9.7% upside at today's price; the note was written off a $282.45 price.
- **House** (Capstone initiation 09-01, unchanged): **Neutral, PT $285** = 25x CY27E $11.30, with CY26/27/28E revenue $8.7 / 12.6 / 15.7bn and EPS $7.30 / 11.30 / 14.34.
  - vs the BBG on-disk CY2027 sum ($12.69bn / $11.91), the house is −1% on revenue and −5% on EPS.
  - **Like-for-like FY28 (Jul-27 → Jun-28):** half of CY27 plus half of CY28 gives a house FY28 of ≈ **$12.82** (my arithmetic). Bernstein is ≈ **+23%** above that and BBG ≈ +12%.
- **Prior wiki:** the page's last broker PT before this note was a $375 attendee note, alongside an earlier $420 reiteration. The house PT is $5 above the BBG low ($280).
- ➤ **Action: decide whether the house's 25x-CY27 framing is still right now that every outside mark prices the FY28 ramp — the house is ~$128 below the Street median on a P&L that is within 5% of consensus for CY27.**

### 2. 🔴 TSM — JPM capex US$86 / 100bn for 2027/28 is +14% / +16% above consensus; house 2026 line stale
- **JPM Hariharan (09-30): OW, PT NT$3,300** (from NT$3,200), which is 20x 12m-forward EPS, at px NT$2,475 on 09-29. JPM vs BBG (live):

| Item (2026 / 2027 / 2028) | JPM | BBG | JPM vs BBG |
|---|--:|--:|--:|
| Adj. EPS (NT$) | 108.62 / 147.80 / 190.42 | 107.09 / 140.73 / 176.82 | +1.4% / +5.0% / +7.7% |
| Revenue (NT$bn) | 5,473 / 7,603 / 9,816 | 5,429.5 / 7,325.6 / 9,186.0 | +0.8% / +3.8% / +6.9% |
| GM | 66.9% / 67.8% / 68.6% | 66.35% / 66.40% / 66.25% | +55bp / +140bp / +235bp |
| Operating profit (NT$bn) | 3,206 / 4,486 / 5,851 | EBIT 3,159 / 4,254 / 5,295 | +1.5% / +5.5% / +10.5% |

- **Capex:** JPM is **US$64 / 86 / 100bn**. BBG BEST_CAPEX is NT$1,994 / 2,386 / 2,740bn, which converts at JPM's implied FX (31.65 / 31.70 / 31.70) to **≈US$63.0 / 75.3 / 86.4bn**. JPM is therefore **+2% / +14% / +16%** above consensus. Fubon's US$62 / 80 / 95bn sits between the two.
- **PT:** BBG consensus is **NT$3,230** (hi 4,200 / lo 2,700, n=41) at px NT$2,510, so JPM is only +2% vs the median. The divergence is in the estimates, not the target.
- **House** (`Modelo Felipe TSM 1Q26.xlsm`, 06-10):

| Item | House | JPM | Fubon | BBG | House gap |
|---|--:|--:|--:|--:|--:|
| 2026E revenue (US$bn) | 165 | 172.9 | 169.4 | ≈171.5 (FX-converted) | **≈ −4%** |
| 2026E EPS (NT$) | 102.5 | 108.62 | | 107.09 | **≈ −4% to −6%** |
| 2027E EPS (NT$) | 143.5 | 147.80 | | 140.73 | −2.9% vs JPM; +2.0% vs BBG |

- ➤ **Action: refresh the house 2026 line (two quarters reported since the model) and take a view on whether 2027-28 capex is the ~US$75 / 86bn the Street carries or JPM's US$86 / 100bn; the CoWoS and semicap read-throughs differ by ~US$11-14bn a year.**

### 3. 🔴 NVDA — Fubon's 2027 GPU shipments are 53% above the house's chip count
- **Fubon (Sept-2026 deck, p.33)**, figures verified on the page text:
  - GPU shipments **5.96mn (2025) → 8.47mn (2026E) → 11.56mn (2027E)**, of which 2027 is B300/B300A 1.728mn + Rubin R200 8.766mn + R300 Ultra 1.065mn.
  - HBM bits are 19.39Eb → 25.81Eb (+33%) against CoWoS +74%, and average HBM per GPU is 279GB.
  - The p.64 table has the "corrected 2027 total" growing 36% y/y.
- **House** (`Modelo Felipe NVDA`, 06-17):
  - Chips deployed are **7.67mn (2026E) → 7.57mn (2027E)**, of which Blackwell / Rubin is 6.57 / 1.10mn in 2026 and 1.17 / 6.40mn in 2027.
  - DC revenue is $379bn / $629bn; total revenue $407bn / $661bn vs BBG FY27 / FY28 (Jan) **$410.8bn / $701.7bn** (house −1% / −6%).
- **The gap:** Fubon is +10% vs the house for 2026 and **+53% for 2027**; Rubin-family 9.83mn vs 6.40mn is +54%. At the house's DC revenue, Fubon's count implies ~$54k per unit vs the house's ~$83k (my arithmetic). Bernstein's VR NVL72 BOM (XPU + HBM ≈ $74k per package, page-image read) sits closer to the house.
- ⚠️ **Basis:**
  - Fubon counts packages (288GB per R200 unit = per package), on a CoWoS-output basis.
  - The house's "chips" basis is not labelled on the page. If it counts dies, the package gap is larger still.
  - Timing: TSMC packaging output leads NVIDIA revenue recognition.
- ➤ **Action: put a unit bridge into the NVDA model — packages × revenue per package for Blackwell/Rubin/Rubin Ultra in 2027 against Fubon's 11.56mn and Bernstein's rack BOM; this is the same volume-vs-price question the 09-28 report raised in GW terms (GS 18 GW vs house 24.8 GW).**

### 4. 🔴 MU — FY27 consensus is post-print on the quarter but not on the year; capex consensus sits below the implied floor
- **Micron F4Q26 (09-30)**:
  - Revenue **$54.23bn**, non-GAAP GM **87.0%**, EPS **$33.42**, vs guide $50.0bn ± 1 / ~86% / $31.00 ± 1.
  - **F1Q27 guide: $61.5bn ± $1.5bn / ~86.25% / $38.15 ± $1.00.** FQ1 is called "the floor for gross margins in fiscal 2027", with sequential revenue growth every quarter.
  - Capex: FQ1 ~$11.5bn, 1H FY27 ~$25bn, "higher in the second half" (muprep.txt lines 370-403; mupr.txt lines 395-411).
- **FQ1 (Nov-26), BBG live:** $61.41bn / EPS $38.31 / GM 86.42%. That is already at the guide, against pre-print panels of $56.0-57bn / $34.85-35.89 recorded on the page.
- **FY27 (Aug-27), BBG live 1FY:** **$269.5bn / EPS $168.22 / GM 86.81% / capex $49.8bn.**
  - vs the page's pre-print BBG FY27 EPS of $151.68 (08-21 pull): +10.9%.
  - vs MS Moore post-print (10-01, on the page): $281.05bn / 87.5% / **$182.52**, so consensus is −4.1% on revenue and **−7.8% on EPS**.
  - vs UBS FY27 $184.19 and the BofA buy-side poll at $183.82: consensus is ~$15-16 below the bulls. ⚠️ With 61 contributors, the 1FY line is most likely only partly refreshed after the print.
- **Capex:** management's shape is 1H ~$25bn plus a larger 2H, which means FY27 is above **$50bn** (our arithmetic; no full-year figure was given). Consensus is **$49.8bn**, below that floor; it was $45.0-45.3bn pre-print. UBS's ~$51bn is the only mark on the page that clears it.
- **PT:** BBG consensus is $1,597.27 (hi $2,700 / lo $900, n=61) at px $1,097.39, i.e. +46%. No house model exists.
- ➤ **Action: treat the FY27 consensus line as stale until it settles near the post-print broker cluster (~$182-184); for supply bears the capex datapoint is the more important one — the increase is construction-led cleanroom for late-CY28+, which dates the oversupply debate.**

### 5. 🔴 LITE / COHR (optics TAM) — Bernstein's transceiver market is 2.3x Goldman's for 2028; no "2028 pause"
- **Bernstein (Exhibit 29; text p.21):** transceiver revenue **$39bn (2025) → $57bn (2026E) → $99bn (2027E) → $158bn (2028E) → $295bn (2030E)**, a ~40% CAGR ("from $57B in 2026 to ~$300B in 2030").
- **Prior wiki** (`themes/optical-cpo`, GS panel 08-10): **$34.2bn / $50.9bn / $72.6bn / $69.1bn** (2025-28E), with 2028 −5% on ASP compression.
  - Bernstein vs GS is +12% for 2026, **+36% for 2027 and 2.3x for 2028.**
  - The GS panel's 3.2T units (13.1M for 2027E) also sit against MS's 10-01 timing: 3.2T *"not expected to ramp in volume until 2029"*.
- **LITE marks:**

| Item | Bernstein | BBG | Bernstein vs BBG |
|---|--:|--:|--:|
| FY27 (Jun) revenue / EPS | $6.50bn / $22.40 | $6.29bn / $21.60 | +3.4% / +3.7% |
| FY28 revenue / EPS | $10.73bn / $34.96 | $9.65bn / $34.07 | +11.2% / +2.6% |

  - ⚠️ Bernstein's own Exhibit 79 chart puts FY28 at **$9,948mn**, not the model's $10,733.7mn. The EPS ties to either figure, so the revenue line is internally inconsistent.
  - PT **$1,220** vs consensus **$1,150.71** (hi $1,400 / lo $820): +6%, but only +16.7% upside at today's $1,045.78 (the note used $921.32). The page already carries $1,270 (Redburn) and $1,280.
  - **House** (CY basis, 06-16 model) vs the BBG CY sums:
    - CY26E $4.2bn / $12.81 vs $4.52bn / $14.47: −7% / −11%, a stale line.
    - CY27E $8.1bn / $30.02 vs $7.98bn / $28.21: +1.5% / **+6.4%**.
  - Bernstein calendarised to CY27 is ≈$8.62bn / ≈$28.68 (my arithmetic). The house is therefore *lower* on revenue but *higher* on EPS than both outside marks, on its ~43% operating margin.
- ➤ **Action: the house optics model should state which TAM shape it sits on (GS's 2028 rollover or Bernstein's 40% CAGR); LITE's CY27 EPS premium rests on margin, COHR's discount on not pricing FY28 — both are TAM-shape bets.**

### 6. 🔴 META — house CY27 capex is $28bn (−14%) below the Street; Barclays gives Muse's cost per user
- **Barclays Sandler (09-30):** hosting a persistent agent costs **$4.07 per DAU per month**, made up of a $3.66 VM (AWS m8a.large, 8 users per instance) and $0.41 of inference. That is *"~10x more expensive"* than ChatGPT's free tier. Barclays says Apple/OpenAI would need *"upwards of $40B+ in extra annual compute"* to win the free tier, which implies ~820m DAU at $48.84 a year (my arithmetic).
  - Steady-state US unit economics: Muse OI per user **$11.62 vs $13.76** for the Family of Apps (FoA), i.e. Muse is margin-dilutive.
  - Rating comes from the roster only: **Overweight, $738.79 price on 09-29**. That is a price, not a PT; the note sets none.
- **House** (`Modelo Meta pós 2Q26`, 06-11): capex **$131bn / $170bn** (2026/27), FCF −$17bn / −$23bn per `raw_rows`. **BBG live: $139.3bn / $198.5bn.** The house is −6% / **−14%**, against the 09-28 gap of −10% on the two-year sum.
  - The P&L is in line: 2027 revenue house $313bn vs BBG $305.9bn (+2%); EPS $38.24 vs $38.38; EBIT margin ~35% vs 34.0%.
- Bernstein Zhu (09-29) independently frames Muse as able to *"take up capex expectations further"* (opinion, no number).
- ➤ **Action: same bridge as 09-28 — house capex vs Street — now with a per-user cost anchor: $4.07 × DAU ramp × 12 is the incremental opex/compute the house needs to size; the Street's +$28bn CY27 capex is roughly 570m DAU of Barclays' cost (my arithmetic, illustrative).**

### 7. ANET — Bernstein 2027 revenue is +9-14% above consensus, but the note prints three different figures

| Item | Bernstein | BBG (FY-Dec) | Bernstein vs BBG |
|---|--:|--:|--:|
| 2027E revenue | **$17.87bn** (Exhibit 60) / $18.1bn (Exhibit 1) / "$18.6B" (text, pp.49-50) | $16.36bn | +9% / +11% / +14% |
| 2027E EPS | **$5.61** | $5.18 | +8.3% |
| 2028E EPS | $7.03 (model) / $7.14 (PT basis) | $6.36 | +10.5% / +12.3% |

- 3Q26E is $3.324bn / $1.08 vs BBG 1FQ $3.327bn / $1.062, so Bernstein is in line for the current quarter.
- **PT $250** vs consensus **$246.78** (hi $330 / lo $181) at px $204.49: at consensus. AI back-end switching share is put at 3% → 6% → ~9% (2024-26E). No house model.
- ➤ **Action: the divergence is 2027 revenue, not the target; quote Exhibit 60's $17.87bn (the model line), not the text's $18.6bn.**

### 8. Celestica (no wiki page) — Bernstein 2027 EPS is +20% above consensus; PT near the Street high
- **Bernstein: OP, PT $520** (top pick), 2027E **$40.0bn / $23.79** vs BBG (CLS US, FY-Dec) **$35.66bn / $19.87**, i.e. **+12% / +20%**. Bernstein's own consensus line ($35.5bn / $19.69) matches.
- PT vs consensus $459.69 (hi $535 / lo $370): +13%, and $15 below the high. Px $373.09 means +39% upside.
- The upside is Jalapeño + TPU + Helios scale-up switching: CCS up ~$20bn to $36bn in 2027. Bernstein names Jalapeño's new rack architecture and Tomahawk 6's "back-end loaded" ramp as the risks. Read-through for AVGO/GOOG/AMD is on those pages; plain text only, since there is no `[[CLS]]` page.
- ➤ **Action: no page to carry it; log on optical-cpo/custom-asic-tpu only — CLS is the highest-conviction above-consensus call in the initiation.**

### 9. CIEN — Outperform with a PT 15% below consensus, on a PT basis that mislabels the year
- **Bernstein: OP, PT $440**, described as "16x our $28 in 2028 EPS". In the model, FY28E EPS is $18.61 and **FY29E is $27.70**, so the PT is 16x FY29, not FY28.

| Item | Bernstein | BBG (FY-Oct) | Bernstein vs BBG |
|---|--:|--:|--:|
| FY27E revenue / EPS | $8.494bn / $12.46 | 2FY $8.458bn / $11.83 | +0.4% / +5.3% |
| FY28E revenue / EPS | $11.17bn / $18.61 | 3FY $10.97bn / $17.41 | +1.9% / +6.9% |

- **PT** vs consensus **$515.94** (hi $660 / lo $347, n=22) at px $379.14: −14.7%, i.e. a rating-vs-PT tension. On the page, Bernstein's $440 sits with MS's $425 (09-03) at the bottom of a $425-658 board (JPM $635, Citi $658).
- ➤ **Action: carry Bernstein's CIEN view as "above on FY27-28 EPS, below on multiple"; note the FY29 basis wherever $440 is quoted.**

### 10. CSCO / GLW — Bernstein's two Market-Performs are at or near the Street LOW on PT, with estimates in line
- **CSCO: MP, PT $110**, which **equals the BBG Street low ($110)**; consensus is $138.88 (hi $170, n=31) and px $108.76. Estimates are in line:

| CSCO item | Bernstein | BBG | Gap |
|---|--:|--:|--:|
| FY27 (Jul) revenue / EPS | $73.37bn / $5.11 | $72.98bn / $5.10 | in line |
| FY28 revenue / EPS | $79.99bn / $5.58 | $78.26bn / $5.58 | +2.2% / 0.0% |

  The whole gap is the multiple (~20x FY28).
- **GLW: MP, PT $140**, against consensus $190.17 (hi $238 / lo $129, n=20) and px $160.42. That is −26% vs the median, $11 above the low, and −12.7% downside. Estimates:

| GLW item | Bernstein | BBG | Gap |
|---|--:|--:|--:|
| 2027E revenue / EPS | $22.87bn / $4.16 | $22.82bn / $4.33 | +0.2% / **−3.9%** |
| 2028E revenue / EPS | $28.10bn / $5.65 | $27.72bn / $5.88 | +1.4% / **−3.9%** |

  ⚠️ Bernstein prints two different GLW PT bases on the same page (p.82): "25x $5.72" and "25x $5.65".
- ➤ **Action: GLW is the only name in the initiation where Bernstein is BELOW consensus EPS; CSCO is a pure multiple call. Neither has a house model.**

### 11. MU / SKHYNIX (memory price path) — Fubon's DRAM contract price falls 16% from the 2Q27 peak while Micron says supply stays constrained through CY28
- **Fubon (pp.27-28):**
  - Commodity DRAM contract (TrendForce-based): **1.45 → 1.81 → 2.10 → 2.17 → 2.25 (2Q27 peak) → 2.17 → 2.03 → 1.91 → 1.89 (2Q28)**. That is −3.2% / −6.7% / −5.7% / −1.5% q/q from 3Q27, and **−16% from peak to 2Q28**.
  - Blended HBM: $18.0 → **$26.1/GB peak in 2Q27** → $24.8 (−5%).
- **Micron (09-30):** industry DRAM bits are ~low-20s % in CY27 and CY28, with *"the industry to remain supply constrained in both years"*. FY27 brings *"a more moderate rate of price increases"* (still increases through Aug-27). CY27 HBM is contracted at *"significant price increases"*.
- **BBG MU** (FY-Aug):

| Item | FY28 (2FY) | FY29 (3FY) |
|---|--:|--:|
| Revenue | $312.2bn | $325.5bn |
| EPS | $202.74 (+21% y/y) | $206.81 (flat) |
| GM | 85.2% | 80.7% |

  Consensus therefore already pencils in a margin roll in FY29, but none in FY28.
- **The tension:** Fubon has commodity DRAM prices falling through Jul-27 → Jun-28, which is MU's FY28. That collides with Micron's "supply constrained in 2028" and with consensus FY28 EPS growth of +21%.
- ⚠️ **Units:** Fubon labels the series "US$/GB", but $1.45 is ~1/8 of the open-market DDR ~$13/GB the page carries (UBS 06-25). That points to a **per-Gb** price mislabelled as per-GB ($1.45/Gb ≈ $11.6/GB). The *shape* is usable; the *level* is not.
- ➤ **Action: the shape (peak 2Q27, −16% into 2Q28) is the first dated commodity-DRAM rollover from a primary on the page; reconcile it against MU FY28 consensus before treating FY28 EPS growth as safe. Do not quote the level until the unit is confirmed on the page image.**

---

## Where the new data CONFIRMS (no action)

| Datapoint (source) | Prior wiki | House | BBG live (10-01) | Verdict |
|---|---|---|---|---|
| AVGO / OpenAI Jalapeño: 1.3 GW in 2027 (Broadcom, via Bernstein) ≈ 5.65k racks at ~180 kW; XPU $2,880K per rack incl. ~$0.85M consigned HBM (Bernstein Exhibit 4, page image) | 09-28: AVGO talks $20-30bn per GW | implied ~$11.6-12.5bn per GW (09-28 report) | n/a | ✓ 5.65k × $2.88M ≈ $16.3bn ⇒ **≈$12.5bn per GW incl. HBM / ≈$8.7bn ex-HBM** (my arithmetic). This brackets the house's ~$12bn per GW and sits well below AVGO's $20-30bn talk. ⚠️ Fubon's base case has 930.4k Jalapeño units in 2027 (1.5mn bull); not reconcilable to racks without a per-rack count |
| GOOG TPU shipments: Bernstein 4.28mn (2026) → 8.96mn (2027); Fubon 4.51mn → 9.23mn (Anthropic 0.9 / 3.3mn) | 09-26 Jefferies relay of Fubon: Anthropic 1 / 3.4mn | GOOG GW ~4.6 / ~7.75 | n/a | ✓ Two independent primaries agree within 3-5%. The relay's Anthropic split is corrected to 0.9 / 3.3mn |
| MEDIATEK: Fubon P&L 2026F NT$656.1bn / 2027F **NT$1,223.6bn** sales; 2027F op profit NT$236.6bn; Buy, TP NT$6,000 | TP NT$6,000 last logged 07-22 | no house model | 1FY NT$665.7bn / 2FY **NT$1,160.6bn**; EBIT 2FY NT$248.1bn; PT NT$5,970 (n=32); px NT$4,980 | ✓ TP at consensus (+0.5%). 2027 sales +5.4% but op profit −4.6% vs consensus (higher opex, similar GM 44.3% vs 44.1%). ⚠️ Fubon's 3Q26F NT$152.6bn is at the bottom of the NT$152.2-159.8bn guide, so the page appears to be a post-2Q26 vintage |
| TSM 3Q26: JPM US$45.8bn, GM 66.8% (top of guide) | guide US$44.6-45.8bn, GM 65-67% | n/a | 1FQ NT$1,453.7bn (≈US$45.9bn at 31.65), GM 66.35% | ✓ Revenue at consensus; JPM is +45bp on GM |
| AMD: Bernstein ~726K GPUs in 2027 ⇒ ~10K MI455X Helios racks; Exhibit 4 XPU $3,472K + HBM $952K per rack | GS DC GPU revenue 2027 $42.3bn (09-28) | no house model | FY2 (2027) total revenue $88.74bn | ✓ 10.08k racks × $4.42M ≈ $44.6bn (my arithmetic), +5% vs GS. ⚠️ Bernstein's Exhibit 55 Helios BOM (GPU $3,600K + HBM $1,642K) would give ≈$52.8bn; the two exhibits disagree |
| ANTHROPIC (private): Bernstein Exhibit 16 run-rate $9bn (Jan-26) → $19bn (Mar) → $47bn (May) → **$65bn (Jul-26)**; IPO expected Nov/Dec | 08-19 desk flow "~$65bn ARR at end-July"; secondary ">$70B by late July"; SemiAnalysis ">$60B (3Q26)" | — | — | ✓ Matches the page's end-July mark. A third-party compilation, not company data. Exhibit 17's MAU "B" unit is garbled and not carried |
| SNPS (GTF Letter 5, buy-side): 25x NTM consensus at $426 (09-25); CDNS 38x at $326 = 51% premium; Street EPS growth "mid-to-high teens" in FY27 | — | no house model | FY26 (Oct) EPS $15.14 / FY27 $18.48 (**+22%**); CDNS 2026 $8.15 / 2027 $9.54; px SNPS **$490.54** / CDNS $350.73 | ✓ Premium reproduces on BBG: NTM ≈ 23.4x vs 35.5x = **~52%** (my arithmetic; GTF uses S&P CapIQ). ⚠️ BBG FY27 growth is +22%, above GTF's "mid-to-high teens". SNPS is +15% since the letter's reference price |
| NVDA / VR NVL72 rack BOM: pod $7,520K, networking $1,170K (15.6%); GB200 NVL72 $4,130K, networking 22.5% (Bernstein Exhibit 4, page image) | page carried rack-cost framing from GS/SemiAnalysis | revenue per chip ~$83k (house arithmetic) | n/a | ✓ Consistent with the house's revenue per chip (see DIVERGES #3) |
| AAOI capacity (MS 10-01): "~12M 800G/1.6T units" annualised; Innolight 44.3M + Eoptolink 56.7M = ~101M, ">8x AAOI" | AAOI March deck capacity rows on the page | n/a | cons PT $140.67 (n=8); px $107.32 | ⚠️ MS's own exhibit annualises 650K per month to 7.8M, not 12M. On 7.8M the China pair is ~13x AAOI. Internal inconsistency flagged; no estimate to reconcile |
| FCC Covered List rule (MS 10-01): phased in at 3.2T, "potentially as soon as October"; Chinese modules importable with ≥65% US BOM content | 08-04 → 09-27 ban narrative on optical-cpo; Jefferies 08-05 "no Chinese optics company on the Covered List" | n/a | n/a | ✓ Narrows the earlier "2.4T and beyond" framing and leaves the 800G/1.6T base untouched. Qualitative; timing conflict with GS 3.2T units is logged in DIVERGES #5 |
| Micron NAND: DC SSD revenue "nearly $10bn" in FQ4, >⅔ of NAND; NAND industry bits low-20s % CY26 → ~mid-20s % CY27-28 | JPM Sur DC SSD ">$5B again" (09-28) | — | SNDK FY27 (Jun) $48.83bn / EPS $212.55 | ✓ Supports the NAND-tightness camp. DC SSD is ~2x JPM's bogey (already scored on MU.md) |

---

## BBG leg — status
LIVE. `bdp` was served by the local Terminal on 2026-10-01 for 22 tickers (MU, LITE, COHR, CIEN, ANET, CSCO, GLW, CLS, 2330 TT, 2454 TT, NVDA, AMD, AVGO, SNPS, CDNS, META, GOOGL, MRVL, 000660 KS, 005930 KS, AAOI, SNDK), across the 1FQ/2FQ/1FY/2FY/3FY overrides. Nothing is PENDING. CY2026/CY2027 sums come from the on-disk `_data/estimates.json` (asof 2026-10-01), with the pre-print-embedded-quarter caveat. ⚠️ The MU 1FY line is post-print on FQ1 but likely only partly revised for FY27. Re-pull after a week of post-print revisions before treating the FY27 consensus as settled. TSMC NT$ → US$ conversions use JPM's own implied rates (31.65 / 31.70 / 31.70); they are approximations, not BBG USD fields.

## Model bridges suggested
1. **COHR**: restate the house PT on FY28 (or CY28) EPS alongside the CY27 25x framing. The house is $128 below the median on a CY27 P&L within 5% of consensus.
2. **NVDA units**: 2027 packages × revenue per package by product, against Fubon's 11.56mn and Bernstein's VR NVL72 BOM (~$74k per package XPU + HBM).
3. **TSM**: roll the 06-10 model for 1H26 actuals; add a 2027-28 capex line and test US$75 / 86bn (Street) vs US$86 / 100bn (JPM).
4. **META capex**: size Muse compute as $4.07 × DAU × 12 (Barclays) against the house's $170bn CY27.
5. **Optics TAM**: pick GS-rollover vs Bernstein-CAGR explicitly in the consolidated optics model (LITE, COHR).
