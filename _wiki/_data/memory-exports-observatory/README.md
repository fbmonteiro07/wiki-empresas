# Memória coreana: exportações e ASP

## Long-history Memory Observatory — 28 October 2026

`tracker.html` is now the self-contained interactive dashboard, mirrored to `_wiki/_dashboards/memory-exports-tracker.html`. The original weekly layout remains at `tracker-legacy.html`. The two wiki hubs are unchanged.

Actual coverage: KCS core exports and BOK dollar price indices January 2010–September 2026 (201 months); flash/SSD composition index January 2014 onward; Hynix disclosures from 2010Q1; Samsung from 2016Q4. InSpectrum contains 26 distinct raw price specifications, including legacy DDR3 and MLC histories exceeding ten years. Modern DDR5 and newer TLC baskets have shorter coverage. No generation splicing or gap filling is used.

The dashboard provides 35 benchmark histories, 156 company/product/information-set/lag models, fixed regime checks, chronological predictions, same-sample baselines, direction confusion matrices, turning-point tests, six spot/contract pairs, trade-flow decomposition, source ledgers, downloads and a saved theme. Historical MAE-advantage ranges use gap-aware paired block resampling. They are not probabilities for a future quarter. The worked calculation and window/band sensitivity are in the Company ASP lab.

106 recovered targets were appended from original Hynix releases and Samsung IR scripts; all 104 previous records are preserved. The protocol is `MEMORY_DASHBOARD_PROTOCOL.md`; data and code before expansion are under `audit/2026-10-28/long_history/before`; original-source research and independent reproduction are under `research/` and `skeptic/` in that audit directory. Missing Hynix 2022Q4 quantitative ASP remains a disclosed limitation. Older NAND predates Solidigm; modern DRAM includes HBM.

Rebuild and mirror with `py weekly_tracker.py --offline --force-rebuild`. The BOK and market-price collectors now request history from 2010; KCS preserves the backfill while refreshing its recent overlap. The observatory rebuilds as part of the existing routine. `build_tracker.py` writes the legacy monitor; `analyze_dashboard.py` and `build_dashboard.py` produce the new main page. Verification: `py -m unittest test_monitor test_extensions test_pricing test_earnings_refit test_dashboard`.

The dated earnings refit below retains its original shorter-history numbers. Those are a frozen earlier model vintage, not the coefficients of the newly expanded study.

## Earnings refit — 28 October 2026

The SK hynix Q3 earnings deck (28 October, p.4, visually verified) is now in the corporate ASP ledger: DRAM **high-20%** and NAND **mid-20%** QoQ. These are HARD source wordings; the existing analyst convention maps them to PARTIAL bands **27–29% / 24–26%**, midpoints **28% / 25%**. NAND includes Solidigm; DRAM is blended including HBM. Prior observations are unchanged.

The frozen 26 October model had Q3 Hynix DRAM **+8.54%**, versus the normalized 28% midpoint, and NAND **+24.02%**, versus 25%. Adding Q3 gives in-sample fitted values **+9.30% / +24.13%**. These are calibration results, not new forecasts. The chronological Q3 test still trains only through Q2. The pricing extension now includes a disclosed latest complete quarter in calibration and suppresses its live forecast, consistent with the main model.

The tracker, report and pricing study show the frozen prediction, reported band, error, updated coefficients, comparable MAEs, target-normalization sensitivity and training-window sensitivity. The latter is materially wider: KCS DRAM fitted Q3 spans **4.80–13.51%** across pre-defined windows. Historical coverage remains incomplete (both products 2022Q4; NAND 2022Q3 open-ended), DDR5 has only one full-quarter Hynix holdout, and the latest-vintage backtest is not a historical publication-vintage test. Operational forecasts remain blocked.

Current Street ledger: **JPM / Joseph Cardoso, Manmohanpreet Singh and Marc Vitenzon, 26 October**, relaying TrendForce, Q4 conventional DRAM **+10–15%** and NAND **+15–20%** QoQ contract prices. **Jefferies / Conor O'Mara, 28 October notes of Harald Lee's 22 October expert call**, says Q4 DRAM nearly +20%. Company actuals, sector contract-price forecasts and fixed InSpectrum baskets are distinct. Broker forecasts do not enter the regression targets. The old September ledger is retained in `data/street_calls_history_2026-09-15.json`; Q3 sector readings and 2027 qualitative context have separate arrays in the new ledger. No Q4 company ASP forecast is issued before a complete October input month; partial October spot remains separate.

