# Reconciliation — 2026-09-24 (night, /run-inbox 23h — 3rd run of the day)

_Scope: every NEW quantitative datapoint from the one source processed this run — **Deutsche Bank · Brad Zelnick / Nasr Islam, "Okta — Thoughts from Oktane 2026", 2026-09-24** ([source](../../relat%C3%B3rios%20bons/01M38KWPD18W275GYHBJDQXZ6C.html)). Datapoints already reconciled from DB's flash in the 21h run are not repeated._

**Baselines.**
- **Prior wiki:** [OKTA](../OKTA.md) live ladder — Barclays OW $215 (09-23) · MS OW $200 (09-24) · Bernstein Market-Perform $174 (09-17) · DB (was mis-recorded as "Buy (05-29)").
- **House model:** none for OKTA (`house.json`) — column N/A, not left blank by oversight.
- **BBG consensus:** on-disk snapshot `_wiki/_data/estimates.json`, `asof = 2026-09-24` (same day) — used as the live baseline, NOT pending. px $209.92; consensus PT $205.88 (n=47, lo $127 / hi $250; 37 Buy / 10 Hold / 0 Sell); EV $34,454m; CY2027 revenue $3,518.6m.

## DIVERGES (the alpha)

| # | New datapoint | Prior wiki | House | BBG | Read |
|---|---|---|---|---|---|
| D1 | **DB rating history: Hold since 2024-11-12; Hold $105 on 2026-05-29; Hold $150 set 2026-08-27** (DB p.5 table) | Stance line: **"DB Buy (05-29)"**; 21h block: "First DB mark on this page" | N/A | BBG hold count 10 (consistent with DB being one of the Holds) | 🔴 **The wiki was wrong, not the Street.** Corrected on the page with the old value in `## Changelog`. Any past "unanimous-ish Buy" reading of the OKTA ladder that counted DB as a Buy overstated bullishness by one house. |
| D2 | **DB PT $150** (reaffirmed) | Ladder low was Bernstein $174 | N/A | **−27.1% vs cons $205.88**; above BBG low $127 | Lowest target on the wiki's ladder, but NOT the Street low — at least one un-ingested house sits at $127. **Recover who owns the $127.** |
| D3 | **Agent-product price ≈ 75% uplift on core** (one Energy CISO: $1.5m/yr vs $2m core; beta since Dec) | Mgmt (via DB/MS): 30-50% ACV uplift on attach | N/A | No BBG field | ⚠️ Single account, beta pricing, a quote. Above mgmt's range — but DB uses it to argue pricing is **fragile** (competition coming), not conservative. Directional only; not written to any estimate. |
| D4 | **Renewal pull-forward: Jan-2027 renewal pulled into Aug-2026** (VAR #3) | Bernstein 09-19: Flex contracts flattering ARR "for the next quarter or two" | N/A | 1FQ (Q3-26E, i.e. F3Q27) revenue $816.0m | Qualitative but directly bears on the F3Q27 cRPO print (~2026-12-02): cRPO beat without sub-revenue acceleration = DB/Bernstein bear case. Adds a second, independent mechanism to the same-direction risk. |

## CONFIRMS (no action)

| # | New datapoint | Baseline | Read |
|---|---|---|---|
| C1 | DB price $205.36 (23-Sep close) | Same close used by MS today; BBG snapshot px later updated to $209.92 | ✅ Same tape |
| C2 | DB *"~10x EV/Revenue (CY27)"* | BBG EV $34,454m / CY2027 rev $3,518.6m = **9.8x** | ✅ Confirms |
| C3 | Shares *"up nearly 140% YTD"* | DB's own history: $79.65 close (2026-03-05) → $205.36 | ✅ Plausible; not independently checked vs 31-Dec close |

## Not reconciled (no quantitative content)
Buyer-named competitive set (CyberArk/SailPoint/Saviynt/BeyondTrust), Ping-wedge cross-sell, OIG/OPA not trialled by 50k-seat customers, $17 mid-market bundle — qualitative; logged on [OKTA](../OKTA.md) and [ai-cybersecurity](../themes/ai-cybersecurity.md).
