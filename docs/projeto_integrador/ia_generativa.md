# Inteligência Artificial Generativa — Projeto Integrador 2026-2

> **Matéria:** Inteligência Artificial Generativa · **Professor:** Raphael
> **Janela:** 06/10 – 15/12/2026 (Bloco 2) · **Encontros:** Qui (4 blocos) + Ter 20:45–22:45
> **Subpergunta que esta matéria responde:** **SP3** (§11 do documento mestre)
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Data de referência:** 05/08/2026 (documento escrito no Bloco 1, antes da matéria abrir)

---

## 1. Objetivo

Responder **SP3**:

> *A ancoragem em fonte normativa (IN 76/77) via RAG reduz alucinação e aumenta aderência
> frente à geração não ancorada?*

Operacionalmente: dado o score de risco de um produtor e seus indicadores, **gerar o
plano de ação** — hoje servido por `/action-plans` — a partir de recuperação em corpus
normativo, e medir se a ancoragem melhora o texto frente a duas alternativas: o gerador
de regras que já está em produção e um LLM sem recuperação.

**SP3 é o núcleo experimental do artigo** (§11 do mestre) por um motivo que esta matéria
precisa honrar: é a única camada cujo substrato de evidência é **real**. A base de
produção é sintética; a IN 76/77 e o material técnico da Embrapa existem, são públicos e
são verificáveis. É onde o trabalho produz resultado que não depende do gerador.

---

## 2. Ficha de admissão (§4 do mestre)

| Teste | Resposta |
|---|---|
| **1. Não-prejuízo** | ✅ **Atende, com condição.** Trabalho isolado em `experimentos/iagen/`, com `requirements` próprio — hoje o `requirements.txt` do projeto **não tem** nenhuma dependência de LLM, vetorial ou de *embeddings* (verificado). A integração ao produto, se ocorrer, entra **atrás de flag**, como **origem de plano adicional** (`origem_plano: "IA"`), preservando `origem_plano: "Sugestão"` e `"Manual"` intactos. Desligar a flag devolve o comportamento atual sem cicatriz. |
| **2. Agregação de valor** | ✅ **Forte, e mensurável.** O gerador atual produz **3 textos distintos para 30 produtores** (§3, medido em produção). O valor não é hipotético: é a diferença entre um plano genérico e um plano específico, com um baseline já quantificado contra o qual comparar. |

> ⚠️ **Condição adicional, não negociável:** nenhum dado pessoal de produtor sai do
> ambiente para uma API de terceiro. Ver §8.3.

---

## 3. O que existe hoje — o baseline **medido**, não suposto

Diferente de PLN (onde faltava corpus) e de RNA (onde havia modelo), esta matéria começa
com algo raro: **o baseline já está no ar e pode ser medido antes de escrever uma linha
de código**. Foi o que se fez.

**Como o plano é gerado hoje.** `gerar_recomendacao()`
(`fornecedor_inteligencia.py:32`) percorre 5 condições booleanas e concatena as frases
fixas correspondentes:

| Condição | Frase emitida |
|---|---|
| `risco_queda_pct ≥ 25` ou `tendencia_volume_pct ≤ -8` | "priorizar contato de campo para proteger volume" |
| `ccs_media ≥ 500` ou `cbt_media ≥ 180` ou `taxa_reprovacao_pct ≥ 1` | "abrir plano de qualidade e verificar manejo, ordenha e tanque" |
| `taxa_descarte_pct ≥ 3` | "investigar descarte e perdas antes da coleta" |
| `taxa_falha_pct ≥ 2` | "revisar rota, janela de coleta e acesso em dias de chuva" |
| `risco_churn_pct ≥ 1` | "acionar retenção comercial" |
| *nenhuma* | "Manter acompanhamento regular e reforçar boas práticas." |

O texto final é `"; ".join(motivos)`. O teto combinatório é 2⁵ = 32 textos possíveis.

### 3.1 Medição em produção (05/08/2026, API Railway)

