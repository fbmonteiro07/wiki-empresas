# Reconciliation — 2026-08-29 (/run-inbox, 8 sources)

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines: (1) prior wiki comments, (2) the Capstone house model (`_data/house.json`), (3) BBG consensus. **DIVERGES = the alpha. CONFIRMS = no action.**_

⚠️ **BBG COLUMN PROVENANCE — READ THIS FIRST. A LIVE `bdp` PULL FAILED TONIGHT** (`ConnectionError: blpapi: could not start session` — Terminal not running / logged out, expected on a 23:40 unattended run). **The BBG column below is therefore the ON-DISK CONSENSUS SNAPSHOT `_data/estimates.json`, asof 2026-08-28 — i.e. genuine BBG consensus, ONE DAY STALE, not a live quote.** No web data has been substituted. Re-run `/wiki-consensus` with the Terminal up to refresh.

✅ **RESOLVED 2026-09-01 — `/wiki-consensus` ran with the Terminal UP.** The BBG column below has been re-placed against a **LIVE** pull: `estimates.json` **asof 2026-09-01**, **99/99 names, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 `carried_over` stamps, and 0 records byte-identical to the 08-28 vintage** (so no silent carry-overs). Additionally an **ad-hoc live `BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY` pull** of `BEST_SALES / BEST_EBIT / BEST_NET_INCOME / BEST_EPS / BEST_EPS_HI / BEST_CAPEX / BEST_CAPEX_LO / BEST_GROSS_MARGIN / BEST_TARGET_PRICE` was taken for **META, STX, WDC, SNDK, MU, KIOXIA, CRM, COHR** — that ad-hoc leg is what closes the CY2028 gap and the FY/CY offsets. **No web data was substituted at any point.**

⚠️ **TWO STANDING BASIS HAZARDS APPLY THROUGHOUT AND ARE HANDLED EXPLICITLY BELOW: (a) `estimates.json` CY sums embed PRE-PRINT consensus for already-reported quarters, so CY2026 understates — CY2027 is the cleaner comparison year; (b) THERE IS NO CY2028 IN BBG AT ALL, so every 2028 claim below is reconciled against the broker's own cited consensus only, and marked PENDING for BBG.** ✅ **HAZARD (b) IS NOW CLOSED: there is still no CY2028 *aggregate* in `estimates.json`, but META's fiscal year IS the calendar year, so the ad-hoc `3FY` override returns a genuine BBG **annual** FY/CY2028 consensus line. Every 2028 `PENDING` cell below is filled from it.** ⚠️ **AND HAZARD (a) TURNS OUT TO BE WORSE THAN STATED FOR CAPEX SPECIFICALLY — see the new basis block under item 1.**

---

## Where the new data DIVERGES

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

⚠️⚠️ **BASIS CORRECTION ADDED 2026-09-01, AND IT RE-SCALES EVERY ROW OF THE TABLE ABOVE. The $214.6bn is the `estimates.json` CY-SUM (four quarterly capex consensus marks added up). The live BBG **ANNUAL** consensus line for the same period (`BEST_CAPEX`, `2FY`) is **$197.1bn** — the CY sum runs **+8.9% hot**. Same wedge in 2026: CY sum $150.6bn vs annual line $139.4bn (**+8.1%**).** 🔴 **THE TIEBREAKER IS MANAGEMENT'S OWN GUIDE: Meta guided FY26 capex to **$130-145bn**. The annual line ($139.4bn) sits INSIDE that guide; the CY sum ($150.6bn) sits **ABOVE THE TOP END OF IT** — a consensus that breaches the company's own ceiling is the artifact, not the mark. Revenue and EPS do NOT show this wedge (2FY rev $304.85bn vs CY sum $304.81bn; 1FY rev $253.99bn vs CY sum $252.52bn), so this is a **capex-specific quarterly-panel artifact**, not the general CY-sum understatement.**

