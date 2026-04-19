# Architecture

This document describes the structural design of the calculator application: how it is partitioned, how data flows through each execution mode, and the rationale behind the major design choices.

---

## Modularization Philosophy

The application is built on four guiding principles:

1. **Separation of concerns** — Mathematical computation, user input/output, session lifecycle, and support utilities are each confined to their own layer. A change to how results are displayed does not risk touching the calculation logic, and vice versa.
2. **Layered architecture** — Layers form a dependency hierarchy: support and core layers have no knowledge of the layers above them. Higher layers (interactive, interface) import from lower layers (core, support) but not the reverse.
3. **Extensibility** — New operations are added by registering them in a single place (`OperationRegistry._load_normal_operations`). The menu, CLI dispatch, and interactive loop automatically discover the new entry without further modification.
4. **Testability** — Because the core layer has no I/O side effects, `Calculator` methods and `OperationRegistry` can be instantiated and exercised in unit tests without patching stdin, stdout, or the filesystem.

---

## Package Boundaries

### `src.core`

Owns all mathematical computation. Contains the `Calculator` class and the `OperationRegistry`. No module in `src.core` may import from `src.interface`, `src.interactive`, or `src.support`.

```
src/core/
  calculator.py         # Calculator — pure numeric methods
  operations_manager.py # OperationRegistry — operation metadata and dispatch table
  operations.py         # get_operation_registry() — factory used by all callers
```

### `src.interface`

Owns stateless translation between raw strings and computed values. Contains helpers for parsing CLI arguments, converting operand strings to numbers, formatting results, and rendering the menu. No module in `src.interface` may import from `src.interactive` or hold session state.

```
src/interface/
  input_parser.py       # parse_cli_args(), convert_operand()
  output_formatter.py   # format_result()
  menu_renderer.py      # display_menu()
```

### `src.interactive`

Owns the interactive session lifecycle. Handles prompting the user, validating input within the retry limit, dispatching operations, displaying results, and coordinating with the history tracker. Imports from `src.core`, `src.interface`, and `src.support`.

```
src/interactive/
  session.py            # run_interactive_session(), get_operation_choice(), get_operands()
  input_handler.py      # Re-exports from session.py for input-only consumers
```

### `src.support`

Owns cross-cutting utilities used by both the CLI path and the interactive path. No imports from `src.core`, `src.interface`, or `src.interactive`.

```
src/support/
  history.py            # HistoryTracker
  error_logging.py      # Re-exports ErrorLogger from src.error_logger
```

---

## Data Flow — Interactive Mode

Invoked with `python -m src`.

```
src/__main__.py
  └── Instantiates Calculator() and HistoryTracker()
  └── Calls run_interactive_session(calculator, history_tracker)

run_interactive_session()  [src/interactive/session.py]
  ├── Calls get_operation_registry(calculator)     → builds registry dict
  ├── Calls display_menu(registry)                 → prints numbered list to stdout
  │
  ├── Loop:
  │   ├── get_operation_choice(registry)
  │   │     ├── Reads raw input from stdin
  │   │     ├── Matches against quit tokens {"q", "quit", "exit"} → returns None
  │   │     ├── Matches "h" → returns ("h", None, None)
  │   │     ├── Matches numeric index → looks up name in registry keys
  │   │     ├── Matches operation name string directly
  │   │     └── On repeated invalid input (≥ MAX_VALIDATION_ATTEMPTS):
  │   │           logs UNSUPPORTED_OPERATION to error.log
  │   │           returns (None, None, None)
  │   │
  │   ├── On None → print "Goodbye." → break
  │   ├── On ("h", None, None) → history_tracker.display() → continue
  │   ├── On (None, None, None) → break
  │   │
  │   ├── get_operands(arity)
  │   │     ├── Prompts for each operand slot (1..arity)
  │   │     ├── Parses each as float(); on failure: logs INVALID_OPERAND, reprompts
  │   │     └── On repeated failure (≥ MAX_VALIDATION_ATTEMPTS) → returns None
  │   │
  │   ├── On operands is None → break
  │   │
  │   ├── If operation is factorial: converts whole-valued floats to int
  │   │
  │   ├── Calls method(*operands)
  │   │     ├── On success: prints result, records in history_tracker
  │   │     └── On ZeroDivisionError / TypeError / ValueError:
  │   │           logs error to error.log, prints error message, continues loop
  │   │
  │   └── display_menu(registry)   ← top of next iteration
  │
  └── history_tracker.save_to_file()   → writes history.txt
```

---

## Data Flow — CLI Mode

Invoked with `python main.py <operation> [operand ...]`.

