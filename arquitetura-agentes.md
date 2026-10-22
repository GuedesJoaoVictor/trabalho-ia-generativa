# Arquitetura da Solução — Decisão e Especificação Técnica

## 1. Decisão: sistema multiagentes

Escolha entre as duas opções do enunciado, com base em [respostas-professor.md](respostas-professor.md):

| Fato da entrevista | Consequência para a arquitetura |
|---|---|
| Sete pontos a avaliar, de áreas diferentes (margem, capacidade, linha, fornecedores, operadores, vendas, novos produtos) | Domínios independentes, cada um com dados e método próprios → um agente por domínio |
| Vender mais e entrar em novos segmentos (circular, urbano, rodoviário, double-deck) | Exige dados externos (mercado, concorrentes, editais) → agente de coleta externa |
| Prioridade nº 1 é o caixa (dividendos, risco de bloqueio pela B3) | As propostas de todas as áreas precisam ser filtradas por restrição financeira → um agente financeiro com poder de veto |
| "Carta branca" e prazo máximo de 12 meses | Não há alçada de aprovação que obrigue um humano em cada passo; a validação pode ser interna (agente Revisor) |
| Restrições concretas: CLT, aviso de 30 dias ao fornecedor | Regras checáveis automaticamente pelo Revisor |
| Prazo de 12 meses para regularizar dividendos (atrasados em 24 meses se o corrente estiver em dia) | O Financeiro modela fluxo mensal com duas janelas: 12 e 24 meses |
| "Podem fazer o que for necessário" (inclusive demitir com rescisão e realocar) | Confirma ausência de aprovação obrigatória; Operações pode propor corte e realocação de operadores |
| Prefeituras só pagam na entrega; multa de 10% + 0,1%/dia por atraso | Atraso adia receita e gera multa → Suprimentos e Operações priorizam o que destrava a entrega |
| Sem caixa; novos produtos só depois de a empresa estar no verde | Financeiro trabalha com caixa inicial zero; Mercado separa plano de estabilização (12 meses) de expansão (fase 2) |
| Chicote Yazaki não pode ser trocado; inversor vem só da China, difícil estocar | Suprimentos trata essas peças como restrições fixas e otimiza o resto |
| Acoplamento ao chassi não pode ser à noite (iluminação e ruído) | Operações modela a etapa 80 com 16 h/dia |

**Aprovação:** respondida na 2ª entrevista ("podem fazer o que for necessário"). Sem aprovação humana obrigatória; o Revisor é a validação. Nada é executado automaticamente: o plano final é entregue ao grupo/cliente.

## 2. Agentes

```
                    ┌──────────────────┐
                    │   Orquestrador   │  distribui tarefas, junta resultados
                    └────────┬─────────┘
     ┌────────────┬──────────┼───────────┬──────────────┐
     ▼            ▼          ▼           ▼              │
┌──────────┐ ┌──────────┐ ┌───────────┐ ┌─────────────┐ │
│Financeiro│ │Operações │ │Suprimentos│ │Mercado/Ext. │ │
└────┬─────┘ └────┬─────┘ └─────┬─────┘ └──────┬──────┘ │
     └────────────┴──────┬──────┴──────────────┘        │
                         ▼                              │
                   ┌──────────┐   reprova → devolve ────┘
                   │ Revisor  │
                   └────┬─────┘
                        ▼
              Plano consolidado (12 meses)
```

