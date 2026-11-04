# Resumo para o grupo: o que foi feito e o que vale entrar no relatório

Prazo: **04/11/2026, 23:55**. Este documento é um briefing, não texto de relatório. A redação, a interpretação e as referências são de vocês (regra 4.1 do enunciado).

## 1. O que existe no repositório

| Parte | Arquivos | Como usar |
|---|---|---|
| Fase I (entrevista) | `fase1-*.md`, `respostas-professor.md`, `respostas-complementares-professor.md` | Material para a seção "Resultados da entrevista" |
| Análise dos dados | `analise_planilha.py` → `resultados-analise.md` | `python3 -I analise_planilha.py > resultados-analise.md` |
| Sistema multiagentes | `dados.py`, `ferramentas.py`, `agentes.py`, `executar.py`, `figuras.py` | `.venv/bin/python executar.py` gera `plano-consolidado.md`, `plano.json`, `figuras/` |
| Teste | `test_sistema.py` | `.venv/bin/python test_sistema.py` deve imprimir `ok` |
| Arquitetura (decisão) | `arquitetura-agentes.md` | Papéis, ferramentas, regras de validação |
| Apresentação | `apresentacao/apresentacao.tex` (13 slides) | `cd apresentacao && latexmk -xelatex apresentacao.tex` |
| Roteiro e perguntas | `apresentacao/roteiro-e-perguntas.md` | Tempo por slide e 14 perguntas prováveis |
| Esqueleto do relatório | `relatorio/relatorio.tex` (abnTeX2, sem texto) | `cd relatorio && latexmk -pdf relatorio.tex` |
| Tabelas prontas | `relatorio/tabelas/*.tex` | `.venv/bin/python gerar_tabelas.py` |
| Conferidor de números | `conferir_relatorio.py` | `.venv/bin/python conferir_relatorio.py relatorio/relatorio.tex` |
| Apoio | `mapa-evidencias-relatorio.md`, `fontes-figuras.md`, `guia-conceitos.md` | Onde está cada evidência, fonte de cada figura, explicação dos conceitos |

## 2. Resultados principais (todos recalculados em código)

- Carteira de 12 meses: R$ 273,9 mi, 320 ônibus. Lucro bruto das entregas: R$ 4,36 mi/mês.
- Dividendos em 12 meses: R$ 33,3 mi (R$ 22,5 mi exigíveis, R$ 10,8 mi de ON suspensos). Plano: R$ 3,77 mi/mês, com atrasados em 24 meses corrigidos pela Selic (R$ 1,29 mi).
- Cobertura (lucro bruto / dividendos): 1,16x sem plano, 1,19x com plano.
- 27 pedidos pendentes = R$ 28,07 mi de receita e R$ 7,07 mi de lucro; multa de R$ 2,81 mi mais R$ 28 mil/dia.
- Capacidade teórica 89 ônibus/mês (3 turnos) e 59 (2 turnos), contra pico de pedidos de 46.
- Refugo: 4% do tempo de ciclo; 71% dos ônibus passam sem retrabalho.
- Plano: 11 propostas, 1 reprovada (reduzir o elétrico), 2 condicionais (diretoria −20%, quadro de operadores).

## 3. O que vale entrar no relatório

### A linha de raciocínio que os dados sustentam
1. O problema central é **cobertura de caixa e entrega**, não falta de capacidade produtiva nem refugo. O lucro bruto mal cobre os dividendos e 27 pedidos presos seguram a receita.
2. O gargalo real está **fora da linha** (fornecedores e paradas de máquina). A planilha chama de "gargalo" as etapas de maior refugo, mas pela capacidade teórica a linha comporta a demanda.
3. Um **Revisor independente** é o que dá confiabilidade: recalcula do zero, aplica as regras do cliente e vetou uma proposta atraente (reduzir o elétrico).

Esses três pontos são o que diferencia o trabalho de uma análise genérica. Construam as seções em volta deles.

### Por seção do enunciado

