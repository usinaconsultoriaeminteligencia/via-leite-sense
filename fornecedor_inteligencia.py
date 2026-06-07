from __future__ import annotations

import numpy as np
import pandas as pd


def _serie_segura(df: pd.DataFrame, coluna: str, default: float = 0.0) -> pd.Series:
    if coluna in df.columns:
        return pd.to_numeric(df[coluna], errors="coerce").fillna(default)
    return pd.Series(default, index=df.index)


def _normalizar_0_1(s: pd.Series, inverso: bool = False) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    p10 = s.quantile(0.10)
    p90 = s.quantile(0.90)
    if pd.isna(p10) or pd.isna(p90) or p90 <= p10:
        out = pd.Series(0.0, index=s.index)
    else:
        out = ((s - p10) / (p90 - p10)).clip(0, 1)
    return 1 - out if inverso else out


def classificar_risco(score: float) -> str:
    if score >= 75:
        return "Alto"
    if score >= 50:
        return "Medio"
    return "Baixo"


def gerar_recomendacao(row: pd.Series) -> str:
    motivos: list[str] = []
    if row.get("risco_queda_pct", 0) >= 25 or row.get("tendencia_volume_pct", 0) <= -8:
        motivos.append("priorizar contato de campo para proteger volume")
    if row.get("ccs_media", 0) >= 500 or row.get("cbt_media", 0) >= 180 or row.get("taxa_reprovacao_pct", 0) >= 1:
        motivos.append("abrir plano de qualidade e verificar manejo, ordenha e tanque")
    if row.get("taxa_descarte_pct", 0) >= 3:
        motivos.append("investigar descarte e perdas antes da coleta")
    if row.get("taxa_falha_pct", 0) >= 2:
        motivos.append("revisar rota, janela de coleta e acesso em dias de chuva")
    if row.get("risco_churn_pct", 0) >= 1:
        motivos.append("acionar retenção comercial")
    if not motivos:
        return "Manter acompanhamento regular e reforçar boas práticas."
    return "; ".join(motivos).capitalize() + "."


