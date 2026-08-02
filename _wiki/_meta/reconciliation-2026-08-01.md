# Reconciliation — 2026-08-01

_Run: `/run-inbox` (scheduled, unattended). Sources reconciled: **KLA Corp Q4 FY26 earnings call (2026-07-28)** and **Teradyne Q2 CY26 earnings call (2026-07-29)**, both Bloomberg FINAL TRANSCRIPTs. ⚠️ **Recovery run** — both transcripts were archived unrouted on 07-31 and restored today, so every number below is being reconciled 3-4 days after the market saw it._

## Baseline availability

| Baseline | Status |
|---|---|
| **1. Prior wiki comments** | ✅ Available — used throughout. |
| **2. Capstone house models** | ⚠️ Partial. `_data/house.json` covers only 8 names (AAPL, AVGO, COHR, GOOG, LITE, META, NVDA, TSM) — **neither KLAC nor TER is in it**. TER has an EPS-only house block on its page from the peer model (`ASML_Peers_SemiCap_v16.xlsx`, 2026-06-15); **KLAC has no house model at all**. |
| **3. BBG consensus (live)** | 🔴 **PENDING — `bdp` raised `HTTP 503: Bloomberg connection test failed - please ensure you are logged in to Bloomberg Terminal`.** Log in to the Terminal / reconnect the Capstone VPN and re-run, or use `/wiki-consensus`. **No web data was substituted.** |
| **3b. BBG consensus (on-disk snapshot)** | ✅ Used as a labelled stand-in — `_wiki/_data/estimates.json`, **asof 2026-07-31**, i.e. *after* both prints. Good enough to place these numbers; **must be re-run live to confirm.** |

---

# DIVERGES (the alpha)

### ① 🔴 TER — the Capstone house model is not stale, it is broken, and it is the largest single gap in the run
| | |
|---|---|
| **New datapoint** | Management re-cut FY26 to **"50% to 52% of annual revenue" in H1**. On H1 actuals of $2.6B that implies **FY26 revenue ≈ $5.00-5.22B**. H1 non-GAAP EPS is **$5.02** (company-stated), with Q3 guided to $1.85-2.15. |
| **House model** | **2026E EPS $5.46 · 2027E $6.90** (Capstone peer model, 2026-06-15) — flagged "below consensus, more cautious on ATE". |
| **BBG (07-31)** | CY2026 EPS **$8.08** · CY2027 **$11.34**. Sum of BBG's own quarterly lines for CY26 = **$8.96**. |
| **Gap** | House is **-32% vs the BBG CY26 line, -39% vs sum-of-quarters, and -39% vs CY27.** |
| **Verdict** | ⚠️ **This is not an edge — it is a model that has been overtaken by events.** H1 actual EPS alone ($5.02) is **92% of the full-year house number** with two quarters and a $1.85-2.15 Q3 guide still to come. The house 2026E will be exceeded by roughly Q3's second week. **Action: the TER line in the peer model must be re-marked before it is used in any screen, comp table or edge calculation.** The page has carried a stale-model flag since 07-28; this run quantifies it. Until re-marked, **any "house vs consensus" edge shown for TER is an artefact.** |

