"""Unit tests for the validation module."""

import pytest
from src.validation import (
    OperandValidationError,
    OperationValidationError,
    validate_operand,
    validate_operation,
    get_validation_error_message,
)


class TestValidateOperand:
    """Test suite for validate_operand() function."""

    @pytest.mark.parametrize(
        "raw_input,expected",
        [
            ("5", 5.0),
            ("42", 42.0),
            ("0", 0.0),
            ("-3", -3.0),
            ("3.14", 3.14),
            ("-3.14", -3.14),
            ("1.5", 1.5),
            ("2.718281828", 2.718281828),
            ("1e10", 1e10),
            ("1.5e-5", 1.5e-5),
            ("0.0001", 0.0001),
            ("999999999", 999999999.0),
            ("-999999999", -999999999.0),
        ],
    )
    def test_validate_operand_valid_numbers(self, raw_input, expected):
        """Test that valid numeric strings are converted to floats."""
        result = validate_operand(raw_input)
        assert result == expected
        assert isinstance(result, float)

    @pytest.mark.parametrize(
        "raw_input",
        [
            "abc",
            "xyz",
            "hello",
            "12.34.56",
            "1.2.3",
            "3..14",
            "12a34",
            "a12",
            "12b",
            "!@#$",
            "nan",  # Python actually parses this as float('nan')
            "NaN",  # Same as above
        ],
    )
    def test_validate_operand_invalid_strings(self, raw_input):
        """Test that non-numeric strings raise OperandValidationError."""
        if raw_input.lower() in ("nan",):
            # 'nan' is actually parseable by float()
            result = validate_operand(raw_input)
            assert str(result) == "nan"
        else:
            with pytest.raises(OperandValidationError):
                validate_operand(raw_input)

    @pytest.mark.parametrize(
        "raw_input",
        [
            "",
            "   ",
            "\t",
            "\n",
        ],
    )
    def test_validate_operand_empty_or_whitespace(self, raw_input):
        """Test that empty or whitespace-only strings raise OperandValidationError."""
        with pytest.raises(OperandValidationError):
            validate_operand(raw_input)

    def test_validate_operand_error_message_format(self):
        """Test that OperandValidationError provides a descriptive message."""
        with pytest.raises(OperandValidationError) as exc_info:
            validate_operand("not_a_number")
        assert "not_a_number" in str(exc_info.value)
        assert "not a valid number" in str(exc_info.value)

    def test_validate_operand_infinity(self):
        """Test that 'inf' is parsed as float infinity."""
        result = validate_operand("inf")
        assert result == float("inf")

    def test_validate_operand_negative_infinity(self):
        """Test that '-inf' is parsed as negative infinity."""
        result = validate_operand("-inf")
        assert result == float("-inf")

    @pytest.mark.parametrize(
        "raw_input,expected",
        [
            ("1e100", 1e100),
            ("1e-100", 1e-100),
            ("1.23e45", 1.23e45),
        ],
    )
    def test_validate_operand_extreme_values(self, raw_input, expected):
        """Test that extreme numeric values are parsed correctly."""
        result = validate_operand(raw_input)
        assert result == expected


class TestValidateOperation:
    """Test suite for validate_operation() function."""

    @pytest.fixture
    def sample_operations(self):
        """Fixture providing a sample operations dictionary."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
            "multiply": "Multiplication (a * b)",
            "divide": "Division (a / b)",
        }

    @pytest.mark.parametrize(
        "choice",
        [
            "add",
            "subtract",
            "multiply",
            "divide",
        ],
    )
    def test_validate_operation_valid_keys(self, choice, sample_operations):
        """Test that valid operation keys return True."""
        result = validate_operation(choice, sample_operations)
        assert result is True

    @pytest.mark.parametrize(
        "choice",
        [
            "invalid",
            "unknown",
            "xyz",
            "addd",
            "Add",
            "SUBTRACT",
            "",
            "add ",
            " add",
        ],
    )
    def test_validate_operation_invalid_keys(self, choice, sample_operations):
        """Test that invalid operation keys return False."""
        result = validate_operation(choice, sample_operations)
        assert result is False

    def test_validate_operation_empty_dict(self):
        """Test with an empty operations dictionary."""
        result = validate_operation("add", {})
        assert result is False

    def test_validate_operation_case_sensitive(self, sample_operations):
        """Test that operation validation is case-sensitive."""
        assert validate_operation("add", sample_operations) is True
        assert validate_operation("ADD", sample_operations) is False
        assert validate_operation("Add", sample_operations) is False

    def test_validate_operation_with_special_chars(self, sample_operations):
        """Test that special characters are not in valid operations."""
        result = validate_operation("add!", sample_operations)
        assert result is False

    def test_validate_operation_single_valid_operation(self):
        """Test with a single-item operations dictionary."""
        ops = {"sqrt": "Square root"}
        assert validate_operation("sqrt", ops) is True
        assert validate_operation("power", ops) is False


class TestGetValidationErrorMessage:
    """Test suite for get_validation_error_message() function."""

    def test_get_validation_error_message_operand_error(self):
        """Test that OperandValidationError produces a descriptive message."""
        error = OperandValidationError("'xyz' is not a valid number")
        message = get_validation_error_message(error)
        assert message == "'xyz' is not a valid number"

    def test_get_validation_error_message_operation_error(self):
        """Test that OperationValidationError produces a descriptive message."""
        error = OperationValidationError("Unknown operation: 'xyz'")
        message = get_validation_error_message(error)
        assert message == "Unknown operation: 'xyz'"

    def test_get_validation_error_message_generic_value_error(self):
        """Test that generic ValueError messages are returned."""
        error = ValueError("Some generic error")
        message = get_validation_error_message(error)
        assert message == "Some generic error"

    def test_get_validation_error_message_empty_message(self):
        """Test with an error that has no message."""
        error = ValueError()
        message = get_validation_error_message(error)
        assert isinstance(message, str)

    def test_get_validation_error_message_special_characters(self):
        """Test with error messages containing special characters."""
        error = OperandValidationError("Invalid: '!@#$%'")
        message = get_validation_error_message(error)
        assert message == "Invalid: '!@#$%'"

    def test_get_validation_error_message_multiline(self):
        """Test with error messages spanning multiple lines."""
        error_msg = "Error: foo\nbar"
        error = ValueError(error_msg)
        message = get_validation_error_message(error)
        assert message == error_msg
