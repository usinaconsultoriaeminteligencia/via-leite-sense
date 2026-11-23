# Roteiro de proteção — VIA LEITE SENSE

**Criado em:** 09/11/2026 · **Base:** [PESQUISA_ANTERIORIDADE_PI_2026-11-09.md](PESQUISA_ANTERIORIDADE_PI_2026-11-09.md)
**Execução e status:** [registro_pi/README.md](registro_pi/README.md). Pagamentos a partir de 20/11/2026.

Três frentes: **domínio**, **marca** e **programa de computador**, mais o que fazer com a **ideia**.
Ordem recomendada: Etapa 0 → 1 (domínio, hoje) → 2 (marca, esta semana) → 3 (software, em seguida).

> **A ideia em si não se registra.** A Lei de Software (9.609/98), a LPI (9.279/96, art. 10) e a Lei de Direito
> Autoral (9.610/98, art. 8º, I) não protegem ideias, métodos de negócio ou conceitos. O que se protege é o
> **nome** (marca), o **código** (registro de programa) e o **segredo** (contratos de confidencialidade).
> Ver Etapa 4.

---

## Etapa 0 — Decisões antes de pagar qualquer taxa

| # | Tarefa | Por quê | Status |
|---|---|---|---|
| 0.1 | **Titular: a USINA I.A., Empresa Simples de Inovação (Inova Simples)**, com a razão social exata do cartão CNPJ. Tem 50% de desconto nas taxas de marca (Nota PFE-INPI nº 9/2020) e trâmite prioritário gratuito (petição 3019). | Marca e domínio ficam no nome de quem explora o negócio. O pedido de marca exige atividade compatível (LPI art. 128). | ☐ |
| 0.2 | **Código:** Fagner é o único autor. Se o titular for a USINA I.A., basta um **termo de cessão de Fagner para a empresa** (uma página). Se Fagner registrar como pessoa física, não precisa de termo. **Equipe:** um termo simples de confidencialidade e de que as contribuições não-código (validação, textos, pitch, logo se alguém desenhou) pertencem ao projeto. | O direito autoral do software nasce com o autor; a empresa só vira titular com cessão escrita (Lei 9.609, art. 4º). O termo da equipe evita disputa futura se alguém sair. | ☐ |
| 0.3 | **Ler as cláusulas de PI** do termo de outorga FAPEG / SENAR (Fase D) e do regulamento do Projeto Integrador (SENAI FATESG). | Editais de fomento e instituições de ensino às vezes reservam cotitularidade ou licença. Melhor saber antes do depósito. | ☐ |
| 0.4 | Conta **gov.br** nível prata ou ouro, e **certificado digital ICP-Brasil e-CNPJ** (tipo A1). | O e-INPI usa o gov.br. A Declaração de Veracidade do software precisa de assinatura com certificado qualificado. | ☐ |
| 0.5 | **Logotipo final** (gota com sensor + "VIA LEITE SENSE"), conforme [BRANDING.md](../BRANDING.md), exportado em JPG. | O INPI pede a imagem da marca mista. Confirmar formato e tamanho no e-Marcas (historicamente JPG de até 2 MB). | ☐ |

---

## Etapa 1 — Domínio (fazer hoje · cerca de R$ 40 por ano cada)

1. Acessar **registro.br** e entrar com o CNPJ da USINA I.A. **Não usar o CPF**: os dados do titular ficam
   públicos no WHOIS.
2. Registrar:
   - `vialeitesense.com.br`: principal
   - `vialeite.com.br`: defensivo, para evitar que um terceiro use (a busca DNS de 09/11 indicou que está livre)
3. Opcional: `vialeitesense.com` numa registradora internacional (Cloudflare, Porkbun etc.), na faixa de US$ 10–15 por ano.
4. Ativar **renovação automática** e o contato de cobrança num e-mail institucional, não pessoal.
5. Apontar o DNS para a Vercel (o front está em `via-leite-sense.vercel.app`): adicionar o domínio no projeto da
   Vercel e criar os registros indicados (A / CNAME) no registro.br.
6. Depois, criar e-mail no domínio (`contato@vialeitesense.com.br`) para os materiais externos.

**Observação:** domínio não dá direito sobre a marca, e marca não dá direito sobre o domínio. São proteções separadas.

---

## Etapa 2 — Marca no INPI (esta semana · cerca de R$ 880)

