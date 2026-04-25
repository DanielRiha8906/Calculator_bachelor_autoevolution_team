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

### Cycle 5: 2026-04-24 — Issue #392 V3 Task 8 (Input Validation with Retry Capability)
**Task:** Add input validation with user retry capability to interactive and CLI modes. Max 3 retries per input field; after exhaustion, exit gracefully.

**Analysis of Current State:**
- `src/calculator.py`: All domain validation (sqrt negative, log non-positive, factorial negative) already present; raises ValueError or ZeroDivisionError
- `src/cli.py`: Interactive mode already has infinite-loop retries in prompt_for_first_number(), prompt_for_second_number(), prompt_for_operator(). Input validation (numeric, operator name) works correctly but has NO RETRY LIMIT.
- `src/batch_cli.py`: Batch mode validates input once; no retry on error (correct for non-interactive)
- `src/__main__.py`: Routes interactive vs batch; error handling in place but needs update for new exception
- `tests/test_cli.py`: 27 tests all mock valid input directly; no tests for retry limits or exhaustion

**Key Architectural Decisions:**
1. **Add `MaxRetriesExceeded` exception class** in `src/cli.py`
   - Raised when user exhausts max retry attempts on any single input field
   - Propagates up through run_calculator() to main()

2. **Add `max_retries` parameter** to all three prompt functions (default 3)
   - Track attempt count internally
   - Before displaying error, check if attempts >= max_retries
   - If limit reached, raise MaxRetriesExceeded with field-specific message
   - Enhance error messages with attempt counter: "(Attempt N/3)"

