"""Integration tests for interactive calculator main() function."""

import pytest
from unittest.mock import patch
from src.__main__ import main


class TestInteractiveSessionBasic:
    """Test suite for basic interactive session flows."""

    @patch("builtins.input", side_effect=["exit"])
    def test_exit_immediately(self, mock_input, capsys):
        """Test that 'exit' command exits the main loop."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["quit"])
    def test_quit_immediately(self, mock_input, capsys):
        """Test that 'quit' command exits the main loop."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["exit"])
    def test_welcome_message_displayed(self, mock_input, capsys):
        """Test that welcome message is displayed at start."""
        main()
        captured = capsys.readouterr()
        assert "Welcome to the Calculator" in captured.out


class TestSingleOperationFlow:
    """Test suite for single operation execution."""

    @patch("builtins.input", side_effect=["add", "5", "3", "exit"])
    def test_single_binary_operation_flow(self, mock_input, capsys):
        """Test executing a single binary operation then exiting."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["square", "5", "exit"])
    def test_single_unary_operation_flow(self, mock_input, capsys):
        """Test executing a single unary operation then exiting."""
        main()
        captured = capsys.readouterr()
        assert "Result of Square (x^2)(5.0) = 25.0" in captured.out

    @patch("builtins.input", side_effect=["subtract", "10", "3", "exit"])
    def test_subtract_operation_flow(self, mock_input, capsys):
        """Test subtract operation."""
        main()
        captured = capsys.readouterr()
        assert "Result of Subtraction (a - b)(10.0, 3.0) = 7.0" in captured.out

    @patch("builtins.input", side_effect=["multiply", "4", "5", "exit"])
    def test_multiply_operation_flow(self, mock_input, capsys):
        """Test multiply operation."""
        main()
        captured = capsys.readouterr()
        assert "Result of Multiplication (a * b)(4.0, 5.0) = 20.0" in captured.out

    @patch("builtins.input", side_effect=["divide", "10", "2", "exit"])
    def test_divide_operation_flow(self, mock_input, capsys):
        """Test divide operation."""
        main()
        captured = capsys.readouterr()
        assert "Result of Division (a / b)(10.0, 2.0) = 5.0" in captured.out

    @patch("builtins.input", side_effect=["cube", "3", "exit"])
    def test_cube_operation_flow(self, mock_input, capsys):
        """Test cube unary operation."""
        main()
        captured = capsys.readouterr()
        assert "Result of Cube (x^3)(3.0) = 27.0" in captured.out


class TestMultipleOperations:
    """Test suite for multiple operations in sequence."""

    @patch("builtins.input", side_effect=["add", "5", "3", "multiply", "2", "4", "exit"])
    def test_multiple_operations_in_sequence(self, mock_input, capsys):
        """Test executing multiple operations in sequence."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Result of Multiplication (a * b)(2.0, 4.0) = 8.0" in captured.out

    @patch("builtins.input", side_effect=[
        "square", "3",
        "cube", "2",
        "square_root", "16",
        "exit"
    ])
    def test_three_unary_operations_sequence(self, mock_input, capsys):
        """Test executing three unary operations in sequence."""
        main()
        captured = capsys.readouterr()
        assert "Result of Square (x^2)(3.0) = 9.0" in captured.out
        assert "Result of Cube (x^3)(2.0) = 8.0" in captured.out
        assert "Result of Square root (√x)(16.0) = 4.0" in captured.out


