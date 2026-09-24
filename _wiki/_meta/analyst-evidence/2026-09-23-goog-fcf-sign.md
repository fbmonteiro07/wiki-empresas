# Supplemental data-quality finding — GOOG FCF sign

Signal ID: manual-goog-fcf-sign-20260923. Editorial supplement; not a new ID in generated signals.json.

Observed September 23, 2026, while checking esti-bf7122f00934 / esti-56921f2baecc.

Hard evidence: _wiki/GOOG.md, "Capstone estimates (house model)", attributed to Capstone's Google Modelo oficial.xlsx dated June 5, 2026, shows FCF ($bn) of 33 / -3 / -55 for 2025 / 2026E / 2027E. The raw_rows field in _wiki/_data/house.json (asof September 22) retains those same negative strings, but the parsed years fields contain fcf=3.0 and fcf=55.0 for 2026 and 2027 respectively.

The sign mismatch between the stored raw table and parsed fields is confirmed. The original workbook was not opened, and the exact parser defect and any downstream valuation impact were not audited. Company pages, model files and parsed data were not changed.

Action: reconcile the original workbook and repair/test the extraction pipeline before using the structured FCF values. Audit other negative-value fields. Keep the separate revenue/EPS basis reconciliation open.

Falsifier for the underlying negative-FCF assumption: the original workbook confirms positive FCF and proves the wiki/raw table stale. That would change which representation to correct; it would not erase the observed internal mismatch.
