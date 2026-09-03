# Reconciliation — /run-inbox 2026-09-02

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines:
**(1) prior wiki comments** · **(2) Capstone house models** · **(3) BBG consensus** (live pull, `E:\bloomberg_api`, 2026-09-02).
DIVERGES = the alpha. CONFIRMS = no action._

**Bloomberg status: LIVE** — Terminal logged in, VPN up. No PENDING column this run.
All consensus figures below are `BEST_*` with `BEST_FPERIOD_OVERRIDE` in `1FY/2FY/3FY`, pulled 2026-09-02.
**USDTWD 31.728** (pulled, not assumed).

> ### ⚠️ BASIS NOTES THAT GOVERN THIS REPORT — READ FIRST
> 1. **AVGO and CRDO have off-calendar fiscal year-ends** (AVGO ~1-Nov, CRDO ~30-Apr). Per standing rule, every
>    figure below uses the **1FY/2FY/3FY annual override, never the CY block** — the CY label lies for these names.
>    AVGO 1FY=FY2026 / 2FY=FY2027 / 3FY=FY2028. CRDO 1FY=FY2027 / 2FY=FY2028 / 3FY=FY2029.
> 2. **TSM `BEST_EPS` is per-ADS but denominated in TWD** (ADR = 5 ordinary shares). The Capstone house model is
>    **per ORDINARY SHARE in NT$**. Comparing them without the ×5 makes an in-line house look ~80% light.
>    Every TSM EPS comparison below is stated on an explicit basis.
> 3. **GOOG `BEST_EPS` at 1FY is CONTAMINATED and must not be used.** BBG 1FY `BEST_NET_INCOME` is **$244,653m
>    against `BEST_EBIT` of $171,405m** — net income exceeds EBIT by ~$73bn, i.e. a large below-the-line item sits
>    in the 2026 number. The apparent 2026→2027 EPS *decline* ($18.699 → $16.015) is an artifact of that item, not
>    a forecast. **Reconcile GOOG at EBIT.** (New trap; not previously logged.)
> 4. **`BEST_CAPEX` for GOOG could not be validated** (1FY −$308.1bn / 2FY −$347.3bn = 71%/64% of consensus
>    revenue, and inconsistent with the house's $183bn/$310bn). Marked **UNRESOLVED**; no capex variance is
>    published for GOOG below rather than publish a number I cannot stand behind.
> 5. **Period-basis discipline:** AXT's "$60-65m" is a **QUARTERLY, PRODUCT-LEVEL (InP only)** figure; consensus
>    "$222m" is **ANNUAL, TOTAL company**. They are not comparable and are not compared.

---

## 🔴 DIVERGES — the alpha

### D1 · AVGO — consensus is AT the FY27 guide but ~18% BELOW the FY28 guide. The whole debate is FY27-vs-FY28 phasing, and it is a VOLUME gap, not a margin gap.

| FY28 (3FY) | Value | vs BBG |
|---|--:|--:|
| BBG consensus revenue | **$236.9bn** | — |
| Guide-implied total revenue *(our bridge)* | **~$290bn** | **+22%** |
| BBG consensus EPS | **$26.175** | — |
| Management guide | **">$30"** | **≥ +15%** |

**Our bridge, with assumptions stated:** management guided **AI semis only** ($115bn FY27, $230bn FY28). Adding the
two segments it did *not* guide out-years for — non-AI semis at the $4.2-4.3bn/qtr run-rate growing ~5%/yr
(~$17.3bn FY27, ~$18.2bn FY28) and infrastructure software off a ~$34bn FY26 base at +12%/+10% (~$38bn, ~$42bn) —
gives **FY27 ≈ $170bn** and **FY28 ≈ $290bn**.

- **FY27: consensus $174.2bn vs our guide-implied ~$170bn → consensus is ~2% ABOVE the guide.** The Street is
  already at (fractionally through) the FY27 number. Nothing left to beat there.
- **FY28: consensus $236.9bn vs our guide-implied ~$290bn → consensus is ~18% BELOW.** This is the gap.
- 🔴 **THE DECOMPOSITION IS THE FINDING: consensus FY28 EBIT margin is $154,500m / $236,909m = 65.2%, i.e. the
  Street ALREADY accepts management's "~66% operating margin sustained". So the entire FY28 shortfall is
  AI-semiconductor VOLUME — not margin, not mix, not opex.** The FY28 debate is a single-variable debate.
- **EPS cross-check — and the reason ">$30" is not independent information:** $290bn × 66% op margin = ~$191bn
  EBIT; less ~$2.4bn interest ($59.6bn fixed-rate debt @ 4% WA coupon); × (1 − 16% tax rate); ÷ 4.94bn diluted
  shares ⇒ **~$32/share**. Management's ">$30 in FY28" is simply its own revenue guide restated at its own
  guided margin, tax rate and share count. **It should not be scored as a second, corroborating datapoint.**

**Action:** the FY28 volume gap is the position. Size it against deployment timing (D2), not against margin.

---

### D2 · AVGO — the Capstone house model's GW ladder MATCHES management almost exactly, but the house books ~20% more AI revenue over FY27-28. The gap is entirely DEPLOYMENT TIMING, and the house should make it explicit.

| | House (2026-06-10) | Management (2026-09-02) |
|---|--:|--:|
| GW deployed FY27 | **9.9** | ~10 *(analyst sum of mgmt's own ladder)* |
| GW deployed FY28 | **19.6** | ~20 *(idem)* |
| AI revenue FY27 | $132bn *(segment line)* / **$139bn** *(GW build)* | **$115bn** |
| AI revenue FY28 | $251bn *(segment line)* / **$274bn** *(GW build)* | **$230bn** |
| FY27+FY28 AI revenue | **~$413bn** *(GW build)* | **~$345bn** |
| FY28 EPS | **$35.96** | ">$30" |

- ✅ **The house's physical picture was right, two and a half months early.** 9.9 / 19.6 GW versus the ~10 / ~20 GW
  that Bernstein derived on the call from management's own customer ladder. That is a genuine forecasting win and
  it should be said plainly.
- 🔴 **But the house implies a flat ~$14.0bn of AVGO content per GW** ($57/4.1, $139/9.9, $274/19.6 — all ≈$14bn),
  which sits between the **$11-12bn/GW implied by dividing management's revenue guide by its own GW ladder** and
  the **$20-30bn/GW of content management actually stated**. The house has, in effect, taken the *demand* GW count
  and applied a *haircut via a low content rate*.
- 🔴 **Management's own reconciliation is different, and it is the one to adopt:** Hock explicitly refuses to equate
  demand GW with shipped GW — *"we're not saying that over the next two years there are 30GW that will go into
  production… we judge it conservatively to be somewhat less."* At his stated $20-30bn/GW of content, ~$345bn of
  revenue implies **only ~12-17GW actually ships** across FY27-28, against ~30GW of demand.
- ➤ **MODEL BRIDGE TO RUN: the house is modelling ~29.5GW of demand as though ~29.5GW ships, at ~$14bn/GW. The
  same $413bn can be reached from ~15GW shipped at ~$27bn/GW. These are NOT the same model — they have opposite
  sensitivities.** Under the house's construction, upside comes from more GW; under management's, GW are already
  sold and upside comes from clearing land/power/shell and substrate/HBM bottlenecks. **Recommend the house split
  its single content-per-GW assumption into (deployed GW) × (ship rate) × (content per shipped GW).** The house's
  ~20% excess over the guide is then explicitly a *timing* call, which is defensible and testable, rather than an
  undifferentiated revenue call.
- ⚠️ **Internal inconsistency in the house model to resolve:** the AI-semis segment line ($63/$132/$251bn) and the
  bottom-up GW build ($57/$139/$274bn) disagree in every year and in **opposite directions** (FY26 −9.5%, FY27
  +5.3%, FY28 +9.2%). Note that the **bottom-up FY26 figure ($57bn) essentially nailed management's actual FY26
  guide of $58bn, while the segment line ($63bn) was 8.6% too high** — the GW engine is the better instrument and
  should probably drive the page.

---

### D3 · GOOG — the house's stated EPS edge has CLOSED. Consensus caught up; the page still claims the old gap.

| 2027E | House (2026-06-05) | BBG 2FY | Gap |
|---|--:|--:|--:|
| Revenue | **$641bn** | $544.2bn | **house +17.8%** |
| EBIT | ~$237bn *(37% margin)* | $217.9bn | house +8.9% |
| EPS | $16.20 | **$16.015** | **+1.2% — in line** |

- 🔴 **The GOOG page's house-read says *"EPS 2027E $16.20 above consensus (~$14.5)"*. BBG now prints $16.015 —
  consensus has risen ~10% and the edge is gone. That claim is STALE and should be corrected on the page.**
- ✅ **But the real house edge was never the EPS line — it is the revenue/compute call, and that one is intact and
  large: +17.8% on 2027 revenue.** The reason the two diverge is the house's own $310bn 2027 capex (≈48% of
  revenue, FCF −$55bn): the house spends its revenue upside on depreciation before it reaches EPS. **State the
  GOOG house view as a revenue-and-capex call, not an earnings call.**
- ✅ **CONFIRMS the capex direction:** the Susquehanna expert call reports Google *"raised capex twice in two
  quarters"* and is **debt-financing the shortfall**, and that Google *"definitely will not be able to meet all the
  demand"*. That is consistent with the house's aggressive capex path.
- ⚠️ **HOUSE-VS-HOUSE INCONSISTENCY — two Capstone models disagree ~2x on the same quantity, five days apart:**
  the **AVGO** model puts Google at **2.5 GW (2026E) / 4.0 GW (2027E)**; the **GOOG** model puts Google compute at
  **~4.6 GW (2026E) / ~7.75 GW (2027E)**. Probably reconcilable (AVGO's row is Broadcom-supplied TPU only; GOOG's
  is likely total compute including GPU and other silicon) — **but neither page says so, and until one of them
  does, any read-across between the two models is unsafe. Resolve and document the definition.**

---

### D4 · AXTI — management's "revenue opportunity exiting 2026" runs ~15-25% ABOVE the consensus-implied Q4. Flagged, deliberately not scored.

- Management (AXT CFO Gary Fisher, BofA-hosted call, 2026-08-31): InP revenue **$17.5m (Q4'25) → $30.691m (Q2'26)**,
  with a **revenue OPPORTUNITY of $60-65m per quarter exiting 2026** versus an original goal of ~$35m/qtr.
  **Q3'26 total revenue guided to $66m** (includes raw materials, per IR's clarification).
