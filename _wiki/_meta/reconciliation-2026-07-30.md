# Reconciliation — run-inbox 2026-07-30

_Variance pass on every NEW quantitative datapoint from the 4 sources routed this run, against three baselines: (1) prior wiki comments on the page, (2) Capstone house models (the `## Capstone estimates` / Snapshot block), (3) **live BBG consensus pulled 2026-07-30** via `E:\bloomberg_api` (`bdp`, `BEST_FPERIOD_OVERRIDE` 1FY/2FY/3FY). **BBG was UP — no PENDING column this run.**_

**Sources reconciled:** META Q2'26 earnings call (2026-07-29) · MSFT 4QFY26 earnings call (2026-07-29) · Aurelion Research/PhotonCap "A Conversation with Lumentum" (2026-07-29) · SemiAnalysis "The Wild Wild West Of LEGO Datacenters" (2026-07-29).

---

## ⚠️ READ THIS FIRST — three basis traps that would manufacture fake divergences

These are the reasons several "gaps" below are **not** gaps. Recorded explicitly because getting them wrong is the single easiest way to fabricate alpha out of an accounting artifact.

1. **Fiscal vs calendar.** MSFT (FY ends Jun), LITE (FY ends ~Jun/Jul), COHR (FY ends Jun), AVGO (FY ends Nov) and NVDA (FY ends late Jan) all have non-calendar years. The **stored page Snapshot blocks are CALENDARIZED (CY26E/CY27E)** while **my live pull is FISCAL (1FY/2FY/3FY)**. Comparing them directly is invalid. Where I compare, I calendarize the fiscal pair explicitly and say so.
2. **MSFT capex basis.** Three different numbers are all correct on their own basis: **$35.8B** = cash paid for PP&E (Q4); **$41.4B ≈ the stated $41B** = all-in incl. $5.6B finance leases (Q4); **~$42.7B** = a *computed plug* (FY26 all-in $140.6B less Q1–Q3 $97.9B). See the MSFT row — the residual is ~$1.3–1.7B, not a $6B disagreement.
3. **MSFT CY26 capex ~$190B → ~$175B is a DEFINITION change, not a cut** (finance→operating lease reclass on a 15→25-yr useful-life extension; "CY26 investment expectations remain unchanged"). **Every FY27 bogey on the page was struck on the OLD definition.** Any FY27 house-vs-street comparison on MSFT capex is currently basis-broken and must be restated before it means anything.

**Live BBG pull, 2026-07-30** (spot / mean PT; EPS·Sales·Capex by fiscal period, capex sign-flipped to positive spend):

| | Spot | Mean PT | EPS 1FY | EPS 2FY | EPS 3FY | Sales 1FY ($mn) | Capex 1FY ($mn) | Capex 2FY ($mn) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| MSFT | 390.54 | 559.39 | 19.56 | 23.11 | 27.30 | 387,379 | 188,291 | 210,048 |
| META | 585.61 | 772.71 | 36.97 | 40.90 | 48.84 | 253,449 | 136,400 | 182,959 |
| LITE | 602.35 | 1,127.51 | 8.16 | 18.41 | 29.57 | 3,000 | 314 | 427 |
| COHR | 222.05 | 395.25 | 5.45 | 8.47 | 12.56 | 7,062 | 853 | 995 |
| VRT | 223.04 | 349.53 | 6.59 | 8.63 | 11.04 | 13,985 | 492 | 554 |
| FLEX | 103.02 | 164.46 | 4.58 | 7.00 | 9.42 | 34,127 | 1,528 | 1,087 |
| NVT | 133.61 | 200.00 | 4.56 | 5.66 | 6.80 | 5,018 | 132 | 138 |
| PWR | 561.14 | 801.19 | 13.70 | 16.29 | 19.29 | 35,016 | 810 | 834 |
| ETN | 361.88 | 464.50 | 13.34 | 15.62 | 18.00 | 31,960 | 1,118 | 1,118 |
| NBIS | 148.22 | 268.55 | -2.54 | -3.03 | -1.96 | 3,350 | 23,103 | 28,966 |
| AMZN | 226.65 | 315.79 | 10.29 | 11.65 | 15.13 | 824,881 | 201,914 | 243,133 |
| NVDA | 190.01 | 304.24 | 8.91 | 12.88 | 15.91 | 393,524 | 7,945 | 9,846 |
| AVGO | 370.32 | 524.15 | 11.59 | 19.25 | 25.63 | 105,849 | 1,011 | 1,349 |
| AMD | 429.56 | 572.34 | 7.42 | 13.66 | 18.96 | 49,965 | 1,325 | 1,573 |

