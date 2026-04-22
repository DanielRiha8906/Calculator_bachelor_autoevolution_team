# Operation Reference

This document lists every operation exposed by the `Calculator` class (`src/core/calculator.py`), including input types, return types, and error conditions.

---

## Basic Arithmetic Operations

All basic arithmetic is implemented as static methods on `NormalOperations` (`src/core/operations/normal.py`) and delegated from `Calculator`.

### `add(a, b) -> float`

Returns the sum of `a` and `b`.

- **Input:** `a`, `b` — any numeric types accepted by Python's `+` operator (int or float).
- **Output:** The sum as a Python numeric value.
- **Errors:** No explicit validation; relies on Python's default arithmetic behaviour.

---

### `subtract(a, b) -> float`

Returns the difference `a - b`.

- **Input:** `a`, `b` — any numeric types accepted by Python's `-` operator (int or float).
- **Output:** The difference as a Python numeric value.
- **Errors:** No explicit validation.

---

### `multiply(a, b) -> float`

Returns the product of `a` and `b`.

- **Input:** `a`, `b` — any numeric types accepted by Python's `*` operator (int or float).
- **Output:** The product as a Python numeric value.
- **Errors:** No explicit validation.

---

### `divide(a, b) -> float`

Returns the quotient `a / b`.

- **Input:** `a`, `b` — any numeric types accepted by Python's `/` operator (int or float).
- **Output:** The quotient as a float.
- **Errors:**
  - `ZeroDivisionError` — raised by Python when `b` is `0`.

---

## Scientific Operations

All scientific operations are implemented as static methods on `ScientificOperations` (`src/core/operations/scientific.py`). Each method validates its inputs before computing.

### `factorial(n) -> int`

Returns `n!` (n factorial).

- **Input:** `n` — must be a plain `int`; `bool` values are rejected.
- **Output:** The factorial as an `int`.
- **Constraints:** `n >= 0`.
- **Errors:**
  - `TypeError` — if `n` is not an `int` or is a `bool`.
  - `ValueError` — if `n < 0`.

---

### `square(x) -> float`

Returns `x` raised to the power of 2 (`x²`).

- **Input:** `x` — must be an `int` or `float`; `bool` values are rejected.
- **Output:** `float(x ** 2)`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.

---

### `cube(x) -> float`

Returns `x` raised to the power of 3 (`x³`).

- **Input:** `x` — must be an `int` or `float`; `bool` values are rejected.
- **Output:** `float(x ** 3)`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.

---

### `square_root(x) -> float`

Returns the square root of `x` (`√x`).

- **Input:** `x` — must be a non-negative `int` or `float`; `bool` values are rejected.
- **Output:** `math.sqrt(x)` as a `float`.
- **Constraints:** `x >= 0`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.
  - `ValueError` — if `x < 0`.

---

### `cube_root(x) -> float`

Returns the real-valued cube root of `x` (`∛x`). Negative inputs are handled correctly by preserving the sign.

- **Input:** `x` — must be an `int` or `float`; `bool` values are rejected.
- **Output:** `math.copysign(abs(x) ** (1/3), x)` as a `float`. For example, `cube_root(-8)` returns `-2.0`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.

---

### `logarithm(x) -> float`

Returns the base-10 logarithm of `x` (`log₁₀(x)`).

- **Input:** `x` — must be a positive `int` or `float`; `bool` values are rejected.
- **Output:** `math.log10(x)` as a `float`.
- **Constraints:** `x > 0`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.
  - `ValueError` — if `x <= 0`.

---

### `natural_logarithm(x) -> float`

Returns the natural logarithm of `x` (`ln(x)`).

- **Input:** `x` — must be a positive `int` or `float`; `bool` values are rejected.
- **Output:** `math.log(x)` as a `float`.
- **Constraints:** `x > 0`.
- **Errors:**
  - `TypeError` — if `x` is not an `int` or `float`, or is a `bool`.
  - `ValueError` — if `x <= 0`.

---

### `power(base, exponent) -> float`

Returns `base` raised to the power of `exponent` (`base ** exponent`).

- **Input:** `base`, `exponent` — each must be an `int` or `float`; `bool` values are rejected.
- **Output:** `float(base ** exponent)`. `0 ** 0` returns `1.0`.
- **Errors:**
  - `TypeError` — if `base` or `exponent` is not an `int` or `float`, or is a `bool`.

---

## Error Behaviour

### Type errors

All scientific operations check their inputs with `isinstance(x, (int, float)) and not isinstance(x, bool)`. If the check fails, a `TypeError` is raised immediately before any computation. `bool` is excluded even though it is a subclass of `int` in Python.

### Value errors

Domain constraints (e.g. negative input to `square_root`, non-positive input to `logarithm`, negative `n` for `factorial`) raise `ValueError` with a descriptive message.

### Division by zero

`divide` raises Python's built-in `ZeroDivisionError` when the denominator is zero.

### What users see vs. what is logged

When an operation raises `ZeroDivisionError` or `ValueError`, `CalculatorSession.execute_operation` catches the exception, logs it silently via `ErrorLogger`, and returns the exception message string as the second element of its return tuple. The CLI then displays the message to the user as `  Error: <message>`. The raw exception is never printed as a traceback.

For `TypeError` and any other unhandled exception, the exception message is similarly returned and displayed, but no category-specific log entry is written (the generic exception branch in `execute_operation` does not call `ErrorLogger`).
