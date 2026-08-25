"""
Achado A2 — identificadores não podem virar features do modelo.

O modelo em produção foi treinado com `fornecedor_cpf_cnpj` e
`fornecedor_nome_razao_social` como features one-hot. A causa não foram os dois
nomes: era `selecionar_colunas` funcionar por lista de exclusão, deixando
qualquer coluna de texto nova entrar como feature sozinha.

Estes testes fecham as duas portas: os nomes conhecidos e a regra geral.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from via_leite.models.treino_mvp_avancado import (
    IDENTIFICADORES_PROIBIDOS,
    e_identificador,
    selecionar_colunas,
)

ARTEFATOS = Path("artefatos_teste") / "metricas_modelo.json"


def _base_falsa(colunas_extra: dict[str, list]) -> pd.DataFrame:
    """Base mínima com as colunas que `selecionar_colunas` espera encontrar."""
    dados = {
        "data": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "litros_coletados_d7": [100.0, 110.0],
        "litros_coletados": [100.0, 110.0],
        "litros_produzidos": [120.0, 130.0],
        "litros_previstos": [105.0, 115.0],
        "target_queda_7d": [0, 0],
        "target_queda_15d": [0, 0],
        "target_queda_30d": [0, 0],
        "temperatura_media": [22.5, 23.1],
        "polo_climatico": ["sul", "norte"],
    }
    dados.update(colunas_extra)
    return pd.DataFrame(dados)


@pytest.mark.parametrize("coluna", sorted(IDENTIFICADORES_PROIBIDOS))
def test_identificador_conhecido_e_reconhecido(coluna):
    assert e_identificador(coluna)


@pytest.mark.parametrize(
    "coluna",
    [
        "cpf_do_produtor",
        "fornecedor_cnpj",
        "documento_fiscal",
        "nome_completo",
        "razao_social_cliente",
        "email_contato",
        "telefone_celular",
        "endereco_fazenda",
        "inscricao_estadual",
    ],
)
def test_identificador_novo_e_apanhado_pelo_padrao(coluna):
    """
    A rede de segurança tem de apanhar colunas que ainda não existem — é assim
    que se evita repetir A2 na próxima junção com uma tabela de cadastro.
    """
    assert e_identificador(coluna)


@pytest.mark.parametrize(
    "coluna",
    ["polo_climatico", "temperatura_media", "id_rota", "id_laticinio", "tipo_sistema"],
)
def test_preditor_legitimo_nao_e_confundido(coluna):
    """
    Rota e laticínio identificam entidades operacionais, não pessoas, e são
    preditores legítimos. Um filtro que os apanhasse seria inútil por excesso.
    """
    assert not e_identificador(coluna)


def test_identificadores_ficam_fora_das_features():
    df = _base_falsa(
        {
            "fornecedor_cpf_cnpj": ["111.111.111-11", "222.222.222-22"],
            "fornecedor_nome_razao_social": ["Fazenda A", "Fazenda B"],
        }
    )
    cat, num = selecionar_colunas(df)
    features = set(cat) | set(num)
    assert "fornecedor_cpf_cnpj" not in features
    assert "fornecedor_nome_razao_social" not in features
    # E o que é legítimo continua a entrar — o filtro não pode esvaziar o modelo.
    assert "polo_climatico" in features
    assert "temperatura_media" in features


def test_pos_condicao_recusa_identificador_na_lista_de_features():
    """
    `garantir_sem_identificadores` é a rede para o dia em que alguém refizer a
    montagem das features e desfizer a exclusão sem reparar. Com o código de
    hoje ela não dispara — a exclusão apanha tudo antes —, por isso testa-se
    directamente, e não através de `selecionar_colunas`.
    """
    from via_leite.models.treino_mvp_avancado import garantir_sem_identificadores

    # Lista saudável passa em silêncio.
    garantir_sem_identificadores(["polo_climatico", "temperatura_media"])

    with pytest.raises(ValueError, match="A2"):
        garantir_sem_identificadores(["temperatura_media", "fornecedor_cpf_cnpj"])


@pytest.mark.skipif(not ARTEFATOS.exists(), reason="artefatos ainda não gerados")
def test_modelo_publicado_nao_tem_identificadores():
    """
    Guarda sobre o artefacto que a API realmente serve. Se alguém retreinar com
    uma versão antiga do código e commitar, isto apanha.
    """
    metricas = json.loads(ARTEFATOS.read_text(encoding="utf-8"))
    publicadas = metricas["features_categoricas"] + metricas["features_numericas"]
    infractoras = [c for c in publicadas if e_identificador(c)]
    assert not infractoras, (
        f"o modelo publicado usa identificadores como features: {infractoras}"
    )
