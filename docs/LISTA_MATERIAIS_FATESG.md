# Plano de Implantação Piloto — Materiais e Equipamentos por Estágio

**Projeto:** VIA LEITE SENSE — Radar de Risco Produtivo, Qualidade e Rentabilidade para a Cadeia Leiteira
**Proponente:** USINA I.A. — Goiânia, GO
**Instituição de apoio:** SENAI FATESG
**Contexto:** Desafio AgroStartup SENAR/SEBRAE Goiás 2026 — fase final
**Data:** Agosto de 2026 | **Versão:** 3.0 — lista completa vinculada a estágios de implantação

---

## 1. Objetivo

Apresentar a relação **completa e discriminada** de materiais e equipamentos
necessários à implantação real do VIA LEITE SENSE em campo, organizada em **seis
estágios sequenciais de implantação**.

Cada estágio é autossuficiente: entrega um resultado verificável, tem critério de saída
objetivo e **não depende dos estágios seguintes para produzir valor**. A instituição
pode apoiar do Estágio 0 até onde o orçamento alcançar, com a garantia de que nenhum
estágio custeado ficará ocioso à espera do próximo.

Todos os itens estão relacionados de forma **atômica** — um componente por linha, com
quantidade e valor unitário — de modo a permitir requisição formal de material sem
reabertura da lista.

---

## 2. Estágio atual do sistema

O VIA LEITE SENSE já está publicado e operacional: aplicação web, API autenticada,
banco de dados, motor de score de risco de 7 dimensões, modelo preditivo com horizonte
de 7/15/30 dias e integração com dados climáticos oficiais do INMET.

A camada de telemetria (**VIA LEITE EDGE**) também já está construída — contrato de
dados dos sensores, regras de alerta e interface de integração implementados e operando
**em modo simulado**.

> **O software não é o gargalo.** O componente ausente é o sensor físico. O apoio
> solicitado não financia desenvolvimento: financia a **instrumentação de um sistema já
> pronto para recebê-la**.

---

## 3. O kit de tanque valida a arquitetura?

Sim — e é por isso que ele é o Estágio 0. Mas convém delimitar com precisão o que ele
prova e o que só o campo prova, para que a expectativa da instituição corresponda ao
resultado entregue.

A cadeia completa do sistema é:

```
sonda física → conversão de sinal → microcontrolador → transporte MQTT
   → concentrador de borda → API → banco de dados → motor de score
      → regra de alerta → interface do usuário
```

### O que o kit de bancada valida integralmente ✅

| Elo da cadeia | Como é validado |
|---|---|
| Aquisição física e conversão de sinal | Sonda PT100 + conversor RTD gerando leitura real |
| Firmware de borda e resiliência | Reconexão automática, operação em bateria durante queda de energia |
| Transporte e protocolo MQTT | Publicação real de mensagens, com perda de conexão induzida |
| **Provedor de telemetria real** | É o **único componente hoje não implementado** no projeto — o kit é o que permite escrevê-lo e testá-lo |
| Ingestão, contrato de dados e persistência | Leitura real percorrendo API e banco, no formato já especificado |
| Motor de score e regras de alerta | Alerta de temperatura disparando a partir de medição, não de simulação |
| Interface do usuário | Leitura real aparecendo no painel em produção |
| **Ingestão concorrente multi-fazenda** | Validada com **2 nós simultâneos** — não com um só |

> Por isso o Estágio 0 prevê **dois kits, não um**. O segundo kit custa cerca de
> R$ 1.030 e é o que diferencia "um sensor funcionando" de "uma arquitetura
> multi-produtor funcionando". Com um único nó, a concorrência de ingestão permanece
> não testada.

### O que o kit valida parcialmente ⚠️

O contrato de telemetria do sistema prevê cinco grandezas medidas: temperatura do
tanque, volume, temperatura ambiente, umidade e THI. Um kit apenas de temperatura
preencheria **uma** delas, deixando as demais como valor de cadastro — e, com isso, os
alertas de volume, de prioridade de coleta e de estresse térmico não seriam de fato
exercitados.

Por cerca de **R$ 240 adicionais por kit** (sensor de umidade/temperatura ambiente,
sensor ultrassônico de nível e sensor de corrente do compressor), **todos os cinco
campos passam a ser medição real** e todas as regras de alerta são exercitadas. Esses
itens já estão incluídos no Estágio 0 por esse motivo.