Rebuild: `py weekly_tracker.py --offline --force-rebuild`. The dated `data/refit_2026-10-28.json` is frozen after creation; future weekly runs must not rewrite the pre-result comparison with revised prices. All prior inputs, scripts and generated pages are archived under `audit/2026-10-28/refit/before`. Review calculations: `build_refit.py`. Verification: `py -m unittest test_monitor test_extensions test_pricing test_earnings_refit` (50 checks). Independent skeptical review reproduced all eight refits and source anchors; arithmetic passes, predictive validation remains PARTIAL.

Monitor local de DRAM e NAND de Samsung e SK hynix. Começou em 14/09/2026; primeira atualização em 15/09/2026. A base aduaneira cobre janeiro/2020 a agosto/2026, com 240 observações (80 meses x 3 categorias). A base de divulgações corporativas contém 98 observações de produto/trimestre: Samsung, 26 trimestres; Hynix, 23 trimestres, com lacunas identificadas (2022Q3, 2022Q4, 2023Q1).

## Arquivos principais

- `report.html`: relatório de leitura, com gráficos, resultado do teste e fontes.
- `data/exports.json`: valores oficiais normalizados, pesos, unidades, fonte, data de coleta e hash do arquivo original.
- `data/company_asp.json`: ASP divulgado, linguagem original resumida, faixa numérica de interpretação, escopo e exclusões.
- `data/analysis.json`: contas mensais/trimestrais, coeficientes, previsões retrospectivas e critérios de uso.
- `data/benchmarks.json`: preços de referência citados no comunicado governamental, separados do valor unitário aduaneiro.
- `data/exports_extended.json`: todos os códigos de 10 dígitos sob HS 8542.32 e HS 8523.51 (inclui SSD, 8523.51.1000), com cobertura por código.
- `data/exports_by_country.json`: exportações por país de destino para DRAM, flash, multichip e SSD (diagnóstico de composição).
- `data/bok_export_price_index.json`: índices de preço de exportação do Banco da Coreia (ECOS), base dólar, 2020=100.
- `data/analysis_ext.json`: proxies alternativos, sensibilidade por janela de treino, estatísticas adicionais de erro, registro proxy×ASP, composição por destino e ledger do Street (`data/street_calls.json`).
- `raw/`: respostas originais do portal, do ECOS e documentos corporativos.
- `data/vintages/` e `data/run_log.jsonl`: snapshots e revisões. O primeiro snapshot foi coletado em setembro/2026, portanto não há vintages históricos anteriores.

## O que estamos medindo

O dado público não identifica Samsung ou Hynix por exportador. A relação estimada é entre a exportação agregada da Coreia e a variação do ASP global de cada empresa. Não se trata de uma série observada do preço de exportação individual das empresas.

| Série aduaneira | HS de 10 dígitos | Uso |
|---|---|---|
| DRAM | 8542321010 | Indicador de valor por peso para confrontar com ASP de DRAM |
| Flash memory | 8542321030 | Aproximação para NAND; não equivale a NAND puro |
| Multichip integrated circuits | 8542323000 | Indicador complementar de composição; não é HBM puro |

Não foi identificada uma série pública de preço/volume que isole HBM nos códigos consultados. MCP não será rebatizado como HBM. Nenhum valor por quilo será convertido em preço por bit sem dados de densidade e composição. ASP divulgado pela empresa também pode incorporar mix; não é necessariamente preço do mesmo produto ao longo do tempo.

## Cálculos

1. O portal público KCS informa exportações em **milhares de USD** e peso líquido em **kg**. Converter o valor monetário multiplicando por 1.000. O endpoint com chave em data.go.kr usa campos/unidades diferentes e não pode compartilhar essa conversão automaticamente.
2. Valor unitário mensal = valor FOB em USD / peso líquido em kg. MoM e YoY comparam esse quociente. Peso não é bit shipment.
3. Valor unitário trimestral = soma dos valores / soma dos pesos. Não usar a média simples dos três valores unitários mensais.
4. Para prever o trimestre com um ou dois meses conhecidos, repetir o último valor e peso mensal observados nos meses faltantes. Trata-se de uma hipótese mecânica explícita de estabilidade até o fim do trimestre.
5. Para cada empresa/produto, estimar `log(1 + ASP_QoQ/100) = alfa + beta * log(UV_trimestre / UV_trimestre_anterior)`. Quatro versões fixas: primeiro mês, primeiros dois meses, trimestre completo e crescimento do trimestre anterior. A versão usada no mês é escolhida pela disponibilidade dos dados, não pelo melhor resultado retrospectivo.
6. Teste cronológico com janela crescente: pelo menos dez trimestres elegíveis anteriores para cada previsão. Não usa dados de trimestres futuros no treinamento. Os dados aduaneiros históricos têm o vintage mais recente; este **não é um backtest com dados disponíveis em cada data histórica**.
7. Comparar erro absoluto médio em pontos percentuais com três critérios simples: ASP sem variação, repetição da variação do trimestre anterior e variação direta do indicador (1:1). Comparações usam os mesmos trimestres com ASP anterior conhecido. A tabela informa o número de previsões comparáveis.
8. Critérios iniciais de uso: pelo menos 18 pontos de treino e 6 previsões comparáveis; beta positivo; erro menor que os três critérios simples; acerto de direção de pelo menos 60%; indicador atual dentro da faixa histórica de treinamento. São critérios analíticos definidos para este piloto, não evidência de validação independente. Para Hynix, exigir também cobertura da contração de 2022Q3 a 2023Q1.