### 2.1 O que depositar
| Campo | Valor |
|---|---|
| Sinal | **VIA LEITE SENSE** |
| Apresentação | **Mista** (nome + gota com sensor) |
| Natureza | Marca de serviço (classe 42) e marca de produto (classe 9) |
| Titular | USINA I.A. (CNPJ) |
| Classes | **42** (principal) e **9**. **Não** depositar em 29, 31 ou 35 (conflitos identificados). |
| Especificação | **Pré-aprovada** (GRU 389), estreita e ligada à cadeia leiteira e à análise preditiva |

Itens a procurar na **lista pré-aprovada** do e-Marcas. Use os termos exatos que a lista oferecer:
- **Classe 42:** software como serviço [SaaS]; plataforma como serviço [PaaS]; análise de dados / análise
  científica de dados; desenvolvimento de software; hospedagem de plataformas na internet.
  **Evitar:** consultoria em hardware, engenharia ou automação industrial. É o território da "Via Láctea Labs".
- **Classe 9:** software de computador, baixável; aplicativos de software para dispositivos móveis, baixáveis.

### 2.2 Passo a passo
1. Entrar no **e-INPI** com o gov.br e cadastrar o titular (CNPJ).
2. Emitir **uma GRU 389 por classe**. A tabela vigente é a de 2025, conforme fonte secundária: **R$ 880 por
   classe, R$ 440 com desconto ME/EPP**. Confirmar o valor no portal ao emitir.
3. Pagar as GRUs e aguardar a compensação.
4. Abrir o formulário **e-Marcas** (um pedido por classe):
   - preencher os dados do titular, a apresentação mista e a imagem do logotipo;
   - descrever os elementos figurativos;
   - marcar os itens da especificação pré-aprovada;
   - declarar a atividade compatível com a classe.
