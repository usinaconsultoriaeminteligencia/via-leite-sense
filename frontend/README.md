# VIA LEITE SENSE Frontend

Camada de apresentacao da AgroStartup VIA LEITE SENSE.

Esta interface comunica uma plataforma moderna de monitoramento inteligente da cadeia leiteira para produtos premium, mantendo a base analitica ja existente no projeto.

## Como abrir

Suba a API:

```powershell
python -m uvicorn via_leite.api.app:app --host 127.0.0.1 --port 8000
```

Suba o frontend:

```powershell
python -m http.server 8600 -d frontend
```

## Narrativa

O frontend apresenta:

- fazendas monitoradas;
- inteligencia preditiva;
- risco operacional;
- qualidade premium;
- impacto logistico;
- leitura de pitch para banca de inovacao agro.

## EDGE

Os endpoints EDGE podem ser consumidos por esta camada para storytelling IoT-ready:

- `GET /api/iot/simulated-readings`
- `GET /api/iot/farms/{farm_id}/latest`
- `GET /api/iot/alerts`
- `GET /api/iot/executive-summary`

Mensagem obrigatoria da experiencia:

> Dados simulados para demonstracao de conceito e validacao de arquitetura IoT.

## Deploy (Vercel)

Este frontend e HTML/CSS/JS puro, sem build step, entao a Vercel so precisa
servir a pasta `frontend/` como site estatico.

1. **Publicar o backend primeiro.** A Vercel nao roda o FastAPI (usa pandas,
   duckdb, scikit-learn e mantem estado em `dados_utilizador/*.duckdb`, que nao
   e serverless-friendly). Hospede `via_leite/api/app.py` em algo com processo
   persistente — Railway, Render ou Fly.io — via:
   ```
   uvicorn via_leite.api.app:app --host 0.0.0.0 --port $PORT
   ```
   Configure `MVP_DATA_DIR`, `MVP_ARTEFATOS_DIR` e `MVP_USER_DATA_DIR` la.

2. **Liberar o dominio da Vercel no CORS do backend.** Defina a variavel de
   ambiente `MVP_CORS_ORIGINS` no host do backend com a URL publica do
   frontend (aceita lista separada por virgula):
   ```
   MVP_CORS_ORIGINS=https://via-leite-sense.vercel.app
   ```

3. **Apontar o frontend para o backend publicado.** Edite o `content` da tag
   `<meta name="via-leite-api-base" ...>` em `index.html` para a URL publica
   da API antes do deploy (ex.: `https://via-leite-api.up.railway.app`).

4. **Deploy na Vercel:**
   - Import do repositorio no dashboard da Vercel, com **Root Directory**
     apontando para `frontend/`, framework "Other" (sem build command); ou
   - via CLI: `vercel --cwd frontend --prod`.

O `vercel.json` desta pasta ja cobre `cleanUrls` e um header basico de
seguranca — nao ha rotas de servidor para reescrever (a navegacao e via
`#hash` no cliente).
