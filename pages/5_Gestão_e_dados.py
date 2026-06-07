from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard_common import artefatos_dir, carregar_dados, data_dir, formatar_numero_br, render_sidebar_filtros
from gestor_store import (
    carregar_fornecedores,
    carregar_lancamentos_gerenciais,
    db_path,
    init_db,
    salvar_fornecedor,
    salvar_lancamento_gerencial,
)


def formatar_df_brasileiro(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_float_dtype(out[col]) or pd.api.types.is_integer_dtype(out[col]):
            out[col] = out[col].map(lambda x: formatar_numero_br(x, 2) if pd.notna(x) else "")
    return out


st.title("Gestao, Fazendas e Dados")
st.caption(
    "Cadastro de fazendas, variaveis estrategicas e lancamentos gerenciais para apoiar monitoramento, rastreabilidade e cadeia leiteira premium."
)

init_db(data_dir())

try:
    pred, _, _, _, _, _, _ = carregar_dados(artefatos_dir(), data_dir())
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

render_sidebar_filtros(pred)
laticinios_opts = sorted(pred["id_laticinio"].dropna().unique().tolist())
fornecedores_base_opts = sorted(pred["id_produtor"].dropna().astype(int).unique().tolist())
polos_opts = sorted(pred["polo_climatico"].dropna().unique().tolist())

tab_fornecedores, tab_lancamentos = st.tabs(["Cadastro de Fornecedores", "Lançamentos Gerenciais Dinâmicos"])

with tab_fornecedores:
    st.markdown("### Cadastro de fornecedores")
    st.caption(
        "Use este formulário para registrar dados cadastrais, produtivos, operacionais, logísticos e financeiros. "
        "Essas informações são persistidas no DuckDB e passam a compor a base analítica do MVP."
    )

    df_fornecedores = carregar_fornecedores()
    fornecedores_existentes = df_fornecedores["id_fornecedor"].astype(str).tolist() if not df_fornecedores.empty else []
    modo = st.radio("Modo de cadastro", ["Novo fornecedor", "Editar fornecedor existente"], horizontal=True)

    selecionado = ""
    dados_atuais = {}
    if modo == "Editar fornecedor existente" and fornecedores_existentes:
        selecionado = st.selectbox("Fornecedor cadastrado", fornecedores_existentes)
        dados_atuais = df_fornecedores[df_fornecedores["id_fornecedor"].astype(str) == selecionado].iloc[0].to_dict()
    elif modo == "Editar fornecedor existente":
        st.info("Ainda não há fornecedores cadastrados para edição.")

    with st.form("form_fornecedor", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        id_sugerido = str(dados_atuais.get("id_fornecedor", "")) if dados_atuais else ""
        id_fornecedor = c1.text_input(
            "Identificação do fornecedor",
            value=id_sugerido,
            placeholder="Ex.: 1024 ou CNPJ interno",
            help="Deixe em branco para gerar o próximo identificador numérico disponível.",
        )
        nome = c2.text_input(
            "Nome ou razão social",
            value=str(dados_atuais.get("nome_razao_social", "")),
            placeholder="Ex.: Fazenda Limoeiro",
        )
        cpf_cnpj = c3.text_input(
            "CPF ou CNPJ",
            value=str(dados_atuais.get("cpf_cnpj", "") if pd.notna(dados_atuais.get("cpf_cnpj", "")) else ""),
            placeholder="Somente números ou formato oficial",
        )

        c4, c5, c6 = st.columns(3)
        polo = c4.selectbox(
            "Localização ou polo",
            options=[""] + polos_opts,
            index=([""] + polos_opts).index(dados_atuais.get("polo_localizacao", ""))
            if dados_atuais.get("polo_localizacao", "") in polos_opts
            else 0,
        )
        capacidade = c5.number_input(
            "Capacidade produtiva ou de tanque (L)",
            min_value=0.0,
            value=float(dados_atuais.get("capacidade_tanque_litros") or 0),
            step=50.0,
            format="%.2f",
        )
        historico = c6.number_input(
            "Histórico de fornecimento (meses)",
            min_value=0.0,
            value=float(dados_atuais.get("historico_fornecimento_meses") or 0),
            step=1.0,
            format="%.2f",
        )

        c7, c8, c9 = st.columns(3)
        data_inicio = c7.date_input(
            "Início da parceria",
            value=pd.to_datetime(dados_atuais.get("data_inicio_parceria") or pd.Timestamp.now()).date(),
        )
        status = c8.checkbox("Fornecedor ativo", value=bool(dados_atuais.get("status_ativo", True)))
        score = c9.number_input(
            "Score inicial de qualidade",
            min_value=0.0,
            max_value=100.0,
            value=float(dados_atuais.get("score_qualidade_inicial") or 0),
            step=1.0,
            format="%.2f",
        )

        indicadores = st.text_area(
            "Indicadores de qualidade",
            value=str(dados_atuais.get("indicadores_qualidade", "")),
            placeholder="Ex.: CCS média, CBT média, histórico de conformidade, auditorias e certificações.",
        )
        c10, c11, c12 = st.columns(3)
        operacionais = c10.text_area(
            "Variáveis operacionais",
            value=str(dados_atuais.get("variaveis_operacionais", "")),
            placeholder="Ex.: tipo de ordenha, refrigeração, frequência de coleta.",
        )
        logisticas = c11.text_area(
            "Variáveis logísticas",
            value=str(dados_atuais.get("variaveis_logisticas", "")),
            placeholder="Ex.: distância, acesso, restrições de rota, custo por km.",
        )
        financeiras = c12.text_area(
            "Variáveis financeiras",
            value=str(dados_atuais.get("variaveis_financeiras", "")),
            placeholder="Ex.: preço negociado, adiantamentos, penalidades e bonificações.",
        )

        salvar = st.form_submit_button("Salvar fornecedor")

    if salvar:
        if not nome.strip():
            st.warning("Informe o nome ou a razão social do fornecedor.")
        else:
            fornecedor_salvo = salvar_fornecedor(
                {
                    "id_fornecedor": id_fornecedor,
                    "nome_razao_social": nome,
                    "cpf_cnpj": cpf_cnpj,
                    "polo_localizacao": polo,
                    "capacidade_tanque_litros": capacidade,
                    "historico_fornecimento_meses": historico,
                    "indicadores_qualidade": indicadores,
                    "variaveis_operacionais": operacionais,
                    "variaveis_logisticas": logisticas,
                    "variaveis_financeiras": financeiras,
                    "data_inicio_parceria": data_inicio,
                    "status_ativo": status,
                    "score_qualidade_inicial": score,
                }
            )
            st.success(f"Fornecedor {fornecedor_salvo} salvo com sucesso.")
            st.rerun()

    st.divider()
    st.markdown("### Fornecedores cadastrados")
    df_fornecedores = carregar_fornecedores()
    if df_fornecedores.empty:
        st.info("Nenhum fornecedor cadastrado até o momento.")
    else:
        cols = [
            "id_fornecedor",
            "nome_razao_social",
            "cpf_cnpj",
            "polo_localizacao",
            "capacidade_tanque_litros",
            "historico_fornecimento_meses",
            "score_qualidade_inicial",
            "status_ativo",
            "atualizado_em",
        ]
        st.dataframe(formatar_df_brasileiro(df_fornecedores[cols]), use_container_width=True, hide_index=True)

with tab_lancamentos:
    st.markdown("### Lançamentos gerenciais dinâmicos")
    st.caption(
        "Registre eventos que afetam a captação, como custos extras, interrupções, penalidades, bonificações, "
        "restrições logísticas ou ajustes operacionais. O impacto deve ser informado em litros equivalentes."
    )

    fornecedores_cadastrados = carregar_fornecedores()["id_fornecedor"].astype(str).tolist()
    fornecedor_opts = ["Aplicar ao laticínio inteiro"] + fornecedores_cadastrados + [str(x) for x in fornecedores_base_opts]
    fornecedor_opts = list(dict.fromkeys(fornecedor_opts))

    with st.form("form_lancamento_gerencial", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        data_ref = c1.date_input("Data de referência", value=pd.Timestamp.now().date())
        id_laticinio = c2.selectbox("Laticínio", options=laticinios_opts, format_func=lambda x: f"Laticínio {x}")
        fornecedor_escolhido = c3.selectbox("Escopo do lançamento", options=fornecedor_opts)

        c4, c5, c6 = st.columns(3)
        categoria = c4.selectbox(
            "Categoria do evento",
            options=[
                "Custo extra",
                "Interrupção operacional",
                "Penalidade de qualidade",
                "Bonificação",
                "Restrição logística",
                "Ajuste financeiro",
                "Outro evento gerencial",
            ],
        )
        impacto = c5.number_input(
            "Impacto gerencial (L)",
            value=0.0,
            step=100.0,
            format="%.2f",
            help="Use valores negativos para perdas ou penalidades e positivos para ganhos ou bonificações.",
        )
        registrado_por = c6.text_input("Registrado por", value="Gestor")

        descricao = st.text_area(
            "Descrição detalhada",
            placeholder="Ex.: interrupção de 4 horas na rota norte, com perda estimada de 1.250,50 L.",
        )
        salvar_evento = st.form_submit_button("Salvar lançamento gerencial")

    if salvar_evento:
        if not categoria.strip():
            st.warning("Informe a categoria do evento.")
        else:
            id_fornecedor = None if fornecedor_escolhido == "Aplicar ao laticínio inteiro" else fornecedor_escolhido
            id_lancamento = salvar_lancamento_gerencial(
                {
                    "data_referencia": data_ref,
                    "id_fornecedor": id_fornecedor,
                    "id_laticinio": id_laticinio,
                    "categoria_evento": categoria,
                    "valor_impacto": impacto,
                    "descricao_detalhada": descricao,
                    "registrado_por": registrado_por,
                }
            )
            st.success(f"Lançamento {id_lancamento} salvo com sucesso.")
            st.rerun()

    st.divider()
    st.markdown("### Histórico de lançamentos")
    lancamentos = carregar_lancamentos_gerenciais()
    if lancamentos.empty:
        st.info("Nenhum lançamento gerencial registrado até o momento.")
    else:
        st.dataframe(formatar_df_brasileiro(lancamentos), use_container_width=True, hide_index=True)

st.caption(f"Banco local DuckDB: `{db_path().resolve()}`")
