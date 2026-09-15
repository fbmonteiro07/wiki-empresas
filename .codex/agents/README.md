# Wiki research agents

Created 2026-09-14. Four project-scoped Codex agents inherit the calling task's model, reasoning, tools, and permissions. Shared evidence and recordkeeping rules: [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).

| Agent | Job | Example request |
|---|---|---|
| [thesis-challenger](thesis-challenger.toml) | Challenge a thesis and adjudicate contrary evidence. | "Use thesis-challenger to challenge our MU thesis and identify what would invalidate it." |
| [readthrough-investigator](readthrough-investigator.toml) | Investigate effects across customers, suppliers, and competitors; recognizes "readtru". | "Use readthrough-investigator on this disclosure and verify which other companies are affected." |
| [forecast-scorekeeper](forecast-scorekeeper.toml) | Preserve forecast vintages and compare with matching results. | "Use forecast-scorekeeper to compare our pre-earnings forecasts with reported results." |
| [research-director](research-director.toml) | Actively answer open questions and pursue accessible evidence. | "Use research-director to solve the open questions in our AI-capex debate, starting with the wiki's evidence." |

The research director must return answers or substantive partial answers with precise gaps. A prioritized to-do list alone does not complete its job. It coordinates available specialists when delegation is authorized and collects/adjudicates their results.

## Records and outputs

- Dated memos/cards: _wiki/_meta/research-agents/<agent-name>/<run>/.
- Question register, owned by research-director: _wiki/_data/research/questions.json.
- Forecast/actual/evaluation register, owned by forecast-scorekeeper: _wiki/_data/research/forecasts.json.
- Registers start empty. Installation does not claim any question answered or forecast scored.
- Cards are handoffs to the parent; the existing Analyst Inbox does not yet import them automatically.

Use the role's name in a request within this wiki project. These are agent names, not newly registered slash commands. If an already-open task does not expose a new role, start a fresh task in this project to load its agent catalog. Installation schedules no recurring runs.

## Configuration reference

The [official OpenAI custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) describes project definitions under .codex/agents/ and the required name, description, and developer_instructions fields. These agents use those fields without changing global configuration.
