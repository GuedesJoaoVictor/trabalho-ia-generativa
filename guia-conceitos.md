# Guia de conceitos (para entender, não para copiar)

Explicação informal para o grupo escrever com as próprias palavras e o próprio entendimento. Não está em formato de relatório.
**Referências:** são as que costumam ser citadas nesses temas; conferiram título, autores, ano e onde foi publicado antes de citar (eu posso errar detalhes).

## 1. IA generativa e LLMs
- Um LLM é um modelo de linguagem treinado para prever o próximo token; fica útil para texto, código e raciocínio porque aprendeu padrões em muito texto.
- Base: arquitetura Transformer (atenção). Pontos que o relatório costuma explicar: treino em larga escala, ajuste por instruções/feedback humano, janela de contexto.
- Limites que importam aqui: o LLM erra conta e inventa fatos. Por isso o nosso sistema **nunca deixa o LLM calcular**: os números vêm de funções Python (`ferramentas.py`).
- Referências: Vaswani et al. (2017) "Attention Is All You Need"; Brown et al. (2020) "Language Models are Few-Shot Learners".

## 2. Agente único vs multiagentes
- Agente: um LLM em laço que decide ações, usa ferramentas e observa resultados. Multiagente: vários agentes com papéis distintos, que podem se criticar.
- Quando multiagente compensa: tarefas com domínios independentes, necessidade de verificação cruzada, contextos que não cabem em um prompt só. Custo: mais complexidade, mais chamadas e coordenação.
- No nosso caso (decidido em `arquitetura-agentes.md`): finanças, linha, suprimentos e mercado são domínios distintos; o cliente deu carta branca; as regras dele são checáveis, o que justifica um Revisor com poder de veto.
- Honestidade: **no modo atual, os agentes são funções Python determinísticas**; o modo com Claude (`--llm`) existe mas nunca foi executado. O relatório e a apresentação precisam dizer isso.
- Referências: Wooldridge, *An Introduction to MultiAgent Systems*; Russell e Norvig, *Artificial Intelligence: A Modern Approach* (agentes); Anthropic (2024) "Building effective agents"; Wu et al. (2023) AutoGen; Du et al. (2023) debate multiagente (para a ideia de revisor/crítico).

## 3. Engenharia de prompt, tool use e RAG
- **Prompt engineering:** instruções claras, papel, exemplos (few-shot), formato de saída, raciocínio passo a passo (chain-of-thought). Referências: Brown et al. (2020); Wei et al. (2022) "Chain-of-Thought Prompting...".
- **Tool use:** o modelo pede para chamar uma função (com argumentos), o código executa e devolve o resultado. É o que usamos: margem, capacidade, dividendos, câmbio. Referências: Yao et al. (2023) ReAct; Schick et al. (2023) Toolformer.
- **RAG:** buscar trechos relevantes em uma base de documentos e colocá-los no contexto antes de gerar. **Nosso sistema não implementa RAG.** O mais próximo é o uso de dados externos (API do Banco Central) como ferramenta. Se citarem RAG, digam que foi estudado e não aplicado, e onde faria sentido (ex.: consultar normas ou contratos). Referência: Lewis et al. (2020).

## 4. Otimização e decisão no domínio
- O plano é, na prática, uma decisão com restrições: maximizar caixa em 12 meses respeitando regras (caixa zero, rescisão CLT, aviso de 30 dias, peças não trocáveis).
- Ferramentas usadas: cálculo de margem e lucro por unidade, capacidade por estação (restrição de gargalo), cobertura (lucro bruto / dividendos), análise de cenários e sensibilidade (operadores por estação, câmbio).
- **Não usamos programação linear nem solver.** Se citarem otimização, descrevam o que foi feito: regras e cenários, não um modelo matemático otimizado.
- Referências: Hillier e Lieberman, *Introduction to Operations Research*; Goldratt, *A Meta* (Teoria das Restrições, base da ideia de gargalo).

## 5. Como o nosso código se encaixa (para a seção de arquitetura)
- `dados.py` lê a planilha → `ferramentas.py` calcula tudo → `agentes.py` monta propostas por domínio → `revisor` recalcula do zero e checa as regras → `consolidar` projeta 12 meses.
- Prova de que o Revisor funciona: `test_sistema.py` mostra que ele reprova a proposta do elétrico, marca como condicional a rescisão com caixa zero e rejeita propostas com número adulterado.
- Premissas (todas marcadas): 3 pessoas por estação (sensibilidade 2 a 4), 75% de ocupação, 20% de manutenção, rescisão de 2,8 salários, multa de 0,1%/dia.