| Seção | O que vale incluir | Evidência |
|---|---|---|
| Introdução | A empresa, o problema (déficit, dividendos atrasados, pedidos pendentes), o objetivo, e a escolha por multiagentes | `resultados-analise.md`, `arquitetura-agentes.md` |
| Embasamento teórico | Os quatro temas do enunciado, ligados ao que o sistema faz. **Dizer que RAG não foi implementado e que não há solver de otimização.** | `guia-conceitos.md` |
| Entrevista | O que o cliente disse que **mudou decisões**: carta branca, caixa zero, dividendos atrasados em 24 meses, chicote e inversor não trocáveis, elétrico mantido, double-deck e P&D na fase 2, inadimplência não é problema | `respostas-*.md` |
| Arquitetura | Diagrama (figura 01), papel de cada agente, ferramentas, as regras do Revisor e a prova no `test_sistema.py`. Por que multiagentes e não agente único com aprovação humana | `arquitetura-agentes.md`, `figuras/01` |
| Análise dos dados | Margens (02), carteira (03), capacidade (04), refugo (05), lead time (06), folha e absenteísmo, dividendos | `fontes-figuras.md`, `relatorio/tabelas/` |
| Soluções e impacto | Tabela de propostas com parecer, projeção de 12 meses (07), a proposta reprovada **e o motivo**, as condicionais e o que depende de validação | `plano-consolidado.md` |
| Conclusão | Resultado, limitações e próximos passos (fase 2) | Seção 4 abaixo |

### Pontos fortes para destacar
- Todos os números saem de funções (`ferramentas.py`); o LLM não calcula.
- Premissas explícitas e marcadas (`PREMISSAS`), com sensibilidade quando há incerteza (operadores: 10, 29 ou 48).
- Dado externo real e datado (Banco Central, consulta de 03/11/2026).
- O Revisor rejeita propostas, o que mostra que a validação funciona.

### O que deixar de fora ou tratar com cuidado
- **Não apresentar o saldo de R$ 15,9 mi como caixa.** É proxy: lucro bruto menos dividendos.
- **Não chamar os agentes de "agentes LLM"** sem ressalva: nos resultados eles são funções Python. O modo com Claude existe, mas nunca foi executado com sucesso (a chave de teste foi recusada).
- Não afirmar demanda de mercado fora de Santa Maria: não há dado.
- Não incluir inadimplência como achado: o cliente disse que não é problema.
- Tratar rescisão (2,8 salários), multa (0,1%/dia) e pessoas por estação como **hipóteses**.

## 4. Limitações (para a conclusão)
Saldo é proxy · capacidade é teórica, sem paradas de máquina · BOM cobre 3 dos 5 modelos e não traz o chassi · dias de atraso por pedido e custo em R$ do refugo não existem na planilha · juros e multa dos dividendos não informados · dividendos ON suspensos fora da quitação · modo LLM não validado · sem RAG e sem solver.

## 5. Divisão sugerida de escrita (ajustem como quiserem)

| Quem | Seções |
|---|---|
| Iuri (Consultor) | Introdução, resultados da entrevista, conclusão |
| Bruno Muniz | Análise dos dados, fontes das figuras |
| Davi | Arquitetura do sistema e validação |
| Diogo e Novak | Soluções e impacto, tabelas |
| João Guedes (Scrum) | Embasamento teórico, referências, formatação MDT, integração do texto |

## 6. Antes de entregar
- [ ] Rodar `conferir_relatorio.py` no texto final e checar cada número sinalizado.
- [ ] Legenda e fonte em toda figura e tabela; remover os `% TODO` do `.tex`.
- [ ] Referências reais, conferidas uma a uma (as citadas em `guia-conceitos.md` são comuns na área, mas confirmem os dados).
- [ ] Formatação pelo **MDT UFSM vigente**; o esqueleto usa o padrão ABNT.
- [ ] Testar o modo `--llm` com chave válida da Anthropic (`sk-ant-...`), se quiserem afirmar que os agentes usam LLM.
- [ ] Cronometrar a apresentação (`apresentacao/roteiro-e-perguntas.md`).
- [ ] Enviar relatório e apresentação antes de 04/11, 23:55.
