from __future__ import annotations

import math
from datetime import date
import os
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from fornecedor_inteligencia import calcular_scores_fornecedores
from gestor_store import (
    carregar_planos_acao,
    conectar,
    carregar_fornecedores_dim,
    carregar_base_treino_via_leite,
    carregar_lancamentos_gerenciais,
    inativar_fornecedor,
    init_db,
    remover_plano_acao,
    salvar_fornecedor,
    salvar_lancamento_gerencial,
    salvar_plano_acao,
)
from onboarding_cliente import run_client_onboarding
from via_leite_edge import (
    EDGE_DISCLAIMER,
    EDGE_MODULE_NAME,
    EDGE_SOURCE_NAME,
    EdgeSettings,
    carregar_configuracao_edge,
    gerar_alertas,
    obter_provider_iot,
    resumo_premium,
)

def data_dir() -> Path:
    return Path(os.environ.get("MVP_DATA_DIR", "dados_teste"))


def artefatos_dir() -> Path:
    return Path(os.environ.get("MVP_ARTEFATOS_DIR", "artefatos_teste"))

app = FastAPI(
    title="VIA LEITE SENSE API",
    description="API de inteligencia operacional para monitoramento leiteiro, cadeia premium e arquitetura IoT-ready.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8600",
        "http://127.0.0.1:8600",
        "http://localhost:8601",
        "http://127.0.0.1:8601",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SupplierIn(BaseModel):
    id: str | None = None
    nome: str = Field(min_length=1)
    documento: str | None = None
    municipio: str | None = None
    polo: str | None = None
    laticinio: str | None = None
    sistema: str | None = None
    capacidadeLitros: float = 0
    historicoMeses: float = 0
    qualidade: str | None = None
    operacionais: str | None = None
    logisticos: str | None = None
    financeiros: str | None = None
    risco: float = 0


class SupplierPatch(BaseModel):
    nome: str | None = None
    documento: str | None = None
    municipio: str | None = None
    polo: str | None = None
    laticinio: str | None = None
    sistema: str | None = None
    capacidadeLitros: float | None = None
    historicoMeses: float | None = None
    qualidade: str | None = None
    operacionais: str | None = None
    logisticos: str | None = None
    financeiros: str | None = None
    risco: float | None = None


class ManagementEventIn(BaseModel):
    idFornecedor: str | None = None
    idLaticinio: str | None = None
    data: date
    categoria: str
    impactoLitros: float = 0
    valorFinanceiro: float = 0
    responsavel: str = "Gestor"
    descricao: str | None = None


class ActionPlanIn(BaseModel):
    id: str | None = None
    fornecedorId: str | None = None
    tipo: str
    responsavel: str
    prazo: int = Field(default=0, ge=0)
    litros: float = 0
    valor: float = 0
    resultadoLitros: float = 0
    resultadoValor: float = 0
    titulo: str = Field(min_length=1)
    descricao: str = Field(min_length=1)
    risco: str = "Baixo"
    dataPrevista: date | None = None
    observacoes: str | None = None
    evidencias: str | None = None
    status: str = "Aberto"
    origem: str = "Manual"


class ActionPlanPatch(BaseModel):
    responsavel: str | None = None
    prazo: int | None = Field(default=None, ge=0)
    descricao: str | None = None
    resultadoLitros: float | None = None
    resultadoValor: float | None = None
    dataPrevista: date | None = None
    observacoes: str | None = None
    evidencias: str | None = None
    status: str | None = None


class OnboardingRunIn(BaseModel):
    cliente: str = Field(min_length=1)
    inputDir: str = Field(min_length=1)
    outputRoot: str = "onboarding_clientes"
    climatePath: str | None = None
    skipTrain: bool = False


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (pd.Timestamp, date)):
        return value.isoformat()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if pd.isna(value):
        return None
    return value


def _classe_risco(score: float) -> str:
    if score >= 75:
        return "Alto"
    if score >= 50:
        return "Médio"
    return "Baixo"


def _ler_csvs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    base_dir = data_dir()
    arts_dir = artefatos_dir()
    prod = pd.read_csv(base_dir / "fact_producao_produtor_dia.csv", parse_dates=["data"])
    dim_prod = pd.read_csv(base_dir / "dim_produtor.csv", parse_dates=["data_inicio_fornecimento"])
    pred_path = arts_dir / "predicoes_teste.csv"
    pred = pd.read_csv(pred_path, parse_dates=["data"]) if pred_path.exists() else pd.DataFrame()
    return prod, dim_prod, pred


def _scores_base() -> pd.DataFrame:
    prod, dim_prod, pred = _ler_csvs()
    scores = calcular_scores_fornecedores(prod, dim_prod, pred)
    scores["id_produtor"] = scores["id_produtor"].astype(str)
    return scores