**Re-placed on the annual line, the gaps NARROW but the ordering and the direction are untouched:** Redburn 2027 **−27.9%** (was −33.7%) · **Capstone house −13.8%** (was −20.8%) · Wells Fargo −8.7% · Citi +4.1%. 2026: Redburn +1.6% (was −6.0%), house −6.0% (was −13.0%). ➤ **The house is still leaning Redburn's way and is still not the consensus view — but it is HALF as contrarian as the CY-sum basis made it look. Anyone sizing the house's edge off the −21% number is overstating it by ~7pp.**

⚠️ **NOT hand-patched: the `📊 Snapshot` block on [[META]] is machine-generated from the CY sums by `build_snapshot.py`, so it still shows $150.6bn / $214.6bn and would be clobbered on the next build. Logged as a tooling item under Open items instead.**

**Resolution mechanism (dated, falsifiable): Meta's own 2027 capex guide, expected with the Q4'26 print. Susan Li explicitly deferred the 2027 financing decision on the Q2 call, so an early signal could come sooner via a financing announcement.**

### 2. [[META]] 2028 — the capex-CUT call. ✅ **BBG RESOLVED 2026-09-01 (ad-hoc `3FY` = FY/CY2028): the capex gap WIDENS to −38.5%, and Redburn's 2028 EPS turns out to sit essentially AT the street high**

| Metric | Redburn 2028E | Redburn's cited cons. (Visible Alpha, 07-21) | Gap vs cited | **BBG annual `3FY` = FY/CY2028 (live 09-01)** | **Gap vs BBG** |
|---|--:|--:|--:|--:|--:|
| Capex | **$131.4bn** | $184.0bn | −28.6% | **$213.8bn** _(street-high spend $305.7bn)_ | 🔴🔴 **−38.5%** |
| EPS | **$59.0** | $40.33 | +46.3% | **$45.90** _(street high **$59.77**)_ | **+28.5%** — *98.7% of the street high* |
| Total revenue | $456.4bn | $354.9bn | +28.6% | **$360.8bn** | +26.5% |
| Income from operations | $196.4bn | $123.3bn | +59.3% | **$121.7bn** | **+61.4%** |
| "Other revenue" | **$68.3bn** | $7.6bn | **+801%** | **no BBG** — no segment line on the wrapper | **un-testable** |
| FCF | **$138.3bn** | $15.9bn | **+768%** | **no BBG** — no forward FCF consensus _(probed live: `BEST_FCF`, `BEST_CASH_FLOW`, `BEST_CFPS`, `BEST_FCF_PER_SH` all return null)_ | **un-testable** |

⚠️ **CORRECTION CARRIED FROM THE INGEST: this page previously recorded Redburn's 2028 capex as "~$100bn" (from the Rowan Joseph relay). The primary says $131.4bn. The −29% direction survives; the magnitude was overstated by ~30% in the relay. Retired to META's `## Changelog`.**

🔴🔴 **THE RESOLUTION — AND THE TWO GAPS MOVE IN OPPOSITE DIRECTIONS, WHICH CHANGES WHICH LEG OF THE THESIS IS THE CONTRARIAN ONE:**

1. **CAPEX: MORE contrarian than the note claims.** BBG's 2028 capex consensus is **$213.8bn**, i.e. **+16.2% above the $184.0bn Visible-Alpha number Redburn cited on 21-Jul**. His gap therefore widens from **−28.6% to −38.5%** — the same mechanism already documented for 2027 in item 1: **consensus kept marching up after he published, so the position got more contrarian without him changing a number.** Note the street-HIGH 2028 capex mark is **$305.7bn**: the Street's own 2028 Meta capex range runs $213.8bn median to $305.7bn high, against Redburn's $131.4bn. **That is a ~2.3x spread between the highest and lowest capex marks on one name in one year.**
2. **EPS: LESS contrarian than the note claims — and this is the more useful correction.** BBG 2028 EPS consensus is **$45.90**, **+13.8% above** the $40.33 Redburn cited, so his +46.3% gap shrinks to **+28.5%**. 🔴 **But the sharper fact is where he sits in the range: BBG's 2028 street-HIGH EPS is $59.77 and Redburn is at $59.0 — 98.7% of it. He is not merely above consensus on 2028 EPS; he is ON the top of the Street's range.** ➤ **Practical read: there is no headroom left in the EPS leg. If the SMB-LLM thesis is right, the re-rating has to come from consensus MIGRATING UP to him rather than from him being discovered — whereas the capex leg still has 38% of gap to close with nobody else near it. The capex call is the differentiated one; the EPS call is a range-edge call.**

