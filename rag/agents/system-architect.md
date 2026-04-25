# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### Cycle 1: 2026-04-24 — Issue #372 V3 Task 1 — Division by Zero Handling

**Task:** Add unit test for division by zero and ensure implementation handles the edge case correctly.

**Key Decisions:**
1. No source code changes required to `src/calculator.py` — the `divide` method already correctly raises `ZeroDivisionError` natively via Python's `/` operator when divisor is zero.
2. Test specifications created for 5 test cases covering: division by zero (exception), normal division, float operands, negative divisor, and zero dividend.
3. All tests target `Calculator.divide()` method; no changes to other operations.

**Patterns Observed:**
- Minimal calculator implementation with raw operators — no defensive programming or custom error handling needed.
- Python's native exception behavior is sufficient and expected per requirements.

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Write 5 failing test functions in `tests/test_calculator.py` covering division edge cases
- Test `test_division_by_zero` MUST assert `ZeroDivisionError` is raised when divisor is 0
- Use pytest's `pytest.raises(ZeroDivisionError)` context manager
- All other tests verify normal behavior with various input types and signs
- File: `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_calculator.py`

**Handoff Notes for python-code-implementer:**
- No `src/` changes required — existing `divide` implementation is correct
- Simply receive pytest-edge-tester's WRITE report; implementation is already complete

### Cycle 2: 2026-04-24 — Issue #381 V3 Task 4 — Seven Advanced Operations

**Task:** Add seven advanced mathematical operations (square, cube, square_root, cube_root, power, log10, ln) to Calculator class with comprehensive test coverage.

**Key Decisions:**

1. **Method signatures:** All methods accept flexible numeric types (int/float mix), following existing Calculator pattern (no strict type validation).

2. **Error handling strategy:** 
   - Domain validation methods (`square_root`, `cube_root`, `power`, `log10`, `ln`) raise explicit `ValueError` with descriptive messages, mirroring the `factorial()` pattern.
   - Non-domain methods (`square`, `cube`) accept all real numbers without error handling.
   - Cube root supports negative inputs (real cube root semantics).

3. **Computation approach:**
   - Leverage existing `math` module imports (`math.sqrt()`, `math.log10()`, `math.log()`).
   - For `power()`: use native `**` operator with validation for negative base + non-integer exponent.
   - For `cube_root()`: compute as `x**(1/3)` for x≥0, or `-((-x)**(1/3))` for x<0 to preserve sign.

4. **Test suite organization:**
   - Create 7 new test classes in `tests/test_calculator.py` (one per operation).
   - Each class follows existing naming pattern (`TestCalculator<Operation>`).
   - Each covers: happy path, edge cases (zero, negatives), floats, and error conditions.
   - Use `pytest.raises(ValueError)` for domain violations; use `pytest.approx()` for floating-point comparisons.
   - Total: ~50 new test functions across all classes, no modifications to existing 23 tests.

**Patterns Observed:**
- Test suite uses class-based organization with consistent fixtures and assertion patterns.
- Error handling in `factorial()` demonstrates the expected pattern for domain validation.
- Calculator methods accept flexible numeric types without strict type enforcement.

**Architectural Impact:**
- Additive changes only — no breaking changes to existing API.
- Error handling pattern (explicit `ValueError`) extends established `factorial()` precedent.
- All computation delegated to `math` module; no new external dependencies required.

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Create 7 test classes in `tests/test_calculator.py`:
  - `TestCalculatorSquare` (5 tests: positive/negative integers, zero, float, small float)
  - `TestCalculatorCube` (5 tests: positive/negative integers, zero, float, negative float)
  - `TestCalculatorSquareRoot` (6 tests: perfect square, non-perfect, zero, float, negative raises ValueError × 2)
  - `TestCalculatorCubeRoot` (6 tests: positive/negative cube, non-perfect, zero, negative float, float)
  - `TestCalculatorPower` (10 tests: basic power, zero exponent, exponent 1, negative exponent, float base/exponent, negative base cases, zero base cases)
  - `TestCalculatorLog10` (8 tests: log10(10), log10(1), log10(100), float, small positive, zero/negative each raise ValueError × 3)
  - `TestCalculatorLn` (8 tests: ln(e), ln(1), small/large positive, float, zero/negative each raise ValueError × 3)
