"""Conteúdo do Plano de Trabalho FAPEG — Desafio AgroStartup 2026 · VIA LEITE SENSE.

Fonte única: `gerar_plano_trabalho.py` preenche o modelo oficial (`modelo_fapeg.docx`) SEM
alterar sua estrutura (orientação da tutoria SENAR/FAPEG em 25/09/2026) e gera a planilha de
controle interno (.xlsx). Editar aqui e regerar; não editar os binários à mão.

Trechos entre colchetes ([PREENCHER ...]) saem destacados em amarelo no documento.

Regra financeira (tutoria 25/09/2026): o recurso é liberado em duas parcelas de R$ 30.000
(meses 1–6 e 7–12, com prestação de contas entre elas). As despesas estão na ordem de compra,
cada uma ligada ao objetivo específico que a exige, e cada parcela soma exatamente R$ 30.000.
"""

EMPRESA = {
    "cnpj": "[PREENCHER CNPJ]",
    "nome_fantasia": "VIA LEITE SENSE",
    "razao_social": "[PREENCHER RAZÃO SOCIAL]",
    "endereco": "Rua 261, nº 384, Setor Leste Universitário — Goiânia/GO",
    "telefone": "(62) 99998-0016",
    "email": "fagnerpro80@gmail.com",
}

PROPONENTE = {
    "cpf": "222.826.828-31",
    "nome": "Fagner Pinho [PREENCHER NOME COMPLETO]",
    "telefone": "(62) 98291-1222",
    "email": "fagnerpro80@gmail.com",
}

# (cpf, nome completo, telefone, e-mail, nível de formação, função na startup)
EQUIPE = [
    ("222.826.828-31", "Fagner Pinho [PREENCHER NOME COMPLETO]", "(62) 98291-1222",
     "fagnerpro80@gmail.com", "Tecnólogo em Inteligência Artificial",
     "CEO — Diretor Executivo e coordenador do projeto"),
    ("[PREENCHER CPF]", "Maria Vitória [PREENCHER NOME COMPLETO]", "[PREENCHER]",
     "[PREENCHER]", "[PREENCHER NÍVEL] em Medicina Veterinária",
     "Diretora Técnica — Médica Veterinária Responsável Técnica"),
    ("[PREENCHER CPF]", "Diego Santana [PREENCHER NOME COMPLETO]", "[PREENCHER]",
     "[PREENCHER]", "[PREENCHER NÍVEL] em Engenharia de Software",
     "CTO — Diretor de Tecnologia"),
    ("702.544.951-25", "Matheus Iverson [PREENCHER NOME COMPLETO]", "(62) 99865-0640",
     "iversonfotografia@gmail.com", "Tecnólogo em Inteligência Artificial",
     "CDO — Diretor de Dados e Inteligência Artificial"),
    ("024.668.311-20", "Daianne Valéria Silva", "(62) 99603-9453",
     "daiannevsilva@hotmail.com", "Tecnóloga em Inteligência Artificial",
     "CPO — Diretora de Produto e Experiência do Usuário"),
]

TITULO = (
    "VIA LEITE SENSE Saúde: monitoramento preditivo da saúde do rebanho leiteiro e da "
    "conservação do leite com sensores de baixo custo e inteligência artificial, validado "
    "em cinco propriedades de Goiás"
)

OBJETIVO_GERAL = (
    "Desenvolver e validar em campo, em 12 meses, o Módulo de Saúde do Rebanho do VIA LEITE "
    "SENSE — sensores de baixo custo no tanque de expansão e no curral, integrados à plataforma "
    "de inteligência artificial já em operação — para emitir alertas antecipados de mastite "
    "subclínica (tendência de CCS), estresse térmico (THI medido na propriedade) e falha de "
    "resfriamento do leite, com validação veterinária em cinco propriedades leiteiras de Goiás, "
    "reduzindo o tempo entre o início do problema sanitário e a intervenção e protegendo a "
    "qualidade do leite que chega ao consumidor."
)

