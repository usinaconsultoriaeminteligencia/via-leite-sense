# Redes Neurais Artificiais (RNA) — Projeto Integrador 2026-2

> **Matéria:** Redes Neurais Artificiais · **Professor:** Cristiano
> **Janela:** 28/07 – 29/09/2026 (Bloco 1) · **Encontros:** Seg (4 blocos) + Ter 18:30–20:30
> **Subpergunta que esta matéria responde:** **SP1** (§11 do documento mestre)
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Data de referência:** 05/08/2026 (sprint 2 de 9)

---

## 1. Objetivo

Responder **SP1**:

> *Qual o ganho real do aprendizado supervisionado sobre o baseline de média móvel de
> 7 dias, e onde está o teto desse ganho em base sintética?*

Operacionalmente: **desafiar o XGBoost em produção com uma rede neural**, no **mesmo
target, mesmo split e mesma semente**, e — mais importante — **medir o teto**. A
entrega desta matéria não é "a rede neural venceu"; é **saber de onde vem o ganho de
22 % que o projeto reporta**, e quanto dele sobrevive a um protocolo limpo.

Esta é a matéria que sustenta a honestidade metodológica de todo o trabalho. Se o
ganho atual estiver inflado, é aqui que isso aparece — e reportar isso **é** a
contribuição, não o fracasso dela (§4 e §8.1 do mestre).

---

## 2. Ficha de admissão (§4 do mestre)

| Teste | Resposta |
|---|---|
| **1. Não-prejuízo** | ✅ **Atende.** Todo o trabalho ocorre em `experimentos/rna/` na branch `academico/2026-2`. `treino_mvp_avancado.py` não é alterado no Bloco 1 — é **lido e replicado**, não modificado. O modelo em produção (`artefatos_teste/modelo_mvp.joblib`, servido por `/model/*`) permanece intocado. Remover a pasta devolve o repositório ao estado atual sem cicatriz. |
| **2. Agregação de valor** | ⏳ **A decidir ao fim da sprint 8**, por critério pré-registrado (§6). A rede neural só entra no produto se superar o XGBoost em MAE de teste **no protocolo corrigido**. Caso contrário, fica como experimento e vira resultado negativo documentado. |

> ⚠️ **Exceção deliberada ao não-prejuízo.** A auditoria da §4 pode recomendar
> **correções no pipeline de produção** (features contaminadas). Essas correções **não**
> entram no Bloco 1. São propostas como tarefa separada, com decisão explícita do
> Fagner, depois de medida a magnitude do impacto. Auditar e corrigir são atos
> distintos: esta matéria audita.

---

## 3. Linha de base atual — verificado no repositório

Tudo abaixo foi lido em `treino_mvp_avancado.py` e em
`artefatos_teste/metricas_modelo.json`. Nada aqui é estimativa.

### 3.1 Configuração

| Item | Valor | Origem |
|---|---|---|
| Modelo | `XGBRegressor` (fallback: `HistGradientBoostingRegressor` se xgboost ausente) | `treino_mvp_avancado.py:182-199` |
| Hiperparâmetros | `n_estimators=300`, `max_depth=8`, `learning_rate=0.05`, `subsample=0.85`, `colsample_bytree=0.85` | idem |
| Semente | `SEED = 42` | `treino_mvp_avancado.py:28` |
| Target | `target_media_coletada_7d` — média de `litros_coletados` nos dias **t+1 … t+7** | `:119-128` |
| Split temporal | treino `< 2024-01-01` · validação `2024` · teste `≥ 2025-01-01` | `:134-138` |
| Volume | treino **32.010** · validação **10.980** · teste **10.920** linhas | `metricas_modelo.json` |
| Features | **133** (119 numéricas + 14 categóricas) | idem |
| Pré-processamento | imputação (mediana / mais frequente) + `OneHotEncoder(handle_unknown="ignore")` | `:165-180` |
| Baseline | **MM7 com fallback em cascata** → MM30 → `producao_media_esperada_litros_dia` | `:213-215` |

