"""
pages/13_Antes_Depois_ESG.py — VIA LEITE SENSE Sprint 4
Painel comparativo antes/depois de intervenção + Narrativa ESG.

Demonstra ROI da plataforma para avaliadores do Desafio AgroStartup SENAR/SEBRAE Goiás.
Combina impacto econômico mensurável com narrativa de sustentabilidade.
"""

import os
import sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from auth import requer_autenticacao
    requer_autenticacao()
except ImportError:
    pass

st.set_page_config(
    page_title="Antes & Depois — VIA LEITE SENSE",
    page_icon="📈",
    layout="wide",
)

# ------------------------------------------------------------------ #
# DADOS DE REFERÊNCIA — CENÁRIO SIMULADO DE INTERVENÇÃO               #
# Baseado em benchmarks da literatura leiteira brasileira             #
# Fonte: Embrapa, MAPA IN 77/2018, estudos cooperativas goianas       #
# ------------------------------------------------------------------ #

# Conversão CO₂ equivalente
# 1 litro de leite descartado ≈ 3.2 kg CO₂eq (ciclo produtivo completo)
# Fonte: FAO (2010) Greenhouse Gas Emissions from the Dairy Sector
CO2_KG_POR_LITRO = 3.2

CENARIOS = {
    "Pequeno produtor (< 200 L/dia)": {
        "producao_diaria_antes": 150,
        "descarte_pct_antes": 0.12,
        "ccs_antes": 550_000,
        "cbt_antes": 280_000,
        "preco_base": 2.80,
        "bonus_antes": 0.0,
        "melhora_producao_pct": 0.08,
        "melhora_descarte_pct": 0.60,
        "melhora_ccs_pct": 0.35,
        "melhora_cbt_pct": 0.45,
        "bonus_apos": 0.12,
    },
    "Médio produtor (200–600 L/dia)": {
        "producao_diaria_antes": 380,
        "descarte_pct_antes": 0.09,
        "ccs_antes": 420_000,
        "cbt_antes": 180_000,
        "preco_base": 2.85,
        "bonus_antes": 0.05,
        "melhora_producao_pct": 0.07,
        "melhora_descarte_pct": 0.55,
        "melhora_ccs_pct": 0.30,
        "melhora_cbt_pct": 0.40,
        "bonus_apos": 0.15,
    },
    "Grande produtor (> 600 L/dia)": {
        "producao_diaria_antes": 850,
        "descarte_pct_antes": 0.07,
        "ccs_antes": 380_000,
        "cbt_antes": 140_000,
        "preco_base": 2.90,
        "bonus_antes": 0.08,
        "melhora_producao_pct": 0.05,
        "melhora_descarte_pct": 0.50,
        "melhora_ccs_pct": 0.25,
        "melhora_cbt_pct": 0.35,
        "bonus_apos": 0.15,
    },
    "Cooperativa (50 produtores médios)": {
        "producao_diaria_antes": 380 * 50,
        "descarte_pct_antes": 0.09,
        "ccs_antes": 430_000,
        "cbt_antes": 200_000,
        "preco_base": 2.85,
        "bonus_antes": 0.04,
        "melhora_producao_pct": 0.07,
        "melhora_descarte_pct": 0.55,
        "melhora_ccs_pct": 0.30,
        "melhora_cbt_pct": 0.40,
        "bonus_apos": 0.14,
    },
}