## Linguagem qualitativa e mudanças de escopo

Faixas são convenções do analista, não intervalos divulgados pela administração: low/mid/high single = 1–3/4–6/7–9%; low/mid/high teens = 11–13/14–16/17–19%; low/mid/high 20s = 20–23/24–26/27–29%. Para outras dezenas, usar o mesmo padrão documentado em cada linha. Around/about X recebe X +/- 1 pp; nearly 20 recebe 18–20%; just over 10 recebe 10–13%. Essas escolhas são aproximações. O modelo usa o ponto médio e guarda os limites para sensibilidade, que **não é intervalo de confiança da previsão**.

- Samsung 2023Q4 DRAM: expressão aberta sobre double digits; excluída do ajuste.
- Samsung 2025Q2 DRAM: divulgação específica de DRAM convencional; excluída do ASP misto.
- Hynix 2022Q1 NAND: entrada da Solidigm altera a base de comparação; excluída.
- Hynix 2023Q3 NAND, 2023Q4 NAND e 2024Q1 DRAM/NAND: expressões apenas direcionais ou com limite aberto; sem ponto médio inventado.
- Hynix 2025Q4 DRAM: a transcrição pública trazia 20%; em 15/09/2026 a linha passou a *mid-20%* (+24–26%) com base em apresentação da empresa espelhada por terceiro, e foi incluída.
- Hynix: em 16/10/2026, apresentações oficiais preencheram DRAM 2022Q3 e DRAM/NAND 2023Q1. NAND 2022Q3 tem queda superior a 20% e fica excluído por limite aberto; 2022Q4 continua sem ASP quantitativo verificado para ambos os produtos. A cobertura da contração continua incompleta e bloqueia a promoção dos modelos. Não interpolar. 2025Q2 foi preenchido em 15/09/2026 a partir de transcrição de terceiro.

## Como interpretar

Uma alta de USD/kg pode vir de preço, maior densidade, embalagem, aplicações, clientes e mix de produtos. A diferença entre operações globais das empresas e exportações da Coreia também importa: produção fora da Coreia, vendas domésticas, transferências entre subsidiárias e timing de embarques/receitas. Um indicador pode acompanhar o ciclo e ainda ser ruim para prever a magnitude do ASP.

Os benchmarks de DDR5/NAND citados pelo governo ficam em uma camada distinta. Servem para confronto direcional do preço de um produto padronizado; não entram nesta regressão curta e não representam índice oficial ajustado por qualidade. Os índices de preço de exportação do BOK/ECOS por item (DRAM, flash memory, computer storage) passaram a ser coletados em 15/09/2026 (`refresh_bok.py`) e entram como indicadores alternativos, não na regressão primária.

## Atualização mensal

No PowerShell:

```powershell
py 'E:\korea-memory-monitor\update.py'
```

A atualização busca o último mês esperado após o dia 15 e revisita os últimos 24 meses. Depois da coleta principal, `update.py` roda os coletores complementares (`refresh_extended.py`, `refresh_country.py`, `refresh_bok.py`); uma falha de coleta preserva o arquivo anterior e o status fica em `data/last_update.json` (`supplementary`). Em seguida `analyze.py`, `analyze_ext.py` e `build_report.py`. Guarda as respostas, verifica completude, duplicatas, códigos e unidades e preserva a base anterior se a coleta falhar. Para recomputar o relatório sem rede:

```powershell
py 'E:\korea-memory-monitor\update.py' --offline
```

A rotina agendada nesta tarefa executará mensalmente no dia 16, às 09h de São Paulo, após a janela usual de publicação. Se o dado ainda não estiver disponível, registrar atraso, manter o mês efetivamente observado e não apresentar o relatório como atualizado. Rodar novamente quando houver publicação; nunca preencher dados ausentes com zeros.

A cada resultado trimestral, conferir o script/apresentação oficial, adicionar as linhas ao `data/company_asp.json` com fonte/data/escopo e recomputar. A cada publicação mensal, conferir se há novos benchmarks e atualizar `data/benchmarks.json`, sem misturar produtos de densidade diferente. `curate_samsung.py`, `curate_hynix.py` e `seed_benchmarks.py` são scripts de carga inicial; **não rodá-los na atualização recorrente**, pois recriam a base inicial.

