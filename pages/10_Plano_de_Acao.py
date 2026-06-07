"""
pages/10_Plano_de_Acao.py — Plano de Ação por Produtor

Permite criar, acompanhar e fechar planos de melhoria por produtor,
com responsável, prazo, status e evidências. Persistido em DuckDB.
"""
from __future__ import annotations

import uuid
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from auth import requer_autenticacao, renderizar_sidebar_usuario
from dashboard_common import aplicar_layout_plotly, artefatos_dir, carregar_dados, data_dir
from fornecedor_inteligencia import calcular_scores_fornecedores
from gestor_store import conectar, garantir_pasta, init_db

requer_autenticacao()
renderizar_sidebar_usuario()

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.vl-pa-header {
    background: linear-gradient(90deg,rgba(74,144,226,0.2),rgba(4,120,87,0.1));
    border-left: 4px solid #4A90E2;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.2rem;
}
.vl-pa-title { color:#F0FFF4; font-size:1.2rem; font-weight:700; margin:0; }
.vl-pa-sub   { color:#93C5FD; font-size:0.85rem; margin:0.2rem 0 0; }

.vl-status-aberto    { background:#1e3a5f; color:#93C5FD;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-em_curso  { background:#78350f; color:#FCD34D;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-concluido { background:#065f46; color:#6EE7B7;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
.vl-status-cancelado { background:#1f2937; color:#9CA3AF;  padding:0.15rem 0.6rem; border-radius:10px; font-size:0.78rem; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Persistência — tabela planos_acao no DuckDB
# ---------------------------------------------------------------------------
PLANOS_COLS = [
    "id_plano", "id_produtor", "nome_fazenda", "polo",
    "dimensao", "descricao_acao", "responsavel",
    "prazo", "status", "evidencia", "criado_em", "atualizado_em",
]

DIMENSOES   = ["Qualidade", "Volume", "Logística", "Continuidade", "Operacional", "Relacionamento"]
STATUS_OPTS = ["Aberto", "Em curso", "Concluído", "Cancelado"]


def _init_planos() -> None:
    garantir_pasta()
    with conectar() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS planos_acao (
                id_plano      VARCHAR PRIMARY KEY,
                id_produtor   VARCHAR,
                nome_fazenda  VARCHAR,
                polo          VARCHAR,
                dimensao      VARCHAR,
                descricao_acao VARCHAR,
                responsavel   VARCHAR,
                prazo         DATE,
                status        VARCHAR DEFAULT 'Aberto',
                evidencia     VARCHAR,
                criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def _salvar_plano(dados: dict) -> str:
    _init_planos()
    if not dados.get("id_plano"):
        dados["id_plano"] = str(uuid.uuid4())[:8].upper()
    with conectar() as con:
        existing = con.execute(
            "SELECT id_plano FROM planos_acao WHERE id_plano = ?",
            [dados["id_plano"]]
        ).fetchone()
        if existing:
            con.execute("""
                UPDATE planos_acao SET
                    dimensao=?, descricao_acao=?, responsavel=?,
                    prazo=?, status=?, evidencia=?,
                    atualizado_em=CURRENT_TIMESTAMP
                WHERE id_plano=?
            """, [
                dados["dimensao"], dados["descricao_acao"], dados["responsavel"],
                dados["prazo"], dados["status"], dados.get("evidencia",""),
                dados["id_plano"],
            ])
        else:
            con.execute("""
                INSERT INTO planos_acao
                (id_plano,id_produtor,nome_fazenda,polo,dimensao,
                 descricao_acao,responsavel,prazo,status,evidencia)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, [
                dados["id_plano"], dados.get("id_produtor",""),
                dados.get("nome_fazenda",""), dados.get("polo",""),
                dados["dimensao"], dados["descricao_acao"],
                dados["responsavel"], dados["prazo"],
                dados.get("status","Aberto"), dados.get("evidencia",""),
            ])
    return dados["id_plano"]


def _carregar_planos(id_produtor: str | None = None) -> pd.DataFrame:
    _init_planos()
    with conectar(read_only=True) as con:
        query = "SELECT * FROM planos_acao"
        params: list = []
        if id_produtor:
            query += " WHERE id_produtor = ?"
            params.append(str(id_produtor))
        query += " ORDER BY criado_em DESC"
        try:
            df = con.execute(query, params).df()
        except Exception:
            df = pd.DataFrame(columns=PLANOS_COLS)
    return df


def _excluir_plano(id_plano: str) -> None:
    with conectar() as con:
        con.execute("DELETE FROM planos_acao WHERE id_plano = ?", [id_plano])


# ---------------------------------------------------------------------------
# Dados do modelo (para lista de produtores e scores)
# ---------------------------------------------------------------------------
init_db(data_dir())

try:
    pred, _, _, prod, dim_prod, _, _ = carregar_dados(artefatos_dir(), data_dir())
    scores_df = calcular_scores_fornecedores(prod, dim_prod, pred)
    tem_dados = True
except Exception:
    scores_df = pd.DataFrame()
    tem_dados = False

# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
st.markdown("## 📋 Plano de Ação por Produtor")
st.caption("Crie, acompanhe e encerre planos de melhoria para cada fazenda da cadeia.")

tab_novo, tab_acompanhar, tab_painel = st.tabs(["➕ Novo Plano", "📌 Acompanhar Planos", "📊 Painel Geral"])

# ============================================================
# NOVO PLANO
# ============================================================
with tab_novo:
    st.markdown("""
    <div class="vl-pa-header">
        <p class="vl-pa-title">Criar plano de ação</p>
        <p class="vl-pa-sub">Registre a ação, o responsável, o prazo e a dimensão de risco</p>
    </div>""", unsafe_allow_html=True)

    # Seleção de produtor
    if tem_dados and not scores_df.empty:
        produtores_opts = scores_df[["id_produtor","municipio","classe_risco"]].copy()
        produtores_opts["label"] = produtores_opts.apply(
            lambda r: f"#{r['id_produtor']} — {r['municipio']} [{r['classe_risco']}]", axis=1
        )
        prod_selecionado = st.selectbox(
            "Produtor / Fazenda",
            produtores_opts["label"].tolist(),
            help="Produtores ordenados por score de risco do modelo."
        )
        idx = produtores_opts["label"].tolist().index(prod_selecionado)
        id_prod_sel = str(produtores_opts.iloc[idx]["id_produtor"])
        polo_sel    = str(scores_df.loc[scores_df["id_produtor"].astype(str) == id_prod_sel, "polo_climatico"].values[0]) \
                      if "polo_climatico" in scores_df.columns else "—"
    else:
        id_prod_sel = st.text_input("ID do Produtor", placeholder="Ex.: 42")
        polo_sel    = st.text_input("Polo / Localização", placeholder="Ex.: RIO_VERDE")

    c1, c2, c3 = st.columns(3)
    nome_fazenda = c1.text_input("Nome da fazenda", placeholder="Ex.: Fazenda São João")
    dimensao     = c2.selectbox("Dimensão do plano", DIMENSOES)
    responsavel  = c3.text_input("Responsável", placeholder="Ex.: Técnico de campo")

    c4, c5 = st.columns(2)
    prazo  = c4.date_input("Prazo", value=date.today() + timedelta(days=15))
    status = c5.selectbox("Status inicial", STATUS_OPTS, index=0)

    descricao = st.text_area(
        "Descrição da ação *",
        placeholder="Ex.: Realizar visita técnica para avaliar higiene de ordenha e protocolo de limpeza do tanque. "
                    "Coletar amostra para análise de CCS e CBT no laboratório parceiro.",
        height=110,
    )
    evidencia = st.text_input(
        "Evidência / Observação (opcional)",
        placeholder="Ex.: Relatório de visita, foto do tanque, laudo laboratorial."
    )

    if st.button("Salvar plano de ação", type="primary", use_container_width=True, key="btn_salvar_plano"):
        if not descricao.strip():
            st.warning("Descreva a ação a ser realizada.")
        else:
            id_plano = _salvar_plano({
                "id_produtor": id_prod_sel,
                "nome_fazenda": nome_fazenda,
                "polo": polo_sel,
                "dimensao": dimensao,
                "descricao_acao": descricao,
                "responsavel": responsavel,
                "prazo": prazo,
                "status": status,
                "evidencia": evidencia,
            })
            st.success(f"✅ Plano **{id_plano}** criado com sucesso!")
            st.rerun()


# ============================================================
# ACOMPANHAR PLANOS
# ============================================================
with tab_acompanhar:
    st.markdown("""
    <div class="vl-pa-header">
        <p class="vl-pa-title">Acompanhamento de planos</p>
        <p class="vl-pa-sub">Atualize status, registre evidências e encerre ações concluídas</p>
    </div>""", unsafe_allow_html=True)

    df_planos = _carregar_planos()

    if df_planos.empty:
        st.info("Nenhum plano cadastrado ainda. Crie o primeiro na aba **Novo Plano**.")
    else:
        # Filtros
        fc1, fc2, fc3 = st.columns(3)
        f_status = fc1.multiselect("Status", STATUS_OPTS, default=["Aberto","Em curso"])
        f_dim    = fc2.multiselect("Dimensão", DIMENSOES, default=DIMENSOES)
        f_prod   = fc3.text_input("Buscar por produtor / fazenda", placeholder="ID ou nome")

        filtrado = df_planos.copy()
        if f_status:
            filtrado = filtrado[filtrado["status"].isin(f_status)]
        if f_dim:
            filtrado = filtrado[filtrado["dimensao"].isin(f_dim)]
        if f_prod.strip():
            mask = (
                filtrado["id_produtor"].astype(str).str.contains(f_prod, case=False, na=False) |
                filtrado["nome_fazenda"].astype(str).str.contains(f_prod, case=False, na=False)
            )
            filtrado = filtrado[mask]

        st.caption(f"{len(filtrado)} plano(s) encontrado(s)")

        for _, row in filtrado.iterrows():
            prazo_dt  = pd.to_datetime(row["prazo"]).date() if pd.notna(row["prazo"]) else None
            atrasado  = prazo_dt and prazo_dt < date.today() and row["status"] not in ("Concluído","Cancelado")
            prazo_str = f"{'⚠️ ' if atrasado else ''}{prazo_dt}" if prazo_dt else "—"
            status_css = row["status"].lower().replace(" ","_").replace("í","i").replace("ú","u")

            with st.expander(
                f"**{row['id_plano']}** · #{row['id_produtor']} {row['nome_fazenda'] or ''} "
                f"· {row['dimensao']} · {prazo_str}",
                expanded=False,
            ):
                st.markdown(f"<span class='vl-status-{status_css}'>{row['status']}</span>",
                            unsafe_allow_html=True)
                st.markdown(f"**Ação:** {row['descricao_acao']}")
                if row.get("evidencia"):
                    st.markdown(f"**Evidência:** {row['evidencia']}")
                st.caption(f"Responsável: {row['responsavel']} · Criado: {row['criado_em']}")

                with st.form(f"form_update_{row['id_plano']}", clear_on_submit=False):
                    uc1, uc2 = st.columns(2)
                    novo_status = uc1.selectbox(
                        "Atualizar status", STATUS_OPTS,
                        index=STATUS_OPTS.index(row["status"]),
                        key=f"st_{row['id_plano']}"
                    )
                    nova_evidencia = uc2.text_input(
                        "Evidência / atualização",
                        value=row.get("evidencia","") or "",
                        key=f"ev_{row['id_plano']}"
                    )
                    novo_resp = st.text_input(
                        "Responsável", value=row["responsavel"] or "",
                        key=f"rp_{row['id_plano']}"
                    )
                    col_save, col_del = st.columns([3,1])
                    salvar_upd = col_save.form_submit_button("💾 Salvar atualização", use_container_width=True)
                    excluir    = col_del.form_submit_button("🗑️ Excluir", use_container_width=True)

                if salvar_upd:
                    _salvar_plano({
                        "id_plano": row["id_plano"],
                        "id_produtor": row["id_produtor"],
                        "nome_fazenda": row["nome_fazenda"],
                        "polo": row.get("polo",""),
                        "dimensao": row["dimensao"],
                        "descricao_acao": row["descricao_acao"],
                        "responsavel": novo_resp,
                        "prazo": row["prazo"],
                        "status": novo_status,
                        "evidencia": nova_evidencia,
                    })
                    st.success("Plano atualizado!")
                    st.rerun()

                if excluir:
                    _excluir_plano(row["id_plano"])
                    st.warning("Plano excluído.")
                    st.rerun()


# ============================================================
# PAINEL GERAL
# ============================================================
with tab_painel:
    st.markdown("""
    <div class="vl-pa-header">
        <p class="vl-pa-title">Painel geral de planos</p>
        <p class="vl-pa-sub">Visão consolidada de todos os planos por status, dimensão e produtor</p>
    </div>""", unsafe_allow_html=True)

    df_todos = _carregar_planos()

    if df_todos.empty:
        st.info("Nenhum plano cadastrado ainda.")
    else:
        # KPIs
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total de planos", len(df_todos))
        k2.metric("Abertos",  len(df_todos[df_todos["status"]=="Aberto"]))
        k3.metric("Em curso", len(df_todos[df_todos["status"]=="Em curso"]))
        k4.metric("Concluídos", len(df_todos[df_todos["status"]=="Concluído"]))

        # Verificar atrasados
        df_todos["prazo_dt"] = pd.to_datetime(df_todos["prazo"], errors="coerce").dt.date
        atrasados = df_todos[
            (df_todos["prazo_dt"] < date.today()) &
            (~df_todos["status"].isin(["Concluído","Cancelado"]))
        ]
        if not atrasados.empty:
            st.warning(f"⚠️ **{len(atrasados)} plano(s) com prazo vencido** — verifique na aba Acompanhar.")

        st.divider()
        g1, g2 = st.columns(2)

        with g1:
            fig_s = px.pie(
                df_todos, names="status",
                title="Distribuição por status",
                color="status",
                color_discrete_map={
                    "Aberto":"#3B82F6","Em curso":"#F59E0B",
                    "Concluído":"#10B981","Cancelado":"#6B7280"
                },
            )
            aplicar_layout_plotly(fig_s)
            st.plotly_chart(fig_s, use_container_width=True)

        with g2:
            contagem_dim = df_todos.groupby("dimensao").size().reset_index(name="total")
            fig_d = px.bar(
                contagem_dim, x="dimensao", y="total",
                title="Planos por dimensão",
                color="total",
                color_continuous_scale=["#1e3a5f","#4ADE80"],
            )
            aplicar_layout_plotly(fig_d)
            st.plotly_chart(fig_d, use_container_width=True)

        st.subheader("Todos os planos")
        cols_exib = ["id_plano","id_produtor","nome_fazenda","dimensao",
                     "responsavel","prazo","status","criado_em"]
        cols_exib = [c for c in cols_exib if c in df_todos.columns]
        st.dataframe(
            df_todos[cols_exib],
            use_container_width=True,
            hide_index=True,
            column_config={
                "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTS),
                "prazo":  st.column_config.DateColumn("Prazo", format="DD/MM/YYYY"),
            }
        )

st.caption("VIA LEITE SENSE · Plano de Ação por Produtor · USINA I.A. Tecnologia e Inovação")
