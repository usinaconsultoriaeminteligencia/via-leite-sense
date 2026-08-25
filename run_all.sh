#!/usr/bin/env bash
set -euo pipefail

python -m via_leite.models.gerador_leite_sintetico
python -m via_leite.models.treino_mvp_avancado
