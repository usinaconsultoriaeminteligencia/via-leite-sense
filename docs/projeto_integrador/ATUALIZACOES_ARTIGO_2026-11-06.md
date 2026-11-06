# Atualizações para o artigo do Projeto Integrador

> **Para:** Fagner Vieira, Daianne Valéria e Matheus Iverson (autores do artigo, `artigo.md` §12).
> **Data de referência:** 06/11/2026 · **Banca:** 12/12/2026 (faltam 36 dias).
> **Base:** plano do artigo (`artigo.md`), escopo de 10/10 (`docs/apresentacao_pi/ESCOPO_DO_ARTIGO_PI.docx`),
> dossiê técnico (`docs/DOSSIE_ARTIGO_PI_VIA_LEITE_SENSE.docx`, gerado em 07/10) e o repositório em `e10a4ab`.
>
> O Projeto Integrador existe para **integrar as cinco matérias do 5º período de IA** num único
> artigo sobre o Via Leite Sense. Este documento lista **o que mudou no sistema depois do plano
> e do dossiê**, **a que matéria cada mudança pertence** e **onde ela entra no artigo**. Ele não substitui o `artigo.md`: é a lista de trabalho para
> atualizá-lo e para escrever as seções.
> Régua acadêmica: limitações e autocrítica **entram** (`artigo.md` §9).

---

## 1. Resumo: o que mudou desde 10/10

| # | Fato novo | Data | Onde entra no artigo |
|---|---|---|---|
| 1 | **C1 fechado** com norma (IN 76/77) e fonte pública real (RBQL, Cravo et al.), sem dado de laticínio | 20/10 | §2, §4, §6 (já citado no plano; falta virar texto) |
| 2 | **Achado novo (A4):** as médias móveis atravessavam a fronteira entre produtores (vazamento de série) | encontrado 11/10, corrigido 06/11 | C-2, §6.1, §5 SP1 |
| 3 | **Números canônicos mudaram duas vezes:** 24,17 → 24,36 (C1) → **24,47** (A4) | 20/10 e 06/11 | §4.2, §5, dossiê, escopo |
| 4 | Achado de qualidade **na própria fonte pública** (ESD do RS em 2023 fora da faixa física) | 20/10 | §2 ou §4 (procedência de dados) |
| 5 | Evidência de validade da base sintética contra a RBQL (CCS mediana 392 = 392 de Goiás) | 20/10 | §4, §6.2 |
| 6 | Arquitetura de produção simplificada: **Streamlit removido**; só SPA (Vercel) + API (Railway) | 06/11 | §3 O sistema |
| 7 | Produção ainda serve o **modelo e o score anteriores** (deploy pendente) | 06/11 | §4.2 (qual artefato citar) |
| 8 | Sem acesso a dados de laticínio; SENAR como rota de dado real (classificação entre os 36, 10/10) | 07/10 e 10/10 | §6.2, §10.2 (validade externa) |
| 9 | Ambiente de execução difere do declarado (`xgboost` 3.4 instalado; `requirements.txt` pede `<3.0`) | 06/11 | §5 Reprodutibilidade |

---

## 2. O que cada matéria entrega ao artigo

O artigo só cumpre o papel de Projeto Integrador se cada matéria aparecer com contribuição
própria e verificável. A pergunta central (`artigo.md` §3) já distribui o trabalho: cada
camada do sistema é uma matéria, e a tese C-1 compara as garantias **entre** elas.

