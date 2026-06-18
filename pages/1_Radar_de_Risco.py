"""
pages/1_Radar_de_Risco.py — VIA LEITE SENSE Sprint 4
Página executiva principal: Radar de Risco Produtivo, Qualidade e Rentabilidade.

Substitui o posicionamento anterior centrado em descarte.
Nova premissa: antecipar queda de produção, perda de qualidade,
risco de penalização/bônus e necessidade de ação preventiva.

Compatível com auth.py e o schema real (fact_producao_produtor_dia.csv).
"""

import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Compatibilidade com estrutura do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from auth import requer_autenticacao
    requer_autenticacao()
except ImportError:
    pass  # Fallback se auth não disponível

try:
    from score_risco import calcular_scores, gerar_ranking_risco, LIMIAR
except ImportError:
    st.error("⚠️ Arquivo score_risco.py não encontrado. Copie-o para a raiz do projeto.")
    st.stop()

# ------------------------------------------------------------------ #
# CONFIGURAÇÃO                                                         #
# ------------------------------------------------------------------ #

st.set_page_config(
    page_title="Radar de Risco — VIA LEITE SENSE",
    page_icon="🎯",
    layout="wide",
)

CORES_RISCO = {
    "Baixo risco": "#22c55e",
    "Atenção":     "#f59e0b",
    "Alto risco":  "#ef4444",
    "Crítico":     "#7c3aed",
}

# ------------------------------------------------------------------ #
# CARREGAMENTO DE DADOS                                                #
# ------------------------------------------------------------------ #

@st.cache_data(ttl=300, show_spinner="Calculando scores de risco...")
def carregar_e_calcular(data_dir: str) -> pd.DataFrame:
    """Carrega base operacional real e aplica motor de scoring."""
    caminho = os.path.join(data_dir, "fact_producao_produtor_dia.csv")
    if not os.path.exists(caminho):
        return pd.DataFrame()

    df = pd.read_csv(caminho, parse_dates=["data"], low_memory=False)

    # Integrar clima por dia e polo climático (evita produto cartesiano)
    caminho_clima = os.path.join(data_dir, "fact_clima_diario.csv")
    if os.path.exists(caminho_clima) and "polo_climatico" in df.columns:
        clima = pd.read_csv(caminho_clima, parse_dates=["data"])
        cols_clima = [c for c in ["data", "polo_climatico", "thi", "temp_med_c"] if c in clima.columns]
        df = df.merge(clima[cols_clima], on=["data", "polo_climatico"], how="left")

    return calcular_scores(df)


DATA_DIR = os.environ.get("MVP_DATA_DIR", "dados_teste")
df_full = carregar_e_calcular(DATA_DIR)

if df_full.empty:
    st.warning("⚠️ Base de dados não encontrada. Execute `gerador_leite_sintetico.py` primeiro.")
    st.info("```bash\npython gerador_leite_sintetico.py --output-dir dados_teste\n```")
    st.stop()


# ------------------------------------------------------------------ #
# SIDEBAR — FILTROS                                                    #
# ------------------------------------------------------------------ #

with st.sidebar:
    st.markdown("### 🎯 Radar de Risco")
    st.caption("Filtre por período, rota ou produtor")

    # Filtro de período
    if "data" in df_full.columns:
        data_min = df_full["data"].min().date()
        data_max = df_full["data"].max().date()
        periodo = st.date_input(
            "Período de análise",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
        )
        if len(periodo) == 2:
            df = df_full[
                (df_full["data"].dt.date >= periodo[0]) &
                (df_full["data"].dt.date <= periodo[1])
            ]
        else:
            df = df_full.copy()
    else:
        df = df_full.copy()

    # Filtro de rota
    if "id_rota" in df.columns:
        rotas = ["Todas"] + sorted(df["id_rota"].dropna().unique().tolist())
        rota_sel = st.selectbox("Rota", rotas)
        if rota_sel != "Todas":
            df = df[df["id_rota"] == rota_sel]

    # Filtro de classe de risco
    classes = ["Todas", "Crítico", "Alto risco", "Atenção", "Baixo risco"]
    classe_sel = st.selectbox("Classe de risco", classes)
    if classe_sel != "Todas" and "classe_risco" in df.columns:
        df = df[df["classe_risco"] == classe_sel]

    st.divider()
    st.caption(f"📊 {len(df):,} registros no período selecionado")


# ------------------------------------------------------------------ #
# HEADER                                                               #
# ------------------------------------------------------------------ #

