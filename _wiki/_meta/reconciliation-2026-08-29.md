# Reconciliation — 2026-08-29 (/run-inbox, 8 sources)

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines: (1) prior wiki comments, (2) the Capstone house model (`_data/house.json`), (3) BBG consensus. **DIVERGES = the alpha. CONFIRMS = no action.**_

⚠️ **BBG COLUMN PROVENANCE — READ THIS FIRST. A LIVE `bdp` PULL FAILED TONIGHT** (`ConnectionError: blpapi: could not start session` — Terminal not running / logged out, expected on a 23:40 unattended run). **The BBG column below is therefore the ON-DISK CONSENSUS SNAPSHOT `_data/estimates.json`, asof 2026-08-28 — i.e. genuine BBG consensus, ONE DAY STALE, not a live quote.** No web data has been substituted. Re-run `/wiki-consensus` with the Terminal up to refresh.

⚠️ **TWO STANDING BASIS HAZARDS APPLY THROUGHOUT AND ARE HANDLED EXPLICITLY BELOW: (a) `estimates.json` CY sums embed PRE-PRINT consensus for already-reported quarters, so CY2026 understates — CY2027 is the cleaner comparison year; (b) THERE IS NO CY2028 IN BBG AT ALL, so every 2028 claim below is reconciled against the broker's own cited consensus only, and marked PENDING for BBG.**

---

## 🔴 DIVERGES — the alpha

### 1. [[META]] 2027 CAPEX — the widest single-name divergence on this wiki, and it now has FOUR marks

