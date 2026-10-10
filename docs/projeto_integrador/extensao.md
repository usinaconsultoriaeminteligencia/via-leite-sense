# Projeto de Extensão Integrador — IA · Projeto Integrador 2026-2

> **Matéria:** Projeto de Extensão Integrador — IA · **Professor:** Willgnner
> **Janela da matéria:** 06/10 – 15/12/2026 (Bloco 2) · **Encontros:** Qua 20:45–22:45
> **⚠️ Janela real de trabalho:** **começa em agosto/2026** — ver §6
> **Papel na pesquisa:** **evidência de validade externa** (§11 do mestre) — **não** é subpergunta
> **Documento mestre:** [`../PROJETO_INTEGRADOR.md`](../PROJETO_INTEGRADOR.md)
> **Data de referência:** 05/08/2026

---

## 1. Objetivo e papel na trilha

A Extensão **não responde uma subpergunta de pesquisa**. Ela responde uma pergunta
diferente, e complementar:

> *O sistema sobrevive ao contato com o produtor real?*

Enquanto SP1, SP2 e SP3 medem camadas técnicas contra dados majoritariamente
sintéticos, a Extensão é o único ponto do trabalho em que o projeto encontra **pessoas
reais em contexto real**. Ela qualifica a resposta da pergunta central sem depender de
um estudo de usuários com rigor estatístico — que uma equipe de três pessoas não tem
escala para conduzir em um semestre.

**Consequência prática (mitiga R2):** se a articulação em campo falhar, **nenhuma
subpergunta é afetada e nenhum documento de matéria precisa ser reescrito**. Perde-se
a validade externa, que passa a ser reportada como limitação. Essa é a razão de a
Extensão ter ficado deliberadamente fora das subperguntas.

---

## 2. Delimitação — o que é extensão e o que **não** pode ser

Esta seção existe porque o Via Leite Sense é **produto comercial** e o autor principal
é o fundador da empresa. Sem uma regra explícita, a atividade de extensão colapsa em
prospecção de clientes — e perde as duas naturezas ao mesmo tempo.

### 2.1 Extensão universitária é

- **Interação dialógica** com comunidade externa: a comunidade traz saber, não só
  recebe solução;
- **Benefício verificável para a comunidade**, independentemente de o projeto ganhar
  algo com isso;
- **Aprendizado recíproco** documentado — inclusive o que o produtor ensinou à equipe;
- **Beneficiários contáveis**, com critério declarado.

### 2.2 Extensão universitária **não** é

- ❌ Estágio ou prestação de serviço;
- ❌ Demonstração comercial disfarçada de oficina;
- ❌ Pesquisa de mercado — as perguntas de `docs/validacao_mercado.md` são de
  **validação comercial** e **não** podem ser o instrumento da oficina de extensão.

### 2.3 Regra de separação (análoga à §8.2 do mestre)

> **A mesma visita não pode ser, ao mesmo tempo, reunião comercial e atividade de
> extensão.** Elas são agendadas, conduzidas e registradas separadamente.

| | Atividade de extensão | Reunião comercial |
|---|---|---|
| Objetivo | Capacitar; devolver conhecimento à comunidade | Vender/contratar |
| Entrega | Oficina, material aberto, orientação sobre IN 76/77 | Proposta, preço, contrato |
| Vale mesmo se… | …a cooperativa **nunca** virar cliente | …não há oficina envolvida |
| Registro | Relatório de extensão, lista de presença | Fora do escopo acadêmico |

**Se uma cooperativa atendida virar cliente**, isso é registrado no relatório como
**fato ocorrido**, jamais como **resultado da extensão** — a extensão não é medida por
conversão. Confundir os dois é o erro que uma banca detecta com uma única pergunta:
*"e se eles não comprassem, a extensão teria valido?"*. A resposta precisa ser sim,
por construção.

---

## 3. Ficha de admissão (§4 do mestre)

| Teste | Resposta |
|---|---|
| **1. Não-prejuízo** | ✅ **Atende integralmente.** A Extensão **não produz código** e não toca o produto. Usa o sistema já no ar (Vercel/Railway) como material didático. Risco técnico nulo. |
| **2. Agregação de valor** | ✅ **Atende.** Entrega a única evidência de contato com usuário real de todo o trabalho, e produz um insumo que nenhuma outra matéria produz: **o que o produtor real diz que precisa**, coletado sem intenção de venda — portanto menos enviesado que qualquer entrevista comercial. |

