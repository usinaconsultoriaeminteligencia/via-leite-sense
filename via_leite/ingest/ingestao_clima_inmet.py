from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

RAW_DIR = Path("dados_inmet_raw")
OUT_DIR = Path("dados_inmet_processado")

# Mapeamento operacional do projeto
ESTACOES_POLO = {
    "RIO_VERDE": {"codigo": "A025", "nome": "RIO VERDE"},
    "JATAI": {"codigo": "A016", "nome": "JATAI"},
    # Mineiros e sudeste podem variar conforme disponibilidade do usuário
    "MINEIROS": {"codigo": None, "nome": "MINEIROS"},
    "SUDESTE_SUL_GOIANO": {"codigo": None, "nome": "SUDESTE_SUL_GOIANO"},
}

COL_MAP = {
    "Data Medicao": "data",
    "DATA (YYYY-MM-DD)": "data",
    "DATA": "data",
    "Hora Medicao": "hora",
    "HORA (UTC)": "hora",
    "HORA UTC": "hora",
    "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)": "precip_mm",
    "PRECIPITACAO TOTAL, HORARIO(mm)": "precip_mm",
    "TEMPERATURA DO AR - BULBO SECO, HORARIA(°C)": "temp_med_c",
    "TEMPERATURA DO AR - BULBO SECO, HORARIA(C)": "temp_med_c",
    "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)": "temp_max_c",
    "TEMPERATURA MAXIMA NA HORA ANT. (AUT) (C)": "temp_max_c",
    "TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)": "temp_min_c",
    "TEMPERATURA MINIMA NA HORA ANT. (AUT) (C)": "temp_min_c",
    "UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)": "umid_max",
    "UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)": "umid_min",
    "UMIDADE RELATIVA DO AR, HORARIA (%)": "umidade_med_pct",
    "VENTO, VELOCIDADE HORARIA (m/s)": "vento_med_ms",
    "RADIACAO GLOBAL (Kj/m²)": "radiacao_proxy",
}


def garantir_pasta(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)



def ler_csv_inmet(path: Path) -> pd.DataFrame:
    encodings = ["utf-8", "latin-1", "cp1252"]
    last_err = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, sep=";", encoding=enc, skiprows=8)
            return df
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Falha ao ler {path.name}: {last_err}")



