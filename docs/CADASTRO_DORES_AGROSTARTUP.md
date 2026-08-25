# Cadastro de Dores — VIA LEITE SENSE

**Setor:** Pecuária Leiteira · **Data:** 12 de agosto de 2026 · **Empresa:** USINA I.A.

Complementa as três dores já cadastradas (Volatilidade dos preços do leite · Impacto do Custo
Brasil na pecuária · Gestão produtiva e financeira para sustentabilidade).

**Regra de honestidade aplicada.** Cada cadastro declara o que a plataforma faz hoje, o que está
projetado e o que ela **não** faz. Nenhuma dor foi cadastrada por proximidade temática: onde o
produto só alcança uma parcela da dor, a parcela está nomeada e a aderência foi rebaixada.

---

## Bloco comum — evidência verificada em produção (12/08/2026)

Todos os números abaixo foram lidos da API de produção no dia do cadastro
(`https://via-leite-sense.vercel.app` · API FastAPI na Railway · rotas autenticadas por
`X-API-Key`, exceto `/health`).

| Fonte | Valor verificado |
|---|---|
| `/training-base/summary` | 54.780 registros · 56 colunas · 01/01/2021 a 31/12/2025 · 30 fornecedores · 4 laticínios |
| `/model/metrics` | XGBRegressor · alvo `target_media_coletada_7d` · horizonte 7 dias · teste: **R² 0,99437 · MAPE 3,58% · MAE 24,17 L** · validação: R² 0,99483 · MAPE 3,36% · split 32.010 / 10.980 / 10.920 |
| `/portfolio` | 30 fornecedores · 21.687,82 L/dia monitorados · 6.361,51 L/dia em risco · score médio 44,6 · 1 crítico · 8 em atenção · descarte 2,00% |
| `/quality-summary` | CCS média 384,08 mil cél/mL · CBT média 141,93 mil UFC/mL · 6 fornecedores em qualidade crítica · 139,01 L de descarte atacável |
| `/impact` | R$ 429.401,90 de valor mensal monitorado |
| `/risk-distribution` | Alto 1 (3,3%) · Médio 8 (26,7%) · Baixo 21 (70,0%) |
| `score_risco.py` | Score VIA LEITE 0–100 · 7 dimensões ponderadas (25/20/15/15/10/10/5) · classes 0–25 · 26–50 · 51–75 · 76–100 · ancorado na IN 77/2018 |
| `perfil/classificador_perfil.py` | Perfil estrutural do produtor: Consistente · Oscilante · Desafiador |
| Pipeline de dados reais | `validar_pacote_dados_reais.py` · `importar_pacote_dados_reais.py` · `guarda_ingestao.py` · `executar_piloto_real.py` |
| Arquitetura | Multi-tenant · IoT-ready (MQTT) · ingestão climática INMET |

> **Delimitação obrigatória, válida para todos os cadastros.** A base de 54.780 registros é
> **sintética**, gerada para validar arquitetura, treinar o modelo e demonstrar o produto — 30
> fornecedores e 4 laticínios simulados sobre séries climáticas reais do INMET. A calibração com
> dados de fazenda reais ocorre na Fase 2 (piloto). Toda meta quantificada marcada como
> *"a validar em piloto"* segue essa regra. Este princípio — não apresentar dado simulado como
> real — é norma interna do projeto, não concessão.

---

## 1. Eficiência operacional na produção leiteira

**Score** 56,96 · **Aderência: Alta** · **Status:** Validada

**Justificativa.** Esta é a dor sobre a qual a plataforma foi construída, e é onde a aderência é
mais direta. A ineficiência operacional na pecuária leiteira não decorre principalmente de falta
de esforço, e sim de **falta de foco**: o produtor e o técnico do laticínio distribuem atenção de
forma homogênea por uma carteira heterogênea, porque não têm como saber onde o problema está se
formando. O Via Leite Sense ataca exatamente esse ponto em quatro frentes:

1. **Priorização substituindo varredura.** O Score VIA LEITE ordena a carteira por risco e
   prioridade de ação. Numa carteira de 30 fornecedores, a plataforma aponta hoje 1 crítico e 8 em
   atenção — ou seja, 70% da base pode seguir em monitoramento padrão enquanto o esforço técnico
   se concentra em 30%. Eficiência operacional, aqui, é deixar de gastar hora técnica onde não há
   problema.
2. **Antecipação substituindo reação.** A previsão de captação em horizonte de 7 dias transforma
   a rotina de conferir o passado em planejar o próximo ciclo — rota, coleta, capacidade de tanque
   e escala de trabalho passam a ser dimensionadas sobre volume esperado, não sobre volume
   histórico.
3. **Perda evitável mensurada, não estimada.** O descarte deixa de ser um número de fim de mês e
   passa a ter causa, fornecedor e valor associados.
4. **Ciclo fechado de ação.** A plataforma registra plano de ação, responsável, meta e resultado, e
   mede efetividade — a eficiência vira série histórica auditável, não percepção.

**Evidência.** Além do bloco comum: `/risk-radar` com ranking por produtor, rota ou laticínio,
score médio, distribuição por classe e horizontes de 7/15/30 dias; `/portfolio` com 21.687,82 L/dia
monitorados e 6.361,51 L/dia classificados em risco; `/risk-distribution` com a carteira segmentada
(1 alto · 8 médio · 21 baixo); `/action-plans` e `/action-plans/effectiveness`, com meta e resultado
em litros e em reais por plano, tipo, responsável e fornecedor — instrumentação implementada e
ainda sem execução registrada, por depender do piloto; `/management-events` para lançamentos
gerenciais; `/model/feature-importance` mostrando que a previsão se apoia majoritariamente em
médias móveis de coleta (7 dias: 55,1%; 30 dias: 20,0%; 3 dias: 14,9%), o que torna o resultado
explicável para quem opera.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Concentrar a assistência técnica nos ~30% da carteira que respondem pela maior parte do risco,
  mantendo os 70% restantes em monitoramento automático.
