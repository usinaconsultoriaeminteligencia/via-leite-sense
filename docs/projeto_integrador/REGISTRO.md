# REGISTRO — Trilha Acadêmica 2026-2

> Índice cronológico e auditável do que foi produzido para o Projeto Integrador entre
> **28/07 e 15/12/2026**, por matéria e data. Serve à **rastreabilidade de autoria**
> (§9 do documento mestre): separa o incremento acadêmico do produto comercial.
>
> **Branch:** `academico/2026-2` · **Convenção de commit:** `acad(<materia>): <resumo>  [autor: <iniciais>]`
> com `<materia>` ∈ `{ia, rna, pln, iagen, extensao, artigo}`.
>
> **Regra:** toda entrada abaixo referencia um commit real. Nada entra aqui por
> intenção — só por artefato versionado.

---

## Iniciais dos autores

| Iniciais | Autor | Papel |
|---|---|---|
| **FV** | Fagner Vieira | Negócio/produto |
| **DV** | Daianne Valéria | Produto/UX |
| **MI** | Matheus Iverson | Dados/modelagem |

**Maria Vitória e Diego Santana não participam do Projeto Integrador** e não são
coautores de nenhum entregável acadêmico (§2 do mestre).

---

## Cronologia

| Data | Matéria | Commit | Entrega | Autor |
|---|---|---|---|---|
| 04/08/2026 | — | *(local)* | Rascunho do documento mestre e briefing de entrada | FV |
| 05/08/2026 | geral | `40cf02d` | **Documento mestre** consolidado com 3 decisões fechadas: autoria (Fagner Vieira), pergunta de pesquisa central + SP1/SP2/SP3, candidato (a) RAG na IA Generativa. Premissas 12.1 e 12.2 resolvidas. | FV |
| 05/08/2026 | rna | `88b7f2f` | **`rna.md`** — objetivo, ficha de admissão, **auditoria do pipeline (A1/A2/A3)**, protocolo experimental pré-registrado, trilha E1–E3, backlog de 9 sprints | FV |
| 05/08/2026 | geral | `88b7f2f` | **`REGISTRO.md`** — este índice | FV |
| 05/08/2026 | rna | `863c677` | Premissa do artefato canônico resolvida; A2 datado como presente em produção | FV |
| 05/08/2026 | extensao | `f50c69a` | **`extensao.md`** — delimitação extensão × prospecção comercial, regra de PII/LGPD, plano de prospecção P1–P4 com marco de decisão em 30/09, desenho da oficina, critério anti-inflação de beneficiários. Correção de PII em `rna.md` e no mestre | FV |
| 05/08/2026 | pln | `86939c4` | **`pln.md`** — constatação de ausência total de corpus; estratégia treino sintético / **teste real**; esquema de anotação; métrica de campo crítico com limiar de recusa; fronteira com IA Generativa | FV |
| 05/08/2026 | extensao | `86939c4` | `extensao.md` §6.3 — **coleta de linguagem para o PLN** incorporada à prospecção de agosto (prazo 31/08) | FV |
| 05/08/2026 | geral | `7c654ca` | Apresentação do PI (12/12) separada do encerramento do semestre (15/12) em todos os documentos | FV |
| 05/08/2026 | ia | `0d5cf32` | **`ia.md`** — formalização do sistema baseado em conhecimento (limiares, 7 dimensões, inferência, classificação) e **6 achados C1–C6**, sendo **C1 defeito de produto verificado**; comparação regras × aprendido; seção de ética/LGPD ancorada em A2 | FV |
| 05/08/2026 | geral | *(esta entrega)* | **Bloco acadêmico no `README.md`** — pergunta central, índice dos 8 documentos, princípio metodológico (ganho sobre baseline, nunca R² absoluto), distinção PI × Maratona, aviso de régua acadêmica × comercial. Correção de bug de documentação: Fluxos 1–2 mandavam rodar `via_leite_app.py`, que hoje é só a página de redirect | FV |
| 05/08/2026 | artigo | `0820a1a` | **`artigo.md`** — plano do artigo: 3 contribuições (estratificação da confiança por camada; protocolo de auditoria de sistema em produção; caso da cadeia leiteira), método consolidado, reprodutibilidade, **ameaças à validade absorvendo os 12 achados**, estrutura em 10 seções com calendário de escrita antecipado, veículos P1–P4 | FV |
| 05/08/2026 | iagen | `fd9879b` | **`ia_generativa.md`** — **baseline do gerador de planos medido em produção** (3 textos distintos para 30 produtores; 42 % sem ação); **achado estrutural dos dois motores de risco**; desenho de **4 braços** (B0 regras / B1 regras+RECEITAS / B2 LLM sem âncora / B3 RAG); métricas M1–M8 com erro crítico decidindo a admissão; restrição de PII ligada a A2; **3 achados G1–G3** | FV |

---

## Decisões estruturais (com data e efeito)

