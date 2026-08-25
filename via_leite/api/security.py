"""
VIA LEITE SENSE — Autenticação da API (Fase 1: chave de API)

Contexto
--------
Até 06/08/2026 os 30 endpoints da API em produção (Railway) estavam abertos ao
público, incluindo 11 de escrita. Este módulo fecha todos eles de uma vez, via
dependência global registada em `backend/app.py`, sem tocar nos 30 decoradores.

Por que chave de API e não login de utilizador
----------------------------------------------
O frontend é um SPA estático (Vercel) — não consegue guardar um segredo. A
chave vive apenas no proxy serverless (`frontend/api/[...path].js`), que corre
no servidor; o browser nunca a vê. Isto fecha a exposição imediatamente.

Identidade individual, papéis e isolamento por cliente (tenant) são a Fase 2,
necessária antes do primeiro onboarding real. Uma chave partilhada não dá
trilha de auditoria por utilizador — não confundir as duas coisas.

Configuração
------------
    VIA_LEITE_API_KEYS   chaves válidas, separadas por vírgula.
                         Aceitar mais de uma permite rotação sem downtime:
                         publica-se a nova, migram-se os clientes, remove-se a
                         antiga.
    VIA_LEITE_PUBLIC_DOCS  "1" para expor /docs, /redoc e /openapi.json.
                           Fechados por omissão: o esquema descreve os
                           endpoints de escrita e os campos de dados pessoais.

Falha fechada: sem `VIA_LEITE_API_KEYS` definida, toda a rota não pública
responde 503. Nunca há chave por omissão — um valor de desenvolvimento embutido
é exatamente o que acaba em produção.

Autor: USINA I.A. / Fagner Vieira
"""
from __future__ import annotations

import os
import secrets

from fastapi import HTTPException, Request, status

API_KEY_HEADER = "X-API-Key"

#: Rotas servidas sem chave. Mantido mínimo e explícito.
#: /health é sondado pela Railway e não devolve dados de negócio.
PUBLIC_PATHS: frozenset[str] = frozenset({"/health"})

_DOC_PATHS: frozenset[str] = frozenset({"/docs", "/redoc", "/openapi.json"})


def configured_keys() -> tuple[str, ...]:
    """Chaves válidas lidas do ambiente. Vazio = API por configurar."""
    raw = os.environ.get("VIA_LEITE_API_KEYS", "")
    return tuple(k.strip() for k in raw.split(",") if k.strip())


def docs_are_public() -> bool:
    return os.environ.get("VIA_LEITE_PUBLIC_DOCS", "") == "1"


def is_public_path(path: str) -> bool:
    if path in PUBLIC_PATHS:
        return True
    if path in _DOC_PATHS:
        return docs_are_public()
    return False


def _key_is_valid(candidate: str, valid: tuple[str, ...]) -> bool:
    """
    Compara em tempo constante contra todas as chaves.

    `compare_digest` evita que o tempo de resposta revele quantos caracteres
    iniciais o atacante acertou. Percorremos a lista inteira sem curto-circuito
    pela mesma razão: sair mais cedo num acerto revelaria a posição da chave.
    """
    matched = False
    for key in valid:
        if secrets.compare_digest(candidate, key):
            matched = True
    return matched


async def require_api_key(request: Request) -> None:
    """
    Dependência global da aplicação. Deixa passar as rotas públicas e exige
    `X-API-Key` em todas as outras.

    Requisições CORS de pré-voo (OPTIONS) passam sem chave: o browser envia-as
    antes de poder anexar cabeçalhos personalizados, e elas não devolvem dados.
    """
    if request.method == "OPTIONS":
        return

    if is_public_path(request.url.path):
        return

    valid = configured_keys()
    if not valid:
        # Falha fechada: por configurar é diferente de aberto.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "API por configurar: defina VIA_LEITE_API_KEYS no ambiente do "
                "servidor."
            ),
        )

    presented = request.headers.get(API_KEY_HEADER, "")
    if not presented or not _key_is_valid(presented, valid):
        # A mesma resposta para ausente e inválida: distinguir as duas diz ao
        # atacante se o cabeçalho é sequer o mecanismo certo.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencial ausente ou inválida.",
            headers={"WWW-Authenticate": API_KEY_HEADER},
        )
