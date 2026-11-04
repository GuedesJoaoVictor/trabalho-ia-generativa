"""Sistema multiagentes: Coleta Externa, Financeiro, Operações, Suprimentos, Mercado, Revisor e Orquestrador.

Modo padrão (determinístico): cada agente chama suas ferramentas por código e devolve propostas com número.
Modo LLM (`--llm`, exige ANTHROPIC_API_KEY): cada especialista vira um agente Claude que escolhe e chama as
mesmas ferramentas (tool use) e escreve um parecer; o Revisor LLM critica o plano. NÃO foi executado ainda
(sem chave no ambiente de desenvolvimento): testar antes de usar.
"""
import functools
import inspect
import json
import os
from dataclasses import asdict, dataclass, field

import ferramentas as F
from dados import planilha

PR = F.PREMISSAS


@dataclass
class Proposta:
    id: str
    agente: str
    titulo: str
    descricao: str
    tipo: str = "acao"           # acao | demissao | troca_fornecedor | reducao_producao | compromisso | fase2
    impacto_mensal: float = 0.0  # R$/mês recorrente (+ melhora o resultado)
    impacto_unico: float = 0.0   # R$ pontuais (+ entrada)
    custo_unico: float = 0.0     # R$ de desembolso para executar
    prazo_meses: float = 1.0
    fontes: list = field(default_factory=list)
    hipoteses: list = field(default_factory=list)
    afirmacoes: dict = field(default_factory=dict)  # rótulo -> valor que o Revisor recalcula do zero
    pecas: list = field(default_factory=list)       # códigos de peças afetadas
    dados: dict = field(default_factory=dict)       # números de apoio
    requer_validacao: str = ""   # ex.: parecer jurídico
    status: str = "pendente"     # preenchido pelo Revisor: aprovada | condicional | reprovada
    motivos: list = field(default_factory=list)


# ============================================================ agentes especialistas
def agente_coleta_externa() -> dict:
    """Busca dados externos (Banco Central) e devolve índices e a correção Selic dos dividendos atrasados."""
    return dict(cotacoes=F.cotacoes_bcb(), encargos=F.encargos_atrasados_selic())