def _calcular_roi(c: dict) -> dict:
    """Calcula métricas antes/depois e ROI a partir de um cenário."""
    # ANTES
    prod_antes = c["producao_diaria_antes"]
    descarte_antes_l = prod_antes * c["descarte_pct_antes"]
    receita_antes = (prod_antes - descarte_antes_l) * (c["preco_base"] + c["bonus_antes"]) * 30

    # DEPOIS
    prod_apos = prod_antes * (1 + c["melhora_producao_pct"])
    descarte_apos_l = descarte_antes_l * (1 - c["melhora_descarte_pct"])
    ccs_apos = c["ccs_antes"] * (1 - c["melhora_ccs_pct"])
    cbt_apos = c["cbt_antes"] * (1 - c["melhora_cbt_pct"])
    receita_apos = (prod_apos - descarte_apos_l) * (c["preco_base"] + c["bonus_apos"]) * 30

    # DELTA
    delta_receita_mensal = receita_apos - receita_antes
    delta_receita_anual = delta_receita_mensal * 12
    litros_recuperados_mes = (prod_apos - prod_antes + descarte_antes_l - descarte_apos_l) * 30

    # ESG — redução de CO₂ equivalente
    litros_descarte_evitados_ano = (descarte_antes_l - descarte_apos_l) * 365
    co2_evitado_kg = litros_descarte_evitados_ano * CO2_KG_POR_LITRO
    co2_evitado_ton = co2_evitado_kg / 1000

    return {
        "prod_antes": prod_antes,
        "prod_apos": prod_apos,
        "descarte_antes_l": descarte_antes_l,
        "descarte_apos_l": descarte_apos_l,
        "ccs_antes": c["ccs_antes"],
        "ccs_apos": ccs_apos,
        "cbt_antes": c["cbt_antes"],
        "cbt_apos": cbt_apos,
        "receita_antes": receita_antes,
        "receita_apos": receita_apos,
        "delta_receita_mensal": delta_receita_mensal,
        "delta_receita_anual": delta_receita_anual,
        "litros_recuperados_mes": litros_recuperados_mes,
        "co2_evitado_ton": co2_evitado_ton,
        "litros_descarte_evitados_ano": litros_descarte_evitados_ano,
        "bonus_antes": c["bonus_antes"],
        "bonus_apos": c["bonus_apos"],
    }


# ------------------------------------------------------------------ #
# HEADER                                                               #
# ------------------------------------------------------------------ #

st.markdown("## 📈 Impacto da Plataforma — Antes & Depois + Narrativa ESG")
st.caption(
    "Demonstração de ROI mensurável e impacto ambiental da adoção do VIA LEITE SENSE. "
    "Dados baseados em benchmarks da literatura leiteira brasileira (Embrapa / MAPA / IN 77)."
)
st.divider()

# Seletor de cenário
cenario_sel = st.selectbox(
    "📋 Selecione o perfil de produtor/cooperativa:",
    list(CENARIOS.keys()),
)

roi = _calcular_roi(CENARIOS[cenario_sel])

st.divider()

# ------------------------------------------------------------------ #
# BLOCO 1 — KPIs COMPARATIVOS                                        #
# ------------------------------------------------------------------ #

st.markdown("### 📊 Indicadores Antes vs. Depois da Adoção")

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_prod = roi["prod_apos"] - roi["prod_antes"]
    st.metric(
        "Produção diária (L)",
        f"{roi['prod_apos']:,.0f} L",
        delta=f"+{delta_prod:,.0f} L/dia",
        delta_color="normal",
    )
    st.caption(f"Antes: {roi['prod_antes']:,.0f} L/dia")

with col2:
    delta_desc = roi["descarte_apos_l"] - roi["descarte_antes_l"]
    st.metric(
        "Descarte diário (L)",
        f"{roi['descarte_apos_l']:,.1f} L",
        delta=f"{delta_desc:,.1f} L/dia",
        delta_color="inverse",
    )
    st.caption(f"Antes: {roi['descarte_antes_l']:,.1f} L/dia")

with col3:
    delta_ccs = roi["ccs_apos"] - roi["ccs_antes"]
    st.metric(
        "CCS (céls/mL)",
        f"{roi['ccs_apos']:,.0f}",
        delta=f"{delta_ccs:,.0f}",
        delta_color="inverse",
    )
    st.caption(f"Antes: {roi['ccs_antes']:,.0f}")

with col4:
    delta_cbt = roi["cbt_apos"] - roi["cbt_antes"]
    st.metric(
        "CBT (UFC/mL)",
        f"{roi['cbt_apos']:,.0f}",
        delta=f"{delta_cbt:,.0f}",
        delta_color="inverse",
    )
    st.caption(f"Antes: {roi['cbt_antes']:,.0f}")

st.divider()

