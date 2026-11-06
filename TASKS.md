# TASKS — Via Leite Sense

> Atualizado em 06/11/2026. Ordem = prioridade. Contexto em `CONTEXT.md`.

## P0 — fazer primeiro

- [ ] **Pedir ao suporte do GitHub a remoção do PR #2 e dos commits órfãos** (Fagner, pela conta
      dona do repositório; formulário de remoção de dados sensíveis em support.github.com).
      Citar o repositório `usinaconsultoriaeminteligencia/via-leite-sense`, o `refs/pull/2/head`
      e os commits `74c1710`, `363b6ff`, `dfa8e5d`, `e9bbcce`, `73c4c54` (arquivo
      `docs/plano_de_trabalho/conteudo.py`). Em 06/11 o commit `73c4c54` ainda abria pelo hash.
- [ ] **Fora da rede da faculdade** (casa ou hotspot do celular): a rede "WiFi-Alunos" bloqueia
      `railway.com` por DNS (resolve para 69.46.46.46); `backboard.railway.com` e `up.railway.app` passam.
      Aproveitar a janela para ligar o auto-deploy GitHub → Railway (painel: Service › Settings ›
      Source › Connect Repo, branch `master`). Depois disso, push no GitHub já publica, inclusive da faculdade.
- [ ] **`railway login` (Fagner) e depois `railway up --ci`.** Conferir `/health`, as 7 dimensões e
      `/api/model/metrics` (MAE 24,47) em produção. Autorizado em 20/10.

## P1

- [ ] **Apagar o app `via-leite-sense` em share.streamlit.io** (Fagner). Desde 06/11 o repositório
      não tem mais o `via_leite_app.py`, e o app mostrava login em vez de redirecionar.
- [ ] Conferir para onde aponta o QR code da tela 13 do pitch; se for `streamlit.app`, trocar por
      `https://via-leite-sense.vercel.app`.

- [ ] Registrar o resultado do Demo Day (29/10) e o próximo marco do AgroStartup.
- [ ] Commitar o material do Demo Day: `docs/ROTEIRO_DEMODAY_VIA_LEITE_SENSE.md/.pdf`,
      `docs/PITCH_DEMODAY_VIA_LEITE_SENSE.pdf`, `docs/PREVIA_SLIDES_DEMODAY.png`,
      `docs/PROMPTS_IMAGENS_PITCH.md`. Decidir se `BRIEFING_DEMODAY_2026-10-20.md`
      (uso interno, tem a lista "Não dizer") entra no repositório público ou no `.gitignore`.
- [ ] Decidir o destino de `docs/apresentacao_pi/PACOTE_VIA_LEITE_SENSE_PI.zip` (17 MB):
      não versionar zip; conferir se tem dado pessoal.

- [ ] **Artigo do PI:** executar `docs/projeto_integrador/ATUALIZACOES_ARTIGO_2026-11-06.md`
      (por matéria; banca 12/12). Atualizar à mão o dossiê e o escopo `.docx` para 24,47 / 22,4%.
- [ ] Alinhar `xgboost` no `requirements.txt` (declara `<3.0`; ambiente roda 3.4.0).

## P2

- [ ] C2 e C4: sobreposição de dimensões (CCS ≥ 500 mil soma 45 pontos) e proveniência dos pesos,
      com análise de sensibilidade.
- [ ] Fase D: planilhas reais de 2 a 3 produtores via SENAR, com NDA, como validação externa.
- [ ] Fase F: pacote `via_leite/assistente/` (templates revisados pela veterinária → interpretação
      da mensagem → gravação via `ingest` → adaptador WhatsApp por último).
- [ ] Documentos externos que ainda serão reenviados: usar "24,5 contra 31,5, cerca de 22%"
      (vigente desde 06/11). Não reescrever o que já foi entregue.

## Backlog

- [ ] ALERTA-008: auto-deploy GitHub → Railway/Vercel.
- [ ] Fase 3 da limpeza (`dados_teste` → `data/reference`, `artefatos_teste` → `data/artifacts`;
      mudar `MVP_DATA_DIR`/`MVP_ARTEFATOS_DIR` na Railway **antes** do deploy).
- [ ] ALERTA-012: senha `usina2025` recuperável no histórico público.
- [ ] Achados A1, A3, C5, C6, G1, G2, G3; órfão `perfil/`.
- [ ] VAE/GAN para dados sintéticos: só a pedido do Fagner.

## Feito recentemente

- [x] 06/11 — Streamlit removido do repositório (redirect, `.streamlit/`, `.devcontainer/`, dependência,
      config do preview); o comando morto `subir_dashboard.ps1` saiu do onboarding.
- [x] 06/11 — Correção das janelas móveis integrada (`da1d6d9`), retreinada e com push no `master`: MAE 24,47 / 22,4%.
- [x] 06/11 — Branch público `fix/rolling-por-produtor` (com CPF) apagado; worktree e branches locais removidos.
- [x] 06/11 — `.gitignore` passa a excluir `entrega 12_10_26/` e o `.zip` (Plano assinado com CPF).
- [x] 23/10 — Roteiro do pitch alinhado às 13 telas; pitch em PDF; prompts de imagem.
- [x] 20/10 — C1 fechado (`111bf80`, `beb0760`, `aa7e753`); push com limpeza do `master`.
