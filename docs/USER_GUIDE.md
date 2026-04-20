# User Guide

This guide explains how to run the calculator and use all available operations in both interactive and CLI modes.

---

## Running the Application

### Interactive Mode

```bash
python -m src
```

Launches a full terminal session where you can run multiple operations in sequence, view history, and quit gracefully.

### CLI Mode

```bash
python main.py <operation> [operand ...]
```

Executes a single operation and exits immediately. Suitable for scripting and automation.

---

## Interactive Mode

### Session Flow

1. The application prints a welcome message and displays the operation menu.
2. Enter an operation name (e.g. `add`) or its menu number (e.g. `1`).
3. When prompted, enter the required operand(s) one at a time.
4. The result is printed: `Result: <value>`.
5. The menu is shown again for the next operation.
6. On exit, session history is saved to `history.txt`.

### Menu Display

```
Available operations:
   1. add (2 operands)
   2. subtract (2 operands)
   3. multiply (2 operands)
   4. divide (2 operands)
   5. power (2 operands)
   6. factorial (1 operand)
   7. square (1 operand)
   8. cube (1 operand)
   9. square_root (1 operand)
  10. cube_root (1 operand)
  11. log (1 operand)
  12. ln (1 operand)
   h. View history
   q. quit
```

### Selecting an Operation

You can enter either the operation name or its menu number:

```
Enter operation name or number (h for history, q to quit): add
Enter operand 1: 3
Enter operand 2: 4
  Result: 7
```

```
Enter operation name or number (h for history, q to quit): 6
Enter operand 1: 5
  Result: 120
```

Input is case-insensitive.

### Viewing History

Enter `h` at the operation prompt to display all successful operations from the current session:

```
Enter operation name or number (h for history, q to quit): h
Session history:
  add(3, 4) = 7
  factorial(5) = 120
```

If no operations have been performed yet, `No history for this session.` is displayed.

### Quitting

Enter `q`, `quit`, or `exit` at the operation prompt. The session prints `Goodbye.` and saves history to `history.txt` before exiting.

### Retry Logic

Both operation selection and operand entry allow up to **5 consecutive invalid inputs** (`MAX_VALIDATION_ATTEMPTS = 5`). After the fifth consecutive invalid entry the session prints `Maximum invalid input attempts reached. Ending session.` and exits, saving history first.

---

## CLI Mode

### Usage Syntax

```bash
python main.py <operation> [operand ...]
```

- `<operation>` — required, the operation name (see table below).
- `[operand ...]` — zero or more operands; the required count depends on the operation.

### Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success — result printed to stdout |
| `1`  | Error — error message printed to stderr |

### Examples

```bash
# Binary operations
python main.py add 3 4          # stdout: 7
python main.py subtract 10 3    # stdout: 7
python main.py multiply 3 4     # stdout: 12
python main.py divide 10 2      # stdout: 5.0
python main.py power 2 10       # stdout: 1024

# Unary operations
python main.py factorial 5      # stdout: 120
python main.py square 4         # stdout: 16
python main.py cube 3           # stdout: 27
python main.py square_root 9    # stdout: 3.0
python main.py cube_root -8     # stdout: -2.0
python main.py log 100          # stdout: 2.0
python main.py ln 1             # stdout: 0.0
```

When no arguments are given:

```bash
python main.py
# stderr: Usage: python main.py <operation> [operand ...]
#         Example: python main.py add 3 4
# exit code: 1
```

---

## Available Operations

### Binary Operations (2 operands)

| Operation  | Description              | Domain                               | Example                        |
|------------|--------------------------|--------------------------------------|--------------------------------|
| `add`      | Addition (a + b)         | Any real numbers                     | `add 3 4` → `7`                |
| `subtract` | Subtraction (a - b)      | Any real numbers                     | `subtract 10 3` → `7`          |
| `multiply` | Multiplication (a * b)   | Any real numbers                     | `multiply 3 4` → `12`          |
| `divide`   | Division (a / b)         | b must not be zero                   | `divide 10 2` → `5.0`          |
| `power`    | Exponentiation (a ^ b)   | Negative base requires integer exp   | `power 2 10` → `1024`          |

### Unary Operations (1 operand)

