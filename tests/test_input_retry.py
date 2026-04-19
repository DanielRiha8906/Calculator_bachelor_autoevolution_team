"""Comprehensive tests for the input_retry module.

Tests cover:
- validate_with_retry: success on first attempt, retries, error formatting, exceptions
- InputRetryConfig: default values, custom configuration
- RetryLimitExceeded: proper exception raising
"""

import pytest
from io import StringIO
import sys

from src.input_retry import (
    validate_with_retry,
    InputRetryConfig,
    RetryLimitExceeded,
    DEFAULT_MAX_RETRIES,
)


# ============================================================================
# DEFAULT_MAX_RETRIES TESTS
# ============================================================================


class TestDefaultMaxRetries:
    """Test suite for DEFAULT_MAX_RETRIES constant."""

    def test_default_max_retries_is_3(self):
        """Test that DEFAULT_MAX_RETRIES equals 3."""
        assert DEFAULT_MAX_RETRIES == 3


# ============================================================================
# RETRY_LIMIT_EXCEEDED EXCEPTION TESTS
# ============================================================================


class TestRetryLimitExceededException:
    """Test suite for RetryLimitExceeded exception."""

    def test_retry_limit_exceeded_is_exception(self):
        """Test that RetryLimitExceeded is an Exception subclass."""
        assert issubclass(RetryLimitExceeded, Exception)

    def test_retry_limit_exceeded_can_be_raised(self):
        """Test that RetryLimitExceeded can be raised."""
        with pytest.raises(RetryLimitExceeded):
            raise RetryLimitExceeded("Test message")

    def test_retry_limit_exceeded_message_preserved(self):
        """Test that RetryLimitExceeded preserves custom message."""
        msg = "Custom error message"
        with pytest.raises(RetryLimitExceeded) as exc_info:
            raise RetryLimitExceeded(msg)
        assert msg in str(exc_info.value)


# ============================================================================
# INPUT_RETRY_CONFIG TESTS
# ============================================================================


class TestInputRetryConfig:
    """Test suite for InputRetryConfig dataclass."""

    def test_input_retry_config_default_max_attempts(self):
        """Test that InputRetryConfig uses DEFAULT_MAX_RETRIES by default."""
        config = InputRetryConfig()
        assert config.max_attempts == DEFAULT_MAX_RETRIES
        assert config.max_attempts == 3

    def test_input_retry_config_custom_max_attempts(self):
        """Test that InputRetryConfig accepts custom max_attempts."""
        config = InputRetryConfig(max_attempts=5)
        assert config.max_attempts == 5

    def test_input_retry_config_max_attempts_one(self):
        """Test InputRetryConfig with max_attempts=1."""
        config = InputRetryConfig(max_attempts=1)
        assert config.max_attempts == 1

    def test_input_retry_config_max_attempts_large(self):
        """Test InputRetryConfig with large max_attempts."""
        config = InputRetryConfig(max_attempts=100)
        assert config.max_attempts == 100

    def test_input_retry_config_is_dataclass(self):
        """Test that InputRetryConfig behaves as a dataclass."""
        config1 = InputRetryConfig(max_attempts=3)
        config2 = InputRetryConfig(max_attempts=3)
        # Dataclasses should support equality comparison
        assert config1 == config2

    def test_input_retry_config_different_values_not_equal(self):
        """Test that InputRetryConfig instances with different values are not equal."""
        config1 = InputRetryConfig(max_attempts=3)
        config2 = InputRetryConfig(max_attempts=5)
        assert config1 != config2


# ============================================================================
# VALIDATE_WITH_RETRY TESTS - HAPPY PATH
# ============================================================================


