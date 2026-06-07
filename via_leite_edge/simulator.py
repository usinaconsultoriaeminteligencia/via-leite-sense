from __future__ import annotations

import hashlib
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from .alerts import (
    calcular_thi,
    classificar_prioridade_coleta,
    classificar_risco_qualidade_leite,
    classificar_risco_termico,
)
from .schemas import IoTReading


FALLBACK_FARMS = [
    {"farm_id": "FZ001", "farm_name": "Fazenda Modelo", "municipio": "Jatai", "capacidade_base": 1000.0},
    {"farm_id": "FZ002", "farm_name": "Sitio Bela Vista", "municipio": "Rio Verde", "capacidade_base": 850.0},
    {"farm_id": "FZ003", "farm_name": "Agropecuaria Santa Rita", "municipio": "Mineiros", "capacidade_base": 1400.0},
]


def _seed(*partes: object) -> int:
    texto = "|".join(str(parte) for parte in partes)
    digest = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def _noise(seed: int, minimo: float, maximo: float) -> float:
    proporcao = (seed % 10_000) / 10_000
    return minimo + (maximo - minimo) * proporcao


def _carregar_catalogo_fazendas(data_dir: Path, limite: int) -> list[dict]:
    caminho = data_dir / "dim_produtor.csv"
    if not caminho.exists():
        return FALLBACK_FARMS[:limite]

    dim = pd.read_csv(caminho)
    if dim.empty:
        return FALLBACK_FARMS[:limite]

    serie_ativos = dim["ativo"].fillna(1) if "ativo" in dim.columns else pd.Series([1] * len(dim), index=dim.index)
    ativos = dim[serie_ativos == 1].copy()
    ativos = ativos.head(limite)
    farms: list[dict] = []
    for _, row in ativos.iterrows():
        produtor_id = int(row.get("id_produtor", len(farms) + 1))
        capacidade = float(
            row.get("capacidade_maxima_litros_dia")
            or row.get("producao_media_esperada_litros_dia")
            or 900.0
        )
        farms.append(
            {
                "farm_id": f"FZ{produtor_id:03d}",
                "farm_name": str(row.get("nome_ficticio") or f"Produtor {produtor_id}"),
                "municipio": str(row.get("municipio") or "Polo Leiteiro"),
                "capacidade_base": round(max(600.0, capacidade * 1.1), 2),
            }
        )
    return farms or FALLBACK_FARMS[:limite]


def gerar_leitura_simulada(farm: dict, timestamp: datetime | None = None) -> IoTReading:
    referencia = timestamp or datetime.now().replace(microsecond=0)
    janela = referencia.strftime("%Y%m%d%H")
    base_seed = _seed(farm["farm_id"], janela)

    ambient_temperature_c = round(_noise(base_seed + 11, 21.0, 38.0), 1)
    humidity_percent = round(_noise(base_seed + 17, 38.0, 85.0), 1)
    thi = calcular_thi(ambient_temperature_c, humidity_percent)

    tank_capacity_liters = round(float(farm.get("capacidade_base", 1000.0)), 1)
    occupancy_ratio = _noise(base_seed + 23, 0.32, 0.96)
    milk_volume_liters = round(tank_capacity_liters * occupancy_ratio, 1)

    temp_component = 2.2 + ((ambient_temperature_c - 20.0) * 0.09) + ((occupancy_ratio - 0.5) * 2.6)
    oscillation = math.sin((_seed(farm["farm_id"], referencia.date()) % 360) * math.pi / 180) * 0.8
    tank_temperature_c = round(max(2.4, min(9.8, temp_component + oscillation)), 1)

    milk_quality_risk = classificar_risco_qualidade_leite(
        temperatura_tanque_c=tank_temperature_c,
        volume_litros=milk_volume_liters,
        capacidade_litros=tank_capacity_liters,
    )
    thermal_stress_risk = classificar_risco_termico(thi)
    collection_priority = classificar_prioridade_coleta(
        volume_litros=milk_volume_liters,
        capacidade_litros=tank_capacity_liters,
        risco_qualidade=milk_quality_risk,
        risco_termico=thermal_stress_risk,
    )

    gps_lat = round(-18.2 + _noise(base_seed + 31, 0.0, 2.1), 6)
    gps_lng = round(-53.3 + _noise(base_seed + 37, 0.0, 4.4), 6)

    return IoTReading(
        sensor_id=f"TANK-{farm['farm_id']}",
        farm_id=farm["farm_id"],
        farm_name=farm["farm_name"],
        timestamp=referencia.isoformat(),
        tank_temperature_c=tank_temperature_c,
        milk_volume_liters=milk_volume_liters,
        tank_capacity_liters=tank_capacity_liters,
        ambient_temperature_c=ambient_temperature_c,
        humidity_percent=humidity_percent,
        thi=thi,
        milk_quality_risk=milk_quality_risk,
        thermal_stress_risk=thermal_stress_risk,
        collection_priority=collection_priority,
        gps_lat=gps_lat,
        gps_lng=gps_lng,
        reading_source="SIMULATED",
    )


def gerar_leituras_simuladas(data_dir: Path, limite: int = 12, timestamp: datetime | None = None) -> list[IoTReading]:
    fazendas = _carregar_catalogo_fazendas(data_dir, limite)
    return [gerar_leitura_simulada(farm, timestamp=timestamp) for farm in fazendas]