def _dim_fornecedores_map() -> dict[str, dict[str, Any]]:
    dim = carregar_fornecedores_dim()
    if dim.empty:
        return {}
    dim["id_fornecedor"] = dim["id_fornecedor"].astype(str)
    return dim.set_index("id_fornecedor").to_dict(orient="index")


def _normalizar_supplier(row: pd.Series, cadastro: dict[str, Any] | None = None) -> dict[str, Any]:
    cadastro = cadastro or {}
    id_fornecedor = str(row.get("id_produtor") or cadastro.get("id_fornecedor") or "")
    nome = cadastro.get("nome_razao_social") or row.get("nome_ficticio") or f"Produtor {id_fornecedor}"
    laticinio = row.get("id_laticinio") or cadastro.get("id_laticinio") or ""
    polo = cadastro.get("polo_localizacao") or row.get("polo_climatico") or ""
    score = float(row.get("score_risco_fornecedor") or cadastro.get("score_qualidade_inicial") or 0)

    return {
        "id": id_fornecedor,
        "nome": _json_safe(nome),
        "documento": _json_safe(cadastro.get("cpf_cnpj") or ""),
        "municipio": _json_safe(row.get("municipio") or polo),
        "polo": _json_safe(str(polo).replace("_", " ").title()),
        "laticinio": f"Laticínio {int(laticinio)}" if str(laticinio).replace(".0", "").isdigit() else _json_safe(laticinio),
        "sistema": _json_safe(str(row.get("tipo_sistema") or "").replace("_", " ").title()),
        "capacidadeLitros": float(cadastro.get("capacidade_tanque_litros") or row.get("litros_coletados_media") or 0),
        "historicoMeses": float(cadastro.get("historico_fornecimento_meses") or 0),
        "qualidade": _json_safe(cadastro.get("indicadores_qualidade") or ""),
        "operacionais": _json_safe(cadastro.get("variaveis_operacionais") or ""),
        "logisticos": _json_safe(cadastro.get("variaveis_logisticas") or ""),
        "financeiros": _json_safe(cadastro.get("variaveis_financeiras") or ""),
        "litrosDia": float(row.get("litros_coletados_media") or 0),
        "risco": score,
        "classeRisco": _classe_risco(score),
        "scoreVolume": float(row.get("score_volume") or 0),
        "scoreQualidade": float(row.get("score_qualidade") or 0),
        "scoreLogistica": float(row.get("score_logistica") or 0),
        "scoreContinuidade": float(row.get("score_continuidade") or 0),
        "tendenciaPct": float(row.get("tendencia_volume_pct") or 0),
        "descartePct": float(row.get("taxa_descarte_pct") or 0),
        "ccs": float(row.get("ccs_media") or 0),
        "cbt": float(row.get("cbt_media") or 0),
        "recomendacao": _json_safe(row.get("recomendacao") or "Manter acompanhamento regular."),
    }


def _suppliers() -> list[dict[str, Any]]:
    init_db(data_dir())
    scores = _scores_base()
    cadastros = _dim_fornecedores_map()
    suppliers: list[dict[str, Any]] = []

    for _, row in scores.iterrows():
        id_produtor = str(row["id_produtor"])
        suppliers.append(_normalizar_supplier(row, cadastros.get(id_produtor)))

    ids_existentes = {item["id"] for item in suppliers}
    for id_fornecedor, cadastro in cadastros.items():
        if id_fornecedor in ids_existentes:
            continue
        vazio = pd.Series({"id_produtor": id_fornecedor, "score_risco_fornecedor": cadastro.get("score_qualidade_inicial") or 0})
        suppliers.append(_normalizar_supplier(vazio, cadastro))

    return sorted(suppliers, key=lambda item: item["risco"], reverse=True)


def _events() -> list[dict[str, Any]]:
    df = carregar_lancamentos_gerenciais()
    if df.empty:
        return []
    out: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        out.append(
            {
                "id": str(row["id_lancamento"]),
                "idFornecedor": _json_safe(row["id_fornecedor"]),
                "idLaticinio": _json_safe(row["id_laticinio"]),
                "data": _json_safe(row["data_referencia"]),
                "categoria": _json_safe(row["categoria_evento"]),
                "impactoLitros": float(row["valor_impacto"] or 0),
                "valorFinanceiro": float(row.get("valor_financeiro") or 0),
                "responsavel": _json_safe(row["registrado_por"]),
                "descricao": _json_safe(row["descricao_detalhada"]),
            }
        )
    return out


