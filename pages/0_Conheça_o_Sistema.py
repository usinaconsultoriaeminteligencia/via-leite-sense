"""
pages/0_Conheca_o_Sistema.py — Landing page pública VIA LEITE SENSE

Página de conversão para produtores e técnicos vindos de redes sociais.
Sem exigência de login. CTAs: testar demo ou deixar contato (WhatsApp).
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from dashboard_common import aplicar_css_nav

aplicar_css_nav()

# ── CSS da landing ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0a1628 0%, #0d2137 50%, #0a1f14 100%);
    }
    [data-testid="stHeader"]  { background: transparent !important; }
    [data-testid="stSidebar"] { background: #0d1b2a !important; }

    /* ── Seção hero ── */
    .lp-eyebrow {
        display: inline-block;
        background: rgba(74,144,226,.15);
        border: 1px solid rgba(74,144,226,.35);
        color: #93C5FD;
        border-radius: 20px;
        padding: .22rem .85rem;
        font-size: .78rem;
        font-weight: 600;
        letter-spacing: .05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .lp-headline {
        font-size: 2.8rem;
        font-weight: 900;
        color: #F0FFF4;
        letter-spacing: -1.5px;
        line-height: 1.12;
        margin-bottom: .5rem;
    }
    .lp-headline em {
        color: #4ADE80;
        font-style: normal;
    }
    .lp-sub {
        font-size: 1.1rem;
        color: #86EFAC;
        margin-bottom: 1rem;
        line-height: 1.55;
    }
    .lp-tagline {
        font-size: .93rem;
        color: #94A3B8;
        line-height: 1.65;
        margin-bottom: 1.6rem;
        max-width: 560px;
    }

    /* ── Dor ── */
    .lp-dor {
        background: rgba(239,68,68,.08);
        border: 1px solid rgba(239,68,68,.25);
        border-left: 4px solid #F87171;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        color: #FCA5A5;
        font-size: .97rem;
        line-height: 1.6;
        margin-bottom: 1.4rem;
        font-style: italic;
    }

    /* ── Benefícios ── */
    .lp-benefit {
        display: flex;
        align-items: flex-start;
        gap: .75rem;
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 12px;
        padding: .9rem 1.1rem;
        margin-bottom: .55rem;
    }
    .lp-benefit-icon {
        font-size: 1.6rem;
        flex-shrink: 0;
        margin-top: .05rem;
    }
    .lp-benefit-title {
        color: #F0FFF4;
        font-weight: 700;
        font-size: .95rem;
        margin-bottom: .15rem;
    }
    .lp-benefit-desc {
        color: #94A3B8;
        font-size: .83rem;
        line-height: 1.5;
    }

    /* ── Métricas ── */
    .lp-metrics {
        display: flex;
        gap: .6rem;
        margin-bottom: 1.6rem;
        flex-wrap: wrap;
    }
    .lp-metric {
        flex: 1;
        min-width: 100px;
        background: rgba(4,120,87,.18);
        border: 1px solid rgba(4,120,87,.4);
        border-radius: 12px;
        padding: .8rem .6rem;
        text-align: center;
    }
    .lp-metric-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #6EE7B7;
        line-height: 1;
    }
    .lp-metric-lbl {
        font-size: .67rem;
        color: #86EFAC;
        margin-top: .25rem;
        text-transform: uppercase;
        letter-spacing: .05em;
    }

    /* ── Depoimento / prova ── */
    .lp-proof {
        background: rgba(74,222,128,.07);
        border: 1px solid rgba(74,222,128,.2);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.4rem;
    }
    .lp-proof-text {
        color: #BBF7D0;
        font-size: .9rem;
        line-height: 1.6;
        font-style: italic;
    }
    .lp-proof-author {
        color: #4ADE80;
        font-size: .78rem;
        font-weight: 600;
        margin-top: .5rem;
    }

    /* ── Perfis de usuário ── */
    .lp-profile {
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.09);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: .55rem;
    }
    .lp-profile-header {
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .05em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }
    .lp-profile-item {
        font-size: .85rem;
        color: #CBD5E1;
        padding: .18rem 0;
        line-height: 1.5;
    }
    .lp-profile-item::before { content: "✓  "; color: #4ADE80; font-weight: 700; }
    .lp-profile-item.blocked { color: #64748B; }
    .lp-profile-item.blocked::before { content: "—  "; color: #475569; }

    /* ── CTA ── */
    .lp-cta-label {
        font-size: .72rem;
        color: #475569;
        text-align: center;
        margin-top: .3rem;
    }

    /* ── Rodapé ── */
    .lp-footer {
        text-align: center;
        color: #334155;
        font-size: .72rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,.05);
        line-height: 1.7;
    }

    /* ── Divisor de seção ── */
    .lp-section-label {
        font-size: .68rem;
        font-weight: 700;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: .1em;
        margin-bottom: .7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ───────────────────────────────────────────────────────────────────
def benefit(icon: str, title: str, desc: str) -> str:
    return (
        f'<div class="lp-benefit">'
        f'<div class="lp-benefit-icon">{icon}</div>'
        f'<div><div class="lp-benefit-title">{title}</div>'
        f'<div class="lp-benefit-desc">{desc}</div></div>'
        f'</div>'
    )


def metric(val: str, lbl: str) -> str:
    return (
        f'<div class="lp-metric">'
        f'<div class="lp-metric-val">{val}</div>'
        f'<div class="lp-metric-lbl">{lbl}</div>'
        f'</div>'
    )


# ── Layout ────────────────────────────────────────────────────────────────────
col_esq, col_dir = st.columns([1.5, 1], gap="large")

# ════════════════════════════════════════════════════════
# COLUNA ESQUERDA — conteúdo de conversão
# ════════════════════════════════════════════════════════
with col_esq:

    # Selo do evento — credibilidade institucional
    st.markdown(
        '<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.9rem">'

        '<div style="display:inline-flex;align-items:center;gap:.45rem;'
        'background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.35);'
        'border-radius:20px;padding:.22rem .9rem">'
        '<span style="font-size:.85rem">🏆</span>'
        '<span style="font-size:.75rem;font-weight:700;color:#86EFAC;'
        'letter-spacing:.04em;text-transform:uppercase">'
        'Desafio AgroStartup 2026 · SENAR / SEBRAE Goiás'
        '</span>'
        '</div>'

        '<div style="display:inline-flex;align-items:center;gap:.45rem;'
        'background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);'
        'border-radius:20px;padding:.22rem .9rem">'
        '<span style="font-size:.85rem">📅</span>'
        '<span style="font-size:.75rem;font-weight:700;color:#FDE68A;'
        'letter-spacing:.04em;text-transform:uppercase">'
        'Apresentação final — 27 de junho'
        '</span>'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )

    # Eyebrow
    st.markdown(
        '<div class="lp-eyebrow">🥛 Para laticínios e cooperativas leiteiras</div>',
        unsafe_allow_html=True,
    )

    # Headline — a dor em forma de pergunta
    st.markdown(
        '<h1 class="lp-headline">'
        'Você só descobre que o produtor<br>'
        'vai parar de fornecer<br>'
        '<em>quando ele já parou.</em>'
        '</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="lp-sub">'
        'VIA LEITE SENSE antecipa quedas de volume e qualidade '
        '<strong style="color:#F0FFF4">7 dias antes</strong> — '
        'para você agir no campo, não apagar incêndio.'
        '</p>',
        unsafe_allow_html=True,
    )

    # Métricas do modelo
    st.markdown(
        '<div class="lp-metrics">'
        + metric("99,4%", "Acurácia R²")
        + metric("3,7%", "Erro médio")
        + metric("107", "Variáveis IA")
        + metric("7 dias", "Antecedência")
        + '</div>',
        unsafe_allow_html=True,
    )

    # Separador
    st.markdown('<div class="lp-section-label">O que a plataforma faz por você</div>', unsafe_allow_html=True)

    # Benefícios
    st.markdown(
        benefit(
            "🧠",
            "Previsão de captação por produtor",
            "IA treinada com clima, manejo, logística e histórico de cada fazenda — "
            "antecipa quem vai cair antes do caminhão sair.",
        )
        + benefit(
            "⚠️",
            "Alerta de risco automático",
            "Score de risco por fazenda com gauge visual e recomendação de ação: "
            "quem ligar primeiro, o que perguntar, o que verificar.",
        )
        + benefit(
            "🌡️",
            "Clima e estresse térmico em tempo real",
            "THI por polo climático (Rio Verde, Jataí, Mineiros) — "
            "quando o calor ameaça a produção, o sistema avisa antes.",
        )
        + benefit(
            "📋",
            "Plano de ação em 1 clique",
            "Selecione o produtor, escolha o problema — o formulário preenche sozinho "
            "com orientação técnica e prazo sugerido.",
        )
        + benefit(
            "📄",
            "Relatório PDF por fazenda",
            "Score, histórico, alertas e recomendações em um PDF profissional "
            "para reuniões de campo ou envio ao produtor.",
        ),
        unsafe_allow_html=True,
    )

    # Prova / contexto
    st.markdown(
        '<div class="lp-proof">'
        '<div class="lp-proof-text">'
        '"O Sul Goiano responde por mais de 60% da captação leiteira de Goiás. '
        'Uma queda de 5% no volume de um polo inteiro compromete toda a programação '
        'de produção de derivados premium naquele mês."'
        '</div>'
        '<div class="lp-proof-author">— Contexto da cadeia leiteira do Centro-Oeste</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Rodapé
    st.markdown(
        '<div class="lp-footer">'
        'Desenvolvido por <strong>Fagner Vieira</strong> · '
        'Graduando em Inteligência Artificial — SENAI FATESG · 4º Período · Goiânia-GO<br>'
        '<strong>USINA I.A. Tecnologia e Inovação</strong> · '
        'Projeto em seleção no Desafio AgroStartup 2026 — SENAR / SEBRAE Goiás<br>'
        '<a href="mailto:fagnerpro80@gmail.com" style="color:#4ADE80;text-decoration:none">'
        'fagnerpro80@gmail.com</a>'
        '</div>',
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════════
# COLUNA DIREITA — CTAs + perfis de acesso
# ════════════════════════════════════════════════════════
with col_dir:

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA 1 — Demo gratuito ─────────────────────────────────────────────
    st.markdown(
        '<div style="background:rgba(4,120,87,.18);border:1px solid rgba(74,222,128,.3);'
        'border-radius:16px;padding:1.4rem 1.4rem 1rem 1.4rem;margin-bottom:1rem">'

        '<div style="font-size:.7rem;color:#4ADE80;font-weight:700;'
        'text-transform:uppercase;letter-spacing:.08em;margin-bottom:.4rem">'
        '🎯 Avalie agora — sem compromisso'
        '</div>'

        '<div style="font-size:1.15rem;font-weight:800;color:#F0FFF4;'
        'margin-bottom:.4rem;line-height:1.3">'
        'Acesse o sistema completo<br>com login de demonstração'
        '</div>'

        '<div style="font-size:.85rem;color:#86EFAC;margin-bottom:.9rem;line-height:1.5">'
        'Veja todos os dashboards, scores por produtor, '
        'alertas de clima e o tour guiado de 5 minutos.'
        '</div>'

        '<div style="background:rgba(0,0,0,.2);border-radius:8px;'
        'padding:.6rem .9rem;margin-bottom:.4rem">'
        '<span style="font-size:.78rem;color:#64748B">Usuário: </span>'
        '<code style="background:rgba(74,222,128,.15);color:#6EE7B7;'
        'padding:.1rem .4rem;border-radius:4px;font-size:.85rem">demo</code>'
        '&nbsp;&nbsp;'
        '<span style="font-size:.78rem;color:#64748B">Senha: </span>'
        '<code style="background:rgba(74,222,128,.15);color:#6EE7B7;'
        'padding:.1rem .4rem;border-radius:4px;font-size:.85rem">demo2025</code>'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )

    st.page_link(
        "via_leite_app.py",
        label="→ Acessar o sistema agora",
        icon="🚀",
        use_container_width=True,
    )
    st.markdown(
        '<div class="lp-cta-label">Acesso imediato · Sem cadastro · Dados simulados</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA 2 — Contato WhatsApp ──────────────────────────────────────────
    st.markdown(
        '<div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.1);'
        'border-radius:16px;padding:1.4rem 1.4rem 1rem 1.4rem;margin-bottom:.7rem">'

        '<div style="font-size:.7rem;color:#FDE68A;font-weight:700;'
        'text-transform:uppercase;letter-spacing:.08em;margin-bottom:.4rem">'
        '📅 Apresentação final dia 27 — preciso da sua opinião antes'
        '</div>'

        '<div style="font-size:1.05rem;font-weight:700;color:#F0FFF4;'
        'margin-bottom:.4rem;line-height:1.35">'
        'Me ajude a validar se isso<br>resolve uma dor real do campo'
        '</div>'

        '<div style="font-size:.83rem;color:#94A3B8;margin-bottom:.9rem;line-height:1.55">'
        'O projeto está em seleção no Desafio AgroStartup 2026 (SENAR/SEBRAE Goiás). '
        'Os organizadores pediram validação com profissionais do setor antes da apresentação. '
        'Não é venda — é uma conversa de 15 minutos sobre o que você viu no sistema.'
        '</div>'

        '</div>',
        unsafe_allow_html=True,
    )

    # Botão WhatsApp via link externo
    components.html(
        """
        <a href="https://wa.me/5562988880016?text=Ol%C3%A1%2C%20Fagner%21%20Vi%20o%20VIA%20LEITE%20SENSE%20e%20gostaria%20de%20conversar%20sobre%20o%20projeto%20antes%20da%20apresenta%C3%A7%C3%A3o%20do%20AgroStartup%20no%20dia%2027."
           target="_blank"
           style="
               display: block;
               background: linear-gradient(135deg, #25D366, #128C7E);
               color: #fff;
               text-align: center;
               padding: .65rem 1rem;
               border-radius: 10px;
               font-size: .92rem;
               font-weight: 700;
               text-decoration: none;
               letter-spacing: .01em;
           ">
            💬 Falar no WhatsApp
        </a>
        <div style="color:#475569;font-size:.72rem;text-align:center;margin-top:.4rem">
            Resposta em até 24h · Piloto sem custo
        </div>
        """,
        height=60,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Perfis de acesso ──────────────────────────────────────────────────
    st.markdown(
        '<div class="lp-section-label">O que cada perfil acessa</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        # Demo
        '<div class="lp-profile">'
        '<div class="lp-profile-header" style="color:#93C5FD">👁️ Avaliador (demo)</div>'
        '<div class="lp-profile-item">Todos os dashboards e análises</div>'
        '<div class="lp-profile-item">Scores de risco por fazenda</div>'
        '<div class="lp-profile-item">Clima, THI e alertas IoT</div>'
        '<div class="lp-profile-item">Tour de demonstração guiado</div>'
        '<div class="lp-profile-item blocked">Cadastro de fazendas</div>'
        '<div class="lp-profile-item blocked">Planos de ação e exportação PDF</div>'
        '</div>'

        # Laticínio
        '<div class="lp-profile">'
        '<div class="lp-profile-header" style="color:#4ADE80">🏭 Operador (laticínio contratado)</div>'
        '<div class="lp-profile-item">Tudo do perfil avaliador</div>'
        '<div class="lp-profile-item">Cadastro e gestão de fazendas</div>'
        '<div class="lp-profile-item">Criação e acompanhamento de planos</div>'
        '<div class="lp-profile-item">Exportação de relatórios PDF</div>'
        '<div class="lp-profile-item">Lançamentos gerenciais e histórico</div>'
        '</div>',
        unsafe_allow_html=True,
    )
