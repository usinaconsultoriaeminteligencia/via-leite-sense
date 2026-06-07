#!/usr/bin/env bash
set -euo pipefail

python ingestao_clima_inmet.py --raw-dir dados_inmet_raw --out-dir dados_inmet_processado
python gerador_leite_sintetico.py --use-real-climate --real-climate-path dados_inmet_processado/fact_clima_diario_inmet.csv --output-dir dados_teste
python treino_mvp_avancado.py
