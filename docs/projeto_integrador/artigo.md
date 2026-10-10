# Artigo científico — Projeto Integrador 2026-2

> **Entregável transversal.** Não pertence a uma matéria: consolida SP1 (RNA), SP2 (PLN)
> e SP3 (IA Generativa) sob a pergunta central (§11 do mestre).
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Prazo que vale: 12/12/2026** (apresentação de banca) — **não** 15/12.
> **Data de referência:** 05/08/2026
>
> Este é o **plano do artigo**, não o artigo. Define contribuição, método,
> reprodutibilidade, ameaças à validade, estrutura e calendário de escrita. O texto
> final nasce em `docs/projeto_integrador/artigo/`.

---

## 1. O problema de calendário — e por que ele define tudo

O calendário é o inimigo do artigo, e é melhor encará-lo agora:

| Resultado | Fica pronto em |
|---|---|
| SP1 (RNA) | 29/09 |
| SP2 (PLN) | 29/09 |
| **SP3 (IA Generativa)** | **30/11** (S8 de `ia_generativa.md`) |
| **Apresentação de banca** | **12/12** |

**Entre o último resultado e a banca há 12 dias.** Escrever um artigo inteiro em 12 dias,
no mesmo período em que a Extensão executa o piloto de campo, não acontece.

**Consequência de método, adotada aqui:** o artigo é escrito **por partes, à medida que
cada bloco fecha**, e não ao final. As seções que não dependem de resultado —
introdução, trabalhos relacionados, método, ameaças à validade — são escritas **entre
agosto e setembro**, enquanto RNA e PLN correm. Em dezembro entra **apenas** o que só
pode existir em dezembro: os números de SP3, a discussão integrada e a conclusão.

> Escrever o método **antes** de ver os resultados não é só logística: é o que impede a
> narrativa de ser construída em torno do que deu certo. O protocolo de RNA já é
> pré-registrado (`rna.md` §5) pela mesma razão. **O artigo herda essa disciplina.**

---

## 2. Contribuição pretendida — o que é novo

O trabalho **não** contribui com arquitetura de modelo nem com algoritmo. Contribui com
uma **resposta metodológica** a uma situação comum e mal documentada: *sistemas de apoio
à decisão construídos sobre substrato majoritariamente sintético, que já estão em
produção.*

Três contribuições, em ordem de força:

### C-1 — Estratificação da confiança por camada (principal)

A tese central: **em um sistema de IA multicamada com dados majoritariamente sintéticos,
a confiabilidade não é uniforme — ela varia com a origem do substrato de cada camada, e
não com a sofisticação do método.**

| Camada | Substrato de evidência | Garantia que oferece |
|---|---|---|
| Conhecimento normativo (SBC) | **Real** — IN 76/77, público, verificável | Auditável; funciona para produtor **novo** (dia 1) |
| Geração ancorada (RAG) | **Real** — o mesmo corpus normativo | Verificável contra a fonte; é onde SP3 mede |
| Entrada em linguagem natural (PLN) | **Misto** — treino sintético, **teste real** | A diferença entre os dois conjuntos **é** o resultado |
| Aprendizado supervisionado (RNA/XGB) | **Sintético** | Mede-se o ganho sobre baseline; o teto é o gerador |

O resultado esperado — e a inversão que dá interesse ao trabalho — é que a camada
**menos sofisticada** (regras normativas) é a que oferece **mais garantia**, porque seu
substrato é real; e a camada mais sofisticada (aprendizado supervisionado) é a que
oferece **menos**, porque em parte aprende o próprio gerador. **Isso contraria a
intuição de que mais aprendizado significa mais confiança.**

### C-2 — Protocolo de auditoria de sistema em produção

O trabalho auditou o próprio produto e produziu **12 achados verificados**
(A1–A3, C1–C6, G1–G3), cada um com evidência reproduzível: execução sobre 54.780 linhas,
consulta à API de produção, leitura de código com arquivo e linha. Três exemplos do que
o protocolo encontra e uma leitura superficial não encontraria:

