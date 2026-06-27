# Plano de Negócio — VIA LEITE SENSE

**Radar de Risco Produtivo, Qualidade e Rentabilidade para a Cadeia Leiteira**

| | |
|---|---|
| **Empresa** | USINA I.A. — Tecnologia e Inovação (Goiânia, GO) |
| **Produto** | VIA LEITE SENSE |
| **Versão** | 2.0 — plano consolidado (funde diagnóstico de mercado + status real do produto) |
| **Data** | 27 de junho de 2026 |
| **Estágio** | MVP em produção · pré-piloto pago · pré-receita |
| **Contexto** | Desafio AgroStartup SENAR/SEBRAE Goiás 2026 |
| **Demo** | https://via-leite-sense.streamlit.app (`demo` / `demo2025`) |

> **Nota de versão.** Esta v2.0 incorpora um diagnóstico de mercado externo (dados IBGE/SIDRA
> 2024, framework de unit economics, compliance e GTM B2B2F) **corrigindo** seu erro central:
> aquele diagnóstico foi produzido sem acesso ao repositório real e tratou o projeto como
> "pré-MVP / concepção". Na verdade o VIA LEITE SENSE **já tem MVP em produção, motor de score,
> pipeline de dados reais e protótipo** — está à frente em produto e atrás em validação comercial.

---

## 1. Sumário executivo

A cadeia leiteira opera com uma **assimetria crítica de informação**: produtores, cooperativas
e laticínios identificam queda de produção e perda de qualidade **depois da coleta**, quando a
perda já é irreversível e já foi paga. A qualidade vem de um exame de laboratório mensal — quando
o resultado chega, já caiu o pagamento e se perdeu o bônus.

O **VIA LEITE SENSE** transforma esse modelo reativo em **gestão preditiva**. Cruzando dados
climáticos (INMET), operacionais (CCS, CBT, temperatura do tanque, litros) e logísticos, gera um
**Score VIA LEITE de Risco (0–100)** que antecipa em **7, 15 e 30 dias** quem terá problema (o
*quando agir*), complementado por um **Perfil estrutural do produtor** — Consistente, Oscilante
ou Desafiador (o *como agir*). O produtor recebe tudo traduzido no **WhatsApp** que já usa.

- **Mercado (IBGE/SIDRA 2024):** o Brasil produziu **35,7 bilhões de litros**, com valor de
  produção de **R$ 87,5 bilhões** (≈ **R$ 2,45/L**). Cadeia grande, fragmentada e digitalizando.
- **Modelo:** SaaS B2B2F — laticínio/cooperativa paga **licença de plataforma + assinatura por
  produtor monitorado**; canal direto para fazendas médias/grandes como segunda via.
- **Preço:** R$ 39 (Básico) a R$ 69 (Pro) por produtor/mês no canal B2B2F; licença de
  cooperativa/laticínio a partir de R$ 6 mil/mês; planos diretos R$ 249–1.499/fazenda/mês.
- **Beachhead:** **Goiás** (5º maior estado leiteiro, 8,2% do país) — desafio SENAR/SEBRAE, rede
  local e diferencial climático do Sul Goiano — expandindo para **MG/PR/RS/SC** (juntos com GO =
  **69%** da produção nacional).
- **Meta de 3 anos (SOM, cenário base):** **~R$ 3,2 milhões de ARR**.
- **Tração:** produto **funcionando e demonstrável ao vivo**; modelo de previsão de volume com
  **R² de 99,4%**; pipeline de dados reais pronto. **Ask:** primeiro laticínio parceiro para
  **piloto pago de 30–90 dias** no Sul Goiano, com baseline e relatório de ROI.

---

## 2. Status real do projeto (diagnóstico corrigido)

Um diagnóstico externo classificou o projeto como "concepção / pré-MVP, sem evidências". Esse
diagnóstico **buscou no diretório errado** e não enxergou os artefatos reais. O status correto:

