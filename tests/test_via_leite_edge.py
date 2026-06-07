from __future__ import annotations

import unittest
import uuid
from pathlib import Path

from via_leite_edge.alerts import (
    calcular_thi,
    classificar_nivel_tanque,
    classificar_thi,
    classificar_volume_tanque,
    gerar_alertas,
)
from via_leite_edge.config import EdgeSettings
from via_leite_edge.providers import SimulatedIoTProvider
from via_leite_edge.premium import classificar_adequacao_premium, resumo_premium
from via_leite_edge.schemas import IoTReading


class ViaLeiteEdgeTests(unittest.TestCase):
    def test_calculo_e_classificacao_thi(self) -> None:
        thi_baixo = calcular_thi(20.0, 50.0)
        thi_critico = calcular_thi(35.0, 70.0)
        self.assertLessEqual(thi_baixo, 68)
        self.assertEqual(classificar_thi(thi_baixo), "BAIXO")
        self.assertGreater(thi_critico, 78)
        self.assertEqual(classificar_thi(thi_critico), "CRITICO")

    def test_classificacao_temperatura_tanque(self) -> None:
        self.assertEqual(classificar_nivel_tanque(4.0), "IDEAL")
        self.assertEqual(classificar_nivel_tanque(4.1), "ATENCAO")
        self.assertEqual(classificar_nivel_tanque(7.0), "ATENCAO")
        self.assertEqual(classificar_nivel_tanque(7.1), "RISCO")

    def test_classificacao_volume_tanque(self) -> None:
        self.assertEqual(classificar_volume_tanque(500, 1000), "NORMAL")
        self.assertEqual(classificar_volume_tanque(700, 1000), "ATENCAO")
        self.assertEqual(classificar_volume_tanque(900, 1000), "PRIORIDADE_COLETA")

    def test_geracao_de_alertas(self) -> None:
        leitura = IoTReading(
            sensor_id="TANK-FZ001",
            farm_id="FZ001",
            farm_name="Fazenda Modelo",
            timestamp="2026-03-01T14:00:00",
            tank_temperature_c=8.1,
            milk_volume_liters=910.0,
            tank_capacity_liters=1000.0,
            ambient_temperature_c=35.0,
            humidity_percent=70.0,
            thi=82.4,
            milk_quality_risk="ALTO",
            thermal_stress_risk="CRITICO",
            collection_priority="ALTA",
            gps_lat=-16.6869,
            gps_lng=-49.2648,
            reading_source="SIMULATED",
        )
        mensagens = {alerta.message for alerta in gerar_alertas(leitura)}
        self.assertIn("Temperatura do tanque acima do recomendado", mensagens)
        self.assertIn("Risco critico de estresse termico", mensagens)
        self.assertIn("Tanque proximo da capacidade maxima", mensagens)
        self.assertIn("Prioridade de coleta elevada", mensagens)
        self.assertIn("Risco de perda de qualidade do leite", mensagens)

    def test_provider_simulado_retorna_leituras(self) -> None:
        data_dir = Path(__file__).resolve().parent / f"_tmp_via_leite_edge_{uuid.uuid4().hex}"
        data_dir.mkdir(parents=True, exist_ok=True)
        try:
            data_dir.joinpath("dim_produtor.csv").write_text(
                "\n".join(
                    [
                        "id_produtor,nome_ficticio,municipio,capacidade_maxima_litros_dia,ativo",
                        "1,PRODUTOR_00001,Rio Verde,1000,1",
                        "2,PRODUTOR_00002,Jatai,800,1",
                    ]
                ),
                encoding="utf-8",
            )
            provider = SimulatedIoTProvider(
                EdgeSettings(
                    simulation_mode=True,
                    provider_name="simulated",
                    sample_size=2,
                    data_dir=data_dir,
                )
            )
            leituras = provider.get_latest_readings()
            self.assertEqual(len(leituras), 2)
            self.assertTrue(all(leitura.reading_source == "SIMULATED" for leitura in leituras))
            self.assertTrue(all(leitura.collection_priority in {"BAIXA", "MEDIA", "ALTA"} for leitura in leituras))
        finally:
            csv_path = data_dir / "dim_produtor.csv"
            if csv_path.exists():
                csv_path.unlink()
            if data_dir.exists():
                data_dir.rmdir()

    def test_resumo_premium(self) -> None:
        leitura = IoTReading(
            sensor_id="TANK-FZ099",
            farm_id="FZ099",
            farm_name="Fazenda Premium",
            timestamp="2026-03-01T14:00:00",
            tank_temperature_c=3.9,
            milk_volume_liters=620.0,
            tank_capacity_liters=1000.0,
            ambient_temperature_c=24.0,
            humidity_percent=58.0,
            thi=67.0,
            milk_quality_risk="BAIXO",
            thermal_stress_risk="BAIXO",
            collection_priority="BAIXA",
            gps_lat=-16.0,
            gps_lng=-49.0,
            reading_source="SIMULATED",
        )
        resumo = resumo_premium(leitura)
        self.assertGreaterEqual(float(resumo["premium_quality_score"]), 70.0)
        self.assertIn(resumo["premium_suitability"], {"ALTA", "MODERADA", "LIMITADA"})
        self.assertTrue(str(resumo["premium_message"]))

    def test_classificacao_adequacao_premium(self) -> None:
        self.assertEqual(classificar_adequacao_premium(86, 82, 30), "ALTA")
        self.assertEqual(classificar_adequacao_premium(70, 68, 44), "MODERADA")
        self.assertEqual(classificar_adequacao_premium(55, 50, 70), "LIMITADA")


if __name__ == "__main__":
    unittest.main()