| Medida | Valor |
|---|---|
| Fornecedores servidos por `/suppliers` | **30** |
| Textos de recomendação **distintos** entre os 30 | **3** |
| Planos em `/action-plans` | **12** |
| Descrições **distintas** entre os 12 planos | **3** |
| Planos cuja descrição é *"Manter acompanhamento regular e reforçar boas práticas"* | **5 de 12 (42 %)** |

> **Cinco dos doze "planos de ação" não contêm ação.** Dizem para continuar
> observando. Esse é o baseline honesto contra o qual a geração ancorada será medida —
> e ele já dá à matéria uma justificativa de produto que não depende de argumento
> acadêmico.

### 3.2 Dois achados de produto encontrados na medição

**G1 — o corte de planos sugeridos é truncado em 12, silenciosamente.**
`_build_suggested_action_plans()` (`backend/app.py:479`) termina em `return plans[:12]`.
Na base atual, **14 fornecedores são elegíveis e 12 planos são gerados** — dois produtores
elegíveis somem sem aviso, sem log e sem ordenação por gravidade (a lista não é ordenada
por risco antes do corte, então quem cai fora é acidente de iteração, não decisão). Para
uma cooperativa com centenas de produtores, o comportamento é o mesmo: 12.
**Estado: 🔴 aberto.** Não é achado desta matéria — é defeito de produto encontrado por
ela, e vai para o `REGISTRO.md` como tal.

**G2 — a camada de "COMO agir" existe e não está ligada ao produto.**
`perfil/classificador_perfil.py` tem `RECEITAS` (leitura, ação, investimento por perfil)
e `recomendacao_combinada()`, cujo *docstring* declara: *"Esta é a entrega de valor:
recomendação cirúrgica em vez de genérica."* **O backend não importa esse módulo**
(verificado: nenhuma referência a `classificador_perfil` em `backend/`). O único
consumidor é `perfil/perfil_demo.py`. Ou seja: a recomendação cirúrgica está escrita,
testada em demo, e **não chega ao usuário** — o que chega é o `"; ".join()` da §3.
**Estado: 🔴 aberto.**

> G2 tem consequência direta para esta matéria: **parte do ganho que se atribuiria ao
> RAG pode ser obtido só ligando o que já existe.** O desenho experimental precisa
> isolar isso, ou o resultado fica contaminado. Ver §6, braço **B1**.

---

## 4. O achado estrutural: **existem dois motores de risco, e o plano usa o outro**

Este é o achado mais importante do documento, e ele muda o enunciado operacional de SP3.

O mestre (§5) e `ia.md` descrevem o motor de risco como `score_risco.py` — 7 dimensões
ponderadas, limiares IN 77, o sistema baseado em conhecimento formalizado na matéria de
IA e auditado nos achados C1–C6. **Não é esse o motor que gera os planos de ação.**

| | `score_risco.py` | `fornecedor_inteligencia.py` |
|---|---|---|
| Campo | `score_via_leite` | `score_risco_fornecedor` |
| Composição | 7 dimensões ponderadas (soma 100) + THI + queda | 4 dimensões: volume 0,35 · qualidade 0,30 · logística 0,20 · continuidade 0,15 |
| Faixas | bins até 101 (C3: `NaN` acima) | ≥ 75 Alto · ≥ 50 Médio · < 50 Baixo |
| Alcance real medido | **máx. 49,40** — metade superior morta (**C1**) | **máx. 76,2** — atinge "Alto" |
| Quem consome | **`/risk-radar`** (linhas 217–229, 1084) | **`/suppliers`** → **`/action-plans`** (linha 327) |
| Formalizado em `ia.md`? | ✅ sim | ❌ **não** |

Ambos são importados por `backend/app.py` (linhas 15–16) e **coexistem com escalas e
cortes diferentes**. O radar de risco e o plano de ação do mesmo produtor respondem a
dois cálculos distintos.

**Três consequências:**

1. **O enunciado de SP3 precisa ser preciso.** "Gerar o plano de ação a partir do score"
   é ambíguo enquanto houver dois. **Decisão desta matéria: o experimento parte de
   `score_risco_fornecedor`**, porque é o que efetivamente alimenta `/action-plans` — a
   alternativa seria trocar o motor e a matéria deixaria de medir o produto real.
