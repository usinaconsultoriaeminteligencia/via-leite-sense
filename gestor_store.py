from __future__ import annotations

import io
import os
import uuid
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

DB_FILENAME = "via_leite.duckdb"

LANCAMENTOS_COLS = [
    "data",
    "id_laticinio",
    "nome_empresa",
    "litros_coletados",
    "litros_previstos",
    "litros_descartados",
    "observacao",
    "registado_em",
]

COLUNAS_CSV_OBRIGATORIAS = ["data", "id_laticinio", "litros_coletados"]

FORNECEDORES_COLS = [
    "id_fornecedor",
    "nome_razao_social",
    "cpf_cnpj",
    "polo_localizacao",
    "capacidade_tanque_litros",
    "historico_fornecimento_meses",
    "indicadores_qualidade",
    "variaveis_operacionais",
    "variaveis_logisticas",
    "variaveis_financeiras",
    "data_inicio_parceria",
    "status_ativo",
    "score_qualidade_inicial",
    "atualizado_em",
]

LEGACY_FORNECEDORES_COLS = [
    "id_fornecedor",
    "nome",
    "localizacao",
    "capacidade_produtiva",
    "historico_fornecimento",
    "indicadores_qualidade",
    "dados_operacionais",
    "dados_logisticos",
    "dados_financeiros",
    "atualizado_em",
]

LANCAMENTOS_GERENCIAIS_COLS = [
    "id_lancamento",
    "data_referencia",
    "id_fornecedor",
    "id_laticinio",
    "categoria_evento",
    "valor_impacto",
    "valor_financeiro",
    "descricao_detalhada",
    "data_registro",
    "registrado_por",
]

PLANOS_ACAO_COLS = [
    "id_plano",
    "id_fornecedor",
    "titulo",
    "descricao",
    "tipo_plano",
    "classe_risco",
    "responsavel",
    "prazo_dias",
    "litros_potenciais",
    "valor_potencial",
    "litros_resultado",
    "valor_resultado",
    "data_prevista",
    "observacoes",
    "evidencias",
    "status_plano",
    "origem_plano",
    "criado_em",
    "atualizado_em",
    "concluido_em",
]


def user_data_dir() -> Path:
    return Path(os.environ.get("MVP_USER_DATA_DIR", "dados_utilizador"))


def default_data_dir() -> Path:
    return Path(os.environ.get("MVP_DATA_DIR", "dados_teste"))


def db_path() -> Path:
    return user_data_dir() / DB_FILENAME


def lancamentos_path() -> Path:
    return user_data_dir() / "lancamentos_laticinio.csv"


def fornecedores_path() -> Path:
    return user_data_dir() / "fornecedores_cadastrais.csv"


def garantir_pasta() -> None:
    user_data_dir().mkdir(parents=True, exist_ok=True)


def _sql_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", "''")


