"""Test suite for the formatter module."""

import pytest

from src.formatter import (
    format_menu_header,
    format_quit_instruction,
    format_history_header,
    format_operation_error,
    format_result,
    format_error,
)


class TestFormatMenuHeader:
    """Test suite for format_menu_header() function."""

    def test_format_menu_header_single_operation(self):
        """Should format header with single operation."""
        result = format_menu_header(["add"])
        assert "\nAvailable operations:" in result
        assert "1. add" in result

    @pytest.mark.parametrize("operations,expected_lines", [
        (["add", "subtract"], ["1. add", "2. subtract"]),
        (["add", "subtract", "multiply"], ["1. add", "2. subtract", "3. multiply"]),
        (["square", "cube"], ["1. square", "2. cube"]),
    ])
    def test_format_menu_header_multiple_operations(self, operations, expected_lines):
        """Should format header with multiple operations and correct numbering."""
        result = format_menu_header(operations)
        assert "\nAvailable operations:" in result
        for expected in expected_lines:
            assert expected in result

    def test_format_menu_header_empty_list(self):
        """Should handle empty operation list."""
        result = format_menu_header([])
        assert "\nAvailable operations:" in result
        # Should just have the header, no operation lines
        assert result == "\nAvailable operations:"

    def test_format_menu_header_many_operations(self):
        """Should handle many operations with correct numbering."""
        ops = ["op" + str(i) for i in range(1, 13)]  # 12 operations
        result = format_menu_header(ops)
        assert "12. op12" in result
        assert "1. op1" in result

    def test_format_menu_header_returns_string(self):
        """Should always return a string."""
        result = format_menu_header(["add"])
        assert isinstance(result, str)

    def test_format_menu_header_special_characters(self):
        """Should handle operation names with underscores and numbers."""
        result = format_menu_header(["square_root", "natural_logarithm"])
        assert "square_root" in result
        assert "natural_logarithm" in result

    def test_format_menu_header_starts_with_newline(self):
        """Output should start with a newline."""
        result = format_menu_header(["add"])
        assert result.startswith("\n")


class TestFormatQuitInstruction:
    """Test suite for format_quit_instruction() function."""

    def test_format_quit_instruction_contains_quit(self):
        """Should mention 'quit' option."""
        result = format_quit_instruction()
        assert "quit" in result.lower()

    def test_format_quit_instruction_contains_exit(self):
        """Should mention 'exit' option."""
        result = format_quit_instruction()
        assert "exit" in result.lower()

    def test_format_quit_instruction_contains_q(self):
        """Should mention 'q' shortcut."""
        result = format_quit_instruction()
        assert "'q'" in result

    def test_format_quit_instruction_contains_history(self):
        """Should mention history option."""
        result = format_quit_instruction()
        assert "history" in result.lower()

    def test_format_quit_instruction_contains_h(self):
        """Should mention 'h' shortcut for history."""
        result = format_quit_instruction()
        assert "'h'" in result

    def test_format_quit_instruction_returns_string(self):
        """Should return a string."""
        result = format_quit_instruction()
        assert isinstance(result, str)

    def test_format_quit_instruction_multiline(self):
        """Should contain multiple lines."""
        result = format_quit_instruction()
        assert "\n" in result

    def test_format_quit_instruction_indented(self):
        """Lines should be indented with spaces."""
        result = format_quit_instruction()
        assert "  (" in result


class TestFormatHistoryHeader:
    """Test suite for format_history_header() function."""

    def test_format_history_header_contains_operation_history(self):
        """Should contain 'Operation history' text."""
        result = format_history_header()
        assert "Operation history" in result

    def test_format_history_header_returns_string(self):
        """Should return a string."""
        result = format_history_header()
        assert isinstance(result, str)

    def test_format_history_header_starts_with_newline(self):
        """Output should start with a newline."""
        result = format_history_header()
        assert result.startswith("\n")

    def test_format_history_header_exact_format(self):
        """Should have exact format with leading newline."""
        result = format_history_header()
        assert result == "\nOperation history:"


class TestFormatOperationError:
    """Test suite for format_operation_error() function."""

    def test_format_operation_error_single_operation(self):
        """Should format error for single operation."""
        result = format_operation_error("add, subtract")
        assert "Invalid operation" in result
        assert "Available operations: add, subtract" in result

    def test_format_operation_error_empty_string(self):
        """Should handle empty operation string."""
        result = format_operation_error("")
        assert "Invalid operation" in result
        assert "Available operations:" in result

    def test_format_operation_error_multiple_operations(self):
        """Should include the operation list as provided."""
        ops = "add, subtract, multiply, divide"
        result = format_operation_error(ops)
        assert ops in result

    def test_format_operation_error_returns_string(self):
        """Should return a string."""
        result = format_operation_error("add")
        assert isinstance(result, str)

    def test_format_operation_error_long_operation_list(self):
        """Should handle long operation lists."""
        long_ops = ", ".join([f"op{i}" for i in range(1, 20)])
        result = format_operation_error(long_ops)
        assert long_ops in result

    def test_format_operation_error_preserves_operation_string(self):
        """Should preserve the exact operation string provided."""
        op_str = "add, subtract, multiply"
        result = format_operation_error(op_str)
        assert result == f"Invalid operation. Available operations: {op_str}"


