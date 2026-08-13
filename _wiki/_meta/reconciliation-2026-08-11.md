# Reconciliation — 2026-08-11 (/run-inbox night run)

_Every NEW quantitative datapoint from tonight's ingest, placed against three baselines: (1) prior wiki comments, (2) Capstone house models (`_data/house.json`, models in `P:\Felipe Monteiro\US Equities\Modelos oficiais\`), (3) BBG consensus. Purely qualitative/thematic content is not reconciled here._

**Sources reconciled:** Bernstein "TSMC: Higher revenue & capex on CPU" (2026-08-10) · Bernstein "Global Semiconductor Equipment: Equip this! Raising WFE growth to 75% in two years" (2026-08-11) · Bernstein "Global Memory, NVIDIA & Broadcom: Quick thoughts on strategic partnerships" (2026-07-27, ingested two weeks late) · Goldman Sachs "Optical Networking: Top 3 investor debates…" (2026-08-11) · NSF NCSES InfoBrief NSF 25-353 (2025-09-29).

⚠️ **BBG BASIS — READ THIS BEFORE USING THE THIRD COLUMN.** The **live** `bdp` call failed at 23:50 with **HTTP 503 — "Bloomberg connection test failed, please ensure you are logged in to Bloomberg Terminal"** (local blpapi also failed: `connect event failed` on 127.0.0.1:8194, i.e. Terminal not running/logged out on an unattended night run). **The BBG column therefore uses the ON-DISK snapshot `_wiki/_data/estimates.json`, which is dated 2026-08-11 — same day, pulled by the 21h run — so it is current, not stale.** No web data was substituted. Where a period basis does not line up (fiscal vs calendar), it is flagged in the row and **the row is excluded from the DIVERGES list**.

⚠️ **UNIT CAVEAT ON TSM.** In `estimates.json`, TSM's `px` is the **ADR price in USD** while `eps` is **TWD per ADR** (1 ADR = 5 ordinary shares) and `ccy` is labelled TWD. Consensus EPS below has been **divided by 5** to compare with Bernstein's per-ordinary-share NT$ estimates. This mixed-unit record is a data-hygiene problem in the snapshot itself and is worth fixing in `fetch_estimates.py`.

---

## Where the new data DIVERGES

### 1. 🔴 KIOXIA — Bernstein's 2027 EPS is **29% BELOW consensus**, and it is the only downside price target in the run
| Baseline | 2026E EPS (¥) | 2027E EPS (¥) | PT | vs spot |
|---|---:|---:|---|---:|
| **Bernstein (07-27, NEW)** | **10,013** | **9,657** | **¥40,000 (Underperform)** | **−16.7%** |
| BBG consensus (08-11) | 8,141 | 13,533 | — | — |
| Delta | **+23.0%** | **−28.6%** | | |
| Prior wiki | JPM OW ¥130,000 (still standing) | | | |

**Bernstein has KIOXIA EPS DECLINING 3.6% in 2027E while consensus has it rising 66%.** That is not a valuation overlay on a shared cycle view — it is a different earnings path, and it is the sharpest single divergence produced by tonight's ingest. **The mechanism is explicit and testable: "we worry about the long-term threat from China in NAND… the threat is much lower in DRAM as China eventually will find it difficult to compete in DRAM market WITHOUT EUV."** ➜ **Action: this is a litho-access ceiling argument, so it is falsifiable in bit-per-wafer, not in wpm. The JPM mark already on the wiki — YMTC at bit/wafer parity with the leaders and ~16% of global NAND supply by 2028E — is the Bernstein thesis arriving on schedule if it holds. Against it: Bernstein has raised this PT ~27x in a year (¥1,500 → ¥40,000) while never moving off Underperform, i.e. repeatedly marked to market by the cycle. Treat the RATING as a structural view being outrun by the tape, and the 2027 EPS gap as the number to attack.** No house model for KIOXIA.

