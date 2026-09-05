# Reconciliation — 2026-09-04 (/run-inbox)

_Variance pass on every NEW quantitative datapoint from tonight's ingest, against three baselines: **(1)** prior wiki comments on disk, **(2)** Capstone house models, **(3)** BBG consensus._

**Sources reconciled (2 of 3 ingested files carry numbers):**
- **UBS · Karl Keirstead** — post-print client call on [[SNOW]] Q2 FY27, 2026-09-03 → [SNOW.md](../SNOW.md), [PLTR.md](../PLTR.md), [themes/tokenmaxxing.md](../themes/tokenmaxxing.md)
- **Mirae Asset Securities · Seun-young Park** — "Robotics: The humanoid era begins", sector initiation at Overweight, 2026-08-21 → [themes/humanoids-robotics.md](../themes/humanoids-robotics.md)
- *(The third inbox file, a claimed JPM/Harlan Sur AVGO call, was rejected as defective — wrong-doc contamination, no datapoints. Nothing to reconcile.)*

**Baseline availability**
| Baseline | Status |
|---|---|
| **(1) Prior wiki comments** | ✅ on disk, used throughout |
| **(2) Capstone house models** | ⛔ **none exist for these names.** SNOW.md states explicitly: *"No Capstone position or house model on disk."* PLTR is likewise absent from `P:\Felipe Monteiro\US Equities\Modelos oficiais\` (NVDA, GOOG, AVGO, COHR, LITE, META, TSM, AAPL, ASML-peers). Korean small-caps obviously not covered. **Not "pending" — genuinely absent.** |
| **(3) BBG consensus** | ✅ **NOT pending.** `_wiki/_data/estimates.json` carries **`asof: 2026-09-04`** — a same-day snapshot that post-dates the 2026-09-02 SNOW print, so it is a valid live baseline. No Terminal call needed and none made. Korean names (Robotis 108490 KQ / SPG 058610 KQ / SBB Tech 389500 KQ) are outside the 100-name estimates universe — no BBG line exists for them. |

⚠️ **Basis discipline applied throughout (SNOW has a January-31 FYE):** `lrq = 2026-07-31` ⇒ **`1FY` = fiscal FY27 (ending 2027-01-31)**, `2FY` = FY28. The `CY2026`/`CY2027` blocks are calendar sums that straddle two fiscal years and **were not used for any fiscal comparison** — all annual figures below come from the `1FY`/`2FY` lines, per the standing off-calendar-FYE rule.

---

## 🔴 DIVERGES (the alpha)

### 1. SNOW — consensus FY27 sits **exactly on the guide**, embedding **zero beat**, against a company that has beaten 5%+ twice running

| | Value | Source |
|---|--:|---|
| SNOW's own FY27 **product** revenue guide | **$6,070m** | Q2 FY27 call, 2026-09-02 |
| BBG consensus FY27 (`1FY`) **total** revenue | **$6,294.7m** | BBG, asof 2026-09-04 |
| Implied product/total ratio | **96.4%** | derived |
| ⇒ Consensus **product** revenue | **~$6,068m** | derived |
| **Gap vs guide** | **−0.03%** | — |

➤ **Consensus is on the guide to within three basis points.** Cross-checked on the quarter and the ratio holds: the Q3 guide midpoint of $1,590m against BBG's `1FQ` total of $1,648.2m implies **96.5%** — the same ratio from an independent line, so this is a real relationship, not a fitted one.

➤ **The divergence:** Keirstead expects **4–5pt beats "at least for the next couple of quarters"** — explicitly *against* CFO Robins' standing "a 3% beat should be considered solid" — because "Brian and the team frankly don't have enough history with the extent of this boost" from CoCo. The realised record on the page backs him: the last four product beats ran **5.4% / 2.3% / 2.6% / 5.2%**, and DB notes these are **the first back-to-back 5%+ beats** in the company's history. **Two 4% beats on the Q3 and Q4 guides add ~$140m ⇒ FY27 product ~$6.21bn, ~2.3% above the consensus line.**

**Action:** this is the cleanest quantified edge in tonight's run. Consensus has priced the guide and nothing more; the debate is entirely about beat magnitude, and both the analyst and the track record sit above the Street's implied zero.

### 2. SNOW — UBS's 42–43% Q4 exit rate requires sequential growth to hold; consensus has it **halving**

| | q/q step | Basis |
|---|--:|---|
| Q2 FY27 actual → Q3 FY27 **guide** ($1,492m → $1,590m) | **+6.6%** | product, company |
| BBG `1FQ` → `2FQ` ($1,648.2m → $1,721.2m) | **+4.4%** | total, consensus |

➤ Keirstead: *"you can run pretty reasonable numbers and get to **42, 43**"* for the 4Q FY27 exit — against the **39–40% January exit bogey heading into the print** and the ~40% "the bulls were modeling" — and *"it wouldn't shock me if it's in the **43 to 45%** zip code"* once the buy-side re-marks. **Consensus embeds sequential dollar growth decelerating by a third into the quarter management itself has flagged as the renewal-heavy one.**

⚠️ **Caveat, stated so it is not over-read:** the two lines are on different revenue bases (product vs total). The comparison is made **on sequential growth**, not on level, and the product/total ratio is stable at 96.4–96.5% across two independent lines — but a precise Q4 y/y bridge would need the FY26 quarterly product split, which is not on disk. **Treat the direction as solid and the magnitude as indicative.**

### 3. SNOW — the wiki's terminal-value bear is **not in the consensus distribution at all**

| BBG PT panel (asof 2026-09-04) | |
|---|--:|
| Consensus | **$430.56** |
| Street high | $525.00 |
| **Street low** | **$280.00** |
| Analysts / Buy / Hold / Sell | 56 / 50 / 5 / 1 |

➤ The page's standing bear — **Rothschild & Co Redburn · Alex Haissl, Sell, PT $110** (2026-05-14) — sits **$170 below BBG's street low**, i.e. **74.5% below consensus**. It is therefore **not in the 56-analyst panel**, or the panel's mark has moved and the wiki's has not.

➤ **Why it matters, and it cuts both ways:** the terminal-value/share-loss bear that [SNOW.md](../SNOW.md) § Debate carries as a live risk is **invisible in the consensus distribution**. There is no crowded bear positioning to squeeze — but equally, no one else on the Street is validating the short, and the "1 Sell" in the panel is somebody else at a much higher price. **Action:** the Redburn PyPI share-data refresh already flagged in § Catalysts is the resolving event; until then, treat the $110 as an outlier mark that consensus does not see.

### 4. SNOW — the CoCo estimate has **no consensus counterpart to diverge from**, which is itself the finding

➤ Keirstead's bottom-up: **~$135m** embedded from last quarter's $180m guide raise (75% of it CoCo) **+ ~$150m** from this quarter's $230m raise ("again said that that was mostly AI") ⇒ **~$300m FY27, upside $350m**, "quickly marching towards being a half a billion dollar" product. That is **~4.9% of the $6,070m FY27 product guide**, and it attributes **~$285m of the $410m in cumulative FY27 raises (~70%)** to one product.

➤ **BBG carries no product-line split**, and management refused to size CoCo on this very call ("Brian didn't want to size it in any way for me"). **The number is unfalsifiable against consensus today.** ⚠️ **Logged on the page as broker arithmetic, explicitly not as a company figure.** The test is the *composition* of the next guide raise, or a first disclosure — both flagged in § Catalysts.

### 5. Humanoids — the new source **contradicts the data already on the theme page, twice, in the same direction**

| Metric, 1H 2026 | **Mirae Asset** (2026-08-21) | **Counterpoint** (2026-08-19, already on page) | Gap |
|---|--:|--:|--:|
| Industrial (+ commercial) share of shipments | **"over 70%"** | **~18%** industrial end-use | **~4x** |
| Global humanoid shipments | **19,000** (+272% YoY) | **22,000+** (+~300% YoY) | **−14%** |

➤ **Mirae's own figure captions read "Source: Counterpoint Research, Mirae Asset"** — so it is citing Counterpoint and printing a materially lower unit number.

➤ **Not resolvable tonight, and deliberately not averaged.** The mix gap is most likely definitional — Mirae's bucket is *industrial **and commercial***, plausibly sweeping in retail/service placements Counterpoint leaves outside "industrial" — but **neither source publishes bucket definitions.** Both numbers now sit on the page and **neither is load-bearing.**

➤ **Why this is alpha and not housekeeping:** it decides whether the category is still demo-led. **Nomura's Unitree risk section (on the same page) says ">73% of humanoid revenue tied to research/education"** — so two of three sources say demo-led, and Mirae says ~70% real end-use. **Anyone sizing the humanoid component TAM off the mix number is picking a side of a 4x disagreement without knowing it.** Action: watch for a source that publishes bucket definitions; treat 1H26 shipments as a **19–22k range**, never a point estimate.

---

## ✅ CONFIRMS (no action)

### 6. SNOW — UBS's "65–70x CY27 free cash flow" reconciles **exactly** to the on-disk consensus

EV **$120.85bn** ÷ (BBG CY2027 revenue **$8,086.8m** × the **23% FCF margin** management reiterated on the call = **$1,860m**) = **65.0x** at spot $347.46. Keirstead quoted the range *"at the expected open"*; consensus puts **the bottom of his range on the number**. His characterisation — *"rich, to be clear, but it's not outrageous for a mid-40s percent growth profile"* — is a judgment, not a number, and is logged as such.

### 7. SNOW — the post-print PT wave clusters tightly around consensus, and **nobody set a new Street high**

| House | PT | vs BBG cons $430.56 | vs spot $347.46 |
|---|--:|--:|--:|
| Goldman Sachs · Borges | $436 | **+1.3%** | +25.5% |
| J.P. Morgan · Chatterjee | $426 *(Dec-27)* | −1.1% | +22.6% |
| Deutsche Bank · Zelnick | $400 | −7.1% | +15.1% |
| Barclays · Lenschow *(EW)* | $384 | −10.8% | +10.5% |
| UBS · Keirstead | *no PT on the call* | — | — |

⚠️ **JPM's is a December-2027 target — one year longer-dated than most of the panel — so its −1.1% is not level-comparable.** The BBG street high of **$525** still sits above every mark the wiki carries: **the post-print revision wave did not reset the top of the range.**

### 8. PLTR — Keirstead's "90, 95%" is **total revenue growth, and it is right**

The page's § Current state has PLTR Q2 2026 **total revenue +93% y/y** ($1.94bn vs Street $1.81bn). No base ambiguity — logged as stated. Databricks' *"core, even when you strip out the pass through revs, mid 60s"* has no independent on-disk check (private company); logged with the "ex-pass-through" qualifier attached, which is the part that matters.

### 9. PLTR — UBS PT $220 is above consensus but not a Street high

BBG cons **$200.07** (n=35, hi $255, lo $80, 24 buy / 9 hold / 2 sell) ⇒ UBS **+10.0%**, and **$35 below** the street high. Unchanged by tonight's source, which carries no new PLTR estimate.

### 10. Humanoids — Mirae **corroborates** three numbers already on the page from independent sourcing

- **Unitree 2025 revenue CNY1.7bn (+335% YoY), first to profit** — independent of Nomura's prospectus-derived numbers on the page (>5,500 units, GM 44–45% FY22 → 60% FY25, profitable).
- **FY2026 global shipments 50,000–60,000** — against Counterpoint's *"exceed 50,000 units in 2026 (+210%)"*.
- **500,000 units by 2030** — against MS's **446k by 2030e for China alone**; mutually consistent on a global-vs-China basis.
- **New, uncontested:** China took **>90% of global humanoid shipments in 2025 and 97% in 1H26** — the sharpest concentration figure the page carries.

---

## ⚠️ BASIS NOTES (differences that are NOT divergences — recorded so nobody logs them as one)

1. **SNOW's 74% gross-margin guide is not comparable to BBG's ~71.4%.** The guide cut (75% → 74%) is a **PRODUCT** gross margin; BBG's `1FY` gm of **71.418%** is **total-company** (product plus professional services). **Do not read the cut as a consensus miss.** Keirstead's framing — the entire AI ramp weighing on product GM *"by 100 bips. I can easily tolerate that"* — is on the product basis and is internally consistent with the guide.
2. **Karp's "100%+ US revenue growth for the next 18 months" cannot be checked against BBG.** The panel carries **total** revenue only (`2FY`/`1FY` = **+50.7%**); the goal is a **US** number. Different base — not a divergence, and not evidence either way.
3. **SNOW's `CY2026`/`CY2027` blocks are not fiscal years** (FYE January 31). Every fiscal comparison above uses `1FY`/`2FY`. Recorded because the CY label is actively misleading for this name.
4. **Mirae's "US$3mn → US$100,000 per robot, ~30-fold over a decade" is a per-robot COST/PRICE series, not a bill of materials.** It must **not** be chained to or netted against Bain's **$40–50k → $10–20k by 2035** BOM or MS's **$46k (2025) → $16k (2034)** China-supply-chain BOM, both of which are component-level. Three bases, all in dollars per robot. Written into the theme block as a standing warning.
5. **The Korean initiations (Robotis TP W356,000 / SPG W129,000 / SBB Tech W47,000, all Buy) have no consensus or house baseline** and are reconciled against nothing. They are logged with their valuation methods (P/S 42.3x, 7.3x and 15.1x on 2027F SPS respectively) so the multiple assumption is visible; **SBB Tech carries a 2026F operating LOSS of W5bn, so its target rests entirely on the 2027 line.**

---

## Carried forward

- **SNOW:** the composition of the next guide raise, or any first CoCo disclosure, tests the ~$300m estimate (§ Catalysts). The Redburn PyPI refresh tests the $110 outlier.
- **PLTR:** the ~Sep 9–10 customer/leadership event and Keirstead's dinner with the CFO/CRO — watch for the UBS note off it (§ Catalysts).
- **Humanoids:** the mix contradiction stays open until a source publishes end-use bucket definitions.
- **AVGO:** got nothing tonight — the inbox file was defective. Re-request the JPM/Harlan Sur recording from the desk.
