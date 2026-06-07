from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ingestao_clima_inmet import enriquecer_clima
from validar_pacote_dados_reais import validate_package

DEFAULT_CLIMATE_SOURCE = Path("dados_inmet_processado") / "fact_clima_diario_inmet.csv"
FALLBACK_CLIMATE_SOURCE = Path("dados_teste") / "fact_clima_diario.csv"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def normalize_text_series(series: pd.Series, default: str = "") -> pd.Series:
    return series.fillna(default).astype(str).str.strip()


def normalize_key_series(series: pd.Series, default: str = "") -> pd.Series:
    return normalize_text_series(series, default).str.upper()


def to_numeric(series: pd.Series, default: float = 0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(default)


def build_dim_tempo(dates: pd.Series) -> pd.DataFrame:
    datas = pd.date_range(dates.min(), dates.max(), freq="D")
    df = pd.DataFrame({"data": datas})
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia"] = df["data"].dt.day
    df["dia_semana"] = df["data"].dt.weekday
    df["semana_ano"] = df["data"].dt.isocalendar().week.astype(int)
    df["trimestre"] = df["data"].dt.quarter
    df["dia_do_ano"] = df["data"].dt.dayofyear
    df["flag_fim_semana"] = df["dia_semana"].isin([5, 6]).astype(int)
    df["flag_feriado"] = 0
    df["estacao_climatica"] = df["mes"].map(
        {
            1: "CHUVOSA",
            2: "CHUVOSA",
            3: "CHUVOSA",
            4: "TRANSICAO_CHUVA_SECA",
            5: "SECA",
            6: "SECA",
            7: "SECA",
            8: "SECA",
            9: "SECA",
            10: "TRANSICAO_SECA_CHUVA",
            11: "CHUVOSA",
            12: "CHUVOSA",
        }
    )
    return df


def normalize_dim_produtor(dim_prod: pd.DataFrame, fact_prod: pd.DataFrame) -> pd.DataFrame:
    df = dim_prod.copy()
    df["id_produtor"] = normalize_text_series(df["id_produtor"])
    df["nome_ficticio"] = normalize_text_series(df["nome_ficticio"])
    df["municipio"] = normalize_text_series(df["municipio"])
    df["polo_climatico"] = normalize_key_series(df["polo_climatico"])
    df["id_laticinio_principal"] = normalize_text_series(df["id_laticinio_principal"])
    df["id_rota_principal"] = normalize_text_series(df["id_rota_principal"])
    df["tipo_sistema"] = normalize_key_series(df.get("tipo_sistema", pd.Series("NAO_INFORMADO", index=df.index)), "NAO_INFORMADO")
    df["nivel_tecnificacao"] = normalize_key_series(df.get("nivel_tecnificacao", pd.Series("NAO_INFORMADO", index=df.index)), "NAO_INFORMADO")
    df["raca_predominante"] = normalize_key_series(df.get("raca_predominante", pd.Series("NAO_INFORMADO", index=df.index)), "NAO_INFORMADO")
    df["porte_produtor"] = normalize_key_series(df.get("porte_produtor", pd.Series("NAO_INFORMADO", index=df.index)), "NAO_INFORMADO")

    prod_avg = (
        fact_prod.groupby("id_produtor", as_index=False)["litros_coletados"]
        .mean()
        .rename(columns={"litros_coletados": "litros_coletados_media"})
    )
    df = df.merge(prod_avg, on="id_produtor", how="left")

    df["vacas_lactacao"] = to_numeric(df.get("vacas_lactacao", pd.Series(0, index=df.index)), 0).round().astype(int)
    df["producao_media_esperada_litros_dia"] = to_numeric(
        df.get("producao_media_esperada_litros_dia", df["litros_coletados_media"]),
        0,
    )
    df["producao_media_esperada_litros_dia"] = df["producao_media_esperada_litros_dia"].where(
        df["producao_media_esperada_litros_dia"] > 0,
        df["litros_coletados_media"].fillna(0),
    )
    df["capacidade_maxima_litros_dia"] = to_numeric(
        df.get("capacidade_maxima_litros_dia", df["producao_media_esperada_litros_dia"] * 1.1),
        0,
    )
    df["distancia_km_laticinio"] = to_numeric(df.get("distancia_km_laticinio", pd.Series(0, index=df.index)), 0)
    df["sensibilidade_seca"] = to_numeric(df.get("sensibilidade_seca", pd.Series(1.0, index=df.index)), 1.0)
    df["sensibilidade_calor"] = to_numeric(df.get("sensibilidade_calor", pd.Series(1.0, index=df.index)), 1.0)
    df["sensibilidade_qualidade"] = to_numeric(df.get("sensibilidade_qualidade", pd.Series(1.0, index=df.index)), 1.0)
    df["prob_churn_base"] = to_numeric(df.get("prob_churn_base", pd.Series(0.0, index=df.index)), 0.0)
    df["data_inicio_fornecimento"] = pd.to_datetime(df["data_inicio_fornecimento"], errors="coerce")
    fallback_start = pd.to_datetime(fact_prod["data"], errors="coerce").min()
    df["data_inicio_fornecimento"] = df["data_inicio_fornecimento"].fillna(fallback_start)
    df["ativo"] = to_numeric(df.get("ativo", pd.Series(1, index=df.index)), 1).astype(int)
    return df[
        [
            "id_produtor",
            "nome_ficticio",
            "municipio",
            "polo_climatico",
            "id_laticinio_principal",
            "id_rota_principal",
            "tipo_sistema",
            "nivel_tecnificacao",
            "raca_predominante",
            "porte_produtor",
            "vacas_lactacao",
            "producao_media_esperada_litros_dia",
            "capacidade_maxima_litros_dia",
            "distancia_km_laticinio",
            "sensibilidade_seca",
            "sensibilidade_calor",
            "sensibilidade_qualidade",
            "prob_churn_base",
            "data_inicio_fornecimento",
            "ativo",
        ]
    ]


def normalize_dim_rota(dim_rota: pd.DataFrame) -> pd.DataFrame:
    df = dim_rota.copy()
    df["id_rota"] = normalize_text_series(df["id_rota"])
    df["id_laticinio"] = normalize_text_series(df["id_laticinio"])
    df["polo_climatico"] = normalize_key_series(df["polo_climatico"])
    df["km_planejado"] = to_numeric(df.get("km_planejado", pd.Series(0, index=df.index)), 0)
    df["capacidade_tanque_litros"] = to_numeric(df.get("capacidade_tanque_litros", pd.Series(0, index=df.index)), 0)
    df["tempo_medio_horas"] = to_numeric(df.get("tempo_medio_horas", pd.Series(0, index=df.index)), 0)
    df["dificuldade_logistica"] = normalize_key_series(
        df.get("dificuldade_logistica", pd.Series("MEDIA", index=df.index)),
        "MEDIA",
    )
    df["percentual_estrada_nao_pavimentada"] = to_numeric(
        df.get("percentual_estrada_nao_pavimentada", pd.Series(0, index=df.index)),
        0,
    )
    return df[
        [
            "id_rota",
            "id_laticinio",
            "polo_climatico",
            "km_planejado",
            "capacidade_tanque_litros",
            "tempo_medio_horas",
            "dificuldade_logistica",
            "percentual_estrada_nao_pavimentada",
        ]
    ]


def normalize_fact_producao(fact_prod: pd.DataFrame, dim_prod: pd.DataFrame, dim_rota: pd.DataFrame, fact_rota: pd.DataFrame | None) -> pd.DataFrame:
    df = fact_prod.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["id_produtor"] = normalize_text_series(df["id_produtor"])
    df["id_laticinio"] = normalize_text_series(df["id_laticinio"])
    df["id_rota"] = normalize_text_series(df["id_rota"])
    df["polo_climatico"] = normalize_key_series(df["polo_climatico"])

    dim_prod_ref = dim_prod[["id_produtor", "id_laticinio_principal", "id_rota_principal", "polo_climatico"]].rename(
        columns={
            "id_laticinio_principal": "id_laticinio_dim",
            "id_rota_principal": "id_rota_dim",
            "polo_climatico": "polo_dim",
        }
    )
    df = df.merge(dim_prod_ref, on="id_produtor", how="left")
    df["id_laticinio"] = df["id_laticinio"].replace("", pd.NA).fillna(df["id_laticinio_dim"])
    df["id_rota"] = df["id_rota"].replace("", pd.NA).fillna(df["id_rota_dim"])
    df["polo_climatico"] = df["polo_climatico"].replace("", pd.NA).fillna(df["polo_dim"])
    df = df.drop(columns=["id_laticinio_dim", "id_rota_dim", "polo_dim"])

    route_rate = pd.DataFrame()
    if fact_rota is not None and not fact_rota.empty:
        route_rate = fact_rota[["data", "id_rota", "custo_total", "litros_realizados"]].copy()
        route_rate["data"] = pd.to_datetime(route_rate["data"], errors="coerce")
        route_rate["id_rota"] = normalize_text_series(route_rate["id_rota"])
        route_rate["custo_total"] = to_numeric(route_rate["custo_total"], 0)
        route_rate["litros_realizados"] = to_numeric(route_rate["litros_realizados"], 0)
        route_rate["custo_logistico_rota"] = route_rate["custo_total"] / route_rate["litros_realizados"].replace(0, np.nan)
        route_rate["custo_logistico_rota"] = route_rate["custo_logistico_rota"].fillna(0)
        route_rate = route_rate[["data", "id_rota", "custo_logistico_rota"]]
        df = df.merge(route_rate, on=["data", "id_rota"], how="left")
    else:
        df["custo_logistico_rota"] = 0.0

    dim_rota_ref = dim_rota[["id_rota", "km_planejado", "dificuldade_logistica", "percentual_estrada_nao_pavimentada"]]
    df = df.merge(dim_rota_ref, on="id_rota", how="left")

    df["litros_coletados"] = to_numeric(df["litros_coletados"], 0)
    df["litros_previstos"] = to_numeric(df.get("litros_previstos", df["litros_coletados"]), 0)
    df["litros_previstos"] = df["litros_previstos"].where(df["litros_previstos"] > 0, df["litros_coletados"])
    df["litros_produzidos"] = to_numeric(df.get("litros_produzidos", df["litros_coletados"]), 0)
    df["litros_produzidos"] = df["litros_produzidos"].where(df["litros_produzidos"] > 0, df["litros_coletados"])
    df["litros_descartados"] = to_numeric(
        df.get("litros_descartados", (df["litros_produzidos"] - df["litros_coletados"]).clip(lower=0)),
        0,
    )
    df["ccs"] = to_numeric(df.get("ccs", pd.Series(0, index=df.index)), 0)
    df["cbt"] = to_numeric(df.get("cbt", pd.Series(0, index=df.index)), 0)
    df["temp_tanque_c"] = to_numeric(df.get("temp_tanque_c", pd.Series(0, index=df.index)), 0)
    df["flag_antibiotico"] = to_numeric(df.get("flag_antibiotico", pd.Series(0, index=df.index)), 0).astype(int)
    flag_q = df.get("flag_qualidade_reprovada", pd.Series(np.nan, index=df.index))
    flag_q = pd.to_numeric(flag_q, errors="coerce")
    derived_flag_q = ((df["ccs"] >= 600) | (df["cbt"] >= 200) | (df["temp_tanque_c"] > 4.5)).astype(int)
    df["flag_qualidade_reprovada"] = flag_q.fillna(derived_flag_q).astype(int)
    df["flag_falha_coleta"] = to_numeric(df.get("flag_falha_coleta", pd.Series(0, index=df.index)), 0).astype(int)
    df["flag_mudou_laticinio"] = to_numeric(df.get("flag_mudou_laticinio", pd.Series(0, index=df.index)), 0).astype(int)

    df["score_sanidade"] = to_numeric(df.get("score_sanidade", pd.Series(0.5, index=df.index)), 0.5)
    df["score_manejo"] = to_numeric(df.get("score_manejo", pd.Series(0.5, index=df.index)), 0.5)
    fallback_cost = (to_numeric(df["km_planejado"], 0) * 0.012).fillna(0)
    df["custo_logistico_rateado"] = to_numeric(
        df.get("custo_logistico_rateado", df["custo_logistico_rota"].where(df["custo_logistico_rota"] > 0, fallback_cost)),
        0,
    )
    df["margem_estimada_fornecedor"] = to_numeric(df.get("margem_estimada_fornecedor", pd.Series(0.45, index=df.index)), 0.45)
    df["target_queda_7d"] = to_numeric(df.get("target_queda_7d", pd.Series(0, index=df.index)), 0).astype(int)
    df["target_queda_15d"] = to_numeric(df.get("target_queda_15d", pd.Series(0, index=df.index)), 0).astype(int)
    df["target_queda_30d"] = to_numeric(df.get("target_queda_30d", pd.Series(0, index=df.index)), 0).astype(int)

    return df[
        [
            "data",
            "id_produtor",
            "id_laticinio",
            "id_rota",
            "polo_climatico",
            "litros_previstos",
            "litros_produzidos",
            "litros_coletados",
            "litros_descartados",
            "ccs",
            "cbt",
            "temp_tanque_c",
            "flag_antibiotico",
            "flag_qualidade_reprovada",
            "flag_falha_coleta",
            "flag_mudou_laticinio",
            "score_sanidade",
            "score_manejo",
            "custo_logistico_rateado",
            "margem_estimada_fornecedor",
            "target_queda_7d",
            "target_queda_15d",
            "target_queda_30d",
        ]
    ].sort_values(["data", "id_produtor"]).reset_index(drop=True)


def build_fact_rota_dia(fact_prod: pd.DataFrame, dim_rota: pd.DataFrame, fact_rota: pd.DataFrame | None) -> pd.DataFrame:
    if fact_rota is not None and not fact_rota.empty:
        df = fact_rota.copy()
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df["id_rota"] = normalize_text_series(df["id_rota"])
        df["id_laticinio"] = normalize_text_series(df["id_laticinio"])
        for col in [
            "litros_previstos",
            "litros_realizados",
            "num_produtores_planejados",
            "num_produtores_atendidos",
            "custo_total",
            "km_rodados",
            "tempo_total_horas",
            "ocupacao_tanque_pct",
            "indice_atraso",
            "indice_perda_rota",
        ]:
            if col in df.columns:
                df[col] = to_numeric(df[col], 0)
        defaults = {
            "num_produtores_planejados": 0,
            "num_produtores_atendidos": 0,
            "custo_total": 0,
            "ocupacao_tanque_pct": 0,
            "indice_atraso": 0,
            "indice_perda_rota": 0,
        }
        for col, value in defaults.items():
            if col not in df.columns:
                df[col] = value
        return df[
            [
                "data",
                "id_rota",
                "id_laticinio",
                "litros_previstos",
                "litros_realizados",
                "num_produtores_planejados",
                "num_produtores_atendidos",
                "custo_total",
                "km_rodados",
                "tempo_total_horas",
                "ocupacao_tanque_pct",
                "indice_atraso",
                "indice_perda_rota",
            ]
        ].sort_values(["data", "id_rota"]).reset_index(drop=True)

    grouped = fact_prod.groupby(["data", "id_rota", "id_laticinio"], as_index=False).agg(
        litros_previstos=("litros_previstos", "sum"),
        litros_realizados=("litros_coletados", "sum"),
        num_produtores_planejados=("id_produtor", "nunique"),
        num_produtores_atendidos=("id_produtor", "nunique"),
        custo_total=("custo_logistico_rateado", lambda s: float((s * fact_prod.loc[s.index, "litros_coletados"]).sum())),
    )
    grouped = grouped.merge(
        dim_rota[["id_rota", "km_planejado", "tempo_medio_horas", "capacidade_tanque_litros", "dificuldade_logistica"]],
        on="id_rota",
        how="left",
    )
    grouped["km_rodados"] = to_numeric(grouped["km_planejado"], 0)
    grouped["tempo_total_horas"] = to_numeric(grouped["tempo_medio_horas"], 0)
    grouped["ocupacao_tanque_pct"] = (
        grouped["litros_realizados"] / to_numeric(grouped["capacidade_tanque_litros"], 0).replace(0, np.nan) * 100
    ).fillna(0)
    grouped["indice_atraso"] = grouped["dificuldade_logistica"].map({"BAIXA": 0.02, "MEDIA": 0.05, "ALTA": 0.09}).fillna(0.04)
    grouped["indice_perda_rota"] = (
        (grouped["litros_previstos"] - grouped["litros_realizados"]) / grouped["litros_previstos"].replace(0, np.nan)
    ).fillna(0).clip(lower=0)
    return grouped[
        [
            "data",
            "id_rota",
            "id_laticinio",
            "litros_previstos",
            "litros_realizados",
            "num_produtores_planejados",
            "num_produtores_atendidos",
            "custo_total",
            "km_rodados",
            "tempo_total_horas",
            "ocupacao_tanque_pct",
            "indice_atraso",
            "indice_perda_rota",
        ]
    ].sort_values(["data", "id_rota"]).reset_index(drop=True)


def build_dim_laticinio(dim_prod: pd.DataFrame, dim_rota: pd.DataFrame, fact_prod: pd.DataFrame) -> pd.DataFrame:
    route_counts = dim_rota.groupby("id_laticinio", as_index=False).agg(numero_rotas=("id_rota", "nunique"))
    prod_stats = dim_prod.groupby("id_laticinio_principal", as_index=False).agg(
        municipio_base=("municipio", lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0]),
        raio_medio_captacao_km=("distancia_km_laticinio", "mean"),
    ).rename(columns={"id_laticinio_principal": "id_laticinio"})
    prod_daily = fact_prod.groupby(["data", "id_laticinio"], as_index=False)["litros_coletados"].sum()
    cap = prod_daily.groupby("id_laticinio", as_index=False)["litros_coletados"].max().rename(
        columns={"litros_coletados": "capacidade_recebimento_litros_dia"}
    )

    df = prod_stats.merge(route_counts, on="id_laticinio", how="outer").merge(cap, on="id_laticinio", how="outer")
    df["municipio_base"] = normalize_text_series(df.get("municipio_base", pd.Series("Nao informado", index=df.index)), "Nao informado")
    df["capacidade_recebimento_litros_dia"] = (to_numeric(df["capacidade_recebimento_litros_dia"], 0) * 1.15).round().astype(int)
    df["numero_rotas"] = to_numeric(df["numero_rotas"], 0).round().astype(int)
    df["raio_medio_captacao_km"] = to_numeric(df["raio_medio_captacao_km"], 0).round(2)
    df["perfil_operacional"] = "PADRAO"
    return df[
        [
            "id_laticinio",
            "municipio_base",
            "capacidade_recebimento_litros_dia",
            "numero_rotas",
            "raio_medio_captacao_km",
            "perfil_operacional",
        ]
    ].sort_values("id_laticinio").reset_index(drop=True)