def agente_financeiro(ext: dict) -> list:
    pas, pend, fl = F.passivo_dividendos(), F.pendentes(), F.folha()
    enc = ext["encargos"]["encargos"]
    plano = F.plano_dividendos(encargos=enc)
    ele = next(m for m in F.margem_por_modelo() if m["cod"] == "BUS-ELE-12M")
    inv = F.leadtime_criticos()
    dir_ = fl["niveis"]["Diretoria"]
    return [
        Proposta("FIN-1", "Financeiro", "Regularizar dividendos: corrente em dia e atrasados em 24 meses", tipo="compromisso",
                 descricao="Pagar o dividendo corrente todo mês e quitar em 24 meses o exigível (atraso PN + exigência judicial) "
                           "com correção Selic, condição dada pelo cliente para afastar o bloqueio pela B3.",
                 impacto_mensal=-plano["parcela_mensal"], prazo_meses=1,
                 fontes=["passivo_dividendos", "plano_dividendos", "encargos_atrasados_selic", "aba Dividendos e Passivos", "BCB SGS 4390"],
                 hipoteses=["Correção pela Selic acumulada (índice de referência; juros e multa reais não informados)",
                            "Dividendos ON suspensos (R$ 10,8 mi) ficam fora da quitação; confirmar com o cliente",
                            "Dividendo corrente = média mensal do cronograma da planilha, com as ações atuais"],
                 afirmacoes=dict(dividendos_total_12m=pas["total"], dividendos_exigivel=pas["exigivel"]),
                 dados=dict(plano, encargos_selic=enc, passivo=pas)),
        Proposta("FIN-2", "Financeiro", "Priorizar a entrega dos 27 pedidos pendentes",
                 descricao="Prefeitura só paga na entrega: os pendentes seguram a receita e geram multa (10% + 0,1%/dia). "
                           "Destravá-los é a maior alavanca de caixa de curto prazo.",
                 impacto_unico=pend["lucro"], prazo_meses=2,
                 fontes=["pendentes", "multa_pendentes", "aba Pedidos por Mês"],
                 hipoteses=["Lucro = preço praticado − custo direto (já inclui mão de obra e impostos, segundo o cliente)",
                            "Dias de atraso e a causa de cada pendente não constam da planilha"],
                 afirmacoes=dict(receita_pendentes=pend["receita"], lucro_pendentes=pend["lucro"], multa_fixa_pendentes=pend["multa_fixa"]),
                 dados=dict(pend, multa_30d=F.multa_pendentes(30)["total"])),
        Proposta("FIN-3", "Financeiro", "Reduzir a produção do elétrico para aliviar caixa (alternativa avaliada)", tipo="reducao_producao",
                 descricao="O cliente aceita reduzir o elétrico se for preciso para estabilizar a empresa. Corte de 50% por 12 meses: "
                           "compara o lucro perdido com o capital que deixa de ficar parado no inversor.",
                 prazo_meses=2, fontes=["margem_por_modelo", "leadtime_criticos"],
                 hipoteses=["Capital liberado = metade do capital em trânsito do inversor (60 dias de lead time)"],
                 afirmacoes=dict(lucro_unid_ele=ele["lucro_unid"]),
                 dados=dict(lucro_perdido_12m=0.5 * ele["lucro_12m"], capital_liberado=0.5 * inv["capital_em_transito"])),
        Proposta("FIN-4", "Financeiro", "Revisar a remuneração da diretoria (-20%)",
                 descricao=f"A diretoria ({dir_['pessoas']} pessoas) custa R$ {dir_['custo_mensal']:,.0f}/mês, "
                           f"{dir_['custo_mensal'] / fl['total_mensal']:.1%} da folha.".replace(",", "."),
                 impacto_mensal=0.20 * dir_["custo_mensal"], prazo_meses=2, fontes=["folha", "aba Folha e Absenteísmo"],
                 hipoteses=["Redução de 20% é cenário, não recomendação fechada"],
                 requer_validacao="Parecer jurídico: irredutibilidade salarial (CLT) e vínculo da diretoria (CLT ou estatutário)",
                 afirmacoes=dict(custo_diretoria_mensal=dir_["custo_mensal"])),
    ]


def agente_operacoes() -> list:
    q = F.qualidade_linha()
    cons, cen = F.cenario_turnos(2, 4), F.cenario_turnos(2, 3)
    amplo = F.cenario_turnos(2, 2)
    return [
        Proposta("OPE-1", "Operações", "Operar em 2 turnos (3º turno só nos picos) e dimensionar o quadro de operadores", tipo="demissao",
                 descricao=f"Com 2 turnos a linha comporta {cen['capacidade']:.0f} veículos/mês contra pico de {cen['demanda_pico']:.0f}. "
                           f"Excedente de operadores: {cons['excedente']} (equipe de 4 por estação, conservador), {cen['excedente']} (3, central), "
                           f"{amplo['excedente']} (2). Realocar para manutenção e qualidade antes de desligar; demitir só o que sobrar.",
                 impacto_mensal=cons["economia_mensal"], custo_unico=cons["custo_rescisao"], prazo_meses=3,
                 fontes=["cenario_turnos", "capacidade_linha", "folha", "aba Linha de Montagem", "aba Folha e Absenteísmo"],
                 hipoteses=["Pessoas simultâneas por estação desconhecidas: 4 (conservador), 3 (central), 2 (otimista)",
                            "Ocupação produtiva de 75% e 20% extra para manutenção das máquinas de segunda mão",
                            f"Rescisão = {PR['rescisao_salarios']} salários base (aviso, multa de 40% do FGTS, 13º e férias proporcionais)",
                            "Quadro calculado pela carga de trabalho, não por escala de turno: validar a escala real",
                            "Capacidade teórica: não considera paradas das máquinas de segunda mão"],
                 afirmacoes=dict(capacidade_2_turnos=cen["capacidade"], custo_medio_operador=cons["economia_mensal"] / cons["excedente"],
                                 demanda_pico=cen["demanda_pico"]),
                 dados=dict(conservador=cons, central=cen, otimista=amplo)),
        Proposta("OPE-2", "Operações", "Manutenção preventiva e padrão de trabalho nas etapas 20, 50 e 60",
                 descricao="As três etapas com refugo/retrabalho acima de 5% concentram a maior parte das horas perdidas. "
                           "Meta: cortar 50% delas, usando operadores realocados da OPE-1.",
                 impacto_mensal=0.5 * q["custo_mensal_retrabalho"], prazo_meses=3,
                 fontes=["qualidade_linha", "aba Linha de Montagem"],
                 hipoteses=["Custo/hora do operador e equipe de 3 por estação (premissas)",
                            "Ganho financeiro direto é pequeno: o retrabalho é 4% do ciclo; o ganho maior é entregar no prazo"],
                 afirmacoes=dict(horas_perdidas_por_veiculo=q["horas_perdidas_por_veiculo"]), dados=q),
    ]


