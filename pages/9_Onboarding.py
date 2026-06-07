"""
pages/9_Onboarding.py — Wizard de Onboarding Interativo VIA LEITE SENSE

Guia o avaliador/cliente por 4 etapas:
  1. Identificação da fazenda / laticínio
  2. Dados produtivos e de qualidade
  3. Logística e clima
  4. Resultado: score premium, diagnóstico e plano sugerido
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

from auth import requer_autenticacao, renderizar_sidebar_usuario

requer_autenticacao()
renderizar_sidebar_usuario()

# ---------------------------------------------------------------------------
# CSS específico da página
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.vl-step-header {
    background: linear-gradient(90deg, rgba(4,120,87,0.2), rgba(74,144,226,0.1));
    border-left: 4px solid #4ADE80;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.2rem;
}
.vl-step-title { color: #F0FFF4; font-size: 1.2rem; font-weight: 700; margin: 0; }
.vl-step-sub   { color: #86EFAC; font-size: 0.85rem; margin: 0.2rem 0 0; }

.vl-score-card {
    background: rgba(4,120,87,0.15);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
}
.vl-score-value { font-size: 3rem; font-weight: 900; color: #4ADE80; line-height: 1; }
.vl-score-label { color: #86EFAC; font-size: 0.85rem; margin-top: 0.3rem; }

.vl-badge-alto     { background:#065f46; color:#6ee7b7; padding:0.2rem 0.7rem;
                     border-radius:12px; font-size:0.8rem; font-weight:700; }
.vl-badge-moderado { background:#78350f; color:#fcd34d; padding:0.2rem 0.7rem;
                     border-radius:12px; font-size:0.8rem; font-weight:700; }
.vl-badge-limitado { background:#7f1d1d; color:#fca5a5; padding:0.2rem 0.7rem;
                     border-radius:12px; font-size:0.8rem; font-weight:700; }

.vl-diag-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Controle de etapas via session_state
# ---------------------------------------------------------------------------
if "ob_step" not in st.session_state:
    st.session_state["ob_step"] = 1
if "ob_dados" not in st.session_state:
    st.session_state["ob_dados"] = {}

dados = st.session_state["ob_dados"]
step  = st.session_state["ob_step"]


def _avancar():
    st.session_state["ob_step"] += 1

def _voltar():
    st.session_state["ob_step"] = max(1, st.session_state["ob_step"] - 1)

def _reiniciar():
    st.session_state["ob_step"] = 1
    st.session_state["ob_dados"] = {}


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.markdown("## 🚀 Onboarding — VIA LEITE SENSE")
st.caption("Cadastre uma fazenda e receba em segundos o diagnóstico de qualidade premium, score preditivo e plano de ação.")

# Barra de progresso
TOTAL_STEPS = 4
progress = (step - 1) / TOTAL_STEPS
labels = ["Identificação", "Produção & Qualidade", "Logística & Clima", "Diagnóstico"]
cols_prog = st.columns(TOTAL_STEPS)
for i, (col, label) in enumerate(zip(cols_prog, labels), 1):
    if i < step:
        col.markdown(f"✅ **{label}**")
    elif i == step:
        col.markdown(f"🔵 **{label}**")
    else:
        col.markdown(f"⬜ {label}")

st.progress(progress)
st.divider()


# ---------------------------------------------------------------------------
# ETAPA 1 — Identificação
# ---------------------------------------------------------------------------
if step == 1:
    st.markdown("""
    <div class="vl-step-header">
        <p class="vl-step-title">Etapa 1 — Identificação da Fazenda</p>
        <p class="vl-step-sub">Dados básicos do produtor e do laticínio parceiro</p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    nome_fazenda  = c1.text_input("Nome da fazenda *", value=dados.get("nome_fazenda",""), placeholder="Ex.: Fazenda Boa Esperança")
    nome_produtor = c2.text_input("Responsável / Produtor *", value=dados.get("nome_produtor",""), placeholder="Ex.: João da Silva")

    c3, c4, c5 = st.columns(3)
    polo = c3.selectbox("Polo climático *",
        ["RIO_VERDE","JATAI","MINEIROS","OUTRO"],
        index=["RIO_VERDE","JATAI","MINEIROS","OUTRO"].index(dados.get("polo","RIO_VERDE")))
    municipio = c4.text_input("Município", value=dados.get("municipio",""), placeholder="Ex.: Rio Verde")
    data_inicio = c5.date_input("Início da parceria", value=dados.get("data_inicio", date.today()))

    tipo_sistema = st.selectbox("Sistema de produção",
        ["PASTO","SEMI_CONFINADO","CONFINADO"],
        index=["PASTO","SEMI_CONFINADO","CONFINADO"].index(dados.get("tipo_sistema","PASTO")))

    nivel_tec = st.select_slider("Nível de tecnificação",
        options=["BAIXO","MEDIO","ALTO"],
        value=dados.get("nivel_tec","MEDIO"))

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Próxima etapa →", type="primary", use_container_width=True, key="btn_step1"):
        if not nome_fazenda.strip() or not nome_produtor.strip():
            st.warning("Preencha nome da fazenda e do responsável.")
        else:
            dados.update(dict(
                nome_fazenda=nome_fazenda, nome_produtor=nome_produtor,
                polo=polo, municipio=municipio,
                data_inicio=data_inicio,
                tipo_sistema=tipo_sistema, nivel_tec=nivel_tec,
            ))
            _avancar(); st.rerun()


