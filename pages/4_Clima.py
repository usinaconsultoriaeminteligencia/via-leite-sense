from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, carregar_contexto

st.title("Clima, THI e Estresse Termico")
st.caption("Leitura climatica para prevenir perdas, proteger a producao leiteira e sustentar derivados premium.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

if ctx.clima_f.empty or ctx.prod_f.empty:
    st.warning("Sem dados de clima ou produção para os filtros atuais.")
    st.stop()

clim1, clim2 = st.columns(2)
clima_sum = ctx.clima_f.groupby(["data", "polo_climatico"], as_index=False).agg(
    precip_mm=("precip_mm", "mean"),
    thi=("thi", "mean"),
    dias_sem_chuva=("dias_sem_chuva", "mean"),
)
fig7 = px.line(clima_sum, x="data", y="precip_mm", color="polo_climatico", title="Precipitação média por polo")
fig7 = aplicar_layout_plotly(fig7)
clim1.plotly_chart(fig7, use_container_width=True)

fig8 = px.line(clima_sum, x="data", y="thi", color="polo_climatico", title="THI médio por polo")
fig8 = aplicar_layout_plotly(fig8)
clim2.plotly_chart(fig8, use_container_width=True)

merged = ctx.prod_f.merge(
    ctx.clima_f[["data", "polo_climatico", "thi", "precip_15d", "dias_sem_chuva"]],
    on=["data", "polo_climatico"],
    how="left",
)
merged["perda_pct"] = (merged["litros_previstos"] - merged["litros_coletados"]) / merged["litros_previstos"].replace(0, pd.NA)
agg = merged.groupby("polo_climatico", as_index=False).agg(
    thi=("thi", "mean"),
    precip_15d=("precip_15d", "mean"),
    perda_pct=("perda_pct", "mean"),
)
fig9 = px.scatter(
    agg,
    x="thi",
    y="perda_pct",
    size="precip_15d",
    color="polo_climatico",
    title="Clima agregado × perda operacional média",
)
fig9 = aplicar_layout_plotly(fig9)
st.plotly_chart(fig9, use_container_width=True)