def agente_suprimentos() -> list:
    lt, pend = F.leadtime_criticos(), F.pendentes()
    cambio = F.sensibilidade_cambio(10)
    dias = 15
    return [
        Proposta("SUP-1", "Suprimentos", "Comprar as peças longas no ato do pedido firme (ar-condicionado 45 d, portas 30 d, inversor 60 d)",
                 descricao="Alinhar o calendário de compras à carteira firme, sem estoque especulativo (cliente: estocar é inviável). "
                           f"Cada dia de atraso evitado nos pendentes poupa R$ {pend['multa_por_dia']:,.0f} de multa.".replace(",", "."),
                 impacto_unico=dias * pend["multa_por_dia"], prazo_meses=1,
                 fontes=["leadtime_criticos", "multa_pendentes", "aba Catálogo de Peças"],
                 hipoteses=[f"Antecipar as compras evita {dias} dias de multa diária (hipótese)",
                            "O capital em trânsito já existe no ciclo atual: nenhuma peça é estocada"],
                 afirmacoes=dict(multa_por_dia=pend["multa_por_dia"]), dados=lt),
        Proposta("SUP-2", "Suprimentos", "Cotar alternativas para ar-condicionado (Thermo King) e portas (Bode)", tipo="troca_fornecedor",
                 descricao="São as peças com maior lead time depois do inversor e as únicas importadas que o cliente permite trocar "
                           "(aviso de 30 dias). Cotar fornecedores nacionais ou com menor prazo; a troca só vale se reduzir prazo ou custo.",
                 prazo_meses=3, pecas=["PEC-MOT-301", "PEC-PORT-501"], fontes=["leadtime_criticos", "sensibilidade_cambio", "BCB SGS 1 e 21619"],
                 hipoteses=["Sem cotação real, o ganho não é somado ao plano; exposição cambial mostrada como risco"],
                 afirmacoes=dict(exposicao_cambial_10pct=cambio["custo_extra_mensal"]), dados=cambio),
        Proposta("SUP-3", "Suprimentos", "Elétrico só contra pedido firme e negociar pagamento do inversor na entrega",
                 descricao=f"O inversor/bateria (R$ 480 mil, 60 dias, sem produtor nacional) prende cerca de R$ {lt['capital_em_transito']:,.0f} "
                           "em trânsito. Condição de pagamento da CATL não informada; é a negociação a abrir.".replace(",", "."),
                 prazo_meses=3, pecas=[], fontes=["leadtime_criticos", "aba Catálogo de Peças"],
                 hipoteses=["Capital liberado possível, não somado ao plano (depende da negociação)"],
                 afirmacoes=dict(capital_inversor_transito=lt["capital_em_transito"]), dados=dict(capital=lt["capital_em_transito"])),
    ]


