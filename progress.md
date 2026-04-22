## Run: Issue #234 — Division-by-zero unit tests

- **Branch:** task/issue-234-division-by-zero
- **PR target:** exp2/structured-team
- **PR:** https://github.com/DanielRiha8906/Calculator_bachelor_autoevolution_team/pull/300

### Files changed

- `tests/test_calculator.py` — added 12 tests covering divide-by-zero (primary requirement), normal divide paths, and basic operation smoke tests

### Files unchanged

- `src/calculator.py` — no changes required; existing `divide(a, b)` already raises `ZeroDivisionError` natively

### Purpose

Add explicit unit test coverage for division-by-zero behavior in the Calculator class, as required by Issue #234.

### Risks

None. Additive test-only change; no production code modified.

### Test results

All 12 tests passed. No regressions.

Duration: 155.9s | Cost: $0.367521 USD | Turns: 15

Duration: 175.0s | Cost: $0.392449 USD | Turns: 12

## Run: Issue #237 — V2 Task 2 Structured/team unit test suite

- **Branch:** task/issue-237-unit-test-suite
- **PR target:** exp2/structured-team

### Files changed

- `tests/test_calculator.py` — expanded `TestCalculatorBasicOperations` class with 19 new test methods covering addition (5), subtraction (7), and multiplication (7) operations

### Files unchanged

- `src/calculator.py` — no changes; tests validate existing behavior only

### Purpose

Add comprehensive unit test coverage for add, subtract, and multiply operations per Issue #237. Division tests already existed; this completes the suite for all four arithmetic operations.

### Risks

None. Additive test-only change; no production code modified.

### Test results

All 28 tests passed (19 new + 9 existing division tests). No regressions. Operations covered: add, subtract, multiply, divide. Edge cases: zero operands, negative numbers, large numbers, floating-point precision (pytest.approx).

Duration: 180.1s | Cost: $0.405448 USD | Turns: 14

Duration: 151.4s | Cost: $0.392515 USD | Turns: 15

## Run: Issue #240 — V2 Task 3 - Structured/team (2026-04-22)

- **Branch:** task/issue-240-factorial-operation
- **PR target:** exp2/structured-team
- **Files changed:**
- `src/calculator.py` — added `import math` and `factorial(self, n: int) -> int` method with input validation
- `src/__main__.py` — added factorial demonstration line
- `tests/test_calculator.py` — added `TestCalculatorFactorial` class with 12 tests covering boundary cases, positive values, and invalid inputs

### Purpose

Add factorial as a supported calculator operation per Issue #240. Implements unary factorial method on Calculator class with validation for non-negative integers, rejecting negatives, floats, strings, and booleans.

### Risks

None. Additive change; `math.factorial` from standard library; no existing code modified.

### Test results

All 40 tests passed (12 new + 28 existing). No regressions.

Duration: 210.9s | Cost: $0.476329 USD | Turns: 15

Duration: 162.7s | Cost: $0.365086 USD | Turns: 11