| Operation     | Description                  | Domain                             | Example                        |
|---------------|------------------------------|------------------------------------|--------------------------------|
| `factorial`   | Factorial (n!)               | Non-negative integers only         | `factorial 5` → `120`          |
| `square`      | Square (x²)                  | Any real number                    | `square 4` → `16`              |
| `cube`        | Cube (x³)                    | Any real number                    | `cube 3` → `27`                |
| `square_root` | Square root (√x)             | x must be ≥ 0                      | `square_root 9` → `3.0`        |
| `cube_root`   | Cube root (∛x), sign-aware   | Any real number                    | `cube_root -8` → `-2.0`        |
| `log`         | Base-10 logarithm (log₁₀ x) | x must be > 0                      | `log 100` → `2.0`              |
| `ln`          | Natural logarithm (ln x)    | x must be > 0                      | `ln 1` → `0.0`                 |

### Domain Constraint Details

- **`divide`:** Passing `0` as the second operand raises a division-by-zero error.
- **`factorial`:** The input must be a non-negative whole number. Floats representing whole numbers (e.g. `5.0`) are accepted in interactive mode but are rejected if the decimal part is non-zero. In CLI mode, `convert_operand` converts `"5.0"` to the integer `5`.
- **`square_root`:** Negative inputs produce an error (`square_root() is not defined for negative numbers`).
- **`power`:** A negative base combined with a non-integer exponent would produce a complex result and is rejected with a `ValueError`.
- **`log` / `ln`:** Zero and negative inputs produce an error.

---

## Session Behavior

### History File (`history.txt`)

- Written by the interactive session on exit (whether the user quits normally or the retry limit is reached).
- Located in the current working directory.
- Each line is one operation in the format: `operation_name(arg1, arg2, ...) = result`
- The file is **overwritten** each time a session ends (not appended).
- Only successful operations are recorded; errors are not included.

Example `history.txt`:

```
add(3, 4) = 7
factorial(5) = 120
square_root(9) = 3.0
```

### Error Log (`error.log`)

- Located in the current working directory.
- Created lazily — the file is only created when the first error actually occurs.
- Errors are **appended** across sessions, so the file grows persistently.
- Each entry is a single line in structured format:

```
TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE
```

Example entries:

```
2024-11-15T14:32:05 | UNSUPPORTED_OPERATION | foobar | N/A | unknown operation 'foobar'
2024-11-15T14:32:18 | INVALID_OPERAND | factorial | slot 1: 'abc' | 'abc' is not a valid number
2024-11-15T14:32:45 | DIVISION_BY_ZERO | divide | 10, 0 | division by zero
```

### Error Types

| Error Type                | When It Occurs                                                    |
|---------------------------|-------------------------------------------------------------------|
| `UNSUPPORTED_OPERATION`   | An operation name or number not in the registry is entered        |
| `INVALID_OPERAND`         | An operand cannot be parsed as a number, or violates type rules   |
| `ARGUMENT_COUNT_MISMATCH` | Wrong number of operands supplied in CLI mode                     |
| `DIVISION_BY_ZERO`        | Division by zero is attempted                                     |
| `INVALID_DOMAIN`          | Input is outside the mathematical domain (e.g. `sqrt` of negative)|

---

## Troubleshooting

**"Unknown operation" error**

Ensure you are spelling the operation name exactly as listed (e.g. `square_root`, not `sqrt`). Operation names are case-insensitive in interactive mode; in CLI mode they are passed directly.

**"operand is not a valid number" error**

Operands must be numeric strings. Commas, spaces, and letters are not accepted. Use `.` as the decimal separator (e.g. `3.14`).

**Session ends unexpectedly after a few wrong inputs**

The retry limit is `MAX_VALIDATION_ATTEMPTS = 5`. If you enter 5 consecutive invalid inputs (for either operation selection or operand values), the session terminates automatically.

**`error.log` not created**

The error log file is created lazily — it only appears after at least one error has been recorded. This is by design.

**`history.txt` is empty or missing**

History is only saved by the interactive session. CLI mode (`python main.py ...`) does not write a history file. If the interactive session was terminated before any operations were performed, the file may be empty or absent.
