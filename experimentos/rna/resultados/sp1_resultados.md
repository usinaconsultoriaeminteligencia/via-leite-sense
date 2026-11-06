# SP1 — resultado (2026-11-06T20:34:23)

Protocolo: `docs/projeto_integrador/rna.md` §5 · orçamento 30 configurações por modelo ·
sementes [42, 43, 44, 45, 46] · treino+validação para o ajuste final · teste (2025) aberto uma vez por semente.

| Modelo | MAE teste (média ± DP) | Ganho sobre baseline | RMSE médio | Inferência (ms/linha) |
|---|---|---|---|---|
| Baseline MM7 com cascata | 31.54 | — | 48.57 | — |
| XGBoost (sintonizado) | 23.28 ± 0.03 | 26.2 % | 35.06 | 0.0128 |
| MLP (sintonizada) | 25.99 ± 0.65 | 17.6 % | 37.79 | 0.0067 |
| XGBoost sem as features do A1 | 24.41 ± 0.05 | 22.6 % | 36.64 | — |

**Decisão (critério de rna.md §6.2):** Resultado negativo: XGBoost vence com intervalos não sobrepostos (achado para o artigo, rna.md §6.2)

Melhor XGBoost: `{'n_estimators': 500, 'max_depth': 8, 'learning_rate': 0.02, 'subsample': 0.7, 'colsample_bytree': 0.6, 'min_child_weight': 1}`
Melhor MLP: `{'hidden_layer_sizes': (256, 128), 'alpha': 0.01, 'learning_rate_init': 0.003, 'batch_size': 256}`

Base sintética (`dados_teste/`, 30 produtores). Não é resultado em dado real.
