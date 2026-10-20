"""
Referência pública RBQL (Zenodo 17714633): o bruto versionado é o publicado,
a normalização não perde nem inventa linha, e o erro conhecido da fonte fica
marcado em vez de corrigido à mão.
"""

import pytest

from via_leite.ingest import referencia_qualidade_rbql as rbql


@pytest.fixture(scope="module")
def ref():
    return rbql.normalizar(rbql.carregar_bruto())


def test_bruto_e_o_publicado_no_zenodo():
    assert rbql.sha256(rbql.BRUTO) == rbql.SHA256_BRUTO


def test_normalizacao_cobre_12_localidades_11_anos_4_metricas(ref):
    assert len(ref) == 12 * 11 * 4
    assert ref["localidade_fonte"].nunique() == 12
    assert sorted(ref["ano"].unique()) == list(range(2013, 2024))


def test_unico_invalido_e_o_esd_do_rs_2023(ref):
    inv = ref[~ref["valido"]]
    assert len(inv) == 1
    linha = inv.iloc[0]
    assert (linha["uf"], linha["ano"], linha["metrica"]) == ("RS", 2023, "esd")


def test_ccs_e_cbt_estao_em_mil_por_ml(ref):
    # Em cél/mL os valores teriam 6 dígitos; em mil cél/mL ficam na casa das centenas.
    for metrica in ("ccs", "cbt"):
        sel = ref[ref["metrica"] == metrica]
        assert sel["maximo"].max() < 2000


def test_faixa_go_recente(ref):
    f = rbql.faixa_referencia(ref, "ccs", uf="GO", desde=2019)
    assert f["anos"] == [2019, 2023]
    assert f["n_pontos"] == 5
    assert f["minimo"] <= f["mediana_ponto_medio"] <= f["maximo"] < rbql.LIMITE_IN76["ccs"]


def test_recorte_vazio_falha_em_voz_alta(ref):
    with pytest.raises(ValueError):
        rbql.faixa_referencia(ref, "ccs", uf="TO")
