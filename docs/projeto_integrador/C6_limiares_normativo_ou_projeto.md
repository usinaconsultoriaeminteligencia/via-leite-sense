# C6: cada limiar do código, normativo ou escolha de projeto

> **Matérias:** Inteligência Artificial (base de conhecimento, `ia.md` §4 C6) e IA Generativa
> (primeira entrega do corpus normativo, `ia_generativa.md` §5.1).
> **Fonte conferida:** texto oficial da IN 76/2018 e da IN 77/2018 (DOU de 30/11/2018), em
> `experimentos/iagen/corpus/`, com URL e hash do PDF no cabeçalho. **Alterações posteriores (IN 58 e
> 59/2019) não foram incorporadas:** conferir antes de citar como vigente.
> **Data:** 06/11/2026.

## Tabela

Limiares de `via_leite/core/score_risco.py` (`LIMIAR`) e de `perfil/classificador_perfil.py`.

| Limiar no código | Valor | Classificação | Dispositivo ou origem |
|---|---|---|---|
| `ccs_alto` | 500 mil cél/mL | **[normativo]**, com ressalva de agregação | IN 76, art. 7º: **média geométrica trimestral** de CCS ≤ 500.000 CS/mL |
| `cbt_alto` | 300 mil UFC/mL | **[normativo]**, com ressalva de agregação | IN 76, art. 7º: **média geométrica trimestral** de CPP ≤ 300.000 UFC/mL |
| `ccs_atencao` | 400 mil cél/mL | **[escolha de projeto]** | 80% do limite legal; ancorado na mediana de Goiás na RBQL (392), não na norma |
| `cbt_atencao` | 100 mil UFC/mL | **[escolha de projeto]** | Topo da faixa real de Goiás na RBQL (40 a 131), não na norma |
| `temp_tanque_max` | 4,0 °C | **[normativo]** | IN 77, art. 18, § 1º: leite refrigerado a no máximo 4,0 °C **em até três horas**; IN 76, art. 3º, II |
| `temp_tanque_critico` | 6,0 °C | **[escolha de projeto]** | Sem dispositivo. A norma fixa 7,0 °C (excepcionalmente 9,0 °C) só para o **recebimento no estabelecimento** (IN 76, art. 3º, I) |
| `gordura_min` | 3,0 g/100 g | **[normativo]** | IN 76, art. 5º, I |
| `proteina_min` | 2,9 g/100 g | **[normativo]** | IN 76, art. 5º, II |
| `thi_conforto` / `thi_atencao` / `thi_alto` | 68 / 72 / 78 | **[escolha de projeto]** (literatura zootécnica) | As INs 76 e 77 não tratam de estresse térmico. Citar a literatura de THI, não a norma |
| `queda_producao_pct` / `_critica` | 10% / 20% | **[escolha de projeto]** | Sem base normativa |
| `perda_logistica_pct` | 5% | **[escolha de projeto]** | Sem base normativa |
| `preco_litro_base`, `bonus_qualidade`, `penalidade_qualidade` | R$ 2,80 / 0,15 / 0,10 | **[escolha de projeto]**, constante de mercado (achado C5) | A norma não fixa preço, bônus nem penalidade |
| `IN77_CCS_LIMITE` / `IN77_CBT_LIMITE` (`classificador_perfil.py`) | 500 / 300 | **[normativo], mas rótulo errado** | O limite está na **IN 76**, art. 7º, não na IN 77. A IN 77 trata da coleta, do transporte e da interrupção da coleta (art. 45) |
| `CCS_SEVERO` / `CBT_SEVERO` | 600 / 450 | **[escolha de projeto]** | 1,2× e 1,5× o limite legal |

## Dois achados que a conferência revelou

1. **Agregação diferente da norma.** A IN 76 avalia CCS e CPP por **média geométrica trimestral**
   de amostras ao menos mensais (art. 7º, §§ 1º e 2º). O código aplica 500 e 300 a **cada leitura
   diária**. O valor é normativo; a forma de aplicar não é. Uma leitura isolada acima de 500 não
   coloca o produtor fora do padrão legal. Para o artigo: declarar que o score usa o limite legal
   como **alerta antecipado por leitura**, e não como verificação de conformidade.
2. **Rótulo de norma trocado.** As constantes `IN77_*` de `classificador_perfil.py` descrevem
   limites que estão na IN 76. Corrigir o nome é uma mudança de produto: fica registrada aqui e
   **não foi feita** nesta etapa.

## Consequência para o artigo

- §4 Método: a camada de regras passa a ter **proveniência por limiar**. Dos 14 grupos de limiar,
  6 são normativos (dois com ressalva de agregação) e 8 são escolha de projeto.
- §9 Ameaças, linha C6: muda de "rótulo normativo em escolha da equipe" para a tabela acima e os
  dois achados.
- C-1 (estratificação da confiança): só a parte normativa da camada de regras tem substrato real.
  As escolhas de projeto têm a mesma garantia que qualquer parâmetro calibrado à mão.
