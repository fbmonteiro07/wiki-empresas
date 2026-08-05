# Reconciliation — 2026-08-04

_Run: `/run-inbox` (scheduled, unattended). Four sources reconciled:_
1. **AMD Q2 2026 earnings call — Bloomberg LIVE TRANSCRIPT, 2026-08-04** (the PRIMARY source for a print that had already been ingested earlier the same day from desk notes).
2. **Barclays · Saket Kalia / Ethan Sneckenberger, "Cloudflare, Inc. — Traffic Continues to Inflect, We Wonder if 'The Check Is in the Mail' Given Volume and Rev. Lags; Latest 2025 Mkt Share Data", 2026-08-04** (earnings preview; completed 03-Aug 16:44 GMT, released 04-Aug 04:10 GMT).
3. **Bernstein QUICK TAKE · Gautam Chhugani / Mahika Sapra / Sanskar Chindalia / Harsh Misra, "AI Infra/miners: Texas data center audit to drive more MW scarcity", 2026-08-04.**
4. **Capstone internal research synthesis · Daniel Grozdea, "SPCX 2Q26 Earnings Preview — reports tonight 8/4 AMC (lockup, not the quarter)", 2026-08-04 13:08** — a PRE-print synthesis of ~3 weeks / 73 SPCX-tagged emails across MS, Bernstein, DB, Cantor, SIG, UBS, Citi, 22V, GS and FundaAI. **Not a Bernstein note** (the router mis-detected the broker).

_Source 4 arrived **before** the print it previews, and the print itself was already on `SPCX.md`. Handled under the relay rule — **the primary wins**; the relay was folded only as a **scored pre-print bar** plus two new covering houses. Nothing in the maiden-print block was altered._

---

## Baseline availability

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Available — used throughout. Every superseded value was moved to the relevant page's `## Changelog` during patching. Only **one** supersession occurred this run (see below); the other three sources were purely additive. |
| **2. Capstone house models** | 🔴 **Effectively unavailable — 10 of the 11 affected names have no house model.** `_data/house.json` covers **NVDA only** among today's names. **No house model for AMD, NET, MSFT, AMZN, CRWV, SPCX, DELL, SMCI, AKAM, FSLY.** ⚠️ AMD is the notable gap: it is the largest print in this run and one of the most-discussed names on the wiki, and there is no house number to place the guide against. |
| **3. BBG consensus (live re-pull)** | ✅ **RESOLVED 2026-08-05 via `/wiki-consensus`** (was 🔴 PENDING on `HTTP 503: Bloomberg connection test failed – please ensure you are logged in to Bloomberg Terminal` at ingest). Live pull `estimates.json` **asof 2026-08-05**, **97/97 names, 0 FAIL lines, 1 record byte-identical to the 08-04 vintage (SAMSUNG — re-pulled standalone and reproduced the same values live, so it is a genuine unchanged record, not a silent carry-over)**, plus an ad-hoc live `PX_LAST` / `BEST_TARGET_PRICE` / `EQY_REC_CONS` pull the same date for all 11 names carrying findings here. **No web data was substituted at any point.** |
| **3b. BBG consensus (on-disk snapshot)** | ✅ **Used as the consensus baseline.** `_data/estimates.json` **asof 2026-08-04** — i.e. a BBG pull dated the same day as every source, 97 names, quarterly (1FQ/2FQ) + CY2026/CY2027. This is genuine BBG consensus, not a substitute. |

### Action required — ✅ BOTH CLOSED 2026-08-05
1. ~~**No `BEST_TARGET_PRICE` this run.** `estimates.json` carries `px` but no consensus target, so **Barclays' NET PT $300 could not be placed against the consensus PT** — the single most useful missing placement (see DIVERGES ①). Re-run `/wiki-consensus` or an ad-hoc `bdp` pull for `NET US Equity`, `AMD US Equity`.~~ ✅ **DONE 2026-08-05** — live PT pull for all 11 names in the run (table below). **The NET placement inverted the finding's mechanism: Barclays is not the stale mark, it is the HIGH mark — the whole Street's average target sits ~10% BELOW spot.** See ①.
2. ~~**SPCX has NO record in `estimates.json`** (97 names; SPCX is not among them). Newly public — **add it to the fetch list.**~~ ✅ **DONE 2026-08-05** — SPCX tested live on the wrapper and **it is covered**: **39 analysts (30 buy / 7 hold / 2 sell), consensus PT $222.60 vs spot $115.81**. Added to `fetch_estimates.py` as batch 10 and fetched; `estimates.json` now carries **98 names** and `SPCX.md` has a consensus snapshot block for the first time. ⚠️ The **Visible Alpha** set inside source 4 remains the correct comparator for the ⑩ *pre-print* bar — BBG's Q2-26 is now a reported actual, not the bar the print was set against. What BBG newly supplies is a **forward** bar (Q3-26E) and a PT.

### ⚠️ Method flags applied
- **`estimates.json` CY2026 systematically understates beats** (known defect, root-caused 2026-08-01, still unfixed: CY sums embed pre-print consensus for already-reported quarters; **CY2027 is clean**). **No conclusion in this report rests on a CY2026 figure** — quarterly (1FQ/2FQ) and CY2027 only.
- **The 08-04 snapshot pre-dates the two prints in this run.** AMD's `lrq` is **2026-06-27** (Q2 actuals not yet folded into the consensus record) and SPCX is absent. For AMD this is exactly the right vintage for scoring a guide against the bar it was set to clear — but every AMD line below will move on the next pull. ✅ **That prediction was correct and is now measured, 2026-08-05: AMD is the ONLY name in this run whose estimates moved, and the direction of every revision supports the findings below rather than eroding them.** Both vintages are kept — 08-04 is the pre-print bar (the right basis for scoring the guide), 08-05 is the post-print mark.
- **`house.json` NVDA `opm` field reads 89% / 92% / 94% (2025/26/27).** Implausible as an operating margin; treated as a **parse artifact and not used**. Only the house `rev` and `eps` lines were relied on.
- **No bridge was built.** `estimates.json` carries no segment split, so AMD's consensus Instinct/Data-Center line cannot be isolated from total revenue. Rather than free-hand a bottoms-up 2027 bridge, the comparison below is stated on figures that exist. (Wiki rule: no un-disciplined models.)

