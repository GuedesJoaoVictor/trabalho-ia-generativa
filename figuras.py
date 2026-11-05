"""Gera as figuras (PNG) em figuras/ a partir das mesmas ferramentas do sistema. Sem legenda numerada:
título curto na imagem; numeração, legenda e fonte ficam para o texto do relatório (MDT)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

import ferramentas as F
from dados import planilha

OUT = "figuras"
AZUL, LARANJA, CINZA, VERDE, VERMELHO = "#1f5fa8", "#e08a1e", "#8a8f98", "#2e8b57", "#c0392b"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
M = lambda x, _=None: f"{x / 1e6:.1f}".replace(".", ",")  # milhões


def _salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{nome}.png")
    plt.close(fig)


def arquitetura():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11.6)
    ax.set_ylim(-0.3, 8)
    ax.axis("off")

    def caixa(x, y, w, h, txt, cor, tc="white", fs=9.5):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12", fc=cor, ec="none"))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", color=tc, fontsize=fs, wrap=True)

    def seta(x1, y1, x2, y2, tracejada=False):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color="#444",
                                     linestyle="--" if tracejada else "-", lw=1.1))

    caixa(0.3, 7.0, 3.2, 0.7, "Planilha do cliente (.xlsx)\n7 abas", CINZA)
    caixa(3.9, 7.0, 3.2, 0.7, "Entrevista com o cliente\n(restrições e prioridades)", CINZA)
    caixa(7.5, 7.0, 3.2, 0.7, "Dados externos\nAPI do Banco Central · busca na web", CINZA)
    caixa(3.3, 5.7, 4.4, 0.8, "Orquestrador\nplaneja, distribui, consolida o plano", AZUL)
    nomes = ["Coleta\nExterna", "Financeiro", "Operações", "Suprimentos", "Mercado"]
    xs = [0.3, 2.5, 4.7, 6.9, 9.1]
    for x, n in zip(xs, nomes):
        caixa(x, 3.9, 1.7, 0.9, n, LARANJA)
        seta(5.5, 5.7, x + 0.85, 4.8)
    caixa(0.3, 2.45, 10.4, 0.8, "Ferramentas (tool use): cálculo em Python sobre a planilha · margem · capacidade · dividendos\n"
          "multa · lead time · câmbio · Selic · busca na web", "#4a4f57")
    for x in xs:
        seta(x + 0.85, 3.9, x + 0.85, 3.25, True)
    seta(1.9, 7.0, 3.9, 6.5)
    seta(5.5, 7.0, 5.5, 6.5)
    seta(9.1, 7.0, 7.0, 6.5)
    caixa(3.3, 1.15, 4.4, 0.8, "Revisor\nrecalcula, aplica as regras do cliente", VERDE)
    seta(5.5, 2.45, 5.5, 1.95)
    ax.add_patch(FancyArrowPatch((7.7, 1.55), (11.0, 1.55), arrowstyle="-", color="#444", lw=1.1, linestyle="--"))
    ax.add_patch(FancyArrowPatch((11.0, 1.55), (11.0, 6.1), arrowstyle="-", color="#444", lw=1.1, linestyle="--"))
    seta(11.0, 6.1, 7.7, 6.1, True)
    ax.text(11.15, 3.8, "reprovada: volta\ncom o motivo", rotation=90, ha="left", va="center", fontsize=8, color="#444")
    caixa(3.3, 0.0, 4.4, 0.7, "Plano consolidado (12 meses)", AZUL)
    seta(5.5, 1.15, 5.5, 0.7)
    _salvar(fig, "01_arquitetura")


def margem():
    mm = F.margem_por_modelo()
    nomes = [m["cod"].replace("BUS-", "") for m in mm]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = range(len(mm))
    ax.bar([i - 0.2 for i in x], [m["margem_catalogo"] * 100 for m in mm], 0.4, label="Preço de catálogo", color=AZUL)
    ax.bar([i + 0.2 for i in x], [m["margem_praticada"] * 100 for m in mm], 0.4, label="Preço praticado nos pedidos", color=LARANJA)
    for i, m in enumerate(mm):
        ax.text(i - 0.2, m["margem_catalogo"] * 100 + 0.4, f"{m['margem_catalogo'] * 100:.1f}".replace(".", ","), ha="center", fontsize=8)
        ax.text(i + 0.2, m["margem_praticada"] * 100 + 0.4, f"{m['margem_praticada'] * 100:.1f}".replace(".", ","), ha="center", fontsize=8)
    ax.set_xticks(list(x), nomes)
    ax.set_ylabel("Margem sobre o preço (%)")
    ax.set_ylim(0, 38)
    ax.set_title("Margem bruta por modelo")
    ax.legend(frameon=False)
    _salvar(fig, "02_margem_modelos")


def carteira():
    ped = planilha()["pedidos"]
    meses = list(dict.fromkeys(p["mes"] for p in ped))
    sts = [("Entregue", AZUL), ("Em Produção", LARANJA), ("Pendente / Atrasado", VERMELHO)]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    base = [0.0] * len(meses)
    for st, cor in sts:
        v = [sum(p["qtd"] for p in ped if p["mes"] == m and p["status"] == st) for m in meses]
        ax.bar(meses, v, bottom=base, label=st, color=cor)
        base = [a + b for a, b in zip(base, v)]
    ax.set_ylabel("Ônibus pedidos")
    ax.set_title("Pedidos por mês e situação")
    ax.legend(frameon=False)
    _salvar(fig, "03_carteira_pedidos")


def capacidade():
    c3, c2 = F.capacidade_linha(3), F.capacidade_linha(2)
    curtos = ["Corte", "Armação", "Pintura", "Chapas", "Vidros", "Elétrica", "Tapeçaria", "Chassi"]
    nomes = [f"{e['etapa']}\n{n}" for e, n in zip(c3["estacoes"], curtos)]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    x = range(len(nomes))
    ax.bar([i - 0.2 for i in x], [e["capacidade"] for e in c3["estacoes"]], 0.4, label="3 turnos", color=AZUL)
    ax.bar([i + 0.2 for i in x], [e["capacidade"] for e in c2["estacoes"]], 0.4, label="2 turnos", color=LARANJA)
    ax.axhline(c3["demanda_pico"], color=VERMELHO, ls="--", lw=1.5, label=f"Pico de pedidos ({c3['demanda_pico']:.0f}/mês)")
    ax.axhline(c3["demanda_media"], color="#333", ls=":", lw=1.5, label=f"Média de pedidos ({c3['demanda_media']:.0f}/mês)")
    ax.set_xticks(list(x), nomes, fontsize=9)
    ax.set_ylabel("Capacidade teórica (ônibus/mês)")
    ax.set_title("Capacidade teórica por estação (ciclo efetivo; etapa 80 limitada a 16 h)")
    ax.legend(frameon=False, loc="upper right")
    _salvar(fig, "04_capacidade_linha")


def qualidade():
    linha = planilha()["linha"]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    nomes = [f"{int(e['etapa'])}" for e in linha]
    cores = [VERMELHO if e["refugo"] >= 0.05 else AZUL for e in linha]
    ax.bar(nomes, [e["refugo"] * 100 for e in linha], color=cores)
    for i, e in enumerate(linha):
        ax.text(i, e["refugo"] * 100 + 0.15, f"{e['refugo'] * 100:.1f}".replace(".", ","), ha="center", fontsize=8)
    ax.set_xlabel("Etapa da linha")
    ax.set_ylabel("Refugo/retrabalho (% do tempo de ciclo)")
    ax.set_title("Refugo e retrabalho por etapa (vermelho: acima de 5%)")
    _salvar(fig, "05_refugo_etapas")


def _curto(txt, n=32):
    return txt if len(txt) <= n else txt[:n].rsplit(" ", 1)[0] + "…"


def leadtime():
    r = F.leadtime_criticos()["ranking"][::-1]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    cor = lambda t: VERMELHO if not t.startswith("Sim") else AZUL
    ax.barh([f"{_curto(p['desc'])} ({p['pais'].split(' /')[0]})" for p in r], [p["lead"] for p in r], color=[cor(p["troca"]) for p in r])
    ax.set_xlabel("Lead time (dias)")
    ax.set_title("Lead time por peça (vermelho: não pode ser trocada)")
    ax.tick_params(axis="y", labelsize=8)
    _salvar(fig, "06_leadtime_pecas")


def caixa(plano):
    c = plano["consolidado"]
    pj = c["projecao"]
    meses = [l["mes"] for l in pj]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    a1.bar(meses, [l["base"] + l["melhorias"] for l in pj], color=AZUL, label="Lucro bruto das entregas + melhorias", zorder=1)
    a1.plot(meses, [l["saida"] for l in pj], color=VERMELHO, lw=2.5, label="Dividendos (corrente + atrasados em 24 m)", zorder=3)
    a1.yaxis.set_major_formatter(M)
    a1.set_ylabel("R$ milhões por mês")
    a1.set_xlabel("Mês do plano")
    a1.set_title("Entrada x compromisso mensal")
    a1.set_ylim(0, max(l["base"] + l["melhorias"] for l in pj) * 1.35)
    a1.legend(frameon=False, fontsize=8, loc="upper center")
    sem = [(l["base"] - l["saida"]) * l["mes"] for l in pj]
    a2.plot(meses, sem, color=CINZA, ls="--", lw=2, label="Sem plano")
    a2.plot(meses, [l["saldo_acumulado"] for l in pj], color=VERDE, lw=2, label="Com plano")
    a2.yaxis.set_major_formatter(M)
    a2.set_ylabel("R$ milhões acumulados")
    a2.set_xlabel("Mês do plano")
    a2.set_title("Saldo acumulado (proxy de caixa)")
    a2.legend(frameon=False, fontsize=8)
    _salvar(fig, "07_caixa_dividendos")


def gerar_todas(plano):
    for f in (arquitetura, margem, carteira, capacidade, qualidade, leadtime):
        f()
    caixa(plano)