class TestValidateWithRetryHappyPath:
    """Test suite for validate_with_retry happy path scenarios."""

    def test_validate_with_retry_success_first_attempt(self, capsys):
        """Test validate_with_retry returns value immediately on first valid attempt."""
        def input_fn():
            return "5"

        def validator(value):
            return value == "5"

        def error_formatter(value, attempt, max_attempts):
            return f"Error: {value}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == "5"
        # Verify no error messages were printed
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_validate_with_retry_success_with_default_config(self, capsys):
        """Test validate_with_retry with default config (None)."""
        def input_fn():
            return 42

        def validator(value):
            return isinstance(value, int) and value == 42

        def error_formatter(value, attempt, max_attempts):
            return f"Invalid: {value}"

        result = validate_with_retry(input_fn, validator, error_formatter, config=None)
        assert result == 42
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_validate_with_retry_success_with_custom_config(self, capsys):
        """Test validate_with_retry with custom InputRetryConfig."""
        def input_fn():
            return "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Error"

        config = InputRetryConfig(max_attempts=5)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)
        assert result == "valid"

    def test_validate_with_retry_numeric_value_validation(self, capsys):
        """Test validate_with_retry with numeric values."""
        def input_fn():
            return 100

        def validator(value):
            return isinstance(value, int) and value > 0

        def error_formatter(value, attempt, max_attempts):
            return "Invalid number"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == 100

    def test_validate_with_retry_with_list_value(self, capsys):
        """Test validate_with_retry can handle list values."""
        def input_fn():
            return [1, 2, 3]

        def validator(value):
            return isinstance(value, list) and len(value) == 3

        def error_formatter(value, attempt, max_attempts):
            return "Invalid list"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == [1, 2, 3]

    def test_validate_with_retry_with_dict_value(self, capsys):
        """Test validate_with_retry can handle dict values."""
        def input_fn():
            return {"key": "value"}

        def validator(value):
            return isinstance(value, dict) and "key" in value

        def error_formatter(value, attempt, max_attempts):
            return "Invalid dict"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == {"key": "value"}


# ============================================================================
# VALIDATE_WITH_RETRY TESTS - RETRIES AND ERROR FORMATTING
# ============================================================================


class TestValidateWithRetryRetriesAndErrorFormatting:
    """Test suite for validate_with_retry retry behavior and error formatting."""

    def test_validate_with_retry_retries_once_before_success(self, capsys):
        """Test validate_with_retry retries once before success."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] == 1 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Error on attempt {attempt}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == "valid"
        assert call_count[0] == 2

    def test_validate_with_retry_retries_twice_before_success(self, capsys):
        """Test validate_with_retry retries twice before success."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            if call_count[0] < 3:
                return "invalid"
            return "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Error {attempt}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == "valid"
        assert call_count[0] == 3

    def test_validate_with_retry_error_formatter_called_with_correct_args(self, capsys):
        """Test that error_formatter is called with correct (value, attempt, max_attempts)."""
        call_count = [0]
        formatter_calls = []

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] == 1 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            formatter_calls.append((value, attempt, max_attempts))
            return f"Error"

        config = InputRetryConfig(max_attempts=3)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)

        # Check that formatter was called once with correct args
        assert len(formatter_calls) == 1
        assert formatter_calls[0] == ("invalid", 1, 3)

    def test_validate_with_retry_error_formatter_called_multiple_times(self, capsys):
        """Test that error_formatter is called for each failed attempt."""
        call_count = [0]
        formatter_calls = []

        def input_fn():
            call_count[0] += 1
            if call_count[0] < 3:
                return "invalid"
            return "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            formatter_calls.append((value, attempt, max_attempts))
            return f"Error on attempt {attempt}"

        config = InputRetryConfig(max_attempts=5)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)

        # Check that formatter was called twice (attempts 1 and 2)
        assert len(formatter_calls) == 2
        assert formatter_calls[0] == ("invalid", 1, 5)
        assert formatter_calls[1] == ("invalid", 2, 5)

    def test_validate_with_retry_error_formatter_output_printed(self, capsys):
        """Test that error_formatter output is printed to stdout."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] == 1 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Custom error message on attempt {attempt}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        captured = capsys.readouterr()
        assert "Custom error message on attempt 1" in captured.out

    def test_validate_with_retry_error_formatter_with_multiple_failures(self, capsys):
        """Test error_formatter output for multiple failures."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            if call_count[0] <= 2:
                return f"invalid_{call_count[0]}"
            return "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Error: {value} on attempt {attempt}/{max_attempts}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        captured = capsys.readouterr()
        assert "Error: invalid_1 on attempt 1/3" in captured.out
        assert "Error: invalid_2 on attempt 2/3" in captured.out

    def test_validate_with_retry_attempt_counter_increments(self, capsys):
        """Test that attempt counter in error_formatter increments correctly."""
        call_count = [0]
        attempts = []

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] < 4 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            attempts.append(attempt)
            return f"Attempt {attempt}"

        config = InputRetryConfig(max_attempts=5)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)

        # Attempts should be [1, 2, 3]
        assert attempts == [1, 2, 3]


