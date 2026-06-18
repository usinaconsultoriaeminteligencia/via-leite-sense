"""
pages/13_Mercado.py — VIA LEITE SENSE
Tamanho de mercado: TAM, SAM e SOM.

Slide de pitch para o Desafio AgroStartup SENAR/SEBRAE Goiás.
Funil de dimensionamento de mercado com premissas editáveis ao vivo
(preço de assinatura e penetração por camada).

TAM — Total Addressable Market: mercado total teórico (toda a demanda possível).
SAM — Serviceable Available Market: parcela atendível pelo modelo de negócio.
SOM — Serviceable Obtainable Market: parcela realista a conquistar no curto prazo.
"""

import os
import sys

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from auth import requer_autenticacao
    requer_autenticacao()
except ImportError:
    pass

st.set_page_config(
    page_title="Mercado (TAM/SAM/SOM) — VIA LEITE SENSE",
    page_icon="📐",
    layout="wide",
)

CORES = {"TAM": "#1e3a8a", "SAM": "#2563eb", "SOM": "#22c55e"}


def _brl(v: float) -> str:
    """Formata valor em R$ com sufixo legível (mi / bi)."""
    if v >= 1_000_000_000:
        return f"R$ {v/1_000_000_000:,.2f} bi".replace(",", "X").replace(".", ",").replace("X", ".")
    if v >= 1_000_000:
        return f"R$ {v/1_000_000:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {v:,.0f}".replace(",", ".")


def _num(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".")


# ------------------------------------------------------------------ #
# HEADER                                                              #
# ------------------------------------------------------------------ #

st.markdown("## 📐 Tamanho de Mercado — TAM, SAM e SOM")
st.caption(
    "Dimensionamento do potencial financeiro da plataforma como um funil: do cenário "
    "mais amplo (teórico) até a parcela realista que conseguimos atender e conquistar."
)

ctx1, ctx2, ctx3, ctx4 = st.columns(4)
ctx1.metric("Produção de leite — Brasil (2023)", "35,4 bi L", delta="IBGE", delta_color="off")
ctx2.metric("Produtores formais — Brasil", "~150 mil", delta="MilkPoint Ventures 2023", delta_color="off")
ctx3.metric("Produção de leite — Goiás (2023)", "2,2 bi L", delta="IBGE · 6º maior estado", delta_color="off")
ctx4.metric("Universo total (incl. informais)", "1,18 mi", delta="Censo Agro 2017", delta_color="off")

st.write("")

with st.expander("ℹ️ O que significam TAM, SAM e SOM"):
    st.markdown(
        "- **TAM — Total Addressable Market:** mercado total teórico. Toda a demanda "
        "possível se 100% dos produtores comerciais do Brasil usassem a plataforma.\n"
        "- **SAM — Serviceable Available Market:** a parcela do TAM que o nosso modelo de "
        "negócio consegue atender — cadeias leiteiras premium do Centro-Oeste, via "
        "cooperativas e laticínios de médio porte.\n"
        "- **SOM — Serviceable Obtainable Market:** a fatia realista que conseguimos "
        "conquistar no curto prazo (3 anos), começando pelo Sul/Sudoeste Goiano."
    )

st.divider()

# ------------------------------------------------------------------ #
# PREMISSAS EDITÁVEIS                                                 #
# ------------------------------------------------------------------ #

with st.sidebar:
    st.markdown("### ⚙️ Premissas do modelo")
    st.caption("Ajuste ao vivo durante o pitch.")

    preco_mensal = st.slider(
        "Assinatura por produtor monitorado (R$/mês)",
        min_value=20, max_value=150, value=60, step=5,
        help="Preço B2B pago pelo laticínio/cooperativa por produtor integrado.",
    )

    tam_produtores = st.number_input(
        "TAM — produtores formais no Brasil",
        min_value=10_000, max_value=1_200_000, value=150_000, step=10_000,
        help="Produtores que entregam a laticínios sob inspeção. ~150 mil em 2023 "
             "(MilkPoint Ventures); universo total incl. informais ~1,18 mi (Censo Agro 2017).",
    )

    sam_pct = st.slider(
        "SAM — % do TAM atendível (Centro-Oeste / cadeias premium)",
        min_value=1, max_value=60, value=10, step=1,
        help="Goiás concentra ~6% da produção nacional; Centro-Oeste e cadeias premium ~10%.",
    )

    som_pct = st.slider(
        "SOM — % do SAM capturável em 3 anos (Sul Goiano)",
        min_value=1, max_value=60, value=30, step=1,
        help="Entrada via 10–15 cooperativas/laticínios médios do Sul/Sudoeste Goiano.",
    )

    st.divider()
    st.caption(
        "Receita = produtores × preço × 12 meses (ARR). "
        "Fontes: IBGE/PPM 2023 (produção), MilkPoint Ventures 2023 (~150 mil produtores "
        "formais), Censo Agropecuário 2017 (1,18 mi total)."
    )

# ------------------------------------------------------------------ #
# CÁLCULO                                                             #
# ------------------------------------------------------------------ #

sam_produtores = tam_produtores * sam_pct / 100
som_produtores = sam_produtores * som_pct / 100

arr = preco_mensal * 12  # receita anual por produtor
tam_rev = tam_produtores * arr
sam_rev = sam_produtores * arr
som_rev = som_produtores * arr

