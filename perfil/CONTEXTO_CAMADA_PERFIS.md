# Handoff p/ Claude Code — Camada de Perfil do Produtor (Via Leite Sense)

> Documento de contexto para retomar no Claude Code, onde há acesso direto ao
> código e à documentação do projeto. Destila uma sessão de estratégia.
> **Objetivo:** confrontar estas decisões com a verdade do código e decidir implementação.

---

## 1. O que motivou esta camada

Pesquisa **MilkPoint, 12/06/2026** (Gonçalves, 2025 — dados reais: 2.002 produtores,
16.362 análises, noroeste do RS) provou via clustering que **não existe "o produtor
de leite"**: há perfis distintos, e cada um exige estratégia de manejo própria.
Assistência técnica genérica destrói resultado.

**Insight central:** o Via Leite hoje entrega 1 eixo (Score de Risco = preditivo,
"QUANDO agir"). A pesquisa opera em outro eixo (perfil estrutural = "COMO agir").
Combiná-los transforma recomendação genérica em cirúrgica.

| | Score de Risco (já existe) | Perfil (a adicionar) |
|---|---|---|
| Pergunta | "Quem está em risco agora?" | "Que TIPO de produtor é este?" |
| Natureza | Dinâmica/temporal/preditiva | Estrutural/lenta/descritiva |
| Uso | Quem visitar esta semana | Que acompanhamento dar |

---

## 2. Decisões de design já tomadas (com fundamento)

**D1 — Classificação por REGRA, não clustering sobre dados sintéticos.**
Rodar K-Means na base sintética geraria perfis que são artefato do próprio gerador,
não descoberta real. A banca derrubaria. Decisão: classificar por regra de negócio
ancorada na **IN 77** (limites regulatórios reais) + receitas de manejo da pesquisa.
Quando houver dados REAIS (pipeline de piloto já existe no repo), aí sim clustering
de verdade faz sentido.

**D2 — Ancorar na direção fisiológica + IN 77, não na numeração da tabela.**
A publicação tem inversão: o texto chama Cluster 1 de "melhor", mas a Tabela 1 mostra
o Cluster 3 com menor CCS (536), maior produção e melhores sólidos. Não propagar o erro.
Régua = menor CCS + menor CBT + maior sólidos = melhor. Cortes pela IN 77.

**D3 — Para o AgroStartup (27/06): roadmap + mini-protótipo isolado, NÃO feature no app.**
A 3 dias do prazo, não mexer no que funciona. Mini-protótipo é função autônoma,
testável à parte. Plugar no Streamlit só depois.

---

## 3. ACHADO IMPORTANTE do mini-protótipo (validar no código)

Ao aplicar os centroides reais da pesquisa ao classificador ancorado na IN 77,
**os 3 clusters caíram fora do limite de CCS da IN 77 (500 mil/mL)** — mesmo o melhor
(536) está +7%. Ou seja: a pesquisa segmenta produtores que em maioria já perderiam
bônus pela régua regulatória.

Implicação de produto: existem DUAS réguas diferentes e o produto deve usar AMBAS em camada:
- **Régua absoluta (IN 77):** ele perde dinheiro AGORA? (bonificação/penalização)
- **Régua relativa (perfil entre pares):** como ele se compara à carteira? (estratégia)

> **Para confrontar no Claude Code:** como o score atual trata CCS/CBT? Usa corte
> absoluto IN 77, relativo, ou outro? A camada de perfil precisa se alinhar a isso.

---

## 4. Perguntas em aberto que SÓ o código responde

1. **CV de produção existe?** A separação Consistente vs. Oscilante depende do
   coeficiente de variação da produção por produtor (série temporal). A base
   (sintética atual / pacote real) tem isso? Ver `gerador_leite_sintetico.py`,
   `fact_producao`, `treino_mvp_avancado.py`.
2. **Como o score é construído hoje?** 7 dimensões mencionadas no deck. Quais são,
   como são ponderadas? Ver `fornecedor_inteligencia.py`, `dashboard_mvp_avancado.py`.
3. **Onde a camada de perfil plugaria** sem quebrar? Provável: página "Fornecedores 360"
   ou "Produtores". Avaliar acoplamento.
4. **Os artefatos do modelo** (`feature_importances.csv`) já expõem CCS/CBT como
   variáveis de peso? Isso conecta perfil ao modelo preditivo.

---

## 5. Ativo pronto (lógica de referência)

Função `classificar_perfil(ccs, cbt, solidos_totais, coef_variacao_producao)`
já construída e testada. Retorna: perfil (Consistente/Oscilante/Desafiador),
confiança, sinais interpretáveis e receita de manejo. Mais
`recomendacao_combinada(score, perfil)` que une os dois eixos.

Lógica resumida:
- qualidade_ok (CCS<=500 E CBT<=300) + estável (CV<=0.15) -> Consistente
- qualidade_ok + instável (CV>0.15) -> Oscilante
- CCS e CBT fora -> Desafiador
- 1 indicador fora -> Oscilante ou Desafiador conforme margem

Receitas por perfil (fundamentadas na pesquisa):
- Consistente: manutenção + captura de bonificação (investimento baixo)
- Oscilante: padronização de rotina/consistência (investimento baixo-médio)
- Desafiador: básico — ordenha, controle de mastite, nutrição (investimento médio)

> O código-fonte completo da função acompanha este handoff (classificador_perfil.py).

---

## 6. Próxima ação sugerida no Claude Code

1. Ler `dashboard_mvp_avancado.py`, `fornecedor_inteligencia.py`, `treino_mvp_avancado.py`
   e responder as 4 perguntas da seção 4.
2. Decidir, COM base no código: a camada de perfil entra como roadmap apenas (27/06)
   ou há janela segura para uma página isolada de demo?
3. Confirmar se o CV de produção é calculável; se não, operar perfil com 2 eixos
   (qualidade IN 77 + sólidos) e marcar CV como "ativa com dados reais".