| Área | Diagnóstico externo (incorreto) | **Status real (verificado no repositório)** |
|---|---|---|
| Definição de produto | "Inicial, falta escopo" | ✅ Produto definido: Radar de Risco + Score + Perfil + 10 módulos |
| Tecnologia | "Não comprovada, sem código" | ✅ MVP em produção (Streamlit Cloud); motor de score; R² 99,4%; arquitetura IoT-ready (MQTT) |
| Pipeline de dados | "Inexistente" | ✅ Validação e execução de piloto com dados reais já codificadas |
| Material de pitch/marca | "Inexistente" | ✅ Protótipo de 14 páginas, roteiro de pitch, identidade visual em PDF |
| Validação com clientes | "Não comprovada" | ⚠️ **Correto** — sem piloto pago, LOI ou contrato ainda |
| Base de dados de produtos | — | ⚠️ Hoje **sintética** (valida arquitetura); dados reais entram no piloto |
| Modelo de negócio / unit economics | "Não comprovado" | ⚠️ **Parcialmente correto** — preço definido, mas não testado em campo |
| Prontidão para captar | "Baixa a média" | ⚠️ **Correto** — falta prova de cliente e tração comercial |

**Leitura honesta:** estamos **à frente em produto e tecnologia** do que o diagnóstico externo
supôs, e **no ponto que ele aponta em validação comercial** — sem receita, sem piloto pago, base
ainda sintética. A prioridade dos próximos 90 dias é exatamente a que o diagnóstico recomenda:
**transformar o MVP pronto em piloto pago e mensurável**, com baseline e ROI documentado.

---

## 3. O problema

A gestão de qualidade do leite hoje é **reativa**. O modelo gera perdas que aparecem tarde demais:

**Para o produtor:**
- Queda de produção por animal/lote sem causa clara, percebida tarde.
- Mastite e problemas sanitários detectados tardiamente.
- Falha de resfriamento do tanque → descarte.
- Leite fora dos padrões IN 77/2018 (CCS/CBT) → penalidade no pagamento.
- Perda de bônus por qualidade; baixa visibilidade do impacto financeiro.

**Para o laticínio/cooperativa:**
- Sem visão preditiva de volume e qualidade por fornecedor.
- Atuação reativa — o problema só aparece na coleta ou no laboratório.
- Alto custo de assistência técnica presencial.
- Dificuldade de priorizar produtores por risco e potencial.

> **A dor central não é o descarte — é a falta de antecipação.** O descarte é o sintoma mais
> visível; a causa é a ausência de um radar de risco. Mesmo produtores sem descarte elevado
> sofrem de falta de previsibilidade, o que amplia o mercado endereçável.

---

## 4. Mercado e oportunidade

### 4.1 Tamanho (dados oficiais IBGE/SIDRA 2024 — verificados na fonte)

| Indicador | Valor 2024 |
|---|---|
| Produção nacional de leite | **35.743.862 mil L** (≈ 35,7 bi L) |
| Valor da produção | **R$ 87.511.969 mil** (≈ R$ 87,5 bi) |
| Preço médio implícito | **≈ R$ 2,45/L** |

Esse valor de produção sustenta um **TAM amplo**. A tese, porém, é construída sobre um SAM
realista: produtores e laticínios com escala, dor econômica clara e capacidade de pagar.

### 4.2 Concentração geográfica (produção 2024, IBGE/SIDRA)

| Estado | Produção 2024 | % Brasil |
|---|---|---|
| Minas Gerais | 9,78 bi L | 27,4% |
| Paraná | 4,62 bi L | 12,9% |
| Rio Grande do Sul | 4,03 bi L | 11,3% |
| Santa Catarina | 3,30 bi L | 9,2% |
| **Goiás** | **2,92 bi L** | **8,2%** |
| **Top 5 (MG+PR+RS+SC+GO)** | **24,65 bi L** | **≈ 69%** |

### 4.3 TAM / SAM / SOM

| Nível | Definição | Estimativa |
|---|---|---|
| **TAM** | Valor da produção leiteira nacional (proxy de cadeia endereçável por software de gestão/qualidade) | R$ 87,5 bi/ano de produção; mercado de software/serviços associado na casa de centenas de milhões de R$ |
| **SAM** | Fazendas médias (>500 L/dia) + laticínios/cooperativas no Top 5 de estados | Milhares de fazendas-alvo; centenas de laticínios/cooperativas |
| **SOM (3 anos)** | Goiás-first → expansão Sul/Sudeste, canal B2B2F | **≈ R$ 3,2 mi de ARR (cenário base)** |

### 4.4 Drivers de demanda
Pressão por qualidade e bonificação; perdas por mastite/descarte; falta de dados confiáveis na
fazenda média; dificuldade dos laticínios em prever volume e risco por fornecedor; escassez de
mão de obra qualificada; digitalização crescente do agro; **estresse térmico sazonal** (THI) —
fator crítico no Centro-Oeste e diferencial do nosso modelo climático.