### 2. 🔴 TOKYO ELECTRON — **+27.7% above consensus on 2027E**, the largest clean above-consensus gap in the run, on a PT just raised 34%
| Baseline | 2026E EPS (¥) | 2027E EPS (¥) | PT | vs spot |
|---|---:|---:|---|---:|
| **Bernstein (08-11, NEW)** | **1,687.17** | **2,635.81** | **¥79,300 (OP)** | **+39.7%** |
| Bernstein prior (07-20) | 1,504.14 | 1,848.77 | ¥59,200 | *(was BELOW spot)* |
| BBG consensus (08-11) | 1,556.34 | 2,063.63 | — | — |
| Delta vs consensus | **+8.4%** | **+27.7%** | | |

**The 2027E estimate was raised 43% in three weeks and now sits 28% above the Street.** The PT implies only **30.1x 2027E**, i.e. the target is carried by earnings, not multiple — and TEL is the cheapest of Bernstein's own "Big 5" at ~30.3-31.6x forward. ➜ **Action: this is the cleanest expression of the memory-led WFE raise in the coverage, because TEL is ranked only SECOND in its own regional cohort (Kokusai > TEL > Screen) yet still carries the biggest consensus gap. If the DRAM WFE line ($69bn 2027E / $96bn 2028E) is right, consensus on TEL is materially too low. No house model.** ⚠️ **Counterweight retained: Bernstein's own 07-30 note has TEL second-to-last of the majors on revenue and EPS CAGR, and at 27% of 1H CY26 revenue from China — "the wrong end" of the localisation risk. Same house, both readings on the page.**

✅ **08-13 live re-placement (this name was in the 38 the 08-12 pull could not reach).** BBG consensus is **UNCHANGED TO THE DECIMAL** — CY2026 **¥1,556.34**, CY2027 **¥2,063.63** — so Bernstein's gaps stand exactly as written: **+8.4% / +27.7%**. **New from the live pull, and it strengthens the finding materially: Bernstein's 2027E ¥2,635.81 is not merely above the median, it is +21.2% ABOVE THE STREET HIGH (¥2,174.66)** — the entire sell-side distribution sits below it. Its 2026E is also **+2.0% above the street high** (¥1,653.51). ⚠️ **The entry moved against it:** spot **¥59,470** (from ~¥56,764 on 08-11, **+4.8%**), so PT upside compressed **+39.7% → +33.3%** and the stock now trades at **28.8x consensus 2027E**. **Stays DIVERGES — and it is the widest above-street-high gap on the board.**

### 3. 🔴 SK HYNIX — Bernstein pulls earnings **FORWARD** vs the Street: +24% on 2026E, in line on 2027E
| Baseline | 2026E EPS (KRW) | 2027E EPS (KRW) | PT | vs spot |
|---|---:|---:|---|---:|
| **Bernstein (07-27, NEW)** | **395,677** | **568,862** | **KRW 3,300,000 (OP)** | **+130.3%** |
| BBG consensus (08-11) | 318,175 | 574,123 | — | — |
| Delta | **+24.4%** | **−0.9%** | | |
| Prior wiki | JPM OW W2,750,000 | | | |

**Same three-year total, different shape: Bernstein loads 2026 and consensus loads 2027.** ➜ **Action: the disagreement is about WHEN the memory earnings land, not how much — which makes it a positioning question rather than a thesis question, and it is resolvable at the next two prints rather than in 2028. Note also that the KRW3.3mn PT is +130% to spot, by far the widest gap in the run, on only 6.2x forward 5Q-8Q EPS of KRW536,158 — the multiple is not doing the work. No house model.**

### 4. 🔴 AVGO — the house model is **+40% above Bernstein on 2028**, and the gap is entirely in the out-year
| Baseline | 2026E EPS (US$) | 2027E EPS (US$) | 2028E EPS (US$) |
|---|---:|---:|---:|
| **Bernstein (07-27, NEW)** | 11.60 | **18.69** | **~25.65** *(implied: PT = ~25x the avg FY27/28 pro-forma EPS of $22.17)* |
| **Capstone house model** | 12.89 | **21.07** | **35.96** |
| BBG consensus (08-11, CY basis) | 13.61 | 21.28 | — |
| House vs Bernstein | +11.1% | **+12.7%** | **+40.2%** |

