# Reconciliation — 2026-08-13 (`/run-inbox`, 23h)

_Every NEW quantitative datapoint from tonight's ingest, marked against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

**Baseline provenance.** BBG consensus is the **on-disk snapshot `_data/estimates.json`, asof 2026-08-13** — a clean 98/98 refresh committed earlier today by `/wiki-consensus` (`8aa871c3`). A **live** `bdp` pull was attempted at 23:23 and failed (`ConnectionError: could not start session` — Terminal logged out at that hour), so no field was re-pulled tonight. This is same-day BBG data, not a live quote and not a web substitute. House models are `_data/house.json`, asof 2026-08-13. Spot prices are the BBG snapshot's `px`.

**Sources reconciled:** 13 (from 18 files). Purely qualitative sources — the SemiAnalysis CPO Book (2026-01-01), the UncoverAlpha structure piece, the Morgan Stanley open-weight ROIC note — carry no new house-comparable estimates and are excluded except where they collide with a number already on a page.

---

## Where the new data DIVERGES

### 1. 🔴 COHR — the house model is 68% above consensus on CY27 EPS, and tonight's guide does not obviously bridge it

| | CY26 | CY27 |
|---|---|---|
| House (Capstone official model) | rev **$9.1bn** · EPS **$8.27** | rev **$16.6bn** · EPS **$19.21** |
| BBG consensus (2026-08-13) | rev $8.6bn · EPS $7.18 | rev **$12.4bn** · EPS **$11.43** |
| Gap | +6% rev · **+15.2% EPS** | **+34% rev · +68.1% EPS** |

This is the largest house-vs-Street gap in tonight's set, and it now sits against a **fresh print and guide** rather than against stale consensus. FQ4 FY26 actuals were rev $2.05B / GM 40.2% / EPS $1.74, and the FQ1 FY27 guide midpoint is **EPS $1.95** on rev $2.3bn with GM 40.5%. A $1.95 quarter annualises to roughly **$7.8** — so the house CY27 EPS of $19.21 requires the exit rate to roughly **2.5x within five quarters**, on gross margin the company just guided at 40.5% mid (a +50bp beat, not the +150bp the page first recorded).

➜ **Action: re-underwrite the house CY27 bridge before it is quoted.** The number is defensible only if the 1.6T ramp plus the >$3B datacom target plus pricing all land at the top of the range. Management did say 1.6T is coming *"even faster than what we thought three months ago"* and that there is *"absolutely no push-out"* — but Vivek Arya's incremental-gross-margin question (mid-40s H1 vs low-40s September) **was asked and not answered** on the call. That unanswered question is precisely the hinge of the house model.
⚠️ Note the house model's own vintage: `Modelo Coherent` figures predate tonight's print. The gap may be a staleness artifact rather than a live view.

### 2. 🔴 BofA raised the CPU TAM 24% and cut price targets on both x86-adjacent incumbents

| Name | BofA action (2026-08-12) | Rating | Prior PT | New PT |
|---|---|---|---|---|
| INTC | **PO cut** | Buy (held) | $160 | **$145** |
| QCOM | **PO cut** | Underperform (held) | $220 | **$180** |
| ARM | PO held | **Neutral** | $260 | $260 |
| AMD | PO held | Buy (top CPU pick) | $620 | $620 |
| NVDA | PO **raised** vs the relay mark | Buy (sector top pick) | $320 *(08-11 relay — wrong)* | **$350** |

CY30E server CPU TAM **~$170bn → $210.6bn (+24%)**, CAGR +30% → **+36.1%**, on the CPU:GPU ratio going ~1:4 (training) → ~1:2 (inference) → **~1:1 (agentic)**.

➜ **The divergence is internal to the note and it is the tradeable observation: a 24% bigger pie, sliced away from the incumbents.** BofA routes the increment to the licensees — NVDA takes **$59.7bn** of the **$79.9bn** merchant pot, against ARM's own silicon at **$15.0bn**. ARM's value share is simultaneously marked **down** (50% → **47%**; 37.9% merchant + 9.4% custom) and its own revenue line is back-loaded ($0.9bn CY27E → $15.0bn CY30E). INTC's dollar share path is re-cut **61% → 22%** while its **unit** share stays #1 at ~36% — a price problem before a volume problem.
➜ **Testable now:** if CPU TAM is genuinely +36% CAGR and the incumbents' POs fall, the trade is expressed in NVDA/AMD, not INTC/QCOM. That is a positioning question for the book.

