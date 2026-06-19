# -*- coding: utf-8 -*-
"""
gerar_prototipo.py — VIA LEITE SENSE
Gera o PDF de prototipagem de alta fidelidade para a apresentação
(AgroStartup SENAR/SEBRAE GO 2026): identidade visual + telas do produto
+ conceito de bot WhatsApp + funil de mercado + QR code da demo.

Saída: prototipo/VIA_LEITE_SENSE_Prototipo.pdf
Render 100% vetorial via reportlab (sem dependência de browser/Figma).
"""
import os
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "VIA_LEITE_SENSE_Prototipo.pdf")
QR_PNG = os.path.join(HERE, "qr_demo.png")
DEMO_URL = "https://via-leite-sense.streamlit.app"

W, H = landscape(A4)  # 842 x 595 pt

# ------------------------------------------------------------------ #
# PALETA — IDENTIDADE VIA LEITE SENSE                                 #
# ------------------------------------------------------------------ #
BG_DEEP  = HexColor("#08161F")  # Azul Abissal — fundo
BG_PANEL = HexColor("#0F2A38")  # Petróleo — painéis
CARD     = HexColor("#13313F")  # Cartão
CARD_HI  = HexColor("#173C4D")
LINE     = HexColor("#21485A")
CYAN     = HexColor("#19D3E6")  # Ciano Sense (tech / radar)
TEAL     = HexColor("#0EA5B5")
GREEN    = HexColor("#34D399")  # Verde Leite (ESG / positivo)
GREEN2   = HexColor("#22C55E")
AMBER    = HexColor("#F59E0B")  # Atenção
RED      = HexColor("#EF4444")  # Risco
PURPLE   = HexColor("#A78BFA")  # Crítico
INK      = HexColor("#EAF4F8")  # Texto claro
MUTED    = HexColor("#8FA8B5")  # Texto secundário
WHITE    = HexColor("#FFFFFF")
WA_GREEN = HexColor("#128C7E")  # WhatsApp header
WA_BUBBLE= HexColor("#DCF8C6")  # WhatsApp balão enviado

# ------------------------------------------------------------------ #
# FONTES (Windows) com fallback                                      #
# ------------------------------------------------------------------ #
def _reg(name, filename):
    try:
        pdfmetrics.registerFont(TTFont(name, f"C:/Windows/Fonts/{filename}"))
        return name
    except Exception:
        return None

FT_DISP = _reg("Disp", "bahnschrift.ttf") or "Helvetica-Bold"
FT_BOLD = _reg("SB", "segoeuib.ttf") or "Helvetica-Bold"
FT_SEMI = _reg("SSB", "seguisb.ttf") or "Helvetica-Bold"
FT_REG  = _reg("S", "segoeui.ttf") or "Helvetica"
FT_LIGHT= _reg("SL", "segoeuil.ttf") or "Helvetica"
FT_SEMIL= _reg("SSL", "segoeuisl.ttf") or "Helvetica"

# ------------------------------------------------------------------ #
# HELPERS                                                            #
# ------------------------------------------------------------------ #
def grad_rect(c, x, y, w, h, c1, c2, vertical=True):
    c.saveState()
    p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
    if vertical:
        c.linearGradient(x, y + h, x, y, (c1, c2), (0, 1), extend=True)
    else:
        c.linearGradient(x, y, x + w, y, (c1, c2), (0, 1), extend=True)
    c.restoreState()

def text(c, x, y, s, font, size, color, align="l", tracking=0):
    c.setFillColor(color); c.setFont(font, size)
    if not tracking:
        if align == "c":
            c.drawCentredString(x, y, s)
        elif align == "r":
            c.drawRightString(x, y, s)
        else:
            c.drawString(x, y, s)
        return
    widths = [c.stringWidth(ch, font, size) for ch in s]
    total = sum(widths) + tracking * max(0, len(s) - 1)
    if align == "c":
        cx = x - total / 2
    elif align == "r":
        cx = x - total
    else:
        cx = x
    for ch, w in zip(s, widths):
        c.drawString(cx, y, ch); cx += w + tracking

def chip(c, x, y, label, fg, bg, font=None, size=8.5, padx=8, ph=16):
    font = font or FT_SEMI
    c.setFont(font, size)
    tw = c.stringWidth(label, font, size)
    c.setFillColor(bg); c.roundRect(x, y, tw + padx * 2, ph, ph / 2, fill=1, stroke=0)
    text(c, x + padx, y + (ph - size) / 2 + 0.5, label, font, size, fg)
    return tw + padx * 2

def droplet(c, cx, cy, r, color):
    p = c.beginPath()
    p.moveTo(cx, cy + 2.0 * r)
    p.curveTo(cx - 0.25 * r, cy + 1.25 * r, cx - r, cy + 0.65 * r, cx - r, cy)
    p.curveTo(cx - r, cy - 0.95 * r, cx + r, cy - 0.95 * r, cx + r, cy)
    p.curveTo(cx + r, cy + 0.65 * r, cx + 0.25 * r, cy + 1.25 * r, cx, cy + 2.0 * r)
    p.close()
    c.setFillColor(color); c.drawPath(p, fill=1, stroke=0)

def pulse(c, cx, cy, color, scale=1.0):
    """Sinal de radar (dot + 2 arcos) — dentro da gota."""
    c.setStrokeColor(color); c.setLineWidth(2.2 * scale); c.setLineCap(1)
    c.setFillColor(color)
    c.circle(cx, cy, 2.6 * scale, fill=1, stroke=0)
    for i, rr in enumerate((9, 15)):
        rr *= scale
        c.arc(cx - rr, cy - rr, cx + rr, cy + rr, 35, 110)

