# Session Behaviour

This document describes how a calculator session is created, what state it maintains, how history is managed, how errors are handled and logged, and how input validation behaves across runtime modes.

---

## Session Lifecycle

A session begins when `interactive_session(calculator)` in `src/cli.py` is called. That function creates a `CalculatorSession` instance (defined in `src/session.py`), which in turn creates an `OperationHistory` and an `ErrorLogger`. The session runs until:

- the user types `quit`, `exit`, or `q`;
- the retry limit for invalid operation selection or operand input is exceeded; or
- CLI mode receives invalid input and raises `SystemExit`.

On any normal exit path, `session.save_history("history.txt")` is called before termination, writing the in-memory history to disk.

### Session state

`CalculatorSession` holds:

- `_calculator` — the `Calculator` instance passed at construction.
- `_history` — an `OperationHistory` instance tracking successful operations.
- `_error_logger` — an `ErrorLogger` instance writing to `error.log`.
- `_operation_list` — a cached list of public operation names, refreshed on each loop iteration.

---

## History Management

### Recording

A history entry is created only when an operation completes without error. The call `session.record_history(op_name, operands, result)` delegates to `OperationHistory.record_operation`, which appends a formatted string to an in-memory list.

### Entry format

Entries follow the pattern:

```
operation_name(arg1, arg2, ...) = result
```

Whole-number floats are collapsed to integers in the display. For example:

```
add(2, 3) = 5
divide(7, 2) = 3.5
square_root(9) = 3
```

### Persistence

When the session ends, `save_to_file("history.txt")` writes every entry to `history.txt` in the current working directory, one entry per line. If the history is empty, an empty file is created (or an existing file is truncated). The file is opened in write mode, so only the current session's history is stored.

### Session scope

History is held in memory for the duration of one process run. There is no mechanism to load history from a previous session; each run starts with an empty history.

---

## Error Handling and Logging

### Log file

`ErrorLogger` writes to `error.log` (in the current working directory by default). The file is opened in **append mode**, so records from previous sessions accumulate rather than being overwritten.

### Log record format

```
YYYY-MM-DD HH:MM:SS,mmm [ERROR] CATEGORY | field='value' ...
```

For example:

```
2026-04-22 10:05:33,412 [ERROR] DIVISION_BY_ZERO | numerator=10.0
2026-04-22 10:05:45,001 [ERROR] INVALID_DOMAIN | operation='square_root' operand=-4.0 reason='x must be non-negative for square root'
```

### Logged categories

| Category | Method | Captured when |
|---|---|---|
| `UNSUPPORTED_OPERATION` | `log_unsupported_operation(operation_name)` | User enters an operation name that is not found on the calculator. |
| `INVALID_OPERAND` | `log_invalid_operand(operand, reason)` | A non-numeric string is entered as an operand; also logged when the interactive retry limit is exceeded. |
| `INCORRECT_ARITY` | `log_incorrect_arity(operation_name, expected, got)` | Mismatch between expected and supplied argument count. |
| `DIVISION_BY_ZERO` | `log_division_by_zero(numerator)` | A `ZeroDivisionError` is caught during `execute_operation`. |
| `INVALID_DOMAIN` | `log_invalid_domain(operation_name, operand, reason)` | A `ValueError` is caught during `execute_operation` (e.g. negative input to `square_root`). |

### User-visible errors vs. silent log entries

The logger has no console handlers and does not call `print`. Every log entry is written silently to `error.log`. The user-facing error message is returned separately by `execute_operation` as a plain string and displayed by the CLI as `  Error: <message>`.

---

## Retry Semantics

Input validation is managed by `OperandValidationSession` and `OperationValidationSession` in `src/validation.py`. Both classes share the same retry logic, controlled by `_MAX_RETRIES_DEFAULT = 5`.

### Interactive mode (TTY detected)

- On each invalid input, an error message is printed and the counter increments.
- After 5 consecutive failures the session prints a termination message and returns `None`.
- The counter resets to zero after each successful input.

### CLI mode (non-TTY / piped input)

- The first invalid input immediately raises `SystemExit` with a descriptive message.
- No retries are performed.

### Mode detection

`detect_mode()` in `src/validation.py` returns `'interactive'` if `sys.stdin.isatty()` is `True`, and `'cli'` otherwise. The CLI calls this once at the start of `interactive_session` and passes the result through to all validation sessions.

---

## Data Isolation

- **History** is session-scoped: each process run starts with an empty `OperationHistory`. The saved `history.txt` is overwritten (not appended) on each quit.
- **Error log** is append-only: `error.log` accumulates records across all sessions indefinitely.
- **No shared state** exists between concurrent sessions; `CalculatorSession` instances are independent.
