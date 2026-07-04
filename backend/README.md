# VIA LEITE SENSE API

API operacional e analitica da plataforma VIA LEITE SENSE.

## Objetivo

Expor a inteligencia da cadeia leiteira para:

- carteira de fazendas;
- planos e eventos gerenciais;
- leituras EDGE IoT-ready;
- resumo executivo para pitch e demonstracao.

## Executar

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

## Endpoints EDGE

- `GET /api/iot/simulated-readings`
- `GET /api/iot/farms/{farm_id}/latest`
- `GET /api/iot/alerts`
- `GET /api/iot/executive-summary`

## Importante

Todos os endpoints EDGE devem sinalizar:

> Dados simulados para demonstracao de conceito e validacao de arquitetura IoT.

## Arquitetura

- provider abstrato IoT;
- provider simulado;
- fallback seguro;
- pronta para integracao futura com MQTT, APIs e sensores reais.

## Deploy (Railway)

Este backend mantem estado em DuckDB (`dados_utilizador/*.duckdb`, multi-tenant
por cliente), entao precisa de um processo persistente com disco — nao roda
como funcao serverless. `railway.json` na raiz do repo ja define o build
(Nixpacks) e o start command.

A cadeia de imports de `backend/app.py` só usa pandas, numpy, duckdb, fastapi
e uvicorn — nada de scikit-learn/xgboost/streamlit/plotly/fpdf2/bcrypt, que só
o app Streamlit e os scripts de treino/scoring precisam. Por isso o Railway
instala a partir de `requirements-api.txt` (via `nixpacks.toml`), não do
`requirements.txt` da raiz — evita puxar ~300MB de `nvidia-nccl-cu12` (dependência
transitiva do xgboost, sem uso em CPU) e o restante das libs pesadas do
Streamlit. Se `backend/app.py` passar a importar algo novo, adicione a
dependência em `requirements-api.txt` também.

1. **Criar o projeto:** importar o repositorio no dashboard da Railway
   (New Project > Deploy from GitHub repo), ou via CLI: `railway login` seguido
   de `railway init` e `railway up` a partir da raiz do repo.

2. **Configurar variaveis de ambiente** no serviço:
   ```
   MVP_DATA_DIR=dados_teste
   MVP_ARTEFATOS_DIR=artefatos_teste
   MVP_USER_DATA_DIR=/data/dados_utilizador
   MVP_CORS_ORIGINS=https://via-leite-sense.vercel.app
   ```
   `MVP_CORS_ORIGINS` aceita lista separada por virgula — inclua a URL da
   Vercel assim que o frontend for publicado.

3. **Adicionar um Volume** (Railway dashboard > serviço > Volumes) montado em
   `/data`, para que `dados_utilizador/via_leite.duckdb` sobreviva a redeploys
   e restarts. Sem o volume, o banco é recriado do zero a cada deploy.

4. **Start command** (já em `railway.json`, não precisa repetir manualmente):
   ```
   uvicorn backend.app:app --host 0.0.0.0 --port $PORT
   ```

5. **Testar o endpoint publicado** (`https://<projeto>.up.railway.app/docs`)
   antes de apontar o frontend para ele.

`.railwayignore` exclui do build ativos pesados que o backend não lê em
runtime (protótipo/pitch, PDFs, CSV de clima INMET, páginas Streamlit,
`frontend/`), para builds mais rápidos.