class TestErrorHandling:
    """Test suite for error handling in interactive session."""

    @patch("builtins.input", side_effect=["divide", "5", "0", "exit"])
    def test_handles_division_by_zero(self, mock_input, capsys):
        """Test that division by zero error is caught and displayed."""
        main()
        captured = capsys.readouterr()
        assert "Error: Division by zero is not allowed." in captured.out
        # Loop should continue after error
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["add", "abc", "5", "3", "exit"])
    def test_handles_invalid_operand_input(self, mock_input, capsys):
        """Test that invalid operand input (non-numeric) triggers error and retries."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        # The error message may vary, but should contain something about the invalid input
        # Loop should continue after retry
        assert "Goodbye!" in captured.out
        # Should have executed add(5, 3) = 8
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out

    @patch("builtins.input", side_effect=["square_root", "-1", "exit"])
    def test_handles_math_domain_error(self, mock_input, capsys):
        """Test that math domain errors (like sqrt of negative) are caught."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    @patch("builtins.input", side_effect=["log", "0", "exit"])
    def test_handles_log_of_zero(self, mock_input, capsys):
        """Test that log(0) error is caught."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    @patch("builtins.input", side_effect=["factorial", "5.5", "exit"])
    def test_handles_factorial_float_input(self, mock_input, capsys):
        """Test that factorial with float input is cast to int."""
        main()
        captured = capsys.readouterr()
        # 5! = 120
        assert "Result of Factorial (n!)(5) = 120" in captured.out


class TestInvalidOperationSelection:
    """Test suite for handling invalid operation selections."""

    @patch("builtins.input", side_effect=["invalid", "add", "2", "3", "exit"])
    def test_invalid_operation_then_valid(self, mock_input, capsys):
        """Test that invalid operation key triggers re-prompt."""
        main()
        captured = capsys.readouterr()
        # Should show invalid choice message
        assert "Invalid choice 'invalid'" in captured.out
        # Should still execute the valid operation
        assert "Result of Addition (a + b)(2.0, 3.0) = 5.0" in captured.out

    @patch("builtins.input", side_effect=["", "xyz", "add", "1", "1", "exit"])
    def test_multiple_invalid_selections_then_valid(self, mock_input, capsys):
        """Test multiple invalid selections before a valid one."""
        main()
        captured = capsys.readouterr()
        assert "Invalid choice ''" in captured.out
        assert "Invalid choice 'xyz'" in captured.out
        assert "Result of Addition (a + b)(1.0, 1.0) = 2.0" in captured.out


class TestKeyboardInterrupt:
    """Test suite for KeyboardInterrupt handling."""

    @patch("builtins.input", side_effect=KeyboardInterrupt())
    def test_keyboard_interrupt_exits_cleanly(self, mock_input, capsys):
        """Test that KeyboardInterrupt (Ctrl+C) exits cleanly."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["add", KeyboardInterrupt()])
    def test_keyboard_interrupt_after_operation_selection(self, mock_input, capsys):
        """Test KeyboardInterrupt after operation selection."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out


class TestFloatingPointOperations:
    """Test suite for floating-point operations."""

    @patch("builtins.input", side_effect=["add", "1.5", "2.5", "exit"])
    def test_add_floating_point_numbers(self, mock_input, capsys):
        """Test addition with floating-point operands."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(1.5, 2.5) = 4.0" in captured.out

    @patch("builtins.input", side_effect=["divide", "5", "2", "exit"])
    def test_divide_resulting_in_float(self, mock_input, capsys):
        """Test division that results in a float."""
        main()
        captured = capsys.readouterr()
        assert "Result of Division (a / b)(5.0, 2.0) = 2.5" in captured.out

    @patch("builtins.input", side_effect=["ln", "2.718281828", "exit"])
    def test_ln_of_e_approximation(self, mock_input, capsys):
        """Test natural log of e approximation."""
        main()
        captured = capsys.readouterr()
        # Should contain the result (approximately 1.0)
        assert "Result of Natural logarithm (ln x)" in captured.out


class TestPowerOperation:
    """Test suite for power operation."""

    @patch("builtins.input", side_effect=["power", "2", "3", "exit"])
    def test_power_operation_basic(self, mock_input, capsys):
        """Test power operation 2^3 = 8."""
        main()
        captured = capsys.readouterr()
        assert "Result of Power (x ^ y)(2.0, 3.0) = 8.0" in captured.out

    @patch("builtins.input", side_effect=["power", "5", "0", "exit"])
    def test_power_operation_exponent_zero(self, mock_input, capsys):
        """Test power operation with exponent 0."""
        main()
        captured = capsys.readouterr()
        assert "Result of Power (x ^ y)(5.0, 0.0) = 1.0" in captured.out


