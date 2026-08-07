## SESSION UPDATE — VIA LEITE SENSE
**Data:** 07/08/2026
**Desenvolvedor:** Fagner Vieira — USINA I.A. (par: Claude Opus 5)
**Branch:** `master` — **publicado em produção**

---

### O que esta sessão fez

Publicou o trabalho de 06/08. A `security/fecha-api` foi empurrada, fundida em
`master` por fast-forward (44 testes a passar) e deployada. A branch foi apagada
depois de a produção estar validada.

**Antes → depois, medido no ar:**

| Verificação | Antes | Depois |
|---|---:|---:|
| `GET /suppliers` sem chave | 200 | **401** |
| `POST /action-plans` sem chave | aberto | **401** |
| `/docs`, `/redoc`, `/openapi.json` | 200 | **404** |
| `/health` | 200 | 200 (público por desenho) |
| MAE do modelo servido | 24,4523 | **24,1726** (sem identificadores) |

Chave nova gerada com `secrets.token_urlsafe(32)`, definida em
`VIA_LEITE_API_KEYS` (Railway) e `VIA_LEITE_API_KEY` (Vercel). A chave de 06/08
nunca chegou a ser usada e está obsoleta. Nenhuma chave em disco, no repositório
ou no cliente — confirmado por varredura do `app.js` e do `index.html` servidos.

---

### Dois defeitos que só o runtime da Vercel revelou

O proxy passava nos testes locais e falhou em produção por duas razões distintas.
Nenhuma delas é detectável sem deployar — é o argumento mais forte a favor do
ALERTA-008 (auto-deploy + ambiente de preview).

**1. `req.query.path` chegava vazio** (`de9f4e3`)

Todo `/api/*` era encaminhado para a raiz da Railway. O diagnóstico veio do corpo
da resposta: `{"detail":"Not Found"}` é formato do FastAPI, não da Vercel — logo o
pedido chegou à Railway **e passou na chave**; só o caminho se perdia. Passou a
derivar do `req.url`.

**2. `api/[...path].js` foi registado como segmento único** (`afb75fc`)

`/api/health` entrava na função; `/api/model/metrics` devolvia o 404 da própria
Vercel **sem sequer a chamar** — metade das rotas inalcançável pelo SPA. Aqui o
corpo do 404 era o `NOT_FOUND` da Vercel, o que separou este caso do anterior.

Correcção: o ficheiro passou a `api/proxy.js` e o `vercel.json` encaminha
`/api/(.*)` para ele com o caminho em `__path`, que a função remove antes de falar
com a Railway. **Deixa de depender da convenção de nomes do ficheiro** — foi
justamente a convenção implícita que falhou em silêncio.

Verificado: 13 rotas a 200, incluindo as de dois segmentos, com query string
preservada.

---

### Ficou por fazer

| Item | Estado |
|------|--------|
| **C1** | diagnosticado; calibração continua a aguardar decisão — é o próximo assunto real |
| C2, C4, C5, C6 | abertos — declaração/proveniência, não código |
| G1, G2, G3 | abertos — produto |
| A1, A3 | **manter abertos** — protocolo pré-registado da sprint 4 |
| ALERTA-008 | auto-deploy ainda não ligado; esta sessão mostrou o custo |
| Senha `usina2025` | ainda recuperável do histórico Git |
| `docs/projeto_integrador/` | continua sem o achado de C1; vive em `academico/2026-2` |

> Contagem de achados corrigida no `PROJECT_REGISTRY.json`: dizia 9, a própria
> lista enumera 10.

---

## SESSION UPDATE — VIA LEITE SENSE
**Data:** 06/08/2026
**Desenvolvedor:** Fagner Vieira — USINA I.A. (par: Claude Opus 5)
**Branch:** `security/fecha-api` (a partir de `master`) — **publicada em 07/08; ver a sessão acima**

---

### Contexto da sessão

A Piracanjuba entrou em negociação para ceder dados reais ao projeto. Isso
converte três achados de "pendência documentada" em bloqueadores de
pré-lançamento, porque passariam a incidir sobre dados pessoais de produtores
reais. O trabalho da sessão foi fechar esses bloqueadores.