### O que o kit **não** valida ❌

| Não validado no Estágio 0 | Onde é validado |
|---|---|
| Comportamento em sala de tanque real — umidade, lavagem, vibração, variação térmica, poeira | Estágio 1 |
| Conectividade rural instável e sincronização após queda de sinal | Estágio 1 |
| Autonomia de 30 dias sem intervenção humana | Estágio 1 — depende de **tempo**, não de material |
| Distribuição real de temperatura de tanque na região, para calibração dos limiares por fazenda | Estágio 1 |
| Rastreabilidade metrológica do dado (valor probatório junto ao laticínio) | Estágio 3 |
| Utilidade percebida do alerta pelo produtor | Estágios 2–3 — é validação de produto, não de arquitetura |
| Qualidade do leite: CCS, CBT e sólidos totais | Estágio 5 |

**Conclusão:** o Estágio 0 valida **a arquitetura**. O Estágio 1 valida **o
equipamento**. Os Estágios 2 e 3 validam **o produto**. São perguntas diferentes, e a
lista foi montada para responder uma de cada vez, na ordem certa.

---

## 4. Visão geral dos estágios

| Estágio | Nome | Pergunta que responde | Duração | Custo | Acumulado | Fase do roadmap |
|:---:|---|---|:---:|---:|---:|:---:|
| **0** | Bancada — prova de arquitetura | A cadeia funciona ponta a ponta com sensor real? | 2 sem. | **2.345** | 2.345 | Fase 4 (início) |
| **1** | Prova de conceito em 1 fazenda | O equipamento sobrevive e mede bem no campo? | 4–6 sem. | **3.680** | 6.025 | Fase 4 |
| **2** | Piloto formal — 3 fazendas | O sistema opera sem intervenção manual? | 8–12 sem. | **12.420** | 18.445 | Fase 2 + 4 |
| **3** | Evidência auditável | O dado tem valor probatório e comercial? | Contínuo | **7.010** | 25.455 | Fase 2 |
| **4** | Expansão e autonomia | O sistema escala para mais polos e locais sem rede? | Contínuo | **10.600** | 36.055 | Fase 4 |
| **5** | Frente de qualidade do leite | Conseguimos medir qualidade em campo? | Contínuo | **52.000** | 88.055 | Fase 3.5 |

**Ferramental de bancada** (Estágio 0) — R$ 2.100 adicionais **apenas se** o laboratório
do campus não dispuser dos equipamentos. Ver seção 11.

> Valores em reais, estimativas de referência para dimensionamento, sujeitas a cotação
> formal. Não constituem proposta de compra.

---

## 5. ESTÁGIO 0 — Bancada: prova de arquitetura

**Objetivo:** montar dois kits completos no laboratório e fazer a leitura de uma sonda
física percorrer toda a cadeia até disparar um alerta na plataforma em produção.

**Critério de saída:**
1. Leitura de sonda real visível no painel em produção;
2. Alerta de temperatura disparado por medição física, não por simulação;
3. Dois nós publicando simultaneamente, sem colisão de ingestão;
4. Recuperação automática após corte de energia e após queda de rede.

**O que destrava no software:** implementação do provedor real de telemetria — hoje o
único componente da camada IoT ainda não escrito.

### Componentes eletrônicos e sensores

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 0.1 | Sonda de temperatura PT100 classe A | Bulbo inox 6×100 mm, 3 fios, cabo 3 m, −50 a +200 °C | 2 | 130 | 260 |
| 0.2 | Módulo conversor RTD MAX31865 | 15 bits, interface SPI | 2 | 70 | 140 |
| 0.3 | Microcontrolador ESP32-S3 DevKitC | Wi-Fi 2,4 GHz + BLE | 2 | 90 | 180 |
| 0.4 | Sensor de temperatura e umidade SHT31-D | ±0,3 °C / ±2 % UR, I²C | 2 | 60 | 120 |
| 0.5 | Sonda digital DS18B20 | Encapsulada em inox, à prova d'água, cabo 3 m | 2 | 45 | 90 |
| 0.6 | Sensor de corrente não invasivo SCT-013-000 | Garra, 100 A | 2 | 75 | 150 |
| 0.7 | Placa condicionadora para SCT-013 | Resistor de carga e deslocamento de nível | 2 | 15 | 30 |
| 0.8 | Sensor de nível ultrassônico JSN-SR04T | Transdutor à prova d'água, 20–600 cm | 2 | 90 | 180 |
| 0.9 | Sensor magnético de abertura (reed switch) | NA/NF, com ímã | 2 | 20 | 40 |
| | **Subtotal — sensores** | | | | **1.190** |