| Matéria (professor) | Camada no artigo | Contribuição no texto | O que mudou desde 10/10 | Situação em 06/11 | Ação para o artigo |
|---|---|---|---|---|---|
| **Inteligência Artificial** (Alexandre Barbosa) | Conhecimento normativo: sistema baseado em conhecimento (`score_risco.py`, 7 dimensões) | Representação de regras, inferência, classificação; comparação regras × aprendido; ética/LGPD (A2) | **C1 fechado** com IN 76/77 + RBQL: a camada de regras ganhou substrato real (§5) | **Medido em 06/11** (`experimentos/ia/`): C2, qualidade × CCS com phi 0,86, e com CCS ≥ 500 as dimensões somam 64,6 pts; C4, *ranking* robusto aos pesos (Spearman ≥ 0,95 em 50 sorteios), mas Alto + Crítico oscila de 30% a 53% | Escrever o C1 como estudo de caso de engenharia de conhecimento; usar C2/C4 medidos: os pesos pouco mudam **quem** vem primeiro e mudam **quantos** são classificados como risco alto |
| **Redes Neurais Artificiais** (Cristiano) | Aprendizado supervisionado (SP1) | NN × XGBoost × baseline, mesmo alvo e mesmo *split*, 5 sementes | **A4** (vazamento nas janelas móveis) corrigido; número de partida agora **24,47 / 22,4 %** (§3, §4) | Protocolo pré-registrado em `rna.md`; **sem código de NN** no repositório | Rodar o protocolo mínimo (§9); usar a série 24,45 → 24,47 como prova de auditoria do pipeline |
| **Processamento de Linguagem Natural** (Raphael) | Entrada em linguagem natural (SP2) | Intenção + NER sobre mensagem do produtor → lançamento estruturado | **Pipeline E0/E1 implementado em 06/11** (`experimentos/pln/`) com corpus sintético de 900 + 300 + 300 frases | Em sintético fora da distribuição: regras F1 0,96 × TF-IDF + LR 0,63; erro de volume 0%; a recusa no limiar 0,7 leva o lançamento correto de 66% a 97% com 34% de cobertura | Coletar o corpus real (kit da Extensão, Instrumento 3) e rodar `--teste-real`; o achado já disponível é a queda do modelo aprendido fora da distribuição |
| **IA Generativa** (Raphael) | Geração ancorada, núcleo experimental (SP3) | RAG sobre IN 76/77 gerando plano de ação; 4 braços (B0–B3); alucinação e aderência (M1–M8) | **Harness dos 4 braços implementado em 06/11** (`experimentos/iagen/`); B0 e B1 medidos | B0 reproduz o baseline (especificidade 0,10). Ligar as `RECEITAS` (B1) leva a 0,83, mas **0,23 sem os números** do score: o resto é artefato de medida. B2/B3 aguardam chave de API e o texto oficial das INs | Colocar IN 76/77 em `iagen/corpus/` e a chave; rodar; dupla avaliação humana em `avaliacao_humana.csv` |
| **Projeto de Extensão Integrador** (Willgnner) | Validade externa (fora das subperguntas) | Piloto com produtores, oficina, **QR de demo**, nº de beneficiários | Classificação entre os 36 do AgroStartup dá acesso ao SENAR; sem dado de laticínio; **Streamlit removido**: o QR de demo tem de apontar para `via-leite-sense.vercel.app` (§6, §8) | **Kit de campo pronto em 06/11** (`extensao_kit_de_campo.md`): termo LGPD, presença, roteiro de escuta com coleta de linguagem para o PLN, folheto com QR, avaliação, consolidação | Agendar a oficina via SENAR; uma coleta alimenta Extensão e PLN; se não acontecer até 12/12, vira limitação declarada (`artigo.md` §10.2) |

**Como a integração aparece no texto:**

- **§3 O sistema:** uma figura com as quatro camadas, cada uma rotulada com a matéria que a
  sustenta (IA → regras; RNA → previsão; PLN → entrada; IA Generativa → plano de ação) e a
  Extensão como o contato com o campo.
- **§8 Discussão (C-1):** a comparação **entre matérias** é o resultado do artigo. A camada de
  IA (regras com substrato real) oferece mais garantia que a de RNA (substrato sintético).
  O C1 e o A4 dão um exemplo concreto de cada lado.
- **§9 Ameaças:** cada achado leva o rótulo da matéria que o encontrou (A → RNA, C → IA,
  G → IA Generativa). Assim fica visível que a auditoria (C-2) atravessou o semestre.
