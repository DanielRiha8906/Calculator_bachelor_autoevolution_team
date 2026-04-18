# Calculator — Bachelor Thesis Self-Evolving Software Prototype

This repository is the practical component of a bachelor thesis on **self-evolving software**: a system capable of autonomously modifying its own source code under the direction of an AI engine (Claude). The calculator application is the subject being evolved; the evolution engine, governance rules, and experiment infrastructure surround it.

> **Research context:** Code in this repository may be intentionally modified by the self-evolution engine during experiment runs. Changes produced autonomously are committed on isolated experiment branches and reviewed by a human before they can be merged. If you are reading this as a developer, treat any file under `src/` as potentially subject to autonomous modification and consult `progress.md` for a log of recent evolution cycles.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation & Setup](#installation--setup)
3. [Usage](#usage)
   - [CLI Mode](#cli-mode)
   - [Interactive Mode](#interactive-mode)
4. [API Overview](#api-overview)
5. [Architecture Overview](#architecture-overview)
6. [Developer Guide](#developer-guide)
7. [Research Context](#research-context)

---

## Project Overview

The calculator implements a standard set of arithmetic and advanced mathematical operations. Its design is intentionally modular so that the self-evolution engine can add, replace, or modify individual operation modules without touching unrelated code.

**Target audience:**

- Thesis evaluators reviewing the self-evolution experiment.
- Developers who extend or maintain the calculator between evolution cycles.
- Researchers reproducing or building on the experiment.

**Core capabilities:**

| Category    | Operations                                                    |
|-------------|---------------------------------------------------------------|
| Arithmetic  | add, subtract, multiply, divide                               |
| Advanced    | factorial, square, cube, square root, cube root, power, log, ln |

---

## Installation & Setup

**Requirements:** Python 3.12 or later.

```bash
# Clone the repository
git clone <repo-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

There are no third-party runtime dependencies. `requirements.txt` currently lists only `pytest` for the test suite.

---

## Usage

### CLI Mode

Pass operands and an operator as positional arguments:

```bash
# Basic arithmetic
python -m src 2 + 3
# Result: 5.0

python -m src 10 / 4
# Result: 2.5

python -m src 7 - 2.5
# Result: 4.5

python -m src 3 '*' 6
# Result: 18.0
```

> Note: The `*` operator may need quoting in some shells to prevent glob expansion.

**Show operation history** with the `--history` (`-H`) flag:

```bash
python -m src 8 / 2 --history
# Result: 4.0
# History:
#   8.0 / 2.0 = 4.0
```

**Exit codes:**

| Code | Meaning                                      |
|------|----------------------------------------------|
| 0    | Successful calculation                       |
| 1    | Input or arithmetic error (ValueError, ZeroDivisionError) |
| 2    | Argument-parsing error (argparse default)    |

**Error examples:**

```bash
python -m src 5 / 0
# Error: division by zero
# (exits with code 1)

python -m src abc + 1
# Error: Invalid operand 'abc': expected a numeric value, e.g. '3' or '2.5'.
# (exits with code 1)
```

### Interactive Mode

Run the module without arguments to enter interactive mode:

```bash
python -m src
```

The interactive mode prompts for each input separately, with up to three retries per field before cancelling:

```
Enter first operand: 12
Enter second operand: 4
Enter operator (+, -, *, /): /
Result: 3.0
```

If an invalid value is entered, the prompt repeats with a retry count:

```
Enter first operand: hello
Invalid input: Invalid operand 'hello': expected a numeric value, e.g. '3' or '2.5'. 2 attempt(s) remaining.
Enter first operand:
```

---

## API Overview

All public classes are importable directly from their respective modules under `src/`.

### `Calculator` (`src/calculator.py`)

A facade that composes `ArithmeticOperations` and `AdvancedOperations`. Instantiate once and call methods directly.

```python
from src.calculator import Calculator

calc = Calculator()

# Arithmetic
calc.add(2, 3)          # 5.0
calc.subtract(10, 4)    # 6.0
calc.multiply(3, 7)     # 21.0
calc.divide(9, 4)       # 2.25

# Advanced
calc.factorial(5)       # 120
calc.square(4)          # 16.0
calc.cube(3)            # 27.0
calc.square_root(16)    # 4.0
calc.cube_root(-8)      # -2.0
calc.power(2, 10)       # 1024.0
calc.log(100)           # 2.0   (base-10)
calc.ln(1)              # 0.0   (natural log)
```

**Error conditions:**

| Method          | Raises                | Condition                       |
|-----------------|-----------------------|---------------------------------|
| `divide`        | `ZeroDivisionError`   | denominator is zero             |
| `factorial`     | `ValueError`          | n is not an int, or n < 0       |
| `square_root`   | `ValueError`          | x < 0                           |
| `log`           | `ValueError`          | x <= 0                          |
| `ln`            | `ValueError`          | x <= 0                          |

### `CalculatorWithHistory` (`src/calculator_with_history.py`)

A stateful wrapper around `Calculator` that records every successful operation. Failed operations (those that raise an exception) are not recorded.

```python
from src.calculator_with_history import CalculatorWithHistory

calc = CalculatorWithHistory()
calc.add(2, 3)       # 5.0
calc.multiply(4, 5)  # 20.0
calc.divide(10, 2)   # 5.0

calc.get_history()
# ['2 + 3 = 5.0', '4 * 5 = 20.0', '10.0 / 2.0 = 5.0']
```

History entries use infix notation for binary arithmetic operations and functional notation for unary operations (e.g. `"factorial(5) = 120"`).

### Operation Modules (`src/operations/`)

| Module                         | Class                  | Responsibility                              |
|--------------------------------|------------------------|---------------------------------------------|
| `src/operations/base.py`       | `OperationModule`      | Abstract base; enforces structural contract |
| `src/operations/arithmetic.py` | `ArithmeticOperations` | add, subtract, multiply, divide             |
| `src/operations/advanced.py`   | `AdvancedOperations`   | factorial, square, cube, roots, power, log, ln |

These modules are not intended for direct use by application code — use `Calculator` or `CalculatorWithHistory` instead. They are kept separate to allow the self-evolution engine to target individual modules independently.

### Parser and Dispatcher (`src/parser.py`, `src/dispatcher.py`)

- `parse_operand(raw: str) -> float` — converts a user-supplied string to a float operand.
- `parse_input(operand_a, operand_b, operator) -> tuple[float, float, str]` — validates both operands and maps the operator symbol to a method name.
- `run_calculation(a, b, method_name) -> tuple[float, CalculatorWithHistory]` — instantiates `CalculatorWithHistory` and dispatches the named method.

### Logging (`src/logger.py`)

```python
from src.logger import get_logger

logger = get_logger(__name__)
```

All modules use `get_logger(__name__)`. Loggers are initialised with a `NullHandler`, so no output appears by default. To enable log output in your own code or scripts:

```python
import logging
logging.basicConfig(level=logging.ERROR)
```

---

## Architecture Overview

```
src/
├── __main__.py              Entry point: routes to CLI or interactive mode
├── cli.py                   Argument parsing and CLI output
├── calculator.py            Facade: owns ArithmeticOperations + AdvancedOperations
├── calculator_with_history.py  Wrapper: adds history recording around Calculator
├── dispatcher.py            Dispatch: instantiates CalculatorWithHistory, calls method
├── parser.py                Pure parsing: string-to-float, operator symbol mapping
├── retry_handler.py         Interactive input with configurable retry logic
├── input_handler.py         Compatibility shim re-exporting parser + dispatcher names
├── logger.py                Centralised logger factory (NullHandler by default)
└── operations/
    ├── base.py              OperationModule abstract base class
    ├── arithmetic.py        ArithmeticOperations: add, subtract, multiply, divide
    └── advanced.py          AdvancedOperations: factorial, roots, power, logarithms
```

**Key design decisions:**

- **Facade pattern** — `Calculator` delegates all calls to the appropriate operation module. Callers only see one interface regardless of which module handles the operation.
- **History wrapper pattern** — `CalculatorWithHistory` wraps `Calculator` via composition, not inheritance, keeping history concerns isolated.
- **Operation delegation** — `ArithmeticOperations` and `AdvancedOperations` both extend `OperationModule`, giving the evolution engine a stable structural contract to target independently.
- **No I/O in core logic** — `parser.py` and `dispatcher.py` contain no I/O. `cli.py` and `retry_handler.py` own all user interaction. This separation makes the core logic testable in isolation.
- **Compatibility shim** — `input_handler.py` re-exports names from `parser.py` and `dispatcher.py` so that existing callers continue to work after the modularisation refactor.

PlantUML class, activity, and sequence diagrams are maintained under `artifacts/` and updated alongside structural changes.

---

## Developer Guide

### Running Tests

```bash
python -m pytest
```

Tests live under `tests/` alongside the source. Do not delete tests to make a failing suite pass — fix the code instead.

### Module Layout

When adding a new operation category, follow this pattern:

1. Create `src/operations/<category>.py` with a class extending `OperationModule`.
2. Compose an instance of the new class into `Calculator.__init__`.
3. Add delegation methods to `Calculator` matching the new module's public interface.
4. Optionally add the same methods to `CalculatorWithHistory` if history recording is needed.
5. Update the relevant PlantUML diagram in `artifacts/`.

### Adding a Single Operation to an Existing Module

Add the method directly to the relevant operation class (`ArithmeticOperations` or `AdvancedOperations`), then add a delegation method to `Calculator`. Keep docstrings consistent with the Google style used throughout.

### Logging

Enable error-level logging for debugging:

```python
import logging
logging.basicConfig(level=logging.ERROR, format="%(name)s %(levelname)s %(message)s")
```

Each module creates its logger on demand via `get_logger(__name__)`, so logs are namespaced by module path (e.g. `src.operations.arithmetic`).

### Code Style

- Type hints on all public function signatures.
- Google-style docstrings with Args, Returns, and Raises sections.
- Explicit exception handling — no bare `except:` clauses.
- Small, single-purpose functions.

---

## Research Context

This project is the practical component of a bachelor thesis investigating **self-evolving software** — systems that autonomously modify their own source code.

The calculator serves as the **evolution target**: a small, well-tested codebase that the AI engine (Claude, operating via GitHub Actions) can safely modify, test, and commit to isolated experiment branches. Each evolution cycle is governed by `CLAUDE.md` and logged in `progress.md`.

**Important implications for developers:**

- Code under `src/` may differ from what you last read if an evolution cycle has run. Always pull the latest state of the experiment branch before making changes.
- The self-evolution engine operates only on the currently active experiment branch. It does not merge into `main` autonomously.
- All patches produced by the system are stored as diff artifacts under `patches/` or `output/` before being applied; they are not silently written.
- Evolution cycles are fully logged (inputs, outputs, diffs, timestamps, cost) in `progress.md` for thesis reproducibility.
- If you observe unexpected changes, consult `git log` and `progress.md` to determine whether they originate from an autonomous evolution cycle.

For governance rules, safety constraints, and experiment-branch policy, see `CLAUDE.md`.
