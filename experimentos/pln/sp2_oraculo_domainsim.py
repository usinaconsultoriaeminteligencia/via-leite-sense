"""SP2 (PLN) com o DomainSim como oráculo independente do lançamento.

Matérias: Processamento de Linguagem Natural (SP2), com o núcleo do DomainSim.

Por que existe: o corpus de fala real (pln.md §4.2) não será coletado a tempo da banca.
Este experimento NÃO substitui linguagem real. Ele troca a pergunta "o modelo entende o
produtor real?" (que continua em aberto) por outra que dá para responder com rigor:
"quando o pipeline lança um volume, o lançamento é consistente com os fatos do domínio?"

Como:
  1. Para cada fazenda, um cenário DomainSim (`ScenarioDefinition`, natureza "synthetic")
     guarda os fatos: entradas de ordenha no tanque e coletas do caminhão, em Decimal L.
  2. Cada entrada vira uma mensagem do produtor, escrita com a família C de frases
     (vocabulário diferente das famílias A, do treino, e B, do teste fora da distribuição).
  3. O pipeline do SP2 extrai o volume de cada mensagem.
  4. Monta-se um segundo cenário com as entradas EXTRAÍDAS e as mesmas coletas, e o
     DomainSim reconcilia. Se faltar leite para uma coleta, o DomainSim recusa
     (`DomainError`, saldo insuficiente): o erro silencioso vira erro detectado.

O DomainSim é usado só como biblioteca, sem nenhuma alteração (D:\\PROJETOS_CODEX\\domainsim,
AGENTS.md). Caminho configurável por DOMAINSIM_SRC.

Uso (da raiz):  python -m experimentos.pln.sp2_oraculo_domainsim
"""
from __future__ import annotations

import json
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

DOMAINSIM_SRC = Path(os.environ.get("DOMAINSIM_SRC", r"D:\PROJETOS_CODEX\domainsim\src"))
sys.path.insert(0, str(DOMAINSIM_SRC))
from domainsim import Movement, MovementKind, ScenarioDefinition, StockSnapshot  # noqa: E402
from domainsim.engine import DomainError, replay  # noqa: E402

from experimentos.pln.corpus_sintetico import por_extenso, sem_acento  # noqa: E402
from experimentos.pln.sp2_pipeline import extrair_entidades, volume_de  # noqa: E402

SAIDA = Path(__file__).parent / "resultados"
BRT = timezone(timedelta(hours=-3))
INICIO = datetime(2026, 10, 1, 0, 0, tzinfo=BRT)

# Família C: frases de entrega escritas à parte, sem reaproveitar A nem B.
FAMILIA_C = [
    "botei {VOL} no resfriador {QUANDO}",
    "{QUANDO} a ordenha rendeu {VOL}",
    "ficou {VOL} no tanque da {TURNO}",
    "produção da {TURNO}: {VOL}",
    "coloquei {VOL} {QUANDO} no tanque",
    "{VOL} da {TURNO} já ta no frio",
]
UNIDADES_C = [" litros", " L", "L", " lt", " litro", " de leite", "", ""]  # "" = sem unidade, como o produtor escreve


def mensagem_de(quantidade: int, turno: str, rng: random.Random) -> str:
    vol = por_extenso(quantidade) if rng.random() < 0.2 else str(quantidade)
    vol += rng.choice(UNIDADES_C)
    t = rng.choice(FAMILIA_C).format(VOL=vol, QUANDO=rng.choice(["hoje", "agora", "nessa ordenha"]), TURNO=turno)
    if rng.random() < 0.35:
        t = sem_acento(t)
    return t


def cenario(fazenda: str, entradas: list[tuple[datetime, Decimal]], coletas: list[tuple[datetime, Decimal]],
            fonte: str) -> ScenarioDefinition:
    movs, seq = [], 0
    for i, (quando, q) in enumerate(entradas):
        seq += 1
        movs.append(Movement(f"{fazenda}-e{i}", fazenda, MovementKind.ENTRY, quando, quando, seq, q, "L", fonte))
    for i, (quando, q) in enumerate(coletas):
        seq += 1
        movs.append(Movement(f"{fazenda}-c{i}", fazenda, MovementKind.COLLECTION, quando, quando, seq, q, "L", fonte))
    ultimo = max(m.occurred_at for m in movs)
    inicial = StockSnapshot(fazenda, INICIO, INICIO, Decimal("0"), Decimal("4000"), "L", fonte)
    return ScenarioDefinition(f"sp2-{fazenda}", "1", fonte, "synthetic", ultimo, ultimo + timedelta(hours=1), inicial, tuple(movs))