## Séries complementares e extensões (15/09/2026)

Uma auditoria independente em 15/09/2026 reproduziu toda a aritmética do monitor (240 valores unitários mensais, 81 trimestrais, as 16 regressões, os backtests e o sinal corrente) e também corrigiu a faixa de normalização que ignorava pesos negativos na regressão. A auditoria de inferência mostrou que o sinal de +16% para o ASP DRAM da Samsung em 3Q26 varia de +6% a +22% conforme a janela de treino, e a vantagem sobre repetir o ASP anterior repousa em 11 trimestres (8 vitórias, p≈0,11). As extensões abaixo tratam disso **sem alterar os modelos primários** nem os critérios de uso.

- `refresh_extended.py` → `data/exports_extended.json`: consulta agrupada por HS6 que devolve todos os códigos de 10 dígitos sob 8542.32 e 8523.51. Nomes oficiais pelo próprio portal: 8542.32.3000 *multichip integrated circuits*; 8542.32.4000 *multi-component integrated circuits (MCOs)* (existe desde a revisão HSK de 2022; não entra em modelo); 8523.51.1000 *unrecorded solid-state non-volatile storage devices*, onde a Coreia classifica os SSDs (não em 8471.70). Em agosto/2026 os SSDs somaram US$ 5,98 bi contra US$ 2,86 bi dos chips flash — chips representam menos de um terço da soma dos valores dessas duas categorias. SSD inclui controlador e outros componentes: essa razão não mede a parcela de NAND puro, e não explica quantitativamente os saltos do valor unitário de Flash. Códigos menores podem ter meses sem comércio; nunca são preenchidos com zero.
- `refresh_country.py` → `data/exports_by_country.json`: modo item×país do portal (`tradeKind ETS_MNK_1020000E`, `cntyNm` vazio devolve todos os destinos). Uso: composição, por exemplo a participação de Taiwan (destino do empacotamento CoWoS) no multichip. Não é série de preço e não é HBM por construção.
- `refresh_bok.py` → `data/bok_export_price_index.json`: índices de preço de exportação do BOK/ECOS — tabela 402Y016 (por item: `DRAM`, `플래시메모리`, `시스템반도체`, `컴퓨터기억장치`) e 402Y014 (`집적회로`, `반도체`, `총지수`), base dólar (`ITEM_CODE2=D`), 2020=100. É pesquisa de preços com especificação controlada, não valor unitário aduaneiro. Sem chave própria a rotina usa a chave pública `sample`, limitada a 10 linhas por chamada e por isso paginada; para dispensar a paginação, registrar uma chave em ecos.bok.or.kr e gravá-la em `data/ecos_key.txt` ou na variável de ambiente `ECOS_API_KEY`. Os códigos de item ficam em `data/ecos_items_cache.json`.
- `analyze_ext.py` → `data/analysis_ext.json`: (1) índices Törnqvist encadeados — NAND = chips flash + SSD; DRAM = DRAM + multichip — com pesos pela participação no valor exportado, evitando somar quilos de bens distintos; (2) os mesmos ajustes, backtests e critérios rodados com cada indicador alternativo (US$/kg KCS, índices Törnqvist, SSD isolado, índices BOK), com auto-verificação de que os proxies primários reproduzem `analysis.json` exatamente; (3) sensibilidade do sinal corrente a quatro janelas de treino (completa; até 2023Q4; sem 2025Q4 em diante; desde 2024Q1; mínimo 8 pontos) — a faixa é incerteza estrutural, não intervalo de confiança; (4) mediana do erro, vitórias contra cada critério simples e teste do sinal unilateral (binomial); erro excluindo o superciclo (2025Q4 em diante); (5) proxy de trimestre completo contra o ASP divulgado nos últimos quatro trimestres; (6) leitura like-for-like (mesmos meses do trimestre anterior) ao lado do carry; (7) composição por destino; (8) ledger do Street.
- `data/street_calls.json`: ledger manual das chamadas atribuídas do Street para o trimestre corrente (produto, escopo, fonte, data, chamada, base, referência na wiki). Bases distintas — contrato, servidor, ASP misto, ex-LTA — são registradas e nunca combinadas em média. A referência canônica de preço DRAM é `dram-pricing-2026` em `_wiki/_meta/assumptions.md`. Atualizar a cada mês; trimestres resolvidos vão para um histórico.
- `weekly_tracker.py`, `build_tracker.py`, `collect_kcs_tentative.py`, `collect_motie_release.py`, `collect_japan_mof.py`, `curate_kioxia.py`: rotina semanal e novas fontes (ver seção própria).
- `test_extensions.py`: testes das extensões (Törnqvist, cauda binomial, janelas, like-for-like, estatísticas de holdout, reprodução dos modelos primários, ledger e relatório).

