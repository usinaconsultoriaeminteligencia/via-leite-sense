# Processamento de Linguagem Natural (PLN) — Projeto Integrador 2026-2

> **Matéria:** Processamento de Linguagem Natural · **Professor:** Raphael
> **Janela:** 28/07 – 29/09/2026 (Bloco 1) · **Encontros:** Qua 18:30–20:30
> **Subpergunta que esta matéria responde:** **SP2** (§11 do documento mestre)
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Data de referência:** 05/08/2026 (sprint 2 de 9)

---

## 1. Objetivo

Responder **SP2**:

> *Com que fidelidade a mensagem livre do produtor se converte em lançamento
> estruturado, sem perda de informação crítica?*

Operacionalmente: dada uma mensagem como

> *"mandei 320 litros hoje, a vaca 12 tá com mastite"*

produzir um **lançamento estruturado** no banco — volume `320`, data `hoje`, evento
sanitário `mastite` no animal `12` — com **classificação de intenção + reconhecimento
de entidades (NER)**, em pipeline clássico.

A motivação é de produto e está documentada: a hipótese **H4** de
`docs/validacao_mercado.md` afirma que *"o principal obstáculo à adoção não é o preço,
mas a dificuldade de inserir dados operacionais de forma sistemática"*. Se H4 estiver
certa, **a entrada de dados é o gargalo de adoção** — e esta matéria ataca exatamente
esse gargalo.

---

## 2. Ficha de admissão (§4 do mestre)

| Teste | Resposta |
|---|---|
| **1. Não-prejuízo** | ✅ **Atende.** Trabalho isolado em `experimentos/pln/`, com **`requirements` próprio**. Hoje o `requirements.txt` do projeto **não tem** spaCy, transformers, nltk nem qualquer dependência de PLN (verificado) — e **não terá** no Bloco 1. Nada é adicionado ao runtime de produção. |
| **2. Agregação de valor** | ✅ **Forte.** Ataca H4, a barreira de adoção declarada. Cria capacidade que o produto não tem: hoje **todo** dado entra por formulário estruturado. |

---

## 3. O problema central: **não existe corpus** — verificado

Esta matéria começa com um obstáculo que RNA não tem. O levantamento do repositório:

| Fonte | O que tem | Serve como corpus? |
|---|---|---|
| `dados_teste/*.csv` (base sintética) | **Nenhuma coluna de texto livre.** Todas as colunas `object` são códigos categóricos (`municipio`, `tipo_sistema`, `nivel_tecnificacao`, `porte_produtor`, `polo_climatico`…) | ❌ Não |
| DuckDB `fact_plano_acao.descricao` | 9–13 linhas por base de teste | ❌ Não — é **texto de gestor** em teste, não fala de produtor |
| DuckDB `fact_plano_acao.observacoes` | 0–1 linha preenchida | ❌ Não |
| `fact_evento_gerencial.descricao_detalhada` | Coluna **declarada** em `gestor_store.py:212`, mas a tabela **não existe** nas bases materializadas | ❌ Não |
| Canal produtor ↔ cooperativa | **Não existe** — está no backlog do produto | ❌ Não |

> **Conclusão: o corpus precisa ser construído do zero.** Isso não é detalhe de
> execução — é o risco número um da matéria e define todo o cronograma.

### 3.1 A armadilha que precisa ser evitada

A saída óbvia é a equipe escrever as mensagens. **É a mesma armadilha que ameaça a
SP1**: em RNA, o modelo pode estar aprendendo o gerador sintético; em PLN, um corpus
escrito pelos três autores treinaria o modelo a **reconhecer o jeito de escrever da
equipe**, não o do produtor rural.

Três pessoas urbanas, com formação em tecnologia, não escrevem como um produtor de
leite do interior de Goiás. Não reproduzem a ortografia, as abreviações, o vocabulário
regional, o áudio transcrito, o "mandei 320 litro" sem s. Um F1 alto sobre esse corpus
seria **métrica de autoconsistência**, não de capacidade.

---

## 4. Estratégia de corpus: **treinar em sintético, testar em real**

A solução espelha o rigor exigido em SP1 e é o desenho metodológico central desta
matéria:

