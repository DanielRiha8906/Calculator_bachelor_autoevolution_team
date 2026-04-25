# RAG: github-task-analyst

## Purpose
Accumulated context from past issue analyses on this experiment branch. Each cycle entry records recurring requirement patterns, ambiguities encountered, and anything useful for the next invocation.

## Cycle Log

### 2026-04-24 | V3 Task 2 - Structured/team (Issue #375)

**Issue:** Create a unit test suite for the calculator's current functionality. Cover existing arithmetic operations and verify that expected results are valid inputs.

**Key Requirements Identified:**
- Primary: Build comprehensive unit test suite for calculator
- Scope: Existing arithmetic operations (scope of operations unclear — may be addition, subtraction, multiplication, division)
- Coverage: Test valid inputs and expected results
- Label: ai-implement:structured-team (indicates team-based structured implementation)

**Ambiguities & Gaps:**
- No comments provided; issue body is minimal
- "Verify that expected results are valid inputs" — phrasing is unusual; may mean "verify outputs are correct" or "validate inputs before operation"
- Specific arithmetic operations not listed (addition? subtraction? multiplication? division? modulo?)
- No mention of error conditions (division by zero, overflow, type errors, invalid operators)
- No existing test file location or naming convention specified
- Does not state whether to test edge cases or just happy path

**Assumed Resolution (for Architect):**
- Test suite should cover: addition, subtraction, multiplication, division (most common calculator operations)
- Include basic edge cases: zero, negative numbers, decimals
- Test file location: `tests/test_calculator.py` (standard convention)
- Verify both valid inputs and correct output results
- Architect and tester to determine whether to test error conditions

**Patterns:**
- Task is test-focused (TDD setup phase)
- Minimal specification suggests flexibility in implementation approach
- "ai-implement:structured-team" label indicates this is part of a team-based structured evolution cycle

### 2026-04-24 | V3 Task 3 - Structured/team (Issue #378)

**Issue:** Add factorial as a supported calculator operation. Make sure the calculator can correctly compute factorial values for valid inputs and update the tests accordingly.

**Key Requirements Identified:**
- Add factorial operation to the calculator
- Must compute factorial correctly for valid inputs
- Update tests to cover the new operation
- Part of V3 structured team implementation cycle (follows Task 1 on division-by-zero handling and Task 2 on test suite creation)

**Explicit Requirements:**
- **Functional:** Add factorial as a calculator operation
- **Testing:** Update existing tests to cover factorial
- **Scope:** Valid inputs only (implicitly excludes invalid cases, or delegates to error handling)

**Ambiguities & Gaps:**
- No definition of "valid inputs" — typical interpretation: non-negative integers (0!, 1!, 2!, etc.)
- Unclear if negative numbers or decimals should be tested (factorial is undefined for negatives, undefined/error for decimals)
- No specification of maximum input (e.g., 170! is near float64 limit; larger values overflow)
- No mention of whether operation is available in normal mode, scientific mode, or both
- Minimal task description; no acceptance criteria or test examples provided
- No comments to clarify intent

