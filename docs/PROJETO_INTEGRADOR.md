# Projeto Integrador 2026-2 — Trilha Acadêmica do Via Leite Sense

> **Nota de 10/10/2026 (trazido do branch `academico/2026-2`):** estes documentos foram escritos em 05/08/2026, antes da reorganização de 25/08. Os caminhos mudaram: `backend/app.py` agora é `via_leite/api/app.py`; `treino_mvp_avancado.py`, `score_risco.py` e `gerador_leite_sintetico.py` estão em `via_leite/models/` e `via_leite/core/`; a falha A2 (CPF/nome como atributos do modelo) já foi corrigida no `master`. O Streamlit foi removido.
>
> Documento **mestre** da trilha acadêmica. Consolida contexto, equipe/autoria,
> mapa matéria→entrega, cronograma, critérios de conclusão e riscos. Os detalhes
> técnicos de cada matéria vivem em `docs/projeto_integrador/` (um arquivo por
> matéria) e o plano do artigo em `docs/projeto_integrador/artigo.md`.
>
> **Natureza:** este é documento **acadêmico** (leva limitações e autocrítica).
> Não confundir com `docs/PITCH.md`, `docs/PLANO_DE_NEGOCIO.md` e materiais para
> SENAR/SEBRAE/investidor, que seguem outra régua (restrição 2 da seção 5).
>
> **Data de referência:** 04/08/2026 (semana 2 do semestre).
> **Apresentação do Projeto Integrador:** **12/12/2026** ← prazo que vale.
> **Encerramento do semestre:** 15/12/2026.
>
> ⚠️ **São datas distintas.** Tudo que vai à banca — relatório, artigo e apresentação —
> precisa estar **pronto em 12/12**, não em 15/12. Os três dias de diferença não são
> folga: são o intervalo entre apresentar e encerrar.

---

## 1. Contexto do produto

O **Via Leite Sense** (USINA I.A.) é um radar de risco produtivo, de qualidade e
de rentabilidade para a cadeia leiteira. É **produto em produção**, anterior ao
semestre — não um sandbox acadêmico. O que já existe, verificado no repositório:

| Camada | Artefato | Estado verificado |
|---|---|---|
| Modelo preditivo | `treino_mvp_avancado.py` | `XGBRegressor`, target `target_media_coletada_7d` (horizonte 7 d), `SEED=42`, split temporal (treino < 2024 / validação 2024 / teste ≥ 2025). ~120 features (lags 1–28, médias móveis 3/7/14/30, THI, interações). |
| Métricas | `artefatos_teste/metricas_modelo.json` | Teste: **MAE 24,45 L** vs **baseline MAE 31,54 L** (ganho ≈ **22 %**); R² 0,994 (baseline já 0,990). |
| Motor de risco (regras) | `score_risco.py` | Score 0–100 com **7 dimensões ponderadas** (soma 100); limiares na **IN 77/2018** do MAPA; classes Baixo/Atenção/Alto/Crítico. |
| Classificador de perfil (regras) | `perfil/classificador_perfil.py` | 3 perfis (Consistente/Oscilante/Desafiador), IN 76/77, saída interpretável (sinais + confiança). |
| Dados | `gerador_leite_sintetico.py`, `ingestao_clima_inmet.py`, `executar_piloto_real.py` | Base **majoritariamente sintética** + clima real INMET; pipeline de dados reais. |
| Produto | `backend/app.py` (~28 endpoints, DuckDB) + `frontend/` (SPA, Vercel) | Streamlit descomissionado (`via_leite_app_legacy.py`). Endpoints-chave: `/action-plans`, `/model/*`, `/risk-radar`, `/api/iot/*`. |
| IoT simulado | `via_leite_edge/` | Módulo de leitura simulada + alertas. |

**Lacunas que a trilha acadêmica preenche** (confirmadas em `requirements.txt`,
que declara apenas `scikit-learn` e `xgboost`): **não há rede neural, não há PLN
e não há camada generativa/LLM**. Cada matéria adiciona uma dessas capacidades —
e cada adição passa pelo critério de admissão da seção 4.

---

## 2. Equipe e autoria — regra obrigatória

A equipe do **produto** Via Leite Sense tem 5 pessoas, mas o **Projeto Integrador
(faculdade)** e a **Maratona SENAR Goiás** têm composições **diferentes**. Esta
distinção é obrigatória em todo documento acadêmico.

