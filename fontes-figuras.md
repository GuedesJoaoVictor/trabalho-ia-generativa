# Fontes das figuras e tabelas (para legendas e "Fonte:")

Só fatos: de onde vem cada dado e o que cada gráfico plota. As legendas e a interpretação são do grupo.
Sugestão de linha de fonte (padrão ABNT para figura própria): "Fonte: elaborado pelos autores (2026), com base em <dado>". Confirmar no MDT.

## Figuras (`figuras/`, geradas por `figuras.py`)

| Arquivo | O que plota | Dado de origem | Cálculo | Atenção ao descrever |
|---|---|---|---|---|
| 01_arquitetura | Fluxo: entradas (planilha, entrevista, Banco Central) → Orquestrador → 5 agentes → ferramentas → Revisor → plano; seta tracejada de volta para propostas reprovadas | Não é dado; reflete `agentes.py` | | O agente de Operações inclui pessoas. O Revisor tem 3 pareceres: aprovada, condicional, reprovada |
| 02_margem_modelos | Margem bruta (%) por modelo, preço de catálogo vs preço praticado nos pedidos | Abas Modelos de Ônibus e Pedidos por Mês | `margem_por_modelo`: (preço − custo direto) / preço | Preço praticado = média dos pedidos. Custo direto vem da planilha |
| 03_carteira_pedidos | Ônibus pedidos por mês, empilhados por situação (Entregue, Em Produção, Pendente/Atrasado) | Aba Pedidos por Mês (direto, sem ferramenta) | Soma de `qtd` por mês e status | O eixo é quantidade, não valor |
| 04_capacidade_linha | Capacidade teórica (ônibus/mês) por estação com 3 e 2 turnos; linhas de pico e média de pedidos | Aba Linha de Montagem; pedidos | `capacidade_linha(3)` e `(2)` | Ciclo efetivo; etapa 80 limitada a 16 h/dia (sem acoplamento ao chassi à noite). Não inclui paradas de máquina |
| 05_refugo_etapas | Refugo/retrabalho (% do tempo de ciclo) por etapa; vermelho se ≥ 5% | Aba Linha de Montagem (direto) | Nenhum | Cliente: refugo é % do tempo de ciclo, não de peças |
| 06_leadtime_pecas | Lead time (dias) por peça; vermelho = não pode ser trocada | Aba Catálogo de Peças | `leadtime_criticos` | Cliente: lead time = tempo médio real de entrega |
| 07_caixa_dividendos | Esquerda: lucro bruto + melhorias vs dividendos por mês. Direita: saldo acumulado com e sem plano | `plano.json` | `consolidar` | **Proxy**: lucro bruto menos dividendos. Não é caixa real |

## Tabelas LaTeX geradas (`relatorio/tabelas/`, por `gerar_tabelas.py`)

Só o `tabular`; envolvam em `table` com legenda e fonte. Se passarem da margem, usem `\small` ou `\resizebox{\textwidth}{!}{...}`.

| Arquivo | Conteúdo | Origem |
|---|---|---|
| propostas.tex | 11 propostas: efeito mensal, pontual, parecer | `plano.json` |
| projecao.tex | 12 meses: lucro bruto, melhorias, pontual, dividendos, saldo | `plano.json` |
| margens.tex | Custo, preço praticado, margem, lucro por ônibus, unidades em 12 meses | `margem_por_modelo` |
| dividendos.tex | R$ 33,3 mi em 12 meses por situação | `passivo_dividendos` |
| capacidade.tex | Ciclo efetivo e capacidade por estação, 3 e 2 turnos | `capacidade_linha` |

Se rodarem `executar.py` de novo: `.venv/bin/python gerar_tabelas.py` para atualizar. Para refugo, folha e lead time, os valores estão em `resultados-analise.md`.

## Pontos que a legenda ou o texto não podem esconder

- Saldo/caixa = proxy. O cliente informou caixa zero.
- Capacidade = teórica.
- Operadores por estação, rescisão (2,8 salários), multa de 0,1%/dia sobre pedidos pendentes e Selic como índice de correção são **premissas** (`PREMISSAS` em `ferramentas.py`).
- A BOM cobre 3 dos 5 modelos e não traz o chassi.
- Inadimplência: sem dados na planilha; o cliente disse que não é problema.
