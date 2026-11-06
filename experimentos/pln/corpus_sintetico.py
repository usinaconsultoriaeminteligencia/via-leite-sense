"""Gerador do corpus SINTÉTICO de mensagens de produtor (pln.md §4 e §4.1).

Matéria: Processamento de Linguagem Natural. Treino e validação são sintéticos; o teste
que vale no artigo é REAL (coletado com consentimento, `pln.md` §4.2), não este.

Cada mensagem sai anotada: intenção (pln.md §5.1) e entidades com posição de caractere
(pln.md §5.2). A variação deliberada de §4.1 é aplicada e registrada por mensagem:
registro coloquial, sem acento, erros de digitação, abreviação, número por extenso,
transcrição de áudio sem pontuação, multi-intenção e mensagem ambígua.

Duas famílias de modelos de frase (A e B) com vocabulário diferente permitem medir a
queda fora da distribuição: treino em A, teste em B. É um ensaio do que acontecerá com o
corpus real, não um substituto dele.
"""
from __future__ import annotations

import csv
import json
import random
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

INTENCOES = [
    "registro_producao",
    "registro_qualidade",
    "ocorrencia_sanitaria",
    "ocorrencia_operacional",
    "ocorrencia_logistica",
    "relato_ambiental",
    "solicitacao",
    "outro",
]

UNIDADES = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
DEZ_A_DEZENOVE = ["dez", "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
DEZENAS = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
CENTENAS = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]


def por_extenso(n: int) -> str:
    """Inteiro de 1 a 1999 por extenso (pt-BR)."""
    if n == 100:
        return "cem"
    partes = []
    if n >= 1000:
        partes.append("mil")
        n -= 1000
    c, r = divmod(n, 100)
    if c:
        partes.append(CENTENAS[c])
    if r:
        if r < 10:
            partes.append(UNIDADES[r])
        elif r < 20:
            partes.append(DEZ_A_DEZENOVE[r - 10])
        else:
            d, u = divmod(r, 10)
            partes.append(DEZENAS[d] + (f" e {UNIDADES[u]}" if u else ""))
    return " e ".join(partes)


@dataclass
class Mensagem:
    texto: str = ""
    intencoes: list[str] = field(default_factory=list)
    entidades: list[dict] = field(default_factory=list)
    variacoes: list[str] = field(default_factory=list)
    familia: str = "A"
    volume_litros: int | None = None

    def add(self, trecho: str, rotulo: str | None = None) -> None:
        if rotulo:
            ini = len(self.texto)
            self.entidades.append({"ini": ini, "fim": ini + len(trecho), "rotulo": rotulo, "texto": trecho})
        self.texto += trecho


ANIMAIS = ["vaca 12", "vaca 7", "a mocha", "a malhada", "novilha 3", "a pintada", "vaca 21"]
DOENCAS = ["mastite", "mamite", "febre do leite", "carrapato", "diarreia"]
EQUIP = ["resfriador", "tanque", "ordenhadeira", "gerador"]
TEMPO = {"A": ["hoje", "ontem", "agora cedo", "essa semana"], "B": ["hj", "ontem a noite", "de manha", "semana passada"]}
INDIC = ["CCS", "CBT", "gordura", "proteina"]

