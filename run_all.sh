#!/usr/bin/env bash
set -euo pipefail

python gerador_leite_sintetico.py
python treino_mvp_avancado.py
