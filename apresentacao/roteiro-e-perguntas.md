# Roteiro da apresentação e perguntas prováveis

Tempo-base: 10 minutos (ajustem se o professor definir outro). Preencham quem fala. O Consultor abre e fecha.

## Roteiro por slide

| # | Slide | Tempo | Quem | A ideia a passar |
|---|---|---|---|---|
| 1 | Capa | 0:15 | Consultor | Quem somos, o que entregamos |
| 2 | Equipe | 0:30 | Scrum Master | Cada papel e o que fez |
| 3 | Sem folga | 1:00 | | 1,16x de cobertura com caixa zero |
| 4 | Margem | 0:40 | | Todos dão lucro; elétrico dá mais por ônibus |
| 5 | Pendentes | 0:50 | | 27 ônibus, R$ 28 mi, prefeitura paga na entrega |
| 6 | Capacidade | 0:50 | | O gargalo está em fornecedor e máquina, não no ciclo |
| 7 | Refugo | 0:30 | | Importa pouco no caixa |
| 8 | Fornecedores | 0:40 | | Inversor: 60 dias, R$ 3,9 mi em trânsito |
| 9 | Arquitetura | 1:00 | | Orquestrador, 5 agentes, Revisor com veto |
| 10 | Revisor | 1:00 | | Regras do cliente e o exemplo do elétrico |
| 11 | Plano | 1:00 | | 11 propostas, 1 reprovada, 2 condicionais |
| 12 | Resultado | 0:50 | | 1,16x → 1,19x, saldo mínimo R$ 1,0 mi |
| 13 | Limites | 0:45 | Consultor | O que ainda confirmar |

## Perguntas prováveis e respostas baseadas nos dados

**1. O que os agentes LLM fazem de fato?**
No modo que gerou os resultados, os agentes são funções Python determinísticas que usam as ferramentas; o LLM não entrou. O modo com Claude está implementado (`--llm`) mas nunca foi executado. Respondam isso sem rodeio. Se testarem com chave de API antes, atualizem a resposta.

**2. Como sabem que os números estão certos?**
A planilha tem fórmulas sem valor guardado, então recalculamos tudo em código. O Revisor recomputa de novo a partir dos dados brutos e rejeita proposta que diverge mais de 0,5%. `test_sistema.py` confere os números-chave e o comportamento do Revisor.

**3. O saldo de R$ 15,9 mi em 12 meses é caixa real?**
Não. É proxy: lucro bruto das entregas menos dividendos. Não inclui despesas fora do custo direto nem outras dívidas, e o cliente informou caixa zero. O número útil é a cobertura (1,19x) e o saldo mínimo do mês 1.

**4. Por que reprovaram reduzir o elétrico, se o cliente aceita?**
Cortar 50% por 12 meses perde R$ 12,2 mi de lucro e libera cerca de R$ 2,0 mi de capital parado no inversor. A regra do Revisor é que o corte só vale se o capital liberado superar o lucro perdido. O elétrico tem o maior lucro por ônibus (R$ 496 mil).

**5. Por que pagar os atrasados em 24 meses e corrigir pela Selic?**
Os 24 meses vêm do cliente. A Selic é nossa premissa de índice de correção, porque o cliente não informou juros e multa. Consultamos a Selic acumulada no Banco Central; a correção dá R$ 1,29 mi sobre R$ 22,5 mi.

**6. E os dividendos ON suspensos de R$ 10,8 mi?**
Ficaram fora da quitação, a confirmar com o cliente. Se entrarem, a pressão de caixa aumenta.

**7. Quantos operadores demitir?**
Depende de quantas pessoas ficam por estação, que a planilha não informa: 10 (4 por estação), 29 (3) ou 48 (2). A economia vai de R$ 58 mil a R$ 169 mil por mês e a rescisão estimada é 2,8 salários. Por isso a proposta é condicional: realocar antes de desligar, validar a escala real, e há caixa zero para pagar rescisão.

**8. Se a linha comporta 89 por mês e o pico é 46, por que atrasa?**
A capacidade é teórica, só pelo tempo de ciclo. Os atrasos vêm de fornecedores e paradas de máquina de segunda mão, que a planilha não mede. Falta o dado de dias de atraso por pedido.

**9. O gargalo não é a pintura (8 h)?**
É a etapa com maior ciclo, mas com 3 turnos ainda comporta 89/mês. O que a planilha chama de gargalo (etapas 20, 50 e 60) são as de maior refugo, e o retrabalho é só 4% do ciclo.

**10. E inadimplência?**
O cliente disse que não é problema e a planilha não tem esse dado. Os atrasos que existem são de dividendos.

**11. Por que não demitir a diretoria / cortar salários?**
Propusemos reduzir 20% como cenário (R$ 77 mil/mês), mas ficou condicional: depende de parecer jurídico (irredutibilidade salarial na CLT e tipo de vínculo da diretoria).

**12. Por que não trocar o fornecedor do inversor ou do chicote?**
O cliente disse que o chicote Yazaki não é substituível e que não há produtor nacional do inversor da CATL. Só ar-condicionado e portas aparecem como trocáveis, com aviso de 30 dias, e cotamos alternativas sem somar ganho ao plano.

**13. Cadê o double-deck e o P&D?**
Fase 2: o cliente quer primeiro a empresa no verde.

**14. O que fariam com mais tempo?**
Rodar o modo com LLM e validar, obter dias de atraso por pedido, custo real do refugo e paradas de máquina, confirmar juros e multa dos dividendos, e cotar as peças alternativas.

## Ensaio

- Cronometrem uma vez inteira antes. Se passar de 10 minutos, cortem os slides 7 e 8 para uma frase cada.
- Todo número falado deve estar em `plano-consolidado.md` ou `resultados-analise.md`.
