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

# Calculator Application

A dual-mode calculator supporting CLI (command-line) and interactive REPL modes. It provides 13 operations — 6 arithmetic and 7 scientific — with session history tracking, error logging, and a consecutive-failure safety limit.

---

## Arithmetic Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| add | `python -m src add <a> <b>` | Adds two numbers |
| subtract | `python -m src subtract <a> <b>` | Subtracts b from a |
| multiply | `python -m src multiply <a> <b>` | Multiplies two numbers |
| divide | `python -m src divide <a> <b>` | Divides a by b (error on zero divisor) |
| factorial | `python -m src factorial <n>` | Computes n! for a non-negative integer n |
| modulo | `python -m src modulo <a> <b>` | Computes the remainder of a divided by b |

---

## Scientific Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| square | `python -m src square <n>` | Computes n² |
| cube | `python -m src cube <n>` | Computes n³ |
| square_root | `python -m src square_root <n>` | Computes √n (non-negative n only) |
| cube_root | `python -m src cube_root <n>` | Computes ∛n (real cube root, supports negatives) |
| power | `python -m src power <base> <exp>` | Computes base raised to integer exponent exp |
| log10 | `python -m src log10 <n>` | Computes log base 10 of n (positive n only) |
| ln | `python -m src ln <n>` | Computes natural logarithm of n (positive n only) |

---

## CLI Mode

Run a single calculation by passing the operation and its operands directly on the command line. The calculator prints the result and exits.

**Usage:**

```
python -m src <operation> [operand1] [operand2]
```

**Examples:**

```
python -m src add 5 3         # Output: 8
python -m src divide 10 2     # Output: 5.0
python -m src square 4        # Output: 16
python -m src factorial 5     # Output: 120
python -m src ln 1            # Output: 0.0
python -m src modulo 10 3     # Output: 1
python -m src power 2 8       # Output: 256
```

If the operation is unknown or operands are invalid, the calculator prints an error message to stderr and exits with a non-zero status code.

---

## Interactive Mode

Running `python -m src` with no arguments starts the interactive REPL. The calculator prompts you for an operation and its operands repeatedly until you choose to exit.

**Starting interactive mode:**

```
python -m src
```

**Example session:**

```
Enter operation (or 'quit' to exit, 'history' to view history): add
Enter operand 1: 5
Enter operand 2: 3
Result: 8

Enter operation (or 'quit' to exit, 'history' to view history): square
Enter operand 1: 4
Result: 16

Enter operation (or 'quit' to exit, 'history' to view history): quit
```

Type `quit` or `exit` (or `q`) at the operation prompt to leave interactive mode.

Type `history` at the operation prompt to display a numbered list of all operations performed during the current session.

---

## Error Handling

The calculator handles errors gracefully in both CLI and interactive modes.

| Error type | CLI behaviour | Interactive behaviour |
|------------|--------------|----------------------|
| Division by zero | Prints error to stderr, exits with code 1 | Prints error, prompts for next operation |
| Invalid operand (non-numeric) | Prints error to stderr, exits with code 1 | Prints error, prompts for next operation |
| Domain error (e.g. sqrt of negative) | Prints error to stderr, exits with code 1 | Prints error, prompts for next operation |
| Unknown operation | Prints error to stderr, exits with code 1 | Prints error, prompts for next operation |

### Consecutive failure limit

In interactive mode, the calculator tracks consecutive failures. After 3 consecutive invalid attempts (unknown operation, invalid operand, or domain/calculation error), the session exits automatically with the message:

```
Too many invalid attempts. Exiting.
```

The failure counter resets to 0 after any successful operation.

### Error logging

All errors that occur during a session are appended to `error_log.txt` in the current working directory. Each log entry contains a UTC ISO8601 timestamp, the error category, the operation attempted, the inputs supplied, and a description of the error. This log is intended for debugging and experiment reproducibility.

---

## Session History

During an interactive session, every successfully completed operation is recorded in the session history. To view the history, type `history` at the operation prompt. The history displays a numbered list of operations and their results in the order they were performed. History is per-session only and is not persisted across restarts (unless a history file path is configured).

---

## Project Structure

```
src/
  __main__.py              — entry point; delegates to src.calculator.main
  calculator/
    main.py                — CLI dispatcher and interactive REPL entry points
    core.py                — Calculator class with all operation methods
    operations/            — individual operation implementations
  history.py               — OperationHistory class for session history tracking
  error_logging.py         — ErrorLog class for timestamped error logging
  application.py           — Application class encapsulating user-interaction logic
tests/                     — pytest test suite
artifacts/                 — PlantUML development diagrams
```
