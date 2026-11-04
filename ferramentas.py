"""Ferramentas (tool use) dos agentes. Funções puras sobre a planilha + dados externos do Banco Central.

Todo número do plano nasce aqui, nunca do LLM. Cada função devolve dict/list serializável em JSON.
As premissas abaixo são os 'botões de calibração': o que não veio da planilha nem do cliente.
"""
import json
import math
import urllib.request
from datetime import date
from functools import cache
from pathlib import Path

from dados import planilha

# ---- premissas (hipóteses marcadas; ajustar quando o cliente informar o valor real) ----
PREMISSAS = dict(
    dias_mes=30,                 # operação contínua (cliente: 24 h por dia)
    horas_operador_mes=176,      # 8 h × 22 dias
    fator_dias_uteis=0.714,      # o mesmo da aba de folha
    encargos=0.45,               # aba de folha
    ocupacao_alvo=0.75,          # HIPÓTESE: operador produtivo 75% do tempo (setup, deslocamento)
    adicional_manutencao=0.20,   # HIPÓTESE: operadores também consertam máquinas de 2ª mão
    equipe_por_estacao=3,        # HIPÓTESE central (sensibilidade 2 a 4): pessoas simultâneas por estação
    rescisao_salarios=2.8,       # HIPÓTESE: aviso + multa FGTS 40% + 13º/férias proporcionais, em salários base
    multa_fixa=0.10,             # cliente: 10% do valor do ônibus
    multa_dia=0.001,             # cliente: 0,1% do valor ao dia (hipótese: sobre o valor do pedido atrasado)
    prazo_atrasados_meses=24,    # cliente: atrasados em 24 meses se o corrente estiver em dia
    horizonte_meses=12,          # cliente: prazo máximo
    mes_referencia="Out/26",
)
P_ = PREMISSAS

DIVIDENDO_EXIGIVEL = ("Acumulado em Atraso", "Exigência Judicial dos Minoritários")
TROCA = {
    "PEC-ELE-401": "Não (cliente: chicote Yazaki é fixo)",
    "PEC-ELE-402": "Sem produtor nacional (importado da China)",
}
CACHE_BCB = Path(__file__).with_name("dados_externos.json")


def _p():
    return planilha()


def _custo():
    return {m["cod"]: m["custo"] for m in _p()["modelos"]}


def _meses():
    return [d["mes"] for d in _p()["dividendos"]]  # Nov/25 .. Out/26, em ordem


# ============================================================ FINANCEIRO
def margem_por_modelo() -> list:
    """Margem de cada modelo: pelo preço de catálogo e pelo preço realmente praticado nos pedidos (12 meses)."""
    out = []
    for m in _p()["modelos"]:
        ped = [p for p in _p()["pedidos"] if p["modelo"] == m["cod"]]
        q = sum(p["qtd"] for p in ped)
        rec = sum(p["qtd"] * p["preco"] for p in ped)
        pm = rec / q if q else m["preco"]
        out.append(dict(
            cod=m["cod"], nome=m["nome"], custo=m["custo"], preco_catalogo=m["preco"], preco_praticado=pm,
            margem_catalogo=(m["preco"] - m["custo"]) / m["preco"], margem_praticada=(pm - m["custo"]) / pm,
            lucro_unid=pm - m["custo"], unid_12m=q, lucro_12m=rec - q * m["custo"]))
    return out


def fluxo_base() -> dict:
    """Receita e lucro bruto (preço praticado − custo direto) em 12 meses, por situação do pedido. Só pedidos
    'Entregue' viram caixa (prefeitura paga na entrega). O custo direto já inclui mão de obra e impostos (cliente)."""
    c = _custo()
    res = {}
    for st in ("Entregue", "Em Produção", "Pendente / Atrasado"):
        ps = [p for p in _p()["pedidos"] if p["status"] == st]
        res[st] = dict(unidades=sum(p["qtd"] for p in ps), receita=sum(p["qtd"] * p["preco"] for p in ps),
                       lucro=sum(p["qtd"] * (p["preco"] - c[p["modelo"]]) for p in ps))
    n = P_["horizonte_meses"]
    return dict(por_status=res,
                receita_total=sum(v["receita"] for v in res.values()),
                lucro_total=sum(v["lucro"] for v in res.values()),
                lucro_entregue_mensal=res["Entregue"]["lucro"] / n,
                unidades_mes=sum(v["unidades"] for v in res.values()) / n)


def pendentes() -> dict:
    """Pedidos 'Pendente / Atrasado': valor, lucro e multa contratual (10% fixa + 0,1%/dia)."""
    f = fluxo_base()["por_status"]["Pendente / Atrasado"]
    return dict(unidades=f["unidades"], receita=f["receita"], lucro=f["lucro"],
                multa_fixa=P_["multa_fixa"] * f["receita"], multa_por_dia=P_["multa_dia"] * f["receita"])


