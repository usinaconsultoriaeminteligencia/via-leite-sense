# Estado real do VIA LEITE SENSE

> Ponto de retomada do projeto. Separa **o que existe e roda** do que existe **só em
> documento**. Verificado em **07/10/2026** (código, `git log` e produção). Se algo aqui
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
| Ingestão com guarda de escala e saturação | `via_leite/ingest/guarda_ingestao.py` | testes (63 passam, 1 xfail proposital) |

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
  O número honesto é o ganho sobre o baseline: MAE 24,3 contra 31,5 (cerca de 23% menor).
- **Possível vazamento a confirmar:** `score_sanidade` e `score_manejo` são variáveis que o
  gerador usa para criar a produção e aparecem entre as features.
- **Vazamento corrigido em 11/10/2026:** as médias móveis `mm_*`/`std_*` atravessavam a
  fronteira entre produtores (ver `docs/DECISIONS.md`); o alvo e o split não tinham o problema.
- **Score (C1):** 4 das 7 dimensões estão mortas (erro de unidade CCS/CBT) e
  `risco_temp_tanque` satura em 94,4% das linhas; só `risco_queda_producao` discrimina.
- **Deploy:** sem auto-deploy (ALERTA-008); a produção já divergiu do `master` por 8 dias.
- **Segurança:** a senha antiga ainda é recuperável do histórico Git e o repositório é público.

## 4. Datas e condicionantes

- **09/10/2026:** resultado da seleção (Desafio AgroStartup). Congelamento de produção até lá:
  não tocar em `security.py`, `via_leite/api/app.py`, `railway.json` nem no C1.
- **Se entrar entre os 36:** o SENAR dá contato direto com produtores, e só então se pedem
  planilhas reais (2 a 3 produtores, com NDA) para recalibrar. Ver fase D abaixo.
- VAE/GAN (dados sintéticos mais realistas) está guardado e só retoma a pedido do Fagner.

## 5. Próximos passos (depois de 09/10)

| Fase | O quê |
|---|---|
| E | Commit dos arquivos soltos e registro da decisão em `DECISIONS.md` e no `PROJECT_REGISTRY.json` |
| A | Auditar dados de treino e métricas (circularidade, vazamento); C1 com limiares normativos |
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
