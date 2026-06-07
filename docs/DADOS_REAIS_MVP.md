# VIA LEITE SENSE - pacote minimo de dados reais

## Objetivo

Este documento define o pacote minimo de dados para colocar o VIA LEITE SENSE em piloto com um laticinio real sem depender de integracao complexa no primeiro momento.

A prioridade comercial nao e pedir "tudo". A prioridade e reduzir friccao de onboarding e provar valor rapido.

## Tese de entrada real

O VIA LEITE SENSE nao precisa nascer com ERP totalmente integrado para gerar valor.

A entrada real pode comecar com 3 blocos:

1. cadastro de produtores;
2. coleta diaria por produtor;
3. cadastro de rotas.

O clima pode ser enriquecido internamente pela propria plataforma via INMET e polo climatico.

## Pacote minimo para piloto

### Obrigatorio

1. `dim_produtor.csv`
2. `fact_producao_produtor_dia.csv`
3. `dim_rota.csv`

### Recomendado

1. `fact_rota_dia.csv`

### Enriquecido pela propria plataforma

1. clima diario por polo;
2. indicadores agregados de efetividade dos planos;
3. classificacoes e scores operacionais;
4. plano de acao e historico de execucao.

## Regras do MVP comercial

### Regra 1

Se o cliente nao tiver laboratorio estruturado, o piloto ainda pode rodar.

Campos de qualidade como `ccs`, `cbt`, `temp_tanque_c` e flags podem entrar vazios ou com zero no primeiro ciclo, desde que isso seja explicitado.

### Regra 2

Se o cliente nao tiver custo logistico detalhado por produtor, o piloto ainda pode rodar.

Nesse caso, o produto opera com:

- rota;
- distancia aproximada;
- dificuldade logistica;
- percentual de estrada nao pavimentada.

### Regra 3

Se o cliente nao tiver dados historicos muito longos, o piloto ainda pode rodar.

A meta inicial recomendada e:

- minimo aceitavel: 90 dias;
- ideal para piloto robusto: 180 dias;
- ideal para modelagem mais confiavel: 12 meses.

## Arquivos e campos

## 1. dim_produtor.csv

Finalidade: cadastrar a base de fornecedores.

### Campos obrigatorios

- `id_produtor`
- `nome_ficticio`
- `municipio`
- `polo_climatico`
- `id_laticinio_principal`
- `id_rota_principal`
- `tipo_sistema`
- `distancia_km_laticinio`
- `data_inicio_fornecimento`
- `ativo`

### Campos recomendados

- `nivel_tecnificacao`
- `porte_produtor`
- `vacas_lactacao`
- `producao_media_esperada_litros_dia`
- `capacidade_maxima_litros_dia`

### Campos opcionais

- `raca_predominante`
- `sensibilidade_seca`
- `sensibilidade_calor`
- `sensibilidade_qualidade`
- `prob_churn_base`

## 2. fact_producao_produtor_dia.csv

Finalidade: base principal da operacao diaria por fornecedor.

### Campos obrigatorios

- `data`
- `id_produtor`
- `id_laticinio`
- `id_rota`
- `polo_climatico`
- `litros_coletados`

### Campos fortemente recomendados

- `litros_previstos`
- `litros_produzidos`
- `litros_descartados`
- `ccs`
- `cbt`
- `temp_tanque_c`
- `flag_antibiotico`
- `flag_qualidade_reprovada`
- `flag_falha_coleta`
- `custo_logistico_rateado`

### Campos opcionais

- `flag_mudou_laticinio`
- `score_sanidade`
- `score_manejo`
- `margem_estimada_fornecedor`

## 3. dim_rota.csv

Finalidade: caracterizar o contexto logistico estrutural.

### Campos obrigatorios

- `id_rota`
- `id_laticinio`
- `polo_climatico`
- `km_planejado`
- `capacidade_tanque_litros`
- `dificuldade_logistica`
- `percentual_estrada_nao_pavimentada`

### Campos recomendados

- `tempo_medio_horas`

## 4. fact_rota_dia.csv

Finalidade: medir execucao real de rota e perdas agregadas.

### Campos obrigatorios para fase 2

- `data`
- `id_rota`
- `id_laticinio`
- `litros_previstos`
- `litros_realizados`
- `km_rodados`
- `tempo_total_horas`

### Campos recomendados

- `num_produtores_planejados`
- `num_produtores_atendidos`
- `custo_total`
- `ocupacao_tanque_pct`
- `indice_atraso`
- `indice_perda_rota`

## O que nao deve travar o piloto

Nao deve travar:

- ausencia de API;
- envio manual em CSV;
- alguns campos de qualidade vazios;
- custo logistico incompleto;
- falta de fact_rota_dia na primeira entrega.

## O que deve travar o piloto

Deve travar:

- IDs inconsistentes entre produtor e coleta;
- data sem padrao;
- duplicidade grave de produtor;
- rota sem relacionamento com produtor;
- volume diario sem identificacao do produtor;
- municipios e polos sem criterio minimo de padronizacao.

## Formato e padrao de entrega

- formato preferencial: CSV UTF-8;
- separador: virgula;
- decimal: ponto;
- datas: `YYYY-MM-DD`;
- uma linha por entidade no cadastro;
- uma linha por produtor por dia na fato de producao;
- uma linha por rota por dia na fato de rota.

## Proposta comercial de onboarding

### Fase 1 - descoberta e padronizacao

- receber amostra real dos arquivos;
- validar colunas;
- mapear lacunas;
- devolver parecer de aderencia.

### Fase 2 - piloto operacional

- carregar historico;
- enriquecer clima;
- gerar carteira inicial;
- abrir primeiros planos de acao;
- medir efetividade.

### Fase 3 - integracao e escala

- automatizar exportacao;
- elevar frequencia de carga;
- incluir laboratorio, ERP e financeiro;
- evoluir para operacao continua.

## Mensagem comercial recomendada

O argumento comercial deve ser simples:

"Para comecar, o cliente nao precisa fazer uma transformacao de sistemas. Basta entregar um pacote minimo de cadastro, coleta diaria e rotas. O restante pode ser enriquecido e amadurecido no piloto."

## Ferramentas do projeto para onboarding

### 1. Validar o pacote recebido

```powershell
python validar_pacote_dados_reais.py --data-dir CAMINHO_DO_PACOTE
```

### 2. Importar e normalizar para o formato do Via Leite

```powershell
python importar_pacote_dados_reais.py --input-dir CAMINHO_DO_PACOTE --output-dir CAMINHO_SAIDA
```

### 2b. Executar o onboarding interno completo

```powershell
python onboarding_cliente.py --cliente "Nome do Cliente" --input-dir CAMINHO_DO_PACOTE
```

Esse comando gera:

- pasta de base operacional;
- pasta de artefatos;
- resumo JSON;
- parecer Markdown;
- scripts `.ps1` para subir o ambiente.

### 3. Usar a saida no fluxo do produto

Depois da importacao, a pasta de saida fica pronta para ser usada como base operacional do produto, incluindo:

- `dim_produtor.csv`
- `fact_producao_produtor_dia.csv`
- `dim_rota.csv`
- `fact_rota_dia.csv`
- `dim_laticinio.csv`
- `dim_tempo.csv`
- `fact_clima_diario.csv`
- `manifesto_importacao.json`
