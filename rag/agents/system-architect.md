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

### 2026-04-24 — PR #434 — Interactive Mode Entry Point (Unresolved Blocker)

**Task:** Address blocker feedback from Owner (DanielRiha8906): "There is no way to launch the application to get into the interactive mode. Change __main__.py that when launched via python -m src, user input will be possible."

**Status:** The `src/interactive.py` and `src/operation_registry.py` modules are ALREADY FULLY IMPLEMENTED and FUNCTIONAL from the previous cycle (issue #385). The blocker is that `src/__main__.py` does not invoke them; it only runs a hardcoded demo.

**Current State:**
- `src/__main__.py`: imports Calculator, defines `main()` with hardcoded demo operations, calls `main()` in `if __name__` block
- `src/interactive.py`: fully implemented with `run_interactive_session()` function; accepts user input via `input()`, displays operation menu, prompts for operands, computes and displays results, handles errors gracefully, loops until user exits
- `src/operation_registry.py`: fully implemented; introspects Calculator class, discovers all public methods, filters to arity 1 or 2, provides get_operations(), get_arity(), call() methods

**Key Decisions:**
- Single-file change to `src/__main__.py`: replace the `main()` call with `run_interactive_session()`
- Keep existing `main()` function for backward compatibility (may be imported elsewhere)
- Add import: `from .interactive import run_interactive_session`
- Change `if __name__ == "__main__":` block from `main()` to `run_interactive_session()`
- This is a 2-line change with zero impact on existing Calculator class or test suite

**Architecture Impact:**
- MINIMAL: only the entry point changes
- `main()` is only called from `__main__` block; nothing else depends on it
- No changes to Calculator, operation_registry, or interactive modules
- Pre-existing tests continue to pass (unless they explicitly test entry point behavior)
- Backward compatible: any code doing `from src import main; main()` still works (just invokes interactive session instead of demo)

**Test Specifications for pytest-edge-tester (WRITE):**
10 scenarios in new `tests/test_interactive_entrypoint.py` or extended `tests/test_interactive.py`:
1. `__main__` block calls `run_interactive_session()` with no arguments
2. User selects 'add', provides operands 5 and 3, gets result 8
3. User selects 'factorial', provides operand 5, gets result 120
4. User completes operation, chooses 'yes' to continue, performs second operation, then exits
5. User completes operation, chooses 'no' to exit (session exits cleanly)
6. Operation list is displayed at session start
7. User enters invalid operation index (e.g., 999), sees "Invalid operation" message, re-prompted
8. User enters non-numeric operand (e.g., "abc"), sees "Invalid input" message, re-prompted
9. User selects divide with operands 5 and 0, sees "Error: Division by zero" message
10. User selects sqrt with operand -4, sees "Error:" message (domain error), session continues

All tests mock `builtins.input()` with sequence of user inputs and mock/capture `builtins.print()` to verify output.

**Source Changes Plan for python-code-implementer:**
- File: `src/__main__.py`
  - Action: Modify existing file
  - Change 1: Add import line at top: `from .interactive import run_interactive_session`
  - Change 2: Keep existing `main()` function unchanged
  - Change 3: In `if __name__ == "__main__":` block, replace `main()` with `run_interactive_session()`
  - Total: 2 lines changed (1 added, 1 modified)
  - No other files need modification

**Why This Fixes the Blocker:**
- Users can now run `python -m src` and immediately enter interactive mode
- No more hardcoded demo; interactive session accepts live user input
- All supporting infrastructure already exists and is tested
- Minimal risk: one entry point change with zero side effects

**Handoff to pytest-edge-tester (WRITE):**
Write 10 test scenarios in `tests/test_interactive_entrypoint.py` (or append to `tests/test_interactive.py`). Tests must mock `input()` and `print()` to simulate user interaction. All tests should FAIL initially because the new import and entry point do not yet exist. Tests verify:
- `run_interactive_session()` is invoked from `__main__` when module is executed
- Normal flow: operation selection → operand input → result display → continue/exit
- Error recovery: invalid operation, non-numeric operand, domain errors, zero division
- Session loop: multi-calculation sessions with proper exit handling

**Handoff to python-code-implementer:**
Implement single-file change to `src/__main__.py`:
1. Add import: `from .interactive import run_interactive_session`
2. Keep `main()` function as-is (backward compatibility)
3. Replace `main()` call in `if __name__ == "__main__":` block with `run_interactive_session()`

No other source files need modification. `src/interactive.py` and `src/operation_registry.py` are already complete and functional. All Calculator methods remain unchanged.

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

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

**Handoff to pytest-edge-tester (WRITE):**
Write 31 test scenarios covering:
- _THEME dict structure and values
- GuiCalculator instantiation (widget creation)
- Result display properties (colors, font, alignment)
- Mode toggle button (text, functionality)
- Number grid structure and buttons
- Operation grid structure, colors, symbols
- Button properties (relief, borderwidth, geometry)
- Background color propagation
- Hover effect bindings and behavior

All tests use mocked root (tk.Tk mock) and check widget attributes. Tests must FAIL initially (new GUI code not yet written).

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

**Key Deliverable:**

iOS-style calculator GUI with modern visual design, centralized theme system, and interactive button layouts while preserving all underlying calculation logic and operation functionality.

