# Architecture Overview

This document describes the structure of the Calculator application as implemented in `src/`.

---

## High-Level Architecture

The application is organised into three conceptual layers: a **core computation layer**, a **session and CLI layer**, and **supporting infrastructure**.

### Core Computation Layer

**`src/core/calculator.py` — `Calculator` class**

The central public API. All computation is delegated to one of two static operation classes; `Calculator` itself contains no arithmetic logic.

Public methods:

| Method | Delegates to |
|---|---|
| `add(a, b)` | `NormalOperations.add` |
| `subtract(a, b)` | `NormalOperations.subtract` |
| `multiply(a, b)` | `NormalOperations.multiply` |
| `divide(a, b)` | `NormalOperations.divide` |
| `factorial(n)` | `ScientificOperations.factorial` |
| `square(x)` | `ScientificOperations.square` |
| `cube(x)` | `ScientificOperations.cube` |
| `square_root(x)` | `ScientificOperations.square_root` |
| `cube_root(x)` | `ScientificOperations.cube_root` |
| `logarithm(x)` | `ScientificOperations.logarithm` |
| `natural_logarithm(x)` | `ScientificOperations.natural_logarithm` |
| `power(base, exponent)` | `ScientificOperations.power` |

**`src/core/operations/normal.py` — `NormalOperations` class**

Contains four static methods for basic arithmetic: `add`, `subtract`, `multiply`, and `divide`. No validation is performed here; division by zero raises Python's built-in `ZeroDivisionError`.

**`src/core/operations/scientific.py` — `ScientificOperations` class**

Contains eight static methods for advanced operations: `factorial`, `square`, `cube`, `square_root`, `cube_root`, `logarithm`, `natural_logarithm`, and `power`. Each method validates its inputs (type and domain) before computing and raises `TypeError` or `ValueError` on constraint violations. Uses the standard library `math` module for `sqrt`, `log`, `log10`, and `copysign`.

---

## Session and CLI Layer

**`src/session.py` — `CalculatorSession` class**

Manages all REPL state for a single interactive session. Owns a `Calculator` instance, an `OperationHistory` instance, and an `ErrorLogger` instance. Performs no I/O (no `print` or `input` calls); all results are returned as values or strings to the caller.

Public methods:

| Method | Purpose |
|---|---|
| `select_operation(raw_choice, mode)` | Resolves user input (name or number) to a canonical operation name; returns `(op_name, exit_code)` |
| `collect_operands(arity, mode)` | Prompts for numeric operands using `OperandValidationSession`; returns `(operands, exit_code)` |
| `execute_operation(op_name, operands)` | Calls the named operation on the calculator; returns `(result, error_msg)` |
| `get_arity(op_name)` | Returns the operand count for a named operation |
| `record_history(op_name, operands, result)` | Records a successful operation in the history |
| `get_history()` | Returns all recorded history entries as a list of strings |
| `save_history(filepath)` | Persists the history to a plain-text file |
| `get_operation_list()` | Returns the current list of available operation names |
| `max_retries` (property) | Returns the maximum retry limit from the validation module |

**`src/cli.py` — `interactive_session(calculator)` function**

Implements the menu-driven REPL loop. Detects the runtime mode via `detect_mode()`, creates a `CalculatorSession`, and loops until the user quits. Business logic (operation execution, history, error logging) is delegated entirely to `CalculatorSession`. Output formatting is delegated to `src/formatter.py`. Handles quit aliases (`quit`, `exit`, `q`) and the history display command (`history`, `h`).

Additional module-level helpers: `get_arity(calculator, op_name)`, `get_operation_menu(calculator)`, `parse_float(value)`, `get_operands(arity, mode)`.

**`src/formatter.py` — Pure output formatting**

Stateless functions that convert data to display strings. No I/O, no imports from other application modules.