Estado da negociação em 06/08/2026: **sem data definida**. Há tempo para fazer
em sequência, sem atalhos.

---

### 1. ALERTA-005 — API de produção sem autenticação — RESOLVIDO em código

Os 30 endpoints estavam abertos ao público, 11 deles de escrita. Confirmado por
varredura: nenhum `Depends`, `APIKey` ou `HTTPBearer` em `backend/app.py`.

- **`backend/security.py`** (novo) — dependência global `require_api_key`.
  Registada em `FastAPI(dependencies=[...])`, e não endpoint a endpoint: um
  endpoint novo fica protegido por omissão. Foi a protecção endpoint a endpoint
  que permitiu chegar a 30 rotas abertas.
- **`frontend/api/[...path].js`** (novo) — proxy serverless na Vercel. O SPA é
  estático e não pode guardar segredo: qualquer chave que carregasse ficaria
  visível no código-fonte da página. O proxy guarda a chave e é o único a falar
  com a Railway. `index.html` passou a apontar para `/api`.
- **Falha fechada** — sem `VIA_LEITE_API_KEYS` o servidor responde 503 a tudo
  o que não seja `/health`. Não há chave por omissão no código.
- `/docs`, `/redoc` e `/openapi.json` fechados por omissão.
- Localhost sai do CORS quando `VIA_LEITE_ENV=production`.

Verificado: **30 rotas exigem chave, 11 de escrita, só `/health` público.**
O teste percorre as rotas registadas na aplicação, não uma lista escrita à mão.

### 2. Achado A2 — identificadores como features — RESOLVIDO

`fornecedor_cpf_cnpj` e `fornecedor_nome_razao_social` eram features one-hot do
modelo em produção. Confirmado no artefacto servido
(`artefatos_teste/metricas_modelo.json`).

Causa raiz: `selecionar_colunas` funcionava por lista de **exclusão** — qualquer
coluna de texto nova virava feature sozinha, e as colunas `fornecedor_*` entram
por junção com a dimensão de produtor. Correcção estrutural: predicado
`e_identificador` (lista explícita + padrões) e pós-condição que faz o treino
parar.

**Ablação (a que a sprint 4 previa para A2):**

| métrica | COM ident. | SEM ident. | delta |
|---------|-----------:|-----------:|------:|
| MAE | 24,4523 | 24,1726 | −0,2797 (−1,1 %) |
| RMSE | 36,8645 | 36,6797 | −0,1848 (−0,5 %) |
| MAPE % | 3,6315 | 3,5824 | −0,0491 (−1,4 %) |
| R² | 0,99431 | 0,99441 | +0,0001 |

Remover os identificadores **melhorou** o modelo. Eram risco LGPD e fragilidade
de cold start por benefício preditivo negativo. Artefactos versionados
regenerados (é o que a API serve; o `.joblib` é gitignored e não vai à Railway).

### 3. Achado C3 — NaN silencioso na classificação — RESOLVIDO

Corte superior passa a `inf` (score alto cai em "Crítico", leitura segura) e
score ausente vira `"Indeterminado"` em vez de NaN.

**Caminho novo, fora do enunciado do achado:** NaN em qualquer coluna `target_`
propaga para o score e daí para a classe. Zero ocorrências na base sintética,
mas dados reais têm falha de medição. Feito antes de C1, como a auditoria pedia.

---

### 4. Achado C1 — diagnóstico RESOLVIDO, calibração EM ABERTO

A auditoria deixava a pergunta: *"calibração dos pesos ou gerador sintético
saudável demais?"* **Nenhuma das duas — é erro de unidade.**

```
LIMIAR["ccs_atencao"] = 400_000        # células/mL
dados["ccs"]          = 93,4 … 769,4   # MIL células/mL
```

Fator 1000. `df["ccs"] >= 400_000` nunca é verdade. Idem CBT. Como
`risco_qualidade` e `risco_perda_bonus` também dependem só de CCS/CBT,
**quatro das sete dimensões estão mortas — 60 dos 100 pontos ponderados**, todas
pela mesma causa.

