# Reconciliation — run-inbox 2026-07-02 (evening batch)

Variance pass on the NEW quantitative datapoints from the 6 substantive sources (MS South Korea, MS NAND Outlook, SemiAnalysis ECTC/Bedrock/Meta-Compute, UBS Asia Semis Sector Keys). Purely thematic/qualitative items (packaging roadmaps, TPU-track mechanics, CPO timing) are excluded from the table but summarized at the end.

**Baselines:** (1) prior wiki comments (on-disk) · (2) Capstone house models (`_wiki/_data/house.json`, asof 2026-07-02) · (3) BBG consensus — **PENDING**: wrapper returned **HTTP 503 (Bloomberg Terminal not logged in)**. Re-run `refresh_features.py --run-estimates` and the BBG column below once the Terminal/VPN is reconnected. Web data was NOT substituted for consensus.

---

## Where the new data DIVERGES

| Name | New datapoint (source) | vs prior wiki | vs house model | vs BBG | Read |
|---|---|---|---|---|---|
| **MEDIATEK** | UBS **Key Call Buy, PT NT$1,800 → NT$6,500** (3.6×); TPU sales US$18/35bn 2027/28E; TPU design-service share 9%→38% 2026/27E; Cloud-ASIC EPS NT$111/219; new drivers ~83% of 2028E rev vs ~40% 2023 (UBS "Sector Keys", 07-02) | Old UBS PT NT$1,800 moved to Changelog. A 3.6× PT step = the Street capitalizing the Google-TPU design-service win into the base case | No house model | **BBG cons PT (2454 TT) NT$5,014 (spot NT$3,825); rev CY26 NT$646bn / CY27 NT$1,039bn; EPS NT$64.58 / NT$127.47 — UBS NT$6,500 is +30% above cons** | **Biggest single move in the batch.** The bull case is now "MediaTek = the #2 merchant TPU ASIC vendor." Stock +203% YTD already prices much of it; the debate is share durability vs Broadcom (which still ships 91%/62% in 26/27E). Watch for a house model init. |
| **AVGO** | UBS: Broadcom TPU **ship share 91% → 62%** 2026→27E as MediaTek takes 9%→38%; Google moving front-end TPU design in-house (UBS, 07-02) | Consistent with existing Redburn/Nomura/JPM "Google cedes share to MediaTek" thread | House EPS 12.89/21.07/**35.96** (26/27/**28**). A declining TPU ship-share is a headwind to the out-year (2028) ASIC ramp the house $35.96 embeds | **BBG cons EPS CY26 $13.59 / CY27 $21.14 (hi 25.34); rev CY26 $123.0B / CY27 $189.1B. House 26/27 ($12.89/$21.07) ≈ cons; no CY28 line** | **Share-cede risk to the AVGO 2028 EPS.** Not a today problem (units still grow), but the mix shift caps the TPU-driven upside. Bridge the house 2028 vs the 62%-and-falling share path. |
| **META** | SemiAnalysis: **>5GW contracted across Cloud & Colo in 1H26** (excl self-build), 2.5GW under construction in two campuses, 2027 capex "shockingly high," ~$10B Anthropic-type deal in talks (SemiAnalysis "Meta Compute", 07-02) | Adds hard GW figures to the existing "capex keeps climbing" thread | House META **FCF 17/23bn 2026/27**. A "shockingly high" 2027 capex step is a downside risk to the house 2027 FCF of $23bn | **BBG cons capex CY26 $148.5B / CY27 $184.1B (hi 358); EPS CY26 $36.38 / CY27 $40.39. A >5GW-in-1H26 pace points to the upper end** | **Capex-upside / FCF-downside tension.** If Meta contracts >5GW in H1 alone and accelerates self-build, the house 2027 FCF looks high. Stress-test the FCF line against a higher 2027 capex. |
| **ANTHROPIC** (private) | SemiAnalysis: **+$21B net-new ARR to ~$30B** (from ~$9B), inference GM **mid-60s** (from ~38% 2025, −94% 2024), OI-profitable in 2Q ex-SBC, >$100B ARR potential by year-end (SemiAnalysis "Bedrock Mix", 05-27) | If the prior wiki ARR figure was materially below $30B, this is a large upward revision | No house/BBG (private) | n/a | **The engine behind the AWS margin story.** The GM ramp (38%→mid-60s) is the reconciling variable — it's what lets Bedrock/Claude lift AWS EBIT +213bp. Verify the prior ARR anchor on the page; if stale, this is a step-change. |
| **SKHYNIX / SAMSUNG** | MS Korea: SK hynix **+KRW1,000tn** AI-DC capex (nearly doubled commitment); Samsung extended chip/HBM plan; Korea "Three Mega Projects" ~KRW2,000tn/$1.5tn (MS "S. Korea Industrial Strategy", 07-01) | On-page already carry JPM ~$3.1tn and DIGITIMES KRW2,655tn for the **same June-29 announcement** — different scopes, NOT merged | No house model | **Not a BBG estimate line — "+KRW1,000tn" is a multi-year national AI-DC commitment, not annual capex (BBG annual capex: SKHY CY26 KRW47.8tn / CY27 KRW60.9tn; Samsung KRW75.6tn / 88.4tn). Scope mismatch — not resolvable to one cons number** | **Scope divergence across brokers on one announcement** — flagged on-page, not reconciled to a single number. The signal is the capex-commitment direction, not the headline size. |

## CONFIRMS (no action)

| Name | New datapoint (source) | Baseline | Note |
|---|---|---|---|
| **TSM** | UBS reiterate **Buy, PT NT$3,400**; N2 ~220kwpm by 2028; capex $60/80/95bn ('26/27/28); server-CPU = ~$44bn rev opp by 2030 (~11% of sales); +62% YTD (UBS, 07-02) | House rev $165bn/2026, EPS 102.5/143.5 ('26/'27); PT/thesis already on page | Reiteration; folded as flow. Server-CPU $44bn is incremental-TAM color, not a P&L change. No drift. |
| **MU** | MS OW, **PT $1,200**, <10x P/E, buybacks 2027, earnings power beyond 2027 (MS "NAND Outlook", 07-02) | Matches PT already on page | Additive; confirms the durable-cycle thesis. |
| **SNDK** | MS OW, **PT $1,750**, <10x, buybacks 2027 (+Fadu eSSD-controller angle) (MS, 07-02) | Matches PT already on page | Additive. Net-new item is the Fadu supply relationship, not a number. |
| **SAMSUNG** | MS OW, **DRAM Top Pick**; 20-30% DRAM price hikes 3Q26; 5.2x 2027e P/E; prefers DRAM > NAND (MS, 07-02) | Consistent with existing bullish-DRAM comments on page | No house model; BBG cons PT KRW 504.9k (005930 KS). Confirms (MS OW, no PT quoted in this row). |
| **KIOXIA** | MS **Top Pick** (Japan semis); FCF ¥4.0-5.0trn FY3/27-28; LTAs >50% CY27 (MS, 07-02) | New coverage-depth on page | Confirms shareholder-return thesis. No house/BBG. |
| **AMZN** | AWS EBIT **+213bp Q/Q**; Bedrock ~$5.5B run-rate = 37% of AWS AI rev, ~30% of Y/Y GP-$ step-up on ~4% of rev (SemiAnalysis, 05-27) | Consistent with the "AWS re-accelerating" thread | Margin driver, not a house-line change. Confirms + upgrades the Sinal margin row. |
| **LITE** | UBS: optical-transceiver SAM 22% CAGR **$12bn→$32bn** 2025-30E; CPO ~$7bn/~20% by 2030E; scale-up GPU-CPO ~2029E (UBS, 07-02) | House rev 4.2/8.1 ('26/'27), EPS 12.81/30.02 | TAM direction supportive; CPO timing (2029E scale-up) is the risk to out-years, not a near-term cut. Confirms. |
| **INTC / AMD / ARM** | UBS server-CPU unit share: Intel **60%→29%**, AMD **24%→29%**, ARM **16%→42%** by 2030E (UBS, 07-02) | ARM/Intel path **reiterates** UBS's own 05-21 note already on-page | Reiteration; no figure superseded. |

---

## Qualitative / thematic (logged to pages & themes, not reconciled)
- **Advanced packaging (ECTC 2026):** Intel EMIB-T (TSVs, tighter bump pitch, glass-core panel) positioned as "most credible alternative to TSMC CoWoS," expected in Google TPU v9; TSMC+Microsoft microfluidic direct-to-silicon cooling; Marvell custom HBM4E (interposer routing 6.5→1.5mm). → cowos-packaging, hbm-memory, optical-cpo, custom-asic-tpu, INTC, TSM, MRVL, MSFT.
- **TPU dual-track mechanics:** Google runs Broadcom v8i + MediaTek v8t into the v9 ramp (2028); total TPU units 4.8m→10.7m 2026/27E. → custom-asic-tpu, GOOG, AVGO, MEDIATEK.
- **GCP margin "illusion":** SemiAnalysis argues GCP OPM is flattered because DeepMind training sits in Alphabet-level activities ($5.4B 1Q26 vs $3.0B 1Q25), not the GCP segment — a quality-of-margin flag against the house GOOG OPM 36%/37% ('26/'27). → GOOG, hyperscaler-capex.
- **Off-coverage NAND PT changes (MS):** Longsys Rmb300→673, SIMO $155→400, Phison NT$2,248→2,588, Fadu (OW, W300bn+ secured). → outros-asia.

## Action items
1. ✅ **BBG PENDING column filled 2026-07-13.** MEDIATEK UBS NT$6,500 is +30% above cons NT$5,014 (2454 TT). META cons capex CY27 $184.1B (a >5GW-1H26 pace points higher, FCF risk). AVGO house 26/27 EPS ≈ cons; the 2028 share-cede risk has no BBG CY28 line to place. SK Hynix/Samsung "+KRW1,000tn" is a multi-year national commitment, not an annual capex line (scope mismatch).
2. **MEDIATEK** — no house model exists; the NT$6,500 Key Call warrants a house init or at least a scenario bridge on the TPU ASIC revenue ($18/35bn 27/28).
3. **META** — stress the house 2027 FCF ($23bn) against a higher 2027 capex given >5GW contracted in H1'26 alone.
4. **AVGO** — bridge the house 2028 EPS ($35.96) against the 62%-and-declining TPU ship-share path.

_BBG column resolved 2026-07-13 — estimates.json asof 2026-07-13; consensus target prices pulled live via BEST_TARGET_PRICE (Bloomberg wrapper). Segment-level items (AI-semis, ASIC) and national capex commitments have no BBG consensus line and are marked as such._
