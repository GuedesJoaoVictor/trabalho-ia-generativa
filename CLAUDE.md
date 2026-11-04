# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## State of the repo

No code, build, lint, or test tooling yet — only two input documents (all in Portuguese):

- `Trabalho final - enunciado.pdf` — the assignment brief (UFSM generative-AI course final project).
- `Estudo_de_Caso_Industria_Onibus_Em_Crise.xlsx` — the scenario data: bus manufacturer "Caxias Heavy Industries" in crisis.

Python 3 is available but `openpyxl` is not installed; the xlsx has no `sharedStrings.xml` (inline strings), so it can also be parsed straight from the zip XML.

Run `python3 -I analise_planilha.py > resultados-analise.md` to regenerate the computed results. The xlsx formulas have empty cached values (`<v></v>`), so every derived number (totals, margins, JCP, absenteeism) must be recomputed in code; `analise_planilha.py` has a zip/XML loader (`dados(i)` for sheet i) to reuse.

## Code (multi-agent system)

Run with the venv (`.venv/bin/python`, has matplotlib + anthropic; not `-I`, which hides local modules):

- `.venv/bin/python executar.py` — runs the agents, writes `plano-consolidado.md`, `plano.json`, `figuras/*.png`. `--llm` adds Claude agents (needs `ANTHROPIC_API_KEY`; never executed yet).
- `.venv/bin/python test_sistema.py` — the single check (key numbers + Revisor rules).
- `dados.py` loads the xlsx → `ferramentas.py` (tools, all numbers, `PREMISSAS` = flagged assumptions) → `agentes.py` (specialist agents → `Proposta` objects → `revisor` recomputes from raw data and applies client rules → `consolidar`) → `executar.py`/`figuras.py`. `analise_planilha.py` is the older standalone analysis with its own loader.
- Client rules enforced by the Revisor: 12-month horizon, CLT severance, 30-day supplier notice, Yazaki harness and CATL inverter not replaceable, production cuts must beat lost profit, caixa zero.
- External data: Banco Central SGS API, cached with query date in `dados_externos.json`.
- `mapa-evidencias-relatorio.md` maps report sections to evidence.

## Assignment requirements (from the enunciado)

- Build an AI solution for the crisis scenario: **either** a multi-agent system (e.g. external-data collection, financial, operational/logistics, reviewer agents) **or** a single agent with human-in-the-loop manual approval. Goal: reverse the operating deficit, cut costs, maximize results.
- Agents may use external info (APIs, web scraping, benchmarks); the report must document the architecture diagram, each agent's role, tools, and validation rules.
- Team roles: Consultor (sole contact with the "client" = professor), Scrum Master, general team (data engineers / agent developers / analysts). Phase I is a client interview questionnaire run only by the Consultor.
- Deadline: **2026-11-04 23:55** (report and presentation locked after). Final presentation covers team roles, diagnosis, restructuring plan and quantitative results.

## Data (xlsx sheets)

Modelos de Ônibus (A1:I9) · Pedidos por Mês (A1:G47) · Linha de Montagem (A1:G12; cycle times, error std-dev, 180 days) · Catálogo de Peças (A1:G16; unit cost, lead time, suppliers) · Lista de Materiais (BOM) (A1:F23; components per model) · Folha e Absenteísmo (A1:I140; anonymized payroll and absences, 180 days) · Dividendos e Passivos (A1:G17; monthly dividend/debt obligations).

Sheets start with a title and subtitle row, then a blank row, then (presumably) headers — account for the offset when loading. The brief names the critical points to find: bottlenecks, scrap (refugo), costs, and default (inadimplência).

## LaTeX

- `apresentacao/apresentacao.tex` (Beamer, completa; nomes da equipe preenchidos) e `relatorio/relatorio.tex` (abnTeX2, texto completo; conferir números com `conferir_relatorio.py`). Compilar: `cd <pasta> && latexmk -pdf <arquivo>.tex`. Figuras vêm de `figuras/`; os números dos slides foram copiados de `plano-consolidado.md` (reconferir se rodar `executar.py` de novo).
- Apoio ao relatório (sem prosa): `gerar_tabelas.py` → `relatorio/tabelas/*.tex`; `conferir_relatorio.py <arquivo.tex>` confere números do texto contra o plano; `fontes-figuras.md`, `guia-conceitos.md` (explicação para o grupo, não texto de relatório) e `apresentacao/roteiro-e-perguntas.md`.
