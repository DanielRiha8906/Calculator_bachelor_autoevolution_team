# CLI Reference

This document describes how to invoke the Calculator from the command line and how the application behaves in interactive and non-interactive (piped) modes.

---

## Bash CLI Invocation

```bash
python -m src
```

This is the only supported invocation method. The application does not accept positional arguments or flags.

### Mode detection

On startup, `detect_mode()` in `src/validation.py` calls `sys.stdin.isatty()`:

- `True` → **interactive mode** (user is at a terminal).
- `False` → **CLI mode** (stdin is a pipe, redirect, or file).

The detected mode is passed to all validation sessions and governs retry and fast-fail behaviour throughout the session.

---

## Interactive Mode Behaviour

When stdin is a TTY, the application enters interactive mode:

- A numbered operation menu is printed on each loop iteration.
- The user selects an operation by name or number.
- Operands are entered one at a time.
- **On invalid operation input:** an error message is printed and the user is re-prompted. After 5 consecutive failures the session terminates with a termination message and history is saved.
- **On invalid operand input:** an error message is printed and the user is re-prompted for the same operand. After 5 consecutive failures for a single operand the session terminates.
- The retry counter resets to zero after each successful input.

---

## CLI Mode Behaviour (Non-TTY / Piped Input)

When stdin is not a TTY (e.g. input is piped or redirected), the application enters CLI mode:

- **Fast-fail on first invalid input:** if an operand cannot be parsed as a float, `SystemExit` is raised immediately with a descriptive message. No retry is attempted.
- **Invalid operation:** `SystemExit` is raised with a message listing available operations.
- The exit code is non-zero when `SystemExit` is raised.

CLI mode is intended for batch processing, scripted use, and automated testing.

---

## Example Bash Usage

### Running interactively

```bash
python -m src
```

The application prints the menu and waits for keyboard input.

### Piping input

Provide newline-separated values on stdin. The first line is the operation selection, followed by one line per operand:

```bash
printf "add\n3\n7\n" | python -m src
```

Because stdin is not a TTY, the application runs in CLI mode: it reads one value per prompt and exits with an error if any value is invalid.

### Checking exit codes

```bash
printf "divide\n10\n0\n" | python -m src
echo "Exit code: $?"
```

A `ZeroDivisionError` will be returned as an error message; the process exits with code `0` because the error is handled by the application. An unparseable operand causes `SystemExit` and a non-zero exit code:

```bash
printf "add\nnotanumber\n" | python -m src
echo "Exit code: $?"   # non-zero
```
