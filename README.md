# VIA LEITE SENSE

Monitoramento Inteligente da Producao Leiteira para Produtos Premium

Plataforma de apoio a decisao para a cadeia leiteira premium: base operacional, IA preditiva, clima, dashboards inteligentes e arquitetura IoT-ready para fazendas monitoradas por sensores virtuais.

O VIA LEITE SENSE transforma dados da fazenda em inteligencia operacional para elevar a qualidade do leite destinado a producao de derivados premium.

O pacote inclui:
- geracao de base sintetica operacional de captacao;
- substituicao do clima sintetico por clima real processado do INMET;
- treino e exportacao de artefatos do modelo preditivo;
- dashboards executivos, operacionais e de pitch;
- camada VIA LEITE EDGE para monitoramento IoT-ready em modo simulado.

## VIA LEITE EDGE

O VIA LEITE EDGE e uma camada experimental IoT-ready da plataforma VIA LEITE.

Nesta fase, utiliza dados sinteticos para validar arquitetura, dashboards, regras de alerta e modelos preditivos.

A solucao esta preparada para integracao futura com sensores reais de tanque, sensores climaticos locais, GPS de caminhoes e sensores de qualidade do leite.

Variaveis de ambiente principais:

```powershell
$env:IOT_SIMULATION_MODE='true'
$env:IOT_PROVIDER='simulated'
```

Endpoints principais:

- `GET /api/iot/simulated-readings`
- `GET /api/iot/farms/{farm_id}/latest`
- `GET /api/iot/alerts`

No Streamlit, a pagina `VIA LEITE EDGE` exibe:

- temperatura do tanque;
- volume do leite;
- THI;
- risco termico;
- risco de qualidade;
- prioridade de coleta;
- ranking de fazendas;
- alertas preventivos ativos.

## Estrutura

- `dados_teste/`  
  pasta padrão com os CSVs dimensionais e de fatos consumidos por `treino_mvp_avancado.py` e `dashboard_mvp_avancado.py` (preenchida ao rodar o gerador sem outro `--output-dir`).
- `ingestao_clima_inmet.py`  
  processa arquivos CSV do INMET e gera `dados_inmet_processado/fact_clima_diario_inmet.csv`.
- `gerador_leite_sintetico.py`  
  gera a base sintética operacional; pode usar clima sintético ou clima real já processado.
- `treino_mvp_avancado.py`  
  faz engenharia de atributos, split temporal, treino do modelo e exportação de artefatos.
- `dashboard_mvp_avancado.py`  
  entrada do dashboard (visão geral); secções em `pages/` (Executivo, Operacional, Produtores, Clima), com filtros partilhados na barra lateral.
- `dashboard_common.py`  
  carregamento em cache dos CSVs/JSON e filtros reutilizáveis pelas páginas.
- `.streamlit/config.toml`  
  tema visual (cores e fundo).
- `gestor_store.py`  
  persistência dos lançamentos introduzidos pelos gestores (CSV em `dados_utilizador/`, configurável com `MVP_USER_DATA_DIR`).
- `pages/5_Gestão_e_dados.py`  
  formulário diário por laticínio, importação em lote e comparativo com a base `fact_producao`.
- `run_all.sh`  
  esteira original com clima sintético.
- `run_all_real_climate.sh`  
  esteira completa com clima real processado do INMET.

## Dependências

```bash
pip install -r requirements.txt
```

## Fluxo 1 — execução rápida com clima sintético

```bash
python gerador_leite_sintetico.py --output-dir dados_teste
python treino_mvp_avancado.py
streamlit run dashboard_mvp_avancado.py
```

## Fluxo 2 — execução com clima real do INMET

### 1. Baixe os CSVs do INMET
Coloque em `dados_inmet_raw/` os arquivos CSV das estações do Sul de Goiás.

Sugestão de nomenclatura dos arquivos:
- `A025_RIO_VERDE.csv`
- `A016_JATAI.csv`
- `MINEIROS.csv`
- `SUDESTE_SUL_GOIANO.csv`

> Observação: o script identifica o polo por nome de arquivo. Para Rio Verde e Jataí, reconhecer `A025`, `RIO_VERDE`, `A016` ou `JATAI` já é suficiente.

### 2. Processar os dados climáticos

```bash
python ingestao_clima_inmet.py --raw-dir dados_inmet_raw --out-dir dados_inmet_processado
```

Saídas esperadas:
- `dados_inmet_processado/fact_clima_diario_inmet.csv`
- `dados_inmet_processado/manifesto_inmet.json`

### 3. Gerar a base operacional com clima real

```bash
python gerador_leite_sintetico.py \
  --use-real-climate \
  --real-climate-path dados_inmet_processado/fact_clima_diario_inmet.csv \
  --output-dir dados_teste
```

### 4. Treinar o modelo

```bash
python treino_mvp_avancado.py
```

### 5. Subir o dashboard

```bash
streamlit run dashboard_mvp_avancado.py
```

## Execução one-shot com clima real

```bash
bash run_all_real_climate.sh
```

## Fluxo 3 - piloto com dados reais importados

### 1. Validar o pacote do cliente

```bash
python validar_pacote_dados_reais.py --data-dir CAMINHO_DO_PACOTE
```

### 2. Importar, normalizar e treinar

```bash
python executar_piloto_real.py \
  --input-dir CAMINHO_DO_PACOTE \
  --base-dir dados_piloto_cliente \
  --artefatos-dir artefatos_piloto_cliente
```

