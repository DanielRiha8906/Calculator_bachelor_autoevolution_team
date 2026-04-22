# Architecture

This document describes the internal structure of the Calculator application: how modules relate to each other, how data flows from raw input to a recorded result, and where the system can be extended.

---

## Module Hierarchy

```
src/
├── main.py               Entry point — routes to REPL or CLI
├── calculator.py         Calculator facade (backward-compatible API)
├── logic.py              CalculatorEngine (computation + history)
├── modes/
│   ├── operations.py     BaseOperationSet ABC, OperationRegistry, canonical name sets
│   ├── basic.py          BasicOperations
│   └── advanced.py       AdvancedOperations
├── input_handler.py      ExpressionParser, InputValidator, CalculatorREPL
├── cli.py                CLIHandler, main_cli entry point
└── logger.py             get_logger factory
```

### Dependency graph (arrows = "imports from")

```
main.py
  ├── calculator.py
  │     └── logic.py
  │           ├── modes/basic.py
  │           │     └── modes/operations.py
  │           └── modes/advanced.py
  │                 └── modes/operations.py
  ├── input_handler.py
  │     ├── calculator.py
  │     ├── logger.py
  │     └── modes/operations.py
  └── cli.py
        ├── calculator.py
        ├── input_handler.py  (ExpressionParser, InputValidator)
        └── logger.py
```

`logger.py` and `modes/operations.py` are leaves with no intra-package dependencies.

---

## Class Responsibilities

### `Calculator` (`src/calculator.py`)

A thin facade that preserves the original public API. Every method call is forwarded unchanged to the underlying `CalculatorEngine`. Its only state is `_mode` (a string) and `_engine` (a `CalculatorEngine` instance). Calling `set_mode()` re-instantiates the engine, which also clears the history.

**Public interface:**

- `set_mode(mode: str)` — switch operation mode and reset the engine
- `get_history() -> list[dict]` — return session history
- `add`, `subtract`, `multiply`, `divide` — binary arithmetic
- `factorial`, `square`, `cube`, `square_root`, `cube_root`, `natural_log`, `log_base_10` — unary advanced operations
- `power` — binary advanced operation

### `CalculatorEngine` (`src/logic.py`)

The computation kernel. Composes one `BasicOperations` instance and one `AdvancedOperations` instance. After every successful call it records the operation to `_history` via `_record_history`. No UI or IO dependencies; safe to instantiate in any context.

**History record schema:**

```python
{
    "operand1": <first operand>,
    "operator": "<operation name>",
    "operand2": <second operand or None>,
    "result":   <numeric result>,
}
```

### `BasicOperations` (`src/modes/basic.py`)

Implements `add`, `subtract`, `multiply`, `divide`. Extends `BaseOperationSet`. Each method performs a pure computation, optionally invokes `_record()` (the injected callback), and returns the result. `divide` raises `ZeroDivisionError` on zero divisor and logs the failure before re-raising.

### `AdvancedOperations` (`src/modes/advanced.py`)

Implements `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `natural_log`, `log_base_10`. Same pattern as `BasicOperations`. Methods that can fail on invalid input (`factorial`, `square_root`, `natural_log`, `log_base_10`) log the error and re-raise.

### `BaseOperationSet` (`src/modes/operations.py`)

Abstract base class for operation classes. Provides:

- `__init__(record_callback)` — stores the optional callback
- `_record(result)` — calls the callback if one was supplied
- `get_operations() -> dict[str, Callable]` — abstract; must return the name-to-method mapping

### `OperationRegistry` (`src/modes/operations.py`)

Runtime registry that maps operation name strings to callables and to the mode that registered them. Not used by the main execution path but available as an extension point for dynamic mode switching.

### `ExpressionParser` (`src/input_handler.py`)

Converts a raw string to an `(operation, operands)` tuple.

Steps:
1. Strip and split the input on whitespace.
2. Lowercase the first token to get the operation name.
3. Coerce remaining tokens to `int` (preferred) or `float` via `_coerce_numeric`.

Raises `ValueError` on empty input or on tokens that cannot be parsed as numbers.

### `InputValidator` (`src/input_handler.py`)

Two-stage validation applied after parsing and before dispatch:

1. `validate_operation(operation)` — checks that the name is in `SUPPORTED_OPERATIONS` (the union of `BASIC_OPERATIONS` and `ADVANCED_OPERATIONS` from `modes/operations.py`).
2. `validate_operand_count(operation, operands)` — checks that the count matches the expected arity (1 for unary operations, 2 for binary).

Raises `ValueError` with a human-readable message on any failure.

### `CalculatorREPL` (`src/input_handler.py`)

Interactive read-eval-print loop. Composes `ExpressionParser`, `InputValidator`, and `Calculator`. On bad input it enters a configurable retry loop (default 3 retries, controlled by `RetryConfig`). Exits cleanly on `exit`/`quit` commands or `KeyboardInterrupt`. Handles `history` as a special command.

### `CLIHandler` (`src/cli.py`)

Non-interactive single-expression evaluator. Uses the same `ExpressionParser` and `InputValidator` as the REPL. Writes the result to stdout; writes all error messages to stderr. Returns exit code `0` on success and `1` on any failure.

### `get_logger` (`src/logger.py`)

Factory function that configures the root logger once (guarded by `_configured`) and then returns a named child logger. Configuration:

- **Console handler** — `WARNING` and above to stdout
- **File handler** — `DEBUG` and above to `calculator.log` (UTF-8, append mode)

---

## Data Flow

### Interactive REPL

```
stdin
  |
  v
