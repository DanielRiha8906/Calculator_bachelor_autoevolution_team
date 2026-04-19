"""Comprehensive pytest tests for the REPL interface.

Tests cover:
- get_operation_selection: valid/invalid inputs, quit handling
- get_operand: numeric inputs, default carry-over, re-prompting
- run: unary and binary operations, error handling, EOF/KeyboardInterrupt
- display_result: output format
- REPLInterface integration
- src/__init__ exports
- src/__main__ main() function
"""

import pytest
import math
from unittest.mock import Mock, patch, call, MagicMock
from io import StringIO

from src.repl import REPLInterface, OPERATIONS
from src.calculator import Calculator
from src import REPLInterface as ImportedREPLInterface


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def calculator():
    """Provide a real Calculator instance."""
    return Calculator()


@pytest.fixture
def repl(calculator):
    """Provide a REPLInterface instance with a real Calculator."""
    return REPLInterface(calculator)


@pytest.fixture
def mock_calculator():
    """Provide a mocked Calculator instance for testing."""
    return Mock(spec=Calculator)


@pytest.fixture
def mock_repl(mock_calculator):
    """Provide a REPLInterface instance with a mocked Calculator."""
    return REPLInterface(mock_calculator)


# ==============================================================================
# TESTS: get_operation_selection
# ==============================================================================

class TestGetOperationSelection:
    """Test suite for get_operation_selection method."""

    def test_valid_selection_first_operation(self, repl):
        """Test valid selection of first operation (add)."""
        with patch("builtins.input", return_value="1"):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_valid_selection_last_operation(self, repl):
        """Test valid selection of last operation (natural_logarithm)."""
        with patch("builtins.input", return_value="12"):
            result = repl.get_operation_selection()
        assert result == "natural_logarithm"

    def test_valid_selection_middle_operation(self, repl):
        """Test valid selection of middle operation (logarithm)."""
        with patch("builtins.input", return_value="6"):
            result = repl.get_operation_selection()
        assert result == "logarithm"

    def test_quit_lowercase(self, repl):
        """Test 'quit' input in lowercase."""
        with patch("builtins.input", return_value="quit"):
            result = repl.get_operation_selection()
        assert result == "quit"

    def test_quit_uppercase(self, repl):
        """Test 'quit' input in uppercase."""
        with patch("builtins.input", return_value="QUIT"):
            result = repl.get_operation_selection()
        assert result == "quit"

    def test_quit_mixed_case(self, repl):
        """Test 'quit' input in mixed case."""
        with patch("builtins.input", return_value="QuIt"):
            result = repl.get_operation_selection()
        assert result == "quit"

    def test_invalid_selection_zero(self, repl):
        """Test out-of-range selection (0) re-prompts."""
        with patch("builtins.input", side_effect=["0", "1"]):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_invalid_selection_beyond_max(self, repl):
        """Test out-of-range selection (99) re-prompts."""
        with patch("builtins.input", side_effect=["99", "3"]):
            result = repl.get_operation_selection()
        assert result == "multiply"

    def test_invalid_selection_negative(self, repl):
        """Test negative number selection re-prompts."""
        with patch("builtins.input", side_effect=["-1", "2"]):
            result = repl.get_operation_selection()
        assert result == "subtract"

    def test_non_numeric_input(self, repl):
        """Test non-numeric input re-prompts."""
        with patch("builtins.input", side_effect=["abc", "4"]):
            result = repl.get_operation_selection()
        assert result == "divide"

    def test_special_characters_input(self, repl):
        """Test special characters input re-prompts."""
        with patch("builtins.input", side_effect=["!@#$", "5"]):
            result = repl.get_operation_selection()
        assert result == "power"

    def test_multiple_invalid_then_valid(self, repl):
        """Test multiple invalid inputs before valid selection."""
        with patch("builtins.input", side_effect=["abc", "99", "0", "7"]):
            result = repl.get_operation_selection()
        assert result == "factorial"

    def test_input_with_leading_trailing_whitespace(self, repl):
        """Test that input with whitespace is handled correctly."""
        with patch("builtins.input", return_value="  3  "):
            result = repl.get_operation_selection()
        assert result == "multiply"

    def test_float_input_reprompts(self, repl):
        """Test that float input re-prompts."""
        with patch("builtins.input", side_effect=["2.5", "10"]):
            result = repl.get_operation_selection()
        assert result == "square_root"

    def test_empty_input_reprompts(self, repl):
        """Test that empty input re-prompts."""
        with patch("builtins.input", side_effect=["", "1"]):
            result = repl.get_operation_selection()
        assert result == "add"


