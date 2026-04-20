# Extending the Calculator

This guide explains how to add new operations, register them, and integrate them into the presentation layers. It also covers adding new presentation modes.

## Table of Contents

- [Adding a New Basic Operation](#adding-a-new-basic-operation)
  - [Step 1 — Implement the arithmetic in ArithmeticEngine](#step-1--implement-the-arithmetic-in-arithmeticengine)
  - [Step 2 — Expose it on Calculator](#step-2--expose-it-on-calculator)
  - [Step 3 — Create an Operation subclass](#step-3--create-an-operation-subclass)
  - [Step 4 — Register the operation](#step-4--register-the-operation)
  - [Step 5 — Add to the interactive OPERATIONS map](#step-5--add-to-the-interactive-operations-map)
- [Adding a Scientific Operation](#adding-a-scientific-operation)
- [Adding a New Presentation Mode](#adding-a-new-presentation-mode)
- [Testing New Features](#testing-new-features)

---

## Adding a New Basic Operation

This walkthrough adds a hypothetical `modulo` (remainder) operation as a worked example.

### Step 1 — Implement the arithmetic in `ArithmeticEngine`

File: `src/logic/core.py`

Add a method to the `ArithmeticEngine` class. Follow the existing pattern: validate types, log errors before raising, return the result.

```python
def modulo(self, a: int | float, b: int | float) -> int | float:
    """Return the remainder of a divided by b.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        a % b

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        logger.error(
            f"modulo: division by zero attempted; a={a}, b={b}; ZeroDivisionError"
        )
    return a % b
```

### Step 2 — Expose it on `Calculator`

File: `src/logic/state.py`

Add a method that delegates to the engine and records the result:

```python
def modulo(self, a: int | float, b: int | float) -> int | float:
    """Return the remainder a % b and record the operation.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        a % b

    Raises:
        ZeroDivisionError: If b is zero.
    """
    result = self._engine.modulo(a, b)
    self._history.add_record("modulo", [a, b], result, datetime.now())
    return result
```

### Step 3 — Create an `Operation` subclass

File: `src/operations/basic.py`

Add a concrete `Operation` class. It must implement `name`, `operand_count`, and `execute`:

```python
class Modulo(Operation):
    """Binary modulo (remainder) operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"modulo"``
        """
        return "modulo"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Return the remainder of args[0] divided by args[1].

        Args:
            *args: Exactly two numeric operands.

        Returns:
            args[0] % args[1]

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """
        return _engine.modulo(args[0], args[1])
```

### Step 4 — Register the operation

Still in `src/operations/basic.py`, add the new class to `register_basic_operations`:

```python
def register_basic_operations(registry: OperationRegistry) -> None:
    # ... existing registrations ...
    registry.register("modulo", Modulo())
```

### Step 5 — Add to the interactive `OPERATIONS` map

File: `src/presentation/interactive.py`

Add an entry to the `OPERATIONS` dict. The key is the user-facing name, the value is `(Calculator_method_name, operand_count)`:

```python
OPERATIONS: dict[str, tuple[str, int]] = {
    # ... existing entries ...
    "modulo": ("modulo", 2),
}
```

The operation is now available in interactive mode. Because the CLI parser works from AST nodes rather than named operations, it requires a separate change to support `%` as a CLI operator — see `_eval_node` in `src/presentation/cli.py`.

---

## Adding a Scientific Operation

Scientific operations follow exactly the same steps as basic operations, but the `Operation` subclass and its registration go in `src/operations/scientific.py`.

Example: adding `sin(x)`:

1. Add `sin` to `ArithmeticEngine` in `src/logic/core.py` (using `math.sin`).
2. Add `sin` to `Calculator` in `src/logic/state.py`.
3. Create a `Sin(Operation)` class in `src/operations/scientific.py`.
4. Register it inside `register_scientific_operations` in the same file:

```python
def register_scientific_operations(registry: OperationRegistry) -> None:
    registry.register("sin", Sin())
```

5. Add `"sin": ("sin", 1)` to `OPERATIONS` in `src/presentation/interactive.py`.

---

## Adding a New Presentation Mode

To add a third presentation mode (for example, a JSON API adapter or a GUI backend):

1. Create a new module under `src/presentation/`, e.g. `src/presentation/json_api.py`.

2. Import `Calculator` from `src.logic`:

```python
from src.logic import Calculator
```

3. Implement your mode. Use `Calculator` through its public API. Do not import from `src.logic.core` or `src.history` unless you need them directly.

4. Wire it into `src/__main__.py`. The entry point inspects `sys.argv` to decide which mode to run. Add your detection logic there:

```python
def main() -> None:
    setup_logging()
    if "--json" in sys.argv:
        from src.presentation.json_api import run_json_api
        run_json_api()
    elif len(sys.argv) > 1:
        exit_code = run_cli(sys.argv[1:])
        sys.exit(exit_code)
    else:
        run_interactive()
```

---

## Testing New Features

Testing is the responsibility of the `pytest-edge-tester` agent / testing team and is out of scope for this guide. When you submit a new operation, document in your report:

- The new `Calculator` method signature.
- Valid input ranges and expected results for representative cases.
- Edge cases: zero, negative values, non-integer floats, `bool` inputs, `None`.
- Expected exceptions and the conditions that trigger them.

This information allows the tester to write targeted tests without re-reading the implementation.
