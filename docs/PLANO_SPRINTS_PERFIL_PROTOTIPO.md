# Plano de Evolução — Camada de Perfil · Sprints · Revisão do Protótipo

> **Status:** plano (não executado). Documento de decisão para aprovar antes de mexer no app.
> **Contexto:** AgroStartup SENAR/SEBRAE GO em 27/06. App em produção (Streamlit Cloud)
> não deve ser alterado a poucos dias do prazo (decisão D3). A camada de perfil já tem
> mini-protótipo isolado validado em `perfil/`.

---

## 1. Plano de integração da Camada de Perfil no app (a executar pós-maratona)

**Objetivo:** levar o perfil estrutural (Consistente/Oscilante/Desafiador) do script
isolado para dentro do app, ao lado do Score de Risco, sem quebrar nada.

**Princípio:** acoplamento mínimo. O perfil é uma camada *aditiva* — só acrescenta
colunas/blocos; nenhuma lógica existente é alterada.

### Ponto de acoplamento (já mapeado no código)
- `fornecedor_inteligencia.calcular_scores_fornecedores()` devolve um DataFrame por
  produtor já com `ccs_media`, `cbt_media`, `score_risco_fornecedor`.
- É consumido por `pages/4_Produtores.py:22` e `pages/7_Fornecedores_360.py:20`.
- O CV de produção é calculável de `ctx.prod_f` (já disponível no contexto).

### Passos (ordem de execução, file-by-file)

1. **Promover o classificador a módulo do app.**
   Manter `perfil/classificador_perfil.py` como fonte única; criar `perfil_servico.py`
   na raiz que importe dele e exponha `enriquecer_com_perfil(scores_df, prod_df)`
   → adiciona colunas `perfil`, `perfil_confianca`, `cv_producao`, `recomendacao_combinada`.
   (Reaproveita `calcular_cv_producao` de `perfil/perfil_demo.py`.)

2. **Cache.** Envolver `enriquecer_com_perfil` em `@st.cache_data` (mesma TTL das
   outras cargas) para não recalcular CV a cada interação.

3. **UI — página Produtores (`pages/4_Produtores.py`).**
   - Coluna **Perfil** (badge colorido) na tabela.
   - Filtro lateral por perfil.
   - Dispersão já existente (score_qualidade × score_volume) colorida por perfil.

4. **UI — Fornecedores 360 (`pages/7_Fornecedores_360.py`).**
   - No detalhe do produtor: badge de perfil + `receita['leitura']`/`acao'/`investimento'`.
   - Linha de **recomendação combinada** (Score × Perfil) — a entrega de valor "cirúrgica".

5. **Alinhar limiar de CBT (decisão de produto).**
   Hoje há 3 números: recomendação do fornecedor (180), `score_risco` (atenção 100 / alto 300),
   classificador (IN 77 = 300). Padronizar antes de unir as telas. Sugestão: usar **300 (IN 77)**
   como limite e **180** apenas como "alerta de bônus" nomeado.

6. **Relatório PDF (`relatorio_pdf.py`).** Incluir o perfil no relatório por produtor (opcional).

### Riscos e mitigação
| Risco | Mitigação |
|---|---|
| Recalcular CV pesa na interação | `@st.cache_data` + agregação vetorizada |
| Produtor com poucos dias (CV instável) | já tratado: CV `None` → confiança menor, perfil por qualidade |
| Sólidos ausentes | perfil opera com CCS/CBT + CV; sólidos "ativa com dados reais" |
| Divergência de limiar CBT | resolver no passo 5 antes da UI |

### Critério de pronto
Perfil visível nas duas páginas, distribuição coerente (3 perfis populados),
sem regressão nas telas existentes, recomendação combinada exibida.

---

## 2. Revisão do Protótipo — informações a incluir

O protótipo atual tem 9 páginas (capa, problema, radar, score, WhatsApp, mercado,
concorrência, posicionamento, QR). Lacunas identificadas para o pitch:

| Prioridade | Slide a adicionar | Por quê |
|---|---|---|
| **ALTA** | **Perfil do Produtor** (Consistente/Oscilante/Desafiador) | Novo diferencial; "score diz QUANDO agir, perfil diz COMO agir". Mostra profundidade técnica. |
| **ALTA** | **Modelo de negócio / Como cobramos** | A banca pergunta "como ganham dinheiro?". Hoje só há TAM/SAM/SOM, sem o modelo (assinatura por produtor pago pelo laticínio). |
| MÉDIA | **Roadmap visual** (Fases 1 → 4 + 3.5) | Mostra visão de evolução e maturidade do plano. |
| MÉDIA | **Impacto / ROI (Antes & Depois)** | Existe no app mas não no PDF; traduz valor em R$. |
| BAIXA | **Equipe com papéis** | Nomes já estão na capa; um slide com papéis reforça credibilidade. |