# O prazo de cada objetivo é o cronograma do projeto (orientação da tutoria): meses 1–6 =
# 1ª parcela (protocolo, protótipo e software); meses 7–12 = 2ª parcela (piloto e validação).
OBJETIVOS_ESPECIFICOS = [
    "Aprovar o protocolo técnico-sanitário e selecionar 5 propriedades leiteiras em Goiás "
    "(≥ 120 vacas em lactação), com termo de adesão, consentimento LGPD e linha de base de CCS, "
    "CBT e produção dos 3 meses anteriores — até o mês 2.",
    "Construir 2 protótipos (nó de tanque e microestação de THI), validá-los em bancada e operar "
    "um deles por 30 dias em uma propriedade, com desvio ≤ 0,5 °C frente a registrador "
    "calibrado, entrega de dados ≥ 95% e recuperação automática após quedas de energia e de "
    "rede — até o mês 5.",
    "Entregar o Módulo de Saúde do Rebanho v1.0 com 3 alertas — tendência de CCS (mastite "
    "subclínica), estresse térmico por THI local e falha de resfriamento do tanque — enviados "
    "por WhatsApp em até 15 minutos, com 100% dos testes críticos aprovados — até o mês 6.",
    "Replicar os kits para as 5 propriedades e operar piloto de campo de 120 dias, com "
    "disponibilidade de dados ≥ 95% e ao menos 4 propriedades ativas ao final — meses 7 a 10.",
    "Validar os alertas sanitários contra referência veterinária (linha de base laboratorial no "
    "mês 6, CMT quinzenal e 550 análises de CCS/CBT), atingindo sensibilidade ≥ 70% com "
    "antecedência ≥ 7 dias sobre o laudo de rotina e precisão ≥ 60% — meses 6 a 11.",
    "Capacitar 25 produtores e ordenhadores e 5 técnicos em prevenção de mastite, manejo do "
    "estresse térmico e resposta aos alertas, com satisfação média ≥ 4 em escala de 1 a 5 — até "
    "o mês 7.",
    "Reduzir em ≥ 15% a CCS média de tanque das propriedades piloto em relação à linha de base e "
    "firmar ≥ 2 cartas de intenção com laticínios ou cooperativas para adoção do módulo — até o "
    "mês 12.",
]

# Descrição — o que estamos desenvolvendo (dividida entre as duas caixas do modelo).
DESCRICAO = [
    [
        "O VIA LEITE SENSE é uma plataforma de inteligência artificial para a cadeia leiteira, já "
        "publicada e em operação: aplicação web, API autenticada, banco de dados, Score VIA LEITE "
        "de risco com 7 dimensões ancoradas na IN 77/2018 e modelo preditivo com horizonte de 7, "
        "15 e 30 dias (R² de 0,994 em teste). Hoje a plataforma prevê volume e risco de qualidade a "
        "partir de registros de produção, laudos e clima oficial do INMET. Este projeto acrescenta "
        "a camada que falta para cuidar da saúde do rebanho: medição física na propriedade e "
        "validação veterinária dos alertas em campo.",
        "A mastite subclínica — inflamação da glândula mamária sem sinal visível — é a doença de "
        "maior impacto econômico na pecuária leiteira e só aparece no laudo mensal de CCS, quando o "
        "leite já foi entregue e a bonificação já foi perdida. O estresse térmico, agravado no "
        "Cerrado goiano, reduz produção e imunidade e é frequentemente confundido com problema "
        "sanitário. A falha de resfriamento do tanque multiplica a carga bacteriana (CBT) em poucas "
        "horas e compromete a segurança do alimento. Nas três situações o produtor descobre tarde, "
        "e o veterinário — profissional escasso no campo — é chamado quando o problema já é grande.",
        "A solução integra três camadas. Na primeira, um nó instalado no tanque de expansão mede a "
        "temperatura do leite por sonda em poço termométrico de inox (sem contato com o produto e "
        "sem alterar a higienização), o nível por ultrassom e o funcionamento do compressor, e uma "
        "microestação no curral mede temperatura e umidade para calcular o THI (índice de "
        "temperatura e umidade) da própria propriedade, em vez da média regional do INMET. Na "
        "segunda, um gateway local recebe os dados, guarda-os durante quedas de rede e os "
        "sincroniza com a nuvem. Na terceira, o motor de risco combina a série de CCS e CBT do "
        "laboratório com o THI local e a telemetria do tanque para emitir três alertas — tendência "
        "de elevação de CCS, estresse térmico e falha de resfriamento — entregues por WhatsApp ao "
        "produtor e em painel ao veterinário e ao técnico do laticínio.",
    ],
    [
        "O grau de inovação está no público e no ponto de medição. Soluções de monitoramento "
        "sanitário individual (coleiras, pedômetros, sensores em linha de ordenha) custam dezenas "
        "de milhares de reais e atendem grandes fazendas tecnificadas. O VIA LEITE SENSE atende o "
        "produtor médio: usa o tanque — equipamento que toda propriedade fornecedora de laticínio "
        "já possui — como ponto de medição, trata a CCS como sinal de tendência e não como "
        "resultado mensal, e separa a queda de produção de origem térmica da de origem sanitária, "
        "com custo de hardware abaixo de R$ 3.000 por propriedade.",
        "Ao final do projeto serão entregues o Módulo de Saúde do Rebanho v1.0 integrado à "
        "plataforma; o projeto documentado e replicável dos kits de campo; regras de alerta "
        "calibradas e validadas por médica veterinária com dados de fazendas goianas; cartilha de "
        "resposta aos alertas; e relatório técnico de validação. O sistema emite indicadores de "
        "risco e recomendações operacionais: não realiza diagnóstico nem prescreve tratamento, e "
        "qualifica a agenda do médico veterinário em vez de substituí-lo. Os dados dos produtores "
        "seguem a LGPD, com consentimento, controle de acesso e minimização de dados pessoais.",
    ],
]

