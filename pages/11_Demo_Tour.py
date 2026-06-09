"""
pages/11_Demo_Tour.py — Modo Demonstração VIA LEITE SENSE
Tour guiado de 5 minutos para pitch · USINA I.A.
"""
from __future__ import annotations

import time

import streamlit as st
import streamlit.components.v1 as components

from auth import esta_autenticado

# Guard: redireciona para login se não autenticado
if not esta_autenticado():
    st.warning("🔒 Acesso restrito. Faça login na página principal.")
    st.page_link("via_leite_app.py", label="→ Ir para o Login", icon="🏠")
    st.stop()

# ── CSS específico do tour ────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0a1628 0%, #0d2137 50%, #0a1f14 100%);
    }
    [data-testid="stHeader"]  { background: transparent !important; }
    [data-testid="stSidebar"] { background: #0d1b2a !important; }

    .demo-chip {
        display:inline-block;
        background:rgba(74,222,128,.15);
        border:1px solid rgba(74,222,128,.4);
        color:#4ADE80;
        border-radius:20px;
        padding:.2rem .85rem;
        font-size:.75rem;
        font-weight:700;
        letter-spacing:.06em;
        text-transform:uppercase;
        margin-bottom:.6rem;
    }
    .demo-slide-title {
        font-size:2.4rem;
        font-weight:900;
        color:#F0FFF4;
        letter-spacing:-1px;
        line-height:1.15;
        margin-bottom:.3rem;
    }
    .demo-slide-sub {
        font-size:1.05rem;
        color:#86EFAC;
        margin-bottom:1.2rem;
    }
    .demo-step-card {
        background:rgba(255,255,255,.05);
        border:1px solid rgba(255,255,255,.1);
        border-radius:12px;
        padding:1rem 1.2rem;
        margin-bottom:.6rem;
    }
    .demo-step-num {
        font-size:.72rem;
        color:#4ADE80;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:.06em;
    }
    .demo-step-text {
        font-size:.92rem;
        color:#E2E8F0;
        line-height:1.55;
        margin-top:.15rem;
    }
    .demo-timer-box {
        background:rgba(74,222,128,.08);
        border:1px solid rgba(74,222,128,.25);
        border-radius:10px;
        padding:.7rem 1rem;
        text-align:center;
        font-size:1.8rem;
        font-weight:800;
        color:#4ADE80;
        letter-spacing:.02em;
        font-family:monospace;
    }
    .demo-nav-hint {
        color:#475569;
        font-size:.78rem;
        text-align:center;
        margin-top:.5rem;
    }
    .demo-pill {
        display:inline-block;
        background:rgba(74,144,226,.18);
        border:1px solid rgba(74,144,226,.35);
        color:#93C5FD;
        border-radius:6px;
        padding:.1rem .55rem;
        font-size:.78rem;
        font-weight:600;
        margin:.1rem .1rem;
    }
    .demo-highlight {
        background:rgba(74,222,128,.12);
        border-left:3px solid #4ADE80;
        border-radius:0 8px 8px 0;
        padding:.6rem .9rem;
        color:#BBF7D0;
        font-size:.88rem;
        line-height:1.5;
        margin-bottom:.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Dados dos slides ──────────────────────────────────────────────────────────
SLIDES = [
    {
        "numero": "01 / 06",
        "chip": "🎯 Abertura  ·  0:00 – 0:45",
        "titulo": "O Problema\nda Cadeia Leiteira",
        "subtitulo": "Por que o laticínio perde leite antes de saber que está perdendo?",
        "pagina_link": None,
        "pagina_label": None,
        "highlight": "30% do leite descartado no Brasil poderia ser evitado com monitoramento antecipado de qualidade e volume.",
        "roteiro": [
            ("Contexto", "O laticínio coleta leite de dezenas de produtores — qualquer queda de 5% no volume é crítica para o plano de produção."),
            ("Dor real", "Gestores só sabem do problema quando o caminhão volta com leite rejeitado ou o produtor para de fornecer."),
            ("Nossa solução", "VIA LEITE SENSE antecipa quedas 7 dias antes usando IA preditiva com 107 variáveis: clima, manejo, logística e histórico."),
        ],
    },
    {
        "numero": "02 / 06",
        "chip": "📊 Painel Executivo  ·  0:45 – 1:30",
        "titulo": "Inteligência\nem Tempo Real",
        "subtitulo": "KPIs de captação, desvio e previsão numa única visão.",
        "pagina_link": "pages/1_Executivo.py",
        "pagina_label": "→ Abrir Painel Executivo",
        "highlight": "Modelo XGBoost treinado com 107 variáveis · R² 99,4% · sMAPE 3,7%",
        "roteiro": [
            ("O que mostrar", "Total captado vs. previsto · Desvio por polo climático · Top 5 produtores em risco."),
            ("Ponto de impacto", "O gráfico 'Volume coletado × previsto' revela onde o modelo acertou e onde o campo surpreendeu."),
            ("Frase de efeito", "'Em 7 dias você já sabe o que vai acontecer no laticínio — antes de qualquer ligação de campo.'"),
        ],
    },
    {
        "numero": "03 / 06",
        "chip": "🏭 Fazenda 360  ·  1:30 – 2:30",
        "titulo": "Score Premium\nVisual por Produtor",
        "subtitulo": "Gauge de risco · Radar 4D · Recomendação automatizada.",
        "pagina_link": "pages/6_Fornecedores_360.py",
        "pagina_label": "→ Abrir Fazenda 360",
        "highlight": "Score composto: Volume 35% · Qualidade 30% · Logística 20% · Continuidade 15%",
        "roteiro": [
            ("O que mostrar", "Selecionar um produtor Alto Risco → mostrar o gauge vermelho + radar 4D desequilibrado."),
            ("Drill-down", "Trocar para um produtor Baixo Risco → gauge verde, radar equilibrado. Contraste visual imediato."),
            ("Recomendação IA", "Mostrar o box de recomendação gerado automaticamente: 'Priorizar contato de campo para proteger volume.'"),
        ],
    },
    {
        "numero": "04 / 06",
        "chip": "🌡️ VIA LEITE EDGE  ·  2:30 – 3:30",
        "titulo": "IoT-Ready:\nDo Sensor à Decisão",
        "subtitulo": "Telemetria de tanque, THI e score premium com arquitetura preparada para sensores reais.",
        "pagina_link": "pages/7_VIA_LEITE_EDGE.py",
        "pagina_label": "→ Abrir VIA LEITE EDGE",
        "highlight": "THI > 72 = estresse térmico. Score tanque < 60 = risco de perda de qualidade. Alertas automáticos.",
        "roteiro": [
            ("O que mostrar", "Dashboard EDGE com telemetria simulada em tempo real · temperatura do tanque · THI atual."),
            ("Arquitetura", "Mostrar que o sistema já aceita dados de sensores reais via MQTT — é só trocar o provider."),
            ("Premium", "Score de tanque calculado em tempo real — quanto mais verde, mais leite A/B entregue ao mercado premium."),
        ],
    },
    {
        "numero": "05 / 06",
        "chip": "📋 Plano de Ação  ·  3:30 – 4:30",
        "titulo": "Do Diagnóstico\nà Ação em 1 Clique",
        "subtitulo": "15 prompts técnicos inteligentes · Persistência em banco · Acompanhamento de resultados.",
        "pagina_link": "pages/10_Plano_de_Acao.py",
        "pagina_label": "→ Abrir Plano de Ação",
        "highlight": "Selecione o produtor → escolha o prompt → clique → formulário preenchido automaticamente.",
        "roteiro": [
            ("O que mostrar", "Selecionar produtor com risco Alto → clicar no prompt 'Queda de volume > 10%' → ver o formulário preencher sozinho."),
            ("Persistência", "Salvar o plano e mostrar no painel geral com KPIs de planos abertos, em andamento e concluídos."),
            ("Resultado", "'Isso é o ciclo completo: IA detecta → gestor decide → sistema registra e acompanha o resultado.'"),
        ],
    },
    {
        "numero": "06 / 06",
        "chip": "🏁 Encerramento  ·  4:30 – 5:00",
        "titulo": "Pronto para\no Mercado Premium",
        "subtitulo": "ESG · Rastreabilidade · Escalabilidade para a cadeia leiteira do Centro-Oeste.",
        "pagina_link": None,
        "pagina_label": None,
        "highlight": "URL ao vivo: https://via-leite-sense.streamlit.app · Login demo / demo2025",
        "roteiro": [
            ("ESG", "Cada descarte evitado é CO₂ não emitido e litros a mais de leite A/B para mercados de alto valor."),
            ("Escalabilidade", "A arquitetura suporta N laticínios, N rotas, dados reais de sensores e integração com ERPs via API."),
            ("Call to action", "'Qual laticínio do grupo teria mais a ganhar sendo o primeiro a usar isso?' — abrir para perguntas."),
        ],
    },
]

# ── Session state ─────────────────────────────────────────────────────────────
if "demo_slide" not in st.session_state:
    st.session_state.demo_slide = 0
if "demo_timer_inicio" not in st.session_state:
    st.session_state.demo_timer_inicio = None

slide_idx = st.session_state.demo_slide
slide = SLIDES[slide_idx]
total = len(SLIDES)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;margin-bottom:.3rem">'
    '<span class="demo-chip">🎬 MODO DEMONSTRAÇÃO · PITCH 5 MIN</span>'
    "</div>",
    unsafe_allow_html=True,
)

prog_val = (slide_idx + 1) / total
st.progress(prog_val, text=f"Slide {slide_idx + 1} de {total}  ·  {slide['chip']}")

st.divider()

# ── Layout principal ──────────────────────────────────────────────────────────
col_slide, col_roteiro, col_timer = st.columns([1.7, 1.5, 0.9])

with col_slide:
    st.markdown(
        f'<div class="demo-chip">{slide["numero"]}</div>',
        unsafe_allow_html=True,
    )
    # Título com quebra de linha
    for linha in slide["titulo"].split("\n"):
        st.markdown(f'<span class="demo-slide-title">{linha}</span>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="demo-slide-sub">{slide["subtitulo"]}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="demo-highlight">💡 {slide["highlight"]}</div>',
        unsafe_allow_html=True,
    )
    if slide["pagina_link"]:
        st.page_link(slide["pagina_link"], label=slide["pagina_label"], icon="🔗")

with col_roteiro:
    st.markdown(
        '<div style="font-size:.7rem;color:#4ADE80;font-weight:700;'
        'text-transform:uppercase;letter-spacing:.08em;margin-bottom:.5rem">'
        "📜 Roteiro do apresentador"
        "</div>",
        unsafe_allow_html=True,
    )
    for titulo_passo, texto_passo in slide["roteiro"]:
        st.markdown(
            f'<div class="demo-step-card">'
            f'<div class="demo-step-num">{titulo_passo}</div>'
            f'<div class="demo-step-text">{texto_passo}</div>'
            "</div>",
            unsafe_allow_html=True,
        )

with col_timer:
    st.markdown(
        '<div style="font-size:.7rem;color:#4ADE80;font-weight:700;'
        'text-transform:uppercase;letter-spacing:.08em;margin-bottom:.5rem">'
        "⏱ Cronômetro"
        "</div>",
        unsafe_allow_html=True,
    )

    # Tempo alvo por slide (segundos)
    tempos_alvo = [45, 90, 150, 210, 270, 300]
    alvo = tempos_alvo[slide_idx]
    mm, ss = divmod(alvo, 60)
    st.markdown(
        f'<div style="font-size:.7rem;color:#475569;margin-bottom:.4rem">'
        f"Meta deste slide: {mm}:{ss:02d}"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("▶ Iniciar / Reiniciar", use_container_width=True):
        st.session_state.demo_timer_inicio = time.time()
        st.rerun()

    if st.session_state.demo_timer_inicio:
        # Calcula segundos já decorridos no momento do render
        _elapsed_base = int(time.time() - st.session_state.demo_timer_inicio)
        # Timer JS: tica no browser sem nenhum rerun do servidor
        components.html(
            f"""
            <style>
            #vls-timer {{
                background: rgba(74,222,128,.08);
                border: 1px solid rgba(74,222,128,.25);
                border-radius: 10px;
                padding: 10px 14px;
                text-align: center;
                font-size: 2rem;
                font-weight: 800;
                font-family: monospace;
                letter-spacing: .02em;
                color: #4ADE80;
            }}
            #vls-over {{
                margin-top: 6px;
                text-align: center;
                font-size: .78rem;
                color: #F87171;
                font-weight: 600;
                display: none;
            }}
            </style>
            <div id="vls-timer">0:00</div>
            <div id="vls-over">⚠️ Tempo do slide ultrapassado!</div>
            <script>
            var elapsed = {_elapsed_base};
            var alvo   = {alvo};
            function tick() {{
                var m = Math.floor(elapsed / 60);
                var s = elapsed % 60;
                var txt = m + ':' + (s < 10 ? '0' : '') + s;
                var el = document.getElementById('vls-timer');
                var ov = document.getElementById('vls-over');
                if (!el) return;
                el.textContent = txt;
                if (elapsed > alvo) {{
                    el.style.color = '#F87171';
                    if (ov) ov.style.display = 'block';
                }} else {{
                    el.style.color = '#4ADE80';
                }}
                elapsed++;
            }}
            tick();
            setInterval(tick, 1000);
            </script>
            """,
            height=90,
        )
    else:
        st.markdown(
            '<div class="demo-timer-box" style="color:#334155">0:00</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Tempo total desde o início do tour
    if st.session_state.demo_timer_inicio and slide_idx == 0:
        pass  # reinicia a cada slide
    st.markdown(
        f'<div class="demo-nav-hint">Slide {slide_idx + 1}/{total}</div>',
        unsafe_allow_html=True,
    )

# ── Navegação ─────────────────────────────────────────────────────────────────
st.divider()

nav_left, nav_mid, nav_right = st.columns([1, 2, 1])

with nav_left:
    if slide_idx > 0:
        if st.button("◀ Anterior", use_container_width=True):
            st.session_state.demo_slide -= 1
            st.session_state.demo_timer_inicio = None
            st.rerun()

with nav_mid:
    # Índice rápido por botões de ponto
    cols_dots = st.columns(total)
    for i, dot_col in enumerate(cols_dots):
        cor = "#4ADE80" if i == slide_idx else "#1E3A5F"
        dot_col.markdown(
            f'<div style="text-align:center;cursor:pointer;'
            f'width:14px;height:14px;border-radius:50%;'
            f'background:{cor};margin:0 auto;margin-top:10px"></div>',
            unsafe_allow_html=True,
        )

with nav_right:
    if slide_idx < total - 1:
        if st.button("Próximo ▶", use_container_width=True, type="primary"):
            st.session_state.demo_slide += 1
            st.session_state.demo_timer_inicio = None
            st.rerun()
    else:
        if st.button("🔄 Recomeçar", use_container_width=True):
            st.session_state.demo_slide = 0
            st.session_state.demo_timer_inicio = None
            st.rerun()

# ── Atalhos de teclado (hint) ─────────────────────────────────────────────────
st.markdown(
    '<div class="demo-nav-hint" style="margin-top:.5rem">'
    "Use os botões ◀ / ▶ para navegar · Clique em ▶ Iniciar para cronometrar cada slide"
    "</div>",
    unsafe_allow_html=True,
)

# ── Barra lateral — visão geral do roteiro ────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗺️ Mapa do Pitch")
    for i, s in enumerate(SLIDES):
        ativo = "→ " if i == slide_idx else "   "
        cor = "#4ADE80" if i == slide_idx else "#475569"
        st.markdown(
            f'<div style="color:{cor};font-size:.83rem;padding:.15rem 0">'
            f"{ativo}{s['numero']}  {s['chip'].split('·')[0].strip()}"
            "</div>",
            unsafe_allow_html=True,
        )
    st.divider()
    st.caption("**VIA LEITE SENSE**\nPitch · Maratona FATESG 2025\nUSINA I.A.")
