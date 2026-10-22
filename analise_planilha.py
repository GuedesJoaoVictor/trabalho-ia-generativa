"""Calcula o que a planilha deixa como fórmula sem valor (<v> vazio). Saída: markdown.

Uso: python3 -I analise_planilha.py > resultados-analise.md
"""
import html
import re
import zipfile
from collections import defaultdict

XLSX = "Estudo_de_Caso_Industria_Onibus_Em_Crise.xlsx"
DIAS_UTEIS = 0.714  # fator usado na própria aba de folha (5/7)


def carregar(i):
    """Linhas de dados da aba i (sem título/subtítulo/cabeçalho/total), como listas de valores."""
    d = zipfile.ZipFile(XLSX).read(f"xl/worksheets/sheet{i}.xml").decode()
    linhas = []
    for r in re.findall(r"<row [^>]*>(.*?)</row>", d, re.S):
        row = {}
        for ref, corpo in re.findall(r'<c r="([A-Z]+)\d+"[^>]*>(.*?)</c>', r, re.S):
            if "<f>" in corpo:
                continue  # fórmula sem valor: calculamos aqui
            v = html.unescape(re.sub(r"<[^>]+>", "", corpo))
            try:
                v = float(v)
            except ValueError:
                pass
            row[ref] = v
        linhas.append(row)
    return linhas[3:]  # título, subtítulo, vazio; a 1ª restante é o cabeçalho


def dados(i):
    return [r for r in carregar(i)[1:] if len(r) > 2]


def brl(x):
    return f"R$ {x:,.0f}".replace(",", ".")


def pct(x):
    return f"{x * 100:.1f}%".replace(".", ",")


def tabela(cab, linhas):
    print("| " + " | ".join(cab) + " |")
    print("|" + "---|" * len(cab))
    for l in linhas:
        print("| " + " | ".join(str(c) for c in l) + " |")
    print()


# ---------------------------------------------------------------- dados
modelos = dados(1)       # A cód, B nome, G custo, H preço
pedidos = dados(2)       # B mês, C modelo, D qtd, E valor unit, G status
linha = dados(3)         # A etapa, B nome, D ciclo h, E desvio, F refugo
pecas = dados(4)         # A cód, D forn, E país, F preço, G lead time
bom = dados(5)           # A modelo, B peça, D qtd, E custo unit
folha = dados(6)         # B cat, C nível, E salário, H faltas
divid = dados(7)         # A mês, B classe, C ações, D div/ação, G status

nome = {m["A"]: m["B"] for m in modelos}

# ---------------------------------------------------------------- 1. margem
print("# Resultados da análise da planilha\n")
print("Valores calculados por `analise_planilha.py` (a planilha traz fórmulas sem resultado).\n")
print("## 1. Margem por modelo\n")
margem = {}
linhas = []
for m in modelos:
    margem[m["A"]] = (m["H"] - m["G"]) / m["H"]
    linhas.append([m["A"], nome[m["A"]], brl(m["G"]), brl(m["H"]), brl(m["H"] - m["G"]), pct(margem[m["A"]])])
tabela(["Cód.", "Modelo", "Custo direto", "Preço médio", "Lucro/unid.", "Margem teórica"], linhas)

# margem "real" com o preço médio efetivamente praticado nos pedidos
print("**Preço efetivamente praticado nos pedidos (12 meses) vs. preço de catálogo:**\n")
por_modelo = defaultdict(lambda: [0, 0.0])
for p in pedidos:
    por_modelo[p["C"]][0] += p["D"]
    por_modelo[p["C"]][1] += p["D"] * p["E"]
linhas = []
for m in modelos:
    q, v = por_modelo[m["A"]]
    pm = v / q if q else 0
    linhas.append([m["A"], int(q), brl(pm), brl(m["H"]), pct(pm / m["H"] - 1), pct((pm - m["G"]) / pm) if q else "-"])
tabela(["Cód.", "Unid. pedidas", "Preço médio praticado", "Preço catálogo", "Desvio", "Margem c/ preço praticado"], linhas)

# ---------------------------------------------------------------- 2. BOM
print("## 2. Custo de materiais (BOM) vs. custo direto estimado\n")
bom_modelo = defaultdict(float)
for b in bom:
    bom_modelo[b["A"]] += b["D"] * b["E"]
