# User Guide

This guide covers all end-user-facing features of the calculator, including CLI and interactive usage, supported operators, and troubleshooting.

## Table of Contents

- [Running the Calculator](#running-the-calculator)
- [CLI Mode](#cli-mode)
  - [Basic Usage](#basic-usage)
  - [Supported Operators](#supported-operators)
  - [Operator Precedence](#operator-precedence)
  - [Grouping with Parentheses](#grouping-with-parentheses)
  - [CLI Examples](#cli-examples)
  - [Exit Codes](#exit-codes)
- [Interactive Mode](#interactive-mode)
  - [Starting Interactive Mode](#starting-interactive-mode)
  - [Operation List](#operation-list)
  - [Entering Operands](#entering-operands)
  - [Exiting](#exiting)
  - [Interactive Examples](#interactive-examples)
- [Troubleshooting](#troubleshooting)

---

## Running the Calculator

The calculator is run as a Python module from the repository root:

```bash
python -m src [expression]
```

- With an expression argument: evaluates the expression and exits (CLI mode).
- Without arguments: opens the interactive prompt.

---

## CLI Mode

### Basic Usage

Pass an arithmetic expression as one or more arguments. The arguments are joined with spaces to form the expression.

```bash
python -m src "3 + 4"
# output: 7

python -m src 3 + 4
# output: 7  (same — arguments are joined)
```

### Supported Operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `3 + 4` | `7` |
| `-` | Subtraction | `10 - 3` | `7` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `10 / 4` | `2.5` |
| `**` | Power (exponentiation) | `2 ** 8` | `256.0` |
| `-` (unary) | Negation | `-5 + 2` | `-3` |

Numbers may be integers (`3`, `100`) or decimals (`3.14`, `0.5`).

### Operator Precedence

Standard mathematical precedence applies:

1. Parentheses `( )`
2. Exponentiation `**`
3. Unary minus `-`
4. Multiplication `*` and division `/` (left to right)
5. Addition `+` and subtraction `-` (left to right)

This matches Python's operator precedence.

### Grouping with Parentheses

Use parentheses to control evaluation order:

```bash
python -m src "2 + 3 * 4"
# output: 14   (multiplication first)

python -m src "(2 + 3) * 4"
# output: 20   (addition first)
```

### CLI Examples

```bash
# Addition
python -m src "5 + 3"
# 8

# Subtraction
python -m src "20 - 7"
# 13

# Multiplication
python -m src "6 * 7"
# 42

# Division
python -m src "15 / 4"
# 3.75

# Power
python -m src "3 ** 4"
# 81.0

# Unary minus
python -m src "-10 + 3"
# -7

# Complex expression
python -m src "2 ** 10 / (4 + 4)"
# 128.0
```

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success — result printed to stdout |
| `1` | Error — message printed to stderr |

---

## Interactive Mode

### Starting Interactive Mode

```bash
python -m src
```

The calculator prints the list of available operations and waits for input.

### Operation List

```
Calculator — available operations:
   1. add
   2. subtract
   3. multiply
   4. divide
   5. factorial
   6. square
   7. cube
   8. square_root
   9. cube_root
  10. power
  11. log10
  12. natural_log
  Type 'quit' or 'exit' to leave.
```

### Entering Operands

After typing an operation name, the calculator prompts for each required operand. Binary operations (two operands) prompt twice; unary operations (one operand) prompt once.

```
Select operation: add
  Enter operand 1: 12
  Enter operand 2: 8
  Result: 20
```

```
Select operation: square_root
  Enter operand: 144
  Result: 12.0
```

If you enter an invalid number, you are given up to 3 attempts per operand. After 3 failed attempts the calculator returns to the operation selection prompt.

Similarly, if you enter an unknown operation name, you have up to 3 attempts. After 3 consecutive invalid operation names the calculator exits.

### Exiting

Type `quit` or `exit` at the operation selection prompt:

```
Select operation: quit
Bye!
```

### Interactive Examples

**Multiplication:**
```
Select operation: multiply
  Enter operand 1: 9
  Enter operand 2: 7
  Result: 63
```

**Factorial:**
```
Select operation: factorial
  Enter operand: 6
  Result: 720
```

**Natural logarithm:**
```
Select operation: natural_log
  Enter operand: 2.718281828
  Result: 0.9999999998...
```

**Cube root of a negative number:**
```
Select operation: cube_root
  Enter operand: -27
  Result: -3.0
```

**Handling invalid input:**
```
Select operation: add
  Enter operand 1: abc
  Error: Invalid number: 'abc'. Please enter an integer or decimal value.
  Invalid input. Attempt 1 of 3.
  Enter operand 1: 5
  Enter operand 2: 3
  Result: 8
```

**Division by zero:**
```
Select operation: divide
  Enter operand 1: 10
  Enter operand 2: 0
  Result: Error: Division by zero is not allowed.
```

---

## Troubleshooting

### "Error: No expression provided"

You ran `python -m src` with a space but no actual expression, or an empty string was passed. Supply a non-empty expression:

```bash
python -m src "5 + 3"
```

### "Error: Invalid expression syntax"

The expression contains syntax Python's parser cannot understand (e.g. missing operands, mismatched parentheses, use of unsupported characters):

```bash
python -m src "5 +"          # missing right-hand operand
python -m src "(3 + 4"       # unmatched parenthesis
python -m src "3 % 2"        # % is not a supported operator
```

Fix: check that the expression is a valid arithmetic expression using only the supported operators listed above.

### "Error: Division by zero is not allowed"

The expression results in a division by zero:

```bash
python -m src "5 / 0"
```

### "Error: Square root is not defined for negative numbers"

Square root of a negative number is not supported. Use `cube_root` if you need the real root of a negative number.

### Operations not available in CLI mode

Scientific operations like `factorial`, `square`, `log10`, etc. are not available as CLI operators. For those, use interactive mode. CLI mode supports only the five infix operators: `+`, `-`, `*`, `/`, `**`.

### Log file

Errors are automatically logged to `calculator.log` in the directory from which you ran the command. If you encounter unexpected behaviour, check that file for detailed error messages.
