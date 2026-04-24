# Codebase Map

Per-file summaries of `src/`. Update after any cycle that modifies a listed file.

## src/calculator.py
- **Last updated:** 2026-04-24 (cycle: Issue #375)
- **Purpose:** Core calculator class implementing four arithmetic operations
- **Public interface:** `Calculator.add(a, b)`, `Calculator.subtract(a, b)`, `Calculator.multiply(a, b)`, `Calculator.divide(a, b)` — all accept int or float operands; `divide` raises `ZeroDivisionError` when b=0
- **Known constraints:** No input type validation; relies on Python's native arithmetic

## src/__main__.py
- **Last updated:** 2026-04-24 (cycle: Issue #390)
- **Purpose:** Calculator entry point supporting both CLI mode and interactive REPL mode
- **Public interface:** `cli_mode()` (argv-aware dispatch), `main()` (interactive REPL only), `_build_registry(calculator)`, `_parse_cli_arguments(registry)`, `_execute_cli_mode(operation, operands, registry)`, `_run_interactive_loop(registry)`, `_parse_number(raw)`
- **CLI syntax:** `python -m src <operation> <operand1> [<operand2>]` — prints result to stdout, exits 0; errors go to stderr with exit 1
- **Interactive mode:** unchanged REPL loop invoked when no CLI args are present
- **Known constraints:** `if __name__ == "__main__"` calls `cli_mode()`; existing tests that call `main()` directly still work unchanged

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