METODOLOGIA = [
    [
        "O projeto é executado em cinco fases encadeadas, cada uma encerrada por um marco com "
        "critério de aceite objetivo; uma fase só libera a seguinte quando o critério é atingido. "
        "As fases 1 a 3 correspondem à primeira parcela do recurso (meses 1 a 6) e as fases 4 e 5 "
        "à segunda (meses 7 a 12). A equipe se reúne semanalmente e registra decisões e mudanças "
        "de escopo com análise de efeito sobre prazo e orçamento.",
        "Fase 1 — Descoberta e protocolo sanitário (meses 1 e 2). Visitas técnicas e entrevistas "
        "semiestruturadas com 15 produtores e 3 técnicos de laticínio para mapear a rotina de "
        "ordenha e a jornada de uso. A médica veterinária redige o protocolo de validação: "
        "critérios de inclusão das propriedades, frequência de CMT, amostragem laboratorial e "
        "definição de caso de CCS elevada (≥ 200 mil cél/mL). Seleção de 5 propriedades da bacia "
        "leiteira goiana com tanque de expansão e cobertura de sinal verificada, com termo de "
        "adesão e consentimento LGPD, e levantamento da linha de base (3 meses de laudos de "
        "CCS/CBT e de produção). Marco: protocolo aprovado e 5 propriedades selecionadas.",
        "Fase 2 — Protótipo e prova de conceito (meses 2 a 5). Seleção de componentes, desenho do "
        "circuito e de gabinetes impressos em 3D (vedação IP65, resistência a UV e a produtos de "
        "limpeza) e montagem de 2 nós de tanque e 1 microestação de THI. Ensaios em bancada contra "
        "registrador calibrado com rastreabilidade RBC, com perda de pacotes medida e corte "
        "induzido de energia e de rede. Em seguida, um protótipo opera 30 dias em uma das "
        "propriedades, com registrador independente em paralelo. Marco: desvio médio ≤ 0,5 °C, "
        "entrega ≥ 95% e recuperação automática comprovadas em relatório de ensaio.",
    ],
    [
        "Fase 3 — Módulo de Saúde do Rebanho (meses 3 a 6). Desenvolvimento incremental com "
        "revisão de código, testes automatizados e teste de usabilidade com produtores. Regras de "
        "alerta: tendência de CCS (inclinação da série do produtor comparada ao próprio histórico "
        "e aos limites da IN 77/2018); estresse térmico (THI local ≥ 72, com duração e "
        "intensidade); e resfriamento (leite acima de 4 °C após 3 horas da ordenha, IN 76 e "
        "77/2018). Os limiares são calibrados pela veterinária e começam conservadores para evitar "
        "falsos positivos. No mês 6 é coletada a linha de base laboratorial individual das vacas. "
        "Marco: v1.0 em produção, alerta entregue em até 15 minutos em teste ponta a ponta.",
        "Fase 4 — Replicação, capacitação e piloto de campo (meses 7 a 10). Montagem de mais 4 nós "
        "de tanque e 4 microestações, instalação nas 5 propriedades com equipamento de proteção e "
        "sem interferência na rotina de higienização, e oficina presencial em cada propriedade "
        "para produtores, ordenhadores e técnicos. Piloto de 120 dias com acompanhamento semanal "
        "remoto e visita mensal; um nó reserva garante substituição imediata em caso de falha. "
        "Validação veterinária: CMT quinzenal nas vacas em lactação, CCS individual mensal e "
        "CCS/CBT de tanque quinzenal em laboratório credenciado à RBQL. Cada alerta emitido é "
        "registrado com a resposta do produtor e o desfecho observado.",
        "Fase 5 — Avaliação, modelo comercial e encerramento (meses 10 a 12). Sensibilidade = "
        "eventos de CCS elevada precedidos de alerta com 7 ou mais dias ÷ eventos confirmados em "
        "laboratório; precisão = alertas confirmados ÷ alertas emitidos. A CCS de tanque é "
        "comparada à linha de base da mesma propriedade; como não há grupo controle, o resultado é "
        "reportado como associação, com as limitações registradas. O THI local é comparado ao da "
        "estação INMET de referência. Os resultados são apresentados a laticínios e cooperativas "
        "para teste de preço e coleta de cartas de intenção, e o projeto se encerra com relatório "
        "técnico e prestação de contas.",
    ],
]