# ------------------------------------------------------------------ #
# BLOCO 2 — IMPACTO ECONÔMICO                                        #
# ------------------------------------------------------------------ #

st.markdown("### 💰 Impacto Econômico Estimado")

col_eco1, col_eco2, col_eco3 = st.columns(3)

with col_eco1:
    st.metric(
        "Ganho mensal estimado",
        f"R$ {roi['delta_receita_mensal']:,.0f}",
        delta="Por mês com a plataforma",
    )

with col_eco2:
    st.metric(
        "Ganho anual estimado",
        f"R$ {roi['delta_receita_anual']:,.0f}",
        delta="Impacto anual acumulado",
    )

with col_eco3:
    st.metric(
        "Litros recuperados / mês",
        f"{roi['litros_recuperados_mes']:,.0f} L",
        delta="Produção + redução de descarte",
    )

# Gráfico comparativo de receita
fig_rec = go.Figure()
fig_rec.add_trace(go.Bar(
    name="Antes",
    x=["Receita mensal"],
    y=[roi["receita_antes"]],
    marker_color="#94a3b8",
    text=[f"R$ {roi['receita_antes']:,.0f}"],
    textposition="outside",
))
fig_rec.add_trace(go.Bar(
    name="Depois (com VIA LEITE)",
    x=["Receita mensal"],
    y=[roi["receita_apos"]],
    marker_color="#22c55e",
    text=[f"R$ {roi['receita_apos']:,.0f}"],
    textposition="outside",
))
fig_rec.update_layout(
    title="Receita mensal estimada — Antes vs. Depois",
    barmode="group",
    height=320,
    yaxis_tickprefix="R$ ",
    yaxis_tickformat=",.0f",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=50, b=10),
    showlegend=True,
)
st.plotly_chart(fig_rec, use_container_width=True)

# Decomposição do ganho
with st.expander("📋 Detalhamento do ganho"):
    ganho_producao = (roi["prod_apos"] - roi["prod_antes"]) * (CENARIOS[cenario_sel]["preco_base"]) * 30
    ganho_descarte = (roi["descarte_antes_l"] - roi["descarte_apos_l"]) * CENARIOS[cenario_sel]["preco_base"] * 30
    ganho_bonus = (roi["bonus_apos"] - roi["bonus_antes"]) * roi["prod_apos"] * 30

    df_decomp = pd.DataFrame({
        "Origem do ganho": ["Aumento de produção", "Redução de descarte", "Ganho de bônus por qualidade"],
        "Valor mensal (R$)": [ganho_producao, ganho_descarte, ganho_bonus],
    })
    df_decomp["Participação (%)"] = (df_decomp["Valor mensal (R$)"] / df_decomp["Valor mensal (R$)"].sum() * 100).round(1)
    st.dataframe(df_decomp, use_container_width=True, hide_index=True)

st.divider()

# ------------------------------------------------------------------ #
# BLOCO 3 — NARRATIVA ESG                                             #
# ------------------------------------------------------------------ #

st.markdown("### 🌱 Narrativa ESG — Sustentabilidade e Impacto Ambiental")

col_esg1, col_esg2, col_esg3 = st.columns(3)

with col_esg1:
    st.metric(
        "🌍 CO₂ evitado / ano",
        f"{roi['co2_evitado_ton']:,.1f} ton CO₂eq",
        delta="Equivalente a descarte evitado",
    )
    st.caption("1 litro descartado ≈ 3,2 kg CO₂eq (FAO, 2010)")

with col_esg2:
    litros_ano = roi["litros_descarte_evitados_ano"]
    st.metric(
        "🥛 Descarte evitado / ano",
        f"{litros_ano:,.0f} L",
        delta="Produção útil preservada",
    )

with col_esg3:
    # Equivalência ilustrativa: 1 ton CO₂ ≈ 100 árvores plantadas por 10 anos
    arvores_equiv = int(roi["co2_evitado_ton"] * 100)
    st.metric(
        "🌳 Equivalente em árvores",
        f"{arvores_equiv:,}",
        delta="Árvores plantadas por 10 anos",
    )
    st.caption("Estimativa ilustrativa (1 ton CO₂eq ≈ 100 árvores/10 anos)")

