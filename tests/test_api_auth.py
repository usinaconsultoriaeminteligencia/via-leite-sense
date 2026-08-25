"""
Testes da autenticação da API (via_leite/api/security.py).

O teste central é `test_toda_rota_nao_publica_exige_chave`: ele percorre as
rotas registadas na aplicação em vez de uma lista escrita à mão. Um endpoint
novo que esqueça a protecção faz este teste falhar sozinho — que é a única
forma de a garantia sobreviver ao próximo programador.
"""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

CHAVE = "chave-de-teste-nao-usar-em-producao"
OUTRA_CHAVE = "segunda-chave-de-rotacao"


def _app(monkeypatch, chaves: str | None = CHAVE, **env: str):
    """
    Importa a aplicação com o ambiente já definido.

    A app lê `VIA_LEITE_PUBLIC_DOCS` no momento da construção, por isso é
    preciso recarregar o módulo depois de mexer no ambiente — não basta
    definir a variável antes de chamar o endpoint.
    """
    import importlib

    if chaves is None:
        monkeypatch.delenv("VIA_LEITE_API_KEYS", raising=False)
    else:
        monkeypatch.setenv("VIA_LEITE_API_KEYS", chaves)
    for nome, valor in env.items():
        monkeypatch.setenv(nome, valor)

    import via_leite.api.security
    import via_leite.api.app

    importlib.reload(via_leite.api.security)
    modulo = importlib.reload(via_leite.api.app)
    return modulo.app


def _rotas_nao_publicas(app) -> list[tuple[str, str]]:
    """(método, caminho) de cada rota que deve exigir chave."""
    from via_leite.api.security import is_public_path

    fora = []
    for rota in app.routes:
        caminho = getattr(rota, "path", None)
        metodos = getattr(rota, "methods", None)
        if not caminho or not metodos or is_public_path(caminho):
            continue
        for metodo in metodos:
            if metodo in {"HEAD", "OPTIONS"}:
                continue
            fora.append((metodo, caminho))
    return fora


def test_health_responde_sem_chave(monkeypatch):
    """A Railway sonda /health sem credencial; fechá-lo derruba o deploy."""
    cliente = TestClient(_app(monkeypatch))
    assert cliente.get("/health").status_code == 200


def test_toda_rota_nao_publica_exige_chave(monkeypatch):
    app = _app(monkeypatch)
    cliente = TestClient(app)
    rotas = _rotas_nao_publicas(app)

    assert rotas, "nenhuma rota encontrada — o teste deixou de proteger algo"

    desprotegidas = []
    for metodo, caminho in rotas:
        # Parâmetros de caminho recebem um valor qualquer: a verificação de
        # credencial corre antes de a rota tocar nos dados, portanto o valor
        # é irrelevante para o que se está a medir.
        url = caminho
        for parte in caminho.split("/"):
            if parte.startswith("{") and parte.endswith("}"):
                url = url.replace(parte, "valor-qualquer")
        resposta = cliente.request(metodo, url)
        if resposta.status_code != 401:
            desprotegidas.append((metodo, caminho, resposta.status_code))

    assert not desprotegidas, (
        "rotas que responderam sem exigir chave: "
        + ", ".join(f"{m} {c} -> {s}" for m, c, s in desprotegidas)
    )


def test_escrita_sem_chave_nao_altera_dados(monkeypatch):
    """
    Os 11 endpoints de escrita eram o achado crítico: qualquer um podia gravar
    na base de produção. 401 tem de vir antes de qualquer efeito.
    """
    cliente = TestClient(_app(monkeypatch))
    resposta = cliente.post("/suppliers", json={"nome": "Fornecedor Intruso"})
    assert resposta.status_code == 401

    listagem = cliente.get("/suppliers", headers={"X-API-Key": CHAVE})
    assert listagem.status_code == 200
    nomes = [s.get("nome") for s in listagem.json()]
    assert "Fornecedor Intruso" not in nomes


def test_chave_correta_passa(monkeypatch):
    cliente = TestClient(_app(monkeypatch))
    assert cliente.get("/suppliers", headers={"X-API-Key": CHAVE}).status_code == 200


def test_chave_errada_e_recusada(monkeypatch):
    cliente = TestClient(_app(monkeypatch))
    resposta = cliente.get("/suppliers", headers={"X-API-Key": "chave-errada"})
    assert resposta.status_code == 401


def test_rotacao_aceita_as_duas_chaves(monkeypatch):
    """Rotação sem downtime: a antiga e a nova valem durante a migração."""
    cliente = TestClient(_app(monkeypatch, chaves=f"{CHAVE},{OUTRA_CHAVE}"))
    for chave in (CHAVE, OUTRA_CHAVE):
        assert cliente.get("/suppliers", headers={"X-API-Key": chave}).status_code == 200


def test_sem_chave_configurada_falha_fechado(monkeypatch):
    """
    Ambiente por configurar tem de recusar, não abrir. Este é o teste que
    impede a regressão para o estado de 06/08/2026.
    """
    cliente = TestClient(_app(monkeypatch, chaves=None))
    assert cliente.get("/suppliers").status_code == 503
    assert cliente.post("/suppliers", json={"nome": "X"}).status_code == 503
    # Mesmo apresentando uma chave: se o servidor não tem nenhuma configurada,
    # não há com o que comparar.
    assert cliente.get("/suppliers", headers={"X-API-Key": CHAVE}).status_code == 503


def test_docs_fechados_por_omissao(monkeypatch):
    cliente = TestClient(_app(monkeypatch))
    for caminho in ("/docs", "/redoc", "/openapi.json"):
        assert cliente.get(caminho).status_code == 404, caminho


def test_docs_abrem_quando_explicitamente_ligados(monkeypatch):
    cliente = TestClient(_app(monkeypatch, VIA_LEITE_PUBLIC_DOCS="1"))
    assert cliente.get("/openapi.json").status_code == 200


def test_cors_nao_traz_localhost_em_producao(monkeypatch):
    import importlib

    monkeypatch.setenv("VIA_LEITE_ENV", "production")
    monkeypatch.setenv("VIA_LEITE_API_KEYS", CHAVE)
    import via_leite.api.app

    modulo = importlib.reload(via_leite.api.app)
    assert modulo._cors_origins() == []


@pytest.fixture(autouse=True)
def _ambiente_limpo(monkeypatch):
    """
    Isola cada teste do ambiente da máquina e devolve os módulos ao estado
    original no fim, para não contaminar o resto da suite.
    """
    for nome in ("VIA_LEITE_API_KEYS", "VIA_LEITE_PUBLIC_DOCS", "VIA_LEITE_ENV"):
        monkeypatch.delenv(nome, raising=False)
    yield
    import importlib

    import via_leite.api.security
    import via_leite.api.app

    for nome in ("VIA_LEITE_API_KEYS", "VIA_LEITE_PUBLIC_DOCS", "VIA_LEITE_ENV"):
        os.environ.pop(nome, None)
    importlib.reload(via_leite.api.security)
    importlib.reload(via_leite.api.app)
