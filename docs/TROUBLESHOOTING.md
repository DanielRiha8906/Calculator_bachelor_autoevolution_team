# Troubleshooting

---

## Interactive Session (REPL)

### The session exits with "Too many invalid attempts. Ending session."

The session terminates after `MAX_RETRIES = 5` consecutive invalid operation names.
An operation name is invalid if it is not present in the `OPERATIONS` registry.

**Resolution:** Use only the keys shown in the menu. The full list is printed before
every prompt. You can also check the available keys programmatically:

```python
from src.operations import OPERATIONS
print(list(OPERATIONS.keys()))
```

---

### The session exits early after operand input

After `MAX_RETRIES = 5` failed attempts to enter a valid operand for a single operand
slot, the current operation is aborted and the message below is printed:

```
Error: Too many invalid attempts for operand. Ending session.
```

Despite the wording, this aborts only the current operation — the session loop
continues to the next iteration.

---

### The session exits with "Goodbye!" immediately

This happens when the input source is exhausted (raises `StopIteration`). In normal
terminal use this occurs if stdin is closed. In scripted use (piping input), it means
all provided lines have been consumed.

---

### Where is history.txt written?

`history.txt` is written to the **current working directory** when you launch the
application. If you run `python -m src` from the project root, the file appears in
the project root.

---

### I typed "history" and got "No history yet."

`history` shows only operations that completed successfully in the **current session**.
If no operation has produced a result yet, the list is empty.

---

## CLI Mode (main.py)

### The command prints nothing and the exit code is 0

The result was printed to stdout. If you redirected stdout, check the output file.
If you see a non-empty stderr, an error occurred despite the exit code being 0 (this
should not happen — check whether stdout and stderr were mixed in your shell).

### The command exits with code 1 and I see "Error:" on stderr

Common causes and their error messages:

| Symptom | Likely cause |
|---------|-------------|
| `"Error: Usage: python main.py ..."` | No arguments provided |
| `"Error: Unknown operation '<op>'"` | Typo in operation name; use one of the keys listed in the error message |
| `"Error: Operation '<op>' requires N operand(s), but M were given."` | Wrong number of values after the operation name |
| `"Error: Invalid operand '<value>': expected a numeric value."` | Non-numeric string passed as operand |
| `"Error: Division by zero is not allowed."` | Second operand is `0` for `divide` |
| `"Error: square_root() is not defined for negative numbers, got <x>"` | Negative operand for `square_root` |
| `"Error: log10() is not defined for x <= 0, got <x>"` | Non-positive operand for `log10` |
| `"Error: ln() is not defined for x <= 0, got <x>"` | Non-positive operand for `ln` |
| `"Error: factorial() is not defined for negative integers, got <n>"` | Negative integer for `factorial` |
| `"Error: Invalid operand '3.5': expected a numeric value."` | Float passed to `factorial` (it requires an integer) |

---

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success — result printed to stdout |
| `1` | Any error — error message on stderr |

---

## Error Interpretation

### Domain errors

A domain error means the mathematical function is not defined for the given input.
Examples: `square_root(-1)`, `log10(0)`, `ln(-5)`, `factorial(-3)`. The error message
identifies the constraint violated.

### Division by zero

Specific to `divide`. The denominator (second operand) cannot be zero. This is
distinct from a domain error in that it raises `ZeroDivisionError` rather than
`ValueError`.

### Type errors

Currently only `factorial` raises `TypeError`. This happens if the operand is a
boolean (`True`/`False`). In CLI mode this is unreachable in practice because `int`
coercion of `"True"` raises `ValueError` first. In programmatic use of `Calculator`
directly, passing `True` raises `TypeError`.

### Invalid operands

If the raw string cannot be converted to the required type (`float` or `int`), the
error `"Invalid operand '<raw>': expected a numeric value."` is shown. This is a
coercion failure, not a mathematical domain error.

---

## Logging and error.log Inspection

`error.log` is written to the **current working directory**. Each line has the format:

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

Log levels used:

| Level | Condition |
|-------|-----------|
| `WARNING` | Unknown operation key entered (interactive mode) |
| `ERROR` | Invalid operand, wrong argument count, division by zero, domain error |

The log is never cleared automatically. To start fresh, delete or archive the file
manually:

```bash
rm error.log          # delete
mv error.log error.log.bak  # archive
```

---

## Development

### Running tests

```bash
python -m pytest
```

All tests are in the `tests/` directory. Do not delete tests to make a failing suite
pass.

### Adding a new operation

1. Add a `Calculator` method in `src/core/calculator.py`.
2. Add a registry entry in `src/operations/normal.py` (or `scientific.py` for
   scientific operations) with the correct `method`, `arity`, `label`, and optional
   `coerce` fields.
3. No changes to `InputHandler`, `CliDispatcher`, or `OperationDispatcher` are
   needed — the registry-driven dispatch handles new entries automatically.
4. Update the PlantUML diagrams in `artifacts/` to reflect the new operation.

### Modifying the session retry limit

Change the `MAX_RETRIES` constant at the top of `src/session/input_handler.py`.
Both the operation retry counter and the per-operand retry loop read this constant.
