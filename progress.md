## Run: Issue #241 — V2 Task 3 - Expert/team (2026-04-22)

- **Branch:** task/issue-241-factorial-operation
- **PR target:** exp2/expert-team
- **Files changed:**
  - `src/calculator.py` — added `factorial(self, n: int) -> int` method with input validation
  - `tests/test_factorial.py` — new file with 19 tests covering happy path, ValueError, and TypeError cases
- **Purpose:** Add factorial as a supported calculator operation with validation rejecting negative integers and non-integer types
- **Risks:** None
- **Tests passed:** 127 passed, 0 failed

Duration: 178.1s | Cost: $0.467658 USD | Turns: 16

---

## Run: Issue #238 — V2 Task 2 Expert/team unit test suite

- **Branch:** task/issue-238-unit-test-suite
- **Target PR branch:** exp2/expert-team
- **Date:** 2026-04-22

### Files changed
- `tests/test_calculator.py` — added 69 new tests across three new classes: TestAdd (25 tests), TestSubtract (25 tests), TestMultiply (19 tests)

### Purpose
Create a comprehensive unit test suite for all four calculator operations. The existing file had TestDivide only (39 tests). Added TestAdd, TestSubtract, and TestMultiply covering normal inputs, edge cases (large/small numbers, float precision), and error conditions (TypeError for invalid inputs). No source changes were needed.

### Risks
None identified. Only test file modified; no production code changed.

### Test results
108 passed, 0 failed, 0 errors (0.07s)

### Tokens / cost / turns
Duration: 228.6s | Cost: $0.522512 USD | Turns: 15

---

## Run: Issue #235 — Division by zero test coverage

- **Branch:** task/issue-235-division-by-zero
- **Target PR branch:** exp2/expert-team
- **Date:** 2026-04-22

### Files changed
- `tests/test_calculator.py` — added 28 tests covering division by zero (integer and float zero denominators), happy path division, zero numerator, floating-point, and numeric extremes

### Purpose
Add focused test coverage asserting that `Calculator.divide()` raises `ZeroDivisionError` on division by zero. No source changes were required — Python's native `/` operator already raises `ZeroDivisionError` correctly.

### Risks
None identified. Only test file modified; no production code changed.

### Test results
28 passed, 0 failed, 0 errors (0.03s)

### Tokens / cost / turns
Duration: 155.1s | Cost: $0.393760 USD | Turns: 14

## Run: Diagram update — Calculator class and divide flow

- **Branch:** task/issue-235-division-by-zero
- **Date:** 2026-04-22

### Files changed
- `artifacts/class_calculator.puml` — class diagram for Calculator with module-level dependencies
- `artifacts/activity_divide.puml` — activity diagram for the two divide() execution paths
- `artifacts/sequence_main.puml` — sequence diagram for __main__.py::main() interactions

### Purpose
Add PlantUML diagrams documenting the Calculator class structure, divide() activity flow, and main() sequence for the division-by-zero feature branch.

### Risks
None. Documentation-only changes; no source or test files modified.

### Test results
N/A — no code changes.

Duration: 196.6s | Cost: $0.471889 USD | Turns: 16

Duration: 190.0s | Cost: $0.469532 USD | Turns: 9
