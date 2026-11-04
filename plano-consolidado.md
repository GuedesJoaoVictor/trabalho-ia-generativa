# Saída do sistema de agentes: plano consolidado

Gerado por `executar.py` (tabelas e números vêm das ferramentas; texto das propostas vem dos agentes). Resultado de máquina, não é o relatório.

## Situação de partida (12 meses)

- Lucro bruto das entregas (proxy de caixa operacional): **R$ 4.363.131/mês**.
- Compromisso de dividendos (corrente + atrasados em 24 meses, com Selic): **R$ 3.766.443/mês**.
- Cobertura sem o plano: **1.16x**; com o plano: **1.19x**.
- O lucro bruto não desconta despesas fora do custo direto nem outras dívidas: é uma folga máxima, não o caixa real.

## Dados externos (Banco Central)

Consulta em 2026-11-03: Selic meta 13.75% a.a.; dólar R$ 5.4935; euro R$ 6.1500000; IPCA do mês 0.82%.

| Parcela em atraso | Principal | Meses | Correção Selic |
|---|---|---|---|
| Dez/25 | R$ 3.750.000 | 10 | R$ 438.075 |
| Fev/26 | R$ 3.750.000 | 8 | R$ 349.060 |
| Abr/26 | R$ 3.750.000 | 6 | R$ 256.384 |
| Jun/26 | R$ 3.750.000 | 4 | R$ 170.065 |
| Ago/26 | R$ 3.750.000 | 2 | R$ 81.058 |
| Out/26 | R$ 3.750.000 | 0 | R$ 0 |
| **Total** | **R$ 22.500.000** | | **R$ 1.294.643** |

## Propostas e parecer do Revisor

| ID | Agente | Proposta | Mensal | Pontual | Desembolso | Prazo | Parecer |
|---|---|---|---|---|---|---|---|
| FIN-1 | Financeiro | Regularizar dividendos: corrente em dia e atrasados em 24 meses | R$ -991.443 | R$ 0 | R$ 0 | 1 m | **aprovada** |
| FIN-2 | Financeiro | Priorizar a entrega dos 27 pedidos pendentes | R$ 0 | R$ 7.072.776 | R$ 0 | 2 m | **aprovada** |
| FIN-3 | Financeiro | Reduzir a produção do elétrico para aliviar caixa (alternativa avaliada) | R$ 0 | R$ 0 | R$ 0 | 2 m | **reprovada** |
| FIN-4 | Financeiro | Revisar a remuneração da diretoria (-20%) | R$ 76.610 | R$ 0 | R$ 0 | 2 m | **condicional** |
| OPE-1 | Operações | Operar em 2 turnos (3º turno só nos picos) e dimensionar o quadro de operadores | R$ 58.415 | R$ 0 | R$ 112.801 | 3 m | **condicional** |
| OPE-2 | Operações | Manutenção preventiva e padrão de trabalho nas etapas 20, 50 e 60 | R$ 2.156 | R$ 0 | R$ 0 | 3 m | **aprovada** |
| SUP-1 | Suprimentos | Comprar as peças longas no ato do pedido firme (ar-condicionado 45 d, portas 30 d, inversor 60 d) | R$ 0 | R$ 421.092 | R$ 0 | 1 m | **aprovada** |
| SUP-2 | Suprimentos | Cotar alternativas para ar-condicionado (Thermo King) e portas (Bode) | R$ 0 | R$ 0 | R$ 0 | 3 m | **aprovada** |
| SUP-3 | Suprimentos | Elétrico só contra pedido firme e negociar pagamento do inversor na entrega | R$ 0 | R$ 0 | R$ 0 | 3 m | **aprovada** |
| MER-1 | Mercado | Priorizar a venda dos modelos de maior lucro por ônibus (frotas sequenciais para prefeituras) | R$ 0 | R$ 0 | R$ 0 | 6 m | **aprovada** |
| MER-2 | Mercado | Fase 2: double-deck e novos segmentos | R$ 0 | R$ 0 | R$ 0 | 24 m | **aprovada** |

