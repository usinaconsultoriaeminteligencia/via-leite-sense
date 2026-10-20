# Estado real do VIA LEITE SENSE

> Ponto de retomada do projeto. Separa **o que existe e roda** do que existe **só em
> documento**. Verificado em **20/10/2026** (código, `git log` e testes; produção conferida pela última vez em 07/10). Se algo aqui
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
  O número honesto é o ganho sobre o baseline: MAE 24,4 contra 31,5 (cerca de 23% menor; era 24,2 antes da calibração de C1 em 20/10/2026).
- **Possível vazamento a confirmar:** `score_sanidade` e `score_manejo` são variáveis que o
  gerador usa para criar a produção e aparecem entre as features.
- **Score (C1 fechado em 20/10/2026, ainda não publicado em produção):** as 7 dimensões
  discriminam (disparo entre 0,4% e 55,3%). Restam C2 (dimensões sobrepostas: um CCS
  ≥ 500 mil soma 45 pontos) e C4 (pesos sem proveniência). Ver §8.
- **Produção roda o score antigo** até um deploy autorizado: lá ainda valem as 4 dimensões
  mortas e o tanque saturado.
- **Deploy:** sem auto-deploy (ALERTA-008); a produção já divergiu do `master` por 8 dias.
- **Segurança:** a senha antiga ainda é recuperável do histórico Git e o repositório é público.

## 4. Datas e condicionantes

- **09/10/2026:** resultado da seleção (Desafio AgroStartup). O congelamento de produção
  terminou com a classificação (10/10).
- **Entrou entre os 36:** o SENAR dá contato direto com produtores; pedir planilhas reais
  (2 a 3 produtores, com NDA) como **validação externa**. Não é pré-condição de nada:
  o C1 foi calibrado sem elas. Ver fase D abaixo.
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
  de cerca de 23% no erro absoluto sobre o baseline.

## 7. Onde olhar

- Contexto de negócio: `docs/PLANO_DE_NEGOCIO.md`, `docs/visao_produto.md`
- Deploy e variáveis: `DEPLOY.md`
- Histórico de sessões: `SESSION_LOG.md`
- Plano de Trabalho FAPEG: `docs/plano_de_trabalho/`

## 8. Decisões registradas

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
| 20/10/2026 | **24,36** | **22,8%** | C1 fechado (`aa7e753`) — **número vigente** |