⚠️ **THE TWO LOAD-BEARING LINES REMAIN UN-TESTABLE AGAINST CONSENSUS, AND THAT IS ITSELF THE FINDING: the +801% "other revenue" call and the +768% FCF call are exactly the two rows BBG carries no comparable for (no segment splits; no forward FCF/CFPS on the wrapper — probed live and confirmed null, not assumed). The single line where "the whole thesis lives" cannot be marked against the Street at all. Judge it on the GW-usage build (Fig 7) and the 45% SMB-LLM IRR, not on a consensus delta.**

➤ **Why the "other revenue" line is the real divergence rather than capex: Redburn is +801% vs consensus on a line consensus barely models ($7.6bn). The capex cut is a CONSEQUENCE of his SMB-LLM/AI-cloud revenue thesis, not an independent forecast. Judge the two separately — the capex call can be right for reasons unrelated to the revenue call, and vice versa.**

### 3. [[KIOXIA]] — Bernstein models 2027 EPS DOWN while consensus models it UP (the direction, not just the level)

| | Bernstein (28-Aug) | BBG CY2027 | Gap |
|---|--:|--:|--:|
| EPS 2026E | JPY 10,013 | JPY 8,116 | +23.4% |
| **EPS 2027E** | **JPY 9,657** | **JPY 13,768** | **−29.9%** |
| Direction y/y | **FALLING** | **RISING** | **OPPOSITE** |

🔴 **This is the cleanest DIVERGES in the memory complex tonight: Bernstein is the ONLY Underperform in its own memory coverage (Samsung, SK hynix, Micron, SanDisk, Seagate, WDC are all Outperform), PT JPY 40,000 vs a JPY 47,900 close = ~17% downside — and the mechanism is an EPS line that declines into 2027 while every other name in the same table compounds sharply.** ⚠️ **Period-basis caveat stated rather than ignored: Kioxia's fiscal year ends in March, so Bernstein's FY labels lead the BBG calendar year. That shifts the LEVELS but does not explain an inverted DIRECTION — which is why this is logged as a real divergence and not a basis artifact.**

✅🔴 **RESOLVED 2026-09-01 ON THE MATCHED FISCAL BASIS — THE PERIOD CAVEAT IS RETIRED AND THE DIVERGENCE IS MUCH WIDER THAN LOGGED.** The stated basis worry is settled from the wiki's own record: Bernstein labels Kioxia **FY26/27/28E EPS ¥10,013 / ¥9,657 / ¥3,896** on the Japanese convention (FY26 = Apr-26→Mar-27). Kioxia's last reported quarter is 2026-06-30, so BBG's `1FY` IS the year ending Mar-2027 — and the mapping is **proven by the base year itself: Bernstein FY26 ¥10,013 vs BBG `1FY` ¥10,264 = −2.4%.** Once the base ties, the later years tie too:

| Bernstein label | Bernstein EPS | BBG matched annual line | Gap |
|---|--:|--:|--:|
| FY26E (→Mar-27) | ¥10,013 | `1FY` **¥10,264** | −2.4% — *ties, so the basis is proven* |
| **FY27E (→Mar-28)** | **¥9,657** | `2FY` **¥14,053** | 🔴 **−31.3%** *(was logged −29.9% vs CY2027)* |
| **FY28E (→Mar-29)** | **¥3,896** | `3FY` **¥16,144** | 🔴🔴 **−75.9%** *(never placed before — no CY2028 existed)* |

