# Adding a new source to the wiki

This is the canonical procedure for adding a document to the research wiki. The goal is not merely to store the file: it must be readable, routed correctly, incorporated with attribution, reconciled against existing views, and preserved in the audit trail.

## Quick path — what you do

1. **Obtain the complete source.** Download the actual report, transcript, filing, deck, or model—not a portal loading page, email shell, free preview, or screenshot of an unidentified exhibit.
2. **Preserve provenance.** Make sure the publisher/broker, analyst or author, publication date, and title are visible in the document or filename. For pasted text or exhibits, explicitly provide the source; it must never be inferred.
3. **Use a helpful filename.** Renaming is optional, but the preferred pattern is:

   ```text
   YYYYMMDD__SOURCE__Short title.ext
   ```

   Example: `20260902__GOOG__Capex update.pdf`. The `YYYYMMDD` filename date is the publication-date anchor and takes priority over unreliable PDF metadata.
4. **Drop the file in one of the two entry folders:**

   - Felipe/direct: `E:\Wiki Felipe empresas\_inbox\`
   - Team/shared: `P:\US Equities\Relatórios para a wiki\`

5. **Close the file after copying it.** Acrobat, Excel, Explorer preview, or another process can lock a file on `P:` and prevent the pipeline from moving it.
6. **Start processing.** Tell Codex **“process the inbox”** for an immediate run, or leave the file for the scheduled `daily-run-inbox` task at 23:00.
7. **Check completion.** A source is complete only when it appears in the relevant wiki page or theme, the raw document is preserved, the ingest/reconciliation records exist, and the file has moved to `_inbox\_done\`.

## Preferred formats

| Input | Treatment | Operator note |
|---|---|---|
| Text-layer PDF | Full text extraction, routing, and faithful page-image HTML rendering | Preferred format for research reports and decks |
| Bloomberg earnings-call PDF | Auto-files as a transcript when company, date, quarter, and text layer resolve | Otherwise falls back to the report flow with a warning |
| Scanned/image-only PDF | Page images are preserved, but routing may return zero characters | Requires OCR or visual transcription before page updates |
| `.md`, `.txt`, `.html` | Text can be routed; the base router does not create the PDF-style page render | Confirm HTML is the real document, not a portal shell |
| Direct `.docx` | Not text-extracted by the base inbox router | Export to PDF/text. The Outlook expert-call sweep is a special case and converts attached `.docx` files |
| `.xlsx` | Preserved as a reference asset but not automatically understood | Requires an explicit workbook review before numbers are used |
| Pasted text, screenshot, or exhibit | Manual source-specific ingestion | Confirm source, author, and date with the user; never guess attribution |

## What the pipeline does after the drop

### 1. Stages every inbound source

The plan command is:

```powershell
py E:\.claude\scripts\ingest_inbox.py
```

Before reading `_inbox`, it also:

- sweeps eligible expert-call forwards from Outlook for the prior three days; and
- sweeps the team `P:` drop folder into `_inbox`.

For the `P:` route, a successfully staged original is moved to `P:\US Equities\Relatórios para a wiki\done\`. A locked file remains in the drop folder for retry.

### 2. Applies duplicate and lock guards

The `P:` sweep compares candidates with prior archives by normalized filename and, where possible, content hash. Exact duplicates are skipped. A same-named file with different content is treated as a possible revision and pulled for review.

If a file is locked, the routing plan shows **STRANDED ON P:** and the command exits with code `3`. The plan for all other sources is usable, but the stranded file is **not** in the wiki. Close the locking application and rerun, or copy that file directly into `_inbox`.

Content review is still required: renamed duplicates, portal shells, disclosure-table false matches, and truncated previews may evade mechanical checks.

### 3. Extracts and preserves the source

For each readable PDF, the router:

- extracts the text used for metadata detection and routing;
- renders a faithful page-by-page HTML copy under `relatórios bons\`; and
- preserves the source so page citations can link back to it.

A recognized Bloomberg earnings-call PDF is instead converted to a dated Markdown transcript under `<TICKER>\transcripts\`. The search index then classifies it as a transcript rather than a generic report.

### 4. Detects metadata

The router proposes the publication date, broker/publisher, company tickers, and relevant cross-company themes.

Date and publisher detection are heuristics, not facts. The filename plus the beginning of the document are scanned, so disclosure pages, stale dates, or another broker named in the text can create a false label.

### 5. Builds a routing proposal

The output is `_inbox\_routing-plan.md`. A company is normally proposed when its alias appears in the filename or at least three times in the extracted text. A theme is proposed after repeated keyword matches.

The plan **does not edit company or theme pages**. It is a candidate map for review.

### 6. Verifies the document and every route

Before writing anything, the reviewer inspects the content and confirms:

- the source is complete and readable;
- publisher, analyst/author, title, and publication date;
- primary source vs sell-side research vs journalism vs independent research;
- whether it is new, a duplicate, a revision, stale historical context, off-coverage, or only a reference asset;
- which company mentions are substantive rather than disclosures, footers, URL chrome, comparables tables, or ambiguous aliases; and
- which themes are genuinely addressed rather than triggered by polysemy.

Routes may be removed or added after this review. No route should be accepted solely because the keyword count is high.

### 7. Patches the research pages with attribution

Net-new information is inserted into `_wiki\<TICKER>.md` and `_wiki\themes\<theme>.md`. Each datapoint carries:

```text
source/broker · analyst or speaker · publication/call date
```

A raw-source link is added to `## Sources` when useful. Old research can be dated historical context, but it must not displace a newer current mark.