---

## 5. Cliente-alvo e segmentos

**Primário — fazendas leiteiras médias.** 50–300 vacas em lactação ou >500 L/dia; ordenha
mecânica e tanque de expansão; histórico de mastite/qualidade/variação; gestor aberto a
tecnologia; em bacias de GO (largada) e MG/PR/RS/SC (expansão). Dor econômica suficiente e
decisão acessível.

**Secundário — laticínios e cooperativas.** 100–2.000 fornecedores; dor em qualidade,
previsibilidade de volume e fidelização. **Este é o canal que paga e distribui** (B2B2F): reduz
CAC, aumenta confiança e cria distribuição em bloco.

**Terciário — veterinários, consultores, nutricionistas.** Canal de indicação e parceiro
operacional, não comprador inicial. O produto gera relatórios úteis para eles, **sem substituí-los**.

---

## 6. Proposta de valor

**Para o produtor:** *"Descubra cedo onde a fazenda perde leite e dinheiro — antes da perda virar
penalidade."* Alertas de queda de produção, temperatura de tanque e anomalias; histórico simples
de ocorrências e qualidade; indicadores traduzidos em R$; relatórios para decidir com
veterinário/laticínio.

**Para o laticínio/cooperativa:** *"Transforme a base de fornecedores em uma rede monitorada,
priorizando assistência técnica, qualidade e previsibilidade de coleta."* Ranking de fornecedores
por risco e potencial; alertas antes da coleta; gestão de programas de qualidade; fidelização;
dados para reduzir perdas industriais.

### Dois eixos do produto
| | Score de Risco (o *quando agir*) | Perfil do produtor (o *como agir*) |
|---|---|---|
| Pergunta | "Quem está em risco agora?" | "Que tipo de produtor é este?" |
| Natureza | Dinâmica, preditiva (7/15/30 dias) | Estrutural, descritiva |
| Saída | Ranking de prioridade + impacto em R$ | Recomendação cirúrgica de manejo |

---

## 7. Produto

### 7.1 Módulos (já existentes no MVP)
Radar de Risco · Executivo · Operacional · Produtores · Clima (THI) · Fornecedores 360 ·
Antes & Depois (ESG) · Gestão e Dados · Via Leite Edge (IoT simulado) · Demo Tour.

### 7.2 Score VIA LEITE de Risco (0–100)
Combina **7 dimensões** ponderadas (queda de produção, qualidade, CCS, CBT, temperatura do tanque,
bônus, descarte), ancoradas na **IN 77/2018**, com contribuição contínua de THI.

| Faixa | Classe | Ação |
|---|---|---|
| 0–25 | 🟢 Baixo | Monitoramento padrão |
| 26–50 | 🟡 Atenção | Revisão preventiva |
| 51–75 | 🔴 Alto | Ação corretiva imediata |
| 76–100 | 🟣 Crítico | Intervenção urgente |

### 7.3 MVP comercial (próximo ciclo) — alinhado ao foco "alertas simples + ROI"
- **App/painel da fazenda:** cadastro, lançamento diário (ordenha/tanque), ocorrências, indicadores (L/dia, L/vaca, descarte e receita estimados), alertas por WhatsApp.
- **Qualidade e tanque:** importação de laboratório (CCS, CBT, gordura, proteína); sensor simples de temperatura do tanque + alerta de falha de resfriamento; painel de bonificação/penalidade.
- **Inteligência e alertas:** detecção de queda anormal, risco por histórico, recomendações operacionais, calculadora de perda em R$.
- **Painel laticínio/cooperativa:** mapa e ranking de fornecedores por risco, evolução de volume, agenda de assistência técnica, exportação/API.

### 7.4 O que NÃO fazer no MVP
Hardware próprio complexo sem prova de demanda; diagnóstico veterinário automático; resolver
reprodução + nutrição + sanidade + finanças com profundidade ao mesmo tempo; depender de
integração com todos os equipamentos de ordenha; **vender "IA" como produto antes de provar ROI**.

### 7.5 Stack
Python 3.11 · Streamlit · Scikit-learn (regressão + scoring) · Pandas/NumPy · Plotly · FastAPI ·
FPDF2 · ingestão INMET. Deploy em Streamlit Cloud. Arquitetura multi-tenant e **IoT-ready (MQTT)**.

