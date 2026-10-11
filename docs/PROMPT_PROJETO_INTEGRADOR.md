# Briefing — Trilha Acadêmica do Via Leite Sense (Projeto Integrador 2026-2)

> Este arquivo é a **instrução de entrada** para o Claude Code. Ele descreve o que
> deve ser elaborado no repositório para sustentar o Projeto Integrador do último
> semestre da Tecnologia em Inteligência Artificial. Não é documento de banca —
> é o briefing que gera os documentos de banca.

---

## 1. Contexto do repositório

Você está no repositório do **VIA LEITE SENSE**, produto da USINA I.A. (radar de risco
produtivo, qualidade e rentabilidade para a cadeia leiteira). O que já existe hoje:

- **Modelo preditivo:** XGBoost tabular em `treino_mvp_avancado.py`, target
  `target_media_coletada_7d`, split temporal (treino < 2024, validação 2024, teste 2025).
  Métricas em `artefatos_teste/metricas_modelo.json`: R² 0,994 / MAE 24,45 L
  (baseline média móvel: MAE 31,54 L).
- **Motor de risco por regras:** `score_risco.py` — score 0–100 com 7 dimensões
  ponderadas, limiares ancorados na IN 77/2018 do MAPA.
- **Classificador de perfil por regras:** `perfil/classificador_perfil.py` — 3 perfis
  (Consistente / Oscilante / Desafiador), fundamentado em IN 76/77 e em Gonçalves (2025).
- **Dados:** gerador sintético (`gerador_leite_sintetico.py`) + ingestão de clima real
  INMET (`ingestao_clima_inmet.py`); pipeline de dados reais em `executar_piloto_real.py`.
- **Produto:** API FastAPI (`backend/app.py`, 30+ endpoints, DuckDB) + SPA em `frontend/`
  publicada na Vercel. Streamlit descomissionado (`via_leite_app_legacy.py`).
- **Módulo IoT simulado:** `via_leite_edge/`.

**Lacunas relevantes para a trilha acadêmica:** não existe rede neural, não existe PLN e
não existe camada generativa/LLM no projeto. Nenhuma dependência de torch, keras,
transformers ou SDK de LLM está declarada em `requirements.txt`.

---

## 2. Equipe e autoria — REGRA OBRIGATÓRIA

A equipe do produto Via Leite Sense tem 5 pessoas, mas **o Projeto Integrador e a Maratona
SENAR Goiás têm composições diferentes**. Isso precisa estar explícito em todo documento
acadêmico que você gerar:

| Pessoa | Projeto Integrador (faculdade) | Maratona SENAR Goiás |
|---|---|---|
| **Fagner Pinho** — negócio/produto | ✅ integrante | ✅ |
| **Daianne Valéria** — produto/UX | ✅ integrante | ✅ |
| **Matheus Iverson** — dados/modelagem | ✅ integrante | ✅ |
| Maria Vitória — veterinária | ❌ **não participa** | ✅ |
| Diego Santana — engenharia de software | ❌ **não participa** | ✅ |

- O Projeto Integrador é entregue por **Fagner, Daianne e Matheus — e somente por eles**.
- **Maria Vitória e Diego Santana atuam exclusivamente na Maratona SENAR Goiás**, não são
  coautores de nenhum entregável acadêmico e não devem aparecer como autores em relatório,
  artigo, apresentação ou ficha de equipe do Projeto Integrador.
- Onde a contribuição deles tocar o produto (validação sanitária, arquitetura/IoT),
  registre como **contribuição externa ao escopo acadêmico**, devidamente creditada como
  tal — nunca como coautoria.
- Todo documento acadêmico deve trazer uma seção **"Equipe e autoria"** com essa distinção
  escrita de forma inequívoca.

---

## 3. Grade do semestre 2026-2 (IA5 — Evento 953633 — Lab. 107)

| Matéria | Professor | Quando |
|---|---|---|
| Redes Neurais Artificiais | Cristiano | Segunda (4 blocos) + Terça 18:30–20:30 · **28/07 a 29/09** |
| Processamento de Linguagem Natural | Raphael | Quarta 18:30–20:30 · **28/07 a 29/09** |
| Inteligência Artificial Generativa | Raphael | Quinta (4 blocos) + Terça 20:45–22:45 · **06/10 a 15/12** |
| Inteligência Artificial | Alexandre Barbosa | Sexta (4 blocos) · semestre inteiro |
| Projeto de Extensão Integrador — IA | Willgnner | Quarta 20:45–22:45 · **06/10 a 15/12** |

