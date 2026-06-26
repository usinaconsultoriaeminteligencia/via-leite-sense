"""
VIA LEITE SENSE — Classificador de Perfil do Produtor (camada de regras)
=========================================================================
Classifica um produtor em um de três perfis estruturais, complementando
o Score de Risco (preditivo) com uma leitura estrutural (que TIPO de produtor).

Fundamentação:
- Faixas de CCS/CBT ancoradas na IN 76/77 (RIISPOA) — régua real de bonificação.
- Perfis e receitas de manejo derivados de Gonçalves (2025), via MilkPoint 12/06/2026:
  estudo real com 2.002 produtores, 16.362 análises (noroeste do RS).
- NÃO é clustering sobre dados sintéticos (isso seria artefato do gerador).
  É classificação por regra de negócio fundamentada — interpretável e defensável.

Eixo de inteligência:
- Score de Risco  -> "QUANDO agir" (dinâmico, temporal, preditivo)
- Perfil          -> "COMO agir"  (estrutural, lento, descritivo)
"""
from dataclasses import dataclass
from enum import Enum


# Limites da IN 77 (leite cru refrigerado, vigente): CCS <= 500 mil/mL, CBT <= 300 mil UFC/mL.
# Usados como régua regulatória — é o corte que define bonificação/penalização real.
IN77_CCS_LIMITE = 500.0   # mil células/mL
IN77_CBT_LIMITE = 300.0   # mil UFC/mL

# Níveis SEVEROS (alto risco) — um indicador sozinho neste patamar já caracteriza
# perfil Desafiador, mesmo com o outro dentro do padrão. CCS_SEVERO = 600 alinha-se
# ao 'ccs_alto' do score_risco.py (faixa de alto risco). CBT_SEVERO = 1,5x o IN 77.
CCS_SEVERO = 600.0        # mil células/mL
CBT_SEVERO = 450.0        # mil UFC/mL


class Perfil(Enum):
    CONSISTENTE = "Consistente"
    OSCILANTE = "Oscilante"
    DESAFIADOR = "Desafiador"


# Receitas de manejo por perfil — texto fundamentado na pesquisa (MilkPoint 06/2026).
RECEITAS = {
    Perfil.CONSISTENTE: {
        "leitura": "Alto desempenho e qualidade dentro do padrão. Manejo consistente.",
        "acao": "Manutenção e captura de bonificação. Foco em estabilidade e ganho de valor agregado.",
        "investimento": "Baixo — o básico já está dominado.",
        "cor": "#1E9E62",
    },
    Perfil.OSCILANTE: {
        "leitura": "Bons resultados intermitentes, com oscilações que limitam o desempenho.",
        "acao": "Padronização de rotina e consistência operacional. Pequenos ajustes geram ganho relevante.",
        "investimento": "Baixo a médio — problema de consistência, não estrutural.",
        "cor": "#E0A000",
    },
    Perfil.DESAFIADOR: {
        "leitura": "Maior variabilidade, CCS/CBT elevados, sólidos menores. Maiores desafios produtivos.",
        "acao": "Trabalhar o básico: rotina de ordenha, controle de mastite e ajustes nutricionais.",
        "investimento": "Médio — foco em fundamentos antes de tecnificação.",
        "cor": "#C9403F",
    },
}


@dataclass
class ResultadoPerfil:
    perfil: Perfil
    confianca: float          # 0..1 — quão claramente o produtor se encaixa
    sinais: list              # explicação interpretável (por que esse perfil)
    receita: dict

    def __repr__(self):
        return f"<{self.perfil.value} | confiança {self.confianca:.0%}>"


