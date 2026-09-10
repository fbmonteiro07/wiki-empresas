# Reconciliation — 2026-09-09 (/run-inbox, 14 sources)

_Conference week: Goldman Sachs Communacopia + Technology and Citi Global TMT, plus Morgan Stanley's 99-page
AI Guidebook and a SemiAnalysis TPU post. **Nine of the fourteen sources are company firesides, i.e. MANAGEMENT
sources, not broker research** — the keyword router labelled every one of them "Goldman"._

**Baselines used.** (1) Prior wiki comments — on disk. (2) Capstone house models — on-page
`## Capstone estimates` blocks. (3) **BBG consensus — `_data/estimates.json`, `asof 2026-09-08`, 105 names.**
The Terminal was not queried live this run; the on-disk snapshot is one day old and is a valid baseline, so the
BBG column is **NOT** marked PENDING.

> ⚠️ **PROVENANCE CORRECTION — appended 2026-09-09 by `/wiki-consensus` (Terminal live, `asof 2026-09-09`).**
> The cross-validation originally printed here — *"the snapshot's META px `$613.48` matches the MS note's printed
> 'Shr price, close (Sep 8, 2026) $613.48' exactly"* — is **WRONG, and the match never existed.** Every 09-08
> vintage of `estimates.json` (commits `a32d2871` and `ec6d2d25`) carries META px **`$617.67`**, not `$613.48`;
> `$613.48` appears in **no vintage in the file's entire git history** (09-04 `$616.77`, 09-03 `$610.68`,
> 09-02 `$592.85` …). `$613.48` is the **MS note's own printed close** and nothing else. The 09-08 fetch ran at
> 12:36 BRT — **intraday**, not at the close — so the snapshot price and the note's closing price are different
> quantities that were never going to agree; the 0.68% gap is the intraday-vs-close wedge, not a validation.
> **Nothing downstream depended on it** (no placement in this report used `$613.48`), but the provenance claim
> itself is retracted.
>
> ⚠️ **AND THE BBG COLUMN OF THIS REPORT STRADDLES TWO VINTAGES.** `/wiki-consensus` rewrote
> `_data/estimates.json` to `asof 2026-09-09` at **18:21:12**; this report was written at **18:21:23** — **eleven
> seconds later**, while the file was being replaced underneath the run. The straddle is visible in the numbers:
> the META PT `$745.22` is the **09-08** value, while the BKNG PT `$239.36` is the **09-09** value (09-08 carried
> `$238.36`). Both have now been re-placed against the live 09-09 snapshot below. **Lesson for the 21h/23h
> ingest pair: stamp the `asof` you actually read AND re-read it once at write time — a header `asof` is not
> proof the whole column came from that vintage.**
>
> ⚠️ **MECHANISM CORRECTED (this run, after checking its own read timestamps).** The straddle is real but the
> 18:21 explanation is not: **this report's BBG numbers were read at ~17:47 and ~17:52, roughly half an hour
> BEFORE `/wiki-consensus` wrote at 18:21:12** — so an 11-second race cannot be the cause. What the 17:47 read
> actually hit was **a working-tree `estimates.json` in the middle of being rewritten by a concurrent fetch**:
> the header still said `asof 2026-09-08` while parts of the body already carried 09-09 values (BKNG PT
> `$239.36`), and the two spot prices captured — META `$613.48`, BKNG `$180.30` — **match no committed vintage
> at all** (09-08 held `$617.67` / `$183.42`; 09-09 holds `$653.69` / `$173.43`), i.e. they were transient
> intraday values written mid-fetch. That `$613.48` coincided exactly with the MS note's printed close is what
> made a torn read look like a validation — the coincidence, not the data, produced the false claim.
> **The sharper lesson: on a shared tree, a derived data file can be TORN, not merely stale. Re-read it once at
> write time and compare against the committed blob, not just its own header.**
>
> ✅ **RE-VERIFIED against the committed `asof 2026-09-09` snapshot: every estimate line used in this report —
> revenue, EBIT, EPS and capex for all ten names — is byte-identical across the two vintages.** Only spot
> prices and consensus PTs moved. **No DIVERGES/CONFIRMS verdict in this report changes**, and the two that
> moved (META, BKNG) both moved in the direction that strengthens the argument, not weakens it.

⚠️ **Alphabet is reconciled at EBIT, never EPS.** The recurring below-the-line artefact is present again:
1FY net income `$249bn` exceeds 1FY EBIT `$172bn` by ~$77bn, and 2FY EPS *falls* `$18.70 → $16.02` while EBIT
*rises* `$172bn → $217bn`. Any EPS-based placement of Alphabet against this batch is meaningless. Also note the
`GOOG` line polls **n=18** analysts (the Class C listing), not GOOGL's ~74 — dispersion, high and low describe
the **listing**, not the company.

---

## DIVERGES — the alpha

### 1. MS's 2027 capex acceleration sits far above BBG consensus, on all four hyperscalers

The single most important number in the Guidebook, and consensus has not moved to it.

| Name | MS '27 DC-capex growth | BBG '27 total-capex growth | Gap | MS '26 DC capex | BBG '26 total capex |
|---|---|---|---|---|---|
| **MSFT** | **+43%** | **+14.9%** | **28.1pp** | $175bn | $188.9bn |
| AMZN | +50% | +26.5% | 23.5pp | $180bn | $220.5bn |
| GOOGL | +83% | +53.4% | 29.6pp | $205bn | $201.5bn |
| META | +55% | +41.4% | 13.6pp | $145bn | $139.4bn |

⚠️ **Base mismatch, stated not netted:** MS measures **data-center** capex; BBG `BEST_CAPEX` is **total** capex.
For AMZN and MSFT the MS figure sits below BBG total, which is coherent. For **GOOGL and META the MS
data-center number meets or exceeds BBG's total** ($205bn vs $201.5bn; $145bn vs $139.4bn) — which is only
possible if MS is including finance leases. META has **$279bn of leases yet to be commenced**, which is
probably the reconciling item. The direction of the gap survives the mismatch.

