# Calculator Application

A Python REPL-based calculator that supports both interactive and non-interactive (CLI) operation. The application provides basic arithmetic and advanced mathematical functions, maintains a session history, and logs all operations to a file.

---

## Quick Start

### Interactive REPL

Start the interactive read-eval-print loop:

```bash
python -m src.main
```

The REPL prompts with `>`. Type an expression and press Enter:

```
Calculator REPL — type an expression (e.g. 'add 5 3') or 'exit' to quit.
> add 5 3
Result: 8
> square_root 16
Result: 4.0
> history
1. 5 add 3 = 8
2. 16 square_root = 4.0
> exit
Goodbye!
```

Special REPL commands:

| Command    | Effect                                      |
|------------|---------------------------------------------|
| `history`  | Print all operations executed this session  |
| `exit`     | Quit the REPL                               |
| `quit`     | Quit the REPL                               |
| Ctrl-C     | Interrupt and quit cleanly                  |

### CLI (Single Expression)

Evaluate one expression non-interactively:

```bash
python -m src.main "add 5 3"
python -m src.main "factorial 7"
python -m src.main "power 2 10"
```

The result is written to stdout. Errors are written to stderr. The process exits with code `0` on success and `1` on any error.

---

## Expression Format

All expressions — in both REPL and CLI mode — follow this format:

```
OPERATION OPERAND1 [OPERAND2]
```

- Operation names are **case-insensitive** (`ADD`, `add`, `Add` are all valid).
- Operands must be integers or decimal numbers.
- Unary operations take one operand; binary operations take two.

Examples:

```
add 10 4
subtract 100 37.5
multiply 6 7
divide 22 7
factorial 5
square 9
cube 3
square_root 25
cube_root -8
power 2 8
natural_log 2.718
log_base_10 1000
```

---

## Operation Reference

### Basic Operations

| Operation  | Operands | Description                        |
|------------|----------|------------------------------------|
| `add`      | 2        | Sum of two numbers                 |
| `subtract` | 2        | Difference of two numbers          |
| `multiply` | 2        | Product of two numbers             |
| `divide`   | 2        | Quotient; raises error if b is 0   |

### Advanced Operations

| Operation     | Operands | Description                                        |
|---------------|----------|----------------------------------------------------|
| `factorial`   | 1        | n! for a non-negative integer                      |
| `square`      | 1        | x squared (x * x)                                 |
| `cube`        | 1        | x cubed (x * x * x)                               |
| `square_root` | 1        | Square root; raises error if x is negative         |
| `cube_root`   | 1        | Real cube root; supports negative inputs           |
| `power`       | 2        | base raised to exponent                            |
| `natural_log` | 1        | Natural logarithm; raises error if x <= 0          |
| `log_base_10` | 1        | Base-10 logarithm; raises error if x <= 0          |

For full signatures, error conditions, and per-operation examples see [OPERATIONS_REFERENCE.md](OPERATIONS_REFERENCE.md).

---

## Architecture Overview

```
Calculator (facade)
    └── CalculatorEngine (computation + history)
            ├── BasicOperations   (add, subtract, multiply, divide)
            └── AdvancedOperations (factorial, square, cube, ...)

Input layer
    ├── ExpressionParser  (tokenises raw strings)
    ├── InputValidator    (checks operation name and operand count)
    └── CalculatorREPL    (interactive loop) / CLIHandler (single expression)

Cross-cutting
    └── Logger (get_logger factory — file + console handlers)
```

| Module                  | Role                                                          |
|-------------------------|---------------------------------------------------------------|
| `src/calculator.py`     | Backward-compatible facade; delegates all calls to the engine |
| `src/logic.py`          | `CalculatorEngine` — pure computation and history tracking    |
| `src/modes/basic.py`    | `BasicOperations` — four arithmetic methods                   |
| `src/modes/advanced.py` | `AdvancedOperations` — eight mathematical methods             |
| `src/modes/operations.py` | `BaseOperationSet` ABC, `OperationRegistry`, canonical name sets |
| `src/input_handler.py`  | `ExpressionParser`, `InputValidator`, `CalculatorREPL`        |
| `src/cli.py`            | `CLIHandler`, `main_cli` entry point                          |
| `src/logger.py`         | `get_logger` factory; one-time root-logger configuration      |

---

## Further Reading

- [ARCHITECTURE.md](ARCHITECTURE.md) — detailed module hierarchy, data flow, and extension points
- [OPERATIONS_REFERENCE.md](OPERATIONS_REFERENCE.md) — complete operation signatures and error conditions
- [DEVELOPMENT.md](DEVELOPMENT.md) — environment setup, adding operations, testing, and Git workflow
