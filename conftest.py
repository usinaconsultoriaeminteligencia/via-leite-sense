# Presença deste arquivo faz o pytest inserir a raiz do projeto em sys.path,
# tornando o pacote `via_leite_edge` importável mesmo com o comando `pytest`
# (sem `python -m`). Sem isto, `pytest -q` falha em coletar os testes com
# ModuleNotFoundError: No module named 'via_leite_edge'.