# ==============================================================================
# TESTS: get_operand
# ==============================================================================

class TestGetOperand:
    """Test suite for get_operand method."""

    def test_valid_integer_input(self, repl):
        """Test valid integer input."""
        with patch("builtins.input", return_value="42"):
            result = repl.get_operand("Enter value: ")
        assert result == 42.0
        assert isinstance(result, float)

    def test_valid_float_input(self, repl):
        """Test valid float input."""
        with patch("builtins.input", return_value="3.14"):
            result = repl.get_operand("Enter value: ")
        assert result == 3.14

    def test_valid_negative_input(self, repl):
        """Test valid negative number input."""
        with patch("builtins.input", return_value="-7.5"):
            result = repl.get_operand("Enter value: ")
        assert result == -7.5

    def test_valid_zero_input(self, repl):
        """Test valid zero input."""
        with patch("builtins.input", return_value="0"):
            result = repl.get_operand("Enter value: ")
        assert result == 0.0

    def test_empty_input_with_last_result_set(self, repl):
        """Test empty input returns last_result when it is set."""
        repl.last_result = 42.0
        with patch("builtins.input", return_value=""):
            result = repl.get_operand("Enter value: ")
        assert result == 42.0

    def test_empty_input_with_last_result_none_reprompts(self, repl):
        """Test empty input re-prompts when last_result is None."""
        repl.last_result = None
        with patch("builtins.input", side_effect=["", "10"]):
            result = repl.get_operand("Enter value: ")
        assert result == 10.0

    def test_non_numeric_input_reprompts(self, repl):
        """Test non-numeric input re-prompts."""
        with patch("builtins.input", side_effect=["abc", "5"]):
            result = repl.get_operand("Enter value: ")
        assert result == 5.0

    def test_multiple_invalid_inputs_before_valid(self, repl):
        """Test multiple invalid inputs before valid."""
        with patch("builtins.input", side_effect=["xyz", "!", "not_a_number", "2.718"]):
            result = repl.get_operand("Enter value: ")
        assert result == 2.718

    def test_whitespace_stripped_from_input(self, repl):
        """Test that whitespace is stripped from input."""
        with patch("builtins.input", return_value="  15.5  "):
            result = repl.get_operand("Enter value: ")
        assert result == 15.5

    def test_empty_input_with_zero_last_result_returns_zero(self, repl):
        """Test empty input with last_result=0.0 returns 0.0."""
        repl.last_result = 0.0
        with patch("builtins.input", return_value=""):
            result = repl.get_operand("Enter value: ")
        assert result == 0.0

    def test_scientific_notation_input(self, repl):
        """Test scientific notation input."""
        with patch("builtins.input", return_value="1e5"):
            result = repl.get_operand("Enter value: ")
        assert result == 100000.0

    def test_very_large_number(self, repl):
        """Test very large number input."""
        with patch("builtins.input", return_value="999999999999999.99"):
            result = repl.get_operand("Enter value: ")
        assert result == 999999999999999.99

    def test_very_small_number(self, repl):
        """Test very small number input."""
        with patch("builtins.input", return_value="0.0000001"):
            result = repl.get_operand("Enter value: ")
        assert result == 0.0000001


# ==============================================================================
# TESTS: display_result
# ==============================================================================

class TestDisplayResult:
    """Test suite for display_result method."""

    def test_display_result_unary_operation(self, repl, capsys):
        """Test display format for unary operation."""
        repl.display_result("factorial", [5.0], 120)
        captured = capsys.readouterr()
        assert "Factorial(5.0) = 120" in captured.out

    def test_display_result_binary_operation(self, repl, capsys):
        """Test display format for binary operation."""
        repl.display_result("add", [3.0, 4.0], 7.0)
        captured = capsys.readouterr()
        assert "Addition(3.0, 4.0) = 7.0" in captured.out

    def test_display_result_with_float_result(self, repl, capsys):
        """Test display with float result."""
        repl.display_result("divide", [10.0, 3.0], 3.3333333)
        captured = capsys.readouterr()
        assert "Division(10.0, 3.0) = 3.3333333" in captured.out

    def test_display_result_logarithm(self, repl, capsys):
        """Test display format for logarithm operation."""
        repl.display_result("logarithm", [8.0, 2.0], 3.0)
        captured = capsys.readouterr()
        assert "Logarithm (base)(8.0, 2.0) = 3.0" in captured.out

    def test_display_result_square_root(self, repl, capsys):
        """Test display format for square root operation."""
        repl.display_result("square_root", [16.0], 4.0)
        captured = capsys.readouterr()
        assert "Square Root(16.0) = 4.0" in captured.out