def logo(c, x, y, size=46, stacked=False, mono=None):
    """Marca VIA LEITE SENSE. x,y = base-left do texto."""
    r = size * 0.30
    cx = x + r
    cy = y + size * 0.18
    if mono:
        droplet(c, cx, cy, r, mono)
        pulse(c, cx, cy + r * 0.15, BG_DEEP, scale=size / 46)
    else:
        # gota com gradiente ciano->verde (clip na própria gota)
        c.saveState()
        p = c.beginPath()
        p.moveTo(cx, cy + 2.0 * r)
        p.curveTo(cx - 0.25 * r, cy + 1.25 * r, cx - r, cy + 0.65 * r, cx - r, cy)
        p.curveTo(cx - r, cy - 0.95 * r, cx + r, cy - 0.95 * r, cx + r, cy)
        p.curveTo(cx + r, cy + 0.65 * r, cx + 0.25 * r, cy + 1.25 * r, cx, cy + 2.0 * r)
        p.close()
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(cx - r, cy - r, cx + r, cy + 2 * r, (GREEN, CYAN), (0, 1), extend=True)
        c.restoreState()
        pulse(c, cx, cy + r * 0.15, BG_DEEP, scale=size / 46)
    tx = x + 2 * r + size * 0.30
    wordc = mono or INK
    if stacked:
        text(c, tx, y + size * 0.42, "VIA LEITE", FT_DISP, size * 0.52, wordc)
        text(c, tx, y + size * 0.06, "SENSE", FT_DISP, size * 0.52, mono or CYAN, tracking=size * 0.04)
    else:
        c.setFont(FT_DISP, size * 0.52)
        text(c, tx, y + size * 0.16, "VIA LEITE ", FT_DISP, size * 0.52, wordc)
        wlt = c.stringWidth("VIA LEITE ", FT_DISP, size * 0.52)
        text(c, tx + wlt, y + size * 0.16, "SENSE", FT_DISP, size * 0.52, mono or CYAN)

def footer(c, page_label):
    text(c, 40, 24, "Tecnologia desenvolvida por USINA I.A.  ·  IA aplicada ao agronegócio — Goiânia/GO",
         FT_REG, 7.5, MUTED)
    text(c, W - 40, 24, page_label, FT_SEMI, 7.5, MUTED, align="r")
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(40, 36, W - 40, 36)

def page_bg(c, panel=False):
    grad_rect(c, 0, 0, W, H, BG_PANEL, BG_DEEP)

def card(c, x, y, w, h, fill=CARD, radius=10, border=None):
    if border:
        c.setStrokeColor(border); c.setLineWidth(1)
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if border else 0)

def section_title(c, x, y, kicker, title, accent=CYAN):
    c.setFillColor(accent); c.roundRect(x, y + 2, 26, 4, 2, fill=1, stroke=0)
    text(c, x + 34, y, kicker.upper(), FT_SEMI, 9, accent, tracking=1.5)
    text(c, x, y - 26, title, FT_DISP, 26, INK)

