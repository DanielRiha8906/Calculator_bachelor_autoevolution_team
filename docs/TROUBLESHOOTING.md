# Troubleshooting

## Error Messages and Solutions

### "Unknown operation: 'xyz'"

**Cause:** The operation token provided to the CLI is not a recognized name or
alias.

**Solution:** Use a valid operation name or alias. See the summary table in
[OPERATIONS_REFERENCE.md](OPERATIONS_REFERENCE.md) for the full list. Common
aliases include `+`, `-`, `*`, `/`, `^`, `sqrt`, `cbrt`, `log`, and `ln`.

```
python -m src add 3 4      # correct
python -m src plus 3 4     # Error: Unknown operation 'plus'
```

**Exit code:** 2

---

### "Missing operand(s) for 'X': expected N operand(s), got M"

**Cause:** The wrong number of operands was provided for the operation.

**Solution:** Binary operations (add, subtract, multiply, divide, power,
logarithm) require exactly 2 operands. Unary operations (factorial, square,
cube, square_root, cube_root, natural_logarithm) require exactly 1 operand.

```
python -m src add 3        # Error: expected 2, got 1
python -m src add 3 4 5    # Error: expected 2, got 3
python -m src add 3 4      # OK: 7.0
```

**Exit code:** 3

---

### "Invalid number: 'abc'"

**Cause:** One of the operand strings cannot be parsed as a float.

**Solution:** Provide numeric values only. Integers and decimal floats are
accepted. Scientific notation (e.g. `1e3`) is also accepted because Python's
`float()` parses it.

```
python -m src add 3 four       # Error: Invalid number: 'four'
python -m src add 3 4.5        # OK: 7.5
python -m src add 3 1e2        # OK: 103.0
```

**Exit code:** 3

---

### "Cannot divide by zero"

**Cause:** The second operand of `divide` (or `/`) is 0.

**Solution:** Provide a non-zero divisor.

```
python -m src divide 5 0    # Error: Cannot divide by zero
python -m src divide 5 2    # OK: 2.5
```

**Exit code:** 4

---

### "factorial() not defined for negative values"

**Cause:** A negative number was passed to `factorial`.

**Solution:** Factorial is defined only for non-negative integers (0, 1, 2, …).

```
python -m src factorial -1    # Error
python -m src factorial 0     # OK: 1
```

**Exit code:** 4

---

### "factorial() only accepts integer values, not non-integer floats"

**Cause:** A float with a fractional part (e.g. 5.5) was passed to `factorial`.

**Solution:** Provide a whole number. `5.0` is accepted (it is treated as
integer 5), but `5.5` is not.

```
python -m src factorial 5.5    # Error
python -m src factorial 5.0    # OK: 120
python -m src factorial 5      # OK: 120
```

**Exit code:** 4

---

### "square_root() not defined for negative values"

**Cause:** A negative number was passed to `square_root` / `sqrt`.

**Solution:** `square_root` operates on the real number line. Use `power` with
exponent 0.5 for complex roots — but note that Python's `**` on negatives with
non-integer exponents also raises a `ValueError` unless you use `complex` types.

```
python -m src sqrt -4    # Error
python -m src sqrt 4     # OK: 2.0
```

**Exit code:** 4

---

### "natural_logarithm() not defined for non-positive values"

**Cause:** A value <= 0 was passed to `natural_logarithm` / `ln`.

**Solution:** The natural logarithm is only defined for x > 0.

```
python -m src ln 0     # Error
python -m src ln -1    # Error
python -m src ln 1     # OK: 0.0
```

**Exit code:** 4

---

### "logarithm() not defined for non-positive values" / "logarithm base must be positive and not equal to 1"

**Cause:** Invalid argument to `logarithm` / `log`.

**Solution:**
- The value x must be strictly positive (x > 0).
- The base must be positive and not equal to 1 (base > 0, base != 1).

```
python -m src log -10 10    # Error: x <= 0
python -m src log 10 0      # Error: base <= 0
python -m src log 10 1      # Error: base == 1
python -m src log 10 10     # OK: 1.0
```

**Exit code:** 4

---

### "Maximum retry attempts exceeded. Session ended." (REPL only)

**Cause:** The REPL received three consecutive invalid inputs — either invalid
menu selections or non-numeric operand strings.

**Solution:** Restart the REPL with `python -m src` and provide valid inputs.
Valid menu selections are integers in the range 1–12, the word `history`, or
the word `quit`.

---

### "Usage: python -m src <operation> <operand> [operand2]"

**Cause:** The CLI was invoked with exactly one argument (which is not
`--repl`). For example: `python -m src add` with no operands.

**Solution:** Provide the operation and at least one operand. If only one
argument is needed, pass the operation name followed by the single operand:

```
python -m src factorial 5
```

**Exit code:** 1

---

## Error Logs

**Location:** `error.log` in the current working directory.

**Format:** One entry per line:

```
<ISO8601 timestamp> | <ERROR_TYPE> | input=<raw input> | <error message>
```

**Example:**

```
2024-03-15T14:23:01.456789 | CALCULATION_ERROR | input='divide 5 0' | Cannot divide by zero
2024-03-15T14:23:15.123456 | UNSUPPORTED_OPERATION | input='plus 3 4' | Unknown operation: 'plus'
2024-03-15T14:24:00.000001 | INVALID_INPUT | input='add 5' | Missing operand(s) for 'add': expected 2 operand(s), got 1
```

The error log is cleared at the start of each new session (both REPL and CLI).
To preserve errors across sessions, copy `error.log` before starting a new run.

---

## File I/O Issues

**`error.log` or `history.txt` cannot be written**

If the process lacks write permission in the current directory, the application
will print a warning to stderr but continue running:

```
Warning: could not write to error log 'error.log': [Errno 13] Permission denied
```

**Solution:** Run the application from a directory where the current user has
write access, or pre-create the files with appropriate permissions.

**Files appear in the wrong directory**

Both `error.log` and `history.txt` are written to the current working directory
at the time the application is launched — not necessarily the repository root.
Check `pwd` if you cannot find the files where expected.

---

## Environment Issues

**Wrong Python version**

The project requires Python 3.12. If you see `SyntaxError` or unexpected type
errors, confirm the version:

```
python --version
python3.12 --version
```

Use `python3.12 -m src` explicitly if your system default is a different
version.

**Virtual environment not activated**

If Python cannot find the `src` package or raises import errors, ensure the
virtual environment is active (`.venv` prefix in the shell prompt) and that you
are running from the repository root.

**Missing dependencies**

The application currently has no third-party dependencies. All imports come
from the Python standard library (`math`, `datetime`, `sys`, `dataclasses`,
`typing`). If you see `ModuleNotFoundError` for a standard library module,
your Python installation may be incomplete.

---

## Behavioral Questions

**Why does `logarithm 1000 10` return `2.9999999999999996` instead of `3.0`?**

This is expected IEEE 754 floating-point behaviour. The result is correct to
within machine epsilon. If you need a rounded display, pipe the result through
a formatting step; the calculator does not round its output.

**How do I clear the operation history without restarting?**

History is automatically cleared at the start of each new session. There is no
command within the REPL to clear history mid-session. Restart the application
to get a fresh history.

**Can I use negative exponents with `power`?**

Yes. `python -m src power 2 -1` returns `0.5`.

**Can I chain operations in CLI mode?**

No. The CLI executes a single operation per invocation. Use shell command
substitution to chain:

```
python -m src add $(python -m src multiply 3 4) 2    # (3*4) + 2 = 14.0
```
