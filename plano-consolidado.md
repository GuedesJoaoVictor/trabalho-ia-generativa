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

## Pareceres dos agentes (modo LLM)

### Financeiro

Com base na análise dos dados financeiros da Caxias Heavy Industries, apresento as 3 recomendações prioritárias para a recuperação da empresa e a regularização dos dividendos:

1. **Priorizar a entrega dos 27 pedidos em atraso:** O fluxo de caixa é gerado apenas na entrega. Atualmente, há R$ 28.072.776,15 parados em pedidos pendentes, sujeitos a uma multa fixa de **R$ 2.807.277,61** mais 0,1% ao dia sobre o valor da receita. A conclusão imediata desses pedidos é fundamental para estancar a perda de margem e garantir o caixa necessário para os dividendos.
   * *Origem:* `pendentes`

2. **Focar a produção no "Rodoviário Premium DD 14m":** Este modelo apresenta a maior margem praticada (32,29%), superando significativamente o Urbano Standard (25,75%) e o Elétrico (25,50%). Maximizar a produção do modelo de maior rentabilidade é a estratégia mais rápida para colocar a empresa no verde sem a necessidade de novos investimentos em P&D ou alteração de fornecedores.
   * *Origem:* `margem_por_modelo`

3. **Regularização estruturada do passivo de dividendos:** O passivo total é de **R$ 33.300.000,00**. Considerando o lucro mensal de R$ 4.363.130,76 (apenas de pedidos entregues), a empresa deve instituir uma saída mensal que combine o pagamento corrente (R$ 2.775.000,00) com a amortização do passivo em atraso, evitando novos bloqueios pela B3. (Hipótese: *a empresa precisará sacrificar parte do lucro operacional para equalizar esse fluxo, uma vez que o caixa é atualmente zero*).
   * *Origem:* `passivo_dividendos`, `fluxo_base`

### Operações

Para atingir a meta de regularização financeira em 12 meses, as operações da Caxias Heavy Industries devem focar na otimização do gargalo, mitigação de desperdícios de qualidade e controle da massa salarial.

Aqui estão as 3 recomendações prioritárias:

1.  **Desengarar a Etapa de Pintura e Tratamento Anticorrosivo (Etapa 30):** Esta etapa limita a capacidade máxima da fábrica em **88,67 veículos/mês**. Como a demanda de pico é de 46 veículos, a operação está subutilizada. Recomenda-se realizar manutenção preventiva intensiva ou reorganização do layout para elevar essa capacidade e evitar o "estouro" de prazos em contratos futuros, garantindo o recebimento das prefeituras.
    *   *Fonte:* `capacidade_linha`

2.  **Redução do Refugo na Instalação Elétrica (Etapa 60):** Com um índice de refugo de **8,9%** e custo de retrabalho que impacta diretamente a margem, esta etapa é a mais crítica da qualidade. Como não é possível trocar o chicote Yazaki, a diretriz é implementar um treinamento técnico rigoroso com a equipe desta estação para reduzir as **0,4895 horas perdidas por veículo** nesta etapa, preservando o caixa atual.
    *   *Fonte:* `qualidade_linha`

3.  **Gestão do Absenteísmo no Nível Operacional:** O nível operacional apresenta um índice de absenteísmo de **5,5%** (608 faltas), elevando o custo médio mensal dessa folha para **R$ 502.366,36**. Recomenda-se a revisão do modelo de turnos e incentivos de produtividade vinculados à assiduidade para reduzir esse custo e proteger a liquidez, dado o cenário de caixa zero.
    *   *Fonte:* `folha`

***Nota:** As recomendações sobre o impacto no fluxo de caixa e os tempos de treinamento são tratadas como hipóteses de gestão, pois não foram devolvidas diretamente pelas ferramentas.*

### Suprimentos

Com base na análise dos dados de suprimentos e na situação crítica de caixa da Caxias Heavy Industries, seguem as três recomendações prioritárias para garantir a continuidade operacional e a viabilidade financeira:

1. **Quitar Pendências Imediatas para Estancar Multas:** A empresa possui 27 unidades pendentes com um valor de multa fixa de **R$ 2.807.277,61** e um acréscimo diário de **R$ 28.072,77**. Dado que o lucro dessas unidades é de **R$ 7.072.776,15**, priorizar a entrega destas unidades é a única forma de obter fluxo de caixa positivo imediato para aliviar a crise e evitar o agravamento da dívida contratual (*Fonte: `pendentes`*).