linhas = []
for m in modelos:
    c = bom_modelo.get(m["A"])
    linhas.append([m["A"], brl(c) if c else "sem BOM", brl(m["G"]), pct(c / m["G"]) if c else "-"])
tabela(["Cód.", "Custo BOM", "Custo direto estimado", "BOM / custo direto"], linhas)

# ---------------------------------------------------------------- 3. pedidos
print("## 3. Carteira de pedidos\n")
meses = []
for p in pedidos:
    if p["B"] not in meses:
        meses.append(p["B"])
total = sum(p["D"] * p["E"] for p in pedidos)
unid = sum(p["D"] for p in pedidos)
print(f"Total da carteira (12 meses): **{brl(total)}** em **{int(unid)}** unidades.\n")
st = defaultdict(lambda: [0, 0.0])
for p in pedidos:
    st[p["G"]][0] += p["D"]
    st[p["G"]][1] += p["D"] * p["E"]
tabela(["Status", "Unidades", "Valor", "% do valor"], [[k, int(v[0]), brl(v[1]), pct(v[1] / total)] for k, v in st.items()])
mes_v = {m: [0, 0.0] for m in meses}
for p in pedidos:
    mes_v[p["B"]][0] += p["D"]
    mes_v[p["B"]][1] += p["D"] * p["E"]
tabela(["Mês", "Unidades", "Valor"], [[m, int(v[0]), brl(v[1])] for m, v in mes_v.items()])
mod_v = defaultdict(float)
for p in pedidos:
    mod_v[p["C"]] += p["D"] * p["E"]
tabela(["Modelo", "Unidades", "Valor", "% do valor"], [[k, int(por_modelo[k][0]), brl(v), pct(v / total)] for k, v in sorted(mod_v.items(), key=lambda x: -x[1])])
media_mensal_un = unid / len(meses)
media_mensal_v = total / len(meses)

# ---------------------------------------------------------------- 4. linha
print("## 4. Linha de montagem: capacidade e qualidade\n")
ciclo_total = sum(e["D"] for e in linha)
rty = 1.0
linhas = []
for e in linha:
    rty *= 1 - e["F"]
    linhas.append([int(e["A"]), e["B"], e["D"], e["E"], pct(e["F"]), round(e["D"] * e["F"], 2)])
tabela(["Etapa", "Estação", "Ciclo (h)", "Desvio (h)", "Refugo/retrab.", "Horas perdidas/veículo (ciclo×taxa)"], linhas)
est_lenta = max(linha, key=lambda e: e["D"])
horas_mes = 24 * 30
cap = horas_mes / est_lenta["D"]
print(f"- Tempo total de ciclo por veículo (soma das etapas): **{ciclo_total:.1f} h**.")
print(f"- Estação mais lenta (limita a vazão): **{est_lenta['B']}**, {est_lenta['D']} h/veículo.")
print(f"- Capacidade teórica operando 24h × 30 dias, sem paradas, com 1 veículo por estação: **{cap:.0f} veículos/mês** ({horas_mes} h / {est_lenta['D']} h). *Hipótese: estações em série, uma máquina por etapa.*")
print(f"- Demanda média de pedidos: **{media_mensal_un:.1f} veículos/mês** → uso da capacidade teórica de **{pct(media_mensal_un / cap)}**.")
print(f"- Rendimento de primeira passagem (produto de 1 − refugo nas 8 etapas): **{pct(rty)}**, ou seja, **{pct(1 - rty)}** dos veículos passam por refugo/retrabalho em alguma etapa.")
print(f"- As 3 etapas sinalizadas como gargalo na planilha (20, 50, 60) respondem por **{pct(sum(e['F'] for e in linha if e['A'] in (20, 50, 60)) / sum(e['F'] for e in linha))}** da soma das taxas de refugo.")
print("- A planilha chama de gargalo as etapas com refugo alto; a etapa que limita a vazão por tempo de ciclo é outra (pintura, 8 h).\n")

# ---------------------------------------------------------------- 5. fornecedores
print("## 5. Fornecedores e lead time\n")
tabela(["Peça", "Fornecedor", "País", "Preço", "Lead time (dias)"],
       [[p["A"], p["D"], p["E"], brl(p["F"]), int(p["G"])] for p in sorted(pecas, key=lambda x: -x["G"])])