### Detalhe

**FIN-1 Regularizar dividendos: corrente em dia e atrasados em 24 meses** (aprovada)

Pagar o dividendo corrente todo mês e quitar em 24 meses o exigível (atraso PN + exigência judicial) com correção Selic, condição dada pelo cliente para afastar o bloqueio pela B3.

Hipóteses:
- Correção pela Selic acumulada (índice de referência; juros e multa reais não informados)
- Dividendos ON suspensos (R$ 10,8 mi) ficam fora da quitação; confirmar com o cliente
- Dividendo corrente = média mensal do cronograma da planilha, com as ações atuais

Fontes: passivo_dividendos; plano_dividendos; encargos_atrasados_selic; aba Dividendos e Passivos; BCB SGS 4390

**FIN-2 Priorizar a entrega dos 27 pedidos pendentes** (aprovada)

Prefeitura só paga na entrega: os pendentes seguram a receita e geram multa (10% + 0,1%/dia). Destravá-los é a maior alavanca de caixa de curto prazo.

Hipóteses:
- Lucro = preço praticado − custo direto (já inclui mão de obra e impostos, segundo o cliente)
- Dias de atraso e a causa de cada pendente não constam da planilha

Fontes: pendentes; multa_pendentes; aba Pedidos por Mês

**FIN-3 Reduzir a produção do elétrico para aliviar caixa (alternativa avaliada)** (reprovada)

O cliente aceita reduzir o elétrico se for preciso para estabilizar a empresa. Corte de 50% por 12 meses: compara o lucro perdido com o capital que deixa de ficar parado no inversor.

Hipóteses:
- Capital liberado = metade do capital em trânsito do inversor (60 dias de lead time)

Revisor:
- lucro perdido em 12 meses (R$ 12,156,697) supera o capital liberado (R$ 1,960,000); o elétrico tem o maior lucro por ônibus

Fontes: margem_por_modelo; leadtime_criticos

**FIN-4 Revisar a remuneração da diretoria (-20%)** (condicional)

A diretoria (5 pessoas) custa R$ 383.052/mês. 25.5% da folha.

Hipóteses:
- Redução de 20% é cenário, não recomendação fechada

Revisor:
- Parecer jurídico: irredutibilidade salarial (CLT) e vínculo da diretoria (CLT ou estatutário)

Fontes: folha; aba Folha e Absenteísmo

**OPE-1 Operar em 2 turnos (3º turno só nos picos) e dimensionar o quadro de operadores** (condicional)

Com 2 turnos a linha comporta 59 veículos/mês contra pico de 46. Excedente de operadores: 10 (equipe de 4 por estação, conservador), 29 (3, central), 48 (2). Realocar para manutenção e qualidade antes de desligar; demitir só o que sobrar.

Hipóteses:
- Pessoas simultâneas por estação desconhecidas: 4 (conservador), 3 (central), 2 (otimista)
- Ocupação produtiva de 75% e 20% extra para manutenção das máquinas de segunda mão
- Rescisão = 2.8 salários base (aviso, multa de 40% do FGTS, 13º e férias proporcionais)
- Quadro calculado pela carga de trabalho, não por escala de turno: validar a escala real
- Capacidade teórica: não considera paradas das máquinas de segunda mão

Revisor:
- rescisão de R$ 112,801 com caixa zero: indicar fonte; retorno em 1.9 meses

Fontes: cenario_turnos; capacidade_linha; folha; aba Linha de Montagem; aba Folha e Absenteísmo

**OPE-2 Manutenção preventiva e padrão de trabalho nas etapas 20, 50 e 60** (aprovada)

As três etapas com refugo/retrabalho acima de 5% concentram a maior parte das horas perdidas. Meta: cortar 50% delas, usando operadores realocados da OPE-1.

