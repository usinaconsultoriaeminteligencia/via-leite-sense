# CONTEXT — Via Leite Sense

> Resumo de retomada. **Atualizado em 06/11/2026.** O detalhe verificado está em
> `docs/ESTADO_REAL.md`; o histórico, em `SESSION_LOG.md`; as tarefas, em `TASKS.md`.
> Se algo aqui divergir do código, o código vence.

## O que é

Plataforma B2B2F de risco de qualidade e previsão de volume de leite por fornecedor, para
laticínios e cooperativas, com foco em Goiás. Equipe de 5 (Fagner, Maria Vitória/vet,
Diego Santana/eng, Matheus, Daianne). Participa do Desafio AgroStartup 2026 (SENAR/FAPEG).

## Arquitetura

| Camada | Onde | Deploy |
|---|---|---|
| API FastAPI + DuckDB, `X-API-Key` (só `/health` é público) | `via_leite/api/` | Railway, manual (`railway up --ci`) |
| SPA vanilla JS + proxy serverless que guarda a chave | `frontend/` | Vercel, manual (`vercel --cwd frontend --prod --yes`) |
| Score de risco (7 dimensões) | `via_leite/core/score_risco.py` | — |
| Modelo XGBoost de volume (7 dias) | `via_leite/models/treino_mvp_avancado.py` | — |
| Ingestão com guardas de escala e saturação | `via_leite/ingest/` | — |
| Referência pública de qualidade (RBQL, Zenodo 17714633) | `via_leite/ingest/referencia_qualidade_rbql.py` | — |

Base de treino: **sintética** (`dados_teste/`, 30 produtores, clima sintético). Não há dado
real de cliente; a Piracanjuba não cede dados (07/10). C1 foi calibrado pela IN 76/77 + RBQL.

## Números canônicos (não citar outros)

- MAE de teste **24,47** contra **31,54** do baseline: ganho de **22,4%** ("24,5 contra 31,5, cerca
  de 22% menor"). Vale desde 06/11 (janelas móveis por produtor). O material do Demo Day
  (até 23/10) cita "24,4 / cerca de 23%" e fica como registro histórico.
- Limiares em mil por mL: CCS 400/500, CBT 100/300 (500 e 300 = IN 76); tanque 4 °C (IN 77).

## Situação em 06/11/2026

- **Código:** `master` = `origin/master`, com o C1 (20/10) e a correção das janelas móveis
  (`da1d6d9`, 06/11). Push feito em 06/11.
- **Produção:** API viva (`/health` 200 em 06/11). **O score novo provavelmente não está no ar:**
  a Railway CLI continua sem login (token expirado desde 20/10), então nenhum deploy saiu desta máquina.
- **Demo Day:** foi em 29/10 (300 pontos, dupla Maria Vitória → Fagner, 13 telas). O resultado
  não está registrado no repositório.
- **Alerta P0 (parcialmente resolvido):** o branch público `fix/rolling-por-produtor`, com CPF e
  telefone de 4 pessoas, foi apagado em 06/11. O **PR #2** fechado ainda aponta para o commit
  `73c4c54`, que abre pelo hash: falta o pedido de remoção ao suporte do GitHub (Fagner).
- **Streamlit fora do projeto (06/11):** código, configuração e dependência removidos; a produção é
  só Vercel + Railway. O app no Streamlit Cloud ainda existe e mostra uma tela de login: apagar em
  share.streamlit.io (Fagner).
- **Vazamento do modelo corrigido** (`da1d6d9`, no `master`): as médias móveis de cada produtor
  herdavam os últimos dias do anterior.

## Decisões vigentes (não reverter sem motivo)

| Decisão | Motivo |
|---|---|
| C1 calibrado por norma + RBQL, sem dado de laticínio | Piracanjuba não cede dados; fonte pública e citável |
| `docs/plano_de_trabalho/` e `entrega 12_10_26*` fora do git | Têm CPF/telefone da equipe; o repositório é público |
| Branch `backup/pre-limpeza-cpf-20261020` só local | Contém os dados pessoais; nunca dar push |
| Correção das janelas trazida só como código + teste + `DECISIONS.md` | Os outros 5 commits do branch já estavam no `master` com hashes novos; o merge traria de volta a pasta com CPF, e os artefatos eram de antes do C1 |
| Material externo não leva auto-crítica | Ver `docs/BRIEFING_DEMODAY_2026-10-20.md` §4 ("Não dizer") |

## Comandos

```powershell
cd "C:\Users\Novou\Desktop\USINA\Via Leite"
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m uvicorn via_leite.api.app:app --reload
```

Variáveis (sem valores): `VIA_LEITE_API_KEYS` (Railway e Vercel), `MVP_DATA_DIR`,
`MVP_ARTEFATOS_DIR` (Railway). Ver `DEPLOY.md`.
