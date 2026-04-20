# Operations Reference

The calculator supports 12 operations. They are listed below in the order they
appear in the REPL menu.

---

## Summary Table

| # | Name | Canonical token | Aliases | Arity | Description |
|---|------|----------------|---------|-------|-------------|
| 1 | Addition | `add` | `+` | 2 | a + b |
| 2 | Subtraction | `subtract` | `-` | 2 | a - b |
| 3 | Multiplication | `multiply` | `*` | 2 | a × b |
| 4 | Division | `divide` | `/` | 2 | a / b |
| 5 | Power | `power` | `^` | 2 | base ^ exponent |
| 6 | Logarithm (base) | `logarithm` | `log` | 2 | log_base(x) |
| 7 | Factorial | `factorial` | — | 1 | n! |
| 8 | Square | `square` | — | 1 | x² |
| 9 | Cube | `cube` | — | 1 | x³ |
| 10 | Square Root | `square_root` | `sqrt` | 1 | √x |
| 11 | Cube Root | `cube_root` | `cbrt` | 1 | ∛x |
| 12 | Natural Logarithm | `natural_logarithm` | `ln` | 1 | ln(x) |

---

## Detailed Operation Descriptions

---

### 1. Addition

- **Canonical token:** `add`
- **Aliases:** `+`
- **Arity:** 2 (binary)
- **Description:** Returns the sum of two numbers.
- **Domain:** All real numbers.
- **Examples:**
  ```
  python -m src add 3 4       # 7.0
  python -m src + 3 4         # 7.0
  python -m src add -5 2.5    # -2.5
  ```
- **Error conditions:** None.

---

### 2. Subtraction

- **Canonical token:** `subtract`
- **Aliases:** `-`
- **Arity:** 2 (binary)
- **Description:** Returns the difference of two numbers (a minus b).
- **Domain:** All real numbers.
- **Examples:**
  ```
  python -m src subtract 10 3     # 7.0
  python -m src - 10 3            # 7.0
  python -m src subtract 2.5 5    # -2.5
  ```
- **Error conditions:** None.

---

### 3. Multiplication

- **Canonical token:** `multiply`
- **Aliases:** `*`
- **Arity:** 2 (binary)
- **Description:** Returns the product of two numbers.
- **Domain:** All real numbers.
- **Examples:**
  ```
  python -m src multiply 3 4      # 12.0
  python -m src * 3 4             # 12.0
  python -m src multiply -2 5     # -10.0
  ```
- **Error conditions:** None.

---

### 4. Division

- **Canonical token:** `divide`
- **Aliases:** `/`
- **Arity:** 2 (binary)
- **Description:** Returns the quotient of two numbers (a divided by b).
- **Domain:** All real numbers; b must not be zero.
- **Examples:**
  ```
  python -m src divide 10 2       # 5.0
  python -m src / 10 2            # 5.0
  python -m src divide 7 2        # 3.5
  ```
- **Error conditions:**
  - `ZeroDivisionError: Cannot divide by zero` — when b is 0.

---

### 5. Power

- **Canonical token:** `power`
- **Aliases:** `^`
- **Arity:** 2 (binary)
- **Description:** Returns the base raised to the given exponent.
- **Domain:** All real numbers (negative exponents and fractional exponents are
  permitted).
- **Examples:**
  ```
  python -m src power 2 10    # 1024.0
  python -m src ^ 2 10        # 1024.0
  python -m src power 4 0.5   # 2.0
  python -m src power 2 -1    # 0.5
  ```
- **Error conditions:** None for real base/exponent combinations; complex
  results (e.g. `(-1) ^ 0.5`) may raise or produce unexpected output depending
  on Python's `**` operator behaviour.

---

### 6. Logarithm (base)

- **Canonical token:** `logarithm`
- **Aliases:** `log`
- **Arity:** 2 (binary)
- **Description:** Returns the logarithm of x in the given base: log_base(x).
  This is computed as `math.log(x, base)`.
- **Note:** This is a two-argument logarithm, unlike `natural_logarithm`. The
  first argument is the value x; the second argument is the base.
- **Domain:**
  - x must be strictly positive (x > 0).
  - base must be positive and not equal to 1 (base > 0, base != 1).