> **Transparência:** dados de mercado são oficiais (IBGE/SIDRA, MilkPoint, Embrapa, MAPA); a base
> operacional atual é **sintética** (valida arquitetura) e nunca é apresentada como real.

---

## 8. Diferenciação competitiva

| Player | Foco | Lacuna |
|---|---|---|
| Cowmed (BR) | Sensores no **animal** (hardware) | Não faz radar preditivo da cadeia |
| DeLaval | Ordenha / automação | Hardware, não risco da carteira |
| Stellapps (Índia) | **Logística** da cooperativa | Não cruza clima + qualidade + economia |
| ERPs agro / consultorias | Registro / serviço | Sem antecipação preditiva acionável |

**Nosso espaço em branco:** ninguém faz o **radar preditivo de risco da cadeia leiteira
brasileira** cruzando **clima + qualidade + impacto econômico**. Diferenciais: **Brasil-first**
(conectividade e margem reais), **B2B2F** (vender via laticínio), **ROI visível** (alerta técnico
→ R$), **baixa fricção** (software-first, sensores simples depois), **WhatsApp no campo**, e
**camada de assistência técnica** que ajuda o veterinário/laticínio a agir melhor.

---

## 9. Modelo de negócio e precificação

**SaaS B2B2F** — o laticínio/cooperativa é o pagador-âncora; o produtor é o usuário. Canal direto
a fazendas médias/grandes como segunda via. Arquitetura de planos que reconcilia preço-por-produtor
(baixo atrito, escala) com preço-por-fazenda (ARPA alto, venda direta):

| Plano | Para quem | Preço |
|---|---|---|
| **Sense B2B2F (núcleo)** | Produtor monitorado, pago pelo laticínio | **R$ 39 (Básico) · R$ 69 (Pro)** /produtor/mês (~R$ 60 médio) |
| **Sense Coop/Laticínio** | Licença de plataforma multi-propriedade | **R$ 6 mil–25 mil/mês** base + R$ 29–99/fazenda |
| **Sense Lite** (direto) | Fazenda pequena/média digitalizando | R$ 249–399/mês + implantação R$ 900–1.500 |
| **Sense Farm** (direto) | Fazenda média com rotina técnica | R$ 699–1.499/mês + implantação R$ 2.500–5.000 |
| **Hardware (opcional)** | Sensor de tanque/gateway | Locação/parceria — **nunca margem negativa** |

**Por que o laticínio paga:** protege a margem — reduz descarte e penalidades, garante o bônus de
qualidade e fideliza o produtor. Um problema de qualidade não-antecipado custa caro, e hoje ele
paga sempre.

**Monetização inicial:** pilotos pagos com ticket simbólico (validar disposição a pagar);
contratos com laticínios para reduzir CAC; hardware em locação/comodato condicionado a contrato
mínimo. **Demais fontes:** implantação/treinamento, API/integrações, relatórios premium e
benchmarking anônimo.

---

## 10. Unit economics (metas)

| Métrica | Meta |
|---|---|
| ARPA — canal B2B2F | ~R$ 60/produtor/mês |
| ARPA — fazenda direta (média) | R$ 700–1.100/mês |
| Margem bruta SaaS | > 75% |
| Margem bruta combinada (com hardware/suporte) | 55–70% |
| CAC por fazenda — canal parceiro | até R$ 3.000 |
| CAC por fazenda — canal direto | até R$ 8.000 |
| Payback do CAC | até 12 meses |
| Churn mensal pós-implantação | < 2% (maduro < 1%) |

**Regra de ROI para o produtor:** se a assinatura custa ~R$ 900/mês (fazenda direta), ele precisa
enxergar ganho ou perda evitada de **R$ 2.000–3.000/mês** para a compra ser confortável — algo
plausível dado o impacto esperado (ver §15). No canal B2B2F (~R$ 60/produtor), o limiar de ROI é
muito menor e o laticínio absorve o custo como proteção de margem.

---

## 11. Go-to-market

**Beachhead — Goiás (Sul Goiano: Rio Verde, Jataí, Mineiros).** Justificativa: desafio
SENAR/SEBRAE Goiás (acesso e credibilidade local), rede USINA I.A., e **diferencial climático**
(estresse térmico sazonal mais agudo → THI tem maior valor percebido). Goiás é o **5º maior estado
leiteiro** (8,2%), grande o bastante para um SOM relevante.