def simular_fazenda(idx: int, rng: random.Random, dias: int = 14) -> dict:
    """Fatos verdadeiros: duas ordenhas por dia; coleta a cada 2 dias leva todo o tanque."""
    fazenda = f"F{idx:02d}"
    media = rng.choice([120, 180, 250, 320, 450, 600])  # litros por ordenha
    entradas, coletas, mensagens, saldo = [], [], [], 0
    for d in range(dias):
        for h, turno in ((6, "manhã"), (17, "tarde")):
            q = max(20, int(rng.gauss(media, media * 0.12)))
            q -= q % 5 if rng.random() < 0.5 else 0
            quando = INICIO + timedelta(days=d, hours=h)
            entradas.append((quando, Decimal(q)))
            mensagens.append({"quando": quando, "verdade": q, "texto": mensagem_de(q, turno, rng)})
            saldo += q
        if d % 2 == 1:
            coletas.append((INICIO + timedelta(days=d, hours=20), Decimal(saldo)))
            saldo = 0
    return {"fazenda": fazenda, "entradas": entradas, "coletas": coletas, "mensagens": mensagens}


def corromper(v: int | None, rng: random.Random, taxa: float) -> int | None:
    """Controle de sensibilidade: erros típicos de leitura do campo crítico (pln.md §6.1)."""
    if v is None or rng.random() >= taxa:
        return v
    if rng.random() < 0.5 and v >= 100:
        return v // 10  # dígito perdido: 320 -> 32
    return v * 10  # zero a mais: 32 -> 320


def avaliar_fazenda(f: dict, taxa_erro: float = 0.0, rng: random.Random | None = None) -> dict:
    verdade = cenario(f["fazenda"], f["entradas"], f["coletas"], "domainsim:fatos")
    ref = replay(verdade)  # balanço de referência (os fatos fecham por construção)
    lidas = []
    for m in f["mensagens"]:
        v = volume_de(m["texto"], extrair_entidades(m["texto"]))
        if taxa_erro:
            v = corromper(v, rng, taxa_erro)
        lidas.append({**m, "lido": v})
    ausentes = [m for m in lidas if m["lido"] is None]
    errados = [m for m in lidas if m["lido"] not in (None, m["verdade"])]
    res = {"fazenda": f["fazenda"], "mensagens": len(lidas), "nao_lidas": len(ausentes), "lidas_erradas": len(errados),
           "estoque_final_referencia_L": str(ref.stock_volume), "exemplos_erro": [(m["texto"], m["verdade"], m["lido"]) for m in errados[:3]],
           "exemplos_nao_lidas": [m["texto"] for m in ausentes[:3]]}
    # Modo (a): o que não foi lido não é lançado. Modo (b): o gestor confirma as pendências
    # (recebe o valor verdadeiro), e o oráculo julga só o que o pipeline lançou sozinho.
    for modo, com_confirmacao in (("sem_confirmacao", False), ("com_confirmacao", True)):
        extraidas = [(m["quando"], Decimal(m["verdade"] if m["lido"] is None else m["lido"]))
                     for m in lidas if m["lido"] is not None or com_confirmacao]
        try:
            lancado = replay(cenario(f["fazenda"], extraidas, f["coletas"], "sp2:lancamentos"))
            res[modo] = {"reconciliacao": "aceita", "divergencia_final_L": str(lancado.stock_volume - ref.stock_volume)}
        except DomainError as e:
            res[modo] = {"reconciliacao": "recusada", "codigo": e.code, "evento": e.event_id}
    return res


def controle(fazendas: list[dict], taxa: float) -> dict:
    """Injeta erros conhecidos (modo com confirmação humana) e mede o que o DomainSim pega."""
    rng = random.Random(7)
    rs = [avaliar_fazenda(f, taxa, rng) for f in fazendas]
    com_erro = [r for r in rs if r["lidas_erradas"]]
    recusadas = [r for r in com_erro if r["com_confirmacao"]["reconciliacao"] == "recusada"]
    divergentes = [r for r in com_erro if r["com_confirmacao"]["reconciliacao"] == "aceita"
                   and Decimal(r["com_confirmacao"]["divergencia_final_L"]) != 0]
    return {"taxa_injetada": taxa, "erros_injetados": sum(r["lidas_erradas"] for r in rs),
            "fazendas_com_erro": len(com_erro), "recusadas_pelo_domainsim": len(recusadas),
            "aceitas_com_divergencia": len(divergentes)}