def classificar_perfil(ccs: float, cbt: float, solidos_totais: float = None,
                       coef_variacao_producao: float = None) -> ResultadoPerfil:
    """
    Classifica o produtor por perfil estrutural.

    Parâmetros:
        ccs   : CCS média (mil células/mL)
        cbt   : CBT/CPP média (mil UFC/mL)
        solidos_totais : opcional (g/100g) — reforça a leitura de qualidade
        coef_variacao_producao : opcional (0..1) — desvio/média da produção;
                                  é o que separa Consistente de Oscilante.

    Retorna ResultadoPerfil com perfil, confiança e sinais interpretáveis.
    """
    sinais = []

    # --- Eixo 1: qualidade vs. limite regulatório (IN 77) ---
    dentro_ccs = ccs <= IN77_CCS_LIMITE
    dentro_cbt = cbt <= IN77_CBT_LIMITE

    if dentro_ccs:
        sinais.append(f"CCS {ccs:.0f} dentro do limite IN 77 ({IN77_CCS_LIMITE:.0f})")
    else:
        margem = (ccs - IN77_CCS_LIMITE) / IN77_CCS_LIMITE
        sinais.append(f"CCS {ccs:.0f} acima do limite IN 77 (+{margem:.0%}) — risco de bônus")

    if dentro_cbt:
        sinais.append(f"CBT {cbt:.0f} dentro do limite IN 77 ({IN77_CBT_LIMITE:.0f})")
    else:
        sinais.append(f"CBT {cbt:.0f} acima do limite IN 77 — risco de penalização")

    # --- Eixo 2: variabilidade (separa Consistente de Oscilante) ---
    # CV alto = produção instável = oscilante, mesmo com qualidade ok.
    instavel = coef_variacao_producao is not None and coef_variacao_producao > 0.15
    if coef_variacao_producao is not None:
        if instavel:
            sinais.append(f"Produção instável (CV {coef_variacao_producao:.0%}) — oscilação de manejo")
        else:
            sinais.append(f"Produção estável (CV {coef_variacao_producao:.0%})")

    # --- Reforço opcional por sólidos ---
    if solidos_totais is not None:
        if solidos_totais >= 12.7:
            sinais.append(f"Sólidos {solidos_totais:.2f} — bom rendimento industrial")
        elif solidos_totais < 12.4:
            sinais.append(f"Sólidos {solidos_totais:.2f} — abaixo, reduz valor do derivado")

    # --- Regra de decisão (interpretável, fundamentada) ---
    qualidade_ok = dentro_ccs and dentro_cbt
    ccs_severo = ccs >= CCS_SEVERO
    cbt_severo = cbt >= CBT_SEVERO
    if ccs_severo:
        sinais.append(f"CCS {ccs:.0f} em nível severo (>= {CCS_SEVERO:.0f}) — alto risco")
    if cbt_severo:
        sinais.append(f"CBT {cbt:.0f} em nível severo (>= {CBT_SEVERO:.0f}) — alto risco")

    if qualidade_ok and not instavel:
        perfil = Perfil.CONSISTENTE
        confianca = 0.9 if coef_variacao_producao is not None else 0.7
    elif qualidade_ok and instavel:
        perfil = Perfil.OSCILANTE
        confianca = 0.85
    elif (not dentro_ccs and not dentro_cbt) or ccs_severo or cbt_severo:
        # Ambos os indicadores fora, OU um deles em nível severo (alto risco real).
        perfil = Perfil.DESAFIADOR
        confianca = 0.9 if (not dentro_ccs and not dentro_cbt) else 0.8
    else:
        # Apenas um indicador levemente fora do limite -> oscilação de qualidade.
        perfil = Perfil.OSCILANTE
        confianca = 0.7

    return ResultadoPerfil(
        perfil=perfil,
        confianca=confianca,
        sinais=sinais,
        receita=RECEITAS[perfil],
    )


def recomendacao_combinada(score_risco: int, resultado_perfil: ResultadoPerfil) -> str:
    """
    Combina o Score de Risco (QUANDO agir) com o Perfil (COMO agir).
    Esta é a entrega de valor: recomendação cirúrgica em vez de genérica.
    """
    urgencia = ("AÇÃO IMEDIATA" if score_risco >= 71
                else "ATENÇÃO" if score_risco >= 41
                else "ESTÁVEL")
    p = resultado_perfil
    return (
        f"[{urgencia} · Score {score_risco}] Perfil {p.perfil.value}. "
        f"{p.receita['acao']} (Investimento esperado: {p.receita['investimento']})"
    )
