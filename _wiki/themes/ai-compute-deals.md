# AI compute deals — announcements and confirmations

_Created 2026-09-23 · rolling cross-company record · updated when relevant sources are ingested. Seed coverage: Anthropic's supplied compute-lineup exhibit and Nscale's later filing. This is not yet a complete historical inventory across all companies._

Track when a deal first becomes public, what its original terms were, and what subsequent evidence establishes. Keep the original announcement and later confirmations, amendments, financing milestones, delays, cancellations and deliveries under the **same deal ID**. A confirmation adds evidence to an existing deal; only an explicitly incremental commitment adds new capacity or value.

Related pages: [Anthropic](../ANTHROPIC.md) · [Nscale](../NSCALE.md) · [Hyperscaler capex](hyperscaler-capex.md) · [AI datacenter power](ai-datacenter-power.md).

## Reading the timeline

- **Event date** is the announcement/reporting or milestone date, at the precision supplied by the source. **Source date** is when the evidence was published. **Recorded date** is when it entered this timeline. Keep all three distinct; a filing can disclose an earlier signing date.
- **Evidence** can be press-reported, company-announced, or confirmed by a filing/contract. Record disagreements explicitly. A repeated headline or broker relay of the same article is not an independent confirmation.
- **Execution** is tracked separately: financing pending/secured, construction, delivery, service commencement, delay or cancellation. A signed agreement does not establish funding or delivery. An expected first-capacity date remains a forecast until supported by delivery evidence.
- Amounts retain their currency, term and basis: ceiling versus firm commitment, contract value versus annual spend or capex. Capacity retains its stated basis: facility MW, IT MW, accelerator count or undisclosed. Unknown terms stay unknown; overlapping cloud, silicon, site and financing announcements are not summed.

## Original announcement timeline

**Source for every seed row: S1**, The Information exhibit supplied by the user as "the info"; printed update **"Sept. 13"**, year unprinted/unconfirmed. **Recorded 2026-09-23.** Event dates below are the exhibit's **"Date Announced/Reported"** field, not independently established first-publication dates. The reported terms are preserved as the original source vintage; later changes appear in the next section. All seed rows initially carry **press-reported** evidence status in this tracker; this does not imply that no other confirmation exists in the wider wiki.

| Event date | Deal ID | Buyer | Counterparty | Original amount | Original capacity | Expected first capacity | Source |
|---|---|---|---|---|---|---|---|
| 2025-10-23 | ANTH-GOOG-20251023 | Anthropic | Google Cloud | Tens of billions | 1,000 MW; basis unspecified | 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2025-11-12 | ANTH-FLUIDSTACK-20251112 | Anthropic | Fluidstack | $50B | Undisclosed | 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2025-11-18 | ANTH-AZURE-NVDA-20251118 | Anthropic | Microsoft Azure/Nvidia | $30B | 1,000 MW; basis unspecified | Undisclosed | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-04-10 | ANTH-CRWV-20260410 | Anthropic | CoreWeave | Multi-billion | Undisclosed | 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-04-20 | ANTH-AWS-20260420 | Anthropic | Amazon AWS | $100B | 5,000 MW; basis unspecified | 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-04-24 | ANTH-GOOG-20260424 | Anthropic | Google | $200B | 5,000 MW; basis unspecified | Undisclosed | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-05-06 | ANTH-SPCX-20260506 | Anthropic | SpaceX | $45B | 300 MW; basis unspecified | May 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-05-07 | ANTH-AKAM-20260507 | Anthropic | Akamai | $1.8B | Undisclosed | Undisclosed | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-07-22 | ANTH-AMD-20260722 | Anthropic | AMD | Undisclosed | 2,000 MW; basis unspecified | H1 2027 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-08-04 | ANTH-VOLTA-20260804 | Anthropic | Volta Infra | $10B | 121 MW; basis unspecified | Dec. 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-08-23 | ANTH-RUM-20260823 | Anthropic | Rum Group | $13.7B | 120-180 MW; basis unspecified | Late 2026 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-08-26 | ANTH-NSCALE-20260826 | Anthropic | Nscale | $45B | 460 MW; basis unspecified | Q4 2027 | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |
| 2026-08-31 | ANTH-LAMBDA-20260831 | Anthropic | Lambda | $35B | Undisclosed | Undisclosed | [S1](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md) |

The two Google rows remain distinct source entries; whether they overlap is unresolved here. Contract durations are not supplied by S1. No total or annualized value is calculated from this table.

## Confirmations, revisions and execution history

Append a dated event whenever the evidence or terms change, referencing the existing deal ID. Preserve the prior value in the event description and the affected company's Changelog. Historical evidence found later is a **backfill**, with its original source date and today's recorded date.

