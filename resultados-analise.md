# Resultados da análise da planilha

Valores calculados por `analise_planilha.py` (a planilha traz fórmulas sem resultado).

## 1. Margem por modelo

| Cód. | Modelo | Custo direto | Preço médio | Lucro/unid. | Margem teórica |
|---|---|---|---|---|---|
| BUS-URB-12M | Urbano Standard 12m | R$ 420.000 | R$ 580.000 | R$ 160.000 | 27,6% |
| BUS-URB-ART | Urbano Articulado 18m | R$ 850.000 | R$ 1.180.000 | R$ 330.000 | 28,0% |
| BUS-ROD-14M | Rodoviário Premium DD 14m | R$ 920.000 | R$ 1.350.000 | R$ 430.000 | 31,9% |
| BUS-MIC-09M | Micro-ônibus Executivo 9m | R$ 280.000 | R$ 390.000 | R$ 110.000 | 28,2% |
| BUS-ELE-12M | Urbano Elétrico 12m (Zero Emissão) | R$ 1.450.000 | R$ 1.980.000 | R$ 530.000 | 26,8% |

**Preço efetivamente praticado nos pedidos (12 meses) vs. preço de catálogo:**

| Cód. | Unid. pedidas | Preço médio praticado | Preço catálogo | Desvio | Margem c/ preço praticado |
|---|---|---|---|---|---|
| BUS-URB-12M | 59 | R$ 565.620 | R$ 580.000 | -2,5% | 25,7% |
| BUS-URB-ART | 36 | R$ 1.163.712 | R$ 1.180.000 | -1,4% | 27,0% |
| BUS-ROD-14M | 36 | R$ 1.358.714 | R$ 1.350.000 | 0,6% | 32,3% |
| BUS-MIC-09M | 140 | R$ 388.554 | R$ 390.000 | -0,4% | 27,9% |
| BUS-ELE-12M | 49 | R$ 1.946.192 | R$ 1.980.000 | -1,7% | 25,5% |

## 2. Custo de materiais (BOM) vs. custo direto estimado

| Cód. | Custo BOM | Custo direto estimado | BOM / custo direto |
|---|---|---|---|
| BUS-URB-12M | R$ 127.670 | R$ 420.000 | 30,4% |
| BUS-URB-ART | sem BOM | R$ 850.000 | - |
| BUS-ROD-14M | R$ 223.400 | R$ 920.000 | 24,3% |
| BUS-MIC-09M | sem BOM | R$ 280.000 | - |
| BUS-ELE-12M | R$ 539.000 | R$ 1.450.000 | 37,2% |

## 3. Carteira de pedidos

Total da carteira (12 meses): **R$ 273.939.931** em **320** unidades.

| Status | Unidades | Valor | % do valor |
|---|---|---|---|
| Entregue | 231 | R$ 189.997.569 | 69,4% |
| Em Produção | 62 | R$ 55.869.586 | 20,4% |
| Pendente / Atrasado | 27 | R$ 28.072.776 | 10,2% |

| Mês | Unidades | Valor |
|---|---|---|
| Nov/25 | 31 | R$ 20.596.411 |
| Dez/25 | 43 | R$ 31.705.222 |
| Jan/26 | 46 | R$ 27.175.139 |
| Fev/26 | 7 | R$ 9.701.228 |
| Mar/26 | 11 | R$ 15.872.326 |
| Abr/26 | 11 | R$ 17.532.998 |
| Mai/26 | 22 | R$ 16.162.920 |
| Jun/26 | 26 | R$ 24.969.885 |
| Jul/26 | 34 | R$ 26.281.441 |
| Ago/26 | 27 | R$ 23.909.248 |
| Set/26 | 35 | R$ 31.960.338 |
| Out/26 | 27 | R$ 28.072.776 |

| Modelo | Unidades | Valor | % do valor |
|---|---|---|---|
| BUS-ELE-12M | 49 | R$ 95.363.394 | 34,8% |
| BUS-MIC-09M | 140 | R$ 54.397.600 | 19,9% |
| BUS-ROD-14M | 36 | R$ 48.913.707 | 17,9% |
| BUS-URB-ART | 36 | R$ 41.893.631 | 15,3% |
| BUS-URB-12M | 59 | R$ 33.371.599 | 12,2% |

## 4. Linha de montagem: capacidade e qualidade