def agente_mercado() -> list:
    op = F.oportunidades_mercado()
    topo = op["modelos"][:3]
    return [
        Proposta("MER-1", "Mercado", "Priorizar a venda dos modelos de maior lucro por ônibus (frotas sequenciais para prefeituras)",
                 descricao="O lucro por ônibus varia de R$ 109 mil (micro) a R$ 496 mil (elétrico). Cada ônibus a mais por mês "
                           "do rodoviário vale R$ 439 mil de lucro bruto por mês; é sensibilidade, não previsão.",
                 prazo_meses=6, fontes=["oportunidades_mercado", "margem_por_modelo"],
                 hipoteses=["Demanda fora de Santa Maria não existe na planilha: o potencial vem da pesquisa externa (modo LLM)",
                            "Não somado ao plano: depende de novos contratos"],
                 afirmacoes=dict(lucro_unid_rodoviario=next(m for m in op["modelos"] if m["cod"] == "BUS-ROD-14M")["lucro_unid"]),
                 dados=dict(modelos=op["modelos"], prioridade=[m["cod"] for m in topo])),
        Proposta("MER-2", "Mercado", "Fase 2: double-deck e novos segmentos", tipo="fase2",
                 descricao="Fora do horizonte financeiro: o cliente quer primeiro a empresa no verde.",
                 prazo_meses=24, fontes=["respostas do cliente"], dados=dict(itens=op["fase2"])),
    ]


# ============================================================ revisor
def _recalc():
    """Recálculo independente (direto da planilha, sem passar por ferramentas.py)."""
    P = planilha()
    ped = P["pedidos"]
    custo = {m["cod"]: m["custo"] for m in P["modelos"]}
    pend = [p for p in ped if p["status"] == "Pendente / Atrasado"]
    receita_p = sum(p["qtd"] * p["preco"] for p in pend)
    op = [f for f in P["folha"] if f["nivel"] == "Operacional"]
    ele = [p for p in ped if p["modelo"] == "BUS-ELE-12M"]
    ele_q, ele_v = sum(p["qtd"] for p in ele), sum(p["qtd"] * p["preco"] for p in ele)
    est = [16 * 30 / (e["ciclo"] * (1 + e["refugo"])) for e in P["linha"]]  # 2 turnos de 8 h
    mes = {}
    for p in ped:
        mes[p["mes"]] = mes.get(p["mes"], 0) + p["qtd"]
    imp = sum(b["qtd"] * b["custo"] * sum(p["qtd"] for p in ped if p["modelo"] == b["modelo"]) / 12
              for b in P["bom"] if next(x for x in P["pecas"] if x["cod"] == b["peca"])["pais"] != "Brasil")
    div = [d["acoes"] * d["dps"] for d in P["dividendos"]]
    return {
        "dividendos_total_12m": sum(div),
        "dividendos_exigivel": sum(d["acoes"] * d["dps"] for d in P["dividendos"]
                                   if d["status"] in ("Acumulado em Atraso", "Exigência Judicial dos Minoritários")),
        "receita_pendentes": receita_p,
        "lucro_pendentes": sum(p["qtd"] * (p["preco"] - custo[p["modelo"]]) for p in pend),
        "multa_fixa_pendentes": 0.10 * receita_p,
        "multa_por_dia": 0.001 * receita_p,
        "lucro_unid_ele": ele_v / ele_q - custo["BUS-ELE-12M"],
        "lucro_unid_rodoviario": (lambda r: sum(p["qtd"] * p["preco"] for p in r) / sum(p["qtd"] for p in r) - custo["BUS-ROD-14M"])(
            [p for p in ped if p["modelo"] == "BUS-ROD-14M"]),
        "custo_diretoria_mensal": 1.45 * sum(f["salario"] for f in P["folha"] if f["nivel"] == "Diretoria"),
        "custo_medio_operador": 1.45 * sum(f["salario"] for f in op) / len(op),
        "capacidade_2_turnos": min(est),
        "demanda_pico": max(mes.values()),
        "horas_perdidas_por_veiculo": sum(e["ciclo"] * e["refugo"] for e in P["linha"]),
        "exposicao_cambial_10pct": imp * 0.10,
        "capital_inversor_transito": ele_q / 12 * 480000 * 60 / 30,
    }


