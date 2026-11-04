"""Carrega a planilha do cliente. As fórmulas vêm sem valor em cache (<v></v>), então só lemos
as células com dado; qualquer total/margem é calculado em ferramentas.py."""
import html
import re
import zipfile
from functools import cache
from pathlib import Path

XLSX = Path(__file__).with_name("Estudo_de_Caso_Industria_Onibus_Em_Crise.xlsx")

# aba -> {nome do campo: coluna}
COLUNAS = {
    1: ("modelos", dict(cod="A", nome="B", segmento="C", chassi="D", pax="F", custo="G", preco="H")),
    2: ("pedidos", dict(mes="B", modelo="C", qtd="D", preco="E", status="G")),
    3: ("linha", dict(etapa="A", nome="B", ciclo="D", desvio="E", refugo="F")),
    4: ("pecas", dict(cod="A", desc="B", forn="D", pais="E", preco="F", lead="G")),
    5: ("bom", dict(modelo="A", peca="B", qtd="D", custo="E")),
    6: ("folha", dict(id="A", cat="B", nivel="C", setor="D", salario="E", faltas="H")),
    7: ("dividendos", dict(mes="A", classe="B", acoes="C", dps="D", status="G")),
}


def _linhas(i):
    d = zipfile.ZipFile(XLSX).read(f"xl/worksheets/sheet{i}.xml").decode()
    for r in re.findall(r"<row [^>]*>(.*?)</row>", d, re.S):
        row = {}
        for col, corpo in re.findall(r'<c r="([A-Z]+)\d+"[^>]*>(.*?)</c>', r, re.S):
            if "<f>" in corpo:
                continue  # fórmula sem valor
            v = html.unescape(re.sub(r"<[^>]+>", "", corpo))
            try:
                v = float(v)
            except ValueError:
                pass
            row[col] = v
        yield row


@cache
def planilha():
    """{'modelos': [dict], 'pedidos': [dict], ...}. Pula título, subtítulo, linha vazia e cabeçalho;
    descarta linhas de total (só o rótulo, pois a fórmula foi ignorada)."""
    out = {}
    for i, (nome, cols) in COLUNAS.items():
        linhas = list(_linhas(i))[4:]
        out[nome] = [{k: r[c] for k, c in cols.items()} for r in linhas if len(r) > 2]
    return out
