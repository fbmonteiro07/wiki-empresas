# Wiki remediation worklist

_Generated 2026-06-30 · closes the loop on `lint_wiki.py` / staleness.md. Rebuild: `py _wiki/_tools/remediate.py`._

## 🔴 BBG estimates missing (98) — scriptable

Run (BBG Terminal must be logged in) — `fetch_estimates.py` merges, so this is safe:

```
py "E:\.claude\scripts\fetch_estimates.py" AAOI AAPL ADI ADVANTEST AGX AIXA AKAM ALAB AMAT AMD AMZN ANET AOSL APH APP ARM ASML AVGO AXTI BE BESI BKNG CDNS CEG CEREBRAS CIEN COHR CRDO CRM CRWD CRWV CSCO DELL DISCO ETN FLEX FSLY GEV GLW GOOG HPE IFX INTC KIOXIA KLAC LITE LRCX MCHP MEDIATEK META MP MRVL MSFT MU NBIS NET NFLX NOW NVDA NVT NVTS NXPI ON ORCL PANW PLTR POET POWI PWR QCOM RDDT SAMSUNG SANM SHOP SKHYNIX SMCI SMIC SNDK SNPS SPOT STX TEL TER TLN TM TOKYOELEC TSEM TSLA TSM TXN UBER VECO VEEV VRT VST WDC WMB WOLF
```

Or auto: `py _wiki/_tools/remediate.py --run-estimates`

AAOI, AAPL, ADI, ADVANTEST, AGX, AIXA, AKAM, ALAB, AMAT, AMD, AMZN, ANET, AOSL, APH, APP, ARM, ASML, AVGO, AXTI, BE, BESI, BKNG, CDNS, CEG, CEREBRAS, CIEN, COHR, CRDO, CRM, CRWD, CRWV, CSCO, DELL, DISCO, ETN, FLEX, FSLY, GEV, GLW, GOOG, HPE, IFX, INTC, KIOXIA, KLAC, LITE, LRCX, MCHP, MEDIATEK, META, MP, MRVL, MSFT, MU, NBIS, NET, NFLX, NOW, NVDA, NVT, NVTS, NXPI, ON, ORCL, PANW, PLTR, POET, POWI, PWR, QCOM, RDDT, SAMSUNG, SANM, SHOP, SKHYNIX, SMCI, SMIC, SNDK, SNPS, SPOT, STX, TEL, TER, TLN, TM, TOKYOELEC, TSEM, TSLA, TSM, TXN, UBER, VECO, VEEV, VRT, VST, WDC, WMB, WOLF

## 🟡 No transcript on disk (19) — needs the transcript-fetcher agent

Spawn one `transcript-fetcher` task per name (paste into Claude Code):

- **AKAM** — "get the latest AKAM earnings transcript -> `E:\Wiki Felipe empresas\AKAM\transcripts\`"
- **AOSL** — "get the latest AOSL earnings transcript -> `E:\Wiki Felipe empresas\AOSL\transcripts\`"
- **APP** — "get the latest APP earnings transcript -> `E:\Wiki Felipe empresas\APP\transcripts\`"
- **AXTI** — "get the latest AXTI earnings transcript -> `E:\Wiki Felipe empresas\AXTI\transcripts\`"
- **BE** — "get the latest BE earnings transcript -> `E:\Wiki Felipe empresas\BE\transcripts\`"
- **CDNS** — "get the latest CDNS earnings transcript -> `E:\Wiki Felipe empresas\CDNS\transcripts\`"
- **CEREBRAS** — "get the latest CEREBRAS earnings transcript -> `E:\Wiki Felipe empresas\CEREBRAS\transcripts\`"
- **ETN** — "get the latest ETN earnings transcript -> `E:\Wiki Felipe empresas\ETN\transcripts\`"
- **FSLY** — "get the latest FSLY earnings transcript -> `E:\Wiki Felipe empresas\FSLY\transcripts\`"
- **MP** — "get the latest MP earnings transcript -> `E:\Wiki Felipe empresas\MP\transcripts\`"
- **NET** — "get the latest NET earnings transcript -> `E:\Wiki Felipe empresas\NET\transcripts\`"
- **PLTR** — "get the latest PLTR earnings transcript -> `E:\Wiki Felipe empresas\PLTR\transcripts\`"
- **POET** — "get the latest POET earnings transcript -> `E:\Wiki Felipe empresas\POET\transcripts\`"
- **POWI** — "get the latest POWI earnings transcript -> `E:\Wiki Felipe empresas\POWI\transcripts\`"
- **SANM** — "get the latest SANM earnings transcript -> `E:\Wiki Felipe empresas\SANM\transcripts\`"
- **SNPS** — "get the latest SNPS earnings transcript -> `E:\Wiki Felipe empresas\SNPS\transcripts\`"
- **TSEM** — "get the latest TSEM earnings transcript -> `E:\Wiki Felipe empresas\TSEM\transcripts\`"
- **TSLA** — "get the latest TSLA earnings transcript -> `E:\Wiki Felipe empresas\TSLA\transcripts\`"
- **VEEV** — "get the latest VEEV earnings transcript -> `E:\Wiki Felipe empresas\VEEV\transcripts\`"

## ⚪ Private — intentionally skipped (3)

ANTHROPIC, OPENAI, SPCX

