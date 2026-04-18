"""Tests for src/validation.py.

Unit tests for the pure validation functions that validate operations and operands.
These tests exercise both the happy path and edge cases without side effects.
"""

from __future__ import annotations

import pytest

from src.validation import validate_operation, validate_operand, VALID_OPERATIONS
from src.mode import Mode


# ---------------------------------------------------------------------------
# validate_operation
# ---------------------------------------------------------------------------


class TestValidateOperation:
    """Tests for validate_operation()."""

    @pytest.mark.parametrize("operation", list(VALID_OPERATIONS))
    def test_each_valid_operation_returns_true(self, operation: str) -> None:
        """Every operation in VALID_OPERATIONS must return (True, '')."""
        valid, error_msg = validate_operation(operation)
        assert valid is True
        assert error_msg == ""

    def test_unknown_operation_returns_false_with_error(self) -> None:
        """An unrecognised operation must return (False, error_message)."""
        valid, error_msg = validate_operation("nonsense")
        assert valid is False
        assert error_msg != ""
        assert "Invalid operation" in error_msg

    def test_unknown_operation_error_includes_valid_list(self) -> None:
        """The error message must list some of the valid operations."""
        valid, error_msg = validate_operation("bogus")
        assert valid is False
        # At least one valid operation key should appear in the error
        assert any(op in error_msg for op in VALID_OPERATIONS)

    def test_empty_string_returns_false(self) -> None:
        """Empty string is not a valid operation."""
        valid, error_msg = validate_operation("")
        assert valid is False
        assert error_msg != ""

    def test_whitespace_only_returns_false(self) -> None:
        """Whitespace-only string is not a valid operation."""
        valid, error_msg = validate_operation("   ")
        assert valid is False
        assert error_msg != ""

    def test_numeric_string_returns_false(self) -> None:
        """A numeric string is not a valid operation."""
        valid, error_msg = validate_operation("123")
        assert valid is False
        assert error_msg != ""

    def test_special_characters_returns_false(self) -> None:
        """Special characters in operation name returns false."""
        valid, error_msg = validate_operation("add@#$")
        assert valid is False
        assert error_msg != ""

    def test_none_like_string_returns_false(self) -> None:
        """The string 'None' is not a valid operation."""
        valid, error_msg = validate_operation("None")
        assert valid is False
        assert error_msg != ""

    def test_partial_operation_name_returns_false(self) -> None:
        """A partial operation name does not match."""
        valid, error_msg = validate_operation("add_partial")
        assert valid is False
        assert error_msg != ""

    def test_operation_with_extra_whitespace_returns_false(self) -> None:
        """Valid operation with surrounding spaces is not auto-stripped here."""
        valid, error_msg = validate_operation("  add  ")
        assert valid is False
        assert error_msg != ""

    def test_case_sensitive(self) -> None:
        """Operation names are case-sensitive in validation (stripped before calling validate_operation)."""
        # Note: in the actual input_loop.py, input is lowercased before validate_operation is called.
        # This test confirms validate_operation itself is case-sensitive.
        valid, error_msg = validate_operation("ADD")
        assert valid is False

    def test_very_long_operation_name_returns_false(self) -> None:
        """A very long string is not a valid operation."""
        valid, error_msg = validate_operation("a" * 1000)
        assert valid is False


# ---------------------------------------------------------------------------
# validate_operand
# ---------------------------------------------------------------------------


