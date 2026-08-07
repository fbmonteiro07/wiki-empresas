# Reconciliation — 2026-08-06 (/run-inbox, second run of the day)

_Every NEW quantitative datapoint from this run, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus (`_data/estimates.json`). Qualitative/thematic content is out of scope._

**Sources reconciled:**
1. **FUNDA — "Deep\|LLM: RSI Is the Most Important Variable, and Compute Is the Deepest Moat" (2026-08-05).** Pages: ANTHROPIC, OPENAI, GOOG, MSFT, AMZN, PLTR + 6 themes.
2. **FUNDA — "Preview\|AWS 3Q25: AWS Acceleration Ahead, but TRN3 Remains the Key" (2025-10-28).** BACKFILL. Pages: AMZN, ANTHROPIC (dated historical only).
3. ~~AlphaSense AMZN expert call (pub 2026-07-30 / int 2026-07-16)~~ — **dropped at routing as an exact duplicate of the 2026-08-05 ingest.** Contributes nothing here.

⚠️ **Scope warning, stated up front.** This run is unusually **light on reconcilable forward estimates and heavy on framework**. The RSI note's headline numbers are (a) private-company metrics with no BBG or house baseline, (b) *already-reported* print figures the wiki holds from primaries, or (c) capability metrics (METR, AI-code share) with no financial baseline at all. The findings below are therefore concentrated in **basis conflicts and stale-baseline detection** rather than estimate variance — which is where this run's alpha actually is.

## Baseline availability — read this before the tables

| Baseline | Status |
|---|---|
| **(1) Prior wiki comments** | ✅ Available (on disk). |
| **(2) Capstone house models** | ⚠️ **Partial.** `house.json` covers AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM. **Of the six names this run patched, only GOOG has a house model.** No house bridge exists for AMZN, MSFT, PLTR, ANTHROPIC or OPENAI. |
| **(3) BBG consensus** | ⚠️ **LIVE FETCH FAILED at ingest — `HTTP 503: Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal`.** The on-disk snapshot was used instead and **it is valid, not a carry-over**: `estimates.json` **asof 2026-08-06** (today), `lrq 2026-06-30` (post-print), with live spot prices on every name used here (AMZN 272.26 / MSFT 499.86 / GOOG 356.62 / PLTR 155.92). **No web data was substituted at any point.** |
| **(3b) Consensus PT / rating** | ✅ **RESOLVED 2026-08-07 via `/wiki-consensus`** (was 🔴 PENDING on the same 503). Terminal back up: full live re-fetch **`estimates.json` asof 2026-08-07, 98/98 names, 0 FAIL lines, 0 records byte-identical to the 08-06 vintage** (i.e. no silent carry-overs), plus an ad-hoc live `bdp` pull of `PX_LAST / BEST_TARGET_PRICE / BEST_ANALYST_RATING / TOT_ANALYST_REC` for the four covered names. **PT table added below.** No web data was substituted at any point. ⚠️ `estimates.json` **still carries no `BEST_TARGET_PRICE` field — now the 6th consecutive run**; the ad-hoc pull is still doing the work. |

---

## BBG consensus pull — live 2026-08-07 (the PT column this run never had)

_Ad-hoc `bdp` against `E:\bloomberg_api`, 2026-08-07. Spot and PT pulled in the same call, so the upside is internally consistent. Rating = `BEST_ANALYST_RATING` on the 1-5 scale (5 = all buys); **n** = `TOT_ANALYST_REC`._