- All tests must be initially failing.
- Use `pytest.approx()` for floating-point assertions.
- Use `pytest.raises(ValueError)` context manager for error cases.

**Handoff Notes for python-code-implementer:**
- Modify `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`:
  - Add 7 methods to Calculator class: `square()`, `cube()`, `square_root()`, `cube_root()`, `power()`, `log10()`, `ln()`.
  - Follow docstring style from `factorial()` (Args, Returns, Raises sections).
  - `square_root()`: raise `ValueError` if x < 0.
  - `cube_root()`: handle negatives via sign-aware computation; no errors.
  - `power()`: raise `ValueError` for negative base + non-integer/non-rational exponent; use `**` operator.
  - `log10()`, `ln()`: raise `ValueError` if x ≤ 0.
  - No changes to existing methods.

### Cycle 3: 2026-04-24 — Issue #393 — Input Validation with Retry Logic and Failure Limits

**Task:** Add graceful input validation and error recovery to calculator's dual input modes (interactive and CLI). Interactive mode must allow retry on invalid input and exit after 3 consecutive failures. CLI mode must reject invalid input with clear error message and exit immediately. Both modes coexist in same binary.

**Key Decisions:**

1. **CLI mode:** No changes required — existing `_parse_cli_arguments()` and `_execute_cli_mode()` already validate strictly and exit with code 1 on any error (invalid operation, wrong arity, non-numeric operand, domain error).

2. **Interactive mode:** Introduce consecutive-failure counter that:
   - Initializes to 0 at start of `_run_interactive_loop()`
   - Increments on: unknown operation, invalid operand (non-numeric), domain errors (ValueError), math errors (ZeroDivisionError)
   - Resets to 0 on successful operation execution
   - Triggers graceful exit when counter reaches 3, printing "Too many invalid attempts. Exiting." and breaking loop

3. **Failure tracking scope:** A "failure" is any error that prevents operation execution or prevents valid result; includes:
   - Unknown operation name (not in registry)
   - Invalid operand (fails `_parse_number()`)
   - Domain error from operation (ValueError, ZeroDivisionError)

4. **No changes to:**
   - `Calculator` class (operations already validate domains correctly)
   - `_parse_number()` (already validates and raises ValueError)
   - `_build_registry()` (no changes needed)
   - `_parse_cli_arguments()` (already complete)
   - `_execute_cli_mode()` (already complete)
   - `cli_mode()` (dispatch logic unchanged)
   - `main()` (backward-compatible entry point)

5. **Error message format:** "Too many invalid attempts. Exiting." — printed to stdout (consistent with existing interactive output style).

**Patterns Observed:**
- Interactive and CLI modes were cleanly separated by `_parse_cli_arguments()` logic (returns None to signal interactive fallback).
- Existing error handling in `_run_interactive_loop()` catches ValueError and ZeroDivisionError; these continue the loop (perfect for counter increment + check logic).
- Operation validation and operand parsing are distinct steps in interactive loop, allowing granular failure tracking.

**Architectural Impact:**
- Interactive mode becomes more robust: prevents infinite retry loops from user frustration or confusion.
- CLI mode unchanged: strict validation and immediate exit already meets requirements.
- Both modes coexist seamlessly in `cli_mode()` dispatcher with no interference.
- No breaking changes to public API (`cli_mode()`, `main()` signatures unchanged).
- Exit is graceful (via break statement) — no SystemExit exception in interactive mode.
- Failure counter logic is encapsulated within `_run_interactive_loop()`; no global state.

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Create new test file: `tests/test_interactive_validation.py`
- Write 14 failing test functions covering:
  - **Consecutive-failure tracking (6 tests):**
    1. `test_interactive_consecutive_failures_three_invalid_ops` — three invalid operations → exit after third
    2. `test_interactive_consecutive_failures_mixed_invalid_op_and_operand` — mix of invalid op and operand failures → exit after third
    3. `test_interactive_consecutive_failures_domain_error_counts` — three domain errors → exit after third
    4. `test_interactive_counter_resets_on_success` — failure, then success, then failures → counter resets
    5. `test_interactive_success_clears_previous_failures` — two failures, success, three failures → exit after third
    6. `test_interactive_exactly_three_failures_before_exit` — verify exactly 3 errors shown, not more
  - **Backward compatibility (5 tests):**
    1. `test_interactive_single_invalid_operation_then_quit` — one error, quit → continues normally
    2. `test_interactive_invalid_operand_reprompts` — invalid operand → reprompts for operation
    3. `test_interactive_successful_operation_output` — successful operation → result printed, counter = 0
    4. `test_interactive_domain_error_does_not_crash` — domain error, then success → graceful recovery
    5. `test_interactive_quit_command_ends_loop_normally` — quit → no "Too many attempts" message
  - **CLI mode regression (2 tests):**
    1. `test_cli_mode_still_rejects_invalid_operand` — invalid operand → SystemExit(1)
    2. `test_cli_mode_still_rejects_domain_error` — domain error → SystemExit(1)
  - **Edge cases (1 test):**
    1. `test_interactive_consecutive_failures_first_failure` — one failure → counter = 1, loop continues