# ================================================================== #
# PÁGINA 1 — CAPA                                                     #
# ================================================================== #
def page_cover(c):
    grad_rect(c, 0, 0, W, H, BG_PANEL, BG_DEEP)
    # halo radial suave
    c.saveState()
    pth = c.beginPath(); pth.rect(0, 0, W, H); c.clipPath(pth, stroke=0, fill=0)
    c.radialGradient(W * 0.74, H * 0.62, 360, (HexColor("#10455A"), BG_DEEP), (0, 1), extend=True)
    c.restoreState()

    chip(c, 60, H - 86, "DESAFIO AGROSTARTUP · SENAR/SEBRAE GOIÁS 2026", CYAN, HexColor("#0c3340"))

    # marca grande
    logo(c, 60, H - 250, size=120, stacked=True)

    text(c, 64, 232, "Radar de Risco da Cadeia Leiteira", FT_LIGHT, 30, INK)
    text(c, 64, 198, "Antecipa queda de produção, perda de qualidade e risco de", FT_REG, 14, MUTED)
    text(c, 64, 178, "penalização — antes que a perda aconteça.", FT_REG, 14, MUTED)

    # tags de valor
    tx = 64
    for t, col in [("IA Preditiva", CYAN), ("Qualidade & ESG", GREEN), ("Clima INMET", AMBER), ("IoT-ready", PURPLE)]:
        tx += chip(c, tx, 132, t, col, HexColor("#0c2c39")) + 10

    text(c, 64, 86, "PROTÓTIPO DE PRODUTO", FT_SEMI, 10, CYAN, tracking=2)
    text(c, 64, 66, "Documento de prototipagem · v2.0", FT_REG, 10, MUTED)

    # gota decorativa grande à direita
    c.saveState()
    p = c.beginPath()
    cx, cy, r = W - 150, 300, 90
    p.moveTo(cx, cy + 2.0 * r)
    p.curveTo(cx - 0.25 * r, cy + 1.25 * r, cx - r, cy + 0.65 * r, cx - r, cy)
    p.curveTo(cx - r, cy - 0.95 * r, cx + r, cy - 0.95 * r, cx + r, cy)
    p.curveTo(cx + r, cy + 0.65 * r, cx + 0.25 * r, cy + 1.25 * r, cx, cy + 2.0 * r)
    p.close(); c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(cx - r, cy - r, cx + r, cy + 2 * r, (GREEN, CYAN), (0, 1), extend=True)
    c.restoreState()
    pulse(c, cx, cy + 14, BG_DEEP, scale=2.4)

    footer(c, "USINA I.A. © 2026  ·  01 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 2 — IDENTIDADE VISUAL                                        #
# ================================================================== #
def page_identity(c):
    page_bg(c)
    section_title(c, 40, H - 70, "Identidade Visual", "Sistema de marca")

    # Logo principal + variações
    card(c, 40, H - 250, 360, 150, fill=BG_DEEP, border=LINE)
    logo(c, 70, H - 195, size=58, stacked=True)
    text(c, 70, H - 232, "Marca principal — gota (leite) + pulso (sensoriamento/risco)", FT_REG, 8.5, MUTED)

    card(c, 420, H - 250, 175, 150, fill=INK)
    logo(c, 445, H - 190, size=44, stacked=True, mono=BG_DEEP)
    text(c, 445, H - 232, "Versão sobre claro", FT_REG, 8, HexColor("#41566a"))

    card(c, 615, H - 250, 187, 150, fill=GREEN)
    logo(c, 640, H - 190, size=44, stacked=True, mono=BG_DEEP)
    text(c, 640, H - 232, "Versão monocromática", FT_REG, 8, HexColor("#0c3a2b"))

    # Paleta
    text(c, 40, H - 290, "PALETA DE CORES", FT_SEMI, 10, CYAN, tracking=1.5)
    swatches = [
        ("Azul Abissal", "#08161F", INK), ("Petróleo", "#0F2A38", INK),
        ("Ciano Sense", "#19D3E6", BG_DEEP), ("Verde Leite", "#34D399", BG_DEEP),
        ("Âmbar", "#F59E0B", BG_DEEP), ("Risco", "#EF4444", WHITE),
        ("Crítico", "#A78BFA", BG_DEEP), ("Tinta", "#EAF4F8", BG_DEEP),
    ]
    sx = 40; sw = 92; gap = 8
    for name, hexv, fg in swatches:
        card(c, sx, H - 380, sw, 78, fill=HexColor(hexv), radius=8,
             border=LINE if hexv in ("#08161F", "#0F2A38") else None)
        text(c, sx + 10, H - 345, name, FT_SEMI, 9, fg)
        text(c, sx + 10, H - 360, hexv.upper(), FT_REG, 8, fg)
        sx += sw + gap

    # Tipografia
    text(c, 40, H - 412, "TIPOGRAFIA", FT_SEMI, 10, CYAN, tracking=1.5)
    text(c, 40, H - 446, "Bahnschrift", FT_DISP, 30, INK)
    text(c, 40, H - 462, "Títulos & marca — display moderno e condensado", FT_REG, 8.5, MUTED)
    text(c, 420, H - 446, "Segoe UI", FT_SEMI, 26, INK)
    text(c, 420, H - 462, "Texto, números e interface — legível e neutra", FT_REG, 8.5, MUTED)
    text(c, 690, H - 440, "Aa Bb Cc", FT_REG, 22, MUTED)
    text(c, 690, H - 462, "0123456789 R$ %", FT_REG, 11, MUTED)

    # conceito
    card(c, 40, 56, W - 80, 30, fill=HexColor("#0c2c39"))
    text(c, 56, 66, "VOZ DA MARCA:", FT_SEMI, 9, CYAN)
    text(c, 145, 66, "Técnica na resolução, simples no manuseio. Do dado à decisão, antes da perda.",
         FT_REG, 10, INK)

    footer(c, "Identidade Visual  ·  02 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 3 — PROBLEMA → SOLUÇÃO                                       #
# ================================================================== #
def page_problem(c):
    page_bg(c)
    section_title(c, 40, H - 70, "O Desafio", "De reativo a preditivo")

    # coluna ANTES
    card(c, 40, 110, 360, H - 230, fill=BG_DEEP, border=RED)
    chip(c, 60, H - 150, "HOJE · GESTÃO REATIVA", WHITE, RED)
    dores = [
        ("Descoberta tardia", "O problema só aparece quando o caminhão volta com leite rejeitado."),
        ("Penalidade no pagamento", "CCS/CBT fora do padrão IN 77 viram desconto — depois da coleta."),
        ("Bônus de qualidade perdido", "Sem antecipação, não há tempo de ação preventiva."),
        ("Estresse térmico ignorado", "Queda de produção em 7–15 dias que ninguém viu chegar."),
    ]
    yy = H - 192
    for t, d in dores:
        c.setFillColor(RED); c.circle(72, yy + 4, 3, fill=1, stroke=0)
        text(c, 86, yy, t, FT_SEMI, 12, INK)
        text(c, 86, yy - 15, d, FT_REG, 9, MUTED)
        yy -= 56

    # seta
    text(c, 418, 296, "→", FT_BOLD, 34, CYAN, align="c")

    # coluna DEPOIS
    card(c, 442, 110, 360, H - 230, fill=BG_DEEP, border=GREEN)
    chip(c, 462, H - 150, "VIA LEITE SENSE · GESTÃO PREDITIVA", BG_DEEP, GREEN)
    ganhos = [
        ("Antecipação de 7–30 dias", "Score de risco por produtor, rota e laticínio."),
        ("Impacto traduzido em R$", "A dor técnica vira linguagem do gestor financeiro."),
        ("Ranking de ação preventiva", "Quem visitar primeiro para proteger receita e bônus."),
        ("Clima + qualidade + volume", "107 variáveis, IA preditiva e dados INMET integrados."),
    ]
    yy = H - 192
    for t, d in ganhos:
        c.setFillColor(GREEN); c.circle(474, yy + 4, 3, fill=1, stroke=0)
        text(c, 488, yy, t, FT_SEMI, 12, INK)
        text(c, 488, yy - 15, d, FT_REG, 9, MUTED)
        yy -= 56

    # faixa de números
    card(c, 40, 56, W - 80, 36, fill=HexColor("#0c2c39"))
    nums = [("R² 99,4%", "acurácia do modelo"), ("7 dim.", "de risco no score"),
            ("até 30 dias", "de antecipação"), ("50–60%", "menos descarte")]
    nx = 70
    for v, d in nums:
        text(c, nx, 74, v, FT_DISP, 14, CYAN)
        text(c, nx, 62, d, FT_REG, 8, MUTED)
        nx += 190

    footer(c, "Problema & Solução  ·  03 / 10")
    c.showPage()

# ------------------ widgets de mockup ------------------------------ #
def kpi(c, x, y, w, label, value, sub, accent):
    card(c, x, y, w, 74, fill=CARD)
    c.setFillColor(accent); c.roundRect(x, y, 4, 74, 2, fill=1, stroke=0)
    text(c, x + 16, y + 52, label, FT_REG, 8, MUTED)
    text(c, x + 16, y + 26, value, FT_DISP, 22, INK)
    text(c, x + 16, y + 12, sub, FT_REG, 7.5, accent)

def gauge(c, cx, cy, r, value, label):
    # fundo semicircular segmentado
    segs = [(0.0, 0.25, GREEN2), (0.25, 0.5, AMBER), (0.5, 0.75, RED), (0.75, 1.0, PURPLE)]
    c.setLineCap(0)
    for a, b, col in segs:
        start = 180 - a * 180
        extent = -(b - a) * 180
        c.setStrokeColor(col); c.setLineWidth(r * 0.34)
        c.arc(cx - r, cy - r, cx + r, cy + r, start, extent)
    # agulha
    import math
    ang = math.radians(180 - value / 100 * 180)
    nx = cx + (r - 4) * math.cos(ang); ny = cy + (r - 4) * math.sin(ang)
    c.setStrokeColor(INK); c.setLineWidth(2.5); c.setLineCap(1)
    c.line(cx, cy, nx, ny)
    c.setFillColor(INK); c.circle(cx, cy, 4, fill=1, stroke=0)
    text(c, cx, cy + 14, f"{value:.0f}", FT_DISP, 26, INK, align="c")
    text(c, cx, cy - 2, "/100", FT_REG, 8, MUTED, align="c")
    text(c, cx, cy - 22, label, FT_SEMI, 8.5, MUTED, align="c")

def radar4d(c, cx, cy, r, vals, labels):
    import math
    axes = len(vals)
    # grade
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for ring in (0.5, 1.0):
        pts = []
        for i in range(axes):
            a = math.radians(90 + i * 360 / axes)
            pts.append((cx + r * ring * math.cos(a), cy + r * ring * math.sin(a)))
        c.lines([(pts[i][0], pts[i][1], pts[(i + 1) % axes][0], pts[(i + 1) % axes][1]) for i in range(axes)])
    # polígono de dados
    p = c.beginPath()
    for i, v in enumerate(vals):
        a = math.radians(90 + i * 360 / axes)
        x = cx + r * v * math.cos(a); y = cy + r * v * math.sin(a)
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    p.close()
    c.setFillColor(Color(0.1, 0.83, 0.6, 0.28)); c.setStrokeColor(GREEN)
    c.setLineWidth(1.6); c.drawPath(p, fill=1, stroke=1)
    for i, lb in enumerate(labels):
        a = math.radians(90 + i * 360 / axes)
        x = cx + (r + 16) * math.cos(a); y = cy + (r + 12) * math.sin(a)
        text(c, x, y - 3, lb, FT_REG, 7.5, MUTED, align="c")

def browser_frame(c, x, y, w, h, title):
    card(c, x, y, w, h, fill=BG_DEEP, radius=12, border=LINE)
    c.setFillColor(CARD_HI); c.roundRect(x, y + h - 30, w, 30, 12, fill=1, stroke=0)
    c.setFillColor(CARD_HI); c.rect(x, y + h - 30, w, 18, fill=1, stroke=0)
    for i, col in enumerate((RED, AMBER, GREEN2)):
        c.setFillColor(col); c.circle(x + 16 + i * 14, y + h - 15, 4, fill=1, stroke=0)
    c.setFillColor(BG_PANEL); c.roundRect(x + 60, y + h - 23, w - 200, 16, 8, fill=1, stroke=0)
    text(c, x + 70, y + h - 19, title, FT_REG, 7.5, MUTED)

# ================================================================== #
# PÁGINA 4 — TELA RADAR DE RISCO                                      #
# ================================================================== #
def page_radar(c):
    page_bg(c)
    section_title(c, 40, H - 64, "Tela do produto", "Radar de Risco", accent=CYAN)
    text(c, W - 40, H - 64, "Página inicial pós-login", FT_REG, 9, MUTED, align="r")

    bx, by, bw, bh = 40, 62, W - 80, H - 176
    browser_frame(c, bx, by, bw, bh, "via-leite-sense.streamlit.app / Radar de Risco")

    ix, iw = bx + 18, bw - 36
    top = by + bh - 58
    logo(c, ix, top, size=30)
    chip(c, ix + iw - 150, top + 2, "Perfil: Demonstração", CYAN, HexColor("#0c2c39"))

    # KPIs
    ky = top - 96
    kw = (iw - 4 * 12) / 5
    kpis = [("Risco de queda", "23,6%", "em atenção", AMBER),
            ("Perda de qualidade", "5,9%", "controlado", GREEN),
            ("Perda de bônus", "5,9%", "controlado", GREEN),
            ("Situações críticas", "0", "nenhuma", GREEN),
            ("Impacto estimado", "R$ 92,6k", "perda/mês evit.", CYAN)]
    for i, (l, v, s, a) in enumerate(kpis):
        kpi(c, ix + i * (kw + 12), ky, kw, l, v, s, a)

    # gauge + ranking
    gy = by + 28
    card(c, ix, gy, 250, ky - gy - 14, fill=CARD)
    text(c, ix + 16, ky - 28, "SCORE MÉDIO DA CARTEIRA", FT_SEMI, 8.5, MUTED)
    gauge(c, ix + 125, gy + 78, 70, 27, "Atenção")

    rx = ix + 266
    rw = iw - 266
    card(c, rx, gy, rw, ky - gy - 14, fill=CARD)
    text(c, rx + 16, ky - 28, "RANKING DE PRIORIDADE DE AÇÃO PREVENTIVA", FT_SEMI, 8.5, MUTED)
    # cabeçalho
    cols = [("Produtor", rx + 16), ("Score", rx + rw - 250), ("Classe", rx + rw - 180), ("Impacto/mês", rx + rw - 90)]
    for t, cxp in cols:
        text(c, cxp, ky - 46, t, FT_SEMI, 8, MUTED)
    rows = [("Sítio Boa Vista", 71, "Crítico", PURPLE, "R$ 6.9k", 0.71),
            ("Faz. Santa Rita", 58, "Alto risco", RED, "R$ 3.6k", 0.58),
            ("Faz. Três Irmãos", 51, "Alto risco", RED, "R$ 4.3k", 0.51),
            ("Recanto do Vale", 47, "Atenção", AMBER, "R$ 1.7k", 0.47),
            ("Sítio Aurora", 45, "Atenção", AMBER, "R$ 1.2k", 0.45)]
    ry = ky - 66
    for nome, sc, cls, col, imp, frac in rows:
        text(c, rx + 16, ry, nome, FT_REG, 9, INK)
        # barra de score
        bx2 = rx + rw - 250
        c.setFillColor(LINE); c.roundRect(bx2, ry - 1, 56, 7, 3, fill=1, stroke=0)
        c.setFillColor(col); c.roundRect(bx2, ry - 1, 56 * frac, 7, 3, fill=1, stroke=0)
        text(c, bx2 + 62, ry, str(sc), FT_SEMI, 8.5, INK)
        chip(c, rx + rw - 180, ry - 4, cls, BG_DEEP, col, size=7.5, ph=14, padx=6)
        text(c, rx + rw - 90, ry, imp, FT_SEMI, 9, INK)
        ry -= 26

    footer(c, "Tela · Radar de Risco  ·  04 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 5 — TELA SCORE / FORNECEDORES 360                            #
# ================================================================== #
def page_score(c):
    page_bg(c)
    section_title(c, 40, H - 64, "Tela do produto", "Score Premium por Produtor", accent=GREEN)
    text(c, W - 40, H - 64, "Fornecedores 360", FT_REG, 9, MUTED, align="r")

    bx, by, bw, bh = 40, 62, W - 80, H - 176
    browser_frame(c, bx, by, bw, bh, "via-leite-sense.streamlit.app / Fornecedores 360")
    ix, iw = bx + 18, bw - 36
    top = by + bh - 58
    logo(c, ix, top, size=30)
    text(c, ix + iw, top + 6, "Sítio Boa Vista · Rota R03 · Polo Rio Verde", FT_REG, 9, MUTED, align="r")

    ch = top - (by + 28) - 16  # altura dos cards
    # gauge grande
    card(c, ix, by + 28, 228, ch, fill=CARD)
    text(c, ix + 16, top - 36, "SCORE VIA LEITE", FT_SEMI, 8.5, MUTED)
    gauge(c, ix + 114, by + 150, 92, 71, "Crítico — ação imediata")

    # radar 4D
    card(c, ix + 244, by + 28, 244, ch, fill=CARD)
    text(c, ix + 260, top - 36, "PERFIL 4D DE RISCO", FT_SEMI, 8.5, MUTED)
    radar4d(c, ix + 366, by + 150, 86, [0.4, 0.85, 0.55, 0.7],
            ["Volume", "Qualidade", "Logística", "Continuidade"])

    # recomendação IA
    rx = ix + 504
    card(c, rx, by + 28, iw - 504, ch, fill=BG_DEEP, border=GREEN)
    chip(c, rx + 16, top - 44, "RECOMENDAÇÃO IA", BG_DEEP, GREEN, size=8)
    recs = ["Priorizar visita técnica em 48h.",
            "CCS em tendência de alta — revisar",
            "rotina de pré e pós-dipping.",
            "Risco de perda de bônus no mês.",
            "Impacto evitável: R$ 6.9k/mês."]
    yy = top - 70
    for line in recs:
        text(c, rx + 16, yy, line, FT_REG, 9, INK); yy -= 17

    footer(c, "Tela · Score Premium  ·  05 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 6 — CONCEITO BOT WHATSAPP                                    #
# ================================================================== #
def page_whatsapp(c):
    page_bg(c)
    section_title(c, 40, H - 70, "Próxima fase", "Comunicação simples na ponta", accent=GREEN)
    text(c, 40, H - 114, "O produtor já vive no WhatsApp. O bot leva o alerta do Radar de Risco",
         FT_REG, 11, MUTED)
    text(c, 40, H - 132, "até ele em linguagem simples — e devolve os dados para a cooperativa.",
         FT_REG, 11, MUTED)

    # benefícios (coluna esquerda)
    bens = [
        ("Linguagem do produtor", "Alerta de risco simples, sem jargão técnico."),
        ("Lançamento por mensagem", "Litros e ocorrências reportados em segundos."),
        ("Ponte com a cooperativa", "Ranking aciona visita preventiva automática."),
        ("Zero fricção", "Sem app para instalar — adoção imediata na ponta."),
    ]
    yy = H - 170
    for t, d in bens:
        card(c, 40, yy - 44, 430, 56, fill=CARD)
        c.setFillColor(GREEN); c.roundRect(40, yy - 44, 4, 56, 2, fill=1, stroke=0)
        text(c, 60, yy - 8, t, FT_SEMI, 12, INK)
        text(c, 60, yy - 26, d, FT_REG, 9.5, MUTED)
        yy -= 68
    card(c, 40, 60, 430, 34, fill=HexColor("#0c2c39"))
    text(c, 56, 78, "ARQUITETURA:", FT_SEMI, 8.5, CYAN)
    text(c, 145, 78, "WhatsApp Cloud API → webhook → motor score_risco.py", FT_REG, 9, INK)

    # ----- mockup de celular -----
    px, py, pw, ph = 560, 70, 220, H - 150
    c.setFillColor(HexColor("#05222a")); c.roundRect(px - 6, py - 6, pw + 12, ph + 12, 30, fill=1, stroke=0)
    c.setFillColor(HexColor("#0B141A")); c.roundRect(px, py, pw, ph, 24, fill=1, stroke=0)
    # header
    c.saveState()
    pth = c.beginPath(); pth.roundRect(px, py + ph - 56, pw, 56, 24); c.clipPath(pth, stroke=0, fill=0)
    c.setFillColor(WA_GREEN); c.rect(px, py + ph - 70, pw, 70, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(WHITE); c.circle(px + 26, py + ph - 30, 13, fill=1, stroke=0)
    droplet(c, px + 26, py + ph - 35, 6, WA_GREEN);
    text(c, px + 46, py + ph - 26, "VIA LEITE · Assistente", FT_SEMI, 9.5, WHITE)
    text(c, px + 46, py + ph - 39, "online", FT_REG, 7.5, HexColor("#bfe9c6"))

    def bubble(cx_left, yb, lines, incoming, time):
        maxw = 0
        for ln in lines:
            maxw = max(maxw, c.stringWidth(ln, FT_REG, 8.3))
        bw = maxw + 22; bh = 14 * len(lines) + 16
        bxp = px + 12 if incoming else px + pw - 12 - bw
        col = WHITE if incoming else WA_BUBBLE
        c.setFillColor(col); c.roundRect(bxp, yb - bh, bw, bh, 8, fill=1, stroke=0)
        ty = yb - 14
        for ln in lines:
            text(c, bxp + 11, ty, ln, FT_REG, 8.3, HexColor("#0b2230")); ty -= 14
        text(c, bxp + bw - 28, yb - bh + 4, time, FT_REG, 6, HexColor("#5a7a86"))
        return bh

    yb = py + ph - 86
    chat = [
        (["Bom dia, Sr. João!", "Alerta VIA LEITE para sua", "entrega:"], True, "07:12"),
        (["Risco de CCS subir nos", "próximos 10 dias.", "Score: 58 — Alto risco."], True, "07:12"),
        (["Ação: reforçar pré e", "pós-dipping nesta semana."], True, "07:13"),
        (["Ok! Coletei 380 L hoje"], False, "07:40"),
        (["Registrado. Tudo certo!", "Volume dentro do previsto.", "Cooperativa avisada para", "visita preventiva."], True, "07:40"),
    ]
    for lines, inc, t in chat:
        bh = bubble(px, yb, lines, inc, t)
        yb -= bh + 8
    # campo de digitação
    c.setFillColor(HexColor("#1f2c34")); c.roundRect(px + 10, py + 10, pw - 20, 22, 11, fill=1, stroke=0)
    text(c, px + 22, py + 17, "Mensagem", FT_REG, 8, HexColor("#6b8290"))
    c.setFillColor(WA_GREEN); c.circle(px + pw - 22, py + 21, 11, fill=1, stroke=0)
    tp = c.beginPath(); tcx = px + pw - 22; tcy = py + 21
    tp.moveTo(tcx - 4, tcy - 4); tp.lineTo(tcx + 5, tcy); tp.lineTo(tcx - 4, tcy + 4); tp.close()
    c.setFillColor(WHITE); c.drawPath(tp, fill=1, stroke=0)

    footer(c, "Conceito · Bot WhatsApp  ·  06 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 7 — MERCADO TAM / SAM / SOM                                  #
# ================================================================== #
def page_market(c):
    page_bg(c)
    section_title(c, 40, H - 70, "Oportunidade", "Tamanho de mercado — TAM · SAM · SOM", accent=CYAN)

    cx = 300
    layers = [
        ("TAM", "R$ 108 mi/ano", "150 mil produtores formais · Brasil", 430, 330, 400, 322, NAVY_OR_BLUE()),
        ("SAM", "R$ 10,8 mi/ano", "15 mil produtores · Centro-Oeste", 300, 200, 318, 238, TEAL),
        ("SOM", "R$ 3,2 mi/ano", "4.500 produtores · Sul Goiano (3 anos)", 188, 84, 234, 162, GREEN),
    ]
    for name, val, desc, wt, wb, yT, yB, col in layers:
        p = c.beginPath()
        p.moveTo(cx - wt / 2, yT); p.lineTo(cx + wt / 2, yT)
        p.lineTo(cx + wb / 2, yB); p.lineTo(cx - wb / 2, yB); p.close()
        c.setFillColor(col); c.drawPath(p, fill=1, stroke=0)
        ymid = (yT + yB) / 2
        text(c, cx, ymid + 2, name, FT_DISP, 17, BG_DEEP, align="c")
        text(c, cx, ymid - 14, val, FT_SEMI, 11, BG_DEEP, align="c")
        # callout à direita
        lx = cx + wt / 2 + 24
        c.setStrokeColor(col); c.setLineWidth(1.2); c.line(cx + wb / 2 + 4, ymid, lx - 6, ymid)
        c.setFillColor(col); c.circle(lx - 6, ymid, 2.4, fill=1, stroke=0)
        text(c, lx, ymid + 3, val, FT_DISP, 14, INK)
        text(c, lx, ymid - 11, desc, FT_REG, 8.5, MUTED)

    # painel de contexto (direita inferior)
    cardx = 560
    text(c, cardx, 150, "CONTEXTO DE MERCADO (2023)", FT_SEMI, 9, CYAN, tracking=1)
    ctx = [("35,4 bi L", "produção Brasil · IBGE"),
           ("2,2 bi L", "produção Goiás · 6º maior"),
           ("~150 mil", "produtores formais · MilkPoint"),
           ("1,18 mi", "total c/ informais · Censo Agro")]
    cxx = cardx
    for i, (v, d) in enumerate(ctx):
        col = cardx + (i % 2) * 130
        row = 110 if i < 2 else 70
        card(c, col, row, 122, 34, fill=CARD)
        text(c, col + 10, row + 18, v, FT_DISP, 14, INK)
        text(c, col + 10, row + 7, d, FT_REG, 6.8, MUTED)

    text(c, 40, 50, "Fontes: IBGE/PPM 2023 · MilkPoint Ventures 2023 · IBGE Censo Agropecuário 2017. "
                    "Receita = produtores × R$ 60/mês × 12. Premissas ajustáveis ao vivo no app.",
         FT_REG, 7.5, MUTED)
    footer(c, "Mercado · TAM/SAM/SOM  ·  07 / 10")
    c.showPage()

# ================================================================== #
# PÁGINA 8 — ACESSE A DEMONSTRAÇÃO (QR)                               #
# ================================================================== #
def page_qr(c):
    grad_rect(c, 0, 0, W, H, BG_PANEL, BG_DEEP)
    c.saveState()
    pth = c.beginPath(); pth.rect(0, 0, W, H); c.clipPath(pth, stroke=0, fill=0)
    c.radialGradient(W * 0.30, H * 0.5, 320, (HexColor("#10455A"), BG_DEEP), (0, 1), extend=True)
    c.restoreState()

    # cartão branco com QR
    qx, qy, qs = 90, H / 2 - 150, 300
    c.setFillColor(WHITE); c.roundRect(qx, qy, qs, qs, 20, fill=1, stroke=0)
    if os.path.exists(QR_PNG):
        c.drawImage(QR_PNG, qx + 24, qy + 24, qs - 48, qs - 48, mask='auto')
    text(c, qx + qs / 2, qy - 24, "Aponte a câmera do celular", FT_SEMI, 11, INK, align="c")

    # texto à direita
    tx = qx + qs + 70
    chip(c, tx, H - 150, "DEMONSTRAÇÃO AO VIVO", CYAN, HexColor("#0c3340"))
    text(c, tx, H - 210, "Acesse o produto", FT_DISP, 40, INK)
    text(c, tx, H - 250, "funcionando agora", FT_DISP, 40, CYAN)

    text(c, tx, H - 286, DEMO_URL, FT_SEMI, 13, GREEN)

    # credenciais
    card(c, tx, H - 372, 360, 64, fill=BG_DEEP, border=LINE)
    text(c, tx + 18, H - 330, "LOGIN DE AVALIAÇÃO", FT_SEMI, 8.5, MUTED, tracking=1)
    text(c, tx + 18, H - 354, "usuário:  demo", FT_REG, 12, INK)
    text(c, tx + 190, H - 354, "senha:  demo2025", FT_REG, 12, INK)

    # o que explorar
    text(c, tx, H - 398, "O QUE EXPLORAR:", FT_SEMI, 9, CYAN, tracking=1)
    items = ["Radar de Risco — score e ranking de ação",
             "Score Premium por produtor (gauge + radar 4D)",
             "Demo Tour guiado de 5 min · slide de mercado",
             "Tamanho de mercado interativo (TAM/SAM/SOM)"]
    yy = H - 420
    for it in items:
        c.setFillColor(GREEN); c.circle(tx + 4, yy + 3, 2.5, fill=1, stroke=0)
        text(c, tx + 16, yy, it, FT_REG, 10, INK); yy -= 20

    logo(c, tx, 70, size=34)
    footer(c, "Demonstração · QR  ·  10 / 10")
    c.showPage()


def NAVY_OR_BLUE():
    return HexColor("#2563EB")


# ================================================================== #
# PÁGINA 8 — CENÁRIO COMPETITIVO                                      #
# ================================================================== #
def page_competitors(c):
    page_bg(c)
    section_title(c, 40, H - 64, "Cenário competitivo", "Quem já existe no mundo", accent=CYAN)
    text(c, 40, H - 110, "A categoria é real e está crescendo — isso valida o problema. O diferencial está no foco.",
         FT_REG, 11, MUTED)

    # faixa de validação de mercado
    vals = [("US$ 1,5 bi", ["mercado global de software", "leiteiro (2024)"]),
            ("~10% a.a.", ["crescimento projetado", "(CAGR até 2030)"]),
            ("Stellapps · Índia", ["2 bi L/ano · aporte", "Gates Foundation"]),
            ("Cowmed · Brasil", ["200 mil animais", "monitorados"])]
    vw = (W - 80 - 3 * 12) / 4
    vx = 40
    for v, d in vals:
        card(c, vx, H - 178, vw, 56, fill=CARD)
        text(c, vx + 14, H - 146, v, FT_DISP, 15, CYAN)
        for k, ln in enumerate(d):
            text(c, vx + 14, H - 160 - k * 11, ln, FT_REG, 7.5, MUTED)
        vx += vw + 12

    # tabela comparativa
    cols = [("Plataforma", 55), ("Origem", 220), ("Foco principal", 300), ("Abordagem", 545), ("Radar preditivo*", 695)]
    rows = [
        ("Cowmed", "Brasil", "Saúde e reprodução do animal", "Coleira IoT (hardware)", "Não", RED),
        ("DeLaval · Afimilk", "Global", "Gestão de ordenha e rebanho", "Software + equipamento", "Não", RED),
        ("Connecterra (Ida)", "Holanda", "IA de comportamento do animal", "Sensor + IA", "Não", RED),
        ("Stellapps", "Índia", "Procurement e cold chain da coop.", "Software + IoT de cadeia", "Parcial", AMBER),
        ("Ever.Ag", "EUA", "Risco de preço da commodity", "Software de mercado", "Parcial", AMBER),
        ("VIA LEITE SENSE", "Brasil / GO", "Risco produtivo, qualidade e renda da cadeia", "Software-first, baixa fricção", "Sim", GREEN),
    ]
    ty = H - 208
    for t, x in cols:
        text(c, x, ty, t.upper(), FT_SEMI, 8, MUTED, tracking=0.4)
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(55, ty - 9, W - 45, ty - 9)
    ry = ty - 26
    rh = 34
    for nome, orig, foco, abor, radar, col in rows:
        hl = nome == "VIA LEITE SENSE"
        if hl:
            c.setFillColor(HexColor("#0e3a44")); c.roundRect(48, ry - 9, W - 96, rh, 8, fill=1, stroke=0)
            c.setFillColor(CYAN); c.roundRect(48, ry - 9, 4, rh, 2, fill=1, stroke=0)
        text(c, cols[0][1], ry, nome, FT_SEMI, 10 if hl else 9.5, CYAN if hl else INK)
        text(c, cols[1][1], ry, orig, FT_REG, 8.5, MUTED)
        text(c, cols[2][1], ry, foco, FT_REG, 8.5, INK if hl else MUTED)
        text(c, cols[3][1], ry, abor, FT_REG, 8.5, INK if hl else MUTED)
        chip(c, cols[4][1], ry - 4, radar, BG_DEEP, col, size=8, ph=15, padx=8)
        ry -= rh
    text(c, 55, ry + 2,
         "* Radar preditivo = cruza clima (THI/INMET) + qualidade (CCS/CBT) + risco econômico, no nível da cadeia.",
         FT_REG, 7.5, MUTED)
    text(c, 55, ry - 12, "Fontes: Grand View / Market.us (mercado), sites das empresas. Posicionamento ilustrativo.",
         FT_REG, 7, HexColor("#5d7986"))
    footer(c, "Cenário competitivo  ·  08 / 10")
    c.showPage()


# ================================================================== #
# PÁGINA 9 — POSICIONAMENTO (MATRIZ 2x2)                              #
# ================================================================== #
def page_positioning(c):
    page_bg(c)
    section_title(c, 40, H - 64, "Posicionamento", "Onde nos posicionamos", accent=GREEN)

    qx, qy, qw, qh = 55, 78, 455, 400
    card(c, qx, qy, qw, qh, fill=BG_DEEP, border=LINE)
    axcx = qx + qw / 2; axcy = qy + qh / 2
    c.setStrokeColor(LINE); c.setLineWidth(1)
    c.line(qx + 20, axcy, qx + qw - 20, axcy)
    c.line(axcx, qy + 24, axcx, qy + qh - 18)
    text(c, qx + qw - 24, axcy - 12, "Cadeia (produtor→laticínio)", FT_SEMI, 8, MUTED, align="r")
    text(c, qx + 24, axcy - 12, "Animal", FT_SEMI, 8, MUTED)
    text(c, axcx + 8, qy + qh - 30, "Software preditivo · baixa fricção", FT_SEMI, 8, MUTED)
    text(c, axcx + 8, qy + 30, "Hardware · CapEx alto", FT_SEMI, 8, MUTED)

    def plot(fx, fy, label, col, big=False, dx=0, dy=0):
        px = qx + fx * qw; py = qy + fy * qh
        r = 9 if big else 5
        if big:
            c.setFillColor(Color(0.20, 0.83, 0.60, 0.25)); c.circle(px, py, r + 9, fill=1, stroke=0)
        c.setFillColor(col); c.circle(px, py, r, fill=1, stroke=0)
        if big:
            c.setStrokeColor(WHITE); c.setLineWidth(1.5); c.circle(px, py, r, fill=0, stroke=1)
        text(c, px + dx, py + r + 5 + dy, label, FT_SEMI if big else FT_REG,
             9.5 if big else 8, INK if big else MUTED, align="c")

    plot(0.17, 0.22, "Cowmed", MUTED)
    plot(0.32, 0.36, "DeLaval / Afimilk", MUTED)
    plot(0.28, 0.66, "Connecterra", MUTED)
    plot(0.68, 0.40, "Stellapps", MUTED)
    plot(0.74, 0.66, "Ever.Ag", MUTED)
    plot(0.81, 0.85, "VIA LEITE SENSE", GREEN, big=True)

    # painel direito
    rx = 540; rw = W - 40 - rx
    text(c, rx, H - 100, "O ESPAÇO EM BRANCO", FT_SEMI, 10, CYAN, tracking=1)
    para = ["Ninguém entrega, no nível da cadeia",
            "brasileira, um radar preditivo que cruza",
            "clima, qualidade e risco econômico —",
            "com baixa fricção e sem hardware caro."]
    yy = H - 124
    for ln in para:
        text(c, rx, yy, ln, FT_REG, 10, INK); yy -= 16
    yy -= 12
    diffs = [("Software-first", "Adesão sem CapEx de sensores."),
             ("Score 360°", "Clima + qualidade + economia num índice."),
             ("Calibrado ao Brasil", "Norma IN 77 e cadeia premium de Goiás.")]
    for t, d in diffs:
        c.setFillColor(GREEN); c.circle(rx + 4, yy + 3, 2.5, fill=1, stroke=0)
        text(c, rx + 16, yy, t, FT_SEMI, 10.5, INK)
        text(c, rx + 16, yy - 13, d, FT_REG, 8.5, MUTED)
        yy -= 40

    card(c, rx, 78, rw, 74, fill=HexColor("#0c2c39"))
    text(c, rx + 14, 130, "POR QUE AGORA", FT_SEMI, 9, AMBER, tracking=1)
    for k, ln in enumerate(["Clima extremo eleva o estresse térmico (THI).",
                            "Mercado premium exige qualidade (IN 77).",
                            "ESG e rastreabilidade viram exigência."]):
        text(c, rx + 14, 112 - k * 15, ln, FT_REG, 8.5, INK)

    footer(c, "Posicionamento  ·  09 / 10")
    c.showPage()


def gerar_qr():
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(DEMO_URL); qr.make(fit=True)
    img = qr.make_image(fill_color="#08161F", back_color="white")
    img.save(QR_PNG)


def main():
    gerar_qr()
    c = canvas.Canvas(OUT, pagesize=landscape(A4))
    c.setTitle("VIA LEITE SENSE — Protótipo")
    c.setAuthor("USINA I.A.")
    page_cover(c)
    page_identity(c)
    page_problem(c)
    page_radar(c)
    page_score(c)
    page_whatsapp(c)
    page_market(c)
    page_competitors(c)
    page_positioning(c)
    page_qr(c)
    c.save()
    print("PDF gerado:", OUT)


if __name__ == "__main__":
    main()