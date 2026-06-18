"""
score_risco.py — VIA LEITE SENSE Sprint 4
Motor de scoring de risco produtivo, qualidade e rentabilidade.

Responsabilidade: receber um DataFrame com colunas da base operacional
e retornar o mesmo DataFrame enriquecido com:
  - targets de risco binários (0/1)
  - score_via_leite (0-100)
  - classe_risco (Baixo / Atenção / Alto / Crítico)
  - impacto_economico_estimado (R$)

Compatível com a base real gerada por gerador_leite_sintetico.py
(fact_producao_produtor_dia.csv) e com dados reais importados via
executar_piloto_real.py. Aliases de coluna garantem que os nomes do
schema real (temp_tanque_c, litros_descartados) sejam reconhecidos.

Uso:
    from score_risco import calcular_scores
    df_com_scores = calcular_scores(df)
    df_com_scores.to_csv("artefatos_teste/ranking_risco.csv", index=False)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# ------------------------------------------------------------------ #
# LIMIARES OPERACIONAIS — baseados em normas brasileiras              #
# IN 77/2018 MAPA e referências da cadeia leiteira goiana             #
# ------------------------------------------------------------------ #

LIMIAR = {
    # Qualidade
    "ccs_atencao": 400_000,    # cel/mL — limiar de atenção (IN 77)
    "ccs_alto": 600_000,       # cel/mL — alto risco de penalização
    "cbt_atencao": 100_000,    # UFC/mL — limiar de atenção
    "cbt_alto": 300_000,       # UFC/mL — alto risco
    "gordura_min": 3.0,        # % — abaixo indica problemas nutricionais
    "proteina_min": 2.9,       # %
    # Estresse térmico
    "thi_conforto": 68,        # THI ≤ 68: conforto
    "thi_atencao": 72,         # THI 69-72: estresse leve
    "thi_alto": 78,            # THI > 78: estresse severo
    # Temperatura do tanque
    "temp_tanque_max": 4.0,    # °C — acima há risco microbiológico
    "temp_tanque_critico": 6.0,
    # Produção
    "queda_producao_pct": 0.10,  # queda > 10% vs. média histórica = risco
    "queda_producao_critica": 0.20,
    # Logística
    "perda_logistica_pct": 0.05,  # > 5% de perda na rota
    # Econômico — preço referência leite premium Goiás
    "preco_litro_base": 2.80,   # R$/litro
    "bonus_qualidade": 0.15,    # R$/litro de bônus por qualidade A
    "penalidade_qualidade": 0.10,  # R$/litro de desconto por não-conformidade
}

# Pesos para composição do score (soma = 100)
PESOS_SCORE = {
    "risco_queda_producao": 25,
    "risco_qualidade":       20,
    "risco_ccs":             15,
    "risco_cbt":             15,
    "risco_temp_tanque":     10,
    "risco_perda_bonus":     10,
    "risco_descarte":         5,
}

# ------------------------------------------------------------------ #
# ALIASES DE COLUNA                                                   #
# Mapeia nomes do schema real (gerador_leite_sintetico.py) para os    #
# nomes canônicos usados pelas funções de risco. Esquerda = canônico, #
# direita = candidatos presentes na base real.                        #
# ------------------------------------------------------------------ #

ALIASES_COLUNA = {
    "temperatura_tanque": ["temp_tanque_c"],
    "volume_descartado":  ["litros_descartados"],
    "temp_media":         ["temp_med_c"],
}


def _normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas canônicas a partir dos nomes do schema real, sem
    sobrescrever colunas já existentes."""
    out = df.copy()
    for canonico, candidatos in ALIASES_COLUNA.items():
        if canonico in out.columns:
            continue
        for cand in candidatos:
            if cand in out.columns:
                out[canonico] = out[cand]
                break
    return out


# ------------------------------------------------------------------ #
# FUNÇÕES DE TARGET DERIVADO                                          #
# ------------------------------------------------------------------ #

def _risco_queda_producao(df: pd.DataFrame) -> pd.Series:
    """1 se produção cair > 10% vs. média histórica do produtor."""
    if "litros_coletados" not in df.columns:
        return pd.Series(0, index=df.index)

    col_prod = "litros_coletados"
    col_prod_media = "media_historica_litros"

    if col_prod_media not in df.columns:
        media = df.groupby("id_produtor")[col_prod].transform("mean")
    else:
        media = df[col_prod_media]

    queda = (media - df[col_prod]) / media.clip(lower=1)
    return (queda >= LIMIAR["queda_producao_pct"]).astype(int)


def _risco_qualidade(df: pd.DataFrame) -> pd.Series:
    """1 se CCS alto OU CBT alto OU gordura baixa."""
    flags = pd.Series(0, index=df.index)
    if "ccs" in df.columns:
        flags = flags | (df["ccs"] >= LIMIAR["ccs_atencao"]).astype(int)
    if "cbt" in df.columns:
        flags = flags | (df["cbt"] >= LIMIAR["cbt_atencao"]).astype(int)
    if "gordura_pct" in df.columns:
        flags = flags | (df["gordura_pct"] < LIMIAR["gordura_min"]).astype(int)
    return flags