Corroborating the high side: Susquehanna's 09-09 desk mark has hyperscaler capex estimates **"exceeding
$1 trillion for 2027/28."**

**Action:** if MS is right, consensus '27 capex is materially too low and the whole supply chain re-rates. The
falsifier is the pre-build mechanic — MS's own '28 deceleration depends on it reversing.

### 2. Cost to run 1GW: the relay carried HALF the primary's number

| Mark | Source | Basis |
|---|---|---|
| **~$5bn/GW/yr** | Hock Tan **as relayed by** JPM (Harlan Sur callback, 2026-09-03) — already on AVGO.md | Anthropic-specific |
| **~$10bn/GW/yr** | **Hock Tan direct**, GS Communacopia, 2026-09-08 | generic |
| **~$8bn/GW** opex (incl. $4.6bn IT depreciation) | Morgan Stanley AI Guidebook, 2026-09-07 | independent model |

The two independent marks bracket each other; **the JPM relay is the outlier at roughly half**. Classic
relay-versus-primary corruption, though the relay may simply be scoped to Anthropic. Both kept and dated on the
page, **not averaged**. **Action: work with $8-10bn/GW/yr and retire the $5bn mark unless JPM confirms its scope.**

### 3. GOOG silicon price/performance — company marketing vs independent measurement

- **80% better price-performance for inference** — Thomas Kurian, Google Cloud CEO, 2026-09-08. No baseline,
  workload, precision or TCO basis stated.
- **up to 50% better perf/$ vs B200/B300** — SemiAnalysis InferenceX, 2026-09-07. External-customer TCO, FP8,
  aggregated-vs-aggregated, one bring-up model.

~30pp apart. Both logged with their bases; **neither adopted**. The only SemiAnalysis cut that brackets 80% is
its *internal-TCO* comparison (+76.7% vs B200 at concurrency 256), so the gap may be internal-cost vs
customer-price — recorded as a labelled hypothesis belonging to neither source, and a question for the FINAL
transcript and for IR. ⚠️ Kurian's **2.7x training** and **30% CPU** claims have **no third-party check anywhere
in the corpus**.

⚠️ And the SemiAnalysis headline has an essential second half that must travel with it: **GB300 NVL72 with
disaggregated serving beats TPUv7 aggregated by ~30% perf/$ in part of the medium-latency range.**

### 4. CRWV's cost of capital: management's characterisation vs traded levels

Intrator: CoreWeave borrows **"at par or close to at par with many of the hyperscalers"** (2026-09-08).
Already on the page from MS Global Credit Strategy: **CoreWeave-offtake bonds 8.2-14.2%** vs **Amazon-offtake
7.9-8.8%**, and a **CRWV BB term loan at 9.15%**. The market is not pricing CRWV at par. Management's version
is **not adopted**. New and unflattering from the same session: the first-ever acknowledgement of **lender
renewal risk**, and the SPV structure's look-through to offtaker credit.

### 5. SNOW gross margin: there is no floor, only a communication guarantee

The page carries a **74% FY27 product-GM guide**. Asked directly about a CoCo-driven GM guardrail, Robins
offered a *communication* commitment — "we would have the ability to communicate that to you within a quarter
or two" — and Ramaswamy took the trade explicitly: "I'm happy to come and explain that to you all day long."
**The 74% is a forecast, not a defended floor.** The offsets management named are slow (scale optimisation,
in-house open-weight inference, bulk buying including the AWS $6bn contract, capacity bought from **both**
OpenAI and Anthropic). **Action: downside GM scenarios should not assume a floor.**

### 6. MSFT — MS models Maia as a LATER ramp than the GOOG/AMZN custom-silicon story

"META and MSFT: ASIC and AMD deployments ramp over time, with >50% of incremental '27 capacity." This cuts
against the Maia enthusiasm the MSFT page has carried. Microsoft is also the **only one of the four whose '28
does not stall** (+20% vs +6/+7/+11%) — and the reason is a timing artefact, not a demand differential: its
pre-build keeps growing (+14% in '27, +8% in '28) while everyone else's reverses.

### 7. The GW anchors on `ai-datacenter-power` do not agree — and the disagreement is the finding

| Anchor | Figure | Scope |
|---|---|---|
| Bernstein | 404GW pipeline, **170GW credible** | global pipeline |
| Jefferies | ~66GW deployments over 5yrs, **~111GW installed by 2030** | North America, installed |
| Morgan Stanley (new) | **~145GW by '28**, 4x from 35GW in '25 | AMZN/GOOGL/META/MSFT compute only |

Three different scopes. **Not reconcilable as stated and not netted.** Recorded as three anchors with bases.

---

### 8. `[23:00 second pass]` SNDK — the largest open edge on the wiki just got NARROWER AND SHARPER: consensus has adopted management's DOWNSIDE case as its BASE case

**The disagreement, restated with tonight's numbers.** CFO Visoso re-affirmed the FY28-30 model a month after
Investor Day: **revenue growth mid-to-high teens, 80% gross margin, 70% operating margin, 50% FCF margin**
(*"That is a model we like"*). Against the BBG annual lines:

| Metric (BBG annual lines, asof 09-09) | FY2027 (`1FY`) | FY2028 (`2FY`) | FY2029 (`3FY`) | Management FY28-30 guide |
|---|--:|--:|--:|---|
| Revenue, $m | 48,826 | 58,589 | **52,671** | growth **mid-to-high teens** |
| Revenue y/y | — | **+20.0%** | **−10.1%** | ~+15-18% |
| Gross margin | 84.38% | 83.68% | **80.58%** | **80%** |
| Operating margin | 79.5% | 78.5% | **71.4%** | **70%** |
| EPS, $ | 211.74 | 259.46 | **211.10** | — |
| EPS y/y | — | +22.5% | **−18.6%** | — |

