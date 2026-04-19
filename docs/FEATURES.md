# Calculator Features

## Operation Catalog

The calculator supports 12 operations split into two categories: 6 binary (two-operand) and 6 unary (one-operand).

---

## Binary Operations

Binary operations require exactly two numeric operands.

### Addition

| Attribute    | Value                         |
|------------- |-------------------------------|
| Name         | `add`                         |
| Arity        | 2                             |
| Aliases      | `+`                           |
| Display name | Addition                      |
| Definition   | Returns `a + b`               |

Examples:
```
add 3 4   -> 7
+ 1.5 2.5 -> 4.0
```

### Subtraction

| Attribute    | Value                         |
|------------- |-------------------------------|
| Name         | `subtract`                    |
| Arity        | 2                             |
| Aliases      | `-`                           |
| Display name | Subtraction                   |
| Definition   | Returns `a - b`               |

Examples:
```
subtract 10 3 -> 7
- 5.0 2.5     -> 2.5
```

### Multiplication

| Attribute    | Value                         |
|------------- |-------------------------------|
| Name         | `multiply`                    |
| Arity        | 2                             |
| Aliases      | `*`                           |
| Display name | Multiplication                |
| Definition   | Returns `a * b`               |

Examples:
```
multiply 3 4 -> 12
* 2.5 4.0    -> 10.0
```

### Division

| Attribute    | Value                         |
|------------- |-------------------------------|
| Name         | `divide`                      |
| Arity        | 2                             |
| Aliases      | `/`                           |
| Display name | Division                      |
| Definition   | Returns `a / b`               |

Examples:
```
divide 10 4  -> 2.5
/ 7.5 2.5    -> 3.0
```

Error conditions:
- Raises `ZeroDivisionError` when `b == 0`.

### Power

| Attribute    | Value                         |
|------------- |-------------------------------|
| Name         | `power`                       |
| Arity        | 2                             |
| Aliases      | `^`                           |
| Display name | Power                         |
| Definition   | Returns `base ** exponent`    |

Examples:
```
power 2 10 -> 1024.0
^ 3 3      -> 27.0
```

### Logarithm (arbitrary base)

| Attribute    | Value                                      |
|------------- |--------------------------------------------|
| Name         | `logarithm`                                |
| Arity        | 2                                          |
| Aliases      | `log`                                      |
| Display name | Logarithm (base)                           |
| Definition   | Returns `math.log(x, base)` — the logarithm of `x` in the given `base` |

This is the **two-argument variant** of logarithm. The first operand is the value `x`, the second is the `base`. This special-case dispatch is handled in `OperationRegistry` rather than directly in `Calculator`.

Examples:
```
logarithm 100 10 -> 2.0
log 8 2          -> 3.0
```

Error conditions:
- Raises `ValueError` when `x <= 0`.
- Raises `ValueError` when `base <= 0` or `base == 1`.

---

## Unary Operations

Unary operations require exactly one numeric operand.

### Factorial

| Attribute    | Value                                             |
|------------- |---------------------------------------------------|
| Name         | `factorial`                                       |
| Arity        | 1                                                 |
| Aliases      | (none)                                            |
| Display name | Factorial                                         |
| Definition   | Returns `n!` (product of all positive integers up to `n`) |

Examples:
```
factorial 5 -> 120
factorial 0 -> 1
```

Error conditions:
- Raises `ValueError` when `n < 0`.
- Raises `TypeError` when the input is a float with a non-integer value (e.g. `5.5`).
- Whole-number floats (e.g. `5.0`) are accepted and automatically converted to `int`.

### Square

| Attribute    | Value                     |
|------------- |---------------------------|
| Name         | `square`                  |
| Arity        | 1                         |
| Aliases      | (none)                    |
| Display name | Square                    |
| Definition   | Returns `x ** 2`          |

Examples:
```
square 4    -> 16.0
square -3   -> 9.0
```

### Cube