**Expansão — MG / PR / RS / SC.** Minas Gerais é o maior mercado nacional (27,4%) e o destino
natural de escala após a prova de valor em Goiás. Os 5 estados somam **69%** da produção.

**Fases comerciais:**
1. **Descoberta e pilotos (0–90 dias):** 10–20 entrevistas com produtores, 5–8 com técnicos, 2–3 com laticínios; 5 fazendas piloto; **1 parceiro institucional** (laticínio/cooperativa). Oferta: diagnóstico barato + piloto + relatório de ROI + contrato de conversão pré-acordado.
2. **Conversão e prova econômica (3–6 meses):** 20–40 fazendas ativas, 1–2 laticínios no painel, primeiro estudo de caso com número, retenção > 80%.
3. **Comercialização regional (6–12 meses):** 80–150 fazendas, 3–5 parceiros de canal, playbook, métricas confiáveis de CAC/payback/churn.
4. **Escala (12–24 meses):** 300–600 fazendas, 5–10 clientes B2B2F, integrações com laboratório/coleta/ERP, modelos preditivos treinados com dados próprios.

**Canais:** laticínios e cooperativas regionais; consultores de qualidade; veterinários e
nutricionistas; distribuidores agropecuários; programas SEBRAE/SENAR/EMATER; feiras de pecuária
leiteira. **Adoção na ponta:** WhatsApp (zero atrito) + QR Code de demo.

**Mensagem comercial:** evitar *"plataforma de IA para revolucionar o leite"*. Usar *"Descubra
onde sua fazenda está perdendo leite e dinheiro"*, *"Alerta antes da perda virar penalidade"*,
*"Para laticínios: fornecedores com risco visível antes da coleta"*.

---

## 12. Projeções financeiras (dois cenários)

### 12.1 Cenário base — conservador, Goiás-first, B2B2F dominante
Unidade principal: **produtor monitorado** (~R$ 60/mês) + licenças de laticínio.

| Ano | Laticínios | Produtores | ARR (R$) | Marco |
|---|---|---|---|---|
| Ano 1 (26–27) | 1–2 | ~250 | ~R$ 200 mil | Piloto pago + 1º contrato |
| Ano 2 (27–28) | ~7 | ~1.500 | ~R$ 1,1 mi | Prova de valor + expansão GO |
| Ano 3 (28–29) | ~20 | ~4.300 | **~R$ 3,2 mi** | SOM atingido; entrada MG/Sul |

### 12.2 Cenário upside — nacional, pós-captação (depende de rodada seed)
Unidade: mix de fazendas diretas (ARPA alto) + B2B2F. **Requer capital** (§13) e execução forte
de canal. Reproduz a curva agressiva do diagnóstico externo, apresentada como **teto**, não base:

| Ano | Fazendas/produtores ativos | ARPA médio/mês | Receita (R$ mil) | EBITDA (R$ mil) |
|---|---|---|---|---|
| Ano 1 | 80 | 750 | 480 | −1.536 |
| Ano 2 | 300 | 950 | 2.616 | −1.378 |
| Ano 3 | 900 | 1.100 | 9.120 | +702 |
| Ano 4 | 2.200 | 1.250 | 25.750 | +8.283 |
| Ano 5 | 5.000 | 1.400 | 65.480 | +27.800 |

> Os dois cenários são **ilustrativos** e serão calibrados com os dados do piloto (conversão,
> churn, mix de planos, produtores por laticínio, custo de hardware/suporte). O upside só se
> materializa com canal B2B2F maduro e capital; a venda direta pura torna a curva mais lenta e cara.

---

## 13. Necessidade de capital (12–18 meses)

| Uso | Valor estimado |
|---|---|
| Produto e engenharia | R$ 900 mil – R$ 1,4 mi |
| Hardware piloto / estoque inicial | R$ 500 mil – R$ 1,0 mi |
| Operação de campo e suporte | R$ 400 mil – R$ 800 mil |
| Comercial e marketing | R$ 300 mil – R$ 700 mil |
| Validação técnica / regulatória | R$ 150 mil – R$ 400 mil |
| Capital de giro / reserva | R$ 300 mil – R$ 600 mil |
| **Total** | **R$ 2,55 mi – R$ 4,9 mi** |

