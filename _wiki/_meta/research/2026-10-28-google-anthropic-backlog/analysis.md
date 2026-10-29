# Google backlog attributable to Anthropic — evidence reconciliation

Recorded 2026-10-28, morning São Paulo, before Alphabet's 3Q26 results. All amounts USD billions unless stated. Research answer, not a new company forecast.

**Exact current customer-level RPO is not disclosed. The historical public proxy is about $200bn / 40%: $200bn was 43.3% of March Cloud RPO, and would be 38.9% of June Cloud RPO if the numerator remained unchanged. The October S-1 establishes a Google-specific minimum contractual commitment of $114.5bn, but does not reconcile it to Google's quarter-end remaining backlog.**

The direct-contract floor, indirect hardware demand, and conditional future TPU procurement must be kept separate. The S-1 does not establish a current concentration range of 22–51%; those endpoints would combine incompatible scopes and dates.

| Evidence / input | Amount | Grounding and what it means |
|---|---:|---|
| Alphabet 1Q26 10-Q, filed 2026-04-30, Note 2 | Cloud 462.3; total Alphabet 467.6 | HARD reported remaining obligations at March 31. |
| The Information, Sri Muppidi / Erin Woo / Amir Efrati, 2026-05-05 | About 200 over five years beginning 2027 | PARTIAL as an economic commitment: press reporting from a person familiar with the arrangement; reported as more than 40% of the backlog announced with 1Q. The complete emailed newsletter/excerpt was read, not the full paywalled article. |
| Alphabet 2Q26 10-Q, filed 2026-07-23, Note 2 | Cloud 513.9; total Alphabet 519.5 | HARD reported remaining obligations at June 30. Cloud rounds to 514 in management remarks. |
| Barclays / Ross Sandler, 2026-07-24, *Unpacking TPU-As-A-Service*, p.6 | Around 88 of TPU revenue in 2Q backlog | HARD transcription of a broker estimate; PARTIAL attribution to any particular customer. Not an Anthropic-only disclosure. |
| Jefferies / Brent Thill et al., September deck priced 2026-09-02, p.34 | Frontier-lab deals 200; other RPO 320; total 520; mix 38% | HARD transcription of a broker construction. The category is frontier-lab deals, not explicitly Anthropic alone. Total approximately matches Alphabet-wide 519.5, not Cloud-only 513.9. This does not independently verify the original contract. |
| Anthropic S-1, filed 2026-10-26, p.171 | Google minimum approximately 114.5 | HARD contractual figure: April 2026–July 2033; March agreement amended May–August. Pay regardless of usage, with true-up and specified exceptions; non-cancelable except Google's uncured material breach. Not identified as the unpaid June balance. |
| Same S-1, p.171 | Additional TPU estimated payments 125–150 | PARTIAL dollar range, estimated by Anthropic: providers **including Google**, not exclusively Google; delivery 2028–31; capacity/deployment/pricing conditions; outside the contractual-commitments table. |
| Same S-1, pp.172–173 | Broadcom equipment lease rent 161.2, excluding interest | HARD aggregate lease figure. Five-year finance leases, parent-guaranteed through Anthropic subsidiaries; some capacity began coming online in 2026, additional capacity expected from 2027. Anthropic's lease payments are not automatically Google's sales price or remaining RPO. |

**Arithmetic and interpretation.** The anchor is reported quarter-end RPO. No conversion coefficient or assumed consumption rate is needed or fitted.

1. Historical March comparison: 200 / 462.3 × 100 = **43.26%**. This explains the contemporary “more than 40%” headline.
2. Holding that old reported amount unchanged: 200 / 513.9 × 100 = **38.92%** against June Cloud RPO. This is a scale proxy, not an updated customer balance.
3. Using total Alphabet instead: 200 / 519.5 × 100 = **38.50%**. Jefferies' rounded 200 / 520 = **38.46%**, consistent with its displayed 38%.
4. The S-1 minimum relative to June Cloud RPO: 114.5 / 513.9 × 100 = **22.28%**. This is only a cross-date scale comparison. It is **not** proof of a 22.3% minimum backlog share.
5. Sensitivity: each $10bn change in the unknown Anthropic-attributable remaining numerator changes the June Cloud comparison by **1.95 percentage points**. The evidence does not calibrate an uncertainty band for that numerator.

**What Google itself confirms.** CFO Anat Ashkenazi on 2026-04-29 and 2026-07-22 says signed TPU-system agreements enter Cloud backlog, alongside GCP agreements. On the July call she says the vast majority is GCP; hardware revenue starts as systems are delivered, with a small amount in Q2 and the bulk of that agreement in 2027. This is a product split, not a customer split: Anthropic can buy GCP services as well as use TPUs bought through other entities. “Mostly GCP” does not mean “mostly non-Anthropic.” The Q2 10-Q defines RPO as revenue not yet recognized and excludes cancellable contracts and certain payments to customers. Recognition also depends on delivery and service consumption. No Anthropic-specific remaining balance is supplied in the passages reviewed.

**The supplier chain explains why $114.5bn is not the whole economic exposure.** Google's own 2026-04-06 announcement says the expansion comes through both Google Cloud services and Google-built TPUs supplied through Broadcom. Barclays' July 24 pp.2–3 model has an SPV buy Google TPUs and lease capacity to Anthropic. Anthropic's S-1 names Broadcom as equipment lessor. A legal customer such as Broadcom/SPV can therefore sit between Google and the ultimate user. Google's aggregate RPO can contain hardware orders whose economic demand depends on Anthropic without naming Anthropic as the customer. There is no disclosed bridge quantifying that indirect portion.