| Ticker | Spot | Cons PT | Upside | Rating (n) | Read |
|---|--:|--:|--:|--:|---|
| **GOOG** | 356.09 | 427.25 | **+20.0%** | 4.83/5 (18) | 🔴 **Largest upside in the run, and it sharpens ① rather than softening it.** ⚠️ The C-share sample is thin (18 recs) because most of the Street publishes on the A-share — **GOOGL corroborates almost exactly: spot 356.95 / PT 428.35 / +20.0%, rating 4.73/5 on 74 recs.** The Street pays a 20% premium to spot **while carrying 2026 capex at the guide midpoint ($200.79bn)**. So the house's $183bn is not conservatism that buys margin of safety — it models ~$18bn **less** cash out than the Street on a name the Street already thinks is 20% cheap, which means **house FCF is overstated against both the company and the Street.** |
| **AMZN** | 278.25 | 326.82 | **+17.5%** | 4.85/5 (82) | ✅ **Highest-rated name in the run on the deepest sample.** Nothing in this run's AMZN findings is an estimate call — ④ is an order-book **calibration prior** and ⑤a a **basis** conflict — and the capex CONFIRMS row holds on the fresh pull (BBG CY26 capex **$214.16bn** vs Jassy's ~$220bn, −2.7%). **CONFIRMS.** |
| **PLTR** | 169.19 | 195.85 | **+15.8%** | 4.27/5 (33) | 🔴 **Weakest conviction of the four — and the entry has deteriorated hard in one session.** The stock ran **155.92 → 169.19 (+8.5%)** since the 08-06 snapshot against an unchanged PT, so upside compressed from **+25.6% to +15.8% on price alone.** Reads with ②: the Street's PT is anchored to a CY27 that decelerates to +54%, and **the tape moved toward the guide before the PTs did.** The divergence stands; the risk/reward on it does not. |
| **MSFT** | 502.20 | 563.49 | **+12.2%** | 4.84/5 (73) | ✅ **Lowest upside of the four, and it is entirely a price move.** PT essentially unchanged from the 08-04 live pull (**$563.65 → $563.49, −0.03%**) while spot rose **$490.64 → $502.20** — the compression from +14.9% to +12.2% carries **no estimate content**. MSFT's only contribution to this run is the top-4 capex CONFIRMS row, which holds. **CONFIRMS.** |
| **ANTHROPIC**, **OPENAI** | — | — | — | — | **No BBG (private — not on the wrapper).** Their datapoints in this run (run-rate, API mix, METR, token prices) have no consensus or house baseline by construction and stay in the CONFIRMS / no-baseline sections unchanged. |

**Estimates themselves did not move.** On the fresh 08-07 pull, **every CY figure cited in this report is unchanged from the 08-06 vintage.** Across the six names the only movements at all are AMZN CY26 revenue **+$16.2m** (+0.002%), PLTR CY27 capex **$78.6m → $81.8m**, and META CY26 EPS **$33.87 → $33.80**. **No finding's numeric basis moved, and no row moves between DIVERGES and CONFIRMS.** The PT layer below is additive.

---

## Where the new data DIVERGES

| Name | New datapoint | Baseline it breaks | Gap | Read |
|---|---|---|---|---|
| **GOOG** | Mgmt 2026 capex guide **$195-205bn**; BBG CY26 **$200.8bn** | **Capstone house model $183bn** | **−8.5% vs guide mid, below the guide FLOOR** | ① House is stale to the 07-22 raise — 2027 matches BBG to the decimal, so this is a missed update, not a call. Fix before any capex/FCF work. |
| **PLTR** | Q2 **+93% y/y** actual; FY26 guide **$8.15bn** | BBG **CY27 +54%** vs +93% trailing; **CY26 $7.97bn sits BELOW the company's own guide** | **−2.2% vs guide; 39pt fwd decel** | ② The steep decel is unexpressed in consensus and is the cleanest long-side read of the RSI thesis in the book — but FUNDA's own FDE-compression argument cuts the other way. Both legs on page. |
| **PLTR** | FUNDA: Q1'26 **+85%**, "**ARR >$6.5B**" | **No primary on-page counterpart**; PLTR does not report ARR | **unverifiable** | ③ **Do not propagate.** Must not be mixed with US Commercial RDV $6.238bn (different metric, similar level). Resolve vs the Q1'26 10-Q. |
| **AMZN** | FUNDA (Oct-25) Trainium **order book 2.2-2.6M** units for 2026 | Fubon **production** 1.6-1.7M; UBS **demand** 1.8M | **+29% to +45% hot** | ④ Three bases, never netted. A reusable **calibration prior** on how much an early order book overstates output — NOT a revision. CoWoS leg scored far better than the unit leg. |
| **AMZN** | FUNDA Project Rainier **4.5GW** / 3 campuses | JPM **2.25GW**; SemiAnalysis **>1.3GW IT** | **~2x, basis unstated** | ⑤a Facility vs IT-load never stated. All three stand per the `assumptions.md` GW rule. |
| **GOOG** | FUNDA Anthropic deal "**up to 1M TPUs**" | Expert callback **~4GW**; JPM **~$40bn** | **1M TPUs > 4GW at v7/v8** | ⑤b Filed as a unit-contract **ceiling**, not netted against the GW or $ marks. |
| **macro** | FUNDA: semis' worst month since **2002** | Page carries worst month since **2008** (08-02 cross-asset; Gaetano/KOSPI) | **6yr claim conflict** | ⑤c Instrument/window mismatch (SOX vs SOXX vs broad basket). Both retained; any use must name the index. |
| **GOOG** | — | `estimates.json` **CY2026 rev $426.8bn** = +5.9% off a $403bn base | **implausible vs 82% cloud growth and house +25%** | ⑥ **CY-sum defect — use sum-of-quarters, do not cite.** Second ticker showing this class after the SPCX capex bug (08-05). |

