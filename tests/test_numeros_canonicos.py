"""
Os números do modelo citados nos documentos têm de ser os do artefato.

Entre 06/08 e 20/10/2026 os documentos do PI citaram MAE 24,45 / ganho 22,5 %,
número de antes do achado A2, enquanto o artefato já dizia 24,17. Ninguém foi
avisado. Este teste falha quando o modelo é retreinado e os documentos não
acompanham — a correção é atualizar o documento, não o teste.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

METRICAS = Path("artefatos_teste/metricas_modelo.json")

# Documento -> trecho que tem de conter o número vigente.
DOCUMENTOS = {
    Path("docs/ESTADO_REAL.md"): "| **{mae}** | **{ganho}%** |",
    Path("docs/projeto_integrador/artigo.md"): "| MAE teste (XGBoost) | **{mae} L** |",
}


def _br(valor: float, casas: int) -> str:
    return f"{valor:.{casas}f}".replace(".", ",")


@pytest.fixture(scope="module")
def vigente() -> dict[str, str]:
    m = json.loads(METRICAS.read_text(encoding="utf-8"))
    mae = m["metricas_teste_modelo"]["mae"]
    base = m["metricas_teste_baseline"]["mae"]
    return {"mae": _br(mae, 2), "ganho": _br((1 - mae / base) * 100, 1)}


@pytest.mark.parametrize("doc", list(DOCUMENTOS), ids=str)
def test_documento_cita_o_mae_do_artefato(doc, vigente):
    esperado = DOCUMENTOS[doc].format(**vigente)
    assert esperado in doc.read_text(encoding="utf-8"), (
        f"{doc} não cita o número vigente do modelo ({esperado!r}). "
        f"O artefato {METRICAS} diz MAE {vigente['mae']} e ganho {vigente['ganho']}%."
    )