### 3. 🔴 ARM — the only negative-upside target in tonight's set, and it is coherent rather than anomalous

BofA **Neutral, PO $260 vs spot $278.65 → −6.7%**. Implied **92.5x** CY27 consensus EPS ($2.81) against a spot multiple of **99.2x**.
➜ Confirmed from the note's own exhibits: ARM is absent from Exhibit 33 and sits under **NEUTRAL** in the coverage cluster — so the sub-spot PO is a considered relative-ranking call, not a stale mark. The bear mechanism is named: *"much of the value accrues to the licensees (i.e. NVDA)"*. **The ISA thesis and the equity thesis are now formally separated on the page** — ARM can be right about architecture and wrong as a stock.
⚠️ Cross-check against the bulls: BofA's CY27-28 AGI line sits **below** the ">$2bn FY27-28 demand" the ARM bulls quote. That gap is unresolved and worth a call.

### 4. 🔴 ORCL — three houses, a $100 target spread, and both Buy-rated houses de-rated the multiple

| House | Date | Rating | PT | Upside vs $156.22 | Implied CY27 P/E (cons EPS $9.19) |
|---|---|---|---|---|---|
| Deutsche Bank · Zelnick | 08-07 | Buy | **$300** | +92.0% | **32.6x** |
| UBS · Keirstead | 08-05 | Buy | **$245** *(prior $285)* | +56.8% | **26.7x** |
| JPM · Chatterjee | 08-13 | OW | **$200** *(prior Dec-26 $210)* | +28.0% | **21.8x** |

Spot trades at **17.0x** the same consensus EPS.

➜ **The pattern, not the levels, is the finding: two positively-rated houses both cut the multiple and both rolled the valuation year forward inside eight days.** UBS goes 28x C27e → **19x C28e with EPS held** — a de-rate, not an estimate cut. JPM's $210 (Dec-26) → $200 (Dec-27) is a **lower absolute target on a later date**. Both headline as constructive; the arithmetic is not.
➜ **Three further ORCL divergences now on file:**
- **The ROIC dispute is definitional, not empirical.** UBS's bridge: $2.6bn NOPAT + $4.2bn D&A over $25bn capex/GW = **27%**; without the D&A add-back = **10%**. Management's "high 20s" and the bears' "low teens" are *the same number*. Anyone arguing this without naming the add-back is arguing about nothing.
- **JPM's own Risks section concedes AI-cloud GM at "reported mid-teens"** against its 30–40% IaaS target — inside an Overweight note. That is the strongest support Redburn's SELL has received from any house.
- **OpenAI's share of RPO is contested: UBS ~40% (~$250bn) vs JPM ~50%+** — a **~$65bn spread** on an undisclosed figure. Unresolvable from outside; flagged as open.
➜ Scale check against consensus: JPM's **OCI/IaaS $18bn FY26 → $180bn FY30** compares with CY27 consensus **total-company** revenue of $106.9bn. The ramp is the entire thesis and it is not in the CY27 numbers yet.

### 5. 🔴 A double-count found in our own prior comment — MSFT/OpenAI revenue share

The wiki logged (07-30, UBS callback) the cessation of MSFT→OpenAI revenue-share payments as an **FY27 tailwind**. Management dates it **earlier**: *"embedded in what you saw in our fiscal year Q4 or calendar year Q2"* — i.e. **already inside the reported F4Q26 67.2% gross margin**.
➜ **Carrying it forward double-counts it.** Corrected on MSFT.md and on `themes/hyperscaler-capex.md`. This is a divergence against *ourselves*, which is the category most likely to survive unchallenged.

### 6. ⚠️ NVDA — house sits 19.6% above consensus on CY27 EPS, and tonight's flow cuts both ways

