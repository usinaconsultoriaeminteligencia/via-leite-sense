"""
Achado C1 — uma dimensão de risco que nunca dispara, ou que dispara em quase
toda a gente, não é um sinal: é uma constante disfarçada.

O score soma 7 dimensões binárias ponderadas. Em 07/08/2026, na base que a
aplicação carrega:

    risco_qualidade      20 pts     0,0%   morta
    risco_ccs            15 pts     0,0%   morta
    risco_cbt            15 pts     0,0%   morta
    risco_perda_bonus    10 pts     0,0%   morta
    risco_temp_tanque    10 pts    94,4%   saturada
    risco_queda_producao 25 pts    23,6%   ok
    risco_descarte        5 pts     0,4%   evento raro

70 dos 100 pontos não distinguem produtor nenhum. O score é, na prática,
`queda_producao` com etapas decorativas em volta — e é por isso que a carteira
não tem um único "Crítico".

As duas causas são a mesma: **limiar escolhido sem olhar a distribuição dos
dados**, uma vez travando em zero e outra em 100%.

    LIMIAR["ccs_atencao"] = 400_000    # cel/mL, mas a coluna vem em MIL cel/mL
    LIMIAR["temp_tanque_max"] = 4.0    # °C, mas o p25 da base é 4,53 °C

**20/10/2026 — unidade corrigida.** Os limiares de CCS/CBT passaram a MIL por
mL, ancorados na IN 76 e na referência pública da RBQL (sem a Piracanjuba, que
não cederá dados). As quatro dimensões mortas voltaram a disparar:

    risco_qualidade      83,0%    risco_cbt          80,6%
    risco_ccs            48,0%    risco_perda_bonus  20,2%

Resta `risco_temp_tanque` saturada. Ali o limiar (4 °C, IN 77) está certo e
o errado é o gerador sintético — é o passo seguinte da calibração, e é ele
que ainda mantém o teste xfail abaixo.

Este módulo não escolhe limiares — isso é decisão de produto e precisa dos
dados reais. Ele faz o defeito **falhar em voz alta** em vez de mentir em
silêncio, e passa a apanhar sozinho qualquer dimensão futura que nasça morta ou
saturada.

A opção 3 da decisão de C1 — instrumentar a ingestão — foi executada em
12/08/2026 e vive em `guarda_ingestao.py`. Este ficheiro passou a importar de
lá `taxa_de_disparo` e os dois limites: um registo do defeito e a guarda que
corre em produção têm de medir a MESMA coisa, senão calibrar uma delas deixa
a outra a mentir.
"""
from __future__ import annotations

import pytest

from via_leite.ingest.guarda_ingestao import TAXA_MAXIMA, TAXA_MINIMA, taxa_de_disparo
from via_leite.store.gestor_store import carregar_base_treino_via_leite, init_db
from via_leite.core.score_risco import PESOS_SCORE, calcular_scores

# Estado conhecido em 20/10/2026, com a unidade de CCS/CBT já corrigida.
# Não é o estado desejado: é o retrato do defeito, para que qualquer mudança
# nele — para melhor ou para pior — apareça em vez de passar despercebida.
DIMENSOES_MORTAS: set[str] = set()
DIMENSOES_SATURADAS = {"risco_temp_tanque"}


def _relatorio(taxas: dict[str, float]) -> str:
    """Tabela legível — um teste que falha tem de dizer o que está errado."""
    linhas = ["", f"{'dimensão':24} {'peso':>5} {'disparo':>9}   estado"]
    for dimensao, taxa in sorted(taxas.items(), key=lambda x: -x[1]):
        if taxa <= TAXA_MINIMA:
            estado = "MORTA"
        elif taxa >= TAXA_MAXIMA:
            estado = "SATURADA"
        else:
            estado = "ok"
        linhas.append(
            f"{dimensao:24} {PESOS_SCORE[dimensao]:>5} {taxa * 100:>8.1f}%   {estado}"
        )
    perdidos = sum(
        PESOS_SCORE[d]
        for d, t in taxas.items()
        if t <= TAXA_MINIMA or t >= TAXA_MAXIMA
    )
    linhas.append(f"{'':24} {'':>5} {'':>9}   {perdidos} de 100 pontos sem informação")
    return "\n".join(linhas)


@pytest.fixture(scope="module")
def taxas_da_base() -> dict[str, float]:
    init_db("dados_teste")
    return taxa_de_disparo(calcular_scores(carregar_base_treino_via_leite()))


# --------------------------------------------------------------------- #
# A guarda, na forma que se quer                                         #
# --------------------------------------------------------------------- #

@pytest.mark.xfail(
    strict=True,
    reason=(
        "Achado C1 em aberto: unidade de CCS/CBT corrigida em 20/10/2026; resta "
        "1 dimensão saturada (temp_tanque) porque o gerador põe o tanque acima "
        "dos 4 °C da IN 77 em 94% das linhas. "
        "Quando a calibração for decidida, este teste passa — e o strict=True "
        "torna o XPASS um erro, forçando a remoção deste marcador."
    ),
)
def test_nenhuma_dimensao_morta_ou_saturada(taxas_da_base):
    """
    O estado desejado. Falha hoje de propósito — é o registo executável de C1.

    Não usar `xfail(strict=False)`: um teste que aceita passar e falhar deixa de
    avisar seja o que for.
    """
    problemas = {
        d: t for d, t in taxas_da_base.items()
        if t <= TAXA_MINIMA or t >= TAXA_MAXIMA
    }
    assert not problemas, _relatorio(taxas_da_base)


# --------------------------------------------------------------------- #
# A guarda que protege hoje                                              #
# --------------------------------------------------------------------- #

def test_o_defeito_conhecido_nao_mudou(taxas_da_base):
    """
    Trava o retrato de C1 para que ele não se agrave em silêncio.

    Falha se uma dimensão nova morrer ou saturar, e falha também se uma das
    conhecidas melhorar — nesse caso a correcção é actualizar as constantes no
    topo deste ficheiro, conscientemente.
    """
    mortas = {d for d, t in taxas_da_base.items() if t <= TAXA_MINIMA}
    saturadas = {d for d, t in taxas_da_base.items() if t >= TAXA_MAXIMA}

    assert mortas == DIMENSOES_MORTAS, _relatorio(taxas_da_base)
    assert saturadas == DIMENSOES_SATURADAS, _relatorio(taxas_da_base)


def test_a_unica_dimensao_que_discrimina_continua_viva(taxas_da_base):
    """
    `queda_producao` foi, até 20/10/2026, o que restava do score, e continua a
    ser a dimensão de maior peso. Se ela partir, o sistema deixa de ordenar produtores por completo e
    ninguém dá por isso — as classes continuam a ser preenchidas.
    """
    taxa = taxas_da_base["risco_queda_producao"]
    assert TAXA_MINIMA < taxa < TAXA_MAXIMA, _relatorio(taxas_da_base)


# A função `taxa_de_disparo` é verificada sem depender de dados em
# `tests/test_guarda_ingestao.py`, onde ela agora vive.