🔴🔴 **THIS IS THE LARGEST QUANTIFIED HOUSE-VS-STREET GAP SURFACED BY THIS RUN, AND IT WAS INVISIBLE UNTIL THE FISCAL PULL: Bernstein has Kioxia EPS COLLAPSING 61% over two years (¥10,013 → ¥3,896) while BBG has it COMPOUNDING 57% (¥10,264 → ¥16,144). The direction inversion this report called "the cleanest DIVERGES tonight" is confirmed like-for-like, is not a level artifact, and WIDENS from −31% to −76% as you go out.**

⚠️ **Per this wiki's standing rule the −75.9% is flagged, NOT dismissed on plausibility: ¥3,896 is a deliberate through-cycle NAND-trough call, and the fact that the fiscal BASE year ties to within 2.4% is the evidence that the comparison is like-for-like rather than a period error.**

**The target price says the same thing more starkly: BBG consensus TP ¥114,476 against a ¥51,000 spot (+124% implied) versus Bernstein's ¥40,000 (−21.6%) — a −65% gap between one house's target and the Street's, on the only Underperform in its own memory coverage.** ⚠️ *Reported as pulled: a +124% consensus TP is an extreme mark and Japanese mid-cap TP dispersion is wide.*

**Corroborating, independent of the model: TrendFocus 2Q26 data via Wells Fargo has Kioxia's enterprise-SSD share at ~8% of EBs, DOWN from 10% in 1Q26, against [[MU]] 14.6% and [[SNDK]] ~19%. Share loss in the one pool that is growing.**

### 4. [[SNDK]] — two houses, ~2x apart on price target, on OPPOSITE ratings, seven days apart

| House | Date | Rating | PT | Price at note |
|---|---|---|--:|--:|
| **Bernstein** (Mark Li et al.) | 2026-08-28 | **Outperform** | **$3,000** | $1,484.95 |
| **Wells Fargo** (Rakers) | 2026-08-21 | **Equal Weight** | **$1,550** | $1,587.58 |

🔴 **A ~94% PT gap with opposite ratings on the same name in the same week is the widest single-name disagreement in memory on this wiki. Neither is stale. This is not reconcilable by basis — it is a genuine disagreement about NAND through-cycle earnings power, and it should be treated as an open position question rather than averaged.** ⚠️ **Note Bernstein's $3,000 is unchanged from its own 07-20 mark already on the SNDK page — the primer RE-STATES it, so this divergence has been open for five weeks, not one day.**

✅🔴 **RESOLVED 2026-09-01 — AND IT CORRECTS THE CHARACTERISATION ABOVE IN AN IMPORTANT WAY. THIS IS NOT AN EARNINGS-POWER DISAGREEMENT; IT IS A MULTIPLE DISAGREEMENT ON SHARED NUMBERS.** Bernstein's $3,000 is explicitly **11x FY28 EPS of $272** (base-case FY27/FY28 $243/$272 — already on the [[SNDK]] page). Placed on the matched BBG fiscal lines (SanDisk's last reported quarter is 2026-07-03, so `1FY` = FY2027):

| | Bernstein | BBG matched annual line | Gap |
|---|--:|--:|--:|
| FY27E EPS | $243 | `1FY` **$211.74** | +14.8% |
| **FY28E EPS** | **$272** | `2FY` **$259.46** | ✅ **+4.8%** — *essentially consensus* |
| FY29E direction | *Bernstein rev −11.9% y/y* | `3FY` EPS **$211.10** | *BBG also rolls over: **−18.6%** vs FY28* |