| Data | Decisão | Efeito |
|---|---|---|
| 05/08/2026 | Autoria assina **Fagner Vieira** (briefing trazia "Fagner Pinho", erro de digitação) | Premissa 12.1 do mestre resolvida |
| 05/08/2026 | Pergunta de pesquisa: **1 central + 3 subperguntas**; a base sintética passa de limitação em rodapé a **condição estrutural** da pergunta | §11 do mestre reescrito; cada matéria ganha uma subpergunta própria |
| 05/08/2026 | **Extensão fica fora das subperguntas**, como evidência de validade externa | Cria plano de contingência para o risco R2: se a cooperativa não se materializar, nenhum documento de matéria precisa ser reescrito |
| 05/08/2026 | IA Generativa: candidato **(a) RAG sobre normativas**; (b) e (c) descartados com motivo registrado | SP3 definida como núcleo experimental do artigo |
| 05/08/2026 | Baseline confirmado por leitura de código: **MM7 com fallback em cascata** (MM30 → `producao_media_esperada_litros_dia`) — não é naïve nem persistência | Premissa 12.2 resolvida; a cascata deve ser descrita no artigo, pois torna o ganho de 22,5 % mais conservador |
| 05/08/2026 | **`artefatos_teste` é o artefato canônico** — confirmado por padrão do script (`:30`), padrão do backend (`app.py:47`) e pelo `/health` da Railway (`artefatosDir: artefatos_teste`, env não sobrescrita) | MAE 24,45 / 22,5 % validados como números oficiais. **Implica que o modelo em produção é o treinado com CPF/razão social como features** — A2 está no ar |
| 05/08/2026 | Confirmado que **não há clientes pagantes** na aplicação | A2 rebaixa de incidente de produção para **correção pré-lançamento**, com prazo: antes do primeiro onboarding real |
| 05/08/2026 | **SP3 ancora em `score_risco_fornecedor`**, não em `score_via_leite` — porque é o score que efetivamente alimenta `/action-plans` (G3) | O experimento mede o produto real. Se os dois motores forem unificados, o desenho de SP3 precisa ser reancorado |
| 05/08/2026 | Experimento de SP3 usa **4 braços**, não 2: B0 (regras em produção), B1 (regras + `RECEITAS`), B2 (LLM sem âncora), B3 (RAG) | B1 isola quanto do ganho vem só de ligar código que já existe (G2). Sem ele, um ganho de B3 seria creditado ao RAG indevidamente |
| 05/08/2026 | **Nenhum dado pessoal de produtor vai para API de terceiro** no experimento de IA Generativa — só indicadores e score, com identificador pseudonimizado | Restrição dura de admissão (§8.3 de `ia_generativa.md`), ligada a **A2**: o projeto não repete em outra camada o erro de usar CPF como insumo de modelo |
| 05/08/2026 | **Apresentação do PI é 12/12/2026** — distinta do encerramento do semestre (15/12/2026) | Prazo real de banca, artigo e apresentação antecipa em 3 dias. Datas de 15/12 nos documentos passam a valer só como **janela de aula** das matérias do Bloco 2, nunca como prazo de entrega |

---

## Achados de auditoria (abertos)

**A1–A3** levantados em `rna.md` §4 (pipeline de treino); **C1–C6** em `ia.md` §4
(motor de risco); **G1–G3** em `ia_generativa.md` §3.2 e §4 (geração de plano de ação).
**Todos aguardam decisão** — nenhum foi corrigido no produto.