def _risco_ccs(df: pd.DataFrame) -> pd.Series:
    if "ccs" not in df.columns:
        return pd.Series(0, index=df.index)
    return (df["ccs"] >= LIMIAR["ccs_atencao"]).astype(int)


def _risco_cbt(df: pd.DataFrame) -> pd.Series:
    if "cbt" not in df.columns:
        return pd.Series(0, index=df.index)
    return (df["cbt"] >= LIMIAR["cbt_atencao"]).astype(int)


def _risco_temp_tanque(df: pd.DataFrame) -> pd.Series:
    if "temperatura_tanque" not in df.columns:
        return pd.Series(0, index=df.index)
    return (df["temperatura_tanque"] > LIMIAR["temp_tanque_max"]).astype(int)


def _risco_perda_bonus(df: pd.DataFrame) -> pd.Series:
    """1 se CCS ou CBT acima do limiar alto → perda de bônus por qualidade."""
    flags = pd.Series(0, index=df.index)
    if "ccs" in df.columns:
        flags = flags | (df["ccs"] >= LIMIAR["ccs_alto"]).astype(int)
    if "cbt" in df.columns:
        flags = flags | (df["cbt"] >= LIMIAR["cbt_alto"]).astype(int)
    return flags


def _risco_descarte(df: pd.DataFrame) -> pd.Series:
    if "volume_descartado" not in df.columns:
        return pd.Series(0, index=df.index)
    if "litros_coletados" not in df.columns:
        return (df["volume_descartado"] > 0).astype(int)
    pct = df["volume_descartado"] / df["litros_coletados"].clip(lower=1)
    return (pct >= LIMIAR["perda_logistica_pct"]).astype(int)


# ------------------------------------------------------------------ #
# SCORE CONSOLIDADO VIA LEITE                                         #
# ------------------------------------------------------------------ #

def _calcular_score_bruto(df: pd.DataFrame) -> pd.Series:
    """
    Score de risco de 0 a 100.
    Quanto MAIOR o score, MAIOR o risco.
    Combina THI + targets binários ponderados.
    """
    score = pd.Series(0.0, index=df.index)

    for target, peso in PESOS_SCORE.items():
        col = f"target_{target}"
        if col in df.columns:
            score += df[col] * peso

    # Contribuição contínua do THI (0 a 15 pontos extras)
    if "thi" in df.columns:
        thi_norm = (df["thi"].clip(lower=LIMIAR["thi_conforto"],
                                   upper=LIMIAR["thi_alto"]) - LIMIAR["thi_conforto"])
        thi_range = LIMIAR["thi_alto"] - LIMIAR["thi_conforto"]
        score += (thi_norm / thi_range) * 15

    # Contribuição contínua da queda de produção (0 a 10 pontos extras)
    if "litros_coletados" in df.columns:
        media = df.groupby("id_produtor")["litros_coletados"].transform("mean") if "id_produtor" in df.columns \
            else df["litros_coletados"].mean()
        queda = ((media - df["litros_coletados"]) / media.clip(lower=1)).clip(lower=0, upper=0.5)
        score += (queda / 0.5) * 10

    return score.clip(lower=0, upper=100).round(1)


def _classificar_risco(score: pd.Series) -> pd.Series:
    bins = [-1, 25, 50, 75, 101]
    labels = ["Baixo risco", "Atenção", "Alto risco", "Crítico"]
    return pd.cut(score, bins=bins, labels=labels)


# ------------------------------------------------------------------ #
# IMPACTO ECONÔMICO ESTIMADO                                          #
# ------------------------------------------------------------------ #

def _calcular_impacto_economico(df: pd.DataFrame) -> pd.Series:
    """
    Estima perda financeira mensal em R$ por linha/produtor.
    Considera:
      - perda de volume por queda de produção
      - penalidade por não-conformidade de qualidade
      - perda de bônus por qualidade
    """
    impacto = pd.Series(0.0, index=df.index)

    preco = LIMIAR["preco_litro_base"]
    bonus = LIMIAR["bonus_qualidade"]
    penalidade = LIMIAR["penalidade_qualidade"]

    if "litros_coletados" in df.columns:
        litros = df["litros_coletados"].clip(lower=0)

        if "target_risco_queda_producao" in df.columns:
            # Estima 15% de queda média para produtores em risco
            impacto += df["target_risco_queda_producao"] * litros * 0.15 * preco * 30

        if "target_risco_perda_bonus" in df.columns:
            impacto += df["target_risco_perda_bonus"] * litros * bonus * 30

        if "target_risco_qualidade" in df.columns:
            impacto += df["target_risco_qualidade"] * litros * penalidade * 30

    return impacto.round(2)


# ------------------------------------------------------------------ #
# FUNÇÃO PRINCIPAL                                                     #
# ------------------------------------------------------------------ #

