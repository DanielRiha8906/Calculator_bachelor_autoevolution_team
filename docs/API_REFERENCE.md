# API Reference

This document describes the public API of every module in the calculator application. All signatures are taken directly from the source code.

---

## Core Calculation API

### `src.core.calculator` — `Calculator`

The `Calculator` class provides all mathematical operations. Every method raises `TypeError` for wrong argument types and `ValueError` for domain violations. None of the methods print, log, or otherwise produce side effects.

```python
class Calculator:
    def add(self, a, b) -> int | float
    def subtract(self, a, b) -> int | float
    def multiply(self, a, b) -> int | float
    def divide(self, a, b) -> int | float
    def factorial(self, n: int) -> int
    def square(self, x: int | float) -> int | float
    def cube(self, x: int | float) -> int | float
    def square_root(self, x: int | float) -> float
    def cube_root(self, x: int | float) -> float
    def power(self, base: int | float, exponent: int | float) -> int | float
    def log(self, x: int | float) -> float
    def ln(self, x: int | float) -> float
```

#### `Calculator.add(a, b)`

Returns `a + b`. No type or domain restrictions beyond Python numeric arithmetic.

#### `Calculator.subtract(a, b)`

Returns `a - b`. No type or domain restrictions.

#### `Calculator.multiply(a, b)`

Returns `a * b`. No type or domain restrictions.

#### `Calculator.divide(a, b)`

Returns `a / b`. Raises `ZeroDivisionError` if `b` is `0`.

#### `Calculator.factorial(n: int) -> int`

Returns `n!`. Raises `TypeError` if `n` is not an `int` (floats are rejected). Raises `ValueError` if `n < 0`. `bool` values are accepted and treated as `0` or `1`.

#### `Calculator.square(x: int | float) -> int | float`

Returns `x * x`. Raises `TypeError` if `x` is not `int` or `float`.

#### `Calculator.cube(x: int | float) -> int | float`

Returns `x * x * x`. Raises `TypeError` if `x` is not `int` or `float`.

#### `Calculator.square_root(x: int | float) -> float`

Returns `math.sqrt(x)`. Raises `TypeError` if `x` is not `int` or `float`. Raises `ValueError` if `x < 0`.

#### `Calculator.cube_root(x: int | float) -> float`

Returns the real-valued cube root of `x`. Negative inputs are handled via sign extraction: `-(abs(x) ** (1/3))`. Raises `TypeError` if `x` is not `int` or `float`.

#### `Calculator.power(base: int | float, exponent: int | float) -> int | float`

Returns `base ** exponent`. Raises `TypeError` if either argument is not `int` or `float`. Raises `ValueError` if `base < 0` and `exponent` is not an `int` (which would produce a complex result).

#### `Calculator.log(x: int | float) -> float`

Returns `math.log10(x)` (base-10 logarithm). Raises `TypeError` if `x` is not `int` or `float`. Raises `ValueError` if `x <= 0`.

#### `Calculator.ln(x: int | float) -> float`

Returns `math.log(x)` (natural logarithm). Raises `TypeError` if `x` is not `int` or `float`. Raises `ValueError` if `x <= 0`.

---

### `src.core.operations` — `get_operation_registry`

```python
def get_operation_registry(calculator: Calculator) -> dict[str, tuple]
```

Builds and returns the operation registry by constructing an `OperationRegistry` instance and calling `get_all_operations()`.

**Args:**
- `calculator` — A `Calculator` instance whose bound methods are stored in the registry.

**Returns:**
A dict mapping operation name (`str`) to a `(method, arity)` 2-tuple where `method` is a bound `Calculator` method and `arity` is `1` (unary) or `2` (binary).

**Example:**

```python
from src.core.calculator import Calculator
from src.core.operations import get_operation_registry

registry = get_operation_registry(Calculator())
method, arity = registry["add"]
print(arity)   # 2
print(method(3, 4))  # 7
```

---

### `src.core.operations_manager` — `OperationRegistry`

```python
class OperationRegistry:
    def __init__(self, calculator: Calculator) -> None
    def get_all_operations(self) -> dict[str, tuple]
    def get_normal_operations(self) -> dict[str, tuple]
```

#### `OperationRegistry.__init__(calculator)`

Initializes the registry and calls `_load_normal_operations()` to populate the 12 standard operations.

#### `OperationRegistry.get_all_operations() -> dict[str, tuple]`

Returns a merged dict of `_normal_operations` and `_scientific_operations`. Currently identical to `get_normal_operations()` since no scientific operations are registered.

#### `OperationRegistry.get_normal_operations() -> dict[str, tuple]`

Returns a copy of the normal operations dict only.

---

## CLI API

### `src.cli` — `parse_arguments`, `execute_cli`

#### `parse_arguments(args: list[str]) -> tuple[str, list[str]]`

Delegates to `parse_cli_args` from `src.interface.input_parser`. Splits a raw argument list into an operation name and operand strings.

**Args:**
- `args` — List of strings where `args[0]` is the operation name and `args[1:]` are operand strings.

**Returns:**
A `(operation_name, operand_strs)` 2-tuple.

**Example:**

```python
from src.cli import parse_arguments

op, operands = parse_arguments(["add", "3", "4"])
# op == "add", operands == ["3", "4"]
```

#### `execute_cli(operation_name: str, operand_strs: list[str], registry: dict, calculator: Calculator) -> int`

Validates the operation, checks operand count, converts operand strings to numbers, dispatches the operation, and prints the result to stdout.

**Args:**
- `operation_name` — The operation to run.
- `operand_strs` — Raw string operands from `sys.argv`.
- `registry` — The dict returned by `get_operation_registry(calculator)`.
- `calculator` — A `Calculator` instance.

