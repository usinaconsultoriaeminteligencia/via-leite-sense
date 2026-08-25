"""VIA LEITE SENSE — pacote da aplicação.

Reúne os módulos que antes viviam soltos na raiz do repositório. A divisão
segue o fluxo dos dados, não a cronologia em que foram escritos:

    core/    motor de score e inteligência de fornecedor
    ingest/  entrada de dados reais — validação, guarda e importação
    models/  geração de base sintética e treino do modelo
    store/   persistência (DuckDB) e onboarding de cliente

Pacote de raiz e não `src/` layout de propósito: o build da Railway instala as
dependências antes de copiar o código, então um `src/` exigiria fixar um
PYTHONPATH — acoplamento implícito que este projeto já pagou caro uma vez
(ver MVP_DATA_DIR no SESSION_LOG). `via_leite_edge/` já funciona
assim.
"""
