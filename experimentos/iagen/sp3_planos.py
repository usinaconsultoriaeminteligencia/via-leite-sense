"""SP3 (IA Generativa): plano de ação ancorado em norma (RAG) x não ancorado x regras.

Matéria: Inteligência Artificial Generativa. Desenho de ia_generativa.md §6 (4 braços)
e §7 (métricas M1–M8), sobre os 30 produtores servidos hoje.

  B0  gerar_recomendacao() de produção (baseline medido: 3 textos / 30 produtores)
  B1  B0 + RECEITAS do classificador de perfil (o G2 ligado): controle
  B2  LLM sem recuperação: score e indicadores no prompt
  B3  LLM + recuperação (TF-IDF) sobre o corpus normativo em corpus/, com recusa

B0 e B1 rodam sempre. B2 e B3 rodam quando houver ANTHROPIC_API_KEY no ambiente;
B3 também precisa do texto oficial em corpus/ (ver corpus/LEIA-ME.md).

Restrição dura (ia_generativa.md §8.3, ligada a A2): ao LLM só vão indicadores, score e
um identificador pseudonimizado (P01..P30). Nenhum nome, CPF, município ou coordenada.

Métricas automáticas: M3 (citação), M4 (especificidade), M5 (fidelidade ao indicador),
M6 (acionabilidade, heurística) e um alarme de guardrail para M7 (dose, carência,
prescrição). M1, M2 e M7 são julgamento humano: o script gera a planilha de dupla
avaliação em resultados/avaliacao_humana.csv.

Uso (da raiz):  python -m experimentos.iagen.sp3_planos
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from perfil.classificador_perfil import classificar_perfil, recomendacao_combinada  # noqa: E402
from via_leite.core.fornecedor_inteligencia import calcular_scores_fornecedores  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CORPUS = Path(__file__).parent / "corpus"
SAIDA = Path(__file__).parent / "resultados"
LIMIAR_RECUSA = 0.12  # similaridade mínima do melhor trecho; abaixo disso B3 não gera (§7.1, item 1)
MODELO_LLM = os.environ.get("VIA_LEITE_LLM_MODELO", "claude-sonnet-5-5")

REGRAS_PROMPT = """Você escreve planos de ação para o gestor de qualidade de uma cooperativa de leite.
Regras obrigatórias:
1. Recomende procedimento e encaminhamento (ex.: coletar amostra para cultura, revisar a rotina de
   ordenha, acionar o responsável técnico). NUNCA indique dose, medicamento, carência ou conduta
   veterinária.
2. Cada recomendação diz o que fazer, quem faz e em que prazo.
3. Só afirme o que estiver nos indicadores do produtor{ancora}.
4. Marque como [norma] o que vem de norma, citando o dispositivo, e como [sugestão] o que é
   escolha de manejo.
