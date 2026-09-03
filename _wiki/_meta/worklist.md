# Wiki remediation worklist

_Generated 2026-09-03 · closes the loop on `lint_wiki.py` / staleness.md. Rebuild: `py _wiki/_tools/remediate.py`._

## 🔴 BBG estimates missing (1) — scriptable

Run (BBG Terminal must be logged in) — `fetch_estimates.py` merges, so this is safe:

```
py "E:\.claude\scripts\fetch_estimates.py" AEIS
```

Or auto: `py _wiki/_tools/remediate.py --run-estimates`

AEIS

## 🟡 No transcript on disk (2) — needs the transcript-fetcher agent

Spawn one `transcript-fetcher` task per name (paste into Claude Code):

- **POET** — "get the latest POET earnings transcript -> `E:\Wiki Felipe empresas\POET\transcripts\`"
- **SMTC** — "get the latest SMTC earnings transcript -> `E:\Wiki Felipe empresas\SMTC\transcripts\`"

## ⚪ Private — intentionally skipped (8)

ANTHROPIC, CEREBRAS, GOOG, INTC, MSFT, OPENAI, QCOM, SPCX

