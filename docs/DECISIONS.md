# VIA LEITE SENSE — decisões técnicas

Registro corrido das decisões que mudam código, dados ou métricas. Uma entrada por
decisão, com a evidência que a sustenta. O `SESSION_LOG.md` conta a sessão; aqui fica
só o que precisa de ser lembrado depois. Decisões do Plano de Trabalho FAPEG ficam em
`docs/plano_de_trabalho/DECISIONS.md`.

## 11/10/2026 — Janelas móveis do modelo passam a respeitar a fronteira entre produtores

**Achado.** Em `via_leite/models/treino_mvp_avancado.py`, as features `mm_*` e `std_*`
(médias e desvios móveis de 3, 7, 14 e 30 dias de litros, CCS, CBT, THI e chuva) eram
calculadas como `group[col].shift(1).rolling(janela).mean()`. O `shift(1)` de um
`SeriesGroupBy` devolve uma Series simples, sem agrupamento; o `rolling` seguinte corria
sobre o DataFrame inteiro. Como a base está ordenada por produtor e data, os primeiros
dias de cada produtor recebiam a média dos últimos dias do produtor anterior.

**Prova.** `tests/test_janelas_moveis_por_produtor.py`: dois produtores consecutivos com
100 L/dia e 1.000 L/dia. No código antigo, `mm_3_litros_coletados` do primeiro registro
do produtor 2 valia 100 (devia ser NaN) e do segundo valia 550. Pela função completa,
`mm_30` do primeiro registro que sobrevive ao filtro `lag_28` valia 968,97 em vez de
1.000.

**Decisão.** Extrair o bloco para `adicionar_janelas_moveis` e calcular com
`group[col].transform(lambda s: s.shift(1).rolling(janela, min_periods=...).agg)`. O
`shift(1)` fica dentro do `transform`: a janela continua a excluir o próprio dia (seria
vazamento do alvo) e passa a nunca sair do produtor. A ordem das colunas foi mantida
porque o `colsample_bytree` do XGBoost depende dela.

**O que não mudou.** O alvo `target_media_coletada_7d` já usava `transform` por grupo e
não atravessa produtores (teste `test_alvo_media_futura_nao_atravessa_produtores`). O
`split_temporal` é por data e continua a dar 32.010 / 10.980 / 10.920 linhas
(`test_split_temporal_continua_por_data`).

**Impacto nos dados.** Na base sintética (30 produtores, 53.910 linhas de modelagem), o
filtro `lag_28` já descartava os 28 primeiros dias de cada produtor, por isso só a
janela de 30 ainda vazava: 29 linhas alteradas (o primeiro dia útil de cada produtor
menos o primeiro), nas colunas `mm_30_*`, `std_30_litros_coletados` e
`tendencia_7_30_litros`. Todas no conjunto de treino; o baseline de validação e teste
é idêntico antes e depois.

**Métricas (XGBRegressor, `dados_teste`).** O artefato commitado em 06/08/2026 não é
reproduzido pelo código antigo nesta máquina (xgboost 3.2, `n_jobs=4`), por isso a
coluna do meio é o código antigo reexecutado hoje, no mesmo ambiente:

| Métrica | Commit 06/08 | Antigo (hoje) | Corrigido |
|---|---:|---:|---:|
| Validação · MAE modelo | 23,13 | 23,12 | 23,11 |
| Validação · RMSE modelo | 35,08 | 34,95 | 34,97 |
| Teste · MAE modelo | 24,17 | 24,22 | 24,32 |
| Teste · RMSE modelo | 36,68 | 36,57 | 36,74 |
| Teste · MAPE modelo | 3,58% | 3,59% | 3,61% |
| Teste · MAE baseline | 31,54 | 31,54 | 31,54 |

O treino é determinístico no mesmo ambiente (duas execuções do código antigo deram
métricas idênticas), logo os 0,1 L a mais no MAE de teste são efeito real das 29 linhas
corrigidas (0,09% do treino) sobre a estrutura das árvores, não ruído. É menor do que
a diferença entre o commit de agosto e o mesmo código hoje (0,05 L) e não muda a
leitura do `ESTADO_REAL.md`: MAE do modelo 24,3 contra 31,5 do baseline (cerca de 23%
menor). A correção vale pelo contrato, não
pela métrica: com dados reais, em que os produtores entram em datas diferentes e as
séries são curtas, a janela de 30 dias contaminada seria exatamente a do produtor
recém-chegado.

**Fora do escopo.** `media_30d_passada` em `gerador_leite_sintetico.py` já usa
`transform` por produtor. Os `rolling` de `ingestao_clima_inmet.py` correm por
estação dentro de um laço e não têm o problema. O DomainSim não foi tocado.
