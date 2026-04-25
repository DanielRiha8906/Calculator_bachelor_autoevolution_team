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

### 2026-04-24 — Issue #465 — V3 Task 16 - GUI Redesign (iOS-Style Calculator)

**Task:** Fully redesign the existing tkinter GUI calculator to adopt a modern iOS-style layout and visual design. This is a **visual-only redesign** that preserves all underlying calculation logic, operation functionality, and mode switching. Redesign will establish:
- Grid-based layout with three main sections (result display, number grid, operation grid)
- Thematic color grouping by operation category (arithmetic, scientific, standard)
- Symbol-based button labels (Unicode mappings: add→"+", multiply→"×", sqrt→"√", etc.)
- Hover effects on all buttons
- Centralized theme dictionary for all colors, fonts, and visual constants

**Scope:** ONLY `src/ui/gui.py` modified; no changes to Calculator, modes.py, operation_registry.py, or any other file.

**Key Decisions:**
- Rename CalculatorApp to GuiCalculator (maintains backward compatibility for tests)
- Create centralized `_THEME` dictionary at module top with all color, font, and styling constants
- Implement complete UI redesign in `_setup_gui()`:
  - Result display: full-width label, right-aligned, monospace font (32pt bold), black bg / white fg
  - Mode toggle button: single button (text changes to "Scientific"/"Normal" based on mode)
  - Number grid: 3×4 grid with buttons 1-9 in rows 1-3, button 0 spanning all 3 columns in row 4
  - Operation grid: 4 columns with auto-sizing rows, all buttons square geometry
