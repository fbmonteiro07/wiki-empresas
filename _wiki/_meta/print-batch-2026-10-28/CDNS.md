# CDNS — Q3 FY26 print-night report (2026-10-28)

**1. Print.** Revenue $1.633bn (+22% y/y), above the $1.595-1.625bn guide (range via JPM TMT desk, 10-02); non-GAAP OpM 44.1% (guide 43.5-44.5%), EPS $2.11 (guide $2.01-2.07). GAAP missed the GAAP guide on an unguided $42.2m Sep-2026 restructuring (10-Q). Core EDA +20%, IP +24% (Q2 +40%), SD&A +30%; recurring +18% (Q2 ~20%); record backlog $8.2bn, cRPO $4.2bn flat. FY26 raised to $6.387-6.417bn (~21%) / OpM 44.7% mid / EPS $8.40 (from $6.30bn / 44.25% / $8.10); Q4 $1.695-1.725bn. Unscored vs Street: no Q3 consensus on disk (CDNS PR + CFO commentary + call, 2026-10-26; 10-Q filed 2026-10-28).

**2. Sections edited.** Current state (new Q3 block on top), Debate (dated bullet), Catalysts (Q3 bullet marked ✅ RESOLVED + 3 new), Intra-quarter (Q2 window archived word for word as `### ARCHIVED — Q2 FY26 intra-quarter window (2026-07-27 → 2026-10-26)`; new window + Sinal table), Sources, Changelog. Superseded → Changelog: the FY26 guide legs, backlog $8.1→8.2bn, beginning-backlog share ~65→~64%, China 15→16%, recurring 18-20%→18%, IP +40→+24%, ">20"→">100" engagements (scope differs), 48x sourcing. The page has no "Management commentary — evolution" section, so none was created.

**3. outcomes.md:** `- CDNS 2026-10-26 — neutral — Q3 FY26 beat-and-raise (FY26 ~21%, EPS $8.40, backlog $8.2bn) beat the top of the guide, but recurring slowed to 18% from ~20%, agentic revenue still unsized, FY OpM mid 44.7% < GS 45.4%; preliminary, no post-print tape`

**4. Compute deals:** none. Switch adopting Millennium/Reality Digital Twin is design software, with no MW or $ attached.

**5. Theme read-throughs**
- custom-asic-tpu: Devgan says "Google and now Meta and Microsoft and Amazon and Tesla" are doing more designs, and system companies are 45% of the business (call, 10-26).
- china-export: the BIS 50%-affiliates rule suspension runs to 2026-11-09; an extension is expected but not yet formalised. CDNS China +4% y/y, 16% of revenue (10-Q, 10-28).
- semicap-wfe / [[TSM]]: Devgan cites a TSMC roadmap slide shown at imec: chip size up 48x in five years from scaling plus 3D-IC/wafer-scale (call, 10-26).
- hbm-memory: verification usage is growing "at major hyperscaler and memory companies" (call, 10-26).
- [[SNPS]]: analysts (Needham's Charles Shi, MS's Lee Simpson) compare Maestro (Cadence's own post-trained models) with GPT-Synopsys. CDNS says it now has royalties in design IP, against SNPS's royalty pitch. CDNS hardware posted another record quarter. CDNS IP slowed to +24%, a mixed read for SNPS IP comps.

**6. 🔭 Variant perception**
- Royalty: the page's 04-29 expert call says there is "no royalty model on interface IP". Devgan now says design IP carries royalties, and 10-Q royalties were $34.9m vs $22.7m a year ago.
- 48x: the page logged an unsourced "complexity" claim. Devgan now attributes it to a TSMC chip-size projection, still second-hand.
- IP: DAMNANG's trigger (1), IP growth above 30%, fired in Q2 but reversed in Q3 (+24%).
- Margin and visibility: Q3 OpM was down 350bp y/y, and the Q4 guide sits below Q4'25's 45.8%. Only ~64% of FY26 revenue comes from beginning backlog, versus SemiAnalysis's "~67% coverage" framing, so more depends on in-year hardware and IP.

**7. Garbles.** In the transcript, Wall's FY26 margin reads "44.10%"; the CFO commentary gives 44.7%. Arya's "compound it to 30%" most likely means "through 2030"; it was not used on the page. Neither was added to the glossary.

**8. Open items.** The Q3 revenue guide range comes only from the JPM desk relay, because the Q2 CFO commentary is not on disk. There is no Q3 Street consensus and no post-print broker note on disk. Segment $ figures are derived from the rounded mix × growth. Mobley's 26% bookings growth is his own estimate. The Q2 window was moved with a guarded Python splice (line endings preserved; no original line lost, verified against HEAD). `transcript_qa.py --pages _wiki/CDNS.md` returned 0 flagged hits. The repo-wide `--diff` scan did not finish within ~10 min across all pages, so I stopped it.
