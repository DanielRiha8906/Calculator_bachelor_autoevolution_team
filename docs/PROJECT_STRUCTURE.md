# Project Structure

## Directory Structure

```
Calculator_bachelor_autoevolution_team/
├── src/                        # Application source code
│   ├── __init__.py             # Package exports
│   ├── __main__.py             # Entry point (python -m src)
│   ├── calculator.py           # Core Calculator class
│   ├── cli.py                  # CLIHandler for non-interactive mode
│   ├── error_logger.py         # ErrorLogger for error tracking
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # OperationHistory for session recording
│   ├── operations.py           # OperationRegistry and Operation dataclass
│   └── repl.py                 # REPLInterface for interactive mode
├── tests/                      # Test suite
│   ├── test_calculator.py
│   ├── test_cli.py
│   ├── test_error_logger.py
│   ├── test_history.py
│   ├── test_operations.py
│   └── test_repl.py
├── artifacts/                  # PlantUML diagrams and development artifacts
├── docs/                       # User-facing documentation
│   ├── FEATURES.md
│   ├── PROJECT_STRUCTURE.md
│   └── USER_GUIDE.md
├── suggestions/                # Proposed policy/workflow changes (human-review artifacts)
├── CLAUDE.md                   # Project instructions for autonomous agents
├── README.md                   # Project overview and quick start
├── progress.md                 # Autonomous run summaries for thesis reproducibility
└── requirements.txt            # Python dependencies
```

---

## Module Overview

### `src/__init__.py`

Exports the three primary public classes so that external consumers can import directly from `src`:

- `Calculator`
- `ErrorLogger`
- `REPLInterface`

### `src/calculator.py` — Core Calculator class

Contains the `Calculator` class, which implements all mathematical operations as plain methods. It has no state and no dependencies on other `src` modules.

Operations implemented directly on `Calculator`:
- Binary: `add`, `subtract`, `multiply`, `divide`, `power`
- Unary: `factorial`, `square`, `cube`, `square_root`, `cube_root`, `natural_logarithm`

Note: `Calculator.logarithm` implements base-10 log for a single argument. The two-argument `logarithm(x, base)` variant exposed to users is handled by `OperationRegistry.dispatch`, not by `Calculator` directly.

### `src/operations.py` — OperationRegistry and Operation dataclass

Two key components:

**`Operation` (frozen dataclass)**
Holds metadata for a single calculator operation:
- `name`: canonical method name (e.g. `"add"`)
- `arity`: 1 (unary) or 2 (binary)
- `display_name`: human-readable label for menus
- `aliases`: additional accepted tokens (e.g. `("+",)` for `"add"`)

**`OperationRegistry`**
The single authoritative source for:
- the full operation catalog (12 operations in `_CATALOG`)
- token-to-operation lookup including aliases
- arity validation
- dispatching operations to a `Calculator` instance

`OperationRegistry.dispatch` contains the special-case logic for the two-argument `logarithm(x, base)` so that neither `CLIHandler` nor `REPLInterface` duplicates it.

### `src/cli.py` — CLIHandler

Handles non-interactive (CLI) usage. Accepts a list of argument strings (`[operation, operand1, operand2?]`), parses and validates them, dispatches to `OperationRegistry`, and returns the numeric result.

Key methods:
- `parse_args(args)`: validates operation name and operand count/format
- `execute(args)`: full parse-dispatch-record pipeline; logs errors via `ErrorLogger` and records successful operations via `OperationHistory`
- `get_operation_mapping()`: delegates to `OperationRegistry` to expose the token-to-name mapping

### `src/repl.py` — REPLInterface

Provides an interactive Read-Eval-Print Loop. Presents a numbered menu of all 12 operations, prompts for operands, dispatches via `OperationRegistry`, and displays results. Carries the last result forward as an optional default for the next operation's first operand.

Key methods:
- `run()`: the main loop; handles `quit`, `history`, and operation selection
- `get_operation_selection()`: displays the menu, validates selection, raises `MaxRetriesExceeded` after 3 consecutive invalid inputs
- `get_operand(prompt)`: prompts for a number, supports carry-over default, raises `MaxRetriesExceeded` after 3 failures
- `display_result(operation, operands, result)`: prints a formatted result line

Module-level constant `OPERATIONS` (dict) is preserved for backwards compatibility with older imports.

### `src/history.py` — OperationHistory

Manages a flat-text operation history file (`history.txt` by default).

