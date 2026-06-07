from __future__ import annotations

from .schemas import IoTAlert, IoTReading


def calcular_thi(temperatura_c: float, umidade_percentual: float) -> float:
    thi = (1.8 * temperatura_c + 32) - ((0.55 - 0.0055 * umidade_percentual) * (1.8 * temperatura_c - 26))
    return round(thi, 1)


def classificar_nivel_tanque(temperatura_c: float) -> str:
    if temperatura_c <= 4.0:
        return "IDEAL"
    if temperatura_c <= 7.0:
        return "ATENCAO"
    return "RISCO"


def classificar_thi(thi: float) -> str:
    if thi <= 68:
        return "BAIXO"
    if thi <= 74:
        return "MODERADO"
    if thi <= 78:
        return "ALTO"
    return "CRITICO"


def classificar_volume_tanque(volume_litros: float, capacidade_litros: float) -> str:
    if capacidade_litros <= 0:
        return "NORMAL"
    ocupacao_pct = volume_litros / capacidade_litros * 100
    if ocupacao_pct <= 50:
        return "NORMAL"
    if ocupacao_pct <= 80:
        return "ATENCAO"
    return "PRIORIDADE_COLETA"


def classificar_risco_qualidade_leite(temperatura_tanque_c: float, volume_litros: float, capacidade_litros: float) -> str:
    classe_temp = classificar_nivel_tanque(temperatura_tanque_c)
    classe_volume = classificar_volume_tanque(volume_litros, capacidade_litros)
    if classe_temp == "RISCO":
        return "ALTO"
    if classe_temp == "ATENCAO" or classe_volume == "PRIORIDADE_COLETA":
        return "MEDIO"
    return "BAIXO"


def classificar_risco_termico(thi: float) -> str:
    classe = classificar_thi(thi)
    if classe == "MODERADO":
        return "MEDIO"
    return classe


def classificar_prioridade_coleta(volume_litros: float, capacidade_litros: float, risco_qualidade: str, risco_termico: str) -> str:
    classe_volume = classificar_volume_tanque(volume_litros, capacidade_litros)
    if classe_volume == "PRIORIDADE_COLETA" or risco_qualidade == "ALTO" or risco_termico == "CRITICO":
        return "ALTA"
    if classe_volume == "ATENCAO" or risco_qualidade == "MEDIO" or risco_termico in {"ALTO", "MEDIO"}:
        return "MEDIA"
    return "BAIXA"


def gerar_alertas(leitura: IoTReading) -> list[IoTAlert]:
    alertas: list[IoTAlert] = []

    def adicionar_alerta(codigo: str, severidade: str, mensagem: str, acao: str) -> None:
        alertas.append(
            IoTAlert(
                id=f"{leitura.farm_id}-{codigo}",
                farm_id=leitura.farm_id,
                severity=severidade,
                message=mensagem,
                created_at=leitura.timestamp,
                recommended_action=acao,
                source=leitura.reading_source,
            )
        )

    if leitura.tank_temperature_c > 7.0:
        adicionar_alerta(
            "TEMP",
            "ALTA",
            "Temperatura do tanque acima do recomendado",
            "Priorizar avaliacao do sistema de resfriamento e antecipar a coleta.",
        )
    elif leitura.tank_temperature_c > 4.0:
        adicionar_alerta(
            "TEMP",
            "MEDIA",
            "Temperatura do tanque em faixa de atencao",
            "Acompanhar estabilidade do resfriamento e revisar janela de coleta.",
        )

    if leitura.thermal_stress_risk == "CRITICO":
        adicionar_alerta(
            "THI",
            "ALTA",
            "Risco critico de estresse termico",
            "Aumentar ventilacao, hidratacao e acompanhar impacto produtivo nas proximas horas.",
        )
    elif leitura.thermal_stress_risk == "ALTO":
        adicionar_alerta(
            "THI",
            "MEDIA",
            "Risco elevado de estresse termico",
            "Monitorar conforto animal e considerar ajustes operacionais preventivos.",
        )

    if classificar_volume_tanque(leitura.milk_volume_liters, leitura.tank_capacity_liters) == "PRIORIDADE_COLETA":
        adicionar_alerta(
            "VOL",
            "ALTA",
            "Tanque proximo da capacidade maxima",
            "Reprogramar coleta para evitar transbordo e perda operacional.",
        )

    if leitura.collection_priority == "ALTA":
        adicionar_alerta(
            "COL",
            "ALTA",
            "Prioridade de coleta elevada",
            "Posicionar a fazenda entre as primeiras rotas e confirmar disponibilidade logistica.",
        )

    if leitura.milk_quality_risk in {"MEDIO", "ALTO"}:
        adicionar_alerta(
            "QUAL",
            "ALTA" if leitura.milk_quality_risk == "ALTO" else "MEDIA",
            "Risco de perda de qualidade do leite",
            "Revisar temperatura, tempo de permanencia no tanque e condicoes de coleta.",
        )

    return alertas