JUSTIFICATIVA = [
    [
        "Relevância para Goiás. Goiás é o 5º maior produtor de leite do Brasil (8,2% da produção "
        "nacional, IBGE/SIDRA 2024) e a atividade sustenta milhares de propriedades familiares e "
        "médias no Sul e no Centro goiano. O estado combina duas condições que agravam o problema: "
        "estresse térmico sazonal intenso no Cerrado e baixa densidade de assistência técnica e "
        "veterinária por propriedade. Um sistema calibrado com dados de fazendas goianas atende "
        "diretamente essa realidade.",
        "Aderência ao tema “Inovar para Cuidar”. O projeto cuida da saúde animal — antecipa a "
        "mastite subclínica e o estresse térmico, principais causas de sofrimento e de perda "
        "produtiva da vaca leiteira — e da saúde humana: o leite mantido abaixo de 4 °C e com CCS e "
        "CBT controladas chega mais seguro ao consumidor, e a detecção precoce da mastite reduz a "
        "necessidade de tratamentos antimicrobianos em casos já agravados, contribuindo para o "
        "controle de resíduos no leite e da resistência antimicrobiana (abordagem Saúde Única).",
        "Dores do setor atendidas. O projeto responde às dores cadastradas no Desafio para a "
        "pecuária leiteira: sanidade do rebanho e produtividade leiteira (alertas de CCS e THI); "
        "qualidade do leite e acesso a mercados (conservação no tanque e histórico auditável de "
        "qualidade); escassez de mão de obra qualificada (o sistema faz a vigilância contínua que "
        "hoje depende do olho treinado, escasso no campo); e eficiência operacional (visitas "
        "técnicas priorizadas por risco em vez de rotina homogênea).",
        "Lacuna das alternativas. O controle de qualidade do leite é retrospectivo: o laudo mensal "
        "informa o problema depois que o leite foi pago. Sistemas individuais de monitoramento de "
        "vacas são caros para o produtor médio, e as estações meteorológicas regionais não "
        "representam o microclima do curral. Falta uma solução acessível que transforme dados já "
        "existentes — laudo, clima e tanque — em ação preventiva.",
    ],
    [
        "Potencial de mercado. O leite movimenta R$ 87,5 bilhões por ano no Brasil (IBGE 2024). O "
        "modelo de negócio é B2B2F: o laticínio ou a cooperativa licencia a plataforma e a oferece "
        "aos fornecedores (R$ 39 a R$ 69 por produtor/mês), porque protege o volume e a qualidade "
        "que compra. O ganho estimado ao produtor é de cerca de R$ 1.200 por mês em bonificação "
        "protegida e descarte evitado (produtor de 400 L/dia), valor a ser confirmado no piloto.",
        "Impacto produtivo e ambiental. A literatura técnica (Embrapa Gado de Leite) aponta redução "
        "de 25 a 35% da CCS e de 50 a 60% do descarte evitável com monitoramento e boas práticas. "
        "Cada litro não descartado evita as emissões já embarcadas em sua produção (cerca de "
        "2,5 kg de CO₂-eq por litro, FAO).",
        "Por que esta equipe é capaz. O risco tecnológico é baixo porque a plataforma já existe e "
        "está em produção: o recurso financia a instrumentação física e a validação sanitária em "
        "campo, não o desenvolvimento do zero. A equipe cobre todas as frentes do projeto — médica "
        "veterinária responsável pelo protocolo e pela validação clínica dos alertas; engenheiro de "
        "software responsável por hardware, firmware e integração IoT; cientista de dados que "
        "construiu o modelo preditivo; especialista em produto e UX para a interface do produtor; e "
        "gestão de produto e negócio com experiência no agro, responsável pela execução, pelas "
        "parcerias com laticínios e pela prestação de contas. A documentação técnica dos kits por "
        "estágio de implantação já foi elaborada com apoio do SENAI FATESG.",
    ],
]

# Resultados esperados: (resultado, entrega e meta) — divididos entre as duas caixas do modelo.
RESULTADOS = [
    [
        ("Protocolo e linha de base (mês 2)",
         "protocolo técnico-sanitário aprovado, 5 propriedades com termo de adesão (≥ 120 vacas "
         "em lactação) e linha de base de CCS, CBT e produção registrada."),
        ("Protótipos validados (mês 5)",
         "2 nós de monitoramento e microestação de THI com desvio ≤ 0,5 °C, entrega de dados "
         "≥ 95% e 30 dias de operação em propriedade, com projeto e manual de montagem."),
        ("Módulo de Saúde do Rebanho v1.0 (mês 6)",
         "3 alertas (CCS, THI e resfriamento) enviados por WhatsApp em até 15 minutos e painel "
         "do veterinário em produção, com 100% dos testes críticos aprovados."),
        ("Piloto de campo concluído (mês 10)",
         "kits operando 120 dias em 5 propriedades, com disponibilidade ≥ 95% e ao menos 4 "
         "propriedades ativas ao final."),
    ],
    [
        ("Alertas sanitários validados (mês 11)",
         "relatório de validação veterinária com 550 análises laboratoriais e CMT quinzenal; "
         "sensibilidade ≥ 70% com antecedência ≥ 7 dias e precisão ≥ 60%."),
        ("Pessoas capacitadas (mês 7)",
         "5 oficinas presenciais e cartilha de resposta aos alertas; 25 produtores e "
         "ordenhadores e 5 técnicos capacitados, com satisfação ≥ 4/5."),
        ("Impacto na saúde do úbere (mês 12)",
         "redução ≥ 15% da CCS média de tanque nas propriedades piloto frente à linha de base."),
        ("Caminho de mercado estruturado (mês 12)",
         "modelo de preço validado e ≥ 2 cartas de intenção de laticínios ou cooperativas."),
    ],
]

