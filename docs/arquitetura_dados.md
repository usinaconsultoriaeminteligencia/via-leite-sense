# Arquitetura de Dados — VIA LEITE SENSE

**Versão:** 2.0 — Sprint 4 | **Data:** Junho 2026

---

## Visão geral das fontes de dados

O MVP opera com três camadas de dados, combinando fontes sintéticas
(para validação de arquitetura), fontes externas abertas (INMET) e
entrada estruturada de dados operacionais reais.

```
┌─────────────────────────────────────────────────────────┐
│                   VIA LEITE SENSE                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Operac.  │  │  Clima   │  │Qualidade │  │  IoT   │ │
│  │ (CSV/    │  │  INMET   │  │ (Manual/ │  │ (Edge  │ │
│  │  Manual) │  │  (API/   │  │  CSV)    │  │  Fase4)│ │
│  │          │  │  CSV)    │  │          │  │        │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘ │
│       └─────────────┴──────────────┴────────────┘      │
│                           │                             │
│              ┌────────────▼──────────────┐             │
│              │   Engenharia de Atributos  │             │
│              │   + Motor de Scoring       │             │
│              │   (score_risco.py)         │             │
│              └────────────┬──────────────┘             │
│                           │                             │
│              ┌────────────▼──────────────┐             │
│              │   Dashboard Streamlit      │             │
│              │   (Radar de Risco,         │             │
│              │    Executivo, Operacional) │             │
│              └───────────────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

---

## Tabela de indicadores

| Indicador | Origem | Frequência | Método de entrada | Arquivo destino |
|---|---|---|---|---|
| **Litros coletados** | Laticínio / produtor | Por coleta (2–3x/semana) | CSV importado ou entrada manual | `fact_producao_produtor_dia.csv` |
| **CCS** (Contagem de Células Somáticas) | Laboratório (RBQL) | Mensal (obrigatório IN 77) | CSV importado | `fact_producao_produtor_dia.csv` |
| **CBT** (Contagem Bacteriana Total) | Laboratório (RBQL) | Mensal (obrigatório IN 77) | CSV importado | `fact_producao_produtor_dia.csv` |
| **Temperatura do tanque** (`temp_tanque_c`) | Tanque de expansão | Contínuo / por coleta | Entrada manual ou sensor IoT (Fase 4) | `fact_producao_produtor_dia.csv` |
| **Volume descartado** (`litros_descartados`) | Laticínio / produtor | Por coleta | CSV importado ou entrada manual | `fact_producao_produtor_dia.csv` |
| **Temperatura ambiente** (`temp_med_c`) | INMET | Diária | API / CSV INMET | `fact_clima_diario.csv` |
| **Precipitação** (`precip_mm`) | INMET | Diária | API / CSV INMET | `fact_clima_diario.csv` |
| **Umidade relativa** (`umidade_med_pct`) | INMET | Diária | API / CSV INMET | `fact_clima_diario.csv` |
| **THI** (Índice de Temperatura e Umidade) | Calculado | Diária | Derivado de temp + umidade INMET | `fact_clima_diario.csv` |
| **Distância da rota** | Operação logística | Estático | Cadastro inicial | `dim_rota.csv` |
| **Custo logístico** (`custo_logistico_rateado`) | Operação logística | Mensal | Entrada manual | `fact_producao_produtor_dia.csv` |

### Fórmula do THI

```
THI = (0.8 × Temp_ar) + ((UR / 100) × (Temp_ar - 14.4)) + 46.4
```

Onde:
- `Temp_ar` = temperatura do ar em °C
- `UR` = umidade relativa em %

Limiares de estresse térmico em bovinos leiteiros:
- THI ≤ 68: zona de conforto
- THI 69–72: estresse leve (início de queda de produção)
- THI 73–78: estresse moderado
- THI > 78: estresse severo (queda significativa de produção e qualidade)

---

## Métodos de entrada por fase

### Fase MVP (atual) — Entrada estruturada

```
Operacional:
  - Gerador sintético: gerador_leite_sintetico.py
  - Dados reais: importar_pacote_dados_reais.py (CSV padronizado)
  - Entrada manual: pages/6_Gestão_e_dados.py (formulário diário)

Climático:
  - Dados reais: ingestao_clima_inmet.py (CSV das estações INMET)
  - Estações do Sul Goiano: A025 (Rio Verde), A016 (Jataí), Mineiros
  - Saída processada: dados_inmet_processado/fact_clima_diario_inmet.csv

