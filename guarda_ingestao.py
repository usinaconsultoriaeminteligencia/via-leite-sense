"""
guarda_ingestao.py — a instrumentação de entrada do achado C1 (opção 3).

C1 nasceu de um limiar escolhido sem olhar a distribuição dos dados:
`LIMIAR["ccs_atencao"] = 400_000` (cel/mL) contra uma coluna que vem em MIL
cel/mL. Quatro dimensões do score morreram em silêncio e nunca ninguém foi
avisado — o radar continuou a desenhar classes de risco, só que sem 70 dos
seus 100 pontos.

A calibração dos limiares é decisão de produto e espera pelos dados reais.
O que **não** espera é a possibilidade de o mesmo erro voltar a entrar sem
ninguém dar por isso. Este módulo corre sobre um lote antes de ele ser
importado e responde a uma pergunta só:

    este lote pode ser pontuado, ou o score que sairia daqui seria mentira?

São duas verificações, e a distinção entre elas é o ponto todo:

1. **Escala** — os dados e o limiar estão na mesma ordem de grandeza?
   Apanha o erro de unidade, que é a causa raiz de C1, e é a única das duas
   que diz *de quem é a culpa*. Um lote correcto que chegue hoje falha aqui
   por causa do código, não por causa do lote — e a mensagem tem de dizer
   isso, senão a guarda acusa o cliente de um defeito nosso.

2. **Taxa de disparo** — cada dimensão medida separa alguém? Uma que nunca
   dispara e uma que dispara em quase toda a gente são igualmente inúteis:
   distribuem o seu peso de forma constante e não ordenam produtores.

E uma distinção que a guarda nunca pode perder: **dimensão não medida não é
dimensão morta.** Um lote sem coluna `ccs` e um lote cujo CCS nunca cruza o
limiar produzem exactamente o mesmo `target_risco_ccs` — tudo a zero — e têm
correcções opostas (pedir a coluna ao cliente × recalibrar o limiar). Tratar
os dois como o mesmo caso foi o que deixou C1 invisível durante meses.

Uso:
    from guarda_ingestao import avaliar_lote, formatar_relatorio
    laudo = avaliar_lote(df)
    print(formatar_relatorio(laudo))
    if laudo["status"] == "erro":
        ...  # não importar
"""
from __future__ import annotations

from math import log10

import pandas as pd

from score_risco import LIMIAR, PESOS_SCORE, calcular_scores

PREFIXO_TARGET = "target_"

# Os dois extremos indefensáveis. O meio-termo é calibração — decisão de
# produto, fora do alcance deste módulo.
TAXA_MINIMA = 0.0   # exclusiva: tem de disparar ao menos uma vez
TAXA_MAXIMA = 0.90  # inclusiva: acima disto deixa de discriminar

# Duas ordens de grandeza. Nenhum rebanho real tem a mediana de milhares de
# colheitas 100x acima ou abaixo do limiar de ATENÇÃO da sua própria norma —
# um limiar de atenção existe justamente para cair dentro da distribuição.
# Passar disto não é rebanho excepcional: é unidade trocada.
FATOR_ESCALA_MAX = 100.0

# Coluna canónica (já depois dos aliases de `score_risco`) -> o limiar contra
# o qual ela é comparada, e a unidade que esse limiar pressupõe.
ESCALA_ESPERADA = {
    "ccs":                ("ccs_atencao",     "cel/mL"),
    "cbt":                ("cbt_atencao",     "UFC/mL"),
    "temperatura_tanque": ("temp_tanque_max", "°C"),
    "gordura_pct":        ("gordura_min",     "%"),
}

# De que colunas cada dimensão depende. Basta UMA estar presente para a
# dimensão contar como medida — é assim que `score_risco` a calcula.
DEPENDENCIAS = {
    "risco_queda_producao": ("litros_coletados",),
    "risco_qualidade":      ("ccs", "cbt", "gordura_pct"),
    "risco_ccs":            ("ccs",),
    "risco_cbt":            ("cbt",),
    "risco_temp_tanque":    ("temperatura_tanque",),
    "risco_perda_bonus":    ("ccs", "cbt"),
    "risco_descarte":       ("volume_descartado",),
}

MORTA = "MORTA"
SATURADA = "SATURADA"
NAO_MEDIDA = "NAO MEDIDA"
OK = "ok"