# ------------------------------------------------------------------ #
# CARDS                                                              #
# ------------------------------------------------------------------ #

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"<div style='background:{CORES['TAM']};border-radius:12px;padding:1.1rem 1.3rem'>"
        f"<div style='color:#cbd5e1;font-size:0.8rem;letter-spacing:.05em'>TAM · MERCADO TOTAL</div>"
        f"<div style='color:#fff;font-size:1.9rem;font-weight:700'>{_brl(tam_rev)}/ano</div>"
        f"<div style='color:#cbd5e1;font-size:0.9rem'>{_num(tam_produtores)} produtores · Brasil</div>"
        f"</div>", unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"<div style='background:{CORES['SAM']};border-radius:12px;padding:1.1rem 1.3rem'>"
        f"<div style='color:#dbeafe;font-size:0.8rem;letter-spacing:.05em'>SAM · MERCADO ATENDÍVEL</div>"
        f"<div style='color:#fff;font-size:1.9rem;font-weight:700'>{_brl(sam_rev)}/ano</div>"
        f"<div style='color:#dbeafe;font-size:0.9rem'>{_num(sam_produtores)} produtores · Centro-Oeste</div>"
        f"</div>", unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"<div style='background:{CORES['SOM']};border-radius:12px;padding:1.1rem 1.3rem'>"
        f"<div style='color:#dcfce7;font-size:0.8rem;letter-spacing:.05em'>SOM · ALVO 3 ANOS</div>"
        f"<div style='color:#fff;font-size:1.9rem;font-weight:700'>{_brl(som_rev)}/ano</div>"
        f"<div style='color:#dcfce7;font-size:0.9rem'>{_num(som_produtores)} produtores · Sul Goiano</div>"
        f"</div>", unsafe_allow_html=True,
    )

st.write("")

# ------------------------------------------------------------------ #
# FUNIL                                                              #
# ------------------------------------------------------------------ #

col_funil, col_tabela = st.columns([1.5, 1])

with col_funil:
    fig = go.Figure(go.Funnel(
        y=["TAM<br>Mercado total", "SAM<br>Atendível", "SOM<br>Alvo 3 anos"],
        x=[tam_rev, sam_rev, som_rev],
        textposition="inside",
        textinfo="value+percent initial",
        texttemplate="%{value:,.3s}  (%{percentInitial:.1%})",
        marker={"color": [CORES["TAM"], CORES["SAM"], CORES["SOM"]]},
        connector={"line": {"color": "#475569", "width": 1}},
    ))
    fig.update_layout(
        title="Funil de mercado — receita recorrente anual (ARR) potencial",
        height=420,
        margin=dict(t=60, b=20, l=10, r=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.markdown("#### Resumo do modelo")
    st.dataframe(
        {
            "Camada": ["TAM", "SAM", "SOM"],
            "Produtores": [_num(tam_produtores), _num(sam_produtores), _num(som_produtores)],
            "ARR potencial": [_brl(tam_rev), _brl(sam_rev), _brl(som_rev)],
        },
        use_container_width=True,
        hide_index=True,
    )
    st.metric(
        "Penetração do SOM no TAM",
        f"{(som_produtores / tam_produtores * 100):.2f}%",
        delta=f"{_num(som_produtores)} de {_num(tam_produtores)} produtores",
        delta_color="off",
    )
    st.caption(
        f"Premissa de preço: R$ {preco_mensal}/produtor/mês "
        f"(R$ {arr:,.0f}/ano por produtor).".replace(",", ".")
    )

st.divider()

# ------------------------------------------------------------------ #
# NARRATIVA DE PITCH                                                 #
# ------------------------------------------------------------------ #

st.markdown(
    f"""
<div style="background:#0f172a;border-left:4px solid #22c55e;padding:1.2rem 1.5rem;border-radius:8px">
<h4 style="color:#22c55e;margin:0 0 0.6rem 0">📢 Leitura para o pitch</h4>
<p style="color:#e2e8f0;line-height:1.7;margin:0">
O Brasil tem um mercado teórico (<strong>TAM</strong>) de <strong>{_brl(tam_rev)}/ano</strong> em
assinaturas de inteligência de risco para a cadeia leiteira. Nosso modelo — venda a
cooperativas e laticínios de médio porte do Centro-Oeste — endereça um
<strong>SAM</strong> de <strong>{_brl(sam_rev)}/ano</strong>. Começando pelo Sul/Sudoeste Goiano,
nossa meta realista de 3 anos (<strong>SOM</strong>) é <strong>{_brl(som_rev)}/ano</strong>,
com {_num(som_produtores)} produtores monitorados. É um mercado grande, com entrada
focada e expansão geográfica natural a partir de Goiás.
</p>
</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "VIA LEITE SENSE — Tamanho de Mercado | Fontes: IBGE/PPM 2023 (produção: BR 35,4 bi L, "
    "GO 2,2 bi L), MilkPoint Ventures 2023 (~150 mil produtores formais), IBGE Censo Agropecuário "
    "2017 (1,18 mi produtores). Contagem de produtores por camada é estimada a partir da participação "
    "na produção — ajuste conforme dados de validação. | USINA I.A. © 2026"
)
