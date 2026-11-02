# Financials — source coverage and remaining gaps

_Recorded 2026-11-01; MSCI, EFX and TRU added 2026-11-02, then CME, ICE, CBOE, NDAQ, OWL and BLK the same day. Derived from local ingestion manifests and file/hash checks; not a claim that all archived pages were read._

**Archive totals:** 411 SEC filings; 181 transcript documents covering 173 distinct issuer-quarter calls; 107 earnings exhibits; 450 company-commentary entries from 332 distinct emails. Cached/live versions and cross-company copies can appear as separate documents; identities are deduplicated for the email count.

[Financials overview](../themes/financials.md) · [Machine-readable coverage](../_data/financials/coverage.json) · [Complete source/provenance ledger](../_data/financials/source_inventory.json)

| Ticker | SEC | Transcript documents / distinct quarters | Earnings exhibits | Commentary candidates | Latest 10-Q period / filing | Inventory |
|---|---:|---:|---:|---:|---|---|
| [JPM](../JPM.md) | 20 | 11 / 10 | 8 | 9 | 2026-06-30 / 2026-08-06 | [Sources](../_dashboards/financials-sources.html#JPM) |
| [SPGI](../SPGI.md) | 20 | 8 / 8 | 4 | 19 | 2026-09-30 / 2026-10-28 | [Sources](../_dashboards/financials-sources.html#SPGI) |
| [MCO](../MCO.md) | 20 | 8 / 8 | 4 | 10 | 2026-09-30 / 2026-10-21 | [Sources](../_dashboards/financials-sources.html#MCO) |
| [BX](../BX.md) | 20 | 8 / 8 | 4 | 22 | 2026-06-30 / 2026-08-07 | [Sources](../_dashboards/financials-sources.html#BX) |
| [KKR](../KKR.md) | 20 | 9 / 8 | 3 | 16 | 2026-06-30 / 2026-08-06 | [Sources](../_dashboards/financials-sources.html#KKR) |
| [GS](../GS.md) | 21 | 8 / 8 | 8 | 6 | 2026-06-30 / 2026-08-03 | [Sources](../_dashboards/financials-sources.html#GS) |
| [V](../V.md) | 20 | 8 / 8 | 4 | 56 | 2026-06-30 / 2026-07-29 | [Sources](../_dashboards/financials-sources.html#V) |
| [MA](../MA.md) | 20 | 9 / 9 | 4 | 32 | 2026-09-30 / 2026-10-29 | [Sources](../_dashboards/financials-sources.html#MA) |
| [APO](../APO.md) | 20 | 23 / 18 | 6 | 12 | 2026-06-30 / 2026-08-10 | [Sources](../_dashboards/financials-sources.html#APO) |
| [HOOD](../HOOD.md) | 21 | 8 / 8 | 6 | 100 | 2026-09-30 / 2026-10-28 | [Sources](../_dashboards/financials-sources.html#HOOD) |
| [COIN](../COIN.md) | 21 | 9 / 8 | 4 | 52 | 2026-09-30 / 2026-10-29 | [Sources](../_dashboards/financials-sources.html#COIN) |
| [MSCI](../MSCI.md) | 20 | 8 / 8 | 4 | 10 | 2026-09-30 / 2026-10-20 | [Sources](../_dashboards/financials-sources.html#MSCI) |
| [EFX](../EFX.md) | 20 | 8 / 8 | 4 | 20 | 2026-09-30 / 2026-10-20 | [Sources](../_dashboards/financials-sources.html#EFX) |
| [TRU](../TRU.md) | 21 | 8 / 8 | 8 | 14 | 2026-09-30 / 2026-10-27 | [Sources](../_dashboards/financials-sources.html#TRU) |
| [CME](../CME.md) | 21 | 8 / 8 | 4 | 19 | 2026-09-30 / 2026-10-23 | [Sources](../_dashboards/financials-sources.html#CME) |
| [ICE](../ICE.md) | 24 | 8 / 8 | 4 | 14 | 2026-09-30 / 2026-10-29 | [Sources](../_dashboards/financials-sources.html#ICE) |
| [CBOE](../CBOE.md) | 20 | 8 / 8 | 4 | 10 | 2026-09-30 / 2026-10-30 | [Sources](../_dashboards/financials-sources.html#CBOE) |
| [NDAQ](../NDAQ.md) | 21 | 8 / 8 | 8 | 14 | 2026-09-30 / 2026-10-22 | [Sources](../_dashboards/financials-sources.html#NDAQ) |
| [OWL](../OWL.md) | 21 | 8 / 8 | 8 | 10 | 2026-09-30 / 2026-10-30 | [Sources](../_dashboards/financials-sources.html#OWL) |
| [BLK](../BLK.md) | 20 | 8 / 8 | 8 | 5 | 2026-06-30 / 2026-08-06 | [Sources](../_dashboards/financials-sources.html#BLK) |

## What the counts mean

- SEC: original 10-K, 10-Q and amendments filed within 2021-10-31–2026-10-31 (through 2026-11-02 for the nine names added that day), including two separately identified Apollo predecessor filings and twelve BlackRock filings from its pre-reorganization registrant. Source dates, fiscal periods, accessions, original URLs and hashes are preserved.
- Calls: at least the latest eight reported quarters per issuer; duplicate company/third-party copies and Coinbase prepared remarks are counted as documents but not extra quarters. Apollo has company-hosted history back to Q1 2022.
- Earnings: SEC-filed 2026 releases and supplements; multiple exhibits can belong to one result.
- Commentary: subject-screened cached candidates plus 33 selected live Outlook messages reviewed on 2026-11-01 (36 company-specific copies). The old collection truncated long bodies. The live collection preserves the connector-returned body, but neither guarantees the linked report was obtained. False matches and invitations are preserved under _discovery and excluded. This was a targeted 2026 year-to-date search; pagination remains available for broader historical review. The nine names added 2026-11-02 (MSCI, EFX, TRU, CME, ICE, CBOE, NDAQ, OWL, BLK) rest on cached excerpts: the Outlook desktop body export stalled that day, so their live reads are cited on the pages as Outlook links rather than archived.
- Reviewed: the synthesis uses the latest result, selected guidance/Q&A, historical management context, relevant filing disclosures and identified sell-side commentary. Cited/selected-passage status is recorded separately from mere availability. [Passage-emission log](../_data/financials/review_passages.jsonl) is a navigation aid, not proof of full-document review.

## Live email review audit

[Queries, selection and pagination](../_data/financials/email_review_2026-11-01/search_audit.json) and [live source manifest](../_data/financials/live_email_manifest.json) preserve the audit trail. Canonical matches to older cached messages use sender, normalized subject and received date within one day; report dates and received UTC timestamps are separate. Goldman HOOD/COIN result alerts remain headline-only. The Redburn prediction-market volume conflict is flagged rather than adopted.

## Open items

- Bloomberg consensus: resolved 2026-11-02. All 20 issuers were pulled from the local terminal into `estimates.json`. The CY lines take reported quarters from back-period BEst values from Bloomberg, which can differ from reported results (GS CY26 EPS $59.53 vs FY26 consensus $71.75), so cite the FY lines. Matched-basis valuation models and house targets are still open. (Was, 2026-11-01: none of these issuers was in the estimates cache because the terminal connection timed out.)
- Q3 releases for APO (November 3) and KKR (November 9) were future events at the cut-off.
- JPM, GS, BX and BLK have Q3 earnings releases but only Q2 10-Qs filed by this cut-off. Visa has FY2026 results but the latest filed 10-K is FY2025.
- Third-party transcript errors, inherited PDF extraction artifacts and cached-email truncation remain possible. Load-bearing current numbers were checked against the company release; original documents remain available.
- Two unsuccessful discovery URLs are retained in the manifests: an old BX MarketBeat link and a guessed Coinbase Q&A PDF. Recent-quarter coverage is complete using the other archived sources.
- Full historical reading, matched-basis valuation models and exhaustive retrieval of every past conference appearance are not claimed.

## Validation

- No missing files, hash mismatches or gaps in the latest eight quarterly-call periods were found.
