# Calculator

A command-line calculator written in Python 3.12 that supports arithmetic,
scientific, and root operations. It can be used interactively through a
menu-driven REPL or non-interactively from the command line.

This project also serves as the base application for a bachelor thesis on
self-evolving software — a system that can autonomously modify its own source
code.

---

## Features

- **Arithmetic:** addition, subtraction, multiplication, division
- **Power and logarithms:** power, base-10 logarithm, arbitrary-base logarithm,
  natural logarithm
- **Root operations:** square root, cube root
- **Polynomial shorthands:** square (x²), cube (x³), factorial (n!)
- **Two interaction modes:** interactive REPL with carry-over result and history,
  or single-shot CLI for scripting
- **Persistent session files:** `error.log` for errors, `history.txt` for
  completed operations
- **Alias support:** use `+`, `-`, `*`, `/`, `^`, `sqrt`, `cbrt`, `log`, `ln`
  as shorthand tokens in CLI mode

---

## Quick Start

**Interactive REPL:**

```
python -m src
```

**Single calculation from the command line:**

```
python -m src add 2 3
# 5.0

python -m src sqrt 144
# 12.0

python -m src log 1000 10
# 2.9999999999999996
```

---

## Installation and Setup

Python 3.12 is required. Full setup instructions are in
[docs/SETUP.md](docs/SETUP.md).

Quick summary:

```
python3.12 -m venv .venv
source .venv/bin/activate      # Linux / macOS
pip install -r requirements.txt
python -m src                  # launch REPL
```

---

## Usage Examples

### REPL walkthrough

```
$ python -m src
Welcome to the Calculator REPL. Type 'quit' to exit.

Available operations:
  1. Addition
  2. Subtraction
  ...
  12. Natural Logarithm
  history. Show operation history
  quit. Exit
Select operation: 1
Enter first value: 10
Enter second value: 3
Addition(10.0, 3.0) = 13.0

Select operation: 2
Enter first value [default: 13.0]:
Enter second value: 4
Subtraction(13.0, 4.0) = 9.0

Select operation: history

Operation history:
  add(10.0, 3.0) = 13.0
  subtract(13.0, 4.0) = 9.0

Select operation: quit
Calculator closed.
```

### CLI examples

```
python -m src multiply 6 7       # 42.0
python -m src power 2 10         # 1024.0
python -m src factorial 10       # 3628800
python -m src cube_root -27      # -3.0
python -m src ln 1               # 0.0
```

For the complete list of operations and all CLI flags see
[docs/USAGE.md](docs/USAGE.md).

---

## Project Structure

```
Calculator_bachelor_autoevolution_team/
├── src/                    # Application source code
│   ├── __main__.py         # Entry point (python -m src)
│   ├── calculator.py       # Calculator facade
│   ├── core/               # Arithmetic engine and operation registry
│   ├── interface/          # REPL and CLI interaction layers
│   └── support/            # Error logging, history, exceptions
├── tests/                  # Test suite
├── docs/                   # Detailed documentation
├── artifacts/              # PlantUML diagrams
├── suggestions/            # Proposed policy/workflow changes
├── patches/                # Generated diff artifacts
├── progress.md             # Autonomous run log
└── CLAUDE.md               # Project governance and safety rules
```

---

## Available Operations

| Operation | Canonical token | Alias | Arity |
|-----------|----------------|-------|-------|
| Addition | `add` | `+` | 2 |
| Subtraction | `subtract` | `-` | 2 |
| Multiplication | `multiply` | `*` | 2 |
| Division | `divide` | `/` | 2 |
| Power | `power` | `^` | 2 |
| Logarithm (base) | `logarithm` | `log` | 2 |
| Factorial | `factorial` | — | 1 |
| Square | `square` | — | 1 |
| Cube | `cube` | — | 1 |
| Square Root | `square_root` | `sqrt` | 1 |
| Cube Root | `cube_root` | `cbrt` | 1 |
| Natural Logarithm | `natural_logarithm` | `ln` | 1 |

Full descriptions, domain constraints, and error conditions are in
[docs/OPERATIONS_REFERENCE.md](docs/OPERATIONS_REFERENCE.md).

---

## Troubleshooting

Common issues and their solutions are covered in
[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

Quick reference for exit codes in CLI mode:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Usage error (wrong number of arguments) |
| 2 | Unknown operation name |
| 3 | Invalid operands |
| 4 | Calculation error (domain error, division by zero) |

---

## Documentation

| File | Contents |
|------|----------|
| [docs/SETUP.md](docs/SETUP.md) | Prerequisites, virtual environment, installation |
| [docs/USAGE.md](docs/USAGE.md) | REPL walkthrough, CLI reference, file outputs |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Module layout, component descriptions, data flow |
| [docs/OPERATIONS_REFERENCE.md](docs/OPERATIONS_REFERENCE.md) | All 12 operations with examples and error conditions |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Error messages, environment issues, behavioral questions |
