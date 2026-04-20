# Developer Guide

This guide covers the project structure, how the layers interact, how to add new operations, and how tests are organized.

---

## Project Structure

```
.
├── main.py                        # CLI entry point
├── src/
│   ├── __init__.py
│   ├── __main__.py                # Interactive entry point (python -m src)
│   ├── core/                      # Pure calculation logic — no I/O
│   │   ├── __init__.py
│   │   ├── calculator.py          # Calculator class
│   │   ├── operations_manager.py  # OperationRegistry class
│   │   └── operations.py         # get_operation_registry() factory
│   ├── interface/                 # Stateless I/O helpers — no session state
│   │   ├── __init__.py
│   │   ├── input_parser.py        # parse_cli_args(), convert_operand()
│   │   ├── output_formatter.py    # format_result()
│   │   └── menu_renderer.py       # display_menu()
│   ├── interactive/               # Interactive session lifecycle
│   │   ├── __init__.py
│   │   ├── session.py             # run_interactive_session(), get_operation_choice(), get_operands()
│   │   └── input_handler.py       # Re-exports from session.py
│   ├── support/                   # Cross-cutting support utilities
│   │   ├── __init__.py
│   │   ├── history.py             # HistoryTracker class
│   │   └── error_logging.py       # Re-exports ErrorLogger
│   ├── calculator.py              # Backward-compat shim → src.core.calculator
│   ├── cli.py                     # parse_arguments(), execute_cli()
│   ├── error_logger.py            # ErrorLogger class (canonical definition)
│   ├── history.py                 # Backward-compat shim → src.support.history
│   └── input_handler.py           # Backward-compat shim → src.interactive.*
└── tests/                         # pytest test suite
```

---

## Modularization Layers

The codebase is divided into four functional layers plus backward-compatibility shims.

### Core Layer (`src/core/`)

Contains all mathematical computation logic. No imports from I/O, session, or display modules are permitted here.

- **`calculator.py`** — The `Calculator` class. Each operation is a pure method that takes numeric arguments and returns a numeric result. Raises `TypeError`, `ValueError`, or `ZeroDivisionError` on invalid input; never prints or logs.
- **`operations_manager.py`** — The `OperationRegistry` class. Holds two internal dicts: `_normal_operations` (currently active) and `_scientific_operations` (reserved for future expansion). Each entry maps an operation name to a `(method, arity)` tuple. `get_all_operations()` merges and returns both dicts.
- **`operations.py`** — The `get_operation_registry(calculator)` factory function. Instantiates `OperationRegistry`, calls `get_all_operations()`, and returns the resulting dict. This is the single entry point used by all callers to obtain the operation registry.

### Interface Layer (`src/interface/`)

Stateless helpers that translate between raw user input/output and the core layer. No session state, no operation dispatch.

- **`input_parser.py`** — `parse_cli_args(args)` splits a raw argument list into an operation name and operand strings. `convert_operand(value)` converts a numeric string to `int` or `float` (whole-number floats become `int`).
- **`output_formatter.py`** — `format_result(result)` converts a numeric result to its string representation.
- **`menu_renderer.py`** — `display_menu(registry)` prints the numbered operation menu to stdout, including the `h` and `q` options.

### Interactive Layer (`src/interactive/`)

Manages the full interactive session lifecycle including user prompting, validation loops, and error handling.

- **`session.py`** — The canonical home of `run_interactive_session()`, `get_operation_choice()`, and `get_operands()`. Also defines `MAX_VALIDATION_ATTEMPTS = 5` and `_HISTORY_TOKEN = "h"`. The module-level `_error_logger` instance is shared by all functions here.
- **`input_handler.py`** — A thin re-export module that surfaces `get_operation_choice`, `get_operands`, `MAX_VALIDATION_ATTEMPTS`, `_HISTORY_TOKEN`, and `_error_logger` under the `src.interactive.input_handler` namespace for callers that need only input collection without the full session.

### Support Layer (`src/support/`)

Cross-cutting utilities with no dependency on core math or interactive session logic.

- **`history.py`** — `HistoryTracker` records operation results in memory during a session, displays them on request, and writes them to `history.txt` on `save_to_file()`.
- **`error_logging.py`** — Re-exports `ErrorLogger` (and module-level internals) from the canonical definition at `src/error_logger.py`. The `ErrorLogger` class is stateless; all state lives in the module-level `_logger` singleton in `src/error_logger.py`.

### Backward-Compatibility Shims (`src/`)

The root-level `src/` shims allow existing callers to keep their original import paths while the canonical implementations live in their new sub-packages.

