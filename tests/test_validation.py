"""Comprehensive tests for src/validation.py.

Tests cover:
- RetryCounter: increment, reset, get, is_exhausted
- validate_operation: valid/invalid keys, error messages
- validate_operand: valid/invalid numeric input, coercion, error messages
- RetryExhausted: exception attributes and behavior
"""

import pytest

from src.validation import (
    RetryCounter,
    RetryExhausted,
    validate_operation,
    validate_operand,
)


# ---------------------------------------------------------------------------
# TestRetryCounter
# ---------------------------------------------------------------------------

class TestRetryCounter:
    """Tests for RetryCounter class."""

    def test_initial_count_is_zero(self):
        """Fresh counter returns 0 for any key."""
        counter = RetryCounter()
        assert counter.get("operation") == 0
        assert counter.get("operand") == 0
        assert counter.get("any_key") == 0

    def test_increment_returns_new_count(self):
        """increment from 0 returns 1."""
        counter = RetryCounter()
        result = counter.increment("operation")
        assert result == 1

    def test_increment_multiple_times(self):
        """3 increments returns 3."""
        counter = RetryCounter()
        counter.increment("operation")
        counter.increment("operation")
        result = counter.increment("operation")
        assert result == 3
        assert counter.get("operation") == 3

    def test_independent_counters(self):
        """operation and operand counters are independent."""
        counter = RetryCounter()
        counter.increment("operation")
        counter.increment("operation")
        counter.increment("operand")
        assert counter.get("operation") == 2
        assert counter.get("operand") == 1

    def test_reset_returns_to_zero(self):
        """increment 3 times then reset; get returns 0."""
        counter = RetryCounter()
        counter.increment("operation")
        counter.increment("operation")
        counter.increment("operation")
        counter.reset("operation")
        assert counter.get("operation") == 0

    def test_get_default_zero(self):
        """unseen key returns 0."""
        counter = RetryCounter()
        assert counter.get("never_seen") == 0

    def test_is_exhausted_false_below_limit(self):
        """4 increments, max_retries=5 → False."""
        counter = RetryCounter()
        counter.increment("test")
        counter.increment("test")
        counter.increment("test")
        counter.increment("test")
        assert counter.is_exhausted("test", 5) is False

    def test_is_exhausted_true_at_limit(self):
        """5 increments, max_retries=5 → True."""
        counter = RetryCounter()
        for _ in range(5):
            counter.increment("test")
        assert counter.is_exhausted("test", 5) is True

    def test_is_exhausted_true_above_limit(self):
        """6 increments, max_retries=5 → True."""
        counter = RetryCounter()
        for _ in range(6):
            counter.increment("test")
        assert counter.is_exhausted("test", 5) is True

    def test_is_exhausted_false_at_zero(self):
        """0 increments, max_retries=5 → False."""
        counter = RetryCounter()
        assert counter.is_exhausted("test", 5) is False

    def test_increment_with_different_input_types(self):
        """Multiple different input_type keys maintain separate counts."""
        counter = RetryCounter()
        counter.increment("op1")
        counter.increment("op1")
        counter.increment("op2")
        counter.increment("op3")
        counter.increment("op3")
        counter.increment("op3")
        assert counter.get("op1") == 2
        assert counter.get("op2") == 1
        assert counter.get("op3") == 3

    def test_reset_only_affects_specified_type(self):
        """reset("op1") does not affect other counters."""
        counter = RetryCounter()
        counter.increment("op1")
        counter.increment("op2")
        counter.reset("op1")
        assert counter.get("op1") == 0
        assert counter.get("op2") == 1


# ---------------------------------------------------------------------------
# TestValidateOperation
# ---------------------------------------------------------------------------