The thesis-drift rule always applies: a superseded number, rating, price target, estimate, or thesis is moved to `## Changelog` with its date before the current body is updated. Nothing material is silently overwritten.

If the source resolves a logged catalyst, its result is recorded in `_wiki\_meta\outcomes.md` as `bull won`, `bear won`, or `neutral` with an explanation.

### 8. Reconciles the new information

**Standing compute-deal timeline rule (user request, 2026-09-23):** whenever an ingested source contains a compute agreement or a subsequent confirmation, amendment, financing milestone, delay, cancellation or delivery, update [AI compute deals — announcements and confirmations](../themes/ai-compute-deals.md). This applies across companies, including inbox, email, newsletter, transcript, filing and manual-exhibit updates. Match the existing deal ID before adding an event. Keep the original announcement and add later evidence under that ID; distinguish event date, publication date and recorded date, and separate contract evidence from financing/delivery. A repeat of the same report is not independent confirmation or incremental capacity. Reconcile the company pages, preserve superseded terms in their Changelogs and apply the timeline's source/basis rules.

Every material datapoint is compared with:

- the prior wiki view and debate;
- Capstone house-model figures, when present;
- Bloomberg consensus, live or cached; and
- canonical cross-company assumptions in `_wiki\_meta\assumptions.md`.

The result is recorded in `_wiki\_meta\reconciliation-YYYY-MM-DD.md`. If Bloomberg is unavailable, the comparison is marked `PENDING`; it is not replaced with an uncited web number. Basis differences remain explicit—for example, facility GW, IT-load GW, and 800V-subset GW are never mixed.

### 9. Archives only after successful incorporation

After all files in the reviewed plan have been classified and any required page updates are complete, run:

```powershell
py E:\.claude\scripts\ingest_inbox.py --archive
```

This moves processed top-level files or folders to `_inbox\_done\` and appends the archive event to `_inbox\_ingest-log.md`. Do not run `--archive` against an inbox containing files that arrived after the reviewed plan; it archives the whole current inbox, not only a selected manifest.

Pipeline control files such as `_expert_calls_seen.json` and `PENDING_FULL_REPORTS.md` are not research sources and must remain available to their owning workflow.

### 10. Rebuilds derived outputs and records the run

The full run rebuilds the wiki HTML, reports index, timelines, search index, graph, dashboards, diff, coverage, catalysts, assumptions, and other derived features. Page edits, reconciliation, and generated artifacts are committed to git.

The 23:00 inbox task commits but does not normally push. The next scheduled 18:15 refresh pushes the repository if there are changes. The local `E:` wiki updates immediately; team/public mirrors may lag until their scheduled sync or push.

## Completion checklist

A source is fully ingested only when all applicable checks are true:

- [ ] Full document captured; no portal shell, truncated preview, or unidentified exhibit
- [ ] Publisher/broker, analyst/author, title, and publication date verified
- [ ] Duplicate/revision status checked by content, not only filename
- [ ] Correct company and theme routes verified from substance
- [ ] New datapoints added with source and date attribution
- [ ] Superseded views preserved in `## Changelog`
- [ ] Relevant compute-deal announcements or subsequent milestones appended to `themes/ai-compute-deals.md`, with existing deal IDs checked and duplicate/overlap treatment recorded
- [ ] Relevant catalyst outcome recorded
- [ ] Reconciliation completed or Bloomberg explicitly marked `PENDING`
- [ ] Raw source/link preserved
- [ ] Source archived under `_inbox\_done\`
- [ ] `_inbox\_ingest-log.md` updated
- [ ] Derived wiki/search/dashboard outputs rebuilt
- [ ] Git commit created without absorbing unrelated working-tree changes

## Where to inspect the result

| Artifact | Purpose |
|---|---|
| `_inbox\_routing-plan.md` | Automated metadata and routing proposal |
| `_wiki\<TICKER>.md` | Company synthesis updated from the source |
| `_wiki\themes\<theme>.md` | Cross-company thematic read-through |
| `relatórios bons\` or `<TICKER>\transcripts\` | Readable raw-source representation |
| `_wiki\_meta\reconciliation-YYYY-MM-DD.md` | New-vs-prior/house/consensus comparison |
| `_inbox\_ingest-log.md` | Audit record of what was ingested, dropped, corrected, or left open |
| `_inbox\_done\` | Archived inbound files |

## Common exceptions

| Symptom | Meaning | Action |
|---|---|---|
| `STRANDED ON P:` / exit code `3` | One or more originals are locked and absent from the plan | Close Acrobat/Excel/Explorer preview, then rerun or stage directly in `_inbox` |
| `0 chars` from a PDF | Image-only scan, broken text layer, or container file | OCR/transcribe visually; do not rely on automatic routes |
| `0 chars` from `.docx`/`.xlsx` | Base router does not parse that direct format | Export to PDF/text or perform an explicit document/workbook review |
| Many implausible ticker hits | Disclosures, footers, coverage tables, URL chrome, or alias collision | Read the body and remove false routes |
| Correct report under another filename | Filename dedup may miss it | Compare title, authors, date, page count, opening page, and content hash |
| HTML says “please wait” or mostly shows navigation | Saved portal shell, not the research document | Download the actual PDF from the authenticated viewer |
| Source is old | Historical evidence, not a current mark | Date it explicitly and do not overwrite newer ratings, targets, or thesis state |
| Bloomberg unavailable | Consensus cannot be refreshed live | Use the dated cached baseline if valid and mark unresolved comparisons `PENDING` |