# ------------------------------------------------------------------ #
# Blocos de medição                                                    #
# ------------------------------------------------------------------ #

def taxa_de_disparo(df: pd.DataFrame) -> dict[str, float]:
    """Fração de linhas em que cada dimensão do score dispara.

    Devolve `{nome_da_dimensao: taxa}` para as dimensões de `PESOS_SCORE`,
    usando as colunas `target_*` produzidas por `calcular_scores`. Uma
    dimensão sem a respectiva coluna fica FORA do resultado, em vez de
    entrar como zero — ver a nota sobre "não medida" no topo do módulo.
    """
    taxas: dict[str, float] = {}
    for dimensao in PESOS_SCORE:
        coluna = f"{PREFIXO_TARGET}{dimensao}"
        if coluna in df.columns:
            taxas[dimensao] = float(df[coluna].mean())
    return taxas


def dimensoes_medidas(df: pd.DataFrame) -> dict[str, bool]:
    """Quais dimensões o lote tem como sustentar.

    Recebe o DataFrame **já normalizado** por `calcular_scores` (é lá que os
    aliases `temp_tanque_c` -> `temperatura_tanque` e `litros_descartados` ->
    `volume_descartado` são resolvidos).
    """
    presentes = set(df.columns)
    return {
        dimensao: any(coluna in presentes for coluna in colunas)
        for dimensao, colunas in DEPENDENCIAS.items()
    }


def _mediana_de_magnitude(serie: pd.Series) -> float | None:
    """Mediana dos valores positivos, ou None se não houver o que medir.

    Zeros e negativos saem porque a comparação é de ordem de grandeza: um
    zero não tem logaritmo e um sensor avariado a devolver zeros não deve
    poder arrastar a mediana para um veredicto de "unidade trocada".
    """
    valores = pd.to_numeric(serie, errors="coerce").dropna()
    valores = valores[valores > 0]
    if valores.empty:
        return None
    return float(valores.median())


def conferir_escala(df: pd.DataFrame) -> list[dict]:
    """Compara a ordem de grandeza de cada coluna com o limiar que a julga.

    Devolve uma lista de divergências. Lista vazia = dados e limiares falam
    a mesma unidade.
    """
    divergencias: list[dict] = []

    for coluna, (chave_limiar, unidade) in ESCALA_ESPERADA.items():
        if coluna not in df.columns:
            continue

        mediana = _mediana_de_magnitude(df[coluna])
        if mediana is None:
            continue

        limiar = float(LIMIAR[chave_limiar])
        if limiar <= 0:
            continue

        fator = mediana / limiar
        if 1 / FATOR_ESCALA_MAX <= fator <= FATOR_ESCALA_MAX:
            continue

        divergencias.append({
            "coluna": coluna,
            "limiar": chave_limiar,
            "valor_limiar": limiar,
            "unidade_do_limiar": unidade,
            "mediana_do_lote": mediana,
            "fator": fator,
            "ordens_de_grandeza": round(log10(fator), 1),
        })

    return divergencias


# ------------------------------------------------------------------ #
# Laudo                                                                #
# ------------------------------------------------------------------ #

def _estado(dimensao: str, taxas: dict[str, float], medidas: dict[str, bool]) -> str:
    if not medidas.get(dimensao, False):
        return NAO_MEDIDA
    taxa = taxas.get(dimensao)
    if taxa is None:
        return NAO_MEDIDA
    if taxa <= TAXA_MINIMA:
        return MORTA
    if taxa >= TAXA_MAXIMA:
        return SATURADA
    return OK


