# GPU pricing dashboard

Added 2026-09-23. [Pricing tab](../_dashboards/gpu-pricing.html) · [OpenRouter + Vercel](../_dashboards/openrouter.html#gpu-pricing).

Sources, collected 2026-09-23:

| Publisher / channel | Instrument | Basis | Latest observation |
| --- | --- | --- | --- |
| Silicon Data / Bloomberg Desktop API | SDH100RT Index | Standardized non-hyperscale H100 rental | 2026-09-22 |
| Silicon Data / Bloomberg Desktop API | SDA100RT Index | Standardized non-hyperscale A100 rental | 2026-09-22 |
| Silicon Data / Bloomberg Desktop API | SDB200RT Index | Standardized non-hyperscale B200 rental | 2026-09-22 |
| SemiAnalysis / Bloomberg Desktop API | SAH100SC Index | H100 spot-contract composite | 2026-09-23 |
| SemiAnalysis / unauthenticated public API | H100, A100, B200 | Published daily spot-contract composites | 2026-09-23 |
| SemiAnalysis / unauthenticated public API | H100 one-year contracts | Survey 25th–75th percentile, typically 25% prepayment | Aug 2026 |

Primary references: [Silicon Data methodology](https://www.silicondata.com/products/silicon-index), [H100 segment definition](https://www.silicondata.com/products/silicon-index/h100), [SemiAnalysis dashboard and methodology](https://gpu-index.semianalysis.com/), [public feed used by that dashboard](https://gpu-index.semianalysis.com/api/public-data). The public endpoint is fresher than the website's initial static HTML; use API observation dates, never the page retrieval date as the price date.

Bloomberg requests use local port 8194, installed blpapi, HistoricalDataRequest PX_LAST and reference fields NAME/PX_LAST/LAST_UPDATE_DT/CRNCY. No package installation or remote Bloomberg fallback. Only daily history is charted; reference quotes are retained separately. Seven distinct delivery series are stored; the two H100 SemiAnalysis delivery channels represent the same publisher and are not independent signals.

The chart displays reported prices without smoothing, daily averaging or forward filling. Missing contract ranges remain blank; sold-out observations are not zero. Contract chart periods have equal visual spacing and varying durations. Each source carries its own observation date and retrieval timestamp. The public contract snapshot has no April 2026 one-year range; do not backfill from older static website defaults.

## Refresh and retention

`py _wiki/_tools/gpu_pricing.py` collects both sources. `py _wiki/_tools/build_gpu_pricing.py` renders the standalone page; `py _wiki/_tools/build_openrouter_dash.py` renders its embedded tab. The existing `refresh_features.py` chain now collects and renders both views, and `refresh_ai_gateways.py` also includes GPU prices. Offline gateway runs rebuild from cache.

Raw responses are timestamped under `_data/gpu-pricing/raw/` and ignored by Git. Normalized caches and status are under `_data/gpu-pricing/`. Failed instruments keep their previous series; errors and stale observations are visible. Historical revisions overwrite the normalized value for that date while preserving raw source vintages. A regressing source snapshot is rejected.

## Access and validation

The main Capstone hub has `openrouter-vercel/` and `gpu-pricing/` links into the internal research wiki. These navigation files are persisted in the hub repository so its daily reset does not remove them; existing unrelated working edits were retained. The pricing page and updated OpenRouter view are also copied to R:, with offline links in `ABRIR-WIKI.html` and the hub mirror. The existing nightly mirror maintains those copies.

Validation: seven Python feed/retention tests; 36 JavaScript chart/filter combinations, contract chart and CSV export; eight link-routing cases (internal server, local fallback, offline R: and public navigation); successful HTTP responses for the internal portal, both hubs and both dashboards. No browser visual inspection was performed.
