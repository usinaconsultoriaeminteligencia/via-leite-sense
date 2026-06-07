from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from executar_piloto_real import run_real_pilot


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return normalized or "cliente"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def build_markdown_report(cliente: str, summary: dict[str, object]) -> str:
    importacao = summary["importacao"]
    prontidao = summary["prontidao_treino"]
    treino = summary["treino"]
    ambiente = summary["ambiente"]
    comandos = summary["proximos_comandos"]

    linhas = [
        f"# Onboarding do cliente - {cliente}",
        "",
        "## Situação geral",
        "",
        f"- Status da validação: `{importacao['validation']['status']}`",
        f"- Base importada em: `{importacao['output_dir']}`",
        f"- Artefatos configurados em: `{ambiente['MVP_ARTEFATOS_DIR']}`",
        f"- Treino executado: `{'sim' if treino['executed'] else 'não'}`",
        "",
        "## Volume do pacote",
        "",
        f"- Produtores: `{importacao['outputs']['dim_produtor']}`",
        f"- Registros de produção: `{importacao['outputs']['fact_producao_produtor_dia']}`",
        f"- Rotas: `{importacao['outputs']['dim_rota']}`",
        f"- Registros de rota: `{importacao['outputs']['fact_rota_dia']}`",
        f"- Dias disponíveis: `{importacao['outputs']['dim_tempo']}`",
        "",
        "## Prontidão de treino",
        "",
        f"- Pronto para treino: `{'sim' if prontidao['ready'] else 'não'}`",
    ]

    if "rows" in prontidao:
        linhas.extend(
            [
                f"- Linhas na fato de produção: `{prontidao['rows']}`",
                f"- Datas únicas: `{prontidao['unique_dates']}`",
                f"- Fornecedores únicos: `{prontidao['unique_suppliers']}`",
            ]
        )
    if treino["reason"]:
        linhas.append(f"- Observação: {treino['reason']}")

    linhas.extend(
        [
            "",
            "## Comandos prontos",
            "",
            "### API",
            "",
            "```powershell",
            comandos["api"],
            "```",
            "",
            "### Frontend",
            "",
            "```powershell",
            comandos["frontend"],
            "```",
            "",
            "### Dashboard",
            "",
            "```powershell",
            comandos["dashboard"],
            "```",
        ]
    )
    return "\n".join(linhas) + "\n"


def build_launcher_scripts(output_dir: Path, summary: dict[str, object]) -> None:
    comandos = summary["proximos_comandos"]
    write_text(output_dir / "subir_api.ps1", comandos["api"] + "\n")
    write_text(output_dir / "subir_dashboard.ps1", comandos["dashboard"] + "\n")
    write_text(output_dir / "subir_frontend.ps1", comandos["frontend"] + "\n")


def run_client_onboarding(
    cliente: str,
    input_dir: Path,
    output_root: Path = Path("onboarding_clientes"),
    climate_path: Path | None = None,
    skip_train: bool = False,
) -> dict[str, object]:
    cliente_slug = slugify(cliente)
    cliente_dir = output_root / cliente_slug
    base_dir = cliente_dir / "base_operacional"
    artefatos_dir = cliente_dir / "artefatos_modelo"
    relatorios_dir = cliente_dir / "relatorios"

    ensure_dir(cliente_dir)
    ensure_dir(relatorios_dir)

    summary = run_real_pilot(
        input_dir=input_dir,
        base_dir=base_dir,
        artefatos_dir=artefatos_dir,
        climate_path=climate_path,
        skip_train=skip_train,
    )

    summary["cliente"] = {
        "nome": cliente,
        "slug": cliente_slug,
        "diretorio": str(cliente_dir.resolve()),
    }

    report_json = relatorios_dir / "onboarding_resumo.json"
    report_md = relatorios_dir / "onboarding_parecer.md"

    write_text(report_json, json.dumps(summary, ensure_ascii=False, indent=2))
    write_text(report_md, build_markdown_report(cliente, summary))
    build_launcher_scripts(cliente_dir, summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o onboarding operacional de um cliente no Via Leite.")
    parser.add_argument("--cliente", required=True, help="Nome do cliente para organização do onboarding.")
    parser.add_argument("--input-dir", type=Path, required=True, help="Pacote de dados reais do cliente.")
    parser.add_argument("--output-root", type=Path, default=Path("onboarding_clientes"), help="Raiz para os artefatos do onboarding.")
    parser.add_argument("--climate-path", type=Path, default=None, help="Arquivo de clima opcional.")
    parser.add_argument("--skip-train", action="store_true", help="Importa a base, mas não executa treino.")
    args = parser.parse_args()

    summary = run_client_onboarding(
        cliente=args.cliente,
        input_dir=args.input_dir,
        output_root=args.output_root,
        climate_path=args.climate_path,
        skip_train=args.skip_train,
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