def calcular_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame da base operacional e retorna enriquecido com scores.

    Colunas adicionadas (quando dados disponíveis):
      target_risco_queda_producao  — binário
      target_risco_qualidade       — binário
      target_risco_ccs             — binário
      target_risco_cbt             — binário
      target_risco_temp_tanque     — binário
      target_risco_perda_bonus     — binário
      target_risco_descarte        — binário
      score_via_leite              — float 0-100
      classe_risco                 — categórico
      impacto_economico_estimado   — float R$
    """
    out = _normalizar_colunas(df)

    out["target_risco_queda_producao"] = _risco_queda_producao(out)
    out["target_risco_qualidade"]      = _risco_qualidade(out)
    out["target_risco_ccs"]            = _risco_ccs(out)
    out["target_risco_cbt"]            = _risco_cbt(out)
    out["target_risco_temp_tanque"]    = _risco_temp_tanque(out)
    out["target_risco_perda_bonus"]    = _risco_perda_bonus(out)
    out["target_risco_descarte"]       = _risco_descarte(out)

    out["score_via_leite"]           = _calcular_score_bruto(out)
    out["classe_risco"]              = _classificar_risco(out["score_via_leite"])
    out["impacto_economico_estimado"] = _calcular_impacto_economico(out)

    return out


def gerar_ranking_risco(df_com_scores: pd.DataFrame,
                        agrupar_por: str = "id_produtor") -> pd.DataFrame:
    """
    Agrega scores por produtor, rota ou laticínio e gera ranking descendente.

    Args:
        df_com_scores: DataFrame já processado por calcular_scores()
        agrupar_por: 'id_produtor' | 'id_rota' | 'id_laticinio'

    Returns:
        DataFrame com ranking de risco, prioridade de ação e impacto econômico.
    """
    if agrupar_por not in df_com_scores.columns:
        raise ValueError(f"Coluna '{agrupar_por}' não encontrada no DataFrame.")

    cols_targets = [c for c in df_com_scores.columns if c.startswith("target_risco_")]
    cols_agg = {
        "score_via_leite":             "mean",
        "impacto_economico_estimado":  "sum",
    }
    for c in cols_targets:
        cols_agg[c] = "mean"

    if "litros_coletados" in df_com_scores.columns:
        cols_agg["litros_coletados"] = "mean"

    ranking = (
        df_com_scores
        .groupby(agrupar_por)
        .agg(cols_agg)
        .reset_index()
        .sort_values("score_via_leite", ascending=False)
        .reset_index(drop=True)
    )

    ranking["score_via_leite"] = ranking["score_via_leite"].round(1)
    ranking["impacto_economico_estimado"] = ranking["impacto_economico_estimado"].round(2)
    ranking["classe_risco"] = _classificar_risco(ranking["score_via_leite"])
    ranking["prioridade_acao"] = ranking.index + 1  # 1 = mais urgente

    return ranking


def exportar_artefato_ranking(df: pd.DataFrame,
                               output_dir: str = "artefatos_teste") -> None:
    """Exporta CSVs de ranking por produtor, rota e laticínio."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    df_scores = calcular_scores(df)

    for dim, col in [
        ("produtor",  "id_produtor"),
        ("rota",      "id_rota"),
        ("laticinio", "id_laticinio"),
    ]:
        if col in df.columns:
            ranking = gerar_ranking_risco(df_scores, agrupar_por=col)
            path = os.path.join(output_dir, f"ranking_risco_{dim}.csv")
            ranking.to_csv(path, index=False)
            print(f"[VIA LEITE] Ranking exportado: {path}")


if __name__ == "__main__":
    # Teste rápido com dados sintéticos mínimos
    np.random.seed(42)
    n = 200
    demo = pd.DataFrame({
        "id_produtor":      [f"P{i:03d}" for i in np.random.randint(1, 21, n)],
        "id_rota":          [f"R{i:02d}" for i in np.random.randint(1, 6, n)],
        "id_laticinio":     ["LAT_DEMO"] * n,
        "litros_coletados": np.random.normal(450, 80, n).clip(100),
        "ccs":              np.random.lognormal(12.5, 0.6, n),
        "cbt":              np.random.lognormal(10.5, 0.8, n),
        "gordura_pct":      np.random.normal(3.5, 0.4, n).clip(2.5, 5.0),
        "temp_tanque_c":    np.random.normal(3.5, 1.2, n).clip(1.0, 8.0),
        "thi":              np.random.normal(71, 6, n).clip(55, 85),
        "litros_descartados": np.random.exponential(10, n).clip(0),
    })

    resultado = calcular_scores(demo)
    print("\n--- Score VIA LEITE — amostra ---")
    print(resultado[["id_produtor", "score_via_leite", "classe_risco",
                      "impacto_economico_estimado"]].head(10).to_string(index=False))

    exportar_artefato_ranking(demo, output_dir="artefatos_teste")
    print("\nConcluído.")
