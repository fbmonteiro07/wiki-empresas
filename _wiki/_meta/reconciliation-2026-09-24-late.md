# Reconciliation — 2026-09-24 (LATE run)

_Second `/run-inbox` of 2026-09-24. The 08:10 run has its own report at [reconciliation-2026-09-24.md](reconciliation-2026-09-24.md); this one covers **only** the two sources that landed on `P:` after that run archived (08:14 and 08:37)._

**Sources reconciled**
1. **Morgan Stanley · Meta A Marshall / Adam Wood / Ryan Lountzis — *"Oktane 2026: AI Bringing Identity Modernization into Focus"*, 2026-09-24 10:30 GMT.** [[OKTA]] Overweight, PT $200.
2. **Bernstein · Madison Rezaei / Gautam Chhugani / Nancy Wu / Mahika Sapra / Sanskar Chindalia / Harsh Misra — *"Neoclouds: A contract sport! CRWV, IREN takeaways from Nscale's S1"*, 2026-09-24 04:01 UTC.** [[CRWV]] Underperform PT $74; IREN Outperform PT $100.

**Baselines used**
- **BBG consensus: LIVE, not pending.** `_wiki/_data/estimates.json` carries `asof = 2026-09-24`, written 09:04 today by the concurrent consensus refresh — a same-day snapshot, so it is used as the baseline rather than marked PENDING. Annual claims are read off the **1FY/2FY/3FY** lines (OKTA's fiscal year ends in January, so the CY sums are a different period and are never netted against them). EBIT is preferred to EPS throughout.
- **House models: none exist for OKTA, CRWV, NBIS or NSCALE** (`house.json`). NVDA has one, but this run's NVDA datapoints are structural (the Nscale financing package), not estimates, so there is nothing in the model to reconcile them against. **No house column below is left blank by oversight.**

---

## ✅ CONFIRMS

| # | Claim (source) | Baseline | Verdict |
|---|---|---|---|
| C1 | **OKTA spot $205.36** (MS, close 23-Sep) | BBG `px` **205.36** | ✅ **Exact.** Both notes in this run also price off the same tape — Bernstein and the concurrent JPM upgrade both use CRWV **$86.90** (23-Sep), matching BBG `px` 86.90 exactly. No stale-price problem anywhere in this batch |
| C2 | **OKTA FY Jan-2028e revenue $3,534m** (MS) | BBG **2FY $3,547.4m** | ✅ **In line, −0.4%** |
| C3 | **OKTA FY Jan-2028e EBIT $941m** (MS) | BBG **2FY EBIT $948.1m** | ✅ **In line, −0.7%.** Reconciled at EBIT per the standing rule |
| C4 | **OKTA FY Jan-2028e EPS $4.29** (MS ModelWare) | BBG **2FY EPS $4.382** | ✅ **−2.1%** — marginally below, consistent with C2/C3. MS's own printed Refinitiv comparison ($4.34) sits between the two |
| C5 | **OKTA FY Jan-2027e EPS $3.92** (MS) | BBG **1FY EPS $3.935** | ✅ **In line, −0.4%** |
| C6 | **OKTA rating distribution 80% OW / 20% EW / 0% UW** (MS, via Refinitiv) | BBG **n=47: 37 buy / 10 hold / 0 sell = 78.7 / 21.3 / 0** | ✅ **Confirms.** The two panels agree on *ratings* to within one name — which makes D1 below the sharper finding, because they do **not** agree on targets |
| C7 | **OKTA consensus PT LOW $127** (MS) | BBG `pt.lo` **127.0** | ✅ **Exact** |
| C8 | **NBIS 1H2026 revenue $981m and op margin −31%** (Bernstein, Exhibit 8) | BBG 1FY rev **$3,337.9m**; Q3-26E **$888.6m** + Q4-26E **$1,427.3m** = $2,315.9m 2H ⇒ implied 1H ≈ **$1,022m**; 1FY EBIT margin **−27.1%** | ✅ **Reconciles.** Bernstein's reported 1H actual and the consensus quarterly path are consistent to ~4% on revenue, and the −31% 1H margin against a −27.1% full-year consensus is the same improving shape. **Bernstein does not cover NBIS and its figures are its own estimates off company disclosures — they nonetheless tie out** |
| C9 | **CRWV FY2025 revenue $5,131m, op income $(45)m, net $(1,223)m; 1H2026 revenue $4,653m, op income $(193)m, net $(1,366)m** (Bernstein, Exhibit 8) | [[CRWV]] page (">$5bn in 2025"), Q2 print already logged | ✅ **Confirms reported actuals.** No new information, logged as an external check |
| C10 | **CRWV DDTL spread ladder** (Bernstein, Exhibit 10: +9.6 / +4.3 / +4.3 / +4.0 / +2.3 / +4.5 / +5.5) | Redburn primary 09-21 already on the page (962 / 425 / 400 / 225 / 450 / 550bp) | ✅ **Second independent house, matches within rounding.** Bernstein adds DDTL 2.1 and 5.0. The cost-of-debt curve is now corroborated, not single-sourced |
| C11 | **CRWV leases all of its datacenters** (Bernstein Exhibit 6: 51 sites, all shown as leased) | Standing claim on the page since the lease-commitments risk was logged | ✅ **Confirms** |
| C12 | **JPM's 09-18 Oktane preview — "no new numbers or mid-term financial targets expected"** | MS, who attended: *"the company did not provide any new financials or targets"* | ✅ **Preview scored correct.** A pre-registered expectation resolved by an eyewitness |

---

## 🔴 DIVERGES — the alpha

### D1. 🔴🔴 **Two consensus panels disagree by 7.6% on OKTA's price target on the same day — and the disagreement is exactly large enough to flip Morgan Stanley's own positioning claim.**

| | MS note (Refinitiv, 2026-09-24) | BBG (`estimates.json`, asof 2026-09-24) | Gap |
|---|--:|--:|--:|
| Consensus PT | **$186.77** | **$200.93** | **+$14.16 / +7.6%** |
| High | $230.00 | $240.00 | +$10 |
| Low | $127.00 | $127.00 | — |
| Panel size | not stated (80/20/0 split) | **n = 47** (37/10/0) | — |

**Why it matters, and it is not a housekeeping point.** MS positions its **$200** target as sitting *above* consensus — true on the Refinitiv panel it prints ($186.77), where $200 is **+7.1%**. **On BBG the same target is AT consensus ($200.93, −0.5%).** So the entire "we are more constructive than the Street" framing of the note is an artifact of panel choice. ➤ **The ratings panels agree to within one name (C6) while the target panels are $14 apart — which means the gap is not a different set of analysts, it is a different set of *targets* for substantially the same analysts (stale marks carried by one vendor and refreshed by the other).** ⚠️ **Neither number is adopted as "the" consensus. The wiki now carries both with their vendor named, and the rule this produces is general: any note claiming a position versus consensus must be checked against the panel the wiki uses, because on this name the two vendors differ by more than most houses' PT revisions.**

### D2. 🔴🔴 **Bernstein's CRWV target is 48% below consensus — the most bearish published mark this wiki carries on the name, and the note gives no estimates to reconcile it with.**

- **Bernstein PT $74** vs **BBG consensus PT $142.18** (n=45; 31 buy / 10 hold / 4 sell; hi $317, lo $39) ⇒ **−48.0%**. Spot $86.90, so Bernstein implies **−14.8%** while the Street implies **+63.6%**.
- ⚠️ **The stated valuation basis CHANGED between Bernstein notes and the change is not explained.** 07-01 (already on the page): *"PT basis: **28.4x 2027E Adj. EBIT/share of $5.81**"* — a per-share multiple. 09-24: *"We value the company on a **25.5x EV/EBIT** basis"* — an enterprise multiple. **These are different constructions, not a multiple cut.**
- ⚠️⚠️ **THE TARGET CANNOT BE REBUILT FROM THIS DOCUMENT AND IS NOT REJECTED ON THAT BASIS.** The note prints no Bernstein revenue or EBIT estimate. Running 25.5x against **BBG 2FY EBIT of $4,154m** gives EV ≈ $105.9bn; against the current EV of $94.6bn and market cap of $48.6bn (net debt ≈ $46.1bn, ~559m shares) that implies roughly **$107/share, not $74** — so Bernstein's own EBIT must sit far below consensus, or the multiple applies to a different year or a per-share quantity. ➤ **The arithmetic gap is logged as an OPEN QUESTION requiring Bernstein's estimate table, NOT as an error.** (Standing rule: reconcile an implausible broker number before discarding it; check the period basis first.)
- ➤ **Corroborating context from the concurrent 21h run on the same page and the same day:** JPM upgraded CRWV to Overweight with **PT $125 from $120** — also **below** the $142.18 BBG consensus. **Three houses now sit at or under consensus on target while the consensus rating stays 31-buy.** The dispersion is extreme: **hi $317 vs lo $39 on a $86.90 stock.**

### D3. 🔴🔴 **A 2x disagreement on CRWV's average contract length, between the two most bearish houses, three days apart — and it is the input the whole asset-liability argument runs on.**

| Source | Average customer contract length |
|---|---|
| **Bernstein, Exhibit 7 (2026-09-24)** | **~6 years** |
| **Rothschild & Co Redburn, 148pp primary (2026-09-21)** | **~3 years** |

**No BBG line exists for this.** Peer marks in the same Bernstein exhibit: Nscale **5.7yr** (filed, and independently on [[NSCALE]] from the S-1), NBIS **~5yr**, IREN **~4yr** — Bernstein's own peer set clusters at 4-6 years, which makes Redburn the outlier. ➤ **Neither adopted. Resolvable off the RPO / backlog-duration disclosure, and it should be resolved: at 3 years the renewal-repricing risk Bernstein itself warns about for 2027-28 arrives inside the forecast period; at 6 years it does not.**

### D4. 🔴🔴 **Bernstein's own new exhibit contradicts Bernstein's own standing bear case on CRWV customer concentration, and the note does not notice.**

| | Bernstein 07-01 (announced-deal $ tally, ~$99.4bn base) | Bernstein 09-24 (estimated expected-backlog %) |
|---|--:|--:|
| Meta | ~35% | **29%** |
| OpenAI | ~23% | **17%** |
| MSFT | ~14% | **7%** |
| Jane Street | ~6% | **6%** |
| NVDA | ~6% | **4%** |
| IBM | ~5% | **4%** |
| Anthropic | ~2% | **2%** |
| **Others** | **~9%** | **32%** |
| **Meta + MSFT ("competitors at renewal")** | **~49%** | **~36%** |

**The 07-01 note's headline was *"nearly half of CRWV's backlog comes from customers who will be full competitors at the time of renewal."* On Bernstein's own 09-24 estimates that share is ~36%, and the unnamed residual has more than tripled.** ⚠️⚠️ **BASIS WARNING, AND IT IS LOAD-BEARING: these are different measurements — announced-deal dollars against a 1Q26 backlog versus an estimated forward "expected backlog" in percent, on a denominator that has grown. The DIRECTION (diversification, named-share falling) is adopted; the MAGNITUDE is not.** ➤ **Resolve off the 10-Q customer-concentration disclosure. If the direction holds, the concentration leg of the Underperform has materially weakened while the target went the other way.**

### D5. ⚠️ **MS models OKTA's dollar net retention flat at 94.0% for four straight years — the arithmetic opposite of this wiki's own bull test.**

MS Key Earnings Inputs: DNR **94.0% in Jan-26A, Jan-27e, Jan-28e and Jan-29e** — no expansion modelled at all. [[OKTA]]'s `## Catalysts` carries the house bogey **"NRR ≥107% and holding"**, and the page calls the Q1 inflection "the first in four years". ⚠️⚠️ **THESE ARE NOT THE SAME SERIES AND ARE NOT NETTED: MS's 94% is its own ModelWare dollar-net-retention construction; the 107% is the company-reported dollar-based net retention rate. There is no BBG consensus line for either.** ➤ **What is reconcilable is the SHAPE, and it is opposite: MS reaches consensus revenue (C2) while assuming zero net expansion, which means its growth comes entirely from new logos and pricing. If the page's ≥107% test passes, MS's revenue line is too low; if MS is right, the page's bull test is measuring something that does not flow through to the model.** Worth resolving before the Q3 FY27 print (~2026-12-02).

### D6. ⚠️ **A stale peer bar that would mis-rank the neocloud cohort — not adopted.**

Bernstein Exhibit 2 shows **CRWV at 1,500MW active + 3,700MW contracted = "5,200MW"**. Both legs are the **end-Q2 vintage** already on [[CRWV]]; the page also carries **4.2GW as of early August** (JPM / Barclays / DB). Further, the page records 3.7GW as *total contracted power*, which conventionally **includes** the active base — in which case the 5,200MW total **double-counts 1.5GW**. ➤ **The exhibit ranks Nscale / CRWV / NBIS / IREN on this basis, so the ranking inherits the error. Nothing from Exhibit 2 was adopted for CRWV.** Nscale's own bar (55 + 1,315 = 1,370MW) matches its S-1 and is fine.

---

## 📌 Carried forward — third-party estimates with no baseline to check against

These are logged on their pages with the estimate flagged as such. **None is adopted as fact; each is listed here so the next run knows it is unverified, not confirmed.**

- **NBIS expected backlog: MSFT 49% / META 38% / Others 14%** (Bernstein estimate). Would make two hyperscale counterparties ~87% of the book — *more* concentrated than the CRWV structure Bernstein has been bearish on since 07-01. **Bernstein does not cover NBIS, shows no workings, and NBIS has not disclosed this.** → chase the company disclosure.
- **Anthropic ≈ 43% of Nscale's expected backlog and ≈ 2% of CRWV's** (Bernstein estimate). Consistent in shape with what [[ANTHROPIC]] already holds, but does not close that page's standing hole (~85% of the $517bn headline still has no named, sized counterparty).
- **NVIDIA's six simultaneous roles at Nscale** — $400M Series B, $777M Series C, $1.2B reserved-capacity commitment, ≥$3.1B subscription incl. a contemplated $1.0B convertible/non-voting issuance, up to $860M Texas guarantee, 9.5M warrants at $0.01. **Filed figures, so not estimates — but the guarantee and warrants were already on [[NVDA]] from the Ionic Digital S-1 at $860.3M and "$60M of Nscale warrants".** The two descriptions of the warrants (by value vs by count) reconcile only at ~$6.3/share of implied Nscale equity value; **that arithmetic is ours, is stated by neither source, and is not adopted.**
- **Bernstein's two-bucket test** — separating *independently financed* demand from demand *enabled by NVIDIA's equity, supply, guarantee and financing*. **No source in this corpus has applied it to NVDA's revenue in aggregate.** Flagged on [[NVDA]] as the right frame for the backstop-universe question and currently unanswered.

---

## Method notes

- **Every exhibit value above was read from a rendered page image (170 dpi), not from the PDF text layer.** `pdfplumber` returned Bernstein's Exhibits 2, 9 and 11-14 as unordered runs of bare numbers with their labels detached — the backlog-concentration pies came out as a bare percentage sequence with no owner. Exhibit 8 is a genuine table and extracted correctly.
- **Both sources' company routing was verified by byte offset against the disclosure appendix.** The OKTA note's nine router-proposed tickers are all coverage-roster artifacts (zero body mentions); the note's actual subject was never proposed. Details in `_inbox/_ingest-log.md`.
- **BBG was live.** No column in this report is marked PENDING.
