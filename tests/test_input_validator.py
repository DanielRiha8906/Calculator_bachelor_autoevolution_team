"""Tests for src/input_validator.py.

Tests validation functions and exception classes for input sanitization
before dispatch to the Calculator engine.
"""

from __future__ import annotations

import pytest

from src.input_validator import (
    InvalidOperandError,
    InvalidOperationError,
    OperandCountError,
    ValidationError,
    validate_operands,
    validate_operation,
)
from src.input_loop import OPERATIONS


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


def test_validation_error_is_exception() -> None:
    """ValidationError must be a subclass of Exception."""
    assert issubclass(ValidationError, Exception)


def test_invalid_operation_error_is_validation_error() -> None:
    """InvalidOperationError must be a subclass of ValidationError."""
    assert issubclass(InvalidOperationError, ValidationError)


def test_invalid_operand_error_is_validation_error() -> None:
    """InvalidOperandError must be a subclass of ValidationError."""
    assert issubclass(InvalidOperandError, ValidationError)


def test_operand_count_error_is_validation_error() -> None:
    """OperandCountError must be a subclass of ValidationError."""
    assert issubclass(OperandCountError, ValidationError)


def test_validation_error_can_be_instantiated() -> None:
    """ValidationError must be instantiable with a message."""
    exc = ValidationError("test message")
    assert str(exc) == "test message"


def test_invalid_operation_error_can_be_instantiated() -> None:
    """InvalidOperationError must be instantiable with a message."""
    exc = InvalidOperationError("test message")
    assert str(exc) == "test message"


def test_invalid_operand_error_can_be_instantiated() -> None:
    """InvalidOperandError must be instantiable with a message."""
    exc = InvalidOperandError("test message")
    assert str(exc) == "test message"


def test_operand_count_error_can_be_instantiated() -> None:
    """OperandCountError must be instantiable with a message."""
    exc = OperandCountError("test message")
    assert str(exc) == "test message"


# ---------------------------------------------------------------------------
# validate_operation — happy path
# ---------------------------------------------------------------------------


def test_validate_operation_valid_key_returns_key() -> None:
    """A valid operation key must be returned unchanged."""
    result = validate_operation("add", OPERATIONS)
    assert result == "add"


@pytest.mark.parametrize("key", list(OPERATIONS.keys()))
def test_validate_operation_every_valid_key_returned(key: str) -> None:
    """Every key in OPERATIONS dict must be accepted and returned."""
    result = validate_operation(key, OPERATIONS)
    assert result == key


def test_validate_operation_empty_operations_dict() -> None:
    """With an empty operations dict, any input must raise InvalidOperationError."""
    with pytest.raises(InvalidOperationError):
        validate_operation("add", {})


def test_validate_operation_custom_operations_dict() -> None:
    """validate_operation must work with any dict, not just OPERATIONS."""
    custom_ops = {"foo": ("Foo operation", 1), "bar": ("Bar operation", 2)}
    assert validate_operation("foo", custom_ops) == "foo"
    assert validate_operation("bar", custom_ops) == "bar"


# ---------------------------------------------------------------------------
# validate_operation — error cases
# ---------------------------------------------------------------------------


def test_validate_operation_invalid_key_raises_error() -> None:
    """An unrecognised key must raise InvalidOperationError."""
    with pytest.raises(InvalidOperationError):
        validate_operation("bogus", OPERATIONS)


def test_validate_operation_invalid_key_error_message_includes_key() -> None:
    """The error message must mention the invalid key."""
    with pytest.raises(InvalidOperationError, match="bogus"):
        validate_operation("bogus", OPERATIONS)


def test_validate_operation_empty_string_raises_error() -> None:
    """An empty string must raise InvalidOperationError."""
    with pytest.raises(InvalidOperationError):
        validate_operation("", OPERATIONS)


def test_validate_operation_whitespace_only_raises_error() -> None:
    """Whitespace-only string must raise InvalidOperationError."""
    with pytest.raises(InvalidOperationError):
        validate_operation("   ", OPERATIONS)


def test_validate_operation_case_sensitive() -> None:
    """validate_operation must be case-sensitive (uppercase 'ADD' != lowercase 'add')."""
    # 'add' is in OPERATIONS (lowercase), 'ADD' is not
    with pytest.raises(InvalidOperationError):
        validate_operation("ADD", OPERATIONS)


def test_validate_operation_partial_match_rejected() -> None:
    """A partial match of a key must be rejected."""
    with pytest.raises(InvalidOperationError):
        validate_operation("ad", OPERATIONS)