**Bernstein's FY27 is 12% below the house and 12% below consensus; by FY28 the house is 40% above Bernstein.** ⚠️ **Basis caveat: AVGO's fiscal year ends in November, so the BBG CY comparison is imperfect and is shown for context only — but the HOUSE-vs-BERNSTEIN comparison is like-for-like (both fiscal) and is the real finding.** ➜ **Action: the house's $35.96 FY28 EPS embeds the $274bn AI-revenue-in-2028 assumption already on `AVGO.md`; Bernstein's implied ~$25.65 does not, and Bernstein's own framing treats "$100B+ next year" as management's guide rather than its own forecast. This is the same FY28 step-up fork the page already carries (house $274bn / Barclays >$300bn / Arete $177bn) — Bernstein now sits at the Arete end of it. Name the bridge before defending the house number.**

### 5. 🔴 NVDA — the house is **+23% above Bernstein and +20% above consensus on 2027**
| Baseline | 2026E EPS (US$) | 2027E EPS (US$) |
|---|---:|---:|
| Bernstein (07-27) | 9.19 | **12.52** |
| BBG consensus (08-11) | 8.86 | 12.91 |
| **Capstone house model** | 9.26 | **15.44** |
| House vs Bernstein | +0.8% | **+23.3%** |
| House vs consensus | +4.5% | **+19.6%** |

**On 2026 everyone agrees inside 5%; on 2027 the house is alone.** Bernstein is actually **3% BELOW consensus** on 2027 while carrying a $315 PT (~25x its own 2027 EPS). ➜ **Action: this is a restatement of a standing house edge rather than a new one, but tonight's datapoint sharpens the supply side of it — the 2GW Vera Rubin DSX AI Factory for SK Telecom in 2027 is a dated, sized, named-offtaker deployment that was not on the page, and Bernstein reads management's cumulative guide as "~$1T across CY25-27 suggestive of close to $500B next year." House revenue of $661bn for 2027 sits above that read. If the house is right, the gap is volume, and the Korean facility is one of the places to look for it.**

### 6. 🟡 TSM — Bernstein's "broadly above consensus" is **much weaker against BBG than against its own consensus set**, and its 2027 capex is BELOW the Street
| Metric | Bernstein (NEW) | Bernstein's stated consensus | BBG consensus (08-11) | vs BBG | Capstone house |
|---|---:|---:|---:|---:|---:|
| EPS 2026E (NT$/ord sh) | **110.70** | 97.9 *(+13.1%)* | 104.01 | **+6.4%** | **102.5** *(house −7.4% vs Bernstein)* |
| EPS 2027E (NT$/ord sh) | **144.85** | 122.3 *(+18.5%)* | 142.21 | **+1.9%** | **143.5** *(house −0.9%)* |
| Revenue 2026E (NT$m) | 5,456,906 | 5,191,000 | 5,435,497 | +0.4% | US$165bn *(vs Bernstein US$173bn, −4.8%)* |
| Revenue 2027E (NT$m) | 7,328,054 | 6,558,000 | 7,343,707 | **−0.2%** | — |
| **Capex 2026E (NT$m)** | 2,016,002 | — | 1,958,813 | **+2.9%** | — |
| **Capex 2027E (NT$m)** | **2,370,075** *(US$75bn)* | — | 2,466,407 *(≈US$78bn)* | **−3.9%** | — |

