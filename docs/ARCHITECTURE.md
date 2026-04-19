# Architecture

## Table of Contents

- [System Overview](#system-overview)
- [Module Breakdown](#module-breakdown)
  - [Entry Point](#entry-point)
  - [Logic Layer](#logic-layer-srclogic)
  - [Operations Subsystem](#operations-subsystem-srcoperations)
  - [Presentation Layer](#presentation-layer-srcpresentation)
  - [Support Modules](#support-modules)
- [Data Flow](#data-flow)
- [Control Flow — CLI Mode](#control-flow--cli-mode)
- [Control Flow — Interactive Mode](#control-flow--interactive-mode)
- [Design Patterns](#design-patterns)
- [Extension Points](#extension-points)
- [Modularization Rationale](#modularization-rationale)
- [Backward-Compatibility Shims](#backward-compatibility-shims)

---

## System Overview

```
src/
├── __main__.py              Entry point — dispatches CLI vs interactive
├── __init__.py              Top-level re-exports (Calculator, OperationHistory, ...)
├── calculator.py            Shim — re-exports Calculator from src.logic.state
├── cli.py                   Shim — re-exports run_cli from src.presentation.cli
├── user_input.py            Shim — re-exports interactive symbols from src.presentation.interactive
├── input_retry.py           Generic input-retry utility (no I/O)
├── logging_config.py        Centralised logging setup
├── history.py               OperationRecord dataclass + OperationHistory container
├── logic/
│   ├── __init__.py          Exports Calculator
│   ├── state.py             Calculator — stateful facade (history + engine)
│   └── core.py              ArithmeticEngine — pure, stateless arithmetic
├── operations/
│   ├── __init__.py          Exports Operation, OperationRegistry, register_*
│   ├── base.py              Operation ABC + OperationRegistry
│   ├── basic.py             12 concrete operation classes + register_basic_operations
│   └── scientific.py        Placeholder for future scientific operations
└── presentation/
    ├── __init__.py
    ├── cli.py               AST-based expression parser + run_cli
    └── interactive.py       Menu-driven loop + operand collection
```

Import direction is strictly downward:

```
presentation  →  logic  →  operations
                         →  history
              →  input_retry
              →  logging_config
```

No module in `logic/` or `operations/` ever imports from `presentation/`.

---

## Module Breakdown

### Entry Point

**`src/__main__.py`**

Called by `python -m src`. Calls `setup_logging()` then inspects `sys.argv`:

- If arguments are present, calls `run_cli(sys.argv[1:])` and exits with the returned code.
- Otherwise, calls `run_interactive()` which blocks until the user quits.

### Logic Layer (`src/logic/`)

#### `src/logic/core.py` — `ArithmeticEngine`

A **stateless** class. Every method takes numeric operands, validates types, performs the computation using Python builtins or `math`, and returns the result. It never records history and never performs I/O.

Validated operations: `add`, `subtract`, `multiply`, `divide`, `factorial`, `square`, `cube`, `square_root`, `cube_root`, `power`, `log10`, `natural_log`.

Key validation rules:
- `bool` operands are rejected with `TypeError` for all operations that do not accept them.
- `float` values that represent exact integers are accepted by `factorial`.
- Negative values raise `ValueError` for `factorial` and `square_root`.
- Zero or negative values raise `ValueError` for `log10` and `natural_log`.
- Division by zero raises `ZeroDivisionError` (Python's native exception from `/`).

#### `src/logic/state.py` — `Calculator`

A **stateful** facade. Owns an `ArithmeticEngine` and an `OperationHistory`. Each public method:

1. Delegates the computation to `self._engine`.
2. Records the result via `self._history.add_record(...)`.
3. Returns the result to the caller.

`Calculator.__init__` also creates an `OperationRegistry` and registers all basic and scientific operations via the two registration functions. The registry is available on the instance as `self._registry` but is not exposed through the public API — it exists to support future programmatic operation dispatch.

### Operations Subsystem (`src/operations/`)

#### `src/operations/base.py`

Defines two classes:

- **`Operation`** — abstract base class with three abstract methods: `name() -> str`, `execute(*args) -> float`, `operand_count() -> int`.
- **`OperationRegistry`** — a `dict`-backed registry. Operations are stored by name string. Public API: `register`, `get`, `list_operations`, `is_registered`.

#### `src/operations/basic.py`

Contains 12 concrete `Operation` subclasses (one per operation). Each delegates to a module-level singleton `_engine = ArithmeticEngine()`. The function `register_basic_operations(registry)` registers all 12.

The 12 operations: `Add`, `Subtract`, `Multiply`, `Divide`, `Factorial`, `Square`, `Cube`, `SquareRoot`, `CubeRoot`, `Power`, `Log10`, `NaturalLog`.

#### `src/operations/scientific.py`

Contains only `register_scientific_operations(registry)`, which is currently a no-op. This is the designated extension point for trigonometric, hyperbolic, and other scientific operations.

### Presentation Layer (`src/presentation/`)

#### `src/presentation/cli.py`

Parses free-form infix expressions using `ast.parse(..., mode="eval")` and walks the resulting AST with `_eval_node`. Supported AST node types:

- `ast.Constant` — numeric literals (int, float; bool rejected)
- `ast.UnaryOp` — unary minus/plus
- `ast.BinOp` — `+`, `-`, `*`, `/`, `**`

All arithmetic is performed by calling the appropriate `Calculator` method, so every step is recorded in history.

Public functions: `parse_and_evaluate(expression, calc)`, `run_cli(args)`.

#### `src/presentation/interactive.py`

Implements the menu-driven REPL. Key symbols:

- `OPERATIONS` dict — maps operation name strings to `(method_name, operand_count)` tuples.
- `parse_number(input_str)` — converts a string to int or float.
- `get_operands(operation)` — prompts for each required operand with retry logic.
- `execute_operation(calc, operation, operands)` — dispatches to the `Calculator` method by name using `getattr`, catches and formats exceptions.
- `run_interactive()` — the main loop.

Invalid operation selections and invalid operand inputs are each retried up to `MAX_RETRIES` (3) times before the session either loops or exits.

### Support Modules

#### `src/history.py`

- **`OperationRecord`** — a frozen dataclass capturing `operation_name`, `operands`, `result`, `timestamp`.
- **`OperationHistory`** — an append-only list of `OperationRecord` objects. Exposes `add_record`, `get_history` (returns a copy), `clear_history`, and `__len__`.

#### `src/logging_config.py`

Configures a file handler on the `"calculator"` logger writing to `calculator.log`. Default level: `ERROR`. Safe to call multiple times (idempotent — checks `_logger.handlers`). Exports a module-level `logger` for direct import.

#### `src/input_retry.py`

Framework-agnostic retry helper. `validate_with_retry(input_fn, validator, error_formatter, config)` repeatedly calls `input_fn` until `validator` returns `True` or `InputRetryConfig.max_attempts` is exhausted, at which point `RetryLimitExceeded` is raised. No I/O is performed by this module itself.

---

## Data Flow

```
User input (string)
        |
        v
  [Presentation layer]
  parse / validate / dispatch
        |
        v
  [Calculator.method(a, b)]         <- src.logic.state
        |
        +----> [ArithmeticEngine.method(a, b)]   <- src.logic.core
        |             |
        |             v
        |         numeric result
        |
        +----> [OperationHistory.add_record(...)]  <- src.history
        |
        v
  numeric result returned to presentation
        |
        v
  Output to stdout
```

---

## Control Flow — CLI Mode

1. `__main__.main()` detects `sys.argv` has arguments.
2. Calls `run_cli(sys.argv[1:])`.
3. `run_cli` joins args into an expression string, creates a `Calculator`, calls `parse_and_evaluate`.
4. `parse_and_evaluate` calls `ast.parse` then walks the tree via `_eval_node`.
5. Each AST binary/unary node dispatches to the corresponding `Calculator` method.
6. The final result is printed to stdout; exit code 0.
7. Any caught exception prints to stderr; exit code 1.

## Control Flow — Interactive Mode

1. `__main__.main()` detects no arguments; calls `run_interactive()`.
2. Operation list is printed. Main loop begins.
3. User enters an operation name; loop retries up to `MAX_RETRIES` for invalid input.
4. `get_operands` prompts for each operand, retrying per-operand up to `MAX_RETRIES`.
5. `execute_operation` calls the `Calculator` method by name and returns the result or an error string.
6. Result is printed. Loop continues until `quit`/`exit` or retry limit reached.

---

## Design Patterns

### Registry Pattern

`OperationRegistry` provides a named-operation lookup table. New operations can be added at runtime by calling `registry.register(name, operation_instance)`. The `Calculator` creates and populates its own registry on construction.

### Separation of Concerns

Each layer has a single axis of responsibility:
- `ArithmeticEngine` — knows only how to compute.
- `OperationHistory` — knows only how to store records.
- `Calculator` — knows how to coordinate compute + store.
- `OperationRegistry` — knows how to map names to operation objects.
- Presentation — knows how to obtain input and display output.

### Facade Pattern

`Calculator` is a facade: it presents a clean, high-level API that hides the delegation to `ArithmeticEngine` and `OperationHistory`. Callers do not need to know about the two-layer implementation.

### Template Method (via ABC)

`Operation` defines the interface contract (`name`, `execute`, `operand_count`) via abstract methods. Each concrete subclass fills in the specifics without changing the calling convention used by `OperationRegistry` consumers.

---

## Extension Points

### Adding a New Operation

1. Create a subclass of `Operation` in `src/operations/basic.py` (or a new file).
2. Implement `name()`, `operand_count()`, and `execute()`.
3. Add the corresponding arithmetic logic to `ArithmeticEngine` in `src/logic/core.py`.
4. Add the corresponding method to `Calculator` in `src/logic/state.py`.
5. Register the new operation inside `register_basic_operations` (or a new registration function).
6. Add the operation name and operand count to `OPERATIONS` in `src/presentation/interactive.py`.

See [EXTENDING.md](EXTENDING.md) for a step-by-step walkthrough.

### Adding Scientific Operations

`src/operations/scientific.py` contains `register_scientific_operations(registry)` which is currently a no-op. Add new `Operation` subclasses there and register them in that function.

### Adding a New Presentation Mode

Create a new module under `src/presentation/`. Import `Calculator` from `src.logic` and drive it through its public API. Register the new mode in `src/__main__.py`.

---

## Modularization Rationale

The original codebase was a single module (`src/calculator.py`, `src/cli.py`, `src/user_input.py`). Modularization introduced in the current iteration separates pure arithmetic from state management, and input handling from output rendering. The goals were:

- **Testability**: `ArithmeticEngine` can be unit-tested without constructing a full `Calculator`.
- **Replaceability**: `OperationHistory` can be swapped (e.g. for a database-backed implementation) without touching arithmetic logic.
- **Extensibility**: New operations are added as classes, not as modifications to an existing monolith.
- **Research use**: The self-evolution experiments target isolated modules, reducing the blast radius of any generated patch.

Backward-compatibility shims (`src/calculator.py`, `src/cli.py`, `src/user_input.py`) ensure that pre-modularization imports continue to work, which is important for experiment reproducibility.