- BBG FY2026 (1FY) consensus **total revenue $222.0m**. Backing out the $66m Q3 guide leaves **$156m** for
  Q1+Q2+Q4; on plausible Q1/Q2 totals (~$38m/~$48m) that implies a **Q4 of roughly $70m**.
- Against management's InP-alone $60-65m **plus** non-InP (GaAs, germanium, raw materials, ~$20-25m/qtr), a Q4 in
  the **$80-90m** range is implied — **~15-25% above what consensus embeds.**
- ⚠️ **NOT SCORED AS A HARD DIVERGENCE, because management hedged it themselves:** it was framed as a *"revenue
  opportunity"* — a statement about capacity, hardware, yield and mix — **not a guide**. AXT explicitly declines to
  disclose wafer or 2-inch-equivalent capacity. Treat as a **positive skew to watch into the Q3 print**, with the
  falsifier being the actual Q4 guide.
- ✅ Consensus **2027 revenue $485.2m (+119% y/y)** is consistent with management's "double capacity again in 2027".
  The Street is already underwriting the capacity plan; it is the *within-2026* exit rate it may be light on.

---

### D5 · TSEM — the Street takes the company's FY28 MARGIN but not its FY28 VOLUME. And Stifel initiates Buy at the very bottom of the target range.

| FY28E | Company target model *(via Stifel)* | BBG 3FY | Gap |
|---|--:|--:|--:|
| Revenue | **$3.6bn** | $3.408bn | **BBG −5.3%** |
| Operating margin | **38.3%** *(on 85% utilisation vs ~60-80% today)* | **41.7%** | **BBG +3.4pp** |