def multa_pendentes(dias: int) -> dict:
    """Multa total dos pedidos pendentes após `dias` de atraso.

    Args:
        dias: dias de atraso (a planilha não informa; é um cenário).
    """
    p = pendentes()
    return dict(dias=dias, multa_fixa=p["multa_fixa"], multa_diaria=p["multa_por_dia"] * dias,
                total=p["multa_fixa"] + p["multa_por_dia"] * dias)


def passivo_dividendos() -> dict:
    """Passivo de dividendos em 12 meses por situação (suspenso, em atraso, exigência judicial)."""
    por = {}
    for d in _p()["dividendos"]:
        por[d["status"]] = por.get(d["status"], 0) + d["acoes"] * d["dps"]
    total = sum(por.values())
    return dict(por_status=por, total=total, exigivel=sum(por.get(s, 0) for s in DIVIDENDO_EXIGIVEL),
                suspenso=por.get("Suspenso p/ Reestruturação", 0), corrente_mensal=total / P_["horizonte_meses"])


def plano_dividendos(incluir_suspensos: bool = False, encargos: float = 0.0) -> dict:
    """Saída mensal para regularizar dividendos: corrente em dia + atrasados quitados em 24 meses.

    Args:
        incluir_suspensos: se os dividendos ON suspensos também entram na quitação.
        encargos: juros/correção acumulados sobre os atrasados (R$), somados ao principal.
    """
    pas = passivo_dividendos()
    atraso = pas["exigivel"] + (pas["suspenso"] if incluir_suspensos else 0) + encargos
    parcela = atraso / P_["prazo_atrasados_meses"]
    return dict(atraso_a_quitar=atraso, parcela_mensal=parcela, corrente_mensal=pas["corrente_mensal"],
                saida_mensal=pas["corrente_mensal"] + parcela)


def folha() -> dict:
    """Folha mensal com encargos, por nível, e absenteísmo (faltas / (pessoas × 180 × 0,714))."""
    out = {}
    for f in _p()["folha"]:
        g = out.setdefault(f["nivel"], dict(pessoas=0, salario=0.0, faltas=0.0))
        g["pessoas"] += 1
        g["salario"] += f["salario"]
        g["faltas"] += f["faltas"]
    for g in out.values():
        g["custo_mensal"] = g["salario"] * (1 + P_["encargos"])
        g["custo_medio"] = g["custo_mensal"] / g["pessoas"]
        g["absenteismo"] = g["faltas"] / (g["pessoas"] * 180 * P_["fator_dias_uteis"])
    return dict(niveis=out, total_mensal=sum(g["custo_mensal"] for g in out.values()),
                pessoas=sum(g["pessoas"] for g in out.values()))


# ============================================================ OPERAÇÕES
def capacidade_linha(turnos: int = 3) -> dict:
    """Capacidade teórica (veículos/mês) por estação com ciclo efetivo = ciclo × (1 + refugo/retrabalho).
    A etapa 80 (acoplamento ao chassi) não opera à noite: no máximo 16 h/dia.

    Args:
        turnos: número de turnos de 8 h (1 a 3).
    """
    est = []
    for e in _p()["linha"]:
        horas = min(8 * turnos, 16) if int(e["etapa"]) == 80 else 8 * turnos
        ef = e["ciclo"] * (1 + e["refugo"])
        est.append(dict(etapa=int(e["etapa"]), nome=e["nome"], horas_dia=horas, ciclo_efetivo=ef,
                        capacidade=horas * P_["dias_mes"] / ef))
    lim = min(est, key=lambda x: x["capacidade"])
    meses = {}
    for p in _p()["pedidos"]:
        meses[p["mes"]] = meses.get(p["mes"], 0) + p["qtd"]
    media, pico = sum(meses.values()) / len(meses), max(meses.values())
    return dict(turnos=turnos, estacoes=est, limite=lim["capacidade"], estacao_limite=lim["nome"],
                demanda_media=media, demanda_pico=pico, uso_pico=pico / lim["capacidade"])


