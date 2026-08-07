"""
Achado C3 — a classificação de risco não pode devolver NaN em silêncio.

O corte superior das faixas era 101. Se o score o ultrapassasse, `pd.cut`
devolvia NaN e o produtor de MAIOR risco saía sem classificação — o oposto do
que o sistema existe para fazer. A auditoria classificou C3 como latente
(o clip em 100 tornava-o inalcançável) e avisou: corrigir C1 activa-o.

Estes testes cobrem os dois caminhos: score acima do tecto e score ausente.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from score_risco import CLASSE_INDETERMINADA, _classificar_risco


def test_faixas_normais_continuam_corretas():
    entrada = pd.Series([0.0, 25.0, 25.1, 50.0, 50.1, 75.0, 75.1, 100.0])
    esperado = [
        "Baixo risco",
        "Baixo risco",
        "Atenção",
        "Atenção",
        "Alto risco",
        "Alto risco",
        "Crítico",
        "Crítico",
    ]
    assert [str(c) for c in _classificar_risco(entrada)] == esperado


def test_score_acima_do_teto_vira_critico_e_nao_nan():
    """
    O cenário que C1 iria activar: se o tecto do score subir, 101+ tem de cair
    em Crítico. Nunca em NaN — subestimar o pior produtor é o pior erro
    possível para este produto.
    """
    entrada = pd.Series([101.0, 120.0, 999.0])
    resultado = _classificar_risco(entrada)
    assert resultado.isna().sum() == 0
    assert all(str(c) == "Crítico" for c in resultado)


def test_score_ausente_fica_visivel_como_indeterminado():
    """
    NaN circula como se fosse categoria e some das contagens. Dados reais têm
    falhas de medição; a falha tem de ser visível, não silenciosa.
    """
    entrada = pd.Series([10.0, np.nan, 80.0])
    resultado = _classificar_risco(entrada)
    assert resultado.isna().sum() == 0
    assert str(resultado.iloc[1]) == CLASSE_INDETERMINADA


def test_nenhuma_linha_da_base_fica_sem_classe():
    """Guarda de ponta a ponta sobre a base que a aplicação realmente usa."""
    from gestor_store import carregar_base_treino_via_leite, init_db
    from score_risco import calcular_scores

    init_db("dados_teste")
    resultado = calcular_scores(carregar_base_treino_via_leite())
    assert resultado["classe_risco"].isna().sum() == 0