---

## Where the new data DIVERGES

### 🔄 BBG refresh layer — added by `/wiki-consensus` 2026-07-30 (estimates.json asof 2026-07-30, 97/97 names)

_Every quantitative row below re-placed against the **fresh CY-basis consensus** (`_data/estimates.json`: calendar-year sums on a uniform non-GAAP basis). **This is a different basis from the intra-day pull in the body of this report**, which used `BEST_FPERIOD_OVERRIDE` 1FY/2FY annual estimates — and on two rows the two bases point in **opposite directions**. Both are retained; neither is silently adopted. **Two corrections carried below, not netted out.**_

_⚠️ **The body's "Live BBG pull, 2026-07-30" spot column is PRE-PRINT.** Those `PX_LAST` values are the 2026-07-29 closes (MSFT 390.54, META 585.61, LITE 602.35), i.e. before the market traded the 7/29-AMC prints. The 07-30 session settled at **MSFT 451.10 (+15.5%), META 539.03 (−8.0%), LITE 693.24 (+15.1%)** — the META move matches the −8/−9% already logged on the page. Any PT-upside figure computed off the body's spot column is overstated._

| Name | New datapoint (source) | Prior wiki / house | BBG consensus (CY basis, asof 2026-07-30) | Verdict | Read |
|---|---|---|---|---|---|
| **META** | Q2'26 call validates the house cost side: total costs +55% y/y; $2.40B legal + $1.18B May-RIF severance; **3P AI token costs newly named as a P&L driver** (META Q2'26 call, 2026-07-29) | House CY26E rev $257.0bn / EPS **$32.72** | CY2026 rev **$252.4bn** · EPS **$33.72** (hi $38.04) | **DIVERGES — narrowed** | House **−3.0% on EPS**, **+1.8% on revenue**. ⚠️ **Correction of magnitude:** the body's −11.5% came off the **fiscal 1FY annual-override** pull (EPS $36.97); on the tracker's **CY quarterly-sum** basis the gap is −3.0%. Same date, same period (META's FY = CY), ~$3.25 apart. The direction holds — house still below Street on EPS while above on revenue — but the body's "cleanest same-basis divergence in the run" **overstates it**; the ~$4/share consensus-cut vector is not supported on the CY basis. Both marks retained. |
| **META** | **NO FY27 capex guide** — Li: "we aren't providing a specific outlook for 2027 CapEx at this time" (call, 2026-07-29); JPM (Anmuth) 2027 capex est **$243B, +70% y/y** (2026-07-30) | Redburn ~$145bn · "Street–JPM" ~$200-205bn · Bernstein $250bn+ · stored snapshot CY27E $198.2bn | CY2027 capex **$206.3bn** (hi $368.6bn — probable bad tick, +79% vs mean, just inside the 1.8x guard) | **DIVERGES — re-signed** | ⚠️ **Sign reversal vs the body.** Live CY-basis consensus **$206.3bn** lands **on** the ~$200-205bn "Street–JPM" mark the body proposed retiring, and ~$23bn **above** the fiscal 2FY pull ($183.0bn) it argued from. Consensus has **risen** ($198.2bn → $206.3bn), not come down. **Do not retire the $200-205bn mark.** Against $206.3bn: JPM's $243B is **+18%**, Redburn's ~$145bn is **−30%**, Bernstein's $250bn+ is **+21%** — the ~$105bn spread survives the print untested, as the body says. |
| **MSFT** | CY26 capex **~$175B**, "CY26 investment expectations remain unchanged" — a finance→operating lease reclass on a 15→25-yr useful-life extension, **not a cut**; Q1FY27 **>$50B**; no FY27 dollar figure (MSFT 4QFY26 call, 2026-07-29) | CY26 ~$190B (Q3FY26 call, 2026-04-29) — superseded · stored snapshot CY26E $157.6bn | CY2026 capex **$157.0bn** (hi $182.4bn) · CY2027 **$208.0bn** (hi $260.8bn) | **DIVERGES — (a) confirmed, (b) still unquantified** | **(a) CONFIRMED:** even after the definitional reduction, mgmt's ~$175B sits **~$18bn ABOVE** the CY26 consensus mean and still **below** street-high $182.4bn — the Street models less capex than the company intends to spend. **(b) Partly de-escalated:** the FY27 bogeys (BofA $243.5B · UBS $255-260B · JPM ~$260B · MS-Altimeter CY27 $276B) are **not** "far above" consensus on the CY basis — they sit between the CY27 mean **$208.0bn** and street-high **$260.8bn**, i.e. at the top of a range the Street already carries, and only MS-Altimeter is through the high. Still struck on the **pre-reclass** definition, so the bridge remains **blocking** and the MSFT capex edge stays **unquantified, not resolved**. |
| **MSFT** | Q4 **OCF $55.4B (+30%)**, **FCF POSITIVE $19.6B**; **FY27 explicitly guided FCF-positive** (call, 2026-07-29) | UBS FY27 FCF **−$21B**; BofA **$32B** trough | **no BBG** — the wrapper carries **no forward OCF/FCF consensus** (latest reported FY actual only) | **CONFIRMS — bear resolved** | A binary directional call, resolved against the bears by **management guidance**, not by consensus — and no consensus line exists to place it against, so this cannot be scored off BBG at all. Weakens the funding-gap/bond-debut thread by removing the near-term trigger, without contradicting it. → log to `_meta/outcomes.md` (UBS −$21B FY27 FCF, bear lost). |
| **MSFT** | Q4 EPS **$4.74** vs cons $4.24 / UBSe $4.41, including **$0.27 of discrete benefit** — largest piece a **$3.2B gain on the Anthropic investment**; clean ≈**$4.47** (call, 2026-07-29) | — | Reported quarter — **no forward line**. Forward: CY2026 EPS **$17.85** (hi $18.36) · CY2027 **$21.18** (hi $23.18) | **CONFIRMS — quality-of-earnings flag** | Still a beat on both marks, so not a miss dressed as a beat — but **+$0.27 of a +$0.50 headline beat is non-operating and its largest component is a mark on an unlisted holding**. A reported quarter cannot be placed against forward consensus; the flag stands on its own. Any FY27 EPS bridge starts from **~$4.47, not $4.74**. Asymmetry retained: MSFT **sizes the Anthropic gain and never sizes the OpenAI drag**. |
| **LITE** | **TD Cowen $990 → $800** (first PT *cut* logged on this page) · UBS re-affirmed hold · Citi Buy $1,100 + catalyst watch · quoted full range **$900-$1,400** (2026-07-29) | No TD Cowen mark; no UBS rating; Citi Buy $1,100 · house CY26E EPS $12.81 / CY27E $30.02 | Mean PT **$1,127.51** (`BEST_TARGET_PRICE`, 2026-07-30) · spot **$693.24** · CY2026 EPS **$13.08** (hi $14.63) · CY2027 **$23.90** (hi $36.81) | **DIVERGES on PT · CONFIRMS on the house** | TD Cowen's $800 is **−29% vs the consensus mean** — a genuine street-low-side mark, unusually wide dispersion. ⚠️ But consensus implies **+63% from spot $693.24**, not the **+87%** the body computed off $602.35 (the **pre-print 07-29 close**; LITE has since moved +15.1%). **House-vs-consensus CONFIRMS the body's calendarization almost exactly:** on the CY basis house CY26E $12.81 is **−1.8%** vs $13.08 and CY27E $30.02 is **+25.6%** vs $23.90 — in line on the current year, above on the out-year, *not* the +57% a naive $12.81-vs-fiscal-$8.16 comparison implies. The **$900-$1,400 range still needs its definition confirmed** before citing. |
| **NBIS** | SemiAnalysis: **DataOne campus, phased and expandable to 300 MW**, paired with **Bloom Energy behind-the-meter fuel cells** (2026-07-29) | Barclays (2026-01-21): **Vineland, NJ MSFT site, 400 MW fully-islanded on 36 × 11.2 MW Bergen gas engines** | **no BBG** (site-level capacity/power — no consensus line). Context only: CY2026 capex **$23.3bn** · CY2027 **$30.5bn** | **DIVERGES — unresolved** | 300 vs 400 MW, fuel cells vs reciprocating gas engines, different counterparty framing. May be two sites, two phases, or one site at different vintages. **Both marks left standing; neither adopted.** BBG is structurally no help here — this is resolvable only from primary filings/permits. **Do NOT mix these into any GW build-up** (facility GW ≠ IT-load GW). |
| **SNAPSHOTS** | All 97 page Snapshot blocks rendered **`asof` BLANK**; META's capex line flagged stale (this report, item 8) | Stored snapshot: META CY26E capex $144.7bn / CY27E $198.2bn, `asof` blank | META CY2026 **$147.1bn** · CY2027 **$206.3bn**; **`asof 2026-07-30` now stamped on all 97 blocks** | **RESOLVED this run** | **Root-caused and fixed:** `build_snapshot.py` read a per-company **`revisions.asof`** key that exists on **0 of 97** companies, so every block had *always* rendered blank — re-running alone would never have fixed it. Now falls back to the `estimates.json` fetch stamp. ⚠️ **Second correction: the body's directional read does not hold.** On a like-for-like CY basis consensus capex **ROSE** on both years ($144.7bn → $147.1bn CY26; $198.2bn → $206.3bn CY27) — "the Street has been CUTTING META capex into the print" was an artifact of comparing a **CY-basis snapshot against a fiscal-annual-override pull**. Note also that CY26 consensus **$147.1bn is now ABOVE the $145B top of the narrowed guide**, which is the opposite of the body's "consensus sits on the ~$137.5bn midpoint". |

_BBG refreshed 2026-07-30 — estimates.json asof 2026-07-30 (CY basis, 97/97 names fetched clean). **No PENDING column existed this run** (the Terminal was up at ingest), so Step 3 had no cell to overwrite; the table above instead re-places every quantitative row against the fresh consensus and records two basis-driven corrections to the body. The narrative items below are left **unchanged** per the thesis-drift rule — read them together with this layer, which is dated and additive._

---

### 1. META — the house model is ~11% BELOW consensus on EPS while slightly ABOVE on revenue, and the call just validated the house's cost side
| Baseline | Mark | vs new |
|---|---|---|
| **House (Capstone)** | CY26E revenue **$257.0bn**, EPS **$32.72** | — |
| **BBG live 1FY** (=FY2026=CY2026, **same basis**) | Sales **$253.4bn**, EPS **$36.97** | House **+1.4% on revenue, −11.5% on EPS** |

**This is the cleanest same-basis divergence in the run** (META's fiscal year IS the calendar year, so no calendarization needed). The house carries *more revenue and materially less earnings* than the Street — i.e. a structurally heavier cost/depreciation assumption. **The Q2 call leans toward the house:** total costs +55% y/y; **$2.40B legal-proceedings charges + $1.18B May-RIF severance**; and — first time ever disclosed — **third-party AI token costs named as a P&L expense driver**. Ex the two one-offs, Q2 OI would have grown **+9% y/y vs the reported −8%**, so the charges are the swing factor, but the token-cost line is structural and recurring.
**Action:** if the house is right on costs and the Street is at $36.97, that is a ~$4/share consensus-cut vector into H2. **Do NOT close this gap on the print** — the house's own capex path is the driver, and it should be checked against the newly-narrowed guide before touching the model.

### 2. META FY27 capex — consensus sits BELOW the number the page attributes to the Street, and management refused to guide
| Baseline | Mark |
|---|---|
| **Prior wiki** | Three-way spread: Redburn **~$145bn** / "Street–JPM" **~$200-205bn** / Bernstein whispered **$250bn+** |
| **Page Snapshot (stale)** | CY27E capex **$198.2bn** |
| **BBG live 2FY** | **$183.0bn** |
| **Management (2026-07-29)** | **NO FY27 guide.** Li: "we aren't providing a specific outlook for 2027 CapEx at this time. Infrastructure planning remains highly dynamic." |

**Live consensus ($183.0bn) is ~$15bn BELOW the page's stored snapshot ($198.2bn) and well below the "~$200-205bn Street–JPM" mark the page carries.** Either the page's Street attribution is stale/high, or consensus has come down into the print. Both readings are actionable and they point opposite ways. **The whole FY27 spread survives the print untested** — Redburn's ~$145bn and Bernstein's $250bn+ are both still live, and the range between them is now ~$105bn on a single line item.
**Action:** re-attribute the "~$200-205bn Street–JPM" figure to a dated note or retire it; the stored Snapshot needs a rebuild (see item 8).

### 3. MSFT — CY26 capex ~$175B vs stored BBG CY26 consensus $157.6bn, and the definition moved under everyone
| Baseline | Mark |
|---|---|
| **Prior wiki** | CY26 ~**$190B** (Q3FY26 call, 2026-04-29) → **superseded this run** |
| **Management (2026-07-29)** | CY26 **~$175B**, *"CY26 investment expectations remain unchanged"* — the delta is a **finance→operating lease reclass** on a **15→25-yr useful-life extension**. Q1FY27 **>$50B**. **No FY27 dollar figure.** |
| **Page Snapshot (calendarized BBG, stale)** | CY26E **$157.6bn** / CY27E **$198.9bn** |
| **BBG live fiscal** | FY27 **$188.3bn** / FY28 **$210.0bn** |

**Two separate divergences here.** (a) Even *after* the definitional reduction, management's ~$175B CY26 sits **~$17bn ABOVE** the stored CY26 consensus of $157.6bn — the Street has been modelling less capex than the company intends to spend. (b) **The FY27 bogeys on the page are now basis-broken**: BofA $243.5B / UBS $255-260B / JPM ~$260B / MS-Altimeter CY27 $276B were all struck on the pre-reclass definition, and all sit far above BBG's live FY27 $188.3bn. Some of that spread is all-in-vs-cash basis, some is the reclass, and some is genuine disagreement — **it cannot be decomposed from the page as it stands.**
**Action:** highest-priority model bridge in the run. Restate the FY27 bogeys onto the post-reclass definition before using any of them. Until then, treat the MSFT capex edge as **unquantified, not resolved**.

### 4. MSFT — the negative-FCF year the Street modelled did not arrive
| Baseline | Mark | vs new |
|---|---|---|
| **Prior wiki** | UBS FY27 FCF **−$21B**; BofA **$32B** trough | — |
| **Management (2026-07-29)** | Q4 **OCF $55.4B (+30%)**, **FCF POSITIVE $19.6B**, and **FY27 explicitly guided FCF-positive** | **Refutes the negative-FCF year outright** |

A directional call with a binary outcome, and it resolved against the bears. This also weakens the funding-gap/bond-debut thread the FY26 10-K ingest set up on 07-29 (zero FY26 debt issuance, cash+STI down $94.6B, new "continued access to capital" risk-factor language) — **not** by contradicting it, but by removing the near-term trigger.
**Action:** log to `_meta/outcomes.md` as a resolved bear (UBS −$21B FY27 FCF). The capital-structure debate stays open; the FCF-sign question does not.

### 5. MSFT — the EPS beat is real but its largest single component is a private-company mark
| Baseline | Mark |
|---|---|
| **BBG/Street** | Q4 consensus EPS **$4.24**; UBSe **$4.41** |
| **Reported** | **$4.74**, including **$0.27 of discrete benefit** — of which a **$3.2B gain on the Anthropic investment**, plus lower voluntary-retirement expense, less severance and Xbox impairments |
| **Clean** | **≈$4.47** |

Still a beat on both marks, so this is not a miss dressed as a beat — but **+$0.27 of a +$0.50 headline beat is non-operating, and the biggest piece is a mark on an unlisted holding.** Note also the asymmetry: **Microsoft sizes the Anthropic gain and never sizes the OpenAI drag** (OI&E "$2.8B *when adjusted for* the impact of our investments in OpenAI"; Q1FY27 ex-OpenAI OI&E guided ≈−$100M).
**Action:** quality-of-earnings flag on the MSFT page (done). Any FY27 EPS bridge should start from ~$4.47, not $4.74.

### 6. LITE — the first PT cut on the page lands ~29% below consensus, and below the page's own stated PT floor
| Baseline | Mark |
|---|---|
| **Prior wiki** | No TD Cowen mark; no UBS rating; Citi Buy $1,100 |
| **New (2026-07-29)** | **TD Cowen $990 → $800** (first PT *cut* ever logged here) · UBS re-affirmed **hold** · Citi **Buy $1,100** + catalyst watch · quoted full range **$900–$1,400** |
| **BBG live** | Mean PT **$1,127.51**; spot **$602.35** |

**Two things worth carrying.** (a) TD Cowen's $800 is **~29% below the $1,127.51 consensus mean** — a genuine street-low-side mark on a name where consensus still implies **~87% upside from $602.35**. That is an unusually wide sell-side dispersion and the PT-vs-spot gap alone deserves scrutiny. (b) **Internal inconsistency flagged, not resolved:** the source quotes a full PT range of **$900–$1,400** while itself reporting an $800 target — so either the range excludes the cut, or it refers to a scenario band rather than published PTs. **Recorded as an inconsistency in the source, not silently reconciled.**
**Action:** verify the $900–$1,400 range's definition before citing it. Watch LITE's **8/11 AMC** print.

### 7. NBIS — two incompatible descriptions of the same New Jersey site
| Baseline | Mark |
|---|---|
| **Prior wiki** | Barclays (2026-01-21): **Vineland, NJ MSFT site, 400 MW fully-islanded on 36 × 11.2 MW Bergen gas engines** |
| **New (2026-07-29)** | SemiAnalysis: **DataOne campus, phased and expandable to 300 MW**, paired with **Bloom Energy behind-the-meter fuel cells** |

Different capacity (300 vs 400 MW), different power solution (fuel cells vs reciprocating gas engines), different counterparty framing. These may be two different sites, two phases, or one site described at different vintages. **Both marks left standing on the page; neither adopted.** Consensus is no help here (BBG carries no site-level data), so this can only be resolved from primary filings/permits.
**Action:** primary-source check before either number is used for a GW build-up. **Do not mix these into any GW total** — per CLAUDE.md, facility GW ≠ IT-load GW.

### 8. Both page Snapshot blocks are STALE, and one is stale in a direction that matters
| Page | Stored Snapshot | BBG live (same-ish basis) | Drift |
|---|---|---|---|
| META | CY26E capex **$144.7bn**, CY27E **$198.2bn** | 1FY **$136.4bn**, 2FY **$183.0bn** | **−$8.3bn / −$15.2bn** |
| MSFT | CY26E capex **$157.6bn** | (fiscal FY27 $188.3bn — not comparable) | asof blank |

Every Snapshot block carries **`asof` BLANK**. The META capex drift is the material one: **the Street has been CUTTING META capex into the print, not raising it** — consensus 1FY $136.4bn now sits essentially on the newly-narrowed guide midpoint (~$137.5bn). Any read of "consensus expects $144.7bn" is wrong by ~$8bn.
**Action:** run `py E:/.claude/scripts/fetch_estimates.py` then `py _wiki/_tools/build_snapshot.py` to re-stamp all Snapshot blocks with a real `asof`. Flagged for `/wiki-consensus`.

---

# CONFIRMS (no action)

### MSFT Azure — beat the guide and raised, against every bogey on the page
**+43% y/y (≈42% cc)** vs a **39–40% cc guide** and buy-side bogeys of **40.7–41%**; **Q1FY27 guided ~+45% cc** vs a **41.4–42%** bogey. FY26 Azure through **$100B, +41%**. A beat *and* a ~3pt forward raise — consensus and bogeys both cleared. Note this **does not** refute the rationing evidence on the page (UBS Evidence Lab 07-26, Business Insider 07-27, Archera 07-13); management never addressed it. Growth and rationing can coexist if supply is the binding constraint.

### MSFT capex basis — reconciled from primary components, not left as a spread
Hood: *"total finance leases were $5.6 billion… cash paid for PP&E was $35.8 billion"* → **$41.4B**, i.e. the stated **$41B is lease-inclusive** and on the **same all-in basis** as the page's computed ~$42.7B. Residual **~$1.3–1.7B**, most plausibly the annual ASC-842 "ROU assets obtained" being a broader measure than four quarters of quoted finance leases, plus rounding. **Not a gross/net artifact.** Both retained with bases named. Separately: the live page's 07-29 UBS desk row quoting "capex $35.8B vs $36.13B" is a **cash-basis** comparison, correctly so — flagged on the page so it is not misread as all-in.

### MSFT cRPO — bigger, longer, and less OpenAI-dependent than the bear framing
**$678B, +84% y/y** (+25% ex-OpenAI); *"all sequential commercial RPO growth… from customers outside of Frontier model companies"*; FY26 cloud *"nearly 90% from customers outside of Frontier model companies."* Bookings **+18% ex-OpenAI vs +10% including** — i.e. **OpenAI is now a drag on the growth rate, not the source of it.** Consistent with the FY26 10-K figures already logged 07-29 (RPO $678B, 2.3-yr duration, ~30% next-12M) — same number, no double-count.

### META Q2 revenue and Q3 guide — within the bars, and the 07-28 bar dispute resolves
Q2 revenue **$60.80B (+28%)**, within the $58–61B guide and above Street $60.2B (already logged from the 8-K on 07-29 — **not re-entered**). **Q3 guide $61–64B = +19–25% y/y** lands at the *bottom* of BofA's 24–25% bar and squarely on JPM's 19–25% — **the unreconciled bar gap logged 07-28 resolves in JPM's favour.** Both bars retained on the page. BBG 1FY sales **$253.4bn** is consistent with the guided trajectory.

### META FY26 capex — consensus has converged onto the guide
Guide **narrowed to $130–145B** (from $125–145B — a low-end raise, **not** the $135–150B full raise BofA floated). BBG live 1FY **$136.4bn** ≈ the **$137.5bn guide midpoint**. Consensus and company are now aligned on the current year; the disagreement has moved entirely to FY27 (see DIVERGES #2).

### META operating metrics — all additive, none contradicted
Advantage+ end-to-end **>$75B annual run-rate** (arc >$20B → >$60B Q3'25 → >$75B, kept as a time series, old values in Changelog); **9M SMBs** on ≥1 AI creative tool (from 8M+); **GEM + sequence learning = +8.3% ad clicks / +15.7% conversion uplift on Facebook**; Meta AI daily interactors **+60%** post-Muse-Spark; Business Agents on WhatsApp/Messenger with **>1M businesses weekly**; FoA other revenue **crossed $1B, +73% y/y**; headcount **>75,000, −3% q/q** (from 77.9k; still includes the ~8k May RIF, majority out by end-Q3'26 → run-rate benefit still ahead). No house or consensus mark contradicts any of these.

### PWR — the SemiAnalysis figures corroborate management's own disclosures rather than replacing them
Technology end-market **<5% → ~10% of backlog in a year, "growing north of 100%"**; **CEI ~$1.5bn DC-related backlog, +>50% since acquisition** (net-new — not disclosed on the calls); **~$700mn committed to factory expansion + MEP fabrication, ~7m sq ft under roof.** These sit *alongside* the page's existing Q1-FY26 marks (~6.7m sq ft off-site footprint; $500–700mn HV-transformer investment) as **broader cuts of the same programme — deliberately not superseded.** BBG 1FY EPS **$13.70** vs stored snapshot CY26E **$13.24**: no meaningful drift. Signal-vs-management upgraded ⚠ nuance → ✓ confirms (old mark preserved).

### NVT — refines the page's own numbers, contradicts none
**~$688mn Trachte / ~$980mn Avail EPG** against the page's ~$0.7bn / ~$1.0bn — a refinement, **left intact rather than overwritten**. **~$1mn/MW** is the first external content-per-MW mark on the name and places NVT at the **narrow end** of the ladder (Eaton ~$2.9–3.4mn, Schneider ~$1.2–3.3mn, Vertiv ~$3.5–7mn, Quanta ~$13mn/MW whole-build). BBG 1FY EPS **$4.56** vs stored CY26E **$4.43** — no drift.

### VRT / FLEX / ETN / AMZN — content and operational marks, no estimate tension
**VRT** content **~$3.5mn/MW discrete → ~$7mn/MW full OneCore**; OneCore became the building block of NVIDIA's **Vera Rubin DSX reference design as of March 2026** (12.5 MW pods); modular lead times **>12 months, units sold out**. Existing marks (**$15.0bn YE25 backlog, 2.9x Q4 book-to-bill**) appear in the note and were **confirmed, not re-entered**. BBG 1FY EPS $6.59 vs stored CY26E $6.30 — modest upward drift, no action.
**FLEX** factory first-pass quality **>95% vs a 60–70% field baseline** (metric = share of test/inspection points cleared without rework); onsite testing cut **up to 70%**; power block **~26% of build content** → IT-ready **~22% faster (~13 vs ~16.7 months)**, **~5% cheaper/MW**. Existing CPI FY26 $6.6bn / Power +61% confirmed, not restated. BBG 1FY EPS $4.58 vs stored CY26E $3.99 — consensus has moved up; snapshot stale but not decision-relevant.
**ETN** **~$2.9mn/MW → ~$3.4mn/MW with liquid cooling** — the **first** content-per-MW figure on the page, so nothing to reconcile against. BBG 1FY EPS $13.34 vs stored CY26E $13.28 — flat.
**AMZN** AWS *"the fastest scaling buildout currently, adding almost 3.9 GW to end-2025"*; **Houdini: deployment 15 weeks → 2–3 weeks, >50,000 on-site electrician hours eliminated per module**, ~45-ft factory-built white-space skid, **~25 weeks construction-start-to-first-server-room**. Operational, not P&L — no estimate tension. BBG 1FY capex **$201.9bn** vs stored CY26E **$203.7bn** — immaterial.

### LITE / COHR house-vs-consensus — the apparent gaps are fiscal-calendar artifacts, NOT alpha
This is the trap flagged at the top, worked through so it is not re-discovered as a finding next run.
- **LITE.** House CY26E EPS **$12.81** / CY27E **$30.02**. BBG fiscal **FY26 $8.16 / FY27 $18.41 / FY28 $29.57**. Calendarizing (LITE's FY ends ~Jun/Jul): CY2026 ≈ ½(FY26+FY27) ≈ **$13.3** vs house $12.81 → house **~4% BELOW**. CY2027 ≈ ½(FY27+FY28) ≈ **$24.0** vs house $30.02 → house **~25% above**. So the house is **in line on the current year and above on the out-year** — a defensible growth-slope difference, *not* the +57% monster a naive $12.81-vs-$8.16 comparison would suggest.
- **COHR.** House CY26E EPS **$8.27**. Calendarized consensus ≈ ½($5.45+$8.47) ≈ **$6.96** → house **~19% above**. Real, but modest and out-year-weighted.
**Action: none on the models.** Recorded so the naive comparison is not mistaken for an edge.

### LITE operating datapoints — management-sourced, no consensus conflict
**~60% of the EML market**, "one of the only, if not the sole, supplier of the highest speed version at volume"; components ~65% / systems ~35%; **Japanese EML capacity up 8x in 2.5 years** (five fabs, a sixth ramping, not yet producing wafers); **two customers = 26% and 12% of fiscal Q3 2026 revenue.** The concentration figure is logged **alongside** the FY25 10-K annual split (16.0%/15.4%), which was retained as the annual measure — different periods, both correct. Note the standing tension with Citi's 07-16 management callback that **NVDA is still a low-single-digit-% customer**, which implies the 26% customer is probably *not* NVDA — flagged on the page, unresolved.

### ANTHROPIC — a balance-sheet mark, deliberately NOT converted into a valuation
MSFT booked a **$3.2B gain** on its Anthropic investment. The only prior anchor on the page is *"MSFT up to USD5bn into Anthropic"* (Nomura, 2026-06-30). **No implied valuation was inferred** — correctly: MSFT's Apr-1→Jun-30 quarter **straddles the 28-May Series H close**, so the gain most plausibly marks to a round already public, and it is a **non-cash mark**. Private name → no BBG, no house model; reconciled against prior wiki comments only. Filed as a modest counterweight to the unverified TickerTrends deceleration read, with the caveat that **a balance-sheet mark and an ARR trajectory are different objects.**

### OPENAI — no quantitative update to reconcile
The OpenAI drag on MSFT's OI&E is **carved out but never sized**; the ~$13B loss-cap / CY27 EPS-inflection thesis got no new number. Qualitative only (model-catalog position; MAI Code 1 Flash at *"comparable quality to GPT-5.6"* in Excel at significantly lower cost; ChatGPT named as a customer of Microsoft's agent web-grounding layer). Nothing to place against a baseline.

### NVDA — qualitative this run; house-vs-street context noted, not actioned
The DSX material routed to NVDA is architectural, with **no new NVDA financial datapoint**, so it generates no variance row. For context only (unchanged by this run): house CY26E EPS **$9.26** vs calendarized consensus ≈**$8.91** (+4%), house CY27E **$15.44** vs ≈**$12.88** (+20%) — the house's out-year premium is a pre-existing position, not a finding from this ingest. Same for AVGO (house CY26E $12.89 vs FY26 consensus $11.59) and AMD (no house model; BBG 1FY EPS $7.42 vs stored CY26E $7.40, flat) — both received competitive read-throughs only.

---

## Open items handed forward
1. **MSFT FY27 capex bogey restatement** onto the post-reclass definition — blocking any MSFT capex edge claim. **Highest priority.**
2. **META FY27 capex Street attribution** — re-source or retire the "~$200-205bn Street–JPM" mark; live consensus is $183.0bn.
3. **Snapshot rebuild** — every block has a blank `asof`; META's capex line is ~$8bn/$15bn stale. → `/wiki-consensus`.
4. **NBIS New Jersey** — 300 MW / fuel cells vs 400 MW / gas engines: primary-source check.
5. **LITE $900–$1,400 PT range** — confirm what the range measures, given the same source reports an $800 target.
6. **`_meta/outcomes.md`** — log MSFT FY27 negative-FCF as a resolved bear (UBS −$21B). META Q2'26 outcome deliberately deferred: the sell-side reaction and stock move are still not ingested, so the bull/bear verdict is not yet gradeable.