def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c: COL_MAP.get(c.strip(), c.strip()) for c in df.columns}
    df = df.rename(columns=cols)
    for col in ["precip_mm", "temp_med_c", "temp_max_c", "temp_min_c", "umid_max", "umid_min", "umidade_med_pct", "vento_med_ms", "radiacao_proxy"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .replace(["", "nan", "None", "/////", "-9999"], np.nan)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df



def agregar_diario(df: pd.DataFrame, polo: str, codigo_estacao: str | None, nome_arquivo: str) -> pd.DataFrame:
    cols_presentes = set(df.columns)
    if "data" not in cols_presentes:
        raise ValueError(f"Arquivo {nome_arquivo} não contém coluna de data reconhecida.")

    work = df.copy()
    if "umidade_med_pct" not in work.columns:
        if "umid_max" in work.columns and "umid_min" in work.columns:
            work["umidade_med_pct"] = work[["umid_max", "umid_min"]].mean(axis=1)

    aggs = {}
    for col in ["precip_mm", "temp_med_c", "temp_max_c", "temp_min_c", "umidade_med_pct", "vento_med_ms", "radiacao_proxy"]:
        if col in work.columns:
            if col == "precip_mm":
                aggs[col] = "sum"
            elif col == "temp_max_c":
                aggs[col] = "max"
            elif col == "temp_min_c":
                aggs[col] = "min"
            else:
                aggs[col] = "mean"

    diario = work.groupby("data", as_index=False).agg(aggs)
    diario["polo_climatico"] = polo
    diario["codigo_estacao"] = codigo_estacao
    diario["arquivo_origem"] = nome_arquivo
    return diario



def calc_thi(temp_c: pd.Series, umidade_pct: pd.Series) -> pd.Series:
    return (1.8 * temp_c + 32) - ((0.55 - 0.0055 * umidade_pct) * (1.8 * temp_c - 26))



def enriquecer_clima(df: pd.DataFrame) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for polo, sub in df.groupby("polo_climatico", sort=False):
        sub = sub.sort_values("data").copy()
        # interpolação conservadora
        for col in ["temp_med_c", "temp_max_c", "temp_min_c", "umidade_med_pct", "vento_med_ms", "radiacao_proxy"]:
            if col in sub.columns:
                sub[col] = sub[col].interpolate(limit_direction="both")
        if "precip_mm" in sub.columns:
            sub["precip_mm"] = sub["precip_mm"].fillna(0)

        # fallback interno entre temperaturas
        if "temp_med_c" in sub.columns:
            if "temp_max_c" not in sub.columns:
                sub["temp_max_c"] = sub["temp_med_c"] + 4
            if "temp_min_c" not in sub.columns:
                sub["temp_min_c"] = sub["temp_med_c"] - 4
        if "temp_med_c" not in sub.columns and {"temp_max_c", "temp_min_c"}.issubset(sub.columns):
            sub["temp_med_c"] = sub[["temp_max_c", "temp_min_c"]].mean(axis=1)

        # completar faixa diária contínua
        full_dates = pd.date_range(sub["data"].min(), sub["data"].max(), freq="D")
        sub = sub.set_index("data").reindex(full_dates).rename_axis("data").reset_index()
        sub["polo_climatico"] = sub["polo_climatico"].ffill().bfill().fillna(polo)
        sub["codigo_estacao"] = sub["codigo_estacao"].ffill().bfill()
        sub["arquivo_origem"] = sub["arquivo_origem"].ffill().bfill()
        for col in ["temp_med_c", "temp_max_c", "temp_min_c", "umidade_med_pct", "vento_med_ms", "radiacao_proxy"]:
            if col in sub.columns:
                sub[col] = sub[col].interpolate(limit_direction="both")
        if "precip_mm" in sub.columns:
            sub["precip_mm"] = sub["precip_mm"].fillna(0)

        sub["precip_3d"] = sub["precip_mm"].rolling(3, min_periods=1).sum()
        sub["precip_7d"] = sub["precip_mm"].rolling(7, min_periods=1).sum()
        sub["precip_15d"] = sub["precip_mm"].rolling(15, min_periods=1).sum()

        dias_sem_chuva = []
        contador = 0
        for p in sub["precip_mm"].fillna(0).values:
            contador = contador + 1 if p < 1.0 else 0
            dias_sem_chuva.append(contador)
        sub["dias_sem_chuva"] = dias_sem_chuva

        sub["thi"] = calc_thi(sub["temp_med_c"], sub["umidade_med_pct"])
        sub["thi_3d_avg"] = sub["thi"].rolling(3, min_periods=1).mean()
        sub["onda_calor_3d"] = (sub["thi_3d_avg"] >= 74).astype(int)
        sub["onda_calor_5d"] = (sub["thi"].rolling(5, min_periods=1).mean() >= 74).astype(int)
        sub["dry_spell_10d"] = (sub["dias_sem_chuva"] >= 10).astype(int)

        media_mensal = sub.groupby(sub["data"].dt.month)["temp_med_c"].transform("mean")
        sub["anomalia_temp"] = sub["temp_med_c"] - media_mensal

        fav = 0.015 * sub["precip_15d"] - 0.025 * sub["dias_sem_chuva"] - 0.020 * np.maximum(sub["thi"] - 72, 0)
        sub["indice_favorabilidade_pastagem"] = np.clip(1 + fav, 0.4, 1.3)
        frames.append(sub)

    out = pd.concat(frames, ignore_index=True)
    return out.sort_values(["polo_climatico", "data"]).reset_index(drop=True)



def inferir_polo_por_nome(nome_arquivo: str) -> str | None:
    upper = nome_arquivo.upper()
    for polo, meta in ESTACOES_POLO.items():
        if meta["codigo"] and meta["codigo"] in upper:
            return polo
        if meta["nome"] and meta["nome"] in upper:
            return polo
    return None



def processar_pasta(raw_dir: Path, out_dir: Path) -> pd.DataFrame:
    garantir_pasta(out_dir)
    arquivos = sorted(raw_dir.glob("*.csv"))
    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {raw_dir}. Baixe os arquivos históricos/automáticos do INMET e coloque nessa pasta."
        )

    diarios: List[pd.DataFrame] = []
    manifest = []
    for path in arquivos:
        polo = inferir_polo_por_nome(path.name)
        if polo is None:
            continue
        raw = ler_csv_inmet(path)
        raw = padronizar_colunas(raw)
        diario = agregar_diario(raw, polo, ESTACOES_POLO[polo]["codigo"], path.name)
        diarios.append(diario)
        manifest.append({
            "arquivo": path.name,
            "polo": polo,
            "codigo_estacao": ESTACOES_POLO[polo]["codigo"],
            "linhas_diarias": int(len(diario)),
            "data_min": str(diario["data"].min().date()) if len(diario) else None,
            "data_max": str(diario["data"].max().date()) if len(diario) else None,
        })

    if not diarios:
        raise RuntimeError(
            "Os arquivos foram encontrados, mas nenhum correspondeu aos polos configurados. Renomeie os arquivos incluindo A025, JATAI, RIO_VERDE etc."
        )

    clima = pd.concat(diarios, ignore_index=True)
    clima = enriquecer_clima(clima)
    clima.to_csv(out_dir / "fact_clima_diario_inmet.csv", index=False, encoding="utf-8-sig")
    with open(out_dir / "manifesto_inmet.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return clima



def main() -> None:
    parser = argparse.ArgumentParser(description="Processa arquivos do INMET e gera clima diário padronizado para o MVP de captação de leite.")
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    clima = processar_pasta(args.raw_dir, args.out_dir)
    print(f"Arquivo gerado: {(args.out_dir / 'fact_clima_diario_inmet.csv').resolve()}")
    print("Polos disponíveis:", sorted(clima['polo_climatico'].dropna().unique().tolist()))
    print("Período:", clima['data'].min(), "até", clima['data'].max())
    print("Linhas:", len(clima))


if __name__ == "__main__":
    main()
