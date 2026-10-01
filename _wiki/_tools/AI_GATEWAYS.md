# OpenRouter + Vercel monitor

Run `py _wiki/_tools/refresh_ai_gateways.py` to collect both public sources, rebuild the existing OpenRouter dashboard, and write the weekly brief. `--offline` uses the last successful derived data. Only Python's standard library is required.

The existing Monday OpenRouter refresh remains in place. A Codex heartbeat named **OpenRouter + Vercel — resumo semanal** runs Friday at 09:00 America/Sao_Paulo in the originating task and delivers the summary there. The workstation and Codex app need to be running for the local automation. Its prompt contains the paths and methodology needed to recover context.

- Dashboard: `_wiki/_dashboards/openrouter.html` (Vercel section: `#vercel`).
- Studies entry: the dashboard hub's **Estudos · OpenRouter + Vercel** card, maintained in `refresh_features.py`.
- Weekly brief: `_wiki/_dashboards/gateway-weekly.html` and `_wiki/_data/ai-gateways/weekly-latest.md`.
- Run status and failures: `_wiki/_data/ai-gateways/status.json`.
- Original Vercel exports and collection manifest: `_wiki/_data/vercel/raw/<UTC timestamp>/`.
- Vercel derived shares: `_wiki/_data/vercel/dashboard.json`.
- OpenRouter history remains in its existing directory. Full dashboard snapshots for future comparisons are also retained in `_wiki/_data/ai-gateways/snapshots/`.

Vercel source: https://vercel.com/ai-gateway/leaderboards/models. Export documentation: https://vercel.com/docs/ai-gateway/leaderboards. License: CC BY 4.0; attribution and transformation notice appear on the dashboard. We request fixed dates, all modalities, model and lab datasets; the dashboard uses the last date common to tokens, requests and spend in both datasets.

Vercel weekly comparisons are **simple averages of daily shares**, never volume-weighted weekly shares. A weekly mean requires all seven days and a change requires all fourteen. Missing top-list entries are unknown, not zero. Reach and Preference are not present in the JSON export; their definitions and source links appear in the dashboard, without invented series.

OpenRouter uses trailing seven-day snapshots. Comparisons state the actual interval when no exact seven-day baseline exists. Model names and catalogue prices do not prove a new release or an actual customer price change. Vercel spend shares are reported by that gateway; OpenRouter dollar figures remain list-price/cache-off estimates. Neither dataset is global market share, and they must not be added together.

On collection failure the runner keeps the previous dashboard and reports the error. Vercel advances its pointer only after both datasets validate. Stale dates remain visible. `test_vercel_gateway.py` checks seven-day calculations, missing observations, duplicate rows and invalid shares.

## Methodology clarification — 2026-09-19

The original integration called Vercel spend “reported spend”, meaning a metric published by Vercel. Its September Production Index clarifies that spending is estimated using labs’ published list prices and that actual bills can differ. Dashboard labels now say estimated spend (list prices); never characterize it as realized revenue. Source: https://vercel.com/blog/ai-gateway-production-index-september-2026. Vercel states monthly traffic is tens of trillions of tokens, without a precise absolute total; do not derive an exact size ratio from the share export.

## Token growth and share charts — 2026-09-21

`gateway_charts.py` now builds ten static SVG charts at the top of the main dashboard and the weekly brief. It also publishes `_dashboards/ai-gateways-charts.html`, the machine-readable `_data/ai-gateways/charts.json`, and a self-contained dated HTML attachment in `_data/ai-gateways/exports/YYYY-MM-DD-ai-gateways-charts.html`. No browser, network access, JavaScript, or third-party dependencies are needed to open the attachment. Every chart has a source/date, hover values, and an expandable data table.

OpenRouter chart history sums **all public-feed prompt + completion tokens**, preserving dormant model rows in older date buckets. This differs from the pre-existing dashboard's text-model filter. Chart dates are the latest bucket's window-end date, not the collection date. Standard/other variants are not automatically described as paid: zero-price/promotional standard variants exist. Model movers keep each variant separate and require both observations; missing entries are not zero. Growth chooses an exact seven-day baseline where available, otherwise the nearest baseline within 4–10 days and labels the actual interval. The first observation and zero denominators have no inferred growth. Lines retain missing observations as gaps; lab history fixes the latest six leaders across the available history.