def conectar(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    garantir_pasta()
    con = duckdb.connect(str(db_path()), read_only=read_only)
    return con


def _csv_view_sql(view_name: str, csv_path: Path) -> str:
    if csv_path.exists():
        return f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT * FROM read_csv_auto('{_sql_path(csv_path)}', header = true);
        """
    return f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM (SELECT 1 WHERE false);"


def init_db(data_dir: Path | str | None = None) -> Path:
    data_dir = Path(data_dir) if data_dir is not None else default_data_dir()
    clima_inmet = Path("dados_inmet_processado") / "fact_clima_diario_inmet.csv"
    clima_padrao = data_dir / "fact_clima_diario.csv"
    clima_path = clima_inmet if clima_inmet.exists() else clima_padrao

    with conectar() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS dim_fornecedor (
                id_fornecedor VARCHAR PRIMARY KEY,
                nome_razao_social VARCHAR,
                cpf_cnpj VARCHAR UNIQUE,
                polo_localizacao VARCHAR,
                capacidade_tanque_litros DECIMAL(18, 2),
                historico_fornecimento_meses DECIMAL(18, 2),
                indicadores_qualidade TEXT,
                variaveis_operacionais TEXT,
                variaveis_logisticas TEXT,
                variaveis_financeiras TEXT,
                data_inicio_parceria DATE,
                status_ativo BOOLEAN,
                score_qualidade_inicial DECIMAL(6, 2),
                atualizado_em TIMESTAMP
            );
            """
        )
        for ddl in [
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS historico_fornecimento_meses DECIMAL(18, 2);",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS indicadores_qualidade TEXT;",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS variaveis_operacionais TEXT;",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS variaveis_logisticas TEXT;",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS variaveis_financeiras TEXT;",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS status_ativo BOOLEAN;",
            "ALTER TABLE dim_fornecedor ADD COLUMN IF NOT EXISTS atualizado_em TIMESTAMP;",
        ]:
            con.execute(ddl)
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS fact_lancamento_gerencial (
                id_lancamento UUID PRIMARY KEY,
                data_referencia DATE,
                id_fornecedor VARCHAR,
                id_laticinio VARCHAR,
                categoria_evento VARCHAR,
                valor_impacto DECIMAL(18, 2),
                valor_financeiro DECIMAL(18, 2),
                descricao_detalhada TEXT,
                data_registro TIMESTAMP,
                registrado_por VARCHAR,
                FOREIGN KEY (id_fornecedor) REFERENCES dim_fornecedor(id_fornecedor)
            );
            """
        )
        con.execute("ALTER TABLE fact_lancamento_gerencial ADD COLUMN IF NOT EXISTS valor_financeiro DECIMAL(18, 2);")
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS fact_plano_acao (
                id_plano UUID PRIMARY KEY,
                id_fornecedor VARCHAR,
                titulo VARCHAR,
                descricao TEXT,
                tipo_plano VARCHAR,
                classe_risco VARCHAR,
                responsavel VARCHAR,
                prazo_dias INTEGER,
                litros_potenciais DECIMAL(18, 2),
                valor_potencial DECIMAL(18, 2),
                litros_resultado DECIMAL(18, 2),
                valor_resultado DECIMAL(18, 2),
                data_prevista DATE,
                observacoes TEXT,
                evidencias TEXT,
                status_plano VARCHAR,
                origem_plano VARCHAR,
                criado_em TIMESTAMP,
                atualizado_em TIMESTAMP,
                concluido_em TIMESTAMP,
                FOREIGN KEY (id_fornecedor) REFERENCES dim_fornecedor(id_fornecedor)
            );
            """
        )
        for ddl in [
            "ALTER TABLE fact_plano_acao ADD COLUMN IF NOT EXISTS data_prevista DATE;",
            "ALTER TABLE fact_plano_acao ADD COLUMN IF NOT EXISTS litros_resultado DECIMAL(18, 2);",
            "ALTER TABLE fact_plano_acao ADD COLUMN IF NOT EXISTS valor_resultado DECIMAL(18, 2);",
            "ALTER TABLE fact_plano_acao ADD COLUMN IF NOT EXISTS observacoes TEXT;",
            "ALTER TABLE fact_plano_acao ADD COLUMN IF NOT EXISTS evidencias TEXT;",
        ]:
            con.execute(ddl)
        con.execute(_csv_view_sql("fact_producao", data_dir / "fact_producao_produtor_dia.csv"))
        con.execute(_csv_view_sql("fact_clima_diario_inmet", clima_path))
        con.execute(
            """
            CREATE OR REPLACE VIEW vw_base_treino_via_leite AS
            WITH gerencial_fornecedor AS (
                SELECT
                    data_referencia,
                    id_laticinio,
                    id_fornecedor,
                    SUM(valor_impacto) AS impacto_gerencial_litros,
                    SUM(COALESCE(valor_financeiro, 0)) AS impacto_gerencial_financeiro,
                    COUNT(*) AS qtd_eventos_gerenciais
                FROM fact_lancamento_gerencial
                WHERE COALESCE(id_fornecedor, '') <> ''
                GROUP BY 1, 2, 3
            ),
            gerencial_laticinio AS (
                SELECT
                    data_referencia,
                    id_laticinio,
                    SUM(valor_impacto) AS impacto_laticinio_litros,
                    SUM(COALESCE(valor_financeiro, 0)) AS impacto_laticinio_financeiro,
                    COUNT(*) AS qtd_eventos_laticinio
                FROM fact_lancamento_gerencial
                WHERE COALESCE(id_fornecedor, '') = ''
                GROUP BY 1, 2
            )
            SELECT
                p.*,
                df.nome_razao_social AS fornecedor_nome_razao_social,
                df.cpf_cnpj AS fornecedor_cpf_cnpj,
                df.polo_localizacao AS fornecedor_polo_localizacao,
                df.capacidade_tanque_litros AS fornecedor_capacidade_tanque_litros,
                df.historico_fornecimento_meses AS fornecedor_historico_fornecimento_meses,
                df.indicadores_qualidade AS fornecedor_indicadores_qualidade,
                df.variaveis_operacionais AS fornecedor_variaveis_operacionais,
                df.variaveis_logisticas AS fornecedor_variaveis_logisticas,
                df.variaveis_financeiras AS fornecedor_variaveis_financeiras,
                df.data_inicio_parceria AS fornecedor_data_inicio_parceria,
                df.status_ativo AS fornecedor_status_ativo,
                df.score_qualidade_inicial AS score_qualidade_inicial,
                c.temp_min_c,
                c.temp_max_c,
                c.temp_med_c,
                c.umidade_med_pct,
                c.precip_mm,
                c.vento_med_ms,
                c.radiacao_proxy,
                c.precip_3d,
                c.precip_7d,
                c.precip_15d,
                c.dias_sem_chuva,
                c.thi,
                c.thi_3d_avg,
                c.onda_calor_3d,
                c.onda_calor_5d,
                c.dry_spell_10d,
                c.anomalia_temp,
                c.indice_favorabilidade_pastagem,
                COALESCE(gf.impacto_gerencial_litros, 0) + COALESCE(gl.impacto_laticinio_litros, 0) AS impacto_gerencial_litros,
                COALESCE(gf.impacto_gerencial_financeiro, 0) + COALESCE(gl.impacto_laticinio_financeiro, 0) AS impacto_gerencial_financeiro,
                COALESCE(gf.qtd_eventos_gerenciais, 0) + COALESCE(gl.qtd_eventos_laticinio, 0) AS qtd_eventos_gerenciais
            FROM fact_producao p
            LEFT JOIN dim_fornecedor df
                ON df.id_fornecedor = CAST(p.id_produtor AS VARCHAR)
            LEFT JOIN fact_clima_diario_inmet c
                ON CAST(c.data AS DATE) = CAST(p.data AS DATE)
                AND c.polo_climatico = p.polo_climatico
            LEFT JOIN gerencial_fornecedor gf
                ON gf.data_referencia = CAST(p.data AS DATE)
                AND gf.id_laticinio = CAST(p.id_laticinio AS VARCHAR)
                AND gf.id_fornecedor = CAST(p.id_produtor AS VARCHAR)
            LEFT JOIN gerencial_laticinio gl
                ON gl.data_referencia = CAST(p.data AS DATE)
                AND gl.id_laticinio = CAST(p.id_laticinio AS VARCHAR);
            """
        )
    return db_path()


