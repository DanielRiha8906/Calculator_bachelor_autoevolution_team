# API Reference

This document covers the public API of every importable class and function in the `src` package. It is intended for developers who consume the calculator programmatically or who are extending the system.

## Table of Contents

- [src.logic — Calculator Facade](#srclogic--calculator-facade)
  - [Calculator](#calculator)
- [src.logic.core — Arithmetic Engine](#srclogiccore--arithmetic-engine)
  - [ArithmeticEngine](#arithmeticengine)
- [src.operations — Operation Abstractions](#srcoperations--operation-abstractions)
  - [Operation](#operation)
  - [OperationRegistry](#operationregistry)
  - [register_basic_operations](#register_basic_operations)
  - [register_scientific_operations](#register_scientific_operations)
- [src.history — Operation History](#srchistory--operation-history)
  - [OperationRecord](#operationrecord)
  - [OperationHistory](#operationhistory)
- [src.presentation.cli — CLI Presentation](#srcpresentationcli--cli-presentation)
  - [parse_and_evaluate](#parse_and_evaluate)
  - [run_cli](#run_cli)
- [src.presentation.interactive — Interactive Presentation](#srcpresentationinteractive--interactive-presentation)
  - [parse_number](#parse_number)
  - [get_operands](#get_operands)
  - [execute_operation](#execute_operation)
  - [format_result](#format_result)
  - [run_interactive](#run_interactive)
  - [OPERATIONS constant](#operations-constant)
  - [InvalidInputError](#invalidinputerror)
  - [OperandRetryExceeded](#operandretryexceeded)
- [src.input_retry — Generic Retry Utility](#srcinput_retry--generic-retry-utility)
  - [InputRetryConfig](#inputretryconfig)
  - [validate_with_retry](#validate_with_retry)
  - [RetryLimitExceeded](#retrylimitexceeded)
- [src.logging_config — Logging Setup](#srclogging_config--logging-setup)
  - [setup_logging](#setup_logging)

---

## `src.logic` — Calculator Facade

Recommended import path: `from src.logic import Calculator`

### `Calculator`

```python
class Calculator
```

Stateful calculator that combines `ArithmeticEngine` (pure computation) with `OperationHistory` (record keeping). All arithmetic methods record their result automatically.

**Constructor**

```python
Calculator()
```

Creates a new `Calculator` with an empty history and a fully populated `OperationRegistry` (all 12 basic operations registered).

---

#### `Calculator.add`

```python
def add(self, a: int | float, b: int | float) -> int | float
```

Return the sum of `a` and `b`.

| Parameter | Type | Description |
|---|---|---|
| `a` | `int \| float` | First operand |
| `b` | `int \| float` | Second operand |

**Returns:** `a + b`

**Example:**
```python
calc = Calculator()
calc.add(3, 4)    # 7
calc.add(1.5, 2)  # 3.5
```

---

#### `Calculator.subtract`

```python
def subtract(self, a: int | float, b: int | float) -> int | float
```

Return `a - b`.

| Parameter | Type | Description |
|---|---|---|
| `a` | `int \| float` | First operand |
| `b` | `int \| float` | Second operand |

**Returns:** `a - b`

---

#### `Calculator.multiply`

```python
def multiply(self, a: int | float, b: int | float) -> int | float
```

Return the product of `a` and `b`.

| Parameter | Type | Description |
|---|---|---|
| `a` | `int \| float` | First operand |
| `b` | `int \| float` | Second operand |

**Returns:** `a * b`

---

#### `Calculator.divide`

```python
def divide(self, a: int | float, b: int | float) -> float
```

Return `a / b`.

| Parameter | Type | Description |
|---|---|---|
| `a` | `int \| float` | Dividend |
| `b` | `int \| float` | Divisor |

**Returns:** `float` quotient.

**Raises:**
- `ZeroDivisionError` — if `b` is zero.

---

#### `Calculator.factorial`

```python
def factorial(self, n: int) -> int
```

Compute `n!`.

| Parameter | Type | Description |
|---|---|---|
| `n` | `int` or integer-valued `float` | Non-negative integer |

**Returns:** `n!` as `int`. Returns `1` for `n = 0`.

**Raises:**
- `TypeError` — if `n` is a `bool`, a non-integer `float`, or any other non-numeric type.
- `ValueError` — if `n < 0`.

**Example:**
```python
calc.factorial(5)    # 120
calc.factorial(5.0)  # 120  (float with integer value is accepted)
```

---

#### `Calculator.square`

```python
def square(self, x: int | float) -> int | float
```

Return `x * x`.

| Parameter | Type | Description |
|---|---|---|
| `x` | `int \| float` | Operand (not `bool`) |

**Returns:** `x**2`. Returns `int` when `x` is `int`, `float` when `x` is `float`.

**Raises:**
- `TypeError` — if `x` is `bool`, `None`, or non-numeric.

---

#### `Calculator.cube`

```python
def cube(self, x: int | float) -> int | float
```

Return `x * x * x`.

Same parameter, return, and exception rules as `square`.

---

#### `Calculator.square_root`

```python
def square_root(self, x: int | float) -> float
```

Compute the square root of `x`.

| Parameter | Type | Description |
|---|---|---|
| `x` | `int \| float` | Non-negative operand (not `bool`) |

**Returns:** `math.sqrt(x)` as `float`.

**Raises:**
- `TypeError` — if `x` is `bool`, `None`, or non-numeric.
- `ValueError` — if `x < 0`.

---

#### `Calculator.cube_root`

```python
def cube_root(self, x: int | float) -> float
```

Compute the real cube root of `x`. Negative inputs are supported.

| Parameter | Type | Description |
|---|---|---|
| `x` | `int \| float` | Operand (not `bool`) |

**Returns:** `float`, preserving the sign of `x`.

**Raises:**
- `TypeError` — if `x` is `bool`, `None`, or non-numeric.

**Example:**
```python
calc.cube_root(-8)  # -2.0
```

---

#### `Calculator.power`

```python
def power(self, base: int | float, exponent: int | float) -> float
```

Raise `base` to the power of `exponent`.

| Parameter | Type | Description |
|---|---|---|
| `base` | `int \| float` | Base (not `bool`) |
| `exponent` | `int \| float` | Exponent (not `bool`) |

**Returns:** `float(base ** exponent)`.

**Raises:**
- `TypeError` — if either argument is `bool`, `None`, or non-numeric.

---

#### `Calculator.log10`

```python
def log10(self, x: int | float) -> float
```

Compute the base-10 logarithm of `x`.

| Parameter | Type | Description |
|---|---|---|
| `x` | `int \| float` | Strictly positive operand (not `bool`) |

**Returns:** `math.log10(x)` as `float`.

**Raises:**
- `TypeError` — if `x` is `bool`, `None`, or non-numeric.
- `ValueError` — if `x <= 0`.

---

#### `Calculator.natural_log`

```python
def natural_log(self, x: int | float) -> float
```

Compute the natural logarithm (base `e`) of `x`.

| Parameter | Type | Description |
|---|---|---|
| `x` | `int \| float` | Strictly positive operand (not `bool`) |

**Returns:** `math.log(x)` as `float`.

**Raises:**
- `TypeError` — if `x` is `bool`, `None`, or non-numeric.
- `ValueError` — if `x <= 0`.

---

#### `Calculator.get_history`

```python
def get_history(self) -> list[OperationRecord]
```

Return a copy of all recorded operation history entries.

**Returns:** List of `OperationRecord` instances in insertion order. Mutations to the returned list do not affect the internal state.

---

#### `Calculator.clear_history`

```python
def clear_history(self) -> None
```

Remove all entries from the operation history.

---

## `src.logic.core` — Arithmetic Engine

Import: `from src.logic.core import ArithmeticEngine`

### `ArithmeticEngine`

```python
class ArithmeticEngine
```

Stateless arithmetic operation provider. Performs computations and validates inputs; never stores state. All `Calculator` methods delegate to an instance of this class.

The method signatures, parameters, return types, and exceptions are identical to the corresponding `Calculator` methods, with the difference that no history recording occurs. Refer to the `Calculator` documentation above for the complete per-method contract.

**Methods:** `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log10`, `natural_log`.

---

## `src.operations` — Operation Abstractions

Import: `from src.operations import Operation, OperationRegistry`

### `Operation`

```python
class Operation(abc.ABC)
```

Abstract base class for all calculator operations.

#### Abstract methods

**`Operation.name`**

```python
@abstractmethod
def name(self) -> str
```

Return the canonical string name of this operation (e.g. `"add"`).

**`Operation.execute`**

```python
@abstractmethod
def execute(self, *args: int | float) -> float
```

Perform the computation. The number of `args` must match `operand_count()`.

**`Operation.operand_count`**

```python
@abstractmethod
def operand_count(self) -> int
```

Return the number of operands required (`1` for unary, `2` for binary).

---

### `OperationRegistry`

```python
class OperationRegistry
```

Maps operation name strings to `Operation` instances.

#### `OperationRegistry.register`

```python
def register(self, operation_name: str, op: Operation) -> None
```

Register `op` under `operation_name`. Overwrites any existing entry with the same name.

#### `OperationRegistry.get`

```python
def get(self, operation_name: str) -> Optional[Operation]
```

Return the `Operation` for `operation_name`, or `None` if not registered.

#### `OperationRegistry.list_operations`

```python
def list_operations(self) -> list[str]
```

Return all registered operation names in insertion order.

#### `OperationRegistry.is_registered`

```python
def is_registered(self, operation_name: str) -> bool
```

Return `True` if `operation_name` has been registered, `False` otherwise.

---

### `register_basic_operations`

```python
def register_basic_operations(registry: OperationRegistry) -> None
```

Register the 12 built-in arithmetic operations with `registry`.

Registered names: `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log10`, `natural_log`.

---

### `register_scientific_operations`

```python
def register_scientific_operations(registry: OperationRegistry) -> None
```

Register scientific operations with `registry`. Currently a no-op — this is the designated extension point for future trigonometric and advanced math operations.

---

## `src.history` — Operation History

Import: `from src.history import OperationRecord, OperationHistory`

### `OperationRecord`

```python
@dataclass
class OperationRecord
```

Immutable record of a single calculator operation.

| Attribute | Type | Description |
|---|---|---|
| `operation_name` | `str` | Name of the operation (e.g. `"add"`) |
| `operands` | `list` | Input values in order |
| `result` | `object` | Computed result |
| `timestamp` | `datetime` | Time of recording |

---

### `OperationHistory`

```python
class OperationHistory
```

Append-only log of `OperationRecord` entries.

#### `OperationHistory.add_record`

```python
def add_record(
    self,
    operation_name: str,
    operands: list,
    result: object,
    timestamp: datetime,
) -> None
```

Append a new record to the log.

#### `OperationHistory.get_history`

```python
def get_history(self) -> list[OperationRecord]
```

Return a shallow copy of all records in insertion order.

#### `OperationHistory.clear_history`

```python
def clear_history(self) -> None
```

Remove all records from the log.

#### `OperationHistory.__len__`

```python
def __len__(self) -> int
```

Return the number of records currently stored.

---

## `src.presentation.cli` — CLI Presentation

Import: `from src.presentation.cli import parse_and_evaluate, run_cli`

### `parse_and_evaluate`

```python
def parse_and_evaluate(expression: str, calc: Calculator) -> int | float
```

Parse and evaluate an infix arithmetic expression string using `ast.parse`.

| Parameter | Type | Description |
|---|---|---|
| `expression` | `str` | Infix arithmetic expression, e.g. `"5 + 3 * 2"` |
| `calc` | `Calculator` | Calculator instance used for each arithmetic step |

**Returns:** Numeric result (`int` or `float`).

**Raises:**
- `ValueError` — empty expression, syntax error, or unsupported operator/node.
- `ZeroDivisionError` — division by zero in the expression.
- `TypeError` — operand type mismatch.

**Supported operators:** `+`, `-` (binary and unary), `*`, `/`, `**`

**Example:**
```python
from src.logic import Calculator
from src.presentation.cli import parse_and_evaluate

calc = Calculator()
parse_and_evaluate("2 ** 10", calc)   # 1024
parse_and_evaluate("(3 + 4) * 2", calc)  # 14
```

---

### `run_cli`

```python
def run_cli(args: list[str]) -> int
```

Join `args` into an expression string, evaluate it, and print the result to stdout.

| Parameter | Type | Description |
|---|---|---|
| `args` | `list[str]` | Tokens from `sys.argv[1:]` |

**Returns:** `0` on success, `1` on any error.

Errors are printed to `stderr`.

---

## `src.presentation.interactive` — Interactive Presentation

Import: `from src.presentation.interactive import run_interactive`

### `parse_number`

```python
def parse_number(input_str: str) -> int | float
```

Convert a string to an `int` (tries first) or `float`.

| Parameter | Type | Description |
|---|---|---|
| `input_str` | `str` | Raw user input |

**Returns:** Parsed numeric value.

**Raises:**
- `InvalidInputError` — if the string cannot be parsed as a number.

---

### `get_operands`

```python
def get_operands(operation: str) -> list[int | float]
```

Prompt the user for all operands required by `operation`, with per-operand retry.

| Parameter | Type | Description |
|---|---|---|
| `operation` | `str` | Key in the `OPERATIONS` dict |

**Returns:** List of parsed numeric operands.

**Raises:**
- `OperandRetryExceeded` — if the user exhausts `MAX_RETRIES` attempts on any single operand.

---

### `execute_operation`

```python
def execute_operation(calc: Calculator, operation: str, operands: list) -> object
```

Dispatch to the `Calculator` method corresponding to `operation`.

| Parameter | Type | Description |
|---|---|---|
| `calc` | `Calculator` | Active calculator instance |
| `operation` | `str` | Key in `OPERATIONS` |
| `operands` | `list` | Numeric operands to pass |

**Returns:** Numeric result, or a human-readable error string if an exception is caught.

---

### `format_result`

```python
def format_result(result: object) -> str
```

Convert a calculation result to a display string. Currently `str(result)`.

---

### `run_interactive`

```python
def run_interactive() -> None
```

Run the interactive calculator REPL. Blocks until the user types `quit` or `exit`, or until the retry limit is reached for operation selection.

---

### `OPERATIONS` constant

```python
OPERATIONS: dict[str, tuple[str, int]]
```

Maps each supported operation name to a `(Calculator_method_name, operand_count)` tuple.

```python
{
    "add":         ("add", 2),
    "subtract":    ("subtract", 2),
    "multiply":    ("multiply", 2),
    "divide":      ("divide", 2),
    "factorial":   ("factorial", 1),
    "square":      ("square", 1),
    "cube":        ("cube", 1),
    "square_root": ("square_root", 1),
    "cube_root":   ("cube_root", 1),
    "power":       ("power", 2),
    "log10":       ("log10", 1),
    "natural_log": ("natural_log", 1),
}
```

---

### `InvalidInputError`

```python
class InvalidInputError(Exception)
```

Raised by `parse_number` when user input cannot be parsed as a number.

---

### `OperandRetryExceeded`

```python
class OperandRetryExceeded(Exception)
```

Raised by `get_operands` when the user fails to supply a valid operand within `MAX_RETRIES` attempts.

---

## `src.input_retry` — Generic Retry Utility

Import: `from src.input_retry import validate_with_retry, InputRetryConfig, RetryLimitExceeded`

### `InputRetryConfig`

```python
@dataclass
class InputRetryConfig
```

Configuration for `validate_with_retry`.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `max_attempts` | `int` | `3` | Maximum input attempts including the first |

---

### `validate_with_retry`

```python
def validate_with_retry(
    input_fn: Callable[[], T],
    validator: Callable[[T], bool],
    error_formatter: Callable[[T, int, int], str],
    config: InputRetryConfig | None = None,
) -> T
```

Repeatedly call `input_fn` until `validator` accepts the value or attempts are exhausted.

| Parameter | Type | Description |
|---|---|---|
| `input_fn` | `Callable[[], T]` | Zero-argument callable that fetches one input value |
| `validator` | `Callable[[T], bool]` | Returns `True` if the value is acceptable; exceptions are treated as `False` |
| `error_formatter` | `Callable[[T, int, int], str]` | `(value, attempt, max_attempts) -> str` — formats the error message printed on failure |
| `config` | `InputRetryConfig \| None` | Retry configuration; defaults to `InputRetryConfig()` |

**Returns:** The first value accepted by `validator`.

**Raises:**
- `RetryLimitExceeded` — when all attempts are exhausted.

---

### `RetryLimitExceeded`

```python
class RetryLimitExceeded(Exception)
```

Raised by `validate_with_retry` when `config.max_attempts` is exhausted without a valid value.

---

## `src.logging_config` — Logging Setup

Import: `from src.logging_config import setup_logging, logger`

### `setup_logging`

```python
def setup_logging(log_file: str = "calculator.log") -> logging.Logger
```

Configure and return the `"calculator"` logger. Safe to call multiple times (idempotent).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `log_file` | `str` | `"calculator.log"` | Path to the log file (relative to cwd) |

**Returns:** The configured `logging.Logger` instance.

Default level: `ERROR`. Format: `<timestamp> <level> <message>`.

### Module-level `logger`

```python
logger: logging.Logger
```

Pre-configured `logging.Logger` named `"calculator"`. Import directly for convenience:

```python
from src.logging_config import logger
logger.error("Something went wrong")
```