**Assumed Resolution (for Architect):**
- **Valid inputs:** Non-negative integers (0, 1, 2, 3, ..., up to a reasonable limit such as 170)
- **Computation:** n! = n × (n-1) × ... × 1, with 0! = 1
- **Operation scope:** Likely scientific mode (based on Issue #273 scientific mode task); confirm if also in normal mode
- **Test coverage:** Happy path (small integers), edge cases (0, 1, large valid input near limit), error conditions (negative, decimal, type errors) to be determined by architect
- **Error handling:** Assume invalid inputs handled consistently with division-by-zero pattern from Issue #372

**Context from Related Issues:**
- V3 Task 1 (#372): Division-by-zero error handling (establishes error-handling pattern for calculator)
- V3 Task 2 (#375): Unit test suite for existing functionality (establishes test structure)
- V2 Task 14 (#273): Scientific mode exists with expanded mathematical functions (factorial likely belongs here)
- Previous versions show calculator supports multiple modes and operation organization

**Patterns:**
- V3 tasks are incremental feature additions building on earlier foundation work
- "ai-implement:structured-team" label consistent across series
- Pattern: minimal task spec + reliance on prior implementation context
- Factorial is unary operator (takes one input), unlike binary arithmetic operations

### 2026-04-24 | V3 Task 4 - Structured/team (Issue #381)

**Issue:** Add square, cube, square root, cube root, power, log and ln as supported calculator operations. Make sure the calculator can execute these operations correctly and update the tests to cover the new functionality.

**Key Requirements Identified:**
- Add seven new mathematical operations: square, cube, square root, cube root, power, log (base 10), ln (natural logarithm)
- All operations must execute correctly
- Update test suite to cover all new operations
- Part of V3 structured team implementation (sequential to Task 3 on factorial)

**Explicit Requirements:**
- **Functional:** Implement seven mathematical operations (each described below)
  - Square: x² (unary; returns x × x)
  - Cube: x³ (unary; returns x × x × x)
  - Square root: √x (unary; mathematical square root)
  - Cube root: ∛x (unary; mathematical cube root)
  - Power: x^y (binary; returns x raised to power y)
  - Log: log₁₀(x) (unary; base-10 logarithm)
  - Ln: ln(x) (unary; natural logarithm, base e)
- **Testing:** Update existing test suite to include coverage for all new operations
- **Scope:** Must execute correctly; implicitly valid inputs only

**Ambiguities & Gaps:**
- No comments provided; issue body is minimal
- No definition of "valid inputs" for each operation:
  - Square, Cube: any real number (including negative)
  - Square root, Cube root: constraints unknown (square root undefined for negatives; cube root defined for all reals)
  - Power: constraints unknown (some bases/exponents may overflow or underflow)
  - Log, Ln: typically defined for positive numbers only
- No specification of behavior on invalid inputs (error handling, return value, exception type)
- No mention of numerical precision, rounding, or floating-point error handling
- Unclear if operations are in normal mode, scientific mode, or both
- No maximum value specifications (overflow limits)
- No test examples or acceptance criteria provided
- Binary operator (power) vs. unary operators (all others) — ambiguity about how power argument is provided in calculator UI (two separate inputs? operator chaining?)

**Assumed Resolution (for Architect):**
- **Valid input ranges:**
  - Square, Cube: all real numbers (−∞ to +∞)
  - Square root: x ≥ 0 (non-negative reals); error/exception for x < 0
  - Cube root: all real numbers; note that real cube root of negative is −∛(−x)
  - Power: x ≥ 0 for positive y; x ≠ 0 for negative y (standard constraint); behavior for x < 0 and fractional exponents TBD
  - Log: x > 0 (positive reals only); error/exception for x ≤ 0
  - Ln: x > 0 (positive reals only); error/exception for x ≤ 0
- **Error handling:** Follow pattern established in Task 1 (#372) on division-by-zero (likely return error message or raise exception)
- **Test coverage:** Happy path (typical valid inputs), edge cases (zero, large values, small positive values near zero), error conditions (negative square root, non-positive log/ln) to be determined by architect
- **Operation scope:** Likely scientific mode (all seven operations are advanced mathematical functions)
- **Power operator input:** Likely requires two operands; behavior depends on calculator architecture (infix: "2 power 3" or function syntax: "power(2, 3)")

**Context from Related Issues:**
- V3 Task 3 (#378): Factorial implementation (unary operation pattern)
- V3 Task 2 (#375): Test suite structure and existing test file location
- V3 Task 1 (#372): Error-handling pattern for invalid inputs
- V2 Task 14 (#273): Scientific mode architecture may guide operation placement

**Patterns:**
- V3 Task 4 is broader than Task 3: seven operations vs. one (factorial)
- Mix of unary and binary operators (all previous tasks dealt with unary or pure arithmetic)
- Power operation introduces first binary non-arithmetic operation in V3
- Minimal spec + reliance on prior context consistent with Task 2 and Task 3
- No mention of operation aliases or alternate names (e.g., sqrt vs. √, log vs. log10)
- Assumed all operations use standard mathematical definitions

### 2026-04-24 | V3 Task 5 - Structured/team (Issue #384)

**Issue:** Add interactive user input so the calculator can read the selected operation and required values at runtime. Make sure the entered values are used to perform calculations correctly and allow the user to continue using the calculator after a result is shown. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Add interactive/runtime user input capability to calculator
- Calculator must read operation selection from user input at runtime
- Calculator must read required values (operands) from user input at runtime
- Entered values must be used correctly to perform calculations
- Calculator must remain operational after displaying a result (loop/continue)
- Update tests to reflect changes to calculator input model

**Explicit Requirements:**
- **Functional:** Interactive user input loop for operation and operands
- **Functional:** Values entered must be correctly used in calculations
- **Functional:** Calculator must not exit after returning a result; must allow continuation of use
- **Testing:** Update existing tests to remain consistent with new input model

**Ambiguities & Gaps:**
- No comments provided; issue body is minimal
- No specification of input interface (CLI prompts? Menu system? Syntax expected?)
- No clarification of "selected operation" — how user selects (typing "add"? "+" symbol? menu number?)
- No specification of "required values" — how many operands? Format? Validation?
- No detail on how loop termination works (Ctrl+C? quit command? specific keyword?)
- No specification of what "enter values correctly" means (which existing operation set? all of them?)
- No mention of error handling during input (invalid operation, non-numeric input, etc.)
- No specification of output format for results (precision, rounding, etc.)
- No mention of whether calculator continues with fresh state or reuses previous result
- Minimal acceptance criteria; no test examples provided

**Assumed Resolution (for Architect):**
- **Input model:** Interactive loop at program entry; prompt user for:
  1. Operation to perform (e.g., "Enter operation: ", expects string like "add", "+", or numeric menu code)
  2. Operand(s) required by that operation (e.g., "Enter first value: ", "Enter second value: ")
- **Execution:** Read inputs → validate → perform operation using accumulated implementation from Tasks 1-4 → display result
- **Loop behavior:** After result display, prompt user again for next operation (do not exit program)
- **Termination:** User-initiated (e.g., "quit", "exit", "q", or Ctrl+C)
- **Error handling:** Handle invalid operations, non-numeric input, and operation-specific errors (e.g., division by zero) consistently with prior tasks
- **Test updates:** Tests will need to adapt from non-interactive/batch input model to interactive loop (may require mocking stdin or changing test structure)

**Context from Related Issues:**
- V3 Task 4 (#381): Seven mathematical operations (square, cube, sqrt, cbrt, power, log, ln)
- V3 Task 3 (#378): Factorial operation
- V3 Task 1 (#372): Division-by-zero error handling pattern
- V3 Task 2 (#375): Test suite and operations scope (arithmetic + scientific)
- Issue #273: Scientific mode (architecture reference for operation organization)

**Patterns:**
- V3 Task 5 is a UI/UX layer task, differs from previous feature-addition tasks (1-4)
- Task 5 consolidates all prior operations into an interactive workflow
- V3 sequence so far: error handling (1) → test suite (2) → factorial (3) → advanced math (4) → interactive UI (5)
- Likely end-of-V3 task; integration and usability focus
- "ai-implement:structured-team" label consistent; no new operations, UX/workflow addition
- No comments suggest this is straightforward specification; ambiguities are structural (input format, loop behavior)

### 2026-04-24 | V3 Task 7 - Structured/team (Issue #390)

**Issue:** Add a CLI mode so the calculator can be executed from bash using command-line arguments. Allow the user to provide the operation and required values directly in the command and print the result to the terminal. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Add command-line argument parsing to calculator
- Calculator must accept operation and operand values as CLI arguments
- Calculator must execute operation and print result directly to terminal (no interactive loop)
- Update test suite to remain consistent with dual-mode behavior (interactive from Task 5 + CLI from Task 7)

**Explicit Requirements:**
- **Functional:** CLI argument parsing for operation and operands
- **Functional:** Direct execution and result output to stdout
- **Testing:** Update tests to accommodate CLI mode coexisting with interactive mode

**Ambiguities & Gaps:**
- No comments provided; issue body is minimal
- **CLI syntax unspecified:** No format defined for command-line invocation (e.g., `calc add 5 3` vs `calc --op add --args 5 3` vs expression string `calc "5 + 3"`)
- **Mode selection logic:** Unclear what triggers CLI vs. interactive mode (argc > 1? flag check? environment variable?)
- **Error handling for CLI:** No specification for invalid arguments, missing operands, invalid operations (assume stderr output + non-zero exit code per CLI conventions)
- **Output format:** No specification for result display (plain number? operation + result? JSON? Assume plain number to stdout)
- **Mode coexistence:** Phrasing "Add a CLI mode" suggests both modes coexist, but not explicit; unclear if CLI replaces or supplements interactive mode
- **Argument validation:** No specification of type checking, range validation, or how operation names map to operation functions
- No test examples or acceptance criteria provided
- No mention of help/usage messages or version flags

**Assumed Resolution (for Architect):**
- **CLI mode activation:** When CLI arguments are provided (argc > 1), skip interactive loop and enter CLI execution mode
- **CLI syntax:** Use positional arguments: `calculator <operation> <operand1> [<operand2> ...]` (simple, clear, UNIX-style)
- **Mode coexistence:** Both CLI and interactive modes available in same binary; interactive is default when no args provided
- **Error handling:** Invalid args → print error to stderr, exit code 1; missing/invalid operands → descriptive error; invalid operation → "unknown operation" message
- **Output:** Plain number to stdout (e.g., `8` for `add 5 3`); no decorative text
- **Operand parsing:** Parse all operands as floats/integers; let operation implementation validate type constraints
- **Operation names:** Map CLI operation names to internal operation functions (likely string matching: "add" → add_operation, "sqrt" → sqrt_operation, etc.)

**Context from Related Issues:**
- V3 Task 5 (#384): Interactive input mode (CLI mode supplements this; both modes must coexist)
- V3 Tasks 1-4 (#372, #375, #378, #381): Operation implementations (factorial, advanced math, error handling, test suite)
- V2 Task 14 (#273): Scientific mode architecture (both interactive and CLI modes should access same operation set)

**Patterns:**
- V3 Task 7 is input-layer task following Task 5; adds alternative input channel (CLI) to existing interactive UI
- Minimal specification consistent with prior V3 tasks; CLI syntax and mode selection logic unspecified
- No new operations; purely input-handling and integration task
- "ai-implement:structured-team" label consistent; no new core features
- Task likely represents completion of input-interface work for V3 (error handling, test coverage, interactive, CLI)
- Ambiguities are straightforward engineering decisions (CLI format, arg parsing, mode logic); no deep domain confusion

### 2026-04-24 | V3 Task 8 - Structured/team (Issue #393)

**Issue:** Add input validation to the calculator's guided interactive mode so invalid user input does not immediately break the session. Let the user retry after invalid operation or operand input, and stop the session after a fixed number of failed attempts. In CLI mode, invalid input should return a clear error message and exit instead of retrying. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Add input validation and error recovery to interactive mode
- Interactive mode must allow retry on invalid input (operation or operand)
- Interactive mode must exit after a fixed maximum number of failed attempts
- CLI mode must return clear error message and exit immediately on invalid input (no retry)
- Update tests to reflect dual-mode input validation behavior

**Explicit Requirements - Interactive Mode:**
- **Functional:** Validate user input for operations and operands
- **Functional:** Allow user to retry after invalid input
- **Functional:** Exit session after fixed number of consecutive failures
- **Error behavior:** Invalid input does not "immediately break the session" (implies graceful error handling, not exception/crash)

**Explicit Requirements - CLI Mode:**
- **Functional:** Return clear error message to user on invalid input
- **Functional:** Exit with appropriate status code (non-zero per CLI conventions)
- **Behavioral:** No retry logic in CLI mode (different from interactive)

**Explicit Requirements - Testing:**
- **Testing:** Update existing test suite to cover both modes and new validation behavior

**Ambiguities & Gaps:**
- **"Fixed number" of failed attempts:** No specification of the exact maximum (3? 5? 10?)
- **"Invalid operation or operand input":** Scope ambiguous:
  - Invalid operation: unrecognized operation name? Already established from Task 7 error handling
  - Invalid operand: non-numeric input? Out-of-range input (e.g., negative for square root)? Type mismatch?
  - Missing operands? Wrong number of operands for operation?
- **Retry mechanism:** Unclear what "retry" means:
  - Prompt user again for same input (operation or operand)?
  - Allow user to restart from operation selection?
  - Allow user to continue in fresh state after N failures?
- **Session exit on max failures:** Behavior undefined:
  - Exit immediately after Nth failure?
  - Display message before exit? (e.g., "Too many invalid attempts. Goodbye.")
  - Return specific exit code?
- **"Clear error message":** No specification of error message format or content (which errors? how detailed?)
- **Counting failures:** Ambiguous:
  - Count per session? Per operation? Reset after successful operation?
  - Count only input parsing failures or also operation-specific errors (e.g., division by zero, invalid math domain)?
  - Are operation-specific errors (sqrt of negative, log of zero) counted same as invalid syntax?
- **Error handling precedent:** Task 7 (#390) established CLI error behavior; Task 8 builds on it but differs (retry in interactive vs. exit in CLI)
- No comments provided; issue body is minimal
- No test examples or acceptance criteria provided
- No mention of error message locale, formatting, or content specifics

**Assumed Resolution (for Architect):**
- **Maximum failed attempts:** Assume 3 consecutive failures (common UX pattern; architect may adjust)
- **Invalid input categories:**
  - **Operation:** Unrecognized operation name (handled in Task 7; reuse that validation)
  - **Operand:** Non-numeric input, or value outside domain of operation (e.g., negative for sqrt, non-positive for log/ln)
  - **Count:** Track consecutive failures; reset counter to 0 on successful operation
- **Retry flow (Interactive):**
  - Detect invalid input → display error message → prompt user again for that input (operation or operand, depending on where error occurred)
  - Increment failure counter
  - After 3 consecutive failures, exit with "Too many invalid attempts" message
- **Exit flow (CLI):**
  - Invalid input detected → print clear error message to stderr → exit with code 1 (from Task 7 pattern)
  - No counter; single error triggers exit
- **Error message content:**
  - For invalid operation: "Unknown operation: <operation>" or "Operation '<op>' not found"
  - For invalid operand: "<input> is not a valid number" or "Cannot perform <operation> with value <input>" (operation-specific message)
  - For max attempts reached: "Too many invalid attempts. Exiting." or "Session terminated due to repeated invalid input."
- **Scope of "invalid input":**
  - Include type errors (non-numeric input)
  - Include domain errors (operation-specific constraints: sqrt(negative), log(non-positive))
  - Include syntax errors (missing operand, extra operand)
  - Question: Are operation-specific errors (division by zero) from Task 1 counted as "failed attempt"? Likely yes, bundled with operand validation.
- **Test updates:** New tests for:
  - Interactive mode with invalid input → retry prompt
  - Interactive mode with N-1 failures → success
  - Interactive mode with N failures → exit message + exit
  - CLI mode with invalid input → error message + exit code 1
  - Both modes with various invalid operand types (non-numeric, domain violations)

**Context from Related Issues:**
- V3 Task 7 (#390): CLI mode and error handling (Task 8 extends this with validation and mode-specific behavior)
- V3 Task 5 (#384): Interactive mode (Task 8 adds robustness to Task 5's input loop)
- V3 Task 1 (#372): Division-by-zero error handling (pattern for operation-specific validation)
- V3 Tasks 2-4: Operation implementations (all must coexist with Task 8's input validation)

**Patterns:**
- V3 Task 8 is error-handling and robustness task following Task 7 (completes input layer)
- Task 8 differentiates behavior by mode: interactive (forgiving, retry) vs. CLI (strict, fail-fast)
- Minimal specification consistent with V3 series; key ambiguity is max-retry count and scope of "invalid input"
- "ai-implement:structured-team" label consistent; no new operations, pure UX/robustness improvement
- Task represents completion of V3 input-layer work: error handling (Task 1) → interactive (Task 5) → CLI (Task 7) → validation & recovery (Task 8)
- Task 8 is final integration task; all prior tasks' features must coexist with new validation behavior

### 2026-04-24 | V3 Task 10 - Structured/team (Issue #399)

**Issue:** Add error logging to the calculator so failures and invalid usage can be recorded in a local log file. Log relevant problems such as invalid input, unsupported operations, and calculation errors without mixing them with normal operation history. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Implement persistent error logging (separate from session-scoped operation history of Task 9)
- Log three explicit error categories: invalid input, unsupported operations, calculation errors
- Error log must be distinct from operation history file (Task 9)
- Update test suite to verify error logging behavior and maintain consistency

**Explicit Requirements:**
- **Functional:** Create and maintain persistent error log file
- **Functional:** Log invalid input errors (non-numeric, type mismatches, missing/wrong operand count)
- **Functional:** Log unsupported operation errors (unrecognized operation names/symbols)
- **Functional:** Log calculation errors (division by zero, domain violations, overflow/underflow)
- **Functional:** Separate error log from operation history; no mixing of error records with successful operation entries
- **Testing:** Update tests to verify error logging and maintain consistency

**Ambiguities & Gaps:**
- **Error log file location:** No specification of where log file should be created (current working directory? app directory? configurable?)
- **Error log file naming:** No specification (error_log.txt? errors.log? calculator_errors.log?)
- **Log file format:** No specification of format (plain text, CSV, JSON, structured?)
- **Log entry content:** Ambiguous what metadata to include:
  - Timestamp (ISO 8601? Unix epoch? Human-readable? Timezone?)
  - Operation name (or "unknown" if unrecognized?)
  - Input values (full values or sanitized?)
  - Error reason/description (stack trace? Summary only?)
  - Error category identifier?
- **Log retention policy:** Unclear if error log should persist across sessions or reset:
  - Task 9 history is session-scoped (cleared between sessions)
  - Should error log accumulate indefinitely or implement rotation/archival?
  - If persistent, should old errors be purged?
- **Log file lifecycle:** Should log file be created only on first error (lazy init) or at application startup?
- **Error detail level:** For operation-specific errors (domain violations), log the numeric value, the operation, or both?
- **Coverage of input validation errors:** Task 8 introduces input validation and retry logic:
  - Does "max retry attempts reached" count as one error or multiple?
  - Should final "session terminated" message be logged?
  - Are validation errors (invalid input) distinct from domain errors (e.g., sqrt of negative)?
- **Performance impact:** Should error logging be synchronous or buffered? Required to block on write or can be asynchronous?
- **Mode coverage:** Should both interactive (Task 5) and CLI (Task 7) modes log errors? Or only specific modes?
- No comments provided; issue body is minimal
- No test examples or acceptance criteria provided
- No mention of error message locale or i18n

**Assumed Resolution (for Architect):**
- **File location:** Same directory as operation history (Task 9); likely current working directory or configurable
- **File name:** `error_log.txt` (consistent with `history.txt` from Task 9)
- **Format:** Structured text/CSV with pipe-delimited fields: `timestamp | error_category | operation | inputs | error_description`
- **Timestamp:** ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) for consistency and reproducibility
- **Log entry examples:**
  - `2026-04-24T13:33:29Z | invalid_input | unknown | ['abc', '5'] | non-numeric input: 'abc'`
  - `2026-04-24T13:33:45Z | unsupported_operation | invalidop | [] | operation 'invalidop' not recognized`
  - `2026-04-24T13:34:01Z | calculation_error | divide | [10, 0] | division by zero`
  - `2026-04-24T13:34:15Z | calculation_error | sqrt | [-4] | cannot compute square root of negative number`
- **Persistence:** Append to error log file across sessions (do not clear); error log is persistent unlike operation history
- **Lazy initialization:** Create error log file on first error occurrence (not at startup)
- **Performance:** Synchronous write for consistency and auditability (errors are important)
- **Mode coverage:** Both interactive and CLI modes must log errors
- **Error categories (from Tasks 1, 7, 8):**
  - **invalid_input:** Task 8 validation errors (non-numeric, type mismatch, missing operand, wrong operand count)
  - **unsupported_operation:** Task 7 CLI mode or interactive mode unrecognized operation
  - **calculation_error:** Task 1 error handling (division by zero), Task 4 domain violations (sqrt negative, log non-positive), any math overflow/underflow
- **Test updates:** New tests should verify:
  - Error log file created on first error
  - Correct error category logged for each error type
  - Error log entries include timestamp, operation, inputs, and description
  - Operation history (Task 9) remains unaffected (no errors in history file)
  - Error log remains separate from history (distinct files, no cross-contamination)
  - Both interactive and CLI modes log errors
  - Multiple errors accumulate in log file

**Context from Related Issues:**
- V3 Task 9 (#396): Operation history file (Task 10 must coexist and not mix with history)
- V3 Task 8 (#393): Input validation (error log must capture all validation failures)
- V3 Task 7 (#390): CLI mode (error log must cover CLI errors)
- V3 Task 5 (#384): Interactive mode (error log must cover interactive errors)
- V3 Task 1 (#372): Division-by-zero error handling (establishes what constitutes an error)
- V3 Tasks 2-4: Operation implementations (error log must capture errors from all operations)

**Patterns:**
- V3 Task 10 is logging/observability task following Task 9 (operation history)
- Task 10 consolidates error handling from Tasks 1, 7, 8 into structured, persistent log file
- V3 sequence: error handling (1) → test suite (2) → operations (3-4) → interactive UI (5) → CLI (7) → validation (8) → operation history (9) → error logging (10)
- Task 10 is likely final integration/observability task for V3
- Minimal specification consistent with V3 series; key ambiguities are file location, format, retention policy
- "ai-implement:structured-team" label consistent; no new operations, pure observability/logging addition
- Task 10 must coexist with Task 9's operation history; both mechanisms must be independent and non-interfering
- Error logging is distinct from operation history: history is session-scoped and contains successful operations; error log is persistent and contains failures

### 2026-04-24 | V3 Task 11 - Structured/team (Issue #402)

**Issue:** Refactor the calculator so calculation logic is separated from user interaction and interface handling. Keep the application object-oriented and preserve the current calculator behavior while making the code easier to maintain and reason about. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Refactor to enforce separation of concerns: isolate calculation logic from UI/interaction
- Maintain object-oriented design (no procedural flattening)
- Preserve all existing calculator behavior (operations, error handling, validation, logging)
- Keep tests passing and consistent with refactored code
- This is an architectural refactoring task, not a feature addition task
- Part of final V3 integration sequence (follows Tasks 1-10 feature work)

**Explicit Requirements:**
- **Functional:** All operations from Tasks 1-4 must work identically
- **Functional:** Input validation from Task 8 must work identically
- **Functional:** CLI mode (Task 7) and interactive mode (Task 5) must work identically
- **Functional:** Operation history (Task 9) and error logging (Task 10) must work identically
- **Non-Functional:** Code must be easier to maintain and reason about than pre-refactoring
- **Non-Functional:** Preserve object-oriented structure (classes, inheritance, composition)
- **Testing:** All existing tests must pass without modification to behavior assertions

**Ambiguities & Gaps:**
- **Specific architectural pattern:** No specification of which design pattern(s) to use (MVC? Layered architecture? Hexagonal? Strategy pattern?)
- **Module/class organization:** Task does not specify how to organize code into modules or classes
- **Refactoring scope:** Unclear whether tests should be restructured or only source code
- **Success metrics:** "Easier to maintain and reason about" is subjective; no measurable criteria specified
- **Interface abstraction:** Should input modes (interactive, CLI) be abstracted behind a unified interface?
- **Backwards compatibility:** All existing tests expect current behavior; task requires preservation
- **Degree of separation:** How tightly should layers be separated? (dependency injection? direct coupling? facade pattern?)
- No comments provided; issue body is minimal
- No design diagrams or architectural sketches provided
- No examples of "poor maintainability" in current code or "good maintainability" target state

**Assumed Resolution (for Architect):**
- **Architecture:** Recommend layered or hexagonal architecture with clear separation:
  1. **Core Logic Layer:** Pure calculation functions, operation registry, error types (no I/O, no UI)
  2. **Input/Validation Layer:** Input parsing, validation, error recovery (CLI args, interactive prompts)
  3. **UI Layer:** Interface handling (interactive loop, CLI dispatcher, result formatting)
  4. **Persistence Layer:** History and error logging (file I/O)
- **Module Organization:** Recommend file structure like:
  - `src/calculator/core.py` — calculation logic, operation definitions
  - `src/calculator/validation.py` — input validation, operand parsing
  - `src/calculator/input.py` — input modes (interactive, CLI)
  - `src/calculator/persistence.py` — history and error logging
  - `src/calculator/main.py` — entry point, mode dispatcher
- **Object-Oriented Design:** Use classes for:
  - Operation abstraction (base Operation class with subclasses for each operation)
  - Calculator engine (Calculator class managing state and operation dispatch)
  - Input handlers (InteractiveInput, CLIInput classes)
  - Validators (InputValidator, OperandValidator classes)
  - Loggers (HistoryLogger, ErrorLogger classes)
- **Backwards Compatibility:** All behavior must remain identical; test assertions must not change, only test structure may adapt
- **Success Metrics (suggested):**
  - Core logic is testable in isolation (no side effects, no I/O)
  - Each class has single, clear responsibility (SRP)
  - Input and UI layers can be tested without triggering actual calculations
  - Adding a new operation requires change in only one place (core logic)
  - Adding a new input mode requires change in only one place (input layer)

**Context from Related Issues:**
- V3 Task 1 (#372): Division-by-zero error handling (must preserve)
- V3 Task 2 (#375): Unit test suite (must pass without behavior changes)
- V3 Tasks 3-4 (#378, #381): Operations implementations (must work identically)
- V3 Task 5 (#384): Interactive mode (must work identically)
- V3 Task 7 (#390): CLI mode (must work identically)
- V3 Task 8 (#393): Input validation (must work identically)
- V3 Tasks 9-10 (#396, #399): Logging (must work identically)

**Patterns:**
- V3 Task 11 is final refactoring/integration task; consolidates all prior feature work into clean architecture
- V3 sequence: error handling (1) → test suite (2) → operations (3-4) → interactive (5) → CLI (7) → validation (8) → logging (9-10) → refactoring (11)
- Minimal specification consistent with V3 series; architect must make design decisions about layer separation, module organization
- "ai-implement:structured-team" label consistent; no new features, pure architectural restructuring
- Task 11 is likely final V3 task; represents completion of structured/team evolution cycle
- Key assumption: current codebase has calculation logic mixed with UI/interaction; refactoring will separate these concerns
- No mention of performance optimization or new dependencies; refactoring is purely structural
- Task is about code organization and maintainability, not behavior change

### 2026-04-24 | V3 Task 13 - Structured/team (Issue #408)

**Issue:** Add written documentation for the calculator application so its features, usage, and project structure are easier to understand. Document how to run and use the calculator, including its available functionality and supported interaction modes. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Create written documentation for calculator application
- Document features (arithmetic operations, advanced math, error handling, validation)
- Document usage (how to run, interaction modes, user workflows)
- Document project structure (modules, architecture, organization)
- Update tests if needed to remain consistent

**Explicit Requirements:**
- **Documentation:** Written documentation covering:
  - Features: What the calculator can do (operations, modes, capabilities)
  - Usage: How to run and use (CLI mode, interactive mode, mode switching)
  - Project structure: How code is organized (module layout, architecture)
  - Interaction modes: CLI mode vs. interactive mode; normal vs. scientific mode
- **Testing:** Update relevant tests if application behavior changed or documentation requirements necessitate test changes

**Ambiguities & Gaps:**
- **Documentation format:** No specification of format (Markdown? HTML? Plain text? Multiple formats?)
- **Documentation location:** Unclear where documentation should be placed (README.md? docs/? separate files?)
- **Documentation scope:** Incomplete specification of what exactly must be documented:
  - Should it cover all operations individually or just mention operation categories?
  - Should error messages and error handling be documented?
  - Should it include code examples or interactive sessions?
  - Should it document the full project history or only current state?
- **Intended audience:** Not specified (developers? end users? both?)
- **Level of detail:** Unclear how deep documentation should go:
  - Installation/setup instructions?
  - Architecture diagrams reference?
  - Configuration options?
  - Troubleshooting guide?
  - Development/extension guidelines?
- **Test updates scope:** Unclear what test updates are needed:
  - Are there documentation-specific tests?
  - Should tests change or just be made consistent if code changed?
  - Are docstring/doctest requirements implied?
- **Integration with existing docs:** Unclear if this supplements or replaces any existing documentation from Task 6 (PlantUML diagrams, Issue #249)
- No comments provided; issue body is minimal
- No acceptance criteria or examples of target documentation quality provided
- No mention of whether documentation should be versioned or kept in sync with code changes

**Assumed Resolution (for Architect):**
- **Format:** Markdown (standard for GitHub projects, readable in text editors and on GitHub web)
- **Location:** Root-level `README.md` file as primary documentation; may supplement with `docs/` directory if extensive content needed
- **Documentation sections should include:**
  1. **Project Overview:** Brief description of calculator purpose and capabilities
  2. **Features:** List of supported operations (arithmetic, scientific, error handling, validation)
  3. **Interaction Modes:** Explain CLI mode and interactive mode; how to select which mode
  4. **Normal Mode vs. Scientific Mode:** Clarify scope of operations in each mode
  5. **Usage Instructions:**
     - How to run in interactive mode (e.g., `python -m calculator` or similar)
     - How to run in CLI mode with examples (e.g., `python -m calculator add 5 3`)
     - How to switch modes in interactive mode
  6. **Project Structure:** Describe module layout and main components (from Task 11 refactoring)
  7. **Operation Reference:** List operations with brief descriptions (or link to separate file if long)
  8. **Error Handling:** Explain error messages and recovery (retry logic from Task 8)
  9. **Session History & Logging:** Brief note on history/error log files (from Tasks 9-10)
- **Scope of test updates:**
  - If application behavior changed (unlikely in pure documentation task), update corresponding tests
  - If docstrings added to functions, may require doctest verification
  - Existing test suite should continue to pass without modification
  - Assume minimal test changes unless application code changed in Task 13
- **Relationship to Task 6 (PlantUML diagrams):** Documentation should reference or embed diagrams if helpful; diagrams support written documentation
- **Audience assumption:** Mixed (both end users and developers); write clearly for both
- **Examples:** Include at least one interactive mode session example and one CLI mode example

**Context from Related Issues:**
- V3 Task 6 (#386): PlantUML documentation diagrams (Task 13 should reference or build on these)
- V3 Tasks 1-11 (#372-405): All feature work and refactoring that Task 13 must document
- V3 Task 12 (#405): Modular refactoring (architecture Task 13 documents)
- V2 Task 13 (#270): Earlier documentation task (may provide template or context)
- Issue #249: PlantUML diagrams task (provides visual documentation)

**Patterns:**
- V3 Task 13 is documentation/user-facing task following Task 12 modular refactoring
- V3 sequence: core features (1-4) → interactive/CLI (5, 7) → validation (8) → logging (9-10) → refactoring (11) → documentation (13)
- Task 13 is near-final task in V3 cycle; represents capture of all prior work in user-accessible form
- Minimal specification consistent with V3 series; documentation architect/writer has flexibility in format and organization
- "ai-implement:structured-team" label consistent; no new features or code, pure documentation/communication
- Task 13 completion means calculator is documented for users and developers; ready for release or deployment
- Ambiguities are typical for documentation tasks: audience, level of detail, scope are creative decisions, not technical ambiguities
- Similar to Task 6 (PlantUML diagrams) but higher-level; diagrams are visual aids, Task 13 is narrative documentation

### 2026-04-24 | V3 Task 14 - Structured/team (Issue #411)

**Issue:** Add a scientific mode to the calculator and allow the user to switch between normal and scientific functionality in interactive mode. Keep normal mode limited to the standard calculator operations, and make scientific mode provide an expanded set of advanced mathematical functions. Update relevant tests as needed so they remain consistent with the current version of the application.

**Key Requirements Identified:**
- Partition calculator operations into two distinct functional groups: normal (arithmetic only) and scientific (advanced math)
- Allow user to switch between modes in interactive REPL session
- Normal mode: add, subtract, multiply, divide (4 operations)
- Scientific mode: factorial, square, cube, sqrt, cbrt, power, log, ln (8 operations)
- All 12 operations implemented in prior tasks (Tasks 1-4); Task 14 introduces mode partitioning and mode-switching capability
- Update tests to verify mode-aware behavior and mode switching

**Explicit Requirements:**
- **Functional:** Mode partitioning — normal vs. scientific operation availability
- **Functional:** Interactive mode switching (via command or menu)
- **Functional:** Operation availability validation (reject op not in current mode with clear error)
- **Functional:** CLI mode defaults to normal mode (stateless, no mode switching in CLI)
- **Testing:** Update tests to cover mode partitioning, switching, error handling

**Ambiguities & Gaps:**
- **Mode-switch command syntax:** Unspecified how user switches modes in interactive mode
  - Examples: `mode scientific`, `switch sci`, `scientific`, menu-driven (1=normal, 2=scientific), numbered commands
  - Current assumption: architect to decide based on existing command patterns (e.g., "history" command from Task 9)
- **CLI mode behavior:** Unclear if CLI should accept mode flag (e.g., `--mode scientific factorial 5`) or always default to normal
  - Current assumption: CLI always normal mode; if scientific op requested, error returned (op not found in normal mode)
- **Current mode display:** No spec on whether mode is shown in interactive prompts or only on switch
  - Examples: `[Normal] >> `, `[Scientific] >> `, or only in feedback ("Switched to Scientific Mode")
- **Session state after mode switch:** Unclear if mode switch should clear session state, reset history, etc.
  - Current assumption: Fresh state on mode switch (no carryover of intermediate results or partial operations)
- **Operation registry refactoring:** No spec on how to implement mode-scoped operation lookup
  - Options: single registry with mode metadata, separate registries per mode, registry.get_operation(name, mode=x), or registry[mode][name]
- **Mode persistence:** Should mode choice persist across session restarts or reset to normal mode each time?
  - Current assumption: Reset to normal mode on session start (stateless)
- **History/logging behavior:** Should history and error log be mode-aware?
  - Current assumption: History and error logging operate independently of mode; records include operation name (implicitly mode-identified by operation)
- No comments provided; issue body is minimal
- No test examples or acceptance criteria provided
- No mention of whether mode-switching should affect other features (validation, error handling, etc.)

**Assumed Resolution (for Architect):**
- **Mode partitioning:**
  - Normal mode: add, subtract, multiply, divide
  - Scientific mode: factorial, square, cube, sqrt, cbrt, power, log, ln
- **Mode-switch mechanism (TBD):** Recommend a command like "mode <name>" (e.g., "mode scientific", "mode normal") consistent with "history" pseudo-command from Task 9
- **CLI default:** Always normal mode; no CLI flag for mode selection (engineering simplification; supports stateless operation)
- **Operation validation:** When user enters operation, check against current mode's operation set; if not found, return error like "factorial not available in normal mode"
- **Mode display:** Recommend showing current mode in interactive prompt (e.g., `Normal >> `) or in mode-switch feedback
- **Session state:** Mode switch clears any pending state; user starts fresh in new mode
- **Operation registry:** Suggest refactoring `_build_registry()` to return mode-scoped registry or add mode parameter to operation lookup method
- **History/Error logging:** No changes to history or error logging mechanisms; record operation name (implicitly identifies mode)
- **Test coverage:** New tests should verify:
  - Operations in normal mode work; scientific ops rejected with clear error
  - Operations in scientific mode work; arithmetic ops accessible but may require testing mode-switch path
  - Mode-switch command parsing and execution
  - Error message for unavailable operation in current mode
  - Backward compatibility: all existing tests pass

**Context from Related Issues:**
- V3 Task 13 (#408): Documentation (README already mentions normal vs. scientific modes from this Task 14 implementation; may need clarification of mode-switch syntax in docs)
- V3 Task 12 (#405): Modular refactoring (Task 14 builds on refactored architecture)
- V3 Tasks 1-11: All prior features (error handling, operations, validation, logging, refactoring) must coexist with mode partitioning
- V2 Task 14 (#273): Earlier scientific mode task (suggests scientific mode is a long-standing feature request; V3 Task 14 formalizes mode switching)

**Patterns:**
- V3 Task 14 is organizational/feature-refinement task, not feature-addition task
- Task 14 concludes V3 structured/team cycle; represents finalization of calculator feature set (no new operations, just mode organization)
- V3 sequence: error handling (1) → test suite (2) → operations (3-4) → interactive (5) → CLI (7) → validation (8) → logging (9-10) → refactoring (11) → documentation (13) → mode-switching (14)
- Minimal specification consistent with V3 series; key ambiguities are mode-switch syntax and CLI behavior
- "ai-implement:structured-team" label consistent; no new operations, pure organizational/UX refinement
- Task 14 likely final V3 task; represents completion of calculator feature work and mode organization
- Ambiguities are straightforward engineering decisions (command syntax, registry design); no domain confusion
- Task builds on all prior work; must integrate with existing error handling, validation, history, logging, and refactored architecture

### 2026-04-25 | PR #459 Review Feedback Analysis (Issue #411 implementation)

**Context:** PR #459 implements Issue #411 (scientific mode with mode switching) but received blocking feedback from the repository owner.

**Unresolved Reviewer Feedback (BLOCKING):**
The single PR comment from DanielRiha8906 (owner) marks **"Fix needed"** and specifies five categories of required work:

1. **Missing Scientific Functions (12 operations required)**
   - Trigonometric: sin, cos, tan
   - Inverse trigonometric: asin, acos, atan (with domain constraints: [-1, 1])
   - Hyperbolic: sinh, cosh, tanh
   - Exponential: exp
   - Mathematical constants: pi, e
   - All must be implemented as Operation subclasses in `src/calculator/operations/scientific.py`
   - All must be registered in `_build_registry()` under MODE_SCIENTIFIC only

2. **Corrected Normal/Scientific Mode Split (CRITICAL ARCHITECTURAL FIX)**
   - Current PR implementation: normal mode has ONLY 5 operations (add, subtract, multiply, divide, modulo) — too restrictive
   - Pre-task (before mode split): calculator supported 10+ operations including square, sqrt, power, log, ln, factorial
   - **Required correction:** Normal mode must include ALL pre-split operations (10+ operations)
   - **Superset relationship:** Scientific mode must be a SUPERSET containing all normal mode operations PLUS 12 new scientific functions
   - **Current error:** The PR's mode split is backward-incompatible; it removes previously supported functions from normal mode
   - Update `_SCIENTIFIC_OPS_BLOCKED` or equivalent data structure to reflect correct split

3. **Preserve and Verify Interactive Mode Switching**
   - Mode-switch commands (e.g., `mode normal`, `mode scientific`) must parse case-insensitively
   - Support aliases: `normal | norm | scientific | sci`
   - Registry must be immediately rebuilt on mode switch (so operations become accessible/blocked instantly)
   - Failure counting must still apply to mode-rejection errors
   - Mode switching must work correctly with ALL newly added scientific functions

4. **Comprehensive Test Coverage for Scientific Functions**
   - Each new function: test correct output, domain error handling, mode availability, mode absence
   - Mode switching with scientific functions: verify correct exposure/hiding with interactive commands
   - Consecutive-failure counting must include mode-rejection errors
   - Validate case-insensitive command parsing and alias handling
   - All pre-existing tests must remain green (zero regressions)

5. **Update Interactive Prompts**
   - Prompt string in `_run_interactive_loop()` must dynamically list available operations per current mode
   - Include all newly added scientific functions in the list when in scientific mode
   - Update list to reflect corrected normal mode operation set
   - Provide clear indication of which mode is active (e.g., mode prefix or feedback message)

**Acceptance Criteria (Blocking PR Merge):**
- [ ] All 12 new scientific functions implemented and registered
- [ ] Normal mode includes full pre-split operation set (not just 5 operations)
- [ ] Scientific mode is true superset (all normal + all scientific)
- [ ] Interactive mode-switch command parsing works correctly
- [ ] Registry rebuild happens immediately on mode switch
- [ ] All new functions have comprehensive tests (correctness, domain errors, mode availability)
- [ ] Pre-existing tests remain green (no regressions)
- [ ] Interactive prompts dynamically reflect available operations
- [ ] PR mergeability changes from "unstable" to "clean"

**Priority:** MUST HAVE — all items block PR merge

**Patterns Identified:**
- Architectural mismatch: mode split design diverges from intent (too restrictive in normal mode)
- Missing feature gap: 12 scientific functions not implemented despite being explicitly required in reviewer feedback
- Backward compatibility violation: normal mode less capable than pre-split calculator
- Test coverage incomplete: no tests for new scientific functions or correct mode split behavior

### 2026-04-25 | V3 Task 15 - Structured/team (Issue #414)

**Issue:** Add a graphical user interface for the calculator application using tkinter. The GUI must provide access to the calculator's currently supported functionality (both normal and scientific modes). The interface must allow operation selection, operand entry, result display, and session history viewing. The GUI must be an extension of the application, not a replacement—existing CLI/interactive modes remain available and fully functional. Update relevant tests to ensure consistency.

**Key Requirements Identified:**
- Build tkinter-based GUI for the calculator application
- Support both normal and scientific mode operation selection in the GUI
- Support operand entry and result display
- Support session history viewing within the application
- GUI is an extension, not a replacement (CLI and interactive modes remain fully functional)
- All existing tests must remain consistent with the new GUI functionality

**Explicit Requirements:**
- **Functional:** GUI access to all currently supported calculator operations (from prior tasks: arithmetic, factorial, square, cube, sqrt, cbrt, power, log, ln, and upcoming from PR #459: trig, inverse trig, hyperbolic, exponential, constants)
- **Functional:** GUI operation selection mechanism (buttons? dropdown menu? search box?)
- **Functional:** GUI operand entry (text fields? spinboxes? numeric input widgets?)
- **Functional:** GUI result display (labels? text output area? history panel?)
- **Functional:** Session history viewing within GUI (history panel? window? integration with result display?)
- **Functional:** Normal mode vs. Scientific mode toggling in GUI (mode selector widget?)
- **Functional:** All existing CLI and interactive modes remain fully operational
- **Testing:** Update relevant tests to accommodate GUI code and maintain test suite consistency

**Ambiguities & Gaps (Inherent to Task):**
- **GUI framework:** tkinter is specified; no version constraints
- **Operation display in GUI:** Unclear how operations are listed/accessible:
  - Grid of buttons (one per operation)? Unscalable for 20+ operations
  - Dropdown menu? Searchable menu? Categorized menus?
  - Text input with autocomplete?
  - Operation palette scrollable list?
- **Operand input:** Unclear how many operand fields to display:
  - Fixed number (e.g., 2 fields always visible, 1 for unary ops unused)?
  - Dynamic based on selected operation (show 1 for unary, 2 for binary)?
  - Text input parsing (user enters "5" and "3", parser determines count)?
- **Mode switching in GUI:** Unclear how user toggles normal ↔ scientific mode:
  - Toggle button? Radio buttons? Menu item? Tab interface?
  - Does mode switch clear pending operands or preserve state?
- **Result display:** Unclear what to show:
  - Numeric result only? Full operation transcript (op + args + result)?
  - Error messages inline or in separate area?
  - Precision/formatting of numeric results?
- **History viewing:** Unclear what "view session history" means in GUI context:
  - Display history in dedicated panel/window?
  - Scrollable list of past operations?
  - Integration with file-based history from Task 9 or session-only view?
- **GUI layout:** No specification of visual organization:
  - Single window with all controls? Multi-window? Tabbed interface?
  - Responsive layout? Fixed size? Resizable?
- **Error handling in GUI:** How are errors presented:
  - Message box? Status bar? Error log panel?
  - Same validation/retry logic as Task 8, or simplified GUI-specific handling?
- **Relationship to existing modes:** Task states "keep existing behavior available outside GUI" but unclear:
  - Can same process run both GUI and CLI simultaneously? (likely not)
  - Should GUI be optional (e.g., `--gui` flag or default entry point)?
  - Does GUI mode prevent interactive/CLI usage or supplement it?
- **Test strategy:** Unclear how to test GUI code:
  - Unit tests on GUI functions? Integration tests? Manual testing?
  - Mock tkinter? Use a testing framework like unittest.mock?
  - How to verify GUI behavior (button clicks, text input) in automated tests?
- No comments provided; issue body is minimal
- No wireframes, mockups, or design specifications
- No mention of accessibility, themes, or UI customization
- No platform/OS requirements (tkinter is cross-platform but behavior may vary)

**Assumed Resolution (for Architect):**
- **GUI Architecture:** Separate GUI layer using tkinter, not integrated into core calculator logic:
  - `src/calculator/gui.py` or `src/calculator/ui/` directory for GUI-related code
  - GUI layer calls calculator.core functions; maintains separation of concerns from Task 11 refactoring
  - Keep `main.py` decision logic: if `--gui` flag or default, launch GUI; otherwise, interactive/CLI modes
- **Operation Selection:** Recommend dynamic dropdown menu or searchable/categorized operation selector:
  - Dropdown menu populated from operation registry (allows easy addition of new operations)
  - If list is long (20+), group operations: Normal Mode (add, subtract, etc.) | Scientific Mode (factorial, sqrt, etc.)
  - Alternative: tabbed interface with Normal and Scientific tabs, each with operation buttons/list
- **Operand Input:** Dynamic widget approach:
  - After operation selected, GUI determines operation arity (unary vs. binary)
  - Display appropriate number of input fields
  - Accept numeric input; validation deferred to calculator core (consistent with Task 8 error handling)
- **Result Display:** Full operation transcript:
  - Show operation name + operands + result (e.g., "add(5, 3) = 8")
  - Error messages appear in same result area (red text or error styling)
  - Results accumulate in scrollable output/history panel
- **History Viewing:** Integrated session history panel:
  - Display list of operations performed in current session (from calculator.core session history, not file)
  - Clicking a history entry shows operation details (operation, operands, result)
  - Alternative: separate "History" window/panel showing all session operations
  - Note: Distinct from file-based history (Task 9); GUI shows session-only history unless explicitly integrated
- **Mode Switching in GUI:** Toggle button or radio buttons:
  - Two radio buttons or toggle: "Normal Mode" | "Scientific Mode"
  - Mode switch dynamically updates operation dropdown/selector (shows only operations available in selected mode)
  - Preserves mode choice across operations (if user switches to scientific, stays in scientific until manually switched back)
  - Clear indication of current mode (e.g., mode label at top of window or highlighted radio button)
- **GUI Layout:** Single main window with panes:
  - Pane 1 (left/top): Operation selector + operand input fields
  - Pane 2 (center/right): Result display area (scrollable text or output panel)
  - Pane 3 (bottom): Session history panel (list of operations) or separate History window
  - Mode toggle at top
  - Resizable window; no fixed minimum size requirement (responsive design not required)
- **Error Handling in GUI:** Consistent with Task 8 validation:
  - Invalid operand input: show error message in result area (e.g., "Invalid operand: 'abc' is not a number")
  - Operation errors (division by zero, sqrt of negative): show error message in result area
  - Failure counting from Task 8 still applies if GUI uses same calculator backend
  - No modal dialogs for errors; display in result area for cohesive UX
- **GUI/CLI/Interactive Coexistence:**
  - Main entry point (`main.py` or `__main__.py`) decides which mode to enter:
    - If `--gui` flag provided, launch tkinter GUI
    - Else if arguments provided, enter CLI mode (from Task 7)
    - Else enter interactive mode (from Task 5)
  - GUI is optional; CLI and interactive modes remain primary entry points
  - Only one mode runs per process invocation (not simultaneous GUI + CLI in same process)
- **Test Strategy:**
  - GUI code should be minimally testable; focus on calculator.core logic tests (already exist)
  - For GUI-specific code (widget setup, event handlers), consider:
    - Separate GUI logic from tkinter calls (e.g., a `GUIController` class with testable methods, separate from `TkinterGUI` widget code)
    - Mock tkinter imports or use a GUI testing library like `pytest-qt` (if switching to Qt) or manual integration tests
    - Or defer GUI testing to manual QA (acceptable for single-file GUI module)
  - All existing tests (from Tasks 1-14) must continue to pass unmodified
  - New tests may be added for GUI-specific logic if separated from tkinter directly
- **Implementation Notes:**
  - Tkinter is bundled with Python; no new dependencies required
  - GUI must not modify calculator.core behavior; it is a pure interface layer
  - Keep GUI code isolated in its own module(s) to maintain separation of concerns
  - Consult current codebase structure (from Tasks 11-12 refactoring) for module organization

**Context from Related Issues:**
- V3 Task 14 (#411): Scientific mode with mode switching (GUI must expose mode toggle and operation categories)
- PR #459: Scientific mode implementation with feedback on missing trigonometric/hyperbolic/exponential functions (GUI must display all implemented operations)
- V3 Tasks 1-13 (#372-408): All prior calculator functionality must be accessible via GUI
- V3 Task 11 (#402): Refactored separation of concerns (GUI fits as input/UI layer above calculator.core)
- V3 Task 9 (#396): Session history (GUI history panel should integrate or reference this)

**Patterns:**
- V3 Task 15 is the final UI/user-facing task in the structured/team cycle
- Task 15 follows completion of all core operations (Tasks 1-4), refactoring (Tasks 11-12), and mode organization (Task 14)
- Task 15 is an "optional" feature in the sense that it supplements (not replaces) existing CLI/interactive modes
- Minimal specification consistent with V3 series; architecture decisions (layout, widget choices) left to implementer
- "ai-implement:structured-team" label consistent; no new operations, pure UI/UX addition
- Task 15 likely completes V3 structured/team cycle: all calculator features accessible via multiple interfaces (CLI, interactive, GUI)
- Key assumption: GUI is a convenience feature; core calculator behavior unmodified
- No mention of themes, styling, or visual polish; basic functional GUI sufficient

**Priority Assessment:**
- GUI feature is a "Could Have" in terms of core calculator function (existing modes remain fully viable)
- However, task is explicitly required by Issue #414; treat as "Must Have" for this specific task
- All acceptance criteria must be verifiable in automated tests where possible; GUI interactions may require manual verification

### 2026-04-25 | V3 Task 16 - Structured/team (Issue #464)

**Issue:** Redesign the calculator GUI to look like a modern calculator app inspired by iOS. The goal is a clean, minimal dark interface with a fixed layout (not responsive). Replaces the generic tkinter GUI from Task 15 with a professional, modern appearance emphasizing visual hierarchy through color and typography.

**Key Requirements Identified:**
- Redesign existing GUI from Task 15 to modern iOS-inspired aesthetic
- Replace generic GUI with dark theme, professional button styling, and specific layout grid
- Standard mode: fixed 4-column × 5-row button grid with specified button positions and functions
- Scientific mode: additional grid on left side containing scientific operations
- Precise color scheme: black (#000000) background, dark grey (#333333) standard buttons, orange (#FF9500) primary operators, light grey (#A5A5A5) utility buttons
- Result display: 24pt+ white text, right-aligned on black background
- Button styling: flat (no 3D relief), square or slightly rounded, uniform size
- Use mathematical symbols for button labels (√, x², ÷, ×, −, n!, ln, etc.)
- Pure presentation/styling change; no logic modifications

**Explicit Requirements:**
- **Layout (Standard Mode):**
  - 4 columns, 5 rows (20 buttons)
  - Row 1: C, Del, Mode, /
  - Row 2: 7, 8, 9, *
  - Row 3: 4, 5, 6, (empty)
  - Row 4: 1, 2, 3, −
  - Row 5: 0 (2 columns wide), ., =
- **Layout (Scientific Mode):** Additional grid on left; exact layout TBD but displays all scientific functions
- **Color Scheme:**
  - Window background: #000000 (pure black)
  - Standard operation buttons: #333333 (dark grey)
  - Primary operators (±, ×, ÷): #FF9500 (orange)
  - Utility buttons (C, Del, Mode, ., =): #A5A5A5 (light grey)
- **Typography:**
  - Result display: 24pt or larger, white text, right-aligned
  - Button labels: short symbols (+, −, ×, ÷, √, x², xʸ, n!, ln, log)
- **Button Styling:**
  - Flat appearance (no 3D relief borders)
  - Square or slightly rounded corners
  - Uniform size within grid
  - Compact, minimal aesthetic (iOS Calculator inspired)
- **Functionality:**
  - All buttons functional (numeric, operators, utility)
  - Clear (C) resets state and display
  - Delete (Del) removes last digit
  - Mode toggle switches between normal and scientific
  - Equals (=) computes and displays result
  - Decimal point, numeric input, operator logic all work unchanged
- **Non-Functional:**
  - No changes to calculation logic or operation implementations
  - No changes to error handling, validation, or logging from prior tasks
  - All existing tests must pass without modification
  - CLI and interactive modes remain available and unchanged

**Ambiguities & Gaps:**
- **Scientific grid layout on left:** Issue states "add a grid to the left... but not shown methods" — phrasing unclear
  - Interpretation: Scientific operations hidden in normal mode; left sidebar/grid displays them when mode switches to scientific
  - Exact positioning (fixed width sidebar vs. expanded grid), button count, and layout of scientific grid not specified
- **Visual feedback on button interaction:** No specification of hover/press effects
  - Assumed: Basic tkinter visual feedback (color change, relief change on click) sufficient
- **Error display:** How errors shown (division by zero, domain violations)?
  - Assumed: Error messages appear in result display area, likely with styling/color differentiation
- **Decimal point handling:** Prevent multiple decimals in one number?
  - Assumed: Yes, standard calculator behavior
- **Leading zeros:** Display "03" or "3" after pressing 0 then 3?
  - Assumed: Standard behavior (likely "3" to match iOS)
- **Scientific mode state:** Does mode switch clear pending operands?
  - Assumed: Mode switch provides fresh state; no carryover of partial operations
- **Responsive design:** Grid is fixed (4×5) — no dynamic resizing?
  - Implied: Fixed layout, not responsive; window may be resizable but grid structure unchanged
- **Accessibility:** No mention of keyboard support, screen readers, or themes
  - Out of scope per specification
- No comments provided; issue body is minimal
- No wireframes, mockups, or design specifications beyond text layout
- No mention of animations, transitions, or advanced visual effects

**Assumed Resolution (for Architect):**
- **GUI framework:** Tkinter (inherited from Task 15); no new dependencies
- **Visual design:**
  - Use tkinter Grid geometry manager for precise button positioning in 4×5 grid
  - Apply exact hex colors via tkinter button/frame background colors
  - Use tkinter font system to set result display to 24pt+ white text
  - Implement flat button appearance by setting relief=tk.FLAT and borderwidth=0
  - Apply slight rounding via tkinter's highlightthickness and compound/image properties (or accept square appearance; rounding is nice-to-have)
- **Color-based hierarchy:**
  - Dark grey (#333333) for standard numeric/operation buttons (most common interactions)
  - Orange (#FF9500) for primary operators (±, ×, ÷) to draw attention
  - Light grey (#A5A5A5) for utility buttons (C, Del, Mode) and decimal/equals to show secondary importance
  - Black background maintains minimal, professional aesthetic
- **Scientific mode display:**
  - When mode switches to scientific, dynamically update GUI to show left-side grid or expand button grid
  - All scientific operations (from PR #459: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, pi, e) become available via buttons or dropdown
  - Exact layout TBD by architect; could be:
    - Fixed left sidebar (separate pane) with scientific buttons
    - Expanded grid that adds columns/rows on left
    - Modal/popup scientific function selector
- **Button factory/helper:** Create function to generate buttons with consistent styling:
  - `create_button(text, color, row, col, command)` helper
  - Centralizes color, font, size, relief settings for maintainability
- **Result display widget:**
  - Use tkinter Label or Entry (read-only) with large font, right-alignment, white color, black background
  - Update on every operation or numeric input
- **Mode toggle logic:**
  - Link to Task 14's mode system; mode switch triggers GUI rebuild or hiding/showing of scientific buttons
  - Clear visual indication of current mode (mode label, button highlight, or pane visibility)
- **Event binding:**
  - Button clicks → call calculator.core operation logic; delegate all computation
  - GUI remains pure presentation layer; no calculation logic in GUI code
- **Integration with Task 15 architecture:**
  - This task replaces the generic Task 15 GUI with the modern design
  - Keep GUI in separate module (`src/calculator/gui.py` or similar)
  - Entry point logic remains: `--gui` flag launches GUI (now with modern design)

**Context from Related Issues:**
- V3 Task 15 (#414): Previous GUI implementation (Task 16 redesigns/replaces this)
- PR #459: Scientific functions available in scientific mode (Task 16 must display all of them)
- V3 Task 14 (#411): Mode architecture (Task 16 uses mode system to show/hide operations)
- V3 Tasks 1-13: All calculator operations must be accessible via redesigned GUI

**Patterns:**
- V3 Task 16 is final UI/design-refinement task in V3 structured/team cycle
- Task 16 is a pure visual redesign; no functional changes or new features
- Minimal specification consistent with V3 series; specific hex colors and layout are fixed; implementation details (scientific grid layout, animation) left to architect
- "ai-implement:structured-team" label consistent; no new operations, pure UI/UX refinement
- Task 16 likely final V3 task; represents completion of calculator with professional, polished UI
- Key assumption: Task 15 GUI already exists and is functionally complete; Task 16 replaces appearance while preserving functionality
- No mention of themes, customization, or accessibility; fixed design per specification
- Task demonstrates importance of visual design in user-facing software; professional appearance enhances usability

**Priority Assessment:**
- GUI redesign is "Should Have" / "Could Have" from core calculator perspective (existing modes remain viable)
- However, task is explicitly scoped and labeled as required (Issue #464); treat as "Must Have" for this task
- All acceptance criteria are verifiable: layout matches spec, colors match hex codes, buttons function, typography meets size requirement
- Design decisions (scientific grid placement, rounding degree, spacing) are architect's choice within spec

---

