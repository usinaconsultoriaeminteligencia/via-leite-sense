from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple

import pandas as pd
import streamlit as st

PAGE_CONFIG = {
    "page_title": "VIA LEITE SENSE | Monitoramento Inteligente da Producao Leiteira",
    "page_icon": "🥛",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}


_CSS_SIDEBAR_NAV = """
<script>
(function renomearInicio() {
    function tentar() {
        var links = document.querySelectorAll('[data-testid="stSidebarNav"] a');
        if (!links.length) { setTimeout(tentar, 150); return; }
        var primeiro = links[0];
        var span = primeiro.querySelector('span') || primeiro;
        if (span.textContent.toLowerCase().includes('via leite app') ||
            span.textContent.toLowerCase().includes('via_leite')) {
            span.textContent = 'Início';
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tentar);
    } else {
        tentar();
    }
    // Re-aplica após reruns do Streamlit
    new MutationObserver(tentar).observe(document.body, { childList: true, subtree: true });
})();
</script>
<style>
/* ── Sidebar nav — acabamento premium ───────────────────────────────────── */

/* Container geral */
[data-testid="stSidebarNav"] {
    padding: 0.4rem 0 0.8rem 0;
}

/* Remove marcadores padrão */
[data-testid="stSidebarNav"] ul {
    padding: 0 !important;
    margin: 0 !important;
    gap: 1px !important;
}
[data-testid="stSidebarNav"] li {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Links — estado normal */
[data-testid="stSidebarNav"] a {
    display: flex !important;
    align-items: center !important;
    padding: 0.42rem 1.1rem !important;
    color: #94A3B8 !important;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.012em !important;
    text-decoration: none !important;
    border-radius: 6px !important;
    margin: 0 6px !important;
    border-left: 2px solid transparent !important;
    transition: background 0.15s, color 0.15s, border-color 0.15s !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

/* Hover */
[data-testid="stSidebarNav"] a:hover {
    background: rgba(74, 222, 128, 0.07) !important;
    color: #D1FAE5 !important;
    border-left-color: rgba(74, 222, 128, 0.4) !important;
}

/* Página ativa */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(74, 222, 128, 0.13) !important;
    color: #4ADE80 !important;
    font-weight: 700 !important;
    border-left-color: #4ADE80 !important;
    letter-spacing: 0.018em !important;
}

/* Span interno do texto */
[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a p {
    color: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    letter-spacing: inherit !important;
}

/* Ícone SVG interno */
[data-testid="stSidebarNav"] a svg {
    opacity: 0.55;
    margin-right: 6px !important;
    flex-shrink: 0 !important;
}
[data-testid="stSidebarNav"] a:hover svg,
[data-testid="stSidebarNav"] a[aria-current="page"] svg {
    opacity: 1;
}

/* Separador visual sutil acima do primeiro item */
[data-testid="stSidebarNav"]::before {
    content: "NAVEGAÇÃO";
    display: block;
    padding: 0 1.1rem 0.4rem 1.1rem;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #334155;
    text-transform: uppercase;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
</style>
"""


def aplicar_css_nav() -> None:
    """Injeta CSS premium do menu lateral. Chamar em todas as páginas."""
    st.markdown(_CSS_SIDEBAR_NAV, unsafe_allow_html=True)


def configurar_pagina() -> None:
    st.set_page_config(**PAGE_CONFIG)


def _guard_autenticacao() -> None:
    """
    Verifica autenticação via session_state (populado por auth.autenticar).
    Bloqueia a página se o usuário não estiver logado.
    Chamado automaticamente em carregar_contexto() — cobre TODAS as páginas.
    """
    if st.session_state.get("authentication_status") is not True:
        st.warning("🔒 Acesso restrito. Faça login na página principal.")
        st.page_link("via_leite_app.py", label="→ Ir para o Login", icon="🏠")
        st.stop()


@dataclass
class DashboardContext:
    metricas: dict
    feat: pd.DataFrame
    dim_prod: pd.DataFrame
    pred_f: pd.DataFrame
    prod_f: pd.DataFrame
    rota_f: pd.DataFrame
    clima_f: pd.DataFrame


def formatar_numero_br(valor: float | int, casas: int = 2) -> str:
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def artefatos_dir() -> Path:
    return Path(os.environ.get("MVP_ARTEFATOS_DIR", "artefatos_teste"))


def data_dir() -> Path:
    return Path(os.environ.get("MVP_DATA_DIR", "dados_teste"))