---

## ✅ BBG live resolution — 2026-08-05

### Did the live pull change the consensus this report was built on? — **For one name, materially: AMD.**

Ten of the eleven names in this run are **estimate-for-estimate unchanged** between the 08-04 and 08-05 vintages (NET, NVDA, MSFT, AMZN, AKAM, FSLY, DELL identical to the decimal; CRWV and SMCI moved only on trivial EPS drift — CRWV CY26 −$0.04, SMCI CY26 $2.92→$2.86). **AMD moved on every line, inside 24 hours of the call**, and the direction of each revision supports the findings below:

| AMD consensus line | 08-04 (pre-print bar) | **08-05 (post-call)** | Δ | What it does to the finding |
|---|--:|--:|--:|---|
| Q3-26E revenue | $12.51bn | **$12.98bn** | **+3.7%** | ⑤ — the Street came **all the way up to the guide**: $13.0bn guide is now only **+0.15%** above consensus (was +3.9%). The revenue beat is fully absorbed. |
| Q3-26E EPS | $1.873 | **$1.932** | **+3.1%** | ⑤ — same: guide-implied ~$1.93 is now **−0.1%** vs consensus (was +3.0%). |
| **Q3-26E gross margin** | 56.242% | **56.143%** | **−10bps** | 🔴 **⑤ STRENGTHENS.** The Street moved revenue and EPS to the guide but **still will not come down to the ~56.0% GM guide** — consensus sits **+14bps above** it. GM is the one guided line the Street refuses to mark to management. |
| Q4-26E revenue | $15.71bn | **$16.11bn** | **+2.6%** | 🔴 **⑥ STRENGTHENS.** The implied sequential step off the $13.0bn guide **widened from +20.9% to +23.9% q/q** — the Street *raised* the least-supported number in the stack after a call that gave no Q4 figure. |
| Q4-26E gross margin | 55.709% | **55.513%** | **−20bps** | ⑤/⑥ — the consensus q/q GM step-down **widened from −53bps to −63bps**. The Street is modelling the Helios ramp as *more* margin-dilutive, not less. |
| **CY2027 revenue** | $78.75bn | **$85.72bn** | **+8.9%** | ★ **④ — the Su effect, measured.** |
| **CY2027 EPS** | $14.01 | **$15.23** | **+8.7%** | ★ **④ — see below.** |
| CY2027 EBIT | $26.28bn | **$29.05bn** | **+10.5%** | ④ — the revision is margin-accretive at the EBIT line even as GM falls, i.e. opex leverage. |
| CY2027 capex | $1.62bn | **$2.57bn** | **+59.1%** | New. Q4-26E capex also **$348m → $611m (+75%)**. The Street is funding the ramp it just underwrote. |
| Consensus PT | $574.48 | **$598.46** | **+4.2%** | 🔴 **The Street raised targets 4.2% while the stock fell 6.8% to $483.56.** Implied upside to the consensus target widened from **+10.7% to +23.6%**. |

**★ The single most important thing to come out of this resolution: item ④ is now evidenced by the tape of revisions, not just by reading the transcript.** The report's claim was that **sell-side consensus was the LOW anchor** and that Su's *"your data center AI number is probably too low"* was a deliberate nudge. **One day later the Street took CY2027 revenue up 8.9% and EPS up 8.7%.** ⚠️ **The magnitude gap is NOT closed** — the buy-side's ~150% DC growth versus a sell-side that was at +88% is not bridged by an 8.9% move at the total-revenue line, and `estimates.json` still carries no segment split, so the revised Instinct line **still cannot be isolated**. **④ therefore stays in DIVERGES: direction confirmed, magnitude gap open.** The honest read is that the Street began closing toward management within a day and has further to go if management's framing is right.

## BBG consensus pull — live 2026-08-05 (the PT column this run never had)

_Live `BEST_TARGET_PRICE` (consensus target), `PX_LAST` and `EQY_REC_CONS` (1–5, 5 = all buys), all 2026-08-05. Prices are minutes apart from the `estimates.json` spots above, so they differ in the last decimal. 📌 = live book position (`book.json`, seeded 2026-07-01)._

| Name | spot | BBG consensus PT | implied upside | cons rating | Wiki broker marks placed against it |
|---|--:|--:|--:|--:|---|
| **SPCX** | 115.81 | **222.60** | **+92.2%** | 4.41 | 🆕 **First BBG mark this wiki has ever carried for SPCX** (39 analysts: 30 buy / 7 hold / 2 sell). The consensus target implies the stock **nearly doubles** — an extraordinary spread for a 39-covered name, and it sits *with* the ⑩ framing that the stock is being set by lockup mechanics rather than the print. Wiki marks: **Cantor OW $246 (+10.5% above consensus PT)**, **SIG Neutral no PT**. |
| **CRWV** | 92.37 | **138.59** | **+50.0%** | 4.19 | Bernstein carries no CRWV rating in the ⑬ note; its standing **Underperform / PT $67 (Rezaei)** is **−27.5% BELOW spot and −51.7% below the consensus target** — the widest single broker-vs-Street gap in this run. |
| **NVDA** | 219.75 | **304.44** | **+38.5%** | 4.88 | 📌long. Highest rating in the set (4.88 = near-unanimous buy). Consensus target implies a far larger move than consensus EPS growth — the same tension flagged on 08-03 ⑧. |
| **AKAM** | 122.22 | **159.95** | **+30.9%** | 4.12 | ⑪ — the Street models **both** −160bps of CDN share loss **and** +31% upside, which is only coherent on the security/compute mix argument already on the page. **CONFIRMS.** |
| **SMCI** | 30.90 | **39.33** | **+27.3%** | **3.26** | ⑭ — **weakest rating in the set by a wide margin** (3.26 ≈ hold). Consistent with the channel-disintermediation risk landing harder on SMCI. |
| **AMD** | 484.25 | **598.46** | **+23.6%** | 4.59 | Raised **+4.2%** post-call into a **−6.8%** stock (see the table above). |
| **AMZN** | 275.40 | **325.89** | **+18.3%** | **4.85** | 📌long. |
| **MSFT** | 490.64 | **563.65** | **+14.9%** | 4.84 | 📌long. ⑨ — capex consensus **unchanged** at $44.65bn / $46.65bn, so the "locked capacity one vintage early" credit stands untouched. |
| **DELL** | 467.02 | **500.52** | **+7.2%** | 4.32 | ⑭ — **lowest upside in the set.** The Street has already priced DELL close to target while still rating it a buy. |
| **FSLY** | 26.84 | **24.40** | **−9.1%** | 3.62 | ⑫ — consensus target is **BELOW spot** after a **+8.7% two-day move** ($24.95 → $27.13). The share-gain story is now more than priced. **CONFIRMS the immateriality call.** |
| **NET** | 296.45 | **267.03** | **−9.9%** | 4.32 | 🔴 **The finding in ① inverts — see ① below.** Barclays' $300 is **+12.3% ABOVE** the consensus target, not behind it. |

