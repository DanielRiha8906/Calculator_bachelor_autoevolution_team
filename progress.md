## Run: Issue #58 — CLI mode for Python calculator

Branch: task/issue-58-cli-mode
PR target: exp/expert-team

Files changed:
- main.py (created) — thin shim at project root; calls run_cli(sys.argv[1:])
- src/cli.py (created) — run_cli() dispatch function and _die() helper; validates op name, arity, and operand coercion against OPERATIONS; writes result to stdout, errors to stderr; exits 0/1
- tests/test_cli.py (created) — 30 tests covering successful two-operand and one-operand calls, parametrized smoke test across all OPERATIONS, unknown operation, wrong arity, non-numeric operand, no-args, and domain errors (divide by zero, sqrt negative, log zero, factorial negative, factorial float string)
- artifacts/class_diagram.puml (modified) — added CLI class and MAIN_NOTE component; added relationships: main → CLI → Calculator and CLI → OPERATIONS_NOTE
- artifacts/activity_diagram.puml (modified) — appended CLI Mode Flow partition after REPL flow; covers all validation and error exit paths
- artifacts/sequence_diagram.puml (modified) — appended "CLI Mode Interaction" scenario after existing interactive scenario; includes success path and alt error block

Purpose: Add CLI access layer for bash-based calculator usage so the calculator can be driven non-interactively from the command line.

Risks: OPERATIONS registry coupling (cli.py depends on structure of OPERATIONS dict from input_handler.py); sys.exit() calls inside run_cli require pytest.raises(SystemExit) in tests; stdout/stderr separation must be maintained for scripting correctness.

Test results: 349 passed, 0 failed, 0 skipped (python3 -m pytest)

Duration: 611.4s | Cost: $1.620374 USD | Turns: 13

---

## Run: Issue #55 — Development artifacts (PlantUML diagrams)

Branch: task/issue-55-development-artifacts
PR target: exp/expert-team

Files changed:
- artifacts/class_diagram.puml — new file; PlantUML class diagram documenting Calculator (12 methods), InputHandler (3 public, 3 private members), OPERATIONS module-level dict, and run_session free function with their relationships
- artifacts/activity_diagram.puml — new file; PlantUML activity diagram tracing the full InputHandler.run() REPL loop including exit/quit branch, unknown operation branch, operand parsing error path, and all Calculator exception paths (ZeroDivisionError, ValueError, TypeError)
- artifacts/sequence_diagram.puml — new file; PlantUML sequence diagram showing a complete successful interaction: program start, menu display, "add" operation with two operands, result output, and "quit" exit

Purpose: Create development artifact documentation diagrams derived exclusively from the actual src/ implementation for thesis traceability and architectural documentation.

Risks: None. No source code, tests, or configuration files were modified. Purely additive artifact creation.

Test results: No source changes; existing test suite state unchanged (252 passed from prior run).

Duration: 378.7s | Cost: $0.975133 USD | Turns: 11

---

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