2. **C1 não invalida esta matéria.** A metade morta da escala é do `score_via_leite`; o
   motor que alimenta os planos alcança 76,2 e classifica "Alto". Os dois achados são
   verdadeiros e **não** se contradizem — são motores diferentes. Registrar isso evita
   uma conclusão errada na banca.
3. **A duplicação em si é achado de produto (G3).** Dois motores de risco não
   documentados como tais, com cortes diferentes, é dívida arquitetural. **Estado: 🔴
   aberto** — fora do escopo de correção desta matéria, dentro do escopo de registro.

---

## 5. O corpus normativo **também não existe no repositório** — mas a diferença importa

Levantamento feito (`grep` por "IN 77", "instrução normativa" em `.py`, `.md`, `.json`,
`.txt`; busca por PDF em todo o repositório):

| Fonte | O que há |
|---|---|
| `score_risco.py`, `perfil/classificador_perfil.py` | **Limiares numéricos** atribuídos à IN 76/77 — nenhum texto normativo |
| `docs/*.md`, `README.md` | **Citações** à IN 76/77 em prosa |
| PDFs no repositório | Apenas material próprio (plano de negócio, pitch, identidade visual) |
| Texto oficial da IN 76 ou IN 77 | ❌ **ausente** |

**Mas o contraste com PLN é o ponto:**

| | PLN (SP2) | IA Generativa (SP3) |
|---|---|---|
| Corpus existe no repo? | ❌ não | ❌ não |
| Corpus **é obtenível**? | ❌ Depende de terceiro (produtor disponível, consentimento, campo) | ✅ **Sim** — documento público do MAPA, mais Embrapa e material técnico |
| Prazo crítico | **31/08**, insubstituível | Nenhum — pode ser montado a qualquer momento |
| Risco de não existir | **Alto (PLN-1)** | Baixo |

> Por isso SP3 é o núcleo experimental e SP2 é a dependência frágil. **A ancoragem de
> SP3 não depende de ninguém aceitar um convite.** Essa assimetria é resultado
> metodológico e entra no artigo: em um projeto com substrato majoritariamente
> sintético, a camada que mais oferece garantia é a que se ancora em fonte pública
> verificável — não a que mais aprende com os dados.

### 5.1 Escopo do corpus (a montar na S2)

Ordem de prioridade, com procedência registrada por documento (fonte, data de acesso,
versão, jurisdição):

1. **IN 77/2018 (MAPA)** — obrigatória, é o que o produto já invoca;
2. **IN 76/2018 (MAPA)** — obrigatória, base do classificador de perfil;
3. **Material técnico Embrapa Gado de Leite** sobre mastite, CCS, CBT, ordenha, resfriamento;
4. **Manuais de boas práticas** de ordenha e qualidade do leite.

> ⚠️ **C6 fica no caminho.** `ia.md` registra que limiares rotulados "IN 77" no código são
> **mais estritos que a norma**. Montar este corpus **resolve C6 de passagem**: com o texto
> oficial em mãos, cada limiar pode ser marcado `[normativo]` ou `[escolha de projeto]`.
> **É a primeira entrega útil desta matéria para o produto**, e ela acontece na S2, antes
> de qualquer geração.

---

## 6. Desenho experimental — **três braços, não dois**

SP3 pergunta "ancorado × não ancorado". Medir só isso seria incompleto, porque o produto
não tem hoje um LLM não ancorado — tem **regras**. E, por G2, tem regras melhores
desligadas. O desenho usa quatro braços, avaliados sobre o **mesmo conjunto de produtores**:

| Braço | O que é | Papel |
|---|---|---|
| **B0** | `gerar_recomendacao()` como está em produção | **Baseline honesto.** 3 textos distintos, 42 % sem ação (§3.1) |
| **B1** | Regras + `RECEITAS` do classificador de perfil (G2 ligado) | **Controle.** Isola quanto do ganho é só ligar o que existe |
| **B2** | LLM **sem** recuperação — score e indicadores no *prompt* | Braço "não ancorado" de SP3 |
| **B3** | **LLM + RAG** sobre o corpus normativo (§5.1) | Braço "ancorado" de SP3 |

