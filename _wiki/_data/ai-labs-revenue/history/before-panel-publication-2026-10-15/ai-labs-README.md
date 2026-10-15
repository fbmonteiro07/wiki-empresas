# AI Labs — OpenAI & Anthropic PnL

Página estática com o PnL estimado dos AI labs (estimativas Wells Fargo Securities), extraído do workbook `oAI and Anth.xlsx` em 11-jun-2026.

## Conteúdo

- **index.html** — dashboard com 6 abas:
  - **Overview** — KPIs (valuation, receita, EBIT, gross margin, compute spend 2026E), gráfico de ARR mensal (jan-25 a dez-26) e comparativo anual de P&L 2023-2030
  - **Anthropic Summary** / **OpenAI Summary** — as Summary Views do workbook (Compute & Cost view, P&L summary, Valuation view, notas)
  - **Anthropic PnL** / **OpenAI PnL** — abas completas de PnL da WFS (revenue build, custos de compute treino/inferência, opex, EBIT, com memos das fontes)
  - **ARR Tracker** — build mensal de ARR → receita reconhecida das duas empresas
- **data.json** — dump bruto das 5 abas (texto formatado como exibido no Excel, pt-BR)

## Destaques (2026E, USD)

| | OpenAI | Anthropic |
|---|---|---|
| Valuation (post-money) | $852B | $380B |
| Receita | $30,5B net ($38,8B gross) | $66,9B |
| Gross Margin | 53,7% | 61,9% |
| EBIT ex-SBC | -$31,2B | +$12,4B |
| Compute total | $48,2B | $38,4B |

Valores em USD milhões, formatação pt-BR (ponto = milhar, vírgula = decimal). EBIT exclui SBC; custo de treino 100% despesado no período (framework WFS).