**Returns:**
`0` on success, `1` on any error (errors are written to stderr and logged to `error.log`).

Does not call `sys.exit()`.

---

## Interface API

### `src.interface.input_parser`

#### `parse_cli_args(args: list[str]) -> tuple[str, list[str]]`

Splits `args` into `(args[0], args[1:])`.

```python
parse_cli_args(["add", "3", "4"])    # -> ("add", ["3", "4"])
parse_cli_args(["factorial", "5"])   # -> ("factorial", ["5"])
```

#### `convert_operand(value: str) -> int | float`

Converts a numeric string to `int` or `float`. Strings representing whole numbers (e.g. `"3.0"`) are returned as `int`. Raises `ValueError` if the string is not parseable as a number.

```python
convert_operand("3")    # -> 3     (int)
convert_operand("3.0")  # -> 3     (int)
convert_operand("3.5")  # -> 3.5   (float)
```

---

### `src.interface.output_formatter`

#### `format_result(result: int | float) -> str`

Converts a numeric result to its string representation via `str(result)`.

```python
format_result(42)    # -> "42"
format_result(3.14)  # -> "3.14"
```

---

### `src.interface.menu_renderer`

#### `display_menu(registry: dict) -> None`

Prints the numbered operation menu to stdout. Each operation is listed with its index and arity hint. The `h` and `q` options are always appended.

```python
display_menu(registry)
# Available operations:
#    1. add (2 operands)
#    2. subtract (2 operands)
#    ...
#    h. View history
#    q. quit
```

---

## Interactive Session API

### `src.interactive.session`

#### Module-level constants

```python
MAX_VALIDATION_ATTEMPTS: int = 5
_HISTORY_TOKEN: str = "h"
```

#### `run_interactive_session(calculator: Calculator, history_tracker: HistoryTracker | None = None) -> None`

Runs the main interactive calculator loop. Displays the menu, collects input, dispatches operations, prints results, handles errors, and saves history on exit.

If `history_tracker` is `None`, a new `HistoryTracker()` is created internally.

The session terminates when:
- The user enters `q`, `quit`, or `exit`.
- `MAX_VALIDATION_ATTEMPTS` consecutive invalid inputs are entered for operation selection or operand input.

`history_tracker.save_to_file()` is called unconditionally on exit.

#### `get_operation_choice(registry: dict[str, tuple]) -> tuple | None`

Prompts the user to select an operation. Accepts operation names (case-insensitive) or menu numbers.

**Returns one of:**
- `(name, method, arity)` — a valid operation was selected.
- `None` — the user entered a quit command.
- `("h", None, None)` — the user requested history.
- `(None, None, None)` — `MAX_VALIDATION_ATTEMPTS` consecutive invalid entries.

#### `get_operands(arity: int) -> list[float] | None`

Prompts for `arity` numeric operand values, one per prompt. Each value is parsed as `float()`.

**Returns:**
- A list of `arity` floats on success.
- `None` if `MAX_VALIDATION_ATTEMPTS` cumulative invalid entries were made across all operand slots.

---

### `src.interactive.input_handler`

Re-exports the following from `src.interactive.session`:

- `get_operation_choice`
- `get_operands`
- `MAX_VALIDATION_ATTEMPTS`
- `_HISTORY_TOKEN`
- `_error_logger`

---

## Support API

### `src.support.history` — `HistoryTracker`

```python
class HistoryTracker:
    def __init__(self) -> None
    def record(self, operation_name: str, operands: list, result: object) -> None
    def get_history(self) -> list[str]
    def display(self) -> None
    def save_to_file(self, filepath: str = "history.txt") -> None
    def clear(self) -> None
```

#### `HistoryTracker.record(operation_name, operands, result)`

Appends `"operation_name(arg1, arg2, ...) = result"` to the in-memory history list.

#### `HistoryTracker.get_history() -> list[str]`

Returns a shallow copy of the history list.

#### `HistoryTracker.display() -> None`

Prints all history entries to stdout. Prints `"No history for this session."` if the list is empty.

#### `HistoryTracker.save_to_file(filepath: str = "history.txt") -> None`

Writes history to the given file path, one entry per line, overwriting any existing file. `OSError` is caught and a warning is printed to stderr.

#### `HistoryTracker.clear() -> None`

Removes all entries from the in-memory history list.

---

### `src.error_logger` — `ErrorLogger`

```python
class ErrorLogger:
    def log_error(self, error_type: str, context: dict[str, Any]) -> None
```

#### `ErrorLogger.log_error(error_type, context)`

Writes a structured error entry to `error.log`.

**Args:**
- `error_type` — A short uppercase string identifying the error category (e.g. `"INVALID_OPERAND"`).
- `context` — A dict with optional keys `"operation"`, `"operands"`, and `"message"`. Missing keys default to `"N/A"` in the log entry.

**Log format:**

```
TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE
```

`error.log` is created lazily on the first call. `OSError` during file creation and any exception during formatting are silently swallowed so logging never crashes the application.

Multiple `ErrorLogger` instances share the same module-level `logging.Logger` and write to the same file.

---

## Entry Points

### `main.py` — CLI entry point

```python
def main() -> None
```

Reads `sys.argv[1:]`, validates that at least one argument is present, constructs `Calculator` and the operation registry, and delegates to `execute_cli()`. Calls `sys.exit()` with the returned exit code.

Invoked via:

```bash
python main.py <operation> [operand ...]
```

### `src/__main__.py` — Interactive entry point

```python
def main() -> None
```

Instantiates `Calculator()` and `HistoryTracker()` and passes them to `run_interactive_session()`.

Invoked via:

```bash
python -m src
```
