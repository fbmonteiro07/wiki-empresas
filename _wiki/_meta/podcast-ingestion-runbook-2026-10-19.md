# Repeatable scoped podcast ingestion — 2026-10-19

Use the existing run-inbox workflow with an explicit manifest of authorized original summaries. This runbook creates no schedule and changes no code/configuration.

1. Stage only the authorized originals in a local batch `_inbox`. Record canonical episode URL/ID, publication date, content hash, review scope and transcript/license limitations. Treat short/expanded versions and clips of the same episode as one evidence unit. Preserve earlier versions.
2. Run the existing router with its supported root override; this suppresses Outlook and P: sweeps:

```powershell
$env:WIKI_INGEST_ROOT = '<local batch root containing _inbox and the relevant _wiki page names>'
py -3 'E:\.claude\scripts\ingest_inbox.py'
Remove-Item Env:\WIKI_INGEST_ROOT
```

3. Review source dates and routing manually. The router can select a review date from the text and misses thematic relationships. Markdown inputs receive text routing only, so create faithful HTML summary representations in `relatórios bons`, label them SUMMARY in its catalog, and keep the supplied body recoverable exactly. Do not label these records transcripts.
4. Read prior company/theme evidence and add attributed analysis, source links and changelogs. Compare the same speaker with dated earlier material; distinguish a revised assumption from a measured result. Reconcile applicable marks against house/BBG on matching definitions. Do not advance global sources-through dates for a podcast-only batch.
5. Obtain the workflow's independent source verifier review. Run `transcript_qa.py --diff` before committing. Preserve primary-access and attribution gaps; use unverified reports only for explicitly labeled original analytical questions.
6. Check each destination's current hash before the additive write. Archive only manifest-listed files to a dedicated `_inbox/_done` folder, retaining names and hashes. The standard `--archive` scans the whole inbox, so it is not suitable while unrelated files remain. Log eight canonical sources separately from five initial-summary ancestors in this batch.
7. Rebuild the existing local wiki HTML, report catalog, search database and graph. Rebuild timelines only if relevant to the existing local renderer; modelled capacity or repeat commentary does not create a new compute-deal event. Do not run live price refreshes, Outlook sends, mail sweeps, cloud uploads or new schedules.
8. Verify source-body fidelity, local link targets, substantive page incorporation, catalogue uniqueness and search hits. Commit only the scoped changes, preserving pre-existing work. Record actual results and blockers in the ingestion ledger rather than treating a copied inbox file as ingested.

This batch's evidence is in `podcast-ingestion-2026-10-19.json`; the reviewed routing and reconciliation are adjacent. Primary episode links remain in the source reports. The routine is manual and repeatable; daily digest scheduling belongs to the separate authorized main-thread workflow.