### Alimentação e proteção

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 0.10 | Fonte chaveada 5 V / 3 A | Entrada bivolt, saída regulada | 2 | 45 | 90 |
| 0.11 | Módulo de carga TP4056 com proteção | Carga e proteção de célula de lítio | 2 | 15 | 30 |
| 0.12 | Célula de lítio 18650 | 3.000 mAh, alta descarga | 4 | 25 | 100 |
| 0.13 | Suporte para 2 células 18650 | Com terminais soldáveis | 2 | 10 | 20 |
| 0.14 | Caixa hermética IP65 | 200×150×80 mm, ABS, com tampa transparente | 2 | 85 | 170 |
| 0.15 | Prensa-cabos PG9 | Jogo com 4 unidades | 2 | 20 | 40 |
| 0.16 | Trilho DIN 35 mm | Barra de 20 cm | 2 | 15 | 30 |
| | **Subtotal — alimentação e proteção** | | | | **480** |

### Interface mecânica e cabeamento

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 0.17 | Poço termométrico inox 304 | Rosca 1/2", imersão sem contato direto com o produto | 2 | 120 | 240 |
| 0.18 | Cabo blindado 2×0,5 mm² | Rolo de 20 m, para instrumentação | 1 | 90 | 90 |
| 0.19 | Conectores e terminais | Kit sortido (ilhós, terminais fêmea, borne) | 1 | 40 | 40 |
| 0.20 | Abraçadeiras e buchas de fixação | Kit sortido | 1 | 20 | 20 |
| | **Subtotal — mecânica e cabeamento** | | | | **390** |

### Consumíveis de prototipagem

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 0.21 | Protoboard 830 pontos | — | 2 | 25 | 50 |
| 0.22 | Jumpers macho/fêmea | Kit com 120 unidades | 1 | 30 | 30 |
| 0.23 | Kit de resistores 1/4 W | Sortido, 600 peças | 1 | 35 | 35 |
| 0.24 | Kit de capacitores | Cerâmicos e eletrolíticos, sortido | 1 | 35 | 35 |
| 0.25 | Barras de pinos header | Jogo macho/fêmea | 1 | 20 | 20 |
| 0.26 | Estanho para solda 1 mm | Rolo 500 g | 1 | 90 | 90 |
| 0.27 | Tubo termorretrátil | Kit sortido com bitolas variadas | 1 | 25 | 25 |
| | **Subtotal — consumíveis** | | | | **285** |

### **SUBTOTAL ESTÁGIO 0: R$ 2.345**

**Nota técnica (0.10 a 0.13):** a bateria tampão é deliberada. Queda de energia é uma
das principais causas de falha de resfriamento — o equipamento precisa continuar
transmitindo justamente durante o evento que ele existe para detectar.

**Nota sanitária (0.17):** a sonda opera em poço termométrico e a medição de nível é
sem contato, preservando a conformidade higiênico-sanitária do tanque (IN 76/77) sem
alterar a rotina de higienização.

---

## 6. ESTÁGIO 1 — Prova de conceito em uma fazenda

**Objetivo:** instalar um kit em tanque de expansão real e mantê-lo operando 30 dias
sem intervenção, com medição independente em paralelo para conferência.

**Critério de saída:**
1. Trinta dias de série contínua com disponibilidade ≥ 95 %;
2. Desvio médio ≤ 0,5 °C contra registrador de referência instalado em paralelo;
3. Nenhuma perda de dado após queda de rede — sincronização posterior confirmada;
4. Primeira distribuição real de temperatura de tanque da região, para calibração dos
   limiares de alerta por fazenda.