MODELOS = {
    # (família A) e (família B): mesmo conteúdo, vocabulário e sintaxe diferentes
    "registro_producao": {
        "A": ["mandei {VOL} {TEMPO}", "{TEMPO} saiu {VOL} na ordenha", "entreguei {VOL} {TEMPO} pro caminhao"],
        "B": ["foram {VOL} {TEMPO}", "tirei {VOL} {TEMPO} sô", "deu {VOL} no tanque {TEMPO}"],
    },
    "registro_qualidade": {
        "A": ["deu {VAL} de {IND} no ultimo exame", "o {IND} veio {VAL}", "resultado do laticinio {IND} {VAL}"],
        "B": ["chegou o laudo {IND} ta {VAL}", "{IND} deu {VAL} esse mes", "o papel do leite falou {IND} {VAL}"],
    },
    "ocorrencia_sanitaria": {
        "A": ["a {ANIMAL} ta com {DOENCA}", "{ANIMAL} amanheceu com {DOENCA}", "suspeita de {DOENCA} na {ANIMAL}"],
        "B": ["acho que a {ANIMAL} pegou {DOENCA}", "{ANIMAL} com {DOENCA} de novo", "tem {DOENCA} na {ANIMAL} {TEMPO}"],
    },
    "ocorrencia_operacional": {
        "A": ["o {EQUIP} parou {TEMPO}", "{EQUIP} deu defeito {TEMPO}", "estragou o {EQUIP}"],
        "B": ["{EQUIP} pifou {TEMPO}", "faltou luz e o {EQUIP} desligou", "o {EQUIP} ta fazendo barulho"],
    },
    "ocorrencia_logistica": {
        "A": ["o caminhao nao veio buscar {TEMPO}", "a coleta atrasou {TEMPO}", "ninguem passou pra pegar o leite"],
        "B": ["o leiteiro furou {TEMPO}", "a estrada ta ruim o carro nao subiu", "cade o caminhao do leite"],
    },
    "relato_ambiental": {
        "A": ["com esse calor caiu a producao", "choveu demais {TEMPO} e as vacas sofreram", "o calor ta judiando do gado"],
        "B": ["sol de rachar a vaca nem come", "seca braba o pasto acabou", "muita chuva o curral virou lama"],
    },
    "solicitacao": {
        "A": ["queria que o tecnico passasse aqui", "preciso de ajuda com o exame", "pode mandar o veterinario"],
        "B": ["da pra alguem vir ver as vaca", "manda o moço da cooperativa aqui", "preciso falar com o tecnico urgente"],
    },
    "outro": {
        "A": ["bom dia", "obrigado pelo aviso", "tudo certo por aqui"],
        "B": ["blz", "valeu", "ok entendi"],
    },
}


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def erro_digitacao(s: str, rng: random.Random) -> str:
    """Troca duas letras adjacentes numa palavra sem dígito (não mexe nas entidades numéricas)."""
    palavras = s.split(" ")
    idx = [i for i, p in enumerate(palavras) if len(p) > 4 and not any(ch.isdigit() for ch in p)]
    if not idx:
        return s
    i = rng.choice(idx)
    p = palavras[i]
    j = rng.randrange(len(p) - 1)
    palavras[i] = p[:j] + p[j + 1] + p[j] + p[j + 2 :]
    return " ".join(palavras)


def preencher(modelo: str, msg: Mensagem, rng: random.Random, familia: str) -> None:
    """Escreve o modelo de frase na mensagem, anotando as entidades."""
    i = 0
    while i < len(modelo):
        if modelo[i] == "{":
            fim = modelo.index("}", i)
            ph = modelo[i + 1 : fim]
            if ph == "VOL":
                n = rng.choice(list(range(40, 900, 5)) + list(range(1000, 1600, 50)))
                msg.volume_litros = n
                estilo = rng.random()
                if estilo < 0.25:
                    num = por_extenso(n)
                    msg.variacoes.append("numero_por_extenso")
                else:
                    num = str(n)
                unidade = rng.choice([" litros", " lt", " l", "L", " litro"]) if familia == "A" else rng.choice([" litros", " lts", "", " de leite"])
                if unidade in (" lt", " lts", " l", "L"):
                    msg.variacoes.append("abreviacao")
                msg.add(num + unidade, "VOLUME")
            elif ph == "VAL":
                v = rng.choice([180, 250, 320, 410, 520, 650, 80, 120, 300])
                msg.add(rng.choice([f"{v}", f"{v} mil", f"{v}mil"]), "VALOR_INDICADOR")
            elif ph == "IND":
                msg.add(rng.choice(INDIC), "INDICADOR")
            elif ph == "ANIMAL":
                msg.add(rng.choice(ANIMAIS), "ANIMAL")
            elif ph == "DOENCA":
                msg.add(rng.choice(DOENCAS), "DOENCA")
            elif ph == "EQUIP":
                msg.add(rng.choice(EQUIP), "EQUIPAMENTO")
            elif ph == "TEMPO":
                msg.add(rng.choice(TEMPO[familia]), "TEMPO")
            i = fim + 1
        else:
            j = modelo.find("{", i)
            j = len(modelo) if j == -1 else j
            msg.add(modelo[i:j])
            i = j


