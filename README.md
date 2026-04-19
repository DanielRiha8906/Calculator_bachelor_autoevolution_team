# Calculator — Python Self-Evolving Software Prototype

This repository contains a Python 3.12 calculator application developed as part of a bachelor thesis on self-evolving software. The calculator supports both an interactive terminal session and a non-interactive command-line interface. It is designed with a layered, modular architecture that cleanly separates calculation logic, user-interface concerns, session management, and support utilities, making each layer independently testable and safely evolvable.

The application records every successful operation to a per-session history and appends structured error entries to a persistent log file. Both modes share the same underlying `Calculator` class and operation registry, ensuring consistent numeric behavior regardless of how the application is invoked.

---

## Quick Start

### Interactive Mode

```bash
python -m src
```

The interactive mode displays a numbered menu of available operations. Enter an operation name or its menu number, provide the required operands when prompted, and the result is printed immediately. Enter `h` to view session history or `q` to quit. History is saved to `history.txt` on exit.

### CLI Mode

```bash
python main.py <operation> [operand ...]
```

Examples:

```bash
python main.py add 3 4
python main.py factorial 5
python main.py square_root 9
python main.py power 2 10
python main.py log 100
```

---

## Supported Operations

| Operation     | Arity  | Description                              | Example                          |
|---------------|--------|------------------------------------------|----------------------------------|
| `add`         | binary | Addition                                 | `add 3 4` → `7`                  |
| `subtract`    | binary | Subtraction                              | `subtract 10 3` → `7`            |
| `multiply`    | binary | Multiplication                           | `multiply 3 4` → `12`            |
| `divide`      | binary | Division                                 | `divide 10 2` → `5.0`            |
| `power`       | binary | Exponentiation (base ^ exponent)         | `power 2 10` → `1024`            |
| `factorial`   | unary  | Factorial of a non-negative integer      | `factorial 5` → `120`            |
| `square`      | unary  | Square of a number (x²)                  | `square 4` → `16`                |
| `cube`        | unary  | Cube of a number (x³)                    | `cube 3` → `27`                  |
| `square_root` | unary  | Square root (√x), x ≥ 0                  | `square_root 9` → `3.0`          |
| `cube_root`   | unary  | Cube root (∛x), any sign                 | `cube_root -8` → `-2.0`          |
| `log`         | unary  | Base-10 logarithm, x > 0                 | `log 100` → `2.0`                |
| `ln`          | unary  | Natural logarithm (ln), x > 0           | `ln 1` → `0.0`                   |

---

## Installation and Setup

**Requirements:** Python 3.12 or newer.

```bash
# Clone the repository
git clone <repository-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Install test dependencies
pip install pytest

# Run the test suite
pytest tests/
```

No additional runtime dependencies are required beyond the Python standard library.

---

## Documentation

| Guide | Description |
|---|---|
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | How to use both interactive and CLI modes, all operations with examples, and troubleshooting |
| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Project structure, how to add new operations, testing strategy |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Modularization philosophy, package boundaries, data flow, error and history strategies |
| [docs/API_REFERENCE.md](docs/API_REFERENCE.md) | Public function and class signatures for all modules |

---

## Session Behavior

- **History:** Every successful operation is recorded in memory during the session. When the session ends (interactive mode only), entries are written to `history.txt` in the current working directory, overwriting any previous file.
- **Error log:** Errors are appended to `error.log` in the current working directory. The file is created lazily — it is only created when the first error actually occurs. Log entries use the structured format `TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE`.
- **Retry limit:** Both operation selection and operand input allow a maximum of `MAX_VALIDATION_ATTEMPTS = 5` consecutive invalid entries before the session terminates automatically.

---

## Project Structure

```
.
├── main.py                   # CLI entry point (python main.py <op> [operands])
├── src/
│   ├── __main__.py           # Interactive entry point (python -m src)
│   ├── core/
│   │   ├── calculator.py     # Calculator class — pure math, no I/O
│   │   ├── operations_manager.py  # OperationRegistry — manages operation dispatch
│   │   └── operations.py     # get_operation_registry() factory
│   ├── interface/
│   │   ├── input_parser.py   # parse_cli_args(), convert_operand()
│   │   ├── output_formatter.py    # format_result()
│   │   └── menu_renderer.py  # display_menu()
│   ├── interactive/
│   │   ├── session.py        # run_interactive_session(), get_operation_choice(), get_operands()
│   │   └── input_handler.py  # Re-exports from session.py
│   ├── support/
│   │   ├── history.py        # HistoryTracker class
│   │   └── error_logging.py  # Re-exports ErrorLogger from src.error_logger
│   ├── calculator.py         # Backward-compat shim → src.core.calculator
│   ├── cli.py                # parse_arguments(), execute_cli()
│   ├── error_logger.py       # ErrorLogger class (canonical)
│   ├── history.py            # Backward-compat shim → src.support.history
│   └── input_handler.py      # Backward-compat shim → src.interactive.*
└── tests/                    # Test suite (pytest)
```