- Color scheme:
  - Arithmetic operators (add, subtract, multiply, divide): orange (#FF9500)
  - Scientific operations: dark gray (#1C1C1E)
  - Standard buttons: medium gray (#333333)
  - Window bg: black (#000000)
  - Mode toggle: dark gray (#2C2C2E)
- Symbol mapping: operation_name → Unicode symbol (add→"+", multiply→"×", divide→"÷", sqrt→"√", square→"x²", cube→"x³", power→"xʸ", factorial→"n!", ln→"ln", log→"log", sin→"sin", cos→"cos", tan→"tan", cot→"cot", asin→"asin", acos→"acos", cbrt→"∛", log10→"log₁₀")
- Hover effects: all buttons bind <Enter>/<Leave> events; background changes to activebackground on hover, reverts on leave
- Button properties: relief=FLAT, borderwidth=0, equal col/row weights for square geometry

**Architecture Observations (from source exploration):**
- CalculatorApp class currently uses form-based layout: mode radiobuttons, operation dropdown, operand text entry fields, calculate button, history display
- Public API methods (calculate, switch_mode, get_current_mode_operations, get_history, is_unary_operation, run) are all tested and must be preserved
- Internal state (_calculator, _registry, _history, _current_mode, _modes) is used by tests via mocks
- _parse_operand() static method used by calculate(); must be preserved
- All existing tests use mocked tk.Tk; will continue to work with renamed class and new widget layout
- Modes.py provides SimpleMode (6 ops) and ScientificMode (18 ops); operation discovery via registry.get_operations_by_mode()

**Patterns Found:**
- Mock-safe widget construction: all tk calls wrapped in try/except for headless test environments
- Dependency injection: root, calculator, registry all injectable for testing
- Grid layout will require tkinter Grid geometry manager (instead of current Pack)
- Hover effects require binding callbacks to Button widgets (tk.Button.bind() method)

**Test Specifications (31 scenarios):**
1. test_theme_dict_exists — _THEME dict exists at module level
2. test_theme_dict_keys — _THEME contains all required keys
3. test_theme_colors_format — All color values are valid hex strings
4. test_gui_calculator_instantiates — GuiCalculator(root=mock) creates without error
5. test_result_display_bg_color — Result display bg=#000000
6. test_result_display_fg_color — Result display fg=#FFFFFF
7. test_result_display_font — Result display uses monospace font
8. test_result_display_anchor — Result display is right-aligned
9. test_mode_toggle_button_exists — Mode toggle button exists
10. test_mode_toggle_text_normal_mode — In NORMAL mode, text="Scientific"
11. test_mode_toggle_text_scientific_mode — In SCIENTIFIC mode, text="Normal"
12. test_mode_toggle_switches_mode — Clicking mode toggle switches mode
13. test_number_grid_3x4_structure — Number grid has 3 columns, 4 rows
14. test_number_buttons_1_to_9 — Buttons for digits 1-9 exist
15. test_zero_button_spans_columns — Button 0 spans all 3 columns in row 4
16. test_operation_grid_4_columns — Operation grid has 4 columns
17. test_operation_grid_rows_normal — Normal mode: correct row count (6 ops)
18. test_operation_grid_rows_scientific — Scientific mode: correct row count (18 ops)
19. test_button_symbol_mapping_add — add operation shows "+" symbol
20. test_button_symbol_mapping_multiply — multiply operation shows "×" symbol
21. test_button_symbol_mapping_sqrt — sqrt operation shows "√" symbol
22. test_arithmetic_operator_colors — add/subtract/multiply/divide have bg=#FF9500
23. test_scientific_button_colors — Scientific ops have bg=#1C1C1E
24. test_button_relief_flat — All operation buttons have relief=FLAT
25. test_button_borderwidth_zero — All operation buttons have borderwidth=0
26. test_button_square_geometry — Operation grid buttons have equal width/height
27. test_hover_effect_binding — Buttons bind <Enter>/<Leave> events
28. test_hover_effect_on_enter — On <Enter>, bg changes to activebackground
29. test_hover_effect_on_leave — On <Leave>, bg reverts to default
30. test_window_bg_from_theme — Root window bg set from _THEME
31. test_frames_bg_from_theme — All frame widgets have bg from _THEME

**Source Changes Plan for python-code-implementer:**

**File:** `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/ui/gui.py`

**Changes:**
1. Add _THEME dictionary at module top (before CalculatorApp class):
   - Keys: WINDOW_BG, RESULT_BG, RESULT_FG, RESULT_FONT, BUTTON_NORMAL_BG, BUTTON_NORMAL_FG, BUTTON_NORMAL_ACTIVE_BG, BUTTON_OPERATOR_BG, BUTTON_OPERATOR_FG, BUTTON_OPERATOR_ACTIVE_BG, BUTTON_SCIENTIFIC_BG, BUTTON_SCIENTIFIC_FG, BUTTON_SCIENTIFIC_ACTIVE_BG, MODE_TOGGLE_BG, MODE_TOGGLE_FG, MODE_TOGGLE_ACTIVE_BG
   - Colors: all hex strings (#RRGGBB format)
   - Font: ("Courier", 32, "bold")

2. Add symbol mapping dictionary:
   - Entries: add→"+", subtract→"−", multiply→"×", divide→"÷", sqrt→"√", square→"x²", cube→"x³", power→"xʸ", factorial→"n!", ln→"ln", log→"log", sin→"sin", cos→"cos", tan→"tan", cot→"cot", asin→"asin", acos→"acos", cbrt→"∛", log10→"log₁₀"
   - Fallback: if operation not in mapping, use operation name

3. Rename CalculatorApp to GuiCalculator (maintain all existing public API)

4. Replace _setup_gui() method completely:
   - Window: 400×680 minimum size, bg from _THEME
   - Result display: full-width label, right-aligned, _THEME colors/font
   - Mode toggle button: full-width, text="Scientific"/"Normal", _THEME colors
   - Number grid: 3×4, buttons 0-9 with grid layout
   - Operation grid: 4 columns, grid layout, all buttons square
   - All buttons have hover effects via _bind_hover_effect()

5. Add helper methods:
   - _on_mode_toggle() — toggle mode, update button text, rebuild operation grid
   - _on_number_button(digit) — append digit to operand
   - _on_operation_button(op_name) — select operation
   - _bind_hover_effect(widget) — bind <Enter>/<Leave> events
   - _get_button_color(op_name) — return (bg, fg, activebackground) for operation
   - _get_symbol_for_operation(op_name) — return symbol or operation name

6. Preserve all existing public methods:
   - calculate(), switch_mode(), get_current_mode_operations(), get_history(), is_unary_operation(), run()
   - _parse_operand() static method

**Files NOT Modified:**
- src/calculator.py
- src/operation_registry.py
- src/infrastructure/history.py
- src/ui/modes.py
- src/core/operations.py
- src/__main__.py

**Architectural Impact:**
- Public API preserved; all existing tests continue to pass
- Visual-only change; no data model or calculation logic changes
- Theme centralization makes future visual updates trivial
- Grid layout replaces form-based layout
- Backward compatibility maintained (tests using mocked root will work)

**Execution Order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

**Test Specifications (31 scenarios, detailed below in Section 1 of output):**
- Frame structure tests: top, content (left+right), bottom frames exist and positioned correctly
- Left panel tests: number grid is 3×4, buttons 1–9 in grid, button 0 spans 3 columns
- Right panel tests: 4 arithmetic buttons vertically stacked
- Bottom panel tests: grid with 4 columns, operation count matches mode, buttons rebuild on mode switch
- Button functionality tests: digit press updates operand, operation press selects operation, mode toggle rebuilds bottom
- Styling tests: colors from _THEME, hover effects, fonts, alignment

**Handoff to pytest-edge-tester (WRITE):**
Write 31 test scenarios covering layout structure, button placement, frame organization, mode switch behavior, and basic functionality. All tests use mocked root and check widget attributes. Tests must FAIL initially (new GUI code not yet written).

**Handoff to python-code-implementer:**
Implement complete GUI redesign in `src/ui/gui.py` per source changes plan. Key deliverables:
- _THEME dict with all visual constants
- Symbol mapping dictionary
- GuiCalculator class (renamed from CalculatorApp) with new _setup_gui() implementation
- Grid-based layout for number and operation buttons
- Mode toggle button with dynamic text
- Hover effects on all buttons
- All existing public API methods preserved

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

1. **BLOCKER 1: __main__.py imports CalculatorApp instead of GuiCalculator**
   - Line 19 in `src/__main__.py`: `from .ui.gui import CalculatorApp`
   - Owner says: "In __main__.py change: from .ui.gui import CalculatorApp, to from .ui.gui import GuiCalculator."
   - IMPACT: `python -m src --gui` launches old CalculatorApp (form-based), not new GuiCalculator
   - FIX: Update import in `src/__main__.py` line 19 to import GuiCalculator

2. **BLOCKER 2: GUI widgets not rendering (display shows blank window)**
   - Owner says: "When launching the new design, nothing shows up. That's because tk.button was changed to _Tkstub…"
   - ANALYSIS: GuiCalculator uses `_TkStub` class for widget creation in all tests/headless envs
   - ISSUE: _TkStub does not render real tkinter widgets; it only stores config for test assertions
   - ROOT CAUSE: When `tkinter` import fails (line 138–141), code creates a stub tk module with tk.Button = _TkStub
   - FIX: When real tkinter is available, use real tk.Button/tk.Frame/tk.Label; _TkStub is only for headless tests
   - Current behavior: tk.Button is always _TkStub (created at module load if tkinter unavailable); once set, never uses real tkinter
   - SOLUTION: In production, tkinter IS available; code should use real tk classes. Test environment should mock appropriately.
   - VERIFICATION NEEDED: Check if headless CI actually imports real tkinter or not

3. **BLOCKER 3: Test suite does not match actual implementation**
   - Owner says: "Modify/Delete all the tests and development artifacts so that the testing suite and artifacts reflect the real behavior."
   - CURRENT STATE: test_gui_redesign.py (566 lines) tests GuiCalculator layout, colors, symbols, hover effects
   - STATUS: Tests reference attributes like `_btn_add`, `_btn_multiply`, `_operation_buttons` which ARE created in GuiCalculator
   - ISSUE: Some tests check mocked tk.Tk behavior that may not reflect actual layout (e.g., grid positioning via grid_info())
   - SPECIFIC TEST ISSUES:
     - Tests mock tk.Tk; _TkStub.grid_info() returns stored kwargs, not actual grid geometry
     - Tests that check grid layout via grid_info() might not reflect real layout behavior
     - Tests that expect button creation may pass but buttons not visible because _TkStub doesn't render
   - FIX: Update tests to verify actual widget structure (tree walk, attribute checks) rather than relying on mocked grid_info()
   - DELETE: Remove any tests that assert internal implementation details unrelated to user-visible behavior
   - ADD: Tests that verify the three-panel layout is actually visible (frames exist, buttons are in them, layout is correct)

**Remaining Work Required:**

1. **Fix Entry Point** (`src/__main__.py` line 19):
   - Change: `from .ui.gui import CalculatorApp`
   - To: `from .ui.gui import GuiCalculator`
   - Line 20: Change: `app = CalculatorApp()`
   - To: `app = GuiCalculator()`

2. **Verify Real tkinter Rendering**:
   - When code runs with real tkinter installed, tk.Button should be real tkinter.Button, NOT _TkStub
   - Current code: lines 138–169 create a fallback tk module if import fails
   - The fallback is CORRECT; but once imported, code uses whatever tk module was set up
   - VERIFICATION: Run `python -m src --gui` in environment where tkinter IS installed
   - EXPECTED: Real tkinter window opens with three-panel layout (left digit grid, right arithmetic, bottom ops)
   - If not: Debug why tkinter import is being skipped or overridden

3. **Update/Delete Test Suite**:
   - Review test_gui_redesign.py and test_gui.py
   - TESTS TO KEEP:
     - _THEME dictionary structure validation (lines 27–68)
     - _OPERATION_SYMBOLS dictionary validation (lines 70–108)
     - GuiCalculator class existence (lines 110–125)
     - Widget attribute existence tests (result_label, mode_toggle_btn, digit buttons, operation buttons)
     - Color value assertions (from _THEME, not from mocked widget cget)
   - TESTS TO FIX:
     - Button hierarchy/positioning tests: use actual widget tree instead of mocked grid_info()
     - Layout structure tests: verify frames exist and buttons are children
     - Mode toggle text tests: ensure they reflect current implementation
   - TESTS TO DELETE:
     - Any test that only checks mocked tk behavior without business logic value
     - Any test that asserts internal _TkStub state rather than user-visible behavior

**Architecture Summary (for layout ref):**

Three-panel hierarchy (from `_setup_ios_gui()`):
- Root window (black bg, 480x640)
  - _top_frame (row=0): result_label + mode_toggle_btn
  - _content_frame (row=1): _left_panel (col=0) + _right_panel (col=1)
    - _left_panel: digit buttons 1-9 in 3x3 grid, button 0 spanning cols 0-2
    - _right_panel: arithmetic ops vertically stacked (divide, multiply, subtract, add)
  - _bottom_frame (row=2): operation grid (4 columns, variable rows per mode)

**Handoff Notes:**

BLOCKER FIX ORDER:
1. Fix `src/__main__.py` imports (trivial, 2 lines)
2. Verify tkinter rendering (run test launch, debug if blank)
3. Create comprehensive test plan for layout verification (15-20 new tests)
4. Update/delete tests to match real behavior

MULTI-AGENT PIPELINE:
- **Analyst:** Issue requirements analysis ✓ (done above)
- **System Architect:** Create detailed test spec + source changes plan (THIS DOCUMENT)
- **pytest-edge-tester (WRITE):** Create failing tests for layout, frame structure, button placement
- **python-code-implementer:** Fix __main__.py imports; debug rendering if needed; update GUI if layout broken
- **pytest-edge-tester (VERIFY):** Run full suite; fix any failing tests to match actual behavior
- **Commit:** Merge PR with fixed imports and passing tests

---