---

## 4. Ativos de partida — o que já existe

Nada aqui parte do zero. Levantado no repositório:

| Ativo | Situação | Uso na extensão |
|---|---|---|
| **Produto no ar** | `via-leite-sense.vercel.app` (200) + API Railway (200), verificados em 05/08/2026 | Demonstração via **QR code** em campo, sem instalação |
| **Relação real de campo já existente** | Uma fazenda com **13 coletas reais de qualidade** (CCS/CBT/gordura/proteína, set/2024–abr/2026) registrada no projeto, via relatório SISATeG | **Porta de entrada mais provável** — é uma relação existente, não uma abordagem fria |
| **Ponte técnica em campo** | Técnica responsável pelo relatório SISATeG, integrante da Maratona SENAR | Articulação e credibilidade local — **com a ressalva de autoria da §11** |
| **Rede AgroStartup SENAR/SEBRAE GO 2026** | Projeto participante | Acesso institucional a cooperativas e sindicatos rurais |
| **Roteiro de entrevistas** | `docs/validacao_mercado.md` (H1–H5 + 10 perguntas a produtor, 8 a laticínio) | ⚠️ **Referência apenas.** É instrumento **comercial**; a oficina precisa de instrumento próprio (§2.2) |
| **Base normativa** | IN 76/77 MAPA, já implementada em `score_risco.py` | **Conteúdo da oficina** — é o conhecimento que se devolve à comunidade |

> **A oficina tem conteúdo próprio, independente do software.** Ensinar produtor a
> ler CCS/CBT à luz da IN 76/77 e a entender o que dispara perda de bônus é valor
> entregue **mesmo que ninguém use a plataforma**. É isso que qualifica a atividade
> como extensão — e não como demonstração de produto.

---

## 5. Regra de dados pessoais e consentimento (LGPD)

Atividade de extensão gera PII: nomes, propriedades, listas de presença, fotos,
dados de produção. O repositório é **público**.

**Regras invioláveis:**

1. **Nenhum nome de produtor, técnico ou propriedade entra em arquivo versionado.**
   Este documento segue essa regra — as pessoas e a fazenda citadas na §4 aparecem
   **sem identificação**, embora sejam conhecidas da equipe.
2. Dados de campo vão para `dados_reais/`, que **já está no `.gitignore`** e permanece
   assim.
3. **Consentimento por escrito** antes de qualquer coleta, foto ou uso de dado —
   com finalidade declarada (acadêmica) e prazo.
4. O relatório de extensão publicável usa **agregados e códigos** (`Produtor A`,
   `Cooperativa 1`), nunca identificadores.
5. Fotos de pessoas exigem autorização de uso de imagem à parte.

> **Coerência interna:** o achado **A2** (`rna.md` §4) critica o uso de CPF como
> variável preditiva. Seria contraditório o trabalho denunciar isso no modelo e
> vazar identificação de produtor no relatório de extensão.

---

## 6. Prospecção — a parte que começa **agora**, não em outubro

A matéria começa em **06/10**. Articular cooperativa leva **meses**. Se a prospecção
começar junto com a matéria, não haverá piloto até 12/12. **Por isso a prospecção é
trabalho de agosto e setembro** — em paralelo a RNA e PLN.

### 6.1 Alvos, em ordem de probabilidade

| # | Alvo | Por quê | Custo de articulação |
|---|---|---|---|
| **P1** | **Ampliar a relação de campo já existente** — do produtor único para o grupo de produtores da mesma rota/laticínio | Relação já estabelecida, com dado real já compartilhado; menor atrito | **Baixo** |
| **P2** | **Cooperativa via rede AgroStartup SENAR/SEBRAE** | Canal institucional já aberto pelo projeto | Médio |
| **P3** | **Sindicato rural / SENAR Goiás — oficina aberta** | Não depende de aceite de uma organização específica | Médio |
| **P4** | **Laticínio da região** | Maior alcance (carteira inteira), mas decisão mais lenta e mais comercial que comunitária | **Alto** |

**Estratégia:** perseguir **P1 e P2 em paralelo** desde agosto. **P3 é a rede de
segurança** — uma oficina aberta via sindicato não depende de nenhuma organização
aceitar, e sozinha já satisfaz o critério da matéria.