lt = {p["A"]: p["G"] for p in pecas}
pais = {p["A"]: p["E"] for p in pecas}
linhas = []
for m in modelos:
    ps = [b["B"] for b in bom if b["A"] == m["A"]]
    if ps:
        crit = max(ps, key=lambda c: lt[c])
        linhas.append([m["A"], int(lt[crit]), crit])
tabela(["Modelo", "Maior lead time da BOM (dias)", "Peça que define"], linhas)
imp_total = sum(b["D"] * b["E"] for b in bom if pais[b["B"]] != "Brasil")
bom_total = sum(b["D"] * b["E"] for b in bom)
print(f"Participação de peças importadas no custo de BOM (3 modelos): **{pct(imp_total / bom_total)}**.\n")

# ---------------------------------------------------------------- 6. folha
print("## 6. Folha de pagamento e absenteísmo\n")
grupos = defaultdict(list)
for f in folha:
    grupos[f["C"]].append(f)
tot_folha = 0.0
linhas = []
for n in ["Operacional", "Analista", "Gestor", "Diretoria"]:
    g = grupos[n]
    custo = sum(f["E"] * 1.45 for f in g)
    tot_folha += custo
    faltas = sum(f["H"] for f in g)
    absent = faltas / (len(g) * 180 * DIAS_UTEIS)
    custo_falta = sum(f["E"] * 1.45 / 30 * f["H"] for f in g)  # dia = total mensal / 30
    linhas.append([n, len(g), brl(custo), brl(custo / len(g)), pct(absent), brl(custo_falta)])
tabela(["Nível", "Pessoas", "Custo mensal (c/ encargos 45%)", "Custo médio/pessoa", "Absenteísmo", "Custo das faltas (180 dias)*"], linhas)
print(f"Folha mensal total (c/ encargos): **{brl(tot_folha)}** para **{len(folha)}** pessoas. Anual: **{brl(tot_folha * 12)}**.")
dir_c = sum(f["E"] * 1.45 for f in grupos["Diretoria"])
print(f"Diretoria: {len(grupos['Diretoria'])} pessoas = **{pct(dir_c / tot_folha)}** da folha.")
op = grupos["Operacional"]
print(f"Cada 10 operadores a menos economizam cerca de **{brl(10 * sum(f['E'] * 1.45 for f in op) / len(op))}/mês** (antes de rescisão).")
print(f"Folha mensal vs. faturamento médio mensal da carteira: **{pct(tot_folha / media_mensal_v)}**.\n")
print("\\* custo da falta = total mensal ÷ 30 × faltas (aproximação). Excesso de operadores **não** é calculável só com a planilha: faltam horas-homem por veículo e escala de turnos.\n")

# ---------------------------------------------------------------- 7. dividendos
print("## 7. Dividendos e JCP\n")
linhas = []
tot_div = tot_jcp = 0.0
por_status = defaultdict(float)
for d in divid:
    dv = d["C"] * d["D"]
    jcp = dv * 0.15
    tot_div += dv
    tot_jcp += jcp
    por_status[d["G"]] += dv
    linhas.append([d["A"], d["B"], brl(dv), brl(jcp), d["G"]])
tabela(["Mês", "Classe", "Dividendos", "JCP (15%)", "Status"], linhas)
tabela(["Status", "Dividendos"], [[k, brl(v)] for k, v in por_status.items()])
print(f"- Total de dividendos em 12 meses: **{brl(tot_div)}**; JCP (15%): **{brl(tot_jcp)}**.")
print(f"- Obs.: o rótulo da planilha diz \"dividendos/JCP acumulados em atraso\", mas a fórmula soma só dividendos (coluna E), e inclui meses \"suspensos\" (ON), não apenas os em atraso (PN).")
print(f"- Dividendos de 12 meses = **{pct(tot_div / total)}** do valor bruto da carteira de pedidos do mesmo período.")
entregue = st["Entregue"][1]
print(f"- Dividendos = **{pct(tot_div / entregue)}** do valor já entregue; folha anual = **{pct(tot_folha * 12 / entregue)}** do valor já entregue.")
mensal_div = tot_div / 12
print(f"- Dividendos médios por mês: **{brl(mensal_div)}**; folha mensal: **{brl(tot_folha)}**; margem bruta teórica média ponderada da carteira: ", end="")
mb = sum((por_modelo[m["A"]][1] - por_modelo[m["A"]][0] * m["G"]) for m in modelos)
print(f"**{pct(mb / total)}** → lucro bruto médio/mês ≈ **{brl(mb / 12)}** (antes de folha, dívidas e outras despesas).\n")