def _normalizar_cpf_cnpj(valor: Any) -> str | None:
    if valor is None or pd.isna(valor):
        return None
    texto = str(valor).strip()
    return texto or None


def _proximo_id_fornecedor(con: duckdb.DuckDBPyConnection) -> str:
    atual = con.execute(
        """
        SELECT MAX(TRY_CAST(id_fornecedor AS INTEGER))
        FROM dim_fornecedor
        WHERE TRY_CAST(id_fornecedor AS INTEGER) IS NOT NULL;
        """
    ).fetchone()[0]
    return str(int(atual or 0) + 1)


def salvar_fornecedor(dados: dict) -> str:
    init_db()
    with conectar() as con:
        id_fornecedor = str(dados.get("id_fornecedor") or "").strip()
        if id_fornecedor in ("", "0"):
            id_fornecedor = _proximo_id_fornecedor(con)

        row = {
            "id_fornecedor": id_fornecedor,
            "nome_razao_social": (dados.get("nome_razao_social") or dados.get("nome") or "").strip(),
            "cpf_cnpj": _normalizar_cpf_cnpj(dados.get("cpf_cnpj")),
            "polo_localizacao": (dados.get("polo_localizacao") or dados.get("localizacao") or "").strip(),
            "capacidade_tanque_litros": float(
                dados.get("capacidade_tanque_litros") or dados.get("capacidade_produtiva") or 0
            ),
            "historico_fornecimento_meses": float(
                dados.get("historico_fornecimento_meses") or dados.get("historico_fornecimento") or 0
            ),
            "indicadores_qualidade": (dados.get("indicadores_qualidade") or "").strip(),
            "variaveis_operacionais": (dados.get("variaveis_operacionais") or dados.get("dados_operacionais") or "").strip(),
            "variaveis_logisticas": (dados.get("variaveis_logisticas") or dados.get("dados_logisticos") or "").strip(),
            "variaveis_financeiras": (dados.get("variaveis_financeiras") or dados.get("dados_financeiros") or "").strip(),
            "data_inicio_parceria": pd.to_datetime(
                dados.get("data_inicio_parceria") or pd.Timestamp.now().date()
            ).date(),
            "status_ativo": bool(dados.get("status_ativo", True)),
            "score_qualidade_inicial": float(dados.get("score_qualidade_inicial") or 0),
            "atualizado_em": pd.Timestamp.now(),
        }

        con.execute(
            """
            INSERT INTO dim_fornecedor (
                id_fornecedor, nome_razao_social, cpf_cnpj, polo_localizacao,
                capacidade_tanque_litros, historico_fornecimento_meses,
                indicadores_qualidade, variaveis_operacionais, variaveis_logisticas,
                variaveis_financeiras, data_inicio_parceria, status_ativo,
                score_qualidade_inicial, atualizado_em
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (id_fornecedor) DO UPDATE SET
                nome_razao_social = excluded.nome_razao_social,
                cpf_cnpj = excluded.cpf_cnpj,
                polo_localizacao = excluded.polo_localizacao,
                capacidade_tanque_litros = excluded.capacidade_tanque_litros,
                historico_fornecimento_meses = excluded.historico_fornecimento_meses,
                indicadores_qualidade = excluded.indicadores_qualidade,
                variaveis_operacionais = excluded.variaveis_operacionais,
                variaveis_logisticas = excluded.variaveis_logisticas,
                variaveis_financeiras = excluded.variaveis_financeiras,
                data_inicio_parceria = excluded.data_inicio_parceria,
                status_ativo = excluded.status_ativo,
                score_qualidade_inicial = excluded.score_qualidade_inicial,
                atualizado_em = excluded.atualizado_em;
            """,
            list(row.values()),
        )
    return id_fornecedor


