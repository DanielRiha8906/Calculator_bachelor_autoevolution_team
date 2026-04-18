# Calculator — Feature Reference

This document provides a detailed reference for every calculator operation: its mathematical definition, operand requirements, valid input ranges, error conditions, and usage examples in both CLI and interactive modes.

All operations are accessed via the operation key name shown in the headings below.

---

## Binary Operations (two operands)

### `add` — Addition

**Definition:** a + b

**Operands:** 2 (both numeric, any real number)

**Valid input range:** All real numbers

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src add 3 5
# Output: 8.0

python -m src add -2.5 1.5
# Output: -1.0
```

Interactive:
```
Enter operation: add
Enter operand 1: 3
Enter operand 2: 5
Result: 8.0
```

---

### `subtract` — Subtraction

**Definition:** a - b

**Operands:** 2 (both numeric, any real number)

**Valid input range:** All real numbers

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src subtract 10 4
# Output: 6.0

python -m src subtract 0 5
# Output: -5.0
```

Interactive:
```
Enter operation: subtract
Enter operand 1: 10
Enter operand 2: 4
Result: 6.0
```

---

### `multiply` — Multiplication

**Definition:** a * b

**Operands:** 2 (both numeric, any real number)

**Valid input range:** All real numbers

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src multiply 6 7
# Output: 42.0

python -m src multiply -3 4
# Output: -12.0
```

Interactive:
```
Enter operation: multiply
Enter operand 1: 6
Enter operand 2: 7
Result: 42.0
```

---

### `divide` — Division

**Definition:** a / b

**Operands:** 2 (both numeric, any real number)

**Valid input range:** a — all real numbers; b — any non-zero real number

**Error conditions:**
- `ValueError: Division by zero is not allowed` — raised when b is 0

**Examples:**

CLI:
```bash
python -m src divide 10 2
# Output: 5.0

python -m src divide 10 0
# stderr: error: Division by zero is not allowed
# exit code: 2
```

Interactive:
```
Enter operation: divide
Enter operand 1: 10
Enter operand 2: 2
Result: 5.0

Enter operation: divide
Enter operand 1: 10
Enter operand 2: 0
Error: Division by zero is not allowed
```

---

### `power` — Exponentiation

**Definition:** base ^ exponent (base ** exponent)

**Operands:** 2 (base and exponent; both numeric, any real number)

**Valid input range:** All real numbers for both operands

**Error conditions:** None (Python handles edge cases such as 0^0 = 1 natively)

**Examples:**

CLI:
```bash
python -m src power 2 8
# Output: 256.0

python -m src power 3 3
# Output: 27.0
```

Interactive:
```
Enter operation: power
Enter operand 1: 2
Enter operand 2: 8
Result: 256.0
```

---

## Unary Operations (one operand)

### `factorial` — Factorial

**Definition:** n! = n * (n-1) * ... * 1; 0! = 1

**Operands:** 1 (must be a non-negative integer)

**Valid input range:** Non-negative integers (0, 1, 2, ...)

**Error conditions:**
- `ValueError: n must be a non-negative integer, got <n>` — raised when n is negative
- `ValueError: n must be an integer, got <type>` — raised when n is not an integer (e.g. a float with a fractional part)

**Notes:** The operand is parsed as float at the input boundary and converted to int for the factorial computation. Whole-number floats such as 5.0 are accepted; fractional floats such as 5.5 are not.

**Examples:**

CLI:
```bash
python -m src factorial 5
# Output: 120.0

python -m src factorial 0
# Output: 1.0

python -m src factorial -3
# stderr: error: n must be a non-negative integer, got -3
# exit code: 2
```

Interactive:
```
Enter operation: factorial
Enter operand: 5
Result: 120.0
```

---

### `square` — Square

**Definition:** x^2

**Operands:** 1 (any real number)

**Valid input range:** All real numbers

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src square 4
# Output: 16.0

python -m src square -3
# Output: 9.0
```

Interactive:
```
Enter operation: square
Enter operand: 4
Result: 16.0
```

---