- **C1** — a metade superior da escala de risco nunca é atingida (máx. 49,40 de 100);
- **G2** — a camada de recomendação específica existe, é testada em demo e **não está
  ligada** ao produto;
- **G3** — **dois** motores de risco coexistem com escalas diferentes, e o que gera os
  planos de ação não é o que a documentação descrevia.

A contribuição não são os achados em si — é o **método** que os produz, replicável por
outra equipe sobre outro sistema aplicado.

### C-3 — Caso documentado de cadeia leiteira brasileira

Aplicação em domínio com literatura escassa em português, com limiares ancorados em IN
76/77 e dados climáticos reais (INMET). Contribuição menor, mas é o que dá ao artigo
veículo natural (§8).

> **O que o trabalho explicitamente NÃO reivindica:** superioridade de modelo, ganho
> generalizável para outras cadeias produtivas, ou validação clínica/sanitária das
> recomendações. Reivindicar qualquer um deles com esta base seria desonesto — e a
> primeira coisa que uma banca derruba.

---

## 3. Pergunta e subperguntas

Reproduzidas do mestre §11, sem alteração — se mudarem lá, mudam aqui.

> **Central:** Como construir e avaliar a confiabilidade de um sistema de apoio à decisão
> baseado em IA para a cadeia leiteira quando o substrato de dados é majoritariamente
> sintético — que garantias cada camada consegue oferecer, e quais permanecem fora de
> alcance?

| # | Subpergunta | Matéria | Métrica | Resultado em |
|---|---|---|---|---|
| SP1 | Ganho real do aprendizado supervisionado sobre o baseline, e o teto em base sintética | RNA | MAE: NN × XGBoost × baseline, 5 sementes | 29/09 |
| SP2 | Fidelidade da conversão mensagem livre → lançamento estruturado | PLN | F1 intenção, F1 NER, taxa de lançamento correto | 29/09 |
| SP3 | A ancoragem normativa via RAG reduz alucinação e aumenta aderência? | IA Gen | M1–M8, 4 braços | 30/11 |

**SP3 é o núcleo experimental.** SP1 é a âncora de honestidade. SP2 sustenta a
viabilidade da entrada de dados. A Extensão entra como **validade externa**, não como
subpergunta (§10.2).

---

## 4. Método consolidado

O detalhe vive em cada documento de matéria; aqui ficam os **invariantes que valem para
o artigo inteiro** e que a banca vai cobrar.

### 4.1 Invariantes

1. **Split temporal, nunca aleatório** — treino < 2024, validação 2024, teste ≥ 2025.
2. **Sementes `[42, 43, 44, 45, 46]`**, resultado como **média ± desvio-padrão**.
3. **Conjunto de teste aberto uma única vez por modelo**, ao final.
4. **Orçamento de sintonia simétrico** entre modelos comparados (30 configurações).
5. **Baseline descrito com precisão:** MM7 **com fallback em cascata** para MM30 e para
   `producao_media_esperada_litros_dia` — **não** é naïve nem persistência. A cascata o
   torna mais forte, e o ganho de 22,5 % mais conservador. **Omiti-la subvende o próprio
   resultado.**
6. **Métrica principal é o ganho sobre o baseline**, nunca o R² absoluto — R² 0,994 com
   baseline em 0,990 não é conquista, e citá-lo como tal é o erro mais fácil de cometer.

### 4.2 Números canônicos verificados (partida)

| Medida | Valor | Fonte |
|---|---|---|
| MAE teste (XGBoost) | **24,45 L** | `artefatos_teste/metricas_modelo.json` |
| MAE teste (baseline) | **31,54 L** | idem |
| **Ganho** | **22,5 %** | idem |
| RMSE | 36,86 vs 48,57 | idem |
| Linhas treino/validação/teste | 32.010 / 10.980 / 10.920 | idem |
| Features | 133 | idem |
| Baseline de geração de plano | **3 textos distintos / 30 produtores; 42 % sem ação** | API de produção, 05/08/2026 |

`artefatos_teste` é o artefato **canônico** — confirmado por padrão do script, padrão do
backend e pelo `/health` da Railway.