🔴 **THE FINDING: Bernstein advertises being 13-19% above consensus, but against the BBG median it is +6.4% and +1.9%, and on 2027 REVENUE it is fractionally BELOW.** The gap is in the consensus set, not in Bernstein's estimates — its "% Diff vs Consensus" column is measured against a materially lower base than the current BBG median. ➜ **Action: do not repeat "Bernstein is 18.5% above consensus on 2027" as if it were a Street-relative statement. Against the live median it is a ~2% call.**
🔴 **SECOND FINDING, and it is the more interesting one: Bernstein models 2027 capex 3.9% BELOW consensus while modelling EPS above it.** That is internally consistent with its own thesis — *"TSMC's recent capex hike is primarily for WAFER capacity, and much less so for CoWoS… CoWoS capacity is still being expanded, but at a pace planned originally"* — and it means part of the EPS edge comes from **lower depreciation**, not higher revenue. ⚠️ **It also puts Bernstein at the bottom of the 2027 capex range the wiki carries: Fubon US$80-85bn (08-03, with "I'm not sure that is enough"), JPM ~US$78bn, TD Cowen US$80bn, Bernstein US$75bn, Redburn US$70-75bn. If Fubon is right, Bernstein's D&A is too low and its 2027 EPS edge shrinks further.**

### 7. 🟡 ADVANTEST — estimates **+29% above consensus on 2026E**, yet the PT was left UNCHANGED
| Baseline | 2026E EPS (¥) | 2027E EPS (¥) | PT |
|---|---:|---:|---|
| Bernstein (08-11) | **948.96** | **1,088.87** | **¥45,800 — UNCHANGED** |
| BBG consensus (08-11) | 733.78 | 959.18 | — |
| Delta | **+29.3%** | **+13.5%** | |

**A ticker-table entry in a WFE note, and the PT did not move even as Bernstein raised targets on five other names in the same table.** The PT implies **42.1x 2027E**, the second-highest implied multiple in the run after DISCO. ➜ **Action: the non-move is the information — Advantest is a TEST name and the WFE raise does not flow through its model, which is also why it is absent from the note's Japan preference ranking. But a +29% consensus gap sitting under a static PT is worth a look: either the estimates or the target is stale.**

✅ **08-13 live re-placement (unreachable on the 08-12 pull).** Consensus **UNCHANGED TO THE DECIMAL** — CY2026 **¥733.78**, CY2027 **¥959.18** ⇒ Bernstein still **+29.3% / +13.5%**. **The live pull sharpens the “either the estimates or the target is stale” question by giving the gap a SHAPE: Bernstein's 2026E ¥948.96 is +20.3% above the STREET HIGH (¥788.74), but its 2027E ¥1,088.87 is only +0.4% above the street high (¥1,084.53)** — an outlier on the near year, merely top-of-range on the out year. Spot **¥35,940** ⇒ the unchanged ¥45,800 PT now implies **+27.4%** upside and **47.7x consensus 2027E**. **Stays DIVERGES (🟡) — the gap is concentrated in the near year, which is where a static PT is least defensible.**

### 8. 🟡 DISCO — **+16% / +24% above consensus**, PT raised 16%, on the thinnest possible coverage
| Baseline | FY26E EPS (¥) | FY27E EPS (¥) | PT |
|---|---:|---:|---|
| Bernstein (08-11) | **1,830.28** | **2,336.94** | **¥99,000 (from ¥85,000)**, +57.2% vs spot |
| BBG consensus (08-11) | 1,577.58 | 1,885.55 | — |
| Delta | **+16.0%** | **+23.9%** | |

⚠️ **Weight this down deliberately: DISCO appears ONLY in the coverage ticker table — no paragraph, no investment-implication line, and it is absent from the note's Japan preference ranking. The PT moved because the sector model moved.** The implied multiple is **42.4x FY27E**, the highest in the run. ➜ **Action: a +24% consensus gap and a 42x implied multiple on a name with no written thesis behind it is a low-conviction signal, not an idea. The page says so.**

✅ **08-13 live re-placement (unreachable on the 08-12 pull) — and this is the one of the three that MOVED.** Consensus drifted **DOWN**: CY2026 **¥1,573.21** (from ¥1,577.58, **−0.3%**) and CY2027 **¥1,877.94** (from ¥1,885.55, **−0.4%**), so the gaps **WIDENED** to **+16.3% / +24.4%** (from +16.0% / +23.9%). Bernstein's FY27E ¥2,336.94 is **+12.0% above the street high** (¥2,086.72). Spot **¥65,830** (+4.5% since 08-11) ⇒ PT upside **+57.2% → +50.4%**, implying **52.7x consensus 2027E**. ⚠️ **The weight-it-down caveat is UNCHANGED and still governs: a ticker-table entry with no written thesis behind it.** **Stays DIVERGES (🟡), low conviction.**