Vercel collection requests 90 days of daily shares. Absolute Vercel token growth cannot be calculated from that export. Weekly changes require all fourteen observations and remain differences between unweighted seven-day means. The token-versus-spend chart is also a comparison of unweighted means and labels list-price estimation explicitly.

The Friday 09:00 America/Sao_Paulo email to `felipe.monteiro@capstone.com.br` must include the dated chart pack as an actual attachment, plus the summary and dashboard links. `send_gateway_email.ps1` supports sending via the existing Outlook desktop account when the connector is unavailable. It checks the exact recipient/account, duplicate subject in Sent Items/Outbox, writes a local pending receipt before dispatch, and verifies Sent Items after dispatch. Never retry an ambiguous send without checking that receipt and Outlook.

## Four-panel token economics study — 2026-09-29

The user confirmed that the reference exhibit consolidates OpenRouter data through JPM; its report date and exact index formula were not supplied. The new study uses our retained OpenRouter captures directly, with explicitly documented formulas rather than copying the exhibit's values.

`or_token_economics.py` joins each ranking capture to its own model prices and catalogue metadata. `token_economics_ui.py` builds four static SVG panels: weekly token volumes; an equal-weight catalogue price index; volume-weighted token price; and matched-token weekly spend. The average index gives each standard text model equal weight and uses a declared 50:50 input/output convention, including unused models. Weighted pricing uses observed prompt/completion mix. Free-tagged variants remain zero-priced; unmatched variants, negative sentinels and ambiguous aliases stay unpriced. Their tokens are excluded from both weighted-price numerator and denominator. Open/closed metadata is a proxy; routers and stealth models remain unclassified.

Outputs: `_data/ai-gateways/token-economics.json` (model-level calculations, raw file hashes and checks), `_dashboards/token-economics.html`, and the `#token-economics` section of `openrouter.html`. `gateway_charts.publish()` includes all four panels before the existing ten in the weekly page and dated email attachment. Both Monday's `build_openrouter_dash.py` and Friday's `refresh_ai_gateways.py` invoke that publisher, so the new panels refresh with the existing routines. Do not change the recipient or create a duplicate weekly job.

Matching price/usage history currently begins with the window ending 2026-07-20; preceding history is not repriced with today's catalogue. Duplicate window ends retain the earliest valid capture. Consecutive snapshots can overlap and must not be summed. Price coverage is shown by category and observation; amber chart rings flag coverage below 99%. Data tables retain missing observations. A separate completed-week chart endpoint checks aggregate token units/scope, not realized spending.

Dollar outputs are **uncalibrated matched-token list-price scenarios**, not billing estimates, realized revenue or guaranteed ceilings. Illustrative 50%/70% cache-read scenarios use observed cache-read prices; the fractions are assumptions, not measured hit rates. Cache writes, tiers, other fees, provider routing and discounts are not modeled. Public `total_usage` values are retained as a diagnostic with unverified units and scope; positive free-tagged values prevent silently equating this field to billed USD. Zero raw cache/BYOK counters do not establish zero real usage. See the dashboard's expandable methodology and `_data/ai-gateways/token-economics-review-2026-09-29.md` for the independent arithmetic audit and remaining limitations.

Friday's summary must read `token-economics.json`, mention volume/mix, the average and weighted price measures, matched spend and coverage, and include the four panels in the actual HTML attachment. Give source/window dates and use strict WoW only for seven-day-separated observations. Vercel remains a separate daily-share analysis; never invent absolute Vercel volumes/spend or a gateway total.

Validation: `py -m unittest discover -s _wiki/_tools -p test_token_economics.py`, plus the existing `test_gateway_charts.py` and `test_vercel_gateway.py`. An offline rebuild uses the retained source dates and reports staleness explicitly.
