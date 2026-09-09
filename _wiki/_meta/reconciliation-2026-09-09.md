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