# ============================================================================
# VALIDATE_WITH_RETRY TESTS - RETRY LIMIT AND EXCEPTIONS
# ============================================================================


class TestValidateWithRetryRetryLimitAndExceptions:
    """Test suite for validate_with_retry retry limits and exception handling."""

    def test_validate_with_retry_raises_on_max_attempts_exceeded(self):
        """Test that validate_with_retry raises RetryLimitExceeded after max attempts."""
        def input_fn():
            return "invalid"

        def validator(value):
            return False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        with pytest.raises(RetryLimitExceeded):
            validate_with_retry(input_fn, validator, error_formatter)

    def test_validate_with_retry_raises_with_default_3_attempts(self):
        """Test that default is 3 attempts before raising."""
        attempt_count = [0]

        def input_fn():
            attempt_count[0] += 1
            return "invalid"

        def validator(value):
            return False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        with pytest.raises(RetryLimitExceeded):
            validate_with_retry(input_fn, validator, error_formatter)

        # Should have been called exactly 3 times
        assert attempt_count[0] == 3

    def test_validate_with_retry_raises_with_custom_max_attempts(self):
        """Test that custom max_attempts is respected."""
        attempt_count = [0]

        def input_fn():
            attempt_count[0] += 1
            return "invalid"

        def validator(value):
            return False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        config = InputRetryConfig(max_attempts=5)
        with pytest.raises(RetryLimitExceeded):
            validate_with_retry(input_fn, validator, error_formatter, config=config)

        assert attempt_count[0] == 5

    def test_validate_with_retry_raises_with_max_attempts_1(self):
        """Test that max_attempts=1 raises on first failure."""
        attempt_count = [0]

        def input_fn():
            attempt_count[0] += 1
            return "invalid"

        def validator(value):
            return False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        config = InputRetryConfig(max_attempts=1)
        with pytest.raises(RetryLimitExceeded):
            validate_with_retry(input_fn, validator, error_formatter, config=config)

        assert attempt_count[0] == 1

    def test_validate_with_retry_exception_from_validator_treated_as_failure(self, capsys):
        """Test that exceptions raised by validator are treated as failures."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] == 1 else "valid"

        def validator(value):
            if value == "invalid":
                raise ValueError("Invalid value!")
            return True

        def error_formatter(value, attempt, max_attempts):
            return f"Error on attempt {attempt}"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == "valid"
        assert call_count[0] == 2

    def test_validate_with_retry_validator_exception_exhausts_retries(self, capsys):
        """Test that validator exceptions exhaust retry attempts."""
        def input_fn():
            return "always_fails"

        def validator(value):
            raise RuntimeError("Validator always fails")

        def error_formatter(value, attempt, max_attempts):
            return f"Error {attempt}"

        with pytest.raises(RetryLimitExceeded):
            validate_with_retry(input_fn, validator, error_formatter)

    def test_validate_with_retry_multiple_exception_types_caught(self, capsys):
        """Test that different exception types from validator are caught."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            if call_count[0] == 1:
                return "value1"
            elif call_count[0] == 2:
                return "value2"
            return "valid"

        def validator(value):
            if value == "value1":
                raise TypeError("Type error")
            elif value == "value2":
                raise KeyError("Key error")
            return True

        def error_formatter(value, attempt, max_attempts):
            return f"Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == "valid"
        assert call_count[0] == 3

    def test_validate_with_retry_exception_message_preserved_in_retry_limit_exceeded(self):
        """Test that RetryLimitExceeded includes descriptive message."""
        def input_fn():
            return "invalid"

        def validator(value):
            return False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        config = InputRetryConfig(max_attempts=2)
        with pytest.raises(RetryLimitExceeded) as exc_info:
            validate_with_retry(input_fn, validator, error_formatter, config=config)

        error_msg = str(exc_info.value)
        assert "2" in error_msg  # Should mention number of attempts
        assert "attempt" in error_msg.lower()


# ============================================================================
# VALIDATE_WITH_RETRY TESTS - EDGE CASES
# ============================================================================