# ---------------------------------------------------------------- 8. atraso e juros
print("## 8. Atraso dos dividendos (referência: fim de Out/26)\n")
print("A planilha **não tem** saldo de dívida bancária, taxa de juros nem multa: só os dividendos. "
      "O que dá para calcular é o passivo de dividendos e uma estimativa de encargos sobre os atrasados, "
      "com taxa **hipotética** (a real deve vir do cliente ou de fonte externa).\n")
ordem = [d["A"] for d in divid]
ref = len(ordem) - 1
em_atraso = [(ordem.index(d["A"]), d["C"] * d["D"]) for d in divid if d["G"] == "Acumulado em Atraso"]
principal = sum(v for _, v in em_atraso)
meses_x_valor = sum((ref - i) * v for i, v in em_atraso)
print(f"- Parcelas PN em atraso: **{len(em_atraso)}** (Dez/25 a Ago/26), principal **{brl(principal)}**; "
      f"média ponderada de **{meses_x_valor / principal:.1f} meses** de atraso; a mais antiga tem {ref - em_atraso[0][0]} meses.")
print()
linhas = []
for taxa in (0.01, 0.015, 0.02):  # ponytail: juros simples, sem correção monetária; trocar pela taxa real do cliente
    juros = taxa * meses_x_valor
    multa = 0.02 * principal
    linhas.append([pct(taxa) + " a.m.", brl(juros), brl(multa), brl(principal + juros + multa)])
tabela(["Taxa hipotética", "Juros acumulados (simples)", "Multa 2% (hipótese)", "Atrasado + encargos"], linhas)
judicial = sum(d["C"] * d["D"] for d in divid if d["G"].startswith("Exigência"))
suspenso = por_status["Suspenso p/ Reestruturação"]
print(f"- Passivo de dividendos de 12 meses, por situação: em atraso **{brl(principal)}** + exigência judicial **{brl(judicial)}** "
      f"= **{brl(principal + judicial)}** exigíveis; suspensos (ON) **{brl(suspenso)}**; total **{brl(tot_div)}**.")
print(f"- Exigível hoje (atraso + judicial) = **{pct((principal + judicial) / tot_div)}** do total. Equivale a **{(principal + judicial) / (mb / 12):.1f} meses** de lucro bruto médio (referência: {brl(mb / 12)}/mês).\n")

# ---------------------------------------------------------------- 9. regras da 2ª entrevista
print("## 9. Impacto das respostas da 2ª entrevista\n")

print("### 9.1 Multa por atraso nos pedidos pendentes\n")
print("Regra do cliente: 10% do valor do ônibus + 0,1% do valor ao dia. "
      "*Hipótese:* os 0,1%/dia incidem sobre o valor dos pedidos atrasados. Dias de atraso não constam na planilha.\n")
pend_v = st["Pendente / Atrasado"][1]
pend_u = int(st["Pendente / Atrasado"][0])
fixa = 0.10 * pend_v
dia = 0.001 * pend_v
tabela(["Dias de atraso", "Multa fixa (10%)", "Multa diária acumulada", "Total"],
       [[d, brl(fixa), brl(dia * d), brl(fixa + dia * d)] for d in (0, 15, 30, 60)])
print(f"- {pend_u} ônibus pendentes, valor **{brl(pend_v)}**; cada dia de atraso custa **{brl(dia)}** de multa, "
      f"**{pct(fixa / pend_v)}** do valor já é devido pela multa fixa (**{brl(fixa)}**).")
print("- Prefeituras só pagam na entrega (resposta 11): atraso adia a receita **e** gera multa.\n")

print("### 9.2 Plano de pagamento dos dividendos (prazo de 12 meses; atrasados em 24 meses se estiver em dia)\n")
atrasado = principal + judicial
cenarios = [("A: atrasados PN + judicial", atrasado), ("B: A + dividendos ON suspensos", atrasado + suspenso)]
linhas = []
for nome_c, valor in cenarios:
    parcela = valor / 24
    linhas.append([nome_c, brl(valor), brl(parcela), brl(mensal_div), brl(mensal_div + parcela), pct((mensal_div + parcela) / (mb / 12))])
