"""Gera tabelas LaTeX (só o tabular, sem legenda) em relatorio/tabelas/ a partir de plano.json e das ferramentas.
Uso: .venv/bin/python gerar_tabelas.py   e no relatório: \\begin{table}...\\input{tabelas/propostas}...\\end{table}"""
import json

import ferramentas as F

pt = lambda x, d=0: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
rs = lambda x: "R\\$ " + pt(x)
esc = lambda s: str(s).replace("&", "\\&").replace("%", "\\%").replace("$", "\\$").replace("#", "\\#").replace("_", "\\_")
plano = json.load(open("plano.json", encoding="utf-8"))


def tab(nome, cols, cab, linhas):
    L = [f"\\begin{{tabular}}{{{cols}}}", "\\toprule", " & ".join(f"\\textbf{{{c}}}" for c in cab) + " \\\\", "\\midrule"]
    L += [" & ".join(l) + " \\\\" for l in linhas] + ["\\bottomrule", "\\end{tabular}"]
    open(f"relatorio/tabelas/{nome}.tex", "w", encoding="utf-8").write("\n".join(L) + "\n")


tab("propostas", "llrrl", ["ID", "Proposta", "Efeito mensal", "Efeito pontual", "Parecer"],
    [[p["id"], esc(p["titulo"]), rs(p["impacto_mensal"]), rs(p["impacto_unico"]), p["status"]] for p in plano["propostas"]])

tab("projecao", "rrrrrr", ["Mês", "Lucro bruto base", "Melhorias", "Pontual", "Dividendos", "Saldo acumulado"],
    [[str(l["mes"])] + [rs(l[k]) for k in ("base", "melhorias", "unico", "saida", "saldo_acumulado")] for l in plano["consolidado"]["projecao"]])

tab("margens", "lrrrrr", ["Modelo", "Custo direto", "Preço praticado", "Margem", "Lucro por ônibus", "Unid. em 12 meses"],
    [[esc(m["nome"]), rs(m["custo"]), rs(m["preco_praticado"]), pt(m["margem_praticada"] * 100, 1) + "\\%", rs(m["lucro_unid"]), pt(m["unid_12m"])] for m in F.margem_por_modelo()])

pd = F.passivo_dividendos()
tab("dividendos", "lr", ["Situação", "Valor em 12 meses"],
    [[esc(k), rs(v)] for k, v in pd["por_status"].items()] + [["\\textbf{Total}", "\\textbf{" + rs(pd["total"]) + "}"]])

c3, c2 = F.capacidade_linha(3), F.capacidade_linha(2)
tab("capacidade", "rrrr", ["Etapa", "Ciclo efetivo (h)", "Capacidade 3 turnos", "Capacidade 2 turnos"],
    [[f"{e['etapa']} {esc(e['nome'])}", pt(e["ciclo_efetivo"], 2), pt(e["capacidade"]), pt(f["capacidade"])] for e, f in zip(c3["estacoes"], c2["estacoes"])])
print("ok: relatorio/tabelas/*.tex")
