<!-- Model card. Registered in _meta/models.md. -->

# Model — Memory Supply/Demand Base Case

**File:** `E:\AI_Demand_Capex\Memory_Supply_Demand_Basecase.xlsx` · **built 2026-07-06** · owner: Felipe (built with Claude) · audited 2x via /double-check (transcription PASS; comparisons PARTIAL→fixed)

## What it answers
The house base case for DRAM / NAND / HBM supply-demand, pricing and vendor revenue, 2025→CY28E. Anchored on **UBS Memory Semis Monthly (3-Jul-2026)** (full transcription, quarterly Q1'25→Q4'27E) + house extensions.

## Key tabs
- **Memory Bible** — master reference (units, base case, pricing, HBM, server DRAM, capex tension, refresh loop)
- **Scenarios** — toggle B3: UBS Base / Soft-BofA / House price paths → drives Vendor P&L
- **Vendor P&L** — implied Samsung / SK Hynix / Micron / Kioxia / SanDisk / YMTC / CXMT memory revenue vs consensus (consensus PENDING BBG); sensitivity ~+$10bn MU revenue (≈+$5.8 EPS) per +$1/GB DDR
- **DRAM S-D / NAND S-D** — UBS quarterly supply/demand/ASP/sufficiency with cross-Street commentary (col R)
- **Demand | HBM (house)** — AI Model units × HBM GB/chip → house HBM bits/$ (≈UBS by '27); HBM-specific sufficiency (HBM in SURPLUS while DDR starves)
- **Demand | Server DRAM (house)** — CPU attach build (user ratios: 1:1 by CY28 → 22.5 EB); two pricing worlds
- **Pricing | history & fwd** — inSpectrum monthly $/GB history 2019→Jul-26 (hidden `_px_monthly` feeds charts) + UBS forward
- **Supply | capacity & capex** — DDR wafers FLAT vs HBM 3.3x; capex/revenue collapse to ~7-9%; cycle-top watch list
- **Print tracker** — each memory print vs the model path (fill verdicts; mirror into edge outcomes)

## Canonical numbers (UBS base)
DRAM revenue $151→$692→$1,248bn ('25/'26E/'27E); NAND $65→$300→$515bn; HBM $33→$63→$169bn; DDR ASP $3.2→$14.2→$21.4/GB; sufficiency '26E: DRAM −8.1% / NAND −9.3% / **HBM +10.2%** (shortage is conventional DRAM, not HBM).

## Refresh
Monthly UBS note → retranscribe S-D tabs · Terminal on: inSpectrum via `P:\Felipe Monteiro\US Equities\_pull_memory_prices*.py` + BBG consensus (MU / 000660 KS / 005930 KS) into Vendor P&L · after each print: Print tracker verdicts.

## Related
[MU](../MU.md) · [SKHYNIX](../SKHYNIX.md) · [SAMSUNG](../SAMSUNG.md) · [KIOXIA](../KIOXIA.md) · [SNDK](../SNDK.md) · theme: [hbm-memory](../themes/hbm-memory.md) · linked models: AI Model (comentado), AI_Chip_Designers_TAM.xlsx
