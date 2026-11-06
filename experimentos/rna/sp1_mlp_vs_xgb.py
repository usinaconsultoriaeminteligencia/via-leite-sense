"""SP1 (RNA) — rede neural MLP x XGBoost x baseline, pelo protocolo de rna.md §5.

Matéria: Redes Neurais Artificiais. Etapa E1 da trilha (rna.md §6.1): MLP tabular.

Invariantes (pré-registrados em rna.md §5.1):
  1. alvo `target_media_coletada_7d` (7 dias);
  2. split temporal: treino < 2024, validação 2024, teste >= 2025;
  3. mesmas features do modelo de produção, sem identificadores (A2);
  4. baseline `gerar_baseline()` inalterado (MM7 com cascata);
  5. sementes 42..46, média e desvio-padrão;
  6. mesmo orçamento de sintonia por modelo, escolhido SÓ na validação;
  7. teste aberto uma única vez por modelo, com a configuração já escolhida.

Extra: ablação do achado A1 (as duas features que expõem o dia t).

Uso (da raiz do repositório):
    python -m experimentos.rna.sp1_mlp_vs_xgb --orcamento 30
Saída: experimentos/rna/resultados/sp1_resultados.json e .md

Fica fora do caminho de produção (critério de admissão, PROJETO_INTEGRADOR.md §4).
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

from via_leite.models.treino_mvp_avancado import (
    DATA_DIR,
    TARGET,
    carregar_bases,
    engenharia_de_atributos,
    gerar_baseline,
    metricas_regressao,
    selecionar_colunas,
    split_temporal,
)

SEMENTES = [42, 43, 44, 45, 46]
FEATURES_A1 = ["litros_ajustados_gerencial", "impacto_gerencial_pct"]
SAIDA = Path(__file__).parent / "resultados"


def preprocessador(cat_cols, num_cols, escalar: bool) -> ColumnTransformer:
    num_steps = [("imputer", SimpleImputer(strategy="median"))]
    if escalar:  # a rede precisa de escala; a árvore não
        num_steps.append(("scaler", StandardScaler()))
    return ColumnTransformer(
        [
            ("num", Pipeline(num_steps), num_cols),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                cat_cols,
            ),
        ]
    )


def sortear_xgb(rng: np.random.Generator) -> dict:
    return {
        "n_estimators": int(rng.choice([200, 300, 500, 800])),
        "max_depth": int(rng.choice([4, 6, 8, 10])),
        "learning_rate": float(rng.choice([0.02, 0.05, 0.1])),
        "subsample": float(rng.choice([0.7, 0.85, 1.0])),
        "colsample_bytree": float(rng.choice([0.6, 0.85, 1.0])),
        "min_child_weight": int(rng.choice([1, 5, 10])),
    }


def sortear_mlp(rng: np.random.Generator) -> dict:
    camadas = [(64,), (128,), (128, 64), (256, 128), (256, 128, 64)]
    return {
        "hidden_layer_sizes": camadas[int(rng.integers(len(camadas)))],
        "alpha": float(rng.choice([1e-5, 1e-4, 1e-3, 1e-2])),
        "learning_rate_init": float(rng.choice([1e-4, 3e-4, 1e-3, 3e-3])),
        "batch_size": int(rng.choice([128, 256, 512])),
    }


def montar(tipo: str, params: dict, semente: int, cat_cols, num_cols) -> Pipeline:
    if tipo == "xgb":
        modelo = XGBRegressor(objective="reg:squarederror", random_state=semente, n_jobs=4, **params)
        return Pipeline([("prep", preprocessador(cat_cols, num_cols, escalar=False)), ("model", modelo)])
    mlp = MLPRegressor(
        activation="relu",
        solver="adam",
        max_iter=200,
        early_stopping=True,  # usa 10% do TREINO, nunca a validação de 2024
        n_iter_no_change=10,
        random_state=semente,
        **params,
    )
    modelo = TransformedTargetRegressor(regressor=mlp, transformer=StandardScaler())
    return Pipeline([("prep", preprocessador(cat_cols, num_cols, escalar=True)), ("model", modelo)])


def sintonizar(tipo, orcamento, dados, cat_cols, num_cols, log) -> tuple[dict, list]:
    """Busca aleatória com o MESMO orçamento por modelo, avaliada só na validação."""
    X_tr, y_tr, X_va, y_va = dados
    rng = np.random.default_rng(42)
    sortear = sortear_xgb if tipo == "xgb" else sortear_mlp
    historico = []
    for i in range(orcamento):
        params = sortear(rng)
        t0 = time.time()
        pipe = montar(tipo, params, 42, cat_cols, num_cols).fit(X_tr, y_tr)
        mae = metricas_regressao(y_va.values, pipe.predict(X_va))["mae"]
        historico.append({"params": params, "mae_validacao": mae, "segundos": round(time.time() - t0, 1)})
        log(f"  [{tipo}] config {i + 1}/{orcamento}: MAE val {mae:.3f} ({historico[-1]['segundos']}s)")
    melhor = min(historico, key=lambda h: h["mae_validacao"])
    return melhor["params"], historico


def avaliar_sementes(tipo, params, dados_finais, cat_cols, num_cols, log) -> dict:
    """Treina com cada semente e abre o teste uma vez por semente, com a config já escolhida."""
    X_tr, y_tr, X_te, y_te = dados_finais
    maes, rmses, tempos_inferencia = [], [], []
    for s in SEMENTES:
        pipe = montar(tipo, params, s, cat_cols, num_cols).fit(X_tr, y_tr)
        t0 = time.time()
        pred = pipe.predict(X_te)
        tempos_inferencia.append((time.time() - t0) / len(X_te) * 1000)
        m = metricas_regressao(y_te.values, pred)
        maes.append(m["mae"])
        rmses.append(m["rmse"])
        log(f"  [{tipo}] semente {s}: MAE teste {m['mae']:.3f}")
    return {
        "mae_media": float(np.mean(maes)),
        "mae_dp": float(np.std(maes, ddof=1)),
        "rmse_media": float(np.mean(rmses)),
        "mae_por_semente": maes,
        "inferencia_ms_por_linha": float(np.mean(tempos_inferencia)),
    }


def decidir(xgb: dict, mlp: dict) -> str:
    """Critério pré-registrado em rna.md §6.2 (intervalos de ±1 DP)."""
    lo_x, hi_x = xgb["mae_media"] - xgb["mae_dp"], xgb["mae_media"] + xgb["mae_dp"]
    lo_m, hi_m = mlp["mae_media"] - mlp["mae_dp"], mlp["mae_media"] + mlp["mae_dp"]
    if hi_m < lo_x:
        return "MLP vence com intervalos não sobrepostos: candidata a entrar no produto (conferir custo de inferência)"
    if hi_x < lo_m:
        return "Resultado negativo: XGBoost vence com intervalos não sobrepostos (achado para o artigo, rna.md §6.2)"
    return "Empate estatístico (intervalos sobrepostos): MLP fica como experimento"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--orcamento", type=int, default=30, help="configurações por modelo (protocolo: 30)")
    ap.add_argument("--data-dir", type=Path, default=DATA_DIR)
    args = ap.parse_args()
    SAIDA.mkdir(parents=True, exist_ok=True)
    linhas_log: list[str] = []

    def log(msg: str) -> None:
        print(msg, flush=True)
        linhas_log.append(msg)

    base_treino, dim_produtor, _, rota = carregar_bases(args.data_dir)
    df = engenharia_de_atributos(base_treino, dim_produtor, rota)
    train, valid, test = split_temporal(df)
    cat_cols, num_cols = selecionar_colunas(df)
    feats = cat_cols + num_cols
    log(f"Linhas: treino {len(train)} | validação {len(valid)} | teste {len(test)} | features {len(feats)}")

    dados_sintonia = (train[feats], train[TARGET], valid[feats], valid[TARGET])
    # Depois da escolha, treina em treino+validação (prática padrão) e testa em 2025.
    trval = pd.concat([train, valid])
    dados_finais = (trval[feats], trval[TARGET], test[feats], test[TARGET])

    resultados: dict = {
        "data_execucao": datetime.now().isoformat(timespec="seconds"),
        "orcamento_por_modelo": args.orcamento,
        "sementes": SEMENTES,
        "linhas": {"treino": len(train), "validacao": len(valid), "teste": len(test)},
        "n_features": len(feats),
    }

    base = metricas_regressao(test[TARGET].values, gerar_baseline(test))
    resultados["baseline_teste"] = base
    log(f"Baseline MM7 com cascata — MAE teste {base['mae']:.3f}")

    for tipo in ["xgb", "mlp"]:
        log(f"Sintonia {tipo} ({args.orcamento} configurações, validação 2024)")
        params, hist = sintonizar(tipo, args.orcamento, dados_sintonia, cat_cols, num_cols, log)
        log(f"Melhor {tipo}: {params}")
        aval = avaliar_sementes(tipo, params, dados_finais, cat_cols, num_cols, log)
        aval["ganho_sobre_baseline_pct"] = (1 - aval["mae_media"] / base["mae"]) * 100
        resultados[tipo] = {"melhor_config": params, "sintonia": hist, "teste": aval}

    resultados["decisao_admissao"] = decidir(resultados["xgb"]["teste"], resultados["mlp"]["teste"])

    # Ablação A1: o XGBoost escolhido, sem as duas features que expõem o dia t.
    sem_a1 = [c for c in num_cols if c not in FEATURES_A1]
    log("Ablação A1 (XGBoost sem litros_ajustados_gerencial e impacto_gerencial_pct)")
    dados_a1 = (trval[cat_cols + sem_a1], trval[TARGET], test[cat_cols + sem_a1], test[TARGET])
    aval_a1 = avaliar_sementes("xgb", resultados["xgb"]["melhor_config"], dados_a1, cat_cols, sem_a1, log)
    resultados["ablacao_A1_xgb"] = aval_a1

    (SAIDA / "sp1_resultados.json").write_text(json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8")
    (SAIDA / "sp1_log.txt").write_text("\n".join(linhas_log), encoding="utf-8")

    x, m = resultados["xgb"]["teste"], resultados["mlp"]["teste"]
    md = f"""# SP1 — resultado ({resultados['data_execucao']})

