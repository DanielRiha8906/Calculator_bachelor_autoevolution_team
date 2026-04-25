# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### 2026-04-24 — Issue #376 V3 Task 2 — Comprehensive Calculator Test Suite Plan

**Task:** Create comprehensive unit test suite for all calculator operations without modifying `src/` logic.

**Key Decisions:**
- Test-only task: zero source code changes to `src/calculator.py` or `src/__main__.py`
- Preserve existing 3 division-by-zero tests; add ~50 new tests covering add, subtract, multiply, divide
- Invalid input tests document actual Python behavior (not prescriptive fixes)
- All floating-point tests use pytest.approx() for precision tolerance
- Organize tests by operation then by scenario type (normal inputs, edge cases, invalid inputs, consistency)

**Architecture Observations:**
- Calculator class is minimal (4 methods, no type checking, no input validation)
- Existing test file has only 3 tests focused on division by zero
- No __init__.py in tests/ directory (simple flat structure)
- Test organization by operation makes maintenance and coverage verification easier

**Patterns Found:**
- pytest fixture pattern already established with `calc` fixture
- All operations perform raw Python operations (a + b, a - b, etc.) with no defensive checks

**Test Specifications Provided:**
- Addition: 9 tests (positive, negative, zero cases, floats, large numbers)
- Subtraction: 9 tests (positive, negative, zero cases, floats, large numbers)
- Multiplication: 10 tests (positive, negative, zero cases, floats, identity element)
- Division: 10 tests (existing 3 + 7 new, floats, zero dividend, zero divisor, large numbers)
- Invalid inputs: 8 tests (strings, None, type mismatches)
- Consistency/cross-operation: 6 tests (inverse operations, commutativity, non-commutativity)

**Handoff to pytest-edge-tester (WRITE):**
Implement ~52 test scenarios in `tests/test_calculator.py`. Keep existing 3 division-by-zero tests. All new tests must initially fail (not yet implemented). Organize by operation for clarity. Use pytest.approx() for floating-point comparisons.

**Handoff to python-code-implementer:**
NO SOURCE CHANGES REQUIRED. This task is test-only. If pytest-edge-tester produces failing tests, the implementer should not modify `src/` to make them pass — only the test suite is being built. The calculator implementation remains as-is.

---

### 2026-04-24 — Issue #379 — Factorial Operation Feature — DETAILED PLAN EMITTED

**Task:** Add factorial operation to Calculator class. Must handle valid non-negative integers (0→1, 1→1, n≥2→n!), explicitly reject negative integers (ValueError), and reject non-integer types (bool, float, str, None with ValueError).

**Key Decisions:**
- Single new method `factorial(self, n: int) -> int` added to Calculator class.
- Iterative (not recursive) implementation to avoid stack overflow on large n.
- Type validation executed first (bool, float, str, None all rejected with ValueError before value check).
- Value validation executed second (negative integers rejected with ValueError).
- Optional single-line demo added to `src/__main__.py` showing `calc.factorial(5)`.
- Unary operation; does not change class API or require refactoring.

**Architecture Observations (confirmed in source exploration):**
- Calculator class at `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py` contains 4 methods (add, subtract, multiply, divide), no __init__, pure functions.
- Existing methods perform raw Python operations with no defensive validation.
- Factorial introduces first unary operation but fits existing single-responsibility pattern.
- Type validation for factorial more strict than binary ops, justified by mathematical domain.
- Tests file at `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_calculator.py` already contains 3 division tests and 52+ other tests from V3 Task 2.

**Test Specifications Provided to pytest-edge-tester (WRITE):**
- Category 1 (Valid non-negative): 4 tests (0, 1, parametrized 2-10, large 20).
- Category 2 (Negative): 1 parametrized test (-1, -5, -100).
- Category 3 (Non-integers): 4 tests (float, string, None, bool).
- Category 4 (Type/edge): 2 tests (return type is int, match math.factorial).
- Total: 11 test functions with ~15 individual assertions when parametrized.

