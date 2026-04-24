# Codebase Map

Per-file summaries of `src/`. Update after any cycle that modifies a listed file.

## src/calculator.py
- **Last updated:** 2026-04-24 (cycle: Issue #375)
- **Purpose:** Core calculator class implementing four arithmetic operations
- **Public interface:** `Calculator.add(a, b)`, `Calculator.subtract(a, b)`, `Calculator.multiply(a, b)`, `Calculator.divide(a, b)` — all accept int or float operands; `divide` raises `ZeroDivisionError` when b=0
- **Known constraints:** No input type validation; relies on Python's native arithmetic

## src/__main__.py
- **Last updated:** — (not yet populated)
- **Purpose:** —
- **Notes:** —

## tests/test_calculator.py
- **Last updated:** 2026-04-24 (cycle: Issue #375)
- **Purpose:** Full unit test suite for Calculator class covering all four operations
- **Test classes:** `TestCalculatorAdd` (6 tests), `TestCalculatorSubtract` (6 tests), `TestCalculatorMultiply` (6 tests), `TestCalculatorDivide` (5 tests)
- **Coverage:** positive/negative integers, floats, zero, mixed signs, identity operations, ZeroDivisionError
