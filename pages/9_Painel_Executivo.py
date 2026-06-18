from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from auth import requer_autenticacao, renderizar_sidebar_usuario
from dashboard_common import formatar_numero_br
from via_leite_edge import EDGE_DISCLAIMER, gerar_alertas, obter_provider_iot, resumo_premium

requer_autenticacao()
renderizar_sidebar_usuario()

st.title("Painel Executivo VIA LEITE SENSE")
st.caption("Monitoramento inteligente da produção leiteira para produtos premium, com IA preditiva, clima, ESG e telemetria IoT-ready.")
st.warning("Dados simulados para demonstração de conceito e validação de arquitetura IoT.")
st.caption("A plataforma transforma dados da fazenda em inteligência operacional para elevar a qualidade do leite destinado a derivados premium.")

provider = obter_provider_iot()
leituras_obj = provider.get_latest_readings()
leituras = [{**item.to_dict(), **resumo_premium(item)} for item in leituras_obj]
alertas = [alerta.to_dict() for leitura in leituras_obj for alerta in gerar_alertas(leitura)]

if not leituras:
    st.warning("Sem leituras EDGE para o painel executivo.")
    st.stop()

df = pd.DataFrame(leituras)
df_alertas = pd.DataFrame(alertas).drop_duplicates(subset=["id"]) if alertas else pd.DataFrame()
df["sensor_status"] = df["premium_quality_score"].apply(lambda valor: "ONLINE" if valor >= 65 else "ATENÇÃO")
df["esg_signal"] = 100.0 - (100.0 - df["conservation_index"]) * 0.75

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Fazendas monitoradas", len(df), "Sensores virtuais ativos")
k2.metric("Status dos sensores", int((df["sensor_status"] == "ONLINE").sum()), "Fazendas com telemetria estável")
k3.metric("Score premium", formatar_numero_br(df["premium_quality_score"].mean(), 1), "Leite apto para cadeia premium")
k4.metric("Risco térmico crítico", int((df["thermal_stress_risk"] == "CRITICO").sum()), "Risco de estresse térmico elevado")
k5.metric("Redução potencial de perdas", f"{formatar_numero_br((100.0 - df['conservation_index']).clip(lower=0).sum() * 3.2, 0)} L", "Risco de perda reduzido pela IA preditiva")

mapa, indicadores = st.columns([1.05, 0.95])
with mapa:
    fig = px.scatter_geo(
        df,
        lat="gps_lat",
        lon="gps_lng",
        color="collection_priority",
        size="milk_volume_liters",
        hover_name="farm_name",
        hover_data=["premium_message", "premium_quality_score", "thermal_stress_risk", "milk_quality_risk"],
        title="Mapa de fazendas e prioridade logística",
        color_discrete_map={"ALTA": "#B42318", "MEDIA": "#B54708", "BAIXA": "#027A48"},
    )
    st.plotly_chart(fig, use_container_width=True)

with indicadores:
    st.subheader("Mensagens inteligentes")
    mensagens = []
    if (df["thermal_stress_risk"] == "CRITICO").any():
        mensagens.append("Risco de estresse térmico elevado")
    if (df["milk_quality_risk"] == "ALTO").any():
        mensagens.append("Qualidade do leite impactada pela temperatura")
    if (df["premium_suitability"] == "ALTA").any():
        mensagens.append("Leite apto para cadeia premium")
    if (df["collection_priority"] == "ALTA").any():
        mensagens.append("Prioridade alta de coleta")
    mensagens.append("Risco de perda reduzido pela IA preditiva")
    for mensagem in mensagens:
        st.markdown(f"- {mensagem}")

    st.subheader("Indicadores ESG")
    st.write(f"Score ESG sintético: **{formatar_numero_br(df['esg_signal'].mean(), 1)}**")
    st.write("Rastreabilidade: sensores virtuais, clima, qualidade e prioridade de coleta integrados em uma única camada.")
    st.write("Sustentabilidade: menor descarte, melhor conservação e menos deslocamento reativo.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Qualidade do leite e cadeia premium")
    fig_quality = px.scatter(
        df,
        x="thermal_stability_score",
        y="premium_quality_score",
        size="milk_volume_liters",
        color="premium_suitability",
        hover_name="farm_name",
        title="Qualidade premium × estabilidade térmica",
        color_discrete_map={"ALTA": "#087443", "MODERADA": "#A75C12", "LIMITADA": "#B42318"},
    )
    st.plotly_chart(fig_quality, use_container_width=True)

with col2:
    st.subheader("Alertas críticos")
    if df_alertas.empty:
        st.success("Sem alertas críticos no snapshot atual.")
    else:
        st.dataframe(
            df_alertas[["severity", "farm_id", "message", "recommended_action"]],
            use_container_width=True,
            hide_index=True,
        )

st.caption(EDGE_DISCLAIMER)