- **Não deixar uma matéria só no plano.** Se PLN ou IA Generativa não tiverem resultado, a
  seção delas mostra o desenho, o que foi medido (o baseline de SP3 já existe) e por que
  não fechou. Seção vazia, nunca.

---

## 3. Números: substituir em todo lugar

**Número vigente (06/11/2026)**, de `artefatos_teste/metricas_modelo.json`, commit `da1d6d9`:

| Métrica (teste, 2025) | XGBoost | Baseline (MM7 com cascata) | Ganho |
|---|---|---|---|
| MAE (L) | **24,47** | **31,54** | **22,4 %** menor |
| RMSE (L) | 37,01 | 48,57 | 23,8 % menor |
| MAPE | 3,63 % | 4,55 % | 0,93 ponto percentual |
| R² | 0,9943 | 0,9901 | (não discrimina; não usar como argumento) |
| Linhas treino / validação / teste | 32.010 / 10.980 / 10.920 | | |
| Atributos | 131 (119 numéricos + 12 categóricos) | | |

**Série histórica.** Ela mostra o protocolo de auditoria funcionando, então vale apresentá-la no artigo:

| Data | MAE teste | Ganho | Por quê mudou |
|---|---|---|---|
| até 06/08 | 24,45 | 22,5 % | Com CPF e razão social como atributos (A2) |
| 06/08 | 24,17 | 23,4 % | A2 corrigido |
| 20/10 | 24,36 | 22,8 % | C1 corrigido (gerador recalibrado em CBT e tanque) |
| **06/11** | **24,47** | **22,4 %** | A4 corrigido (janelas móveis por produtor) |

> **Leitura que vale escrever no artigo:** cada correção de auditoria **piorou** um pouco o
> erro ou o deixou estável, e nunca o melhorou de forma artificial. É o comportamento esperado
> quando se remove um vazamento ou um sinal espúrio. O ganho sobre o baseline caiu de 23,4 %
> para 22,4 % e permanece robusto. Essa série é **evidência para C-2**: o protocolo encontra
> problemas cuja correção custa desempenho, e o trabalho reporta o custo.

**Onde trocar:**

| Documento | Está | Trocar por |
|---|---|---|
| `DOSSIE_ARTIGO_PI_VIA_LEITE_SENSE.docx` §7 | MAE 24,17 · RMSE 36,68 · MAPE 3,58 % · R² 0,9944 · "23 % menor" | Tabela acima |
| Dossiê §7, frase de abertura | "iguais às servidas por `/model/metrics` em produção" | **Remover** até o deploy (fato 7). Hoje a produção serve outro artefato |
| Dossiê, rodapé | "commit `74c1710`" | `e10a4ab` ou posterior. O `74c1710` foi reescrito na limpeza de 20/10 e **não existe** no repositório público |
| `ESCOPO_DO_ARTIGO_PI.docx` §3 e §8 | "MAE 24,17 contra 31,54 (23 % menor)" | 24,47 contra 31,54 (22,4 %) |
| `artigo.md` §4.2, coluna Fonte | `fix/janelas-moveis` | `da1d6d9` (o branch já foi integrado e apagado) |
| `artigo.md` §2 C-2 e §6 | "12 achados" | **13 achados** (A1–A4, C1–C6, G1–G3) |
| `rna.md`, `ia.md` | Conferir menções a 24,17 / 23 % | 24,47 / 22,4 % |

O teste `tests/test_numeros_canonicos.py` já falha se `ESTADO_REAL.md` ou `artigo.md` citarem
um MAE diferente do artefato. **Os `.docx` não são cobertos:** conferir à mão.

---

## 4. Achado novo A4: entra em C-2 e em §6.1