def inativar_fornecedor(id_fornecedor: str) -> bool:
    init_db()
    with conectar() as con:
        result = con.execute(
            """
            UPDATE dim_fornecedor
            SET status_ativo = false, atualizado_em = ?
            WHERE id_fornecedor = ?;
            """,
            [pd.Timestamp.now(), str(id_fornecedor)],
        )
        return result.rowcount != 0


def carregar_fornecedores() -> pd.DataFrame:
    init_db()
    with conectar(read_only=True) as con:
        df = con.execute("SELECT * FROM dim_fornecedor ORDER BY id_fornecedor").fetchdf()
    for col in FORNECEDORES_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    if df.empty:
        return pd.DataFrame(columns=FORNECEDORES_COLS + LEGACY_FORNECEDORES_COLS[1:])

    df["nome"] = df["nome_razao_social"]
    df["localizacao"] = df["polo_localizacao"]
    df["capacidade_produtiva"] = df["capacidade_tanque_litros"]
    df["historico_fornecimento"] = df["historico_fornecimento_meses"]
    df["dados_operacionais"] = df["variaveis_operacionais"].fillna("")
    df["dados_logisticos"] = df["variaveis_logisticas"].fillna("")
    df["dados_financeiros"] = df["variaveis_financeiras"].fillna("")
    return df[FORNECEDORES_COLS + LEGACY_FORNECEDORES_COLS[1:]]


def carregar_fornecedores_dim() -> pd.DataFrame:
    init_db()
    with conectar(read_only=True) as con:
        return con.execute(
            """
            SELECT *
            FROM dim_fornecedor
            WHERE COALESCE(status_ativo, true)
            ORDER BY id_fornecedor;
            """
        ).fetchdf()