The FT / Ryan McMorrow, 2026-08-04, *Inside Google's $200bn Wall Street finance machine for Anthropic*, provides a separate financing view. The archived pages 1–4 describe about $200bn of interlocking contracts, roughly four-fifths tied to chips; a $35bn first hardware purchase through Compute SPV in June; and about $128bn of Broadcom purchase commitments reportedly relating almost entirely to a further Google TPU hardware leg. These are financing/programme and hardware-purchase bases. The FT's $200bn is not a second $200bn Google Cloud service commitment and cannot be added to the May headline. Nor does the first hardware transfer by itself establish Google's revenue-recognition or remaining-RPO amount.

**Broker and email provenance.** The May 6 full email bodies show one underlying report propagating across desks:

| Source/date | Evidence contribution |
|---|---|
| BofA / Justin Post, relayed in Claudio Franco's one-liners, 2026-05-06 | Says the deal was **likely** included in Q1 backlog; explicitly flags questions about the TPU sales component. Analyst inference. |
| JPM / Mark Schilsky, 2026-05-06 | Treats the news as apparently already in backlog, hence not incremental. Desk interpretation. |
| Morgan Stanley / Thomas Wigg, Goldman / Peter Bartlett, Jefferies / Jeffrey Favuzza, 2026-05-06 | Repeat the approximately $200bn / >40% press report. No independent confirmation. |
| Jefferies / Brent Thill, 2026-09-02 | Later 38% frontier-lab chart, visually checked; not an audited Anthropic customer balance. |
| FUNDA, *ANT: S-1 Review and First-Cut EPS Model*, dated 2026-10-26, received 2026-10-27 | Separates direct GCP commitment and Broadcom lease route. Its gross Google hardware-sales treatment is expressly the author's view; the S-1 does not add supplier accounting confirmation. |
| October broker checks, 2026-10-07–27 | Selected full bodies on Google previews, Anthropic and financing supplied no replacement customer-level RPO bridge. This is a targeted search, not certification of every email in the mailbox. |

**Combinations rejected.** Do not add 200 + 114.5; do not add 88 to 200; do not infer a reconciliation from 114.5 + 88 being close to 200. Do not assign all 125–150 to Google. Do not add Broadcom lease rent, SPV debt proceeds, credit backstops or Google equity funding to Google's revenue backlog. These measure different counterparties, recognition dates and financial claims. The S-1's additional TPU estimate is a conditional procurement disclosure with an unresolved dollar amount, not simply an optional/non-binding purchase plan.

**What would establish the current answer.** The missing disclosure is a quarter-end reconciliation of (a) direct Anthropic GCP RPO, (b) remaining Google hardware RPO to Broadcom/SPVs for Anthropic, (c) overlap with the historical $200bn, (d) revenue already recognized and post-quarter amendments, and (e) the Google allocation of the 2028–31 conditional TPU arrangements. Updating the total denominator alone cannot resolve these.

**Validation: PARTIAL.** The independent double-check passed the arithmetic and source numbers, but rejected a current “Anthropic is 40%” claim. Timing and customer-allocation guardrails remain unresolved. This is a verified historical proxy and a documented contract stack, not a precise current concentration model. See [calculations](calculations.json) and [audit](audit.md).

**Source access and archive.** Graph context, GOOG and ANTHROPIC Debate/Changelog sections, the compute-deal timeline, full-corpus FTS, official Q1/Q2 filings, relevant earnings passages, the S-1 contractual sections, broker report images, and 21 selected full email bodies were inspected. The Information item is a newsletter excerpt; keyword result lists are not represented as full reads. Saved emails: [May/S-1 source set](outlook-sources.json), [October checks](outlook-october-checks.json).

- [Alphabet Q1 10-Q, 2026-04-30](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000048/goog-20260331.htm).
- [Alphabet Q2 10-Q, 2026-07-23](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm).
- [Anthropic S-1, 2026-10-26, pp.171–173](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm).
- [Google Cloud announcement, 2026-04-06](https://www.googlecloudpresscorner.com/2026-04-06-Anthropic-Expands-Use-of-Google-Cloud-and-TPUs).
- [The Information original, 2026-05-05](https://www.theinformation.com/articles/anthropic-commits-spending-200-billion-googles-cloud-chips); [Reuters relay, 2026-05-05](https://www.streetinsider.com/Reuters/Anthropic%2Bcommits%2Bto%2Bspending%2B%24200%2Bbillion%2Bon%2BGoogles%2Bcloud%2Band%2Bchips%2C%2Bthe%2BInformation%2Breports/26435779.html).
- [Barclays, 2026-07-24](../../../../relat%C3%B3rios%20bons/Barclays_Alphabet_Inc_Unpacking_TPU_As_A_Service.html), pp.2–6.
- [Jefferies, 2026-09-02](../../../../relat%C3%B3rios%20bons/AI_Deep_Dive_Jeffries.html), p.34.
- [FT, 2026-08-04](../../../../relat%C3%B3rios%20bons/Inside_Googles_200bn_Wall_Street_finance_machine_for_Anthropic.html), archived pp.1–4 inspected.
- [Google 1Q call](../../../../GOOG/transcripts/GOOG_Q1-2026-earnings_2026-04-29.md), lines186–190; [Google 2Q call](../../../../GOOG/transcripts/GOOG_Q2-2026-earnings_2026-07-22.md), lines152–156 and248–252.