**O que era.** Em `via_leite/models/treino_mvp_avancado.py`, as médias e os desvios móveis
(`mm_*`, `std_*`, janelas de 3/7/14/30 dias sobre litros, CCS, CBT, THI e chuva) eram
calculados como `group[col].shift(1).rolling(janela)`. O `shift(1)` de um `SeriesGroupBy`
devolve uma série **sem agrupamento**, e o `rolling` seguinte corria sobre o DataFrame
inteiro. Como a base está ordenada por produtor e data, os primeiros dias de cada produtor
recebiam a média dos últimos dias do produtor anterior.

**Prova.** `tests/test_janelas_moveis_por_produtor.py`: dois produtores consecutivos com
100 e 1.000 L/dia. No código antigo, `mm_3` do 2º registro do produtor 2 valia 550 (mistura
dos dois). Corrigido com `transform` por produtor.

**Magnitude.** O filtro de `lag_28` já descartava os 28 primeiros dias de cada produtor,
então só a janela de 30 dias vazava: **29 linhas alteradas, todas no treino (0,09 %)**.
Efeito no teste: MAE de 24,34 para **24,47** (+0,13 L), medido com o código antigo e o novo
no mesmo ambiente.

**Por que importa mesmo sendo pequeno.** Na base sintética, todos os produtores começam na
mesma data. **Com dado real, produtores entram em datas diferentes**, e a janela contaminada
seria justamente a do produtor recém-chegado, o caso de *cold start* que A2 já tinha tornado
central. O defeito é pequeno na base sintética e grande no uso real. Esse contraste é o
argumento de C-1.

**Linha nova para a tabela §6.1 (Validade interna):**

| Ameaça | Origem | Tratamento no artigo |
|---|---|---|
| Atributos de janela móvel misturavam produtores consecutivos (vazamento entre séries) | **A4** | Corrigido (`da1d6d9`) com teste de regressão; reportar magnitude (+0,13 L) e o risco ampliado em dado real com entradas escalonadas |

**Parágrafo sugerido (§9 Ameaças ou §5 SP1):**

> Durante a auditoria, verificou-se que os atributos de média e desvio móveis eram
> calculados sobre a base concatenada, e não por produtor, de modo que os primeiros
> registros de cada série incorporavam valores da série anterior. A correção alterou 29
> linhas de treino (0,09 %) e elevou o MAE de teste de 24,34 para 24,47 L. O efeito é
> pequeno na base sintética porque todos os produtores iniciam na mesma data. Em dados
> reais, com entradas escalonadas, a contaminação recairia sobre os produtores recém-incluídos,
> precisamente o caso em que o sistema tem menos histórico.

---

## 5. C1 e a fonte pública: transformar em texto

O plano já registra o fechamento do C1. Falta escrever, e estes são os fatos a usar:

- **Fonte:** série de qualidade da RBQL/MAPA (CCS, CPP, EST, ESD), 12 localidades,
  2013–2023, curada por **Cravo et al., WCAMA/CSBC 2026**; dataset no **Zenodo,
  DOI 10.5281/zenodo.17714633, CC-BY 4.0**. Bruto versionado sem alteração em
  `dados_publicos/rbql_zenodo_17714633/`, com `PROVENIENCIA.md` e hash.
- **Causa do C1:** limiar em células/mL comparado a coluna em **mil** células/mL, mais um
  gerador irrealista em CBT e na temperatura do tanque.
- **Correção:** limiares em mil/mL (CCS 400/500, CBT 100/300; 500 e 300 são os limites da
  IN 76); gerador com CBT de mediana 134 → 79 mil UFC/mL e tanque acima de 4 °C de 94 % → 29 %
  das linhas.
- **Resultado:** nenhuma das 7 dimensões morta ou saturada (disparo entre 0,4 % e 55,3 %);
  máximo do score passou de 49,40 para 100; Alto + Crítico em 42 % das linhas.
- **Evidência de validade (§6.2):** a CCS mediana da base sintética é **392 mil cél/mL**,
  igual à de Goiás na RBQL em 2019–2023 (**392**). A CBT sintética (79) **continua acima**
  da de Goiás (60). Declarar a diferença residual em vez de omiti-la.