| Conjunto | Origem | Uso | Tamanho-alvo |
|---|---|---|---|
| **Treino + validação** | **Sintético**, gerado pela equipe a partir de um roteiro de variação (§4.1) | Treinar e sintonizar | 600–1.000 mensagens |
| **Teste** | **REAL** — falas coletadas de produtores | **Aberto uma única vez, ao final** | 60–150 mensagens |

> **A métrica que vale no artigo é a do conjunto real.** O desempenho no conjunto
> sintético é reportado apenas como referência interna, e a **diferença entre os dois**
> é o resultado mais interessante da matéria: ela mede exatamente o quanto a linguagem
> sintética engana.

### 4.1 Variação deliberada no corpus sintético

Para o corpus sintético não ser homogêneo, gerar com variação explícita e documentada
em: registro (formal ↔ coloquial), erros de ortografia e ausência de acentuação,
abreviações (`lt`, `qtd`, `vc`), unidades escritas por extenso (`trezentos e vinte
litros`), transcrição de áudio (frases longas sem pontuação), mensagens **multi-intenção**
(volume + sanitário na mesma frase) e mensagens **ambíguas ou incompletas** — que são as
que realmente quebram o pipeline.

### 4.2 Origem do conjunto real — **depende da Extensão, e há conflito de calendário**

A fonte natural de fala real é o **bloco 4 (escuta)** da oficina de extensão
(`extensao.md` §7.1). Mas:

- **PLN encerra em 29/09**;
- **A oficina de extensão acontece entre outubro e novembro.**

**O dado real chega depois de a matéria fechar.** Isso precisa de solução, não de
observação.

**Solução adotada — coleta antecipada de linguagem, em agosto/setembro.** Aproveitar
os contatos de **prospecção P1/P2** (`extensao.md` §6), que já ocorrem em agosto, para
uma coleta pequena e específica: pedir ao produtor que **descreva, com as palavras
dele**, o que reportaria à cooperativa em situações típicas (entregou X litros; vaca
com mastite; queda de produção no calor; problema na coleta).

- **Não é a oficina** e não a substitui — é uma coleta de linguagem de ~20 min;
- **60–150 enunciados bastam** para um conjunto de teste, muito menos do que treino
  exigiria;
- Se render menos que o mínimo, o conjunto real vira **estudo qualitativo de erro**
  (análise das falhas, sem F1 sobre ele), e a limitação é declarada.

> ⚠️ **Vale a regra de PII da `extensao.md` §5.** Fala de produtor é dado pessoal.
> Consentimento por escrito antes da coleta; corpus **anonimizado** antes de qualquer
> versionamento (nomes de pessoas, propriedades e animais identificáveis substituídos
> por marcadores). O corpus bruto **não entra no repositório público**.

---

## 5. Esquema de anotação

Rascunho — a ser fechado na sprint 4, **antes** de anotar.

### 5.1 Intenções

| Intenção | Exemplo |
|---|---|
| `registro_producao` | "mandei 320 litros hoje" |
| `registro_qualidade` | "deu 250 de CCS no último exame" |
| `ocorrencia_sanitaria` | "a vaca 12 tá com mastite" |
| `ocorrencia_operacional` | "o resfriador parou de noite" |
| `ocorrencia_logistica` | "o caminhão não veio buscar" |
| `relato_ambiental` | "com esse calor caiu a produção" |
| `solicitacao` | "queria que o técnico passasse aqui" |
| `outro` / `indefinido` | fora de escopo ou ambíguo demais |

### 5.2 Entidades

| Entidade | Exemplo |
|---|---|
| `VOLUME` | `320 litros`, `trezentos e vinte` |
| `ANIMAL` | `vaca 12`, `a mocha` |
| `DOENCA` | `mastite`, `mamite` |
| `TEMPO` | `hoje`, `ontem`, `semana passada` |
| `INDICADOR` | `CCS`, `CBT`, `gordura` |
| `VALOR_INDICADOR` | `250`, `250 mil` |
| `EQUIPAMENTO` | `resfriador`, `tanque`, `ordenhadeira` |
| `MEDICAMENTO` | (a confirmar se ocorre no corpus real) |

