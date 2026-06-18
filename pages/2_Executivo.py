from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, carregar_contexto, formatar_numero_br

st.title("Visão Executiva VIA LEITE SENSE")
st.caption("Desempenho do modelo, leitura de risco e inteligência para leite destinado a produtos premium.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

m = ctx.metricas["metricas_teste_modelo"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("RMSE (teste)", formatar_numero_br(m["rmse"], 2))
c2.metric("MAE (teste)", formatar_numero_br(m["mae"], 2))
c3.metric("R² (teste)", formatar_numero_br(m["r2"], 3))
c4.metric("sMAPE (teste)", f"{formatar_numero_br(m['smape_pct'], 2)}%")

st.divider()

if ctx.pred_f.empty:
    st.warning("Sem dados no intervalo e nos filtros selecionados.")
    st.stop()

col_a, col_b = st.columns(2)
serie = ctx.pred_f.groupby("data", as_index=False).agg(y_real=("y_real", "mean"), y_pred=("y_pred_modelo", "mean"))
fig = px.line(serie, x="data", y=["y_real", "y_pred"], title="Média diária - realizado × previsto para a cadeia premium")
fig = aplicar_layout_plotly(fig)
col_a.plotly_chart(fig, use_container_width=True)

erro_lac = ctx.pred_f.groupby("id_laticinio", as_index=False).agg(
    erro_abs_medio=("erro_abs_modelo", "mean"),
    y_real=("y_real", "mean"),
)
fig2 = px.bar(erro_lac, x="id_laticinio", y="erro_abs_medio", title="Erro absoluto médio por laticínio")
fig2 = aplicar_layout_plotly(fig2)
col_b.plotly_chart(fig2, use_container_width=True)

if not ctx.feat.empty:
    st.subheader("Principais variáveis do modelo")
    st.dataframe(ctx.feat.head(25), use_container_width=True, hide_index=True)
