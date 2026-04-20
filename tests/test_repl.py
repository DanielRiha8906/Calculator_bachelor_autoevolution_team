"""Comprehensive pytest tests for the REPL interface.

Tests cover:
- get_operation_selection: valid/invalid inputs, quit handling
- get_operand: numeric inputs, default carry-over, re-prompting
- run: unary and binary operations, error handling, EOF/KeyboardInterrupt
- display_result: output format
- REPLInterface integration
- src/__init__ exports
- src/__main__ main() function
- Retry logic: MAX_RETRIES, MaxRetriesExceeded exception
- Input validation helpers: _is_valid_operand, _is_valid_operation_input
"""

import pytest
import math
from unittest.mock import Mock, patch, call, MagicMock
from io import StringIO

from src.repl import REPLInterface, OPERATIONS, MAX_RETRIES
from src.calculator import Calculator
from src.exceptions import MaxRetriesExceeded
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
    return REPLInterface(calculator, error_logger=None)


@pytest.fixture
def mock_calculator():
    """Provide a mocked Calculator instance for testing."""
    return Mock(spec=Calculator)


@pytest.fixture
def mock_repl(mock_calculator):
    """Provide a REPLInterface instance with a mocked Calculator."""
    return REPLInterface(mock_calculator, error_logger=None)


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
        """Test two invalid inputs before valid selection."""
        # 3 inputs will raise exception, so use only 2 invalid before valid
        with patch("builtins.input", side_effect=["abc", "99", "7"]):
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
        """Test two invalid inputs before valid."""
        # 3 inputs will raise exception, so use only 2 invalid before valid
        with patch("builtins.input", side_effect=["xyz", "!", "2.718"]):
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
# TESTS: Input Validation Helpers
# ==============================================================================