---

## Where the new data DIVERGES

_Summary of the open divergences after the 08-05 BBG resolution (detail in ①–⑧ below). Status = where the row landed once the live consensus was placed against it._

| Name | The new datapoint | Consensus mark (08-05) | Status | Read |
|---|---|---|---|---|
| **NET** ① | Barclays OW PT $300 (04-Aug) | cons PT **$267.03**, spot $296.45 | 🔴 **DIVERGES — mechanism inverted** | Barclays is the **HIGH** mark, +12.3% above a Street target that sits ~10% **below** spot. The whole Street is behind the tape into an 08-06 print, not just Barclays. |
| **NET** ② | Barclays Q2 GM ~72.0% vs EBIT ~14.0% | GM **73.12%**, EBIT 13.60% — **unchanged** | 🔴 **DIVERGES — untouched, tests tomorrow** | −112bps below consensus on GM while +40bps above on EBIT. Falsifiable on the 08-06 print. |
| **NET** ③ | cRPO +31%, DBNR ~119% modelled | **not in `estimates.json`** (re-verified 08-05) | ⚪ **Coverage gap, not a divergence** | The two metrics that actually test the thesis still have no consensus comparator. |
| **AMD** ④ | Su: ~$30bn 2027 Instinct "probably too low" | CY27 rev **$85.72bn (+8.9% in a day)**, EPS **$15.23** | 🔴 **DIVERGES — direction CONFIRMED, magnitude open** | The Street began closing toward management within 24h. No segment split, so the +88% vs ~150% DC-growth gap is still unbridged. |
| **AMD** ⑤ | Q3 guide: rev $13.0bn / EPS ~$1.93 / GM ~56.0% | rev $12.98bn, EPS $1.932, **GM 56.14%** | 🔴 **DIVERGES — strengthens** | The Street marked revenue and EPS to the guide and **still sits above it on GM**. GM remains the only guided line consensus rejects. |
| **AMD** ⑥ | No Q4 figure given ("higher than" Q3) | Q4 rev **$16.11bn** = **+23.9% q/q** off the guide | 🔴 **DIVERGES — strengthens** | The Street *raised* the step it was already carrying on adjectives alone. Still the weakest link in the AMD stack. |
| **NVDA** ⑦ | IREN: NVDA ~$15mn/IT MW vs MSFT ~$10mn (+50%) | CY27 rev **$568.19bn / EPS $12.91 — unchanged** | 🟠 **Watch item (returns, not estimates)** | House stays **+16.3% rev / +19.6% EPS** above consensus. A cost datapoint on the leased-capacity leg, into a tightening MW market. |
| **Power** ⑧ | ERCOT "Batch Zero" paused; 474 GW requested | qualitative — no consensus line | 🟠 **Watch item** | Third political vector on power inside a week. Time-to-power lengthens for new builds while approved MW re-rate. |

### ① ★ NET — the Overweight has already been overtaken by the tape, two days before the print
| Mark | Value | Source |
|---|--:|---|
| Barclays PT | **$300.00** | Barclays · Kalia, 2026-08-04 |
| Barclays reference price | $278.98 (31-Jul-26) | same |
| Barclays stated upside | **+7.5%** | same |
| **BBG `px` asof 2026-08-04** | **$301.33** | `estimates.json` |
| **Implied upside at the current mark** | **−0.4%** | derived from the two figures above |

**The note was released 04-Aug 04:10 GMT off a 31-Jul reference price, and the stock closed above the target price on the day of release.** The Overweight now carries no implied upside. This is the rating-vs-PT tension the reconciliation step exists to catch, and it is **live into an 08-06 print**. Two readings, and the history favours the first: Barclays' own PT path is **$235 (OW initiation, 02-Dec-2025) → $250 (10-Feb-2026) → $300 (13-Jul-2026)** — three raises in eight months — so **a fourth raise into or immediately after the print is the base case**, and the note's own logic ("could see upside as the lag starts to catch up") is written as a setup for exactly that. The alternative is that the rating is stale. ~~⚠️ **Cannot be placed against the consensus PT this run — BBG live is down.** That placement is the first thing to run when it returns.~~

✅ **08-05 PT placement (was PENDING) — and it inverts the mechanism of this finding:**

| Mark (live 2026-08-05) | Value | vs spot $296.45 |
|---|--:|--:|
| Barclays PT | **$300.00** | **+1.2%** |
| **BBG consensus PT** | **$267.03** | **−9.9%** |
| BBG consensus rating (`EQY_REC_CONS`) | **4.32 / 5** | ≈ buy |
| **Barclays vs the consensus target** | — | **+12.3% ABOVE** |

**The report read this as "Barclays' PT has been overtaken by the tape." The live pull shows something worse for the Street and better for Barclays: the ENTIRE consensus target is below spot.** Barclays at $300 is not the lagging mark — it is **+12.3% above** the Street's average target and one of the few targets still above the stock. The **whole sell-side carries a ~4.3/5 buy rating on a name trading ~11% through its own average price target**, into an 08-06 print. So the "stale rating" reading is the correct one, but it applies **Street-wide, not to Barclays** — and Barclays' three-raise path ($235 → $250 → $300) makes it the house most likely to be *first* rather than last to re-mark.