- 🔴 **The Street is MORE optimistic than the company on margin and LESS optimistic on revenue.** That is an unusual
  and specific combination: consensus is not disputing the accretive mix, it is disputing whether the SiPho volume
  and the utilisation recovery arrive. **The debate is the denominator — 5 to 25 points of utilisation — not the
  margin story.**
- **Stifel initiates BUY with a $270 target — the bottom of the ~$270-355 range it itself reports, and 12.6% below
  the $308.88 BBG consensus target price** (spot $206.81). A Buy at the low end of the Street's targets is a
  distinctive stance and should be logged as such rather than as a bullish datapoint.
- ⚠️ **Do NOT score Stifel against the consensus printed in its own note at FY3.** Stifel reports the street at
  $3.62bn / 37.1% adj OM / $10.53 EPS (FactSet); BBG prints $3.408bn / 41.7% / $9.502. The revenue gap is 5.9% and
  the EPS gap 9.8% — **within the known FactSet-vs-Bloomberg divergence band at FY3 for this wiki. This is a
  CONSENSUS-VENDOR BASIS difference, not an analytical divergence.**

---

### D6 · AXTI — management's FIRST-EVER capex path runs 40-90% ABOVE consensus. This is the cleanest hard divergence of the run.

| CY2027 capex | Value |
|---|--:|
| **Management: "~$150m, up to $200m"** | $150-200m |
| **BBG consensus (2FY `BEST_CAPEX`)** | **$106.2m** |
| **Gap** | **+41% to +88%** |