### 2b. Fluxo interno de onboarding por cliente

```bash
python onboarding_cliente.py \
  --cliente "Nome do Cliente" \
  --input-dir CAMINHO_DO_PACOTE
```

Esse fluxo organiza uma pasta por cliente com:

- base operacional importada;
- artefatos do modelo;
- parecer em Markdown;
- resumo JSON;
- scripts prontos para subir API, frontend e dashboard.

### 3. Subir API e dashboard sobre a base importada

API:

```powershell
$env:MVP_DATA_DIR='C:\CAMINHO\PARA\dados_piloto_cliente'
$env:MVP_ARTEFATOS_DIR='C:\CAMINHO\PARA\artefatos_piloto_cliente'
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Dashboard:

```powershell
$env:MVP_DATA_DIR='C:\CAMINHO\PARA\dados_piloto_cliente'
$env:MVP_ARTEFATOS_DIR='C:\CAMINHO\PARA\artefatos_piloto_cliente'
streamlit run dashboard_mvp_avancado.py
```

## Saídas do treino

Pasta `artefatos_teste/` (padrão; sobrescreva com `python treino_mvp_avancado.py --artefatos-dir ...`):
- `metricas_modelo.json`
- `modelo_mvp.joblib`
- `predicoes_teste.csv`
- `resumo_teste_por_laticinio.csv`
- `resumo_teste_por_polo.csv`
- `feature_importances.csv`
- `amostra_base_modelagem.csv`

## Indicadores do dashboard

### Executivo
- RMSE, MAE, R² e sMAPE do teste;
- realizado x previsto ao longo do tempo;
- erro médio por laticínio;
- top variáveis do modelo.

### Operacional
- rotas com maior perda;
- ocupação de tanque x perda operacional;
- custo logístico por litro;
- produtores críticos de qualidade;
- clima por polo, com foco em precipitação e THI.

## Observações de implementação

1. O clima real é processado para série diária contínua, com:
   - precipitação diária;
   - temperatura mínima, média e máxima;
   - umidade relativa média;
   - vento e radiação, quando presentes;
   - THI e acumulados de chuva.

2. A operação leiteira permanece sintética, mas causalmente ligada ao clima.

3. A arquitetura suporta extensões como dados operacionais reais do laticínio, ingestão automática de clima e publicação do dashboard em ambiente corporativo.

## Controle de Acesso e Perfis de Usuário

A plataforma possui autenticação própria com bcrypt e três perfis de acesso.

### Perfis

| Perfil | Credencial padrão | Destinado a |
|--------|-------------------|-------------|
| `admin` | `admin` / `usina2025` | Administrador da plataforma (USINA I.A.) |
| `laticinio` | `laticinio` / `leite2025` | Cliente operador — cooperativa ou laticínio contratante |
| `demo` | `demo` / `demo2025` | Avaliador externo, investidor ou cliente em fase de avaliação |

> Em produção, substituir as credenciais padrão via `st.secrets` (Streamlit Cloud) ou `config_auth.yaml` (local).

### Matriz de permissões por página

| Página | demo 👁️ | laticinio 🏭 | admin 🔑 |
|--------|:-------:|:-----------:|:-------:|
| Início (login) | ✅ | ✅ | ✅ |
| Executivo | ✅ | ✅ | ✅ |
| Operacional | ✅ | ✅ | ✅ |
| Produtores | ✅ | ✅ | ✅ |
| Clima | ✅ | ✅ | ✅ |
| Gestão e dados | ❌ | ✅ | ✅ |
| Fornecedores 360 | ✅ | ✅ | ✅ |
| Via Leite Edge | ✅ | ✅ | ✅ |
| Painel Executivo | ✅ | ✅ | ✅ |
| Onboarding | ✅ | ✅ | ✅ |
| Plano de Ação | ❌ | ✅ | ✅ |
| Demonstração | ✅ | ✅ | ✅ |

**Páginas bloqueadas para `demo`:** Gestão e dados e Plano de Ação — ambas permitem escrita no banco de dados.

### Guards implementados em `auth.py`

| Função | Comportamento |
|--------|--------------|
| `requer_autenticacao()` | Bloqueia se não estiver logado |
| `requer_papel(["admin", "laticinio"])` | Bloqueia se não estiver logado ou se o perfil não estiver na lista |
| `esta_autenticado()` | Retorna `True`/`False` sem bloquear (uso condicional) |

### Configurar credenciais em produção

**Streamlit Cloud** — adicionar em `st.secrets`:
```toml
[auth.credentials.usernames.admin]
name = "Nome Admin"
email = "admin@empresa.com.br"
role = "admin"
password = "$2b$12$..."  # hash bcrypt

[auth.credentials.usernames.operador]
name = "Nome Operador"
email = "operador@empresa.com.br"
role = "laticinio"
password = "$2b$12$..."
```

**Local** — criar `config_auth.yaml` na raiz do projeto com a mesma estrutura.

Para gerar hashes bcrypt:
```python
import bcrypt
print(bcrypt.hashpw(b"senha_aqui", bcrypt.gensalt(rounds=12)).decode())
```

## Roadmap sugerido

- parametrizar polos e códigos de estações via arquivo YAML/JSON;
- incorporar calendário oficial de feriados;
- pipeline de classificação de risco de queda e churn;
- publicar o dashboard com autenticação.
