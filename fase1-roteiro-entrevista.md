# Fase I — Roteiro de Entrevista com o Cliente

**Cenário:** Caxias Heavy Industries — indústria de ônibus em crise
**Entrevistador:** Consultor (único canal de comunicação com o cliente)
**Objetivo:** coletar regras de negócio, restrições financeiras/operacionais e objetivos estratégicos que a planilha não responde.

> Cada pergunta indica a aba/dado da planilha que a motivou (entre colchetes), para o Consultor saber o que está tentando fechar. **P0** = imprescindível (se o tempo for curto, fazer só estas).

---

## 1. Objetivos e Mandato

1. **(P0)** Qual é a meta principal da reestruturação: reverter o déficit operacional, gerar caixa, reduzir dívida, preservar empregos, retomar dividendos? Em que ordem de prioridade?
2. **(P0)** Qual o horizonte de tempo para ver resultado (3, 6, 12 meses)? Há algum evento com data (vencimento de dívida, audiência judicial, assembleia)?
3. Existe uma meta numérica (ex.: margem mínima, redução de custo em %, caixa mínimo)?
4. O que a empresa **não** aceita mexer (demissões, fornecedores específicos, modelos do portfólio, certificações)?
5. O que o cliente espera receber de nós: diagnóstico, plano de ação priorizado, simulações de cenário, ou uma ferramenta que continue rodando?

## 2. Situação Financeira e Passivos

*[Aba Dividendos e Passivos]*

6. **(P0)** Qual a posição de caixa atual e a necessidade mensal de caixa para operar? Há linha de crédito disponível?
7. **(P0)** A planilha mostra dividendos/JCP "suspensos" (ações ON) e "acumulados em atraso" (ações PN), e em Out/26 uma "exigência judicial dos minoritários". Qual o valor e o prazo da exigência judicial? Há risco de bloqueio de contas/ativos?
8. Qual é o saldo total de dívida (curto e longo prazo), com credores, taxas e covenants? A aba trata de dividendos, mas fala em "amortização de dívidas" — onde estão esses dados?
9. A suspensão dos dividendos ON e o atraso dos PN foram deliberados em assembleia? Quanto desse passivo precisa ser pago, e quanto pode ser renegociado ou parcelado?
10. Os valores de JCP na planilha usam 15% do dividendo. Essa é a regra tributária/contratual aplicada, ou uma simplificação?
11. **Inadimplência:** o enunciado cita inadimplência como ponto crítico, mas não há dados de contas a receber na planilha. Quanto da carteira está inadimplente? Quais clientes, prazos médios de recebimento, e qual a política de cobrança/crédito?
12. Há capital de giro travado em estoque (peças importadas, baterias) ou em pedidos "Em Produção"?

## 3. Carteira de Pedidos e Mercado

*[Abas Pedidos por Mês e Modelos de Ônibus]*

13. **(P0)** A carteira tem pedidos "Pendente / Atrasado" nos últimos meses (ex.: Out/26). Qual a causa — falta de peça, refugo, gargalo, falta de pessoal, falta de pagamento do cliente? Há multa contratual por atraso?
14. Quem são os clientes (prefeituras, operadoras de BRT, frotistas, fretamento)? Há concentração em poucos clientes ou em contratos públicos/licitações?
15. Os pedidos têm adiantamento/sinal? Em que momento a empresa fatura e recebe (na encomenda, na produção, na entrega)?
16. Qual a capacidade nominal da fábrica (ônibus/mês)? Hoje opera com quanto de ocupação?
17. Qual a margem **real** por modelo? A planilha traz a margem teórica (custo direto vs. preço); o custo direto inclui mão de obra, refugo, frete e impostos?
18. Há modelos que a empresa aceitaria descontinuar ou priorizar (ex.: elétrico, articulado, micro)? O elétrico exige bateria importada de ~R$ 480 mil: ele é estratégico ou consome caixa?
19. Os preços de venda são reajustáveis (cláusula de reajuste em contrato)? Há espaço para repassar aumento de custo ao cliente?

## 4. Produção, Gargalos e Qualidade

*[Aba Linha de Montagem]*

