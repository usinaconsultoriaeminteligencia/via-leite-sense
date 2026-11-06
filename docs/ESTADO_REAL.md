# Estado real do VIA LEITE SENSE

> Ponto de retomada do projeto. Separa **o que existe e roda** do que existe **só em
> documento**. Verificado em **06/11/2026** (`git log`, branches e `/health` de produção; testes rodados pela última vez em 20/10). Se algo aqui
> divergir do código, o código vence. Atualizar este arquivo a cada marco.

## 1. Existe e roda (verificado)

| Componente | Onde | Evidência |
|---|---|---|
| API FastAPI com autenticação `X-API-Key` (só `/health` é público) | `via_leite/api/` | `/health` 200 e `/portfolio` sem chave 401, em 07/10/2026 |
| Proxy serverless e SPA | `frontend/` (Vercel) | `/api/health` 200 |
| Score de risco (7 dimensões) | `via_leite/core/score_risco.py` | ver limitações abaixo |
| Modelo XGBoost de volume (horizonte 7 dias) | `via_leite/models/treino_mvp_avancado.py` | `/api/model/metrics` |
| Ranking por fornecedor, rota e laticínio | `via_leite/core/fornecedor_inteligencia.py` | SPA em produção |
| Relatório PDF por fornecedor | `via_leite/api/relatorio_pdf.py` | 200, `application/pdf` (02/09) |
| Ingestão com guarda de escala e saturação | `via_leite/ingest/guarda_ingestao.py` | 69 testes passam; guarda de saturação ativa desde 20/10 |
| Referência pública de qualidade (RBQL, Zenodo 17714633) | `via_leite/ingest/referencia_qualidade_rbql.py` | `tests/test_referencia_qualidade_rbql.py` |

## 2. Existe SÓ em documento (não há código no produto)

| Funcionalidade | Onde está descrita | Estado |
|---|---|---|
| Assistente no WhatsApp (alerta ao produtor) | Pág. 06 do `prototipo/VIA_LEITE_SENSE_Prototipo.pdf` ("PRÓXIMA FASE" / "Conceito"), `docs/visao_produto.md`, Plano FAPEG (tarefa S4) | **Mockup.** Nenhuma integração com WhatsApp |
| Linguagem traduzida (CCS/CBT em recado simples) | Pág. 06 do protótipo | Não implementada |
| Interpretar a resposta do produtor ("hoje tirei 380 litros") | Pág. 06 do protótipo | Não implementada |
| Aviso automático à cooperativa | Pág. 06 do protótipo | Não implementado (a indústria vê a priorização na tela) |
| Alerta com até 30 dias de antecedência | Vídeo de pitch (2:59) | Há alvos de queda de 7/15/30 dias, só em base sintética; sem evidência em dado real |
| "Clinicamente seguro" | Vídeo de pitch | Sem validação clínica no repositório |
| Biblioteca de recomendações sanitárias (ex.: "lave e seque o úbere") | Pág. 06 do protótipo | Não existe; precisa de validação da veterinária |

Não há biblioteca de LLM, de WhatsApp nem pacote de mensagens em `requirements*.txt`,
`pyproject.toml` ou `via_leite/`.

## 3. Limitações conhecidas do que roda

- **Dados:** o modelo é treinado e validado em **base sintética** (`dados_teste`, gerada por
  `via_leite/models/gerador_leite_sintetico.py`). Não há dado real de cliente. A Piracanjuba
  não enviará dados (informado em 07/10/2026).
- **Métricas:** o R² de 0,994 não informa, pois o baseline (média móvel de 7 dias) tem 0,990.
  O número honesto é o ganho sobre o baseline: MAE 24,5 contra 31,5 (cerca de 22% menor). Era 24,2 até 20/10 e 24,4 até 06/11; material externo anterior a 06/11 cita "24,4 / cerca de 23%".
- **Vazamento entre produtores (corrigido em 06/11/2026):** as médias e desvios móveis
  (`mm_*`, `std_*`) eram calculados sobre o DataFrame inteiro, e os primeiros dias de cada
  produtor herdavam os últimos do anterior. Correção de 11/10 trazida para o branch
  `fix/janelas-moveis` e retreinada sobre a base do C1 (`da1d6d9`, no `master`; produção ainda não). Ver `docs/DECISIONS.md`.
- **Possível vazamento a confirmar:** `score_sanidade` e `score_manejo` são variáveis que o
  gerador usa para criar a produção e aparecem entre as features.
