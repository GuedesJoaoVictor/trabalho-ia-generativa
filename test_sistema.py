"""Checagem mínima: números-chave batem com o cálculo direto da planilha e o Revisor barra o que deve barrar.
Rodar: .venv/bin/python test_sistema.py"""
import agentes
import ferramentas as F

r = agentes.orquestrar()
st = {p.id: p.status for p in r["propostas"]}

# números-chave (recalculados à mão a partir da planilha)
assert abs(F.passivo_dividendos()["total"] - 33_300_000) < 1
assert abs(F.passivo_dividendos()["exigivel"] - 22_500_000) < 1
assert abs(F.pendentes()["receita"] - 28_072_776.15) < 1
assert F.pendentes()["unidades"] == 27
assert round(F.capacidade_linha(2)["limite"]) == 59 and round(F.capacidade_linha(3)["limite"]) == 89
assert F.folha()["pessoas"] == 135 and round(F.folha()["total_mensal"]) == 1_501_569

# o Revisor barra o corte do elétrico, exige validação na diretoria e rescisão com caixa zero, e aprova o resto
assert st["FIN-3"] == "reprovada"
assert st["FIN-4"] == "condicional" and st["OPE-1"] == "condicional"
assert st["FIN-1"] == st["FIN-2"] == "aprovada"

# proposta adulterada: número errado e troca de peça proibida
errada = agentes.Proposta("X-1", "teste", "n", "d", fontes=["x"], afirmacoes=dict(dividendos_total_12m=1.0))
troca = agentes.Proposta("X-2", "teste", "n", "d", tipo="troca_fornecedor", fontes=["x"], pecas=["PEC-ELE-401"], prazo_meses=1)
sem_resc = agentes.Proposta("X-3", "teste", "n", "d", tipo="demissao", fontes=["x"], prazo_meses=1)
longa = agentes.Proposta("X-4", "teste", "n", "d", fontes=["x"], prazo_meses=18)
agentes.revisor([errada, troca, sem_resc, longa])
assert all(p.status == "reprovada" for p in (errada, troca, sem_resc, longa)), [p.motivos for p in (errada, troca, sem_resc, longa)]

# consolidação coerente
c = r["consolidado"]
assert abs(c["saida_dividendos"] - (2_775_000 + (22_500_000 + F.encargos_atrasados_selic()["encargos"]) / 24)) < 1
print("ok")