⚠️ **Two corrections to the original ① wording, both dated 2026-08-05, original preserved above:** (1) the stock has since traded **back below** $300 — NET is $296.45 (PT pull) / $297.41 (`estimates.json` 08-05) versus $301.33 on 08-04 — so Barclays' target now carries **+0.9–1.2%** implied upside rather than the −0.4% recorded at ingest. The substance is unchanged (an Overweight with ~1% of upside), but the specific "closed above the target price" claim was true on 08-04 and is **not** true on 08-05. (2) **NET's estimates did not move at all** between the two vintages — every quarterly and CY line is identical to the decimal, so this is a pure price/target story, not a revision story.

### ② NET — Barclays sits ~110bps BELOW consensus on gross margin while sitting ABOVE it on EBIT
| Metric (Q2 FY26E) | Barclays | BBG consensus | Variance |
|---|--:|--:|--:|
| Revenue | ~$665m | **$666.4m** | −0.2% (in line) |
| Gross margin | **~72.0%** | **73.12%** | **−112bps** |
| EBIT margin | **~14.0%** | 13.60% (= $90.6m / $666.4m) | **+40bps** |

**Both cannot be comfortably true unless Barclays models materially lighter opex than the Street.** The two-sidedness is the point: if Barclays is right on gross margin and the Street is right on opex, **consensus EBIT is too high**; if Barclays' opex assumption is the right one, its own Rule-of-50 path is safer than the GM line suggests. Barclays' framing pre-empts the bear read — the path to the 70-77% long-term range **"will not be linear"** because **Act 3 carries below-corporate-average gross margins and is growing as a mix**, and a GM downtick **should arrive with an uptick in growth or operating margin**. **That is a falsifiable claim: if 08-06 prints GM at/below ~72% WITHOUT a faster growth or better EBIT print, the mix argument fails on its first test.** Watch the 08-06 GM against **72.0% (Barclays) / 73.1% (consensus)**.

✅ **08-05 re-placement (was PENDING):** the live pull leaves **every NET consensus line unchanged to the decimal** — Q2-26E revenue **$666.4m**, GM **73.121%**, EBIT **$90.64m**, EPS **$0.271**; Q3-26E **$722.7m / 73.073% / $0.323**; CY2027 **$3,582.4m / $1.60**. **Nobody re-marked NET in the 48 hours before its print.** So the −112bps GM gap and the +40bps EBIT gap are both **exactly as stated**, and the 08-06 test is live against **72.0% (Barclays) / 73.121% (consensus)** with a **$666.4m** revenue bar. **Stays DIVERGES.**

### ③ NET — the revenue line is not the test; the two metrics that matter are not in consensus
Barclays models **~30% growth to ~$665m** against consensus **$666.4m** — a 0.2% gap, i.e. **the revenue print is non-falsifying either way**. The thesis rests on **cRPO growth (+31% modelled)** and **DBNR (118% in 1Q26 → ~119% modelled)**, **neither of which `estimates.json` carries**. ⚠️ **So the wiki cannot currently score the actual test of this thesis against consensus** — the cap-model lag argument ("timing rather than underlying demand") is only checkable on cRPO and DBNR. Flagged as a coverage gap in the consensus data, not a disagreement.

✅ **08-05 re-verified:** the fresh pull confirms the gap is structural, not a stale-file artifact — `estimates.json` carries **no cRPO and no DBNR field for any of the 98 names** (the fetch requests rev/ebit/ebitda/ni/eps/gm/capex only). **This is a data-coverage limitation of the wrapper's field set, not a divergence, and it will not resolve on a re-pull.** Closing it would require adding the two fields to `fetch_estimates.py` — logged as a tooling item, deliberately not done inside a consensus refresh. Consensus revenue is **unchanged at $666.4m** vs Barclays' ~$665m, so the revenue line remains non-falsifying either way.

### ④ ★ AMD — management put a floor above a NAMED 2027 number, and consensus is the low anchor
On the call, **C.J. Muse (Cantor) put ~$30bn of 2027 Instinct revenue** to management as implied by the data-center guide. **Lisa Su: *"what you're hearing from us is that your data center AI number is probably too low"*** — and separately, that "over 100%" should be read as **"well over 100%."**

| 2027 Data Center growth view | Mark | Source |
|---|--:|---|
| Sell-side consensus | **+88% y/y** | already on `AMD.md` (Jefferies, 2026-08-04) |
| Management language | **"well over" +100%** | Q2 call transcript, 2026-08-04 |
| Buy-side feedback | **~150%**, some **175-200%** | Jefferies desk, 2026-08-04 |

**Consensus is the LOW anchor of the three, and management spent the call nudging it upward without giving a number.** BBG CY2027 total revenue consensus is **$78.75bn** / EPS **$14.01**.

✅ **08-05 resolution (was PENDING) — the revision tape now evidences this call:**

| AMD CY2027 consensus | 08-04 (pre-print bar) | **08-05 (post-call)** | Δ |
|---|--:|--:|--:|
| Revenue | $78.75bn | **$85.72bn** | **+8.9%** |
| EPS | $14.01 | **$15.23** | **+8.7%** |
| EBIT | $26.28bn | **$29.05bn** | **+10.5%** |
| Consensus PT | $574.48 | **$598.46** | **+4.2%** |

**Within 24 hours of Su saying an analyst's ~$30bn 2027 Instinct figure was "probably too low," the Street took CY2027 revenue up 8.9% and EPS up 8.7% — while the stock fell 6.8%.** That is the cleanest possible corroboration of the report's reading that consensus was the low anchor and that the sell-off was about vague *language*, not a disappointing *number*. ⚠️ **The gap is narrowed, not closed, and this must not be overstated:** an 8.9% move at the **total-revenue** line does not bridge **+88% vs ~150%** at the **Instinct** line, and `estimates.json` still carries **no segment split**, so the revised data-center number **remains un-isolatable**. No bridge has been built here — that rule is unchanged. **Stays DIVERGES: direction confirmed, magnitude open.** ⚠️ **The Instinct line cannot be isolated — `estimates.json` has no segment split — so this is deliberately left as a range disagreement rather than a fabricated bridge.** The actionable form: **management has now explicitly rejected ~$30bn of 2027 Instinct as too low on the record**, which converts the buy-side's 150% from an aggressive assumption into the one closer to management's own framing. The reason the stock fell anyway is that the language was vague, not that the number was disappointing — and this exchange is the closest management came to a figure.