### 3.2 Resultados de referência (conjunto de teste, ≥ 2025)

| Métrica | Modelo | Baseline | Ganho |
|---|---|---|---|
| **MAE (L)** | **24,45** | **31,54** | **22,5 %** |
| RMSE (L) | 36,86 | 48,57 | 24,1 % |
| MAPE (%) | 3,63 | 4,55 | — |
| R² | 0,9943 | 0,9901 | — |

> **Números de partida, de antes de A2 (06/08) e de C1 (20/10/2026).** O vigente é MAE
> **24,36** contra 31,54 (ganho de **22,8 %**), com 131 features. A série completa está em
> `docs/ESTADO_REAL.md` §8. Esta tabela fica como registro do ponto de partida.

> **Regra de reporte (§8.1 do mestre):** a métrica principal é **MAE e o ganho sobre o
> baseline**. O R² de 0,994 **não** é resultado — é sintoma de que o baseline já explica
> 0,990 da variância, isto é, de que a série é fortemente autocorrelacionada e a base é
> sintética. Citar R² absoluto como conquista é erro metodológico e será tratado como
> tal neste trabalho.

---

## 4. Auditoria do pipeline — **pré-requisito da comparação justa**

Comparar uma rede neural com o XGBoost **como ele está hoje** produziria um número sem
valor científico. A auditoria abaixo levantou três achados no conjunto de features
atual. **Todos precisam de decisão antes da sprint 4**, porque definem qual é o
"XGBoost de referência" contra o qual a rede será medida.

### A1 — Quebra de convenção temporal (duas features expõem o dia *t*)

O pipeline estabelece, de forma consistente, que a predição usa dados até **t−1**:
`litros_coletados` está na lista de exclusão (`:149`) e **todas** as médias móveis e
desvios aplicam `.shift(1)` antes do `rolling` (`:82-94`). Duas features derivadas
violam essa convenção e reintroduzem o dia *t*:

| Feature | Definição | Problema |
|---|---|---|
| `litros_ajustados_gerencial` | `litros_coletados[t] + impacto_gerencial_litros` | Contém `litros_coletados[t]` quase puro |
| `impacto_gerencial_pct` | `impacto_gerencial_litros / litros_coletados[t]` | Expõe `litros_coletados[t]` no denominador |

**Nuance importante — não afirmar mais do que se pode provar:** isto **não** é
vazamento do futuro. O target são os dias t+1…t+7 e, ao prever no fim do dia *t*, a
coleta de *t* seria legitimamente conhecida. O defeito é de **inconsistência**: o
pipeline declara uma convenção (até t−1) e duas features a violam. Como a série é
altamente autocorrelacionada, o dia *t* é informativo — mas **a magnitude é
desconhecida**. A ablação da sprint 4 é que vai medi-la.

**Ação:** ablação controlada (com e sem as duas features), semente fixa. O resultado
define a convenção oficial, aplicada igualmente ao XGBoost e à rede neural.

### A2 — Identificadores pessoais como features one-hot ⚠️

O conjunto categórico de `artefatos_teste` inclui:

- **`fornecedor_cpf_cnpj`**
- **`fornecedor_nome_razao_social`**

Ambos passam por `OneHotEncoder`. Três consequências:

1. **Metodológica.** One-hot sobre identificador é **memorização por indivíduo**: o
   modelo aprende "o produtor *X* entrega ~*N* litros". Isso infla a métrica sem
   representar capacidade de generalização.
2. **De produto (cold start).** Com `handle_unknown="ignore"`, **todo produtor novo
   recebe vetor nulo** nessas colunas. O modelo degrada silenciosamente exatamente no
   caso de maior valor comercial — o cliente recém-onboardado. Não há erro, não há
   alerta: só previsão pior.

   > **Janela favorável (confirmado em 05/08/2026):** a aplicação **ainda não tem
   > clientes pagantes**. Nenhum usuário real é prejudicado hoje. Isso rebaixa A2 de
   > incidente de produção para **correção pré-lançamento** — mas também estabelece o
   > prazo: **precisa estar resolvido antes do primeiro onboarding real**, porque o
   > primeiro cliente é, por definição, um produtor desconhecido pelo modelo.