# ---------------------------------------------------------------------------
# DESPESAS — em ordem de compra. "meses": {mês: valor}. "oe": nº do objetivo específico.
# Itens comprados nas duas parcelas aparecem em linhas separadas (uma por parcela).
# ---------------------------------------------------------------------------
R_MATERIAL = "CUSTEIO: Aquisição de material de consumo"
R_SERVICO = "CUSTEIO: Serviços de terceiros de pessoa física e/ou jurídica de caráter eventual"
R_CAPITAL = "CAPITAL: Aquisição de máquinas, equipamentos, aparelhos e utensílios"

ESPEC_NO = ("sonda de temperatura resistiva classe A com 3 fios e cabo de 3 m; conversor de "
            "sinal de 15 bits; microcontrolador 32 bits dual-core com Wi-Fi e BLE; sensor digital "
            "de temperatura e umidade ±0,3 °C; sensor ultrassônico de nível à prova d'água; "
            "sensor de corrente não invasivo 100 A com condicionador; 2 células de lítio com "
            "módulo de carga; fonte 5 V/3 A")
ESPEC_INST = ("poço termométrico em inox 304 rosca 1/2\"; caixa hermética IP65 200 × 150 × 80 mm; "
              "4 prensa-cabos; 10 m de cabo blindado 2 × 0,5 mm²; terminais e fixadores inox")
ESPEC_THI = ("sensor digital de temperatura e umidade ±0,3 °C; microcontrolador 32 bits com "
             "Wi-Fi; célula de lítio com módulo de carga; painel solar 6 V/2 W")
ESPEC_GW = ("computador de placa única 64 bits, 4 núcleos, 8 GB de RAM, com gabinete com "
            "dissipação ativa, fonte de 27 W e cartão de memória industrial de 32 GB")
ESPEC_4G = ("roteador LTE categoria 4 com slot para chip, Wi-Fi e porta Ethernet, com antena "
            "externa de 9 dBi, cabo de 5 m e suporte de mastro")
ESPEC_LOG = ("registrador autônomo de temperatura com sonda externa, faixa −40 a +85 °C, "
             "resolução 0,1 °C, memória ≥ 16.000 leituras, USB, com certificado de calibração")

