from __future__ import annotations

from abc import ABC, abstractmethod

from .alerts import gerar_alertas
from .config import EdgeSettings, carregar_configuracao_edge
from .schemas import IoTAlert, IoTReading
from .simulator import gerar_leituras_simuladas


class IoTProvider(ABC):
    @abstractmethod
    def get_latest_readings(self) -> list[IoTReading]:
        raise NotImplementedError

    def get_latest_for_farm(self, farm_id: str) -> IoTReading | None:
        for leitura in self.get_latest_readings():
            if leitura.farm_id == farm_id:
                return leitura
        return None

    def get_active_alerts(self) -> list[IoTAlert]:
        alertas: list[IoTAlert] = []
        for leitura in self.get_latest_readings():
            alertas.extend(gerar_alertas(leitura))
        ordem = {"ALTA": 0, "MEDIA": 1, "BAIXA": 2}
        return sorted(alertas, key=lambda item: (ordem.get(item.severity, 9), item.farm_id, item.id))


class SimulatedIoTProvider(IoTProvider):
    def __init__(self, settings: EdgeSettings | None = None) -> None:
        self.settings = settings or carregar_configuracao_edge()

    def get_latest_readings(self) -> list[IoTReading]:
        return gerar_leituras_simuladas(self.settings.data_dir, limite=self.settings.sample_size)


class RealIoTProvider(IoTProvider):
    def get_latest_readings(self) -> list[IoTReading]:
        raise NotImplementedError("RealIoTProvider ainda nao possui integracao com sensores reais.")


def obter_provider_iot(settings: EdgeSettings | None = None) -> IoTProvider:
    settings = settings or carregar_configuracao_edge()
    if settings.simulation_mode or settings.provider_name == "simulated":
        return SimulatedIoTProvider(settings)
    if settings.provider_name == "real":
        return RealIoTProvider()
    return SimulatedIoTProvider(settings)
