# Reconciliation — 2026-08-24 (/run-inbox, 23h scheduled run)

_Every NEW quantitative datapoint from this ingest, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`), (3) BBG consensus. Qualitative/benchmark sources (SemiAnalysis AgentX, the Hot Chips talks, the MS identity note) carry no marks and are excluded per the skill._

## Baseline availability for this run

| Baseline | Status | Note |
|---|---|---|
| Prior wiki comments | ✅ **available** | On-disk, read per page. |
| Capstone house models | ⚠️ **N/A for every name in this run** | `_data/house.json` (asof 2026-08-24) covers only **AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM**. This run's quantitative names are **MRVL** and **SAMSUNG** — neither has a house model. GOOG and NVDA *do*, but neither new source carries a GOOG or NVDA estimate (both are read-throughs). **So the house-model column is genuinely empty this run, not skipped.** |
| BBG consensus | ✅ **available from disk** · ⚠️ **live wrapper DOWN** | `bdp()` raised `ConnectionError — blpapi: could not start session` (repeated `Failed to connect to 127.0.0.1:8194`, Terminal not running / logged out at 23:42). **However `_data/estimates.json` carries a snapshot stamped `asof: 2026-08-24` — today — so consensus below is real and current, taken from disk rather than substituted from the web.** ⚠️ **No BBG figure in this report was refreshed live; if the Terminal comes back, re-run `/wiki-consensus` to confirm, particularly the CY2028 line which the snapshot does not carry.** |

⚠️ **Standing caveat applied throughout, not re-derived here:** the CY columns in `estimates.json` are calendar-year *sums*, which understate reported quarters and carry a documented, year-inverting bias on the Korean names. **Samsung is therefore reconciled at OPERATING PROFIT / EBIT, never at EPS** (the common-vs-preferred share-count trap); Samsung EPS lines are shown for completeness and explicitly marked not-load-bearing.

---

## DIVERGES (the alpha)

### 1. 🔴🔴 HBM 2027 ASP — UBS **+90%** vs JPM **+42%**. The widest pricing gap on the wiki.

| Source | Figure | Basis |
|---|---|---|
| **UBS** (Gaudois, Korea Summit, 2026-08-24) | **Samsung blended HBM ASP +90% YoY in '27E** | Single supplier, blended across its own generation mix |
| **JPM** (Kwon, model of 2026-08-09, workbooks now on disk) | **industry HBM ASP +42% y/y '27** ($1.9 → $2.8 → $3.4 per Gb, 26/27/28E) | Industry-wide, $/Gb |
| BBG | **— no consensus line for HBM ASP** | n/a |

**Why it is not automatically a contradiction:** the bases differ. A single supplier's *blended* ASP can legitimately outrun an *industry* $/Gb series if that supplier's mix shifts hard toward higher-stack / HBM4E parts — and Samsung is precisely the name with the most mix headroom, entering 2027 with the lowest HBM4 base. **Why it is still the run's top item:** 48pp is far too wide for mix alone, and the two numbers drive opposite conclusions about how much of the 2027 memory P&L is price versus volume.

➜ **ACTION: resolve at the 4Q26 / January disclosures, or by rebuilding UBS's blended ASP on JPM's $/Gb basis from the `SKH HBM` / `Samsung HBM` sheets in `JPM_HBM_client_model_Aug2026.xlsx` (now archived in `_inbox\_done\`). Until then, do not quote either number without its basis. OPEN.**

### 2. 🔴 MRVL CY28 EPS — Wells Fargo **~$11/sh** vs UBS **$9.82**: **+12.0%**, and the two most recent PTs move in opposite directions.

| Source | CY28/FY29 EPS | PT | Date |
|---|---|---|---|
| **Wells Fargo** (Rakers) — NEW | **+$11/sh** | **$240 → $310** (~28x) | 08-24 |
| UBS (Arcuri) | $9.82 | **$340 → $300** (30x) | 08-24 |
| JPM (Sur) | ~$11.00 | OW | 08-19/24 |
| Morgan Stanley (Moore) | — | $195 → **$224** (EW) | 08-23 |
| BBG | **no CY2028 line in the snapshot** | — | — |

**➜ The genuine finding is a CONFIRM sitting inside a DIVERGE.** Wells Fargo and JPM land on **the same ~$11 CY28 EPS by fully independent methods** — JPM via a ~$19.2bn/yr Google attach, Wells via an **$80bn cumulative GOOGL revenue thru FY33** bridge at ~50% GM / ~12% opex-to-rev with warrant dilution. Two methods, one number, materially tightening the confidence interval around ~$11 and leaving **UBS's $9.82 as the outlier, 12% low**. Meanwhile the *targets* span **$224 → $310** on essentially agreed earnings.

➜ **So the open MRVL question is now the MULTIPLE, not the earnings power** — 28x (Wells) vs 30x (UBS) vs MS's explicit "still trades at more than 2x" relative objection. **That is a cleaner, more tradeable framing than the page had this morning.** ⚠️ **Wells' bridge rests on an assumption it flags itself: only ~60% of its Google revenue is treated as incremental to guidance. That single input, not the EPS, is what to stress.**

### 3. ⚠️ Samsung FY27 operating profit — Goldman **W561.7tn** is **−3.8%** below consensus, and the house spread stays ~15% wide.

| Source | CY27 EBIT (W tn) | vs BBG |
|---|---|---|
| JPM | 549 | −5.9% |
| **Goldman (NEW, 08-23)** | **561.7** | **−3.8%** |
| KB | 575 | −1.5% |
| **BBG consensus (disk, 08-24)** | **583.7** | — |
| Morgan Stanley | 629 | +7.8% |

**➜ Goldman enters on the LOW side of consensus on 2027 operating profit while carrying the second-highest price target on the page (W490,000, Buy-on-Conviction-List).** That combination is the interesting part: GS is not underwriting the target with above-consensus out-year operating profit — it is underwriting it with **capital returns and a multiple**, which is exactly what its own text says (*"significant shareholder returns to help drive higher valuation multiples"*). ⚠️ **The MS-vs-JPM 15% spread on FY27 OP remains the larger, less-discussed disagreement on this name than the capital-returns argument the headlines are about — unchanged by this run, restated because a fourth house has now been added without narrowing it.**

### 4. ⚠️ Samsung EPS — UBS is **−6.2%** below consensus for CY26 while **+25.6%** above for CY28. A duration disagreement, not a level one.

| | UBS | BBG (disk) | Δ |
|---|---|---|---|
| CY2026 EPS | W43,532 | W46,433 | **−6.2%** |
| CY2027 EPS | W73,903 | W75,326 | −1.9% |
| CY2028 EPS | W84,988 | *(UBS prints cons. 67,676)* | **+25.6%** |

⚠️ **NOT LOAD-BEARING — read the caveat.** Samsung EPS on BBG is preferred-inclusive while broker headline EPS is common-only, and the CY column is a calendar sum with a year-inverting bias on the Korean names. **The direction is nonetheless consistent with every other house on this page (below near-term, above in the out-years) and with UBS's own framing.** The reliable version of this observation is the EBIT table in item 3.
**One clean, basis-free fact from the same note:** the **consensus UBS prints against itself FELL in all three years** between 08-07 and 08-23 (12/26E 48,296→48,038 · 12/27E 69,649→69,075 · 12/28E 68,932→67,676) **while UBS held its own numbers unchanged** — i.e. UBS's premium widened passively, by consensus moving down, not by UBS marking up.

### 5. ⚠️ "Vera Rubin crushes Blackwell" — **disconfirmed by its own primary.**

NVDA.md carried this from a FinTwit relay (@firstadopter / @SemiAnalysis_, 08-24/25). **The 108-page AgentX launch article benchmarks GB300 NVL72, GB200 NVL72, B300, B200, H200, RTX Pro Servers, MI355X, MI325 and MI300X — and contains no Vera Rubin comparison at all.** Marked unverified on the page. ➜ **Not a valuation item, but a corpus-integrity one: a relay claim that the primary does not support, caught only because the primary arrived.**

---

## CONFIRMS (no action)

### A. ✅ Samsung CY26 operating profit — three independent sources inside **0.3%**. The number that looked impossible is right.

| Source | CY26 OP / EBIT (W tn) | vs BBG |
|---|---|---|
| **BBG consensus (disk, 08-24)** | **378.9** | — |
| **Goldman (NEW)** | **379.0** | **+0.02%** |
| **KB Securities (NEW)** | **380** | **+0.28%** |

**➜ Logged deliberately as a near-miss avoided.** KB's *"Based on our 2026E OP of KRW380tn"* reads as absurd against Samsung's historic ~W33tn and would have been easy to discard as a typo. It is consensus, on a W720tn revenue base at a ~53% EBIT margin. **Same failure mode as the previously-logged JPM-Korea episode: reconcile before rejecting.**

### B. ✅ Wells Fargo's near-year MRVL estimates are **consensus, to within 2%** — which is itself the finding.

| | Wells Fargo | BBG (disk) | Δ |
|---|---|---|---|
| FY27E revenue | $11,740mn | CY2026 $11,531mn | +1.8% |
| FY27E EPS | $4.07 | CY2026 $4.04 | **+0.7%** |
| FY28E revenue | $16,850mn | CY2027 $16,896mn | −0.3% |
| FY28E EPS | $6.22 | CY2027 $6.27 | **−0.8%** |

*(MRVL FY ends late-Jan, so FY27 ≈ CY2026 — a one-month offset, immaterial at this tolerance. Wells prints its own consensus comparison at $4.05 / $6.19, within 0.5% of the BBG disk line, which independently validates the mapping.)*

**➜ Wells is at consensus for two years and 30% above the share price on its target. The entire PT is carried by FY29/CY28 — so this note is a *duration* call dressed as an estimate note, and nothing in the next two prints can validate or refute it.** Worth knowing before the **8/27 print**.

### C. ✅ The Samsung sell-off is real and the marks agree.

Samsung **W281,500 (21-Aug) → W257,000 (24-Aug) = −8.7%**, per the UBS Korea Summit note. **BBG's disk snapshot for the same day prints W256,000 — a 0.39% difference, i.e. the same mark.** The move is confirmed, not a broker typo. ➜ **It resolves the 08-21 three-way disagreement empirically in favour of the MS/JPM "sell-the-news" read over the Citi/KB "re-rating trigger" read, while every house held its rating and PT.**
⚠️ **MRVL moved the same way and it is not in any of the notes: Wells references $237.04 (08/21); BBG's 08-24 snapshot is $225.11 — −5.0%. Every Wells upside/downside percentage in that note is stale by that amount.**

### D. ✅ The JPM workbooks corroborate the model layer already on the wiki — verified, not assumed.

| Metric | `JPM_HBM_client_model_Aug2026.xlsx` | Already on `themes/hbm-memory.md` (from the 08-09 note) |
|---|---|---|
| HBM bit demand 26/27/28E (mn GB) | 3,579 / 6,268 / 10,750 | 3,579 / 6,268 / 10,751 ✅ |
| Adjusted S/D glut 26/27/28E | −14.6% / −13.9% / −21.7% | −15 / −14 / −22% ✅ |
| HBM ASP 26/27/28E | $1.936 / $2.752 / $3.370 per bit | $1.9 / $2.8 / $3.4 per Gb ✅ |

**➜ No datapoint was re-folded; the value is that the model is now auditable on disk rather than quoted second-hand.** One item the workbook makes newly visible: the accelerator-unit table (000s) runs **NVDA 8,920 → 9,975 → 11,640** against **ASIC 7,315 → 14,410 → 17,920** for 26/27/28E — **ASIC units pass NVDA units by ~1.44x in 2027E**, the unit-side counterpart of the "ASIC overtakes NVDA as the largest HBM bit consumer in 2027E (48% vs 42%)" conclusion already carried.

### E. ✅ Samsung's 60%-fulfilment figure corroborates Micron's, from the other side of the market.

UBS: *"only 60% of demand is fulfilled now (broadly in line with MU comments last week) and unfulfilled demand is being added to the 2027 base line."* ➜ **Two of the three DRAM suppliers, same week, same number** — and it matches the "60% of big-tech demand" datapoint already on `themes/hbm-memory.md` from 08-11. Supports the supply-not-demand reading of the de-spec debate.

---

## Open items carried forward

| # | Item | Resolves at |
|---|---|---|
| 1 | **HBM 2027 ASP: UBS +90% (Samsung blended) vs JPM +42% (industry $/Gb)** — 48pp, bases differ but not by that much | 4Q26 / Jan disclosures, or rebuild UBS on JPM's basis from the archived workbook |
| 2 | **LTA FCF deduction: UBS ("marginal … most LTAs have cash in escrow, by definition excluded") vs Citi/GS (deducted, shrinks the pool)** — a falsifiable *accounting* disagreement that sets the size of Samsung's payout pool | Samsung 4Q26 disclosure |
| 3 | **"Kestrel" codename collision** — MRVL/Google warrant trigger (⇒ possibly TPU v9, pre-Nov-27) vs a reported ~$100bn / 430-acre Google campus in Kansas City | MRVL Investor Day **10/6**, or the next 8-K |
| 4 | **Samsung FY27 OP spread ~15% wide** (JPM 549 → MS 629, consensus 583.7) — larger than the capital-returns debate and less discussed | 4Q26 print |
| 5 | **BBG live re-check** — every consensus figure here is from the 08-24 disk snapshot; the wrapper was down. **No CY2028 line exists in the snapshot**, which is exactly where the MRVL argument lives | Re-run `/wiki-consensus` once the Terminal is back |
| 6 | **KB conflict weighting** — KB is mandated on Samsung's treasury-share transaction while publishing a buyback-is-a-rerating-catalyst note. Its arithmetic checks out (item A); its enthusiasm should be discounted | standing |

_Generated by /run-inbox, 2026-08-24. BBG column sourced from `_data/estimates.json` (asof 2026-08-24) because the live `bdp()` wrapper raised ConnectionError; **no web data was substituted for consensus.**_
