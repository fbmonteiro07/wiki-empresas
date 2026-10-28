# SK hynix 3Q26 — source reconciliation

Recorded 2026-10-28; event 2026-10-28 KST / evening 2026-10-27 São Paulo. Targeted ingest requested by user.

## Evidence obtained

- Company preliminary consolidated K-IFRS release: https://news.skhynix.com/en/q3-2026-business-results/.
- J.P. Morgan / Jay Kwon and Sangsik Lee, 2026-10-28, First Take: 3Q26 beat and W100trn shareholder return program announcement. Full connector-returned email archived in `_inbox/_done/20261028_JPM_Jay-Kwon_Sangsik-Lee_SKHYNIX_3Q26-first-take.email.json`; readable text HTML in `relatórios bons/`. First take predates call. OW / KRW2.75m June-27 PT unchanged.
- Jefferies / Conor O'Mara, 2026-10-28 01:25:18 UTC, detailed call/Q&A sales notes. Full returned email archived in `_inbox/_done/20261028_Jefferies_Conor-OMara_SKHYNIX_3Q26-call-notes.email.json`; readable HTML in `relatórios bons/`. Secondary, not verbatim transcript; embedded CID images were not retrieved.
- Vital Knowledge / Adam Crisafulli, 2026-10-28 00:06:02 UTC, earnings takeaways. Full returned email archived in `_inbox/_done/20261028_Vital-Knowledge_Adam-Crisafulli_SKHYNIX_3Q26.email.json`; readable HTML in `relatórios bons/`. Commentary, not guidance.
- Culpium / Tim Culpan (10-28 article, received 10-27 23:31:59 UTC) consulted for cross-check only: free-tier excerpt, not full research; not ingested as a complete source. Jefferies / Steven Wong morning preview was redundant and not separately filed.

## Reconciled values and unresolved bases

| Item | Sources | Treatment |
|---|---|---|
| Revenue / OP | Company KRW104,615.5bn / 83,333.8bn; Jefferies email contains KRW83.3bn and KRW10.4tn | Company units adopted. Raw errors preserved, no silent source edit. |
| Net income | Company consolidated KRW39,775.6bn; JPM KRW39,534bn | Keep consolidated primary. Do not assume JPM attribution-to-owners basis without deck evidence. |
| OPM | Company 80% Q3 / 76% Q2 rounded; JPM Q3 79.7% but Q2 42.2% | Company rounded comparison used; erroneous Q2 broker cell not adopted. |
| Consensus | JPM table revenue KRW97,870bn / OP76,740bn; Vital sales KRW98.6B and OP77.5T; Jefferies OP77.5 with inconsistent units | JPM dated Bloomberg comparison used. Do not mix independent consensus snapshots or repair typos by inference. |
| Capex | JPM Q3 KRW12.7tn / YTD31tn; Culpium excerpt YTD32.4tn | Await deck basis; no annual guide inferred from conflicting spending figures. |
| FY26 returns | Company approximately KRW100tn, dividends >=30tn and repurchases/cancellations >=60tn including August40tn; JPM 60tn/40tn split | Company wording governs. Minimum components need not sum exactly to approximate total. |
| Kioxia | Company most realized gains returned via special dividends; Jefferies describes KRW100tn as Kioxia gain/special dividend | Reject Kioxia-only100tn interpretation; total FY26 return program is100tn. |
| August buyback / new authorization | August40tn purchased last week, cancellation forthcoming; new20tn splits10tn cancellation/10tn employee compensation | Keep completion, authorization and cancellation distinct; compensation excluded from return total. |
| LTAs | Company14 customers, >50% total capacity2027–28, typically5 years, agreed price range; UBS10-16 floor-only/no-ceiling rumor | Primary description governs; exact bounds/contract uniformity undisclosed. Prior rumor retained in Changelog archive. |
| Sold out2029 | Jefferies notes combine secured volumes and demand discussions | Not a fully signed three-year contracted book; no new deal ID or customer mapping. |
| HBM demand >2x supply / yield / margins | Jefferies sales notes relaying management | Secondary label retained; no numerical yield/margin implied and no validation of individual12-Hi sockets. |
| HBM4 crossover | Company Q4 volume+revenue target; M15X YE26 max-capacity target | Guidance only; prior failure/delay hypotheses remain unresolved at SKU level. |

## Page and archive handling