def revisor(propostas: list) -> list:
    """Valida cada proposta. aprovada | condicional (exige ação do cliente/grupo) | reprovada."""
    rec = _recalc()
    for p in propostas:
        rep, cond = [], []
        if not p.fontes:
            rep.append("sem fonte rastreável")
        if p.tipo != "fase2" and p.prazo_meses > PR["horizonte_meses"]:
            rep.append(f"prazo {p.prazo_meses} m acima do limite de {PR['horizonte_meses']} meses do cliente")
        for rot, val in p.afirmacoes.items():
            if rot not in rec:
                rep.append(f"'{rot}' sem recálculo independente")
            elif abs(val - rec[rot]) > 0.005 * abs(rec[rot]):
                rep.append(f"'{rot}': agente {val:,.2f} x recálculo {rec[rot]:,.2f}")
        if p.tipo == "demissao":
            if p.custo_unico <= 0:
                rep.append("demissão sem custo de rescisão (vínculo CLT)")
            elif p.impacto_mensal > 0:
                cond.append(f"rescisão de R$ {p.custo_unico:,.0f} com caixa zero: indicar fonte; retorno em {p.custo_unico / p.impacto_mensal:.1f} meses")
        if p.tipo == "troca_fornecedor":
            if {"PEC-ELE-401", "PEC-ELE-402"} & set(p.pecas):
                rep.append("peça não substituível (chicote Yazaki fixo; inversor sem produtor nacional)")
            if p.prazo_meses < 1:
                rep.append("troca exige aviso de 30 dias")
        if p.tipo == "reducao_producao":
            liq = p.dados["capital_liberado"] - p.dados["lucro_perdido_12m"]
            if liq <= 0:
                rep.append(f"lucro perdido em 12 meses (R$ {p.dados['lucro_perdido_12m']:,.0f}) supera o capital liberado "
                           f"(R$ {p.dados['capital_liberado']:,.0f}); o elétrico tem o maior lucro por ônibus")
        if p.tipo != "demissao" and p.custo_unico > 0:
            cond.append(f"desembolso de R$ {p.custo_unico:,.0f} com caixa zero: indicar fonte")
        if p.requer_validacao:
            cond.append(p.requer_validacao)
        p.motivos = rep + cond
        p.status = "reprovada" if rep else "condicional" if cond else "aprovada"
    return propostas


# ============================================================ orquestrador
def consolidar(propostas: list, ext: dict) -> dict:
    """Junta as propostas válidas e projeta 12 meses de caixa operacional (proxy) contra os compromissos."""
    ok = [p for p in propostas if p.status in ("aprovada", "condicional") and p.tipo != "fase2"]
    comp = next(p for p in ok if p.tipo == "compromisso")
    base = F.fluxo_base()["lucro_entregue_mensal"]
    saida = comp.dados["saida_mensal"]
    melhorias = [p for p in ok if p.tipo != "compromisso"]
    saldo, linhas = 0.0, []
    for m in range(1, PR["horizonte_meses"] + 1):
        rec = sum(p.impacto_mensal for p in melhorias if m > p.prazo_meses)
        unico = sum(p.impacto_unico for p in melhorias if m == p.prazo_meses) - sum(p.custo_unico for p in melhorias if m == p.prazo_meses)
        saldo += base + rec - saida + unico
        linhas.append(dict(mes=m, base=base, melhorias=rec, unico=unico, saida=saida, saldo_acumulado=saldo))
    return dict(base_mensal=base, saida_dividendos=saida, cobertura_sem_plano=base / saida,
                cobertura_com_plano=(base + sum(p.impacto_mensal for p in melhorias)) / saida,
                melhorias_mensais=sum(p.impacto_mensal for p in melhorias),
                unicos=sum(p.impacto_unico for p in melhorias), custos_unicos=sum(p.custo_unico for p in melhorias),
                saldo_12m=saldo, saldo_minimo=min(l["saldo_acumulado"] for l in linhas), projecao=linhas)


