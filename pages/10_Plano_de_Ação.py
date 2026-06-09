"""
pages/10_Plano_de_Acao.py — Plano de Ação por Produtor

Crie, acompanhe e encerre planos de melhoria com:
  - Prompts inteligentes por dimensão + perfil de risco do produtor
  - Caminhos guiados: o que fazer, como evidenciar, prazo padrão
  - Seleção de prompt preenche o formulário automaticamente
  - Acompanhamento com filtros, edição e painel de KPIs
"""
from __future__ import annotations

import uuid
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from auth import requer_autenticacao, renderizar_sidebar_usuario
from dashboard_common import aplicar_layout_plotly, artefatos_dir, carregar_dados, data_dir
from fornecedor_inteligencia import calcular_scores_fornecedores
from gestor_store import conectar, garantir_pasta, init_db

requer_autenticacao()
renderizar_sidebar_usuario()

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.vl-pa-header {
    background: linear-gradient(90deg,rgba(74,144,226,0.2),rgba(4,120,87,0.1));
    border-left: 4px solid #4A90E2;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.2rem;
}
.vl-pa-title { color:#F0FFF4; font-size:1.2rem; font-weight:700; margin:0; }
.vl-pa-sub   { color:#93C5FD; font-size:0.85rem; margin:0.2rem 0 0; }

/* Prompt cards */
.vl-prompt-card {
    background: rgba(74,144,226,0.08);
    border: 1px solid rgba(74,144,226,0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.65rem;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
}
.vl-prompt-card:hover { border-color: #4ADE80; background: rgba(74,222,128,0.08); }
.vl-prompt-card.selected { border-color: #4ADE80; background: rgba(74,222,128,0.12); }
.vl-prompt-urgencia { font-size:0.75rem; font-weight:700; border-radius:8px;
                      padding:0.15rem 0.55rem; margin-bottom:0.4rem; display:inline-block; }
.vl-p-alta   { background:#7f1d1d; color:#fca5a5; }
.vl-p-media  { background:#78350f; color:#fcd34d; }
.vl-p-baixa  { background:#065f46; color:#6ee7b7; }
.vl-prompt-titulo { color:#F0FFF4; font-weight:700; font-size:0.95rem; margin:0.2rem 0; }
.vl-prompt-desc   { color:#94A3B8; font-size:0.83rem; line-height:1.5; margin:0.2rem 0; }
.vl-prompt-path   { color:#60A5FA; font-size:0.78rem; margin-top:0.4rem; }
.vl-prompt-meta   { color:#475569; font-size:0.75rem; margin-top:0.25rem; }

/* Status badges */
.vl-status-aberto    { background:#1e3a5f; color:#93C5FD;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-em_curso  { background:#78350f; color:#FCD34D;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-concluido { background:#065f46; color:#6EE7B7;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-cancelado { background:#1f2937; color:#9CA3AF;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }

/* Guia lateral */
.vl-guia-item {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #4A90E2;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    border-radius: 0 8px 8px 0;
}
.vl-guia-step { color:#93C5FD; font-size:0.78rem; font-weight:600; }
.vl-guia-text { color:#CBD5E1; font-size:0.82rem; margin-top:0.15rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# BANCO DE PROMPTS — biblioteca de ações por dimensão e urgência
# ---------------------------------------------------------------------------
# Estrutura de cada prompt:
#   titulo, urgencia (Alta/Media/Baixa), descricao, caminho (passos),
#   evidencia_sugerida, prazo_dias, dimensao, tag (para filtragem)
# ---------------------------------------------------------------------------
PROMPTS_BIBLIOTECA: list[dict] = [

    # ── QUALIDADE ────────────────────────────────────────────────────────
    {
        "dimensao": "Qualidade", "urgencia": "Alta",
        "titulo": "CCS elevada — protocolo de qualidade urgente",
        "descricao": (
            "CCS acima do limite premium (400 mil céls/mL). "
            "Risco imediato de desqualificação da cadeia premium e rejeição no laticínio."
        ),
        "caminho": [
            "1. Visita técnica em até 48h para avaliação de higiene de ordenha",
            "2. Coletar amostra de CMT (California Mastitis Test) em todas as vacas",
            "3. Isolar animais com mastite clínica e iniciar tratamento veterinário",
            "4. Revisar protocolo de limpeza de teteiras e tanque de resfriamento",
            "5. Repetir análise laboratorial em 15 dias para verificar evolução",
        ],
        "evidencia_sugerida": "Resultado CMT + laudo CCS laboratorial + relatório de visita técnica",
        "prazo_dias": 7,
        "tag": "ccs",
    },
    {
        "dimensao": "Qualidade", "urgencia": "Alta",
        "titulo": "CBT elevada — higienização e controle bacteriano",
        "descricao": (
            "Contagem Bacteriana Total acima de 100 mil UFC/mL. "
            "Indica falha em higienização, refrigeração inadequada ou problema na água de limpeza."
        ),
        "caminho": [
            "1. Verificar temperatura do tanque de resfriamento (deve estar ≤ 4°C em 2h)",
            "2. Coletar amostra de água de limpeza para análise microbiológica",
            "3. Revisar concentração e tempo de contato dos produtos de limpeza",
            "4. Inspecionar borrachas, gaxetas e tubulações da ordenhadeira",
            "5. Confirmar CBT abaixo de 100 na próxima análise periódica",
        ],
        "evidencia_sugerida": "Relatório de temperatura do tanque + laudo CBT + checklist de higienização",
        "prazo_dias": 7,
        "tag": "cbt",
    },
    {
        "dimensao": "Qualidade", "urgencia": "Alta",
        "titulo": "Ocorrência de antibiótico — protocolo de descarte e rastreio",
        "descricao": (
            "Leite com resíduo de antibiótico detectado ou animal em tratamento não identificado. "
            "Risco de contaminação do lote e descarte total no recebimento."
        ),
        "caminho": [
            "1. Identificar e isolar imediatamente o(s) animal(is) em tratamento",
            "2. Implementar controle visual (tinta ou fita) para vacas sob antibiótico",
            "3. Descartar integralmente o leite do animal até término do período de carência",
            "4. Registrar ocorrência no mapa de saúde do rebanho",
            "5. Treinar ordenhador para identificação e comunicação de animais tratados",
        ],
        "evidencia_sugerida": "Foto da identificação dos animais + receita veterinária + registro de descarte",
        "prazo_dias": 1,
        "tag": "antibiotico",
    },
    {
        "dimensao": "Qualidade", "urgencia": "Media",
        "titulo": "Temperatura do tanque — ajuste de resfriamento",
        "descricao": (
            "Temperatura habitual do tanque acima de 5°C. "
            "Leite premium exige resfriamento a ≤ 4°C nas 2h após ordenha."
        ),
        "caminho": [
            "1. Verificar funcionamento do compressor e nível de gás refrigerante",
            "2. Checar capacidade do tanque x volume de leite produzido",
            "3. Avaliar ventilação da sala de ordenha e tanque",
            "4. Programar manutenção preventiva do equipamento de frio",
            "5. Monitorar temperatura diariamente por 7 dias e registrar",
        ],
        "evidencia_sugerida": "Registro diário de temperatura + laudo de manutenção do tanque",
        "prazo_dias": 15,
        "tag": "temperatura",
    },
    {
        "dimensao": "Qualidade", "urgencia": "Media",
        "titulo": "Taxa de descarte elevada — investigação de perdas",
        "descricao": (
            "Descarte acima de 3% indica problema recorrente de qualidade ou operacional. "
            "Impacto direto na rentabilidade e no score do fornecedor."
        ),
        "caminho": [
            "1. Mapear as causas de descarte dos últimos 30 dias (mastite, antibiótico, acidez, temperatura)",
            "2. Calcular custo financeiro do descarte por litro e por período",
            "3. Definir meta de redução: ≤ 1% em 30 dias",
            "4. Implementar check diário antes de cada coleta",
            "5. Revisar resultado com o produtor ao final do período",
        ],
        "evidencia_sugerida": "Planilha de causas de descarte + mapa de coleta + relatório de melhoria",
        "prazo_dias": 30,
        "tag": "descarte",
    },

    # ── VOLUME ───────────────────────────────────────────────────────────
    {
        "dimensao": "Volume", "urgencia": "Alta",
        "titulo": "Queda de volume — diagnóstico e recuperação urgente",
        "descricao": (
            "Tendência de queda superior a 10% na captação. "
            "Risco de perda de fornecimento e impacto no planejamento do laticínio."
        ),
        "caminho": [
            "1. Entrevista com o produtor para identificar causas (saúde do rebanho, nutrição, vendas de vacas)",
            "2. Avaliar escore corporal e condição nutricional das vacas em lactação",
            "3. Revisar fornecimento e qualidade do volumoso (silagem, pasto)",
            "4. Verificar se houve venda de animais ou redução do rebanho",
            "5. Definir plano nutricional com veterinário/zootecnista em 7 dias",
        ],
        "evidencia_sugerida": "Histórico de volume das últimas 4 semanas + relatório de visita + plano nutricional",
        "prazo_dias": 7,
        "tag": "queda_volume",
    },
    {
        "dimensao": "Volume", "urgencia": "Media",
        "titulo": "Baixa produtividade por vaca — revisão de manejo",
        "descricao": (
            "Produção abaixo de 12 L/vaca/dia indica oportunidade de melhoria em genética, "
            "nutrição ou manejo reprodutivo."
        ),
        "caminho": [
            "1. Calcular produção média real por vaca em lactação",
            "2. Avaliar qualidade e quantidade do concentrado fornecido",
            "3. Verificar intervalo entre partos e eficiência reprodutiva",
            "4. Propor ajuste de suplementação para vacas de alta produção",
            "5. Estimar potencial de aumento e definir meta para 60 dias",
        ],
        "evidencia_sugerida": "Ficha zootécnica + planilha de produção por vaca + protocolo nutricional",
        "prazo_dias": 60,
        "tag": "produtividade",
    },
    {
        "dimensao": "Volume", "urgencia": "Baixa",
        "titulo": "Expansão de rebanho — estudo de viabilidade",
        "descricao": (
            "Produtor com capacidade de tanque subutilizada e potencial de crescimento. "
            "Oportunidade de aumentar captação com baixo risco logístico."
        ),
        "caminho": [
            "1. Levantar capacidade de suporte da pastagem e instalações",
            "2. Calcular investimento necessário para novas vacas (custo x payback)",
            "3. Avaliar disponibilidade de crédito rural (PRONAF/BNDES)",
            "4. Proposta formal ao produtor com projeção de receita adicional",
            "5. Acompanhar implantação em 90 dias",
        ],
        "evidencia_sugerida": "Estudo de viabilidade + proposta comercial + contrato atualizado",
        "prazo_dias": 90,
        "tag": "expansao",
    },

    # ── LOGÍSTICA ────────────────────────────────────────────────────────
    {
        "dimensao": "Logística", "urgencia": "Alta",
        "titulo": "Falha recorrente de coleta — renegociação de rota",
        "descricao": (
            "Taxa de falha de coleta acima de 2% compromete a segurança do abastecimento "
            "e gera custos extras de logística reversa."
        ),
        "caminho": [
            "1. Mapear os dias e causas das falhas nas últimas 4 semanas",
            "2. Identificar se o problema é acesso viário, janela de coleta ou volume insuficiente",
            "3. Negociar ajuste na janela de coleta ou rota alternativa para dias de chuva",
            "4. Avaliar custo-benefício de coleta a cada 2 dias x diária",
            "5. Comunicar mudança ao motorista e ao produtor com antecedência",
        ],
        "evidencia_sugerida": "Mapa de falhas + relatório de rota + novo cronograma de coleta",
        "prazo_dias": 15,
        "tag": "falha_coleta",
    },
    {
        "dimensao": "Logística", "urgencia": "Media",
        "titulo": "Estrada não pavimentada — plano de acesso em período chuvoso",
        "descricao": (
            "Alto percentual de estrada sem pavimento aumenta risco de falha na coleta "
            "e deterioração do leite em dias de chuva intensa."
        ),
        "caminho": [
            "1. Identificar os trechos críticos no período de chuva (dez–mar)",
            "2. Articular com produtor para manutenção básica da estrada (cascalho, drenagem)",
            "3. Mapear rota alternativa e validar com o motorista",
            "4. Definir protocolo: coleta antecipada em dias de previsão de chuva forte",
            "5. Incluir alerta climático automático no roteiro logístico",
        ],
        "evidencia_sugerida": "Foto da estrada + mapa de rota alternativa + protocolo de coleta em período de chuva",
        "prazo_dias": 30,
        "tag": "estrada",
    },
    {
        "dimensao": "Logística", "urgencia": "Baixa",
        "titulo": "Otimização de rota — redução de custo logístico",
        "descricao": (
            "Custo por litro transportado acima da média da rota. "
            "Oportunidade de agrupamento com produtores próximos."
        ),
        "caminho": [
            "1. Calcular custo atual por litro transportado (combustível + hora + manutenção)",
            "2. Identificar produtores na mesma microrregião para agrupamento",
            "3. Simular nova rota consolidada e estimar economia",
            "4. Negociar ajuste de janela de coleta com os produtores envolvidos",
            "5. Implantar nova rota e monitorar por 30 dias",
        ],
        "evidencia_sugerida": "Planilha de custo por litro + mapa de nova rota + relatório de economia",
        "prazo_dias": 45,
        "tag": "custo_logistico",
    },

    # ── CONTINUIDADE ─────────────────────────────────────────────────────
    {
        "dimensao": "Continuidade", "urgencia": "Alta",
        "titulo": "Risco de saída — ação comercial imediata",
        "descricao": (
            "Sinal de insatisfação ou proposta de concorrente detectado. "
            "Risco real de perda do fornecedor nos próximos 30 dias."
        ),
        "caminho": [
            "1. Visita presencial do gerente comercial em até 72h",
            "2. Ouvir as motivações do produtor sem pressão ou promessas imediatas",
            "3. Levantar o diferencial da proposta concorrente (preço, prazo, serviços)",
            "4. Apresentar contraproposta com base nos dados de relacionamento e histórico",
            "5. Formalizar acordo em contrato atualizado com cláusulas de fidelidade",
        ],
        "evidencia_sugerida": "Ata de visita + proposta comercial formalizada + contrato assinado",
        "prazo_dias": 7,
        "tag": "churn",
    },
    {
        "dimensao": "Continuidade", "urgencia": "Media",
        "titulo": "Revisão de precificação — alinhamento de margem",
        "descricao": (
            "Margem estimada por litro abaixo da média da bacia. "
            "Produtor pode estar comparando propostas de concorrentes."
        ),
        "caminho": [
            "1. Calcular preço médio de mercado para o polo climático",
            "2. Avaliar histórico de pagamento, bonificações e descontos aplicados",
            "3. Propor ajuste de precificação baseado em qualidade (CCS + CBT)",
            "4. Apresentar ao produtor o comparativo de rentabilidade com premiação premium",
            "5. Documentar novo acordo em aditivo contratual",
        ],
        "evidencia_sugerida": "Comparativo de preços + simulação de bonificação + aditivo contratual",
        "prazo_dias": 20,
        "tag": "margem",
    },
    {
        "dimensao": "Continuidade", "urgencia": "Baixa",
        "titulo": "Programa de fidelização — premiação por qualidade",
        "descricao": (
            "Produtor com bom histórico e potencial de expansão. "
            "Oportunidade de fidelizar com programa de bonificação por CCS/CBT."
        ),
        "caminho": [
            "1. Mapear os últimos 6 meses de qualidade e volume do produtor",
            "2. Calcular bonificação acumulada por atingimento de metas",
            "3. Apresentar certificado de fornecedor premium e plaqueta de identificação",
            "4. Incluir produtor no programa de visitas técnicas gratuitas",
            "5. Renovar contrato com cláusula de fidelidade e benefícios exclusivos",
        ],
        "evidencia_sugerida": "Histórico de qualidade + certificado emitido + contrato renovado",
        "prazo_dias": 30,
        "tag": "fidelizacao",
    },

    # ── OPERACIONAL ──────────────────────────────────────────────────────
    {
        "dimensao": "Operacional", "urgencia": "Media",
        "titulo": "Capacitação do ordenhador — boas práticas de ordenha",
        "descricao": (
            "Falhas operacionais recorrentes indicam necessidade de treinamento técnico. "
            "O ordenhador é o principal fator de controle de CCS e CBT."
        ),
        "caminho": [
            "1. Agendar treinamento presencial de boas práticas de ordenha (4h)",
            "2. Aplicar checklist de higiene antes e depois de cada ordenha",
            "3. Demonstrar técnica correta de pré e pós-dipping",
            "4. Treinar identificação visual de mastite subclínica",
            "5. Aplicar avaliação prática 30 dias após o treinamento",
        ],
        "evidencia_sugerida": "Lista de presença + checklist preenchido + resultado de CCS pós-treinamento",
        "prazo_dias": 20,
        "tag": "treinamento",
    },
    {
        "dimensao": "Operacional", "urgencia": "Baixa",
        "titulo": "Manutenção preventiva da ordenhadeira",
        "descricao": (
            "Equipamento sem manutenção registrada nos últimos 6 meses. "
            "Desgaste de borrachas e variação de vácuo impactam diretamente a saúde do úbere."
        ),
        "caminho": [
            "1. Agendar visita de técnico credenciado para inspeção completa",
            "2. Substituir borrachas de teteiras (vida útil: 2.500 ordenhas ou 6 meses)",
            "3. Calibrar nível de vácuo e pulsação conforme manual do fabricante",
            "4. Limpar e desincrustar tubulações com produto enzimático",
            "5. Emitir laudo de manutenção e programar próxima revisão",
        ],
        "evidencia_sugerida": "Laudo técnico + nota fiscal de peças substituídas + foto do equipamento",
        "prazo_dias": 30,
        "tag": "manutencao",
    },

    # ── RELACIONAMENTO ───────────────────────────────────────────────────
    {
        "dimensao": "Relacionamento", "urgencia": "Media",
        "titulo": "Visita de acompanhamento — fortalecimento do vínculo",
        "descricao": (
            "Produtor sem visita técnica há mais de 60 dias. "
            "Visitas regulares aumentam a retenção e antecipam problemas."
        ),
        "caminho": [
            "1. Agendar visita técnica-comercial em data conveniente para o produtor",
            "2. Levar relatório de desempenho do mês: volume, qualidade e ranking",
            "3. Ouvir demandas e dificuldades sem agenda de vendas",
            "4. Apresentar benefícios disponíveis (assistência técnica, crédito, insumos)",
            "5. Registrar principais pontos e próxima data de retorno",
        ],
        "evidencia_sugerida": "Ata de visita + foto na propriedade + próxima data agendada",
        "prazo_dias": 15,
        "tag": "visita",
    },
    {
        "dimensao": "Relacionamento", "urgencia": "Baixa",
        "titulo": "Comunicação de resultados — relatório mensal ao produtor",
        "descricao": (
            "Produtor não recebe feedback regular sobre sua qualidade e ranking. "
            "Transparência aumenta engajamento e confiança na parceria."
        ),
        "caminho": [
            "1. Configurar envio mensal do boletim de desempenho por WhatsApp ou e-mail",
            "2. Incluir: volume coletado, CCS, CBT, ranking e bonificação do mês",
            "3. Destacar conquistas e oportunidades de melhoria de forma positiva",
            "4. Abrir canal de resposta para dúvidas e sugestões",
            "5. Avaliar satisfação com NPS trimestral (pergunta única por WhatsApp)",
        ],
        "evidencia_sugerida": "Template do boletim + confirmação de envio + respostas de NPS",
        "prazo_dias": 30,
        "tag": "comunicacao",
    },
]


def _prompts_para(dimensao: str, classe_risco: str = "") -> list[dict]:
    """Retorna prompts filtrados por dimensão, priorizando urgência conforme risco."""
    base = [p for p in PROMPTS_BIBLIOTECA if p["dimensao"] == dimensao]
    if classe_risco == "Alto":
        base.sort(key=lambda x: {"Alta": 0, "Media": 1, "Baixa": 2}[x["urgencia"]])
    return base


# ---------------------------------------------------------------------------
# Persistência DuckDB
# ---------------------------------------------------------------------------
PLANOS_COLS = [
    "id_plano", "id_produtor", "nome_fazenda", "polo",
    "dimensao", "descricao_acao", "responsavel",
    "prazo", "status", "evidencia", "criado_em", "atualizado_em",
]
STATUS_OPTS  = ["Aberto", "Em curso", "Concluído", "Cancelado"]
DIMENSOES    = ["Qualidade", "Volume", "Logística", "Continuidade", "Operacional", "Relacionamento"]


def _init_planos() -> None:
    garantir_pasta()
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS planos_acao (
                id_plano       VARCHAR PRIMARY KEY,
                id_produtor    VARCHAR,
                nome_fazenda   VARCHAR,
                polo           VARCHAR,
                dimensao       VARCHAR,
                descricao_acao VARCHAR,
                responsavel    VARCHAR,
                prazo          DATE,
                status         VARCHAR DEFAULT 'Aberto',
                evidencia      VARCHAR,
                criado_em      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def _salvar_plano(dados: dict) -> str:
    _init_planos()
    if not dados.get("id_plano"):
        dados["id_plano"] = str(uuid.uuid4())[:8].upper()
    with conectar() as con:
        existe = con.execute(
            "SELECT id_plano FROM planos_acao WHERE id_plano = ?", [dados["id_plano"]]
        ).fetchone()
        if existe:
            con.execute("""
                UPDATE planos_acao SET
                    dimensao=?, descricao_acao=?, responsavel=?,
                    prazo=?, status=?, evidencia=?,
                    atualizado_em=CURRENT_TIMESTAMP
                WHERE id_plano=?
            """, [dados["dimensao"], dados["descricao_acao"], dados["responsavel"],
                  dados["prazo"], dados["status"], dados.get("evidencia",""),
                  dados["id_plano"]])
        else:
            con.execute("""
                INSERT INTO planos_acao
                (id_plano,id_produtor,nome_fazenda,polo,dimensao,
                 descricao_acao,responsavel,prazo,status,evidencia)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, [dados["id_plano"], dados.get("id_produtor",""),
                  dados.get("nome_fazenda",""), dados.get("polo",""),
                  dados["dimensao"], dados["descricao_acao"],
                  dados["responsavel"], dados["prazo"],
                  dados.get("status","Aberto"), dados.get("evidencia","")])
    return dados["id_plano"]


def _carregar_planos(id_produtor: str | None = None) -> pd.DataFrame:
    _init_planos()
    with conectar(read_only=True) as con:
        q = "SELECT * FROM planos_acao"
        p: list = []
        if id_produtor:
            q += " WHERE id_produtor = ?"
            p.append(str(id_produtor))
        q += " ORDER BY criado_em DESC"
        try:
            df = con.execute(q, p).df()
        except Exception:
            df = pd.DataFrame(columns=PLANOS_COLS)
    return df


def _excluir_plano(id_plano: str) -> None:
    with conectar() as con:
        con.execute("DELETE FROM planos_acao WHERE id_plano = ?", [id_plano])


# ---------------------------------------------------------------------------
# Dados do modelo
# ---------------------------------------------------------------------------
init_db(data_dir())
try:
    pred, _, _, prod, dim_prod, _, _ = carregar_dados(artefatos_dir(), data_dir())
    scores_df = calcular_scores_fornecedores(prod, dim_prod, pred)
    tem_dados = not scores_df.empty
except Exception:
    scores_df = pd.DataFrame()
    tem_dados = False

# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
st.markdown("## 📋 Plano de Ação por Produtor")
st.caption("Crie e acompanhe planos de melhoria com orientação técnica passo a passo.")

tab_novo, tab_acompanhar, tab_painel = st.tabs(["➕ Novo Plano", "📌 Acompanhar", "📊 Painel"])

# ============================================================
# ABA NOVO PLANO
# ============================================================
with tab_novo:
    # Session state para formulário pré-preenchido por prompt
    if "pa_dimensao"  not in st.session_state: st.session_state["pa_dimensao"]  = "Qualidade"
    if "pa_descricao" not in st.session_state: st.session_state["pa_descricao"] = ""
    if "pa_evidencia" not in st.session_state: st.session_state["pa_evidencia"] = ""
    if "pa_prazo"     not in st.session_state: st.session_state["pa_prazo"]     = date.today() + timedelta(days=15)
    if "pa_prompt_sel" not in st.session_state: st.session_state["pa_prompt_sel"] = ""

    col_form, col_guia = st.columns([1.6, 1], gap="large")

    # ── COLUNA ESQUERDA: formulário ──────────────────────────────────────
    with col_form:
        st.markdown("""
        <div class="vl-pa-header">
            <p class="vl-pa-title">Criar plano de ação</p>
            <p class="vl-pa-sub">Selecione um prompt ou preencha manualmente</p>
        </div>""", unsafe_allow_html=True)

        # Seleção de produtor
        if tem_dados:
            produtores_opts = scores_df[["id_produtor","municipio","classe_risco"]].copy()
            produtores_opts["label"] = produtores_opts.apply(
                lambda r: f"#{r['id_produtor']} — {r['municipio']} [{r['classe_risco']}]", axis=1
            )
            prod_label = st.selectbox("Produtor / Fazenda *", produtores_opts["label"].tolist())
            idx = produtores_opts["label"].tolist().index(prod_label)
            id_prod_sel  = str(produtores_opts.iloc[idx]["id_produtor"])
            classe_risco = str(produtores_opts.iloc[idx]["classe_risco"])
            polo_sel     = str(scores_df.loc[
                scores_df["id_produtor"].astype(str)==id_prod_sel, "polo_climatico"
            ].values[0]) if "polo_climatico" in scores_df.columns else "—"
        else:
            id_prod_sel  = st.text_input("ID do Produtor *", placeholder="Ex.: 42")
            polo_sel     = st.text_input("Polo", placeholder="Ex.: RIO_VERDE")
            classe_risco = "Medio"

        c1, c2, c3 = st.columns(3)
        nome_fazenda = c1.text_input("Nome da fazenda", placeholder="Fazenda São João")
        responsavel  = c2.text_input("Responsável", placeholder="Técnico de campo")

        # Dimensão — controla os prompts exibidos na coluna direita
        dim_idx = DIMENSOES.index(st.session_state["pa_dimensao"]) if st.session_state["pa_dimensao"] in DIMENSOES else 0
        dimensao = c3.selectbox("Dimensão *", DIMENSOES, index=dim_idx, key="sel_dimensao_form",
                                on_change=lambda: st.session_state.update({"pa_prompt_sel":""}))
        st.session_state["pa_dimensao"] = dimensao

        c4, c5 = st.columns(2)
        prazo  = c4.date_input("Prazo *", value=st.session_state["pa_prazo"])
        status = c5.selectbox("Status inicial", STATUS_OPTS, index=0)

        descricao = st.text_area(
            "Descrição da ação *",
            value=st.session_state["pa_descricao"],
            placeholder="Selecione um prompt ao lado ou descreva a ação aqui...",
            height=130, key="ta_descricao",
        )
        evidencia = st.text_input(
            "Evidência sugerida",
            value=st.session_state["pa_evidencia"],
            placeholder="Ex.: Relatório de visita, laudo laboratorial...",
            key="ti_evidencia",
        )

        if st.button("💾 Salvar plano de ação", type="primary", use_container_width=True, key="btn_salvar"):
            if not descricao.strip():
                st.warning("Descreva a ação a ser realizada.")
            elif not id_prod_sel:
                st.warning("Selecione ou informe o produtor.")
            else:
                id_plano = _salvar_plano({
                    "id_produtor": id_prod_sel, "nome_fazenda": nome_fazenda,
                    "polo": polo_sel, "dimensao": dimensao,
                    "descricao_acao": descricao, "responsavel": responsavel,
                    "prazo": prazo, "status": status, "evidencia": evidencia,
                })
                st.success(f"✅ Plano **{id_plano}** criado!")
                # Limpa formulário
                for k in ["pa_descricao","pa_evidencia","pa_prompt_sel"]:
                    st.session_state[k] = ""
                st.session_state["pa_prazo"] = date.today() + timedelta(days=15)
                st.rerun()

    # ── COLUNA DIREITA: prompts inteligentes ─────────────────────────────
    with col_guia:
        st.markdown("### 💡 Prompts de Ação")
        st.caption(f"Sugestões para a dimensão **{dimensao}**. Clique para usar.")

        prompts = _prompts_para(dimensao, classe_risco)
        urgencia_cor = {"Alta": "vl-p-alta", "Media": "vl-p-media", "Baixa": "vl-p-baixa"}

        for i, p in enumerate(prompts):
            cor = urgencia_cor.get(p["urgencia"], "vl-p-baixa")
            sel = st.session_state.get("pa_prompt_sel") == p["tag"]
            borda = "border-color:#4ADE80;" if sel else ""

            st.markdown(f"""
            <div class="vl-prompt-card {'selected' if sel else ''}" style="{borda}">
                <span class="vl-prompt-urgencia {cor}">{p['urgencia']}</span>
                <p class="vl-prompt-titulo">{p['titulo']}</p>
                <p class="vl-prompt-desc">{p['descricao']}</p>
                <p class="vl-prompt-path">📍 <strong>Caminho:</strong> {p['caminho'][0]}</p>
                <p class="vl-prompt-meta">📅 Prazo sugerido: {p['prazo_dias']} dias
                &nbsp;·&nbsp; 📋 {p['evidencia_sugerida'][:55]}...</p>
            </div>""", unsafe_allow_html=True)

            if st.button(f"↳ Usar este prompt", key=f"prompt_{i}_{p['tag']}", use_container_width=True):
                # Monta descrição completa com caminho passo a passo
                caminho_txt = "\n".join(p["caminho"])
                descricao_completa = f"{p['descricao']}\n\nCaminho sugerido:\n{caminho_txt}"
                st.session_state["pa_descricao"]  = descricao_completa
                st.session_state["pa_evidencia"]  = p["evidencia_sugerida"]
                st.session_state["pa_prazo"]      = date.today() + timedelta(days=p["prazo_dias"])
                st.session_state["pa_dimensao"]   = p["dimensao"]
                st.session_state["pa_prompt_sel"] = p["tag"]
                st.rerun()

        # Guia de boas práticas no rodapé
        with st.expander("📖 Guia de boas práticas — quando agir?", expanded=False):
            guias = {
                "Qualidade":     ("CCS > 400 ou CBT > 100", "Visita técnica em até 48h"),
                "Volume":        ("Queda > 10% em 2 semanas", "Diagnóstico nutricional em 7 dias"),
                "Logística":     ("Falha de coleta > 2%", "Revisão de rota em 15 dias"),
                "Continuidade":  ("Sinal de churn ou margem < média", "Visita comercial em 72h"),
                "Operacional":   ("Falha operacional recorrente", "Treinamento em 20 dias"),
                "Relacionamento":("Sem visita há 60+ dias", "Agendamento imediato"),
            }
            for dim, (gatilho, resposta) in guias.items():
                ativo = "▶ " if dim == dimensao else ""
                st.markdown(f"""
                <div class="vl-guia-item">
                    <p class="vl-guia-step">{ativo}{dim} — Gatilho: {gatilho}</p>
                    <p class="vl-guia-text">Resposta recomendada: {resposta}</p>
                </div>""", unsafe_allow_html=True)


# ============================================================
# ABA ACOMPANHAR
# ============================================================
with tab_acompanhar:
    st.markdown("""
    <div class="vl-pa-header">
        <p class="vl-pa-title">Acompanhamento de planos</p>
        <p class="vl-pa-sub">Atualize status, registre evidências e encerre ações concluídas</p>
    </div>""", unsafe_allow_html=True)

    df_planos = _carregar_planos()

    if df_planos.empty:
        st.info("Nenhum plano cadastrado ainda. Crie o primeiro na aba **Novo Plano**.")
    else:
        fc1, fc2, fc3 = st.columns(3)
        f_status = fc1.multiselect("Status", STATUS_OPTS, default=["Aberto","Em curso"])
        f_dim    = fc2.multiselect("Dimensão", DIMENSOES, default=DIMENSOES)
        f_prod   = fc3.text_input("Buscar produtor / fazenda", placeholder="ID ou nome")

        filtrado = df_planos.copy()
        if f_status: filtrado = filtrado[filtrado["status"].isin(f_status)]
        if f_dim:    filtrado = filtrado[filtrado["dimensao"].isin(f_dim)]
        if f_prod.strip():
            mask = (
                filtrado["id_produtor"].astype(str).str.contains(f_prod, case=False, na=False) |
                filtrado["nome_fazenda"].astype(str).str.contains(f_prod, case=False, na=False)
            )
            filtrado = filtrado[mask]

        st.caption(f"{len(filtrado)} plano(s) encontrado(s)")

        for _, row in filtrado.iterrows():
            prazo_dt  = pd.to_datetime(row["prazo"]).date() if pd.notna(row["prazo"]) else None
            atrasado  = prazo_dt and prazo_dt < date.today() and row["status"] not in ("Concluído","Cancelado")
            prazo_str = f"{'⚠️ ' if atrasado else ''}{prazo_dt}" if prazo_dt else "—"
            css_key   = row["status"].lower().replace(" ","_").replace("í","i").replace("ú","u").replace("ó","o")

            with st.expander(
                f"**{row['id_plano']}** · #{row['id_produtor']} {row.get('nome_fazenda','') or ''} "
                f"· {row['dimensao']} · {prazo_str}", expanded=False
            ):
                st.markdown(f"<span class='vl-status-{css_key}'>{row['status']}</span>",
                            unsafe_allow_html=True)
                st.markdown(f"**Ação:** {row['descricao_acao']}")
                if row.get("evidencia"):
                    st.markdown(f"**Evidência:** {row['evidencia']}")
                st.caption(f"Responsável: {row['responsavel']} · Criado: {row['criado_em']}")

                with st.form(f"upd_{row['id_plano']}", clear_on_submit=False):
                    uc1, uc2 = st.columns(2)
                    novo_status = uc1.selectbox("Status", STATUS_OPTS,
                        index=STATUS_OPTS.index(row["status"]), key=f"st_{row['id_plano']}")
                    nova_ev = uc2.text_input("Evidência", value=row.get("evidencia","") or "",
                        key=f"ev_{row['id_plano']}")
                    novo_resp = st.text_input("Responsável", value=row.get("responsavel","") or "",
                        key=f"rp_{row['id_plano']}")
                    cs, cd = st.columns([3,1])
                    salvar_upd = cs.form_submit_button("💾 Salvar", use_container_width=True)
                    excluir    = cd.form_submit_button("🗑️ Excluir", use_container_width=True)

                if salvar_upd:
                    _salvar_plano({
                        "id_plano": row["id_plano"], "id_produtor": row["id_produtor"],
                        "nome_fazenda": row.get("nome_fazenda",""), "polo": row.get("polo",""),
                        "dimensao": row["dimensao"], "descricao_acao": row["descricao_acao"],
                        "responsavel": novo_resp, "prazo": row["prazo"],
                        "status": novo_status, "evidencia": nova_ev,
                    })
                    st.success("Atualizado!")
                    st.rerun()

                if excluir:
                    _excluir_plano(row["id_plano"])
                    st.warning("Plano excluído.")
                    st.rerun()


# ============================================================
# ABA PAINEL
# ============================================================
with tab_painel:
    st.markdown("""
    <div class="vl-pa-header">
        <p class="vl-pa-title">Painel geral de planos</p>
        <p class="vl-pa-sub">Visão consolidada por status, dimensão e produtores</p>
    </div>""", unsafe_allow_html=True)

    df_todos = _carregar_planos()

    if df_todos.empty:
        st.info("Nenhum plano cadastrado ainda.")
    else:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total",     len(df_todos))
        k2.metric("Abertos",   len(df_todos[df_todos["status"]=="Aberto"]))
        k3.metric("Em curso",  len(df_todos[df_todos["status"]=="Em curso"]))
        k4.metric("Concluídos",len(df_todos[df_todos["status"]=="Concluído"]))

        df_todos["prazo_dt"] = pd.to_datetime(df_todos["prazo"], errors="coerce").dt.date
        atrasados = df_todos[
            (df_todos["prazo_dt"] < date.today()) &
            (~df_todos["status"].isin(["Concluído","Cancelado"]))
        ]
        if not atrasados.empty:
            st.warning(f"⚠️ **{len(atrasados)} plano(s) com prazo vencido**")

        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            fig_s = px.pie(df_todos, names="status", title="Por status",
                color="status", color_discrete_map={
                    "Aberto":"#3B82F6","Em curso":"#F59E0B",
                    "Concluído":"#10B981","Cancelado":"#6B7280"})
            aplicar_layout_plotly(fig_s)
            st.plotly_chart(fig_s, use_container_width=True)
        with g2:
            cnt = df_todos.groupby("dimensao").size().reset_index(name="total")
            fig_d = px.bar(cnt, x="dimensao", y="total", title="Por dimensão",
                color="total", color_continuous_scale=["#1e3a5f","#4ADE80"])
            aplicar_layout_plotly(fig_d)
            st.plotly_chart(fig_d, use_container_width=True)

        cols_exib = ["id_plano","id_produtor","nome_fazenda","dimensao",
                     "responsavel","prazo","status"]
        cols_exib = [c for c in cols_exib if c in df_todos.columns]
        st.dataframe(df_todos[cols_exib], use_container_width=True, hide_index=True,
            column_config={
                "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTS),
                "prazo":  st.column_config.DateColumn("Prazo", format="DD/MM/YYYY"),
            })

st.caption("VIA LEITE SENSE · Plano de Ação por Produtor · USINA I.A. Tecnologia e Inovação")