🔴🔴🔴 **THE DIVERGENCE IS ENTIRELY IN THE TOP LINE, AND THE MARGINS AGREE ALMOST EXACTLY. THAT DECOMPOSITION IS
THE FINDING.** Take management's guide at a ~16% mid-point off the consensus FY28 base: FY29 revenue would be
≈ **$68.0bn**, against consensus **$52.7bn** — the Street sits **~22% below the guide-implied level**, and the
y/y growth rates differ by **~26 points** (−10.1% vs ~+16%). But on the two margin lines the Street is *above*
the guide, not below: **GM 80.58% vs 80% guided (+0.6pp)** and **OpM 71.4% vs 70% guided (+1.4pp)**.

➤➤ **WHY THAT IS NEWS TONIGHT: the CFO put the downside case into arithmetic for the first time, and it is what
consensus is already modelling.** Asked whether *"two-thirds of your business in a downside scenario being 80%
gross margin and remaining one-third at prevailing prices"* was the right way to think about it, Visoso answered
*"**Yes. That's an easy way to think about it. Totally agree.**"* **Consensus FY29 is a ~80.6% gross margin on a
revenue base that FALLS ~10% — i.e. the Street has taken the NBM FLOOR as the outcome and assumed the
non-contracted third re-prices DOWN.** So the argument is not "is the guide credible" in the abstract. It reduces
to two testable questions: **(a) does the one-third at prevailing prices collapse, and (b) do the two-thirds under
NBM step UP rather than sit at the floor?** Bernstein's 09-08 detail bears directly on (b) — *"CONTRACT VALUE
INCREASES THROUGHOUT THE CONTRACT LIFE (2x IN 2 YEARS)"* — which is incompatible with a flat-at-the-floor FY29.
**One of those two positions is wrong, and both are now specified well enough to be checked against the FY28
prints.**

