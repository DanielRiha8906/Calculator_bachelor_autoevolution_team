# RAG: github-task-analyst

## Purpose
Accumulated context from past issue analyses on this experiment branch. Each cycle entry records recurring requirement patterns, ambiguities encountered, and anything useful for the next invocation.

## Cycle Log

### Cycle: 2026-04-24 — Issue #376: V3 Task 2 - Expert/team
- **Task Type:** Test suite creation (Red phase of TDD)
- **Scope:** Unit tests for calculator's currently implemented operations
- **Key Patterns:**
  - Task is self-contained; no linked issues or comments providing additional context
  - Scope is focused and explicitly excludes refactoring (except small correctness fixes)
  - Edge cases clearly enumerated: division by zero, invalid inputs, floating-point arithmetic
  - Key ambiguity: division-by-zero behavior not specified (current implementation behavior must be tested as-is)
- **Ambiguities Flagged:**
  1. Exact list of "currently implemented operations" not provided — will be discovered during test-write phase
  2. Division by zero handling unspecified — behavior must be verified from calculator implementation
  3. Floating-point tolerance approach not mandated (exact vs. approximate equality)
- **Handoff Notes:**
  - Architect should produce test specifications covering all operations (once discovered) with normal and edge case inputs
  - Tester will write failing tests matching those specs
  - Implementer will add code only if calculator implementation itself needs fixes (unlikely, as task is test-only)
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #379: V3 Task 3 - Expert/team
- **Task Type:** New feature implementation (Green + Refactor phase of TDD)
- **Scope:** Add factorial operation to calculator
- **Key Patterns:**
  - Clear, self-contained feature request with explicit boundary cases (0, 1, negative, non-integers)
  - No comments or linked issues; requirements fully expressed in issue body
  - Explicit scope constraint: "avoid unrelated refactoring"
  - Part of multi-task progression (follows issue #376)
- **Ambiguities Flagged:**
  1. Factorial behavior for non-integer inputs (floats) — stated as rejection requirement but no error type specified
  2. Maximum input value not stated — mathematically unbounded, but Python int can handle it; implementation must decide on reasonable limits
  3. Return type not specified (int vs float) — presumed int based on factorial mathematical definition
  4. Integration point not specified (how factorial operation is wired into calculator API)
- **Handoff Notes:**
  - Architect must specify where factorial integrates (operation registry, CLI, API function name)
  - Tester will write failing tests for valid (0, 1, positive integers) and invalid cases (negatives, floats, edge cases)
  - Implementer receives tester's failing test names and must implement factorial function + integration to make them pass
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #382: V3 Task 4 - Expert/team
- **Task Type:** Feature expansion (add 8 new mathematical operations)
- **Scope:** Add square, cube, square root, cube root, power, log₁₀, ln as calculator operations; handle domain errors and mathematical edge cases
- **Key Patterns:**
  - Clear operation list with explicit emphasis on edge cases (domain validation for sqrt/log/ln, negative cube root handling)
  - No comments or linked issues; all requirements in issue body
  - Explicit constraint: "avoid unrelated refactoring"
  - Continuation of task progression (follows issues #376, #379)
  - Mixed unary (6 ops) and binary (1 op) operation types; cube root requires special handling (negative domain valid unlike sqrt)
- **Ambiguities Flagged:**
  1. Power operation edge cases (0^0, negative base with fractional exponent) — no specification; assumed Python `**` semantics
  2. Error type/signaling — not specified; assumed to match existing invalid-input handling (e.g., division by zero pattern)
  3. Floating-point comparison tolerance — not specified; assumed to match existing test conventions
  4. Negative zero handling — edge case not mentioned; presumed Python default semantics
- **Handoff Notes:**
  - Architect must explicitly clarify power operation behavior for edge cases (0^0, negative base + fractional exponent)
  - Architect must produce test specs listing all 8 operations with normal and error cases; special attention to cube root (negative inputs must succeed) vs sqrt/log/ln (domain errors)
  - Tester will write failing tests for each operation + edge case
  - Implementer will integrate all operations into operation registry and make failing tests pass
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #385: V3 Task 5 - Expert/team (PR #434 Review)
- **Task Type:** PR review analysis (feedback extraction and requirements synthesis)
- **Scope:** Identify unresolved feedback on PR #434 implementing interactive user input
- **Key Finding:**
  - PR implements interactive session module (`src/interactive.py`, `src/operation_registry.py`) with 15 new passing tests
  - **Unresolved blocker:** No command-line entry point to invoke interactive mode
  - Owner feedback: "There is no way to launch the application to get into the interactive mode. Change __main__.py that when launched via python -m src, user input will be possible."
- **Requirement Extracted:**
  - `src/__main__.py` must be modified to invoke `run_interactive_session()` when package is executed via `python -m src`
  - Simplest solution: unconditionally launch interactive mode (2–5 line change)
  - Alternative interpretations possible: startup menu, CLI args, auto-detect mode — not specified
- **Ambiguities:**
  1. Exact mechanism for entry point selection (auto-launch vs. menu) not specified
  2. Whether to support both interactive and non-interactive modes from CLI not specified
  3. CLI argument syntax (if needed) not specified
- **Handoff Notes:**
  - For system architect: specification is minimal; recommend unconditional interactive mode launch as simplest solution
  - For implementer: one-file change to `src/__main__.py`; imports and calls `run_interactive_session()` from `src.interactive`
  - For tester: verify that `python -m src` (or configured entry point) successfully launches interactive loop; ensure existing tests remain green
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #391: V3 Task 7 - Expert/team
- **Task Type:** Feature implementation (CLI argument parsing and execution)
- **Scope:** Add command-line interface to calculator accepting operation and operand arguments
- **Key Patterns:**
  - Clear, self-contained feature request with concrete examples
  - No comments or linked issues; all requirements in issue body
  - Explicit scope constraint: "keep change scoped to bash-based CLI access"
  - Follows completion of issues #376, #379, #382, #385 (core operations and interactive mode established)
  - Requires support for both unary (factorial) and binary (add) operations via CLI
- **Ambiguities Flagged:**
  1. Entry point location — issue examples show `python main.py` but codebase likely uses `python -m src`; specification does not clarify
  2. Error handling behavior — "predictably for incorrect argument usage" is vague; no specification of exit codes, error messages, or exact validation order
  3. Supported operations list — task says "current operations" but does not enumerate which operations are "current" (must discover from operation registry)
  4. Operand count validation — no specification of handling mismatched operand counts (e.g., `add 5` or `factorial 5 7`)
  5. Operand type validation — no specification of behavior for non-numeric arguments (e.g., `add abc 7`)
  6. Output format — "through standard terminal output" is generic; no spec for float precision, newlines, or error output stream (stdout vs stderr)
- **Handoff Notes:**
  - Architect must clarify: (1) exact entry point (main.py vs python -m src), (2) error handling strategy (exit codes, message format), (3) operand validation order, (4) output format for results
  - Architect should produce test specs covering: valid single/multi-arg operations, missing args, excess args, non-numeric args, edge cases per operation type
  - Tester will write failing tests for all scenarios above
  - Implementer will add CLI argument parsing (argparse or manual) and invoke operation registry with parsed operands
  - Note: Test suite must remain accurate to "current version of application" — implies tests should reflect actual behavior, not aspirational behavior
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #394: V3 Task 8 - Expert/team
- **Task Type:** Feature enhancement (input validation with retry logic)
- **Scope:** Add input validation with retry logic to interactive mode; maintain fail-fast CLI behavior
- **Key Patterns:**
  - Clear dual-mode specification: retry logic for interactive, fail-fast for CLI
  - No comments or linked issues; all requirements in issue body
  - Explicit scope constraint: "keep the change scoped to input validation behavior"
  - Follows completion of issues #376–#391 (core operations, interactive mode, CLI all established)
  - Task builds on existing interactive mode (`src/interactive.py`) and CLI mode (`src/cli.py`)
- **Key Findings:**
  1. **Task context:** Interactive mode already exists and works; CLI mode already exists and works; this task enhances input validation in interactive mode only
  2. **Retry mechanics:** Invalid operation selection and non-numeric operands trigger re-prompting; max 5 consecutive failed attempts per session
  3. **Session termination:** After 5 failed attempts, session exits with clear message; counter resets to 0 on successful input
  4. **CLI behavior:** No changes to CLI mode; fail-fast behavior remains (exit with error on any validation failure)
  5. **Error categories:** Input validation failures (unknown op, non-numeric operand) count toward limit; computation errors (sqrt negative, div by zero) do NOT count
- **Ambiguities Flagged:**
  1. Counter reset trigger — does it reset only on valid input, or also when user chooses to continue after a computation error? (RESOLVED: reset only on valid input)
  2. Failed attempt definition — does it include computation errors or only validation failures? (RESOLVED: validation failures only; computation errors are not counted)
  3. List format for available operations — what format when user enters invalid operation? (DEFERRED to implementation; use existing format from interactive mode)
  4. Exact error message wording — are message strings prescriptive or suggestive? (DEFERRED; use reasonable, user-friendly messages matching current style)
  5. Early exit mechanism — can user exit before hitting 5-attempt limit? (DEFERRED; maintain current behavior; 5-attempt limit is primary termination trigger)
- **Handoff Notes:**
  - Architect should clarify: (1) whether counter increments for computation errors (NO), (2) whether reset happens on successful input only (YES), (3) acceptable error message format/style
  - Architect must produce test specs covering: valid operations, invalid operations (with re-prompt), non-numeric operands (with re-prompt), counter reset on success, counter increment on failure, session termination at 5 attempts, computation errors not counted
  - Tester will write failing tests for interactive mode validation scenarios and verify CLI mode remains fail-fast
  - Implementer will add validation logic to `src/interactive.py` (operation selection, operand parsing); no changes to `src/cli.py` required
  - Critical: All existing tests must remain passing (no regression)
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #397: V3 Task 9 - Expert/team
- **Task Type:** Feature implementation (session history tracking with file I/O)
- **Scope:** Add operation history to interactive mode; record all operations in function-style format; persist to file on session end; reset on new session start
- **Key Patterns:**
  - Clear, self-contained feature request with explicit format examples
  - No comments or linked issues; all requirements in issue body
  - Explicit scope constraint: "keep the change scoped to local session history"
  - Follows completion of issues #376–#394 (core operations, interactive/CLI modes, input validation all established)
  - Scope is limited to interactive mode only; no CLI history tracking required
- **Key Findings:**
  1. **History format:** Function-style notation with all types of operations: `add(2, 3) = 5`, `power(2, 3) = 8`, `sqrt(9) = 3`, `factorial(5) = 120`
  2. **Display mechanism:** Current session history can be shown on request (command/menu option not specified; implementation discretion)
  3. **Persistence:** History written to `history.txt` when session ends; file is overwritten (not appended) on subsequent sessions
  4. **Session lifecycle:** Each new session starts with empty history; no data carried over from previous sessions
  5. **Success condition:** Only successful operations recorded; computation errors and input validation failures not added to history
- **Ambiguities Flagged:**
  1. History display command name/integration — issue does not specify how user requests history display (dedicated command, menu option, etc.); assume architect will determine based on existing interactive mode patterns
  2. File location — task says "such as history.txt" without specifying exact path; assume project root or cwd, no nested directories
  3. Error handling on file I/O — no spec for behavior if file write fails (permissions, disk full); assume graceful handling (log, inform user, allow session to end)
  4. Numeric precision in output — no spec for float formatting (repr vs str vs custom); assume Python default repr() or str()
  5. Whether computation errors are recorded — not explicitly stated; assume only successful results are recorded
- **Handoff Notes:**
  - Architect should clarify: (1) history display command integration point, (2) file write error handling strategy, (3) result numeric formatting preference
  - Architect must produce test specs covering: recording unary/binary operations, history display functionality, file write on session end, empty history on new session start, graceful error handling for file I/O
  - Tester will write failing tests for all scenarios above; verify both interactive and existing tests remain passing
  - Implementer will integrate history recording into `src/interactive.py` (post-operation hook), add history display command, implement file write on session exit
  - Critical: All existing tests must pass; no unrelated refactoring
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — PR #444 Review: Unresolved Feedback on Issue #397 Implementation
- **Task Type:** PR review feedback analysis (identify unresolved requirements)
- **Scope:** Extract and structure unresolved owner feedback on PR #444 (session history feature implementation)
- **Key Finding (BLOCKER):**
  - **Unresolved Comment by @DanielRiha8906 (Owner):** "Add an option when launching the application to view history of operations via an index."
  - **Status:** Flagged as "Needs fix"; PR state is OPEN with label `request-changes:expert-team`
  - **Current Implementation Gap:** PR implements history recording and file persistence, but **does not provide a user-facing mechanism** to view recorded history during/at session launch
- **Requirement Extracted:**
  - **FR1 (MUST HAVE):** Add user-facing menu option or command in interactive mode to view operation history indexed by entry number
  - **Scope:** History viewing must integrate into interactive session launch/menu flow; exact entry point not specified by owner
  - **Pattern:** Indexed display of operations (e.g., "1. add(2, 3) = 5", "2. sqrt(9) = 3.0", etc.)
  - **Behavior:** User can select or view history entries; gracefully handle empty history
- **Critical Ambiguities Requiring Architect Clarification:**
  1. **Display timing:** At startup (mandatory), on-demand during session, or optional pre-session menu?
  2. **Navigation/selection:** Is index used for full entry viewing, or just enumerated display?
  3. **History scope:** Current-session ops only, or include previous session data from `history.txt`?
  4. **Integration point:** Where in existing interactive menu flow is history option placed?
  5. **Empty history handling:** Exact user message/behavior when no operations recorded yet?
- **Handoff Notes:**
  - Architect MUST clarify the 5 ambiguities above before system design proceeds
  - Test specs must cover: history display with 1/N operations, indexed selection (if applicable), empty history, no-crash behavior, menu integration
  - Tester will write failing tests for history viewing feature (new tests beyond the 21 already in test_history.py)
  - Implementer will modify `src/interactive.py` to add history viewing mechanism; may require minor enhancements to `src/history.py` if display method is insufficient
  - All 241 existing tests must remain green throughout
- **Patterns Observed:**
  - PR comments from owner are concise and actionable but sometimes lack implementation details
  - "Needs fix" label followed by explicit task statement is the blocking signal for PRs in this pipeline
  - Each task/PR builds on prior features; interdependencies are tracked in issue progression
- **Label:** `request-changes:expert-team` (blocking; requires modification before merge)

### Cycle: 2026-04-24 — Issue #400: V3 Task 10 - Expert/team
- **Task Type:** Feature implementation (error logging with file I/O)
- **Scope:** Add error-only logging to both interactive and CLI modes; record errors to dedicated log file; keep separate from operation history
- **Key Patterns:**
  - Clear, self-contained feature request with explicit error categories
  - No comments or linked issues; all requirements in issue body
  - Explicit scope constraint: "keep error logging separate from user-facing operation history, avoid turning logging into a general persistence system"
  - Follows completion of issues #376–#397 (all prior calculator features established)
  - Applies to both interactive mode and CLI mode (dual-mode consistency required)
- **Key Findings:**
  1. **Error categories (4 types):** unsupported operations, invalid operand input, incorrect argument counts (CLI), runtime calculation errors (div by zero, invalid math domains)
  2. **Log destination:** Dedicated local log file (e.g., `error.log`); not merged with `history.txt`
  3. **Mode coverage:** Both interactive and CLI modes must log consistently
  4. **Scope boundary:** Errors only; no general persistence, archival, or analytics features
  5. **Non-functional:** Logging must not interfere with operation, handle I/O failures gracefully, maintain all existing tests green
- **Ambiguities Flagged:**
  1. Log file location — assumed project root or cwd; architect to clarify if configurable or fixed
  2. Log entry format — no specification of timestamp, fields, or verbosity; architect must specify (suggest ISO8601 timestamp + error category + operation + message)
  3. File I/O error handling — no behavior spec if log write fails; architect to specify (warn user, silent skip, crash)
  4. Log file persistence — assumed append across sessions; architect to clarify if overwrite each session
  5. Error message duplication — no spec for interaction with user-facing error messages; assumed independent (both logged and displayed to user)
  6. CLI stderr behavior — no spec if logged errors also written to stderr; assumed yes for CLI mode
- **Handoff Notes:**
  - Architect MUST clarify the 6 ambiguities above; produce design spec with log format, error message content per category, I/O error handling strategy, file location/mode
  - Architect must produce test specs covering 8 categories: invalid ops (interactive + CLI), invalid operands (interactive + CLI), incorrect arg counts (CLI), runtime errors (interactive + CLI), log format/content, history separation, graceful error handling, test suite regression
  - Tester will write failing tests for all 8 categories; all tests must fail before handoff to implementer
  - Implementer will integrate logging subsystem (suggest Python `logging` module) with hook points in `src/interactive.py` and `src/cli.py`; ensure all test-defined error conditions logged; do not modify history-related code unless verification needed
  - Tester (VERIFY phase) will run full suite; confirm 8 test categories pass and all existing tests remain green
  - Critical: No test regressions; logging must be transparent to existing functionality
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-24 — Issue #406: V3 Task 12 - Expert/team (CURRENT)
- **Task Type:** Architectural refactoring (module organization and operations structure design)
- **Scope:** Refactor calculator codebase into multiple well-organized modules; establish clear separation between core logic, interface handling, session-related behavior, and supporting utilities; introduce clean operations structure ready for future normal/scientific mode separation
- **Key Patterns:**
  - No comments or linked issues; all requirements in issue body
  - Explicitly excludes full scientific mode implementation; only the structural boundary should be prepared
  - Task is NOT a feature addition; it is a structural/organizational task
  - Explicit scope constraint: "preserve current behavior of existing features"
  - Prerequisite tasks completed: issues #376–#400 establish all current features (basic ops, factorial, 8 scientific ops, interactive mode, CLI mode, input validation, history tracking, error logging)
  - Design-first task; requires architect approval before implementation proceeds
- **Key Requirements (from issue body):**
  1. **FR1 (MUST HAVE):** Refactor calculator into **multiple modules** with clear separation of concerns
  2. **FR2 (MUST HAVE):** Organize into conceptual areas: **core logic**, **interface handling**, **session-related behavior**, **supporting concerns**
  3. **FR3 (MUST HAVE):** Introduce a **clearer operations structure** for currently implemented features
  4. **FR4 (MUST HAVE):** Design operations structure so **future normal/scientific separation has an obvious place** in module layout
  5. **NFR1:** Preserve 100% current behavior of existing features (no user-visible changes)
  6. **NFR2:** Maintain object-oriented design throughout
  7. **NFR3:** Introduce abstractions only where they clearly support maintainability and extensibility
  8. **NFR4:** Maintain all existing tests; tests must accurately reflect current version
  9. **SC1:** Do NOT implement full scientific mode unless necessary for structural boundaries
- **Discovered Files/Modules (from prior task context):**
  - `src/__main__.py` (application entry point)
  - `src/interactive.py` (interactive session mode)
  - `src/cli.py` (CLI argument parsing and execution)
  - `src/operation_registry.py` (operation registration and lookup)
  - `src/history.py` (session history tracking and persistence)
  - Implicit: core calculator logic, possibly spread across multiple files
- **Ambiguities Flagged:**
  1. **Exact module boundaries:** Which operations/components belong in which modules? What naming convention? (e.g., `src/core/`, `src/interface/`, `src/session/`, `src/utils/` or flat structure?)
  2. **Operations structure specifics:** Should operations be organized as classes (Strategy pattern), a factory/registry, a dispatch table, or something else?
  3. **Normal vs scientific separation point:** Where should the abstraction/separation exist for future scientific mode? (e.g., inherit from base Operation, use operation type tags, separate registries?)
  4. **Backward compatibility of imports:** Should existing imports from refactored modules still work (compatibility layer), or is breaking API acceptable?
  5. **Test file reorganization:** Should tests be refactored to match new module structure, or remain as-is (accepting that test organization might diverge from source)?
  6. **Dependencies between modules:** Are there circular dependency risks or ordering constraints in the new structure?
- **Constraints:**
  - Must not implement scientific mode operations (only structural readiness)
  - Must not break any existing test
  - Must preserve all user-facing behavior (interactive mode, CLI, history, logging, input validation)
  - No changes to CLAUDE.md, .gitignore, or workflow files
- **Acceptance Criteria (inferred):**
  - AC1: Codebase organized into well-named modules with clear purpose
  - AC2: Each module exhibits single responsibility (core, interface, session, supporting)
  - AC3: Operations can be trivially separated into normal/scientific without refactoring module structure
  - AC4: All existing tests pass (no regression)
  - AC5: Code is readable, maintainable, and OOP design is evident
  - AC6: No user-visible behavior change (feature parity maintained)
- **Handoff Notes for Next Agent (Architect):**
  - This task is a DESIGN task; produce architectural plan BEFORE implementation starts
  - Architect must address the 6 ambiguities above in the design document
  - Architect should produce a module dependency diagram showing refactored structure
  - Architect should specify test refactoring strategy (mirror source structure or keep as-is?)
  - Architect should propose operation structure (e.g., base class, registry pattern, etc.) that clearly accommodates future normal/scientific separation
  - Tester will write NO new tests (test suite is stable); only verify refactored code passes all existing tests in VERIFY phase
  - Implementer will refactor according to architect's design; file moves and reorganization is the primary work
  - Critical: This is a large-scope refactoring; must keep commits atomic and reversible
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)
- **Patterns Observed:**
  - Issue #406 is the first structuring/architectural task in the progression (all prior tasks were feature additions)
  - Task represents a significant shift from feature-driven to design-driven work
  - Successor tasks (if any) will likely assume this refactored structure as a foundation

### Cycle: 2026-04-24 — PR #453 Review: Unresolved Feedback on Issue #406 Implementation
- **Task Type:** PR review feedback analysis (identify unresolved requirements)
- **Scope:** Extract and structure unresolved owner feedback on PR #453 (Issue #406 modular refactoring implementation)
- **PR Status:** OPEN with label `request-changes:expert-team` (blocking feedback present)
- **PR Test Results:** 334 tests passed, 0 failed; test suite passes completely
- **PR Implementation Summary:**
  - Introduces `src/core/`, `src/ui/`, `src/infrastructure/`, `src/session/` sub-packages
  - Moves UI logic (`interactive.py`, `cli.py`) to `src/ui/`
  - Moves supporting logic (`history.py`, `error_logger.py`) to `src/infrastructure/`
  - Adds `OperationType` enum and `OperationMetadata` dataclass in `src/core/operations.py`
  - Adds `SessionManager` class in `src/session/manager.py`
  - Implements backward-compatibility re-exports in `src/__init__.py`
  - Preserves old flat files at `src/` root to avoid breaking ~90 existing tests
- **UNRESOLVED BLOCKER (Critical):**
  - **Owner Comment:** "NEEDS FIX" with explicit task list:
    1. `__main__.py` not updated to use new sub-packages
    2. `python -m src` still routes to old `src/cli.py` and `src/interactive.py`
    3. New `src/ui/`, `src/infrastructure/`, `src/session/`, `src/core/` are unreachable via entry point
    4. Update tests to reflect new import paths
  - **Status:** Single unresolved comment; no review comments or review threads marked as resolved
- **Requirements Extracted from Unresolved Feedback:**
  1. **FR1 (MUST HAVE):** Update `src/__main__.py` to import and invoke entry points from the NEW sub-packages (`src.ui.interactive`, `src.ui.cli`) instead of old flat imports
  2. **FR2 (MUST HAVE):** Verify that `python -m src` launches application using NEW sub-package code paths (new interactive and/or CLI implementations)
  3. **FR3 (MUST HAVE):** Update ~90 existing test files to import from new sub-package paths instead of old flat `src/` paths (e.g., `from src.ui.interactive import ...` instead of `from src.interactive import ...`)
  4. **FR4 (SHOULD HAVE):** Consider whether old flat files (`src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py`) should be deleted after test imports updated, or kept for gradual migration
  5. **NFR1:** No test regressions; all 334 passing tests must remain passing after changes
  6. **NFR2:** Verify entry point accessibility: new sub-packages must be reachable and executable via `python -m src`
- **Critical Ambiguities Requiring Architect/Implementer Clarification:**
  1. **Entry point routing:** Should `src/__main__.py` unconditionally launch interactive mode, support both modes via CLI args, or auto-detect based on environment?
  2. **Test import update scope:** Should all ~90 tests be updated at once, or in phases? Which tests are highest priority?
  3. **Old flat file retention:** PR preserves old files for backward compatibility; should they be removed, deprecated with warnings, or kept indefinitely?
  4. **Import path strategy:** Should `src/__init__.py` re-exports remain as primary API, or should new sub-package imports be preferred?
  5. **Backward-compatibility guarantees:** Does the project commit to supporting old flat-file imports indefinitely, or is this a one-time migration window?
- **Owner Expectations Inferred:**
  - Entry point MUST be updated; new packages MUST be reachable; tests MUST reflect new structure
  - Owner sees this as a necessary completion step for the refactoring to be functional
  - Four-part task list suggests implementer should handle all four items (not piecemeal)
- **Handoff Notes:**
  - For system architect: Clarify entry point strategy and test migration plan; produce implementation spec for `src/__main__.py` and test update approach
  - For implementer: Update `src/__main__.py` to route to new sub-package entry points; update all ~90 test imports to use new paths; verify `python -m src` invokes new code; ensure no test regressions
  - For tester: Verify all 334 tests pass after changes; confirm entry point works as expected; test both interactive and CLI modes (if supported)
  - Critical: Four-part task is tightly coupled; all parts must be completed together; partial completion is not acceptable per owner feedback
- **Label:** `request-changes:expert-team` (blocking feedback; requires fixes before merge)
- **Patterns Observed:**
  - PR was generated by Claude Code (autonomous agent); owner (DanielRiha8906) provides corrective feedback
  - Feedback is actionable and specific (task list provided)
  - Test suite passing does not guarantee full task completion (tests still used old imports, so they don't validate new sub-package accessibility)
  - Backward-compatibility re-exports masked the incomplete entry point update (tests passed but entry point was not updated)

### Cycle: 2026-04-24 — Issue #409: V3 Task 13 - Expert/team (Documentation)
- **Task Type:** Documentation creation (user guide and developer guide)
- **Scope:** Add comprehensive written documentation for the calculator application covering user usage, developer maintenance, code structure, and current implementation behavior
- **Key Patterns:**
  - Clear, self-contained documentation task with explicit scope
  - No comments or linked issues; requirements fully expressed in issue body
  - Explicit constraint: "Keep the documentation aligned with the actual implementation rather than idealized or planned future behavior"
  - Follows completion of issues #376–#406 (all calculator features and modular refactoring established)
  - Documentation-only task; no source code changes required
- **Key Requirements (from issue body):**
  1. **FR1 (MUST HAVE):** Document the **available calculator functionality** (operations list with arity and domain constraints)
  2. **FR2 (MUST HAVE):** Document **guided interactive mode** usage (how to run, example session, available commands)
  3. **FR3 (MUST HAVE):** Document **bash-based CLI usage** (syntax, examples for binary/unary operations, exit codes)
  4. **FR4 (MUST HAVE):** Document **local session behavior** such as **history tracking** (file format, display, overwrite behavior)
  5. **FR5 (MUST HAVE):** Document **error logging** (what is logged, file location, format, append behavior)
  6. **FR6 (MUST HAVE):** Document **current code structure after refactoring** (module organization, layer architecture, purpose of each module/file)
  7. **NFR1:** Keep documentation aligned with **actual implementation** (post-refactoring), not idealized future state
  8. **NFR2:** Maintain relevant tests so they accurately reflect current version
- **Deliverables Created:**
  - `README.md` — Comprehensive rewrite with 400+ lines covering:
    - **User Guide** section with subsections: Running the Application, Interactive Mode, CLI Usage, Operations List (with domain validation details), History Tracking, Error Logging
    - **Developer Guide** section with subsections: Code Structure (modular layer architecture diagram), Module Purposes (table of 6 key modules), Entry Point Flow, Running Tests
    - **Repository Overview** — file tree showing project structure
    - **Auto-Evolution Engine** — overview of CLAUDE.md, agent responsibilities, and workflow automation
    - **Local Setup** — quick-start for development
    - **Running Auto-Evolution** — instructions for triggering agent pipeline
  - `tests/test_documentation.py` — 16 new tests validating README content:
    - **Existence tests (2):** README exists and is non-empty
    - **User Guide tests (6):** Has User Guide section, run instructions, interactive mode walkthrough, CLI syntax, operations list, history/error logging mentions
    - **Developer Guide tests (5):** Has Developer Guide section, code structure, module purposes, entry point flow, test execution docs
    - **Operations & domain tests (2):** Operations with arity documented, domain validation/constraints documented
    - **1 aggregate test** (test_readme_has_domain_validation_info)
- **Implementation Details (from PR/progress.md):**
  - `README.md` completely rewritten (not incremental)
  - Tests added to `tests/test_documentation.py` (16 new tests)
  - All 350 tests passing (no regressions)
  - Branch: `task/issue-409-documentation`
  - PR target: `exp3/expert-team`
- **Files Modified in src/:** NONE (documentation-only)
- **Files Added/Modified:**
  - Added: `README.md` (comprehensive user + developer guide)
  - Added: `tests/test_documentation.py` (16 validation tests)
  - Updated: `rag/agents/python-code-implementer.md` and `rag/agents/pytest-edge-tester.md` (cycle entries appended)
- **Key Content from README.md:**
  - **User Guide:** Shows 12 supported operations (5 binary: add/subtract/multiply/divide/power; 7 unary: factorial/square/cube/sqrt/cbrt/ln/log10)
  - **Domain Validation:** Explicitly documents constraints (sqrt: x >= 0, factorial: non-negative int, ln/log10: x > 0, divide: divisor != 0)
  - **Interactive Mode:** Includes example session with menu, operand prompts, result display, history view ("h"), exit ("no"/"n"), 5-attempt limit behavior
  - **CLI Usage:** Shows `python -m src <operation> <operand1> [operand2]` pattern with binary/unary examples; documents exit codes (0 success, 1 error)
  - **History:** Describes `history.txt` format (function-style: `add(10, 5) = 15`), overwrite-on-write behavior, mid-session view capability
  - **Error Logging:** Describes `error.log` (append mode, never overwrites), timestamp format, error type labels, graceful I/O failure handling
  - **Code Structure:** Modular layer architecture (core, ui, infrastructure, session); maps 6 key modules to layers and responsibilities
  - **Entry Point:** Documents `__main__.py` dispatch logic (no args = interactive, args = CLI)
- **Ambiguities Resolved During Implementation:**
  - None flagged; task was straightforward documentation of existing implementation
- **Acceptance Criteria (met):**
  - AC1: All operations documented with arity and domain constraints — YES
  - AC2: Interactive mode walkthrough provided with example — YES
  - AC3: CLI syntax documented with examples — YES
  - AC4: History behavior documented — YES
  - AC5: Error logging documented — YES
  - AC6: Code structure documented — YES
  - AC7: Documentation aligned with actual post-refactoring code — YES
  - AC8: No source code changes; documentation-only — YES
  - AC9: Tests added to validate documentation exists and has required sections — YES (16 tests)
  - AC10: All tests pass; no regressions — YES (350 passed)
- **Handoff Notes:**
  - No architect handoff required; documentation task is self-contained
  - No test-writing phase required; tests validate documentation structure, not feature behavior
  - Documentation is complete and production-ready; no further work needed for this issue
  - Future documentation updates (if any) should maintain the same structure and detail level
- **Label:** `ai-implement:expert-team` (expert team delivery)
- **Patterns Observed:**
  - Documentation task required full understanding of post-refactoring code structure (previous refactoring task #406 was prerequisite)
  - Task successfully completed in single agent cycle (no PR review feedback needed)
  - Tests for documentation are meta-tests (they verify the README has required sections, not that code behaves correctly)
  - README now serves as authoritative user and developer guide; should be updated whenever feature behavior changes

### Cycle: 2026-04-24 — Issue #412: V3 Task 14 - Expert/team
- **Task Type:** Feature implementation (normal/scientific calculator mode selection in interactive mode)
- **Scope:** Add interactive mode support for switching between normal and scientific operation sets during a session
- **Key Patterns:**
  - Clear, self-contained feature request with explicit operation lists for each mode
  - No comments or linked issues; all requirements expressed in issue body
  - Explicit scope constraint: "keep the change scoped to interactive mode switching rather than GUI or bash-based CLI mode selection"
  - Follows completion of issues #376–#409 (all foundation features and refactoring established)
  - Task explicitly defers GUI and CLI mode switching out of scope; focus is interactive-only
  - Task explicitly reuses "existing modular operation structure" so normal/scientific remain cleanly separated
- **Key Requirements (from issue body):**
  1. **FR1 (MUST HAVE):** Add support for **normal and scientific calculator modes** in **interactive mode only**
  2. **FR2 (MUST HAVE):** Allow user to **switch between modes during a session** without restarting application
  3. **FR3 (MUST HAVE):** **Normal mode** operations: standard calculator ops (add, subtract, multiply, divide, square, sqrt)
  4. **FR4 (MUST HAVE):** **Scientific mode** operations: expanded set including normal ops PLUS advanced functions (power, cube, cube root, factorial, log10, ln, sin, cos, tan, cot, asin, acos)
  5. **FR5 (MUST HAVE):** **Interactive flow clearly presents** operations available in currently selected mode
  6. **FR6 (MUST HAVE):** Use **existing modular operation structure** so normal and scientific functionality remain **separated cleanly**
  7. **NFR1:** Scope is **interactive mode switching only** — no changes to GUI or bash-based CLI mode selection
  8. **NFR2:** Maintain relevant tests so they accurately reflect current version of application
- **Current State (Discovered from README + Codebase Map):**
  - **Currently supported operations (12 total):**
    - Binary: add, subtract, multiply, divide, power
    - Unary: factorial, square, cube, sqrt, cbrt, ln, log10
  - **Note:** sin, cos, tan, cot, asin, acos NOT YET IMPLEMENTED — task assumes these will be implemented elsewhere or this task includes their implementation
  - **Current interactive mode:** Shows all 12 operations in a single menu; no mode selection exists yet
  - **Current modular structure:** `src/core/operations.py`, `src/ui/interactive.py`, `src/operation_registry.py`
- **Ambiguities Flagged:**
  1. **Trigonometric operations (sin, cos, tan, cot, asin, acos):** Not in current implementation; task lists them as scientific-mode operations. CLARIFICATION NEEDED: Should this task include implementing these 6 new operations, or assume they exist? (Most likely: architect must determine if trig ops should be added as part of this task or are out of scope)
  2. **Normal mode operations scope:** Issue lists "square" and "sqrt" as normal; current code has both; confirmed. But does "standard calculator operations" include power? (Issue lists power under scientific, but it's currently available; architect must clarify if power should be moved to scientific-only or remain in both modes)
  3. **Mode selection mechanism:** No specification of how user selects/switches modes (dedicated menu option, command, etc.); architect discretion based on interactive mode pattern
  4. **Mode persistence:** Does selected mode persist across multiple operations within a session, or reset after each operation? (ASSUMPTION: persists until user explicitly switches)
  5. **Default mode on startup:** Which mode should interactive session default to — normal or scientific? (ASSUMPTION: normal, as conservative default)
  6. **Trigonometric angle units:** If trig operations are implemented, are they in degrees or radians? (DEFERRED; only relevant if trig ops added in this task)
  7. **CLI and GUI implications:** Task explicitly excludes CLI mode switching. But if user switches to scientific mode in interactive, can they later use those operations via CLI? (ASSUMPTION: CLI remains unchanged; CLI mode does not support mode switching, and only supports operations that exist at CLI entry point)
- **Constraints:**
  - Must use existing modular operation structure (don't break existing registry/core patterns)
  - Scope limited to interactive mode; no CLI or GUI changes
  - All existing tests must pass (no regression)
  - Must maintain clean separation between normal and scientific operation sets
- **Acceptance Criteria (inferred):**
  - AC1: User can select between normal and scientific modes at session start or during session
  - AC2: Only operations belonging to selected mode are shown in the interactive menu
  - AC3: Mode can be switched without exiting the session
  - AC4: Mode selection is clearly presented and intuitive
  - AC5: Normal mode has 6 operations (add, subtract, multiply, divide, square, sqrt)
  - AC6: Scientific mode has normal ops + 8 advanced ops (power, cube, cbrt, factorial, log10, ln, sin, cos, tan, cot, asin, acos)
  - AC7: All existing tests pass; new tests cover mode selection and operation filtering
  - AC8: Code organization reflects clean separation of normal vs scientific operations
- **Handoff Notes for Architect:**
  - **CRITICAL AMBIGUITY 1:** Are trigonometric functions (sin, cos, tan, cot, asin, acos) already implemented in this codebase, or should they be added as part of this task?
  - **CRITICAL AMBIGUITY 2:** Should `power` operation be available in normal mode, scientific mode only, or both? (Currently available in all modes; issue lists under scientific)
  - Architect must clarify mode selection UI (menu option, command string, etc.) and decide if any new operations must be implemented
  - Architect should produce test specs covering: mode selection, operation filtering per mode, mode switching mid-session, normal mode operations (verify correct set), scientific mode operations (verify correct set), edge cases
  - Architect should design data structure for separating normal vs scientific operations (could use operation tags, separate registries, or metadata flags on existing operations)
  - Architect should consider whether to refactor `OperationType` enum or introduce new `OperationCategory` or `OperationMode` enum for this purpose
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)
- **Patterns Observed:**
  - Task builds on completed refactoring (#406); new mode selection feature leverages modular structure
  - Issue provides operation lists but does not specify precise implementation structure (leaves architect flexibility)
  - Trigonometric operations listed but not yet implemented; architect decision needed on scope
- **Files Likely to Be Modified:**
  - `src/operation_registry.py` — to support filtering operations by mode
  - `src/ui/interactive.py` — to add mode selection menu and filter operation display
  - `src/core/operations.py` — possibly to add mode metadata or new operation category enum
  - `tests/` — new tests for mode selection and operation filtering

### Cycle: 2026-04-25 — Issue #415: V3 Task 15 - Expert/team
- **Task Type:** Feature implementation (GUI layer using tkinter)
- **Scope:** Add graphical user interface for calculator using tkinter; preserve existing calculator behavior and application logic; reuse existing operations without duplication
- **Key Patterns:**
  - Clear, self-contained feature request with explicit functional requirements
  - No comments or linked issues; all requirements in issue body
  - Explicit scope constraint: "scope to adding tkinter-based GUI rather than replacing existing interactive or bash-based CLI modes"
  - Follows completion of all prior tasks (#376–#414); builds on fully modularized codebase and comprehensive documentation
  - Task is feature addition (new GUI) not refactoring; focuses on new UI layer
  - Explicitly emphasizes reuse of existing application logic to avoid duplication
- **Key Requirements (from issue body):**
  1. **FR1 (MUST HAVE):** Add **graphical user interface for calculator using tkinter**
  2. **FR2 (MUST HAVE):** **Preserve current calculator behavior** — no changes to existing interactive/CLI modes
  3. **FR3 (MUST HAVE):** **Reuse existing application logic** rather than duplicating in GUI layer
  4. **FR4 (MUST HAVE):** GUI allows user access to **all currently available calculator functionality**
  5. **FR5 (MUST HAVE):** GUI supports **operation selection** (all supported operations)
  6. **FR6 (MUST HAVE):** GUI supports **operand entry** (unary and binary functions)
  7. **FR7 (MUST HAVE):** GUI displays **calculation results**
  8. **FR8 (MUST HAVE):** GUI supports **switching between simple and scientific mode**
  9. **FR9 (MUST HAVE):** GUI allows viewing **session history**
  10. **FR10 (MUST HAVE):** Use **object-oriented mode design** with **shared base abstraction for calculator modes**
  11. **FR11 (MUST HAVE):** **Common structure** handles simple/scientific behavior while keeping operation sets **separate**
  12. **NFR1:** User can **open calculator window** without terminal prompts
  13. **NFR2:** User can **choose between simple and scientific mode** through interface
  14. **NFR3:** User can **perform supported calculations** through interface
  15. **NFR4:** User can **inspect current session history**
  16. **NFR5:** Application is **usable without relying on terminal prompts**
  17. **SC1:** Do NOT modify/replace existing interactive CLI mode
  18. **SC2:** Do NOT modify/replace existing bash-based CLI mode
  19. **SC3:** Keep change scoped to adding GUI; maintain relevant tests (tests must reflect current version)
- **Current State (Discovered from RAG + Prior Task Context):**
  - **Architecture established:** Modular structure (src/core/, src/ui/, src/infrastructure/, src/session/)
  - **Existing UI modes:** Interactive (terminal-based), CLI (bash-based argument parsing)
  - **Operations available (12 total):** add, subtract, multiply, divide, power, factorial, square, cube, sqrt, cbrt, ln, log10
  - **Missing trig operations:** sin, cos, tan, cot, asin, acos (listed in issue #412 but not yet implemented; architect must clarify if available for GUI)
  - **Mode support:** Issue #412 (interactive mode switching) may or may not be completed before this task; architect must check current state
  - **History tracking:** history.py module already implements persistence; GUI can reuse
  - **Error logging:** error_logger.py already implements error tracking; GUI can reuse
  - **Session management:** SessionManager in src/session/manager.py (may or may not be fully utilized by GUI)
- **Ambiguities Flagged:**
  1. **Trigonometric operations availability:** Issue #415 expects "all currently available" operations in GUI. If trig ops from #412 not implemented, should GUI implementation wait or include stub/placeholder? (CLARIFICATION NEEDED: architect must determine which operations are actually available)
  2. **Mode switching implementation:** Issue #412 adds interactive-mode switching; does GUI also need to support mode switching, or is it orthogonal to GUI implementation? (ASSUMPTION: GUI supports mode switching in same way interactive mode does, if mode switching is implemented by then)
  3. **GUI entry point:** How is GUI launched? (a) New entry point in __main__.py with CLI arg flag, (b) separate script/command, (c) choice menu in existing __main__.py, (d) standalone launcher script? (DEFERRED to architect; no specification provided)
  4. **History display format:** Should GUI history display match function-style format from history.txt (e.g., "add(2, 3) = 5"), or can it use tabular/graphical format? (ASSUMPTION: reuse existing history module format; flexible display allowed)
  5. **Session persistence in GUI:** Does GUI session start fresh (like interactive mode), or can user load previous session history via GUI menu? (ASSUMPTION: fresh session per GUI invocation; history viewing shows previous sessions if desired)
  6. **Error handling in GUI:** How are calculator errors (domain errors, invalid operations) displayed? (ASSUMPTION: GUI shows error messages in dedicated error label/dialog instead of stderr)
  7. **Mode persistence in GUI:** When user closes and reopens GUI, does selected mode persist? (ASSUMPTION: mode resets to default (simple) on each new GUI session)
  8. **Unary vs binary operation handling:** How does GUI distinguish unary vs binary ops in input flow? (e.g., prompt for single operand for sqrt, two operands for add) (DEFERRED to architect; UI design pattern not specified)
  9. **OOP mode design specifics:** "Object-oriented mode design with shared base abstraction" — does this mean: (a) base class for Mode with subclasses SimpleMode/ScientificMode, (b) mode metadata in operation registry, (c) factory pattern for mode instantiation, or (d) something else? (DEFERRED to architect; no implementation pattern specified)
  10. **Reuse of existing logic:** Which modules/functions should GUI call directly? (ASSUMPTION: GUI delegates to Calculator class and OperationRegistry; avoids reimplementing operation logic)
  11. **Test strategy for GUI:** Should GUI be tested via unit tests (mocking tkinter), integration tests (launching GUI window), or both? (DEFERRED; test phase will determine approach)
- **Constraints:**
  - Must not modify existing interactive or CLI modes
  - Must reuse existing application logic (Calculator, operations, history, error logging)
  - Must preserve all existing test pass rate (no regression)
  - GUI is NEW UI layer alongside existing UI modes; does not replace them
  - Mode abstraction must support future extension (simple/scientific separation pattern from #412)
  - No changes to CLAUDE.md, .gitignore, or workflow files
- **Acceptance Criteria (inferred):**
  - AC1: GUI launches successfully from configured entry point without terminal prompts
  - AC2: GUI displays all currently available operations in mode-appropriate list
  - AC3: User can select operation and enter operands (single for unary, two for binary) via GUI
  - AC4: User can click "Calculate" button and see result displayed in GUI
  - AC5: GUI displays errors gracefully (e.g., domain errors, invalid operands)
  - AC6: User can switch between simple and scientific modes using GUI controls
  - AC7: Simple mode displays only basic operations; scientific mode displays all operations
  - AC8: User can access session history from GUI (view operations performed, formatted consistently with history.txt)
  - AC9: User can close GUI window and exit application cleanly (no hanging threads, proper cleanup)
  - AC10: All existing tests pass; no regression from adding GUI module
  - AC11: GUI code is organized in modular fashion (e.g., src/ui/gui.py or src/ui/tkinter_app.py) following existing structure
  - AC12: Object-oriented mode abstraction is evident; base class or interface supports both simple/scientific behaviors
  - AC13: Existing application logic (operations, history, logging) is reused, not duplicated in GUI
- **Handoff Notes for Architect:**
  1. **CRITICAL AMBIGUITY 1:** Confirm which operations are "currently available" (12 known + 6 trig from #412?). If trig not yet implemented, clarify scope for GUI task.
  2. **CRITICAL AMBIGUITY 2:** Clarify mode switching design: does GUI leverage interactive mode switching from #412, or implement independently?
  3. **CRITICAL AMBIGUITY 3:** Design object-oriented mode abstraction: propose base class structure (e.g., `class Mode(ABC)` with `get_operations()` method, or operation registry filtering approach).
  4. **CRITICAL AMBIGUITY 4:** Specify GUI entry point mechanism: CLI arg, separate script, menu choice, or standalone launcher.
  5. Architect should produce test specs covering: GUI window launch, operation selection, operand entry (unary/binary), result display, error display, mode switching, history viewing, window close/cleanup, mode persistence behavior, code organization.
  6. Architect should produce UI/UX design sketch or pseudocode showing tkinter widget layout (e.g., operation buttons, operand entry fields, result label, mode selector, history viewer).
  7. Architect should clarify reuse strategy: which existing classes/functions should GUI import and delegate to (Calculator, OperationRegistry, OperationHistory, ErrorLogger, SessionManager).
  8. Architect should specify file organization: where GUI code lives (src/ui/gui.py vs src/ui/tkinter_app.py vs src/ui/gui_app.py), and whether mode abstraction lives in src/core/ or src/ui/.
- **Patterns Observed:**
  - Task builds on fully completed prior work (#376–#414); inherits modular structure and comprehensive documentation
  - Task involves new UI layer (GUI) alongside existing UI modes (interactive, CLI); architectural pattern is additive, not replacements
  - Mode switching design (from #412) is prerequisite or parallel concern; GUI must align with mode abstraction strategy
  - Strong emphasis on reuse over duplication suggests architect should design clear API boundaries between GUI and core logic
- **Files Likely to Be Modified/Created:**
  - **Create:** `src/ui/gui.py` or `src/ui/tkinter_app.py` (main GUI implementation)
  - **Create or modify:** Mode abstraction (possibly `src/core/mode_base.py` or enhancements to `src/core/operations.py`)
  - **Modify:** `src/__main__.py` (to add GUI entry point or launcher choice)
  - **Possibly modify:** `src/ui/interactive.py` (if mode abstraction is shared with interactive mode)
  - **Tests:** `tests/test_gui.py` or similar (new GUI test module)
  - **May reference (no modification):** `src/calculator.py`, `src/operation_registry.py`, `src/infrastructure/history.py`, `src/infrastructure/error_logger.py`
- **Label:** `ai-implement:expert-team` (orchestrated expert team delivery)

### Cycle: 2026-04-25 — PR #462 Review: Unresolved Feedback on Issue #415 Implementation
- **Task Type:** PR review feedback analysis (identify unresolved requirements from owner comment)
- **Scope:** Extract and structure unresolved owner feedback on PR #462 (Issue #415 tkinter GUI implementation)
- **PR Status:** OPEN (likely with `request-changes` label based on owner feedback)
- **PR Implementation Summary (from PR body):**
  - **`src/ui/modes.py`** — New `CalculatorMode` abstract base class with `SimpleMode` (6 ops: add, subtract, multiply, divide, square, sqrt) and `ScientificMode` (all 12 legacy ops) subclasses; clean OO mode abstraction as required
  - **`src/ui/gui.py`** — New `CalculatorApp` tkinter GUI that reuses `Calculator`, `OperationRegistry`, and `OperationHistory` without modification; supports mode switching, dynamic unary/binary operand fields, error display in GUI label, and scrollable session history; fully injectable (`root`, `calculator`, `registry` params) for testability
  - **`src/__main__.py`** — Added `--gui` flag: `python -m src --gui` launches GUI; existing CLI and interactive paths unchanged
  - **`tests/test_gui.py`** — 30 new tests covering modes, calculations, error handling, history tracking, and operation classification (all headless via mocked tkinter root)
  - **`tests/test_core_separation.py`** — Fixed pre-existing test isolation bug in `test_circular_imports`: `sys.modules` was cleared but never restored, causing 5 GUI tests to fail when the full suite ran together
- **UNRESOLVED BLOCKER (Critical):**
  - **Owner Comment (2026-04-25 15:42:36Z):** "**Fix needed**" with explicit task list:
    1. **"When changing modes from Normal to Scientific, nothing changes."** — Mode switching in GUI does not update displayed operations
    2. **"When Selecting the Scientific modes, the operations are not updated."** — Scientific mode operations list not reflected in UI controls
    3. **"Add the Scientific operations when scientific mode is selected, add the functionality to them."** — Scientific mode must display/enable additional operations (power, cube, cbrt, factorial, log10, ln) not shown in simple mode
    4. **"Every functionality from CLI should be incorporated into the GUI"** — GUI must support ALL operations available via CLI (or via operation registry); no feature gaps between CLI and GUI
  - **Status:** Single unresolved comment; no code-level review comments or review threads; comment is owner's functional test result (mode switching broken, operations not filtering)
- **Requirements Extracted from Unresolved Feedback:**
  1. **FR1 (MUST HAVE):** Implement **dynamic operation filtering** in GUI when user switches modes
     - When user selects simple mode: display only 6 basic operations (add, subtract, multiply, divide, square, sqrt)
     - When user selects scientific mode: display all 12 operations (simple 6 + power, cube, cbrt, factorial, log10, ln)
     - Current state: mode switching does not update operation controls
  2. **FR2 (MUST HAVE):** Ensure **mode switch persists across operand re-entry and result display**
     - User switches from simple to scientific → operation list updates → user can select scientific operation → calculate → result shown → mode remains scientific
     - Current state: mode switching appears to have no effect on available operations
  3. **FR3 (MUST HAVE):** Ensure **GUI operation set matches or exceeds CLI operation set**
     - CLI supports: add, subtract, multiply, divide, power, factorial, square, cube, sqrt, cbrt, ln, log10 (12 ops)
     - GUI simple mode must support: add, subtract, multiply, divide, square, sqrt (6 ops)
     - GUI scientific mode must support: all 12 CLI ops (6 simple + 6 scientific)
     - Verify no operations are missing or inaccessible in GUI vs CLI
  4. **FR4 (MUST HAVE):** Verify **operation functionality matches CLI behavior**
     - Each operation in GUI (simple or scientific) must produce the same result and error behavior as CLI
     - Domain errors, input validation, and result precision must match CLI
     - Current state: unclear if this is a separate issue or related to mode switching bug
  5. **NFR1:** Mode switching must be **responsive** (instant UI update, no lag, no need to restart GUI)
  6. **NFR2:** **Error message clarity** — if scientific operation selected in simple mode (by mistake), error message should guide user to scientific mode
  7. **NFR3:** All **445 tests must pass** after fixes (PR summary claims 445 passing; no regressions allowed)
- **Critical Ambiguities / Clarifications Needed:**
  1. **Mode persistence mechanism:** When user switches mode, is it persisted in an instance variable in `CalculatorMode`-based object, and is the GUI observing/listening to mode changes? (Current code may have mode object but GUI controls not bound to re-render on mode change)
  2. **Operation list update trigger:** What should trigger operation list update in GUI? (a) mode selection radio button click, (b) dropdown selection, (c) menu choice? Which UI element is responsible for triggering the filter?
  3. **Default mode on GUI launch:** Should GUI start in simple mode (conservative) or scientific mode (feature-complete)? (Owner comment implies simple mode is the "default" based on wording "changing modes from Normal to Scientific")
  4. **Operation display implementation:** Are operations shown as: (a) buttons that gray out when not available, (b) dynamic list that is cleared/repopulated, (c) tabs, (d) dropdown menu? If (a), buttons must be re-enabled/disabled on mode change; if (b)/(c)/(d), UI must re-render.
  5. **Operand field adaptation:** When user switches modes, do operand entry fields adapt for unary vs binary ops? (PR summary mentions "dynamic unary/binary operand fields" but unclear if mode switching triggers re-layout)
  6. **Scientific operations behavior:** Are the 6 additional scientific operations (power, cube, cbrt, factorial, log10, ln) already fully implemented and tested in CLI/core modules, or are they new stubs needing implementation? (Assumed: already implemented; issue #382 added these ops; GUI just needs to filter them)
- **Owner Expectations Inferred:**
  - Mode switching MUST work visually; owner tested manually and found it non-functional
  - All 12 operations must be accessible in scientific mode within the GUI
  - Owner expects feature parity: if operation works in CLI, it must work in GUI
  - Four-point task list suggests multiple interconnected issues, not a single root cause
- **Handoff Notes:**
  - For system architect: Clarify mode persistence and operation filtering mechanism; specify which UI elements (buttons, dropdowns, tabs) trigger and reflect mode changes
  - For implementer: Debug mode switching code path in `src/ui/gui.py`; ensure operation controls (buttons/dropdown/tabs) are programmatically updated when `CalculatorMode` object switches modes; verify all 12 operations accessible in scientific mode; test mode switching end-to-end
  - For tester: Write new tests specifically for mode switching behavior (dynamic operation list update, persist across operations, match CLI operation set); verify all 445 tests pass after fixes
  - For debugging: Root cause likely is: (a) mode object changes internally but GUI controls not re-rendered, (b) operation filtering logic not hooked to mode UI element, or (c) operation list not repopulated on mode switch
  - Critical: This is blocking the PR merge; all 4 functional issues must be resolved before acceptance
- **Label:** `request-changes:expert-team` (blocking feedback; functional regression on mode switching)
- **Patterns Observed:**
  - Owner tested PR manually and found functional failure (mode switching broken)
  - PR passes automated test suite (30 tests + 445 total) but fails owner's manual functional test
  - Suggests test suite may not adequately cover mode switching UI behavior (tests may be mocking/headless without verifying actual UI control updates)
  - Strong indication that GUI code has logic for modes but UI binding/reactivity is incomplete
