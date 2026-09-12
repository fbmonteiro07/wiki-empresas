# Reconciliation — 2026-09-11 (/run-inbox, 5 sources)

_A SemiAnalysis deep-dive on NVIDIA's off-balance-sheet backstop book, **two broker-hosted company-management
firesides** (Microsoft IR at Jefferies London; AMD's McNamara + Ramsay at Goldman Communacopia), a technical
hardware expert call on KV cache and the memory hierarchy, and a **six-month-stale** Morgan Stanley cybersecurity
primer swept off the P: backlog._

> ⚠️ **TWO OF TONIGHT'S FIVE SOURCES ARE COMPANY MANAGEMENT, NOT BROKER RESEARCH.** The keyword router labelled the
> Microsoft fireside "Jefferies" and the AMD fireside "Goldman". Both are company management speaking at a
> broker-hosted event. **No Jefferies or Goldman rating, price target or estimate exists in either file**, and none
> was created. This is the recurring failure mode logged against BBG FINAL TRANSCRIPT files and broker-hosted
> firesides — it caught two of five sources tonight.

> 📚 **ONE SOURCE IS SIX MONTHS OLD AND IS NOT FLOW.** `SOFTWARE_20260320_0403.pdf` (MS, Marshall/Weiss,
> "Revisiting Cybersecurity 101") is dated **2026-03-20** and arrived via a backlog sweep, not the wire. It was
> ingested at its **real date** as structural/historical context, was kept **out of every live intra-quarter table**
> (none of PANW/CRWD/CSCO has a window covering March; NET has no intra-quarter block at all), and **supersedes
> nothing**. Its March multiples must never be chained to the live marks on those pages.

> 🚫 **ONE INBOX FILE WAS NOT A SOURCE AT ALL.** `LITE_Topics_and_Debates_2026-09-11.docx` is a **Capstone-internal
> primer compiled from this wiki** — its own footer says so. Patching `LITE.md` from it would have re-attributed the
> wiki's own datapoints to a new "source" and double-counted them. Ten of its substantive items were spot-checked
> and all ten are already on the page under their original attributions. **LITE.md was not touched, and LITE
> contributes nothing to this reconciliation.** (The router had read the file as 0 chars — its content lives in Word
> tables, which `ingest_inbox.py`'s docx path does not extract. 28,202 chars were recovered by hand.)

**Baselines used.** (1) Prior wiki comments — on disk. (2) Capstone house models — `_data/house.json`, `asof
2026-09-11`, **8 names only (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM)**. Of tonight's names only **NVDA, GOOG,
META and AVGO** have a house model; **AMD, MSFT, CRWV, PANW, CRWD, CSCO, NET, OPENAI and ANTHROPIC reconcile on two
baselines**. (3) **BBG consensus — `_data/estimates.json`, `asof 2026-09-11`, 106 names.** The Terminal was not
re-queried at 23:00; the snapshot is **same-day**, so the BBG column is **NOT marked PENDING**. Orphan-ticker audit
run in both directions: `set(companies) − set(TICKERS)` and the reverse are **both empty (106/106)** — the 09-08
orphan defect has not recurred.

> ⚠️ **The snapshot is intraday.** The LITE primer written earlier today quotes `px $937.22`; the snapshot carries
> `px $927.03`. Same date, different intraday vintage. **Price moved; the estimate lines did not** — do not treat the
> two as different consensus vintages.

---

## DIVERGES — the alpha

### 1. NVDA — two houses, one disclosure, opposite postures — but it is a **BASIS** difference, not a disagreement

SemiAnalysis lands one day after Morgan Stanley's cross-asset webcast on the same question. They do **not** contradict
each other; they are measuring different objects, and the page now says so.

| | Morgan Stanley (Moore/Tyler, 2026-09-10, data as of 09-09) | SemiAnalysis (2026-09-11) |
|---|---|---|
| Object measured | **ratings-style debt-equivalent** | **gross maximum notional** |
| Size | ~$200bn all-in at CY28-end, ~$170bn of it away from funded debt | **$497.5bn filed today → $2.1tn by F1/31** (their expansion scenario) |
| Residual-value tail | illustrative peak **~$90bn** shortly after CY28-end (~$70bn tax-affected) | residual-value line alone **$55bn F1/27 → $373bn F1/31** |
| Posture | equity **OW PT $300**; credit **Neutral \| Sidelined** — *"too early-stage, opaque, and sizable to step in"* | *"Green light – go, go go!"* — argues NVDA **should offer more** support |

➤ **They agree on the two things that matter structurally**: the residual-value cap at **25%** (now a three-source
settlement with NVIDIA IR 09-08), and that **reported leverage is not the binding constraint** (MS ~0.4x CY28E;
SemiAnalysis −0.1x net debt/EBITDA in F1/27 falling to −1.6x by F1/31, against a downgrade threshold credit analysts
put near 1.5x).
➤ **What is genuinely contestable, and is tradeable, is the rate and the tenor:**
- **Backstop floor: MS runs $2.12/hr/GPU; SemiAnalysis observes ~$2.35/hr/GPU for a GB300 on six years.** ~11% apart
  on the input that drives the entire rev-share upside grid.
- **MS's upside grid runs $12–18/hr *spot*. SemiAnalysis's observed 5-year *contract* rate is $4.50–4.60** — ~2.6x
  apart, different tenors. On the contract curve the spread over a $2.12–2.35 floor is **~$2.2–2.5/hr, not $9.88**,
  so a 50% revenue share is roughly **a quarter** of the $4.94/GPU/hr the MS grid is built on.
➤ **The testable claim:** MS's +9.42%/+15.14% FY29 EPS upside is a *spot-priced* number. If the AICP book prices on
contract tenors — which is what the three announced deals show — the same 5GW yields materially less. **Score it
against the next disclosed AICP contract rate.** ⚠️ And per the 09-10 report's own guard: the ~$65bn rev-share
exposure bucket and the EPS upside grid run off the **same 5GW** — never count the upside without the exposure.

### 2. AMD — management's headline EPS ambition is **not** above the Street, and the $100bn server goal sits past the Street's horizon

| AMD | Management (GS Communacopia, 2026-09-11) | BBG consensus (`asof 2026-09-11`) |
|---|---|--:|
| EPS "over the strategic timeframe" | *">$20"*, now *"significantly more than $20"* | **`3FY` (FY2028) EPS $22.84** |
| 2027 data center | *"much more than doubling"* | `2FY` total revenue **$87.9bn, +72.1%** on `1FY` $51.1bn |
| Server TAM 2030 → AMD share | $220bn TAM, *">50%"* → *"a $100 billion server business"* | `3FY` (FY2028) **total company** revenue **$121.1bn** |

➤ **The Street already crosses $20 in FY2028 at $22.84.** "Significantly more than $20" is therefore only a raise if
it means materially above $22.84 — and management did not say that. **Do not read the phrase as guidance above
consensus; on the printed numbers it is roughly in line with it.**
➤ **The $100bn server ambition is a 2030 number against a Street whose entire company is $121bn in FY2028.** That is
not a disagreement — it is an out-year the Street has not underwritten and cannot be seen in the wrapper (no FY2030
line). Flagged as an un-modelled gap, not a variance.
⚠️ **BASIS TRAP — the 2027 comparison cannot be made precisely.** Management's claim is about the **data center
segment**; `estimates.json` carries **no segment splits**. The +72.1% total-company consensus growth is consistent
with DC more than doubling only if DC carries the mix. **Stated, not resolved.**

### 3. AMD — the number that actually drifted is the **CPU:GPU ratio**, and the bases may not be like-for-like

The page carried **CPU:GPU 4:1 *today*, tightening toward 1:1** (Advancing AI roundtable, 2026-07-23). McNamara now
puts **1:1 in the present tense**: *"today, we're saying 1:1 sort of ratio, and it's going to continue to grow."*
**July's destination has become September's base.** Old mark moved to `## Changelog` with its 07-23 date.
⚠️ **Three bounds before this reaches a model.** (1) Management **refuses the ratio twice in the same answer** —
*"it's very hard to just say, 'Oh, here's a fixed ratio'"*. (2) The 07-23 4:1 was a **head-node** ratio; the 09-11
answer spans head nodes **and** the new agentic-sandbox class — **the bases may not be comparable**. (3) McNamara's
own history in the same breath is *"started out on one to four, a CPU to GPU."* **Not a modelling input.**

### 4. MSFT — consensus capex decelerates hard while management says it must **keep building ahead**

| MSFT capex | FY26 actual | `1FY` FY27E | `2FY` FY28E | `3FY` FY29E |
|---|--:|--:|--:|--:|
| $bn | 115.9 | **188.5** | **217.0** | **242.6** |
| y/y | — | **+62.5%** | **+15.2%** | **+11.8%** |

Against that, management's own framing on 09-11: the constraint is **power shells**, not chips — *"land is cheap… a
cold shell is also cheap. What's expensive are the kits you put inside. We just don't have enough space to go buy
more kits"*; capacity-constrained not demand-constrained; and on ROIC, *"the demand signal keeps ticking up. And as
the demand signal continues to grow, you've got to then build ahead of that… it just does push out that time frame
when those lines cross."*
➤ **The Street's FY28–FY29 capex line embeds a sharp deceleration to low-teens growth that management has not
guided and whose stated logic points the other way.** Either consensus is carrying an unstated build-out taper, or
FY28–29 capex is too low. ⚠️ **Note the unit mismatch before trading it:** management's *"double capacity in two
years"* is **gigawatts**, the consensus line is **dollars**, and management explicitly withheld the starting point.
**Testable at each `/wiki-consensus` refresh and at the FY27 guide.**
⚠️ **And a number was DENIED, not replaced.** Management says it told Bloomberg's Brody Ford that the "38 gigawatts by
2032" figure was wrong — *"Those numbers are not right… He published anyway."* **No 2032 capacity number entered any
page from either side.**

### 5. CRWV — the same $6.3bn is characterised two opposite ways, and the two readings are not compatible

| Source | Characterisation | What it implies |
|---|---|---|
| Bernstein (Quick Take, 2026-07-01) — on the page | an NVDA **backstop**; NVDA *"will purchase unsold CRWV capacity, through 4/13/2032"* | **contingent** demand — a floor, drawn only on failure |
| SemiAnalysis (2026-09-11) | inside NVDA's **cloud service agreements** — NVDA's own model-development/CI-CD compute, explicitly distinguished from the AICP backstop line | **contracted revenue** from an AA-rated tenant |

Same size, same end-date, opposite economics. **Neither adopted.** It resolves off the 10-Q line-item language —
whether the $6.3bn sits in "cloud service agreements" or in the "AI cloud agreements" take-or-pay line. **Until it
does, CRWV revenue quality on this contract is unknown, and it should not be modelled as either.**

### 6. GOOG — SemiAnalysis's $75.5bn of "guarantees" is **+$31.5bn** above the disclosed line, with no stated scope

The page carries **$44bn** as Google's own disclosed lease-payment guarantee (up from $6.5bn at end-September; The
Information, 2026-07-26), plus JPM's ~$9bn financial guarantees and ~$28bn credit derivatives. SemiAnalysis says
**$75.5bn**, labelled only "guarantees", with **no filing reference and no stated basis**. It is either a wider basis
or a grown book and the note does not say which. **Not superseded, Changelog not touched, and $75.5bn must never be
quoted as a disclosed number.** Same treatment for **META $59.0bn**, which sits as a **third basis** between the
page's WSJ **$347bn of uncommenced leases** (gross, undiscounted, multi-decade) and Barclays' **$39.93bn outstanding
/ 3,024MW**. Three bases, none superseded, none averaged.

### 7. MSFT — management restated an **older** stake figure than the page already carries

Management: *"the last number we gave you was we had a **27%** stake in OpenAI"*, equity method. The page already
carries the **newer and more precise ~25% as-converted from the FY26 10-K**. This is management restating its own
prior disclosure, so it is a **stale-number flag, not a supersession** — the `## Risks` line was left byte-identical.
⚠️ **Do not "update" the page to 27% on the strength of this call.**

---

## CONFIRMS — no action

1. **NVDA — SemiAnalysis's consensus proxy is honest.** They cite *"consensus estimates have it generating ~$441B of
   EBITDA in F1/28"*; BBG `2FY` EBITDA is **$451.0bn** — **−2.2%**. Their own model's **$283bn** for F1/27 sits
   **+3.9%** above BBG `1FY` **$272.4bn**. Close enough that none of their leverage ratios depend on a variant
   earnings view — **the argument is about the obligation stack, not about the numerator.**
2. **NVDA — the note's two totals reconcile exactly, and against this wiki's own primaries.** The headline **$530bn**
   and the later *"$497.5B filed today"* are **$32.5bn apart and both correct on their own basis**: the page's 08-26
   CFO-commentary tables give `366 + 56 + 108.5 = 530.5`, and `530.5 − 25 (equity investments) − 8 (capex) = 497.5`
   — which is precisely the six off-balance-sheet line items `279 + 108.5 + 36 + 20 + 29 + 25`. **A basis difference,
   not an error.** (An initial reading of this run treated the gap as unexplained; it is not.) **Nothing in the stack
   is net-new to the wiki — only the totals and the basis are.**
3. **NVDA — "OpenAI is 97% of the guarantee cap" is arithmetic, not a model output.** `$105.0bn ÷ $108.5bn = 96.8%`,
   straight off the 10-Q. The single point on which MS and SemiAnalysis fully converge.
4. **NVDA — per-capacity obligation arithmetic checks against primaries.** `$105bn ÷ 4.25GW = $24.7bn/GW`;
   `$21.1bn ÷ 360MW = $58.6M/MW`; the 3.75GW PORTS option at $24.7bn/GW = **$92.6bn**, which is the note's own "~$93bn".
   ⚠️ **The note writes both "3.8 GW" and "3.75 GW"; the page keeps 3.75GW (08-17 primary) — and it is the figure
   that makes the note's own arithmetic work.**
5. **NVDA — the 25% residual-value cap is now three-source settled** (SemiAnalysis 09-11, MS 09-10, NVIDIA IR 09-08).
6. **NVDA — house model vs BBG, unchanged and still the 09-10 divergence.** House CY2027 revenue **$661bn** / non-GAAP
   EPS **$15.49** against BBG `CY2027` **$701.6bn / $15.76** — house **−5.8%** on revenue, **−1.7%** on EPS. Tonight's
   source moves neither. *(09-10 §3 stays open.)*
7. **AMD — the TAM ladder was NOT raised. It is the third restatement in six weeks.** `$60bn → $120bn → $220bn`
   server TAM, `>$2trn by 2030`, `>60%/>80%/>35%`, `>50% of $220bn`, `$100bn server business`, 2027 DC "much more
   than doubling", Q2 enterprise server +70% — **all already on the page** from 07-23, 08-04, 08-27 and 09-08, and the
   09-08 block had already flagged the $2trn as *"NOT a fourth raise"*. **Durability, not news — do not double-count
   a raise that did not happen.** ⚠️ One unreconciled management-vs-management inconsistency recorded, not resolved:
   Ramsay puts the $2trn TAM at a **40%** growth rate; the page's 07-23 mark is **+45% CAGR**. Same company, seven
   weeks apart. Neither retired.
8. **MSFT — the capacity guide was restated, not changed.** *"From the end of 2025… we would double capacity in two
   years"* (end-25 → end-27) was already on the page from the 4Q FY26 call; now twice-sourced. The starting point is
   still withheld.
9. **MSFT — MS's March cyber sizing corroborates the January mark.** The deck's ~11%-of-cybersecurity-market framing
   matches the ~$30bn/~11% already on the page from MS's 2026-01-26 note. Only the product-depth ranking is new.
10. **Cyber group — the March deck's structural claims are intact and were filed as history.** Total cyber spend
    **$246.2bn (2024) → $430.5bn (2029)** at a steady **6.5–6.8% of IT spend**; AI Security Tracker **PANW 4.5 =
    CRWD 4.5 > MSFT 4.0**, CSCO 1.75 (8th); recurring-revenue mix **61% (2016) → 90% (2025)**; group operating margin
    **5.8% (2020) → 24.1% (2027e)**. **No multiple was invented for CSCO — it is not in the deck's comp table.**

---

## Traps carried out of this run

- **UNIT HAZARD — a THIRD class of per-capacity dollar figure is now in the corpus, and it must not merge with the
  other two.** SemiAnalysis's `$59bn/GW` (AICP), `$24.7bn/GW` (PORTS-Pike LPS) and `$9.4bn/GW` (residual value) are
  **maximum obligation / credit exposure per unit of capacity enabled**. They are **not** revenue per watt, **not**
  build cost per GW, and **not** MS's `$3/watt`, which is a **contractual price floor**. Four distinct bases now
  circulate on the NVDA page alone. **Never net them, never chain them into a series.**
- **STOCK vs FLOW.** SemiAnalysis's *"~6.5GW ≈ 2.5–3M GB300-equivalents ≈ 25–35% of CY2027 shipments"* sets a
  **multi-year stock** against a **one-year flow**. The note's own annualised figure — ~0.6M GPUs/yr, **<10%** of the
  CY2027 forecast — is the like-for-like number. **Quote the second, not the first.**
- **ASPIRATIONAL ≠ FORECAST.** The entire F1/28–F1/31 path ($2.5tn of capital-partnership funding, residual value to
  $373bn, the $2.1tn stack) is the authors' explicit capacity test — *"this does not represent our base case or a
  definitive forecast"*. Logged, never written into page numbers.
- **ASR garbles quoted as heard, never "corrected":** `"PowerShell capacity"` = power shell · `"ROC"` = ROIC ·
  `"genitive flow"` = agentic flow · `"Azure 365"`/`"Entra 65"` = Agent 365/Entra · `"D-seek"` = DeepSeek.
  **`"Methos"`, `"jalapeno chip"`, `"Kami 3"` and `"Astra"` were left unidentified.** ⚠️ Specifically: the page
  separately carries The Information's 07-28 report framing Project Perception against Anthropic's *Mythos* — **the
  garbled transcript word is NOT treated as evidence for that identification.**
- **MI450 vs MI455 inside one hour.** Ramsay: Anthropic *"buying up to 2 GW worth of **MI450**"*; later, *"ramping
  and launching Helios and **MI455**"*. Both quoted as said; **not reconciled.**
- **CHART VALUES READ FROM PIXELS.** The MS deck's SIEM pie extracted as `Exabeam M1ic4r.o1s%oft 4.2%`. Pages 27, 35,
  41 and 63 were **rendered at 170dpi and read as images** before any share was quoted (confirming MSFT 14.1%,
  Exabeam 4.2%, PANW 26.2%, CRWD 17%, Cisco/Splunk 28.1%, recurring mix 61%→90%). **Two charts were refused
  outright** — the 14-name EV/Sales-vs-M&A bar chart (run-on label row) and the Firewall/UTM sub-split
  (counterintuitive legend-to-series assignment).
- **Shared-scratchpad collision recurred.** A helper script was overwritten mid-task by a concurrent agent; it was
  re-created under a unique name and byte counts re-verified. **No edit was affected.** Per-agent filenames remain
  mandatory.

---

## Carried forward from 2026-09-10 — still open, NOT evicted

The edge tracker resolves DIVERGES off the newest reconciliation report, so the seven still-open divergences from
2026-09-10 are restated here to keep them live. **Tonight's sources advance two of them.**

| # | Name | Still-open divergence | Moved tonight? |
|---|---|---|---|
| 2 | ORCL | RPO conversion pace contests the BofA bear, **but the bases differ** | no |
| 3 | NVDA | House model is **~7pp below both management and consensus** on FY28 growth | **no** — re-verified above (CONFIRMS §6), house −5.8% rev / −1.7% EPS vs BBG CY2027 |
| 4 | META | JPM's PT went up **28% on zero change to earnings** | no |
| 5 | PANW | MS calls it a **Top Pick with a PT below the Street median** | context added (March primer dates the AI-security preference five months earlier) |
| 6 | NVDA | MS is **OW on below-consensus numbers and a below-consensus target** | no |
| 7 | NVDA | **One house, OW equity + sidelined credit** | **ADVANCED → see §1.** SemiAnalysis is the independent second read; the split is now shown to be a **basis** difference, and the contestable input is isolated to the backstop **rate and tenor** |
| 8 | ORCL | Street underwrote **~8% of the new RPO**, almost none in FY28 | no — **re-test at the next `/wiki-consensus` and after the October Investor Day** |

_§1 of 2026-09-10 (ORCL guidance raise) was resolved 2026-09-11 → CONFIRMS and is not carried._
