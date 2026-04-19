# User Guide

## Introduction

The Calculator is a Python command-line application that supports 12 mathematical operations. It can be used in two interaction modes:

- **REPL mode** (interactive): a numbered menu guides you through each operation step by step.
- **CLI mode** (non-interactive): pass the operation and operands directly as command-line arguments for scripting and automation.

Both modes record operation history to `history.txt` and errors to `error.log` in the current working directory.

---

## Installation & Setup

Requirements: Python 3.12 or later.

```bash
# Clone the repository
git clone <repository-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## REPL Mode (Interactive)

### Starting REPL mode

Launch the REPL with no arguments, or with the explicit `--repl` flag:

```bash
python -m src
# or
python -m src --repl
```

### Menu navigation

On startup you will see:

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

Enter the number of the operation you want, `history` to review past operations, or `quit` to exit.

After 3 consecutive invalid selections the session ends automatically with the message "Maximum retry attempts exceeded. Session ended."

### Entering operands

After selecting an operation, you will be prompted for one or two numeric values depending on the operation's arity:

- **Unary operations** (Factorial, Square, Cube, Square Root, Cube Root, Natural Logarithm): one value prompt.
- **Binary operations** (Addition, Subtraction, Multiplication, Division, Power, Logarithm): two value prompts — "first value" and "second value".

For **Logarithm (base)**, the first operand is the value `x` and the second is the `base`.

Enter any valid number (integer or decimal, including negative values where the operation allows it). After 3 consecutive invalid entries the session ends automatically.

### Result carry-over feature

After each successful operation, the result is stored as the session's `last_result`. The next time you are prompted for the **first** operand of any operation, the prompt will show:

```
Enter value [default: <last_result>]:
```

Press Enter without typing anything to reuse the previous result as the input. This makes chaining operations more efficient — for example computing the square root of a previously computed value without re-entering it.

Carry-over is available only for the first operand of binary operations and the single operand of unary operations; it is not offered for the second operand of binary operations.

### History display

Type `history` at the operation selection prompt to view all operations performed in the current session:

```
Operation history:
  add(3.0, 4.0) = 7.0
  square_root(49.0) = 7.0
```

If no operations have been performed yet, "No history recorded yet." is displayed.

### Exit handling

- Type `quit` at the operation selection prompt to exit cleanly.
- Press `Ctrl+C` or `Ctrl+D` (EOF) at any prompt to exit immediately.

---

## CLI Mode (Command-line)

### How to invoke CLI mode

Pass an operation name (or alias) followed by the required operands as command-line arguments:

```bash
python -m src <operation> <operand1> [operand2]
```

At least two arguments are required (operation + at least one operand). Providing only one argument that is not `--repl` prints a usage message and exits with code 1.

### Operation and operand syntax

- The first argument is the operation name or a recognised alias (see below).
- Subsequent arguments are numeric operands parsed as floating-point numbers.
- The number of operands must exactly match the operation's arity (1 for unary, 2 for binary).

### Symbol aliases

The following short-hand symbols are accepted as operation names:

| Symbol | Operation            |
|--------|----------------------|
| `+`    | add                  |
| `-`    | subtract             |
| `*`    | multiply             |
| `/`    | divide               |
| `^`    | power                |
| `log`  | logarithm            |
| `sqrt` | square_root          |
| `cbrt` | cube_root            |
| `ln`   | natural_logarithm    |

Operations with no alias (`factorial`, `square`, `cube`) must be used by their canonical name.

### Exit codes

| Code | Meaning                                                         |
|------|-----------------------------------------------------------------|
| 0    | Success — result printed to stdout                              |
| 1    | Usage error — wrong number of top-level arguments               |
| 2    | Unknown operation name                                          |
| 3    | Invalid operands — missing, non-numeric, or wrong count         |
| 4    | Operation error — division by zero, math domain error, or other numeric exception |

### Examples for each operation

```bash
# Binary operations
python -m src add 3 4            # -> 7.0
python -m src + 1.5 2.5          # -> 4.0
python -m src subtract 10 3      # -> 7.0
python -m src - 5.0 2.5          # -> 2.5
python -m src multiply 3 4       # -> 12.0
python -m src * 2.5 4.0          # -> 10.0
python -m src divide 10 4        # -> 2.5
python -m src / 7.5 2.5          # -> 3.0
python -m src power 2 10         # -> 1024.0
python -m src ^ 3 3              # -> 27.0
python -m src logarithm 100 10   # -> 2.0  (log base 10 of 100)
python -m src log 8 2            # -> 3.0  (log base 2 of 8)

