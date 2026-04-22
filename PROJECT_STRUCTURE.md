# Project Structure

## Directory layout

```
Calculator_bachelor_autoevolution_team/
├── src/                    # Application source code (Python package)
│   ├── __init__.py         # Public package exports
│   ├── __main__.py         # Entry point — interactive and CLI dispatch
│   ├── calculator.py       # Core arithmetic class
│   ├── cli.py              # CLI argument parsing and execution
│   ├── engine.py           # Pure computation orchestration layer
│   ├── error_logger.py     # Centralised error logging
│   ├── history.py          # Persistent operation history
│   ├── io_handler.py       # User input/output and REPL interaction
│   ├── operations.py       # Operation registry
│   ├── validation.py       # Input validation utilities
│   └── workflow.py         # Interactive session orchestration
├── tests/                  # Pytest test suite
├── artifacts/              # PlantUML development diagrams
├── logs/                   # Runtime error log (auto-created)
├── Calc_prompty/           # Prompt files for the auto-evolution system
├── CLAUDE.md               # Agent instruction document
├── GETTING_STARTED.md      # Quick-start guide
├── OPERATIONS.md           # Complete operation reference
├── PROJECT_STRUCTURE.md    # This file
├── README.md               # Project overview (Czech + English)
├── progress.md             # Per-run experiment log
└── requirements.txt        # Python dependencies (pytest only)
```

## Source modules (`src/`)

### `__init__.py`

Re-exports the main public classes so callers can import directly from `src`
without knowing internal sub-module paths.

Public exports: `Calculator`, `CalculationEngine`, `CalculatorWorkflow`,
`InputHandler`, `OperationRegistry`, `UserInterface`.

### `__main__.py`

Entry point invoked by `python -m src`.  Inspects `sys.argv`:

- **No arguments** — constructs `Calculator`, `InputHandler`,
  `OperationHistory`, and `OperationRegistry`, then runs the interactive REPL
  loop via `main()`.
- **Arguments present** — delegates to `cli.cli_main(sys.argv[1:])` for a
  single-expression CLI execution.

Key function: `main()`.

### `calculator.py`

Contains the `Calculator` class — the single authoritative source of
arithmetic logic.  Every public method performs exactly one computation and
logs any domain error before re-raising the original exception.

Intentionally limited to foundational operations.  Scientific or
domain-specific functions should be added via
`OperationRegistry.register_operation()` rather than by extending this class.

Key class: `Calculator`.

Methods: `add`, `subtract`, `multiply`, `divide`, `power`, `factorial`,
`square`, `cube`, `square_root`, `cube_root`, `log`, `ln`.

### `cli.py`

Handles the CLI execution path when the package is invoked with arguments.

- `parse_args(argv)` — converts raw argument strings to an operation name and
  a list of validated float operands.
- `execute_cli(operation, operands)` — resolves the operation from the
  registry, checks arity, converts integer-requiring operands (e.g.
  `factorial`), and invokes the bound `Calculator` method.
- `cli_main(argv)` — top-level entry point: calls `parse_args` and
  `execute_cli`, formats the result, and manages exit codes.

### `engine.py`

`CalculationEngine` is the pure computation layer between the workflow/CLI
and the operation registry.  It holds no I/O or UI logic.

- `execute_operation(operation_key, operands)` — looks up the key in the
  registry and calls the bound method with the unpacked operand list.

Any operation added to the registry via `register_operation()` is
automatically available here without any changes to this module.

Key class: `CalculationEngine`.

### `error_logger.py`

Provides a dedicated `logging.Logger` on the `calculator.errors` namespace.
Writes structured `ERROR`-level records to `logs/error.log` in ISO-8601
timestamped format.  Falls back silently to a `NullHandler` if the log
directory cannot be created, so a logging failure never crashes the
application.

Three public helpers:

- `log_validation_error(detail)` — logs bad operand input.
- `log_operation_error(operation_key, error_msg)` — logs unrecognised
  operation keys.
- `log_calculation_error(operation, operands, error_msg)` — logs domain or
  arithmetic failures (e.g. division by zero, square root of a negative
  number).

### `history.py`

`OperationHistory` appends each completed operation as a plain text line to
`history.txt`.  Line numbers are assigned at display time so the file itself
remains a simple append-only log.

- `record_operation(operation, operands, result)` — appends one entry.
- `display_history()` — returns a numbered, human-readable string of all
  entries, or `"No history yet."` when the file is absent or empty.
- `clear()` — deletes the history file; called at session start for a clean
  slate.
- `is_empty()` — returns `True` when no history exists.

Key class: `OperationHistory`.

### `io_handler.py`

Contains two classes:

**`InputHandler`** — drives all user-facing prompts in the interactive REPL.

- `get_operation_choice(available_operations)` — displays the menu, reads
  user input, and handles the `history`, `exit`, and `quit` sentinels.
  Raises `InputRetryExhaustedError` after 3 consecutive invalid entries.
- `get_operand(prompt)` — reads and validates a single numeric operand.
  Raises `InputRetryExhaustedError` after 3 invalid entries.