**A comparação que responde SP3 é B3 × B2.** As comparações B2 × B0 e B3 × B1 são o que
torna o resultado defensável como contribuição de produto, e não só de ementa.

> **B1 é o braço que protege a honestidade do trabalho.** Sem ele, um ganho de B3 sobre
> B0 seria atribuído ao RAG quando parte dele vem de código que já estava escrito. Essa é
> a mesma disciplina de RNA (comparar contra baseline forte, não contra espantalho) e o
> mesmo espírito da §8.1 do mestre.

---

## 7. Métricas — como se mede alucinação sem enganar a si mesmo

Avaliação sobre uma **amostra fixa de 30 produtores** (a base servida hoje), com os
quatro braços gerando para os mesmos casos. Julgamento por **dupla avaliação
independente**, com discordância resolvida por terceiro — a mesma disciplina de Kappa
adotada em PLN §5.

| # | Métrica | Definição operacional | Braços |
|---|---|---|---|
| **M1** | **Taxa de alucinação** | Proporção de afirmações verificáveis que **contradizem** o corpus ou os indicadores do produtor. Unidade = afirmação, não texto | B2, B3 |
| **M2** | **Aderência à fonte** | Proporção de afirmações normativas **rastreáveis** a um trecho recuperado | B3 (B2 por construção = 0) |
| **M3** | **Cobertura de citação** | Proporção de recomendações que citam o dispositivo aplicável | B2, B3 |
| **M4** | **Especificidade** | Textos distintos ÷ produtores. **Baseline medido: 3/30 = 0,10** | todos |
| **M5** | **Fidelidade ao indicador** | O texto reflete os indicadores reais do produtor? (CCS alto → fala de CCS) | todos |
| **M6** | **Acionabilidade** | O plano diz **o que fazer**, com responsável e prazo — ou só manda observar? Baseline: **58 %** acionáveis | todos |
| **M7** | **Erro crítico** | Recomendação sanitária **incorreta ou perigosa** (§7.1) | todos |
| **M8** | **Custo e latência** | R$/plano e segundos/plano | B2, B3 |

### 7.1 M7 é a métrica que decide a admissão

A lição de PLN §6.1 vale aqui, mais forte: **nem todo erro custa o mesmo.**

- Um plano vago ("manter acompanhamento") é **inútil** — custo baixo, é o que já se tem.
- Um plano **específico e errado** — recomendar carência de antibiótico errada, indicar
  descarte quando não é caso, ou omitir descarte quando é — tem custo **sanitário,
  econômico e potencialmente legal**. O produtor pode agir sobre ele.

**Gerar texto convincente é exatamente o que um LLM faz bem.** É a diferença entre um
sistema inútil e um sistema perigoso, e ela precisa estar declarada antes do primeiro
*prompt*, não descoberta na banca.

**Consequências de projeto (espelham o limiar de recusa de PLN §6.1):**

1. **Recusa explícita.** Sem trecho recuperado acima do limiar de similaridade, o sistema
   **não gera** — devolve o plano de regras (B0/B1) e sinaliza. Silêncio ancorado é
   melhor que texto plausível.
2. **Nenhuma dosagem, carência ou prescrição.** O sistema recomenda **procedimento e
   encaminhamento** ("coletar amostra para cultura", "acionar o responsável técnico"),
   nunca conduta veterinária. Fronteira declarada no *prompt* e verificada por guardrail.
3. **Revisão humana antes de chegar ao produtor.** Plano gerado nasce
   `status: "Aberto"`, `origem_plano: "IA"`, e é do gestor da cooperativa — nunca
   entregue direto a produtor sem revisão, no escopo desta matéria.
4. **Marcação de procedência no texto.** O que é norma é citado; o que é sugestão de
   projeto é marcado como tal. É a mesma exigência que C6 impõe ao código.

> **Validação sanitária é contribuição externa.** Maria Vitória (veterinária) atua **só
> na Maratona SENAR** e **não é coautora** (§2 do mestre, §12 deste documento). Se
> revisar clinicamente a amostra de M7, entra como **contribuição externa creditada
> nominalmente** — nunca como autoria. Se não houver revisão veterinária, **M7 é
> reportada como limitação declarada**, e a admissão ao produto não acontece.

