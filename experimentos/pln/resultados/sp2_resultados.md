# SP2 — resultado (2026-11-06T20:37:43)

Treino: 900 mensagens sintéticas (família A). **Nenhum conjunto abaixo é real**; o número que vale no artigo vem de `--teste-real`.

| Conjunto | Modelo | F1 macro intenção | F1 entidades (exato) | F1 VOLUME | Lançamento correto | Erro no volume | Volume errado sem aviso |
|---|---|---|---|---|---|---|---|
| sintetico_A (mesma distribuição) | E0 regras | 0.835 | 0.994 | 1.000 | 79.3% | 0.0% | 0 |
| sintetico_A (mesma distribuição) | E1 TF-IDF + LR | 0.998 | 0.994 | 1.000 | 99.7% | 0.0% | 0 |
| sintetico_B (fora da distribuição) | E0 regras | 0.963 | 0.937 | 0.966 | 92.3% | 0.0% | 0 |
| sintetico_B (fora da distribuição) | E1 TF-IDF + LR | 0.630 | 0.937 | 0.966 | 66.3% | 0.0% | 0 |

## Recusa (E1): cobertura × lançamento correto

| Conjunto | limiar 0.0 | limiar 0.4 | limiar 0.5 | limiar 0.6 | limiar 0.7 | limiar 0.8 | limiar 0.9 |
|---|---|---|---|---|---|---|---|
| sintetico_A (mesma distribuição) | 100% / 100% | 100% / 100% | 100% / 100% | 100% / 100% | 99% / 100% | 99% / 100% | 94% / 100% |
| sintetico_B (fora da distribuição) | 100% / 66% | 73% / 80% | 62% / 82% | 50% / 85% | 34% / 97% | 19% / 100% | 8% / 100% |

Célula = cobertura / lançamento correto entre as mensagens aceitas.