- Unlike D4, this one is **not hedged**: it is a management capex plan, stated on the record, and it is the first
  capex path this page has ever carried. Consensus CY2026 capex ($30.9m) is consistent with the company; **the
  divergence opens in 2027**, which is exactly when the second capacity doubling lands.
- ➤ **Internally coherent with everything else AXT said:** you cannot double capacity again in 2027 against a
  >18-month supply deficit on a $106m budget. **The Street has the revenue ramp (2027 consensus +119% y/y) but has
  not funded it.** Either consensus capex rises or consensus revenue falls — they are not currently consistent
  with each other.
- ⚠️ Watch the FCF consequence: on consensus 2027 revenue of $485.2m and EBIT of $160.3m, a $150-200m capex year
  is roughly the whole of EBIT. **The equity/financing question is live and nobody is modelling it.**
- 🔗 **This is the same shape as the COHR house call (C5) and reinforces it:** two separate names in the same
  indium-phosphide chain where the Street models the volume but under-funds the capex needed to deliver it.
  COHR: house $2.6bn vs BBG $1.5bn (2FY). AXT: management $150-200m vs BBG $106m. **Same trade, two rungs of the
  chain.**

---

## ✅ CONFIRMS — no action

### C1 · AVGO — the primary matched the relays on every single reported and guided number.
The 21:00 run built the AVGO print page from desk relays (Jefferies, GS, Vital Knowledge, Barclays, JPM, UBS,
TMTB). Tonight's **primary** (the 8-K/press release + the call itself) reproduced **every** headline figure with
**zero discrepancies**: revenue $29.591bn (+86%), GM 75.0%, op margin 67.9%, non-GAAP EPS $3.32, FCF $13.665bn,
AI semis $16.7bn (+221% y/y, +54% q/q), the full FQ4 guide ($34.8bn / AI $21.7bn / 66% op margin / ~73% GM),
FY26 AI $58bn, FY27 $115bn, FY28 $230bn, EPS ">$30", "$350bn over two years", and the whole customer GW ladder.
➤ **That is itself a useful result about relay quality on this name — but note it did NOT extend to WORDING**, where
four real errors were found and corrected (see the ingest log: TPU v8 "surpasses" → "comparable if not surpasses";
InP capacity "doubled" → "more than tripled"; "Tomahawk 6 sold out" re-attributed from management to the JPM
analyst's question; and the CFO's own 76%→67% segment-GM correction documented).