### 6.3 ⚠️ Carona obrigatória: coleta de linguagem para o PLN

A matéria de **PLN encerra em 29/09**, antes de a oficina acontecer. Ela precisa de
**fala real de produtor** para o conjunto de teste, e a única janela disponível é a
**prospecção de agosto/setembro** (ver `pln.md` §4.2).

**Portanto, todo contato P1/P2 deve incluir uma coleta de linguagem de ~20 min:** pedir
ao produtor que descreva, **com as palavras dele**, o que reportaria à cooperativa em
situações típicas (entregou X litros; vaca com mastite; queda de produção no calor;
problema na coleta). Meta: **60–150 enunciados**.

- **Não é a oficina** e não a substitui — é anterior e muito menor;
- Vale a regra de PII da §5: **consentimento por escrito** e anonimização antes de
  qualquer versionamento;
- **Falhar aqui não compromete a Extensão**, mas compromete o conjunto de teste do PLN
  (risco PLN-1). É a dependência mais frágil entre matérias de toda a trilha.

### 6.2 Marco de decisão — **30/09/2026**

Até 30/09 é preciso ter **pelo menos um aceite formal** (P1, P2 ou P3). Se não houver:

- **Aciona-se P3** como plano garantido (oficina aberta, menor dependência externa);
- Se nem P3 for viável, **aciona-se o plano de contingência do §11 do mestre**: a
  Extensão é reportada com o alcance que tiver, e a validade externa vira limitação
  declarada no artigo. **Nenhuma outra matéria é afetada.**

---

## 7. Desenho do piloto

### 7.1 Oficina (atividade central)

| Bloco | Conteúdo | Duração |
|---|---|---|
| 1 | **Qualidade do leite e a IN 76/77** — o que são CCS e CBT, o que dispara perda de bônus, como ler o próprio relatório de qualidade | 40 min |
| 2 | **Clima e produção** — estresse térmico (THI), seca, e por que a queda aparece dias depois | 30 min |
| 3 | **Demonstração** — o radar de risco via QR code, no celular do próprio produtor | 30 min |
| 4 | **Escuta (mão dupla)** — o que o produtor faz hoje, o que falta, o que a ferramenta erra | 40 min |

O **bloco 4 é obrigatório** e é o que distingue extensão de palestra. É também o
insumo mais valioso para o produto — coletado **sem** intenção de venda.

### 7.2 Instrumentos a produzir

- Material didático da oficina (aberto, reutilizável, cedido à comunidade);
- Cartaz/folheto com **QR** para a demo;
- Termo de consentimento (§5);
- Lista de presença (com base para contagem de beneficiários);
- Roteiro de escuta do bloco 4 — **próprio**, distinto do roteiro comercial;
- Formulário de avaliação da oficina pelos participantes.

---

## 8. Contagem de beneficiários — critério declarado

O relatório exige **nº de beneficiários** (§7 do mestre). Números de extensão são
facilmente inflados; o critério fica declarado **antes** da coleta:

| Categoria | Definição | Como se comprova |
|---|---|---|
| **Diretos** | Pessoas que participaram presencialmente de uma atividade (oficina, visita técnica) | Lista de presença assinada |
| **Indiretos** | Pessoas da mesma unidade produtiva que não participaram, mas são atingidas pela orientação recebida | Declaração do participante, com nº de pessoas na propriedade |
| **Alcance potencial** | Produtores da carteira da cooperativa que teve material cedido | **Reportado separadamente e nunca somado aos demais** |

> **Regra anti-inflação:** o número principal do relatório é **beneficiários diretos**.
> Os demais aparecem como linhas distintas, jamais agregados num total único. Um
> relatório que anuncia "500 beneficiários" a partir do tamanho da carteira de uma
> cooperativa é exatamente o que desqualifica um trabalho de extensão.

---

## 9. Cronograma