Protocolo: `docs/projeto_integrador/rna.md` §5 · orçamento {args.orcamento} configurações por modelo ·
sementes {SEMENTES} · treino+validação para o ajuste final · teste (2025) aberto uma vez por semente.

| Modelo | MAE teste (média ± DP) | Ganho sobre baseline | RMSE médio | Inferência (ms/linha) |
|---|---|---|---|---|
| Baseline MM7 com cascata | {base['mae']:.2f} | — | {base['rmse']:.2f} | — |
| XGBoost (sintonizado) | {x['mae_media']:.2f} ± {x['mae_dp']:.2f} | {x['ganho_sobre_baseline_pct']:.1f} % | {x['rmse_media']:.2f} | {x['inferencia_ms_por_linha']:.4f} |
| MLP (sintonizada) | {m['mae_media']:.2f} ± {m['mae_dp']:.2f} | {m['ganho_sobre_baseline_pct']:.1f} % | {m['rmse_media']:.2f} | {m['inferencia_ms_por_linha']:.4f} |
| XGBoost sem as features do A1 | {aval_a1['mae_media']:.2f} ± {aval_a1['mae_dp']:.2f} | {(1 - aval_a1['mae_media'] / base['mae']) * 100:.1f} % | {aval_a1['rmse_media']:.2f} | — |

**Decisão (critério de rna.md §6.2):** {resultados['decisao_admissao']}

Melhor XGBoost: `{resultados['xgb']['melhor_config']}`
Melhor MLP: `{resultados['mlp']['melhor_config']}`

Base sintética (`dados_teste/`, 30 produtores). Não é resultado em dado real.
"""
    (SAIDA / "sp1_resultados.md").write_text(md, encoding="utf-8")
    log(md)


if __name__ == "__main__":
    main()