---

## 8. Arquitetura e restrições

### 8.1 Isolamento

Tudo em `experimentos/iagen/`, com `requirements` próprio. O produto só é tocado se a
admissão passar, e então **atrás de flag**, como origem adicional de plano.

### 8.2 Escolha de modelo — decisão adiada, critério fixado agora

**[premissa a confirmar — depende da ementa do Raphael.]** O critério não depende dela:
o experimento precisa de **reprodutibilidade** (versão de modelo fixada e registrada,
temperatura fixa, *prompts* versionados) e de **viabilidade de custo** no cenário de
produto. Se a ementa exigir modelo aberto local, o desenho **não muda** — muda o braço
B2/B3 de modelo, e a comparação continua válida.

### 8.3 PII — restrição dura, ligada a A2

O *prompt* **não carrega** nome, CPF/CNPJ ou identificação de propriedade. Envia
**indicadores e score**, com identificador pseudonimizado.

Motivos, nesta ordem: (1) enviar CPF de produtor a uma API de terceiro é tratamento de
dado pessoal sem base legal declarada — **LGPD**; (2) `rna.md` já registra em **A2** que
CPF e razão social são usados como *features* do modelo **em produção**, e esta matéria
**não vai repetir o erro em outra camada**; (3) a regra de PII de `extensao.md` §5 vale
para todo o projeto.

> A restrição também é **de produto**: um sistema que precisa mandar o cadastro do
> produtor para fora é mais difícil de vender a cooperativa do que um que manda
> indicadores anônimos.

### 8.4 Custo e conectividade

`pln.md` §8 abre o gancho: rodar local é vantagem de produto para o campo. Aqui ele
fecha. Plano gerado sob demanda, para produtor em risco, é volume baixo (12–14 hoje) —
mas o custo cresce com a carteira. **M8 mede isso**, e a discussão custo × qualidade ×
soberania do dado é uma das conclusões do artigo, não uma nota de rodapé.

---

## 9. Backlog por sprint (06/10 – 12/12)

**Prazo que vale: 12/12** (apresentação), não 15/12 (§ mestre, cabeçalho).

| Sprint | Período | Entrega | Estado |
|---|---|---|---|
| **S0** | **ago–set (Bloco 1)** | **Baseline medido** (§3.1) e achados G1–G3 registrados — **✅ feito neste documento**, antes de a matéria abrir | ✅ |
| S1 | 06/10 – 12/10 | Ambientação; fechar escolha de modelo (§8.2) contra a ementa | ⬜ |
| S2 | 13/10 – 19/10 | **Corpus normativo montado** (§5.1) com procedência; **C6 conferido de passagem** | ⬜ |
| S3 | 20/10 – 26/10 | Indexação e recuperação; ajuste de segmentação e limiar de similaridade | ⬜ |
| S4 | 27/10 – 02/11 | B1 implementado (ligar `RECEITAS` — G2); amostra de 30 casos congelada | ⬜ |
| S5 | 03/11 – 09/11 | B2 (não ancorado) + *prompts* versionados + guardrails da §7.1 | ⬜ |
| S6 | 10/11 – 16/11 | **B3 (RAG)** — o braço que responde SP3 | ⬜ |
| S7 | 17/11 – 23/11 | **Avaliação cega dos 4 braços**; dupla avaliação; M1–M8 | ⬜ |
| S8 | 24/11 – 30/11 | Análise de erro; revisão sanitária de M7 (se houver); decisão de admissão | ⬜ |
| S9 | 01/12 – 07/12 | Seção do artigo (SP3 = núcleo experimental); consolidação | ⬜ |
| S10 | 08/12 – **12/12** | **Apresentação de banca** | ⬜ |

**S2 é o marco.** Sem corpus com procedência, B3 não existe e SP3 fica sem resposta. Ao
contrário de PLN-1, **não depende de terceiro** — depende só de execução, e por isso não
tem desculpa.

---

## 10. Entregáveis (critério de conclusão — §7 do mestre)