### ⑤ AMD — the Q3 guide beat consensus on revenue and EPS but MISSED it on gross margin
| Metric (Q3 FY26) | AMD guide | BBG 1FQ consensus | Variance |
|---|--:|--:|--:|
| Revenue (mid) | **$13.0bn** ±$300m | **$12.51bn** | **+3.9%** |
| Implied EPS | ~**$1.93** | **$1.873** | **+3.0%** |
| Gross margin | ~**56.0%** | **56.24%** | **−24bps** |
| Opex | **~$3.65bn** | not in consensus record | — |

**Gross margin is the only guided metric below consensus** — and it is guided **flat q/q on a +13% sequential revenue step**. That is now corroborated from three directions on the record: Jean Hu's **"data center AI… gross margin slightly below corporate average"**, Su's **Helios yield admission** ("expect overall yields to improve in the next few quarters — especially for a highly complex product"), and SemiAnalysis's 07-24 finding that AMD **cannot pass through the expected 2027 HBM price increase** because "most of AMD's volume goes to large buyers with real negotiating leverage." **The mix arithmetic that has capped this bull case all year is unchanged, and the fastest-growing line remains the least accretive.**

✅ **08-05 resolution (was PENDING) — this is the finding the live pull strengthened most:**

| Metric (Q3 FY26) | AMD guide | BBG 1FQ cons **08-04** | BBG 1FQ cons **08-05** | Guide vs the NEW consensus |
|---|--:|--:|--:|--:|
| Revenue (mid) | $13.0bn ±$300m | $12.51bn | **$12.98bn** | **+0.15%** (was +3.9%) |
| Implied EPS | ~$1.93 | $1.873 | **$1.932** | **−0.1%** (was +3.0%) |
| **Gross margin** | ~**56.0%** | 56.242% | **56.143%** | **−14bps** (was −24bps) |

**The Street marked revenue and EPS all the way to the guide inside one day — and did not come down to the gross-margin guide.** Consensus GM fell only 10bps (56.242% → 56.143%) and still sits **14bps above** what management actually guided. **After the guide, GM is the only line on which the Street is still refusing to take management's number** — which is exactly the shape of ⑤. The three corroborating sources (Hu's "slightly below corporate average," Su's Helios yield admission, SemiAnalysis's HBM pass-through finding) all point the same way, and the Street's own Q4 mark now agrees: it cut Q4 GM another 20bps to **55.513%**, widening the modelled q/q step-down from **−53bps to −63bps**. **Stays DIVERGES, strengthened.**

### ⑥ ⚠️ AMD — consensus Q4 embeds a very steep step that management never underwrote with a number
| Metric (Q4 FY26E) | BBG 2FQ consensus | Implied vs the Q3 guide |
|---|--:|--:|
| Revenue | **$15.71bn** | **+20.9% q/q** off $13.0bn |
| Gross margin | **55.71%** | **−53bps q/q** vs the ~56% Q3 guide |

**The Street is carrying a ~$2.7bn sequential revenue add with margin dilution, on the strength of adjectives.** Management said only that Q4 would be **"higher than"** Q3's strong double-digit growth, that **"the Helios ramp is just starting at the end of Q3 and it'll be much more substantial in Q4,"** and that Q1-27 would be **"a further step up."** No Q4 figure was given. ⚠️ **This is the least-supported number in the AMD consensus stack and the first place a Helios slip or a yield problem would surface.** Note the consensus GM step-down implicitly agrees with ⑤ — the Street is already modelling the ramp as margin-dilutive.

✅ **08-05 resolution (was PENDING) — the Street raised the number it never underwrote:**

| Metric (Q4 FY26E) | BBG 2FQ **08-04** | BBG 2FQ **08-05** | Δ |
|---|--:|--:|--:|
| Revenue | $15.71bn | **$16.11bn** | **+2.6%** |
| Implied step off the $13.0bn Q3 guide | +20.9% q/q | **+23.9% q/q** | **+3.0pp steeper** |
| EPS | $2.632 | **$2.662** | +1.1% |
| Gross margin | 55.709% | **55.513%** | **−20bps** |
| Capex | $348m | **$611m** | **+75.5%** |

**Management gave no Q4 figure — only "higher than" Q3, "much more substantial in Q4" on Helios, and "a further step up" in Q1-27 — and the Street responded by taking Q4 revenue UP 2.6%, to a ~$3.1bn sequential add.** The finding is unchanged in kind and worse in degree: **this remains the least-supported number in the AMD stack, and it is now larger.** The simultaneous 20bps GM cut means the Street is explicitly modelling the add as margin-dilutive, which is internally consistent with ⑤ but leaves both numbers resting on the same un-quantified Helios ramp. **Stays DIVERGES, strengthened.** ⚠️ The +75% Q4 capex revision is new and unexplained by anything on the call — logged, not interpreted.

### ⑦ ★ NVDA — paying up ~50% per megawatt versus Microsoft, at the same counterparty
Bernstein Exhibit 2, IREN revenue yield:

| Contract | Per **IT MW** | Per **gross MW** |
|---|--:|--:|
| Microsoft | **~$10mn** | ~$11mn |
| **NVIDIA** | **~$15mn** | ~$14mn |
| Enterprises | — | ~$11mn |
| **NVDA vs MSFT (IT MW basis)** | **+50%** | +27% |

⚠️ **Bases must not be mixed** — the per-IT-MW and per-gross-MW series are different denominators and are carried separately. Recent **enterprise cloud deals price GPU-hour rates 20-25% above prior guidance**, and Bernstein's logic is explicit: **"If MWs are scarce, it makes sense to earn more per MW."**

Placed against the only house model available this run:

| NVDA | House (`house.json`) | BBG CY2027 | House vs consensus |
|---|--:|--:|--:|
| 2027 revenue | **$661bn** | **$568.2bn** | **+16.3%** |
| 2027 EPS | **$15.44** | **$12.91** | **+19.6%** |

**The house is already the aggressive mark, and this is a cost datapoint on the leased-capacity leg of that thesis** — not a revenue variance but a **returns** variance. It does not change the model; it raises the cost of the megawatts the model's compute-leasing strategy consumes, at a moment when the supply of approved megawatts is being throttled (see ⑧). **Logged as a watch item, not an estimate change.**