class TestInputValidationHelpers:
    """Test suite for input validation helper methods."""

    # =========================================================================
    # _is_valid_operand Tests
    # =========================================================================

    def test_is_valid_operand_integer(self, repl):
        """Test _is_valid_operand returns True for valid integer."""
        assert repl._is_valid_operand("42") is True

    def test_is_valid_operand_negative_integer(self, repl):
        """Test _is_valid_operand returns True for negative integer."""
        assert repl._is_valid_operand("-42") is True

    def test_is_valid_operand_float(self, repl):
        """Test _is_valid_operand returns True for valid float."""
        assert repl._is_valid_operand("3.14") is True

    def test_is_valid_operand_negative_float(self, repl):
        """Test _is_valid_operand returns True for negative float."""
        assert repl._is_valid_operand("-2.718") is True

    def test_is_valid_operand_zero(self, repl):
        """Test _is_valid_operand returns True for zero."""
        assert repl._is_valid_operand("0") is True

    def test_is_valid_operand_zero_float(self, repl):
        """Test _is_valid_operand returns True for 0.0."""
        assert repl._is_valid_operand("0.0") is True

    def test_is_valid_operand_scientific_notation(self, repl):
        """Test _is_valid_operand returns True for scientific notation."""
        assert repl._is_valid_operand("1e5") is True
        assert repl._is_valid_operand("1.5e-10") is True
        assert repl._is_valid_operand("-3.2e4") is True

    def test_is_valid_operand_leading_whitespace(self, repl):
        """Test _is_valid_operand strips leading whitespace."""
        assert repl._is_valid_operand("  42") is True

    def test_is_valid_operand_trailing_whitespace(self, repl):
        """Test _is_valid_operand strips trailing whitespace."""
        assert repl._is_valid_operand("42  ") is True

    def test_is_valid_operand_both_whitespace(self, repl):
        """Test _is_valid_operand strips both leading and trailing whitespace."""
        assert repl._is_valid_operand("  42  ") is True

    def test_is_valid_operand_empty_string(self, repl):
        """Test _is_valid_operand returns False for empty string."""
        assert repl._is_valid_operand("") is False

    def test_is_valid_operand_whitespace_only(self, repl):
        """Test _is_valid_operand returns False for whitespace-only string."""
        assert repl._is_valid_operand("   ") is False

    def test_is_valid_operand_alphabetic_string(self, repl):
        """Test _is_valid_operand returns False for alphabetic string."""
        assert repl._is_valid_operand("abc") is False

    def test_is_valid_operand_mixed_alphanumeric(self, repl):
        """Test _is_valid_operand returns False for mixed alphanumeric."""
        assert repl._is_valid_operand("123abc") is False
        assert repl._is_valid_operand("abc123") is False

    def test_is_valid_operand_special_characters(self, repl):
        """Test _is_valid_operand returns False for special characters."""
        assert repl._is_valid_operand("!@#$%") is False
        assert repl._is_valid_operand("1+2") is False
        assert repl._is_valid_operand("1.2.3") is False

    def test_is_valid_operand_infinity(self, repl):
        """Test _is_valid_operand with infinity."""
        assert repl._is_valid_operand("inf") is True
        assert repl._is_valid_operand("-inf") is True

    def test_is_valid_operand_very_large_number(self, repl):
        """Test _is_valid_operand with very large number."""
        assert repl._is_valid_operand("1e308") is True

    def test_is_valid_operand_very_small_number(self, repl):
        """Test _is_valid_operand with very small number."""
        assert repl._is_valid_operand("1e-308") is True

    # =========================================================================
    # _is_valid_operation_input Tests
    # =========================================================================

    def test_is_valid_operation_input_quit_lowercase(self, repl):
        """Test _is_valid_operation_input returns True for 'quit'."""
        assert repl._is_valid_operation_input("quit") is True

    def test_is_valid_operation_input_quit_uppercase(self, repl):
        """Test _is_valid_operation_input returns True for 'QUIT'."""
        assert repl._is_valid_operation_input("QUIT") is True

    def test_is_valid_operation_input_quit_mixed_case(self, repl):
        """Test _is_valid_operation_input returns True for 'QuIt'."""
        assert repl._is_valid_operation_input("QuIt") is True

    def test_is_valid_operation_input_quit_with_whitespace(self, repl):
        """Test _is_valid_operation_input strips whitespace for 'quit'."""
        assert repl._is_valid_operation_input("  quit  ") is True

    def test_is_valid_operation_input_minimum_index(self, repl):
        """Test _is_valid_operation_input returns True for minimum valid index (1)."""
        assert repl._is_valid_operation_input("1") is True

    def test_is_valid_operation_input_maximum_index(self, repl):
        """Test _is_valid_operation_input returns True for maximum valid index (12)."""
        assert repl._is_valid_operation_input("12") is True

    def test_is_valid_operation_input_middle_index(self, repl):
        """Test _is_valid_operation_input returns True for middle valid index."""
        assert repl._is_valid_operation_input("6") is True

    def test_is_valid_operation_input_zero(self, repl):
        """Test _is_valid_operation_input returns False for 0."""
        assert repl._is_valid_operation_input("0") is False

    def test_is_valid_operation_input_negative(self, repl):
        """Test _is_valid_operation_input returns False for negative number."""
        assert repl._is_valid_operation_input("-1") is False

    def test_is_valid_operation_input_beyond_max(self, repl):
        """Test _is_valid_operation_input returns False for number > 12."""
        assert repl._is_valid_operation_input("13") is False
        assert repl._is_valid_operation_input("99") is False

    def test_is_valid_operation_input_float(self, repl):
        """Test _is_valid_operation_input returns False for float."""
        assert repl._is_valid_operation_input("1.5") is False

    def test_is_valid_operation_input_alphabetic(self, repl):
        """Test _is_valid_operation_input returns False for alphabetic string."""
        assert repl._is_valid_operation_input("abc") is False

    def test_is_valid_operation_input_empty_string(self, repl):
        """Test _is_valid_operation_input returns False for empty string."""
        assert repl._is_valid_operation_input("") is False

    def test_is_valid_operation_input_whitespace_only(self, repl):
        """Test _is_valid_operation_input returns False for whitespace-only string."""
        assert repl._is_valid_operation_input("   ") is False

    def test_is_valid_operation_input_special_characters(self, repl):
        """Test _is_valid_operation_input returns False for special characters."""
        assert repl._is_valid_operation_input("!@#$") is False

    def test_is_valid_operation_input_with_leading_whitespace(self, repl):
        """Test _is_valid_operation_input strips leading whitespace."""
        assert repl._is_valid_operation_input("  1") is True

    def test_is_valid_operation_input_with_trailing_whitespace(self, repl):
        """Test _is_valid_operation_input strips trailing whitespace."""
        assert repl._is_valid_operation_input("1  ") is True