# Unary operations
python -m src factorial 5        # -> 120
python -m src square 4           # -> 16.0
python -m src cube 3             # -> 27.0
python -m src square_root 9      # -> 3.0
python -m src sqrt 2             # -> 1.4142135623730951
python -m src cube_root 27       # -> 3.0
python -m src cbrt -8            # -> -2.0
python -m src natural_logarithm 1 # -> 0.0
python -m src ln 2.718281828459045 # -> 1.0
```

---

## Common Use Cases

### Chaining operations in shell scripts

Use CLI mode with shell command substitution to chain operations:

```bash
# Compute sqrt(3^2 + 4^2) (Pythagorean theorem)
A=$(python -m src power 3 2)
B=$(python -m src power 4 2)
SUM=$(python -m src add "$A" "$B")
python -m src sqrt "$SUM"     # -> 5.0
```

### Interactive exploration

Use REPL mode when exploring multiple operations:

```bash
python -m src
# Select 5 (Power), enter 2 and 10 -> 1024.0
# Press Enter on the next prompt to reuse 1024.0 as input
# Select 10 (Square Root) -> 32.0
```

---

## Error Messages & Troubleshooting

| Error message                                        | Cause                                           | Solution                                         |
|------------------------------------------------------|-------------------------------------------------|--------------------------------------------------|
| `Error: Unknown operation: 'xyz'`                    | The operation name is not recognised            | Check spelling; use a valid name or alias        |
| `Error: Missing operand(s) for 'add': expected 2...` | Wrong number of operands supplied               | Provide the correct number of operands           |
| `Error: Invalid number: 'abc'`                       | An operand could not be parsed as a number      | Ensure all operands are numeric values           |
| `Error: Cannot divide by zero`                       | Division with a zero divisor                    | Use a non-zero second operand                    |
| `Error: factorial() not defined for negative values` | Negative input to `factorial`                   | Use a non-negative integer                       |
| `Error: factorial() only accepts integer values...`  | Non-integer float passed to `factorial`         | Use whole numbers (e.g. `5` not `5.5`)           |
| `Error: square_root() not defined for negative values` | Negative input to `square_root`               | Use a non-negative value                         |
| `Error: logarithm() not defined for non-positive values` | Non-positive `x` in logarithm             | Use a positive value for `x`                     |
| `Error: logarithm base must be positive and not equal to 1` | Invalid base for `logarithm`          | Use a positive base other than 1                 |
| `Error: natural_logarithm() not defined for non-positive values` | Non-positive input to `ln`       | Use a positive value                             |
| `Maximum retry attempts exceeded. Session ended.`    | 3 consecutive invalid inputs in REPL mode       | Restart the REPL and enter valid values          |

---

## File Outputs

### `history.txt`

Created (or truncated) at the start of each session. Each line records one completed operation in the format:

```
add(3.0, 4.0) = 7.0
square_root(49.0) = 7.0
```

The file is written in the current working directory. I/O errors are printed to stderr and do not interrupt the session.

### `error.log`

Created (or truncated) at the start of each session. Each line records one error in the format:

```
<ISO8601 timestamp> | <ERROR_TYPE> | input=<user_input> | <exception message>
```

Where `ERROR_TYPE` is one of:
- `INVALID_INPUT` — bad operand format or wrong operand count
- `UNSUPPORTED_OPERATION` — unrecognised operation name
- `CALCULATION_ERROR` — numeric/domain error during calculation

Example entry:
```
2025-03-01T14:32:11.045321 | CALCULATION_ERROR | input='divide 5 0' | Cannot divide by zero
```

The file is written in the current working directory. I/O errors are printed to stderr and do not interrupt the session.