- Prever a captação com erro médio inferior a 4% (MAPE de 3,58% em teste), permitindo dimensionar
  rota e coleta sobre volume esperado.
- Reduzir em 50–60% o descarte evitável (benchmark Embrapa), sobre uma base atual de 2,00% de
  descarte e 139,01 L classificados como atacáveis.
- Registrar 100% dos planos de ação com meta e resultado mensuráveis, criando série histórica de
  efetividade por tipo de intervenção.

**Limite reconhecido.** A plataforma não opera equipamento, não substitui rotina de ordenha e não
integra automaticamente com todos os sistemas de sala de ordenha do mercado. Ela indica onde agir e
mede o resultado da ação; a execução permanece humana.

---

## 2. Qualidade do leite e acesso a mercados

**Score** 33,28 · **Aderência: Alta** · **Status:** Validada

**Justificativa.** O modelo brasileiro de controle de qualidade do leite é estruturalmente
retrospectivo: a análise de CCS e CBT é laboratorial e periódica, e o resultado chega quando o
leite já foi coletado, processado e pago. O produtor descobre que perdeu a bonificação depois de
tê-la perdido, e o laticínio descobre a não-conformidade depois de tê-la recebido no tanque. A
consequência não é apenas financeira — é de **acesso a mercado**: cadeias premium, exportação e
linhas de maior valor agregado exigem consistência comprovada, e consistência não se demonstra com
laudo isolado, demonstra-se com série histórica.

A plataforma atua sobre três camadas dessa dor:

1. **Acompanhamento contínuo dos indicadores que definem a classificação.** CCS e CBT são
   monitorados de forma corrida e ancorados nos limites da IN 77/2018, e não apenas conferidos
   quando o laudo chega. Na carteira monitorada, a média atual é de 384,08 mil cél/mL de CCS e
   141,93 mil UFC/mL de CBT, com 6 fornecedores identificados em qualidade crítica.
2. **Cadeia fria como variável de qualidade, não de logística.** A temperatura do tanque entra no
   score como dimensão própria, porque falha de resfriamento degrada CBT antes de qualquer outra
   coisa aparecer — é o ponto de perda mais rápido e mais evitável da cadeia.
3. **Histórico auditável como credencial comercial.** Cinco anos de série estruturada por
   fornecedor é o insumo que permite a um laticínio comprovar consistência de fornecimento para o
   comprador final. É esse documento que abre linha premium, não o laudo do mês.

**Evidência.** Além do bloco comum: `/quality-summary` com CCS, CBT, percentual de descarte,
descarte atacável em litros e contagem de fornecedores em qualidade crítica; dimensões dedicadas de
CCS (peso 15), CBT (peso 15), qualidade (peso 20) e temperatura de tanque (peso 10) no
`score_risco.py`, com limiares ancorados na IN 77/2018; `perfil/classificador_perfil.py` com limiar
de severidade de CCS em 600 mil cél/mL para separar perfil Desafiador; `/supplier-events/{id}` para
rastreabilidade de ocorrências por fornecedor; `relatorio_pdf.py` para emissão de relatório por
fornecedor; módulo Via Leite Edge com índice de conservação (média 84,0) e score de qualidade
premium por tanque — este último sobre telemetria **simulada**, com disclaimer explícito na própria
resposta da API.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Melhora de 25–35% em CCS e de 35–45% em CBT (benchmarks Embrapa/MAPA) sobre a linha de base
  levantada no início do piloto.
- Antecipar em 7 ou mais dias ao menos 70% dos eventos de não-conformidade — critério-âncora
  técnico do projeto, a ser medido em backtest com dados reais.
- Preservar integralmente a bonificação por qualidade dos fornecedores monitorados, faixa de
  R$ 0,08 a R$ 0,15 por litro conforme contrato.
- Entregar a cada fornecedor série histórica auditável de qualidade utilizável como credencial
  comercial em negociação de contrato e em acesso a linhas premium.

**Limite reconhecido.** A plataforma não realiza análise laboratorial nem substitui o laudo
oficial: ela consome o resultado do laboratório, cruza com clima e operação e antecipa tendência. A
classificação oficial do leite permanece com o laboratório credenciado.

---

## 3. Cansaço por gestão, segurança e comercialização

**Score** 56,96 · **Aderência: Média** · **Status:** Validada

**Justificativa.** A dor descreve três fontes distintas de desgaste, e a honestidade exige separá-las:
a plataforma atua sobre **uma**, tangencia a segunda e não alcança a terceira.

1. **Gestão — atuação direta.** O desgaste de gestão na pecuária leiteira vem menos do volume de
   decisões e mais da **qualidade da informação disponível para decidir**. O produtor administra
   caderno, planilha, laudo em papel e memória, e sustenta cognitivamente um estado que deveria
   estar registrado. A plataforma transfere essa carga para o sistema: consolida produção,
   qualidade, clima e ocorrências em um painel único, entrega a decisão pronta e ordenada por
   prioridade, e converte o indicador técnico em valor financeiro. Decidir com uma lista de
   prioridade custa menos que decidir com uma pilha de dados brutos.
2. **Comercialização — atuação parcial.** A plataforma não vende leite nem negocia contrato, mas
   remove uma das causas do desgaste comercial: negociar sem dado. Cinco anos de série auditável de
   volume e qualidade por fornecedor mudam a posição do produtor na conversa com o laticínio.