3. **Distinguish retryable errors (user input) from non-retryable errors (domain)**
   - Retryable: non-numeric operand, invalid operator name
   - Non-retryable: sqrt of negative, factorial of negative, division by zero (Calculator raises ValueError/ZeroDivisionError directly)
   - run_calculator() catches Calculator errors and re-raises (doesn't retry)
   - Prompt functions catch ValueError from float() parsing, retry on that

4. **Update `src/__main__.py`** to catch and handle MaxRetriesExceeded
   - Import MaxRetriesExceeded from cli
   - In interactive mode's try/except, add handler: display_error + sys.exit(1)
   - Ensures explicit exit code 1 on all error paths

5. **Keep batch mode unchanged**
   - Batch mode is stateless, non-interactive; no retry needed
   - User provides all args at once; if invalid, exit immediately with code 1
   - No changes to src/batch_cli.py required

**Patterns Found:**
- Retry patterns: infinite loop with early termination condition (attempt counter)
- Exception hierarchy: custom exception (MaxRetriesExceeded) for control flow; standard exceptions (ValueError, ZeroDivisionError) for Calculator domain errors
- CLI architecture: separation of retryable (prompt functions) vs non-retryable (Calculator operations) error handling

**Risks & Mitigations:**
- Risk: Existing tests that expect infinite retries fail. Mitigation: tests write new failing tests first; all 27 existing tests mock valid input only, so never trigger retries (backward compatible).
- Risk: Domain errors become retryable. Mitigation: Calculator raises ValueError/ZeroDivisionError directly; run_calculator() re-raises without catching from within retry loops (tests 11-14 verify).
- Risk: Unclear error messages. Mitigation: error text includes attempt counter and field name; final message when exhausted explicitly states "Maximum retry attempts exceeded".
- Risk: Batch mode user confusion. Mitigation: batch mode unchanged; users understand it's non-interactive, no retries (tests 18-19 verify behavior frozen).

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 25 test cases in `tests/test_cli.py` (new file, or append to existing). Cover: (1) Retry limit enforcement per field (3 tests), (2) Successful retries after failures (3 tests), (3) Full workflow retry limits (3 tests), (4) Domain errors vs retryable errors (5 tests), (5) Integration with main() (3 tests), (6) Batch mode unchanged (2 tests), (7) Error message clarity (3 tests), (8) Backward compatibility and integration (4 tests). Expected: 25 new failing tests; all 27 existing tests still pass (no modifications to existing test input mocks needed).
- **python-code-implementer:** Implement changes per plan: (1) Add MaxRetriesExceeded exception to cli.py, (2) Update three prompt functions with max_retries parameter and attempt tracking, (3) Update cli.py docstrings, (4) Import MaxRetriesExceeded in __main__.py and add exception handler. No changes to calculator.py or batch_cli.py. Target: all 25 new tests passing + all 27 existing tests passing (52 total passing at end of cycle).

### Cycle 6: 2026-04-24 — PR #443 Unresolved Feedback (History Persistence & Interactive Loop)
**Task:** Address two PR #443 review comments: (1) Add interactive loop to CLI so user can perform multiple consecutive operations without restarting, (2) Implement file-based history storage (write to history.txt) with user discovery mechanism.

**Analysis of Current State:**
- `src/calculator.py`: History infrastructure complete (get_history(), clear_history(), _record_operation() all working); no changes needed
- `src/cli.py`: Interactive prompt functions exist; display_history() and _format_history_entry() already implemented; has MaxRetriesExceeded exception and retry logic from prior cycle
- `src/__main__.py`: Entry point calls run_calculator() once in interactive mode, then exits; batch/interactive mode detection already in place
- `tests/test_history.py`: 30 tests for in-memory history recording; all passing; no changes required
- Current limitation: run_calculator() executes one operation and returns (no loop); history exists only in-memory during session (not persisted)

**Key Architectural Decisions:**
1. **Add `persist_history_to_file()` function** in `src/cli.py`
   - Signature: persist_history_to_file(calc: Calculator, filepath: str = "history.txt") -> None
   - Behavior: Append all entries from calc.get_history() to filepath in append mode (preserves prior sessions)
   - Format: flat text, one line per operation (reuse _format_history_entry internally)
   - Error handling: wrap in try/except; log warning but do not raise (don't crash on I/O errors)

2. **Add `display_history_notification()` function** in `src/cli.py`
   - Signature: display_history_notification(filepath: str = "history.txt") -> None
   - Behavior: Print user-friendly message directing them to view history
   - Output example: "History saved to history.txt. View your history with: python -m calculator history"
   - Called after each successful operation in interactive mode

3. **Modify `run_calculator()` signature** in `src/cli.py`
   - New: run_calculator(calc: Calculator | None = None, max_retries: int = 3) -> float
   - If calc is None: create new Calculator (backward compatible)
   - If calc provided: reuse it (allows history accumulation across loop iterations)
   - After operation display, call display_history_notification() before returning result
   - Return value is still the numeric result (not affected by notification)

4. **Support "quit" and "exit" commands** in prompt_for_operator()
   - If user enters "quit" or "exit", return special sentinel value (e.g., string "QUIT")
   - Caller (main loop) interprets "QUIT" to break the interactive loop

5. **Implement interactive loop** in `src/__main__.py`
   - In interactive mode (len(sys.argv) == 1):
     - Create single Calculator instance at loop start
     - while True: call run_calculator(calc) in try block
     - If result is the "QUIT" sentinel: break loop
     - If MaxRetriesExceeded or domain error: display error, break (exit with code 1)
     - After loop exits: call persist_history_to_file(calc) to save accumulated history
     - Handle Ctrl+C (KeyboardInterrupt): catch, persist history, exit cleanly
   - Preserve batch mode routing (len(sys.argv) > 1) unchanged

6. **Optional: Add "history" command support** in `src/__main__.py`
   - Detect if sys.argv[1:] == ['history']
   - If so: load history.txt from disk, display in human-readable format, exit(0)
   - This provides user-discovery: after running operations, user can type "python -m calculator history"

7. **No changes to batch_cli.py**
   - Batch mode remains stateless, non-interactive, single-operation
   - Batch mode does not write to history.txt (by design: batch is for scripting, not exploration)

**Patterns Found:**
- Session-level state: main() now maintains a persistent Calculator instance across multiple run_calculator() calls
- Sentinel-value flow control: "QUIT" string distinguishes user request to exit from normal numeric result
- Append-based persistence: history.txt grows across sessions (each session appends); no session separation
- User discovery: notification messages guide users to available features

**Risks & Mitigations:**
- Risk: run_calculator() signature change breaks existing code. Mitigation: new parameter has default (None), so backward compatible; existing tests mock input and don't rely on shared Calculator instance.
- Risk: File I/O errors (disk full, permission denied) crash the program. Mitigation: wrap persist_history_to_file() in try/except; log warning but continue (non-critical feature).
- Risk: Ctrl+C exits without saving history. Mitigation: wrap main loop in try/finally to ensure persist_history_to_file() is always called before exit.
- Risk: "QUIT" string returned from run_calculator() confuses downstream code. Mitigation: Check return value type in main loop (is it float? or string?); or use exception-based flow (raise QuitRequested) instead.
- Risk: history.txt grows unbounded across sessions. Mitigation: Not in scope; document as limitation (future: add --clear-history option or max-size limit).

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 10 failing test cases covering: (1) Interactive loop with 3+ operations per session (tests 1-3), (2) History file written and formatted correctly (tests 4-6), (3) User notification message displayed (tests 7-8), (4) Backward compatibility: batch mode unaffected, quit command works (tests 9-10). All 10 tests must initially fail. Expected: no changes to existing 30 history recording tests or 27 CLI prompt tests; all remain passing.
- **python-code-implementer:** After tests are written and fail, implement per plan: (1) Add persist_history_to_file() and display_history_notification() functions to cli.py, (2) Modify run_calculator() signature to accept optional persistent Calculator, (3) Add "quit"/"exit" sentinel handling to prompt_for_operator(), (4) Implement interactive loop and history file persistence in __main__.py, (5) Optional: add "history" command. No changes to calculator.py or batch_cli.py. Target: all 10 new tests passing + all 57 existing tests (30 history + 27 CLI) passing = 67 total.

### Cycle 7: 2026-04-24 — Issue #401 V3 Task 11 (Separate Calculator Logic from Interface)
**Task:** Refactor to separate core calculation logic (Calculator class) from user interface concerns (prompts, display, error messages, operation routing, history persistence).

**Analysis of Current State:**
- `src/calculator.py`: Contains pure mathematical operations (11 methods) + history recording infrastructure. No UI imports. Clean separation on calc side.
- `src/cli.py`: Contains ALL interactive UI logic: exception classes, operation metadata dict, prompt functions, display functions, history formatting/persistence, and main orchestration function `run_calculator()`.
- `src/batch_cli.py`: Batch mode handler. Imports operation metadata and display functions from `cli.py`.
- `src/__main__.py`: Entry point. Routes interactive vs batch modes. Imports UI functions from `cli.py`.
- `tests/test_calculator.py`: Tests Calculator in isolation (pure math). No UI imports.
- `tests/test_cli.py`: Tests interactive prompts, display functions, and run_calculator flow.
- `tests/test_batch_cli.py`: Tests batch mode argument parsing and execution.
- `tests/test_history.py`: Tests Calculator history recording.

**Problem Identified:**
- `calculator.py` is clean (no UI concerns), but `cli.py` is a monolith combining prompts, display, exception classes, operation metadata, and orchestration
- `batch_cli.py` imports from `cli.py` to reuse operation metadata and display functions (indirect coupling through facade)
- Clear module boundaries needed: Calculator has no UI; UI module has no business logic

**Key Architectural Decisions:**
1. **Create new `src/interface.py`** — Consolidate ALL user interface concerns here
   - Move `MaxRetriesExceeded` exception from cli.py
   - Move `OPERATIONS` dict from cli.py
   - Move all prompt functions: `prompt_for_first_number`, `prompt_for_operator`, `prompt_for_second_number`
   - Move all display functions: `display_result`, `display_result_unary`, `display_result_binary`, `display_error`, `display_history`, `display_history_notification`
   - Move helper functions: `_get_operation_arity`, `_get_calculator_method`, `_get_display_symbol`, `_format_history_entry`
   - Move persistence function: `persist_history_to_file`
   - Move main orchestration: `run_calculator(calc, max_retries)`
   - Import: `Calculator` from `.calculator`, only standard library (sys, math, builtins.input)

2. **Convert `src/cli.py`** to a backward-compatibility facade
   - Remove ALL implementation code (prompts, displays, operations, exceptions)
   - Import everything from `interface.py` and re-export it
   - Maintain existing docstring explaining facade purpose
   - Ensures no breaking changes: `from src.cli import run_calculator` still works

3. **Update `src/batch_cli.py`** to import from interface, not cli
   - Change: `from .cli import OPERATIONS, display_result_unary, display_result_binary`
   - To: `from .interface import OPERATIONS, display_result_unary, display_result_binary`
   - No behavioral changes; only import source changes

4. **Verify `src/__main__.py`** imports work
   - Current imports from `cli` continue working due to facade
   - No changes required (backward compatible)
   - Optional: update to import from `interface` directly for clarity (not required)

5. **No changes to calculator.py**
   - Already clean; no UI imports or concerns
   - History recording is core business logic, not UI

**Separation of Concerns Achieved:**
- **`src/calculator.py`**: Pure math operations + history recording (zero UI concerns)
- **`src/interface.py`**: ALL user interaction, prompts, display, error messages, operation routing, history persistence (zero business logic)
- **`src/cli.py`**: Backward-compatibility facade (re-exports interface for existing imports)
- **`src/batch_cli.py`**: Batch mode handler (imports from interface, not through cli facade)
- **`src/__main__.py`**: Entry point and mode routing (no changes needed)

**Patterns Found:**
- Facade pattern: cli.py becomes a re-export facade for backward compatibility
- One-way dependency: interface → calculator (no cycles)
- Complete separation: calculator has zero UI imports; interface has zero math implementations

**Risks & Mitigations:**
- Risk: Import cycles if interface imports from cli. Mitigation: interface only imports Calculator; no cycle possible.
- Risk: Existing imports from cli.py break. Mitigation: cli.py re-exports everything; zero breaking changes.
- Risk: Interface.py becomes too large. Mitigation: Acceptable for current scope; future splits (interactive.py, display.py) possible if needed.
- Risk: Tests import from cli directly and break. Mitigation: cli still exports everything; tests pass unchanged.

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 15 test cases covering: (1) Separation verification (4 tests: calculator has no UI imports, interface exports all functions, operations dict exists, exception exists), (2) Backward compatibility (3 tests: imports from cli.py still work, run_calculator works same as before, batch_cli imports from interface), (3) Functional equivalence (4 tests: prompts work, displays work, persistence works, orchestration works), (4) No regressions (4 tests: all existing calculator tests pass, all existing cli tests pass, all existing batch_cli tests pass, all existing history tests pass). All new tests must initially fail or verify pre-conditions. Expected: 15 tests covering architecture + verification of no test regressions.
- **python-code-implementer:** (1) Create `src/interface.py` by copying all UI code from `cli.py` (prompts, displays, operations dict, exception, helper functions, persistence, run_calculator). (2) Convert `src/cli.py` to a facade: remove all impl, add `from .interface import *` with explicit re-exports. (3) Update `src/batch_cli.py`: change imports from `.cli` to `.interface` for operation metadata and display functions. (4) Verify `src/__main__.py` imports work (no changes needed). (5) Run full test suite: all existing tests must pass (zero behavioral changes, only module org). Target: all 15 architecture tests passing + all existing 110+ tests passing.

### Cycle 8: 2026-04-24 — Issue #404 V3 Task 12 (Refactor Calculator into More Modules and Prepare for Scientific Mode)
**Task:** Refactor calculator into more modules and prepare structural foundation for future scientific mode.

**Analysis of Current State:**
- `src/calculator.py` is a facade re-exporting Calculator from `calculator.py` (pre-Cycle 8 state: monolithic)
- `src/interface.py` contains ALL user interface logic (operations dict, prompts, displays, persistence, orchestration)
- `src/cli.py` is a backward-compatibility facade re-exporting from interface
- `src/batch_cli.py` imports from interface and uses Calculator
- `src/__main__.py` routes interactive/batch/history modes
- All 12 operations (4 basic: add/subtract/multiply/divide; 8 advanced: square/cube/sqrt/cbrt/factorial/power/log/ln) live in a single Calculator class
- Requirements: Modularize operations into separate modules (basic, advanced); prepare structure for future scientific mode extensibility

**Key Architectural Decisions:**
1. **Create `src/basic_operations.py`** — Pure functions for arithmetic (add, subtract, multiply, divide)
   - No imports except math stdlib if needed
   - No Calculator dependency or history recording
   - Serves as template for other operation modules
   
2. **Create `src/advanced_operations.py`** — Pure functions for advanced math (square, cube, sqrt, cbrt, factorial, power, log, ln)
   - Imports: math stdlib only
   - No Calculator dependency or history recording
   - Demonstrates extensibility: new scientific module can follow same pattern
   
3. **Create `src/calculator_core.py`** — Calculator class orchestrator
   - Imports: basic_operations, advanced_operations (relative imports)
   - Delegates each operation to corresponding module function
   - Maintains history recording (core business logic, not UI)
   - Public interface identical to old Calculator (12 methods + history API)
   
4. **Modify `src/calculator.py`** — Become a facade for backward compatibility
   - Import Calculator from calculator_core
   - Re-export as before
   - Ensures existing code continues working
   
5. **Modify `src/interface.py`** — Update import source
   - Change: `from .calculator import Calculator` → `from .calculator_core import Calculator`
   - Only change: import source (no behavior change)
   
6. **Modify `src/batch_cli.py`** — Update import source
   - Change: `from .calculator import Calculator` → `from .calculator_core import Calculator`
   - Only change: import source (no behavior change)
   
7. **Verify `src/__main__.py`** — No changes needed
   - Imports from cli (facade) which re-exports; chain still works
   - If desired for clarity, could update imports but not required

**Module Organization Achieved:**
```
basic_operations.py        [NEW] Pure arithmetic: add, subtract, multiply, divide
advanced_operations.py     [NEW] Pure advanced math: square, cube, sqrt, cbrt, factorial, power, log, ln
calculator_core.py         [NEW] Calculator orchestrator + history
calculator.py              [MODIFIED] Facade re-exporting Calculator from calculator_core
interface.py               [MODIFIED] Import Calculator from calculator_core (not calculator)
cli.py                     [UNCHANGED] Facade re-exporting from interface
batch_cli.py               [MODIFIED] Import Calculator from calculator_core (not calculator)
__main__.py                [UNCHANGED] Entry point (imports via cli)
```

**Dependency Graph:**
- basic_operations: no deps → advanced_operations: math stdlib → calculator_core: imports both → calculator: imports calculator_core → interface/batch_cli: import calculator_core → cli: imports interface → __main__: imports cli

**Preparation for Scientific Mode:**
- Future: Create `src/scientific_operations.py` with trig, stats, etc.
- Add Calculator methods delegating to scientific_operations (same pattern as basic/advanced)
- Add operation keys to OPERATIONS dict in interface
- Zero impact on existing code

**Patterns Found:**
- Module taxonomy: operation modules (basic, advanced, future scientific) export pure functions; calculator_core orchestrates and adds history
- Extensibility pattern: new operation modules follow identical structure; Calculator.py adds delegation methods
- Facade pattern continues: calculator.py, cli.py maintain backward compatibility

**Risks & Mitigations:**
- Risk: Import cycles. Mitigation: pure function modules have no inter-dependencies; calculator_core imports them one-way; no cycles.
- Risk: Tests break due to import changes. Mitigation: public API unchanged (Calculator from calculator import); all tests pass unchanged.
- Risk: Refactoring logic errors. Mitigation: delegation-only changes in calculator_core; no business logic modification.
- Risk: Performance regression. Mitigation: method call delegation overhead negligible; zero performance impact.

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write 30 test cases covering: (1) Module imports (tests 1-4: basic_ops, advanced_ops, calculator_core, operations registry can be imported), (2) Backward compatibility (tests 5-9: Calculator still importable from src.calculator, same public API, history works), (3) Operation functions (tests 6-24: basic_ops functions work, advanced_ops functions work, error handling preserved), (4) Extensibility (tests 25-28: operations registry complete, module structure clear, new modules can follow same pattern), (5) No regressions (tests 29-30: all 100+ existing tests still pass, batch_cli works unchanged). All new tests must initially fail or verify pre-conditions.
- **python-code-implementer:** Implement per plan: (1) Create basic_operations.py with 4 functions, (2) Create advanced_operations.py with 8 functions + math imports, (3) Create calculator_core.py with Calculator class delegating to both modules, (4) Replace calculator.py with facade, (5) Update imports in interface.py and batch_cli.py. Zero behavior changes; all 100+ existing tests pass; architecture clear and extensible.

### Cycle 9: 2026-04-25 — PR #457 Unresolved Feedback (Scientific Mode UI Integration Issue)
**Task:** Fix the integration gap between scientific mode state management in Calculator and interactive UI display of scientific operations. PR #457 implements scientific operations and mode management but does not properly expose them through the interactive UI.

**Current Problem Analysis:**
- Calculator class (`calculator_core.py`) has complete scientific operation methods (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, get_pi, get_e) ✓
- Mode state management in Calculator works correctly (enable_scientific_mode, disable_scientific_mode, toggle_scientific_mode, is_scientific_mode) ✓
- SCIENTIFIC_OPERATIONS dict exists in `interface.py` with proper metadata ✓
- prompt_for_operator() accepts mode parameter and correctly shows/hides scientific ops based on mode ✓
- scientific_operations.py module exists with all 12 pure functions ✓
- **BUT:** __main__.py tracks mode as a local string variable and toggles it, but never synchronizes Calculator._scientific_mode with the UI mode state
- **Result:** prompt_for_operator receives correct mode string, displays correct operations, user can select them, but Calculator instance's internal scientific_mode flag is never updated

**Integration Gap Root Cause:**
- Line 45 in `__main__.py`: `mode = "scientific" if mode == "normal" else "normal"` toggles the local string
- This local string is passed to `run_calculator(calc=calc, max_retries=3, mode=mode)` 
- `run_calculator` passes mode to `prompt_for_operator(max_retries=max_retries, mode=mode)`
- prompt_for_operator uses mode string to determine which operations dict to use (OPERATIONS or OPERATIONS+SCIENTIFIC_OPERATIONS)
- BUT `calc.enable_scientific_mode()` and `calc.disable_scientific_mode()` are never called
- The Calculator's internal _scientific_mode flag remains False throughout, even though UI shows scientific ops

**Key Architectural Decision:**
Synchronize the Calculator's internal mode state with the UI mode string by calling Calculator mode methods when mode changes.

**Where to Make the Change:**
- In `__main__.py`, when MODE_TOGGLE is detected, also call the appropriate Calculator method:
  - If mode is currently "normal", call `calc.enable_scientific_mode()` before updating mode string
  - If mode is currently "scientific", call `calc.disable_scientific_mode()` before updating mode string
- This ensures Calculator's _scientific_mode flag stays in sync with the UI's mode string

**Pattern Observed:**
- Mode state is now managed in TWO places: Calculator instance and __main__ loop variable
- Both must be kept synchronized for end-to-end functionality

**Risks & Mitigations:**
- Risk: Forgetting to call Calculator methods leaves internal state inconsistent. Mitigation: centralize mode toggle in one place (either Calculator or __main__) with clear responsibility.
- Risk: Tests don't verify integration (only unit tests of isolated components). Mitigation: write integration tests simulating full user flow: mode toggle → operation selection → execution.

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write failing integration tests (see Test Specifications below) that simulate end-to-end user flow in scientific mode. Tests must verify that after mode toggle, user can select and execute scientific operations, and Calculator internal state reflects the mode change.
- **python-code-implementer:** Modify `__main__.py` to synchronize Calculator mode state with UI mode string. When MODE_TOGGLE is returned from run_calculator, call the appropriate Calculator method (enable/disable) before updating the mode string variable. Verify all integration tests pass.

