"""
Vazamento entre produtores nas janelas móveis (mm_*/std_*).

As features de média móvel eram calculadas como
``group[col].shift(1).rolling(janela).mean()``. O ``shift(1)`` num
SeriesGroupBy devolve uma Series simples, sem agrupamento; o ``.rolling()``
seguinte corre sobre o DataFrame inteiro e, como ele está ordenado por
produtor e data, a janela do primeiro registro de um produtor é preenchida
com os últimos dias do produtor anterior.

O ``shift(1)`` continua obrigatório: a janela só pode olhar para dias
anteriores ao registro, nunca para o próprio dia.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from via_leite.models.treino_mvp_avancado import (
    HORIZONTE_DIAS,
    TARGET,
    adicionar_janelas_moveis,
    engenharia_de_atributos,
    split_temporal,
)

COLUNAS_JANELA = ["litros_coletados", "ccs", "cbt", "thi", "precip_mm"]


def _dois_produtores(n_dias: int, valor_1: float, valor_2: float, inicio: str = "2024-01-01") -> pd.DataFrame:
    """Dois produtores consecutivos, constantes e bem distintos, já ordenados por produtor e data."""
    datas = pd.date_range(inicio, periods=n_dias, freq="D")
    linhas = []
    for id_produtor, valor in ((1, valor_1), (2, valor_2)):
        for data in datas:
            linhas.append(
                {
                    "id_produtor": id_produtor,
                    "data": data,
                    "nome_ficticio": f"produtor_{id_produtor}",
                    "id_rota": 1,
                    "id_laticinio": 1,
                    "polo_climatico": "sul",
                    "litros_coletados": valor,
                    "litros_produzidos": valor * 1.1,
                    "ccs": valor,
                    "cbt": valor,
                    "thi": valor,
                    "precip_mm": valor,
                    "precip_15d": valor,
                    "dias_sem_chuva": 0,
                    "distancia_km_laticinio": 10.0,
                    "custo_logistico_rateado": 1.0,
                    "producao_media_esperada_litros_dia": valor,
                    "impacto_gerencial_litros": 0.0,
                    "qtd_eventos_gerenciais": 0,
                    "score_qualidade_inicial": 0.0,
                    "fornecedor_capacidade_tanque_litros": 5000,
                    "fornecedor_historico_fornecimento_meses": 12,
                    "fornecedor_status_ativo": True,
                }
            )
    return pd.DataFrame(linhas).sort_values(["id_produtor", "data"]).reset_index(drop=True)


ROTA = pd.DataFrame(
    {
        "id_rota": [1],
        "dificuldade_logistica": [1],
        "percentual_estrada_nao_pavimentada": [0.5],
        "capacidade_tanque_litros": [5000],
    }
)
DIM_PRODUTOR = pd.DataFrame({"id_produtor": [1, 2]})


def test_mm_3_do_primeiro_registro_do_segundo_produtor_nao_ve_o_primeiro():
    """
    Caso do achado: produtor 1 entrega 100 L/dia, produtor 2 entrega 1000 L/dia.

    No primeiro registro do produtor 2 não existe dia anterior DELE, logo
    ``mm_3_litros_coletados`` tem de ser NaN. Com o vazamento ela valia 100
    (os dois últimos dias do produtor 1) e, no segundo registro, 550
    (um dia do produtor 1 + um do produtor 2).
    """
    df = adicionar_janelas_moveis(_dois_produtores(n_dias=5, valor_1=100.0, valor_2=1000.0))
    produtor_2 = df[df["id_produtor"] == 2]

    primeiro = produtor_2.iloc[0]
    segundo = produtor_2.iloc[1]

    assert np.isnan(primeiro["mm_3_litros_coletados"]), (
        f"mm_3 do 1o registro do produtor 2 = {primeiro['mm_3_litros_coletados']}: veio do produtor 1"
    )
    assert segundo["mm_3_litros_coletados"] == 1000.0
    # std com min_periods=2: no 2o registro so ha 1 dia anterior do produtor 2
    assert np.isnan(primeiro["std_3_litros_coletados"])
    assert np.isnan(segundo["std_3_litros_coletados"])


def test_nenhuma_janela_atravessa_produtores():
    """Para toda coluna e toda janela, só valores do próprio produtor entram na média."""
    df = adicionar_janelas_moveis(_dois_produtores(n_dias=40, valor_1=100.0, valor_2=1000.0))
    produtor_2 = df[df["id_produtor"] == 2]
    produtor_1 = df[df["id_produtor"] == 1]

    for janela in [3, 7, 14, 30]:
        for col in COLUNAS_JANELA:
            sufixo = "precip" if col == "precip_mm" else col
            nome = f"mm_{janela}_{sufixo}"
            assert np.isnan(produtor_2[nome].iloc[0]), f"{nome} vazou no 1o registro do produtor 2"
            assert (produtor_2[nome].iloc[1:] == 1000.0).all(), f"{nome} misturou produtor 1 no produtor 2"
            assert (produtor_1[nome].iloc[1:] == 100.0).all(), nome
        assert produtor_2[f"std_{janela}_litros_coletados"].iloc[2:].eq(0.0).all()


def test_shift_1_continua_a_excluir_o_proprio_dia():
    """A janela só olha para trás: o valor do dia não entra na própria média."""
    base = _dois_produtores(n_dias=4, valor_1=0.0, valor_2=0.0)
    base.loc[base["id_produtor"] == 1, "litros_coletados"] = [10.0, 20.0, 30.0, 40.0]
    df = adicionar_janelas_moveis(base)
    produtor_1 = df[df["id_produtor"] == 1]["mm_3_litros_coletados"].tolist()
    assert np.isnan(produtor_1[0])
    assert produtor_1[1:] == [10.0, 15.0, 20.0]


def test_engenharia_de_atributos_ponta_a_ponta_nao_vaza_na_janela_30():
    """
    Pela função completa: o filtro ``lag_28`` descarta os 28 primeiros dias de
    cada produtor, mas a janela de 30 do 29.º dia ainda alcançava o último dia
    do produtor anterior. Esse é o único registro por produtor que o vazamento
    ainda tocava no treino real (mm_30, std_30, tendencia_7_30 e o baseline).
    """
    base = _dois_produtores(n_dias=60, valor_1=100.0, valor_2=1000.0)
    df = engenharia_de_atributos(base, DIM_PRODUTOR, ROTA)
    produtor_2 = df[df["id_produtor"] == 2]
    assert len(produtor_2) > 0

    assert (produtor_2["mm_30_litros_coletados"] == 1000.0).all()
    assert produtor_2["std_30_litros_coletados"].eq(0.0).all()
    assert (produtor_2["tendencia_7_30_litros"] == 0.0).all()


def test_alvo_media_futura_nao_atravessa_produtores():
    """
    O alvo usa ``transform`` por grupo, portanto já era por produtor; fica
    registrado como contrato. O último dia de cada produtor não tem futuro
    dentro do grupo, o alvo é NaN e a linha sai da base.
    """
    base = _dois_produtores(n_dias=60, valor_1=100.0, valor_2=1000.0)
    df = engenharia_de_atributos(base, DIM_PRODUTOR, ROTA)

    produtor_1 = df[df["id_produtor"] == 1]
    produtor_2 = df[df["id_produtor"] == 2]
    assert (produtor_1[TARGET] == 100.0).all()
    assert (produtor_2[TARGET] == 1000.0).all()
    # cada produtor perde o ultimo dia (sem futuro) e os 28 primeiros (sem lag_28)
    assert len(produtor_1) == 60 - 28 - 1
    assert len(produtor_2) == 60 - 28 - 1
    assert HORIZONTE_DIAS == 7


def test_split_temporal_continua_por_data():
    """O split é por data, não por produtor; os dois produtores aparecem em cada fatia."""
    base = _dois_produtores(n_dias=800, valor_1=100.0, valor_2=1000.0, inicio="2023-01-01")
    df = engenharia_de_atributos(base, DIM_PRODUTOR, ROTA)
    train, valid, test = split_temporal(df)

    assert train["data"].max() < pd.Timestamp("2024-01-01")
    assert valid["data"].min() >= pd.Timestamp("2024-01-01")
    assert valid["data"].max() < pd.Timestamp("2025-01-01")
    assert test["data"].min() >= pd.Timestamp("2025-01-01")
    assert len(train) + len(valid) + len(test) == len(df)
    for fatia in (train, valid, test):
        assert set(fatia["id_produtor"]) == {1, 2}