### 9. 🟡 The WFE level itself — Bernstein's CY27 is now **ABOVE both vendors willing to name a number**
| Source | CY2026 | CY2027 | CY2028 |
|---|---:|---:|---:|
| **Bernstein (08-11, CORRECTED)** | **$154bn** | **$204bn** | **$259bn** |
| Bernstein prior | $148bn | $175bn | $198bn |
| KLA (management, FQ4 call) | low-$150s | **">$190bn"** | — |
| Tokyo Electron (management) | ">$150bn" | ">$190bn" | — |
| LRCX (management) | low-$150s (+36-40%) | — | — |
| Screen / Kokusai | ">$140bn" / +25% | "similar growth" / +20% | — |
| Prior wiki (Bernstein 07-20 GW-frame) | — | $200bn *(50GW scenario)* | $245bn *(CY28)* |

🔴 **For the first time this cycle a major sell-side WFE mark sits ABOVE management's own stake in the ground — $204bn vs ">$190bn" from both KLA and TEL.** The standing framing on `KLAC.md` ("buyside is already there and higher — doesn't move the needle") has been inverted at the top end. ⚠️ **Note the corrected 2026 figure: at the relayed $148bn the current-year mark equalled the PRIOR estimate; at $154bn it is a $6bn raise and sits slightly ABOVE LRCX's own low-$150bn guide rather than below it — see the correction record on `LRCX.md`.** ➜ **Action: the CY27 gap ($204bn vs >$190bn) is the number to test at the next two semicap prints; it is also ~$4bn above Bernstein's own July GW-derived $200bn for CY27, so the house's two frameworks now agree.**

### 10. 🟡 AMAT — Bernstein's raise is **100% volume, 0% margin**, which collides with UBS on the same page
| Metric | Bernstein FY26E | FY27E | FY28E |
|---|---:|---:|---:|
| Revenue | $33,233m *(unch)* | $42,628m *(from $40,688m)* | $53,053m *(from $46,646m)* |
| **Gross margin** | **49.9%** | **50.5%** | **50.9%** — **UNCHANGED IN EVERY YEAR** |
| Operating margin | 32.5% *(unch)* | 34.9% *(from 34.1%)* | 36.5% *(from 35.3%)* |
| EPS | $12.17 *(unch)* | $16.68 *(from $15.56)* | $22.04 *(from $18.69)* |

**UBS (07-30, already on `AMAT.md`) underwrites "upside to 54-55% gross margin over time as it pushes pricing higher." Bernstein's terminal GM is ~51%. Two bulls, same direction, ~350-400bps apart at the gross line.** ➜ **Action: the AMAT bull case has two incompatible engines running under it. Ask which one the 08-13 print supports — pricing commentary is the discriminator, and UBS has already named it as "the most important metric."** ⚠️ **PT construction flagged: $675 implies 40.5x FY27E or 30.6x FY28E on Bernstein's own numbers, against the note's own observation that AMAT trades at ~32.6x forward — i.e. the target is a hold-the-multiple-and-roll-to-FY28 construction. The note does not state an AMAT valuation methodology in the text; this is inferred and labelled as such.**

---

## CONFIRMS (no action)

