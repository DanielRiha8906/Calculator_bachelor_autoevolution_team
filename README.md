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
| `exp2` | Přidání kroku do workflow pro vytváření diagramů | Ano |
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

---

## Overview

This repository contains a **calculator** application built as part of a bachelor's thesis on self-evolving software. The calculator supports both interactive (guided prompt) and batch (CLI argument) modes, covering 12 arithmetic and mathematical operations. The application is also used as the subject of autonomous code evolution experiments driven by LLM-based agents.

---

## Installation

### Getting Started

1. Clone the repository.
2. Create and activate a virtual environment using `.venv`:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

The calculator can be run in two modes: **interactive** mode and **batch** (CLI) mode.

### Interactive Mode

Run the application without arguments to enter the guided interactive prompt:

```bash
python -m src
```

The application will prompt you step-by-step: enter an operation, provide operand(s), and receive the result. After each calculation, the result is displayed and you are prompted to continue. Type `quit` or `exit` at the operation prompt to end the session.

### Batch / CLI Mode

Pass an operation keyword and operands as command-line arguments for single-shot batch execution:

```bash
python -m src add 5 3
python -m src subtract 10 4
python -m src multiply 6 7
python -m src divide 20 4
python -m src square 9
python -m src sqrt 16
python -m src factorial 5
python -m src power 2 8
python -m src log 100
python -m src ln 2.718
```

The result is printed to stdout and the process exits with code `0` on success or `1` on error.

To see all supported commands:

```bash
python -m src --help
```

---

## Supported Operations

The following 12 operations are available in both interactive and batch modes:

| Keyword     | Operation              | Arity  | Example                      |
|-------------|------------------------|--------|------------------------------|
| `add`       | Addition               | binary | `add 5 3` → 8                |
| `subtract`  | Subtraction            | binary | `subtract 10 4` → 6          |
| `multiply`  | Multiplication         | binary | `multiply 6 7` → 42          |
| `divide`    | Division               | binary | `divide 20 4` → 5.0          |
| `square`    | Square (x²)            | unary  | `square 9` → 81              |
| `cube`      | Cube (x³)              | unary  | `cube 3` → 27                |
| `sqrt`      | Square root            | unary  | `sqrt 16` → 4.0              |
| `cbrt`      | Cube root              | unary  | `cbrt 27` → 3.0              |
| `factorial` | Factorial (n!)         | unary  | `factorial 5` → 120          |
| `power`     | Exponentiation (x^y)  | binary | `power 2 8` → 256            |
| `log`       | Base-10 logarithm      | unary  | `log 100` → 2.0              |
| `ln`        | Natural logarithm      | unary  | `ln 2.718` → ~1.0            |

---

## Error Handling

The application handles common error conditions gracefully:

- **Division by zero**: attempting `divide x 0` prints an error message and, in batch mode, exits with code `1`. In interactive mode the user is re-prompted.
- **Invalid input**: non-numeric arguments cause an error message and a retry prompt in interactive mode, or a non-zero exit in batch mode.
- **Negative square root**: `sqrt` of a negative number raises a `ValueError` (not a valid real result).
- **Non-positive logarithm**: `log` and `ln` raise a `ValueError` for arguments ≤ 0.
- **Non-integer factorial**: `factorial` raises a `ValueError` for non-integer or negative inputs.

### Retry Behavior

In interactive mode, the application allows up to 3 invalid input attempts per prompt before raising `MaxRetriesExceeded` and terminating the session. Each invalid entry counts as one attempt; after the maximum number of attempts is exceeded, the session exits automatically.

---

## History Feature

Every completed calculation is recorded in the session history. At the end of an interactive session, the full history of operations is automatically persisted to `history.txt` in the working directory.

To display the history from a previous session, run:

```bash
python -m src history
```

Each history record contains the operation performed, the operands, and the result.

---

## Architecture

The calculator is organized into focused, single-responsibility modules under `src/`:

### Module Responsibilities

| Module                 | Responsibility                                                                                 |
|------------------------|-----------------------------------------------------------------------------------------------|
| `calculator_core.py`   | Core `Calculator` class: delegates to pure-function modules, records operation history.        |
| `basic_operations.py`  | Pure functions for the four basic arithmetic operations: add, subtract, multiply, divide.      |
| `advanced_operations.py` | Pure functions for advanced math: square, cube, sqrt (square root), cbrt (cube root), factorial, power, log, ln. |
| `interface.py`         | All CLI user-interface logic: prompt functions, display functions, `run_calculator` loop.      |
| `cli.py`               | Backward-compatible facade re-exporting everything from `interface.py`.                       |
| `batch_cli.py`         | Batch/non-interactive command-line mode: parses `sys.argv`, executes a single operation, exits with an appropriate code. |
| `calculator.py`        | Backward-compatible facade re-exporting `Calculator` from `calculator_core.py`.               |
| `error_logger.py`      | Structured file-based error logging (`log_error`, `log_calculation_error`, etc.) to `error.log`. |
| `__main__.py`          | Entry point: routes to batch mode when arguments are provided, otherwise starts the interactive session loop. |

### Data Flow

1. `__main__.py` reads `sys.argv` and dispatches to either `batch_cli.batch_main` or the interactive loop in `interface.run_calculator`.
2. Both paths instantiate `Calculator` (from `calculator_core`), which delegates each mathematical operation to `basic_operations` or `advanced_operations`.
3. Results are displayed via the display functions in `interface.py` and recorded in the `Calculator` history.
4. On session end, history is written to disk by `persist_history_to_file`.