# ==============================================================================
# TESTS: Retry Logic and MAX_RETRIES
# ==============================================================================

class TestRetryLogicAndMaxAttempts:
    """Test suite for retry logic and maximum attempt handling."""

    # =========================================================================
    # get_operand Retry Tests
    # =========================================================================

    def test_get_operand_invalid_then_valid_no_exception(self, repl):
        """Test get_operand accepts valid input after 1 invalid input."""
        with patch("builtins.input", side_effect=["invalid", "42"]):
            result = repl.get_operand("Enter value: ")
        assert result == 42.0

    def test_get_operand_exactly_two_invalid_then_valid(self, repl):
        """Test get_operand accepts valid input after exactly 2 invalid inputs."""
        with patch("builtins.input", side_effect=["bad1", "bad2", "3.14"]):
            result = repl.get_operand("Enter value: ")
        assert result == 3.14

    def test_get_operand_exactly_two_invalid_then_valid_resets(self, repl):
        """Test get_operand accepts valid input after exactly 2 invalid inputs (does not reach MAX_RETRIES)."""
        # 2 invalid attempts (attempts = 1, then 2), both < 3, so should continue and accept 3rd valid input
        with patch("builtins.input", side_effect=["!@#", "xyz", "100"]):
            result = repl.get_operand("Enter value: ")
        assert result == 100.0

    def test_get_operand_three_invalid_raises_exception(self, repl):
        """Test get_operand raises MaxRetriesExceeded after exactly 3 invalid inputs."""
        # After 3rd invalid input, attempts >= MAX_RETRIES (3 >= 3), so exception is raised
        with patch("builtins.input", side_effect=["bad1", "bad2", "bad3"]):
            with pytest.raises(MaxRetriesExceeded) as exc_info:
                repl.get_operand("Enter value: ")
        assert "Maximum retry attempts exceeded" in str(exc_info.value)

    def test_get_operand_many_invalid_raises_exception(self, repl):
        """Test get_operand raises MaxRetriesExceeded with many invalid inputs."""
        invalid_inputs = ["bad" + str(i) for i in range(10)]
        with patch("builtins.input", side_effect=invalid_inputs):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operand("Enter value: ")

    def test_get_operand_exception_message(self, repl):
        """Test get_operand exception has correct message."""
        with patch("builtins.input", side_effect=["x", "y", "z", "w"]):
            with pytest.raises(MaxRetriesExceeded) as exc_info:
                repl.get_operand("Enter value: ")
        assert str(exc_info.value) == "Maximum retry attempts exceeded. Session ended."

    def test_get_operand_empty_strings_count_as_invalid(self, repl):
        """Test that empty strings count as invalid attempts when last_result is None."""
        repl.last_result = None
        with patch("builtins.input", side_effect=["", "", "", ""]):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operand("Enter value: ")

    def test_get_operand_max_retries_constant(self, repl):
        """Test that MAX_RETRIES is exactly 3."""
        assert MAX_RETRIES == 3

    # =========================================================================
    # get_operation_selection Retry Tests
    # =========================================================================

    def test_get_operation_selection_invalid_then_valid_no_exception(self, repl):
        """Test get_operation_selection accepts valid input after 1 invalid input."""
        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_get_operation_selection_exactly_two_invalid_then_valid(self, repl):
        """Test get_operation_selection accepts valid input after exactly 2 invalid inputs."""
        with patch("builtins.input", side_effect=["0", "99", "2"]):
            result = repl.get_operation_selection()
        assert result == "subtract"

    def test_get_operation_selection_exactly_two_invalid_then_valid(self, repl):
        """Test get_operation_selection accepts valid input after exactly 2 invalid inputs (does not reach MAX_RETRIES)."""
        # 2 invalid attempts, attempts = 1 then 2, both < 3, so should accept 3rd valid input
        with patch("builtins.input", side_effect=["abc", "0", "1"]):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_get_operation_selection_three_invalid_raises_exception(self, repl):
        """Test get_operation_selection raises MaxRetriesExceeded after exactly 3 invalid inputs."""
        # After 3rd invalid input, attempts >= MAX_RETRIES (3 >= 3), so exception is raised
        with patch("builtins.input", side_effect=["bad1", "bad2", "bad3"]):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operation_selection()

    def test_get_operation_selection_three_out_of_range_raises_exception(self, repl):
        """Test get_operation_selection raises MaxRetriesExceeded after 3 out-of-range inputs."""
        with patch("builtins.input", side_effect=["0", "13", "99"]):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operation_selection()

    def test_get_operation_selection_mixed_invalid_types_raises_exception(self, repl):
        """Test get_operation_selection with mixed invalid types raises MaxRetriesExceeded."""
        with patch("builtins.input", side_effect=["abc", "0", "-1"]):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operation_selection()

    def test_get_operation_selection_non_integer_string_then_valid(self, repl):
        """Test get_operation_selection counts non-integer strings as invalid attempt."""
        with patch("builtins.input", side_effect=["2.5", "1"]):
            result = repl.get_operation_selection()
        assert result == "add"

    def test_get_operation_selection_exception_message(self, repl):
        """Test get_operation_selection exception has correct message."""
        with patch("builtins.input", side_effect=["x", "y", "z", "w"]):
            with pytest.raises(MaxRetriesExceeded) as exc_info:
                repl.get_operation_selection()
        assert str(exc_info.value) == "Maximum retry attempts exceeded. Session ended."

    # =========================================================================
    # Retry Counter Reset Tests
    # =========================================================================

    def test_retry_counter_resets_between_operations(self, repl, capsys):
        """Test that retry counter resets after successful input between different operations."""
        # Goal: show that retry counter for one context (e.g., get_operation_selection) is independent
        # Perform one operation successfully with some retries, then another with retries
        # Operation 1 (Add): 5 + 3 = 8
        # Operation 2 (Multiply): 8 * 2 = 16
        with patch("builtins.input", side_effect=[
            "abc",      # Invalid operation selection (attempts=1)
            "0",        # Invalid operation selection (attempts=2)
            "1",        # Valid: add
            "bad1",     # Invalid operand (attempts=1)
            "5",        # Valid first operand
            "3",        # Valid second operand
            "xyz",      # Invalid operation selection (attempts=1) - counter reset
            "3",        # Valid: multiply
            "bad2",     # Invalid operand (attempts=1) - counter reset
            "8",        # Valid first operand
            "2",        # Valid second operand
            "quit"      # Quit
        ]):
            repl.run()
        captured = capsys.readouterr()
        # First operation should succeed: add 5 + 3 = 8
        # Second operation should succeed: multiply 8 * 2 = 16
        assert "Addition" in captured.out
        assert "Multiplication" in captured.out

    def test_retry_counter_independent_between_operands(self, repl, capsys):
        """Test that retry counter is independent for each operand prompt."""
        # Single binary operation with retry attempts in both operands
        with patch("builtins.input", side_effect=[
            "1",        # Valid operation: add
            "bad1",     # Invalid first operand
            "5",        # Valid first operand
            "bad2",     # Invalid second operand
            "10",       # Valid second operand
            "quit"
        ]):
            repl.run()
        captured = capsys.readouterr()
        assert "Addition(5.0, 10.0) = 15.0" in captured.out

    def test_multiple_failed_operations_then_raises(self, repl, capsys):
        """Test that 3 invalid operation selections raises MaxRetriesExceeded."""
        with patch("builtins.input", side_effect=[
            "abc",      # Invalid (attempts=1)
            "0",        # Invalid (attempts=2)
            "99"        # Invalid (attempts=3) -> raises MaxRetriesExceeded
        ]):
            repl.run()
        captured = capsys.readouterr()
        assert "Maximum retry attempts exceeded" in captured.out

    # =========================================================================
    # run() with MaxRetriesExceeded Tests
    # =========================================================================

    def test_run_catches_max_retries_exceeded_during_operation_selection(self, repl, capsys):
        """Test run() catches MaxRetriesExceeded from get_operation_selection."""
        with patch("builtins.input", side_effect=["x", "y", "z", "w"]):
            repl.run()
        captured = capsys.readouterr()
        assert "Maximum retry attempts exceeded. Session ended." in captured.out

    def test_run_catches_max_retries_exceeded_during_operand_collection_first_operand(self, repl, capsys):
        """Test run() catches MaxRetriesExceeded from get_operand (first operand)."""
        with patch("builtins.input", side_effect=[
            "1",        # Valid operation: add
            "x", "y", "z", "w"  # Invalid operands (4 attempts)
        ]):
            repl.run()
        captured = capsys.readouterr()
        assert "Maximum retry attempts exceeded. Session ended." in captured.out

    def test_run_catches_max_retries_exceeded_during_operand_collection_second_operand(self, repl, capsys):
        """Test run() catches MaxRetriesExceeded from get_operand (second operand)."""
        with patch("builtins.input", side_effect=[
            "1",        # Valid operation: add
            "5",        # Valid first operand
            "x", "y", "z", "w"  # Invalid second operands (4 attempts)
        ]):
            repl.run()
        captured = capsys.readouterr()
        assert "Maximum retry attempts exceeded. Session ended." in captured.out

    def test_run_returns_after_max_retries_exceeded(self, repl):
        """Test run() returns cleanly after MaxRetriesExceeded."""
        with patch("builtins.input", side_effect=["x", "y", "z", "w"]):
            repl.run()  # Should not raise, should return cleanly

    def test_run_eof_takes_precedence_over_max_retries(self, repl, capsys):
        """Test that EOFError is caught before MaxRetriesExceeded could be raised."""
        inputs = iter(["1", "x", "y"])
        def mock_input(prompt=""):
            try:
                return next(inputs)
            except StopIteration:
                raise EOFError

        with patch("builtins.input", side_effect=mock_input):
            repl.run()
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out

    def test_run_keyboard_interrupt_takes_precedence_over_max_retries(self, repl, capsys):
        """Test that KeyboardInterrupt is caught before MaxRetriesExceeded could be raised."""
        inputs = iter(["1", "x", "y"])
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
# TESTS: MaxRetriesExceeded Exception
# ==============================================================================