| Etapa | Estação | Ciclo (h) | Desvio (h) | Refugo/retrab. | Horas perdidas/veículo (ciclo×taxa) |
|---|---|---|---|---|---|
| 10 | Corte e Dobra de Vigas | 3.5 | 0.45 | 2,1% | 0.07 |
| 20 | Armação da Estrutura Lateral e Teto | 6.2 | 1.15 | 5,8% | 0.36 |
| 30 | Pintura e Tratamento Anticorrosivo | 8.0 | 0.8 | 1,5% | 0.12 |
| 40 | Chapeamento e Chapa Externa | 4.8 | 0.65 | 3,2% | 0.15 |
| 50 | Montagem de Vidros e Parabrisas | 2.9 | 0.95 | 7,4% | 0.21 |
| 60 | Instalação Elétrica e Mapeamento Chicote | 5.5 | 1.4 | 8,9% | 0.49 |
| 70 | Tapeçaria e Revestimento Interno | 6.0 | 0.5 | 1,8% | 0.11 |
| 80 | Acoplamento ao Chassi e Teste Final | 4.2 | 0.7 | 2,5% | 0.11 |

- Tempo total de ciclo por veículo (soma das etapas): **41.1 h**.
- Estação mais lenta (limita a vazão): **Pintura e Tratamento Anticorrosivo**, 8.0 h/veículo.
- Capacidade teórica operando 24h × 30 dias, sem paradas, com 1 veículo por estação: **90 veículos/mês** (720 h / 8.0 h). *Hipótese: estações em série, uma máquina por etapa.*
- Demanda média de pedidos: **26.7 veículos/mês** → uso da capacidade teórica de **29,6%**.
- Rendimento de primeira passagem (produto de 1 − refugo nas 8 etapas): **71,0%**, ou seja, **29,0%** dos veículos passam por refugo/retrabalho em alguma etapa.
- As 3 etapas sinalizadas como gargalo na planilha (20, 50, 60) respondem por **66,6%** da soma das taxas de refugo.
- A planilha chama de gargalo as etapas com refugo alto; a etapa que limita a vazão por tempo de ciclo é outra (pintura, 8 h).

## 5. Fornecedores e lead time

| Peça | Fornecedor | País | Preço | Lead time (dias) |
|---|---|---|---|---|
| PEC-ELE-402 | CATL Tech | China | R$ 480.000 | 60 |
| PEC-MOT-301 | Thermo King | EUA / Importado | R$ 28.500 | 45 |
| PEC-PORT-501 | Bode Eletrônica | Alemanha | R$ 6.500 | 30 |
| PEC-VID-101 | Vidroplan Auto | Brasil | R$ 3.400 | 20 |
| PEC-ELE-401 | Yazaki Brasil | Brasil | R$ 4.200 | 18 |
| PEC-BAN-201 | Marcopolo/Seating | Brasil | R$ 1.100 | 15 |
| PEC-EST-002 | Novelis do Brasil | Brasil | R$ 1.250 | 12 |
| PEC-VID-102 | AGC Vidros | Brasil | R$ 480 | 10 |
| PEC-ILU-701 | Arteb Faróis | Brasil | R$ 2.100 | 10 |
| PEC-PNT-601 | PPG Industries | Brasil | R$ 9.200 | 8 |
| PEC-EST-001 | Açotubo Indústria | Brasil | R$ 850 | 7 |
| PEC-BAN-202 | Plastilindo | Brasil | R$ 180 | 5 |

| Modelo | Maior lead time da BOM (dias) | Peça que define |
|---|---|---|
| BUS-URB-12M | 45 | PEC-MOT-301 |
| BUS-ROD-14M | 45 | PEC-MOT-301 |
| BUS-ELE-12M | 60 | PEC-ELE-402 |

Participação de peças importadas no custo de BOM (3 modelos): **67,9%**.

## 6. Folha de pagamento e absenteísmo

| Nível | Pessoas | Custo mensal (c/ encargos 45%) | Custo médio/pessoa | Absenteísmo | Custo das faltas (180 dias)* |
|---|---|---|---|---|---|
| Operacional | 86 | R$ 502.366 | R$ 5.841 | 5,5% | R$ 117.291 |
| Analista | 31 | R$ 338.612 | R$ 10.923 | 2,0% | R$ 29.495 |
| Gestor | 13 | R$ 277.539 | R$ 21.349 | 1,2% | R$ 14.347 |
| Diretoria | 5 | R$ 383.052 | R$ 76.610 | 0,0% | R$ 0 |

Folha mensal total (c/ encargos): **R$ 1.501.569** para **135** pessoas. Anual: **R$ 18.018.827**.
Diretoria: 5 pessoas = **25,5%** da folha.
Cada 10 operadores a menos economizam cerca de **R$ 58.415/mês** (antes de rescisão).
Folha mensal vs. faturamento médio mensal da carteira: **6,6%**.

