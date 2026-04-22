# Operations Reference

This document covers all built-in calculator operations and the mechanism for
registering new ones at runtime.

## Built-in operations

### add

| Property | Value |
|---|---|
| Key | `add` |
| Symbol | `+` |
| Definition | a + b |
| Arity | 2 |
| Operand constraints | Any real numbers |

**Interactive mode:**

```
Select an operation: add
Enter first operand: 3
Enter second operand: 5
Result of Addition (a + b)(3.0, 5.0) = 8.0
```

**CLI mode:**

```bash
python -m src add 3 5
# 8
```

**Error conditions:** None (overflow is not checked; Python integers are
arbitrary-precision and floats follow IEEE 754).

---

### subtract

| Property | Value |
|---|---|
| Key | `subtract` |
| Symbol | `-` |
| Definition | a - b |
| Arity | 2 |
| Operand constraints | Any real numbers |

**Interactive mode:**

```
Select an operation: subtract
Enter first operand: 10
Enter second operand: 4
Result of Subtraction (a - b)(10.0, 4.0) = 6.0
```

**CLI mode:**

```bash
python -m src subtract 10 4
# 6
```

**Error conditions:** None.

---

### multiply

| Property | Value |
|---|---|
| Key | `multiply` |
| Symbol | `*` |
| Definition | a * b |
| Arity | 2 |
| Operand constraints | Any real numbers |

**Interactive mode:**

```
Select an operation: multiply
Enter first operand: 7
Enter second operand: 6
Result of Multiplication (a * b)(7.0, 6.0) = 42.0
```

**CLI mode:**

```bash
python -m src multiply 7 6
# 42
```

**Error conditions:** None.

---

### divide

| Property | Value |
|---|---|
| Key | `divide` |
| Symbol | `/` |
| Definition | a / b |
| Arity | 2 |
| Operand constraints | Any real numbers; `b` must not be zero |

**Interactive mode:**

```
Select an operation: divide
Enter first operand: 9
Enter second operand: 3
Result of Division (a / b)(9.0, 3.0) = 3.0
```

**CLI mode:**

```bash
python -m src divide 9 3
# 3
```

**Error conditions:**

- `ZeroDivisionError` — raised (and logged) when `b` is zero. In interactive
  mode the error is displayed and the user is re-prompted; in CLI mode the
  process exits with code 1.

---

### power

| Property | Value |
|---|---|
| Key | `power` |
| Symbol | `^` |
| Definition | x ^ y |
| Arity | 2 |
| Operand constraints | Any real `x`, any real `y`; `x = 0` with `y < 0` is undefined |

**Interactive mode:**

```
Select an operation: power
Enter first operand: 2
Enter second operand: 10
Result of Power (x ^ y)(2.0, 10.0) = 1024.0
```

**CLI mode:**

```bash
python -m src power 2 10
# 1024
```

**Error conditions:**

- `ValueError` — raised (and logged) when `x` is `0` and `y` is negative
  (`0 raised to a negative power is undefined`).

---

### factorial

| Property | Value |
|---|---|
| Key | `factorial` |
| Symbol | `n!` |
| Definition | n! = n * (n-1) * ... * 1, with 0! = 1 |
| Arity | 1 |
| Operand constraints | Non-negative integer (`n >= 0`). Floats and negative values are rejected. |

**Interactive mode:**

```
Select an operation: factorial
Enter value: 7
Result of Factorial (n!)(7) = 5040
```

**CLI mode:**

```bash
python -m src factorial 7
# 5040
```

**Error conditions:**

- `ValueError` — raised (and logged) when `n` is negative or not an integer
  (`Factorial is only defined for non-negative integers`).

---

### square

| Property | Value |
|---|---|
| Key | `square` |
| Symbol | `x^2` |
| Definition | x * x |
| Arity | 1 |
| Operand constraints | Any real number |

**Interactive mode:**

```
Select an operation: square
Enter value: 9
Result of Square (x^2)(9.0) = 81.0
```

**CLI mode:**

```bash
python -m src square 9
# 81
```

**Error conditions:** None.

---

### cube

| Property | Value |
|---|---|
| Key | `cube` |
| Symbol | `x^3` |
| Definition | x * x * x |
| Arity | 1 |
| Operand constraints | Any real number |

**Interactive mode:**

```
Select an operation: cube
Enter value: 3
Result of Cube (x^3)(3.0) = 27.0
```

**CLI mode:**

```bash
python -m src cube 3
# 27
```

**Error conditions:** None.

---

### square_root

| Property | Value |
|---|---|
| Key | `square_root` |
| Symbol | `√x` |
| Definition | Principal (non-negative) square root of x |
| Arity | 1 |
| Operand constraints | Non-negative real number (`x >= 0`) |

**Interactive mode:**

```
Select an operation: square_root
Enter value: 144
Result of Square root (√x)(144.0) = 12.0
```

**CLI mode:**

```bash
python -m src square_root 144
# 12
```

**Error conditions:**

- `ValueError` — raised (and logged) when `x` is negative
  (`Square root is not defined for negative numbers`).

---

### cube_root

| Property | Value |
|---|---|
| Key | `cube_root` |
| Symbol | `∛x` |
| Definition | Real cube root of x, sign-preserving: cube_root(-8) = -2 |
| Arity | 1 |
| Operand constraints | Any real number (including negative values) |

**Interactive mode:**

```
Select an operation: cube_root
Enter value: 27
Result of Cube root (∛x)(27.0) = 3.0
```

**CLI mode:**

```bash
python -m src cube_root 27
# 3
```

**Error conditions:** None. Unlike Python's `x ** (1/3)`, this operation
correctly handles negative inputs without producing a complex number.

---

### log

| Property | Value |
|---|---|
| Key | `log` |
| Symbol | `log₁₀` |
| Definition | Base-10 logarithm of x |
| Arity | 1 |
| Operand constraints | Strictly positive real number (`x > 0`) |

**Interactive mode:**

```
Select an operation: log
Enter value: 1000
Result of Base-10 logarithm (log₁₀ x)(1000.0) = 3.0
```

**CLI mode:**

```bash
python -m src log 1000
# 3.0
```

**Error conditions:**

- `ValueError` — raised (and logged) when `x <= 0`
  (`Logarithm is only defined for positive numbers`).

---

### ln

| Property | Value |
|---|---|
| Key | `ln` |
| Symbol | `ln` |
| Definition | Natural logarithm of x (base e) |
| Arity | 1 |
| Operand constraints | Strictly positive real number (`x > 0`) |

**Interactive mode:**

```
Select an operation: ln
Enter value: 1
Result of Natural logarithm (ln x)(1.0) = 0.0
```

**CLI mode:**

```bash
python -m src ln 1
# 0.0
```

**Error conditions:**

- `ValueError` — raised (and logged) when `x <= 0`
  (`Natural logarithm is only defined for positive numbers`).

---

## Extending the registry

The `OperationRegistry` exposes a `register_operation()` method that lets you
add operations at runtime without modifying any source file or subclassing
`Calculator`.  The new operation is immediately available to
`CalculationEngine.execute_operation()`.

```python
import math
from src.operations import OperationRegistry
from src.calculator import Calculator

calc = Calculator()
registry = OperationRegistry(calc)

# Register sine — one operand, expects a value in radians.
registry.register_operation(
    key="sin",
    method=math.sin,
    arity=1,
    description="Sine of x in radians (sin x)",
)
```

**`register_operation()` raises:**

- `ValueError` — if `key` is already registered, or if `arity` is not a
  positive integer.
- `TypeError` — if `method` is not callable.
