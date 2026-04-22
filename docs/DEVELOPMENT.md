# Development Guide

This guide covers environment setup, adding operations, testing strategy, code style, and Git workflow for contributors to the Calculator project.

---

## Development Environment Setup

### Prerequisites

- Python 3.12
- `pip` and `venv` (both included with Python 3.12)
- Git

### Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd Calculator_bachelor_autoevolution_team

# 2. Create and activate a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate.bat       # Windows cmd
.venv\Scripts\Activate.ps1       # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Interactive REPL
python -m src.main

# Single expression (CLI mode)
python -m src.main "add 5 3"
```

---

## Running Tests

Tests use `pytest`. Run the full suite from the repository root:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_logic.py
```

Run with verbose output:

```bash
pytest -v
```

Collect but do not execute tests (useful for verifying test discovery):

```bash
pytest --collect-only
```

Do not delete or skip tests to make a failing suite pass. If a test must be skipped temporarily, mark it with `@pytest.mark.skip` and add a comment explaining why and what needs to change before it can be re-enabled.

---

## Adding a New Basic Operation

Basic operations live in `src/modes/basic.py` and are dispatched through `CalculatorEngine` and `Calculator`.

### Step 1 — Register the name

In `src/modes/operations.py`, add the operation name to `BASIC_OPERATIONS`:

```python
BASIC_OPERATIONS: frozenset[str] = frozenset(
    {"add", "subtract", "multiply", "divide", "modulo"}  # new: modulo
)
```

### Step 2 — Implement the method on BasicOperations

In `src/modes/basic.py`, add a method to `BasicOperations`:

```python
def modulo(self, a: Numeric, b: Numeric) -> Numeric:
    """Return the remainder of *a* divided by *b*.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        ``a % b``.

    Raises:
        ZeroDivisionError: If *b* is zero.
    """
    result = a % b
    self._record(result)
    return result
```

Register it in `get_operations()`:

```python
def get_operations(self) -> dict[str, Callable]:
    return {
        "add": self.add,
        "subtract": self.subtract,
        "multiply": self.multiply,
        "divide": self.divide,
        "modulo": self.modulo,   # new
    }
```

### Step 3 — Forward through CalculatorEngine

In `src/logic.py`, add a method on `CalculatorEngine`:

```python
def modulo(self, a, b):
    result = self._basic.modulo(a, b)
    self._record_history(a, "modulo", b, result)
    return result
```

### Step 4 — Forward through Calculator

In `src/calculator.py`, add a forwarding method on `Calculator`:

```python
def modulo(self, a, b):
    return self._engine.modulo(a, b)
```

### Verification

Because `BASIC_OPERATIONS` is the single source of truth consumed by `InputValidator` and `CalculatorREPL`, no changes to the input layer are needed. Confirm the operation is available at the REPL prompt:

```
> modulo 10 3
Result: 1
```

---

## Adding a New Advanced Operation

Advanced operations live in `src/modes/advanced.py`. Follow the same four-step process as for basic operations, substituting `ADVANCED_OPERATIONS` and `AdvancedOperations`.

### Arity consideration

The input layer in `src/input_handler.py` automatically classifies operations into unary or binary groups:

```python
_ONE_OPERAND_OPS = frozenset(ADVANCED_OPERATIONS - {"power"})
_TWO_OPERAND_OPS = frozenset(BASIC_OPERATIONS | {"power"})
```

- If the new operation is **unary** (one operand), add it to `ADVANCED_OPERATIONS` and it will automatically appear in `_ONE_OPERAND_OPS`.
- If the new operation is **binary** (two operands), add it to `ADVANCED_OPERATIONS` **and** also add it to `_TWO_OPERAND_OPS` by listing it explicitly in `input_handler.py` alongside `"power"`.

---

## Testing Strategy

The goal is correctness of the computation and input pipeline, not coverage metrics.

### What to test

- Each operation with valid inputs (happy path).
- Each operation with inputs at domain boundaries (e.g. `factorial 0`, `square_root 0`, `divide 1 very_small`).
- Each operation with invalid inputs that should raise an exception (`divide 1 0`, `square_root -1`, `factorial -1`, `factorial 5.0`).
- `ExpressionParser.parse` with empty input, one token, two tokens, three tokens, non-numeric operands.
- `InputValidator.validate_operation` with unknown names.
- `InputValidator.validate_operand_count` with wrong counts.
- `CalculatorEngine.get_history` — verify that each call appends exactly one record with correct keys.
- `Calculator.set_mode` — verify that history is cleared after the call.

### What not to test

- Implementation details of `BasicOperations._record` or `AdvancedOperations._record` — these are private.
- The exact log message format — log content may change without notice.

---

## Code Style Conventions

The project follows PEP 8 with these conventions already present in the codebase:

- **Type hints on all public function signatures.** Use `Union[int, float]` where both are acceptable; use `float` for functions that always return a float.
- **Small, single-purpose functions.** Each method does one thing. If a helper is needed, add a private method (prefixed `_`) rather than making the public method longer.
- **Explicit, readable Python over compact clever code.** Prefer a plain `for` loop with a clear variable name over a one-liner that requires a comment to explain.
- **Google-style docstrings** with `Args:`, `Returns:`, and `Raises:` sections on all public methods.
- **No bare `except:` clauses.** Always name the exception type.
- **Imports in order:** stdlib, then third-party, then intra-package relative imports. Use `from __future__ import annotations` at the top of any module that needs it.
- **Composition over inheritance** for operation classes. `BasicOperations` and `AdvancedOperations` extend `BaseOperationSet` only because the abstract contract requires it; they do not share state through inheritance.

---

## Git Workflow

- **One concern per commit.** Do not mix a bug fix with a refactor in the same commit.
- **Atomic commits.** Stage only the files relevant to the change (`git add -p` for partial staging).
- **Commit messages:** imperative mood, present tense, 72-character subject limit. Body explains *why*, not *what*.
- **Branch per feature or fix:** `feature/<short-description>` or `fix/<short-description>`.
- **Never commit directly to `main`.** Open a pull request and request review.
- **Never amend a published commit.** If a correction is needed after pushing, make a new commit.

Example commit message:

```
Add modulo operation to BasicOperations

Modulo is a frequently requested operation that fits naturally alongside
the existing four arithmetic methods. Added to BASIC_OPERATIONS so the
input layer picks it up automatically.
```