- [ ] **Corpus normativo** indexado, com procedência por documento (fonte, data, versão);
- [ ] Pipeline RAG reprodutível em `experimentos/iagen/`, com `requirements` próprio,
      *prompts* versionados, modelo e temperatura fixados;
- [ ] **Amostra de avaliação congelada** (30 produtores) + saídas dos 4 braços;
- [ ] **M1–M8 reportadas**, com **B3 × B2** respondendo SP3 e **B3 × B1** isolando o ganho real;
- [ ] **Protocolo de guardrails** (§7.1) documentado e demonstrado, incluindo caso de recusa;
- [ ] Concordância entre avaliadores reportada;
- [ ] **C6 respondido** — limiares marcados `[normativo]` ou `[escolha de projeto]`;
- [ ] Ficha de admissão respondida; **G1–G3** registrados em `REGISTRO.md`.

---

## 11. Riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| GEN-1 | **LLM gerar recomendação sanitária errada e convincente** | **Alto** | §7.1 inteira: recusa explícita, proibição de conduta clínica, revisão humana, M7 como critério de admissão |
| GEN-2 | **Ganho de B3 ser na verdade o ganho de ligar `RECEITAS`** (G2) | Alto | Braço **B1** existe exatamente para isolar isso |
| GEN-3 | Corpus normativo mal segmentado → recuperação ruim → RAG parece pior do que é | Médio | S3 dedicada a segmentação e limiar; reportar qualidade de recuperação separada da geração |
| GEN-4 | Avaliação de alucinação virar opinião dos autores | Médio | Definição por **afirmação verificável**, dupla avaliação independente, concordância reportada |
| GEN-5 | Custo/latência inviabilizarem em escala de cooperativa | Médio | **M8**; discussão local × API já aberta em `pln.md` §8 |
| GEN-6 | Bloco 2 concentrar IA Gen **e** Extensão no mesmo trimestre curto | **Alto** | S0 antecipada (já feita); corpus (S2) não depende de terceiros e pode adiantar; Extensão tem marco próprio em 30/09 |
| GEN-7 | Ementa exigir tema diverso (ex.: geração de imagem, *fine-tuning*) | Médio | Eixo "geração ancorada e avaliação de alucinação" se adapta; §8.2 fixa o critério, não o modelo |
| GEN-8 | PII vazar para API de terceiro | **Alto** | §8.3 — pseudonimização obrigatória; ligada a **A2** |

---

## 12. Premissas a confirmar

1. **Ementa da matéria** (Raphael) — indisponível. **[premissa a confirmar]** (§8.2).
2. **Modelo e orçamento** — não decididos. O critério está fixado (§8.2); a escolha é da S1.
3. **Revisão veterinária de M7** — depende de Maria Vitória aceitar contribuir **fora**
   da autoria acadêmica. **Não confirmada.** Sem ela, M7 vira limitação declarada.
4. **Versão vigente da IN 77** — confirmar se houve alteração desde 2018 antes de tratar
   o texto como corpus de referência. Liga-se a **C6**.
5. **Qual score alimenta o plano no futuro** — esta matéria adota
   `score_risco_fornecedor` porque é o que está em produção (§4). Se o produto unificar os
   dois motores (G3), o experimento precisa ser reancorado.

---

## 13. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**.

| Autor | Papel nesta matéria |
|---|---|
| **Matheus Iverson** — dados/modelagem | Pipeline RAG, indexação, implementação dos 4 braços, métricas M1–M8 |
| **Daianne Valéria** — produto/UX | Corpus e procedência, protocolo de avaliação, desenho da revisão humana, critério de acionabilidade |
| **Fagner Vieira** — negócio/produto | Critério de admissão, restrição de PII, custo × soberania do dado, relatório |

**Maria Vitória e Diego Santana não participam do Projeto Integrador** e **não são
coautores** desta ou de qualquer entrega acadêmica. Atuam exclusivamente na Maratona
SENAR Goiás. Se houver revisão sanitária da amostra de M7 por Maria Vitória, ela é
creditada como **contribuição externa ao escopo acadêmico**, nominalmente — **nunca como
coautoria**.

**Convenção de commit:** `acad(iagen): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

_Documento da matéria de IA Generativa — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §13)._
