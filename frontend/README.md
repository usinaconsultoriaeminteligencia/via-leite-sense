# VIA LEITE SENSE Frontend

Camada de apresentacao da AgroStartup VIA LEITE SENSE.

Esta interface comunica uma plataforma moderna de monitoramento inteligente da cadeia leiteira para produtos premium, mantendo a base analitica ja existente no projeto.

## Como abrir

Suba a API:

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
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