### 4.3 Avaliação humana (SP2 e SP3)

Onde há julgamento humano — anotação de corpus (SP2) e avaliação de alucinação (SP3) —
vale a mesma regra: **dupla avaliação independente, concordância reportada**
(Kappa de Cohen em SP2), discordância resolvida por terceiro. Sem esse número, a
qualidade é afirmação, não evidência.

---

## 5. Reprodutibilidade

Checklist que acompanha a submissão:

- [ ] **Sementes e splits** declarados e fixos no código;
- [ ] **Versões** de Python e de todas as bibliotecas relevantes;
- [ ] Para SP3: **modelo, versão, temperatura e *prompts* versionados** — sem isso o
      resultado não é reproduzível nem por nós mesmos daqui a três meses;
- [ ] **Procedência do corpus normativo** (fonte, data de acesso, versão do documento);
- [ ] Scripts de treino e avaliação em `experimentos/`, com `requirements` próprio;
- [ ] **O que não pode ser publicado, declarado como tal**: o corpus real de fala de
      produtor (PII) e os dados reais de fazenda (`dados_reais/`, fora do versionamento)
      **não** acompanham o artigo. Publicam-se o esquema, as estatísticas agregadas e o
      procedimento — não o dado.

> **Ponto forte inesperado:** a base sintética é *gerável*. `gerador_leite_sintetico.py`
> está no repositório público — qualquer revisor pode **regenerar a base e refazer SP1**.
> Poucos trabalhos aplicados oferecem isso. O que é a maior limitação do trabalho é,
> para reprodutibilidade, uma vantagem — e vale dizer isso explicitamente.

---

## 6. Ameaças à validade

Seção obrigatória, e a que mais distingue o trabalho. É aqui que os 12 achados entram
como **método**, não como confissão.

### 6.1 Validade interna

| Ameaça | Origem | Tratamento no artigo |
|---|---|---|
| Identificadores como *features* (CPF, razão social) permitem memorização por indivíduo | **A2** | Protocolo de SP1 exclui identificadores; ablação quantifica. Declarar que o **modelo em produção** os usa |
| Convenção temporal inconsistente em 2 *features* | **A1** | Ablação mede a magnitude; declarar que **não** é vazamento de futuro, é inconsistência |
| Hiperparâmetros nunca sintonizados; validação nunca usada para seleção | **A3** | Protocolo §4.1 corrige: orçamento simétrico, validação para seleção, teste aberto 1×  |
| Ganho do RAG confundido com ganho de código já existente | **G2** | Braço **B1** isola |
| Pesos do score sem proveniência documentada | **C4** | Declarar como escolha de projeto; análise de sensibilidade |
| Dimensões do score não são independentes (CCS ≥ 600k dispara 3 delas, 45/100) | **C2** | Declarar a sobreposição; não apresentar como 7 evidências independentes |

### 6.2 Validade externa

| Ameaça | Tratamento |
|---|---|
| **Base majoritariamente sintética** — o modelo aprende, em parte, o gerador | É a **condição da pergunta central**, não um defeito escondido. Reportar ganho sobre baseline; discutir o teto |
| **Escala da metade morta do score** (máx. 49,40; zero Alto risco) | **C1** — declarar que o diagnóstico (calibração × gerador saudável demais) está **em aberto**, com as duas hipóteses e suas correções opostas |
| Piloto de campo pode não se materializar | Contingência do mestre §11: SP1–SP3 permanecem intactas; perde-se validade externa, reportada como limitação |
| Um único produto, uma cadeia, uma região | Declarar o escopo; C-1 é proposta como **hipótese transferível**, não como lei |
| Dados reais disponíveis são de **qualidade**, sem volume | Não permitem validar o modelo preditivo (que exige produção diária). Declarar |

### 6.3 Validade de construto

- **"Alucinação" precisa de definição operacional** antes de virar número. Adotada:
  *proporção de afirmações verificáveis que contradizem o corpus ou os indicadores do
  produtor* — unidade é a **afirmação**, não o texto (`ia_generativa.md` §7).
