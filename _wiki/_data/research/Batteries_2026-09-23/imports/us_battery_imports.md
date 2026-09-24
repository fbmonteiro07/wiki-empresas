# US battery imports: China, storage systems and Base Power

Retrieved September 23, 2026. Official trade data available through July 2026.

**China remains a major foreign supplier, but the latest recorded import values do not justify assuming that most imported housed storage systems come directly from China. Country of origin of a system, origin of its cells, and location of final assembly are separate questions. Base Power's cell origin remains unverified in this review.**

## Official data and grounding

Source for all trade tables: **USITC DataWeb, publishing US Department of Commerce / Census Bureau merchandise trade statistics**, retrieved September 23, 2026. Query: General Imports; General Customs Value; actual US dollars; all countries individually; all districts; no unit conversion. The dollar values below are **HARD reported inputs**. Shares are **DERIVED** by division of those inputs, with no forecast or estimated conversion factor.

[Official DataWeb query builder](https://dataweb.usitc.gov/trade/search/GenImp/HTS) · [Census release schedule](https://www.census.gov/foreign-trade/schedule.html) · [Census definitions](https://www.census.gov/foreign-trade/reference/definitions/index.html).

Customs value excludes US import duties and international freight/insurance. General imports record physical arrivals, including arrivals into bonded warehouses and foreign-trade zones. The country is the reported customs origin, not necessarily the shipping port or the nationality of the company's shareholders. These are nominal dollar flows, not installed capacity or energy capacity.

## Broad lithium-ion battery imports: HTS 850760

This category includes batteries for different applications, including EVs and electronics. It is not a stationary-storage-only series.

| Period | World imports, USD bn — HARD | China, USD bn — HARD | China share — DERIVED |
|---|---:|---:|---:|
| Full-year 2024 | 23.609 | 16.317 | 69.1% |
| Full-year 2025 | 19.728 | 11.697 | 59.3% |
| January-July 2025 | 12.245 | 7.591 | 62.0% |
| January-July 2026 | 9.721 | 3.825 | 39.3% |

Source: USITC DataWeb / Census, September 23 extraction. Values displayed in billions for readability; exact dollars are retained in the source files. The comparable January-July periods show China's share falling from 62.0% to 39.3%. The full-year rows provide historical context; the incomplete 2026 dollar total should not be compared directly with a full-year total as a growth rate. China remains the largest individual origin in the broad January-July 2026 table.

Worked calculation: **$3,825,215,075 / $9,721,366,797 × 100 = 39.3485%, rounded to 39.3%.** Both numerator and denominator are HARD official values for the same period and HTS universe.

## A new, more relevant code for housed storage systems

The **USITC 484(f) Committee changes effective February 1, 2026** discontinued 8507.60.0020 and split it into 8507.60.0030 and 8507.60.0090. Code **8507.60.0030** covers a housed energy-storage device of at least **1 kWh**, containing lithium-ion modules, battery-management circuitry and other components enabling energy storage/discharge. It is not limited to residential systems. Separately imported cells do not meet that full-system definition.

[Official USITC change record, printed pages 60-62](https://www.usitc.gov/tariff_affairs/documents/list_of_committee_changes_for_january-1-2026-and-february-1-2026.pdf) · [Current HTS](https://hts.usitc.gov/?query=8507.60).

Reported **February-July 2026** imports under 8507600030 totaled **$2,584,726,446**:

| Leading customs origin | Imports, USD m — HARD | Share of world value — DERIVED |
|---|---:|---:|
| Japan | 754.431 | 29.2% |
| South Korea | 679.981 | 26.3% |
| China | 401.056 | 15.5% |
| Malaysia | 202.759 | 7.8% |
| Vietnam | 175.218 | 6.8% |

Source: USITC DataWeb / Census, September 23 extraction. The table lists the five largest origins; other origins are retained in the raw data.

Worked calculation: **$401,055,914 / $2,584,726,446 × 100 = 15.5164%, rounded to 15.5%.** This is China's share of reported import value in this code and period. It is not China's share of US stationary-storage deployment, batteries consumed, GWh, or underlying cell content.

The monthly pattern also matters: China's reported BESS share was **10.4% in May, 19.2% in June and 28.0% in July 2026**. July's exact values were **$165,579,261 from China / $590,492,006 from all origins**. Thus the broad historical decline should not be read as a continuously falling share in every storage subcategory. The new classification has a short history and cannot establish a long-run trend yet. [Monthly evidence](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/bess_8507600030_monthly_official.json>).

## What this means for Base Power and the investment theme

**Base Power's own product page, checked September 23**, says Base Core is built at its Austin factory and uses LFP chemistry. The reviewed page does not identify the cell supplier or cell country of origin. Accordingly, this review does not classify Base Core itself as a finished-system import from China and does not infer domestic cell production from domestic assembly. [Base Core](https://www.basepowercompany.com/core).

**Our interpretation:** Coatue's distributed-storage thesis can coexist with international sourcing of cells and components. The economic exposure may sit in system design, assembly, installation and dispatch as well as in cell manufacturing. The observed shift in recorded import origins does not by itself establish reduced reliance on Chinese upstream inputs, tariff causation, or stronger margins for any named supplier.

These trade tables cannot establish the import share of total US battery demand because domestic shipments, exports, inventories and a consistent product/valuation bridge are absent. They also cannot identify company-level suppliers. No conversion from dollars or kilograms into GWh is attempted.

## Verification and reproducibility

**Independent calculation review: PASS**, covering arithmetic, captured-table reconciliations and HTS scope. It was not a second live DataWeb extraction. [Audit record](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/audit.md>).

- Country rows reconcile exactly to the published world totals for all captured periods.
- Every BESS country's February-July monthly sum reconciles exactly to its aggregated query result.
- Every January-July 2025 country sum reconciles exactly between monthly and aggregated views.
- The query builder displayed erroneous end-of-year labels in the partial-year annual views. The selected date inputs and explicit monthly columns establish the actual periods; the monthly data are authoritative for these reconciliations.
- The derived 2024 lithium share rounds to the **69%** reported by **CRS Michael Alan Havlin, R48538, November 26, 2025**. This is a separately published compilation using the same underlying Census system, not independent customs collection. [CRS report, accessible mirror](https://www.everycrsreport.com/reports/R48538.html).
- No load-bearing estimates or calibrated parameters are used. The relevant sensitivity is product coverage and valuation/origin definitions, rather than uncertainty in an assumed coefficient.

[Exact calculations and automatic checks](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/calculated_shares_and_checks.json>) · [Reproduction script](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/verify_imports.py>) · [Broad official table](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/lithium_850760_official.json>) · [Prior-year monthly table](<E:/Wiki Felipe empresas/_wiki/_data/research/Batteries_2026-09-23/imports/lithium_850760_jan_jul_2025_monthly_official.json>).