> Para o **cenário base (Goiás-first)**, a operação pode ser bootstrapped/seed-light, com a maior
> parte deste capital atrelada ao **cenário upside** (escala nacional + estoque de hardware).

---

## 14. Roadmap de produto

| Fase | Status | Período | Entrega principal |
|---|---|---|---|
| Fase 1 — MVP | ✅ Concluído | Dez 25 – Abr 26 | Produto demonstrável ao vivo |
| Fase 3 — Score de Risco | ✅ Concluído | Jun 2026 | Score VIA LEITE + Radar |
| Fase 3.5 — Perfil do Produtor | 🔬 Protótipo validado | Jun 2026 | Consistente/Oscilante/Desafiador |
| Fase 2 — Piloto real | 🔄 Planejado | Jul – Set 2026 | Validação com dados reais de laticínio |
| Fase 4 — IoT/Edge | ⬜ Futuro | 2027 | Telemetria em tempo real (MQTT) + sensores |

**Backlog prioritário:** bot WhatsApp (alertas + lançamentos); canal de comunicação
produtor↔cooperativa; UX trivial para baixo letramento digital; QR de demo; identidade visual.
**Princípios de IA:** começar com regras/thresholds + detecção de anomalia por histórico;
explicabilidade obrigatória ("por quê" e "o que fazer"); modelos universais só com dados reais.

---

## 15. Impacto, operação e ROI

**Impacto esperado** (benchmarks Embrapa, MAPA IN 77/2018, FAO):

| Indicador | Melhora média |
|---|---|
| Redução de descarte | 50–60% |
| Melhora de CCS | 25–35% |
| Melhora de CBT | 35–45% |
| Ganho de receita (médio produtor) | R$ 800–1.500/mês |
| CO₂ evitado (cooperativa 50 prod.) | 180+ t/ano |

**Implantação:** diagnóstico → cadastro/importação → instalação do sensor de tanque/gateway →
treinamento → configuração de alertas → revisão em 15 dias → **relatório de ROI em 60–90 dias**.
**Suporte:** N1 WhatsApp/chat; N2 técnico de campo/parceiro; N3 engenharia. SLA de falha crítica
de tanque ≤ 4 h comerciais.

---

## 16. Regulação, riscos jurídicos e compliance

- Qualidade do leite cru refrigerado e procedimentos de coleta/transporte (IN 77/IN 76).
- **LGPD** para dados de produtores e usuários; propriedade e uso de dados produtivos.
- **Posicionar alertas como "indicadores de risco" e "recomendações operacionais"** — o sistema
  apoia a decisão e **não substitui diagnóstico veterinário** (validação clínica fica com a
  veterinária da equipe e o profissional do cliente).
- Se houver sensor com finalidade analítica/diagnóstica do leite: avaliar certificação,
  calibração e responsabilidade técnica.
- **Entregáveis:** termo de uso, política de privacidade e acordo de compartilhamento de dados
  com laticínios/cooperativas.

---

## 17. Riscos e mitigações

| Risco | Impacto | Mitigação |
|---|---|---|
| Virar hardware caro antes de provar venda | Alto | Software-first; sensores simples e parcerias; validar ROI primeiro |
| Produtor não registrar dados | Alto | UX por WhatsApp, automação máxima, poucos campos obrigatórios |
| Conectividade rural ruim | Alto | Gateway offline-first, sincronização posterior, alertas locais |
| CAC alto na venda direta | Alto | Priorizar laticínios/cooperativas e consultores como canal |
| Alertas com falsos positivos | Alto | Começar com regras simples, calibrar por fazenda, medir precisão |
| Promessa sanitária excessiva | Médio/alto | Apoio à decisão, validação com veterinária; sem diagnóstico automático |
| Base sintética / falta de prova de ROI | Alto | Pipeline de dados reais pronto; todo piloto com baseline e relatório financeiro; backtest ≥ 70% de acerto com 7+ dias |
| Concorrente global em grandes fazendas | Médio | Foco em mid-market brasileiro, integração e custo acessível |
| Dependência de fonte climática (INMET) | Médio | Arquitetura IoT-ready para sensores climáticos locais (Fase 4) |

---

## 18. Equipe

**USINA I.A.** — estúdio de tecnologia e IA para PMEs, setor público e agronegócio (Goiânia, GO).