Regras: os proxies alternativos são diagnósticos e **não substituem o proxy primário por melhor backtest**. O índice chips+SSD foi acrescentado como candidato por cobertura econômica depois de examinar o histórico; a promoção a proxy primário exige mais trimestres de acompanhamento e será registrada aqui quando ocorrer. O relatório mostra o modelo primário e as alternativas lado a lado, sempre com a faixa por janela e o registro proxy×ASP dos últimos trimestres, e confronta o resultado com o ledger do Street.

Estado em 15/09/2026: Hynix passou a ter 2025Q2 e 2025Q4 na base (2025Q4 DRAM = *mid-20%*, de apresentação espelhada por terceiro), restando 2022Q3, 2022Q4 e 2023Q1; os comunicados do newsroom da SK hynix para esses trimestres não quantificam ASP (checado em 15/09/2026), de modo que a lacuna depende das transcrições das calls.

## Quebra preço × volume (15/09/2026)

Todo valor exportado apresentado no relatório e no tracker vem acompanhado da sua decomposição em volume e preço-mix: **Coreia**: valor = peso líquido (kg) × US$/kg, o peso sendo a única referência de volume da aduana coreana (a preliminar de 10 dias não traz peso); **Japão**: valor = unidades × ¥/unidade (o MOF não publica peso para 8542.32). Identidade multiplicativa (1 + Δvalor/100) = (1 + Δvolume/100) × (1 + Δpreço/100), com variações em %, verificada em `test_extensions.py`. Horizontes: mês (MoM e YoY), trimestre completo (QoQ e YoY) e trimestre até agora em base like-for-like (mesmos meses do trimestre e do ano anteriores, sem carry). Cálculo em `analyze_ext.py` (`pv_decomposition`), por código separadamente — nunca somar quilos de bens distintos. Peso e unidades não são bits: densidade, formato (wafer, componente, módulo) e mix movem o preço unitário.

## Rotina semanal — tracker (15/09/2026)

`weekly_tracker.py` transforma o monitor em rotina semanal (Task Scheduler **"Memory Exports Tracker (weekly)"**, segundas 08:20, via `E:\.claude\scripts
efresh_memory_exports.bat`; log em `refresh_memory_exports.log`). Cada fonte é coletada de forma independente e à prova de falha (o arquivo anterior permanece; o erro fica registrado em `data/tracker_state.json`); os modelos e o relatório só são reconstruídos quando seus insumos mudam. Saída: `tracker.html` (página semanal) e cópias em `_wiki/_dashboards/memory-exports-tracker.html` e `memory-exports-report.html` (sem git — a rotina das 18:15 da wiki leva os arquivos). A automação mensal (dia 16) do Codex para esta pasta torna-se redundante.

Fontes e cadência esperada:

| Fonte | Coletor | Saída | Publicação |
|---|---|---|---|
| KCS preliminar de 10 dias (menu 10일 단위 잠정치): exportações acumuladas 1–10, 1–20 e mês fechado para os 10 principais itens (반도체 = semicondutores; 컴퓨터 = computadores, onde saem os SSD) e 10 destinos | `collect_kcs_tentative.py` | `data/kcs_tentative.json` | dias 11 e 21; mês fechado ~dia 1 |
| KCS detalhe HS10 (DRAM, flash, multichip, SSD; códigos estendidos; destinos) | `refresh.py`, `refresh_extended.py`, `refresh_country.py` | `data/exports*.json` | ~dia 15 do mês seguinte |
| MOTIE release mensal (수출입동향 via korea.kr): total, semicondutores, computadores e a nota de preços fixos (DDR4 8Gb, DDR5 16Gb, NAND 128Gb) | `collect_motie_release.py` | `data/motie_releases.json`; meses novos entram em `data/benchmarks.json` | dia 1 |
| BOK ECOS índices de preço de exportação | `refresh_bok.py` | `data/bok_export_price_index.json` | ~dia 15 |
| Japão MOF, flash memory 8542.32-921 (e DRAM 8542.32-911) por país | `collect_japan_mof.py` | `data/japan_exports.json` | 確報 CSV no e-Stat ~fim do mês seguinte; 速報 via servlet ~dia 20 |
| Kioxia ASP divulgado (decks FY2018–FY2024Q2 + transcrições da wiki) | `curate_kioxia.py` (semente; não rodar na rotina) | `data/kioxia_asp.json` | trimestral |