Key methods:
- `clear_history()`: truncates or creates the file at session start
- `record_operation(entry)`: appends one line per completed operation
- `display_history()`: reads and returns all entries as a list of strings

All I/O errors are caught and logged to stderr so history failures never interrupt a session.

### `src/error_logger.py` — ErrorLogger

Manages a flat-text error log file (`error.log` by default).

Error entries are written in the format:
```
<ISO8601 timestamp> | <error_type> | input=<user_input> | <exception message>
```

Three error type constants:
- `ErrorLogger.INVALID_INPUT`
- `ErrorLogger.UNSUPPORTED_OPERATION`
- `ErrorLogger.CALCULATION_ERROR`

Key methods:
- `clear_errors()`: truncates or creates the file at session start
- `log_error(error_type, user_input, exception)`: appends one structured entry
- `get_errors()`: reads and returns all entries as a list of strings

All I/O errors are caught and logged to stderr.

### `src/exceptions.py` — Custom exceptions

Defines application-specific exception types:

- `MaxRetriesExceeded`: raised by `REPLInterface` when the user exhausts the maximum number of allowed invalid-input retries (3 consecutive failures for either operation selection or operand entry).

### `src/__main__.py` — Entry point

Invoked via `python -m src`. Determines the interaction mode from `sys.argv`:

- **REPL mode**: no arguments, or a single `--repl` flag
- **CLI mode**: operation followed by one or two operands

In both modes, a fresh `OperationHistory` and `ErrorLogger` are created and cleared at startup. All CLI errors are mapped to specific exit codes (see the [User Guide](USER_GUIDE.md) for details).

---

## Architecture Description

The application follows a layered architecture:

```
User (stdin / argv)
        |
        v
   __main__.py          <- mode selection and wiring
        |
   +----+----+
   |         |
CLIHandler  REPLInterface    <- interaction layers
   |         |
   +---------+
        |
  OperationRegistry          <- catalog, arity, dispatch (single source of truth)
        |
    Calculator               <- pure math, no I/O
```

Side-channel services (`OperationHistory`, `ErrorLogger`) are injected into both `CLIHandler` and `REPLInterface` as optional dependencies, making them independently testable.

---

## Data Flow

### CLI mode

1. `__main__.main()` parses `sys.argv[1:]`.
2. `CLIHandler.execute(args)` is called.
3. `CLIHandler.parse_args(args)` resolves the token to a canonical name via `OperationRegistry.resolve` and validates operand count.
4. `OperationRegistry.dispatch(name, operands)` executes the operation (applying special-case logic for `logarithm`).
5. The result is recorded in `OperationHistory` and printed to stdout.
6. Errors are logged via `ErrorLogger` and the process exits with a non-zero code.

### REPL mode

1. `__main__.main()` creates a `REPLInterface` and calls `repl.run()`.
2. `REPLInterface.get_operation_selection()` displays the menu and returns a canonical operation name.
3. `REPLInterface.get_operand()` collects one or two numeric inputs (with optional carry-over from the previous result).
4. `REPLInterface._execute()` delegates to `OperationRegistry.dispatch`.
5. The result is displayed, stored as `last_result` for carry-over, and recorded in `OperationHistory`.
6. The loop repeats until the user types `quit` or sends EOF/interrupt.

---

## Design Patterns

- **Registry pattern**: `OperationRegistry` centralises all operation metadata and dispatch logic, eliminating duplication between `CLIHandler` and `REPLInterface`.
- **Dependency injection**: `OperationHistory` and `ErrorLogger` are passed into `CLIHandler` and `REPLInterface` as optional constructor arguments, enabling easy substitution in tests.
- **Frozen dataclass**: `Operation` is immutable, making catalog entries safe to share across all components without copying.
- **Single responsibility**: each module has one well-defined role; `Calculator` does math, `OperationRegistry` does routing, interaction layers handle I/O.

---

## Testing Structure

Tests live in `tests/` alongside the source, with one test file per source module:

| Test file               | Module under test        |
|-------------------------|--------------------------|
| `test_calculator.py`    | `src/calculator.py`      |
| `test_cli.py`           | `src/cli.py`             |
| `test_error_logger.py`  | `src/error_logger.py`    |
| `test_history.py`       | `src/history.py`         |
| `test_operations.py`    | `src/operations.py`      |
| `test_repl.py`          | `src/repl.py`            |

Run the full suite with:

```bash
python -m pytest tests/
```