Data de referência: **04/08/2026** (semana 2 do semestre). Encerramento: **15/12/2026**.

---

## 4. O que cada matéria deve receber do Via Leite Sense

Use isto como base, mas critique e refine se identificar caminho melhor dentro do repo.

**Inteligência Artificial (Alexandre Barbosa)** — matéria fundacional, é a que já está mais
coberta. Formalizar `score_risco.py` + `perfil/classificador_perfil.py` como **sistema
baseado em conhecimento** (representação, regras, decisão sob incerteza) e comparar com a
abordagem aprendida. Gancho opcional de busca/otimização: priorização e sequenciamento de
rotas de coleta usando `dim_rota` (distância, custo logístico, dificuldade). Seção de
ética e LGPD sobre dados de produtor identificável.

**Redes Neurais Artificiais (Cristiano)** — matéria de maior carga horária. Entrega:
desafiar o XGBoost com rede neural no **mesmo target e mesmo split temporal**. Trilha
sugerida: MLP tabular → LSTM/GRU sobre a série por produtor → opcionalmente N-BEATS ou TFT.
O pipeline de features (lags 1–28, médias móveis 3/7/14/30, THI, interações) já existe em
`treino_mvp_avancado.py` e deve ser reaproveitado para garantir comparação justa.

**Processamento de Linguagem Natural (Raphael)** — construção do zero; casa com o backlog
de canal produtor↔cooperativa. Entrega: classificação de intenção + NER sobre mensagens
livres do produtor ("mandei 320 litros hoje, a vaca 12 tá com mastite") convertidas em
lançamento estruturado no banco. Priorizar pipeline clássico (TF-IDF/embeddings, spaCy,
BERTimbau) — a matéria quer o pipeline, não uma chamada de API. Entrega secundária: busca
semântica sobre IN 76/77, Embrapa e MilkPoint.

**Inteligência Artificial Generativa (Raphael)** — camada LLM. Candidatos em ordem de
força: (a) RAG sobre normativas gerando o texto do plano de ação a partir do score,
aproveitando os endpoints `/action-plans` existentes; (b) geração sintética com modelo
generativo (CTGAN/TimeGAN) substituindo o gerador por regras — ataca de frente a
fragilidade da base sintética; (c) agente que redige o resumo executivo semanal.
Incluir avaliação: alucinação, aderência à fonte, guardrails.

**Projeto de Extensão Integrador (Willgnner)** — extensão exige **comunidade externa real e
documentada**, não código. Entrega: piloto com cooperativa/produtores em Goiás, oficina de
capacitação, QR de demo em campo, relatório com nº de beneficiários e evidências.
⚠️ A matéria começa em 06/10, mas articular cooperativa leva meses — o cronograma precisa
colocar a prospecção começando em **agosto**, não em outubro.

---

## 5. Restrições e princípios inegociáveis

1. **Honestidade metodológica sobre a base.** A base é majoritariamente sintética, gerada
   pelo próprio `gerador_leite_sintetico.py` — o modelo aprende, em parte, o gerador. Todo
   documento acadêmico deve declarar isso e **reportar o ganho sobre o baseline**
   (MAE 24,45 vs 31,54 ≈ 22% melhor) como métrica principal, nunca o R² 0,994 absoluto.
2. **Separação entre documento acadêmico e documento externo.** Relatório de banca leva
   seção de limitações e autocrítica; `docs/PITCH.md`, `docs/PLANO_DE_NEGOCIO.md` e
   qualquer material para SENAR/SEBRAE/investidor **não levam**. Não deixe uma coisa
   vazar na outra.