Hipóteses:
- Custo/hora do operador e equipe de 3 por estação (premissas)
- Ganho financeiro direto é pequeno: o retrabalho é 4% do ciclo; o ganho maior é entregar no prazo

Fontes: qualidade_linha; aba Linha de Montagem

**SUP-1 Comprar as peças longas no ato do pedido firme (ar-condicionado 45 d, portas 30 d, inversor 60 d)** (aprovada)

Alinhar o calendário de compras à carteira firme. sem estoque especulativo (cliente: estocar é inviável). Cada dia de atraso evitado nos pendentes poupa R$ 28.073 de multa.

Hipóteses:
- Antecipar as compras evita 15 dias de multa diária (hipótese)
- O capital em trânsito já existe no ciclo atual: nenhuma peça é estocada

Fontes: leadtime_criticos; multa_pendentes; aba Catálogo de Peças

**SUP-2 Cotar alternativas para ar-condicionado (Thermo King) e portas (Bode)** (aprovada)

São as peças com maior lead time depois do inversor e as únicas importadas que o cliente permite trocar (aviso de 30 dias). Cotar fornecedores nacionais ou com menor prazo; a troca só vale se reduzir prazo ou custo.

Hipóteses:
- Sem cotação real, o ganho não é somado ao plano; exposição cambial mostrada como risco

Fontes: leadtime_criticos; sensibilidade_cambio; BCB SGS 1 e 21619

**SUP-3 Elétrico só contra pedido firme e negociar pagamento do inversor na entrega** (aprovada)

O inversor/bateria (R$ 480 mil. 60 dias. sem produtor nacional) prende cerca de R$ 3.920.000 em trânsito. Condição de pagamento da CATL não informada; é a negociação a abrir.

Hipóteses:
- Capital liberado possível, não somado ao plano (depende da negociação)

Fontes: leadtime_criticos; aba Catálogo de Peças

**MER-1 Priorizar a venda dos modelos de maior lucro por ônibus (frotas sequenciais para prefeituras)** (aprovada)

O lucro por ônibus varia de R$ 109 mil (micro) a R$ 496 mil (elétrico). Cada ônibus a mais por mês do rodoviário vale R$ 439 mil de lucro bruto por mês; é sensibilidade, não previsão.

Hipóteses:
- Demanda fora de Santa Maria não existe na planilha: o potencial vem da pesquisa externa (modo LLM)
- Não somado ao plano: depende de novos contratos

Fontes: oportunidades_mercado; margem_por_modelo

**MER-2 Fase 2: double-deck e novos segmentos** (aprovada)

Fora do horizonte financeiro: o cliente quer primeiro a empresa no verde.

Fontes: respostas do cliente

## Projeção de 12 meses (proxy de caixa)

Saldo mínimo R$ 1.017.779; saldo em 12 meses R$ 15.852.553. Entradas pontuais somadas: R$ 7.493.868; desembolsos: R$ 112.801.

| Mês | Lucro bruto base | Melhorias | Pontual | Dividendos | Saldo acumulado |
|---|---|---|---|---|---|
| 1 | R$ 4.363.131 | R$ 0 | R$ 421.092 | R$ 3.766.443 | R$ 1.017.779 |
| 2 | R$ 4.363.131 | R$ 0 | R$ 7.072.776 | R$ 3.766.443 | R$ 8.687.242 |
| 3 | R$ 4.363.131 | R$ 76.610 | R$ -112.801 | R$ 3.766.443 | R$ 9.247.739 |
| 4 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 9.981.607 |
| 5 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 10.715.476 |
| 6 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 11.449.344 |
| 7 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 12.183.212 |
| 8 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 12.917.080 |
| 9 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 13.650.948 |
| 10 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 14.384.816 |
| 11 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 15.118.685 |
| 12 | R$ 4.363.131 | R$ 137.181 | R$ 0 | R$ 3.766.443 | R$ 15.852.553 |