- `display_result(operation, operands, result)` — prints the formatted result.
- `display_error(message)` — prints a user-friendly error line.
- `display_history()` — delegates to the attached `OperationHistory`.

**`UserInterface`** — pure output class used by `CalculatorWorkflow`.  All
methods write to stdout and return `None`.

- `display_result`, `display_error`, `display_operations`, `display_history`.

**`InputRetryExhaustedError`** — raised when the user exhausts all retry
attempts for any input prompt.

### `operations.py`

`OperationRegistry` maps string keys to `(bound_method, arity, description)`
tuples.  Built-in operations are wired to `Calculator` instance methods in
`__init__`.

- `get_operation(key)` — returns the tuple or raises `KeyError` (and logs the
  error) for unknown keys.
- `list_operations()` — returns a `{key: description}` mapping used by the
  REPL menu.
- `register_operation(key, method, arity, description)` — adds a new
  operation at runtime.  Validates that the key is unique, `method` is
  callable, and `arity` is a positive integer.

Key class: `OperationRegistry`.

### `validation.py`

Centralised input validation utilities.

- `validate_operand(raw)` — converts a string to `float`; raises
  `OperandValidationError` on failure (after logging).
- `validate_operation(choice, available_operations)` — checks whether a
  string key exists in the registry mapping; logs and returns `False` on
  failure.
- `get_validation_error_message(error)` — returns the string representation
  of a validation exception for display.

Custom exceptions: `OperandValidationError`, `OperationValidationError`.

### `workflow.py`

`CalculatorWorkflow` coordinates the interactive session loop using
composition.  It holds references to a `CalculationEngine`, `InputHandler`,
`UserInterface`, and `OperationHistory` and contains no arithmetic logic.

- `run()` — main session loop: prompts for an operation, collects operands,
  executes via the engine, records in history, and displays the result.
- `_get_operands(operation_key)` — queries the registry for arity and prompts
  accordingly.
- `_handle_calculation_error(error)` — delegates error display to
  `UserInterface`.

Key class: `CalculatorWorkflow`.

## Tests (`tests/`)

The test suite uses `pytest` (the only external dependency).  Test files cover:

- `test_calculator.py` — unit tests for `Calculator` arithmetic methods.
- `test_cli.py` — tests for `parse_args`, `execute_cli`, and `cli_main`.
- `test_cli_mode_validation.py` — edge cases for CLI operand validation.
- `test_engine.py` — unit tests for `CalculationEngine.execute_operation`.
- `test_error_logger.py` — unit tests for each logging helper.
- `test_error_logging_integration.py` — integration: errors are written to the
  log file during calculation failures.
- `test_guided_mode_integration.py` — integration tests for guided interactive
  flows.
- `test_history.py` — unit tests for `OperationHistory`.
- `test_input_validation.py` — tests for `validate_operand` and related
  helpers.
- `test_integration.py` — end-to-end session integration tests.
- `test_interactive_session.py` — interactive REPL session tests.
- `test_io_handler.py` — unit tests for `InputHandler` and `UserInterface`.
- `test_io_handler_guided_mode.py` — guided mode specific I/O tests.
- `test_operations.py` — unit tests for `OperationRegistry`.
- `test_workflow.py` — unit tests for `CalculatorWorkflow`.

## Artifacts (`artifacts/`)

PlantUML source files (`.puml`) for development diagrams.  Diagrams are split
by concern rather than kept in a single monolithic file:

- **Class diagrams** — `calculator_class_diagram.puml`,
  `class_diagram_core.puml`, `class_diagram_calculator_io.puml`,
  `class_diagram_workflow.puml`, `class_error_logger.puml`.
- **Activity diagrams** — interactive loop, CLI mode, workflow loop, error
  flow, division, logarithm.
- **Sequence diagrams** — operation execution, CLI execution, history command,
  workflow operation execution, divide-by-zero flow.

## Logs (`logs/`)

Created automatically at runtime.  Contains `error.log`, an append-only file
of structured `ERROR`-level records produced by `error_logger.py`.  Each line
carries an ISO-8601 timestamp, level, logger name, error category
(`VALIDATION_ERROR`, `OPERATION_ERROR`, or `CALCULATION_ERROR`), and details.
The directory and file are created on first use; a missing `logs/` directory
never prevents the application from running.

## Design principles

**Separation of concerns** — arithmetic logic lives exclusively in
`Calculator`; I/O lives in `io_handler`; orchestration lives in `workflow` and
`__main__`; registry management lives in `operations`.  No module reaches
across these boundaries.

**OperationRegistry extension pattern** — the registry is the single point of
extension.  Adding a new operation requires only one `register_operation()`
call; `CalculationEngine`, `CalculatorWorkflow`, and the REPL menu all pick it
up automatically.  The `Calculator` class itself must not be modified for new
operations.

**Error logging** — every domain error (bad input, unknown operation,
arithmetic failure) is logged to `logs/error.log` before or alongside being
raised.  Logging failures are silently suppressed so they cannot crash the
application.

**No external dependencies beyond pytest** — the application uses only the
Python standard library (`math`, `logging`, `os`, `sys`).  `pytest` is the
sole development dependency, declared in `requirements.txt`.
