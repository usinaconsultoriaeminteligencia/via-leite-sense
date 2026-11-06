"""IA (sistema baseado em conhecimento): mede os achados C2 e C4 do motor de regras.

Matéria: Inteligência Artificial. Base: ia.md §3 (formalização) e §4 (achados).

C2  As 7 dimensões não são independentes. Mede a co-ocorrência das dimensões binárias
    (quanto do score vem de dimensões que disparam juntas) e a correlação phi entre elas.
C4  Os pesos (25/20/15/15/10/10/5) não têm proveniência. Mede a sensibilidade do
    resultado ao peso: perturbação de ±20% em cada peso, pesos sorteados (Dirichlet em
    torno dos atuais) e pesos iguais. Compara o ranking de produtores (Spearman e
    sobreposição do top-10) e a proporção de linhas em Alto risco + Crítico.

Se o ranking quase não muda com o peso, o C4 é de baixa consequência e pode ser
declarado. Se muda muito, os pesos precisam de elicitação (ia.md §4, C4).

Uso (da raiz):  python -m experimentos.ia.c2_c4_sensibilidade
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

import via_leite.core.score_risco as sr

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = Path(__file__).parent / "resultados"
DIMS = list(sr.PESOS_SCORE)


def base() -> pd.DataFrame:
    """Mesma montagem do /risk-radar (via_leite/api/app.py, _risk_radar_base)."""
    df = pd.read_csv(RAIZ / "dados_teste/fact_producao_produtor_dia.csv", parse_dates=["data"], low_memory=False)
    clima = pd.read_csv(RAIZ / "dados_teste/fact_clima_diario.csv", parse_dates=["data"])
    cols = [c for c in ["data", "polo_climatico", "thi", "temp_med_c"] if c in clima.columns]
    return df.merge(clima[cols], on=["data", "polo_climatico"], how="left")


def scores_com_pesos(df_alvos: pd.DataFrame, pesos: dict) -> pd.Series:
    original = dict(sr.PESOS_SCORE)
    try:
        sr.PESOS_SCORE.clear(); sr.PESOS_SCORE.update(pesos)
        return sr._calcular_score_bruto(df_alvos)
    finally:
        sr.PESOS_SCORE.clear(); sr.PESOS_SCORE.update(original)


def resumo(df: pd.DataFrame, score: pd.Series) -> tuple[pd.Series, float]:
    por_produtor = score.groupby(df["id_produtor"]).mean()
    classes = sr._classificar_risco(score)
    alto = float(classes.isin(["Alto risco", "Crítico"]).mean())
    return por_produtor, alto


def main() -> None:
    df = sr.calcular_scores(base())
    alvos = df[[f"target_{d}" for d in DIMS]].astype(int)
    alvos.columns = DIMS

    # ---------------- C2: co-ocorrência
    taxa = alvos.mean()
    phi = alvos.corr()  # correlação de Pearson entre binárias = coeficiente phi
    pares = [(a, b, float(phi.loc[a, b])) for i, a in enumerate(DIMS) for b in DIMS[i + 1 :]]
    pares.sort(key=lambda x: -abs(x[2]))
    qual = ["risco_qualidade", "risco_ccs", "risco_cbt", "risco_perda_bonus"]
    ccs_alto = df["ccs"] >= sr.LIMIAR["ccs_alto"] if "ccs" in df.columns else pd.Series(False, index=df.index)
    pontos_ccs_alto = (alvos.loc[ccs_alto, DIMS] * pd.Series(sr.PESOS_SCORE)).sum(axis=1)

    # ---------------- C4: sensibilidade
    ref_prod, ref_alto = resumo(df, df["score_via_leite"])
    top10 = set(ref_prod.nlargest(10).index)
    cenarios = []

    def registrar(nome, pesos):
        prod, alto = resumo(df, scores_com_pesos(df, pesos))
        cenarios.append({
            "cenario": nome,
            "spearman_ranking_produtores": float(prod.corr(ref_prod, method="spearman")),
            "sobreposicao_top10": len(top10 & set(prod.nlargest(10).index)) / 10,
            "alto_mais_critico": alto,
        })

    for d in DIMS:
        for f in (0.8, 1.2):
            p = dict(sr.PESOS_SCORE); p[d] = sr.PESOS_SCORE[d] * f
            registrar(f"{d} x{f}", p)
    registrar("pesos iguais", {d: 100 / len(DIMS) for d in DIMS})
    rng = np.random.default_rng(42)
    base_w = np.array([sr.PESOS_SCORE[d] for d in DIMS], dtype=float)
    for i in range(50):
        w = rng.dirichlet(base_w / 2) * 100  # sorteio em torno dos pesos atuais
        registrar(f"dirichlet {i:02d}", dict(zip(DIMS, w)))

    cen = pd.DataFrame(cenarios)
    diri = cen[cen.cenario.str.startswith("dirichlet")]
    res = {
        "data_execucao": datetime.now().isoformat(timespec="seconds"),
        "linhas": len(df),
        "produtores": int(df["id_produtor"].nunique()),
        "C2": {
            "taxa_disparo_por_dimensao": taxa.round(4).to_dict(),
            "pares_mais_correlacionados_phi": pares[:6],
            "linhas_com_ccs_ge_500": int(ccs_alto.sum()),
            "pontos_medios_das_dimensoes_quando_ccs_ge_500": float(pontos_ccs_alto.mean()) if len(pontos_ccs_alto) else None,
            "dimensoes_de_qualidade_que_disparam_juntas_pct": float((alvos[qual].sum(axis=1) >= 2).mean()),
        },
        "C4": {
            "referencia_alto_mais_critico": ref_alto,
            "perturbacao_20pct": cen[cen.cenario.str.contains(" x")].to_dict("records"),
            "pesos_iguais": cen[cen.cenario == "pesos iguais"].to_dict("records")[0],
            "dirichlet_50": {
                "spearman_min": float(diri.spearman_ranking_produtores.min()),
                "spearman_mediana": float(diri.spearman_ranking_produtores.median()),
                "top10_min": float(diri.sobreposicao_top10.min()),
                "top10_mediana": float(diri.sobreposicao_top10.median()),
                "alto_mais_critico_faixa": [float(diri.alto_mais_critico.min()), float(diri.alto_mais_critico.max())],
            },
        },
    }
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "c2_c4_resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")

    pert = cen[cen.cenario.str.contains(" x")]
    pi = res["C4"]["pesos_iguais"]; dr = res["C4"]["dirichlet_50"]
    md = [f"# C2 e C4: resultado ({res['data_execucao']})", "",
          f"Base: `dados_teste/` ({res['linhas']} linhas, {res['produtores']} produtores), mesma montagem do `/risk-radar`.", "",
          "## C2: co-ocorrência das dimensões", "",
          "| Dimensão | Disparo |", "|---|---|"] + [f"| {d} | {v:.1%} |" for d, v in taxa.items()] + [
          "", "Pares mais correlacionados (phi): " + "; ".join(f"{a} × {b} = {v:.2f}" for a, b, v in pares[:4]), "",
          f"Linhas com CCS ≥ 500 mil: {res['C2']['linhas_com_ccs_ge_500']}; nelas, as dimensões binárias somam em média "
          f"**{res['C2']['pontos_medios_das_dimensoes_quando_ccs_ge_500'] or 0:.1f}** pontos. Linhas com 2+ dimensões de qualidade juntas: "
          f"{res['C2']['dimensoes_de_qualidade_que_disparam_juntas_pct']:.1%}.", "",
          "## C4: sensibilidade aos pesos", "",
          f"Referência: Alto + Crítico em {ref_alto:.1%} das linhas.", "",
          "| Cenário | Spearman do ranking | Top-10 mantido | Alto + Crítico |", "|---|---|---|---|",
          f"| Cada peso ±20% (pior caso de 14) | {pert.spearman_ranking_produtores.min():.3f} | {pert.sobreposicao_top10.min():.0%} | "
          f"{pert.alto_mais_critico.min():.1%} a {pert.alto_mais_critico.max():.1%} |",
          f"| Pesos iguais | {pi['spearman_ranking_produtores']:.3f} | {pi['sobreposicao_top10']:.0%} | {pi['alto_mais_critico']:.1%} |",
          f"| 50 sorteios Dirichlet (mínimo / mediana) | {dr['spearman_min']:.3f} / {dr['spearman_mediana']:.3f} | "
          f"{dr['top10_min']:.0%} / {dr['top10_mediana']:.0%} | {dr['alto_mais_critico_faixa'][0]:.1%} a {dr['alto_mais_critico_faixa'][1]:.1%} |", ""]
    (SAIDA / "c2_c4_resultados.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
