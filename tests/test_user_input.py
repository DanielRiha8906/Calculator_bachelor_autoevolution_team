"""Comprehensive tests for the user_input module.

Tests cover:
- parse_number: valid integers, floats, invalid inputs, edge cases
- get_operands: unary/binary operations, retry logic
- execute_operation: arithmetic, single-operand, error handling
- format_result: numeric formatting
- run_interactive: interactive loop behavior
"""

import pytest
from unittest.mock import patch, MagicMock, call
import sys
from io import StringIO

from src.user_input import (
    InvalidInputError,
    OPERATIONS,
    parse_number,
    get_operands,
    execute_operation,
    format_result,
    run_interactive,
)
from src.calculator import Calculator


# ============================================================================
# PARSE_NUMBER TESTS
# ============================================================================


class TestParseNumber:
    """Test suite for parse_number function."""

    def test_parse_number_valid_positive_integer(self):
        """Test parsing a valid positive integer."""
        assert parse_number("5") == 5
        assert isinstance(parse_number("5"), int)

    def test_parse_number_valid_negative_integer(self):
        """Test parsing a valid negative integer."""
        assert parse_number("-10") == -10
        assert isinstance(parse_number("-10"), int)

    def test_parse_number_zero_integer(self):
        """Test parsing zero as an integer."""
        assert parse_number("0") == 0
        assert isinstance(parse_number("0"), int)

    def test_parse_number_valid_positive_float(self):
        """Test parsing a valid positive float."""
        assert parse_number("3.14") == pytest.approx(3.14)
        assert isinstance(parse_number("3.14"), float)

    def test_parse_number_valid_negative_float(self):
        """Test parsing a valid negative float."""
        assert parse_number("-2.5") == pytest.approx(-2.5)
        assert isinstance(parse_number("-2.5"), float)

    def test_parse_number_zero_float(self):
        """Test parsing 0.0 as a float."""
        assert parse_number("0.0") == pytest.approx(0.0)

    def test_parse_number_large_integer(self):
        """Test parsing a very large integer."""
        large_int = "999999999999999999"
        assert parse_number(large_int) == 999999999999999999

    def test_parse_number_large_float(self):
        """Test parsing a very large float."""
        large_float = "1.23456789e10"
        result = parse_number(large_float)
        assert result == pytest.approx(1.23456789e10)

    def test_parse_number_small_float(self):
        """Test parsing a very small float."""
        small_float = "1.23456789e-10"
        result = parse_number(small_float)
        assert result == pytest.approx(1.23456789e-10)

    def test_parse_number_with_whitespace_prefix(self):
        """Test parsing number with leading whitespace."""
        assert parse_number("  5") == 5

    def test_parse_number_with_whitespace_suffix(self):
        """Test parsing number with trailing whitespace."""
        assert parse_number("5  ") == 5

    def test_parse_number_with_whitespace_both(self):
        """Test parsing number with leading and trailing whitespace."""
        assert parse_number("  3.14  ") == pytest.approx(3.14)

    def test_parse_number_invalid_string(self):
        """Test parsing a non-numeric string raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("abc")

    def test_parse_number_invalid_empty_string(self):
        """Test parsing empty string raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("")

    def test_parse_number_invalid_whitespace_only(self):
        """Test parsing whitespace-only string raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("   ")

    def test_parse_number_invalid_special_characters(self):
        """Test parsing string with special characters raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("5$")

    def test_parse_number_invalid_mixed_alphanumeric(self):
        """Test parsing mixed alphanumeric string raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("5a")

    def test_parse_number_invalid_multiple_dots(self):
        """Test parsing float with multiple decimal points raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("3.14.15")

    def test_parse_number_invalid_only_dot(self):
        """Test parsing string with only a dot raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number(".")

    def test_parse_number_invalid_letters_with_decimal(self):
        """Test parsing "3.14a" raises InvalidInputError."""
        with pytest.raises(InvalidInputError):
            parse_number("3.14a")

    def test_parse_number_invalid_scientific_notation_malformed(self):
        """Test parsing malformed scientific notation."""
        with pytest.raises(InvalidInputError):
            parse_number("1.5e")

    def test_parse_number_error_message_includes_input(self):
        """Test that error message includes the problematic input."""
        with pytest.raises(InvalidInputError) as exc_info:
            parse_number("invalid")
        assert "invalid" in str(exc_info.value)

    def test_parse_number_tries_int_first(self):
        """Test that int conversion is attempted before float."""
        # "5" should be parsed as int, not float
        result = parse_number("5")
        assert isinstance(result, int)
        assert result == 5

    def test_parse_number_negative_zero(self):
        """Test parsing -0 as integer."""
        result = parse_number("-0")
        assert result == 0
        assert isinstance(result, int)


# ============================================================================
# OPERATIONS DICT TESTS
# ============================================================================


class TestOperationsDict:
    """Test suite for the OPERATIONS dictionary."""

    def test_operations_dict_has_all_12_keys(self):
        """Test that OPERATIONS dict contains exactly 12 operations."""
        expected_keys = {
            "add", "subtract", "multiply", "divide",
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "log10", "natural_log"
        }
        assert set(OPERATIONS.keys()) == expected_keys
        assert len(OPERATIONS) == 12

    def test_operations_dict_binary_operations_have_2_operands(self):
        """Test that binary operations require 2 operands."""
        binary_ops = ["add", "subtract", "multiply", "divide", "power"]
        for op in binary_ops:
            _, operand_count = OPERATIONS[op]
            assert operand_count == 2, f"{op} should require 2 operands"

    def test_operations_dict_unary_operations_have_1_operand(self):
        """Test that unary operations require 1 operand."""
        unary_ops = ["factorial", "square", "cube", "square_root", "cube_root", "log10", "natural_log"]
        for op in unary_ops:
            _, operand_count = OPERATIONS[op]
            assert operand_count == 1, f"{op} should require 1 operand"

    def test_operations_dict_maps_to_calculator_methods(self):
        """Test that all operation names map to valid Calculator method names."""
        calc = Calculator()
        for op_name, (method_name, _) in OPERATIONS.items():
            assert hasattr(calc, method_name), f"Calculator missing method {method_name} for operation {op_name}"

    def test_operations_dict_values_are_tuples_with_2_elements(self):
        """Test that all values are (method_name, operand_count) tuples."""
        for op_name, value in OPERATIONS.items():
            assert isinstance(value, tuple)
            assert len(value) == 2
            assert isinstance(value[0], str)
            assert isinstance(value[1], int)


# ============================================================================
# GET_OPERANDS TESTS
# ============================================================================


class TestGetOperands:
    """Test suite for get_operands function."""

    @patch("builtins.input", return_value="5")
    def test_get_operands_unary_operation_single_value(self, mock_input):
        """Test get_operands for a unary operation (square) returns single operand."""
        result = get_operands("square")
        assert result == [5]
        assert len(result) == 1

    @patch("builtins.input", side_effect=["5", "3"])
    def test_get_operands_binary_operation_two_values(self, mock_input):
        """Test get_operands for a binary operation (add) returns two operands."""
        result = get_operands("add")
        assert result == [5, 3]
        assert len(result) == 2

    @patch("builtins.input", side_effect=["10", "2"])
    def test_get_operands_divide_operation(self, mock_input):
        """Test get_operands for divide operation."""
        result = get_operands("divide")
        assert result == [10, 2]

    @patch("builtins.input", return_value="5")
    def test_get_operands_factorial_operation(self, mock_input):
        """Test get_operands for factorial operation (unary)."""
        result = get_operands("factorial")
        assert result == [5]

    @patch("builtins.input", return_value="3.14")
    def test_get_operands_accepts_floats(self, mock_input):
        """Test that get_operands correctly parses float operands."""
        result = get_operands("square")
        assert result == [pytest.approx(3.14)]

    @patch("builtins.input", return_value="-5")
    def test_get_operands_accepts_negative_numbers(self, mock_input):
        """Test that get_operands correctly parses negative operands."""
        result = get_operands("square")
        assert result == [-5]

    @patch("builtins.input", return_value="0")
    def test_get_operands_accepts_zero(self, mock_input):
        """Test that get_operands correctly parses zero."""
        result = get_operands("square")
        assert result == [0]

    @patch("builtins.input", side_effect=["abc", "5"])
    @patch("builtins.print")
    def test_get_operands_retries_on_invalid_input(self, mock_print, mock_input):
        """Test that get_operands retries when invalid input is given."""
        result = get_operands("square")
        assert result == [5]
        # Verify input was called twice (once for invalid, once for valid)
        assert mock_input.call_count == 2
        # Verify error message was printed
        mock_print.assert_called()
        print_calls = [str(call) for call in mock_print.call_args_list]
        error_printed = any("Error" in str(call) for call in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["", "not_a_number", "5"])
    @patch("builtins.print")
    def test_get_operands_retries_multiple_times(self, mock_print, mock_input):
        """Test that get_operands retries multiple times until valid input."""
        result = get_operands("square")
        assert result == [5]
        assert mock_input.call_count == 3

    @patch("builtins.input", side_effect=["5", "abc", "3"])
    @patch("builtins.print")
    def test_get_operands_binary_retry_on_second_operand(self, mock_print, mock_input):
        """Test retry behavior when second operand is invalid."""
        result = get_operands("add")
        assert result == [5, 3]
        assert mock_input.call_count == 3

    @patch("builtins.input", side_effect=["1", "2", "3"])
    def test_get_operands_power_operation(self, mock_input):
        """Test get_operands for power operation (binary)."""
        result = get_operands("power")
        assert result == [1, 2]
        assert len(result) == 2

    @patch("builtins.input", return_value="100")
    def test_get_operands_large_number(self, mock_input):
        """Test get_operands with large numbers."""
        result = get_operands("square")
        assert result == [100]

    @patch("builtins.input", return_value="0.0001")
    def test_get_operands_small_float(self, mock_input):
        """Test get_operands with very small float."""
        result = get_operands("square")
        assert result == [pytest.approx(0.0001)]


# ============================================================================
# EXECUTE_OPERATION TESTS
# ============================================================================


class TestExecuteOperation:
    """Test suite for execute_operation function."""

    def test_execute_operation_add(self):
        """Test execute_operation for add with valid operands."""
        calc = Calculator()
        result = execute_operation(calc, "add", [5, 3])
        assert result == 8

    def test_execute_operation_subtract(self):
        """Test execute_operation for subtract."""
        calc = Calculator()
        result = execute_operation(calc, "subtract", [10, 3])
        assert result == 7

    def test_execute_operation_multiply(self):
        """Test execute_operation for multiply."""
        calc = Calculator()
        result = execute_operation(calc, "multiply", [4, 5])
        assert result == 20

    def test_execute_operation_divide(self):
        """Test execute_operation for divide."""
        calc = Calculator()
        result = execute_operation(calc, "divide", [10, 2])
        assert result == 5.0

    def test_execute_operation_divide_by_zero_returns_error_string(self):
        """Test that divide by zero returns error string, not exception."""
        calc = Calculator()
        result = execute_operation(calc, "divide", [10, 0])
        assert isinstance(result, str)
        assert "Error" in result
        assert "Division by zero" in result

    def test_execute_operation_factorial(self):
        """Test execute_operation for factorial."""
        calc = Calculator()
        result = execute_operation(calc, "factorial", [5])
        assert result == 120

    def test_execute_operation_square(self):
        """Test execute_operation for square."""
        calc = Calculator()
        result = execute_operation(calc, "square", [4])
        assert result == 16

    def test_execute_operation_cube(self):
        """Test execute_operation for cube."""
        calc = Calculator()
        result = execute_operation(calc, "cube", [3])
        assert result == 27

    def test_execute_operation_square_root(self):
        """Test execute_operation for square_root."""
        calc = Calculator()
        result = execute_operation(calc, "square_root", [16])
        assert result == pytest.approx(4.0)

    def test_execute_operation_cube_root(self):
        """Test execute_operation for cube_root."""
        calc = Calculator()
        result = execute_operation(calc, "cube_root", [8])
        assert result == pytest.approx(2.0)

    def test_execute_operation_power(self):
        """Test execute_operation for power."""
        calc = Calculator()
        result = execute_operation(calc, "power", [2, 3])
        assert result == pytest.approx(8.0)

    def test_execute_operation_log10(self):
        """Test execute_operation for log10."""
        calc = Calculator()
        result = execute_operation(calc, "log10", [100])
        assert result == pytest.approx(2.0)

    def test_execute_operation_natural_log(self):
        """Test execute_operation for natural_log."""
        calc = Calculator()
        result = execute_operation(calc, "natural_log", [1])
        assert result == pytest.approx(0.0)

    def test_execute_operation_factorial_negative_returns_error(self):
        """Test that factorial with negative input returns error string."""
        calc = Calculator()
        result = execute_operation(calc, "factorial", [-5])
        assert isinstance(result, str)
        assert "Error" in result

    def test_execute_operation_square_root_negative_returns_error(self):
        """Test that square_root with negative input returns error string."""
        calc = Calculator()
        result = execute_operation(calc, "square_root", [-4])
        assert isinstance(result, str)
        assert "Error" in result

    def test_execute_operation_log10_zero_returns_error(self):
        """Test that log10 with zero returns error string."""
        calc = Calculator()
        result = execute_operation(calc, "log10", [0])
        assert isinstance(result, str)
        assert "Error" in result

    def test_execute_operation_log10_negative_returns_error(self):
        """Test that log10 with negative input returns error string."""
        calc = Calculator()
        result = execute_operation(calc, "log10", [-5])
        assert isinstance(result, str)
        assert "Error" in result

    def test_execute_operation_natural_log_negative_returns_error(self):
        """Test that natural_log with negative input returns error string."""
        calc = Calculator()
        result = execute_operation(calc, "natural_log", [-5])
        assert isinstance(result, str)
        assert "Error" in result

    def test_execute_operation_with_floats(self):
        """Test execute_operation with floating-point operands."""
        calc = Calculator()
        result = execute_operation(calc, "add", [3.5, 2.5])
        assert result == pytest.approx(6.0)

    def test_execute_operation_with_negative_operands(self):
        """Test execute_operation with negative operands."""
        calc = Calculator()
        result = execute_operation(calc, "add", [-5, 3])
        assert result == -2

    def test_execute_operation_cube_with_negative(self):
        """Test cube operation with negative number."""
        calc = Calculator()
        result = execute_operation(calc, "cube", [-3])
        assert result == -27

    def test_execute_operation_cube_root_with_negative(self):
        """Test cube_root operation with negative number."""
        calc = Calculator()
        result = execute_operation(calc, "cube_root", [-8])
        assert result == pytest.approx(-2.0)

    def test_execute_operation_zero_operand(self):
        """Test operations with zero as operand."""
        calc = Calculator()
        result = execute_operation(calc, "square", [0])
        assert result == 0

    def test_execute_operation_factory_with_zero(self):
        """Test factorial with zero."""
        calc = Calculator()
        result = execute_operation(calc, "factorial", [0])
        assert result == 1

    def test_execute_operation_power_zero_exponent(self):
        """Test power with exponent zero."""
        calc = Calculator()
        result = execute_operation(calc, "power", [5, 0])
        assert result == pytest.approx(1.0)


# ============================================================================
# FORMAT_RESULT TESTS
# ============================================================================


class TestFormatResult:
    """Test suite for format_result function."""

    def test_format_result_integer(self):
        """Test formatting an integer result."""
        result = format_result(8)
        assert result == "8"
        assert isinstance(result, str)

    def test_format_result_float(self):
        """Test formatting a float result."""
        result = format_result(3.14)
        assert result == "3.14"

    def test_format_result_zero(self):
        """Test formatting zero."""
        result = format_result(0)
        assert result == "0"

    def test_format_result_negative_integer(self):
        """Test formatting a negative integer."""
        result = format_result(-10)
        assert result == "-10"

    def test_format_result_negative_float(self):
        """Test formatting a negative float."""
        result = format_result(-3.14)
        assert result == "-3.14"

    def test_format_result_error_string(self):
        """Test formatting an error message string."""
        error_msg = "Error: Division by zero is not allowed."
        result = format_result(error_msg)
        assert result == error_msg

    def test_format_result_large_integer(self):
        """Test formatting a large integer."""
        result = format_result(999999999)
        assert result == "999999999"

    def test_format_result_scientific_notation_float(self):
        """Test formatting a float in scientific notation."""
        result = format_result(1.23e-5)
        assert "1.23e-05" in result or "1.23e-5" in result

    def test_format_result_very_small_float(self):
        """Test formatting a very small float."""
        result = format_result(0.0000001)
        assert isinstance(result, str)
        assert "0" in result

    def test_format_result_returns_string_type(self):
        """Test that format_result always returns a string."""
        assert isinstance(format_result(42), str)
        assert isinstance(format_result(3.14), str)
        assert isinstance(format_result("error"), str)


# ============================================================================
# RUN_INTERACTIVE TESTS
# ============================================================================


class TestRunInteractive:
    """Test suite for run_interactive function."""

    @patch("builtins.input", side_effect=["quit"])
    @patch("builtins.print")
    def test_run_interactive_quit_immediately(self, mock_print, mock_input):
        """Test that run_interactive exits with 'quit' command."""
        run_interactive()
        # Verify "Bye!" was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        bye_printed = any("Bye!" in str(call) for call in print_calls)
        assert bye_printed

    @patch("builtins.input", side_effect=["exit"])
    @patch("builtins.print")
    def test_run_interactive_exit_immediately(self, mock_print, mock_input):
        """Test that run_interactive exits with 'exit' command."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        bye_printed = any("Bye!" in str(call) for call in print_calls)
        assert bye_printed

    @patch("builtins.input", side_effect=["add", "5", "3", "quit"])
    @patch("builtins.print")
    def test_run_interactive_single_add_operation(self, mock_print, mock_input):
        """Test single add operation followed by quit."""
        run_interactive()
        # Verify result was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        result_printed = any("Result" in str(call) or "8" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["square", "4", "quit"])
    @patch("builtins.print")
    def test_run_interactive_single_unary_operation(self, mock_print, mock_input):
        """Test single unary operation (square)."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        result_printed = any("Result" in str(call) or "16" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["invalid_op", "quit"])
    @patch("builtins.print")
    def test_run_interactive_unknown_operation_error(self, mock_print, mock_input):
        """Test that unknown operation prints error and continues."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Error message should be printed
        error_printed = any("Unknown operation" in str(call) for call in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["unknown", "quit"])
    @patch("builtins.print")
    def test_run_interactive_unknown_operation_does_not_crash(self, mock_print, mock_input):
        """Test that unknown operation does not crash the program."""
        # This should not raise any exception
        run_interactive()
        assert mock_print.called

    @patch("builtins.input", side_effect=["add", "10", "5", "multiply", "3", "4", "quit"])
    @patch("builtins.print")
    def test_run_interactive_multiple_operations(self, mock_print, mock_input):
        """Test multiple operations in sequence."""
        run_interactive()
        # Should have multiple Result outputs
        print_calls = [str(call) for call in mock_print.call_args_list]
        result_count = sum(1 for call in print_calls if "Result" in str(call))
        assert result_count >= 2

    @patch("builtins.input", side_effect=["divide", "10", "0", "quit"])
    @patch("builtins.print")
    def test_run_interactive_division_by_zero(self, mock_print, mock_input):
        """Test that division by zero prints error message and continues."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should print error message
        error_printed = any("Error" in str(call) or "Division by zero" in str(call) for call in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["QUIT"])
    @patch("builtins.print")
    def test_run_interactive_quit_case_insensitive(self, mock_print, mock_input):
        """Test that quit is case-insensitive."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        bye_printed = any("Bye!" in str(call) for call in print_calls)
        assert bye_printed

    @patch("builtins.input", side_effect=["EXIT"])
    @patch("builtins.print")
    def test_run_interactive_exit_case_insensitive(self, mock_print, mock_input):
        """Test that exit is case-insensitive."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        bye_printed = any("Bye!" in str(call) for call in print_calls)
        assert bye_printed

    @patch("builtins.input", side_effect=["Quit"])
    @patch("builtins.print")
    def test_run_interactive_quit_mixed_case(self, mock_print, mock_input):
        """Test that quit works with mixed case."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        bye_printed = any("Bye!" in str(call) for call in print_calls)
        assert bye_printed

    @patch("builtins.input", side_effect=["factorial", "5", "quit"])
    @patch("builtins.print")
    def test_run_interactive_factorial_operation(self, mock_print, mock_input):
        """Test factorial operation in interactive mode."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # 5! = 120
        result_printed = any("Result" in str(call) or "120" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["log10", "100", "quit"])
    @patch("builtins.print")
    def test_run_interactive_log10_operation(self, mock_print, mock_input):
        """Test log10 operation in interactive mode."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # log10(100) = 2
        result_printed = any("Result" in str(call) or "2" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["add", "abc", "5", "3", "quit"])
    @patch("builtins.print")
    def test_run_interactive_retry_invalid_operand(self, mock_print, mock_input):
        """Test that invalid operand is retried."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should eventually succeed and print result
        result_printed = any("Result" in str(call) or "8" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["", "unknown", "add", "2", "3", "quit"])
    @patch("builtins.print")
    def test_run_interactive_multiple_invalid_operations(self, mock_print, mock_input):
        """Test multiple invalid operations before valid one."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should eventually succeed
        result_printed = any("Result" in str(call) or "5" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["power", "2", "10", "quit"])
    @patch("builtins.print")
    def test_run_interactive_power_operation(self, mock_print, mock_input):
        """Test power operation (2^10 = 1024)."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        result_printed = any("Result" in str(call) or "1024" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["add", "1.5", "2.5", "quit"])
    @patch("builtins.print")
    def test_run_interactive_float_operands(self, mock_print, mock_input):
        """Test operations with float operands."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # 1.5 + 2.5 = 4
        result_printed = any("Result" in str(call) or "4" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["subtract", "10", "15", "quit"])
    @patch("builtins.print")
    def test_run_interactive_negative_result(self, mock_print, mock_input):
        """Test operation that results in negative number."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # 10 - 15 = -5
        result_printed = any("Result" in str(call) or "-5" in str(call) for call in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["square_root", "-4", "quit"])
    @patch("builtins.print")
    def test_run_interactive_square_root_negative(self, mock_print, mock_input):
        """Test square_root with negative number (should error gracefully)."""
        run_interactive()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should print error
        error_printed = any("Error" in str(call) for call in print_calls)
        assert error_printed