CAPITAL = [
    dict(item="Computador portátil para desenvolvimento e ciência de dados",
         espec="Processador de 8 núcleos/16 threads ou superior; 32 GB de RAM; SSD NVMe 1 TB; GPU "
               "dedicada com 8 GB; tela 15,6\".",
         qtd=1, unit=8500, oe="2, 3 e 5", meses={1: 8500},
         just="Uso exclusivo no projeto para compilar o firmware dos protótipos, rodar o ambiente "
              "de testes e treinar e recalibrar os modelos com as séries de telemetria das "
              "propriedades. Os equipamentos pessoais da equipe não comportam o treinamento com "
              "dados de alta frequência."),
    dict(item="Estação de solda com controle digital de temperatura",
         espec="Potência ≥ 60 W, faixa 200–480 °C, com suporte e esponja.",
         qtd=1, unit=700, oe="2", meses={1: 700},
         just="Montagem dos protótipos e das unidades de campo (soldagem de sensores, conectores "
              "e placas) e reparos durante o piloto."),
    dict(item="Multímetro digital true RMS",
         espec="Categoria CAT III 600 V; mede tensão, corrente, resistência, continuidade e "
               "temperatura.",
         qtd=1, unit=450, oe="2 e 4", meses={1: 450},
         just="Verificação de alimentação, consumo em bateria e diagnóstico de falhas na bancada "
              "e na instalação em campo."),
    dict(item="Fonte de alimentação de bancada regulável",
         espec="Saída 0–30 V / 0–5 A, com ajuste fino e indicação digital de tensão e corrente.",
         qtd=1, unit=650, oe="2", meses={1: 650},
         just="Ensaios de consumo, simulação de queda e retorno de energia e teste de autonomia "
              "em bateria, exigidos pelo critério de aceite dos protótipos."),
    dict(item="Impressora 3D de fabricação por filamento fundido",
         espec="Área de impressão ≥ 250 × 250 × 250 mm; mesa aquecida ≥ 100 °C; câmara fechada; "
               "nivelamento automático; compatível com PETG e ASA.",
         qtd=1, unit=5500, oe="2 e 4", meses={2: 5500},
         just="Fabricação dos gabinetes estanques, suportes de sonda e abrigos de radiação das "
              "microestações, sob medida para cada tanque e curral, com iteração rápida do "
              "desenho após os ensaios e reposição de peças no piloto. A câmara fechada é "
              "necessária para o ASA, resistente a UV e a produtos de limpeza."),
    dict(item="Computador de borda (gateway) — prova de conceito",
         espec=ESPEC_GW + ".", qtd=1, unit=1100, oe="2", meses={3: 1100},
         just="Recebe os dados dos sensores na propriedade da prova de conceito, armazena durante "
              "quedas de internet e sincroniza com a nuvem, para que nenhuma leitura se perca "
              "justamente durante o evento que o sistema precisa detectar."),
    dict(item="Roteador 4G com antena externa — prova de conceito",
         espec=ESPEC_4G + ".", qtd=1, unit=750, oe="2", meses={3: 750},
         just="Enlace entre o gateway e a nuvem na propriedade da prova de conceito, em área "
              "rural com sinal fraco; a antena externa viabiliza a entrega de dados ≥ 95%."),
    dict(item="Registrador de temperatura de referência — bancada e prova de conceito",
         espec=ESPEC_LOG + ".", qtd=2, unit=450, oe="2", meses={3: 900},
         just="Medição independente em paralelo aos protótipos, na bancada e no tanque, para "
              "comprovar o desvio ≤ 0,5 °C. Sem a segunda medição o teste afirma que o sensor "
              "funciona; com ela, demonstra."),
    dict(item="Computadores de borda (gateways) — piloto",
         espec=ESPEC_GW + ".", qtd=4, unit=1100, oe="4", meses={7: 4400},
         just="Um para cada uma das outras 4 propriedades do piloto, com a mesma função do "
              "gateway da prova de conceito."),
    dict(item="Roteadores 4G com antena externa — piloto",
         espec=ESPEC_4G + ".", qtd=4, unit=750, oe="4", meses={7: 3000},
         just="Um para cada uma das outras 4 propriedades do piloto, condição para a "
              "disponibilidade de dados ≥ 95% exigida no piloto."),
    dict(item="Registradores de temperatura de referência — piloto",
         espec=ESPEC_LOG + ".", qtd=4, unit=450, oe="4 e 5", meses={7: 1800},
         just="Medição independente nos tanques das demais propriedades, para conferir a "
              "temperatura do leite durante todo o piloto."),
]