**Por que o registrador independente é indispensável:** sem uma segunda medição,
o piloto afirma que o sensor funciona; com ela, o piloto **demonstra** que funciona.
É a diferença entre relato e evidência.

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 1.1 | Registrador autônomo de temperatura | Data logger calibrado, sonda externa, memória ≥ 16.000 pontos, USB | 2 | 400 | 800 |
| 1.2 | Computador de borda Raspberry Pi 5 | 4 GB RAM — broker MQTT local e buffer offline | 1 | 650 | 650 |
| 1.3 | Fonte oficial USB-C 27 W | Para o computador de borda | 1 | 150 | 150 |
| 1.4 | Gabinete com dissipação ativa | Para o computador de borda | 1 | 150 | 150 |
| 1.5 | Cartão microSD 32 GB classe industrial | Alta resistência a ciclos de escrita | 2 | 150 | 300 |
| 1.6 | Roteador 4G LTE CAT4 | Slot para SIM, Wi-Fi, porta Ethernet | 1 | 550 | 550 |
| 1.7 | Antena externa LTE 9 dBi | Cabo de 5 m e suporte de mastro | 1 | 180 | 180 |
| 1.8 | Nobreak 600 VA | Com estabilização, para o ponto de rede | 1 | 450 | 450 |
| 1.9 | Termômetro infravermelho | −30 a +200 °C, emissividade ajustável | 1 | 250 | 250 |
| 1.10 | Material de fixação em campo | Eletroduto flexível, abraçadeiras inox, silicone neutro, parafusos e buchas | 1 | 200 | 200 |

### **SUBTOTAL ESTÁGIO 1: R$ 3.680**

---

## 7. ESTÁGIO 2 — Piloto formal em três fazendas

**Objetivo:** atingir o critério formal da Fase 4 do roadmap do projeto — três fazendas
com sensores físicos transmitindo em tempo real, sem intervenção manual — e substituir
a estação climática regional por medição na própria propriedade.

**Critério de saída:**
1. Três fazendas operando simultaneamente por 60 dias;
2. Ao menos três alertas acionáveis reconhecidos como úteis pelo produtor ou técnico;
3. Nenhum registro dependente de preenchimento manual pelo produtor;
4. THI local medido, com comparação documentada contra a estação INMET de referência.

**Por que a estação meteorológica própria:** a estação INMET mais próxima pode estar a
dezenas de quilômetros da propriedade. O THI medido na porteira torna o alerta de
estresse térmico específico daquele rebanho, e não uma média regional.

### Réplica de dois kits de campo *(relação idêntica à do Estágio 0)*

| # | Item | Qtd | Unit. R$ | Total R$ |
|---:|---|---:|---:|---:|
| 2.1 | Sonda PT100 classe A com poço termométrico inox | 2 | 250 | 500 |
| 2.2 | Módulo conversor RTD MAX31865 | 2 | 70 | 140 |
| 2.3 | Microcontrolador ESP32-S3 DevKitC | 2 | 90 | 180 |
| 2.4 | Sensor de temperatura e umidade SHT31-D | 2 | 60 | 120 |
| 2.5 | Sonda digital DS18B20 em inox | 2 | 45 | 90 |
| 2.6 | Sensor de corrente SCT-013-000 + placa condicionadora | 2 | 90 | 180 |
| 2.7 | Sensor de nível ultrassônico JSN-SR04T | 2 | 90 | 180 |
| 2.8 | Reed switch de abertura de tampa | 2 | 20 | 40 |
| 2.9 | Conjunto de alimentação (fonte + TP4056 + 2× 18650 + suporte) | 2 | 95 | 190 |
| 2.10 | Caixa IP65 + prensa-cabos + trilho DIN | 2 | 120 | 240 |
| 2.11 | Cabo blindado, conectores e fixação | 2 | 100 | 200 |
| | **Subtotal — kits** | | | **2.060** |

### Conectividade, borda e campo

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 2.12 | Computador de borda Raspberry Pi 5 4 GB + fonte + gabinete | Conjunto completo | 2 | 950 | 1.900 |
| 2.13 | Cartão microSD 32 GB industrial | — | 2 | 150 | 300 |
| 2.14 | Roteador 4G LTE CAT4 | Slot SIM, Wi-Fi, Ethernet | 2 | 550 | 1.100 |
| 2.15 | Antena externa LTE 9 dBi + cabo 5 m | Com suporte de mastro | 2 | 180 | 360 |
| 2.16 | Nobreak 600 VA | Com estabilização | 2 | 450 | 900 |
| 2.17 | Material de fixação e instalação em campo | Por propriedade | 2 | 200 | 400 |
| | **Subtotal — conectividade e borda** | | | | **4.960** |