| Pessoa | Papel | Projeto Integrador | Maratona SENAR |
|---|---|---|---|
| **Fagner Vieira** — negócio/produto | Fundador USINA I.A. | ✅ integrante e autor | ✅ |
| **Daianne Valéria** — produto/UX | Produto/UX | ✅ integrante e autora | ✅ |
| **Matheus Iverson** — dados/modelagem | Dados/modelagem | ✅ integrante e autor | ✅ |
| Maria Vitória — veterinária | Validação sanitária | ❌ **não participa** | ✅ |
| Diego Santana — engenharia de software | Arquitetura/IoT | ❌ **não participa** | ✅ |

**Regras (inegociáveis):**

- O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
  Iverson — e somente por eles**. Autoria de relatório, artigo, apresentação e ficha
  de equipe = esses três.
- **Maria Vitória e Diego Santana atuam exclusivamente na Maratona SENAR Goiás.**
  Não são coautores de nenhum entregável acadêmico e não aparecem como autores.
- Onde a contribuição deles tocar o produto (validação sanitária; arquitetura/IoT),
  registrar como **contribuição externa ao escopo acadêmico**, creditada como tal —
  **nunca como coautoria**.
- Todo documento acadêmico traz uma seção **"Equipe e autoria"** com esta distinção
  escrita de forma inequívoca.

> ✅ **Resolvido (05/08/2026).** O conflito de nome ("Fagner Pinho" no briefing de
> entrada × "Fagner Vieira" no repositório) foi confirmado pelo autor: o nome
> correto, que assina toda a autoria acadêmica, é **Fagner Vieira**. O briefing
> continha erro de digitação e não deve ser tomado como fonte para autoria.

---

## 3. Grade do semestre (IA5 — Evento 953633 — Lab. 107)

| Matéria | Professor | Janela | Encontros |
|---|---|---|---|
| Redes Neurais Artificiais (RNA) | Cristiano | **28/07 – 29/09** | Seg (4 blocos) + Ter 18:30–20:30 |
| Processamento de Linguagem Natural (PLN) | Raphael | **28/07 – 29/09** | Qua 18:30–20:30 |
| Inteligência Artificial Generativa | Raphael | **06/10 – 15/12** | Qui (4 blocos) + Ter 20:45–22:45 |
| Inteligência Artificial (IA) | Alexandre Barbosa | **semestre inteiro** | Sex (4 blocos) |
| Projeto de Extensão Integrador — IA | Willgnner | **06/10 – 15/12** | Qua 20:45–22:45 |

Dois blocos temporais: **Bloco 1 (28/07–29/09)** = RNA + PLN; **Bloco 2
(06/10–15/12)** = IA Generativa + Extensão. **IA (Alexandre)** atravessa o semestre.

> ⚠️ **Alerta de cronograma (Extensão).** A matéria de Extensão só começa em
> **06/10**, mas articular cooperativa/produtores leva **meses**. A prospecção
> precisa começar em **agosto** — ver seção 5 e `docs/projeto_integrador/extensao.md`.

---

## 4. Critério de admissão — nada entra "porque a matéria pediu"

O Via Leite Sense é produto em produção. **Toda** implementação proposta por uma
matéria precisa passar, **antes de virar código**, pelos dois testes abaixo, e a
resposta a cada um fica registrada na **ficha de admissão** do documento da matéria:

1. **Não-prejuízo** — não quebra, não regride e não degrada o que já funciona
   (`backend/app.py`, `frontend/`, `score_risco.py`, `treino_mvp_avancado.py`,
   pipeline de dados). A adição é **isolável e reversível** (módulo novo, flag ou
   branch); removê-la devolve o produto ao estado anterior sem cicatriz.
2. **Agregação de valor** — melhora o produto de forma defensável: ganho de acurácia
   sobre o baseline atual, nova capacidade com demanda real do cliente, ou redução de
   custo/atrito. **"Cumprir ementa" não é valor.**

**Se uma entrega não passar nos dois testes**, ela **não vai para o produto**: fica
como experimento fora do caminho de produção (`experimentos/`, notebook ou branch
descartável) e é reportada honestamente no artigo como **hipótese testada e
rejeitada** — resultado negativo documentado também é contribuição.

---

## 5. Mapa matéria → entrega