\* custo da falta = total mensal ÷ 30 × faltas (aproximação). Excesso de operadores **não** é calculável só com a planilha: faltam horas-homem por veículo e escala de turnos.

## 7. Dividendos e JCP

| Mês | Classe | Dividendos | JCP (15%) | Status |
|---|---|---|---|---|
| Nov/25 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Dez/25 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Acumulado em Atraso |
| Jan/26 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Fev/26 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Acumulado em Atraso |
| Mar/26 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Abr/26 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Acumulado em Atraso |
| Mai/26 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Jun/26 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Acumulado em Atraso |
| Jul/26 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Ago/26 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Acumulado em Atraso |
| Set/26 | ON (Com Direito a Voto) | R$ 1.800.000 | R$ 270.000 | Suspenso p/ Reestruturação |
| Out/26 | PN (Preferenciais) | R$ 3.750.000 | R$ 562.500 | Exigência Judicial dos Minoritários |

| Status | Dividendos |
|---|---|
| Suspenso p/ Reestruturação | R$ 10.800.000 |
| Acumulado em Atraso | R$ 18.750.000 |
| Exigência Judicial dos Minoritários | R$ 3.750.000 |

- Total de dividendos em 12 meses: **R$ 33.300.000**; JCP (15%): **R$ 4.995.000**.
- Obs.: o rótulo da planilha diz "dividendos/JCP acumulados em atraso", mas a fórmula soma só dividendos (coluna E), e inclui meses "suspensos" (ON), não apenas os em atraso (PN).
- Dividendos de 12 meses = **12,2%** do valor bruto da carteira de pedidos do mesmo período.
- Dividendos = **17,5%** do valor já entregue; folha anual = **9,5%** do valor já entregue.
- Dividendos médios por mês: **R$ 2.775.000**; folha mensal: **R$ 1.501.569**; margem bruta teórica média ponderada da carteira: **27,4%** → lucro bruto médio/mês ≈ **R$ 6.265.828** (antes de folha, dívidas e outras despesas).

## 8. Atraso dos dividendos (referência: fim de Out/26)

A planilha **não tem** saldo de dívida bancária, taxa de juros nem multa: só os dividendos. O que dá para calcular é o passivo de dividendos e uma estimativa de encargos sobre os atrasados, com taxa **hipotética** (a real deve vir do cliente ou de fonte externa).

- Parcelas PN em atraso: **5** (Dez/25 a Ago/26), principal **R$ 18.750.000**; média ponderada de **6.0 meses** de atraso; a mais antiga tem 10 meses.

| Taxa hipotética | Juros acumulados (simples) | Multa 2% (hipótese) | Atrasado + encargos |
|---|---|---|---|
| 1,0% a.m. | R$ 1.125.000 | R$ 375.000 | R$ 20.250.000 |
| 1,5% a.m. | R$ 1.687.500 | R$ 375.000 | R$ 20.812.500 |
| 2,0% a.m. | R$ 2.250.000 | R$ 375.000 | R$ 21.375.000 |

- Passivo de dividendos de 12 meses, por situação: em atraso **R$ 18.750.000** + exigência judicial **R$ 3.750.000** = **R$ 22.500.000** exigíveis; suspensos (ON) **R$ 10.800.000**; total **R$ 33.300.000**.
- Exigível hoje (atraso + judicial) = **67,6%** do total. Equivale a **3.6 meses** de lucro bruto médio (referência: R$ 6.265.828/mês).

## 9. Impacto das respostas da 2ª entrevista

### 9.1 Multa por atraso nos pedidos pendentes

Regra do cliente: 10% do valor do ônibus + 0,1% do valor ao dia. *Hipótese:* os 0,1%/dia incidem sobre o valor dos pedidos atrasados. Dias de atraso não constam na planilha.

| Dias de atraso | Multa fixa (10%) | Multa diária acumulada | Total |
|---|---|---|---|
| 0 | R$ 2.807.278 | R$ 0 | R$ 2.807.278 |
| 15 | R$ 2.807.278 | R$ 421.092 | R$ 3.228.369 |
| 30 | R$ 2.807.278 | R$ 842.183 | R$ 3.649.461 |
| 60 | R$ 2.807.278 | R$ 1.684.367 | R$ 4.491.644 |

- 27 ônibus pendentes, valor **R$ 28.072.776**; cada dia de atraso custa **R$ 28.073** de multa, **10,0%** do valor já é devido pela multa fixa (**R$ 2.807.278**).
- Prefeituras só pagam na entrega (resposta 11): atraso adia a receita **e** gera multa.