| Event date | Recorded date | Deal ID | Event / evidence | What changed or was established | Execution status / remaining question | Source |
|---|---|---|---|---|---|---|
| 2026-09-18 | 2026-09-23 | ANTH-NSCALE-20260826 | Filing confirmation; historical backfill | S1's reported **$45B** is refined to **up to approximately $44.6bn** in the S-1. Agreements were **signed 2026-08-25**, distinct from the exhibit's **2026-08-26** announcement/reporting date. Four agreements with Nscale subsidiaries for dedicated GPU infrastructure at Monarch, supporting **NVIDIA Vera Rubin NVL72**. The Facilities table identifies a US-owned **460 MW IT** contracted site; its mapping to Monarch is the existing wiki's inference, not a site name printed in that row. | **Contract confirmed; financing still pending as of the filing.** No binding financing commitments for performance under the Anthropic agreements. S1's **Q4 2027** first-capacity forecast remains attributed to S1 and is not upgraded to delivery evidence. | [S2](../../NSCALE/NSCALE_S-1_2026-09-18_0001193125-26-395475.html), [S3](../../NSCALE/S-1_exhibits/ck0002110365-ex10_25.htm); site mapping: [Nscale wiki](../NSCALE.md) |

## Current follow-up points

- **ANTH-NSCALE-20260826:** seek evidence of qualifying financing and service commencement. The later filing takes precedence for contract value; it does not establish that the original capacity forecast has been delivered.
- **Other seed deals:** attach any primary confirmation already on disk or found during subsequent source reviews. Do not treat an unreviewed contract as cancelled or unconfirmed merely because this tracker is newly seeded.
- **All companies:** add new deals from future ingests, and backfill existing coverage as it is reviewed. Explicitly identify related/overlapping commitments before treating an expansion as incremental.

## Update procedure

1. Search this page and the buyer/supplier pages before creating a deal ID. Match counterparties, site, tranche and contract scope; company-name matches alone are insufficient. Retain the ID if a later filing changes the reported signing date or legal counterparty name.
2. For a new deal, append its original announcement row with the source date, recorded date and link. The shared seed metadata above applies only to the initial S1 rows; subsequent rows must state their own provenance. Preserve date precision; never invent a day for a month-only disclosure.
3. For a confirmation, amendment, financing event, delay, cancellation or delivery, append to the history using the same ID. State the old and new terms, the exact increment if disclosed, the source's evidence level and the execution status. Link related tranches instead of double-counting them.
4. Cite publisher/company/broker, author or speaker when available, publication date and archived original. Mark relay chains and independent corroboration separately. A source repeating its own earlier report adds no new confirmation event unless it supplies material new terms.
5. Reconcile the relevant company pages and preserve superseded values in their Changelogs. Update the theme Changelog. If the event resolves a tracked catalyst, record the outcome in `_wiki/_meta/outcomes.md` under the existing rules.
6. Refresh search and the offline wiki view after edits. Preserve the immutable source exhibits; changes belong in this timeline and the company synthesis.

## Sources

- **S1 — The Information, "Anthropic's Compute Lineup"**, source identified by the user as "the info"; received **2026-09-23**. Printed update **"Sept. 13"**, year not printed; author/article URL not shown. [Original screenshot](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.png) · [Transcription and provenance](../_data/figures/2026-09-23_ANTHROPIC_Compute_Lineup_user_exhibit.md). Announcement dates and original amounts/capacities above are transcribed from this exhibit.
- **S2 — Nscale Limited S-1, filed 2026-09-18**, accession **0001193125-26-395475**. Reviewed relevant sections on Anthropic Services Agreements, financing risk, and Facilities for this timeline. [Archived filing](../../NSCALE/NSCALE_S-1_2026-09-18_0001193125-26-395475.html).
- **S3 — Nscale S-1 exhibit 10.25, "Order for GPU Services", filed 2026-09-18**. Dedicated single-tenant GPU services, four-tranche agreement structure and qualifying-financing terms. [Archived contract](../../NSCALE/S-1_exhibits/ck0002110365-ex10_25.htm).

## Changelog

- **2026-09-23 — Created at the user's request for a general, continuously maintained announcement/confirmation timeline.** Seeded the original Anthropic exhibit and backfilled Nscale's later filing confirmation under the same deal ID. The $45B press vintage remains in the original row; the up-to-$44.6bn filed ceiling appears as a subsequent event. Added a standing rule to the repository instructions and source-ingestion procedure. Initial coverage is explicitly partial; no claim of a complete cross-company backfill.