def _ensure_supplier_registry_entry(fornecedor_id: str | None, suppliers: list[dict[str, Any]] | None = None) -> None:
    if not fornecedor_id:
        return
    if _dim_fornecedores_map().get(str(fornecedor_id)):
        return
    suppliers = suppliers or _suppliers()
    supplier = next((item for item in suppliers if item["id"] == str(fornecedor_id)), None)
    if not supplier:
        return
    salvar_fornecedor(
        {
            "id_fornecedor": supplier["id"],
            "nome_razao_social": supplier["nome"],
            "cpf_cnpj": supplier.get("documento"),
            "polo_localizacao": supplier.get("polo") or supplier.get("municipio") or "",
            "capacidade_tanque_litros": supplier.get("capacidadeLitros") or supplier.get("litrosDia") or 0,
            "historico_fornecimento_meses": supplier.get("historicoMeses") or 0,
            "indicadores_qualidade": supplier.get("qualidade") or "",
            "variaveis_operacionais": supplier.get("operacionais") or "",
            "variaveis_logisticas": supplier.get("logisticos") or "",
            "variaveis_financeiras": supplier.get("financeiros") or "",
            "score_qualidade_inicial": supplier.get("risco") or 0,
        }
    )


def _tipo_plano_supplier(supplier: dict[str, Any]) -> tuple[str, str, int, float]:
    if supplier["scoreQualidade"] >= 70:
        return "Qualidade", "Coordenação de Qualidade", 10, 0.18
    if supplier["scoreLogistica"] >= 80:
        return "Logística", "Gestão de Rotas", 7, 0.12
    if supplier["tendenciaPct"] < -6:
        return "Campo", "Técnico de Campo", 14, 0.15
    return "Relacionamento", "Captação Comercial", 21, 0.15