# ==============================================================================
# TESTS: run() - UNARY OPERATIONS
# ==============================================================================

class TestRunUnaryOperations:
    """Test suite for run() with unary operations."""

    def test_run_factorial_happy_path(self, repl, capsys):
        """Test factorial operation happy path."""
        # Input: 7 (factorial), 5 (operand), quit
        with patch("builtins.input", side_effect=["7", "5", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Factorial(5.0) = 120" in captured.out
        assert repl.last_result == 120

    def test_run_square_happy_path(self, repl, capsys):
        """Test square operation happy path."""
        with patch("builtins.input", side_effect=["8", "7", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Square(7.0) = 49.0" in captured.out
        assert repl.last_result == 49.0

    def test_run_cube_happy_path(self, repl, capsys):
        """Test cube operation happy path."""
        with patch("builtins.input", side_effect=["9", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Cube(3.0) = 27.0" in captured.out
        assert repl.last_result == 27.0

    def test_run_square_root_happy_path(self, repl, capsys):
        """Test square root operation happy path."""
        with patch("builtins.input", side_effect=["10", "25", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Square Root(25.0) = 5.0" in captured.out
        assert repl.last_result == 5.0

    def test_run_cube_root_happy_path(self, repl, capsys):
        """Test cube root operation happy path."""
        with patch("builtins.input", side_effect=["11", "8", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Cube Root(8.0) = 2.0" in captured.out

    def test_run_natural_logarithm_happy_path(self, repl, capsys):
        """Test natural logarithm operation happy path."""
        with patch("builtins.input", side_effect=["12", "2.718281828", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Natural Logarithm" in captured.out
        assert "1." in captured.out  # approximately 1.0

    def test_run_unary_operation_carries_result_to_next(self, repl, capsys):
        """Test that unary operation result is available as default for next operation."""
        # First operation: square 4 -> 16
        # Second operation: use default 16 for square -> 256
        # Third operation: quit
        with patch("builtins.input", side_effect=["8", "4", "8", "", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Square(4.0) = 16.0" in captured.out
        assert "Square(16.0) = 256.0" in captured.out


# ==============================================================================
# TESTS: run() - BINARY OPERATIONS
# ==============================================================================

class TestRunBinaryOperations:
    """Test suite for run() with binary operations."""

    def test_run_add_happy_path(self, repl, capsys):
        """Test addition operation happy path."""
        with patch("builtins.input", side_effect=["1", "3", "4", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Addition(3.0, 4.0) = 7.0" in captured.out
        assert repl.last_result == 7.0

    def test_run_subtract_happy_path(self, repl, capsys):
        """Test subtraction operation happy path."""
        with patch("builtins.input", side_effect=["2", "10", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Subtraction(10.0, 3.0) = 7.0" in captured.out
        assert repl.last_result == 7.0

    def test_run_multiply_happy_path(self, repl, capsys):
        """Test multiplication operation happy path."""
        with patch("builtins.input", side_effect=["3", "5", "6", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Multiplication(5.0, 6.0) = 30.0" in captured.out
        assert repl.last_result == 30.0

    def test_run_divide_happy_path(self, repl, capsys):
        """Test division operation happy path."""
        with patch("builtins.input", side_effect=["4", "12", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Division(12.0, 3.0) = 4.0" in captured.out
        assert repl.last_result == 4.0

    def test_run_power_happy_path(self, repl, capsys):
        """Test power operation happy path."""
        with patch("builtins.input", side_effect=["5", "2", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Power(2.0, 3.0) = 8.0" in captured.out
        assert repl.last_result == 8.0

    def test_run_binary_operation_first_operand_default(self, repl, capsys):
        """Test that binary operation first operand uses last_result as default."""
        # First operation: 5 + 3 = 8
        # Second operation: use default 8 for first operand, 2 for second
        # Third operation: quit
        with patch("builtins.input", side_effect=["1", "5", "3", "2", "", "2", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Addition(5.0, 3.0) = 8.0" in captured.out
        assert "Subtraction(8.0, 2.0) = 6.0" in captured.out

    def test_run_binary_operation_second_operand_no_default(self, repl, capsys):
        """Test that binary operation second operand has no default."""
        # First operation: 10 + 5 = 15
        # Second operation: try empty string for second operand (should fail because last_result was set to None)
        # Then provide a valid second operand
        with patch("builtins.input", side_effect=["1", "10", "5", "2", "15", "", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        # First addition should work
        assert "Addition(10.0, 5.0) = 15.0" in captured.out
        # Second subtraction's second operand: empty should re-prompt, then we provide empty again
        # which should fail and show "Invalid number"
        assert "Invalid number" in captured.out


# ==============================================================================
# TESTS: run() - LOGARITHM OPERATION (special handling)
# ==============================================================================

class TestRunLogarithm:
    """Test suite for run() with logarithm operation (arity 2, special dispatch)."""

    def test_run_logarithm_valid_base_and_value(self, repl, capsys):
        """Test logarithm with valid base and value."""
        with patch("builtins.input", side_effect=["6", "8", "2", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Logarithm (base)(8.0, 2.0) = 3.0" in captured.out
        assert repl.last_result == 3.0

    def test_run_logarithm_base_zero_raises_error(self, repl, capsys):
        """Test logarithm with base 0 raises ValueError."""
        with patch("builtins.input", side_effect=["6", "8", "0", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "logarithm base must be positive and not equal to 1" in captured.out
        assert repl.last_result is None

    def test_run_logarithm_base_one_raises_error(self, repl, capsys):
        """Test logarithm with base 1 raises ValueError."""
        with patch("builtins.input", side_effect=["6", "8", "1", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "logarithm base must be positive and not equal to 1" in captured.out
        assert repl.last_result is None

    def test_run_logarithm_negative_base_raises_error(self, repl, capsys):
        """Test logarithm with negative base raises ValueError."""
        with patch("builtins.input", side_effect=["6", "8", "-2", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_run_logarithm_non_positive_x_raises_error(self, repl, capsys):
        """Test logarithm with non-positive x raises ValueError."""
        with patch("builtins.input", side_effect=["6", "0", "2", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "logarithm() not defined for non-positive values" in captured.out

    def test_run_logarithm_negative_x_raises_error(self, repl, capsys):
        """Test logarithm with negative x raises ValueError."""
        with patch("builtins.input", side_effect=["6", "-5", "2", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out


# ==============================================================================
# TESTS: run() - ERROR HANDLING
# ==============================================================================

class TestRunErrorHandling:
    """Test suite for run() error handling."""

    def test_run_divide_by_zero_error(self, repl, capsys):
        """Test division by zero raises ZeroDivisionError."""
        with patch("builtins.input", side_effect=["4", "10", "0", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "Cannot divide by zero" in captured.out
        assert repl.last_result is None

    def test_run_square_root_negative_error(self, repl, capsys):
        """Test square root of negative raises ValueError."""
        with patch("builtins.input", side_effect=["10", "-4", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "square_root() not defined for negative values" in captured.out
        assert repl.last_result is None

    def test_run_factorial_non_integer_float_error(self, repl, capsys):
        """Test factorial of non-integer float raises TypeError."""
        with patch("builtins.input", side_effect=["7", "2.5", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "factorial() only accepts integer values" in captured.out
        assert repl.last_result is None

    def test_run_factorial_negative_error(self, repl, capsys):
        """Test factorial of negative number raises ValueError."""
        with patch("builtins.input", side_effect=["7", "-5", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "factorial() not defined for negative values" in captured.out

    def test_run_error_doesnt_update_last_result(self, repl, capsys):
        """Test that errors do not update last_result."""
        # Note: For binary operations, last_result is set to None before collecting
        # the second operand. So after collecting operands, last_result is None.
        # When error occurs, last_result stays at its current value (None for binary ops).
        # For unary operations, last_result retains its previous value.
        repl.last_result = 10.0
        # Use unary operation (square_root) with negative number to trigger error
        with patch("builtins.input", side_effect=["10", "-4", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert repl.last_result == 10.0  # Unchanged

    def test_run_loop_continues_after_error(self, repl, capsys):
        """Test that REPL loop continues after an error."""
        with patch("builtins.input", side_effect=["4", "0", "0", "1", "2", "3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "Addition(2.0, 3.0) = 5.0" in captured.out


# ==============================================================================
# TESTS: run() - EOF / KEYBOARD INTERRUPT
# ==============================================================================

class TestRunEOFKeyboardInterrupt:
    """Test suite for run() EOF and KeyboardInterrupt handling."""

    def test_run_eof_during_operation_selection(self, repl, capsys):
        """Test EOF during operation selection."""
        with patch("builtins.input", side_effect=EOFError):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out

    def test_run_keyboard_interrupt_during_operation_selection(self, repl, capsys):
        """Test KeyboardInterrupt during operation selection."""
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out

    def test_run_eof_during_operand_collection(self, repl, capsys):
        """Test EOF during operand collection."""
        # First input returns a valid operation, second input raises EOFError
        def input_side_effect(prompt=""):
            if "Select operation:" in prompt or not hasattr(input_side_effect, "called"):
                input_side_effect.called = True
                return "1"
            raise EOFError

        with patch("builtins.input", side_effect=["1", EOFError()]):
            # We need to trigger the EOFError on the second input (operand collection)
            # Let's use a different approach
            pass

        # Better approach: simulate two inputs, second raises EOFError
        inputs = iter(["1"])
        def mock_input(prompt=""):
            try:
                return next(inputs)
            except StopIteration:
                raise EOFError

        with patch("builtins.input", side_effect=mock_input):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out

    def test_run_keyboard_interrupt_during_operand_collection(self, repl, capsys):
        """Test KeyboardInterrupt during operand collection."""
        inputs = iter(["1"])
        def mock_input(prompt=""):
            try:
                return next(inputs)
            except StopIteration:
                raise KeyboardInterrupt

        with patch("builtins.input", side_effect=mock_input):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out


# ==============================================================================
# TESTS: run() - INTEGRATION AND WORKFLOW
# ==============================================================================

class TestRunIntegration:
    """Integration tests for run() method."""

    def test_run_welcome_message(self, repl, capsys):
        """Test that welcome message is displayed."""
        with patch("builtins.input", side_effect=["quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Welcome to the Calculator REPL" in captured.out

    def test_run_quit_message(self, repl, capsys):
        """Test that quit message is displayed."""
        with patch("builtins.input", side_effect=["quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out

    def test_run_multiple_operations_in_sequence(self, repl, capsys):
        """Test multiple operations in sequence with last_result carry-over."""
        # 1. Add 5 + 3 = 8
        # 2. Multiply by default 8 * 2 = 16
        # 3. Square 16 = 256
        with patch("builtins.input", side_effect=["1", "5", "3", "3", "", "2", "8", "16", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Addition(5.0, 3.0) = 8.0" in captured.out
        assert "Multiplication(8.0, 2.0) = 16.0" in captured.out
        assert "Square(16.0) = 256.0" in captured.out

    def test_run_operations_menu_displayed(self, repl, capsys):
        """Test that operations menu is displayed."""
        with patch("builtins.input", side_effect=["quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Available operations:" in captured.out
        assert "Addition" in captured.out
        assert "quit" in captured.out.lower()


# ==============================================================================
# TESTS: _execute method
# ==============================================================================

class TestExecute:
    """Test suite for _execute method."""

    def test_execute_add(self, repl):
        """Test _execute dispatches add correctly."""
        result = repl._execute("add", [3.0, 4.0])
        assert result == 7.0

    def test_execute_subtract(self, repl):
        """Test _execute dispatches subtract correctly."""
        result = repl._execute("subtract", [10.0, 3.0])
        assert result == 7.0

    def test_execute_multiply(self, repl):
        """Test _execute dispatches multiply correctly."""
        result = repl._execute("multiply", [5.0, 6.0])
        assert result == 30.0

    def test_execute_divide(self, repl):
        """Test _execute dispatches divide correctly."""
        result = repl._execute("divide", [12.0, 3.0])
        assert result == 4.0

    def test_execute_power(self, repl):
        """Test _execute dispatches power correctly."""
        result = repl._execute("power", [2.0, 3.0])
        assert result == 8.0

    def test_execute_factorial(self, repl):
        """Test _execute dispatches factorial correctly."""
        result = repl._execute("factorial", [5.0])
        assert result == 120

    def test_execute_square(self, repl):
        """Test _execute dispatches square correctly."""
        result = repl._execute("square", [7.0])
        assert result == 49.0

    def test_execute_cube(self, repl):
        """Test _execute dispatches cube correctly."""
        result = repl._execute("cube", [3.0])
        assert result == 27.0

    def test_execute_square_root(self, repl):
        """Test _execute dispatches square_root correctly."""
        result = repl._execute("square_root", [16.0])
        assert result == 4.0

    def test_execute_cube_root(self, repl):
        """Test _execute dispatches cube_root correctly."""
        result = repl._execute("cube_root", [8.0])
        assert result == 2.0

    def test_execute_natural_logarithm(self, repl):
        """Test _execute dispatches natural_logarithm correctly."""
        result = repl._execute("natural_logarithm", [2.718281828])
        assert abs(result - 1.0) < 0.001

    def test_execute_logarithm_uses_math_log(self, repl):
        """Test _execute uses math.log directly for logarithm."""
        result = repl._execute("logarithm", [8.0, 2.0])
        assert result == 3.0

    def test_execute_logarithm_base_validation(self, repl):
        """Test _execute validates logarithm base."""
        with pytest.raises(ValueError):
            repl._execute("logarithm", [8.0, 1.0])

    def test_execute_logarithm_x_validation(self, repl):
        """Test _execute validates logarithm x."""
        with pytest.raises(ValueError):
            repl._execute("logarithm", [0.0, 2.0])


# ==============================================================================
# TESTS: _first_operand_prompt helper
# ==============================================================================

class TestFirstOperandPrompt:
    """Test suite for _first_operand_prompt helper method."""

    def test_first_operand_prompt_with_last_result(self, repl):
        """Test prompt includes last_result when set."""
        repl.last_result = 42.0
        prompt = repl._first_operand_prompt("value")
        assert "42.0" in prompt
        assert "default" in prompt.lower()

    def test_first_operand_prompt_without_last_result(self, repl):
        """Test prompt without last_result when None."""
        repl.last_result = None
        prompt = repl._first_operand_prompt("value")
        assert "default" not in prompt.lower()
        assert "Enter value:" in prompt

    def test_first_operand_prompt_custom_label(self, repl):
        """Test prompt with custom label."""
        repl.last_result = None
        prompt = repl._first_operand_prompt("first value")
        assert "first value" in prompt


# ==============================================================================
# TESTS: REPL Initialization
# ==============================================================================

class TestREPLInitialization:
    """Test suite for REPLInterface initialization."""

    def test_repl_init_stores_calculator(self, calculator):
        """Test __init__ stores calculator reference."""
        repl = REPLInterface(calculator)
        assert repl.calculator is calculator

    def test_repl_init_sets_last_result_none(self, calculator):
        """Test __init__ initializes last_result to None."""
        repl = REPLInterface(calculator)
        assert repl.last_result is None

    def test_repl_init_with_mock_calculator(self, mock_calculator):
        """Test __init__ works with mocked calculator."""
        repl = REPLInterface(mock_calculator)
        assert repl.calculator is mock_calculator
        assert repl.last_result is None


# ==============================================================================
# TESTS: src/__init__ exports
# ==============================================================================

class TestModuleExports:
    """Test suite for module exports."""

    def test_repl_interface_exported_from_src(self):
        """Test that REPLInterface is exported from src package."""
        assert ImportedREPLInterface is REPLInterface

    def test_repl_interface_in_all(self):
        """Test that REPLInterface is in __all__."""
        from src import __all__
        assert "REPLInterface" in __all__


# ==============================================================================
# TESTS: src/__main__ main() function
# ==============================================================================

class TestMainFunction:
    """Test suite for main() function in src/__main__."""

    def test_main_calls_repl_run(self):
        """Test that main() creates and runs a REPLInterface."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run") as mock_run:
            with patch("src.__main__.Calculator"):
                main(argv=[])
        mock_run.assert_called_once()

    def test_main_catches_eof_error(self):
        """Test that main() catches EOFError from repl.run()."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=EOFError):
            # Should not raise
            main(argv=[])

    def test_main_catches_keyboard_interrupt(self):
        """Test that main() catches KeyboardInterrupt from repl.run()."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=KeyboardInterrupt):
            # Should not raise
            main(argv=[])

    def test_main_prints_closed_message_on_eof(self, capsys):
        """Test that main() prints closed message on EOFError."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=EOFError):
            main(argv=[])
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out


# ==============================================================================
# EDGE CASES AND ADDITIONAL COVERAGE
# ==============================================================================

class TestEdgeCasesAndAdditionalCoverage:
    """Test suite for edge cases and additional coverage."""

    def test_get_operand_very_large_float(self, repl):
        """Test get_operand with very large float."""
        with patch("builtins.input", return_value="1e308"):
            result = repl.get_operand("Enter: ")
        assert result == 1e308

    def test_get_operand_very_small_float(self, repl):
        """Test get_operand with very small float."""
        with patch("builtins.input", return_value="1e-308"):
            result = repl.get_operand("Enter: ")
        assert result == 1e-308

    def test_operations_dict_integrity(self):
        """Test that OPERATIONS dict has correct structure."""
        assert len(OPERATIONS) == 12
        assert all("arity" in op_meta for op_meta in OPERATIONS.values())
        assert all("name" in op_meta for op_meta in OPERATIONS.values())

    def test_operations_dict_arities(self):
        """Test that operations have correct arities."""
        unary_ops = ["factorial", "square", "cube", "square_root", "cube_root", "natural_logarithm"]
        binary_ops = ["add", "subtract", "multiply", "divide", "power", "logarithm"]

        for op in unary_ops:
            assert OPERATIONS[op]["arity"] == 1

        for op in binary_ops:
            assert OPERATIONS[op]["arity"] == 2

    def test_run_large_integer_input(self, repl, capsys):
        """Test run with large integer input."""
        with patch("builtins.input", side_effect=["1", "999999", "1", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Addition(999999.0, 1.0) = 1000000.0" in captured.out

    def test_run_negative_number_operations(self, repl, capsys):
        """Test run with negative number operations."""
        with patch("builtins.input", side_effect=["2", "-5", "-3", "quit"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Subtraction(-5.0, -3.0) = -2.0" in captured.out

    def test_get_operation_selection_boundary_values(self, repl):
        """Test get_operation_selection with boundary values."""
        # Test min and max valid selections
        with patch("builtins.input", return_value="1"):
            result = repl.get_operation_selection()
        assert result == "add"

        with patch("builtins.input", return_value="12"):
            result = repl.get_operation_selection()
        assert result == "natural_logarithm"

    def test_display_result_with_integer_operands(self, repl, capsys):
        """Test display_result handles integer operands."""
        repl.display_result("add", [1, 2], 3)
        captured = capsys.readouterr()
        assert "Addition(1, 2) = 3" in captured.out

    def test_display_result_with_many_operands(self, repl, capsys):
        """Test display_result joins multiple operands correctly."""
        repl.display_result("logarithm", [8.0, 2.0], 3.0)
        captured = capsys.readouterr()
        assert "8.0, 2.0" in captured.out

    def test_run_mixed_operation_types(self, repl, capsys):
        """Test run with mixed unary and binary operations."""
        # 1. Square operation (unary): input 8, operand 4 -> 16
        # 2. Addition operation (binary): input 1, first 16 (default), second 9 -> 25
        # 3. Quit
        with patch("builtins.input", side_effect=[
            "8",     # Operation: Square
            "4",     # Operand: 4
            "1",     # Operation: Add
            "",      # First operand: use default (16)
            "9",     # Second operand: 9
            "quit"   # Quit
        ]):
            repl.run()
        captured = capsys.readouterr()
        assert "Square(4.0) = 16.0" in captured.out
        assert "Addition(16.0, 9.0) = 25.0" in captured.out


# ==============================================================================
# STRESS AND ROBUSTNESS TESTS
# ==============================================================================

class TestStressAndRobustness:
    """Stress tests for robustness."""

    def test_many_invalid_inputs_eventually_valid(self, repl):
        """Test that many invalid inputs eventually work."""
        invalid_inputs = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
        inputs = invalid_inputs + ["1"]
        with patch("builtins.input", side_effect=inputs):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_repeated_error_operations(self, repl, capsys):
        """Test multiple error operations in a row."""
        with patch("builtins.input", side_effect=[
            "4", "1", "0",  # Divide by 0 - error
            "4", "2", "0",  # Divide by 0 - error
            "4", "3", "0",  # Divide by 0 - error
            "quit"
        ]):
            repl.run()
        captured = capsys.readouterr()
        # Should have three error messages
        assert captured.out.count("Error:") == 3