### ② 🟠 KLAC — management softened "CY27 > CY26" to "≈ CY26", and nothing in the Street's numbers reflects it
| | |
|---|---|
| **New datapoint** | *"There's a consensus view out there… somewhere in and around the **$190 billion** range… more or less, you're in and around $190 billion or so, translates into a **mid-20 tech growth rate, which is similar to the growth rate of 2026**."* (Bren Higgins, Q4 FY26 call, 2026-07-28) |
| **Prior wiki** | **"CY2027 growth > CY2026"** — carried since the Q3 FY26 call (2026-04-29) and repeatedly cited as the differentiator (JPM/Sur: the only large-cap "to put a stake in the ground"). It appears in `Debate`, `Catalysts`, the management-evolution table and the semicap-wfe theme. |
| **BBG (07-31)** | CY2026 rev **$15,488M** → CY2027 **$19,825M** = **+28.0%**. |
| **Gap** | ⚠️ **Two readings, and honesty requires giving both.** Management used two figures in one sentence: *"mid-20"* and *"similar to 2026"*. CY26 KLA revenue growth is ~28% (Barclays · O'Malley, 2026-07-30). So **consensus at +28% matches the "similar to 2026" clause and sits ~3pts above the literal "mid-20" clause.** The consensus *level* is therefore defensible. |
| **Verdict** | 🟠 **The alpha is not in the level — it is in the derivative.** The Street is modelling CY27 as a continuation; the page (and the JPM framing) has been modelling it as an **acceleration**, on the strength of a management commitment that management has now quietly dropped. **Nobody reported this** — it is a Q&A answer, absent from every desk first-take on 07-28. **Action: strip the ">"-based acceleration language out of the CY27 bull case and re-test the multiple on ≈-in-line growth.** Done on the page today; the sell-side has not. |

### ③ 🟠 KLAC — consensus expands CY27 gross margin while management says the headwind runs *through* 2027
| | |
|---|---|
| **New datapoint** | The memory-component cost hit is *"somewhere around 100 basis points. **It's probably a little bit more than that. I think that likely continues as we move forward through 2027**"* — normalising to a tailwind only afterwards. Management would not commit to a December step-up (*"could be a little bit higher, too. So we'll just have to see"*). |
| **Prior wiki** | The page read the 62.5% Sept guide (vs the 62% Jefferies bogey) as evidence **the headwind was easing** — scored **✓ confirma** in the Sinal table. |
| **BBG (07-31)** | CY2026 GM **62.2%** → CY2027 **62.8%** = **+60bps expansion**. CY27 EPS $5.98 vs CY26 $4.35 = **+37.5%**, well ahead of +28% revenue. |
| **Gap** | For consensus to hold, KLA's 60-65% incremental gross margin on +28% revenue must **more than absorb a >100bps headwind management says persists all year**. Not impossible — but it is an assumption the call did not support, and management declined three separate invitations to endorse margin expansion. |
| **Size it honestly** | Holding CY27 GM flat at 62.2% instead of 62.8% costs ~$119M of gross profit on $19.8B → **≈ $0.08 of CY27 EPS, ~1.3%.** **Small.** The value here is directional, not P&L-material: it is one more piece of the same pattern (see ④). |
| **Verdict** | 🟠 Sinal row re-scored **✓ → ⚠ nuança** on the page. Low materiality on its own; **read it together with ④.** |

### ④ 🔴 KLAC — the pricing lever is confirmed absent, and the sector generalisation on the semicap-wfe theme was wrong
| | |
|---|---|
| **New datapoint** | Jefferies (Curtis) on the call: *"even ASML is talking about raising prices on EUV… it seems like **you're struggling to do that**. Is there something unique?"* Higgins: ***"it's pretty hard to go back to your customers after you've taken orders and start to change prices on those orders"*** — resets deferred to new-product introductions. Wallace offers only *"conversations about… how KLA will help to capture some of that value."* |
| **Prior wiki** | ⚠️ **The `semicap-wfe` theme carried a sector-level claim** — *"semicap pricing power is becoming increasingly apparent"* (UBS · Ruple, off the LRCX call) — as if it applied to the group. Separately, UBS (Arcuri, 2026-07-25) had called **KLAC specifically the least likely of the Big Three to pursue pricing.** |
| **Verdict** | 🔴 **UBS's name-specific call is now confirmed by management on tape, and the theme's sector generalisation is corrected.** The accurate statement is: **[[ASML]] and [[LRCX]] are monetising the cycle through price; [[KLAC]] is not, and says so.** This matters more than ③ on its own because it is *structural* — it removes the margin-offset mechanism the rest of the group has, in the same cycle where KLA's own input costs (memory) are inflating. **Combined effect of ②+③+④: the KLAC bear case migrates from "KLA lags the DRAM-heavy cycle" (a revisions call, still unproven) to "KLA is the one large-cap semicap without a pricing lever, growing ≈ in line with the group in CY27, at the highest multiple in the group" — a valuation call, now management-confirmed.** That is a more durable version of the UBS/Redburn argument than the page previously carried. |
| **Cross-read** | ✅ **Positive for [[ASML]]** — a competitor's management publicly declining the lever that Bernstein made ASML its 3Q26 Best Idea on, two days before the Best-Idea note. Logged on ASML.md. |

### ⑤ 🟠 TER — BBG's own FY-level line is stale against BBG's own quarterly lines
| | |
|---|---|
| **The arithmetic** | Q1 actual $1,282.5M + Q2 actual $1,329.0M + BBG Q3E $1,216.7M + BBG Q4E $1,202.5M = **$5,030.7M** and EPS $2.56 + $2.47 + $1.988 + $1.942 = **$8.96**. But the **BBG CY2026 aggregate line reads $4,851M / $8.08**. |
| **Gap** | The FY line is **-$179M (-3.6%) on revenue and -$0.88 (-9.8%) on EPS** versus the sum of its own quarterly consensus — the classic signature of a **staler contributor set at the annual level than at the quarterly level**, three days after the print. |
| **Why it matters operationally** | ⚠️ **The wiki's own derived artefacts read the FY line.** The `📊 Consensus snapshot` block on TER.md and the edge tracker both consume `estimates.json` CY2026/CY2027 — so **any house-vs-consensus or guide-vs-consensus comparison for TER right now is being run against a number ~10% light on EPS.** Compounds with ①. |
| **Verdict** | 🟠 **Action: re-run `fetch_estimates.py` for TER once the Terminal is back, before trusting the snapshot or the edge tracker on this name.** Note KLAC does *not* have this problem (sum-of-quarters $15,592M vs the CY line $15,488M — only -0.7%). |

### ⑥ 🟡 TER — the CPO 2027 number is guided *down*, against how the wiki was carrying the ramp
| | |
|---|---|
| **New datapoint** | CPO test is *"a $300 million to $700 million market by 2028"* — and for 2027 specifically, ***"probably aiming towards more of the low side… the low-end would be in the $200 million range. I don't think there is as much upside next year as there is upside in 2028."*** |
| **Prior wiki** | The `optical-cpo` theme and TER.md carried *"$300-700M mid-term TAM"* (UBS CPO call, 2026-05-04) with an H2-weighted ramp, and the theme's recent-signals blocks have been tracking accelerating CPO insertion activity (Chroma shipping insertion 3/4 from 3Q26, Hon's insertion-4 handlers in October). |
| **Gap** | The vendor is **guiding the near year to the bottom of the path** (~$100M 2026 → ~$200M 2027 → $300-700M 2028), with the 2028 outcome contingent on scale-out ramps succeeding *during* 2027. |
| **Verdict** | 🟡 **Not a thesis break — a phasing correction.** CPO is a 2028 story with a 2027 proving year, not a 2027 revenue story. Relevant to anyone underwriting CPO contribution in TER's or [[ADVANTEST]]'s CY27 numbers. ⚠️ Also logged: TER's warning that it and a customer had *entirely different definitions of insertion 2* — **which should discount every insertion-share percentage on the optical-cpo page**, including Chroma's ">50% insertion 3 / 100% insertion 4.0". |