Resumo executivo; o escopo técnico, backlog em sprints e a ficha de admissão de
cada uma estão no arquivo correspondente em `docs/projeto_integrador/`.

| Matéria | Entrega-núcleo | Aproveita do repo | Documento |
|---|---|---|---|
| **IA** (Alexandre) | Formalizar `score_risco.py` + `classificador_perfil.py` como **sistema baseado em conhecimento** (representação, regras, decisão sob incerteza) e comparar com o aprendido. Gancho opcional: otimização de **sequenciamento de rotas** com `dim_rota`. Seção de ética/LGPD (produtor identificável). | `score_risco.py`, `perfil/`, `dim_rota` | `ia.md` |
| **RNA** (Cristiano) | Desafiar o XGBoost com **rede neural** no **mesmo target e mesmo split**. Trilha: MLP tabular → LSTM/GRU sobre a série por produtor → (opcional) N-BEATS/TFT. | pipeline de features de `treino_mvp_avancado.py` | `rna.md` |
| **PLN** (Raphael) | **Classificação de intenção + NER** sobre mensagens livres do produtor ("mandei 320 litros hoje, a vaca 12 tá com mastite") → lançamento estruturado no banco. Pipeline clássico (TF-IDF/embeddings, spaCy, BERTimbau). Secundária: busca semântica sobre IN 76/77, Embrapa, MilkPoint. | canal produtor↔cooperativa (backlog) | `pln.md` |
| **IA Generativa** (Raphael) | **Decidido (05/08/2026): candidato (a) — RAG sobre normativas** gerando o plano de ação a partir do score (endpoints `/action-plans`), com avaliação de alucinação/aderência/guardrails. **Precisão (05/08): "o score" é `score_risco_fornecedor` (`fornecedor_inteligencia.py`), não o `score_via_leite` formalizado em `ia.md` — são dois motores distintos (achado G3).** É o núcleo experimental do artigo (SP3, §11). Descartados por ora: (b) geração sintética (CTGAN/TimeGAN) — maior risco técnico e não gera capacidade nova; (c) agente de resumo semanal — menos ancorável em fonte, avaliação de alucinação frágil na banca. | `/action-plans` | `ia_generativa.md` |
| **Extensão** (Willgnner) | **Comunidade externa real**: piloto com cooperativa/produtores em Goiás, oficina de capacitação, QR de demo em campo, relatório com nº de beneficiários e evidências. | produto no ar (Vercel) | `extensao.md` |

---

## 6. Cronograma dos dois blocos

Datas reais; sprints semanais detalhadas em cada documento de matéria.

### Bloco 1 — 28/07 a 29/09 (RNA + PLN) · IA em paralelo
- **RNA:** MLP tabular (baseline neural) → LSTM/GRU por produtor → comparação justa com o XGBoost. Marco: relatório de comparação com o mesmo split/semente.
- **PLN:** corpus de mensagens do produtor → intenção + NER → conversão em lançamento. Marco: pipeline avaliado (F1 por intenção, F1 de entidade).
- **IA (transversal):** formalização do sistema baseado em conhecimento; seção ética/LGPD. Marco: documento conceitual + comparação regras × aprendido.
- **⚠️ Extensão (antecipada):** **iniciar prospecção de cooperativa em agosto**, ainda no Bloco 1, mesmo a matéria começando só em 06/10.

### Bloco 2 — 06/10 a 15/12 (IA Generativa + Extensão) · IA encerra
- **IA Generativa:** implementar o candidato **aprovado (a) — RAG de plano de ação** + avaliação de alucinação/guardrails. Responde SP3 (§11).
- **Extensão:** executar o piloto em campo (oficina, QR de demo, coleta de evidências e beneficiários) com a cooperativa já articulada no Bloco 1.
- **IA:** fechamento (gancho de otimização de rotas, se admitido) e consolidação para o artigo.
- **Fechamento (até 12/12 — data da apresentação):** artigo científico submetível +
  `REGISTRO.md` completo + apresentação de banca. **Não usar 15/12 como prazo:** aquela
  é a data de encerramento do semestre, posterior à apresentação.

---

## 7. Critérios de conclusão por matéria

Cada matéria só é considerada concluída quando **todos** os itens abaixo existem e
estão versionados na branch acadêmica:

- **IA:** documento do sistema baseado em conhecimento; comparação regras × aprendido;
  seção de ética/LGPD. Ficha de admissão respondida.
- **RNA:** notebook/script reprodutível (semente fixa, mesmo split); tabela de
  comparação NN × XGBoost × baseline por MAE; decisão de admissão (entra no produto
  ou fica como experimento).
- **PLN:** dataset anotado + pipeline treinável; métricas (F1 intenção, F1 NER);
  demonstração de conversão mensagem→lançamento. Ficha de admissão respondida.
- **IA Generativa:** implementação do candidato aprovado; **avaliação de alucinação,
  aderência à fonte e guardrails**; ficha de admissão respondida.
- **Extensão:** relatório de piloto com **nº de beneficiários**, evidências de campo,
  material de oficina e QR de demo. (Não é código — é comunidade documentada.)

---

## 8. Princípios inegociáveis (resumo da seção 5 do briefing)

1. **Honestidade sobre a base.** A base é majoritariamente sintética (o modelo
   aprende, em parte, o próprio gerador). Reportar sempre o **ganho sobre o baseline**
   (MAE 24,45 vs 31,54 ≈ 22 %) como métrica principal — **nunca** o R² 0,994 absoluto.
2. **Separação acadêmico × externo.** Banca leva limitações; PITCH/PLANO_DE_NEGOCIO
   e material SENAR/SEBRAE/investidor **não**. Não deixar vazar um no outro.
3. **Não apresentar dado simulado como real** (já vigente em `docs/PRODUTO.md`).
4. **Critério de admissão** (seção 4): não-prejuízo + agregação de valor.
5. **Artigo científico entre os entregáveis** → reprodutibilidade (semente, split,
   versões), comparação justa (mesmo target/split/features) e baseline + limitações.
6. **Rastreabilidade de autoria** (seção 9).

---

## 9. Rastreabilidade de autoria

O incremento acadêmico é auditável e separado do produto comercial:

- **Branch dedicada:** `academico/2026-2` (proposta; ver `REGISTRO.md`).
- **Convenção de commit:** identifica matéria e autor —
  `acad(<materia>): <resumo>  [autor: <iniciais>]`, com `<materia>` ∈
  `{ia, rna, pln, iagen, extensao, artigo}`.
- **Índice:** `docs/projeto_integrador/REGISTRO.md` — o que foi produzido entre
  28/07 e 15/12/2026, por matéria e data.

---

## 10. Riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| R1 | **Base sintética limita a validade** externa e o veículo do artigo | Alto | Honestidade metodológica; reportar ganho sobre baseline; discutir ameaça à validade; considerar validação parcial com os dados reais já registrados no projeto (em `dados_reais/`, fora do versionamento por conter PII) |
| R2 | **Extensão exige articulação longa** e começa tarde na grade | Alto | Prospecção de cooperativa **em agosto**, antecipada ao Bloco 2 |
| R3 | **NN pode não superar o XGBoost** em dados tabulares | Médio | Resultado negativo é válido no artigo; NN não entra no produto se não passar na admissão |
| R4 | **Camada LLM alucinar** em contexto normativo | Médio | RAG restrito à fonte + avaliação de aderência/guardrails |
| R5 | **Escopo de 5 matérias dispersar** em 5 trabalhos soltos | Médio | Pergunta de pesquisa central única (seção 11) unindo as entregas |
| R6 | **Autoria/nome inconsistente** entre produto e academia | Baixo | Confirmar nome (seção 2) e manter a distinção PI × Maratona em todo documento |

---

## 11. Pergunta de pesquisa central — **decidida em 05/08/2026**

Para evitar cinco trabalhos soltos, a trilha adota **uma pergunta central e três
subperguntas falseáveis**, cada uma sob responsabilidade de uma matéria.

A decisão inverte a maior fragilidade do projeto — a base majoritariamente sintética
(R1) — de limitação declarada em rodapé para **condição estrutural da própria
pergunta**. Não se pergunta "o sistema funciona apesar da base?", e sim "o que se pode
legitimamente afirmar, e o que não se pode, quando a base é sintética?". A limitação
deixa de ser concessão e vira objeto de estudo.

### Pergunta central