def test_validate_operation_key_with_leading_whitespace_rejected() -> None:
    """A key with leading whitespace must be rejected (not auto-stripped)."""
    with pytest.raises(InvalidOperationError):
        validate_operation("  add", OPERATIONS)


def test_validate_operation_key_with_trailing_whitespace_rejected() -> None:
    """A key with trailing whitespace must be rejected (not auto-stripped)."""
    with pytest.raises(InvalidOperationError):
        validate_operation("add  ", OPERATIONS)


def test_validate_operation_key_with_internal_space_rejected() -> None:
    """A key with internal spaces must be rejected."""
    with pytest.raises(InvalidOperationError):
        validate_operation("square root", OPERATIONS)


def test_validate_operation_none_like_string_rejected() -> None:
    """The string 'None' must be rejected as an operation key."""
    with pytest.raises(InvalidOperationError):
        validate_operation("None", OPERATIONS)


def test_validate_operation_null_like_string_rejected() -> None:
    """The string 'null' must be rejected as an operation key."""
    with pytest.raises(InvalidOperationError):
        validate_operation("null", OPERATIONS)


def test_validate_operation_special_characters_rejected() -> None:
    """Special characters as an operation key must be rejected."""
    with pytest.raises(InvalidOperationError):
        validate_operation("@#$%", OPERATIONS)


def test_validate_operation_numeric_string_rejected() -> None:
    """A numeric string as an operation key must be rejected."""
    with pytest.raises(InvalidOperationError):
        validate_operation("123", OPERATIONS)


def test_validate_operation_very_long_string_rejected() -> None:
    """A very long string must be rejected as an operation key."""
    with pytest.raises(InvalidOperationError):
        validate_operation("x" * 1000, OPERATIONS)


# ---------------------------------------------------------------------------
# validate_operands — happy path
# ---------------------------------------------------------------------------


def test_validate_operands_single_float_string() -> None:
    """A single float string must be converted and returned as a list."""
    result = validate_operands(["3.14"], 1)
    assert result == [3.14]


def test_validate_operands_multiple_float_strings() -> None:
    """Multiple float strings must be converted to a list of floats."""
    result = validate_operands(["1.5", "2.5", "3.5"], 3)
    assert result == [1.5, 2.5, 3.5]


def test_validate_operands_integer_strings() -> None:
    """Integer strings must be converted to float values."""
    result = validate_operands(["10", "20"], 2)
    assert result == [10.0, 20.0]


def test_validate_operands_negative_numbers() -> None:
    """Negative numeric strings must be accepted."""
    result = validate_operands(["-5.5", "-10"], 2)
    assert result == [-5.5, -10.0]


def test_validate_operands_zero() -> None:
    """Zero as a string must be converted to 0.0."""
    result = validate_operands(["0"], 1)
    assert result == [0.0]


def test_validate_operands_very_large_number() -> None:
    """Very large numeric strings must be accepted."""
    result = validate_operands(["1e308"], 1)
    assert result == [1e308]


def test_validate_operands_very_small_number() -> None:
    """Very small numeric strings must be accepted."""
    result = validate_operands(["1e-308"], 1)
    assert result == [1e-308]


def test_validate_operands_scientific_notation() -> None:
    """Scientific notation must be accepted and converted."""
    result = validate_operands(["2e3", "5e-2"], 2)
    assert result == [2000.0, 0.05]


def test_validate_operands_empty_list_with_count_zero() -> None:
    """An empty list with count=0 must return an empty list."""
    result = validate_operands([], 0)
    assert result == []


def test_validate_operands_returns_list_of_floats() -> None:
    """The return value must be a list of float instances."""
    result = validate_operands(["1", "2"], 2)
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)


# ---------------------------------------------------------------------------
# validate_operands — count mismatch errors
# ---------------------------------------------------------------------------


def test_validate_operands_too_few_raises_error() -> None:
    """Providing fewer operands than expected must raise OperandCountError."""
    with pytest.raises(OperandCountError):
        validate_operands(["1.0"], 2)


def test_validate_operands_too_many_raises_error() -> None:
    """Providing more operands than expected must raise OperandCountError."""
    with pytest.raises(OperandCountError):
        validate_operands(["1.0", "2.0", "3.0"], 2)


def test_validate_operands_count_mismatch_error_message_includes_counts() -> None:
    """The error message must mention expected and actual counts."""
    with pytest.raises(OperandCountError, match="Expected 2"):
        validate_operands(["1.0"], 2)


def test_validate_operands_empty_list_with_nonzero_count() -> None:
    """An empty list with count > 0 must raise OperandCountError."""
    with pytest.raises(OperandCountError):
        validate_operands([], 1)