3. **Segurança — sem atuação.** Segurança do trabalho na fazenda não é endereçada pelo produto.

**Evidência.** Além do bloco comum: painel único consolidando produção, qualidade, clima e
ocorrências (`/portfolio`, `/quality-summary`, `/risk-radar`, `/management-events`); ranking de
prioridade que substitui a decisão aberta por decisão ordenada; conversão do risco técnico em valor
financeiro em `/impact` (R$ 429.401,90/mês monitorados); `/action-plans` com responsável e meta
definidos, o que distribui a carga em vez de concentrá-la no produtor; relatório em PDF por
fornecedor via `relatorio_pdf.py`; entrega prevista por WhatsApp, canal já usado pelo produtor, no
backlog prioritário.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Substituir o acompanhamento manual de 30 fornecedores por uma lista diária de prioridade com 1 a
  9 nomes — redução direta do número de decisões que exigem atenção do gestor.
- Consolidar em uma única fonte os registros hoje dispersos entre caderno, planilha e laudo.
- Reduzir o tempo entre o evento e o conhecimento do evento, que é o que gera retrabalho e decisão
  sob pressão.
- Entregar histórico auditável para negociação comercial, reduzindo a assimetria de informação na
  relação produtor–laticínio.

**Limite reconhecido.** Aderência classificada como Média por precisão: a plataforma reduz a carga
**de gestão** e apoia a **comercialização**; não atua sobre segurança do trabalho e não realiza
intermediação comercial. O cansaço físico do trabalho de campo não é endereçado por software.

---

## 4. Escassez de mão de obra qualificada

**Score** 96,00 · **Aderência: Média** · **Status:** Validada

**Justificativa.** É a dor de maior score do setor e exige a delimitação mais rigorosa do cadastro:
**o Via Leite Sense não forma nem repõe mão de obra**. Qualquer alegação nesse sentido seria falsa.
O que a plataforma faz é atuar sobre o mecanismo pelo qual a escassez causa dano.

A escassez de mão de obra qualificada machuca a pecuária leiteira por uma razão específica: o
conhecimento que detecta o problema cedo — o olho treinado que percebe a queda de produção antes
dela aparecer no tanque, ou a mudança de comportamento que antecede a mastite — é justamente o
conhecimento escasso. Onde falta gente qualificada, o problema só é percebido quando já é grande.

A plataforma opera como **camada de conhecimento embarcado**:

1. **Codifica o julgamento técnico em regra explícita.** As sete dimensões do score formalizam o
   que um técnico experiente avaliaria — e a avaliação passa a rodar todos os dias, sobre todos os
   fornecedores, independentemente de haver alguém disponível para fazê-la.
2. **Torna a equipe existente mais produtiva.** O ranking de prioridade permite que o mesmo técnico
   cubra uma carteira maior sem perda de qualidade, porque ele deixa de visitar às cegas.
3. **Reduz a exigência de qualificação na ponta.** O alerta explica o porquê e indica o que fazer.
   Executar uma instrução clara exige menos qualificação do que diagnosticar do zero.
4. **Retém conhecimento na saída do funcionário.** Histórico, plano de ação e efetividade ficam no
   sistema. A rotatividade deixa de zerar a memória operacional da propriedade.

**Evidência.** Além do bloco comum: sete dimensões de risco formalizadas e ponderadas em
`score_risco.py`, com limiares ancorados na IN 77/2018 — julgamento técnico convertido em regra
auditável; `/risk-radar` com ranking de prioridade de ação por produtor, rota e laticínio;
`perfil/classificador_perfil.py` classificando o produtor em Consistente, Oscilante ou Desafiador,
que é a tradução do "que tipo de caso é este" em recomendação de manejo; explicabilidade verificável
em `/model/feature-importance`, com as três médias móveis de coleta respondendo por 90% da decisão
do modelo — o sistema mostra o porquê, não apenas o resultado; `/action-plans` retendo responsável,
meta e resultado; monitoramento automático de 30 fornecedores e 21.687,82 L/dia sem intervenção
humana contínua.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Ampliar a carteira coberta por técnico sem ampliar a equipe, pela substituição de visita
  programada por visita dirigida por risco.
- Garantir avaliação diária de 100% dos fornecedores monitorados, patamar inalcançável por
  inspeção humana em carteira dispersa.
- Entregar todo alerta com causa e ação recomendada, reduzindo o nível de qualificação exigido de
  quem executa.
- Preservar o histórico operacional independentemente da rotatividade de pessoal.

**Limite reconhecido.** A plataforma não forma, não contrata e não substitui mão de obra. Atua
sobre o **efeito** da escassez — a perda por detecção tardia — e não sobre a escassez em si.
Aderência Média por essa razão, apesar do score do setor.

---

## 5. Estresse por ritmo intenso e falta de mão de obra

**Score** 80,00 · **Aderência: Média** · **Status:** Validada

**Justificativa.** Vale a mesma delimitação da dor anterior: a plataforma não reduz jornada nem
repõe pessoal. Atua sobre um componente específico e documentado do estresse na atividade leiteira
— **a carga de vigilância permanente**.

Boa parte do desgaste psicológico do produtor de leite não vem do trabalho executado, e sim do
trabalho de *vigiar*: a preocupação contínua com o que pode estar acontecendo e ainda não foi
percebido. Tanque que pode ter falhado, vaca que pode estar iniciando mastite, produção que pode
estar caindo sem causa aparente. É uma carga que não termina no fim do expediente, e o produtor a
carrega justamente porque **não existe sistema vigiando em seu lugar**.

A atuação se dá em três pontos:

1. **Transferência da vigilância para o sistema.** O monitoramento contínuo remove a necessidade de
   conferência preventiva constante — o produtor é chamado quando há motivo.
2. **Redução da operação em modo emergência.** O trabalho sob pressão é mais desgastante que o
   trabalho planejado, e a antecipação de 7 a 30 dias converte urgência em rotina programável.
3. **Diluição da responsabilidade solitária.** No modelo B2B2F, o mesmo alerta chega ao produtor e
   ao laticínio, o que ativa a assistência técnica sem depender de o produtor pedir ajuda.

**Evidência.** Além do bloco comum: monitoramento automático e contínuo de 30 fornecedores e
21.687,82 L/dia; horizontes de antecipação de 7, 15 e 30 dias em `/risk-radar`; classificação da
carteira que dispensa atenção ativa sobre 70% dos fornecedores em situação de baixo risco;
`/api/iot/alerts` e `/api/iot/executive-summary` com alerta de risco térmico e falha de cadeia fria
por tanque — telemetria **simulada** na fase atual, com sensor físico previsto para a Fase 4 (2027);
arquitetura B2B2F em que o alerta é compartilhado com o laticínio, e não apenas emitido ao produtor.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Substituir conferência preventiva de rotina por notificação dirigida, mantendo 70% da carteira
  fora do ciclo de atenção ativa.
- Converter eventos hoje tratados em urgência em ações programadas com 7 a 30 dias de antecedência.
- Reduzir o intervalo entre a falha de resfriamento e o conhecimento da falha, que é a principal
  fonte de perda súbita e de sobressalto na rotina.
- Acionar automaticamente a assistência técnica do laticínio nos casos de risco alto, sem depender
  de iniciativa do produtor.

**Limite reconhecido.** A plataforma não reduz jornada de trabalho, não repõe mão de obra e não
constitui intervenção de saúde ocupacional. Atua sobre a carga de vigilância e sobre a operação em
modo emergência. O alerta automatizado de falha de tanque, que é o componente mais forte desta
alegação, depende de sensor físico previsto para a Fase 4 — na fase atual, a telemetria é simulada.

---

## 6. Gestão e qualificação da mão de obra

**Score** 56,96 · **Aderência: Média** · **Status:** Validada

**Justificativa.** A qualificação de mão de obra na pecuária leiteira esbarra em dois obstáculos
práticos: não se sabe **o que** treinar, e não se sabe **se o treinamento funcionou**. O
treinamento é ofertado por catálogo, aplicado de forma homogênea e avaliado por presença. A
plataforma atua sobre os dois obstáculos, ainda que não ministre capacitação:

1. **Diagnóstico da necessidade de treinamento.** A dimensão de risco predominante em uma
   propriedade indica a lacuna de competência. Falha recorrente de temperatura de tanque aponta
   manejo de cadeia fria; CCS persistentemente elevado aponta higiene de ordenha. O treinamento
   deixa de ser genérico e passa a ser dirigido por evidência.
2. **Instrução operacional no lugar de diagnóstico.** O plano de ação entregue com o alerta funciona
   como protocolo executável: o funcionário recebe o que fazer, não a tarefa de descobrir o que
   está errado. Isso reduz a qualificação exigida na execução enquanto a qualificação estrutural
   não chega.
3. **Medição do efeito da capacitação.** Meta e resultado registrados por plano de ação permitem
   verificar se o indicador melhorou depois da intervenção — avaliação por resultado, não por
   presença.
4. **Priorização do esforço de capacitação.** O ranking indica quais propriedades justificam
   investimento de treinamento primeiro.

**Evidência.** Além do bloco comum: sete dimensões de risco que isolam a natureza do problema
(queda de produção, qualidade, CCS, CBT, temperatura de tanque, bônus, descarte), permitindo mapear
lacuna de competência por propriedade; `perfil/classificador_perfil.py` com classificação estrutural
Consistente/Oscilante/Desafiador, que orienta o tipo de acompanhamento adequado a cada produtor;
`/action-plans` com tipo, responsável, meta em litros e em reais; `/action-plans/effectiveness` com
apuração de efetividade por tipo, responsável e fornecedor — instrumentação implementada, sem
execução registrada até o piloto; `/supplier-events/{id}` para histórico de ocorrências por
fornecedor.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Substituir o treinamento por catálogo por treinamento dirigido pela dimensão de risco
  predominante em cada propriedade.
- Avaliar 100% dos planos de ação por resultado medido em litros e em reais, e não por presença.
- Reduzir a qualificação exigida na execução, entregando protocolo em vez de diagnóstico.
- Construir base de efetividade por tipo de intervenção, permitindo identificar quais capacitações
  produzem retorno mensurável.

**Limite reconhecido.** A plataforma não ministra treinamento, não certifica competência e não
substitui programas de capacitação do SENAR ou de assistência técnica. Ela diagnostica a lacuna,
entrega o protocolo e mede o resultado.

---

## 7. Sanidade do rebanho e produtividade leiteira

**Score** 29,28 · **Aderência: Média** · **Status:** Validada

**Justificativa.** Esta é a dor de maior sensibilidade regulatória do cadastro, e a delimitação
precede o argumento: **o Via Leite Sense não realiza diagnóstico veterinário e não o substitui**.
Esse é um limite de projeto, declarado no plano de negócio e sustentado por decisão técnica com
respaldo da veterinária da equipe, e não uma ressalva de estilo.