### 9.2 Plano de pagamento dos dividendos (prazo de 12 meses; atrasados em 24 meses se estiver em dia)

| Cenário | Atrasado a quitar | Parcela/mês (24 m) | Dividendo corrente/mês | Saída mensal total | % do lucro bruto médio/mês |
|---|---|---|---|---|---|
| A: atrasados PN + judicial | R$ 22.500.000 | R$ 937.500 | R$ 2.775.000 | R$ 3.712.500 | 59,2% |
| B: A + dividendos ON suspensos | R$ 33.300.000 | R$ 1.387.500 | R$ 2.775.000 | R$ 4.162.500 | 66,4% |

- Sem juros e multa (taxa não informada). Dividendo corrente = média mensal do cronograma da planilha (ON e PN alternam), mantendo as ações atuais.
- Lucro bruto médio/mês de referência: **R$ 6.265.828** (margem direta; segundo o cliente o custo direto já inclui mão de obra e impostos).

### 9.3 Capacidade com restrições informadas

Restrições: 3 turnos de 8 h (24 h); etapa 80 (acoplamento ao chassi) não opera à noite (iluminação e ruído) → 16 h. Tempo de ciclo efetivo = ciclo × (1 + taxa de refugo/retrabalho), pois o cliente disse que a taxa é sobre o tempo de ciclo.

| Etapa | Estação | Horas/dia | Ciclo efetivo (h) | Capacidade teórica (veíc./mês) |
|---|---|---|---|---|
| 10 | Corte e Dobra de Vigas | 24 | 3.57 | 201 |
| 20 | Armação da Estrutura Lateral e Teto | 24 | 6.56 | 110 |
| 30 | Pintura e Tratamento Anticorrosivo | 24 | 8.12 | 89 |
| 40 | Chapeamento e Chapa Externa | 24 | 4.95 | 145 |
| 50 | Montagem de Vidros e Parabrisas | 24 | 3.11 | 231 |
| 60 | Instalação Elétrica e Mapeamento Chicote | 24 | 5.99 | 120 |
| 70 | Tapeçaria e Revestimento Interno | 24 | 6.11 | 118 |
| 80 | Acoplamento ao Chassi e Teste Final | 16 | 4.3 | 111 |

- Limite teórico da linha: **89 veículos/mês** (Pintura e Tratamento Anticorrosivo). Demanda média **26.7**, pico mensal **46** (51,9% do limite).
- Se o limite teórico fosse real, não haveria pedidos atrasados: o gargalo efetivo está em **fornecedores e paradas de máquina de segunda mão**, não no tempo de ciclo. Não há dados de paradas na planilha.

### 9.4 Capital imobilizado em inversores/baterias (peça importada, sem produtor nacional)

- Elétricos: **4.1 unid./mês** × R$ 480.000 = **R$ 1.960.000/mês** em inversores/baterias.
- Com lead time de **60 dias**, o capital em trânsito/estoque é de cerca de **R$ 3.920.000** (se pago no pedido; condição de pagamento não informada).
- Chicote Yazaki (PEC-ELE-401) **não pode ser trocado** (cliente); lead time 18 dias.

### 9.5 Lead time como medida de atraso do fornecedor

Segundo o cliente, lead time é o tempo médio real de entrega do fornecedor; logo ele já é o dado de atraso. Prazo mínimo pedido→entrega por modelo = maior lead time da BOM + tempo de ciclo da linha, se a peça só for comprada após o pedido.

| Modelo | Maior lead time (dias) | Ciclo da linha (dias) | Prazo mínimo pedido→entrega (dias) |
|---|---|---|---|
| BUS-URB-12M | 45 | 1.7 | 47 |
| BUS-ROD-14M | 45 | 1.7 | 47 |
| BUS-ELE-12M | 60 | 1.7 | 62 |

| Peça | Fornecedor | Lead time (dias) | Troca possível? |
|---|---|---|---|
| PEC-ELE-402 | CATL Tech | 60 | Sem produtor nacional |
| PEC-MOT-301 | Thermo King | 45 | Sim, com aviso de 30 dias |
| PEC-PORT-501 | Bode Eletrônica | 30 | Sim, com aviso de 30 dias |
| PEC-VID-101 | Vidroplan Auto | 20 | Sim, com aviso de 30 dias |
| PEC-ELE-401 | Yazaki Brasil | 18 | Não (cliente) |
| PEC-BAN-201 | Marcopolo/Seating | 15 | Sim, com aviso de 30 dias |