### ⑦ 🟡 ADVANTEST vs TER — a direct, dated share contradiction, and one stale PT
| | |
|---|---|
| **New datapoint** | Advantest (07-28) guided to **gaining SOC share and losing memory share**. TER's CEO (07-29): *"**I agree with their commentary about memory**, but in terms of SOC, it's **probably going to be pretty flat, maybe a slight incremental gain for us**."* UBS's Arcuri computed TER total test share at **~37%, "up just a touch… basically flat."** |
| **Gap** | **Both cannot be gaining SOC share unless the donor is a smaller vendor.** Logged as an open contradiction rather than resolved. Settles with the FY2026 final ATE share data (~April 2027). |
| **Bonus — PT staleness** | ADVANTEST spot **¥32,500** (BBG, 07-31) vs wiki PTs: Bernstein **¥39,200** (07-20), MS OW **¥36,000**, **JEF Buy ¥30,000 (2026-06-03) — now BELOW spot.** ⚠️ The JEF mark is 2 months stale and no longer a Buy-consistent target; treat as un-refreshed. |

---

# CONFIRMS (no action)

| # | Item | New datapoint | Baseline | Result |
|---|---|---|---|---|
| 1 | **KLAC Sept guide vs Street** | Guide $4.0B / GM 62.5% / EPS $1.16 | BBG Q3-26E **$4,022M / 62.35% / $1.158** | ✅ **Consensus is sitting exactly on the guide.** No revision gap — consistent with the Barclays "buyside is already there" read that explains the -7/-9% reaction. |
| 2 | **KLAC 2H/1H shape** | *"2H CY26 growth for KLA over 1H to be approximately 20%"* | 1H CY26 actual $7,075M; BBG Sept+Dec = $4,022 + $4,495 = **$8,517M = +20.4%** | ✅ **Precise match.** The Street has modelled the shape correctly. |
| 3 | **KLAC Dec-quarter GM** | Declined to commit to a step-up: *"in this range, but it could be a little bit higher"* | BBG Q4-26E GM **62.45%** vs Q3E 62.35% — essentially flat | ✅ Consensus is not assuming a December step-up. Correctly conservative. |
| 4 | **KLAC CY27 WFE $190B** | Management-cited consensus **~$190B** | Wiki marks: **MS $191B** (2026-06-22) ✅ near-exact · BofA ~$200B (07-30) close · JEF $165bn (06-08) low · **UBS ~$145B (2025-12-22) far low but 7 months stale** | ✅ **$190B is the centre of gravity; MS is the closest published mark.** ⚠️ The UBS CY27 figure on the KLAC/semicap pages should be treated as superseded, not as a live divergence. |
| 5 | **KLAC backlog** | RPO *"about $12.5 billion"*, grown "pretty consistently" | BofA (07-30): *"backlog +59% y/y"* → implies ~$7.9B a year ago | ✅ Internally consistent. **And it refutes UBS's "systems backlog is back to normal" bear leg** — a book with 2H27 delivery dates and 18-24 month lead times on some products is not normalised. |
| 6 | **TER test intensity** | Test ÷ semi-capex **4% (2023) → 7% (2025) → 8% (1H26)**, settling **7-8%**; ATE TAM **≥$20B** on ~$250B WFE | BofA (Arya, 2026-07-30): *"test intensity sustaining at **7-8% of WFE**, implying a **$14bn+ ATE opportunity at $200bn WFE**"* | ✅ **Two independent derivations, same band** — one from the vendor's capex arithmetic, one from a sell-side model. Strongest structural corroboration in the run. ⚠️ But see the caveats note below. |
| 7 | **TER Q3 guide vs Street** | $1.2-1.3B (mid $1.25B) / EPS $1.85-2.15 (mid $2.00) / GM 58-59% | BBG Q3-26E **$1,216.7M / $1.988 / 58.49%** | ✅ EPS and GM on the guide mid; **revenue consensus $33M below the guide midpoint** — a small unclosed gap, consistent with ⑤'s staleness. |
| 8 | **TER FY26 H1 weighting** | Re-cut to **50-52% H1** | BBG quarterly lines imply H1 = **51.9%** of the sum-of-quarters | ✅ **Already consistent at the quarterly level** — the quarterly contributors have marked to the re-cut; only the FY aggregate has not (⑤). |
| 9 | **TER full-year GM** | *"right around 59% — just shy of our target earnings model"* | BBG CY2026 GM **58.5%** | ✅ In line, consensus a touch conservative. |
| 10 | **KLAC advanced packaging** | Raised to **~$1.1B CY26, +>70% y/y** (from a "high 50%" internal prior); AP market re-marked ~20% → mid-to-high-30s | Prior wiki mark: **~$1B, ~70% y/y** (Q3 FY26 call) | ✅ Raised ~10%; direction and magnitude consistent with the CoWoS/hybrid-bonding evidence on `cowos-packaging`. No consensus line exists at segment level. |
| 11 | **KLAC PT vs spot** | — | Spot **$182.82** (BBG 07-31) vs GS $230 / MS $274 / TD Cowen $260 / UBS $240 / Bernstein $197.50 | ✅ **The stock now trades below every published PT on the page (+8% to +50% implied).** ⚠️ Note Bernstein's $197.50 was set on 07-20 *below* the then-spot of $212.75 as a valuation-caution signal — **the stock has since come to the PT and passed it**, so that call has effectively played out. |

