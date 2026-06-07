# Roadmap de Gestao de Fornecedores

Esta evolucao reposiciona o MVP de captacao preditiva para uma plataforma de inteligencia de fornecedores para laticinios.

## Camada adicionada

- `fornecedor_inteligencia.py`: consolida volume, qualidade, logistica e continuidade em um score relativo de risco por produtor.
- `pages/6_Fornecedores_360.py`: detalha cada produtor com score, recomendacao, historico de volume, qualidade e descarte.
- `pages/3_Produtores.py`: passa a priorizar fornecedores por score composto, nao apenas por descarte e eventos de qualidade.

## Dimensoes do score

- Volume: risco de queda e tendencia recente de captacao.
- Qualidade: CCS, CBT, reprovacao e antibiotico.
- Logistica: falha de coleta, custo e distancia.
- Continuidade: churn observado e margem estimada.

## Proximos passos de produto

- Criar workflow de plano de acao por produtor, com responsavel, prazo, status e evidencias.
- Treinar modelos dedicados para risco de queda, qualidade e churn usando os alvos sinteticos ja existentes.
- Incluir importacao operacional por produtor, rota e unidade, alem do lancamento consolidado por laticinio.
- Separar features disponiveis antes da coleta das features disponiveis depois do laboratorio para evitar vazamento operacional.
