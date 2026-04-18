# Session Behavior

This document describes the interactive session driven by `InputHandler` in
`src/session/input_handler.py`. For the activity diagram see
[`artifacts/activity_diagram.puml`](../artifacts/activity_diagram.puml).

---

## InputHandler Class Overview

`InputHandler` is the REPL controller for the calculator. It owns:

- A reference to a `Calculator` instance (passed at construction time).
- An `OperationDispatcher` (created in `__init__`), which handles operand coercion
  and method dispatch.
- A `History` instance (created in `__init__`), which accumulates successful
  operations during the session.
- An optional `Logger` instance; if `None` at construction, one is created lazily
  on the first call to `run()`.
- An `input_fn` callable (defaults to `builtins.input`), injectable for testing.

```python
handler = InputHandler(
    calculator=Calculator(),
    input_fn=None,   # defaults to built-in input()
    logger=None,     # defaults to Logger() created lazily in run()
)
handler.run()
```

The convenience function `run_session(calculator, input_fn=None, logger=None)` creates
an `InputHandler` and calls `run()` in one step. This is the function called by
`src/__main__.py`.

---

## Session Flow

```
run()
├─ Create Logger() if not provided
├─ op_attempts = 0
└─ loop:
    ├─ _show_menu()                          # print OPERATIONS to stdout
    ├─ prompt: "Enter operation (or 'exit'/'quit' to stop):"
    │
    ├─ if input == "exit" or "quit"  →  print "Goodbye!" and break
    │
    ├─ if input == "history"
    │   ├─ print all history entries, or "No history yet."
    │   └─ continue
    │
    ├─ if input not in OPERATIONS
    │   ├─ op_attempts += 1
    │   ├─ logger.log_unsupported_operation(op_choice)
    │   ├─ print "Error: Unknown operation '<op>'. Please choose from the menu."
    │   ├─ print "Available operations: ..."
    │   └─ if op_attempts >= MAX_RETRIES  →  print "Too many invalid attempts. Ending session." and break
    │
    └─ if input in OPERATIONS
        ├─ op_attempts = 0
        ├─ look up arity and coerce from OPERATIONS
        ├─ _prompt_operands(arity, coerce)       # see Operand Collection below
        ├─ if ValueError from _prompt_operands   →  print "Error: <exc>"; continue
        ├─ _dispatch(op_choice, operands)
        │   └─ OperationDispatcher.dispatch()
        │       └─ Calculator.<method>(*operands)
        ├─ if ZeroDivisionError  →  log + print "Error: Division by zero is not allowed."
        ├─ if ValueError         →  log + print "Error: <exc>"
        ├─ if TypeError          →  log + print "Error: <exc>"
        └─ else                  →  print "Result: <result>"; history.add_operation(...)

finally (always, even on early exit):
    history.save_to_file("history.txt")
```

---

## Retry Logic

`MAX_RETRIES = 5` is a module-level constant in `src/session/input_handler.py`.

### Operation retry

The counter `op_attempts` increments each time the user enters an operation key not
found in `OPERATIONS`. It resets to `0` when a valid key is entered. When
`op_attempts >= MAX_RETRIES` the session terminates with:

```
Too many invalid attempts. Ending session.
```

### Operand retry

Inside `_prompt_operands`, each operand position gets up to `MAX_RETRIES` independent
attempts. If the user provides an invalid value (cannot be coerced to the expected
type), the error is printed and the same operand is prompted again. After `MAX_RETRIES`
failures for a single operand slot, a `ValueError` is raised with the message:

```
Too many invalid attempts for operand. Ending session.
```

This `ValueError` is caught in `run()` and prints:

```
Error: Too many invalid attempts for operand. Ending session.
```

The session then continues to the next iteration (it does not terminate the whole
session, unlike the operation retry which does break the loop). Note that the
phrasing "Ending session" in the operand message is slightly misleading — it aborts
the current operation but not the session itself.

---

## Operation Menu Display

`_show_menu()` is called at the start of every loop iteration. It prints all entries
from `OPERATIONS` in insertion order:

```
Available operations:
  add            — Add two numbers
  subtract       — Subtract two numbers
  multiply       — Multiply two numbers
  divide         — Divide two numbers
  power          — Raise a number to a power
  factorial      — Factorial of a non-negative integer
  square         — Square a number (x^2)
  cube           — Cube a number (x^3)
  square_root    — Square root of a number
  cube_root      — Cube root of a number
  log10          — Base-10 logarithm of a number
  ln             — Natural logarithm of a number
```

---

## Operand Collection and Validation

`_prompt_operands(arity, coerce)` collects the required number of operands.

- For **arity 2** operations, the labels are `"first"` and `"second"`:
  ```
  Enter first operand: 
  Enter second operand: 
  ```
- For **arity 1** operations, no label is prepended:
  ```
  Enter operand: 
  ```

Each operand value is passed to `OperationDispatcher.coerce_operands([raw], coerce)`.
The `coerce` callable is taken from the operation's registry entry (defaults to
`float`; `factorial` uses `int`).

A `ValueError` from coercion prints `"Error: Invalid operand '<raw>': expected a
numeric value."` and retries the same operand (up to `MAX_RETRIES` times).

---

## History Tracking

After each **successful** dispatch, the result is recorded:

```python
history.add_operation(op_choice, operands, result)
```

Entries are formatted as:

```
operation(arg1, arg2, ...) = result
```

Examples:
```
add(10.0, 5.0) = 15.0
factorial(6) = 720
square_root(16.0) = 4.0
```

During a session, the user can view history at any time by entering `history` at the
operation prompt. The session prints all entries, or `"No history yet."` if none exist.

---

## File Outputs

### history.txt

Written by `History.save_to_file("history.txt")` in the `finally` block of `run()`.
This means it is always written — even if the session ends due to too many retries or
a `StopIteration` from an exhausted input source.

- **Location:** current working directory when the process runs.
- **Format:** one history entry per line in function-call notation.
- **Behavior:** created or overwritten each session (not appended).
- **On empty session:** an empty file is created.

### error.log

Written by `Logger` throughout the session whenever an error event occurs. Never
truncated — entries accumulate across all runs.

- **Location:** current working directory when the process runs.
- **Format:** `YYYY-MM-DD HH:MM:SS LEVEL message`
- **Entries logged:**
  - `WARNING`: unsupported operation key entered
  - `ERROR`: invalid operand value, argument count mismatch, division by zero, domain error

---

## Error Handling Per Operation Type

| Error Type | Source | Session Action | Logged |
|------------|--------|---------------|--------|
| Unknown operation key | User input | Print error; increment `op_attempts`; retry | Yes (WARNING) |
| Invalid operand (coercion failure) | User input | Print error; retry operand up to `MAX_RETRIES` | Yes (ERROR) |
| Division by zero | `Calculator.divide` | Print `"Error: Division by zero is not allowed."` | Yes (ERROR) |
| Domain error (`ValueError`) | `Calculator.*` | Print `"Error: <exc>"` | Yes (ERROR) |
| Type error (`TypeError`) | `Calculator.factorial` | Print `"Error: <exc>"` | Yes (ERROR) |
| Input exhausted (`StopIteration`) | `input_fn` | Print `"Goodbye!"`; break loop cleanly | No |
