# Module Reference

This document describes every major module in the `src/` package.

---

## Calculator

**File:** `src/core/calculator.py`
**Exported via:** `src/core/__init__.py`, `src/__init__.py`, shim `src/calculator.py`

### Purpose

Pure-computation class. Implements every arithmetic and mathematical operation
supported by the application. Has no I/O dependencies and raises domain-specific
exceptions for invalid inputs.

### Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `add` | `(a, b) -> float` | Returns `a + b` |
| `subtract` | `(a, b) -> float` | Returns `a - b` |
| `multiply` | `(a, b) -> float` | Returns `a * b` |
| `divide` | `(a, b) -> float` | Raises `ZeroDivisionError` when `b == 0` |
| `factorial` | `(n: int) -> int` | Raises `TypeError` for booleans or non-int; `ValueError` for negative int |
| `square` | `(x: float) -> float` | Returns `x ** 2` |
| `cube` | `(x: float) -> float` | Returns `x ** 3` |
| `square_root` | `(x: float) -> float` | Raises `ValueError` when `x < 0` |
| `cube_root` | `(x: float) -> float` | Delegates to `math.cbrt`; defined for all reals |
| `log10` | `(x: float) -> float` | Raises `ValueError` when `x <= 0` |
| `ln` | `(x: float) -> float` | Raises `ValueError` when `x <= 0` |
| `power` | `(x: float, y: float) -> float` | Returns `x ** y` |

### Error Conditions

- `ZeroDivisionError`: `divide(a, 0)`
- `ValueError`: `square_root` of a negative; `log10` or `ln` of a non-positive; `factorial` of a negative integer
- `TypeError`: `factorial` of a boolean or non-integer type

### Used By

`OperationDispatcher.dispatch()` calls `Calculator` methods via `getattr`. Neither
`InputHandler` nor `CliDispatcher` call `Calculator` directly.

---

## OperationDispatcher

**File:** `src/shared/dispatcher.py`
**Exported via:** `src/shared/__init__.py`, `src/__init__.py`, shim `src/dispatcher.py`

### Purpose

Centralises the two pieces of dispatch logic shared by interactive and CLI modes:

1. Coercing raw string operands to typed numeric values.
2. Resolving and calling the correct `Calculator` method by name.

Has no I/O, no logging, and no dependency on any specific interaction mode.

### Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__` | `(calculator: Calculator) -> None` | Stores the `Calculator` reference |
| `coerce_operands` | `(raw_args: list[str], coerce: Callable) -> list` | Applies `coerce` to each element; raises `ValueError` on first failure |
| `dispatch` | `(op_key: str, operands: list) -> float \| int` | Resolves `OPERATIONS[op_key]["method"]`, calls it on `calculator` |

### Error Conditions

- `ValueError`: raised by `coerce_operands` when any element cannot be converted
- `ValueError`, `ZeroDivisionError`, `TypeError`: propagated unmodified from `Calculator` methods through `dispatch`

### Used By

`InputHandler` and `CliDispatcher` each hold an `OperationDispatcher` instance and
delegate all coercion and dispatch to it.

---

## InputHandler

**File:** `src/session/input_handler.py`
**Exported via:** `src/session/__init__.py`, shim `src/input_handler.py`

### Purpose

Drives the interactive REPL session. Owns the prompt loop, retry logic, error
handling for session context, and session teardown (history file write).

### Key Classes and Functions

| Name | Kind | Description |
|------|------|-------------|
| `MAX_RETRIES` | constant (`int = 5`) | Maximum consecutive invalid inputs before session or operand collection terminates |
| `InputHandler` | class | Full session driver |
| `run_session` | function | Convenience wrapper: creates `InputHandler` and calls `run()` |

### InputHandler Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__` | `(calculator, input_fn=None, logger=None) -> None` | `input_fn` defaults to `builtins.input`; `logger` is created lazily in `run()` |
| `run` | `() -> None` | Starts the session loop; writes `history.txt` on exit regardless of how the loop ends |

### Error Conditions

- If the user enters an unknown operation `MAX_RETRIES` times in a row, the session
  ends with `"Too many invalid attempts. Ending session."`.
- If operand entry fails `MAX_RETRIES` times for a single operand slot, a `ValueError`
  is raised internally, caught in `run()`, and the current operation is aborted.
- `StopIteration` from the input callable (exhausted input source) causes a clean
  `"Goodbye!"` exit.

### Used By

`src/__main__.py` calls `run_session(calc)` to start the interactive session.

---

## CliDispatcher

**File:** `src/interface/cli.py`
**Exported via:** `src/interface/__init__.py`, `src/__init__.py`, shim `src/cli.py`