def calcular_scores_fornecedores(
    prod: pd.DataFrame,
    dim_prod: pd.DataFrame,
    pred: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if prod.empty:
        return pd.DataFrame()

    work = prod.copy()
    work["data"] = pd.to_datetime(work["data"], errors="coerce")
    work["litros_coletados"] = _serie_segura(work, "litros_coletados")
    work["litros_previstos"] = _serie_segura(work, "litros_previstos")
    work["litros_descartados"] = _serie_segura(work, "litros_descartados")
    work["ccs"] = _serie_segura(work, "ccs")
    work["cbt"] = _serie_segura(work, "cbt")
    work["flag_qualidade_reprovada"] = _serie_segura(work, "flag_qualidade_reprovada")
    work["flag_falha_coleta"] = _serie_segura(work, "flag_falha_coleta")
    work["flag_antibiotico"] = _serie_segura(work, "flag_antibiotico")
    work["flag_mudou_laticinio"] = _serie_segura(work, "flag_mudou_laticinio")
    if "target_queda_7d" not in work.columns:
        work["target_queda_7d"] = 0

    agg = work.groupby("id_produtor", as_index=False).agg(
        id_laticinio=("id_laticinio", "last"),
        id_rota=("id_rota", "last"),
        polo_climatico=("polo_climatico", "last"),
        dias_observados=("data", "nunique"),
        data_ultima=("data", "max"),
        litros_coletados_total=("litros_coletados", "sum"),
        litros_coletados_media=("litros_coletados", "mean"),
        litros_previstos_total=("litros_previstos", "sum"),
        litros_descartados_total=("litros_descartados", "sum"),
        ccs_media=("ccs", "mean"),
        cbt_media=("cbt", "mean"),
        reprovacoes=("flag_qualidade_reprovada", "sum"),
        falhas_coleta=("flag_falha_coleta", "sum"),
        antibiotico=("flag_antibiotico", "sum"),
        churn_eventos=("flag_mudou_laticinio", "sum"),
        risco_queda_pct=("target_queda_7d", "mean"),
        score_sanidade=("score_sanidade", "mean"),
        score_manejo=("score_manejo", "mean"),
        custo_logistico_medio=("custo_logistico_rateado", "mean"),
        margem_estimada_media=("margem_estimada_fornecedor", "mean"),
    )

    agg["risco_queda_pct"] = agg["risco_queda_pct"].fillna(0) * 100
    agg["taxa_descarte_pct"] = (
        agg["litros_descartados_total"] / agg["litros_previstos_total"].replace(0, np.nan) * 100
    ).fillna(0)
    agg["taxa_reprovacao_pct"] = (agg["reprovacoes"] / agg["dias_observados"].replace(0, np.nan) * 100).fillna(0)
    agg["taxa_falha_pct"] = (agg["falhas_coleta"] / agg["dias_observados"].replace(0, np.nan) * 100).fillna(0)
    agg["risco_antibiotico_pct"] = (agg["antibiotico"] / agg["dias_observados"].replace(0, np.nan) * 100).fillna(0)
    agg["risco_churn_pct"] = (agg["churn_eventos"] / agg["dias_observados"].replace(0, np.nan) * 100).fillna(0)

    trend = (
        work.sort_values(["id_produtor", "data"])
        .groupby("id_produtor")[["data", "litros_coletados"]]
        .apply(_calcular_tendencia_produtor)
        .rename("tendencia_volume_pct")
        .reset_index()
    )
    agg = agg.merge(trend, on="id_produtor", how="left")
    agg["tendencia_volume_pct"] = agg["tendencia_volume_pct"].fillna(0)

    dim_cols = [
        "id_produtor",
        "municipio",
        "tipo_sistema",
        "nivel_tecnificacao",
        "raca_predominante",
        "porte_produtor",
        "vacas_lactacao",
        "distancia_km_laticinio",
        "prob_churn_base",
    ]
    dim_cols = [c for c in dim_cols if c in dim_prod.columns]
    if dim_cols:
        agg = agg.merge(dim_prod[dim_cols], on="id_produtor", how="left")

    if pred is not None and not pred.empty and "id_produtor" in pred.columns:
        pred_agg = pred.groupby("id_produtor", as_index=False).agg(
            previsto_7d=("y_pred_modelo", "mean"),
            realizado_7d=("y_real", "mean"),
            erro_abs_predicao=("erro_abs_modelo", "mean"),
        )
        agg = agg.merge(pred_agg, on="id_produtor", how="left")
    else:
        agg["previsto_7d"] = np.nan
        agg["realizado_7d"] = np.nan
        agg["erro_abs_predicao"] = np.nan

    volume_risco = _normalizar_0_1(-agg["tendencia_volume_pct"]) * 0.55 + _normalizar_0_1(agg["risco_queda_pct"]) * 0.45
    qualidade_risco = (
        _normalizar_0_1(agg["ccs_media"]) * 0.30
        + _normalizar_0_1(agg["cbt_media"]) * 0.25
        + _normalizar_0_1(agg["taxa_reprovacao_pct"]) * 0.20
        + _normalizar_0_1(agg["risco_antibiotico_pct"]) * 0.25
    )
    logistica_risco = _normalizar_0_1(agg["taxa_falha_pct"]) * 0.45 + _normalizar_0_1(agg["custo_logistico_medio"]) * 0.35
    if "distancia_km_laticinio" in agg.columns:
        logistica_risco = logistica_risco + _normalizar_0_1(agg["distancia_km_laticinio"]) * 0.20
    continuidade_risco = _normalizar_0_1(agg["risco_churn_pct"]) * 0.55 + _normalizar_0_1(agg["margem_estimada_media"], inverso=True) * 0.45

    agg["score_volume"] = (volume_risco * 100).round(1)
    agg["score_qualidade"] = (qualidade_risco * 100).round(1)
    agg["score_logistica"] = (logistica_risco.clip(0, 1) * 100).round(1)
    agg["score_continuidade"] = (continuidade_risco * 100).round(1)
    agg["score_risco_fornecedor"] = (
        agg["score_volume"] * 0.35
        + agg["score_qualidade"] * 0.30
        + agg["score_logistica"] * 0.20
        + agg["score_continuidade"] * 0.15
    ).round(1)
    agg["classe_risco"] = agg["score_risco_fornecedor"].apply(classificar_risco)
    agg["recomendacao"] = agg.apply(gerar_recomendacao, axis=1)

    return agg.sort_values("score_risco_fornecedor", ascending=False).reset_index(drop=True)


def _calcular_tendencia_produtor(sub: pd.DataFrame) -> float:
    sub = sub.sort_values("data")
    if len(sub) < 14:
        return 0.0
    janela = min(30, max(7, len(sub) // 4))
    inicio = sub["litros_coletados"].head(janela).mean()
    fim = sub["litros_coletados"].tail(janela).mean()
    if not inicio or pd.isna(inicio):
        tendencia = 0.0
    else:
        tendencia = (fim - inicio) / inicio * 100
    return float(tendencia)
