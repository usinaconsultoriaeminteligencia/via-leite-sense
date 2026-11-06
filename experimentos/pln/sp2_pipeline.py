"""SP2 (PLN): mensagem livre do produtor → lançamento estruturado (pln.md §6 e §7).

Matéria: Processamento de Linguagem Natural.

Trilha implementada (pln.md §7):
  E0: regras + regex, para intenção e entidades (baseline honesto);
  E1: TF-IDF de n-gramas de caractere + Regressão Logística, para intenção;
      as entidades seguem pelo extrator de regras/léxico (o CRF fica para a próxima etapa).
Mecanismo de recusa (pln.md §6.1): abaixo do limiar de confiança, a mensagem vai para
confirmação humana em vez de ser lançada.

Métricas (pln.md §6): F1 macro de intenção, F1 span-level exato por entidade, taxa de
lançamento correto ponta a ponta, erro em campo crítico (volume) e cobertura × precisão
sob recusa.

Uso (da raiz):
    python -m experimentos.pln.corpus_sintetico
    python -m experimentos.pln.sp2_pipeline
    python -m experimentos.pln.sp2_pipeline --teste-real caminho/corpus_real_anonimizado.csv
O corpus real segue o formato de `dados/corpus_real_MODELO.csv` e NÃO entra no repositório.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline

from experimentos.pln.corpus_sintetico import CENTENAS, DEZENAS, DEZ_A_DEZENOVE, INTENCOES, UNIDADES

DADOS = Path(__file__).parent / "dados"
SAIDA = Path(__file__).parent / "resultados"
LIMIARES = [0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


# --------------------------------------------------------------------------- extração (E0)
_NUM_PAL = {norm(p): v for v, p in enumerate(UNIDADES) if p}
_NUM_PAL.update({norm(p): 10 + i for i, p in enumerate(DEZ_A_DEZENOVE)})
_NUM_PAL.update({norm(p): 10 * i for i, p in enumerate(DEZENAS) if p})
_NUM_PAL.update({norm(p): 100 * i for i, p in enumerate(CENTENAS) if p})
_NUM_PAL.update({"cem": 100, "mil": 1000})
_PAL = "|".join(sorted(map(re.escape, _NUM_PAL), key=len, reverse=True))
_UNID = r"(?:\s?(?:litros?|lts?|l)\b|L\b|\s+de\s+leite)"
RE_VOL_DIG = re.compile(rf"\b(\d{{2,4}}){_UNID}", re.I)
RE_VOL_EXT = re.compile(rf"\b((?:{_PAL})(?:\s+e\s+(?:{_PAL})|\s+(?:{_PAL}))*){_UNID}", re.I)
RE_VOL_VERBO_EXT = re.compile(rf"\b(?:mandei|entreguei|tirei|foram|deu|saiu)\s+((?:{_PAL})(?:\s+e\s+(?:{_PAL}))*)\b", re.I)
RE_VOL_VERBO = re.compile(r"\b(?:mandei|entreguei|tirei|foram|deu|saiu)\s+(\d{2,4})\b(?!\s*(?:mil|de\s+(?:ccs|cbt|gordura|proteina)))", re.I)
LEXICO = {
    "DOENCA": ["mastite", "mamite", "febre do leite", "carrapato", "diarreia"],
    "EQUIPAMENTO": ["resfriador", "tanque", "ordenhadeira", "gerador"],
    "INDICADOR": ["ccs", "cbt", "gordura", "proteina"],
    "TEMPO": ["hoje", "hj", "ontem a noite", "ontem", "agora cedo", "de manha", "essa semana", "semana passada"],
}
RE_ANIMAL = re.compile(r"\b(?:vaca|novilha)\s+\d+\b|\ba\s+(?:mocha|malhada|pintada)\b", re.I)
RE_VALOR = re.compile(r"\b(?:ccs|cbt|gordura|proteina|veio|ta)\s+(\d{2,3}(?:\s?mil)?)\b|\b(\d{2,3}(?:\s?mil)?)(?=\s+de\s+(?:ccs|cbt|gordura|proteina)\b)", re.I)


def extenso_para_int(s: str) -> int | None:
    total, ok = 0, False
    # a unidade pode vir colada na última palavra ("cento e oitentaL"); sem isto, 180 vira 100
    s = re.sub(r"(?:\s*de\s+leite|litros?|lts?|l)$", "", norm(s).strip())
    for tok in s.replace(" e ", " ").split():
        if tok in _NUM_PAL:
            v = _NUM_PAL[tok]
            total = total * 1000 if v == 1000 and total else total + v if v != 1000 else 1000 + total
            ok = True
    return total if ok else None


def extrair_entidades(texto: str) -> list[dict]:
    t = norm(texto)  # mesmo tamanho do original (só tira acento e caixa)
    ents: list[dict] = []

    def add(ini, fim, rot):
        if not any(not (fim <= e["ini"] or ini >= e["fim"]) for e in ents):
            ents.append({"ini": ini, "fim": fim, "rotulo": rot})

    for rx in (RE_VOL_DIG, RE_VOL_EXT):
        for m in rx.finditer(t):
            add(m.start(), m.end(), "VOLUME")
    for rx in (RE_VOL_VERBO, RE_VOL_VERBO_EXT):  # número sem unidade depois de verbo de entrega
        for m in rx.finditer(t):
            add(m.start(1), m.end(1), "VOLUME")
    for m in RE_ANIMAL.finditer(t):
        add(m.start(), m.end(), "ANIMAL")
    for rot, termos in LEXICO.items():
        for termo in sorted(termos, key=len, reverse=True):
            for m in re.finditer(rf"\b{re.escape(termo)}\b", t):
                add(m.start(), m.end(), rot)
    for m in RE_VALOR.finditer(t):
        g = 1 if m.group(1) else 2
        add(m.start(g), m.end(g), "VALOR_INDICADOR")
    return sorted(ents, key=lambda e: e["ini"])


def volume_de(texto: str, ents: list[dict]) -> int | None:
    for e in ents:
        if e["rotulo"] == "VOLUME":
            trecho = texto[e["ini"] : e["fim"]]
            dig = re.search(r"\d+", trecho)
            return int(dig.group()) if dig else extenso_para_int(trecho)
    return None


REGRAS_INTENCAO = [  # E0: primeira regra que casa decide
    ("ocorrencia_sanitaria", r"mastite|mamite|febre do leite|carrapato|diarreia"),
    ("registro_qualidade", r"\b(ccs|cbt|gordura|proteina|laudo|exame)\b"),
    ("ocorrencia_operacional", r"resfriador|ordenhadeira|gerador|pifou|estragou|defeito|desligou|barulho"),
    ("ocorrencia_logistica", r"caminhao|coleta|leiteiro|buscar|pegar o leite|estrada"),
    ("relato_ambiental", r"calor|chuva|choveu|seca|sol\b|lama"),
    ("solicitacao", r"tecnico|veterinario|ajuda|vir ver|moco da cooperativa|mandar"),
    ("registro_producao", r"\d{2,4}|litro|\blts?\b|tanque|ordenha|mandei|entreguei|tirei"),
]


def intencao_regras(texto: str) -> str:
    t = norm(texto)
    for intent, rx in REGRAS_INTENCAO:
        if re.search(rx, t):
            return intent
    return "outro"


# --------------------------------------------------------------------------- avaliação
def carregar(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        l["intencoes"] = l["intencoes"].split("|")
        l["entidades"] = json.loads(l["entidades"]) if l["entidades"] else []
        l["volume_litros"] = int(l["volume_litros"]) if l.get("volume_litros") else None
    return linhas


def f1_spans(ouro: list[list[dict]], pred: list[list[dict]]) -> dict:
    rots = sorted({e["rotulo"] for es in ouro for e in es})
    out = {}
    for r in rots + ["_todas"]:
        tp = fp = fn = 0
        for g, p in zip(ouro, pred):
            G = {(e["ini"], e["fim"], e["rotulo"]) for e in g if r == "_todas" or e["rotulo"] == r}
            P = {(e["ini"], e["fim"], e["rotulo"]) for e in p if r == "_todas" or e["rotulo"] == r}
            tp += len(G & P); fp += len(P - G); fn += len(G - P)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        out[r] = {"f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0, "precisao": prec, "revocacao": rec, "suporte": tp + fn}
    return out


def avaliar(nome: str, linhas: list[dict], intencoes_pred: list[str], confiancas: list[float] | None) -> dict:
    ouro_int = [l["intencoes"][0] for l in linhas]
    ents_pred = [extrair_entidades(l["texto"]) for l in linhas]
    vol_pred = [volume_de(l["texto"], e) for l, e in zip(linhas, ents_pred)]

    def lancamento_ok(i):
        l = linhas[i]
        return intencoes_pred[i] == ouro_int[i] and vol_pred[i] == l["volume_litros"]

    com_vol = [i for i, l in enumerate(linhas) if l["volume_litros"] is not None]
    res = {
        "conjunto": nome,
        "n": len(linhas),
        "f1_macro_intencao": f1_score(ouro_int, intencoes_pred, average="macro", labels=INTENCOES, zero_division=0),
        "acuracia_intencao": float(np.mean([a == b for a, b in zip(ouro_int, intencoes_pred)])),
        "f1_entidades": f1_spans([l["entidades"] for l in linhas], ents_pred),
        "lancamento_correto": float(np.mean([lancamento_ok(i) for i in range(len(linhas))])),
        "erro_campo_critico_volume": float(np.mean([vol_pred[i] != linhas[i]["volume_litros"] for i in com_vol])) if com_vol else None,
        "volume_lido_errado_sem_aviso": int(sum(1 for i in com_vol if vol_pred[i] not in (None, linhas[i]["volume_litros"]))),
    }
    if confiancas is not None:  # cobertura x precisão sob recusa (pln.md §6.1)
        curva = []
        for lim in LIMIARES:
            aceitas = [i for i, c in enumerate(confiancas) if c >= lim]
            curva.append({
                "limiar": lim,
                "cobertura": len(aceitas) / len(linhas),
                "lancamento_correto_entre_aceitas": float(np.mean([lancamento_ok(i) for i in aceitas])) if aceitas else None,
            })
        res["recusa"] = curva
    erros = Counter(f"{o} → {p}" for o, p in zip(ouro_int, intencoes_pred) if o != p)
    res["confusoes_mais_comuns"] = erros.most_common(5)
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--teste-real", type=Path, help="CSV anonimizado no formato de dados/corpus_real_MODELO.csv")
    args = ap.parse_args()
    treino = carregar(DADOS / "sintetico_treino_A.csv")
    conjuntos = {
        "sintetico_A (mesma distribuição)": carregar(DADOS / "sintetico_teste_A.csv"),
        "sintetico_B (fora da distribuição)": carregar(DADOS / "sintetico_teste_B_fora_distribuicao.csv"),
    }
    if args.teste_real:
        conjuntos["REAL (vale no artigo)"] = carregar(args.teste_real)

    clf = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), preprocessor=norm, min_df=2, sublinear_tf=True)),
        ("lr", LogisticRegression(max_iter=2000, C=5.0, class_weight="balanced")),
    ]).fit([l["texto"] for l in treino], [l["intencoes"][0] for l in treino])

    relatorio = {"data_execucao": datetime.now().isoformat(timespec="seconds"), "n_treino": len(treino), "resultados": []}
    for nome, linhas in conjuntos.items():
        textos = [l["texto"] for l in linhas]
        relatorio["resultados"].append({"modelo": "E0 regras", **avaliar(nome, linhas, [intencao_regras(t) for t in textos], None)})
        proba = clf.predict_proba(textos)
        pred = list(clf.classes_[proba.argmax(1)])
        relatorio["resultados"].append({"modelo": "E1 TF-IDF + LR", **avaliar(nome, linhas, pred, list(proba.max(1)))})

    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "sp2_resultados.json").write_text(json.dumps(relatorio, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [f"# SP2 — resultado ({relatorio['data_execucao']})", "",
          f"Treino: {len(treino)} mensagens sintéticas (família A). **Nenhum conjunto abaixo é real**; o número que vale no artigo vem de `--teste-real`.", "",
          "| Conjunto | Modelo | F1 macro intenção | F1 entidades (exato) | F1 VOLUME | Lançamento correto | Erro no volume | Volume errado sem aviso |",
          "|---|---|---|---|---|---|---|---|"]
    for r in relatorio["resultados"]:
        fv = r["f1_entidades"].get("VOLUME", {}).get("f1", 0)
        ev = r["erro_campo_critico_volume"]
        md.append(f"| {r['conjunto']} | {r['modelo']} | {r['f1_macro_intencao']:.3f} | {r['f1_entidades']['_todas']['f1']:.3f} | {fv:.3f} | "
                  f"{r['lancamento_correto']:.1%} | {ev:.1%} | {r['volume_lido_errado_sem_aviso']} |")
    md += ["", "## Recusa (E1): cobertura × lançamento correto", "", "| Conjunto | " + " | ".join(f"limiar {l}" for l in LIMIARES) + " |",
           "|---|" + "---|" * len(LIMIARES)]
    for r in relatorio["resultados"]:
        if "recusa" in r:
            cel = [f"{c['cobertura']:.0%} / {c['lancamento_correto_entre_aceitas']:.0%}" if c["lancamento_correto_entre_aceitas"] is not None else "—" for c in r["recusa"]]
            md.append(f"| {r['conjunto']} | " + " | ".join(cel) + " |")
    md += ["", "Célula = cobertura / lançamento correto entre as mensagens aceitas.", ""]
    (SAIDA / "sp2_resultados.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