| Agente | Responsabilidade | Perguntas do cliente que responde | Dados |
|---|---|---|---|
| **Orquestrador** | Recebe o objetivo, aciona os especialistas, resolve conflitos de prioridade (caixa primeiro), monta o plano | — | Todas as saídas |
| **Financeiro** | Margem por modelo, passivo de dividendos/JCP, fluxo de caixa mensal, risco de bloqueio. Veta propostas sem caixa | Margem de lucro por modelo; regularizar dividendos | Modelos, Pedidos, Dividendos, Folha |
| **Operações** | Capacidade produtiva (24h), causas de gargalo e refugo, excesso de operadores e custo de 24h, absenteísmo | Capacidade; causas na linha; excesso de operadores | Linha de Montagem, Folha |
| **Suprimentos** | Atraso por fornecedor, custo da BOM, alternativas de fornecedor (aviso de 30 dias), peças críticas | Atrasos e substituição de fornecedores | Catálogo de Peças, BOM |
| **Mercado / Coleta Externa** | Novos clientes além de Santa Maria, segmentos e produtos (double-deck, urbano, circular) que usem a linha atual, benchmarks | Novos clientes; novos produtos | Pedidos + web/APIs |
| **Revisor** | Valida números, restrições e coerência entre propostas; devolve ao agente com o motivo | Consistência do plano | Saídas de todos |

## 3. Ferramentas (tool use)

- **Cálculo em Python (pandas):** toda conta (margem, capacidade, custo de refugo, passivo) é feita por função, nunca "de cabeça" pelo LLM. O LLM escolhe a função e interpreta o resultado.
- **Leitor da planilha:** carrega as 7 abas considerando o deslocamento de 3 linhas (título, subtítulo, vazio) e as fórmulas como texto (a planilha traz `D5*E5` etc. sem valor calculado).
- **Busca web / scraping (agente Mercado):** preços de aço e alumínio, câmbio, editais e frotas de municípios, concorrentes de double-deck. Cada dado externo guarda URL e data de consulta.
- **RAG (opcional):** consulta a documentos do cliente (respostas da entrevista, enunciado) para manter as restrições sempre no contexto.

## 4. Regras de validação (Revisor)

1. Todo número do plano tem origem rastreável: aba/linha da planilha ou URL externa com data.
2. Recalcular por código os valores-chave e comparar com o que o agente afirmou; divergência → devolve.
3. Hipótese não confirmada pela planilha ou pela entrevista é marcada como **hipótese** (ex.: caixa, dívida e inadimplência não existem na base).
4. Respeitar as restrições do cliente: horizonte de 12 meses, vínculo CLT (custo de rescisão entra na conta de redução de operadores), aviso de 30 dias na troca de fornecedor.
5. Nenhuma proposta pode piorar o caixa dos primeiros meses sem apontar a fonte de financiamento, já que a prioridade é regularizar dividendos.
6. Multa por atraso (10% do valor + 0,1%/dia) entra como custo de qualquer cenário que atrase entregas.
7. Propostas com economia e custo de implantação devem informar o prazo de retorno.

## 5. Lacunas e hipóteses

Respondido pelo cliente:
- Dívida = só dividendos (não há outros credores); inadimplência não é problema.
- **Caixa = não tem** → hipótese de trabalho: caixa inicial zero. O plano precisa se autofinanciar pelo lucro operacional; qualquer cenário que exija desembolso antecipado (ex.: estoque de inversores) precisa apontar a fonte.
- **Lead time = tempo médio real de entrega** → já é o dado de atraso do fornecedor; não há outro a coletar.
- **Double-deck e P&D ficam para depois** de a empresa estar "no verde": o agente de Mercado propõe novos produtos como fase 2, fora do fluxo de caixa dos primeiros 12 meses.
- Refugo = % do tempo de ciclo; custo direto inclui mão de obra e impostos.

Ainda sem resposta (tratar como hipótese):
- Taxa de juros e multa dos dividendos atrasados; valor da exigência dos minoritários.
- Custo em R$ do refugo; horas de parada de máquina (maquinário de segunda mão).
- BOM sem os modelos Urbano Articulado e Micro-ônibus; chassi não aparece na BOM (hipótese: explica parte do custo direto).
- Demanda fora de Santa Maria.

## 6. Próximos passos técnicos

1. Carregar as 7 abas e calcular o que a planilha não calcula (margem por modelo, capacidade, passivo de dividendos, custo da folha).
2. Implementar as ferramentas de cálculo e o leitor da planilha.
3. Implementar os agentes e o Revisor; testar com a base.