✅ **08-05 resolution (was PENDING):** **NVDA consensus is unchanged to the decimal** — CY2027 revenue **$568.19bn**, EPS **$12.91**, GM 74.3%; Q2-26E $91.78bn / $2.08. So the house gaps stand **exactly** as stated: **+16.3% on revenue, +19.6% on EPS**. New from the live pull: consensus PT **$304.44** vs spot **$219.75** (**+38.5%**) on a **4.88/5** rating — the highest-conviction name in this run, and a consensus target implying a move far larger than consensus EPS growth supports (the same tension logged on 08-03 ⑧). **Unchanged: a returns/cost watch item on the leased-capacity leg, not an estimate revision.**

### ⑧ ⚠️ The scarcity mechanism behind ⑦ — a third political vector on power in one week
Texas Governor Abbott has directed the **PUCT and ERCOT to audit every data-center project in the interconnection process**; **ERCOT has PAUSED the "Batch Zero" review that was due to publish classification results on 2026-08-07.** The queue stands at **474 GW of interconnection REQUESTS with data centers ~90% of new requests** (⚠️ **requested-capacity basis — NOT comparable to energized, IT-load or facility GW**; cross-checks consistently against the **>2,000 GW FERC queue / 4-5 year wait** already on the power dossier, a different queue on the same basis). Bernstein: the audit **"throttles speculative data center pipeline and makes genuine sites with development history more valuable."**

**This is the third distinct political/regulatory vector logged on `themes/ai-datacenter-power.md` inside a week** — the NY moratorium (via Baker, 08-04), the Texas tax-abatement repeals (The Information, 08-02) and now the ERCOT audit (08-04). **Time-to-power is lengthening for new builds while already-approved MW re-rate** — which is the same fact pattern driving ⑦ and the CONFIRM in ⑨.

---

## ✅ CONFIRMS — no action

### ⑨ MSFT — the mirror image of ⑦, and a genuine confirm of timing
Microsoft's earlier IREN contract at **~$10mn per IT MW** now sits **~33% below the current clearing price (~$15mn under the NVDA contract)**. Against MSFT capex consensus of **$44.65bn (Q3-26E)** and **$46.6bn (Q4-26E)** — annualising above $180bn — **locking hosted capacity one vintage early is worth real money, and the wiki should credit it as such rather than treating the contract as a neutral fact.** No estimate change.

✅ **08-05 resolution (was PENDING):** **MSFT consensus unchanged to the decimal** — Q3-26E capex **$44.65bn**, Q4-26E capex **$46.65bn**, CY2027 capex $204.02bn, EPS $4.727 / $4.846. The credit stands on an untouched consensus base. Live PT **$563.65** vs spot **$490.64** (**+14.9%**), rating **4.84/5**. 📌long. **CONFIRMS — no action.**

### ⑩ SPCX — the pre-print bar, scored against the actuals already on the page
| Metric (Q2 26) | Visible Alpha consensus | MSe | **Actual** | Score |
|---|--:|--:|--:|---|
| Revenue | $6.9bn | $6.75bn | **$7.81bn** | **+13.2% vs consensus** |
| Adj. EBITDA | $2.1bn | $2.0bn | **$3.5bn** | **+66.7%** |
| Consumer Starlink subs | 12.1mn | 12.0mn | **12M** | −0.8% (in line) |
| Consumer monthly ARPU | $65.5 | $65.5 | **$66** | +0.8% (in line) |
| End-of-period compute | 1.4 GW | 1.4 GW | **1.4 GW** | on the nose |
| EBIT | −$1.6bn | −$1.7bn | _no actual on page_ | open |
| Adj. diluted EPS | −$0.32 | −$0.35 | _no actual on page_ | open |

**The shape is unambiguous: the two P&L lines blew out while every operating KPI landed exactly on the bar.** That **CONFIRMS** the page's standing conclusion — reached independently by MS ("largely at the mercy of technical forces") and DB ("neither of the two things that move the stock is the print") — that the quarter was never the driver, and it explains a **−5 to −7%** reaction to a large beat. Two new covering houses added this run: **Cantor OW $246** (whose EBITDA-beat call scored right) and **SIG Neutral, no PT**. ~~⚠️ **Not BBG-verifiable — SPCX has no `estimates.json` record.**~~

✅ **08-05 resolution (was PENDING) — SPCX now has BBG coverage in the wiki for the first time.** Tested live on the wrapper, added to `fetch_estimates.py` (batch 10) and fetched; `estimates.json` is now **98 names** and `SPCX.md` carries a consensus snapshot block.

| SPCX (BBG live 2026-08-05) | Value |
|---|--:|
| Spot | **$115.81** |
| **Consensus PT** | **$222.60** (**+92.2%**) |
| Analyst coverage | **39** — 30 buy / 7 hold / 2 sell (`EQY_REC_CONS` **4.41/5**) |
| Q3-26E revenue | **$12.40bn** (street high $16.02bn) |
| Q3-26E adj. EBITDA | **$6.32bn** (street high $9.11bn) |
| Q3-26E EPS / GM | **$0.152** / 58.9% |
| Q4-26E revenue / EBITDA | **$17.80bn** / **$10.23bn** |
| CY2027 revenue / EPS | **$91.54bn** / **$1.33** |

**Two things follow, and they cut in opposite directions.** (1) **The ⑩ CONFIRM is unaffected**: BBG's Q2-26 is now a *reported actual*, so the **Visible Alpha** set inside source 4 remains the correct — and only — comparator for the *pre-print bar* this item scores. Nothing in ⑩ changes. (2) **What is genuinely new is a forward bar**: Q3-26E **$12.40bn revenue / $6.32bn EBITDA**, i.e. the Street models **+59% q/q revenue** off the $7.81bn Q2 actual and **+81% q/q** on EBITDA, and a consensus target implying the stock **nearly doubles** on 39-analyst coverage. **That is a very aggressive forward bar sitting under a stock the page argues is being set by lockup mechanics rather than fundamentals** — the tension is worth carrying into the Q3 print.

⚠️ **Three cautions on this brand-new record, none of them resolvable inside a consensus refresh:** (a) **CY2026 is under the known pre-print CY defect** (`n_actual=2`) and must not be used; (b) the **CY2027 capex street-high of $303.8bn** (median $135.6bn) is **implausible on its face** and is treated as an outlier/units artifact — **not used anywhere above**; (c) the Q3/Q4 sequential ramp above is a **very** steep curve for a newly-public name and has not been validated against a second source. **The record is now present and attributed; it is not yet vetted.**