### Estação meteorológica e validação de interface

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 2.18 | Estação meteorológica automática | Temperatura, umidade, pluviometria, vento e radiação solar; Wi-Fi, alimentação solar | 1 | 2.200 | 2.200 |
| 2.19 | Abrigo meteorológico ventilado | Padrão, com proteção contra radiação | 1 | 250 | 250 |
| 2.20 | Mastro/tripé galvanizado 2 m | Com base e esticadores | 1 | 150 | 150 |
| 2.21 | Smartphone Android | 6 GB RAM / 128 GB, 4G — validação da interface em aparelho e rede equivalentes aos do usuário real | 2 | 1.400 | 2.800 |
| | **Subtotal — clima e interface** | | | | **5.400** |

### **SUBTOTAL ESTÁGIO 2: R$ 12.420**

**Nota (2.21):** o usuário final é o produtor rural, frequentemente com aparelho de
entrada e baixo letramento digital. Validar a interface nessas condições é requisito de
produto, não conveniência de equipe.

---

## 8. ESTÁGIO 3 — Evidência auditável

**Objetivo:** converter o dado coletado em evidência com valor probatório e comercial —
rastreável metrologicamente, apresentável a laticínio e defensável em relatório de ROI.

**Critério de saída:**
1. Sondas verificadas contra padrão rastreável, antes e depois da campanha de campo;
2. Relatório de piloto com dado primário e memória de cálculo auditável;
3. Rota de coleta rastreada, com tempo de trânsito do leite documentado;
4. Demonstrador funcional operando em feira, banca ou visita comercial.

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 3.1 | Termômetro digital de referência | −30 a +100 °C, resolução 0,01 °C, **com certificado de calibração rastreável (RBC)** | 1 | 1.800 | 1.800 |
| 3.2 | Maleta demonstradora | Reservatório instrumentado de 20 L, kit edge, display 7", fonte e identidade visual | 1 | 1.500 | 1.500 |
| 3.3 | Rastreador GPS veicular 4G | Com acesso a API/protocolo aberto | 2 | 500 | 1.000 |
| 3.4 | Kit de coleta para laboratório | 100 frascos com conservante bronopol, caixa térmica, gelo reciclável, lacres e etiquetas | 1 | 900 | 900 |
| 3.5 | Transdutor de nível submersível | 4–20 mA, inox 316 — maior precisão que o ultrassônico onde houver espuma | 2 | 380 | 760 |
| 3.6 | Bateria portátil 20.000 mAh + capa reforçada | Para dispositivos de campo | 2 | 350 | 700 |
| 3.7 | Kit CMT (California Mastitis Test) | Raquete de 4 poços + reagente 5 L | 1 | 350 | 350 |

### **SUBTOTAL ESTÁGIO 3: R$ 7.010**

**Por que o item 3.1 importa mais do que o preço sugere:** a plataforma emite alerta de
risco de qualidade a partir de faixas de temperatura previstas na IN 77. Alerta
sustentado por sensor sem rastreabilidade metrológica não tem valor probatório junto ao
laticínio. Este item converte a leitura do nosso sensor em **medição auditável** — e,
com ela, o piloto em evidência comercial.

---

## 9. ESTÁGIO 4 — Expansão e autonomia

**Objetivo:** cobrir o segundo polo climático, viabilizar instalação em tanques sem rede
elétrica estável e constituir ambiente de homologação próprio.

**Critério de saída:** operação em dois polos climáticos distintos com comparação
documentada de THI; ao menos um ponto operando com energia autônoma por 30 dias.

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 4.1 | Estação meteorológica automática | Segunda unidade, segundo polo climático | 1 | 2.200 | 2.200 |
| 4.2 | Abrigo meteorológico + mastro | Conjunto | 1 | 400 | 400 |
| 4.3 | Painel solar fotovoltaico 50 W | Policristalino, com moldura | 2 | 300 | 600 |
| 4.4 | Controlador de carga MPPT 10 A | 12 V | 2 | 250 | 500 |
| 4.5 | Bateria selada 12 V 18 Ah | VRLA/AGM | 2 | 300 | 600 |
| 4.6 | Caixa de proteção para sistema solar | IP65, com ventilação | 2 | 50 | 100 |
| 4.7 | Tablet 10" 4G | Uso pelo técnico/consultor em visita à propriedade | 1 | 1.800 | 1.800 |
| 4.8 | Mini PC 16 GB RAM / SSD 512 GB | Ambiente de homologação espelhado da produção e broker MQTT central | 1 | 3.500 | 3.500 |
| 4.9 | Nobreak 1200 VA senoidal | Para o servidor de homologação | 1 | 900 | 900 |