- All tests must FAIL before implementation.
- Use pytest `monkeypatch` to mock stdin via `builtins.input()`.
- Use `capsys` to capture stdout/stderr.
- Test file location: `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_interactive_validation.py`

**Handoff Notes for python-code-implementer:**
- Modify `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/__main__.py`:
  - Refactor `_run_interactive_loop()` to add `consecutive_failures: int = 0` counter.
  - On each error (unknown operation, invalid operand, domain/math error):
    - Print error message (existing behavior)
    - Increment `consecutive_failures`
    - If `consecutive_failures >= 3`: print "Too many invalid attempts. Exiting." and break loop
    - Otherwise: `continue` to next iteration
  - On successful operation execution:
    - Print result (existing behavior)
    - Reset `consecutive_failures = 0`
  - No changes to function signature or public API.
  - Preserve all existing error messages and output format.
  - No changes to `_parse_cli_arguments()`, `_execute_cli_mode()`, `cli_mode()`, or `main()`.

### Cycle 4: 2026-04-25 — PR #459 Unresolved Reviewer Feedback — Add 12 Missing Scientific Functions and Fix Mode Split

**Task:** Fix critical architectural mismatch where normal mode is too restrictive (only 5 operations instead of 10+), add 12 missing scientific functions (trig, inverse trig, hyperbolic, exponential, constants), correct the mode registry builder, and update interactive prompts.

**Key Decisions:**

1. **Mode split correction (CRITICAL):**
   - Normal mode must include ALL pre-split operations: add, subtract, multiply, divide, modulo, factorial, square, cube, square_root, cube_root, power, log10, ln (13 operations)
   - Scientific mode must be a true superset: all 13 above + 12 new scientific functions (25 total)
   - Current `_SCIENTIFIC_OPS_BLOCKED` list in `src/calculator/main.py` is now obsolete; blocking logic will be removed

2. **12 new scientific operations to implement as Operation subclasses:**
   - **Trigonometric (3):** sin(x), cos(x), tan(x) — arity 1 each, input in radians, return float
   - **Inverse Trigonometric (3):** asin(x), acos(x), atan(x) — arity 1 each, domain constraints, return float
     - asin: domain [-1, 1], raises ValueError outside
     - acos: domain [-1, 1], raises ValueError outside
     - atan: domain all reals, no error
   - **Hyperbolic (3):** sinh(x), cosh(x), tanh(x) — arity 1 each, input all reals, return float
   - **Exponential (1):** exp(x) — arity 1, input all reals, return float
   - **Mathematical Constants (2):** pi, e — arity 0 each (no operands), return float
   - All use `math` module functions (`math.sin`, `math.asin`, `math.sinh`, `math.exp`, `math.pi`, `math.e`)

3. **Implementation location:** All 12 new operations added to `src/calculator/operations/scientific.py` as separate Operation subclasses, following existing pattern

4. **Registry builder changes:**
   - Refactor `_build_registry(mode)` in `src/calculator/main.py` to register correct operation sets per mode
   - Normal mode: registers all 13 basic + existing scientific operations (add, subtract, multiply, divide, modulo, factorial, square, cube, square_root, cube_root, power, log10, ln)
   - Scientific mode: normal + all 12 new (trig, inverse trig, hyperbolic, exponential, constants)
   - Remove `_SCIENTIFIC_OPS_BLOCKED` blocking mechanism entirely since no operations should be blocked