Dentro desse limite, a atuação é real e relevante. A CCS é um indicador consagrado de saúde da
glândula mamária, e sua elevação sustentada precede clinicamente a manifestação evidente da
mastite. O que a plataforma faz é **tratar a CCS como sinal de tendência e não como resultado
mensal**: acompanhamento contínuo, comparação com o histórico do próprio produtor e alerta quando a
trajetória se deteriora — antes do laudo seguinte. O papel é o de **triagem que qualifica a agenda
do veterinário**, ampliando o alcance de um profissional escasso e caro. Some-se a isso o
componente de estresse térmico: o THI e as variáveis derivadas entram no modelo e permitem
antecipar quedas de produção de origem ambiental, que são um determinante direto de produtividade e
frequentemente confundidas com problema sanitário.

**Evidência.** Além do bloco comum: dimensões dedicadas de CCS (peso 15) e de qualidade (peso 20)
no `score_risco.py`, com limiares ancorados na IN 77/2018; CCS média de 384,08 mil cél/mL e 6
fornecedores em qualidade crítica identificados em `/quality-summary`; limiar de severidade de CCS
em 600 mil cél/mL em `perfil/classificador_perfil.py`; variáveis climáticas de estresse térmico no
conjunto de treino (`thi`, `thi_3d_avg`, `onda_calor_3d`, `onda_calor_5d`, `anomalia_temp`,
`intensidade_estresse_termico`), a partir de séries reais do INMET; `/supplier-events/{id}` com
histórico de ocorrências por fornecedor, insumo para a consulta veterinária; participação de médica
veterinária na equipe desde 27/06/2026, responsável pela validação sanitária e pela calibração dos
alertas.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Antecipar tendência de elevação de CCS antes do laudo seguinte, encurtando a janela entre o
  início do problema e a intervenção.
- Aumentar o número de propriedades cobertas por veterinário, pela substituição de visita de rotina
  por visita priorizada por risco.
- Separar queda de produção de origem térmica de queda de origem sanitária, evitando intervenção
  desnecessária.
- Entregar ao veterinário histórico estruturado de qualidade e ocorrências no momento da consulta.

**Limite reconhecido.** A plataforma emite **indicadores de risco e recomendações operacionais**.
Não realiza diagnóstico, não prescreve tratamento, não substitui o médico veterinário e não
constitui dispositivo de finalidade diagnóstica. Aderência Média por essa razão.

---

## 8. Sustentabilidade ambiental na pecuária leiteira

**Score** — · **Aderência: Média** · **Status:** Validada

**Justificativa.** A pegada ambiental da pecuária leiteira tem um componente frequentemente
ignorado porque não aparece como emissão: **o leite descartado carrega toda a emissão da sua
produção e não entrega nenhum valor**. Água, alimentação, energia de resfriamento e emissão
entérica já foram integralmente gastos quando o litro é descartado por falha de resfriamento ou
reprovação de qualidade. Evitar descarte é, em termos ambientais, a intervenção de melhor relação
custo-benefício da cadeia, porque não exige mudança de sistema produtivo — exige apenas que a perda
não ocorra.

A plataforma atua nesse ponto por três caminhos:

1. **Redução de perda como redução de emissão.** Cada litro preservado elimina a emissão embarcada
   correspondente, estimada pela FAO em cerca de 2,5 kg de CO₂-eq por litro na América Latina.
2. **Eficiência logística.** A priorização de coleta por risco e por volume evita deslocamento
   desnecessário na captação, componente relevante da pegada da cadeia.
3. **Mensuração auditável, e não declaração.** O produto entrega indicador ambiental calculado
   sobre operação registrada, o que é o que programas de sustentabilidade de laticínio e exigências
   de comprador final efetivamente demandam.

**Evidência.** Além do bloco comum: módulo Antes & Depois (ESG) no produto; `/api/iot/executive-summary`
com score ESG de 72,1, índice de conservação médio de 84,0 e oportunidade de redução de perda de
616,3 litros — sobre telemetria **simulada**, com disclaimer explícito na resposta da API;
`/quality-summary` com 2,00% de descarte e 139,01 L de descarte atacável identificados na carteira;
variáveis de captação e custo logístico no modelo (`custo_logistico_rateado`, `distancia_km_laticinio`,
`percentual_estrada_nao_pavimentada`); memória de cálculo documentada no plano de negócio, com
fator FAO 2010 aplicado sobre litros preservados.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Evitar cerca de 180 toneladas de CO₂-eq por ano em uma cooperativa de 50 produtores, pela via do
  desperdício não ocorrido — cálculo: 50 produtores × ~4 L/dia × 365 dias × 2,5 kg CO₂-eq/L.
- Reduzir em 50–60% o descarte evitável, com efeito ambiental proporcional e imediato.
- Entregar indicador ambiental auditável por fornecedor e por carteira, utilizável em programa de
  sustentabilidade do laticínio e em exigência de comprador final.
- Reduzir deslocamento improdutivo na captação pela priorização de rota por risco e volume.

**Limite reconhecido.** A plataforma não realiza inventário de emissões certificado, não emite
crédito de carbono e não atua sobre as fontes principais de emissão do sistema — fermentação
entérica, manejo de dejetos e uso do solo. Atua sobre a parcela evitável por eficiência.

---

## 9. Organização coletiva dos produtores leiteiros

**Score** 29,28 · **Aderência: Média** · **Status:** Validada

**Justificativa.** A dificuldade de organização coletiva na pecuária leiteira tem uma causa que
antecede a disposição associativa: **falta de linguagem comum**. Produtores de uma mesma
cooperativa medem de formas diferentes, registram em suportes diferentes e não conseguem se
comparar — e sem comparação não há diagnóstico coletivo, não há prioridade compartilhada e não há
base para ação conjunta.

A plataforma foi desenhada em torno da relação coletiva, e não da propriedade isolada:

