# User Guide

This guide explains how to install, run, and interact with the Calculator application.

---

## Installation and Setup

**Requirements:** Python 3.12 or later.

1. Clone the repository and navigate to its root directory.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Calculator

Start the interactive session with:

```bash
python -m src
```

The application launches a menu-driven REPL (Read-Eval-Print Loop). On each iteration it prints the numbered list of available operations, prompts for a selection, collects any required operands, and displays the result.

---

## Supported Operations

The following operations are available:

| # | Operation | Description | Operands |
|---|---|---|---|
| 1 | `add` | Sum of two numbers | 2 |
| 2 | `cube` | Cube of a number (x³) | 1 |
| 3 | `cube_root` | Real-valued cube root (∛x) | 1 |
| 4 | `divide` | Quotient of two numbers | 2 |
| 5 | `factorial` | Factorial of a non-negative integer (n!) | 1 |
| 6 | `logarithm` | Base-10 logarithm | 1 |
| 7 | `multiply` | Product of two numbers | 2 |
| 8 | `natural_logarithm` | Natural logarithm (ln) | 1 |
| 9 | `power` | Base raised to an exponent | 2 |
| 10 | `square` | Square of a number (x²) | 1 |
| 11 | `square_root` | Square root of a non-negative number | 1 |
| 12 | `subtract` | Difference of two numbers (a - b) | 2 |

**Input format:** operands are entered as numeric values (integers or decimals, e.g. `3`, `3.14`, `-7`).

**Output format:** results are displayed as `  Result: <value>`.

---

## Examples

### Add two numbers

```
Available operations:
  1. add
  ...

Select operation (name or number): add
  Enter operand 1: 12
  Enter operand 2: 8
  Result: 20.0
```

### Divide two numbers

```
Select operation (name or number): divide
  Enter operand 1: 15
  Enter operand 2: 4
  Result: 3.75
```

### Square a number

```
Select operation (name or number): square
  Enter operand 1: 7
  Result: 49.0
```

### Viewing history

Type `history` or `h` at the operation prompt:

```
Select operation (name or number): history

Operation history:
  add(12, 8) = 20
  divide(15, 4) = 3.75
  square(7) = 49
```

### Quitting the session

Type `quit`, `exit`, or `q` at the operation prompt:

```
Select operation (name or number): q
Goodbye!
```

The session history is saved to `history.txt` in the current working directory before the program exits.

---

## Session Behaviour

- **Each run is independent.** History is not loaded from previous sessions.
- **History is saved on quit.** When the session ends normally (via `quit`/`exit`/`q` or after exceeding the retry limit), the operation history is written to `history.txt`.
- **Errors are logged silently.** Invalid inputs and domain errors are recorded in `error.log` but no traceback is shown to the user. The user sees a concise `  Error: <message>` line.
- **Retry on invalid input (interactive mode).** If you enter a non-numeric operand or an unrecognised operation, the application re-prompts you. After 5 consecutive failures the session terminates automatically.
