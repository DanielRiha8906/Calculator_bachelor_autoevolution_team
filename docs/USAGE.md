# Usage Guide

## Interaction Modes Overview

The calculator supports two interaction modes:

| Mode | When it activates | How to invoke |
|------|-------------------|---------------|
| **REPL** | No arguments (or only `--repl`) | `python -m src` |
| **CLI** | Operation name and operand(s) provided | `python -m src <operation> <operand> [operand2]` |

Both modes share the same underlying operations and produce identical numeric
results.

---

## REPL Mode Walkthrough

### Starting the REPL

```
python -m src
```

or

```
python -m src --repl
```

The REPL prints a welcome message and displays the operation menu:

```
Welcome to the Calculator REPL. Type 'quit' to exit.

Available operations:
  1. Addition
  2. Subtraction
  3. Multiplication
  4. Division
  5. Power
  6. Logarithm (base)
  7. Factorial
  8. Square
  9. Cube
  10. Square Root
  11. Cube Root
  12. Natural Logarithm
  history. Show operation history
  quit. Exit
Select operation:
```

### Selecting an Operation

Type the number next to the operation you want and press Enter:

```
Select operation: 1
Enter first value: 10
Enter second value: 3
Addition(10.0, 3.0) = 13.0
```

### Carry-Over Default

After each successful calculation the result is stored as `last_result`. On
the next operation, the first-value prompt shows this as a default:

```
Select operation: 1
Enter first value [default: 13.0]:
```

Pressing Enter without typing accepts the default. Typing a new value overrides
it. The carry-over applies only to the first operand of binary operations.

### Viewing History

Type `history` at the operation selection prompt to display all operations
performed during the current session:

```
Select operation: history

Operation history:
  add(10.0, 3.0) = 13.0
  subtract(13.0, 4.0) = 9.0
```

### Exiting the REPL

Type `quit` at the operation selection prompt:

```
Select operation: quit
Calculator closed.
```

Pressing Ctrl+C or Ctrl+D (EOF) also closes the REPL cleanly.

### Invalid Input Handling

If you type something that is not a valid menu number, `history`, or `quit`,
the REPL re-prompts up to 3 times (MAX_RETRIES = 3). After the third
consecutive invalid input the session ends:

```
Select operation: abc
Invalid selection. Enter a number from the list, 'history', or 'quit'.
Select operation: xyz
Invalid selection. Enter a number from the list, 'history', or 'quit'.
Select operation: ??
Maximum retry attempts exceeded. Session ended.
```

The same retry limit applies to operand entry.

---

## CLI Mode

### Syntax

```
python -m src <operation> <operand> [operand2]
```

- `<operation>` — the canonical operation name or an accepted alias.
- `<operand>` — a numeric value (integer or decimal).
- `[operand2]` — required for binary operations; omit for unary operations.

The result is printed to stdout on success. Errors are printed to stderr and
the process exits with a non-zero exit code.

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Wrong number of arguments (usage error) |
| 2 | Unknown operation name |
| 3 | Invalid operands (missing, non-numeric, wrong count) |
| 4 | Calculation error (division by zero, math domain error) |

---

## CLI Examples for All 12 Operations

### Addition
```
python -m src add 5 3        # 8.0
python -m src + 5 3          # 8.0
```

### Subtraction
```
python -m src subtract 10 4  # 6.0
python -m src - 10 4         # 6.0
```

### Multiplication
```
python -m src multiply 6 7   # 42.0
python -m src * 6 7          # 42.0
```

### Division
```
python -m src divide 15 4    # 3.75
python -m src / 15 4         # 3.75
```

### Power
```
python -m src power 2 8      # 256.0
python -m src ^ 2 8          # 256.0
```

### Logarithm (base)
```
python -m src logarithm 1000 10    # 2.9999999999999996
python -m src log 8 2              # 3.0
```

### Factorial
```
python -m src factorial 6    # 720
python -m src factorial 0    # 1
```

### Square
```
python -m src square 9       # 81.0
```

### Cube
```
python -m src cube 4         # 64.0
```

### Square Root
```
python -m src square_root 16    # 4.0
python -m src sqrt 2            # 1.4142135623730951
```

### Cube Root
```
python -m src cube_root 27    # 3.0
python -m src cbrt -8         # -2.0
```

### Natural Logarithm
```
python -m src natural_logarithm 1    # 0.0
python -m src ln 10                  # 2.302585092994046
```

---

## Special Behaviors

### Logarithm is Always Two-Argument

Unlike `natural_logarithm` (one argument), `logarithm` / `log` always requires
two arguments: the value x and the base.

```
python -m src log 100 10     # 2.0   (log base 10 of 100)
python -m src log 32 2       # 5.0   (log base 2 of 32)
```

Providing only one argument is an arity error:

```
python -m src log 100
# Error: Missing operand(s) for 'log': expected 2 operand(s), got 1
```

### Carry-Over in REPL

The REPL carries the result of the previous operation forward as the default
first operand. This allows chaining calculations without retyping numbers. The
carry-over is reset to `None` after each binary operation's first operand is
collected, so the second operand always requires explicit input.

---

## Edge Cases

### Negative Numbers as CLI Operands

Negative numbers work as operands:

```
python -m src subtract 0 5     # -5.0
python -m src cube -3          # -27.0
python -m src cbrt -27         # -3.0
```

### Float Precision

Floating-point arithmetic can produce results with small rounding errors:

```
python -m src logarithm 1000 10    # 2.9999999999999996  (not exactly 3.0)
```

This is expected IEEE 754 behaviour and not a bug.

### Domain Errors

Operations outside their domain raise a `ValueError` and exit with code 4 in
CLI mode, or print an error and continue in REPL mode:

```
python -m src sqrt -4
# Error: square_root() not defined for negative values

python -m src ln 0
# Error: natural_logarithm() not defined for non-positive values

python -m src divide 5 0
# Error: Cannot divide by zero

python -m src factorial -1
# Error: factorial() not defined for negative values
```

---

## File Outputs

### error.log

Location: `error.log` in the current working directory.

At session start (both REPL and CLI), the error log is cleared. Errors
encountered during the session are appended one per line in the format:

```
<ISO8601 timestamp> | <ERROR_TYPE> | input=<user_input> | <error message>
```

Example:

```
2024-03-15T14:23:01.456789 | CALCULATION_ERROR | input='divide 5 0' | Cannot divide by zero
2024-03-15T14:23:15.123456 | INVALID_INPUT | input='add 5' | Missing operand(s) for 'add': expected 2 operand(s), got 1
```

Error type constants:

| Constant | Meaning |
|----------|---------|
| `INVALID_INPUT` | Input could not be parsed or count is wrong |
| `UNSUPPORTED_OPERATION` | Operation name not recognised |
| `CALCULATION_ERROR` | Numeric/domain error during calculation |

### history.txt

Location: `history.txt` in the current working directory.

At session start, the history file is cleared. Each completed operation is
appended as one line:

```
add(2.0, 3.0) = 5.0
multiply(5.0, 4.0) = 20.0
```

The history file is also accessible interactively by typing `history` in the
REPL.