def _build_suggested_action_plans(suppliers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plans = []
    for supplier in suppliers:
        if supplier["risco"] < 48 and supplier["scoreQualidade"] < 70 and supplier["scoreLogistica"] < 80:
            continue
        tipo, responsavel, prazo, fator = _tipo_plano_supplier(supplier)
        litros = float(supplier["litrosDia"] or 0) * fator
        plans.append(
            {
                "fornecedorId": supplier["id"],
                "fornecedorNome": supplier["nome"],
                "risco": supplier["classeRisco"],
                "tipo": tipo,
                "responsavel": responsavel,
                "prazo": prazo,
                "litros": litros,
                "valor": litros * 2.25 * 30,
                "resultadoLitros": 0,
                "resultadoValor": 0,
                "titulo": f"{supplier['nome']} - {supplier['municipio']}",
                "descricao": supplier["recomendacao"],
                "dataPrevista": (pd.Timestamp.now().normalize() + pd.Timedelta(days=prazo)).date().isoformat(),
                "observacoes": "",
                "evidencias": "",
                "status": "Aberto",
                "origem": "Sugestão",
            }
        )
    return plans[:12]


def _portfolio(suppliers: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    risk_suppliers = [s for s in suppliers if s["classeRisco"] in ("Alto", "Médio")]
    total_litros = sum(float(s["litrosDia"] or 0) for s in suppliers)
    litros_risco = sum(float(s["litrosDia"] or 0) for s in risk_suppliers)
    score_medio = sum(float(s["risco"] or 0) for s in suppliers) / len(suppliers) if suppliers else 0
    descarte_medio = sum(float(s["descartePct"] or 0) for s in suppliers) / len(suppliers) if suppliers else 0
    impacto = sum(float(e["impactoLitros"] or 0) for e in events)

    return {
        "fornecedores": len(suppliers),
        "criticos": len([s for s in suppliers if s["classeRisco"] == "Alto"]),
        "atencao": len([s for s in suppliers if s["classeRisco"] == "Médio"]),
        "litrosRisco": litros_risco,
        "litrosTotais": total_litros,
        "scoreMedio": score_medio,
        "descartePct": descarte_medio,
        "impactoGerencialLitros": impacto,
    }


def _risk_distribution(suppliers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total = len(suppliers) or 1
    litros_total = sum(float(s["litrosDia"] or 0) for s in suppliers) or 1
    return [
        {
            "classeRisco": classe,
            "fornecedores": len([s for s in suppliers if s["classeRisco"] == classe]),
            "percentual": len([s for s in suppliers if s["classeRisco"] == classe]) / total * 100,
            "litrosDia": sum(float(s["litrosDia"] or 0) for s in suppliers if s["classeRisco"] == classe),
            "percentualLitros": sum(float(s["litrosDia"] or 0) for s in suppliers if s["classeRisco"] == classe)
            / litros_total
            * 100,
        }
        for classe in ("Alto", "Médio", "Baixo")
    ]


def _quality_summary(suppliers: list[dict[str, Any]]) -> dict[str, Any]:
    total_litros = sum(float(s["litrosDia"] or 0) for s in suppliers)
    descarte_medio = sum(float(s["descartePct"] or 0) for s in suppliers) / len(suppliers) if suppliers else 0
    return {
        "ccsMedia": sum(float(s["ccs"] or 0) for s in suppliers) / len(suppliers) if suppliers else 0,
        "cbtMedia": sum(float(s["cbt"] or 0) for s in suppliers) / len(suppliers) if suppliers else 0,
        "descartePct": descarte_medio,
        "descarteAtacavelLitros": total_litros * descarte_medio / 100 * 0.32,
        "fornecedoresQualidadeCritica": len([s for s in suppliers if float(s["scoreQualidade"] or 0) >= 70]),
    }


def _action_plans(suppliers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if carregar_planos_acao().empty:
        for plan in _build_suggested_action_plans(suppliers):
            _ensure_supplier_registry_entry(plan["fornecedorId"], suppliers)
            salvar_plano_acao(
                {
                    "id_fornecedor": plan["fornecedorId"],
                    "titulo": plan["titulo"],
                    "descricao": plan["descricao"],
                    "tipo_plano": plan["tipo"],
                    "classe_risco": plan["risco"],
                    "responsavel": plan["responsavel"],
                    "prazo_dias": plan["prazo"],
                    "litros_potenciais": plan["litros"],
                    "valor_potencial": plan["valor"],
                    "litros_resultado": plan["resultadoLitros"],
                    "valor_resultado": plan["resultadoValor"],
                    "data_prevista": plan["dataPrevista"],
                    "observacoes": plan["observacoes"],
                    "evidencias": plan["evidencias"],
                    "status_plano": plan["status"],
                    "origem_plano": plan["origem"],
                }
            )

    df = carregar_planos_acao()
    suppliers_map = {supplier["id"]: supplier for supplier in suppliers}
    plans: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        fornecedor_id = str(row.get("id_fornecedor") or "")
        supplier = suppliers_map.get(fornecedor_id, {})
        plans.append(
            {
                "id": str(row["id_plano"]),
                "fornecedorId": fornecedor_id or None,
                "fornecedorNome": supplier.get("nome"),
                "risco": _json_safe(row.get("classe_risco") or supplier.get("classeRisco") or "Baixo"),
                "tipo": _json_safe(row.get("tipo_plano") or ""),
                "responsavel": _json_safe(row.get("responsavel") or ""),
                "prazo": int(row.get("prazo_dias") or 0),
                "litros": float(row.get("litros_potenciais") or 0),
                "valor": float(row.get("valor_potencial") or 0),
                "resultadoLitros": float(row.get("litros_resultado") or 0),
                "resultadoValor": float(row.get("valor_resultado") or 0),
                "dataPrevista": _json_safe(row.get("data_prevista")),
                "observacoes": _json_safe(row.get("observacoes") or ""),
                "evidencias": _json_safe(row.get("evidencias") or ""),
                "titulo": _json_safe(row.get("titulo") or ""),
                "descricao": _json_safe(row.get("descricao") or ""),
                "status": _json_safe(row.get("status_plano") or "Aberto"),
                "origem": _json_safe(row.get("origem_plano") or "Manual"),
                "criadoEm": _json_safe(row.get("criado_em")),
                "atualizadoEm": _json_safe(row.get("atualizado_em")),
                "concluidoEm": _json_safe(row.get("concluido_em")),
            }
        )
    return plans


def _action_plan_effectiveness(plans: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [plan for plan in plans if plan.get("status") == "Concluido"]

    def summarize(items: list[dict[str, Any]], key: str, label_key: str | None = None) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, Any]] = {}
        for item in items:
            group_key = str(item.get(key) or "Não informado")
            bucket = grouped.setdefault(
                group_key,
                {
                    "label": item.get(label_key or key) or group_key,
                    "planos": 0,
                    "metaLitros": 0.0,
                    "resultadoLitros": 0.0,
                    "metaValor": 0.0,
                    "resultadoValor": 0.0,
                },
            )
            bucket["planos"] += 1
            bucket["metaLitros"] += float(item.get("litros") or 0)
            bucket["resultadoLitros"] += float(item.get("resultadoLitros") or 0)
            bucket["metaValor"] += float(item.get("valor") or 0)
            bucket["resultadoValor"] += float(item.get("resultadoValor") or 0)

        out = []
        for bucket in grouped.values():
            meta_litros = float(bucket["metaLitros"] or 0)
            resultado_litros = float(bucket["resultadoLitros"] or 0)
            efetividade = (resultado_litros / meta_litros * 100) if meta_litros else 0.0
            out.append(
                {
                    **bucket,
                    "desvioLitros": resultado_litros - meta_litros,
                    "desvioValor": float(bucket["resultadoValor"] or 0) - float(bucket["metaValor"] or 0),
                    "efetividadePct": efetividade,
                }
            )
        return sorted(out, key=lambda item: (item["efetividadePct"], item["resultadoLitros"]), reverse=True)

    total_meta_litros = sum(float(plan.get("litros") or 0) for plan in completed)
    total_resultado_litros = sum(float(plan.get("resultadoLitros") or 0) for plan in completed)
    total_meta_valor = sum(float(plan.get("valor") or 0) for plan in completed)
    total_resultado_valor = sum(float(plan.get("resultadoValor") or 0) for plan in completed)

    return {
        "resumo": {
            "planosConcluidos": len(completed),
            "metaLitros": total_meta_litros,
            "resultadoLitros": total_resultado_litros,
            "metaValor": total_meta_valor,
            "resultadoValor": total_resultado_valor,
            "efetividadePct": (total_resultado_litros / total_meta_litros * 100) if total_meta_litros else 0.0,
        },
        "porTipo": summarize(completed, "tipo"),
        "porResponsavel": summarize(completed, "responsavel"),
        "porFornecedor": summarize(completed, "fornecedorId", "fornecedorNome"),
    }


def _edge_snapshot() -> dict[str, Any]:
    settings = carregar_configuracao_edge()
    source = EDGE_SOURCE_NAME
    note = None

    try:
        provider = obter_provider_iot(settings)
        leituras = provider.get_latest_readings()
    except NotImplementedError:
        fallback_settings = EdgeSettings(
            simulation_mode=True,
            provider_name="simulated",
            sample_size=settings.sample_size,
            data_dir=settings.data_dir,
        )
        provider = obter_provider_iot(fallback_settings)
        leituras = provider.get_latest_readings()
        source = f"{EDGE_SOURCE_NAME}_FALLBACK"
        note = "Provider IoT real ainda nao implementado; retorno em modo simulado para demonstracao."
    except Exception as exc:
        return {
            "status": "degraded",
            "module": EDGE_MODULE_NAME,
            "source": "EDGE_SAFE_FALLBACK",
            "disclaimer": EDGE_DISCLAIMER,
            "readings": [],
            "alerts": [],
            "error": str(exc),
        }

    alertas = []
    for leitura in leituras:
        alertas.extend(gerar_alertas(leitura))

    leituras_com_premium = [{**leitura.to_dict(), **resumo_premium(leitura)} for leitura in leituras]

    payload = {
        "status": "success",
        "module": EDGE_MODULE_NAME,
        "source": source,
        "disclaimer": EDGE_DISCLAIMER,
        "readings": leituras_com_premium,
        "alerts": sorted(
            (alerta.to_dict() for alerta in alertas),
            key=lambda item: ({"ALTA": 0, "MEDIA": 1, "BAIXA": 2}.get(item["severity"], 9), item["farm_id"], item["id"]),
        ),
    }
    if note:
        payload["note"] = note
    return payload


@app.on_event("startup")
def startup() -> None:
    init_db(data_dir())


@app.get("/health")
def health() -> dict[str, Any]:
    init_db(data_dir())
    return {
        "status": "ok",
        "database": str(Path(os.environ.get("MVP_USER_DATA_DIR", "dados_utilizador")) / "via_leite.duckdb"),
        "dataDir": str(data_dir()),
        "artefatosDir": str(artefatos_dir()),
    }


@app.post("/onboarding/run")
def onboarding_run(payload: OnboardingRunIn) -> dict[str, Any]:
    try:
        summary = run_client_onboarding(
            cliente=payload.cliente,
            input_dir=Path(payload.inputDir),
            output_root=Path(payload.outputRoot),
            climate_path=Path(payload.climatePath) if payload.climatePath else None,
            skip_train=payload.skipTrain,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return summary


@app.get("/portfolio")
def portfolio() -> dict[str, Any]:
    suppliers = _suppliers()
    events = _events()
    return _portfolio(suppliers, events)


@app.get("/suppliers")
def list_suppliers() -> list[dict[str, Any]]:
    return _suppliers()


@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: str) -> dict[str, Any]:
    for supplier in _suppliers():
        if supplier["id"] == supplier_id:
            return supplier
    raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")


@app.post("/suppliers", status_code=201)
def create_supplier(payload: SupplierIn) -> dict[str, Any]:
    supplier_id = salvar_fornecedor(
        {
            "id_fornecedor": payload.id,
            "nome_razao_social": payload.nome,
            "cpf_cnpj": payload.documento,
            "polo_localizacao": payload.polo or payload.municipio or "",
            "capacidade_tanque_litros": payload.capacidadeLitros,
            "historico_fornecimento_meses": payload.historicoMeses,
            "indicadores_qualidade": payload.qualidade or "",
            "variaveis_operacionais": payload.operacionais or "",
            "variaveis_logisticas": payload.logisticos or "",
            "variaveis_financeiras": payload.financeiros or "",
            "score_qualidade_inicial": payload.risco,
        }
    )
    return get_supplier(supplier_id)


@app.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: str, payload: SupplierIn) -> dict[str, Any]:
    payload.id = supplier_id
    supplier_id = salvar_fornecedor(
        {
            "id_fornecedor": supplier_id,
            "nome_razao_social": payload.nome,
            "cpf_cnpj": payload.documento,
            "polo_localizacao": payload.polo or payload.municipio or "",
            "capacidade_tanque_litros": payload.capacidadeLitros,
            "historico_fornecimento_meses": payload.historicoMeses,
            "indicadores_qualidade": payload.qualidade or "",
            "variaveis_operacionais": payload.operacionais or "",
            "variaveis_logisticas": payload.logisticos or "",
            "variaveis_financeiras": payload.financeiros or "",
            "score_qualidade_inicial": payload.risco,
        }
    )
    return get_supplier(supplier_id)


@app.patch("/suppliers/{supplier_id}")
def patch_supplier(supplier_id: str, payload: SupplierPatch) -> dict[str, Any]:
    current = get_supplier(supplier_id)
    updates = payload.dict(exclude_unset=True, exclude_none=True)
    merged = current | updates
    return update_supplier(supplier_id, SupplierIn(**merged))


@app.delete("/suppliers/{supplier_id}", status_code=204, response_class=Response)
def delete_supplier(supplier_id: str) -> Response:
    get_supplier(supplier_id)
    inativar_fornecedor(supplier_id)
    return Response(status_code=204)


@app.get("/management-events")
def list_management_events() -> list[dict[str, Any]]:
    return _events()


@app.post("/management-events", status_code=201)
def create_management_event(payload: ManagementEventIn) -> dict[str, Any]:
    if payload.idFornecedor:
        known = {supplier["id"]: supplier for supplier in _suppliers()}
        supplier = known.get(payload.idFornecedor)
        if supplier and not _dim_fornecedores_map().get(payload.idFornecedor):
            salvar_fornecedor(
                {
                    "id_fornecedor": supplier["id"],
                    "nome_razao_social": supplier["nome"],
                    "polo_localizacao": supplier["polo"],
                    "capacidade_tanque_litros": supplier["capacidadeLitros"],
                    "score_qualidade_inicial": supplier["risco"],
                }
            )

    id_laticinio = payload.idLaticinio
    if not id_laticinio and payload.idFornecedor:
        supplier = next((item for item in _suppliers() if item["id"] == payload.idFornecedor), None)
        if supplier:
            id_laticinio = str(supplier["laticinio"]).replace("Laticínio", "").strip()

    event_id = salvar_lancamento_gerencial(
        {
            "data_referencia": payload.data,
            "id_fornecedor": payload.idFornecedor,
            "id_laticinio": id_laticinio or "",
            "categoria_evento": payload.categoria,
            "valor_impacto": payload.impactoLitros,
            "valor_financeiro": payload.valorFinanceiro,
            "descricao_detalhada": payload.descricao or "",
            "registrado_por": payload.responsavel,
        }
    )
    return next(event for event in _events() if event["id"] == event_id)


@app.delete("/management-events", status_code=204, response_class=Response)
def clear_management_events() -> Response:
    init_db(data_dir())
    with conectar() as con:
        con.execute("DELETE FROM fact_lancamento_gerencial;")
    return Response(status_code=204)


@app.get("/action-plans")
def action_plans() -> list[dict[str, Any]]:
    return _action_plans(_suppliers())


@app.get("/action-plans/effectiveness")
def action_plans_effectiveness() -> dict[str, Any]:
    return _action_plan_effectiveness(_action_plans(_suppliers()))


@app.post("/action-plans/bootstrap")
def bootstrap_action_plans() -> list[dict[str, Any]]:
    suppliers = _suppliers()
    existing = carregar_planos_acao()
    existing_pairs = {
        (str(row["id_fornecedor"] or ""), str(row["tipo_plano"] or ""), str(row["status_plano"] or ""))
        for _, row in existing.iterrows()
    }
    for plan in _build_suggested_action_plans(suppliers):
        key = (str(plan["fornecedorId"] or ""), str(plan["tipo"]), "Aberto")
        if key in existing_pairs:
            continue
        _ensure_supplier_registry_entry(plan["fornecedorId"], suppliers)
        salvar_plano_acao(
            {
                "id_fornecedor": plan["fornecedorId"],
                "titulo": plan["titulo"],
                "descricao": plan["descricao"],
                "tipo_plano": plan["tipo"],
                "classe_risco": plan["risco"],
                "responsavel": plan["responsavel"],
                "prazo_dias": plan["prazo"],
                "litros_potenciais": plan["litros"],
                "valor_potencial": plan["valor"],
                "litros_resultado": plan["resultadoLitros"],
                "valor_resultado": plan["resultadoValor"],
                "data_prevista": plan["dataPrevista"],
                "observacoes": plan["observacoes"],
                "evidencias": plan["evidencias"],
                "status_plano": "Aberto",
                "origem_plano": "Sugestão",
            }
        )
    return _action_plans(suppliers)


@app.post("/action-plans", status_code=201)
def create_action_plan(payload: ActionPlanIn) -> dict[str, Any]:
    _ensure_supplier_registry_entry(payload.fornecedorId)
    plan_id = salvar_plano_acao(
        {
            "id_plano": payload.id,
            "id_fornecedor": payload.fornecedorId,
            "titulo": payload.titulo,
            "descricao": payload.descricao,
            "tipo_plano": payload.tipo,
            "classe_risco": payload.risco,
            "responsavel": payload.responsavel,
            "prazo_dias": payload.prazo,
            "litros_potenciais": payload.litros,
            "valor_potencial": payload.valor,
            "litros_resultado": payload.resultadoLitros,
            "valor_resultado": payload.resultadoValor,
            "data_prevista": payload.dataPrevista,
            "observacoes": payload.observacoes,
            "evidencias": payload.evidencias,
            "status_plano": payload.status,
            "origem_plano": payload.origem,
        }
    )
    plan = next((item for item in _action_plans(_suppliers()) if item["id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=500, detail="Plano de ação não encontrado após gravação.")
    return plan


@app.patch("/action-plans/{plan_id}")
def patch_action_plan(plan_id: str, payload: ActionPlanPatch) -> dict[str, Any]:
    df = carregar_planos_acao()
    row = df[df["id_plano"].astype(str) == str(plan_id)] if not df.empty else pd.DataFrame()
    if row.empty:
        raise HTTPException(status_code=404, detail="Plano de ação não encontrado.")
    current = row.iloc[0]
    status = payload.status or str(current.get("status_plano") or "Aberto")
    salvar_plano_acao(
        {
            "id_plano": plan_id,
            "id_fornecedor": current.get("id_fornecedor"),
            "titulo": current.get("titulo"),
            "descricao": payload.descricao if payload.descricao is not None else current.get("descricao"),
            "tipo_plano": current.get("tipo_plano"),
            "classe_risco": current.get("classe_risco"),
            "responsavel": payload.responsavel if payload.responsavel is not None else current.get("responsavel"),
            "prazo_dias": payload.prazo if payload.prazo is not None else current.get("prazo_dias"),
            "litros_potenciais": current.get("litros_potenciais"),
            "valor_potencial": current.get("valor_potencial"),
            "litros_resultado": payload.resultadoLitros if payload.resultadoLitros is not None else current.get("litros_resultado"),
            "valor_resultado": payload.resultadoValor if payload.resultadoValor is not None else current.get("valor_resultado"),
            "data_prevista": payload.dataPrevista if payload.dataPrevista is not None else current.get("data_prevista"),
            "observacoes": payload.observacoes if payload.observacoes is not None else current.get("observacoes"),
            "evidencias": payload.evidencias if payload.evidencias is not None else current.get("evidencias"),
            "status_plano": status,
            "origem_plano": current.get("origem_plano"),
            "criado_em": current.get("criado_em"),
            "atualizado_em": pd.Timestamp.now(),
            "concluido_em": pd.Timestamp.now() if status == "Concluido" else None,
        }
    )
    plan = next((item for item in _action_plans(_suppliers()) if item["id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=500, detail="Plano de ação não encontrado após atualização.")
    return plan


@app.delete("/action-plans/{plan_id}", status_code=204, response_class=Response)
def delete_action_plan(plan_id: str) -> Response:
    if not remover_plano_acao(plan_id):
        raise HTTPException(status_code=404, detail="Plano de ação não encontrado.")
    return Response(status_code=204)


@app.get("/risk-distribution")
def risk_distribution() -> list[dict[str, Any]]:
    return _risk_distribution(_suppliers())


@app.get("/quality-summary")
def quality_summary() -> dict[str, Any]:
    return _quality_summary(_suppliers())


@app.get("/supplier-events/{supplier_id}")
def supplier_events(supplier_id: str) -> list[dict[str, Any]]:
    get_supplier(supplier_id)
    return [event for event in _events() if event["idFornecedor"] == supplier_id]


@app.get("/training-base/summary")
def training_base_summary() -> dict[str, Any]:
    df = carregar_base_treino_via_leite(data_dir())
    if df.empty:
        return {"linhas": 0, "colunas": 0, "dataInicial": None, "dataFinal": None}
    data_col = pd.to_datetime(df["data"], errors="coerce") if "data" in df.columns else pd.Series(dtype="datetime64[ns]")
    return {
        "linhas": int(len(df)),
        "colunas": int(len(df.columns)),
        "dataInicial": _json_safe(data_col.min()) if not data_col.empty else None,
        "dataFinal": _json_safe(data_col.max()) if not data_col.empty else None,
        "fornecedores": int(df["id_produtor"].nunique()) if "id_produtor" in df.columns else 0,
        "laticinios": int(df["id_laticinio"].nunique()) if "id_laticinio" in df.columns else 0,
        "eventosGerenciais": int(df["qtd_eventos_gerenciais"].sum()) if "qtd_eventos_gerenciais" in df.columns else 0,
    }


@app.get("/impact")
def impact() -> dict[str, Any]:
    suppliers = _suppliers()
    events = _events()
    portfolio = _portfolio(suppliers, events)
    risk_liters = float(portfolio["litrosRisco"])
    avoidable_discard = float(portfolio["litrosTotais"]) * float(portfolio["descartePct"]) / 100 * 0.32
    protected_revenue = risk_liters * 2.25 * 30
    return {
        "litrosRisco": risk_liters,
        "descarteAtacavel": avoidable_discard,
        "valorMensalMonitorado": protected_revenue,
        "eventosGerenciais": len(events),
    }


@app.get("/api/iot/simulated-readings")
def iot_simulated_readings() -> dict[str, Any]:
    snapshot = _edge_snapshot()
    return {
        "status": snapshot["status"],
        "module": snapshot["module"],
        "source": snapshot["source"],
        "disclaimer": snapshot["disclaimer"],
        "readings": snapshot.get("readings", []),
        "alertsCount": len(snapshot.get("alerts", [])),
        **({"note": snapshot["note"]} if snapshot.get("note") else {}),
        **({"error": snapshot["error"]} if snapshot.get("error") else {}),
    }


@app.get("/api/iot/farms/{farm_id}/latest")
def iot_farm_latest(farm_id: str) -> dict[str, Any]:
    snapshot = _edge_snapshot()
    leitura = next((item for item in snapshot.get("readings", []) if item["farm_id"] == farm_id), None)
    if leitura is None and snapshot["status"] == "success":
        raise HTTPException(status_code=404, detail="Fazenda nao encontrada nas leituras EDGE.")
    return {
        "status": snapshot["status"],
        "module": snapshot["module"],
        "source": snapshot["source"],
        "disclaimer": snapshot["disclaimer"],
        "readings": [leitura] if leitura else [],
        **({"note": snapshot["note"]} if snapshot.get("note") else {}),
        **({"error": snapshot["error"]} if snapshot.get("error") else {}),
    }


@app.get("/api/iot/alerts")
def iot_alerts() -> dict[str, Any]:
    snapshot = _edge_snapshot()
    return {
        "status": snapshot["status"],
        "module": snapshot["module"],
        "source": snapshot["source"],
        "disclaimer": snapshot["disclaimer"],
        "alerts": snapshot.get("alerts", []),
        **({"note": snapshot["note"]} if snapshot.get("note") else {}),
        **({"error": snapshot["error"]} if snapshot.get("error") else {}),
    }


@app.get("/api/iot/executive-summary")
def iot_executive_summary() -> dict[str, Any]:
    snapshot = _edge_snapshot()
    leituras = snapshot.get("readings", [])
    if not leituras:
        return {
            "status": snapshot["status"],
            "module": snapshot["module"],
            "source": snapshot["source"],
            "disclaimer": snapshot["disclaimer"],
            "summary": {},
            "readings": [],
            "alerts": snapshot.get("alerts", []),
            **({"note": snapshot["note"]} if snapshot.get("note") else {}),
            **({"error": snapshot["error"]} if snapshot.get("error") else {}),
        }

    df = pd.DataFrame(leituras)
    perdas_pct = float(((100.0 - df["conservation_index"]).clip(lower=0).mean()) / 100.0)
    score_esg = max(0.0, min(100.0, 84.0 - perdas_pct * 100.0 * 0.9 + (df["premium_quality_score"].mean() - 60.0) * 0.25))
    summary = {
        "farms": int(len(df)),
        "sensor_status_ok": int((df["premium_quality_score"] >= 65).sum()),
        "high_logistics_priority": int((df["collection_priority"] == "ALTA").sum()),
        "critical_thermal_risk": int((df["thermal_stress_risk"] == "CRITICO").sum()),
        "premium_score_avg": round(float(df["premium_quality_score"].mean()), 1),
        "thermal_stability_avg": round(float(df["thermal_stability_score"].mean()), 1),
        "conservation_index_avg": round(float(df["conservation_index"].mean()), 1),
        "operational_risk_avg": round(float(df["operational_risk_score"].mean()), 1),
        "esg_score": round(score_esg, 1),
        "loss_reduction_opportunity_liters": round(float((100.0 - df["conservation_index"]).clip(lower=0).sum() * 3.2), 1),
    }
    return {
        "status": snapshot["status"],
        "module": snapshot["module"],
        "source": snapshot["source"],
        "disclaimer": snapshot["disclaimer"],
        "summary": summary,
        "readings": leituras,
        "alerts": snapshot.get("alerts", []),
        **({"note": snapshot["note"]} if snapshot.get("note") else {}),
        **({"error": snapshot["error"]} if snapshot.get("error") else {}),
    }
