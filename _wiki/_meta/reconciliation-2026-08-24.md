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

## Where the new data DIVERGES

### 1. 🔴🔴 HBM 2027 ASP — UBS **+90%** vs JPM **+42%**. The widest pricing gap on the wiki.

| Source | Figure | Basis |
|---|---|---|
| **UBS** (Gaudois, Korea Summit, 2026-08-24) | **Samsung blended HBM ASP +90% YoY in '27E** | Single supplier, blended across its own generation mix |
| **JPM** (Kwon, model of 2026-08-09, workbooks now on disk) | **industry HBM ASP +42% y/y '27** ($1.9 → $2.8 → $3.4 per Gb, 26/27/28E) | Industry-wide, $/Gb |
| BBG | **— no consensus line for HBM ASP** | n/a |

**Why it is not automatically a contradiction:** the bases differ. A single supplier's *blended* ASP can legitimately outrun an *industry* $/Gb series if that supplier's mix shifts hard toward higher-stack / HBM4E parts — and Samsung is precisely the name with the most mix headroom, entering 2027 with the lowest HBM4 base. **Why it is still the run's top item:** 48pp is far too wide for mix alone, and the two numbers drive opposite conclusions about how much of the 2027 memory P&L is price versus volume.

➜ **ACTION: resolve at the 4Q26 / January disclosures, or by rebuilding UBS's blended ASP on JPM's $/Gb basis from the `SKH HBM` / `Samsung HBM` sheets in `JPM_HBM_client_model_Aug2026.xlsx` (now archived in `_inbox\_done\`). Until then, do not quote either number without its basis. OPEN.**

### 2. 🔴 MRVL CY28 EPS — Wells Fargo AND JPM both land on ~$11/sh, **+12.0% above the live BBG consensus of $9.818** (UBS's $9.82 IS that consensus). Two houses, two independent methods, one above-Street number — and the PTs span $224-$325 on it.

> ✅ **08-25 resolution — READ THIS BEFORE THE TABLE BELOW.** Live BBG `3FY` consensus CY28 EPS is **$9.818**, so **UBS's $9.82 IS consensus (+0.02%), not a 12%-low outlier** — Wells and JPM are the two standing +12.0% ABOVE the Street. The finding survives and strengthens; the "UBS is the outlier" sentence does not. Full detail in the 08-25 layer at the end of this file.

| Source | CY28/FY29 EPS | PT | Date |
|---|---|---|---|
| **Wells Fargo** (Rakers) — NEW | **+$11/sh** | **$240 → $310** (~28x) | 08-24 |
| UBS (Arcuri) | $9.82 | **$340 → $300** (30x) | 08-24 |
| JPM (Sur) | ~$11.00 | OW | 08-19/24 |
| Morgan Stanley (Moore) | — | $195 → **$224** (EW) | 08-23 |
| BBG | **no CY2028 line in the snapshot** | — | — |

**➜ The genuine finding is a CONFIRM sitting inside a DIVERGE.** Wells Fargo and JPM land on **the same ~$11 CY28 EPS by fully independent methods** — JPM via a ~$19.2bn/yr Google attach, Wells via an **$80bn cumulative GOOGL revenue thru FY33** bridge at ~50% GM / ~12% opex-to-rev with warrant dilution. Two methods, one number, materially tightening the confidence interval around ~$11 and leaving **UBS's $9.82 as the outlier, 12% low**. Meanwhile the *targets* span **$224 → $310** on essentially agreed earnings.

➜ **So the open MRVL question is now the MULTIPLE, not the earnings power** — 28x (Wells) vs 30x (UBS) vs MS's explicit "still trades at more than 2x" relative objection. **That is a cleaner, more tradeable framing than the page had this morning.** ⚠️ **Wells' bridge rests on an assumption it flags itself: only ~60% of its Google revenue is treated as incremental to guidance. That single input, not the EPS, is what to stress.**

### 3. ✅ RESOLVED 2026-08-25 → CONFIRMS — Samsung FY27 operating profit. On the ANNUAL consensus line Goldman is **−1.5%**, not −3.8%, i.e. essentially AT consensus; and GS's **W490,000 PT IS the consensus target** (live `BEST_TARGET_PRICE` W490,018). What survives is the basis-independent **JPM 549 → MS 629 spread, +14.6%**. See the 08-25 resolution layer at the end of this file.

| Source | CY27 EBIT (W tn) | vs BBG |
|---|---|---|
| JPM | 549 | −5.9% |
| **Goldman (NEW, 08-23)** | **561.7** | **−3.8%** |
| KB | 575 | −1.5% |
| **BBG consensus (disk, 08-24)** | **583.7** | — |
| Morgan Stanley | 629 | +7.8% |

**➜ Goldman enters on the LOW side of consensus on 2027 operating profit while carrying the second-highest price target on the page (W490,000, Buy-on-Conviction-List).** That combination is the interesting part: GS is not underwriting the target with above-consensus out-year operating profit — it is underwriting it with **capital returns and a multiple**, which is exactly what its own text says (*"significant shareholder returns to help drive higher valuation multiples"*). ⚠️ **The MS-vs-JPM 15% spread on FY27 OP remains the larger, less-discussed disagreement on this name than the capital-returns argument the headlines are about — unchanged by this run, restated because a fourth house has now been added without narrowing it.**

### 4. ⚠️ NOT LOAD-BEARING — Samsung EPS. UBS reads −6.2% below consensus for CY26 and +25.6% above for CY28 on the bases printed here; on the live ANNUAL BBG line those become **+4.9% ABOVE** (CY27, sign flips) and **+11.6%** (CY28). A basis artifact, not a tradeable duration call.

> ⚠️ **08-25 resolution:** on the **annual** consensus line UBS is **+4.9% ABOVE** in CY2027, not −1.9% below — **the sign flips with the basis**, a year earlier than this table implies. Confirms the not-load-bearing caveat rather than repairing the row. See the 08-25 layer.

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
| 4 | ✏️ **UPDATED 08-25 — Samsung FY27 OP spread is +14.6% wide (JPM 549 → MS 629) and BASIS-INDEPENDENT.** Consensus is **W570.4tn on the annual line**, not the 583.7 CY sum used above; re-placed, all four houses cluster inside the Street's own dispersion and **MS's +10.3% is the tail, not Goldman's entry point** | 4Q26 print |
| 5 | ✅ **CLOSED 2026-08-25 — BBG live re-check done.** Terminal back up; `estimates.json` refreshed live to asof 2026-08-25 (98/98, 0 carry-overs) and the missing **CY2028 line pulled ad-hoc via `3FY`**. Snapshot figures verified accurate; **rows 2, 3 and 4 changed meaning** — see the resolution layer | ✅ closed |
| 6 | **KB conflict weighting** — KB is mandated on Samsung's treasury-share transaction while publishing a buyback-is-a-rerating-catalyst note. Its arithmetic checks out (item A); its enthusiasm should be discounted | standing |
| 7 | 🔴 **NEW 08-25 — Morgan Stanley's MRVL PT ($224) is 8.2% BELOW spot ($244.11) and 19.1% below the consensus target ($276.94).** An explicit relative-value short call unless MS moves it | MRVL print **8/27**, or an MS note |
| 8 | 🔴 **NEW 08-25 — is "UBS C2028 EPS $9.82" UBS's own estimate or the consensus line?** It matches the BBG `3FY` mean to three decimals ($9.818). Decides whether UBS is an independent third mark or a restatement of the Street | sight of the UBS primary |
| 9 | ⚠️ **NEW 08-25 — `fetch_estimates.py` has no units guard.** The WOLF ~1000x defect self-repaired on Bloomberg's side this run; nothing prevents its return, and nothing detects it automatically | a code fix (out of scope for a consensus refresh) |

_Generated by /run-inbox, 2026-08-24. BBG column sourced from `_data/estimates.json` (asof 2026-08-24) because the live `bdp()` wrapper raised ConnectionError; **no web data was substituted for consensus.**_

---

## BBG column resolved — live pull 2026-08-25 (`/wiki-consensus`, scheduled)

_The 08-24 report was written with the wrapper down and its BBG column taken from the same-day on-disk snapshot; **open item #5 asked for exactly this re-check.** Terminal is back up. Full live re-fetch: **`estimates.json` asof 2026-08-25, 98/98 names, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 names dropped or added, and 0 records byte-identical to the 08-24 vintage** — verified record-by-record in Python, **not** taken from the script's own `98/98 ok` line. Plus an **ad-hoc live `BEST_FPERIOD_OVERRIDE=1FY…4FY` pull of `BEST_SALES / BEST_EBIT / BEST_NET_INCOME / BEST_EPS / BEST_EPS_HI / BEST_EPS_LO / BEST_CAPEX` and a `PX_LAST / BEST_TARGET_PRICE / BEST_ANALYST_RATING / TOT_ANALYST_REC` pull for MRVL, SAMSUNG and SKHYNIX** — which is what supplies the **CY2028 line the snapshot does not carry**. No web data was substituted at any point._

**Headline: the 08-24 snapshot was accurate — every consensus figure in the report above re-prints within 0.02% on a like-for-like basis. But two of the five rows change their MEANING once the missing CY2028 line and the correct annual basis are supplied, and one of them inverts.**

### 🔴 ROW 2 MOVES — MRVL CY28 EPS. The report named UBS the outlier. **UBS is the consensus, to three decimals. Wells and JPM are the pair standing apart.**

`MRVL US Equity`, `BEST_FPERIOD_OVERRIDE=3FY` (= FY2029 ≈ CY2028), live 2026-08-25:

| CY28 / FY29 EPS | Figure | vs BBG consensus **$9.818** |
|---|---|---|
| **BBG consensus mean (3FY)** | **$9.818** | — |
| BBG street-high (`BEST_EPS_HI`) | $14.50 | +47.7% |
| BBG street-low (`BEST_EPS_LO`) | $7.50 | −23.6% |
| **UBS (Arcuri, 08-24)** | **$9.82** | **+0.02% — i.e. AT consensus** |
| **Wells Fargo (Rakers, 08-24)** | ~$11 | **+12.0%** |
| **JPM (Sur, 08-19)** | ~$11.00 | **+12.0%** |
| _page mark "Street ~$9.64" (08-24)_ | $9.64 | −1.8% (the page mark was stale-low) |
| _page mark "Street ~$9.52" (08-20)_ | $9.52 | −3.0% |

**➜ The report's framing — _"two methods, one number … leaving UBS's $9.82 as the outlier, 12% low"_ — is now the wrong way round.** UBS's $9.82 is not an idiosyncratic low mark; it is the Street's own mean to within 0.02%. The Wells/JPM convergence on ~$11 is **real and remains the finding**, but it is a convergence **away from** the Street, not a triangulation **of** it: two houses, +12% above consensus, arrived at independently. **That is a stronger, cleaner statement of the alpha than the report made** — the row stays in DIVERGES and gets *more* force, not less, but the sentence naming UBS as the outlier must not be quoted.

⚠️ **Two readings of UBS's $9.82, and this pull cannot separate them:** (a) UBS genuinely rebased its C2028 estimate onto consensus, or (b) the sales relay printed the *consensus* line and it was logged as UBS's own. A figure matching the BBG mean to three decimals is a coincidence worth naming. **Do not treat "UBS $9.82" as an independent house mark until the primary is seen.** _(This also bears on the standing UBS PT inconsistency: 30x × $9.82 = $295 ≈ the $300 PT, and 30x × $10.31 = $309 ≈ the $310 PT — both notes are internally consistent with their own stated EPS, so the $300-vs-$310 gap looks like a genuine estimate change between notes rather than relay corruption. Supporting evidence, not proof; the $300-310 range with dates attached still stands.)_

**Calibration on how big the ~$11 call actually is:** it sits **25% of the way from the consensus mean to the street high**, well inside a Street dispersion that runs $7.50–$14.50. **~$11 is an above-consensus call, not a heroic one.**

### 🔴 NEW — the MRVL disagreement decomposes exactly, and MS's target is now UNDERWATER

Live 08-25: **`PX_LAST` $244.11** · **`BEST_TARGET_PRICE` $276.94** · `BEST_ANALYST_RATING` 4.74/5 across **50** recommendations.

| House | PT | vs consensus PT $276.94 | vs spot $244.11 | Implied x on consensus $9.818 |
|---|---|---|---|---|
| Jefferies (Curtis, 08-20) | $325 | +17.4% | +33.1% | 33.1x |
| **Wells Fargo (08-24)** | **$310** | +11.9% | +27.0% | **31.6x** |
| UBS (08-24) | $300 | +8.3% | +22.9% | 30.6x |
| **BBG consensus PT** | **$276.94** | — | **+13.5%** | **28.2x** |
| **Morgan Stanley (Moore, 08-23)** | **$224** | **−19.1%** | **−8.2% — BELOW the share price** | 22.8x |

**➜ The consensus target is 28.2x consensus CY28 EPS — which is, to a rounding error, the *~28x Wells says it is using*.** So the two ends of the debate separate cleanly and neither is doing anything exotic with the multiple: **Wells gets to $310 by applying the market's own multiple to an above-consensus EPS; MS gets to $224 by applying a 22.8x multiple to the market's own EPS.** The report's conclusion — _"the open MRVL question is now the MULTIPLE, not the earnings power"_ — **is confirmed and now quantified: the multiple spread (22.8x–33.1x) is doing roughly half the work, the EPS spread (0% to +12%) the rest.**

🔴 **And the tape has overtaken the note.** MRVL **$225.11 (08-24) → $244.11 (08-25), +8.4% in one session** — so the report's warning that _"every Wells upside/downside percentage in that note is stale"_ was right but **now points the other way**: the stock is **+3.0% ABOVE Wells' $237.04 reference price**, not 5% below it. Wells' printed **+30.8%** upside is really **+27.0%**. **MS's $224 target has been taken out to the upside and now sits 8.2% below spot** — a target that argued the stock was expensive at $225 is a short call at $244 until MS moves it. **Diarise against the 8/27 print.**

### ⚠️ ROW 3 RE-PLACED, AND KB CROSSES THE LINE — Samsung FY27 OP on the ANNUAL consensus line, not the CY sum

The report used the **CY2027 calendar sum (W583.7tn)**, correctly flagging the Korean CY-sum caveat as a standing warning. The live annual pull now lets that caveat be **quantified instead of just flagged — and it inverts by year exactly as the standing note says:**

| Samsung EBIT | Annual line (`kFY`) | CY sum (`estimates.json`) | CY sum is |
|---|---|---|---|
| FY2026 | **W384.4tn** | W379.1tn | **−1.38% BELOW** |
| FY2027 | **W570.4tn** | W583.7tn | **+2.34% ABOVE** |

**FY27 operating profit re-placed on the annual line (`2FY`, W570.4tn):**

| Source | CY27 EBIT (W tn) | vs ANNUAL line | _(vs CY sum, as printed 08-24)_ |
|---|---|---|---|
| JPM | 549 | **−3.8%** | _(−5.9%)_ |
| **Goldman (08-23)** | **561.7** | **−1.5%** | _(−3.8%)_ |
| **KB** | **575** | **+0.8% — ABOVE** | _(−1.5% — below)_ |
| Morgan Stanley | 629 | **+10.3%** | _(+7.8%)_ |

**➜ Two things change.** (1) **KB flips sign** — on the correct annual basis it is *above* consensus, not below. (2) 🔴 **Goldman is not "on the LOW side of consensus" — at −1.5% it is essentially AT consensus**, inside the noise. **The report's item-3 thesis (_"GS is not underwriting the target with above-consensus out-year operating profit — it is underwriting it with capital returns and a multiple"_) therefore loses most of its force and should not be quoted as written.**

🔴 **The second leg of that thesis fails outright on a live pull.** The report describes Goldman as _"carrying the second-highest price target on the page (W490,000)"_. Live: **`BEST_TARGET_PRICE` = W490,018** across 44 recommendations (rating 4.93/5). **Goldman's W490,000 IS the consensus target, to 0.004%.** GS is at consensus on the target *and* at consensus on FY27 OP — there is no "high target on low estimates" combination left to explain. **Row moves from DIVERGES to CONFIRMS.**

**What survives, and it is the part the report already said was the bigger story:** the **JPM 549 → MS 629 spread is +14.6% and is basis-independent** — it does not move with the CY/annual choice. For scale, the Street's own FY27 EPS dispersion is `BEST_EPS` 70,453 with high 95,681 (+35.8%) and low 51,001 (−27.6%), so **all four house OP marks sit well inside the Street's own band.** ➜ **Item 3 is downgraded to: the four houses are tightly clustered around consensus on FY27 OP, and the real disagreement is MS's +10% tail, not Goldman's entry point.**

### ✅ ROW A CONFIRMS, but the "inside 0.3%" precision was a CY-sum artifact

| Source | CY26 OP (W tn) | vs ANNUAL W384.4tn | _(vs CY sum W379.1tn)_ |
|---|---|---|---|
| Goldman | 379.0 | −1.4% | _(−0.02%)_ |
| KB | 380 | −1.1% | _(+0.24%)_ |

**➜ Still a CONFIRM — both houses land within 1.4% of consensus, and the report's real point stands untouched: KB's _"2026E OP of KRW380tn"_ is consensus, not a typo, and the reconcile-before-rejecting lesson holds.** But **the headline _"three independent sources inside 0.3%"_ is an artifact of the calendar sum**; on the annual line the agreement is inside 1.4%. Accurate, less dramatic.

### ⚠️ ROW 4 — the report's own "NOT LOAD-BEARING" warning is vindicated harder than it knew: the sign flips

| Samsung EPS | Annual (`kFY`) | CY sum | CY sum is | UBS vs ANNUAL | _(UBS vs CY sum, as printed)_ |
|---|---|---|---|---|---|
| CY2026 | W48,057 | W46,433 | −3.38% | **−9.4%** | _(−6.2%)_ |
| CY2027 | W70,453 | W75,326 | **+6.92%** | **+4.9% — ABOVE** | _(−1.9% — below)_ |

**➜ On the annual line UBS is ALREADY above consensus by CY2027, not "below near-term, above in the out-years" crossing somewhere in CY2028.** The duration crossover happens **a full year earlier** than the report's table implies. ⚠️ **This does not make the row usable — the common-vs-preferred share-count trap is untouched by any of this, and Samsung stays reconciled at OPERATING PROFIT / NET INCOME, never EPS.** It is logged as a **worked example of why**: the same broker, the same consensus, two bases, opposite signs.

### ✅ ROW C CONFIRMS and extends — the sell-off was real, and it has partly retraced

| Samsung mark | Level | |
|---|---|---|
| 21-Aug (UBS note) | W281,500 | — |
| 24-Aug (UBS note) | W257,000 | −8.7% |
| **24-Aug BBG disk** | **W256,000** | 0.39% from UBS — same mark ✅ |
| **25-Aug BBG live** | **W261,000** | **+1.95% vs 08-24; still −7.3% vs 21-Aug** |

**➜ The report's empirical resolution of the 08-21 three-way disagreement in favour of the MS/JPM "sell-the-news" read stands — but ~22% of the drop came back the next session, so it reads as a sharp de-rating on the announcement rather than a decisive re-rating trigger either way.** ⚠️ **Context the report could not have: `BEST_TARGET_PRICE` W490,018 vs spot W261,000 is +87.8% consensus upside, and SKHYNIX prints +88.5% on the same day (W3,231,945 vs W1,715,000). The Street is carrying ~88% upside on BOTH Korean memory names simultaneously** — a positioning fact that dwarfs the W25,000 argument the notes are having.

### Rows unchanged

- **Row 1 (HBM 2027 ASP, UBS +90% vs JPM +42%)** — **no BBG consensus line exists for HBM ASP.** Correctly marked "n/a" in the report; **stays OPEN**, unarbitrable by this or any BBG pull. Resolution path unchanged: 4Q26/January disclosures, or rebuilding UBS on JPM's $/Gb basis.
- **Row 5 (Vera Rubin / AgentX)** — a corpus-integrity item with no quantitative mark. **No BBG line; unchanged.**
- **Row B (Wells near-year MRVL) CONFIRMS on the annual line too**, and slightly tighter: FY27 rev +1.6%, FY27 EPS **+0.4%**, FY28 rev −0.7%, FY28 EPS −1.9% vs `1FY`/`2FY`. ⚠️ **One live correction: Wells printed consensus FY28 EPS of $6.19 (8/23); the live line is $6.339, +2.4% in two sessions.** Consensus is revising **up** into the print, so Wells' "we are at consensus" claim is already marginally stale on the low side.
- **Row D (JPM workbooks)** — internal model-vs-model audit, no consensus component. Unchanged.
- **Row E (60% fulfilment)** — no BBG line. Unchanged.

### Data-quality findings from this refresh

- ✅ 🔴 **The WOLF ~1000x units defect logged on 08-24 has REPAIRED ITSELF on Bloomberg's side — the standing "do not quote WOLF revenue" warning is LIFTED.** `BEST_SALES` for `WOLF US Equity` now returns **150.0 (millions)** where it returned **75,075.0 (thousands)** on 08-21 and 08-24. CY2026 revenue **$151,952.2m → $603.7m**, CY2027 **$356,364.5m → $720.5m**, against a **$1.34bn market cap** and **$665.1m of latest actual FY revenue** — coherent for the first time (0.45x rev/market-cap, vs 122x). ⚠️ **This was a Bloomberg-side fix, not a code fix: `fetch_estimates.py` still carries no units guard, so the defect can silently return.** Any note quoting WOLF revenue, EBITDA margin or EV/sales off an **08-24-or-earlier** vintage is still ~1000x too high.
- **Re-screened all 98 names for the same scale defect: one flag, and it is the documented benign one.** Only **TM** exceeds 5x revenue/market-cap (188x) — the known ADR basis split (fundamentals in JPY, `mktcap` in USD). **No other name fails.**
- **Consensus was near-static; the tape did all the work.** Only **3 names** moved CY2026 rev/EPS by >0.5% (CRWD EPS +1.7%, VST EPS +0.6%, WOLF = the units repair) and **8** on CY2027 (NVT rev +2.4%, VST EPS +1.4%, SNPS EPS −0.6%). Against that: **MRVL +7.8%, SMCI +9.3%, AXTI +9.6%, BE +8.4%, LITE +5.9%, NBIS +5.8%** in one session. **Estimates did not move; prices did — which is precisely the condition under which PT-vs-spot rows go stale fastest.**
- ⚠️ **Standing gaps, unchanged:** `estimates.json` carries **no `BEST_TARGET_PRICE`** and **no CY2028**, so both still require an ad-hoc pull every run — **and as this resolution demonstrates, that is not a cosmetic gap: the single most important row in this report could not be arbitrated without it.**

### 🔴 ADDENDUM — the Samsung "+25.6%" in row 4 is measured against a consensus line that BBG does not recognise, and the cross-check locates the fault precisely

Row 4's CY2028 cell reads `UBS W84,988 vs (UBS prints cons. 67,676) = +25.6%` — it is placed against **UBS's own printed consensus**, because the snapshot has no CY2028. The live `3FY` pull supplies the missing line, and the three-year cross-check of *UBS's printed consensus against BBG's* is the interesting part:

| Samsung EPS (W) | UBS's printed consensus | BBG live (`kFY`) | UBS-printed vs BBG |
|---|---|---|---|
| FY2026 | 48,038 | **48,057** | **−0.04% — identical** |
| FY2027 | 69,075 | **70,453** | −1.96% |
| **FY2028** | **67,676** | **76,179** | **−11.16%** |

**➜ The two vendors agree to within 0.04% in FY26 and to 2% in FY27, then blow apart to 11% in FY28. A share-count / preferred-inclusive basis difference would show up as a roughly CONSTANT wedge across all three years — it does not.** So the FY2028 gap is **year-specific, not basis-driven**, and the tell is the shape: **UBS's printed consensus has Samsung EPS FALLING in FY28 (69,075 → 67,676, −2.0%), while BBG's panel has it RISING (70,453 → 76,179, +8.1%).** Two consensus panels, opposite directions, on the same year.

**➜ Placed against the line BBG actually carries, UBS's own FY2028 estimate of W84,988 is +11.6% above consensus — not +25.6%.** More than half of the report's headline gap was the *denominator*, not UBS's view. ⚠️ **The row stays NOT LOAD-BEARING and stays out of anything tradeable** — but the reason is now demonstrated rather than asserted: **any out-year Samsung comparison against a broker's own printed consensus is unsafe, because the out-year panels themselves disagree by double digits.** The standing rule is unchanged and reinforced: **reconcile Samsung at OPERATING PROFIT / NET INCOME on the annual line, never at EPS, and never against a broker-printed consensus.**

_BBG column resolved 2026-08-25 — `estimates.json` asof **2026-08-25**._
