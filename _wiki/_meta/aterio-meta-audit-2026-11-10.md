# Meta Aterio capacity reconciliation — 2026-11-10

**Conclusion: August arithmetic passes; completeness as a current Meta capacity forecast does not.** The dashboard covers US buildings attributed to Meta by Aterio's structured provider/end-user fields. Its house headline is additions in 2026–30, using the agreed November 9 filters and a uniform facility/IT proxy. It is not Meta's global installed compute, all contracted compute, or full campus design capacity. No numerical override was adopted.

## Reproducible bridge

Source: **Aterio licensed US inventory, 2026-08-31**, independently recalculated on 2026-11-10. **HARD** means exact vendor fields, not independently verified physical capacity. The **1.15** divisor is a HARD measured cross-sectional median on 1,025 US rows with both fields, but its application to each Meta building is an **ESTIMATE**. The source contains 417 ratios of exactly 1.000. Rules remain those decided on 2026-11-09 in [treatment.json](../_data/aterio/treatment.json).

| Measure | Source inputs and arithmetic | GW IT-equivalent |
|---|---|---:|
| Self-built additions 2026–30 | 9,312.44 MW / 1.15 / 1,000 | 8.098 |
| Named tenant additions 2026–30 | 3,945.60 MW / 1.15 / 1,000 | 3.431 |
| Total additions | 13,258.04 MW / 1.15 / 1,000 | **11.529** |
| Operating before 2026 | 4,239.93 MW / 1.15 / 1,000 | 3.687 |
| End-2030 capacity under house rules | (4,239.93 + 13,258.04) MW / 1.15 / 1,000 | **15.216** |
| Medium additions dated 2026–30, separate scenario | 1,489.32 MW / 1.15 / 1,000 | 1.295 |
| End-2030 including Medium | (4,239.93 + 13,258.04 + 1,489.32) MW / 1.15 / 1,000 | **16.511** |

The end-year scenarios assume no retirements. Do not add all August operating capacity (4.523 GW IT-eq) to 11.529: 2026 activations already appear in additions. Independent raw-CSV selection found 269 unique buildings, 259 live/non-withdrawn, and matched the company-lookup route. Its rounded serialization creates only 0.26 MW of difference in the house cohort, immaterial at displayed precision.

## Why it can look low

1. **Hyperion phase and date filters.** Aterio records 2,040 MW under construction, 857.2 MW of Medium phases dated 2030, and 2,143 MW of Medium phases dated 2031–35. Only the construction phases enter the house headline: **2,040 / 1.15 / 1,000 = 1.774 GW IT-eq**. [Meta's Richland Parish page](https://datacenters.atmeta.com/richland-parish-data-center/), checked 2026-11-10, describes **5 GW of compute capacity** at full build, while retaining an older “over two gigawatts” paragraph. No precise ramp is supplied there. Do not call the 5 GW facility power, delivered capacity or a 2030 completion commitment.
2. **Later broker benchmark is much larger, but not reconciled.** Bernstein / Madison Rezaei et al., **2026-11-06**, Exhibit 15, prints about **6 GW operating / 15 GW under construction** for Facebook. The existing digitized values are 5.91 / 14.60; those decimals are not printed disclosures. Our August fields total **5.201 GW operating / 8.849 GW construction, facility basis**. Bernstein's underlying export date, attribution and GW basis are not established. Promoting all announced phases on campuses with construction raises the August construction sensitivity to **15.785 GW facility**, illustrating how classification can produce a similar level without any new building. This is not evidence that all those phases are under construction. [Original rendered chart, p.14](../_data/aterio/meta-audit-2026-11-10/bernstein-exhibit15-p14.jpg).
3. **Cloud contracts and geography are incomplete.** The recorded tenant list has no Nebius or CoreWeave provider attribution. Nebius's [2026-03-16 company release](https://nebius.com/newsroom/nebius-signs-new-ai-infrastructure-agreement-with-meta) confirms dedicated capacity beginning early 2027 and a separate contingent capacity purchase arrangement, without a GW figure. The existing cloud-contract work remains separate: no additive MW assigned without site and tranche reconciliation, and overseas capacity is outside the US census. Crusoe Childress and Warrenton already appear in the census and must not be added again.
4. **Specific data-quality gaps.** Nine live buildings have no selected MW. Aterio's HOU3 / Houston Dual-Facility Campus row (UID `8c5eb1c4-35bd-452c-9ad7-338657086592`) has a blank end-user field, but its 2026-06-06 JR note says Meta/Paile LLC leases it, citing comptroller data. That leaves **43 MW facility** of vendor-attributed operating capacity outside structured matching. Primary lease evidence remains unverified; no override adopted and no attribution inferred for HOU4.

## Sensitivity and guardrails

- Retaining the same rows but using Aterio's explicit critical-IT field when positive, otherwise the 1.15 proxy, yields **11.924 GW additions**, versus 11.529. **ESTIMATE / data-quality sensitivity, not a correction:** 22 of the 23 affected house rows have identical selected-power and IT fields. Hyperion is the largest contributor. The roughly 0.40 GW effect cannot account for the much larger broker discrepancy.
- The existing alternative divisor assumptions give **11.332 GW at 1.17** and **10.439 GW at 1.27**. A larger facility/IT divisor lowers the result. No divisor was fitted to force agreement with Bernstein.
- **PASS:** raw arithmetic, unique IDs, role union, house filters, stock/addition bookkeeping, agreement with displayed rounding.
- **PARTIAL:** independent physical-stock and annual-delivery validation unavailable. Bernstein's construction stock is not an annual addition or a company disclosure. Timing, attribution and power-basis differences remain unresolved.
- **Focused skeptic:** independent double-check completed before final delivery; arithmetic passed, interpretation remains PARTIAL. Corrected the unsupported same-basis statement and strict-floor claim, and documented the notes-only HOU3 attribution.

Evidence: [audit.json](../_data/aterio/meta-audit-2026-11-10/audit.json), [independent stdlib calculation](../_data/aterio/meta-audit-2026-11-10/audit.py), [selected building rows](../_data/aterio/meta-audit-2026-11-10/meta_buildings.csv). Original census fields, dates, house rules and deal terms remain intact. The dashboard now labels the headline as US additions and operating capacity by its snapshot date; the Meta panel and methodology explain these limitations.
