from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard_common import PAGE_CONFIG, aplicar_layout_plotly, carregar_contexto, formatar_numero_br

st.set_page_config(**PAGE_CONFIG)

st.title("VIA LEITE SENSE")
st.subheader("Monitoramento Inteligente da Produção Leiteira para Produtos Premium")
st.caption("Plataforma para fazenda, sensor e cadeia premium: IA preditiva, clima, rastreabilidade e telemetria IoT-ready.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.info(
        "Garanta que existem `dados_teste/` e `artefatos_teste/` "
        "(ou defina as variáveis `MVP_DATA_DIR` e `MVP_ARTEFATOS_DIR`). "
        "Depois execute `python treino_mvp_avancado.py`."
    )
    st.stop()

mt = ctx.metricas["metricas_teste_modelo"]
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("RMSE (teste)", formatar_numero_br(mt["rmse"], 2))
col2.metric("MAE (teste)", formatar_numero_br(mt["mae"], 2))
col3.metric("R² (teste)", formatar_numero_br(mt["r2"], 3))
col4.metric("sMAPE (teste)", f"{formatar_numero_br(mt['smape_pct'], 2)}%")
col5.metric("Registros no teste", formatar_numero_br(ctx.metricas["teste_linhas"], 0))

st.divider()

st.markdown(
    """
**Navegação** - Use o menu da barra lateral para abrir cada área:

| Seção | Conteúdo |
|--------|----------|
| **Visão Executiva** | IA preditiva para risco, variáveis críticas e proteção da cadeia leiteira |
| **Operacional** | Rotas, tanque, custo por litro e redução de perdas |
| **Fazendas e Qualidade Premium** | Qualidade do leite, risco e adequação para derivados premium |
| **Clima** | Chuva, THI, estresse térmico e sensibilidade da fazenda |
| **Gestão e Dados** | Cadastro de fazendas, lançamentos e onboarding de pilotos |
| **Fazenda 360** | Risco, qualidade, continuidade e leitura de produção por fazenda |
| **VIA LEITE EDGE** | Sensores virtuais, prioridade de coleta e score premium |
| **Painel Executivo VIA LEITE SENSE** | Mapa de fazendas, status dos sensores, ESG e narrativa para pitch |
"""
)

if not ctx.pred_f.empty:
    st.subheader("Leitura Executiva da Produção")
    serie = ctx.pred_f.groupby("data", as_index=False).agg(
        y_real=("y_real", "mean"),
        y_pred=("y_pred_modelo", "mean"),
    )
    fig = px.line(serie, x="data", y=["y_real", "y_pred"], title="Realizado × Previsto")
    aplicar_layout_plotly(fig)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum registro de previsão após aplicar os filtros. Amplie o período ou redefina laticínios e polos.")

st.divider()
st.info("Dados simulados para demonstração de conceito e validação de arquitetura IoT.")
st.caption("O VIA LEITE SENSE transforma dados da fazenda em inteligência operacional para elevar a qualidade do leite destinado a derivados premium.")
st.caption("Comando recomendado: `streamlit run via_leite_sense.py`")
