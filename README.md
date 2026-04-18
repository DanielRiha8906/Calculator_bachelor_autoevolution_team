# Calculator — Self-Evolving Software Prototype

A command-line calculator implemented in Python 3.12 as part of a bachelor thesis on self-evolving software. The project demonstrates a clean two-layer architecture (Calculation Layer and Interaction Layer) and supports both an interactive menu-driven mode and a non-interactive CLI mode.

---

## Features

The calculator supports twelve mathematical operations:

**Arithmetic (binary)**
- `add` — addition (a + b)
- `subtract` — subtraction (a - b)
- `multiply` — multiplication (a * b)
- `divide` — division (a / b); raises an error on division by zero

**Exponents and powers (unary/binary)**
- `power` — exponentiation (base ^ exponent); binary
- `square` — square of a number (x^2); unary
- `cube` — cube of a number (x^3); unary
- `factorial` — factorial of a non-negative integer (n!); unary; integer input only

**Roots (unary)**
- `square_root` — square root (sqrt(x)); x must be non-negative
- `cube_root` — cube root (cbrt(x)); all real numbers supported

**Logarithms (unary)**
- `log` — base-10 logarithm (log10(x)); x must be positive
- `ln` — natural logarithm (ln(x)); x must be positive

See `FEATURES.md` for full per-operation documentation including error conditions.

---

## Installation and Setup

**Requirements:** Python 3.12

```bash
# Clone the repository
git clone <repo-url>
cd Calculator_bachelor_autoevolution_team

# Create and activate a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Interactive mode (no arguments)

Run without any arguments to start the menu-driven REPL:

```bash
python -m src
```

The program prints a menu of all available operations on each iteration. Type the operation name at the prompt, then enter the required operand(s) when prompted.

**Special commands in interactive mode:**
- `history` — display all operations performed in the current session
- `exit` — quit the calculator

**Example session:**

```
Available operations:
  add          - Add (a + b)
  subtract     - Subtract (a - b)
  multiply     - Multiply (a * b)
  divide       - Divide (a / b)
  power        - Power (base ^ exponent)
  factorial    - Factorial (n!)
  square       - Square (x^2)
  cube         - Cube (x^3)
  square_root  - Square root (sqrt(x))
  cube_root    - Cube root (cbrt(x))
  log          - Log base-10 (log10 x)
  ln           - Natural logarithm (ln x)
  history      - View operation history
  exit         - Quit the calculator

Enter operation: add
Enter operand 1: 3
Enter operand 2: 5
Result: 8.0

Enter operation: square_root
Enter operand: 16
Result: 4.0

Enter operation: history
3.0 add 5.0 = 8.0
square_root(16.0) = 4.0

Enter operation: exit
Goodbye!
```

### Retry logic

In interactive mode, if an invalid operation or non-numeric operand is entered, the program re-prompts up to 3 times before terminating the session (for invalid operations) or returning to the main menu (for invalid operands).

### CLI mode (operation and operands as arguments)

Pass the operation name followed by its operands directly on the command line:

```bash
python -m src <operation> <operand1> [operand2]
```

The result is printed to stdout. Errors are printed to stderr with exit code 2.

**CLI examples:**

```bash
# Binary operations (two operands)
python -m src add 3 5          # Output: 8.0
python -m src subtract 10 4    # Output: 6.0
python -m src multiply 6 7     # Output: 42.0
python -m src divide 10 2      # Output: 5.0
python -m src power 2 8        # Output: 256.0

# Unary operations (one operand)
python -m src factorial 5      # Output: 120.0
python -m src square 4         # Output: 16.0
python -m src cube 3           # Output: 27.0
python -m src square_root 9    # Output: 3.0
python -m src cube_root 27     # Output: 3.0
python -m src log 100          # Output: 2.0
python -m src ln 1             # Output: 0.0
```

**CLI error examples:**

```bash
python -m src divide 10 0
# stderr: error: Division by zero is not allowed
# exit code: 2

python -m src square_root -4
# stderr: error: square_root requires a non-negative number, got -4.0
# exit code: 2

python -m src add 3
# stderr: error: operation 'add' requires 2 operand(s), but 1 were supplied.
# exit code: 2
```

---

## Project Structure

```
src/
  __init__.py         — package initializer
  __main__.py         — entry point; routes to CLI or interactive mode
  calculator.py       — Calculation Layer: Calculator class; pure computation, no I/O
  cli.py              — Interaction Layer: CLI argument parsing and dispatch (run_cli)
  input_loop.py       — Interaction Layer: interactive REPL, menu, retry logic (run_loop)
  history.py          — Interaction Layer service: OperationHistory; records to history.txt
  error_logger.py     — Interaction Layer service: ErrorLogger; records to error.log
  validation.py       — Interaction Layer: validate_operation and validate_operand helpers
  operations/
    __init__.py       — subpackage initializer (no public exports)
    arithmetic.py     — add, subtract, multiply, divide
    exponents.py      — power, factorial, square, cube
    roots.py          — square_root, cube_root
    logarithmic.py    — log, ln
```

### Architecture

The codebase is split into two layers:

- **Calculation Layer** (`calculator.py` + `operations/`): pure arithmetic, no I/O or user interaction. `Calculator` is a delegation wrapper; each method calls the corresponding function in the `operations` subpackage.
- **Interaction Layer** (`cli.py`, `input_loop.py`, `history.py`, `error_logger.py`, `validation.py`): handles all user-facing behaviour — argument parsing, menu display, input validation, retry logic, history recording, and error logging.

---

## Testing

Run the full test suite with:

```bash
python -m pytest
```

Tests live alongside source code in the `tests/` directory and cover unit tests for all Calculator methods, validation logic, retry behaviour, history recording, error logging, and integration tests for both interactive and CLI modes.

---

## Diagrams

PlantUML architecture and flow diagrams are maintained in `artifacts/`:

- `artifacts/class_diagram.puml` — class and module structure with layer boundaries
- `artifacts/activity_diagram.puml` — full activity flow for both interactive and CLI modes
- `artifacts/sequence_diagram.puml` — participant interaction sequences for key scenarios
