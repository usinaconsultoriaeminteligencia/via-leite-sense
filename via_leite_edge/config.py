from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

EDGE_MODULE_NAME = "VIA_LEITE_EDGE"
EDGE_SOURCE_NAME = "SIMULATED_IOT_DATA"
EDGE_DISCLAIMER = "Dados simulados para validacao de arquitetura e demonstracao de conceito."


def _ler_bool_env(nome: str, padrao: bool) -> bool:
    valor = os.environ.get(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


@dataclass(frozen=True)
class EdgeSettings:
    simulation_mode: bool = True
    provider_name: str = "simulated"
    sample_size: int = 12
    data_dir: Path = Path("dados_teste")
    source_name: str = EDGE_SOURCE_NAME
    disclaimer: str = EDGE_DISCLAIMER


def carregar_configuracao_edge() -> EdgeSettings:
    simulation_mode = _ler_bool_env("IOT_SIMULATION_MODE", True)
    provider_name = os.environ.get("IOT_PROVIDER", "simulated").strip().lower() or "simulated"
    sample_size_raw = os.environ.get("IOT_SIMULATION_SAMPLE_SIZE", "12").strip()
    try:
        sample_size = max(1, int(sample_size_raw))
    except ValueError:
        sample_size = 12
    data_dir = Path(os.environ.get("MVP_DATA_DIR", "dados_teste"))
    return EdgeSettings(
        simulation_mode=simulation_mode,
        provider_name=provider_name,
        sample_size=sample_size,
        data_dir=data_dir,
    )