class TestValidateWithRetryEdgeCases:
    """Test suite for validate_with_retry edge cases."""

    def test_validate_with_retry_with_none_value(self, capsys):
        """Test validate_with_retry with None as a valid return value."""
        def input_fn():
            return None

        def validator(value):
            return value is None

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result is None

    def test_validate_with_retry_with_false_as_valid_value(self, capsys):
        """Test validate_with_retry where False is a valid value (not failure)."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return False

        def validator(value):
            # Return True if we successfully validated False
            return value is False

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result is False
        assert call_count[0] == 1

    def test_validate_with_retry_with_empty_string_value(self, capsys):
        """Test validate_with_retry with empty string as valid value."""
        def input_fn():
            return ""

        def validator(value):
            return value == ""

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == ""

    def test_validate_with_retry_with_empty_list_value(self, capsys):
        """Test validate_with_retry with empty list as valid value."""
        def input_fn():
            return []

        def validator(value):
            return isinstance(value, list)

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == []

    def test_validate_with_retry_with_zero_value(self, capsys):
        """Test validate_with_retry with zero as valid value."""
        def input_fn():
            return 0

        def validator(value):
            return isinstance(value, int) and value == 0

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        assert result == 0

    def test_validate_with_retry_large_max_attempts(self, capsys):
        """Test validate_with_retry with large max_attempts."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return "valid" if call_count[0] == 50 else "invalid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return f"Error"

        config = InputRetryConfig(max_attempts=100)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)
        assert result == "valid"
        assert call_count[0] == 50

    def test_validate_with_retry_complex_validator_logic(self, capsys):
        """Test validate_with_retry with complex validation logic."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            # Return values: 1, 2, 3, 4, 5, 6, ... to eventually hit an even number > 4
            return call_count[0]

        def validator(value):
            # Only accept values that are even and greater than 4
            # This means 6, 8, 10, ... are valid
            return isinstance(value, int) and value % 2 == 0 and value > 4

        def error_formatter(value, attempt, max_attempts):
            return f"Invalid: {value}"

        result = validate_with_retry(input_fn, validator, error_formatter, config=InputRetryConfig(max_attempts=10))
        assert result == 6
        assert call_count[0] == 6

    def test_validate_with_retry_error_formatter_receives_all_attempts_info(self, capsys):
        """Test that error_formatter receives correct max_attempts each time."""
        call_count = [0]
        formatter_calls = []

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] < 3 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            formatter_calls.append((attempt, max_attempts))
            return "Error"

        config = InputRetryConfig(max_attempts=7)
        result = validate_with_retry(input_fn, validator, error_formatter, config=config)

        # All formatter calls should have max_attempts=7
        for attempt, max_attempts in formatter_calls:
            assert max_attempts == 7

    def test_validate_with_retry_input_fn_called_exactly_as_many_times_as_needed(self, capsys):
        """Test that input_fn is called exactly once per attempt (no extra calls)."""
        call_count = [0]

        def input_fn():
            call_count[0] += 1
            return "invalid" if call_count[0] < 3 else "valid"

        def validator(value):
            return value == "valid"

        def error_formatter(value, attempt, max_attempts):
            return "Error"

        result = validate_with_retry(input_fn, validator, error_formatter)
        # Should be called exactly 3 times: twice returning "invalid", once "valid"
        assert call_count[0] == 3


# ============================================================================
# PARAMETRIZED TESTS FOR COMPREHENSIVE COVERAGE
# ============================================================================


@pytest.mark.parametrize("max_attempts,expected_calls", [
    (1, 1),
    (2, 2),
    (3, 3),
    (5, 5),
    (10, 10),
])
def test_validate_with_retry_parametrized_max_attempts(max_attempts, expected_calls):
    """Parametrized test for different max_attempts values."""
    call_count = [0]

    def input_fn():
        call_count[0] += 1
        return "invalid"

    def validator(value):
        return False

    def error_formatter(value, attempt, max_attempts):
        return "Error"

    config = InputRetryConfig(max_attempts=max_attempts)
    with pytest.raises(RetryLimitExceeded):
        validate_with_retry(input_fn, validator, error_formatter, config=config)

    assert call_count[0] == expected_calls


@pytest.mark.parametrize("success_on_attempt", [1, 2, 3, 5])
def test_validate_with_retry_parametrized_success_attempts(success_on_attempt):
    """Parametrized test for success on various attempts."""
    call_count = [0]

    def input_fn():
        call_count[0] += 1
        return "valid" if call_count[0] == success_on_attempt else "invalid"

    def validator(value):
        return value == "valid"

    def error_formatter(value, attempt, max_attempts):
        return "Error"

    config = InputRetryConfig(max_attempts=10)
    result = validate_with_retry(input_fn, validator, error_formatter, config=config)

    assert result == "valid"
    assert call_count[0] == success_on_attempt