def salvar_lancamento_gerencial(dados: dict) -> str:
    init_db()
    id_lancamento = str(dados.get("id_lancamento") or uuid.uuid4())
    id_fornecedor = str(dados.get("id_fornecedor") or "").strip() or None
    id_laticinio = str(dados.get("id_laticinio") or "").strip()
    row = [
        id_lancamento,
        pd.to_datetime(dados.get("data_referencia")).date(),
        id_fornecedor,
        id_laticinio,
        (dados.get("categoria_evento") or "").strip(),
        float(dados.get("valor_impacto") or 0),
        float(dados.get("valor_financeiro") or 0),
        (dados.get("descricao_detalhada") or "").strip(),
        pd.Timestamp.now(),
        (dados.get("registrado_por") or "Gestor").strip(),
    ]
    with conectar() as con:
        con.execute(
            """
            INSERT INTO fact_lancamento_gerencial (
                id_lancamento, data_referencia, id_fornecedor, id_laticinio,
                categoria_evento, valor_impacto, valor_financeiro, descricao_detalhada,
                data_registro, registrado_por
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            row,
        )
    return id_lancamento


def carregar_lancamentos_gerenciais() -> pd.DataFrame:
    init_db()
    with conectar(read_only=True) as con:
        df = con.execute(
            """
            SELECT *
            FROM fact_lancamento_gerencial
            ORDER BY data_referencia DESC, data_registro DESC;
            """
        ).fetchdf()
    for col in LANCAMENTOS_GERENCIAIS_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[LANCAMENTOS_GERENCIAIS_COLS]


def salvar_plano_acao(dados: dict) -> str:
    init_db()
    id_plano_raw = dados.get("id_plano")
    try:
        id_plano = str(uuid.UUID(str(id_plano_raw))) if id_plano_raw else str(uuid.uuid4())
    except (ValueError, TypeError, AttributeError):
        id_plano = str(uuid.uuid5(uuid.NAMESPACE_URL, str(id_plano_raw)))
    concluido_em = dados.get("concluido_em")
    row = [
        id_plano,
        str(dados.get("id_fornecedor") or "").strip() or None,
        (dados.get("titulo") or "").strip(),
        (dados.get("descricao") or "").strip(),
        (dados.get("tipo_plano") or "").strip(),
        (dados.get("classe_risco") or "").strip(),
        (dados.get("responsavel") or "").strip(),
        int(dados.get("prazo_dias") or 0),
        float(dados.get("litros_potenciais") or 0),
        float(dados.get("valor_potencial") or 0),
        float(dados.get("litros_resultado") or 0),
        float(dados.get("valor_resultado") or 0),
        pd.to_datetime(dados.get("data_prevista")).date() if dados.get("data_prevista") else None,
        (dados.get("observacoes") or "").strip(),
        (dados.get("evidencias") or "").strip(),
        (dados.get("status_plano") or "Aberto").strip(),
        (dados.get("origem_plano") or "Manual").strip(),
        pd.to_datetime(dados.get("criado_em") or pd.Timestamp.now()),
        pd.to_datetime(dados.get("atualizado_em") or pd.Timestamp.now()),
        pd.to_datetime(concluido_em) if concluido_em else None,
    ]
    with conectar() as con:
        con.execute(
            """
            INSERT INTO fact_plano_acao (
                id_plano, id_fornecedor, titulo, descricao, tipo_plano, classe_risco,
                responsavel, prazo_dias, litros_potenciais, valor_potencial,
                litros_resultado, valor_resultado, data_prevista, observacoes, evidencias, status_plano, origem_plano,
                criado_em, atualizado_em, concluido_em
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (id_plano) DO UPDATE SET
                id_fornecedor = excluded.id_fornecedor,
                titulo = excluded.titulo,
                descricao = excluded.descricao,
                tipo_plano = excluded.tipo_plano,
                classe_risco = excluded.classe_risco,
                responsavel = excluded.responsavel,
                prazo_dias = excluded.prazo_dias,
                litros_potenciais = excluded.litros_potenciais,
                valor_potencial = excluded.valor_potencial,
                litros_resultado = excluded.litros_resultado,
                valor_resultado = excluded.valor_resultado,
                data_prevista = excluded.data_prevista,
                observacoes = excluded.observacoes,
                evidencias = excluded.evidencias,
                status_plano = excluded.status_plano,
                origem_plano = excluded.origem_plano,
                criado_em = excluded.criado_em,
                atualizado_em = excluded.atualizado_em,
                concluido_em = excluded.concluido_em;
            """,
            row,
        )
    return id_plano


def carregar_planos_acao() -> pd.DataFrame:
    init_db()
    with conectar(read_only=True) as con:
        df = con.execute(
            """
            SELECT *
            FROM fact_plano_acao
            ORDER BY
                CASE WHEN COALESCE(status_plano, 'Aberto') = 'Concluido' THEN 1 ELSE 0 END,
                atualizado_em DESC,
                criado_em DESC;
            """
        ).fetchdf()
    for col in PLANOS_ACAO_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    return df[PLANOS_ACAO_COLS]


def remover_plano_acao(id_plano: str) -> bool:
    init_db()
    with conectar() as con:
        result = con.execute("DELETE FROM fact_plano_acao WHERE id_plano = ?;", [str(id_plano)])
        return result.rowcount != 0


def carregar_base_treino_via_leite(data_dir: Path | str | None = None) -> pd.DataFrame:
    init_db(data_dir)
    with conectar(read_only=True) as con:
        df = con.execute("SELECT * FROM vw_base_treino_via_leite").fetchdf()
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df


def carregar_lancamentos() -> pd.DataFrame:
    gerenciais = carregar_lancamentos_gerenciais()
    if gerenciais.empty:
        return pd.DataFrame(columns=LANCAMENTOS_COLS)
    df = pd.DataFrame(
        {
            "data": pd.to_datetime(gerenciais["data_referencia"], errors="coerce"),
            "id_laticinio": pd.to_numeric(gerenciais["id_laticinio"], errors="coerce"),
            "nome_empresa": "",
            "litros_coletados": 0.0,
            "litros_previstos": 0.0,
            "litros_descartados": pd.to_numeric(gerenciais["valor_impacto"], errors="coerce").fillna(0),
            "observacao": gerenciais["descricao_detalhada"].fillna(""),
            "registado_em": pd.to_datetime(gerenciais["data_registro"], errors="coerce"),
        }
    )
    return df[LANCAMENTOS_COLS]


def guardar_dataframe_completo(df: pd.DataFrame) -> None:
    init_db()
    with conectar() as con:
        con.execute("DELETE FROM fact_lancamento_gerencial;")
    if not df.empty:
        acrescentar_linhas(df)


def acrescentar_linhas(novas: pd.DataFrame) -> tuple[int, str | None]:
    if novas.empty:
        return 0, None
    inseridas = 0
    for _, row in novas.iterrows():
        valor_impacto = float(row.get("litros_coletados", 0) or 0) - float(row.get("litros_previstos", 0) or 0)
        salvar_lancamento_gerencial(
            {
                "data_referencia": row.get("data"),
                "id_fornecedor": None,
                "id_laticinio": row.get("id_laticinio"),
                "categoria_evento": "Volume informado pelo gestor",
                "valor_impacto": valor_impacto,
                "descricao_detalhada": row.get("observacao", ""),
                "registrado_por": "Importação CSV",
            }
        )
        inseridas += 1
    return inseridas, None


def validar_frame_import(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    miss = [c for c in COLUNAS_CSV_OBRIGATORIAS if c not in df.columns]
    if miss:
        return None, f"Colunas em falta: {', '.join(miss)}"
    work = df.copy()
    work["data"] = pd.to_datetime(work["data"], errors="coerce")
    if work["data"].isna().any():
        return None, "Existem datas inválidas na coluna `data`."
    work["id_laticinio"] = pd.to_numeric(work["id_laticinio"], errors="coerce")
    if work["id_laticinio"].isna().any():
        return None, "Existem IDs de laticínio inválidos."
    work["id_laticinio"] = work["id_laticinio"].astype(int)
    work["litros_coletados"] = pd.to_numeric(work["litros_coletados"], errors="coerce")
    if work["litros_coletados"].isna().any() or (work["litros_coletados"] < 0).any():
        return None, "`litros_coletados` deve ser numérico e maior ou igual a zero."
    work["litros_previstos"] = pd.to_numeric(
        work.get("litros_previstos", work["litros_coletados"]), errors="coerce"
    ).fillna(work["litros_coletados"])
    work["litros_descartados"] = pd.to_numeric(work.get("litros_descartados", 0.0), errors="coerce").fillna(0)
    work["nome_empresa"] = work.get("nome_empresa", "").fillna("").astype(str)
    work["observacao"] = work.get("observacao", "").fillna("").astype(str)
    return work[LANCAMENTOS_COLS[:7]], None


def bytes_modelo_csv() -> bytes:
    buf = io.StringIO()
    pd.DataFrame(
        [
            {
                "data": "2025-06-01",
                "id_laticinio": 1,
                "nome_empresa": "Laticínio exemplo",
                "litros_coletados": 125000.50,
                "litros_previstos": 128000.00,
                "litros_descartados": 420.00,
                "observacao": "Turno único",
            }
        ]
    ).to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8-sig")


def guardar_fornecedores(df: pd.DataFrame) -> None:
    init_db()
    with conectar() as con:
        con.execute("DELETE FROM dim_fornecedor;")
    for _, row in df.iterrows():
        salvar_fornecedor(row.to_dict())
