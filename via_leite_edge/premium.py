from __future__ import annotations

from .schemas import IoTReading


def _clamp(valor: float, minimo: float = 0.0, maximo: float = 100.0) -> float:
    return max(minimo, min(maximo, valor))


def score_estabilidade_termica(tank_temperature_c: float, ambient_temperature_c: float, thi: float) -> float:
    penalidade_tanque = abs(tank_temperature_c - 4.0) * 11.5
    penalidade_ambiente = max(0.0, ambient_temperature_c - 24.0) * 1.2
    penalidade_thi = max(0.0, thi - 68.0) * 1.1
    return round(_clamp(100.0 - penalidade_tanque - penalidade_ambiente - penalidade_thi), 1)


def score_conservacao(tank_temperature_c: float, volume_pct: float) -> float:
    penalidade_tanque = max(0.0, tank_temperature_c - 4.0) * 13.0
    penalidade_ocupacao = max(0.0, volume_pct - 75.0) * 0.9
    bonus_ocupacao = max(0.0, 55.0 - volume_pct) * 0.08
    return round(_clamp(86.0 - penalidade_tanque - penalidade_ocupacao + bonus_ocupacao), 1)


def score_risco_operacional(collection_priority: str, milk_quality_risk: str, thermal_stress_risk: str) -> float:
    prioridade = {"BAIXA": 18.0, "MEDIA": 49.0, "ALTA": 82.0}.get(collection_priority, 45.0)
    qualidade = {"BAIXO": 18.0, "MEDIO": 56.0, "ALTO": 88.0}.get(milk_quality_risk, 45.0)
    termico = {"BAIXO": 12.0, "MEDIO": 44.0, "ALTO": 72.0, "CRITICO": 95.0}.get(thermal_stress_risk, 42.0)
    return round(_clamp(prioridade * 0.35 + qualidade * 0.35 + termico * 0.30), 1)


def score_qualidade_premium(
    tank_temperature_c: float,
    milk_quality_risk: str,
    thermal_stress_risk: str,
    volume_pct: float,
) -> float:
    conservacao = score_conservacao(tank_temperature_c, volume_pct)
    penalidade_qualidade = {"BAIXO": 4.0, "MEDIO": 18.0, "ALTO": 34.0}.get(milk_quality_risk, 16.0)
    penalidade_termica = {"BAIXO": 3.0, "MEDIO": 12.0, "ALTO": 22.0, "CRITICO": 32.0}.get(thermal_stress_risk, 10.0)
    return round(_clamp(conservacao + 18.0 - penalidade_qualidade - penalidade_termica), 1)


def classificar_adequacao_premium(score_qualidade: float, score_conservacao_valor: float, risco_operacional: float) -> str:
    if score_qualidade >= 80 and score_conservacao_valor >= 78 and risco_operacional <= 38:
        return "ALTA"
    if score_qualidade >= 65 and score_conservacao_valor >= 62 and risco_operacional <= 58:
        return "MODERADA"
    return "LIMITADA"


def mensagem_premium(adequacao: str) -> str:
    if adequacao == "ALTA":
        return "Leite apto para cadeia premium"
    if adequacao == "MODERADA":
        return "Leite monitorado com potencial para derivados premium"
    return "Qualidade do leite impactada pela temperatura"


def resumo_premium(leitura: IoTReading) -> dict[str, float | str]:
    volume_pct = (leitura.milk_volume_liters / leitura.tank_capacity_liters * 100.0) if leitura.tank_capacity_liters else 0.0
    estabilidade = score_estabilidade_termica(leitura.tank_temperature_c, leitura.ambient_temperature_c, leitura.thi)
    conservacao = score_conservacao(leitura.tank_temperature_c, volume_pct)
    risco_operacional = score_risco_operacional(
        leitura.collection_priority,
        leitura.milk_quality_risk,
        leitura.thermal_stress_risk,
    )
    qualidade_premium = score_qualidade_premium(
        leitura.tank_temperature_c,
        leitura.milk_quality_risk,
        leitura.thermal_stress_risk,
        volume_pct,
    )
    adequacao = classificar_adequacao_premium(qualidade_premium, conservacao, risco_operacional)
    return {
        "volume_pct": round(volume_pct, 1),
        "premium_quality_score": qualidade_premium,
        "thermal_stability_score": estabilidade,
        "operational_risk_score": risco_operacional,
        "conservation_index": conservacao,
        "premium_suitability": adequacao,
        "premium_message": mensagem_premium(adequacao),
    }