3. **Ética e LGPD.** **CPF/CNPJ usado como variável preditiva.** Este achado alimenta
   diretamente a seção de ética/LGPD da matéria de IA (§5 do mestre) — é o exemplo
   concreto que aquele documento precisa.

**Evidência quantitativa preliminar.** O repositório tem dois artefatos de treino:

| Artefato | Features | MAE teste | Ganho sobre baseline |
|---|---|---|---|
| `artefatos_teste/` (com bloco `fornecedor_*`) | 133 | **24,45** | 22,5 % |
| `artefatos_validacao/` (sem bloco `fornecedor_*`) | 118 | **25,64** | 18,7 % |

A diferença de **≈ 1,2 L de MAE** — quase **4 pontos percentuais** do ganho reportado —
está associada ao bloco `fornecedor_*`, que contém os identificadores. **Isto é
sugestivo, não conclusivo:** os dois artefatos diferem em 15 features, não apenas nas
duas identificadoras. A ablação controlada da sprint 4 é que isola o efeito.

**Ação:** remover identificadores do conjunto de features do experimento
(irrevogável — não é opção de tuning) e medir o custo real em MAE. Se houver perda,
substituir por **atributos do produtor** (porte, tecnificação, sistema, raça), que
generalizam para produtor novo, em vez da identidade dele.

### A3 — Ausência de sintonia e de estimativa de variância

Três limitações do protocolo atual, todas relevantes para uma comparação justa:

- **Hiperparâmetros são constantes fixas** (`:183-192`), nunca sintonizados.
- **O conjunto de validação nunca é usado para seleção** — só é pontuado (`:271-272`).
  Na prática há **dois conjuntos de teste**, não um de validação.
- **Execução única, semente única.** Não há estimativa de variância.

**Por que isso é decisivo:** redes neurais **exigem** sintonia e têm variância entre
sementes bem maior que a de árvores. Sintonizar a rede e não sintonizar o XGBoost
produziria uma comparação enviesada — e o viés apareceria a favor da rede, o que é
pior, porque é o resultado que a matéria "gostaria" de obter.

**Ação:** protocolo simétrico (§5). Ambos os modelos recebem o mesmo orçamento de
busca sobre o **mesmo conjunto de validação**, e ambos são executados em **5 sementes**
com média ± desvio.

---

## 5. Protocolo experimental

Regras **pré-registradas** — fixadas antes de rodar qualquer modelo, para que a
escolha do vencedor não seja retroativa.

### 5.1 Invariantes (idênticos para todos os modelos)

1. **Target:** `target_media_coletada_7d`, horizonte 7 dias.
2. **Split temporal:** treino < 2024 · validação 2024 · teste ≥ 2025. **Nunca**
   aleatório — a série é temporal e embaralhar vazaria futuro no treino.
3. **Conjunto de features:** o conjunto **corrigido** pela auditoria (§4), sem
   identificadores e com convenção temporal única.
4. **Baseline:** `gerar_baseline()` inalterado — MM7 com fallback em cascata.
5. **Sementes:** `[42, 43, 44, 45, 46]`. Reporte de **média ± desvio-padrão**.
6. **Sintonia:** mesmo orçamento (30 configurações, busca aleatória) para cada modelo,
   avaliada **exclusivamente** no conjunto de validação (2024).
7. **Teste tocado uma vez.** O conjunto ≥ 2025 é aberto **uma única vez por modelo**,
   ao final, com a configuração já escolhida na validação.

### 5.2 Descrição honesta do baseline no artigo

