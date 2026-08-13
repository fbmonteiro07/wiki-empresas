# Reconciliation — 2026-08-12 (/run-inbox, 55 files)

_Every NEW quantitative datapoint from this run, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`, 8 names), (3) BBG consensus. Qualitative/thematic notes are skipped._

> ## ⚠️ BBG COLUMN — PARTIALLY PENDING
> **A live BBG pull was attempted twice at 23:20 and FAILED both ways** — local blpapi refused on `127.0.0.1:8194` ("could not start session / Terminal not running or logged out"), and the `BBG_SERVER_FIRST=1` route returned the same `ConnectionError`. **Terminal is logged out and/or the Capstone VPN is down.**
>
> **However, `_data/estimates.json` carries a SUCCESSFUL same-day pull (`asof 2026-08-12`, 98 companies, 0 null prices — validated against the known all-null-wipe failure mode).** That snapshot is used as the consensus baseline throughout and is labelled as such. **It is a snapshot, not a live quote.**
>
> ⚠️ **38 names in that file were CARRIED OVER from 2026-08-11 rather than refreshed.** Of the names in this reconciliation, the stale ones are **ETN, NBIS, CRWV, AKAM** — flagged inline as `[STALE 08-11]`. Every consensus figure for those four is one day old.
>
> **No web data was substituted for consensus.** Re-run `/wiki-consensus` once the Terminal is back to convert the flagged rows.

---

## DIVERGES — the alpha

### 1. 🔴🔴 STX — two bulls, same name, same horizon, ~2x apart on EPS. The single widest gap in this run.

| Source | 2028 EPS | Basis |
|---|---|---|
| **UBS · Timothy Arcuri** (2026-07-29) | **$110–120** | Blended pricing accelerating past +8%, costs down mid-teens, GM to "mid-70s a year from now" |
| **Bernstein · Newman/Li/Sun** (2026-08-07) | **$64.40** | FY28E, PT $1,350 at 21x |
| **BBG consensus** (snapshot 08-12) | CY2027 **$45.20** | — |
| Price | **$878.21** | Bernstein PT implies +54%; Arcuri's EPS at Bernstein's 21x implies **$2,300–2,520** |

**Why this is not a rounding difference.** Both houses are bullish, both underwrite the same mechanism (HAMR mix + supply discipline + pricing), and they are **~80% apart on 2028 earnings power**. Arcuri's own framing is a direct shot at the sell-side: *"I do not know why my competitors do not have gross margin somewhere in the MID-70s a year from now… it's not rocket science."*

**The testable bridge is pricing PERSISTENCE, not level.** Both agree on the observed series — blended pricing **+4% (Mar-q) → +7% (Jun) → ~+8% (Sep guided)**. Arcuri's number requires it to keep rising sequentially **beyond +8%** *"as what they put in the hopper a year ago ships out"*; Bernstein's does not. Bernstein independently supplies the check that makes this resolvable: **~6% q/q June pricing**, and the disclosure that **POs are set 4–5 quarters before shipment with ~3 quarters of production lead time** — i.e. the next two quarters of price are already largely contracted and observable.

⚠️ **Arcuri's own bear case is unusually explicit and belongs in the same box: *"this thing is going to be MORE CYCLICAL THAN MEMORY in the downturn… when this turns off for drives, it is either on or it's off."*** ➜ **Action: this is a live, dated, falsifiable disagreement on a name where consensus sits below BOTH houses. Highest-value item in the run.**

### 2. 🔴 WDC — a rating change the wiki never carried, and a 6.4x price-target move

**Bernstein: Market-Perform $120 → OUTPERFORM $770** (21x FY28E EPS **$36.58**), price $454.10.
- **vs prior wiki:** the page had **no Outperform mark at all** and carried the stale $120. Old value moved to Changelog.
- **vs consensus:** CY2027 EPS **$26.06** — Bernstein's FY28 is **+40%** above the consensus CY27 mark one year earlier.
- **Corroboration from a different seat, same week:** WDC's post-print management callback (UBS/Arcuri, 08-06) gives **HAMR qualified at 4 customers with failure rates ~half of Seagate's at a similar stage**, production ramp **1H CY27**, **50T ePMR in 2H CY2027**, cost/TB **−10%**.
- ⚠️ **The offsetting fact, also from management: LTAs reprice every 3/6/9/12 months and current pricing was negotiated ~1 year ago** — so realised WDC pricing lags the spot series that is driving the STX bull case above.

➜ **Action: the HDD complex now carries two Bernstein Outperforms and a Street that is materially below on both. The pair trade is STX-vs-WDC on HAMR timing, and the wiki now has both sides dated.**

### 3. 🔴 SNDK — the LTA debate is a MULTIPLE debate, and two houses take opposite signs off the identical fact

Fact, undisputed: **two-thirds of SNDK volume sits on LTAs at an 80% floor gross margin.**

| House | Reading | Mark |
|---|---|---|
| **Bernstein** (08-07) | *"greater LTA coverage is POSITIVE for the stock's multiple and re-rating potential… reduce perceived cyclicality"* | **Outperform, PT $3,000** = 11x FY28E EPS $272.09 |
| **Jefferies · Blayne Curtis** (08-07, same day) | *"if you're signing deals at 80% gross margin, your ASPs are not going up as much… **THE MULTIPLE CONTRACTS**"* | — |

- **vs consensus:** CY2027 EPS **$236.66**; Bernstein's FY28 $272.09 is +15% on top of that. Price **$1,344.29** ⇒ Bernstein PT implies **+123%**.
- **The split is clean and resolvable:** Bernstein is pricing **reduced downside variance**; Jefferies is pricing **forgone upside**. ➜ **The resolution comes from what spot does NEXT, not from the LTA terms themselves.** If spot NAND keeps climbing, Jefferies is right that the LTAs cap participation; if spot rolls, Bernstein is right that the floor is worth a multiple.

### 4. 🔴 COHR — the house model is ~92% above consensus on 2027 EPS. This is the largest house-vs-Street gap on the board and it needs a bridge.

| | CY2026 | CY2027 | CY2028 |
|---|---|---|---|
| **Capstone house** | rev **$9.1bn**, EPS **$8.27**, GM 40% | rev **$16.6bn**, EPS **$19.21**, GM 41% | rev $19.6bn, EPS $23.60 |
| **BBG consensus** (08-12) | rev **$8.25bn**, EPS **$6.82** | rev **$11.19bn**, EPS **$10.00** | — |
| **Gap** | rev +10%, EPS **+21%** | rev **+48%**, EPS **+92%** | — |

**What this run adds to the bridge — and it supports the house on the near term:** COHR's own FY26 print (08-12) delivered **revenue $7.12bn (+23% reported / +28% pro forma)**, **non-GAAP GM 39.4% (+152bps)**, **OM 20.5%**, **EPS $5.61 (+59%)**, with **FQ1 FY27 guided to rev $2.2–2.4bn (mid $2.3bn) and EPS $1.85–2.05 (mid $1.95)** — an annualised run-rate of **~$9.2bn revenue / ~$7.80 EPS entering FY27, i.e. already at the house's CY2026 marks.** Management targets its **first >$3bn revenue quarter by end of fiscal '27** (~$12bn annualised) and says **FY27 is completely booked**, with POs through end-CY27 and into CY28 and **LTAs to end-decade at agreed pricing for the full term**.

⚠️ **But the house's CY2027 $16.6bn requires ~$4.15bn/quarter — roughly 38% ABOVE management's own end-FY27 ">$3bn quarter" target.** ➜ **Action: the near-term half of the house model is corroborated by the print; the 2027 leg is not, and the gap to management's own stated milestone is the specific thing to defend or cut.** Note the house GM (41%) is *below* management's >42% target, so the gap is entirely volume, not margin.

🔴 **Also corrected this run (was a wiki error, not a divergence): the page had logged COHR's FQ1 GM guide as the TOP of the range — "41.5% vs Street 40.0%, +150bps." The actual guide is 39.5–41.5% and the CFO stated the midpoint at 40.5% ⇒ +50bps vs Street.** This is a better explanation of the −5% reaction than "Industrial was softer," and it partly invalidates the margin-catalyst case MS used to prefer COHR over LITE.

### 5. 🔴 LITE — house is ABOVE consensus on 2027 and BELOW on 2026; the new Redburn PT sits between them

| | CY2026 | CY2027 |
|---|---|---|
| **Capstone house** | rev **$4.2bn**, EPS **$12.81**, OM 32% | rev **$8.1bn**, EPS **$30.02**, OM 43% |
| **BBG consensus** (08-12) | rev **$4.50bn**, EPS **$14.30** | rev **$7.86bn**, EPS **$27.40** |
| **Gap** | rev −7%, EPS **−10%** | rev +3%, EPS **+10%** |

- **New sell-side marks this run: R&Co Redburn Buy, PT $1,270.27** (price $932.47 ⇒ +36%); **Jefferies frames the 2028 bar as *"most people have had $50"* with *"no more than a 20 multiple"* ⇒ ~$1,000.**
- ⚠️ **The house's shape — below Street in 2026, above in 2027 — is a TIMING call, and this run supplies the first hard test of it.** The Q4FY26 print beat on every line and pulled the $1.25B target model in *"more than a quarter ahead of schedule,"* which is evidence AGAINST the house's below-Street 2026. ➜ **Action: the 2026 leg of the house model looks too low after the print and should be re-marked; the 2027 leg is the part worth keeping.**

### 6. 🔴 GOOG — a three-way spread on 2026 EPS, with the house at the BOTTOM

| Source | 2026 EPS | 2027 EPS |
|---|---|---|
| **BofA** (IR callback, 07-23) | **~$15.00** (raised from ~$14.70) | — |
| **BBG consensus** (08-12) | **$12.94** | $16.50 |
| **Capstone house** | **$11.80** | $16.20 |

**The house is 9% below consensus and 21% below BofA on 2026, while sitting in line on 2027.** ⚠️ **Given Q2 delivered capex doubling y/y to $44.9bn, the 2026 outlook raised to $195–205bn, cloud backlog +385% to $514bn and paid clicks reaccelerating to +13%, a 2026 EPS 9% below the Street is a position that needs defending or cutting — it is the kind of stale-low mark that quietly becomes a short thesis the desk does not actually hold.**

⚠️ **Two capex marks that do NOT net, and matter for [[AVGO]]:** MS took 2027 capex **$350bn → $375bn** — but **partly because it now assumes FEWER third-party TPU sales** (4 GW of 2028 external TPU may go on-prem). **Do not read the capex take-up as a straight merchant-ASIC positive.**

⚠️ **Basis discipline flag: BofA's "TPU revenue" plug of $0.5–0.6bn for 2Q26 sits against the Capstone 10-Q triangulation of $1.2–1.3bn already on the page — a ~2x gap on a number Alphabet does not disclose. Not netted.** Separately, both BofA and GS now bracket **TPU-system EBITDA margin at ~30% / mid-30s–40%+**, against a previously feared mid-teens.

### 7. 🔴 TXN — UBS is 17% above consensus on 2027, and the PT moved twice without the wiki catching the first

- **UBS PT $350 → $380** (2026-07-23). ⚠️ **The page had been carrying a stale $245 from 2025-12-22** — old value moved to Changelog. Price **$276.59** ⇒ +37% to the new PT.
- **UBS 2027E: revenue $26–27bn, EPS ~$12, cash ~$13.50/share** vs **consensus CY2027 EPS $10.30, revenue $25.0bn** ⇒ **UBS +17% on EPS**.
- **The bridge is disclosed and checkable:** Sep-Q gross margin **+140–150bps q/q** (UBS explicitly corrects the earnings call, where *"somebody said gross margin is flat for the guidance. That's wrong"*), Sep-Q y/y cash drop-through **~80%** with *"not much pricing in it"*, and **data-centre at $2.7bn in 2026**.
- **Management (TXN IR, 08-06) supplies the counterweight:** **FCF/share ladder $20bn rev → $8–9 … $26bn → $11–12** on $2–3bn capex, **1H26 pricing net ~flat**, and a *normal* seasonal Q4 **down mid-to-upper single digits q/q**. ➜ **UBS's $12 requires the upper half of that ladder; the ladder is management's own, so the divergence is arithmetically bounded.**

### 8. 🔴 INTC — BofA is ~50% above consensus on 2026 EPS

**BofA ~$1.50 (2026, ex-foundry-upside baseline) vs BBG consensus CY2026 $1.01** (+49%); BofA PT **$160** vs price **$100.95**. Path: *"rule of 45"* on 15% top-line ⇒ **~$2/$3/$4/$5 → ~$5 by 2030**; the $160 PT is explicitly conditioned on **INTC reaching ~10% of the foundry market**.
- ⚠️ **The wiki now carries a relay-vs-primary correction that cuts in Intel's favour and should be read alongside:** the 08-03 UBS relay had Intel IR calling Diamond multi-threading *"a mistake"*; the **primary 07-28 transcript has Pitzer drawing the opposite inference** — single-threaded workloads mattering more *"gives us some optimism that Diamond is actually a MORE COMPETITIVE product than we would've thought."*
- ⚠️ **Against the bull: KLA does not get paid twice for Intel.** Arcuri's arithmetic — Intel capex **~$20bn → ~$30bn** (WFE **$12–13bn → ~$23bn**) 2026→2027 with **KLA revenue ~FLAT**, because KLA *"massively out-shipped WFE"* at Intel in 2026 on pulled-forward tools. **This directly contests the "KLAC is the way to play Intel" framing the wiki carried on 08-11.**

### 9. 🔴 SKHYNIX / SAMSUNG — Mirae is the only house to re-cut after the print, and it cut CAPEX into an up-guided capex cycle

| | Mirae (08-11) | BBG consensus (08-12) | Gap |
|---|---|---|---|
| **SKHYNIX** 2026F OP | **W268,072bn** | W266,376bn | +0.6% (in line) |
| **SKHYNIX** 2026F EPS | **W364,482** | CY2026 W318,057 | **+14.6%** |
| **SKHYNIX** TP | **W2,800,000** | price W1,521,000 | **+84%** |
| **SAMSUNG** 2026F EPS | **W46,469** | CY2026 W46,404 | +0.1% (in line) |
| **SAMSUNG** TP | **W370,000** | price W258,000 | **+43%** |

🔴 **Caught a stale street-high on the wiki: the SKHYNIX page had carried "Mirae/Jefferies ~W4.2m" since 07-14. Mirae's own TP history shows the cut to W2,800,000 on 2026-07-29** — the page was ~50% too high on its own cited street-high for two weeks. Corrected, old value in Changelog.

⚠️ **The genuine divergence is capex, and it points the wrong way: Mirae cut SK hynix capex ~10% at both years (W56.9/79.7tn → W51.2/71.7tn accrual) EVEN AS THE COMPANY GUIDED CAPEX UP ~80%.** Either Mirae is modelling slippage the company is not conceding, or the accrual-vs-cash basis is doing the work. ➜ **A house cutting Korean capex into an up-guided cycle is exactly the kind of divergence to interrogate — it reads directly to [[AMAT]]/[[LRCX]]/[[KLAC]]/[[TOKYOELEC]] order books.**

### 10. ⚠️ AKAM — the CEO gave two different FY27 growth numbers on the same call, and they straddle consensus

**Consensus implies +13.1% FY27 revenue growth** (CY2026 $4,491.75m → CY2027 $5,081.22m). On the same 08-10 call the CEO said **"mid-teens"** early and **"we should be in the low teens next year"** later. ➜ **Consensus sits at the low end of the CEO's own range. The page's low-teens mark (GS, 08-07) was NOT superseded — correctly, since the primary contradicts itself.** Everything else on that call is corroborative rather than divergent: **$2.8bn of multi-year CIS commits signed YTD**, CIS growth **+39% last quarter / ~50% FY26**, **$1 capex → $1 of ARR** on ordinary deals and **≥2:1 revenue-to-investment on mega-deals**. ⚠️ **The one item that is genuinely forward-risky: $500M of incremental GPU capex, largely FY27, with the "large majority" for customers NOT YET SIGNED.**

### 11. ⚠️ NBIS / CRWV — consensus has not absorbed the disclosed backlogs `[STALE 08-11]`

- **NBIS:** ARR **$3.0bn at end-June** (+598% y/y) against **consensus FY2026 revenue of $3.23bn** — i.e. the exit ARR alone roughly equals the full consensus year. **Contracted/committed backlog ~$40bn** against **consensus CY2027 revenue of $11.74bn**. **YE26 contracted power raised to 5 GW** (from >4 GW), with **">1 GW per year deployment starting 2027."**
- **CRWV:** **contracted power 4.2 GW** plus **>1.5 GW of optioned power** ⇒ management's *"close to about 6 gigawatts already."* Jefferies models **implied RPO $200–230bn vs $99bn today** at $12bn/GW over a 5-year average duration, against **consensus CY2027 revenue of $26.2bn**.
- ⚠️ **Both consensus rows are one day stale, and both companies are loss-making at the consensus line (NBIS CY2026 EPS −$3.55, CRWV −$3.86), so the EPS comparison is not meaningful — the divergence is a REVENUE-RECOGNITION-TIMING question, not an earnings-power one.** ➜ **Re-run once the Terminal is up.**
- 🔴 **The cross-cutting number that reprices both: GW monetisation went from $8–12bn to $30–50bn per GW in six months (3–5x)** — but ⚠️ *"all those 30 to 50 have the option for a 90-DAY LEASE CANCEL,"* so **headline deal size ≠ committed size**, and Jefferies is explicit that the benefit accrues to the **hyperscalers**, not to [[ORCL]] or [[CRWV]] *"where you're doing a five-year contract with LOCKED-IN unit economics."*

### 12. ⚠️ AMD — UBS's 2027 DC number is far above the figure floated on the call

**UBS: 2027 DC GPU "mid-40s" $bn**, explicitly rejecting the **$30bn** floated on the call as *"way, way too low"*; **~$30bn incremental GPU + ~$20bn incremental CPU ⇒ ~$70bn total DC north star for 2027.** Against **consensus CY2027 total revenue of $86.6bn**, a $70bn DC segment implies DC is ~81% of the company. **FY26 bar ">$15bn" DC GPU ⇒ Dec-Q ~$6.5bn** vs Jun-Q $2.75bn — a very steep implied exit.
- **Corroborated from the customer side this run, which is what makes it interesting:** an [[ANTHROPIC]] infrastructure practitioner says the two gates have cleared — **software** (*"PyTorch-native workloads, software stability, observability… have gotten much better over the past two years… WHICH IS WHY NOW IT'S THE RIGHT TIME"*) and, decisively, **packaging/scale-up** (*"MI355 was good but VERY LIMITED — only eight together, a TRAY solution. But NOW AMD HAS A RACK-SCALE SOLUTION… VERY COMPARABLE TO AN INFINIBAND [NVL]72"*).
- ⚠️ **UBS's own "$70 billion for this year" phrasing is internally inconsistent** — the arithmetic only closes for 2027. Carried as 2027 with the misstatement flagged.

### 13. ⚠️ PWR / VRT / NVT / ETN — Bernstein's marks are mostly IN LINE; the divergence is the framework, not the numbers

| Ticker | Bernstein 2026E / 2027E EPS | Consensus CY2026 / CY2027 | Read |
|---|---|---|---|
| **PWR** | **$16.90 / $19.24** | $15.09 / $19.50 | **+12% 2026**, in line 2027 |
| **VRT** | $6.60 / $9.06 | $6.47 / $9.23 | in line |
| **NVT** | $4.84 / $6.26 | $4.69 / $6.47 | in line |
| **ETN** `[STALE 08-11]` | $13.45 / $16.37 | $13.40 / $15.84 | in line 2026, **+3% 2027** |

⚠️ **Note the SHAPE of the PWR action: rating held at Market-Perform, PT $538 → $748 (+39%), 2026E EPS $13.04 → $16.90 (+30%). Bernstein marked to earnings power it had underestimated; it did not re-rate the stock.** A PT raised 39% on an unchanged rating is a house telling you it was wrong on numbers, not that it has changed its mind.

🔴 **The real divergence is an INPUT, and it is ~7x wide.** Bernstein's whole 35 GW/yr labor ceiling is computed off **1,772 MEP man-hours/MW and ~0.9 workers/MW**. SemiAnalysis (07-29, already on these pages) uses **~12,000 field man-hours/MW and ~6 workers/MW at peak**. Different bases (full-project average across shell+TFO vs peak-concurrency fit-out field hours) explain part of it, **not a factor of seven**. ➜ **If SemiAnalysis is closer to right, Bernstein's ceiling is materially too generous and its central conclusion — *"enough to support the consensus view of 25–35 GW/year"* — INVERTS into a binding constraint. Neither figure was overwritten; both sit side by side.**

### 14. ⚠️ META — the house sits above both the Street and the pre-print bar

**House 2027 EPS $38.24** vs **consensus CY2027 $36.39** (+5%) vs **MS's pre-print bar of *"closer to 35 than 33"***. The house is the highest of the three. ⚠️ **MS characterises META's NeoCloud effort as *"Plan B," H100s not Blackwells — an earnings floor, not a multiple driver**, and ranks META **4th of five** on installed capacity by YE2028. ➜ **A house above Street on a name the covering analyst ranks second-from-bottom on compute capacity is a position worth re-testing.**

---

## CONFIRMS — no action

- **LITE Q4FY26 print** beat every published bogey (rev $1.006–1.010B vs Street $988–990M; GM 50.4% vs 48.5–48.8%; EPS $3.23 vs $2.97) and the F1Q27 guide midpoint **$1.250B** cleared UBS $1.15–1.20B, MS $1.175–1.20B and Jefferies/whisper $1.25B+. **Confirms the intra-quarter flow's direction; the flat tape is an expectations verdict, not a fundamental one.**
- **CY2027 WFE:** BofA **confirms $190bn** on a client call (it did NOT raise), matching **KLAC's ">$190bn"** and **TOKYOELEC's ">$190bn"**. UBS's *"up at least 30%, probably more like 35%"* off a ~$150bn 2026 base lands at **~$195–203bn**. ➜ **Three houses and two vendors now cluster at ~$190–203bn against Bernstein's $204bn — the CY27 cluster TIGHTENED this run rather than widening.**
- **VRT / NVT** — Bernstein in line with consensus at both years; no action.
- **SAMSUNG 2026F EPS** — Mirae within 0.1% of consensus; the divergence on that name is the TP and the capex, not the earnings.
- **SKHYNIX 2026F OP** — Mirae within 0.6% of consensus.
- **GLW** — the $10bn Photonics-by-end-decade opportunity is reconfirmed as **architecture-agnostic** (*"includes assumptions for both NPO and CPO"*), and **GlassBridge is NOT a new announcement** — a 2025 paper already embedded in the $10bn target. **Confirms the existing page; no estimate change.**
- **UBER** — Avride's 60,000+ commercial rides and >200-vehicle fleet are **pilot-scale against Uber's trip base**: directional on partner momentum, immaterial to near-term revenue. No estimate implication.
- **SPOT** — the model-routing citation is a **cost-structure datapoint with no rating, PT or estimate** attached; it bears on the AI-inference-cost bear (MS 05-08), not on revenue.
- **NXPI** — no new numbers; the UBS downgrade rationale (China auto inventory build) was put to TXN management, who **neither confirmed nor dismissed it**. The debate is live but unresolved and unquantified.

---

## Cross-cutting items that are not single-name reconciliations

1. **Memory is now ~15–20% of the entire gigawatt bill of materials** (memory ~25% of the Rubin RACK cost × IT ~60% of total GW cost), **up from GB300**. Willingness to bear it is judged *"pretty high"* on the ROIC frameworks. ➜ **Reads to every hyperscaler margin model and to [[MU]]/[[SKHYNIX]]/[[SAMSUNG]] pricing power.**
2. **2027 HBM pricing has a bear-side ceiling of +20–30%** set by NVDA's ~75% system-margin defence, against a modelled doubling (~$550 → $1,200–1,400). **The low end of every input on the wiki** — and it predicts **HBM ASP decelerates while HBM VOLUME does not**, which is a different failure mode from the one currently modelled.
3. **HBM cost accounting differs by vendor and drives reported GM:** NVDA marks up, AVGO passes through at cost, MRVL consigns. **Jefferies: AVGO's ASIC gross margin goes *"from like 60 to 50 pretty quick."*** ➜ **Directly contests the 75.5%/75.2% FY27/28E GM held in the 08-09 Mizuho model on AVGO.md. Any cross-vendor revenue-per-XPU comparison must be basis-checked.**
4. **"2027 is going to be the LAST significant second-derivative step-up in capex throughout this cycle"** (MS) — a dated rotation call between semis, hardware, memory and software/internet.
5. **NAND greenfield timing is contested between two equipment vendors:** LRCX management says true capacity addition is **2H2028** (clean room the 2027 constraint); KLA's Rick Wallace said 2027 sees *"some greenfield investment in flash."* **LRCX is the more specific and is management on its own order book.**

---

_Baselines: prior wiki comments (on disk) · `_data/house.json` asof 2026-08-12 (8 names: AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM) · `_data/estimates.json` BBG snapshot asof 2026-08-12 (98 names, 38 carried over from 08-11). **Live BBG PENDING — Terminal logged out at 23:20; re-run `/wiki-consensus` when back.**_
