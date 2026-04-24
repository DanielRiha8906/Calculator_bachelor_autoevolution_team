# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### Cycle 1: 2026-04-24 — Issue #371 V3 Task 1 (test division incorrect inputs)
**Task:** Write test cases for division with invalid/incorrect inputs, particularly division by zero.

**Analysis:**
- `src/calculator.py` contains a `Calculator` class with a `divide(a, b)` method that performs simple division
- Division naturally raises `ZeroDivisionError` when b=0 (no special handling needed)
- `tests/test_calculator.py` exists but is minimal (only imports)
- Task is test-only; no source code changes needed

**Key Decisions:**
- Write 8 test cases covering: division by zero (error case), zero as numerator, negative operands (all combinations), normal division, and fractional results
- All tests go in `tests/test_calculator.py` and will initially fail (Red phase)
- No modifications to `src/calculator.py` required—existing division behavior already satisfies requirements

**Patterns Found:**
- Test file was pre-created but empty of test functions (common pattern in this repo for task initialization)

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** 8 test functions to write in `tests/test_calculator.py`. All tests must initially fail because the test file currently has no test functions.
- **python-code-implementer:** No source changes needed. Division already exists and behaves correctly. Pass only if pytest-edge-tester confirms all new tests are written and fail.

### Cycle 2: 2026-04-24 — Issue #374 V3 Task 2 (comprehensive calculator test suite)
**Task:** Create comprehensive test suite covering all existing calculator functionality plus advanced mathematical functions.

**Analysis:**
- Current Calculator has only 4 basic operations: add, subtract, multiply, divide
- Issue #371 task already added 8 division tests; total existing test count = 8
- Requirements call for tests on: basic arithmetic (partially done), advanced functions (square, cube, sqrt, cbrt, factorial, power, log, ln), error handling
- Advanced mathematical functions do NOT exist yet in `src/calculator.py`
- This is a test-creation task, but tests cannot pass without implementation
- Solution: Define comprehensive test specs in architect output; implementation comes after tests are written

**Key Decisions:**
- Write 68 total test cases: 15 new for basic arithmetic (add/subtract/multiply not yet tested), 45 for advanced functions, 8 for error handling and edge cases
- Tests require 8 new Calculator methods: square, cube, square_root, cube_root, factorial, power, log, ln
- Import math module in Calculator for sqrt, factorial, log functions
- Use pytest.approx() for floating-point comparisons; pytest.raises() for error cases
- All error conditions raise ValueError (domain errors) or TypeError (type errors)

**Patterns Found:**
- Test-first workflow: specs define the contract; implementation follows failing tests
- Calculator class design: pure functions, no state, consistent error handling

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write all 68 test cases (including existing 8 division tests, which should not be re-created). Organize into test classes by functionality. Expected initial failure count: 60 (division tests already pass; new tests fail).
- **python-code-implementer:** After tester confirms tests are written and correct count fail, implement the 8 missing methods in Calculator. All methods must follow error specifications in test specs. Target: all 68 tests passing.

### Cycle 3: 2026-04-24 — PR #432 Unresolved Feedback (extend CLI to all Calculator operations)
**Task:** Extend the CLI interface to support all 11 Calculator methods (currently supports only 4 binary operators). PR #432 implemented basic CLI but left 7 operations inaccessible: cube, square, sqrt, cbrt, power, log, ln.

**Analysis of Current State:**
- `src/calculator.py` has 11 methods: 4 binary (add, subtract, multiply, divide), 7 other (square [unary], cube [unary], square_root [unary], cube_root [unary], power [binary], log [unary], ln [unary], factorial [unary]). Total: 8 unary + 3 binary operations.
- `src/cli.py` currently hardcoded for binary only: prompts first_number, operator, second_number. Uses SUPPORTED_OPERATORS set with only {"+", "-", "*", "/"}.
- `tests/test_cli.py` has 27 tests covering the 4-operator flow; all tests mock input via `builtins.input` with side_effect sequences.
- All 27 tests must continue passing after changes (backward compatibility requirement).
- Current display_result() assumes binary: prints "first operator second = result"

**Key Architectural Decisions:**
1. **New OPERATIONS dict** replaces SUPPORTED_OPERATORS. Maps operation key (str) to tuple: (arity, method_name, display_symbol, description). Supports all 11 operations.
   - Example: "sqrt" → (1, "square_root", "sqrt", "Square root"), "+" → (2, "add", "+", "Addition"), "power" → (2, "power", "^", "Power")
   
2. **Arity-aware workflow** in run_calculator():
   - Get operation_key from prompt_for_operator()
   - Determine arity from OPERATIONS[operation_key][0]
   - If arity==1: prompt for single number, call unary method, display via display_result_unary()
   - If arity==2: prompt for two numbers, call binary method, display via display_result_binary()

3. **Preserve existing function signatures** where feasible:
   - prompt_for_first_number() and prompt_for_second_number() unchanged (return float)
   - display_result(first, operator, second, result) unchanged (used only for binary in tests)
   - Add new display_result_unary() and display_result_binary() for internal use

4. **Error handling**: Catch ValueError (domain errors), ZeroDivisionError, TypeError; display via display_error(). For backward compatibility with test 27 (division by zero), verify that ZeroDivisionError still propagates if caught in run_calculator().

