"""Unit tests for InputHandler class."""

import pytest
from unittest.mock import patch
from src.io_handler import InputHandler


class TestGetOperationChoice:
    """Test suite for InputHandler.get_operation_choice() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
            "multiply": "Multiplication (a * b)",
        }

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_valid_selection(self, mock_input, handler, available_ops, capsys):
        """Test that a valid operation key is returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        captured = capsys.readouterr()
        assert "Available operations:" in captured.out
        assert "add: Addition (a + b)" in captured.out

    @patch("builtins.input", side_effect=["invalid", "subtract"])
    def test_get_operation_choice_invalid_then_valid(self, mock_input, handler, available_ops, capsys):
        """Test that invalid input triggers re-prompt, then valid key is accepted."""
        result = handler.get_operation_choice(available_ops)
        assert result == "subtract"
        captured = capsys.readouterr()
        assert "Invalid choice 'invalid'" in captured.out

    @patch("builtins.input", return_value="exit")
    def test_get_operation_choice_exit_returns_exit(self, mock_input, handler, available_ops, capsys):
        """Test that 'exit' is returned as a special sentinel."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="quit")
    def test_get_operation_choice_quit_returns_quit(self, mock_input, handler, available_ops, capsys):
        """Test that 'quit' is returned as a special sentinel."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", return_value="EXIT")
    def test_get_operation_choice_case_insensitive_exit(self, mock_input, handler, available_ops, capsys):
        """Test that 'EXIT' (uppercase) is converted to lowercase and returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="QUIT")
    def test_get_operation_choice_case_insensitive_quit(self, mock_input, handler, available_ops, capsys):
        """Test that 'QUIT' (uppercase) is converted to lowercase and returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", side_effect=["", "  ", "add"])
    def test_get_operation_choice_multiple_invalid_inputs(self, mock_input, handler, available_ops, capsys):
        """Test multiple invalid inputs before a valid one."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        captured = capsys.readouterr()
        # Should have printed invalid choice messages for each invalid input
        assert captured.out.count("Invalid choice") == 2

    @patch("builtins.input", return_value=" multiply ")
    def test_get_operation_choice_with_whitespace(self, mock_input, handler, available_ops, capsys):
        """Test that input with surrounding whitespace is stripped."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"

    @patch("builtins.input", return_value="MuLtIpLy")
    def test_get_operation_choice_mixed_case_valid_selection(self, mock_input, handler, available_ops, capsys):
        """Test that mixed case input is converted to lowercase and validated."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"


class TestGetOperand:
    """Test suite for InputHandler.get_operand() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @patch("builtins.input", return_value="5.5")
    def test_get_operand_valid_float(self, mock_input, handler):
        """Test that a valid float string is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 5.5
        assert isinstance(result, float)

    @patch("builtins.input", return_value="42")
    def test_get_operand_valid_integer(self, mock_input, handler):
        """Test that an integer string is parsed as float."""
        result = handler.get_operand("Enter value: ")
        assert result == 42.0
        assert isinstance(result, float)

    @patch("builtins.input", return_value="-3.14")
    def test_get_operand_negative_float(self, mock_input, handler):
        """Test that negative floats are parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == -3.14

    @patch("builtins.input", return_value=" 7.5 ")
    def test_get_operand_with_whitespace(self, mock_input, handler):
        """Test that input with whitespace is stripped before parsing."""
        result = handler.get_operand("Enter value: ")
        assert result == 7.5

    @patch("builtins.input", return_value="0")
    def test_get_operand_zero(self, mock_input, handler):
        """Test that zero is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 0.0

    @patch("builtins.input", return_value="1e10")
    def test_get_operand_scientific_notation(self, mock_input, handler):
        """Test that scientific notation is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 1e10

    @patch("builtins.input", return_value="abc")
    def test_get_operand_invalid_input_raises_valueerror(self, mock_input, handler):
        """Test that non-numeric input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="12.34.56")
    def test_get_operand_invalid_format_raises_valueerror(self, mock_input, handler):
        """Test that malformed numeric input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="")
    def test_get_operand_empty_string_raises_valueerror(self, mock_input, handler):
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="inf")
    def test_get_operand_infinity(self, mock_input, handler):
        """Test that 'inf' is parsed as infinity."""
        result = handler.get_operand("Enter value: ")
        assert result == float("inf")


class TestDisplayResult:
    """Test suite for InputHandler.display_result() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    def test_display_result_binary_operation(self, handler, capsys):
        """Test result display for a binary operation."""
        handler.display_result("add", [5, 3], 8)
        captured = capsys.readouterr()
        assert "Result of add(5, 3) = 8" in captured.out

    def test_display_result_unary_operation(self, handler, capsys):
        """Test result display for a unary operation."""
        handler.display_result("square", [5], 25)
        captured = capsys.readouterr()
        assert "Result of square(5) = 25" in captured.out

    def test_display_result_float_operands(self, handler, capsys):
        """Test result display with float operands."""
        handler.display_result("divide", [10.0, 2.5], 4.0)
        captured = capsys.readouterr()
        assert "Result of divide(10.0, 2.5) = 4.0" in captured.out

    def test_display_result_float_result(self, handler, capsys):
        """Test result display with float result."""
        handler.display_result("divide", [5, 2], 2.5)
        captured = capsys.readouterr()
        assert "Result of divide(5, 2) = 2.5" in captured.out

    def test_display_result_negative_operands(self, handler, capsys):
        """Test result display with negative operands."""
        handler.display_result("multiply", [-3, 4], -12)
        captured = capsys.readouterr()
        assert "Result of multiply(-3, 4) = -12" in captured.out

    def test_display_result_zero_result(self, handler, capsys):
        """Test result display with zero result."""
        handler.display_result("subtract", [5, 5], 0)
        captured = capsys.readouterr()
        assert "Result of subtract(5, 5) = 0" in captured.out

    def test_display_result_multiple_operands(self, handler, capsys):
        """Test result display format with multiple operands."""
        # Even though the current implementation expects binary/unary,
        # verify it handles lists of any size
        handler.display_result("operation", [1, 2, 3], 6)
        captured = capsys.readouterr()
        assert "Result of operation(1, 2, 3) = 6" in captured.out


class TestDisplayError:
    """Test suite for InputHandler.display_error() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    def test_display_error_simple_message(self, handler, capsys):
        """Test error display with a simple message."""
        handler.display_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Error: Something went wrong" in captured.out

    def test_display_error_division_by_zero(self, handler, capsys):
        """Test error display for division by zero."""
        handler.display_error("Division by zero is not allowed.")
        captured = capsys.readouterr()
        assert "Error: Division by zero is not allowed." in captured.out

    def test_display_error_invalid_operation(self, handler, capsys):
        """Test error display for invalid operation."""
        handler.display_error("Unknown operation: 'unknown'")
        captured = capsys.readouterr()
        assert "Error: Unknown operation: 'unknown'" in captured.out

    def test_display_error_empty_message(self, handler, capsys):
        """Test error display with empty message."""
        handler.display_error("")
        captured = capsys.readouterr()
        assert "Error: " in captured.out

    def test_display_error_special_characters(self, handler, capsys):
        """Test error display with special characters."""
        handler.display_error("Invalid input: expect 5.5 or 'exit'")
        captured = capsys.readouterr()
        assert "Error: Invalid input: expect 5.5 or 'exit'" in captured.out