### ① The Capstone GOOG house model has not absorbed the 2026 capex raise — it sits ~$15bn below the guide floor

Alphabet raised its 2026 capex outlook to **$195-205bn** on the 07-22 print (UBS/Arcuri, 07-27, already on `GOOG.md`).

| Baseline | GOOG 2026 capex | vs guide midpoint ($200bn) |
|---|--:|--:|
| **Capstone house model** (`house.json`, from `Modelo` scrape) | **$183bn** | **−8.5%, and BELOW the $195bn guide FLOOR** |
| **BBG consensus** (CY2026, asof 2026-08-06) | **$200.8bn** | +0.4% — **dead on the guide midpoint** |
| Management guide (07-22) | $195-205bn | — |

✅ **08-07 resolution — the PT column makes this worse, not better.** BBG CY2026 capex re-pulled live at **$200,793.02m, unchanged to the cent** from 08-06, so the −8.5% house gap is confirmed on fresh data. New: the Street carries **+20.0% upside** (PT $427.25 vs spot $356.09; GOOGL corroborates at $428.35 / +20.0% on 74 recs) with a **4.83/5** rating — i.e. **the Street is underwriting the raised capex and still calls the stock 20% cheap.** That removes the only benign reading of the house number: it is not a capex-discipline call being rewarded with a valuation cushion, because the Street already has the cushion *while* spending $18bn more. **DIVERGES stands, and the fix is now higher priority — house FCF is overstated against both the company guide and consensus.**

**The house is the outlier, and it is outside the company's own stated range.** BBG and management agree to within 0.4%; the house is the only one of the three that hasn't moved. 2027 is the opposite — house **$310bn** vs BBG **$310.2bn**, identical — which strongly suggests the 2026 line is simply **stale relative to the 07-22 raise**, not a deliberate below-consensus call. **Action: check `Modelo Google` against the raised guide before the model is used for anything capex- or FCF-sensitive.** This matters more than usual this week because the FUNDA note's entire argument is about how to *value* hyperscaler capex — and we would be arguing it off a capex number the company has already superseded.

### ② PLTR — consensus embeds a violent deceleration the note's own datapoints argue against, and consensus is BELOW the company's own guide

✅ **08-07 resolution — the call survives on the numbers and gets worse on the entry.** Live re-pull: **CY2026 revenue $7,968.88m and CY2027 $12,273.5m, both unchanged to the cent**, so consensus still sits **−2.2% below the company's own raised FY26 guide** and still embeds the **+93% → +54%** step-down. **DIVERGES confirmed on fresh data.** But PLTR **rallied +8.5% (155.92 → 169.19) in the one session since**, against an unchanged PT of **$195.85** — upside compressed **+25.6% → +15.8%**, on the **lowest analyst rating of the four names in this run (4.27/5, 33 recs)**. 🔴 **Read: the tape moved toward the guide before the PTs did.** The thesis is intact and still unexpressed in consensus estimates; the *risk/reward* on expressing it is materially worse than it was 24 hours ago, and that belongs in the sizing decision, not the thesis.

FUNDA supplies the two-point growth sequence: **+85% y/y in fiscal Q1 2026 → +93% in Q2**. The Q2 figure is confirmed by the primary (press release, 2026-08-03).

| Line | Value | Source |
|---|--:|---|
| Q2-26 actual revenue growth | **+93% y/y** | PLTR press release, 2026-08-03 (primary) |
| FY26 revenue **guide** (raised 11pts on the print) | **$8.15bn**, +82% y/y | PLTR, 2026-08-03 |
| **BBG consensus CY2026 revenue** | **$7.97bn** | estimates.json, asof 2026-08-06 |
| **BBG consensus CY2027 revenue** | **$12.27bn** → **+54% y/y** | estimates.json |

