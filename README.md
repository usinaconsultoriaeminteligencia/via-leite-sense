# VIA LEITE SENSE

**Radar de Risco Produtivo, Qualidade e Rentabilidade para a Cadeia Leiteira**

Plataforma de IA preditiva que integra dados climáticos, operacionais e indicadores
de qualidade para **antecipar queda de produção, perda de qualidade, risco de
penalização/bônus e necessidade de ação preventiva** — antes que a perda ocorra.

Desenvolvido por **USINA I.A.** para o **Desafio AgroStartup SENAR/SEBRAE Goiás 2026**.

🔗 **Demo ao vivo:** https://via-leite-sense.vercel.app
🔗 **API (backend):** https://via-leite-sense-api-production.up.railway.app
🔗 **GitHub:** https://github.com/usinaconsultoriaeminteligencia/via-leite-sense

> **Arquitetura de produção:** frontend SPA na **Vercel** consumindo a **API FastAPI
> na Railway** (DuckDB em volume persistente). O app **Streamlit** foi descomissionado —
> `via-leite-sense.streamlit.app` agora redireciona para a Vercel. O código Streamlit
> Streamlit foi removido em 25/08/2026 — `via_leite_app.py` é apenas a página de
> redirect, que existe para não quebrar os QR codes e links já impressos do pitch.
> O app completo permanece no histórico do Git (até `0c945aa`).

---

## O que o VIA LEITE SENSE resolve

A cadeia leiteira premium opera com uma assimetria crítica de informação: produtores,
cooperativas e laticínios identificam problemas de qualidade e queda de produção
**após a coleta** — quando a perda já é irreversível.

O VIA LEITE SENSE transforma esse modelo reativo em gestão preditiva. Ao cruzar
dados climáticos (INMET), indicadores operacionais (CCS, CBT, temperatura do tanque,
litros coletados) e variáveis logísticas, a plataforma antecipa com até 30 dias
os riscos que causam perda de produtividade e rentabilidade.

> **Descarte de leite é monitorado pela plataforma, mas é uma consequência —
> não a dor central. A dor central é a falta de antecipação.**

---

## Score VIA LEITE de Risco Produtivo

Cada produtor, rota e laticínio recebe um score consolidado de 0 a 100:

| Faixa | Classe | Ação recomendada |
|-------|--------|-----------------|
| 0–25  | 🟢 Baixo risco | Monitoramento padrão |
| 26–50 | 🟡 Atenção | Revisão preventiva |
| 51–75 | 🔴 Alto risco | Ação corretiva imediata |
| 76–100 | 🟣 Crítico | Intervenção urgente |

O score combina 7 dimensões de risco ponderadas, com contribuição contínua
de THI (estresse térmico) e tendência de queda de produção.

---

## Módulos da plataforma

| Módulo | Descrição |
|--------|-----------|
| 🎯 **Radar de Risco** | Página executiva — score, ranking e horizonte 7/15/30 dias |
| 📊 **Executivo** | KPIs estratégicos da cooperativa |
| ⚙️ **Operacional** | Rotas, coletas, logística |
| 👨‍🌾 **Produtores** | Performance individual |
| 🌤️ **Clima** | THI, precipitação, estresse térmico |
| 🏭 **Fornecedores 360** | Score premium com gauge + radar 4D |
| 🌱 **Antes & Depois — ESG** | ROI da plataforma + narrativa de sustentabilidade |
| 📋 **Gestão e Dados** | Lançamentos manuais por laticínio |
| 🔌 **Via Leite Edge** | Monitoramento IoT em modo simulado |
| 🎭 **Demo Tour** | Pitch guiado de 5 minutos |

---

## Documentação estratégica

| Documento | Conteúdo |
|-----------|----------|
| [docs/visao_produto.md](docs/visao_produto.md) | Missão, proposta de valor, posicionamento, público-alvo |
| [docs/arquitetura_dados.md](docs/arquitetura_dados.md) | Fontes de dados, indicadores, métodos de entrada, schema CSV |
| [docs/roadmap.md](docs/roadmap.md) | Fases 1–4 com status, entregas e critérios de conclusão |
| [docs/validacao_mercado.md](docs/validacao_mercado.md) | Hipóteses, perguntas de entrevista, critérios de validação do MVP |

---

## Stack tecnológica