O gerador não é "saudável demais": produz CCS até **769 mil/mL**, bem acima do
limite de 500 mil da IN 77. Há produtores em risco na base; o sistema é que não
os vê.

**Divergência de números explicada:** os 49,40 da auditoria reproduzem no CSV
bruto (`fact_producao_produtor_dia.csv`). Na base enriquecida com clima o score
chega a 61,5 e há **1067 linhas em "Alto risco"** — "zero Alto risco" vale para
um caminho de dados, não para os dois. O `thi` (0–15 pontos) é a diferença.

**Corrigir a unidade sozinho troca sub-alerta por sobre-alerta:**

| classe | hoje | com unidade corrigida |
|--------|-----:|----------------------:|
| Baixo risco | 40.470 | 6.855 |
| Atenção | 13.243 | 8.840 |
| Alto risco | 1.067 | 26.894 |
| Crítico | **0** | **12.191** |

71 % da carteira em Alto/Crítico. Aí a questão de calibração dos pesos (C4)
torna-se legítima. **Os limiares NÃO foram alterados** — é decisão de produto
com julgamento de domínio.

> Peso académico: isto fecha um diagnóstico que `artigo.md` e `REGISTRO.md`
> declaram em aberto. "Erro de unidade" é achado mais forte para a banca do que
> "calibração indefinida". `docs/projeto_integrador/` ainda **não** foi
> actualizado — vive na branch `academico/2026-2`.

---

### DECISÃO PENDENTE — como resolver C1

1. Corrigir unidade + recalibrar pesos (análise de sensibilidade F2/F3).
2. Corrigir unidade + subir os cortes das faixas (25/50/75 foram desenhados para
   um score que nunca passava de 49).
3. Só instrumentar agora: detectar e rejeitar unidade errada na ingestão, para
   os dados da Piracanjuba não serem mal lidos em silêncio; adiar a recalibração.

**Recomendação:** 3 agora + 1 quando os dados reais chegarem. Recalibrar contra
dados sintéticos produz um número que vai mudar de qualquer forma.

---

### Ficou por fazer

| Item | Estado |
|------|--------|
| C1 | diagnosticado; calibração aguarda decisão |
| C2, C4, C5, C6 | abertos — declaração/proveniência, não código |
| G1, G2, G3 | abertos — produto (corte em 12, `RECEITAS` desligada, dois motores) |
| A1, A3 | **manter abertos** — protocolo pré-registado da sprint 4 |
| ALERTA-008 | auto-deploy GitHub → Vercel/Railway ainda não ligado |
| Senha `usina2025` | ainda recuperável do histórico Git |

### Ao retomar

> ⚠️ **Superado em 07/08/2026** — o que se segue descreve o estado no fim da
> sessão de 06/08. O trabalho foi publicado no dia seguinte; a `security/fecha-api`
> já não existe. Ver a sessão de 07/08 no topo deste ficheiro.

O trabalho está em `security/fecha-api`, **não fundido em `master` e não
empurrado**. Nada foi publicado: produção continua com a API aberta e o modelo
antigo até haver deploy.

**Sequência obrigatória ao publicar** (fora de ordem, o site cai):

1. Railway: definir `VIA_LEITE_API_KEYS` e `VIA_LEITE_ENV=production`
2. Railway: deploy do backend
3. Vercel: definir `VIA_LEITE_API_URL` e `VIA_LEITE_API_KEY`
4. Vercel: deploy do frontend
5. Confirmar o site e depois `/health`

Detalhe completo em `DEPLOY.md`. Chave gerada nesta sessão está no gestor de
senhas do Fagner — não ficou no repositório.

---

## SESSION UPDATE — VIA LEITE SENSE
**Data:** 18/06/2026
**Desenvolvedor:** Fagner Vieira — USINA I.A.

---

### O que foi feito (Sprint 4 — Radar de Risco + ESG, integração dos pacotes docs/sprint4)

Integração dos pacotes externos `via-leite-docs` e `via-leite-sprint4` ao projeto,
com correção de incompatibilidades de schema.