| Attribute    | Value                     |
|------------- |---------------------------|
| Name         | `cube`                    |
| Arity        | 1                         |
| Aliases      | (none)                    |
| Display name | Cube                      |
| Definition   | Returns `x ** 3`          |

Examples:
```
cube 3    -> 27.0
cube -2   -> -8.0
```

### Square Root

| Attribute    | Value                                         |
|------------- |-----------------------------------------------|
| Name         | `square_root`                                 |
| Arity        | 1                                             |
| Aliases      | `sqrt`                                        |
| Display name | Square Root                                   |
| Definition   | Returns `math.sqrt(x)` — the non-negative square root of `x` |

Examples:
```
square_root 9   -> 3.0
sqrt 2          -> 1.4142135623730951
```

Error conditions:
- Raises `ValueError` when `x < 0`.

### Cube Root

| Attribute    | Value                                              |
|------------- |----------------------------------------------------|
| Name         | `cube_root`                                        |
| Arity        | 1                                                  |
| Aliases      | `cbrt`                                             |
| Display name | Cube Root                                          |
| Definition   | Returns the real-valued cube root of `x`, preserving sign |

The implementation uses `math.copysign(abs(x) ** (1/3), x)` to correctly handle negative inputs (unlike `x ** (1/3)` which returns a complex number for negative `x` in Python).

Examples:
```
cube_root 27   -> 3.0
cbrt -8        -> -2.0
cube_root 0    -> 0.0
```

### Natural Logarithm

| Attribute    | Value                                            |
|------------- |--------------------------------------------------|
| Name         | `natural_logarithm`                              |
| Arity        | 1                                                |
| Aliases      | `ln`                                             |
| Display name | Natural Logarithm                                |
| Definition   | Returns `math.log(x)` — the natural logarithm (base e) of `x` |

Examples:
```
natural_logarithm 1      -> 0.0
ln 2.718281828459045     -> 1.0
```

Error conditions:
- Raises `ValueError` when `x <= 0`.

---

## Domain Constraints & Error Conditions

| Operation          | Constraint                                  | Error type          |
|--------------------|---------------------------------------------|---------------------|
| `divide`           | `b != 0`                                    | `ZeroDivisionError` |
| `factorial`        | `n >= 0`, integer value                     | `ValueError`, `TypeError` |
| `square_root`      | `x >= 0`                                    | `ValueError`        |
| `natural_logarithm`| `x > 0`                                     | `ValueError`        |
| `logarithm`        | `x > 0`, `base > 0`, `base != 1`           | `ValueError`        |
| `square`           | No constraints                              | N/A                 |
| `cube`             | No constraints                              | N/A                 |
| `cube_root`        | No constraints                              | N/A                 |
| `add`              | No constraints                              | N/A                 |
| `subtract`         | No constraints                              | N/A                 |
| `multiply`         | No constraints                              | N/A                 |
| `power`            | No constraints (Python handles complex results) | N/A             |

---

## Numeric Precision & Edge Cases

- All arithmetic uses Python native `float` (IEEE 754 double precision).
- `factorial` returns `int` for exact results; all other operations return `float`.
- `cube_root(0)` returns `0.0` directly as a special case to avoid rounding artefacts in the `copysign`/`abs` path.
- `factorial` accepts whole-number floats such as `5.0` and converts them to `int` internally before computing.
- `power` with a negative base and fractional exponent may return `nan` or raise depending on Python float semantics.

---

## Operation Aliases Reference

| Alias  | Canonical name       |
|--------|----------------------|
| `+`    | `add`                |
| `-`    | `subtract`           |
| `*`    | `multiply`           |
| `/`    | `divide`             |
| `^`    | `power`              |
| `log`  | `logarithm`          |
| `sqrt` | `square_root`        |
| `cbrt` | `cube_root`          |
| `ln`   | `natural_logarithm`  |

Operations with no alias (`factorial`, `square`, `cube`) must be referred to by their canonical name in CLI mode and are selected by menu number in REPL mode.