def load_climate_source(climate_path: Path | None) -> pd.DataFrame:
    source = climate_path if climate_path else DEFAULT_CLIMATE_SOURCE
    if source.exists():
        return pd.read_csv(source, parse_dates=["data"])
    if FALLBACK_CLIMATE_SOURCE.exists():
        return pd.read_csv(FALLBACK_CLIMATE_SOURCE, parse_dates=["data"])
    raise FileNotFoundError("Nenhuma fonte de clima encontrada para enriquecer o pacote real.")


def build_fact_clima_diario(fact_prod: pd.DataFrame, climate_path: Path | None) -> pd.DataFrame:
    climate = load_climate_source(climate_path).copy()
    climate["data"] = pd.to_datetime(climate["data"], errors="coerce")
    climate["polo_climatico"] = normalize_key_series(climate["polo_climatico"])

    target_dates = pd.date_range(fact_prod["data"].min(), fact_prod["data"].max(), freq="D")
    target_polos = sorted(fact_prod["polo_climatico"].dropna().unique().tolist())

    base = climate[climate["polo_climatico"].isin(target_polos)].copy()
    if base.empty:
        base = climate.copy()

    frames: list[pd.DataFrame] = []
    available_polos = sorted(base["polo_climatico"].dropna().unique().tolist())
    overall_daily = base.groupby("data", as_index=False).mean(numeric_only=True)

    for polo in target_polos:
        sub = base[base["polo_climatico"] == polo].copy()
        if sub.empty:
            sub = overall_daily.copy()
            sub["polo_climatico"] = polo

        sub = sub.set_index("data").reindex(target_dates).rename_axis("data").reset_index()
        sub["polo_climatico"] = polo
        if "codigo_estacao" not in sub.columns:
            sub["codigo_estacao"] = pd.NA
        if "arquivo_origem" not in sub.columns:
            sub["arquivo_origem"] = "clima_referencia"
        frames.append(sub)

    climate_target = pd.concat(frames, ignore_index=True)
    climate_target = enriquecer_clima(climate_target)
    keep_cols = [
        "data",
        "polo_climatico",
        "temp_min_c",
        "temp_max_c",
        "temp_med_c",
        "umidade_med_pct",
        "precip_mm",
        "vento_med_ms",
        "radiacao_proxy",
        "precip_3d",
        "precip_7d",
        "precip_15d",
        "dias_sem_chuva",
        "thi",
        "thi_3d_avg",
        "onda_calor_3d",
        "onda_calor_5d",
        "dry_spell_10d",
        "anomalia_temp",
        "indice_favorabilidade_pastagem",
    ]
    return climate_target[keep_cols].sort_values(["polo_climatico", "data"]).reset_index(drop=True)


