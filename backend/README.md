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