🔴 **Both houses are sitting on roughly the SAME FY28 earnings number (Bernstein just +4.8% over consensus), so the 94% PT gap is almost entirely MULTIPLE: ~11x (Bernstein) against ~6x (Wells Fargo's $1,550 on the same $259-272). The debate is not "what does SanDisk earn" — Bernstein, Wells Fargo and the Street broadly agree through FY28. The debate is WHAT MULTIPLE A PEAK NAND YEAR DESERVES, which is a different and much more tractable question than the one this report originally posed.**

➤ **And BBG hands over the reason the multiple is contested, which is the genuinely new fact: consensus itself has SNDK EPS ROLLING OVER 18.6% in FY29 ($259.46 → $211.10). The Street is NOT modelling a durable plateau — it is modelling a cycle PEAK in FY28. That independently corroborates what the [[SNDK]] page already flags about Bernstein's own model (revenue $56.8bn FY28 → $50.1bn FY29, −11.9%, i.e. quietly rejecting management's guided mid-to-high-teens growth for FY28-30).** 🔴 **So Bernstein's model AND consensus both reject the company's own growth guide. The position question, restated correctly: you are being asked to pay 11x for a year the Street thinks is the top.**

**Consensus TP lands almost exactly between the two houses: BBG $2,259.03 against a $1,557.51 spot, versus Bernstein $3,000 (+32.8% over the consensus TP) and Wells Fargo $1,550 (−31.4%). The midpoint of the two houses is $2,275 — within 0.7% of the consensus target. The Street has split the difference rather than taken a side.**

### 5. [[MSFT]] — Citi's 2027 capex sits 23% ABOVE BBG (flagged, but basis is uncertain)

**Citi $252.9bn (2027E) vs BBG $205.2bn = +23.2%; 2026E Citi $174.1bn vs BBG $153.5bn = +13.4%.** ⚠️ **HELD AS A SOFT DIVERGENCE, NOT A HARD ONE: Citi's row is labelled "Calendarized Azure CAPEX," and it is not established whether that is a SUBSET of Microsoft total capex (which would make a +23% reading over BBG total impossible to interpret) or a full-company calendarisation. Until the line definition is confirmed, do not trade this gap. Contrast with the AMZN row below, where the same ambiguity resolves the other way.**

---

### 6. [[STX]] / [[WDC]] — ✅ **RESOLVED 2026-09-01, AND THE "~40% FY/CY OFFSET" TURNS OUT TO HAVE BEEN A MISLABELLED YEAR IN THIS REPORT. On the matched fiscal basis Bernstein is a uniform +14% to +18% above consensus on BOTH names — a real, modest edge that was previously logged as "not alpha"**

⚠️ **ROOT CAUSE FIRST, BECAUSE IT IS A PROCESS FINDING: the CONFIRMS section below logged "$64.40" and "$36.58" as *Bernstein 2027E EPS*. They are not. Bernstein's own 08-07 NDR note — already quoted verbatim on both wiki pages — states **STX: "21x FY28 EPS $64.40; FY27E $40.61"** and **WDC: "21x FY28 EPS $36.58; FY27E $23.39"**. So a **FY2028** number was placed against **BBG CY2027**. That double-counts the offset and is what manufactured the ~40% gap. The report was right to refuse to log it as alpha; it was wrong about why.**

**Both names have a ~3-July fiscal year end (`lrq` 2026-07-03, i.e. FY2026 is reported), so BBG `1FY` = FY2027 and `2FY` = FY2028. Placed correctly, using Bernstein's own labels:**

| Name | Bernstein label & EPS | BBG matched annual line | Gap |
|---|--:|--:|--:|
| [[STX]] | FY27E $40.61 | `1FY` **$35.72** | **+13.7%** |
| **[[STX]]** | **FY28E $64.40** | `2FY` **$55.67** | **+15.7%** |
| [[WDC]] | FY27E $23.39 | `1FY` **$19.81** | **+18.1%** |
| **[[WDC]]** | **FY28E $36.58** | `2FY` **$31.59** | **+15.8%** |

🔴 **THE FINDING: Bernstein is +13.7% to +18.1% above consensus on both HDD names across both forecast years — four independent marks clustered in a 4.4pp band. That uniformity is itself the evidence the basis is now right (a residual period error would show up as a wild, non-uniform gap like the +80%/+85% you get against `1FY`, or the ~+40% you get against CY2027). It is not a 40% call and it is not nothing: it is a consistent mid-teens above-Street HDD earnings view.**