**Regra de anotação:** dupla anotação independente em ao menos **20 %** do corpus, com
**concordância entre anotadores medida por Kappa de Cohen**. Sem esse número, a
qualidade do corpus é afirmação, não evidência — e é a primeira coisa que uma banca
pede.

---

## 6. Métricas e critério de sucesso

| Nível | Métrica | Observação |
|---|---|---|
| Intenção | **F1 macro** | Macro, não micro — as classes serão desbalanceadas e `registro_producao` dominaria |
| Entidade | **F1 span-level** (esquema CoNLL, correspondência exata) | Correspondência parcial reportada à parte |
| Corpus | **Kappa de Cohen** entre anotadores | Qualidade do dado antes da qualidade do modelo |
| **Ponta a ponta** | **Taxa de lançamento correto** | A métrica que importa para o produto |
| **Crítico** | **Taxa de erro em campo crítico** | Ver §6.1 |

### 6.1 Nem todo erro custa o mesmo

Esta é a distinção que separa um trabalho aplicado de um exercício de ementa:

- Errar a **intenção** de uma mensagem → o gestor reclassifica. Custo baixo.
- Errar o **volume** (`320` lido como `32`) → **entra dado errado no banco, alimenta o
  modelo preditivo e corrompe o score de risco**. Custo alto e silencioso.

**Consequência de projeto:** o pipeline deve ter **limiar de confiança com recusa
explícita**. Abaixo do limiar, a mensagem vai para **confirmação humana** em vez de ser
lançada. Um sistema que acerta 92 % e admite não saber nos 8 % restantes é
operacionalmente superior a um que acerta 95 % em silêncio. **Cobertura × precisão sob
recusa** entra na avaliação.

---

## 7. Trilha de modelos

| Etapa | Abordagem | Papel |
|---|---|---|
| **E0** | Regras + regex (números + unidades, léxico de doenças) | **Baseline honesto.** Para extração de volume, regex é forte — e se ele empatar com o modelo neural, isso é resultado |
| **E1** | TF-IDF + Regressão Logística / SVM (intenção); CRF (NER) | Baseline clássico de ementa |
| **E2** | Embeddings estáticos pt-BR + spaCy | Ganho de generalização lexical |
| **E3** | **BERTimbau** *fine-tuned* (classificação + token classification) | Teto esperado do pipeline clássico |

**Critério de decisão (§4 do mestre):** entra no produto se o pipeline atingir taxa de
lançamento correto ponta a ponta que justifique o canal de entrada por texto, **com**
mecanismo de recusa funcionando. Caso contrário, permanece experimento e o resultado é
reportado.

---

## 8. Fronteira com a IA Generativa — não invadir

Um LLM resolveria a extração com *prompt* e poucos exemplos. **Não é o que esta
matéria faz**, por três razões:

1. **Ementa:** a matéria é de PLN clássico (§5 do mestre) — TF-IDF, embeddings, spaCy,
   BERTimbau;
2. **Separação de matérias:** a camada LLM é da IA Generativa (SP3, RAG normativo).
   Resolver PLN com LLM colapsaria duas entregas em uma;
3. **Mérito científico:** comparar pipeline clássico com LLM **é interessante** — mas
   como **discussão no artigo**, com o clássico devidamente construído primeiro.

> **Gancho legítimo para o artigo:** medir o custo/benefício do pipeline clássico
> (roda local, sem custo por chamada, auditável) contra a conveniência do LLM. Para
> produtor rural com conectividade instável, **rodar local é vantagem de produto**, não
> só de custo. Essa discussão fecha SP2 com SP3.

---

## 9. Backlog por sprint (28/07 – 29/09)