> **Como construir e avaliar a confiabilidade de um sistema de apoio à decisão baseado
> em IA para a cadeia leiteira quando o substrato de dados é majoritariamente sintético
> — isto é, que garantias cada camada (conhecimento normativo, aprendizado
> supervisionado, entrada em linguagem natural e geração ancorada em fonte) consegue
> efetivamente oferecer, e quais permanecem fora de alcance?**

A cláusula final ("quais permanecem fora de alcance") é deliberada: resultado negativo
documentado é contribuição (§4) e a honestidade sobre a base (§8.1) passa a ser
metodologia, não ressalva.

### Subperguntas

| # | Subpergunta | Matéria | Como se responde (métrica) |
|---|---|---|---|
| **SP1** | Qual o ganho real do aprendizado supervisionado sobre o baseline de média móvel de 7 dias, e onde está o teto desse ganho em base sintética? | RNA (+ IA) | MAE de NN × XGBoost × baseline, mesmo target/split/semente. Partida verificada: **24,45 vs 31,54 ≈ 22 %**. |
| **SP2** | Com que fidelidade a mensagem livre do produtor se converte em lançamento estruturado, sem perda de informação crítica? | PLN | F1 por intenção, F1 de entidade (NER), taxa de perda em campos obrigatórios. |
| **SP3** | A ancoragem em fonte normativa (IN 76/77) via RAG reduz alucinação e aumenta aderência frente à geração não ancorada? | IA Generativa | Comparação ancorado × não ancorado: taxa de alucinação, aderência à fonte, cobertura de citação. |

**SP3 é o núcleo experimental do artigo.** Motivo: é a única camada cujo substrato de
evidência é **real** — o corpus normativo (IN 76/77, Embrapa) existe e é verificável,
enquanto a base de produção é sintética. É onde o trabalho produz resultado que não
depende do gerador. **SP1** é a âncora de honestidade metodológica (mede o teto e o
admite). **SP2** sustenta a viabilidade da entrada de dados.

### Papel da Extensão

A Extensão **não** é subpergunta — é **evidência de validade externa**. O critério da
matéria (§7) é comunidade documentada (beneficiários, oficina, evidências de campo),
não experimento controlado. O piloto responde "o sistema sobrevive ao contato com o
produtor real?", qualificando a resposta da pergunta central sem depender de um estudo
de usuários que a equipe não tem escala para conduzir com rigor em um semestre.

### Plano de contingência (mitiga R2)

Se a articulação com a cooperativa não se materializar até **outubro**, a pergunta
central e as três subperguntas permanecem **intactas** — perde-se apenas a validade
externa, reportada então como limitação. **Nenhum documento de matéria precisa ser
reescrito.** Essa é a razão de a Extensão ficar fora das subperguntas.

O desenvolvimento formal — contribuição pretendida, protocolo experimental,
reprodutibilidade e veículo-alvo — está em `docs/projeto_integrador/artigo.md`.

---

## 12. Premissas a confirmar

Marcadas por não haver fonte fechada no repositório ou por dependerem do professor:

1. ~~**Nome do autor**~~ — ✅ **resolvido em 05/08/2026: Fagner Vieira.** Ver §2.
2. ~~**Definição do baseline**~~ — ✅ **resolvido em 05/08/2026 por leitura do código.**
   `gerar_baseline()` (`treino_mvp_avancado.py:213`) é **média móvel de 7 dias**
   (`mm_7_litros_coletados`) com fallback em cascata para a **média móvel de 30 dias**
   (`mm_30_litros_coletados`) e, persistindo o vazio, para
   `producao_media_esperada_litros_dia`. O rótulo correto no artigo é, portanto,
   *"baseline de média móvel de 7 dias com fallback"* — **não** naïve nem persistência.
   A cascata de fallback deve ser descrita, pois torna o baseline mais forte do que uma
   MM7 pura e, com isso, o ganho de 22 % mais conservador (a favor da honestidade §8.1).
3. **Citação "Gonçalves (2025)"** — o briefing atribui o classificador de perfil a "IN
   76/77 e Gonçalves (2025)", mas o módulo cita **IN 76/77 + MilkPoint (06/2026)**;
   "Gonçalves (2025)" **não foi encontrado** no repositório. Confirmar a referência real.
4. **Ementas das matérias** — indisponíveis. Onde a entrega depender do que o professor
   cobrará, o documento da matéria marca **[premissa a confirmar]** em vez de afirmar.

---

_Documento mestre da trilha acadêmica — Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §2)._
