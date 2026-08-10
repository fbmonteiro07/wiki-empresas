# Reconciliation — 2026-07-30 (run-inbox, 23h)

_Variance pass on every NEW quantitative datapoint from tonight's inbox against three baselines: (1) prior wiki comments, (2) Capstone house models (`_wiki/_data/house.json`, asof 2026-07-30), (3) BBG consensus (live pull 2026-07-30, `E:\bloomberg_api`, `BEST_FPERIOD_OVERRIDE` 1FY/2FY). Sources: AMZN Q2'26 call transcript, Apple 8-K/FQ3'26 release, five MSFT research notes (WF/UBS/JPM/MS/DB), two MSFT IR callbacks (UBS/BofA), the WF MSFT model, and MS "Playing the AI Infrastructure Dip" (2026-07-27)._

**BBG status: LIVE.** No PENDING columns this run.

**BBG snapshot used throughout** (spot / consensus PT / 1FY / 2FY, $ unless noted):

| Ticker | Spot | Cons. PT | 1FY EPS | 2FY EPS | 1FY sales ($mn) | 2FY sales ($mn) | 1FY capex ($mn) | 2FY capex ($mn) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| MSFT (FY27/FY28) | 451.10 | 559.80 | 19.649 | 23.285 | 389,269 | 464,495 | 189,659 | 218,283 |
| AMZN (FY26/FY27) | 235.50 | 316.05 | 10.292 | 11.652 | 824,898 | 935,044 | 202,497 | 244,864 |
| AAPL (FY26/FY27) | 333.43 | 323.27 | 8.757 | 9.682 | 478,538 | 523,303 | 12,219 | 14,181 |
| NVDA (FYJan27/28) | 195.04 | 304.24 | 8.910 | 12.878 | 393,524 | 565,037 | 7,945 | 9,846 |
| AVGO (FYOct26/27) | 387.84 | 524.15 | 11.586 | 19.251 | 105,849 | 173,823 | 1,011 | 1,349 |
| MU (FYAug26/27) | 874.66 | 1,589.48 | 73.153 | 152.737 | 129,634 | 248,746 | 28,019 | 45,048 |
| META (FY26/FY27) | 539.03 | 768.91 | 35.927 | 39.639 | 253,703 | 303,328 | 136,721 | 187,230 |
| GOOGL (FY26/FY27) | 333.66 | 427.75 | 18.994 | 16.081 | 434,918 | 549,070 | 201,533 | 301,191 |
| TSM (ADR) | 403.31 | 548.60 | n/a¹ | n/a¹ | n/a¹ | n/a¹ | n/a¹ | n/a¹ |

¹ The `TSM US Equity` ADR line returns a **USD price and PT against TWD EPS/sales** (BEST_EPS 535.6, BEST_SALES 5,430,383). Mixed-currency — **not used**. Any TSM consensus comparison needs the `2330 TT Equity` local line; not pulled this run.

---

## Where the new data DIVERGES

### 1. ★ MSFT FY27 capex: BBG consensus is BELOW every apples-to-apples desk estimate, including the cash-basis ones

| Basis | Estimate | Source |
|---|--:|---|
| BBG consensus, FY27 (Jun-27) | **$189.7bn** | BBG `BEST_CAPEX` 1FY, live 2026-07-30 |
| Cash ceiling implied by FY27 FCF-positive | **≤ ~$215bn** | JPM · Schilsky, 2026-07-30 |
| Cash capex range | **$218-232bn** | Wells Fargo Exhibit 1, 2026-07-30 |
| Cash capex implied by FCF-positive vs $215bn OCF | **$200-210bn** | UBS callback, 2026-07-30 |
| Reported (post-reclassification) | **$205-215bn** | Rothschild/Redburn · Adley, 2026-07-30 |
| Old basis (incl. finance leases) | **$235-245bn** | Rothschild/Redburn · Adley, 2026-07-30 |
| Old basis (incl. finance leases) | **$250-260bn** | UBS callback, 2026-07-30 |