| Membro | Papel | Desde |
|---|---|---|
| **Fagner Pinho** | Negócio / Produto (CEO/comercial agro) | Fundação |
| **Matheus Iverson** | Dados / Modelagem preditiva | Fundação |
| **Daianne Valéria** | Produto / UX | Fundação |
| **Maria Vitória** | **Veterinária** — validação sanitária, calibração de alertas, compliance técnico | **27/06/2026** |
| **Diego Santana** | **Engenheiro de Software** — arquitetura, backend/API, IoT-ready | **27/06/2026** |

> A entrada de **Maria Vitória (veterinária)** e **Diego Santana (engenheiro de software)** em
> 27/06/2026 fortalece a equipe exatamente nos dois pontos que o diagnóstico de mercado apontou
> como críticos: **rigor sanitário/regulatório** (não prometer diagnóstico, validar alertas com
> respaldo veterinário) e **execução técnica/IoT** (robustez de arquitetura, integrações e
> prontidão para a fase de sensores). A equipe agora cobre negócio, dados, produto, veterinária e
> engenharia.

---

## 19. Critérios de sucesso dos pilotos

Um piloto é bem-sucedido se atingir **≥ 4 de 7** critérios:
1. Produtor usa o sistema semanalmente sem cobrança constante.
2. ≥ 80% dos dados críticos registrados/coletados automaticamente.
3. ≥ 3 alertas acionáveis relevantes em 90 dias.
4. Evidência de perda evitada ou melhoria de qualidade.
5. Produtor aceita pagar assinatura após o piloto.
6. Técnico/laticínio considera os relatórios úteis.
7. Custo de suporte por fazenda dentro do esperado.

**Critério-âncora (técnico):** o Score VIA LEITE deve identificar ≥ 70% dos eventos de
não-conformidade com **7+ dias de antecedência** no backtest com dados reais.

---

## 20. Tese de investimento e o pedido (ask)

A tese é atrativa porque há **mercado grande e fragmentado** (R$ 87,5 bi/ano), **dor econômica
recorrente**, **canal escalável via laticínios** (B2B2F), **receita recorrente** e **dados
proprietários** que se acumulam — com expansão futura para crédito, seguro, insumos e programas de
qualidade. O ponto de prova para investidores **não é "tem IA"** — é *"produtores e laticínios
pagam porque economizam dinheiro ou protegem receita"*.

> **Ask:** o primeiro **laticínio/cooperativa parceiro no Sul Goiano** para um **piloto pago de
> 30–90 dias com dados reais** — com baseline, relatório de ROI e contrato de conversão
> pré-acordado. O produto está **no ar e demonstrável ao vivo**:
> https://via-leite-sense.streamlit.app

---

## 21. Fontes

- **IBGE/SIDRA — Produção e valor da produção de leite no Brasil, 2024** (verificado na fonte):
  https://apisidra.ibge.gov.br/values/t/74/n1/all/v/106,215/p/2024/c80/2682?formato=json
- **IBGE/SIDRA — Produção de leite por UF, 2024** (verificado):
  https://apisidra.ibge.gov.br/values/t/74/n3/all/v/106/p/2024/c80/2682?formato=json
- **IBGE/SIDRA — Efetivo dos rebanhos, 2024:**
  https://apisidra.ibge.gov.br/values/t/3939/n1/all/v/all/p/2024/c79/all?formato=json
- **ArXiv — The Role of Artificial Intelligence in the Dairy Industry:** https://arxiv.org/abs/2406.12770
- Embrapa Gado de Leite; MAPA IN 77/2018; MilkPoint (Gonçalves, 2025); FAO (2010).

## 22. Lacunas a validar

- Preços regionais do leite ao produtor em 2026 (Cepea/contratos locais).
- Número de propriedades leiteiras por estado e faixa de produção no recorte-alvo.
- Custos reais de hardware homologável no Brasil.
- Disposição a pagar por segmento (testar em piloto pago).
- Requisitos regulatórios de qualquer sensor que meça qualidade/composição do leite.
- Parceiros de piloto e cartas de intenção (LOI).

---

*VIA LEITE SENSE — Plano de Negócio v2.0 · USINA I.A. © 2026*
*Equipe: Fagner Pinho · Matheus Iverson · Daianne Valéria · Maria Vitória · Diego Santana*