- **`score_risco.py`** (novo, raiz) — motor de scoring 0–100, 7 dimensões de risco,
  classe de risco e impacto econômico estimado. Inclui camada de aliases
  (`ALIASES_COLUNA`) que mapeia o schema real (`temp_tanque_c`, `litros_descartados`,
  `temp_med_c`) para os nomes canônicos do scoring.
- **`pages/1_Radar_de_Risco.py`** (novo) — página executiva principal (KPIs, gauge,
  mapa de calor, ranking, horizonte 7/15/30 dias). Loader corrigido para
  `fact_producao_produtor_dia.csv` e merge de clima por `["data","polo_climatico"]`.
- **`pages/13_Antes_Depois_ESG.py`** (novo) — painel ROI antes/depois + narrativa ESG.
- **Renumeração das páginas** — Radar inserido logo após a landing
  (`0_Conheça` → `1_Radar` → `2_Executivo` → … → `12_Demonstração` → `13_ESG`);
  os 4 `page_link` internos da página Demonstração foram atualizados.
- **Documentação** — README da pasta docs adotado como `README.md` raiz; copiados
  `docs/visao_produto.md`, `roadmap.md`, `validacao_mercado.md`, `arquitetura_dados.md`;
  schema do `arquitetura_dados.md` corrigido para refletir os CSVs reais.

### Decisões técnicas tomadas (Sprint 4)

| Decisão | Justificativa | Alternativa descartada |
|---------|--------------|----------------------|
| Aliases de coluna no score_risco em vez de renomear os dados | `dashboard_common.py` e todas as páginas já dependem dos nomes atuais | Renomear colunas dos CSVs |
| Score passa a somar `target_risco_*` (bug do sprint4) | O código original buscava `risco_*` e os alvos binários nunca entravam no score | Manter cálculo só por THI/queda |
| Merge clima por `["data","polo_climatico"]` | Evita produto cartesiano (clima tem 1 linha por polo/dia) | Merge só por `data` |
| Radar como página `1_` (renumerar todas) | Reposicionamento: Radar é a 1ª tela pós-login | Slot livre no fim do menu |

### Validação
- `python score_risco.py` → OK (exporta 3 rankings em `artefatos_teste/`)
- Scoring contra base real (54.780 linhas): merge sem explosão, classes distribuídas, tanque/descarte ativos
- `py_compile` em todas as páginas alteradas → OK

---

## SESSION UPDATE — VIA LEITE SENSE
**Data:** 09/06/2026
**Desenvolvedor:** Fagner Vieira — USINA I.A.

---

### O que foi feito (Sprint 3 — Refinamentos de UI/UX)

- Renomeação dos arquivos de páginas para nomes em português com acentuação correta:
  - `10_Plano_de_Acao.py` → `10_Plano_de_Ação.py`
  - `11_Demo_Tour.py` → `11_Demonstração.py`
  - `7_VIA_LEITE_EDGE.py` → `7_Via_Leite_Edge.py`
  - `8_Painel_Executivo_VIA_LEITE_SENSE.py` → `8_Painel_Executivo.py`
- Sidebar nav premium: fonte consistente, hover suave, página ativa destacada (`dashboard_common.py`)
- Fix timer do Demo Tour: cronômetro JS client-side (remove sleep+rerun que crashava o servidor)
- Renomeação da entrada "via leite app" para "Início" no menu lateral via JS MutationObserver
- Solução final: JS em `components.html` + `window.parent` para garantir renomeação robusta

### Decisões técnicas tomadas

| Decisão | Justificativa | Alternativa descartada |
|---------|--------------|----------------------|
| JS em components.html via window.parent para renomear menu | Streamlit não expõe API para alterar nome da app no menu; MutationObserver no iframe não alcança o frame pai | Tentar via st.markdown com target iframe |
| Timer JS client-side no Demo Tour | sleep()+rerun() causava crash e comportamento imprevisível no Streamlit | Loop rerun com sleep no servidor |

### Estado anterior → Estado atual
- **Antes:** Páginas com nomes em inglês/misturados, timer do Demo Tour instável, menu mostrando "via leite app"
- **Depois:** Nomes em português corretos, timer estável client-side, menu exibe "Início"

