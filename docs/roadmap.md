# Roadmap — VIA LEITE SENSE

**Versão:** 2.0 — Sprint 4 | **Data:** Junho 2026

---

## Visão de evolução do produto

O VIA LEITE SENSE evolui em quatro fases, cada uma expandindo o alcance
do produto de uma solução de análise histórica para um sistema de
inteligência preditiva em tempo real com telemetria IoT.

```
Fase 1        Fase 2        Fase 3        Fase 4
  │             │             │             │
  ▼             ▼             ▼             ▼
MVP com       Piloto com    Score de      IoT + Teleme-
entrada       laticínios    Risco         tria em
simplificada  reais + CSV   Produtivo     Tempo Real
  │             │             │             │
Validar       Validar       Validar       Escalar
arquitetura   demanda       modelo        produto
```

---

## Fase 1 — MVP com entrada simplificada e clima integrado

**Status:** ✅ Concluído (Sprints 1–3)

**Objetivo:** Validar a arquitetura técnica e a hipótese de que dados
climáticos e operacionais sintéticos são suficientes para demonstrar
o valor da plataforma antes da coleta de dados reais.

### Entregas

- [x] Gerador de base sintética operacional (`gerador_leite_sintetico.py`)
- [x] Ingestão de clima real INMET (`ingestao_clima_inmet.py`)
- [x] Modelo preditivo de volume coletado (`treino_mvp_avancado.py`)
- [x] Dashboards Executivo, Operacional, Produtores, Clima
- [x] Autenticação com 3 perfis (admin, laticínio, demo)
- [x] Score Premium Visual — gauge Plotly + radar 4D por fornecedor
- [x] Modo Demo Tour — pitch guiado de 5 minutos
- [x] Exportação de relatório PDF A4 por fornecedor
- [x] Deploy em produção (Streamlit Cloud)
- [x] Via Leite Edge — arquitetura IoT simulada

### Critério de conclusão

Produto demonstrável ao vivo para avaliadores, investidores e potenciais
clientes sem dependência de dados reais de fazenda.

---

## Fase 2 — Piloto com laticínios/cooperativas e importação CSV/API

**Status:** 🔄 Planejado — pós-maratona SEBRAE Goiás (julho/agosto 2026)

**Objetivo:** Validar o produto com dados reais de pelo menos um laticínio
ou cooperativa parceira no Sul Goiano, ajustando o modelo preditivo com
dados históricos reais e coletando evidências de impacto econômico.

### Entregas previstas

- [ ] Onboarding estruturado de cliente piloto (`onboarding_cliente.py` — já existe)
- [ ] Validação de pacote de dados reais (`validar_pacote_dados_reais.py` — já existe)
- [ ] Pipeline de importação e normalização (`executar_piloto_real.py` — já existe)
- [ ] Ajuste do modelo com dados reais de fazenda (re-treino com sazonalidade real)
- [ ] API REST para integração com sistemas de gestão de laticínios
- [ ] Módulo de comparação de performance real vs. previsto
- [ ] Relatório de piloto com evidências de redução de risco

### Parceiros potenciais

Cooperativas e laticínios do Sul Goiano (Rio Verde, Jataí, Mineiros) —
região com maior concentração de produtores de leite premium de Goiás.

### Critério de conclusão

Pelo menos 1 laticínio utilizando a plataforma com dados reais por
30 dias, com registro mensurável de redução de eventos de risco.

---

## Fase 3 — Score de risco produtivo e qualidade

**Status:** ✅ Concluído antecipadamente — Sprint 4 (Junho 2026)

**Objetivo:** Adicionar camada analítica de classificação de risco sobre
o modelo de regressão existente, criando o Score VIA LEITE consolidado.

### Entregas

- [x] Motor de scoring de risco (`score_risco.py`)
- [x] 7 targets derivados de risco (queda produção, qualidade, CCS, CBT, tanque, bônus, descarte)
- [x] Score VIA LEITE 0–100 com 4 classes (Baixo / Atenção / Alto / Crítico)
- [x] Impacto econômico estimado por produtor/rota/laticínio
- [x] Ranking de prioridade de ação preventiva
- [x] Página executiva Radar de Risco (horizonte 7/15/30 dias)
- [x] Painel Antes/Depois com narrativa ESG
- [x] Artefatos CSV de ranking exportáveis

### Observação

Esta fase foi antecipada para o Sprint 4 por demanda do Desafio AgroStartup
SENAR/SEBRAE Goiás 2026. O Score VIA LEITE é agora o elemento central
da proposta de valor e do pitch da plataforma.

---

## Fase 4 — VIA LEITE EDGE com sensores IoT e telemetria

**Status:** ⬜ Planejado — 2026/2027

**Objetivo:** Substituir o modo simulado de IoT por integração real com
sensores físicos instalados nas fazendas, eliminando a dependência de
entrada manual de dados e habilitando alertas em tempo real.

### Arquitetura alvo

```
Fazenda (Edge)              Cloud (VIA LEITE)
     │                            │
     ├─ Sensor temperatura tanque ─┤
     ├─ Sensor THI local          ─┤──► MQTT Broker ──► FastAPI Backend
     ├─ GPS caminhão coleta       ─┤                         │
     └─ Sensor nível tanque       ─┘                    Dashboard
                                                        + Alertas
                                                        + Score Tempo Real
```

### Entregas previstas

- [ ] Protocolo MQTT para sensores de temperatura do tanque
- [ ] Sensores climáticos locais (substituir INMET por dados da fazenda)
- [ ] GPS em caminhões de coleta (rastreamento e tempo estimado)
- [ ] Painel de telemetria em tempo real (via_leite_edge — já existe em modo simulado)
- [ ] Alertas push para gestor do laticínio
- [ ] API pública para integração com sistemas de terceiros

### Variáveis de ambiente já preparadas

```bash
# Ativar modo IoT real (substituir simulado)
$env:IOT_SIMULATION_MODE='false'
$env:IOT_PROVIDER='mqtt'

# Endpoints já definidos na arquitetura atual
GET /api/iot/simulated-readings
GET /api/iot/farms/{farm_id}/latest
GET /api/iot/alerts
```

### Critério de conclusão

Pelo menos 3 fazendas com sensores físicos instalados, transmitindo
dados em tempo real para o dashboard sem intervenção manual.

---

## Resumo do roadmap

| Fase | Status | Período | Entrega principal |
|------|--------|---------|-------------------|
| Fase 1 — MVP | ✅ Concluído | Dez 2025 – Abr 2026 | Produto demonstrável ao vivo |
| Fase 2 — Piloto real | 🔄 Planejado | Jul – Set 2026 | Validação com dados reais |
| Fase 3 — Score de Risco | ✅ Concluído | Jun 2026 | Score VIA LEITE + Radar de Risco |
| Fase 4 — IoT/Edge | ⬜ Futuro | 2027 | Telemetria em tempo real |

---

*VIA LEITE SENSE — Roadmap | USINA I.A. © 2026*