# ---------------------------------------------------------------------------
# ETAPA 2 — Produção & Qualidade
# ---------------------------------------------------------------------------
elif step == 2:
    st.markdown("""
    <div class="vl-step-header">
        <p class="vl-step-title">Etapa 2 — Produção e Qualidade do Leite</p>
        <p class="vl-step-sub">Indicadores produtivos e de qualidade para cálculo do score premium</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    vacas        = c1.number_input("Vacas em lactação", min_value=1, value=dados.get("vacas",30), step=1)
    prod_media   = c2.number_input("Produção média diária (L)", min_value=50.0, value=float(dados.get("prod_media",600.0)), step=50.0)
    cap_tanque   = c3.number_input("Capacidade do tanque (L)", min_value=100.0, value=float(dados.get("cap_tanque",1200.0)), step=100.0)

    st.markdown("##### Indicadores de qualidade")
    c4, c5, c6 = st.columns(3)
    ccs   = c4.number_input("CCS média (mil céls/mL)", min_value=0.0, value=float(dados.get("ccs",300.0)),
                             step=10.0, help="Contagem de Células Somáticas — padrão premium: < 400")
    cbt   = c5.number_input("CBT média (mil UFC/mL)", min_value=0.0, value=float(dados.get("cbt",80.0)),
                             step=5.0, help="Contagem Bacteriana Total — padrão premium: < 100")
    temp_tanque = c6.number_input("Temp. tanque habitual (°C)", min_value=2.0, max_value=10.0,
                                   value=float(dados.get("temp_tanque",4.0)), step=0.5)

    c7, c8 = st.columns(2)
    taxa_descarte = c7.slider("Taxa de descarte (%)", 0.0, 15.0, value=float(dados.get("taxa_descarte",2.0)), step=0.5)
    antibiotico   = c8.checkbox("Ocorrência recente de antibiótico no leite", value=dados.get("antibiotico",False))

    raca = st.selectbox("Raça predominante",
        ["GIROLANDO","HOLANDESA","JERSEY","MISTA","OUTRA"],
        index=["GIROLANDO","HOLANDESA","JERSEY","MISTA","OUTRA"].index(dados.get("raca","GIROLANDO")))

    bcol1, bcol2 = st.columns([1,4])
    bcol1.button("← Voltar", on_click=_voltar, key="btn_back2")
    if bcol2.button("Próxima etapa →", type="primary", use_container_width=True, key="btn_step2"):
        dados.update(dict(
            vacas=vacas, prod_media=prod_media, cap_tanque=cap_tanque,
            ccs=ccs, cbt=cbt, temp_tanque=temp_tanque,
            taxa_descarte=taxa_descarte, antibiotico=antibiotico, raca=raca,
        ))
        _avancar(); st.rerun()


# ---------------------------------------------------------------------------
# ETAPA 3 — Logística & Clima
# ---------------------------------------------------------------------------
elif step == 3:
    st.markdown("""
    <div class="vl-step-header">
        <p class="vl-step-title">Etapa 3 — Logística e Sensibilidade Climática</p>
        <p class="vl-step-sub">Dados de rota, distância e exposição ao clima</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    distancia      = c1.number_input("Distância ao laticínio (km)", min_value=1.0, value=float(dados.get("distancia",40.0)), step=5.0)
    freq_coleta    = c2.selectbox("Frequência de coleta",
        ["Diária","A cada 2 dias","A cada 3 dias"],
        index=["Diária","A cada 2 dias","A cada 3 dias"].index(dados.get("freq_coleta","Diária")))
    pct_nao_pav    = c3.slider("Estrada não pavimentada (%)", 0, 100, value=dados.get("pct_nao_pav",20))

    st.markdown("##### Sensibilidade climática")
    c4, c5, c6 = st.columns(3)
    sens_seca  = c4.slider("Sensib. à seca (0–2)", 0.0, 2.0, value=float(dados.get("sens_seca",1.0)), step=0.1)
    sens_calor = c5.slider("Sensib. ao calor (0–2)", 0.0, 2.0, value=float(dados.get("sens_calor",1.0)), step=0.1)
    sens_qual  = c6.slider("Sensib. à qualidade (0–2)", 0.0, 2.0, value=float(dados.get("sens_qual",1.0)), step=0.1)

    st.markdown("##### Contexto de negócio")
    c7, c8 = st.columns(2)
    margem_est = c7.number_input("Margem estimada por litro (R$)", min_value=0.0,
                                  value=float(dados.get("margem_est",0.80)), step=0.05, format="%.2f")
    prob_churn = c8.slider("Risco de saída estimado (%)", 0.0, 10.0,
                            value=float(dados.get("prob_churn",1.0)), step=0.1)

    bcol1, bcol2 = st.columns([1,4])
    bcol1.button("← Voltar", on_click=_voltar, key="btn_back3")
    if bcol2.button("Gerar diagnóstico →", type="primary", use_container_width=True, key="btn_step3"):
        dados.update(dict(
            distancia=distancia, freq_coleta=freq_coleta, pct_nao_pav=pct_nao_pav,
            sens_seca=sens_seca, sens_calor=sens_calor, sens_qual=sens_qual,
            margem_est=margem_est, prob_churn=prob_churn,
        ))
        _avancar(); st.rerun()


# ---------------------------------------------------------------------------
# ETAPA 4 — Diagnóstico e Score Premium
# ---------------------------------------------------------------------------
elif step == 4:
    st.markdown("""
    <div class="vl-step-header">
        <p class="vl-step-title">Etapa 4 — Diagnóstico VIA LEITE SENSE</p>
        <p class="vl-step-sub">Score premium, aptidão para cadeia premium e plano de ação sugerido</p>
    </div>""", unsafe_allow_html=True)

    # ── Cálculo do score premium ──────────────────────────────────────────
    def _norm(v, vmin, vmax, inverso=False):
        r = max(0.0, min(1.0, (v - vmin) / max(vmax - vmin, 1e-9)))
        return 1 - r if inverso else r

    # Dimensão Qualidade (peso 40%)
    score_ccs   = _norm(dados["ccs"], 0, 800, inverso=True)
    score_cbt   = _norm(dados["cbt"], 0, 300, inverso=True)
    score_desc  = _norm(dados["taxa_descarte"], 0, 15, inverso=True)
    score_temp  = _norm(dados["temp_tanque"], 2, 10, inverso=True)
    penalidade_anti = 0.15 if dados["antibiotico"] else 0.0
    dim_qualidade = max(0.0, (score_ccs*0.35 + score_cbt*0.30 + score_desc*0.20 + score_temp*0.15) - penalidade_anti)

    # Dimensão Volume / Produção (peso 30%)
    prod_por_vaca = dados["prod_media"] / max(dados["vacas"], 1)
    score_prod    = _norm(prod_por_vaca, 5, 40)
    score_ocup    = _norm(dados["prod_media"] / max(dados["cap_tanque"], 1), 0.3, 0.95)
    dim_volume    = score_prod * 0.6 + score_ocup * 0.4

    # Dimensão Logística (peso 15%)
    score_dist   = _norm(dados["distancia"], 5, 150, inverso=True)
    score_pav    = _norm(dados["pct_nao_pav"], 0, 100, inverso=True)
    dim_logistica = score_dist * 0.5 + score_pav * 0.5

    # Dimensão Continuidade (peso 15%)
    score_churn  = _norm(dados["prob_churn"], 0, 10, inverso=True)
    score_margem = _norm(dados["margem_est"], 0, 2)
    dim_continuidade = score_churn * 0.6 + score_margem * 0.4

    score_premium = round(
        (dim_qualidade * 40 + dim_volume * 30 + dim_logistica * 15 + dim_continuidade * 15), 1
    )

    # Aptidão
    if score_premium >= 70:
        aptidao = "ALTA"
        aptidao_badge = '<span class="vl-badge-alto">ALTA APTIDÃO PREMIUM</span>'
        aptidao_msg = "Leite apto para cadeia premium. Monitorar e manter o padrão."
        cor_gauge = "#4ADE80"
    elif score_premium >= 45:
        aptidao = "MODERADA"
        aptidao_badge = '<span class="vl-badge-moderado">APTIDÃO MODERADA</span>'
        aptidao_msg = "Potencial identificado. Ajustes pontuais podem elevar ao premium."
        cor_gauge = "#FCD34D"
    else:
        aptidao = "LIMITADA"
        aptidao_badge = '<span class="vl-badge-limitado">APTIDÃO LIMITADA</span>'
        aptidao_msg = "Necessita intervenção antes de ingressar na cadeia premium."
        cor_gauge = "#F87171"

    # ── Layout do diagnóstico ─────────────────────────────────────────────
    col_score, col_gauge, col_radar = st.columns([1, 1.2, 1.8])

    with col_score:
        st.markdown(f"""
        <div class="vl-score-card">
            <div class="vl-score-value">{score_premium}</div>
            <div class="vl-score-label">Score Premium</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"<br>{aptidao_badge}", unsafe_allow_html=True)
        st.caption(aptidao_msg)

    with col_gauge:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_premium,
            number={"font": {"color": cor_gauge, "size": 36}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#64748b"},
                "bar":  {"color": cor_gauge, "thickness": 0.28},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 45],  "color": "rgba(127,29,29,0.3)"},
                    {"range": [45, 70], "color": "rgba(120,53,15,0.3)"},
                    {"range": [70, 100],"color": "rgba(6,78,59,0.3)"},
                ],
                "threshold": {"line": {"color": "#F0FFF4", "width": 2}, "value": score_premium},
            },
            title={"text": "Score Premium", "font": {"color": "#94A3B8", "size": 13}},
        ))
        fig_g.update_layout(
            height=220, margin=dict(l=20, r=20, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#F0FFF4",
        )
        st.plotly_chart(fig_g, use_container_width=True)

    with col_radar:
        categorias = ["Qualidade", "Volume", "Logística", "Continuidade"]
        valores    = [
            round(dim_qualidade * 100, 1),
            round(dim_volume * 100, 1),
            round(dim_logistica * 100, 1),
            round(dim_continuidade * 100, 1),
        ]
        fig_r = go.Figure(go.Scatterpolar(
            r=valores + [valores[0]],
            theta=categorias + [categorias[0]],
            fill="toself",
            fillcolor="rgba(74,222,128,0.15)",
            line=dict(color="#4ADE80", width=2),
        ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], color="#64748b"),
                angularaxis=dict(color="#94A3B8"),
            ),
            showlegend=False,
            height=230,
            margin=dict(l=30, r=30, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_r, use_container_width=True)

    st.divider()

    # ── Diagnóstico por dimensão ──────────────────────────────────────────
    st.subheader("Diagnóstico por dimensão")
    dim_cols = st.columns(4)
    dims = [
        ("🧪 Qualidade", dim_qualidade, "CCS, CBT, descarte e temperatura do tanque"),
        ("📦 Volume",    dim_volume,    "Produção por vaca e ocupação de tanque"),
        ("🚛 Logística", dim_logistica, "Distância, pavimentação e frequência de coleta"),
        ("🔄 Continuidade", dim_continuidade, "Risco de saída e margem estimada"),
    ]
    for col, (titulo, val, desc) in zip(dim_cols, dims):
        pct = round(val * 100, 0)
        cor = "#4ADE80" if pct >= 70 else "#FCD34D" if pct >= 45 else "#F87171"
        col.metric(titulo, f"{pct:.0f}/100")
        col.progress(val, text=desc)

    st.divider()

    # ── Plano de ação sugerido ────────────────────────────────────────────
    st.subheader("📋 Plano de Ação Sugerido")

    acoes = []
    if dados["ccs"] >= 400:
        acoes.append(("🔴 Urgente", "Qualidade",
            f"CCS = {dados['ccs']:.0f} mil céls/mL está acima do limite premium (400). "
            "Revisar higiene de ordenha, saúde do úbere e protocolo de limpeza do tanque.",
            "7 dias"))
    if dados["cbt"] >= 100:
        acoes.append(("🔴 Urgente", "Qualidade",
            f"CBT = {dados['cbt']:.0f} mil UFC/mL supera o padrão premium (100). "
            "Verificar temperatura do tanque, higienização de equipamentos e água de limpeza.",
            "7 dias"))
    if dados["taxa_descarte"] >= 3:
        acoes.append(("🟡 Importante", "Operacional",
            f"Taxa de descarte = {dados['taxa_descarte']:.1f}%. "
            "Investigar causas: antibióticos, CCS elevada ou problemas na coleta.",
            "15 dias"))
    if dados["temp_tanque"] > 5:
        acoes.append(("🟡 Importante", "Qualidade",
            f"Temperatura do tanque = {dados['temp_tanque']:.1f}°C. "
            "Leite premium requer resfriamento abaixo de 4°C nas 2h após ordenha.",
            "imediato"))
    if dados["antibiotico"]:
        acoes.append(("🔴 Urgente", "Qualidade",
            "Ocorrência recente de antibiótico detectada. "
            "Implementar protocolo de descarte e identificação de animais em tratamento.",
            "imediato"))
    if dados["pct_nao_pav"] >= 40:
        acoes.append(("🟢 Melhoria", "Logística",
            f"{dados['pct_nao_pav']}% da rota não pavimentada aumenta risco de falha na coleta. "
            "Avaliar rota alternativa em períodos de chuva.",
            "30 dias"))
    if dados["prob_churn"] >= 3:
        acoes.append(("🟡 Importante", "Relacionamento",
            f"Risco de saída = {dados['prob_churn']:.1f}%. "
            "Acionar visita comercial e revisar condições contratuais.",
            "15 dias"))
    if prod_por_vaca < 12:
        acoes.append(("🟢 Melhoria", "Produção",
            f"Produtividade = {prod_por_vaca:.1f} L/vaca/dia. "
            "Avaliar nutrição, genética e manejo reprodutivo para elevar a média.",
            "60 dias"))
    if not acoes:
        acoes.append(("✅ Excelente", "Geral",
            "Todos os indicadores estão dentro dos padrões premium. "
            "Manter monitoramento regular e documentar boas práticas para replicação.",
            "contínuo"))

    for prioridade, categoria, descricao, prazo in acoes:
        st.markdown(f"""
        <div class="vl-diag-item">
            <strong style="color:#F0FFF4">{prioridade} · {categoria}</strong>
            <span style="color:#64748b; font-size:0.78rem; float:right">Prazo: {prazo}</span>
            <p style="color:#94A3B8; margin:0.3rem 0 0; font-size:0.88rem">{descricao}</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Resumo final ─────────────────────────────────────────────────────
    st.subheader("📄 Resumo do Onboarding")
    r1, r2, r3 = st.columns(3)
    r1.metric("Fazenda", dados["nome_fazenda"])
    r2.metric("Polo climático", dados["polo"])
    r3.metric("Sistema", dados["tipo_sistema"])
    r4, r5, r6 = st.columns(3)
    r4.metric("Produção/dia", f"{dados['prod_media']:,.0f} L")
    r5.metric("Vacas em lactação", str(dados["vacas"]))
    r6.metric("Distância ao laticínio", f"{dados['distancia']:.0f} km")

    st.success(
        f"**{dados['nome_fazenda']}** onboardada com score premium **{score_premium}/100** "
        f"e aptidão **{aptidao}**. "
        f"{len(acoes)} ação(ões) identificada(s) no plano inicial."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns(3)
    bc1.button("← Revisar dados", on_click=_voltar, key="btn_back4")
    if bc2.button("🔄 Nova fazenda", use_container_width=True, key="btn_reiniciar"):
        _reiniciar(); st.rerun()
    bc3.markdown(
        "<a href='/Fornecedores_360' target='_self'>"
        "<button style='width:100%;padding:0.5rem;background:#065f46;color:#F0FFF4;"
        "border:none;border-radius:8px;cursor:pointer;font-weight:600'>"
        "Ver Fornecedores 360 →</button></a>",
        unsafe_allow_html=True,
    )

    st.caption("Dados simulados para demonstração. Score calculado com modelo proprietário VIA LEITE SENSE — USINA I.A.")