- SKHYNIX Current state, Debate, catalysts, rolling management table and new Q3 intra-quarter baseline updated. Whole Q2 intra-quarter window and prior management table preserved under Changelog; five resolved catalyst lines preserved verbatim.
- hbm-memory updated; ai-compute-deals reviewed and updated as anonymous aggregate LTA context, without new deal ID, dollar sum or MW.
- Index thesis updated with old value in SKHYNIX Changelog; hbm-cycle canonical string unchanged, two company-specific variants added. BBG and house estimates unchanged.
- Outcomes distinguish announcement from delivery; November19 purchase-window entry records early completion but leaves cancellation open.
- Pre-ingest page snapshot: `_wiki/_meta/2026-10-28-skhynix-before.md`. No unrelated inbound files moved or archived.

## Coverage gap

Full verbatim 3Q26 earnings-call transcript not yet obtained. Local SKHYNIX/transcripts, active inbox and P: drop checked; latest archived company call is July29. Detailed Jefferies Q&A notes are searchable as a report and are not misfiled as a transcript. Official deck capture and final validation recorded below when complete.

## Validation and primary archive

- Official release HTML archived with source metadata/SHA256 in `_inbox/_done/20261028_SKHYNIX_3Q26_official-release.html` and `.source.json`; searchable extracted article text in `_wiki/_data/figures/20261028_SKHYNIX_3Q26_official-release.md`.
- Independent focused QA: no factual/attribution issue found in inserted release, LTA, HBM or capital-return terms. Before/after Counter check found zero missing preexisting nonblank lines. Reviewer requested explaining the net-income miss; broker-attributed FX/valuation-loss paragraph added.
- Existing whole-page transcription linter flags belong to retained historical content, not new text.

## Primary deck resolution — final source check

Official PDF: `_inbox/_done/20261028_SKHYNIX_3Q26_official-earnings-deck.pdf` (3,111,952 bytes), matching `.source.json`; searchable extraction `_wiki/_data/figures/20261028_SKHYNIX_3Q26_official-earnings-deck.md`. Source: https://mis-prod-koce-homepage-cdn-01-blob-ep.azureedge.net/web/attach/21435786328187801.pdf. Pages9/10/16 visually checked against rendered images.

- Page4 independently confirms DRAM bits ~+10% and ASP high20%; NAND bits slightly down, ASP mid20%.
- Page6 confirms consolidated NI39.78tn, net nonoperating loss32.63tn, FX loss11.63tn and investment-asset loss22.92tn. Does not identify the investment asset as Kioxia; that identification remains JPM interpretation. Attachment2 exact FX11,633bn; Others21,452bn is a different line from22.92tn, not a contradiction to overwrite.
- Pages9/10 distinguish 2027 market achievable-demand DRAM mid20%/NAND highteens from company Q4 shipment guidance DRAM mid20%/NAND mid-single% including Solidigm. No company2027 shipment guidance inferred.
- Page11 primary confirms2027 HBM negotiations finalized, profitability gap versus conventional DRAM narrowing meaningfully.
- Page15 EPS54,773 basic/54,454 diluted; no attributable-to-parent NI breakdown. JPM39.534tn basis therefore still unresolved.
- Page16 PP&E cash acquisition12,670bn3Q /10,671bn2Q; no1Q/YTD total. JPM12.7tn quarterly is supported; YTD31tn/32.4tn difference stays open. Cash balance includes short-term financial instruments/investments.
- Full transcript still not captured. Official webcast requires email verification; public transcript indexes checked through2Q26; TradingView/Quartr716480 lead inaccessible. Secondary Jefferies notes remain a report, not a fabricated transcript.

## Final QA

Independent deck audit passed: EPS, operating cash flow, PP&E cash spending and FX/investment-loss figures match; Q4 company shipment guidance and 2027 market demand are correctly separated; JPM net-profit basis remains unresolved. Source links in new sections checked with no missing targets.

Search verified five new source documents: official release and deck extracts plus JPM, Jefferies and Vital text reports. Offline wiki rebuilt successfully (111 companies / 23 themes); final EPS and market/company-basis wording verified in generated HTML. Feature-refresh log: `_wiki/_meta/refresh-2026-10-28-skhynix.log`. The generic GPU-price step reports Bloomberg timeout and retains its last good data; this does not affect the SK hynix earnings sources.