### ⑪ AKAM — the share loss is real and the consensus revenue line already reflects the right mechanism
**Akamai 21.9% of global CDN revenue in 2025, −160bps y/y** (after −230bps in 2024; series 25.7% → 24.6% → 25.8% → 23.5% → 21.9%), in a market that **grew +5.9% to $17.96bn** — so this is **share loss, not TAM loss**. Against BBG consensus **CY2026 $4.51bn → CY2027 $4.99bn (+10.7%)**: consensus still models growth, which is only coherent because the growth is coming from **security/compute, not delivery** — exactly the framing already on the page. **CONFIRMS; no estimate action.**

✅ **08-05 resolution (was PENDING):** **AKAM consensus unchanged to the decimal** — CY2026 **$4,507.4m** → CY2027 **$4,988.1m (+10.7%)**, EPS $6.71 → $7.22, GM 70.9% → 70.5%. New: PT **$159.95** vs spot **$122.22** (**+30.9%**), rating **4.12/5**. **The Street simultaneously carries −160bps of CDN share loss and +31% upside — coherent only on the security/compute mix argument, which is precisely the page's framing. CONFIRMS.**

### ⑫ FSLY — a real but immaterial share gain
**Fastly 3.2% in 2025, +25bps y/y** (series 2.4% → 2.7% → 2.9% → 2.9% → 3.2%; the 2023→2024 delta was **+0bps**, so 2025 is a modest inflection rather than a trend). BBG consensus **CY2026 $719.5m → CY2027 $798.4m (+11.0%)**. ⚠️ **+25bps on a $17.96bn market ≈ $45mn of relative positioning — immaterial against a ~$720mn revenue base, and this figure is OUR arithmetic on two source numbers, not Bernstein's or Barclays'** (it was deliberately kept off the page for that reason). **CONFIRMS; no estimate action.**

✅ **08-05 resolution (was PENDING):** **FSLY consensus unchanged to the decimal** — CY2026 **$719.55m** → CY2027 **$798.39m (+11.0%)**, EPS $0.28 → $0.41. But the **price** moved: **$24.95 (08-04) → $27.13 (08-05), +8.7% in two days**, and the live consensus PT is **$24.40 — BELOW spot (−9.1%)** on a **3.62/5** rating. **A +25bps share gain worth ~$45mn of relative positioning is now trading above the Street's own average target. That reinforces the immateriality call rather than undermining it. CONFIRMS.**

### ⑬ CRWV — contracted capacity insulated; the cost side is the watch item
**Core Scientific has already delivered 437 MW to CoreWeave and remains on track to 590 MW by early 2027, so CORZ execution timelines are NOT impacted by the Texas audit** — even though CORZ's 300 MW gross Pecos expansion is exposed. Against BBG **CY2027 revenue $25.05bn** and **Q2-26E capex $7.94bn**: no estimate change. ⚠️ The offsetting read is the same one as ⑦ — **CoreWeave leases all of its datacenters, so a rising $/MW clearing price is a rising cost of sourcing**, compounding the yield-on-cost pressure already on the page. Bernstein carries no CRWV rating in this note; its standing **Underperform / PT $67** (Rezaei) is untouched.

✅ **08-05 resolution (was PENDING):** **CRWV consensus effectively unchanged** — CY2027 revenue **$25,049.9m** (vs $25,049.5m on 08-04, i.e. flat), Q2-26E capex **$7,939.5m** identical, CY2026 EPS drifted −$0.04 to −$3.72. No estimate action, as stated. New and worth carrying: consensus PT **$138.59** vs spot **$92.37** (**+50.0%**) on a **4.19/5** rating — which places **Bernstein's standing Underperform / $67 at −27.5% below spot and −51.7% below the consensus target, the widest single broker-vs-Street gap in this run.** The cost-side watch item (CRWV leases all of its datacenters, so a rising $/MW clearing price is a rising sourcing cost) is unchanged. **CONFIRMS.**

### ⑭ DELL / SMCI — a denied rumour, correctly logged as a watch item only
The reported **$52bn / 13,000-rack GB300 order placed directly with Foxconn was called "fake news" by Musk**. Wells Fargo's Aaron Rakers' conditional read — **IF a buyer of that scale ordered racks direct from the ODM, that bypasses the OEM channel and is negative for DELL and SMCI** — survives the denial as a **structural channel-disintermediation question**, because the denial kills the specific order, not the mechanism. BBG consensus untested and unchanged: **DELL CY2027 $196.2bn / EPS $22.12**; **SMCI CY2027 $60.3bn / EPS $3.75**. **No estimate action.** It lands harder on SMCI, which does L7-L10 in-house.