**The finding: consensus $189.7bn sits below the LOWEST desk estimate on any basis — 12% under JPM's cash ceiling, 13-18% under Wells Fargo's cash range, and 24-27% under the old-basis cluster.** Consensus looks anchored on the reported CY26 headline ($175-190bn) rather than on any FY27 build. Note BBG's FY28 capex ($218.3bn) is *below* Wells Fargo's FY27 range — the consensus capex curve is roughly one year behind the desks.

**Why it matters and what to do with it:** if the desks are right, consensus is carrying too little MSFT capex, therefore too little D&A (a downstream EPS risk that partly offsets the revenue upside), and — the bigger read — **the semis/supply-chain complex is being modelled off a hyperscaler capex number that the reclassification made artificially small.** This is the exact failure mode Rothschild named: "reported capex is becoming a WORSE proxy for silicon demand." Actionable: track cash PP&E and the finance/operating-lease split, not the headline. **Conviction: high** (six independent desk estimates, one consensus line, no basis ambiguity once labelled). **Materiality: high** (a $30-70bn gap on a single company's annual spend).

### 2. ★ MU: Morgan Stanley's bullish note carries a target 24% BELOW consensus, and its valuation EPS is 74% below the consensus FY27 number

- **MS PT $1,200** (30x "through-cycle earnings of $40") vs **BBG consensus PT $1,589.48** → **MS is 24.5% below the Street's average target on a note that reads unambiguously bullish** ("we like the memory names… the memory shortage will intensify in 2027 and again in 2028… no signs of shortages abating").
- The mechanism is the denominator: **MS values MU on $40 of through-cycle EPS, against BBG consensus of $73.15 (FY Aug-26) and $152.74 (FY Aug-27)** — i.e. MS's valuation earnings are **45% below the current fiscal year** and **74% below FY27 consensus**.
- **This is the whole memory debate reduced to one number: is ~$150 of FY27 EPS a level or a peak?** MS is explicitly underwriting the peak-and-normalise view in its target price while writing the shortage-intensifies view in its text. Prior wiki comments on [MU](../MU.md) carry the shortage thesis but not this valuation inconsistency.
- **Actionable:** any MU position sized off "MS is bullish" is mis-reading the note — MS's target implies +37% from spot ($874.66) while consensus implies +82%. **Conviction: high** (both numbers are printed in the note). **Materiality: high.**

### 3. ★ AAPL: the Capstone house model is ~16% above consensus on FY26 EPS, and the June-quarter actuals now make the gap arithmetically hard

| | House (Capstone) | BBG consensus | Gap |
|---|--:|--:|--:|
| FY26E revenue | $480bn | $478.5bn | +0.3% |
| **FY26E EPS** | **$10.12** | **$8.757** | **+15.6%** |
| FY27E revenue | $539bn | $523.3bn | +3.0% |
| **FY27E EPS** | **$11.11** | **$9.682** | **+14.8%** |

**The arithmetic that makes this urgent:** the 8-K filed tonight reports **nine-month FY26 diluted EPS of $6.88**. The house's $10.12 therefore requires **~$3.24 in the September quarter**; consensus $8.757 implies **~$1.88**. That is a **~1.7x gap on the stub quarter**, against a guide of revenue **+9-11% y/y** and **underlying gross margin ~46.5%** (47-48% reported including ~1pt of tariff refund) — the weakest GM guide of the cycle, with management attributing "more than 100% of" the June-quarter sequential decline to memory.

⚠️ **Basis caveat before anyone acts on this:** the house model's FY25 EPS of $8.35 also sits above what the filing's nine-month FY25 figure ($5.62) implies on a GAAP diluted run-rate, which suggests **the house table may be on an adjusted-EPS basis rather than GAAP diluted.** If so, part of the gap is definitional, not analytical. **The action is the same either way: the house AAPL model (dated `Modelo Apple Felipe 2Q26 - WIP.xlsm`, 2026-06-16) predates the memory guide and needs a re-cut with the basis stated on the page.** **Conviction: high on the need for a revision; medium on the size of the true gap until the basis is confirmed.** **Materiality: high** (AAPL is a house-modelled name and the number feeds [AAPL.md](../AAPL.md)'s Capstone estimates block).

### 4. ★ AMZN FY26 capex: consensus has not caught up to management's own raise

- **Management guided ~$220bn** of 2026 cash capex on tonight's call (up from ~$200bn, "the higher cost of memory pushing this number up").
- **BBG consensus 1FY capex: $202.5bn** — **8.1% below the company's own guide**, because the pull is same-day with the print.
- FY27: **consensus $244.9bn vs JPM's $290.7bn** already on [AMZN.md](../AMZN.md) — **JPM is 18.7% above consensus.**
- **Actionable but decaying:** the FY26 gap closes mechanically as estimates refresh over the next few days; the FY27 gap is the durable one. **Conviction: high. Materiality: medium** (direction is known, timing is the only edge).

### 5. ★ NVDA: the house model is ~20% above both consensus and Morgan Stanley

| 2027 (house CY27 ≈ BBG FY Jan-28) | House | BBG 2FY | MS ModelWare CY27 |
|---|--:|--:|--:|
| Revenue | $661bn | $565.0bn | — |
| EPS | $15.44 GAAP / $15.49 non-GAAP | $12.878 | $13.08 |

**House revenue +17% and house EPS +20% vs consensus; MS's $13.08 is essentially AT consensus (+1.6%).** So the house is the outlier, not MS. Note also the mild irony worth recording: **MS calls NVDA its Top Pick in semis with a $288 PT, which is 5.1% BELOW the consensus PT of $304.24** — a relative-value call, explicitly ("we understand that there is more leverage in other parts of the supply chain, but we now feel that this is the best value in the group"), not a numbers call.
**Cross-check that supports the house rather than undercutting it:** MS's own engineering assumption is **+250% exaFLOPs per generation for +60% more power** and **~140%/yr CAGR in compute sold 2025-28**; the house's GW-sold ladder (~9.2 in 2025 → ~16.0 in 2026E → ~24.8 in 2027E, +74%/+55%) is *slower* in GW than MS's compute CAGR, which is internally consistent (compute per GW rises). The house's revenue gap is therefore a price/mix call, not a volume call. **Conviction: medium. Materiality: high.**

### 6. AVGO: house 2027 EPS is 10% above consensus and 18% above the MS number in tonight's note

- **House 2027E EPS $21.07** vs **BBG 2FY (Oct-27) $19.251** (+9.5%) vs **MS 2027e ModelWare base $17.92** (house +17.6%).
- **MS PT $502 vs consensus PT $524.15** — again slightly *below* consensus despite the bullish text.
- The house's AI-semis ramp ($63bn 2026 → $132bn 2027 → $251bn 2028) is consistent with MS's "**AVGO should remain the majority TPU supplier over time, with ~80% share**" — the two agree on share and disagree on level. **Conviction: medium. Materiality: medium.**

### 7. META: house FY26 EPS is ~9% below consensus, and the capex bases do not line up

- **House 2026E EPS $32.72 vs BBG 1FY $35.927 (house −8.9%)**; house 2027E $38.24 vs BBG 2FY $39.639 (house −3.5%). The house is the *bearish* outlier here, opposite to its posture on AAPL/NVDA/AVGO.
- **Capex: house $131bn (2026) + $170bn (2027) = $301bn** vs **consensus $136.7bn + $187.2bn = $323.9bn** (house −7%). MS's "**$380bn+ of capex ('27+'28)**" is a *different pair of years* and cannot be compared directly — if FY27 lands at the consensus $187bn, MS's figure implies ~$193bn+ in FY28, which is a modest step-up and looks conservative against the trajectory. **Flagged as a base mismatch, not a divergence.**
- **MS PT $775 vs consensus PT $768.91 — in line (+0.8%).**

### 8. ⚠ GW BASE MISMATCHES — do not net these against each other

Per `_meta/assumptions.md`, never mix GW bases. Three different MS numbers for the same companies appeared in the same fortnight and they are **not** the same measure:

| Company | MS 2026-07-01 (on [AMZN.md](../AMZN.md)) | MS 2026-07-27 (tonight's note) | House (`house.json`) |
|---|---|---|---|
| GOOGL | ~9GW **IT capacity added in 2027** | 9GW **added '27**, 11GW **added '28**, **31GW total available '28** | ~4.6GW (2026E) → ~7.75GW (2027E), labelled "**GW (TPU/compute)**" |
| AMZN | ~5GW **added 2027** | **35GW total available '28** | — |
| META | ~3.5GW **added 2027** | **14GW / 21GW TOTAL by '27/'28**, from ~3.5GW **at YE25** | — |

**The META line is the trap: "~3.5GW" appears in one note as a 2027 annual ADD and in the other as the YE25 INSTALLED BASE.** Anyone reading the two notes together will double-count. GOOGL's house figure (~7.75GW 2027) is a TPU/compute measure and is not comparable to MS's 9GW IT-capacity add. **No conclusion drawn — this is a flag for whoever next touches the GW numbers.**

### 9. MSFT Azure FY27: Wells Fargo underwrites ~45% for a full year, against an IR comment that December could decelerate

- **WF model: Azure FY26 $106.5bn → FY27E $154.9bn (+45.4%) → FY28E $221.7bn (+43.1%).**
- Against it, from the UBS callback the same day: **IR "did point out that Azure growth could even decelerate sequentially in the December quarter,"** and UBS itself models December **flat at ~45%** "just because the sequential numbers get very, very large."
- **So WF's model has the September guide rate persisting for eight quarters, while the company declined to commit to it for one.** Not a contradiction of any published number — a difference in how much of the guide is extrapolated. No consensus Azure line exists in BBG to arbitrate. **Conviction: medium (this is a modelling-aggressiveness flag, not an error). Materiality: high** — Azure is ~40% of the MSFT FY28 revenue delta between the desks.

---

## CONFIRMS — no action

| Datapoint | New (tonight) | Baseline | Verdict |
|---|---|---|---|
| **MSFT FY27 EPS** | WF $19.58 · UBS $19.68 · JPM $19.40 · MS $19.67 | BBG 1FY **$19.649** | Sell-side cluster is consensus, within ±1.3%. The revisions (JPM $18.70→$19.40, UBS $19.26→$19.68, WF $19.46→$19.58) closed a gap *to* consensus rather than opening one. |
| **MSFT FY28 EPS** | WF $23.53 · UBS $23.17 · JPM $23.15 · MS $23.86 | BBG 2FY **$23.285** | Tight around consensus; MS the high at +2.5%. |
| **MSFT FY27 revenue** | WF $393.9bn · UBS $392.6bn · JPM $392.2bn | BBG 1FY **$389.3bn** | Street ~+0.9%. |
| **MSFT FY28 revenue** | WF $481.2bn · JPM $473.0bn · UBS $465.4bn | BBG 2FY **$464.5bn** | UBS on consensus; **WF +3.6% is the outlier high** — mild, logged not escalated. |
| **MSFT consensus PT** | WF $650 · MS $600 · JPM $550 · DB $550 · UBS $525 | BBG **$559.80** | Median of the five ($550) is on consensus. **WF $650 = +16% vs consensus (Street high on the page); UBS $525 = −6% (low).** Spot $451.10. |
| **MSFT OpenAI revenue** | $24bn of FY26, "~7% revenue customer" | FY26 revenue $331.8bn → 7.2% | Internally consistent; first-time disclosure, no prior mark to supersede. |
| **MSFT RPO** | BofA "+$51bn q/q to ~$680bn" | Page carries **$678bn, +84%** (10-K) | Confirms; BofA's is the rounded call figure. |
| **MSFT capacity** | +1GW, 31 DCs, 88 for the year | Already on [MSFT.md](../MSFT.md) from the call | Confirms — three sources now (call, UBS callback, BofA callback). |
| **AMZN PT** | MS $330 (07-27) | BBG **$316.05**; GS $335, JPM $330, Barclays $330, BofA $310 on page | Tight cluster around consensus; MS +4.4%. |
| **AMZN AWS margin** | Reported ~39.3-39.4%, **+650bps y/y / +520bps ex-derivative** | Page carried "39.4%, ~600bp above plan" | Confirms the level; **the +520bps clean figure is new and annotated on the page** (see the AMZN Changelog — no number was deleted). |
| **AAPL reported FQ3** | Rev $109.4bn, GM 50.1%, EPS $2.02, all segment/geo lines | Page (from the call + six desks, 21h pass) | Every figure ties to the 8-K. Clean confirmation of the earlier ingest. |
| **AAPL consensus PT** | MS $360 · BofA $380 · UBS $296 | BBG **$323.27** | Wide but centred; spot $333.43 is *above* consensus PT. |
| **GOOG FY27 EPS** | — | House **$16.20** vs BBG 2FY **$16.081** | House on consensus (+0.7%). |
| **GOOG FY27 capex** | — | House **$310bn** vs BBG 2FY **$301.2bn** | House +2.9%, in line. |
| **MU price direction** | MS: prices **+≥25% like-for-like 2Q→3Q**, "above our estimates and above 3rd-party estimates" | Page carries the shortage thesis broadly | Confirms direction; the divergence is in the *valuation*, not the pricing call (see DIVERGES #2). |
| **Memory demand mix** | Server share of DRAM 37% (2023) → 59% (2028e); enterprise SSD 18% → 65% of NAND | [hbm-memory](../themes/hbm-memory.md) | New granularity, same direction as the existing dossier. |

---

## Not reconcilable this run (recorded so nobody re-does the work)

- **TSM** — the ADR BBG line mixes USD price/PT with TWD EPS/sales. MS's PT is NT$2,988 on the local line (2330.TW). Needs a `2330 TT Equity` pull to compare against the house model (2027E EPS NT$143.5). **MS PT ÷ house 2027 EPS = 20.8x**, recorded as a standalone marker only.
- **SAMSUNG, SKHYNIX, ASML, ADVANTEST, MEDIATEK, BESI, IFX, SMIC** — no Capstone house models and no BBG pull for the local lines this run. New MS ratings/PTs (SAMSUNG OW KRW381,000; SKHYNIX OW KRW2,600,000; ASML OW 22% upside; ADVANTEST OW ¥36,000; TSM OW NT$2,988) are logged on the pages against **prior wiki comments only**. ⚠️ **ADVANTEST's ¥36,000 is priced as of 2026-07-24 — five days before the 07-29 beat-and-raise — so it is stale on the upside versus Bernstein's post-print ▲¥45,800.**
- **WMB, VST, TLN, CEG** — the MS entries are ways-to-play screen lines (rating + % upside), reconciled against prior wiki comments only; no house models exist.
- **ANTHROPIC, OPENAI** — private, no BBG/house by construction. Tonight's relevant items (AMZN and MSFT both building first-party models to sit below the frontier on cost; OpenAI at $24bn of MSFT FY26 revenue) are logged against prior wiki comments on the respective pages.

---

## Two items to carry into the next pass

1. **Re-cut the Capstone AAPL model and state its EPS basis on the page.** It is dated 2026-06-16, sits ~16% above consensus on FY26 EPS, and the September-quarter guide issued tonight (revenue +9-11%, underlying GM ~46.5%) makes the implied stub quarter hard to reach on any basis. See DIVERGES #3.
2. **Resolve the MSFT capex basis question in the consensus line itself.** Consensus FY27 capex of $189.7bn cannot be compared to desk numbers until BBG's contributors settle on reported-vs-old basis post-reclassification. Until they do, **do not use BBG MSFT capex as the denominator in any semis read-through** — use cash PP&E plus the finance/operating lease split. See DIVERGES #1.
