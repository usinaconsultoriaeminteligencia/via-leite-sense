# Inteligência Artificial (IA) — Projeto Integrador 2026-2

> **Matéria:** Inteligência Artificial · **Professor:** Alexandre Barbosa
> **Janela:** **semestre inteiro** (28/07 – 12/12/2026) · **Encontros:** Sex (4 blocos)
> **Papel na pesquisa:** camada de **conhecimento** da pergunta central; apoia **SP1**
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Data de referência:** 05/08/2026

---

## 1. Objetivo

Formalizar `score_risco.py` e `perfil/classificador_perfil.py` como um **sistema
baseado em conhecimento** — representação, regras, decisão sob incerteza — e
**compará-lo com o aprendido** (o XGBoost da SP1). Inclui a seção de **ética e LGPD**
de toda a trilha.

É a matéria transversal: atravessa o semestre e é onde o trabalho responde *por que
existe uma camada de regras* num produto que também tem modelo estatístico.

**A formalização já produziu resultado.** A §4 registra seis achados obtidos ao
representar formalmente o que o código faz — sendo o primeiro deles grave o bastante
para redefinir a prioridade da matéria.

---

## 2. Ficha de admissão (§4 do mestre)

| Teste | Resposta |
|---|---|
| **1. Não-prejuízo** | ✅ **Atende.** A matéria **formaliza e audita**; não altera `score_risco.py` nem `perfil/`. As correções propostas na §4 são registradas como recomendação, com decisão do Fagner à parte. |
| **2. Agregação de valor** | ✅ **Já agregou, antes de qualquer implementação.** O achado **C1** identifica que o motor de risco **nunca emite suas duas classes mais severas** sobre a base de produção. Isso é defeito de produto encontrado por formalização acadêmica. |

---

## 3. O sistema de conhecimento como ele está hoje

Levantado em `score_risco.py` (365 linhas). Esta é a representação formal que a matéria
precisa produzir — e ela não existia escrita em lugar nenhum.

### 3.1 Base de conhecimento — limiares

Declarados em `LIMIAR` (`score_risco.py:33`), atribuídos no comentário a
**"IN 77/2018 MAPA e referências da cadeia leiteira goiana"**:

| Domínio | Parâmetro | Valor |
|---|---|---|
| Qualidade | `ccs_atencao` / `ccs_alto` | 400.000 / 600.000 cel/mL |
| Qualidade | `cbt_atencao` / `cbt_alto` | 100.000 / 300.000 UFC/mL |
| Qualidade | `gordura_min` / `proteina_min` | 3,0 % / 2,9 % |
| Térmico | `thi_conforto` / `thi_atencao` / `thi_alto` | 68 / 72 / 78 |
| Tanque | `temp_tanque_max` / `_critico` | 4,0 °C / 6,0 °C |
| Produção | `queda_producao_pct` / `_critica` | 10 % / 20 % |
| Logística | `perda_logistica_pct` | 5 % |
| Econômico | `preco_litro_base` / `bonus_qualidade` / `penalidade_qualidade` | R$ 2,80 / R$ 0,15 / R$ 0,10 |

### 3.2 Motor de inferência — 7 dimensões ponderadas

`PESOS_SCORE` (`:60`), **soma = 100** (verificado):

| Dimensão | Peso | Regra |
|---|---|---|
| `risco_queda_producao` | 25 | queda ≥ 10 % vs. média histórica |
| `risco_qualidade` | 20 | **OR** de CCS ≥ 400k, CBT ≥ 100k, gordura < 3 % |
| `risco_ccs` | 15 | CCS ≥ 400k |
| `risco_cbt` | 15 | CBT ≥ 100k |
| `risco_temp_tanque` | 10 | temperatura > 4 °C |
| `risco_perda_bonus` | 10 | CCS ≥ 600k **ou** CBT ≥ 300k |
| `risco_descarte` | 5 | perda logística ≥ 5 % |

Ao somatório ponderado somam-se ainda dois componentes contínuos (`:186-197`):
**THI normalizado** (até +10) e **queda de produção** (até +10).

### 3.3 Classificação e saída

`_classificar_risco` (`:202`) usa `bins = [-1, 25, 50, 75, 101]` →
**Baixo risco · Atenção · Alto risco · Crítico**. Saídas: `score_via_leite`,
`classe_risco`, `impacto_economico_estimado`.

---

## 4. Achados da formalização

Obtidos ao executar o motor sobre `dados_teste/fact_producao_produtor_dia.csv`
(**54.780 linhas** — a base que alimenta o produto).

### C1 — ✅ **A metade superior da escala estava morta** (fechado em 20/10/2026)