**Two findings, and they point the same way:**
1. 🔴 **Consensus CY2026 revenue ($7.97bn) sits ~2.2% BELOW the company's own raised FY26 guide ($8.15bn).** Either the CY sum has not absorbed the 08-03 raise (three days old — the likely explanation, and the same class of CY-sum lag already documented in this wiki), or the Street is discounting the guide. **Do not treat the CY2026 field as a clean bogey for PLTR this week — check quarters.** Sum-of-quarters cross-check is only partially available (Q3-26E $2.176bn + Q4-26E $2.447bn = 2H $4.62bn; 1H actual would need to be $3.35bn to reconcile to $7.97bn against a company guide implying ~$3.53bn).
2. **The CY27 step-down from +93% trailing to +54% forward is the real debate.** FUNDA's argument is that agentic/coding-adjacent deployment is what drove the acceleration and that continual learning extends it — which, if right, is an argument the deceleration is too steep. **This is unexpressed in consensus and is the cleanest long-side expression of the RSI thesis in the covered book.** ⚠️ Counterweight from the same note, and it is genuinely two-sided: FUNDA also argues continual learning **compresses FDE-style deployment cost** — which is Palantir's moat *and* its revenue. Both legs are now written on `PLTR.md`.

### ③ FUNDA's Q1'26 "ARR above $6.5B" for PLTR is UNVERIFIED and is not a company-reported metric