st.markdown("""
<style>
.risco-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    border-left: 4px solid;
    margin-bottom: 0.5rem;
}
.metrica-label { font-size: 0.78rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
.metrica-valor { font-size: 2rem; font-weight: 700; line-height: 1.1; }
.metrica-delta { font-size: 0.82rem; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🎯 Radar de Risco Produtivo, Qualidade e Rentabilidade")
st.caption(
    "Antecipação de queda de produção, perda de qualidade, risco de penalização/bônus "
    "e necessidade de ação preventiva — VIA LEITE SENSE"
)
st.divider()


# ------------------------------------------------------------------ #
# KPIs DE ALERTA — LINHA 1                                            #
# ------------------------------------------------------------------ #

def _pct_risco(col: str) -> float:
    if col not in df.columns or len(df) == 0:
        return 0.0
    return round(df[col].mean() * 100, 1)

def _n_criticos() -> int:
    if "classe_risco" not in df.columns:
        return 0
    return int((df["classe_risco"] == "Crítico").sum())

def _impacto_total() -> float:
    if "impacto_economico_estimado" not in df.columns:
        return 0.0
    return df["impacto_economico_estimado"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    v = _pct_risco("target_risco_queda_producao")
    delta_cor = "🔴" if v > 30 else "🟡" if v > 15 else "🟢"
    st.metric("⚠️ Risco de queda de produção", f"{v}%", delta=f"{delta_cor} dos produtores")

with col2:
    v = _pct_risco("target_risco_qualidade")
    delta_cor = "🔴" if v > 25 else "🟡" if v > 10 else "🟢"
    st.metric("🧪 Risco de perda de qualidade", f"{v}%", delta=f"{delta_cor} dos registros")

with col3:
    v = _pct_risco("target_risco_perda_bonus")
    delta_cor = "🔴" if v > 20 else "🟡" if v > 8 else "🟢"
    st.metric("💰 Risco de perda de bônus", f"{v}%", delta=f"{delta_cor} dos registros")

with col4:
    n = _n_criticos()
    st.metric("🚨 Situações Críticas", str(n), delta="Ação imediata" if n > 0 else "Nenhuma crítica")

with col5:
    impacto = _impacto_total()
    st.metric("💸 Impacto econômico estimado",
              f"R$ {impacto:,.0f}",
              delta="Perda potencial mensal")

st.divider()


# ------------------------------------------------------------------ #
# LINHA 2 — SCORE MÉDIO + DISTRIBUIÇÃO DE CLASSE                     #
# ------------------------------------------------------------------ #

col_gauge, col_dist = st.columns([1, 1.8])

with col_gauge:
    if "score_via_leite" in df.columns and len(df) > 0:
        score_medio = df["score_via_leite"].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_medio,
            title={"text": "Score VIA LEITE<br><span style='font-size:0.8em'>Risco médio da carteira (0=mínimo, 100=máximo)</span>"},
            delta={"reference": 25, "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#3b82f6"},
                "steps": [
                    {"range": [0, 25],  "color": "#dcfce7"},
                    {"range": [25, 50], "color": "#fef9c3"},
                    {"range": [50, 75], "color": "#fee2e2"},
                    {"range": [75, 100],"color": "#f3e8ff"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 3},
                    "thickness": 0.8,
                    "value": 75,
                },
            },
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=60, b=10, l=20, r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

with col_dist:
    if "classe_risco" in df.columns and len(df) > 0:
        contagem = (
            df["classe_risco"]
            .value_counts()
            .reindex(["Crítico", "Alto risco", "Atenção", "Baixo risco"], fill_value=0)
            .reset_index()
        )
        contagem.columns = ["Classe", "Registros"]
        contagem["Cor"] = contagem["Classe"].map(CORES_RISCO)

        fig_bar = px.bar(
            contagem,
            x="Classe", y="Registros",
            color="Classe",
            color_discrete_map=CORES_RISCO,
            title="Distribuição por classe de risco",
            text="Registros",
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            showlegend=False,
            height=280,
            margin=dict(t=50, b=10, l=10, r=10),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.divider()


# ------------------------------------------------------------------ #
# LINHA 3 — MAPA DE CALOR DE RISCO POR INDICADOR                     #
# ------------------------------------------------------------------ #

st.markdown("### 📊 Mapa de Calor de Risco por Indicador")

targets_disponiveis = {
    "target_risco_queda_producao": "Queda de produção",
    "target_risco_qualidade":      "Perda de qualidade",
    "target_risco_ccs":            "CCS elevado",
    "target_risco_cbt":            "CBT elevado",
    "target_risco_temp_tanque":    "Temperatura tanque",
    "target_risco_perda_bonus":    "Perda de bônus",
    "target_risco_descarte":       "Descarte",
}

dim_col = None
for c in ["id_rota", "id_laticinio"]:
    if c in df.columns:
        dim_col = c
        break

if dim_col and any(t in df.columns for t in targets_disponiveis):
    cols_presentes = {k: v for k, v in targets_disponiveis.items() if k in df.columns}
    heatmap_data = (
        df.groupby(dim_col)[list(cols_presentes.keys())]
        .mean()
        .mul(100)
        .round(1)
    )
    heatmap_data.columns = list(cols_presentes.values())
    heatmap_data.index.name = dim_col.replace("id_", "").capitalize()

    fig_heat = px.imshow(
        heatmap_data,
        text_auto=".0f",
        color_continuous_scale=["#dcfce7", "#fef9c3", "#fee2e2", "#7c3aed"],
        aspect="auto",
        title=f"% de registros em risco — por {dim_col.replace('id_', '').capitalize()}",
        labels={"color": "% em risco"},
    )
    fig_heat.update_layout(height=350, margin=dict(t=50, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("Dados insuficientes para mapa de calor. Verifique se a base contém id_rota e indicadores de risco.")

st.divider()


# ------------------------------------------------------------------ #
# LINHA 4 — RANKING DE PRODUTORES / AÇÃO PREVENTIVA                  #
# ------------------------------------------------------------------ #

st.markdown("### 🚨 Ranking de Prioridade de Ação Preventiva")

dim_ranking = st.radio(
    "Agrupar ranking por:",
    ["Produtor", "Rota", "Laticínio"],
    horizontal=True,
    key="dim_ranking_radar",
)

dim_map = {"Produtor": "id_produtor", "Rota": "id_rota", "Laticínio": "id_laticinio"}
col_dim = dim_map[dim_ranking]

if col_dim in df.columns and "score_via_leite" in df.columns:
    ranking = gerar_ranking_risco(df, agrupar_por=col_dim)

    cols_exibir = [col_dim, "score_via_leite", "classe_risco",
                   "impacto_economico_estimado", "prioridade_acao"]
    cols_exibir = [c for c in cols_exibir if c in ranking.columns]

    targets_no_ranking = [c for c in ranking.columns if c.startswith("target_risco_")]
    if targets_no_ranking:
        cols_exibir += targets_no_ranking[:4]  # Mostrar até 4 targets

    st.dataframe(
        ranking[cols_exibir].head(20),
        use_container_width=True,
        column_config={
            "score_via_leite": st.column_config.ProgressColumn(
                "Score VIA LEITE", min_value=0, max_value=100, format="%.1f"
            ),
            "impacto_economico_estimado": st.column_config.NumberColumn(
                "Impacto Est. (R$/mês)", format="R$ %.0f"
            ),
            "prioridade_acao": st.column_config.NumberColumn("Prioridade", format="%d"),
        },
    )

    # Download do ranking
    csv_ranking = ranking.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Exportar ranking completo (CSV)",
        data=csv_ranking,
        file_name=f"ranking_risco_{col_dim.replace('id_', '')}.csv",
        mime="text/csv",
    )
else:
    st.info(f"Coluna '{col_dim}' não encontrada na base de dados.")

st.divider()


# ------------------------------------------------------------------ #
# LINHA 5 — HORIZONTE TEMPORAL DE RISCO (7 / 15 / 30 dias)           #
# ------------------------------------------------------------------ #

st.markdown("### 📅 Horizonte de Risco — 7, 15 e 30 dias")
st.caption(
    "Estimativa de exposição ao risco com base na tendência recente dos indicadores. "
    "Quanto maior o score médio das últimas semanas, maior a probabilidade de evento adverso."
)

if "data" in df.columns and "score_via_leite" in df.columns:
    hoje = df["data"].max()
    horizontes = {"7 dias": 7, "15 dias": 15, "30 dias": 30}

    cols_horiz = st.columns(3)
    for i, (label, dias) in enumerate(horizontes.items()):
        corte = hoje - pd.Timedelta(days=dias)
        subset = df[df["data"] >= corte]
        if len(subset) > 0:
            score_h = subset["score_via_leite"].mean()
            n_criticos_h = int((subset.get("classe_risco", pd.Series()) == "Crítico").sum())
            impacto_h = subset.get("impacto_economico_estimado", pd.Series(0)).sum()
            classe_h = "🟢" if score_h < 25 else "🟡" if score_h < 50 else "🔴" if score_h < 75 else "🟣"
            with cols_horiz[i]:
                st.metric(
                    f"{classe_h} Próximos {label}",
                    f"Score {score_h:.1f}",
                    delta=f"{n_criticos_h} críticos | R$ {impacto_h:,.0f} em risco",
                )
else:
    st.info("Coluna 'data' não disponível para análise temporal.")

st.divider()
st.caption("VIA LEITE SENSE — Radar de Risco Produtivo, Qualidade e Rentabilidade | USINA I.A. © 2026")