Distribuição real de `score_via_leite` sobre as 54.780 linhas:

| | Valor |
|---|---|
| Mínimo | 0,00 |
| Média | 16,49 |
| **Máximo** | **49,40** |

Contra as faixas de classificação:

| Classe | Faixa | Ocorrências |
|---|---|---|
| Baixo risco | 0 – 25 | **41.832** |
| Atenção | 25 – 50 | **12.948** |
| **Alto risco** | 50 – 75 | **0** |
| **Crítico** | 75 – 101 | **0** |

> **O produto é um "radar de risco" cujas duas classes de risco nunca acendem.** O
> máximo observado — 49,40 — fica **abaixo do limite de 50** que abriria "Alto risco".
> Não é raridade estatística: é **teto**. Em nenhum dos 54.780 registros o sistema
> classificou um produtor como Alto risco ou Crítico.

**Duas explicações possíveis, e distingui-las é trabalho desta matéria:**

1. **Calibração:** os pesos e faixas estão desalinhados com a distribuição real dos
   sinais — as flags raramente coocorrem, então a soma ponderada não alcança 50;
2. **Gerador:** a base sintética produz um rebanho irrealisticamente saudável, e o
   motor está certo em não alarmar.

São diagnósticos opostos com correções opostas. **Enquanto não se distingue, não se
corrige** — mexer nas faixas sem saber a causa é ajustar o termômetro para a
temperatura desejada.

**Conexão com a Extensão:** os dados reais de qualidade já registrados no projeto
(13 coletas, com picos de CCS bem acima da média) são a evidência independente para
esse teste — é ali que se vê se produtor real gera score na faixa alta.

> **Fechamento — 20/10/2026.** Nenhuma das duas hipóteses era a causa primária. A causa
> era **de unidade**: os limiares de CCS/CBT estavam em cél/mL e UFC/mL e as colunas vêm
> em **mil** por mL, o que matava 4 das 7 dimensões. Corrigida a unidade, apareceu um
> segundo defeito, oposto à hipótese 2: o gerador era **pouco** saudável em CBT (mediana
> 134 mil contra 60 em GO) e no tanque (acima de 4 °C em 94% dos dias). A calibração usou
> a IN 76/77 e o dataset de qualidade da RBQL (Zenodo 17714633), sem dado de cliente.
> Resultado: máximo 100, "Alto risco" + "Crítico" em 42% das linhas. Commits `b3ea169`,
> `c0c2424` e `a3ae356`; registro em `docs/ESTADO_REAL.md` §8.

### C2 — As 7 dimensões **não são independentes**

Um único CCS ≥ 500 mil/mL dispara **três** dimensões simultaneamente (o corte era 600 mil
até 20/10/2026, quando passou ao limite da IN 76):

| Dimensão | Peso | Por quê |
|---|---|---|
| `risco_qualidade` | 20 | OR inclui CCS ≥ 400 mil |
| `risco_ccs` | 15 | CCS ≥ 400 mil |
| `risco_perda_bonus` | 10 | CCS ≥ 500 mil |
| **Total de uma só medição** | **45** | de 100 |

O mesmo vale para CBT (20 + 15 + 10 = 45). **Apresentar isso como "7 dimensões
ponderadas" é impreciso** — há forte sobreposição por construção. Não é
necessariamente errado (pode ser ênfase deliberada em qualidade), mas **precisa ser
declarado**, e a documentação atual não declara.

### C3 — Score pode ultrapassar o teto da classificação (latente)

Teto teórico = 100 (flags) + 10 (THI) + 10 (queda) = **120**. As faixas terminam em
**101**. Verificado: `_classificar_risco` devolve **`NaN`** para qualquer score acima
de 101 — silenciosamente, sem erro.

**Hoje é inalcançável** (máximo observado 49,40), portanto **não** é bug ativo. Mas os
dois achados se acoplam: **corrigir C1 — fazer a faixa alta ser alcançável — é
exatamente o que ativa C3.** O produtor de maior risco, aquele que o sistema existe
para sinalizar, sairia sem classificação. Corrigir C3 **antes** de mexer em C1.

### C4 — Proveniência dos pesos não está documentada

Os pesos (25/20/15/15/10/10/5) não têm origem registrada. **A IN 77 estabelece
limiares, não pesos** — nenhuma norma diz que queda de produção vale 25 e descarte
vale 5. São julgamento especializado (legítimo) ou arbitrários (problema), e hoje é
impossível distinguir pelo código.

**É a contribuição central da matéria:** elicitar, documentar e submeter os pesos a
**análise de sensibilidade** — quanto a classificação muda quando cada peso varia. Um
sistema baseado em conhecimento cuja base de conhecimento não tem proveniência não é
formalizável; é código com números.