✅ **08-05 resolution (was PENDING):** **both CY2027 lines unchanged to the decimal** — **DELL $196,194.7m / EPS $22.12**; **SMCI $60,300.0m / EPS $3.75** (SMCI's CY2026 EPS drifted $2.92 → $2.86, a −2.1% trim on the near year only). So "consensus untested and unchanged" is now literally verified. The live PT/rating pull **independently corroborates the "lands harder on SMCI" read**: **DELL PT $500.52 vs spot $467.02 = +7.2% (the lowest upside in the run) on a 4.32/5 buy rating**, versus **SMCI PT $39.33 vs spot $30.90 = +27.3% on a 3.26/5 rating — the weakest rating in the run by a wide margin.** The Street is more skeptical on SMCI's *quality* while pricing more upside into it. **CONFIRMS.**

### ⑮ AMD — segment profitability and cash flow: no consensus comparator, one new watch item
`estimates.json` carries no segment operating income and no FCF line, so the transcript's new disclosures **cannot be reconciled against BBG at all**. Against the **page**, however, one comparison is available and it is worth flagging:

| AMD cash flow | Q1 FY26 | Q2 FY26 | Direction |
|---|--:|--:|---|
| Operating cash flow | — | $2.4bn | — |
| **Free cash flow** | **$2.6bn (a record)** | **$1.6bn** | **−38% q/q** |
| Inventory | — | **~$8.5bn** (up q/q) | building |
| Cash + STI | $12.3bn | $13.1bn | +$0.8bn |

**FCF fell ~38% q/q on a +13% q/q revenue step, with inventory building** — management's only explanation was "to support strong data center demand," which is a demand-positive framing of a working-capital drag. New Q2 segment operating income, also with no consensus comparator: **Data Center $2.1bn / 31%**, **Client & Gaming $582mn / 15% (vs $767mn / 21% a year ago — down in both dollars and margin)**, **Embedded $386mn / 40% (vs $275mn / 33%)**. **Logged as a watch item ahead of the Q3 print, not as a divergence.**

✅ **08-05 resolution (was PENDING):** re-verified against the fresh pull — **the wrapper's field set still carries no segment operating income and no forward FCF line**, so the transcript's segment and cash-flow disclosures **remain unreconcilable against BBG on a re-pull**. Like ③, this is a **field-coverage limitation, not a divergence**, and it will not resolve by re-running the fetch. One adjacent number did move and is worth pairing with the inventory build: **consensus CY2027 capex went $1,617m → $2,572m (+59.1%)** and **Q4-26E capex $348m → $611m (+75.5%)** — the Street is now funding the ramp whose working-capital drag this item flags. **Stays a watch item ahead of the Q3 print.**

---

## Internal inconsistencies caught and logged rather than resolved
1. **AMD "same rack power" vs SemiAnalysis's rack model.** Management claims Helios delivers **"up to 15% more throughput at the SAME RACK POWER and up to 30% more tokens per dollar than the competition."** SemiAnalysis's 07-24 bottoms-up build has **MI455X at ~240kW server / ~257kW all-in vs GB300 NVL72 at ~142kW / ~159kW**, i.e. "MI455X lands even beyond VR NVL72 in power draw." **These cannot both be right.** The page already carried a BofA-vs-SemiAnalysis power disagreement; management's claim is now a **third, on-the-record** input to it. **Resolvable against real Helios deployment data in 2H26 — not adjudicated here.**
2. **RIOT capacity, inside a single Bernstein note:** "~1 GW energized operating capacity in Texas available for AI deployments (700 MW Rockdale + 400 MW Corsicana)" — which itself sums to 1.1 GW — against "**ready operational 1.7 GW capacity in Texas**" in the co-location-lease discussion, while Exhibit 1 shows 1,700 MW as *Texas concentration of the planned pipeline*. Both carried, flagged, neither chosen.
3. **SPCX Starship Flight 13 date:** the page dates it **2026-07-24**; source 4 says **July 26-27**. Logged for a primary check.
4. **`MSFT.md` has TWO `## Changelog` sections** (~line 231 and ~line 425) — a pre-existing structural defect, out of scope for this run. This run's entry went into the first. **Referred to `/wiki-lint`.**

## Method note on the one supersession this run
Only one thesis-drift move occurred across eleven files: **`AMD.md` stated in two places that the earnings transcript was "not on file"** (the `## Current state` lead and the Jefferies 08-04 intra-quarter row, which described itself as "the most complete call reconstruction available (transcript not on file)"). Both statements became false when source 1 landed and were corrected in place, with the prior wording preserved in the Changelog. ⚠️ **Materially: the transcript CONFIRMED the desk-note reconstruction line by line — not one figure was revised.** That is a quality datapoint about the desk notes this wiki relies on when transcripts are late.

## Top of the run
1. **★ NET (①) — an Overweight whose stock closed above its price target on the day the note was released, two days before the print.** ~~The most actionable single finding, and the PT-vs-consensus placement is still blocked on Bloomberg.~~ ✅ **Placed 2026-08-05, and the mechanism inverted: the CONSENSUS target ($267.03) is ~10% BELOW spot, and Barclays' $300 is the +12.3% HIGH mark.** Still the most actionable finding in the run — just Street-wide rather than Barclays-specific, into an 08-06 print.
2. **★ AMD (④) — Su told an analyst on the record that ~$30bn of 2027 Instinct is "probably too low,"** which makes the +88% sell-side consensus the low anchor against a buy-side already at ~150%. ✅ **Evidenced 2026-08-05: the Street took CY2027 revenue +8.9% and EPS +8.7% within 24 hours, while the stock fell 6.8%.** Direction confirmed; the segment-level magnitude gap is still open.
3. **★ NVDA (⑦) — paying ~50% more per IT MW than Microsoft did at the same counterparty**, against a house model already 16-20% above consensus, into a tightening approved-megawatt market (⑧). ✅ **Consensus unchanged 08-05 — the +16.3% / +19.6% house gaps stand exactly.**
4. **AMD (⑥) — consensus Q4 revenue implies +20.9% q/q on adjectives alone**, the weakest link in the AMD stack. ✅ **Now +23.9% q/q — the Street RAISED it 2.6% on 08-05.** The weakest link got weaker.
5. **AMD (⑤) — gross margin was the only guided metric below consensus**, now corroborated on the record from three independent directions. ✅ **Strengthened 08-05: the Street marked revenue and EPS to the guide and still sits 14bps ABOVE the GM guide.**
6. **SPCX (⑩) — a +13% revenue and +67% EBITDA beat with every KPI exactly in line, and the stock fell**, confirming the technicals-over-fundamentals framing both covering houses set in advance. ✅ **SPCX now has a BBG record (98 names): 39 analysts, consensus PT $222.60 vs $115.81 spot (+92.2%), and a Q3 bar of $12.40bn revenue / $6.32bn EBITDA.**

---

_BBG column resolved 2026-08-05 — `estimates.json` asof **2026-08-05** (98 names: 97 refreshed clean, 0 FAIL, + SPCX newly added), plus an ad-hoc live `PX_LAST` / `BEST_TARGET_PRICE` / `EQY_REC_CONS` pull the same date for all 11 names carrying findings. **No web data was substituted at any point.** Outcome: **no row moved between DIVERGES and CONFIRMS** — 8 DIVERGES / watch items and 7 CONFIRMS, exactly as written on 08-04. Two DIVERGES rows (⑤, ⑥) strengthened on the revision tape, one (④) gained direct corroboration, and one (①) kept its conclusion while inverting its mechanism. `build_snapshot.py`, `build_edge.py` and `build_wiki_html.py` re-run afterwards._
