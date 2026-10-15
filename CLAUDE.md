# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## State of the repo

No code, build, lint, or test tooling yet — only two input documents (all in Portuguese):

- `Trabalho final - enunciado.pdf` — the assignment brief (UFSM generative-AI course final project).
- `Estudo_de_Caso_Industria_Onibus_Em_Crise.xlsx` — the scenario data: bus manufacturer "Caxias Heavy Industries" in crisis.

Python 3 is available but `openpyxl` is not installed; the xlsx has no `sharedStrings.xml` (inline strings), so it can also be parsed straight from the zip XML.

## Assignment requirements (from the enunciado)

- Build an AI solution for the crisis scenario: **either** a multi-agent system (e.g. external-data collection, financial, operational/logistics, reviewer agents) **or** a single agent with human-in-the-loop manual approval. Goal: reverse the operating deficit, cut costs, maximize results.
- Agents may use external info (APIs, web scraping, benchmarks); the report must document the architecture diagram, each agent's role, tools, and validation rules.
- Team roles: Consultor (sole contact with the "client" = professor), Scrum Master, general team (data engineers / agent developers / analysts). Phase I is a client interview questionnaire run only by the Consultor.
- **Report must be written by humans — no LLM/text generation for the report.** AI is allowed only for the technical solution/agents. Do not draft report prose; help with code, data analysis, and technical artifacts only.
- Report follows MDT UFSM formatting; sections: introduction, theoretical background (GenAI/LLMs, single vs multi-agent, prompt engineering / tool use / RAG, optimization methods), practical application (interview results, agent architecture, data analysis, solutions and impact), conclusion.
- Deadline: **2026-11-04 23:55** (report and presentation locked after). Final presentation covers team roles, diagnosis, restructuring plan and quantitative results.

## Data (xlsx sheets)

Modelos de Ônibus (A1:I9) · Pedidos por Mês (A1:G47) · Linha de Montagem (A1:G12; cycle times, error std-dev, 180 days) · Catálogo de Peças (A1:G16; unit cost, lead time, suppliers) · Lista de Materiais (BOM) (A1:F23; components per model) · Folha e Absenteísmo (A1:I140; anonymized payroll and absences, 180 days) · Dividendos e Passivos (A1:G17; monthly dividend/debt obligations).

Sheets start with a title and subtitle row, then a blank row, then (presumably) headers — account for the offset when loading. The brief names the critical points to find: bottlenecks, scrap (refugo), costs, and default (inadimplência).