- **Examples:**
  ```
  python -m src logarithm 100 10    # 2.0
  python -m src log 8 2             # 3.0
  python -m src log 1000 10         # 3.0
  ```
- **Error conditions:**
  - `ValueError: logarithm() not defined for non-positive values` — when x <= 0.
  - `ValueError: logarithm base must be positive and not equal to 1` — when
    base <= 0 or base == 1.

---

### 7. Factorial

- **Canonical token:** `factorial`
- **Aliases:** none
- **Arity:** 1 (unary)
- **Description:** Returns n factorial (n!), the product of all positive
  integers from 1 to n.
- **Domain:**
  - n must be a non-negative integer or a float that represents a whole number
    (e.g. 5.0 is accepted; 5.5 is not).
  - n must satisfy n >= 0.
- **Examples:**
  ```
  python -m src factorial 5     # 120
  python -m src factorial 0     # 1
  python -m src factorial 10    # 3628800
  ```
- **Error conditions:**
  - `ValueError: factorial() not defined for negative values` — when n < 0.
  - `TypeError: factorial() only accepts integer values, not non-integer floats`
    — when n is a non-integer float such as 5.5.

---

### 8. Square

- **Canonical token:** `square`
- **Aliases:** none
- **Arity:** 1 (unary)
- **Description:** Returns x raised to the power of 2 (x²).
- **Domain:** All real numbers.
- **Examples:**
  ```
  python -m src square 4      # 16.0
  python -m src square -3     # 9.0
  python -m src square 2.5    # 6.25
  ```
- **Error conditions:** None.

---

### 9. Cube

- **Canonical token:** `cube`
- **Aliases:** none
- **Arity:** 1 (unary)
- **Description:** Returns x raised to the power of 3 (x³).
- **Domain:** All real numbers.
- **Examples:**
  ```
  python -m src cube 3        # 27.0
  python -m src cube -2       # -8.0
  python -m src cube 2.5      # 15.625
  ```
- **Error conditions:** None.

---

### 10. Square Root

- **Canonical token:** `square_root`
- **Aliases:** `sqrt`
- **Arity:** 1 (unary)
- **Description:** Returns the non-negative square root of x (√x).
- **Domain:** x must be non-negative (x >= 0).
- **Examples:**
  ```
  python -m src square_root 9     # 3.0
  python -m src sqrt 2            # 1.4142135623730951
  python -m src sqrt 0            # 0.0
  ```
- **Error conditions:**
  - `ValueError: square_root() not defined for negative values` — when x < 0.

---

### 11. Cube Root

- **Canonical token:** `cube_root`
- **Aliases:** `cbrt`
- **Arity:** 1 (unary)
- **Description:** Returns the real-valued cube root of x (∛x). Handles
  negative inputs correctly by preserving the sign of x.
- **Domain:** All real numbers (including negative values).
- **Examples:**
  ```
  python -m src cube_root 27      # 3.0
  python -m src cbrt -8           # -2.0
  python -m src cbrt 0            # 0.0
  ```
- **Error conditions:** None.

---

### 12. Natural Logarithm

- **Canonical token:** `natural_logarithm`
- **Aliases:** `ln`
- **Arity:** 1 (unary)
- **Description:** Returns the natural logarithm (base e) of x: ln(x).
- **Domain:** x must be strictly positive (x > 0).
- **Examples:**
  ```
  python -m src natural_logarithm 1    # 0.0
  python -m src ln 2.718281828         # ~1.0
  python -m src ln 10                  # 2.302585092994046
  ```
- **Error conditions:**
  - `ValueError: natural_logarithm() not defined for non-positive values` —
    when x <= 0.

---

## Special Case: Two-Argument Logarithm

The `logarithm` / `log` operation is the only two-argument operation in the
logarithm family. It accepts an explicit base so that arbitrary-base logarithms
can be computed:

```
log(x, base) = math.log(x, base)
```

This is distinct from `natural_logarithm` (`ln`), which is always base e and
takes only one argument.

The special-case dispatch for the two-argument logarithm is handled entirely
inside `OperationRegistry.dispatch` (in `src/core/operations.py`), so neither
the CLI nor the REPL needs to implement it independently.