class TestMaxRetriesExceededException:
    """Test suite for MaxRetriesExceeded exception class."""

    def test_max_retries_exceeded_is_exception(self):
        """Test MaxRetriesExceeded is a subclass of Exception."""
        assert issubclass(MaxRetriesExceeded, Exception)

    def test_max_retries_exceeded_can_be_instantiated(self):
        """Test MaxRetriesExceeded can be instantiated."""
        exc = MaxRetriesExceeded("Test message")
        assert isinstance(exc, MaxRetriesExceeded)
        assert isinstance(exc, Exception)

    def test_max_retries_exceeded_stores_message(self):
        """Test MaxRetriesExceeded stores the message."""
        msg = "Custom error message"
        exc = MaxRetriesExceeded(msg)
        assert str(exc) == msg

    def test_max_retries_exceeded_can_be_raised_and_caught(self):
        """Test MaxRetriesExceeded can be raised and caught."""
        with pytest.raises(MaxRetriesExceeded):
            raise MaxRetriesExceeded("Test")

    def test_max_retries_exceeded_can_be_caught_as_exception(self):
        """Test MaxRetriesExceeded can be caught as generic Exception."""
        with pytest.raises(Exception):
            raise MaxRetriesExceeded("Test")


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

    def test_many_invalid_inputs_raises_exception(self, repl):
        """Test that many invalid inputs raises MaxRetriesExceeded after 3."""
        invalid_inputs = ["!", "@", "#"]  # Exactly 3 invalid inputs
        with patch("builtins.input", side_effect=invalid_inputs):
            with pytest.raises(MaxRetriesExceeded):
                repl.get_operation_selection()

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


