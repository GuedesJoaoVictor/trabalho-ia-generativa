# Mapa de evidências para o relatório (Fase III)

Material de apoio para o grupo: **onde estão os dados, números e figuras** que cada seção do enunciado pede.
Não contém texto do relatório. A redação, a interpretação e as referências são do grupo. Prazo: **04/11/2026, 23:55**.

## 1. Seção do enunciado → evidência disponível

| Seção do relatório | O que o enunciado pede | Onde está o material | O que o grupo ainda precisa fazer |
|---|---|---|---|
| 1. Introdução e contextualização | Empresa, problema central, justificativa | Abas da planilha; [respostas-professor.md](respostas-professor.md); [resultados-analise.md](resultados-analise.md) (carteira, folha, dividendos) | Escrever; levantar dados públicos da empresa, se houver |
| 2. Embasamento teórico | IA generativa e LLMs; single vs multi-agent; prompt engineering, tool use, RAG; otimização e decisão no domínio | O sistema usa tool use (ferramentas.py), multiagentes (agentes.py) e validação por Revisor. RAG não foi implementado | Pesquisar e citar a literatura. As referências precisam ser reais e conferidas pelo grupo |
| 3.1 Resultados da entrevista | Diagnóstico das necessidades do cliente | [fase1-perguntas-complementares.md](fase1-perguntas-complementares.md), [respostas-professor.md](respostas-professor.md), [respostas-complementares-professor.md](respostas-complementares-professor.md), [fase1-roteiro-entrevista.md](fase1-roteiro-entrevista.md) | Sintetizar em texto |
| 3.2 Arquitetura do sistema | Diagrama de fluxo, papel de cada agente, ferramentas externas, regras de validação | [figuras/01_arquitetura.png](figuras/01_arquitetura.png); [arquitetura-agentes.md](arquitetura-agentes.md) (papéis, ferramentas, 6 regras); `agentes.py` função `revisor` (regras reais); API do Banco Central (dados externos) | Descrever; justificar a escolha multiagentes com as respostas do cliente |
| 3.3 Análise dos dados | Planilhas, gargalos, refugo, custos, inadimplência | [resultados-analise.md](resultados-analise.md); figuras 02 a 06 | Interpretar. **Inadimplência:** o cliente informou que não é problema (sem dados na planilha) |
| 3.4 Soluções e impacto | Resultados quantitativos e qualitativos | [plano-consolidado.md](plano-consolidado.md), `plano.json`, figura 07 | Interpretar, discutir as hipóteses de cada proposta |
| 4. Conclusão | Síntese, limitações, recomendações | Seção 3 abaixo (limitações do sistema e dos dados) | Escrever |

## 2. Números-chave e de onde saem

| Dado | Valor | Origem |
|---|---|---|
| Carteira de 12 meses | R$ 273,9 mi, 320 ônibus | `fluxo_base`; resultados-analise.md §3 |
| Lucro bruto das entregas | R$ 4,36 mi/mês | `fluxo_base` |
| Margem por modelo (preço praticado) | 25,5% (elétrico) a 32,3% (rodoviário) | `margem_por_modelo`; figura 02 |
| Pedidos pendentes | 27 ônibus, R$ 28,07 mi; multa fixa R$ 2,81 mi + R$ 28 mil/dia | `pendentes` |
| Dividendos em 12 meses | R$ 33,3 mi (R$ 22,5 mi exigíveis, R$ 10,8 mi suspensos) | `passivo_dividendos` |
| Correção Selic dos atrasados | R$ 1,29 mi (Selic acumulada do Banco Central, consulta de 03/11/2026) | `encargos_atrasados_selic`; `dados_externos.json` |
| Saída mensal de dividendos no plano | R$ 3,77 mi (corrente + atrasados em 24 meses) | `plano_dividendos` |
| Cobertura (lucro bruto / dividendos) | 1,16x sem plano; 1,19x com plano | `consolidar` |
| Capacidade teórica da linha | 89 ônibus/mês (3 turnos); 59 (2 turnos); pico de pedidos 46 | `capacidade_linha`; figura 04 |
| Rendimento de primeira passagem | 71% (29% dos ônibus passam por retrabalho) | `qualidade_linha` |
| Operadores excedentes | 10 (conservador), 29 (central), 48 (otimista) | `cenario_turnos` (premissas) |
| Prazo mínimo pedido→entrega | 62 dias (elétrico); 47 dias (urbano e rodoviário) | `leadtime_criticos` |
| Capital em trânsito do inversor | R$ 3,92 mi | `leadtime_criticos` |
| Exposição cambial (+10%) | R$ 245 mil/mês de custo extra | `sensibilidade_cambio` |

## 3. Limitações e hipóteses (inventário para a conclusão)

- **O "caixa" do plano é um proxy:** lucro bruto das entregas (preço − custo direto) menos dividendos. Não inclui despesas fora do custo direto nem outras dívidas, e o cliente informou caixa zero.
- **Capacidade teórica:** não inclui paradas das máquinas de segunda mão; os atrasos reais indicam que a capacidade efetiva é menor.
- **Operadores:** o número depende de pessoas por estação (desconhecido) e de rescisão estimada em 2,8 salários. O quadro é calculado por carga de trabalho, não por escala de turno.
- **Multa:** supõe 0,1%/dia sobre o valor dos pedidos atrasados; dias de atraso desconhecidos.
- **Selic:** índice de referência assumido; o cliente não informou juros nem multa dos dividendos.
- **Dividendos ON suspensos** (R$ 10,8 mi) ficaram fora da quitação, a confirmar.
- **Custo direto:** a BOM cobre só 3 dos 5 modelos e o chassi não aparece nela.
- **Modo LLM do sistema** (`executar.py --llm`) **nunca foi executado** (sem chave de API no desenvolvimento). Os resultados do plano vêm do modo determinístico.
- **Pesquisa de mercado externa** (demanda fora de Santa Maria, financiamento) depende do modo LLM com busca na web; não há dado de mercado no plano.
- Double-deck e P&D ficaram para a fase 2 por decisão do cliente.

## 4. Conferir antes de entregar

- [ ] Formatação conforme o **MDT UFSM vigente** (margens, fontes, citações, referências, legendas de figuras e tabelas). O padrão ABNT usual é margens de 3 cm (superior e esquerda) e 2 cm (direita e inferior), fonte 12, entrelinhas 1,5; **confirmar no MDT**, que é o que vale.
- [ ] Toda figura e tabela com número, legenda e fonte (as figuras em [figuras/](figuras/) não têm legenda numerada).
- [ ] Todo número do texto conferido contra [plano-consolidado.md](plano-consolidado.md) ou [resultados-analise.md](resultados-analise.md).
- [ ] Todas as referências verificadas em fonte real.
- [ ] Texto escrito pelo grupo (regra 4.1 do enunciado).
- [ ] Apresentação: equipe e papéis, diagnóstico, plano e resultados quantitativos.
- [ ] Relatório e apresentação enviados antes de 04/11/2026, 23:55 (depois disso são bloqueados).
