"""
via_leite_app.py — Entry point principal do VIA LEITE SENSE.

Execute com:
    streamlit run via_leite_app.py

Responsabilidades:
  - Renderizar a landing page (antes do login)
  - Gerenciar autenticação nativa (bcrypt + session_state)
  - Redirecionar para o dashboard após login
"""
from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Configuração da página — DEVE ser a primeira chamada Streamlit
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VIA LEITE SENSE | Monitoramento Inteligente da Produção Leiteira",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from auth import (  # noqa: E402
    esta_autenticado,
    renderizar_formulario_login,
    renderizar_sidebar_usuario,
)

# ---------------------------------------------------------------------------
# CSS global — branding Via Leite
# Paleta: verde agro #027A48 · azul técnico #4A90E2 · cinza carbono escuro
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Fundo */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0a1628 0%, #0d2137 45%, #0a1f14 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] { background: #0d1b2a !important; }
    [data-testid="stSidebarContent"] { background: #0d1b2a !important; }

    /* ---- Hero ---- */
    .vl-badge {
        display: inline-block;
        background: rgba(74,144,226,0.15);
        border: 1px solid rgba(74,144,226,0.4);
        color: #93C5FD;
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        letter-spacing: 0.02em;
    }
    .vl-hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #F0FFF4;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }
    .vl-hero-accent { color: #4ADE80; }
    .vl-hero-subtitle {
        font-size: 1.2rem;
        color: #86EFAC;
        font-weight: 400;
        margin-bottom: 1.2rem;
    }
    .vl-tagline {
        font-size: 0.975rem;
        color: #94A3B8;
        margin-bottom: 1.8rem;
        max-width: 600px;
        line-height: 1.6;
    }

    /* ---- KPIs ---- */
    .vl-kpi-row {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1.8rem;
        flex-wrap: wrap;
    }
    .vl-kpi {
        background: rgba(4,120,87,0.18);
        border: 1px solid rgba(4,120,87,0.45);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        min-width: 120px;
        text-align: center;
        flex: 1;
    }
    .vl-kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #6EE7B7;
        line-height: 1.1;
    }
    .vl-kpi-label {
        font-size: 0.7rem;
        color: #86EFAC;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* ---- Feature cards ---- */
    .vl-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.65rem;
        transition: border-color 0.2s;
    }
    .vl-card:hover { border-color: rgba(74,222,128,0.3); }
    .vl-card-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
    .vl-card-title {
        color: #F0FFF4;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.15rem;
    }
    .vl-card-desc { color: #94A3B8; font-size: 0.83rem; line-height: 1.4; }

    /* ---- Login box ---- */
    .vl-login-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.8rem;
        margin-top: 2rem;
    }

    /* Inputs — legíveis em qualquer tema */
    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stTextInput"] input {
        background-color: #1e3a5f !important;
        color: #F0FFF4 !important;
        border: 1.5px solid #3b82f6 !important;
        border-radius: 8px !important;
        caret-color: #4ADE80 !important;
        -webkit-text-fill-color: #F0FFF4 !important;
    }
    div[data-testid="stTextInput"] > div > div > input:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color: #4ADE80 !important;
        box-shadow: 0 0 0 2px rgba(74,222,128,0.15) !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] > div > div > input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }
    /* Label dos inputs */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label p {
        color: #93C5FD !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    /* Ícone olho (password toggle) */
    div[data-testid="stTextInput"] button svg {
        fill: #94A3B8 !important;
    }

    /* Botão primário do formulário */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"],
    div[data-testid="stForm"] button[data-testid="stFormSubmitButton"],
    div[data-testid="stForm"] button[type="submit"] {
        background: linear-gradient(135deg, #059669, #047857) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, #047857, #065f46) !important;
    }

    /* Alertas de erro (senha incorreta) */
    div[data-testid="stAlert"] {
        background: rgba(185,28,28,0.25) !important;
        border: 1px solid rgba(239,68,68,0.4) !important;
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"] p {
        color: #FCA5A5 !important;
    }

    /* Tabelas de credenciais demo */
    table { border-collapse: collapse; width: 100%; }
    th, td {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        padding: 0.3rem 0.5rem !important;
        border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    }
    th { color: #CBD5E1 !important; font-weight: 600 !important; }
    code {
        background: rgba(74,222,128,0.15) !important;
        color: #6EE7B7 !important;
        padding: 0.15rem 0.4rem !important;
        border-radius: 4px !important;
        font-size: 0.83rem !important;
    }

    /* ---- Rodapé ---- */
    .vl-footer {
        text-align: center;
        color: #334155;
        font-size: 0.72rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Componentes HTML
# ---------------------------------------------------------------------------
def _kpi(valor: str, label: str) -> str:
    return (
        f'<div class="vl-kpi">'
        f'<div class="vl-kpi-value">{valor}</div>'
        f'<div class="vl-kpi-label">{label}</div>'
        "</div>"
    )


def _card(icon: str, title: str, desc: str) -> str:
    return (
        f'<div class="vl-card">'
        f'<div class="vl-card-icon">{icon}</div>'
        f'<div class="vl-card-title">{title}</div>'
        f'<div class="vl-card-desc">{desc}</div>'
        "</div>"
    )


# ---------------------------------------------------------------------------
# Sessão autenticada — dashboard principal
# ---------------------------------------------------------------------------
def _renderizar_dashboard_autenticado() -> None:
    st.set_page_config(
        page_title="VIA LEITE SENSE | Dashboard",
        page_icon="🥛",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def _executar_dashboard() -> None:
    """Executa o módulo de dashboard como se fosse o entry point."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_vls_dashboard", "dashboard_mvp_avancado.py")
    mod = importlib.util.module_from_spec(spec)   # type: ignore[arg-type]
    spec.loader.exec_module(mod)                   # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Landing page
# ---------------------------------------------------------------------------
def _renderizar_landing() -> None:
    col_hero, col_login = st.columns([1.45, 1], gap="large")

    # ── COLUNA ESQUERDA — hero ──────────────────────────────────────────────
    with col_hero:
        st.markdown(
            '<div class="vl-badge">🏆 FATESG SENAI · Maratona de Inovação 2025</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="vl-hero-title">VIA LEITE<br>'
            '<span class="vl-hero-accent">SENSE</span></p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="vl-hero-subtitle">'
            "Monitoramento Inteligente da Produção Leiteira"
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="vl-tagline">'
            "Plataforma de IA preditiva para a cadeia leiteira premium: "
            "qualidade, rastreabilidade, logística e telemetria IoT-ready — "
            "do sensor à decisão, em tempo real."
            "</p>",
            unsafe_allow_html=True,
        )

        # KPIs do modelo
        st.markdown(
            '<div class="vl-kpi-row">'
            + _kpi("99,4%", "Acurácia R²")
            + _kpi("3,7%", "Erro sMAPE")
            + _kpi("107", "Variáveis IA")
            + _kpi("8", "Módulos")
            + "</div>",
            unsafe_allow_html=True,
        )

        # Feature cards
        features = [
            (
                "🧠",
                "IA Preditiva XGBoost",
                "Previsão de captação 7 dias à frente com 107 variáveis "
                "climáticas, operacionais e de comportamento de fornecedor.",
            ),
            (
                "🌡️",
                "VIA LEITE EDGE — IoT-ready",
                "Telemetria de tanque, THI e score premium com arquitetura "
                "preparada para sensores reais MQTT/API.",
            ),
            (
                "🗺️",
                "Mapa de Fazendas ao Vivo",
                "Prioridade logística, risco térmico e qualidade por polo "
                "climático (Rio Verde · Jataí · Mineiros).",
            ),
            (
                "📊",
                "Fornecedores 360",
                "Score composto de volume, qualidade, logística e continuidade "
                "com recomendação automatizada por produtor.",
            ),
            (
                "♻️",
                "ESG e Rastreabilidade",
                "Redução de descarte, conservação do leite e narrativa de "
                "sustentabilidade para auditoria e mercados premium.",
            ),
        ]
        for icon, title, desc in features:
            st.markdown(_card(icon, title, desc), unsafe_allow_html=True)

        st.markdown(
            '<div class="vl-footer">'
            "Tecnologia desenvolvida por <strong>USINA I.A. Tecnologia e Inovação</strong>"
            " · IA aplicada para agronegócio · Goiânia-GO"
            "</div>",
            unsafe_allow_html=True,
        )

    # ── COLUNA DIREITA — login ──────────────────────────────────────────────
    with col_login:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="vl-login-box">', unsafe_allow_html=True)
            renderizar_formulario_login("Acesso à Plataforma")
            st.markdown("</div>", unsafe_allow_html=True)

        # Credenciais de demonstração
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔑 Credenciais de demonstração", expanded=True):
            st.markdown(
                "| Usuário | Senha | Perfil |\n"
                "|---------|-------|--------|\n"
                "| `demo` | `demo2025` | Avaliador |\n"
                "| `laticinio` | `leite2025` | Operação |\n"
                "| `admin` | `usina2025` | Admin |"
            )
            st.caption("Credenciais apenas para demonstração do protótipo.")


# ---------------------------------------------------------------------------
# Roteamento principal
# ---------------------------------------------------------------------------
def main() -> None:
    if esta_autenticado():
        renderizar_sidebar_usuario()
        _executar_dashboard()
    else:
        _renderizar_landing()


main()