class TestValidateOperand:
    """Tests for validate_operand()."""

    def test_integer_string_returns_true(self) -> None:
        """Integer string like '5' must parse to float 5.0."""
        valid, value, error_msg = validate_operand("5")
        assert valid is True
        assert value == 5.0
        assert isinstance(value, float)
        assert error_msg == ""

    def test_float_string_returns_true(self) -> None:
        """Float string like '3.14' must parse correctly."""
        valid, value, error_msg = validate_operand("3.14")
        assert valid is True
        assert value == pytest.approx(3.14)
        assert error_msg == ""

    def test_negative_integer_returns_true(self) -> None:
        """Negative integer string must parse correctly."""
        valid, value, error_msg = validate_operand("-42")
        assert valid is True
        assert value == -42.0
        assert error_msg == ""

    def test_negative_float_returns_true(self) -> None:
        """Negative float string must parse correctly."""
        valid, value, error_msg = validate_operand("-3.14")
        assert valid is True
        assert value == pytest.approx(-3.14)
        assert error_msg == ""

    def test_zero_returns_true(self) -> None:
        """String '0' must parse to 0.0."""
        valid, value, error_msg = validate_operand("0")
        assert valid is True
        assert value == 0.0
        assert error_msg == ""

    def test_zero_float_returns_true(self) -> None:
        """String '0.0' must parse to 0.0."""
        valid, value, error_msg = validate_operand("0.0")
        assert valid is True
        assert value == 0.0
        assert error_msg == ""

    def test_scientific_notation_returns_true(self) -> None:
        """Scientific notation like '1e10' must parse correctly."""
        valid, value, error_msg = validate_operand("1e10")
        assert valid is True
        assert value == 1e10
        assert error_msg == ""

    def test_scientific_notation_negative_exponent_returns_true(self) -> None:
        """Scientific notation with negative exponent like '1e-5' must parse correctly."""
        valid, value, error_msg = validate_operand("1e-5")
        assert valid is True
        assert value == pytest.approx(1e-5)
        assert error_msg == ""

    def test_very_large_number_returns_true(self) -> None:
        """Very large number like '1e308' must parse."""
        valid, value, error_msg = validate_operand("1e308")
        assert valid is True
        assert value == 1e308
        assert error_msg == ""

    def test_very_small_number_returns_true(self) -> None:
        """Very small number like '1e-308' must parse."""
        valid, value, error_msg = validate_operand("1e-308")
        assert valid is True
        assert value == pytest.approx(1e-308)
        assert error_msg == ""

    def test_leading_whitespace_stripped(self) -> None:
        """String with leading whitespace like '  42  ' must parse after stripping."""
        valid, value, error_msg = validate_operand("  42  ")
        assert valid is True
        assert value == 42.0
        assert error_msg == ""

    def test_plus_sign_prefix_returns_true(self) -> None:
        """String with explicit plus sign like '+5' must parse."""
        valid, value, error_msg = validate_operand("+5")
        assert valid is True
        assert value == 5.0
        assert error_msg == ""

    def test_plus_negative_returns_false(self) -> None:
        """String like '+-5' is invalid."""
        valid, value, error_msg = validate_operand("+-5")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_empty_string_returns_false(self) -> None:
        """Empty string is not numeric."""
        valid, value, error_msg = validate_operand("")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""
        assert "numeric" in error_msg

    def test_whitespace_only_returns_false(self) -> None:
        """Whitespace-only string is not numeric."""
        valid, value, error_msg = validate_operand("   ")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_alphabetic_string_returns_false(self) -> None:
        """Alphabetic string like 'abc' is not numeric."""
        valid, value, error_msg = validate_operand("abc")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_none_like_string_returns_false(self) -> None:
        """String 'None' is not numeric."""
        valid, value, error_msg = validate_operand("None")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_mixed_alphanumeric_returns_false(self) -> None:
        """String like '123abc' is not numeric."""
        valid, value, error_msg = validate_operand("123abc")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_special_characters_returns_false(self) -> None:
        """String with special chars like '5@#$' is not numeric."""
        valid, value, error_msg = validate_operand("5@#$")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_multiple_dots_returns_false(self) -> None:
        """String with multiple decimal points like '3.14.159' is invalid."""
        valid, value, error_msg = validate_operand("3.14.159")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_multiple_signs_returns_false(self) -> None:
        """String with multiple signs like '--5' is invalid."""
        valid, value, error_msg = validate_operand("--5")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_inf_string_returns_true(self) -> None:
        """String 'inf' can be parsed as float('inf')."""
        valid, value, error_msg = validate_operand("inf")
        assert valid is True
        assert value == float('inf')
        assert error_msg == ""

    def test_nan_string_returns_true(self) -> None:
        """String 'nan' can be parsed as float('nan')."""
        valid, value, error_msg = validate_operand("nan")
        assert valid is True
        assert value != value  # NaN != NaN
        assert error_msg == ""

    def test_dot_only_returns_false(self) -> None:
        """String '.' is not a valid number."""
        valid, value, error_msg = validate_operand(".")
        assert valid is False
        assert value == 0.0
        assert error_msg != ""

    def test_decimal_with_no_integer_part_returns_true(self) -> None:
        """String '.5' is valid (parses as 0.5)."""
        valid, value, error_msg = validate_operand(".5")
        assert valid is True
        assert value == 0.5
        assert error_msg == ""

    def test_decimal_with_no_fractional_part_returns_true(self) -> None:
        """String '5.' is valid (parses as 5.0)."""
        valid, value, error_msg = validate_operand("5.")
        assert valid is True
        assert value == 5.0
        assert error_msg == ""

    def test_error_message_contains_helpful_text(self) -> None:
        """Error messages must be user-friendly."""
        valid, value, error_msg = validate_operand("xyz")
        assert valid is False
        assert "numeric" in error_msg or "number" in error_msg


