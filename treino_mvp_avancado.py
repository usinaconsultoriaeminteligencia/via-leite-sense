from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from gestor_store import carregar_base_treino_via_leite, init_db

try:
    from xgboost import XGBRegressor

    XGB_OK = True
except Exception:
    from sklearn.ensemble import HistGradientBoostingRegressor

    XGB_OK = False

SEED = 42
DATA_DIR = Path("dados_teste")
ARTEFATOS_DIR = Path("artefatos_teste")
HORIZONTE_DIAS = 7
TARGET = "target_media_coletada_7d"


def garantir_pasta(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def carregar_bases(data_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    init_db(data_dir)
    base_treino = carregar_base_treino_via_leite(data_dir)
    dim_produtor = pd.read_csv(data_dir / "dim_produtor.csv", parse_dates=["data_inicio_fornecimento"])
    dim_tempo = pd.read_csv(data_dir / "dim_tempo.csv", parse_dates=["data"])
    rota = pd.read_csv(data_dir / "dim_rota.csv")
    return base_treino, dim_produtor, dim_tempo, rota


def adicionar_features_temporais(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia_semana"] = df["data"].dt.weekday
    df["dia_do_ano"] = df["data"].dt.dayofyear
    df["semana_ano"] = df["data"].dt.isocalendar().week.astype(int)
    df["sin_dia_ano"] = np.sin(2 * np.pi * df["dia_do_ano"] / 365.25)
    df["cos_dia_ano"] = np.cos(2 * np.pi * df["dia_do_ano"] / 365.25)
    return df


def engenharia_de_atributos(base_treino: pd.DataFrame, dim_produtor: pd.DataFrame, rota: pd.DataFrame) -> pd.DataFrame:
    df = base_treino.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    if "nome_ficticio" not in df.columns:
        df = df.merge(dim_produtor, on="id_produtor", how="left", suffixes=("", "_cad"))

    rota_cols = ["id_rota", "dificuldade_logistica", "percentual_estrada_nao_pavimentada", "capacidade_tanque_litros"]
    if "dificuldade_logistica" not in df.columns:
        df = df.merge(rota[rota_cols], on="id_rota", how="left")

    df = adicionar_features_temporais(df)
    df = df.sort_values(["id_produtor", "data"]).reset_index(drop=True)
    group = df.groupby("id_produtor", sort=False)

    lags_base = [1, 2, 3, 7, 14, 21, 28]
    for lag in lags_base:
        df[f"lag_litros_coletados_{lag}"] = group["litros_coletados"].shift(lag)
        df[f"lag_litros_produzidos_{lag}"] = group["litros_produzidos"].shift(lag)
        df[f"lag_precip_15d_{lag}"] = group["precip_15d"].shift(lag)
        df[f"lag_thi_{lag}"] = group["thi"].shift(lag)

    for janela in [3, 7, 14, 30]:
        df[f"mm_{janela}_litros_coletados"] = (
            group["litros_coletados"].shift(1).rolling(janela, min_periods=1).mean().reset_index(level=0, drop=True)
        )
        df[f"std_{janela}_litros_coletados"] = (
            group["litros_coletados"].shift(1).rolling(janela, min_periods=2).std().reset_index(level=0, drop=True)
        )
        df[f"mm_{janela}_ccs"] = group["ccs"].shift(1).rolling(janela, min_periods=1).mean().reset_index(level=0, drop=True)
        df[f"mm_{janela}_cbt"] = group["cbt"].shift(1).rolling(janela, min_periods=1).mean().reset_index(level=0, drop=True)
        df[f"mm_{janela}_thi"] = group["thi"].shift(1).rolling(janela, min_periods=1).mean().reset_index(level=0, drop=True)
        df[f"mm_{janela}_precip"] = (
            group["precip_mm"].shift(1).rolling(janela, min_periods=1).mean().reset_index(level=0, drop=True)
        )

    df["tendencia_7_30_litros"] = df["mm_7_litros_coletados"] - df["mm_30_litros_coletados"]
    df["proporcao_coletado_produzido_lag1"] = df["lag_litros_coletados_1"] / df[
        "lag_litros_produzidos_1"
    ].replace(0, np.nan)
    df["intensidade_estresse_termico"] = np.maximum(df["thi"] - 72, 0)
    df["interacao_seca_calor"] = df["dias_sem_chuva"] * np.maximum(df["thi"] - 70, 0)
    df["chuva_x_estrada_ruim"] = df["precip_mm"] * df["percentual_estrada_nao_pavimentada"]
    df["distancia_x_custo"] = df["distancia_km_laticinio"] * df["custo_logistico_rateado"]

    df["impacto_gerencial_litros"] = pd.to_numeric(df.get("impacto_gerencial_litros", 0), errors="coerce").fillna(0)
    df["qtd_eventos_gerenciais"] = pd.to_numeric(df.get("qtd_eventos_gerenciais", 0), errors="coerce").fillna(0)
    df["score_qualidade_inicial"] = pd.to_numeric(df.get("score_qualidade_inicial", 0), errors="coerce").fillna(0)
    df["fornecedor_capacidade_tanque_litros"] = pd.to_numeric(
        df.get("fornecedor_capacidade_tanque_litros", 0), errors="coerce"
    ).fillna(0)
    df["fornecedor_historico_fornecimento_meses"] = pd.to_numeric(
        df.get("fornecedor_historico_fornecimento_meses", 0), errors="coerce"
    ).fillna(0)
    status_fornecedor = df.get("fornecedor_status_ativo", pd.Series(1, index=df.index))
    df["fornecedor_status_ativo"] = status_fornecedor.fillna(True).astype(int)
    df["litros_ajustados_gerencial"] = df["litros_coletados"] + df["impacto_gerencial_litros"]
    df["impacto_gerencial_pct"] = df["impacto_gerencial_litros"] / df["litros_coletados"].replace(0, np.nan)

    def media_futura(series: pd.Series, horizonte: int) -> pd.Series:
        arr = series.values
        out = np.full(len(arr), np.nan)
        for i in range(len(arr)):
            j = min(len(arr), i + 1 + horizonte)
            if i + 1 < len(arr):
                out[i] = np.mean(arr[i + 1 : j])
        return pd.Series(out, index=series.index)

    df[TARGET] = group["litros_coletados"].transform(lambda s: media_futura(s, HORIZONTE_DIAS))
    df = df[df[TARGET].notna()].copy()
    df = df[df["lag_litros_coletados_28"].notna()].copy()
    return df


def split_temporal(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = df[df["data"] < "2024-01-01"].copy()
    valid = df[(df["data"] >= "2024-01-01") & (df["data"] < "2025-01-01")].copy()
    test = df[df["data"] >= "2025-01-01"].copy()
    return train, valid, test


def selecionar_colunas(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    excluir = {
        "data",
        "nome_ficticio",
        "municipio",
        "data_inicio_fornecimento",
        "fornecedor_data_inicio_parceria",
        TARGET,
        "litros_coletados",
        "litros_produzidos",
        "litros_previstos",
        "target_queda_7d",
        "target_queda_15d",
        "target_queda_30d",
    }
    cat_cols = [c for c in df.columns if df[c].dtype == "object" and c not in excluir]
    num_cols = [
        c
        for c in df.columns
        if c not in excluir and c not in cat_cols and not pd.api.types.is_datetime64_any_dtype(df[c])
    ]
    return cat_cols, num_cols


def montar_pipeline(cat_cols: List[str], num_cols: List[str]) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num_cols),
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

    if XGB_OK:
        model = XGBRegressor(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            objective="reg:squarederror",
            random_state=SEED,
            n_jobs=4,
        )
    else:
        model = HistGradientBoostingRegressor(
            learning_rate=0.05,
            max_depth=10,
            max_iter=350,
            random_state=SEED,
        )

    return Pipeline(steps=[("prep", preprocessor), ("model", model)])


def metricas_regressao(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.clip(np.abs(y_true), 1e-6, None))) * 100)
    smape = float(np.mean(2 * np.abs(y_pred - y_true) / np.clip(np.abs(y_true) + np.abs(y_pred), 1e-6, None)) * 100)
    return {"rmse": rmse, "mae": mae, "r2": r2, "mape_pct": mape, "smape_pct": smape}


def gerar_baseline(df: pd.DataFrame) -> np.ndarray:
    baseline = df["mm_7_litros_coletados"].fillna(df["mm_30_litros_coletados"])
    return baseline.fillna(df["producao_media_esperada_litros_dia"]).values


def salvar_importancias(pipe: Pipeline, output_path: Path) -> None:
    try:
        prep = pipe.named_steps["prep"]
        model = pipe.named_steps["model"]
        feature_names = list(prep.get_feature_names_out())
        if hasattr(model, "feature_importances_"):
            imp = pd.DataFrame(
                {
                    "feature": feature_names,
                    "importance": model.feature_importances_,
                }
            ).sort_values("importance", ascending=False)
            imp.head(200).to_csv(output_path, index=False, encoding="utf-8-sig")
    except Exception:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Treina o MVP avançado de previsão de captação de leite.")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--artefatos-dir", type=Path, default=ARTEFATOS_DIR)
    args = parser.parse_args()

    data_dir = args.data_dir
    artefatos_dir = args.artefatos_dir
    garantir_pasta(artefatos_dir)

    base_treino, dim_produtor, _, rota = carregar_bases(data_dir)
    base_modelo = engenharia_de_atributos(base_treino, dim_produtor, rota)
    train, valid, test = split_temporal(base_modelo)
    cat_cols, num_cols = selecionar_colunas(base_modelo)

    features = cat_cols + num_cols
    X_train, y_train = train[features], train[TARGET]
    X_valid, y_valid = valid[features], valid[TARGET]
    X_test, y_test = test[features], test[TARGET]

    pipe = montar_pipeline(cat_cols, num_cols)
    pipe.fit(X_train, y_train)

    pred_valid = pipe.predict(X_valid)
    pred_test = pipe.predict(X_test)

    baseline_valid = gerar_baseline(valid)
    baseline_test = gerar_baseline(test)

    resultados = {
        "modelo": "XGBRegressor" if XGB_OK else "HistGradientBoostingRegressor",
        "target": TARGET,
        "horizonte_dias": HORIZONTE_DIAS,
        "treino_linhas": int(len(train)),
        "validacao_linhas": int(len(valid)),
        "teste_linhas": int(len(test)),
        "metricas_validacao_modelo": metricas_regressao(y_valid.values, pred_valid),
        "metricas_validacao_baseline": metricas_regressao(y_valid.values, baseline_valid),
        "metricas_teste_modelo": metricas_regressao(y_test.values, pred_test),
        "metricas_teste_baseline": metricas_regressao(y_test.values, baseline_test),
        "features_numericas": num_cols,
        "features_categoricas": cat_cols,
    }

    predicoes_test = test[["data", "id_produtor", "id_laticinio", "id_rota", "polo_climatico"]].copy()
    predicoes_test["y_real"] = y_test.values
    predicoes_test["y_pred_modelo"] = pred_test
    predicoes_test["y_pred_baseline"] = baseline_test
    predicoes_test["erro_abs_modelo"] = np.abs(predicoes_test["y_real"] - predicoes_test["y_pred_modelo"])
    predicoes_test["erro_abs_baseline"] = np.abs(predicoes_test["y_real"] - predicoes_test["y_pred_baseline"])

    resumo_laticinio = predicoes_test.groupby("id_laticinio", as_index=False).agg(
        y_real=("y_real", "mean"),
        y_pred_modelo=("y_pred_modelo", "mean"),
        erro_abs_modelo=("erro_abs_modelo", "mean"),
    )
    resumo_polo = predicoes_test.groupby("polo_climatico", as_index=False).agg(
        y_real=("y_real", "mean"),
        y_pred_modelo=("y_pred_modelo", "mean"),
        erro_abs_modelo=("erro_abs_modelo", "mean"),
    )

    predicoes_test.to_csv(artefatos_dir / "predicoes_teste.csv", index=False, encoding="utf-8-sig")
    resumo_laticinio.to_csv(artefatos_dir / "resumo_teste_por_laticinio.csv", index=False, encoding="utf-8-sig")
    resumo_polo.to_csv(artefatos_dir / "resumo_teste_por_polo.csv", index=False, encoding="utf-8-sig")
    base_modelo.head(20000).to_csv(artefatos_dir / "amostra_base_modelagem.csv", index=False, encoding="utf-8-sig")

    with open(artefatos_dir / "metricas_modelo.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    joblib.dump(pipe, artefatos_dir / "modelo_mvp.joblib")
    salvar_importancias(pipe, artefatos_dir / "feature_importances.csv")

    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    print("Artefatos salvos em:", artefatos_dir.resolve())


if __name__ == "__main__":
    main()