CUSTEIO = [
    dict(item="Hospedagem em nuvem da plataforma — meses 1 a 6",
         espec="Servidor de aplicação, banco de dados gerenciado, broker MQTT e backup diário "
               "(6 meses × R$ 300,00).",
         rubrica=R_SERVICO, qtd=6, unit=300, oe="2 e 3",
         meses={m: 300 for m in range(1, 7)},
         just="Infraestrutura que recebe a telemetria dos protótipos, executa o motor de risco e "
              "hospeda o ambiente de desenvolvimento do Módulo de Saúde do Rebanho."),
    dict(item="Combustível para deslocamentos — meses 1 a 6",
         espec="Gasolina comum: 240 L × R$ 6,30 (visitas de seleção, instalação da prova de "
               "conceito e coleta da linha de base).",
         rubrica=R_MATERIAL, qtd=240, unit=6.30, oe="1, 2 e 5",
         meses={1: 504, 2: 252, 4: 378, 6: 378},
         just="Visitas de seleção das propriedades e entrevistas (meses 1 e 2), instalação da "
              "prova de conceito (mês 4) e coleta da linha de base laboratorial (mês 6)."),
    dict(item="Componentes eletrônicos dos nós de tanque — protótipos",
         espec="Por kit: " + ESPEC_NO + ".", rubrica=R_MATERIAL, qtd=2, unit=950, oe="2",
         meses={2: 1900},
         just="Composição dos 2 protótipos (bancada e prova de conceito), que medem temperatura "
              "do leite, nível e funcionamento do compressor, base do alerta de resfriamento."),
    dict(item="Componentes da microestação de THI — protótipo",
         espec="Por unidade: " + ESPEC_THI + ".", rubrica=R_MATERIAL, qtd=1, unit=300, oe="2",
         meses={2: 300},
         just="Protótipo da microestação que mede o THI local para o alerta de estresse "
              "térmico."),
    dict(item="Filamento para impressão 3D (PETG e ASA)",
         espec="Carretel de 1 kg, 1,75 mm: 6 de PETG e 6 de ASA resistente a UV.",
         rubrica=R_MATERIAL, qtd=12, unit=125, oe="2 e 4", meses={2: 750, 3: 750},
         just="Matéria-prima dos gabinetes, suportes e abrigos de radiação de todos os kits, "
              "incluindo as iterações de desenho dos protótipos."),
    dict(item="Consumíveis de prototipagem eletrônica",
         espec="Placas perfuradas, estanho 1 mm, tubo termorretrátil, conectores, barras de "
               "pinos, jumpers, resistores e capacitores sortidos (1 lote).",
         rubrica=R_MATERIAL, qtd=1, unit=688, oe="2", meses={2: 688},
         just="Montagem dos protótipos e das unidades de campo na bancada."),
    dict(item="Material de instalação sanitária dos nós de tanque — protótipos",
         espec="Por kit: " + ESPEC_INST + ".", rubrica=R_MATERIAL, qtd=2, unit=400, oe="2",
         meses={3: 800},
         just="O poço de inox mantém a sonda sem contato com o leite, preservando a conformidade "
              "higiênico-sanitária (IN 76/77) e a rotina de limpeza do tanque."),
    dict(item="Calibração rastreável (RBC) das sondas dos protótipos",
         espec="Calibração em 3 pontos (0, 4 e 10 °C) com certificado RBC (2 sondas).",
         rubrica=R_SERVICO, qtd=2, unit=200, oe="2", meses={4: 400},
         just="Garante valor de prova à medição de temperatura do leite na faixa crítica da "
              "IN 76/77 (≤ 4 °C) e sustenta o critério de desvio ≤ 0,5 °C."),
    dict(item="Serviço de mensageria (API de mensagens) — meses 5 e 6",
         espec="Plano empresarial de API de mensagens para notificações (2 meses × R$ 150,00).",
         rubrica=R_SERVICO, qtd=2, unit=150, oe="3", meses={5: 150, 6: 150},
         just="Envio dos alertas no aplicativo de mensagens que o produtor já usa, testado com "
              "produtores antes do piloto."),
    dict(item="Reagente para California Mastitis Test (CMT) — linha de base",
         espec="Frasco de 1 L de reagente para CMT.", rubrica=R_MATERIAL, qtd=6, unit=55,
         oe="5", meses={6: 330},
         just="Teste de campo por quarto mamário para a linha de base sanitária das vacas em "
              "lactação e primeiras rodadas do piloto."),
    dict(item="Raquete (bandeja) para CMT",
         espec="Bandeja com 4 compartimentos, em plástico lavável.", rubrica=R_MATERIAL, qtd=6,
         unit=45, oe="5", meses={6: 270},
         just="Uma por propriedade e uma com a veterinária, para a execução do CMT."),
    dict(item="Caixa térmica para transporte de amostras de leite",
         espec="Caixa térmica de 12 L com gelo reciclável.", rubrica=R_MATERIAL, qtd=3,
         unit=150, oe="5", meses={6: 450},
         just="Transporte refrigerado das amostras até o laboratório credenciado, condição para "
              "a validade das análises de CCS e CBT."),
    dict(item="Análises laboratoriais de CCS — linha de base",
         espec="Contagem de células somáticas individual por vaca em laboratório credenciado à "
               "RBQL, incluindo frascos com conservante (100 análises).",
         rubrica=R_SERVICO, qtd=100, unit=12, oe="5", meses={6: 1200},
         just="Linha de base individual das vacas antes do início do piloto, referência para "
              "medir a antecedência dos alertas e a variação da CCS."),
    dict(item="Componentes eletrônicos dos nós de tanque — piloto",
         espec="Por kit: " + ESPEC_NO + ".", rubrica=R_MATERIAL, qtd=4, unit=950, oe="4",
         meses={7: 3800},
         just="Replicação para as outras 4 propriedades do piloto; o protótipo da bancada passa "
              "a ser o nó reserva para substituição imediata."),
    dict(item="Material de instalação sanitária dos nós de tanque — piloto",
         espec="Por kit: " + ESPEC_INST + ".", rubrica=R_MATERIAL, qtd=4, unit=400, oe="4",
         meses={7: 1600},
         just="Instalação sanitariamente segura nas 4 propriedades adicionais."),
    dict(item="Componentes das microestações de THI — piloto",
         espec="Por unidade: " + ESPEC_THI + ".", rubrica=R_MATERIAL, qtd=4, unit=300, oe="4",
         meses={7: 1200},
         just="Uma por propriedade adicional, para medir o THI local e compará-lo à estação "
              "INMET de referência."),
    dict(item="Calibração rastreável (RBC) das sondas do piloto",
         espec="Calibração em 3 pontos (0, 4 e 10 °C) com certificado RBC (4 sondas).",
         rubrica=R_SERVICO, qtd=4, unit=200, oe="4", meses={7: 800},
         just="Mesma garantia metrológica dos protótipos para as sondas instaladas no piloto."),
    dict(item="Reagente para California Mastitis Test (CMT) — piloto",
         espec="Frasco de 1 L de reagente para CMT.", rubrica=R_MATERIAL, qtd=6, unit=55,
         oe="5", meses={7: 330},
         just="CMT quinzenal por quarto mamário durante o piloto, referência veterinária para "
              "confirmar ou descartar cada alerta de CCS."),
    dict(item="Cartilha impressa de resposta aos alertas",
         espec="12 páginas, colorida, formato A5, papel couchê — “Sinais de alerta: mastite, "
               "estresse térmico e conservação do leite”.",
         rubrica=R_SERVICO, qtd=70, unit=17, oe="6", meses={7: 1190},
         just="Material das 5 oficinas de capacitação (25 produtores e ordenhadores e 5 "
              "técnicos) e distribuição a laticínios e cooperativas parceiras."),
    dict(item="Análises laboratoriais de CCS e CBT — piloto",
         espec="CCS individual por vaca (mensal) e CCS/CBT de tanque (quinzenal) em laboratório "
               "credenciado à RBQL, incluindo frascos com conservante (450 análises).",
         rubrica=R_SERVICO, qtd=450, unit=12, oe="5 e 7",
         meses={7: 1440, 8: 1440, 9: 1320, 10: 1200},
         just="Padrão-ouro para medir a sensibilidade e a precisão dos alertas e a redução da "
              "CCS de tanque; sem laudo laboratorial não há como comprovar os resultados."),
    dict(item="Hospedagem em nuvem da plataforma — meses 7 a 12",
         espec="Servidor de aplicação, banco de dados gerenciado, broker MQTT e backup diário "
               "(6 meses × R$ 300,00).",
         rubrica=R_SERVICO, qtd=6, unit=300, oe="4 e 5",
         meses={m: 300 for m in range(7, 13)},
         just="Recebe a telemetria das 5 propriedades em tempo real e executa o motor de risco "
              "durante o piloto e a avaliação."),
    dict(item="Serviço de mensageria (API de mensagens) — meses 7 a 12",
         espec="Plano empresarial de API de mensagens para notificações (6 meses × R$ 150,00).",
         rubrica=R_SERVICO, qtd=6, unit=150, oe="4", meses={m: 150 for m in range(7, 13)},
         just="Envio dos alertas aos produtores das 5 propriedades durante o piloto."),
    dict(item="Combustível para deslocamentos — meses 7 a 12",
         espec="Gasolina comum: 600 L × R$ 6,30 (≈ 33 viagens de ≈ 180 km ida e volta).",
         rubrica=R_MATERIAL, qtd=600, unit=6.30, oe="4, 5 e 7",
         meses={7: 945, 8: 630, 9: 630, 10: 630, 11: 315, 12: 630},
         just="Instalação e oficinas (mês 7), visitas mensais e coleta quinzenal de amostras "
              "no piloto (meses 7 a 10), coleta final (mês 11) e apresentação dos resultados a "
              "laticínios e cooperativas (mês 12)."),
]

