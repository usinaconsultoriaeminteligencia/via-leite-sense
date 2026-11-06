# Kit de campo da Extensão: Via Leite Sense

> **Matéria:** Projeto de Extensão Integrador (Willgnner). Instrumentos listados em
> `extensao.md` §7.2 e ainda não produzidos. Prontos para imprimir.
> **Regra de dados (extensao.md §5):** nada preenchido volta para o repositório. Formulários
> preenchidos e fotos ficam em `dados_reais/` (fora do git) ou em papel. O relatório usa códigos
> (`Produtor A`, `Cooperativa 1`).
> **Integração com PLN:** o Instrumento 3 (roteiro de escuta) já coleta as frases no formato do
> corpus real do SP2 (`experimentos/pln/dados/corpus_real_MODELO.csv`). Uma coleta serve às duas matérias.

---

## Instrumento 1: Termo de consentimento livre e esclarecido

**Projeto:** Via Leite Sense, Projeto Integrador do 5º período de Inteligência Artificial
(SENAI FATESG), atividade de extensão.

Eu, ______________________________________, declaro que fui informado(a) de que:

1. **Finalidade:** a atividade é acadêmica. As informações servem para avaliar uma ferramenta
   de apoio à qualidade do leite e para um artigo científico. Não há venda nem compromisso comercial.
2. **O que será coletado** (marque o que autoriza):
   - [ ] Minhas respostas na conversa (anotadas pela equipe)
   - [ ] Frases que eu disser sobre a rotina da fazenda, **sem meu nome**, para treinar e testar
     um sistema que entende mensagens de produtor
   - [ ] Dados de produção e de qualidade que eu escolher compartilhar
   - [ ] Fotos em que eu apareça (autorização de imagem à parte, Instrumento 1-A)
3. **Anonimato:** meu nome, o nome da propriedade e de animais não aparecem em nenhum material
   publicado. No artigo e no relatório, apareço como código (ex.: "Produtor A").
4. **Guarda:** os dados ficam com a equipe do projeto, fora de qualquer repositório público, e são
   apagados até ___/___/______.
5. **Liberdade:** posso recusar, parar a qualquer momento ou pedir a exclusão dos meus dados,
   sem prejuízo, pelo contato: ______________________.
6. **Base legal:** consentimento (Lei 13.709/2018, LGPD, art. 7º, I), para finalidade acadêmica.

Local e data: ____________________   Assinatura: ____________________

Responsável pela coleta: ____________________   Assinatura: ____________________

### Instrumento 1-A: Autorização de uso de imagem

Autorizo o uso de fotos em que apareço, tiradas em ___/___/______, apenas em material acadêmico
do projeto (relatório de extensão e apresentação de banca), sem fins comerciais.
[ ] Sim  [ ] Não      Assinatura: ____________________

---

## Instrumento 2: Lista de presença (base dos beneficiários diretos)

Atividade: ______________________  Data: ___/___/______  Local: ______________________

| Nº | Nome | Função (produtor, familiar, funcionário, técnico) | Pessoas na unidade produtiva | Consentimento assinado? | Assinatura |
|---|---|---|---|---|---|
| 1 | | | | [ ] | |
| 2 | | | | [ ] | |
| 3 | | | | [ ] | |
| 4 | | | | [ ] | |
| 5 | | | | [ ] | |
| 6 | | | | [ ] | |
| 7 | | | | [ ] | |
| 8 | | | | [ ] | |

A coluna "Pessoas na unidade produtiva" dá os **indiretos** (extensao.md §8). **Nunca somar
diretos, indiretos e alcance potencial num número só.**

---

## Instrumento 3: Roteiro de escuta (bloco 4 da oficina) e coleta de linguagem

Duração: cerca de 40 min. Tom de conversa, não de entrevista comercial. Anotar **as palavras do
produtor como ele falou**, sem corrigir português nem trocar termo.

### Parte A: escuta (para o relatório de extensão)

