# Operations Reference

All operations are defined in `src/operations/normal.py` (as `NORMAL_OPERATIONS`) and
composed into the unified `OPERATIONS` dict in `src/operations/__init__.py`. The
corresponding computation methods live in `src/core/calculator.py`.

---

## Arithmetic Operations

### add

| Field | Value |
|-------|-------|
| Key | `add` |
| Calculator method | `Calculator.add(a, b)` |
| Arity | 2 |
| Operand type | float |
| Return type | float |
| Label | Add two numbers |

**Behavior:** Returns `a + b`.

**Error conditions:** None specific to this operation.

**Examples:**

```bash
python main.py add 5 7       # 12.0
python main.py add -3 1.5    # -1.5
```

---

### subtract

| Field | Value |
|-------|-------|
| Key | `subtract` |
| Calculator method | `Calculator.subtract(a, b)` |
| Arity | 2 |
| Operand type | float |
| Return type | float |
| Label | Subtract two numbers |

**Behavior:** Returns `a - b`.

**Error conditions:** None specific to this operation.

**Examples:**

```bash
python main.py subtract 10 3    # 7.0
python main.py subtract 0 5     # -5.0
```

---

### multiply

| Field | Value |
|-------|-------|
| Key | `multiply` |
| Calculator method | `Calculator.multiply(a, b)` |
| Arity | 2 |
| Operand type | float |
| Return type | float |
| Label | Multiply two numbers |

**Behavior:** Returns `a * b`.

**Error conditions:** None specific to this operation.

**Examples:**

```bash
python main.py multiply 4 8     # 32.0
python main.py multiply -2 3    # -6.0
```

---

### divide

| Field | Value |
|-------|-------|
| Key | `divide` |
| Calculator method | `Calculator.divide(a, b)` |
| Arity | 2 |
| Operand type | float |
| Return type | float |
| Label | Divide two numbers |

**Behavior:** Returns `a / b`.

**Error conditions:**
- `ZeroDivisionError` when `b == 0`. Displayed to the user as
  `"Error: Division by zero is not allowed."` and logged via `Logger.log_division_by_zero`.

**Examples:**

```bash
python main.py divide 10 4    # 2.5
python main.py divide 7 2     # 3.5
python main.py divide 5 0     # Error: Division by zero is not allowed.  [exit 1]
```

---

## Power and Root Operations

### power

| Field | Value |
|-------|-------|
| Key | `power` |
| Calculator method | `Calculator.power(x, y)` |
| Arity | 2 |
| Operand type | float |
| Return type | float |
| Label | Raise a number to a power |

**Behavior:** Returns `x ** y`.

**Error conditions:** None raised by the method itself. Note that Python's `**`
operator can produce `inf` for very large exponents without raising an exception.

**Examples:**

```bash
python main.py power 2 10     # 1024.0
python main.py power 3 3      # 27.0
python main.py power 5 0      # 1.0
```

---

### square

| Field | Value |
|-------|-------|
| Key | `square` |
| Calculator method | `Calculator.square(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Square a number (x^2) |

**Behavior:** Returns `x ** 2`.

**Error conditions:** None.

**Examples:**

```bash
python main.py square 9     # 81.0
python main.py square -4    # 16.0
```

---

### cube

| Field | Value |
|-------|-------|
| Key | `cube` |
| Calculator method | `Calculator.cube(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Cube a number (x^3) |

**Behavior:** Returns `x ** 3`.

**Error conditions:** None.

**Examples:**

```bash
python main.py cube 3     # 27.0
python main.py cube -2    # -8.0
```

---

### square_root

| Field | Value |
|-------|-------|
| Key | `square_root` |
| Calculator method | `Calculator.square_root(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Square root of a number |

**Behavior:** Returns `math.sqrt(x)`.

**Error conditions:**
- `ValueError` when `x < 0`. Error message:
  `"square_root() is not defined for negative numbers, got <x>"`.
  Logged via `Logger.log_domain_error`.

**Examples:**

```bash
python main.py square_root 16    # 4.0
python main.py square_root 2     # 1.4142135623730951
python main.py square_root -1    # Error: square_root() is not defined...  [exit 1]
```

---

### cube_root

| Field | Value |
|-------|-------|
| Key | `cube_root` |
| Calculator method | `Calculator.cube_root(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Cube root of a number |

**Behavior:** Returns `math.cbrt(x)`. Defined for all real numbers, including
negatives.

**Error conditions:** None.

**Examples:**

```bash
python main.py cube_root 27     # 3.0
python main.py cube_root -8     # -2.0
python main.py cube_root 2      # 1.2599210498948732
```

---

## Logarithmic Operations

### log10

| Field | Value |
|-------|-------|
| Key | `log10` |
| Calculator method | `Calculator.log10(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Base-10 logarithm of a number |

**Behavior:** Returns `math.log10(x)`.

**Error conditions:**
- `ValueError` when `x <= 0`. Error message:
  `"log10() is not defined for x <= 0, got <x>"`.
  Logged via `Logger.log_domain_error`.

**Examples:**

```bash
python main.py log10 1000    # 3.0
python main.py log10 1       # 0.0
python main.py log10 0       # Error: log10() is not defined for x <= 0...  [exit 1]
python main.py log10 -5      # Error: log10() is not defined for x <= 0...  [exit 1]
```

---

### ln

| Field | Value |
|-------|-------|
| Key | `ln` |
| Calculator method | `Calculator.ln(x)` |
| Arity | 1 |
| Operand type | float |
| Return type | float |
| Label | Natural logarithm of a number |

**Behavior:** Returns `math.log(x)` (natural logarithm, base e).

**Error conditions:**
- `ValueError` when `x <= 0`. Error message:
  `"ln() is not defined for x <= 0, got <x>"`.
  Logged via `Logger.log_domain_error`.

**Examples:**

```bash
python main.py ln 1          # 0.0
python main.py ln 2.718      # approximately 0.9999
python main.py ln 0          # Error: ln() is not defined for x <= 0...  [exit 1]
```

---

## Special Operations

### factorial

| Field | Value |
|-------|-------|
| Key | `factorial` |
| Calculator method | `Calculator.factorial(n)` |
| Arity | 1 |
| Operand type | int (coerce field is `int`, not `float`) |
| Return type | int |
| Label | Factorial of a non-negative integer |

**Behavior:** Returns `math.factorial(n)`. Operands are coerced to `int` before the
method is called; passing `"6"` on the CLI yields the integer `720`, not `720.0`.

**Error conditions:**
- `TypeError` when `n` is a boolean: `"factorial() does not accept boolean values, got <n>"`.
- `TypeError` when `n` is not an integer after coercion: `"factorial() only accepts non-negative integers, got '<type>'"`.
- `ValueError` when `n < 0`: `"factorial() is not defined for negative integers, got <n>"`.
- All errors are logged via `Logger.log_domain_error`.

**Examples:**

```bash
python main.py factorial 6      # 720
python main.py factorial 0      # 1
python main.py factorial -1     # Error: factorial() is not defined for negative integers...  [exit 1]
python main.py factorial 3.5    # Error: Invalid operand '3.5': expected a numeric value.  [exit 1]
```

Note: `3.5` fails at the coercion stage (`int("3.5")` raises `ValueError`) before it
reaches `Calculator.factorial`.