def orquestrar() -> dict:
    ext = agente_coleta_externa()
    propostas = agente_financeiro(ext) + agente_operacoes() + agente_suprimentos() + agente_mercado()
    revisor(propostas)
    return dict(externo=ext, propostas=propostas, consolidado=consolidar(propostas, ext))


# ============================================================ modo LLM (não testado: exige ANTHROPIC_API_KEY)
MODELO = "claude-opus-5-5"
CONTEXTO = ("Cliente: Caxias Heavy Industries (ônibus), em crise. Prioridade: regularizar dividendos em 12 meses e reduzir o risco de bloqueio "
            "pela B3; caixa zero; prefeituras só pagam na entrega; chicote Yazaki não pode ser trocado; inversor só da China; "
            "troca de fornecedor exige aviso de 30 dias; vínculo CLT; double-deck e P&D só depois de a empresa estar no verde; "
            "carta branca para mudanças. Use SOMENTE números devolvidos pelas ferramentas e marque como hipótese o que não vier delas.")
ESPECIALISTAS = {
    "Financeiro": [F.margem_por_modelo, F.fluxo_base, F.pendentes, F.multa_pendentes, F.passivo_dividendos, F.plano_dividendos, F.folha],
    "Operações": [F.capacidade_linha, F.qualidade_linha, F.cenario_turnos, F.folha],
    "Suprimentos": [F.leadtime_criticos, F.sensibilidade_cambio, F.pendentes],
    "Coleta Externa": [F.cotacoes_bcb, F.encargos_atrasados_selic],
}


def _como_tool(fn):
    import anthropic

    def w(**k):
        return json.dumps(fn(**k), ensure_ascii=False, default=str)

    # schema montado à mão: o pydantic não enxerga anotações de wrapper no Python 3.14
    tipo = {int: "integer", float: "number", bool: "boolean", str: "string"}
    props, obrig = {}, []
    for n, p in inspect.signature(fn).parameters.items():
        t = p.annotation if p.annotation is not p.empty else (type(p.default) if p.default is not p.empty else float)
        props[n] = {"type": tipo.get(t, "number")}
        if p.default is p.empty:
            obrig.append(n)
    w.__name__ = fn.__name__
    return anthropic.beta_tool(w, name=fn.__name__, description=(fn.__doc__ or fn.__name__).strip(),
                               input_schema={"type": "object", "properties": props, "required": obrig})


MODELO_GEMINI = "gemini-flash-latest"


def _parecer_gemini(plano: dict) -> dict:
    """Mesmo desenho do modo Claude, com Gemini: function calling automático nas ferramentas de ferramentas.py,
    Google Search para o Mercado e uma crítica do Revisor. Os números do plano continuam vindo do código."""
    from google import genai
    from google.genai import types
    client = genai.Client(http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=5)))
    ger = lambda **kw: client.models.generate_content(model=MODELO_GEMINI, **kw).text or ""
    out = {}
    for nome, tools in ESPECIALISTAS.items():
        out[nome] = ger(contents="Analise sua área com as ferramentas e liste as 3 recomendações mais relevantes, cada uma com o número e a ferramenta de origem.",
                        config=types.GenerateContentConfig(system_instruction=f"Você é o agente {nome}. {CONTEXTO}", tools=list(tools)))
    out["Mercado"] = ger(contents="Pesquise fontes públicas sobre demanda por ônibus urbanos, escolares/micro e elétricos em prefeituras do RS "
                                  "e linhas de financiamento (ex.: BNDES) e liste oportunidades com a URL de cada fonte.",
                         config=types.GenerateContentConfig(system_instruction=f"Você é o agente de Mercado. {CONTEXTO}", tools=[types.Tool(google_search=types.GoogleSearch())]))
    plano_json = json.dumps([asdict(p) for p in plano["propostas"]], ensure_ascii=False, default=str)
    out["Revisor"] = ger(contents=f"Critique este plano: contradições, números sem fonte, restrições do cliente violadas.\n{plano_json}",
                         config=types.GenerateContentConfig(system_instruction=f"Você é o Revisor. {CONTEXTO}"))
    return out


