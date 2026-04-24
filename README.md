# Calculator — Self-Evolving Software

**Bachelor thesis project:**
*Software Auto-Evolution Using Autonomous Agents Driven by a Large Language Model*

This repository is a simple object-oriented calculator application used as the subject of an auto-evolution experiment. The system autonomously modifies the calculator's source code through multi-agent pipelines.

---

## Table of Contents

1. [User Guide](#user-guide)
   - [Running the Application](#running-the-application)
   - [Interactive Mode](#interactive-mode)
   - [CLI Usage](#cli-usage)
   - [Operations List](#operations-list)
   - [History Tracking](#history-tracking)
   - [Error Logging](#error-logging)
2. [Developer Guide](#developer-guide)
   - [Code Structure](#code-structure)
   - [Module Purposes](#module-purposes)
   - [Entry Point Flow](#entry-point-flow)
   - [Running Tests](#running-tests)
3. [Repository Overview](#repository-overview)
4. [Auto-Evolution Engine](#auto-evolution-engine)
5. [Local Setup](#local-setup)
6. [Running Auto-Evolution](#running-auto-evolution)

---

## User Guide

### Running the Application

Install dependencies and activate the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then start the calculator:

```bash
python -m src
```

Running without arguments launches **interactive mode**. Passing an operation name and operands uses **CLI mode**.

---

### Interactive Mode

Interactive mode presents a menu of available operations and prompts the user to enter operands. The session loops until the user chooses to exit.

Example interactive session:

```
Available operations:
  0: add (binary)
  1: subtract (binary)
  2: multiply (binary)
  3: divide (binary)
  4: power (binary)
  5: factorial (unary)
  6: square (unary)
  7: cube (unary)
  8: sqrt (unary)
  9: cbrt (unary)
  10: ln (unary)
  11: log10 (unary)
  h: View operation history
Select an operation (index): 0
Enter operand 1: 10
Enter operand 2: 5
Result: 15
Continue? (yes/no): yes
Select an operation (index): 8
Enter operand: 25
Result: 5.0
Continue? (yes/no): no
```

- Enter `h` at the operation prompt to view the current session history.
- Enter `no` or `n` at any prompt to exit and save history.
- After 5 consecutive invalid inputs, the session terminates automatically.

---

### CLI Usage

Pass the operation name and its operands as command-line arguments:

```bash
python -m src <operation> <operand1> [operand2]
```

**Binary operation examples** (two operands required):

```bash
python -m src add 10 5
# Output: 15

python -m src subtract 20 8
# Output: 12

python -m src multiply 4 7
# Output: 28

python -m src divide 100 4
# Output: 25.0

python -m src power 2 10
# Output: 1024
```

**Unary operation examples** (one operand required):

```bash
python -m src factorial 6
# Output: 720

python -m src sqrt 144
# Output: 12.0

python -m src ln 1
# Output: 0.0

python -m src log10 1000
# Output: 3.0
```

The CLI exits with code `0` on success and `1` on any error (unknown operation, wrong number of operands, invalid operand format, or a domain validation error).

---

### Operations List

The calculator supports 12 operations in two categories:

#### Binary operations (two operands)

| Operation  | Syntax                         | Description                          |
|------------|--------------------------------|--------------------------------------|
| `add`      | `python -m src add a b`        | Returns `a + b`                      |
| `subtract` | `python -m src subtract a b`   | Returns `a - b`                      |
| `multiply` | `python -m src multiply a b`   | Returns `a * b`                      |
| `divide`   | `python -m src divide a b`     | Returns `a / b` (b must not be zero) |
| `power`    | `python -m src power base exp` | Returns `base` raised to `exp`       |

#### Unary operations (one operand)

| Operation   | Syntax                       | Domain constraint              |
|-------------|------------------------------|--------------------------------|
| `factorial` | `python -m src factorial n`  | n must be a non-negative integer |
| `square`    | `python -m src square x`     | Any real number                |
| `cube`      | `python -m src cube x`       | Any real number                |
| `sqrt`      | `python -m src sqrt x`       | x must be non-negative         |
| `cbrt`      | `python -m src cbrt x`       | Any real number                |
| `ln`        | `python -m src ln x`         | x must be a positive number    |
| `log10`     | `python -m src log10 x`      | x must be a positive number    |

**Domain validation** — operations enforce the following constraints and raise a `ValueError` when violated:

- `sqrt`: x must be non-negative (x >= 0). Negative inputs are rejected.
- `factorial`: n must be a non-negative integer. Floats, booleans, and negative values are rejected.
- `ln`: x must be positive (x > 0). Zero and negative inputs are rejected.
- `log10`: x must be positive (x > 0). Zero and negative inputs are rejected.
- `divide`: divisor must not be zero. A `ZeroDivisionError` is raised otherwise.

---

### History Tracking

Every successful operation is recorded in memory during a session. When the session ends (via `no` in interactive mode, or after each CLI invocation), the history is written to `history.txt` in the current working directory.

The file is overwritten on each write. Each line follows the format:

```
operation_name(arg1, arg2, ...) = result
```

Example `history.txt`:

```
add(10, 5) = 15
sqrt(25) = 5.0
factorial(6) = 720
```

You can also view the history mid-session in interactive mode by entering `h` at the operation prompt.

---

### Error Logging

All errors encountered during a session are appended to `error.log` in the current working directory. The file is never overwritten — entries accumulate across runs.

Each log entry includes:

- Timestamp in `YYYY-MM-DD HH:MM:SS` format
- Error type label (e.g. `[Invalid Operation]`, `[Runtime Calculation Error]`)
- Context fields (operation name, operand value, message)

Example `error.log` entries:

```
[2026-04-24 12:00:01] [Invalid Operation] operation=None, message=Invalid operation. Please try again.
[2026-04-24 12:00:05] [Runtime Calculation Error] operation=sqrt, operands=(-4,), message=square root of negative numbers is not supported
```

Error logging failures (e.g. permission denied) are printed to `stderr` and never crash the application.

---

## Developer Guide

### Code Structure

The source code is organized into a modular layer architecture under `src/`:

```
src/
├── __main__.py                  # Entry point — dispatches to CLI or interactive mode
├── __init__.py
├── calculator.py                # Pure calculation core (no UI dependencies)
├── operation_registry.py        # Operation discovery and dynamic dispatch
├── core/                        # Domain-level abstractions
│   ├── __init__.py
│   └── operations.py            # Operation metadata definitions
├── ui/                          # Presentation layer
│   ├── __init__.py
│   ├── interactive.py           # Interactive terminal session
│   └── cli.py                   # Command-line interface handler
├── infrastructure/              # Cross-cutting concerns
│   ├── __init__.py
│   ├── history.py               # Session history tracking and file persistence
│   └── error_logger.py          # Structured error logging to error.log
└── session/                     # Session state management
    ├── __init__.py
    └── manager.py
```

The three main layers are:

- `src/ui/` — presentation layer (interactive.py, cli.py). Depends on core and infrastructure. No business logic.
- `src/infrastructure/` — cross-cutting concerns (history.py, error_logger.py). No UI dependencies.
- `src/core/` — domain-level abstractions (operations.py). No external dependencies.

---

### Module Purposes

| Module                  | Layer          | Responsibility                                                            |
|-------------------------|----------------|---------------------------------------------------------------------------|
| `calculator.py`         | Core           | Pure calculation methods: add, subtract, multiply, divide, power, factorial, square, cube, sqrt, cbrt, ln, log10. Raises `ValueError` and `ZeroDivisionError` only. |
| `operation_registry.py` | Core           | Discovers operations from the Calculator via reflection, resolves arity, and dispatches calls by name. Decouples UI from Calculator method details. |
| `interactive.py`        | UI             | Interactive terminal session loop: displays operation menu, collects user input, invokes operations, tracks history, logs errors, handles retries. |
| `cli.py`                | UI             | Command-line interface: parses `sys.argv`, validates operation name and operand count, invokes operation, prints result or error, persists history. |
| `history.py`            | Infrastructure | Records successful operations in memory during a session and persists them to `history.txt` on exit. |
| `error_logger.py`       | Infrastructure | Appends structured error entries with timestamps to `error.log`. Covers invalid operations, invalid operands, wrong argument counts, and runtime errors. |

---

### Entry Point Flow

`__main__.py` is the single entry point for the application. It dispatches based on command-line arguments:

```
python -m src           → run_interactive_session()   (no arguments)
python -m src add 1 2   → run_cli()                   (arguments present)
```

The `__main__.py` module imports `run_cli` from `src/ui/cli.py` and `run_interactive_session` from `src/ui/interactive.py`. It does not contain any calculation or validation logic itself.

---

### Running Tests

The test suite uses `pytest`. To run all tests:

```bash
pytest tests/
```

To run a specific test file:

```bash
pytest tests/test_calculator.py
pytest tests/test_documentation.py
```

To run with verbose output:

```bash
pytest -v tests/
```

All tests must pass before any commit. The TDD pipeline requires failing tests to be written before implementation code.

---

## Repository Overview

```
calculator/
├── src/                        # Application source code (see Developer Guide)
├── tests/                      # pytest test suite
├── artifacts/                  # PlantUML development diagrams
├── rag/                        # Self-maintained RAG knowledge base
├── Calc_prompty/               # Task prompts for the auto-evolution system
│   └── Task_list_calc.txt
├── progress.md                 # Per-run log (branch, changes, tests, time, cost)
├── CLAUDE.md                   # Agent instruction rules
├── .mcp.json                   # GitHub MCP server configuration
├── requirements.txt
└── .gitignore
```

---

## Auto-Evolution Engine

The self-evolving system is implemented in three main parts:

### 1. Main Configuration — `CLAUDE.md`

`CLAUDE.md` is the primary instruction document for the LLM agents. It defines:

- Safe-change rules (atomic commits, no speculative changes, sandboxing)
- Agent responsibility boundaries (who owns `src/`, who owns `tests/`)
- Hard limits that apply even in autonomous mode
- Experiment reproducibility requirements (logging, patch storage)
- Self-modification restrictions (CLAUDE.md is immutable; proposals go to `suggestions/update_claude.md`)

### 2. Agents — `.claude/agents/`

Five specialized agents, each defined in a Markdown file:

| File                        | Role                  | Responsibility              |
|-----------------------------|-----------------------|-----------------------------|
| `github-task-analyst.md`    | Issue analysis        | Issue text only             |
| `system-architect.md`       | Architecture design   | Read-only analysis          |
| `python-code-implementer.md`| Code implementation   | `src/`, `artifacts/`        |
| `pytest-edge-tester.md`     | Test creation and run | `tests/`                    |
| `uml-diagram-designer.md`   | UML diagrams          | `artifacts/`                |

### 3. Workflows — `.github/workflows/`

GitHub Actions workflows control the agent pipeline:

| File                                   | Trigger                              | Purpose                          |
|----------------------------------------|--------------------------------------|----------------------------------|
| `pr-tests.yml`                         | Pull request                         | Run pytest on every PR           |
| `claude-implement-shared.yml`          | Called by other workflows            | Main multi-agent pipeline        |
| `claude-implement-expert-team.yml`     | Label `ai-implement:expert-team`     | Expert variant run               |
| `claude-implement-naive-team.yml`      | Label `ai-implement:naive-team`      | Naive variant run                |
| `claude-implement-structured-team.yml` | Label `ai-implement:structured-team` | Structured variant run           |

The pipeline runs up to 24 steps and logs cost and duration to `progress.md`.

---

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python -m src
```

Run the tests:

```bash
pytest tests/
```

---

## Running Auto-Evolution

1. Create a GitHub issue describing the desired change
2. Add label `ai-implement:<variant>` (naive-team, expert-team, or structured-team)
3. The workflow creates a `task/issue-<id>-<desc>` branch, runs the pipeline, and opens a PR
4. For corrections, use label `request-changes:<variant>`
5. Only a human merges the PR — agents never self-merge

---

## Key Constraints

- Agents never modify `CLAUDE.md`, `.github/workflows/`, or `.gitignore`
- All changes are stored as patches under `patches/`
- Every run logs results to `progress.md`
- The GitHub MCP server handles repository communication