2. **Gestão de Capital de Giro no Estoque de Elétricos:** O inversor de potência e bateria (`PEC-ELE-402`) da China possui o maior lead time (60 dias) e consome **R$ 1.960.000,00** mensais em capital parado (*Fonte: `leadtime_criticos`*). Como este item é essencial para o modelo elétrico e não pode ser substituído, a empresa deve suspender a produção de novos modelos elétricos excedentes à demanda contratada para liberar capital de giro, focando apenas no que está vendido, dada a necessidade de caixa zero.

3. **Proteção contra Volatilidade Cambial (Hedge):** 69,9% dos custos de peças são importados. Uma variação de 10% no câmbio gera um impacto negativo de **R$ 244.662,50** extras por mês nos custos (*Fonte: `sensibilidade_cambio`*). Como a empresa não tem margem de erro, é recomendável estabelecer contratos de câmbio futuro para as importações críticas (Inversor/Bateria e Ar Condicionado) a fim de blindar o lucro operacional necessário para a regularização dos dividendos em 12 meses (*Hipótese: baseada no risco de exposição cambial identificado*).

### Coleta Externa

Com base na análise de viabilidade financeira e operacional da Caxias Heavy Industries, considerando o cenário de caixa zero e a dependência de componentes importados, aqui estão as 3 recomendações prioritárias:

1.  **Dolarização dos Contratos de Fornecimento e Repasse:** Com o USD a **5.4935 (ferramenta: cotacoes_bcb)**, a empresa deve negociar cláusulas de reajuste automático nos contratos com as prefeituras vinculadas à variação cambial. Como o pagamento só ocorre na entrega e o inversor é chinês, a margem de lucro está em risco iminente de erosão cambial.
2.  **Mitigação do Custo do Capital de Giro:** Dada a Selic de **13.75 (ferramenta: cotacoes_bcb)**, a empresa deve evitar financiamentos bancários de curto prazo para cobrir o "buraco" de caixa entre o início da produção e o recebimento das prefeituras. *Hipótese: Recomenda-se buscar antecipação de recebíveis via FIDC com as prefeituras para minimizar o impacto dos juros compostos em atrasos ou necessidades operacionais.*
3.  **Priorização de Eficiência sobre Inovação (Otimização da Cadeia):** Com o custo de substituição de fornecedores travado pelo aviso prévio de 30 dias e a impossibilidade de trocar o chicote Yazaki, a prioridade é a gestão de estoque *just-in-time* rigorosa. *Hipótese: Como a empresa precisa estar no verde em 12 meses e o IPCA está em 0.82 (ferramenta: cotacoes_bcb), a estratégia é focar na produção de modelos atuais com margem positiva, suspendendo permanentemente gastos com P&D e projetos Double-Deck até a estabilização do fluxo de caixa.*

### Mercado

Como Agente de Mercado para a Caxias Heavy Industries, apresento o diagnóstico de oportunidades baseado nos dados oficiais coletados.

Considerando nossa restrição de caixa zero e a necessidade de regularizar dividendos em 12 meses, as oportunidades identificadas focam em financiamento federal que garante liquidez na entrega, mitigando o risco de inadimplência municipal.

### Oportunidades Identificadas

