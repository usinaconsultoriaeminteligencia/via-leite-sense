"""
Testes do relatório em PDF (`via_leite/api/relatorio_pdf.py` + endpoint da API).

Contexto: o gerador nasceu na página Streamlit `7_Fornecedores_360.py`. Quando
o app Streamlit foi descomissionado, a página morreu — mas o gerador nunca
dependeu de Streamlit (só pandas e fpdf), então foi portado para a API em vez
de descartado. Estes testes existem para que a capacidade não se perca outra
vez em silêncio: se o endpoint sumir, a suíte fica vermelha.

A protecção por chave NÃO é testada aqui — `test_api_auth.py` percorre todas as
rotas registadas e cobre esta automaticamente.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def cliente():
    import via_leite.api.app as app_mod
    from via_leite.api.security import require_api_key

    app_mod.app.dependency_overrides[require_api_key] = lambda: None
    yield TestClient(app_mod.app)
    app_mod.app.dependency_overrides.clear()


def _algum_id(cliente: TestClient) -> str:
    from via_leite.api.app import _scores_base

    return str(_scores_base().iloc[0]["id_produtor"])


def test_relatorio_devolve_pdf_valido(cliente: TestClient) -> None:
    resp = cliente.get(f"/suppliers/{_algum_id(cliente)}/report.pdf")

    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    # Assinatura do formato — garante que saiu um PDF, não uma página de erro
    # com status 200, que é como um relatório quebrado passa despercebido.
    assert resp.content[:5] == b"%PDF-"
    assert len(resp.content) > 1000


def test_relatorio_sugere_nome_de_ficheiro(cliente: TestClient) -> None:
    id_prod = _algum_id(cliente)
    resp = cliente.get(f"/suppliers/{id_prod}/report.pdf")

    assert f'filename="relatorio_produtor_{id_prod}.pdf"' in resp.headers["content-disposition"]


def test_produtor_inexistente_devolve_404(cliente: TestClient) -> None:
    resp = cliente.get("/suppliers/id-que-nao-existe/report.pdf")

    assert resp.status_code == 404
