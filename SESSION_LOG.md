# HANDOFF — VIA LEITE SENSE — 07/06/2026

## Estado Atual
Projeto deployado e funcional em produção. Sprint 1 e Sprint 2 concluídos.

**URL:** https://via-leite-sense.streamlit.app
**GitHub:** https://github.com/usinaconsultoriaeminteligencia/via-leite-sense
**Branch:** master | Último commit: f367bb2

---

## O que foi feito nesta sessão

### Sprint 1 — CONCLUÍDO
- `via_leite_app.py` — landing page profissional (hero, KPIs, 5 feature cards, branding verde agro + azul técnico)
- `auth.py` — autenticação nativa com bcrypt + st.session_state, sem dependência externa
  - 3 perfis: admin / laticinio / demo
  - Anti-brute-force: bloqueio 60s após 5 tentativas
  - Credenciais: demo/demo2025 · laticinio/leite2025 · admin/usina2025
- `dashboard_common.py` — guard `_guard_autenticacao()` em `carregar_contexto()` protege todas as páginas
- `requirements.txt` — versões pinadas, pronto para Streamlit Cloud
- `.gitignore` — segredos, dados multi-tenant e .duckdb excluídos
- `DEPLOY.md` — passo a passo completo Streamlit Cloud
- `gerar_senhas.py` — utilitário bcrypt para secrets.toml

### Fixes aplicados em produção
- `gestor_store.py` — fallback DuckDB: `ConnectionException` → reabre sem `read_only`
- `auth.py` + `dashboard_mvp_avancado.py` — corrigido `StreamlitDuplicateElementId` botão Sair
- `.streamlit/config.toml` — tema escuro nativo alinhado com landing
- CSS inputs — seletores específicos + `-webkit-text-fill-color` para legibilidade

### Sprint 2 — CONCLUÍDO
- `pages/9_Onboarding.py` — Wizard 4 etapas
  - Identificação (polo, sistema, tecnificação)
  - Produção & Qualidade (CCS, CBT, temp tanque, descarte, antibiótico)
  - Logística & Clima (distância, pavimentação, sensibilidades)
  - Diagnóstico: score 0–100, gauge Plotly, radar 4D, plano automático
- `pages/10_Plano_de_Acao.py` — Plano de Ação por Produtor
  - 15 prompts técnicos por dimensão (Qualidade/Volume/Logística/Continuidade/Operacional/Relacionamento)
  - Cada prompt: 5 passos de caminho + evidência sugerida + prazo padrão
  - Clicar no prompt preenche o formulário automaticamente via session_state
  - Persistência DuckDB (tabela planos_acao)
  - Painel geral com KPIs, gráficos e alerta de atrasados

---

## Arquivos modificados nesta sessão
- `via_leite_app.py` — entry point + landing page
- `auth.py` — autenticação nativa
- `dashboard_common.py` — guard + tema
- `dashboard_mvp_avancado.py` — remove sidebar duplicado
- `gestor_store.py` — fix DuckDB cloud
- `.streamlit/config.toml` — tema escuro
- `requirements.txt` — dependências pinadas
- `.gitignore` — criado
- `DEPLOY.md` — criado
- `gerar_senhas.py` — criado
- `pages/9_Onboarding.py` — criado
- `pages/10_Plano_de_Acao.py` — criado (com prompts inteligentes)

---

## Próximos passos — Sprint 3 (08–16/06)

### Prioridade ALTA (antes da tutoria 09/06)
1. [ ] Testar todas as 8 páginas logado como `demo` no Streamlit Cloud
2. [ ] Verificar se Onboarding (pág 9) e Plano de Ação (pág 10) aparecem no menu lateral

### Prioridade ALTA (Sprint 3 — antes de 16/06)
3. [ ] **Score Premium Visual** — card gauge na página Fornecedores 360 (`pages/6_Fornecedores_360.py`)
4. [ ] **Modo Demonstração** — tour guiado com highlights para pitch de 5 min
5. [ ] **Exportar PDF** — relatório executivo de 1 página por fazenda

### Prioridade MÉDIA (antes de 27/06)
6. [ ] Painel comparativo antes/depois de intervenção
7. [ ] Narrativa ESG — cálculo de redução de descarte
8. [ ] Refinamento visual — consistência de cores em todas as páginas
9. [ ] Ensaio do pitch — roteiro de 5 min com URL ao vivo

---

## Comandos para retomar
```powershell
cd "C:\Users\Novou\Desktop\USINA\Via Leite"
streamlit run via_leite_app.py
# Login: demo / demo2025

git log --oneline -8   # ver histórico
git push               # enviar para Streamlit Cloud
```

## Secrets do Streamlit Cloud (hashes reais gerados nesta sessão)
```toml
[auth.credentials.usernames.demo]
password = "$2b$12$paN5Cvhg03D1HqOLkP61HeRebC7yRbW3RXr1Thx323LHY8WBarMaG"

[auth.credentials.usernames.laticinio]
password = "$2b$12$zANqNcUmVOmEQpJvS03fSOr2Vhg05GrRLbZnKD9VVKns2CpNf0Maa"

[auth.credentials.usernames.admin]
password = "$2b$12$1xdCxsiuTOkhaWsRhAptNOdFTzP0t1qQvukCHnsAgP/k4UjEiAdmO"

[auth.cookie]
name        = "via_leite_session"
key         = "vls2025maratonafatesgsenai32chars"
expiry_days = 1
```

## Alertas ativos
- Nenhum bloqueador crítico
- DuckDB em cloud: o fallback está funcionando mas monitorar
- Páginas 9 e 10 ainda não foram testadas no Streamlit Cloud

---
*Sessão encerrada em 07/06/2026 — USINA I.A. | Fagner Vieira*
