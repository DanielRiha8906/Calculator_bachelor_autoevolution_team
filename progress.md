## Run: Issue #11 — TestSuite (task/issue-11-test-suite) — 2026-04-16

**Branch:** task/issue-11-test-suite → PR target: exp/structured-team

**Files changed:**
- `tests/test_calculator.py` — appended 16 new test functions covering add, subtract, multiply, divide operations

**Purpose:** Create a comprehensive unit test suite for the Calculator class covering all 4 arithmetic operations with happy-path and edge-case tests (zero operands, negative numbers, floats, large values, invalid types, division by zero).

**Risks:** Low. Test-only change; no production code modified.

**Test results:** 21 passed, 0 failed — `python -m pytest tests/test_calculator.py -v`

**Tokens used:** PENDING
**Estimated cost:** PENDING
**Turns:** PENDING

---

## Run: Issue #8 — ZeroDivisionError (task/issue-8-zero-division-error) — 2026-04-16

**Branch:** task/issue-8-zero-division-error → PR target: exp/structured-team

**Files changed:**
- `src/calculator.py` — added `ValueError` guard to `Calculator.divide` when `b == 0`
- `tests/test_calculator.py` — added `test_divide_by_zero_raises_value_error` and `test_divide_happy_path`

**Purpose:** Handle division by zero explicitly in the calculator. Previously the method performed bare `a / b`, raising Python's native `ZeroDivisionError`. Now raises `ValueError("Division by zero is not allowed")` when `b == 0`.

**Risks:** Low. Change is fully self-contained; no other code calls `Calculator.divide` outside tests.

**Test results:** 2 passed, 0 failed — `python -m pytest -v`

**Tokens used:** ~88,300 (across 4 agents)
**Estimated cost:** ~$0.09 USD
**Turns:** 4 agent invocations (analyst → architect → implementer → tester)
