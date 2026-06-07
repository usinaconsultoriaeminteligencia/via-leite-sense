from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

from importar_pacote_dados_reais import import_package


def run_command(command: list[str], env: dict[str, str]) -> None:
    result = subprocess.run(command, env=env, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Falha ao executar comando: {' '.join(command)}")


def training_readiness(base_dir: Path) -> dict[str, object]:
    fact_path = base_dir / "fact_producao_produtor_dia.csv"
    if not fact_path.exists():
        return {"ready": False, "reason": "Base operacional não encontrada para treino."}

    fact = pd.read_csv(fact_path, parse_dates=["data"])
    rows = int(len(fact))
    unique_dates = int(fact["data"].nunique()) if "data" in fact.columns else 0
    unique_suppliers = int(fact["id_produtor"].nunique()) if "id_produtor" in fact.columns else 0

    if rows < 60 or unique_dates < 30 or unique_suppliers < 3:
        return {
            "ready": False,
            "reason": "Pacote importado com massa insuficiente para treino confiável.",
            "rows": rows,
            "unique_dates": unique_dates,
            "unique_suppliers": unique_suppliers,
        }

    return {
        "ready": True,
        "rows": rows,
        "unique_dates": unique_dates,
        "unique_suppliers": unique_suppliers,
    }


def run_real_pilot(
    input_dir: Path,
    base_dir: Path,
    artefatos_dir: Path,
    climate_path: Path | None = None,
    skip_train: bool = False,
) -> dict[str, object]:
    manifest = import_package(input_dir, base_dir, climate_path)
    readiness = training_readiness(base_dir)

    env = os.environ.copy()
    env["MVP_DATA_DIR"] = str(base_dir.resolve())
    env["MVP_ARTEFATOS_DIR"] = str(artefatos_dir.resolve())

    training_status = {"executed": False, "skipped": False, "reason": None}
    if skip_train:
        training_status = {"executed": False, "skipped": True, "reason": "Treino ignorado por parâmetro --skip-train."}
    elif not readiness["ready"]:
        training_status = {"executed": False, "skipped": True, "reason": str(readiness["reason"])}
    else:
        run_command(
            [
                sys.executable,
                "treino_mvp_avancado.py",
                "--data-dir",
                str(base_dir),
                "--artefatos-dir",
                str(artefatos_dir),
            ],
            env,
        )
        training_status = {"executed": True, "skipped": False, "reason": None}

    return {
        "importacao": manifest,
        "prontidao_treino": readiness,
        "treino": training_status,
        "ambiente": {
            "MVP_DATA_DIR": env["MVP_DATA_DIR"],
            "MVP_ARTEFATOS_DIR": env["MVP_ARTEFATOS_DIR"],
        },
        "proximos_comandos": {
            "api": f"$env:MVP_DATA_DIR='{env['MVP_DATA_DIR']}'; $env:MVP_ARTEFATOS_DIR='{env['MVP_ARTEFATOS_DIR']}'; python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000",
            "frontend": "python -m http.server 8600 -d frontend",
            "dashboard": f"$env:MVP_DATA_DIR='{env['MVP_DATA_DIR']}'; $env:MVP_ARTEFATOS_DIR='{env['MVP_ARTEFATOS_DIR']}'; streamlit run dashboard_mvp_avancado.py",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a esteira de piloto real do Via Leite.")
    parser.add_argument("--input-dir", type=Path, required=True, help="Pacote de dados reais do cliente.")
    parser.add_argument("--base-dir", type=Path, required=True, help="Diretorio de saida para a base operacional importada.")
    parser.add_argument("--artefatos-dir", type=Path, required=True, help="Diretorio de saida para os artefatos do modelo.")
    parser.add_argument("--climate-path", type=Path, default=None, help="Arquivo de clima opcional.")
    parser.add_argument("--skip-train", action="store_true", help="Importa a base mas nao roda treino.")
    args = parser.parse_args()

    summary = run_real_pilot(
        input_dir=args.input_dir,
        base_dir=args.base_dir,
        artefatos_dir=args.artefatos_dir,
        climate_path=args.climate_path,
        skip_train=args.skip_train,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
