# SP2 com oráculo DomainSim (2026-11-06T20:53:53)

20 fazendas × 14 dias × 2 ordenhas = 560 mensagens da família C (vocabulário fora do treino; 25% sem unidade).
Fatos e reconciliação pelo núcleo do DomainSim, sem alteração nele. **Não é linguagem real.**

## Leitura do volume (campo crítico)

| Medida | Valor |
|---|---|
| Volume lido corretamente | 72.1 % |
| Não lido (vai para confirmação humana) | 27.9 % |
| Lido errado (lançado errado, sem aviso) | 0.0 % |

Exemplos não lidos: `coloquei 152 agora no tanque`; `114 da manha ja ta no frio`; `nessa ordenha a ordenha rendeu 131`; `botei 130 no resfriador agora`; `ficou 110 no tanque da manha`

## Reconciliação pelo DomainSim

| Modo | Fazendas recusadas | Aceitas com estoque divergente |
|---|---|---|
| (a) sem confirmação humana: o não lido não é lançado | 20 de 20 | 0 de 20 |
| (b) com confirmação humana das pendências | 0 de 20 | 0 de 20 |

## Controle de sensibilidade (modo b, erros injetados de propósito)

| Taxa injetada | Erros | Fazendas com erro | Recusadas pelo DomainSim | Aceitas com divergência |
|---|---|---|---|---|
| 1% | 3 | 3 | 2 | 1 |
| 3% | 14 | 9 | 7 | 2 |
| 5% | 18 | 12 | 8 | 4 |

Recusa = coleta maior que o estoque lançado (volume lido a menos). Volume lido a mais fecha o balanço com sobra:
o DomainSim aceita, e só a divergência contra os fatos o revela.