| Oportunidade | Detalhes | Fonte |
| :--- | :--- | :--- |
| **Projeto E-BUS POA (Porto Alegre)** | Licitação para 100 ônibus elétricos com orçamento de R$ 447,7 milhões via BNDES (Fundo Clima/Novo PAC). | [Prefeitura de Porto Alegre](https://prefeitura.poa.br/smmu/noticias/prefeitura-inicia-consulta-de-precos-para-aquisicao-de-100-onibus-eletricos) |
| **Linha FINAME (BNDES)** | Apoio direto à eletrificação de frotas municipais. O crédito é operacionalizado via instituições financeiras parceiras. | [BNDES Cidades](https://cidades.bndes.gov.br/solucao/eletrificacao-da-frota-ate-100/) |

### Análise Estratégica para a Caxias Heavy Industries

1.  **Prioridade E-BUS POA:** Esta é a oportunidade imediata. A consulta pública aberta em 04/11/2026 exige respostas até 25/11/2026. Como o financiamento do BNDES é via Fundo Clima/PAC, o risco de crédito é minimizado, pois o pagamento ocorre na entrega (conforme nossas restrições de fluxo).
2.  **Adequação Técnica:** Manteremos o inversor de origem chinesa conforme permitido pela diretriz atual. O uso de chicotes Yazaki, por não poderem ser trocados, deve ser validado tecnicamente na engenharia de integração com o motor elétrico para garantir a conformidade com as exigências da licitação de Porto Alegre.
3.  **Restrições Operacionais:**
    *   *P&D e Double-Deck:* **Congelados.** Não há margem para desvios de recursos antes do atingimento da meta de 12 meses.
    *   *Fornecedores:* Qualquer alteração necessária para atender à viabilidade técnica do E-BUS deverá ser notificada imediatamente para respeitar o aviso prévio de 30 dias.

### Hipóteses de Mercado (Não confirmadas por dados da busca)
*   **Demanda Escolar/Micro:** *Hipótese:* Com o foco no "Novo PAC", municípios menores do RS devem buscar renovação de frota escolar via adesão a atas de registro de preços federais. A Caxias Heavy Industries deve monitorar o portal do FNDE para futuras demandas de ônibus rurais/escolares, que possuem menor complexidade tecnológica que os elétricos e margens mais estáveis.
*   **Capacidade de Entrega:** *Hipótese:* A capacidade produtiva atual da empresa pode ser insuficiente para atender aos 100 veículos de Porto Alegre sozinha; parcerias estratégicas (consórcios) podem ser necessárias para não comprometer o cronograma de entrega e o recebimento dos valores.

### Revisor

Como Revisor, analisei o plano para a Caxias Heavy Industries. O plano apresenta inconsistências críticas que violam as diretrizes de viabilidade financeira e restrições impostas.

### 1. Violações de Restrições e Contradições
*   **Violação de Caixa Zero:** A ação `OPE-1` prevê um custo de rescisão de **R$ 112.800,79** (hipótese) para atingir economia de pessoal, mas não aponta a fonte de liquidez. Com caixa zero, qualquer desembolso sem receita imediata é inviável.
*   **Contradição sobre P&D:** A ação `MER-2` menciona "Double-deck" como fase 2, mas a estratégia `MER-1` sugere focar em modelos de maior lucro. O custo de oportunidade de P&D não foi calculado, criando um risco de desvio de foco e caixa para algo que o cliente proibiu até estar no verde.
*   **Risco B3 vs. Caixa:** O plano `FIN-1` compromete **R$ 3.766.443,44** mensais (corrente + atrasados) para evitar o bloqueio da B3. Dado que as prefeituras só pagam na entrega (o que pode levar mais de 60 dias de *lead time*), existe um descasamento temporal (gap) de liquidez severo que não foi mitigado.

### 2. Números sem Fonte/Hipóteses Críticas
*   **R$ 2.807.277,61 (FIN-2):** O valor da "multa fixa" carece de fundamentação contratual clara na base fornecida.
*   **Custos de rescisão (OPE-1):** O cálculo de "2.8 salários base" para rescisão é uma **hipótese**. Sem o custo exato de cada rescisão CLT, o *payback* de 1.9 meses não é confiável.
*   **Lucro dos Pendentes (FIN-2):** O valor de **R$ 7.072.776,15** como lucro dos 27 pedidos é uma **hipótese** que pressupõe que o custo direto fornecido pela empresa está correto e não será majorado por ineficiências na linha.

### 3. Diagnóstico de Riscos
*   **Chicote Yazaki:** Respeitado (Nenhuma ação propõe a troca).
*   **Inversor da China:** O plano `SUP-1` corretamente mantém a dependência, mas o custo de **R$ 3.920.000,00** em capital parado (trânsito) é um dreno insustentável para uma empresa com caixa zero.
*   **Aviso de 30 dias:** A ação `SUP-2` busca alternativas para ar-condicionado e portas, respeitando o aviso de 30 dias, mas a ausência de cotações reais torna o impacto financeiro nulo no momento.

### 4. Recomendações do Revisor
1.  **Suspender `OPE-1`:** Com caixa zero, não há orçamento para pagar rescisões de R$ 112 mil. A realocação deve ser interna e custo zero.
2.  **Negociar com a B3:** O passivo de dividendos de **R$ 22.500.000,00** é o maior risco. Propor a quitação apenas *após* a entrada da receita dos 27 pedidos pendentes (**R$ 28.072.776,15**).
3.  **Prioridade Financeira:** A única fonte de oxigênio é a entrega dos 27 pedidos. O financeiro deve condicionar os pagamentos de dividendos à confirmação do recebimento da prefeitura, não a um cronograma mensal fixo, devido à instabilidade do fluxo de caixa.

**Status:** Plano sob revisão. Necessária validação jurídica sobre o vínculo da diretoria e a possibilidade de renegociação dos dividendos com a B3 antes de qualquer desembolso.