3. **Não apresentar dado simulado como real** — princípio já vigente em `docs/PRODUTO.md`.
4. **Critério de admissão — nenhuma adição entra "porque a matéria pediu".** O Via Leite
   Sense é produto em produção, não sandbox acadêmico. Toda implementação proposta precisa
   passar simultaneamente pelos dois testes abaixo, e o documento da matéria deve registrar
   a resposta de cada um antes de a tarefa virar código:
   - **Não-prejuízo:** não quebra, não regride e não degrada o que já funciona
     (`backend/app.py`, `frontend/`, `score_risco.py`, `treino_mvp_avancado.py`, pipeline de
     dados). Nada de refatorar o que já roda para acomodar experimento acadêmico. A adição
     deve ser isolável e reversível — módulo novo, flag ou branch — de modo que removê-la
     devolva o produto ao estado anterior sem cicatriz.
   - **Agregação de valor:** a adição melhora o produto final de forma defensável — ganho
     de acurácia sobre o baseline atual, nova capacidade de produto com demanda real do
     cliente, ou redução de custo/atrito operacional. "Cumprir ementa" não é valor.
   Se uma entrega da matéria **não** passar nos dois testes, ela **não vai para o produto**:
   fica como experimento fora do caminho de produção (notebook, `experimentos/`, branch
   descartável) e é reportada honestamente no artigo como hipótese testada e rejeitada —
   resultado negativo documentado também é contribuição científica.
5. **Um artigo científico está entre os entregáveis.** Isso eleva a régua de tudo o que for
   feito: experimento precisa ser **reprodutível** (semente fixa, split declarado, dados e
   versões registrados), comparação precisa ser **justa** (mesmo target, mesmo split, mesmo
   conjunto de features), e resultado precisa vir com **baseline e limitações**. Planeje
   cada adição já pensando em qual seção do artigo ela alimenta — método, resultado ou
   ameaça à validade. Autoria do artigo: **somente Fagner, Daianne e Matheus** (ver seção 2).
6. **Rastreabilidade de autoria.** O Via Leite Sense é anterior ao semestre e é produto
   comercial da USINA I.A. O incremento acadêmico precisa ser auditável: branch dedicada,
   convenção de commit e um índice do que foi produzido entre 28/07 e 15/12/2026.

---

## 6. Entregáveis desta rodada

Produza, nesta ordem:

1. **`docs/PROJETO_INTEGRADOR.md`** — documento mestre: contexto, equipe e autoria (com a
   distinção Projeto Integrador × Maratona SENAR bem explícita), mapa matéria→entrega,
   cronograma dos dois blocos (28/07–29/09 e 06/10–15/12), critérios de conclusão por
   matéria e riscos.
2. **`docs/projeto_integrador/`** — um documento por matéria (`rna.md`, `pln.md`,
   `ia_generativa.md`, `ia.md`, `extensao.md`), cada um com: objetivo acadêmico, escopo
   técnico, backlog quebrado em sprints semanais com datas reais, artefatos esperados
   (notebook, script, relatório, dataset), critério de aceite e — obrigatoriamente — a
   **ficha de admissão** exigida pela restrição 5.4: resposta explícita aos testes de
   não-prejuízo e de agregação de valor, mais a decisão resultante (entra no produto /
   fica como experimento fora do caminho de produção).
3. **`docs/projeto_integrador/artigo.md`** — plano do artigo científico: pergunta de
   pesquisa, contribuição pretendida, estrutura de seções, qual matéria alimenta cada
   seção, protocolo experimental (dados, split, semente, baselines, métricas), plano de
   reprodutibilidade e veículo-alvo com prazo de submissão. Autoria: Fagner, Daianne e
   Matheus. Recomende uma pergunta de pesquisa central que una as matérias em vez de
   cinco trabalhos soltos — e diga com franqueza se a base sintética limita o veículo ao
   qual o artigo pode ser submetido.
4. **Convenção de rastreabilidade** — proposta de branch (ex.: `academico/2026-2`), padrão
   de commit que identifique matéria e autor, e um `docs/projeto_integrador/REGISTRO.md`
   que sirva de índice do que foi produzido no semestre.
5. **Atualização mínima do `README.md`** — um bloco curto apontando a trilha acadêmica,
   sem inflar o README nem alterar o posicionamento comercial do produto.

**Não implemente código de modelo, PLN ou LLM nesta rodada.** Esta rodada é de
planejamento e documentação. Ao final, liste em ordem de prioridade as três primeiras
tarefas de código e pergunte por onde começar.

---

## 7. Como trabalhar

- Leia os arquivos citados antes de escrever sobre eles; não infira comportamento.
- Escreva em **português do Brasil**, tom técnico e direto, no padrão dos documentos que já
  existem em `docs/`.
- Se algo do briefing conflitar com o que você encontrar no repositório, **aponte o
  conflito** em vez de escolher silenciosamente um dos lados.
- Ementas das matérias não estão disponíveis: onde a entrega depender do que o professor
  vai cobrar, marque como **premissa a confirmar** em vez de afirmar.