1. Como o senhor/a senhora fica sabendo hoje do resultado de CCS e CBT? Em quanto tempo?
2. Quando o leite é penalizado ou perde bônus, o que costuma ter acontecido?
3. O que faz quando o calor aperta? Percebe queda de leite? Quantos dias depois?
4. O que viu na demonstração que faria diferença na rotina? E o que não serve?
5. Por onde gostaria de receber um aviso: WhatsApp, ligação, papel, técnico?

### Parte B: coleta de linguagem (alimenta o corpus real do PLN)

Ler cada situação e pedir: **"Como o senhor mandaria isso para a cooperativa, do seu jeito?"**
Anotar a frase exata (ou gravar, se o termo autorizar, e transcrever depois).

| # | Situação lida pela equipe | Intenção (preencher depois) | Frase do produtor |
|---|---|---|---|
| 1 | Hoje entregou o leite do dia | registro_producao | |
| 2 | Uma vaca amanheceu com o úbere inchado | ocorrencia_sanitaria | |
| 3 | Chegou o resultado do laboratório | registro_qualidade | |
| 4 | O resfriador deu problema à noite | ocorrencia_operacional | |
| 5 | O caminhão não passou para buscar | ocorrencia_logistica | |
| 6 | Com o calor a produção caiu | relato_ambiental | |
| 7 | Quer que o técnico venha à fazenda | solicitacao | |
| 8 | Entregou o leite **e** tem uma vaca doente | registro_producao + ocorrencia_sanitaria | |

**Antes de qualquer arquivo digital:** trocar nomes de pessoa, fazenda e animal por marcadores
(`[PESSOA_1]`, `[FAZENDA_1]`, `[ANIMAL_1]`). Digitar no formato de
`experimentos/pln/dados/corpus_real_MODELO.csv` e guardar em `dados_reais/`.
Meta (`pln.md` §4): **60 a 150 frases**. Com menos, o SP2 vira análise qualitativa de erro (contingência PLN-1).

---

## Instrumento 4: Folheto da demonstração (bloco 3)

> **Via Leite Sense: o risco do seu leite antes da coleta**
>
> Aponte a câmera do celular para o QR code e veja o painel de demonstração.
>
> [QR code → https://via-leite-sense.vercel.app]
>
> Dados de demonstração: o painel usa uma base de referência, não os dados da sua fazenda.
> Projeto acadêmico do SENAI FATESG, 5º período de Inteligência Artificial.

**Conferir antes de imprimir:** o QR tem de apontar para `via-leite-sense.vercel.app`. O endereço
antigo do Streamlit foi desativado em 06/11/2026. Testar com dois celulares, de preferência na
rede ou nos dados móveis que os produtores usam.

---

## Instrumento 5: Avaliação da oficina pelos participantes

Marque de 1 (nada) a 5 (muito):

| Pergunta | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Entendi o que são CCS e CBT e por que afetam o preço do leite | | | | | |
| Entendi como o calor afeta a produção | | | | | |
| A demonstração no celular foi fácil de acompanhar | | | | | |
| Eu usaria um aviso desse tipo na minha rotina | | | | | |
| A linguagem da equipe foi clara | | | | | |

O que mais ajudou? ____________________________________________

O que faltou ou ficou confuso? __________________________________

---

## Instrumento 6: Planilha de consolidação (relatório de extensão)

Guardar em `dados_reais/extensao/` (fora do git). O relatório publica só o agregado.

| Código da atividade | Data | Tipo (oficina, visita) | Diretos | Indiretos | Alcance potencial (separado) | Frases coletadas para o PLN | Termos assinados |
|---|---|---|---|---|---|---|---|
| ATV-01 | | | | | | | |

**Para o artigo** (`artigo.md` §6.2, validade externa): número de participantes diretos, de
frases reais coletadas e o que a escuta mostrou sobre a utilidade do aviso. Se o piloto não
acontecer até 12/12, isso vira limitação declarada (`artigo.md` §10.2) e o artigo não muda.