### C2 · AVGO FY26 — consensus is consistent with the Q4 guide.
BBG 1FY revenue **$105,998m** vs FY25 actual **$63,887m** (+65.9%). Q3 actual $29.591bn + Q4 guide $34.8bn =
$64.4bn of H2, implying ~$41.6bn of H1 — consistent with the reported Q1/Q2 shape. No variance.

### C3 · CRDO — consensus sits almost exactly ON management's own framework. Nothing to trade.
- **Revenue:** guide ">85% y/y growth" for FY27. BBG 1FY **$2,509.68m** ÷ FY26 actual **$1,335.116m** = **+88.0%** —
  consensus takes management slightly *more* than at its word, ~3pp above the floor.
- **EPS — the tightest fit in tonight's run:** management guides FY27 non-GAAP **net margin "in the vicinity of
  50%"** on ~200m diluted shares. 50% × $2,509.68m ÷ 200m = **$6.27**. BBG 1FY consensus EPS = **$6.279**.
  **0.1% apart.** Consensus is not forecasting Credo; it is arithmetic on Credo's guide.
- **Optical:** the ">$600m of FY27 optical revenue, each of ZeroFlap / SiPho PICs / optical DSPs >$100m" is
  **23.9% of consensus FY27 revenue** — the segment decomposition is new information, but the total it rolls up to
  is already in the number. ➤ **The tradeable question on CRDO is therefore the MIX and the 2H inflection, not the
  full-year total.**
- No Capstone house model exists for CRDO → baseline (2) not available. **Gap worth closing given the position.**

### C4 · TSM — Stifel's initiation is in line with both BBG and the house. The only notable thing is the target.
| FY2028E | Stifel-reported street *(FactSet)* | BBG 3FY | Gap |
|---|--:|--:|--:|
| Revenue | $296bn | **$288.5bn** *(TWD 9,152,936m ÷ 31.728)* | 2.5% |
| Operating margin | 59.8% | **58.2%** | 1.6pp |
| EPS (per ADS) | $29.36 | **$27.12** *(TWD 860.435 ÷ 31.728)* | 7.6% |

All three inside the expected FY3 vendor-divergence band → **basis, not alpha**. Stifel says so itself: *"we are
in-line with consensus on TSM… our sales and EPS estimates relatively similar to the street."* ➤ **The call is on
multiple and cycle entry, not on numbers — a new Buy that explicitly claims no estimate edge.**
- **House check, on the correct basis:** house EPS **NT$102.5 (2026E) / NT$143.5 (2027E) per ORDINARY SHARE** ×5 =
  **NT$512.5 / NT$717.5 per ADS** vs BBG **NT$535.558 / NT$701.920** → **−4.3% / +2.2%. In line.** House 2026E
  revenue US$165bn vs BBG US$171.0bn → −3.5%. In line.
- **The target is the datapoint:** Stifel **$515 vs BBG consensus PT $550.95 → 6.5% below**. Another new Buy
  initiated beneath the Street's average target.

### C5 · COHR / LITE — tonight's two independent supply-chain sources CORROBORATE the differentiated half of the COHR house initiation.
The Capstone COHR initiation (2026-09-01, NEUTRAL, PT $285) rests its differentiated view **on cash, not earnings**:
FY27 capex ~**$2.6bn** against BBG consensus of ~**$1.6bn**, driving FCF ~−$1.2bn and a debt draw.
Two independent points in the same supply chain, 48 hours apart, say the input side is acutely short:
- **AXT (2026-08-31):** indium-phosphide substrate supply/demand *"not balanced at all"*, gap **">18 months"**,
  demand growing faster than capacity; only **AXT (~40%) and Sumitomo (~40%)** can move the needle, and
  **Sumitomo's doubling does not complete until 2028**.
