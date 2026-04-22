## Run: Issue #247 — V2 Task 5 - Expert/team (2026-04-22)

- **Branch:** task/issue-247-interactive-input
- **PR target:** exp2/expert-team
- **Files changed:**
  - `src/cli.py` — New interactive CLI module with menu-driven session loop, arity detection via inspect, operand collection with re-prompt on invalid input, and graceful error handling
  - `src/__main__.py` — Updated entry point to instantiate Calculator and call interactive_session
  - `tests/test_cli.py` — 58 new tests covering get_arity, parse_float, get_operation_menu, get_operands, and interactive_session (full session flow, exit conditions, error handling)
- **Purpose:** Add interactive user input so the calculator reads operation selection and operands at runtime, supports 1- and 2-operand operations, and allows multiple calculations per session
- **Risks:** None — Calculator class is untouched; existing 237 tests unaffected; new interactive layer is purely additive
- **Tests passed:** 295 passed, 0 failed

Duration: PENDING | Cost: PENDING | Turns: PENDING

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

## Run: update-diagrams — Factorial Operation UML (2026-04-22)

- **Branch:** task/issue-241-factorial-operation
- **PR target:** main
- **Files changed:**
  - `artifacts/class_calculator.puml` — Class diagram updated with factorial method
  - `artifacts/activity_factorial.puml` — New activity diagram for factorial validation and computation flow
  - `artifacts/sequence_calculator_operations.puml` — New sequence diagram for key calculator operation scenarios

Duration: 193.5s | Cost: $0.430946 USD | Turns: 4

## Run: Issue #244 — V2 Task 4 - Expert/team (2026-04-22)

- **Branch:** task/issue-244-expert-team-operations
- **PR target:** exp2/expert-team
- **Files changed:**
  - `src/calculator.py` — Added square, cube, square_root, cube_root, logarithm, natural_logarithm (unary) and power (binary) methods with type/domain validation
  - `tests/test_advanced_operations.py` — New test file with 237 tests covering happy paths, edge cases, and invalid inputs for all 7 new methods
- **Purpose:** Add advanced mathematical operations (square, cube, sqrt, cbrt, power, log, ln) to the Calculator class as required by Issue #244
- **Risks:** None — all changes are additive; existing tests unaffected
- **Tests passed:** 237 passed, 0 failed

Duration: 250.6s | Cost: $0.564973 USD | Turns: 17

## Run: update-diagrams — Expert Operations UML (2026-04-22)

- **Branch:** task/issue-244-expert-team-operations
- **PR target:** exp2/expert-team
- **Files changed:**
  - `artifacts/class_calculator.puml` — Updated with 7 new expert operation methods (square, cube, square_root, cube_root, logarithm, natural_logarithm, power) and validation notes
  - `artifacts/activity_expert_operations.puml` — New activity diagram for square_root (with domain constraint) and power (binary validation) flows
  - `artifacts/sequence_calculator_operations.puml` — Appended 4 new scenarios (E-H) for square_root happy path, square_root ValueError, logarithm happy path, and power happy path

Duration: 224.8s | Cost: $0.616434 USD | Turns: 16