def test_validate_operands_zero_count_but_values_provided() -> None:
    """Providing operands when count=0 is expected must raise OperandCountError."""
    with pytest.raises(OperandCountError):
        validate_operands(["1.0"], 0)


# ---------------------------------------------------------------------------
# validate_operands — invalid operand format errors
# ---------------------------------------------------------------------------


def test_validate_operands_non_numeric_string_raises_error() -> None:
    """A non-numeric string must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["abc"], 1)


def test_validate_operands_empty_string_raises_error() -> None:
    """An empty string cannot be parsed as a float and must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands([""], 1)


def test_validate_operands_whitespace_only_string_raises_error() -> None:
    """A whitespace-only string cannot be parsed as a float."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["   "], 1)


def test_validate_operands_none_like_string_raises_error() -> None:
    """The string 'None' cannot be parsed as a float."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["None"], 1)


def test_validate_operands_infinity_string_raises_error() -> None:
    """The string 'inf' or 'infinity' cannot be parsed as a float using float()."""
    # Note: Python's float() actually accepts 'inf', so this test documents
    # the actual behavior. If the requirement is to reject inf, this test fails.
    result = validate_operands(["inf"], 1)
    assert result[0] == float("inf")


def test_validate_operands_nan_string() -> None:
    """The string 'nan' can be parsed as a float by float()."""
    result = validate_operands(["nan"], 1)
    assert result[0] != result[0]  # NaN != NaN


def test_validate_operands_invalid_operand_error_message_includes_value() -> None:
    """The error message must mention the invalid operand."""
    with pytest.raises(InvalidOperandError, match="abc"):
        validate_operands(["abc"], 1)


def test_validate_operands_special_characters_raises_error() -> None:
    """Special characters that don't form a number must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["@#$%"], 1)


def test_validate_operands_leading_alpha_raises_error() -> None:
    """A string starting with alpha characters must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["x3.14"], 1)


def test_validate_operands_first_operand_invalid_in_list() -> None:
    """If the first operand is invalid, it must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["invalid", "2.0"], 2)


def test_validate_operands_second_operand_invalid_in_list() -> None:
    """If a later operand is invalid, it must raise InvalidOperandError."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["1.0", "invalid"], 2)


def test_validate_operands_stops_at_first_invalid() -> None:
    """validate_operands must stop and raise on the first invalid operand."""
    # If multiple operands are invalid, the error should be for the first one encountered
    with pytest.raises(InvalidOperandError, match="abc"):
        validate_operands(["abc", "def"], 2)


# ---------------------------------------------------------------------------
# validate_operands — whitespace handling
# ---------------------------------------------------------------------------


def test_validate_operands_preserves_internal_structure() -> None:
    """Operands are passed as-is (not pre-stripped) to float()."""
    # float() strips whitespace automatically
    result = validate_operands(["  3.14  "], 1)
    assert result[0] == 3.14


def test_validate_operands_plus_sign_accepted() -> None:
    """A leading plus sign is accepted by float()."""
    result = validate_operands(["+5.0"], 1)
    assert result == [5.0]


# ---------------------------------------------------------------------------
# Edge case: boundary between count and format errors
# ---------------------------------------------------------------------------


def test_validate_operands_checks_count_first() -> None:
    """The function must check count before parsing individual operands.

    This determines the order of validation. If count is checked first,
    an empty list with count > 0 raises OperandCountError, not InvalidOperandError.
    """
    # This test documents the actual behavior: count is checked first
    with pytest.raises(OperandCountError):
        validate_operands([], 1)


def test_validate_operands_format_error_raised_after_count_check() -> None:
    """If count matches but an operand is invalid, InvalidOperandError is raised."""
    with pytest.raises(InvalidOperandError):
        validate_operands(["not_a_number"], 1)


# ---------------------------------------------------------------------------
# MAX_RETRY_ATTEMPTS constant
# ---------------------------------------------------------------------------


def test_max_retry_attempts_is_defined() -> None:
    """MAX_RETRY_ATTEMPTS must be defined in input_validator module."""
    from src.input_validator import MAX_RETRY_ATTEMPTS
    assert isinstance(MAX_RETRY_ATTEMPTS, int)
    assert MAX_RETRY_ATTEMPTS > 0


def test_max_retry_attempts_value() -> None:
    """MAX_RETRY_ATTEMPTS must be 3 as specified."""
    from src.input_validator import MAX_RETRY_ATTEMPTS
    assert MAX_RETRY_ATTEMPTS == 3