5. No máximo 5 itens, em português do Brasil, texto simples."""


def norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")


# ----------------------------------------------------------------------------- casos
def montar_casos() -> pd.DataFrame:
    dados, arts = RAIZ / "dados_teste", RAIZ / "artefatos_teste"
    prod = pd.read_csv(dados / "fact_producao_produtor_dia.csv", parse_dates=["data"])
    dim = pd.read_csv(dados / "dim_produtor.csv", parse_dates=["data_inicio_fornecimento"])
    pred = pd.read_csv(arts / "predicoes_teste.csv", parse_dates=["data"])
    s = calcular_scores_fornecedores(prod, dim, pred)
    cv = prod.groupby("id_produtor")["litros_coletados"].agg(lambda x: x.std() / x.mean() if x.mean() else np.nan)
    s["cv_producao"] = s["id_produtor"].map(cv)
    s = s.sort_values("id_produtor").reset_index(drop=True)
    s["pseudonimo"] = [f"P{i + 1:02d}" for i in range(len(s))]  # nada identificável sai daqui
    return s


def indicadores_para_llm(r: pd.Series) -> dict:
    return {
        "produtor": r["pseudonimo"],
        "score_risco_0_100": round(float(r["score_risco_fornecedor"]), 1),
        "classe_risco": r["classe_risco"],
        "ccs_media_mil_cel_ml": round(float(r["ccs_media"]), 0),
        "cbt_media_mil_ufc_ml": round(float(r["cbt_media"]), 0),
        "taxa_reprovacao_pct": round(float(r["taxa_reprovacao_pct"]), 2),
        "taxa_descarte_pct": round(float(r["taxa_descarte_pct"]), 2),
        "risco_queda_volume_pct": round(float(r["risco_queda_pct"]), 1),
        "tendencia_volume_pct": round(float(r["tendencia_volume_pct"]), 1),
        "taxa_falha_coleta_pct": round(float(r["taxa_falha_pct"]), 2),
        "risco_antibiotico_pct": round(float(r["risco_antibiotico_pct"]), 2),
    }


# ----------------------------------------------------------------------------- braços
def b0(r: pd.Series) -> str:
    return r["recomendacao"]


def b1(r: pd.Series) -> str:
    perfil = classificar_perfil(float(r["ccs_media"]), float(r["cbt_media"]), coef_variacao_producao=float(r["cv_producao"]))
    return f"{r['recomendacao']} {recomendacao_combinada(int(round(r['score_risco_fornecedor'])), perfil)}"


def carregar_corpus() -> list[dict]:
    """Cada .txt em corpus/ começa com cabeçalho 'fonte:', 'versao:', 'acesso:' e é cortado em trechos."""
    trechos = []
    for arq in sorted(CORPUS.glob("*.txt")):
        txt = arq.read_text(encoding="utf-8")
        cab, _, corpo = txt.partition("\n---\n")
        meta = dict(l.split(":", 1) for l in cab.splitlines() if ":" in l)
        partes = re.split(r"\n(?=Art\.\s*\d+)", corpo) if "Art." in corpo else corpo.split("\n\n")
        for p in partes:
            p = p.strip()
            if len(p) > 40:
                art = re.match(r"(Art\.\s*\d+[º°]?)", p)
                trechos.append({"documento": meta.get("fonte", arq.stem).strip(), "dispositivo": art.group(1) if art else "", "texto": p})
    return trechos


# palavras vazias: sem elas, "preço do boi gordo na bolsa" casava com a norma pelo "do" e pelo "na"
STOP_PT = sorted({norm(w) for w in """a o as os um uma de do da dos das no na nos nas em por para com sem ao aos
e ou que se seu sua seus suas este esta estes estas esse essa isso ser deve devem pelo pela pelos pelas
sao são é ter tem como mais menos quando onde qual quais leite""".split()})


class Recuperador:
    def __init__(self, trechos: list[dict]):
        self.trechos = trechos
        self.vec = TfidfVectorizer(preprocessor=norm, ngram_range=(1, 2), sublinear_tf=True, stop_words=STOP_PT)
        self.M = self.vec.fit_transform([t["texto"] for t in trechos])

    def buscar(self, consulta: str, k: int = 4) -> list[tuple[float, dict]]:
        sims = (self.M @ self.vec.transform([consulta]).T).toarray().ravel()
        idx = sims.argsort()[::-1][:k]
        return [(float(sims[i]), self.trechos[i]) for i in idx]


def consulta_do_caso(ind: dict) -> str:
    termos = ["qualidade do leite cru refrigerado"]
    if ind["ccs_media_mil_cel_ml"] >= 400: termos += ["contagem de células somáticas CCS mastite"]
    if ind["cbt_media_mil_ufc_ml"] >= 100: termos += ["contagem bacteriana total CBT CPP higiene ordenha refrigeração tanque"]
    if ind["risco_antibiotico_pct"] > 0: termos += ["resíduos de antimicrobianos"]
    return " ".join(termos)


def chamar_llm(sistema: str, usuario: str) -> tuple[str, float]:
    chave = os.environ["ANTHROPIC_API_KEY"]
    corpo = json.dumps({"model": MODELO_LLM, "max_tokens": 700, "temperature": 0,
                        "system": sistema, "messages": [{"role": "user", "content": usuario}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=corpo, headers={
        "x-api-key": chave, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=60) as resp:
        out = json.loads(resp.read())
    return "".join(b.get("text", "") for b in out["content"]), time.time() - t0


def b2(ind: dict) -> tuple[str, float]:
    return chamar_llm(REGRAS_PROMPT.format(ancora=""), "Indicadores do produtor:\n" + json.dumps(ind, ensure_ascii=False))


def b3(ind: dict, rec: Recuperador) -> tuple[str, float, list, bool]:
    achados = rec.buscar(consulta_do_caso(ind))
    if not achados or achados[0][0] < LIMIAR_RECUSA:
        return "", 0.0, achados, True  # recusa: devolve o plano de regras e sinaliza (§7.1)
    contexto = "\n\n".join(f"[{t['documento']} {t['dispositivo']}] {t['texto'][:1200]}" for _, t in achados)
    sistema = REGRAS_PROMPT.format(ancora=" e nos trechos normativos fornecidos; cite o dispositivo de cada [norma]")
    texto, seg = chamar_llm(sistema, f"Trechos normativos:\n{contexto}\n\nIndicadores do produtor:\n{json.dumps(ind, ensure_ascii=False)}")
    return texto, seg, achados, False


# ----------------------------------------------------------------------------- métricas
VERBOS_ACAO = r"\b(verificar|revisar|coletar|acionar|investigar|abrir|priorizar|padronizar|trabalhar|ajustar|agendar|treinar|limpar|higienizar|conferir|registrar|encaminhar|orientar)\w*"
GUARDRAIL = r"\b\d+\s?(mg|ml|ui)\b|\bcar[eê]ncia\b|\b(antibi[oó]tico|amoxicilina|penicilina|cefalosporina|oxitetraciclina)\b|\bdose\b|\baplicar\b"


def fidelidade(texto: str, r: pd.Series) -> float | None:
    """M5: dos indicadores alterados do produtor, quantos o texto menciona."""
    t, alvos = norm(texto), []
    if r["ccs_media"] >= 400: alvos.append(r"ccs|celulas somaticas|mastite|ordenha")
    if r["cbt_media"] >= 100: alvos.append(r"cbt|cpp|bacteri|higien|tanque|resfri")
    if r["risco_queda_pct"] >= 25 or r["tendencia_volume_pct"] <= -8: alvos.append(r"volume|producao|queda")
    if r["taxa_falha_pct"] >= 2: alvos.append(r"rota|coleta")
    return float(np.mean([bool(re.search(a, t)) for a in alvos])) if alvos else None


def metricas(nome: str, textos: list[str], casos: pd.DataFrame) -> dict:
    validos = [(t, r) for t, (_, r) in zip(textos, casos.iterrows()) if t]
    if not validos:
        return {"braco": nome, "executado": False}
    fid = [f for t, r in validos if (f := fidelidade(t, r)) is not None]
    return {
        "braco": nome,
        "executado": True,
        "n": len(validos),
        "M3_citacao_norma": float(np.mean([bool(re.search(r"\bIN\s?7[67]\b|instru[cç][aã]o normativa", t, re.I)) for t, _ in validos])),
        "M4_especificidade": len({t for t, _ in validos}) / len(validos),
        # sem números: impede que "Score 48" x "Score 22" conte como texto diferente
        "M4_especificidade_sem_numeros": len({re.sub(r"\d+[.,]?\d*", "#", t) for t, _ in validos}) / len(validos),
        "M5_fidelidade_indicador": float(np.mean(fid)) if fid else None,
        # heurística: há ao menos um verbo de ação; o julgamento fino (responsável e prazo) é humano
        "M6_acionabilidade_heuristica": float(np.mean([bool(re.search(VERBOS_ACAO, norm(t))) for t, _ in validos])),
        "alarme_guardrail_M7": int(sum(bool(re.search(GUARDRAIL, norm(t))) for t, _ in validos)),
    }


def main() -> None:
    casos = montar_casos()
    SAIDA.mkdir(parents=True, exist_ok=True)
    textos = {"B0": [b0(r) for _, r in casos.iterrows()], "B1": [b1(r) for _, r in casos.iterrows()],
              "B2": [""] * len(casos), "B3": [""] * len(casos)}
    extra = {"B2_latencia_s": [], "B3_latencia_s": [], "B3_recusas": 0, "B3_trechos": {}}
    tem_llm = bool(os.environ.get("ANTHROPIC_API_KEY"))
    corpus = carregar_corpus()
    rec = Recuperador(corpus) if corpus else None
    if tem_llm:
        for i, (_, r) in enumerate(casos.iterrows()):
            ind = indicadores_para_llm(r)
            textos["B2"][i], s = b2(ind)
            extra["B2_latencia_s"].append(s)
            if rec:
                t, s, achados, recusou = b3(ind, rec)
                textos["B3"][i] = t if not recusou else b1(r) + " [recusa: sem trecho normativo acima do limiar]"
                extra["B3_recusas"] += int(recusou)
                extra["B3_latencia_s"].append(s)
                extra["B3_trechos"][ind["produtor"]] = [(round(sc, 3), t["documento"], t["dispositivo"]) for sc, t in achados]

    res = {
        "data_execucao": datetime.now().isoformat(timespec="seconds"),
        "n_produtores": len(casos),
        "llm": MODELO_LLM if tem_llm else "não executado (sem ANTHROPIC_API_KEY)",
        "corpus_trechos": len(corpus),
        "metricas": [metricas(b, textos[b], casos) for b in ["B0", "B1", "B2", "B3"]],
        "B3_recusas": extra["B3_recusas"],
        "latencia_media_s": {k: float(np.mean(v)) for k, v in extra.items() if k.endswith("_s") and v},
        "B3_trechos_recuperados": extra["B3_trechos"],
    }
    (SAIDA / "sp3_resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    # planilha para dupla avaliação humana de M1, M2 e M7 (ia_generativa.md §7)
    with (SAIDA / "avaliacao_humana.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["produtor", "braco", "indicadores", "plano", "M1_afirmacoes_verificaveis", "M1_contradizem",
                    "M2_rastreaveis_a_trecho", "M7_erro_critico_sim_nao", "avaliador", "observacao"])
        for i, (_, r) in enumerate(casos.iterrows()):
            for b in ["B0", "B1", "B2", "B3"]:
                if textos[b][i]:
                    for av in ("A", "B"):
                        w.writerow([r["pseudonimo"], b, json.dumps(indicadores_para_llm(r), ensure_ascii=False), textos[b][i], "", "", "", "", av, ""])

    linhas = [f"# SP3 — resultado ({res['data_execucao']})", "",
              f"30 produtores da base de referência · LLM: {res['llm']} · corpus normativo: {len(corpus)} trechos", "",
              "| Braço | Executado | M3 citação | M4 especificidade | M4 sem números | M5 fidelidade | M6 acionável (heur.) | Alarmes M7 |", "|---|---|---|---|---|---|---|---|"]
    for m in res["metricas"]:
        if m["executado"]:
            linhas.append(f"| {m['braco']} | sim | {m['M3_citacao_norma']:.0%} | {m['M4_especificidade']:.2f} | "
                          f"{m['M4_especificidade_sem_numeros']:.2f} | {m['M5_fidelidade_indicador']:.0%} | {m['M6_acionabilidade_heuristica']:.0%} | {m['alarme_guardrail_M7']} |")
        else:
            linhas.append(f"| {m['braco']} | não | — | — | — | — | — | — |")
    linhas += ["", "M1, M2 e M7 são julgamento humano: preencher `avaliacao_humana.csv` (dois avaliadores, Kappa).", ""]
    (SAIDA / "sp3_resultados.md").write_text("\n".join(linhas), encoding="utf-8")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