**Do not propagate this figure.** "ARR" is FUNDA's characterisation; Palantir does not report ARR. The page carries **US Commercial RDV of $6.238bn** — a *different* measure that lands at a coincidentally similar level, and mixing them would be a real error. The **+85% Q1'26 growth** figure likewise has **no primary on-page counterpart** to check against (the page carried only qualitative broker reaction for Q1'26 until this run). Both are logged on `PLTR.md` with the caveat attached. **Resolve against the Q1'26 10-Q before either is used.**

### ④ Trainium: a nine-month-old order book ran 29-45% hot versus current production — a reusable calibration prior

Three marks, **three different bases, never netted:**

| Mark | Basis | 2026 | 2027 | Source |
|---|---|--:|--:|---|
| FUNDA (2025-10-28) | **order book** ("units on order") | **2.2-2.6M** | — | FUNDA AWS 3Q25 preview |
| UBS / Sunny Lin | **unit demand** (Trainium3) | 1.8M | 2.8M | already on page |
| Fubon (2026-08-03) | **chip production** (total Trainium) | 1.6-1.7M | ~3.0M | already on page |

**Order book ran ~+29% (2.2 vs 1.7M) to ~+45% (midpoints 2.4 vs 1.65M) above the eventual production mark, and ~+33% above the demand mark.** **This is NOT a revision — neither existing mark was edited.** It is a **calibration prior on how much an early supply-chain order book overstates eventual output**, and it is directly reusable the next time a channel check hands us a forward order number. Scored the other way, **FUNDA's CoWoS leg was good**: 120-160K wafers vs Fubon's later 127,500 AWS CoWoS wafers for 2026 (scopes differ — TRN3-attributable vs all-AWS). **Read: on this vendor, the packaging leg travelled better than the unit leg.**

### ⑤ Three basis conflicts left standing (all logged on-page, none merged or averaged)

| # | Conflict | The marks | Why unresolved |
|---|---|---|---|
| **a** | **Project Rainier sizing** | FUNDA **4.5GW** across 3 campuses (Indiana 2.2GW), *"more than the 1.3GW media reported"* · JPM **2.25 GW** (2025-09-18) · SemiAnalysis **>1.3GW of IT capacity** (2025-09-03) | FUNDA never states **facility vs IT-load**. Per the `_meta/assumptions.md` GW rule these bases must never be mixed. All three stand with their sources. |
| **b** | **Anthropic–Google compute** | FUNDA **"up to one million TPUs"** · expert callback **~4GW** (04-30) · JPM **~$40bn** (06-16) | 1mn TPUs at v7/v8 power is materially more than 4GW. Filed as a **unit-contract ceiling**, not netted against the GW or $ marks. |
| **c** | **Semis' worst month since —** | FUNDA: **2002** · `macro-cycle.md` already carries **2008** (08-02 cross-asset; Gaetano on KOSPI) | Instrument/window mismatch (SOX vs SOXX vs broad basket). Both retained; the page now carries a rule that **any use must name the index**. |

### ⑥ Data-quality: the `estimates.json` GOOG CY2026 revenue field is not usable

✅ **08-07 resolution — the fresh pull turns this from a suspicion into a proven script defect.** A fully live re-fetch (98/98 names, **zero** records byte-identical to the prior vintage, i.e. every other field on the ticker moved) reproduces `GOOG.CY2026.rev` at **$426,843.57m — to the cent.** A stale-snapshot artifact would not survive a clean re-pull unchanged; a **deterministic CY-sum bug fed the same inputs** would, and does. 🔴 **Reclassify from "data-quality flag" to confirmed script-level defect** — third ticker-instance after SPCX capex (08-05) and this one. Sum-of-quarters is likewise unchanged: 2H-26E **$234,203.9m** (Q3E $110,937.6 + Q4E $123,266.3). **The workaround is unchanged: use sum-of-quarters, do not cite the CY2026 revenue field.**

`GOOG.CY2026.rev` = **$426.8bn**, which is **+5.9%** off the house's $403bn 2025 base — implausible against a quarter in which Google Cloud grew **82%** and against the house's own **+25%** (to $505bn). 2H-26E alone is **$234.2bn** (Q3E $110.9 + Q4E $123.3), implying a 1H of $192.6bn. **This is the same CY-sum defect class already documented in this wiki (reported quarters embedded at pre-print consensus, which understates).** 🔴 **Use sum-of-quarters for GOOG revenue; do not cite the CY2026 revenue field.** The GOOG **capex** CY field, by contrast, cross-checks cleanly against the guide (see ①) and is fine.

---

## ✅ CONFIRMS (no action)

| Datapoint (new, from this run) | Baseline | Verdict |
|---|---|---|
| **Top-4 2026 capex ~$725B, +77% y/y** (FUNDA) | **BBG sum-of-CY2026-capex = $719bn** (AMZN 214.2 + GOOG 200.8 + MSFT 153.7 + META 149.9). Canonical `assumptions.md`: **~$700-725B 2026E**. ✅ **Re-verified on the live 08-07 pull: all four capex lines unchanged to the cent, sum $718,577.8m = $718.6bn (−0.9% vs FUNDA's ~$725bn).** | ✅ **CONFIRMS within 0.9% of BBG and inside the canonical range.** A third-party restatement of the same four guides — **not** a downward revision of the page's ~$750bn big-four (JPM desk) or ~$860bn broad-cloud (BofA) marks, which are wider baskets. Logged with the basis labelled. |
| **AMZN 2026 capex ~$220bn** (Jassy, via FUNDA) | **BBG CY2026 capex $214.16bn** _(unchanged on the live 08-07 re-pull; street-high $221.9bn)_; guide ~$200→220bn | ✅ **CONFIRMS** — consensus sits mid-to-upper guide, ~2.7% below the top, and **the street-high $221.9bn is the only mark that clears Jassy's ~$220bn.** Already on page from the primary; FUNDA adds nothing. |
| **Azure +43% / >$100B; Google Cloud +82%; AWS +37%, fastest in 18 quarters** | Primaries (2026-07-22 → 07-30) already on pages | ✅ **CONFIRMS.** Deliberately **not re-stated** in any page body — primary wins. FUNDA is a secondary aggregator here. |
| **OpenAI 07-30 price cuts: Luna −80% ($1/$6 → $0.20/$1.20 per M tok), Terra −20%** | Page carried only UBS/Reuters' generic *"cut prices on smaller models"* | ✅ **CONFIRMS and ITEMISES** the prior qualitative mark. ⚠️ **Note on `tokenmaxxing.md`: the page's 07-18 Terra rate of $2.5/$15 is now PRE-CUT. FUNDA publishes no post-cut Terra rate — deriving one by applying −20% is forbidden on the page.** |
| **Anthropic run-rate ">$70B by late July"** | Prior wiki: **>$60B 3Q26** (SemiAnalysis, 07-08); Yipit $69B (07-10) sits between | ✅ **CONFIRMS the direction** and slots cleanly above Yipit. **Superseded as the headline mark** (logged to `ANTHROPIC.md` `## Changelog`) — but labelled **secondary/aggregated reporting, not a primary disclosure and not a bottoms-up model**; SemiAnalysis remains the last *modelled* figure and the full trajectory was preserved. **No BBG/house baseline exists (private).** |
| **Anthropic API mix 70-75%, eight-figure accounts doubling in 6 months** | Barclays ~70% direct API (03-11); SemiAnalysis 75-85% usage-based | ✅ **CONFIRMS** — inside the existing range. Corroboration only. |
| **PLTR Q2 +93% y/y** | PLTR press release 2026-08-03 (primary, on page) | ✅ **CONFIRMS.** Not re-stated in the body. |

---

## 📌 New, no baseline to reconcile against (logged, not reconcilable)

These are recorded so a later run can score them, not because they diverge from anything:

- **METR time-horizon: Claude Opus 4.5 at 320 minutes (Jan-2026 update); doubling ~7 months pre-2023 → ~89 days from 2024.** First METR mark on `ANTHROPIC.md`. No financial baseline exists.
- **AI-written code share:** Google **75%** (25% → 50% → 75% over 18 months); Anthropic company-wide **70-90%**; frontline engineers ~100%; Boris Cherny at 22-27 PRs/day. The *series* is the signal.
- **Anthropic R&D velocity contribution 5% → 15-20% over six months** (Amodei, Feb-2026).
- **OpenAI: 99.8% of weekly output tokens via Codex; >85% per employee; ~150 FDEs.**
- **AlphaEvolve: +23% on a key Gemini training kernel; continuously recovers 0.7% of Google's global compute.** Two different units — the fleet-level one is the vertical-integration argument.
- **China: Kimi K3 within ~2-3 months of the US frontier against a 5-17x frontier chip-performance gap (Council on Foreign Relations).** ⚠️ The lag and the gap must **not** be netted against each other.
- **Token prices falling ~10x/year** — carried on `tokenmaxxing.md` as the consumer-surplus-vs-producer-profit risk, now its own Key-debates axis.

---

## Open items carried forward

1. ~~🔴 **BBG consensus PT / rating — PENDING** (503, Terminal not logged in).~~ ✅ **DONE 2026-08-07** — Terminal back up, full live re-fetch (98/98, 0 FAIL, 0 carry-overs) + ad-hoc PT/rating pull. **PT table added; no row moved between DIVERGES and CONFIRMS.** The three things that came out of it: **(a)** GOOG's +20% consensus upside *strengthens* ① by removing the benign reading of the stale house capex; **(b)** PLTR's +8.5% one-session rally cut ②'s upside from +25.6% to +15.8% against an unchanged PT — thesis intact, entry worse; **(c)** ⑥ is now a **proven** deterministic script defect, not a stale-snapshot flag.
2. 🔴 **`estimates.json` has no `BEST_TARGET_PRICE` field — now the 6th consecutive run.** Standing script gap, still unfixed; every run needs an ad-hoc `bdp` pull to cover it. **Fix at the source: add `BEST_TARGET_PRICE` + `BEST_ANALYST_RATING` + `TOT_ANALYST_REC` to the `meta` field list in `fetch_estimates.py` (~line 97), which today pulls only `PX_LAST / NAME / EQY_FUND_CRNCY / CUR_MKT_CAP / CURR_ENTP_VAL`.** `build_edge.py` would then stop reporting "0 PT/spot rows".
3. 🔴 **Check the Capstone GOOG model's 2026 capex ($183bn) against the raised $195-205bn guide** — finding ①. **Priority raised 08-07** (see the PT read).
4. 🔴 **`GOOG.CY2026.rev` unusable** — finding ⑥. **Escalated 2026-08-07 from "flag" to confirmed script-level defect**: a clean live re-pull reproduces the value to the cent while every other field on the ticker moved. Same CY-sum class as the SPCX capex bug (08-05). **Two independent tickers, now with a deterministic-reproduction proof — fix the CY-sum path in `fetch_estimates.py`.**
   - ⚠️ **Scope note:** only GOOG revenue and SPCX capex have been *demonstrated* defective. The defect is a **reported-quarter basis mismatch**, so it can only bite CY periods with `n_actual > 0` — i.e. **CY2026 across the book, not CY2027** (`n_actual: 0`). Sum-of-quarters is the safe read for any CY2026 field until the path is fixed.
5. **Resolve PLTR Q1'26 +85% / "ARR $6.5B" against the 10-Q** — finding ③.
6. **PLTR CY27 +54% vs +93% trailing** — the run's one clean unexpressed long-side divergence (②). ⚠️ **Still unexpressed in consensus as of 08-07, but +8.5% of the upside has already been paid** — see the resolution note on ②.

---

_BBG column resolved 2026-08-07 — `estimates.json` asof 2026-08-07 (98/98 names, 0 FAIL lines, 0 records byte-identical to the 08-06 vintage), plus an ad-hoc live `bdp` pull for `BEST_TARGET_PRICE` / `BEST_ANALYST_RATING` / `TOT_ANALYST_REC`. No web data substituted at any point._