- **Score (C1 fechado em 20/10/2026, ainda não publicado em produção):** as 7 dimensões
  discriminam (disparo entre 0,4% e 55,3%). Restam C2 (dimensões sobrepostas: um CCS
  ≥ 500 mil soma 45 pontos) e C4 (pesos sem proveniência). Ver §8.
- **Produção roda o score antigo** até um deploy autorizado: lá ainda valem as 4 dimensões
  mortas e o tanque saturado.
- **Streamlit removido (06/11/2026):** a página de redirect, o `.streamlit/`, o `.devcontainer/` e a
  dependência saíram do repositório. O app `via-leite-sense.streamlit.app` já não redirecionava:
  mandava o visitante para o login do Streamlit. Falta o Fagner apagá-lo em share.streamlit.io.
- **Deploy:** sem auto-deploy (ALERTA-008); a produção já divergiu do `master` por 8 dias.
- **Segurança:** a senha antiga ainda é recuperável do histórico Git e o repositório é público.
- **Dados pessoais no GitHub (06/11/2026):** o branch `fix/rolling-por-produtor`, publicado antes
  da limpeza de 20/10, versionava `docs/plano_de_trabalho/conteudo.py` com CPF e telefone da
  equipe. O branch foi apagado em 06/11, mas o **PR #2** (fechado) mantém `refs/pull/2/head` e o
  commit `73c4c54` continua abrindo pelo hash. Só o suporte do GitHub remove. Ver §8.

## 4. Datas e condicionantes

- **09/10/2026:** resultado da seleção (Desafio AgroStartup). O congelamento de produção
  terminou com a classificação (10/10).
- **Entrou entre os 36:** o SENAR dá contato direto com produtores; pedir planilhas reais
  (2 a 3 produtores, com NDA) como **validação externa**. Não é pré-condição de nada:
  o C1 foi calibrado sem elas. Ver fase D abaixo.
- **29/10/2026:** Demo Day (300 pontos pelo resultado preliminar de 22/10; 3 min + 2 min, dupla
  Maria Vitória → Fagner, 13 telas). Roteiro em `docs/ROTEIRO_DEMODAY_VIA_LEITE_SENSE.md`.
  **Resultado ainda não registrado aqui.**
- VAE/GAN (dados sintéticos mais realistas) está guardado e só retoma a pedido do Fagner.

## 5. Próximos passos (depois de 09/10)

| Fase | O quê |
|---|---|
| E | Commit dos arquivos soltos e registro da decisão em `DECISIONS.md` e no `PROJECT_REGISTRY.json` |
| A | Auditar dados de treino e métricas (circularidade, vazamento). ~~C1 com limiares normativos~~ feito em 20/10 (§8) |
| B | Regras de plausibilidade no `guarda_ingestao.py` (inspiradas no Manual Lactaleite, §12.1) |
| C | Indicadores de gestão (custo por litro, vacas em lactação, produção por vaca e por hectare) |
| F | **Pacote `via_leite/assistente/`**: (1) templates de risco em texto simples revisados pela veterinária; (2) interpretação da mensagem do produtor (regras primeiro, LLM só nos casos ambíguos); (3) gravação pela camada `ingest` com validação; (4) adaptador do WhatsApp Cloud API por último. Os passos 1 a 3 dão para demonstrar sem WhatsApp, com endpoint simulado |
| D | Planilhas reais dos produtores, condicionada à classificação |
| G | Auto-deploy (ALERTA-008) e fase 3 da limpeza (`dados_teste` e `artefatos_teste`) |

## 6. Respostas prontas para a banca (honestas)

- **O WhatsApp já funciona?** O alerta existe como tela e relatório em PDF; o canal WhatsApp é
  o próximo marco, descrito como conceito desde o protótipo.
- **Com que dados validaram os 30 dias?** Em base sintética de referência. O piloto de 30 a 90
  dias é o que mede isso em dado real.
- **O que significa "clinicamente seguro"?** Os critérios de risco são definidos com a
  veterinária da equipe a partir de limiares normativos; a validação em campo vem no piloto.
- **O modelo foi treinado com dados reais?** Não. Foi validado em base sintética, com ganho
  de cerca de 22% no erro absoluto sobre o baseline.

## 7. Onde olhar

- Contexto de negócio: `docs/PLANO_DE_NEGOCIO.md`, `docs/visao_produto.md`
- Deploy e variáveis: `DEPLOY.md`
- Histórico de sessões: `SESSION_LOG.md`
- Plano de Trabalho FAPEG: `docs/plano_de_trabalho/`

## 8. Decisões registradas