Qualidade (CCS/CBT):
  - Entrada manual via formulário Streamlit
  - Importação CSV com colunas padronizadas
  - Validação via validar_pacote_dados_reais.py
```

### Fase 2 — Integração com sistemas de laticínios

```
- Importação via API REST dos sistemas de gestão de laticínios
  (e.g., Sumá, Agriness, sistemas próprios de cooperativas)
- Webhook para recebimento automático de resultados de laboratório
- Integração com plataformas de RBQL (Rede Brasileira de Qualidade do Leite)
```

### Fase 4 — IoT e telemetria em tempo real

```
- Sensores de temperatura no tanque de expansão
- Sensores climáticos locais (temperatura, umidade, THI em tempo real)
- GPS em caminhões de coleta
- Sensores de nível/volume do tanque
- Protocolo: MQTT → via_leite_edge → FastAPI backend
- Variáveis de ambiente: IOT_SIMULATION_MODE, IOT_PROVIDER
- Endpoints: GET /api/iot/simulated-readings, /api/iot/farms/{farm_id}/latest
```

---

## Schema dos arquivos CSV (padrão MVP)

> Os nomes abaixo refletem o schema **real** gerado por `gerador_leite_sintetico.py`.
> O motor `score_risco.py` mantém uma camada de aliases (`ALIASES_COLUNA`) que mapeia
> os nomes reais para os nomes canônicos do scoring — por isso `temp_tanque_c` e
> `litros_descartados` são reconhecidos automaticamente.

### fact_producao_produtor_dia.csv

Tabela-fato central por produtor/dia. Inclui qualidade (CCS/CBT) embutida —
não há `fact_qualidade.csv` separado no MVP.

```
data, id_produtor, id_laticinio, id_rota, polo_climatico,
litros_previstos, litros_produzidos, litros_coletados, litros_descartados,
ccs, cbt, temp_tanque_c,
flag_antibiotico, flag_qualidade_reprovada, flag_falha_coleta, flag_mudou_laticinio,
score_sanidade, score_manejo,
custo_logistico_rateado, margem_estimada_fornecedor,
target_queda_7d, target_queda_15d, target_queda_30d
```

### fact_clima_diario.csv

```
data, polo_climatico,
temp_min_c, temp_max_c, temp_med_c,
umidade_med_pct, precip_mm, vento_med_ms, radiacao_proxy,
precip_3d, precip_7d, precip_15d, dias_sem_chuva,
thi, thi_3d_avg, onda_calor_3d, onda_calor_5d,
dry_spell_10d, anomalia_temp, indice_favorabilidade_pastagem
```

> Integração: a junção clima × produção é feita por `["data", "polo_climatico"]`
> (não apenas por `data`), evitando produto cartesiano entre os polos.

### fact_rota_dia.csv

```
data, id_rota, id_laticinio,
litros_previstos, litros_realizados,
num_produtores_planejados, num_produtores_atendidos,
custo_total, km_rodados, tempo_total_horas,
ocupacao_tanque_pct, indice_atraso, indice_perda_rota
```

### dim_produtor.csv

```
id_produtor, nome_ficticio, municipio, polo_climatico,
id_laticinio_principal, id_rota_principal,
tipo_sistema, nivel_tecnificacao, raca_predominante, porte_produtor,
vacas_lactacao, producao_media_esperada_litros_dia, capacidade_maxima_litros_dia,
distancia_km_laticinio,
sensibilidade_seca, sensibilidade_calor, sensibilidade_qualidade,
prob_churn_base, data_inicio_fornecimento, ativo
```

> Dimensões auxiliares: `dim_rota.csv`, `dim_laticinio.csv`, `dim_tempo.csv`.

---

## Observações de implementação

**Continuidade temporal:** o script `ingestao_clima_inmet.py` garante
série diária contínua, interpolando dados ausentes quando necessário.

**Dados sintéticos:** `gerador_leite_sintetico.py` gera dados operacionais
causalmente correlacionados com o clima — a produção cai em dias de THI alto,
o descarte aumenta quando CBT cresce, simulando a realidade da fazenda.

**Integração futura:** a arquitetura modular permite substituição do gerador
sintético por ingestão real sem alteração nos módulos de scoring e dashboard.
O parâmetro `MVP_DATA_DIR` controla qual base é utilizada em cada ambiente.

---

*VIA LEITE SENSE — Arquitetura de Dados | USINA I.A. © 2026*