- **Broadcom (2026-09-02):** *"demand for lasers — CW lasers, EML — is far surpassing supply out there in the
  industry"*, and it is **more than tripling its own EML/CW/VCSEL indium-phosphide capacity year on year** in the
  US and Singapore, with capex stepping from **$532m (Q3) to a $1.4bn Q4 guide**.
➤ **A chain that is short of substrate and short of lasers is precisely the condition under which COHR's capex must
run above consensus. Tonight's sources support the house's above-consensus capex call.**
⚠️ **Two-sided, and the other side belongs in the bear case:** Broadcom tripling its own laser capacity is a
**competitive threat to merchant share at COHR and LITE**, not only a demand signal.

### C6 · SKHYNIX / SAMSUNG / MU — share and regulatory datapoints; no P&L variance applies.
The TrendForce item is **eSSD market share and a regulatory condition**, not an estimate: 2Q26 eSSD share
**Samsung 35.1% / SK hynix Group incl. Solidigm 21.1% (from 23.1%) / Micron 17.1% (from 15.4%)**, and the SAMR
price cap on SK hynix's China PCIe/SATA eSSDs expiring December 2026 (**expiry ≠ removal**). ➤ **No consensus
variance pass is meaningful here** — the correct treatment is the conditional catalyst that has been logged on
SKHYNIX, plus the basis warning that TrendForce eSSD share is **not** NAND bit share and **not** a series with the
page's existing Q4-2025 mark. Consensus is recorded for context only: MU 1FY EPS $72.805 / 2FY $152.333 /
3FY $170.807, PT $1,578.12 vs spot $956.08.

---

## 📋 Consensus reference — BBG pull, 2026-09-02

| | Spot | Cons. PT | 1FY sales | 1FY EBIT | 1FY EPS | 2FY EPS | 3FY EPS |
|---|--:|--:|--:|--:|--:|--:|--:|
| AVGO | $367.24 | $527.84 | $105,998m | $70,375m | 11.606 | 19.243 | 26.175 |
| CRDO | $165.22 | $283.50 | $2,509.7m | $1,261.0m | 6.279 | 9.743 | 12.596 |
| TSM *(TWD, per ADS)* | $415.50 | $550.95 | TWD 5,425,008m | TWD 3,175,524m | 535.558 | 701.920 | 860.435 |
| TSEM | $206.81 | $308.88 | $1,980.0m | $439.4m | 3.874 | 6.583 | 9.502 |
| AXTI | $56.95 | $95.03 | $222.0m | $54.2m | 0.904 | 2.225 | 4.374 |
| GOOG *(use EBIT)* | $333.78 | $427.91 | $432,908m | $171,405m | ⚠️ 18.699 | 16.015 | 19.532 |
| MU | $956.08 | $1,578.12 | $129,337m | $98,506m | 72.805 | 152.333 | 170.807 |

---

## Open items carried forward
1. **GOOG house model:** correct the stale *"above consensus (~$14.5)"* EPS claim (consensus is now $16.015) and
   restate the house view as a revenue/capex call. **Resolve the 2.5/4.0 GW (AVGO model) vs 4.6/7.75 GW (GOOG
   model) definition conflict.**
2. **AVGO house model:** split content-per-GW into (deployed GW) × (ship rate) × (content per shipped GW); and
   reconcile the segment AI line against the bottom-up GW build.
3. **CRDO and TSEM have no Capstone house model** — baseline (2) unavailable for two names now carrying live calls.
4. **`BEST_CAPEX` is unreliable for GOOG** — needs a validated capex source before any capex variance is published.
5. A **Bloomberg FINAL transcript for the AVGO call will supersede** tonight's LIVE version (which had no text
   layer); re-ingest and re-check the four wording corrections when it lands.
