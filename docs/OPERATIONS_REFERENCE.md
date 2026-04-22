# Operations Reference

Complete reference for all operations supported by the Calculator application.

All expressions follow the format:

```
OPERATION OPERAND1 [OPERAND2]
```

Operation names are case-insensitive. Operands must be integers or decimal numbers. Integer tokens are parsed as `int`; tokens containing a decimal point are parsed as `float`.

---

## Basic Operations

These operations require exactly **two operands**.

### `add`

| Property     | Value                          |
|--------------|--------------------------------|
| Signature    | `add A B`                      |
| Operands     | 2                              |
| Returns      | `A + B` (int or float)         |
| Errors       | None                           |

**Examples:**

```
add 5 3        -> 8
add 2.5 1.5    -> 4.0
add -10 10     -> 0
```

---

### `subtract`

| Property     | Value                          |
|--------------|--------------------------------|
| Signature    | `subtract A B`                 |
| Operands     | 2                              |
| Returns      | `A - B` (int or float)         |
| Errors       | None                           |

**Examples:**

```
subtract 10 4       -> 6
subtract 5.5 2.25   -> 3.25
subtract 0 100      -> -100
```

---

### `multiply`

| Property     | Value                          |
|--------------|--------------------------------|
| Signature    | `multiply A B`                 |
| Operands     | 2                              |
| Returns      | `A * B` (int or float)         |
| Errors       | None                           |

**Examples:**

```
multiply 6 7      -> 42
multiply 2.5 4    -> 10.0
multiply -3 -3    -> 9
```

---

### `divide`

| Property     | Value                                              |
|--------------|----------------------------------------------------|
| Signature    | `divide A B`                                       |
| Operands     | 2                                                  |
| Returns      | `A / B` as float                                   |
| Errors       | `ZeroDivisionError` if B is 0                      |

**Examples:**

```
divide 10 4    -> 2.5
divide 9 3     -> 3.0
divide 7 0     -> Math error: division by zero.
```

---

## Advanced Operations

### `factorial`

| Property     | Value                                                              |
|--------------|--------------------------------------------------------------------|
| Signature    | `factorial N`                                                      |
| Operands     | 1                                                                  |
| Returns      | N! as int                                                          |
| Errors       | `TypeError` if N is not an integer; `ValueError` if N is negative  |

Note: The parser coerces whole-number tokens to `int`. Passing `5` works; passing `5.0` raises a `TypeError` because `5.0` is parsed as `float`.

**Examples:**

```
factorial 0     -> 1
factorial 5     -> 120
factorial 10    -> 3628800
factorial -1    -> Type error: factorial() requires a non-negative integer, got int
factorial 5.0   -> Type error: factorial() requires a non-negative integer, got float
```

---

### `square`

| Property     | Value                          |
|--------------|--------------------------------|
| Signature    | `square X`                     |
| Operands     | 1                              |
| Returns      | X * X (int or float)           |
| Errors       | None                           |

**Examples:**

```
square 4      -> 16
square 2.5    -> 6.25
square -3     -> 9
```

---

### `cube`

| Property     | Value                          |
|--------------|--------------------------------|
| Signature    | `cube X`                       |
| Operands     | 1                              |
| Returns      | X * X * X (int or float)       |
| Errors       | None                           |

**Examples:**

```
cube 3       -> 27
cube 2.5     -> 15.625
cube -2      -> -8
```

---

### `square_root`

| Property     | Value                                          |
|--------------|------------------------------------------------|
| Signature    | `square_root X`                                |
| Operands     | 1                                              |
| Returns      | Non-negative square root of X as float         |
| Errors       | `ValueError` if X is negative                  |

**Examples:**

```
square_root 25      -> 5.0
square_root 2       -> 1.4142135623730951
square_root 0       -> 0.0
square_root -4      -> Math error: math domain error
```

---

### `cube_root`

| Property     | Value                                              |
|--------------|----------------------------------------------------|
| Signature    | `cube_root X`                                      |
| Operands     | 1                                                  |
| Returns      | Real cube root of X as float; preserves sign       |
| Errors       | None                                               |

**Examples:**

```
cube_root 27     -> 3.0
cube_root -8     -> -2.0
cube_root 2      -> 1.2599210498948732
```

---

### `power`

| Property     | Value                                  |
|--------------|----------------------------------------|
| Signature    | `power BASE EXPONENT`                  |
| Operands     | 2                                      |
| Returns      | BASE raised to EXPONENT (int or float) |
| Errors       | None for real results                  |

**Examples:**

```
power 2 10     -> 1024
power 3 3      -> 27
power 2 0.5    -> 1.4142135623730951
power 4 -1     -> 0.25
```

---

### `natural_log`

| Property     | Value                                              |
|--------------|----------------------------------------------------|
| Signature    | `natural_log X`                                    |
| Operands     | 1                                                  |
| Returns      | Natural logarithm of X (ln X) as float             |
| Errors       | `ValueError` if X is less than or equal to 0       |

**Examples:**

```
natural_log 1           -> 0.0
natural_log 2.718281828 -> ~1.0
natural_log 10          -> 2.302585092994046
natural_log 0           -> Math error: math domain error
natural_log -5          -> Math error: math domain error
```

---

### `log_base_10`

| Property     | Value                                              |
|--------------|----------------------------------------------------|
| Signature    | `log_base_10 X`                                    |
| Operands     | 1                                                  |
| Returns      | Base-10 logarithm of X (log10 X) as float          |
| Errors       | `ValueError` if X is less than or equal to 0       |

**Examples:**

```
log_base_10 1       -> 0.0
log_base_10 10      -> 1.0
log_base_10 1000    -> 3.0
log_base_10 0       -> Math error: math domain error
log_base_10 -1      -> Math error: math domain error
```

---

## Error Handling Summary

| Situation                              | Error type        | Message prefix in REPL/CLI     |
|----------------------------------------|-------------------|--------------------------------|
| Unknown operation name                 | `ValueError`      | `Validation error:`            |
| Wrong number of operands               | `ValueError`      | `Validation error:`            |
| Non-numeric token in operands          | `ValueError`      | `Input error:`                 |
| Division by zero                       | `ZeroDivisionError` | `Math error:`                |
| Square root of a negative number       | `ValueError`      | `Math error:`                  |
| Natural log or log10 of x <= 0        | `ValueError`      | `Math error:`                  |
| Factorial of a negative integer        | `ValueError`      | `Type error:` / `Math error:`  |
| Factorial of a non-integer type        | `TypeError`       | `Type error:`                  |

All errors are also written to `calculator.log` at `ERROR` level. The REPL continues after an error; the CLI exits with code `1`.