20. **(P0)** A planilha aponta três estações críticas: **Armação da Estrutura** (etapa 20, refugo 5,8%), **Montagem de Vidros** (etapa 50, 7,4%) e **Instalação Elétrica** (etapa 60, 8,9%). Os senhores concordam com esse diagnóstico? Existe outra estação que sentem como problema e não aparece como crítica?
21. **(P0)** Qual é o **custo de um refugo/retrabalho** em cada uma dessas etapas (material perdido, horas, parada de linha)? Existe um registro do custo da não qualidade?
22. Quais são as causas conhecidas: robô ABB desregulado, material fora de especificação, treinamento, manutenção? A manutenção é preventiva ou corretiva? Há dados de paradas de máquina?
23. A linha trabalha em quantos turnos? Há horas extras para compensar atrasos?
24. Os dados de refugo/retrabalho de 180 dias estão disponíveis em detalhe (por lote, por modelo, por turno)? Podem ser fornecidos?
25. Peças refugadas são descartadas, retrabalhadas ou devolvidas ao fornecedor com crédito? Há garantia contratual?
26. Existe sistema (ERP/MES/CLP) de onde os dados saem? Seria possível a solução consumir esses dados de forma automática, ou o fluxo será por planilha?
27. Há indicadores de qualidade pós-entrega (garantia, recall, reclamação de cliente)?

## 5. Suprimentos e Fornecedores

*[Abas Catálogo de Peças e Lista de Materiais (BOM)]*

28. **(P0)** Quais peças causam paradas por falta ou atraso? Os lead times da planilha (ex.: bateria 60 dias, ar-condicionado 45 dias, portas 30 dias) são reais ou há atrasos além disso?
29. Existem fornecedores alternativos homologados para peças críticas (vidros, chicote elétrico, ar-condicionado)? Há restrição de homologação (cliente exige marca)?
30. Qual a exposição cambial? Peças de EUA, China e Alemanha são cotadas em dólar/euro? Há hedge?
31. Há contratos de longo prazo, volume mínimo ou exclusividade com fornecedores? Qual a condição de pagamento (prazo, antecipado)?
32. Qual política de estoque é usada (estoque de segurança, just-in-time, compra por pedido)? Qual o valor do estoque parado?
33. A BOM da planilha cobre apenas 3 dos 5 modelos (faltam **Urbano Articulado** e **Micro-ônibus**). A BOM completa está disponível? A planilha de peças tem 12 itens: o catálogo completo é maior?
34. O custo da BOM inclui frete, impostos de importação e perda esperada (scrap)?

## 6. Pessoas e Folha de Pagamento

*[Aba Folha e Absenteísmo]*

35. **(P0)** A planilha mostra 86 operadores, 31 analistas, 13 gestores e 5 diretores. O absenteísmo é concentrado em algum perfil, turno ou estação? Qual a causa conhecida (saúde, transporte, clima, atestados)?
36. Qual o custo de uma falta (parada de linha, hora extra, substituição, temporário)?
37. Os encargos de 45% sobre o salário são o total real (incluindo benefícios, FGTS, provisões)?
38. Há restrição de acordo coletivo/sindicato para redução de jornada, banco de horas, demissão ou terceirização? Existe estabilidade assegurada?
39. A estrutura gerencial (13 gestores) e a diretoria (5) são consideradas parte do problema ou fora de escopo?
40. A fórmula de absenteísmo da planilha usa 0,714 (5/7 dias). A empresa adota esse critério ou há outro padrão interno?

## 7. Restrições, Dados e Uso da Solução

41. **(P0)** Quais ações a solução **pode recomendar** e quais ela **nunca** pode propor (ex.: demissão em massa, troca de fornecedor, venda de ativos, renegociação de contrato)?
42. Quem aprova as recomendações e em qual alçada? O processo exige validação humana antes de qualquer ação (relevante para o desenho Human-in-the-Loop vs. multiagentes)?
43. Podemos usar **informações externas** na análise (preço de aço/alumínio, câmbio, benchmarks do setor, notícias de licitações e editais)? Há alguma fonte oficial que o cliente prefira?
44. Os dados da planilha são completos e atuais? Existe algo conhecido como incorreto, estimado ou desatualizado?
45. Existem dados confidenciais que não devem aparecer no relatório e na apresentação (nomes, valores, clientes)?
46. Como o cliente avaliará o sucesso da entrega — quais métricas finais ele quer ver (R$ economizados, % de refugo, dias de atraso, caixa liberado)?

---

## Lacunas da base de dados já identificadas (para o Consultor fechar na entrevista)

| Lacuna | Perguntas |
|---|---|
| Sem dados de contas a receber / inadimplência | 11, 15 |
| Sem saldo de caixa nem posição de dívida | 6, 8, 9 |
| Sem custo da não qualidade (refugo/retrabalho em R$) | 21, 24, 25 |
| BOM incompleta (faltam BUS-URB-ART e BUS-MIC-09M) | 33 |
| Causa do status "Pendente / Atrasado" não informada | 13 |
| Sem detalhe de causa de absenteísmo / turnos | 35, 36 |