5. **Interactive mode prompt update:**
   - Dynamic operation listing: after mode switch or at startup, print available operations based on current registry
   - Use `registry.list_all()` to generate the dynamic prompt text
   - Update the initial prompt at the start of `_run_interactive_loop()` and after successful mode switch
   - Include all current-mode operations in the help text

6. **Naming pattern for constants:**
   - "pi" and "e" are constants (zero-operand operations), not regular functions
   - Will show "pi" and "e" in interactive prompts as selectable "operations" even though they take no input
   - User input "pi" or "e" will prompt for zero operands and immediately return the constant value

7. **Backward compatibility:**
   - `src/__main__.py` shim already calls `cli_mode(MODE_SCIENTIFIC)`, so CLI users get all 25 operations (unaffected)
   - Existing tests remain unchanged; new tests will be added for new functions
   - Interactive mode default is `MODE_NORMAL` (13 operations); users can switch to scientific (25 operations)
   - Error handling and exception types unchanged

**Patterns Observed:**
- Operation subclasses follow consistent three-member pattern: `name` property, `arity` property, `execute()` method
- Math operations delegate to Python `math` module; no custom implementations needed
- Domain validation follows ValueError pattern established by existing operations (square_root, log10, ln)
- Registry rebuild on mode switch is already working; no changes needed to that logic

**Architectural Impact:**
- **Normal mode** becomes more capable and aligns with pre-split expectations (13 basic/core operations)
- **Scientific mode** becomes the true superset with all advanced math (25 total operations)
- No breaking changes to existing public API; all mode logic contained within `src/calculator/main.py`
- Interactive prompt now self-describing (dynamic operation list)
- Removes cognitive gap between "basic arithmetic" (5 ops) and "normal mode" label
- All new scientific operations use `math` module; no new dependencies

**Test Coverage Plan:**
- **New scientific function tests (12 function classes, ~8-10 tests each):**
  - ScientificSin: valid inputs (-π to π), approximate comparisons, special values (0, π/2, π)
  - ScientificCos: valid inputs, special values
  - ScientificTan: valid inputs, special values (avoiding undefined near π/2)
  - ScientificAsin: valid inputs in [-1, 1], domain errors outside range (3 error tests), special values
  - ScientificAcos: valid inputs in [-1, 1], domain errors (3 error tests), special values
  - ScientificAtan: valid inputs (all reals), special values
  - ScientificSinh: valid inputs, special values
  - ScientificCosh: valid inputs, special values
  - ScientificTanh: valid inputs, special values
  - ScientificExp: valid inputs, e^0=1, e^1≈e, e^negative close to 0
  - ScientificPi: returns math.pi, arity 0, no-operand execution
  - ScientificE: returns math.e, arity 0, no-operand execution
- **Mode split tests (5-6 tests):**
  - Normal mode has 13 operations (add...ln)
  - Scientific mode has 25 operations (normal + trig/inverse/hyperbolic/exponential/constants)
  - Mode switch rebuilds registry correctly
  - Availability of new functions per mode
- **Interactive prompt tests (2-3 tests):**
  - Prompt lists normal mode operations (13 names)
  - Prompt lists scientific mode operations (25 names)
  - Mode switch updates prompt
- **Backward compatibility tests (2-3 tests):**
  - CLI mode with MODE_SCIENTIFIC works (existing test suite passes)
  - Interactive mode default behavior unchanged
  - Failure counting still works

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Create new test file: `tests/test_scientific_functions.py`
- Write ~110 failing test functions covering all 12 new operations
- Test structure (per operation class):
  - **Trigonometric (sin, cos, tan):** valid angles, radians conversion check, special values (sin(0)=0, cos(0)=1, tan(0)=0), float approximations
  - **Inverse Trig (asin, acos, atan):**
    - asin/acos: domain tests (valid -1 to 1), 3 domain error tests (outside range), inverse relationship tests
    - atan: valid inputs (all reals), inverse relationship test
  - **Hyperbolic (sinh, cosh, tanh):** valid inputs, special values, approximations
  - **Exponential (exp):** exp(0)=1, exp(1)≈e, positive/negative/float inputs
  - **Constants (pi, e):** no operands required, return correct float values, arity=0