1. **O modelo de negócio é o coletivo.** A arquitetura B2B2F tem o laticínio ou a cooperativa como
   contratante e a carteira de produtores como unidade de gestão. O produto só faz sentido pleno em
   grupo.
2. **Padronização de medida.** Todos os fornecedores da carteira passam a ser avaliados pelos
   mesmos indicadores, com os mesmos limiares e no mesmo horizonte — condição para benchmarking
   interno legítimo.
3. **Diagnóstico agregado.** O radar agrupa por rota e por laticínio, o que revela problemas
   coletivos — uma rota inteira com falha de cadeia fria é problema de infraestrutura compartilhada,
   não de produtor individual, e a solução é necessariamente coletiva.
4. **Simetria de informação.** Produtor e cooperativa passam a olhar o mesmo dado, o que muda a
   qualidade da relação.

**Evidência.** Além do bloco comum: arquitetura multi-tenant com 30 fornecedores e 4 laticínios na
base; `/risk-radar` com agrupamento por produtor, rota ou laticínio e mapa de calor por rota,
permitindo diagnóstico de problema compartilhado; `/risk-distribution` com a carteira segmentada por
classe de risco; `/portfolio` com visão consolidada da carteira; modelo comercial B2B2F com licença
de cooperativa e assinatura por produtor monitorado; canal de comunicação produtor↔cooperativa e
benchmarking anônimo entre fornecedores no backlog prioritário do produto.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Estabelecer indicador padronizado e comparável para 100% dos fornecedores de uma mesma carteira.
- Identificar problemas de natureza coletiva pelo agrupamento por rota, distinguindo-os de falha
  individual.
- Fornecer à cooperativa base objetiva para priorizar investimento coletivo — resfriador
  comunitário, melhoria de estrada, programa de qualidade dirigido.
- Reduzir a assimetria de informação entre produtor e cooperativa, disponibilizando o mesmo
  indicador a ambos.

**Limite reconhecido.** A plataforma não organiza, não constitui e não administra cooperativa. Ela
fornece a infraestrutura de informação sobre a qual a organização coletiva pode se apoiar. O
benchmarking anônimo entre produtores está no backlog e não é entrega da fase atual.

---

## 10. Escala e estrutura produtiva competitiva

**Score** 39,04 · **Aderência: Média** · **Status:** Validada

**Justificativa.** A competitividade por escala na pecuária leiteira costuma ser lida como questão
de tamanho de rebanho, mas o determinante prático é outro: **capacidade de operar de forma
consistente no tamanho que se tem**. Um produtor que oscila entrega menos valor que um produtor
menor e regular, porque a indústria precifica previsibilidade. E crescer sem informação estruturada
amplia a exposição em vez da margem.

A plataforma atua em três frentes:

1. **Consistência como ativo competitivo.** O eixo de variabilidade do classificador de perfil
   separa o produtor Consistente do Oscilante, e é essa distinção que a indústria remunera.
2. **Diagnóstico de subutilização estrutural.** O modelo carrega capacidade instalada, produção
   esperada e rebanho em lactação, o que permite comparar o realizado com o potencial da estrutura
   existente. Muito ganho de escala está disponível sem investimento — está na diferença entre o
   que a estrutura comporta e o que ela entrega.
3. **Decisão de investimento com base em dado.** Cinco anos de série por fornecedor permitem avaliar
   se a limitação é de estrutura, de manejo ou de sanidade antes de decidir onde aplicar capital.

**Evidência.** Além do bloco comum: variáveis estruturais no modelo — `capacidade_maxima_litros_dia`,
`producao_media_esperada_litros_dia`, `vacas_lactacao`, `capacidade_tanque_litros`,
`nivel_tecnificacao`, `porte_produtor`, `tipo_sistema`; `perfil/classificador_perfil.py` com eixo de
variabilidade separando Consistente de Oscilante; estrutura `Supplier` com indicadores financeiros e
capacidade instalada por fornecedor; `/portfolio` com 21.687,82 L/dia distribuídos entre 30
fornecedores, permitindo comparação de eficiência por porte; base de 54.780 registros com cinco anos
por fornecedor como insumo de decisão de investimento.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Quantificar a diferença entre capacidade instalada e produção realizada por fornecedor,
  identificando ganho de escala disponível sem novo investimento.
- Classificar a carteira por consistência de entrega, atributo diretamente remunerado pela indústria.
- Subsidiar decisão de investimento com cinco anos de série própria, distinguindo limitação
  estrutural de limitação de manejo.
- Sustentar contratos de fornecimento mais longos com base em previsibilidade demonstrada.

**Limite reconhecido.** A plataforma não financia, não dimensiona projeto de engenharia e não
substitui consultoria de estruturação produtiva. Ela mede a distância entre o potencial da estrutura
existente e o resultado obtido.

---

## 11. Instabilidade econômica e endividamento familiar

**Score** 67,20 · **Aderência: Baixa** · **Status:** Validada

**Justificativa.** A aderência é declaradamente baixa e o limite é amplo: **a plataforma não
concede crédito, não renegocia dívida e não presta assessoria financeira**. As causas do
endividamento na pecuária leiteira são majoritariamente macroeconômicas e estruturais — custo de
insumo, taxa de juros, ciclo de preço, ausência de reserva.

Há, porém, dois pontos legítimos de atuação, e ambos são de natureza informacional:

1. **Perda evitável como componente da fragilidade financeira.** Parte do endividamento familiar se
   forma pela erosão contínua da margem por perdas que poderiam não ter ocorrido — descarte,
   penalidade de qualidade, bônus perdido. Não é a causa principal, mas é a única parcela sob
   governança direta do produtor, e é sobre ela que a plataforma atua, com efeito relativo maior
   justamente nos ciclos de preço deprimido.