### **SUBTOTAL ESTÁGIO 4: R$ 10.600**

---

## 10. ESTÁGIO 5 — Frente de qualidade do leite

**Objetivo:** medir qualidade do leite em campo — frente de dado hoje **inacessível ao
projeto** e que ativa uma funcionalidade já especificada e inativa.

**Critério de saída:** camada de Perfil do Produtor operando com dados reais de sólidos;
acompanhamento de CCS em periodicidade semanal em vez de mensal.

| # | Item | Especificação | Qtd | Unit. R$ | Total R$ |
|---:|---|---|---:|---:|---:|
| 5.1 | Analisador ultrassônico portátil de leite | Gordura, proteína, sólidos não gordurosos, densidade, lactose, água adicionada e crioscopia; resultado em ~60 s | 1 | 18.000 | 18.000 |
| 5.2 | Contador portátil de células somáticas | Leitura direta de CCS em campo | 1 | 25.000 | 25.000 |
| 5.3 | Cassetes descartáveis para contador de CCS | Caixa com 500 unidades | 1 | 3.000 | 3.000 |
| 5.4 | Banho termostático de bancada | −10 a +40 °C, estabilidade ±0,1 °C, para calibração e ensaio dos sensores | 1 | 6.000 | 6.000 |

### **SUBTOTAL ESTÁGIO 5: R$ 52.000**

**Item 5.1 — o único equipamento que ativa uma funcionalidade inteira já pronta:** a
camada de Perfil do Produtor (Fase 3.5 do roadmap) foi especificada sobre **sólidos
totais — gordura e proteína** — variável que o projeto não possui em nenhuma base de
dados. Sem este equipamento, a funcionalidade permanece especificada e inativa.

**Itens 5.2 e 5.3:** a CCS é hoje obtida por laboratório externo em periodicidade
mensal (IN 77). A medição em campo permitiria acompanhamento semanal — aumento de
aproximadamente **quatro vezes** na resolução temporal da principal variável de
qualidade do modelo preditivo.

**Item 5.4:** dispensável se o campus dispuser de câmara climática, estufa ou
refrigerador de ensaio.

---

## 11. Ferramental de bancada — solicitar como acesso ao laboratório

Equipamentos necessários ao Estágio 0 que o campus provavelmente já possui. Solicitá-los
como uso de infraestrutura libera orçamento para o que só pode ser adquirido.

| Item | Especificação | Valor se comprado |
|---|---|---:|
| Multímetro true RMS | CAT III 600 V, com corrente e temperatura | R$ 450 |
| Estação de solda com controle de temperatura | Com sugador, malha dessoldante e suporte | R$ 600 |
| Fonte de bancada | 0–30 V / 0–5 A, digital, com limite de corrente | R$ 700 |
| Analisador lógico USB | 8 canais, 24 MHz — depuração de I²C e SPI | R$ 350 |
| **Total condicional** | | **R$ 2.100** |

Recursos adicionais sem desembolso, de valor equivalente ao material:

| Recurso | Aplicação |
|---|---|
| **Impressora 3D** | Suportes de sonda, gabaritos de fixação e invólucros customizados para o tanque |
| **Laboratório de metrologia** | Verificação das sondas contra padrão rastreável (substitui parte do item 3.1) |
| **Câmara climática / estufa / refrigerador de ensaio** | Ensaio dos sensores em faixa controlada de 0 a 10 °C (substitui o item 5.4, R$ 6.000) |
| **Osciloscópio de bancada** | Depuração de sinal analógico |
| **Bancada dedicada durante o piloto** | Montagem, manutenção e queima dos kits antes do envio a campo |
| **Alunos em projeto integrador, TCC ou estágio** | Frente de montagem e ensaios, com contrapartida acadêmica formalizável |
| **Carta de apoio institucional** | Facilita significativamente o acesso a cooperativas e laticínios da região |