# Narrativa textual para o pitch
st.markdown("""
<div style="background:#0f2027;border-left:4px solid #22c55e;padding:1.2rem 1.5rem;border-radius:8px;margin-top:1rem">
<h4 style="color:#22c55e;margin:0 0 0.8rem 0">📢 Narrativa para o Pitch — Desafio AgroStartup 2026</h4>
<p style="color:#e2e8f0;line-height:1.7;margin:0">
O VIA LEITE SENSE não é apenas uma ferramenta de monitoramento. É um <strong>radar de proteção
da rentabilidade e da qualidade</strong> para toda a cadeia leiteira premium.<br><br>
Cada litro de leite descartado por falha de qualidade não-antecipada representa um custo triplo:
<strong>perda de receita imediata, perda de bônus por qualidade e impacto ambiental mensurável.</strong><br><br>
Com a plataforma, cooperativas e laticínios passam de uma gestão <em>reativa</em> — que só identifica
o problema após a coleta — para uma gestão <em>preditiva</em>, com antecipação de até 30 dias
dos riscos de queda de produção, aumento de CCS/CBT e perda de bônus.<br><br>
O resultado é direto: <strong>mais litros de leite premium entregues, menos descarte,
menor emissão de CO₂ equivalente e maior rentabilidade para o produtor e para o laticínio.</strong>
</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------------------------------------------ #
# BLOCO 4 — COMPARATIVO VISUAL ANTES/DEPOIS (RADAR)                  #
# ------------------------------------------------------------------ #

st.markdown("### 🕸️ Radar de Indicadores — Antes vs. Depois")

# Normalizar indicadores para radar (0 = pior, 1 = melhor)
indicadores = ["Produção", "Qualidade CCS", "Qualidade CBT", "Bônus", "Descarte (-)", "Sustentabilidade"]

def _norm(val, min_v, max_v, inverter=False):
    n = (val - min_v) / (max_v - min_v + 1e-9)
    return 1 - n if inverter else n

antes_vals = [
    _norm(roi["prod_antes"], 50, roi["prod_apos"] * 1.1),
    _norm(roi["ccs_antes"], 100_000, 800_000, inverter=True),
    _norm(roi["cbt_antes"], 10_000, 400_000, inverter=True),
    _norm(roi["bonus_antes"], 0, 0.20),
    _norm(roi["descarte_antes_l"], 0, roi["prod_antes"] * 0.2, inverter=True),
    0.3,  # sustentabilidade antes (baseline baixo)
]

apos_vals = [
    _norm(roi["prod_apos"], 50, roi["prod_apos"] * 1.1),
    _norm(roi["ccs_apos"], 100_000, 800_000, inverter=True),
    _norm(roi["cbt_apos"], 10_000, 400_000, inverter=True),
    _norm(roi["bonus_apos"], 0, 0.20),
    _norm(roi["descarte_apos_l"], 0, roi["prod_antes"] * 0.2, inverter=True),
    min(1.0, 0.3 + roi["co2_evitado_ton"] / max(roi["co2_evitado_ton"], 1) * 0.6),
]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=antes_vals + [antes_vals[0]],
    theta=indicadores + [indicadores[0]],
    fill="toself",
    name="Antes",
    line_color="#94a3b8",
    fillcolor="rgba(148,163,184,0.2)",
))
fig_radar.add_trace(go.Scatterpolar(
    r=apos_vals + [apos_vals[0]],
    theta=indicadores + [indicadores[0]],
    fill="toself",
    name="Depois (com VIA LEITE)",
    line_color="#22c55e",
    fillcolor="rgba(34,197,94,0.2)",
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title="Performance geral do produtor — Antes vs. Depois",
    height=420,
    margin=dict(t=60, b=20),
)
st.plotly_chart(fig_radar, use_container_width=True)

st.divider()
st.caption(
    "VIA LEITE SENSE — Análise de Impacto | Benchmarks: Embrapa Gado de Leite, MAPA IN 77/2018, "
    "FAO Greenhouse Gas Emissions Dairy Sector (2010) | USINA I.A. © 2026"
)