| Function | Returns |
|---|---|
| `format_menu_header(operations)` | Multi-line numbered operation menu |
| `format_quit_instruction()` | Quit and history shortcut hint lines |
| `format_history_header()` | Header string for the history section |
| `format_operation_error(operation)` | Error string for an invalid operation |
| `format_result(op_name, operands, result)` | Formatted result line, e.g. `"  Result: 5"` |
| `format_error(error_msg)` | Formatted error line, e.g. `"  Error: division by zero"` |

---

## Validation and Mode Detection

**`src/validation.py`**

Provides mode detection and session-scoped input validation classes.

- `detect_mode() -> str`: Returns `'interactive'` if `sys.stdin.isatty()`, otherwise `'cli'`.
- `format_operation_error(available_ops)`: Formats a human-readable list of valid operations.
- `OperandValidationSession`: Manages retry logic for numeric (float) operand input. In interactive mode, allows up to `_MAX_RETRIES_DEFAULT` (5) consecutive failures before returning `None`. In CLI mode, raises `SystemExit` on the first invalid value.
- `OperationValidationSession`: Manages retry logic for operation name input. Same retry and fast-fail behaviour as above, with case-insensitive matching against a provided list of valid operation names.

The module-level constant `_MAX_RETRIES_DEFAULT = 5` governs the retry limit for both session classes.

---

## Supporting Infrastructure

**`src/history.py` — `OperationHistory` class**

Records successful operations as formatted strings. Entries use the pattern `operation_name(arg1, arg2) = result`. Whole-number floats are displayed without the decimal point (e.g. `3.0` becomes `3`). Persistence is via `save_to_file(filepath)`, which writes all entries to a plain-text file (one entry per line). History is session-scoped and not shared across runs.

Public methods: `record_operation`, `get_history`, `clear`, `save_to_file`.

**`src/error_logger.py` — `ErrorLogger` class**

Appends categorised `ERROR`-level records to a log file (default `error.log`) using Python's `logging` module. Has no console handlers — all logging is silent to the user. The file is opened in append mode so records from previous sessions are preserved.

Logging methods and their categories:

| Method | Category label |
|---|---|
| `log_unsupported_operation(operation_name)` | `UNSUPPORTED_OPERATION` |
| `log_invalid_operand(operand, reason)` | `INVALID_OPERAND` |
| `log_incorrect_arity(operation_name, expected, got)` | `INCORRECT_ARITY` |
| `log_division_by_zero(numerator)` | `DIVISION_BY_ZERO` |
| `log_invalid_domain(operation_name, operand, reason)` | `INVALID_DOMAIN` |

Log record format: `%(asctime)s [%(levelname)s] %(message)s`

---

## Entry Point

**`src/__main__.py` — `main()` function**

Creates a `Calculator` instance and passes it to `interactive_session(calc)`. Invoked via `python -m src`.

---

## Backward Compatibility

**`src/calculator.py`**

A compatibility shim. Re-exports `Calculator` from `src.core.calculator` so that any existing consumer importing `src.calculator.Calculator` continues to work without modification.

---

## Module Dependency Graph

```
src/__main__.py
  └── src.core.calculator (Calculator)
  └── src.cli (interactive_session)

src/cli.py
  ├── src.core.calculator (Calculator)
  ├── src.formatter (format_*)
  ├── src.session (CalculatorSession)
  └── src.validation (detect_mode, OperandValidationSession,
                      OperationValidationSession, format_operation_error)

src/session.py
  ├── src.core.calculator (Calculator)
  ├── src.error_logger (ErrorLogger)
  ├── src.history (OperationHistory)
  └── src.validation (OperandValidationSession, OperationValidationSession)

src/core/calculator.py
  ├── src.core.operations.normal (NormalOperations)
  └── src.core.operations.scientific (ScientificOperations)

src/core/operations/normal.py       (no internal imports)
src/core/operations/scientific.py   (math)
src/formatter.py                    (no internal imports)
src/history.py                      (no internal imports)
src/error_logger.py                 (logging)
src/validation.py                   (sys, collections.abc)
src/calculator.py                   (src.core.calculator — shim only)
```
