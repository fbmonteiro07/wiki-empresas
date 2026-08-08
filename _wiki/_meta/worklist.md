# Wiki remediation worklist

_Generated 2026-08-07 · closes the loop on `lint_wiki.py` / staleness.md. Rebuild: `py _wiki/_tools/remediate.py`._

## 🔴 BBG estimates missing (1) — scriptable

Run (BBG Terminal must be logged in) — `fetch_estimates.py` merges, so this is safe:

```
py "E:\.claude\scripts\fetch_estimates.py" AEIS
```

Or auto: `py _wiki/_tools/remediate.py --run-estimates`

AEIS

## 🟡 No transcript on disk (16) — needs the transcript-fetcher agent

Spawn one `transcript-fetcher` task per name (paste into Claude Code):

- **AEIS** — "get the latest AEIS earnings transcript -> `E:\Wiki Felipe empresas\AEIS\transcripts\`"
- **AKAM** — "get the latest AKAM earnings transcript -> `E:\Wiki Felipe empresas\AKAM\transcripts\`"
- **AOSL** — "get the latest AOSL earnings transcript -> `E:\Wiki Felipe empresas\AOSL\transcripts\`"
- **APP** — "get the latest APP earnings transcript -> `E:\Wiki Felipe empresas\APP\transcripts\`"
- **AXTI** — "get the latest AXTI earnings transcript -> `E:\Wiki Felipe empresas\AXTI\transcripts\`"
- **BE** — "get the latest BE earnings transcript -> `E:\Wiki Felipe empresas\BE\transcripts\`"
- **ETN** — "get the latest ETN earnings transcript -> `E:\Wiki Felipe empresas\ETN\transcripts\`"
- **FSLY** — "get the latest FSLY earnings transcript -> `E:\Wiki Felipe empresas\FSLY\transcripts\`"
- **MP** — "get the latest MP earnings transcript -> `E:\Wiki Felipe empresas\MP\transcripts\`"
- **NET** — "get the latest NET earnings transcript -> `E:\Wiki Felipe empresas\NET\transcripts\`"
- **PLTR** — "get the latest PLTR earnings transcript -> `E:\Wiki Felipe empresas\PLTR\transcripts\`"
- **POET** — "get the latest POET earnings transcript -> `E:\Wiki Felipe empresas\POET\transcripts\`"
- **POWI** — "get the latest POWI earnings transcript -> `E:\Wiki Felipe empresas\POWI\transcripts\`"
- **SNPS** — "get the latest SNPS earnings transcript -> `E:\Wiki Felipe empresas\SNPS\transcripts\`"
- **TSEM** — "get the latest TSEM earnings transcript -> `E:\Wiki Felipe empresas\TSEM\transcripts\`"
- **VEEV** — "get the latest VEEV earnings transcript -> `E:\Wiki Felipe empresas\VEEV\transcripts\`"

## ⚪ Private — intentionally skipped (6)

ANTHROPIC, CEREBRAS, GOOG, MSFT, OPENAI, SPCX

