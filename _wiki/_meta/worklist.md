# Wiki remediation worklist

_Generated 2026-09-23 · closes the loop on `lint_wiki.py` / staleness.md. Rebuild: `py _wiki/_tools/remediate.py`._

## 🔴 BBG estimates missing (1) — scriptable

Run (BBG Terminal must be logged in) — `fetch_estimates.py` merges, so this is safe:

```
py "E:\.claude\scripts\fetch_estimates.py" NSCALE
```

Or auto: `py _wiki/_tools/remediate.py --run-estimates`

NSCALE

## 🟡 No transcript on disk (3) — needs the transcript-fetcher agent

Spawn one `transcript-fetcher` task per name (paste into Claude Code):

- **NSCALE** — "get the latest NSCALE earnings transcript -> `E:\Wiki Felipe empresas\NSCALE\transcripts\`"
- **POET** — "get the latest POET earnings transcript -> `E:\Wiki Felipe empresas\POET\transcripts\`"
- **SMTC** — "get the latest SMTC earnings transcript -> `E:\Wiki Felipe empresas\SMTC\transcripts\`"

## ⚪ Private — intentionally skipped (14)

ANTHROPIC, AVGO, CEREBRAS, CRM, GOOG, INTC, MDB, MSFT, OKTA, OPENAI, ORCL, QCOM, SNOW, SPCX

