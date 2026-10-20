# Proveniência — referência pública de qualidade do leite (RBQL)

| Campo | Valor |
|---|---|
| Arquivo bruto | `quality_data.csv` (sem alteração) |
| Origem | Zenodo, registro 17714633 — DOI [10.5281/zenodo.17714633](https://doi.org/10.5281/zenodo.17714633), versão 0.1, publicado em 25/11/2025 |
| Autoria | Max Felipe Santos Cravo |
| Licença | CC-BY 4.0 — redistribuição permitida com atribuição |
| Artigo associado | Cravo, M. F. S. S.; Cruz, P. V.; Zavaleta, J.; Serra da Cruz, S. M. *Construindo e Explorando Datasets Curados Sobre a Produção Leiteira do Brasil*. 17º WCAMA, CSBC 2026, Gramado/RS |
| Fonte primária declarada | Observatório da Qualidade do Leite (MAPA/RBQL), coleta manual |
| Baixado em | 20/10/2026, via API do Zenodo |
| SHA-256 | `b683d62de83ee14575ac7abdc21fb9157a86dc5ebdb7909f6f6bcef20f2a4d17` |
| Processado por | `python -m via_leite.ingest.referencia_qualidade_rbql` |
| Saídas | `referencia_qualidade_rbql.csv` (formato longo), `resumo_referencia_rbql.json` |

## Conteúdo

12 localidades × 11 anos (2013–2023). Para cada ano há um par mínimo/máximo de
CCS (mil cél/mL), CPP (mil UFC/mL), EST (%) e ESD (%). A fonte grafa "CSS"; o
correto é CCS. CPP é o nome que a IN 76 dá à contagem bacteriana (CBT no projeto).

## Premissas (não confirmadas pela fonte)

1. **O que é o par mín/máx.** Nem o artigo nem os notebooks do Zenodo dizem
   como o par foi obtido. A leitura mais provável é a faixa anual dos valores
   mensais publicados no Observatório. Em qualquer leitura, **é dado agregado
   por localidade, não distribuição por produtor**.
2. **"Goiânia (Centro-oeste)" = Goiás.** O rótulo nomeia a cidade-sede do
   laboratório da RBQL; o projeto o usa como proxy de GO.
3. **Nordeste e Norte** vêm agregados por região na fonte, sem UF.

## Erros encontrados na fonte (mantidos no bruto, marcados no processado)

| Linha | Problema | Tratamento |
|---|---|---|
| Rio Grande do Sul, 2023, ESD | máx. 12,59 % (valor típico de EST) com mín. 8,88 % | `valido = False`; fora dos resumos. CCS e CPP da mesma linha estão íntegros |

## Para que serve no Via Leite Sense

Fixar a **unidade** e a **ordem de grandeza** de CCS e CBT na calibração do
achado C1, no lugar dos dados da Piracanjuba, que não virão (sem acordo,
07/10/2026). Não serve para treinar modelo: a granularidade é ano × estado.