tabela(["Cenário", "Atrasado a quitar", "Parcela/mês (24 m)", "Dividendo corrente/mês", "Saída mensal total", "% do lucro bruto médio/mês"], linhas)
print("- Sem juros e multa (taxa não informada). Dividendo corrente = média mensal do cronograma da planilha (ON e PN alternam), mantendo as ações atuais.")
print(f"- Lucro bruto médio/mês de referência: **{brl(mb / 12)}** (margem direta; segundo o cliente o custo direto já inclui mão de obra e impostos).\n")

print("### 9.3 Capacidade com restrições informadas\n")
print("Restrições: 3 turnos de 8 h (24 h); etapa 80 (acoplamento ao chassi) não opera à noite (iluminação e ruído) → 16 h. "
      "Tempo de ciclo efetivo = ciclo × (1 + taxa de refugo/retrabalho), pois o cliente disse que a taxa é sobre o tempo de ciclo.\n")
linhas = []
caps = []
for e in linha:
    h = 16 if e["A"] == 80 else 24
    ef = e["D"] * (1 + e["F"])
    c = h * 30 / ef
    caps.append((c, e["B"]))
    linhas.append([int(e["A"]), e["B"], h, round(ef, 2), round(c)])
tabela(["Etapa", "Estação", "Horas/dia", "Ciclo efetivo (h)", "Capacidade teórica (veíc./mês)"], linhas)
cmin = min(caps)
pico = max(v[0] for v in mes_v.values())
print(f"- Limite teórico da linha: **{cmin[0]:.0f} veículos/mês** ({cmin[1]}). Demanda média **{media_mensal_un:.1f}**, pico mensal **{int(pico)}** ({pct(pico / cmin[0])} do limite).")
print("- Se o limite teórico fosse real, não haveria pedidos atrasados: o gargalo efetivo está em **fornecedores e paradas de máquina de segunda mão**, não no tempo de ciclo. Não há dados de paradas na planilha.\n")

print("### 9.4 Capital imobilizado em inversores/baterias (peça importada, sem produtor nacional)\n")
inv = next(p for p in pecas if p["A"] == "PEC-ELE-402")
ele_un_mes = por_modelo["BUS-ELE-12M"][0] / len(meses)
saida = ele_un_mes * inv["F"]
print(f"- Elétricos: **{ele_un_mes:.1f} unid./mês** × {brl(inv['F'])} = **{brl(saida)}/mês** em inversores/baterias.")
print(f"- Com lead time de **{int(inv['G'])} dias**, o capital em trânsito/estoque é de cerca de **{brl(saida * inv['G'] / 30)}** (se pago no pedido; condição de pagamento não informada).")
print(f"- Chicote Yazaki (PEC-ELE-401) **não pode ser trocado** (cliente); lead time {int(lt['PEC-ELE-401'])} dias.\n")

print("### 9.5 Lead time como medida de atraso do fornecedor\n")
print("Segundo o cliente, lead time é o tempo médio real de entrega do fornecedor; logo ele já é o dado de atraso. "
      "Prazo mínimo pedido→entrega por modelo = maior lead time da BOM + tempo de ciclo da linha, se a peça só for comprada após o pedido.\n")
linhas = []
for m in modelos:
    ps = [b["B"] for b in bom if b["A"] == m["A"]]
    if ps:
        linhas.append([m["A"], int(max(lt[c] for c in ps)), f"{ciclo_total / 24:.1f}", f"{max(lt[c] for c in ps) + ciclo_total / 24:.0f}"])
tabela(["Modelo", "Maior lead time (dias)", "Ciclo da linha (dias)", "Prazo mínimo pedido→entrega (dias)"], linhas)
tabela(["Peça", "Fornecedor", "Lead time (dias)", "Troca possível?"],
       [[p["A"], p["D"], int(p["G"]), "Não (cliente)" if p["A"] == "PEC-ELE-401" else "Sem produtor nacional" if p["A"] == "PEC-ELE-402" else "Sim, com aviso de 30 dias"]
        for p in sorted(pecas, key=lambda x: -x["G"])[:6]])