**Proposta mínima para o 27/06:** adicionar **Perfil do Produtor** + **Modelo de negócio**
(as duas ALTA). As demais entram em revisão posterior.

### Esboço do slide "Perfil do Produtor"
- Conceito de 2 eixos (Score × Perfil) — tabela curta.
- Os 3 perfis com cor, leitura e receita de manejo (Consistente/Oscilante/Desafiador).
- Mini-resultado real: "na carteira de demonstração: 16 Consistentes · 11 Oscilantes · 3 Desafiadores".
- Frase: "Assistência técnica genérica destrói resultado; o perfil torna a recomendação cirúrgica."
- Fonte: Gonçalves (2025) / MilkPoint — 2.002 produtores, 16.362 análises.

### Esboço do slide "Modelo de negócio"
- Quem paga: laticínio/cooperativa (B2B), por produtor monitorado.
- Faixa: R$ ~60/produtor/mês (já usada no TAM/SAM/SOM) — coerência com a página de mercado.
- Camadas: básico (radar) · pro (perfil + plano de ação) · enterprise (IoT/API).
- Por que o laticínio paga: protege qualidade da carteira e reduz perdas.

---

## 3. Organização de Sprints

### Sprint 4.5 — Pré-maratona (até 27/06) · APENAS protótipo e roadmap
**Objetivo:** fortalecer o pitch sem tocar no app em produção.
- [ ] Adicionar slide **Perfil do Produtor** ao protótipo PDF.
- [ ] Adicionar slide **Modelo de negócio** ao protótipo PDF.
- [ ] (opcional) slide de Roadmap.
- **Conclusão:** PDF atualizado; app intacto.

### Sprint 5 — Integração da Camada de Perfil no app (pós-27/06)
**Objetivo:** executar o Plano da seção 1.
- [ ] `perfil_servico.py` (`enriquecer_com_perfil`) + cache.
- [ ] Perfil nas páginas Produtores e Fornecedores 360.
- [ ] Padronizar limiar de CBT.
- [ ] Recomendação combinada (Score × Perfil) na UI.
- **Conclusão:** perfil em produção, sem regressão.

### Sprint 6 — Piloto com dados reais (Fase 2 do roadmap)
**Objetivo:** validar perfil e score com 1 laticínio/cooperativa real.
- [ ] Onboarding de dados reais (pipeline já existe: `executar_piloto_real.py`).
- [ ] Habilitar **sólidos totais** (gordura/proteína) no perfil quando vierem nos dados.
- [ ] **Clustering real** (K-Means) para confrontar com a regra IN 77.
- [ ] Re-treino do modelo com sazonalidade real.
- **Conclusão:** 1 piloto com 30 dias de dados reais e evidência de impacto.

### Sprint 7 — Assistente no WhatsApp (comunicação produtor ↔ cooperativa)
**Objetivo:** tirar o conceito do protótipo e torná-lo real.
- [ ] WhatsApp Cloud API + webhook → motor de risco/perfil.
- [ ] Alertas traduzidos + lançamento de dados por mensagem.
- [ ] Notificação da cooperativa por ranking de prioridade.
- **Conclusão:** 1 produtor recebendo alerta real e respondendo dados.
- **Ref.:** backlog em memória (`backlog-comunicacao-produtor-ux-marca`).

### Sprint 8 — VIA LEITE EDGE / IoT real (Fase 4)
**Objetivo:** substituir IoT simulado por sensores reais (tanque, THI local).
- [ ] MQTT → FastAPI → dashboard.
- **Conclusão:** ≥3 fazendas transmitindo em tempo real.

---

## 4. Dependências e sequência

```
Sprint 4.5 (protótipo)  ──►  27/06 maratona
Sprint 5 (perfil no app) ──► depende de: decisão de limiar CBT
Sprint 6 (piloto real)   ──► depende de: parceiro + dados reais (habilita sólidos/clustering)
Sprint 7 (WhatsApp)      ──► depende de: número WhatsApp Business + backend
Sprint 8 (IoT)           ──► depende de: hardware em campo
```

---

*Plano — VIA LEITE SENSE | revisão antes da execução.*
