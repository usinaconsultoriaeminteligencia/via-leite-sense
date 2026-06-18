from __future__ import annotations

import plotly.express as px
import streamlit as st

from dashboard_common import aplicar_layout_plotly, carregar_contexto, formatar_numero_br
from fornecedor_inteligencia import calcular_scores_fornecedores
from gestor_store import carregar_fornecedores
from relatorio_pdf import gerar_relatorio_produtor

st.title("Fazenda 360")
st.caption("Risco, qualidade, capacidade, continuidade e leitura premium por fazenda.")

try:
    ctx = carregar_contexto()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

scores = calcular_scores_fornecedores(ctx.prod_f, ctx.dim_prod, ctx.pred_f)

if scores.empty:
    st.warning("Sem fornecedores no intervalo e filtros selecionados.")
    st.stop()

alto = int((scores["classe_risco"] == "Alto").sum())
medio = int((scores["classe_risco"] == "Medio").sum())
baixo = int((scores["classe_risco"] == "Baixo").sum())
volume_risco = float(scores.loc[scores["classe_risco"].isin(["Alto", "Medio"]), "litros_coletados_media"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fornecedores críticos", alto)
c2.metric("Atenção", medio)
c3.metric("Monitorados", baixo)
c4.metric("Litros por dia em risco", formatar_numero_br(volume_risco, 0))

st.divider()

ranking_cols = [
    "id_produtor",
    "id_laticinio",
    "polo_climatico",
    "municipio",
    "porte_produtor",
    "score_risco_fornecedor",
    "classe_risco",
    "score_volume",
    "score_qualidade",
    "score_logistica",
    "score_continuidade",
    "tendencia_volume_pct",
    "taxa_descarte_pct",
    "ccs_media",
    "cbt_media",
    "recomendacao",
]
ranking_cols = [c for c in ranking_cols if c in scores.columns]

left, right = st.columns([1.15, 0.85])

with left:
    st.subheader("Prioridade de atuação")
    st.dataframe(
        scores[ranking_cols].head(50),
        use_container_width=True,
        hide_index=True,
        column_config={
            "score_risco_fornecedor": st.column_config.ProgressColumn(
                "Score de risco",
                help="0 = baixo risco, 100 = risco máximo relativo ao painel filtrado.",
                min_value=0,
                max_value=100,
            ),
            "score_volume": st.column_config.ProgressColumn("Volume", min_value=0, max_value=100),
            "score_qualidade": st.column_config.ProgressColumn("Qualidade", min_value=0, max_value=100),
            "score_logistica": st.column_config.ProgressColumn("Logística", min_value=0, max_value=100),
            "score_continuidade": st.column_config.ProgressColumn("Continuidade", min_value=0, max_value=100),
            "tendencia_volume_pct": st.column_config.NumberColumn("Tendência de volume (%)", format="%.2f"),
            "taxa_descarte_pct": st.column_config.NumberColumn("Descarte (%)", format="%.2f"),
            "ccs_media": st.column_config.NumberColumn("CCS média", format="%.2f"),
            "cbt_media": st.column_config.NumberColumn("CBT média", format="%.2f"),
        },
    )

with right:
    risco_mix = scores.groupby("classe_risco", as_index=False).agg(fornecedores=("id_produtor", "count"))
    ordem = {"Alto": 0, "Medio": 1, "Baixo": 2}
    risco_mix["ordem"] = risco_mix["classe_risco"].map(ordem)
    risco_mix = risco_mix.sort_values("ordem")
    fig = px.bar(
        risco_mix,
        x="classe_risco",
        y="fornecedores",
        color="classe_risco",
        title="Carteira por risco",
        color_discrete_map={"Alto": "#B42318", "Medio": "#B54708", "Baixo": "#027A48"},
    )
    aplicar_layout_plotly(fig)
    st.plotly_chart(fig, use_container_width=True)

    scatter = px.scatter(
        scores,
        x="score_qualidade",
        y="score_volume",
        size="litros_coletados_media",
        color="classe_risco",
        hover_name="id_produtor",
        title="Volume × qualidade",
        color_discrete_map={"Alto": "#B42318", "Medio": "#B54708", "Baixo": "#027A48"},
    )
    aplicar_layout_plotly(scatter)
    st.plotly_chart(scatter, use_container_width=True)

st.divider()

st.subheader("Detalhe do fornecedor")
opcoes = scores["id_produtor"].tolist()
selecionado = st.selectbox(
    "Produtor",
    options=opcoes,
    format_func=lambda x: f"Produtor {x} - risco {formatar_numero_br(scores.loc[scores['id_produtor'] == x, 'score_risco_fornecedor'].iloc[0], 1)}",
)

det = scores[scores["id_produtor"] == selecionado].iloc[0]
hist = ctx.prod_f[ctx.prod_f["id_produtor"] == selecionado].sort_values("data").copy()

# ── Score Premium Visual ──────────────────────────────────────────────────────
_score = float(det["score_risco_fornecedor"])
_classe = det["classe_risco"]
_cor_gauge = {"Alto": "#B42318", "Medio": "#B54708", "Baixo": "#027A48"}.get(_classe, "#6B7280")
_cor_bg = {"Alto": "#FEF3F2", "Medio": "#FFFAEB", "Baixo": "#ECFDF3"}.get(_classe, "#F9FAFB")

col_gauge, col_radar, col_kpis = st.columns([1.1, 1.1, 1.0])

with col_gauge:
    import plotly.graph_objects as go

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=_score,
        delta={"reference": 50, "suffix": " vs médio"},
        number={"font": {"size": 42, "color": _cor_gauge}, "suffix": " pts"},
        title={"text": f"<b>Score de Risco</b><br><span style='font-size:14px;color:{_cor_gauge}'>{_classe.upper()}</span>",
               "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#6B7280",
                     "tickvals": [0, 25, 50, 75, 100]},
            "bar": {"color": _cor_gauge, "thickness": 0.3},
            "bgcolor": "#1E2433",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "#132D1F"},
                {"range": [50, 75], "color": "#2D2010"},
                {"range": [75, 100], "color": "#2D1010"},
            ],
            "threshold": {
                "line": {"color": "#FFFFFF", "width": 3},
                "thickness": 0.8,
                "value": _score,
            },
        },
    ))
    fig_gauge.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    _dims = ["Volume", "Qualidade", "Logística", "Continuidade"]
    _vals = [
        float(det.get("score_volume", 0)),
        float(det.get("score_qualidade", 0)),
        float(det.get("score_logistica", 0)),
        float(det.get("score_continuidade", 0)),
    ]
    fig_radar = go.Figure(go.Scatterpolar(
        r=_vals + [_vals[0]],
        theta=_dims + [_dims[0]],
        fill="toself",
        fillcolor={"Alto": "rgba(180,35,24,0.25)", "Medio": "rgba(181,71,8,0.25)", "Baixo": "rgba(2,122,72,0.25)"}.get(_classe, "rgba(107,114,128,0.25)"),
        line=dict(color=_cor_gauge, width=2),
        marker=dict(size=6, color=_cor_gauge),
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], tickfont_size=9,
                            gridcolor="#374151", tickcolor="#9CA3AF"),
            angularaxis=dict(tickfont_size=11, gridcolor="#374151"),
        ),
        showlegend=False,
        height=230,
        margin=dict(l=30, r=30, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB",
        title=dict(text="<b>Dimensões de Risco</b>", font_size=13, x=0.5),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_kpis:
    st.markdown(f"""
    <div style="background:{_cor_bg};border-left:4px solid {_cor_gauge};border-radius:8px;padding:14px 16px;margin-bottom:8px">
      <div style="font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:.05em">Produção média/dia</div>
      <div style="font-size:22px;font-weight:700;color:#111827">{formatar_numero_br(det['litros_coletados_media'], 0)} L</div>
    </div>
    <div style="background:{_cor_bg};border-left:4px solid {_cor_gauge};border-radius:8px;padding:14px 16px;margin-bottom:8px">
      <div style="font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:.05em">Tendência de volume</div>
      <div style="font-size:22px;font-weight:700;color:#111827">{formatar_numero_br(det['tendencia_volume_pct'], 1)}%</div>
    </div>
    <div style="background:{_cor_bg};border-left:4px solid {_cor_gauge};border-radius:8px;padding:14px 16px">
      <div style="font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:.05em">Descarte · CCS · CBT</div>
      <div style="font-size:16px;font-weight:700;color:#111827">{formatar_numero_br(det['taxa_descarte_pct'], 2)}% · {formatar_numero_br(det['ccs_media'], 0)} · {formatar_numero_br(det['cbt_media'], 0)}</div>
    </div>
    """, unsafe_allow_html=True)

st.info(det["recomendacao"])

# ── Exportar PDF ──────────────────────────────────────────────────────────────
with st.expander("📄 Exportar Relatório Executivo em PDF", expanded=False):
    col_pdf_info, col_pdf_btn = st.columns([2, 1])
    with col_pdf_info:
        st.caption(
            "Gera um relatório A4 com score de risco, dimensões, KPIs operacionais, "
            "recomendação da IA, histórico de volume e dados cadastrais do produtor."
        )
    with col_pdf_btn:
        try:
            # Prepara histórico dos últimos 30 registros
            _hist_pdf = None
            if not hist.empty:
                _hist_pdf = (
                    hist.groupby("data", as_index=False)
                    .agg(
                        litros_coletados=("litros_coletados", "sum"),
                        litros_previstos=("litros_previstos", "sum"),
                    )
                    .sort_values("data")
                    .tail(30)
                )
            _nome_lat = str(det.get("id_laticinio", ""))
            _pdf_bytes = gerar_relatorio_produtor(det, _hist_pdf, _nome_lat)
            st.download_button(
                label="⬇️ Baixar PDF",
                data=_pdf_bytes,
                file_name=f"relatorio_produtor_{selecionado}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        except Exception as _err:
            st.error(f"Erro ao gerar PDF: {_err}")

if not hist.empty:
    serie = hist.groupby("data", as_index=False).agg(
        litros_coletados=("litros_coletados", "sum"),
        litros_previstos=("litros_previstos", "sum"),
        ccs=("ccs", "mean"),
        cbt=("cbt", "mean"),
        litros_descartados=("litros_descartados", "sum"),
    )
    tabs = st.tabs(["Volume", "Qualidade", "Descarte"])
    with tabs[0]:
        fig_v = px.line(
            serie,
            x="data",
            y=["litros_coletados", "litros_previstos"],
            markers=True,
            title="Volume coletado × previsto",
        )
        aplicar_layout_plotly(fig_v)
        st.plotly_chart(fig_v, use_container_width=True)
    with tabs[1]:
        fig_q = px.line(serie, x="data", y=["ccs", "cbt"], markers=True, title="Qualidade do leite")
        aplicar_layout_plotly(fig_q)
        st.plotly_chart(fig_q, use_container_width=True)
    with tabs[2]:
        fig_d = px.bar(serie, x="data", y="litros_descartados", title="Litros descartados")
        aplicar_layout_plotly(fig_d)
        st.plotly_chart(fig_d, use_container_width=True)

base_info = {
    "Município": det.get("municipio", ""),
    "Polo": det.get("polo_climatico", ""),
    "Laticínio": det.get("id_laticinio", ""),
    "Rota": det.get("id_rota", ""),
    "Sistema": det.get("tipo_sistema", ""),
    "Tecnificação": det.get("nivel_tecnificacao", ""),
    "Porte": det.get("porte_produtor", ""),
    "Distância (km)": det.get("distancia_km_laticinio", ""),
}
st.json(base_info, expanded=False)

df_fornecedores = carregar_fornecedores()
if not df_fornecedores.empty:
    forn_idx = df_fornecedores["id_fornecedor"].astype(str) == str(selecionado)
    if forn_idx.any():
        st.markdown("#### Informações cadastrais (Gestão e Dados)")
        forn_det = df_fornecedores[forn_idx].iloc[0]
        f1, f2, f3 = st.columns(3)
        with f1:
            st.write(f"**Identificação:** {forn_det.get('nome', '-')}")
            st.write(f"**Localização:** {forn_det.get('localizacao', '-')}")
            st.write(f"**Indicadores de qualidade:** {forn_det.get('indicadores_qualidade', '-')}")
        with f2:
            try:
                cap_prod = formatar_numero_br(float(forn_det.get("capacidade_produtiva", 0)), 2)
                hist_forn = formatar_numero_br(float(forn_det.get("historico_fornecimento", 0)), 2)
            except Exception:
                cap_prod = "-"
                hist_forn = "-"
            st.write(f"**Capacidade produtiva:** {cap_prod} L")
            st.write(f"**Histórico de fornecimento:** {hist_forn} meses")
        with f3:
            st.write(f"**Operacionais:** {forn_det.get('dados_operacionais', '-')}")
            st.write(f"**Logísticos:** {forn_det.get('dados_logisticos', '-')}")
            st.write(f"**Financeiros:** {forn_det.get('dados_financeiros', '-')}")
