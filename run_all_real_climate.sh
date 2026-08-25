#!/usr/bin/env bash
set -euo pipefail

python -m via_leite.ingest.ingestao_clima_inmet --raw-dir dados_inmet_raw --out-dir dados_inmet_processado
python -m via_leite.models.gerador_leite_sintetico --use-real-climate --real-climate-path dados_inmet_processado/fact_clima_diario_inmet.csv --output-dir dados_teste
python -m via_leite.models.treino_mvp_avancado