### C5 — Constantes de mercado embutidas no código

`preco_litro_base = 2,80`, `bonus_qualidade = 0,15`, `penalidade_qualidade = 0,10`
estão no mesmo dicionário dos limiares sanitários. São **coisas de naturezas
diferentes**: limiar sanitário muda por norma (raro, público, datado); preço de leite
muda por mercado (constante, regional, volátil).

Violação clássica da separação **base de conhecimento × motor de inferência**: fatos
voláteis viram constantes de código, e o `impacto_economico_estimado` — número que vai
ao cliente — envelhece em silêncio.

### C6 — Rótulo normativo em limiares que são escolha da equipe

O comentário do bloco atribui os limiares à **IN 77/2018**, mas os valores de
*atenção* são **mais estritos** que os limites regulatórios — o que é coerente com um
sistema de **alerta antecipado**, e não com transcrição da norma.

**Isso não é defeito — é boa engenharia mal documentada.** O problema é atribuir à
norma um número que é decisão de projeto. Para a banca, cada limiar precisa estar
marcado como **[normativo]** ou **[escolha de projeto]**, com a justificativa dos
segundos.

> ⚠️ **[premissa a confirmar]** Os valores exatos da IN 76/77 devem ser conferidos
> **no texto oficial da norma**, não em memória nem em fonte secundária. Esta seção
> afirma apenas que há divergência entre o rótulo e o valor — a conferência
> ponto a ponto é tarefa da sprint de formalização.

---

## 5. Comparação regras × aprendido

O eixo que a matéria pede, e que agora tem substância:

| Aspecto | Sistema de regras (`score_risco.py`) | Aprendido (XGBoost, SP1) |
|---|---|---|
| Entrada | Limiares normativos + medições | ~120 features derivadas |
| Saída | Score 0–100 + classe + impacto R$ | Litros previstos (t+1…t+7) |
| Interpretabilidade | **Total** — cada ponto é rastreável a uma regra | Parcial (importâncias) |
| Dado necessário | Funciona com **um** dia de medição | Exige **28 dias** de histórico (`lag_28`) |
| Produtor novo | **Funciona no primeiro dia** | Degrada (achado **A2** de `rna.md`) |
| Fraqueza | Calibração (**C1**) e proveniência (**C4**) | Aprende o gerador; memoriza identidade |

> **Tese defensável da matéria:** as duas camadas não competem — **cobrem lacunas uma
> da outra**. A regra atende o produtor novo, de quem não há histórico; o modelo atende
> o produtor maduro, de quem há 28 dias de série. É por isso que a arquitetura é
> híbrida, e não por indecisão. Esse é o argumento que a pergunta central (§11 do
> mestre) precisa sustentar.

---

## 6. Ética e LGPD

Seção obrigatória da trilha (§5 do mestre). O produtor é **pessoa identificável** e o
produto trata dados que afetam sua renda.

### 6.1 Caso concreto — o achado A2

`rna.md` §4.A2: **`fornecedor_cpf_cnpj` e `fornecedor_nome_razao_social` são features
one-hot do modelo em produção.** É o exemplo que esta seção precisa — não hipótese, mas
o próprio sistema:

- **Minimização:** CPF não é necessário para prever litros. Usar identificador como
  variável preditiva falha o princípio;
- **Finalidade:** CPF foi coletado para cadastro, não para alimentar modelo;
- **Discriminação:** modelo que memoriza indivíduo pode perpetuar avaliação histórica
  desfavorável de um produtor, independentemente da melhora recente dele.

### 6.2 Agenda da seção

1. **Decisão automatizada e direito à revisão** — o score afeta bônus e prioridade de
   visita. O produtor pode contestar? Hoje **não há** canal previsto;
2. **Transparência** — a interpretabilidade da regra é um **ativo de conformidade**:
   é possível dizer ao produtor *por que* seu score é X, o que o modelo estatístico não
   permite com a mesma clareza;
3. **Minimização** — revisar todo o schema, não só o modelo;
4. **PII no trabalho acadêmico** — regra já vigente (`extensao.md` §5), com o incidente
   corrigido em 05/08 registrado como precedente;
5. **Risco de dano** — um falso "Baixo risco" pode custar bônus ao produtor. **C1
   mostra que isso não é hipotético:** o sistema hoje é incapaz de emitir alerta severo.

---

## 7. Gancho opcional — otimização de sequenciamento de rotas

Previsto no mestre como opcional, usando `dim_rota` (`dificuldade_logistica`,
`percentual_estrada_nao_pavimentada`, `capacidade_tanque_litros`).