O baseline **não** é naïve nem persistência. É **média móvel de 7 dias com fallback em
cascata** para MM30 e para `producao_media_esperada_litros_dia`. A cascata o torna
**mais forte** que uma MM7 pura — e, portanto, o ganho de 22,5 % é **mais conservador**
do que aparenta. Descrever a cascata é obrigatório: omiti-la subvende o próprio
resultado e é imprecisão técnica.

---

## 6. Trilha de modelos e critério de decisão

### 6.1 Trilha

| Etapa | Modelo | Justificativa | Sprints |
|---|---|---|---|
| **E1** | **MLP tabular** | Baseline neural. Mede o custo de trocar árvores por rede **sem** mudar a representação dos dados. | 3–4 |
| **E2** | **LSTM / GRU por produtor** | Onde a rede pode legitimamente vencer: consome a **sequência bruta** em vez das ~120 features derivadas à mão. Se a engenharia manual de atributos já captura tudo, a diferença será nula — e isso é resultado. | 5–7 |
| **E3** *(opcional)* | N-BEATS / TFT | Só se E2 mostrar sinal e houver folga de cronograma. **Não** é compromisso de entrega. | 8 |

### 6.2 Critério de decisão — pré-registrado

Decide a admissão no produto (§4 do mestre):

- **Entra no produto** se: MAE de teste **menor** que o do XGBoost corrigido, com
  intervalo de ±1 desvio-padrão (5 sementes) **não sobreposto**, **e** tempo de
  inferência compatível com os endpoints `/model/*`.
- **Fica como experimento** se: empate estatístico (intervalos sobrepostos) ou ganho
  que não justifique o custo operacional de manter um segundo runtime de modelo.
- **Resultado negativo** se: a rede perder. Vai para o artigo **como achado**, com a
  discussão de por que gradient boosting domina dados tabulares — que é a expectativa
  da literatura e o cenário **mais provável** (risco R3 do mestre).

> **O terceiro cenário não é fracasso.** Confirmar, com protocolo limpo, que a rede
> neural não supera o XGBoost neste problema é um resultado publicável — e mais
> defensável do que um ganho marginal obtido com protocolo frouxo.

---

## 7. Backlog por sprint (28/07 – 29/09)

| Sprint | Período | Entrega | Estado |
|---|---|---|---|
| S1 | 28/07 – 03/08 | Ambientação na matéria; leitura do pipeline atual | ✅ |
| **S2** | **04/08 – 10/08** | **Este documento + auditoria (§4) fechada** | 🔄 **atual** |
| S3 | 11/08 – 17/08 | `experimentos/rna/` estruturado; extração do pipeline de features como módulo reutilizável (sem tocar em produção) | ⬜ |
| S4 | 18/08 – 24/08 | **Ablações A1 e A2** com número fechado; definição do conjunto de features oficial | ⬜ |
| S5 | 25/08 – 31/08 | XGBoost **de referência** re-treinado no protocolo corrigido, 5 sementes | ⬜ |
| S6 | 01/09 – 07/09 | **E1 — MLP tabular** treinada e sintonizada | ⬜ |
| S7 | 08/09 – 14/09 | **E2 — LSTM/GRU** por produtor | ⬜ |
| S8 | 15/09 – 21/09 | Tabela comparativa final; **decisão de admissão** | ⬜ |
| S9 | 22/09 – 29/09 | Relatório da matéria; seção de método e resultados do artigo | ⬜ |

**Folga proposital:** E3 é opcional e ocupa a folga de S8. Se S4 revelar que a
correção do conjunto de features é mais trabalhosa que o previsto, **E3 é a primeira
coisa a cair** — nunca a sintonia ou as 5 sementes, que são o que garante a validade.

---

## 8. Entregáveis (critério de conclusão — §7 do mestre)

- [ ] `experimentos/rna/` — script/notebook **reprodutível** (semente fixa, mesmo split, `requirements` próprio).
- [ ] **Relatório de ablação** (A1 e A2) com impacto em MAE quantificado.
- [ ] **Tabela comparativa** MLP × LSTM/GRU × XGBoost × baseline, por MAE, média ± desvio de 5 sementes.
- [ ] **Decisão de admissão** registrada e justificada (entra no produto ou permanece experimento).
- [ ] Seção de método e resultados redigida para `artigo.md`.
- [ ] Registro em `REGISTRO.md`.