➤ **AND IT CROSS-CHECKS CLEANLY AGAINST THE TARGET PRICES, WHICH IS WHY IT SHOULD BE TRUSTED: Bernstein's PTs are struck at 21x FY28. Its premium over the consensus TP is **+21.3% for STX** ($1,350 vs BBG $1,112.70) and **+17.8% for WDC** ($770 vs BBG $653.63) — within a few points of its EPS premium (+15.7% / +15.8%) at essentially the market multiple. **So on the HDD pair Bernstein is running an ESTIMATE call, not a multiple call, and its target prices are internally consistent with its own numbers.**

🔴🔴 **THE CROSS-NAME READ, AND IT IS THE MOST USEFUL THING TO FALL OUT OF THIS RUN: the SAME analyst team, in the SAME week, is running two OPPOSITE kinds of bet inside one memory/storage coverage — on the HDD names ([[STX]], [[WDC]]) it is ~+16% above the Street on numbers at a market multiple; on the NAND name ([[SNDK]], §4) it is ON the Street's numbers (+4.8% FY28) at ~11x versus Wells Fargo's ~6x. Bernstein's HDD conviction is in the earnings; its NAND conviction is entirely in the multiple. Those two bets fail for completely different reasons and should not be sized as one "Bernstein is bullish memory" position.**

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

### [[MU]] — confirms on EVERY available basis (and that is what retires the period caveat)
**Bernstein's MU "2027E $158.99" carries no verified period label — the [[MU]] page excludes it from like-for-like rankings for exactly that reason. The 09-01 fiscal pull makes the label question moot for THIS comparison, because all three candidate mappings agree:**

| Candidate basis | BBG line | Gap to Bernstein $158.99 |
|---|--:|--:|
| FY2027 (ending ~Sep-27) | `2FY` **$152.33** | +4.4% |
| CY2027 | CY sum **$165.19** | −3.8% |
| FY2028 (ending ~Sep-28) | `3FY` **$170.81** | −6.9% |

✅ **Every mapping lands inside ±7%, so the conclusion is BASIS-INVARIANT: Bernstein's MU number is a consensus number however you read the label. CONFIRMS, and unusually safely — no period assumption is doing any work.** ⚠️ *The MU page's standing exclusion of the $158.99 mark from ranked comparisons still stands and should not be lifted: it is justified for RANKING (where a 7pp spread matters), just not needed to reach a confirm/diverge verdict here.* ⚠️ *Note the CY2027 mark drifted $163.76 (08-28) → $165.19 (09-01) over the refresh.*

