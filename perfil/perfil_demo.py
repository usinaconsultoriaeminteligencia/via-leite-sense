"""
perfil_demo.py — Mini-protótipo ISOLADO da Camada de Perfil do Produtor.
=======================================================================
NÃO é feature do app. Roda à parte, sobre a base real do projeto, para
provar o conceito antes de qualquer integração no Streamlit (decisão D3).

O que faz:
  1. Carrega a base operacional (fact_producao_produtor_dia + dim_produtor).
  2. Reaproveita o score existente (fornecedor_inteligencia.calcular_scores_fornecedores),
     que já entrega ccs_media / cbt_media / score_risco_fornecedor por produtor.
  3. Calcula o CV de produção por produtor (std/média de litros_produzidos),
     que é o eixo que separa Consistente x Oscilante.
  4. Classifica cada produtor (classificador_perfil) — 2 eixos (CCS/CBT IN 77) + CV.
     Sólidos NÃO existe na base atual -> entra só com dados reais.
  5. Cruza Score (QUANDO agir) + Perfil (COMO agir) = recomendação cirúrgica.
  6. Exporta artefatos_teste/perfil_produtor.csv e imprime diagnóstico.

Uso:
    python perfil/perfil_demo.py            # base padrão dados_teste
    python perfil/perfil_demo.py --data-dir CAMINHO
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

# raiz do projeto no path (para importar módulos do app sem tocá-los)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from via_leite.core.fornecedor_inteligencia import calcular_scores_fornecedores  # noqa: E402
from perfil.classificador_perfil import (  # noqa: E402
    Perfil,
    classificar_perfil,
    recomendacao_combinada,
)

COL_PRODUCAO = "litros_produzidos"  # CV calculado sobre a produção (eixo estrutural)


def calcular_cv_producao(prod: pd.DataFrame, col: str = COL_PRODUCAO) -> pd.DataFrame:
    """CV = desvio-padrão / média da produção diária, por produtor."""
    if col not in prod.columns:
        col = "litros_coletados"
    s = pd.to_numeric(prod[col], errors="coerce")
    base = prod.assign(_v=s)
    g = base.groupby("id_produtor")["_v"]
    cv = (g.std(ddof=1) / g.mean()).rename("cv_producao")
    n = g.size().rename("dias_serie")
    return pd.concat([cv, n], axis=1).reset_index()


def montar_perfis(data_dir: Path) -> pd.DataFrame:
    prod = pd.read_csv(data_dir / "fact_producao_produtor_dia.csv", parse_dates=["data"])
    dim = pd.read_csv(data_dir / "dim_produtor.csv")

    scores = calcular_scores_fornecedores(prod, dim, pred=None)
    cv = calcular_cv_producao(prod)
    df = scores.merge(cv, on="id_produtor", how="left")

    perfis, confs, recs = [], [], []
    for _, r in df.iterrows():
        cv_val = r["cv_producao"] if pd.notna(r["cv_producao"]) else None
        res = classificar_perfil(
            ccs=float(r["ccs_media"]),
            cbt=float(r["cbt_media"]),
            solidos_totais=None,          # ausente na base atual
            coef_variacao_producao=cv_val,
        )
        perfis.append(res.perfil.value)
        confs.append(res.confianca)
        recs.append(recomendacao_combinada(int(round(r["score_risco_fornecedor"])), res))

    df["perfil"] = perfis
    df["perfil_confianca"] = confs
    df["recomendacao_combinada"] = recs
    return df


def diagnostico(df: pd.DataFrame) -> None:
    print("\n=== DIAGNÓSTICO DA CAMADA DE PERFIL (mini-protótipo isolado) ===")
    print(f"Produtores classificados: {len(df)}")

    print("\n-- CV de produção (para validar o corte 0,15) --")
    q = df["cv_producao"].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).round(3)
    print(q.to_string())
    instavel = (df["cv_producao"] > 0.15).mean() * 100
    print(f"% com CV > 0,15 (instável): {instavel:.1f}%")

    print("\n-- CCS/CBT vs IN 77 (régua absoluta) --")
    print(f"CCS média da carteira: {df['ccs_media'].mean():.0f} mil  | acima de 500: "
          f"{(df['ccs_media'] > 500).mean()*100:.1f}%")
    print(f"CBT média da carteira: {df['cbt_media'].mean():.0f} mil  | acima de 300: "
          f"{(df['cbt_media'] > 300).mean()*100:.1f}%")

    print("\n-- Distribuição de perfis --")
    print(df["perfil"].value_counts().to_string())

    print("\n-- Amostra (Score x Perfil x recomendação) --")
    cols = ["id_produtor", "score_risco_fornecedor", "classe_risco",
            "ccs_media", "cbt_media", "cv_producao", "perfil", "perfil_confianca"]
    cols = [c for c in cols if c in df.columns]
    print(df.sort_values("score_risco_fornecedor", ascending=False)[cols].head(8).to_string(index=False))

    print("\n-- Exemplos de recomendação combinada --")
    for _, r in df.sort_values("score_risco_fornecedor", ascending=False).head(3).iterrows():
        print(f"  • {r['id_produtor']}: {r['recomendacao_combinada']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Mini-protótipo isolado da camada de perfil.")
    ap.add_argument("--data-dir", type=Path, default=Path("dados_teste"))
    ap.add_argument("--out", type=Path, default=Path("artefatos_teste/perfil_produtor.csv"))
    args = ap.parse_args()

    df = montar_perfis(args.data_dir)
    diagnostico(df)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False, encoding="utf-8-sig")
    print(f"\n[OK] Artefato exportado: {args.out}")


if __name__ == "__main__":
    main()