MODELO_LOCAL = os.environ.get("MODELO_LOCAL", "qwen3:4b")


def _parecer_local(plano: dict) -> dict:
    """Mesmo desenho, com modelo local via Ollama (sem chave, sem internet): especialistas chamam as ferramentas,
    o Revisor critica o plano. Sem busca na web: o agente de Mercado fica de fora (não inventa fonte)."""
    import ollama

    def ger(system, user, tools=()):
        porNome = {f.__name__: f for f in tools}
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        for _ in range(8):
            m = ollama.chat(model=MODELO_LOCAL, messages=msgs, tools=list(tools) or None, think=False,
                            options={"num_ctx": 8192, "temperature": 0.2}).message
            msgs.append(m)
            if not m.tool_calls:
                return m.content or ""
            for tc in m.tool_calls:
                try:
                    res = json.dumps(porNome[tc.function.name](**tc.function.arguments), ensure_ascii=False, default=str)
                except Exception as e:  # modelo pequeno erra argumentos: devolve o erro para ele corrigir
                    res = f"erro: {e}"
                msgs.append({"role": "tool", "tool_name": tc.function.name, "content": res[:6000]})  # cabe no contexto de 8k
        return ""

    out = {}
    for nome, tools in ESPECIALISTAS.items():
        out[nome] = ger(f"Você é o agente {nome}. {CONTEXTO}",
                        "Analise sua área com as ferramentas e liste as 3 recomendações mais relevantes, cada uma com o número e a ferramenta de origem.", tools)
    resumo = json.dumps([{k: getattr(p, k) for k in ("id", "titulo", "impacto_mensal", "impacto_unico", "custo_unico", "status", "motivos", "hipoteses")}
                         for p in plano["propostas"]], ensure_ascii=False, default=str)
    out["Revisor"] = ger(f"Você é o Revisor. {CONTEXTO}", f"Critique este plano: contradições, números sem fonte, restrições do cliente violadas.\n{resumo}")
    return out


def parecer_llm(plano: dict, local: bool = False) -> dict:
    """Cada especialista (Claude) chama suas ferramentas e escreve um parecer; o Revisor (Claude) critica o plano;
    o Mercado pesquisa na web (servidor de busca da API). Devolve textos; os números do plano continuam vindo do código."""
    if local:
        return _parecer_local(plano)
    if os.environ.get("GEMINI_API_KEY"):
        return _parecer_gemini(plano)
    import anthropic
    client = anthropic.Anthropic()
    out = {}
    for nome, tools in ESPECIALISTAS.items():
        runner = client.beta.messages.tool_runner(
            model=MODELO, max_tokens=16000, tools=[_como_tool(t) for t in tools], system=f"Você é o agente {nome}. {CONTEXTO}",
            messages=[{"role": "user", "content": "Analise sua área com as ferramentas e liste as 3 recomendações mais relevantes, cada uma com o número e a ferramenta de origem."}])
        out[nome] = "".join(b.text for b in runner.until_done().content if b.type == "text")
    r = client.messages.create(
        model=MODELO, max_tokens=16000, tools=[{"type": "web_search_20260209", "name": "web_search"}],
        system=f"Você é o agente de Mercado. {CONTEXTO}",
        messages=[{"role": "user", "content": "Pesquise fontes públicas sobre demanda por ônibus urbanos, escolares/micro e elétricos em prefeituras do RS "
                                              "e linhas de financiamento (ex.: BNDES) e liste oportunidades com a URL de cada fonte."}])
    out["Mercado"] = "".join(b.text for b in r.content if b.type == "text")
    plano_json = json.dumps([asdict(p) for p in plano["propostas"]], ensure_ascii=False, default=str)
    r = client.messages.create(
        model=MODELO, max_tokens=16000, system=f"Você é o Revisor. {CONTEXTO}",
        messages=[{"role": "user", "content": f"Critique este plano: contradições, números sem fonte, restrições do cliente violadas.\n{plano_json}"}])
    out["Revisor"] = "".join(b.text for b in r.content if b.type == "text")
    return out
