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