# ---------------------------------------------------------------------------
# validate_operation with mode parameter
# ---------------------------------------------------------------------------


class TestValidateOperationWithMode:
    """Tests for validate_operation() with the mode parameter."""

    def test_no_mode_accepts_add(self) -> None:
        """validate_operation('add', mode=None) must return (True, '')."""
        valid, error_msg = validate_operation("add", mode=None)
        assert valid is True
        assert error_msg == ""

    def test_no_mode_accepts_all_valid_operations(self) -> None:
        """validate_operation with mode=None must accept all VALID_OPERATIONS."""
        for op in VALID_OPERATIONS:
            valid, error_msg = validate_operation(op, mode=None)
            assert valid is True, f"Operation '{op}' should be valid with mode=None"
            assert error_msg == ""

    def test_no_mode_accepts_history(self) -> None:
        """validate_operation('history', mode=None) must return (True, '')."""
        valid, error_msg = validate_operation("history", mode=None)
        assert valid is True
        assert error_msg == ""

    def test_no_mode_rejects_unknown_operation(self) -> None:
        """validate_operation('bogus', mode=None) must return (False, error_msg)."""
        valid, error_msg = validate_operation("bogus", mode=None)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_accepts_add(self) -> None:
        """validate_operation('add', mode=NORMAL) must return (True, '')."""
        valid, error_msg = validate_operation("add", mode=Mode.NORMAL)
        assert valid is True
        assert error_msg == ""

    def test_normal_mode_accepts_subtract(self) -> None:
        """validate_operation('subtract', mode=NORMAL) must return (True, '')."""
        valid, error_msg = validate_operation("subtract", mode=Mode.NORMAL)
        assert valid is True
        assert error_msg == ""

    def test_normal_mode_accepts_multiply(self) -> None:
        """validate_operation('multiply', mode=NORMAL) must return (True, '')."""
        valid, error_msg = validate_operation("multiply", mode=Mode.NORMAL)
        assert valid is True
        assert error_msg == ""

    def test_normal_mode_accepts_divide(self) -> None:
        """validate_operation('divide', mode=NORMAL) must return (True, '')."""
        valid, error_msg = validate_operation("divide", mode=Mode.NORMAL)
        assert valid is True
        assert error_msg == ""

    def test_normal_mode_rejects_power(self) -> None:
        """validate_operation('power', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("power", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_factorial(self) -> None:
        """validate_operation('factorial', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("factorial", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_square(self) -> None:
        """validate_operation('square', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("square", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_log(self) -> None:
        """validate_operation('log', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("log", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_ln(self) -> None:
        """validate_operation('ln', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("ln", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_square_root(self) -> None:
        """validate_operation('square_root', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("square_root", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_cube_root(self) -> None:
        """validate_operation('cube_root', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("cube_root", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_rejects_cube(self) -> None:
        """validate_operation('cube', mode=NORMAL) must return (False, error_msg)."""
        valid, error_msg = validate_operation("cube", mode=Mode.NORMAL)
        assert valid is False
        assert error_msg != ""

    def test_scientific_mode_accepts_add(self) -> None:
        """validate_operation('add', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("add", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_power(self) -> None:
        """validate_operation('power', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("power", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_factorial(self) -> None:
        """validate_operation('factorial', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("factorial", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_square(self) -> None:
        """validate_operation('square', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("square", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_cube(self) -> None:
        """validate_operation('cube', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("cube", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_square_root(self) -> None:
        """validate_operation('square_root', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("square_root", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_cube_root(self) -> None:
        """validate_operation('cube_root', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("cube_root", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_log(self) -> None:
        """validate_operation('log', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("log", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_accepts_ln(self) -> None:
        """validate_operation('ln', mode=SCIENTIFIC) must return (True, '')."""
        valid, error_msg = validate_operation("ln", mode=Mode.SCIENTIFIC)
        assert valid is True
        assert error_msg == ""

    def test_scientific_mode_rejects_unknown_operation(self) -> None:
        """validate_operation('bogus', mode=SCIENTIFIC) must return (False, error_msg)."""
        valid, error_msg = validate_operation("bogus", mode=Mode.SCIENTIFIC)
        assert valid is False
        assert error_msg != ""

    def test_normal_mode_error_message_lists_valid_operations(self) -> None:
        """Normal mode error message must list the 4 valid operations."""
        valid, error_msg = validate_operation("power", mode=Mode.NORMAL)
        assert valid is False
        # Error should mention valid operations
        assert "add" in error_msg or "Valid operations" in error_msg

    def test_scientific_mode_error_message_lists_valid_operations(self) -> None:
        """Scientific mode error message must list valid operations."""
        valid, error_msg = validate_operation("bogus", mode=Mode.SCIENTIFIC)
        assert valid is False
        # Error should mention at least some valid operations
        assert any(op in error_msg for op in ["add", "power", "factorial"])

    def test_mode_none_backward_compatibility(self) -> None:
        """validate_operation with mode=None must match pre-mode behavior."""
        # All VALID_OPERATIONS should be accepted
        for op in VALID_OPERATIONS:
            valid, _ = validate_operation(op, mode=None)
            assert valid is True

    def test_normal_mode_only_four_operations(self) -> None:
        """NORMAL mode should accept exactly 4 operations."""
        from src.mode import get_normal_operations
        normal_ops = get_normal_operations()

        accepted_count = 0
        for op in ["add", "subtract", "multiply", "divide", "power", "factorial",
                  "square", "cube", "square_root", "cube_root", "log", "ln"]:
            valid, _ = validate_operation(op, mode=Mode.NORMAL)
            if valid:
                accepted_count += 1

        assert accepted_count == 4, f"NORMAL mode should accept 4 ops, accepted {accepted_count}"

    def test_scientific_mode_twelve_operations(self) -> None:
        """SCIENTIFIC mode should accept exactly 12 operations."""
        from src.mode import get_scientific_operations

        ops_to_test = [
            "add", "subtract", "multiply", "divide",
            "power", "factorial", "square", "cube",
            "square_root", "cube_root", "log", "ln"
        ]

        accepted_count = 0
        for op in ops_to_test:
            valid, _ = validate_operation(op, mode=Mode.SCIENTIFIC)
            if valid:
                accepted_count += 1

        assert accepted_count == 12, f"SCIENTIFIC mode should accept 12 ops, accepted {accepted_count}"