### [[STX]] / [[WDC]] — ❌ **MOVED OUT OF CONFIRMS 2026-09-01 → see [Where the new data DIVERGES §6](#6-stx--wdc)**
**These two were parked here as "FY/CY offset — not logged as alpha." The 09-01 fiscal pull shows the numbers had been mislabelled ($64.40 and $36.58 are Bernstein's **FY28E**, not 2027E), and once matched correctly Bernstein is a uniform **+13.7% to +18.1%** above consensus on both names across both years. That is a real divergence, so the finding has been promoted to §6 of the DIVERGES section rather than left as a dismissed artifact here. The retired rows are preserved for the record:**

| Name | logged as "Bernstein 2027E EPS" | logged vs BBG CY2027 | logged gap | retired because |
|---|--:|--:|--:|---|
| [[STX]] | $64.40 | $45.51 | +41.5% | $64.40 is **FY28E**; matched gap is **+15.7%** |
| [[WDC]] | $36.58 | $26.06 | +40.4% | $36.58 is **FY28E**; matched gap is **+15.8%** |

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

_Status updated 2026-09-01 by `/wiki-consensus`._

1. ✅ **DONE — Refresh BBG live and re-run this reconciliation.** Live pull 2026-09-01, 99/99 names, and every finding above re-placed against it.
2. ✅ **DONE — fiscal-basis BBG comparables for [[STX]] / [[WDC]] / [[SNDK]].** Result was not the expected one: STX/WDC were mislabelled in this very report and are a real +14-18% edge (⇒ new §6); SNDK's 94% PT gap turned out to be a MULTIPLE disagreement on shared numbers (⇒ §4).
3. ⏳ **STILL OPEN — confirm the line definition of Citi's "Calendarized Azure CAPEX" ([[MSFT]])** before treating the +23% gap as alpha. **Not a BBG question** — it needs the Citi workbook's own row definition, so `/wiki-consensus` cannot close it. Carried to the next `/run-inbox`.
4. ✅ **DONE — [[META]] 2028.** No CY2028 aggregate exists, but META's FY = CY, so an ad-hoc `3FY` override returns a genuine annual 2028 consensus line. All five `PENDING` cells filled (⇒ §2). The capex gap widened to −38.5%; the EPS gap narrowed to +28.5% and Redburn sits at 98.7% of the street high.
5. ✅ **RESOLVED — [[SNDK]] Bernstein $3,000 vs Wells Fargo $1,550.** The bridge is short because the estimates barely differ: both houses are within ~5-15% of consensus FY28 EPS, so the entire 94% PT gap is multiple (~11x vs ~6x) on a year the Street itself models as the cycle peak (consensus FY29 EPS −18.6%). ⇒ §4.
6. 🔧 **NEW — TOOLING: `build_snapshot.py` renders CAPEX from the `estimates.json` CY SUM, which runs ~8-9% hot versus the BBG ANNUAL consensus line and, for [[META]] FY26, breaches management's own $130-145bn guide ceiling ($150.6bn vs $139.4bn).** Revenue and EPS do not show the wedge. Every `📊 Snapshot` capex figure on every page carries this bias, and so does any divergence measured off it (see §1). **Fix candidate: prefer `BEST_CAPEX` on the `1FY`/`2FY` override for calendar-FY companies, or label the snapshot capex row as a quarterly-sum basis.** Not patched by hand — the block is machine-generated.
7. 🔴 **NEW — [[KIOXIA]]'s FY28 gap (−75.9%, §3) has never been on the page**, because no CY2028 line existed to place it against. It is now the widest quantified house-vs-Street gap in the reconciliation backlog and should be surfaced to [[KIOXIA]] and to the edge tracker on the next ingest.

---

_BBG column resolved 2026-09-01 — `estimates.json` asof **2026-09-01** (99/99 live, 0 FAIL lines, 0 `error` keys, 0 null prices, 0 `carried_over` stamps, **0 records byte-identical to the 08-28 vintage** so no silent carry-overs), plus an ad-hoc live `BEST_FPERIOD_OVERRIDE=1FY/2FY/3FY` pull for **META, STX, WDC, SNDK, MU, KIOXIA, CRM, COHR**. **All five `PENDING` cells in §2 are filled** — they were the only literal `PENDING` table cells left anywhere in the 45-file reconciliation backlog (verified by scanning table cells, not prose, and not by trusting the prior run's summary line)._

_**Where the rows landed:** §1 [[META]] 2027 capex — **stays DIVERGES**, magnitude re-scaled on the annual line (house −13.8% not −20.8%). §2 [[META]] 2028 — **stays DIVERGES**, capex gap WIDENS −28.6% → −38.5%, EPS gap NARROWS +46.3% → +28.5% at 98.7% of the street high; "other revenue" and FCF are **un-testable** (no BBG segment or forward-FCF line, probed and confirmed null). §3 [[KIOXIA]] — **stays DIVERGES, materially widened** (−31.3% FY27, −75.9% FY28) and its period caveat retired. §4 [[SNDK]] — **stays DIVERGES but re-characterised** from an earnings dispute to a multiple dispute. §6 [[STX]]/[[WDC]] — **PROMOTED CONFIRMS → DIVERGES** (+14-18%, after correcting a FY28-labelled-as-2027 error in this report). [[MU]] — **stays CONFIRMS**, now basis-invariant._

_Canonical header `## Where the new data DIVERGES` applied (was `## 🔴 DIVERGES — the alpha`) so `build_edge.py` parses the section. **No web data was substituted at any point.**_
