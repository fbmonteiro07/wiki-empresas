# AI credit & funding monitor

The dashboard is served from this workspace at
http://ds-cap-33:8080/wiki/_dashboards/credit-monitor.html.
Do not move this internal research to a public host.

User authorization dated 2026-09-29 supersedes the 2026-08-24 manual-only decision:
refresh weekly and email Felipe on Friday mornings. The Codex heartbeat runs Fridays
at 09:00 America/Sao_Paulo in the originating task. The workstation and Codex must
be running; Bloomberg must be signed in and Outlook must have the existing account
felipe.monteiro@capstone.com.br available. Email goes only to that same address,
with no CC/BCC. The send script validates the exact account and recipient, retains
a dispatch receipt and checks Sent Items; it does not equate submission with delivery.

## Weekly procedure

1. Read AGENTS.md. Before research, run graph_query.py for AI credit/funding,
   then read the relevant company Debate/Changelog sections, the canonical
   assumptions, and themes/ai-compute-deals.md. Search the full corpus with search.py
   for new credit trackers, issuance, loans, financing costs, concessions and
   funding confirmations since the previous review. Use the available Outlook
   archive or existing read-only Outlook tooling and primary company/filing
   sources to resolve relevant changes. Preserve source name, analyst and date.
2. Review funding_deals.json. Keep old source observations dated, and only change
   an instrument, amount, source or assessment when new evidence supports it.
   Before editing, archive the original file to _data/credit-monitor/research-history/
   with a timestamp. Add stable deal_id values when linking to the compute-deal
   timeline. A repeated announcement or confirmation is not new committed capital.
   Preserve old values in history and the affected company Changelog; maintain
   ai-compute-deals.md following its update procedure. Add confirmed catalyst
   outcomes to _meta/outcomes.md. Never infer an outcome merely from an elapsed date.
3. Keep `asof` as the research evidence date. Do not advance it merely because a
   fetch or build ran. `weekly_review` can record `reviewed_at`, `summary`, and
   `sources` (a list of dated citations/links), including review coverage and gaps.
   Each snapshot section retains its own underlying source date. If evidence
   cannot be updated, state that explicitly in weekly_review rather than calling
   the old assessment current. Source observations may have different dates.
4. Run `py _wiki/_tools/test_credit_monitor.py`, then
   `py _wiki/_tools/refresh_credit_monitor.py`. This refreshes completed-session
   Bloomberg history through yesterday, builds the dashboard atomically, verifies
   the live page matches, and prepares the dated brief and self-contained HTML
   attachment under _data/credit-monitor/exports/. Inspect the prepared email and
   run audit. It includes weekly/monthly changes with actual comparison dates,
   newly added/revised ledger evidence, research watchpoints and coverage gaps.
5. Send with `powershell.exe -NoProfile -File _wiki/_tools/send_credit_email.ps1
   -BodyPath <dated-email.txt> -AttachmentPath <dated-credit-monitor.html>
   -Subject "AI Credit & Funding | Weekly summary | YYYY-MM-DD" -Send`.
   Alternatively `py _wiki/_tools/refresh_credit_monitor.py --send` runs the chain
   and send together. An explicit partial-data brief is allowed when a source
   fails; keep the last valid dataset, explain the failed source and its dates,
   and do not imply a successful refresh. Inspect before sending if any step failed.
6. Verify the receipt and Sent Items. For an ambiguous result use the same mailer
   arguments with `-Verify`; never resend blindly or erase a receipt to retry.
   Once a receipt exists, the runner preserves that date's exact export artifacts.
   Briefly report completion or a concrete failure in the originating task.

## Implementation and checks

- `fetch_funding.py`: Bloomberg local terminal only; all configured instruments
  must succeed before replacement. Prior market snapshots are archived. No pip.
- `funding_common.py`: dated calendar lookbacks, finite observations, missing-data
  and freshness checks. Rate/OAS changes use bp; bond-price changes retain units.
  Baselines older than four calendar days from the target are unavailable.
- `build_funding_monitor.py` + `funding_dashboard_ui.py`: attributed SVG charts,
  responsive layout, source dates, search/category filters, theme and print mode.
- `refresh_credit_monitor.py`: overlap lock, retained snapshots, publication check,
  report exports, input hashes, run audit and optional email. `--skip-fetch` is an
  explicitly labeled preview and cannot be combined with `--send`.
- `send_credit_email.ps1`: hard-coded sole account/recipient, approved attachment
  directory, duplicate subject checks, durable pending receipt and Sent Items check.

The routine writes derived data, dashboards and metadata only. Research page edits
require the separate evidence review above; feature scripts never edit company pages.