Notas sobre o MOTIE: o corpo do release às vezes só existe no host `admin.korea.kr` ou no PDF anexo (`common/download.do?fileId=…`); o coletor tenta HTML e cai para o PDF. A nota de preços fixos muda de formato (cinco meses; dois pontos com YoY; trajetória trimestral) — quando não há meses explícitos, só o preço do mês do release é aproveitado.

## Japão — exportações de NAND (Kioxia / SanDisk)

Yokkaichi e Kitakami são as únicas fábricas de NAND do Japão, então a série de exportação de *flash memory* é uma leitura quase pura de Kioxia + SanDisk (a DRAM 8542.32-911 é a Micron Hiroshima). Códigos do 輸出統計品目表 2024: 8542.32 → RAM: 911 DRAM, 919 outras; ROM: **921 flash memory**, 929 outras. Fonte: MOF via e-Stat (普通貿易統計 › 品別国別表 › 輸出, arquivo mensal do grupo de capítulos 84-85類; um arquivo por ano com todos os meses; download `stat-search/file-download?statInfId=…&fileKind=1` sem login) e o servlet de busca do MOF (`/JCWSV01/servlet/JCWSV01`, formulário da tela 品別国別表 — atenção: as telas 23/25 usam `JCWSV09`) para o mês preliminar. Valor em milhares de ienes (armazenado em ienes), quantidade em unidades (`Unit2 = NO`). ¥/unidade mistura densidade e formato (wafer vs. componente); a comparação natural é com o ASP **base JPY** da Kioxia, que a empresa divulga como “ASP (JPY, QoQ)”. Destinos: China (montagem da SanDisk em Xangai), Taiwan (OSATs da Kioxia), Vietnã, Singapura, Filipinas.

Kioxia: `data/kioxia_asp.json` traz 26 trimestres (FY18 Q3 → FY24 Q2 dos decks oficiais em `raw/kioxia_decks`, base JPY, com a base USD quando informada; FY25 Q4 e FY26 Q1 das transcrições na wiki). Faltam FY24 Q3–FY25 Q3 (os decks recentes são servidos por um widget que o coletor ainda não lê). Regressão Japão × Kioxia ainda não montada: exige emparelhar trimestre fiscal (abr–mar) com meses civis e decidir a base (JPY).

## Próximas melhorias de pesquisa

Completar o ASP Hynix 2022Q4 e procurar faixa fechada para NAND 2022Q3; DRAM 2022Q3 e DRAM/NAND 2023Q1 foram verificados nas apresentações oficiais em 16/10/2026; acompanhar por mais trimestres a estabilidade do índice chips+SSD e do índice BOK como indicadores antes de qualquer troca de proxy primário; registrar chave ECOS própria; acumular vintages para avaliação prospectiva; medir estabilidade por regime e por mix de HBM/SSD. Não liberar um ASP de NAND pontual apenas porque a correlação do trimestre completo é positiva.

## Fontes

