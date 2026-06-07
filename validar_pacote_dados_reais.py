from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED_FILES = {
    "dim_produtor.csv": [
        "id_produtor",
        "nome_ficticio",
        "municipio",
        "polo_climatico",
        "id_laticinio_principal",
        "id_rota_principal",
        "tipo_sistema",
        "distancia_km_laticinio",
        "data_inicio_fornecimento",
        "ativo",
    ],
    "fact_producao_produtor_dia.csv": [
        "data",
        "id_produtor",
        "id_laticinio",
        "id_rota",
        "polo_climatico",
        "litros_coletados",
    ],
    "dim_rota.csv": [
        "id_rota",
        "id_laticinio",
        "polo_climatico",
        "km_planejado",
        "capacidade_tanque_litros",
        "dificuldade_logistica",
        "percentual_estrada_nao_pavimentada",
    ],
}

OPTIONAL_FILES = {
    "fact_rota_dia.csv": [
        "data",
        "id_rota",
        "id_laticinio",
        "litros_previstos",
        "litros_realizados",
        "km_rodados",
        "tempo_total_horas",
    ]
}


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def validate_columns(df: pd.DataFrame, required: list[str]) -> list[str]:
    return [col for col in required if col not in df.columns]


def validate_dates(df: pd.DataFrame, column: str) -> list[str]:
    if column not in df.columns:
        return []
    parsed = pd.to_datetime(df[column], errors="coerce")
    invalid = int(parsed.isna().sum())
    return [f"coluna `{column}` com {invalid} data(s) invalida(s)"] if invalid else []


def validate_non_negative(df: pd.DataFrame, columns: list[str]) -> list[str]:
    issues: list[str] = []
    for column in columns:
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce")
        invalid = int(((values < 0) & values.notna()).sum())
        if invalid:
            issues.append(f"coluna `{column}` com {invalid} valor(es) negativos")
    return issues


def validate_relationships(dim_prod: pd.DataFrame, fact_prod: pd.DataFrame, dim_rota: pd.DataFrame) -> list[str]:
    issues: list[str] = []

    prod_ids = set(dim_prod["id_produtor"].astype(str))
    fact_prod_ids = set(fact_prod["id_produtor"].astype(str))
    missing_prod = sorted(fact_prod_ids - prod_ids)
    if missing_prod:
        issues.append(f"{len(missing_prod)} produtor(es) na fato sem cadastro em `dim_produtor.csv`")

    route_ids = set(dim_rota["id_rota"].astype(str))
    fact_route_ids = set(fact_prod["id_rota"].astype(str))
    missing_route = sorted(fact_route_ids - route_ids)
    if missing_route:
        issues.append(f"{len(missing_route)} rota(s) na fato sem cadastro em `dim_rota.csv`")

    duplicates = int(dim_prod["id_produtor"].astype(str).duplicated().sum())
    if duplicates:
        issues.append(f"`dim_produtor.csv` tem {duplicates} ID(s) de produtor duplicado(s)")

    return issues


def validate_package(data_dir: Path) -> dict:
    report = {
        "status": "ok",
        "required_files": {},
        "optional_files": {},
        "relationship_issues": [],
        "summary": {},
    }

    loaded: dict[str, pd.DataFrame] = {}

    for filename, required_columns in REQUIRED_FILES.items():
        path = data_dir / filename
        file_report = {"exists": path.exists(), "missing_columns": [], "issues": []}
        if not path.exists():
            report["status"] = "error"
            report["required_files"][filename] = file_report
            continue

        df = read_csv(path)
        loaded[filename] = df
        file_report["rows"] = int(len(df))
        file_report["missing_columns"] = validate_columns(df, required_columns)
        if file_report["missing_columns"]:
            report["status"] = "error"

        if "data" in df.columns:
            file_report["issues"].extend(validate_dates(df, "data"))
        if "data_inicio_fornecimento" in df.columns:
            file_report["issues"].extend(validate_dates(df, "data_inicio_fornecimento"))

        file_report["issues"].extend(
            validate_non_negative(
                df,
                [
                    "litros_coletados",
                    "litros_previstos",
                    "litros_produzidos",
                    "litros_descartados",
                    "distancia_km_laticinio",
                    "km_planejado",
                    "capacidade_tanque_litros",
                ],
            )
        )
        report["required_files"][filename] = file_report

    for filename, required_columns in OPTIONAL_FILES.items():
        path = data_dir / filename
        file_report = {"exists": path.exists(), "missing_columns": [], "issues": []}
        if path.exists():
            df = read_csv(path)
            file_report["rows"] = int(len(df))
            file_report["missing_columns"] = validate_columns(df, required_columns)
            file_report["issues"].extend(validate_dates(df, "data"))
            file_report["issues"].extend(
                validate_non_negative(df, ["litros_previstos", "litros_realizados", "km_rodados", "tempo_total_horas"])
            )
        report["optional_files"][filename] = file_report

    if all(name in loaded for name in ("dim_produtor.csv", "fact_producao_produtor_dia.csv", "dim_rota.csv")):
        report["relationship_issues"] = validate_relationships(
            loaded["dim_produtor.csv"],
            loaded["fact_producao_produtor_dia.csv"],
            loaded["dim_rota.csv"],
        )
        if report["relationship_issues"]:
            report["status"] = "warning" if report["status"] == "ok" else report["status"]

    report["summary"] = {
        "required_files_present": sum(1 for item in report["required_files"].values() if item["exists"]),
        "required_files_total": len(REQUIRED_FILES),
        "optional_files_present": sum(1 for item in report["optional_files"].values() if item["exists"]),
        "optional_files_total": len(OPTIONAL_FILES),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida o pacote minimo de dados reais do Via Leite.")
    parser.add_argument("--data-dir", type=Path, required=True, help="Diretorio com os CSVs do cliente.")
    parser.add_argument("--out", type=Path, default=None, help="Arquivo JSON opcional para salvar o relatorio.")
    args = parser.parse_args()

    report = validate_package(args.data_dir)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.out:
        args.out.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