### Purpose

Parses command-line arguments and executes a single calculation. Prints the result to
stdout on success or an error message to stderr on failure.

### Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__` | `(calculator: Calculator, logger: Logger \| None = None) -> None` | `logger` is created lazily in `dispatch_from_args()` |
| `dispatch_from_args` | `(args: list[str]) -> int` | Returns `0` on success, `1` on any error |

### Error Conditions

All errors print to stderr and return exit code `1`:

- No arguments provided (prints usage)
- Unknown operation key
- Wrong number of operands for the requested operation
- Invalid operand (cannot be coerced to the expected type)
- Domain error from `Calculator` (e.g. division by zero, negative square root)

### Used By

`main.py:main()` creates a `CliDispatcher` and calls `dispatch_from_args(sys.argv[1:])`.

---

## Logger

**File:** `src/shared/logger.py`
**Exported via:** `src/shared/__init__.py`, `src/__init__.py`, shim `src/logger.py`

### Purpose

File-based error logger. Wraps Python's `logging` module with calculator-specific
methods. Appends to `error.log` (or a configurable path) in plain-text format across
all runs. Records only error events — not successful operations.

### Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__` | `(log_file: str = "error.log") -> None` | Opens or creates `log_file` in append mode |
| `log_unsupported_operation` | `(operation: str) -> None` | WARNING level |
| `log_invalid_operand` | `(raw_value: str, expected_type: str) -> None` | ERROR level |
| `log_invalid_argument_count` | `(operation: str, expected: int, given: int) -> None` | ERROR level |
| `log_division_by_zero` | `(operands: list) -> None` | ERROR level |
| `log_domain_error` | `(operation: str, error_message: str) -> None` | ERROR level |

### Log Format

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

### Used By

`InputHandler.run()` and `CliDispatcher.dispatch_from_args()` both instantiate and
call `Logger` methods when errors occur.

---

## History

**File:** `src/session/history.py`
**Exported via:** `src/session/__init__.py` (indirectly), shim `src/history.py`

### Purpose

Session-scoped operation recorder. Stores successful operations in function-call
notation and writes them to `history.txt` when the session ends.

### Public Interface

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__` | `() -> None` | Initialises empty `_operations` list |
| `add_operation` | `(operation_name: str, operands: list, result: float \| int) -> None` | Appends formatted entry |
| `get_all` | `() -> list[str]` | Returns a shallow copy of all entries |
| `save_to_file` | `(filepath: str) -> None` | Writes one entry per line; raises `OSError` on failure |

### Entry Format

```
operation_name(arg1, arg2, ...) = result
```

Example: `add(10.0, 5.0) = 15.0`

### Used By

`InputHandler` creates one `History` instance per session and calls `add_operation`
after each successful calculation. `run()` calls `save_to_file("history.txt")` in a
`finally` block before returning.

---

## OPERATIONS Registry

**File:** `src/operations/__init__.py` (composition),
`src/operations/normal.py` (normal operations),
`src/operations/scientific.py` (scientific operations, currently empty)

**Exported via:** `src/__init__.py`, shim `src/operations.py`

### Purpose

Single source of truth for all supported operations. Both `InputHandler` and
`CliDispatcher` read from this registry to determine available operations, required
arity, operand type coercion, and the human-readable label shown in the menu.

### Registry Structure

```python
OPERATIONS: dict[str, dict] = {
    "<key>": {
        "method": "<Calculator method name>",
        "arity": <1 or 2>,
        "label": "<human-readable description>",
        "coerce": <callable>,   # optional; defaults to float
    },
    ...
}
```

### Current Entries (NORMAL_OPERATIONS)

| Key | Method | Arity | Coerce |
|-----|--------|-------|--------|
| `add` | `add` | 2 | float |
| `subtract` | `subtract` | 2 | float |
| `multiply` | `multiply` | 2 | float |
| `divide` | `divide` | 2 | float |
| `power` | `power` | 2 | float |
| `factorial` | `factorial` | 1 | int |
| `square` | `square` | 1 | float |
| `cube` | `cube` | 1 | float |
| `square_root` | `square_root` | 1 | float |
| `cube_root` | `cube_root` | 1 | float |
| `log10` | `log10` | 1 | float |
| `ln` | `ln` | 1 | float |

`SCIENTIFIC_OPERATIONS` is currently an empty dict reserved for future extension.

### Used By

`InputHandler._show_menu()`, `InputHandler.run()`,
`CliDispatcher.dispatch_from_args()`, and `OperationDispatcher.dispatch()` all
import and read `OPERATIONS`.