def qualidade_linha() -> dict:
    """Refugo/retrabalho como % do tempo de ciclo: horas perdidas por veículo, rendimento de 1ª passagem e
    custo mensal estimado dessas horas (equipe e custo/hora são hipóteses)."""
    linha = _p()["linha"]
    horas = sum(e["ciclo"] * e["refugo"] for e in linha)
    rty = math.prod(1 - e["refugo"] for e in linha)
    ciclo = sum(e["ciclo"] for e in linha)
    ops = [f for f in _p()["folha"] if f["nivel"] == "Operacional"]
    custo_hora = sum(f["salario"] for f in ops) / len(ops) * (1 + P_["encargos"]) / P_["horas_operador_mes"]
    veic_mes = fluxo_base()["unidades_mes"]
    return dict(ciclo_total_h=ciclo, horas_perdidas_por_veiculo=horas, pct_do_ciclo=horas / ciclo,
                rendimento_primeira_passagem=rty,
                criticas=[dict(etapa=int(e["etapa"]), nome=e["nome"], refugo=e["refugo"], horas=e["ciclo"] * e["refugo"])
                          for e in linha if e["refugo"] >= 0.05],
                custo_hora_operador=custo_hora,
                custo_mensal_retrabalho=horas * P_["equipe_por_estacao"] * veic_mes * custo_hora)


def cenario_turnos(turnos: int, equipe: int = 0) -> dict:
    """Quantos operadores o cenário exige e o que sobra, com custo de rescisão e retorno (payback).

    Args:
        turnos: 2 ou 3 turnos de 8 h.
        equipe: pessoas simultâneas por estação (0 usa a premissa central; sensibilidade 2 a 4).
    """
    equipe = equipe or P_["equipe_por_estacao"]
    cap = capacidade_linha(turnos)
    ciclo_ef = sum(e["ciclo_efetivo"] for e in cap["estacoes"])
    hh_mes = ciclo_ef * equipe * cap["demanda_pico"]  # horas-homem no mês de pico
    prod = P_["horas_operador_mes"] * (1 - folha()["niveis"]["Operacional"]["absenteismo"]) * P_["ocupacao_alvo"]
    nec = math.ceil(hh_mes / prod * (1 + P_["adicional_manutencao"]))
    atual = folha()["niveis"]["Operacional"]
    sobra = max(0, atual["pessoas"] - nec)
    sal_base = atual["salario"] / atual["pessoas"]
    economia = sobra * sal_base * (1 + P_["encargos"])
    resc = sobra * sal_base * P_["rescisao_salarios"]
    return dict(turnos=turnos, equipe=equipe, cobre_pico=cap["limite"] >= cap["demanda_pico"],
                capacidade=cap["limite"], demanda_pico=cap["demanda_pico"], uso_pico=cap["uso_pico"],
                operadores_atuais=atual["pessoas"], operadores_necessarios=nec, excedente=sobra,
                economia_mensal=economia, custo_rescisao=resc, payback_meses=resc / economia if economia else None)


# ============================================================ SUPRIMENTOS
def leadtime_criticos() -> dict:
    """Peças por lead time (tempo médio real de entrega), se podem ser trocadas, e prazo mínimo pedido→entrega
    por modelo (maior lead time da BOM + ciclo da linha). Capital parado no inversor/bateria do elétrico."""
    pecas = {p["cod"]: p for p in _p()["pecas"]}
    ranking = [dict(cod=p["cod"], desc=p["desc"], forn=p["forn"], pais=p["pais"], preco=p["preco"], lead=p["lead"],
                    troca=TROCA.get(p["cod"], "Sim, com aviso de 30 dias"))
               for p in sorted(pecas.values(), key=lambda x: -x["lead"])]
    ciclo_dias = sum(e["ciclo"] for e in _p()["linha"]) / 24
    modelos = []
    for m in _p()["modelos"]:
        ps = [b["peca"] for b in _p()["bom"] if b["modelo"] == m["cod"]]
        if ps:
            crit = max(ps, key=lambda c: pecas[c]["lead"])
            modelos.append(dict(cod=m["cod"], lead_max=pecas[crit]["lead"], peca=crit,
                                prazo_minimo=pecas[crit]["lead"] + ciclo_dias))
    inv = pecas["PEC-ELE-402"]
    ele_mes = sum(p["qtd"] for p in _p()["pedidos"] if p["modelo"] == "BUS-ELE-12M") / P_["horizonte_meses"]
    return dict(ranking=ranking, modelos=modelos, ciclo_dias=ciclo_dias, eletricos_por_mes=ele_mes,
                gasto_inversor_mensal=ele_mes * inv["preco"],
                capital_em_transito=ele_mes * inv["preco"] * inv["lead"] / P_["dias_mes"])


def sensibilidade_cambio(var_pct: float = 10.0) -> dict:
    """Quanto o custo mensal de peças importadas sobe se o câmbio subir `var_pct`% (BOM dos 3 modelos que têm BOM).

    Args:
        var_pct: variação do câmbio em %.
    """
    pais = {p["cod"]: p["pais"] for p in _p()["pecas"]}
    un = {}
    for p in _p()["pedidos"]:
        un[p["modelo"]] = un.get(p["modelo"], 0) + p["qtd"] / P_["horizonte_meses"]
    imp = tot = 0.0
    por_modelo = {}
    for b in _p()["bom"]:
        v = b["qtd"] * b["custo"] * un.get(b["modelo"], 0)
        tot += v
        if pais[b["peca"]] != "Brasil":
            imp += v
            por_modelo[b["modelo"]] = por_modelo.get(b["modelo"], 0) + v
    return dict(var_pct=var_pct, importado_mensal=imp, share_importado=imp / tot, custo_extra_mensal=imp * var_pct / 100)