House CY27 rev **$661bn** vs consensus $568.3bn (**+16%**); EPS **$15.44** vs $12.91 (**+19.6%**). CY26 gap is far smaller (+4% rev, +4.5% EPS) — so the house edge is entirely an **out-year** call.
➜ Tonight's two NVDA sources pull in opposite directions and neither is decisive: BofA raises the PO to $350 and calls CPUs **additive, not substitutive** (supportive of the out-year); UncoverAlpha argues the ~75% gross margin is the thing the ecosystem is organising against, with GOOG at >3mn TPUs/yr and ~3.5GW of Broadcom-built next-gen TPU capacity from 2027.
➜ **The house CY27 number is a margin call as much as a volume call.** Worth stating which, explicitly, in the model.

### 7. ⚠️ NBIS — a basis correction that changes how the guide should be read

Management separated three numbers that had been collapsing into one on the page: **5 GW contracted (YE26)** / **800 MW–1 GW connected (YE26)** / that same **800 MW–1 GW active only through 1H2027**.
➜ This is the honest explanation for the beat-with-reiterated-guide that the 08-12 ingest left unresolved — connected ≠ contracted ≠ revenue-generating, and the commissioning chain (commission → network → clusters → platform → onboarding) sits between them.
➜ **Also a basis flag: the $40–50M/MW marks are GB300-era, not Vera Rubin.** Management declined to confirm the VR link. Do not carry those marks into a VR-based model.
➜ No house model for NBIS; consensus CY26/CY27 EPS is negative (−$3.40 / −$4.43), so this reconciles against prior wiki comments only.

### 8. ⚠️ STX — the primary transcript softens a claim the relay had hardened

The 21h relay logged pricing as *accelerating*. The primary has management **walking that back explicitly**: "accelerating" was the wrong word; the trend has moved **above zero** after years of negative-single-digit declines and stays above zero through FY2027 — a **floor, not a slope**.
➜ Host's sequential ladder (Dec **+4%** → Mar **+6%** → Jun **+7%**) runs ~1pt above Bernstein's "~6% QoQ" mark and is **unreconciled**.
➜ **"Targeting the mid-20s" is data-center exabyte growth, not a margin metric** — corrected during this run before it reached the page.

---

## CONFIRMS — no action

| Datapoint | Baseline it confirms |
|---|---|
| **MSFT capacity constraint is "powered up data center shells" (land, permits, build, equipment), not GPUs** — lasting "at least through the end of the calendar year" | Confirms the shells-not-chips framing already standing on MSFT.md and `themes/ai-datacenter-power.md` — now **first-party** rather than third-party inference. Management rules out *both* ends: *"it's not that we can't get servers"* and *"it's not that we can't get the energy"* — the gate is sequenced construction/permitting **time**. |
| **JPM MSFT PT $625** (prior $550), OW held | Consistent with the page's existing OW stance. PT implies **29.2x** BBG CY27 consensus EPS ($21.38) vs 23.2x spot — a re-rating call, and JPM says so explicitly (20x CY28 vs S&P ~17x; a 21% premium against a 43% historical average). No estimate divergence: JPM FY28E EPS raised only $23.15 → $23.85. |
| **BofA AMD Buy / PO $620** on 27x CY28E EPS incl. SBC | Identical to the mark already logged 08-05. No drift. |
| **COHR FQ4 GM guide correction (mid 40.5%, +50bp not +150bp)** | The FINAL transcript **confirms** the correction the 21h pass made off the initial draft. Nothing rolled back. |
| **LITE house vs consensus** — CY27 rev +3%, EPS +8.1% | Within normal dispersion; no action. CY26 EPS runs −11.2% vs consensus but the page now carries fresher first-party guidance (~$2bn/quarter run-rate by the Sep-2027 quarter) that supersedes both. |
| **META / AVGO house vs consensus** — all within ±5.3% on EPS | No edge. Note META's *consensus* moved materially though: mean PT $823.38 → **$755.23**, Street-low $664.46 → **$580**. |
| **Jefferies AEHR initiation, Buy PT $175** | Off-coverage, no house or BBG line. Its testable claim — *"neither [Teradyne nor Advantest] has established a meaningful position in high-power wafer-level burn-in"* — is logged on TER/ADVANTEST as **a falsifiable assertion published inside an initiation on the challenger**, not as a finding. |
| **UBS Semtech Buy PT $225** | Off-coverage, no page. Only the datacenter revenue ramp (~$13MM C1Q23 → $97MM C1Q26) carried, to `themes/optical-cpo`. |