CONTRAPARTIDA = [
    dict(item="Consultoria jurídica em proteção de dados (LGPD)",
         espec="Termo de consentimento do produtor, política de privacidade e acordo de "
               "compartilhamento de dados com laticínios.",
         rubrica=R_SERVICO, qtd=1, unit=2000, oe="1", meses={1: 2000},
         just="Base legal para coletar e tratar os dados das propriedades antes da instalação "
              "dos equipamentos."),
    dict(item="Serviço de contabilidade para a gestão financeira do projeto — meses 1 a 6",
         espec="Escrituração, conciliação da conta do projeto e apoio à prestação de contas da "
               "1ª parcela (6 meses × R$ 250,00).",
         rubrica=R_SERVICO, qtd=6, unit=250, oe="todos",
         meses={m: 250 for m in range(1, 7)},
         just="Assegura a conta exclusiva, a comprovação fiscal e a prestação de contas da 1ª "
              "parcela conforme a Resolução Normativa FAPEG nº 1/2023."),
    dict(item="Equipamentos de proteção descartáveis para acesso à sala de ordenha",
         espec="Luvas nitrílicas, toucas, propés e aventais descartáveis (1 lote).",
         rubrica=R_MATERIAL, qtd=1, unit=1000, oe="4 e 5", meses={7: 1000},
         just="Biosseguridade nas visitas de instalação e de coleta, evitando levar agentes "
              "patogênicos entre as propriedades."),
    dict(item="Serviço de contabilidade para a gestão financeira do projeto — meses 7 a 12",
         espec="Escrituração, conciliação da conta do projeto e apoio à prestação de contas "
               "final (6 meses × R$ 250,00).",
         rubrica=R_SERVICO, qtd=6, unit=250, oe="todos",
         meses={m: 250 for m in range(7, 13)},
         just="Assegura a comprovação fiscal e a prestação de contas final do projeto."),
]