2. **Histórico auditável como ativo de acesso a crédito.** O produtor de leite normalmente negocia
   crédito sem comprovação estruturada de receita e de qualidade, e paga por essa opacidade. Cinco
   anos de série documentada de volume e de qualidade constituem um ativo negocial — este é o
   caminho de maior potencial da dor, e está no horizonte de evolução do produto, não na entrega
   atual.

**Evidência.** Além do bloco comum: `/impact` com R$ 429.401,90 de valor mensal monitorado e
conversão do risco técnico em valor financeiro; cálculo de impacto econômico por fornecedor no
`score_risco.py`, combinando queda de produção, perda de bônus e penalidade de qualidade;
`/quality-summary` com descarte atacável quantificado em litros; base de 54.780 registros com cinco
anos de série por fornecedor; estrutura `Supplier` com indicadores financeiros e margem estimada por
fornecedor.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Tornar visível e mensurável a perda evitável mensal, hoje diluída no resultado e raramente
  atribuída a causa.
- Proteger a bonificação por qualidade, faixa de R$ 0,08 a R$ 0,15 por litro, cujo peso relativo na
  margem cresce nos ciclos de preço baixo.
- Constituir histórico auditável de volume e qualidade utilizável na negociação de crédito rural.
- Evolução prevista: camada de indicadores financeiros por propriedade e integração com produtos de
  crédito e seguro, ambos fora da entrega atual.

**Limite reconhecido.** A plataforma não concede crédito, não renegocia dívida, não presta
assessoria financeira e não atua sobre os determinantes macroeconômicos do endividamento. Aderência
Baixa, cadastrada apenas pela parcela de perda evitável e pelo valor informacional do histórico.

---

## 12. Sucessão familiar e atratividade da atividade

**Score** 56,96 · **Aderência: Baixa** · **Status:** Validada

**Justificativa.** A aderência é baixa e a razão é honesta: **sucessão familiar é fenômeno
cultural, geracional e patrimonial, e nenhum software o resolve**. Cadastramos a dor por um vínculo
específico e verificável, não por afinidade temática.

O vínculo é o seguinte. Dois fatores frequentemente citados na baixa atratividade da atividade
leiteira para a geração seguinte são o regime de vigilância permanente e a informalidade da gestão —
a atividade é percebida como um trabalho que não desliga e que se administra por memória e caderno.
A digitalização da rotina atua sobre a percepção nos dois pontos: a gestão passa a se parecer com a
de qualquer outro negócio, com indicador, meta e histórico; e a vigilância contínua é transferida
para o sistema. Há ainda um terceiro elemento, mais concreto: a transição sucessória é o momento em
que o conhecimento tácito do titular se perde, e o histórico estruturado é o que permite ao sucessor
assumir sem recomeçar a curva de aprendizado.

**Evidência.** Além do bloco comum: base de 54.780 registros com cinco anos de série contínua por
fornecedor — memória operacional que sobrevive à transição; `/supplier-events/{id}` e
`/management-events` com histórico de ocorrências e decisões gerenciais registradas; `/action-plans`
com efetividade apurada por tipo de intervenção, o que documenta o que funcionou na propriedade;
interface web acessível por navegador e entrega prevista por WhatsApp, no backlog prioritário;
monitoramento automático que reduz a necessidade de conferência presencial constante.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Preservar cinco anos de memória operacional estruturada, transferível ao sucessor sem depender do
  conhecimento tácito do titular.
- Documentar quais intervenções produziram resultado na propriedade, encurtando a curva de
  aprendizado da sucessão.
- Reduzir o regime de vigilância presencial contínua, um dos fatores citados na baixa atratividade
  da atividade.
- Aproximar a gestão da propriedade leiteira do padrão de gestão por indicador praticado em outros
  setores.

**Limite reconhecido.** A plataforma não atua sobre renda, sobre estrutura patrimonial, sobre
partilha, sobre projeto de vida familiar ou sobre qualquer determinante central da decisão
sucessória. Aderência Baixa, cadastrada exclusivamente pela preservação de memória operacional e
pela redução do regime de vigilância.

---

## 13. Manejo nutricional e produção de volumosos

**Score** 42,72 · **Aderência: Baixa** · **Status:** Validada

**Justificativa.** A delimitação é definida por decisão de escopo do produto: **o Via Leite Sense
não formula dieta, não calcula exigência nutricional e não substitui zootecnista ou nutricionista**.
Não resolver nutrição com profundidade é opção declarada de arquitetura, para não diluir o foco em
risco e qualidade.

A atuação existente é indireta e de natureza climática, e é real. A produção de volumoso depende
diretamente de regime hídrico e de temperatura, e o modelo incorpora séries reais do INMET com
variáveis derivadas construídas justamente para capturar esse efeito: precipitação acumulada em 3,
7 e 15 dias, contagem de dias sem chuva, veranico de 10 dias, anomalia de temperatura e um índice
de favorabilidade de pastagem. O resultado prático é a capacidade de antecipar janela de restrição
de forragem e de distinguir queda de produção de origem ambiental de queda de origem sanitária ou
de manejo — que é exatamente a dúvida diagnóstica que faz o produtor intervir na dieta sem
necessidade.

**Evidência.** Além do bloco comum: variáveis climáticas e agronômicas no conjunto de treino —
`indice_favorabilidade_pastagem`, `dry_spell_10d`, `dias_sem_chuva`, `precip_3d`, `precip_7d`,
`precip_15d`, `anomalia_temp`, `interacao_seca_calor`, `sensibilidade_seca`; ingestão climática do
INMET implementada em `ingestao_clima_inmet.py`, sobre séries reais; horizonte de previsão de 7 dias
para média coletada, com MAPE de 3,58% em teste; dimensão de queda de produção com peso 25 no
`score_risco.py`; variáveis de sistema produtivo e tecnificação (`tipo_sistema`,
`nivel_tecnificacao`) na base.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Antecipar janelas de restrição de forragem por veranico e por anomalia térmica, permitindo
  planejamento de suplementação antes da queda de produção.
