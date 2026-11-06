# C2 e C4: resultado (2026-11-06T20:41:09)

Base: `dados_teste/` (54780 linhas, 30 produtores), mesma montagem do `/risk-radar`.

## C2: co-ocorrência das dimensões

| Dimensão | Disparo |
|---|---|
| risco_queda_producao | 23.6% |
| risco_qualidade | 55.3% |
| risco_ccs | 48.0% |
| risco_cbt | 30.6% |
| risco_temp_tanque | 29.0% |
| risco_perda_bonus | 20.2% |
| risco_descarte | 0.4% |

Pares mais correlacionados (phi): risco_qualidade × risco_ccs = 0.86; risco_qualidade × risco_cbt = 0.60; risco_ccs × risco_perda_bonus = 0.52; risco_qualidade × risco_perda_bonus = 0.45

Linhas com CCS ≥ 500 mil: 11070; nelas, as dimensões binárias somam em média **64.6** pontos. Linhas com 2+ dimensões de qualidade juntas: 55.3%.

## C4: sensibilidade aos pesos

Referência: Alto + Crítico em 41.8% das linhas.

| Cenário | Spearman do ranking | Top-10 mantido | Alto + Crítico |
|---|---|---|---|
| Cada peso ±20% (pior caso de 14) | 0.997 | 90% | 38.2% a 46.4% |
| Pesos iguais | 0.994 | 100% | 35.8% |
| 50 sorteios Dirichlet (mínimo / mediana) | 0.950 / 0.993 | 70% / 90% | 30.1% a 52.7% |