| Shim file             | Re-exports from                        |
|-----------------------|----------------------------------------|
| `src/calculator.py`   | `src.core.calculator.Calculator`       |
| `src/history.py`      | `src.support.history.HistoryTracker`   |
| `src/error_logger.py` | Canonical definition (not a shim)      |
| `src/input_handler.py`| `src.core.operations`, `src.interface.menu_renderer`, `src.interactive.*` |

---

## Architecture Diagram

```
                    ┌─────────────────┐       ┌───────────────────────────┐
                    │    main.py      │       │    src/__main__.py         │
                    │  (CLI entry)    │       │  (interactive entry)       │
                    └────────┬────────┘       └────────────┬──────────────┘
                             │                             │
                             ▼                             ▼
                    ┌─────────────────┐       ┌───────────────────────────┐
                    │   src/cli.py    │       │  src/interactive/session.py│
                    │ execute_cli()   │       │ run_interactive_session()  │
                    └────────┬────────┘       └───────┬────────────────────┘
                             │                         │
              ┌──────────────┼─────────────────────────┤
              │              │                         │
              ▼              ▼                         ▼
  ┌─────────────────┐ ┌─────────────┐      ┌──────────────────────────────┐
  │src/interface/   │ │  src/core/  │      │       src/support/            │
  │ input_parser.py │ │calculator.py│      │  history.py  error_logging.py │
  │output_formatter │ │operations.py│      └──────────────────────────────┘
  │menu_renderer.py │ │ops_manager  │
  └─────────────────┘ └─────────────┘
```

---

## Development Setup

Requirements: Python 3.12 or newer.

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Install test dependencies
pip install pytest

# Run the test suite
pytest tests/

# Run the application
python -m src                    # interactive mode
python main.py add 3 4           # CLI mode
```

---

## How to Add a New Operation

Follow these four steps to register a new operation end-to-end.

### Step 1 — Implement the method on `Calculator`

Open `src/core/calculator.py` and add a new method. Follow the existing style: use type hints, raise `TypeError` for wrong types, raise `ValueError` for domain violations, never print or log.

```python
def my_op(self, x: int | float) -> float:
    """One-line description.

    Args:
        x: Description and domain constraints.

    Returns:
        Description of return value.

    Raises:
        TypeError: If x is not int or float.
        ValueError: If x is outside the valid domain.
    """
    if not isinstance(x, (int, float)):
        raise TypeError(f"my_op() requires a numeric argument, got {type(x).__name__!r}")
    # ... computation ...
    return result
```

### Step 2 — Register the operation in `OperationRegistry`

Open `src/core/operations_manager.py` and add a `_register_op` call inside `_load_normal_operations`:

```python
self._register_op("my_op", self._calculator.my_op, 1)  # 1 = unary, 2 = binary
```

### Step 3 — Verify the operation is discoverable

No other code changes are required. `get_operation_registry()` already calls `OperationRegistry.get_all_operations()`, which includes the new entry. Both the interactive menu and the CLI dispatch will automatically pick it up.

### Step 4 — Write tests

Add unit tests in `tests/` covering: correct output, `TypeError` on wrong type, `ValueError` on domain violations, and edge cases. Test coverage for the new operation in CLI and interactive modes is also recommended.

---

## Testing Strategy

Tests live in `tests/` and are run with `pytest`.

- **Unit tests** — Test individual `Calculator` methods in isolation. Cover correct results, type errors, value errors, and boundary conditions.
- **Integration tests** — Test `execute_cli()` end-to-end with real argument lists. Verify stdout, stderr, and return codes.
- **Structure tests** — Verify module layout, shim re-exports, and that canonical paths are consistent with backward-compat shims.
- **Logic separation tests** — Assert that core modules (`src/core/`) contain no I/O imports and that interface modules contain no calculation logic.

The test suite intentionally prioritizes correctness of the calculation and dispatch pipeline over raw line coverage.

---

## Key Design Decisions

### Backward Compatibility

When the codebase was modularized from a flat layout to the current layered structure, the root-level `src/*.py` shim files were retained so that existing callers (including the test suite and external consumers of the old import paths) required no changes.

### `OperationRegistry`

The registry pattern centralizes all knowledge about which operations exist and how many operands they take. Adding a new operation requires a change in exactly one place (`_load_normal_operations`) rather than scattered `if/elif` chains throughout the codebase.

### Layer Isolation

The core layer has no imports from the interface, interactive, or support layers. This ensures the `Calculator` class and operation registry can be imported and tested without pulling in any I/O or session state. Violations of this constraint would be caught by the structure tests.

### Lazy Error Log Creation

`error.log` is only created when the first error is actually logged. Processes that run successfully never create the file. This is controlled by the `_handler_attached` flag and `_ensure_handler()` in `src/error_logger.py`.