- Distinguir queda de produção de origem climática de queda de origem sanitária ou de manejo,
  evitando intervenção nutricional desnecessária.
- Fornecer ao nutricionista série histórica de produção correlacionada com clima, insumo hoje
  indisponível na maior parte das propriedades.
- Evolução prevista: sensores climáticos locais na Fase 4, substituindo a estação INMET de
  referência por medição na propriedade.

**Limite reconhecido.** A plataforma não formula dieta, não calcula exigência nutricional, não
dimensiona área de volumoso e não substitui profissional de nutrição animal. Aderência Baixa,
cadastrada pela camada climática que condiciona a produção de volumoso.

---

## 14. Eficiência produtiva e genética na pecuária leiteira

**Score** 46,72 · **Aderência: Baixa** · **Status:** Validada

**Justificativa.** A dor combina dois temas de natureza distinta, e a plataforma alcança apenas um.
**Sobre genética não há atuação alguma**: o produto não avalia mérito genético, não orienta
acasalamento, não trabalha com índice de seleção e não substitui programa de melhoramento.

Sobre eficiência produtiva a atuação é parcial e verificável. O modelo carrega rebanho em lactação
e produção esperada por propriedade, o que permite acompanhar produtividade realizada contra
potencial declarado e detectar desvio antes que ele se consolide. Mais relevante: a plataforma
isola o efeito do estresse térmico sobre a produção, que é um dos determinantes mais subestimados
de produtividade no Centro-Oeste e frequentemente atribuído a limitação genética do rebanho quando
é, na verdade, ambiental. Distinguir uma coisa da outra evita decisão cara e equivocada de
substituição de animais.

**Evidência.** Além do bloco comum: variáveis de rebanho e potencial no modelo — `vacas_lactacao`,
`producao_media_esperada_litros_dia`, `capacidade_maxima_litros_dia`, `raca_predominante`,
`porte_produtor`; variáveis de estresse térmico (`thi`, `thi_3d_avg`, `onda_calor_3d`,
`onda_calor_5d`, `intensidade_estresse_termico`, `sensibilidade_calor`) sobre séries reais do INMET;
dimensão de queda de produção com peso 25 no `score_risco.py`; previsão de média coletada em 7 dias
com R² de 0,99437 e MAPE de 3,58% em teste; `/risk-radar` com 23,6% da base sinalizada em risco de
queda de produção.

**Impacto esperado.** Metas quantificadas (a validar em piloto):

- Acompanhar produtividade realizada contra potencial declarado por propriedade, detectando desvio
  antes da consolidação.
- Quantificar a parcela da queda de produção atribuível a estresse térmico, separando-a de
  limitação genética ou de manejo.
- Antecipar queda de produção com 7 dias e erro médio inferior a 4%, permitindo intervenção antes
  da perda.
- Evitar decisões de descarte ou substituição de animais fundamentadas em diagnóstico incorreto de
  causa.

**Limite reconhecido.** A plataforma não avalia mérito genético, não orienta acasalamento, não
calcula índice de seleção e não substitui programa de melhoramento ou controle leiteiro oficial.
Aderência Baixa, cadastrada exclusivamente pela perna de eficiência produtiva.

---

## Dores deliberadamente não cadastradas

Registradas aqui com a justificativa da exclusão. A ausência é decisão de integridade e deve ser
sustentável se questionada.

| Dor | Score | Por que não cadastramos |
|---|---|---|
| Uso de álcool para estresse no trabalho | 67,20 | Saúde do trabalhador e dependência química. Nenhuma funcionalidade do produto atua sobre a dor. Cadastrar seria oportunismo temático. |
| Importância da qualidade do sono | 52,96 | O único vínculo plausível — o alarme automático de tanque dispensar a conferência noturna — depende de sensor físico previsto apenas para a Fase 4 e não é entrega atual. Alegar melhora de sono a partir de telemetria simulada não se sustenta. |
| Uso de EPI para proteção contra agrotóxicos | 46,72 | Segurança do trabalho e uso de defensivos. Fora do escopo do produto em qualquer horizonte do roadmap. |
| Eficiência reprodutiva na pecuária leiteira | 33,28 | O produto não trabalha com intervalo entre partos, taxa de concepção, detecção de cio ou protocolo reprodutivo. Não resolver reprodução é decisão explícita de escopo. |
| Segurança no trabalho na fazenda | 33,28 | Segurança ocupacional, acidentes e norma regulamentadora. Sem interseção com as funcionalidades existentes. |

---

## Ordem de prioridade recomendada na apresentação

1. **Carro-chefe (prova dura disponível):** Eficiência operacional · Qualidade do leite e acesso a
   mercados · Gestão produtiva e financeira *(já cadastrada)*.
2. **Diferenciação (dores de alto score do setor, com delimitação rigorosa):** Escassez de mão de
   obra qualificada · Estresse por ritmo intenso · Cansaço por gestão.
3. **Contexto e amplitude:** as demais.

A força do conjunto não está no número de dores cadastradas — está em cada cadastro declarar o
próprio limite. Um cadastro com limite explícito resiste à arguição; um cadastro sem limite cai na
primeira pergunta.

---

*VIA LEITE SENSE — Cadastro de Dores · USINA I.A. © 2026*
*Números verificados na API de produção em 12/08/2026.*