| Datapoint | New value | Baseline | Read |
|---|---|---|---|
| **ASML EPS** | EUR 38.91 (2026E) / 53.56 (2027E) | BBG 36.60 / 53.04 | **+6.3% / +1.0% — effectively consensus.** The EUR 2,500 PT (40x Q5-8 EPS of EUR 62.6) is a MULTIPLE call, not an estimate call. No house model for ASML. |
| **ASML FY26 revenue** | EUR 44bn (midpoint of the raised EUR 43-46bn guide, +35% y/y) | BBG CY2026 EUR 42.6bn | +3.2% — inside the company's own guided range. |
| **ASML DUV capacity** | 200 units by 2028 | ASML target 220 | **Bernstein is 9% BELOW management inside a top-pick call** — conservative in the unusual direction; confirms rather than stretches. |
| **SAMSUNG EPS** | KRW 48,393 (2026E) / 77,273 (2027E) | BBG 46,404 / 75,198 | **+4.3% / +2.8% — in line.** The KRW440,000 PT (+82.6% vs spot) is carried by the 6.2x multiple, not by estimates. |
| **TSM revenue 2027E** | NT$7,328bn | BBG NT$7,344bn | −0.2% — in line (see DIVERGES #6 for why this matters). |
| **NVDA 2026E EPS** | $9.19 | BBG $8.86 · house $9.26 | All three inside 5%. |
| **KLAC / LRCX FY28E EPS** | $7.05 / $10.97 | BBG CY2027 $6.26 / $10.63 | +12.6% / +3.2% — modest, and the fiscal-vs-calendar offset explains most of it. Both PTs imply ~35x the second forward year, the same construction as AMAT. |
| **Global optical module TAM** | $34.2bn (2025) → $50.9bn (26E) → $72.6bn (27E) → **$69.1bn (28E)** | No prior wiki TAM at this granularity | **First full speed-tier module TAM on the wiki.** No conflict to reconcile — but the **2028E DECLINE** is a new, dated, falsifiable claim that nothing else on `optical-cpo` carries. Flagged there rather than here. |
| **US business R&D** | $722bn (2023, +4.4%); semis (NAICS 3344) 25.8% R&D intensity | No prior wiki baseline | Reference statistic, 2023 vintage, pre-dates the AI capex acceleration. Filed to `macro-cycle` only. |

---

## Rows EXCLUDED from the divergence list on basis mismatch (recorded so nobody re-derives them as findings)

| Name | Apparent gap | Why it is not a finding |
|---|---|---|
| **MU** | Bernstein FY26E $67.39 vs BBG CY2026 $96.45 = **−30%** | **MU's fiscal year ends in August.** With EPS compounding ~140% y/y, a four-month basis shift produces most of this gap. FY27E $158.99 vs CY2027 $163.61 is **−2.8%**, i.e. in line once the base evens out. Not a divergence. |
| **AMAT** | FY26E $12.17 vs CY2026 $13.74 = **−11.4%**; FY27E vs CY2027 = **−12.6%** | **AMAT's fiscal year ends in late October.** On a business growing 28% in FY27 the two-month offset is worth roughly 5pp, and the non-GAAP/GAAP treatment differs. The real AMAT finding is the margin architecture (DIVERGES #10), not the level. |
| **AVGO (vs BBG only)** | FY26E $11.60 vs CY2026 $13.61 = **−14.8%** | **AVGO's fiscal year ends in November.** The house-vs-Bernstein comparison in DIVERGES #4 is fiscal-to-fiscal and is the valid one. |
| **LRCX / KLAC FY27E** | +22.1% / +22.4% vs BBG CY2026 | **Both fiscal years end in June**, so FY27E straddles CY2026H2 and CY2027H1 — roughly half a year of growth is being counted as an estimate gap. The FY28E-vs-CY2027 comparisons are the cleaner ones and are in the CONFIRMS table. |

---

## Carry-forward / open items
1. ~~**BBG live pull failed (503, Terminal logged out).** The on-disk snapshot used here is same-day, so nothing is PENDING — but a live re-pull would let the KIOXIA and TOKYOELEC gaps be checked against intraday medians rather than the 21h snapshot. Run `/wiki-consensus` when the Terminal is up.~~ ⚠️ **PARTIALLY DONE 2026-08-12 — `KIOXIA` re-placed live, `TOKYOELEC` COULD NOT BE.** The 08-12 `/wiki-consensus` pull completed **60 of 98 names**; the BBG entitlement flipped to `LIMIT / REVIEW / Access pending review` at ticker 61 and the HTTP wrapper fallback was unreachable (ConnectTimeout), so the last 38 names — **including TOKYOELEC, ADVANTEST and DISCO** — are still the 2026-08-11 snapshot and are now stamped as such (`revisions.asof=2026-08-11`, `carried_over=true`). **Every fresh name re-places to the decimal and no row moves between DIVERGES and CONFIRMS:** KIOXIA 2026E **¥8,140.64** / 2027E **¥13,532.64** (unchanged ⇒ Bernstein still **+23.0% / −28.6%**, #1 stands); SKHYNIX 2026E KRW **318,057** (−0.04% drift) / 2027E **574,123** unchanged ⇒ **+24.4% / −0.9%**, #3 stands; NVDA **$8.86 / $12.91** and AVGO **$13.61 / $21.28** both unchanged ⇒ #4 and #5 stand; TSM rev/capex/EPS unchanged ⇒ Bernstein **+6.4% / +1.8%** on EPS, **−0.2%** on 2027 revenue and **−3.9%** on 2027 capex, so #6's "it is a ~2% call, not an 18.5% one" holds on live data. ~~**Divergences #2 (TOKYOELEC), #7 (ADVANTEST) and #8 (DISCO) remain un-re-placed and still rest on the 08-11 snapshot — re-run `/wiki-consensus` once the entitlement clears.**~~ ✅ **CLOSED 2026-08-13 — the entitlement cleared and all 98 names pulled live (0 carry-overs).** All three re-placed above: **TOKYOELEC and ADVANTEST consensus unchanged to the decimal** (gaps stand at +8.4%/+27.7% and +29.3%/+13.5%), **DISCO drifted −0.3%/−0.4% so its gaps WIDENED** to +16.3%/+24.4%. **No row crossed DIVERGES ↔ CONFIRMS.** The material addition is that **all three Bernstein marks sit ABOVE THE STREET HIGH, not just above the median** (TOKYOELEC 2027E +21.2%, DISCO FY27E +12.0%, ADVANTEST 2026E +20.3%) — a stronger statement than the original finding made.
2. **`estimates.json` has a mixed-unit record for TSM** (px in USD per ADR, eps in TWD per ADR, ccy labelled TWD). Worth fixing in `fetch_estimates.py` — any automated house-vs-consensus comparison on TSM is currently wrong by 5x unless it happens to divide.
3. **No house model exists for ASML, TOKYOELEC, KIOXIA, SKHYNIX, SAMSUNG, DISCO or ADVANTEST** — five of the ten divergences above therefore have only two baselines. The Japanese semicap names in particular now carry the largest consensus gaps in the coverage with no house view against them.
4. **Kokusai (6525.JP) has no wiki page and is Bernstein's TOP Japan pick, ranked above TOKYOELEC.** Second time in three weeks. It cannot be reconciled at all.

---

_BBG column resolved 2026-08-12 — `estimates.json` asof **2026-08-12 (PARTIAL: 60/98 names fetched live; 38 names, incl. TOKYOELEC / ADVANTEST / DISCO, carried over from 2026-08-11 and stamped `revisions.asof=2026-08-11`)**. No `PENDING` cell existed in this report, so Step 3 had no cell to overwrite; the re-placement above is the resolution of carry-forward item 1. **No row crossed DIVERGES ↔ CONFIRMS.** Canonical header `## Where the new data DIVERGES` applied (was `## DIVERGES (the alpha)`)._

_BBG column re-resolved 2026-08-13 — `estimates.json` asof **2026-08-13 (FULL: 98/98 names pulled live; 0 records byte-identical to the 08-12 vintage, 0 null prices, 0 carry-over stamps)**. The three names stranded by the 08-12 entitlement block (TOKYOELEC / ADVANTEST / DISCO) are now re-placed on live data in §§2, 7 and 8. **No row crossed DIVERGES ↔ CONFIRMS.**_
