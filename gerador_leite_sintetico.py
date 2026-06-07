from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

START_DATE = "2021-01-01"
END_DATE = "2025-12-31"

N_PRODUTORES = 2400
N_LATICINIOS = 4

OUTPUT_DIR = "dados_teste"

# Colunas esperadas em fact_clima_diario (sintético ou INMET já enriquecido)
CLIMA_COLUNAS_FACT = [
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

POLOS = {
    "RIO_VERDE": {"peso": 0.35, "temp_offset": 0.0, "rain_factor": 1.00},
    "JATAI": {"peso": 0.25, "temp_offset": 0.3, "rain_factor": 0.95},
    "MINEIROS": {"peso": 0.20, "temp_offset": 0.6, "rain_factor": 0.90},
    "SUDESTE_SUL_GOIANO": {"peso": 0.20, "temp_offset": -0.2, "rain_factor": 1.05},
}

SISTEMAS = ["PASTO", "SEMI_CONFINADO", "CONFINADO"]
PESO_SISTEMAS = [0.55, 0.30, 0.15]

TECNIFICACAO = ["BAIXO", "MEDIO", "ALTO"]
PESO_TEC = [0.40, 0.40, 0.20]

RACAS = ["GIROLANDO", "HOLANDESA", "MISTA"]
PESO_RACAS = [0.45, 0.25, 0.30]

PERFIL_LATICINIO = ["EFICIENTE", "PADRAO", "RESTRITO"]
PESO_PERFIL_LATICINIO = [0.30, 0.50, 0.20]

MUNICIPIOS_POLO = {
    "RIO_VERDE": ["Rio Verde", "Montividiu", "Santo Antônio da Barra"],
    "JATAI": ["Jataí", "Perolândia", "Serranópolis"],
    "MINEIROS": ["Mineiros", "Portelândia", "Santa Rita do Araguaia"],
    "SUDESTE_SUL_GOIANO": ["Morrinhos", "Piracanjuba", "Itumbiara"],
}


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def classify_estacao(month: int) -> str:
    if month in [11, 12, 1, 2, 3]:
        return "CHUVOSA"
    if month == 4:
        return "TRANSICAO_CHUVA_SECA"
    if month in [5, 6, 7, 8, 9]:
        return "SECA"
    return "TRANSICAO_SECA_CHUVA"


def calc_thi(temp_c: pd.Series, umidade_pct: pd.Series) -> pd.Series:
    return (1.8 * temp_c + 32) - ((0.55 - 0.0055 * umidade_pct) * (1.8 * temp_c - 26))


def normaliza_serie(x: pd.Series) -> pd.Series:
    std = x.std()
    if std == 0 or pd.isna(std):
        return pd.Series(np.zeros(len(x)), index=x.index)
    return (x - x.mean()) / std


def gerar_dim_tempo(start_date: str, end_date: str) -> pd.DataFrame:
    datas = pd.date_range(start_date, end_date, freq="D")
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
    df["estacao_climatica"] = df["mes"].apply(classify_estacao)
    return df


def gerar_clima_diario(dim_tempo: pd.DataFrame) -> pd.DataFrame:
    frames = []

    for polo, cfg in POLOS.items():
        base = dim_tempo[["data", "ano", "mes", "dia_do_ano", "estacao_climatica"]].copy()
        n = len(base)

        seasonal_temp = 24 + 3.0 * np.sin(2 * np.pi * (base["dia_do_ano"] - 300) / 365.25)
        temp_media = seasonal_temp + cfg["temp_offset"] + rng.normal(0, 1.0, n)
        amp = 8 + rng.normal(0, 1.0, n)
        temp_min = temp_media - amp / 2
        temp_max = temp_media + amp / 2

        chuva_bruta = (
            4.0
            + 5.5 * (1 + np.sin(2 * np.pi * (base["dia_do_ano"] - 320) / 365.25))
            + rng.gamma(shape=1.4, scale=2.0, size=n)
        )
        fator_mes = np.where(base["mes"].isin([5, 6, 7, 8, 9]), 0.12, 1.0)
        fator_mes = np.where(base["mes"] == 10, 0.55, fator_mes)
        precip = chuva_bruta * fator_mes * cfg["rain_factor"]

        prob_sem_chuva = np.where(base["mes"].isin([5, 6, 7, 8, 9]), 0.82, 0.42)
        sem_chuva = rng.random(n) < prob_sem_chuva
        precip = np.where(sem_chuva, 0.0, precip)

        chuva_extrema_idx = rng.choice(n, size=max(3, n // 180), replace=False)
        precip[chuva_extrema_idx] *= rng.uniform(2.5, 4.5, size=len(chuva_extrema_idx))

        for _ in range(3):
            start = int(rng.integers(0, n - 20))
            dur = int(rng.integers(7, 18))
            if base.iloc[start]["mes"] in [5, 6, 7, 8, 9, 10]:
                precip[start:start + dur] = precip[start:start + dur] * rng.uniform(0.0, 0.15)

        umidade = 68 + 0.35 * precip - 0.55 * (temp_max - temp_media) + rng.normal(0, 4, n)
        umidade = np.clip(umidade, 28, 98)
        vento = np.clip(rng.normal(2.8, 0.9, n), 0.2, 8.0)
        radiacao_proxy = np.clip(
            1.0 + 0.04 * (temp_max - 20) - 0.02 * precip + rng.normal(0, 0.08, n),
            0.3,
            1.8,
        )

        df = pd.DataFrame({
            "data": base["data"],
            "polo_climatico": polo,
            "temp_min_c": temp_min,
            "temp_max_c": temp_max,
            "temp_med_c": temp_media,
            "umidade_med_pct": umidade,
            "precip_mm": precip,
            "vento_med_ms": vento,
            "radiacao_proxy": radiacao_proxy,
        })

        df["precip_3d"] = df["precip_mm"].rolling(3, min_periods=1).sum()
        df["precip_7d"] = df["precip_mm"].rolling(7, min_periods=1).sum()
        df["precip_15d"] = df["precip_mm"].rolling(15, min_periods=1).sum()

        dias_sem_chuva = []
        contador = 0
        for p in df["precip_mm"].values:
            if p < 1.0:
                contador += 1
            else:
                contador = 0
            dias_sem_chuva.append(contador)
        df["dias_sem_chuva"] = dias_sem_chuva

        df["thi"] = calc_thi(df["temp_med_c"], df["umidade_med_pct"])
        df["thi_3d_avg"] = df["thi"].rolling(3, min_periods=1).mean()
        df["onda_calor_3d"] = (df["thi_3d_avg"] >= 74).astype(int)
        df["onda_calor_5d"] = (df["thi"].rolling(5, min_periods=1).mean() >= 74).astype(int)
        df["dry_spell_10d"] = (df["dias_sem_chuva"] >= 10).astype(int)

        media_mensal = df.groupby(df["data"].dt.month)["temp_med_c"].transform("mean")
        df["anomalia_temp"] = df["temp_med_c"] - media_mensal

        fav = 0.015 * df["precip_15d"] - 0.025 * df["dias_sem_chuva"] - 0.020 * np.maximum(df["thi"] - 72, 0)
        df["indice_favorabilidade_pastagem"] = np.clip(1 + fav, 0.4, 1.3)
        frames.append(df)

    clima = pd.concat(frames, ignore_index=True)
    clima = clima.sort_values(["polo_climatico", "data"]).reset_index(drop=True)
    return clima


def carregar_clima_de_arquivo(path: Path, dim_tempo: pd.DataFrame) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de clima não encontrado: {path}")
    df = pd.read_csv(path, parse_dates=["data"])
    missing = [c for c in CLIMA_COLUNAS_FACT if c not in df.columns]
    if missing:
        raise ValueError(f"CSV de clima real sem colunas obrigatórias: {missing}")
    df = df[CLIMA_COLUNAS_FACT].copy()
    dmin, dmax = dim_tempo["data"].min(), dim_tempo["data"].max()
    df = df[(df["data"] >= dmin) & (df["data"] <= dmax)]
    return df.sort_values(["polo_climatico", "data"]).reset_index(drop=True)


def gerar_dim_laticinio() -> pd.DataFrame:
    municipios_base = ["Rio Verde", "Jataí", "Mineiros", "Itumbiara"]
    rows = []
    for i in range(N_LATICINIOS):
        rows.append({
            "id_laticinio": i + 1,
            "municipio_base": municipios_base[i],
            "capacidade_recebimento_litros_dia": int(rng.integers(80000, 450001)),
            "numero_rotas": int(rng.integers(8, 17)),
            "raio_medio_captacao_km": float(np.round(rng.uniform(40, 180), 2)),
            "perfil_operacional": rng.choice(PERFIL_LATICINIO, p=PESO_PERFIL_LATICINIO),
        })
    return pd.DataFrame(rows)


def gerar_dim_rota(dim_laticinio: pd.DataFrame) -> pd.DataFrame:
    rows = []
    id_rota = 1
    for _, lac in dim_laticinio.iterrows():
        for _ in range(int(lac["numero_rotas"])):
            dificuldade = rng.choice(["BAIXA", "MEDIA", "ALTA"], p=[0.35, 0.45, 0.20])
            pct_nao_pav = {
                "BAIXA": rng.uniform(0.00, 0.15),
                "MEDIA": rng.uniform(0.10, 0.40),
                "ALTA": rng.uniform(0.35, 0.80),
            }[dificuldade]
            rows.append({
                "id_rota": id_rota,
                "id_laticinio": int(lac["id_laticinio"]),
                "polo_climatico": rng.choice(list(POLOS.keys()), p=[POLOS[p]["peso"] for p in POLOS]),
                "km_planejado": float(np.round(rng.uniform(60, 280), 2)),
                "capacidade_tanque_litros": int(rng.integers(5000, 22001)),
                "tempo_medio_horas": float(np.round(rng.uniform(3.0, 10.0), 2)),
                "dificuldade_logistica": dificuldade,
                "percentual_estrada_nao_pavimentada": float(np.round(pct_nao_pav, 3)),
            })
            id_rota += 1
    return pd.DataFrame(rows)


def gerar_dim_produtor(dim_rota: pd.DataFrame) -> pd.DataFrame:
    pesos_polos = [POLOS[k]["peso"] for k in POLOS]
    polos = list(POLOS.keys())
    rows = []
    for i in range(N_PRODUTORES):
        polo = rng.choice(polos, p=pesos_polos)
        sistema = rng.choice(SISTEMAS, p=PESO_SISTEMAS)
        tec = rng.choice(TECNIFICACAO, p=PESO_TEC)
        raca = rng.choice(RACAS, p=PESO_RACAS)
        porte = rng.choice(["PEQUENO", "MEDIO", "GRANDE"], p=[0.58, 0.30, 0.12])
        if porte == "PEQUENO":
            vacas = int(rng.integers(12, 41))
        elif porte == "MEDIO":
            vacas = int(rng.integers(41, 121))
        else:
            vacas = int(rng.integers(121, 221))

        prod_vaca_map = {
            ("PASTO", "BAIXO"): rng.uniform(7, 11),
            ("PASTO", "MEDIO"): rng.uniform(9, 13),
            ("PASTO", "ALTO"): rng.uniform(11, 15),
            ("SEMI_CONFINADO", "BAIXO"): rng.uniform(11, 15),
            ("SEMI_CONFINADO", "MEDIO"): rng.uniform(14, 20),
            ("SEMI_CONFINADO", "ALTO"): rng.uniform(18, 24),
            ("CONFINADO", "BAIXO"): rng.uniform(17, 22),
            ("CONFINADO", "MEDIO"): rng.uniform(20, 28),
            ("CONFINADO", "ALTO"): rng.uniform(24, 34),
        }
        prod_vaca = prod_vaca_map[(sistema, tec)]
        if raca == "HOLANDESA":
            prod_vaca *= 1.08
        elif raca == "MISTA":
            prod_vaca *= 0.94
        prod_media = vacas * prod_vaca

        rotas_polo = dim_rota[dim_rota["polo_climatico"] == polo]
        rota = rotas_polo.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0] if not rotas_polo.empty else dim_rota.sample(1).iloc[0]

        sens_seca = {"PASTO": rng.uniform(0.90, 1.20), "SEMI_CONFINADO": rng.uniform(0.55, 0.90), "CONFINADO": rng.uniform(0.20, 0.50)}[sistema]
        sens_calor = {"PASTO": rng.uniform(0.70, 1.05), "SEMI_CONFINADO": rng.uniform(0.65, 1.00), "CONFINADO": rng.uniform(0.55, 0.95)}[sistema]
        if tec == "ALTO":
            sens_calor *= 0.88
            sens_seca *= 0.82
        elif tec == "BAIXO":
            sens_calor *= 1.08
            sens_seca *= 1.10

        rows.append({
            "id_produtor": i + 1,
            "nome_ficticio": f"PRODUTOR_{i+1:05d}",
            "municipio": rng.choice(MUNICIPIOS_POLO[polo]),
            "polo_climatico": polo,
            "id_laticinio_principal": int(rota["id_laticinio"]),
            "id_rota_principal": int(rota["id_rota"]),
            "tipo_sistema": sistema,
            "nivel_tecnificacao": tec,
            "raca_predominante": raca,
            "porte_produtor": porte,
            "vacas_lactacao": vacas,
            "producao_media_esperada_litros_dia": float(np.round(prod_media, 2)),
            "capacidade_maxima_litros_dia": float(np.round(prod_media * rng.uniform(1.05, 1.35), 2)),
            "distancia_km_laticinio": float(np.round(rng.uniform(8, 180), 2)),
            "sensibilidade_seca": float(np.round(sens_seca, 3)),
            "sensibilidade_calor": float(np.round(sens_calor, 3)),
            "sensibilidade_qualidade": float(np.round(rng.uniform(0.7, 1.3), 3)),
            "prob_churn_base": float(np.round(rng.uniform(0.00005, 0.0015), 6)),
            "data_inicio_fornecimento": pd.Timestamp(pd.Timestamp(START_DATE) - pd.Timedelta(days=int(rng.integers(180, 1600)))),
            "ativo": 1,
        })
    return pd.DataFrame(rows)


@dataclass
class ProdutorParams:
    id_produtor: int
    polo_climatico: str
    id_laticinio_principal: int
    id_rota_principal: int
    tipo_sistema: str
    nivel_tecnificacao: str
    raca_predominante: str
    vacas_lactacao: int
    producao_media_esperada_litros_dia: float
    capacidade_maxima_litros_dia: float
    distancia_km_laticinio: float
    sensibilidade_seca: float
    sensibilidade_calor: float
    sensibilidade_qualidade: float
    prob_churn_base: float


def gerar_fato_producao(dim_tempo: pd.DataFrame, clima: pd.DataFrame, dim_produtor: pd.DataFrame, dim_rota: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    clima_idx = clima.set_index(["polo_climatico", "data"]).sort_index()
    rota_idx = dim_rota.set_index("id_rota")
    registros_prod = []

    for _, prod in dim_produtor.iterrows():
        p = ProdutorParams(
            id_produtor=int(prod["id_produtor"]),
            polo_climatico=str(prod["polo_climatico"]),
            id_laticinio_principal=int(prod["id_laticinio_principal"]),
            id_rota_principal=int(prod["id_rota_principal"]),
            tipo_sistema=str(prod["tipo_sistema"]),
            nivel_tecnificacao=str(prod["nivel_tecnificacao"]),
            raca_predominante=str(prod["raca_predominante"]),
            vacas_lactacao=int(prod["vacas_lactacao"]),
            producao_media_esperada_litros_dia=float(prod["producao_media_esperada_litros_dia"]),
            capacidade_maxima_litros_dia=float(prod["capacidade_maxima_litros_dia"]),
            distancia_km_laticinio=float(prod["distancia_km_laticinio"]),
            sensibilidade_seca=float(prod["sensibilidade_seca"]),
            sensibilidade_calor=float(prod["sensibilidade_calor"]),
            sensibilidade_qualidade=float(prod["sensibilidade_qualidade"]),
            prob_churn_base=float(prod["prob_churn_base"]),
        )

        base = dim_tempo[["data", "ano", "mes", "dia_do_ano", "estacao_climatica"]].copy()
        clima_p = clima_idx.loc[p.polo_climatico].reset_index()
        df = base.merge(clima_p, on="data", how="left")

        amp_sazonal = {"PASTO": rng.uniform(0.10, 0.22), "SEMI_CONFINADO": rng.uniform(0.06, 0.14), "CONFINADO": rng.uniform(0.02, 0.08)}[p.tipo_sistema]
        fase = rng.uniform(0, 2 * np.pi)
        f_sazonal = 1 + amp_sazonal * np.sin(2 * np.pi * df["dia_do_ano"] / 365.25 + fase)

        chuva_norm = normaliza_serie(df["precip_15d"])
        seca_norm = normaliza_serie(df["dias_sem_chuva"])
        g_chuva = 0.6 * chuva_norm - 0.4 * seca_norm
        if p.tipo_sistema == "PASTO":
            f_chuva = np.clip(1 + (0.11 * p.sensibilidade_seca) * g_chuva, 0.78, 1.15)
        elif p.tipo_sistema == "SEMI_CONFINADO":
            f_chuva = np.clip(1 + (0.06 * p.sensibilidade_seca) * g_chuva, 0.88, 1.08)
        else:
            f_chuva = np.clip(1 + (0.025 * p.sensibilidade_seca) * g_chuva, 0.94, 1.04)

        thi = df["thi"].values
        beta = 0.0045 * p.sensibilidade_calor
        gamma = 0.0075 * p.sensibilidade_calor
        f_calor = np.ones(len(df))
        mask1 = (thi >= 68) & (thi < 78)
        mask2 = thi >= 78
        f_calor[mask1] = 1 - beta * (thi[mask1] - 68)
        f_calor[mask2] = 1 - beta * 10 - gamma * (thi[mask2] - 78)
        f_calor = np.clip(f_calor, 0.72, 1.00)
        f_calor *= np.where(df["onda_calor_5d"].values == 1, 0.97, 1.0)

        score_manejo = {"BAIXO": rng.uniform(0.35, 0.58), "MEDIO": rng.uniform(0.55, 0.78), "ALTO": rng.uniform(0.75, 0.96)}[p.nivel_tecnificacao]
        score_sanidade = np.clip(score_manejo + rng.normal(0, 0.06), 0.25, 0.98)
        f_manejo = 0.90 + 0.09 * score_manejo + 0.05 * score_sanidade

        ruido = np.zeros(len(df))
        eps = rng.normal(0, 0.035 * p.producao_media_esperada_litros_dia, len(df))
        for t in range(1, len(df)):
            ruido[t] = 0.65 * ruido[t - 1] + eps[t]

        litros_previstos = p.producao_media_esperada_litros_dia * f_sazonal * f_chuva * f_calor * f_manejo + ruido

        prob_antibiotico = 0.0008 * p.sensibilidade_qualidade
        prob_reprov_qualidade = 0.0012 * p.sensibilidade_qualidade
        prob_falha_coleta = 0.0010
        prob_mudou_laticinio = p.prob_churn_base

        flag_antibiotico = (rng.random(len(df)) < prob_antibiotico).astype(int)
        flag_qualidade_reprovada = (rng.random(len(df)) < prob_reprov_qualidade).astype(int)

        rota = rota_idx.loc[p.id_rota_principal]
        fator_dificuldade = {"BAIXA": 0.7, "MEDIA": 1.0, "ALTA": 1.5}[rota["dificuldade_logistica"]]
        prob_falha_coleta_t = prob_falha_coleta + 0.00008 * df["precip_mm"].values * fator_dificuldade + 0.0015 * rota["percentual_estrada_nao_pavimentada"]
        flag_falha_coleta = (rng.random(len(df)) < prob_falha_coleta_t).astype(int)
        flag_mudou_laticinio = (rng.random(len(df)) < prob_mudou_laticinio).astype(int)

        litros_previstos = np.clip(litros_previstos, 0, p.capacidade_maxima_litros_dia)
        penal_sanitaria = 1 - (0.18 * flag_antibiotico + 0.10 * flag_qualidade_reprovada)
        litros_produzidos = np.clip(litros_previstos * penal_sanitaria, 0, p.capacidade_maxima_litros_dia)

        coleta_base = rng.uniform(0.965, 0.998, len(df))
        coleta_base -= 0.0010 * df["precip_mm"].values * rota["percentual_estrada_nao_pavimentada"]
        coleta_base -= 0.20 * flag_falha_coleta
        coleta_base -= 0.15 * flag_qualidade_reprovada
        coleta_base = np.clip(coleta_base, 0.0, 1.0)

        litros_coletados = litros_produzidos * coleta_base
        litros_descartados = np.maximum(litros_produzidos - litros_coletados, 0)

        base_ccs = {"BAIXO": rng.uniform(350, 650), "MEDIO": rng.uniform(220, 420), "ALTO": rng.uniform(140, 280)}[p.nivel_tecnificacao]
        base_cbt = {"BAIXO": rng.uniform(80, 220), "MEDIO": rng.uniform(35, 120), "ALTO": rng.uniform(10, 60)}[p.nivel_tecnificacao]

        ccs = base_ccs + 4.5 * np.maximum(df["thi"].values - 72, 0) + 90 * flag_antibiotico + 65 * flag_qualidade_reprovada + rng.normal(0, 25, len(df))
        cbt = base_cbt + 1.2 * df["temp_max_c"].values + 45 * flag_qualidade_reprovada + rng.normal(0, 10, len(df))
        ccs = np.clip(ccs, 80, 2000)
        cbt = np.clip(cbt, 5, 800)

        temp_tanque = np.clip(3.5 + 0.03 * df["temp_max_c"].values + 0.008 * p.distancia_km_laticinio + rng.normal(0, 0.5, len(df)), 2.0, 12.0)
        custo_logistico_rateado = np.clip(0.10 + 0.0045 * p.distancia_km_laticinio + 0.0020 * rota["km_planejado"] + 0.0035 * df["precip_mm"].values * rota["percentual_estrada_nao_pavimentada"], 0.12, 5.00)
        margem_estimada_fornecedor = np.clip(0.62 + 0.0035 * score_manejo * 100 - 0.0016 * custo_logistico_rateado - 0.00035 * ccs - 0.0008 * cbt, -2.00, 2.50)

        prod_df = pd.DataFrame({
            "data": df["data"],
            "id_produtor": p.id_produtor,
            "id_laticinio": p.id_laticinio_principal,
            "id_rota": p.id_rota_principal,
            "polo_climatico": p.polo_climatico,
            "litros_previstos": np.round(litros_previstos, 2),
            "litros_produzidos": np.round(litros_produzidos, 2),
            "litros_coletados": np.round(litros_coletados, 2),
            "litros_descartados": np.round(litros_descartados, 2),
            "ccs": np.round(ccs, 2),
            "cbt": np.round(cbt, 2),
            "temp_tanque_c": np.round(temp_tanque, 2),
            "flag_antibiotico": flag_antibiotico,
            "flag_qualidade_reprovada": flag_qualidade_reprovada,
            "flag_falha_coleta": flag_falha_coleta,
            "flag_mudou_laticinio": flag_mudou_laticinio,
            "score_sanidade": np.round(score_sanidade, 3),
            "score_manejo": np.round(score_manejo, 3),
            "custo_logistico_rateado": np.round(custo_logistico_rateado, 4),
            "margem_estimada_fornecedor": np.round(margem_estimada_fornecedor, 4),
        })
        registros_prod.append(prod_df)

    fact_prod = pd.concat(registros_prod, ignore_index=True).sort_values(["id_produtor", "data"]).reset_index(drop=True)

    fact_prod["media_30d_passada"] = fact_prod.groupby("id_produtor")["litros_coletados"].transform(lambda s: s.rolling(30, min_periods=7).mean())

    def future_mean(series: pd.Series, horizon: int) -> pd.Series:
        arr = series.values
        out = np.full(len(arr), np.nan)
        for i in range(len(arr)):
            j = min(len(arr), i + 1 + horizon)
            if i + 1 < len(arr):
                out[i] = np.mean(arr[i + 1:j])
        return pd.Series(out, index=series.index)

    fact_prod["media_futura_7d"] = fact_prod.groupby("id_produtor")["litros_coletados"].transform(lambda s: future_mean(s, 7))
    fact_prod["media_futura_15d"] = fact_prod.groupby("id_produtor")["litros_coletados"].transform(lambda s: future_mean(s, 15))
    fact_prod["media_futura_30d"] = fact_prod.groupby("id_produtor")["litros_coletados"].transform(lambda s: future_mean(s, 30))

    fact_prod["target_queda_7d"] = (fact_prod["media_futura_7d"] <= fact_prod["media_30d_passada"] * 0.90).astype(int)
    fact_prod["target_queda_15d"] = (fact_prod["media_futura_15d"] <= fact_prod["media_30d_passada"] * 0.90).astype(int)
    fact_prod["target_queda_30d"] = (fact_prod["media_futura_30d"] <= fact_prod["media_30d_passada"] * 0.90).astype(int)
    fact_prod = fact_prod.drop(columns=["media_30d_passada", "media_futura_7d", "media_futura_15d", "media_futura_30d"])

    fact_rota = fact_prod.groupby(["data", "id_rota", "id_laticinio"], as_index=False).agg(
        litros_previstos=("litros_previstos", "sum"),
        litros_realizados=("litros_coletados", "sum"),
        num_produtores_planejados=("id_produtor", "nunique"),
        num_produtores_atendidos=("litros_coletados", lambda s: int((s > 0).sum())),
        custo_total=("custo_logistico_rateado", "sum"),
    )

    fact_rota = fact_rota.merge(dim_rota[["id_rota", "km_planejado", "tempo_medio_horas", "capacidade_tanque_litros", "percentual_estrada_nao_pavimentada", "polo_climatico"]], on="id_rota", how="left")
    fact_rota = fact_rota.merge(clima[["data", "polo_climatico", "precip_mm"]], on=["data", "polo_climatico"], how="left")
    fator_chuva_rota = 1 + 0.0025 * fact_rota["precip_mm"] * fact_rota["percentual_estrada_nao_pavimentada"]
    fact_rota["km_rodados"] = np.round(fact_rota["km_planejado"] * rng.uniform(0.98, 1.08, len(fact_rota)), 2)
    fact_rota["tempo_total_horas"] = np.round(fact_rota["tempo_medio_horas"] * fator_chuva_rota * rng.uniform(0.95, 1.10, len(fact_rota)), 2)
    fact_rota["ocupacao_tanque_pct"] = np.round(100 * fact_rota["litros_realizados"] / fact_rota["capacidade_tanque_litros"].replace(0, np.nan), 2)
    fact_rota["indice_atraso"] = np.round(np.maximum(fact_rota["tempo_total_horas"] / fact_rota["tempo_medio_horas"] - 1, 0), 4)
    fact_rota["indice_perda_rota"] = np.round(np.maximum(fact_rota["litros_previstos"] - fact_rota["litros_realizados"], 0) / fact_rota["litros_previstos"].replace(0, np.nan), 4)
    fact_rota = fact_rota.drop(columns=["km_planejado", "tempo_medio_horas", "capacidade_tanque_litros", "percentual_estrada_nao_pavimentada", "polo_climatico", "precip_mm"])
    return fact_prod, fact_rota


def exportar_csv(df: pd.DataFrame, nome_arquivo: str, pasta: str) -> None:
    df.to_csv(os.path.join(pasta, nome_arquivo), index=False, encoding="utf-8-sig")


def main(output_dir: str, use_real_climate: bool, real_climate_path: str | None) -> None:
    ensure_output_dir(output_dir)
    dim_tempo = gerar_dim_tempo(START_DATE, END_DATE)
    if use_real_climate:
        if not real_climate_path:
            raise SystemExit("--use-real-climate exige --real-climate-path")
        fact_clima_diario = carregar_clima_de_arquivo(Path(real_climate_path), dim_tempo)
    else:
        fact_clima_diario = gerar_clima_diario(dim_tempo)
    dim_laticinio = gerar_dim_laticinio()
    dim_rota = gerar_dim_rota(dim_laticinio)
    dim_produtor = gerar_dim_produtor(dim_rota)
    fact_producao_produtor_dia, fact_rota_dia = gerar_fato_producao(dim_tempo, fact_clima_diario, dim_produtor, dim_rota)

    exportar_csv(dim_laticinio, "dim_laticinio.csv", output_dir)
    exportar_csv(dim_rota, "dim_rota.csv", output_dir)
    exportar_csv(dim_produtor, "dim_produtor.csv", output_dir)
    exportar_csv(dim_tempo, "dim_tempo.csv", output_dir)
    exportar_csv(fact_clima_diario, "fact_clima_diario.csv", output_dir)
    exportar_csv(fact_producao_produtor_dia, "fact_producao_produtor_dia.csv", output_dir)
    exportar_csv(fact_rota_dia, "fact_rota_dia.csv", output_dir)

    print("Concluído.")
    print(f"Arquivos salvos em: {output_dir}")
    print(f"dim_produtor: {dim_produtor.shape}")
    print(f"fact_clima_diario: {fact_clima_diario.shape}")
    print(f"fact_producao_produtor_dia: {fact_producao_produtor_dia.shape}")
    print(f"fact_rota_dia: {fact_rota_dia.shape}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera base sintética de captação de leite.")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="Pasta de saída dos CSVs")
    parser.add_argument("--use-real-climate", action="store_true", help="Usa clima já processado (ex.: INMET)")
    parser.add_argument("--real-climate-path", default=None, help="Caminho para fact_clima_diario_inmet.csv")
    ns = parser.parse_args()
    main(ns.output_dir, ns.use_real_climate, ns.real_climate_path)
