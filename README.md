# Calculator — Self-Evolving Software Prototype

This repository is the practical implementation component of a bachelor thesis on
**self-evolving software**: a system capable of autonomously modifying its own source
code. The calculator application serves as the subject program that the self-evolution
engine operates on.

---

## Requirements

- Python 3.12
- pip (for dependency installation)

## Installation and Setup

```bash
# Clone the repository
git clone <repository-url>
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

The application supports two interaction modes: a **guided interactive session** and a
**single-shot CLI** invocation.

### Mode 1 — Guided Interactive Session

Launch the REPL-style session using the package entry point:

```bash
python -m src
```

The session prints an operation menu, then prompts for an operation name and its
operands in a loop. Type `exit` or `quit` to end the session.

**Example session:**

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

Enter operation (or 'exit'/'quit' to stop): add
Enter first operand: 10
Enter second operand: 5
Result: 15.0

Enter operation (or 'exit'/'quit' to stop): factorial
Enter operand: 6
Result: 720

Enter operation (or 'exit'/'quit' to stop): quit
Goodbye!
```

You can also type `history` at the operation prompt to print all operations performed
in the current session.

### Mode 2 — Single-Shot CLI

Pass the operation and operands directly as command-line arguments to `main.py`:

```bash
python main.py <operation> <operand1> [<operand2>]
```

**Examples:**

```bash
# Binary operations
python main.py add 5 7          # prints: 12.0
python main.py subtract 10 3    # prints: 7.0
python main.py multiply 4 8     # prints: 32.0
python main.py divide 10 4      # prints: 2.5
python main.py power 2 10       # prints: 1024.0

# Unary operations
python main.py factorial 6      # prints: 720
python main.py square 9         # prints: 81.0
python main.py square_root 16   # prints: 4.0
python main.py cube_root 27     # prints: 3.0
python main.py log10 1000       # prints: 3.0
python main.py ln 1             # prints: 0.0
```

Results are written to **stdout**. Errors are written to **stderr** and the process
exits with code `1`.

---

## Session Files

After an interactive session ends, two files may be created or updated in the working
directory:

| File | Purpose |
|------|---------|
| `history.txt` | One-line record per successful operation, in function-call notation: `add(10.0, 5.0) = 15.0`. Created or overwritten each session. |
| `error.log` | Cumulative log of error events across all runs (unsupported operations, invalid operands, domain errors, division by zero). Never truncated. |

The CLI mode writes to `error.log` on error but does not produce `history.txt`.

---

## Troubleshooting

**Session exits before I finish entering operations**
The session terminates automatically after 5 consecutive invalid operation names or
after 5 consecutive invalid operand inputs for a single operand. See
[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for details.

**CLI prints nothing to stdout**
Check stderr for the error message. Common causes: unknown operation name, wrong
number of operands, or a domain error (e.g. square root of a negative number).

**`error.log` grows indefinitely**
This is by design — the log accumulates across runs for research reproducibility.
Delete or archive it manually when it is no longer needed.

---

## Extended Documentation

| Document | Contents |
|----------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Module layout, data flow, design patterns |
| [docs/MODULES.md](docs/MODULES.md) | Per-module reference: classes, public interfaces, error conditions |
| [docs/OPERATIONS_REFERENCE.md](docs/OPERATIONS_REFERENCE.md) | Every supported operation with examples and error conditions |
| [docs/SESSION_BEHAVIOR.md](docs/SESSION_BEHAVIOR.md) | Interactive session flow, retry logic, history and logging |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common problems and solutions |

PlantUML diagrams are in [artifacts/](artifacts/).

---

## Running Tests

```bash
python -m pytest
```
