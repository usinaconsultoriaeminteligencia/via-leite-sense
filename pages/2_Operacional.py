from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, carregar_contexto

st.title("Operacional - Eficiencia, Coleta e Conservacao")
st.caption("Rotas, tanques e logistica leiteira para reduzir perdas e proteger a cadeia premium.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

if ctx.rota_f.empty:
    st.warning("Sem dados de rota para os filtros atuais.")
    st.stop()

c1, c2 = st.columns(2)
resumo_rota = ctx.rota_f.groupby("id_rota", as_index=False).agg(
    litros_realizados=("litros_realizados", "mean"),
    ocupacao_tanque_pct=("ocupacao_tanque_pct", "mean"),
    indice_atraso=("indice_atraso", "mean"),
    indice_perda_rota=("indice_perda_rota", "mean"),
)
fig = px.scatter(
    resumo_rota,
    x="ocupacao_tanque_pct",
    y="indice_perda_rota",
    size="litros_realizados",
    hover_name="id_rota",
    title="Rotas - Ocupação do tanque × índice de perda",
)
fig = aplicar_layout_plotly(fig)
c1.plotly_chart(fig, use_container_width=True)

resumo_lac = ctx.rota_f.groupby("id_laticinio", as_index=False).agg(
    litros_realizados=("litros_realizados", "sum"),
    custo_total=("custo_total", "sum"),
    km_rodados=("km_rodados", "sum"),
)
resumo_lac["custo_por_litro"] = resumo_lac["custo_total"] / resumo_lac["litros_realizados"].replace(0, pd.NA)
fig2 = px.bar(resumo_lac, x="id_laticinio", y="custo_por_litro", title="Custo logístico por litro (agregado)")
fig2 = aplicar_layout_plotly(fig2)
c2.plotly_chart(fig2, use_container_width=True)

st.subheader("Ranking de rotas por perda")
st.dataframe(
    resumo_rota.sort_values("indice_perda_rota", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "litros_realizados": st.column_config.NumberColumn("Litros realizados", format="%.2f"),
        "ocupacao_tanque_pct": st.column_config.NumberColumn("Ocupação do tanque (%)", format="%.2f"),
        "indice_atraso": st.column_config.NumberColumn("Índice de atraso", format="%.2f"),
        "indice_perda_rota": st.column_config.NumberColumn("Índice de perda da rota", format="%.2f"),
    },
)