class TestFormatResult:
    """Test suite for format_result() function."""

    def test_format_result_simple_integer_result(self):
        """Should format result with integer result."""
        result = format_result("add", [2.0, 3.0], 5)
        assert "Result: 5" in result

    @pytest.mark.parametrize("op_name,operands,result_val", [
        ("add", [2.0, 3.0], 5),
        ("subtract", [5.0, 2.0], 3),
        ("multiply", [4.0, 2.0], 8),
        ("divide", [10.0, 2.0], 5.0),
        ("square", [3.0], 9.0),
    ])
    def test_format_result_various_operations(self, op_name, operands, result_val):
        """Should format result correctly for various operations."""
        result = format_result(op_name, operands, result_val)
        assert "Result:" in result
        assert str(result_val) in result

    def test_format_result_float_result(self):
        """Should format result with float result."""
        result = format_result("divide", [7.0, 2.0], 3.5)
        assert "Result: 3.5" in result

    def test_format_result_zero_result(self):
        """Should handle zero result."""
        result = format_result("subtract", [5.0, 5.0], 0)
        assert "Result: 0" in result

    def test_format_result_negative_result(self):
        """Should handle negative result."""
        result = format_result("subtract", [2.0, 5.0], -3)
        assert "Result: -3" in result

    def test_format_result_very_large_result(self):
        """Should handle very large result."""
        result = format_result("power", [2.0, 100.0], 2**100)
        assert "Result:" in result

    def test_format_result_very_small_result(self):
        """Should handle very small float result."""
        result = format_result("divide", [1.0, 1e10], 1e-10)
        assert "Result:" in result

    def test_format_result_returns_string(self):
        """Should return a string."""
        result = format_result("add", [2.0, 3.0], 5)
        assert isinstance(result, str)

    def test_format_result_starts_with_spaces(self):
        """Output should be indented with leading spaces."""
        result = format_result("add", [2.0, 3.0], 5)
        assert result.startswith("  ")

    def test_format_result_ignores_operands_and_op_name(self):
        """Should only include result in output, not operands or op_name."""
        result = format_result("add", [2.0, 3.0], 5)
        # The function only cares about the result, not the operands or op_name
        assert "add" not in result or "add" not in result.lower() or "add" in "Result" or "add" in "5"

    def test_format_result_special_float_values(self):
        """Should handle special float values like infinity."""
        result = format_result("divide", [1.0, 0.0], float('inf'))
        assert "Result:" in result
        assert "inf" in str(result).lower()


class TestFormatError:
    """Test suite for format_error() function."""

    def test_format_error_simple_message(self):
        """Should format simple error message."""
        result = format_error("division by zero")
        assert "Error: division by zero" in result

    @pytest.mark.parametrize("error_msg", [
        "division by zero",
        "invalid input",
        "out of range",
        "domain error",
        "unknown error",
    ])
    def test_format_error_various_messages(self, error_msg):
        """Should format various error messages correctly."""
        result = format_error(error_msg)
        assert f"Error: {error_msg}" in result

    def test_format_error_empty_string(self):
        """Should handle empty error message."""
        result = format_error("")
        assert "Error:" in result

    def test_format_error_long_message(self):
        """Should handle long error messages."""
        long_msg = "a" * 100
        result = format_error(long_msg)
        assert long_msg in result

    def test_format_error_returns_string(self):
        """Should return a string."""
        result = format_error("test error")
        assert isinstance(result, str)

    def test_format_error_starts_with_spaces(self):
        """Output should be indented with leading spaces."""
        result = format_error("test")
        assert result.startswith("  ")

    def test_format_error_preserves_message(self):
        """Should preserve exact error message."""
        msg = "specific error message"
        result = format_error(msg)
        assert result == f"  Error: {msg}"

    def test_format_error_special_characters(self):
        """Should handle error messages with special characters."""
        result = format_error("error: x must be >= 0")
        assert ">=" in result

    def test_format_error_multiline_message(self):
        """Should handle multiline error messages."""
        msg = "line1\nline2"
        result = format_error(msg)
        assert "line1\nline2" in result
