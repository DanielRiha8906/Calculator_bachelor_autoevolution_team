# Architecture Overview

## Module Organization

The application source code lives entirely under `src/` and is organized into
three sub-packages:

```
src/
├── __init__.py          # Exports Calculator, ErrorLogger, REPLInterface
├── __main__.py          # Entry point (python -m src)
├── calculator.py        # Canonical Calculator implementation
├── cli.py               # Backward-compat shim -> src.interface.cli
├── error_logger.py      # Backward-compat shim -> src.support.error_logger
├── exceptions.py        # Backward-compat shim -> src.support.exceptions
├── history.py           # Backward-compat shim -> src.support.history
├── repl.py              # Backward-compat shim -> src.interface.repl
│
├── core/
│   ├── __init__.py      # Exports CalculationEngine, Operation, OperationRegistry
│   ├── engine.py        # CalculationEngine — four arithmetic operations
│   └── operations.py    # Operation dataclass, _CATALOG, OperationRegistry
│
├── interface/
│   ├── __init__.py      # Exports CLIHandler, REPLInterface
│   ├── cli.py           # CLIHandler — non-interactive CLI argument processing
│   └── repl.py          # REPLInterface — menu-driven interactive loop
│
└── support/
    ├── __init__.py      # Exports ErrorLogger, MaxRetriesExceeded, OperationHistory
    ├── error_logger.py  # ErrorLogger — flat-file error recording
    ├── exceptions.py    # MaxRetriesExceeded custom exception
    └── history.py       # OperationHistory — flat-file operation history
```

---

## Component Descriptions

### Calculator (`src/calculator.py`)

The `Calculator` class is the public facade for all calculation operations. It
owns the scientific and root operations directly (`factorial`, `square`, `cube`,
`square_root`, `cube_root`, `power`, `logarithm`, `natural_logarithm`) and
delegates the four basic arithmetic operations to an internal
`CalculationEngine` instance.

Neither the CLI nor the REPL calls `Calculator` methods directly. They use
`OperationRegistry.dispatch`, which calls `Calculator` methods via `getattr`.

### CalculationEngine (`src/core/engine.py`)

`CalculationEngine` implements the four fundamental arithmetic operations: `add`,
`subtract`, `multiply`, `divide`. It is instantiated and held privately by
`Calculator`. The engine raises `ZeroDivisionError` when dividing by zero.

There is no public API contract requiring callers to interact with
`CalculationEngine` directly; all external access goes through `Calculator`.

### OperationRegistry (`src/core/operations.py`)

`OperationRegistry` is the single authoritative source for:

- the complete list of supported operations and their metadata (defined in the
  module-level `_CATALOG` list of `Operation` dataclass instances),
- token resolution — mapping names and aliases to canonical operation names,
- arity lookup — how many operands each operation requires,
- operation dispatch — calling the correct `Calculator` method with the
  validated operands.

The registry holds a flat `_lookup` dict built at construction time from the
`_CATALOG`. Every accepted token (canonical name plus all aliases) maps to the
corresponding `Operation` instance.

The `logarithm` operation is a special case inside `dispatch`: rather than
forwarding to `Calculator.logarithm` (which is base-10 only), the registry
executes `math.log(x, base)` directly, implementing a two-argument arbitrary-
base logarithm with its own domain validation.

### REPLInterface (`src/interface/repl.py`)

`REPLInterface` drives the interactive menu loop. It:

1. Displays a numbered menu of operations derived from the registry.
2. Accepts and validates a menu selection (with up to MAX_RETRIES = 3 retries).
3. Prompts for operands, offering the previous result as a default for the
   first operand of each operation.
4. Delegates execution to `OperationRegistry.dispatch`.
5. Prints the result in the form `OperationDisplayName(operands) = result`.
6. Records the operation in `OperationHistory` (if provided).
7. Logs errors to `ErrorLogger` (if provided).

### CLIHandler (`src/interface/cli.py`)

`CLIHandler` handles non-interactive execution from the command line. It:

1. Parses a `list[str]` of arguments (operation token followed by operand
   strings) via `parse_args`.
2. Resolves the operation token and validates operand count using
   `OperationRegistry`.
3. Dispatches the operation via `OperationRegistry.dispatch`.
4. Records the result in `OperationHistory` (if provided).
5. Logs errors to `ErrorLogger` (if provided) before re-raising.

### ErrorLogger (`src/support/error_logger.py`)

`ErrorLogger` writes errors to a flat text file (`error.log` by default). Each
entry is one line in the format:

```
<ISO8601 timestamp> | <ERROR_TYPE> | input=<user_input> | <error message>
```

Three error type constants are defined: `INVALID_INPUT`,
`UNSUPPORTED_OPERATION`, and `CALCULATION_ERROR`. All file I/O errors are
caught and logged to stderr so they never interrupt the calculator session.

### OperationHistory (`src/support/history.py`)

`OperationHistory` records completed operations to a flat text file
(`history.txt` by default). Each entry is one line in the form
`operation(operands) = result`. File I/O errors are swallowed in the same way
as `ErrorLogger`. The REPL reads history back via `display_history()` when the
user types `history`.

---

## Data Flow

### REPL Mode

```
python -m src
  -> __main__.main()
     -> OperationHistory.clear_history()
     -> ErrorLogger.clear_errors()
     -> Calculator()
     -> REPLInterface(calc, history, error_logger)
        -> REPLInterface.run()
           loop:
             -> get_operation_selection()      [prints menu, reads stdin]
             -> get_operand()                  [reads stdin, validates float]
             -> OperationRegistry.dispatch()   [calls Calculator method]
             -> display_result()               [prints to stdout]
             -> OperationHistory.record_operation()
             [on error] -> ErrorLogger.log_error()
```

### CLI Mode

```
python -m src <operation> <operands...>
  -> __main__.main(argv)
     -> OperationHistory.clear_history()
     -> ErrorLogger.clear_errors()
     -> Calculator()
     -> CLIHandler(calc, history, error_logger)
        -> CLIHandler.execute(argv)
           -> CLIHandler.parse_args(argv)       [resolves token, validates operands]
           -> OperationRegistry.dispatch()      [calls Calculator method]
           -> OperationHistory.record_operation()
           [on error] -> ErrorLogger.log_error()
     -> print(result)
     -> sys.exit(0)
  [on error] -> print(error, stderr) -> sys.exit(non-zero)
```

---

## Operation Dispatch Mechanism

All operation execution flows through `OperationRegistry.dispatch(operation, operands)`:

1. If `operation == "logarithm"`, the registry executes
   `math.log(x, base)` directly with explicit domain validation.
2. For all other operations, `getattr(self.calculator, operation)(*operands)`
   is called — this dynamically resolves the method by name on the `Calculator`
   instance.

This means the `Calculator` class acts as the implementation target but never
needs to know about the registry or either interface layer.

---

## Backward Compatibility

When the codebase was modularized into `src/core/`, `src/interface/`, and
`src/support/`, shim modules were created at the old locations to avoid
breaking any existing imports:

| Shim path | Canonical location |
|-----------|-------------------|
| `src/cli.py` | `src/interface/cli.py` |
| `src/repl.py` | `src/interface/repl.py` |
| `src/error_logger.py` | `src/support/error_logger.py` |
| `src/history.py` | `src/support/history.py` |
| `src/exceptions.py` | `src/support/exceptions.py` |

Each shim re-exports the same public names from the canonical module. New code
should import from the canonical locations.
