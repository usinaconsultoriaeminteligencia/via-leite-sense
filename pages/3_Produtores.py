from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, carregar_contexto
from fornecedor_inteligencia import calcular_scores_fornecedores

st.title("Fazendas e Qualidade Premium")
st.caption("Priorizacao de fazendas por risco de volume, qualidade, logistica, continuidade e potencial para produtos premium.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

if ctx.prod_f.empty:
    st.warning("Sem dados de produção para os filtros atuais.")
    st.stop()

resumo_prod = calcular_scores_fornecedores(ctx.prod_f, ctx.dim_prod, ctx.pred_f)
top_risco = resumo_prod.head(50)

p1, p2 = st.columns(2)
fig5 = px.box(
    resumo_prod,
    x="tipo_sistema",
    y="litros_coletados_media",
    title="Captação média por tipo de sistema",
)
fig5 = aplicar_layout_plotly(fig5)
p1.plotly_chart(fig5, use_container_width=True)

fig6 = px.scatter(
    top_risco,
    x="score_qualidade",
    y="score_volume",
    size="litros_coletados_media",
    color="classe_risco",
    hover_name="id_produtor",
    title="Foco em qualidade e volume - Top 50 por risco",
    color_discrete_map={"Alto": "#B42318", "Medio": "#B54708", "Baixo": "#027A48"},
)
fig6 = aplicar_layout_plotly(fig6)
p2.plotly_chart(fig6, use_container_width=True)

st.subheader("Lista prioritária para ação")
cols = [
    "id_produtor",
    "id_laticinio",
    "municipio",
    "tipo_sistema",
    "nivel_tecnificacao",
    "litros_coletados_media",
    "score_risco_fornecedor",
    "classe_risco",
    "tendencia_volume_pct",
    "taxa_descarte_pct",
    "ccs_media",
    "cbt_media",
    "recomendacao",
]
cols = [c for c in cols if c in top_risco.columns]
st.dataframe(
    top_risco[cols],
    use_container_width=True,
    hide_index=True,
    column_config={
        "score_risco_fornecedor": st.column_config.ProgressColumn("Score de risco", min_value=0, max_value=100),
        "litros_coletados_media": st.column_config.NumberColumn("Litros por dia", format="%.2f"),
        "tendencia_volume_pct": st.column_config.NumberColumn("Tendência (%)", format="%.2f"),
        "taxa_descarte_pct": st.column_config.NumberColumn("Descarte (%)", format="%.2f"),
        "ccs_media": st.column_config.NumberColumn("CCS média", format="%.2f"),
        "cbt_media": st.column_config.NumberColumn("CBT média", format="%.2f"),
    },
)