**Recomendação: não priorizar.** A matéria já tem escopo suficiente e um achado
(**C1**) que exige trabalho real. Roteirização é problema clássico de otimização, mas
**não** responde à pergunta central e competiria com a formalização. Fica como
**menção no relatório**, com implementação apenas se sobrar folga após C1–C6.

---

## 8. Backlog — semestre inteiro (28/07 – 12/12)

| Fase | Período | Entrega |
|---|---|---|
| **F1** | Ago | Formalização escrita da base de conhecimento (**§3 — feito**) e achados **C1–C6** (**feito**) |
| **F2** | Set | **Diagnóstico de C1**: calibração ou gerador? Análise de sensibilidade dos pesos (**C4**) |
| **F3** | Out | Elicitação e documentação de proveniência (**C4/C6**); marcação [normativo] × [escolha de projeto] |
| **F4** | Out–Nov | Seção de ética/LGPD (§6); comparação regras × aprendido (§5) com os números da SP1 já fechados |
| **F5** | Nov–12/12 | Consolidação para o artigo; recomendações de correção (C1, C3, C5) com decisão registrada |

**Dependência:** a §5 só fecha depois de a SP1 entregar os números do protocolo
corrigido (sprint 8 de RNA, ~21/09). Antes disso, a comparação seria contra métricas
que a própria auditoria já contestou.

---

## 9. Entregáveis (critério de conclusão — §7 do mestre)

- [ ] Documento do sistema baseado em conhecimento (representação, regras, inferência) — §3;
- [ ] **Diagnóstico de C1** com conclusão fundamentada (calibração × gerador);
- [ ] **Análise de sensibilidade** dos 7 pesos;
- [ ] Tabela de proveniência dos limiares — [normativo] × [escolha de projeto];
- [ ] Comparação regras × aprendido, com números;
- [ ] **Seção de ética e LGPD**;
- [ ] Recomendações de correção com decisão de produto registrada;
- [ ] Ficha de admissão respondida; registro em `REGISTRO.md`.

---

## 10. Riscos

| # | Risco | Impacto | Mitigação |
|---|---|---|---|
| IA-1 | **C1 revelar que o motor de risco precisa de recalibração ampla** | **Alto** | É achado, não fracasso. Recalibrar é decisão de produto, fora do escopo acadêmico do Bloco 1 |
| IA-2 | Proveniência dos pesos ser irrecuperável (ninguém lembra) | Médio | Então documenta-se como **julgamento não registrado** e faz-se a sensibilidade — que é o que dá base defensável |
| IA-3 | Conferência da IN 76/77 no texto oficial não ser feita a tempo | Médio | Tarefa de F3; sem ela, nenhuma afirmação normativa entra no artigo |
| IA-4 | Escopo inflar com o gancho de rotas | Baixo | Já despriorizado (§7) |
| IA-5 | Ética virar seção genérica de LGPD | Médio | Ancorada em **A2** e **C1**, que são deste sistema |

---

## 11. Premissas a confirmar

1. **Ementa da matéria** (Alexandre Barbosa) — indisponível. **[premissa a confirmar]**
2. **Valores oficiais da IN 76/77** — conferir **no texto da norma** (§4.C6).
3. **Proveniência dos pesos** — perguntar a quem definiu 25/20/15/15/10/10/5. Se foi o
   próprio Fagner, registrar o raciocínio original.
4. **Origem da referência de perfil** — o briefing cita "Gonçalves (2025)"; o módulo
   cita **IN 76/77 + MilkPoint (06/2026)**. "Gonçalves (2025)" **não existe no
   repositório**. Confirmar antes de citar.
5. **`classificador_perfil.py`** — este documento formalizou `score_risco.py`; o
   classificador de perfil (3 classes) precisa do mesmo tratamento em F2.

---

## 12. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**.

| Autor | Papel nesta matéria |
|---|---|
| **Fagner Vieira** | Proveniência dos limiares e pesos (conhecimento do domínio); decisão sobre correções |
| **Matheus Iverson** | Diagnóstico de C1, análise de sensibilidade, comparação regras × aprendido |
| **Daianne Valéria** | Seção de ética/LGPD; transparência da decisão para o produtor |

**Maria Vitória e Diego Santana não participam do Projeto Integrador** e **não são
coautores** desta ou de qualquer entrega acadêmica. Atuam exclusivamente na Maratona
SENAR Goiás.

> **Nota de escopo:** a validação sanitária dos limiares se beneficiaria de leitura
> veterinária. Essa contribuição, se ocorrer, é **externa ao escopo acadêmico** e
> creditada como tal — nunca como coautoria.

**Convenção de commit:** `acad(ia): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

_Documento da matéria de IA — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §12)._