# ==============================================================================
# TESTS: REPLInterface Error Logging Integration
# ==============================================================================

class TestREPLInterfaceErrorLogging:
    """Test suite for error logging integration in REPLInterface."""

    def test_repl_logs_division_by_zero_error(self):
        """Test that REPL logs CALCULATION_ERROR on division by zero."""
        import tempfile
        from src.error_logger import ErrorLogger

        calc = Calculator()
        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = f"{tmpdir}/error.log"
            error_logger = ErrorLogger(error_file=error_log_path)
            error_logger.clear_errors()

            repl = REPLInterface(calc, error_logger=error_logger)

            with patch("builtins.input", side_effect=[
                "4",  # Operation: divide
                "10",  # First operand
                "0",   # Second operand (divide by 0)
                "quit"
            ]):
                repl.run()

            errors = error_logger.get_errors()
            assert len(errors) == 1
            assert "CALCULATION_ERROR" in errors[0]
            assert "divide" in errors[0]

    def test_repl_logs_value_error_for_invalid_math(self):
        """Test that REPL logs CALCULATION_ERROR on value error."""
        import tempfile
        from src.error_logger import ErrorLogger

        calc = Calculator()
        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = f"{tmpdir}/error.log"
            error_logger = ErrorLogger(error_file=error_log_path)
            error_logger.clear_errors()

            repl = REPLInterface(calc, error_logger=error_logger)

            with patch("builtins.input", side_effect=[
                "7",     # Operation: square_root
                "-5",    # Negative number (invalid for square root)
                "quit"
            ]):
                repl.run()

            errors = error_logger.get_errors()
            assert len(errors) == 1
            assert "CALCULATION_ERROR" in errors[0]

    def test_repl_logs_type_error_for_factorial_of_float(self):
        """Test that REPL logs CALCULATION_ERROR on type error."""
        import tempfile
        from src.error_logger import ErrorLogger

        calc = Calculator()
        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = f"{tmpdir}/error.log"
            error_logger = ErrorLogger(error_file=error_log_path)
            error_logger.clear_errors()

            repl = REPLInterface(calc, error_logger=error_logger)

            with patch("builtins.input", side_effect=[
                "7",     # Operation: factorial (index 7)
                "3.5",   # Float (invalid for factorial)
                "quit"
            ]):
                repl.run()

            errors = error_logger.get_errors()
            assert len(errors) == 1
            assert "CALCULATION_ERROR" in errors[0]

    def test_repl_successful_operation_not_logged_as_error(self):
        """Test that successful operations are not logged to error log."""
        import tempfile
        from src.error_logger import ErrorLogger

        calc = Calculator()
        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = f"{tmpdir}/error.log"
            error_logger = ErrorLogger(error_file=error_log_path)
            error_logger.clear_errors()

            repl = REPLInterface(calc, error_logger=error_logger)

            with patch("builtins.input", side_effect=[
                "1",   # Operation: add
                "5",   # First operand
                "3",   # Second operand
                "quit"
            ]):
                repl.run()

            errors = error_logger.get_errors()
            assert errors == []

    def test_repl_multiple_errors_all_logged(self):
        """Test that multiple errors are all logged."""
        import tempfile
        from src.error_logger import ErrorLogger

        calc = Calculator()
        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = f"{tmpdir}/error.log"
            error_logger = ErrorLogger(error_file=error_log_path)
            error_logger.clear_errors()

            repl = REPLInterface(calc, error_logger=error_logger)

            with patch("builtins.input", side_effect=[
                "4", "10", "0",      # Divide by 0 - error 1
                "4", "20", "0",      # Divide by 0 - error 2
                "7", "-1",           # Square root of negative - error 3
                "quit"
            ]):
                repl.run()

            errors = error_logger.get_errors()
            assert len(errors) == 3
            for error_line in errors:
                assert "CALCULATION_ERROR" in error_line

    def test_repl_with_none_error_logger_still_runs(self):
        """Test that REPL runs correctly with error_logger=None."""
        calc = Calculator()
        repl = REPLInterface(calc, error_logger=None)

        # Should not raise or crash even with errors
        with patch("builtins.input", side_effect=[
            "4", "10", "0",   # Divide by 0 - error but should continue
            "quit"
        ]):
            repl.run()  # Should not raise
