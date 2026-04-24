# Codebase Map

Per-file summaries of `src/`. Update after any cycle that modifies a listed file.

## src/calculator.py
- **Last updated:** 2026-04-24 (cycle: Issue #375)
- **Purpose:** Core calculator class implementing four arithmetic operations
- **Public interface:** `Calculator.add(a, b)`, `Calculator.subtract(a, b)`, `Calculator.multiply(a, b)`, `Calculator.divide(a, b)` — all accept int or float operands; `divide` raises `ZeroDivisionError` when b=0
- **Known constraints:** No input type validation; relies on Python's native arithmetic

## src/__main__.py
- **Last updated:** 2026-04-24 (cycle: Issue #396)
- **Purpose:** Calculator entry point supporting both CLI mode and interactive REPL mode
- **Public interface:** `cli_mode()` (argv-aware dispatch), `main()` (interactive REPL only), `_build_registry(calculator)`, `_parse_cli_arguments(registry)`, `_execute_cli_mode(operation, operands, registry)`, `_run_interactive_loop(registry, history_file_path=None)`, `_parse_number(raw)`
- **CLI syntax:** `python -m src <operation> <operand1> [<operand2>]` — prints result to stdout, exits 0; errors go to stderr with exit 1
- **Interactive mode:** REPL with consecutive-failure tracking and operation history; exits with "Too many invalid attempts. Exiting." after 3 consecutive failures; counter resets on successful operation; "history" command displays current session history
- **Known constraints:** `if __name__ == "__main__"` calls `cli_mode()`; CLI mode has no retry logic (fail-fast); interactive mode never crashes on invalid input

## src/history.py
- **Last updated:** 2026-04-24 (cycle: Issue #396)
- **Purpose:** Encapsulates operation history tracking — in-memory storage, file persistence, and session isolation
- **Public interface:** `OperationHistory(file_path=None)`, `.record(operation, operands, result)`, `.get_all() -> list[str]`, `.display() -> str`, `.clear()`
- **Session isolation:** constructor clears/creates the history file on each instantiation; previous session data is never loaded
- **Known constraints:** file I/O errors are logged and swallowed (never crash the caller); history file defaults to "history.txt" in cwd

## tests/test_cli_mode.py
- **Last updated:** 2026-04-24 (cycle: Issue #390)
- **Purpose:** 22-test suite covering CLI mode argument parsing, execution, error handling, and interactive fallback
- **Test classes:** `TestCLIBasicOperations` (9), `TestCLIFloatsAndNegatives` (2), `TestCLIErrorHandling` (8), `TestInteractiveModeBackwardCompatibility` (3)
- **Coverage:** all 12 operations via CLI, float/negative operands, missing/invalid args, domain errors, interactive fallback

## tests/test_calculator.py
- **Last updated:** 2026-04-24 (cycle: Issue #375)
- **Purpose:** Full unit test suite for Calculator class covering all four operations
- **Test classes:** `TestCalculatorAdd` (6 tests), `TestCalculatorSubtract` (6 tests), `TestCalculatorMultiply` (6 tests), `TestCalculatorDivide` (5 tests)
- **Coverage:** positive/negative integers, floats, zero, mixed signs, identity operations, ZeroDivisionError

## tests/test_interactive_validation.py
- **Last updated:** 2026-04-24 (cycle: Issue #393)
- **Purpose:** 14-test suite covering interactive mode input validation with consecutive-failure tracking
- **Test groups:** Group A (6 tests): consecutive failure counting/exit; Group B (5 tests): backward compatibility; Group C (2 tests): CLI regression; Group D (1 test): edge cases
- **Coverage:** three consecutive failures → exit; counter reset on success; invalid op/operand/domain errors; quit before limit; CLI mode unchanged

## tests/test_history.py
- **Last updated:** 2026-04-24 (cycle: Issue #396)
- **Purpose:** 23-test suite covering operation history recording, display, file persistence, and session isolation
- **Test groups:** Group A (8 tests): recording basics (success + failure cases); Group B (4 tests): display command; Group C (4 tests): file persistence/session isolation; Group D (2 tests): failure counter integration; Group E (5 tests): edge cases
- **Coverage:** record on success, no-record on failure, history display, empty/populated display, session isolation, injectable file path, case-insensitive "history" command
