# Calculator Documentation

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [CLI Mode](#cli-mode)
  - [Interactive Mode](#interactive-mode)
- [Architecture Overview](#architecture-overview)
- [Detailed Documentation](#detailed-documentation)
- [Contributing](#contributing)

---

## Project Overview

This is a modular Python calculator application that supports both command-line (one-shot expression) and interactive (menu-driven) usage modes. It is also the subject of a bachelor thesis on self-evolving software and serves as the runtime target for autonomous code-mutation experiments.

The calculator evaluates arithmetic expressions safely — user input is never passed to `eval()`. Expression parsing uses Python's `ast` module, and all arithmetic is routed through a typed engine with explicit validation.

Supported operations:

- Basic: addition, subtraction, multiplication, division
- Power/root: square, cube, square root, cube root, arbitrary power
- Logarithms: base-10 logarithm (`log10`), natural logarithm (`ln`)
- Combinatorics: factorial

---

## Installation

**Requirements:** Python 3.12 or later.

```bash
# Clone the repository
git clone <repo-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Install dependencies (none beyond the standard library at present)
pip install -r requirements.txt
```

---

## Quick Start

### CLI Mode

Pass any infix arithmetic expression as a command-line argument:

```bash
python -m src "3 + 4"          # prints: 7
python -m src "10 / 2 - 1"     # prints: 4.0
python -m src "2 ** 8"         # prints: 256.0
python -m src "7 * (3 + 2)"    # prints: 35
```

Errors (division by zero, invalid syntax, etc.) are printed to `stderr` and the exit code is `1`.

### Interactive Mode

Run without arguments to enter the menu-driven prompt:

```bash
python -m src
```

The shell displays the list of available operations. Type the operation name, then enter the operand(s) when prompted:

```
Calculator — available operations:
   1. add
   2. subtract
   ...
  12. natural_log
  Type 'quit' or 'exit' to leave.

Select operation: add
  Enter operand 1: 5
  Enter operand 2: 3
  Result: 8
```

Type `quit` or `exit` to terminate the session.

---

## Architecture Overview

The application is organised into four layers:

| Layer | Package | Responsibility |
|---|---|---|
| Presentation | `src/presentation/` | CLI parsing, interactive loop, I/O |
| Logic | `src/logic/` | State management, history recording |
| Operations | `src/operations/` | Operation registry, concrete operation classes |
| Support | `src/` (top-level) | History storage, logging, retry utilities |

Each layer imports only downward — presentation imports logic, logic imports operations and history, operations import only the engine. No layer imports from a higher layer.

---

## Detailed Documentation

| Document | Audience | Description |
|---|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Developers | Module breakdown, data flow, design patterns, extension points |
| [API_REFERENCE.md](API_REFERENCE.md) | Developers | Full class/function reference with signatures, parameters, and examples |
| [USER_GUIDE.md](USER_GUIDE.md) | End users | CLI and interactive mode usage, operators, troubleshooting |
| [EXTENDING.md](EXTENDING.md) | Contributors | How to add new operations and presentation modes |

---

## Contributing

This repository is primarily a research artefact. Direct contributions to `main` are not accepted; all changes must go through an experiment branch. See the top-level `CLAUDE.md` for the full contribution policy and git hygiene rules.