- **Achado na fonte:** o valor de ESD do RS em 2023 está fora da faixa física. Foi
  **marcado como inválido, não corrigido**. Mostra que o protocolo se aplica também ao
  dado de entrada. Mencionar com cuidado, citando os autores e sem tom de crítica.

**Para §2 Trabalhos relacionados.** Cravo et al. afirmam que os dados da cadeia leiteira
brasileira são dispersos e fragmentados e deixam como trabalho futuro descer ao nível de
propriedade e calcular o índice de temperatura e umidade (ITU/THI). O Via Leite trabalha
nesse nível, por produtor e com THI diário. Escrever como **complementaridade de escala**
(estado × ano contra produtor × dia), sem afirmar superioridade.

**Para C-1.** O C1 é o exemplo mais claro da tese: a camada de regras ganhou garantia
quando seu substrato passou a ser **real** (norma + RBQL), sem nenhuma sofisticação a mais
de método.

**Ressalva (§6.2, já no plano; manter):** a RBQL é distribuição **agregada** (estado × ano),
não distribuição por produtor. A calibração por produtor depende da Extensão.

---

## 6. §3 O sistema: arquitetura atual

Substituir qualquer menção a Streamlit. Desde 06/11/2026 o repositório **não tem mais
Streamlit** (o app foi descomissionado em 25/08 e a página de redirect saiu em 06/11).

- **Fluxo:** navegador → SPA estática (Vercel) → função serverless que injeta a chave
  (`X-API-Key`) → API FastAPI (Railway) → DuckDB em volume persistente.
- **Módulos:** `via_leite/api/` (API), `via_leite/core/` (score de 7 dimensões e
  inteligência de fornecedor), `via_leite/models/` (gerador sintético e XGBoost),
  `via_leite/ingest/` (ingestão com guardas de escala e de saturação; referência RBQL).
- **Caminhos citados nos achados mudaram** (reorganização de 25/08): `backend/app.py` →
  `via_leite/api/app.py`. G1 está hoje em `via_leite/api/app.py:501` (`return plans[:12]`);
  os dois motores de G3 são importados em `via_leite/api/app.py:17` e `:19`. Atualizar
  `REGISTRO.md`, `ia_generativa.md` e `rna.md` antes de citar linha no artigo.
- **G2 continua verdadeiro:** `perfil/classificador_perfil.py` (`RECEITAS`) segue sem
  importação no pacote `via_leite/`.

---

## 7. §5 Reprodutibilidade: itens novos no checklist

- [ ] **Base versionada:** `dados_teste/` tem **30 produtores e clima sintético**. O padrão
      do gerador é 2.400 produtores. Declarar o comando exato:
      `python -m via_leite.models.gerador_leite_sintetico --n-produtores 30`.
- [ ] **Versões reais de execução:** Python 3.12.10, xgboost 3.4.0, scikit-learn 1.9.0,
      pandas 2.3.3. O `requirements.txt` declara `xgboost<3.0`: **alinhar antes da
      submissão**, ou o revisor instala outra versão.
- [ ] **Variação de ambiente medida:** o mesmo código deu MAE 24,36 em 20/10 e 24,34 em
      06/11 (Δ 0,02 L, mudança de ambiente). O artefato de agosto já não reproduzia com
      xgboost 3.x. Isso reforça o invariante de **5 sementes com média ± desvio** (A3 segue
      aberto: hoje o número canônico é de **execução única**).
- [ ] **Guarda de consistência numérica:** `tests/test_numeros_canonicos.py` falha quando o
      documento cita número diferente do artefato. Vale citar como prática de
      reprodutibilidade documental.
- [ ] **O que não se publica:** além de `dados_reais/` e do corpus de fala, `docs/plano_de_trabalho/`
      (dados pessoais da equipe) fica fora do repositório público.

---

## 8. §6.2 Validade externa e §10: o que mudou

- **Sem dado de laticínio.** Um laticínio consultado não cedeu dados (07/10). No artigo:
  "não houve acesso a dados de laticínio". **Não nomear a empresa.**
