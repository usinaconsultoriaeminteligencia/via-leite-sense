"""VIA LEITE SENSE — redirecionamento para a nova infraestrutura.

O produto migrou para Railway (API FastAPI) + Vercel (frontend SPA).
Esta página redireciona automaticamente para o novo endereço público.

O app Streamlit original está preservado em `via_leite_app_legacy.py`
(rode com `streamlit run via_leite_app_legacy.py` para desenvolvimento local)
e também no histórico do Git.
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

NOVO_URL = "https://via-leite-sense.vercel.app"

st.set_page_config(
    page_title="VIA LEITE SENSE — Novo endereço",
    page_icon="🥛",
    layout="centered",
)

# Oculta a navegação de páginas herdada (o app foi descomissionado).
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"], [data-testid="stSidebar"] { display: none; }
        [data-testid="stAppViewContainer"] { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Redirect automático — navega a janela do topo (fora do iframe do componente).
components.html(
    f"""
    <script>
        window.top.location.replace("{NOVO_URL}");
    </script>
    """,
    height=0,
)

st.title("🥛 VIA LEITE SENSE mudou de endereço")
st.markdown(
    f"""
A plataforma agora roda em nova infraestrutura — mais rápida e escalável.

Se o redirecionamento automático não ocorrer, acesse o novo endereço:

### 👉 [{NOVO_URL}]({NOVO_URL})
"""
)
st.link_button("Acessar o VIA LEITE SENSE", NOVO_URL, type="primary")
st.caption("USINA I.A. — Radar de Risco da cadeia leiteira premium.")