- Also write registry and mode split tests:
  - Test that normal mode contains exactly 13 operations
  - Test that scientific mode contains exactly 25 operations
  - Test each new function is unavailable in normal mode
  - Test each new function is available in scientific mode
- Use `pytest.approx()` for all floating-point assertions (due to math operation precision)
- Use `pytest.raises(ValueError)` for domain error tests
- Test file location: `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_scientific_functions.py`

**Handoff Notes for python-code-implementer:**
- **File 1:** `src/calculator/operations/scientific.py`
  - Add 12 new Operation subclasses at the end:
    - `ScientificSin()`: name="sin", arity=1, execute(x) → math.sin(x)
    - `ScientificCos()`: name="cos", arity=1, execute(x) → math.cos(x)
    - `ScientificTan()`: name="tan", arity=1, execute(x) → math.tan(x)
    - `ScientificAsin()`: name="asin", arity=1, validate domain [-1, 1], execute(x) → math.asin(x), raise ValueError if out of domain
    - `ScientificAcos()`: name="acos", arity=1, validate domain [-1, 1], execute(x) → math.acos(x), raise ValueError if out of domain
    - `ScientificAtan()`: name="atan", arity=1, execute(x) → math.atan(x)
    - `ScientificSinh()`: name="sinh", arity=1, execute(x) → math.sinh(x)
    - `ScientificCosh()`: name="cosh", arity=1, execute(x) → math.cosh(x)
    - `ScientificTanh()`: name="tanh", arity=1, execute(x) → math.tanh(x)
    - `ScientificExp()`: name="exp", arity=1, execute(x) → math.exp(x)
    - `ScientificPi()`: name="pi", arity=0, execute() → math.pi (no arguments)
    - `ScientificE()`: name="e", arity=0, execute() → math.e (no arguments)
  - All must follow existing Operation ABC pattern and docstring style
  - Imports: no new imports needed; `math` already imported

- **File 2:** `src/calculator/main.py`
  - Import 12 new operation classes:
    ```python
    from src.calculator.operations.scientific import (
        ScientificSquare, ..., ScientificLn,
        ScientificSin, ScientificCos, ScientificTan,
        ScientificAsin, ScientificAcos, ScientificAtan,
        ScientificSinh, ScientificCosh, ScientificTanh,
        ScientificExp, ScientificPi, ScientificE,
    )
    ```
  - Refactor `_build_registry(mode)` function:
    - Create `normal_ops` list with all 13 core operations: add, subtract, multiply, divide, modulo, factorial, square, cube, square_root, cube_root, power, log10, ln
    - In MODE_NORMAL: register only normal_ops (13 total)
    - In MODE_SCIENTIFIC: register normal_ops + all 12 new operations (25 total)
    - Return early after both paths are complete
  - **Delete `_SCIENTIFIC_OPS_BLOCKED` constant** (lines 48-55) — no longer needed
  - Update mode blocking logic in `_run_interactive_loop()`:
    - **Delete the entire mode-based blocking check** (lines 201-211 in current code that checks `if current_mode == MODE_NORMAL and operation in _SCIENTIFIC_OPS_BLOCKED`)
    - This logic becomes obsolete: all operations in registry are valid; registry itself enforces availability
  - Update interactive prompt:
    - After mode switch succeeds, call `registry.list_all()` to get current operation names
    - Update the initial prompt to dynamically list available operations: extract operation names from registry and format them nicely
    - Or, simpler: replace the hard-coded prompt with a call to format `registry.list_all()` into the prompt string
  - No changes to function signatures, error handling, or public API
  - Preserve all existing logic for mode switching, failure counting, history, error logging

**Handoff Notes for Integration & Testing:**
- After pytest-edge-tester writes failing tests and python-code-implementer writes code:
  - All 110+ new tests must pass
  - All existing tests must remain green (no regressions)
  - CI/CD should show zero test failures
  - Mode split validated: normal=13, scientific=25
  - No changes to CLI behavior (backward compatible via MODE_SCIENTIFIC in shim)

