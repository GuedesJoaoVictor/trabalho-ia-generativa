"""Roda o sistema de agentes e grava plano.json, plano-consolidado.md e as figuras.

Uso:  .venv/bin/python executar.py          # modo determinístico (sem chave)
      .venv/bin/python executar.py --llm    # + pareceres via API (GEMINI_API_KEY ou ANTHROPIC_API_KEY)
      .venv/bin/python executar.py --local  # + pareceres com modelo local (Ollama, MODELO_LOCAL=qwen3:4b)
"""
import json
import sys
from dataclasses import asdict

import agentes
import figuras

r = lambda x: f"R$ {x:,.0f}".replace(",", ".")


def md(plano, pareceres=None):
    c, ext = plano["consolidado"], plano["externo"]
    cot = ext["cotacoes"]
    L = ["# Saída do sistema de agentes: plano consolidado",
         "", "Gerado por `executar.py` (tabelas e números vêm das ferramentas; texto das propostas vem dos agentes). "
         "Resultado de máquina, não é o relatório.", "",
         "## Situação de partida (12 meses)", "",
         f"- Lucro bruto das entregas (proxy de caixa operacional): **{r(c['base_mensal'])}/mês**.",
         f"- Compromisso de dividendos (corrente + atrasados em 24 meses, com Selic): **{r(c['saida_dividendos'])}/mês**.",
         f"- Cobertura sem o plano: **{c['cobertura_sem_plano']:.2f}x**; com o plano: **{c['cobertura_com_plano']:.2f}x**.",
         "- O lucro bruto não desconta despesas fora do custo direto nem outras dívidas: é uma folga máxima, não o caixa real.", "",
         "## Dados externos (Banco Central)", "",
         f"Consulta em {cot['consultado_em']}: Selic meta {cot['selic_meta_aa']['valor']}% a.a.; dólar R$ {cot['usd_brl']['valor']}; "
         f"euro R$ {cot['eur_brl']['valor']}; IPCA do mês {cot['ipca_mes']['valor']}%.", "",
         "| Parcela em atraso | Principal | Meses | Correção Selic |", "|---|---|---|---|"]
    L += [f"| {p['mes']} | {r(p['principal'])} | {p['meses_atraso']} | {r(p['encargos'])} |" for p in ext["encargos"]["parcelas"]]
    L += [f"| **Total** | **{r(ext['encargos']['principal'])}** | | **{r(ext['encargos']['encargos'])}** |", "",
          "## Propostas e parecer do Revisor", "",
          "| ID | Agente | Proposta | Mensal | Pontual | Desembolso | Prazo | Parecer |", "|---|---|---|---|---|---|---|---|"]
    for p in plano["propostas"]:
        L.append(f"| {p.id} | {p.agente} | {p.titulo} | {r(p.impacto_mensal)} | {r(p.impacto_unico)} | {r(p.custo_unico)} | {p.prazo_meses:g} m | **{p.status}** |")
    L += ["", "### Detalhe", ""]
    for p in plano["propostas"]:
        L += [f"**{p.id} {p.titulo}** ({p.status})", "", p.descricao, ""]
        if p.hipoteses:
            L += ["Hipóteses:"] + [f"- {h}" for h in p.hipoteses] + [""]
        if p.motivos:
            L += ["Revisor:"] + [f"- {m}" for m in p.motivos] + [""]
        L += ["Fontes: " + "; ".join(p.fontes), ""]
    L += ["## Projeção de 12 meses (proxy de caixa)", "",
          f"Saldo mínimo {r(c['saldo_minimo'])}; saldo em 12 meses {r(c['saldo_12m'])}. Entradas pontuais somadas: {r(c['unicos'])}; desembolsos: {r(c['custos_unicos'])}.", "",
          "| Mês | Lucro bruto base | Melhorias | Pontual | Dividendos | Saldo acumulado |", "|---|---|---|---|---|---|"]
    L += [f"| {l['mes']} | {r(l['base'])} | {r(l['melhorias'])} | {r(l['unico'])} | {r(l['saida'])} | {r(l['saldo_acumulado'])} |" for l in c["projecao"]]
    if pareceres:
        L += ["", "## Pareceres dos agentes Claude (modo LLM)", ""]
        for k, v in pareceres.items():
            L += [f"### {k}", "", v, ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    plano = agentes.orquestrar()
    pareceres = agentes.parecer_llm(plano, local="--local" in sys.argv) if ("--llm" in sys.argv or "--local" in sys.argv) else None
    figuras.gerar_todas(plano)
    open("plano-consolidado.md", "w", encoding="utf-8").write(md(plano, pareceres))
    json.dump(dict(consolidado=plano["consolidado"], externo=plano["externo"], propostas=[asdict(p) for p in plano["propostas"]],
                   pareceres=pareceres), open("plano.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("ok: plano-consolidado.md, plano.json, figuras/")