# ============================================================ MERCADO / COLETA EXTERNA
def oportunidades_mercado() -> dict:
    """Economia unitária por modelo (lucro por ônibus, peso na carteira) para priorizar onde vender; e o que o
    cliente deixou para a fase 2 (double-deck e P&D só depois de a empresa estar no verde)."""
    mm = margem_por_modelo()
    rec = sum(m["unid_12m"] * m["preco_praticado"] for m in mm)
    lead = {m["cod"]: m["lead_max"] for m in leadtime_criticos()["modelos"]}
    return dict(
        modelos=sorted([dict(cod=m["cod"], nome=m["nome"], lucro_unid=m["lucro_unid"], unid_12m=m["unid_12m"],
                             pct_receita=m["unid_12m"] * m["preco_praticado"] / rec, lead_max=lead.get(m["cod"]))
                        for m in mm], key=lambda x: -x["lucro_unid"]),
        fase2=["Double-deck (cliente: só depois de a empresa estar no verde)",
               "Novos segmentos que aproveitem a linha: circular, urbano, rodoviário",
               "Venda de frotas sequenciais a prefeituras (hoje a venda é concentrada em Santa Maria)"])


def _bcb(serie: int, ini: str, fim: str) -> list:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados?formato=json&dataInicial={ini}&dataFinal={fim}"
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)


@cache
def dados_externos() -> dict:
    """Séries do Banco Central (SGS): Selic meta, Selic acumulada no mês, dólar e euro (venda), IPCA mensal.
    Guarda cópia em dados_externos.json com a data da consulta; sem rede, usa a cópia."""
    series = {"selic_meta_aa": 432, "selic_acum_mes": 4390, "usd_brl": 1, "eur_brl": 21619, "ipca_mes": 433}
    try:
        out = dict(consultado_em=date.today().isoformat(), fonte="https://api.bcb.gov.br/dados/serie/bcdata.sgs.<serie>/dados",
                   series={k: dict(serie=n, dados=_bcb(n, "01/10/2025", "31/12/2026")) for k, n in series.items()})
        CACHE_BCB.write_text(json.dumps(out, ensure_ascii=False))
        return out
    except OSError:
        return json.loads(CACHE_BCB.read_text())  # sem rede: usa a última consulta


def cotacoes_bcb() -> dict:
    """Últimos valores de Selic (meta a.a.), dólar, euro e IPCA do mês, com a data da consulta."""
    d = dados_externos()["series"]
    ult = lambda k: d[k]["dados"][-1]
    return dict(consultado_em=dados_externos()["consultado_em"], selic_meta_aa=ult("selic_meta_aa"), usd_brl=ult("usd_brl"),
                eur_brl=ult("eur_brl"), ipca_mes=ult("ipca_mes"))


def encargos_atrasados_selic() -> dict:
    """Correção pela Selic acumulada, de cada parcela em atraso até o fim de Out/26 (HIPÓTESE: o contrato pode
    prever outro índice; o cliente não informou juros nem multa)."""
    mes_n = {m: i for i, m in enumerate(_meses())}  # Nov/25 -> 0
    selic = {}  # (ano, mes) -> % no mês
    for r in dados_externos()["series"]["selic_acum_mes"]["dados"]:
        dd, mm, aa = r["data"].split("/")
        selic[(int(aa), int(mm))] = float(r["valor"])

    def ym(i):  # índice do mês -> (ano, mês); Nov/25 = (2025, 11)
        return (2025 + (10 + i) // 12, (10 + i) % 12 + 1)

    ref = mes_n[P_["mes_referencia"]]
    parcelas = []
    for d in _p()["dividendos"]:
        if d["status"] not in DIVIDENDO_EXIGIVEL:
            continue
        i = mes_n[d["mes"]]
        fator = math.prod(1 + selic[ym(j)] / 100 for j in range(i + 1, ref + 1))
        v = d["acoes"] * d["dps"]
        parcelas.append(dict(mes=d["mes"], principal=v, meses_atraso=ref - i, fator=fator, encargos=v * (fator - 1)))
    return dict(parcelas=parcelas, principal=sum(p["principal"] for p in parcelas),
                encargos=sum(p["encargos"] for p in parcelas), consultado_em=dados_externos()["consultado_em"])
