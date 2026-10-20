"""
Referência pública de qualidade do leite (RBQL) — base real para calibrar C1.

A Piracanjuba não cederá dados (sem acordo, 07/10/2026). A calibração dos
limiares de CCS/CBT passa a se apoiar em norma (IN 76/77) e em distribuição
real pública: o dataset de qualidade da Rede Brasileira de Qualidade do Leite
curado por Cravo et al. (WCAMA/CSBC 2026), publicado no Zenodo sob CC-BY 4.0.

    Fonte:   https://doi.org/10.5281/zenodo.17714633  (arquivo quality_data.csv)
    Bruto:   dados_publicos/rbql_zenodo_17714633/quality_data.csv
    Saída:   dados_publicos/rbql_zenodo_17714633/referencia_qualidade_rbql.csv
             dados_publicos/rbql_zenodo_17714633/resumo_referencia_rbql.json

O que este módulo faz e o que não faz:

- Normaliza o bruto para formato longo (localidade, UF, região, ano, métrica,
  mínimo, máximo, unidade) e verifica a integridade (hash, faixas, mín ≤ máx).
- Resume a faixa de referência por localidade no recorte pedido.
- **Não** escolhe limiar. O dado é agregado por estado/região e por ano; não é
  distribuição por produtor. Serve para fixar unidade e ordem de grandeza.

Unidades (convenção da RBQL e dos laudos, a mesma do gerador sintético):
CCS em mil células/mL; CPP (≈ CBT) em mil UFC/mL; EST e ESD em %.

Uso:
    python -m via_leite.ingest.referencia_qualidade_rbql
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path("dados_publicos/rbql_zenodo_17714633")
BRUTO = BASE_DIR / "quality_data.csv"
SAIDA_CSV = BASE_DIR / "referencia_qualidade_rbql.csv"
SAIDA_RESUMO = BASE_DIR / "resumo_referencia_rbql.json"

DOI = "10.5281/zenodo.17714633"
SHA256_BRUTO = "b683d62de83ee14575ac7abdc21fb9157a86dc5ebdb7909f6f6bcef20f2a4d17"

# Rótulo da fonte -> (UF, região). Nordeste e Norte vêm agregados na fonte.
# "Goiânia (Centro-oeste)" é tomado como Goiás: premissa, ver PROVENIENCIA.md.
LOCALIDADES = {
    "Espirito Santo": ("ES", "Sudeste"),
    "Goiânia (Centro-oeste)": ("GO", "Centro-Oeste"),
    "Mato grosso (Centro-oeste)": ("MT", "Centro-Oeste"),
    "Mato grosso do sul (Centro-oeste)": ("MS", "Centro-Oeste"),
    "Minas Gerais": ("MG", "Sudeste"),
    "Nordeste (como um todo)": (None, "Nordeste"),
    "Norte (como um todo)": (None, "Norte"),
    "Parana": ("PR", "Sul"),
    "Rio Grande do Sul": ("RS", "Sul"),
    "Rio de Janeiro": ("RJ", "Sudeste"),
    "Santa Catarina": ("SC", "Sul"),
    "São Paulo": ("SP", "Sudeste"),
}

# Métrica da fonte -> (nome canônico do projeto, unidade, faixa plausível).
# A fonte escreve "CSS"; o correto é CCS. CPP é o nome da IN 76 para a CBT.
METRICAS = {
    "CSS": ("ccs", "mil_cel_ml", (20, 2000)),
    "CPP": ("cbt", "mil_ufc_ml", (1, 2000)),
    "EST": ("est", "pct", (10, 15)),
    "ESD": ("esd", "pct", (7, 10)),
}

# Limites regulatórios da IN 76/2018, na mesma unidade da referência.
LIMITE_IN76 = {"ccs": 500, "cbt": 300}


def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def carregar_bruto(caminho: Path = BRUTO, verificar_hash: bool = True) -> pd.DataFrame:
    if verificar_hash and sha256(caminho) != SHA256_BRUTO:
        raise ValueError(
            f"{caminho} difere do arquivo publicado no Zenodo ({DOI}). "
            "Baixe de novo ou atualize SHA256_BRUTO e PROVENIENCIA.md juntos."
        )
    return pd.read_csv(caminho, sep=";", encoding="utf-8")


def normalizar(bruto: pd.DataFrame) -> pd.DataFrame:
    desconhecidas = set(bruto["Region"]) - set(LOCALIDADES)
    if desconhecidas:
        raise ValueError(f"Localidades sem mapeamento: {sorted(desconhecidas)}")

    linhas = []
    for _, r in bruto.iterrows():
        uf, regiao = LOCALIDADES[r["Region"]]
        ano = int(str(r["Date"])[:4])
        for chave, (metrica, unidade, (lo, hi)) in METRICAS.items():
            vmin, vmax = float(r[f"{chave}_Min"]), float(r[f"{chave}_Max"])
            # Erro da fonte não se corrige à mão: marca, explica e tira dos resumos.
            motivo = ""
            if vmin > vmax:
                motivo = "mínimo > máximo"
            elif not (lo <= vmin and vmax <= hi):
                motivo = f"fora da faixa plausível {lo}–{hi} {unidade}"
            linhas.append({
                "localidade_fonte": r["Region"],
                "uf": uf,
                "regiao": regiao,
                "ano": ano,
                "metrica": metrica,
                "minimo": vmin,
                "maximo": vmax,
                "unidade": unidade,
                "valido": not motivo,
                "motivo_invalido": motivo,
            })
    return pd.DataFrame(linhas)


def faixa_referencia(ref: pd.DataFrame, metrica: str, uf: str | None = None,
                     regiao: str | None = None, desde: int | None = None) -> dict:
    """Faixa observada (mín. dos mínimos, mediana dos pontos médios, máx. dos máximos)."""
    sel = ref[(ref["metrica"] == metrica) & ref["valido"]]
    if uf is not None:
        sel = sel[sel["uf"] == uf]
    if regiao is not None:
        sel = sel[sel["regiao"] == regiao]
    if desde is not None:
        sel = sel[sel["ano"] >= desde]
    if sel.empty:
        raise ValueError(f"Sem dados para {metrica} uf={uf} regiao={regiao} desde={desde}")
    meio = (sel["minimo"] + sel["maximo"]) / 2
    return {
        "metrica": metrica,
        "unidade": sel["unidade"].iloc[0],
        "anos": [int(sel["ano"].min()), int(sel["ano"].max())],
        "n_pontos": int(len(sel)),
        "minimo": float(sel["minimo"].min()),
        "mediana_ponto_medio": float(meio.median()),
        "maximo": float(sel["maximo"].max()),
    }


def resumir(ref: pd.DataFrame, desde: int = 2019) -> dict:
    recortes = {
        "GO": {"uf": "GO"},
        "Centro-Oeste": {"regiao": "Centro-Oeste"},
        "Brasil (12 localidades)": {},
    }
    return {
        "fonte": f"https://doi.org/{DOI}",
        "sha256_bruto": SHA256_BRUTO,
        "recorte_anos": f"{desde}+",
        "invalidos": ref.loc[~ref["valido"], ["localidade_fonte", "ano", "metrica", "minimo",
                                              "maximo", "motivo_invalido"]].to_dict("records"),
        "limite_in76": {k: {"valor": v, "unidade": METRICAS[{"ccs": "CSS", "cbt": "CPP"}[k]][1]}
                        for k, v in LIMITE_IN76.items()},
        "faixas": {
            nome: {m: faixa_referencia(ref, m, desde=desde, **filtro) for m in ("ccs", "cbt")}
            for nome, filtro in recortes.items()
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--desde", type=int, default=2019, help="primeiro ano do resumo")
    args = ap.parse_args()

    ref = normalizar(carregar_bruto())
    ref.to_csv(SAIDA_CSV, index=False, encoding="utf-8")
    resumo = resumir(ref, desde=args.desde)
    SAIDA_RESUMO.write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(ref)} linhas -> {SAIDA_CSV}")
    for inv in resumo["invalidos"]:
        print(f"  INVÁLIDO na fonte: {inv['localidade_fonte']} {inv['ano']} {inv['metrica']} "
              f"{inv['minimo']}–{inv['maximo']} ({inv['motivo_invalido']})")
    for nome, faixas in resumo["faixas"].items():
        for m, f in faixas.items():
            print(f"  {nome:<24} {m}: {f['minimo']:.0f}–{f['maximo']:.0f} "
                  f"(mediana {f['mediana_ponto_medio']:.0f}) {f['unidade']}  [{f['anos'][0]}–{f['anos'][1]}]")


if __name__ == "__main__":
    main()