| # | Achado | Matéria de origem | Estado | Decisão pendente de |
|---|---|---|---|---|
| **A1** | `litros_ajustados_gerencial` e `impacto_gerencial_pct` quebram a convenção temporal do pipeline (expõem o dia *t*, que todas as demais features evitam via `shift(1)`) | rna | 🔴 aberto | Ablação da sprint 4 mede a magnitude |
| **A2** | **`fornecedor_cpf_cnpj` e `fornecedor_nome_razao_social` usados como features one-hot** — memorização por indivíduo, degradação silenciosa para produtor novo (cold start) e uso de CPF como variável preditiva | rna | 🔴 aberto | Ablação da sprint 4; alimenta a seção de ética/LGPD da matéria de IA |
| **A3** | Hiperparâmetros nunca sintonizados; conjunto de validação nunca usado para seleção; execução única sem estimativa de variância | rna | 🔴 aberto | Protocolo simétrico definido em `rna.md` §5 |
| **C1** | 🔴 **A metade superior da escala de risco está morta.** Sobre as 54.780 linhas da base de produção, `score_via_leite` tem máximo **49,40** — abaixo do limite de 50 que abriria "Alto risco". **Zero** ocorrências de Alto risco e Crítico | ia | 🔴 aberto | Diagnóstico F2: calibração dos pesos ou gerador sintético saudável demais? |
| **C2** | As "7 dimensões ponderadas" não são independentes — um CCS ≥ 600k dispara 3 delas (20+15+10 = 45 de 100). O mesmo para CBT | ia | 🔴 aberto | Declarar a sobreposição; decidir se é ênfase deliberada |
| **C3** | Score pode chegar a 120, mas as faixas terminam em 101 → `_classificar_risco` devolve **`NaN`** silencioso. **Latente** (hoje inalcançável), mas **corrigir C1 o ativa** | ia | 🔴 aberto | Corrigir **antes** de mexer em C1 |
| **C4** | Proveniência dos pesos (25/20/15/15/10/10/5) não documentada. A IN 77 dá limiares, **não pesos** | ia | 🔴 aberto | Elicitação + análise de sensibilidade (F2/F3) |
| **C5** | Constantes de mercado (preço R$ 2,80, bônus R$ 0,15, penalidade R$ 0,10) embutidas no código junto dos limiares sanitários — o impacto econômico mostrado ao cliente envelhece em silêncio | ia | 🔴 aberto | Separar base de conhecimento de motor de inferência |
| **C6** | Limiares rotulados como "IN 77" são mais estritos que a norma — design de alerta antecipado atribuído a fonte normativa | ia | 🔴 aberto | Marcar cada limiar como [normativo] ou [escolha de projeto], conferindo no texto oficial |
| **G1** | **Planos sugeridos truncados em 12, sem ordenação e sem aviso.** `_build_suggested_action_plans` termina em `return plans[:12]` (`backend/app.py:479`); na base atual **14 elegíveis → 12 gerados**, e quem cai fora é acidente de iteração. Em carteira grande, continua 12 | iagen | 🔴 aberto | Ordenar por gravidade antes de cortar; decidir se o limite é de UI ou de regra |
| **G2** | **A camada de "COMO agir" existe e não está ligada.** `perfil/classificador_perfil.py` (`RECEITAS`, `recomendacao_combinada`) declara-se "a entrega de valor: recomendação cirúrgica em vez de genérica", mas **o backend não importa o módulo** — o único consumidor é `perfil/perfil_demo.py`. O que chega ao usuário é o `"; ".join()` de 5 regras | iagen | 🔴 aberto | Ligar ao produto (é o braço B1 do experimento de SP3) — parte do ganho atribuível ao RAG pode vir só disso |
| **G3** | **Dois motores de risco coexistem, com escalas e cortes diferentes.** `score_risco.py` (`score_via_leite`, 7 dims, o formalizado em `ia.md`) alimenta **só `/risk-radar`**; `fornecedor_inteligencia.py` (`score_risco_fornecedor`, 4 dims 0,35/0,30/0,20/0,15) alimenta **`/suppliers` → `/action-plans`**. Ambos importados em `backend/app.py:15-16` | iagen | 🔴 aberto | Decidir se unifica; enquanto não, documentar qual score responde por qual tela |

> **G3 evita uma conclusão errada na banca.** O máximo de 49,40 do **C1** é do
> `score_via_leite`; o motor que alimenta os planos de ação alcança **76,2** e classifica
> "Alto". Os dois achados são verdadeiros e **não se contradizem** — são motores
> diferentes. C1 **não** invalida a matéria de IA Generativa.

> **A2 tem alcance além do acadêmico.** É simultaneamente achado metodológico, defeito
> de produto (cold start do cliente novo) e questão de LGPD. **Está no ar**: a produção
> serve `artefatos_teste`, que é o treino **com** os identificadores. Como **ainda não
> há clientes pagantes**, nenhum usuário real é afetado hoje — a correção é
> **pré-lançamento**, com prazo antes do primeiro onboarding real.

---

## Pendências de documento

| Entregável | Estado |
|---|---|
| `../PROJETO_INTEGRADOR.md` (mestre) | ✅ commitado (`40cf02d`) |
| `rna.md` | ✅ esta entrega |
| `REGISTRO.md` | ✅ esta entrega |
| `pln.md` | ✅ esta entrega — **ação em aberto: coleta de linguagem real até 31/08 (risco PLN-1)** |
| `ia.md` | ✅ esta entrega — **6 achados (C1–C6); C1 é defeito de produto** |
| `extensao.md` | ✅ esta entrega — **ação em aberto: prospecção P1/P2 inicia em agosto; marco de decisão 30/09** |
| `ia_generativa.md` | ✅ esta entrega — **escrito no Bloco 1, antes de a matéria abrir**; baseline já medido (sprint S0 cumprida); **3 achados G1–G3** |
| `artigo.md` | ✅ esta entrega — **marco real é 30/09** (6 das 10 seções não dependem de resultado e devem estar prontas no fim do Bloco 1; risco ART-1) |
| Bloco acadêmico no `README.md` | ✅ esta entrega |

**Os 8 entregáveis de documento estão completos.** O que resta na trilha não é
documentação — é **execução** (corpus, experimentos, campo) e **decisão sobre os 12
achados em aberto**, que seguem sem prazo atribuído exceto C6 (19/10, resolvido de
passagem pela montagem do corpus normativo).

---

_Registro da trilha acadêmica — Via Leite Sense · USINA I.A. · 2026-2._