| Mark | 2027 capex | vs BBG ($214.6bn) | Source |
|---|--:|--:|---|
| **R&Co Redburn · Dominic Ball** | **$142.2bn** | **−33.7%** | primary PDF, 2026-07-30 |
| **Capstone house model** | **$170bn** | **−20.8%** | `house.json` |
| Wells Fargo · Gawrelski | $180bn | −16.1% | primary PDF, 2026-07-09 |
| **Citi AI Industry Model** | **$205.3bn** | **−4.3%** | workbook, 2026-08-05 |
| Buy-side bar (per Ball's own investor conversations) | *">$200bn"* | ≈flat | 2026-07-30 |
| **BBG consensus (08-28 snapshot)** | **$214.6bn** | — | `estimates.json` |

🔴🔴 **THE FINDING THAT MATTERS, AND IT IS NOT VISIBLE FROM THE NOTE ALONE: Redburn published his gap as −15% vs consensus, citing Visible Alpha consensus of $167.0bn on 2026-07-30. BBG consensus one month later is $214.6bn. **CONSENSUS HAS RISEN ~28% SINCE HE PUBLISHED, SO HIS ACTUAL GAP HAS WIDENED FROM −15% TO −34%** — the position got roughly twice as contrarian without the analyst changing a number.** ⚠️ **Part of that move is vendor (Visible Alpha vs BBG) and part is genuine consensus drift over four weeks — both are named here rather than smoothed. Either way the direction is unambiguous.**

➤ **HOUSE POSITION, AND THIS IS THE ACTIONABLE PART: the Capstone model at $170bn is ALREADY BELOW BBG BY 21%, i.e. the house is leaning the same way as Redburn, just less far. The house is NOT the consensus view on Meta capex — it is a quarter of the way to the most contrarian mark on the page. Same shape in 2026: house $131bn vs BBG $150.6bn (−13%), Redburn $141.6bn, Citi $143.7bn.**

**Resolution mechanism (dated, falsifiable): Meta's own 2027 capex guide, expected with the Q4'26 print. Susan Li explicitly deferred the 2027 financing decision on the Q2 call, so an early signal could come sooner via a financing announcement.**

### 2. [[META]] 2028 — the capex-CUT call, ⚠️ BBG PENDING (no CY2028 line exists)

| Metric | Redburn 2028E | Redburn's cited consensus | Gap | BBG |
|---|--:|--:|--:|:--:|
| Capex | **$131.4bn** | $184.0bn | **−28.6%** | **PENDING** |
| EPS | **$59.0** | $40.33 | **+46.3%** | **PENDING** |
| Total revenue | $456.4bn | $354.9bn | +28.6% | **PENDING** |
| "Other revenue" | **$68.3bn** | $7.6bn | **+801%** | **PENDING** |
| FCF | **$138.3bn** | $15.9bn | **+768%** | **PENDING** |

⚠️ **CORRECTION CARRIED FROM THE INGEST: this page previously recorded Redburn's 2028 capex as "~$100bn" (from the Rowan Joseph relay). The primary says $131.4bn. The −29% direction survives; the magnitude was overstated by ~30% in the relay. Retired to META's `## Changelog`.**

➤ **Why the "other revenue" line is the real divergence rather than capex: Redburn is +801% vs consensus on a line consensus barely models ($7.6bn). The capex cut is a CONSEQUENCE of his SMB-LLM/AI-cloud revenue thesis, not an independent forecast. Judge the two separately — the capex call can be right for reasons unrelated to the revenue call, and vice versa.**

### 3. [[KIOXIA]] — Bernstein models 2027 EPS DOWN while consensus models it UP (the direction, not just the level)

| | Bernstein (28-Aug) | BBG CY2027 | Gap |
|---|--:|--:|--:|
| EPS 2026E | JPY 10,013 | JPY 8,116 | +23.4% |
| **EPS 2027E** | **JPY 9,657** | **JPY 13,768** | **−29.9%** |
| Direction y/y | **FALLING** | **RISING** | **OPPOSITE** |

🔴 **This is the cleanest DIVERGES in the memory complex tonight: Bernstein is the ONLY Underperform in its own memory coverage (Samsung, SK hynix, Micron, SanDisk, Seagate, WDC are all Outperform), PT JPY 40,000 vs a JPY 47,900 close = ~17% downside — and the mechanism is an EPS line that declines into 2027 while every other name in the same table compounds sharply.** ⚠️ **Period-basis caveat stated rather than ignored: Kioxia's fiscal year ends in March, so Bernstein's FY labels lead the BBG calendar year. That shifts the LEVELS but does not explain an inverted DIRECTION — which is why this is logged as a real divergence and not a basis artifact.**

**Corroborating, independent of the model: TrendFocus 2Q26 data via Wells Fargo has Kioxia's enterprise-SSD share at ~8% of EBs, DOWN from 10% in 1Q26, against [[MU]] 14.6% and [[SNDK]] ~19%. Share loss in the one pool that is growing.**

### 4. [[SNDK]] — two houses, ~2x apart on price target, on OPPOSITE ratings, seven days apart

| House | Date | Rating | PT | Price at note |
|---|---|---|--:|--:|
| **Bernstein** (Mark Li et al.) | 2026-08-28 | **Outperform** | **$3,000** | $1,484.95 |
| **Wells Fargo** (Rakers) | 2026-08-21 | **Equal Weight** | **$1,550** | $1,587.58 |

🔴 **A ~94% PT gap with opposite ratings on the same name in the same week is the widest single-name disagreement in memory on this wiki. Neither is stale. This is not reconcilable by basis — it is a genuine disagreement about NAND through-cycle earnings power, and it should be treated as an open position question rather than averaged.** ⚠️ **Note Bernstein's $3,000 is unchanged from its own 07-20 mark already on the SNDK page — the primer RE-STATES it, so this divergence has been open for five weeks, not one day.**

### 5. [[MSFT]] — Citi's 2027 capex sits 23% ABOVE BBG (flagged, but basis is uncertain)

**Citi $252.9bn (2027E) vs BBG $205.2bn = +23.2%; 2026E Citi $174.1bn vs BBG $153.5bn = +13.4%.** ⚠️ **HELD AS A SOFT DIVERGENCE, NOT A HARD ONE: Citi's row is labelled "Calendarized Azure CAPEX," and it is not established whether that is a SUBSET of Microsoft total capex (which would make a +23% reading over BBG total impossible to interpret) or a full-company calendarisation. Until the line definition is confirmed, do not trade this gap. Contrast with the AMZN row below, where the same ambiguity resolves the other way.**

---

## ✅ CONFIRMS — no action

### [[SKHYNIX]] — Bernstein 2027 EPS is within 0.2% of BBG
**Bernstein KRW 568,862 vs BBG CY2027 KRW 567,860 = +0.18%.** ➤ **Effectively identical. Bernstein's Outperform / KRW 3,300,000 is a VALUATION call on consensus numbers, not an estimate call — useful to know, because it means the SK hynix bull case does not depend on beating the Street's model.** (2026E is +23% above BBG, consistent with the known CY-sum understatement in a reported year.)

### [[SAMSUNG]] — Bernstein EPS within 3-4% of BBG, ⚠️ but read with the share-count caveat
**Bernstein 2026E KRW 48,393 vs BBG 46,433 (+4.2%); 2027E KRW 77,273 vs BBG 75,326 (+2.6%).** ⚠️⚠️ **PER THE STANDING RULE ON THIS WIKI, THIS COMPARISON IS ONLY PROVISIONALLY VALID: Bernstein prints the SAME EPS against both the common (005930) and preferred (005935) lines, and broker headline EPS is typically common-only while BBG is preferred-inclusive. The 3-4% agreement may therefore be coincidental. For any decision, place Samsung at NET INCOME (BBG CY2027 KRW 473.4tn), not EPS.**

### [[SHOP]] — Redburn's EPS is the consensus number; the revenue "gap" is a BASIS ARTIFACT, not a divergence

| | Redburn 2027E | BBG CY2027 | Read |
|---|--:|--:|---|
| EPS | **$2.5** (PT bridge uses **$2.55**) | **$2.55** | ✅ **IDENTICAL** |
| Revenue | $8,900m | $18,943m | ⚠️ **BASIS ARTIFACT — do NOT log as a divergence** |

🔴 **SCREENED OUT DELIBERATELY: Redburn's revenue line is ~47% of the BBG line in both 2026 and 2027, and Redburn's own note reports its revenue as **+3% vs consensus** — which is impossible against a number 2x larger. Redburn is modelling Shopify on a NET revenue / gross-profit basis while BBG carries GROSS revenue (Shopify reports merchant solutions gross, including payment processing). This is exactly the gross/net artifact the edge screen is supposed to reject, and it is rejected here.**

➤ **What survives is the more interesting finding: Redburn's PT cut to $130 is built on **50x the CONSENSUS 2027 EPS of $2.55** — not on a reduced estimate. Combined with Redburn being ABOVE consensus in 2026 (+2%/+3%) and 2027 (+3%/+6%) and only below in 2028 (−7%/−6%), **the Shopify downgrade contains no near-term estimate cut at all. It is a pure multiple/duration call.** Anyone reading the Neutral as an earnings warning has it backwards.**

### [[GOOG]] capex — three independent marks agree inside 4%
**Citi 2027E $321.6bn vs Capstone house $310bn (+3.7%) vs BBG $308.7bn (+4.2%). 2026E: Citi $204.5bn vs BBG $201.2bn (+1.6%), house $183bn.** ➤ **Tight three-way agreement on the largest capex line in the complex. Corroborated qualitatively by Wells Fargo's independent read that *"only Google will deliver more than 7GW of capacity in '27, powered by TPU capacity"* — two different methods (spend and capacity), same conclusion: Google is the 2027 capacity leader. No action.**

### [[META]] capex 2026 (Citi) and [[AMZN]] — within tolerance / basis-explained
- **META 2026E: Citi $143.7bn vs BBG $150.6bn (−4.6%); 2027E Citi $205.3bn vs BBG $214.6bn (−4.3%). CONFIRMS — Citi is essentially the consensus view, which is precisely why it is the right counterparty to Redburn in the DIVERGES table above.**
- **AMZN: Citi 2027E $244.1bn vs BBG $283.9bn (−14.0%); 2026E $167.2bn vs $214.2bn (−21.9%). ⚠️ NOT A DIVERGENCE — Citi's row is explicitly labelled "Infrastructure (mostly AWS)", a SUBSET of Amazon's total capex (which includes fulfilment and logistics). Being below the BBG total-capex line is the expected result. Screened out.**

### [[MU]] / [[STX]] / [[WDC]] — FY-vs-CY offsets, not disagreements
**Bernstein labels are fiscal years for all three (MU ends ~Aug/Sep; STX and WDC end ~Jun/Jul, and Bernstein states "base year is 2026"), while BBG here is calendarised. In a steeply rising cycle an FY that leads the CY reads higher, which is exactly the pattern observed:**

| Name | Bernstein 2027E EPS | BBG CY2027 EPS | Gap | Read |
|---|--:|--:|--:|---|
| [[MU]] | $158.99 | $163.76 | −2.9% | ✅ **CONFIRMS** (2026 gap of −30% is the FY/CY offset) |
| [[STX]] | $64.40 | $45.51 | +41.5% | ⚠️ FY/CY offset — **not logged as alpha** |
| [[WDC]] | $36.58 | $26.06 | +40.4% | ⚠️ FY/CY offset — **not logged as alpha** |

⚠️ **STX/WDC are flagged rather than dismissed: a ~40% gap is large enough that it MIGHT contain a genuine above-consensus view on top of the calendar offset. Resolving it needs Bernstein's FY-labelled BBG comparables (`BEST_FPERIOD_OVERRIDE` on the fiscal basis), which requires a live Terminal. **Carried forward as an open item for `/wiki-consensus`.** Recorded here deliberately: per this wiki's own history, calling a scaling error before checking the period basis has produced false rejections twice.**

### Cross-house PT spreads on the memory complex (same week, both houses live)
| Name | Bernstein (08-28) | Wells Fargo (08-21) | Spread |
|---|--:|--:|--:|
| [[MU]] | O, $1,300 | OW, **$1,525** | WF **+17%** above |
| [[STX]] | O, **$1,350** | OW, $1,180 | Bernstein **+14%** above |
| [[WDC]] | O, **$770** | OW, $730 | +5% — **tightest agreement** |
| [[SNDK]] | O, **$3,000** | **EW**, $1,550 | **+94% — see DIVERGES #4** |
➤ **Note the pattern: the two houses agree on direction everywhere except SanDisk, and the disagreement widens monotonically with NAND exposure — WDC (HDD) 5% apart, STX (HDD) 14%, MU (mixed) 17%, SNDK (pure NAND) 94%. The disagreement IS the NAND through-cycle-margin debate.**

---

## Qualitative items NOT reconciled (no quantitative claim to test)

- **Bernstein's NVHBM value-migration call ([[NVDA]]/[[TSM]] gain, memory suppliers lose base-die differentiation)** — structural, no number attached. 🔴 **But flagged as the most important un-modelled risk in the batch: every HBM forecast on this wiki prices BITS and ASP, and none price the base-die content being reassigned.**
- **[[SKHYNIX]] "Customer B" at 13.4% of 2Q26 revenue (larger than Customer A, widely believed to be NVIDIA)** — identity unresolved by the analyst; candidates GOOG/AVGO/AMD/AAPL. **A disclosed fact, not an estimate; nothing to reconcile until the identity is known.**
- **CPO engineering targets (>100Tb/s per node, <1pJ/bit, <10ns), the ~1.4x-vs-~3.0x-per-2-years bandwidth-wall ratio, HBF/HBC/zHBM/XBM/ZAM architectures** — roadmap items dated 2027-2029; no revenue line to test.
- **Nscale (private, pre-IPO), Theseus Infrastructure ([[ANTHROPIC]]), [[AVGO]]'s reported ~$100bn AI-financing debt raise** — private/unconfirmed; no consensus exists.
- **[[META]] API priced at 25% of [[ANTHROPIC]]/[[OPENAI]] offerings; CTM ~$40bn of '26 ad revenue (Mizuho expert)** — expert-call and press-derived, not company guidance.

---

## Open items carried forward

1. **Refresh BBG live and re-run this reconciliation** — tonight's column is the 08-28 on-disk snapshot (Terminal was logged out).
2. **Pull fiscal-basis BBG comparables for [[STX]] / [[WDC]] / [[SNDK]]** to convert the FY/CY offsets into a real above/below-consensus read.
3. **Confirm the line definition of Citi's "Calendarized Azure CAPEX" ([[MSFT]])** before treating the +23% gap as alpha.
4. **No CY2028 exists in BBG** — the entire [[META]] 2028 capex-cut debate is currently un-reconcilable against consensus. Needs an ad-hoc 3FY pull.
5. **[[SNDK]] Bernstein $3,000 vs Wells Fargo $1,550** — open five weeks; worth a dedicated bridge.