### Arquivos modificados
- `dashboard_common.py` — sidebar premium + JS MutationObserver + solução window.parent
- `pages/11_Demonstração.py` — timer JS client-side, renomeado
- `pages/10_Plano_de_Ação.py` — renomeado
- `pages/7_Via_Leite_Edge.py` — renomeado
- `pages/8_Painel_Executivo.py` — renomeado

### Problemas encontrados e resoluções

| Problema | Causa | Solução aplicada |
|----------|-------|-----------------|
| MutationObserver não renomeava o menu | JS no iframe não acessa o frame pai por segurança | JS injetado em components.html com window.parent.document |
| Timer crashava o servidor | sleep()+rerun() em loop no Streamlit é bloqueante | setInterval JS puro no client-side |

### Próximos passos (ordenados por prioridade)
1. [ ] Fazer push para o GitHub e verificar deploy no Streamlit Cloud
2. [ ] Testar Demo Tour completo no ambiente de produção
3. [ ] Validar Export PDF no Streamlit Cloud (verificar se fpdf2 está no requirements.txt)
4. [ ] Adicionar dados reais de produtores piloto ao sistema
5. [ ] Integrar ingestão automática de dados INMET para predição climática

### Bloqueios ativos
- Nenhum

### Dependências externas
- Streamlit Cloud: https://via-leite-sense.streamlit.app
- GitHub: https://github.com/usinaconsultoriaeminteligencia/via-leite-sense

---

*Registrado por Claude — USINA I.A.*

---

# HANDOFF — VIA LEITE SENSE — 09/06/2026

## Estado Atual
Projeto deployado e funcional em produção. Sprint 1, Sprint 2 e Sprint 3 concluídos.

**URL:** https://via-leite-sense.streamlit.app
**GitHub:** https://github.com/usinaconsultoriaeminteligencia/via-leite-sense
**Branch:** master | Último commit: f157a9d

---

## O que foi feito nesta sessão (Sprint 3)

### Score Premium Visual — CONCLUÍDO
- `pages/6_Fornecedores_360.py` — bloco visual premium no Detalhe do Fornecedor:
  - Gauge Plotly (indicator) com score 0–100, delta vs. médio e cor por classe de risco
  - Radar 4D (Volume, Qualidade, Logística, Continuidade) com fill colorido por classe
  - Cards KPI laterais com bordas coloridas (produção média, tendência, descarte/CCS/CBT)

### Modo Demonstração — CONCLUÍDO
- `pages/11_Demonstração.py` — tour guiado de pitch de 5 minutos:
  - 6 slides navegáveis com ◀ / ▶ e barra de progresso
  - Cronômetro JS client-side por slide com meta de tempo e alerta de estouro
  - Roteiro do apresentador (3 pontos por slide: contexto, ação, frase de efeito)
  - Links diretos para cada módulo demonstrado ao vivo
  - Mapa do pitch na sidebar com slide ativo destacado em verde

### Exportar PDF — CONCLUÍDO
- `relatorio_pdf.py` — módulo FPDF2 com relatório A4 profissional

### Refinamentos UI/UX — CONCLUÍDO (Sprint 3 final)
- Nomes de páginas em português com acentuação correta
- Sidebar nav premium com fonte consistente e hover suave
- Menu lateral exibe "Início" em vez de "via leite app"

---

## Para Continuar — Próxima Ação Imediata

```bash
cd "C:\Users\Novou\Desktop\USINA\Via Leite"
git push origin master
# Verificar deploy automático no Streamlit Cloud
```

Depois verificar se `fpdf2` está no `requirements.txt` — necessário para Export PDF funcionar em produção.

---

## Decisões Técnicas Já Tomadas (não reverter sem justificativa)
| Decisão | Motivo |
|---------|--------|
| Timer JS client-side no Demo Tour | sleep+rerun crashava o servidor Streamlit |
| JS em components.html via window.parent | Único método que alcança o frame pai para renomear o menu |
| FPDF2 para geração de PDF | Sem dependências de sistema (wkhtmltopdf etc.), compatível com Streamlit Cloud |

---

## Comandos para Iniciar
```bash
cd "C:\Users\Novou\Desktop\USINA\Via Leite"
streamlit run via_leite_app.py
```