5. **Backward compatibility strategy**:
   - pytest-edge-tester will adjust all 27 existing test mocks to new input order if necessary (operation_key first, then operands)
   - OR: If input order can remain operand-first, tests need minimal changes
   - Goal: all 27 existing tests pass without modification to test expectations (only mock adjustment)

**Patterns Found:**
- CLI design pattern: sequential prompts for operands, then operation execution, then display
- Test pattern: mock builtins.input with side_effect list in sequence order
- Operation taxonomy: unary (5) vs binary (6) methods in Calculator; both must be supported in CLI

**Risks & Mitigations:**
- Risk: Test input order change breaks 27 tests. Mitigation: pytest-edge-tester adjusts mocks during WRITE phase.
- Risk: Error handling differs for unary vs binary (e.g., sqrt(-1) vs 10/0). Mitigation: unified error catching in run_calculator().
- Risk: Display format mismatch (e.g., "sqrt(5) = 2.236" vs expected "5 sqrt = 2.236"). Mitigation: use new display_result_unary/binary functions; keep legacy display_result unchanged.

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 19 new test scenarios (tests 1-19 in this output's Test Specifications section). Existing 27 tests (backward compatibility tests 20-27) must be either preserved as-is OR updated to match new run_calculator() input flow. Key: all 46 total tests (27 existing + 19 new) must pass by end of cycle.
- **python-code-implementer:** Receives architect's plan + tester's WRITE report. Implements src/cli.py refactor per plan, focusing on: (1) OPERATIONS dict with all 11 operations and arity, (2) arity-aware run_calculator(), (3) helper functions for operation lookup and display, (4) error handling that preserves test expectations. Calculator class unchanged. Target: pytest-edge-tester VERIFY phase confirms all tests passing.

### Cycle 4: 2026-04-24 — Issue #389 V3 Task 7 (Add CLI Mode to Calculator)
**Task:** Add batch/command-line mode to calculator alongside existing interactive mode. CLI should accept operations from bash like `python -m calculator add 5 3`.

**Analysis of Current State:**
- `src/calculator.py` fully implemented with 11 methods (4 binary, 8 unary)
- `src/cli.py` implements interactive-only mode: sequential prompts for operands, operation, displays result
- `src/__main__.py` is entry point for interactive mode only
- `tests/test_cli.py` has 27 tests covering interactive flow
- Existing OPERATIONS dict in cli.py maps all 11 operations with arity info
- Requirements: batch mode with proper exit codes (0 success, 1 error), --help support, all operations accessible, error handling for all edge cases

**Key Architectural Decisions:**
1. **Create new `src/batch_cli.py`** module for batch/command-line argument processing
   - Does NOT duplicate operation logic; imports and reuses OPERATIONS dict from cli.py
   - Handles sys.argv parsing, operation validation, operand parsing, error handling
   - Returns exit code (0 or 1) based on success/failure
   - Outputs results to stdout, errors to stderr

2. **Modify `src/__main__.py`** to detect mode based on argument count
   - If len(sys.argv) > 1: batch mode (import batch_cli.batch_main, execute, sys.exit with returned code)
   - If len(sys.argv) == 1: interactive mode (existing flow)
   - Maintains backward compatibility: calling with no args still runs interactive mode

3. **Support in batch_cli.py:**
   - --help/-h flags: print usage and exit 0
   - All 12 operations: add, subtract, multiply, divide, square, cube, sqrt, cbrt, factorial, power, log, ln
   - Full error handling: ValueError (domain errors), ZeroDivisionError, TypeError
   - Argument validation: count (must match arity), type (must be numeric)
   - Output format: reuse display_result_unary() and display_result_binary() for consistency

4. **No changes to Calculator or existing cli.py**
   - Reuse OPERATIONS dict, helper functions, display functions
   - All Calculator methods already error-check properly (sqrt(-1), log(0), etc.)

5. **Test strategy:**
   - Create `tests/test_batch_cli.py` with 28 test scenarios
   - Covers: all 12 operations, help flag, error cases (div/0, sqrt negative, log non-positive, factorial negative), argument validation (missing, invalid type, too many), invalid operations
   - Tests use subprocess.run or direct batch_main() calls with mocked sys.argv

**Patterns Found:**
- Mode detection pattern: multi-purpose CLI entry point dispatching to interactive or batch handler
- Operation reuse: OPERATIONS dict is the single source of truth for all operation metadata

**Risks & Mitigations:**
- Risk: Mode detection logic error breaks interactive mode. Mitigation: simple check `len(sys.argv) > 1` is unambiguous; thoroughly test both paths.
- Risk: Batch mode error messages don't match user expectations. Mitigation: use stderr consistently, clear error text.
- Risk: Subprocess tests are brittle (e.g., timing, PATH). Mitigation: prefer direct function call tests with mocked sys.argv for reliability.

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 28 test cases in tests/test_batch_cli.py covering all scenarios in Test Specifications section. All tests must initially fail (batch_cli module doesn't exist yet).
- **python-code-implementer:** After tests are written and failing, implement: (1) Create src/batch_cli.py with parse_batch_args(), execute_batch(), batch_main() functions. (2) Modify src/__main__.py to detect mode and route. Target: all 28 batch tests + all 27 existing interactive tests passing.