def contar(resultados: list[dict], modo: str) -> tuple[int, int]:
    recus = sum(r[modo]["reconciliacao"] == "recusada" for r in resultados)
    diverg = sum(r[modo]["reconciliacao"] == "aceita" and Decimal(r[modo]["divergencia_final_L"]) != 0 for r in resultados)
    return recus, diverg


def main() -> None:
    rng = random.Random(2026)
    fazendas = [simular_fazenda(i + 1, rng) for i in range(20)]
    resultados = [avaliar_fazenda(f) for f in fazendas]
    controles = [controle(fazendas, t) for t in (0.01, 0.03, 0.05)]
    n = sum(r["mensagens"] for r in resultados)
    nao_lidas = sum(r["nao_lidas"] for r in resultados)
    erradas = sum(r["lidas_erradas"] for r in resultados)
    rec_a, div_a = contar(resultados, "sem_confirmacao")
    rec_b, div_b = contar(resultados, "com_confirmacao")
    resumo = {
        "data_execucao": datetime.now().isoformat(timespec="seconds"),
        "domainsim_src": str(DOMAINSIM_SRC),
        "fazendas": len(resultados), "mensagens": n,
        "volume_lido_correto_pct": (n - nao_lidas - erradas) / n * 100,
        "nao_lidas_pct": nao_lidas / n * 100,
        "lidas_erradas_pct": erradas / n * 100,
        "sem_confirmacao": {"recusadas": rec_a, "aceitas_com_divergencia": div_a},
        "com_confirmacao": {"recusadas": rec_b, "aceitas_com_divergencia": div_b},
        "controle_sensibilidade": controles,
        "exemplos_nao_lidas": [t for r in resultados for t in r["exemplos_nao_lidas"]][:8],
        "por_fazenda": resultados,
    }
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "sp2_oraculo_domainsim.json").write_text(json.dumps(resumo, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    F = len(resultados)
    md = [f"# SP2 com oráculo DomainSim ({resumo['data_execucao']})", "",
          f"{F} fazendas × 14 dias × 2 ordenhas = {n} mensagens da família C (vocabulário fora do treino; 25% sem unidade).",
          "Fatos e reconciliação pelo núcleo do DomainSim, sem alteração nele. **Não é linguagem real.**", "",
          "## Leitura do volume (campo crítico)", "",
          "| Medida | Valor |", "|---|---|",
          f"| Volume lido corretamente | {resumo['volume_lido_correto_pct']:.1f} % |",
          f"| Não lido (vai para confirmação humana) | {resumo['nao_lidas_pct']:.1f} % |",
          f"| Lido errado (lançado errado, sem aviso) | {resumo['lidas_erradas_pct']:.1f} % |", "",
          "Exemplos não lidos: " + "; ".join(f"`{t}`" for t in resumo["exemplos_nao_lidas"][:5]), "",
          "## Reconciliação pelo DomainSim", "",
          "| Modo | Fazendas recusadas | Aceitas com estoque divergente |", "|---|---|---|",
          f"| (a) sem confirmação humana: o não lido não é lançado | {rec_a} de {F} | {div_a} de {F} |",
          f"| (b) com confirmação humana das pendências | {rec_b} de {F} | {div_b} de {F} |", "",
          "## Controle de sensibilidade (modo b, erros injetados de propósito)", "",
          "| Taxa injetada | Erros | Fazendas com erro | Recusadas pelo DomainSim | Aceitas com divergência |", "|---|---|---|---|---|"] + [
          f"| {c['taxa_injetada']:.0%} | {c['erros_injetados']} | {c['fazendas_com_erro']} | {c['recusadas_pelo_domainsim']} | {c['aceitas_com_divergencia']} |" for c in controles] + [
          "", "Recusa = coleta maior que o estoque lançado (volume lido a menos). Volume lido a mais fecha o balanço com sobra:",
          "o DomainSim aceita, e só a divergência contra os fatos o revela.", ""]
    texto_md = "\n".join(md) + "\n"
    (SAIDA / "sp2_oraculo_domainsim.md").write_text(texto_md, encoding="utf-8")
    print(texto_md)


if __name__ == "__main__":
    main()