def import_package(input_dir: Path, output_dir: Path, climate_path: Path | None = None) -> dict:
    report = validate_package(input_dir)
    if report["status"] == "error":
        raise ValueError("Pacote de dados reais inválido. Rode o validador e corrija os erros antes da importação.")

    ensure_dir(output_dir)

    dim_prod_raw = read_csv(input_dir / "dim_produtor.csv")
    fact_prod_raw = read_csv(input_dir / "fact_producao_produtor_dia.csv")
    dim_rota_raw = read_csv(input_dir / "dim_rota.csv")
    fact_rota_raw = read_csv(input_dir / "fact_rota_dia.csv") if (input_dir / "fact_rota_dia.csv").exists() else None

    dim_rota = normalize_dim_rota(dim_rota_raw)
    fact_prod_base = fact_prod_raw.copy()
    fact_prod_base["data"] = pd.to_datetime(fact_prod_base["data"], errors="coerce")
    fact_prod_base["id_produtor"] = normalize_text_series(fact_prod_base["id_produtor"])
    fact_prod_base["litros_coletados"] = to_numeric(fact_prod_base["litros_coletados"], 0)
    dim_prod = normalize_dim_produtor(dim_prod_raw, fact_prod_base)
    fact_prod = normalize_fact_producao(fact_prod_raw, dim_prod, dim_rota, fact_rota_raw)
    fact_rota = build_fact_rota_dia(fact_prod, dim_rota, fact_rota_raw)
    dim_laticinio = build_dim_laticinio(dim_prod, dim_rota, fact_prod)
    dim_tempo = build_dim_tempo(fact_prod["data"])
    fact_clima = build_fact_clima_diario(fact_prod, climate_path)

    dim_prod.to_csv(output_dir / "dim_produtor.csv", index=False, encoding="utf-8-sig")
    fact_prod.to_csv(output_dir / "fact_producao_produtor_dia.csv", index=False, encoding="utf-8-sig")
    dim_rota.to_csv(output_dir / "dim_rota.csv", index=False, encoding="utf-8-sig")
    fact_rota.to_csv(output_dir / "fact_rota_dia.csv", index=False, encoding="utf-8-sig")
    dim_laticinio.to_csv(output_dir / "dim_laticinio.csv", index=False, encoding="utf-8-sig")
    dim_tempo.to_csv(output_dir / "dim_tempo.csv", index=False, encoding="utf-8-sig")
    fact_clima.to_csv(output_dir / "fact_clima_diario.csv", index=False, encoding="utf-8-sig")

    manifest = {
        "input_dir": str(input_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "climate_source": str((climate_path or (DEFAULT_CLIMATE_SOURCE if DEFAULT_CLIMATE_SOURCE.exists() else FALLBACK_CLIMATE_SOURCE)).resolve()),
        "validation": report,
        "outputs": {
            "dim_produtor": int(len(dim_prod)),
            "fact_producao_produtor_dia": int(len(fact_prod)),
            "dim_rota": int(len(dim_rota)),
            "fact_rota_dia": int(len(fact_rota)),
            "dim_laticinio": int(len(dim_laticinio)),
            "dim_tempo": int(len(dim_tempo)),
            "fact_clima_diario": int(len(fact_clima)),
        },
    }
    (output_dir / "manifesto_importacao.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Importa um pacote de dados reais para a estrutura operacional do Via Leite.")
    parser.add_argument("--input-dir", type=Path, required=True, help="Diretorio com os arquivos CSV entregues pelo cliente.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Diretorio de saída no formato consumido pelo Via Leite.")
    parser.add_argument("--climate-path", type=Path, default=None, help="Arquivo de clima opcional para enriquecimento.")
    args = parser.parse_args()

    manifest = import_package(args.input_dir, args.output_dir, args.climate_path)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
