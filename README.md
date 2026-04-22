# Calculator — self-evolving software

## Overview

This repository contains a command-line calculator application written in
Python 3.12.  The calculator is the primary subject of an autonomous
self-evolution experiment: a multi-agent system driven by a large language
model iteratively extends and improves the application's source code without
human intervention.

The calculator itself supports two modes of operation:

- **Interactive REPL** — launch with `python -m src` (no arguments) to enter
  a menu-driven session with history tracking and retry-limited input.
- **CLI mode** — pass an operation and operands as arguments
  (`python -m src add 3 5`) for single-expression execution from scripts or
  pipelines.

## Key features

- **12 built-in operations:** `add`, `subtract`, `multiply`, `divide`,
  `power`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `log`
  (base-10), and `ln` (natural logarithm).
- **Operation history** — every result in an interactive session is recorded
  and can be reviewed with the `history` command.
- **Extensibility** — new operations can be registered at runtime via
  `OperationRegistry.register_operation()` without modifying any existing
  source file.
- **Structured error logging** — all domain errors are written to
  `logs/error.log` in ISO-8601 timestamped format. Logging failures are
  silently suppressed and never crash the application.
- **No external dependencies** — the application relies only on the Python
  standard library; `pytest` is the sole development dependency.

## Documentation

| Document | Purpose |
|---|---|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Installation, prerequisites, and usage examples for both modes |
| [OPERATIONS.md](OPERATIONS.md) | Complete reference for every built-in operation and the registry extension API |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Module-by-module architecture overview and design principles |

## Quick project structure

```
src/          Application source code
tests/        Pytest test suite
artifacts/    PlantUML development diagrams
logs/         Runtime error log (auto-created)
Calc_prompty/ Prompt files for the auto-evolution system
progress.md   Per-run experiment log
```

---

# Kalkulačka — autoevoluční software

**Název bakalářské práce:**  
*Autoevoluce softwaru pomocí autonomních agentů řízených velkým jazykovým modelem*

Tento repozitář reprezentuje jednoduchou aplikaci vytvořenou v rámci bakalářské práce. Autoevoluce je zde aplikována na implementaci objektově orientované kalkulačky.

---

## Struktura repozitáře

Struktura kódu na hlavní větvi:

```
calculator/
├── src/                        # Zdrojový kód aplikace
│   ├── calculator.py           # Hlavní třída kalkulačky s metodami (add, subtract, divide, multiply)
│   ├── __main__.py             # Vstupní bod aplikace
│   └── __init__.py
├── tests/
│   └── test_calculator.py      # Testy pomocí pytest
├── artifacts/                  # Složka pro vývojové diagramy (PlantUML)
├── Calc_prompty/               # Prompty pro jednotlivé úkoly autoevolučního systému
│   └── Task_list_calc.txt      # Seznam všech úkolů
├── progress.md                 # Log jednotlivých běhů (větve, změny, testy, čas, cena)
├── CLAUDE.md                   # Definice pravidel pro agenty
├── .mcp.json                   # Konfigurace GitHub MCP serveru
├── requirements.txt
└── .gitignore
```

---

## Autoevoluční engine

Tento systém je implementován ve třech hlavních částech:

### 1. Hlavní konfigurace — `CLAUDE.md`

Soubor `CLAUDE.md` slouží jako základní instrukční dokument pro LLM. Definuje:

- pravidla bezpečných změn (atomické commity, zákaz spekulativních změn, sandboxing)
- hranice odpovědností agentů (např. kdo spravuje `src/`, kdo `tests/`)
- pevná omezení platná i při plně autonomním běhu
- požadavky na reprodukovatelnost experimentu (logování, ukládání patchů)
- omezení sebe-modifikace (soubor `CLAUDE.md` je neměnný; návrhy změn se ukládají do `suggestions/update_claude.md`)

Každý agent i workflow tento soubor používá jako primární zdroj instrukcí.

---

### 2. Agenti — `.claude/agents/`

Systém obsahuje pět specializovaných agentů, každý definovaný v samostatném Markdown souboru:

| Soubor | Role | Odpovědnost |
|---|---|---|
| `github-task-analyst.md` | Analýza GitHub issues | pouze text zadání |
| `system-architect.md` | Návrh architektury | pouze čtení |
| `python-code-implementer.md` | Implementace kódu | `src/`, `artifacts/` |
| `pytest-edge-tester.md` | Tvorba a spouštění testů | `tests/` |
| `uml-diagram-designer.md` | Tvorba UML diagramů | `artifacts/` |

Každý agent má vlastní paměťový adresář `.claude/agent-memory/`, kde si uchovává kontext mezi běhy.

---

### 3. Workflows — `.github/workflows/`

Devět GitHub Actions workflow souborů řídí běh agentů:

| Soubor | Trigger | Účel |
|---|---|---|
| `pr-tests.yml` | Pull request | Spouští pytest pro každý PR |
| `claude-implement-shared.yml` | Voláno jinými workflow | Hlavní multi-agent pipeline |
| `claude-implement-naive-team.yml` | Label `ai-implement:naive-team` | Spuštění pro naive variantu |
| `claude-implement-expert-team.yml` | Label `ai-implement:expert-team` | Spuštění pro expert variantu |
| `claude-implement-structured-team.yml` | Label `ai-implement:structured-team` | Spuštění pro structured variantu |
| `pr-request-changes-shared.yml` | Voláno jinými workflow | Opravy na základě review |
| `pr-request-changes-naive-team.yml` | Label `request-changes:naive-team` | Opravy naive varianty |
| `pr-request-changes-expert-team.yml` | Label `request-changes:expert-team` | Opravy expert varianty |
| `pr-request-changes-structured-team.yml` | Label `request-changes:structured-team` | Opravy structured varianty |

Pipeline běží maximálně 24 kroků a zapisuje cenu a dobu běhu do `progress.md`.

---

## Experimentální větve

Experiment probíhá ve třech generacích. Každá z nich má tři větve na základě promptů
| Prefix | Rozdíl v generaci | Dokončeno |
| --- | --- | --- |
| `exp1` | Základní verze| Ano |
| `exp2` | Přidání kroku do workflow pro vytváření diagramů | In progress |
| `exp3` | Změnění standartní pipeline a Claude.MD na Test Driven Development, přidání generace vlastních RAG dokumentů | In progress |


| Větev | Styl promptu | Trigger label |
|---|---|---|
| `exp2/naive-team` | Neřízené prompty | `ai-implement:naive-team` |
| `exp2/expert-team` | Řízené prompty | `ai-implement:expert-team` |
| `exp2/structured-team` | Strukturované prompty | `ai-implement:structured-team` |

Každá varianta dostává stejný úkol, ale jiný prompt.

Workflow:
- vytvoří `task/issue-<id>-<desc>` větev
- provede změny
- otevře PR zpět do experimentální větve (nikdy do `main`)

---

## Lokální spuštění

```Bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Spuštění aplikace
`python -m src`

# Spuštění testů
`pytest tests/`


---

## Spuštění autoevoluce

1. Vytvoř GitHub issue
2. Přidej label `ai-implement:<varianta>`
3. Workflow vytvoří PR
4. Pro opravy použij `request-changes:<varianta>`
5. Merge provádí pouze člověk

---

## Klíčová omezení

- Agenti nikdy nemění `CLAUDE.md`, `.github/workflows/` ani `.gitignore`
- Všechny změny se ukládají jako patch do `patches/`
- Každý běh zapisuje výsledky do `progress.md`
- GitHub MCP server zajišťuje komunikaci s repozitářem