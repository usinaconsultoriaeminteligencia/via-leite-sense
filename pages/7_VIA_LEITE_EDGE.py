from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, formatar_numero_br
from via_leite_edge import EDGE_DISCLAIMER, EdgeSettings, carregar_configuracao_edge, gerar_alertas, obter_provider_iot, resumo_premium

st.title("VIA LEITE EDGE - Monitoramento IoT-ready")
st.caption("Telemetria sintética para monitorar fazendas, sensores virtuais, risco térmico, coleta e qualidade do leite para cadeias premium.")

st.markdown(
    """
    <div style="margin: 0 0 16px 0; padding: 12px 16px; border-radius: 12px; border: 1px solid #b9ddcf; background: #eefaf4; color: #0f5132; font-weight: 700;">
      Dados simulados para demonstração de conceito e validação de arquitetura IoT.
    </div>
    """,
    unsafe_allow_html=True,
)
st.info(EDGE_DISCLAIMER)

try:
    settings = carregar_configuracao_edge()
    provider = obter_provider_iot(settings)
    leituras_obj = provider.get_latest_readings()
    readings = [{**item.to_dict(), **resumo_premium(item)} for item in leituras_obj]
    alertas = [alerta.to_dict() for leitura in leituras_obj for alerta in gerar_alertas(leitura)]
except NotImplementedError:
    fallback_settings = EdgeSettings(
        simulation_mode=True,
        provider_name="simulated",
        sample_size=settings.sample_size,
        data_dir=settings.data_dir,
    )
    provider = obter_provider_iot(fallback_settings)
    leituras_obj = provider.get_latest_readings()
    readings = [{**item.to_dict(), **resumo_premium(item)} for item in leituras_obj]
    alertas = [alerta.to_dict() for leitura in leituras_obj for alerta in gerar_alertas(leitura)]
    st.warning("Provider IoT real ainda não implementado. A visualização foi mantida em modo simulado.")
except Exception as exc:
    st.warning("A camada EDGE não conseguiu carregar leituras. O dashboard entrou em fallback seguro.")
    st.code(str(exc))
    readings = []
    alertas = []

if not readings:
    st.warning("Nenhuma leitura simulada disponível no momento.")
    st.stop()

df = pd.DataFrame(readings)
df_alertas = pd.DataFrame(alertas).drop_duplicates(subset=["id"]) if alertas else pd.DataFrame(
    columns=["id", "farm_id", "severity", "message", "created_at", "recommended_action", "source"]
)

ordem_prioridade = {"ALTA": 0, "MEDIA": 1, "BAIXA": 2}
ordem_risco = {"CRITICO": 0, "ALTO": 1, "MEDIO": 2, "BAIXO": 3}
df["priority_order"] = df["collection_priority"].map(ordem_prioridade).fillna(9)
df["thermal_order"] = df["thermal_stress_risk"].map(ordem_risco).fillna(9)
df["quality_order"] = df["milk_quality_risk"].map(ordem_risco).fillna(9)
df = df.sort_values(["priority_order", "quality_order", "thermal_order", "tank_temperature_c"], ascending=[True, True, True, False])

top = df.iloc[0]
volume_total = float(df["milk_volume_liters"].sum())
ocupacao_media = float(df["volume_pct"].mean())
thi_max = float(df["thi"].max())
premium_medio = float(df["premium_quality_score"].mean())
estabilidade_media = float(df["thermal_stability_score"].mean())

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Temperatura do tanque", f"{formatar_numero_br(top['tank_temperature_c'], 1)} °C", top["milk_quality_risk"])
c2.metric("Volume monitorado", f"{formatar_numero_br(volume_total, 0)} L", f"{formatar_numero_br(ocupacao_media, 1)}% de ocupação média")
c3.metric("THI máximo", formatar_numero_br(thi_max, 1), f"{int((df['thermal_stress_risk'] == 'CRITICO').sum())} fazendas críticas")
c4.metric("Risco térmico", f"{int((df['thermal_stress_risk'].isin(['ALTO', 'CRITICO'])).sum())} ativos", "Risco de estresse térmico elevado")
c5.metric("Score premium", formatar_numero_br(premium_medio, 1), "Qualidade premium do leite")
c6.metric("Estabilidade térmica", formatar_numero_br(estabilidade_media, 1), "Conservação da cadeia fria")

st.markdown(
    "A qualidade do leite impacta diretamente a produção de derivados premium e produtos de maior valor agregado, "
    "como chocolates artesanais, sobremesas especiais e linhas lácteas premium."
)

col_a, col_b = st.columns([1.1, 0.9])

with col_a:
    st.subheader("Ranking de fazendas por prioridade de coleta")
    st.dataframe(
        df[
            [
                "farm_id",
                "farm_name",
                "tank_temperature_c",
                "milk_volume_liters",
                "tank_capacity_liters",
                "volume_pct",
                "thi",
                "premium_quality_score",
                "premium_suitability",
                "collection_priority",
                "premium_message",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "tank_temperature_c": st.column_config.NumberColumn("Temp. tanque (°C)", format="%.1f"),
            "milk_volume_liters": st.column_config.NumberColumn("Volume (L)", format="%.1f"),
            "tank_capacity_liters": st.column_config.NumberColumn("Capacidade (L)", format="%.1f"),
            "volume_pct": st.column_config.NumberColumn("Ocupação (%)", format="%.1f"),
            "thi": st.column_config.NumberColumn("THI", format="%.1f"),
            "premium_quality_score": st.column_config.ProgressColumn("Score premium", min_value=0, max_value=100),
        },
    )

with col_b:
    st.subheader("Mapa de pressão operacional")
    fig = px.scatter_geo(
        df,
        lat="gps_lat",
        lon="gps_lng",
        color="collection_priority",
        size="milk_volume_liters",
        hover_name="farm_name",
        hover_data=["farm_id", "premium_quality_score", "thermal_stress_risk", "premium_message"],
        title="Fazendas monitoradas por sensores virtuais",
        color_discrete_map={"ALTA": "#B42318", "MEDIA": "#B54708", "BAIXA": "#027A48"},
    )
    aplicar_layout_plotly(fig)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns([0.95, 1.05])
with left:
    st.subheader("Qualidade Premium")
    premium_mix = df.groupby("premium_suitability", as_index=False).agg(
        fazendas=("farm_id", "count"),
        score_medio=("premium_quality_score", "mean"),
    )
    fig_mix = px.bar(
        premium_mix,
        x="premium_suitability",
        y="fazendas",
        color="premium_suitability",
        text_auto=True,
        title="Adequação para derivados premium",
        color_discrete_map={"ALTA": "#087443", "MODERADA": "#A75C12", "LIMITADA": "#B42318"},
    )
    aplicar_layout_plotly(fig_mix)
    st.plotly_chart(fig_mix, use_container_width=True)
    st.caption("Dados simulados para demonstração de conceito e validação de arquitetura IoT.")

with right:
    st.subheader("Alertas ativos")
    if df_alertas.empty:
        st.success("Sem alertas ativos no snapshot atual.")
    else:
        st.dataframe(
            df_alertas[["severity", "farm_id", "message", "recommended_action", "created_at", "source"]],
            use_container_width=True,
            hide_index=True,
        )
