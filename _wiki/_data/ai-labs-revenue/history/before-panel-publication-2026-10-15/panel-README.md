# Capstone Wiki

Buyside dashboards — semis, AI infrastructure and AI labs. Live site published via GitHub Pages:
**https://fbmonteiro07.github.io/Capstone-Wiki/**

## Dashboards

| Pasta | Dashboard | Conteúdo |
|---|---|---|
| [`wiki-map/`](wiki-map/) | Wiki Map & Repo State 🗺️ | Sector map da wiki de research (101 páginas/14 setores), grafo interativo da supply chain, inventário do acervo, thesis drift semanal + roadmap (snapshot 02-Jul-26) |
| [`ai-labs/`](ai-labs/) | AI Labs 🧪 | OpenAI & Anthropic estimated PnL (WFS) — revenue build, compute spend, EBIT bridges 2023-2030, ARR tracker, valuation |
| [`openrouter-vercel/`](openrouter-vercel/) | OpenRouter + Vercel | Gateway adoption, token share and weekly research; opens the internal research wiki. |
| [`gpu-pricing/`](gpu-pricing/) | GPU rental pricing | Bloomberg / Silicon Data and SemiAnalysis public indices, H100 one-year ranges; opens the internal research wiki. |
| [`capex-cloud/`](capex-cloud/) | Capex Cloud ☁️ | Hyperscaler capex (MSFT/AMZN/GOOGL/META/ORCL) — BBG consensus, revision tracker, PP&E breakdown, XLSX download |
| [`wfe/`](wfe/) | Claude WFE ✨ | Scenario-driven WFE — Capstone vs UBS vs live Street, EUV cost model, scenario valuation |
| [`semicap/`](semicap/) | Semicap | SemiCap peer overview, metrics and charts (+ `capex-flow.html` sub-page) |
| [`rack-bom/`](rack-bom/) | NVL72 B.O.M. | GB200/GB300/VR200 bill of materials per rack (MS, Bernstein) |
| [`odm-csp/`](odm-csp/) | ODM - CSP | ODM ↔ client flux 2026 — rack units, Sankey by quarter |
| [`gw-designer-valuation/`](gw-designer-valuation/) | GW per Designer & Valuation | GW added per designer 2025-27 — Capstone models vs SemiAnalysis |

## Convenções

- **Pastas em kebab-case** (sem espaços — URL limpa no Pages), uma pasta por dashboard
- **Página principal = `index.html`** dentro da pasta → URL termina na pasta (ex.: `/capex-cloud/`)
- Arquivos de dados (`.js`/`.json`/`.xlsx`) ficam **ao lado da página** que os carrega (referência relativa)
- Novo dashboard = nova pasta + um card no [`index.html`](index.html) da raiz + linha nesta tabela
- URLs antigas (pré-reorganização de jun-2026) redirecionam via [`404.html`](404.html)
