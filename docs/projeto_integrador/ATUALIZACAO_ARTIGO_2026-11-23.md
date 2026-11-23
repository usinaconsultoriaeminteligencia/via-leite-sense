# Atualização do artigo — Projeto Integrador 2026-2 (Via Leite Sense)

**Autores:** Fagner Vieira, Daianne Valéria e Matheus Iverson · **Posição em:** 23/11/2026 · **Banca:** 12/12/2026

Este documento resume o que mudou no Via Leite Sense desde o plano do artigo (05/08) e o escopo apresentado em 10/10, e o que cada matéria já mediu. O detalhe está em `docs/projeto_integrador/artigo.md` (§13) e em `ATUALIZACOES_ARTIGO_2026-11-06.md`.

## 1. O que mudou desde 10/10

| # | Fato novo | Data | Onde entra no artigo |
|---|---|---|---|
| 1 | C1 fechado: limiares do score de risco calibrados pela IN 76/77 e pela base pública RBQL (Cravo et al., Zenodo 10.5281/zenodo.17714633), sem dado de laticínio | 20/10 | §2, §4, §6 |
| 2 | Achado novo A4: as médias móveis misturavam um produtor com o anterior (vazamento entre séries); corrigido com teste de regressão | 06/11 | C-2, §6.1, §5 |
| 3 | Números canônicos mudaram: 24,17 → 24,36 (C1) → 24,47 (A4) | 20/10 e 06/11 | §4.2, §5 |
| 4 | Validade da base sintética contra a RBQL: CCS mediana 392 mil/mL, igual à de Goiás (392); CBT sintética (79) ainda acima da de Goiás (60) | 20/10 | §4, §6.2 |
| 5 | Arquitetura simplificada: Streamlit removido; SPA (Vercel) + API FastAPI (Railway) + DuckDB | 06/11 | §3 |
| 6 | Código das quatro matérias técnicas implementado e executado em experimentos/ | 06/11 | §5, §6, §7 |
| 7 | Classificação entre as 36 startups do Desafio AgroStartup: rota de contato com produtores via SENAR | 10/10 | §6.2, §10.2 |

Agora são 13 achados da auditoria (A1–A4, C1–C6, G1–G3), e não 12.

## 2. Números vigentes (teste, 2025)

| Métrica | XGBoost | Baseline (MM7 com cascata) | Ganho |
|---|---|---|---|
| MAE (L) | 24,47 | 31,54 | 22,4 % menor |
| RMSE (L) | 37,01 | 48,57 | 23,8 % menor |
| MAPE | 3,63 % | 4,55 % | 0,93 ponto percentual |
| R² | 0,9943 | 0,9901 | não discrimina; não usar como argumento |

Cada correção da auditoria piorou um pouco o erro ou o deixou estável, e nunca o melhorou de forma artificial. É a evidência de que o protocolo de auditoria (C-2) funciona e reporta o custo das correções.

## 3. Situação por matéria

| Matéria (professor) | O que foi implementado e medido | O que falta |
|---|---|---|
| Inteligência Artificial (Alexandre Barbosa) | Score de risco formalizado como sistema baseado em conhecimento; C1, C3 e C6 fechados; C2 (sobreposição: phi 0,86 entre qualidade e CCS) e C4 (sensibilidade dos pesos: ranking robusto, Spearman ≥ 0,95, mas Alto + Crítico de 30 % a 53 %) medidos | Texto: comparação regras × aprendido e seção de ética/LGPD |
| Redes Neurais Artificiais (Cristiano) | SP1 com 5 sementes e 30 configurações por modelo: XGBoost 23,28 ± 0,03, MLP 25,99 ± 0,65, baseline 31,54. Resultado negativo para a rede neural. Ablação do A1: 24,41 | LSTM/GRU (ou declarar fora por prazo); texto de §5 |
| Processamento de Linguagem Natural (Raphael) | SP2: regras × TF-IDF + LR em 1.500 frases sintéticas. Fora da distribuição, regras F1 0,96 contra 0,63; volume lido errado 0 %; recusa no limiar 0,7 leva o lançamento correto de 66 % a 97 %. Contra o oráculo do DomainSim: volume errado 0 % | Corpus real (limitação declarada); texto de §6 |
| IA Generativa (Raphael) | SP3: harness dos 4 braços; corpus oficial da IN 76 e IN 77 (105 trechos, com hash); B0 (0,10) e B1 (0,83; 0,23 sem os números) medidos | Rodar B2/B3 (LLM sem e com RAG); avaliação humana com Kappa; texto de §7 |
| Projeto de Extensão (Willgnner) | Kit de campo pronto: termo LGPD, lista de presença, roteiro de escuta, folheto com QR para via-leite-sense.vercel.app, avaliação e consolidação | Realizar a oficina via SENAR; se não ocorrer até 12/12, vira limitação declarada |

## 4. Próximos passos até a banca

- Escrever as seções que não dependem de resultado: §1 Introdução, §2 Trabalhos relacionados, §3 O sistema, §4 Método e §9 Ameaças à validade.
- Redigir §5 (SP1) e §6 (SP2) com os números acima.
- Rodar B2/B3 e a avaliação humana de SP3 até 30/11; depois §7, §8 e §10 (01 a 07/12).
- Revisão integral de 08 a 10/12: consistência numérica, linguagem de pitch e referências.

## 5. Limitações declaradas

- A base é majoritariamente sintética (30 produtores em dados_teste/); nenhum número acima é resultado em dado real.
- Não houve acesso a dados de laticínio.
- A calibração pela RBQL usa distribuição agregada (estado × ano), não por produtor.
- Sem corpus real de mensagens de produtores para o PLN.