- [Korea Customs Service, portal público](https://tradedata.go.kr/cts/index.do)
- [KCS, documentação do serviço de estatísticas por produto](https://www.data.go.kr/data/15101609/openapi.do)
- [KCS, classificação HS de memórias](https://unipass.customs.go.kr/clip/hsinfosrch/openULS0201005Q.do?searchVal=854232)
- [Samsung IR, resultados trimestrais](https://www.samsung.com/global/ir/financial-information/earnings-release/), scripts oficiais preservados em `raw/samsung_scripts/`.
- Hynix: apresentações oficiais em `raw/hynix_decks/`; transcrições públicas de falas da administração e transcrição Bloomberg local para 2026Q2. Fonte individual em cada linha de `data/company_asp.json`.
- [Governo coreano, exportações de agosto/2026 e referências de preços](https://admin.korea.kr/briefing/pressReleaseView.do?newsId=156776348&pWise=mSub&pWiseSub=C4)

## Auditoria matemática concluída — 15/09/2026

[Relatório completo da auditoria](audit/2026-09-15/AUDIT.html), com contas abertas, valores antes/depois e fontes. Verificação independente: 16 modelos primários e 88 configurações nas extensões (incluem os 16 primários), 240 linhas KCS primárias, 1.027 estendidas, 10.860 por destino, 644 observações BOK e 2.270 linhas japonesas. Os 29 testes passaram. Samsung DRAM permanece +15,56% QoQ, mas a faixa por janela de treino é +6,44% a +21,75%; não é intervalo de confiança. O erro comparável histórico é 13,08 pp. O envelope de normalização foi corrigido para considerar pesos negativos da regressão. Hynix 2025Q2 foi preenchido e 2025Q4 DRAM reconciliado; as mudanças estão preservadas na trilha da auditoria.

A rotina semanal agora compara hashes de todos os insumos de modelo e do código contra o último build bem-sucedido, não apenas antes/depois da coleta atual. Isso captura mudanças isoladas em BOK, destinos, índices estendidos, ASP manual e código. A falha de impressão no console Windows também foi corrigida. Para repetir a auditoria independente, usar o Python do runtime com NumPy para audit_math.py --current e audit_extensions.py; a rotina mensal e os 29 testes usam a biblioteca padrão.

## Revisão de Flash — preço versus composição, 15/09/2026

A seção Flash agora compara USD/kg de chips, SSD e índice chips+SSD com BOK Flash, BOK storage e benchmark NAND 128Gb. flash_diagnostic.py decompõe exatamente a variação por destino; a parcela dentro do país continua contendo mix e não é preço puro. Agosto: +63,33% USD/kg; BOK Flash +8,38%; mix de destinos +13,26 pp; dentro dos destinos +50,06 pp. Nenhum coeficiente foi alterado. Todos os 33 testes passaram. [Revisão detalhada](audit/2026-09-15/flash-review/REVIEW.md).


## Preços InSpectrum / Bloomberg — 16/09/2026

Novo estudo em [pricing.html](pricing.html), integrado ao relatório e às rotinas mensal/semanal. Coletor refresh_market_prices.py usa exclusivamente a API local do Terminal autorizado, mantém respostas originais e snapshots; falhas preservam o arquivo anterior e são registradas na rotina. São 18 séries, contratos e spot; a série antiga ISTPDR72 tem cobertura interrompida em abril/2026 e não é carregada para frente.

Contratos são a última cotação mensal; spot é média de observações diárias. Cestas geométricas com componentes fixos e pesos iguais, sem conversão USD/bit ou pesos ajustados ao fit. Metadados GB/Gb de ISTPND27/28 são ambíguos; somente variações dentro da série são usadas. O protocolo de candidatos está em PRICING_PROTOCOL.md. Resultados e cálculos em data/pricing_analysis.json; preços e hashes de origem em data/market_prices.json.

Backtests cronológicos após dez trimestres de treino, com comparadores zero, persistência e variação direta, em trimestres comuns. Lag spot/contrato preserva o corte de informação no treino (mínimo 24 meses). Datas de índice não provam datas de divulgação: histórico revisado atual, não execução histórica em tempo real. Não há preço HBM identificado; faltam ASP Hynix 2022Q3–2023Q1.

Critérios de promoção dos modelos anteriores agora incluem superar a variação direta do indicador. Coeficientes anteriores não mudaram: o Samsung DRAM continua gerando +15,56% mecanicamente, mas deixa de passar os critérios porque o MAE de 13,08 pp supera o da regra direta (9,97 pp). O novo estudo InSpectrum permanece experimental, mesmo quando melhora o erro.

Atualização isolada: py refresh_market_prices.py, py analyze_pricing.py, py build_pricing_report.py. Atualização completa: py update.py. Rebuild sem rede: py update.py --offline. Verificações: py -m unittest test_monitor test_extensions test_pricing; py audit_pricing.py. O Terminal precisa estar disponível na sessão que executa a rotina.


## Atualização mensal verificada — 16/10/2026

KCS coletado até setembro/2026, com revisão de outubro/2024 a setembro/2026: 72 observações primárias reconsultadas, respostas originais e snapshots preservados. Setembro vs. agosto: DRAM valor +6,63%, peso +31,40%, USD/kg -18,85%; Flash valor +15,18%, peso +47,70%, USD/kg -22,01%. No 3T26 completo, USD/kg sobe 11,21% em DRAM e 45,44% em Flash. BOK setembro: DRAM +2,26% MoM e Flash -0,69% MoM. Os benchmarks governamentais DDR5 16Gb e NAND 128Gb estão em setembro (US$ 48,0 e US$ 30,6), confirmados no PDF oficial de 01/10, p. 1; preserva-se o arredondamento da série histórica. A p. 7 tem NAND com duas casas decimais, sem misturá-las à série arredondada. Esses preços já tinham sido acrescentados pela rotina semanal em 05/10; nesta rodada foi enriquecida a proveniência.

Revisões KCS: agosto MCP +US$ 751 mil (+0,0061%); SSD -1 kg, sem alteração de valor; dois códigos menores com pequenos ajustes. Nenhuma revisão de DRAM/Flash nos 24 meses reconsultados. BOK revisou o índice total de agosto de 153,64 para 154,00, sem revisão dos itens de memória. A decomposição de Flash atribui -12,79 pp da queda de setembro ao mix de destinos; a parcela dentro dos destinos ainda contém mix de produto e não equivale a preço puro.

Hynix: PDFs oficiais em `raw/hynix_decks/2022Q3.pdf`, `2022Q4.pdf` e `2023Q1.pdf`, com página 4 renderizada e conferida visualmente. DRAM 2022Q3: around 20% de queda, normalizado em -21% a -19%; DRAM 2023Q1: high teens de queda, -19% a -17%; NAND 2023Q1: around 10% de queda, -11% a -9%. As faixas são convenções do analista. NAND 2022Q3: queda superior a 20%, limite aberto, sem midpoint e fora do ajuste. A apresentação 2022Q4 e a transcrição pública revisada não forneceram ASP quantitativo verificável; a lacuna permanece. A divulgação mais recente com ASP na base segue 2T26 para ambas as empresas; nenhum ASP de 3T26 foi acrescentado. Samsung agenda a call de 3T26 para 29/10/2026.

Os quatro modelos primários seguem **exploratórios**, sem previsão operacional. Para 3T26 completo: Samsung DRAM +9,46% mecânico, MAE 12,58 pp (11 testes comuns); Hynix DRAM +8,54%, MAE 8,97 pp (11); Samsung NAND +24,66%, MAE 16,88 pp (15); Hynix NAND +24,02%, MAE 22,80 pp (8). Samsung DRAM não supera a regra direta, Samsung NAND não supera persistência e Hynix continua com cobertura incompleta da contração (NAND também falha em persistência). Modelos alternativos continuam diagnósticos.

Bloomberg local não iniciou sessão. A base InSpectrum anterior foi preservada: consulta bem-sucedida em 16/09/2026, último mês completo dos contratos em agosto/2026. Para atualizar, executar `refresh_market_prices.py` com Terminal aberto e autenticado e reconstruir o relatório. Falha e datas estão em `data/monthly_update_summary.json` e `audit/2026-10-16/monthly/online_status.json`, mesmo após o rebuild offline. O coletor MOTIE teve HTTP 404 em uma tentativa; a verificação foi concluída pelo PDF oficial da página pública, preservado na auditoria.

Verificação: 47 testes passam; auditoria independente dos 16 modelos primários, 88 configurações das extensões e 76 configurações de preços. A auditoria matemática agora usa o horizonte corrente (3 meses nesta rodada), e os arquivos de auditoria corrente usam pasta datada, preservando os resultados de setembro. A aritmética dos modelos primários coincide com o cálculo independente com diferença máxima de 4,3e-14. Trilha completa em [verificação mensal](audit/2026-10-16/monthly/monthly_update_summary.json). Relatório e estudo de preços foram reconstruídos offline após os insumos.


## Automatic Q4 watch — 28 October 2026

The previous monthly Codex heartbeat is now an active weekday watch at 09:00 and 16:00, America/Sao_Paulo, in the Memory Observatory chat. It runs `py monitor_memory.py`, reviews new BOK / spot / contract / trade evidence and relevant sell-side commentary, and republishes the existing internal dashboard. The Monday 08:20 Windows refresh remains a fallback. The initial October 28 assessment and earnings refit are preserved; the active review is versioned separately. October BOK and material direction/confidence changes are deduplicated. Full procedure: [MEMORY_WATCH_WORKFLOW.md](MEMORY_WATCH_WORKFLOW.md).

Local execution needs the workstation and Codex running; InSpectrum needs the authenticated Bloomberg Terminal. The page checks for published updates every five minutes while visible and retains chart selections when reloading. On source failure, previous data and its actual date remain visible.


### Source collector repair and audit — 28 October 2026

MOTIE now uses the public release page first, follows relative PDF links, and
tries the alternate host after a retrieval failure. It archives the official PDF
with its SHA-256, rechecks the newest release on every run, rejects empty search
or missing semiconductor totals, and records benchmark revisions for review
without overwriting existing price vintages. The September PDF omits the percent
glyph after the semiconductor YoY value; the parser accepts that observed format.

KCS headline, extended memory/SSD and destination data refresh independently;
all re-fetch the trailing 24 months even when the latest month is unchanged.
Incomplete BOK items, KCS preliminary categories/pagination, or destination
coverage now fail before replacing the old dataset. Japan distinguishes an
explicit unpublished-month response from a parser/download failure and keeps
previous preliminary rows if the supplementary lookup fails.

`data/source_health.json` provides eight numeric feed checks and three separately
labelled research ledgers. `data/tracker_last_online.json` preserves the online
check when an offline render runs. The dashboard Sources section shows both the
observation date and the check date. Company ASP and broker commentary require
the scheduled Codex research review; collector success does not imply a new
earnings transcript or report was read. Outlook connectivity was verified on
28 October; this repair did not mark a full new research sweep as completed.

Repair evidence and live run: `audit/2026-10-28/source-refresh-fix/`. Regression
checks: `py -m unittest test_source_refresh` (network-free failure fixtures).