| Período | Fase | Entrega | Estado |
|---|---|---|---|
| **Ago (S2–S5)** | **Prospecção** | Contato com P1 e P2; carta de apresentação institucional | 🔄 **inicia agora** |
| **Ago–Set** | **Coleta de linguagem (PLN)** | 60–150 enunciados reais de produtor, com consentimento — **prazo duro: até 31/08** (§6.3) | ⬜ |
| Set (S6–S9) | Articulação | Aceite formal; data da oficina agendada | ⬜ |
| **30/09** | **Marco de decisão** | Aceite obtido **ou** P3 acionado | ⬜ |
| Out (06/10 →) | Preparação | Material didático, termo de consentimento, QR, roteiro de escuta | ⬜ |
| Out–Nov | **Execução** | Oficina realizada; evidências e listas coletadas | ⬜ |
| Nov | Devolutiva | Retorno à comunidade com o que foi aprendido (fecha o ciclo dialógico) | ⬜ |
| Até **12/12** | Relatório | Relatório final + insumos para o artigo — **prazo é a apresentação (12/12)**, não o fim do semestre (15/12) | ⬜ |

**A devolutiva de novembro não é formalidade.** Extensão sem retorno à comunidade é
extração de dado. É o item que, omitido, mais enfraquece o relatório.

---

## 10. Entregáveis (critério de conclusão — §7 do mestre)

- [ ] Relatório de piloto com **nº de beneficiários** por categoria (§8);
- [ ] Evidências de campo (fotos autorizadas, listas de presença, registro da oficina);
- [ ] Material didático da oficina, cedido à comunidade;
- [ ] QR de demo em uso documentado;
- [ ] **Síntese da escuta (bloco 4)** — o que o produtor real disse que precisa;
- [ ] Termos de consentimento arquivados (**fora do versionamento**);
- [ ] Registro em `REGISTRO.md`.

---

## 11. Equipe e autoria (§2 do mestre — obrigatório)

O Projeto Integrador é entregue por **Fagner Vieira, Daianne Valéria e Matheus
Iverson — e somente por eles**.

| Autor | Papel nesta matéria |
|---|---|
| **Fagner Vieira** | Articulação institucional, condução da oficina, relatório |
| **Daianne Valéria** | Material didático, roteiro de escuta, avaliação pelos participantes |
| **Matheus Iverson** | Preparo da demo e leitura técnica do que a escuta revelar |

### ⚠️ Ponto sensível — a ponte de campo não é coautora

A relação de campo mais promissora (§4, P1) chega ao projeto por meio de uma **técnica
integrante da Maratona SENAR**, que **não participa do Projeto Integrador**. Isso cria
um risco real de confusão de autoria, e ele precisa ser tratado de frente:

- Ela pode **abrir portas, articular e participar da atividade em campo** —
  contribuição legítima e valiosa;
- Sua contribuição é creditada como **"contribuição externa ao escopo acadêmico"**,
  nominalmente, na seção de agradecimentos/créditos do relatório;
- **Ela não é coautora** do relatório, do artigo, da apresentação ou da ficha de
  equipe, e **não assina** nenhum entregável acadêmico;
- O mesmo vale para o integrante de engenharia/IoT da Maratona.

**Maria Vitória e Diego Santana atuam exclusivamente na Maratona SENAR Goiás.**

**Convenção de commit:** `acad(extensao): <resumo>  [autor: <iniciais>]` na branch
`academico/2026-2`.

---

## 12. Premissas a confirmar

1. **Ementa e critérios do professor Willgnner** — indisponíveis. Carga horária mínima
   de extensão, formato exigido de relatório e se há template institucional de lista de
   presença/termo. **[premissa a confirmar]** — é a premissa de maior impacto: pode
   alterar o desenho da §7.
2. **Exigência institucional de registro do projeto de extensão** (SENAI FATESG) —
   verificar se há cadastro/protocolo prévio obrigatório, com prazo. Se houver, pode ser
   anterior a 06/10.
3. **Disponibilidade da ponte de campo** para articular P1 — não confirmada com a
   pessoa.
4. **Aceite da fazenda já relacionada** em participar como comunidade do piloto — o
   compartilhamento anterior de dados **não** implica aceite de participação.
5. **Necessidade de comitê de ética** — projetos com seres humanos podem exigir
   submissão. Como aqui não há pesquisa com seres humanos no sentido estrito (é
   capacitação, não experimento), provavelmente **não** se aplica — mas **confirmar com
   o professor**, pois um erro aqui invalida a coleta.

---

_Documento da matéria de Extensão — trilha acadêmica Via Leite Sense · USINA I.A. · 2026-2._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson (ver §11)._
