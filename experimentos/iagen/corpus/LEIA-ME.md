# Corpus normativo do SP3 (RAG)

O braço B3 só roda com o **texto oficial** aqui. Não colar resumo, paráfrase nem texto gerado
por IA: o experimento mede justamente a aderência a esta fonte.

## O que colocar (ordem de `ia_generativa.md` §5.1)

1. **IN 77/2018 (MAPA)**: obtenção, armazenamento e transporte do leite cru refrigerado.
2. **IN 76/2018 (MAPA)**: identidade e qualidade do leite cru refrigerado (CCS, CPP/CBT, composição).
3. Material técnico da **Embrapa Gado de Leite** sobre mastite, CCS, CBT, ordenha e resfriamento.
4. Manuais de boas práticas de ordenha.

Fonte oficial das INs: Diário Oficial da União e portal do MAPA (gov.br). Registrar a URL e a
data de acesso no cabeçalho.

## Formato de cada arquivo `.txt` (UTF-8)

```
fonte: IN 77/2018 (MAPA)
versao: DOU de 30/11/2018, seção 1
acesso: 2026-11-07
url: <endereço oficial>
---
Art. 1º ...
Art. 2º ...
```

O script corta por artigo (`Art. N`) quando houver; senão, por parágrafo. Cada trecho
recuperado entra no prompt com documento e dispositivo, para a citação ser verificável (M2, M3).

## Antes de rodar o B3

- Com o texto em mãos, marcar cada limiar do código como `[normativo]` ou `[escolha de projeto]`.
  Isso fecha o **C6** (`ia.md`) e é a primeira entrega da matéria para o produto.
- Conferir o limiar de recusa `LIMIAR_RECUSA` em `sp3_planos.py` com 3 ou 4 consultas manuais.
