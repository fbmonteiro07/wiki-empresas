# Reconciliation — 2026-08-13 (`/run-inbox`, 23h)

_Every NEW quantitative datapoint from tonight's ingest, marked against three baselines: (1) prior wiki comments, (2) Capstone house models, (3) BBG consensus._

**Baseline provenance.** BBG consensus is the **on-disk snapshot `_data/estimates.json`, asof 2026-08-13** — a clean 98/98 refresh committed earlier today by `/wiki-consensus` (`8aa871c3`). A **live** `bdp` pull was attempted at 23:23 and failed (`ConnectionError: could not start session` — Terminal logged out at that hour), so no field was re-pulled tonight. This is same-day BBG data, not a live quote and not a web substitute. House models are `_data/house.json`, asof 2026-08-13. Spot prices are the BBG snapshot's `px`.

**Sources reconciled:** 13 (from 18 files). Purely qualitative sources — the SemiAnalysis CPO Book (2026-01-01), the UncoverAlpha structure piece, the Morgan Stanley open-weight ROIC note — carry no new house-comparable estimates and are excluded except where they collide with a number already on a page.

---

## DIVERGES — the alpha

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

- **COHR house CY27 (+68% vs consensus)** — re-underwrite against the printed guide, or mark the model stale. Highest-priority item on this list.
- **ORCL revenue-per-GW**: the $10bn vs $30–50bn/GW gap now has a **bull** reading (UBS: "strong upward bias") against the SemiAnalysis/Jefferies structural-handicap reading. Left explicitly unresolved — the highest-value open ORCL debate.
- **QCOM**: management guides **$15B+ datacenter revenue by FY29**; BofA models **~$2.4bn CY29E server CPU**. ~6x apart — reconcilable only if that revenue is *not* server CPU. Worth asking IR.
- **ADVANTEST's Jefferies rating is self-contradictory in the source** (comp table NR on the US line; disclosure list "6857 JP ¥35,940 **BUY**"). No rating claim was made. Resolve before citing.
- **BBG live re-pull**: not required for this report — the on-disk snapshot is same-day — but any *intraday* mark (spot, live consensus revisions after 18:29) needs the Terminal up.

---

_Next scheduled reconciliation: the following `/run-inbox` or `/wiki-consensus` pass. Prior: `reconciliation-2026-08-12.md`._