- **SENAR como rota de dado real:** a startup foi classificada entre as 36 do Desafio
  AgroStartup (10/10), o que dá contato com produtores. Plano: planilhas de 2 a 3
  produtores, com NDA, como **validação externa**. Ainda não aconteceu; manter a
  contingência de §10.2 ("o artigo não muda").
- **Material comercial fica fora** (§9 do plano): Demo Day (29/10), pitch, preços e
  projeções de receita **não entram** no artigo.

---

## 9. Calendário: situação em 06/11

O escopo de 10/10 registrava que **nenhuma** seção estava escrita e que SP1 e SP2 estavam
sem código. Não há, no repositório, pasta `experimentos/` nem `docs/projeto_integrador/artigo/`.

| Marco do escopo de 10/10 | Prazo | Situação verificável no repositório |
|---|---|---|
| §1–§4 e §9 escritos | 31/10 | **Sem texto no repositório.** Confirmar com a equipe |
| SP1 (rede neural) com resultado | 31/10 | **Sem código** em `experimentos/` |
| SP2 (PLN) com corpus e métricas | 15/11 | **Sem código nem corpus** |
| Corpus normativo do RAG | 19/10 | **Sem artefato** |
| SP3 medido | 30/11 | Depende do corpus |
| §7, §8, §10 | 01–07/12 | — |
| Revisão integral | 08–10/12 | — |

**Recomendação de triagem (decidir esta semana):**

1. **Escrever já as seções independentes de resultado** (§1, §2, §3, §4, §9). Este
   documento e o dossiê cobrem §3, §4 e §9 quase por inteiro. É o que protege C-1 e
   C-2, que **não dependem** de SP1–SP3 (risco ART-2).
2. **SP1:** fechar o protocolo mínimo (XGBoost × baseline, 5 sementes, A1 por ablação). A
   rede neural entra só se couber. Um resultado negativo também serve.
3. **SP2:** se não houver corpus real até 15/11, aplicar a contingência PLN-1 (análise
   qualitativa, sem F1) e declarar.
4. **SP3:** é o núcleo e o mais arriscado. Montar o corpus normativo (IN 76/77) agora. Se o
   RAG não fechar até 30/11, o artigo se sustenta com C-1 + C-2 + SP1, e SP3 vira trabalho
   futuro com desenho pré-registrado (`ia_generativa.md`).

---

## 10. Checklist por autor

| Autor | Tarefa | Seção |
|---|---|---|
| **Fagner** | Atualizar dossiê e escopo (§3 deste doc); §3 O sistema com a arquitetura atual (§6); §9 Ameaças com A4 (§4) | §3, §9 |
| **Matheus** | §4 Método com a série histórica e a reprodutibilidade (§7); protocolo de 5 sementes; alinhar `xgboost` no `requirements.txt`; texto do A4 em SP1 | §4, §5 |
| **Daianne** | §2 Trabalhos relacionados com Cravo et al. e a complementaridade de escala (§5); decisão sobre SP2 (corpus ou contingência) | §2, §6 |
| **Todos** | Substituir "12 achados" por "13"; conferir que nenhum `.docx` cita 24,17 ou 24,36; revisão de linguagem de *pitch* | todo o texto |

---

## 11. Não escrever no artigo

- "MAE 24,17", "MAE 24,36", "23 % menor": **números vencidos**. O vigente é 24,47 / 22,4 %.
- "Métricas iguais às de produção": falso até o deploy do modelo de 06/11.
- O nome do laticínio que não cedeu dados.
- Qualquer número do pitch ou do Plano de Negócio (preço, receita, "R$ 800 a 1.500/mês").
- "Gonçalves (2025)": referência não verificada (risco ART-6).
- Streamlit como parte do sistema.

---

_Atualizações do artigo — trilha acadêmica Via Leite Sense · USINA I.A. · 06/11/2026._
_Autoria acadêmica: Fagner Vieira, Daianne Valéria e Matheus Iverson._