class TestValidateOperation:
    """Tests for validate_operation function."""

    def test_valid_operation_returns_key(self):
        """returns the op_key unchanged if valid."""
        ops = {"add": {}, "subtract": {}}
        result = validate_operation("add", ops)
        assert result == "add"

    def test_invalid_operation_raises_value_error(self):
        """raises ValueError for unknown key."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError):
            validate_operation("badop", ops)

    def test_error_message_includes_invalid_key(self):
        """ValueError message includes the invalid key."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError, match="badop"):
            validate_operation("badop", ops)

    def test_error_message_includes_available_operations(self):
        """ValueError message includes 'Available operations:' and lists keys."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError, match="Available operations:"):
            validate_operation("badop", ops)

    def test_error_message_lists_all_available_keys(self):
        """Error message includes all keys from operations dict."""
        ops = {"add": {}, "subtract": {}, "multiply": {}}
        try:
            validate_operation("badop", ops)
        except ValueError as exc:
            msg = str(exc)
            assert "add" in msg
            assert "subtract" in msg
            assert "multiply" in msg

    def test_all_registered_operations_valid(self):
        """Every standard operation key is valid."""
        from src.input_handler import OPERATIONS
        for op_key in OPERATIONS.keys():
            result = validate_operation(op_key, OPERATIONS)
            assert result == op_key

    def test_empty_string_invalid(self):
        """empty string raises ValueError."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError):
            validate_operation("", ops)

    def test_case_sensitive(self):
        """'Add' (capitalized) is invalid when only 'add' (lowercase) exists."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError):
            validate_operation("Add", ops)

    def test_whitespace_not_stripped(self):
        """' add' (with leading space) is invalid."""
        ops = {"add": {}, "subtract": {}}
        with pytest.raises(ValueError):
            validate_operation(" add", ops)

    def test_single_operation_dict(self):
        """dict with a single operation works correctly."""
        ops = {"only_op": {}}
        result = validate_operation("only_op", ops)
        assert result == "only_op"

    def test_unknown_with_single_operation_listed(self):
        """Unknown key with single operation lists that operation."""
        ops = {"only_op": {}}
        with pytest.raises(ValueError, match="only_op"):
            validate_operation("unknown", ops)


# ---------------------------------------------------------------------------
# TestValidateOperand
# ---------------------------------------------------------------------------

class TestValidateOperand:
    """Tests for validate_operand function."""

    def test_valid_float(self):
        """'3.14' → 3.14."""
        result = validate_operand("3.14", float)
        assert result == pytest.approx(3.14)

    def test_valid_integer(self):
        """'5' → 5.0 (via float coerce)."""
        result = validate_operand("5", float)
        assert result == 5.0

    def test_valid_negative(self):
        """-10' → -10.0."""
        result = validate_operand("-10", float)
        assert result == -10.0

    def test_valid_zero(self):
        """'0' → 0.0."""
        result = validate_operand("0", float)
        assert result == 0.0

    def test_valid_scientific_notation(self):
        """'1e3' → 1000.0."""
        result = validate_operand("1e3", float)
        assert result == 1000.0

    def test_valid_scientific_notation_negative_exponent(self):
        """'1e-2' → 0.01."""
        result = validate_operand("1e-2", float)
        assert result == pytest.approx(0.01)

    def test_invalid_string_raises_value_error(self):
        """'abc' raises ValueError."""
        with pytest.raises(ValueError):
            validate_operand("abc", float)

    def test_invalid_empty_string_raises_value_error(self):
        """'' raises ValueError."""
        with pytest.raises(ValueError):
            validate_operand("", float)

    def test_invalid_special_chars(self):
        """'5@3' raises ValueError."""
        with pytest.raises(ValueError):
            validate_operand("5@3", float)

    def test_error_message_includes_operand(self):
        """ValueError message includes the invalid operand."""
        with pytest.raises(ValueError, match="abc"):
            validate_operand("abc", float)

    def test_error_message_indicates_numeric_expected(self):
        """ValueError message mentions 'numeric value'."""
        with pytest.raises(ValueError, match="numeric"):
            validate_operand("notanumber", float)

    def test_coerce_int(self):
        """coerce=int: '5' → 5 (integer type)."""
        result = validate_operand("5", int)
        assert result == 5
        assert isinstance(result, int)

    def test_coerce_int_invalid_float_string(self):
        """coerce=int: '3.5' raises ValueError (int() cannot parse '3.5')."""
        with pytest.raises(ValueError):
            validate_operand("3.5", int)

    def test_operand_position_in_error_optional(self):
        """Providing operand_position parameter does not break the function."""
        result = validate_operand("2.5", float, operand_position="first")
        assert result == 2.5

    def test_whitespace_accepted_by_float(self):
        """Leading/trailing whitespace is accepted by float() coercion."""
        result = validate_operand("  5  ", float)
        assert result == 5.0

    def test_valid_negative_float(self):
        """-3.14' → -3.14."""
        result = validate_operand("-3.14", float)
        assert result == pytest.approx(-3.14)

    def test_valid_large_number(self):
        """Very large number as string coerces correctly."""
        result = validate_operand("9" * 50, float)
        assert result > 0

    def test_infinity_string(self):
        """'inf' coerces to float('inf')."""
        result = validate_operand("inf", float)
        assert result == float("inf")

    def test_negative_infinity_string(self):
        """'-inf' coerces to float('-inf')."""
        result = validate_operand("-inf", float)
        assert result == float("-inf")


# ---------------------------------------------------------------------------
# TestRetryExhausted
# ---------------------------------------------------------------------------

class TestRetryExhausted:
    """Tests for RetryExhausted exception."""

    def test_exception_stores_input_type(self):
        """input_type attribute is set."""
        exc = RetryExhausted("operation", 5)
        assert exc.input_type == "operation"

    def test_exception_stores_max_retries(self):
        """max_retries attribute is set."""
        exc = RetryExhausted("operation", 5)
        assert exc.max_retries == 5

    def test_exception_is_subclass_of_exception(self):
        """isinstance check."""
        exc = RetryExhausted("operand", 5)
        assert isinstance(exc, Exception)

    def test_exception_message_contains_type_and_limit(self):
        """str(exc) includes input_type and max_retries."""
        exc = RetryExhausted("operation", 5)
        msg = str(exc)
        assert "operation" in msg
        assert "5" in msg

    def test_exception_message_format(self):
        """Exception message follows expected format."""
        exc = RetryExhausted("operand", 3)
        msg = str(exc)
        assert "Max retries" in msg
        assert "3" in msg
        assert "operand" in msg

    def test_exception_can_be_raised_and_caught(self):
        """Exception can be raised and caught as normal."""
        with pytest.raises(RetryExhausted) as exc_info:
            raise RetryExhausted("test_input", 10)
        assert exc_info.value.input_type == "test_input"
        assert exc_info.value.max_retries == 10

    def test_different_input_types(self):
        """Different input_type values are preserved."""
        exc1 = RetryExhausted("operation", 5)
        exc2 = RetryExhausted("operand", 5)
        assert exc1.input_type == "operation"
        assert exc2.input_type == "operand"

    def test_different_retry_limits(self):
        """Different max_retries values are preserved."""
        exc1 = RetryExhausted("test", 3)
        exc2 = RetryExhausted("test", 10)
        assert exc1.max_retries == 3
        assert exc2.max_retries == 10
