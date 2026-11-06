# Experimentos do Projeto Integrador (5º período de IA)

Código de aplicação de cada matéria, **fora do caminho de produção** (critério de admissão,
`docs/PROJETO_INTEGRADOR.md` §4). Nada aqui é importado pela API nem pelo frontend. Cada
script grava o resultado em `resultados/` (JSON + Markdown) para o artigo citar.

Rodar sempre da raiz do repositório, com o ambiente do projeto:

```powershell
cd "C:\Users\Novou\Desktop\USINA\Via Leite"
.\.venv\Scripts\python -m experimentos.<pasta>.<script>
```

| Matéria (professor) | Pasta | Script | Pergunta | Precisa de algo externo? |
|---|---|---|---|---|
| **Inteligência Artificial** (Alexandre Barbosa) | `ia/` | `c2_c4_sensibilidade` | O motor de regras tem dimensões sobrepostas (C2)? Quanto o resultado depende dos pesos sem proveniência (C4)? | Não |
| **Redes Neurais Artificiais** (Cristiano) | `rna/` | `sp1_mlp_vs_xgb --orcamento 30` | SP1: a rede neural (MLP) supera o XGBoost e o baseline, pelo protocolo pré-registrado? Inclui a ablação do A1 | Não (cerca de 40 min) |
| **Processamento de Linguagem Natural** (Raphael) | `pln/` | `corpus_sintetico`, depois `sp2_pipeline` | SP2: com que fidelidade a mensagem do produtor vira lançamento? Regras (E0) × TF-IDF + LR (E1), com recusa | **Corpus real** para o número que vale (`--teste-real`) |
| **IA Generativa** (Raphael) | `iagen/` | `sp3_planos` | SP3: o plano ancorado em norma (RAG) é mais fiel e menos alucinado? 4 braços B0–B3 | **Chave de API** (`ANTHROPIC_API_KEY`) para B2/B3 e **texto oficial das INs** em `iagen/corpus/` para B3 |
| **Extensão** (Willgnner) | `docs/projeto_integrador/extensao_kit_de_campo.md` | — | Validade externa: oficina, escuta, coleta de linguagem, beneficiários | Campo (SENAR ou cooperativa) |

## Regras que valem para todos

- **Base sintética.** `dados_teste/` tem 30 produtores e clima sintético. Nenhum número daqui é
  resultado em dado real, e o artigo diz isso.
- **Sem identificador.** Nenhum script usa CPF, nome ou município como entrada (achado A2). O SP3
  manda ao LLM só indicadores e pseudônimo (`P01`..`P30`).
- **Dado real fica fora do git.** Corpus de fala real, planilhas de produtor e formulários de
  extensão vão para `dados_reais/` (no `.gitignore`).
- **Resultado negativo também é resultado.** Se a rede perde para o XGBoost, ou o RAG não reduz
  alucinação, isso entra no artigo com o mesmo peso.

## Versões usadas na última execução

Python 3.12.10 · xgboost 3.4.0 · scikit-learn 1.9.0 · pandas 2.3.3. O `requirements.txt`
declara `xgboost<3.0`: alinhar antes da submissão do artigo.