CalculatorREPL.run()
  |
  +--> [special command: "history" / "exit" / "quit"]
  |
  v
_evaluate(raw_input)
  |
  v
ExpressionParser.parse(raw_input)
  --> (operation: str, operands: list[int | float])
  |
  v
InputValidator.validate(operation, operands)
  --> raises ValueError on bad name or wrong count
  |
  v
CalculatorREPL._dispatch(operation, operands)
  --> getattr(calculator, operation)(*operands)
  |
  v
Calculator.<method>(...)
  --> CalculatorEngine.<method>(...)
       |
       +--> BasicOperations.<method>(...)  or  AdvancedOperations.<method>(...)
       |        performs computation, raises on invalid input
       |
       +--> CalculatorEngine._record_history(...)
       |        appends dict to _history
       |
       +--> returns result
  |
  v
stdout: "Result: <value>"
```

### CLI

The same parse -> validate -> dispatch -> record flow applies. `CLIHandler.run()` is the coordinator instead of `CalculatorREPL._evaluate()`. There is no retry loop or history command; the process exits after one expression.

---

## Input Validation Pipeline

```
raw string
    |
    v
ExpressionParser._coerce_numeric()  -- per token
    raises ValueError on non-numeric token
    |
    v
ExpressionParser.parse()
    raises ValueError on empty input
    returns (operation, operands)
    |
    v
InputValidator.validate_operation()
    raises ValueError if operation not in SUPPORTED_OPERATIONS
    |
    v
InputValidator.validate_operand_count()
    raises ValueError if count != expected arity
    |
    v
dispatch to Calculator method
```

---

## History Tracking

History is stored as a plain Python list of dicts inside `CalculatorEngine._history`. It grows monotonically for the lifetime of the engine instance. Calling `Calculator.set_mode()` creates a new engine, which resets the history.

The list is accessible via `Calculator.get_history()` and `CalculatorEngine.get_history()`. The REPL exposes it through the `history` command.

No persistence to disk is performed; history is in-memory only.

---

## Logging Infrastructure

All modules obtain their logger via `get_logger(__name__)`. The factory configures the root logger the first time it is called:

| Handler        | Level   | Destination                |
|----------------|---------|----------------------------|
| Console        | WARNING | stdout (via `StreamHandler`) |
| File           | DEBUG   | `calculator.log` (append)  |

Format: `YYYY-MM-DD HH:MM:SS  LEVEL     module.name  message`

Operations that fail for mathematical reasons (zero division, domain errors, invalid factorial input) log at `ERROR` level inside the operation class before re-raising, so the log file contains a full trace even if the caller swallows the exception.

---

## Extension Points

### Adding a new basic operation

1. Add the method to `BasicOperations` in `src/modes/basic.py`.
2. Register it in the `get_operations()` dict of `BasicOperations`.
3. Add the name to `BASIC_OPERATIONS` in `src/modes/operations.py`.
4. Expose it via a forwarding method on `CalculatorEngine` in `src/logic.py`.
5. Expose it via a forwarding method on `Calculator` in `src/calculator.py`.

No changes to `InputValidator` or `ExpressionParser` are needed — they derive their operation sets from `BASIC_OPERATIONS` and `ADVANCED_OPERATIONS` at import time.

### Adding a new advanced operation

Follow the same steps as above, targeting `AdvancedOperations` and `ADVANCED_OPERATIONS` instead.

If the new operation is **unary** (one operand), it will automatically be added to `_ONE_OPERAND_OPS` in `input_handler.py` (which is derived from `ADVANCED_OPERATIONS - {"power"}`). If it is **binary**, add it to `_TWO_OPERAND_OPS` as well.

### Switching to persistent history

Replace `CalculatorEngine._history` (a list) with a custom storage object that implements `append` and returns a list-like on `__iter__`. No other change is needed because all callers interact with history only through `get_history()`.