- **Python 3.11+** — linguagem principal
- **Streamlit** — dashboard interativo
- **Scikit-learn** — modelo preditivo de regressão + scoring de risco
- **Pandas / NumPy** — processamento de dados
- **Plotly** — visualizações interativas
- **FastAPI** — API backend (opcional)
- **FPDF2** — exportação de relatórios PDF

---

## Instalação

```bash
pip install -r requirements.txt
```

---

## Execução

### Fluxo 1 — Clima sintético (demonstração imediata)

```bash
python gerador_leite_sintetico.py --output-dir dados_teste
python treino_mvp_avancado.py
streamlit run via_leite_app.py
```

### Fluxo 2 — Clima real INMET

```bash
# 1. Colocar CSVs do INMET em dados_inmet_raw/
python ingestao_clima_inmet.py --raw-dir dados_inmet_raw --out-dir dados_inmet_processado
python gerador_leite_sintetico.py --use-real-climate \
  --real-climate-path dados_inmet_processado/fact_clima_diario_inmet.csv \
  --output-dir dados_teste
python treino_mvp_avancado.py
streamlit run via_leite_app.py
```

### Fluxo 3 — Gerar artefatos de ranking de risco

```bash
python score_risco.py
# Saída: artefatos_teste/ranking_risco_produtor.csv
#         artefatos_teste/ranking_risco_rota.csv
#         artefatos_teste/ranking_risco_laticinio.csv
```

### Fluxo 4 — Piloto com dados reais importados

```bash
python validar_pacote_dados_reais.py --data-dir CAMINHO_DO_PACOTE
python executar_piloto_real.py \
  --input-dir CAMINHO_DO_PACOTE \
  --base-dir dados_piloto_cliente \
  --artefatos-dir artefatos_piloto_cliente
```

---

## Credenciais de acesso

| Perfil | Usuário | Senha | Acesso |
|--------|---------|-------|--------|
| Demonstração | `demo` | `demo2025` | Todas as páginas de leitura |
| Laticínio | `laticinio` | `leite2025` | Inclui gestão e plano de ação |
| Admin | `admin` | _privada_ | Acesso completo |

> A autenticação por utilizador saiu com o app Streamlit em 25/08/2026. A API em
> produção autentica por `X-API-Key` em todas as rotas exceto `/health`
> (`backend/security.py`) — ver ALERTA-005, fechado em 06/08.

---

## Controle de acesso por página

| Página | demo 👁️ | laticinio 🏭 | admin 🔑 |
|--------|---------|-------------|---------|
| Radar de Risco | ✅ | ✅ | ✅ |
| Executivo | ✅ | ✅ | ✅ |
| Operacional | ✅ | ✅ | ✅ |
| Produtores | ✅ | ✅ | ✅ |
| Clima | ✅ | ✅ | ✅ |
| Fornecedores 360 | ✅ | ✅ | ✅ |
| Antes & Depois ESG | ✅ | ✅ | ✅ |
| Via Leite Edge | ✅ | ✅ | ✅ |
| Demo Tour | ✅ | ✅ | ✅ |
| Gestão e dados | ❌ | ✅ | ✅ |
| Plano de Ação | ❌ | ✅ | ✅ |

---

## Impacto esperado com a plataforma

| Indicador | Melhora média esperada |
|-----------|----------------------|
| Redução de descarte | 50–60% |
| Melhora de CCS | 25–35% |
| Melhora de CBT | 35–45% |
| Ganho de receita mensal (médio produtor) | R$ 800–1.500/mês |
| CO₂ equivalente evitado (cooperativa 50 prod.) | 180+ toneladas/ano |

*Benchmarks: Embrapa Gado de Leite, MAPA IN 77/2018, FAO (2010).*

---

## Roadmap

- [x] Fase 1 — MVP com entrada simplificada e clima INMET integrado
- [x] Fase 3 — Score VIA LEITE de Risco Produtivo (antecipado para Sprint 4)
- [ ] Fase 2 — Piloto com laticínios/cooperativas e importação CSV/API
- [ ] Fase 4 — Via Leite Edge com sensores IoT e telemetria em tempo real

Detalhes: [docs/roadmap.md](docs/roadmap.md)

---

## Sobre

**VIA LEITE SENSE** é desenvolvido pela [USINA I.A.](https://www.usinaia.com.br),
estúdio de tecnologia e IA para PMEs, setor público e agronegócio — Goiânia, GO.

Submetido ao **Desafio AgroStartup 2026** — SENAR / SEBRAE Goiás.