class TestCubeRootOperation:
    """Test suite for cube_root operation."""

    @patch("builtins.input", side_effect=["cube_root", "8", "exit"])
    def test_cube_root_positive_number(self, mock_input, capsys):
        """Test cube root of 8."""
        main()
        captured = capsys.readouterr()
        assert "Result of Cube root (∛x)(8.0) = 2.0" in captured.out

    @patch("builtins.input", side_effect=["cube_root", "-8", "exit"])
    def test_cube_root_negative_number(self, mock_input, capsys):
        """Test cube root of negative number."""
        main()
        captured = capsys.readouterr()
        # -8^(1/3) should be -2.0
        assert "Result of Cube root (∛x)(-8.0) = -2.0" in captured.out


class TestLogOperation:
    """Test suite for log operation."""

    @patch("builtins.input", side_effect=["log", "100", "exit"])
    def test_log_base_10_of_100(self, mock_input, capsys):
        """Test log base 10 of 100."""
        main()
        captured = capsys.readouterr()
        assert "Result of Base-10 logarithm (log₁₀ x)(100.0) = 2.0" in captured.out

    @patch("builtins.input", side_effect=["log", "1", "exit"])
    def test_log_base_10_of_1(self, mock_input, capsys):
        """Test log base 10 of 1."""
        main()
        captured = capsys.readouterr()
        assert "Result of Base-10 logarithm (log₁₀ x)(1.0) = 0.0" in captured.out


class TestFactorialOperation:
    """Test suite for factorial operation with integer conversion."""

    @patch("builtins.input", side_effect=["factorial", "5", "exit"])
    def test_factorial_of_5(self, mock_input, capsys):
        """Test factorial of 5."""
        main()
        captured = capsys.readouterr()
        assert "Result of Factorial (n!)(5) = 120" in captured.out

    @patch("builtins.input", side_effect=["factorial", "0", "exit"])
    def test_factorial_of_0(self, mock_input, capsys):
        """Test factorial of 0."""
        main()
        captured = capsys.readouterr()
        assert "Result of Factorial (n!)(0) = 1" in captured.out

    @patch("builtins.input", side_effect=["factorial", "-1", "exit"])
    def test_factorial_of_negative_number(self, mock_input, capsys):
        """Test that factorial of negative number is caught as error."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out


class TestEdgeCasesInInteractiveMode:
    """Test suite for edge cases in interactive mode."""

    @patch("builtins.input", side_effect=["divide", "0", "5", "exit"])
    def test_divide_zero_dividend(self, mock_input, capsys):
        """Test dividing zero by non-zero."""
        main()
        captured = capsys.readouterr()
        assert "Result of Division (a / b)(0.0, 5.0) = 0.0" in captured.out

    @patch("builtins.input", side_effect=["square", "0", "exit"])
    def test_square_of_zero(self, mock_input, capsys):
        """Test square of zero."""
        main()
        captured = capsys.readouterr()
        assert "Result of Square (x^2)(0.0) = 0.0" in captured.out

    @patch("builtins.input", side_effect=["multiply", "-5", "-3", "exit"])
    def test_multiply_negative_numbers(self, mock_input, capsys):
        """Test multiplying two negative numbers."""
        main()
        captured = capsys.readouterr()
        assert "Result of Multiplication (a * b)(-5.0, -3.0) = 15.0" in captured.out

    @patch("builtins.input", side_effect=["add", "1e10", "2e10", "exit"])
    def test_add_large_numbers(self, mock_input, capsys):
        """Test addition of very large numbers."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(10000000000.0, 20000000000.0) = 30000000000.0" in captured.out