---

## Screened out as basis artifacts — NOT divergences

These would each read as a large edge and none of them is one. Recording them so a later pass does not "rediscover" them.

1. **TSM house vs consensus shows −80% EPS / −97% revenue.** Pure **currency/unit artifact**: house is USD $bn and USD EPS; the BBG line is **TWD millions** (rev 5,437,587) and TWD EPS (520.27). Not comparable as stored. ➜ *Do not compare TSM house-vs-BBG without an FX conversion.*
2. **GOOG house revenue +18% vs consensus in both years, while house EPS is −8.8% / −1.8%.** Revenue running far above with EPS below is the signature of a **gross-vs-net revenue basis mismatch**, not a margin view. ➜ *Confirm the house revenue basis before quoting the +18%.*
3. **AMZN Morgan Stanley FY26e EPS $13.43 vs BBG snapshot $9.60 (~+40%).** MS's own consensus line moved with it ($9.59 → $12.69 across exhibits), which points at **GAAP below-the-line Anthropic/OpenAI revaluation gains**, not an operating revision. ➜ Logged verbatim on AMZN.md and deliberately **not merged**.
4. **GOOG "~3.5GW" appears twice from different bases.** UncoverAlpha's is **Anthropic/Broadcom-dedicated next-gen TPU capacity**; the page's existing MS figure is **third-party TPU sales** capacity. Identical number, different base — netting them would manufacture phantom corroboration.
5. **BofA's CY30 $2.16Tn is a systems TAM (vendor revenue), not capex** — excludes land/shell/power, includes non-hyperscaler buyers. Not comparable to the page's hyperscaler capex column. Separately, the page already carries "~$210bn" as BofA's META 2028E capex — **name collision** with the $210.6bn CPU TAM.
6. **AEHR's two estimate series are calendar vs fiscal.** Jefferies' tearsheet is headed *"FY (Jun)"* while carrying **calendar** figures ($53.2M/$93.3M/$169.1M/$244.7M); the prose carries fiscal ($59M FY25 → $206M FY28E); and the PT is struck off a third figure (CY29E revenue $328M). Three bases, one page.
7. **MSFT ">350 customers on track for >1trn tokens"** is a **floor (>350trn), not a platform total.**
8. **GOOG ">3mn TPUs annually" is a production rate** — must not be chained to MS's 3.7M shipment forecast or TrendForce's 12–15mn target.

---

## Open items for the desk

- **COHR house CY27 (+68% vs consensus median — and ⚠️ +40% above the STREET HIGH, per the 08-14 re-placement below)** — re-underwrite against the printed guide, or mark the model stale. Highest-priority item on this list, and upgraded by the street-high placement: no analyst on the tape underwrites this number.
- **ORCL revenue-per-GW**: the $10bn vs $30–50bn/GW gap now has a **bull** reading (UBS: "strong upward bias") against the SemiAnalysis/Jefferies structural-handicap reading. Left explicitly unresolved — the highest-value open ORCL debate.
- **QCOM**: management guides **$15B+ datacenter revenue by FY29**; BofA models **~$2.4bn CY29E server CPU**. ~6x apart — reconcilable only if that revenue is *not* server CPU. Worth asking IR.
- **ADVANTEST's Jefferies rating is self-contradictory in the source** (comp table NR on the US line; disclosure list "6857 JP ¥35,940 **BUY**"). No rating claim was made. Resolve before citing.
- ~~**BBG live re-pull**: not required for this report — the on-disk snapshot is same-day — but any *intraday* mark (spot, live consensus revisions after 18:29) needs the Terminal up.~~ ✅ **DONE 2026-08-14 via `/wiki-consensus`** — full live pull (98/98) plus an ad-hoc `BEST_TARGET_PRICE / BEST_ANALYST_RATING` pull. See the re-placement layer below.

---

## BBG re-placement — 2026-08-14 `/wiki-consensus`

