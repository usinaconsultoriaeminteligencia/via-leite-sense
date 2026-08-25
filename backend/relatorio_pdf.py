"""
relatorio_pdf.py — Gerador de Relatório Executivo PDF por Produtor
VIA LEITE SENSE · USINA I.A.

Dependência: fpdf2 >= 2.7
"""
from __future__ import annotations

import datetime
from io import BytesIO
from typing import Any

import pandas as pd
from fpdf import FPDF

# ── Paleta ────────────────────────────────────────────────────────────────────
_VERDE      = (2, 122, 72)        # #027A48
_LARANJA    = (181, 71, 8)        # #B54708
_VERMELHO   = (180, 35, 24)       # #B42318
_AZUL_ESCURO = (13, 27, 42)       # fundo header
_CINZA_TEXTO = (55, 65, 81)       # #374151
_CINZA_CLARO = (243, 244, 246)    # #F3F4F6
_BRANCO      = (255, 255, 255)
_PRETO       = (17, 24, 39)

_COR_CLASSE: dict[str, tuple[int, int, int]] = {
    "Alto":  _VERMELHO,
    "Medio": _LARANJA,
    "Baixo": _VERDE,
}

_BADGE_BG: dict[str, tuple[int, int, int]] = {
    "Alto":  (254, 243, 242),
    "Medio": (255, 250, 235),
    "Baixo": (236, 253, 245),
}


def _cor_score(score: float) -> tuple[int, int, int]:
    if score >= 75:
        return _VERMELHO
    if score >= 50:
        return _LARANJA
    return _VERDE


# ── Componentes de desenho ────────────────────────────────────────────────────

def _barra_progresso(
    pdf: FPDF,
    x: float, y: float,
    largura: float, altura: float,
    valor: float,          # 0–100
    cor: tuple[int, int, int],
    label: str,
    show_pct: bool = True,
) -> None:
    """Desenha label + trilho cinza + barra colorida."""
    # Label
    pdf.set_xy(x, y - 4)
    pdf.set_font("Helvetica", size=7)
    pdf.set_text_color(*_CINZA_TEXTO)
    pdf.cell(largura * 0.65, 4, label)
    if show_pct:
        pdf.set_xy(x + largura * 0.65, y - 4)
        pdf.set_font("Helvetica", "B", size=7)
        pdf.set_text_color(*cor)
        pdf.cell(largura * 0.35, 4, f"{valor:.0f} pts", align="R")

    # Trilho
    pdf.set_fill_color(*_CINZA_CLARO)
    pdf.rect(x, y, largura, altura, style="F")

    # Preenchimento
    fill_w = (valor / 100) * largura
    if fill_w > 0:
        pdf.set_fill_color(*cor)
        pdf.rect(x, y, fill_w, altura, style="F")


def _kpi_box(
    pdf: FPDF,
    x: float, y: float,
    largura: float, altura: float,
    valor: str,
    label: str,
    cor_borda: tuple[int, int, int],
) -> None:
    """Card KPI com borda lateral colorida."""
    # Fundo
    pdf.set_fill_color(*_CINZA_CLARO)
    pdf.rect(x, y, largura, altura, style="F")
    # Borda esquerda colorida
    pdf.set_fill_color(*cor_borda)
    pdf.rect(x, y, 2, altura, style="F")
    # Valor
    pdf.set_xy(x + 4, y + 1.5)
    pdf.set_font("Helvetica", "B", size=9)
    pdf.set_text_color(*_PRETO)
    pdf.cell(largura - 4, 5, valor)
    # Label
    pdf.set_xy(x + 4, y + 7)
    pdf.set_font("Helvetica", size=6)
    pdf.set_text_color(*_CINZA_TEXTO)
    pdf.cell(largura - 4, 3.5, label.upper())


def _secao_titulo(pdf: FPDF, x: float, y: float, texto: str) -> None:
    pdf.set_xy(x, y)
    pdf.set_font("Helvetica", "B", size=8)
    pdf.set_text_color(*_VERDE)
    pdf.cell(0, 5, texto.upper())
    pdf.set_draw_color(*_VERDE)
    pdf.line(x, y + 5, x + 180, y + 5)


# ── PDF principal ─────────────────────────────────────────────────────────────