⚠️ **What tonight did NOT do: management supplied no FY29 revenue number, no NBM price schedule and no
non-contracted-mix assumption. The divergence is unresolved and stays OPEN. It also remains the largest open edge
on this wiki** (prior vintages logged it as *"SNDK FY29 −10.1% vs guide mid-to-high-teens"* — **the −10.1% is
unchanged in tonight's refresh, so the gap is not a stale-snapshot artifact and the guide did not drift**).

**Street placement, for completeness:** consensus PT **$2,259.03** vs px **$1,764.17** = **+28.1%** upside;
**27 buy / 4 hold / 0 sell**, rating 4.71/5; street high **$3,900**, low **$1,400**. No PT was carried by tonight's
source, so nothing moved.

### 9. `[23:00 second pass]` CRM — the Street is modelling FLAT-TO-RISING gross margin on the same product management just admitted it is subsidising

**New tonight:** Slack's GM disclosed that **Slackbot is *"built on top of Anthropic"*** and that ***"one of the
bets that we make is we actually take on the burden of token economics ourselves"*** — bundled into Salesforce's
*"highest grade plan."* This is the product behind Mike Spencer's 08-27 admission that the FY27 margin guide was
held *"because we're covering some of the token spend."*

| BBG annual lines (asof 09-09) | FY2027 (`1FY`) | FY2028 (`2FY`) | FY2029 (`3FY`) |
|---|--:|--:|--:|
| Gross margin | 80.10% | **80.32%** | **80.19%** |
| Operating margin | 34.4% | **34.8%** | **36.2%** |
| Revenue y/y | — | +9.9% | +9.5% |

🔴🔴 **CONSENSUS MODELS NO GROSS-MARGIN EROSION AT ALL — GM is flat-to-up across the whole forecast period, and
OPERATING margin EXPANDS ~180bp by FY29, through exactly the years in which management says it is absorbing an
uncapped variable inference cost on a growing product.** Consensus FY27 OpM (34.4%) also sits marginally *above*
the reaffirmed **34%** guide.

➤ **THE EDGE: this is an admitted cost that the Street has not put in the model.** It is asymmetric in a specific
way — the exposure is **not** portfolio-wide. On **Agentforce, Piper and Fin the customer pays Anthropic
directly** (*"you're not paying for Anthropic Tokens"*; *"you do that with them, with Anthropic"*), so the
absorbed cost is **Slack-specific** and scales with Slackbot attach on the top plan, not with Agentforce. **That
makes it modellable and falsifiable rather than a general worry: watch subscription gross margin against Slack
seat/plan mix, not against Agentforce ARR.**

⚠️ **Guards: management gave no Slackbot gross margin, no attach rate for the highest-grade plan, and no dollar
token cost. The mitigations are real and stated (an *"opinionated harness out of the box"*, deliberate downtiering,
and a claim that the premium comes *"at the expense of utilization of other tools"*). It is entirely possible the
net effect is immaterial — but consensus is not modelling a cost the company says it is paying, and that gap is
the position.**

### 10. `[23:00 second pass]` NOW — a small, one-directional gross-margin disagreement

The page carries BofA's 07-20 mark that 2Q gross margin stepped down ~150bp to **79.5%**, then **+100bp next
year**. BBG consensus annual GM is **78.73% (FY26) → 78.84% (FY27) → 78.62% (FY28)** — **flat, and ~70-90bp
BELOW the level BofA describes, with no recovery in it at all.** ⚠️ **Small, and possibly a basis difference
(segment/subscription vs total company gross margin is not disclosed in the snapshot), so this is logged as a
watch item rather than a position — but the direction is one-sided: if the +100bp recovery lands, consensus GM is
too low; nothing in consensus is priced for it.**

## CONFIRMS — no action

### AVGO — the fireside reaffirms the guide and reframes what constrains it

FY27 AI **$115bn**, FY28 **$230bn**, FY28 EPS **>$30**, ANTHROPIC largest FY27 XPU customer with OPENAI second,
and the **$20-30bn/GW chip-content** figure all stand from the 09-02 print. Against BBG:

| Period | BBG total revenue | Guide (AI only) | Implied non-AI + software |
|---|---|---|---|
| 1FY (FY26) | $106.0bn | $58bn | $48.0bn |
| 2FY (FY27) | $173.9bn | $115bn | $58.9bn |
| 3FY (FY28) | $276.4bn | $230bn | $46.4bn |

⚠️ **Flag for the house, not a divergence:** the implied non-AI + software line *rises* to $58.9bn in FY27 then
*falls* to $46.4bn in FY28. Either the Street models FY28 AI **above** the $230bn guide, or its FY28 total is
internally inconsistent. Worth a model bridge.

🔴 **The reframing that matters: the guide is DE-RATED FOR POWER, in the CEO's own words.** Chips, wafers,
memory and substrates are "pretty well locked in" and "more within our control"; what is not deterministic is a
**power-ready site**, and the binding item he names is not equipment but **construction, including local
permitting**. So the number is "a judged number based on not just supply of memory, wafers, but availability
and readiness of power sites." **The most-quoted guide in semis is power-constrained, not demand-constrained —
which changes what a miss would mean.**

Debt: the CEO's "about $56 billion" is a round number; the Q3 8-K has **$59.6bn gross principal at 4% / 7.4yr
WAL**, less $1.5bn retired post-quarter. The filing governs.

### AMD — the CFO restated the page; the news is a margin direction and a roadmap date

Already on the page and merely reiterated: the **$2tn 2030 TAM** (logged 07-23 — this is **not** a fourth raise),
the data-centre doubling, CPU **2H >80% / next year >70%**, the MI450 Q3→Q4→1Q27 cadence, the Cerebras
partnership. BBG: 2FY revenue **$88.3bn** vs 1FY **$51.1bn** = **+73%**, consistent with (slightly above) a
data-centre doubling. **CONFIRMS.**

Net-new: **Q4 and 2027 GM "slightly lower" than the 56% Q3 guide** — the first management-stated direction on
the page, and a negative; **MI500 dated** (2H27 introduction, primary product 2028, scale-up domain ">72");
**Intel Foundry declined**, TSMC stays "our primary supplier on the wafer side"; the **"Tallis"** team
acquisition for internal ultra-low-latency inference silicon via chiplets (spelling unconfirmed).

### META — PT level unchanged, PT *method* changed

MS OW / Top Pick / **PT $775** vs BBG consensus **$746.66** (n=79, hi $1,000, lo $580) → **+3.8% above
consensus, well below the Street high.** Not a Street-high call. **CONFIRMS.**
_(Re-placed 2026-09-09 on the live snapshot: consensus PT $745.22 → **$746.66** (+0.19% d/d), n / hi / lo all
unchanged; spot **$617.67 → $653.69, +5.83% in one session** on the settlement clearing event. The verdict is
unchanged — but note the whole move was **spot converging on a static PT**, which is the same mechanism the
options-implied series below already flagged, now with 5.8pts of it in a single day.)_

🔴 But the derivation moved even though the number did not: now "~23X P/E applied to the average of our $34/$35
EPS in '27/'28", where on 07-27 the identical $775 was a DCF at ~8% WACC and ~3% terminal growth that merely
*implied* ~23x. **A level-only check would have missed this.** Also superseded and retired to the Changelog:
bull-case implied multiple ~29x → ~28x; consensus PT top end $1,015 → $1,000; and the options-implied series,
now three dated points (24-Jul → 12-Aug → 8-Sep), bear probability **−2.7pts** with a static PT — spot
converging on the target rather than the distribution re-pricing the thesis.

⚠️ Revenue estimates were revised **up** (cc growth 26.6/22.2/19.9) while **GAAP OI is identical** to the 08-12
revision. Revenue improved, profit did not — the depreciation wall is confirmed on the day the justifying
product shipped.

### BKNG — the disintermediation debate finally has quantities, from management

Five months of argument with no measured quantity. Three arrived, all from the CFO on 2026-09-09:

- **LLM traffic "still significantly below 1%," paid and unpaid** — independently corroborated from a different
  method by **BofA/SimilarWeb ~0.6% (Jul-26)** already on the page.
- **Two thirds of traffic direct** (one third paid, deliberately).
- **Payments facilitated on "a low 70%" of all transactions.**

Set that last figure beside Nowak's argument the **previous day** — that Google will not want to be merchant of
record, run customer service, or clear payment volume across hundreds of currencies in real time — and a
broker's structural claim and a company disclosure, recorded a day apart with neither citing the other, land on
the same mechanism. **CONFIRMS from two directions.**

Valuation: px **$173.43** vs consensus PT **$239.36** (**+38.0%**); **2FY P/E 14.0x, 3FY 12.1x** — consistent
with Nowak's "priced as if it's going to be disrupted" and his growth-adjusted GDS (Sabre/Amadeus) comparison.
_(Re-placed 2026-09-09 on the live snapshot. The original line read "px $180.30 … (+33%); 2FY P/E 14.6x, 3FY
12.6x". **$180.30 was the broker note's price, not the snapshot's** — no vintage of `estimates.json` ever
carried it (09-08 `$183.42`, 09-09 `$173.43`). BKNG fell **−5.45%** on the session, so on live marks the
discount is **deeper, not shallower**: +38.0% to consensus PT against the +33% originally printed. Share-count
sanity per the split-refutation test passes — implied shares `ni/eps` 766.6m vs `mktcap/px` 751.4m, ~2% apart,
so BKNG `eps` is usable here.)_

Thesis-drift applied: the bear's "supply +8% to **8.6M** listings" (Barclays, 2026-02-18) superseded by
management's **9.1M**; the bear's *point* (supply growth hasn't converted to room nights) retained.
⚠️ Basis guard: **9.1M listings and 4.7M properties are different series** — not netted.
⚠️ Left unresolved on purpose: MS says Google "does not want" merchant-of-record; Bernstein (08-28) has
Google's own group PM saying it "may change."

### NVDA — an open flag CLOSED

Carried since 2026-08-24: do the neoclouds get revenue sharing, a GPU residual-value backstop, or both?
Answered point-blank at the NVIDIA IR session hosted for BTG's Brazilian institutions (San Francisco,
2026-09-08): the **residual-value support ("up to 25%", case-by-case) belongs to the $500bn third-party capital
platform**, while the **neocloud agreements guarantee OFF-TAKE, "not the residual value."** Two different
instruments; only one carries the 25%. Still undisclosed: dollar amount, project count, tenor, first-loss. The
Information's "$125B, or 25%" was **not** confirmed.

### SNOW — Cortex Code remains unsized, now confirmed twice

The logged disclosure gap was re-tested directly on 2026-09-08 and answered entirely in process — no dollar, no
run-rate, no % of guidance. **The UBS broker-arithmetic mark (~$300m FY27 / ~$350m upside / "half a billion")
stays a test, not a fact** — it would be ~3.7% of BBG 2FY revenue of $8.1bn. Usable and new: CoCo guidance now
rests on **two quarters of observed data**; retention stable as CoCo scaled; ramp curves "steeper and steeper."

### MS AI Guidebook — relay vs primary, and one base correction

The concurrent /wiki-ingest logged this note **second-hand** ("Morgan Stanley TMT sales · Wigg relaying the MS
AI Guidebook", 09-08). This run holds the **99-page primary**.

- Relay "+60% in 2027 ($550B), decel to +12% in 2028 ($170B)" → **primary confirms verbatim.**
- Relay "compute capacity growing 4x TO 145GW IN 2028 and ASICs growing in mix TO 66% (from 34% in 2025)" →
  primary confirms the path, but the 66% is **of INCREMENTAL capacity, not of total mix**: "custom ASICs rising
  from 34% of incremental capacity in '25 to 66% in '28" (~2GW → ~17GW). **Base correction.**
- Primary-only: **GOOGL adds the most capacity** and is adding more ASIC than GPU capacity from '26.

---

## Corrections to this run's own first reading

1. **The "$30bn/GW convergence within 24 hours" was overstated and is withdrawn as framed.** MS's $30bn/GW did
   **not** originate in the 09-07 Guidebook — it first published in MS's **2026-07-27** "Paths to 25-50% GenAI
   ROIC" and is re-published here. And Hock Tan's ~$30bn/GW was **already on the wiki from the Q3 FY26 call of
   2026-09-02**, so his 09-08 remark is a restatement too. The cross-source agreement is real and the methods
   are genuinely independent (a sell-side bottom-up token model vs a supplier CEO), but **neither mark is new
   and the 24-hour coincidence did not happen.** The whole per-GW block is a restatement rather than fresh
   evidence — logged as a dedup on AVGO, AMZN and MSFT so it is not double-counted as corroboration.

2. **PDF extraction drops the glyphs M, N and D in certain bold runs, and the first decode was wrong.**
   `"Ramping V A capacity"` decodes to **NVDA**, not to a custom-silicon line, and `"ASIC and A deployments"`
   decodes to **AMD** — corroborated by the same slide's intact legend "Other ASIC + AMD". So MS has **Amazon
   ramping NVIDIA through '26/'27 while forward-selling Trn3/Trn4**, a materially different statement from the
   custom-silicon reading. Written onto all three pages so it can be re-checked against the final PDF.
   (Same class as the known "A Z"=AMZN / " ETA"=META / " SFT"=MSFT dropped-leading-character defect.)

## Source-quality items carried onto the pages

- **Internal inconsistency in the MS deck, logged and not used:** its mega-cap exhibit marks AMZN Infrastructure
  Capex at **$140bn/$170bn '26E/'27E**, contradicting its own narrative $180bn/+50%, while the GOOGL and META
  rows in the same exhibit reconcile exactly. Also a bear-case heading of "~11x" against a body "~12x", and a
  case-(a) ROIC of ~30% in the bullet vs ~31% in the slide heading.
- **AVGO is an INITIAL DRAFT transcript.** Two ASR defects flagged rather than repaired: the FY27 guide renders
  as "$115 **million**" (logged as $115bn), and the XPV ramp as "a gigawatt for Anthropic this year and **big
  five** in 2027" (almost certainly "five gigawatts" — **not** resolved).
- **CRWV's LIVE transcript mangles proper nouns**: "coral reef"/"Corey"/"Cori"/"Curaleaf" = CoreWeave;
  "Mike Andrada" = Mike Intrator. Decoded before quoting; the garbling is recorded on the page.
- **No figure anywhere in this run was taken from a chart region.**

## Housekeeping raised

- **GOOG.md**: ~20 rows dated 08-18 → 09-09 are filed under `### Archived — Q1 FY26 intra-quarter flow
  (Apr 29 → Jul 22, 2026)`. The live Q2 table is the earlier one on the page. Same defect found on **BKNG.md**
  and **META.md** (the concurrent run appended 09-09 rows to closed windows / to the bottom of a
  reverse-chronological table). This run filed correctly and left re-filing notes inside the last cell; moving
  them needs a rewrite mandate.
- `ingest_inbox.py`'s `SKIP` set omits `PENDING_FULL_REPORTS.md` and `_expert_calls_seen.json`, so every run
  proposes them as sources and `--archive` swallows them. Backed up and restored with md5 verified again today.

---

_BBG column resolved 2026-09-09 — `estimates.json` **asof 2026-09-09**, **105/105 live** (0 `error` keys, 0
`carried_over` stamps, 0 null/zero prices, **0 records byte-identical to the 09-08 vintage**, every `px` moved,
`pt` present on all 105). Orphan-ticker audit clean **both directions** (105 TICKERS = 105 companies, zero set
difference) — the 5-name gap closed on 09-08 has held. `build_snapshot.py`: **105 injected, 3 skipped** —
ANTHROPIC / OPENAI / CEREBRAS, all genuinely private or not on the wrapper, no silent absentees._

_**Re-placement result: the report's conclusions survive the live refresh intact.** The headline DIVERGES table
(§1, MS '27 DC-capex vs BBG '27 total capex) is **numerically identical** on the 09-09 pull — MSFT +14.9%,
AMZN +26.5%, GOOG +53.4%, META +41.4%, so all four gaps (28.1 / 23.5 / 29.6 / 13.6pp) stand unchanged: **capex
consensus did not move day-over-day; only prices and PTs did.** Also re-verified exact on live data: the AVGO
revenue ladder ($106.0bn / $173.9bn / $276.4bn, so the FY28 non-AI inconsistency flag stands) and SNOW 2FY
revenue $8.10bn (UBS's ~$300m = **3.70%**, as printed). Two placements moved and are corrected above: **META**
(CONFIRMS, +4.0% → **+3.8%**) and **BKNG** (CONFIRMS, +33% → **+38.0%**). **No row changed section — nothing
moved between DIVERGES and CONFIRMS.**_

_✅ **The `§1` capex table's basis caveat gains one item, unstated in the original.** The report flags the
**data-center-vs-total** mismatch, which is right, but for **MSFT** there is also a **period-basis** mismatch:
`1FY`/`2FY` are Microsoft's **June** fiscal years, not calendar years, so "+14.9%" is FY27-over-FY26, not
CY27-over-CY26. The CY blocks disagree materially — CY-sum capex growth is **+34.9%** against the annual line's
**+14.9%**, a **20pp** wedge, and CY2026 capex sums to **$154.1bn** against the `1FY` annual **$188.9bn**
(**−18.4%**). The annual line is the right one to use (and is what the table used), but the direction of the
[[MSFT]] gap is **basis-sensitive in a way the other three are not** — GOOG's wedge is −0.2%, AMZN's −2.8%,
META's **+8.0%** (the known META CY-sum overshoot, which is why META's own guide ceiling must break the tie).
Stated, not netted; no number in the table changed._


---

# Reconciliation — 2026-09-09, SECOND PASS (23:00 `/run-inbox`, 3 sources)

_A second `/run-inbox` ran at 23:00 because the plan step's **P: sweep** pulled three new files after the 18:17
run had archived its batch. All three are **Bloomberg transcripts of company firesides at the same Goldman Sachs
Communacopia + Technology Conference** covered above — **[[SNDK]]** (Goeckeler + Visoso, *FINAL*), **[[NOW]]**
(McDermott, *FINAL*) and **[[CRM]]** (Patterson + Seaman, *INITIAL DRAFT*). Same source class, same router
mislabel ("Goldman" = the host and questioner). **MANAGEMENT sources: no rating, no PT, no estimates in any of
them — so nothing in this pass supersedes a Street mark, and no `## Changelog` entry was required.**_

**Baselines used.** (1) **Prior wiki comments** — on disk, and this pass is unusually rich in them because all
three sessions were already on the wiki as *second-hand relays* from the 21:00 `/wiki-ingest`. (2) **Capstone
house models — N/A: `_data/house.json` carries no SNDK, NOW or CRM node** (house coverage is NVDA/GOOG/AVGO/COHR/
LITE/META/TSM/AAPL), so baseline 2 is genuinely absent rather than skipped. (3) **BBG consensus —
`_data/estimates.json`, `asof 2026-09-09`, the live refresh `/wiki-consensus` wrote at 18:21 today. NOT PENDING.**

> ⚠️ **VINTAGE NOTE, given the straddle documented above.** This pass reads the **post-refresh** `asof 2026-09-09`
> file, written at 18:21:12 and unchanged since — so it is a single clean vintage, not a straddle. Every figure
> below is quoted from it directly.
>
> ⚠️ **PERIOD BASIS — this matters more than usual here.** **SNDK** (`lrq 2026-07-03`) and **CRM**
> (`lrq 2026-07-31`) both have **off-calendar fiscal years**, so the `CY20xx` blocks in `estimates.json` are
> **NOT** the fiscal years management is guiding, and the `CY` label would lie. **Every SNDK and CRM figure below
> is taken from the BBG ANNUAL lines (`1FY`/`2FY`/`3FY`), never the CY sums.** For SNDK, `1FY`=FY2027,
> `2FY`=FY2028, `3FY`=FY2029. For CRM, `1FY`=FY2027 (Jan-27), `2FY`=FY2028, `3FY`=FY2029. NOW is a December
> filer, so `1FY`=FY2026.

## DIVERGES — the alpha (second pass)

_The three divergences this pass produced — **#8 SNDK** (consensus has adopted management's DOWNSIDE case as its BASE case), **#9 CRM** (the Street models NO gross-margin erosion on a cost management admits it is absorbing) and **#10 NOW** (a one-directional gross-margin watch item) — are written up **in the first `## DIVERGES` section of this report, above**, numbered 8-10 and tagged `[23:00 second pass]`._

> ⚠️ **THEY ARE FILED THERE DELIBERATELY, AND THIS IS A TOOLING CONSTRAINT WORTH KNOWING: `_wiki/_tools/build_edge.py` harvests the FIRST `## DIVERGES` block ONLY** — `re.search(r"##\s*[^\n]*DIVERGES[^\n]*.*?(?=\n##\s|\Z)", md, re.S|re.I)`, which stops at the next `##` heading and never iterates. **A second `## DIVERGES` section later in the same file is invisible to the edge tracker and to the `_dashboards/edge.html` hub.** A first attempt at this pass put items 8-10 in their own trailing section and `edge.md` harvested only items 1-7; they were relocated into the first block and `refresh_features.py` re-run. **Any future multi-pass day must append into the existing DIVERGES section, not open a new one** (or `build_edge.py` needs `finditer`).

## CONFIRMS — no action

### SNDK — the contract book, the market structure and the HBF calendar all reconcile

**8 NBM customers** (*"eight very strong partnerships"* in *"only nine months since we signed the first deal"*),
**~80% GM at floor pricing**, **third-party financial guarantees**, **two-thirds of FY28 bits covered** with FY29
*"at that rough level or maybe moving higher"* — all consistent with the 08-05 print and the 08-19 Investor Day
transcript already on the page. **HBF: *"just taping out the die"*, samples *"next year"*, *"a couple more years"*
to commercial — consistent with the Investor Day mark (2027 samples, no commercial date, outside the FY28-30
model). The goalposts did NOT move again this window**, which is itself worth recording given the page documents a
~two-quarter slip between April and August. **Market structure: *"data center becomes more than half of the NAND
market"* CONFIRMS the print's ~30% CY25 → 50% CY26 datacentre-share framing.** ⚠️ Unit guard held: that is the
INDUSTRY mix, not SanDisk's own (~1/3).

### SNDK — the "unquantified claim" the page flagged is now quantified, and it has NO consensus comparand

The 08-19 Síntese named management's unsized productivity headroom *"the single most important unquantified claim
on this page."* Goeckeler sized it: **~27% compounded bit growth over a 10-year period from nodal transitions,
*"that's not new CapEx."*** **This cannot be reconciled against consensus — `estimates.json` carries no bit-supply
or bit-shipment line, and no house model exists — so it is recorded as a management claim with a falsification
test attached: it is a CAPABILITY CAGR, and the check is future bit-SHIPMENT disclosure against the guided
mid-teens.** ⚠️ **Explicitly NOT netted against the industry bit-supply numbers on the theme page (MS 2027
industry NAND bits +26%; YMTC *"+25% y-y"*) — those are shipment growth on a different base.** Its analytical
value is that it **resolves the HBF-cannibalisation bear and kills the HBF-as-supply-sink bull in the same
sentence** (written up on [[SNDK]] and `themes/hbm-memory`).

### CRM — two numbers this wiki was carrying SECOND-HAND are now confirmed at source

The page held **~5% premium-SKU penetration** and a **60-80% uplift** from a product webinar relayed by TMTB
(09-01) and from MS's Adam Wood relay (09-04). Borges put both to management on stage and Patterson confirmed the
uplift verbatim (*"**That's right.** That would be what that number would correlate to"*), with the 5% attributed
to *"Miguel on the earnings call."* **Neither figure has a BBG comparand (no SKU-level consensus data), so this is
a baseline-1 confirmation — but it closes the relay-vs-primary risk on two numbers the page's whole AI-monetisation
row rests on. CONFIRMS.**

**And the arithmetic those two numbers imply is a useful sizing check against consensus:** a **60-80% uplift on
~5%** of the base is worth roughly **3-4% of that base's revenue** today (5% × ~70% mid-point) — against consensus
FY28 revenue growth of **+9.9%**. ⚠️ **Inputs: 5% penetration (HARD, company), 60-80% uplift (HARD, company),
"applies to the full comparable seat base" (ASSUMED). NOT a forecast and not adopted — the point is directional:
on management's own two numbers the premium SKU is currently a low-single-digit contributor, so the FY28
consensus growth rate does not depend on it, and the upside case is a PENETRATION case. That is the same
conclusion the page's 09-05 note reached from the MS relay, now from the primary.**

⚠️ **NOT reconciled, deliberately: the new absolute prices — Agentforce One at *"$550 US"* retail against
*"about $1,300"* of average per-sales-professional spend on the surrounding stack — carry NO stated period in the
draft transcript. Per-user-per-month and per-user-per-year are both readable and differ by 12x. The RATIO is
usable; the LEVEL is not modellable until the FINAL transcript or the price list confirms the period. Flagged on
the page, excluded from every calculation here.**

### CRM — the FY28 consensus EPS DECLINE is a below-the-line artifact, not deterioration

Worth stating explicitly because the raw snapshot invites a wrong read: **consensus FY28 EPS is $16.134 vs
$16.731 in FY27 — a −3.6% DECLINE — while EBIT rises +11.4% ($15,899m → $17,714m) and revenue +9.9%.** The cause
is visible in the same file: **NI/EBIT is 88.2% in FY27 and 75.3% in FY28**, a 12.9pp step down. FY27 carries the
strategic-investment gains this page already flags (**$2.53/sh inside the Q2 FY27 non-GAAP print**, and
*"essentially the ENTIRE FY27 EPS guidance raise is that realised mark"*); FY28 does not repeat them.
➤ **RULE APPLIED (same trap logged on [[GOOG]]): reconcile Salesforce at EBIT, never at EPS. Any statement that
"consensus has CRM earnings going backwards in FY28" is an artifact of non-operating gains in the base year.
CONFIRMS the page's existing flag, and no divergence exists here.**

### NOW — consensus is NOT the constraint on the 2030 target, and Bernstein is the Street high

**The 2030 guide reconciles with room to spare.** Consensus annual revenue: **$16,211m (FY26) → $19,245m (+18.7%)
→ $22,658m (+17.7%)**. Getting from the consensus FY28 level to management's **$30bn 2030 subscription-revenue
target** requires roughly **+15.1% a year** — **below the +17.7% consensus already models for FY28.** ⚠️ **Basis
caveat, stated rather than buried: $30bn is a SUBSCRIPTION line and $22,658m is TOTAL revenue. Subscription is the
large majority of NOW's revenue, so the comparison is close but not exact and the true required CAGR is slightly
higher. Even so, the sign of the conclusion is not in doubt: consensus's own trajectory reaches the target with
growth DECELERATING. CONFIRMS — the 2030 algo is not where the disagreement lives.**

**Placement of the two live Street marks on this page against consensus PT $144.78 (px $131.11, +10.4% upside;
47 buy / 3 hold / 2 sell):** **Bernstein's Outperform PT $248 (09-09) is +71% above consensus PT and sits exactly
ON the BBG street high of $248.00 — Bernstein IS the Street high on NOW.** Wells Fargo's $175 (08-12) is **+20.9%**
above consensus. ➤ **Worth recording: NOW carries the LOWEST consensus upside of the three names in this pass
(+10.4% vs CRM +13.0% and SNDK +28.1%) while carrying the widest single-house spread to consensus. The bull case
on this page is a genuine outlier position, not a consensus one.**

### NOW — the new product-level disclosures are confirmatory in scale, with an ACV caveat

**ServiceNow's own CRM product *"doubling on a year-over-year basis"* and *"crossed $2 billion in ACV"*** is
**~12.3% of consensus FY26 revenue ($16,211m)**, and the ~$1bn of ACV implied by the doubling is **~33% of the
entire FY26→FY27 consensus revenue increment ($3,034m)**. ⚠️⚠️ **ACV IS NOT REVENUE — it is annualised contract
value, recognised over a term, so this is a SCALE CHECK and explicitly not a revenue bridge; the conversion
timing is undisclosed. But it establishes that the product management is now leading with is large enough to
matter to the consensus growth rate, which the wiki previously had no way to judge. Similarly the $1.5bn 2026 AI
ACV target ≈ 9.3% of consensus FY26 revenue.** CONFIRMS in direction, not adopted as an input.

## Relay-vs-primary: what the primaries changed, and one bull mark NUANCED

All three sessions were already on the wiki as broker write-ups or desk relays from the 21:00 `/wiki-ingest`.
**The primaries won on every point of difference and none of the relayed numbers proved WRONG — but three were
materially incomplete:**

1. **SNDK** — the relay's third takeaway was the unfalsifiable *"efficient manufacturing at low capital intensity
   enables cost-effective bit growth."* The primary is the **27% / no-capex** number, plus the Investor Day
   **2.7x-per-petabyte** capital-efficiency comparison and the **mid-single-digit capital-intensity** target.
2. **NOW** — the relay carried the AI-ACV metrics and the *"uneven adoption"* concession. The primary adds the
   **$2bn CRM-product ACV**, **AI *"up ninefold in nine months"***, the **500,000 mid-market** target for the beta
   AI help desk, and the security stack (**SecOps >$1bn**, *"eighth largest… ambition to be number one"*, **7bn
   devices under management, +40bn coming**).
3. **NOW — and the 4.5x seat claim this wiki explicitly REFUSED to adopt is now testable.** The page marked it
   *"a vendor lifetime-value statistic with no cohort, no base period and no definition — NOT ADOPTED."* The
   primary supplies the base and the window (**"the revenue of the original seat ON THE DATE THE CONTRACT WAS
   SIGNED, THROUGHOUT THE FULFILLMENT OF THE CONTRACT"**) — and the verb is **"we predict."** **Still NOT ADOPTED,
   but the objection moves from *undefined* to *undemonstrated*, which is a different and checkable complaint.**

⚠️ **THE ONE EXISTING MARK THAT WAS NUANCED RATHER THAN CONFIRMED — [[CRM]]/[[ANTHROPIC]].** The 09-01 webinar row
states the Anthropic economics are *"explicitly NOT shared."* **That is true for Agentforce, Piper and Fin and
FALSE for Slack**, where Salesforce absorbs the token cost (see DIVERGES #9). **The partnership therefore runs two
different commercial models at once — pass-through on the agent platform, absorption on the collaboration layer —
and only the second one touches Salesforce's gross margin.** Written onto [[CRM]], [[ANTHROPIC]] and
`themes/tokenmaxxing`.

## Source-quality items carried onto the pages

- **[[CRM]] — BBG *INITIAL DRAFT* mislabels the second speaker as "Robin Washington" (President & COO/CFO)
  throughout.** The panel was **Bill Patterson + Rob Seaman (EVP & GM, Slack)** — established by the analyst's
  introduction and her closing (*"thanking Bill and Rob"*). **Washington was not present. Every Slack quote was
  re-attributed to Seaman; none of it may be carried to the CFO.** A FINAL transcript will supersede.
- **[[CRM]] — a dollar/headcount garble that self-corrects inside the document:** *"the total TAM for knowledge
  workers is around a $1 billion"* is rendered later as *"in excess of a billion PEOPLE."* **It is a headcount; the
  $1bn "TAM" was not logged.**
- **[[NOW]] — an internal contradiction inside a *FINAL* transcript, recorded not resolved:** platform scale given
  as *"100 billion workflows doing 8 trillion transactions"* early and *"100 billion workflows, a trillion
  transactions"* later — **an 8x discrepancy on the same metric from the same speaker in one sitting.** Neither
  adopted; the CMDB-scale claim should be sourced to a filing.
- **[[NOW]] — unsourced self-rankings flagged and not adopted:** *"fastest-growing enterprise security company in
  the world"*, *"eighth largest"*, the *"5x to 10x TCO"* build-vs-buy ratio, *"90% of organizations"*, *"85% of
  companies."* One customer name garbled (*"Grossman"*, a German drugstore chain with *"5,200 drug stores"*) —
  **left unresolved rather than guessed.**
- **[[SNDK]] — a quarter-label discrepancy between the primary and this wiki's own note.** The 08-19 Síntese
  addendum attributes the **$5bn cash generated / $4.5bn repurchased** pair to **"Q1"**; the CFO says **"we
  generated $5 billion in cash in Q4, and we bought $4.5 billion of that back,"** consistent with the Q4 FY26
  print on 08-05. **Flagged on the page, not silently rewritten — one of the two labels is wrong and the primary is
  the better authority.**

## Housekeeping raised

- **[[SNDK]] page — EIGHT ROWS ARE IN THE WRONG INTRA-QUARTER TABLE.** Rows dated **09-03 → 09-09** sit in the
  page's **ARCHIVED (Q3-FY26-window)** full-log table, below a `Signal vs management` block whose reference print
  is Q3 FY26 — including the 09-09 Goldman relay of tonight's session. The open **Q1 FY27** window opened
  **2026-08-05**, so all eight belong in the FIRST log table. **Tonight's row was filed in the correct (open)
  table; the misfiled rows were left in place** — re-filing eight dense rows is a separate operation with its own
  risk of content loss. **Flagged for follow-up.**
- **[[SNDK]] page — the `Signal vs management` table has two 5-cell rows in a 4-column table**
  (`Pricing / peak margin`, `Demand / TAM`). **Pre-existing**; verified byte-identical before and after tonight's
  edits, and appended-into rather than restructured.
- **`ingest_inbox.py` — `--archive` still swallows `PENDING_FULL_REPORTS.md` and `_expert_calls_seen.json`**
  (its `SKIP` list covers only `_readme.md`, `_routing-plan.md`, `_ingest-log.md`). Both were backed up before
  and restored after, **md5-verified identical**. Recurring; a two-line fix to the SKIP list would end it.
