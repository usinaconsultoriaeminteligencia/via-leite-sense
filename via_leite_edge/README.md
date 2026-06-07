# VIA LEITE EDGE

O VIA LEITE EDGE e uma camada experimental IoT-ready da plataforma VIA LEITE.

Nesta fase, utiliza dados sinteticos para validar arquitetura, dashboards, regras de alerta e modelos preditivos.

A solucao esta preparada para integracao futura com sensores reais de tanque, sensores climaticos locais, GPS de caminhoes e sensores de qualidade do leite.

## Estrutura

```text
via_leite_edge/
├── __init__.py
├── alerts.py
├── config.py
├── providers.py
├── schemas.py
├── simulator.py
└── README.md
```

## Componentes

- `schemas.py`: contratos de leitura IoT e alerta preventivo.
- `alerts.py`: funcoes puras para THI, temperatura do tanque, volume, risco e prioridade de coleta.
- `simulator.py`: geracao de leituras sinteticas por fazenda a partir da base atual do projeto.
- `providers.py`: abstracao `IoTProvider`, provider simulado e placeholder para provider real.
- `config.py`: configuracao do modo demo por variaveis de ambiente.

## Variaveis de ambiente

```text
IOT_SIMULATION_MODE=true
IOT_PROVIDER=simulated
IOT_SIMULATION_SAMPLE_SIZE=12
```

## Objetivo desta fase

- validar arquitetura backend para ingestao e exposicao de telemetria;
- demonstrar dashboards e alertas preventivos sem depender de hardware;
- testar regras de classificacao e priorizacao de coleta;
- reduzir risco de implementacao na futura camada de IoT real.

## Importante

Todos os dados expostos pelo modulo EDGE nesta fase sao simulados. O dashboard e a API devem sempre sinalizar isso de forma explicita para evitar interpretacao de que ha sensores reais em producao.