5. Protocolar e **guardar o número do processo** (9 dígitos) e o recibo.
5b. **Inova Simples:** em cada processo, peticionar o **código 3019** ("Trâmite prioritário de marcas com direito à
   gratuidade"). É sem custo e leva o comprovante Inova Simples anexado. Com isso o exame sai em poucos meses.
6. A partir daí, usar **"VIA LEITE SENSE™"** ou "marca depositada" nos materiais. O **®** só pode ser usado depois da concessão.

### 2.3 Depois do depósito
| Fase | Prazo | O que fazer |
|---|---|---|
| Publicação na RPI | semanas após o depósito | Conferir se os dados saíram corretos |
| **Oposição de terceiros** | 60 dias após a publicação | Se a Montanhes ("VIA LEITE") ou a "Via Láctea Labs" se opuserem: manifestação em 60 dias (GRU 339, cerca de R$ 90 com desconto) |
| Exame de mérito | meta INPI 2026: cerca de 10 meses sem oposição | Se houver **exigência**: responder em 60 dias (GRU 338/340, cerca de R$ 90 com desconto). Argumentar pelo conjunto: o "SENSE" e a figura, a apostila "LEITE" sem exclusividade no registro da Montanhes, e os ramos distintos. |
| Concessão | — | Taxa de concessão e certificado são **gratuitos** desde a tabela de 2025 (certificado digital). Validade de 10 anos, prorrogável. |
| Vigilância | contínua | Ler a RPI (seção Marcas) uma vez por mês e buscar "VIA LEITE", "LEITE SENSE" e "VIA SENSE" para ver novos pedidos de terceiros |

**Plano B se a classe 42 for indeferida:** recorrer (60 dias) **e** depositar uma variação com mais distintividade:
o símbolo da gota como **marca figurativa** isolada ou uma forma como "VLSENSE".

---

## Etapa 3 — Programa de computador no INPI (depois da Etapa 0.2 · cerca de R$ 210)

O registro é **declaratório**. O direito autoral existe desde a criação, e o registro serve de **prova de autoria e
data**. Vale por 50 anos. **O código não é enviado ao INPI**: só um resumo hash. O arquivo original fica sob a sua
guarda e é a prova.

### 3.1 Preparar a versão a registrar
Rodar no PowerShell, na raiz do repositório:

```bash
git tag -a v1.0-inpi -m "Versao registrada no INPI"
```

```bash
git archive --format=zip -o via-leite-sense-v1.0-inpi.zip v1.0-inpi
```

```powershell
Get-FileHash .\via-leite-sense-v1.0-inpi.zip -Algorithm SHA512
```

- Antes de gerar o pacote, conferir se o commit **não contém dados pessoais** (CPF, razão social de fornecedores)
  nem `dados_reais/`. O `git archive` só leva os arquivos versionados, mas vale verificar.
- Guardar o `.zip`, o hash, o algoritmo (SHA-512) e o commit em **pelo menos 2 lugares** (Drive e mídia
  offline). Se o arquivo se perder, o registro deixa de provar o conteúdo.

### 3.2 Dados que o formulário e-Software pede
| Campo | Preenchimento sugerido |
|---|---|
| Título | VIA LEITE SENSE — Radar de Risco Produtivo, Qualidade e Rentabilidade para a Cadeia Leiteira |
| Data de criação | Data do primeiro commit do repositório |
| Data de publicação | Primeira divulgação pública (repo público / demo na Vercel). Conferir no histórico. |
| Linguagens | Python (API FastAPI, modelos de IA), JavaScript/HTML/CSS (frontend SPA), SQL (DuckDB) |
| Campo de aplicação / tipo de programa | Escolher nas tabelas do INPI (agropecuária, análise de dados / inteligência artificial) |
| Autor | **Fagner** (único autor do código), com CPF |
| Titular | USINA I.A. (CNPJ) com o termo de cessão da Etapa 0.2, ou Fagner como pessoa física |
| Resumo hash | O SHA-512 da etapa 3.1, copiado sem omitir caracteres |

### 3.3 Passo a passo
1. Emitir a **GRU 730**: cerca de **R$ 210**, sem desconto para programa de computador, segundo fontes de 10/2026.
   Confirmar o valor ao emitir.
2. Pagar e aguardar a compensação.
3. Baixar a **Declaração de Veracidade (DV)** e assiná-la com o **certificado ICP-Brasil**.
4. Protocolar no **e-Software** com a DV assinada e o hash.
5. O certificado de registro sai publicado na RPI (seção Programas de Computador), normalmente em poucos dias.
6. Para **versões futuras com mudança substancial**, fazer um novo registro como programa derivado. Uma vez por
   ano, ou a cada marco do produto, é suficiente.

---

## Etapa 4 — Proteger a "ideia" (o que não tem registro)

1. **NDA / acordo de confidencialidade** antes de mostrar modelos, dados ou arquitetura a laticínios, cooperativas
   ou investidores em piloto. O pitch público, por si só, não precisa de NDA.
2. **Segredo industrial:** manter os pesos dos modelos, a calibração e os dados de treino fora de qualquer
   repositório público. A Lei 9.279, art. 195, pune a concorrência desleal por uso de segredo de negócio.
3. **Prova de anterioridade:** os commits datados e o registro de software já documentam quem fez o quê e quando.
4. **Patente:** não se aplica ao software em si. Só considerar se o `via_leite_edge` virar um dispositivo ou método
   físico novo. Nesse caso, fazer uma busca específica primeiro: já existem patentes de sensores e
   rastreabilidade de leite.

---

## Custos e cronograma

| Item | Quando | Custo estimado |
|---|---|---|
| Domínios .com.br (2) | Hoje | cerca de R$ 80 por ano |
| Certificado e-CNPJ A1 | Esta semana | cerca de R$ 150–250 (varia por autoridade certificadora) |
| Marca: 2 classes (GRU 389 com desconto) | Esta semana | cerca de R$ 880 |
| Programa de computador (GRU 730) | Após o termo de cessão | cerca de R$ 210 |
| **Total inicial** | | **cerca de R$ 1.300–1.450** |
| Reservas: exigência/manifestação | Se ocorrer | cerca de R$ 90 cada |
| Agente de PI (revisar especificação e responder oposição) | Opcional | sob orçamento |

> Os valores do INPI vêm de fontes secundárias (tabela de 2025, ainda vigente em 11/2026). A tabela oficial no gov.br
> exige login. **Confirmar sempre na tela de emissão da GRU.**

## Fontes
- INPI pePI (buscas de 09/11/2026): https://busca.inpi.gov.br/pePI/
- Valores e prazos de marca (Portaria GM/MDIC 110/2025 e INPI/PR 10/2025): https://pistapop.com.br/2026/09/registro-de-marca-no-inpi-como-funciona-quanto-custa-e-o-que-muda-em-2026/ · https://sarahfiorot.adv.br/direito-empresarial/quanto-custa-registrar-marca-inpi-2026/
- Registro de software (GRU 730, DV, hash): https://bonelapi.com.br/blog/registro-de-software/ · https://www.sprintcodes.com.br/registro-de-software-inpi/ · https://quasa.io/pt/media/registrar-software-no-inpi-exige-certificado-a-conta-govbr-nao-basta
- Preço .com.br: https://teletime.com.br/14/10/2026/br-6-milhoes/