@st.cache_data(ttl=3600, show_spinner="Carregando dados...")
def carregar_dados(
    art_dir: Path,
    d_dir: Path,
) -> Tuple[pd.DataFrame, dict, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    req = [
        art_dir / "predicoes_teste.csv",
        art_dir / "metricas_modelo.json",
        d_dir / "fact_producao_produtor_dia.csv",
        d_dir / "dim_produtor.csv",
        d_dir / "fact_rota_dia.csv",
        d_dir / "fact_clima_diario.csv",
    ]
    missing = [p for p in req if not p.exists()]
    if missing:
        names = ", ".join(p.name for p in missing)
        raise FileNotFoundError(f"Arquivos em falta: {names}")

    pred = pd.read_csv(art_dir / "predicoes_teste.csv", parse_dates=["data"])
    metricas = json.loads((art_dir / "metricas_modelo.json").read_text(encoding="utf-8"))
    feat_path = art_dir / "feature_importances.csv"
    feat = pd.read_csv(feat_path) if feat_path.exists() else pd.DataFrame(columns=["feature", "importance"])

    prod = pd.read_csv(d_dir / "fact_producao_produtor_dia.csv", parse_dates=["data"])
    dim_prod = pd.read_csv(d_dir / "dim_produtor.csv")
    rota = pd.read_csv(d_dir / "fact_rota_dia.csv", parse_dates=["data"])
    clima = pd.read_csv(d_dir / "fact_clima_diario.csv", parse_dates=["data"])
    return pred, metricas, feat, prod, dim_prod, rota, clima


def aplicar_layout_plotly(fig, title: str | None = None) -> Any:
    kw: dict = dict(
        template="plotly_white",
        font=dict(family="Segoe UI, sans-serif", size=12),
        legend_title_text="",
        margin=dict(l=40, r=24, t=48, b=40),
        hovermode="x unified",
    )
    if title is not None:
        kw["title"] = title
    fig.update_layout(**kw)
    return fig


def render_sidebar_filtros(pred: pd.DataFrame) -> Tuple[list, list, Any, Any]:
    with st.sidebar:
        st.markdown("### Filtros globais")
        laticinios = sorted(pred["id_laticinio"].dropna().unique().tolist())
        polos = sorted(pred["polo_climatico"].dropna().unique().tolist())
        datas = (pred["data"].min().date(), pred["data"].max().date())

        lats = st.multiselect("Laticínios", laticinios, default=laticinios)
        pols = st.multiselect("Polos climáticos", polos, default=polos)
        intervalo = st.date_input("Período", value=datas)

        st.divider()
        st.caption("Caminhos: `MVP_DATA_DIR`, `MVP_ARTEFATOS_DIR` (opcional).")

    if isinstance(intervalo, tuple) and len(intervalo) == 2:
        ini, fim = pd.Timestamp(intervalo[0]), pd.Timestamp(intervalo[1])
    else:
        ini, fim = pred["data"].min(), pred["data"].max()

    return lats, pols, ini, fim


def filtrar_conjuntos(
    pred: pd.DataFrame,
    prod: pd.DataFrame,
    rota: pd.DataFrame,
    clima: pd.DataFrame,
    lats: list,
    pols: list,
    ini: pd.Timestamp,
    fim: pd.Timestamp,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pred_f = pred[
        (pred["id_laticinio"].isin(lats)) & (pred["polo_climatico"].isin(pols)) & (pred["data"].between(ini, fim))
    ].copy()
    prod_f = prod[
        (prod["id_laticinio"].isin(lats)) & (prod["polo_climatico"].isin(pols)) & (prod["data"].between(ini, fim))
    ].copy()
    rota_f = rota[(rota["id_laticinio"].isin(lats)) & (rota["data"].between(ini, fim))].copy()
    clima_f = clima[(clima["polo_climatico"].isin(pols)) & (clima["data"].between(ini, fim))].copy()
    return pred_f, prod_f, rota_f, clima_f


def carregar_contexto() -> DashboardContext:
    _guard_autenticacao()
    aplicar_css_nav()
    art, dat = artefatos_dir(), data_dir()
    pred, metricas, feat, prod, dim_prod, rota, clima = carregar_dados(art, dat)
    lats, pols, ini, fim = render_sidebar_filtros(pred)
    pred_f, prod_f, rota_f, clima_f = filtrar_conjuntos(pred, prod, rota, clima, lats, pols, ini, fim)
    return DashboardContext(
        metricas=metricas,
        feat=feat,
        dim_prod=dim_prod,
        pred_f=pred_f,
        prod_f=prod_f,
        rota_f=rota_f,
        clima_f=clima_f,
    )