| Sprint | Período | Entrega | Estado |
|---|---|---|---|
| S1 | 28/07 – 03/08 | Ambientação na matéria | ✅ |
| **S2** | **04/08 – 10/08** | **Este documento; constatação de ausência de corpus** | 🔄 **atual** |
| S3 | 11/08 – 17/08 | Esquema de anotação fechado; roteiro de variação; **roteiro da coleta de linguagem** (entra na prospecção P1/P2 de agosto) | ⬜ |
| S4 | 18/08 – 24/08 | Corpus sintético gerado (600–1.000); anotação iniciada; **Kappa** medido | ⬜ |
| S5 | 25/08 – 31/08 | **Coleta de linguagem real em campo** (janela crítica) | ⬜ |
| S6 | 01/09 – 07/09 | E0 + E1 treinados e avaliados | ⬜ |
| S7 | 08/09 – 14/09 | E2 + E3 (BERTimbau) | ⬜ |
| S8 | 15/09 – 21/09 | **Avaliação no conjunto real** (aberto uma vez); análise de erro; limiar de recusa | ⬜ |
| S9 | 22/09 – 29/09 | Relatório; seção do artigo; decisão de admissão | ⬜ |

**S5 é o gargalo de todo o cronograma.** Depende de terceiro (produtor disponível) e
não pode ser recuperada depois — se escorregar para outubro, o conjunto real não existe
a tempo. **Deve ser tratada como marco, não como tarefa.**

---

## 10. Entregáveis (critério de conclusão — §7 do mestre)

- [ ] **Corpus anotado** — sintético (treino/validação) + real (teste), com esquema documentado;
- [ ] **Kappa de Cohen** reportado;
- [ ] Pipeline treinável e reprodutível em `experimentos/pln/`, com `requirements` próprio;
- [ ] **F1 por intenção** e **F1 de entidade**, no conjunto sintético **e** no real, lado a lado;
- [ ] **Demonstração de conversão** mensagem → lançamento estruturado;
- [ ] Análise de erro em campo crítico + limiar de recusa;
- [ ] Ficha de admissão respondida; registro em `REGISTRO.md`.

---

## 11. Riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| PLN-1 | **Coleta real não acontece a tempo (S5)** | **Alto** | Antecipar para a prospecção de agosto; plano B: conjunto real vira análise qualitativa sem F1, com limitação declarada |
| PLN-2 | Corpus sintético enviesado pela escrita da equipe | Alto | Roteiro de variação (§4.1); a métrica que vale é a do conjunto real; reportar a diferença entre os dois |
| PLN-3 | Corpus pequeno demais para BERTimbau | Médio | E0–E2 não dependem de volume; se E3 não convergir, é resultado reportável |
| PLN-4 | Erro em `VOLUME` corromper o banco e o modelo | **Alto** | Limiar de recusa + confirmação humana (§6.1); nunca lançar sem confirmação abaixo do limiar |
| PLN-5 | PII nas mensagens reais | Alto | Consentimento + anonimização antes de versionar; bruto fora do repositório |
| PLN-6 | Tentação de resolver com LLM | Médio | Fronteira da §8; LLM é matéria da IA Generativa |

---

## 12. Premissas a confirmar

1. **Ementa da matéria** (Raphael) — indisponível. Se exigir tema específico
   (ex.: análise de sentimento, sumarização), o escopo se adapta **sem** abandonar o
   eixo intenção + NER. **[premissa a confirmar]**
2. **Viabilidade da coleta de linguagem em agosto** — depende do aceite dos contatos
   P1/P2 (`extensao.md` §6). **Não confirmada.**
3. **Anotadores disponíveis** — a dupla anotação exige duas pessoas com o mesmo
   entendimento do esquema. Equipe tem três; confirmar quem anota.
4. **Canal real de mensagens (WhatsApp?)** — o produto não tem canal produtor ↔
   cooperativa. Definir se o trabalho assume WhatsApp como canal-alvo muda o formato do
   corpus (áudio transcrito vs. digitado). **[premissa a confirmar]**

---

## 13. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**.

| Autor | Papel nesta matéria |
|---|---|
| **Matheus Iverson** — dados/modelagem | Pipeline, treino, avaliação, análise de erro |
| **Daianne Valéria** — produto/UX | Esquema de anotação, roteiro de variação, coleta de linguagem em campo, desenho da confirmação humana |
| **Fagner Vieira** — negócio/produto | Ligação com H4, critério de admissão, relatório |

**Maria Vitória e Diego Santana não participam do Projeto Integrador** e **não são
coautores** desta ou de qualquer entrega acadêmica. Atuam exclusivamente na Maratona
SENAR Goiás.

**Convenção de commit:** `acad(pln): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

_Documento da matéria de PLN — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §13)._
