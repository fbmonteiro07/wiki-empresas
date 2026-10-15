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

## Daily alerts (added 2026-10-14)

Why: on 2026-10-13 CoreWeave's 5Y CDS went back to its late-July high (~1,000bp; Rothschild & Co TMT Daily,
Adley/Shaw, 2026-10-14; Susquehanna, Hearon, 2026-10-14: +79bp, briefly above 1,000bp intraday) and nothing
flagged it: this monitor tracked four index-level series on Fridays, and the 2026-10-09 brief failed to send
(Outlook OST at its size limit, no retry). The daily layer below sits on top of the weekly research brief.

Files
- `_data/credit_watch_config.json` — HAND-EDIT: instruments (Bloomberg ticker CANDIDATES tried in order; `status`
  unverified / needs_isin until confirmed at the Terminal via CDSW / SRCH), sigma-scaled rules per instrument
  (`d1_abs`, `d1_z`, `d5_abs`, `level_line`, `high_60d`, `high_1y`), the mail patterns and the delivery block.
- `fetch_credit_watch.py` — fail-soft per instrument into `_data/credit_watch.json` (previous points kept on
  failure; the first LIMIT / WORKFLOW_REVIEW_NEEDED answer marks `bbg_status` blocked and skips the rest).
  Equities come from `_data/technicals/prices.json` (the 18:15 chain), no second Bloomberg pull.
  `--probe` lists which candidate tickers resolve.
- `credit_alerts.py` — the engine: MARKET layer (1d / 5-obs change in the instrument's own unit, trailing-60
  sigma, new 60d / 1y highs, level lines; spreads on widening, equities on down moves and sigma-gated) and MAIL
  layer (`credit_mail_collect.ps1`: credit terms attributed to the nearest watched name; hyperscalers and labs
  need two distinct firms; boilerplate excerpts de-duplicated for 14 days). Writes `_data/credit-monitor/alerts/
  {latest.json, log.jsonl, state.json, emails/, receipts/}`; `--send` e-mails "AI Credit ALERT | date | headline"
  to Felipe only, confirmed in Sent Items, with the Outbox-backlog guard.
- `test_credit_alerts.py` — rule-engine checks (units, sigma, highs, level lines, mail proximity, de-dup).
- The dashboard section "Daily alerts & single-name watch" (02 in the sidebar) renders latest.json + the log.

Lane: Claude task `credit-alerts`, Mon–Fri 09:30 and 18:30 São Paulo —
`py _wiki/_tools/credit_alerts.py --fetch --mail --send`, then `fetch_funding.py` + `build_funding_monitor.py` so the
four index gauges at the top of the page and section 02 both refresh daily (gauges = last completed session;
the research ledger, scoreboard and watchlist stay weekly), push notification when something fired, and on
Friday 09:30 a check that the weekly brief actually went out (retry `send_credit_email.ps1 -Verify` / `-Send`
once if the 09:00 Codex heartbeat recorded an e-mail failure). Weekly brief unchanged.

Open items: confirm the CDS / bond tickers once the Desktop API block clears (`fetch_credit_watch.py --probe`),
paste ISINs for the CRWV 2026 notes, the 2032s and the 2033 convertible, re-base `level_line` on real history.

## Issuer yield board (added 2026-10-14, Felipe: "quero um monitor com o yield de CRWV, ORCL, NBIS, hyperscalers e outros")

Section "Issuer yields — live board" on the dashboard (sidebar 04), placed ahead of the static Morgan Stanley spread
snapshots, which are now labelled as dated broker snapshots. Universe = `_data/credit_watch_config.json → board`:
CoreWeave (8 notes incl. the 2032 9.625% headline, the EUR 8.5% and three converts, + 5Y CDS), Nebius (five
converts, no CDS), Oracle (Feb-26 jumbo 5/10/30/40y + Sep-25 10/30y, CDS = ORCLCP), Meta, Amazon, Alphabet,
Microsoft, NVIDIA (10y/30y points + 5Y CDS), xAI 12.5% 2030, the CRWV-offtake project bonds (APLD ComputeCo, Core
Scientific Finance I, Edged Compute), Cipher Compute, WULF Compute, IREN converts, Stingray (AMZN offtake), HUT 8 DC
(IG project bond) and SoftBank. Tickers were resolved with the Bloomberg instrument lookup (//blp/instruments),
which answers even while the data service is blocked; the fetch tries decimal / fraction / 2- and 4-digit-year
spellings and pins the first that returns history. Each bond = daily YLD_YTM_MID history + bdp snapshot (price,
Z-spread, size, S&P / Moody's); each CDS = PX_LAST history. Alert rules per tier (HY bonds 40bp/2.5σ, IG 15bp/3σ,
converts 60bp/3σ, CRWV CDS 50bp + 800bp line, ORCL CDS 15bp + 200bp line) — the board instruments are therefore
also covered by the daily ALERT e-mail. Convertible YTMs are flagged and never compared with straight debt.
Status 2026-10-14: instruments resolved, no yields yet (Desktop API block) — fills on the first unblocked run.
