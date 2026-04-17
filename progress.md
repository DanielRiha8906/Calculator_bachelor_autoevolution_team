## Run: Interactive session loop — InputHandler and run_session

Branch: exp/expert-team
PR target: exp/expert-team

Files changed:
- src/input_handler.py — new module; OPERATIONS registry dict covering all 12 Calculator operations (5 binary, 7 unary); InputHandler class with run(), _show_menu(), _prompt_operands(), _dispatch(); run_session() convenience function
- tests/test_input_handler.py — 10 new tests covering exit/quit, binary ops (add, power), unary ops (square_root, factorial), invalid operation key, invalid operand, division by zero, and a multi-operation session
- src/__main__.py — replaced hardcoded demo body of main() with run_session(calc)

Purpose: Introduce an interactive REPL session to the calculator so users can choose and execute operations without code changes.

Risks: Low. No existing Calculator logic or test_calculator.py was modified. __main__.py interface (main() entry point) preserved; only its body changed.

Test results: 252 passed, 0 failed, 0 skipped (python -m pytest); includes 73 additional edge-case tests in tests/test_input_handler_edge.py

Files also changed:
- tests/test_input_handler_edge.py — 73 edge-case tests (negative operands, floats, zero, very large numbers, case-insensitive input, all unary/binary ops parametrized)

Duration: 586.5s | Cost: $1.376030 USD | Turns: 15

---

## Run: Issue #18 — V1 Task 4 - Mathematical functions (square, cube, sqrt, cbrt, log10, ln, power)

Branch: task/issue-18-math-functions
PR target: exp/expert-team

Files changed:
- src/calculator.py — added 7 new methods to Calculator: square, cube, square_root, cube_root, log10, ln, power. Each follows the factorial canonical pattern with type hints, Google-style docstrings, ValueError guards for domain errors, and math module delegation.
- tests/test_calculator.py — appended 85 new tests across 7 groups covering happy paths, domain error cases (ValueError for sqrt/log10/ln with invalid inputs), cube_root correctness on negatives (math.cbrt), and native ZeroDivisionError for power(0,-1).

Purpose: Implement unary operations (square, cube, square_root, cube_root, log10, ln) and binary operation (power) as calculator functions with consistent error handling.

Risks: Low. Purely additive changes. No existing methods or tests were modified. math.cbrt used for cube_root to correctly handle negative reals.

Test results: 169 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 437.3s | Cost: $1.009475 USD | Turns: 17

---

## Run: Issue #15 — Factorial feature implementation

Branch: task/issue-15-factorial
PR target: exp/expert-team

Files changed:
- src/calculator.py — added `import math` at the top; added `Calculator.factorial(n)` method with bool guard, int type check, negative value check, and `math.factorial(n)` delegation
- tests/test_calculator.py — appended a new "Tests for Calculator.factorial" section: test_factorial_happy_path (4 parametrized cases), test_factorial_returns_int, test_factorial_negative_raises_value_error (3 parametrized cases), test_factorial_invalid_type_raises_type_error (6 parametrized cases)

Purpose: Implement Calculator.factorial with full input validation (reject booleans, non-integers, and negatives) and corresponding test coverage per the architect's plan.

Risks: Low. Change is purely additive; no existing methods were modified. bool-before-int guard ordering is critical and is correctly implemented.

Test results: 60 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 342.7s | Cost: $0.823135 USD | Turns: 13

---

## Run: Issue #12 — V1 Task 2 - Test Suite Expansion (add, subtract, multiply)

Branch: task/issue-12-test-suite-expert-team
PR target: exp/expert-team

Files changed:
- tests/test_calculator.py — appended three new sections: test_add_cases (7 rows), test_add_does_not_mutate_inputs, test_subtract_cases (6 rows), test_subtract_does_not_mutate_inputs, test_multiply_cases (7 rows), test_multiply_does_not_mutate_inputs

Purpose: Expand test coverage to Calculator.add, Calculator.subtract, and Calculator.multiply with parametrized happy-path cases and side-effect-freedom checks. No production code was modified.

Risks: None. Change is purely additive (test-only). No existing tests removed or altered.

Test results: 46 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 355.4s | Cost: $0.810131 USD | Turns: 13

---

## Run: Issue #9 — V1 Task 1 - ZeroDivisionError - Expert/team

Branch: task/issue-9-zero-division-error
PR target: exp/expert-team

Files changed:
- tests/test_calculator.py — added test_divide_by_zero and 22 edge-case tests covering integer/float zero divisors, negative numerators, large numerators, 0/0, and IEEE 754 negative zero

Purpose: Add focused test coverage asserting Calculator.divide raises ZeroDivisionError on zero divisors. No implementation change was needed — the native Python / operator already raises ZeroDivisionError.

Risks: None. Change is purely additive (test-only). No production code was modified.

Test results: 23 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 293.9s | Cost: $0.799775 USD | Turns: 13