_No `PENDING` cell existed in this report (the 08-13 snapshot was same-day), so Step 3 had no cell to overwrite. This layer instead re-places every quantitative row above against a **fresh live pull**: `estimates.json` **asof 2026-08-14, 98/98 names, 0 FAIL lines, 0 null prices, 0 carry-over stamps, 1 record (BESI) byte-identical to the 08-13 vintage**. Consensus barely moved overnight (largest drift in this report's names: NBIS CY27 rev +1.28%, COHR CY27 rev +1.04%); **prices moved much more than estimates did**, which is what changes the placements below. **No row crosses DIVERGES ↔ CONFIRMS.**_

**The one finding that materially changes: the house-vs-STREET-HIGH placement.** The report states its house gaps against the consensus **median** only. Placed against the **street high** (`_hi`), two of them invert in character:

| Name | Year | House | Cons median | Street high | vs median | **vs street high** |
|---|---|---|---|---|---|---|
| **COHR** | CY27 EPS | **$19.21** | $11.45 | **$13.72** | +67.8% | **+40.0%** |
| **COHR** | CY27 rev | **$16.6bn** | $12.52bn | **$13.96bn** | +32.6% | **+18.9%** |
| **COHR** | CY26 EPS | $8.27 | $7.18 | $7.95 | +15.2% | **+4.0%** |
| **NVDA** | CY27 EPS | $15.44 | $12.93 | **$15.94** | +19.4% | **−3.1%** |
| **NVDA** | CY27 rev | $661bn | $569.1bn | **$732.2bn** | +16.1% | **−9.7%** |

➜ **COHR (DIVERGES #1) is stronger than written — and worse for the model.** The house is above the *most bullish analyst on the tape* on both CY26 and CY27, on revenue and EPS. "+68% vs the median" could be dismissed as a stale-median artifact; **+40% above the street high cannot be.** No one underwrites this number. This upgrades the open item from "re-underwrite" to **"re-underwrite before the number is quoted to anyone, internal or external."**
➜ **NVDA (DIVERGES #6) is weaker than written.** The house CY27 sits **inside** the Street's range — below the street high on both revenue and EPS. It is an above-median call, not an out-of-consensus one. The report's own framing ("the house edge is entirely an out-year call") survives, but the edge is **positional within the Street distribution, not differentiated from it**. Do not present NVDA CY27 as a contrarian house view.
➜ For completeness, the CONFIRMS rows hold on street-high too: LITE CY27 EPS −21.0%, META CY27 −15.7%, AVGO CY27 −16.9% vs their street highs — all comfortably inside the range, no action.

**PT placements** (ad-hoc live `bdp` pull 2026-08-14; `estimates.json` carries no `BEST_TARGET_PRICE`, so these are a separate pull). Broker PTs from the report vs the **BBG mean target**:

| Name | Broker PT (report) | BBG mean PT | Broker vs Street | Spot | BBG upside | Rating (n) |
|---|---|---|---|---|---|---|
| **INTC** | BofA **$145** (cut from $160) | $119.18 | **+21.7%** | $102.84 | +15.9% | **3.61**/5 (54) |
| **QCOM** | BofA **$180** (cut from $220) | $202.47 | **−11.1%** | $163.35 | +24.0% | **3.69**/5 (45) |
| **NVDA** | BofA **$350** | $303.71 | **+15.2%** | $225.08 | +34.9% | **4.88**/5 (81) |
| **AMD** | BofA **$620** | $620.95 | **−0.2%** | $500.15 | +24.2% | 4.59/5 (66) |
| **ARM** | BofA **$260** | $283.52 | **−8.3%** | $276.45 | **+2.6%** | 4.25/5 (48) |
| **ORCL** | DB $300 / UBS $245 / **JPM $200** | **$252.05** | DB +19.0% / UBS −2.8% / **JPM −20.6%** | $153.54 | **+64.2%** | 4.55/5 (51) |
| **MSFT** | JPM **$625** | $568.51 | +9.9% | $498.36 | +14.1% | 4.84/5 (73) |
| **COHR** | — | $418.43 | — | $324.31 | +29.0% | 4.52/5 (27) |
| **STX** | Bernstein $1,350 | $1,112.70 | +21.3% | $951.65 | +16.9% | 4.70/5 (27) |
| **NBIS** | — | $284.10 | — | $267.86 | **+6.1%** | 4.29/5 (21) |

➜ **DIVERGES #2 sharpens: BofA's two cuts land on opposite sides of the Street.** Even after cutting INTC to $145, BofA is still **+21.7% above** the Street mean — its "PO cut" leaves it a relative *bull* on INTC. On QCOM the $180 sits **−11.1% below** the mean, consistent with the held Underperform. So the note is not uniformly bearish on the incumbents; it is bearish on QCOM and merely less-bullish on INTC. The rating field corroborates the direction: INTC **3.61** and QCOM **3.69** are the only two sub-4 ratings in the set, against NVDA's 4.88. **The "sliced away from the incumbents" framing holds — the Street already agrees, and has for a while.**
➜ **AMD is the quiet anomaly**: BofA calls it the **top CPU pick** and prints a PT **dead-on the Street mean** (−0.2%). The conviction is in the ranking, not in the number.
➜ **DIVERGES #3 (ARM) is materially strengthened.** The BBG mean PT implies **+2.6%** upside — **the lowest in this entire 14-name set** (next lowest is NBIS at +6.1%; the median across the set is ~+24%). BofA's sub-spot $260 is not an outlier, it is **8.3% below a Street that is itself already at fair value.** The report called this "coherent rather than anomalous"; the live tape now evidences it. The ISA-thesis / equity-thesis separation stands on data, not inference. **Still DIVERGES — but the divergence is ARM-vs-its-own-multiple, not BofA-vs-the-Street.**
➜ **DIVERGES #4 (ORCL) re-places, and JPM is the outlier.** At a BBG mean of **$252.05**, JPM's $200 is **−20.6% below the Street** — not merely the low of the three houses on the page. UBS $245 is essentially *at* the mean (−2.8%); DB $300 is +19.0% above. Recomputed on today's $153.54 spot the three upsides are **DB +95.4% / UBS +59.6% / JPM +30.3%** (vs +92.0% / +56.8% / +28.0% on 08-13 — all widened as the stock fell −2.0%). Spot now trades **16.7x** CY27 consensus EPS of $9.19 (was 17.0x); the BBG mean PT implies **27.4x**. **The report's finding — both Buy-rated houses de-rated the multiple while staying constructive — is unaffected and now has the Street mean as a fourth reference point sitting between them.**
➜ **NBIS (#7) gets a live caveat**: after a **+6.0% move** in the price, the BBG mean PT is only **+6.1%** above spot. The Street has closed the gap to the price. The report's basis correction (contracted ≠ connected ≠ revenue-generating) is exactly the kind of thing that re-opens it; consensus CY26/CY27 EPS remain negative (−$3.40 / −$4.43, unchanged).
➜ **MSFT (CONFIRMS) holds to the decimal**: consensus CY27 EPS **$21.38 unchanged**, so JPM's $625 still implies **29.2x** vs **23.3x** spot. JPM sits +9.9% above the Street mean with the highest rating in the set (4.84/5). **No action.**

**Prices moved, estimates did not.** Notable one-day spot moves inside this report's names: **AMD +4.4%**, **NBIS +6.0%**, **LITE +5.9%**, **STX +4.2%**, **AVGO −5.3%**, **ORCL −2.0%**. Every consensus EPS line for ARM, AMD, MSFT, STX, LITE, META, AVGO, AKAM and SPCX came back **unchanged to the cent**. The overnight information was entirely in price.

---

_BBG column resolved 2026-08-14 — `estimates.json` asof **2026-08-14** (98/98 live, 0 FAIL, 0 null prices, 0 carry-over stamps; BESI the sole byte-identical record). No `PENDING` cell existed in this report; the layer above is the live re-placement its own open item asked for. **No row crossed DIVERGES ↔ CONFIRMS.** Canonical header `## Where the new data DIVERGES` applied (was `## DIVERGES — the alpha`)._

---

_Next scheduled reconciliation: the following `/run-inbox` or `/wiki-consensus` pass. Prior: `reconciliation-2026-08-12.md`._