def gerar_relatorio_produtor(
    det: Any,        # pd.Series ou dict-like com os scores
    hist_serie: pd.DataFrame | None = None,
    nome_laticinio: str = "",
) -> bytes:
    """
    Gera relatório executivo em PDF para um produtor.

    Parâmetros
    ----------
    det          : linha de scores (de calcular_scores_fornecedores)
    hist_serie   : DataFrame com colunas [data, litros_coletados, litros_previstos]
                   (últimos 30 dias); se None, omite o gráfico de histórico
    nome_laticinio : nome do laticínio para exibição

    Retorna
    -------
    bytes : conteúdo do PDF pronto para st.download_button
    """
    id_prod  = str(det.get("id_produtor", "—"))
    classe   = str(det.get("classe_risco", "Baixo"))
    score    = float(det.get("score_risco_fornecedor", 0))
    s_vol    = float(det.get("score_volume", 0))
    s_qual   = float(det.get("score_qualidade", 0))
    s_log    = float(det.get("score_logistica", 0))
    s_cont   = float(det.get("score_continuidade", 0))
    litros   = float(det.get("litros_coletados_media", 0))
    tend     = float(det.get("tendencia_volume_pct", 0))
    descarte = float(det.get("taxa_descarte_pct", 0))
    ccs      = float(det.get("ccs_media", 0))
    cbt      = float(det.get("cbt_media", 0))
    rec      = str(det.get("recomendacao", "—"))
    municipio = str(det.get("municipio", "—"))
    polo     = str(det.get("polo_climatico", "—"))
    sistema  = str(det.get("tipo_sistema", "—"))
    tecnif   = str(det.get("nivel_tecnificacao", "—"))
    porte    = str(det.get("porte_produtor", "—"))
    cor      = _COR_CLASSE.get(classe, _CINZA_TEXTO)
    data_hoje = datetime.date.today().strftime("%d/%m/%Y")

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(False)
    pdf.set_margins(15, 15, 15)

    # ── HEADER ──────────────────────────────────────────────────────────────
    pdf.set_fill_color(*_AZUL_ESCURO)
    pdf.rect(0, 0, 210, 28, style="F")

    pdf.set_xy(15, 6)
    pdf.set_font("Helvetica", "B", size=16)
    pdf.set_text_color(*_BRANCO)
    pdf.cell(100, 8, "VIA LEITE SENSE")

    pdf.set_xy(15, 15)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(134, 239, 172)   # verde claro
    pdf.cell(100, 5, "Relatorio Executivo de Produtor")

    pdf.set_xy(115, 6)
    pdf.set_font("Helvetica", "B", size=8)
    pdf.set_text_color(*_BRANCO)
    pdf.cell(80, 5, f"Produtor: {id_prod}", align="R")

    pdf.set_xy(115, 12)
    pdf.set_font("Helvetica", size=7)
    pdf.set_text_color(148, 163, 184)
    if nome_laticinio:
        pdf.cell(80, 5, f"Laticinio: {nome_laticinio}", align="R")

    pdf.set_xy(115, 18)
    pdf.set_font("Helvetica", size=7)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(80, 5, f"Gerado em: {data_hoje}", align="R")

    # ── SCORE PRINCIPAL ──────────────────────────────────────────────────────
    y_score = 34
    _secao_titulo(pdf, 15, y_score, "Score de Risco Geral")

    # Número grande
    pdf.set_xy(15, y_score + 8)
    pdf.set_font("Helvetica", "B", size=38)
    pdf.set_text_color(*cor)
    pdf.cell(40, 18, f"{score:.0f}")

    # "pts" pequeno
    pdf.set_xy(47, y_score + 20)
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(*cor)
    pdf.cell(12, 6, "pts")

    # Badge de classe
    badge_bg = _BADGE_BG.get(classe, _CINZA_CLARO)
    pdf.set_fill_color(*badge_bg)
    pdf.rect(15, y_score + 27, 25, 7, style="F")
    pdf.set_xy(15, y_score + 28)
    pdf.set_font("Helvetica", "B", size=8)
    pdf.set_text_color(*cor)
    pdf.cell(25, 5, classe.upper(), align="C")

    # Barra do score geral
    _barra_progresso(
        pdf, 65, y_score + 16, 130, 5,
        score, cor,
        "Score geral  (0 = sem risco · 100 = risco maximo)",
        show_pct=False,
    )
    pdf.set_xy(175, y_score + 11)
    pdf.set_font("Helvetica", "B", size=14)
    pdf.set_text_color(*cor)
    pdf.cell(20, 7, f"{score:.0f}", align="R")

    # ── DIMENSÕES ────────────────────────────────────────────────────────────
    y_dim = y_score + 40
    _secao_titulo(pdf, 15, y_dim, "Dimensoes de Risco")

    dims = [
        ("Volume",       s_vol,  _cor_score(s_vol)),
        ("Qualidade",    s_qual, _cor_score(s_qual)),
        ("Logistica",    s_log,  _cor_score(s_log)),
        ("Continuidade", s_cont, _cor_score(s_cont)),
    ]
    y_bar = y_dim + 8
    for label_dim, val_dim, cor_dim in dims:
        _barra_progresso(pdf, 15, y_bar, 180, 4, val_dim, cor_dim, label_dim)
        y_bar += 11

    # ── KPIs ─────────────────────────────────────────────────────────────────
    y_kpi = y_bar + 4
    _secao_titulo(pdf, 15, y_kpi, "Indicadores Operacionais")

    kpi_w = 34
    kpi_h = 14
    gap   = 3
    kpis = [
        (f"{litros:,.0f} L/dia",   "Producao media",     cor),
        (f"{tend:+.1f}%",          "Tendencia volume",   _cor_score(max(0, -tend + 50))),
        (f"{descarte:.2f}%",       "Taxa de descarte",   _cor_score(descarte * 10)),
        (f"{ccs:,.0f}",            "CCS media",          _cor_score(min(100, ccs / 10))),
        (f"{cbt:,.0f}",            "CBT media",          _cor_score(min(100, cbt / 3))),
    ]
    x_kpi = 15
    for val_k, label_k, cor_k in kpis:
        _kpi_box(pdf, x_kpi, y_kpi + 8, kpi_w, kpi_h, val_k, label_k, cor_k)
        x_kpi += kpi_w + gap

    # ── RECOMENDAÇÃO ─────────────────────────────────────────────────────────
    y_rec = y_kpi + kpi_h + 16
    _secao_titulo(pdf, 15, y_rec, "Recomendacao da Plataforma")

    # Caixa de recomendação
    pdf.set_fill_color(*_CINZA_CLARO)
    pdf.rect(15, y_rec + 7, 180, 18, style="F")
    pdf.set_fill_color(*cor)
    pdf.rect(15, y_rec + 7, 3, 18, style="F")

    pdf.set_xy(21, y_rec + 10)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(*_CINZA_TEXTO)
    pdf.multi_cell(174, 5, rec)

    # ── HISTÓRICO (sparkline texto) ───────────────────────────────────────────
    y_hist = y_rec + 32
    if hist_serie is not None and not hist_serie.empty and len(hist_serie) >= 3:
        _secao_titulo(pdf, 15, y_hist, "Historico de Volume (ultimos registros)")

        ultimos = hist_serie.sort_values("data").tail(10)
        col_w = 180 / len(ultimos)
        x_h = 15
        y_h_base = y_hist + 8

        max_vol = max(ultimos["litros_coletados"].max(), 1)
        bar_max_h = 18

        for _, row_h in ultimos.iterrows():
            vol = float(row_h.get("litros_coletados", 0))
            prev = float(row_h.get("litros_previstos", vol))
            h_vol  = max(1, (vol  / max_vol) * bar_max_h)
            h_prev = max(1, (prev / max_vol) * bar_max_h)

            # Barra prevista (cinza)
            pdf.set_fill_color(209, 213, 219)
            pdf.rect(x_h + 1, y_h_base + bar_max_h - h_prev, col_w * 0.4, h_prev, style="F")

            # Barra real (colorida)
            pdf.set_fill_color(*cor)
            pdf.rect(x_h + col_w * 0.45, y_h_base + bar_max_h - h_vol, col_w * 0.45, h_vol, style="F")

            # Data
            try:
                data_str = pd.Timestamp(row_h["data"]).strftime("%d/%m")
            except Exception:
                data_str = ""
            pdf.set_xy(x_h, y_h_base + bar_max_h + 1)
            pdf.set_font("Helvetica", size=5)
            pdf.set_text_color(*_CINZA_TEXTO)
            pdf.cell(col_w, 3, data_str, align="C")
            x_h += col_w

        # Legenda
        pdf.set_xy(15, y_h_base + bar_max_h + 6)
        pdf.set_fill_color(209, 213, 219)
        pdf.rect(15, y_h_base + bar_max_h + 7, 5, 3, style="F")
        pdf.set_xy(22, y_h_base + bar_max_h + 6)
        pdf.set_font("Helvetica", size=6)
        pdf.set_text_color(*_CINZA_TEXTO)
        pdf.cell(20, 4, "Previsto")

        pdf.set_fill_color(*cor)
        pdf.rect(45, y_h_base + bar_max_h + 7, 5, 3, style="F")
        pdf.set_xy(52, y_h_base + bar_max_h + 6)
        pdf.cell(20, 4, "Coletado")

    # ── DADOS CADASTRAIS ──────────────────────────────────────────────────────
    y_cad = 240
    _secao_titulo(pdf, 15, y_cad, "Dados Cadastrais")

    cad_items = [
        ("Municipio", municipio),
        ("Polo climatico", polo),
        ("Sistema", sistema),
        ("Tecnificacao", tecnif),
        ("Porte", porte),
    ]
    pdf.set_xy(15, y_cad + 7)
    for key_c, val_c in cad_items:
        pdf.set_font("Helvetica", "B", size=7)
        pdf.set_text_color(*_CINZA_TEXTO)
        pdf.cell(35, 4.5, f"{key_c}:")
        pdf.set_font("Helvetica", size=7)
        pdf.set_text_color(*_PRETO)
        pdf.cell(50, 4.5, val_c)
    pdf.ln(0)

    # ── FOOTER ───────────────────────────────────────────────────────────────
    pdf.set_fill_color(*_AZUL_ESCURO)
    pdf.rect(0, 284, 210, 14, style="F")
    pdf.set_xy(15, 287)
    pdf.set_font("Helvetica", size=6)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(
        100, 5,
        "VIA LEITE SENSE  |  Monitoramento Inteligente da Producao Leiteira  |  USINA I.A.",
    )
    pdf.set_xy(115, 287)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(80, 5, f"Gerado em {data_hoje}  |  Confidencial", align="R")

    # ── Saída ─────────────────────────────────────────────────────────────────
    buf = BytesIO()
    buf.write(pdf.output())
    return buf.getvalue()
