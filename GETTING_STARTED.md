# Getting Started

## Prerequisites

- **Python 3.12** or later
- A terminal with access to `pip` and `venv`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Calculator_bachelor_autoevolution_team
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the calculator

The calculator has two modes of operation.

### Interactive mode

Launch the REPL by running the package with no arguments:

```bash
python -m src
```

The calculator prints a welcome message and a numbered list of available
operations on each prompt cycle.  You select an operation by typing its name,
then supply the requested operand(s) one at a time.

Example session:

```
Welcome to the Calculator. Press Ctrl+C or type 'exit' to quit.

Available operations:
  add: Addition (a + b)
  subtract: Subtraction (a - b)
  multiply: Multiplication (a * b)
  divide: Division (a / b)
  power: Power (x ^ y)
  factorial: Factorial (n!)
  square: Square (x^2)
  cube: Cube (x^3)
  square_root: Square root (√x)
  cube_root: Cube root (∛x)
  log: Base-10 logarithm (log₁₀ x)
  ln: Natural logarithm (ln x)
  exit / quit: Exit the calculator
Select an operation: add
Enter first operand: 3
Enter second operand: 5
Result of Addition (a + b)(3.0, 5.0) = 8.0
```

#### Viewing operation history

Type `history` at the operation selection prompt to print all operations
performed in the current session:

```
Select an operation: history
1. add(3.0, 5.0) = 8.0
2. square_root(16.0) = 4.0
```

History is stored in `history.txt` and is cleared automatically at the start
of each new session.

#### Exiting interactive mode

- Type `exit` or `quit` at the operation prompt, or
- Press `Ctrl+C` at any prompt.

Both print `Goodbye!` and terminate cleanly.

#### MaxRetries termination

The interactive session allows up to **3 consecutive invalid inputs** per
prompt (operation selection or operand entry).  Once all attempts are
exhausted the message `Maximum retry attempts reached. Session ended.` is
printed and the session ends without an error code.

### CLI mode

Pass the operation name and its operands as command-line arguments for a
single-expression execution:

```bash
python -m src <operation> <operand> [<operand> ...]
```

The result is printed to stdout and the process exits with code 0 on success,
or code 1 with an `Error: ...` message on stderr on failure.

Examples:

```bash
python -m src add 3 5          # prints: 8
python -m src subtract 10 4    # prints: 6
python -m src multiply 7 6     # prints: 42
python -m src divide 9 3       # prints: 3
python -m src power 2 10       # prints: 1024
python -m src factorial 7      # prints: 5040
python -m src square 9         # prints: 81
python -m src cube 3           # prints: 27
python -m src square_root 144  # prints: 12
python -m src cube_root 27     # prints: 3
python -m src log 1000         # prints: 3.0
python -m src ln 1             # prints: 0.0
```

Error example:

```bash
python -m src divide 5 0
# stderr: Error: division by zero
# exit code: 1
```

## Running tests

```bash
pytest tests/
```