def gerar(n: int, familia: str, semente: int) -> list[Mensagem]:
    rng = random.Random(semente)
    pesos = [0.30, 0.12, 0.16, 0.10, 0.09, 0.09, 0.07, 0.07]  # desbalanceado de propósito (F1 macro)
    saida = []
    for _ in range(n):
        msg = Mensagem(familia=familia)
        intent = rng.choices(INTENCOES, pesos)[0]
        msg.intencoes.append(intent)
        preencher(rng.choice(MODELOS[intent][familia]), msg, rng, familia)
        # multi-intenção: volume + sanitário na mesma frase (pln.md §4.1)
        if intent == "registro_producao" and rng.random() < 0.15:
            msg.add(rng.choice([" e ", ", ", " mas "]))
            preencher(rng.choice(MODELOS["ocorrencia_sanitaria"][familia]), msg, rng, familia)
            msg.intencoes.append("ocorrencia_sanitaria")
            msg.variacoes.append("multi_intencao")
        # mensagem ambígua/incompleta: número sem unidade nem verbo
        if rng.random() < 0.04:
            msg = Mensagem(familia=familia, intencoes=["outro"], variacoes=["ambigua"])
            msg.add(rng.choice(["320", "deu ruim", "aquilo de ontem", "e agora?"]))
        texto = msg.texto
        # transformações que não deslocam as entidades: acento e caixa preservam o tamanho
        r = rng.random()
        if r < 0.35:
            texto = sem_acento(texto)
            msg.variacoes.append("sem_acento")
        if rng.random() < 0.2:
            texto = texto.upper() if rng.random() < 0.3 else texto.capitalize()
            msg.variacoes.append("caixa")
        if rng.random() < 0.15 and not msg.entidades:
            texto = erro_digitacao(texto, rng)
            msg.variacoes.append("erro_digitacao")
        if rng.random() < 0.15:
            msg.variacoes.append("transcricao_audio")  # já sem pontuação final
        else:
            texto += rng.choice(["", ".", "!", " 👍"]) if familia == "A" else rng.choice(["", "", "..", " kkk"])
        assert len(texto) >= len(msg.texto) or not msg.entidades
        for e in msg.entidades:  # confere que as posições continuam válidas
            assert sem_acento(texto[e["ini"] : e["fim"]]).lower() == sem_acento(e["texto"]).lower(), (texto, e)
        msg.texto = texto
        saida.append(msg)
    return saida


def salvar(mensagens: list[Mensagem], caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["texto", "intencoes", "entidades", "variacoes", "familia", "volume_litros"])
        for m in mensagens:
            w.writerow([m.texto, "|".join(m.intencoes), json.dumps(m.entidades, ensure_ascii=False),
                        "|".join(m.variacoes), m.familia, m.volume_litros if m.volume_litros is not None else ""])


if __name__ == "__main__":
    base = Path(__file__).parent / "dados"
    salvar(gerar(900, "A", 42), base / "sintetico_treino_A.csv")
    salvar(gerar(300, "A", 7), base / "sintetico_teste_A.csv")
    salvar(gerar(300, "B", 99), base / "sintetico_teste_B_fora_distribuicao.csv")
    print("corpus gravado em", base)