**Source Changes Plan for python-code-implementer:**
- File 1: `src/calculator.py` — Add method `factorial(self, n: int) -> int` with full input validation (type + value) and iterative computation. Placement: after divide method, before blank line.
- File 2 (optional): `src/__main__.py` — Add single print line `print("Factorial:", calc.factorial(5))` after Division line.

**Handoff to pytest-edge-tester (WRITE):**
Implement 11 test functions (or ~8-10 if parametrized aggressively) organized in 4 categories. All must fail initially. Use parametrize for multi-case tests. Use pytest.raises for exception testing. Match existing test style in test_calculator.py.

**Handoff to python-code-implementer (upon tester's WRITE report):**
Implement `Calculator.factorial(self, n: int) -> int` in `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`. Must:
1. Reject bool (ValueError, "boolean values")
2. Reject float (ValueError, "got float")
3. Reject str (ValueError, "got str")
4. Reject None (ValueError, "got NoneType")
5. Reject negative int (ValueError, "negative numbers")
6. Return 1 for n=0, return 1 for n=1, compute iteratively for n≥2.
7. Return type always int.

Execution order: pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #385 — V3 Task 5 - Expert/team — Interactive User Input Session

**Task:** Add interactive user input to calculator enabling operation selection, variable-arity operand input, result display, and multi-calculation session support.

**Key Decisions:**
- Create two new modules: `operation_registry.py` (operation discovery and arity metadata) and `interactive.py` (session handler)
- Dynamic operation discovery via reflection on Calculator class using `inspect.signature()`
- Unary detection: 1 non-self parameter; binary: 2 non-self parameters
- Interactive session loop: operation prompt → operand prompts (based on arity) → calculation → result display → continue/exit prompt → loop or exit
- Error handling: catch ValueError, ZeroDivisionError, and other exceptions; display error message; ask "Continue? (yes/no):" and allow recovery
- Input parsing: attempt float() conversion; if fails, re-prompt with "Invalid input. Please enter a number."
- Operation selection: numeric (0, 1, 2...) or name-based (TBD by implementer); invalid selection re-prompts
- No modifications to Calculator methods; no changes to operation implementations
- Existing hardcoded demo in `__main__.py` preserved; interactive mode added as new optional path

**Architecture Observations (from source exploration):**
- Calculator class (`/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`): 12 methods total
  - Binary (5): add, subtract, multiply, divide, power
  - Unary (7): factorial, square, cube, sqrt, cbrt, ln, log10
- No existing operation registry; operations are bare methods on class
- `__main__.py` currently calls hardcoded demo; no interactive entry point
- Test file uses pytest fixture pattern with `calc` fixture; easily extensible
- Trigonometric functions (sin, cos, tan, cot, asin, acos) mentioned in brief are NOT implemented; task uses only what exists

**Patterns Found:**
- Single-responsibility methods on Calculator class
- Type hints already present on recent methods (factorial, square, cube, etc.)
- Test organization by operation type works well
- Input/output testing requires mocking of `builtins.input` and `builtins.print`

**Test Specifications Provided to pytest-edge-tester (WRITE):**
15 comprehensive interactive scenarios in `tests/test_interactive.py`:
1. Binary operation (add) with valid operands → result displayed
2. Unary operation (factorial) with valid operand → result displayed
3. Unary operation (square) with valid operand → result displayed
4. Invalid operation selection → re-prompt
5. Non-numeric operand → re-prompt
6. Domain error (sqrt of negative) → error message, ask continue, allow recovery
7. Binary operation (divide) with valid operands → result displayed
8. Zero division error → error message, ask continue
9. Multiple calculations in session → both results shown, loop works
10. Factorial with float operand → domain error
11. Operation list displayed at start
12. User chooses "Continue: yes" → loops correctly
13. User chooses "Continue: no" → session exits
14. Operand input with whitespace/type tolerance (if applicable)
15. Float operands for binary operations → calculated correctly

All tests mock `builtins.input` and `builtins.print` to control interaction flow.

**Source Changes Plan for python-code-implementer:**
1. Create `src/operation_registry.py`:
   - Class `OperationRegistry(calculator: Calculator)`
   - Methods: `get_operations() -> List[str]`, `get_arity(op_name: str) -> int`, `call(op_name: str, *args) -> Any`
   - Uses `inspect.signature()` to determine arity
   - Sorted operation list for consistent UI
   - Full type hints

2. Create `src/interactive.py`:
   - Function `run_interactive_session(calculator: Calculator = None) -> None`
   - Function `parse_operand(user_input: str) -> float | int` (attempts float conversion; raises ValueError on fail)
   - Main loop: operation prompt → operand prompts → execute → display result or error → continue/exit
   - All exception handling in loop; no unhandled exceptions leak
   - Uses `input()` and `print()` for user interaction
   - Full type hints

3. Optionally modify `src/__main__.py`:
   - Add import: `from src.interactive import run_interactive_session`
   - Keep hardcoded `main()` unchanged (regression safety)
   - Either: add conditional flag `--interactive` in `if __name__` block, OR add comment noting interactive mode availability
   - Simplest: NO CHANGE to `__main__.py` is acceptable; interactive mode available as importable function

**No Changes to `src/calculator.py`:**
- All 12 existing methods remain unchanged
- No type validation added to binary operations
- No new methods added (trigonometric ops NOT included in this task)

**Handoff to pytest-edge-tester (WRITE):**
Write 15 test scenarios in `tests/test_interactive.py`. All tests must mock `builtins.input` (with list of user inputs in sequence) and `builtins.print` (to capture output). Each test calls `run_interactive_session(calculator)` or similar. Scenarios cover: valid calculations (unary/binary), invalid operation selection, non-numeric operands, domain errors, zero division, session loops, operation list display, continue/exit handling. All tests must FAIL initially (functions don't exist yet).

**Handoff to python-code-implementer (upon tester's WRITE report):**
Implement two new modules and optionally modify `__main__.py` per source changes plan above. Key requirements:
- OperationRegistry must correctly identify arity (1 or 2) for all 12 operations
- Interactive session must support the full flow: list → select → prompt operands → calculate → result/error → continue/exit
- All exceptions caught and handled gracefully; user can recover from any error
- Input parsing robust (float conversion, re-prompt on failure)
- Operation selection validation (re-prompt on invalid)
- Session loop correctly implements "Continue? (yes/no):" logic

Execution order: pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #391 — V3 Task 7 - Expert/team — CLI for Bash Invocation

**Task:** Add a command-line interface (CLI) enabling bash-based calculator invocation with operation name and operand arguments, supporting both unary and binary operations.

**Requirements:**
- Accept operation name as first positional argument
- Accept operand(s) as subsequent positional arguments
- Support variable operand counts: unary operations (e.g., factorial) and binary operations (e.g., add)
- Example invocations: `python -m src add 5 7` (binary), `python -m src factorial 5` (unary)
- Invoke calculator's operation registry with parsed operands
- Print operation result to standard output
- Incorrect argument usage must produce predictable, consistent behavior with non-zero exit code

**Key Decisions:**
- Create new module `src/cli.py` with CLI argument parser and operation executor
- Reuse existing `OperationRegistry` for operation discovery and execution (no duplication)
- Auto-detect CLI vs interactive mode in `__main__.py`: if argv > 1, run CLI; else run interactive
- Error handling: argument errors and computation errors both exit with code 1
- Results printed to stdout; errors and usage messages to stderr
- Operand parsing: supports int and float (decimal point detection); non-numeric input raises ValueError
- No changes to Calculator, OperationRegistry, or interactive modules; they remain unchanged

**Architecture Observations (from source exploration):**
- OperationRegistry (`src/operation_registry.py`) already introspects Calculator and discovers 12 operations (5 binary, 7 unary)
- Interactive mode (`src/interactive.py`) already uses OperationRegistry; mirrors operand parsing pattern
- Current `__main__.py` only dispatches to interactive; no CLI support exists
- Calculator has 12 methods with proper type hints and domain validation (e.g., sqrt rejects negatives, factorial rejects non-ints)
- Test infrastructure uses pytest with fixture pattern; mocking for input/output is standard

**Patterns Observed:**
- Parse operand pattern: try int first (no decimal point), fall back to float (has decimal point)
- Error handling pattern: catch specific exceptions (ZeroDivisionError, ValueError), print to stderr, exit with non-zero code
- Operation execution pattern: OperationRegistry.call(operation_name, *operands) returns result or raises exception
- Input validation pattern: validate before execution (operand count, operand format, operation existence)

**Test Specifications Provided to pytest-edge-tester (WRITE):**
25 test scenarios in new `tests/test_cli.py`:

1. **test_cli_binary_add_valid_integers**: argv=['add', '5', '7'] → stdout='12\n', exit=0
2. **test_cli_binary_subtract_valid_integers**: argv=['subtract', '10', '3'] → stdout='7\n', exit=0
3. **test_cli_binary_multiply_valid_integers**: argv=['multiply', '4', '5'] → stdout='20\n', exit=0

---

### 2026-04-25 — PR #466 — Left/Right/Bottom Layout Redesign (Unresolved Owner Feedback)

**Task:** Refactor iOS-style GUI layout from current single-column model to **left + right + bottom distributed layout**:
- **LEFT SIDE:** Number grid (digits 1–9 plus 0) in 3×4 arrangement
- **RIGHT SIDE:** Arithmetic operations (add, subtract, multiply, divide) vertically stacked
- **BOTTOM SECTION:** All remaining operations (layout adapts per mode: simple vs scientific)

**Status:** PR #466 is under review. Owner feedback (unresolved) requests a fundamental layout restructuring of `GuiCalculator` in `src/ui/gui.py`. Current layout has number grid and operations in sequential frames; new layout requires simultaneous left/right positioning with dynamic bottom section rebuild on mode switch.

**Current PR State (from source reading):**
- `GuiCalculator` class exists in `src/ui/gui.py` (lines 475–1086)
- `_THEME` dict complete (lines 12–29) with all required colors
- `_OPERATION_SYMBOLS` dict complete (lines 31–51)
- Three-panel layout already implemented: TOP (result + mode toggle), CONTENT (left + right), BOTTOM (operations)
- Helper methods exist: `_build_left_panel()`, `_build_right_panel()`, `_build_bottom_panel()`, `_rebuild_bottom_panel()`
- Mode toggle callback `_on_mode_toggle()` implemented with bottom panel rebuild
- Digit press handler `_on_digit_press()` implemented
- Operation press handler `_on_op_press()` implemented
- Hover effects via `_on_button_enter()` and `_on_button_leave()` already in place
- _TkStub class (lines 54–136) implements all necessary widget methods for headless testing

**Critical Issues Identified (from PR owner feedback):**

1. **BLOCKER 1: __main__.py imports CalculatorApp instead of GuiCalculator** — ALREADY FIXED IN SOURCE
   - Line 19 in `src/__main__.py`: CORRECT — imports GuiCalculator
   - Line 20: CORRECT — instantiates GuiCalculator
   - STATUS: No change needed; this is already correct

2. **BLOCKER 2: GUI widgets not rendering (display shows blank window)** — ROOT CAUSE: _make_button, _make_label, _make_frame ALWAYS RETURN _TkStub
   - Lines 676–724: `_make_button()` always returns `_TkStub()` instance (line 705)
   - Lines 726–760: `_make_label()` always returns `_TkStub()` instance (line 758)
   - Lines 762–778: `_make_frame()` always returns `_TkStub()` instance (line 776)
   - ROOT CAUSE: Widget factory methods create _TkStub directly; never use real tk.Button/tk.Label/tk.Frame
   - IMPACT: When tkinter IS available (normal Python environment), code still uses stubs; widgets don't render
   - FIX: Change _make_button, _make_label, _make_frame to use REAL tk classes when available
   - ARCHITECTURE PROBLEM: Current code tries to support both real and mocked tk, but implementation is inverted
   - SOLUTION: When _TK_AVAILABLE==True, use real tk.* classes; only use _TkStub for testing/mocking

3. **BLOCKER 3: Test suite does not match actual implementation**
   - Owner says: "Modify/Delete all the tests and development artifacts so that the testing suite and artifacts reflect the real behavior."
   - CURRENT STATE: test_gui_redesign.py (566 lines) tests GuiCalculator layout, colors, symbols, hover effects
   - STATUS: Tests reference attributes like `_btn_add`, `_btn_multiply`, `_operation_buttons` which ARE created in GuiCalculator
   - ISSUE: Tests check mocked tk.Tk behavior that may not reflect actual widget creation
   - SPECIFIC TEST ISSUES:
     - Tests mock tk.Tk; _TkStub.grid_info() returns stored kwargs, not actual grid geometry
     - Tests verify _TkStub behavior, which won't match real tkinter behavior
     - Some assertions depend on mocked behavior that won't occur in real GUI
   - FIX: Tests must remain; they validate the correct structure. But they need to account for real tk behavior vs mock.

**Root Cause Analysis:**

The three-panel layout IS correctly implemented in GuiCalculator. The real issue is that _make_button, _make_label, _make_frame are broken:

```python
# Lines 705, 758, 776 in _make_button, _make_label, _make_frame:
def _make_button(self, parent, text, bg, fg, active_bg, command=None):
    try:
        btn = _TkStub(...)  # <-- ALWAYS creates _TkStub, never tk.Button!
        ...
        return btn
```

**Correct behavior should be:**
- If _TK_AVAILABLE==True: use `tk.Button(parent, ...)` to create REAL buttons
- If _TK_AVAILABLE==False: use `_TkStub(...)` for testing

**Current behavior:**
- Always returns `_TkStub()`, even when real tkinter is available
- This causes widgets to be test doubles instead of real UI elements
- Display is blank because _TkStub doesn't render anything

**Remaining Work Required:**

1. **Fix Widget Factory Methods** (`src/ui/gui.py` lines 676–778):
   - `_make_button()` should return `tk.Button(...)` when _TK_AVAILABLE, else _TkStub
   - `_make_label()` should return `tk.Label(...)` when _TK_AVAILABLE, else _TkStub
   - `_make_frame()` should return `tk.Frame(...)` when _TK_AVAILABLE, else _TkStub
   - Keep all hover binding and theming logic
   - Preserve attribute assignment (_orig_bg, _active_bg) for styling access

2. **Update Test Suite** (test_gui.py and test_gui_redesign.py):
   - KEEP: All structural tests (frame existence, button existence, mode toggle)
   - KEEP: Color and styling assertions (from _THEME dict)
   - KEEP: Layout tests that validate grid layout
   - UPDATE: Tests must mock tk.Tk at module load (not just in test patches)
   - DELETE: Tests that assert _TkStub-specific behavior (grid_info, cget return values from _TkStub)
   - ADD: Tests that verify real widgets work (if running in environment with real tkinter)

**Architecture Summary (for reference):**

Three-panel hierarchy (from `_setup_ios_gui()`):
- Root window (black bg, 480x640)
  - _top_frame (row=0): result_label + mode_toggle_btn
  - _content_frame (row=1): _left_panel (col=0) + _right_panel (col=1)
    - _left_panel: digit buttons 1-9 in 3x3 grid, button 0 spanning cols 0-2
    - _right_panel: arithmetic ops vertically stacked (divide, multiply, subtract, add)
  - _bottom_frame (row=2): operation grid (4 columns, variable rows per mode)

**Handoff Plan (TDD Order):**

1. **pytest-edge-tester (WRITE):** Create comprehensive tests for widget creation (button, label, frame) that verify:
   - When _TK_AVAILABLE, widgets are real tk instances (not _TkStub)
   - When testing (mocked), widgets are _TkStub instances
   - Layout structure is correct (frames in right hierarchy)
   - Button colors/fonts/relief are correct
   - Mode toggle rebuilds bottom panel correctly
   
2. **python-code-implementer:** Fix _make_button, _make_label, _make_frame to:
   - Use real tk classes when _TK_AVAILABLE==True
   - Fall back to _TkStub when _TK_AVAILABLE==False
   - Preserve all styling and binding behavior
   
3. **pytest-edge-tester (VERIFY):** Run full suite; all tests must pass

4. **Commit:** Close PR with fixed widget factories and passing tests

---

