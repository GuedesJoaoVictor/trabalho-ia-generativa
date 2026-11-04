"""Confere o texto do grupo contra os números do sistema (não escreve nada, só aponta).
Uso: .venv/bin/python conferir_relatorio.py relatorio/relatorio.tex [apresentacao/apresentacao.tex ...]
Aponta: números sem correspondência no plano/ferramentas (com o valor mais próximo), seções do enunciado que faltam,
legendas/fontes vazias e % TODO restantes. Número sem correspondência não é erro: pode ser fonte externa. Confira à mão."""
import json
import re
import sys

import ferramentas as F

# --- valores de referência: tudo que o sistema calcula (nome -> valor)
REF = {}


def coletar(o, caminho):
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        REF[caminho] = float(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            coletar(v, f"{caminho}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            coletar(v, f"{caminho}[{i}]")


plano = json.load(open("plano.json", encoding="utf-8"))
for k in ("consolidado", "externo"):
    coletar(plano[k], k)
for p in plano["propostas"]:
    coletar({k: p[k] for k in ("impacto_mensal", "impacto_unico", "custo_unico", "prazo_meses")}, p["id"])
chamadas = {"margem": F.margem_por_modelo, "fluxo": F.fluxo_base, "pendentes": F.pendentes, "dividendos": F.passivo_dividendos,
            "folha": F.folha, "cap3": lambda: F.capacidade_linha(3), "cap2": lambda: F.capacidade_linha(2),
            "qualidade": F.qualidade_linha, "leadtime": F.leadtime_criticos, "cambio": lambda: F.sensibilidade_cambio(10),
            "turnos_cons": lambda: F.cenario_turnos(2, 4), "turnos_cent": lambda: F.cenario_turnos(2, 3),
            "turnos_otim": lambda: F.cenario_turnos(2, 2), "premissas": lambda: F.PREMISSAS}
for nome, f in chamadas.items():
    try:
        coletar(f(), nome)
    except Exception as e:  # ferramenta mudou de assinatura: avisa e segue
        print(f"aviso: não coletei {nome}: {e}")

MULT = {"mi": 1e6, "milhão": 1e6, "milhões": 1e6, "milhao": 1e6, "milhoes": 1e6, "mil": 1e3}
NUM = re.compile(r"(?<![\w\-.,/\\])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)\s*(milhões|milhão|milhoes|milhao|mi\b|mil\b|\\?%|x\b)?")
LIXO = re.compile(r"\\(vspace|hspace|column|rule|fontsize|fig|includegraphics|vskip|stat\[?\w*\]?)\*?(\[[^\]]*\])?(\{[^}]*\})*|\\\\\[[^\]]*\]|"
                  r"\\(cite\w*|ref|label|autoref|pageref)\{[^}]*\}|(Figura|Tabela|Quadro|seção|capítulo|p\.|pág\.|fig\.)\s*\d+(\.\d+)*")


def candidatos(v, un):
    m = MULT.get(un, 1.0)
    return [v * m, v * m / 100] if un in ("%", "\\%") else [v * m]


def conferir(arq):
    txt = open(arq, encoding="utf-8").read()
    linhas = []
    for i, l in enumerate(txt.splitlines(), 1):
        if re.match(r"\s*\\(documentclass|usepackage|setbeamer|definecolor|newcommand|renewcommand|set\w*font|graphicspath|input|include)", l):
            continue
        l = re.sub(r"(?<!\\)%.*", "", l)
        linhas.append((i, LIXO.sub(" ", l)))
    sem, ok = [], 0
    for i, l in linhas:
        for m in NUM.finditer(l):
            bruto, un = m.group(1), (m.group(2) or "").strip()
            v = float(bruto.replace(".", "").replace(",", "."))
            casas = len(bruto.split(",")[1]) if "," in bruto else 0
            if not un and 1900 <= v <= 2100:  # ano
                continue
            tol = 0.5 * 10 ** -casas * MULT.get(un, 1.0) * (1 / 100 if un in ("%", "\\%") else 1) + 1e-9
            alvos = candidatos(v, un)
            achou = any(abs(a - abs(r)) <= max(tol, abs(r) * 0.0005) for a in alvos for r in REF.values())
            if achou:
                ok += 1
            else:
                nome, val = min(REF.items(), key=lambda kv: min(abs(kv[1] - a) / (abs(kv[1]) + 1e-9) for a in alvos))
                sem.append((i, m.group(0).strip(), nome, val))
    print(f"\n=== {arq}: {ok} números confirmados, {len(sem)} sem correspondência ===")
    for i, t, n, v in sem:
        print(f"  linha {i}: '{t}' (mais próximo: {n} = {v:,.4g})")
    return txt


NECESSARIO = {"introdução": r"introdu", "IA generativa/LLMs": r"generativ|LLM", "agente único vs multiagentes": r"multi-?agente|multiagente",
              "engenharia de prompt": r"prompt", "tool use": r"tool use|uso de ferramentas|chamada de ferramentas", "RAG": r"\bRAG\b",
              "otimização": r"otimiza", "resultados da entrevista": r"entrevista", "arquitetura": r"arquitetura", "análise dos dados": r"an[áa]lise dos dados",
              "soluções e impacto": r"impacto", "conclusão": r"conclus", "refugo/gargalo": r"refugo|gargalo", "referências": r"refer[êe]ncias|\\bibliography"}
for arq in sys.argv[1:] or ["relatorio/relatorio.tex"]:
    t = conferir(arq)
    if "relatorio" in arq:
        falta = [k for k, rx in NECESSARIO.items() if not re.search(rx, t, re.I)]
        print("  tópicos do enunciado que não aparecem:", ", ".join(falta) or "nenhum")
        print("  legendas/fontes vazias:", len(re.findall(r"\\(caption|fonte)\{\s*(%[^\n]*)?\n?\s*\}", t)), "| % TODO restantes:", t.count("TODO"))