- **"Plano de ação" idem:** o baseline chama de plano um texto que manda observar. A
  métrica de **acionabilidade** (M6) existe porque o construto não é auto-evidente.
- **Constantes econômicas embutidas no código** (**C5**) — preço, bônus e penalidade
  envelhecem em silêncio; qualquer impacto em reais reportado no artigo herda isso.
  Declarar data e origem dos valores.

### 6.4 Validade de conclusão

Execução única, sem estimativa de variância, é o erro mais fácil (**A3**). O protocolo de
5 sementes com média ± desvio-padrão e o critério de **intervalos não sobrepostos**
(`rna.md` §6.2) existem para que "modelo A é melhor que B" seja afirmação sustentada, e
não diferença na terceira casa decimal.

---

## 7. Estrutura do artigo

Alvo: **8–12 páginas** em formato de conferência (a ajustar ao veículo, §8).

| § | Seção | Depende de resultado? | Escrever em |
|---|---|---|---|
| 1 | Introdução — problema, contexto da cadeia leiteira, pergunta central | ❌ | **ago/set** |
| 2 | Trabalhos relacionados — predição em pecuária leiteira, SBC em agro, RAG em domínio normativo, dados sintéticos | ❌ | **ago/set** |
| 3 | O sistema — arquitetura em 4 camadas, o que já existia | ❌ | **ago/set** |
| 4 | Método — invariantes, protocolo por subpergunta, avaliação humana | ❌ | **ago/set** |
| 5 | SP1 — aprendizado supervisionado e seu teto | ✅ | out |
| 6 | SP2 — entrada em linguagem natural | ✅ | out |
| 7 | **SP3 — geração ancorada (núcleo)** | ✅ | **dez** |
| 8 | Discussão integrada — estratificação da confiança (C-1) | ✅ | **dez** |
| 9 | **Ameaças à validade** | ❌ | **ago/set** |
| 10 | Conclusão e trabalhos futuros | ✅ | dez |

**Seis das dez seções não dependem de resultado nenhum e podem estar prontas em
setembro.** É a diferença entre um artigo escrito e um artigo apressado.

---

## 8. Veículo-alvo

**[premissa a confirmar]** — prazos de submissão variam a cada edição e **não devem ser
assumidos**; confirmar nos sites oficiais antes de fixar calendário.

| Prioridade | Veículo | Aderência |
|---|---|---|
| **P1** | **SBIAgro** — Congresso Brasileiro de Agroinformática | Melhor encaixe: agro + computação, comunidade brasileira, aceita relato aplicado com limitações declaradas |
| P2 | **ENIAC** (Encontro Nacional de Inteligência Artificial e Computacional, SBC) | IA aplicada; aceita trabalho de graduação com método sólido |
| P3 | Revista Brasileira de Computação Aplicada (RBCA) | Periódico, sem prazo de evento — **rede de segurança** se nenhum congresso encaixar no calendário |
| P4 | Anais do próprio SENAI FATESG / evento interno | Garantia mínima de veículo |

> **Regra:** o artigo é escrito para ser **submetível**, não necessariamente submetido
> até 12/12. O entregável do PI é o artigo pronto; a submissão segue o calendário do
> veículo, que pode cair depois. **Não travar a entrega esperando janela de congresso.**

---

## 9. Separação acadêmico × comercial

Restrição 2 do mestre §8, e a mais fácil de violar por descuido:

| Vai para o artigo | **Não** vai para PITCH / PLANO_DE_NEGÓCIO / SENAR / investidor |
|---|---|
| Base majoritariamente sintética | — |
| C1: metade da escala de risco nunca acende | — |
| A2: CPF como *feature* em produção | — |
| Resultados negativos (ex.: NN não superar XGBoost) | — |
| Ganho de 22,5 %, com a cascata do baseline descrita | O PITCH pode citar o ganho; **sem** inverter o sinal das limitações |

**O vazamento perigoso é o inverso:** linguagem de *pitch* entrando no artigo
("solução inovadora", "revolucionar a cadeia leiteira"). A banca pune isso mais do que
pune limitação declarada.

---