---

## 9. Riscos específicos desta matéria

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| RNA-1 | Rede neural não supera o XGBoost | Baixo | **É o resultado esperado** (R3 do mestre). Protocolo pré-registrado converte isso em achado, não em frustração. |
| RNA-2 | Ablação revela que o ganho de 22,5 % cai bastante | Médio | É exatamente o que SP1 pergunta. Reportar o número corrigido e explicar a diferença — **antes** que a banca o encontre. |
| RNA-3 | Base sintética impõe teto: o modelo aprende o gerador | Alto | Discutir como ameaça à validade; usar os dados reais já registrados no projeto como verificação parcial **apenas se** houver dado de volume (hoje **não há** — ver §10). |
| RNA-4 | Custo computacional de LSTM por produtor | Médio | Amostrar subconjunto de produtores; documentar o critério de amostragem. |
| RNA-5 | Sintonia assimétrica enviesar a comparação | Alto | Orçamento idêntico para os dois modelos (§5.1.6), fixado antes de rodar. |

---

## 10. Premissas a confirmar

1. **Ementa da matéria** (Cristiano) — indisponível. Se ele exigir implementação de rede
   *from scratch* (retropropagação manual), isso entra como **E0** didático, sem alterar
   a trilha E1–E3. **[premissa a confirmar]**
2. **Dados reais já registrados no projeto** (uma propriedade; identificação em
   `dados_reais/`, **fora do versionamento** por conter PII) — hoje contêm **apenas
   qualidade** (CCS, CBT, gordura, proteína; 13 coletas, set/2024–abr/2026), **sem
   volume/litros**. Portanto **não** servem para validar o target de coleta. Reportar
   como limitação, não como mitigação executada. Muda se dados de volume forem obtidos.
3. **Definição de "produtor novo"** para o teste de cold start (A2) — precisa de critério
   (produtor ausente do conjunto de treino) e de contagem no split atual.
4. ~~**Alvo da comparação: `artefatos_teste` ou `artefatos_validacao`?**~~ ✅
   **Resolvido em 05/08/2026 — `artefatos_teste` é o artefato canônico**, confirmado por
   três fontes concordantes:
   1. É o `ARTEFATOS_DIR` padrão do script de treino (`treino_mvp_avancado.py:30`);
   2. É o padrão do backend (`backend/app.py:47`:
      `os.environ.get("MVP_ARTEFATOS_DIR", "artefatos_teste")`);
   3. **É o que a produção realmente serve** — `/health` na Railway retorna
      `"artefatosDir": "artefatos_teste"`, ou seja, a variável de ambiente **não** está
      sobrescrita no deploy.

   Portanto **MAE 24,45 / ganho de 22,5 % são os números corretos** a citar.
   **Consequência que precisa ficar registrada:** o modelo servido em produção é
   exatamente o treinado **com** `fornecedor_cpf_cnpj` e `fornecedor_nome_razao_social`
   como features one-hot. O achado **A2 não é hipotético — está no ar** (ver §4.A2).

---

## 11. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**.

| Autor | Papel nesta matéria |
|---|---|
| **Matheus Iverson** — dados/modelagem | **Condução técnica**: ablações, treino, sintonia, tabela comparativa |
| **Fagner Vieira** — negócio/produto | Critério de admissão, decisão de produto, redação do relatório |
| **Daianne Valéria** — produto/UX | Leitura de resultado sob a ótica do usuário (o que MAE de 24 L significa para o técnico de campo) |

**Maria Vitória e Diego Santana não participam do Projeto Integrador** e **não são
coautores** desta ou de qualquer entrega acadêmica. Atuam exclusivamente na Maratona
SENAR Goiás.

**Convenção de commit:** `acad(rna): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

_Documento da matéria de RNA — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §11)._