### `cube` — Cube

**Definition:** x^3

**Operands:** 1 (any real number)

**Valid input range:** All real numbers

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src cube 3
# Output: 27.0

python -m src cube -2
# Output: -8.0
```

Interactive:
```
Enter operation: cube
Enter operand: 3
Result: 27.0
```

---

### `square_root` — Square Root

**Definition:** sqrt(x)

**Operands:** 1 (non-negative real number)

**Valid input range:** x >= 0

**Error conditions:**
- `ValueError: square_root requires a non-negative number, got <x>` — raised when x is negative

**Examples:**

CLI:
```bash
python -m src square_root 9
# Output: 3.0

python -m src square_root 2
# Output: 1.4142135623730951

python -m src square_root -4
# stderr: error: square_root requires a non-negative number, got -4.0
# exit code: 2
```

Interactive:
```
Enter operation: square_root
Enter operand: 9
Result: 3.0

Enter operation: square_root
Enter operand: -4
Error: square_root requires a non-negative number, got -4.0
```

---

### `cube_root` — Cube Root

**Definition:** cbrt(x)

**Operands:** 1 (any real number)

**Valid input range:** All real numbers (negative numbers are supported via Python 3.12 `math.cbrt`)

**Error conditions:** None

**Examples:**

CLI:
```bash
python -m src cube_root 27
# Output: 3.0

python -m src cube_root -8
# Output: -2.0
```

Interactive:
```
Enter operation: cube_root
Enter operand: 27
Result: 3.0
```

---

### `log` — Base-10 Logarithm

**Definition:** log10(x)

**Operands:** 1 (positive real number)

**Valid input range:** x > 0

**Error conditions:**
- `ValueError: log requires a positive number, got <x>` — raised when x is zero or negative

**Examples:**

CLI:
```bash
python -m src log 100
# Output: 2.0

python -m src log 1
# Output: 0.0

python -m src log 0
# stderr: error: log requires a positive number, got 0.0
# exit code: 2
```

Interactive:
```
Enter operation: log
Enter operand: 100
Result: 2.0

Enter operation: log
Enter operand: -5
Error: log requires a positive number, got -5.0
```

---

### `ln` — Natural Logarithm

**Definition:** ln(x) = loge(x)

**Operands:** 1 (positive real number)

**Valid input range:** x > 0

**Error conditions:**
- `ValueError: ln requires a positive number, got <x>` — raised when x is zero or negative

**Examples:**

CLI:
```bash
python -m src ln 1
# Output: 0.0

python -m src ln 2.718281828459045
# Output: 1.0 (approximately)

python -m src ln 0
# stderr: error: ln requires a positive number, got 0.0
# exit code: 2
```

Interactive:
```
Enter operation: ln
Enter operand: 1
Result: 0.0
```

---

## Meta-Commands (interactive mode only)

### `history` — View Session History

Displays all operations performed since the current interactive session started. History is also persisted to `history.txt` in the working directory.

Binary operation entries are formatted as:
```
operand1 operation operand2 = result
```

Unary operation entries are formatted as:
```
operation(operand) = result
```

If no operations have been performed yet:
```
No operations recorded in this session.
```

The `history` command is not available in CLI mode.

### `exit` — Quit

Typing `exit` at the operation prompt ends the interactive session with the message `Goodbye!`.

---

## Error Handling

### Interactive mode

Invalid operations and non-numeric operands trigger a retry prompt. The user has up to 3 attempts per prompt:

- **Invalid operation:** after 3 failed attempts, the message `Maximum retry attempts reached. Terminating session.` is shown and the session ends.
- **Invalid operand:** after 3 failed attempts for a single operand, the message `Maximum retry attempts reached for operand N. Returning to menu.` is shown and the menu is redisplayed.

Calculation errors (e.g. division by zero) display `Error: <message>` and return to the menu without ending the session.

### CLI mode

All errors print a message to stderr and exit with code 2. No retry logic is applied in CLI mode.

All errors are logged to `error.log` in the working directory with a UTC timestamp, error category, message, and context.