---

## ⚠️ Method flags carried out of this run

1. **BBG live is PENDING.** Everything above uses the 2026-07-31 on-disk snapshot. Re-run `py E:/.claude/scripts/fetch_estimates.py KLAC TER ADVANTEST` → `build_snapshot.py`, or `/wiki-consensus`, once the Terminal is logged in and the VPN is up. **Item ⑤ specifically needs a live re-pull.**
2. **Two different "test intensity" ratios are now in circulation and they are not interchangeable.** TER's is **test ÷ semi-CAPEX (7-8%)**; UBS's long-standing figure is **test ÷ semiconductor REVENUE (~1%)**. Both are on the wiki. Do not compare or blend them.
3. **TER's own downside caveat is missing from the sell-side framing of item 6.** Management allows the ratio *"could revert down to 6%, 7% or so"* in 2027 on the WFE→ATE lag (~1yr from WFE spend to wafer output, plus ~16-week tester lead times). BofA's "sustaining at 7-8%" does not carry it. **A 7% vs 8% ratio on a $250B WFE base is a $2.5B swing in ATE TAM.**
4. **KLAC's revenue-mix figures are on two different denominators.** Full-year CY26 foundry/logic given as *"low to mid-60s"* on a semiconductor-customers-only basis vs the **~82%/~18%** the page carries from the Q3 call. Management stated explicitly these are not the same base. Both kept on the page; **do not build a mix trend line across them.**
5. **No house model exists for KLAC**, so baseline 2 could not be run on the primary name of this ingest. Worth deciding whether the semicap peer model should carry it.
6. **TER customer names are sell-side inference, not disclosure.** The transcript names **no** customer — NVDA, Amazon "Project Vulcan" and Google/TPU are all analyst attributions. Labelled as such on the page today. Any model crediting a named-customer ramp is crediting an inference.