## 10. Dependências e riscos

### 10.1 Dependências externas

| Dependência | Prazo | Se falhar |
|---|---|---|
| **Coleta de fala real** (SP2) | **31/08** | Conjunto real vira análise qualitativa sem F1; §6 do artigo declara a limitação (**risco PLN-1**) |
| Corpus normativo (SP3) | 19/10 | **Não depende de terceiro** — só de execução |
| Piloto de campo (Extensão) | 30/09 (marco de decisão) | §10.2 |
| Revisão veterinária de M7 (SP3) | — | M7 vira limitação declarada; sem ela, não há admissão ao produto |

### 10.2 Se a Extensão não acontecer

**O artigo não muda.** A Extensão está deliberadamente fora das subperguntas: perde-se a
seção de validade externa, que passa a limitação declarada. Nenhuma seção precisa ser
reescrita. Essa é a razão de o desenho ter sido feito assim.

### 10.3 Riscos do próprio artigo

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| ART-1 | **Resultados de SP3 chegam 30/11, banca em 12/12** | **Alto** | §7: seis seções escritas até setembro; dezembro só recebe números |
| ART-2 | Nenhum resultado positivo em nenhuma subpergunta | Médio | C-1 e C-2 **não dependem** de resultado positivo. Uma estratificação em que tudo é fraco ainda responde a pergunta central |
| ART-3 | Escopo de 3 subperguntas estourar 12 páginas | Médio | SP3 é o núcleo; SP1 e SP2 podem comprimir para 1 página cada, com detalhe nos documentos de matéria |
| ART-4 | Linguagem de *pitch* vazar (§9) | Médio | Revisão dedicada antes da entrega |
| ART-5 | Trabalhos relacionados fracos (literatura escassa em pt-BR) | Médio | Buscar em inglês (*dairy yield prediction*, *RAG regulatory compliance*); declarar a escassez |
| ART-6 | Premissa **"Gonçalves (2025)"** citada no briefing e **não encontrada** no repositório | Baixo | Confirmar ou remover — **não citar referência não verificada** |

---

## 11. Calendário de escrita

| Período | Entrega | Depende de |
|---|---|---|
| **ago** | §1 Introdução, §3 O sistema | nada |
| **set** | §2 Trabalhos relacionados, §4 Método, **§9 Ameaças** | nada |
| **29/09** | Resultados de SP1 e SP2 fecham | RNA, PLN |
| **out** | §5 SP1, §6 SP2; primeira versão completa **menos** SP3 | resultados de set |
| **30/11** | Resultados de SP3 fecham | IA Gen S8 |
| **01–07/12** | §7 SP3, §8 Discussão, §10 Conclusão | SP3 |
| **08–10/12** | Revisão integral: consistência numérica, §9 (vazamento de *pitch*), referências | — |
| **12/12** | **Artigo pronto + apresentação de banca** | — |

**O marco real é 30/09**, não dezembro: se as seções independentes de resultado não
estiverem prontas no fim do Bloco 1, ART-1 se materializa e não há como recuperar.

---

## 12. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**. **A autoria do artigo é dos três**, na ordem a definir
por contribuição de escrita.

| Autor | Papel no artigo |
|---|---|
| **Fagner Vieira** — negócio/produto | §1 Introdução, §3 O sistema, §9 Ameaças, revisão de separação acadêmico × comercial, submissão |
| **Matheus Iverson** — dados/modelagem | §4 Método, §5 SP1, §7 SP3 (resultados), reprodutibilidade |
| **Daianne Valéria** — produto/UX | §2 Trabalhos relacionados, §6 SP2, §8 Discussão, protocolo de avaliação humana |

**Maria Vitória e Diego Santana não são coautores do artigo** nem de qualquer entregável
acadêmico. Atuam exclusivamente na Maratona SENAR Goiás. Contribuições que toquem o
produto (validação sanitária; arquitetura/IoT) entram na seção de **agradecimentos**,
como contribuição externa creditada nominalmente — **nunca na autoria**.

**Convenção de commit:** `acad(artigo): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

_Plano do artigo científico — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §12)._