---

## 12. Custeio — não é material permanente

Listado à parte, apenas para conhecimento da instituição.

| Item | Estágio | Estimativa |
|---|:---:|---:|
| Plano de dados M2M/IoT — 1 chip × 12 meses | 1 | R$ 360 |
| Planos de dados M2M/IoT — 2 chips × 12 meses | 2 | R$ 720 |
| Análises laboratoriais CCS/CBT/sólidos — 100 amostras | 3 | R$ 2.500 |
| Deslocamento às fazendas piloto (Sul Goiano) | 1–3 | a definir |
| Hospedagem em nuvem | — | já custeada pela USINA I.A. |

---

## 13. Resumo orçamentário e pontos de corte

| Apoio concedido até | Valor | O que fica pronto |
|---|---:|---|
| **Estágio 0** | **R$ 2.345** | Arquitetura validada de ponta a ponta com sensor físico real e dois nós concorrentes. Provedor de telemetria real implementado. |
| **Estágios 0 + 1** | **R$ 6.025** | Um tanque real medido por 30 dias, com validação independente e limiares calibrados pela distribuição real da região. |
| **Estágios 0 a 2** | **R$ 18.445** | Três fazendas operando sem intervenção manual, com clima medido na porteira. Cumpre o critério formal da Fase 4 do roadmap. |
| **Estágios 0 a 3** | **R$ 25.455** | Piloto com evidência auditável, rastreabilidade metrológica, rota rastreada e demonstrador comercial. |
| **Estágios 0 a 4** | **R$ 36.055** | Dois polos climáticos, autonomia energética e ambiente de homologação próprio. |
| **Estágios 0 a 5** | **R$ 88.055** | Escopo integral, incluindo medição de qualidade do leite em campo. |

> **Recomendação:** o **Estágio 0 (R$ 2.345)** é o melhor primeiro passo. É o menor
> valor da lista que produz um resultado demonstrável e irreversível — a partir dele o
> projeto deixa de ter camada simulada. Havendo margem, **Estágios 0 + 1 (R$ 6.025)**
> é o ponto em que o piloto passa a gerar evidência de campo, e não apenas prova
> técnica.

---

## 14. Contrapartidas oferecidas pela USINA I.A.

| Contrapartida | Descrição |
|---|---|
| **Crédito institucional** | Menção ao SENAI FATESG como apoiador técnico no pitch, na documentação, na plataforma e nos materiais de divulgação |
| **Relatório técnico por estágio** | Ao final de cada estágio custeado, relatório com metodologia, dados e critério de saída atingido — prestação de contas incremental |
| **Transferência de conhecimento** | Palestra/oficina aberta sobre arquitetura IoT + IA aplicada ao agronegócio, para alunos dos cursos de TI e áreas correlatas |
| **Campo de projeto para alunos** | Abertura do piloto como objeto de projeto integrador, TCC ou estágio supervisionado |
| **Destinação dos equipamentos** | Ao término do piloto, os bens permanentes seguem a política que a instituição determinar (devolução, comodato ou incorporação ao laboratório) |
| **Código-fonte e documentação** | Camada de telemetria documentada e disponibilizada como referência didática |

---

## 15. Cronograma por estágio

| Semana | Estágio | Atividade |
|:---:|:---:|---|
| 1 | 0 | Recebimento, montagem e queima dos dois kits em bancada |
| 2 | 0 | Implementação do provedor real de telemetria; leitura física chegando ao painel em produção |
| 3 | 1 | Ensaio de resiliência (corte de energia e de rede); instalação do registrador de referência |
| 4 | 1 | Instalação do primeiro kit em tanque real |
| 5–8 | 1 | Trinta dias de operação assistida; conferência contra o registrador; calibração dos limiares |
| 9–10 | 2 | Instalação nas fazendas 2 e 3; estação meteorológica em operação |
| 11–16 | 2 | Operação sem intervenção manual; acompanhamento e ajuste fino dos alertas |
| 17–20 | 3 | Verificação metrológica das sondas; consolidação da evidência; relatório de piloto |
| Contínuo | 4–5 | Expansão conforme apoio concedido |

---

*VIA LEITE SENSE — USINA I.A. © 2026 | Documento elaborado para o SENAI FATESG*