def avaliar_lote(df: pd.DataFrame) -> dict:
    """Decide se um lote pode ser pontuado, e diz porquê.

    `status`:
      - `"erro"`  — o score que sairia daqui não é interpretável
      - `"aviso"` — pontuável, mas com dimensões que o lote não sustenta
      - `"ok"`    — as 7 dimensões medidas e a discriminar

    A ordem importa: uma divergência de escala **cala** o diagnóstico de
    taxa de disparo, porque com a unidade trocada as taxas descrevem o
    defeito, não os dados. Reportar as duas coisas ao mesmo nível mandaria
    recalibrar limiares que estão certos.
    """
    com_scores = calcular_scores(df)

    taxas = taxa_de_disparo(com_scores)
    medidas = dimensoes_medidas(com_scores)
    divergencias = conferir_escala(com_scores)

    estados = {d: _estado(d, taxas, medidas) for d in PESOS_SCORE}

    def _pontos(alvo: str) -> int:
        return sum(PESOS_SCORE[d] for d, e in estados.items() if e == alvo)

    laudo = {
        "status": OK,
        "linhas": int(len(df)),
        "divergencias_de_escala": divergencias,
        "taxas": taxas,
        "estados": estados,
        "pontos": {
            "mortos": _pontos(MORTA),
            "saturados": _pontos(SATURADA),
            "nao_medidos": _pontos(NAO_MEDIDA),
        },
        "motivos": [],
    }
    laudo["pontos"]["sem_informacao"] = (
        laudo["pontos"]["mortos"]
        + laudo["pontos"]["saturados"]
        + laudo["pontos"]["nao_medidos"]
    )

    if divergencias:
        laudo["status"] = "erro"
        for d in divergencias:
            laudo["motivos"].append(
                f"escala: `{d['coluna']}` tem mediana {d['mediana_do_lote']:.4g} "
                f"e é julgada por LIMIAR[{d['limiar']!r}] = {d['valor_limiar']:.4g} "
                f"{d['unidade_do_limiar']} — fator {d['fator']:.3g} "
                f"({d['ordens_de_grandeza']:+} ordens de grandeza). "
                "Um dos dois está na unidade errada."
            )
        # Com a escala trocada, as taxas abaixo são sintoma, não diagnóstico.
        return laudo

    sem_discriminar = sorted(
        d for d, e in estados.items() if e in (MORTA, SATURADA)
    )
    if sem_discriminar:
        laudo["status"] = "erro"
        laudo["motivos"].append(
            "dimensões que não separam ninguém: "
            + ", ".join(f"{d} ({estados[d].lower()})" for d in sem_discriminar)
            + f" — {laudo['pontos']['mortos'] + laudo['pontos']['saturados']} "
            "de 100 pontos do score sem informação."
        )

    nao_medidas = sorted(d for d, e in estados.items() if e == NAO_MEDIDA)
    if nao_medidas:
        if laudo["status"] == OK:
            laudo["status"] = "aviso"
        colunas = sorted({
            c for d in nao_medidas for c in DEPENDENCIAS[d]
        } - set(com_scores.columns))
        laudo["motivos"].append(
            "dimensões sem dado no lote: "
            + ", ".join(nao_medidas)
            + f" — {laudo['pontos']['nao_medidos']} de 100 pontos indisponíveis. "
            + (f"Colunas em falta: {', '.join(colunas)}." if colunas else "")
        )

    return laudo


def formatar_relatorio(laudo: dict) -> str:
    """Tabela legível. Uma guarda que rejeita sem explicar acaba desligada."""
    linhas = [
        "",
        f"GUARDA DE INGESTÃO — {laudo['linhas']} linha(s) — status: {laudo['status'].upper()}",
        "",
        f"{'dimensão':24} {'peso':>5} {'disparo':>9}   estado",
    ]

    def _chave(item: tuple[str, str]) -> tuple[int, float]:
        dimensao, estado = item
        return (0 if estado == NAO_MEDIDA else 1, -laudo["taxas"].get(dimensao, -1.0))

    for dimensao, estado in sorted(laudo["estados"].items(), key=_chave):
        taxa = laudo["taxas"].get(dimensao)
        disparo = "—" if estado == NAO_MEDIDA or taxa is None else f"{taxa * 100:.1f}%"
        linhas.append(
            f"{dimensao:24} {PESOS_SCORE[dimensao]:>5} {disparo:>9}   {estado}"
        )

    pontos = laudo["pontos"]
    linhas.append(
        f"{'':24} {'':>5} {'':>9}   "
        f"{pontos['sem_informacao']} de 100 pontos sem informação "
        f"(mortos {pontos['mortos']} · saturados {pontos['saturados']} · "
        f"não medidos {pontos['nao_medidos']})"
    )

    if laudo["motivos"]:
        linhas.append("")
        for motivo in laudo["motivos"]:
            linhas.append(f"  - {motivo}")

    if laudo["divergencias_de_escala"]:
        linhas.extend([
            "",
            "  A escala é a causa raiz de C1 e ainda está EM ABERTO no código.",
            "  Antes de devolver o lote ao fornecedor, confirmar em que unidade",
            "  ele foi entregue: hoje o mais provável é o limiar estar errado,",
            "  não o dado.",
        ])

    return "\n".join(linhas)
