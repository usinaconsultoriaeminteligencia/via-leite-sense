"""
Testes da guarda de ingestão (achado C1, opção 3).

A guarda existe para responder a uma pergunta com consequência: importar ou
não. Por isso o que aqui se testa não é só "a conta está certa" — é que a
guarda **separa casos que se parecem uns com os outros e pedem correcções
opostas**:

    dimensão morta       -> o limiar não bate na distribuição   (recalibrar)
    dimensão não medida  -> a coluna não veio no lote            (pedir ao cliente)
    escala trocada       -> unidade divergente entre dado/limiar (corrigir C1)

Os três produzem `target_*` idênticos — tudo a zero — e foi essa confusão que
manteve C1 invisível.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from via_leite.ingest.guarda_ingestao import (
    MORTA,
    NAO_MEDIDA,
    OK,
    SATURADA,
    avaliar_lote,
    conferir_escala,
    dimensoes_medidas,
    formatar_relatorio,
    taxa_de_disparo,
)
from via_leite.core.score_risco import PESOS_SCORE, calcular_scores


def lote_saudavel(n: int = 100) -> pd.DataFrame:
    """Um lote em que as 7 dimensões disparam, mas nenhuma satura.

    Construído por índice, não por sorteio: uma guarda que decide importações
    não pode ter o seu próprio teste a oscilar com a semente.
    """
    idx = np.arange(n)
    litros = np.where(idx % 4 == 0, 200.0, 400.0)
    return pd.DataFrame({
        "id_produtor":        [f"P{i % 5:03d}" for i in idx],
        "litros_coletados":   litros,
        # Ordem de grandeza coerente com LIMIAR (cel/mL e UFC/mL).
        "ccs":                np.where(idx % 2 == 0, 700_000.0, 250_000.0),
        "cbt":                np.where(idx % 2 == 0, 150_000.0, 60_000.0),
        "temp_tanque_c":      np.where(idx % 3 == 0, 5.0, 3.5),
        "litros_descartados": np.where(idx % 5 == 0, litros * 0.10, 0.0),
    })


# ------------------------------------------------------------------ #
# taxa_de_disparo                                                      #
# ------------------------------------------------------------------ #

def test_taxa_de_disparo_conta_o_que_deve():
    df = pd.DataFrame({
        "target_risco_ccs": [0, 0, 0, 0],
        "target_risco_cbt": [1, 1, 1, 1],
        "target_risco_queda_producao": [1, 0, 0, 0],
    })
    taxas = taxa_de_disparo(df)
    assert taxas["risco_ccs"] == 0.0
    assert taxas["risco_cbt"] == 1.0
    assert taxas["risco_queda_producao"] == 0.25


def test_dimensao_ausente_nao_e_inventada():
    """
    Uma coluna em falta não pode virar taxa 0 — isso confundiria "dimensão que
    não disparou" com "dimensão que nem foi calculada", que são problemas
    diferentes e com correcções diferentes.
    """
    taxas = taxa_de_disparo(pd.DataFrame({"target_risco_ccs": [0, 1]}))
    assert set(taxas) == {"risco_ccs"}


# ------------------------------------------------------------------ #
# Escala — a verificação que diz de quem é a culpa                     #
# ------------------------------------------------------------------ #

def test_escala_coerente_nao_gera_divergencia():
    assert conferir_escala(calcular_scores(lote_saudavel())) == []


def test_escala_apanha_o_fator_1000_de_c1():
    """O defeito original: coluna em MIL cel/mL julgada por um limiar em cel/mL."""
    df = lote_saudavel()
    df["ccs"] /= 1000
    df["cbt"] /= 1000

    divergencias = {d["coluna"]: d for d in conferir_escala(calcular_scores(df))}

    assert set(divergencias) == {"ccs", "cbt"}
    # Perto de três ordens de grandeza abaixo — não exactamente 1/1000, porque a
    # mediana do lote não assenta em cima do limiar. O que tem de valer é a
    # magnitude, não o número redondo.
    assert divergencias["ccs"]["ordens_de_grandeza"] == pytest.approx(-3.0, abs=0.3)
    assert divergencias["ccs"]["fator"] < 1 / 100
    assert divergencias["ccs"]["unidade_do_limiar"] == "cel/mL"


def test_escala_nao_confunde_rebanho_limpo_com_unidade_trocada():
    """
    Um rebanho bom de facto tem CCS abaixo do limiar — e isso não é defeito.
    A guarda só acusa a partir de duas ordens de grandeza, precisamente para
    não transformar "cliente com leite bom" em "pacote inválido".
    """
    df = lote_saudavel()
    df["ccs"] = 120_000.0  # ~3x abaixo do limiar de atenção: plausível
    assert conferir_escala(calcular_scores(df)) == []


def test_escala_ignora_coluna_sem_valores_positivos():
    """Sensor avariado a devolver zeros não pode virar veredicto de unidade."""
    df = lote_saudavel()
    df["ccs"] = 0.0
    assert [d["coluna"] for d in conferir_escala(calcular_scores(df))] == []


# ------------------------------------------------------------------ #
# Medida × não medida                                                  #
# ------------------------------------------------------------------ #

def test_dimensoes_medidas_resolve_pelos_aliases():
    """
    O lote traz `temp_tanque_c` e `litros_descartados`; as dependências estão
    escritas nos nomes canónicos. Se a guarda não olhasse o DataFrame já
    normalizado, daria as duas dimensões como não medidas — e um lote
    perfeitamente bom levaria um aviso falso.
    """
    medidas = dimensoes_medidas(calcular_scores(lote_saudavel()))
    assert medidas["risco_temp_tanque"] is True
    assert medidas["risco_descarte"] is True
    assert set(medidas) == set(PESOS_SCORE)


def test_coluna_ausente_e_nao_medida_nao_morta():
    laudo = avaliar_lote(lote_saudavel().drop(columns=["ccs", "cbt"]))

    assert laudo["estados"]["risco_ccs"] == NAO_MEDIDA
    assert laudo["estados"]["risco_cbt"] == NAO_MEDIDA
    assert laudo["estados"]["risco_qualidade"] == NAO_MEDIDA
    assert laudo["pontos"]["mortos"] == 0
    assert laudo["pontos"]["nao_medidos"] == 60
    # Falta de dado é aviso: o lote é importável, o score é que fica mais pobre.
    assert laudo["status"] == "aviso"
    assert "ccs" in laudo["motivos"][0]


def test_dimensao_medida_que_nunca_dispara_e_morta():
    df = lote_saudavel()
    df["temp_tanque_c"] = 2.0  # medida, sempre abaixo do limiar

    laudo = avaliar_lote(df)

    assert laudo["estados"]["risco_temp_tanque"] == MORTA
    assert laudo["pontos"]["mortos"] == PESOS_SCORE["risco_temp_tanque"]
    assert laudo["status"] == "erro"


def test_dimensao_que_dispara_em_quase_todos_e_saturada():
    df = lote_saudavel()
    df["temp_tanque_c"] = 9.0  # medida, sempre acima do limiar

    laudo = avaliar_lote(df)

    assert laudo["estados"]["risco_temp_tanque"] == SATURADA
    assert laudo["pontos"]["saturados"] == PESOS_SCORE["risco_temp_tanque"]
    assert laudo["status"] == "erro"


# ------------------------------------------------------------------ #
# O laudo                                                              #
# ------------------------------------------------------------------ #

def test_lote_saudavel_passa_com_as_sete_dimensoes_vivas():
    laudo = avaliar_lote(lote_saudavel())

    assert laudo["status"] == OK
    assert set(laudo["estados"].values()) == {OK}
    assert laudo["pontos"]["sem_informacao"] == 0
    assert laudo["motivos"] == []


def test_escala_trocada_cala_o_diagnostico_de_saturacao():
    """
    Com a unidade errada, as taxas descrevem o defeito e não os dados.
    Reportar as duas coisas ao mesmo nível mandaria recalibrar limiares que
    estão certos — que é o oposto da correcção devida.
    """
    df = lote_saudavel()
    df["ccs"] /= 1000
    df["cbt"] /= 1000

    laudo = avaliar_lote(df)

    assert laudo["status"] == "erro"
    assert len(laudo["divergencias_de_escala"]) == 2
    assert all(m.startswith("escala:") for m in laudo["motivos"])
    assert not any("não separam ninguém" in m for m in laudo["motivos"])


def test_relatorio_diz_quantos_pontos_se_perderam():
    laudo = avaliar_lote(lote_saudavel().drop(columns=["ccs", "cbt"]))
    texto = formatar_relatorio(laudo)

    assert "60 de 100 pontos sem informação" in texto
    assert NAO_MEDIDA in texto
    assert "AVISO" in texto


def test_relatorio_do_lote_saudavel_nao_inventa_alarme():
    texto = formatar_relatorio(avaliar_lote(lote_saudavel()))

    assert "0 de 100 pontos sem informação" in texto
    assert MORTA not in texto
    assert SATURADA not in texto