### 06/11/2026 — Branch público com CPF e correção de modelo fora do `master`

- **Achado:** `origin/fix/rolling-por-produtor` (`73c4c54`, 11/10) parte do histórico **anterior**
  à limpeza de 20/10. Seus commits `74c1710`..`73c4c54` versionam `docs/plano_de_trabalho/`
  (7 arquivos), com CPF e telefone de 4 pessoas em `conteudo.py`. A limpeza reescreveu só o `master`.
- **Decisão:** integrar **só** `73c4c54` por cherry-pick num branch novo sobre o `master`; os outros
  cinco commits já estão no `master` com hashes novos (`c5902b4`, `2eae637`, `276fd87`, `e0c4fee`,
  `9e40cb2`). Merge descartado: traria a pasta de volta. Depois, apagar o branch remoto
  (precisa do OK do Fagner: é ação pública e irreversível) e pedir ao suporte do GitHub a remoção
  dos commits órfãos, que continuam acessíveis pelo hash.
- **Execução (06/11, com OK do Fagner):** código, teste e `docs/DECISIONS.md` de `73c4c54` trazidos
  para o `master` (`da1d6d9`, push em 06/11); os artefatos de 11/10 (base anterior ao C1) foram descartados e
  regenerados. `git push origin --delete fix/rolling-por-produtor` feito; worktree e branches locais
  removidos. **Pendente:** o PR #2 segue expondo o commit; pedido ao suporte do GitHub é do Fagner.
- **Efeito no número canônico:** MAE de teste **24,47** contra 31,54 (ganho de **22,4%**). O código
  antigo, no mesmo ambiente, dá 24,34, então os +0,13 L são efeito da correção e não do ambiente.
- **Prevenção:** `entrega 12_10_26/` e `entrega 12_10_26.zip` (Plano de Trabalho assinado) entraram
  no `.gitignore`.

### 20/10/2026 — C1 calibrado sem a Piracanjuba

- **Contexto:** a Piracanjuba não cederá dados (07/10). A decisão de 12/08, de calibrar o C1
  só com os dados dela, perdeu o gatilho.
- **Decisão:** calibrar com a norma (IN 76/77) e uma fonte pública e real: o dataset de
  qualidade da RBQL curado por Cravo et al. (WCAMA/CSBC 2026), Zenodo
  [10.5281/zenodo.17714633](https://doi.org/10.5281/zenodo.17714633), CC-BY 4.0.
- **Execução:**

| Commit | O quê |
|---|---|
| `111bf80` | Referência RBQL versionada com proveniência; achou um erro na fonte (ESD do RS em 2023) |
| `beb0760` | Limiares em **mil por mL**: CCS 400/500, CBT 100/300 (500 e 300 = IN 76) |
| `aa7e753` | Gerador: CBT de mediana 134 para 79 (GO real = 60); tanque acima de 4 °C de 94% para 29% |

- **Resultado:** nenhuma dimensão morta ou saturada; "Alto risco" + "Crítico" em 42% das
  linhas (era 0% em 05/08 e 71% só com a unidade corrigida). MAE de teste 24,36 contra
  31,54 do baseline (ganho de 22,8%).
- **Código no GitHub (push de 20/10, `aad85c3`); produção ainda não.** O deploy foi autorizado em
  20/10, mas a Railway CLI está sem login (token expirado). Falta: `railway login` (Fagner) e
  `railway up --ci`. Até lá, produção mostra o score antigo.
- **Limpeza antes do push:** os commits locais versionavam `docs/plano_de_trabalho/` com CPF e
  telefone da equipe. Foram refeitos sem a pasta (hashes mudaram), que agora está no
  `.gitignore`. Backup local com os dados: branch `backup/pre-limpeza-cpf-20261020` — nunca publicar.
- **Achado de reprodutibilidade:** a base versionada usa 30 produtores e clima sintético
  (o padrão do gerador é 2.400). Agora está em `--n-produtores`.

### Série do MAE de teste (para não citar número velho)

| Data | MAE teste | Ganho sobre baseline | Por quê mudou |
|---|---|---|---|
| até 06/08/2026 | 24,45 | 22,5% | Com CPF e razão social como features (A2) |
| 06/08/2026 | 24,17 | 23,4% | A2 fechado (`fa4ef0d`) |
| 20/10/2026 | 24,36 | 22,8% | C1 fechado (`aa7e753`) |
| 06/11/2026 | **24,47** | **22,4%** | Janelas móveis por produtor (`da1d6d9`) — **número vigente** |

