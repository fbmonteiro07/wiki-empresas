# Verification completed 23 September 2026

- Deliverable: `_deliverables/CPU_market_share_2021_2030_2026-09-23.docx`.
- Independent source audit: transcription and arithmetic PASS; external forecast validity PARTIAL. See `audit.md`.
- All share inputs independently checked against the dated original broker exhibits by the audit agent.
- Automated numerical checks: shares within 0 to 100 and source row totals within 0.11 percentage point of 100; PC extension preserves 100 before display rounding.
- Incorporated audit qualifications: visible 2025 Arm value-share restatement, illustrative PC 2029–2030 extension, differing UBS universe and qualified merchant Arm ASP assumption.
- Packaged `render_docx.py` initial conversion failed because LibreOffice is not bundled or available on PATH in this Windows runtime. No installed desktop LibreOffice used.
- Fallback: native Microsoft Word exported the document to an internal QA PDF; packaged `render_docx.py` rasterized it using bundled Poppler. The Word statistics API returned one page, but the rendered PDF and PNGs correctly contain five pages; PNG inspection is controlling.
- Inspected every final page image after the last edit. Five clean pages, no clipping or overflow; removed inherited blue title border. Source links, annual tables, forecast labels and worked calculations are readable.
- No wiki ticker pages, standing assumptions, research ratings or compute-deal records changed. Output is a separate comparison document, not a newly adopted house forecast.