```
main.py :: main()
  ├── Reads sys.argv[1:]
  ├── If empty → prints usage to stderr, sys.exit(1)
  ├── Instantiates Calculator()
  ├── Calls get_operation_registry(calculator)     → builds registry dict
  ├── Splits args into operation_name, operand_strs
  └── Calls execute_cli(operation_name, operand_strs, registry, calculator)
        → sys.exit(return_code)

execute_cli()  [src/cli.py]
  ├── Looks up operation_name in registry
  │     └── Not found → logs UNSUPPORTED_OPERATION, prints to stderr, returns 1
  │
  ├── Checks len(operand_strs) == arity
  │     └── Mismatch → logs ARGUMENT_COUNT_MISMATCH, prints to stderr, returns 1
  │
  ├── Converts each operand string via convert_operand()
  │     └── ValueError → logs INVALID_OPERAND, prints to stderr, returns 1
  │
  ├── Calls method(*operands)
  │     ├── On ZeroDivisionError → logs DIVISION_BY_ZERO, prints to stderr, returns 1
  │     ├── On TypeError / ValueError → logs INVALID_OPERAND, prints to stderr, returns 1
  │     └── On success → prints result to stdout, returns 0
  │
  └── (no history is written in CLI mode)
```

---

## Error Logging Strategy

### Class: `ErrorLogger` (`src/error_logger.py`)

`ErrorLogger` is a thin, stateless wrapper around a module-level Python `logging.Logger` named `"calculator.errors"`. All state (the logger, the `FileHandler`, and the `_handler_attached` flag) lives at module level so that multiple `ErrorLogger` instances all write to the same log file through the shared logger.

### Structured Log Format

Each error entry is a single line:

```
TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE
```

Example:

```
2024-11-15T14:32:05 | DIVISION_BY_ZERO | divide | 10, 0 | float division by zero
```

Fields default to `"N/A"` when not supplied in the context dict.

### Error Types

| Type                      | Logged when                                                        |
|---------------------------|--------------------------------------------------------------------|
| `UNSUPPORTED_OPERATION`   | Operation name not found in the registry                           |
| `INVALID_OPERAND`         | Operand cannot be parsed as a number, or violates Calculator type rules |
| `ARGUMENT_COUNT_MISMATCH` | Wrong number of operands in CLI mode                               |
| `DIVISION_BY_ZERO`        | `ZeroDivisionError` raised during dispatch                         |
| `INVALID_DOMAIN`          | Value outside the mathematical domain (e.g. negative square root)  |

### Lazy File Creation

The `FileHandler` for `error.log` is attached once, on the first call to `log_error()`, via the `_ensure_handler()` helper. This means `error.log` is never created for processes that complete without any errors. Any `OSError` raised while opening the file is silently swallowed so that a logging failure never crashes the application.

---

## History Tracking Strategy

### Class: `HistoryTracker` (`src/support/history.py`)

`HistoryTracker` is scoped to a single interactive session. It holds a plain Python list of strings in memory.

- `record(operation_name, operands, result)` — Appends `"operation_name(arg1, arg2, ...) = result"` to the in-memory list.
- `display()` — Prints all entries to stdout. Prints `"No history for this session."` if the list is empty.
- `save_to_file(filepath="history.txt")` — Writes the full list to a file, one entry per line, overwriting any previous file. `OSError` is caught and a warning is printed to stderr, allowing the session to exit cleanly.
- `get_history()` — Returns a copy of the list (used by tests).
- `clear()` — Empties the in-memory list.

History is **not** written during the CLI mode (`python main.py ...`). It is only written at the end of an interactive session.

---

## Backward Compatibility Layer

When the codebase was restructured from a flat `src/` layout to the current sub-package layout, root-level shim modules were introduced so that existing import paths continue to work without changes to callers:

| Import path                          | Resolves to canonical location                              |
|--------------------------------------|-------------------------------------------------------------|
| `from src.calculator import Calculator` | `src.core.calculator.Calculator`                          |
| `from src.history import HistoryTracker` | `src.support.history.HistoryTracker`                   |
| `from src.input_handler import ...`  | `src.core.operations`, `src.interface.menu_renderer`, `src.interactive.*` |
| `from src.support.error_logging import ErrorLogger` | `src.error_logger.ErrorLogger`             |

The shims contain no logic — they are purely re-export modules using `from <canonical> import <symbol>`.

---

## Constants

| Constant                  | Value          | Location                       | Purpose                                              |
|---------------------------|----------------|--------------------------------|------------------------------------------------------|
| `MAX_VALIDATION_ATTEMPTS` | `5`            | `src/interactive/session.py`   | Maximum consecutive invalid inputs before auto-exit  |
| Error log file path       | `"error.log"`  | `src/error_logger.py`          | Append-only structured error log                     |
| History file path         | `"history.txt"`| `src/support/history.py`       | Per-session operation history written on exit        |

All file paths are relative to the current working directory at the time the application is run.

---

## Future Extensibility Notes

- **Scientific mode:** `OperationRegistry` already reserves a `_scientific_operations` dict. Scientific mode operations can be registered via a separate `_load_scientific_operations()` method and exposed only when a mode flag is active.
- **New operation arity:** The `(method, arity)` tuple in the registry can be extended to a named tuple or dataclass if additional metadata (e.g. display name, help text) is needed.
- **Output formatting:** `format_result()` in `src/interface/output_formatter.py` is the single point where results are converted to strings, making precision or locale changes a one-line modification.
- **Alternative history backends:** `HistoryTracker.save_to_file()` is the only method that touches the filesystem. Replacing it with a database or remote write requires changing only that method.
